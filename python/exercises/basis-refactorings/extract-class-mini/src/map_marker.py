"""MapMarker class for representing map markers with coordinates and metadata."""

import math
from typing import Any


class MapMarker:
    """A map marker with coordinate data and marker-specific properties.

    This class currently has too many responsibilities, mixing coordinate logic
    with marker-specific functionality. The coordinates should be extracted
    into a separate Coordinate class.
    """

    def __init__(
        self,
        latitude: float,
        longitude: float,
        altitude: float,
        title: str,
        description: str,
        icon_url: str = "/default-marker.png",
        is_visible: bool = True,
    ) -> None:
        """Initialize a new MapMarker.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            altitude: Altitude in meters
            title: Marker title
            description: Marker description
            icon_url: URL to marker icon
            is_visible: Whether marker is visible
        """
        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude
        self._title = title
        self._description = description
        self._icon_url = icon_url
        self._is_visible = is_visible

    def get_latitude(self) -> float:
        """Get the latitude coordinate."""
        return self._latitude

    def get_longitude(self) -> float:
        """Get the longitude coordinate."""
        return self._longitude

    def get_altitude(self) -> float:
        """Get the altitude in meters."""
        return self._altitude

    def get_title(self) -> str:
        """Get the marker title."""
        return self._title

    def get_description(self) -> str:
        """Get the marker description."""
        return self._description

    def get_icon_url(self) -> str:
        """Get the marker icon URL."""
        return self._icon_url

    def is_visible(self) -> bool:
        """Check if the marker is visible."""
        return self._is_visible

    def set_visible(self, is_visible: bool) -> None:
        """Set the marker visibility.

        Args:
            is_visible: Whether the marker should be visible
        """
        self._is_visible = is_visible

    def update_info(self, title: str, description: str) -> None:
        """Update the marker title and description.

        Args:
            title: New title
            description: New description
        """
        self._title = title
        self._description = description

    def change_icon(self, icon_url: str) -> None:
        """Change the marker icon.

        Args:
            icon_url: URL to the new icon
        """
        self._icon_url = icon_url

    def move_to(self, latitude: float, longitude: float, altitude: float) -> None:
        """Move the marker to new coordinates.

        Args:
            latitude: New latitude
            longitude: New longitude
            altitude: New altitude in meters
        """
        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude

    def distance_to(self, latitude: float, longitude: float) -> float:
        """Calculate distance to another point using Haversine formula.

        Args:
            latitude: Target latitude
            longitude: Target longitude

        Returns:
            Distance in meters
        """
        # Haversine formula for calculating distance between two points on Earth
        earth_radius = 6371000  # meters

        lat1_rad = math.radians(self._latitude)
        lat2_rad = math.radians(latitude)
        delta_lat_rad = math.radians(latitude - self._latitude)
        delta_lon_rad = math.radians(longitude - self._longitude)

        a = math.sin(delta_lat_rad / 2) * math.sin(delta_lat_rad / 2) + math.cos(
            lat1_rad
        ) * math.cos(lat2_rad) * math.sin(delta_lon_rad / 2) * math.sin(
            delta_lon_rad / 2
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return earth_radius * c

    def get_formatted_coordinates(self) -> str:
        """Get formatted coordinate string.

        Returns:
            Formatted coordinate string
        """
        return f"Lat: {self._latitude:.6f}°, Lon: {self._longitude:.6f}°, Alt: {self._altitude:.1f}m"

    def is_at_same_location(
        self, latitude: float, longitude: float, tolerance: float = 0.001
    ) -> bool:
        """Check if marker is at the same location as given coordinates.

        Args:
            latitude: Target latitude
            longitude: Target longitude
            tolerance: Tolerance for comparison

        Returns:
            True if within tolerance, False otherwise
        """
        return (
            abs(self._latitude - latitude) < tolerance
            and abs(self._longitude - longitude) < tolerance
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert marker to dictionary representation.

        Returns:
            Dictionary with all marker data
        """
        return {
            "latitude": self._latitude,
            "longitude": self._longitude,
            "altitude": self._altitude,
            "title": self._title,
            "description": self._description,
            "icon_url": self._icon_url,
            "is_visible": self._is_visible,
        }
