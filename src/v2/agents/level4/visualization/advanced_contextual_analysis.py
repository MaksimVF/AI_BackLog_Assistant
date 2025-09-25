




"""
Advanced Contextual Analysis

Enhanced contextual analysis using sophisticated graph algorithms.
"""

import logging
import networkx as nx
from typing import Dict, Any, List, Optional
from crewai import Agent

logger = logging.getLogger(__name__)

class AdvancedContextualAnalysis:
    """
    Provides advanced contextual analysis using graph algorithms.
    """

    def __init__(self):
        """
        Initialize advanced contextual analysis with graph capabilities.
        """
        # Initialize CrewAI agent for advanced analysis
        self.agent = Agent(
            name="AdvancedContextualAnalysis",
            role="Advanced contextual analysis with graph algorithms",
            goal="""
                Provide sophisticated contextual understanding using graph algorithms.
                Detect complex relationships and patterns in data.
            """,
            backstory="""
                You are an advanced contextual analysis agent that uses
                sophisticated graph algorithms to detect complex relationships.
            """,
            tools=[],
            verbose=True
        )

    def analyze_relationships(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze relationships in data using graph algorithms.

        Args:
            data: Data to analyze

        Returns:
            Relationship analysis results
        """
        try:
            # Create graph from data
            graph = self._create_graph_from_data(data)

            # Run various graph algorithms
            analysis_results = {
                "centrality": self._calculate_centrality(graph),
                "communities": self._detect_communities(graph),
                "clusters": self._find_clusters(graph),
                "influencers": self._identify_influencers(graph),
                "anomalies": self._detect_anomalies(graph),
                "temporal_patterns": self._analyze_temporal_patterns(data)
            }

            logger.info("Advanced contextual analysis completed")
            return analysis_results

        except Exception as e:
            logger.error(f"Advanced contextual analysis failed: {e}")
            raise

    def _create_graph_from_data(self, data: List[Dict[str, Any]]) -> nx.Graph:
        """
        Create a graph from the data.

        Args:
            data: Data to convert to graph

        Returns:
            NetworkX graph
        """
        graph = nx.Graph()

        # Add nodes and edges based on data relationships
        for item in data:
            node_id = item.get("id", str(hash(str(item))))
            graph.add_node(node_id, **item)

            # Add relationships (simplified example)
            if "related_to" in item:
                for related_id in item["related_to"]:
                    graph.add_edge(node_id, related_id)

        return graph

    def _calculate_centrality(self, graph: nx.Graph) -> Dict[str, Any]:
        """
        Calculate centrality measures for the graph.

        Args:
            graph: NetworkX graph

        Returns:
            Centrality analysis results
        """
        return {
            "degree_centrality": nx.degree_centrality(graph),
            "betweenness_centrality": nx.betweenness_centrality(graph),
            "closeness_centrality": nx.closeness_centrality(graph),
            "eigenvector_centrality": nx.eigenvector_centrality(graph)
        }

    def _detect_communities(self, graph: nx.Graph) -> Dict[str, Any]:
        """
        Detect communities in the graph.

        Args:
            graph: NetworkX graph

        Returns:
            Community detection results
        """
        # Use Louvain method for community detection
        from networkx.algorithms.community import louvain_communities

        communities = list(louvain_communities(graph))
        return {
            "num_communities": len(communities),
            "communities": [list(community) for community in communities]
        }

    def _find_clusters(self, graph: nx.Graph) -> Dict[str, Any]:
        """
        Find clusters in the graph.

        Args:
            graph: NetworkX graph

        Returns:
            Clustering results
        """
        # Use k-clique percolation for clustering
        from networkx.algorithms.community import k_clique_communities

        clusters = list(k_clique_communities(graph, 3))
        return {
            "num_clusters": len(clusters),
            "clusters": [list(cluster) for cluster in clusters]
        }

    def _identify_influencers(self, graph: nx.Graph) -> Dict[str, Any]:
        """
        Identify influential nodes in the graph.

        Args:
            graph: NetworkX graph

        Returns:
            Influencer identification results
        """
        # Get top nodes by different centrality measures
        centrality = nx.degree_centrality(graph)
        top_influencers = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]

        return {
            "top_influencers": top_influencers,
            "influence_score": sum([score for _, score in top_influencers])
        }

    def _detect_anomalies(self, graph: nx.Graph) -> Dict[str, Any]:
        """
        Detect anomalies in the graph.

        Args:
            graph: NetworkX graph

        Returns:
            Anomaly detection results
        """
        # Simple anomaly detection based on degree
        degrees = dict(graph.degree())
        avg_degree = sum(degrees.values()) / len(degrees)

        anomalies = []
        for node, degree in degrees.items():
            if degree > avg_degree * 2:  # More than 2x average degree
                anomalies.append(node)

        return {
            "anomalies": anomalies,
            "anomaly_count": len(anomalies)
        }

    def _analyze_temporal_patterns(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze temporal patterns in the data.

        Args:
            data: Data to analyze

        Returns:
            Temporal pattern analysis results
        """
        # Group data by time periods
        from collections import defaultdict
        from datetime import datetime

        time_groups = defaultdict(list)
        for item in data:
            if "timestamp" in item:
                try:
                    dt = datetime.fromisoformat(item["timestamp"])
                    time_key = f"{dt.year}-{dt.month}"
                    time_groups[time_key].append(item)
                except:
                    continue

        # Analyze patterns over time
        patterns = {}
        for time_key, items in time_groups.items():
            patterns[time_key] = {
                "count": len(items),
                "average_value": sum(item.get("value", 0) for item in items) / len(items) if items else 0
            }

        return {
            "time_periods": len(patterns),
            "patterns": patterns
        }

    def get_insights(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get comprehensive insights from advanced analysis.

        Args:
            data: Data to analyze

        Returns:
            Comprehensive insights
        """
        # Run full analysis
        analysis = self.analyze_relationships(data)

        # Generate insights
        insights = {
            "key_influencers": analysis["influencers"]["top_influencers"],
            "important_communities": analysis["communities"]["communities"][:3],  # Top 3 communities
            "potential_anomalies": analysis["anomalies"]["anomalies"],
            "temporal_trends": analysis["temporal_patterns"]["patterns"],
            "recommendations": self._generate_recommendations(analysis)
        }

        return insights

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations based on analysis.

        Args:
            analysis: Analysis results

        Returns:
            List of recommendations
        """
        recommendations = []

        # Analyze centrality
        if analysis["centrality"]["degree_centrality"]:
            top_node = max(analysis["centrality"]["degree_centrality"].items(), key=lambda x: x[1])
            recommendations.append(f"Focus on key influencer: {top_node[0]} with highest centrality")

        # Analyze communities
        if analysis["communities"]["num_communities"] > 1:
            recommendations.append(f"Explore {analysis['communities']['num_communities']} distinct communities")

        # Analyze anomalies
        if analysis["anomalies"]["anomaly_count"] > 0:
            recommendations.append(f"Investigate {analysis['anomalies']['anomaly_count']} potential anomalies")

        # Analyze temporal patterns
        if analysis["temporal_patterns"]["time_periods"] > 1:
            recommendations.append("Analyze trends over time periods")

        return recommendations



