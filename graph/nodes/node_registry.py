from graph.nodes.answer import DefaultAnswerNode
from graph.nodes.quality import DefaultQualityNode
from graph.nodes.classify import classify_question_node, check_rag_needed_node
from graph.nodes.base import SatisfactionNode

from graph.nodes.rag.answer import RagAnswerNode
from graph.nodes.rag.quality import SufficientNode
from graph.nodes.rag.search import search_documents_node

from graph.nodes.search.answer import WebPromptNode
from graph.nodes.search.web import search_web_node, generate_web_answer_node

class FunctionNodeWrapper:
    """
    함수형 노드를 클래스형 노드처럼 사용할 수 있도록 래핑합니다.
    """
    def __init__(self, func):
        self.func = func
    def __call__(self, state):
        return self.func(state)

NODE_REGISTRY = {
    "default_answer": DefaultAnswerNode(),
    "final_quality": DefaultQualityNode(),
    "classify_question": FunctionNodeWrapper(classify_question_node),
    "check_rag_needed": FunctionNodeWrapper(check_rag_needed_node),
    "satisfaction": SatisfactionNode(),
    "rag_answer": RagAnswerNode(),
    "sufficient": SufficientNode(),
    "search_documents": FunctionNodeWrapper(search_documents_node),
    "web_prompt": WebPromptNode(),
    "search_web": FunctionNodeWrapper(search_web_node),
    "generate_web_answer": FunctionNodeWrapper(generate_web_answer_node),
} 