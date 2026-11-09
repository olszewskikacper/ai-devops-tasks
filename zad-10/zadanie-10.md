# Zadanie 10: Generowanie prostego pliku .gitignore

**Użyty asystent:** Claude (Claude Code)

## Prompt 1

```
Stwórz plik .gitignore dla projektu Node.js, który używa Docker i przechowuje dane w lokalnej bazie MongoDB.
```

### Wygenerowany `.gitignore`

```gitignore
# Zależności Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# Zmienne środowiskowe i sekrety
.env
.env.*
!.env.example

# Dane lokalnej bazy MongoDB
data/
db/
mongo-data/
mongodb-data/
*.wt
*.lock
mongod.lock
*.bson

# Docker
docker-compose.override.yml
.docker/
*.pid

# Logi
logs/
*.log

# Build i cache
dist/
build/
coverage/
.cache/
.nyc_output/
*.tsbuildinfo

# Pliki systemowe
.DS_Store
Thumbs.db

# Edytory i IDE
.vscode/
.idea/
*.swp
*.swo
```

Plik zapisano jako `.gitignore` w repozytorium.

**Uwaga:** wzorzec `*.lock` jest szeroki i zignoruje także `yarn.lock`, `Cargo.lock` itp. W projekcie Node.js plik `yarn.lock` lub `package-lock.json` zwykle **powinien** być w repozytorium, więc przy użyciu Yarna trzeba tę linię usunąć albo zawęzić do `mongod.lock`.

## Prompt 2

```
Dlaczego ważne jest ignorowanie tych plików?
```

### Wyjaśnienie

| Pliki | Dlaczego ignorować |
|---|---|
| `node_modules/` | Ogromny katalog (setki MB), w pełni odtwarzalny poleceniem `npm install` na podstawie `package.json` i `package-lock.json`. Wersjonowanie go zaśmieca repozytorium i spowalnia operacje. |
| `.env`, `.env.*` | Zawierają **sekrety**: hasła, klucze API, dane dostępowe do bazy. Po wypchnięciu do repozytorium (zwłaszcza publicznego) wyciekają, a usunięcie ich z historii Gita jest trudne. Zamiast tego commituje się `.env.example` bez prawdziwych wartości. |
| Dane MongoDB (`data/`, `*.wt`, `*.bson`) | To binarne pliki danych lokalnej bazy. Są duże, zmieniają się przy każdym uruchomieniu, mogą zawierać prawdziwe dane (w tym osobowe) i powodują konflikty. Dane nie są kodem źródłowym. |
| `docker-compose.override.yml`, `.docker/` | Lokalne ustawienia dewelopera (porty, wolumeny), różne na każdej maszynie. |
| Logi (`*.log`, `logs/`) | Generowane automatycznie, rosną w nieskończoność, mogą zawierać wrażliwe informacje. |
| `dist/`, `build/`, `coverage/` | Artefakty generowane z kodu źródłowego. Można je zawsze odtworzyć, a ich commitowanie powoduje zbędne konflikty. |
| `.DS_Store`, `.vscode/`, `.idea/` | Pliki specyficzne dla systemu lub edytora konkretnej osoby, nieistotne dla reszty zespołu. |

### Najważniejsze powody

1. **Bezpieczeństwo:** sekrety i dane nie mogą trafić do repozytorium.
2. **Czystość i wydajność:** repozytorium zawiera tylko kod źródłowy, bez plików generowanych, więc jest małe i szybkie.
3. **Mniej konfliktów:** pliki lokalne i generowane inaczej wyglądają u każdego członka zespołu.
4. **Powtarzalność:** wszystko, co da się odtworzyć (zależności, build), odtwarza się poleceniami, a nie z historii Gita.

**Pamiętaj:** `.gitignore` działa tylko dla plików jeszcze nieśledzonych. Jeśli plik został już zacommitowany, trzeba go usunąć z indeksu: `git rm --cached <plik>`.
