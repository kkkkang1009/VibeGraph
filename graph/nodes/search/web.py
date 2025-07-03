from graph.models.state import QAState
from graph.utils.search import perform_web_search
from graph.config import llm

def search_web_node(state: QAState) -> QAState:
    """
    온라인 웹 검색 노드
    """
    question = state.get("question", "")
    search_results = perform_web_search(question)
    return {
        **state,
        "web_search_results": search_results,
        "search_type": "web"
    }

def generate_web_answer_node(state: QAState) -> QAState:
    """
    웹 검색 결과를 활용한 답변 생성 노드
    """
    question = state.get("question", "")
    web_results = state.get("web_search_results", [])
    if web_results:
        context = "\n".join([f"{r['title']}: {r['snippet']}" for r in web_results])
        prompt = f"다음 웹 검색 결과를 참고해서 질문에 답해줘:\n{context}\n\n질문: {question}"
    else:
        prompt = f"질문에 답해줘: {question}"
    response = llm.predict(prompt)
    print(f"[DEBUG] 웹검색 답변 생성: {response}")
    return {**state, "answer": response} 