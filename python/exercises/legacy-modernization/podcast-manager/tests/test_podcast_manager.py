"""
Black-box tests for the podcast manager CLI application.
These tests define the expected external behavior that must be maintained during refactoring.
"""

import sys
import os
import subprocess
import tempfile
import shutil
import json
import unittest
from pathlib import Path
from typing import Dict, List, Any


class PodcastManagerTest(unittest.TestCase):
    """Comprehensive black-box tests for podcast manager functionality."""

    def setUp(self) -> None:
        """Set up isolated test environment for each test."""
        self.test_dir = tempfile.mkdtemp(prefix="podcast_test_")
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Copy the script to test directory
        self.script_path = Path(__file__).parent.parent / "src" / "podcast_manager.py"
        shutil.copy(self.script_path, os.path.join(self.test_dir, "podcast_manager.py"))

    def tearDown(self) -> None:
        """Clean up test environment after each test."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def execute_command(self, command: str) -> Dict[str, Any]:
        """Execute a podcast manager command and return results."""
        full_command = f"{sys.executable} podcast_manager.py {command}"
        result = subprocess.run(
            full_command, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace"
        )

        # Combine stdout and stderr for output, as some messages may go to stderr
        stdout_text = result.stdout if result.stdout is not None else ""
        stderr_text = result.stderr if result.stderr is not None else ""
        combined_output = stdout_text + stderr_text

        return {
            "output": combined_output,
            "stderr": result.stderr,
            "return_code": result.returncode,
            "lines": combined_output.splitlines(),
        }

    def create_mock_rss_feed(self) -> str:
        """Create a mock RSS feed file for testing."""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
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
</rss>"""

        feed_file = os.path.join(self.test_dir, "test_feed.xml")
        with open(feed_file, "w", encoding="utf-8") as f:
            f.write(xml_content)
        return f"file://{feed_file}"

    def test_help_is_displayed_with_no_arguments(self) -> None:
        """Test that help is displayed when no arguments are provided."""
        result = self.execute_command("")

        self.assertEqual(1, result["return_code"])
        self.assertIn("Benutzung:", result["output"])
        self.assertIn("add <podcast_rss_url>", result["output"])
        self.assertIn("list", result["output"])
        self.assertIn("download <podcast_id>", result["output"])
        self.assertIn("export <json|txt>", result["output"])
        self.assertIn("tag <podcast_id> <tag_name>", result["output"])
        self.assertIn("cleanup", result["output"])

    def test_list_with_empty_database(self) -> None:
        """Test list command with empty database."""
        result = self.execute_command("list")

        self.assertEqual(0, result["return_code"])
        self.assertIn("--- Abonnierte Podcasts ---", result["output"])
        self.assertIn("--- Heruntergeladene Episoden ---", result["output"])

    def test_add_podcast_creates_files(self) -> None:
        """Test that adding a podcast creates necessary files."""
        feed_url = self.create_mock_rss_feed()
        result = self.execute_command(f'add "{feed_url}"')

        self.assertEqual(0, result["return_code"])
        self.assertIn("Versuche, Podcast von URL hinzuzufügen...", result["output"])
        self.assertIn("Podcast 'Test Podcast' hinzugefügt!", result["output"])

        # Check database file was created
        self.assertTrue(os.path.exists("podcasts_db.json"))
        with open("podcasts_db.json", "r", encoding="utf-8") as f:
            db_content = json.load(f)
        self.assertIn("podcasts", db_content)
        self.assertIn("episodes", db_content)
        self.assertEqual(1, len(db_content["podcasts"]))
        self.assertEqual("Test Podcast", db_content["podcasts"][0]["title"])
        self.assertEqual(feed_url, db_content["podcasts"][0]["url"])

        # Check log file was created
        self.assertTrue(os.path.exists("activity.log"))
        with open("activity.log", "r", encoding="utf-8") as f:
            log_content = f.read()
        self.assertIn("ADDED PODCAST: Test Podcast", log_content)

    def test_add_podcast_with_missing_url(self) -> None:
        """Test add command without URL parameter."""
        result = self.execute_command("add")

        self.assertEqual(0, result["return_code"])
        self.assertIn("Fehler: URL fehlt.", result["output"])

    def test_add_podcast_with_invalid_url(self) -> None:
        """Test add command with invalid URL."""
        result = self.execute_command(
            'add "https://invalid-url-that-does-not-exist.com/feed.xml"'
        )

        self.assertEqual(0, result["return_code"])
        self.assertIn("Versuche, Podcast von URL hinzuzufügen...", result["output"])
        self.assertIn("Konnte die URL nicht abrufen.", result["output"])

    def test_list_with_added_podcast(self) -> None:
        """Test list command after adding a podcast."""
        feed_url = self.create_mock_rss_feed()
        self.execute_command(f'add "{feed_url}"')

        result = self.execute_command("list")

        self.assertEqual(0, result["return_code"])
        self.assertIn("--- Abonnierte Podcasts ---", result["output"])
        self.assertIn("ID: 1 - Test Podcast", result["output"])
        self.assertIn(feed_url, result["output"])
        self.assertIn("--- Heruntergeladene Episoden ---", result["output"])

    def test_download_with_missing_id(self) -> None:
        """Test download command without podcast ID."""
        result = self.execute_command("download")

        self.assertEqual(0, result["return_code"])
        self.assertIn("Fehler: Podcast-ID fehlt.", result["output"])

    def test_download_with_non_existent_id(self) -> None:
        """Test download command with non-existent podcast ID."""
        result = self.execute_command("download 999")

        self.assertEqual(0, result["return_code"])
        self.assertIn("Suche nach Episoden zum Herunterladen...", result["output"])
        self.assertIn("Podcast-ID nicht gefunden.", result["output"])

    def test_tag_with_missing_parameters(self) -> None:
        """Test tag command with missing parameters."""
        result = self.execute_command("tag 1")

        self.assertEqual(0, result["return_code"])
        self.assertIn("Fehler: Podcast-ID oder Tag fehlt.", result["output"])

    def test_tag_functionality(self) -> None:
        """Test adding tags to podcasts."""
        feed_url = self.create_mock_rss_feed()
        self.execute_command(f'add "{feed_url}"')

        result = self.execute_command('tag 1 "news"')

        self.assertEqual(0, result["return_code"])
        self.assertIn("Tag 'news' zu Podcast ID 1 hinzugefügt.", result["output"])

        # Check database was updated
        with open("podcasts_db.json", "r", encoding="utf-8") as f:
            db_content = json.load(f)
        self.assertIn("news", db_content["podcasts"][0]["tags"])

    def test_export_json_functionality(self) -> None:
        """Test JSON export functionality."""
        feed_url = self.create_mock_rss_feed()
        self.execute_command(f'add "{feed_url}"')

        result = self.execute_command("export json")

        self.assertEqual(0, result["return_code"])
        self.assertIn("Daten nach export.json exportiert.", result["output"])
        self.assertTrue(os.path.exists("export.json"))

        with open("export.json", "r", encoding="utf-8") as f:
            export_content = json.load(f)
        self.assertIn("podcasts", export_content)
        self.assertIn("episodes", export_content)
        self.assertEqual("Test Podcast", export_content["podcasts"][0]["title"])

    def test_export_txt_functionality(self) -> None:
        """Test TXT export functionality."""
        feed_url = self.create_mock_rss_feed()
        self.execute_command(f'add "{feed_url}"')

        result = self.execute_command("export txt")

        self.assertEqual(0, result["return_code"])
        self.assertIn("Daten nach export.txt exportiert.", result["output"])
        self.assertTrue(os.path.exists("export.txt"))

        with open("export.txt", "r", encoding="utf-8") as f:
            export_content = f.read()
        self.assertIn("Podcast: Test Podcast", export_content)

    def test_export_with_default_format(self) -> None:
        """Test export command with default format (txt)."""
        feed_url = self.create_mock_rss_feed()
        self.execute_command(f'add "{feed_url}"')

        result = self.execute_command("export")

        self.assertEqual(0, result["return_code"])
        self.assertIn("Daten nach export.txt exportiert.", result["output"])
        self.assertTrue(os.path.exists("export.txt"))

    def test_export_with_unknown_format(self) -> None:
        """Test export command with unknown format."""
        result = self.execute_command("export unknown")

        self.assertEqual(0, result["return_code"])
        self.assertIn("Unbekanntes Exportformat.", result["output"])

    def test_cleanup_without_missing_files(self) -> None:
        """Test cleanup command when no files are missing."""
        result = self.execute_command("cleanup")

        self.assertEqual(0, result["return_code"])
        self.assertIn("Führe Wartungsarbeiten durch...", result["output"])
        self.assertIn("Alles in Ordnung.", result["output"])

    def test_unknown_command(self) -> None:
        """Test behavior with unknown command."""
        result = self.execute_command("unknowncommand")

        self.assertEqual(0, result["return_code"])
        self.assertIn("Unbekannter Befehl: unknowncommand", result["output"])

    def test_download_creates_downloads_directory(self) -> None:
        """Test that download command attempts to create downloads directory."""
        feed_url = self.create_mock_rss_feed()
        self.execute_command(f'add "{feed_url}"')

        # Since we can't mock HTTP requests in this black-box test,
        # we'll just verify the attempt was made
        result = self.execute_command("download 1")

        self.assertEqual(0, result["return_code"])
        self.assertIn("Suche nach Episoden zum Herunterladen...", result["output"])

    def test_persistence_across_multiple_commands(self) -> None:
        """Test that data persists across multiple command executions."""
        feed_url = self.create_mock_rss_feed()

        # Add podcast
        self.execute_command(f'add "{feed_url}"')

        # Add tag
        self.execute_command('tag 1 "tech"')

        # List should show both podcast and tag
        result = self.execute_command("list")
        self.assertIn("Test Podcast", result["output"])

        # Database should persist changes
        with open("podcasts_db.json", "r", encoding="utf-8") as f:
            db_content = json.load(f)
        self.assertIn("tech", db_content["podcasts"][0]["tags"])

    def test_tag_with_invalid_podcast_id(self) -> None:
        """Test tag command with invalid podcast ID format."""
        result = self.execute_command('tag invalid_id "tech"')

        self.assertEqual(0, result["return_code"])
        self.assertIn("Fehler: Podcast-ID muss eine Zahl sein.", result["output"])


if __name__ == "__main__":
    unittest.main()
