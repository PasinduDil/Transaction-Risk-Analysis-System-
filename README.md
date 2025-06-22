# Transaction Risk Analysis Project

A system that receives transaction data via webhook, uses an LLM to analyze risk patterns, and notifies administrators about suspicious transactions.

## Project Structure

```
├── src/
│   ├── webhook/
│   │   ├── __init__.py
│   │   ├── routes.py          # Webhook endpoint definitions
│   │   ├── auth.py           # Authentication middleware
│   │   └── validators.py      # Request data validation
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── analyzer.py        # LLM integration for risk analysis
│   │   ├── prompts.py         # LLM prompt templates
│   │   └── parser.py          # LLM response parsing
│   ├── notifications/
│   │   ├── __init__.py
│   │   ├── admin.py           # Admin notification logic
│   │   └── templates.py        # Notification templates
│   └── common/
│       ├── __init__.py
│       ├── models.py          # Data models
│       ├── config.py          # Configuration settings
│       └── constants.py       # Project constants
├── tests/
│   ├── test_webhook.py
│   ├── test_llm.py
│   ├── test_notifications.py
│   └── test_data/            # Test fixtures and data
├── docs/
│   ├── api.md                # API documentation
│   └── setup.md              # Setup instructions
├── requirements.txt          # Python dependencies
└── main.py                   # Application entry point
```

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables in `.env`:
   ```env
   # API Configuration
   DEBUG=False

   # Security
   WEBHOOK_SECRET=your_webhook_secret_here
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=your_admin_password_here

   # LLM Configuration
   QROC_API_KEY=your_qroc_api_key_here
   QROC_API_ENDPOINT=https://api.qroc.ai/v1
   QROC_MODEL=your_model_name
   LLM_TEMPERATURE=0.0
   LLM_MAX_TOKENS=500
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## API Documentation

### Webhook Endpoint

- **URL**: `/api/webhook`
- **Method**: `POST`
- **Auth**: Basic Authentication
- **Request Body**: Transaction JSON (see schema in docs/api.md)
- **Response**: 200 OK, 400 Bad Request, 401 Unauthorized

### Admin Notification API

- **URL**: `/api/notifications`
- **Method**: `GET`
- **Auth**: Admin Authentication
- **Response**: List of high-risk transaction notifications

## Testing

Run tests with:
```bash
python -m pytest
```

Test cases cover:
- Normal transactions
- Cross-border transactions
- High-value transactions
- High-risk country transactions
- Invalid data handling
- Authentication failures

## License

MIT