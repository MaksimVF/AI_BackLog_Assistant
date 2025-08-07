






import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.system_admin.monitoring_agent import MonitoringAgent
from agents.system_admin.logging_manager import initialize_logging
from agents.system_admin.self_healing_agent import SelfHealingAgent
from agents.system_admin.historical_analyzer import HistoricalAnalyzer

# Initialize FastAPI app
app = FastAPI(
    title="AI_BackLog_Assistant Web Dashboard",
    description="Web interface for monitoring and managing AI_BackLog_Assistant",
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

# Initialize logging
logging_manager = initialize_logging(
    service_name="WebDashboard",
    environment=os.getenv('ENV', 'dev')
)

# Initialize system components
monitoring_agent = MonitoringAgent()
self_healing_agent = SelfHealingAgent()
historical_analyzer = HistoricalAnalyzer()

# Pydantic models for API responses
class SystemStatus(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    process_count: int
    status: str
    timestamp: str

class LogEntry(BaseModel):
    timestamp: str
    level: str
    service: str
    environment: str
    message: str
    logger: str
    module: str
    function: str
    line: int

class Alert(BaseModel):
    id: str
    timestamp: str
    level: str
    message: str
    source: str
    status: str

class TrendAnalysis(BaseModel):
    metric: str
    trend: Dict[str, Any]
    forecast: Dict[str, Any]
    risk_level: str
    recommendations: List[str]

class ConfigUpdate(BaseModel):
    parameter: str
    value: Any

# WebSocket manager for real-time updates
class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                self.disconnect(connection)

ws_manager = WebSocketManager()

# API Endpoints
@app.get("/api/status", response_model=SystemStatus)
async def get_system_status():
    """Get current system status"""
    try:
        status = monitoring_agent.get_current_status()
        return SystemStatus(
            cpu_usage=status.get('cpu_usage', 0.0),
            memory_usage=status.get('memory_usage', 0.0),
            disk_usage=status.get('disk_usage', 0.0),
            process_count=status.get('process_count', 0),
            status=status.get('status', 'unknown'),
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logging.error(f"Failed to get system status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get system status")

@app.get("/api/logs", response_model=List[LogEntry])
async def get_logs(limit: int = 100, level: Optional[str] = None):
    """Get recent log entries"""
    try:
        # In a real implementation, this would query the logging system
        # For now, return mock data
        logs = []
        for i in range(min(limit, 10)):
            logs.append(LogEntry(
                timestamp=datetime.utcnow().isoformat(),
                level=level or "INFO",
                service="WebDashboard",
                environment="dev",
                message=f"Test log message {i+1}",
                logger="test",
                module="test",
                function="test",
                line=1
            ))
        return logs
    except Exception as e:
        logging.error(f"Failed to get logs: {e}")
        raise HTTPException(status_code=500, detail="Failed to get logs")

@app.get("/api/alerts", response_model=List[Alert])
async def get_alerts(status: Optional[str] = None):
    """Get active alerts"""
    try:
        # In a real implementation, this would query the alert system
        alerts = []
        for i in range(3):
            alerts.append(Alert(
                id=f"alert-{i+1}",
                timestamp=datetime.utcnow().isoformat(),
                level="WARNING",
                message=f"Test alert message {i+1}",
                source="system",
                status=status or "active"
            ))
        return alerts
    except Exception as e:
        logging.error(f"Failed to get alerts: {e}")
        raise HTTPException(status_code=500, detail="Failed to get alerts")

@app.get("/api/trends", response_model=List[TrendAnalysis])
async def get_trend_analysis():
    """Get trend analysis and predictions"""
    try:
        # Get predictions from historical analyzer
        predictions = historical_analyzer.predict_system_issues()

        # Format response
        results = []
        for metric, prediction in predictions.get('predictions', {}).items():
            results.append(TrendAnalysis(
                metric=metric,
                trend=prediction.get('trend', {}),
                forecast=prediction.get('forecast', {}),
                risk_level=prediction.get('issue_prediction', {}).get('risk_level', 'unknown'),
                recommendations=prediction.get('issue_prediction', {}).get('predicted_issues', [])
            ))

        return results
    except Exception as e:
        logging.error(f"Failed to get trend analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to get trend analysis")

@app.post("/api/self-healing")
async def trigger_self_healing(action: str):
    """Trigger self-healing action"""
    try:
        if action == "optimize_resources":
            result = self_healing_agent.optimize_resources()
        elif action == "restart_service":
            result = self_healing_agent.restart_service("test_service")
        elif action == "clear_cache":
            result = self_healing_agent.clear_cache()
        else:
            raise HTTPException(status_code=400, detail="Invalid action")

        return {"status": "success", "result": result}
    except Exception as e:
        logging.error(f"Failed to trigger self-healing: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to trigger self-healing: {e}")

@app.post("/api/config")
async def update_config(update: ConfigUpdate):
    """Update system configuration"""
    try:
        # In a real implementation, this would update the configuration
        # For now, just log the update
        logging.info(f"Configuration update requested: {update.parameter} = {update.value}")

        # Return mock response
        return {
            "status": "success",
            "parameter": update.parameter,
            "value": update.value,
            "message": "Configuration updated successfully"
        }
    except Exception as e:
        logging.error(f"Failed to update configuration: {e}")
        raise HTTPException(status_code=500, detail="Failed to update configuration")

# WebSocket endpoint for real-time updates
@app.websocket("/ws/updates")
async def websocket_updates(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

# Background task to send periodic updates
async def send_periodic_updates():
    """Send periodic updates to WebSocket clients"""
    while True:
        try:
            # Get system status
            status = monitoring_agent.get_current_status()

            # Send update
            await ws_manager.broadcast({
                "type": "system_status",
                "data": status,
                "timestamp": datetime.utcnow().isoformat()
            })

            # Wait before next update
            await asyncio.sleep(10)
        except Exception as e:
            logging.error(f"Failed to send periodic update: {e}")
            await asyncio.sleep(10)

# Start background task
@app.on_event("startup")
async def startup_event():
    """Handle startup events"""
    logging.info("Starting Web Dashboard backend")
    # Start periodic updates
    asyncio.create_task(send_periodic_updates())

if __name__ == "__main__":
    import uvicorn
    import asyncio

    # Run the FastAPI app
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )






