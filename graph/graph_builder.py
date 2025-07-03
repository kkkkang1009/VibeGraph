from langgraph.graph import StateGraph, END
from graph.models.state import QAState
from graph.nodes.basic_nodes import BasicAnswerNode, BasicQualityNode, BasicSatisfactionNode, classify_question_node
from graph.nodes.rag_node import search_documents_node, RagAnswerNode, RagQualityNode
from graph.nodes.search_node import search_web_node, WebAnswerNode
from graph.logic.decision import (
    decide_quality_next,
    decide_rag_quality_next,
    decide_satisfaction_next,
)

def build_graph():
    """통합 분기 QA 그래프 빌더"""
    builder = StateGraph(QAState)  # type: ignore
    
    # 기본 노드들
    builder.add_node("generate_answer", BasicAnswerNode())
    builder.add_node("check_satisfaction", BasicSatisfactionNode())
    builder.add_node("evaluate_quality", BasicQualityNode())
    builder.add_node("classify_question", classify_question_node)
    
    # RAG 노드들
    builder.add_node("search_documents", search_documents_node)
    builder.add_node("generate_rag_answer", RagAnswerNode())
    builder.add_node("check_rag_quality", RagQualityNode())
    
    # 웹 검색 노드들
    builder.add_node("search_web", search_web_node)
    builder.add_node("answer_with_web_search", WebAnswerNode())
    
    # 시작점 설정
    builder.set_entry_point("classify_question")
    
    # 분류 결과에 따라 플로우 분기 (web, rag, basic)
    builder.add_conditional_edges("classify_question", lambda state: state.get("question_type", "basic"), {
        "web": "search_web",
        "rag": "search_documents",
        "basic": "generate_answer"
    })
    
    # 웹 검색 플로우
    builder.add_edge("search_web", "answer_with_web_search")
    builder.add_edge("answer_with_web_search", "check_satisfaction")
    
    # RAG 플로우
    builder.add_edge("search_documents", "generate_rag_answer")
    builder.add_edge("generate_rag_answer", "check_rag_quality")
    
    # 기본 플로우
    builder.add_edge("generate_answer", "evaluate_quality")
    
    # 품질 평가 결과에 따른 분기
    builder.add_conditional_edges("evaluate_quality", decide_quality_next, {
        "check_satisfaction": "check_satisfaction",
        "generate_answer": "generate_answer",
        "search_documents": "search_documents",
        "fail": END
    })
    
    # RAG 품질 확인 결과에 따른 분기
    builder.add_conditional_edges("check_rag_quality", decide_rag_quality_next, {
        "satisfied": "check_satisfaction",
        "search_more": "search_documents",
        "regenerate": "generate_rag_answer"
    })
    
    # 최종 만족도 확인 및 종료 결정
    builder.add_conditional_edges("check_satisfaction", decide_satisfaction_next, {
        "generate_answer": "generate_answer",
        "end": END
    })
    
    return builder.compile()