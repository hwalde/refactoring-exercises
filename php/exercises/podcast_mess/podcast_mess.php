<?php
// podcast_mess.php
// Ein CLI Tool zur Verwaltung von Podcasts... auf die PHP-Art.
// Geschrieben von jemandem, der prozeduralen Stil in Klassen liebt.

// Globale Konstanten sind super praktisch. Niemand wird sie je ändern müssen.
define('DB_FILE', __DIR__ . '/podcasts_db.json');
define('LOG_FILE', __DIR__ . '/activity.log');

class PodcastThing {
    // Alles ist public, weil Kapselung überbewertet wird.
    public $data;

    public function __construct() {
        $this->data = null;
        $this->load_all_the_stuff();
    }

    private function load_all_the_stuff() {
        // Lädt die DB. Der @-Operator unterdrückt Fehler. Sehr praktisch, dann muss man kein try-catch schreiben.
        if (file_exists(DB_FILE)) {
            $fileContent = @file_get_contents(DB_FILE);
            $this->data = json_decode($fileContent, true); // true für assoziatives Array
        }
        
        // Wenn $this->data immer noch nicht gesetzt ist, initialisieren wir es.
        // Schwache Typisierung und Null-Werte machen das einfach.
        if (!$this->data) {
            $this->data = ['podcasts' => [], 'episodes' => []];
        }
    }

    // Diese Methode macht fast alles. Sehr effizient.
    public function doStuff($command, $url_or_podcast_id, $extra_param = null) {
        // Logik basiert auf Strings, weil das einfach ist.
        if ($command === 'add') {
            echo "Versuche, Podcast von URL hinzuzufügen...\n";
            // Direkte Abhängigkeit, keine Abstraktion. @ unterdrückt wieder Fehler.
            $xmlString = @file_get_contents($url_or_podcast_id);
            
            if ($xmlString === false) {
                echo "Konnte die URL nicht abrufen.\n";
                return;
            }

            // Parsen von XML direkt hier, weil warum nicht?
            $podcast_xml = @simplexml_load_string($xmlString);
            if ($podcast_xml === false) {
                echo "Konnte XML nicht parsen.\n";
                return;
            }

            $podcast_title = (string) $podcast_xml->channel->title;

            // Data Clump: Titel und URL gehören zusammen, werden aber getrennt behandelt
            $new_podcast = [
                'id' => count($this->data['podcasts']) + 1,
                'title' => $podcast_title,
                'url' => $url_or_podcast_id,
                'tags' => []
            ];
            $this->data['podcasts'][] = $new_podcast;

            // Duplizierter Code: Speichern der DB
            file_put_contents(DB_FILE, json_encode($this->data, JSON_PRETTY_PRINT));
            
            echo "Podcast '{$podcast_title}' hinzugefügt!\n";
            // Duplizierter Logging-Code
            file_put_contents(LOG_FILE, "[" . date('c') . "] ADDED PODCAST: {$podcast_title}\n", FILE_APPEND);

        } elseif ($command === 'download') {
            echo "Suche nach Episoden zum Herunterladen...\n";
            $podcast_to_download = null;
            foreach ($this->data['podcasts'] as $p) {
                if ((string)$p['id'] === (string)$url_or_podcast_id) {
                    $podcast_to_download = $p;
                    break;
                }
            }
            
            if ($podcast_to_download) {
                $xmlString = @file_get_contents($podcast_to_download['url']);
                $podcast_xml = @simplexml_load_string($xmlString);
                
                // Monolithische Schleife: Parsen, Filtern, Herunterladen
                foreach ($podcast_xml->channel->item as $item) {
                    $episode_title = (string) $item->title;
                    // Zugriff auf Attribute mit unsicherem Chaining
                    $episode_url = (string) $item->enclosure['url'];
                    
                    if (!empty($episode_url)) {
                        // Primitive Obsession: Alles ist ein String
                        // Shotgun Surgery: Eine Änderung hier (z.B. Dateiname) erfordert Wissen über die gesamte Methode
                        $filename = 'downloads/' . str_replace(' ', '_', $podcast_to_download['title']) . '_' . str_replace(' ', '_', $episode_title) . '.mp3';
                        
                        // Organisation von Dateien ist UI-Logik, sollte nicht hier sein
                        if (!is_dir('downloads')) {
                            mkdir('downloads');
                        }
                        
                        echo "Lade '{$episode_title}' herunter...\n";
                        
                        // Feature Envy: Greift direkt auf file_get_contents zu
                        $ep_data = @file_get_contents($episode_url);
                        if ($ep_data) {
                            file_put_contents($filename, $ep_data);
                            
                            $new_ep = [
                                'podcast_id' => $podcast_to_download['id'],
                                'title' => $episode_title,
                                'file' => $filename,
                                'rating' => 0
                            ];
                            $this->data['episodes'][] = $new_ep;
                            
                            file_put_contents(LOG_FILE, "[" . date('c') . "] DOWNLOADED: {$episode_title}\n", FILE_APPEND);
                            sleep(1); // Magic Number: Warten, einfach so.
                        } else {
                            echo "Download von '{$episode_title}' fehlgeschlagen.\n";
                            continue;
                        }
                    }
                }

                // Duplizierter Code: Speichern der DB
                file_put_contents(DB_FILE, json_encode($this->data, JSON_PRETTY_PRINT));
            } else {
                echo "Podcast-ID nicht gefunden.\n";
            }
        }
    }
    
