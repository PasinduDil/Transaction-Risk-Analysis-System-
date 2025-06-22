from fastapi.security import HTTPBasicCredentials
from src.common.config import Settings
from passlib.context import CryptContext

# Initialize settings and password context
settings = Settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_webhook_auth(credentials: HTTPBasicCredentials) -> bool:
    """
    Verify webhook authentication credentials.
    
    Args:
        credentials: HTTPBasicCredentials object containing username and password
        
    Returns:
        bool: True if credentials are valid, False otherwise
    """
    try:
        # In a production environment, you would want to use constant-time comparison
        # to prevent timing attacks
        is_username_valid = credentials.username == settings.ADMIN_USERNAME
        is_password_valid = credentials.password == settings.WEBHOOK_SECRET
        
        return is_username_valid and is_password_valid
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """
    Generate password hash for storing in configuration.
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)