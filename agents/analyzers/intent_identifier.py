from typing import Dict, List, Literal, Optional
from pydantic import BaseModel
from tools.llm_tool import LLMTool

class IntentAnalysis(BaseModel):
    """Analysis result for intent identification"""
    intent_type: Literal['вопрос', 'задача', 'наблюдение', 'опыт', 'вывод', 'размышление', 'кризис', 'неизвестно']
    confidence: float
    reasoning: str

class IntentIdentifier:
    """Identifies the intent or purpose behind input data using hybrid approach"""

    def __init__(self):
        # Define intent patterns and keywords for fast matching
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
                'keywords': ['думаю', 'размышляю', 'идея', 'гипотеза', 'теория', 'предположение', 'что если'],
                'patterns': ['что если', 'возможно', 'думаю что', 'а что если', 'что будет если']
            },
            'кризис': {
                'keywords': ['помогите', 'срочно', 'проблема', 'кризис', 'паника', 'катастрофа'],
                'patterns': ['помогите!', 'у нас кризис', 'все сроки горят', 'нужна помощь']
            }
        }
        # Initialize LLM tool for advanced intent detection
        self.llm = LLMTool()

    def identify(self, text: str) -> IntentAnalysis:
        """
        Identify the intent behind the input text using hybrid approach

        Args:
            text: Input text to analyze

        Returns:
            IntentAnalysis with identification results
        """
        # First try fast keyword/pattern matching
        keyword_result = self._identify_keywords(text)

        # If confidence is high enough, return keyword result
        if keyword_result.confidence > 0.6:
            return keyword_result

        # Otherwise, try LLM-based intent detection
        llm_result = self._identify_llm(text)

        # Return LLM result if available, otherwise fallback to keyword result
        return llm_result if llm_result else keyword_result

    def _identify_keywords(self, text: str) -> IntentAnalysis:
        """Identify intent using keyword and pattern matching"""
        scores = {}
        total_indicators = 0
        lower_text = text.lower()

        for intent, patterns in self.intent_patterns.items():
            score = 0
            score += sum(lower_text.count(keyword.lower()) for keyword in patterns['keywords'])
            score += sum(lower_text.count(pattern.lower()) for pattern in patterns['patterns'])
            scores[intent] = score
            total_indicators += score

        if total_indicators == 0:
            best_intent = 'неизвестно'
            confidence = 0.0
        else:
            best_intent = max(scores.items(), key=lambda x: x[1])[0]
            confidence = scores[best_intent] / total_indicators if total_indicators > 0 else 0.0

        reasoning = f"Анализ показал, что текст имеет признаки '{best_intent}'. "
        reasoning += f"Основные индикаторы: {', '.join([k for k, v in scores.items() if v > 0])}."

        return IntentAnalysis(
            intent_type=best_intent,
            confidence=confidence,
            reasoning=reasoning
        )

    def _identify_llm(self, text: str) -> Optional[IntentAnalysis]:
        """Identify intent using LLM model"""
        try:
            prompt = f"""
Ты — классификатор намерений. Прочитай следующий запрос пользователя и определи его предполагаемое действие.
Запрос: "{text}"
Выбери одно из: ["вопрос", "задача", "наблюдение", "опыт", "вывод", "размышление", "кризис", "неизвестно"]
Ответ должен содержать только одно слово без пояснений.
"""

            intent = self.llm.call_intent_model(prompt)
            if not intent:
                return None

            intent = intent.strip().lower()

            # Validate that intent is one of our expected types
            if intent not in self.intent_patterns and intent != 'неизвестно':
                intent = 'неизвестно'

            return IntentAnalysis(
                intent_type=intent,
                confidence=0.9,  # High confidence for LLM results
                reasoning=f"LLM-анализ определил намерение как '{intent}'."
            )
        except Exception as e:
            print(f"[WARNING] LLM intent identification failed: {e}")
            return None
