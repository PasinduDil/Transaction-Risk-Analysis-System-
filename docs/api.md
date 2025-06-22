# Transaction Risk Analysis API Documentation

## Base URL

```
http://localhost:8000/api
```

## Authentication

All endpoints require Basic Authentication.

## Endpoints

### 1. Transaction Webhook

Receive and analyze transaction data.

- **URL**: `/webhook`
- **Method**: `POST`
- **Auth Required**: Yes

#### Request Body

```json
{
    "transaction_id": "tx_12345abcde",
    "timestamp": "2025-05-07T14:30:45Z",
    "amount": 129.99,
    "currency": "USD",
    "customer": {
        "id": "cust_98765zyxwv",
        "country": "US",
        "ip_address": "192.168.1.1"
    },
    "payment_method": {
        "type": "credit_card",
        "last_four": "4242",
        "country_of_issue": "CA"
    },
    "merchant": {
        "id": "merch_abcde12345",
        "name": "Example Store",
        "category": "electronics"
    }
}
```

#### Success Response

- **Code**: 200 OK
```json
{
    "status": "success",
    "message": "Transaction processed successfully",
    "transaction_id": "tx_12345abcde",
    "risk_score": "0.85"
}
```

#### Error Responses

- **Code**: 400 Bad Request
```json
{
    "detail": "Invalid transaction data: [error details]"
}
```

- **Code**: 401 Unauthorized
```json
{
    "detail": "Invalid authentication credentials"
}
```

### 2. Admin Notifications

Retrieve high-risk transaction notifications.

- **URL**: `/notifications`
- **Method**: `GET`
- **Auth Required**: Yes (Admin)

#### Query Parameters

- `status` (optional): Filter notifications by status (pending, reviewed, dismissed)

#### Success Response

- **Code**: 200 OK
```json
[
    {
        "alert_type": "high_risk_transaction",
        "transaction_id": "tx_12345abcde",
        "risk_score": 0.85,
        "risk_factors": [
            "Customer country (US) differs from card country (CA)",
            "Transaction amount significantly higher than customer average",
            "Multiple transactions within short timeframe"
        ],
        "transaction_details": {
            // Original transaction JSON
        },
        "llm_analysis": "This transaction shows multiple risk indicators...",
        "timestamp": "2025-05-07T14:30:45Z",
        "status": "pending"
    }
]
```

### 3. Update Notification Status

Update the status of a notification.

- **URL**: `/notifications/{notification_id}/status`
- **Method**: `PUT`
- **Auth Required**: Yes (Admin)

#### Request Body

```json
{
    "status": "reviewed" // or "dismissed"
}
```

#### Success Response

- **Code**: 200 OK
```json
{
    "message": "Notification status updated to reviewed"
}
```

## Error Handling

The API uses standard HTTP status codes:

- 200: Success
- 400: Bad Request (invalid input)
- 401: Unauthorized (invalid credentials)
- 404: Not Found
- 500: Internal Server Error

## Rate Limiting

To prevent abuse, the API implements rate limiting:

- Webhook endpoint: 100 requests per minute
- Admin endpoints: 1000 requests per hour

## Best Practices

1. Always include proper authentication headers
2. Validate transaction data before sending
3. Handle API responses appropriately
4. Implement proper error handling
5. Monitor notification endpoints for high-risk alerts