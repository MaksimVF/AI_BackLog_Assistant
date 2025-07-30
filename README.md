
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
   - (Future agents for video, audio, image, document, and text processing)

2. **Memory**: Weaviate-based vector store for data persistence

3. **Schemas**: Pydantic models for data validation and structure

4. **Utilities**: Supporting modules for document processing
   - **Table Extractor**: Extracts tables from PDF, DOCX, TXT (utils/table_extractor.py)
   - **Text Cleaner**: Normalizes and cleans text data (tools/text_cleaner.py)
   - **File Type Detector**: Identifies document types (utils/filetype_detector.py)

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

## Usage Example

```python
from analyzers.document_parser import DocumentParser
from analyzers.contextual_router import ContextualRouter
from agents.categorization.categorization_agent import CategorizationAgent

# Initialize components
parser = DocumentParser()
router = ContextualRouter()
categorizer = CategorizationAgent()

# Process a document
text = "Договор № 345/2023 от 01.07.2023 между ООО «Пример» и ИП Иванов"

# Extract entities
entities = parser.parse(text)
print(entities)
# Output: {'date': '01.07.2023', 'sum': '120 000,00 руб', ...}

# Route document
context = router.route("example_contract.txt")
print(context["route"])
# Output: 'contract_handler'

# Categorize document
categorization = categorizer.categorize_document(text)
print(categorization)
# Output: {
#   'document_type': 'договор',
#   'domain': 'юриспруденция',
#   'semantic_tags': ['договор', 'ООО', 'ИП', 'поставка', 'товары'],
#   'similar_documents': [
#     {'id': 'doc_1', 'score': 0.91, 'summary': 'Похожий документ 1'},
#     {'id': 'doc_2', 'score': 0.87, 'summary': 'Похожий документ 2'}
#   ],
#   'group': {
#     'group_id': 'group_001',
#     'group_name': 'Общие документы',
#     'confidence': 0.85,
#     'tags': ['документ', 'общий', 'неклассифицированный']
#   }
# }
```

# Contextualize document
from agents.contextualization_agent.contextualizer_core import ContextualizerCore
contextualizer = ContextualizerCore()
context = contextualizer.process_document(text)
print(context)
# Output: {
#   'text': 'Договор № 345/2023 от 01.07.2023 между ООО «Пример» и ИП Иванов',
#   'chunks': ['Договор № 345/2023 от 01.07.2023', 'между ООО «Пример» и ИП Иванов'],
#   'knowledge_graph': {
#     'entities': ['ООО Пример', 'Иванов', 'Договор', 'Москва'],
#     'relations': [('ООО Пример', 'заключает', 'Договор'), ...]
#   },
#   'references': {
#     'Договор № 345/2023 от 01.07.2023': [{'content': 'Совпадение 1', 'title': 'Документ 1', 'certainty': 0.9}],
#     'между ООО «Пример» и ИП Иванов': [{'content': 'Совпадение 2', 'title': 'Документ 2', 'certainty': 0.8}]
#   },
#   'clusters': [[{'source': 'document', 'text': 'Договор № 345/2023 от 01.07.2023'}, ...]]
# }
```

## Current Status

The system has been implemented with a focus on reflection agents. However, several key agents require LLM (Language Model) integration for full functionality:

### LLM-Dependent Agents (Requiring Future Implementation)

1. **FactVerificationAgent** (agents/reflection/fact_verification_agent.py)
   - Requires LLM client for factual verification
   - Placeholder implementation currently returns a message about missing dependencies

2. **AdvancedSentimentAndToneAnalyzer** (agents/reflection/advanced_sentiment_tone_analyzer.py)
   - Requires LLM client for advanced sentiment analysis
   - Placeholder implementation currently returns a message about missing dependencies

3. **SummaryGenerator** (agents/reflection/summary_generator.py)
   - Requires LLM client for document summarization
   - Placeholder implementation currently returns a message about missing dependencies

## Next Steps

To complete the implementation, the following tasks need to be addressed:

1. **Implement LLM Client**: Create the core LLM client module (`core.llm_client`)
2. **Add Text Splitter Utility**: Implement the text splitting utility (`tools.utils.text_splitter`)
3. **Integrate LLM Dependencies**: Update the placeholder implementations in the reflection agents
4. **Test LLM Integrations**: Verify that all LLM-dependent agents work correctly with the new dependencies
5. **Enhance CategorizationAgent**: Improve the sub-agents with more sophisticated classification and mapping algorithms

## Future Plans

- Add more specialized agents
- Implement FastAPI interface
- Add advanced analytics capabilities
- Integrate with external APIs for enhanced data processing
- Complete LLM integration for all reflection agents
- Implement proper NLP and vector search dependencies for ContextualizationAgent sub-agents
- Integrate spaCy and networkx for KnowledgeGraphAgent
- Add Weaviate integration for ReferenceMatcherAgent
