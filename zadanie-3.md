# Zadanie 3: Podstawowe formatowanie promptu

**Użyty asystent:** Claude (Claude Code)

## Prompt 1: niestrukturyzowany

```
dockerfile node
```

### Odpowiedź

Zakładam, że chodzi o przykładowy Dockerfile dla aplikacji Node.js. Poniżej typowy wariant:

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
EXPOSE 3000
CMD ["node", "index.js"]
```

Prompt jest niejednoznaczny, więc musiałem zgadnąć wersję Node, port, punkt wejścia i sposób instalacji zależności. Jeśli masz inne wymagania, napisz je, a dopasuję plik.

## Prompt 2: strukturyzowany

```
Napisz prosty Dockerfile dla aplikacji Node.js, który:
- używa Node 18 jako obrazu bazowego
- kopiuje pliki package.json i package-lock.json
- instaluje zależności
- kopiuje resztę plików aplikacji
- wystawia port 3000
- uruchamia aplikację poleceniem "npm start"
```

### Odpowiedź

```dockerfile
# Obraz bazowy: Node 18
FROM node:18

# Katalog roboczy w kontenerze
WORKDIR /app

# Kopiowanie package.json i package-lock.json
COPY package.json package-lock.json ./

# Instalacja zależności
RUN npm install

# Kopiowanie reszty plików aplikacji
COPY . .

# Wystawienie portu 3000
EXPOSE 3000

# Uruchomienie aplikacji
CMD ["npm", "start"]
```

Każdy punkt z promptu ma odpowiadającą mu instrukcję w pliku. Kolejność kopiowania (najpierw pliki z zależnościami, potem reszta) pozwala Dockerowi cache'ować warstwę z `npm install`, jeśli zależności się nie zmieniły.

## Porównanie i wnioski

| Aspekt | Prompt 1 | Prompt 2 |
|---|---|---|
| Wersja Node | Zgadnięta (20-alpine) | Zgodna z żądaniem (18) |
| Pliki zależności | `package*.json` (skrót) | Wprost `package.json` i `package-lock.json` |
| Polecenie startowe | Zgadnięte (`node index.js`) | `npm start` zgodnie z promptem |
| Dodatkowe założenia | Alpine, `npm ci --omit=dev` | Brak, tylko to, o co poproszono |
| Potrzeba poprawek | Duża, trzeba by dopytać o szczegóły | Mała, plik gotowy do użycia |

**Wnioski:**
- Krótki prompt zmusza model do zgadywania. Wynik jest poprawny technicznie, ale może nie pasować do projektu.
- Prompt z listą wymagań daje przewidywalny, powtarzalny wynik zgodny z oczekiwaniami i oszczędza kolejne iteracje.
- Dobry prompt określa cel, konkretne wymagania (wersje, porty, polecenia) i najlepiej format odpowiedzi.
- Lista punktowana dobrze sprawdza się też jako checklista do weryfikacji, czy odpowiedź spełnia wszystkie warunki.
