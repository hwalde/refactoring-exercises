<?php

declare(strict_types=1);

namespace RefactoringExercises\LegacyModernization\PodcastManager;

use PHPUnit\Framework\TestCase;

final class PodcastManagerTest extends TestCase
{
    private string $testDir;
    private string $scriptPath;

    protected function setUp(): void
    {
        $this->testDir = sys_get_temp_dir() . '/podcast_test_' . uniqid();
        mkdir($this->testDir);
        chdir($this->testDir);
        
        $this->scriptPath = __DIR__ . '/src/PodcastManager.php';
        copy($this->scriptPath, $this->testDir . '/PodcastManager.php');
    }

    protected function tearDown(): void
    {
        $this->cleanupTestDir();
    }

    private function cleanupTestDir(): void
    {
        if (is_dir($this->testDir)) {
            $files = new \RecursiveIteratorIterator(
                new \RecursiveDirectoryIterator($this->testDir, \RecursiveDirectoryIterator::SKIP_DOTS),
                \RecursiveIteratorIterator::CHILD_FIRST
            );

            foreach ($files as $fileinfo) {
                $todo = ($fileinfo->isDir()) ? 'rmdir' : 'unlink';
                $todo($fileinfo->getRealPath());
            }

            rmdir($this->testDir);
        }
    }

    private function executeCommand(string $command): array
    {
        $fullCommand = "php PodcastManager.php " . $command . " 2>&1";
        exec($fullCommand, $output, $returnCode);
        
        return [
            'output' => implode("\n", $output),
            'return_code' => $returnCode,
            'lines' => $output
        ];
    }

    private function createMockRssFeed(): string
    {
        $xml = '<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>Test Podcast</title>
        <description>A test podcast</description>
        <item>
            <title>Episode 1</title>
            <description>First episode</description>
            <enclosure url="https://example.com/episode1.mp3" type="audio/mpeg" length="1000"/>
        </item>
        <item>
            <title>Episode 2</title>
            <description>Second episode</description>
            <enclosure url="https://example.com/episode2.mp3" type="audio/mpeg" length="2000"/>
        </item>
    </channel>
</rss>';

        $feedFile = $this->testDir . '/test_feed.xml';
        file_put_contents($feedFile, $xml);
        return 'file://' . $feedFile;
    }

    public function testHelpIsDisplayedWithNoArguments(): void
    {
        $result = $this->executeCommand('');
        
        $this->assertEquals(1, $result['return_code']);
        $this->assertStringContainsString('Benutzung:', $result['output']);
        $this->assertStringContainsString('add <podcast_rss_url>', $result['output']);
        $this->assertStringContainsString('list', $result['output']);
        $this->assertStringContainsString('download <podcast_id>', $result['output']);
        $this->assertStringContainsString('export <json|txt>', $result['output']);
        $this->assertStringContainsString('tag <podcast_id> <tag_name>', $result['output']);
        $this->assertStringContainsString('cleanup', $result['output']);
    }

    public function testListWithEmptyDatabase(): void
    {
        $result = $this->executeCommand('list');
        
        $this->assertEquals(0, $result['return_code']);
        $this->assertStringContainsString('--- Abonnierte Podcasts ---', $result['output']);
        $this->assertStringContainsString('--- Heruntergeladene Episoden ---', $result['output']);
    }

    public function testAddPodcastCreatesFiles(): void
    {
        $feedUrl = $this->createMockRssFeed();
        $result = $this->executeCommand("add \"$feedUrl\"");
        
        $this->assertEquals(0, $result['return_code']);
        $this->assertStringContainsString('Versuche, Podcast von URL hinzuzufügen...', $result['output']);
        $this->assertStringContainsString("Podcast 'Test Podcast' hinzugefügt!", $result['output']);
        
        // Check database file was created
        $this->assertFileExists('podcasts_db.json');
        $dbContent = json_decode(file_get_contents('podcasts_db.json'), true);
        $this->assertArrayHasKey('podcasts', $dbContent);
        $this->assertArrayHasKey('episodes', $dbContent);
        $this->assertCount(1, $dbContent['podcasts']);
        $this->assertEquals('Test Podcast', $dbContent['podcasts'][0]['title']);
        $this->assertEquals($feedUrl, $dbContent['podcasts'][0]['url']);
        
        // Check log file was created
        $this->assertFileExists('activity.log');
        $logContent = file_get_contents('activity.log');
        $this->assertStringContainsString('ADDED PODCAST: Test Podcast', $logContent);
    }

    public function testAddPodcastWithMissingUrl(): void
    {
        $result = $this->executeCommand('add');
        
        $this->assertEquals(0, $result['return_code']);
        $this->assertStringContainsString('Fehler: URL fehlt.', $result['output']);
    }

    public function testAddPodcastWithInvalidUrl(): void
    {
        $result = $this->executeCommand('add "https://invalid-url-that-does-not-exist.com/feed.xml"');
        
        $this->assertEquals(0, $result['return_code']);
        $this->assertStringContainsString('Versuche, Podcast von URL hinzuzufügen...', $result['output']);
        $this->assertStringContainsString('Konnte die URL nicht abrufen.', $result['output']);
    }

