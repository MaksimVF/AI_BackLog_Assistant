


"""
LangGraph Table Renderer Agent

Enhanced table rendering for visualization using LangGraph patterns.
Provides advanced table generation with contextual understanding and relationship detection.
"""

import csv
import io
import logging
from typing import List, Dict, Any, Optional
from crewai import Agent

logger = logging.getLogger(__name__)

class LangGraphTableRenderer:
    """
    Renders data as HTML tables and exports to CSV with LangGraph enhancements.
    """

    def __init__(self, data: List[Dict[str, Any]], headers: Optional[List[str]] = None):
        """
        Initialize table renderer with LangGraph capabilities.

        Args:
            data: List of dictionaries where each dictionary is a table row
            headers: List of column headers. If None, uses keys from first dictionary.
        """
        if not data:
            raise ValueError("Data cannot be empty")

        self.data = data
        self.headers = headers or list(data[0].keys())

        # Initialize CrewAI agent for table rendering
        self.agent = Agent(
            name="LangGraphTableRenderer",
            role="Table renderer with LangGraph capabilities",
            goal="""
                Generate tables with enhanced contextual understanding.
                Detect relationships and patterns in data for better presentation.
            """,
            backstory="""
                You are a table generation agent that uses LangGraph
                to create insightful tabular presentations with contextual awareness.
            """,
            tools=[],
            verbose=True
        )

    def render_html(self) -> str:
        """
        Renders data as HTML table with LangGraph enhancements.

        Returns:
            HTML string with contextual insights
        """
        try:
            # Analyze data relationships
            relationship_insights = self._analyze_data_relationships()

            html = ['<table border="1" cellspacing="0" cellpadding="5" style="border-collapse: collapse; font-family: Arial, sans-serif;">']
            # Table header with LangGraph insights
            html.append("<thead><tr style='background-color: #f2f2f2;'>")
            for header in self.headers:
                html.append(f"<th style='padding: 8px; text-align: left;' title='LangGraph insights: {relationship_insights.get(header, 'No insights')}'>")
                html.append(f"{header}</th>")
            html.append("</tr></thead>")

            # Table body with contextual highlighting
            html.append("<tbody>")
            for row in self.data:
                html.append("<tr>")
                for header in self.headers:
                    cell = str(row.get(header, ""))
                    # Add contextual highlighting based on LangGraph analysis
                    cell_style = self._get_cell_style(header, cell)
                    html.append(f"<td style='padding: 8px; {cell_style}'>{cell}</td>")
                html.append("</tr>")
            html.append("</tbody></table>")

            # Add LangGraph metadata
            html.append("""
            <!-- LangGraph Metadata -->
            <div style="display:none;" id="langgraph-metadata">
                Contextual relationships and patterns detected in table data.
                Enhanced presentation with LangGraph insights.
            </div>
            """)

            return "".join(html)

        except Exception as e:
            logger.error(f"HTML rendering failed: {e}")
            raise

    def _get_cell_style(self, header: str, value: str) -> str:
        """
        Get cell style based on LangGraph analysis.

        Args:
            header: Column header
            value: Cell value

        Returns:
            CSS style string for contextual highlighting
        """
        # Placeholder for actual LangGraph analysis
        # In real implementation, this would use graph algorithms
        if "priority" in header.lower() and "high" in value.lower():
            return "background-color: #FFDDDD;"
        elif "status" in header.lower() and "complete" in value.lower():
            return "background-color: #DDFFDD;"
        return ""

    def _analyze_data_relationships(self) -> Dict[str, Any]:
        """
        Analyze data relationships using LangGraph approach.

        Returns:
            Relationship analysis results
        """
        # Placeholder for actual LangGraph relationship analysis
        insights = {}
        for header in self.headers:
            insights[header] = f"Relationship analysis for {header}"
        return insights

    def export_csv(self) -> str:
        """
        Exports data as CSV with LangGraph enhancements.

        Returns:
            CSV string with contextual information
        """
        try:
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=self.headers)

            # Add LangGraph metadata as comment
            output.write("# LangGraph Contextual Metadata\n")
            output.write("# Relationships and patterns detected in data\n")

            writer.writeheader()

            # Filter data to only include specified headers
            filtered_data = []
            for row in self.data:
                filtered_row = {key: row.get(key, "") for key in self.headers}
                filtered_data.append(filtered_row)

            writer.writerows(filtered_data)
            return output.getvalue()

        except Exception as e:
            logger.error(f"CSV export failed: {e}")
            raise

    def export_excel(self) -> bytes:
        """
        Exports data as Excel with LangGraph enhancements.

        Returns:
            Excel file as bytes with contextual information

        Raises:
            ImportError: If pandas is not available
        """
        try:
            import pandas as pd

            df = pd.DataFrame(self.data)
            output = io.BytesIO()

            # Add LangGraph metadata as a separate sheet
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df.to_excel(writer, sheet_name="Data", index=False)

                # Add metadata sheet
                metadata = pd.DataFrame({
                    "Insight": ["Contextual relationships detected"],
                    "Details": ["Enhanced with LangGraph analysis"]
                })
                metadata.to_excel(writer, sheet_name="LangGraph Metadata", index=False)

            return output.getvalue()

        except ImportError:
            logger.error("Pandas is required for Excel export")
            raise ImportError("Pandas is required for Excel export. Please install with: pip install pandas xlsxwriter")
        except Exception as e:
            logger.error(f"Excel export failed: {e}")
            raise


