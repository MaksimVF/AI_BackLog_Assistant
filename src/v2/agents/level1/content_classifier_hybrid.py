


"""
Hybrid Content Classifier Agent for Level 1 Processing
Uses rule-based classification with LLM fallback for complex cases
"""

import logging
import re
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

class HybridContentClassifierAgent:
    """Classifies content using hybrid approach: rules + LLM fallback"""

    def __init__(self, use_llm_fallback: bool = True):
        # Enhanced content type patterns
        self.content_patterns = {
            'feature_request': [
                r'feature(s)? request(s)?',
                r'new feature(s)?',
                r'add (functionality|capability)',
                r'implement',
                r'would like to see',
                r'it would be great if'
            ],
            'bug_report': [
                r'bug(s)?',
                r'error(s)?',
                r'issue(s)?',
                r'problem(s)?',
                r'crash(es)?',
                r'not working',
                r'broken',
                r'defect',
                r'glitch'
            ],
            'user_feedback': [
                r'feedback',
                r'comment(s)?',
                r'review(s)?',
                r'opinion(s)?',
                r'thought(s)?',
                r'suggestion(s)?',
                r'improvement(s)?'
            ],
            'technical_question': [
                r'question(s)?',
                r'query|queries',
                r'asking',
                r'need help',
                r'how to',
                r'what is',
                r'why does',
                r'technical support',
                r'troubleshoot',
                r'configure',
                r'set up',
                r'install',
                r'integration',
                r'api',
                r'authentication',
                r'permission',
                r'error message',
                r'debug',
                r'code example',
                r'syntax',
                r'library',
                r'framework',
                r'compatibility',
                r'version',
                r'update',
                r'upgrade',
                r'migration',
                r'deployment',
                r'hosting',
                r'server',
                r'database',
                r'network',
                r'security',
                r'performance'
            ],
            'marketing_idea': [
                r'marketing idea(s)?',
                r'promotion(s)?',
                r'campaign idea(s)?',
                r'advertising suggestion(s)?',
                r'SEO suggestion(s)?',
                r'social media idea(s)?',
                r'social media campaign',
                r'brand awareness',
                r'targeting young professionals',
                r'run a campaign',
                r'marketing strategy',
                r'marketing plan',
                r'boost our brand',
                r'increase visibility',
                r'customer acquisition',
                r'lead generation',
                r'content marketing idea',
                r'email marketing campaign',
                r'influencer marketing',
                r'viral marketing'
            ],
            'content_request': [
                r'content request(s)?',
                r'need (article|blog post|video)',
                r'create content',
                r'write about',
                r'content idea(s)?',
                r'write a blog post',
                r'create an article',
                r'produce a video',
                r'design an infographic',
                r'write content about',
                r'content creation',
                r'content production',
                r'content writing',
                r'content design',
                r'content for',
                r'content on',
                r'content about',
                r'blog post about',
                r'article about',
                r'video about',
                r'content needed',
                r'content required'
            ],
            'project_management': [
                r'project management',
                r'task management',
                r'deadline(s)?',
                r'project status',
                r'team coordination',
                r'agile',
                r'scrum',
                r'kanban'
            ],
            'billing_question': [
                r'billing',
                r'invoice(s)?',
                r'payment(s)?',
                r'pricing',
                r'subscription',
                r'refund',
                r'charge',
                r'billing question',
                r'invoice question',
                r'payment question',
                r'pricing question',
                r'subscription question',
                r'billing issue',
                r'invoice issue',
                r'payment issue',
                r'billing problem',
                r'invoice problem',
                r'payment problem',
                r'question about my invoice',
                r'question about my payment',
                r'question about my subscription',
                r'question about pricing',
                r'question about billing',
                r'question about charges',
                r'billing inquiry',
                r'payment inquiry',
                r'invoice inquiry',
                r'billing support',
                r'payment support',
                r'invoice support',
                r'billing help',
                r'payment help',
                r'invoice help'
            ],
            'general_inquiry': [
                r'general question(s)?',
                r'info',
                r'information',
                r'details',
                r'can you tell me',
                r'what do you know about'
            ]
        }

        # Enhanced emotion patterns
        self.emotion_patterns = {
            'positive': [
                r'good',
                r'great',
                r'excellent',
                r'happy',
                r'love',
                r'awesome',
                r'perfect',
                r'thank(s)?',
                r'wonderful',
                r'fantastic',
                r'helpful',
                r'useful',
                r'beneficial',
                r'valuable',
                r'important',
                r'like',
                r'want',
                r'would like',
                r'would love'
            ],
            'negative': [
                r'bad',
                r'terrible',
                r'hate',
                r'angry',
                r'problem',
                r'issue',
                r'bug',
                r'error',
                r'crash',
                r'broken',
                r'sad',
                r'unhappy',
                r'frustrated',
                r'disappointed',
                r'don\'t like',
                r'not good',
                r'poor'
            ],
            'urgent': [
                r'urgent',
                r'immediately',
                r'ASAP',
                r'right now',
                r'critical',
                r'important',
                r'priority',
                r'emergency',
                r'need quickly',
                r'urgently',
                r'right away'
            ],
            'confused': [
                r'confused',
                r"don't understand",
                r"can't figure out",
                r'how does this work',
                r'what should I do',
                r'need clarification',
                r'not sure',
                r'help me understand',
                r'not clear',
                r'need explanation'
            ]
        }

        # Domain patterns
        self.domain_patterns = {
            'software_development': [
                r'software',
                r'development',
                r'coding',
                r'programming',
                r'code',
                r'api',
                r'framework',
                r'library',
                r'git',
                r'version control',
                r'javascript',
                r'python',
                r'java',
                r'c\+\+',
                r'c#',
                r'php',
                r'ruby',
                r'database',
                r'sql',
                r'nosql',
                r'frontend',
                r'backend',
                r'fullstack',
                r'devops',
                r'cloud',
                r'aws',
                r'azure',
                r'google cloud',
                r'microservice',
                r'container',
                r'docker',
                r'kubernetes'
            ],
            'digital_marketing': [
                r'marketing',
                r'SEO',
                r'SEM',
                r'PPC',
                r'social media',
                r'advertising',
                r'campaign',
                r'promotion',
                r'branding',
                r'analytics',
                r'google analytics',
                r'facebook ads',
                r'instagram',
                r'twitter',
                r'linkedin',
                r'content marketing',
                r'email marketing',
                r'influencer',
                r'conversion rate',
                r'CTR',
                r'ROI',
                r'KPI',
                r'segmentation',
                r'targeting',
                r'retargeting',
                r'funnel',
                r'customer journey'
            ],
            'content_creation': [
                r'content',
                r'blog',
                r'article',
                r'video',
                r'podcast',
                r'infographic',
                r'copywriting',
                r'creative',
                r'design',
                r'graphic',
                r'writing',
                r'editorial',
                r'content strategy',
                r'storytelling',
                r'visual content',
                r'video production',
                r'audio editing',
                r'photography',
                r'illustration',
                r'content calendar',
                r'content management',
                r'CMS',
                r'wordpress',
                r'content distribution'
            ],
            'project_management': [
                r'project',
                r'management',
                r'task',
                r'deadline',
                r'agile',
                r'scrum',
                r'kanban',
                r'team',
                r'coordination',
                r'planning',
                r'jira',
                r'trello',
                r'asana',
                r'ms project',
                r'gantt chart',
                r'resource allocation',
                r'project timeline',
                r'project scope',
                r'project budget',
                r'risk management',
                r'stakeholder',
                r'project deliverable',
                r'project milestone',
                r'project tracking'
            ],
            'customer_support': [
                r'support',
                r'customer',
                r'helpdesk',
                r'ticket',
                r'complaint',
                r'resolution',
                r'assistance',
                r'help',
                r'service',
                r'client',
                r'customer service',
                r'customer experience',
                r'CX',
                r'chat support',
                r'email support',
                r'phone support',
                r'live chat',
                r'support ticket',
                r'knowledge base',
                r'FAQ',
                r'customer satisfaction',
                r'NPS',
                r'CSAT'
            ],
            'sales': [
                r'sales',
                r'lead',
                r'opportunity',
                r'pipeline',
                r'CRM',
                r'conversion',
                r'revenue',
                r'quota',
                r'forecast',
                r'deal',
                r'sales funnel',
                r'sales process',
                r'sales strategy',
                r'sales target',
                r'sales performance',
                r'sales analytics',
                r'sales automation',
                r'sales enablement',
                r'upselling',
                r'cross-selling',
                r'sales cycle'
            ],
            'finance': [
                r'finance',
                r'accounting',
                r'budget',
                r'invoice',
                r'payment',
                r'billing',
                r'tax',
                r'audit',
                r'financial',
                r'ROI',
                r'profit',
                r'loss',
                r'revenue',
                r'expense',
                r'cash flow',
                r'balance sheet',
                r'income statement',
                r'financial report',
                r'financial planning',
                r'financial analysis',
                r'financial forecasting',
                r'financial management'
            ]
        }

        self.use_llm_fallback = use_llm_fallback
        self.confidence_threshold = 0.7  # Below this, use LLM fallback

    def classify(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify content using hybrid approach

        Args:
            processed_data: Data from modality processors

        Returns:
            Classified data with enhanced details
        """
        try:
            content = processed_data.get('content', '')
            metadata = processed_data.get('metadata', {})

            # Classify content type with confidence
            content_type, type_confidence = self._classify_content_type_with_confidence(content)

            # Classify domain
            domain, domain_confidence = self._classify_domain_with_confidence(content)

            # Analyze emotion (can be multiple)
            emotions = self._analyze_emotions(content)
            primary_emotion = emotions[0] if emotions else 'neutral'
            emotion_score = self._calculate_emotion_score(primary_emotion)

            # Calculate initial score
            initial_score = self._calculate_initial_score(content_type, emotion_score)

            # Check if we need LLM fallback
            if self.use_llm_fallback and (type_confidence < self.confidence_threshold or domain_confidence < self.confidence_threshold):
                # Here we would call LLM for more accurate classification
                # For now, we'll just log that we would use LLM
                logger.info(f"Would use LLM fallback for low confidence: type={type_confidence:.2f}, domain={domain_confidence:.2f}")

            result = {
                'content': content,
                'metadata': {
                    **metadata,
                    'content_type': content_type,
                    'content_confidence': type_confidence,
                    'domain': domain,
                    'domain_confidence': domain_confidence,
                    'emotions': emotions,
                    'primary_emotion': primary_emotion,
                    'emotion_score': emotion_score,
                    'initial_score': initial_score,
                    'classification_method': 'hybrid'
                }
            }

            logger.info(f"Classified content: type={content_type}, domain={domain}, emotions={emotions}, score={initial_score}")
            return result

        except Exception as e:
            logger.error(f"Error classifying content: {e}")
            raise ValueError(f"Content classification failed: {e}")

    def _classify_content_type_with_confidence(self, content: str) -> tuple:
        """Classify content type with confidence score"""
        best_type = 'general_inquiry'
        best_score = 0

        for content_type, patterns in self.content_patterns.items():
            score = sum(1 for pattern in patterns if re.search(pattern, content.lower()))
            if score > best_score:
                best_score = score
                best_type = content_type

        # Calculate confidence (0-1)
        confidence = min(1.0, best_score * 0.2)  # Max 5 patterns = 1.0 confidence

        return best_type, confidence

    def _classify_domain_with_confidence(self, content: str) -> tuple:
        """Classify domain with confidence score"""
        best_domain = 'general'
        best_score = 0

        for domain, patterns in self.domain_patterns.items():
            score = sum(1 for pattern in patterns if re.search(pattern, content.lower()))
            if score > best_score:
                best_score = score
                best_domain = domain

        # Calculate confidence (0-1)
        confidence = min(1.0, best_score * 0.15)  # Max 6-7 patterns = 1.0 confidence

        return best_domain, confidence

    def _analyze_emotions(self, content: str) -> List[str]:
        """Analyze multiple emotions in the content"""
        emotions_found = []

        for emotion, patterns in self.emotion_patterns.items():
            score = sum(1 for pattern in patterns if re.search(pattern, content.lower()))
            if score > 0:
                emotions_found.append(emotion)

        return emotions_found if emotions_found else ['neutral']

    def _calculate_emotion_score(self, primary_emotion: str) -> float:
        """Calculate emotion score based on primary emotion"""
        emotion_scores = {
            'positive': 0.75,
            'negative': 0.25,
            'urgent': 0.8,
            'confused': 0.4,
            'neutral': 0.5
        }
        return emotion_scores.get(primary_emotion, 0.5)

    def _calculate_initial_score(self, content_type: str, emotion_score: float) -> float:
        """Calculate initial score based on content type and emotion"""
        # Base scores by content type
        type_scores = {
            'feature_request': 0.85,
            'bug_report': 0.9,  # High priority
            'user_feedback': 0.7,
            'technical_question': 0.65,
            'marketing_idea': 0.75,
            'content_request': 0.7,
            'project_management': 0.6,
            'billing_question': 0.55,
            'general_inquiry': 0.45
        }

        base_score = type_scores.get(content_type, 0.4)
        return (base_score * 0.6) + (emotion_score * 0.4)  # Weighted average

