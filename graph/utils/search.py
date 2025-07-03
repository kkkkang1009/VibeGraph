from typing import List, Dict
import requests
import os

def search_documents(query: str) -> list[str]:
    """문서 검색 함수"""
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string.")
    # 실제 문서 검색 로직 구현 필요
    # 임시로 더미 데이터 반환
    return [f"문서1: {query}에 대한 정보", f"문서2: {query} 관련 내용"]

def perform_web_search(query: str) -> List[Dict]:
    """웹 검색 실행 (실제 구현 필요)"""
    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CSE_ID")
    if not api_key or not cx:
        raise EnvironmentError("Google API key or CSE ID is not set.")
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string.")
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
        "num": 5,  # 결과 개수
        "hl": "ko"
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    items = resp.json().get("items", [])
    results = []
    for item in items:
        results.append({
            "title": item.get("title"),
            "snippet": item.get("snippet"),
            "url": item.get("link"),
            "source": "web"
        })
    return results

def perform_news_search(query: str) -> List[Dict]:
    """뉴스 검색 실행 (실제 구현 필요)"""
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string.")
    # 실제로는 News API, Google News 등 사용
    return [
        {
            "title": f"뉴스 검색 결과: {query}",
            "snippet": f"{query}에 대한 최신 뉴스입니다.",
            "url": "https://news.example.com",
            "source": "news"
        }
    ]

def perform_wikipedia_search(query: str) -> List[Dict]:
    """위키피디아 검색 실행 (실제 구현 필요)"""
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string.")
    # 실제로는 Wikipedia API 사용
    return [
        {
            "title": f"위키피디아: {query}",
            "snippet": f"{query}에 대한 위키피디아 정보입니다.",
            "url": "https://wikipedia.org",
            "source": "wikipedia"
        }
    ]

def remove_duplicates(results: List[Dict]) -> List[Dict]:
    """중복 결과 제거"""
    seen = set()
    unique_results = []
    for result in results:
        key = (result.get("url"), result.get("title"), result.get("snippet"))
        if key not in seen:
            seen.add(key)
            unique_results.append(result)
    return unique_results 