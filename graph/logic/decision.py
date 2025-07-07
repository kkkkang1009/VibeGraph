import logging
from graph.models.state import QAState
from langgraph.graph import END  # 추가

MAX_TRIES = 5  # 반복 제한 (필요시 조정)

logger = logging.getLogger(__name__)

def decide_next(state: QAState, score_key: str, mapping: dict, tries_limit: int = MAX_TRIES) -> str:
    score = state.get(score_key)
    tries = state.get("tries", 0)
    if tries >= tries_limit or score == "fail":
        return "fail"
    return mapping.get(score, "generate_answer")


def decide_quality_next(state: QAState) -> str:
    """
    통합 분기 결정 로직 (quality_score)
    답변 유형(basic/web/rag)에 따라 regenerate 분기 시 각각의 생성 노드로 분기
    """
    score = state.get("quality_score")
    qtype = state.get("question_type", "basic")
    if score == "regenerate":
        if qtype == "rag":
            return "rag_answer"
        elif qtype == "web":
            return "generate_web_answer"
        else:
            return "default_answer"
    elif score == "good" or score == "fail":
        return "end"
    else:
        return "default_answer"


def decide_sufficient_next(state: QAState) -> str:
    """
    RAG sufficient 평가 결과 분기 (sufficient_score)
    단계적 접근: 재검색 → query 재수정 → 다른 전략
    """
    score = state.get("sufficient_score")
    tries = state.get("rag_search_tries", 0)
    
    if score == "sufficient":
        return "rag_answer"
    elif score == "needs_more_search":
        # 단계적 접근
        if tries == 0:
            # 첫 번째 시도: 같은 query로 재검색
            return "search_documents"
        elif tries == 1:
            # 두 번째 시도: query 재수정 후 검색
            return "contextual_query_refinement"
        else:
            # 세 번째 이상: 다른 검색 전략 또는 기본 답변
            return "default_answer"
    else:
        return "search_documents"  # fallback


def decide_web_quality_next(state: QAState) -> str:
    """
    웹 검색 품질 평가 결과 분기 (web_quality_score)
    단계적 접근: 재검색 → query 재수정 → 다른 전략
    """
    score = state.get("web_quality_score")
    tries = state.get("web_search_tries", 0)
    
    if score == "sufficient":
        return "web_answer"
    elif score == "needs_more_search":
        # 단계적 접근
        if tries == 0:
            # 첫 번째 시도: 같은 query로 재검색
            return "search_web"
        elif tries == 1:
            # 두 번째 시도: query 재수정 후 검색
            return "contextual_query_refinement"
        else:
            # 세 번째 이상: 다른 검색 전략 또는 기본 답변
            return "default_answer"
    elif score == "refine_query":
        # query 재수정이 필요한 경우
        return "contextual_query_refinement"
    else:
        return "web_answer"  # fallback

# 미사용 함수 (향후 확장 시 사용 가능)
# def decide_satisfaction_next(state: QAState) -> str:
#     """
#     통합 분기 결정 로직 (satisfied)
#     """
#     satisfied = state.get("satisfied", False)
#     tries = state.get("tries", 0)
#     logger.debug(f"[decide_satisfaction_next] satisfied={satisfied}, tries={tries}")
#     if satisfied or tries >= 3:
#         logger.debug("[decide_satisfaction_next] return 'end'")
#         return "end"
#     else:
#         logger.debug("[decide_satisfaction_next] return 'generate_answer'")
#         return "generate_answer"

# 미사용 함수 (향후 확장 시 사용 가능)
# def get_retry_strategy(state: QAState) -> str:
#     """반복 횟수에 따른 전략 결정"""
#     tries = state["tries"]
#     
#     if tries == 1:
#         return "detailed_answer"  # 첫 번째: 상세 답변
#     elif tries == 2:
#         return "simple_answer"    # 두 번째: 간단 답변
#     else:
#         return "end"              # 세 번째: 종료 