# Zadanie 25: Generowanie prostego Jenkinsfile

**Użyty asystent:** Claude (Claude Code)

## Prompt 1

```
Wygeneruj prosty Jenkinsfile dla aplikacji Node.js, który będzie zawierał etapy:
- checkout kodu z repozytorium
- instalacja zależności (npm install)
- uruchomienie testów (npm test)
- budowanie aplikacji (npm run build)
- budowanie obrazu Docker
- publikowanie obrazu do rejestru Docker

Użyj składni deklaratywnej Jenkinsa.
```

Wygenerowany plik: [`Jenkinsfile`](Jenkinsfile).

```groovy
pipeline {
    agent any

    environment {
        IMAGE_NAME  = 'twoj-uzytkownik/moja-aplikacja'
        REGISTRY_CREDENTIALS = 'dockerhub-credentials'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Install dependencies') { steps { sh 'npm install' } }
        stage('Test') { steps { sh 'npm test' } }
        stage('Build') { steps { sh 'npm run build' } }
        stage('Build Docker image') {
            steps { sh 'docker build -t $IMAGE_NAME:$BUILD_NUMBER -t $IMAGE_NAME:latest .' }
        }
        stage('Push Docker image') {
            steps {
                withCredentials([usernamePassword(credentialsId: env.REGISTRY_CREDENTIALS,
                        usernameVariable: 'REGISTRY_USER', passwordVariable: 'REGISTRY_PASS')]) {
                    sh '''
                        echo "$REGISTRY_PASS" | docker login -u "$REGISTRY_USER" --password-stdin
                        docker push $IMAGE_NAME:$BUILD_NUMBER
                        docker push $IMAGE_NAME:latest
                        docker logout
                    '''
                }
            }
        }
    }

    post { success { ... } failure { ... } always { cleanWs() } }
}
```

(Powyżej wersja skrócona, pełny kod jest w pliku `Jenkinsfile`.)

## Prompt 2

```
Wyjaśnij, co dokładnie dzieje się w każdym etapie tego Jenkinsfile i jakie są najlepsze praktyki przy tworzeniu pipeline'ów Jenkins.
```

## Wyjaśnienie struktury

| Element | Co robi |
|---|---|
| `pipeline { }` | Główny blok składni deklaratywnej. |
| `agent any` | Pipeline może działać na dowolnym dostępnym węźle (agencie) Jenkinsa. |
| `environment` | Zmienne środowiskowe dostępne we wszystkich etapach. |
| `options` | Ustawienia całego pipeline'u: limit czasu 30 minut, przechowywanie 10 ostatnich buildów, zakaz równoległych buildów tego samego zadania. |
| `stages` / `stage` | Kolejne etapy, widoczne w Jenkinsie jako osobne kolumny. |
| `post` | Akcje po zakończeniu, zależnie od wyniku (`success`, `failure`, `always`). |

## Wyjaśnienie etapów

1. **Checkout.** `checkout scm` pobiera kod z repozytorium skonfigurowanego dla zadania, w wersji (commicie lub gałęzi), która uruchomiła build. Jest to pierwszy etap, bo wszystkie kolejne potrzebują kodu.
2. **Install dependencies.** `npm install` instaluje zależności z `package.json` do katalogu `node_modules`. Bez tego nie da się uruchomić testów ani budowania.
3. **Test.** `npm test` uruchamia testy zdefiniowane w skrypcie `test`. Jeśli testy zakończą się błędem (kod wyjścia różny od 0), etap kończy się niepowodzeniem i pipeline się zatrzymuje, więc wadliwy kod nie dociera do obrazu ani do rejestru.
4. **Build.** `npm run build` buduje aplikację (np. transpilacja TypeScript, bundlowanie frontendu). Zwróć uwagę, że potrzebne jest `npm run build`, a samo `npm build` nie jest poprawnym poleceniem do uruchomienia skryptu.
5. **Build Docker image.** `docker build` tworzy obraz z `Dockerfile` i nadaje mu dwa tagi: numer buildu (`$BUILD_NUMBER`, unikalny i identyfikowalny) oraz `latest`.
6. **Push Docker image.** Etap loguje się do rejestru danymi z magazynu poświadczeń Jenkinsa (`withCredentials`), wysyła oba tagi (`docker push`) i się wylogowuje. Hasło jest przekazywane przez `--password-stdin`, żeby nie pojawiło się w liście procesów, a Jenkins maskuje je w logach.
7. **Post.** `cleanWs()` czyści katalog roboczy po buildzie, żeby nie zajmować dysku i nie przenosić plików między buildami.

## Najlepsze praktyki dla pipeline'ów Jenkins

1. **Pipeline as Code.** Trzymaj `Jenkinsfile` w repozytorium razem z kodem. Wtedy jest wersjonowany i przeglądany jak kod.
2. **Składnia deklaratywna** zamiast skryptowej, gdy to możliwe. Jest czytelniejsza i walidowana przed uruchomieniem.
3. **Sekrety tylko przez Credentials.** Nigdy nie wpisuj haseł w `Jenkinsfile`. Używaj `withCredentials` i `--password-stdin`.
4. **`npm ci` zamiast `npm install`** w CI. Instaluje dokładnie wersje z `package-lock.json`, jest szybsze i powtarzalne. Tu użyłem `npm install`, bo o to prosiło zadanie.
5. **Publikuj tylko z gałęzi głównej.** Obecny pipeline wysyła obraz z każdej gałęzi. W praktyce etap push warto objąć warunkiem `when { branch 'main' }` (w pipeline wielogałęziowym).
6. **Tagi z wersją.** Nie polegaj wyłącznie na `latest`. Unikalny tag (numer buildu lub skrót commita) pozwala na wycofanie wersji.
7. **Limity i sprzątanie:** `timeout`, `buildDiscarder`, `cleanWs()`, żeby nie wisiały zawieszone buildy ani nie rosło zużycie dysku.
8. **Fail fast.** Najszybsze kontrole (testy, lint) umieszczaj na początku. Równoległość (`parallel`) tam, gdzie etapy są niezależne.
9. **Izolowane środowisko buildu.** Rozważ agenta w kontenerze (`agent { docker { image 'node:20' } }`) lub narzędzie `tools { nodejs ... }`, zamiast zakładać, że na agencie jest właściwa wersja Node.js.
10. **Powiadomienia i raporty** w bloku `post` (np. wiadomość na Slack lub e-mail o niepowodzeniu, publikacja raportów testów).

## Założenia i weryfikacja

- Jenkinsfile zakłada, że agent ma zainstalowane `node`, `npm` oraz `docker` i że istnieje skonfigurowane poświadczenie `dockerhub-credentials`. Nazwa obrazu `twoj-uzytkownik/moja-aplikacja` to przykład do podmiany.
- Aplikacja musi mieć skrypty `test` i `build` w `package.json` oraz `Dockerfile`.
- **Nie uruchamiałem tego pliku w Jenkinsie** (nie mam instancji). Sprawdziłem jedynie, że nawiasy klamrowe są zbilansowane. Przed użyciem warto zwalidować plik w Jenkinsie (Declarative Linter) lub uruchomić go na testowym zadaniu.
