const sum = require('./sum');

test('dodaje 1 + 2 i zwraca 3', () => {
  expect(sum(1, 2)).toBe(3);
});

test('dodaje liczby ujemne', () => {
  expect(sum(-1, -2)).toBe(-3);
});

test('dodaje zero', () => {
  expect(sum(5, 0)).toBe(5);
});
