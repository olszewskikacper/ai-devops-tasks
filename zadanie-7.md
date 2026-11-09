# Zadanie 7: Wygenerowanie prostego skryptu Bash

**Użyty asystent:** Claude (Claude Code)

## Prompt 1

```
Napisz prosty skrypt bash, który sprawdza, czy usługa Docker działa, a jeśli nie - próbuje ją uruchomić.
```

### Skrypt (`check_docker.sh`)

```bash
#!/bin/bash
# Sprawdza, czy usługa Docker działa, a jeśli nie - próbuje ją uruchomić.

if systemctl is-active --quiet docker; then
    echo "Docker działa."
    exit 0
fi

echo "Docker nie działa. Próbuję uruchomić..."
sudo systemctl start docker

if systemctl is-active --quiet docker; then
    echo "Docker został uruchomiony."
    exit 0
else
    echo "Nie udało się uruchomić Dockera." >&2
    exit 1
fi
```

Uruchomienie: `chmod +x check_docker.sh && ./check_docker.sh`

## Prompt 2

```
Wyjaśnij działanie tego skryptu linia po linii, tak jakbyś tłumaczył osobie początkującej.
```

### Wyjaśnienie

| Linia | Wyjaśnienie |
|---|---|
| `#!/bin/bash` | Tzw. shebang. Mówi systemowi, że ten plik ma być uruchomiony przez program Bash. |
| `# Sprawdza, czy...` | Komentarz. Zaczyna się od `#` i jest ignorowany przez komputer, służy tylko człowiekowi. |
| `if systemctl is-active --quiet docker; then` | `systemctl` to narzędzie do zarządzania usługami w Linuxie. `is-active docker` sprawdza, czy usługa Docker działa. `--quiet` oznacza, że nic nie wypisuje, tylko zwraca wynik (sukces lub porażka). `if ... then` wykonuje kolejne linie, jeśli sprawdzenie się powiodło. |
| `echo "Docker działa."` | Wypisuje komunikat na ekranie. |
| `exit 0` | Kończy skrypt. Kod `0` w świecie Linuxa oznacza „wszystko w porządku”. |
| `fi` | Zamyka blok `if` (słowo `if` napisane od tyłu). |
| `echo "Docker nie działa. Próbuję uruchomić..."` | Ta linia wykona się tylko wtedy, gdy Docker nie działał, bo w przeciwnym razie skrypt zakończył się wcześniej przez `exit 0`. |
| `sudo systemctl start docker` | Prosi system o uruchomienie usługi Docker. `sudo` daje uprawnienia administratora, bo zwykły użytkownik nie może uruchamiać usług systemowych. |
| `if systemctl is-active --quiet docker; then` | Drugie sprawdzenie, czy po próbie uruchomienia Docker faktycznie działa. |
| `echo "Docker został uruchomiony."` / `exit 0` | Jeśli się udało, informujemy o tym i kończymy z kodem sukcesu. |
| `else` | „W przeciwnym razie”: ta część wykona się, jeśli Docker nadal nie działa. |
| `echo "Nie udało się uruchomić Dockera." >&2` | Wypisuje komunikat o błędzie. `>&2` kieruje go do strumienia błędów (stderr), a nie zwykłego wyjścia. |
| `exit 1` | Kończy skrypt z kodem `1`, czyli informacją o błędzie. Inne programy lub skrypty mogą to sprawdzić. |
| `fi` | Zamyka drugi blok `if`. |

### Podsumowanie w jednym zdaniu

Skrypt pyta system, czy Docker działa. Jeśli tak, kończy pracę. Jeśli nie, próbuje go uruchomić i sprawdza, czy się udało.

## Uwagi

- Skrypt zakłada system Linux z `systemd`. Na Windows (Docker Desktop) ani w WSL bez systemd nie zadziała.
- Składnię skryptu sprawdziłem poleceniem `bash -n check_docker.sh`. Nie uruchamiałem go, bo wymaga Linuksa z systemd i uprawnień `sudo`.
