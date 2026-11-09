# Zadanie 26: Analiza i poprawa istniejącego Jenkinsfile

**Użyty asystent:** Claude (Claude Code)

## Prompt

```
Ten Jenkinsfile zawiera kilka błędów. Znajdź je i zaproponuj poprawioną wersję. Wyjaśnij, jakie były problemy i jak je naprawiłeś.
```

## Oryginał (`Jenkinsfile-with-errors`)

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            stesp {
                sh 'npm install'
                sh 'npm build'
            }
        }
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker build -t myapp .'
                sh 'docker push myapp:latest'
            }
            when {
                branch 'master'
            }
        }
    }
}
```

## Znalezione błędy

### Błędy, które psują pipeline

| # | Miejsce | Problem | Poprawka |
|---|---|---|---|
| 1 | `stesp {` w etapie Build | **Literówka** w słowie kluczowym `steps`. Jenkins odrzuci plik z błędem składni jeszcze przed uruchomieniem. | `steps {` |
| 2 | `sh 'npm build'` | W npm **nie ma polecenia `build`**. Skrypty uruchamia się przez `npm run <nazwa>`. Etap zakończy się błędem. | `sh 'npm run build'` |
| 3 | `docker push myapp:latest` | Obraz jest nazwany tylko `myapp`, bez użytkownika lub rejestru, więc Docker próbuje wysłać go do `docker.io/library/myapp`, na co nie ma uprawnień. Brakuje też **logowania** do rejestru. | Pełna nazwa (`twoj-uzytkownik/myapp`) oraz `docker login` z poświadczeniami Jenkinsa (`withCredentials`) |

### Problemy z jakością i bezpieczeństwem (nie błędy składni)

| # | Miejsce | Problem | Poprawka |
|---|---|---|---|
| 4 | `branch 'master'` | Domyślna gałąź w większości repozytoriów to dziś `main`. Jeśli gałąź nazywa się inaczej, etap Deploy **nigdy się nie uruchomi**, i to bez żadnego błędu. Warunek `branch` działa też tylko w zadaniach wielogałęziowych (multibranch). | `branch 'main'` (dostosować do repozytorium) |
| 5 | `when` po `steps` | Zgodnie z konwencją i dokumentacją warunek `when` stawia się **przed** `steps`, bo opisuje, czy etap w ogóle ma się wykonać. Nie sprawdzałem, czy Jenkins odrzuci taką kolejność, więc traktuję to jako kwestię czytelności, a nie pewny błąd. | Przeniesienie `when` nad `steps` |
| 6 | Tylko tag `latest` | Brak unikalnego tagu uniemożliwia identyfikację i wycofanie wersji. | Dodatkowy tag z `$BUILD_NUMBER` |
| 7 | Budowanie i wysyłanie bez poświadczeń w kodzie | Poprawne podejście to magazyn poświadczeń Jenkinsa, a nie hasła w pliku. | `withCredentials` i `--password-stdin` |

## Poprawiona wersja (`Jenkinsfile-fixed`)

```groovy
pipeline {
    agent any

    environment {
        // Pełna nazwa obrazu wraz z użytkownikiem/rejestrem
        IMAGE_NAME = 'twoj-uzytkownik/myapp'
    }

    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }

        stage('Test') {
            steps {
                sh 'npm test'
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh 'docker build -t $IMAGE_NAME:$BUILD_NUMBER -t $IMAGE_NAME:latest .'
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'REGISTRY_USER',
                    passwordVariable: 'REGISTRY_PASS'
                )]) {
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
}
```

## Uwagi

- Kolejność etapów (Build, Test, Deploy) została bez zmian, a Deploy uruchamia się tylko dla gałęzi głównej.
- Dodatkowe usprawnienia, które warto rozważyć: `post { always { cleanWs() } }`, `options { timeout(...) }` oraz zamiana `npm install` na `npm ci`.
- Nazwa obrazu i identyfikator poświadczenia (`dockerhub-credentials`) to przykłady do dostosowania.

## Weryfikacja

**Nie uruchamiałem tych plików w Jenkinsie.** Sprawdziłem tylko, że nawiasy klamrowe w obu wersjach są zbilansowane. Błędy 1 i 2 wynikają ze składni Jenkinsa i npm, a błąd 3 z działania Dockera. Jeśli masz dostęp do Jenkinsa, plik można zwalidować przez Declarative Linter:

```bash
curl -X POST -u UZYTKOWNIK:TOKEN -F "jenkinsfile=<Jenkinsfile-fixed" $JENKINS_URL/pipeline-model-converter/validate
```
