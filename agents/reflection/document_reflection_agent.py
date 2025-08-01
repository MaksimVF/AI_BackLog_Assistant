




"""
DocumentReflectionAgent - Comprehensive agent for document analysis and reflection.

This agent integrates multiple sub-agents to provide a complete analysis of documents,
including fact verification, sentiment analysis, redundancy detection, ambiguity detection,
conflict detection, and more.
"""

from .gap_detector import GapDetector
from .redundancy_detector import RedundancyDetector
from .ambiguity_detector import AmbiguityDetector
from .conflict_detector import ConflictDetector
from .style_and_tone_analyzer import StyleAndToneAnalyzer
from .advanced_sentiment_tone_analyzer import AdvancedSentimentAndToneAnalyzer
from .fact_verification_agent import FactVerificationAgent
from .document_summarizer import DocumentSummarizer
from .semantic_consistency_checker import SemanticConsistencyChecker

class DocumentReflectionAgent:
    """
    Comprehensive agent for document analysis and reflection.
    """

    def __init__(self):
        """
        Initialize DocumentReflectionAgent with all sub-agents.
        """
        # Basic analysis agents
        self.gap_detector = GapDetector()
        self.redundancy_detector = RedundancyDetector()
        self.ambiguity_detector = AmbiguityDetector()
        self.conflict_detector = ConflictDetector()
        self.style_analyzer = StyleAndToneAnalyzer()

        # Advanced LLM-based agents
        self.advanced_sentiment_analyzer = AdvancedSentimentAndToneAnalyzer()
        self.fact_verifier = FactVerificationAgent()
        self.summary_generator = DocumentSummarizer()

        # Semantic analysis
        self.semantic_checker = SemanticConsistencyChecker()

    def analyze_text(self, text: str, text_blocks: list = None) -> dict:
        """
        Analyze text content using all relevant sub-agents.

        Args:
            text: Full text of the document
            text_blocks: Optional list of text blocks for redundancy detection

        Returns:
            Dictionary with comprehensive analysis results
        """
        results = {}

        # Text analysis
        results["summary"] = self.summary_generator.generate_summary(text)
        results["sentiment_analysis"] = self.advanced_sentiment_analyzer.analyze(text)
        results["style_analysis"] = self.style_analyzer.analyze(text)
        results["fact_verification"] = self.fact_verifier.verify_facts(text)
        results["ambiguity_detection"] = self.ambiguity_detector.evaluate(text)
        results["conflict_detection"] = self.conflict_detector.evaluate(text)

        # Redundancy detection (if text blocks provided)
        if text_blocks:
            results["redundancy_analysis"] = self.redundancy_detector.evaluate(text_blocks)
        else:
            results["redundancy_analysis"] = {"message": "Text blocks not provided for redundancy analysis"}

        return results

    def analyze_structure(self, structured_data: dict) -> dict:
        """
        Analyze structured document data.

        Args:
            structured_data: Structured document data

        Returns:
            Dictionary with structural analysis results
        """
        results = {}

        # Structural analysis
        results["gap_analysis"] = self.gap_detector.evaluate(structured_data)
        results["semantic_consistency"] = self.semantic_checker.analyze(structured_data)

        return results

    def comprehensive_analysis(self, text: str, structured_data: dict, text_blocks: list = None) -> dict:
        """
        Perform comprehensive analysis of both text and structured data.

        Args:
            text: Full text of the document
            structured_data: Structured document data
            text_blocks: Optional list of text blocks

        Returns:
            Dictionary with complete analysis results
        """
        text_results = self.analyze_text(text, text_blocks)
        structure_results = self.analyze_structure(structured_data)

        # Combine results
        return {
            "text_analysis": text_results,
            "structure_analysis": structure_results,
            "overall_status": self._generate_overall_status(text_results, structure_results)
        }

    def _generate_overall_status(self, text_results: dict, structure_results: dict) -> dict:
        """
        Generate overall status based on all analysis results.
        """
        issues = []

        # Check text analysis issues
        if text_results["ambiguity_detection"]["ambiguity_detected"]:
            issues.append("Обнаружены двусмысленные формулировки")

        if text_results["conflict_detection"]["conflict_detected"]:
            issues.append("Обнаружены логические противоречия")

        # Check structure analysis issues
        if structure_results["gap_analysis"]["missing_fields_found"]:
            issues.append(f"Отсутствуют обязательные поля: {', '.join(structure_results['gap_analysis']['missing_fields'])}")

        if not structure_results["semantic_consistency"]["is_complete"]:
            issues.append("Документ неполный или содержит семантические противоречия")

        # Generate recommendation
        if issues:
            recommendation = "Рекомендуется ревизия документа. Проблемы: " + "; ".join(issues)
        else:
            recommendation = "Документ семантически корректен и полон."

        return {
            "issues_found": bool(issues),
            "issue_list": issues,
            "recommendation": recommendation
        }



