# Zadanie 12: Optymalizacja prostego skryptu

**Użyty asystent:** Claude (Claude Code)

## Prompt

```
Czy ten kod można zoptymalizować? Jeśli tak, zaproponuj bardziej wydajną wersję.
```

## Oryginalna wersja

```python
def find_duplicates(list_of_items):
    duplicates = []
    for i in range(len(list_of_items)):
        for j in range(i+1, len(list_of_items)):
            if list_of_items[i] == list_of_items[j] and list_of_items[i] not in duplicates:
                duplicates.append(list_of_items[i])
    return duplicates
```

## Odpowiedź: tak, kod można zoptymalizować

Problemy w oryginale:
1. **Podwójna pętla** daje złożoność czasową **O(n²)**. Każdy element jest porównywany z każdym kolejnym.
2. **`not in duplicates`** to wyszukiwanie liniowe na liście, co dokłada kolejny czynnik w pesymistycznym przypadku.

## Zoptymalizowana wersja

```python
from collections import Counter

def find_duplicates(list_of_items):
    counts = Counter(list_of_items)
    return [item for item in counts if counts[item] > 1]
```

## Wyjaśnienie usprawnień

- `Counter` zlicza wystąpienia w **jednym przejściu** po liście (O(n)), korzystając z tablicy mieszającej.
- Filtrowanie wyników to kolejne O(n), więc całość ma złożoność **O(n)** zamiast O(n²).
- Wynik jest ten sam co w oryginale: elementy występujące więcej niż raz, każdy po jednym razie, **w kolejności pierwszego wystąpienia** (słownik w Pythonie 3.7+ zachowuje kolejność wstawiania).
- Kod jest krótszy i czytelniejszy.
- Ograniczenie: elementy muszą być hashowalne (np. liczby, napisy, krotki). Oryginał działał też dla list zagnieżdżonych, bo używał tylko `==`.

## Weryfikacja

- **Poprawność:** przetestowałem obie funkcje na 300 losowych listach i na dużej liście. Wyniki były identyczne, łącznie z kolejnością.
- **Wydajność:** dla 5000 elementów oryginał zajął ok. **0,40 s**, a wersja zoptymalizowana ok. **0,0003 s**. Przy większych danych różnica rośnie, bo jedna wersja skaluje się kwadratowo, a druga liniowo.

**Uwaga z procesu:** pierwsza wersja, którą napisałem (oparta na zbiorze `set`), zwracała elementy w innej kolejności niż oryginał (`[2, 1]` zamiast `[1, 2]`). Wykrył to test porównawczy i poprawiłem implementację na powyższą. Gdyby kolejność nie miała znaczenia, wystarczyłby wariant ze zbiorem.
