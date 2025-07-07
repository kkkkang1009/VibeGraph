"""
프롬프트 템플릿 중앙 관리 모듈
모든 노드에서 사용하는 프롬프트들을 한 곳에서 관리합니다.
"""

from typing import Dict, Any, Optional


class PromptTemplates:
    """프롬프트 템플릿들을 중앙에서 관리하는 클래스"""
    
    # 질문 정제 관련 프롬프트
    QUERY_REFINEMENT = """
다음 질문을 더 구체적이고 명확하게 수정해주세요. 
수정된 질문은 더 정확한 답변을 얻을 수 있도록 구체적이고 명확해야 합니다.

원본 질문: {question}

수정 시 고려사항:
1. 모호한 표현을 구체적으로 변경
2. 필요한 세부사항 추가
3. 질문의 의도를 명확히 표현
4. 검색이나 답변에 도움이 되는 키워드 포함

수정된 질문만 출력하세요:
"""

    CONTEXTUAL_QUERY_REFINEMENT = """
질문 유형: {question_type}

다음 질문을 {refinement_guide}

원본 질문: {question}

수정된 질문만 출력하세요:
"""

    # 답변 생성 관련 프롬프트
    DEFAULT_ANSWER = "질문에 답해주세요. 질문: {question}"
    
    WEB_ANSWER_WITH_CONTEXT = """다음 웹 검색 결과를 참고해서 질문에 답해줘:
{context}

질문: {question}"""

    WEB_ANSWER_WITHOUT_CONTEXT = "질문에 답해줘: {question}"
    
    RAG_ANSWER_WITH_DOCUMENTS = """다음 문서를 참고하여 질문에 답해주세요:

문서:
{documents}

질문: {question}"""
    
    RAG_ANSWER_WITHOUT_DOCUMENTS = "질문에 답해주세요: {question}"
    
    # 품질 평가 관련 프롬프트
    ANSWER_QUALITY_EVALUATION = """
다음 최종 답변의 품질을 평가해주세요:
질문: {question}
답변: {answer}
평가 기준:
1. 답변이 질문에 적절히 답하는가?
2. 답변이 충분히 상세하고 명확한가?
3. 답변이 신뢰할 만한가?
결과를 다음 중 하나로 답해주세요:
- 'good': 품질이 좋음
- 'regenerate': 답변 재생성 필요
"""

    RAG_SUFFICIENCY_EVALUATION = """
다음은 질문에 대해 검색된 문서 목록입니다.
질문: {question}
검색된 문서 수: {document_count}
평가 기준:
1. 문서들이 질문에 충분히 관련이 있는가?
2. 정보가 다양하고 신뢰할 만한가?
3. 이 문서들만으로 질문에 대한 답변을 생성할 수 있는가?
4. 더 많은 문서가 필요한가?
결과를 다음 중 하나로 답해주세요:
- 'sufficient': 문서가 충분히 적합하고, 답변 생성이 가능함
- 'needs_more_search': 더 많은 문서 검색 필요
"""

    # 질문 유형별 정제 가이드
    REFINEMENT_GUIDES = {
        "web": "웹 검색에 최적화된 질문으로 수정하세요. 검색 엔진에서 찾기 쉬운 키워드를 포함하고, 구체적인 정보를 요청하는 형태로 만들어주세요.",
        "rag": "문서 검색에 최적화된 질문으로 수정하세요. 관련 문서를 찾기 쉬운 키워드를 포함하고, 문서 내용을 기반으로 답변할 수 있는 형태로 만들어주세요.",
        "basic": "일반적인 대화형 질문으로 수정하세요. 명확하고 이해하기 쉬운 형태로 만들어주세요."
    }

    @classmethod
    def get_refinement_guide(cls, question_type: str) -> str:
        """질문 유형에 따른 정제 가이드를 반환합니다."""
        return cls.REFINEMENT_GUIDES.get(question_type, cls.REFINEMENT_GUIDES["basic"])

    @classmethod
    def format_prompt(cls, template: str, **kwargs) -> str:
        """프롬프트 템플릿을 포맷팅합니다."""
        return template.format(**kwargs)


