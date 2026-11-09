# Zadanie 28: Skrypt do zarządzania zadaniami Jenkins

**Użyty asystent:** Claude (Claude Code)

## Prompt 1

```
Napisz skrypt w Pythonie, który używa Jenkins API do:
- listowania wszystkich zadań (jobs)
- sprawdzania statusu ostatnich buildów
- uruchamiania wybranego zadania

Uwzględnij obsługę autoryzacji i obsługę błędów.
```

Wygenerowany skrypt: [`jenkins-manager.py`](jenkins-manager.py).

## Prompt 2

```
Wyjaśnij, jak działa ten skrypt i jakich bibliotek używa do komunikacji z Jenkins API. Podaj również przykładowe polecenia, jak używać tego skryptu.
```

## Jak działa skrypt

Skrypt to narzędzie wiersza poleceń z trzema podpoleceniami: `list`, `status` i `build`. Komunikuje się z Jenkinsem przez jego **REST API** (JSON po HTTP).

### Użyte biblioteki

Skrypt używa **wyłącznie biblioteki standardowej Pythona**, więc nie wymaga instalacji żadnych pakietów:

| Biblioteka | Do czego służy |
|---|---|
| `urllib.request`, `urllib.error` | Wysyłanie żądań HTTP i obsługa błędów sieciowych. |
| `urllib.parse` | Kodowanie nazw zadań i parametrów w adresie URL. |
| `base64` | Budowanie nagłówka `Authorization: Basic ...`. |
| `json` | Parsowanie odpowiedzi API. |
| `argparse` | Podpolecenia i argumenty wiersza poleceń. |
| `os`, `sys` | Zmienne środowiskowe i kody wyjścia. |

Popularną alternatywą jest biblioteka `requests` (krótszy kod) lub dedykowana `python-jenkins`. Wybrałem bibliotekę standardową, żeby skrypt działał bez instalowania zależności.

### Struktura

- **`JenkinsClient`** to klasa odpowiadająca za komunikację: `list_jobs()`, `last_build(nazwa)` i `trigger_build(nazwa, parametry)`.
- **`JenkinsError`** to własny wyjątek na wszystkie błędy komunikacji.
- Funkcje `cmd_list`, `cmd_status` i `cmd_build` obsługują podpolecenia.

### Autoryzacja

Skrypt używa **Basic Auth z tokenem API**. Dane podajesz w zmiennych środowiskowych (nie w kodzie ani w historii poleceń):

- `JENKINS_URL`: adres Jenkinsa (np. `http://localhost:8080`),
- `JENKINS_USER`: nazwa użytkownika,
- `JENKINS_API_TOKEN`: token API (nie hasło).

Token wygenerujesz w Jenkinsie: *Twoja nazwa użytkownika → Configure → API Token → Add new Token*.

### Obsługa błędów

| Sytuacja | Zachowanie |
|---|---|
| Brak zmiennych środowiskowych | Czytelny komunikat i kod wyjścia 1. |
| `401` | "nieprawidłowy login lub token API". |
| `403` | "brak uprawnień do tej operacji". |
| `404` | "nie znaleziono zasobu", a dla `status` zadanie bez buildów jest opisane jako "brak buildów (lub zadanie nie istnieje)". |
| Serwer niedostępny | Komunikat o braku połączenia. |
| Przekroczenie czasu | Limit 15 sekund na żądanie. |
| Odpowiedź nie jest JSON-em | Komunikat o nieprawidłowej odpowiedzi. |
| Błędny format parametru `-p` | Komunikat, że potrzeba `KLUCZ=WARTOŚĆ`. |

### Szczegół techniczny: ochrona CSRF

Żądania `POST` (uruchamianie builda) wymagają w wielu instalacjach tzw. crumb (token CSRF). Skrypt pobiera go z `/crumbIssuer/api/json` i dołącza do żądania. Jeśli Jenkins nie udostępnia tego endpointu (404), krok jest pomijany. Zadania w folderach zapisuje się jako `folder/zadanie`, a skrypt zamienia to na ścieżkę `/job/folder/job/zadanie`.

## Przykładowe polecenia

```bash
# Konfiguracja (Linux/macOS)
export JENKINS_URL=http://localhost:8080
export JENKINS_USER=admin
export JENKINS_API_TOKEN=twoj_token

# Konfiguracja (PowerShell)
$env:JENKINS_URL = "http://localhost:8080"
$env:JENKINS_USER = "admin"
$env:JENKINS_API_TOKEN = "twoj_token"

# Lista wszystkich zadań
python jenkins-manager.py list

# Status ostatniego builda wszystkich zadań
python jenkins-manager.py status

# Status jednego zadania (także w folderze)
python jenkins-manager.py status moj-projekt
python jenkins-manager.py status folder/zadanie

# Uruchomienie zadania
python jenkins-manager.py build moj-projekt

# Uruchomienie zadania z parametrami
python jenkins-manager.py build moj-projekt -p ENV=prod -p VERSION=1.2
```

Przykładowe wyjście:

```
$ python jenkins-manager.py status
app-build: #42 SUCCESS (1234 ms)
app-deploy: #7 FAILURE (99 ms)
nigdy: brak buildów (lub zadanie nie istnieje)
```

## Weryfikacja

**Nie testowałem skryptu na prawdziwym Jenkinsie.** Sprawdziłem go na lokalnym, prostym serwerze HTTP, który udawał Jenkinsa (autoryzacja Basic, lista zadań, status buildów, crumb i uruchamianie buildów). Na nim działały: `list`, `status` (wszystkie i jedno zadanie, także z folderu), `build` bez parametrów i z parametrami (serwer odebrał `ENV=prod&VERSION=1.2`) oraz wszystkie ścieżki błędów (zły token, nieznane zadanie, brak zmiennych, niedostępny serwer, błędny parametr), z kodem wyjścia 1.

Test ujawnił jedną niedoskonałość: zadanie bez żadnego builda wypisywało surowy błąd 404. Poprawiłem to na czytelny komunikat. Zachowanie prawdziwego Jenkinsa (np. dokładny format odpowiedzi, ścieżki dla wtyczek folderów) może się nieco różnić od mojego uproszczonego serwera.
