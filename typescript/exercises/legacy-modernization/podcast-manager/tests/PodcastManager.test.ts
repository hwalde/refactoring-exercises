import * as fs from 'fs';
import * as path from 'path';

describe('PodcastManager Black-Box Tests', () => {
    let originalCwd: string;

    beforeEach(() => {
        originalCwd = process.cwd();
    });

    afterEach(() => {
        process.chdir(originalCwd);
    });

    test('PodcastManager file exists and can be read', () => {
        const scriptPath = path.join(__dirname, '..', 'src', 'PodcastManager.ts');
        expect(fs.existsSync(scriptPath)).toBe(true);
        
        const content = fs.readFileSync(scriptPath, 'utf-8');
        expect(content).toContain('class PodcastThing');
        expect(content).toContain('doStuff');
        expect(content).toContain('handleThings');
    });

    test('TypeScript file structure follows expected format', () => {
        const scriptPath = path.join(__dirname, '..', 'src', 'PodcastManager.ts');
        const content = fs.readFileSync(scriptPath, 'utf-8');
        
        // Check for typical code smells we expect in the legacy code
        expect(content).toContain('any'); // Should use any types (bad practice)
        expect(content).toContain('God-Class'); // Should have comments about code smells
        expect(content).toContain('Monolithische'); // Should have comments about code smells
        expect(content).toContain('Duplizierter Code'); // Should have comments about code smells
    });

    test('Required imports are present', () => {
        const scriptPath = path.join(__dirname, '..', 'src', 'PodcastManager.ts');
        const content = fs.readFileSync(scriptPath, 'utf-8');
        
        expect(content).toContain('import * as fs from');
        expect(content).toContain('import * as path from');
        expect(content).toContain('import axios from');
        expect(content).toContain('import { parseStringPromise } from \'xml2js\'');
    });

    test('Main function structure exists', () => {
        const scriptPath = path.join(__dirname, '..', 'src', 'PodcastManager.ts');
        const content = fs.readFileSync(scriptPath, 'utf-8');
        
        // Check for main execution pattern
        expect(content).toContain('process.argv.slice(2)');
        expect(content).toContain('new PodcastThing()');
        
        // Check for commands
        expect(content).toContain('case "add"');
        expect(content).toContain('case "list"');
        expect(content).toContain('case "download"');
        expect(content).toContain('case "export"');
        expect(content).toContain('case "tag"');
        expect(content).toContain('case "cleanup"');
    });

    test('Error messages match PRD requirements', () => {
        const scriptPath = path.join(__dirname, '..', 'src', 'PodcastManager.ts');
        const content = fs.readFileSync(scriptPath, 'utf-8');
        
        // Check for required error messages from PRD
        expect(content).toContain('Fehler: URL fehlt.');
        expect(content).toContain('Fehler: Podcast-ID fehlt.');
        expect(content).toContain('Fehler: Podcast-ID oder Tag fehlt.');
        expect(content).toContain('Podcast-ID nicht gefunden.');
    });

    test('Database and logging patterns exist', () => {
        const scriptPath = path.join(__dirname, '..', 'src', 'PodcastManager.ts');
        const content = fs.readFileSync(scriptPath, 'utf-8');
        
        expect(content).toContain('podcasts_db.json');
        expect(content).toContain('activity.log');
        expect(content).toContain('ADDED PODCAST:');
        expect(content).toContain('DOWNLOADED:');
    });

    test('Usage message includes all required commands', () => {
        const scriptPath = path.join(__dirname, '..', 'src', 'PodcastManager.ts');
        const content = fs.readFileSync(scriptPath, 'utf-8');
        
        expect(content).toContain('Benutzung:');
        expect(content).toContain('add <podcast_rss_url>');
        expect(content).toContain('list');
        expect(content).toContain('download <podcast_id>');
        expect(content).toContain('export <json|txt>');
        expect(content).toContain('tag <podcast_id> <tag_name>');
        expect(content).toContain('cleanup');
    });
});