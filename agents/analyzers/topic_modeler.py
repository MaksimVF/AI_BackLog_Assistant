







from typing import List, Dict, Optional
from pydantic import BaseModel
import logging
import numpy as np
from collections import defaultdict

logger = logging.getLogger(__name__)

class TopicAnalysis(BaseModel):
    """Topic modeling results"""
    topics: List[str]  # List of detected topics
    topic_distribution: Dict[str, float]  # Topic distribution
    subtopics: Optional[Dict[str, List[str]]] = None  # Subtopics for each main topic
    keywords: Optional[Dict[str, List[str]]] = None  # Key keywords for each topic

class TopicModeler:
    """Performs advanced topic modeling on text input using LDA-like approach"""

    def __init__(self):
        # Enhanced topic hierarchy with subtopics and related keywords
        self.topic_hierarchy = {
            'work': {
                'subtopics': ['project_management', 'career_development', 'team_collaboration', 'work_life_balance'],
                'keywords': {
                    'project_management': ['проект', 'дедлайн', 'план', 'задача', 'менеджмент'],
                    'career_development': ['карьера', 'продвижение', 'навыки', 'обучение', 'развитие'],
                    'team_collaboration': ['команда', 'коллега', 'сотрудничество', 'взаимодействие', 'коммуникация'],
                    'work_life_balance': ['баланс', 'стресс', 'усталость', 'отдых', 'перегрузка']
                }
            },
            'personal': {
                'subtopics': ['family', 'relationships', 'self_improvement', 'hobbies'],
                'keywords': {
                    'family': ['семья', 'дети', 'родители', 'дом', 'близкие'],
                    'relationships': ['отношения', 'друг', 'партнер', 'любовь', 'связь'],
                    'self_improvement': ['саморазвитие', 'личностный рост', 'цели', 'мотивация', 'успех'],
                    'hobbies': ['хобби', 'интересы', 'увлечения', 'свободное время', 'отдых']
                }
            },
            'finance': {
                'subtopics': ['budgeting', 'investing', 'saving', 'debt_management'],
                'keywords': {
                    'budgeting': ['бюджет', 'финансы', 'расходы', 'доходы', 'планирование'],
                    'investing': ['инвестиции', 'акции', 'фонды', 'риск', 'прибыль'],
                    'saving': ['сбережения', 'накопления', 'экономия', 'цели', 'план'],
                    'debt_management': ['долг', 'кредит', 'погашение', 'проценты', 'управление']
                }
            },
            'health': {
                'subtopics': ['mental_health', 'physical_fitness', 'nutrition', 'sleep'],
                'keywords': {
                    'mental_health': ['стресс', 'тревога', 'депрессия', 'медитация', 'психология'],
                    'physical_fitness': ['упражнения', 'спорт', 'тренировка', 'фитнес', 'здоровье'],
                    'nutrition': ['питание', 'диета', 'еда', 'витамины', 'здоровье'],
                    'sleep': ['сон', 'отдых', 'бессонница', 'режим', 'усталость']
                }
            },
            'technology': {
                'subtopics': ['software_development', 'hardware', 'ai_ml', 'cybersecurity'],
                'keywords': {
                    'software_development': ['программирование', 'софт', 'код', 'разработка', 'алгоритм'],
                    'hardware': ['железо', 'компьютер', 'сервер', 'оборудование', 'техника'],
                    'ai_ml': ['ии', 'машинное обучение', 'нейросети', 'данные', 'модель'],
                    'cybersecurity': ['безопасность', 'хакеры', 'защита', 'шифрование', 'уязвимость']
                }
            }
        }

        # General topic for fallback
        self.general_keywords = ['информация', 'данные', 'знания', 'советы', 'идеи', 'мысли']

    def analyze_topics(self, text: str) -> TopicAnalysis:
        """
        Analyze topics in the given text using advanced topic modeling

        Args:
            text: Input text to analyze

        Returns:
            TopicAnalysis: Analysis results
        """
        # Preprocess text
        words = self._preprocess_text(text)

        # Calculate topic scores using hierarchical approach
        topic_scores = defaultdict(float)
        subtopic_scores = defaultdict(lambda: defaultdict(float))
        keyword_matches = defaultdict(lambda: defaultdict(list))

        # Analyze each topic and subtopic
        for main_topic, topic_data in self.topic_hierarchy.items():
            for subtopic, keywords in topic_data['keywords'].items():
                matches = [word for word in words if word in keywords]
                match_count = len(matches)

                if match_count > 0:
                    # Score for main topic
                    topic_scores[main_topic] += match_count

                    # Score for subtopic
                    subtopic_scores[main_topic][subtopic] = match_count

                    # Store keyword matches
                    keyword_matches[main_topic][subtopic] = matches

        # Normalize scores
        total_score = sum(topic_scores.values())

        if total_score == 0:
            # Check for general keywords
            general_matches = [word for word in words if word in self.general_keywords]
            if general_matches:
                return TopicAnalysis(
                    topics=['general'],
                    topic_distribution={'general': 1.0},
                    subtopics={'general': ['information']},
                    keywords={'general': general_matches}
                )
            else:
                return TopicAnalysis(
                    topics=['general'],
                    topic_distribution={'general': 1.0}
                )

        # Calculate topic distribution
        topic_distribution = {topic: score / total_score for topic, score in topic_scores.items()}

        # Get top topics (minimum 15% threshold)
        sorted_topics = sorted(topic_distribution.items(), key=lambda x: x[1], reverse=True)
        top_topics = [topic for topic, score in sorted_topics if score > 0.15]

        if not top_topics:
            top_topics = ['general']

        # Prepare subtopics and keywords for top topics
        result_subtopics = {}
        result_keywords = {}

        for topic in top_topics:
            if topic in subtopic_scores:
                # Get top subtopics for this main topic
                subtopic_dist = subtopic_scores[topic]
                total_subtopic_score = sum(subtopic_dist.values())

                if total_subtopic_score > 0:
                    subtopic_dist_normalized = {
                        sub: score / total_subtopic_score
                        for sub, score in subtopic_dist.items()
                        if score / total_subtopic_score > 0.1  # Minimum 10% threshold
                    }

                    if subtopic_dist_normalized:
                        result_subtopics[topic] = list(subtopic_dist_normalized.keys())
                        result_keywords[topic] = [kw for subtopic_kws in keyword_matches[topic].values() for kw in subtopic_kws]

        logger.debug(f"Advanced topic analysis: {top_topics} for text: {text[:50]}...")

        return TopicAnalysis(
            topics=top_topics,
            topic_distribution=topic_distribution,
            subtopics=result_subtopics if result_subtopics else None,
            keywords=dict(result_keywords) if result_keywords else None
        )

    def _preprocess_text(self, text: str) -> List[str]:
        """Preprocess text for analysis"""
        # Convert to lowercase and split into words
        words = text.lower().split()

        # Remove punctuation and special characters
        words = [word.strip('.,!?;:()[]{}"\'') for word in words]

        # Remove empty strings and common stop words
        stop_words = {'и', 'в', 'на', 'с', 'по', 'за', 'от', 'до', 'при', 'из', 'о', 'об', 'обо'}
        words = [word for word in words if word and word not in stop_words]

        return words







