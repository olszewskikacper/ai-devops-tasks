# Zadanie 15: Refaktoryzacja prostej funkcji

**Użyty asystent:** Claude (Claude Code)

## Prompt

```
Zrefaktoryzuj tę funkcję, aby była bardziej czytelna i łatwiejsza w utrzymaniu.
```

## Pliki

- `config.js`: oryginalna funkcja z łańcuchem `if-else`.
- `config-refactored.js`: wersja zrefaktoryzowana.

## Zrefaktoryzowana wersja

```javascript
const CONFIGS = {
  development: {
    apiUrl: 'http://localhost:3000/api',
    debug: true,
    timeout: 5000
  },
  testing: {
    apiUrl: 'http://test-server:3000/api',
    debug: true,
    timeout: 5000
  },
  staging: {
    apiUrl: 'https://staging.example.com/api',
    debug: false,
    timeout: 10000
  },
  production: {
    apiUrl: 'https://api.example.com',
    debug: false,
    timeout: 15000
  }
};

const DEFAULT_ENV = 'development';

function getEnvironmentConfig(env) {
  const config = Object.hasOwn(CONFIGS, env) ? CONFIGS[env] : CONFIGS[DEFAULT_ENV];
  return { ...config };
}

module.exports = getEnvironmentConfig;
```

## Opis zmian

1. **Dane oddzielone od logiki.** Konfiguracje środowisk trafiły do obiektu-słownika `CONFIGS`, a funkcja ma teraz dwie linie.
2. **Brak `if-else`.** Wybór konfiguracji to wyszukanie klucza w obiekcie zamiast sprawdzania kolejnych warunków.
3. **Nazwana wartość domyślna.** Środowisko domyślne zapisano w stałej `DEFAULT_ENV`, więc jest jawne, a nie ukryte w gałęzi `else`. Dotąd domyślna konfiguracja była zduplikowana kodem identycznym z `development`.
4. **Zwracana kopia** (`{ ...config }`). Wywołujący może zmodyfikować wynik, nie psując współdzielonej konfiguracji.
5. **`Object.hasOwn`** zamiast zwykłego `CONFIGS[env]`. Dzięki temu wejścia typu `'toString'` lub `'__proto__'` nie trafią do odziedziczonych właściwości obiektu i dostaną konfigurację domyślną, tak jak w oryginale.

## Korzyści

- **Czytelność:** wszystkie środowiska widać w jednym miejscu, w tabelarycznej postaci.
- **Łatwość rozbudowy:** nowe środowisko to jeden wpis w `CONFIGS`, bez dotykania logiki.
- **Mniej powtórzeń:** znikło powielanie `return { apiUrl, debug, timeout }`, a więc i ryzyko literówek.
- **Łatwiejsze testowanie:** dane można testować i walidować osobno.

## Weryfikacja

Uruchomiłem obie funkcje w Node.js i porównałem wyniki (`assert.deepStrictEqual`) dla wejść: `development`, `testing`, `staging`, `production`, nieznana wartość, `undefined`, `null`, pusty napis, `'toString'` i `'__proto__'`. Wszystkie wyniki były identyczne z oryginałem, więc refaktoryzacja nie zmienia zachowania.

**Uwaga:** `Object.hasOwn` wymaga Node.js 16.9 lub nowszego.
