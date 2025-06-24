export class MapMarker {
  private latitude: number;
  private longitude: number;
  private altitude: number;
  private title: string;
  private description: string;
  private iconUrl: string;
  private isVisibleFlag: boolean;

  constructor(
    latitude: number,
    longitude: number,
    altitude: number,
    title: string,
    description: string,
    iconUrl: string = '/default-marker.png',
    isVisible: boolean = true
  ) {
    this.latitude = latitude;
    this.longitude = longitude;
    this.altitude = altitude;
    this.title = title;
    this.description = description;
    this.iconUrl = iconUrl;
    this.isVisibleFlag = isVisible;
  }

  getLatitude(): number {
    return this.latitude;
  }

  getLongitude(): number {
    return this.longitude;
  }

  getAltitude(): number {
    return this.altitude;
  }

  getTitle(): string {
    return this.title;
  }

  getDescription(): string {
    return this.description;
  }

  getIconUrl(): string {
    return this.iconUrl;
  }

  isVisible(): boolean {
    return this.isVisibleFlag;
  }

  setVisible(isVisible: boolean): void {
    this.isVisibleFlag = isVisible;
  }

  updateInfo(title: string, description: string): void {
    this.title = title;
    this.description = description;
  }

  changeIcon(iconUrl: string): void {
    this.iconUrl = iconUrl;
  }

  moveTo(latitude: number, longitude: number, altitude: number): void {
    this.latitude = latitude;
    this.longitude = longitude;
    this.altitude = altitude;
  }

  distanceTo(latitude: number, longitude: number): number {
    // Haversine formula for calculating distance between two points on Earth
    const earthRadius = 6371000; // meters

    const lat1Rad = this.toRadians(this.latitude);
    const lat2Rad = this.toRadians(latitude);
    const deltaLatRad = this.toRadians(latitude - this.latitude);
    const deltaLonRad = this.toRadians(longitude - this.longitude);

    const a =
      Math.sin(deltaLatRad / 2) * Math.sin(deltaLatRad / 2) +
      Math.cos(lat1Rad) *
        Math.cos(lat2Rad) *
        Math.sin(deltaLonRad / 2) *
        Math.sin(deltaLonRad / 2);

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return earthRadius * c;
  }

  getFormattedCoordinates(): string {
    return `Lat: ${this.latitude.toFixed(6)}°, Lon: ${this.longitude.toFixed(6)}°, Alt: ${this.altitude.toFixed(1)}m`;
  }

  isAtSameLocation(
    latitude: number,
    longitude: number,
    tolerance: number = 0.001
  ): boolean {
    return (
      Math.abs(this.latitude - latitude) < tolerance &&
      Math.abs(this.longitude - longitude) < tolerance
    );
  }

  toArray(): Record<string, number | string | boolean> {
    return {
      latitude: this.latitude,
      longitude: this.longitude,
      altitude: this.altitude,
      title: this.title,
      description: this.description,
      iconUrl: this.iconUrl,
      isVisible: this.isVisibleFlag,
    };
  }

  private toRadians(degrees: number): number {
    return degrees * (Math.PI / 180);
  }
}
