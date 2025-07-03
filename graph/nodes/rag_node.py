from graph.config import llm
from graph.models.state import QAState
from graph.utils import search_documents, format_documents
from .base_node import AnswerNode, QualityNode

def search_documents_node(state: QAState) -> QAState:
    """문서 검색 노드"""
    if not state.get("use_rag", False):
        return state
    
    # 문서 검색 로직
    search_query = state["question"]
    documents = search_documents(search_query)
    
    return {
        **state,
        "retrieved_documents": documents,
        "search_query": search_query,
        "document_sources": ["source1", "source2"]
    }

class RagAnswerNode(AnswerNode):
    def build_prompt(self, state):
        question = state["question"]
        documents = state.get("retrieved_documents", [])
        if documents:
            context = format_documents(documents)
            return f"다음 문서를 참고하여 질문에 답해주세요:\n\n문서:\n{context}\n\n질문: {question}"
        else:
            return f"질문에 답해주세요: {question}"

class RagQualityNode(QualityNode):
    def build_prompt(self, state):
        answer = state["answer"]
        documents = state.get("retrieved_documents", [])
        return f"""
        다음 RAG 답변의 품질을 평가해주세요:
        질문: {state['question']}
        답변: {answer}
        사용된 문서 수: {len(documents) if documents else 0}
        평가 기준:
        1. 답변이 질문에 적절히 답하는가?
        2. 문서 정보가 충분히 활용되었는가?
        3. 더 많은 문서가 필요한가?
        결과를 다음 중 하나로 답해주세요:
        - 'satisfied': 만족함
        - 'regenerate': 같은 문서로 재생성 필요
        - 'search_more': 더 많은 문서 검색 필요
        """
    def update_state(self, state, result):
        if "satisfied" in result.lower():
            rag_score = "satisfied"
        elif "search_more" in result.lower():
            rag_score = "search_more"
        elif "regenerate" in result.lower():
            rag_score = "regenerate"
        else:
            rag_score = "regenerate"  # fallback
        return {
            **state,
            "rag_quality_score": rag_score,
            "needs_more_search": rag_score == "search_more",
            "needs_regeneration": rag_score == "regenerate"
        }

