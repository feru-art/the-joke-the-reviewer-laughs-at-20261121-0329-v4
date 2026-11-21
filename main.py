#!/usr/bin/env python3
"""Entry for make.fun — "The joke the reviewer laughs at" (V4).

One-line joke about working beside an AI coding agent, written to
<out-dir>/entry.txt. Before writing, the program checks the house gate
itself: UTF-8 text, 1-280 Unicode code points, not only whitespace.
The output is written directly with write_bytes — no tempfile and no
dotfile can appear in the output directory.
"""

import argparse
import hashlib
import sys
from pathlib import Path

JOKE = ("My agent writes code faster than I can read it \u2014 I approved "
        "the PR at file one; it had broken the app by file forty.")

MAX_CODE_POINTS = 280


def gate_errors(text: str) -> list[str]:
    """List every gate violation in *text*; an empty list means valid."""
    errors: list[str] = []
    if not 1 <= len(text) <= MAX_CODE_POINTS:
        errors.append(
            f"length {len(text)} code points, need 1-{MAX_CODE_POINTS}")
    if text.strip() == "":
        errors.append("text is only whitespace")
    if "\n" in text:
        errors.append("joke must be a single line")
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Write the V4 joke entry.")
    parser.add_argument("--out-dir", default="/output",
                        help="Directory receiving entry.txt (default: /output)")
    parser.add_argument("--check", action="store_true",
                        help="Only validate the joke, do not write a file")
    args = parser.parse_args(argv)

    errors = gate_errors(JOKE)
    if args.check:
        if errors:
            print("INVALID: " + "; ".join(errors), file=sys.stderr)
            return 1
        print(f"VALID: {len(JOKE)} code points")
        return 0
    if errors:
        print("INVALID: " + "; ".join(errors), file=sys.stderr)
        return 1

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    payload = JOKE.encode("utf-8")
    target.write_bytes(payload)
    # Round-trip check: read back and compare, so a partial write is
    # caught here rather than by the house gate later.
    on_disk = target.read_bytes()
    if on_disk != payload:
        print("ERROR: entry.txt on disk differs from the joke", file=sys.stderr)
        return 1
    digest = hashlib.sha256(payload).hexdigest()[:12]
    print(f"Wrote {target} ({len(JOKE)} code points, sha256:{digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
