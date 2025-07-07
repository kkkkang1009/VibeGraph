from graph.nodes.base import QualityNode
from graph.prompts.templates import prompt_builder

class SufficientNode(QualityNode):
    def build_prompt(self, state):
        documents = state.get("retrieved_documents", [])
        question = state["question"]
        return prompt_builder.build_rag_sufficiency_prompt(question, documents)
        
    def update_state(self, state, result):
        # RAG 검색 결과(문서) 품질 및 답변 생성 가능성만 평가
        if "sufficient" in result.lower():
            sufficient_score = "sufficient"
        elif "search_more" in result.lower():
            sufficient_score = "needs_more_search"
        else:
            sufficient_score = "needs_more_search"  # fallback
        return {
            **state,
            "sufficient_score": sufficient_score,
            "needs_more_search": sufficient_score == "needs_more_search"
        } 