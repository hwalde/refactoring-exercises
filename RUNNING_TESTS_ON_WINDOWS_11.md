# Tests mit PowerShell ausführen (Windows)

## TypeScript

```powershell
cd typescript
npm install
# Beispiel für long-method exercise:
npm test exercises/code-smells/long-method/tests/
# Für andere exercises entsprechend den Pfad anpassen
```

## PHP

```powershell
cd php
composer install
# Beispiel für LongMethod exercise:
vendor\bin\phpunit.bat exercises\CodeSmells\LongMethod\
# Für andere exercises entsprechend den Pfad anpassen
```

## Python

```powershell
cd python
python -m venv venv
.\venv\Scripts\Activate.ps1
python.exe -m pip install --upgrade pip
pip install pytest
# Beispiel für long-method exercise:
pytest exercises/code-smells/long-method/tests/
# Für andere exercises entsprechend den Pfad anpassen
```