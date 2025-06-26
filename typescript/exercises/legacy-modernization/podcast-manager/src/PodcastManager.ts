// podcast_mess.ts
// Ein CLI Tool zur Verwaltung von Podcasts... irgendwie in TypeScript.
// Geschrieben von einem Anfänger, der "any" liebt.

import * as fs from 'fs';
import * as path from 'path';
import axios from 'axios';
import { parseStringPromise } from 'xml2js';
import { exit } from 'process';

// Globale Konstanten sind super, besonders für Dateipfade.
const DB_FILE = path.join(process.cwd(), 'podcasts_db.json');
const LOG_FILE = path.join(process.cwd(), 'activity.log');

class PodcastThing {
    // TypeScript? Ja, aber "any" ist mein Lieblingstyp. Maximale Flexibilität!
    // So muss ich mir keine Gedanken über Interfaces oder Typen machen.
    private data: any;

    constructor() {
        this.data = null; // Erstmal null, wird dann geladen.
        this.load_all_the_stuff();
    }

    private load_all_the_stuff() {
        // Lädt die DB synchron. Blockiert den Event-Loop, aber ist einfacher zu schreiben.
        // Was soll schon schiefgehen?
        try {
            if (fs.existsSync(DB_FILE)) {
                const fileContent = fs.readFileSync(DB_FILE, 'utf-8');
                this.data = JSON.parse(fileContent);
            } else {
                this.data = { podcasts: [], episodes: [] };
            }
        } catch (e) {
            console.log("Fehler beim Laden der DB, erstelle eine neue.");
            this.data = { podcasts: [], episodes: [] };
        }
    }

    // Diese Methode macht fast alles. Sehr effizient. Async/await macht es modern.
    public async doStuff(command: string, urlOrPodcastId: string, _extraParam: string | null = null): Promise<void> {
        // Logik basiert auf Strings, weil Enums zu kompliziert sind.
        if (command === 'add') {
            console.log("Versuche, Podcast von URL hinzuzufügen...");
            try {
                // Direkte Abhängigkeit, keine Abstraktion
                const resp = await axios.get(urlOrPodcastId, { timeout: 10000 }); // Magic Number: 10s Timeout

                // Parsen von XML direkt hier, weil warum nicht?
                const podcastXml = await parseStringPromise(resp.data);
                
                // Tiefe Verschachtelung und unsichere Zugriffe. 'any' macht's möglich.
                const channel = podcastXml.rss.channel[0];
                const podcastTitle = channel.title[0];

                // Data Clump: Titel und URL gehören zusammen, werden aber getrennt behandelt
                const newPodcast = { id: this.data.podcasts.length + 1, title: podcastTitle, url: urlOrPodcastId, tags: [] };
                this.data.podcasts.push(newPodcast);

                // Duplizierter Code: Speichern der DB
                fs.writeFileSync(DB_FILE, JSON.stringify(this.data, null, 4));
                
                console.log(`Podcast '${podcastTitle}' hinzugefügt!`);
                // Duplizierter Logging-Code
                fs.appendFileSync(LOG_FILE, `[${new Date().toISOString()}] ADDED PODCAST: ${podcastTitle}\n`);

            } catch (e: any) { // Exceptions sind lästig, einfach eine Nachricht ausgeben.
                console.log("Irgendwas ist schiefgelaufen beim Hinzufügen.", e.message);
            }

        } else if (command === 'download') {
            console.log("Suche nach Episoden zum Herunterladen...");
            const podcastToDownload = this.data.podcasts.find((p: any) => String(p.id) === String(urlOrPodcastId));
            
            if (podcastToDownload) {
                // Noch ein Netzwerk-Call...
                const resp = await axios.get(podcastToDownload.url, { timeout: 10000 });
                const podcastXml = await parseStringPromise(resp.data);
                
                // const _tempEpisodes: any[] = []; // Schlechter Variablenname - entfernt da ungenutzt
                
                // Monolithische Schleife: Parsen, Filtern, Herunterladen
                for (const item of podcastXml.rss.channel[0].item) {
                    const episodeTitle = item.title[0];
                    const episodeUrlElement = item.enclosure?.[0];
                    
                    if (episodeUrlElement) {
                        const episodeUrl = episodeUrlElement.$.url;
                        
                        // Primitive Obsession: Alles ist ein String
                        // Shotgun Surgery: Eine Änderung hier (z.B. Dateiname) erfordert Wissen über die gesamte Methode
                        const filename = `downloads/${podcastToDownload.title.replace(/\s/g, '_')}_${episodeTitle.replace(/\s/g, '_')}.mp3`;
                        
                        // Organisation von Dateien ist UI-Logik, sollte nicht hier sein
                        if (!fs.existsSync('downloads')) {
                            fs.mkdirSync('downloads');
                        }
                        
                        console.log(`Lade '${episodeTitle}' herunter...`);
                        
                        try {
                            // Feature Envy: Greift direkt auf axios zu, anstatt eine Funktion zu verwenden
                            const epData = await axios.get(episodeUrl, { timeout: 30000, responseType: 'arraybuffer' });
                            fs.writeFileSync(filename, epData.data);
                            
                            // Noch mehr Daten-Management
                            const newEp = { podcast_id: podcastToDownload.id, title: episodeTitle, file: filename, rating: 0 };
                            this.data.episodes.push(newEp);
                            
                            fs.appendFileSync(LOG_FILE, `[${new Date().toISOString()}] DOWNLOADED: ${episodeTitle}\n`);
                            
                            // Warten, einfach so.
                            await new Promise(resolve => setTimeout(resolve, 1000)); // Magic Number
                        } catch (err) {
                            console.log(`Download von '${episodeTitle}' fehlgeschlagen.`);
                            continue; // Bei Fehler einfach weitermachen
                        }
                    }
                }

                // Duplizierter Code: Speichern der DB
                fs.writeFileSync(DB_FILE, JSON.stringify(this.data, null, 4));
            } else {
                console.log("Podcast-ID nicht gefunden.");
            }
        }
    }
    
