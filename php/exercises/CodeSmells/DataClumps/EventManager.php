<?php

declare(strict_types=1);

namespace RefactoringExercises\CodeSmells\DataClumps;

/**
 * EventManager handles event creation and management
 *
 * This class demonstrates the "Data Clumps" code smell by having multiple methods
 * that repeatedly use the same groups of parameters together:
 * - Date, time, and timezone parameters
 * - Address components (street, city, country, postal code)
 * - Coordinate parameters (latitude, longitude)
 * - Contact information (name, email, phone)
 * 
 * These parameter groups should be refactored into Parameter Objects.
 */
class EventManager
{
    private array $events = [];
    private array $venues = [];
    private array $notifications = [];

    /**
     * Creates a new event with date/time, location, and organizer information
     */
    public function createEvent(
        string $title,
        string $description,
        string $date,
        string $startTime,
        string $endTime,
        string $timezone,
        string $street,
        string $city,
        string $country,
        string $postalCode,
        float $latitude,
        float $longitude,
        string $organizerName,
        string $organizerEmail,
        string $organizerPhone,
        int $maxAttendees = 100,
        float $ticketPrice = 0.0
    ): array {
        // Validate date and time
        if (!$this->isValidDate($date)) {
            throw new \InvalidArgumentException('Invalid date format');
        }
        
        if (!$this->isValidTime($startTime) || !$this->isValidTime($endTime)) {
            throw new \InvalidArgumentException('Invalid time format');
        }
        
        if (!$this->isValidTimezone($timezone)) {
            throw new \InvalidArgumentException('Invalid timezone');
        }
        
        if (!$this->isTimeRangeValid($startTime, $endTime)) {
            throw new \InvalidArgumentException('End time must be after start time');
        }

        // Validate address
        if (!$this->isValidAddress($street, $city, $country, $postalCode)) {
            throw new \InvalidArgumentException('Invalid address information');
        }

        // Validate coordinates
        if (!$this->isValidCoordinates($latitude, $longitude)) {
            throw new \InvalidArgumentException('Invalid coordinates');
        }

        // Validate contact information
        if (!$this->isValidContact($organizerName, $organizerEmail, $organizerPhone)) {
            throw new \InvalidArgumentException('Invalid organizer contact information');
        }

        $eventId = $this->generateId();
        $event = [
            'id' => $eventId,
            'title' => $title,
            'description' => $description,
            'date' => $date,
            'startTime' => $startTime,
            'endTime' => $endTime,
            'timezone' => $timezone,
            'street' => $street,
            'city' => $city,
            'country' => $country,
            'postalCode' => $postalCode,
            'latitude' => $latitude,
            'longitude' => $longitude,
            'organizerName' => $organizerName,
            'organizerEmail' => $organizerEmail,
            'organizerPhone' => $organizerPhone,
            'maxAttendees' => $maxAttendees,
            'ticketPrice' => $ticketPrice,
            'attendees' => 0,
            'status' => 'active'
        ];

        $this->events[$eventId] = $event;
        return $event;
    }

    /**
     * Updates event timing information
     */
    public function updateEventTiming(
        string $eventId,
        string $date,
        string $startTime,
        string $endTime,
        string $timezone
    ): bool {
        if (!isset($this->events[$eventId])) {
            return false;
        }

        // Validate date and time
        if (!$this->isValidDate($date)) {
            throw new \InvalidArgumentException('Invalid date format');
        }
        
        if (!$this->isValidTime($startTime) || !$this->isValidTime($endTime)) {
            throw new \InvalidArgumentException('Invalid time format');
        }
        
        if (!$this->isValidTimezone($timezone)) {
            throw new \InvalidArgumentException('Invalid timezone');
        }
        
        if (!$this->isTimeRangeValid($startTime, $endTime)) {
            throw new \InvalidArgumentException('End time must be after start time');
        }

        $this->events[$eventId]['date'] = $date;
        $this->events[$eventId]['startTime'] = $startTime;
        $this->events[$eventId]['endTime'] = $endTime;
        $this->events[$eventId]['timezone'] = $timezone;

        return true;
    }

    /**
     * Updates event location information
     */
    public function updateEventLocation(
        string $eventId,
        string $street,
        string $city,
        string $country,
        string $postalCode,
        float $latitude,
        float $longitude
    ): bool {
        if (!isset($this->events[$eventId])) {
            return false;
        }

        // Validate address
        if (!$this->isValidAddress($street, $city, $country, $postalCode)) {
            throw new \InvalidArgumentException('Invalid address information');
        }

        // Validate coordinates
        if (!$this->isValidCoordinates($latitude, $longitude)) {
            throw new \InvalidArgumentException('Invalid coordinates');
        }

        $this->events[$eventId]['street'] = $street;
        $this->events[$eventId]['city'] = $city;
        $this->events[$eventId]['country'] = $country;
        $this->events[$eventId]['postalCode'] = $postalCode;
        $this->events[$eventId]['latitude'] = $latitude;
        $this->events[$eventId]['longitude'] = $longitude;

        return true;
    }

