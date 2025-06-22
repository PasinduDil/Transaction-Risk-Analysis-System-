from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from src.common.models import Transaction, AdminNotification
from src.common.config import Settings
from src.llm.analyzer import analyze_transaction_risk
from src.notifications.admin import send_notification
from src.webhook.auth import verify_webhook_auth
from src.webhook.validators import validate_transaction_data
from typing import Dict

router = APIRouter()
security = HTTPBasic()
settings = Settings()

@router.post("/webhook", response_model=Dict[str, str])
async def transaction_webhook(
    transaction: Transaction,
    credentials: HTTPBasicCredentials = Depends(security)
) -> Dict[str, str]:
    """Handle incoming transaction webhooks and perform risk analysis."""
    
    # Verify webhook authentication
    if not verify_webhook_auth(credentials):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"}
        )
    
    # Validate transaction data
    try:
        validate_transaction_data(transaction)
    except (ValueError, TypeError) as e:
        raise HTTPException(status_code=422, detail=str(e))
    
    # Analyze transaction risk using LLM
    try:
        risk_analysis = await analyze_transaction_risk(transaction)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk analysis failed: {str(e)}")
    
    # If high risk, notify administrators
    if risk_analysis.risk_score >= settings.HIGH_RISK_THRESHOLD:
        notification = AdminNotification(
            transaction_id=transaction.transaction_id,
            risk_score=risk_analysis.risk_score,
            risk_factors=risk_analysis.risk_factors,
            transaction_details=transaction,
            llm_analysis=risk_analysis.reasoning
        )
        await send_notification(notification)
    
    return {
        "status": "success",
        "message": "Transaction processed successfully",
        "transaction_id": transaction.transaction_id,
        "risk_score": str(risk_analysis.risk_score)
    }