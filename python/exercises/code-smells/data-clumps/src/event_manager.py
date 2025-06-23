"""
EventManager handles event creation and management

This class demonstrates the "Data Clumps" code smell by having multiple methods
that repeatedly use the same groups of parameters together:
- Date, time, and timezone parameters
- Address components (street, city, country, postal code)
- Coordinate parameters (latitude, longitude)
- Contact information (name, email, phone)

These parameter groups should be refactored into Parameter Objects.
"""

import math
import re
import uuid
from dataclasses import dataclass
from datetime import datetime

import pytz


@dataclass
class Event:
    """Represents an event with all its details"""

    id: str
    title: str
    description: str
    date: str
    start_time: str
    end_time: str
    timezone: str
    street: str
    city: str
    country: str
    postal_code: str
    latitude: float
    longitude: float
    organizer_name: str
    organizer_email: str
    organizer_phone: str
    max_attendees: int
    ticket_price: float
    attendees: int
    status: str


@dataclass
class Venue:
    """Represents a venue with location and contact details"""

    id: str
    name: str
    description: str
    street: str
    city: str
    country: str
    postal_code: str
    latitude: float
    longitude: float
    contact_name: str
    contact_email: str
    contact_phone: str
    capacity: int
    status: str


@dataclass
class Notification:
    """Represents a notification sent to an organizer"""

    id: str
    event_id: str
    organizer_name: str
    organizer_email: str
    organizer_phone: str
    message: str
    sent_at: str
    status: str


@dataclass
class TimeConversion:
    """Represents a time converted to a different timezone"""

    date: str
    time: str
    timezone: str


