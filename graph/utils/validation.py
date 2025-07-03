def validate_question(question: str) -> bool:
    """질문 유효성 검사"""
    return len(question.strip()) > 0 and "?" in question 