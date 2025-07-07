from graph.nodes.base import AnswerNode
from graph.prompts.templates import prompt_builder

class WebPromptNode(AnswerNode):
    def build_prompt(self, state):
        question = state.get("question", "")
        web_results = state.get("web_search_results", [])
        return prompt_builder.build_web_answer_prompt(question, web_results) 