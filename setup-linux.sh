#!/bin/bash

# Setup Script für Linux (Ubuntu 24.04)
# Refactoring Training - Exercise Environment

set -e  # Exit on any error

echo "🚀 Refactoring Training - Linux Setup"
echo "====================================="

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Dieses Skript ist nur für Linux. Verwenden Sie setup-windows.ps1 für Windows."
    exit 1
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Update package manager
print_status "Aktualisiere Paketmanager..."
sudo apt update

# Install PHP 8.3
print_status "Installiere PHP 8.3..."
if ! command_exists php; then
    sudo apt install -y php8.3 php8.3-cli php8.3-mbstring php8.3-xml php8.3-curl php8.3-zip
    print_success "PHP installiert"
else
    PHP_VERSION=$(php -r "echo PHP_VERSION;")
    if [[ $PHP_VERSION == 8.3* ]] || [[ $PHP_VERSION == 8.2* ]]; then
        print_success "PHP $PHP_VERSION bereits installiert"
    else
        print_warning "PHP Version $PHP_VERSION gefunden. PHP 8.2+ wird empfohlen."
    fi
fi

# Install Composer
print_status "Installiere Composer..."
if ! command_exists composer; then
    # Download and install composer
    curl -sS https://getcomposer.org/installer | php
    sudo mv composer.phar /usr/local/bin/composer
    sudo chmod +x /usr/local/bin/composer
    print_success "Composer installiert"
else
    print_success "Composer bereits installiert"
fi

# Install Node.js and npm
print_status "Installiere Node.js..."
if ! command_exists node; then
    # Install Node.js LTS
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
    sudo apt-get install -y nodejs
    print_success "Node.js installiert"
else
    NODE_VERSION=$(node -v)
    print_success "Node.js $NODE_VERSION bereits installiert"
fi

# Install Python 3.11+
print_status "Installiere Python..."
if ! command_exists python3; then
    sudo apt install -y python3 python3-pip python3-venv
    print_success "Python installiert"
else
    PYTHON_VERSION=$(python3 --version)
    print_success "$PYTHON_VERSION bereits installiert"
fi

# Install pip if not available
if ! command_exists pip3; then
    sudo apt install -y python3-pip
fi

# Setup PHP project
print_status "Richte PHP-Projekt ein..."
cd php
if [ ! -d "vendor" ]; then
    composer install --no-dev
    print_success "PHP Dependencies installiert"
else
    print_success "PHP Dependencies bereits installiert"
fi

# Run PHP tests to verify setup
print_status "Teste PHP Setup..."
if vendor/bin/phpunit --version >/dev/null 2>&1; then
    print_success "PHPUnit funktioniert"
    # Run actual tests
    if vendor/bin/phpunit exercises/CodeSmells/LongMethod/ --no-coverage >/dev/null 2>&1; then
        print_success "PHP Tests erfolgreich"
    else
        print_warning "PHP Tests fehlgeschlagen - bitte manuell prüfen"
    fi
else
    print_error "PHPUnit Setup fehlgeschlagen"
fi

cd ..

# Setup TypeScript project
print_status "Richte TypeScript-Projekt ein..."
cd typescript
if [ ! -d "node_modules" ]; then
    npm install
    print_success "TypeScript Dependencies installiert"
else
    print_success "TypeScript Dependencies bereits installiert"
fi

# Run TypeScript tests to verify setup
print_status "Teste TypeScript Setup..."
if npm test >/dev/null 2>&1; then
    print_success "TypeScript Tests erfolgreich"
else
    print_warning "TypeScript Tests fehlgeschlagen - bitte manuell prüfen"
fi

cd ..

# Setup Python project
print_status "Richte Python-Projekt ein..."
cd python

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Python Virtual Environment erstellt"
else
    print_success "Python Virtual Environment bereits vorhanden"
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
if [ ! -f "venv/pyvenv.cfg" ] || ! pip list | grep -q pytest; then
    pip install -r requirements.txt
    print_success "Python Dependencies installiert"
else
    print_success "Python Dependencies bereits installiert"
fi

# Run Python tests to verify setup
print_status "Teste Python Setup..."
if pytest exercises/code-smells/long-method/tests/ -v >/dev/null 2>&1; then
    print_success "Python Tests erfolgreich"
else
    print_warning "Python Tests fehlgeschlagen - bitte manuell prüfen"
fi

deactivate
cd ..

# Optional: Install development tools
print_status "Installiere optionale Entwicklungstools..."

# Git (should be already installed)
if ! command_exists git; then
    sudo apt install -y git
    print_success "Git installiert"
fi

# VS Code (optional)
if ! command_exists code; then
    print_warning "VS Code nicht gefunden. Installation über:"
    echo "  wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg"
    echo "  sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/"
    echo "  sudo sh -c 'echo \"deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main\" > /etc/apt/sources.list.d/vscode.list'"
    echo "  sudo apt update && sudo apt install code"
else
    print_success "VS Code gefunden. Extensions werden automatisch über .vscode/extensions.json empfohlen."
    print_info "Wichtige Extensions: PHP Intelephense, PHPStan, Jest, Python (mit nativem Testing-Support)"
fi

# Summary
echo ""
echo "🎉 Setup abgeschlossen!"
echo "======================"
print_success "Alle Projekte sind eingerichtet und getestet"
echo ""
echo "📁 Nächste Schritte:"
echo "  1. Öffnen Sie das Projekt in Ihrer IDE:"
echo "     - VS Code: code ."
echo "     - PhpStorm: File → Open → refactoring-exercises/php/"
echo "     - WebStorm: File → Open → refactoring-exercises/typescript/"
echo "     - PyCharm: File → Open → refactoring-exercises/python/"
echo ""
echo "  2. Tests ausführen:"
echo "     - PHP: cd php && vendor/bin/phpunit"
echo "     - TypeScript: cd typescript && npm test"
echo "     - Python: cd python && source venv/bin/activate && pytest exercises/"
echo ""
echo "  3. Erste Aufgabe starten:"
echo "     - Öffnen Sie exercises/CodeSmells/LongMethod/task.md (PHP)"
echo "     - Oder exercises/code-smells/long-method/task.md (TypeScript/Python)"
echo ""
echo "📖 Weitere Hilfe: README.md und IDE_SETUP.md"