    /**
     * Registers a new venue with address and contact information
     */
    public function registerVenue(
        string $name,
        string $description,
        string $street,
        string $city,
        string $country,
        string $postalCode,
        float $latitude,
        float $longitude,
        string $contactName,
        string $contactEmail,
        string $contactPhone,
        int $capacity = 50
    ): array {
        // Validate address
        if (!$this->isValidAddress($street, $city, $country, $postalCode)) {
            throw new \InvalidArgumentException('Invalid address information');
        }

        // Validate coordinates
        if (!$this->isValidCoordinates($latitude, $longitude)) {
            throw new \InvalidArgumentException('Invalid coordinates');
        }

        // Validate contact information
        if (!$this->isValidContact($contactName, $contactEmail, $contactPhone)) {
            throw new \InvalidArgumentException('Invalid contact information');
        }

        $venueId = $this->generateId();
        $venue = [
            'id' => $venueId,
            'name' => $name,
            'description' => $description,
            'street' => $street,
            'city' => $city,
            'country' => $country,
            'postalCode' => $postalCode,
            'latitude' => $latitude,
            'longitude' => $longitude,
            'contactName' => $contactName,
            'contactEmail' => $contactEmail,
            'contactPhone' => $contactPhone,
            'capacity' => $capacity,
            'status' => 'active'
        ];

        $this->venues[$venueId] = $venue;
        return $venue;
    }

    /**
     * Sends event notification to organizer
     */
    public function sendEventNotification(
        string $eventId,
        string $organizerName,
        string $organizerEmail,
        string $organizerPhone,
        string $message
    ): bool {
        if (!isset($this->events[$eventId])) {
            return false;
        }

        // Validate contact information
        if (!$this->isValidContact($organizerName, $organizerEmail, $organizerPhone)) {
            throw new \InvalidArgumentException('Invalid organizer contact information');
        }

        $notificationId = $this->generateId();
        $notification = [
            'id' => $notificationId,
            'eventId' => $eventId,
            'organizerName' => $organizerName,
            'organizerEmail' => $organizerEmail,
            'organizerPhone' => $organizerPhone,
            'message' => $message,
            'sentAt' => date('Y-m-d H:i:s'),
            'status' => 'sent'
        ];

        $this->notifications[$notificationId] = $notification;
        return true;
    }

    /**
     * Schedules recurring event
     */
    public function scheduleRecurringEvent(
        string $baseEventId,
        string $pattern,
        int $occurrences,
        string $startDate,
        string $startTime,
        string $endTime,
        string $timezone
    ): array {
        if (!isset($this->events[$baseEventId])) {
            throw new \InvalidArgumentException('Base event not found');
        }

        // Validate date and time
        if (!$this->isValidDate($startDate)) {
            throw new \InvalidArgumentException('Invalid date format');
        }
        
        if (!$this->isValidTime($startTime) || !$this->isValidTime($endTime)) {
            throw new \InvalidArgumentException('Invalid time format');
        }
        
        if (!$this->isValidTimezone($timezone)) {
            throw new \InvalidArgumentException('Invalid timezone');
        }
        
        if (!$this->isTimeRangeValid($startTime, $endTime)) {
            throw new \InvalidArgumentException('End time must be after start time');
        }

        $recurringEvents = [];
        $baseEvent = $this->events[$baseEventId];

        for ($i = 0; $i < $occurrences; $i++) {
            $eventDate = $this->calculateNextDate($startDate, $pattern, $i);
            $eventId = $this->generateId();
            
            $event = $baseEvent;
            $event['id'] = $eventId;
            $event['date'] = $eventDate;
            $event['startTime'] = $startTime;
            $event['endTime'] = $endTime;
            $event['timezone'] = $timezone;
            $event['title'] = $baseEvent['title'] . ' (Recurring)';
            $event['attendees'] = 0;

            $this->events[$eventId] = $event;
            $recurringEvents[] = $event;
        }

        return $recurringEvents;
    }

    /**
     * Calculates distance between two coordinate points
     */
    public function calculateDistance(
        float $lat1,
        float $lon1,
        float $lat2,
        float $lon2
    ): float {
        if (!$this->isValidCoordinates($lat1, $lon1) || !$this->isValidCoordinates($lat2, $lon2)) {
            throw new \InvalidArgumentException('Invalid coordinates');
        }

        $earthRadius = 6371; // Earth's radius in kilometers
        
        $dLat = deg2rad($lat2 - $lat1);
        $dLon = deg2rad($lon2 - $lon1);
        
        $a = sin($dLat/2) * sin($dLat/2) + cos(deg2rad($lat1)) * cos(deg2rad($lat2)) * sin($dLon/2) * sin($dLon/2);
        $c = 2 * atan2(sqrt($a), sqrt(1-$a));
        
        return $earthRadius * $c;
    }

