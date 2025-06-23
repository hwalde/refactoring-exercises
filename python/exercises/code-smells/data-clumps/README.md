# Data Clumps refactorieren

**Schwierigkeit**: advanced  
**Geschätzte Zeit**: 45min  
**Konzepte**: data-clumps, parameter-object, value-objects, tell-dont-ask

## Schnellstart

1. **Tests ausführen**:
   ```bash
   # Python (vom refactoring-exercises/ Ordner)
   cd python && source venv/bin/activate && pytest exercises/code-smells/data-clumps/tests/ -v
   ```

2. **Code bearbeiten**: 
   - Python: Dateien in `src/` Unterordner

3. **Tests erneut ausführen** (müssen grün bleiben!)

## Ziel

Refactoriere eine EventManager-Klasse, die unter Data Clumps leidet, indem du wiederkehrende Parameter-Gruppen in Parameter Objects kapselst. Lerne das Parameter Object Pattern und das Tell-Don't-Ask Prinzip anzuwenden.

## Hilfe

- Detaillierte Beschreibung: `task.md`
- Schrittweise Hinweise: `hints/`