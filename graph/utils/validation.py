def validate_question(question: str) -> bool:
    """
    질문 유효성 검사 (비어있지 않고, 물음표 포함)
    """
    if not isinstance(question, str):
        raise TypeError("질문은 문자열이어야 합니다.")
    if len(question.strip()) == 0:
        return False
    if "?" not in question:
        return False
    # 추가 검증 포인트: 금지어, 길이 제한 등
    return True 