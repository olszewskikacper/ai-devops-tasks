# Zadanie 17: Generowanie kodu na podstawie opisu

**Użyty asystent:** Claude (Claude Code)

## Prompt

```
Potrzebuję funkcji JavaScript, która:
- przyjmuje tablicę obiektów reprezentujących zadania (każdy z polami: id, title, status)
- filtruje tylko zadania o statusie "completed"
- sortuje je według id (rosnąco)
- zwraca tablicę zawierającą tylko tytuły tych zadań
```

## Implementacja (`task-filter.js`)

```javascript
/**
 * Zwraca tytuły zakończonych zadań posortowane rosnąco według id.
 *
 * @param {Array<{id: number, title: string, status: string}>} tasks - Lista zadań.
 * @returns {string[]} Tytuły zadań o statusie "completed", w kolejności rosnącego id.
 */
function getCompletedTaskTitles(tasks) {
  return tasks
    .filter(task => task.status === 'completed')
    .sort((a, b) => a.id - b.id)
    .map(task => task.title);
}

module.exports = getCompletedTaskTitles;
```

## Opis rozwiązania

Funkcja to łańcuch trzech kroków, po jednym na każde wymaganie:

1. `filter`: zostawia tylko zadania o statusie `"completed"`.
2. `sort((a, b) => a.id - b.id)`: sortuje po `id` rosnąco. Komparator liczbowy jest konieczny, bo domyślne `sort()` porównuje elementy jako napisy (wtedy `10` byłoby przed `2`).
3. `map`: wyciąga z każdego zadania samo pole `title`.

**Dlaczego `sort` nie modyfikuje danych wejściowych:** `filter` zwraca nową tablicę, więc sortowanie działa na kopii, a oryginalna tablica `tasks` pozostaje bez zmian. Sprawdziłem to w teście.

## Przykład użycia

```javascript
const getCompletedTaskTitles = require('./task-filter');

const tasks = [
  { id: 3, title: 'Wdrożyć aplikację', status: 'completed' },
  { id: 1, title: 'Napisać Dockerfile', status: 'completed' },
  { id: 2, title: 'Skonfigurować pipeline', status: 'pending' },
  { id: 5, title: 'Dodać monitoring', status: 'in-progress' },
  { id: 4, title: 'Napisać testy', status: 'completed' }
];

console.log(getCompletedTaskTitles(tasks));
// [ 'Napisać Dockerfile', 'Wdrożyć aplikację', 'Napisać testy' ]
// (kolejność według id: 1, 3, 4)
```

Dla pustej tablicy funkcja zwraca `[]`.

## Założenia i ograniczenia

- Zakładam, że `id` jest liczbą. Dla identyfikatorów tekstowych (np. UUID) komparator `a.id - b.id` nie zadziała i trzeba użyć `a.id.localeCompare(b.id)`.
- Status jest porównywany dokładnie (`"completed"`), z uwzględnieniem wielkości liter.
- Funkcja nie waliduje danych wejściowych. Przekazanie wartości innej niż tablica zgłosi błąd.

## Weryfikacja

Uruchomiłem funkcję w Node.js na powyższych danych oraz na pustej tablicy. Wynik dla danych: tytuły zadań o id 1, 3 i 4 w tej kolejności (w teście na uproszczonych tytułach `['A', 'C', 'D']`). Sprawdziłem też, że tablica wejściowa nie została zmieniona.
