import pytest
from src.llm.analyzer import analyze_transaction_risk, calculate_base_risk_score
from src.llm.parser import parse_llm_response, extract_key_insights
from src.common.models import Transaction, RiskAnalysis
from datetime import datetime, timezone
import json

# Test data
SAMPLE_TRANSACTION = Transaction(
    transaction_id="tx_test123",
    timestamp=datetime.now(timezone.utc),
    amount=99.99,
    currency="USD",
    customer={
        "id": "cust_test",
        "country": "US",
        "ip_address": "192.168.1.1"
    },
    payment_method={
        "type": "credit_card",
        "last_four": "4242",
        "country_of_issue": "US"
    },
    merchant={
        "id": "merch_test",
        "name": "Test Store",
        "category": "electronics"
    }
)

SAMPLE_LLM_RESPONSE = """
{
    "risk_score": 0.7,
    "risk_factors": [
        "High transaction amount",
        "Cross-border payment"
    ],
    "reasoning": "Transaction shows elevated risk due to high amount and cross-border nature",
    "recommended_action": "review"
}
"""

@pytest.mark.asyncio
async def test_analyze_transaction_risk():
    """Test transaction risk analysis."""
    risk_analysis = await analyze_transaction_risk(SAMPLE_TRANSACTION)
    
    assert isinstance(risk_analysis, RiskAnalysis)
    assert 0 <= risk_analysis.risk_score <= 1
    assert isinstance(risk_analysis.risk_factors, list)
    assert risk_analysis.reasoning
    assert risk_analysis.recommended_action in ["allow", "review", "block"]

def test_calculate_base_risk_score():
    """Test base risk score calculation."""
    # Test normal transaction
    normal_score = calculate_base_risk_score(SAMPLE_TRANSACTION)
    assert 0 <= normal_score <= 1
    
    # Test high-risk country transaction
    high_risk_transaction = SAMPLE_TRANSACTION.model_copy()
    high_risk_transaction.customer.country = "RU"
    high_risk_score = calculate_base_risk_score(high_risk_transaction)
    assert high_risk_score > normal_score
    
    # Test cross-border transaction
    cross_border_transaction = SAMPLE_TRANSACTION.model_copy()
    cross_border_transaction.payment_method.country_of_issue = "CA"
    cross_border_score = calculate_base_risk_score(cross_border_transaction)
    assert cross_border_score > normal_score

def test_parse_llm_response():
    """Test LLM response parsing."""
    risk_analysis = parse_llm_response(SAMPLE_LLM_RESPONSE)
    
    assert isinstance(risk_analysis, RiskAnalysis)
    assert risk_analysis.risk_score == 0.7
    assert len(risk_analysis.risk_factors) == 2
    assert risk_analysis.recommended_action == "review"

def test_parse_llm_response_invalid_json():
    """Test handling of invalid JSON in LLM response."""
    with pytest.raises(ValueError):
        parse_llm_response("invalid json")

def test_parse_llm_response_missing_fields():
    """Test handling of missing fields in LLM response."""
    invalid_response = """
    {
        "risk_score": 0.5,
        "risk_factors": []
    }
    """
    with pytest.raises(ValueError):
        parse_llm_response(invalid_response)

def test_parse_llm_response_invalid_score():
    """Test handling of invalid risk score in LLM response."""
    invalid_response = """
    {
        "risk_score": 1.5,
        "risk_factors": [],
        "reasoning": "test",
        "recommended_action": "review"
    }
    """
    with pytest.raises(ValueError):
        parse_llm_response(invalid_response)

def test_parse_llm_response_invalid_action():
    """Test handling of invalid recommended action in LLM response."""
    invalid_response = """
    {
        "risk_score": 0.5,
        "risk_factors": [],
        "reasoning": "test",
        "recommended_action": "invalid"
    }
    """
    with pytest.raises(ValueError):
        parse_llm_response(invalid_response)

def test_extract_key_insights():
    """Test extraction of key insights from risk analysis."""
    risk_analysis = RiskAnalysis(
        risk_score=0.8,
        risk_factors=["factor1", "factor2", "factor3", "factor4"],
        reasoning="Test reasoning that is quite long and needs to be truncated properly",
        recommended_action="block"
    )
    
    insights = extract_key_insights(risk_analysis)
    
    assert insights["risk_level"] == "high"
    assert len(insights["primary_factors"]) <= 3
    assert len(insights["summary"]) <= 200
    assert insights["recommended_action"] == "block"