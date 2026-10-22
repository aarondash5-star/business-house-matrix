# Gate E independent RC1 autonomous capability challenges

Public non-sensitive benchmarks. The **trusted tests must be committed and
SHA-pinned before model invocation**. The model is allowed to write only its
explicitly enrolled source paths. No credentials, private data, network,
dependency installation, or Git push.

## Node challenge: normalizeTag

Generate ONLY `benchmarks/gate_e/normalize_tag.js`.
Export `normalizeTag` using CommonJS `module.exports = {normalizeTag}`.
Accept a string, trim surrounding whitespace, lower-case ASCII letters,
replace each contiguous run of non-alphanumeric characters with a single
hyphen, and remove leading or trailing hyphens. Return an empty string if
input is not a string or contains no ASCII letters or digits.
Independent owner-authored tests: `tests/gate_e_normalize_tag.test.js`.

## Python two-file challenge: receipt total

Generate BOTH `benchmarks/gate_e/money.py` and
`benchmarks/gate_e/invoice.py`.
`money.parse_cents(text)` receives a str in the strict format
`12`, `12.3`, `12.34` or optionally prefixed by `$`; returns
integer cents, e.g. `$12.30` -> `1230`, `0` -> `0`.
Reject negative signs, whitespace, more than two fractional digits,
empty strings, non-string values or any other characters with ValueError.
`invoice.invoice_total(lines)` receives a list of strings, calls
`parse_cents` for each, and returns their sum in integer cents.
Reject non-lists with ValueError; an empty list totals 0.
Independent owner-authored tests: `tests/test_gate_e_invoice_rc1.py`.
The files must have an appropriate import so both work together.

## Evidence requirements

For each unique benchmark, record immutable public base Git SHA, exact
enrollment, model identity, bounded attempts, full negative security tests,
independent QA outputs and local-only review. Do not replay the previous
completed Python parse_pairs pilot. No final Gate E release until these
model runs and external-project source-identity audits are independently
verified.
