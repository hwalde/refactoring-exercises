# IDE Setup und Konfiguration

Diese Anleitung zeigt, wie Sie die Refactoring-Übungen in verschiedenen IDEs einrichten und ausführen.

## 🚀 Schnellstart

### PhpStorm (PHP)
1. **Projekt öffnen**: `File` → `Open` → `refactoring-exercises/php/`
2. **Composer installieren**: Terminal in PhpStorm → `composer install`
3. **PHPUnit konfigurieren**:
   - `File` → `Settings` → `PHP` → `Test Frameworks`
   - `+` → `PHPUnit Local`
   - `Use Composer autoloader`: `vendor/autoload.php`
   - `Default configuration file`: `phpunit.xml`

### WebStorm (TypeScript)
1. **Projekt öffnen**: `File` → `Open` → `refactoring-exercises/typescript/`
2. **Dependencies installieren**: Terminal → `npm install`
3. **Jest konfigurieren**:
   - `File` → `Settings` → `Languages & Frameworks` → `JavaScript` → `Testing` → `Jest`
   - `Jest package`: `node_modules/jest`
   - `Configuration file`: `jest.config.js`

### PyCharm (Python)
1. **Projekt öffnen**: `File` → `Open` → `refactoring-exercises/python/`
2. **Virtual Environment erstellen**: Terminal → `python -m venv venv && source venv/bin/activate`
3. **Dependencies installieren**: `pip install -r requirements.txt`
4. **pytest konfigurieren**:
   - `File` → `Settings` → `Tools` → `Python Integrated Tools`
   - `Testing`: `pytest`
   - `pytest target`: `refactoring-exercises/python`

### VS Code (Alle Sprachen)
1. **Workspace öffnen**: `File` → `Open Folder` → `refactoring-exercises/`
2. **Extensions installieren** (automatisch über `.vscode/extensions.json`):
   - PHP: `PHP Intelephense`, `PHPUnit Test Explorer`, `PHPStan`
   - TypeScript: `TypeScript`, `Jest`, `ESLint`, `Prettier`
   - Python: `Python` (enthält native Testing-Support)

---

## 📁 Run Configurations

### PhpStorm - PHPUnit Run Configurations

#### Long Method Test (Einzelaufgabe)
```
Name: Long Method Tests
Test scope: Directory
Directory: exercises/CodeSmells/LongMethod
Use alternative configuration file: ✓
Alternative configuration file: phpunit.xml
```

#### Alle Tests
```
Name: All PHP Tests
Test scope: Defined in the configuration file
Use alternative configuration file: ✓
Alternative configuration file: phpunit.xml
```

### WebStorm - Jest Run Configurations

#### Long Method Test (Einzelaufgabe)
```
Name: Long Method Tests (TS)
Jest package: node_modules/jest
Working directory: typescript/
Jest options: --config jest.config.js
Test file patterns: exercises/code-smells/long-method/tests/*.test.ts
```

#### Alle Tests
```
Name: All TypeScript Tests
Jest package: node_modules/jest
Working directory: typescript/
Jest options: --config jest.config.js
Test file patterns: exercises/**/*.test.ts
```

### PyCharm - pytest Run Configurations

#### Long Method Test (Einzelaufgabe)
```
Name: Long Method Tests (Python)
Target type: Script path
Target: exercises/code-smells/long-method/tests/
Python interpreter: venv/bin/python
Working directory: python/
Additional arguments: -v
```

#### Alle Tests
```
Name: All Python Tests
Target type: Module name
Target: pytest
Python interpreter: venv/bin/python
Working directory: python/
Additional arguments: exercises/ -v
```

---

## 🔧 VS Code Tasks und Launch Configurations

### `.vscode/tasks.json`
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "PHP: Run Tests",
            "type": "shell",
            "command": "vendor/bin/phpunit",
            "group": "test",
            "options": {
                "cwd": "${workspaceFolder}/php"
            },
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        },
        {
            "label": "TypeScript: Run Tests",
            "type": "shell",
            "command": "npm",
            "args": ["test"],
            "group": "test",
            "options": {
                "cwd": "${workspaceFolder}/typescript"
            },
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        },
        {
            "label": "Python: Run Tests",
            "type": "shell",
            "command": "pytest",
            "args": ["exercises/", "-v"],
            "group": "test",
            "options": {
                "cwd": "${workspaceFolder}/python"
            },
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        }
    ]
}
```

### `.vscode/launch.json`
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug PHP Tests",
            "type": "php",
            "request": "launch",
            "program": "${workspaceFolder}/php/vendor/bin/phpunit",
            "args": [
                "exercises/CodeSmells/LongMethod/"
            ],
            "cwd": "${workspaceFolder}/php",
            "runtimeArgs": [
                "-d",
                "xdebug.start_with_request=yes"
            ]
        },
        {
            "name": "Debug TypeScript Tests",
            "type": "node",
            "request": "launch",
            "program": "${workspaceFolder}/typescript/node_modules/.bin/jest",
            "args": [
                "--config",
                "jest.config.js",
                "--runInBand"
            ],
            "cwd": "${workspaceFolder}/typescript",
            "console": "integratedTerminal",
            "internalConsoleOptions": "neverOpen"
        },
        {
            "name": "Debug Python Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": [
                "exercises/code-smells/long-method/tests/",
                "-v"
            ],
            "cwd": "${workspaceFolder}/python",
            "console": "integratedTerminal",
            "justMyCode": false
        }
    ]
}
```

