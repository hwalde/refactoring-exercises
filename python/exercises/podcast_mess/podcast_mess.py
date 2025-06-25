# podcast_mess.py
# Ein CLI Tool zur Verwaltung von Podcasts... irgendwie.
# Geschrieben von einem Anfänger. Bitte nicht urteilen.

import sys
import os
import requests
import json
import xml.etree.ElementTree as ET
import time
from datetime import datetime

# Globale Variable für die "Datenbank". Super praktisch.
DB_FILE = 'podcasts_db.json'
# Noch mehr globale Sachen
LOG_FILE = 'activity.log'

class PodcastThing:
    def __init__(self):
        # Initialisiert das Ding mit Zeug.
        self.data = None
        self.things = []
        self.load_all_the_stuff()

    def load_all_the_stuff(self):
        # Lädt die DB, wenn sie da ist.
        # Keine Fehlerbehandlung, was soll schon schiefgehen?
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {'podcasts': [], 'episodes': []}

    # Diese Methode macht fast alles. Sehr effizient.
    def doStuff(self, command, url_or_podcast_id, extra_param=None):
        # Logik basiert auf Strings, weil das einfach ist.
        if command == 'add':
            print("Versuche, Podcast von URL hinzuzufügen...")
            try:
                # Direkte Abhängigkeit, keine Abstraktion
                resp = requests.get(url_or_podcast_id, timeout=10)
                # Magic Number: 10s Timeout
                
                # Parsen von XML direkt hier, weil warum nicht?
                podcast_xml = ET.fromstring(resp.content)
                channel = podcast_xml.find('channel')
                podcast_title = channel.find('title').text
                
                # Data Clump: Titel und URL gehören zusammen, werden aber getrennt behandelt
                new_podcast = {'id': len(self.data['podcasts']) + 1, 'title': podcast_title, 'url': url_or_podcast_id, 'tags': []}
                self.data['podcasts'].append(new_podcast)
                
                # Duplizierter Code: Speichern der DB
                with open(DB_FILE, 'w') as f:
                    json.dump(self.data, f, indent=4)
                
                print(f"Podcast '{podcast_title}' hinzugefügt!")
                with open(LOG_FILE, 'a') as log:
                    log.write(f"[{datetime.now()}] ADDED PODCAST: {podcast_title}\n")
                    
            except: # Exceptions sind lästig, einfach ignorieren.
                print("Irgendwas ist schiefgelaufen beim Hinzufügen.")
                pass

        elif command == 'download':
            print("Suche nach Episoden zum Herunterladen...")
            podcast_to_download = None
            for p in self.data['podcasts']:
                if str(p['id']) == str(url_or_podcast_id):
                    podcast_to_download = p
                    break
            
            if podcast_to_download:
                # Noch ein Netzwerk-Call...
                resp = requests.get(podcast_to_download['url'], timeout=10)
                podcast_xml = ET.fromstring(resp.content)
                
                temp_episodes = [] # Schlechter Variablenname
                
                # Monolithische Schleife: Parsen, Filtern, Herunterladen
                for item in podcast_xml.findall('.//item'):
                    episode_title = item.find('title').text
                    episode_url_element = item.find('enclosure')
                    
                    if episode_url_element is not None:
                        episode_url = episode_url_element.attrib.get('url')
                        
                        # Primitive Obsession: Alles ist ein String
                        # Shotgun Surgery: Eine Änderung hier (z.B. Dateiname) erfordert das Wissen über die gesamte Methode
                        filename = f"downloads/{podcast_to_download['title'].replace(' ', '_')}_{episode_title.replace(' ', '_')}.mp3"
                        
                        # Organisation von Dateien ist UI-Logik, sollte nicht hier sein
                        if not os.path.exists('downloads'):
                            os.makedirs('downloads')
                        
                        print(f"Lade '{episode_title}' herunter...")
                        
                        try:
                            # Feature Envy: Greift direkt auf requests zu, anstatt eine Funktion zu verwenden
                            ep_data = requests.get(episode_url, timeout=30).content
                            with open(filename, 'wb') as f:
                                f.write(ep_data)
                            
                            # Noch mehr Daten-Management
                            new_ep = {'podcast_id': podcast_to_download['id'], 'title': episode_title, 'file': filename, 'rating': 0}
                            self.data['episodes'].append(new_ep)
                            
                            with open(LOG_FILE, 'a') as log:
                                log.write(f"[{datetime.now()}] DOWNLOADED: {episode_title}\n")

                            time.sleep(1) # Magic Number: 1 Sekunde warten, um nicht gebannt zu werden?
                        except:
                            print(f"Download von '{episode_title}' fehlgeschlagen.")
                            continue # Bei Fehler einfach weitermachen

                # Duplizierter Code: Speichern der DB
                with open(DB_FILE, 'w') as f:
                    json.dump(self.data, f, indent=4)
            else:
                print("Podcast-ID nicht gefunden.")
        
        # ... diese Methode könnte noch 150 Zeilen weitergehen mit "tag", "rate", "cleanup", etc.
    
    # Eine weitere riesige Methode für andere Dinge
    def handleThings(self, action, format_type='plain'):
        if action == 'list':
            print("\n--- Abonnierte Podcasts ---")
            for p_thing in self.data['podcasts']:
                # Vermischung von Datenzugriff und Präsentation
                print(f"ID: {p_thing['id']} - {p_thing['title']} ({p_thing['url']})")
                
            print("\n--- Heruntergeladene Episoden ---")
            for e_thing in self.data['episodes']:
                p_title = "Unbekannt"
                for p_thing in self.data['podcasts']:
                    if p_thing['id'] == e_thing['podcast_id']:
                        p_title = p_thing['title']
                        break
                print(f"- {e_thing['title']} (von '{p_title}') -> Gespeichert in: {e_thing['file']}")
                
        elif action == 'export':
            # String-basierte Logik für verschiedene Formate
            # Wäre ein perfekter Fall für das Strategy Pattern
            if format_type == 'json':
                filename = 'export.json'
                with open(filename, 'w') as f:
                    # Duplizierter Code: Das ist die dritte JSON-Dump-Operation
                    json.dump(self.data, f, indent=4)
                print(f"Daten nach {filename} exportiert.")
            elif format_type == 'txt':
                filename = 'export.txt'
                with open(filename, 'w') as f:
                    # Komplett andere Logik, direkt hier implementiert
                    for p in self.data['podcasts']:
                        f.write(f"Podcast: {p['title']}\n")
                        for e in self.data['episodes']:
                            if e['podcast_id'] == p['id']:
                                f.write(f"  - Episode: {e['title']}\n")
                print(f"Daten nach {filename} exportiert.")
            else:
                print("Unbekanntes Exportformat.")
    
    # Eine schlecht benannte Methode, die etwas verarbeitet
    def processData(self, some_id, new_tag):
        # Divergent Change: Diese Klasse ändert sich, wenn das Tagging, das Herunterladen,
        # das Hinzufügen oder das Exportieren geändert wird.
        for p in self.data['podcasts']:
            if p['id'] == some_id:
                p['tags'].append(new_tag)
                print(f"Tag '{new_tag}' zu Podcast ID {some_id} hinzugefügt.")
                break
        # Wieder... duplizierter Code zum Speichern.
        with open(DB_FILE, 'w') as f:
            json.dump(self.data, f, indent=4)
            
    # Diese Methode existiert nur, weil der Name "handleThings" nicht generisch genug war.
    def makeItWork(self):
        # Repariert irgendwas, wer weiß was.
        print("Führe Wartungsarbeiten durch...")
        temp_stuff = self.data['episodes']
        cleaned_stuff = [item for item in temp_stuff if os.path.exists(item['file'])]
        
        if len(temp_stuff) != len(cleaned_stuff):
            print("Einige Episodendateien fehlten und wurden aus der DB entfernt.")
            self.data['episodes'] = cleaned_stuff
            # Und nochmal speichern!
            with open(DB_FILE, 'w') as f:
                json.dump(self.data, f, indent=4)
        else:
            print("Alles in Ordnung.")


