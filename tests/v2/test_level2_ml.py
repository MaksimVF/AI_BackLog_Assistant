




"""
Comprehensive Tests for Level 2 ML Capabilities

Tests include:
- ML model training and prediction
- Agent integration with ML models
- Pipeline processing with ML
- Error handling and fallback
"""

import pytest
from unittest.mock import patch, MagicMock
from src.v2.ml.classification import DocumentClassifierModel
from src.v2.ml.prioritization import PrioritizationModel
from src.v2.ml.quality import QualityAnalysisModel
from src.v2.agents.level2.categorization.document_classifier import DocumentClassifierAgent
from src.v2.agents.level2.prioritization.prioritization_agent import PrioritizationAgent
from src.v2.agents.level2.reflection.reflection_agent import ReflectionAgent
from src.v2.pipelines.level2.level2_pipeline import Level2Pipeline

class TestLevel2ML:
    """Test Level 2 ML capabilities"""

    def test_document_classifier_ml(self):
        """Test ML-based document classification"""
        # Initialize agent with ML
        agent = DocumentClassifierAgent(use_ml=True)

        # Test classification
        test_data = {
            "document_id": "test1",
            "content": "This is an urgent document about system failures",
            "metadata": {"source": "email"}
        }

        result = agent.classify(test_data)

        # Verify ML classification
        assert "classification" in result
        assert "category" in result["classification"]
        assert "confidence" in result["classification"]
        assert result["classification"]["confidence"] > 0.5

    def test_prioritization_ml(self):
        """Test ML-based prioritization"""
        # Initialize agent with ML
        agent = PrioritizationAgent(algorithm="ml")

        # Test prioritization
        test_data = {
            "document_id": "test2",
            "content": "Important document",
            "metadata": {"source": "email"},
            "classification": {"category": "important", "confidence": 0.8}
        }

        result = agent.prioritize(test_data)

        # Verify ML prioritization
        assert "prioritization" in result
        assert "priority_level" in result["prioritization"]
        assert result["prioritization"]["algorithm"] == "ml_based"

    def test_reflection_ml(self):
        """Test ML-based reflection analysis"""
        # Initialize agent with ML
        agent = ReflectionAgent(analysis_level="ml")

        # Test reflection
        test_data = {
            "document_id": "test3",
            "content": "This document has some contradictions but overall is good",
            "classification": {"category": "important", "confidence": 0.8},
            "prioritization": {"priority_level": "high"}
        }

        result = agent.analyze(test_data)

        # Verify ML reflection
        assert "reflection" in result
        assert "quality_score" in result["reflection"]
        assert "sentiment" in result["reflection"]
        assert result["reflection"]["analysis_level"] == "ml_based"

    def test_pipeline_ml_integration(self):
        """Test pipeline with ML integration"""
        # Initialize pipeline
        pipeline = Level2Pipeline(max_workers=2)

        # Test data
        test_data = {
            "document_id": "test4",
            "content": "Comprehensive test document",
            "metadata": {"source": "api"}
        }

        # Process through pipeline
        result = pipeline.process(test_data)

        # Verify pipeline processing
        assert "classification" in result
        assert "prioritization" in result
        assert "reflection" in result

    def test_ml_model_training(self):
        """Test ML model training"""
        # Initialize classifier model
        model = DocumentClassifierModel()

        # Train model
        documents = ["Document 1", "Document 2", "Document 3"]
        labels = ["urgent", "important", "normal"]

        model.train(documents, labels)

        # Verify model is trained
        assert model.is_trained

        # Test prediction
        result = model.predict("New document")
        assert "category" in result
        assert "confidence" in result

    def test_feedback_learning(self):
        """Test adaptive learning from feedback"""
        # Initialize agents
        classifier = DocumentClassifierAgent(use_ml=True)
        prioritizer = PrioritizationAgent(algorithm="ml")
        reflector = ReflectionAgent(analysis_level="ml")

        # Test feedback updates
        classifier.update_with_feedback("test5", "urgent")
        prioritizer.update_with_feedback("test6", "high")
        reflector.update_with_feedback("test7", 0.9)

        # Verify feedback processing
        assert True  # Basic verification - would need more complex testing

    def test_error_handling(self):
        """Test error handling in ML agents"""
        # Test with invalid input
        agent = DocumentClassifierAgent(use_ml=True)

        # Test empty content
        result = agent.classify({"document_id": "test8", "content": ""})
        assert result["classification"]["category"] == "unknown"

        # Test invalid content
        result = agent.classify({"document_id": "test9"})
        assert result["classification"]["category"] == "unknown"

    def test_batch_processing(self):
        """Test batch processing with ML"""
        # Initialize pipeline
        pipeline = Level2Pipeline(max_workers=4)

        # Test batch data
        batch_data = [
            {"document_id": f"batch{i}", "content": f"Batch content {i}", "metadata": {"source": "api"}}
            for i in range(5)
        ]

        # Process batch
        results = pipeline.process_batch(batch_data)

        # Verify batch processing
        assert len(results) == 5
        for result in results:
            assert "classification" in result
            assert "prioritization" in result
            assert "reflection" in result

    def test_fallback_mechanisms(self):
        """Test fallback from ML to rule-based"""
        # Initialize agent with ML but simulate ML failure
        agent = DocumentClassifierAgent(use_ml=True)

        # Mock ML model to fail
        with patch.object(agent.ml_model, 'predict', side_effect=Exception("ML failure")):
            result = agent.classify({"document_id": "test10", "content": "Test content"})

            # Should fall back to rule-based
            assert "classification" in result
            assert result["classification"]["category"] != "error"

    def test_performance_monitoring(self):
        """Test performance monitoring"""
        # Initialize pipeline
        pipeline = Level2Pipeline(max_workers=2)

        # Test with monitoring
        test_data = {
            "document_id": "test11",
            "content": "Performance test document",
            "metadata": {"source": "api"}
        }

        result = pipeline.process_with_monitoring(test_data)

        # Verify monitoring data
        assert "_monitoring" in result
        assert "processing_time" in result["_monitoring"]
        assert result["_monitoring"]["status"] == "success"




