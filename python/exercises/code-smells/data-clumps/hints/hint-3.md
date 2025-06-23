# Hint 3: EventManager refactorieren und finale Optimierungen

## Was zu tun ist

Jetzt geht es darum, die EventManager-Klasse zu refactorieren um die neuen Parameter Objects zu verwenden:

- **Methodensignaturen vereinfachen**: Ersetze Parameter-Listen durch Parameter Objects
- **Delegation implementieren**: Nutze die Methoden der Parameter Objects statt eigene Validierung
- **Kombinierte Objects erstellen**: Überlege, ob manche Parameter Objects zusammengehören (z.B. Adresse + Koordinaten = Location)
- **Tests anpassen**: Stelle sicher, dass alle Tests weiterhin funktionieren

## Worauf achten

- **Schrittweise vorgehen**: Refactoriere eine Methode nach der anderen
- **Tests laufen lassen**: Nach jeder Änderung sollten die Tests grün bleiben
- **Backwards Compatibility**: Überlege, ob du Adapter-Methoden für die alte API brauchst
- **Code-Duplikation entfernen**: Nutze die neuen Objects konsequent überall

## Qualitätsprüfung

Bevor du fertig bist, prüfe folgende Punkte:

- **Sind alle Data Clumps eliminiert?** Keine Methode sollte mehr dieselben Parameter-Gruppen haben
- **Ist die Validierung zentralisiert?** Jedes Parameter Object validiert sich selbst
- **Sind die Objects unveränderlich?** Verwende @dataclass(frozen=True)
- **Funktionieren alle Tests?** Sowohl die originalen als auch neue Tests für die Parameter Objects
- **Ist der Code lesbarer geworden?** Methodensignaturen sollten klarer und kürzer sein

**Finale Überlegungen:**
- Welche weiteren Methoden könnten zu den Parameter Objects gehören?
- Gibt es noch andere Code Smells, die durch die Refactorierung sichtbar werden?
- Wie würde sich der Code bei zukünftigen Änderungen verhalten?