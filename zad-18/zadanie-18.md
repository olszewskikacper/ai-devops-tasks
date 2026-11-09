# Zadanie 18: Analiza wymagań bezpieczeństwa

**Użyty asystent:** Claude (Claude Code)

## Pytanie 1

```
Jakie są 5 kluczowych praktyk bezpieczeństwa dla aplikacji Dockerowych w środowisku produkcyjnym?
```

### Odpowiedź

1. **Nie uruchamiaj kontenerów jako root.** Proces w kontenerze powinien działać jako zwykły użytkownik. Jeśli atakujący przejmie aplikację, ma ograniczone uprawnienia, a ucieczka z kontenera jest trudniejsza.
2. **Używaj minimalnych, zaufanych obrazów i skanuj je.** Obrazy oficjalne lub zweryfikowane, lekkie (alpine, distroless, slim), z przypiętą wersją (nie `latest`). Skanowanie podatności (Trivy, Docker Scout, Grype) w pipeline CI/CD.
3. **Nie przechowuj sekretów w obrazie ani w repozytorium.** Hasła i klucze przekazuj przez Docker secrets, zmienne środowiskowe z zewnętrznego magazynu (Vault, menedżer sekretów chmury) lub pliki poza repozytorium. Sekrety wpisane w `Dockerfile` zostają w warstwach obrazu.
4. **Ogranicz uprawnienia i zasoby kontenera.** System plików tylko do odczytu (`read_only`), odebranie zbędnych capabilities (`cap_drop: ALL`), `no-new-privileges`, limity pamięci i CPU. Nigdy `--privileged` ani montowanie `docker.sock`.
5. **Izoluj sieć i dbaj o aktualizacje.** Osobne sieci dla usług, wystawianie tylko niezbędnych portów, TLS. Regularna przebudowa obrazów z aktualnymi łatkami i monitoring oraz logowanie zdarzeń.

## Pytanie uzupełniające

```
Jak mogę zaimplementować pierwszą z tych praktyk w moim Dockerfile i docker-compose.yml?
```

### Odpowiedź: uruchamianie jako użytkownik inny niż root

**Dockerfile** (przykład dla Node.js):

```dockerfile
FROM node:20-alpine

WORKDIR /app

# Zależności instalujemy jako root, ale pliki przekazujemy użytkownikowi "node"
COPY --chown=node:node package*.json ./
RUN npm ci --omit=dev

COPY --chown=node:node . .

# Od tego momentu proces działa jako zwykły użytkownik (UID 1000), a nie root
USER node

EXPOSE 3000
CMD ["node", "index.js"]
```

Obraz `node` ma już wbudowanego użytkownika `node`. Dla obrazów bez gotowego użytkownika trzeba go utworzyć:

```dockerfile
RUN addgroup -S app && adduser -S app -G app
USER app
```

**docker-compose.yml:**

```yaml
services:
  app:
    build: .
    user: "1000:1000"            # wymusza użytkownika bez roota (nawet gdyby obraz o tym zapomniał)
    ports:
      - "3000:3000"
    read_only: true              # system plików kontenera tylko do odczytu
    tmpfs:
      - /tmp                     # zapisywalny katalog tymczasowy w pamięci
    cap_drop:
      - ALL                      # odbieramy wszystkie uprawnienia systemowe (capabilities)
    security_opt:
      - no-new-privileges:true   # proces nie może zdobyć wyższych uprawnień
```

Ostatnie trzy ustawienia (`read_only`, `cap_drop`, `no-new-privileges`) należą do praktyki nr 4, ale razem z użytkownikiem bez roota tworzą spójną, utwardzoną konfigurację.

### Uwaga: porty poniżej 1024

Użytkownik bez roota nie może domyślnie nasłuchiwać na portach poniżej 1024. Dlatego aplikacja powinna używać portu wysokiego (np. 3000), a mapowanie na port 80 zrobić po stronie hosta (`"80:3000"`).

### Jak sprawdzić, że działa

```bash
docker compose up -d
docker compose exec app id          # powinno pokazać uid=1000, a nie uid=0(root)
docker compose exec app whoami      # node
docker compose exec app touch /test # powinno się nie udać (read-only filesystem)
```

## Uwaga o weryfikacji

Konfiguracji **nie uruchamiałem** w Dockerze. Powyższe komendy kontrolne trzeba wykonać u siebie. Przykłady oparte są na standardowych opcjach Dockera i obrazu `node`.
