# Zadanie 22: Generowanie README dla projektu

**Użyty asystent:** Claude (Claude Code)

## Prompt

```
Nazwa projektu: Simple Task API
Opis: REST API do zarządzania zadaniami, napisane w Node.js z Express i MongoDB.
Główne funkcje:
- Tworzenie, odczytywanie, aktualizacja i usuwanie zadań
- Filtrowanie zadań według statusu i priorytetów
- Prostą autoryzację użytkowników

Stwórz prosty plik README.md dla tego projektu, zawierający sekcje: opis, instalacja, użycie, endpointy API.
```

Wygenerowany plik znajduje się w [`project-readme.md`](project-readme.md).

## Uwagi dotyczące jakości wygenerowanej dokumentacji

### Mocne strony

- **Wszystkie wymagane sekcje:** opis, instalacja, użycie i endpointy API, plus wymagania, model danych i kody odpowiedzi.
- **Gotowe do użycia przykłady:** komendy `git clone`, `npm install`, plik `.env` oraz zapytania `curl` można skopiować i uruchomić.
- **Czytelna struktura:** tabele endpointów i parametrów filtrowania ułatwiają szybkie przeglądanie.
- **Odzwierciedlone wymagania:** każda z trzech funkcji z opisu ma swoje miejsce w dokumencie.

### Słabe strony i ryzyka

- **Wiele wymyślonych szczegółów.** Prompt nie podał ścieżek endpointów, pól zadania, nazw wartości statusów i priorytetów, metody autoryzacji ani nazw skryptów npm. Przyjąłem `/api/tasks`, `/api/auth/login`, JWT, statusy `pending`/`in-progress`/`completed`, priorytety `low`/`medium`/`high` oraz skrypty `npm start` i `npm run dev`. To **założenia**, a nie fakty o projekcie.
- **Adres repozytorium to placeholder** (`<twoj-uzytkownik>`) i trzeba go podmienić.
- **Wzmianka o pliku `.env.example` i licencji MIT** to konwencje, a nie informacje z promptu. Takiego pliku i licencji nie ma w projekcie, bo projekt nie istnieje.
- **Brak sekcji, które w prawdziwym README byłyby przydatne:** uruchamianie w Dockerze, testy, struktura katalogów, sposób wnoszenia zmian.
- **Przykładowe dane i hasła** (`haslo123`) to tylko ilustracja.

### Wnioski

1. README wygenerowane **przed napisaniem kodu** jest szkicem. Po powstaniu aplikacji trzeba je zweryfikować z rzeczywistymi endpointami i konfiguracją, bo model nie ma jak sprawdzić, co jest w kodzie.
2. Im konkretniejszy prompt, tym mniej zgadywania. Warto podać listę endpointów, model danych i wybraną metodę autoryzacji.
3. Dobrze mieć w README jawne miejsca do uzupełnienia (jak placeholder repozytorium), zamiast udawać pewność.
4. AI szybko daje dobry **szkielet** i spójny format, a człowiek dopracowuje szczegóły i dba o aktualność.
5. Dokument nie był uruchamiany ani testowany, bo opisywany projekt nie istnieje. Przykłady `curl` są więc nieprzetestowane.
