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

# mysqldump zapisuje bezpośrednio do pliku (--result-file), bo przekierowanie
# ">" w PowerShellu mogłoby zmienić kodowanie danych.
& mysqldump -u root -p --result-file="$TempSql" $DbName

if ($LASTEXITCODE -eq 0) {
    # Kompresja do .gz (Windows nie ma wbudowanego polecenia gzip)
    $inStream  = [System.IO.File]::OpenRead($TempSql)
    $outStream = [System.IO.File]::Create($FileName)
    $gzip      = New-Object System.IO.Compression.GZipStream($outStream, [System.IO.Compression.CompressionMode]::Compress)
    try {
        $inStream.CopyTo($gzip)
    }
    finally {
        $gzip.Dispose()
        $outStream.Dispose()
        $inStream.Dispose()
    }
    Remove-Item -Path $TempSql -Force
    Write-Host "Backup zakończony sukcesem: $FileName"
}
else {
    if (Test-Path $TempSql) { Remove-Item -Path $TempSql -Force }
    Write-Host "Błąd podczas wykonywania backupu!"
    exit 1
}
