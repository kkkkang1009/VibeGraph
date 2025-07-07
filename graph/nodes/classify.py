from graph.models.state import QAState
from graph.logic.classification import classify_question

def classify_question_node(state: QAState) -> QAState:
    """
    질문 분류 결과를 상태에 저장하는 노드
    """
    return classify_question(state) 