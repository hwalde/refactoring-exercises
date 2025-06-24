# Remote Desktop Requirements (Windows 11)

Anforderungen für Windows 11 Remote Desktop Schulungsinstanzen.

## Systemanforderungen

### Hardware (pro Instanz)
- **CPU**: 4+ Kerne (für bis zu 10 gleichzeitige Benutzer)
- **RAM**: 8GB minimum (16GB+ empfohlen)
- **Storage**: 100GB SSD pro Instanz
- **Network**: Stabile Internet-Verbindung (min. 100 Mbps)

### Software Basis
- **OS**: Windows 11 Pro (für RDP-Support)
- **RDP**: Remote Desktop aktiviert
- **Updates**: Aktuelle Windows Updates installiert
- **Git**: Git für Windows (https://git-scm.com/download/win)

## Benötigte Software-Installation

### 1. Entwicklungs-Runtimes

#### PHP 8.3
- **Download**: https://windows.php.net/download/
- **Version**: PHP 8.3.*
- **Installation**: 
  - ZIP-Datei herunterladen und entpacken (z.B. nach `C:\php`)
  - PATH-Variable um PHP-Ordner erweitern
  - `php.ini-development` zu `php.ini` kopieren
- **Xdebug Extension**: https://xdebug.org/download
  - Xdebug DLL herunterladen und in `ext/` Ordner kopieren
  - **Wichtig**: Datei zu `php_xdebug.dll` umbenennen
  - In `php.ini` hinzufügen: `zend_extension="php_xdebug.dll"`
  - Coverage aktivieren: `xdebug.mode=coverage`
- **Composer**: https://getcomposer.org/Composer-Setup.exe herunterladen und ausführen

#### Node.js
- **Download**: https://nodejs.org/en/download/
- **Version**: Aktuelles stable release
- **Installation**: Windows Installer (.msi)
- **Pfad**: Automatisch zu PATH hinzugefügt
- **NPM**: Wird automatisch mit Node.js installiert

#### Python 3.12
- **Download**: https://www.python.org/downloads/windows/
- **Version**: Python 3.12.*
- **Installation**: "Add Python to PATH" aktivieren
- **Alternative**: Microsoft Store Version

### 2. IDEs und Editoren

#### JetBrains IDEs (Erforderlich)
```powershell
# JetBrains Toolbox herunterladen und installieren
# Von: https://www.jetbrains.com/toolbox-app/

# Über Toolbox installieren:
# - PyCharm (Python Development)
# - WebStorm (TypeScript Development)
# - PHPStorm (PHP Development)
```

#### Visual Studio Code (Erforderlich)
```powershell
# VS Code herunterladen
# Von: https://code.visualstudio.com/download

# Erforderliche Extensions:
code --install-extension ms-vscode.vscode-typescript-next
code --install-extension ms-python.python
code --install-extension bmewburn.vscode-intelephense-client
code --install-extension esbenp.prettier-vscode
code --install-extension ms-python.black-formatter
```

### 3. Zusätzliche Tools

#### Git für Windows
- **Download**: https://git-scm.com/download/win
- **Konfiguration**: Git Bash und Git GUI installieren

#### Windows Terminal (Modern)
- **Installation**: Über Microsoft Store
- **Alternative**: PowerShell 7+

## Automatisches Setup-Skript

### PowerShell Setup-Skript
```powershell
# setup-windows.ps1
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Write-Host "=== Refactoring Training - Windows Setup ===" -ForegroundColor Green

# Chocolatey Package Manager installieren
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Chocolatey..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# Software über Chocolatey installieren
Write-Host "Installing development tools..." -ForegroundColor Yellow
choco install -y nodejs-lts python3 git vscode

# JetBrains Toolbox
Write-Host "Installing JetBrains Toolbox..." -ForegroundColor Yellow
choco install -y jetbrainstoolbox

# VS Code Extensions
Write-Host "Installing VS Code extensions..." -ForegroundColor Yellow
code --install-extension ms-vscode.vscode-typescript-next
code --install-extension ms-python.python
code --install-extension bmewburn.vscode-intelephense-client
code --install-extension esbenp.prettier-vscode

Write-Host "=== Installation completed! ===" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Download and setup PHP 8.3 manually"
Write-Host "2. Install and configure Xdebug extension"
Write-Host "3. Install JetBrains IDEs via Toolbox"
Write-Host "4. Restart system"
Write-Host "5. Run project setup: .\scripts\setup-projects.ps1"
```

## Projekt-Konfiguration

### 1. Repository Setup
```powershell
# Repository clonen
git clone <repository-url> refactoring-training
cd refactoring-training\refactoring-exercises

# Setup-Skript ausführen
.\scripts\setup-projects.ps1
```

### 2. Dependencies installieren
```powershell
# PHP Dependencies
cd php
composer install
cd ..

# TypeScript Dependencies
cd typescript
npm install
cd ..

# Python Dependencies
cd python
python -m venv venv
venv\Scripts\activate
pip install -e ".[dev]"
cd ..
```

### 3. Tests validieren
```powershell
# PHP Tests
cd php
composer test
cd ..

# TypeScript Tests
cd typescript
npm test
cd ..

# Python Tests
cd python
venv\Scripts\activate
pytest
cd ..
```

## IDE-Konfigurationen

### PhpStorm Setup
```yaml
# .idea/php.xml
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="PhpProjectSharedConfiguration">
    <option name="suggestionLevel" value="WARNING" />
  </component>
  <component name="PhpUnit">
    <option name="directories">
      <list>
        <option value="$PROJECT_DIR$/exercises" />
      </list>
    </option>
  </component>
</project>
```

### WebStorm Setup
```json
// .vscode/settings.json (für VS Code)
{
  "typescript.preferences.includePackageJsonAutoImports": "on",
  "typescript.suggest.autoImports": true,
  "jest.jestCommandLine": "npm test",
  "typescript.validate.enable": true
}
```

### PyCharm Setup
```yaml
# .idea/misc.xml
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectRootManager" version="2" project-jdk-name="Python 3.11 (venv)" project-jdk-type="Python SDK" />
</project>
```

## Remote Desktop Konfiguration

### RDP-Einstellungen
```powershell
# Remote Desktop aktivieren
Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections" -Value 0

# Mehrere gleichzeitige Sessions erlauben (Windows 11 Pro)
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server\Licensing Core" -Name "EnableConcurrentSessions" -Value 1
```

### Benutzer-Management
```powershell
# Schulungs-Benutzer erstellen
$users = @("student01", "student02", "student03") # bis student10

foreach ($user in $users) {
    $password = ConvertTo-SecureString "Training2024!" -AsPlainText -Force
    New-LocalUser -Name $user -Password $password -Description "Training User"
    Add-LocalGroupMember -Group "Remote Desktop Users" -Member $user
}
```

## Performance-Optimierung

### 1. Windows-Optimierungen
```powershell
# Unnötige Services deaktivieren
Set-Service -Name "Themes" -StartupType Disabled
Set-Service -Name "TabletInputService" -StartupType Disabled

# Visuelle Effekte reduzieren
$path = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects"
Set-ItemProperty -Path $path -Name "VisualFXSetting" -Value 2
```

### 2. IDE-Optimierungen
```powershell
# JetBrains IDEs: Memory-Einstellungen erhöhen
$phpstormVmoptions = @"
-Xmx2g
-XX:ReservedCodeCacheSize=512m
-XX:+UseConcMarkSweepGC
-XX:SoftRefLRUPolicyMSPerMB=50
"@

# In entsprechende .vmoptions Dateien schreiben
```

## Netzwerk und Sicherheit

### Firewall-Regeln
```powershell
# RDP erlauben
New-NetFirewallRule -DisplayName "Allow RDP" -Direction Inbound -Protocol TCP -LocalPort 3389 -Action Allow

# Development Ports (optional)
New-NetFirewallRule -DisplayName "Node.js Dev" -Direction Inbound -Protocol TCP -LocalPort 3000-3999 -Action Allow
New-NetFirewallRule -DisplayName "PHP Dev" -Direction Inbound -Protocol TCP -LocalPort 8000-8999 -Action Allow
```

### Updates und Wartung
```powershell
# Automatische Updates konfigurieren
$AU = New-Object -ComObject Microsoft.Update.AutoUpdate
$AU.Settings.NotificationLevel = 2  # Download and notify

# Wartungsfenster definieren
$MaintenanceSettings = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File C:\Scripts\maintenance.ps1"
Register-ScheduledTask -TaskName "Maintenance" -Action $MaintenanceSettings -Trigger (New-ScheduledTaskTrigger -Daily -At "02:00")
```

## Deployment-Checkliste

### Vor Schulung
- [ ] Alle Software installiert und getestet
- [ ] Benutzer-Accounts erstellt
- [ ] Repository geclont und Dependencies installiert
- [ ] Tests laufen erfolgreich
- [ ] RDP-Zugang getestet
- [ ] Backup der VM erstellt

### Pro Instanz (10 Benutzer)
- [ ] Windows 11 Pro aktiviert
- [ ] 16GB RAM verfügbar
- [ ] 100GB freier Speicher
- [ ] Alle IDEs installiert
- [ ] Projekt-Setup abgeschlossen
- [ ] Performance getestet

### Monitoring
```powershell
# Performance Monitor Setup
$counters = @(
    "\Processor(_Total)\% Processor Time",
    "\Memory\Available MBytes",
    "\Terminal Services Session(*)\% Processor Time"
)

# Log für Monitoring
Get-Counter -Counter $counters -Continuous -SampleInterval 30 | Export-Counter -Path "C:\Logs\performance.csv"
```

## Troubleshooting

### Häufige Probleme

#### PHP
```powershell
# PHP nicht im PATH
# PATH-Variable prüfen und PHP-Ordner hinzufügen
$env:PATH += ";C:\php"

# Xdebug lädt nicht
# 1. Prüfen ob php_xdebug.dll im ext/ Ordner ist
# 2. php.ini Einträge prüfen:
#    zend_extension="php_xdebug.dll"
#    xdebug.mode=coverage

# PHP Version prüfen
php --version
php -m | findstr xdebug
```

#### Node.js/NPM
```powershell
# NPM Permission Fehler
npm config set cache C:\npm-cache --global
npm config set prefix C:\npm-global --global
```

#### Python/pip
```powershell
# Virtual Environment Probleme
Remove-Item -Recurse -Force venv
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

### Support-Informationen sammeln
```powershell
# System-Info für Support
$info = @{
    "OS" = (Get-WmiObject Win32_OperatingSystem).Caption
    "RAM" = [math]::Round((Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory/1GB, 2)
    "CPU" = (Get-WmiObject Win32_Processor).Name
    "PHP" = php --version 2>$null
    "Node" = node --version 2>$null
    "Python" = python --version 2>$null
}

$info | ConvertTo-Json | Out-File "C:\support-info.json"
```

## Kostenoptimierung

### VM-Sizing
- **Standard**: 4 vCPU, 16GB RAM für 8-10 Benutzer
- **Premium**: 8 vCPU, 32GB RAM für 15-20 Benutzer
- **Storage**: SSD für bessere Performance

### Auto-Shutdown
```powershell
# Automatisches Herunterfahren nach Schulung
$trigger = New-ScheduledTaskTrigger -Daily -At "18:00"
$action = New-ScheduledTaskAction -Execute "shutdown.exe" -Argument "/s /t 60"
Register-ScheduledTask -TaskName "AutoShutdown" -Action $action -Trigger $trigger
```