









"""
Advanced Export Manager

Enhanced export capabilities with interactive HTML and PDF reports.
"""

import logging
import json
import csv
import io
from typing import List, Dict, Any, Optional
from crewai import Agent
from weasyprint import HTML, CSS
from jinja2 import Template

logger = logging.getLogger(__name__)

class AdvancedExportManager:
    """
    Manages advanced export capabilities with interactive HTML and PDF reports.
    """

    def __init__(self):
        """
        Initialize advanced export manager with CrewAI agent.
        """
        # Initialize CrewAI agent for advanced export
        self.agent = Agent(
            name="AdvancedExportManager",
            role="Advanced export manager for visualization",
            goal="""
                Manage advanced export capabilities with interactive HTML and PDF reports.
                Provide comprehensive export options for visualization.
            """,
            backstory="""
                You are an advanced export manager that uses
                sophisticated techniques to generate comprehensive reports.
            """,
            tools=[],
            verbose=True
        )

    def export_to_interactive_html(self, data: List[Dict[str, Any]], title: str = "Interactive Report") -> str:
        """
        Export data to interactive HTML report.

        Args:
            data: Data to export
            title: Report title

        Returns:
            HTML content
        """
        try:
            # Generate interactive HTML report
            html_template = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{{ title }}</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    h1 { color: #333; }
                    table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #f2f2f2; }
                    tr:nth-child(even) { background-color: #f9f9f9; }
                    .chart { width: 100%; height: 400px; margin: 20px 0; }
                    .interactive { cursor: pointer; }
                </style>
            </head>
            <body>
                <h1>{{ title }}</h1>
                <div class="chart" id="chart"></div>
                <table>
                    <thead>
                        <tr>
                            {% for key in data[0].keys() %}
                                <th>{{ key }}</th>
                            {% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in data %}
                            <tr class="interactive" onclick="showDetails({{ loop.index }})">
                                {% for key in item.keys() %}
                                    <td>{{ item[key] }}</td>
                                {% endfor %}
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
                <script>
                    function showDetails(index) {
                        const item = {{ data | tojson }};
                        alert('Details for item ' + index + ': ' + JSON.stringify(item[index - 1]));
                    }
                </script>
            </body>
            </html>
            """

            # Render template
            template = Template(html_template)
            html_content = template.render(title=title, data=data)

            logger.info("Generated interactive HTML report")
            return html_content

        except Exception as e:
            logger.error(f"Interactive HTML export failed: {e}")
            raise

    def export_to_pdf(self, data: List[Dict[str, Any]], title: str = "PDF Report") -> bytes:
        """
        Export data to PDF report.

        Args:
            data: Data to export
            title: Report title

        Returns:
            PDF content as bytes
        """
        try:
            # Generate HTML content first
            html_content = self.export_to_interactive_html(data, title)

            # Convert HTML to PDF
            pdf_buffer = io.BytesIO()
            HTML(string=html_content).write_pdf(pdf_buffer)

            pdf_buffer.seek(0)
            pdf_data = pdf_buffer.getvalue()
            pdf_buffer.close()

            logger.info("Generated PDF report")
            return pdf_data

        except Exception as e:
            logger.error(f"PDF export failed: {e}")
            raise

    def export_to_excel(self, data: List[Dict[str, Any]], filename: str = "report.xlsx") -> bytes:
        """
        Export data to Excel format.

        Args:
            data: Data to export
            filename: Excel filename

        Returns:
            Excel content as bytes
        """
        try:
            import pandas as pd

            # Convert data to DataFrame
            df = pd.DataFrame(data)

            # Export to Excel
            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False)

            excel_buffer.seek(0)
            excel_data = excel_buffer.getvalue()
            excel_buffer.close()

            logger.info("Generated Excel report")
            return excel_data

        except Exception as e:
            logger.error(f"Excel export failed: {e}")
            raise

    def export_to_json(self, data: List[Dict[str, Any]], indent: int = 2) -> str:
        """
        Export data to JSON format.

        Args:
            data: Data to export
            indent: JSON indentation

        Returns:
            JSON content
        """
        try:
            # Convert data to JSON
            json_content = json.dumps(data, indent=indent)

            logger.info("Generated JSON export")
            return json_content

        except Exception as e:
            logger.error(f"JSON export failed: {e}")
            raise

    def export_to_csv(self, data: List[Dict[str, Any]]) -> str:
        """
        Export data to CSV format.

        Args:
            data: Data to export

        Returns:
            CSV content
        """
        try:
            # Convert data to CSV
            csv_buffer = io.StringIO()
            if data:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerows(data)

                csv_content = csv_buffer.getvalue()
                csv_buffer.close()

                logger.info("Generated CSV export")
                return csv_content
            else:
                return ""

        except Exception as e:
            logger.error(f"CSV export failed: {e}")
            raise

    def generate_comprehensive_report(self, data: List[Dict[str, Any]], title: str = "Comprehensive Report") -> Dict[str, Any]:
        """
        Generate comprehensive report with multiple formats.

        Args:
            data: Data to export
            title: Report title

        Returns:
            Comprehensive report with multiple formats
        """
        try:
            # Generate multiple formats
            report = {
                "html": self.export_to_interactive_html(data, title),
                "pdf": self.export_to_pdf(data, title),
                "excel": self.export_to_excel(data),
                "json": self.export_to_json(data),
                "csv": self.export_to_csv(data),
                "metadata": {
                    "title": title,
                    "item_count": len(data),
                    "contextual_insights": "Comprehensive report with multiple formats"
                }
            }

            logger.info("Generated comprehensive report")
            return report

        except Exception as e:
            logger.error(f"Comprehensive report generation failed: {e}")
            raise

    def generate_visualization_report(self, data: List[Dict[str, Any]], charts: List[Dict[str, Any]], title: str = "Visualization Report") -> Dict[str, Any]:
        """
        Generate visualization report with charts and data.

        Args:
            data: Data to export
            charts: Chart configurations
            title: Report title

        Returns:
            Visualization report
        """
        try:
            # Generate HTML template with charts
            html_template = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{{ title }}</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    h1 { color: #333; }
                    .chart { width: 100%; height: 400px; margin: 20px 0; }
                    table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #f2f2f2; }
                    tr:nth-child(even) { background-color: #f9f9f9; }
                </style>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            </head>
            <body>
                <h1>{{ title }}</h1>
                {% for chart in charts %}
                    <div class="chart">
                        <canvas id="chart-{{ loop.index }}"></canvas>
                        <script>
                            document.addEventListener('DOMContentLoaded', function() {
                                var ctx = document.getElementById('chart-{{ loop.index }}').getContext('2d');
                                new Chart(ctx, {
                                    type: '{{ chart.type }}',
                                    data: {
                                        labels: {{ chart.labels | tojson }},
                                        datasets: [{
                                            label: '{{ chart.label }}',
                                            data: {{ chart.data | tojson }},
                                            backgroundColor: {{ chart.colors | tojson }},
                                            borderColor: 'rgba(75, 192, 192, 1)',
                                            borderWidth: 1
                                        }]
                                    },
                                    options: {
                                        responsive: true,
                                        scales: {
                                            y: {
                                                beginAtZero: true
                                            }
                                        }
                                    }
                                });
                            });
                        </script>
                    </div>
                {% endfor %}
                <table>
                    <thead>
                        <tr>
                            {% for key in data[0].keys() %}
                                <th>{{ key }}</th>
                            {% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in data %}
                            <tr>
                                {% for key in item.keys() %}
                                    <td>{{ item[key] }}</td>
                                {% endfor %}
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </body>
            </html>
            """

            # Render template
            template = Template(html_template)
            html_content = template.render(title=title, data=data, charts=charts)

            # Generate PDF version
            pdf_buffer = io.BytesIO()
            HTML(string=html_content).write_pdf(pdf_buffer)

            pdf_buffer.seek(0)
            pdf_data = pdf_buffer.getvalue()
            pdf_buffer.close()

            logger.info("Generated visualization report")
            return {
                "html": html_content,
                "pdf": pdf_data,
                "metadata": {
                    "title": title,
                    "item_count": len(data),
                    "chart_count": len(charts),
                    "contextual_insights": "Visualization report with charts and data"
                }
            }

        except Exception as e:
            logger.error(f"Visualization report generation failed: {e}")
            raise

    def generate_accessible_report(self, data: List[Dict[str, Any]], title: str = "Accessible Report") -> Dict[str, Any]:
        """
        Generate accessible report with ARIA labels and colorblind-friendly palettes.

        Args:
            data: Data to export
            title: Report title

        Returns:
            Accessible report
        """
        try:
            # Generate accessible HTML template
            html_template = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{{ title }}</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    h1 { color: #333; }
                    table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #f2f2f2; }
                    tr:nth-child(even) { background-color: #f9f9f9; }
                    .colorblind-friendly { color: #000; background-color: #fff; }
                    .high-contrast { color: #000; background-color: #fff; }
                </style>
            </head>
            <body>
                <h1>{{ title }}</h1>
                <table aria-label="{{ title }}">
                    <thead>
                        <tr>
                            {% for key in data[0].keys() %}
                                <th scope="col">{{ key }}</th>
                            {% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in data %}
                            <tr>
                                {% for key in item.keys() %}
                                    <td>{{ item[key] }}</td>
                                {% endfor %}
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </body>
            </html>
            """

            # Render template
            template = Template(html_template)
            html_content = template.render(title=title, data=data)

            # Generate PDF version
            pdf_buffer = io.BytesIO()
            HTML(string=html_content).write_pdf(pdf_buffer)

            pdf_buffer.seek(0)
            pdf_data = pdf_buffer.getvalue()
            pdf_buffer.close()

            logger.info("Generated accessible report")
            return {
                "html": html_content,
                "pdf": pdf_data,
                "metadata": {
                    "title": title,
                    "item_count": len(data),
                    "contextual_insights": "Accessible report with ARIA labels and colorblind-friendly palettes"
                }
            }

        except Exception as e:
            logger.error(f"Accessible report generation failed: {e}")
            raise








