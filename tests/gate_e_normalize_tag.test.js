const test = require('node:test');
const assert = require('node:assert/strict');
const {normalizeTag} = require('../benchmarks/gate_e/normalize_tag');

test('normalizes ordinary words and punctuation', () => {
  assert.equal(normalizeTag('Hello, WORLD!'), 'hello-world');
  assert.equal(normalizeTag('A__b...c'), 'a-b-c');
});
test('trims leading and trailing punctuation', () => {
  assert.equal(normalizeTag('  ###Goa---WELLNESS!!!  '), 'goa-wellness');
});
test('collapses repeated separators', () => {
  assert.equal(normalizeTag('a / / b --- c'), 'a-b-c');
});
test('keeps ASCII digits', () => {
  assert.equal(normalizeTag('  Room #12!!  '), 'room-12');
});
test('non-string and empty input become empty string', () => {
  assert.equal(normalizeTag(null), '');
  assert.equal(normalizeTag(undefined), '');
  assert.equal(normalizeTag(12), '');
  assert.equal(normalizeTag({}), '');
  assert.equal(normalizeTag('  +++  '), '');
});
test('idempotent normalized input', () => {
  const text='north-goa-2026';
  assert.equal(normalizeTag(text), text);
});
