from langgraph.graph import StateGraph, END
from graph.models.state import QAState
from graph.nodes.node_registry import NODE_REGISTRY
from graph.logic.decision import (
    decide_quality_next,
    decide_sufficient_next,
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
    
    # (1) 분류 플로우
    builder.add_conditional_edges(
        "classify_question",
        lambda state: state.get("question_type", "basic"),
        {
            "web": "search_web",
            "rag": "search_documents",
            "basic": "generate_answer"
        }
    )
    
    # (2) 웹 검색 플로우
    builder.add_edge("search_web", "web_prompt")
    
    # (3) RAG 플로우
    builder.add_edge("search_documents", "generate_rag_answer")
    builder.add_edge("generate_rag_answer", "sufficient")
    
    # (4) 기본 플로우
    builder.add_edge("generate_answer", "final_quality")
    
    # (5) 품질 평가 결과 분기
    builder.add_conditional_edges(
        "final_quality",
        decide_quality_next,
        {
            "generate_answer": "generate_answer",
            "generate_web_answer": "generate_web_answer",
            "generate_rag_answer": "generate_rag_answer",
            "end": "end"
        }
    )
    
    # (6) RAG sufficient 평가 결과 분기
    builder.add_conditional_edges(
        "sufficient",
        decide_sufficient_next,
        {
            "sufficient": "generate_rag_answer",
            "search_more": "search_documents"
        }
    )
    
    return builder.compile()