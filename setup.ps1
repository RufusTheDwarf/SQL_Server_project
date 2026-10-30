[CmdletBinding()]
param(
    [string]$SqlServer = ".\SQLEXPRESS",
    [ValidateRange(1, 65535)]
    [int]$Port = 5000,
    [switch]$SkipIntegrationTests
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Join-Path $PSScriptRoot "version-finale\mission-sql-cinema"
$DatabaseName = "MissionCinema"
$RequiredDriver = "ODBC Driver 18 for SQL Server"
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$AppUrl = "http://127.0.0.1:$Port"

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor White
}

function Invoke-Sql {
    param(
        [string]$Query,
        [string]$Database = "master"
    )

    $arguments = @(
        "-S", $SqlServer,
        "-E",
        "-b",
        "-r", "1",
        "-h", "-1",
        "-W",
        "-C",
        "-d", $Database,
        "-Q", $Query
    )

    $output = & $script:SqlCmdPath @arguments 2>&1
    $exitCode = $LASTEXITCODE
    $text = ($output | Out-String).Trim()

    if ($exitCode -ne 0) {
        throw "sqlcmd a retourne le code $exitCode. $text"
    }

    return $text
}

function Invoke-SqlFile {
    param(
        [string]$Path,
        [string]$Database = $DatabaseName
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Fichier SQL introuvable : $Path"
    }

    Write-Host "Execution : $Path"
    $arguments = @(
        "-S", $SqlServer,
        "-E",
        "-b",
        "-r", "1",
        "-C",
        "-d", $Database,
        "-i", $Path
    )

    & $script:SqlCmdPath @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Echec de l'execution SQL : $Path (code $LASTEXITCODE)."
    }
}

function Invoke-Python {
    param([string[]]$PythonArguments)

    & $script:VenvPython @PythonArguments
    if ($LASTEXITCODE -ne 0) {
        throw "La commande Python a echoue : $($PythonArguments -join ' ')"
    }
}

try {
    Write-Step "Verification du dossier du projet"
    if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) {
        throw "Dossier du projet introuvable. Lance setup.ps1 depuis la racine du depot SQL_Server_project."
    }

    $requiredFiles = @(
        "app.py",
        "requirements.txt",
        "sql\00_create_database.sql",
        "sql\01_schema.sql",
        "sql\02_generate_reservations.sql",
        "sql\03_verify_volume.sql",
        "tests\test_app.py"
    )
    foreach ($relativePath in $requiredFiles) {
        if (-not (Test-Path -LiteralPath (Join-Path $ProjectRoot $relativePath) -PathType Leaf)) {
            throw "Fichier requis introuvable : $relativePath"
        }
    }

    Write-Step "Verification du port local"
    $listener = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($null -ne $listener) {
        throw "Le port $Port est deja utilise. Ferme l'application qui l'utilise ou relance avec -Port 5001."
    }

    Write-Step "Verification de SQL Server et de sqlcmd"
    $sqlcmd = Get-Command "sqlcmd.exe" -CommandType Application -ErrorAction SilentlyContinue
    if ($null -eq $sqlcmd) {
        $sqlcmd = Get-Command "sqlcmd" -CommandType Application -ErrorAction SilentlyContinue
    }
    if ($null -eq $sqlcmd) {
        throw "sqlcmd est introuvable. Installe les outils en ligne de commande SQL Server, puis rouvre PowerShell. Le moteur SQL Server doit aussi etre installe."
    }
    $script:SqlCmdPath = $sqlcmd.Source

    $probe = Invoke-Sql -Query "SET NOCOUNT ON; SELECT 1;" -Database "master"
    if ($probe -notmatch "(?m)^\s*1\s*$") {
        throw "La connexion a SQL Server n'a pas renvoye le resultat attendu. Verifie le nom de l'instance avec -SqlServer."
    }
    Write-Host "Connexion SQL Server OK : $SqlServer"

    Write-Step "Verification de Python"
    $pythonLauncher = Get-Command "py.exe" -CommandType Application -ErrorAction SilentlyContinue
    if ($null -ne $pythonLauncher) {
        $pythonBase = $pythonLauncher.Source
        $pythonArgs = @("-3")
    } else {
        $pythonCommand = Get-Command "python.exe" -CommandType Application -ErrorAction SilentlyContinue
        if ($null -eq $pythonCommand) {
            throw "Python est introuvable. Installe Python 3.10 ou plus recent, puis relance setup.ps1."
        }
        $pythonBase = $pythonCommand.Source
        $pythonArgs = @()
    }

    $pythonVersion = & $pythonBase @pythonArgs -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    if ($LASTEXITCODE -ne 0) {
        throw "Impossible de lancer Python."
    }
    $versionParts = $pythonVersion.Trim().Split(".")
    $major = [int]$versionParts[0]
    $minor = [int]$versionParts[1]
    if (($major -lt 3) -or ($major -eq 3 -and $minor -lt 10)) {
        throw "Python 3.10 ou plus recent est necessaire. Version detectee : $pythonVersion"
    }
    Write-Host "Python $pythonVersion"

    Write-Step "Creation de l'environnement et installation des dependances"
    if (-not (Test-Path -LiteralPath $VenvPython -PathType Leaf)) {
        & $pythonBase @pythonArgs -m venv (Join-Path $ProjectRoot ".venv")
        if ($LASTEXITCODE -ne 0) {
            throw "La creation de l'environnement virtuel a echoue."
        }
    }
    Invoke-Python -PythonArguments @("-m", "pip", "install", "--upgrade", "pip")
    Invoke-Python -PythonArguments @("-m", "pip", "install", "-r", (Join-Path $ProjectRoot "requirements.txt"))

    $installedDrivers = & $VenvPython -c "import pyodbc; print('\n'.join(pyodbc.drivers()))"
    if ($LASTEXITCODE -ne 0) {
        throw "Impossible de lire les pilotes ODBC installes."
    }
    if ($installedDrivers -notmatch [regex]::Escape($RequiredDriver)) {
        throw "Le pilote '$RequiredDriver' est introuvable. Installe Microsoft ODBC Driver 18 for SQL Server, puis relance setup.ps1."
    }


    Write-Step "Creation ou verification de la base"
    $databaseExists = Invoke-Sql -Query "SET NOCOUNT ON; SELECT CASE WHEN DB_ID(N'MissionCinema') IS NULL THEN 0 ELSE 1 END;" -Database "master"
    if ($databaseExists -notmatch "(?m)^\s*1\s*$") {
        Invoke-SqlFile -Path (Join-Path $ProjectRoot "sql\00_create_database.sql") -Database "master"
    } else {
        Write-Host "La base MissionCinema existe deja. Aucune base ne sera supprimee."
    }

    Write-Step "Verification du schema"
    $schemaState = Invoke-Sql -Database $DatabaseName -Query @"
