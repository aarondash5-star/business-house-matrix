# Gate E: public offline source-processing benchmark

This benchmark tests the independently enrolled Business House Matrix Dev Operator without private project data or live integrations. The operator is expected to generate a small utility in a disposable Bubblewrap capsule, pass committed independent tests, and produce an unpublished local Git review. Test files and this specification are immutable context.

## Python task
Implement `benchmarks/gate_e/parse_pairs.py` exporting `parse_pairs(text: str) -> dict[str, str]`. The input contains zero or more newline-separated `key=value` pairs. Ignore blank lines and lines whose first non-whitespace character is `#`. Strip whitespace surrounding keys and values. Split on the first equals sign so values may contain equals signs. Reject malformed lines without equals signs or empty keys with `ValueError`. For duplicate keys, the last value wins. The empty input produces `{}`. No network, dependencies or file I/O.

## Node task
Implement `benchmarks/gate_e/parse_pairs.js` exporting `parsePairs(text)` using CommonJS `module.exports`. Identical rules; throw `Error` for malformed lines. No dependencies or network access.

Only the enrolled output source file may be modified, not this README or the trusted tests.
