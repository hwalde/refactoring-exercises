# Large Class - UserManager refactorieren

**Schwierigkeit**: advanced  
**Geschätzte Zeit**: 45min  
**Konzepte**: extract-class, single-responsibility, code-smells

## Schnellstart

1. **Tests ausführen**:
   ```bash
   # TypeScript (vom refactoring-exercises/ Ordner)  
   cd typescript && npm test -- --testPathPattern="large-class"
   ```

2. **Code bearbeiten**: 
   - Dateien in `src/` Unterordner

3. **Tests erneut ausführen** (müssen grün bleiben!)

## Ziel

Refactoriere die über 300 Zeilen lange `UserManager` Klasse in kleinere, fokussierte Klassen mit jeweils einer klar definierten Verantwortlichkeit. Die Klasse übernimmt derzeit zu viele Aufgaben: Benutzerverwaltung, Authentifizierung, Autorisierung, E-Mail-Versand und Logging.

## Hilfe

- Detaillierte Beschreibung: `task.md`
- Schrittweise Hinweise: `hints/`