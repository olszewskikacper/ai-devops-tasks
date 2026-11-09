# Zadanie 9: Weryfikacja prostego YAML

**Użyty asystent:** Claude (Claude Code)

## Prompt

```
Czy ten plik YAML jest poprawny? Jeśli nie, popraw błędy.
```

## Oryginalny plik

```yaml
services:
  web:
    image: nginx
    ports:
      - "80:80"
  app:
    build: .
    ports
      - "3000:3000"
    depends_on:
      - db
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD=password
```

## Znalezione błędy

Plik **nie jest poprawny**. Znalazłem dwa błędy.

1. **Brak dwukropka po `ports` w usłudze `app`** (`ports` zamiast `ports:`). To błąd składni YAML: parser nie rozpozna klucza i zgłosi błąd parsowania.
2. **Zła notacja zmiennej środowiskowej w usłudze `db`.** Linia `POSTGRES_PASSWORD=password` pod `environment:` to zwykły ciąg znaków, a nie para klucz-wartość. Docker Compose wymaga tu mapy (`KLUCZ: wartość`) albo listy (`- KLUCZ=wartość`). Ten zapis nie przejdzie walidacji Compose (`environment must be a mapping or a list`).

## Poprawiona wersja

```yaml
services:
  web:
    image: nginx
    ports:
      - "80:80"
  app:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - db
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: password
```

Alternatywny poprawny zapis zmiennej środowiskowej (lista):

```yaml
    environment:
      - POSTGRES_PASSWORD=password
```

## Uwagi

- Nie przeprowadziłem automatycznej walidacji narzędziem (brak modułu PyYAML w środowisku), więc analiza jest ręczna. Plik można sprawdzić poleceniem `docker compose config`.
- Hasło `password` w pliku jest dopuszczalne tylko w przykładzie. W prawdziwym projekcie trzeba użyć pliku `.env` albo sekretów (`secrets`).
- Dobrą praktyką jest dodanie `restart: unless-stopped` oraz przypięcie wersji obrazów (np. `postgres:16` zamiast `postgres`).
