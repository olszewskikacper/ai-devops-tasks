# Zadanie 29: Generowanie szablonu konfiguracji Jenkins

**Użyty asystent:** Claude (Claude Code)

## Prompt 1

```
Wygeneruj szablon Jenkins Configuration as Code (JCasC) w formacie YAML, który konfiguruje:
- podstawowe ustawienia Jenkins (liczba wykonawców, timeout)
- globalny katalog narzędzi (Maven, Node.js, Docker)
- podstawowe wtyczki
- przykładowe zadanie typu pipeline
```

Wygenerowany plik: [`jenkins-casc.yaml`](jenkins-casc.yaml).

## Co konfiguruje szablon

| Sekcja | Zawartość |
|---|---|
| `jenkins` | Komunikat systemowy, `numExecutors: 2`, ponowienia pobierania z repozytorium, okres ciszy przed buildem, lokalna baza użytkowników z kontem `admin` (hasło ze zmiennej `${ADMIN_PASSWORD}`), wyłączona rejestracja i brak dostępu anonimowego. |
| `tool` | Globalny katalog narzędzi: Maven 3.9.9, Node.js 20.18.0 i Docker (instalowane automatycznie). |
| `unclassified` | Adres URL Jenkinsa. |
| `jobs` | Przykładowe zadanie `przykladowy-pipeline` (typ pipeline), tworzone przez wtyczkę Job DSL. |

### Dwie ważne uwagi o zakresie

1. **Timeout.** Jenkins nie ma jednego globalnego ustawienia limitu czasu buildów w podstawowej konfiguracji. Dlatego limit czasu (`timeout(time: 15, unit: 'MINUTES')`) umieściłem w opcjach przykładowego pipeline'u. Globalny limit wymagałby dodatkowej wtyczki (Build Timeout).
2. **Wtyczki.** JCasC konfiguruje **ustawienia** wtyczek, ale ich nie instaluje. Dlatego lista wtyczek trafia do osobnego pliku `plugins.txt` (poniżej), a ich instalacją zajmuje się narzędzie `jenkins-plugin-cli`.

## Prompt 2

```
Wyjaśnij, jak używać tego pliku konfiguracyjnego z Jenkinsem. Podaj kroki instalacji i uruchomienia Jenkinsa z tym szablonem.
```

## Instrukcja użycia

Najprostsza droga to uruchomienie Jenkinsa w Dockerze z własnym obrazem. Utwórz katalog z trzema plikami: `jenkins-casc.yaml`, `plugins.txt` i `Dockerfile`.

### Krok 1: `plugins.txt` (wtyczki)

```
configuration-as-code
job-dsl
workflow-aggregator
git
nodejs
maven-plugin
docker-commons
```

Opis wtyczek:

| Wtyczka | Po co |
|---|---|
| `configuration-as-code` | Wczytuje plik JCasC. |
| `job-dsl` | Pozwala tworzyć zadania z sekcji `jobs`. |
| `workflow-aggregator` | Pakiet wtyczek pipeline (Pipeline). |
| `git` | Obsługa repozytoriów Git. |
| `nodejs` | Katalog narzędzi Node.js. |
| `maven-plugin` | Katalog narzędzi Maven. |
| `docker-commons` | Katalog narzędzi Docker i obsługa poświadczeń. |

### Krok 2: `Dockerfile`

```dockerfile
FROM jenkins/jenkins:lts-jdk17

# Wyłączamy kreator pierwszego uruchomienia, bo konfigurację zapewnia JCasC
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"
ENV CASC_JENKINS_CONFIG=/usr/local/casc/jenkins-casc.yaml

# Instalacja wtyczek
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

# Plik konfiguracyjny JCasC
COPY --chown=jenkins:jenkins jenkins-casc.yaml /usr/local/casc/jenkins-casc.yaml
```

Plik konfiguracyjny leży poza katalogiem `/var/jenkins_home`, żeby nie kolidował z wolumenem danych.

### Krok 3: budowanie obrazu i uruchomienie

```bash
docker build -t jenkins-casc .

docker run -d --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  -e ADMIN_PASSWORD='ZmienToHaslo123' \
  -v jenkins_home:/var/jenkins_home \
  jenkins-casc
```

### Krok 4: sprawdzenie

1. Otwórz `http://localhost:8080` i zaloguj się jako `admin` z hasłem z `ADMIN_PASSWORD`.
2. Sprawdź, że widoczny jest komunikat systemowy i zadanie `przykladowy-pipeline`.
3. Wejdź w **Manage Jenkins → Tools** i sprawdź narzędzia Maven, NodeJS i Docker.
4. Wejdź w **Manage Jenkins → Configuration as Code**, żeby zobaczyć wczytaną konfigurację lub błędy.
5. Uruchom `przykladowy-pipeline` (**Build Now**) i sprawdź log.

### Zmiana konfiguracji

Edytujesz `jenkins-casc.yaml`, a potem w **Manage Jenkins → Configuration as Code** klikasz **Reload existing configuration** (albo przebudowujesz obraz). Zmiany wprowadzone ręcznie w interfejsie mogą zostać nadpisane przy następnym wczytaniu, więc YAML jest jedynym źródłem prawdy.

### Alternatywa: bez własnego obrazu

Można też uruchomić standardowy obraz, zainstalować wtyczki ręcznie i zamontować plik:

```bash
docker run -d -p 8080:8080 -e ADMIN_PASSWORD='...' \
  -e CASC_JENKINS_CONFIG=/casc/jenkins-casc.yaml \
  -v $(pwd)/jenkins-casc.yaml:/casc/jenkins-casc.yaml \
  jenkins/jenkins:lts-jdk17
```

W tym wariancie wtyczki z `plugins.txt` trzeba zainstalować osobno, inaczej konfiguracja zgłosi błąd.

## Bezpieczeństwo

- Hasło nie jest zapisane w pliku, tylko pobierane ze zmiennej środowiskowej `ADMIN_PASSWORD`. W produkcji lepsze są sekrety Dockera lub menedżer sekretów.
- Rejestracja nowych użytkowników i dostęp anonimowy są wyłączone.
- Wtyczka Job DSL z `sandbox(true)` ogranicza uprawnienia skryptów zadania.

## Weryfikacja

- **Składnia YAML:** przetworzyłem plik parserem YAML i wczytał się poprawnie (klucze główne: `jenkins`, `tool`, `unclassified`, `jobs`).
- **Nie uruchamiałem Jenkinsa.** Nie sprawdziłem więc, czy nazwy kluczy i instalatorów (np. `nodeJSInstaller`, `fromDocker`) pasują do schematu w aktualnych wersjach wtyczek. Szablon oparłem na standardowej dokumentacji JCasC, ale ostateczną walidacją jest widok **Manage Jenkins → Configuration as Code** po uruchomieniu. Wersje narzędzi (Maven 3.9.9, Node.js 20.18.0) warto dostosować do aktualnych.
