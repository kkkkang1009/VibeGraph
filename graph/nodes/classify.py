from graph.models.state import QAState
from graph.logic.classification import classify_question, should_use_rag

def classify_question_node(state: QAState) -> QAState:
    """
    질문 분류 결과를 상태에 저장하는 노드
    """
    return {**state, "question_type": classify_question(state)}

def check_rag_needed_node(state: QAState) -> QAState:
    """
    RAG 사용 여부를 상태에 저장하는 노드
    """
    return {**state, "use_rag": should_use_rag(state)} 