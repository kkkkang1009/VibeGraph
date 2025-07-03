from graph.nodes.base import QualityNode
from graph.config import llm

MAX_TRIES = 5  # 예시

class DefaultQualityNode(QualityNode):
    def build_prompt(self, state):
        answer = state.get("answer", "")
        question = state["question"]
        # 최종 answer(최종 답변)의 품질만 평가
        return f"""
        다음 최종 답변의 품질을 평가해주세요:
        질문: {question}
        답변: {answer}
        평가 기준:
        1. 답변이 질문에 적절히 답하는가?
        2. 답변이 충분히 상세하고 명확한가?
        3. 답변이 신뢰할 만한가?
        결과를 다음 중 하나로 답해주세요:
        - 'good': 품질이 좋음
        - 'regenerate': 답변 재생성 필요
        """
    def update_state(self, state, result):
        # 최종 answer 품질만 평가
        if "good" in result:
            score = "good"
        elif "regenerate" in result:
            score = "regenerate"
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
            "needs_regeneration": "regenerate" in score
        } 