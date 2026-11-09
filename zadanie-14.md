# Zadanie 14: Wyjaśnienie fragmentu logów

**Użyty asystent:** Claude (Claude Code)

## Logi

```
May 19 10:15:32 server dockerd[1234]: time="2025-05-19T10:15:32.123456789Z" level=info msg="Container 78a2b3c4 health status changed from starting to healthy"
May 19 10:16:45 server dockerd[1234]: time="2025-05-19T10:16:45.987654321Z" level=info msg="Container 78a2b3c4 failed to connect to 172.17.0.3:5432: connection refused"
May 19 10:16:47 server dockerd[1234]: time="2025-05-19T10:16:47.246813579Z" level=warning msg="Container 78a2b3c4 health status changed from healthy to unhealthy"
```

## Pytanie

```
Co się dzieje w tych logach? Jakie problemy można zidentyfikować?
```

## Co się dzieje (oś czasu)

| Czas | Poziom | Zdarzenie |
|---|---|---|
| 10:15:32 | info | Kontener `78a2b3c4` przechodzi ze stanu `starting` do `healthy`. Healthcheck zaczął przechodzić pomyślnie. |
| 10:16:45 | info | Kontener nie może połączyć się z `172.17.0.3:5432` (`connection refused`). |
| 10:16:47 | warning | Stan zdrowia zmienia się z `healthy` na `unhealthy`. |

Komponenty:
- `dockerd[1234]` – demon Dockera, który zapisuje zdarzenia.
- `172.17.0.3` – adres w domyślnej sieci mostkowej Dockera (`docker0`, podsieć `172.17.0.0/16`).
- Port `5432` – standardowy port **PostgreSQL**.
- `connection refused` – na docelowym adresie nikt nie nasłuchuje na tym porcie. Host odpowiada, ale odmawia połączenia.

## Zidentyfikowane problemy

1. **Utrata połączenia z bazą PostgreSQL.** Kontener (prawdopodobnie aplikacja) przestał łączyć się z bazą pod `172.17.0.3:5432`. Najczęstsze przyczyny: kontener bazy został zatrzymany, zrestartowany lub się zawiesił, Postgres jeszcze się nie uruchomił po restarcie, albo adres IP kontenera bazy się zmienił.
2. **Kontener przeszedł w stan `unhealthy`.** Healthcheck prawdopodobnie zależy od połączenia z bazą, więc niedostępność bazy została przeniesiona na zdrowie kontenera. Przejście nastąpiło 2 sekundy po błędzie połączenia, a kontener był zdrowy przez około 73 sekundy.
3. **Twardo wpisany adres IP.** Połączenie po `172.17.0.3` jest kruche, bo w domyślnej sieci Dockera adresy IP przydzielane są dynamicznie i zmieniają się po restarcie kontenera. Lepiej używać nazw usług i własnej sieci użytkownika.
4. **Brak mechanizmu oczekiwania na zależność.** Aplikacja uzyskała status `healthy`, zanim (lub mimo że) baza była stabilnie dostępna. Brakuje retry z opóźnieniem albo `depends_on` z warunkiem `service_healthy`.

## Czego z logów nie da się ustalić

- Czy to ten sam kontener łączy się z bazą, czy baza to osobny kontener. Jest to najbardziej prawdopodobne, ale to założenie.
- Dlaczego baza była niedostępna. Potrzebne są logi kontenera bazy.
- Dziwne jest, że komunikat o błędzie połączenia pochodzi z `dockerd`. Zwykle taki błąd loguje sama aplikacja. Warto sprawdzić, jak skonfigurowano zbieranie logów.

## Jak zdiagnozować

```bash
docker ps -a                                   # czy kontener bazy działa
docker logs 78a2b3c4                           # logi aplikacji
docker logs <kontener_bazy>                    # logi PostgreSQL
docker inspect 78a2b3c4 --format '{{json .State.Health}}'   # historia healthchecków
docker network inspect bridge                  # adresy IP kontenerów
```

## Zalecenia

1. Sprawdzić, czy kontener PostgreSQL działa, i przeanalizować jego logi pod kątem restartu lub awarii.
2. Używać własnej sieci Dockera i nazwy usługi (np. `db:5432`) zamiast adresu IP.
3. W Docker Compose ustawić `depends_on` z `condition: service_healthy` i healthcheck bazy (`pg_isready`).
4. Dodać w aplikacji ponawianie połączenia (retry z backoffem).
5. Ustawić monitoring i alert na stan `unhealthy`.
