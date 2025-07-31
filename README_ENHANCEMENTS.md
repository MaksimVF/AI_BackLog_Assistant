

# AI Backlog Assistant - Enhancements

## Overview

This document outlines the significant enhancements made to the AI Backlog Assistant's context classification and intent identification capabilities.

## Table of Contents

1. [Enhanced Context Classifier](#enhanced-context-classifier)
2. [Improved Intent Identifier](#improved-intent-identifier)
3. [New Tools and Utilities](#new-tools-and-utilities)
4. [Testing and Validation](#testing-and-validation)
5. [Integration Guide](#integration-guide)

## Enhanced Context Classifier

### Key Improvements

1. **Semantic Similarity Approach**: Added semantic embedding-based classification that compares user input with historical data using cosine similarity.

2. **Hybrid Classification**: Combines semantic similarity with keyword-based fallback for robustness.

3. **Expanded Context Categories**: Added new context types including:
   - финансовый (financial)
   - юридический (legal)
   - бытовой (household)

4. **Improved Keyword Matching**: Enhanced keyword lists for better accuracy in fallback mode.

### Technical Implementation

- **Primary Method**: Uses `embed_text()` and `cosine_similarity()` for semantic comparison
- **Fallback Method**: Enhanced keyword matching with comprehensive keyword lists
- **Threshold**: 0.75 similarity score required for semantic match
- **Integration**: Works with existing `SemanticEmbedder` and `WeaviateTool`

### Benefits

- **Higher Accuracy**: Semantic understanding vs simple keyword matching
- **Adaptive Learning**: Improves over time as history grows
- **Robustness**: Falls back to keyword matching when semantic approach fails
- **Better Context Detection**: More nuanced understanding of user intent

## Improved Intent Identifier

### Key Improvements

1. **Hybrid Approach**: Combines fast keyword/pattern matching with LLM-based intent detection.

2. **Enhanced Patterns**: Improved keyword and pattern lists for better accuracy.

3. **LLM Integration**: Uses LLM for cases where keyword confidence is low.

4. **Comprehensive Intent Types**: Supports 8 different intent categories.

### Technical Implementation

- **Fast Path**: Keyword/pattern matching with confidence threshold (0.6)
- **Slow Path**: LLM-based intent detection for ambiguous cases
- **Fallback**: Returns to keyword result if LLM fails
- **Validation**: Ensures LLM results match expected intent types

### Benefits

- **Speed**: Fast response for clear cases
- **Accuracy**: LLM handles complex/ambiguous language
- **Reliability**: Fallback ensures always available
- **Flexibility**: Can adapt to new intent types via LLM

## New Tools and Utilities

### 1. Similarity Tool (`tools/similarity.py`)

- **Function**: `cosine_similarity(vec1, vec2)`
- **Purpose**: Calculate cosine similarity between two vectors
- **Usage**: Used by context classifier for semantic comparison

### 2. LLM Tool (`tools/llm_tool.py`)

- **Class**: `LLMTool`
- **Methods**:
  - `call_model(prompt)`: General LLM interface
  - `call_intent_model(prompt)`: Specialized for intent classification
- **Purpose**: Provides LLM capabilities for intent identification

### 3. Metadata Builder (`agents/analyzers/metadata_builder.py`)

- **Class**: `MetadataBuilder`
- **Methods**:
  - `build_metadata(user_input)`: Generates comprehensive metadata
  - `build_metadata_for_storage(user_input)`: Formats metadata for storage systems
- **Purpose**: Centralized metadata generation for all input data
- **Features**:
  - Basic metadata (ID, timestamp, source, etc.)
  - Language detection
  - Context classification
  - Intent identification
  - Domain inference
  - Confidence scoring
  - Format detection

### 5. Text Cleaner (`agents/analyzers/text_cleaner.py`)

- **Class**: `TextCleaner`
- **Methods**:
  - `clean(text)`: Clean and normalize text with metadata
  - `clean_list(texts)`: Apply cleaning to list of texts
  - `tokenize(text)`: Basic tokenization
  - `normalize_for_language(text, target_language)`: Language-specific normalization
  - `log_processing_trace(input_text, result)`: Generate processing trace
- **Purpose**: Enhanced text cleaning with language detection and trace logging
- **Features**:
  - Configurable cleaning options
  - Language detection
  - Multi-language support
  - Trace logging
  - Extensible for tokenization and lemmatization

### 4. Semantic Router (`agents/analyzers/semantic_router.py`)

- **Class**: `SemanticRouter`
- **Methods**:
  - `route(user_input)`: Comprehensive semantic routing
  - `route_with_fallback(user_input)`: Routing with fallback
- **Purpose**: Advanced routing based on source type and content analysis
- **Features**:
  - Source-based routing (video, audio, text)
  - Content-based routing (context, intent)
  - Priority determination
  - Comprehensive reasoning

### Text Cleaner Tests

1. **Basic Test** (`test_text_cleaner.py`):
   - Tests basic text cleaning
   - Tests custom configuration
   - Tests list processing
   - Tests tokenization
   - Tests processing trace logging
  - Fallback mechanism

## Testing and Validation

### Context Classifier Tests

1. **Basic Test** (`test_context_classifier.py`):
   - Tests keyword-based classification
   - Validates all context types
   - Measures confidence scores

2. **Mock Test** (`test_context_classifier_with_mock.py`):
   - Tests semantic similarity with mocked embeddings
   - Validates fallback behavior
   - Measures semantic matching accuracy

### Intent Identifier Tests

### Semantic Router Tests

1. **Basic Test** (`test_semantic_router.py`):
   - Tests source-based routing
   - Tests content-based routing
   - Tests priority determination
   - Tests fallback mechanism

1. **Basic Test** (`test_intent_identifier.py`):
   - Tests keyword/pattern matching
   - Validates all intent types
   - Measures confidence scores
   - Tests LLM fallback behavior

### Metadata Builder Tests

1. **Basic Test** (`test_metadata_builder.py`):
   - Tests comprehensive metadata generation
   - Validates integration with context classifier and intent identifier
   - Tests storage format compatibility
   - Validates language detection

## Integration Guide

### Context Classifier Usage

```python
from agents.analyzers.context_classifier import ContextClassifier

### Text Cleaner Usage

```python
from agents.analyzers.text_cleaner import TextCleaner

cleaner = TextCleaner()

- **Text Cleaner**: Configurable performance, language detection adds minimal overhead

# Basic cleaning
result = cleaner.clean("  Пример текста!  ")
print(result["cleaned"])  # "пример текста!"
print(result["language"])  # "ru"

# Custom configuration
custom_cleaner = TextCleaner({
    "lowercase": False,
    "preserve_punctuation": [".", ",", "!", "?"]
})
result = custom_cleaner.clean("Keep THIS! Text, please.")

# List processing
results = cleaner.clean_list(["text1", "text2"])


4. **Text Cleaner**:
   - Add NLP-based tokenization (spaCy, NLTK)
   - Implement lemmatization
   - Add domain-specific normalization rules
   - Integrate with external language services
# With trace logging
result = cleaner.clean("Important text", log_trace=True)
```

classifier = ContextClassifier()

# Basic usage (keyword-based)
result = classifier.classify("Как приготовить ужин?")
print(result.context)  # "бытовой"
print(result.confidence)  # 1.0

# Advanced usage (with history)
history = [
    {"text": "Проблемы с кредитом", "context": "финансовый", "embedding": [0.1, 0.2, 0.3]},
    {"text": "Приготовить ужин", "context": "бытовой", "embedding": [0.4, 0.5, 0.6]}
]
result = classifier.classify("Как приготовить обед?", history=history)
```

### Intent Identifier Usage

```python
from agents.analyzers.intent_identifier import IntentIdentifier

identifier = IntentIdentifier()
result = identifier.identify("Как работает эта система?")
print(result.intent_type)  # "вопрос"
print(result.confidence)  # 1.0
```

### Semantic Router Usage

```python
from agents.analyzers.semantic_router import SemanticRouter

router = SemanticRouter()

- **Semantic Router**: Combines multiple analysis methods, fallback ensures reliability

# Basic routing
user_input = {
    "user_id": "user123",
    "text": "Как работает эта система?",
    "source": "web"
}
result = router.route(user_input)
print(result["agents"])  # ["text_cleaner", "general_qa_agent"]
print(result["reasoning"])
print(result["priority"])

# Routing with fallback
result = router.route_with_fallback(user_input)
```


3. **Semantic Router**:
   - Add LLM-based dynamic routing
   - Implement continuous learning from routing outcomes
   - Add real-time performance monitoring
   - Integrate with external service registries
### Metadata Builder Usage

```python
from agents.analyzers.metadata_builder import MetadataBuilder

builder = MetadataBuilder()

# Basic metadata generation
user_input = {
    "user_id": "user123",
    "text": "Как работает эта система?",
    "source": "web"
}
metadata = builder.build_metadata(user_input)
print(metadata["context"])  # "профессиональный"
print(metadata["intent"])   # "вопрос"
print(metadata["language"]) # "ru"

# Metadata for storage (Weaviate format)
storage_data = builder.build_metadata_for_storage(user_input)
# Can be directly used with WeaviateTool.add_document_chunk()
```

## Performance Considerations

- **Context Classifier**: Semantic approach requires embedding service (local or remote)
- **Intent Identifier**: LLM calls only made when confidence < 0.6 (optimized usage)
- **Metadata Builder**: Integrates both classifiers, language detection adds minimal overhead
- **Fallback**: All systems gracefully degrade to keyword matching when services unavailable

## Future Enhancements

1. **Context Classifier**:
   - Add more context categories
   - Implement continuous learning from user feedback
   - Optimize embedding caching

2. **Intent Identifier**:
   - Expand intent types
   - Implement intent-specific confidence thresholds
   - Add multilingual support


3. **Metadata Builder**:
   - Add geolocation detection
   - Implement source trust scoring
   - Add content format detection (list, dialog, etc.)
   - Integrate with external knowledge bases for domain enrichment
3. **Infrastructure**:
   - Add local embedding service
   - Implement LLM service
   - Add monitoring for service availability

## Conclusion

These enhancements significantly improve the AI Backlog Assistant's ability to understand user context and intent, leading to better routing, more accurate responses, and an overall improved user experience.

## Domain-Specific Categorization Enhancements

### Overview
We have significantly enhanced the SecondLevelCategorizationAgent by adding domain-specific categorizers for various industries and use cases. This expansion allows the system to better handle documents from different domains with more accurate and relevant categorization.

### New Domain-Specific Categorizers

#### 1. LegalCategorizer
**Purpose**: Classifies legal documents and requests
**Categories**:
- contract: Юридический договор или соглашение
- court_decision: Решение суда или арбитража
- legal_opinion: Юридическое заключение или мнение
- complaint: Жалоба или исковое заявление
- regulation: Нормативный акт или постановление
- legal_consultation: Запрос на юридическую консультацию

#### 2. HealthcareCategorizer
**Purpose**: Classifies medical and healthcare documents
**Categories**:
- medical_record: Медицинская карта или история болезни
- prescription: Рецепт на лекарства
- diagnostic_report: Результаты диагностики или анализа
- treatment_plan: План лечения или реабилитации
- patient_complaint: Жалоба пациента на лечение или обслуживание
- research_paper: Научная статья или исследование в медицине

#### 3. PersonalGrowthCategorizer
**Purpose**: Classifies personal development and self-improvement documents
**Categories**:
- goal_setting: Постановка личных или профессиональных целей
- self_reflection: Рефлексия или анализ личного опыта
- learning_plan: План обучения или саморазвития
- motivation: Мотивационные заметки или цитаты
- habit_tracking: Отслеживание привычек или рутины
- personal_challenge: Личный вызов или испытание

#### 4. CustomerSupportCategorizer
**Purpose**: Classifies customer support tickets and requests
**Categories**:
- technical_issue: Техническая проблема или ошибка
- billing_question: Вопрос по оплате или счету
- feature_request: Запрос на новую функцию или улучшение
- complaint: Жалоба на продукт или сервис
- general_question: Общий вопрос о продукте или услуге
- account_issue: Проблема с аккаунтом или доступом

#### 5. ProjectManagementCategorizer
**Purpose**: Classifies project management documents
**Categories**:
- project_plan: План проекта или дорожная карта
- task_list: Список задач или чеклист
- meeting_notes: Заметки или протокол встречи
- risk_assessment: Оценка рисков или проблем
- progress_report: Отчёт о прогрессе или статусе
- resource_allocation: Распределение ресурсов или бюджета

### Implementation Details

- Each domain categorizer follows the same pattern as the existing IT and Finance categorizers
- Uses embedding-based similarity matching for categorization
- Each categorizer has its own taxonomy file in JSON format
- Domain router automatically selects the appropriate categorizer based on the detected domain

### Benefits

1. **Improved Accuracy**: Domain-specific categorization provides more relevant results than generic classification
2. **Extensibility**: Easy to add new domains by following the established pattern
3. **Better User Experience**: Users from different industries get more meaningful categorization
4. **Enhanced Automation**: More precise categorization enables better downstream processing and routing

### Usage Example

```python
from agents.categorization.second_level_categorization_agent import SecondLevelCategorizationAgent

agent = SecondLevelCategorizationAgent()

# Example legal document
legal_doc = "Договор аренды №789 от 2025-02-20. Арендодатель: ООО 'Недвижимость Плюс'"
result = agent.categorize(legal_doc, "legal")
print(result)
# Output: {'category': 'contract', 'confidence': 0.785, 'source': 'legal', 'domain': 'legal'}
```

