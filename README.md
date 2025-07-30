
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
     - **DocumentClassifierAgent**: Determines document type
     - **DomainClassifierAgent**: Identifies industry domain
     - **TaxonomyMapperAgent**: Maps to internal taxonomies
     - **TaggingAgent**: Extracts relevant tags and keywords
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
categorization = categorizer.categorize(text)
print(categorization)
# Output: {
#   'document_type': 'contract',
#   'domain': 'law',
#   'taxonomy': {
#     'okved_code': '69.10',
#     'kbk_code': '18210102010011000110',
#     'internal_classifier': 'contract_law_001'
#   },
#   'tags': ['договор', 'contract', 'medium_document']
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
