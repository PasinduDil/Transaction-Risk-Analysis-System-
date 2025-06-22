import pytest
from fastapi.testclient import TestClient
from main import app
from src.common.models import AdminNotification, Transaction
from src.notifications.admin import send_notification, load_notifications, save_notifications
from src.notifications.templates import (
    format_transaction_details,
    format_risk_analysis,
    create_email_notification,
    create_slack_notification
)
from datetime import datetime, timezone
import os
import json
import base64

# Initialize test client
client = TestClient(app)

# Test data
SAMPLE_TRANSACTION = Transaction(
    transaction_id="tx_test123",
    timestamp=datetime.now(timezone.utc),
    amount=999.99,
    currency="USD",
    customer={
        "id": "cust_test",
        "country": "US",
        "ip_address": "192.168.1.1"
    },
    payment_method={
        "type": "credit_card",
        "last_four": "4242",
        "country_of_issue": "CA"
    },
    merchant={
        "id": "merch_test",
        "name": "Test Store",
        "category": "electronics"
    }
)

SAMPLE_NOTIFICATION = AdminNotification(
    alert_type="high_risk_transaction",
    transaction_id="tx_test123",
    risk_score=0.85,
    risk_factors=[
        "Cross-border payment",
        "High transaction amount"
    ],
    transaction_details=SAMPLE_TRANSACTION,
    llm_analysis="High risk due to cross-border payment and large amount",
    timestamp=datetime.now(timezone.utc),
    status="pending"
)

@pytest.fixture
def auth_headers():
    """Fixture for authentication headers."""
    credentials = base64.b64encode(b"admin:admin").decode()
    return {"Authorization": f"Basic {credentials}"}

@pytest.fixture
def clean_notifications():
    """Fixture to ensure clean notification state."""
    if os.path.exists("notifications.json"):
        os.remove("notifications.json")
    yield
    if os.path.exists("notifications.json"):
        os.remove("notifications.json")

@pytest.mark.asyncio
async def test_send_notification(clean_notifications):
    """Test sending a notification."""
    await send_notification(SAMPLE_NOTIFICATION)
    
    notifications = await load_notifications()
    assert len(notifications) == 1
    assert notifications[0]["transaction_id"] == "tx_test123"

def test_get_notifications_endpoint(auth_headers, clean_notifications):
    """Test getting notifications through the API."""
    # First send a notification
    client.post(
        "/api/webhook",
        json=SAMPLE_TRANSACTION.model_dump(mode='json'),
        headers=auth_headers
    )
    
    # Then get notifications
    response = client.get("/api/notifications", headers=auth_headers)
    assert response.status_code == 200
    
    notifications = response.json()
    assert isinstance(notifications, list)
    if notifications:  # If notification was high risk enough to be recorded
        assert notifications[0]["transaction_id"] == "tx_test123"

def test_get_notifications_unauthorized():
    """Test getting notifications without authentication."""
    response = client.get("/api/notifications")
    assert response.status_code == 401

def test_update_notification_status(auth_headers, clean_notifications):
    """Test updating notification status."""
    # First create a notification
    client.post(
        "/api/webhook",
        json=SAMPLE_TRANSACTION.model_dump(mode='json'),
        headers=auth_headers
    )
    
    # Get the notification ID
    response = client.get("/api/notifications", headers=auth_headers)
    notifications = response.json()
    
    if notifications:  # If notification was created
        notification_id = notifications[0]["transaction_id"]
        
        # Update status
        response = client.put(
            f"/api/notifications/{notification_id}/status",
            json={"status": "reviewed"},
            headers=auth_headers
        )
        assert response.status_code == 200
        
        # Verify update
        response = client.get("/api/notifications", headers=auth_headers)
        updated_notifications = response.json()
        assert updated_notifications[0]["status"] == "reviewed"

def test_notification_templates():
    """Test notification template formatting."""
    # Test transaction details formatting
    transaction_details = format_transaction_details(SAMPLE_TRANSACTION)
    assert SAMPLE_TRANSACTION.transaction_id in transaction_details
    assert str(SAMPLE_TRANSACTION.amount) in transaction_details
    assert SAMPLE_TRANSACTION.currency in transaction_details
    
    # Test email notification
    email = create_email_notification(SAMPLE_NOTIFICATION)
    assert "subject" in email
    assert "body" in email
    assert SAMPLE_NOTIFICATION.transaction_id in email["body"]
    
    # Test Slack notification
    slack = create_slack_notification(SAMPLE_NOTIFICATION)
    assert "blocks" in slack
    assert len(slack["blocks"]) > 0
    assert SAMPLE_NOTIFICATION.transaction_id in str(slack["blocks"])

@pytest.mark.asyncio
async def test_notification_storage(clean_notifications):
    """Test notification storage operations."""
    # Test saving notifications
    notifications = [SAMPLE_NOTIFICATION.model_dump()]
    await save_notifications(notifications)
    
    # Test loading notifications
    loaded = await load_notifications()
    assert len(loaded) == 1
    assert loaded[0]["transaction_id"] == SAMPLE_NOTIFICATION.transaction_id
    
    # Test updating notifications
    loaded[0]["status"] = "reviewed"
    await save_notifications(loaded)
    
    # Verify update
    reloaded = await load_notifications()
    assert reloaded[0]["status"] == "reviewed"