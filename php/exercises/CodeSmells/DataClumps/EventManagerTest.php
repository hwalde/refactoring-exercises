<?php

declare(strict_types=1);

namespace RefactoringExercises\CodeSmells\DataClumps;

use PHPUnit\Framework\TestCase;

class EventManagerTest extends TestCase
{
    private EventManager $eventManager;

    protected function setUp(): void
    {
        $this->eventManager = new EventManager();
    }

    public function testCreateEventWithValidData(): void
    {
        $event = $this->eventManager->createEvent(
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
            52.5200,
            13.4050,
            'John Doe',
            'john@example.com',
            '+49-30-12345678',
            200,
            50.0
        );

        $this->assertNotEmpty($event['id']);
        $this->assertEquals('Tech Conference', $event['title']);
        $this->assertEquals('2024-09-15', $event['date']);
        $this->assertEquals('09:00:00', $event['startTime']);
        $this->assertEquals('17:00:00', $event['endTime']);
        $this->assertEquals('Europe/Berlin', $event['timezone']);
        $this->assertEquals('Musterstraße 123', $event['street']);
        $this->assertEquals('Berlin', $event['city']);
        $this->assertEquals('Germany', $event['country']);
        $this->assertEquals('10115', $event['postalCode']);
        $this->assertEquals(52.5200, $event['latitude']);
        $this->assertEquals(13.4050, $event['longitude']);
        $this->assertEquals('John Doe', $event['organizerName']);
        $this->assertEquals('john@example.com', $event['organizerEmail']);
        $this->assertEquals('+49-30-12345678', $event['organizerPhone']);
        $this->assertEquals(200, $event['maxAttendees']);
        $this->assertEquals(50.0, $event['ticketPrice']);
        $this->assertEquals('active', $event['status']);
    }

    public function testCreateEventWithInvalidDate(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid date format');

        $this->eventManager->createEvent(
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
            52.5200,
            13.4050,
            'John Doe',
            'john@example.com',
            '+49-30-12345678'
        );
    }

    public function testCreateEventWithInvalidTime(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid time format');

        $this->eventManager->createEvent(
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
            52.5200,
            13.4050,
            'John Doe',
            'john@example.com',
            '+49-30-12345678'
        );
    }

    public function testCreateEventWithInvalidTimezone(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid timezone');

        $this->eventManager->createEvent(
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
            52.5200,
            13.4050,
            'John Doe',
            'john@example.com',
            '+49-30-12345678'
        );
    }

    public function testCreateEventWithInvalidTimeRange(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('End time must be after start time');

        $this->eventManager->createEvent(
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
            52.5200,
            13.4050,
            'John Doe',
            'john@example.com',
            '+49-30-12345678'
        );
    }

    public function testCreateEventWithInvalidAddress(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid address information');

        $this->eventManager->createEvent(
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
            52.5200,
            13.4050,
            'John Doe',
            'john@example.com',
            '+49-30-12345678'
        );
    }

    public function testCreateEventWithInvalidCoordinates(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid coordinates');

        $this->eventManager->createEvent(
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
            13.4050,
            'John Doe',
            'john@example.com',
            '+49-30-12345678'
        );
    }

    public function testCreateEventWithInvalidContact(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid organizer contact information');

        $this->eventManager->createEvent(
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
            52.5200,
            13.4050,
            'John Doe',
            'invalid-email',
            '+49-30-12345678'
        );
    }

    public function testUpdateEventTiming(): void
    {
        $event = $this->eventManager->createEvent(
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
            52.5200,
            13.4050,
            'John Doe',
            'john@example.com',
            '+49-30-12345678'
        );

        $result = $this->eventManager->updateEventTiming(
            $event['id'],
            '2024-09-20',
            '10:00:00',
            '18:00:00',
            'Europe/London'
        );

        $this->assertTrue($result);
        
        $events = $this->eventManager->getEvents();
        $updatedEvent = $events[$event['id']];
        
        $this->assertEquals('2024-09-20', $updatedEvent['date']);
        $this->assertEquals('10:00:00', $updatedEvent['startTime']);
        $this->assertEquals('18:00:00', $updatedEvent['endTime']);
        $this->assertEquals('Europe/London', $updatedEvent['timezone']);
    }

    public function testUpdateEventTimingWithInvalidEventId(): void
    {
        $result = $this->eventManager->updateEventTiming(
            'invalid-id',
            '2024-09-20',
            '10:00:00',
            '18:00:00',
            'Europe/London'
        );

        $this->assertFalse($result);
    }

    public function testUpdateEventLocation(): void
    {
        $event = $this->eventManager->createEvent(
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
            52.5200,
            13.4050,
            'John Doe',
            'john@example.com',
            '+49-30-12345678'
        );

        $result = $this->eventManager->updateEventLocation(
            $event['id'],
            'New Street 456',
            'Munich',
            'Germany',
            '80331',
            48.1351,
            11.5820
        );

        $this->assertTrue($result);
        
        $events = $this->eventManager->getEvents();
        $updatedEvent = $events[$event['id']];
        
        $this->assertEquals('New Street 456', $updatedEvent['street']);
        $this->assertEquals('Munich', $updatedEvent['city']);
        $this->assertEquals('80331', $updatedEvent['postalCode']);
        $this->assertEquals(48.1351, $updatedEvent['latitude']);
        $this->assertEquals(11.5820, $updatedEvent['longitude']);
    }

