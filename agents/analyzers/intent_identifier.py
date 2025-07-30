




from typing import Dict, List, Literal
from pydantic import BaseModel

class IntentAnalysis(BaseModel):
    """Analysis result for intent identification"""
    intent_type: Literal['вопрос', 'задача', 'наблюдение', 'опыт', 'вывод', 'размышление', 'кризис', 'неизвестно']
    confidence: float
    reasoning: str

class IntentIdentifier:
    """Identifies the intent or purpose behind input data"""

    def __init__(self):
        # Define intent patterns and keywords
        self.intent_patterns = {
            'вопрос': {
                'keywords': ['как', 'что', 'почему', 'где', 'когда', 'кто', 'какой', 'сколько', '?'],
                'patterns': ['можете помочь', 'подскажите', 'объясните']
            },
            'задача': {
                'keywords': ['нужно', 'требуется', 'сделать', 'решить', 'задача', 'цель', 'план'],
                'patterns': ['помогите с', 'как сделать', 'какие шаги']
            },
            'наблюдение': {
                'keywords': ['вижу', 'заметил', 'интересно', 'факты', 'данные', 'результаты'],
                'patterns': ['я заметил', 'интересный факт', 'по моим наблюдениям']
            },
            'опыт': {
                'keywords': ['опыт', 'случилось', 'произошло', 'ситуация', 'история', 'пример'],
                'patterns': ['со мной случилось', 'в моей практике', 'пример из жизни']
            },
            'вывод': {
                'keywords': ['поэтому', 'следовательно', 'вывод', 'результат', 'итог', 'конклюзия'],
                'patterns': ['из этого следует', 'в итоге', 'мои выводы']
            },
            'размышление': {
                'keywords': ['думаю', 'размышляю', 'идея', 'гипотеза', 'теория', 'предположение'],
                'patterns': ['что если', 'возможно', 'думаю что']
            },
            'кризис': {
                'keywords': ['помогите', 'срочно', 'проблема', 'кризис', 'паника', 'катастрофа'],
                'patterns': ['помогите!', 'у нас кризис', 'все сроки горят', 'нужна помощь']
            }
        }

    def identify(self, text: str) -> IntentAnalysis:
        """
        Identify the intent behind the input text

        Args:
            text: Input text to analyze

        Returns:
            IntentAnalysis with identification results
        """
        # Calculate scores for each intent
        scores = {}
        total_indicators = 0

        # Convert text to lowercase for case-insensitive matching
        lower_text = text.lower()

        for intent, patterns in self.intent_patterns.items():
            score = 0

            # Check keywords
            score += sum(lower_text.count(keyword.lower()) for keyword in patterns['keywords'])

            # Check patterns
            score += sum(lower_text.count(pattern.lower()) for pattern in patterns['patterns'])

            scores[intent] = score
            total_indicators += score

        # Determine best intent
        if total_indicators == 0:
            best_intent = 'неизвестно'
            confidence = 0.0
        else:
            best_intent = max(scores.items(), key=lambda x: x[1])[0]
            confidence = scores[best_intent] / total_indicators if total_indicators > 0 else 0.0

        # Generate reasoning
        reasoning = f"Анализ показал, что текст имеет признаки '{best_intent}'. "
        reasoning += f"Основные индикаторы: {', '.join([k for k, v in scores.items() if v > 0])}."

        return IntentAnalysis(
            intent_type=best_intent,
            confidence=confidence,
            reasoning=reasoning
        )





