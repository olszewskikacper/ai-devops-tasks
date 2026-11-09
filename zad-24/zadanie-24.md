# Zadanie 24: Interpretacja danych wydajnościowych

**Użyty asystent:** Claude (Claude Code)

## Dane wejściowe

```
Metryki serwera API (ostatnie 24h):
- Średni czas odpowiedzi: 230ms
- 95 percentyl czasu odpowiedzi: 450ms
- 99 percentyl czasu odpowiedzi: 1200ms
- Liczba zapytań: 15,000
- Liczba błędów 5xx: 120
- Użycie CPU: średnio 45%, max 80%
- Użycie pamięci: średnio 2.1GB, max 3.5GB (z 4GB dostępnych)
```

## Pytanie

```
Zinterpretuj te dane. Czy widzisz jakieś potencjalne problemy? Co sugerujesz, aby poprawić wydajność?
```

## Interpretacja

### Wartości wyliczone z danych

| Wskaźnik | Wartość | Komentarz |
|---|---|---|
| Wskaźnik błędów 5xx | 120 / 15 000 = **0,8%** | Wyraźnie za dużo jak na błędy serwera. |
| Średnie obciążenie | 15 000 / 86 400 s ≈ **0,17 żądania/s** (ok. 625/h) | Bardzo niskie. |
| Żądania wolniejsze niż 450 ms | ok. 5% ≈ **750** | Wynika z definicji p95. |
| Żądania wolniejsze niż 1200 ms | ok. 1% ≈ **150** | Wynika z definicji p99. |
| Szczyt pamięci | 3,5 / 4 GB = **87,5%** | Mały zapas. |
| Średnia pamięć | 2,1 / 4 GB = 52,5% | Wysoki poziom bazowy jak na niski ruch. |

### Obserwacje

1. **Opóźnienia: długi ogon.** Średnia (230 ms) jest dobra, p95 (450 ms) akceptowalny, ale p99 (1200 ms) jest około 5 razy większy od średniej. Jedno na sto żądań jest wyraźnie wolne. Średnia ukrywa ten problem, więc to percentyle są tu ważniejsze. Wolne żądania mogą wynikać np. z zimnych cache, wolnych zapytań do bazy, pauz odśmiecania pamięci (GC) albo zewnętrznych zależności.
2. **Błędy 5xx: 0,8%.** Przy typowym celu dostępności 99,9% (czyli 0,1% błędów) to wartość ośmiokrotnie za wysoka. Dane nie mówią, kiedy błędy występują, więc nie wiadomo, czy są rozłożone równomiernie, czy skupione w krótkich incydentach.
3. **CPU: nie jest wąskim gardłem.** Średnio 45% i szczyt 80% to rozsądny zapas. Szczyt 80% jest jednak blisko progu, od którego rosną kolejki.
4. **Pamięć: główne ryzyko.** Szczyt 3,5 GB z 4 GB oznacza, że zostaje tylko 0,5 GB zapasu. Dodatkowo średnie 2,1 GB przy bardzo małym ruchu sugeruje wysokie zużycie bazowe (duże cache, wyciek pamięci albo zbyt hojnie ustawiony runtime). Gdy limit pamięci zostanie przekroczony, proces może zostać ubity (OOM) i zwrócić błędy 5xx.

### Potencjalne powiązanie, które trzeba sprawdzić

Wolne odpowiedzi (p99), błędy 5xx i wysoki szczyt pamięci **mogą mieć wspólną przyczynę**, np. presję na pamięć powodującą częste GC, a w skrajnym przypadku restarty. **To hipoteza, a nie wniosek.** Z tych danych nie da się tego udowodnić, bo brakuje korelacji w czasie.

## Czego brakuje w danych

- Rozkład w czasie (godzinowy): czy błędy i wolne żądania występują w tych samych momentach co szczyty pamięci i CPU.
- Podział na endpointy: czy problem dotyczy kilku konkretnych ścieżek.
- Rodzaje błędów 5xx (500, 502, 503, 504) i ich komunikaty w logach.
- Informacje o restartach procesu lub kontenera (OOM kill).
- Cele jakościowe (SLO), względem których oceniamy wartości.
- Sposób pomiaru: czy czas odpowiedzi liczony jest po stronie serwera czy klienta.

## Rekomendacje

### Pilne (diagnostyka)

1. **Sprawdzić, skąd biorą się błędy 5xx:** logi aplikacji, restarty, `docker inspect ... OOMKilled`, komunikaty z bazy i zależności.
2. **Wykres pamięci w czasie.** Jeśli rośnie liniowo bez spadków, to wyciek pamięci i trzeba użyć profilera pamięci. Jeśli skacze, trzeba znaleźć endpointy lub zadania, które ją zajmują.
3. **Skorelować** p99, 5xx i pamięć na wspólnej osi czasu (Prometheus i Grafana).

### Krótkoterminowe

4. **Zwiększyć zapas pamięci** (np. do 6–8 GB) albo zmniejszyć zużycie. To obejście na czas diagnozy, a nie rozwiązanie przyczyny.
5. **Ustawić limity i alerty:** alert przy 80% pamięci, przy wskaźniku 5xx powyżej 0,5% i przy p99 powyżej ustalonego progu.
6. **Zidentyfikować najwolniejsze endpointy** (śledzenie, np. OpenTelemetry) i sprawdzić zapytania do bazy (indeksy, N+1).

### Dłuższy horyzont

7. **Cache** dla często odczytywanych danych, **timeouty i ponowienia** dla zależności zewnętrznych.
8. **Skalowanie poziome** z równoważeniem obciążenia, gdy ruch wzrośnie. Przy obecnym ruchu 0,17 żądania/s CPU nie jest problemem.
9. **Testy obciążeniowe** (k6, JMeter), żeby poznać realne granice przed wzrostem ruchu.

## Wniosek

Najważniejszy sygnał to nie średnia, lecz **ogon opóźnień (p99), 0,8% błędów 5xx i niewielki zapas pamięci**. Wyglądają jak objawy jednego problemu z zasobami lub z konkretnymi wolnymi ścieżkami. Zanim zacznie się optymalizować, trzeba zebrać dane, które pozwolą to potwierdzić.
