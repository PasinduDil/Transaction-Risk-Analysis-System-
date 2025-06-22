from typing import Dict

def get_risk_analysis_prompt(transaction_json: str) -> Dict[str, str]:
    """
    Generate the prompt for transaction risk analysis.
    
    Args:
        transaction_json: Transaction data in JSON format
        
    Returns:
        Dict containing system and user prompts
    """
    system_prompt = """
    You are a specialized financial risk analyst. Evaluate transaction data and determine 
    a risk score from 0.0 (no risk) to 1.0 (extremely high risk) based on fraud patterns. 
    Provide clear reasoning and risk factors.
    
    Response format:
    {{
        "risk_score": 0.0-1.0,
        "risk_factors": ["factor1", "factor2"...],
        "reasoning": "Brief analysis explanation",
        "recommended_action": "allow|review|block"
    }}
    
    Consider:
    1. Geographic mismatches (customer/payment country differences, high-risk jurisdictions)
    2. Transaction patterns (unusual amounts, timing)
    3. Payment method risks
    4. Merchant category risks
    
    Score guidelines:
    - 0.0-0.3: Allow (low risk)
    - 0.3-0.7: Review (medium risk)
    - 0.7-1.0: Block (high risk)
    """
    
    user_prompt = f"Analyze this transaction:\n{transaction_json}"
    
    return {
        "system": system_prompt,
        "user": user_prompt
    }

def get_transaction_summary_prompt(transaction_json: str) -> Dict[str, str]:
    """
    Generate prompt for creating a human-readable transaction summary.
    
    Args:
        transaction_json: Transaction data in JSON format
        
    Returns:
        Dict containing system and user prompts
    """
    system_prompt = """
    Create a clear, concise summary of the transaction highlighting key details 
    and any unusual patterns. Focus on information relevant to risk assessment.
    """
    
    user_prompt = f"Summarize this transaction:\n{transaction_json}"
    
    return {
        "system": system_prompt,
        "user": user_prompt
    }