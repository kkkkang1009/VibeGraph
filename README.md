# LangGraph QA System

고도화된 질의응답 시스템을 위한 LangGraph 기반 워크플로우 프로젝트입니다.

## 📁 프로젝트 구조

```
langgraph-study/
├── main.py                    # 메인 실행 파일
└── graph/                     # 그래프 관련 모듈
    ├── config.py              # 공통 설정 (LLM, API 키 등)
    ├── graph_builder.py       # 그래프 빌더
    ├── models/                # 데이터 모델들
    │   ├── __init__.py
    │   └── state.py           # QAState 정의
    ├── logic/                 # 분기 로직들
    │   ├── __init__.py
    │   ├── decision.py        # 의사결정 로직
    │   └── classification.py  # 분류 로직
    ├── utils/                 # 유틸리티 함수들
    │   ├── __init__.py
    │   ├── search.py          # 검색 관련
    │   ├── formatting.py      # 포맷팅 관련
    │   └── validation.py      # 검증 관련
    └── nodes/                 # 실행 노드들
        ├── __init__.py
        ├── basic_nodes.py     # 기본 노드들
        └── rag_node.py        # RAG 노드들
```

## 🔄 워크플로우

### 전체 플로우 다이어그램

```
시작
  ↓
질문 분류 → RAG 필요성 확인
  ↓
┌─────────────────┬─────────────────┐
│   RAG 플로우    │   기본 플로우   │
│                 │                 │
│ 문서 검색       │ 답변 생성       │
│ ↓               │ ↓               │
│ RAG 답변 생성   │ 품질 평가       │
│ ↓               │ ↓               │
│ RAG 품질 확인   │ ┌─────────────┐ │
│ ↓               │ │ 품질 결과   │ │
│ ┌─────────────┐ │ │ good        │ │
│ │ 만족        │ │ │ regenerate  │ │
│ │ 불만족      │ │ │ search_more │ │
│ └─────────────┘ │ └─────────────┘ │
│ ↓               │ ↓               │
│ 만족도 확인     │ 만족도 확인     │
│ ↓               │ ↓               │
│ ┌─────────────┐ │ ┌─────────────┐ │
│ │ 만족        │ │ │ 만족        │ │
│ │ 불만족      │ │ │ 불만족      │ │
│ └─────────────┘ │ └─────────────┘ │
│ ↓               │ ↓               │
└─────────────────┴─────────────────┘
                    ↓
                  종료 (END)
```

### 상세 워크플로우

1. **질문 분류** (`classify_question`)
   - 질문 유형 분석 (역사, 수학, 번역, 일반)
   - `question_type` 필드에 결과 저장

2. **RAG 필요성 확인** (`check_rag_needed`)
   - 키워드 기반 RAG 사용 여부 결정
   - "최신", "2024", "최근" 등 키워드 감지

3. **분기 처리**
   - **RAG 플로우**: 문서 검색 → RAG 답변 생성 → 품질 확인
   - **기본 플로우**: 답변 생성 → 품질 평가

4. **품질 관리**
   - 답변 품질 평가 및 개선 방향 제시
   - 재생성, 추가 검색, 만족도 확인 등

5. **최종 확인**
   - 사용자 만족도 확인
   - 필요시 재시도 또는 종료

## 🧩 노드 구성

### 기본 노드들 (`basic_nodes.py`)

- **`generate_answer_node`**: 기본 답변 생성
- **`check_satisfaction_node`**: 답변 만족도 확인
- **`evaluate_quality_node`**: 답변 품질 평가

### RAG 노드들 (`rag_node.py`)

- **`search_documents_node`**: 문서 검색
- **`generate_rag_answer_node`**: RAG 기반 답변 생성
- **`check_rag_quality_node`**: RAG 답변 품질 확인

### 로직 노드들

- **`classify_question`**: 질문 분류 로직
- **`should_use_rag`**: RAG 사용 여부 결정
- **`decide_next`**: 다음 단계 결정

## 📊 상태 관리 (QAState)

```python
class QAState(TypedDict):
    question: str                    # 사용자 질문
    answer: Optional[str]            # 생성된 답변
    satisfied: Optional[bool]        # 만족도
    tries: int                       # 시도 횟수

    retrieved_documents: Optional[List[str]]  # 검색된 문서들
    document_sources: Optional[List[str]]     # 문서 출처들
    search_query: Optional[str]      # 검색 쿼리
    use_rag: bool                    # RAG 사용 여부
    quality_score: Optional[str]     # 품질 점수
    needs_regeneration: Optional[bool]  # 재생성 필요 여부
    needs_more_search: Optional[bool]   # 추가 검색 필요 여부
    question_type: Optional[str]     # 질문 분류 결과
```

## 🚀 사용 방법

### 1. 환경 설정

```bash
# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
export OPENAI_API_KEY="your-api-key-here"
```

### 2. 실행

```bash
python main.py
```

### 3. 사용 예시

```
💬 LangGraph 챗봇입니다. 질문을 입력하세요. 종료하려면 'exit'을 입력하세요.

❓ 질문: 고구려의 역사에 대해 알려주세요
🧠 답변: 고구려는 기원전 37년에 건국된 고대 한국의 왕국입니다...

❓ 질문: 2024년 최신 AI 기술 동향은?
🧠 답변: [RAG 기반 답변] 2024년 AI 기술 동향에 대해...
```

## 🔧 설정

### config.py 주요 설정

```python
# LLM 모델 설정
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 환경변수
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

### 로직 커스터마이징

- **분류 로직**: `graph/logic/classification.py`
- **의사결정 로직**: `graph/logic/decision.py`
- **유틸리티**: `graph/utils/` 폴더

## 🧪 확장 가능성

### 추가 가능한 기능들

1. **다중 모델 지원**
   - 다양한 LLM 모델 선택
   - 모델별 특화 노드

2. **고급 RAG**
   - 벡터 데이터베이스 연동
   - 하이브리드 검색

3. **대화 기억**
   - 대화 히스토리 관리
   - 컨텍스트 유지

4. **사용자 맞춤화**
   - 개인화 설정
   - 선호도 학습

5. **성능 모니터링**
   - 응답 시간 측정
   - 품질 메트릭 수집

## 📝 개발 가이드

### 새로운 노드 추가

1. `graph/nodes/` 폴더에 새 파일 생성
2. 함수 시그니처: `def node_name(state: QAState) -> QAState:`
3. `graph_builder.py`에 노드 등록

### 새로운 로직 추가

1. `graph/logic/` 폴더에 새 파일 생성
2. 함수 시그니처: `def logic_name(state: QAState) -> str:`
3. `graph_builder.py`에 조건부 엣지 추가

### 새로운 유틸리티 추가

1. `graph/utils/` 폴더에 새 파일 생성
2. 순수 함수로 구현
3. 필요한 노드에서 임포트 사용

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해주세요. 