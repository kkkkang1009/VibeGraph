from graph.nodes.base import QualityNode
from graph.prompts.templates import prompt_builder

class WebSearchQualityNode(QualityNode):
    """
    웹 검색 결과의 품질을 평가하는 노드
    """
    
    def build_prompt(self, state):
        question = state.get("question", "")
        web_results = state.get("web_search_results", [])
        return prompt_builder.build_web_search_quality_prompt(question, web_results)
        
    def update_state(self, state, result):
        # 웹 검색 결과 품질 평가
        if "sufficient" in result.lower():
            web_quality_score = "sufficient"
        elif "refine_query" in result.lower():
            web_quality_score = "refine_query"
        else:
            web_quality_score = "sufficient"  # fallback
            
        return {
            **state,
            "web_quality_score": web_quality_score,
            "needs_query_refinement": web_quality_score == "refine_query",
            "needs_more_search": web_quality_score == "refine_query"  # refine_query일 때도 더 많은 검색이 필요할 수 있음
        } 