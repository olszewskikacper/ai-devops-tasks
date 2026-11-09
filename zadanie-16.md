# Zadanie 16: Konwersja Bash do PowerShell

**Użyty asystent:** Claude (Claude Code)

## Prompt

```
Przekonwertuj ten skrypt bash na równoważny skrypt PowerShell dla Windows.
```

## Pliki

- `backup-db.sh`: oryginalny skrypt bash.
- `backup-db.ps1`: wersja PowerShell.

## Skrypt PowerShell (`backup-db.ps1`)

```powershell
# Prosty skrypt do backupu bazy danych (wersja PowerShell dla Windows)

$DbName    = "app_database"
$BackupDir = "C:\Backups\db"
$Date      = Get-Date -Format "yyyyMMdd_HHmmss"
$FileName  = Join-Path $BackupDir "${DbName}_${Date}.sql.gz"
$TempSql   = Join-Path $BackupDir "${DbName}_${Date}.sql"

# Sprawdź czy katalog istnieje
if (-not (Test-Path -Path $BackupDir -PathType Container)) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
    Write-Host "Utworzono katalog $BackupDir"
}

# Wykonaj backup
Write-Host "Rozpoczynam backup bazy $DbName..."
& mysqldump -u root -p --result-file="$TempSql" $DbName

if ($LASTEXITCODE -eq 0) {
    # Kompresja do .gz (Windows nie ma wbudowanego polecenia gzip)
    $inStream  = [System.IO.File]::OpenRead($TempSql)
    $outStream = [System.IO.File]::Create($FileName)
    $gzip      = New-Object System.IO.Compression.GZipStream($outStream, [System.IO.Compression.CompressionMode]::Compress)
    try { $inStream.CopyTo($gzip) }
    finally { $gzip.Dispose(); $outStream.Dispose(); $inStream.Dispose() }
    Remove-Item -Path $TempSql -Force
    Write-Host "Backup zakończony sukcesem: $FileName"
}
else {
    if (Test-Path $TempSql) { Remove-Item -Path $TempSql -Force }
    Write-Host "Błąd podczas wykonywania backupu!"
    exit 1
}
```

(Powyżej wersja skrócona o puste linie i część komentarzy. Pełna wersja jest w pliku `backup-db.ps1`.)

## Główne różnice między bash a PowerShell (na tym przykładzie)

| Zagadnienie | Bash | PowerShell |
|---|---|---|
| Zmienne | `DB_NAME="..."`, odczyt `$DB_NAME` | `$DbName = "..."`, `$` także przy przypisaniu |
| Ścieżki | `/var/backups/db` | `C:\Backups\db` (litery dysków, `\`), składanie przez `Join-Path` |
| Data | `$(date +%Y%m%d_%H%M%S)` | `Get-Date -Format "yyyyMMdd_HHmmss"` (cmdlet zamiast programu `date`) |
| Interpolacja | `${BACKUP_DIR}/${DB_NAME}_${DATE}` | `"${DbName}_${Date}.sql.gz"` (przy `_` po nazwie zmiennej potrzebne `${}`) |
| Warunek na katalog | `[ ! -d "$DIR" ]` | `-not (Test-Path -Path $Dir -PathType Container)` |
| Tworzenie katalogu | `mkdir -p` | `New-Item -ItemType Directory -Force` |
| Wyjście | `echo` | `Write-Host` |
| Kod wyjścia polecenia | `$?` / `$? -eq 0` | `$LASTEXITCODE` dla programów zewnętrznych |
| Potoki | Przesyłają **tekst/bajty** | Przesyłają **obiekty** .NET |
| Przekierowanie `>` | Zapisuje bajty bez zmian | Przekodowuje tekst (w PS 5.1 do UTF-16), co **psuje dane binarne i dumpy** |
| Kompresja | `gzip` | Brak wbudowanego `gzip`, użyto klasy .NET `GZipStream` |
| Operatory porównania | `-eq` w `[ ]` | `-eq`, `-ne`, `-not` (zamiast `==`, `!`) |

## Wnioski

1. **Konwersja nie jest dosłowna.** Potok `mysqldump | gzip > plik` nie przenosi się 1:1. W PowerShellu `>` zmienia kodowanie, więc użyłem `--result-file` w `mysqldump` i osobnej kompresji.
2. **Nie ma `gzip` na Windows,** dlatego skorzystałem z .NET (`System.IO.Compression.GZipStream`). Alternatywą jest zainstalowanie 7-Zip lub użycie `tar`.
3. **Plik z polskimi znakami wymaga BOM.** Windows PowerShell 5.1 czyta plik `.ps1` bez BOM jako ANSI. Za pierwszym razem polskie znaki zepsuły cudzysłowy i skrypt się nie parsował (`The string is missing the terminator`). Plik zapisałem jako **UTF-8 z BOM**. W PowerShell 7+ ten problem nie występuje.
4. **Różnica filozofii:** bash operuje na tekście i małych programach, a PowerShell na obiektach i cmdletach `Czasownik-Rzeczownik`.
5. **Domyślna ścieżka:** katalog `/var/backups/db` nie ma odpowiednika w Windows, więc przyjąłem `C:\Backups\db`. To założenie, które trzeba dostosować.

## Weryfikacja

- `bash -n backup-db.sh`: składnia poprawna.
- Parser PowerShell (`[Parser]::ParseFile`): `PARSE OK` (po dodaniu BOM).
- Osobno sprawdziłem fragment z kompresją `GZipStream` na pliku testowym z polskimi znakami: plik `.gz` powstał poprawnie.
- **Nie uruchamiałem** skryptów z prawdziwym `mysqldump`, bo nie mam skonfigurowanego serwera MySQL.
- Skrypt prosi o hasło interaktywnie (`-p`), tak jak oryginał.