SET NOCOUNT ON;
DECLARE @Expected INT = (
    SELECT COUNT(*)
    FROM sys.tables
    WHERE schema_id = SCHEMA_ID(N'dbo')
      AND name IN (N'Films', N'Cinemas', N'Clients', N'Seances', N'Reservations')
);
DECLARE @AnyTable INT = (
    SELECT COUNT(*)
    FROM sys.tables
    WHERE schema_id = SCHEMA_ID(N'dbo')
);
SELECT CASE
    WHEN @Expected = 5 THEN 'READY'
    WHEN @Expected = 0 AND @AnyTable = 0 THEN 'EMPTY'
    ELSE 'PARTIAL'
END;
"@

    if ($schemaState -match "(?m)^\s*EMPTY\s*$") {
        Invoke-SqlFile -Path (Join-Path $ProjectRoot "sql\01_schema.sql")
    } elseif ($schemaState -match "(?m)^\s*READY\s*$") {
        Write-Host "Le schema attendu existe deja. Il est conserve."
    } else {
        throw "Le schema dbo est partiel ou contient des tables inattendues. Le setup s'arrete sans supprimer ni modifier les tables existantes. Fais verifier la base MissionCinema."
    }

    Write-Step "Verification des droits de lecture SQL"
    $selectPermission = Invoke-Sql -Database $DatabaseName -Query "SET NOCOUNT ON; SELECT CASE WHEN HAS_PERMS_BY_NAME(N'dbo.Reservations', N'OBJECT', N'SELECT') = 1 THEN 1 ELSE 0 END;"
    if ($selectPermission -notmatch "(?m)^\s*1\s*$") {
        throw "Le compte Windows courant n'a pas le droit SELECT sur dbo.Reservations. Un administrateur doit executer sql\04_role_lecture.sql et ajouter le compte Windows au role mission_cinema_lecture."
    }

    Write-Step "Generation ou reprise des 10 millions de reservations"
    Invoke-SqlFile -Path (Join-Path $ProjectRoot "sql\02_generate_reservations.sql")

    Write-Step "Verification des volumes et des relations"
    Invoke-SqlFile -Path (Join-Path $ProjectRoot "sql\03_verify_volume.sql")

    $dataCheck = Invoke-Sql -Database $DatabaseName -Query @"
