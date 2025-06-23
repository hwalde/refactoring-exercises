# Hint 3: Finalisierung und Qualitätsprüfung

## Was zu tun ist

Du solltest jetzt die meisten Duplikationen eliminiert haben. Zeit für die finale Politur und Qualitätsprüfung:

**Methodennamen überprüfen:**
- Sind alle extrahierten Methoden aussagekräftig benannt?
- Verraten die Namen was die Methode tut, ohne in den Code schauen zu müssen?
- Folgen die Namen den PHP-Konventionen (camelCase)?

**Parameter-Design bewerten:**
- Haben deine Methoden eine sinnvolle Anzahl Parameter? (nicht zu viele)
- Sind die Parameter klar verständlich und gut getypt?
- Könntest du verwandte Parameter in ein Array oder Objekt gruppieren?

**Template Method Pattern erwägen:**
- Hast du ähnliche Algorithmen mit verschiedenen Schritten gefunden?
- Könnte eine Template-Methode den gemeinsamen Ablauf definieren?
- Welche Schritte sind fix, welche könnten als abstrakte/überschreibbare Methoden definiert werden?

## Worauf achten

- **DRY vs. Klarheit**: Manchmal ist etwas Duplikation besser als überabstrahierter Code
- **Single Responsibility**: Jede extrahierte Methode sollte eine klar definierte Aufgabe haben
- **Testbarkeit**: Sind die neuen Methoden gut testbar? (Falls nötig, private → protected für Tests)
- **Code-Stil**: PSR-12 Konventionen einhalten, Type Declarations verwenden

## Nächster Schritt

**Qualitätssicherung durchführen:**

1. **Tests laufen lassen**: Alle bestehenden Tests müssen grün bleiben
2. **Code-Stil prüfen**: php-cs-fixer sollte keine Probleme finden
3. **Static Analysis**: PHPStan sollte ohne Warnungen durchlaufen
4. **Code Review**: Lese deinen refactorierten Code durch - ist er verständlicher als vorher?

**Finale Überprüfung:**
- Ist der Code DRYer (weniger Duplikation) geworden?
- Ist der Code trotzdem noch verständlich und wartbar?
- Haben die extrahierten Methoden aussagekräftige Namen?
- Sind die Abstraktionen gerechtfertigt oder hast du überabstrahiert?

Wenn alles grün ist und der Code sauberer aussieht - herzlichen Glückwunsch! Du hast erfolgreich Duplicate Code refactoriert.