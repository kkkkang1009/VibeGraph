from graph.config import llm
from graph.models.state import QAState
from graph.logic.classification import classify_question, should_use_rag
from .base_node import AnswerNode, QualityNode, SatisfactionNode

MAX_TRIES = 5  # 예시

class BasicAnswerNode(AnswerNode):
    def build_prompt(self, state):
        question = state["question"]
        return f"질문에 답해줘. 질문: {question}"

class BasicQualityNode(QualityNode):
    def build_prompt(self, state):
        answer = state.get("answer", "")
        question = state["question"]
        return f"""
        다음 답변의 품질을 평가해주세요:
        질문: {question}
        답변: {answer}
        평가 기준:
        1. 답변이 질문에 적절히 답하는가?
        2. 답변이 충분히 상세한가?
        3. 답변이 정확한가?
        결과를 다음 중 하나로 답해주세요:
        - 'good': 품질이 좋음
        - 'regenerate': 재생성 필요
        - 'search_more': 더 많은 정보 검색 필요
        """
    def update_state(self, state, result):
        if "good" in result:
            score = "good"
        elif "regenerate" in result:
            score = "regenerate"
        elif "search_more" in result:
            score = "search_more"
        else:
            score = "good"  # fallback
        if state["tries"] >= MAX_TRIES:
            return {
                **state,
                "quality_score": "fail",
                "error": "답변이 5회 조건을 만족하지 못했습니다. 반복 중단."
            }
        return {
            **state,
            "quality_score": score,
            "needs_regeneration": "regenerate" in score,
            "needs_more_search": "search_more" in score
        }

class BasicSatisfactionNode(SatisfactionNode):
    pass

def classify_question_node(state: QAState) -> QAState:
    """질문 분류 결과를 상태에 저장하는 노드"""
    return {**state, "question_type": classify_question(state)}

def check_rag_needed_node(state: QAState) -> QAState:
    """RAG 사용 여부를 상태에 저장하는 노드"""
    return {**state, "use_rag": should_use_rag(state)}