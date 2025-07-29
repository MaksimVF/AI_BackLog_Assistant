# AI BackLog Assistant

This repository contains a multi-agent system built on CrewAI for analyzing and processing various types of user data (video, audio, images, documents, text).

## Features

- **Modular Architecture**: Each agent performs a specialized role
- **Extensible Design**: Easy to add new agents and data types
- **Vector Memory**: Uses Weaviate for efficient data storage and retrieval
- **CrewAI Integration**: Manages agents and tasks through CrewAI framework

## Components

1. **Agents**: Specialized modules for different processing tasks
   - ReflectionAgent: Analyzes input data and determines required actions
   - (Future agents for video, audio, image, document, and text processing)

2. **Memory**: Weaviate-based vector store for data persistence

3. **Schemas**: Pydantic models for data validation and structure

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start Weaviate (locally or via Docker)

3. Run the system:
   ```bash
   python main.py
   ```

## Future Plans

- Add more specialized agents
- Implement FastAPI interface
- Add advanced analytics capabilities
