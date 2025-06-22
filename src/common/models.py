from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

class BaseModelWithConfig(BaseModel):
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda dt: dt.isoformat()
        }
    )

class Customer(BaseModelWithConfig):
    id: str = Field(..., pattern=r'^cust_[a-zA-Z0-9]+$')
    country: str = Field(..., pattern=r'^[A-Z]{2}$')
    ip_address: str = Field(..., pattern=r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')

class PaymentMethod(BaseModelWithConfig):
    type: str = Field(..., pattern=r'^(credit_card|debit_card|bank_transfer)$')
    last_four: str = Field(..., pattern=r'^\d{4}$')
    country_of_issue: str = Field(..., pattern=r'^[A-Z]{2}$')

class Merchant(BaseModelWithConfig):
    id: str = Field(..., pattern=r'^merch_[a-zA-Z0-9]+$')
    name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., pattern=r'^[a-z_]+$')

class Transaction(BaseModelWithConfig):
    transaction_id: str = Field(..., pattern=r'^tx_[a-zA-Z0-9]+$')
    timestamp: datetime
    amount: float = Field(..., gt=0)
    currency: str = Field(..., pattern=r'^[A-Z]{3}$')
    customer: Customer
    payment_method: PaymentMethod
    merchant: Merchant

class RiskAnalysis(BaseModelWithConfig):
    risk_score: float = Field(..., ge=0.0, le=1.0)
    risk_factors: List[str]
    reasoning: str
    recommended_action: str = Field(default="review", pattern=r'^(allow|review|block)$')

class AdminNotification(BaseModelWithConfig):
    alert_type: str = "high_risk_transaction"
    transaction_id: str
    risk_score: float
    risk_factors: List[str]
    transaction_details: Transaction
    llm_analysis: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"  # pending, reviewed, dismissed
    admin_notes: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }