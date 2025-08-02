



"""
Quality Assurance Agent

Performs final quality checks on processed data before output.
"""

from typing import Dict, Any
from pydantic import BaseModel

class QualityAssessment(BaseModel):
    """Structure for quality assessment results"""
    completeness: float
    accuracy: float
    consistency: float
    overall_quality: float
    issues: list

class QualityAssuranceAgent:
    """
    Performs quality assurance checks on processed data.
    """

    def assess_quality(
        self,
        processed_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Assess the quality of processed data.

        Args:
            processed_data: Data to assess

        Returns:
            Quality assessment results
        """
        # Check completeness
        completeness = self._check_completeness(processed_data)

        # Check accuracy
        accuracy = self._check_accuracy(processed_data)

        # Check consistency
        consistency = self._check_consistency(processed_data)

        # Calculate overall quality
        overall_quality = (completeness + accuracy + consistency) / 3

        # Identify any issues
        issues = self._identify_issues(processed_data)

        result = QualityAssessment(
            completeness=completeness,
            accuracy=accuracy,
            consistency=consistency,
            overall_quality=overall_quality,
            issues=issues
        )

        return result.dict()

    def _check_completeness(self, data: Dict[str, Any]) -> float:
        """Check data completeness"""
        required_fields = ['document_id', 'processed_text', 'analysis', 'metadata']
        missing_fields = [field for field in required_fields if field not in data]

        # Calculate completeness score (100% if no fields missing)
        completeness = 100 - (len(missing_fields) * 10)
        return max(0, min(100, completeness))

    def _check_accuracy(self, data: Dict[str, Any]) -> float:
        """Check data accuracy"""
        # In a real implementation, this would perform actual accuracy checks
        # For now, return a default score
        return 95.0

    def _check_consistency(self, data: Dict[str, Any]) -> float:
        """Check data consistency"""
        # Check that analysis results are consistent with each other
        analysis = data.get('analysis', {})

        # Check priority vs criticality consistency
        priority = analysis.get('priority', 'medium')
        criticality = analysis.get('criticality', 'normal')

        consistency_score = 100
        if priority == 'high' and criticality == 'normal':
            consistency_score = 80
        elif priority == 'low' and criticality == 'critical':
            consistency_score = 70

        return consistency_score

    def _identify_issues(self, data: Dict[str, Any]) -> list:
        """Identify potential quality issues"""
        issues = []

        # Check for missing required fields
        required_fields = ['document_id', 'processed_text', 'analysis', 'metadata']
        for field in required_fields:
            if field not in data:
                issues.append(f"Missing required field: {field}")

        # Check analysis consistency
        analysis = data.get('analysis', {})
        priority = analysis.get('priority', 'medium')
        criticality = analysis.get('criticality', 'normal')

        if priority == 'high' and criticality == 'normal':
            issues.append("Inconsistency: High priority but normal criticality")
        elif priority == 'low' and criticality == 'critical':
            issues.append("Inconsistency: Low priority but critical criticality")

        return issues


