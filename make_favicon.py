import struct, zlib, os

w, h = 32, 32
bg = (0x14, 0x20, 0x1E)
wh = (0xFF, 0xFF, 0xFF)

pixels = []
for y in range(h):
    row = []
    for x in range(w):
        lit = False
        if 2<=x<=4 and 8<=y<=24: lit=True
        if 11<=x<=13 and 8<=y<=24: lit=True
        if 5<=x<=10 and 8<=y<=10: lit=True
        if 5<=x<=10 and 15<=y<=17: lit=True
        if 16<=x<=18 and 8<=y<=24: lit=True
        if 27<=x<=29 and 8<=y<=24: lit=True
        if x==19 and 9<=y<=13: lit=True
        if x==20 and 10<=y<=14: lit=True
        if x==21 and 11<=y<=15: lit=True
        if x==22 and 12<=y<=16: lit=True
        if x==23 and 11<=y<=15: lit=True
        if x==24 and 10<=y<=14: lit=True
        if x==25 and 9<=y<=13: lit=True
        if x==26 and 8<=y<=12: lit=True
        row.append(wh if lit else bg)
    pixels.append(row)

def chunk(tag, data):
    c = zlib.crc32(tag + data) & 0xFFFFFFFF
    return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', c)

raw = b''
for row in pixels:
    raw += b'\x00'
    for r, g, b in row:
        raw += bytes([r, g, b])

png = b'\x89PNG\r\n\x1a\n'
png += chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
png += chunk(b'IDAT', zlib.compress(raw, 9))
png += chunk(b'IEND', b'')

ico = struct.pack('<HHH', 0, 1, 1)
ico += struct.pack('<BBBBHHII', w, h, 0, 0, 1, 24, len(png), 22)
ico += png

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'favicon.ico')
with open(out, 'wb') as f:
    f.write(ico)
print(f"Written {len(ico)} bytes to {out}")
