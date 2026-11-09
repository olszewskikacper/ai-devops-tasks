# Zadanie 4: Określanie roli w promptach

**Użyty asystent:** Claude (Claude Code)

## Prompt 1: zwykłe pytanie

```
Jak rozwiązać problem z dużym zużyciem pamięci przez kontener Docker?
```

### Odpowiedź

1. **Sprawdź zużycie:** `docker stats` pokaże pamięć każdego kontenera na żywo.
2. **Ustaw limit pamięci:** `docker run --memory=512m ...`, żeby jeden kontener nie zjadał całego hosta.
3. **Znajdź przyczynę w aplikacji:** wycieki pamięci, zbyt duże cache, zbyt wiele wątków lub procesów. Użyj profilera dla swojego języka.
4. **Zmniejsz obraz i zależności:** użyj lżejszego obrazu bazowego (np. alpine) i usuń niepotrzebne pakiety.
5. **Zrestartuj kontener** jako rozwiązanie tymczasowe, np. z `--restart=unless-stopped`.

## Prompt 2: z przypisaną rolą

```
Jesteś doświadczonym DevOps Engineerem z 10-letnim doświadczeniem. Jak rozwiązać problem z dużym zużyciem pamięci przez kontener Docker?
```

### Odpowiedź

Zacząłbym od diagnozy, a dopiero potem dobrał rozwiązanie.

**1. Zmierz i zlokalizuj**
- `docker stats --no-stream` pokazuje bieżące zużycie, a `docker inspect <id> --format '{{.State.OOMKilled}}'` sprawdza, czy kontener był ubity przez OOM killera.
- `docker exec <id> cat /sys/fs/cgroup/memory.current` (cgroup v2) daje dokładną wartość widzianą przez jądro. Pamiętaj, że w cgroup liczy się też page cache, więc samo `docker stats` bywa mylące.
- Historia i trendy: cAdvisor, Prometheus i Grafana. Wyciek widać jako stały wzrost bez spadków. Jednorazowy skok to zwykle obciążenie.

**2. Odróżnij wyciek od zwykłego zapotrzebowania**
- Wyciek: pamięć rośnie liniowo mimo stałego ruchu. Użyj profilowania w języku aplikacji (heap dump w JVM, `--inspect` w Node, `tracemalloc` w Pythonie, `pprof` w Go).
- Zapotrzebowanie: zwiększ limit lub zoptymalizuj dane i cache.
- Częsta pułapka: runtime nie widzi limitu kontenera. JVM ustaw przez `-XX:MaxRAMPercentage`, a Node przez `--max-old-space-size`.

**3. Ustaw limity i rezerwacje**
- `docker run --memory=1g --memory-reservation=768m --memory-swap=1g`. Ustawienie swap równego limitowi wyłącza swap, więc awaria jest szybka i przewidywalna.
- W Compose: `deploy.resources.limits.memory`. W Kubernetes: `resources.requests` i `limits`, przy czym limit dobieraj na podstawie realnych pomiarów, nie zgadywania.

**4. Zoptymalizuj obraz i proces**
- Budowanie wieloetapowe (multi-stage), lekkie obrazy bazowe, jeden proces na kontener.
- Ogranicz liczbę workerów (np. gunicorn, nginx) do liczby wynikającej z limitu pamięci.

**5. Zapobiegaj na przyszłość**
- Alert na np. 80% limitu (Prometheus Alertmanager) zamiast reagowania po OOM.
- Test obciążeniowy przed wdrożeniem i healthcheck z automatycznym restartem jako siatka bezpieczeństwa, a nie jako lekarstwo.

**Zasada:** najpierw pomiar, potem limit, a restart traktuj tylko jako obejście do czasu znalezienia przyczyny.

## Porównanie i obserwacje

| Aspekt | Zwykły prompt | Prompt z rolą |
|---|---|---|
| Struktura | Płaska lista 5 kroków | Podział na fazy: diagnoza, analiza, limity, optymalizacja, prewencja |
| Szczegółowość | Ogólna | Konkretne flagi i komendy (`--memory-swap`, `OOMKilled`, cgroup v2) |
| Narzędzia | `docker stats`, profiler (ogólnie) | cAdvisor, Prometheus, Grafana, Alertmanager, pprof, tracemalloc |
| Perspektywa | Lista możliwych działań | Metodyka pracy: najpierw diagnoza, restart tylko jako obejście |
| Ostrzeżenia | Brak | Pułapki praktyczne (page cache, runtime niewidzący limitu) |

**Wnioski:**
- Przypisanie roli zmieniło ton, głębokość i kolejność odpowiedzi. Odpowiedź ekspercka zaczyna od diagnozy, a nie od gotowych rozwiązań.
- Dodała też praktyczne niuanse, które pojawiają się z doświadczeniem: pułapki, kompromisy i profilaktykę.
- Rola nie dodaje wiedzy, której model nie ma. Kieruje nią w stronę rejestru i poziomu szczegółu typowego dla specjalisty.
- Rola działa najlepiej razem z konkretnym kontekstem (stack, wersje, objawy). Sama zmienia styl, ale nie zastąpi danych o problemie.
