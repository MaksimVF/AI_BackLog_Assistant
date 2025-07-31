

# AI BackLog Assistant

This repository contains a multi-agent system built on CrewAI for analyzing and processing various types of user data (video, audio, images, documents, text).

## Features

- **Modular Architecture**: Each agent performs a specialized role
- **Extensible Design**: Easy to add new agents and data types
- **Vector Memory**: Uses Weaviate for efficient data storage and retrieval
- **CrewAI Integration**: Manages agents and tasks through CrewAI framework
- **Advanced Document Processing**: Entity extraction, classification, and routing
- **Multi-language Support**: Russian and English document analysis
- **Reflection Agents**: Advanced agents for document analysis and reflection
- **Self-Learning**: Categorization agents improve over time with new examples
- **Production NLP**: Integrated sentence-transformers for high-quality embeddings
- **LLM Fallback**: Automatic fallback to LLM for low-confidence categorizations
    - **Prioritization**: RICE\/ICE scoring, bottleneck detection, and criticality classification

## Components

1. **Agents**: Specialized modules for different processing tasks
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
    - **PrioritizationAgent**: Assigns RICE\/ICE score, finds bottlenecks, returns priority status
    - **ScoringAgent**: Calculates ICE\/RICE scores with automatic parameter estimation
    - **BottleneckDetectorAgent**: Identifies task bottlenecks and dependencies
    - **CriticalityClassifierAgent**: Classifies tasks as critical\/high\/medium\/low
    - **EffortEstimatorAgent**: Estimates effort when not provided
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
- ✅ PrioritizationAgent with ICE\/RICE scoring and bottleneck detection
- ✅ Test suite for categorization functionality
- ✅ Self-learning mechanism for categorization improvement
- ✅ LLM fallback for low-confidence categorizations
- ✅ Production-ready NLP dependencies
- ✅ Comprehensive logging and retraining system

### In Progress
- ⏳ LLM integration for all sub-agents
- ⏳ Advanced analytics capabilities

### Future Work
- 🔮 Integrate spaCy and networkx for KnowledgeGraphAgent
- 🔮 Complete LLM integration for reflection agents
- 🔮 Add more domain-specific categorizers (legal, medical, etc.)
- 🔮 Implement FastAPI interface for production deployment

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

## Testing

Run tests with:
```bash
python test_categorization_agent.py
python test_second_level_categorization.py
python test_self_learning_categorization.py
python test_prioritization_agent.py
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

