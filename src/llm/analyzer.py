from src.common.models import Transaction, RiskAnalysis
from src.common.config import Settings
from src.llm.prompts import get_risk_analysis_prompt
from src.llm.parser import parse_llm_response
import requests
from typing import Dict, Any
import json

settings = Settings()

async def analyze_transaction_risk(transaction: Transaction) -> RiskAnalysis:
    """
    Analyze transaction risk using Groq LLM.
    
    Args:
        transaction: Transaction object to analyze
        
    Returns:
        RiskAnalysis: Analysis results including risk score and factors
        
    Raises:
        Exception: If LLM analysis fails
    """
    try:
        # Calculate base risk score first
        base_risk_score = calculate_base_risk_score(transaction)
        
        try:
            # Prepare transaction data for the prompt
            transaction_json = transaction.model_dump_json()
            
            # Get the prompt template
            prompt = get_risk_analysis_prompt(transaction_json)
            
            # Call Groq API
            headers = {
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": settings.GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]}
                ],
                "temperature": settings.LLM_TEMPERATURE,
                "max_tokens": settings.LLM_MAX_TOKENS
            }
            
            response = requests.post(
                f"{settings.GROQ_API_ENDPOINT}/chat/completions",
                headers=headers,
                json=payload
            )
            
            response.raise_for_status()
            
            # Parse and validate LLM response
            llm_response = response.json()["choices"][0]["message"]["content"]
            risk_analysis = parse_llm_response(llm_response)
            
            return risk_analysis
            
        except (requests.exceptions.RequestException, Exception) as e:
            # If LLM analysis fails, return base risk analysis
            return RiskAnalysis(
                risk_score=base_risk_score,
                risk_factors=["LLM analysis unavailable - using base risk score"],
                reasoning="Risk analysis based on basic transaction properties due to LLM service unavailability."
            )
            
    except Exception as e:
        raise Exception(f"Risk analysis failed completely: {str(e)}")

def calculate_base_risk_score(transaction: Transaction) -> float:
    """
    Calculate initial risk score based on basic transaction properties.
    This serves as a fallback if LLM analysis fails.
    
    Args:
        transaction: Transaction to analyze
        
    Returns:
        float: Base risk score between 0.0 and 1.0
    """
    risk_score = 0.0
    
    # Check for high-risk countries
    if transaction.customer.country in settings.HIGH_RISK_COUNTRIES:
        risk_score += 0.4
    if transaction.payment_method.country_of_issue in settings.HIGH_RISK_COUNTRIES:
        risk_score += 0.4
    
    # Check for cross-border transaction
    if transaction.customer.country != transaction.payment_method.country_of_issue:
        risk_score += 0.3
    
    # Check for high-value transaction (over 1000)
    if transaction.amount > 1000:
        risk_score += 0.3
    elif transaction.amount > 500:
        risk_score += 0.2
    
    # Normalize risk score to be between 0 and 1
    return min(risk_score, 1.0)