    // Eine weitere riesige Methode für andere Dinge
    public handleThings(action: string, formatType: string = 'plain'): void {
        if (action === 'list') {
            console.log("\n--- Abonnierte Podcasts ---");
            for (const pThing of this.data.podcasts) {
                // Vermischung von Datenzugriff und Präsentation
                console.log(`ID: ${pThing.id} - ${pThing.title} (${pThing.url})`);
            }
            
            console.log("\n--- Heruntergeladene Episoden ---");
            for (const eThing of this.data.episodes) {
                const pTitle = this.data.podcasts.find((p: any) => p.id === eThing.podcast_id)?.title || "Unbekannt";
                console.log(`- ${eThing.title} (von '${pTitle}') -> Gespeichert in: ${eThing.file}`);
            }
        } else if (action === 'export') {
            // String-basierte Logik für verschiedene Formate
            // Wäre ein perfekter Fall für das Strategy Pattern
            if (formatType === 'json') {
                const filename = 'export.json';
                // Duplizierter Code: Das ist die dritte JSON-Schreib-Operation
                fs.writeFileSync(filename, JSON.stringify(this.data, null, 4));
                console.log(`Daten nach ${filename} exportiert.`);
            } else if (formatType === 'txt') {
                const filename = 'export.txt';
                let content = '';
                for (const p of this.data.podcasts) {
                    content += `Podcast: ${p.title}\n`;
                    for (const e of this.data.episodes) {
                        if (e.podcast_id === p.id) {
                            content += `  - Episode: ${e.title}\n`;
                        }
                    }
                }
                fs.writeFileSync(filename, content);
                console.log(`Daten nach ${filename} exportiert.`);
            } else {
                console.log("Unbekanntes Exportformat.");
            }
        }
    }

    // Eine schlecht benannte Methode, die etwas verarbeitet
    public processData(someId: number, newTag: string): void {
        // Divergent Change: Diese Klasse ändert sich bei jeder Kleinigkeit.
        const p = this.data.podcasts.find((p: any) => p.id === someId);
        if (p) {
            p.tags.push(newTag);
            console.log(`Tag '${newTag}' zu Podcast ID ${someId} hinzugefügt.`);
        }
        // Wieder... duplizierter Code zum Speichern.
        fs.writeFileSync(DB_FILE, JSON.stringify(this.data, null, 4));
    }
    
    // Diese Methode existiert nur, weil der Name "handleThings" nicht generisch genug war.
    public makeItWork(): void {
        console.log("Führe Wartungsarbeiten durch...");
        const originalCount = this.data.episodes.length;
        // Filtert Einträge, deren Datei nicht mehr existiert
        this.data.episodes = this.data.episodes.filter((item: any) => fs.existsSync(item.file));
        
        if (originalCount !== this.data.episodes.length) {
            console.log("Einige Episodendateien fehlten und wurden aus der DB entfernt.");
            // Und nochmal speichern!
            fs.writeFileSync(DB_FILE, JSON.stringify(this.data, null, 4));
        } else {
            console.log("Alles in Ordnung.");
        }
    }
}

// Hauptlogik des Skripts, direkt im globalen Scope, in einer IIFE wegen top-level await.
(async () => {
    // Direkter Zugriff auf process.argv
    const args = process.argv.slice(2);
    
    // Globale Instanz der God-Class
    const managerThing = new PodcastThing();
    
    if (args.length === 0) {
        // UI-Code vermischt mit App-Logik
        console.log("Benutzung:");
        console.log("  npx ts-node src/PodcastManager.ts add <podcast_rss_url>");
        console.log("  npx ts-node src/PodcastManager.ts list");
        console.log("  npx ts-node src/PodcastManager.ts download <podcast_id>");
        console.log("  npx ts-node src/PodcastManager.ts export <json|txt>");
        console.log("  npx ts-node src/PodcastManager.ts tag <podcast_id> <tag_name>");
        console.log("  npx ts-node src/PodcastManager.ts cleanup");
        exit(1);
    }
    
    // String-basierte Steuerung des gesamten Programms
    const command = args[0];
    
    switch (command) {
        case "add":
            if (args.length < 2) {
                console.log("Fehler: URL fehlt.");
            } else {
                await managerThing.doStuff('add', args[1]!); // Methode mit String-Flag aufrufen
            }
            break;
        case "list":
            managerThing.handleThings('list');
            break;
        case "download":
            if (args.length < 2) {
                console.log("Fehler: Podcast-ID fehlt.");
            } else {
                await managerThing.doStuff('download', args[1]!); // Dieselbe Methode für einen anderen Zweck
            }
            break;
        case "export":
            managerThing.handleThings('export', args[1] || 'txt');
            break;
        case "tag":
            if (args.length < 3) {
                console.log("Fehler: Podcast-ID oder Tag fehlt.");
            } else {
                managerThing.processData(parseInt(args[1]!, 10), args[2]!); // Eine weitere Methode
            }
            break;
        case "cleanup":
            managerThing.makeItWork(); // Und noch eine...
            break;
        default:
            console.log(`Unbekannter Befehl: ${command}`);
    }
})();