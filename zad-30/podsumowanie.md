# Zadanie 30: Podsumowanie nauki z AI

**Użyty asystent:** Claude (Claude Code)

## Prompt

```
Wykonałem serię 29 zadań związanych z wykorzystaniem AI w praktykach DevOps. Pomóż mi stworzyć podsumowanie, które zawiera:
- Kluczowe wnioski z pracy z AI
- Najmocniejsze i najsłabsze strony AI w kontekście DevOps
- 3-5 konkretnych scenariuszy, w których AI może najbardziej usprawnić moją pracę
- Wskazówki do efektywnego korzystania z AI w przyszłych projektach
```

## 1. Kluczowe wnioski z pracy z AI

1. **Jakość wyniku zależy od jakości polecenia.** W zadaniu 3 niedookreślony prompt ("dockerfile node") zmusił model do zgadywania wersji, portu i punktu wejścia. Prompt z listą wymagań dał gotowy, przewidywalny plik. Rola (zadanie 4) zmieniła strukturę odpowiedzi i poziom szczegółu, ale nie dodała wiedzy.
2. **AI szybko daje dobry szkielet.** Dockerfile, Jenkinsfile, README, dokumentacja API, szablon JCasC i skrypty powstawały w minuty i miały poprawną strukturę.
3. **Wynik trzeba zweryfikować.** W trakcie serii kilka rzeczy wyszło dopiero przy sprawdzeniu, nie przy pisaniu:
   - Zoptymalizowana wersja `find_duplicates` (zadanie 12) zwracała elementy w **innej kolejności** niż oryginał (`[2, 1]` zamiast `[1, 2]`). Wyłapał to test porównawczy na losowych danych.
   - Skrypt PowerShell z polskimi znakami (zadanie 16) **w ogóle się nie parsował** w Windows PowerShell 5.1, bo plik bez BOM był czytany jako ANSI. Naprawiło to zapisanie w UTF-8 z BOM.
   - Skrypt do Jenkinsa (zadanie 28) pokazywał surowy błąd 404 dla zadania bez buildów. Wyszło to dopiero przy teście na atrapie serwera.
4. **AI zmyśla szczegóły, gdy brakuje danych.** W dokumentacji API (zadanie 19) i README (zadanie 22) pola odpowiedzi, ścieżki i nazwy skryptów były założeniami, bo prompt ich nie podawał. Wyglądają tak samo pewnie jak fakty, dlatego trzeba je jawnie oznaczać.
5. **Nie wszystko da się sprawdzić.** Jenkinsa, Dockera, bazy MySQL ani renderowania Mermaid nie uruchamiałem. Te zadania są **przeanalizowane, ale nieprzetestowane**, i w plikach to zaznaczyłem.

## 2. Mocne i słabe strony AI w kontekście DevOps

### Mocne strony

| Obszar | Przykład z serii |
|---|---|
| Szkielety konfiguracji i kodu | Dockerfile, `.gitignore`, Jenkinsfile, JCasC, docker-compose |
| Wyjaśnianie | Błąd zajętego portu (zad. 8), logi kontenera (zad. 14), dane wydajnościowe (zad. 24) |
| Wyszukiwanie błędów w konfiguracji | YAML (zad. 9), Jenkinsfile (zad. 26) |
| Tłumaczenie między technologiami | Bash na PowerShell (zad. 16), JSON na CSV (zad. 21) |
| Dokumentacja i diagramy | README, API, Mermaid, ASCII (zad. 5, 6, 19, 22, 27) |
| Refaktoryzacja i optymalizacja | Zad. 12, 15, 23 |
| Praca z formatami pomocniczymi | Wyrażenia regularne (zad. 20) |

### Słabe strony

| Ograniczenie | Skutek |
|---|---|
| Brak wiedzy o konkretnym środowisku | Zgadywanie nazw, ścieżek, wersji i adresów |
| Pewny ton mimo niepewności | Błędy i zmyślenia brzmią wiarygodnie |
| Subtelne różnice w zachowaniu | Kolejność wyników, kodowanie plików, kompatybilność wersji |
| Brak możliwości uruchomienia we własnym środowisku | Konfiguracje Jenkinsa, Dockera i bazy wymagają sprawdzenia u siebie |
| Aktualność | Wersje narzędzi i składnia wtyczek mogą być przestarzałe |
| Bezpieczeństwo | Wygenerowane przykłady mogą zawierać proste hasła lub zbyt szerokie uprawnienia |

