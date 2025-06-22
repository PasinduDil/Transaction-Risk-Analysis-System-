# Setup Instructions

## Prerequisites

1. Python 3.8 or higher
2. pip (Python package installer)
3. Virtual environment tool (venv)
4. OpenAI API key or other LLM provider credentials

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd transaction-risk-analysis
```

2. Create and activate a virtual environment:
```bash
# On macOS/Linux
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root:
```env
# API Configuration
DEBUG=False

# Security
WEBHOOK_SECRET=your_webhook_secret_here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_admin_password_here

# LLM Configuration
LLM_API_KEY=your_openai_api_key_here
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.0
LLM_MAX_TOKENS=500
```

2. Update the configuration values:
- Generate a secure webhook secret
- Set strong admin credentials
- Add your OpenAI API key

## Running the Application

1. Start the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Testing

1. Run the test suite:
```bash
python -m pytest
```

2. Test the webhook endpoint:
```bash
curl -X POST http://localhost:8000/api/webhook \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'username:password' | base64)" \
  -d @tests/test_data/normal_transaction.json
```

## Development

1. Enable debug mode in `.env`:
```env
DEBUG=True
```

2. The server will automatically reload when code changes are detected.

## Monitoring

1. Check the logs:
```bash
tail -f app.log
```

2. Monitor notifications:
```bash
curl http://localhost:8000/api/notifications \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)"
```

## Security Considerations

1. Keep your `.env` file secure and never commit it to version control
2. Regularly rotate webhook secrets and admin credentials
3. Monitor API usage and implement rate limiting in production
4. Use HTTPS in production environments
5. Regularly update dependencies for security patches

## Production Deployment

1. Use a production-grade WSGI server (e.g., Gunicorn)
2. Set up proper logging and monitoring
3. Configure SSL/TLS certificates
4. Implement proper backup strategies
5. Set up alerting for system health

## Troubleshooting

1. Check the logs for detailed error messages
2. Verify environment variables are set correctly
3. Ensure all dependencies are installed
4. Confirm API keys are valid and have sufficient permissions
5. Check network connectivity and firewall settings

## Support

For issues and support:
1. Check the documentation
2. Review common issues in troubleshooting guide
3. Contact the development team

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request