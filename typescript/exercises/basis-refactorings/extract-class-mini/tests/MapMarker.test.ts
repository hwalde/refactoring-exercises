import { MapMarker } from '../src/MapMarker';

describe('MapMarker', () => {
  let marker: MapMarker;

  beforeEach(() => {
    marker = new MapMarker(
      52.52,
      13.405,
      34.0,
      'Brandenburg Gate',
      'Historic landmark in Berlin',
      '/brandenburg-gate.png',
      true
    );
  });

  describe('Constructor', () => {
    test('sets all properties correctly', () => {
      const testMarker = new MapMarker(
        40.7128,
        -74.006,
        10.0,
        'Statue of Liberty',
        'Famous statue in New York Harbor'
      );

      expect(testMarker.getLatitude()).toBe(40.7128);
      expect(testMarker.getLongitude()).toBe(-74.006);
      expect(testMarker.getAltitude()).toBe(10.0);
      expect(testMarker.getTitle()).toBe('Statue of Liberty');
      expect(testMarker.getDescription()).toBe(
        'Famous statue in New York Harbor'
      );
      expect(testMarker.getIconUrl()).toBe('/default-marker.png');
      expect(testMarker.isVisible()).toBe(true);
    });

    test('sets custom icon and visibility correctly', () => {
      const testMarker = new MapMarker(
        48.8566,
        2.3522,
        35.0,
        'Eiffel Tower',
        'Iron lattice tower in Paris',
        '/eiffel-tower.png',
        false
      );

      expect(testMarker.getIconUrl()).toBe('/eiffel-tower.png');
      expect(testMarker.isVisible()).toBe(false);
    });
  });

  describe('Coordinate getters', () => {
    test('return correct coordinate values', () => {
      expect(marker.getLatitude()).toBe(52.52);
      expect(marker.getLongitude()).toBe(13.405);
      expect(marker.getAltitude()).toBe(34.0);
    });
  });

  describe('Marker info getters', () => {
    test('return correct marker information', () => {
      expect(marker.getTitle()).toBe('Brandenburg Gate');
      expect(marker.getDescription()).toBe('Historic landmark in Berlin');
      expect(marker.getIconUrl()).toBe('/brandenburg-gate.png');
      expect(marker.isVisible()).toBe(true);
    });
  });

  describe('Visibility management', () => {
    test('allows changing visibility', () => {
      marker.setVisible(false);
      expect(marker.isVisible()).toBe(false);

      marker.setVisible(true);
      expect(marker.isVisible()).toBe(true);
    });
  });

  describe('Info updates', () => {
    test('allows updating title and description', () => {
      marker.updateInfo('Berlin Gate', 'Updated description');

      expect(marker.getTitle()).toBe('Berlin Gate');
      expect(marker.getDescription()).toBe('Updated description');
    });
  });

  describe('Icon changes', () => {
    test('allows changing icon', () => {
      marker.changeIcon('/new-icon.png');
      expect(marker.getIconUrl()).toBe('/new-icon.png');
    });
  });

  describe('Movement', () => {
    test('allows moving to new coordinates', () => {
      marker.moveTo(51.5074, -0.1278, 11.0);

      expect(marker.getLatitude()).toBe(51.5074);
      expect(marker.getLongitude()).toBe(-0.1278);
      expect(marker.getAltitude()).toBe(11.0);
    });
  });

  describe('Distance calculations', () => {
    test('calculates zero distance to same location', () => {
      const distance = marker.distanceTo(52.52, 13.405);
      expect(distance).toBeCloseTo(0.0, 0);
    });

    test('calculates distance to known location', () => {
      // Distance from Brandenburg Gate to Reichstag Building (approximately 1960m)
      const distance = marker.distanceTo(52.5186, 13.3761);
      expect(distance).toBeCloseTo(1960.0, -2);
    });

    test('calculates distance to far away location', () => {
      // Distance from Berlin to Paris (approximately 878 km)
      const distance = marker.distanceTo(48.8566, 2.3522);
      expect(distance).toBeCloseTo(878000.0, -4);
    });
  });

  describe('Coordinate formatting', () => {
    test('formats coordinates correctly', () => {
      const formatted = marker.getFormattedCoordinates();
      expect(formatted).toBe('Lat: 52.520000°, Lon: 13.405000°, Alt: 34.0m');
    });

    test('formats negative coordinates correctly', () => {
      const testMarker = new MapMarker(
        -33.8688,
        151.2093,
        58.0,
        'Sydney Opera House',
        'Iconic building'
      );
      const formatted = testMarker.getFormattedCoordinates();
      expect(formatted).toBe('Lat: -33.868800°, Lon: 151.209300°, Alt: 58.0m');
    });
  });

  describe('Location comparison', () => {
    test('detects same location within tolerance', () => {
      expect(marker.isAtSameLocation(52.5201, 13.4051)).toBe(true);
      expect(marker.isAtSameLocation(52.5199, 13.4049)).toBe(true);
    });

    test('detects different location outside tolerance', () => {
      expect(marker.isAtSameLocation(52.521, 13.406)).toBe(false);
      expect(marker.isAtSameLocation(52.51, 13.4)).toBe(false);
    });

    test('respects custom tolerance', () => {
      expect(marker.isAtSameLocation(52.525, 13.41, 0.01)).toBe(true);
      expect(marker.isAtSameLocation(52.525, 13.41, 0.001)).toBe(false);
    });
  });

  describe('Array conversion', () => {
    test('converts to array correctly', () => {
      const expected = {
        latitude: 52.52,
        longitude: 13.405,
        altitude: 34.0,
        title: 'Brandenburg Gate',
        description: 'Historic landmark in Berlin',
        iconUrl: '/brandenburg-gate.png',
        isVisible: true,
      };

      expect(marker.toArray()).toEqual(expected);
    });

    test('converts to array after modifications', () => {
      marker.moveTo(48.8566, 2.3522, 35.0);
      marker.updateInfo('Eiffel Tower', 'Iron lattice tower in Paris');
      marker.changeIcon('/eiffel-tower.png');
      marker.setVisible(false);

      const expected = {
        latitude: 48.8566,
        longitude: 2.3522,
        altitude: 35.0,
        title: 'Eiffel Tower',
        description: 'Iron lattice tower in Paris',
        iconUrl: '/eiffel-tower.png',
        isVisible: false,
      };

      expect(marker.toArray()).toEqual(expected);
    });
  });
});