class EventManager:
    """Manages events, venues, and notifications with data clumps"""

    def __init__(self) -> None:
        self.events: dict[str, Event] = {}
        self.venues: dict[str, Venue] = {}
        self.notifications: dict[str, Notification] = {}

    def create_event(
        self,
        title: str,
        description: str,
        date: str,
        start_time: str,
        end_time: str,
        timezone_str: str,
        street: str,
        city: str,
        country: str,
        postal_code: str,
        latitude: float,
        longitude: float,
        organizer_name: str,
        organizer_email: str,
        organizer_phone: str,
        max_attendees: int = 100,
        ticket_price: float = 0.0,
    ) -> Event:
        """Creates a new event with date/time, location, and organizer information"""

        # Validate date and time
        if not self._is_valid_date(date):
            raise ValueError("Invalid date format")

        if not self._is_valid_time(start_time) or not self._is_valid_time(end_time):
            raise ValueError("Invalid time format")

        if not self._is_valid_timezone(timezone_str):
            raise ValueError("Invalid timezone")

        if not self._is_time_range_valid(start_time, end_time):
            raise ValueError("End time must be after start time")

        # Validate address
        if not self._is_valid_address(street, city, country, postal_code):
            raise ValueError("Invalid address information")

        # Validate coordinates
        if not self._is_valid_coordinates(latitude, longitude):
            raise ValueError("Invalid coordinates")

        # Validate contact information
        if not self._is_valid_contact(organizer_name, organizer_email, organizer_phone):
            raise ValueError("Invalid organizer contact information")

        event_id = self._generate_id()
        event = Event(
            id=event_id,
            title=title,
            description=description,
            date=date,
            start_time=start_time,
            end_time=end_time,
            timezone=timezone_str,
            street=street,
            city=city,
            country=country,
            postal_code=postal_code,
            latitude=latitude,
            longitude=longitude,
            organizer_name=organizer_name,
            organizer_email=organizer_email,
            organizer_phone=organizer_phone,
            max_attendees=max_attendees,
            ticket_price=ticket_price,
            attendees=0,
            status="active",
        )

        self.events[event_id] = event
        return event

    def update_event_timing(
        self,
        event_id: str,
        date: str,
        start_time: str,
        end_time: str,
        timezone_str: str,
    ) -> bool:
        """Updates event timing information"""

        if event_id not in self.events:
            return False

        # Validate date and time
        if not self._is_valid_date(date):
            raise ValueError("Invalid date format")

        if not self._is_valid_time(start_time) or not self._is_valid_time(end_time):
            raise ValueError("Invalid time format")

        if not self._is_valid_timezone(timezone_str):
            raise ValueError("Invalid timezone")

        if not self._is_time_range_valid(start_time, end_time):
            raise ValueError("End time must be after start time")

        event = self.events[event_id]
        event.date = date
        event.start_time = start_time
        event.end_time = end_time
        event.timezone = timezone_str

        return True

    def update_event_location(
        self,
        event_id: str,
        street: str,
        city: str,
        country: str,
        postal_code: str,
        latitude: float,
        longitude: float,
    ) -> bool:
        """Updates event location information"""

        if event_id not in self.events:
            return False

        # Validate address
        if not self._is_valid_address(street, city, country, postal_code):
            raise ValueError("Invalid address information")

        # Validate coordinates
        if not self._is_valid_coordinates(latitude, longitude):
            raise ValueError("Invalid coordinates")

        event = self.events[event_id]
        event.street = street
        event.city = city
        event.country = country
        event.postal_code = postal_code
        event.latitude = latitude
        event.longitude = longitude

        return True

    def register_venue(
        self,
        name: str,
        description: str,
        street: str,
        city: str,
        country: str,
        postal_code: str,
        latitude: float,
        longitude: float,
        contact_name: str,
        contact_email: str,
        contact_phone: str,
        capacity: int = 50,
    ) -> Venue:
        """Registers a new venue with address and contact information"""

        # Validate address
        if not self._is_valid_address(street, city, country, postal_code):
            raise ValueError("Invalid address information")

        # Validate coordinates
        if not self._is_valid_coordinates(latitude, longitude):
            raise ValueError("Invalid coordinates")

        # Validate contact information
        if not self._is_valid_contact(contact_name, contact_email, contact_phone):
            raise ValueError("Invalid contact information")

        venue_id = self._generate_id()
        venue = Venue(
            id=venue_id,
            name=name,
            description=description,
            street=street,
            city=city,
            country=country,
            postal_code=postal_code,
            latitude=latitude,
            longitude=longitude,
            contact_name=contact_name,
            contact_email=contact_email,
            contact_phone=contact_phone,
            capacity=capacity,
            status="active",
        )

        self.venues[venue_id] = venue
        return venue

    def send_event_notification(
        self,
        event_id: str,
        organizer_name: str,
        organizer_email: str,
        organizer_phone: str,
        message: str,
    ) -> bool:
        """Sends event notification to organizer"""

        if event_id not in self.events:
            return False

        # Validate contact information
        if not self._is_valid_contact(organizer_name, organizer_email, organizer_phone):
            raise ValueError("Invalid organizer contact information")

        notification_id = self._generate_id()
        notification = Notification(
            id=notification_id,
            event_id=event_id,
            organizer_name=organizer_name,
            organizer_email=organizer_email,
            organizer_phone=organizer_phone,
            message=message,
            sent_at=datetime.now().isoformat(),
            status="sent",
        )

        self.notifications[notification_id] = notification
        return True

    def schedule_recurring_event(
        self,
        base_event_id: str,
        pattern: str,
        occurrences: int,
        start_date: str,
        start_time: str,
        end_time: str,
        timezone_str: str,
    ) -> list[Event]:
        """Schedules recurring event"""

        if base_event_id not in self.events:
            raise ValueError("Base event not found")

        # Validate date and time
        if not self._is_valid_date(start_date):
            raise ValueError("Invalid date format")

        if not self._is_valid_time(start_time) or not self._is_valid_time(end_time):
            raise ValueError("Invalid time format")

        if not self._is_valid_timezone(timezone_str):
            raise ValueError("Invalid timezone")

        if not self._is_time_range_valid(start_time, end_time):
            raise ValueError("End time must be after start time")

        recurring_events = []
        base_event = self.events[base_event_id]

        for i in range(occurrences):
            event_date = self._calculate_next_date(start_date, pattern, i)
            event_id = self._generate_id()

            event = Event(
                id=event_id,
                title=base_event.title + " (Recurring)",
                description=base_event.description,
                date=event_date,
                start_time=start_time,
                end_time=end_time,
                timezone=timezone_str,
                street=base_event.street,
                city=base_event.city,
                country=base_event.country,
                postal_code=base_event.postal_code,
                latitude=base_event.latitude,
                longitude=base_event.longitude,
                organizer_name=base_event.organizer_name,
                organizer_email=base_event.organizer_email,
                organizer_phone=base_event.organizer_phone,
                max_attendees=base_event.max_attendees,
                ticket_price=base_event.ticket_price,
                attendees=0,
                status="active",
            )

            self.events[event_id] = event
            recurring_events.append(event)

        return recurring_events

    def calculate_distance(
        self, lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """Calculates distance between two coordinate points"""

        if not self._is_valid_coordinates(lat1, lon1) or not self._is_valid_coordinates(
            lat2, lon2
        ):
            raise ValueError("Invalid coordinates")

        earth_radius = 6371  # Earth's radius in kilometers

        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)

        a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(
            math.radians(lat1)
        ) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) * math.sin(d_lon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return earth_radius * c

    def find_events_in_date_range(
        self,
        start_date: str,
        start_time: str,
        end_date: str,
        end_time: str,
        timezone_str: str,
    ) -> list[Event]:
        """Finds events within date range"""

        # Validate date and time
        if not self._is_valid_date(start_date) or not self._is_valid_date(end_date):
            raise ValueError("Invalid date format")

        if not self._is_valid_time(start_time) or not self._is_valid_time(end_time):
            raise ValueError("Invalid time format")

        if not self._is_valid_timezone(timezone_str):
            raise ValueError("Invalid timezone")

        matching_events = []

        for event in self.events.values():
            if self._is_event_in_date_range(
                event, start_date, start_time, end_date, end_time, timezone_str
            ):
                matching_events.append(event)

        return matching_events

    def convert_time_to_timezone(
        self, date: str, time: str, from_timezone: str, to_timezone: str
    ) -> TimeConversion:
        """Converts time to different timezone"""

        if not self._is_valid_date(date):
            raise ValueError("Invalid date format")

        if not self._is_valid_time(time):
            raise ValueError("Invalid time format")

        if not self._is_valid_timezone(from_timezone) or not self._is_valid_timezone(
            to_timezone
        ):
            raise ValueError("Invalid timezone")

        # Create datetime in source timezone
        from_tz = pytz.timezone(from_timezone)
        to_tz = pytz.timezone(to_timezone)

        date_time_str = f"{date} {time}"
        naive_dt = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        from_dt = from_tz.localize(naive_dt)
        to_dt = from_dt.astimezone(to_tz)

        return TimeConversion(
            date=to_dt.strftime("%Y-%m-%d"),
            time=to_dt.strftime("%H:%M:%S"),
            timezone=to_timezone,
        )

    # Validation methods (these contain the data clumps logic)
    def _is_valid_date(self, date: str) -> bool:
        """Validates date format"""
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
            return False
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _is_valid_time(self, time: str) -> bool:
        """Validates time format"""
        return bool(re.match(r"^\d{2}:\d{2}:\d{2}$", time))

    def _is_valid_timezone(self, timezone_str: str) -> bool:
        """Validates timezone"""
        try:
            pytz.timezone(timezone_str)
            return True
        except pytz.exceptions.UnknownTimeZoneError:
            return False

    def _is_time_range_valid(self, start_time: str, end_time: str) -> bool:
        """Validates that end time is after start time"""
        return start_time < end_time

    def _is_valid_address(
        self, street: str, city: str, country: str, postal_code: str
    ) -> bool:
        """Validates address components"""
        return (
            street.strip() != ""
            and city.strip() != ""
            and country.strip() != ""
            and postal_code.strip() != ""
        )

    def _is_valid_coordinates(self, latitude: float, longitude: float) -> bool:
        """Validates coordinate values"""
        return -90 <= latitude <= 90 and -180 <= longitude <= 180

    def _is_valid_contact(self, name: str, email: str, phone: str) -> bool:
        """Validates contact information"""
        email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        return (
            name.strip() != ""
            and re.match(email_pattern, email) is not None
            and phone.strip() != ""
        )

    def _is_event_in_date_range(
        self,
        event: Event,
        start_date: str,
        start_time: str,
        end_date: str,
        end_time: str,
        timezone_str: str,
    ) -> bool:
        """Checks if event is within date range"""
        # Simplified comparison - in real implementation would handle timezone conversion
        event_datetime = f"{event.date} {event.start_time}"
        range_start = f"{start_date} {start_time}"
        range_end = f"{end_date} {end_time}"

        return range_start <= event_datetime <= range_end

    def _calculate_next_date(
        self, base_date: str, pattern: str, occurrence: int
    ) -> str:
        """Calculates next date based on pattern"""
        date = datetime.strptime(base_date, "%Y-%m-%d")

        if pattern == "daily":
            from datetime import timedelta

            date += timedelta(days=occurrence)
        elif pattern == "weekly":
            from datetime import timedelta

            date += timedelta(weeks=occurrence)
        elif pattern == "monthly":
            month = date.month + occurrence
            year = date.year + (month - 1) // 12
            month = ((month - 1) % 12) + 1
            date = date.replace(year=year, month=month)

        return date.strftime("%Y-%m-%d")

    def _generate_id(self) -> str:
        """Generates unique ID"""
        return f"evt_{uuid.uuid4().hex[:9]}"

    # Getters for testing
    def get_events(self) -> list[Event]:
        """Returns list of all events"""
        return list(self.events.values())

    def get_venues(self) -> list[Venue]:
        """Returns list of all venues"""
        return list(self.venues.values())

    def get_notifications(self) -> list[Notification]:
        """Returns list of all notifications"""
        return list(self.notifications.values())
