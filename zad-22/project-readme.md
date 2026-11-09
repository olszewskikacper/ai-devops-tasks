# Simple Task API

REST API do zarządzania zadaniami, napisane w Node.js z użyciem Express i MongoDB.

## Opis

Simple Task API pozwala tworzyć, odczytywać, aktualizować i usuwać zadania, filtrować je według statusu i priorytetu oraz chronić dostęp prostą autoryzacją użytkowników.

### Funkcje

- Tworzenie, odczytywanie, aktualizacja i usuwanie zadań (CRUD)
- Filtrowanie zadań według statusu i priorytetu
- Prosta autoryzacja użytkowników (rejestracja, logowanie, token JWT)

## Wymagania

- Node.js 18 lub nowszy
- MongoDB 6 lub nowszy (lokalnie lub w chmurze)
- npm

## Instalacja

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/<twoj-uzytkownik>/simple-task-api.git
cd simple-task-api

# 2. Zainstaluj zależności
npm install

# 3. Skonfiguruj zmienne środowiskowe
cp .env.example .env
```

Zawartość pliku `.env`:

```env
PORT=3000
MONGODB_URI=mongodb://localhost:27017/simple-task-api
JWT_SECRET=zmien-na-dlugi-losowy-ciag
```

```bash
# 4. Uruchom aplikację
npm start
```

Serwer będzie dostępny pod adresem `http://localhost:3000`.

Tryb deweloperski z automatycznym przeładowaniem: `npm run dev`.

## Użycie

Wszystkie endpointy zadań wymagają nagłówka `Authorization: Bearer <token>`.

```bash
# Rejestracja
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"jan@example.com","password":"haslo123"}'

# Logowanie (zwraca token)
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"jan@example.com","password":"haslo123"}'

# Utworzenie zadania
curl -X POST http://localhost:3000/api/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Napisać testy","status":"pending","priority":"high"}'

# Lista zadań ze statusem "pending" i wysokim priorytetem
curl "http://localhost:3000/api/tasks?status=pending&priority=high" \
  -H "Authorization: Bearer <token>"
```

## Endpointy API

### Autoryzacja

| Metoda | Endpoint | Opis |
|---|---|---|
| `POST` | `/api/auth/register` | Rejestracja nowego użytkownika |
| `POST` | `/api/auth/login` | Logowanie, zwraca token JWT |

### Zadania

| Metoda | Endpoint | Opis |
|---|---|---|
| `GET` | `/api/tasks` | Lista zadań (obsługuje filtry) |
| `GET` | `/api/tasks/:id` | Szczegóły jednego zadania |
| `POST` | `/api/tasks` | Utworzenie zadania |
| `PUT` | `/api/tasks/:id` | Aktualizacja zadania |
| `DELETE` | `/api/tasks/:id` | Usunięcie zadania |

### Filtrowanie (`GET /api/tasks`)

| Parametr | Wartości | Opis |
|---|---|---|
| `status` | `pending`, `in-progress`, `completed` | Filtr według statusu |
| `priority` | `low`, `medium`, `high` | Filtr według priorytetu |

### Model zadania

```json
{
  "id": "64f1c2e5a1b2c3d4e5f6a7b8",
  "title": "Napisać testy",
  "description": "Testy jednostkowe dla modułu zadań",
  "status": "pending",
  "priority": "high",
  "createdAt": "2025-05-19T10:15:32.000Z"
}
```

### Kody odpowiedzi

| Kod | Znaczenie |
|---|---|
| `200` | Sukces |
| `201` | Zasób utworzony |
| `400` | Nieprawidłowe dane wejściowe |
| `401` | Brak lub nieprawidłowy token |
| `404` | Nie znaleziono zasobu |

## Licencja

MIT
