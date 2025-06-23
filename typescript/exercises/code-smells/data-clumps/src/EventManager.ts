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

interface Event {
  id: string;
  title: string;
  description: string;
  date: string;
  startTime: string;
  endTime: string;
  timezone: string;
  street: string;
  city: string;
  country: string;
  postalCode: string;
  latitude: number;
  longitude: number;
  organizerName: string;
  organizerEmail: string;
  organizerPhone: string;
  maxAttendees: number;
  ticketPrice: number;
  attendees: number;
  status: string;
}

interface Venue {
  id: string;
  name: string;
  description: string;
  street: string;
  city: string;
  country: string;
  postalCode: string;
  latitude: number;
  longitude: number;
  contactName: string;
  contactEmail: string;
  contactPhone: string;
  capacity: number;
  status: string;
}

interface Notification {
  id: string;
  eventId: string;
  organizerName: string;
  organizerEmail: string;
  organizerPhone: string;
  message: string;
  sentAt: string;
  status: string;
}

interface TimeConversion {
  date: string;
  time: string;
  timezone: string;
}

export class EventManager {
  private events: Map<string, Event> = new Map();
  private venues: Map<string, Venue> = new Map();
  private notifications: Map<string, Notification> = new Map();

  /**
   * Creates a new event with date/time, location, and organizer information
   */
  createEvent(
    title: string,
    description: string,
    date: string,
    startTime: string,
    endTime: string,
    timezone: string,
    street: string,
    city: string,
    country: string,
    postalCode: string,
    latitude: number,
    longitude: number,
    organizerName: string,
    organizerEmail: string,
    organizerPhone: string,
    maxAttendees: number = 100,
    ticketPrice: number = 0.0
  ): Event {
    // Validate date and time
    if (!this.isValidDate(date)) {
      throw new Error('Invalid date format');
    }

    if (!this.isValidTime(startTime) || !this.isValidTime(endTime)) {
      throw new Error('Invalid time format');
    }

    if (!this.isValidTimezone(timezone)) {
      throw new Error('Invalid timezone');
    }

    if (!this.isTimeRangeValid(startTime, endTime)) {
      throw new Error('End time must be after start time');
    }

    // Validate address
    if (!this.isValidAddress(street, city, country, postalCode)) {
      throw new Error('Invalid address information');
    }

    // Validate coordinates
    if (!this.isValidCoordinates(latitude, longitude)) {
      throw new Error('Invalid coordinates');
    }

    // Validate contact information
    if (!this.isValidContact(organizerName, organizerEmail, organizerPhone)) {
      throw new Error('Invalid organizer contact information');
    }

    const eventId = this.generateId();
    const event: Event = {
      id: eventId,
      title,
      description,
      date,
      startTime,
      endTime,
      timezone,
      street,
      city,
      country,
      postalCode,
      latitude,
      longitude,
      organizerName,
      organizerEmail,
      organizerPhone,
      maxAttendees,
      ticketPrice,
      attendees: 0,
      status: 'active',
    };

    this.events.set(eventId, event);
    return event;
  }

  /**
   * Updates event timing information
   */
  updateEventTiming(
    eventId: string,
    date: string,
    startTime: string,
    endTime: string,
    timezone: string
  ): boolean {
    const event = this.events.get(eventId);
    if (!event) {
      return false;
    }

    // Validate date and time
    if (!this.isValidDate(date)) {
      throw new Error('Invalid date format');
    }

    if (!this.isValidTime(startTime) || !this.isValidTime(endTime)) {
      throw new Error('Invalid time format');
    }

    if (!this.isValidTimezone(timezone)) {
      throw new Error('Invalid timezone');
    }

    if (!this.isTimeRangeValid(startTime, endTime)) {
      throw new Error('End time must be after start time');
    }

    event.date = date;
    event.startTime = startTime;
    event.endTime = endTime;
    event.timezone = timezone;

    return true;
  }

  /**
   * Updates event location information
   */
  updateEventLocation(
    eventId: string,
    street: string,
    city: string,
    country: string,
    postalCode: string,
    latitude: number,
    longitude: number
  ): boolean {
    const event = this.events.get(eventId);
    if (!event) {
      return false;
    }

    // Validate address
    if (!this.isValidAddress(street, city, country, postalCode)) {
      throw new Error('Invalid address information');
    }

    // Validate coordinates
    if (!this.isValidCoordinates(latitude, longitude)) {
      throw new Error('Invalid coordinates');
    }

    event.street = street;
    event.city = city;
    event.country = country;
    event.postalCode = postalCode;
    event.latitude = latitude;
    event.longitude = longitude;

    return true;
  }

