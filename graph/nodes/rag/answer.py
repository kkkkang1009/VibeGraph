from graph.nodes.base import AnswerNode
from graph.utils import format_documents

class RagAnswerNode(AnswerNode):
    def build_prompt(self, state):
        question = state["question"]
        documents = state.get("retrieved_documents", [])
        if documents:
            context = format_documents(documents)
            return f"다음 문서를 참고하여 질문에 답해주세요:\n\n문서:\n{context}\n\n질문: {question}"
        else:
            return f"질문에 답해주세요: {question}" 