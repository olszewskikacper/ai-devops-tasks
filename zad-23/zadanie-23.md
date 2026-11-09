# Zadanie 23: Analiza złożoności algorytmu

**Użyty asystent:** Claude (Claude Code)

## Prompt

```
Jaka jest złożoność czasowa i pamięciowa tego algorytmu? Czy można go zoptymalizować?
```

## Algorytm (`find-pairs.js`)

```javascript
function findPairs(arr, targetSum) {
  const pairs = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] + arr[j] === targetSum) {
        pairs.push([arr[i], arr[j]]);
      }
    }
  }
  return pairs;
}
```

## Analiza złożoności (wersja oryginalna)

**Czasowa: O(n²).** Dwie zagnieżdżone pętle porównują każdą parę elementów dokładnie raz, czyli n·(n−1)/2 porównań. Dla n = 20 000 to około 200 milionów porównań.

**Pamięciowa:**
- Pamięć pomocnicza: **O(1)**, bo poza wynikiem są tylko zmienne `i` i `j`.
- Wynik (`pairs`): w najgorszym przypadku **O(n²)** (np. gdy wszystkie elementy są równe połowie sumy, każda para pasuje).

## Optymalizacja (`find-pairs-optimized.js`)

```javascript
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
```

### Jak to działa

Dla każdego elementu nie szukamy partnera w całej tablicy, tylko pytamy mapę (tablicę mieszającą), ile razy wcześniej pojawiła się wartość `targetSum - current`. Wyszukiwanie w mapie to średnio O(1). Każda wcześniejsza wartość pasująca do dopełnienia daje jedną parę, więc powtórzone liczby dają powtórzone pary, tak jak w oryginale.

### Złożoność wersji zoptymalizowanej

| | Oryginał | Zoptymalizowana |
|---|---|---|
| Czas | O(n²) | **O(n + k)**, gdzie k to liczba zwróconych par |
| Pamięć pomocnicza | O(1) | O(n) na mapę |

To klasyczna zamiana **pamięci na czas**. Gdy par jest mało, czas jest praktycznie liniowy. W skrajnym przypadku (np. `[1,1,1,...]` i suma 2) liczba par k sama wynosi O(n²), więc żaden algorytm nie jest wtedy szybszy od samego wypisania wyniku.

## Różnice w zachowaniu

- Zwracany **zbiór par jest ten sam**, w tym samej orientacji (`[wcześniejszy, późniejszy]`).
- **Kolejność par może być inna.** Oryginał układa pary według pierwszego indeksu `i`, a wersja zoptymalizowana według drugiego (`j`). Przykład: dla `[1,2,3,4,3]` i sumy 6 obie dają `[[2,4],[3,3]]`, ale dla innych danych kolejność może się różnić.
- Dla liczb zmiennoprzecinkowych odejmowanie (`targetSum - current`) może dać inny wynik niż porównanie `a + b === targetSum` z powodu błędów zaokrągleń. Dla liczb całkowitych wyniki są identyczne.

## Weryfikacja

- **Poprawność:** porównałem obie funkcje na 2000 losowych tablic (długość do 30, wartości od −10 do 10, losowa suma), porównując wyniki jako multizbiory par. Wszystkie wyniki były zgodne. Sprawdziłem też przypadki brzegowe: `[1,1,1]` z sumą 2 daje 3 pary w obu wersjach, a pusta tablica i jeden element dają `[]`.
- **Wydajność:** dla tablicy 20 000 liczb (jedno uruchomienie, wartości orientacyjne) oryginał potrzebował ok. 142 ms, a wersja zoptymalizowana ok. 2,4 ms.

## Wnioski

1. Podwójna pętla to sygnał ostrzegawczy: warto zapytać, czy da się użyć struktury danych z szybkim wyszukiwaniem (mapa, zbiór).
2. Optymalizacja kosztuje pamięć i czasem zmienia kolejność wyników, więc warto to zaznaczyć.
3. Przy optymalizacji należy zawsze porównać wyniki z wersją oryginalną na losowych danych.