    public function testRegisterVenue(): void
    {
        $venue = $this->eventManager->registerVenue(
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

        $this->assertNotEmpty($venue['id']);
        $this->assertEquals('Convention Center', $venue['name']);
        $this->assertEquals('Convention Street 1', $venue['street']);
        $this->assertEquals('Hamburg', $venue['city']);
        $this->assertEquals('Germany', $venue['country']);
        $this->assertEquals('20095', $venue['postalCode']);
        $this->assertEquals(53.5511, $venue['latitude']);
        $this->assertEquals(9.9937, $venue['longitude']);
        $this->assertEquals('Jane Smith', $venue['contactName']);
        $this->assertEquals('jane@venue.com', $venue['contactEmail']);
        $this->assertEquals('+49-40-987654321', $venue['contactPhone']);
        $this->assertEquals(500, $venue['capacity']);
    }

    public function testSendEventNotification(): void
    {
        $event = $this->eventManager->createEvent(
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
            52.5200,
            13.4050,
            'John Doe',
            'john@example.com',
            '+49-30-12345678'
        );

        $result = $this->eventManager->sendEventNotification(
            $event['id'],
            'John Doe',
            'john@example.com',
            '+49-30-12345678',
            'Event reminder: Your event is tomorrow!'
        );

        $this->assertTrue($result);
        
        $notifications = $this->eventManager->getNotifications();
        $this->assertCount(1, $notifications);
        
        $notification = array_values($notifications)[0];
        $this->assertEquals($event['id'], $notification['eventId']);
        $this->assertEquals('John Doe', $notification['organizerName']);
        $this->assertEquals('john@example.com', $notification['organizerEmail']);
        $this->assertEquals('+49-30-12345678', $notification['organizerPhone']);
        $this->assertEquals('Event reminder: Your event is tomorrow!', $notification['message']);
    }

    public function testScheduleRecurringEvent(): void
    {
        $baseEvent = $this->eventManager->createEvent(
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
            52.5200,
            13.4050,
            'John Doe',
            'john@example.com',
            '+49-30-12345678'
        );

        $recurringEvents = $this->eventManager->scheduleRecurringEvent(
            $baseEvent['id'],
            'weekly',
            3,
            '2024-09-15',
            '14:00:00',
            '15:00:00',
            'Europe/Berlin'
        );

        $this->assertCount(3, $recurringEvents);
        
        $this->assertEquals('2024-09-15', $recurringEvents[0]['date']);
        $this->assertEquals('2024-09-22', $recurringEvents[1]['date']);
        $this->assertEquals('2024-09-29', $recurringEvents[2]['date']);
        
        foreach ($recurringEvents as $event) {
            $this->assertEquals('14:00:00', $event['startTime']);
            $this->assertEquals('15:00:00', $event['endTime']);
            $this->assertEquals('Europe/Berlin', $event['timezone']);
            $this->assertStringContainsString('Recurring', $event['title']);
        }
    }

    public function testCalculateDistance(): void
    {
        $distance = $this->eventManager->calculateDistance(
            52.5200, // Berlin
            13.4050,
            48.1351, // Munich
            11.5820
        );

        $this->assertGreaterThan(500, $distance);
        $this->assertLessThan(600, $distance);
    }

    public function testCalculateDistanceWithInvalidCoordinates(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid coordinates');

        $this->eventManager->calculateDistance(
            200.0, // invalid latitude
            13.4050,
            48.1351,
            11.5820
        );
    }

    public function testFindEventsInDateRange(): void
    {
        $this->eventManager->createEvent(
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
            52.5200,
            13.4050,
            'John Doe',
            'john@example.com',
            '+49-30-12345678'
        );

        $this->eventManager->createEvent(
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
            52.5200,
            13.4050,
            'Jane Doe',
            'jane@example.com',
            '+49-30-87654321'
        );

        $events = $this->eventManager->findEventsInDateRange(
            '2024-09-14',
            '00:00:00',
            '2024-09-16',
            '23:59:59',
            'Europe/Berlin'
        );

        $this->assertCount(1, $events);
        $this->assertEquals('Event 1', $events[0]['title']);
    }

    public function testConvertTimeToTimezone(): void
    {
        $result = $this->eventManager->convertTimeToTimezone(
            '2024-09-15',
            '14:00:00',
            'Europe/Berlin',
            'America/New_York'
        );

        $this->assertEquals('2024-09-15', $result['date']);
        $this->assertEquals('08:00:00', $result['time']);
        $this->assertEquals('America/New_York', $result['timezone']);
    }

    public function testConvertTimeToTimezoneWithInvalidTimezone(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid timezone');

        $this->eventManager->convertTimeToTimezone(
            '2024-09-15',
            '14:00:00',
            'Invalid/Timezone',
            'America/New_York'
        );
    }
}