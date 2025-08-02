

# AI BackLog Assistant

This repository contains a multi-agent system built on CrewAI for analyzing and processing various types of user data (video, audio, images, documents, text).

## Features

- **Pipeline Architecture**: Organized into three main pipelines (IPP, IMP, OP) for clear data flow
- **Modular Architecture**: Each agent performs a specialized role within pipelines
- **Extensible Design**: Easy to add new agents and data types to pipelines
- **Vector Memory**: Uses Weaviate for efficient data storage and retrieval
- **CrewAI Integration**: Manages agents and tasks through CrewAI framework
- **Advanced Document Processing**: Entity extraction, classification, and routing
- **Multi-language Support**: Russian and English document analysis
- **Reflection Agents**: Advanced agents for document analysis and reflection
- **Self-Learning**: Categorization agents improve over time with new examples
- **Production NLP**: Integrated sentence-transformers for high-quality embeddings
- **LLM Fallback**: Automatic fallback to LLM for low-confidence categorizations
- **Prioritization**: RICE/ICE scoring, bottleneck detection, and criticality classification
- **Pipeline Coordination**: Clear data contracts and validation between pipeline stages

## Components

1. **Pipelines**: Organized processing pipelines for clear data flow
   - **Input Processing Pipeline (IPP)**: Primary data ingestion and structuring
   - **Information Manipulation Pipeline (IMP)**: Analysis, enrichment, and decision making
   - **Output Pipeline (OP)**: Final result preparation and delivery
   - **MainPipelineCoordinator**: Manages end-to-end pipeline coordination

2. **Agents**: Specialized modules for different processing tasks
   - **ReflectionAgent**: Analyzes input data and determines required actions
   - **Contextual Router**: Semantic routing for document processing (analyzers/contextual_router.py)
   - **Document Classifier**: Categorizes documents by type (analyzers/document_classifier.py)
   - **Document Parser**: Extracts entities and structured blocks (analyzers/document_parser.py)
   - **Report Handler**: Processes and structures various report types (handlers/report_handler.py)
   - **CategorizationAgent**: Comprehensive document categorization (agents/categorization/)
     - **DocumentClassifierAgent**: Determines document type using LLM
     - **DomainClassifierAgent**: Identifies industry domain using LLM
     - **SemanticTaggingAgent**: Extracts semantic tags and entities using LLM
     - **SimilarityMatcherAgent**: Finds similar documents using Weaviate
     - **DocumentGroupAssignerAgent**: Assigns documents to groups/clusters
     - **SecondLevelCategorizationAgent**: Performs domain-specific categorization
       - **ITCategorizer**: Classifies IT-related documents (bug reports, API specs, etc.)
       - **FinanceCategorizer**: Classifies finance documents (invoices, reports, etc.)
       - **LegalCategorizer**: Classifies legal documents (contracts, court decisions, etc.)
       - **HealthcareCategorizer**: Classifies medical documents (records, prescriptions, etc.)
       - **PersonalGrowthCategorizer**: Classifies personal development documents (goals, reflections, etc.)
       - **CustomerSupportCategorizer**: Classifies support tickets (technical issues, billing questions, etc.)
       - **ProjectManagementCategorizer**: Classifies project documents (plans, task lists, etc.)
       - **FallbackCategorizer**: Handles general documents
       - **DomainRouter**: Routes documents to appropriate domain-specific categorizers
   - **ContextualizationAgent**: Context enrichment and memory management (agents/contextualization_agent/)
     - **ReferenceMatcherAgent**: Finds knowledge base references using Weaviate
     - **KnowledgeGraphAgent**: Builds knowledge graphs from document content
     - **DocumentRelinkerAgent**: Links related document fragments
     - **ContextMemoryAgent**: Manages long-term context memory
     - **ContextualizerCore**: Coordinates all contextualization sub-agents
   - **Reflection Agents**: Advanced agents for document analysis (agents/reflection/)
     - **FactVerificationAgent**: Verifies factual accuracy of statements (requires LLM)
     - **AdvancedSentimentAndToneAnalyzer**: Analyzes sentiment and tone (requires LLM)
     - **SummaryGenerator**: Generates document summaries (requires LLM)
   - **Information Manipulation Pipeline (IMP) Agents**:
     - **ResultAggregatorAgent**: Aggregates results from IPP agents
     - **ContextEnricherAgent**: Adds contextual information from knowledge bases
     - **MetadataEnricherAgent**: Enhances metadata with analysis results
     - **QualityAssuranceAgent**: Ensures final output quality
