from src.common.models import Transaction
from src.common.config import Settings
from datetime import datetime, timezone
from typing import List
import ipaddress

settings = Settings()

def validate_transaction_data(transaction: Transaction) -> None:
    """
    Validate transaction data for completeness and correctness.
    
    Args:
        transaction: Transaction object to validate
        
    Raises:
        ValueError: If validation fails
    """
    errors: List[str] = []
    
    # Validate timestamp
    try:
        # Ensure timestamp is not in the future
        if transaction.timestamp > datetime.now(timezone.utc):
            errors.append("Transaction timestamp cannot be in the future")
    except Exception:
        errors.append("Invalid timestamp format")
    
    # Validate amount
    if transaction.amount <= 0:
        errors.append("Transaction amount must be positive")
    
    # Validate currency
    if not transaction.currency or len(transaction.currency) != 3:
        errors.append("Invalid currency code")
    
    # Validate customer data
    if not transaction.customer.id or not transaction.customer.country:
        errors.append("Missing required customer information")
    
    # Validate IP address
    try:
        ipaddress.ip_address(transaction.customer.ip_address)
    except ValueError:
        errors.append("Invalid IP address")
    
    # Validate payment method
    if not transaction.payment_method.type or not transaction.payment_method.last_four:
        errors.append("Missing required payment method information")
    
    if len(transaction.payment_method.last_four) != 4 or not transaction.payment_method.last_four.isdigit():
        errors.append("Invalid payment method last four digits")
    
    # Validate merchant
    if not transaction.merchant.id or not transaction.merchant.name or not transaction.merchant.category:
        errors.append("Missing required merchant information")
    
    # Check for high-risk countries
    if (transaction.customer.country in settings.HIGH_RISK_COUNTRIES or
        transaction.payment_method.country_of_issue in settings.HIGH_RISK_COUNTRIES):
        # We don't raise an error for high-risk countries, but we'll let the risk analysis handle it
        pass
    
    if errors:
        raise ValueError("\n".join(errors))