WEB_KEYWORDS = [
    "검색", "인터넷", "웹", "구글", "뉴스",
    "실시간", "site:", "날씨", "유튜브", "2025"
]

RAG_KEYWORDS = [
    "문서", "정책", "가이드", "설명서", "내부",
    "자료", "FAQ", "매뉴얼", "매거진", "백서"
]

from graph.models.state import QAState

def classify_question(state: QAState) -> QAState:
    """질문 유형에 따라 분기 결정하고 search_type 설정"""
    question = state.get("question", "")
    
    # 검색 타입 초기화
    search_type = None
    question_type = "basic"
    
    # 키워드 기반 분류
    if any(web in question for web in WEB_KEYWORDS):
        search_type = "web"
        question_type = "web"
    elif any(rag in question for rag in RAG_KEYWORDS):
        search_type = "rag"
        question_type = "rag"
    
    return {
        **state,
        "search_type": search_type,
        "question_type": question_type
    }

def should_use_rag(state: QAState) -> bool:
    """RAG 사용 여부 결정"""
    search_type = state.get("search_type")
    return search_type == "rag"

def should_use_web(state: QAState) -> bool:
    """웹 검색 사용 여부 결정"""
    search_type = state.get("search_type")
    return search_type == "web" 