    /**
     * Finds events within date range
     */
    public function findEventsInDateRange(
        string $startDate,
        string $startTime,
        string $endDate,
        string $endTime,
        string $timezone
    ): array {
        // Validate date and time
        if (!$this->isValidDate($startDate) || !$this->isValidDate($endDate)) {
            throw new \InvalidArgumentException('Invalid date format');
        }
        
        if (!$this->isValidTime($startTime) || !$this->isValidTime($endTime)) {
            throw new \InvalidArgumentException('Invalid time format');
        }
        
        if (!$this->isValidTimezone($timezone)) {
            throw new \InvalidArgumentException('Invalid timezone');
        }

        $matchingEvents = [];
        
        foreach ($this->events as $event) {
            if ($this->isEventInDateRange($event, $startDate, $startTime, $endDate, $endTime, $timezone)) {
                $matchingEvents[] = $event;
            }
        }

        return $matchingEvents;
    }

    /**
     * Converts time to different timezone
     */
    public function convertTimeToTimezone(
        string $date,
        string $time,
        string $fromTimezone,
        string $toTimezone
    ): array {
        if (!$this->isValidDate($date)) {
            throw new \InvalidArgumentException('Invalid date format');
        }
        
        if (!$this->isValidTime($time)) {
            throw new \InvalidArgumentException('Invalid time format');
        }
        
        if (!$this->isValidTimezone($fromTimezone) || !$this->isValidTimezone($toTimezone)) {
            throw new \InvalidArgumentException('Invalid timezone');
        }

        $dateTime = new \DateTime($date . ' ' . $time, new \DateTimeZone($fromTimezone));
        $dateTime->setTimezone(new \DateTimeZone($toTimezone));

        return [
            'date' => $dateTime->format('Y-m-d'),
            'time' => $dateTime->format('H:i:s'),
            'timezone' => $toTimezone
        ];
    }

    // Validation methods (these contain the data clumps logic)
    private function isValidDate(string $date): bool
    {
        return (bool) preg_match('/^\d{4}-\d{2}-\d{2}$/', $date) && strtotime($date) !== false;
    }

    private function isValidTime(string $time): bool
    {
        return (bool) preg_match('/^\d{2}:\d{2}:\d{2}$/', $time);
    }

    private function isValidTimezone(string $timezone): bool
    {
        return in_array($timezone, timezone_identifiers_list());
    }

    private function isTimeRangeValid(string $startTime, string $endTime): bool
    {
        return strtotime($startTime) < strtotime($endTime);
    }

    private function isValidAddress(string $street, string $city, string $country, string $postalCode): bool
    {
        return !empty($street) && !empty($city) && !empty($country) && !empty($postalCode);
    }

    private function isValidCoordinates(float $latitude, float $longitude): bool
    {
        return $latitude >= -90 && $latitude <= 90 && $longitude >= -180 && $longitude <= 180;
    }

    private function isValidContact(string $name, string $email, string $phone): bool
    {
        return !empty($name) && 
               filter_var($email, FILTER_VALIDATE_EMAIL) !== false && 
               !empty($phone);
    }

    private function isEventInDateRange(
        array $event,
        string $startDate,
        string $startTime,
        string $endDate,
        string $endTime,
        string $timezone
    ): bool {
        // Simplified comparison - in real implementation would handle timezone conversion
        $eventDateTime = $event['date'] . ' ' . $event['startTime'];
        $rangeStart = $startDate . ' ' . $startTime;
        $rangeEnd = $endDate . ' ' . $endTime;
        
        return $eventDateTime >= $rangeStart && $eventDateTime <= $rangeEnd;
    }

    private function calculateNextDate(string $baseDate, string $pattern, int $occurrence): string
    {
        $date = new \DateTime($baseDate);
        
        switch ($pattern) {
            case 'daily':
                $date->add(new \DateInterval('P' . $occurrence . 'D'));
                break;
            case 'weekly':
                $date->add(new \DateInterval('P' . ($occurrence * 7) . 'D'));
                break;
            case 'monthly':
                $date->add(new \DateInterval('P' . $occurrence . 'M'));
                break;
        }
        
        return $date->format('Y-m-d');
    }

    private function generateId(): string
    {
        return 'evt_' . uniqid();
    }

    // Getters for testing
    public function getEvents(): array
    {
        return $this->events;
    }

    public function getVenues(): array
    {
        return $this->venues;
    }

    public function getNotifications(): array
    {
        return $this->notifications;
    }
}