SET NOCOUNT ON;
SET DATEFIRST 7;
DECLARE @Reservations BIGINT = (SELECT COUNT_BIG(*) FROM dbo.Reservations);
DECLARE @Orphans BIGINT = (
    SELECT COUNT_BIG(*)
    FROM dbo.Reservations AS r
    LEFT JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
    LEFT JOIN dbo.Clients AS c ON c.client_id = r.client_id
    WHERE s.seance_id IS NULL OR c.client_id IS NULL
);
DECLARE @TopGenre NVARCHAR(30) = (
    SELECT TOP (1) f.genre
    FROM dbo.Reservations AS r
    INNER JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
    INNER JOIN dbo.Films AS f ON f.film_id = s.film_id
    GROUP BY f.genre
    ORDER BY COUNT_BIG(*) DESC, f.genre
);
DECLARE @TopCinema NVARCHAR(80) = (
    SELECT TOP (1) c.nom
    FROM dbo.Reservations AS r
    INNER JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
    INNER JOIN dbo.Cinemas AS c ON c.cinema_id = s.cinema_id
    GROUP BY c.nom, c.cinema_id
    ORDER BY COUNT_BIG(*) DESC, c.nom
);
DECLARE @TopDay INT = (
    SELECT TOP (1) DATEPART(WEEKDAY, date_reservation)
    FROM dbo.Reservations
    GROUP BY DATEPART(WEEKDAY, date_reservation)
    ORDER BY COUNT_BIG(*) DESC, DATEPART(WEEKDAY, date_reservation)
);
SELECT CASE
    WHEN @Reservations >= 10000000
     AND @Orphans = 0
     AND @TopGenre = N'Science-fiction'
     AND @TopCinema = N'Cinéma du Centre'
     AND @TopDay = 7
    THEN 1 ELSE 0
END;
"@
    if ($dataCheck -notmatch "(?m)^\s*1\s*$") {
        throw "Les donnees ne passent pas le controle final (volume, relations ou reponses attendues). Lis les resultats de sql/03_verify_volume.sql."
    }
    Write-Host "Controle SQL : au moins 10 000 000 reservations, aucune relation orpheline et trois gagnants distincts."

    Write-Step "Tests applicatifs"
    Invoke-Python -PythonArguments @("-m", "unittest", "discover", "-s", (Join-Path $ProjectRoot "tests"), "-p", "test_app.py", "-v")

    if (-not $SkipIntegrationTests) {
        Write-Step "Tests d'integration avec SQL Server"
        $env:RUN_SQL_INTEGRATION = "1"
        try {
            Invoke-Python -PythonArguments @("-m", "unittest", "discover", "-s", (Join-Path $ProjectRoot "tests"), "-p", "test_sql_integration.py", "-v")
        } finally {
            Remove-Item Env:RUN_SQL_INTEGRATION -ErrorAction SilentlyContinue
        }
    } else {
        Write-Host "Tests d'integration ignores a la demande."
    }

    Write-Step "Demarrage de Mission SQL Cinema"
    Remove-Item Env:DEMO_MODE -ErrorAction SilentlyContinue
    $env:SQL_SERVER = $SqlServer
    $env:SQL_DATABASE = $DatabaseName
    $env:SQL_DRIVER = $RequiredDriver
    $env:APP_PORT = [string]$Port

    if (-not $env:FLASK_SECRET_KEY) {
        $env:FLASK_SECRET_KEY = (& $VenvPython -c "import secrets; print(secrets.token_urlsafe(48))").Trim()
        if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($env:FLASK_SECRET_KEY)) {
            throw "Impossible de generer la cle de session Flask."
        }
    }

    $logDirectory = Join-Path $ProjectRoot "logs"
    New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
    $stdoutLog = Join-Path $logDirectory "flask-stdout.log"
    $stderrLog = Join-Path $logDirectory "flask-stderr.log"
    $server = Start-Process -FilePath $VenvPython -ArgumentList @("-u", "app.py") -WorkingDirectory $ProjectRoot -RedirectStandardOutput $stdoutLog -RedirectStandardError $stderrLog -WindowStyle Hidden -PassThru
    Set-Content -LiteralPath (Join-Path $ProjectRoot "mission-sql-cinema.pid") -Value $server.Id -NoNewline

    $serverReady = $false
    for ($attempt = 0; $attempt -lt 45; $attempt++) {
        $server.Refresh()
        if ($server.HasExited) {
            break
        }
        $listener = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if ($null -ne $listener) {
            $serverReady = $true
            break
        }
        Start-Sleep -Seconds 1
    }

    if (-not $serverReady) {
        $server.Refresh()
        if (-not $server.HasExited) {
            Stop-Process -Id $server.Id -Force -ErrorAction SilentlyContinue
        }
        $errorLog = ""
        if (Test-Path -LiteralPath $stderrLog) {
            $errorLog = (Get-Content -LiteralPath $stderrLog -Raw -ErrorAction SilentlyContinue)
        }
        throw "Flask n'a pas ouvert le port $Port. Consulte $stderrLog. $errorLog"
    }

    Write-Host ""
    Write-Host "Mission SQL Cinema est demarre." -ForegroundColor Green
    Write-Host $AppUrl -ForegroundColor Green
    Write-Host "Processus Flask : $($server.Id)"
    Write-Host "Journal des erreurs : $stderrLog"
    Write-Host "Pour arreter le serveur : Stop-Process -Id $($server.Id)"
    try {
        Start-Process $AppUrl
    } catch {
        Write-Warning "Le navigateur n'a pas pu etre ouvert automatiquement. Copie cette adresse dans ton navigateur : $AppUrl"
    }
}
catch {
    Write-Host ""
    Write-Host "ECHEC DU SETUP : $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Aucune table ni base existante n'a ete supprimee par ce script." -ForegroundColor Yellow
    exit 1
}
