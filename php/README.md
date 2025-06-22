# PHP Refactoring Exercises

PHP 8.2+ Refactoring-Übungen mit PHPUnit, PHPStan und PHP-CS-Fixer.

## Voraussetzungen

- PHP 8.2 oder höher
- Composer
- Eine der unterstützten IDEs

## Setup

1. **Dependencies installieren**:
   ```bash
   composer install
   ```

2. **Tests ausführen** (müssen alle grün sein):
   ```bash
   vendor/bin/phpunit
   ```

## Test-Ausführung

### PhpStorm
1. Rechtsklick auf `phpunit.xml` → "Run 'phpunit.xml'"
2. Oder: Run → "Edit Configurations" → "+" → "PHPUnit" → "Defined in the configuration file"

### VS Code
1. **Empfohlene Extensions**:
   - PHP Intelephense
   - PHPUnit Test Explorer
   - PHP CS Fixer

2. **Tasks** (Ctrl+Shift+P → "Tasks: Run Task"):
   - "PHP: Run Tests"
   - "PHP: Check Code Style"
   - "PHP: Fix Code Style"

3. **Launch Configuration** (.vscode/launch.json):
   ```json
   {
       "name": "Debug PHPUnit",
       "type": "php",
       "request": "launch",
       "program": "${workspaceFolder}/vendor/bin/phpunit",
       "args": ["--configuration", "phpunit.xml"],
       "cwd": "${workspaceFolder}"
   }
   ```

### Kommandozeile

#### Linux (Bash)
```bash
# Tests ausführen
vendor/bin/phpunit

# Tests mit Coverage
vendor/bin/phpunit --coverage-html=coverage

# Spezifische Aufgabe testen
vendor/bin/phpunit exercises/CodeSmells/LongMethod/OrderProcessorTest.php

# Code Style prüfen
vendor/bin/php-cs-fixer fix --dry-run --diff

# Code Style automatisch korrigieren
vendor/bin/php-cs-fixer fix

# Statische Analyse
vendor/bin/phpstan analyse
```

#### Windows (PowerShell)
```powershell
# Tests ausführen
vendor\bin\phpunit.bat

# Tests mit Coverage
vendor\bin\phpunit.bat --coverage-html=coverage

# Spezifische Aufgabe testen
vendor\bin\phpunit.bat exercises\CodeSmells\LongMethod\OrderProcessorTest.php

# Code Style prüfen
vendor\bin\php-cs-fixer.bat fix --dry-run --diff

# Code Style automatisch korrigieren
vendor\bin\php-cs-fixer.bat fix

# Statische Analyse
vendor\bin\phpstan.bat analyse
```

## Arbeitsweise

1. **Aufgabe auswählen**: Wechsle in einen Aufgaben-Ordner (z.B. `exercises/CodeSmells/LongMethod/`)
2. **Tests ausführen**: `vendor/bin/phpunit exercises/CodeSmells/LongMethod/OrderProcessorTest.php` (Windows: `vendor\bin\phpunit.bat exercises\CodeSmells\LongMethod\OrderProcessorTest.php`)
3. **Code refactorieren**: Ändere die Datei `OrderProcessor.php`
4. **Tests erneut ausführen**: Stelle sicher, dass sie grün bleiben

## Code-Qualität

- **PSR-12 Standard**: Eingehalten durch PHP-CS-Fixer
- **PHPStan Level 8**: Maximale statische Analyse
- **Type Declarations**: Vollständige Typisierung erforderlich
- **Strict Types**: Aktiviert in allen Dateien

## Debugging

### PhpStorm
- Breakpoints setzen und "Debug" statt "Run" wählen
- Xdebug wird automatisch erkannt

### VS Code
- Xdebug Extension installieren
- Launch Configuration verwenden (siehe oben)
- F5 für Debug-Start

## Troubleshooting

### "Class not found" Fehler
```bash
composer dump-autoload
```

### "Permission denied" unter Linux
```bash
sudo chown -R $USER:$USER .
chmod -R 755 .
```

### "No code coverage driver available" 
PHPUnit benötigt Xdebug oder PCOV für Coverage-Reports. PCOV installieren:
```bash
# Linux/macOS
sudo pecl install pcov

# Dann in php.ini hinzufügen:
extension=pcov

# Test mit aktiviertem PCOV
php -dpcov.enabled=1 vendor/bin/phpunit --coverage-html=coverage
```

### PHP Version prüfen
```bash
php --version
composer --version
```