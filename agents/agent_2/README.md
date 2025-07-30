
# Agent 2: Contextual Document Router

## Overview

Agent 2 provides semantic routing capabilities for directing documents to appropriate sub-agents based on their content. This module uses the `semantic_router` package with embedding-based classification to determine the most suitable handler for different types of documents.

## Features

- **Semantic Routing**: Uses embeddings to understand document content and route accordingly
- **Document Specialization**: Handles invoices, contracts, reports, and generic text
- **Extensible**: Easy to add new document types and handlers
- **Fallback Handling**: Gracefully handles unknown or empty inputs

## Components

### Contextual Router

The main component that performs semantic analysis and routing:

- **Routes**: Predefined document types with example utterances
  - `invoice_handler`: For invoices, acts, and receipts
  - `contract_handler`: For contracts and agreements
  - `report_handler`: For reports and summaries
  - `generic_handler`: For general text

## Installation

The required dependencies are automatically installed with the main project. The key dependencies are:

- `semantic-router[fastembed]`
- `fastembed` (installed as part of semantic-router)

## Usage

```python
from agents.agent_2.contextual_router import route_text

# Example document text
document = "Настоящий договор аренды заключён между сторонами..."

# Route the document
agent_name = route_text(document)
print(f"Document routed to: {agent_name}")
```

## API

### `route_text(text: str) -> str`

Determine the most appropriate sub-agent for the given text.

**Parameters:**
- `text`: Input text to route

**Returns:**
- Name of the sub-agent route

### `get_all_routes() -> List[str]`

Get a list of all available route names.

### `get_route_description(route_name: str) -> Optional[str]`

Get the description for a specific route.

## Testing

Run the test script to verify the routing functionality:

```bash
python test_agent_2_router.py
```

## Integration

This module can be integrated with the main agent system by:

1. Importing the `route_text` function
2. Using it to determine which sub-agent should process a given document
3. Passing the document to the appropriate handler based on the route

## Future Enhancements

- Add more specialized document types
- Implement confidence scoring for routing decisions
- Add multilingual support
- Integrate with the main agent workflow

## Example

See `example_agent_2_usage.py` for a complete usage example.
