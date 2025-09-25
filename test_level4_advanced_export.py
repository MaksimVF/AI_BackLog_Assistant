









"""
Test Advanced Export Capabilities

Comprehensive test suite for the advanced export capabilities.
"""

import logging
from src.v2.agents.level4.visualization.advanced_export_manager import AdvancedExportManager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def test_advanced_export():
    """Test the advanced export capabilities"""
    print("Testing Advanced Export Capabilities...")

    # Sample data
    tasks = [
        {"id": 1, "title": "Fix security vulnerability", "priority": "high", "category": "security", "value": 10},
        {"id": 2, "title": "Update UI components", "priority": "medium", "category": "ui", "value": 5},
        {"id": 3, "title": "Add documentation", "priority": "low", "category": "docs", "value": 3},
        {"id": 4, "title": "Optimize database queries", "priority": "high", "category": "performance", "value": 8},
        {"id": 5, "title": "Implement API endpoint", "priority": "medium", "category": "api", "value": 6},
    ]

    # Test advanced export manager
    print("\nTesting AdvancedExportManager...")
    export_manager = AdvancedExportManager()

    # Test interactive HTML export
    print("\nTesting interactive HTML export...")
    html_content = export_manager.export_to_interactive_html(tasks, "Test Report")
    print(f"✅ HTML export: {len(html_content)} characters")

    # Test PDF export
    print("\nTesting PDF export...")
    pdf_content = export_manager.export_to_pdf(tasks, "Test Report")
    print(f"✅ PDF export: {len(pdf_content)} bytes")

    # Test Excel export
    print("\nTesting Excel export...")
    excel_content = export_manager.export_to_excel(tasks)
    print(f"✅ Excel export: {len(excel_content)} bytes")

    # Test JSON export
    print("\nTesting JSON export...")
    json_content = export_manager.export_to_json(tasks)
    print(f"✅ JSON export: {len(json_content)} characters")

    # Test CSV export
    print("\nTesting CSV export...")
    csv_content = export_manager.export_to_csv(tasks)
    print(f"✅ CSV export: {len(csv_content)} characters")

    # Test comprehensive report
    print("\nTesting comprehensive report...")
    comprehensive_report = export_manager.generate_comprehensive_report(tasks, "Comprehensive Report")
    print(f"✅ Comprehensive report: {list(comprehensive_report.keys())}")

    # Test visualization report
    print("\nTesting visualization report...")
    chart_config = {
        "type": "bar",
        "labels": ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5"],
        "data": [10, 5, 3, 8, 6],
        "label": "Task Values",
        "colors": ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"]
    }
    visualization_report = export_manager.generate_visualization_report(tasks, [chart_config], "Visualization Report")
    print(f"✅ Visualization report: {list(visualization_report.keys())}")

    # Test accessible report
    print("\nTesting accessible report...")
    accessible_report = export_manager.generate_accessible_report(tasks, "Accessible Report")
    print(f"✅ Accessible report: {list(accessible_report.keys())}")

    print("\n🎉 All advanced export capabilities tests completed successfully!")

if __name__ == "__main__":
    test_advanced_export()












