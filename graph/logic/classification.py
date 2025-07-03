WEB_KEYWORDS = ["검색", "인터넷", "웹", "구글", "뉴스", "실시간", "site:"]
RAG_KEYWORDS = ["최신", "2024", "최근", "현재", "실시간"]

from graph.models.state import QAState

def classify_question(state: QAState) -> str:
    """질문 유형에 따라 분기 결정 (웹, RAG, 일반)"""
    question = state["question"]

    if any(web in question for web in WEB_KEYWORDS):
        return "web"
    elif any(rag in question for rag in RAG_KEYWORDS):
        return "rag"
    else:
        return "basic"

def should_use_rag(state: QAState) -> bool:
    """RAG 사용 여부 결정"""
    question = state["question"].lower()
    return any(keyword in question for keyword in RAG_KEYWORDS) 