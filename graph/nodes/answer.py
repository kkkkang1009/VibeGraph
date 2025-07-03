from graph.nodes.base import AnswerNode

class DefaultAnswerNode(AnswerNode):
    def build_prompt(self, state):
        question = state["question"]
        return f"질문에 답해주세요. 질문: {question}" 