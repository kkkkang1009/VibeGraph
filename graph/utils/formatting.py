def format_documents(documents: list[str]) -> str:
    """문서들을 포맷팅하는 함수"""
    return "\n".join([f"- {doc}" for doc in documents])

def extract_keywords(text: str) -> list[str]:
    """텍스트에서 키워드 추출"""
    # 간단한 키워드 추출 로직
    words = text.split()
    return [word for word in words if len(word) > 2] 