  /**
   * Registers a new venue with address and contact information
   */
  registerVenue(
    name: string,
    description: string,
    street: string,
    city: string,
    country: string,
    postalCode: string,
    latitude: number,
    longitude: number,
    contactName: string,
    contactEmail: string,
    contactPhone: string,
    capacity: number = 50
  ): Venue {
    // Validate address
    if (!this.isValidAddress(street, city, country, postalCode)) {
      throw new Error('Invalid address information');
    }

    // Validate coordinates
    if (!this.isValidCoordinates(latitude, longitude)) {
      throw new Error('Invalid coordinates');
    }

    // Validate contact information
    if (!this.isValidContact(contactName, contactEmail, contactPhone)) {
      throw new Error('Invalid contact information');
    }

    const venueId = this.generateId();
    const venue: Venue = {
      id: venueId,
      name,
      description,
      street,
      city,
      country,
      postalCode,
      latitude,
      longitude,
      contactName,
      contactEmail,
      contactPhone,
      capacity,
      status: 'active',
    };

    this.venues.set(venueId, venue);
    return venue;
  }

  /**
   * Sends event notification to organizer
   */
  sendEventNotification(
    eventId: string,
    organizerName: string,
    organizerEmail: string,
    organizerPhone: string,
    message: string
  ): boolean {
    if (!this.events.has(eventId)) {
      return false;
    }

    // Validate contact information
    if (!this.isValidContact(organizerName, organizerEmail, organizerPhone)) {
      throw new Error('Invalid organizer contact information');
    }

    const notificationId = this.generateId();
    const notification: Notification = {
      id: notificationId,
      eventId,
      organizerName,
      organizerEmail,
      organizerPhone,
      message,
      sentAt: new Date().toISOString(),
      status: 'sent',
    };

    this.notifications.set(notificationId, notification);
    return true;
  }

  /**
   * Schedules recurring event
   */
  scheduleRecurringEvent(
    baseEventId: string,
    pattern: string,
    occurrences: number,
    startDate: string,
    startTime: string,
    endTime: string,
    timezone: string
  ): Event[] {
    const baseEvent = this.events.get(baseEventId);
    if (!baseEvent) {
      throw new Error('Base event not found');
    }

    // Validate date and time
    if (!this.isValidDate(startDate)) {
      throw new Error('Invalid date format');
    }

    if (!this.isValidTime(startTime) || !this.isValidTime(endTime)) {
      throw new Error('Invalid time format');
    }

    if (!this.isValidTimezone(timezone)) {
      throw new Error('Invalid timezone');
    }

    if (!this.isTimeRangeValid(startTime, endTime)) {
      throw new Error('End time must be after start time');
    }

    const recurringEvents: Event[] = [];

    for (let i = 0; i < occurrences; i++) {
      const eventDate = this.calculateNextDate(startDate, pattern, i);
      const eventId = this.generateId();

      const event: Event = {
        ...baseEvent,
        id: eventId,
        date: eventDate,
        startTime,
        endTime,
        timezone,
        title: baseEvent.title + ' (Recurring)',
        attendees: 0,
      };

      this.events.set(eventId, event);
      recurringEvents.push(event);
    }

    return recurringEvents;
  }

  /**
   * Calculates distance between two coordinate points
   */
  calculateDistance(
    lat1: number,
    lon1: number,
    lat2: number,
    lon2: number
  ): number {
    if (
      !this.isValidCoordinates(lat1, lon1) ||
      !this.isValidCoordinates(lat2, lon2)
    ) {
      throw new Error('Invalid coordinates');
    }

    const earthRadius = 6371; // Earth's radius in kilometers

    const dLat = this.degToRad(lat2 - lat1);
    const dLon = this.degToRad(lon2 - lon1);

    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(this.degToRad(lat1)) *
        Math.cos(this.degToRad(lat2)) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return earthRadius * c;
  }

