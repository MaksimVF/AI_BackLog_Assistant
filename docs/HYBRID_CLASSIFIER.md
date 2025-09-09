




# Hybrid Content Classifier for AI Backlog Assistant

## Overview

The Hybrid Content Classifier is an enhanced version of the Content Classifier Agent that provides more detailed categorization for IT, marketing, and freelance domains. It uses a hybrid approach that combines rule-based classification with LLM fallback for complex cases.

## Key Features

1. **Enhanced Content Types**: More granular classification for IT, marketing, and freelance content
2. **Domain Classification**: Identifies the subject area (software development, digital marketing, etc.)
3. **Emotion Analysis**: Detects multiple emotions including urgency and confusion
4. **Hybrid Approach**: Uses rules first, falls back to LLM for complex cases
5. **Improved Scoring**: Better prioritization based on content type and emotion

## Content Types

The hybrid classifier supports the following content types:

- `feature_request` - Requests for new functionality
- `bug_report` - Bug reports and technical issues
- `user_feedback` - General user feedback
- `technical_question` - Technical support questions
- `marketing_idea` - Marketing campaign ideas
- `content_request` - Requests for content creation
- `project_management` - Project management questions
- `billing_question` - Billing and payment inquiries
- `general_inquiry` - General questions

## Domains

The classifier identifies the following domains:

- `software_development` - Software and coding related
- `digital_marketing` - Marketing and advertising
- `content_creation` - Content production
- `project_management` - Project coordination
- `customer_support` - Customer service
- `sales` - Sales related
- `finance` - Financial topics
- `general` - General topics

## Emotions

The classifier detects multiple emotions:

- `positive` - Positive sentiment
- `negative` - Negative sentiment
- `urgent` - Urgent requests
- `confused` - Confused or unclear requests
- `neutral` - Neutral sentiment

## Integration

The hybrid classifier can be used as a drop-in replacement for the standard ContentClassifierAgent:

```python
from src.v2.agents.level1.content_classifier_hybrid import HybridContentClassifierAgent

classifier = HybridContentClassifierAgent()
result = classifier.classify({
    'content': 'Your text here',
    'metadata': {}
})

print(result['metadata']['content_type'])
print(result['metadata']['domain'])
print(result['metadata']['emotions'])
```

## Configuration

The classifier can be configured to disable LLM fallback:

```python
classifier = HybridContentClassifierAgent(use_llm_fallback=False)
```

## Scoring

The classifier calculates an initial score based on:
- Content type importance (feature requests and bugs have higher priority)
- Emotion score (urgent and positive emotions increase score)
- Domain relevance

## Benefits

1. **Better Categorization**: More specific categories for IT and marketing
2. **Improved Prioritization**: Better scoring for urgent and important items
3. **Cost Efficiency**: Uses rules first, LLM only when needed
4. **Extensibility**: Easy to add new patterns and categories

## Use Cases

- IT support ticket classification
- Marketing campaign idea triage
- Feature request prioritization
- Content creation workflows
- Customer support automation

## Performance

The hybrid classifier provides better accuracy than the basic classifier while maintaining low computational cost by using LLM only when necessary.

## Future Enhancements

- Add more domain-specific patterns
- Improve emotion detection with sentiment analysis
- Add intent detection for better categorization
- Implement learning from user feedback

