



from typing import Dict, List, Literal, Optional
from pydantic import BaseModel
from tools.semantic_embedder import SemanticEmbedder
from tools.similarity import cosine_similarity
from tools.weaviate_tool import WeaviateTool

class ContextAnalysis(BaseModel):
    """Analysis result for context classification"""
    context: Literal['личный', 'профессиональный', 'кризисный', 'общий', 'неизвестно', 'финансовый', 'юридический', 'бытовой']
    confidence: float
    reasoning: str

class ContextClassifier:
    """Classifies the context of input data using semantic similarity"""

    def __init__(self):
        self.embedder = SemanticEmbedder()
        self.weaviate = WeaviateTool()
        # Fallback keyword-based approach for when semantic approach isn't available
        self.context_keywords = {
            'личный': [
                'семья', 'отношения', 'эмоции', 'саморазвитие', 'хобби', 'здоровье',
                'чувствую', 'настроение', 'личная жизнь', 'самопознание', 'медитация',
                'улучшение', 'благосостояние', 'психология', 'внутренний', 'душевный',
                'заняться', 'практика', 'осознанность', 'релаксация', 'духовный'
            ],
            'профессиональный': [
                'работа', 'карьера', 'бизнес', 'проект', 'команда', 'дедлайн',
                'стартап', 'маркетинг', 'стратегия', 'финансы', 'компания', 'менеджмент',
                'коллеги', 'офис', 'корпоративный', 'производительность'
            ],
            'кризисный': [
                'проблема', 'кризис', 'стресс', 'конфликт', 'срочно', 'помощь',
                'помогите', 'сроки горят', 'катастрофа', 'паника', 'эмоциональный',
                'плохо', 'трудности', 'сложности', 'проблемный', 'критический'
            ],
            'финансовый': [
                'деньги', 'инвестиции', 'бюджет', 'кредит', 'налоги', 'банк',
                'финансы', 'доход', 'расход', 'счет', 'платеж', 'кредитный',
                'финансовый', 'экономика', 'бухгалтерия', 'аудит'
            ],
            'юридический': [
                'закон', 'договор', 'контракт', 'суд', 'адвокат', 'право',
                'юридический', 'нормативный', 'регулирование', 'лицензия',
                'аренда', 'соглашение', 'правовой', 'юриспруденция'
            ],
            'бытовой': [
                'дом', 'ремонт', 'уборка', 'покупки', 'еда', 'приготовление',
                'чистка', 'организация', 'планирование', 'повседневный',
                'кухня', 'ужин', 'обед', 'завтрак', 'продукты', 'быт',
                'домашний', 'семейный', 'повседневность'
            ],
            'общий': [
                'информация', 'вопрос', 'совет', 'идея', 'план', 'факт',
                'интересный', 'статистика', 'исследование', 'данные', 'знания',
                'космос', 'наука', 'технология', 'образование', 'культура'
            ]
        }

    def classify(self, text: str, history: Optional[List[Dict]] = None) -> ContextAnalysis:
        """
        Classify the context of the input text using semantic similarity with history.

        Args:
            text: Input text to classify
            history: Optional list of historical interactions for semantic comparison

        Returns:
            ContextAnalysis with classification results
        """
        # Try semantic approach first
        semantic_result = self._classify_semantic(text, history)
        if semantic_result:
            return semantic_result

        # Fall back to keyword-based approach
        return self._classify_keywords(text)

    def _classify_semantic(self, text: str, history: Optional[List[Dict]]) -> Optional[ContextAnalysis]:
        """Classify using semantic similarity with historical data"""
        if not history:
            return None

        try:
            input_embedding = self.embedder.embed(text)
            if not input_embedding:
                return None

            similarities = []
            for entry in history:
                if "embedding" not in entry:
                    continue

                hist_embedding = entry["embedding"]
                score = cosine_similarity(input_embedding, hist_embedding)
                similarities.append((score, entry.get("context", "общий")))

            # Determine most similar context
            if similarities:
                similarities.sort(reverse=True)
                top_score, top_context = similarities[0]
                if top_score > 0.75:  # High similarity threshold
                    return ContextAnalysis(
                        context=top_context,
                        confidence=top_score,
                        reasoning=f"Семантический анализ показал высокое сходство ({top_score:.2f}) с предыдущим контекстом '{top_context}'."
                    )
        except Exception as e:
            print(f"[WARNING] Semantic classification failed: {e}")

        return None

    def _classify_keywords(self, text: str) -> ContextAnalysis:
        """Fallback keyword-based classification"""
        scores = {}
        total_keywords = 0

        for context, keywords in self.context_keywords.items():
            score = sum(text.lower().count(keyword.lower()) for keyword in keywords)
            scores[context] = score
            total_keywords += score

        # Determine best context
        if total_keywords == 0:
            best_context = 'неизвестно'
            confidence = 0.0
        else:
            best_context = max(scores.items(), key=lambda x: x[1])[0]
            confidence = scores[best_context] / total_keywords if total_keywords > 0 else 0.0

        # Generate reasoning
        reasoning = f"Анализ показал, что текст содержит ключевые слова, относящиеся к '{best_context}' контексту. "
        reasoning += f"Основные индикаторы: {', '.join([k for k, v in scores.items() if v > 0])}."

        return ContextAnalysis(
            context=best_context,
            confidence=confidence,
            reasoning=reasoning
        )



