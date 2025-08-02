

# AI Backlog Assistant Pipeline Architecture

## Overview

This document describes the new pipeline architecture for the AI Backlog Assistant, which organizes the agents into three main pipelines:

1. **Input Processing Pipeline (IPP)** - Primary data ingestion and structuring
2. **Information Manipulation Pipeline (IMP)** - Analysis, enrichment, and decision making
3. **Output Pipeline (OP)** - Final result preparation and delivery

## Architecture Diagram

```
[Raw Input Data] → [Input Processing Pipeline] → [Structured Data] →
→ [Information Manipulation Pipeline] → [Enriched Data] →
→ [Output Pipeline] → [Final Results]
```

## Pipeline Components

### 1. Input Processing Pipeline (IPP)

**Purpose**: Convert raw input data into structured format with basic metadata.

**Agents**:
- `ModalityDetectorAgent` - Determines input modality (text/audio/video)
- `TextProcessorAgent` - Processes text input
- `AudioTranscriberAgent` - Converts audio to text
- `VideoAnalyzerAgent` - Analyzes video content
- `EntityExtractor` - Extracts entities from processed content
- `IntentIdentifier` - Identifies user intent
- `MetadataBuilder` - Creates initial metadata

**Input Schema**:
```json
{
  "document_id": "unique_identifier",
  "raw_content": "any",
  "metadata": {}
}
```

**Output Schema**:
```json
{
  "document_id": "unique_identifier",
  "raw_text": "processed_text",
  "modality": "text/audio/video",
  "entities": {"entity_type": ["values"]},
  "intent": "identified_intent",
  "metadata": {"key": "value"}
}
```

### 2. Information Manipulation Pipeline (IMP)

**Purpose**: Analyze, enrich, and process data to extract insights and make decisions.

**Agents**:
- `ResultAggregatorAgent` - Aggregates IPP results
- `ContextEnricherAgent` - Adds contextual information
- `PrioritizationAgent` - Determines priority
- `CriticalityClassifierAgent` - Assesses criticality
- `BottleneckDetectorAgent` - Identifies bottlenecks
- `ScoringAgent` - Calculates priority scores
- `DecisionMakerAgent` - Makes recommendations
- `MetadataEnricherAgent` - Adds analysis metadata
- `QualityAssuranceAgent` - Ensures output quality

**Input Schema**: IPP Output Schema

**Output Schema**:
```json
{
  "document_id": "unique_identifier",
  "processed_text": "enriched_text",
  "analysis": {
    "priority": "high/medium/low",
    "criticality": "critical/important/normal",
    "bottlenecks": ["list_of_issues"],
    "scores": {"priority_score": 8.5, "criticality_score": 7.2},
    "decision": "recommended_action"
  },
  "metadata": {"enriched": "metadata"},
  "quality": {"completeness": 95, "accuracy": 92}
}
```

### 3. Output Pipeline (OP)

**Purpose**: Prepare and deliver final results to users.

**Agents**:
- `SummaryAgent` - Generates summaries
- `OutputAgent` - Formats and delivers results
- `FormatAdapter` - Adapts to different output formats
- `ResponseFormatter` - Structures the response
- `OutputSanitizer` - Ensures quality and security

**Input Schema**: IMP Output Schema

**Output Schema**:
```json
{
  "document_id": "unique_identifier",
  "summary": "final_summary_text",
  "key_points": ["point1", "point2"],
  "recommendations": ["recommendation1"],
  "formatted_output": "final_result",
  "delivery_format": "json/html/pdf"
}
```

## Implementation

### Base Pipeline

All pipelines inherit from `BasePipeline` which provides:
- Input/output validation
- Performance tracking
- Error handling
- Logging

### Pipeline Coordination

The `MainPipelineCoordinator` manages the end-to-end flow:
- Sequentially processes data through IPP → IMP → OP
- Handles data transformation between pipelines
- Provides individual pipeline access for testing

### Data Contracts

Each pipeline defines Pydantic models for input/output validation:
- `IPPInputSchema` / `IPPOutputSchema`
- `IMPInputSchema` / `IMPOutputSchema`
- `OPInputSchema` / `OPOutputSchema`

## Usage Example

```python
from pipelines import MainPipelineCoordinator

# Create coordinator
coordinator = MainPipelineCoordinator()

# Process data end-to-end
result = coordinator.process_end_to_end(
    document_id="doc_001",
    raw_content="Text or binary content",
    metadata={"source": "user_upload"}
)

# Access individual pipelines
ipp_result = coordinator.process_ipp(data)
imp_result = coordinator.process_imp(ipp_result)
op_result = coordinator.process_op(imp_result)
```

## Benefits

1. **Clear Separation of Concerns**: Each pipeline has distinct responsibilities
2. **Improved Maintainability**: Easier to update individual agents
3. **Better Scalability**: Can add new agents without major refactoring
4. **Standardized Data Flow**: Clear contracts between pipelines
5. **Enhanced Quality Control**: Dedicated QA stage

## Testing

The architecture includes:
- Unit tests for individual agents
- Integration tests for pipeline coordination
- Mock implementations for development/testing

## Future Enhancements

1. Add async processing support
2. Implement parallel processing for independent agents
3. Add monitoring and observability
4. Implement versioning for pipeline configurations
5. Add dynamic pipeline configuration

