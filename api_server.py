


"""
API Server with health check endpoints for AI_BackLog_Assistant
"""

import os
import sys
import threading
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

# Add project root to path for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize enhanced logging system
from agents.system_admin.logging_manager import initialize_logging
from agents.system_admin.monitoring_agent import MonitoringAgent
from health import get_health_status, get_readiness_status

# Initialize logging
logging_manager = initialize_logging(
    service_name="APIServer",
    environment=os.getenv('ENV', 'dev')
)
logger = logging_manager.get_logger()

# Initialize monitoring agent
monitoring_agent = MonitoringAgent()

# Initialize FastAPI app
app = FastAPI(
    title="AI_BackLog_Assistant API",
    description="API for AI_BackLog_Assistant with health monitoring",
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

# Pydantic models for API responses
class HealthStatus(BaseModel):
    status: str
    timestamp: str
    system: dict
    services: dict
    alerts: list

class ReadinessStatus(BaseModel):
    status: str
    timestamp: str
    system: dict
    services: dict

# Start background monitoring
def start_background_monitoring():
    """Start background monitoring thread"""
    def monitoring_loop():
        while True:
            try:
                # Get and log system status periodically
                status = monitoring_agent.get_system_status()
                logger.info("Background monitoring update", extra={
                    'cpu_usage': status.get('cpu', {}).get('percent', 0),
                    'memory_usage': status.get('memory', {}).get('virtual', {}).get('percent', 0),
                    'disk_usage': status.get('disk', {}).get('usage', {}).get('percent', 0)
                })

                # Sleep for 60 seconds
                time.sleep(60)
            except Exception as e:
                logger.error(f"Background monitoring error: {e}")
                time.sleep(10)

    # Start monitoring thread
    monitoring_thread = threading.Thread(
        target=monitoring_loop,
        daemon=True,
        name="BackgroundMonitoring"
    )
    monitoring_thread.start()
    logger.info("Started background monitoring")

# API Endpoints
@app.get("/health", response_model=HealthStatus)
async def health_check():
    """Health check endpoint"""
    try:
        health_status = get_health_status()
        return health_status
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")

@app.get("/ready", response_model=ReadinessStatus)
async def readiness_check():
    """Readiness check endpoint"""
    try:
        readiness_status = get_readiness_status()
        return readiness_status
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=500, detail="Readiness check failed")

@app.get("/status")
async def system_status():
    """Get detailed system status"""
    try:
        status = monitoring_agent.get_system_status()
        return {
            'status': 'success',
            'timestamp': datetime.utcnow().isoformat(),
            'data': status
        }
    except Exception as e:
        logger.error(f"System status failed: {e}")
        raise HTTPException(status_code=500, detail="System status failed")

@app.get("/metrics")
async def system_metrics():
    """Get system metrics"""
    try:
        status = monitoring_agent.get_system_status()
        system_info = status.get('system', {})

        metrics = {
            'cpu': system_info.get('cpu', {}),
            'memory': system_info.get('memory', {}),
            'disk': system_info.get('disk', {}),
            'network': system_info.get('network', {}),
            'processes': system_info.get('processes', {})
        }

        return {
            'status': 'success',
            'timestamp': datetime.utcnow().isoformat(),
            'metrics': metrics
        }
    except Exception as e:
        logger.error(f"Metrics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Metrics retrieval failed")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Handle startup events"""
    logger.info("Starting API Server")
    start_background_monitoring()

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI app
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

