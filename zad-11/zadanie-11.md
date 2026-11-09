# Zadanie 11: Generowanie prostego testu jednostkowego

**Użyty asystent:** Claude (Claude Code)

## Prompt

```
Napisz prosty test jednostkowy dla tej funkcji używając Jest. Wyjaśnij, czym jest Jest, jak go zainstalować w projekcie i jak uruchomić ten test. Podaj również strukturę plików projektu.
```

Funkcja:

```javascript
function sum(a, b) {
  return a + b;
}
```

## Czym jest Jest

Jest to framework do testowania kodu JavaScript (utrzymywany przez Meta). Zawiera w jednym pakiecie runner testów, bibliotekę asercji (`expect`), mockowanie oraz raport pokrycia kodu. Nie wymaga skomplikowanej konfiguracji, a pliki `*.test.js` znajduje automatycznie.

## Struktura plików projektu

```
projekt/
├── package.json
├── sum.js
└── sum.test.js
```

## Kod

`sum.js`:

```javascript
function sum(a, b) {
  return a + b;
}

module.exports = sum;
```

`sum.test.js`:

```javascript
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
```

`module.exports = sum;` jest potrzebne, żeby plik testowy mógł zaimportować funkcję.

## Instalacja i uruchomienie

```bash
npm init -y                      # utworzenie package.json (jeśli go nie ma)
npm install --save-dev jest      # instalacja Jesta jako zależności deweloperskiej
```

W `package.json` ustaw skrypt testowy:

```json
"scripts": {
  "test": "jest"
}
```

Uruchomienie testów:

```bash
npm test
# lub bezpośrednio
npx jest
```

## Weryfikacja

Pliki skopiowałem do czystego katalogu tymczasowego, zainstalowałem Jest i uruchomiłem `npx jest`. Wynik: `Test Suites: 1 passed, 1 total`, `Tests: 3 passed, 3 total`.

## Wnioski

- Każdy test to `test('opis', () => { ... })` z asercją `expect(wynik).toBe(oczekiwana_wartosc)`.
- Dobry test sprawdza nie tylko typowy przypadek, ale też wartości graniczne (zero, liczby ujemne).
- Testy jednostkowe stanowią podstawę etapu `test` w pipeline CI/CD.
