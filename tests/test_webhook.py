import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timezone
from main import app
from src.common.config import Settings
from src.webhook.auth import get_password_hash
import base64
import json

# Initialize test client
client = TestClient(app)
settings = Settings()

# Test data
NORMAL_TRANSACTION = {
    "transaction_id": "tx_testnormal",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "amount": 99.99,
    "currency": "USD",
    "customer": {
        "id": "cust_test123",
        "country": "US",
        "ip_address": "192.168.1.1"
    },
    "payment_method": {
        "type": "credit_card",
        "last_four": "4242",
        "country_of_issue": "US"
    },
    "merchant": {
        "id": "merch_test123",
        "name": "Test Store",
        "category": "electronics"
    }
}

CROSS_BORDER_TRANSACTION = {
    **NORMAL_TRANSACTION,
    "transaction_id": "tx_testcrossborder",
    "customer": {**NORMAL_TRANSACTION["customer"], "country": "US"},
    "payment_method": {**NORMAL_TRANSACTION["payment_method"], "country_of_issue": "CA"}
}

HIGH_VALUE_TRANSACTION = {
    **NORMAL_TRANSACTION,
    "transaction_id": "tx_testhighvalue",
    "amount": 9999.99
}

HIGH_RISK_COUNTRY_TRANSACTION = {
    **NORMAL_TRANSACTION,
    "transaction_id": "tx_testhighrisk",
    "customer": {**NORMAL_TRANSACTION["customer"], "country": "RU"}
}

INCOMPLETE_TRANSACTION = {
    "transaction_id": "tx_testincomplete",
    "amount": 99.99,
    "currency": "USD"
}

def get_auth_header(username: str, password: str) -> dict:
    """Generate Basic Auth header."""
    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {credentials}"}

@pytest.fixture
def auth_headers():
    """Fixture for authentication headers."""
    return get_auth_header(settings.ADMIN_USERNAME, settings.WEBHOOK_SECRET)

def test_webhook_normal_transaction(auth_headers):
    """Test normal transaction processing."""
    response = client.post(
        "/api/webhook",
        json=NORMAL_TRANSACTION,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "risk_score" in data

def test_webhook_cross_border_transaction(auth_headers):
    """Test cross-border transaction processing."""
    response = client.post(
        "/api/webhook",
        json=CROSS_BORDER_TRANSACTION,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert float(data["risk_score"]) >= 0.3  # Expect higher risk for cross-border

def test_webhook_high_value_transaction(auth_headers):
    """Test high-value transaction processing."""
    response = client.post(
        "/api/webhook",
        json=HIGH_VALUE_TRANSACTION,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert float(data["risk_score"]) >= 0.3  # Expect higher risk for large amounts

def test_webhook_high_risk_country(auth_headers):
    """Test transaction from high-risk country."""
    response = client.post(
        "/api/webhook",
        json=HIGH_RISK_COUNTRY_TRANSACTION,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert float(data["risk_score"]) >= 0.7  # Expect very high risk

def test_webhook_incomplete_data(auth_headers):
    """Test handling of incomplete transaction data."""
    response = client.post(
        "/api/webhook",
        json=INCOMPLETE_TRANSACTION,
        headers=auth_headers
    )
    assert response.status_code == 422
    assert "detail" in response.json()

def test_webhook_invalid_auth():
    """Test handling of invalid authentication."""
    response = client.post(
        "/api/webhook",
        json=NORMAL_TRANSACTION,
        headers=get_auth_header("wrong", "credentials")
    )
    assert response.status_code == 401

def test_webhook_missing_auth():
    """Test handling of missing authentication."""
    response = client.post(
        "/api/webhook",
        json=NORMAL_TRANSACTION
    )
    assert response.status_code == 401

def test_webhook_invalid_json(auth_headers):
    """Test handling of invalid JSON data."""
    response = client.post(
        "/api/webhook",
        data="invalid json",
        headers=auth_headers
    )
    assert response.status_code == 422

def test_webhook_future_timestamp(auth_headers):
    """Test handling of future timestamp."""
    future_transaction = {
        **NORMAL_TRANSACTION,
        "timestamp": "2025-12-31T23:59:59Z"
    }
    response = client.post(
        "/api/webhook",
        json=future_transaction,
        headers=auth_headers
    )
    assert response.status_code == 422

def test_webhook_invalid_amount(auth_headers):
    """Test handling of invalid amount."""
    invalid_amount_transaction = {
        **NORMAL_TRANSACTION,
        "amount": -100
    }
    response = client.post(
        "/api/webhook",
        json=invalid_amount_transaction,
        headers=auth_headers
    )
    assert response.status_code == 422