- **PrioritizationAgent**: Enhanced prioritization with configurable thresholds, LLM integration, and detailed reasoning
- **ScoringAgent**: Calculates ICE/RICE scores with automatic parameter estimation and LLM support
- **BottleneckDetectorAgent**: Enhanced bottleneck detection with configurable thresholds and risk analysis
- **CriticalityClassifierAgent**: Advanced criticality classification with effort-impact ratio and risk factor analysis
- **EffortEstimatorAgent**: Enhanced effort estimation with LLM integration and fallback heuristics
   - (Future agents for video, audio, image, document, and text processing)

2. **Memory**: Weaviate-based vector store for data persistence

3. **Schemas**: Pydantic models for data validation and structure

4. **Utilities**: Supporting modules for document processing
   - **Table Extractor**: Extracts tables from PDF, DOCX, TXT (utils/table_extractor.py)
   - **Text Cleaner**: Normalizes and cleans text data (tools/text_cleaner.py)
   - **File Type Detector**: Identifies document types (utils/filetype_detector.py)

## Implementation Status

### Completed
- ✅ DocumentClassifierAgent with placeholder logic
- ✅ DomainClassifierAgent with placeholder logic
- ✅ SemanticTaggingAgent with placeholder logic
- ✅ SimilarityMatcherAgent with placeholder logic
- ✅ DocumentGroupAssignerAgent with placeholder logic
- ✅ CategorizationAgent coordinator
- ✅ SecondLevelCategorizationAgent with domain-specific categorizers
- ✅ ITCategorizer for IT-related documents
- ✅ FinanceCategorizer for finance documents
- ✅ FallbackCategorizer for general documents
- ✅ DomainRouter for categorization routing
- ✅ Embedding-based classification with sentence-transformers
- ✅ Enhanced PrioritizationAgent with configurable thresholds and LLM integration
- ✅ Enhanced BottleneckDetectorAgent with risk analysis and configurable thresholds
- ✅ Enhanced CriticalityClassifierAgent with effort-impact ratio and risk factor analysis
- ✅ Enhanced EffortEstimatorAgent with LLM integration and improved heuristics
- ✅ Comprehensive test coverage for all prioritization components
- ✅ PrioritizationAgent with ICE/RICE scoring and bottleneck detection
- ✅ Test suite for categorization functionality
- ✅ Self-learning mechanism for categorization improvement
- ✅ LLM fallback for low-confidence categorizations
- ✅ Production-ready NLP dependencies
- ✅ Comprehensive logging and retraining system
- ✅ Pipeline architecture with IPP, IMP, and OP pipelines
- ✅ Base pipeline class with validation and error handling
- ✅ Main pipeline coordinator for end-to-end processing
- ✅ IMP agents: ResultAggregatorAgent, ContextEnricherAgent, MetadataEnricherAgent, QualityAssuranceAgent
- ✅ Data contracts and validation schemas for all pipelines

### In Progress
- ⏳ LLM integration for all sub-agents
- ⏳ Advanced analytics capabilities
- ⏳ Integration of existing agents into new pipeline architecture

### Future Work
- 🔮 Integrate spaCy and networkx for KnowledgeGraphAgent
- 🔮 Complete LLM integration for reflection agents
- 🔮 Add more domain-specific categorizers (legal, medical, etc.)
- 🔮 Implement FastAPI interface for production deployment
- 🔮 Add async processing support for pipelines
- 🔮 Implement parallel processing for independent agents

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Weaviate instance
4. Configure environment variables

## Usage

```python
from agents.categorization.categorization_agent import CategorizationAgent

# Initialize components
categorizer = CategorizationAgent()

# Process a document
text = "Договор № 345/2023 от 01.07.2023 между ООО «Пример» и ИП Иванов"

# Categorize document
result = categorizer.categorize_document(text)
print(result)
# Output: {
#   "document_type": "contract",
#   "domain": "legal",
#   "second_level_category": {"category": "contract", "confidence": 0.95, "source": "legal"},
#   "semantic_tags": ["agreement", "date", "parties"],
#   "similar_documents": [...],
#   "group": "legal_contracts"
# }

### Using Pipeline Architecture

```python
from pipelines import MainPipelineCoordinator

