from graph.models.state import QAState
from graph.utils import search_documents

def search_documents_node(state: QAState) -> QAState:
    """
    문서 검색 노드
    """
    if not state.get("use_rag", False):
        return state
    search_query = state["question"]
    documents = search_documents(search_query)
    return {
        **state,
        "retrieved_documents": documents,
        "search_query": search_query,
        "document_sources": ["source1", "source2"]
    } 