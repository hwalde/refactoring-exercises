import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from event_manager import EventManager


class TestEventManager:

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.event_manager = EventManager()

    def test_create_event_with_valid_data(self):
        """Test creating event with valid data"""
        event = self.event_manager.create_event(
            "Tech Conference",
            "Annual technology conference",
            "2024-09-15",
            "09:00:00",
            "17:00:00",
            "Europe/Berlin",
            "Musterstraße 123",
            "Berlin",
            "Germany",
            "10115",
            52.5200,
            13.4050,
            "John Doe",
            "john@example.com",
            "+49-30-12345678",
            200,
            50.0,
        )

        assert event.id is not None
        assert event.title == "Tech Conference"
        assert event.date == "2024-09-15"
        assert event.start_time == "09:00:00"
        assert event.end_time == "17:00:00"
        assert event.timezone == "Europe/Berlin"
        assert event.street == "Musterstraße 123"
        assert event.city == "Berlin"
        assert event.country == "Germany"
        assert event.postal_code == "10115"
        assert event.latitude == 52.5200
        assert event.longitude == 13.4050
        assert event.organizer_name == "John Doe"
        assert event.organizer_email == "john@example.com"
        assert event.organizer_phone == "+49-30-12345678"
        assert event.max_attendees == 200
        assert event.ticket_price == 50.0
        assert event.status == "active"

    def test_create_event_with_invalid_date(self):
        """Test creating event with invalid date"""
        with pytest.raises(ValueError, match="Invalid date format"):
            self.event_manager.create_event(
                "Tech Conference",
                "Description",
                "invalid-date",
                "09:00:00",
                "17:00:00",
                "Europe/Berlin",
                "Musterstraße 123",
                "Berlin",
                "Germany",
                "10115",
                52.5200,
                13.4050,
                "John Doe",
                "john@example.com",
                "+49-30-12345678",
            )

    def test_create_event_with_invalid_time(self):
        """Test creating event with invalid time"""
        with pytest.raises(ValueError, match="Invalid time format"):
            self.event_manager.create_event(
                "Tech Conference",
                "Description",
                "2024-09-15",
                "invalid-time",
                "17:00:00",
                "Europe/Berlin",
                "Musterstraße 123",
                "Berlin",
                "Germany",
                "10115",
                52.5200,
                13.4050,
                "John Doe",
                "john@example.com",
                "+49-30-12345678",
            )

    def test_create_event_with_invalid_timezone(self):
        """Test creating event with invalid timezone"""
        with pytest.raises(ValueError, match="Invalid timezone"):
            self.event_manager.create_event(
                "Tech Conference",
                "Description",
                "2024-09-15",
                "09:00:00",
                "17:00:00",
                "Invalid/Timezone",
                "Musterstraße 123",
                "Berlin",
                "Germany",
                "10115",
                52.5200,
                13.4050,
                "John Doe",
                "john@example.com",
                "+49-30-12345678",
            )

    def test_create_event_with_invalid_time_range(self):
        """Test creating event with invalid time range"""
        with pytest.raises(ValueError, match="End time must be after start time"):
            self.event_manager.create_event(
                "Tech Conference",
                "Description",
                "2024-09-15",
                "17:00:00",
                "09:00:00",
                "Europe/Berlin",
                "Musterstraße 123",
                "Berlin",
                "Germany",
                "10115",
                52.5200,
                13.4050,
                "John Doe",
                "john@example.com",
                "+49-30-12345678",
            )

    def test_create_event_with_invalid_address(self):
        """Test creating event with invalid address"""
        with pytest.raises(ValueError, match="Invalid address information"):
            self.event_manager.create_event(
                "Tech Conference",
                "Description",
                "2024-09-15",
                "09:00:00",
                "17:00:00",
                "Europe/Berlin",
                "",  # empty street
                "Berlin",
                "Germany",
                "10115",
                52.5200,
                13.4050,
                "John Doe",
                "john@example.com",
                "+49-30-12345678",
            )

    def test_create_event_with_invalid_coordinates(self):
        """Test creating event with invalid coordinates"""
        with pytest.raises(ValueError, match="Invalid coordinates"):
            self.event_manager.create_event(
                "Tech Conference",
                "Description",
                "2024-09-15",
                "09:00:00",
                "17:00:00",
                "Europe/Berlin",
                "Musterstraße 123",
                "Berlin",
                "Germany",
                "10115",
                200.0,  # invalid latitude
                13.4050,
                "John Doe",
                "john@example.com",
                "+49-30-12345678",
            )

    def test_create_event_with_invalid_contact(self):
        """Test creating event with invalid contact"""
        with pytest.raises(ValueError, match="Invalid organizer contact information"):
            self.event_manager.create_event(
                "Tech Conference",
                "Description",
                "2024-09-15",
                "09:00:00",
                "17:00:00",
                "Europe/Berlin",
                "Musterstraße 123",
                "Berlin",
                "Germany",
                "10115",
                52.5200,
                13.4050,
                "John Doe",
                "invalid-email",
                "+49-30-12345678",
            )

    def test_update_event_timing(self):
        """Test updating event timing"""
        event = self.event_manager.create_event(
            "Tech Conference",
            "Description",
            "2024-09-15",
            "09:00:00",
            "17:00:00",
            "Europe/Berlin",
            "Musterstraße 123",
            "Berlin",
            "Germany",
            "10115",
            52.5200,
            13.4050,
            "John Doe",
            "john@example.com",
            "+49-30-12345678",
        )

        result = self.event_manager.update_event_timing(
            event.id, "2024-09-20", "10:00:00", "18:00:00", "Europe/London"
        )

        assert result is True

        events = self.event_manager.get_events()
        updated_event = next(e for e in events if e.id == event.id)

        assert updated_event.date == "2024-09-20"
        assert updated_event.start_time == "10:00:00"
        assert updated_event.end_time == "18:00:00"
        assert updated_event.timezone == "Europe/London"

    def test_update_event_timing_with_invalid_event_id(self):
        """Test updating event timing with invalid event id"""
        result = self.event_manager.update_event_timing(
            "invalid-id", "2024-09-20", "10:00:00", "18:00:00", "Europe/London"
        )

        assert result is False

    def test_update_event_location(self):
        """Test updating event location"""
        event = self.event_manager.create_event(
            "Tech Conference",
            "Description",
            "2024-09-15",
            "09:00:00",
            "17:00:00",
            "Europe/Berlin",
            "Musterstraße 123",
            "Berlin",
            "Germany",
            "10115",
            52.5200,
            13.4050,
            "John Doe",
            "john@example.com",
            "+49-30-12345678",
        )

        result = self.event_manager.update_event_location(
            event.id, "New Street 456", "Munich", "Germany", "80331", 48.1351, 11.5820
        )

        assert result is True

        events = self.event_manager.get_events()
        updated_event = next(e for e in events if e.id == event.id)

        assert updated_event.street == "New Street 456"
        assert updated_event.city == "Munich"
        assert updated_event.postal_code == "80331"
        assert updated_event.latitude == 48.1351
        assert updated_event.longitude == 11.5820

    def test_register_venue(self):
        """Test registering venue"""
        venue = self.event_manager.register_venue(
            "Convention Center",
            "Large convention center",
            "Convention Street 1",
            "Hamburg",
            "Germany",
            "20095",
            53.5511,
            9.9937,
            "Jane Smith",
            "jane@venue.com",
            "+49-40-987654321",
            500,
        )

        assert venue.id is not None
        assert venue.name == "Convention Center"
        assert venue.street == "Convention Street 1"
        assert venue.city == "Hamburg"
        assert venue.country == "Germany"
        assert venue.postal_code == "20095"
        assert venue.latitude == 53.5511
        assert venue.longitude == 9.9937
        assert venue.contact_name == "Jane Smith"
        assert venue.contact_email == "jane@venue.com"
        assert venue.contact_phone == "+49-40-987654321"
        assert venue.capacity == 500

    def test_send_event_notification(self):
        """Test sending event notification"""
        event = self.event_manager.create_event(
            "Tech Conference",
            "Description",
            "2024-09-15",
            "09:00:00",
            "17:00:00",
            "Europe/Berlin",
            "Musterstraße 123",
            "Berlin",
            "Germany",
            "10115",
            52.5200,
            13.4050,
            "John Doe",
            "john@example.com",
            "+49-30-12345678",
        )

        result = self.event_manager.send_event_notification(
            event.id,
            "John Doe",
            "john@example.com",
            "+49-30-12345678",
            "Event reminder: Your event is tomorrow!",
        )

        assert result is True

        notifications = self.event_manager.get_notifications()
        assert len(notifications) == 1

        notification = notifications[0]
        assert notification.event_id == event.id
        assert notification.organizer_name == "John Doe"
        assert notification.organizer_email == "john@example.com"
        assert notification.organizer_phone == "+49-30-12345678"
        assert notification.message == "Event reminder: Your event is tomorrow!"

    def test_schedule_recurring_event(self):
        """Test scheduling recurring event"""
        base_event = self.event_manager.create_event(
            "Weekly Meeting",
            "Team meeting",
            "2024-09-15",
            "14:00:00",
            "15:00:00",
            "Europe/Berlin",
            "Office Street 1",
            "Berlin",
            "Germany",
            "10115",
            52.5200,
            13.4050,
            "John Doe",
            "john@example.com",
            "+49-30-12345678",
        )

        recurring_events = self.event_manager.schedule_recurring_event(
            base_event.id,
            "weekly",
            3,
            "2024-09-15",
            "14:00:00",
            "15:00:00",
            "Europe/Berlin",
        )

        assert len(recurring_events) == 3

        assert recurring_events[0].date == "2024-09-15"
        assert recurring_events[1].date == "2024-09-22"
        assert recurring_events[2].date == "2024-09-29"

        for event in recurring_events:
            assert event.start_time == "14:00:00"
            assert event.end_time == "15:00:00"
            assert event.timezone == "Europe/Berlin"
            assert "Recurring" in event.title

    def test_calculate_distance(self):
        """Test calculating distance between coordinates"""
        distance = self.event_manager.calculate_distance(
            52.5200, 13.4050, 48.1351, 11.5820  # Berlin  # Munich
        )

        assert 500 < distance < 600

    def test_calculate_distance_with_invalid_coordinates(self):
        """Test calculating distance with invalid coordinates"""
        with pytest.raises(ValueError, match="Invalid coordinates"):
            self.event_manager.calculate_distance(
                200.0, 13.4050, 48.1351, 11.5820  # invalid latitude
            )

    def test_find_events_in_date_range(self):
        """Test finding events in date range"""
        self.event_manager.create_event(
            "Event 1",
            "Description",
            "2024-09-15",
            "09:00:00",
            "17:00:00",
            "Europe/Berlin",
            "Street 1",
            "Berlin",
            "Germany",
            "10115",
            52.5200,
            13.4050,
            "John Doe",
            "john@example.com",
            "+49-30-12345678",
        )

        self.event_manager.create_event(
            "Event 2",
            "Description",
            "2024-09-20",
            "10:00:00",
            "18:00:00",
            "Europe/Berlin",
            "Street 2",
            "Berlin",
            "Germany",
            "10115",
            52.5200,
            13.4050,
            "Jane Doe",
            "jane@example.com",
            "+49-30-87654321",
        )

        events = self.event_manager.find_events_in_date_range(
            "2024-09-14", "00:00:00", "2024-09-16", "23:59:59", "Europe/Berlin"
        )

        assert len(events) == 1
        assert events[0].title == "Event 1"

    def test_convert_time_to_timezone(self):
        """Test converting time to timezone"""
        result = self.event_manager.convert_time_to_timezone(
            "2024-09-15", "14:00:00", "Europe/Berlin", "America/New_York"
        )

        assert result.date == "2024-09-15"
        assert result.time == "08:00:00"
        assert result.timezone == "America/New_York"

    def test_convert_time_to_timezone_with_invalid_timezone(self):
        """Test converting time to timezone with invalid timezone"""
        with pytest.raises(ValueError, match="Invalid timezone"):
            self.event_manager.convert_time_to_timezone(
                "2024-09-15", "14:00:00", "Invalid/Timezone", "America/New_York"
            )
