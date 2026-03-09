# koloMOGorov

Approximating the Kolmogorov complexity of text using pure Python — no compression libraries allowed.

## The Challenge

Given `enwik9_100kb.txt` (the first 100KB of the enwik9 Wikipedia XML dump), write a Python script `compress.py` that:

1. **When run, outputs the exact contents of `enwik9_100kb.txt`** — byte-for-byte, lossless.
2. **Is significantly smaller than the original file** — target is 50% of 102,400 bytes (51,200 bytes).
3. **Uses no external or standard library compression** — no `zlib`, `gzip`, `bz2`, `lzma`, `base64`, etc. Only pure Python logic that exploits patterns in the data.

This is essentially computing an approximation of the [Kolmogorov complexity](https://en.wikipedia.org/wiki/Kolmogorov_complexity) of the text: the shortest program that produces the output.

## Rules

- `compress.py` must run with just `python3 compress.py` and write the exact original text to stdout
- No imports of compression/encoding libraries — the compression must come from understanding the structure of the data
- The script size is the metric: smaller script = better compression = closer to Kolmogorov complexity

## Approach

Iterative — start naive (>100%), then exploit patterns to shrink:

1. **Dictionary substitution**: Identify frequently repeated strings (XML tags, common words, wiki markup) and replace them with short tokens
2. **Structural templates**: The XML follows a rigid `<page>/<revision>/<contributor>` structure — generate it from compact data
3. **Content modeling**: The article text has patterns (wiki links `[[...]]`, references `<ref>...</ref>`, headings `==...==`) that can be reconstructed
4. **Delta encoding**: Many numeric IDs and timestamps are sequential or close — store deltas

## Files

- `enwik9_100kb.txt` — the target output (102,400 bytes)
- `compress.py` — the self-decompressing script (goal: <51,200 bytes)
- `verify.py` — compares `compress.py` output against the original, shows diffs on mismatch
