



import os
import sys
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the third level router
from app_third_level import router as third_level_router

# Create the FastAPI app
app = FastAPI(
    title="AI Backlog Assistant - Third Level API",
    description="Third level API for AI Backlog Assistant",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the third level router
app.include_router(third_level_router)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Handle startup events"""
    print("Starting AI Backlog Assistant - Third Level API")

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI app
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,  # Use a different port than the web dashboard
        log_level="info"
    )


