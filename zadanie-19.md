# Zadanie 19: Generowanie prostej dokumentacji

**Użyty asystent:** Claude (Claude Code)

## Prompt

```
Stwórz dokumentację tego endpointu w formacie Markdown, zawierającą opis, parametry, przykładowe żądanie i odpowiedź.
```

(Opis endpointu: `GET /api/users` z parametrami `page`, `limit` i `role`.)

Wygenerowana dokumentacja znajduje się w pliku [`api-docs.md`](api-docs.md).

## Refleksje na temat jakości wygenerowanej dokumentacji

### Co wyszło dobrze

- **Kompletna struktura:** opis, tabela parametrów (typ, wymagalność, wartość domyślna), przykład żądania (HTTP i `curl`), przykład odpowiedzi, opis pól i kody statusu.
- **Czytelność:** tabele i bloki kodu ułatwiają szybkie znalezienie informacji.
- **Zgodność z opisem wejściowym:** wartości domyślne (`page=1`, `limit=10`) i limit 100 zostały odwzorowane dokładnie.

### Co jest słabością

- **Wymyślone szczegóły.** Opis endpointu nie zawierał struktury odpowiedzi, więc pola użytkownika (`id`, `name`, `email`, `role`) oraz obiekt `pagination` są **moimi założeniami**. Wyglądają wiarygodnie, ale mogą nie pasować do prawdziwego API. Najgroźniejsze w dokumentacji generowanej przez AI jest to, że zmyślone fragmenty wyglądają tak samo pewnie jak prawdziwe.
- **Niejednoznaczna reguła:** "max 100" można zrozumieć jako odrzucenie (`400`) albo przycięcie do 100. Wybrałem pierwszą opcję i oznaczyłem to w dokumencie, ale to decyzja projektowa, nie fakt.
- **Brak informacji, których nie podano:** uwierzytelnianie, limity zapytań (rate limiting), sortowanie, sposób przekazywania `role` dla wielu ról, format błędów.
- **Przykładowe dane są sztuczne** (np. `total: 7` zgadza się z przykładem, ale to tylko ilustracja).

### Wnioski

1. AI dobrze **porządkuje i formatuje** wiedzę, ale **nie zna Twojego systemu**. Wygenerowany dokument trzeba zweryfikować z kodem lub z faktyczną odpowiedzią API (np. `curl`).
2. Dobrą praktyką jest **jawne oznaczanie założeń**. Dodałem je na końcu `api-docs.md`.
3. Jakość wyniku zależy od wejścia. Gdybym dostał przykładową odpowiedź JSON lub kod kontrolera, dokumentacja byłaby dokładniejsza.
4. Najlepszy efekt daje połączenie: AI szkicuje, człowiek weryfikuje, a docelowo specyfikacja (np. OpenAPI) jest generowana z kodu.
