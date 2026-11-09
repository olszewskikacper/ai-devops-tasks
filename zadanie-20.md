# Zadanie 20: Generowanie wyrażeń regularnych

**Użyty asystent:** Claude (Claude Code)

## Prompt 1

```
Potrzebuję wyrażenia regularnego, które waliduje format adresu IPv4 (np. 192.168.1.1).
```

### Wyrażenie regularne

```regex
^(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$
```

## Prompt 2

```
Wyjaśnij, jak działa to wyrażenie regularne i przetestuj je na kilku przykładach (poprawnych i niepoprawnych).
```

### Wyjaśnienie

Adres IPv4 to cztery liczby od 0 do 255 oddzielone kropkami. Wyrażenie najpierw opisuje jedną liczbę (oktet), a potem powtarza ją cztery razy.

**Oktet** `(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)` to jedna z czterech możliwości:

| Fragment | Dopasowuje | Zakres |
|---|---|---|
| `25[0-5]` | 250 do 255 | |
| `2[0-4]\d` | 200 do 249 | |
| `1\d\d` | 100 do 199 | |
| `[1-9]?\d` | jedna lub dwie cyfry, bez zera wiodącego | 0 do 99 |

**Całość:**

| Część | Znaczenie |
|---|---|
| `^` i `$` | Początek i koniec napisu. Cały tekst musi być adresem, a nie tylko jego fragmentem. |
| `(?:oktet\.){3}` | Trzy oktety, każdy z kropką na końcu. |
| `oktet` na końcu | Czwarty oktet, bez kropki. |
| `(?:...)` | Grupa nieprzechwytująca (nie zapamiętuje dopasowania). |

Wyrażenie **odrzuca zera wiodące** (np. `192.168.01.1`), bo w niektórych systemach liczba z zerem wiodącym bywa interpretowana jako ósemkowa. Jeśli takie adresy mają być dozwolone, zamiast `[1-9]?\d` trzeba użyć `\d{1,2}`.

### Funkcja (`ipv4-validator.js`)

```javascript
const OCTET = '(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)';
const IPV4_REGEX = new RegExp(`^(?:${OCTET}\\.){3}${OCTET}$`);

function isValidIPv4(ip) {
  return typeof ip === 'string' && IPV4_REGEX.test(ip);
}

module.exports = isValidIPv4;
```

Wyrażenie jest zbudowane z osobnego fragmentu `OCTET`, żeby uniknąć powtarzania długiego wzorca. Sprawdzenie `typeof ip === 'string'` chroni przed wartościami innymi niż tekst.

## Przykłady testów

Wszystkie poniższe przypadki uruchomiłem w Node.js i wyniki zgadzały się z oczekiwaniem.

**Poprawne (`true`):**

| Adres | Uwaga |
|---|---|
| `192.168.1.1` | typowy adres prywatny |
| `0.0.0.0` | wartości graniczne (minimum) |
| `255.255.255.255` | wartości graniczne (maksimum) |
| `10.0.0.1` | |
| `8.8.8.8` | |
| `127.0.0.1` | loopback |

**Niepoprawne (`false`):**

| Adres | Powód |
|---|---|
| `256.1.1.1` | oktet powyżej 255 |
| `999.999.999.999` | oktety powyżej 255 |
| `192.168.1` | tylko trzy oktety |
| `192.168.1.1.1` | pięć oktetów |
| `192.168.01.1` | zero wiodące |
| `abc.def.ghi.jkl` | nie są liczbami |
| `1.2.3.` | pusty czwarty oktet |
| `.1.2.3` | pusty pierwszy oktet |
| `1..2.3` | pusty oktet w środku |
| `192.168.1.-1` | liczba ujemna |
| `192.168.1.1 ` (spacja na końcu) | spacja przed końcem napisu |
| ` 1.2.3.4` (spacja na początku) | spacja na początku |
| `1.2.3.4\n` (znak nowej linii) | znak nowej linii na końcu |
| pusty napis | brak danych |
| `null`, `undefined`, `1234` | nie są napisami |

## Uwagi i ograniczenia

- Wyrażenie sprawdza **format**, a nie to, czy adres istnieje lub jest przydzielony (np. nie rozróżnia adresów prywatnych i publicznych).
- Nie obsługuje IPv6 ani notacji CIDR (`192.168.1.0/24`).
- Ostrożnie z `$` w innych językach: w niektórych (np. Python `re.match` z `$`) znak nowej linii na końcu bywa akceptowany. W JavaScript bez flagi `m` `$` oznacza dokładny koniec napisu, co potwierdził test z `\n`.
