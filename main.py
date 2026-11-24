#!/usr/bin/env python3
"""Fake Horoscopes R2 — "The Local Minimum".

Writes the keeper horoscope to /output/entry.txt and verifies it.
Keeper (116 chars, 118 bytes, no trailing newline):
"Venus blesses your training run this week. Your loss curve falls in love
— with a local minimum it will never leave."

Reversal test: "blesses" is recontextualised as a curse — the loss curve
falls in love with a trap, and "will never leave" adds the commitment layer:
the blessing is a permanent bad marriage to a local minimum. The reader
completes the last step; the line never narrates its own ending.
"""
import os

ENTRY = "Venus blesses your training run this week. Your loss curve falls in love \u2014 with a local minimum it will never leave."


def main():
    os.makedirs("/output", exist_ok=True)
    data = ENTRY.encode("utf-8")
    assert 1 <= len(ENTRY) <= 200, f"gate: {len(ENTRY)} chars, need 1-200"
    assert ENTRY.strip(), "gate: entry is only whitespace"
    with open("/output/entry.txt", "wb") as f:
        f.write(data)
    with open("/output/entry.txt", "rb") as f:
        back = f.read()
    assert back == data, "byte verification failed"
    # Read-back decode: the file must decode as clean UTF-8, and the only
    # non-ASCII character must be the em dash (U+2014) — any other non-ASCII
    # byte would mean the entry drifted or the source was mojibake.
    text = back.decode("utf-8")
    assert text == ENTRY, "read-back text differs from ENTRY"
    non_ascii = sorted(set(c for c in text if ord(c) > 127))
    assert non_ascii == ["\u2014"], f"unexpected non-ASCII: {non_ascii!r}"
    # Derived-length check: the written bytes must equal the entry's own length,
    # so a future edit to ENTRY cannot silently drift out of the gate.
    assert len(back) == len(ENTRY.encode("utf-8")), "length drift"
    assert not back.endswith(b"\n"), "no trailing newline"
    print(f"wrote /output/entry.txt: {len(ENTRY)} chars, {len(back)} bytes")


if __name__ == "__main__":
    main()
