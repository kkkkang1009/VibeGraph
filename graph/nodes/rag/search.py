from graph.models.state import QAState
from graph.utils import search_documents

def search_documents_node(state: QAState) -> QAState:
    """
    문서 검색 노드
    """
    if state.get("search_type") != "rag":
        return state
    
    # RAG 검색 시도 횟수 추적
    current_tries = state.get("rag_search_tries", 0)
    
    search_query = state.get("question", "")
    documents = search_documents(search_query)
    
    return {
        **state,
        "retrieved_documents": documents,
        "search_query": search_query,
        "document_sources": ["source1", "source2"],
        "rag_search_tries": current_tries + 1
    } 