















"""
Advanced Dashboard Generator

Generates advanced dashboards with customizable layouts and drill-down capabilities.
"""

import logging
import json
from typing import List, Dict, Any, Optional
from crewai import Agent

logger = logging.getLogger(__name__)

class AdvancedDashboardGenerator:
    """
    Generates advanced dashboards with customizable layouts and drill-down capabilities.
    """

    def __init__(self):
        """
        Initialize advanced dashboard generator with CrewAI agent.
        """
        # Initialize CrewAI agent for advanced dashboard generation
        self.agent = Agent(
            name="AdvancedDashboardGenerator",
            role="Advanced dashboard generator for visualization",
            goal="""
                Generate advanced dashboards with customizable layouts and drill-down capabilities.
                Provide comprehensive dashboard generation for visualization.
            """,
            backstory="""
                You are an advanced dashboard generator that uses
                sophisticated techniques to create comprehensive dashboards.
            """,
            tools=[],
            verbose=True
        )

    def generate_dashboard(self, data: List[Dict[str, Any]], layout: str = "grid", title: str = "Advanced Dashboard") -> Dict[str, Any]:
        """
        Generate advanced dashboard with customizable layout.

        Args:
            data: Data to visualize
            layout: Dashboard layout
            title: Dashboard title

        Returns:
            Advanced dashboard
        """
        try:
            # Generate dashboard based on layout
            if layout == "grid":
                return self._generate_grid_dashboard(data, title)
            elif layout == "flex":
                return self._generate_flex_dashboard(data, title)
            elif layout == "tabbed":
                return self._generate_tabbed_dashboard(data, title)
            else:
                return self._generate_grid_dashboard(data, title)

        except Exception as e:
            logger.error(f"Dashboard generation failed: {e}")
            raise

    def _generate_grid_dashboard(self, data: List[Dict[str, Any]], title: str) -> Dict[str, Any]:
        """
        Generate grid layout dashboard.

        Args:
            data: Data to visualize
            title: Dashboard title

        Returns:
            Grid layout dashboard
        """
        try:
            # Generate grid layout HTML
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
                    .grid-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
                    .grid-item { background-color: #f9f9f9; padding: 20px; border-radius: 5px; }
                    .grid-item h2 { color: #555; }
                </style>
            </head>
            <body>
                <h1>{{ title }}</h1>
                <div class="grid-container">
                    {% for item in data %}
                        <div class="grid-item">
                            <h2>{{ item.title }}</h2>
                            <p>Priority: {{ item.priority }}</p>
                            <p>Category: {{ item.category }}</p>
                            <p>Value: {{ item.value }}</p>
                        </div>
                    {% endfor %}
                </div>
            </body>
            </html>
            """

            # Render template
            from jinja2 import Template
            template = Template(html_template)
            html_content = template.render(title=title, data=data)

            logger.info("Generated grid layout dashboard")
            return {
                "html": html_content,
                "layout": "grid",
                "metadata": {
                    "contextual_insights": "Grid layout dashboard with customizable layout",
                    "item_count": len(data)
                }
            }

        except Exception as e:
            logger.error(f"Grid layout dashboard generation failed: {e}")
            raise

    def _generate_flex_dashboard(self, data: List[Dict[str, Any]], title: str) -> Dict[str, Any]:
        """
        Generate flex layout dashboard.

        Args:
            data: Data to visualize
            title: Dashboard title

        Returns:
            Flex layout dashboard
        """
        try:
            # Generate flex layout HTML
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
                    .flex-container { display: flex; flex-wrap: wrap; gap: 20px; }
                    .flex-item { background-color: #f9f9f9; padding: 20px; border-radius: 5px; flex: 1 1 300px; }
                    .flex-item h2 { color: #555; }
                </style>
            </head>
            <body>
                <h1>{{ title }}</h1>
                <div class="flex-container">
                    {% for item in data %}
                        <div class="flex-item">
                            <h2>{{ item.title }}</h2>
                            <p>Priority: {{ item.priority }}</p>
                            <p>Category: {{ item.category }}</p>
                            <p>Value: {{ item.value }}</p>
                        </div>
                    {% endfor %}
                </div>
            </body>
            </html>
            """

            # Render template
            from jinja2 import Template
            template = Template(html_template)
            html_content = template.render(title=title, data=data)

            logger.info("Generated flex layout dashboard")
            return {
                "html": html_content,
                "layout": "flex",
                "metadata": {
                    "contextual_insights": "Flex layout dashboard with customizable layout",
                    "item_count": len(data)
                }
            }

        except Exception as e:
            logger.error(f"Flex layout dashboard generation failed: {e}")
            raise

    def _generate_tabbed_dashboard(self, data: List[Dict[str, Any]], title: str) -> Dict[str, Any]:
        """
        Generate tabbed layout dashboard.

        Args:
            data: Data to visualize
            title: Dashboard title

        Returns:
            Tabbed layout dashboard
        """
        try:
            # Generate tabbed layout HTML
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
                    .tab-container { display: flex; flex-direction: column; }
                    .tab-buttons { display: flex; gap: 10px; margin-bottom: 20px; }
                    .tab-button { padding: 10px 20px; background-color: #f0f0f0; border: none; cursor: pointer; }
                    .tab-button.active { background-color: #ddd; }
                    .tab-content { display: none; padding: 20px; background-color: #f9f9f9; border-radius: 5px; }
                    .tab-content.active { display: block; }
                </style>
            </head>
            <body>
                <h1>{{ title }}</h1>
                <div class="tab-container">
                    <div class="tab-buttons">
                        {% for i in range(data|length) %}
                            <button class="tab-button" onclick="showTab({{ i }})">Item {{ i+1 }}</button>
                        {% endfor %}
                    </div>
                    {% for i in range(data|length) %}
                        <div class="tab-content" id="tab-{{ i }}">
                            <h2>{{ data[i].title }}</h2>
                            <p>Priority: {{ data[i].priority }}</p>
                            <p>Category: {{ data[i].category }}</p>
                            <p>Value: {{ data[i].value }}</p>
                        </div>
                    {% endfor %}
                </div>
                <script>
                    function showTab(index) {
                        // Hide all tabs
                        const tabs = document.querySelectorAll('.tab-content');
                        tabs.forEach(tab => tab.classList.remove('active'));

                        // Show selected tab
                        const selectedTab = document.getElementById('tab-' + index);
                        selectedTab.classList.add('active');

                        // Update button styles
                        const buttons = document.querySelectorAll('.tab-button');
                        buttons.forEach((button, i) => {
                            if (i === index) {
                                button.classList.add('active');
                            } else {
                                button.classList.remove('active');
                            }
                        });
                    }

                    // Show first tab by default
                    showTab(0);
                </script>
            </body>
            </html>
            """

            # Render template
            from jinja2 import Template
            template = Template(html_template)
            html_content = template.render(title=title, data=data)

            logger.info("Generated tabbed layout dashboard")
            return {
                "html": html_content,
                "layout": "tabbed",
                "metadata": {
                    "contextual_insights": "Tabbed layout dashboard with customizable layout",
                    "item_count": len(data)
                }
            }

        except Exception as e:
            logger.error(f"Tabbed layout dashboard generation failed: {e}")
            raise

    def generate_drilldown_dashboard(self, data: List[Dict[str, Any]], title: str = "Drilldown Dashboard") -> Dict[str, Any]:
        """
        Generate dashboard with drill-down capabilities.

        Args:
            data: Data to visualize
            title: Dashboard title

        Returns:
            Dashboard with drill-down capabilities
        """
        try:
            # Generate drill-down dashboard HTML
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
                    .drilldown-container { display: flex; flex-direction: column; gap: 20px; }
                    .drilldown-item { background-color: #f9f9f9; padding: 20px; border-radius: 5px; cursor: pointer; }
                    .drilldown-item h2 { color: #555; }
                    .drilldown-details { display: none; margin-top: 10px; padding: 10px; background-color: #fff; border: 1px solid #ddd; }
                </style>
            </head>
            <body>
                <h1>{{ title }}</h1>
                <div class="drilldown-container">
                    {% for item in data %}
                        <div class="drilldown-item" onclick="toggleDetails({{ loop.index }})">
                            <h2>{{ item.title }}</h2>
                            <div class="drilldown-details" id="details-{{ loop.index }}">
                                <p>Priority: {{ item.priority }}</p>
                                <p>Category: {{ item.category }}</p>
                                <p>Value: {{ item.value }}</p>
                            </div>
                        </div>
                    {% endfor %}
                </div>
                <script>
                    function toggleDetails(index) {
                        const details = document.getElementById('details-' + index);
                        if (details.style.display === 'none' || details.style.display === '') {
                            details.style.display = 'block';
                        } else {
                            details.style.display = 'none';
                        }
                    }
                </script>
            </body>
            </html>
            """

            # Render template
            from jinja2 import Template
            template = Template(html_template)
            html_content = template.render(title=title, data=data)

            logger.info("Generated drill-down dashboard")
            return {
                "html": html_content,
                "layout": "drilldown",
                "metadata": {
                    "contextual_insights": "Dashboard with drill-down capabilities",
                    "item_count": len(data)
                }
            }

        except Exception as e:
            logger.error(f"Drill-down dashboard generation failed: {e}")
            raise

    def generate_customizable_dashboard(self, data: List[Dict[str, Any]], layout: str = "grid", title: str = "Customizable Dashboard") -> Dict[str, Any]:
        """
        Generate customizable dashboard with various layout options.

        Args:
            data: Data to visualize
            layout: Dashboard layout
            title: Dashboard title

        Returns:
            Customizable dashboard
        """
        try:
            # Generate customizable dashboard
            dashboard = self.generate_dashboard(data, layout, title)

            # Add customization options
            customization_options = {
                "layout_options": ["grid", "flex", "tabbed"],
                "theme_options": ["light", "dark", "high-contrast"],
                "color_options": ["default", "colorblind-friendly", "pastel"],
                "interaction_options": ["click", "hover", "drill-down"]
            }

            # Add customization metadata
            dashboard["customization_options"] = customization_options
            dashboard["metadata"]["customizable"] = True

            logger.info("Generated customizable dashboard")
            return dashboard

        except Exception as e:
            logger.error(f"Customizable dashboard generation failed: {e}")
            raise

    def generate_dashboard_insights(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate dashboard insights.

        Args:
            data: Data to analyze

        Returns:
            Dashboard insights
        """
        try:
            # Generate insights
            insights = {
                "data_quality": "high",
                "dashboard_insights": "Comprehensive dashboard with advanced capabilities",
                "recommendations": self._generate_dashboard_recommendations(data),
                "metadata": {
                    "contextual_insights": "Dashboard insights with recommendations",
                    "insight_level": "advanced"
                }
            }

            logger.info("Generated dashboard insights")
            return insights

        except Exception as e:
            logger.error(f"Dashboard insights generation failed: {e}")
            raise

    def _generate_dashboard_recommendations(self, data: List[Dict[str, Any]]) -> List[str]:
        """
        Generate dashboard recommendations.

        Args:
            data: Data to analyze

        Returns:
            List of dashboard recommendations
        """
        # Generate recommendations
        recommendations = [
            "Use grid layout for better organization",
            "Consider drill-down capabilities for detailed analysis",
            "Implement customizable layouts for different use cases"
        ]

        return recommendations

    def generate_dashboard_report(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate comprehensive dashboard report.

        Args:
            data: Data to analyze

        Returns:
            Dashboard report
        """
        try:
            # Generate report
            report = {
                "data": data,
                "insights": self.generate_dashboard_insights(data),
                "metadata": {
                    "contextual_insights": "Comprehensive dashboard report",
                    "report_level": "advanced"
                }
            }

            logger.info("Generated dashboard report")
            return report

        except Exception as e:
            logger.error(f"Dashboard report generation failed: {e}")
            raise

    def get_dashboard_recommendations(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get dashboard recommendations.

        Args:
            data: Data to analyze

        Returns:
            Dashboard recommendations
        """
        try:
            # Generate recommendations
            recommendations = {
                "dashboard_recommendations": [
                    "Use customizable layouts for better organization",
                    "Implement drill-down capabilities for detailed analysis",
                    "Consider different themes for better accessibility"
                ],
                "metadata": {
                    "contextual_insights": "Dashboard recommendations for better visualization",
                    "recommendation_level": "advanced"
                }
            }

            logger.info("Generated dashboard recommendations")
            return recommendations

        except Exception as e:
            logger.error(f"Dashboard recommendations generation failed: {e}")
            raise













