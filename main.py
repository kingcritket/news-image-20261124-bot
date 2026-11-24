#!/usr/bin/env python3
"""
main.py -- delivery shipper for the "Tuesday, In Full" entry.

The artwork is finished long before this script runs: entry.png sits
next to me, already rendered and committed. My whole job is to carry
that file into the output folder without altering a single byte, and
to prove -- before and after the move -- that what travels is really
the 1024 x 1024 PNG the page claims to be.

How I check a PNG with nothing but the standard library: the format
opens with a fixed eight-byte signature, and the IHDR chunk that
follows stores the canvas width and height as two big-endian 32-bit
integers at byte offsets 16 and 20. If the signature is wrong, or the
dimensions are anything other than 1024 x 1024, I stop with a nonzero
exit instead of shipping a broken entry.

The destination comes from the MAKEFUN_OUTPUT_DIR environment
variable; when it is unset I fall back to a plain "output" folder in
the current working directory.
"""

import os
import struct
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
EXPECTED = (1024, 1024)


def png_dimensions(raw):
    """Return (width, height) read from the IHDR, or None if not a PNG."""
    if len(raw) < 24 or not raw.startswith(PNG_MAGIC):
        return None
    return struct.unpack(">II", raw[16:24])


def checked_bytes(path):
    """Read a file and return its bytes only if it passes the PNG gate."""
    raw = path.read_bytes()
    dims = png_dimensions(raw)
    if dims is None:
        raise SystemExit(f"refusing to ship: {path} is not a PNG file")
    if dims != EXPECTED:
        raise SystemExit(
            f"refusing to ship: {path} is {dims[0]}x{dims[1]}, "
            f"expected {EXPECTED[0]}x{EXPECTED[1]}"
        )
    return raw


def main():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    payload = checked_bytes(source)

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(payload)

    # Second gate on the delivered copy: same bytes, same dimensions.
    delivered = checked_bytes(target)
    if delivered != payload:
        raise SystemExit("refusing to ship: delivered copy differs")

    print(f"shipped entry.png ({len(payload)} bytes, 1024x1024) -> {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
