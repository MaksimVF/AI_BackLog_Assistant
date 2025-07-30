
# AI BackLog Assistant

This repository contains a multi-agent system built on CrewAI for analyzing and processing various types of user data (video, audio, images, documents, text).

## Features

- **Modular Architecture**: Each agent performs a specialized role
- **Extensible Design**: Easy to add new agents and data types
- **Vector Memory**: Uses Weaviate for efficient data storage and retrieval
- **CrewAI Integration**: Manages agents and tasks through CrewAI framework
- **Advanced Document Processing**: Entity extraction, classification, and routing
- **Multi-language Support**: Russian and English document analysis

## Components

1. **Agents**: Specialized modules for different processing tasks
   - **ReflectionAgent**: Analyzes input data and determines required actions
   - **Contextual Router**: Semantic routing for document processing (analyzers/contextual_router.py)
   - **Document Classifier**: Categorizes documents by type (analyzers/document_classifier.py)
   - **Document Parser**: Extracts entities and structured blocks (analyzers/document_parser.py)
   - **Report Handler**: Processes and structures various report types (handlers/report_handler.py)
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

# Initialize components
parser = DocumentParser()
router = ContextualRouter()

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
```

## Future Plans

- Add more specialized agents
- Implement FastAPI interface
- Add advanced analytics capabilities
- Integrate with external APIs for enhanced data processing