# Hauptlogik des Skripts, direkt im globalen Scope.
# Keine Funktionen, keine Struktur.
if __name__ == "__main__":
    args = sys.argv[1:] # Direkter Zugriff auf sys.argv
    
    # Globale Instanz der God-Class
    manager_thing = PodcastThing()
    
    if not args:
        # UI-Code vermischt mit App-Logik
        print("Benutzung:")
        print("  python podcast_mess.py add <podcast_rss_url>")
        print("  python podcast_mess.py list")
        print("  python podcast_mess.py download <podcast_id>")
        print("  python podcast_mess.py export <json|txt>")
        print("  python podcast_mess.py tag <podcast_id> <tag_name>")
        print("  python podcast_mess.py cleanup")
        sys.exit(1)

    # String-basierte Steuerung des gesamten Programms
    command = args[0]
    
    if command == "add":
        if len(args) < 2:
            print("Fehler: URL fehlt.")
        else:
            url = args[1]
            manager_thing.doStuff('add', url) # Methode mit String-Flag aufrufen
    elif command == "list":
        manager_thing.handleThings('list')
    elif command == "download":
        if len(args) < 2:
            print("Fehler: Podcast-ID fehlt.")
        else:
            pid = args[1]
            manager_thing.doStuff('download', pid) # Dieselbe Methode für einen anderen Zweck
    elif command == "export":
        fmt = 'plain'
        if len(args) > 1:
            fmt = args[1]
        manager_thing.handleThings('export', fmt)
    elif command == "tag":
        if len(args) < 3:
            print("Fehler: Podcast-ID oder Tag fehlt.")
        else:
            pid = int(args[1])
            tag = args[2]
            manager_thing.processData(pid, tag) # Eine weitere Methode, die Dinge tut
    elif command == "cleanup":
        manager_thing.makeItWork() # Und noch eine...
    else:
        print(f"Unbekannter Befehl: {command}")