<?php

declare(strict_types=1);

namespace RefactoringExercises\BasisRefactorings\ExtractClassMini;

use PHPUnit\Framework\TestCase;

/**
 * @internal
 *
 * @coversNothing
 */
class MapMarkerTest extends TestCase
{
    private MapMarker $marker;

    protected function setUp(): void
    {
        $this->marker = new MapMarker(
            52.5200,
            13.4050,
            34.0,
            'Brandenburg Gate',
            'Historic landmark in Berlin',
            '/brandenburg-gate.png',
            true
        );
    }

    public function testConstructorSetsAllProperties(): void
    {
        $marker = new MapMarker(
            40.7128,
            -74.0060,
            10.0,
            'Statue of Liberty',
            'Famous statue in New York Harbor'
        );

        $this->assertSame(40.7128, $marker->getLatitude());
        $this->assertSame(-74.0060, $marker->getLongitude());
        $this->assertSame(10.0, $marker->getAltitude());
        $this->assertSame('Statue of Liberty', $marker->getTitle());
        $this->assertSame('Famous statue in New York Harbor', $marker->getDescription());
        $this->assertSame('/default-marker.png', $marker->getIconUrl());
        $this->assertTrue($marker->isVisible());
    }

    public function testConstructorWithCustomIconAndVisibility(): void
    {
        $marker = new MapMarker(
            48.8566,
            2.3522,
            35.0,
            'Eiffel Tower',
            'Iron lattice tower in Paris',
            '/eiffel-tower.png',
            false
        );

        $this->assertSame('/eiffel-tower.png', $marker->getIconUrl());
        $this->assertFalse($marker->isVisible());
    }

    public function testGetCoordinates(): void
    {
        $this->assertSame(52.5200, $this->marker->getLatitude());
        $this->assertSame(13.4050, $this->marker->getLongitude());
        $this->assertSame(34.0, $this->marker->getAltitude());
    }

    public function testGetMarkerInfo(): void
    {
        $this->assertSame('Brandenburg Gate', $this->marker->getTitle());
        $this->assertSame('Historic landmark in Berlin', $this->marker->getDescription());
        $this->assertSame('/brandenburg-gate.png', $this->marker->getIconUrl());
        $this->assertTrue($this->marker->isVisible());
    }

    public function testSetVisible(): void
    {
        $this->marker->setVisible(false);
        $this->assertFalse($this->marker->isVisible());

        $this->marker->setVisible(true);
        $this->assertTrue($this->marker->isVisible());
    }

    public function testUpdateInfo(): void
    {
        $this->marker->updateInfo('Berlin Gate', 'Updated description');

        $this->assertSame('Berlin Gate', $this->marker->getTitle());
        $this->assertSame('Updated description', $this->marker->getDescription());
    }

    public function testChangeIcon(): void
    {
        $this->marker->changeIcon('/new-icon.png');
        $this->assertSame('/new-icon.png', $this->marker->getIconUrl());
    }

    public function testMoveTo(): void
    {
        $this->marker->moveTo(51.5074, -0.1278, 11.0);

        $this->assertSame(51.5074, $this->marker->getLatitude());
        $this->assertSame(-0.1278, $this->marker->getLongitude());
        $this->assertSame(11.0, $this->marker->getAltitude());
    }

    public function testDistanceToSameLocation(): void
    {
        $distance = $this->marker->distanceTo(52.5200, 13.4050);
        $this->assertEqualsWithDelta(0.0, $distance, 0.1);
    }

    public function testDistanceToKnownLocation(): void
    {
        // Distance from Brandenburg Gate to Reichstag Building (approximately 1960m)
        $distance = $this->marker->distanceTo(52.5186, 13.3761);
        $this->assertEqualsWithDelta(1960.0, $distance, 100.0);
    }

    public function testDistanceToFarAwayLocation(): void
    {
        // Distance from Berlin to Paris (approximately 878 km)
        $distance = $this->marker->distanceTo(48.8566, 2.3522);
        $this->assertEqualsWithDelta(878000.0, $distance, 10000.0);
    }

    public function testGetFormattedCoordinates(): void
    {
        $formatted = $this->marker->getFormattedCoordinates();
        $this->assertSame('Lat: 52.520000°, Lon: 13.405000°, Alt: 34.0m', $formatted);
    }

    public function testGetFormattedCoordinatesWithNegativeValues(): void
    {
        $marker = new MapMarker(-33.8688, 151.2093, 58.0, 'Sydney Opera House', 'Iconic building');
        $formatted = $marker->getFormattedCoordinates();
        $this->assertSame('Lat: -33.868800°, Lon: 151.209300°, Alt: 58.0m', $formatted);
    }

    public function testIsAtSameLocationWithinTolerance(): void
    {
        $this->assertTrue($this->marker->isAtSameLocation(52.5201, 13.4051));
        $this->assertTrue($this->marker->isAtSameLocation(52.5199, 13.4049));
    }

    public function testIsAtSameLocationOutsideTolerance(): void
    {
        $this->assertFalse($this->marker->isAtSameLocation(52.5210, 13.4060));
        $this->assertFalse($this->marker->isAtSameLocation(52.5100, 13.4000));
    }

    public function testIsAtSameLocationWithCustomTolerance(): void
    {
        $this->assertTrue($this->marker->isAtSameLocation(52.5250, 13.4100, 0.01));
        $this->assertFalse($this->marker->isAtSameLocation(52.5250, 13.4100, 0.001));
    }

    public function testToArray(): void
    {
        $expected = [
            'latitude' => 52.5200,
            'longitude' => 13.4050,
            'altitude' => 34.0,
            'title' => 'Brandenburg Gate',
            'description' => 'Historic landmark in Berlin',
            'iconUrl' => '/brandenburg-gate.png',
            'isVisible' => true,
        ];

        $this->assertSame($expected, $this->marker->toArray());
    }

    public function testToArrayAfterModifications(): void
    {
        $this->marker->moveTo(48.8566, 2.3522, 35.0);
        $this->marker->updateInfo('Eiffel Tower', 'Iron lattice tower in Paris');
        $this->marker->changeIcon('/eiffel-tower.png');
        $this->marker->setVisible(false);

        $expected = [
            'latitude' => 48.8566,
            'longitude' => 2.3522,
            'altitude' => 35.0,
            'title' => 'Eiffel Tower',
            'description' => 'Iron lattice tower in Paris',
            'iconUrl' => '/eiffel-tower.png',
            'isVisible' => false,
        ];

        $this->assertSame($expected, $this->marker->toArray());
    }
}
