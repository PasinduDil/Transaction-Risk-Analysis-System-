from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from src.webhook.routes import router as webhook_router
from src.notifications.admin import router as notification_router
from src.common.config import Settings
import uvicorn

app = FastAPI(
    title="Transaction Risk Analysis API",
    description="API for analyzing transaction risks using LLM and notifying administrators",
    version="1.0.0"
)

# Load settings
settings = Settings()

# Add security
security = HTTPBasic()

# Include routers
app.include_router(webhook_router, prefix="/api", tags=["webhook"])
app.include_router(notification_router, prefix="/api", tags=["notifications"])

@app.get("/")
async def root():
    return {"message": "Transaction Risk Analysis API"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )