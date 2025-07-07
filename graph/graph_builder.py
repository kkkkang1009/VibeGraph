from langgraph.graph import StateGraph, END
from graph.models.state import QAState
from graph.nodes.node_registry import NODE_REGISTRY
from graph.logic.decision import (
    decide_quality_next,
    decide_sufficient_next,
    decide_web_quality_next,
)

def build_graph():
    """통합 분기 QA 그래프 빌더"""
    builder = StateGraph(QAState)  # type: ignore
    
    # 1. 노드 등록
    for name, node in NODE_REGISTRY.items():
        builder.add_node(name, node)
    
    # 2. 시작점 지정
    builder.set_entry_point("classify_question")
    
    # 3. 엣지/분기 추가
    
    # (1) 분류 후 질문 유형에 따른 직접 분기
    builder.add_conditional_edges(
        "classify_question",
        lambda state: state.get("question_type", "basic"),
        {
            "web": "search_web",
            "rag": "search_documents",
            "basic": "default_answer"
        }
    )
    
    # (4) 웹 검색 플로우
    builder.add_edge("search_web", "web_quality")
    
    # (5) 웹 검색 품질 평가 결과 분기
    builder.add_conditional_edges(
        "web_quality",
        decide_web_quality_next,
        {
            "web_answer": "web_answer",
            "search_web": "search_web",
            "contextual_query_refinement": "contextual_query_refinement",
            "default_answer": "default_answer"
        }
    )
    
    # (6) 웹 답변 생성 후 품질 평가
    builder.add_edge("web_answer", "final_quality")
    
    # (7) RAG 플로우
    builder.add_edge("search_documents", "sufficient")
    
    # (8) RAG sufficient 평가 결과 분기 (재검색 또는 query 재수정)
    builder.add_conditional_edges(
        "sufficient",
        decide_sufficient_next,
        {
            "rag_answer": "rag_answer",
            "search_documents": "search_documents",
            "contextual_query_refinement": "contextual_query_refinement",
            "default_answer": "default_answer"
        }
    )
    
    # (9) RAG 답변 생성 후 품질 평가
    builder.add_edge("rag_answer", "final_quality")
    
    # (10) 기본 플로우
    builder.add_edge("default_answer", "final_quality")
    
    # (11) 품질 평가 결과 분기
    builder.add_conditional_edges(
        "final_quality",
        decide_quality_next,
        {
            "default_answer": "default_answer",
            "web_answer": "web_answer",
            "rag_answer": "rag_answer",
            "end": END
        }
    )
    
    return builder.compile()