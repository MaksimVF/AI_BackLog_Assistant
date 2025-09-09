



"""
PipelineAdjuster - Sub-agent for recommending pipeline adjustments.

This agent analyzes data quality and suggests re-running specific tools
or agents to improve extraction results.
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class PipelineAdjuster:
    def __init__(self):
        """
        Initialize the PipelineAdjuster.
        """
        self.quality_thresholds = {
            "ocr_quality": 0.8,
            "audio_quality": 0.7,
            "text_coverage": 0.6,
            "confidence_score": 0.75
        }

    def adjust(self, data: Dict[str, Any], evaluation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recommend pipeline adjustments based on data quality.

        Args:
            data: Structured data to analyze
            evaluation_results: Results from other evaluators

        Returns:
            Dictionary with pipeline adjustment recommendations
        """
        recommendations = []

        # Check OCR quality
        if "ocr_quality" in data and data["ocr_quality"] < self.quality_thresholds["ocr_quality"]:
            recommendations.append({
                "action": "re_run_ocr",
                "reason": f"OCR quality {data['ocr_quality']:.2f} below threshold {self.quality_thresholds['ocr_quality']}",
                "parameters": {"enhance_images": True}
            })

        # Check audio quality
        if "audio_quality" in data and data["audio_quality"] < self.quality_thresholds["audio_quality"]:
            recommendations.append({
                "action": "re_run_audio2text",
                "reason": f"Audio quality {data['audio_quality']:.2f} below threshold {self.quality_thresholds['audio_quality']}",
                "parameters": {"noise_reduction": True}
            })

        # Check completeness
        if evaluation_results.get("completeness_score", 1.0) < self.quality_thresholds["confidence_score"]:
            recommendations.append({
                "action": "re_extract_data",
                "reason": f"Completeness score {evaluation_results['completeness_score']:.2f} below threshold {self.quality_thresholds['confidence_score']}",
                "parameters": {"focus_areas": evaluation_results.get("missing_fields", [])}
            })

        return {
            "recommendations": recommendations,
            "adjustments_needed": len(recommendations) > 0,
            "status": "optimal" if not recommendations else "needs_adjustment"
        }

    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the PipelineAdjuster.

        Returns:
            Dictionary with status information
        """
        return {
            "agent": "PipelineAdjuster",
            "status": "ready",
            "thresholds": self.quality_thresholds
        }