class PromptBuilder:
    """프롬프트를 동적으로 구성하는 빌더 클래스"""
    
    def __init__(self):
        self.templates = PromptTemplates()
    
    def build_query_refinement_prompt(self, question: str) -> str:
        """질문 정제 프롬프트를 생성합니다."""
        return self.templates.format_prompt(
            self.templates.QUERY_REFINEMENT,
            question=question
        )
    
    def build_contextual_query_refinement_prompt(self, question: str, question_type: str = "basic") -> str:
        """컨텍스트 기반 질문 정제 프롬프트를 생성합니다."""
        refinement_guide = self.templates.get_refinement_guide(question_type)
        return self.templates.format_prompt(
            self.templates.CONTEXTUAL_QUERY_REFINEMENT,
            question=question,
            question_type=question_type,
            refinement_guide=refinement_guide
        )
    
    def build_web_answer_prompt(self, question: str, web_results: Optional[list] = None) -> str:
        """웹 검색 기반 답변 프롬프트를 생성합니다."""
        if web_results:
            context = "\n".join([f"{r['title']}: {r['snippet']}" for r in web_results])
            return self.templates.format_prompt(
                self.templates.WEB_ANSWER_WITH_CONTEXT,
                context=context,
                question=question
            )
        else:
            return self.templates.format_prompt(
                self.templates.WEB_ANSWER_WITHOUT_CONTEXT,
                question=question
            )
    
    def build_rag_answer_prompt(self, question: str, documents: Optional[list] = None) -> str:
        """RAG 기반 답변 프롬프트를 생성합니다."""
        if documents:
            from graph.utils import format_documents
            formatted_docs = format_documents(documents)
            return self.templates.format_prompt(
                self.templates.RAG_ANSWER_WITH_DOCUMENTS,
                documents=formatted_docs,
                question=question
            )
        else:
            return self.templates.format_prompt(
                self.templates.RAG_ANSWER_WITHOUT_DOCUMENTS,
                question=question
            )
    
    def build_default_answer_prompt(self, question: str) -> str:
        """기본 답변 프롬프트를 생성합니다."""
        return self.templates.format_prompt(
            self.templates.DEFAULT_ANSWER,
            question=question
        )
    
    def build_answer_quality_prompt(self, question: str, answer: str) -> str:
        """답변 품질 평가 프롬프트를 생성합니다."""
        return self.templates.format_prompt(
            self.templates.ANSWER_QUALITY_EVALUATION,
            question=question,
            answer=answer
        )
    
    def build_rag_sufficiency_prompt(self, question: str, documents: Optional[list] = None) -> str:
        """RAG 충분성 평가 프롬프트를 생성합니다."""
        document_count = len(documents) if documents else 0
        return self.templates.format_prompt(
            self.templates.RAG_SUFFICIENCY_EVALUATION,
            question=question,
            document_count=document_count
        )
    
    def build_web_search_quality_prompt(self, question: str, web_results: Optional[list] = None) -> str:
        """웹 검색 결과 품질 평가 프롬프트를 생성합니다."""
        if web_results:
            context = "\n".join([f"{r.get('title', '')}: {r.get('snippet', '')}" for r in web_results])
            return f"""다음 웹 검색 결과를 평가해주세요:
질문: {question}
검색 결과:
{context}

평가 기준:
1. 검색 결과가 질문과 관련이 있는가?
2. 정보가 충분하고 신뢰할 만한가?
3. 이 결과들로 질문에 답변할 수 있는가?

결과를 다음 중 하나로 답해주세요:
- 'sufficient': 충분한 정보가 있음
- 'refine_query': 질문을 더 구체적으로 수정하거나 더 많은 검색이 필요함"""
        else:
            return f"""질문에 대한 웹 검색 결과가 없습니다.
질문: {question}

결과를 다음 중 하나로 답해주세요:
- 'refine_query': 질문을 더 구체적으로 수정하거나 더 많은 검색이 필요함"""


# 전역 인스턴스 생성
prompt_builder = PromptBuilder() 