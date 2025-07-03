from graph.models.state import QAState
from typing import List, Dict
from graph.utils.search import perform_web_search, perform_news_search, perform_wikipedia_search, remove_duplicates
from graph.config import llm
from .base_node import AnswerNode

class WebAnswerNode(AnswerNode):
    def build_prompt(self, state):
        question = state["question"]
        web_results = state.get("web_search_results", [])
        if web_results:
            context = "\n".join([f"{r['title']}: {r['snippet']}" for r in web_results])
            return f"다음 웹 검색 결과를 참고해서 질문에 답해주세요:\n{context}\n\n질문: {question}"
        else:
            return f"질문에 답해주세요: {question}"

def search_web_node(state: QAState) -> QAState:
    """온라인 웹 검색 노드"""
    question = state["question"]
    
    # 웹 검색 실행
    search_results = perform_web_search(question)
    
    return {
        **state,
        "web_search_results": search_results,
        "search_type": "web"
    }

def answer_with_web_search_node(state: QAState) -> QAState:
    """웹 검색 결과를 활용한 답변 생성 노드"""
    question = state["question"]
    web_results = state.get("web_search_results", [])
    if web_results:
        context = "\n".join([f"{r['title']}: {r['snippet']}" for r in web_results])
        prompt = f"다음 웹 검색 결과를 참고해서 질문에 답해줘:\n{context}\n\n질문: {question}"
    else:
        prompt = f"질문에 답해줘: {question}"
    response = llm.predict(prompt)
    print(f"[DEBUG] 웹검색 답변 생성: {response}")
    return {**state, "answer": response}

# 미사용 노드들 (향후 확장 시 사용)
# def search_news_node(state: QAState) -> QAState:
#     """뉴스 검색 노드"""
#     question = state["question"]
#     
#     # 뉴스 검색 실행
#     news_results = perform_news_search(question)
#     
#     return {
#         **state,
#         "news_search_results": news_results,
#         "search_type": "news"
#     }

# def search_wikipedia_node(state: QAState) -> QAState:
#     """위키피디아 검색 노드"""
#     question = state["question"]
#     
#     # 위키피디아 검색 실행
#     wiki_results = perform_wikipedia_search(question)
#     
#     return {
#         **state,
#         "wikipedia_results": wiki_results,
#         "search_type": "wikipedia"
#     }

# def combine_search_results_node(state: QAState) -> QAState:
#     """여러 검색 결과를 통합하는 노드"""
#     web_results = state.get("web_search_results", []) or []
#     news_results = state.get("news_search_results", []) or []
#     wiki_results = state.get("wikipedia_results", []) or []
#     
#     # 모든 검색 결과 통합
#     combined_results = []
#     combined_results.extend(web_results)
#     combined_results.extend(news_results)
#     combined_results.extend(wiki_results)
#     
#     # 중복 제거 및 정렬
#     unique_results = remove_duplicates(combined_results)
#     
#     return {
#         **state,
#         "combined_search_results": unique_results,
#         "total_search_results": len(unique_results)
#     } 