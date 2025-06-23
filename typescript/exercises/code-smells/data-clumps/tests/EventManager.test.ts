import { EventManager } from '../src/EventManager';

describe('EventManager', () => {
  let eventManager: EventManager;

  beforeEach(() => {
    eventManager = new EventManager();
  });

  describe('createEvent', () => {
    test('should create event with valid data', () => {
      const event = eventManager.createEvent(
        'Tech Conference',
        'Annual technology conference',
        '2024-09-15',
        '09:00:00',
        '17:00:00',
        'Europe/Berlin',
        'Musterstraße 123',
        'Berlin',
        'Germany',
        '10115',
        52.52,
        13.405,
        'John Doe',
        'john@example.com',
        '+49-30-12345678',
        200,
        50.0
      );

      expect(event.id).toBeDefined();
      expect(event.title).toBe('Tech Conference');
      expect(event.date).toBe('2024-09-15');
      expect(event.startTime).toBe('09:00:00');
      expect(event.endTime).toBe('17:00:00');
      expect(event.timezone).toBe('Europe/Berlin');
      expect(event.street).toBe('Musterstraße 123');
      expect(event.city).toBe('Berlin');
      expect(event.country).toBe('Germany');
      expect(event.postalCode).toBe('10115');
      expect(event.latitude).toBe(52.52);
      expect(event.longitude).toBe(13.405);
      expect(event.organizerName).toBe('John Doe');
      expect(event.organizerEmail).toBe('john@example.com');
      expect(event.organizerPhone).toBe('+49-30-12345678');
      expect(event.maxAttendees).toBe(200);
      expect(event.ticketPrice).toBe(50.0);
      expect(event.status).toBe('active');
    });

    test('should throw error for invalid date', () => {
      expect(() => {
        eventManager.createEvent(
          'Tech Conference',
          'Description',
          'invalid-date',
          '09:00:00',
          '17:00:00',
          'Europe/Berlin',
          'Musterstraße 123',
          'Berlin',
          'Germany',
          '10115',
          52.52,
          13.405,
          'John Doe',
          'john@example.com',
          '+49-30-12345678'
        );
      }).toThrow('Invalid date format');
    });

    test('should throw error for invalid time', () => {
      expect(() => {
        eventManager.createEvent(
          'Tech Conference',
          'Description',
          '2024-09-15',
          'invalid-time',
          '17:00:00',
          'Europe/Berlin',
          'Musterstraße 123',
          'Berlin',
          'Germany',
          '10115',
          52.52,
          13.405,
          'John Doe',
          'john@example.com',
          '+49-30-12345678'
        );
      }).toThrow('Invalid time format');
    });

    test('should throw error for invalid timezone', () => {
      expect(() => {
        eventManager.createEvent(
          'Tech Conference',
          'Description',
          '2024-09-15',
          '09:00:00',
          '17:00:00',
          'Invalid/Timezone',
          'Musterstraße 123',
          'Berlin',
          'Germany',
          '10115',
          52.52,
          13.405,
          'John Doe',
          'john@example.com',
          '+49-30-12345678'
        );
      }).toThrow('Invalid timezone');
    });

    test('should throw error for invalid time range', () => {
      expect(() => {
        eventManager.createEvent(
          'Tech Conference',
          'Description',
          '2024-09-15',
          '17:00:00',
          '09:00:00',
          'Europe/Berlin',
          'Musterstraße 123',
          'Berlin',
          'Germany',
          '10115',
          52.52,
          13.405,
          'John Doe',
          'john@example.com',
          '+49-30-12345678'
        );
      }).toThrow('End time must be after start time');
    });

    test('should throw error for invalid address', () => {
      expect(() => {
        eventManager.createEvent(
          'Tech Conference',
          'Description',
          '2024-09-15',
          '09:00:00',
          '17:00:00',
          'Europe/Berlin',
          '', // empty street
          'Berlin',
          'Germany',
          '10115',
          52.52,
          13.405,
          'John Doe',
          'john@example.com',
          '+49-30-12345678'
        );
      }).toThrow('Invalid address information');
    });

    test('should throw error for invalid coordinates', () => {
      expect(() => {
        eventManager.createEvent(
          'Tech Conference',
          'Description',
          '2024-09-15',
          '09:00:00',
          '17:00:00',
          'Europe/Berlin',
          'Musterstraße 123',
          'Berlin',
          'Germany',
          '10115',
          200.0, // invalid latitude
          13.405,
          'John Doe',
          'john@example.com',
          '+49-30-12345678'
        );
      }).toThrow('Invalid coordinates');
    });

    test('should throw error for invalid contact', () => {
      expect(() => {
        eventManager.createEvent(
          'Tech Conference',
          'Description',
          '2024-09-15',
          '09:00:00',
          '17:00:00',
          'Europe/Berlin',
          'Musterstraße 123',
          'Berlin',
          'Germany',
          '10115',
          52.52,
          13.405,
          'John Doe',
          'invalid-email',
          '+49-30-12345678'
        );
      }).toThrow('Invalid organizer contact information');
    });
  });

  describe('updateEventTiming', () => {
    test('should update event timing', () => {
      const event = eventManager.createEvent(
        'Tech Conference',
        'Description',
        '2024-09-15',
        '09:00:00',
        '17:00:00',
        'Europe/Berlin',
        'Musterstraße 123',
        'Berlin',
        'Germany',
        '10115',
        52.52,
        13.405,
        'John Doe',
        'john@example.com',
        '+49-30-12345678'
      );

      const result = eventManager.updateEventTiming(
        event.id,
        '2024-09-20',
        '10:00:00',
        '18:00:00',
        'Europe/London'
      );

      expect(result).toBe(true);

      const events = eventManager.getEvents();
      const updatedEvent = events.find(e => e.id === event.id)!;

      expect(updatedEvent.date).toBe('2024-09-20');
      expect(updatedEvent.startTime).toBe('10:00:00');
      expect(updatedEvent.endTime).toBe('18:00:00');
      expect(updatedEvent.timezone).toBe('Europe/London');
    });

    test('should return false for invalid event id', () => {
      const result = eventManager.updateEventTiming(
        'invalid-id',
        '2024-09-20',
        '10:00:00',
        '18:00:00',
        'Europe/London'
      );

      expect(result).toBe(false);
    });
  });

  describe('updateEventLocation', () => {
    test('should update event location', () => {
      const event = eventManager.createEvent(
        'Tech Conference',
        'Description',
        '2024-09-15',
        '09:00:00',
        '17:00:00',
        'Europe/Berlin',
        'Musterstraße 123',
        'Berlin',
        'Germany',
        '10115',
        52.52,
        13.405,
        'John Doe',
        'john@example.com',
        '+49-30-12345678'
      );

      const result = eventManager.updateEventLocation(
        event.id,
        'New Street 456',
        'Munich',
        'Germany',
        '80331',
        48.1351,
        11.582
      );

      expect(result).toBe(true);

      const events = eventManager.getEvents();
      const updatedEvent = events.find(e => e.id === event.id)!;

      expect(updatedEvent.street).toBe('New Street 456');
      expect(updatedEvent.city).toBe('Munich');
      expect(updatedEvent.postalCode).toBe('80331');
      expect(updatedEvent.latitude).toBe(48.1351);
      expect(updatedEvent.longitude).toBe(11.582);
    });
  });

  describe('registerVenue', () => {
    test('should register venue', () => {
      const venue = eventManager.registerVenue(
        'Convention Center',
        'Large convention center',
        'Convention Street 1',
        'Hamburg',
        'Germany',
        '20095',
        53.5511,
        9.9937,
        'Jane Smith',
        'jane@venue.com',
        '+49-40-987654321',
        500
      );

      expect(venue.id).toBeDefined();
      expect(venue.name).toBe('Convention Center');
      expect(venue.street).toBe('Convention Street 1');
      expect(venue.city).toBe('Hamburg');
      expect(venue.country).toBe('Germany');
      expect(venue.postalCode).toBe('20095');
      expect(venue.latitude).toBe(53.5511);
      expect(venue.longitude).toBe(9.9937);
      expect(venue.contactName).toBe('Jane Smith');
      expect(venue.contactEmail).toBe('jane@venue.com');
      expect(venue.contactPhone).toBe('+49-40-987654321');
      expect(venue.capacity).toBe(500);
    });
  });

  describe('sendEventNotification', () => {
    test('should send event notification', () => {
      const event = eventManager.createEvent(
        'Tech Conference',
        'Description',
        '2024-09-15',
        '09:00:00',
        '17:00:00',
        'Europe/Berlin',
        'Musterstraße 123',
        'Berlin',
        'Germany',
        '10115',
        52.52,
        13.405,
        'John Doe',
        'john@example.com',
        '+49-30-12345678'
      );

      const result = eventManager.sendEventNotification(
        event.id,
        'John Doe',
        'john@example.com',
        '+49-30-12345678',
        'Event reminder: Your event is tomorrow!'
      );

      expect(result).toBe(true);

      const notifications = eventManager.getNotifications();
      expect(notifications).toHaveLength(1);

      const notification = notifications[0]!;
      expect(notification.eventId).toBe(event.id);
      expect(notification.organizerName).toBe('John Doe');
      expect(notification.organizerEmail).toBe('john@example.com');
      expect(notification.organizerPhone).toBe('+49-30-12345678');
      expect(notification.message).toBe(
        'Event reminder: Your event is tomorrow!'
      );
    });
  });

  describe('scheduleRecurringEvent', () => {
    test('should schedule recurring event', () => {
      const baseEvent = eventManager.createEvent(
        'Weekly Meeting',
        'Team meeting',
        '2024-09-15',
        '14:00:00',
        '15:00:00',
        'Europe/Berlin',
        'Office Street 1',
        'Berlin',
        'Germany',
        '10115',
        52.52,
        13.405,
        'John Doe',
        'john@example.com',
        '+49-30-12345678'
      );

      const recurringEvents = eventManager.scheduleRecurringEvent(
        baseEvent.id,
        'weekly',
        3,
        '2024-09-15',
        '14:00:00',
        '15:00:00',
        'Europe/Berlin'
      );

      expect(recurringEvents).toHaveLength(3);

      expect(recurringEvents[0]!.date).toBe('2024-09-15');
      expect(recurringEvents[1]!.date).toBe('2024-09-22');
      expect(recurringEvents[2]!.date).toBe('2024-09-29');

      recurringEvents.forEach(event => {
        expect(event.startTime).toBe('14:00:00');
        expect(event.endTime).toBe('15:00:00');
        expect(event.timezone).toBe('Europe/Berlin');
        expect(event.title).toContain('Recurring');
      });
    });
  });

  describe('calculateDistance', () => {
    test('should calculate distance between coordinates', () => {
      const distance = eventManager.calculateDistance(
        52.52, // Berlin
        13.405,
        48.1351, // Munich
        11.582
      );

      expect(distance).toBeGreaterThan(500);
      expect(distance).toBeLessThan(600);
    });

    test('should throw error for invalid coordinates', () => {
      expect(() => {
        eventManager.calculateDistance(
          200.0, // invalid latitude
          13.405,
          48.1351,
          11.582
        );
      }).toThrow('Invalid coordinates');
    });
  });

  describe('findEventsInDateRange', () => {
    test('should find events in date range', () => {
      eventManager.createEvent(
        'Event 1',
        'Description',
        '2024-09-15',
        '09:00:00',
        '17:00:00',
        'Europe/Berlin',
        'Street 1',
        'Berlin',
        'Germany',
        '10115',
        52.52,
        13.405,
        'John Doe',
        'john@example.com',
        '+49-30-12345678'
      );

      eventManager.createEvent(
        'Event 2',
        'Description',
        '2024-09-20',
        '10:00:00',
        '18:00:00',
        'Europe/Berlin',
        'Street 2',
        'Berlin',
        'Germany',
        '10115',
        52.52,
        13.405,
        'Jane Doe',
        'jane@example.com',
        '+49-30-87654321'
      );

      const events = eventManager.findEventsInDateRange(
        '2024-09-14',
        '00:00:00',
        '2024-09-16',
        '23:59:59',
        'Europe/Berlin'
      );

      expect(events).toHaveLength(1);
      expect(events[0]!.title).toBe('Event 1');
    });
  });

  describe('convertTimeToTimezone', () => {
    test('should convert time to timezone', () => {
      const result = eventManager.convertTimeToTimezone(
        '2024-09-15',
        '14:00:00',
        'Europe/Berlin',
        'America/New_York'
      );

      expect(result.date).toBe('2024-09-15');
      expect(result.time).toBe('08:00:00');
      expect(result.timezone).toBe('America/New_York');
    });

    test('should throw error for invalid timezone', () => {
      expect(() => {
        eventManager.convertTimeToTimezone(
          '2024-09-15',
          '14:00:00',
          'Invalid/Timezone',
          'America/New_York'
        );
      }).toThrow('Invalid timezone');
    });
  });
});
