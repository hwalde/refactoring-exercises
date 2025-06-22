# Python Refactoring Exercises

Python 3.11+ Refactoring-Übungen mit pytest, Black, Ruff und mypy.

## Voraussetzungen

- Python 3.11 oder höher
- pip oder poetry
- Eine der unterstützten IDEs

## Setup

1. **Virtual Environment erstellen** (empfohlen):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # oder
   venv\Scripts\activate     # Windows
   ```

2. **Dependencies installieren**:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Tests ausführen** (müssen alle grün sein):
   ```bash
   pytest
   ```

## Test-Ausführung

### PyCharm Professional
1. Rechtsklick auf `pytest.ini` → "Run 'pytest in ...'"
2. Oder: Run → "Edit Configurations" → "+" → "Python tests" → "pytest"

### VS Code
1. **Empfohlene Extensions**:
   - Python (ms-python.python - enthält Testing-Support)
   - Pylance
   - Black Formatter (ms-python.black-formatter)
   - Ruff (charliermarsh.ruff)
   - Mypy Type Checker (ms-python.mypy-type-checker)

2. **Testing**: VS Code native Testing UI (seit v1.59) automatisch verfügbar

3. **Settings** (.vscode/settings.json):
   ```json
   {
     "python.testing.pytestEnabled": true,
     "python.testing.unittestEnabled": false,
     "python.defaultInterpreterPath": "./venv/bin/python"
   }
   ```

4. **Launch Configuration** (.vscode/launch.json):
   ```json
   {
     "configurations": [
       {
         "name": "Debug pytest",
         "type": "python",
         "request": "launch",
         "module": "pytest",
         "args": ["-v"],
         "console": "integratedTerminal"
       }
     ]
   }
   ```

### Kommandozeile

#### Linux (Bash)
```bash
# Tests ausführen
pytest

# Tests mit Coverage
pytest --cov=exercises --cov-report=html

# Spezifische Tests
pytest exercises/code-smells/long-method/tests/

# Tests im Watch-Modus (mit pytest-watch)
pip install pytest-watch
ptw

# Code formatieren
black exercises/

# Code-Format prüfen
black --check exercises/

# Linting
ruff exercises/

# Linting mit Auto-Fix
ruff --fix exercises/

# Type-Checking
mypy exercises/
```

#### Windows (PowerShell)
```powershell
# Tests ausführen
pytest

# Tests mit Coverage
pytest --cov=exercises --cov-report=html

# Spezifische Tests
pytest exercises/code-smells/long-method/tests/

# Code formatieren
black exercises/

# Code-Format prüfen
black --check exercises/

# Linting
ruff exercises/

# Linting mit Auto-Fix
ruff --fix exercises/

# Type-Checking
mypy exercises/
```

## Arbeitsweise

1. **Aufgabe auswählen**: Wechsle in einen Aufgaben-Ordner (z.B. `exercises/code-smells/long-method/`)
2. **Tests ausführen**: `pytest exercises/code-smells/long-method/tests/`
3. **Code refactorieren**: Ändere Dateien in `src/`
4. **Tests erneut ausführen**: Stelle sicher, dass sie grün bleiben

## Code-Qualität

- **Type Hints**: Vollständige Typisierung mit mypy strict mode
- **Black**: Automatische Code-Formatierung
- **Ruff**: Schneller Linter (Ersetzt flake8, isort, etc.)
- **pytest**: Moderne Test-Framework mit Fixtures

## Debugging

### PyCharm
- Breakpoints setzen und "Debug" statt "Run" wählen
- pytest-Integration automatisch verfügbar

### VS Code
- Python Extension für Debugging
- Launch Configuration verwenden (siehe oben)
- F5 für Debug-Start

## Troubleshooting

### "Module not found" Fehler
```bash
pip install -e ".[dev]"
# oder
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Virtual Environment Probleme
```bash
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Python Version prüfen
```bash
python --version
pip --version
```

### pytest Cache leeren
```bash
pytest --cache-clear
```

### Package Installation im Development Mode
```bash
# Editierbare Installation für lokale Entwicklung
pip install -e ".[dev]"
```