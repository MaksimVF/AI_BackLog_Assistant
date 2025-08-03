




# AI Backlog Assistant Web Server

## Overview

This Flask-based web server provides the backend for the AI Backlog Assistant web interface. It includes:

- User authentication system with group/organization support
- API endpoints for document upload and processing
- Integration with the pipeline system
- Web interface for managing projects and analytics
- Organization-based access control

## Features

### Authentication

- User registration and login
- Session management
- Protected routes for authenticated users
- Organization-based access control
- Role-based permissions (owner, admin, member, viewer)

### Organization Management

- Create and manage organizations
- Invite/remove users from organizations
- Switch between personal and organization contexts
- Role-based access within organizations

### API Endpoints

- `/api/status` - System status
- `/api/upload` - Document upload for processing
- Organization management endpoints
- Additional endpoints for pipeline integration

### Web Interface

- Dashboard with project overview
- Project management pages
- Analytics and visualization
- User settings and configuration
- Organization management interface

## Setup

### Requirements

- Python 3.7+
- Flask and related dependencies (see requirements.txt)
- PostgreSQL (recommended) or SQLite

### Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export SECRET_KEY='your-secret-key-here'
   export DATABASE_URL='postgresql://username:password@localhost/dbname'  # or use SQLite
   ```

3. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

### Running the Server

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Access the web interface at `http://localhost:5000`

## Integration with Pipeline System

The web server is designed to integrate with the AI Backlog Assistant pipeline system. When documents are uploaded:

1. The document is received via the `/api/upload` endpoint
2. It's processed through the pipeline system
3. Results are returned to the user interface

## Organization Model

The system supports both personal and organizational contexts:

- **Personal access**: Users can work individually
- **Organizational access**: Users can collaborate within organizations
- **Role-based permissions**: Different roles (owner, admin, member, viewer) have different access levels
- **Context switching**: Users can switch between personal and organizational contexts

## Future Enhancements

- Add more detailed analytics endpoints
- Implement API key management
- Add document management features
- Enhance error handling and logging
- Add Telegram bot integration

## License

This project is licensed under the MIT License.


