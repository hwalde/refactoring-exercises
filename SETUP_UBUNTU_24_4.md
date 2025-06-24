# Linux Requirements (Ubuntu 24.04)

Anforderungen und Setup-Anleitung für Refactoring-Übungen unter Ubuntu 24.04 LTS.

## Systemanforderungen

### Hardware
- **CPU**: 2+ Kerne (4+ empfohlen)
- **RAM**: 4GB minimum (8GB+ empfohlen)
- **Storage**: 5GB freier Speicherplatz
- **Internet**: Für initialen Download der Dependencies

### Software
- **Ubuntu**: 24.04 LTS (frische Installation)
- **User**: Sudo-Berechtigung erforderlich

## Automatisches Setup

### Schnell-Installation (empfohlen)
```bash
# Repository clonen
git clone <repository-url> refactoring-training
cd refactoring-training/refactoring-exercises

# Setup-Skript ausführen
chmod +x scripts/setup-linux.sh
./scripts/setup-linux.sh
```

### Setup-Skript Inhalt
Das Skript installiert automatisch alle benötigten Komponenten:

```bash
#!/bin/bash
set -e

echo "=== Refactoring Training - Linux Setup ==="

# System Update
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# PHP 8.2+ Installation
echo "Installing PHP 8.2..."
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:ondrej/php -y
sudo apt update
sudo apt install -y php8.2 php8.2-cli php8.2-mbstring php8.2-xml php8.2-curl php8.2-zip

# Composer Installation
echo "Installing Composer..."
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer

# Node.js 20 LTS Installation
echo "Installing Node.js 20 LTS..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Python 3.11+ (already in Ubuntu 24.04)
echo "Setting up Python 3.11..."
sudo apt install -y python3 python3-pip python3-venv

# Git (usually pre-installed)
sudo apt install -y git

# IDEs and Editors
echo "Installing development tools..."

# VS Code
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install -y code

# JetBrains Toolbox (for PhpStorm, WebStorm, PyCharm)
echo "Downloading JetBrains Toolbox..."
wget -O jetbrains-toolbox.tar.gz "https://data.services.jetbrains.com/products/download?platform=linux&code=TBA"
tar -xzf jetbrains-toolbox.tar.gz
sudo mv jetbrains-toolbox-*/jetbrains-toolbox /usr/local/bin/
rm -rf jetbrains-toolbox*

echo "=== Installation completed! ==="
echo "Next steps:"
echo "1. Install JetBrains IDEs via Toolbox: jetbrains-toolbox"
echo "2. Run project setup: ./scripts/setup-projects.sh"
```

## Manuelle Installation

### 1. PHP 8.2+ Setup
```bash
# PHP Repository hinzufügen
sudo apt install software-properties-common
sudo add-apt-repository ppa:ondrej/php
sudo apt update

# PHP 8.2 und Extensions installieren
sudo apt install php8.2 php8.2-cli php8.2-mbstring php8.2-xml php8.2-curl php8.2-zip

# Composer installieren
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer

# Verifizierung
php --version  # Sollte 8.2+ zeigen
composer --version
```

### 2. Node.js 20 LTS Setup
```bash
# NodeSource Repository
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verifizierung
node --version  # Sollte v20.x.x zeigen
npm --version
```

### 3. Python 3.11+ Setup
```bash
# Python 3.11 (bereits in Ubuntu 24.04)
sudo apt install python3 python3-pip python3-venv

# Verifizierung
python3 --version  # Sollte 3.11+ zeigen
pip3 --version
```

### 4. IDEs Installation

#### VS Code
```bash
# Microsoft Repository
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code

# Empfohlene Extensions installieren
code --install-extension ms-vscode.vscode-typescript-next
code --install-extension ms-python.python
code --install-extension bmewburn.vscode-intelephense-client
```

#### JetBrains IDEs
```bash
# Toolbox herunterladen und installieren
wget -O jetbrains-toolbox.tar.gz "https://data.services.jetbrains.com/products/download?platform=linux&code=TBA"
tar -xzf jetbrains-toolbox.tar.gz
sudo mv jetbrains-toolbox-*/jetbrains-toolbox /usr/local/bin/

# Toolbox starten und IDEs installieren
jetbrains-toolbox
```

**Über Toolbox installieren**:
- PhpStorm (für PHP)
- WebStorm (für TypeScript)
- PyCharm Professional (für Python)

## Projekt-Setup

### 1. Dependencies installieren
```bash
cd refactoring-exercises

# PHP Dependencies
cd php && composer install && cd ..

# TypeScript Dependencies  
cd typescript && npm install && cd ..

# Python Dependencies
cd python && python3 -m venv venv && source venv/bin/activate && pip install -e ".[dev]" && cd ..
```

### 2. Tests ausführen (Validierung)
```bash
# PHP Tests
cd php && composer test && cd ..

# TypeScript Tests
cd typescript && npm test && cd ..

# Python Tests  
cd python && source venv/bin/activate && pytest && cd ..
```

## Troubleshooting

### PHP Probleme
```bash
# Composer Permissions
sudo chown -R $USER:$USER ~/.composer

# PHP Extensions fehlen
sudo apt install php8.2-{mbstring,xml,curl,zip}
```

### Node.js Probleme
```bash
# NPM Permissions
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### Python Probleme
```bash
# Virtual Environment neu erstellen
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
```

### IDE Probleme
```bash
# VS Code Reset
rm -rf ~/.vscode
code --reset-permissions

# JetBrains Cache leeren
rm -rf ~/.cache/JetBrains
```

## Performance-Optimierung

### 1. System-Tuning
```bash
# Mehr File Watchers für IDEs
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### 2. IDE-Optimierung
```bash
# Für JetBrains IDEs: Mehr Memory
echo "-Xmx4g" >> ~/.local/share/JetBrains/Toolbox/apps/PhpStorm/ch-0/*/bin/phpstorm64.vmoptions
```

## Offline-Fähigkeit

Nach initialem Setup funktionieren alle Übungen offline:
- Dependencies sind lokal installiert
- Keine Netzwerkverbindung für Code-Ausführung nötig
- Tests laufen komplett lokal

## Sicherheit

### Firewall (optional)
```bash
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

### Updates
```bash
# Regelmäßige Updates
sudo apt update && sudo apt upgrade
npm update -g
composer global update
```

## Validierung der Installation

### Funktionstest
```bash
# Alle Tests in allen Sprachen ausführen
./scripts/validate-setup.sh
```

**Erwartete Ausgabe**:
```
✅ PHP 8.2+ installed
✅ Composer working
✅ Node.js 20+ installed
✅ NPM working
✅ Python 3.11+ installed
✅ pip working
✅ All project dependencies installed
✅ All tests passing
✅ Setup completed successfully!
```

## Support

Bei Problemen:
1. Prüfe Systemanforderungen
2. Führe Setup-Skript erneut aus
3. Schaue in Troubleshooting-Sektion
4. Kontaktiere Support mit Fehlermeldung und `uname -a` Output