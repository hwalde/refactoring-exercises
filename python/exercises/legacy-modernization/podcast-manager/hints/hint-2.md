# Hint 2: Schrittweise Refaktorierung und Architektur-Design

## Was zu tun ist
Jetzt, da Sie die Code-Smells identifiziert haben, beginnen Sie mit der schrittweisen Refaktorierung. Arbeiten Sie sich von innen nach außen vor.

**Extraktions-Strategie:**
- Beginnen Sie mit Domain-Modellen (Value Objects)
- Extrahieren Sie dann Service-Klassen
- Trennen Sie Infrastructure von Domain-Logik
- Refaktorieren Sie die CLI-Schnittstelle zum Schluss

## Domain-Modelle erstellen
Welche Konzepte der realen Welt werden in Ihrem Code repräsentiert?
- Was macht einen Podcast aus? (ID, Titel, URL, Tags)
- Was definiert eine Episode? (Titel, Datei-Pfad, Podcast-Zugehörigkeit)
- Verwenden Sie `@dataclass` für diese Strukturen

## Service-Klassen identifizieren
Welche Geschäftsoperationen lassen sich gruppieren?
- RSS-Feed parsen und Podcasts extrahieren
- Episodes herunterladen und speichern
- Daten exportieren (verschiedene Formate)
- Aktivitäten protokollieren

## Infrastructure abstrahieren
Welche externen Abhängigkeiten können Sie kapseln?
- Datei-System-Operationen (JSON speichern/laden)
- HTTP-Requests für RSS-Feeds und Downloads
- Logging-Mechanismus

## Worauf achten
- Führen Sie nach jedem Refaktorierungs-Schritt die Tests aus
- Ändern Sie das äußere Verhalten nicht
- Nutzen Sie Dependency Injection für bessere Testbarkeit
- Behandeln Sie Fehler spezifisch, nicht mit blanken `except:` Blöcken

## Python-Best-Practices
- Verwenden Sie Type Hints für alle Parameter und Rückgabewerte
- Nutzen Sie `Protocol` für Interface-Definition wenn nötig
- Implementieren Sie `__str__` und `__repr__` für Debug-Ausgaben

## Nächster Schritt
Beginnen Sie mit der Erstellung von `Podcast` und `Episode` Dataclasses. Überlegen Sie, welche Validierung diese benötigen und wie sie sich verhalten sollen.