  /**
   * Finds events within date range
   */
  findEventsInDateRange(
    startDate: string,
    startTime: string,
    endDate: string,
    endTime: string,
    timezone: string
  ): Event[] {
    // Validate date and time
    if (!this.isValidDate(startDate) || !this.isValidDate(endDate)) {
      throw new Error('Invalid date format');
    }

    if (!this.isValidTime(startTime) || !this.isValidTime(endTime)) {
      throw new Error('Invalid time format');
    }

    if (!this.isValidTimezone(timezone)) {
      throw new Error('Invalid timezone');
    }

    const matchingEvents: Event[] = [];

    for (const event of this.events.values()) {
      if (
        this.isEventInDateRange(event, startDate, startTime, endDate, endTime)
      ) {
        matchingEvents.push(event);
      }
    }

    return matchingEvents;
  }

  /**
   * Converts time to different timezone
   */
  convertTimeToTimezone(
    date: string,
    time: string,
    fromTimezone: string,
    toTimezone: string
  ): TimeConversion {
    if (!this.isValidDate(date)) {
      throw new Error('Invalid date format');
    }

    if (!this.isValidTime(time)) {
      throw new Error('Invalid time format');
    }

    if (
      !this.isValidTimezone(fromTimezone) ||
      !this.isValidTimezone(toTimezone)
    ) {
      throw new Error('Invalid timezone');
    }

    // Create date in source timezone
    const dateTime = new Date(`${date}T${time}`);

    // Convert to target timezone using Intl API
    const formatter = new Intl.DateTimeFormat('en-CA', {
      timeZone: toTimezone,
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false,
    });

    const parts = formatter.formatToParts(dateTime);
    const datePart = `${parts.find(p => p.type === 'year')?.value}-${parts.find(p => p.type === 'month')?.value}-${parts.find(p => p.type === 'day')?.value}`;
    const timePart = `${parts.find(p => p.type === 'hour')?.value}:${parts.find(p => p.type === 'minute')?.value}:${parts.find(p => p.type === 'second')?.value}`;

    return {
      date: datePart,
      time: timePart,
      timezone: toTimezone,
    };
  }

  // Validation methods (these contain the data clumps logic)
  private isValidDate(date: string): boolean {
    return /^\d{4}-\d{2}-\d{2}$/.test(date) && !isNaN(Date.parse(date));
  }

  private isValidTime(time: string): boolean {
    return /^\d{2}:\d{2}:\d{2}$/.test(time);
  }

  private isValidTimezone(timezone: string): boolean {
    try {
      Intl.DateTimeFormat(undefined, { timeZone: timezone });
      return true;
    } catch {
      return false;
    }
  }

  private isTimeRangeValid(startTime: string, endTime: string): boolean {
    return startTime < endTime;
  }

  private isValidAddress(
    street: string,
    city: string,
    country: string,
    postalCode: string
  ): boolean {
    return (
      street.trim() !== '' &&
      city.trim() !== '' &&
      country.trim() !== '' &&
      postalCode.trim() !== ''
    );
  }

  private isValidCoordinates(latitude: number, longitude: number): boolean {
    return (
      latitude >= -90 && latitude <= 90 && longitude >= -180 && longitude <= 180
    );
  }

  private isValidContact(name: string, email: string, phone: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return name.trim() !== '' && emailRegex.test(email) && phone.trim() !== '';
  }

  private isEventInDateRange(
    event: Event,
    startDate: string,
    startTime: string,
    endDate: string,
    endTime: string
  ): boolean {
    // Simplified comparison - in real implementation would handle timezone conversion
    const eventDateTime = `${event.date} ${event.startTime}`;
    const rangeStart = `${startDate} ${startTime}`;
    const rangeEnd = `${endDate} ${endTime}`;

    return eventDateTime >= rangeStart && eventDateTime <= rangeEnd;
  }

  private calculateNextDate(
    baseDate: string,
    pattern: string,
    occurrence: number
  ): string {
    const date = new Date(baseDate);

    switch (pattern) {
      case 'daily':
        date.setDate(date.getDate() + occurrence);
        break;
      case 'weekly':
        date.setDate(date.getDate() + occurrence * 7);
        break;
      case 'monthly':
        date.setMonth(date.getMonth() + occurrence);
        break;
    }

    return date.toISOString().split('T')[0]!;
  }

  private degToRad(deg: number): number {
    return deg * (Math.PI / 180);
  }

  private generateId(): string {
    return 'evt_' + Math.random().toString(36).substr(2, 9);
  }

  // Getters for testing
  getEvents(): Event[] {
    return Array.from(this.events.values());
  }

  getVenues(): Venue[] {
    return Array.from(this.venues.values());
  }

  getNotifications(): Notification[] {
    return Array.from(this.notifications.values());
  }
}