---

## 🔍 Debugging

### PhpStorm
1. **Xdebug installieren**: `sudo apt install php-xdebug` (Linux) oder `brew install php@8.3-xdebug` (macOS)
2. **Konfiguration**: `File` → `Settings` → `PHP` → `Debug`
3. **Breakpoints setzen**: Klick auf Zeilennummer
4. **Debug starten**: ▶️ neben Run Configuration

### WebStorm
1. **Chrome DevTools**: Automatisch verfügbar
2. **Breakpoints setzen**: Klick auf Zeilennummer
3. **Debug starten**: ▶️ neben Run Configuration

### PyCharm
1. **Breakpoints setzen**: Klick auf Zeilennummer
2. **Debug starten**: 🐛 neben Run Configuration

### VS Code
1. **Extensions**: Entsprechende Debugger-Extensions installiert
2. **Breakpoints setzen**: F9 oder Klick auf Zeilennummer
3. **Debug starten**: F5 oder `Run and Debug` Panel

---

## 📊 Code Quality Tools

### PhpStorm Integration
- **PHPStan**: `File` → `Settings` → `PHP` → `Quality Tools` → `PHPStan`
  - PHPStan path: `vendor/bin/phpstan`
  - Configuration file: `phpstan.neon`
- **PHP-CS-Fixer**: `File` → `Settings` → `PHP` → `Quality Tools` → `PHP CS Fixer`
  - PHP CS Fixer path: `vendor/bin/php-cs-fixer`
  - Configuration: `.php-cs-fixer.php`

### WebStorm Integration
- **ESLint**: `File` → `Settings` → `Languages & Frameworks` → `JavaScript` → `Code Quality Tools` → `ESLint`
  - Automatic ESLint configuration ✓
- **Prettier**: `File` → `Settings` → `Languages & Frameworks` → `JavaScript` → `Prettier`
  - Prettier package: `node_modules/prettier`

### PyCharm Integration
- **Black**: `File` → `Settings` → `Tools` → `External Tools`
  - Program: `black`
  - Arguments: `$FilePath$`
- **Ruff**: External Tool similar zu Black
- **mypy**: `File` → `Settings` → `Tools` → `External Tools`

### VS Code Integration
- **Settings Sync**: Extensions konfigurieren automatisch die Tools
- **Format on Save**: In Settings aktivieren
- **Problems Panel**: Zeigt Lint-Fehler automatisch an
- **Testing**: Native Testing UI (seit v1.59) - Tests direkt im Test Explorer Panel
- **PHPStan**: `SanderRonde.phpstan-vscode` für statische Code-Analyse

---

## 🚨 Troubleshooting

### PHP - "Class not found"
```bash
cd php && composer dump-autoload
```

### TypeScript - "Module not found"
```bash
cd typescript && npm install
```

### Python - "ModuleNotFoundError"
```bash
cd python && source venv/bin/activate && pip install -r requirements.txt
```

### Tests laufen nicht
1. **Arbeitsverzeichnis prüfen**: Muss das jeweilige Sprachverzeichnis sein
2. **Dependencies installiert**: `composer install`, `npm install`, `pip install -r requirements.txt`
3. **Konfigurationsdateien vorhanden**: `phpunit.xml`, `jest.config.js`, `pytest.ini`

---

## 💡 Produktivitäts-Tipps

### Keyboard Shortcuts
- **Run Tests**: `Ctrl+Shift+F10` (IntelliJ) / `Ctrl+F5` (VS Code)
- **Debug Tests**: `Ctrl+Shift+F9` (IntelliJ) / `F5` (VS Code)
- **Refactor → Extract Method**: `Ctrl+Alt+M` (IntelliJ) / `Ctrl+Shift+R` (VS Code)
- **Format Code**: `Ctrl+Alt+L` (IntelliJ) / `Shift+Alt+F` (VS Code)

### Live Templates / Snippets
Erstellen Sie Snippets für häufige Refactoring-Patterns:
- `extract-method`
- `inline-variable`
- `rename-method`

### File Watchers (JetBrains IDEs)
- **PHP-CS-Fixer**: Automatisches Formatieren bei Dateiänderungen
- **Prettier**: Automatisches Formatieren für TypeScript
- **Black**: Automatisches Formatieren für Python