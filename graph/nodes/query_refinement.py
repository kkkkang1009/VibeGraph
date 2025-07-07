from graph.nodes.base import BaseNode
from graph.models.state import QAState
from graph.config import llm
from graph.prompts.templates import prompt_builder

class QueryRefinementNode(BaseNode):
    """
    최초 질문을 더 구체적이고 명확하게 수정하는 노드
    """
    
    def build_prompt(self, state: QAState) -> str:
        question = state.get("question", "")
        return prompt_builder.build_query_refinement_prompt(question)
    
    def __call__(self, state: QAState) -> QAState:
        prompt = self.build_prompt(state)
        refined_question = llm.predict(prompt).strip()
        
        # 원본 질문과 수정된 질문을 모두 저장
        return {
            **state, 
            "original_question": state.get("question", ""),
            "question": refined_question,
            "query_refined": True
        }

class ContextualQueryRefinementNode(BaseNode):
    """
    질문 유형에 따라 컨텍스트를 고려하여 질문을 수정하는 노드
    """
    
    def build_prompt(self, state: QAState) -> str:
        question = state.get("question", "")
        question_type = state.get("question_type") or "basic"
        return prompt_builder.build_contextual_query_refinement_prompt(question, question_type)
    
    def __call__(self, state: QAState) -> QAState:
        prompt = self.build_prompt(state)
        refined_question = llm.predict(prompt).strip()
        
        # RAG 재시도인지 확인 (rag_search_tries가 1 이상이면 재시도)
        rag_search_tries = state.get("rag_search_tries", 0) or 0
        is_rag_retry = rag_search_tries >= 1
        
        # 웹 검색 재시도인지 확인 (web_search_tries가 1 이상이면 재시도)
        web_search_tries = state.get("web_search_tries", 0) or 0
        is_web_retry = web_search_tries >= 1
        
        return {
            **state, 
            "original_question": state.get("question", ""),
            "question": refined_question,
            "query_refined": True,
            "refinement_type": "contextual",
            "is_rag_retry": is_rag_retry,  # RAG 재시도 플래그 추가
            "is_web_retry": is_web_retry   # 웹 검색 재시도 플래그 추가
        } 