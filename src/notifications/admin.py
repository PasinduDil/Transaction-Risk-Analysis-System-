from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from src.common.models import AdminNotification
from src.common.config import Settings
from typing import List, Dict
import json
import aiofiles
from datetime import datetime
import os

router = APIRouter()
security = HTTPBasic()
settings = Settings()

# In a production environment, use a proper database
NOTIFICATIONS_FILE = "notifications.json"

async def load_notifications() -> List[Dict]:
    """Load notifications from storage."""
    try:
        if not os.path.exists(NOTIFICATIONS_FILE):
            return []
        async with aiofiles.open(NOTIFICATIONS_FILE, mode='r') as f:
            content = await f.read()
            return json.loads(content) if content else []
    except Exception:
        return []

async def save_notifications(notifications: List[Dict]) -> None:
    """Save notifications to storage."""
    def datetime_handler(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return str(obj)

    async with aiofiles.open(NOTIFICATIONS_FILE, mode='w') as f:
        await f.write(json.dumps(notifications, default=datetime_handler))

async def send_notification(notification: AdminNotification) -> None:
    """
    Send notification to administrators.
    
    Args:
        notification: AdminNotification object
    """
    try:
        # Load existing notifications
        notifications = await load_notifications()
        
        # Add new notification
        notifications.append(notification.model_dump())
        
        # Save updated notifications
        await save_notifications(notifications)
        
        # In a production environment, you would also want to:
        # 1. Send email alerts
        # 2. Trigger push notifications
        # 3. Update admin dashboard
        # 4. Log the notification in monitoring system
        
    except Exception as e:
        raise Exception(f"Failed to send notification: {str(e)}")

@router.get("/notifications", response_model=List[AdminNotification])
async def get_notifications(
    credentials: HTTPBasicCredentials = Depends(security),
    status: str = None
) -> List[AdminNotification]:
    """
    Get list of notifications with optional status filter.
    
    Args:
        credentials: Admin credentials
        status: Optional status filter (pending, reviewed, dismissed)
    """
    # Verify admin credentials
    if not verify_admin_auth(credentials):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"}
        )
    
    try:
        notifications = await load_notifications()
        
        # Apply status filter if provided
        if status:
            notifications = [n for n in notifications if n.get("status") == status]
        
        return [AdminNotification(**n) for n in notifications]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/notifications/{notification_id}/status")
async def update_notification_status(
    notification_id: str,
    status: str,
    credentials: HTTPBasicCredentials = Depends(security)
) -> Dict[str, str]:
    """
    Update notification status.
    
    Args:
        notification_id: ID of the notification to update
        status: New status (reviewed or dismissed)
        credentials: Admin credentials
    """
    if status not in ["reviewed", "dismissed"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    # Verify admin credentials
    if not verify_admin_auth(credentials):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"}
        )
    
    try:
        notifications = await load_notifications()
        
        # Find and update notification
        for notification in notifications:
            if notification.get("transaction_id") == notification_id:
                notification["status"] = status
                notification["updated_at"] = datetime.utcnow().isoformat()
                await save_notifications(notifications)
                return {"message": f"Notification status updated to {status}"}
        
        raise HTTPException(status_code=404, detail="Notification not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def verify_admin_auth(credentials: HTTPBasicCredentials) -> bool:
    """Verify admin credentials."""
    return (
        credentials.username == settings.ADMIN_USERNAME and
        credentials.password == settings.ADMIN_PASSWORD
    )