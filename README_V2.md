


# AI Backlog Assistant v2.0

## Overview

AI Backlog Assistant v2.0 is a refactored implementation that provides a cleaner, more modular architecture for processing and analyzing backlog items. This version focuses on:

1. **Clear separation of concerns** - Each agent has a specific responsibility
2. **Modular design** - Easy to add or replace components
3. **Improved performance** - More efficient processing pipeline
4. **Better maintainability** - Cleaner code organization

## Architecture

### Directory Structure

```
src/
├── v1/                      # Original implementation (preserved)
├── v2/                      # New refactored implementation
│   ├── agents/
│   │   ├── level1/          # Level 1 agents
│   │   │   ├── processors/  # Modality-specific processors
│   │   │   ├── input_receiver.py
│   │   │   ├── modality_detector.py
│   │   │   ├── content_classifier.py
│   │   │   └── trigger_agent.py
│   │   ├── level2/          # Level 2 agents (TBD)
│   │   └── level3/          # Level 3 agents (TBD)
│   ├── pipelines/           # Pipeline coordinators
│   │   ├── level1_pipeline.py
│   │   ├── level2_pipeline.py (TBD)
│   │   └── level3_pipeline.py (TBD)
│   └── main.py              # Main entry point
├── common/                  # Shared utilities and config
│   ├── config/
│   └── utils/
```

### Level 1 Processing Pipeline

The Level 1 pipeline consists of several agents that work together to process incoming data:

1. **Input Receiver Agent** - Validates and sanitizes input data
2. **Modality Detection Agent** - Determines the type of input (text, audio, video, image)
3. **Modality Processors** - Process data based on its modality:
   - Text Processor
   - Audio Transcriber
   - Video Processor
   - Image Processor
4. **Content Classifier Agent** - Classifies content type, emotion, and provides initial scoring
5. **Trigger Agent** - Determines when to trigger Level 2 processing

## Implementation Status

### Completed Components

- ✅ Input Receiver Agent
- ✅ Modality Detection Agent
- ✅ Text Processor
- ✅ Audio Transcriber (placeholder)
- ✅ Video Processor (placeholder)
- ✅ Image Processor (placeholder)
- ✅ Content Classifier Agent
- ✅ Trigger Agent
- ✅ Level 1 Pipeline Coordinator
- ✅ Level 2 Pipeline Coordinator
- ✅ Document Classifier Agent (with ML and adaptive learning)
- ✅ Prioritization Agent (with ML-based prioritization)
- ✅ Reflection Agent (with ML quality analysis)

### Enhanced Features

- ✅ Parallel processing for batch operations
- ✅ Comprehensive error handling and logging
- ✅ Performance monitoring and metrics
- ✅ Configurable agent parameters
- ✅ Caching for frequent operations
- ✅ Machine learning models for classification
- ✅ Adaptive learning from user feedback
- ✅ Sentiment analysis and contradiction detection
- ✅ Quality scoring with ML models
- ✅ Interactive feedback collection
- ✅ Clarifying questions for ambiguous classifications
- ✅ Continuous improvement engine
- ✅ LangGraph-based agents for contextual understanding
- ✅ Graph-based classification and prioritization
- ✅ Enhanced relationship detection

### Components to Implement

- ✅ Level 3 Agents and Pipeline
- ⬜ Enhanced modality processors with actual implementations
- ⬜ Integration with storage systems
- ⬜ API endpoints

## Usage

### Running the Level 1 Pipeline

```bash
cd /workspace/AI_BackLog_Assistant
PYTHONPATH=/workspace/AI_BackLog_Assistant/src python -m src.v2.main
```

### Running the Level 2 Pipeline

The Level 2 pipeline processes data from Level 1 through categorization, prioritization, and reflection agents with ML capabilities.

