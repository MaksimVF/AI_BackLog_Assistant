

from fastapi import FastAPI
from api.auth import router as auth_router
from api.admin import router as admin_router
from level2.api.router import router as level2_router
from config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI(
    title="AI Backlog Assistant API",
    description="Secure API for AI Backlog Assistant with authentication and authorization",
    version="1.0.0"
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(admin_router)
app.include_router(level2_router)
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to AI Backlog Assistant API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        # Uncomment the following lines to enable HTTPS
        # ssl_keyfile=SSL_KEY,
        # ssl_certfile=SSL_CERTIFICATE,
    )

