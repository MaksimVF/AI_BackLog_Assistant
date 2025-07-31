















"""
Test SeriesSync Agent
"""

from agents.series_sync.series_sync_agent import SeriesSyncAgent

def test_series_sync_agent():
    """Test the SeriesSyncAgent with sample data."""

    # Sample event log
    event_log = [
        {"timestamp": "2025-07-01", "type": "incident", "project": "Alpha", "description": "Server crash", "priority": "high"},
        {"timestamp": "2025-07-03", "type": "incident", "project": "Alpha", "description": "Network outage", "priority": "medium"},
        {"timestamp": "2025-07-05", "type": "task", "project": "Beta", "description": "Feature implementation", "priority": "low"},
        {"timestamp": "2025-07-07", "type": "incident", "project": "Alpha", "description": "Database error", "priority": "high"},
        {"timestamp": "2025-07-10", "type": "incident", "project": "Alpha", "description": "API timeout", "priority": "medium"}
    ]

    # Sample case database
    case_database = [
        {
            "title": "Server Crash Resolution",
            "description": "Multiple server crashes due to memory leaks",
            "tags": ["incident", "server", "memory"],
            "category": "incident"
        },
        {
            "title": "Network Outage Procedure",
            "description": "Standard procedure for handling network outages",
            "tags": ["incident", "network"],
            "category": "procedure"
        },
        {
            "title": "Database Optimization",
            "description": "Guide for optimizing database performance",
            "tags": ["maintenance", "database"],
            "category": "guide"
        }
    ]

    print("Testing SeriesSyncAgent...")
    print("Event log:", event_log)
    print("Case database:", case_database)
    print("\n" + "="*60 + "\n")

    # Create and test the SeriesSyncAgent
    agent = SeriesSyncAgent(
        event_log=event_log,
        case_database=case_database
    )

    # Run analysis
    result = agent.run(
        time_window_start="2025-07-01",
        time_window_end="2025-07-10",
        filters={"project": "Alpha"},
        context={"category": "incident", "tags": ["incident"]}
    )

    # Generate formatted report
    report = agent.generate_formatted_report(result)

    print("ANALYSIS RESULT:")
    print("Data series length:", len(result["data_series"]))
    print("Patterns detected:", len(result["patterns"]["patterns_detected"]))
    print("Relevant cases found:", len(result["relevant_cases"]))
    print("\n" + "="*60 + "\n")

    print("FORMATTED REPORT:")
    print(report)

    print("\n" + "="*60 + "\n")
    print("Test completed successfully!")

if __name__ == "__main__":
    test_series_sync_agent()