# Create pipeline coordinator
coordinator = MainPipelineCoordinator()

# Process data through complete pipeline
result = coordinator.process_end_to_end(
    document_id="doc_001",
    raw_content="Text or binary content about AI pipeline architecture",
    metadata={"source": "user_upload", "user": "researcher"}
)

print("Final Result:")
print(f"Document ID: {result['document_id']}")
print(f"Summary: {result['summary']}")
print(f"Key Points: {result['key_points']}")
print(f"Recommendations: {result['recommendations']}")
print(f"Format: {result['delivery_format']}")

# Output: {
#   "document_id": "doc_001",
#   "summary": "Comprehensive analysis of AI pipeline architecture...",
#   "key_points": ["Pipeline stages", "Data flow", "Agent coordination"],
#   "recommendations": ["Implement async processing", "Add monitoring"],
#   "formatted_output": "Final formatted result",
#   "delivery_format": "json"
# }
```

### Using Individual Pipelines

```python
from pipelines import MainPipelineCoordinator

coordinator = MainPipelineCoordinator()

# Step 1: Input Processing Pipeline
ipp_result = coordinator.process_ipp({
    "document_id": "doc_001",
    "raw_content": "Text content to process",
    "metadata": {"source": "api"}
})

# Step 2: Information Manipulation Pipeline
imp_result = coordinator.process_imp(ipp_result)

# Step 3: Output Pipeline
final_result = coordinator.process_op(imp_result)
```

## Testing

Run tests with:
```bash
# Test categorization functionality
python test_categorization_agent.py
python test_second_level_categorization.py
python test_self_learning_categorization.py

# Test prioritization functionality
python test_prioritization_agent.py

# Test pipeline architecture
python test_simple_pipeline.py
python test_main_coordinator.py
python test_pipeline.py
```

## Future Plans

- Add more specialized agents
- Implement FastAPI interface
- Add advanced analytics capabilities
- Integrate with external APIs for enhanced data processing
- Complete LLM integration for all reflection agents
- Implement proper NLP and vector search dependencies for ContextualizationAgent sub-agents
- Integrate spaCy and networkx for KnowledgeGraphAgent
- Add more domain-specific categorizers for comprehensive document analysis

## System Administration Agents

### Overview

The system includes a hierarchical agent system for centralized administration, monitoring, and error handling. The system follows a super-agent pattern with specialized sub-agents for different administrative tasks.

### Architecture

The system consists of a `SuperAdminAgent` that coordinates several specialized sub-agents:

1. **ErrorHandlerAgent** - Handles exceptions and errors
2. **LogCollectorAgent** - Collects and manages system logs
3. **NotificationAgent** - Sends alerts and notifications
4. **SecurityAgent** - Handles access control and security monitoring
5. **DiagnosticsAgent** - Runs system health checks and diagnostics
6. **MonitoringAgent** - Monitors system resources and services

### Directory Structure

```
agents/
├── base.py                  # Base agent class
├── super_admin_agent.py     # Main super agent
└── system_admin/            # Sub-agents
    ├── error_handler_agent.py
    ├── log_collector_agent.py
    ├── monitoring_agent.py
    ├── notification_agent.py
    ├── security_agent.py
    └── diagnostics_agent.py
```

### Usage Example

```python
from agents.super_admin_agent import SuperAdminAgent

# Initialize the super agent
admin = SuperAdminAgent()

# Check system health
health_report = admin.health_check()
print("System Health:", health_report)

# Handle errors
try:
    # Some operation that might fail
    pass
except Exception as e:
    admin.handle_exception(e, "module_name")

# Check access permissions
if admin.check_access("user_id", "read", "resource"):
    # Grant access
    pass
else:
    # Deny access
    admin.notify_admin("Unauthorized access attempt")

# Run security scan
security_report = admin.run_security_scan()
print("Security Status:", security_report)
```

### Testing

Run tests with:
```bash
python -m unittest tests/test_system_admin_agents.py
```

