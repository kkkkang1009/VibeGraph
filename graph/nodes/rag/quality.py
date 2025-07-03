from graph.nodes.base import QualityNode

class SufficientNode(QualityNode):
    def build_prompt(self, state):
        documents = state.get("retrieved_documents", [])
        question = state["question"]
        # RAG 검색 결과(문서)의 품질 및 답변 생성 가능성 평가
        return f"""
        다음은 질문에 대해 검색된 문서 목록입니다.
        질문: {question}
        검색된 문서 수: {len(documents) if documents else 0}
        평가 기준:
        1. 문서들이 질문에 충분히 관련이 있는가?
        2. 정보가 다양하고 신뢰할 만한가?
        3. 이 문서들만으로 질문에 대한 답변을 생성할 수 있는가?
        4. 더 많은 문서가 필요한가?
        결과를 다음 중 하나로 답해주세요:
        - 'sufficient': 문서가 충분히 적합하고, 답변 생성이 가능함
        - 'search_more': 더 많은 문서 검색 필요
        """
    def update_state(self, state, result):
        # RAG 검색 결과(문서) 품질 및 답변 생성 가능성만 평가
        if "sufficient" in result.lower():
            sufficient_score = "sufficient"
        elif "search_more" in result.lower():
            sufficient_score = "search_more"
        else:
            sufficient_score = "search_more"  # fallback
        return {
            **state,
            "sufficient_score": sufficient_score,
            "needs_more_search": sufficient_score == "search_more"
        } 