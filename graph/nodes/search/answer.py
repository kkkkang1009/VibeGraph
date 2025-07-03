from graph.nodes.base import AnswerNode

class WebPromptNode(AnswerNode):
    def build_prompt(self, state):
        question = state.get("question", "")
        web_results = state.get("web_search_results", [])
        if web_results:
            context = "\n".join([f"{r['title']}: {r['snippet']}" for r in web_results])
            return f"다음 웹 검색 결과를 참고해서 질문에 답해주세요:\n{context}\n\n질문: {question}"
        else:
            return f"질문에 답해주세요: {question}" 