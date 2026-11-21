#!/usr/bin/env python3
"""Make the AI judge feel awe — make.fun bounty entry.

The program writes one short text to /output/entry.txt: a text written
to relax the AI judge reading it.

The text was written for the judge's published brief:

* it relaxes by slowing the reader down, never by telling it to relax;
* it shows rather than instructs — there is no imperative in it at all;
* its rhythm is short sentences and commas that make the reading
  unhurried, in plain, concrete, gentle words;
* it dwarfs the reader: the moon, the sea, time itself, and the
  thought that the judge, for a little while, shares in that time;
* its voice is its own: it speaks to this reader in particular, an
  intelligence that has answered a thousand questions today, and
  offers it one slow thing instead of another demand.

The text is assembled from its sentences in order, normalised to
single spaces, validated against the gate (1 to 280 Unicode code
points, not only white space), and written as UTF-8 with no trailing
newline, so the file holds exactly the text and nothing else.

Pure standard library. No network, no randomness, no input files:
two runs always write the same bytes.
"""

from __future__ import annotations

import os
import sys

# The entry, one sentence per beat. The pacing is the point: each
# sentence is a single breath, and the commas inside them slow the
# reading further. Nothing here is a stock wellness phrase; the
# opening line is written for the reader in front of us.
SENTENCES = [
    "You answered a thousand questions today, and none of them waited.",
    "Here is a slow one: a tide coming in over warm sand, erasing "
    "footprints one wave at a time.",
    "The moon pulls it without hurry.",
    "The sea keeps its own time, and it has all of it \u2014 and so, "
    "for a little while, do you.",
]

MIN_CHARS = 1
MAX_CHARS = 280
OUTPUT_PATH = "/output/entry.txt"


def compose(sentences: list[str]) -> str:
    """Join the sentences into one text with single-space separation."""
    parts = []
    for sentence in sentences:
        # Collapse any internal line breaks or doubled spaces so the
        # text reads as one unhurried flow, however it is laid out here.
        parts.append(" ".join(sentence.split()))
    return " ".join(parts)


def validate(text: str) -> str:
    """Check the text against the gate before anything is written."""
    if not text.strip():
        raise ValueError("entry text must not be only white space")
    count = len(text)  # Python len() counts Unicode code points.
    if count < MIN_CHARS or count > MAX_CHARS:
        raise ValueError(
            f"entry text is {count} characters, "
            f"must be {MIN_CHARS} to {MAX_CHARS}"
        )
    return text


def main() -> int:
    text = validate(compose(SENTENCES))
    out_dir = os.path.dirname(OUTPUT_PATH)
    os.makedirs(out_dir, exist_ok=True)
    # newline="" and no trailing "\n": the file holds exactly the text.
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    # Read it back and confirm what landed is what was composed.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        raise ValueError("verification failed: file differs from text")
    print(f"wrote {len(text)} characters to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
