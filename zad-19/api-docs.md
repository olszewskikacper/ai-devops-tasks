# GET /api/users

Zwraca stronicowaną listę użytkowników, z opcjonalnym filtrem według roli.

## Parametry zapytania

| Parametr | Typ | Wymagany | Domyślnie | Opis |
|---|---|---|---|---|
| `page` | integer | nie | `1` | Numer strony (liczony od 1). |
| `limit` | integer | nie | `10` | Liczba wyników na stronę. Wartość od 1 do 100. |
| `role` | string | nie | brak | Zwraca tylko użytkowników o podanej roli (np. `admin`, `user`). |

## Przykładowe żądanie

```http
GET /api/users?page=2&limit=5&role=admin HTTP/1.1
Host: api.example.com
Accept: application/json
```

```bash
curl "https://api.example.com/api/users?page=2&limit=5&role=admin"
```

## Przykładowa odpowiedź

**Status:** `200 OK`

```json
{
  "data": [
    { "id": 6, "name": "Jan Kowalski", "email": "jan@example.com", "role": "admin" },
    { "id": 7, "name": "Anna Nowak", "email": "anna@example.com", "role": "admin" }
  ],
  "pagination": {
    "page": 2,
    "limit": 5,
    "total": 7,
    "totalPages": 2
  }
}
```

## Pola odpowiedzi

| Pole | Typ | Opis |
|---|---|---|
| `data` | array | Lista użytkowników na bieżącej stronie. Pusta tablica, jeśli nic nie pasuje. |
| `data[].id` | integer | Unikalny identyfikator użytkownika. |
| `data[].name` | string | Imię i nazwisko. |
| `data[].email` | string | Adres e-mail. |
| `data[].role` | string | Rola użytkownika. |
| `pagination.page` | integer | Bieżąca strona. |
| `pagination.limit` | integer | Rozmiar strony. |
| `pagination.total` | integer | Łączna liczba pasujących użytkowników. |
| `pagination.totalPages` | integer | Łączna liczba stron. |

## Kody odpowiedzi

| Kod | Znaczenie |
|---|---|
| `200 OK` | Sukces. |
| `400 Bad Request` | Nieprawidłowy parametr (np. `page=0`, `limit=500`, wartość nienumeryczna). |

> **Założenia:** w opisie endpointu nie podano struktury odpowiedzi, kodów błędów ani uwierzytelniania. Pola użytkownika (`id`, `name`, `email`, `role`), obiekt `pagination` oraz zwracanie `400` dla `limit` powyżej 100 (zamiast przycinania do 100) to moje założenia, które trzeba uzgodnić z rzeczywistą implementacją.
