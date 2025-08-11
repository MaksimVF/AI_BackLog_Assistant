




import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.super_admin_agent import SuperAdminAgent
from security.permissions import require_role, TokenData
from models.user import UserRole
from config.llm_config import get_available_models, get_llm_config
from config.agent_config import get_agent_registry, AgentConfig, list_agents

# Initialize FastAPI app
app = FastAPI(
    title="AI_BackLog_Assistant Admin Panel",
    description="Administrative interface for AI_BackLog_Assistant",
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

# Initialize SuperAdminAgent
super_admin = SuperAdminAgent()

# Pydantic models for API responses
class SystemStatus(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    process_count: int
    status: str
    timestamp: str

class User(BaseModel):
    id: str
    username: str
    email: str
    role: str
    status: str

class Alert(BaseModel):
    id: str
    timestamp: str
    level: str
    message: str
    source: str
    status: str

class ConfigUpdate(BaseModel):
    parameter: str
    value: Any

class AgentInfo(BaseModel):
    name: str
    description: str
    default_model: Optional[str]
    allowed_models: List[str]
    enabled: bool

class AgentAssignment(BaseModel):
    agent_name: str
    model_name: str

class LLMModelInfo(BaseModel):
    name: str
    provider: str
    is_default: bool

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
@app.get("/api/admin/status", response_model=SystemStatus)
async def get_admin_status(current_user: TokenData = Depends(require_role(UserRole.ADMIN))):
    """Get current system status for admin"""
    try:
        # Get health check from SuperAdminAgent
        health_report = super_admin.health_check()

        # Extract monitoring data
        system_status = health_report.get('system_status', {})

        return SystemStatus(
            cpu_usage=system_status.get('cpu_usage', 0.0),
            memory_usage=system_status.get('memory_usage', 0.0),
            disk_usage=system_status.get('disk_usage', 0.0),
            process_count=system_status.get('process_count', 0),
            status=system_status.get('status', 'unknown'),
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logging.error(f"Failed to get admin status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get admin status")

@app.get("/api/admin/metrics")
async def get_system_metrics(current_user: TokenData = Depends(require_role(UserRole.ADMIN))):
    """Get detailed system metrics"""
    try:
        # Get health check and monitoring data
        health_report = super_admin.health_check()
        system_status = health_report.get('system_status', {})

        # Generate mock historical data for demonstration
        history = []
        for i in range(24):  # Last 24 hours
            history.append({
                "timestamp": f"{i}:00",
                "cpu_usage": system_status.get('cpu_usage', 0.0) + (i * 0.5),
                "memory_usage": system_status.get('memory_usage', 0.0) + (i * 0.3),
                "disk_usage": system_status.get('disk_usage', 0.0) + (i * 0.2)
            })

        return {
            "cpu_usage": system_status.get('cpu_usage', 0.0),
            "memory_usage": system_status.get('memory_usage', 0.0),
            "disk_usage": system_status.get('disk_usage', 0.0),
            "process_count": system_status.get('process_count', 0),
            "status": system_status.get('status', 'unknown'),
            "history": history
        }
    except Exception as e:
        logging.error(f"Failed to get system metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get system metrics")

@app.get("/api/admin/monitoring")
async def get_monitoring_data(current_user: TokenData = Depends(require_role(UserRole.ADMIN))):
    """Get comprehensive monitoring data"""
    try:
        # Get health check and monitoring data
        health_report = super_admin.health_check()
        system_status = health_report.get('system_status', {})

        # Generate mock historical data
        history = []
        for i in range(24):
            history.append({
                "timestamp": f"{i}:00",
                "cpu_usage": system_status.get('cpu_usage', 0.0) + (i * 0.5),
                "memory_usage": system_status.get('memory_usage', 0.0) + (i * 0.3),
                "disk_usage": system_status.get('disk_usage', 0.0) + (i * 0.2)
            })

        # Get alerts (mock data for now)
        alerts = [
            {
                "id": "alert-1",
                "level": "WARNING",
                "message": "High CPU usage detected",
                "source": "system_monitor",
                "timestamp": datetime.utcnow().isoformat()
            },
            {
                "id": "alert-2",
                "level": "INFO",
                "message": "Memory usage increasing",
                "source": "system_monitor",
                "timestamp": datetime.utcnow().isoformat()
            }
        ]

        return {
            "cpu_usage": system_status.get('cpu_usage', 0.0),
            "memory_usage": system_status.get('memory_usage', 0.0),
            "disk_usage": system_status.get('disk_usage', 0.0),
            "process_count": system_status.get('process_count', 0),
            "status": system_status.get('status', 'healthy'),
            "history": history,
            "alerts": alerts
        }
    except Exception as e:
        logging.error(f"Failed to get monitoring data: {e}")
        raise HTTPException(status_code=500, detail="Failed to get monitoring data")

@app.get("/api/admin/users", response_model=List[User])
async def get_users(current_user: TokenData = Depends(require_role(UserRole.ADMIN))):
    """Get user list"""
    try:
        # Mock user data for demonstration
        # In a real implementation, this would query the user database
        users = [
            {
                "id": "1",
                "username": "admin",
                "email": "admin@example.com",
                "role": "admin",
                "status": "active"
            },
            {
                "id": "2",
                "username": "user1",
                "email": "user1@example.com",
                "role": "user",
                "status": "active"
            },
            {
                "id": "3",
                "username": "manager",
                "email": "manager@example.com",
                "role": "manager",
                "status": "active"
            }
        ]
        return users
    except Exception as e:
        logging.error(f"Failed to get users: {e}")
        raise HTTPException(status_code=500, detail="Failed to get users")

@app.post("/api/admin/self-healing")
async def trigger_self_healing(
    action: str,
    current_user: TokenData = Depends(require_role(UserRole.ADMIN))
):
    """Trigger self-healing action"""
    try:
        if action == "optimize_resources":
            result = super_admin.perform_self_healing()
        elif action == "restart_service":
            result = super_admin.restart_service("test_service")
        else:
            raise HTTPException(status_code=400, detail="Invalid action")

        return {"status": "success", "result": result}
    except Exception as e:
        logging.error(f"Failed to trigger self-healing: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to trigger self-healing: {e}")

@app.post("/api/admin/config")
async def update_config(
    update: ConfigUpdate,
    current_user: TokenData = Depends(require_role(UserRole.ADMIN))
):
    """Update system configuration"""
    try:
        # In a real implementation, this would update the configuration
        logging.info(f"Configuration update requested: {update.parameter} = {update.value}")

        return {
            "status": "success",
            "parameter": update.parameter,
            "value": update.value,
            "message": "Configuration updated successfully"
        }
    except Exception as e:
        logging.error(f"Failed to update configuration: {e}")
        raise HTTPException(status_code=500, detail="Failed to update configuration")

@app.get("/api/admin/agents", response_model=List[AgentInfo])
async def get_agents(current_user: TokenData = Depends(require_role(UserRole.ADMIN))):
    """Get list of agents and their configurations"""
    try:
        agent_registry = get_agent_registry()
        agents = []

        for agent_name in agent_registry.list_agents():
            agent_config = agent_registry.get_agent_config(agent_name)
            if agent_config:
                agents.append(AgentInfo(
                    name=agent_config.name,
                    description=agent_config.description,
                    default_model=agent_config.default_model,
                    allowed_models=agent_config.allowed_models,
                    enabled=agent_config.enabled
                ))

        return agents
    except Exception as e:
        logging.error(f"Failed to get agents: {e}")
        raise HTTPException(status_code=500, detail="Failed to get agents")

@app.get("/api/admin/llm-models", response_model=List[LLMModelInfo])
async def get_llm_models(current_user: TokenData = Depends(require_role(UserRole.ADMIN))):
    """Get available LLM models"""
    try:
        llm_config = get_llm_config()
        models = []

        for model in llm_config.models:
            models.append(LLMModelInfo(
                name=model.name,
                provider=model.provider.value,
                is_default=model.is_default
            ))

        return models
    except Exception as e:
        logging.error(f"Failed to get LLM models: {e}")
        raise HTTPException(status_code=500, detail="Failed to get LLM models")

@app.post("/api/admin/agent-assignments")
async def assign_model_to_agent(
    assignment: AgentAssignment,
    current_user: TokenData = Depends(require_role(UserRole.ADMIN))
):
    """Assign an LLM model to an agent"""
    try:
        agent_registry = get_agent_registry()
        agent_config = agent_registry.get_agent_config(assignment.agent_name)

        if not agent_config:
            raise HTTPException(status_code=404, detail=f"Agent {assignment.agent_name} not found")

        # Check if model is available
        available_models = get_available_models()
        if assignment.model_name not in available_models:
            raise HTTPException(status_code=400, detail=f"Model {assignment.model_name} not available")

        # Check if model is allowed for this agent
        if assignment.model_name not in agent_config.allowed_models:
            raise HTTPException(status_code=400, detail=f"Model {assignment.model_name} not allowed for agent {assignment.agent_name}")

        # Assign the model to the agent
        agent_registry.set_default_model_for_agent(assignment.agent_name, assignment.model_name)

        return {
            "status": "success",
            "agent_name": assignment.agent_name,
            "model_name": assignment.model_name,
            "message": "Model assigned to agent successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to assign model to agent: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to assign model to agent: {e}")

# WebSocket endpoint for real-time updates
@app.websocket("/api/admin/ws/updates")
async def websocket_updates(websocket: WebSocket):
    """WebSocket endpoint for real-time admin updates"""
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

# Background task to send periodic updates
import asyncio

async def send_periodic_updates():
    """Send periodic updates to WebSocket clients"""
    while True:
        try:
            # Get system status
            health_report = super_admin.health_check()
            system_status = health_report.get('system_status', {})

            # Send update
            await ws_manager.broadcast({
                "type": "system_status",
                "data": {
                    "cpu_usage": system_status.get('cpu_usage', 0.0),
                    "memory_usage": system_status.get('memory_usage', 0.0),
                    "disk_usage": system_status.get('disk_usage', 0.0),
                    "status": system_status.get('status', 'unknown')
                },
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
    logging.info("Starting Admin Panel backend")
    # Start periodic updates
    asyncio.create_task(send_periodic_updates())

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI app
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=4000,  # Admin interface port
        log_level="info"
    )





