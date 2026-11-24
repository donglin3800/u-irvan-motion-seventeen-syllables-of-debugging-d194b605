#!/usr/bin/env python3
"""One haiku about debugging, in the 5-7-5 shape.

The poem is fixed text: a breakpoint holds its breath while the log
swears nothing changed, and the last line turns on the culprit -- a
single comma that had moved. The program checks its own syllable
counts against a small word table, then writes the three lines to
entry.txt under the output directory the grader provides. No clock,
no network, no randomness, so every run writes the same bytes.
"""

import os
import sys

HAIKU_LINES = (
    "Breakpoint holds its breath",
    "the log insists nothing changed",
    "a comma had moved",
)

SHAPE = (5, 7, 5)
CHAR_LIMIT = 200

WORD_SYLLABLES = {
    "a": 1,
    "breath": 1,
    "breakpoint": 2,
    "changed": 1,
    "comma": 2,
    "had": 1,
    "holds": 1,
    "insists": 2,
    "its": 1,
    "log": 1,
    "moved": 1,
    "nothing": 2,
    "the": 1,
}


def count_syllables(line):
    total = 0
    for word in line.split():
        beats = WORD_SYLLABLES.get(word.lower())
        if beats is None:
            raise ValueError("no syllable count for word: " + word)
        total += beats
    return total


def build_text():
    if len(HAIKU_LINES) != 3:
        raise ValueError("a haiku has exactly three lines")
    for line, wanted in zip(HAIKU_LINES, SHAPE):
        if not line.strip():
            raise ValueError("a haiku line must not be blank")
        got = count_syllables(line)
        if got != wanted:
            raise ValueError(
                "line %r has %d syllables, want %d" % (line, got, wanted)
            )
    text = "\n".join(HAIKU_LINES) + "\n"
    if not 1 <= len(text) <= CHAR_LIMIT:
        raise ValueError("haiku is %d chars, limit is %d" % (len(text), CHAR_LIMIT))
    return text


def main():
    try:
        text = build_text()
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
