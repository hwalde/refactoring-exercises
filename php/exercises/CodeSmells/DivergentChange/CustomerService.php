<?php

declare(strict_types=1);

namespace RefactoringExercises\CodeSmells\DivergentChange;

class CustomerService
{
    private array $customers = [];

    private array $loginAttempts = [];

    private array $marketingPreferences = [];

    private array $orderHistory = [];

    private array $addresses = [];

    public function registerCustomer(string $email, string $password, string $firstName, string $lastName): int
    {
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            throw new \InvalidArgumentException('Invalid email format');
        }

        if (strlen($password) < 8) {
            throw new \InvalidArgumentException('Password must be at least 8 characters');
        }

        if (empty($firstName) || empty($lastName)) {
            throw new \InvalidArgumentException('First name and last name are required');
        }

        foreach ($this->customers as $customer) {
            if ($customer['email'] === $email) {
                throw new \InvalidArgumentException('Customer with this email already exists');
            }
        }

        $customerId = count($this->customers) + 1;
        $this->customers[$customerId] = [
            'id' => $customerId,
            'email' => $email,
            'password' => password_hash($password, PASSWORD_DEFAULT),
            'firstName' => $firstName,
            'lastName' => $lastName,
            'status' => 'active',
            'createdAt' => new \DateTime(),
            'lastLogin' => null,
        ];

        $this->marketingPreferences[$customerId] = [
            'emailMarketing' => true,
            'smsMarketing' => false,
            'pushNotifications' => true,
            'preferredChannels' => ['email'],
        ];

