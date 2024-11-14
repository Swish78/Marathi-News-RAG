from typing import List
import networkx as nx
from langchain.vectorstores import Chroma


class GraphBuilder:
    def __init__(self):
        self.graph = nx.Graph()

    def build_graph(self, chunks: List[str], embeddings: Chroma) -> nx.Graph:
        # Adding Nodes
        for i, chunk in enumerate(chunks):
            self.graph.add_node(i, text=chunk)

        # Adding edges based on similarity
        for i in range(len(chunks)):
            results = embeddings.similarity_search_with_score(chunks[i], k=3)
            for doc, score in results:
                if score > 0.7:
                    j = chunks.index(doc.page_content)
                    if i != j:
                        self.graph.add_edge(i, j, weight=score)

        return self.graph

    def get_important_chunks(self, top_k: int = 3) -> List[str]:
        pagerank = nx.pagerank(self.graph)
        important_nodes = sorted(
            [(node, score) for node, score in pagerank.items()],
            key=lambda x: x[1],
            reverse=True
        )[:top_k]
        return [self.graph.nodes[node]['text'] for node, _ in important_nodes]
