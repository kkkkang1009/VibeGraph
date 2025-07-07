from graph.models.state import QAState
from graph.utils.search import perform_web_search
from graph.config import llm
from graph.prompts.templates import prompt_builder

def search_web_node(state: QAState) -> QAState:
    """
    온라인 웹 검색 노드
    """
    if state.get("search_type") != "web":
        return state
    
    # 웹 검색 시도 횟수 추적
    current_tries = state.get("web_search_tries", 0) or 0
    
    question = state.get("question", "")
    search_results = perform_web_search(question)
    return {
        **state,
        "web_search_results": search_results,
        "search_type": "web",
        "web_search_tries": current_tries + 1
    }

def web_answer_node(state: QAState) -> QAState:
    """
    웹 검색 결과를 활용한 답변 생성 노드
    """
    question = state.get("question", "")
    web_results = state.get("web_search_results", [])
    prompt = prompt_builder.build_web_answer_prompt(question, web_results)
    response = llm.predict(prompt)
    print(f"[DEBUG] 웹검색 답변 생성: {response}")
    return {**state, "answer": response} 