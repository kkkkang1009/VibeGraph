from graph.config import llm

class BaseNode:
    def __call__(self, state):
        raise NotImplementedError("모든 노드는 __call__을 구현해야 합니다.")

class AnswerNode(BaseNode):
    def build_prompt(self, state):
        raise NotImplementedError

    def __call__(self, state):
        prompt = self.build_prompt(state)
        response = llm.predict(prompt)
        return {**state, "answer": response, "tries": state.get("tries", 0) + 1}

class QualityNode(BaseNode):
    def build_prompt(self, state):
        raise NotImplementedError

    def update_state(self, state, result):
        raise NotImplementedError

    def __call__(self, state):
        prompt = self.build_prompt(state)
        result = llm.predict(prompt)
        return self.update_state(state, result)

class SatisfactionNode(QualityNode):
    def build_prompt(self, state):
        return f"이 답이 만족스러운가? '{state['answer']}' (네/아니오):"

    def update_state(self, state, result):
        satisfied = "네" in result
        return {**state, "satisfied": satisfied} 