# TypeScript Refactoring Exercises

TypeScript 5.x Refactoring-Übungen mit Jest, ESLint und Prettier.

## Voraussetzungen

- Node.js 18+ (LTS)
- npm oder yarn
- Eine der unterstützten IDEs

## Setup

1. **Dependencies installieren**:
   ```bash
   npm install
   ```

2. **Tests ausführen** (müssen alle grün sein):
   ```bash
   npm test
   ```

## Test-Ausführung

### WebStorm
1. Rechtsklick auf `jest.config.js` → "Run 'All Tests'"
2. Oder: Run → "Edit Configurations" → "+" → "Jest" → Default configuration

### VS Code
1. **Empfohlene Extensions**:
   - TypeScript Hero
   - Jest Runner
   - ESLint
   - Prettier - Code formatter

2. **Tasks** (.vscode/tasks.json):
   ```json
   {
     "version": "2.0.0",
     "tasks": [
       {
         "label": "TypeScript: Run Tests",
         "type": "shell",
         "command": "npm test",
         "group": "test"
       },
       {
         "label": "TypeScript: Lint",
         "type": "shell", 
         "command": "npm run lint",
         "group": "build"
       }
     ]
   }
   ```

3. **Launch Configuration** (.vscode/launch.json):
   ```json
   {
     "configurations": [
       {
         "name": "Debug Jest Tests",
         "type": "node",
         "request": "launch",
         "program": "${workspaceFolder}/node_modules/.bin/jest",
         "args": ["--runInBand"],
         "console": "integratedTerminal",
         "internalConsoleOptions": "neverOpen"
       }
     ]
   }
   ```

### Kommandozeile

#### Linux (Bash)
```bash
# Tests ausführen
npm test

# Tests im Watch-Modus
npm run test:watch

# Tests mit Coverage
npm run test:coverage

# Linting
npm run lint

# Linting mit Auto-Fix
npm run lint:fix

# Code formatieren
npm run format

# Code-Format prüfen
npm run format:check

# Type-Checking
npm run typecheck
```

#### Windows (PowerShell)
```powershell
# Tests ausführen
npm test

# Tests im Watch-Modus
npm run test:watch

# Tests mit Coverage
npm run test:coverage

# Linting
npm run lint

# Linting mit Auto-Fix
npm run lint:fix

# Code formatieren
npm run format

# Code-Format prüfen
npm run format:check

# Type-Checking
npm run typecheck
```

## Arbeitsweise

1. **Aufgabe auswählen**: Wechsle in einen Aufgaben-Ordner (z.B. `exercises/code-smells/long-method/`)
2. **Tests ausführen**: `npm test exercises/code-smells/long-method/tests/`
3. **Code refactorieren**: Ändere Dateien in `src/`
4. **Tests erneut ausführen**: Stelle sicher, dass sie grün bleiben

## Code-Qualität

- **Strict Mode**: Aktiviert für maximale Typsicherheit
- **ESLint**: Erweiterte Linting-Regeln
- **Prettier**: Einheitliche Code-Formatierung
- **100% Type Coverage**: Kein `any` erlaubt

## Debugging

### WebStorm
- Breakpoints setzen und "Debug" statt "Run" wählen
- Jest-Integration automatisch verfügbar

### VS Code
- Jest Extension für Test-Debugging
- Launch Configuration verwenden (siehe oben)
- F5 für Debug-Start

## Troubleshooting

### "Module not found" Fehler
```bash
rm -rf node_modules package-lock.json
npm install
```

### TypeScript Compilation Fehler
```bash
npm run typecheck
```

### Node.js/npm Version prüfen
```bash
node --version
npm --version
```

### Jest Cache leeren
```bash
npx jest --clearCache
```