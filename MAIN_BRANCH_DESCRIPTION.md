
# 🚀 AI BackLog Assistant - Main Branch Description

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
   - [Agents](#agents)
   - [Tools](#tools)
   - [Utilities](#utilities)
   - [Memory System](#memory-system)
4. [Agent Descriptions](#agent-descriptions)
5. [Data Flow](#data-flow)
6. [Technical Specifications](#technical-specifications)
7. [Implementation Status](#implementation-status)

---

## 🏢 Project Overview

AI BackLog Assistant is an intelligent multi-agent system built on CrewAI for analyzing and processing various types of user data including video, audio, images, documents, and text. The system features a modular architecture with specialized agents that perform different processing tasks.

## 🏛️ Architecture

The system follows a modular, agent-based architecture with these key components:

1. **Agents**: Specialized modules for different processing tasks
2. **Tools**: Utility functions and integrations
3. **Memory**: Weaviate-based vector store for data persistence
4. **Schemas**: Pydantic models for data validation
5. **Utilities**: Supporting modules for document processing

---

## 🔧 Core Components

### Agents

The system contains numerous specialized agents organized into categories:

#### 🤖 Core Agents
- **CoreAgent**: Main coordination agent
- **ReflectionAgent**: Cognitive analysis and pipeline optimization
- **InputClassifierAgent**: Determines input type and routes accordingly
- **AggregatorAgent**: Combines outputs from multiple agents
- **Router**: Routes tasks to appropriate agents

#### 📄 Document Processing Agents
- **CategorizationAgent**: Comprehensive document categorization
  - **DocumentClassifierAgent**: Determines document type
  - **DomainClassifierAgent**: Identifies industry domain
  - **SemanticTaggingAgent**: Extracts semantic tags
  - **SimilarityMatcherAgent**: Finds similar documents
  - **DocumentGroupAssignerAgent**: Assigns documents to groups
  - **SecondLevelCategorizationAgent**: Domain-specific categorization

#### 🧠 Contextualization Agents
- **ContextualizationAgent**: Context enrichment and memory management
  - **ReferenceMatcherAgent**: Finds knowledge base references
  - **KnowledgeGraphAgent**: Builds knowledge graphs
  - **DocumentRelinkerAgent**: Links related documents
  - **ContextMemoryAgent**: Manages long-term context memory

#### 📊 Prioritization Agents
- **PrioritizationAgent**: Task prioritization with ICE/RICE scoring
- **BottleneckDetectorAgent**: Identifies process bottlenecks
- **CriticalityClassifierAgent**: Classifies task criticality
- **EffortEstimatorAgent**: Estimates task effort
- **ScoringAgent**: Calculates prioritization scores

#### 🤖 Reflection Agents
- **ReflectionAgent**: Advanced document analysis
  - **FactVerificationAgent**: Verifies factual accuracy
  - **SentimentAndToneAnalyzer**: Analyzes sentiment and tone
  - **SummaryGenerator**: Generates document summaries
  - **CompletenessEvaluator**: Assesses information completeness
  - **AmbiguityResolver**: Identifies and resolves ambiguities

#### 🎯 Execution Planning Agents
- **ExecutionPlannerAgent**: Creates task execution plans
  - **TimelineEstimator**: Estimates task duration
  - **DeadlineCalculator**: Calculates precise deadlines
  - **SchedulingIntegrator**: Integrates with scheduling systems
  - **FollowUpNotifier**: Sets reminders and checkpoints

#### 🎨 Visualization Agents
- **VisualizationAgent**: Creates visual representations
  - **ChartGenerator**: Generates charts
  - **TableRenderer**: Renders tables
  - **ExportManager**: Handles data exports

#### 🔍 Analysis Agents
- **ImageAnalyzerAgent**: Analyzes image content
- **VideoAnalyzerAgent**: Processes video content
- **AudioTranscriberAgent**: Transcribes audio to text
- **TextProcessorAgent**: Processes text data
- **ModalityDetectorAgent**: Detects input modality

### Tools

The system includes various utility tools:

- **Audio2TextTool**: Audio transcription
- **Image2TextTool**: Image OCR and analysis
- **Video2TextTool**: Video frame extraction and analysis
- **PDFExtractor**: PDF content extraction
- **WeaviateStorageTool**: Vector database integration
- **LLMTool**: Language model integration
- **SimilarityTool**: Semantic similarity calculation

### Utilities

Supporting utilities include:

- **TableExtractor**: Extracts tables from documents
- **TextCleaner**: Normalizes and cleans text data
- **FileTypeDetector**: Identifies document types
- **DocumentClassifier**: Categorizes documents

### Memory System

- **WeaviateClient**: Vector database client for efficient storage and retrieval
- **SchemaConfig**: Weaviate schema configuration

---

## 🤖 Agent Descriptions

### CoreAgent
**Purpose**: Main coordination agent that manages the overall workflow
**Inputs**: User requests, agent outputs
**Outputs**: Processed results, coordination signals
**Key Functions**: Task routing, agent coordination, result aggregation

### ReflectionAgent
**Purpose**: Cognitive analysis and pipeline optimization
**Inputs**: Document content, metadata
**Outputs**: Analysis reports, pipeline adjustments
**Key Functions**: Completeness evaluation, ambiguity resolution, hypothesis generation

### CategorizationAgent
**Purpose**: Comprehensive document categorization
**Inputs**: Document text/content
**Outputs**: Categorization results with confidence scores
**Key Functions**: Document type classification, domain identification, semantic tagging

### PrioritizationAgent
**Purpose**: Task prioritization using ICE/RICE scoring
**Inputs**: Task data, effort estimates
**Outputs**: Prioritization scores, criticality classification
**Key Functions**: Bottleneck detection, effort estimation, scoring

### ExecutionPlannerAgent
**Purpose**: Creates comprehensive task execution plans
**Inputs**: Task data, decision results
**Outputs**: Execution plans with timelines and resources
**Key Functions**: Timeline estimation, deadline calculation, resource allocation

---

## 📊 Data Flow

1. **Input**: User submits data (video, audio, image, document, text)
2. **Modality Detection**: ModalityDetectorAgent identifies input type
3. **Routing**: Router directs input to appropriate processing agent
4. **Processing**: Specialized agents process the input
5. **Categorization**: CategorizationAgent classifies the content
6. **Contextualization**: ContextualizationAgent enriches context
7. **Reflection**: ReflectionAgent performs cognitive analysis
8. **Prioritization**: PrioritizationAgent determines importance
9. **Execution Planning**: ExecutionPlannerAgent creates action plan
10. **Output**: AggregatorAgent combines results for final output

---

## 🔧 Technical Specifications

- **Framework**: CrewAI
- **Vector Database**: Weaviate
- **NLP**: Sentence-transformers, spaCy
- **OCR**: Tesseract, EasyOCR
- **Audio Processing**: Whisper, Vosk
- **Video Processing**: OpenCV, FFmpeg
- **Languages**: Python (primary), support for Russian and English

---

## ✅ Implementation Status

### Completed Features
- ✅ Document classification and categorization
- ✅ Prioritization with ICE/RICE scoring
- ✅ Reflection agents for cognitive analysis
- ✅ Execution planning with timeline estimation
- ✅ Weaviate integration for vector storage
- ✅ Modality detection and routing
- ✅ Comprehensive test coverage

### In Progress
- ⏳ Advanced LLM integration
- ⏳ Enhanced analytics capabilities
- ⏳ Additional domain-specific categorizers

### Future Work
- 🔮 FastAPI interface for production
- 🔮 Additional document format support
- 🔮 Advanced NLP model integration
- 🔮 Real-time processing capabilities

---

*Last Updated: 2025-08-01*
