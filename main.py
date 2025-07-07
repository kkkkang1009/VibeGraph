from graph.graph_builder import build_graph
from graph.models.state import QAState

def main():
    graph = build_graph()

    print("💬 LangGraph 챗봇입니다. 질문을 입력하세요. 종료하려면 'exit'을 입력하세요.\n")

    while True:
        question = input("❓ 질문: ").strip()

        if question.lower() == "exit":
            print("👋 종료합니다.")
            break
        
        # QAState 타입에 맞게 초기 상태 설정
        state: QAState = {
            "question": question,
            "tries": 0
        }

        print(f"\n🔄 그래프 실행 시작...")
        print(f"📝 질문: {question}")
        
        # result = graph.invoke(state)

        stream = graph.stream(state)

        final_state = None
        step_count = 0

        try:
            for step in stream:
                step_count += 1
                print(f"\n📊 [STEP {step_count}] ========================================")
                print(f"[DEBUG] 전체 step 객체: {step}")
                
                for node_name, events in step.items():
                    print(f"\n🔧 [NODE] {node_name}")
                    
                    if not isinstance(events, list):
                        events = [events]

                    for i, event in enumerate(events):
                        if isinstance(event, dict):
                            # event를 QAState로 타입 캐스팅
                            state = event  # type: ignore[assignment]
                            final_state = state  # type: ignore[assignment]
                            
                            # 중요한 상태 변화만 출력
                            print(f"  ✅ 상태 업데이트")
                            if state.get('answer') and len(str(state.get('answer', ''))) > 50:
                                print(f"  📝 답변: {str(state.get('answer', ''))[:50]}...")
                            elif state.get('answer'):
                                print(f"  📝 답변: {state.get('answer')}")
                            
                            # tries가 증가했을 때만 출력
                            if state.get('tries', 0) > 0:
                                print(f"  🔁 시도 횟수: {state.get('tries')}")
                            
                            # 에러가 있을 때만 출력
                            if state.get('error'):
                                print(f"  ❌ 에러: {state.get('error')}")
                        else:
                            print(f"  ⚠️  예상치 못한 이벤트 타입: {type(event)}")
                
                print(f"📊 [STEP {step_count}] 완료 ========================================\n")
                
        except Exception as e:
            print(f"\n❌ 스트림 처리 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
        
        # 스트림 완료 후 최종 결과 출력
        print(f"\n🎯 스트림 완료! 총 {step_count}개 단계 실행됨")
        print("=" * 60)
        
        if final_state is not None:
            print(f"📌 최종 답변: {final_state.get('answer', '답변 없음')}")
            print(f"🔁 반복 횟수: {final_state.get('tries', 0)}")
            print(f"😊 만족 여부: {final_state.get('satisfied', 'N/A')}")
            print(f"🔍 검색 유형: {final_state.get('search_type', 'None')}")
            retrieved_docs = final_state.get('retrieved_documents', [])
            print(f"📚 검색된 문서 수: {len(retrieved_docs) if retrieved_docs else 0}")
            error_msg = final_state.get('error')
            if error_msg:
                print(f"❌ 에러: {error_msg}")
        else:
            print("⚠️  최종 state를 찾을 수 없습니다.")
        
        print("=" * 60)
        print()

if __name__ == "__main__":
    main()