




"""
Final verification test for the pipeline architecture
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all pipeline modules can be imported"""
    try:
        # Test base pipeline
        from pipelines.base_pipeline import BasePipeline, PipelineConfig
        print("✅ Base pipeline imported successfully")

        # Test pipeline schemas (these should work without crewai)
        from pipelines.input_processing_pipeline import IPPInputSchema, IPPOutputSchema
        from pipelines.information_manipulation_pipeline import IMPInputSchema, IMPOutputSchema
        from pipelines.output_pipeline import OPInputSchema, OPOutputSchema
        print("✅ Pipeline schemas imported successfully")

        # Test IMP agents (these should work without crewai)
        from agents.imp.result_aggregator_agent import ResultAggregatorAgent
        from agents.imp.context_enricher_agent import ContextEnricherAgent
        from agents.imp.metadata_enricher_agent import MetadataEnricherAgent
        from agents.imp.quality_assurance_agent import QualityAssuranceAgent
        print("✅ IMP agents imported successfully")

        return True

    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_schema_validation():
    """Test schema validation"""
    try:
        from pipelines.input_processing_pipeline import IPPInputSchema, IPPOutputSchema
        from pipelines.information_manipulation_pipeline import IMPInputSchema, IMPOutputSchema
        from pipelines.output_pipeline import OPInputSchema, OPOutputSchema

        # Test IPP schemas
        ipp_input = IPPInputSchema(
            document_id="test_doc",
            raw_content="test content",
            metadata={"source": "test"}
        )
        assert ipp_input.document_id == "test_doc"

        ipp_output = IPPOutputSchema(
            document_id="test_doc",
            raw_text="processed text",
            modality="text",
            entities={"test": ["entity1"]},
            intent="test_intent",
            metadata={"source": "test"}
        )
        assert ipp_output.modality == "text"

        # Test IMP schemas
        imp_input = IMPInputSchema(
            document_id="test_doc",
            raw_text="processed text",
            modality="text",
            entities={"test": ["entity1"]},
            intent="test_intent",
            metadata={"source": "test"}
        )
        assert imp_input.document_id == "test_doc"

        imp_output = IMPOutputSchema(
            document_id="test_doc",
            processed_text="enriched text",
            analysis={
                "priority": "high",
                "criticality": "normal",
                "bottlenecks": [],
                "scores": {"priority_score": 5.0},
                "decision": "proceed"
            },
            metadata={"source": "test"},
            quality={"completeness": 90}
        )
        assert imp_output.analysis["priority"] == "high"

        # Test OP schemas
        op_input = OPInputSchema(
            document_id="test_doc",
            processed_text="enriched text",
            analysis={
                "priority": "high",
                "criticality": "normal",
                "bottlenecks": [],
                "scores": {"priority_score": 5.0},
                "decision": "proceed"
            },
            metadata={"source": "test"},
            quality={"completeness": 90}
        )
        assert op_input.document_id == "test_doc"

        op_output = OPOutputSchema(
            document_id="test_doc",
            summary="final summary",
            key_points=["point1", "point2"],
            recommendations=["rec1"],
            formatted_output="final result",
            delivery_format="json"
        )
        assert op_output.delivery_format == "json"

        print("✅ Schema validation tests passed")
        return True

    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        return False

def test_base_pipeline():
    """Test base pipeline functionality"""
    try:
        from pipelines.base_pipeline import BasePipeline, PipelineConfig

        class TestPipeline(BasePipeline):
            def _process(self, data):
                return {"processed": True, "input": data}

        pipeline = TestPipeline(PipelineConfig(enable_logging=False))
        result = pipeline.process({"test": "data"})

        assert result["processed"] == True
        assert result["input"]["test"] == "data"

        print("✅ Base pipeline test passed")
        return True

    except Exception as e:
        print(f"❌ Base pipeline test failed: {e}")
        return False

def test_imp_agents():
    """Test IMP agent instantiation"""
    try:
        # These should work without crewai since they use base agent class
        from agents.imp.result_aggregator_agent import ResultAggregatorAgent
        from agents.imp.context_enricher_agent import ContextEnricherAgent
        from agents.imp.metadata_enricher_agent import MetadataEnricherAgent
        from agents.imp.quality_assurance_agent import QualityAssuranceAgent

        # Test instantiation
        result_aggregator = ResultAggregatorAgent()
        context_enricher = ContextEnricherAgent()
        metadata_enricher = MetadataEnricherAgent()
        quality_assurance = QualityAssuranceAgent()

        print("✅ IMP agent instantiation tests passed")
        return True

    except Exception as e:
        print(f"❌ IMP agent test failed: {e}")
        return False

def run_all_tests():
    """Run all verification tests"""
    print("Running final verification tests...\n")

    tests = [
        ("Import Tests", test_imports),
        ("Schema Validation Tests", test_schema_validation),
        ("Base Pipeline Tests", test_base_pipeline),
        ("IMP Agent Tests", test_imp_agents),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append(False)

    passed = sum(results)
    total = len(results)

    print(f"\n=== FINAL RESULTS ===")
    print(f"Tests Passed: {passed}/{total}")

    if passed == total:
        print("🎉 ALL TESTS PASSED! Pipeline architecture is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please review the implementation.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)


