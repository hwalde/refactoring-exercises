# Feature Envy - OrderCalculator refactorieren

**Schwierigkeit**: advanced  
**Geschätzte Zeit**: 40min  
**Konzepte**: move-method, tell-dont-ask, feature-envy

## Schnellstart

1. **Tests ausführen**:
   ```bash
   # Python (vom refactoring-exercises/ Ordner)
   cd python && source venv/bin/activate && pytest exercises/code-smells/feature-envy/tests/ -v
   ```

2. **Code bearbeiten**: 
   - Dateien in `src/` Unterordner

3. **Tests erneut ausführen** (müssen grün bleiben!)

## Ziel

Refactoriere die `OrderCalculator` Klasse, indem du Methoden zu den Klassen verschiebst, deren Daten sie hauptsächlich verwenden. Die Klasse zeigt "Feature Envy" - ihre Methoden nutzen hauptsächlich Daten von anderen Objekten (`Order`, `Customer`, `Product`) anstatt eigene Daten.

## Hilfe

- Detaillierte Beschreibung: `task.md`
- Schrittweise Hinweise: `hints/`