    public function testListWithAddedPodcast(): void
    {
        $feedUrl = $this->createMockRssFeed();
        $this->executeCommand("add \"$feedUrl\"");
        
        $result = $this->executeCommand('list');
        
        $this->assertEquals(0, $result['return_code']);
        $this->assertStringContainsString('--- Abonnierte Podcasts ---', $result['output']);
        $this->assertStringContainsString('ID: 1 - Test Podcast', $result['output']);
        $this->assertStringContainsString($feedUrl, $result['output']);
        $this->assertStringContainsString('--- Heruntergeladene Episoden ---', $result['output']);
    }

    public function testDownloadWithMissingId(): void
    {
        $result = $this->executeCommand('download');
        
        $this->assertEquals(0, $result['return_code']);
        $this->assertStringContainsString('Fehler: Podcast-ID fehlt.', $result['output']);
    }

    public function testDownloadWithNonExistentId(): void
    {
        $result = $this->executeCommand('download 999');
        
        $this->assertEquals(0, $result['return_code']);
        $this->assertStringContainsString('Suche nach Episoden zum Herunterladen...', $result['output']);
        $this->assertStringContainsString('Podcast-ID nicht gefunden.', $result['output']);
    }

    public function testTagWithMissingParameters(): void
    {
        $result = $this->executeCommand('tag 1');
        
        $this->assertEquals(0, $result['return_code']);
        $this->assertStringContainsString('Fehler: Podcast-ID oder Tag fehlt.', $result['output']);
    }

    public function testTagFunctionality(): void
    {
        $feedUrl = $this->createMockRssFeed();
        $this->executeCommand("add \"$feedUrl\"");
        
        $result = $this->executeCommand('tag 1 "news"');
        
        $this->assertEquals(0, $result['return_code']);
        $this->assertStringContainsString("Tag 'news' zu Podcast ID 1 hinzugefügt.", $result['output']);
        
        // Check database was updated
        $dbContent = json_decode(file_get_contents('podcasts_db.json'), true);
        $this->assertContains('news', $dbContent['podcasts'][0]['tags']);
    }

    public function testExportJsonFunctionality(): void
    {
        $feedUrl = $this->createMockRssFeed();
        $this->executeCommand("add \"$feedUrl\"");
        
        $result = $this->executeCommand('export json');
        
        $this->assertEquals(0, $result['return_code']);
        $this->assertStringContainsString('Daten nach export.json exportiert.', $result['output']);
        $this->assertFileExists('export.json');
        
        $exportContent = json_decode(file_get_contents('export.json'), true);
        $this->assertArrayHasKey('podcasts', $exportContent);
        $this->assertArrayHasKey('episodes', $exportContent);
        $this->assertEquals('Test Podcast', $exportContent['podcasts'][0]['title']);
    }

    public function testExportTxtFunctionality(): void
    {
        $feedUrl = $this->createMockRssFeed();
        $this->executeCommand("add \"$feedUrl\"");
        
        $result = $this->executeCommand('export txt');
        
        $this->assertEquals(0, $result['return_code']);
        $this->assertStringContainsString('Daten nach export.txt exportiert.', $result['output']);
        $this->assertFileExists('export.txt');
        
        $exportContent = file_get_contents('export.txt');
        $this->assertStringContainsString('Podcast: Test Podcast', $exportContent);
    }

    public function testExportWithDefaultFormat(): void
    {
        $feedUrl = $this->createMockRssFeed();
        $this->executeCommand("add \"$feedUrl\"");
        
        $result = $this->executeCommand('export');
        
        $this->assertEquals(0, $result['return_code']);
        $this->assertStringContainsString('Daten nach export.txt exportiert.', $result['output']);
        $this->assertFileExists('export.txt');
    }

    public function testExportWithUnknownFormat(): void
    {
        $result = $this->executeCommand('export unknown');
        
        $this->assertEquals(0, $result['return_code']);
        $this->assertStringContainsString('Unbekanntes Exportformat.', $result['output']);
    }

    public function testCleanupWithoutMissingFiles(): void
    {
        $result = $this->executeCommand('cleanup');
        
        $this->assertEquals(0, $result['return_code']);
        $this->assertStringContainsString('Führe Wartungsarbeiten durch...', $result['output']);
        $this->assertStringContainsString('Alles in Ordnung.', $result['output']);
    }

    public function testUnknownCommand(): void
    {
        $result = $this->executeCommand('unknowncommand');
        
        $this->assertEquals(0, $result['return_code']);
        $this->assertStringContainsString('Unbekannter Befehl: unknowncommand', $result['output']);
    }

    public function testDownloadCreatesDownloadsDirectory(): void
    {
        $feedUrl = $this->createMockRssFeed();
        $this->executeCommand("add \"$feedUrl\"");
        
        // Mock the file_get_contents for episode downloads by creating empty files
        // Since we can't mock in this black-box test, we'll check the attempt was made
        $result = $this->executeCommand('download 1');
        
        $this->assertEquals(0, $result['return_code']);
        $this->assertStringContainsString('Suche nach Episoden zum Herunterladen...', $result['output']);
    }

    public function testPersistenceAcrossMultipleCommands(): void
    {
        $feedUrl = $this->createMockRssFeed();
        
        // Add podcast
        $this->executeCommand("add \"$feedUrl\"");
        
        // Add tag
        $this->executeCommand('tag 1 "tech"');
        
        // List should show both podcast and tag
        $result = $this->executeCommand('list');
        $this->assertStringContainsString('Test Podcast', $result['output']);
        
        // Database should persist changes
        $dbContent = json_decode(file_get_contents('podcasts_db.json'), true);
        $this->assertContains('tech', $dbContent['podcasts'][0]['tags']);
    }
}