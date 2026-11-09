# Zadanie 8: Analiza krótkiego błędu

**Użyty asystent:** Claude (Claude Code)

## Komunikat błędu

```
ERROR: for app  Cannot start service app: driver failed programming external connectivity on endpoint app (172.18.0.2): Error starting userland proxy: listen tcp4 0.0.0.0:3000: bind: address already in use
```

## Pytanie

```
Co oznacza ten błąd i jak mogę go rozwiązać?
```

## Wyjaśnienie

Docker próbuje opublikować port kontenera (mapowanie `3000:3000`) na porcie 3000 hosta. Nie może tego zrobić, bo **inny proces już nasłuchuje na porcie 3000** (`address already in use`). Dwa procesy nie mogą jednocześnie używać tego samego adresu i portu.

Fragmenty komunikatu:
- `Cannot start service app` – nie udało się uruchomić usługi `app` (zwykle z `docker-compose.yml`).
- `172.18.0.2` – adres kontenera w sieci Dockera.
- `listen tcp4 0.0.0.0:3000` – Docker chciał nasłuchiwać na wszystkich interfejsach IPv4 na porcie 3000.
- `bind: address already in use` – właściwa przyczyna, port jest zajęty.

Typowe przyczyny:
1. Inny kontener używa już portu 3000 (np. stary kontener, który nie został zatrzymany).
2. Aplikacja uruchomiona lokalnie (np. `npm start`) zajmuje port.
3. Inna usługa na hoście korzysta z tego portu.

## Rozwiązania

### 1. Znajdź, co zajmuje port

Linux/macOS:
```bash
sudo lsof -i :3000
# lub
sudo ss -tulpn | grep :3000
```

Windows (PowerShell):
```powershell
netstat -ano | findstr :3000
Get-Process -Id <PID>
```

### 2. Sprawdź kontenery Dockera

```bash
docker ps --filter "publish=3000"
docker stop <id_kontenera>
# lub zatrzymaj cały stack
docker compose down
```

### 3. Zatrzymaj proces zajmujący port

```bash
kill <PID>                      # Linux/macOS
Stop-Process -Id <PID>          # Windows PowerShell
```

### 4. Zmień port po stronie hosta

W `docker-compose.yml` zmień mapowanie, np. na 3001 (port wewnątrz kontenera zostaje bez zmian):

```yaml
services:
  app:
    ports:
      - "3001:3000"
```

Dla `docker run`: `docker run -p 3001:3000 moj-obraz`

### 5. Uruchom ponownie

```bash
docker compose up
```

## Wnioski

- Błąd dotyczy hosta, a nie samej aplikacji w kontenerze. Przyczyną jest kolizja portów.
- Najpierw należy ustalić, co zajmuje port, zanim cokolwiek się zatrzyma (to może być ważny proces).
- Najbezpieczniejszym rozwiązaniem, gdy nie chcemy niczego zatrzymywać, jest zmiana portu hosta w mapowaniu.
