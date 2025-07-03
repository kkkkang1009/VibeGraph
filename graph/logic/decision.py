from graph.models.state import QAState

MAX_TRIES = 5  # 반복 제한 (필요시 조정)

def decide_quality_next(state: QAState) -> str:
    """
    통합 분기 결정 로직
    - quality_score, rag_quality_score, satisfied, tries 등 다양한 상태를 종합적으로 판단
    """
    # 품질 평가 분기
    score = state.get("quality_score")
    tries = state.get("tries", 0)

    # 1. 품질 평가 단계 (evaluate_quality)
    if tries >= MAX_TRIES or score == "fail":
        return "fail"
    if score == "good":
        return "check_satisfaction"
    elif score == "regenerate":
        return "generate_answer"
    elif score == "search_more":
        return "search_documents"
    else:
        return "generate_answer"  # fallback

def decide_rag_quality_next(state: QAState) -> str:
    """
    통합 분기 결정 로직
    - quality_score, rag_quality_score, satisfied, tries 등 다양한 상태를 종합적으로 판단
    """
    # 2. RAG 품질 평가 단계 (check_rag_quality)
    rag_score = state.get("rag_quality_score")
    if rag_score == "satisfied":
        return "satisfied"
    elif rag_score == "search_more":
        return "search_more"
    elif rag_score == "regenerate":
        return "regenerate"
    else:
        return "regenerate"  # fallback

def decide_satisfaction_next(state: QAState) -> str:
    """
    통합 분기 결정 로직
    - quality_score, rag_quality_score, satisfied, tries 등 다양한 상태를 종합적으로 판단
    """
    # 3. 최종 만족도 확인 단계 (check_satisfaction)
    satisfied = state.get("satisfied", False)
    tries = state.get("tries", 0)
    print(f"[DEBUG][decide_satisfaction_next] satisfied={satisfied}, tries={tries}")
    if satisfied:
        print("[DEBUG][decide_satisfaction_next] return 'end'")
        return "end"
    elif tries >= 3:
        print("[DEBUG][decide_satisfaction_next] return 'end' (tries)")
        return "end"
    else:
        print("[DEBUG][decide_satisfaction_next] return 'generate_answer'")
        return "generate_answer"

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