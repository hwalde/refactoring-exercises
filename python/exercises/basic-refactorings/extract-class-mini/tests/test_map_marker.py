"""Tests for MapMarker class."""

import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from map_marker import MapMarker


class TestMapMarker:
    """Test cases for MapMarker class."""

    def setup_method(self):
        """Set up test fixture."""
        self.marker = MapMarker(
            52.5200,
            13.4050,
            34.0,
            "Brandenburg Gate",
            "Historic landmark in Berlin",
            "/brandenburg-gate.png",
            True,
        )

    def test_constructor_sets_all_properties(self):
        """Test that constructor sets all properties correctly."""
        marker = MapMarker(
            40.7128,
            -74.0060,
            10.0,
            "Statue of Liberty",
            "Famous statue in New York Harbor",
        )

        assert marker.get_latitude() == 40.7128
        assert marker.get_longitude() == -74.0060
        assert marker.get_altitude() == 10.0
        assert marker.get_title() == "Statue of Liberty"
        assert marker.get_description() == "Famous statue in New York Harbor"
        assert marker.get_icon_url() == "/default-marker.png"
        assert marker.is_visible()

    def test_constructor_with_custom_icon_and_visibility(self):
        """Test constructor with custom icon and visibility."""
        marker = MapMarker(
            48.8566,
            2.3522,
            35.0,
            "Eiffel Tower",
            "Iron lattice tower in Paris",
            "/eiffel-tower.png",
            False,
        )

        assert marker.get_icon_url() == "/eiffel-tower.png"
        assert not marker.is_visible()

    def test_get_coordinates(self):
        """Test getting coordinates."""
        assert self.marker.get_latitude() == 52.5200
        assert self.marker.get_longitude() == 13.4050
        assert self.marker.get_altitude() == 34.0

    def test_get_marker_info(self):
        """Test getting marker information."""
        assert self.marker.get_title() == "Brandenburg Gate"
        assert self.marker.get_description() == "Historic landmark in Berlin"
        assert self.marker.get_icon_url() == "/brandenburg-gate.png"
        assert self.marker.is_visible()

    def test_set_visible(self):
        """Test setting visibility."""
        self.marker.set_visible(False)
        assert not self.marker.is_visible()

        self.marker.set_visible(True)
        assert self.marker.is_visible()

    def test_update_info(self):
        """Test updating marker information."""
        self.marker.update_info("Berlin Gate", "Updated description")

        assert self.marker.get_title() == "Berlin Gate"
        assert self.marker.get_description() == "Updated description"

    def test_change_icon(self):
        """Test changing icon."""
        self.marker.change_icon("/new-icon.png")
        assert self.marker.get_icon_url() == "/new-icon.png"

    def test_move_to(self):
        """Test moving marker to new location."""
        self.marker.move_to(51.5074, -0.1278, 11.0)

        assert self.marker.get_latitude() == 51.5074
        assert self.marker.get_longitude() == -0.1278
        assert self.marker.get_altitude() == 11.0

    def test_distance_to_same_location(self):
        """Test distance calculation to same location."""
        distance = self.marker.distance_to(52.5200, 13.4050)
        assert abs(distance - 0.0) < 0.1

    def test_distance_to_known_location(self):
        """Test distance calculation to known location."""
        # Distance from Brandenburg Gate to Reichstag Building (approximately 1960m)
        distance = self.marker.distance_to(52.5186, 13.3761)
        assert abs(distance - 1960.0) < 100.0

    def test_distance_to_far_away_location(self):
        """Test distance calculation to far away location."""
        # Distance from Berlin to Paris (approximately 878 km)
        distance = self.marker.distance_to(48.8566, 2.3522)
        assert abs(distance - 878000.0) < 10000.0

    def test_get_formatted_coordinates(self):
        """Test formatted coordinates output."""
        formatted = self.marker.get_formatted_coordinates()
        assert formatted == "Lat: 52.520000°, Lon: 13.405000°, Alt: 34.0m"

    def test_get_formatted_coordinates_with_negative_values(self):
        """Test formatted coordinates with negative values."""
        marker = MapMarker(
            -33.8688, 151.2093, 58.0, "Sydney Opera House", "Iconic building"
        )
        formatted = marker.get_formatted_coordinates()
        assert formatted == "Lat: -33.868800°, Lon: 151.209300°, Alt: 58.0m"

    def test_is_at_same_location_within_tolerance(self):
        """Test location comparison within tolerance."""
        assert self.marker.is_at_same_location(52.5201, 13.4051)
        assert self.marker.is_at_same_location(52.5199, 13.4049)

    def test_is_at_same_location_outside_tolerance(self):
        """Test location comparison outside tolerance."""
        assert not self.marker.is_at_same_location(52.5210, 13.4060)
        assert not self.marker.is_at_same_location(52.5100, 13.4000)

    def test_is_at_same_location_with_custom_tolerance(self):
        """Test location comparison with custom tolerance."""
        assert self.marker.is_at_same_location(52.5250, 13.4100, 0.01)
        assert not self.marker.is_at_same_location(52.5250, 13.4100, 0.001)

    def test_to_dict(self):
        """Test conversion to dictionary."""
        expected = {
            "latitude": 52.5200,
            "longitude": 13.4050,
            "altitude": 34.0,
            "title": "Brandenburg Gate",
            "description": "Historic landmark in Berlin",
            "icon_url": "/brandenburg-gate.png",
            "is_visible": True,
        }

        assert self.marker.to_dict() == expected

    def test_to_dict_after_modifications(self):
        """Test conversion to dictionary after modifications."""
        self.marker.move_to(48.8566, 2.3522, 35.0)
        self.marker.update_info("Eiffel Tower", "Iron lattice tower in Paris")
        self.marker.change_icon("/eiffel-tower.png")
        self.marker.set_visible(False)

        expected = {
            "latitude": 48.8566,
            "longitude": 2.3522,
            "altitude": 35.0,
            "title": "Eiffel Tower",
            "description": "Iron lattice tower in Paris",
            "icon_url": "/eiffel-tower.png",
            "is_visible": False,
        }

        assert self.marker.to_dict() == expected
