from graph.models.state import QAState

def classify_question(state: QAState) -> str:
    """질문 유형에 따라 분기 결정 (웹, 역사, 수학, 번역, 일반)"""
    question = state["question"]

    # 웹 검색이 필요한 키워드
    web_keywords = ["검색", "인터넷", "웹", "구글", "뉴스", "실시간", "site:", "최신"]
    rag_keywords = ["최신", "2024", "최근", "현재", "실시간"]

    if any(web in question for web in web_keywords):
        return "web"
    elif any(rag in question for rag in rag_keywords):
        return "rag"
    else:
        return "basic"

def should_use_rag(state: QAState) -> bool:
    """RAG 사용 여부 결정"""
    question = state["question"].lower()
    
    # 특정 키워드가 있으면 RAG 사용
    rag_keywords = ["최신", "2024", "최근", "현재", "실시간"]
    return any(keyword in question for keyword in rag_keywords) 