        return $customerId;
    }

    public function authenticateCustomer(string $email, string $password): ?int
    {
        $customer = $this->findCustomerByEmail($email);

        if (!$customer) {
            $this->recordFailedLoginAttempt($email);

            return null;
        }

        if ($this->isAccountLocked($customer['id'])) {
            throw new \RuntimeException('Account is temporarily locked due to too many failed attempts');
        }

        if (!password_verify($password, $customer['password'])) {
            $this->recordFailedLoginAttempt($email);

            return null;
        }

        $this->clearFailedLoginAttempts($customer['id']);
        $this->updateLastLogin($customer['id']);

        return $customer['id'];
    }

    public function updateContactInformation(int $customerId, string $firstName, string $lastName, string $phone): void
    {
        if (!isset($this->customers[$customerId])) {
            throw new \InvalidArgumentException('Customer not found');
        }

        if (empty($firstName) || empty($lastName)) {
            throw new \InvalidArgumentException('First name and last name are required');
        }

        if (!empty($phone) && !preg_match('/^\+?[1-9]\d{1,14}$/', $phone)) {
            throw new \InvalidArgumentException('Invalid phone number format');
        }

        $this->customers[$customerId]['firstName'] = $firstName;
        $this->customers[$customerId]['lastName'] = $lastName;
        $this->customers[$customerId]['phone'] = $phone;
    }

    public function addCustomerAddress(int $customerId, string $street, string $city, string $zipCode, string $country, bool $isDefault = false): int
    {
        if (!isset($this->customers[$customerId])) {
            throw new \InvalidArgumentException('Customer not found');
        }

        if (empty($street) || empty($city) || empty($zipCode) || empty($country)) {
            throw new \InvalidArgumentException('All address fields are required');
        }

        if (!isset($this->addresses[$customerId])) {
            $this->addresses[$customerId] = [];
        }

        $addressId = count($this->addresses[$customerId]) + 1;

        if ($isDefault) {
            foreach ($this->addresses[$customerId] as &$address) {
                $address['isDefault'] = false;
            }
        }

        $this->addresses[$customerId][$addressId] = [
            'id' => $addressId,
            'street' => $street,
            'city' => $city,
            'zipCode' => $zipCode,
            'country' => $country,
            'isDefault' => $isDefault || empty($this->addresses[$customerId]),
        ];

        return $addressId;
    }

    public function updateMarketingPreferences(int $customerId, bool $emailMarketing, bool $smsMarketing, bool $pushNotifications, array $preferredChannels): void
    {
        if (!isset($this->customers[$customerId])) {
            throw new \InvalidArgumentException('Customer not found');
        }

        $validChannels = ['email', 'sms', 'push', 'mail'];
        foreach ($preferredChannels as $channel) {
            if (!in_array($channel, $validChannels, true)) {
                throw new \InvalidArgumentException("Invalid marketing channel: {$channel}");
            }
        }

        $this->marketingPreferences[$customerId] = [
            'emailMarketing' => $emailMarketing,
            'smsMarketing' => $smsMarketing,
            'pushNotifications' => $pushNotifications,
            'preferredChannels' => $preferredChannels,
        ];
    }

    public function sendMarketingCampaign(int $customerId, string $subject, string $content, string $channel): bool
    {
        if (!isset($this->customers[$customerId])) {
            throw new \InvalidArgumentException('Customer not found');
        }

        if (!isset($this->marketingPreferences[$customerId])) {
            return false;
        }

        $preferences = $this->marketingPreferences[$customerId];

        switch ($channel) {
            case 'email':
                if (!$preferences['emailMarketing'] || !in_array('email', $preferences['preferredChannels'], true)) {
                    return false;
                }

                break;

            case 'sms':
                if (!$preferences['smsMarketing'] || !in_array('sms', $preferences['preferredChannels'], true)) {
                    return false;
                }

                break;

            case 'push':
                if (!$preferences['pushNotifications'] || !in_array('push', $preferences['preferredChannels'], true)) {
                    return false;
                }

                break;

            default:
                throw new \InvalidArgumentException("Unsupported marketing channel: {$channel}");
        }

        return true;
    }

    public function recordPurchase(int $customerId, array $items, float $totalAmount): int
    {
        if (!isset($this->customers[$customerId])) {
            throw new \InvalidArgumentException('Customer not found');
        }

        if (empty($items)) {
            throw new \InvalidArgumentException('Purchase must contain at least one item');
        }

        if ($totalAmount <= 0) {
            throw new \InvalidArgumentException('Total amount must be positive');
        }

        if (!isset($this->orderHistory[$customerId])) {
            $this->orderHistory[$customerId] = [];
        }

        $orderId = count($this->orderHistory[$customerId]) + 1;
        $this->orderHistory[$customerId][$orderId] = [
            'id' => $orderId,
            'items' => $items,
            'totalAmount' => $totalAmount,
            'orderDate' => new \DateTime(),
            'status' => 'completed',
        ];

        return $orderId;
    }

    public function getCustomerSpendingHistory(int $customerId): array
    {
        if (!isset($this->customers[$customerId])) {
            throw new \InvalidArgumentException('Customer not found');
        }

        if (!isset($this->orderHistory[$customerId])) {
            return [];
        }

        $history = [];
        foreach ($this->orderHistory[$customerId] as $order) {
            $history[] = [
                'orderId' => $order['id'],
                'amount' => $order['totalAmount'],
                'date' => $order['orderDate'],
                'itemCount' => count($order['items']),
            ];
        }

        usort($history, function ($a, $b) {
            return $b['date'] <=> $a['date'];
        });

        return $history;
    }

    public function calculateCustomerLifetimeValue(int $customerId): float
    {
        if (!isset($this->customers[$customerId])) {
            throw new \InvalidArgumentException('Customer not found');
        }

        if (!isset($this->orderHistory[$customerId])) {
            return 0.0;
        }

        $totalSpent = 0.0;
        foreach ($this->orderHistory[$customerId] as $order) {
            $totalSpent += $order['totalAmount'];
        }

        return $totalSpent;
    }

    public function getCustomerProfile(int $customerId): array
    {
        if (!isset($this->customers[$customerId])) {
            throw new \InvalidArgumentException('Customer not found');
        }

        return [
            'personal' => [
                'id' => $this->customers[$customerId]['id'],
                'firstName' => $this->customers[$customerId]['firstName'],
                'lastName' => $this->customers[$customerId]['lastName'],
                'email' => $this->customers[$customerId]['email'],
                'phone' => $this->customers[$customerId]['phone'] ?? null,
                'status' => $this->customers[$customerId]['status'],
            ],
            'addresses' => $this->addresses[$customerId] ?? [],
            'marketing' => $this->marketingPreferences[$customerId] ?? null,
            'orderHistory' => $this->getCustomerSpendingHistory($customerId),
            'lifetimeValue' => $this->calculateCustomerLifetimeValue($customerId),
        ];
    }

    private function findCustomerByEmail(string $email): ?array
    {
        foreach ($this->customers as $customer) {
            if ($customer['email'] === $email) {
                return $customer;
            }
        }

        return null;
    }

    private function recordFailedLoginAttempt(string $email): void
    {
        if (!isset($this->loginAttempts[$email])) {
            $this->loginAttempts[$email] = [];
        }
        $this->loginAttempts[$email][] = new \DateTime();
    }

    private function isAccountLocked(int $customerId): bool
    {
        $customer = $this->customers[$customerId];
        $email = $customer['email'];

        if (!isset($this->loginAttempts[$email])) {
            return false;
        }

        $recentAttempts = array_filter($this->loginAttempts[$email], function ($attempt) {
            return $attempt > (new \DateTime())->modify('-15 minutes');
        });

        return count($recentAttempts) >= 3;
    }

    private function clearFailedLoginAttempts(int $customerId): void
    {
        $customer = $this->customers[$customerId];
        unset($this->loginAttempts[$customer['email']]);
    }

    private function updateLastLogin(int $customerId): void
    {
        $this->customers[$customerId]['lastLogin'] = new \DateTime();
    }
}
