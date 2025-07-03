from typing import TypedDict, Optional, List, Dict

class QAState(TypedDict):
    question: str
    answer: Optional[str]
    satisfied: Optional[bool]
    tries: int
    retrieved_documents: Optional[List[str]]
    document_sources: Optional[List[str]]
    search_query: Optional[str]
    use_rag: bool
    quality_score: Optional[str]
    needs_regeneration: Optional[bool]
    needs_more_search: Optional[bool]
    question_type: Optional[str]  # 질문 분류 결과
    rag_quality_score: Optional[str]  # RAG 품질 점수
    # 온라인 검색 관련 필드들
    web_search_results: Optional[List[Dict]]
    search_type: Optional[str]  # 검색 유형 (web, news, wikipedia, combined)
    error: Optional[str]  # 에러 메시지 