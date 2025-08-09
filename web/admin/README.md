

# AI_BackLog_Assistant Admin Panel

## Overview

The Admin Panel provides a comprehensive administrative interface for managing the AI_BackLog_Assistant system. It includes user management, system monitoring, configuration management, log viewing, and alert management.

## Features

### 1. Dashboard
- Real-time system status monitoring
- System metrics visualization
- Quick access to key administrative functions

### 2. User Management
- View and manage user accounts
- Assign roles and permissions
- Monitor user activity

### 3. System Monitoring
- Real-time system health monitoring
- Resource utilization charts
- System alert management
- Self-healing controls

### 4. Configuration
- System parameter configuration
- LLM model management
- Tariff plan management
- Feature configuration

### 5. Log Management
- View system logs
- Filter and search logs
- Log level filtering

### 6. Alert Management
- View active alerts
- Acknowledge and resolve alerts
- Alert history

## Architecture

### Frontend
- **React**: JavaScript library for UI
- **Material-UI**: Component library
- **Recharts**: Charting library
- **Axios**: HTTP client
- **Socket.IO**: Real-time updates

### Backend
- **FastAPI**: Python web framework
- **WebSocket**: Real-time updates
- **SuperAdminAgent**: Administrative operations
- **JWT Authentication**: Secure access control

## Setup

### Backend

1. Install dependencies:
   ```bash
   cd web/admin/backend
   pip install -r requirements.txt
   ```

2. Run the backend:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 4000
   ```

### Frontend

1. Install dependencies:
   ```bash
   cd web/admin
   npm install
   ```

2. Run the frontend:
   ```bash
   npm start
   ```

## API Endpoints

### GET /api/admin/status
Get current system status.

**Response:**
```json
{
  "cpu_usage": 35.2,
  "memory_usage": 42.5,
  "disk_usage": 57.8,
  "process_count": 123,
  "status": "healthy",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

### GET /api/admin/metrics
Get detailed system metrics.

**Response:**
```json
{
  "cpu_usage": 35.2,
  "memory_usage": 42.5,
  "disk_usage": 57.8,
  "process_count": 123,
  "status": "healthy",
  "history": [
    {
      "timestamp": "00:00",
      "cpu_usage": 35.2,
      "memory_usage": 42.5,
      "disk_usage": 57.8
    }
  ]
}
```

### GET /api/admin/users
Get user list.

**Response:**
```json
[
  {
    "id": "1",
    "username": "admin",
    "email": "admin@example.com",
    "role": "admin",
    "status": "active"
  }
]
```

### POST /api/admin/self-healing
Trigger self-healing action.

**Request:**
```json
{
  "action": "optimize_resources"
}
```

**Response:**
```json
{
  "status": "success",
  "result": "Resources optimized"
}
```

## WebSocket

### /api/admin/ws/updates
Real-time updates for system status and alerts.

**Messages:**
```json
{
  "type": "system_status",
  "data": {
    "cpu_usage": 35.2,
    "memory_usage": 42.5,
    "disk_usage": 57.8,
    "status": "healthy"
  },
  "timestamp": "2023-01-01T00:00:00Z"
}
```

## Deployment

### Docker

1. Build backend image:
   ```bash
   cd web/admin/backend
   docker build -t ai-backlog-admin-backend .
   ```

2. Build frontend image:
   ```bash
   cd web/admin
   docker build -t ai-backlog-admin-frontend .
   ```

3. Run containers:
   ```bash
   docker-compose up
   ```

### Kubernetes

1. Apply manifests:
   ```bash
   kubectl apply -f k8s/
   ```

2. Access service:
   ```bash
   kubectl port-forward svc/ai-backlog-admin 8080:80
   ```

## Security

- **Authentication**: JWT with role-based access control
- **Authorization**: Admin role required for all endpoints
- **HTTPS**: Encrypt all traffic
- **2FA**: Two-factor authentication for admin access

## Future Enhancements

- **Advanced Analytics**: Predictive system monitoring
- **Audit Logs**: Comprehensive audit trail
- **Custom Dashboards**: User-configurable dashboards
- **Notification System**: Email/SMS alerts for critical events
- **Multi-tenant Support**: Organization-level administration

