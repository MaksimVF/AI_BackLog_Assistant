








"""
Network Graph Generator

Generates advanced network graphs for visualization.
"""

import logging
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict, Any, Optional
from crewai import Agent

logger = logging.getLogger(__name__)

class NetworkGraphGenerator:
    """
    Generates network graphs for visualization with advanced capabilities.
    """

    def __init__(self):
        """
        Initialize network graph generator with CrewAI agent.
        """
        # Initialize CrewAI agent for network graph generation
        self.agent = Agent(
            name="NetworkGraphGenerator",
            role="Network graph generator for visualization",
            goal="""
                Generate network graphs for visualization.
                Provide advanced network visualization capabilities.
            """,
            backstory="""
                You are a network graph generator that uses
                advanced graph algorithms for visualization.
            """,
            tools=[],
            verbose=True
        )

    def generate_network_graph(self, data: List[Dict[str, Any]], graph_type: str = "basic") -> Dict[str, Any]:
        """
        Generate network graph from data.

        Args:
            data: Data to visualize
            graph_type: Type of network graph

        Returns:
            Network graph visualization
        """
        try:
            # Create graph from data
            graph = self._create_graph_from_data(data)

            # Generate graph based on type
            if graph_type == "basic":
                return self._generate_basic_graph(graph)
            elif graph_type == "community":
                return self._generate_community_graph(graph)
            elif graph_type == "centrality":
                return self._generate_centrality_graph(graph)
            elif graph_type == "3d":
                return self._generate_3d_graph(graph)
            else:
                return self._generate_basic_graph(graph)

        except Exception as e:
            logger.error(f"Network graph generation failed: {e}")
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

    def _generate_basic_graph(self, graph: nx.Graph) -> Dict[str, Any]:
        """
        Generate basic network graph.

        Args:
            graph: NetworkX graph

        Returns:
            Basic network graph visualization
        """
        try:
            # Generate basic visualization
            pos = nx.spring_layout(graph)
            plt.figure(figsize=(10, 8))
            nx.draw(graph, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10)
            plt.title("Basic Network Graph")

            # Save to buffer
            import io
            buffer = io.BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)

            return {
                "graph_type": "basic",
                "image_data": buffer.getvalue(),
                "metadata": {
                    "nodes": len(graph.nodes),
                    "edges": len(graph.edges),
                    "contextual_insights": "Basic network graph with relationships"
                }
            }

        except Exception as e:
            logger.error(f"Basic graph generation failed: {e}")
            raise

    def _generate_community_graph(self, graph: nx.Graph) -> Dict[str, Any]:
        """
        Generate community network graph.

        Args:
            graph: NetworkX graph

        Returns:
            Community network graph visualization
        """
        try:
            # Detect communities
            from networkx.algorithms.community import louvain_communities
            communities = list(louvain_communities(graph))

            # Assign colors to communities
            colors = ["red", "blue", "green", "yellow", "purple", "orange"]
            community_colors = {}
            for i, community in enumerate(communities):
                for node in community:
                    community_colors[node] = colors[i % len(colors)]

            # Generate visualization
            pos = nx.spring_layout(graph)
            plt.figure(figsize=(10, 8))
            nx.draw(graph, pos, with_labels=True, node_size=500,
                   node_color=[community_colors[node] for node in graph.nodes],
                   font_size=10)
            plt.title("Community Network Graph")

            # Save to buffer
            import io
            buffer = io.BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)

            return {
                "graph_type": "community",
                "image_data": buffer.getvalue(),
                "metadata": {
                    "nodes": len(graph.nodes),
                    "edges": len(graph.edges),
                    "communities": len(communities),
                    "contextual_insights": "Community network graph with detected communities"
                }
            }

        except Exception as e:
            logger.error(f"Community graph generation failed: {e}")
            raise

    def _generate_centrality_graph(self, graph: nx.Graph) -> Dict[str, Any]:
        """
        Generate centrality network graph.

        Args:
            graph: NetworkX graph

        Returns:
            Centrality network graph visualization
        """
        try:
            # Calculate centrality
            centrality = nx.degree_centrality(graph)
            node_sizes = [centrality[node] * 1000 for node in graph.nodes]

            # Generate visualization
            pos = nx.spring_layout(graph)
            plt.figure(figsize=(10, 8))
            nx.draw(graph, pos, with_labels=True, node_size=node_sizes,
                   node_color="skyblue", font_size=10)
            plt.title("Centrality Network Graph")

            # Save to buffer
            import io
            buffer = io.BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)

            return {
                "graph_type": "centrality",
                "image_data": buffer.getvalue(),
                "metadata": {
                    "nodes": len(graph.nodes),
                    "edges": len(graph.edges),
                    "centrality": centrality,
                    "contextual_insights": "Centrality network graph with node importance"
                }
            }

        except Exception as e:
            logger.error(f"Centrality graph generation failed: {e}")
            raise

    def _generate_3d_graph(self, graph: nx.Graph) -> Dict[str, Any]:
        """
        Generate 3D network graph.

        Args:
            graph: NetworkX graph

        Returns:
            3D network graph visualization
        """
        try:
            # Generate 3D visualization
            from mpl_toolkits.mplot3d import Axes3D

            pos = nx.spring_layout(graph, dim=3)
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')

            # Draw nodes
            for node, (x, y, z) in pos.items():
                ax.scatter(x, y, z, s=500, c='skyblue', edgecolors='k')

            # Draw edges
            for (u, v) in graph.edges:
                x = [pos[u][0], pos[v][0]]
                y = [pos[u][1], pos[v][1]]
                z = [pos[u][2], pos[v][2]]
                ax.plot(x, y, z, c='gray', alpha=0.5)

            # Set labels
            for node, (x, y, z) in pos.items():
                ax.text(x, y, z, str(node), fontsize=10)

            ax.set_title("3D Network Graph")

            # Save to buffer
            import io
            buffer = io.BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)

            return {
                "graph_type": "3d",
                "image_data": buffer.getvalue(),
                "metadata": {
                    "nodes": len(graph.nodes),
                    "edges": len(graph.edges),
                    "contextual_insights": "3D network graph with spatial relationships"
                }
            }

        except Exception as e:
            logger.error(f"3D graph generation failed: {e}")
            raise

    def generate_network_analysis(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate network analysis from data.

        Args:
            data: Data to analyze

        Returns:
            Network analysis results
        """
        try:
            # Create graph from data
            graph = self._create_graph_from_data(data)

            # Run network analysis
            analysis = {
                "centrality": nx.degree_centrality(graph),
                "betweenness": nx.betweenness_centrality(graph),
                "closeness": nx.closeness_centrality(graph),
                "communities": list(nx.algorithms.community.louvain_communities(graph)),
                "density": nx.density(graph),
                "average_clustering": nx.average_clustering(graph)
            }

            return {
                "network_analysis": analysis,
                "metadata": {
                    "nodes": len(graph.nodes),
                    "edges": len(graph.edges),
                    "contextual_insights": "Comprehensive network analysis"
                }
            }

        except Exception as e:
            logger.error(f"Network analysis failed: {e}")
            raise

    def generate_network_insights(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate network insights from data.

        Args:
            data: Data to analyze

        Returns:
            Network insights
        """
        try:
            # Create graph from data
            graph = self._create_graph_from_data(data)

            # Run network analysis
            analysis = self.generate_network_analysis(data)

            # Generate insights
            insights = {
                "key_influencers": self._identify_key_influencers(analysis["network_analysis"]["centrality"]),
                "important_communities": self._identify_important_communities(analysis["network_analysis"]["communities"]),
                "network_health": self._assess_network_health(analysis["network_analysis"]),
                "recommendations": self._generate_network_recommendations(analysis["network_analysis"])
            }

            return {
                "network_insights": insights,
                "metadata": {
                    "nodes": len(graph.nodes),
                    "edges": len(graph.edges),
                    "contextual_insights": "Network insights with recommendations"
                }
            }

        except Exception as e:
            logger.error(f"Network insights generation failed: {e}")
            raise

    def _identify_key_influencers(self, centrality: Dict[str, float]) -> List[str]:
        """
        Identify key influencers from centrality.

        Args:
            centrality: Centrality scores

        Returns:
            List of key influencers
        """
        # Get top influencers
        sorted_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        return [node for node, score in sorted_centrality[:5]]

    def _identify_important_communities(self, communities: List[List[str]]) -> List[Dict[str, Any]]:
        """
        Identify important communities.

        Args:
            communities: List of communities

        Returns:
            List of important communities
        """
        # Get largest communities
        sorted_communities = sorted(communities, key=lambda x: len(x), reverse=True)
        return [{"community": list(community), "size": len(community)} for community in sorted_communities[:3]]

    def _assess_network_health(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess network health.

        Args:
            analysis: Network analysis results

        Returns:
            Network health assessment
        """
        # Assess network health
        density = analysis["density"]
        avg_clustering = analysis["average_clustering"]

        health = "healthy" if density > 0.3 and avg_clustering > 0.3 else "moderate" if density > 0.1 else "weak"

        return {
            "health": health,
            "density": density,
            "average_clustering": avg_clustering
        }

    def _generate_network_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Generate network recommendations.

        Args:
            analysis: Network analysis results

        Returns:
            List of recommendations
        """
        recommendations = []

        # Generate recommendations based on analysis
        if analysis["density"] < 0.3:
            recommendations.append("Consider adding more connections to improve network density")

        if analysis["average_clustering"] < 0.3:
            recommendations.append("Consider strengthening community clusters")

        if len(analysis["communities"]) > 5:
            recommendations.append("Consider merging similar communities")

        return recommendations






