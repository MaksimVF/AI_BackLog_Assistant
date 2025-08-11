




from typing import List, Dict, Tuple
import spacy
import networkx as nx

class KnowledgeGraphAgent:
    """
    KnowledgeGraphAgent: Строит граф знаний из текста.

    Извлекает сущности (Named Entities), строит граф знаний из текста,
    может связывать сущности между собой и с внешними базами (при необходимости),
    используется для последующего логического и смыслового обогащения данных.
    """

    def __init__(self):
        # Initialize spaCy model
        try:
            self.nlp = spacy.load("ru_core_news_lg")  # Use large model if available
        except OSError:
            try:
                self.nlp = spacy.load("ru_core_news_sm")  # Fallback to small model
            except OSError:
                raise ImportError("Russian spaCy model not found. Please install with: python -m spacy download ru_core_news_sm")
        self.graph = nx.DiGraph()

    def extract_entities_and_relations(self, text: str) -> Tuple[List[str], List[Tuple[str, str, str]]]:
        """
        Извлекает сущности и простые отношения (subject - verb - object) из текста.

        Args:
            text: Входной текст.

        Returns:
            Кортеж: (список сущностей, список триплетов отношений).
        """
        doc = self.nlp(text)
        entities = list({ent.text for ent in doc.ents})

        relations = []
        for sent in doc.sents:
            subject, verb, obj = None, None, None
            for token in sent:
                if token.dep_ in ("nsubj", "nsubjpass"):
                    subject = token.text
                elif token.dep_ == "ROOT":
                    verb = token.text
                elif token.dep_ in ("obj", "dobj", "pobj"):  # Added 'obj' for Russian
                    obj = token.text
            if subject and verb and obj:
                relations.append((subject, verb, obj))

        return entities, relations

    def build_graph(self, text: str) -> Dict:
        """
        Строит граф знаний на основе извлечённых сущностей и связей.

        Args:
            text: Входной текст.

        Returns:
            Структуру графа в виде словаря.
        """
        entities, relations = self.extract_entities_and_relations(text)

        # Clear previous graph
        self.graph.clear()

        # Add nodes and edges
        for entity in entities:
            self.graph.add_node(entity)

        for subj, verb, obj in relations:
            self.graph.add_edge(subj, obj, label=verb)

        # Convert to dictionary representation
        return {
            "entities": list(self.graph.nodes()),
            "relations": [(u, self.graph.edges[u, v]["label"], v) for u, v in self.graph.edges()]
        }




