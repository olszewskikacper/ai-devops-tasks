# Zadanie 13: Generowanie komentarzy dokumentacyjnych

**Użyty asystent:** Claude (Claude Code)

## Prompt

```
Dodaj do tej funkcji komentarze dokumentacyjne w formacie JSDoc.
```

## Pliki

- `fetch-user.js`: oryginalna funkcja `fetchUserData` bez komentarzy.
- `fetch-user-documented.js`: ta sama funkcja z komentarzami JSDoc. Kod funkcji pozostał bez zmian.

## Dodana dokumentacja JSDoc

```javascript
/**
 * @typedef {Object} UserData
 * @property {string} name - Imię i nazwisko użytkownika.
 * @property {string} email - Adres e-mail użytkownika.
 * @property {Date} lastLogin - Data i czas ostatniego logowania.
 */

/**
 * Pobiera dane użytkownika z API na podstawie jego identyfikatora.
 *
 * Wysyła żądanie GET na adres `https://api.example.com/users/{userId}`.
 * Błędy HTTP i błędy sieciowe są przechwytywane, logowane w konsoli,
 * a funkcja zwraca wtedy `null` zamiast zgłaszać wyjątek.
 *
 * @param {(string|number)} userId - Identyfikator użytkownika do pobrania.
 * @returns {Promise<UserData|null>} Obietnica z obiektem danych użytkownika
 *   lub `null`, jeśli żądanie się nie powiodło (status inny niż 2xx
 *   albo błąd sieci/parsowania JSON).
 *
 * @example
 * fetchUserData(42).then(user => {
 *   if (user) console.log(user.name, user.lastLogin);
 * });
 */
```

## Krótki opis użytych tagów JSDoc

| Tag | Znaczenie |
|---|---|
| `/** ... */` | Blok komentarza dokumentacyjnego (z dwiema gwiazdkami, w odróżnieniu od zwykłego `/* */`). |
| `@typedef` + `@property` | Definicja własnego typu, tu struktury zwracanego obiektu `UserData`. |
| `@param {typ} nazwa - opis` | Opis parametru funkcji i jego typu. `(string\|number)` oznacza typ złożony. |
| `@returns {typ} opis` | Opis zwracanej wartości. `Promise<UserData\|null>` oznacza obietnicę z wynikiem lub `null`. |
| `@example` | Przykład użycia funkcji. |

## Korzyści

- Edytory (np. VS Code) pokazują opis i typy przy podpowiadaniu kodu.
- Z komentarzy można wygenerować dokumentację HTML narzędziem `jsdoc`.
- Dokumentacja opisuje także zachowanie przy błędzie (zwraca `null`, nie rzuca wyjątku), które nie jest oczywiste z samej sygnatury.

## Weryfikacja

Składnię obu plików sprawdziłem poleceniem `node --check`. Nie uruchamiałem funkcji, bo `api.example.com` to adres przykładowy.
