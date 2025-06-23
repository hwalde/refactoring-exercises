<?php

declare(strict_types=1);

namespace RefactoringExercises\CodeSmells\FeatureEnvy;

class Customer
{
    private string $id;
    private string $name;
    private string $email;
    private string $type;
    private int $loyaltyYears;
    private string $address;
    private string $phoneNumber;

    public function __construct(
        string $id,
        string $name,
        string $email,
        string $type,
        int $loyaltyYears,
        string $address = '',
        string $phoneNumber = ''
    ) {
        $this->id = $id;
        $this->name = $name;
        $this->email = $email;
        $this->type = $type;
        $this->loyaltyYears = $loyaltyYears;
        $this->address = $address;
        $this->phoneNumber = $phoneNumber;
    }

    public function getId(): string
    {
        return $this->id;
    }

    public function getName(): string
    {
        return $this->name;
    }

    public function getEmail(): string
    {
        return $this->email;
    }

    public function getType(): string
    {
        return $this->type;
    }

    public function getLoyaltyYears(): int
    {
        return $this->loyaltyYears;
    }

    public function getAddress(): string
    {
        return $this->address;
    }

    public function getPhoneNumber(): string
    {
        return $this->phoneNumber;
    }
}