/**
 * Zwraca wszystkie pary (i < j) elementów tablicy, których suma wynosi targetSum.
 * Zachowuje się jak wersja z podwójną pętlą (powtórzone wartości dają powtórzone
 * pary), ale pary pojawiają się w innej kolejności.
 *
 * Czas: O(n + k), gdzie k to liczba zwróconych par. Pamięć: O(n) na mapę.
 */
function findPairs(arr, targetSum) {
  const pairs = [];
  const seen = new Map(); // wartość -> ile razy wystąpiła wśród wcześniejszych elementów

  for (const current of arr) {
    const complement = targetSum - current;
    const count = seen.get(complement) || 0;
    for (let k = 0; k < count; k++) {
      pairs.push([complement, current]);
    }
    seen.set(current, (seen.get(current) || 0) + 1);
  }
  return pairs;
}

module.exports = findPairs;