```python
from src.v2.pipelines.level2 import Level2Pipeline
from src.v2.ml.classification import DocumentClassifierModel
from src.v2.feedback.feedback_collector import FeedbackCollector
from src.v2.feedback.interactive_agent import InteractiveFeedbackAgent

# Initialize Level 2 pipeline with ML capabilities
level2_pipeline = Level2Pipeline(max_workers=8)

# Process data from Level 1
level1_data = {
    "document_id": "doc123",
    "content": "Sample document content",
    "metadata": {
        "source": "api",
        "modality": "text"
    }
}

# Process through Level 2 with monitoring
result = level2_pipeline.process_with_monitoring(level1_data)
print(result)

# Process batch of documents in parallel
batch_data = [
    {"document_id": "doc1", "content": "Content 1", "metadata": {"source": "email"}},
    {"document_id": "doc2", "content": "Content 2", "metadata": {"source": "api"}},
    {"document_id": "doc3", "content": "Content 3", "metadata": {"source": "web"}}
]

batch_results = level2_pipeline.process_batch(batch_data)
print(f"Processed {len(batch_results)} documents")

# Train and update ML models
classifier = DocumentClassifierModel()
classifier.train(
    documents=["Sample document 1", "Sample document 2"],
    labels=["urgent", "important"]
)
print("ML model trained")

# Use feedback system
feedback_collector = FeedbackCollector()
feedback_collector.collect_classification_feedback(
    document_id="doc123",
    user_category="urgent",
    original_category="important",
    confidence=0.7
)

# Use interactive feedback
interactive_agent = InteractiveFeedbackAgent()
question = interactive_agent.ask_clarifying_question(
    document_id="doc123",
    classification={"category": "important", "confidence": 0.5}
)
print(f"Clarifying question: {question['question']}")
```

### Running the Level 3 Pipeline

The Level 3 pipeline processes data from Level 2 through advanced analysis agents.

```python
from src.v3.pipelines.level3_pipeline import Level3Pipeline

# Initialize Level 3 pipeline
level3_pipeline = Level3Pipeline(max_workers=8)

# Example data from Level 2
level2_data = {
    "document_id": "doc123",
    "content": "Sample document content",
    "metadata": {
        "source": "api",
        "modality": "text"
    },
    "classification": {
        "category": "important",
        "domain": "system",
        "confidence": 0.8
    },
    "prioritization": {
        "priority_level": "high",
        "priority_score": 0.85
    },
    "reflection": {
        "quality_score": 0.75,
        "issues": ["Basic analysis completed"],
        "improvement_areas": ["Enhance with NLP models"]
    }
}

# Process through Level 3
result = level3_pipeline.process(level2_data)
print(result)

# Process batch of documents in parallel
batch_data = [
    {
        "document_id": f"doc{i}",
        "content": f"Content {i}",
        "metadata": {"source": "api"},
        "classification": {"category": "important", "confidence": 0.8},
        "prioritization": {"priority_level": "high", "priority_score": 0.85}
    }
    for i in range(5)
]

batch_results = level3_pipeline.process_batch(batch_data)
print(f"Processed {len(batch_results)} documents")
```

### Running the LangGraph Pipeline

The LangGraph pipeline processes data from Level 1 through graph-based agents.

```python
from src.v2.pipelines.langgraph_pipeline import LangGraphPipeline

# Initialize LangGraph pipeline
langgraph_pipeline = LangGraphPipeline(max_workers=8)

# Example data from Level 1
level1_data = {
    "document_id": "doc123",
    "content": "Sample document content",
    "metadata": {
        "source": "api",
        "modality": "text"
    }
}

# Process through LangGraph pipeline
result = langgraph_pipeline.process(level1_data)
print(result)

# Process batch of documents in parallel
batch_data = [
    {"document_id": f"doc{i}", "content": f"Content {i}", "metadata": {"source": "api"}}
    for i in range(5)
]

batch_results = langgraph_pipeline.process_batch(batch_data)
print(f"Processed {len(batch_results)} documents")
```

### Example Output

```
🚀 Starting AI Backlog Assistant v2.0

📦 Processing input 1/4
Input: I have an idea for a new feature: dark mode suppor...
✅ Processing successful!
   Modality: text
   Content Type: idea
   Emotion: neutral
   Initial Score: 0.65
   Trigger Level 2: False
```

## Development

### Adding New Agents

1. Create a new Python file in the appropriate directory
2. Implement the agent class with a clear interface
3. Add the agent to the pipeline coordinator if needed

### Running Tests

(TBD - Test framework to be implemented)

## Migration from v1

The v1 implementation has been preserved in the `src/v1/` directory. The new v2 implementation provides:

- Cleaner architecture
- Better separation of concerns
- More modular design
- Improved performance

Gradual migration is recommended to ensure compatibility.

## Future Plans

1. Complete Level 2 and Level 3 implementations
2. Enhance modality processors with actual implementations
3. Add proper storage integration
4. Implement comprehensive test suite
5. Add API endpoints and integrations

