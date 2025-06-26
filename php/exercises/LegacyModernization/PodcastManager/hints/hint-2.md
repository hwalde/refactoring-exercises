# Hint 2: Schrittweise Refaktorierung und Klassen-Extraktion

## Was zu tun ist
Jetzt wo du die Probleme identifiziert hast, beginne mit der schrittweisen Refaktorierung. Arbeite iterativ und stelle sicher, dass die Tests nach jedem Schritt weiter funktionieren.

**Extrahiere separate Klassen für verschiedene Verantwortlichkeiten:**
- Welche Klasse könnte für das Parsen von RSS-Feeds zuständig sein?
- Was wäre eine sinnvolle Abstraktion für Podcast- und Episode-Daten?
- Wie könnte eine Klasse für das Speichern/Laden von Daten aussehen?
- Welche Logik gehört in einen Service für Downloads?

## Refaktorierung-Strategie
- **Extract Class**: Ziehe verwandte Methoden und Daten in eigene Klassen
- **Extract Method**: Teile lange Methoden in kleinere, fokussierte Methoden auf
- **Introduce Parameter Object**: Gruppiere zusammengehörige Daten
- **Replace Magic Numbers/Strings**: Verwende sprechende Konstanten
- **Dependency Injection**: Mache Abhängigkeiten explizit

## Worauf achten
- Führe nach jedem Refaktorierung-Schritt die Tests aus
- Ändere nur die interne Struktur, nicht das äußere Verhalten
- Verwende sprechende Namen für Klassen, Methoden und Variablen
- Halte die Klassen fokussiert - jede sollte nur eine Verantwortlichkeit haben
- Denke über Error-Handling und Exception-Design nach

## Nächster Schritt
Überlege dir wie die verschiedenen Klassen miteinander interagieren sollen. Welche Interfaces brauchst du? Wie wird die Dependency Injection aussehen? Welche Klasse orchestriert die anderen?