#!/usr/bin/env python3
"""Enable the Search function on iPod Video 5G (stock firmware)."""
import hashlib, os, struct, sys

HELP = """\
usage: python3 patch.py <Firmware-file>

  <Firmware-file>  the "Firmware-13.x.y" file extracted from the iPod IPSW
                   (the IPSW is a zip: unzip iPod_13.1.3.ipsw)

writes: <Firmware-file>-search.bin  ->  sudo ./ipodpatcher -wfb <Firmware-file>-search.bin

supported firmware: 1.3 (families 13/20), 1.2.1 (family 13)
"""

# sha1 of the stock osos image -> (firmware version, offset of the byte to flip)
KNOWN = {
    "3281abc9f44bb8ddfa4e00da03488308fe624c53": ("1.3",   0x130b50),
    "b0a3c5ed5866563cc5b185d777b8f81ba17c4ab1": ("1.2.1", 0x12e880),
}

if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
    print(HELP); sys.exit(0 if len(sys.argv) == 2 else 1)
path = sys.argv[1]
if not os.path.isfile(path):
    sys.exit(f"error: file not found: {path}\n\n{HELP}")

fw = open(path, "rb").read()
if fw[:2] == b"PK":
    sys.exit("error: this is the IPSW (a zip). Unzip it and pass the Firmware-* file.")
if fw[0x4200:0x4204] != b"!ATA":
    sys.exit("error: not an iPod firmware image (no directory at 0x4200)")

devoff, length = struct.unpack_from("<II", fw, 0x4200 + 12)   # first directory entry = osos
osos = bytearray(fw[0x200 + devoff:0x200 + devoff + length])  # image starts one sector after devOffset

sha = hashlib.sha1(osos).hexdigest()
if sha not in KNOWN:
    sys.exit(f"error: unknown firmware (osos sha1 {sha}); nothing written")
version, off = KNOWN[sha]
if osos[off] != 0:
    sys.exit("error: unexpected byte at patch offset; nothing written")

osos[off] = 1                                   # the revision check now always passes
out = os.path.basename(path) + "-search.bin"
open(out, "wb").write(osos)
print(f"firmware {version}: byte 0x{off:x} patched, wrote {out}")
