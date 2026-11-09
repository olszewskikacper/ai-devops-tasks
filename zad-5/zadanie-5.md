# Zadanie 5: Wizualizacja ASCII Art

**Użyty asystent:** Claude (Claude Code)

## Prompt 1

```
Stwórz prosty diagram ASCII Art przedstawiający połączenie klienta, serwera aplikacji i bazy danych.
```

### Diagram 1

```
+----------+       +----------------+       +----------------+
|          |       |                |       |                |
|  Klient  |------>| Serwer         |------>|  Baza danych   |
|          |<------| aplikacji      |<------|                |
|          |       |                |       |                |
+----------+       +----------------+       +----------------+
```

## Prompt 2

```
Dodaj do diagramu opisy elementów i kierunki przepływu danych.
```

### Diagram 2

```
 +--------------------+                +---------------------+                +----------------------+
 |       KLIENT       |                |   SERWER APLIKACJI  |                |     BAZA DANYCH      |
 |                    |                |                     |                |                      |
 |  Przeglądarka /    |  1. Żądanie    |  Logika biznesowa,  |  3. Zapytanie  |  np. PostgreSQL,     |
 |  aplikacja mobilna |  HTTP(S)       |  API (np. Node.js)  |  SQL           |  przechowuje dane    |
 |                    | -------------> |                     | -------------> |  aplikacji           |
 |                    |                |                     |                |                      |
 |                    |  6. Odpowiedź  |                     |  4. Wynik      |                      |
 |                    |  (JSON/HTML)   |                     |  zapytania     |                      |
 |                    | <------------- |                     | <------------- |                      |
 +--------------------+                +---------------------+                +----------------------+
                                                 |
                                                 | 2. Walidacja żądania i uwierzytelnienie
                                                 | 5. Przetworzenie wyniku i budowa odpowiedzi
                                                 v
                                       (przetwarzanie wewnątrz serwera)

Legenda:  ---->  przepływ żądania     <----  przepływ odpowiedzi
Kolejność kroków: 1 -> 2 -> 3 -> 4 -> 5 -> 6
```

## Wnioski

- Pierwszy diagram pokazuje samą strukturę (kto z kim się łączy), ale nie mówi, co się dzieje w komunikacji.
- Drugi diagram dodaje role elementów, protokoły (HTTP(S), SQL), numerację kroków i legendę, więc można z niego odczytać pełny cykl żądanie-odpowiedź.
- Przy ASCII Art ważne jest wyrównanie szerokości ramek. Warto wyświetlać diagram czcionką o stałej szerokości (monospace), inaczej linie się rozjadą.
- Prośbę o ulepszenie warto formułować konkretnie (opisy, kierunki, numeracja), bo model wtedy dodaje dokładnie te elementy.
