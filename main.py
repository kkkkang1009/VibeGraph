from graph.graph_builder import build_graph

def main():
    graph = build_graph()

    print("💬 LangGraph 챗봇입니다. 질문을 입력하세요. 종료하려면 'exit'을 입력하세요.\n")

    while True:
        question = input("❓ 질문: ").strip()

        if question.lower() == "exit":
            print("👋 종료합니다.")
            break
        
        state = {
            "question": question,
            "tries": 0
        }

        # result = graph.invoke(state)

        stream = graph.stream(state)

        final_state = None

        for step in stream:
            print("[DEBUG] step:", step)
            for node_name, events in step.items():
                print("[DEBUG] node_name:", node_name, "events:", events)
                if not isinstance(events, list):
                    events = [events]

                for event in events:
                    print("[DEBUG] event:", event)
                    if isinstance(event, dict):
                        state = event
                        final_state = state
        else:
            print("\n✅ 대화가 종료되었습니다. (자동 감지)")
            if final_state is not None:
                print(f"📌 최종 답변: {final_state['answer']}")
                print(f"🔁 반복 횟수: {final_state['tries']}")
            else:
                print("최종 state를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()