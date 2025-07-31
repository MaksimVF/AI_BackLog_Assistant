













"""
Test Fallback Planner
"""

from agents.service.fallback_planner import FallbackPlanner

fallback_config = {
    "ChartGenerator": {
        "TimeoutError": "TableRenderer",
        "ValueError": "SimplifiedChartMode"
    },
    "SchedulingIntegrator": {
        "APIError": "ManualExport"
    }
}

def test_fallback_planner_returns_configured_fallback():
    """Test that FallbackPlanner returns configured fallback"""
    planner = FallbackPlanner(fallback_config)
    fallback = planner.run({
        "agent": "ChartGenerator",
        "error_type": "TimeoutError",
        "attempt": 1
    })

    assert fallback["fallback"] == "TableRenderer"
    assert fallback["action"] == "retry_with_fallback"
    assert fallback["attempt"] == 2

def test_fallback_planner_handles_unknown_case():
    """Test FallbackPlanner with unknown agent/error"""
    planner = FallbackPlanner(fallback_config)
    fallback = planner.run({
        "agent": "UnknownAgent",
        "error_type": "WhateverError",
        "attempt": 2
    })

    assert fallback["fallback"] == "manual_review"
    assert fallback["action"] == "escalate"
    assert fallback["attempt"] == 3

def test_fallback_planner_without_config():
    """Test FallbackPlanner without config"""
    planner = FallbackPlanner()
    fallback = planner.run({
        "agent": "AnyAgent",
        "error_type": "AnyError",
        "attempt": 1
    })

    assert fallback["fallback"] == "manual_review"
    assert fallback["action"] == "escalate"

if __name__ == "__main__":
    test_fallback_planner_returns_configured_fallback()
    test_fallback_planner_handles_unknown_case()
    test_fallback_planner_without_config()
    print("All fallback planner tests passed!")














