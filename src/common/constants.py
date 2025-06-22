# Risk Analysis Constants
RISK_LEVELS = {
    "LOW": (0.0, 0.3),
    "MEDIUM": (0.3, 0.7),
    "HIGH": (0.7, 1.0)
}

# High-risk countries (based on AML/CFT considerations)
HIGH_RISK_COUNTRIES = [
    "RU",  # Russia
    "IR",  # Iran
    "KP",  # North Korea
    "VE",  # Venezuela
    "MM"   # Myanmar
]

# Transaction amount thresholds (in USD)
AMOUNT_THRESHOLDS = {
    "HIGH": 5000.00,
    "VERY_HIGH": 10000.00
}

# Time-based risk factors
TIME_RISK_FACTORS = {
    "UNUSUAL_HOURS": (22, 5),  # 10 PM to 5 AM considered unusual
    "VELOCITY_WINDOW_MINUTES": 60,  # Time window for checking transaction velocity
    "MAX_TRANSACTIONS_PER_HOUR": 10  # Maximum normal transactions per hour
}

# Payment method risk levels (0.0 to 1.0)
PAYMENT_METHOD_RISK = {
    "credit_card": 0.3,
    "debit_card": 0.2,
    "bank_transfer": 0.1,
    "crypto": 0.8,
    "prepaid_card": 0.6
}

# Merchant category risk levels (0.0 to 1.0)
MERCHANT_CATEGORY_RISK = {
    "gambling": 0.8,
    "cryptocurrency": 0.8,
    "jewelry": 0.6,
    "electronics": 0.4,
    "travel": 0.3,
    "retail": 0.2,
    "groceries": 0.1
}

# HTTP Response Messages
HTTP_MESSAGES = {
    "SUCCESS": "Transaction processed successfully",
    "INVALID_AUTH": "Invalid authentication credentials",
    "INVALID_DATA": "Invalid transaction data",
    "SERVER_ERROR": "Internal server error",
    "NOT_FOUND": "Resource not found"
}

# Notification Types
NOTIFICATION_TYPES = {
    "HIGH_RISK": "high_risk_transaction",
    "SUSPICIOUS": "suspicious_pattern",
    "SYSTEM_ERROR": "system_error"
}

# Notification Status
NOTIFICATION_STATUS = {
    "PENDING": "pending",
    "REVIEWED": "reviewed",
    "DISMISSED": "dismissed"
}

# API Rate Limits
RATE_LIMITS = {
    "WEBHOOK": 100,  # requests per minute
    "ADMIN_API": 1000  # requests per hour
}

# Cache Settings
CACHE_SETTINGS = {
    "TRANSACTION_CACHE_TTL": 3600,  # 1 hour in seconds
    "MAX_CACHE_SIZE": 10000  # Maximum number of cached items
}

# Logging Levels
LOG_LEVELS = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10
}