    // Eine weitere riesige Methode für andere Dinge
    public function handleThings($action, $format_type = 'plain') {
        if ($action === 'list') {
            echo "\n--- Abonnierte Podcasts ---\n";
            foreach ($this->data['podcasts'] as $p_thing) {
                // Vermischung von Datenzugriff und Präsentation
                echo "ID: {$p_thing['id']} - {$p_thing['title']} ({$p_thing['url']})\n";
            }
            
            echo "\n--- Heruntergeladene Episoden ---\n";
            foreach ($this->data['episodes'] as $e_thing) {
                $p_title = "Unbekannt";
                foreach ($this->data['podcasts'] as $p_thing) {
                    if ($p_thing['id'] == $e_thing['podcast_id']) {
                        $p_title = $p_thing['title'];
                        break;
                    }
                }
                echo "- {$e_thing['title']} (von '{$p_title}') -> Gespeichert in: {$e_thing['file']}\n";
            }
        } elseif ($action === 'export') {
            // String-basierte Logik für verschiedene Formate
            if ($format_type === 'json') {
                $filename = 'export.json';
                // Duplizierter Code: Das ist die dritte JSON-Schreib-Operation
                file_put_contents($filename, json_encode($this->data, JSON_PRETTY_PRINT));
                echo "Daten nach {$filename} exportiert.\n";
            } elseif ($format_type === 'txt') {
                $filename = 'export.txt';
                $content = '';
                foreach ($this->data['podcasts'] as $p) {
                    $content .= "Podcast: {$p['title']}\n";
                    foreach ($this->data['episodes'] as $e) {
                        if ($e['podcast_id'] == $p['id']) {
                            $content .= "  - Episode: {$e['title']}\n";
                        }
                    }
                }
                file_put_contents($filename, $content);
                echo "Daten nach {$filename} exportiert.\n";
            } else {
                echo "Unbekanntes Exportformat.\n";
            }
        }
    }

    // Eine schlecht benannte Methode, die etwas verarbeitet
    public function processData($some_id, $new_tag) {
        foreach ($this->data['podcasts'] as &$p) { // Referenz (&) um direkt zu ändern, super undurchsichtig.
            if ($p['id'] == $some_id) {
                $p['tags'][] = $new_tag;
                echo "Tag '{$new_tag}' zu Podcast ID {$some_id} hinzugefügt.\n";
                break;
            }
        }
        // Wieder... duplizierter Code zum Speichern.
        file_put_contents(DB_FILE, json_encode($this->data, JSON_PRETTY_PRINT));
    }
    
    // Diese Methode existiert nur, weil der Name "handleThings" nicht generisch genug war.
    public function makeItWork() {
        echo "Führe Wartungsarbeiten durch...\n";
        $original_count = count($this->data['episodes']);
        
        $cleaned_stuff = array_filter($this->data['episodes'], function($item) {
            return file_exists($item['file']);
        });
        
        if ($original_count !== count($cleaned_stuff)) {
            echo "Einige Episodendateien fehlten und wurden aus der DB entfernt.\n";
            $this->data['episodes'] = array_values($cleaned_stuff); // re-index array
            // Und nochmal speichern!
            file_put_contents(DB_FILE, json_encode($this->data, JSON_PRETTY_PRINT));
        } else {
            echo "Alles in Ordnung.\n";
        }
    }
}

// Hauptlogik des Skripts, direkt im globalen Scope.
// $argv ist eine superglobale Variable, immer verfügbar.
if ($argc <= 1) {
    // UI-Code vermischt mit App-Logik
    echo "Benutzung:\n";
    echo "  php " . basename(__FILE__) . " add <podcast_rss_url>\n";
    echo "  php " . basename(__FILE__) . " list\n";
    echo "  php " . basename(__FILE__) . " download <podcast_id>\n";
    echo "  php " . basename(__FILE__) . " export <json|txt>\n";
    echo "  php " . basename(__FILE__) . " tag <podcast_id> <tag_name>\n";
    echo "  php " . basename(__FILE__) . " cleanup\n";
    exit(1);
}

// Globale Instanz der God-Class
$manager_thing = new PodcastThing();
$command = $argv[1];

// String-basierte Steuerung des gesamten Programms
switch ($command) {
    case "add":
        if ($argc < 3) {
            echo "Fehler: URL fehlt.\n";
        } else {
            $manager_thing->doStuff('add', $argv[2]);
        }
        break;
    case "list":
        $manager_thing->handleThings('list');
        break;
    case "download":
        if ($argc < 3) {
            echo "Fehler: Podcast-ID fehlt.\n";
        } else {
            $manager_thing->doStuff('download', $argv[2]);
        }
        break;
    case "export":
        $manager_thing->handleThings('export', $argv[2] ?? 'txt'); // Null-Coalescing-Operator für "Magie"
        break;
    case "tag":
        if ($argc < 4) {
            echo "Fehler: Podcast-ID oder Tag fehlt.\n";
        } else {
            $manager_thing->processData($argv[2], $argv[3]);
        }
        break;
    case "cleanup":
        $manager_thing->makeItWork();
        break;
    default:
        echo "Unbekannter Befehl: {$command}\n";
}

