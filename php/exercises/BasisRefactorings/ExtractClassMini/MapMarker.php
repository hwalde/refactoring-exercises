<?php

declare(strict_types=1);

namespace RefactoringExercises\BasisRefactorings\ExtractClassMini;

class MapMarker
{
    private float $latitude;

    private float $longitude;

    private float $altitude;

    private string $title;

    private string $description;

    private string $iconUrl;

    private bool $isVisible;

    public function __construct(
        float $latitude,
        float $longitude,
        float $altitude,
        string $title,
        string $description,
        string $iconUrl = '/default-marker.png',
        bool $isVisible = true
    ) {
        $this->latitude = $latitude;
        $this->longitude = $longitude;
        $this->altitude = $altitude;
        $this->title = $title;
        $this->description = $description;
        $this->iconUrl = $iconUrl;
        $this->isVisible = $isVisible;
    }

    public function getLatitude(): float
    {
        return $this->latitude;
    }

    public function getLongitude(): float
    {
        return $this->longitude;
    }

    public function getAltitude(): float
    {
        return $this->altitude;
    }

    public function getTitle(): string
    {
        return $this->title;
    }

    public function getDescription(): string
    {
        return $this->description;
    }

    public function getIconUrl(): string
    {
        return $this->iconUrl;
    }

    public function isVisible(): bool
    {
        return $this->isVisible;
    }

    public function setVisible(bool $isVisible): void
    {
        $this->isVisible = $isVisible;
    }

    public function updateInfo(string $title, string $description): void
    {
        $this->title = $title;
        $this->description = $description;
    }

    public function changeIcon(string $iconUrl): void
    {
        $this->iconUrl = $iconUrl;
    }

    public function moveTo(float $latitude, float $longitude, float $altitude): void
    {
        $this->latitude = $latitude;
        $this->longitude = $longitude;
        $this->altitude = $altitude;
    }

    public function distanceTo(float $latitude, float $longitude): float
    {
        // Haversine formula for calculating distance between two points on Earth
        $earthRadius = 6371000; // meters

        $lat1Rad = deg2rad($this->latitude);
        $lat2Rad = deg2rad($latitude);
        $deltaLatRad = deg2rad($latitude - $this->latitude);
        $deltaLonRad = deg2rad($longitude - $this->longitude);

        $a = sin($deltaLatRad / 2) * sin($deltaLatRad / 2)
             + cos($lat1Rad) * cos($lat2Rad)
             * sin($deltaLonRad / 2) * sin($deltaLonRad / 2);

        $c = 2 * atan2(sqrt($a), sqrt(1 - $a));

        return $earthRadius * $c;
    }

    public function getFormattedCoordinates(): string
    {
        return sprintf(
            'Lat: %.6f°, Lon: %.6f°, Alt: %.1fm',
            $this->latitude,
            $this->longitude,
            $this->altitude
        );
    }

    public function isAtSameLocation(float $latitude, float $longitude, float $tolerance = 0.001): bool
    {
        return abs($this->latitude - $latitude) < $tolerance
               && abs($this->longitude - $longitude) < $tolerance;
    }

    public function toArray(): array
    {
        return [
            'latitude' => $this->latitude,
            'longitude' => $this->longitude,
            'altitude' => $this->altitude,
            'title' => $this->title,
            'description' => $this->description,
            'iconUrl' => $this->iconUrl,
            'isVisible' => $this->isVisible,
        ];
    }
}
