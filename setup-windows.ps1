# Setup Script für Windows 11 (PowerShell)
# Refactoring Training - Exercise Environment

param(
    [switch]$Force,
    [switch]$SkipChocoInstall
)

# Requires PowerShell 5.1 or later
#Requires -Version 5.1

# Check if running as Administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Color output functions
function Write-Info {
    param($Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Success {
    param($Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param($Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param($Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Function to check if command exists
function Test-Command {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Function to install Chocolatey
function Install-Chocolatey {
    if (!(Test-Command "choco")) {
        Write-Info "Installiere Chocolatey Package Manager..."
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        if (Test-Command "choco") {
            Write-Success "Chocolatey erfolgreich installiert"
        } else {
            Write-Error "Chocolatey Installation fehlgeschlagen"
            exit 1
        }
    } else {
        Write-Success "Chocolatey bereits installiert"
    }
}

# Main setup function
function Start-Setup {
    Write-Host "🚀 Refactoring Training - Windows Setup" -ForegroundColor Blue
    Write-Host "=======================================" -ForegroundColor Blue
    Write-Host ""

    # Check if running as administrator for some installations
    if (!(Test-Administrator)) {
        Write-Warning "Einige Installationen benötigen Administrator-Rechte."
        Write-Warning "Starten Sie PowerShell als Administrator für vollständiges Setup."
        Write-Host ""
    }

    # Install Chocolatey if not skipped
    if (!$SkipChocoInstall) {
        Install-Chocolatey
    }

    # Install PHP
    Write-Info "Installiere PHP..."
    if (!(Test-Command "php")) {
        if (Test-Command "choco") {
            choco install php -y
            Write-Success "PHP installiert"
        } else {
            Write-Warning "PHP manuell installieren: https://windows.php.net/download/"
        }
    } else {
        $phpVersion = & php -r "echo PHP_VERSION;"
        Write-Success "PHP $phpVersion bereits installiert"
    }

    # Install Composer
    Write-Info "Installiere Composer..."
    if (!(Test-Command "composer")) {
        if (Test-Command "choco") {
            choco install composer -y
            Write-Success "Composer installiert"
        } else {
            Write-Warning "Composer manuell installieren: https://getcomposer.org/download/"
        }
    } else {
        Write-Success "Composer bereits installiert"
    }

    # Install Node.js
    Write-Info "Installiere Node.js..."
    if (!(Test-Command "node")) {
        if (Test-Command "choco") {
            choco install nodejs -y
            Write-Success "Node.js installiert"
        } else {
            Write-Warning "Node.js manuell installieren: https://nodejs.org/"
        }
    } else {
        $nodeVersion = & node -v
        Write-Success "Node.js $nodeVersion bereits installiert"
    }

    # Install Python
    Write-Info "Installiere Python..."
    if (!(Test-Command "python")) {
        if (Test-Command "choco") {
            choco install python -y
            Write-Success "Python installiert"
        } else {
            Write-Warning "Python manuell installieren: https://www.python.org/downloads/"
        }
    } else {
        $pythonVersion = & python --version
        Write-Success "$pythonVersion bereits installiert"
    }

    # Refresh PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

    # Setup PHP project
    Write-Info "Richte PHP-Projekt ein..."
    Set-Location "php"
    
    if (!(Test-Path "vendor")) {
        if (Test-Command "composer") {
            composer install --no-dev
            Write-Success "PHP Dependencies installiert"
        } else {
            Write-Error "Composer nicht verfügbar. PHP Setup übersprungen."
        }
    } else {
        Write-Success "PHP Dependencies bereits installiert"
    }

    # Test PHP setup
    Write-Info "Teste PHP Setup..."
    if (Test-Command "vendor\bin\phpunit.bat") {
        try {
            $phpunitResult = & vendor\bin\phpunit.bat exercises\CodeSmells\LongMethod\ --no-coverage 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Success "PHP Tests erfolgreich"
            } else {
                Write-Warning "PHP Tests fehlgeschlagen - bitte manuell prüfen"
            }
        }
        catch {
            Write-Warning "PHP Tests konnten nicht ausgeführt werden"
        }
    } else {
        Write-Warning "PHPUnit nicht verfügbar"
    }

    Set-Location ".."

    # Setup TypeScript project
    Write-Info "Richte TypeScript-Projekt ein..."
    Set-Location "typescript"
    
    if (!(Test-Path "node_modules")) {
        if (Test-Command "npm") {
            npm install
            Write-Success "TypeScript Dependencies installiert"
        } else {
            Write-Error "npm nicht verfügbar. TypeScript Setup übersprungen."
        }
    } else {
        Write-Success "TypeScript Dependencies bereits installiert"
    }

    # Test TypeScript setup
    Write-Info "Teste TypeScript Setup..."
    if (Test-Command "npm") {
        try {
            $npmTestResult = npm test 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Success "TypeScript Tests erfolgreich"
            } else {
                Write-Warning "TypeScript Tests fehlgeschlagen - bitte manuell prüfen"
            }
        }
        catch {
            Write-Warning "TypeScript Tests konnten nicht ausgeführt werden"
        }
    }

    Set-Location ".."

    # Setup Python project
    Write-Info "Richte Python-Projekt ein..."
    Set-Location "python"

    # Create virtual environment
    if (!(Test-Path "venv")) {
        if (Test-Command "python") {
            python -m venv venv
            Write-Success "Python Virtual Environment erstellt"
        } else {
            Write-Error "Python nicht verfügbar. Python Setup übersprungen."
            Set-Location ".."
            return
        }
    } else {
        Write-Success "Python Virtual Environment bereits vorhanden"
    }

    # Activate virtual environment and install dependencies
    if (Test-Path "venv\Scripts\Activate.ps1") {
        & "venv\Scripts\Activate.ps1"
        
        if (Test-Path "requirements.txt") {
            pip install -r requirements.txt
            Write-Success "Python Dependencies installiert"
        }

        # Test Python setup
        Write-Info "Teste Python Setup..."
        try {
            $pytestResult = pytest "exercises\code-smells\long-method\tests\" -v 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Python Tests erfolgreich"
            } else {
                Write-Warning "Python Tests fehlgeschlagen - bitte manuell prüfen"
            }
        }
        catch {
            Write-Warning "Python Tests konnten nicht ausgeführt werden"
        }

        deactivate
    }

    Set-Location ".."

    # Optional tools
    Write-Info "Prüfe optionale Entwicklungstools..."

    if (!(Test-Command "git")) {
        Write-Warning "Git nicht gefunden. Installation über Chocolatey: choco install git"
    }

    if (!(Test-Command "code")) {
        Write-Warning "VS Code nicht gefunden. Installation über: https://code.visualstudio.com/"
    } else {
        Write-Info "VS Code gefunden. Extensions werden automatisch über .vscode/extensions.json empfohlen."
        Write-Info "Wichtige Extensions: PHP Intelephense, PHPUnit Test Explorer, Jest, Python (mit Testing-Support)"
    }

    # Summary
    Write-Host ""
    Write-Host "🎉 Setup abgeschlossen!" -ForegroundColor Green
    Write-Host "======================" -ForegroundColor Green
    Write-Success "Alle verfügbaren Projekte wurden eingerichtet"
    Write-Host ""
    Write-Host "📁 Nächste Schritte:" -ForegroundColor Blue
    Write-Host "  1. Öffnen Sie das Projekt in Ihrer IDE:"
    Write-Host "     - VS Code: code ."
    Write-Host "     - PhpStorm: File → Open → refactoring-exercises\php\"
    Write-Host "     - WebStorm: File → Open → refactoring-exercises\typescript\"
    Write-Host "     - PyCharm: File → Open → refactoring-exercises\python\"
    Write-Host ""
    Write-Host "  2. Tests ausführen:" -ForegroundColor Blue
    Write-Host "     - PHP: cd php && vendor\bin\phpunit.bat"
    Write-Host "     - TypeScript: cd typescript && npm test"
    Write-Host "     - Python: cd python && venv\Scripts\Activate.ps1 && pytest exercises\"
    Write-Host ""
    Write-Host "  3. Erste Aufgabe starten:" -ForegroundColor Blue
    Write-Host "     - Öffnen Sie exercises\CodeSmells\LongMethod\task.md (PHP)"
    Write-Host "     - Oder exercises\code-smells\long-method\task.md (TypeScript/Python)"
    Write-Host ""
    Write-Host "📖 Weitere Hilfe: README.md und IDE_SETUP.md" -ForegroundColor Blue
}

# Error handling
trap {
    Write-Error "Ein Fehler ist aufgetreten: $_"
    Write-Host "Versuchen Sie das Script als Administrator auszuführen oder installieren Sie die Tools manuell."
    exit 1
}

# Start the setup
Start-Setup