## 3. Scenariusze, w których AI najbardziej usprawni pracę

1. **Diagnozowanie błędów i logów.** Wklejasz komunikat lub fragment logu i dostajesz przyczynę, kroki diagnostyczne i komendy (zad. 8, 14). To oszczędza czas przy typowych problemach, ale proponowane polecenia warto rozumieć, zanim się je uruchomi.
2. **Szkice konfiguracji i pipeline'ów** (Dockerfile, CI/CD, IaC). Szybki start zamiast pustego pliku, potem dopracowanie pod własny projekt i uruchomienie w prawdziwym środowisku.
3. **Przegląd konfiguracji pod kątem błędów i bezpieczeństwa.** AI jest skuteczne w wychwytywaniu literówek, niepoprawnych poleceń i oczywistych luk (zad. 9, 18, 26). Jako dodatkowa para oczu, a nie jedyna kontrola.
4. **Dokumentacja i diagramy.** README, opisy endpointów, schematy Mermaid i runbooki powstają szybko. Trzeba je tylko zweryfikować z rzeczywistym kodem.
5. **Automatyzacja drobnych zadań i migracje** (skrypty Bash, PowerShell i Python, konwersje formatów, wyrażenia regularne). Dobra jakość przy małych, dobrze zdefiniowanych zadaniach.

## 4. Wskazówki do efektywnego korzystania z AI

1. **Podawaj konkrety:** wersje, system, ograniczenia, oczekiwany format i przykład danych. Im mniej luk, tym mniej zgadywania.
2. **Podawaj kontekst problemu:** komunikat błędu w całości, fragment konfiguracji, co już próbowałeś.
3. **Dziel duże zadania na etapy** i weryfikuj każdy z nich.
4. **Zawsze testuj wynik.** Uruchom kod, zwaliduj konfigurację (`docker compose config`, linter Jenkinsa, `bash -n`), porównaj z oryginałem na losowych danych.
5. **Proś o założenia wprost:** "wypisz, co przyjąłeś, a czego nie wiedziałeś".
6. **Nie wklejaj sekretów** (hasła, tokeny, klucze). Używaj zmiennych środowiskowych i zamienników w przykładach.
7. **Traktuj AI jak szybkiego, ale niedoświadczonego współpracownika.** Przyspiesza pracę, ale odpowiedzialność za wynik zostaje po stronie człowieka (code review, testy, kontrola w CI).
8. **Zrozum, zanim użyjesz.** Prośba o wyjaśnienie "linia po linii" (zad. 7) buduje własną wiedzę, a ślepe kopiowanie ją osłabia.
9. **Wersjonuj wyniki w Git** razem z promptami, żeby można było wrócić do tego, co i dlaczego zostało wygenerowane.

## 5. Moje przemyślenia

Najważniejsza lekcja z tej serii: AI jest świetnym **akceleratorem**, ale nie **autorytetem**. Największa wartość pojawiała się tam, gdzie wynik dało się szybko sprawdzić (test, parser, porównanie z oryginałem), a największe ryzyko tam, gdzie nie dało się go sprawdzić bez prawdziwego środowiska (Jenkins, Docker, baza danych).

Dwa błędy z serii (kolejność wyników i polskie znaki w PowerShellu) nie wyglądały na błędy w odpowiedzi, a wyszły dopiero po uruchomieniu kodu. To mocny argument za nawykiem: **najpierw zweryfikuj, potem zaufaj**. W praktyce DevOps taki nawyk jest zresztą naturalny, bo cały pipeline CI/CD służy do automatycznego sprawdzania zmian.

Drugi wniosek dotyczy komunikacji: im lepiej opiszę środowisko i oczekiwania, tym lepszy wynik. Pisanie dobrego polecenia to w dużej mierze umiejętność precyzyjnego formułowania wymagań, która przydaje się także w pracy z ludźmi i w tworzeniu dokumentacji.

Na koniec uwaga o uczciwości: zadania w tej serii wykonywałem jako asystent w terminalu (Claude Code), a nie w panelu Cursor, i nie wszystkie elementy dało się odtworzyć dosłownie (np. zrzuty ekranu z Mermaid Live Editor). Odpowiednie pliki to zaznaczają.
