# Hint 1: Data Clumps identifizieren

## Was zu tun ist

Beginne mit der Analyse der EventManager-Klasse und identifiziere die wiederkehrenden Parameter-Gruppen:

- **Zeitbezogene Parameter**: Welche Parameter tauchen immer zusammen auf, wenn es um Termine geht?
- **Ortsbezogene Parameter**: Welche Parameter beschreiben zusammen einen Ort?
- **Kontaktbezogene Parameter**: Welche Parameter bilden zusammen Kontaktinformationen?

Schaue dir besonders die Methodensignaturen an - Parameter, die immer zusammen auftreten, sind Kandidaten für Parameter Objects.

## Worauf achten

- **Validierung**: Wird die gleiche Validierung für bestimmte Parameter-Gruppen mehrfach durchgeführt?
- **Logische Zusammengehörigkeit**: Welche Parameter ergeben fachlich eine Einheit?
- **Wiederholung**: Wo siehst du dieselben Parameter-Kombinationen in verschiedenen Methoden?

## Nächster Schritt

Erstelle eine Liste der identifizierten Parameter-Gruppen und überlege dir sinnvolle Klassennamen für diese Gruppen. Denke dabei an die fachliche Bedeutung, nicht an die technische Implementierung.

**Fragen zum Nachdenken:**
- Wie oft kommen `date`, `startTime`, `endTime`, `timezone` zusammen vor?
- Was haben `street`, `city`, `country`, `postalCode` gemeinsam?
- Warum werden `latitude` und `longitude` immer zusammen verwendet?