# Hint 3: Modelliere Status-Übergänge und vervollständige das Refactoring

## Was zu tun ist

- Analysiere die komplexesten Geschäftsregeln: Status-Übergänge und ihre Validierung
- Verstehe die Status-Zustandsmaschine bevor du implementierst
- Führe ein finales Review durch, um sicherzustellen, dass keine Primitive Obsession mehr existiert

## Status-Analyse-Fragen

**Erlaubte Status-Werte entdecken:**
- **Welche Status-Strings** kommen im Code und in den Tests vor?
- **Wo wird Status-Validierung** bereits gemacht? (Schaue in `updateInvoiceStatus`)
- **Was ist der Standard-Status** für neue Rechnungen?

**Status-Übergänge verstehen:**
- **Von welchen Status** kann zu welchen anderen gewechselt werden?
- **Gibt es End-Status**, von denen kein Übergang mehr möglich ist?
- **Welche Übergänge sind Einbahnstraßen** (z.B. von paid zurück zu draft)?
- **Zeichne ein Zustandsdiagramm** der erlaubten Übergänge!

## Denkfragen für InvoiceStatus Design

- **Soll InvoiceStatus nur Validierung** machen oder auch die Übergangs-Logik kapseln?
- **Braucht es Factory-Methoden** für häufig verwendete Status?
- **Wie kompliziert ist die Übergangs-Validierung?** Eine einfache Liste oder komplexere Regeln?
- **Welche Exception-Message** wird bei ungültigen Übergängen erwartet?

## Worauf achten

- **State Machine Pattern**: Status-Übergänge sind klassisches Anwendungsgebiet für Zustandsmaschinen
- **Immutable Objects**: Status-Änderungen sollten neue Objekte erzeugen, nicht bestehende mutieren
- **Business Rules**: Die Übergangsregeln sind Geschäftslogik - sie gehören ins Value Object!
- **Testing Strategy**: Status-Übergänge haben viele Edge-Cases - teste alle Kombinationen

## Finales Refactoring-Review

**Vollständigkeits-Check:**
- Gibt es noch primitive Typen, die Domänen-Konzepte repräsentieren?
- Sind alle Validierungsregeln aus der Hauptklasse in Value Objects gewandert?
- Haben alle Value Objects sinnvolle `equals()` Methoden?
- Sind alle Value Objects immutable?

**Qualitäts-Check:**
- Laufen alle Tests noch durch?
- Ist der Code expresssiver und typsicherer geworden?
- Sind die Exception-Messages identisch zum Original?

## Nächster Schritt

Vervollständige das Refactoring und führe eine Gesamt-Review durch. Frage dich: Würde ein neuer Entwickler die Geschäftsregeln jetzt schneller verstehen?