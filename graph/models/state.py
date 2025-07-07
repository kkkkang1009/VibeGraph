from typing import TypedDict, Optional, List, Dict

class QAState(TypedDict, total=False):
    # 필수 필드 (Required fields)
    question: str  # 질문 (Question)
    tries: int     # 시도 횟수 (Number of tries)

    # 선택 필드 (Optional fields)
    answer: Optional[str]  # 답변 (Answer)
    search_type: Optional[str]                # 검색 유형 (Search type: web, news, wikipedia, combined)
    satisfied: Optional[bool]                 # 만족 여부 (Satisfaction)
    error: Optional[str]                      # 에러 메시지 (Error message) 
    # RAG Node
    retrieved_documents: Optional[List[str]]  # 검색된 문서 리스트 (Retrieved documents)
    document_sources: Optional[List[str]]     # 문서 출처 리스트 (Document sources)
    search_query: Optional[str]               # 검색 쿼리 (Search query)
    quality_score: Optional[str]              # 품질 평가 점수 (Quality score)
    needs_regeneration: Optional[bool]        # 답변 재생성 필요 여부 (Needs regeneration)
    needs_more_search: Optional[bool]         # 추가 검색 필요 여부 (Needs more search)
    question_type: Optional[str]              # 질문 분류 결과 (Question type: web, rag, basic)
    sufficient_score: Optional[str]           # RAG sufficient 평가 점수 (RAG sufficient score)
    # Web Node
    web_search_results: Optional[List[Dict]]  # 웹 검색 결과 (Web search results)