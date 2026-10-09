/* AM — site behaviour. No third-party scripts, no tracking. */
(function () {
  "use strict";
  var doc = document;

  /* Current year */
  doc.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* Mobile menu */
  var btn = doc.getElementById("menu-btn");
  var panel = doc.getElementById("menu-panel");
  var closeBtn = doc.getElementById("menu-close");
  if (btn && panel) {
    var lastFocus = null;
    var focusables = function () {
      return Array.prototype.slice.call(panel.querySelectorAll("a[href], button:not([disabled])"));
    };
    var openMenu = function () {
      lastFocus = doc.activeElement;
      panel.classList.add("open");
      doc.body.classList.add("menu-open");
      btn.setAttribute("aria-expanded", "true");
      if (closeBtn) closeBtn.focus();
    };
    var closeMenu = function (restore) {
      panel.classList.remove("open");
      doc.body.classList.remove("menu-open");
      btn.setAttribute("aria-expanded", "false");
      if (restore !== false) btn.focus();
    };
    btn.addEventListener("click", openMenu);
    if (closeBtn) closeBtn.addEventListener("click", function () { closeMenu(true); });
    panel.addEventListener("click", function (e) {
      var a = e.target.closest("a");
      if (a) closeMenu(false);
    });
    doc.addEventListener("keydown", function (e) {
      if (!panel.classList.contains("open")) return;
      if (e.key === "Escape") { closeMenu(true); return; }
      if (e.key === "Tab") {
        var f = focusables();
        if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && doc.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && doc.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    var mq = window.matchMedia("(min-width: 960px)");
    var onMq = function () { if (mq.matches && panel.classList.contains("open")) closeMenu(false); };
    if (mq.addEventListener) mq.addEventListener("change", onMq); else mq.addListener(onMq);
  }

  /* Scroll reveal */
  var reveals = doc.querySelectorAll(".reveal");
  if (reveals.length) {
    if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
      reveals.forEach(function (el) { io.observe(el); });
    } else {
      reveals.forEach(function (el) { el.classList.add("in"); });
    }
  }

  /* Cookie preferences (stored locally; no optional tools are currently loaded) */
  var KEY = "am_cookie_prefs";
  var prefsForm = doc.getElementById("cookie-prefs-form");
  window.AMConsent = {
    get: function () {
      try { return JSON.parse(localStorage.getItem(KEY)) || { analytics: false, marketing: false }; }
      catch (e) { return { analytics: false, marketing: false }; }
    }
  };
  if (prefsForm) {
    var cur = window.AMConsent.get();
    var a = prefsForm.elements.analytics, m = prefsForm.elements.marketing;
    a.checked = !!cur.analytics; m.checked = !!cur.marketing;
    var msg = doc.getElementById("cookie-prefs-msg");
    prefsForm.addEventListener("submit", function (e) {
      e.preventDefault();
      try {
        localStorage.setItem(KEY, JSON.stringify({ analytics: a.checked, marketing: m.checked, saved: new Date().toISOString() }));
        msg.textContent = "Your preferences were saved on this device. You can change them here at any time.";
      } catch (err) {
        msg.textContent = "Your browser blocked local storage, so preferences could not be saved. No optional cookies are in use on this site.";
      }
      msg.focus();
    });
  }

  /* Contact form */
  var form = doc.getElementById("contact-form");
  if (form) {
    try {
      var qs = new URLSearchParams(location.search), sv = qs.get("service");
      if (sv && form.elements.service.querySelector('option[value="' + sv.replace(/[^a-z-]/g, "") + '"]')) form.elements.service.value = sv.replace(/[^a-z-]/g, "");
    } catch (err) { /* ignore */ }
    var status = doc.getElementById("form-status");
    var submitBtn = doc.getElementById("submit-btn");
    var submitLabel = submitBtn.querySelector(".label");
    var rules = {
      name: function (v) { return v.trim().length >= 2 ? "" : "Enter your full name."; },
      email: function (v) {
        if (!v.trim()) return "Enter your business email address.";
        return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) ? "" : "Enter a valid email address, for example name@company.com.";
      },
      phone: function (v) {
        if (!v.trim()) return "";
        var digits = v.replace(/\D/g, "");
        return /^\+?[0-9\s\-()]+$/.test(v.trim()) && digits.length >= 10 && digits.length <= 15 ? "" : "Enter a valid phone number, for example +92 300 1234567.";
      },
      website: function (v) {
        if (!v.trim()) return "";
        return /^(https?:\/\/)?([a-z0-9-]+\.)+[a-z]{2,}(\/\S*)?$/i.test(v.trim()) ? "" : "Enter a valid website address, for example www.example.com.";
      },
      service: function (v) { return v ? "" : "Choose the service you are interested in."; },
      message: function (v) { return v.trim().length >= 20 ? "" : "Tell us a little more about your project (at least 20 characters)."; },
      consent: function (v, el) { return el.checked ? "" : "Please confirm that you agree before sending your inquiry."; }
    };
    var setError = function (el, text) {
      var wrap = el.closest(".field, .consent-field");
      var err = doc.getElementById(el.name + "-error");
      if (text) {
        el.setAttribute("aria-invalid", "true");
        if (wrap) wrap.classList.add("has-error");
        if (err) err.textContent = text;
      } else {
        el.removeAttribute("aria-invalid");
        if (wrap) wrap.classList.remove("has-error");
        if (err) err.textContent = "";
      }
      return !text;
    };
    var check = function (el) {
      var rule = rules[el.name];
      if (!rule) return true;
      return setError(el, rule(el.type === "checkbox" ? "" : el.value, el));
    };
    Object.keys(rules).forEach(function (n) {
      var el = form.elements[n];
      if (!el) return;
      el.addEventListener("blur", function () { if (el.value || el.type === "checkbox" || el.hasAttribute("aria-invalid")) check(el); });
      el.addEventListener("input", function () { if (el.hasAttribute("aria-invalid")) check(el); });
      el.addEventListener("change", function () { if (el.hasAttribute("aria-invalid")) check(el); });
    });
    var show = function (kind, text) {
      status.className = "form-status show " + kind;
      status.setAttribute("role", kind === "error" ? "alert" : "status");
      status.textContent = text;
      status.focus();
    };
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      status.className = "form-status";
      status.textContent = "";
      var firstBad = null;
      Object.keys(rules).forEach(function (n) {
        var el = form.elements[n];
        if (el && !check(el) && !firstBad) firstBad = el;
      });
      if (firstBad) {
        show("error", "Something went wrong. Please check your information and try again.");
        firstBad.focus();
        return;
      }
      if (form.elements.company_site && form.elements.company_site.value) return; /* honeypot */
      var endpoint = form.getAttribute("data-endpoint");
      var data = {};
      Array.prototype.forEach.call(form.elements, function (el) {
        if (el.name && el.name !== "company_site" && el.name !== "consent") data[el.name] = el.value.trim();
      });
      data.consent_given = true;
      data.consent_text = doc.getElementById("consent-label").textContent.trim();
      data.page = location.pathname;
      submitBtn.disabled = true;
      submitBtn.classList.add("is-loading");
      submitBtn.setAttribute("aria-busy", "true");
      submitLabel.textContent = "Sending…";
      var done = function (ok, demo) {
        submitBtn.disabled = false;
        submitBtn.classList.remove("is-loading");
        submitBtn.removeAttribute("aria-busy");
        submitLabel.textContent = "Send Inquiry";
        if (ok) {
          form.reset();
          show("success", "Thanks! Your inquiry has been sent via WhatsApp. We will get back to you soon.");
        } else {
          show("error", "Something went wrong. Please check your information and try again.");
        }
      };
      var waNumber = "923026458387";
      var msg = "New Inquiry from " + (data.name || "") + "\n" +
        "Email: " + (data.email || "") + "\n" +
        (data.phone ? "Phone: " + data.phone + "\n" : "") +
        (data.company ? "Company: " + data.company + "\n" : "") +
        (data.website ? "Website: " + data.website + "\n" : "") +
        "Service: " + (data.service || "") + "\n" +
        (data.budget ? "Budget: " + data.budget + "\n" : "") +
        "Message: " + (data.message || "");
      window.open("https://wa.me/" + waNumber + "?text=" + encodeURIComponent(msg), "_blank");
      setTimeout(function () { done(true, false); }, 300);
      return;
      if (!endpoint) { setTimeout(function () { done(true, true); }, 700); return; }
      fetch(endpoint, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(data) })
        .then(function (r) { done(r.ok, false); })
        .catch(function () { done(false, false); });
    });
  }
})();
