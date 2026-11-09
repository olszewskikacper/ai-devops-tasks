# Zadanie 2: Porównanie odpowiedzi różnych modeli

**Pytanie (identyczne dla obu modeli):**
> Wymień 5 korzyści z używania kontenerów Docker w środowisku programistycznym.

**Modele:** Claude Haiku (mały, szybki) oraz Claude Opus (duży, najbardziej zaawansowany). Oba odpytane z tym samym promptem.

## Odpowiedź 1: Claude Haiku

1. Spójność środowiska: kod działa tak samo na laptopie, u kolegi i na serwerze, bo wszyscy uruchamiają ten sam obraz kontenera. Znika problem „u mnie działa”.
2. Izolacja zależności: każdy projekt ma własne wersje języka, bibliotek i narzędzi, więc projekty nie konfliktują ze sobą i nie zaśmiecają systemu hosta.
3. Szybkie wdrożenie nowych osób: zamiast ręcznej instalacji kilkunastu narzędzi wystarcza zazwyczaj jedno polecenie (np. docker compose up) i środowisko jest gotowe.
4. Łatwa odtwarzalność i czyszczenie: środowisko jest opisane w kodzie (Dockerfile, compose), można je w każdej chwili odbudować od zera, a usunięcie kontenera nie pozostawia śmieci w systemie.
5. Prosta obsługa usług pomocniczych: bazy danych, kolejki, cache i inne zależności uruchamia się jako kontenery w ustalonej wersji, co ułatwia testowanie i zgodność z produkcją.

## Odpowiedź 2: Claude Opus

1. **Spójność środowisk.** Kod uruchamia się tak samo na każdej maszynie, czyli u programisty, na CI i na produkcji, więc znika problem „u mnie działa”.
2. **Izolacja zależności.** Każdy projekt ma własne wersje bibliotek, runtime'ów i narzędzi, które ze sobą nie kolidują. Na jednym hoście mogą równolegle działać na przykład Python 3.9 i 3.12.
3. **Szybki onboarding i odtwarzalność.** Nowa osoba stawia całe środowisko jednym poleceniem (`docker compose up`), bez ręcznej instalacji i konfiguracji. Środowisko jest zapisane jako kod w Dockerfile i compose.yaml.
4. **Lekkość i szybkość.** Kontenery współdzielą jądro systemu hosta, więc startują w sekundy i zużywają mniej zasobów niż maszyny wirtualne. Łatwo je tworzyć, usuwać i odtwarzać.
5. **Łatwa integracja z CI/CD i usługami zewnętrznymi.** Bazy danych, kolejki czy cache (PostgreSQL, Redis, RabbitMQ) uruchamia się lokalnie w kontenerach, bez instalowania ich w systemie. Ten sam obraz można potem budować, testować i wdrażać w pipeline'ie.

## Podsumowanie różnic

| Aspekt | Haiku | Opus |
|---|---|---|
| Długość | Krótsza, zwięzła | Nieco dłuższa |
| Formatowanie | Zwykła lista | Pogrubione nagłówki punktów |
| Konkretne przykłady | Ogólne (`docker compose up`) | Więcej: Python 3.9 vs 3.12, PostgreSQL/Redis/RabbitMQ |
| Pokryte tematy | Spójność, izolacja, onboarding, odtwarzalność, usługi pomocnicze | Te same plus lekkość względem VM i integracja z CI/CD |

**Wnioski:** Oba modele poprawnie wskazały trzon korzyści (spójność, izolacja, szybki onboarding). Haiku dał zwięzłą, poprawną odpowiedź, ale bardziej ogólną. Opus był bardziej szczegółowy, podał konkretne przykłady i wymienił korzyści (lekkość względem VM, CI/CD), których Haiku nie ujął osobno. Haiku połączył natomiast odtwarzalność z czyszczeniem środowiska. Do szybkiego przeglądu wystarczy mniejszy model, a do tematów wymagających głębi i przykładów lepszy jest większy.
