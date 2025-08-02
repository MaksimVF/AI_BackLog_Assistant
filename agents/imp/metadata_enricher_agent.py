



"""
Metadata Enricher Agent

Enriches metadata with additional information based on analysis results.
"""

from typing import Dict, Any
from pydantic import BaseModel
from datetime import datetime

class MetadataEnricherAgent:
    """
    Enriches metadata with analysis-derived information.
    """

    def enrich(
        self,
        document_id: str,
        original_metadata: Dict[str, Any],
        priority: str,
        criticality: str,
        decision: str
    ) -> Dict[str, Any]:
        """
        Enrich metadata with analysis results.

        Args:
            document_id: Unique document identifier
            original_metadata: Original metadata from previous stages
            priority: Calculated priority
            criticality: Calculated criticality
            decision: Recommended decision

        Returns:
            Enriched metadata
        """
        # Add analysis-derived metadata
        analysis_metadata = {
            'priority': priority,
            'criticality': criticality,
            'recommended_action': decision,
            'analysis_timestamp': datetime.now().isoformat(),
            'analysis_version': '1.0'
        }

        # Add ownership and responsibility information
        ownership_metadata = self._determine_ownership(original_metadata, priority, criticality)

        # Add compliance and regulatory metadata
        compliance_metadata = self._determine_compliance(original_metadata, criticality)

        # Merge all metadata
        enriched_metadata = {
            **original_metadata,
            'analysis': analysis_metadata,
            'ownership': ownership_metadata,
            'compliance': compliance_metadata
        }

        return enriched_metadata

    def _determine_ownership(self, metadata: Dict[str, Any], priority: str, criticality: str) -> Dict[str, Any]:
        """Determine ownership based on priority and criticality"""
        # In a real implementation, this would use business rules
        if priority == 'high' and criticality == 'critical':
            return {
                'owner': 'executive_team',
                'responsible_party': 'cto',
                'escalation_level': 'level_1'
            }
        elif priority == 'high':
            return {
                'owner': 'management',
                'responsible_party': 'project_manager',
                'escalation_level': 'level_2'
            }
        else:
            return {
                'owner': 'operational_team',
                'responsible_party': 'team_lead',
                'escalation_level': 'level_3'
            }

    def _determine_compliance(self, metadata: Dict[str, Any], criticality: str) -> Dict[str, Any]:
        """Determine compliance requirements"""
        # In a real implementation, this would check regulatory requirements
        if criticality == 'critical':
            return {
                'compliance_level': 'high',
                'regulatory_requirements': ['GDPR', 'HIPAA', 'SOX'],
                'audit_required': True
            }
        elif criticality == 'important':
            return {
                'compliance_level': 'medium',
                'regulatory_requirements': ['GDPR'],
                'audit_required': False
            }
        else:
            return {
                'compliance_level': 'low',
                'regulatory_requirements': [],
                'audit_required': False
            }



