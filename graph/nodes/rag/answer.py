from graph.nodes.base import AnswerNode
from graph.prompts.templates import prompt_builder

class RagAnswerNode(AnswerNode):
    def build_prompt(self, state):
        question = state["question"]
        documents = state.get("retrieved_documents", [])
        return prompt_builder.build_rag_answer_prompt(question, documents) 