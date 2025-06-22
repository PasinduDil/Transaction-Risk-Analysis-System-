from src.common.models import Transaction, RiskAnalysis, AdminNotification
from typing import Dict, Any
from datetime import datetime

def format_transaction_details(transaction: Transaction) -> str:
    """
    Format transaction details for notification.
    
    Args:
        transaction: Transaction object
        
    Returns:
        str: Formatted transaction details
    """
    return f"""
    Transaction ID: {transaction.transaction_id}
    Amount: {transaction.amount} {transaction.currency}
    Time: {transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}
    
    Customer:
    - ID: {transaction.customer.id}
    - Country: {transaction.customer.country}
    - IP: {transaction.customer.ip_address}
    
    Payment Method:
    - Type: {transaction.payment_method.type}
    - Last Four: {transaction.payment_method.last_four}
    - Country: {transaction.payment_method.country_of_issue}
    
    Merchant:
    - Name: {transaction.merchant.name}
    - Category: {transaction.merchant.category}
    """

def format_risk_analysis(analysis: RiskAnalysis) -> str:
    """
    Format risk analysis results for notification.
    
    Args:
        analysis: RiskAnalysis object
        
    Returns:
        str: Formatted risk analysis
    """
    risk_level = "HIGH" if analysis.risk_score >= 0.7 else "MEDIUM" if analysis.risk_score >= 0.3 else "LOW"
    
    return f"""
    Risk Level: {risk_level} (Score: {analysis.risk_score:.2f})
    
    Risk Factors:
    {chr(10).join(f'- {factor}' for factor in analysis.risk_factors)}
    
    Analysis:
    {analysis.reasoning}
    
    Recommended Action: {analysis.recommended_action.upper()}
    """

def create_email_notification(notification: AdminNotification) -> Dict[str, str]:
    """
    Create email notification content.
    
    Args:
        notification: AdminNotification object
        
    Returns:
        Dict containing email subject and body
    """
    subject = f"High Risk Transaction Alert - Score {notification.risk_score:.2f}"
    
    body = f"""
    HIGH RISK TRANSACTION DETECTED
    
    {format_transaction_details(notification.transaction_details)}
    

    RISK ANALYSIS:

    {format_risk_analysis(RiskAnalysis(
        risk_score=notification.risk_score,
        risk_factors=notification.risk_factors,
        reasoning=notification.llm_analysis,
        recommended_action='block' if notification.risk_score >= 0.7 else 'review'
    ))}
    

    Please review this transaction immediately and take appropriate action.

    Access the admin dashboard for more details and to update the status of this alert.

    Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
    """
    
    return {
        "subject": subject,
        "body": body
    }

def create_slack_notification(notification: AdminNotification) -> Dict[str, Any]:
    """
    Create Slack notification content.
    
    Args:
        notification: AdminNotification object
        
    Returns:
        Dict containing Slack message format
    """
    return {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🚨 High Risk Transaction - Score {notification.risk_score:.2f}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Transaction ID:*\n{notification.transaction_id}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Amount:*\n{notification.transaction_details.amount} {notification.transaction_details.currency}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Risk Factors:*\n{chr(10).join(f'• {factor}' for factor in notification.risk_factors)}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Analysis:*\n{notification.llm_analysis}"
                }
            }
        ]
    }