from src.common.models import RiskAnalysis
import json
from typing import Dict, Any

def parse_llm_response(response: str) -> RiskAnalysis:
    """
    Parse and validate LLM response into RiskAnalysis object.
    
    Args:
        response: JSON string from LLM
        
    Returns:
        RiskAnalysis object
        
    Raises:
        ValueError: If response format is invalid
    """
    try:
        # Parse JSON response
        data = json.loads(response)
        
        # Validate required fields
        required_fields = ["risk_score", "risk_factors", "reasoning", "recommended_action"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate risk score range
        risk_score = float(data["risk_score"])
        if not 0.0 <= risk_score <= 1.0:
            raise ValueError("Risk score must be between 0.0 and 1.0")
        
        # Validate risk factors
        if not isinstance(data["risk_factors"], list):
            raise ValueError("Risk factors must be a list")
        
        # Validate recommended action
        valid_actions = ["allow", "review", "block"]
        if data["recommended_action"] not in valid_actions:
            raise ValueError(f"Invalid recommended action. Must be one of: {valid_actions}")
        
        # Create RiskAnalysis object
        return RiskAnalysis(
            risk_score=risk_score,
            risk_factors=data["risk_factors"],
            reasoning=data["reasoning"],
            recommended_action=data["recommended_action"]
        )
        
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON response from LLM")
    except Exception as e:
        raise ValueError(f"Error parsing LLM response: {str(e)}")

def extract_key_insights(analysis: RiskAnalysis) -> Dict[str, Any]:
    """
    Extract key insights from risk analysis for notification purposes.
    
    Args:
        analysis: RiskAnalysis object
        
    Returns:
        Dict containing key insights
    """
    return {
        "risk_level": "high" if analysis.risk_score >= 0.7 else "medium" if analysis.risk_score >= 0.3 else "low",
        "primary_factors": analysis.risk_factors[:3] if len(analysis.risk_factors) > 3 else analysis.risk_factors,
        "recommended_action": analysis.recommended_action,
        "summary": analysis.reasoning[:200] + "..." if len(analysis.reasoning) > 200 else analysis.reasoning
    }