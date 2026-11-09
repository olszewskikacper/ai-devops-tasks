# Zadanie 21: Transformacja danych

**Użyty asystent:** Claude (Claude Code)

## Prompt

```
Przekształć te dane JSON do formatu CSV z kolumnami: id, name, email, roles.
```

## Pliki

- `users.json`: oryginalne dane JSON.
- `users.csv`: wynik konwersji.

## Wynik (`users.csv`)

```csv
id,name,email,roles
1,Jan Kowalski,jan@example.com,admin;user
2,Anna Nowak,anna@example.com,user
```

## Opis procesu konwersji

1. **Nagłówek:** pierwsza linia zawiera nazwy kolumn: `id,name,email,roles`.
2. **Jeden użytkownik to jeden wiersz.** Tablica `users` jest przetwarzana element po elemencie.
3. **Pola proste** (`id`, `name`, `email`) są przepisywane bez zmian.
4. **Pole `roles` jest tablicą,** której CSV nie obsługuje natywnie, więc elementy łączę w jeden napis, rozdzielając je średnikiem: `["admin", "user"]` → `admin;user`.
5. Separatorem pól jest przecinek.

## Potencjalne wyzwania

### Reprezentacja tablicy `roles`

CSV jest formatem płaskim (tabela), a JSON może zawierać zagnieżdżone struktury. Są trzy główne podejścia:

| Podejście | Przykład | Zalety | Wady |
|---|---|---|---|
| **Łączenie separatorem** (użyte tutaj) | `admin;user` | Prosty plik, jeden wiersz na użytkownika | Separator nie może występować w wartościach. Odczyt wymaga rozdzielenia napisu. |
| **Jedna kolumna na rolę** | `role_1,role_2` | Łatwe filtrowanie | Nieznana liczba kolumn, wiele pustych pól |
| **Osobny wiersz dla każdej roli** | `1,Jan,...,admin` i `1,Jan,...,user` | Dane znormalizowane | Powielenie `id`, `name`, `email`. Wiersze nie odpowiadają już użytkownikom. |
| **JSON w komórce** | `"[""admin"",""user""]"` | Bez utraty informacji | Mało czytelne, wymaga podwójnego cudzysłowu |

Wybrałem separator średnikowy, bo jest najprostszy i najczęstszy dla list krótkich wartości.

### Inne problemy

1. **Znaki specjalne w danych.** Jeśli pole zawiera przecinek, cudzysłów lub nową linię (np. `Kowalski, Jan`), musi być ujęte w cudzysłowy, a cudzysłowy wewnątrz podwojone (`"` → `""`). W naszych danych tego nie ma, więc cudzysłowy pominąłem. Przy ogólnej konwersji trzeba to robić zawsze.
2. **Kodowanie znaków.** Polskie znaki wymagają UTF-8. Excel często potrzebuje znaku BOM, żeby je poprawnie wyświetlić.
3. **Separator zależny od ustawień regionalnych.** W polskim Excelu domyślnym separatorem bywa średnik, nie przecinek, co koliduje z użyciem średnika wewnątrz pola `roles`.
4. **Typy danych.** CSV nie rozróżnia liczb i tekstu. `id` to po otwarciu pliku zwykły napis, a wartości typu `0123` mogą stracić zero wiodące.
5. **Brakujące i dodatkowe pola.** Jeśli jakiś użytkownik nie ma pola `email` lub ma dodatkowe pole, kolumny trzeba ustalić z góry, a braki wypełnić pustą wartością.
6. **Konwersja odwrotna.** Przejście z CSV z powrotem do JSON wymaga znajomości, że `roles` to lista, i rozdzielenia jej po średniku.
7. **Bezpieczeństwo (CSV injection).** Komórki zaczynające się od `=`, `+`, `-`, `@` mogą być wykonane jako formuły w arkuszu. Przy danych od użytkowników warto je zabezpieczyć.

## Weryfikacja

Napisałem w Node.js krótki skrypt, który generuje CSV z `users.json` (łącząc `roles` średnikiem), i porównałem wynik z plikiem `users.csv`. Pliki były identyczne.
