# Graph-Vibe: LangGraph 기반 지능형 QA 시스템

고도화된 질의응답 시스템을 위한 LangGraph 기반 워크플로우 프로젝트입니다. RAG(Retrieval-Augmented Generation)와 웹 검색을 통합하여 정확하고 최신 정보를 제공하는 AI 챗봇입니다.

## 🚀 주요 기능

- **지능형 질문 분류**: 질문 유형을 자동으로 분석하고 적절한 처리 경로 선택
- **RAG 통합**: 문서 검색 기반 답변 생성으로 정확성 향상
- **웹 검색**: 실시간 웹 검색을 통한 최신 정보 제공
- **품질 관리**: 답변 품질 자동 평가 및 개선
- **스트리밍 응답**: 실시간으로 답변 생성 과정 확인

## 📁 프로젝트 구조

```
graph-vibe/
├── main.py                    # 메인 실행 파일
├── requirements.txt           # 의존성 관리 (uv 사용)
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
        ├── base.py            # 기본 노드 클래스
        ├── node_registry.py   # 노드 등록 관리
        ├── classify.py        # 질문 분류 노드
        ├── answer.py          # 기본 답변 생성 노드
        ├── quality.py         # 품질 평가 노드
        ├── rag/               # RAG 관련 노드들
        │   ├── __init__.py
        │   ├── search.py      # 문서 검색
        │   ├── answer.py      # RAG 답변 생성
        │   └── quality.py     # RAG 품질 확인
        └── search/            # 웹 검색 관련 노드들
            ├── __init__.py
            ├── web.py         # 웹 검색
            └── answer.py      # 검색 기반 답변 생성
```

## 🔄 워크플로우

### 전체 플로우 다이어그램

```
시작
  ↓
질문 분류 → 처리 방식 결정
  ↓
┌─────────────────┬─────────────────┬─────────────────┐
│   RAG 플로우    │   웹 검색 플로우 │   기본 플로우   │
│                 │                 │                 │
│ 문서 검색       │ 웹 검색         │ 답변 생성       │
│ ↓               │ ↓               │ ↓               │
│ RAG 답변 생성   │ 검색 기반 답변   │ 품질 평가       │
│ ↓               │ ↓               │ ↓               │
│ RAG 품질 확인   │ 품질 평가       │ ┌─────────────┐ │
│ ↓               │ ↓               │ │ 품질 결과   │ │
│ ┌─────────────┐ │ ┌─────────────┐ │ │ good        │ │
│ │ 만족        │ │ │ 만족        │ │ │ regenerate  │ │
│ │ 불만족      │ │ │ 불만족      │ │ │ search_more │ │
│ └─────────────┘ │ └─────────────┘ │ └─────────────┘ │
│ ↓               │ ↓               │ ↓               │
│ 만족도 확인     │ 만족도 확인     │ 만족도 확인     │
│ ↓               │ ↓               │ ↓               │
│ ┌─────────────┐ │ ┌─────────────┐ │ ┌─────────────┐ │
│ │ 만족        │ │ │ 만족        │ │ │ 만족        │ │
│ │ 불만족      │ │ │ 불만족      │ │ │ 불만족      │ │
│ └─────────────┘ │ └─────────────┘ │ └─────────────┘ │
│ ↓               │ ↓               │ ↓               │
└─────────────────┴─────────────────┴─────────────────┘
                    ↓
                  종료 (END)
```

### 상세 워크플로우

1. **질문 분류** (`classify_question`)
   - 질문 유형 분석 (역사, 수학, 번역, 일반, 최신 정보 등)
   - `question_type` 필드에 결과 저장

2. **처리 방식 결정** (`decide_next`)
   - RAG 사용 여부 확인 (키워드 기반)
   - 웹 검색 필요성 확인 (최신 정보 요청)
   - 기본 답변 생성 여부 결정

3. **분기 처리**
   - **RAG 플로우**: 문서 검색 → RAG 답변 생성 → 품질 확인
   - **웹 검색 플로우**: 웹 검색 → 검색 기반 답변 생성 → 품질 확인
   - **기본 플로우**: 답변 생성 → 품질 평가

4. **품질 관리**
   - 답변 품질 평가 및 개선 방향 제시
   - 재생성, 추가 검색, 만족도 확인 등

5. **최종 확인**
   - 사용자 만족도 확인
   - 필요시 재시도 또는 종료

## 🧩 노드 구성

### 기본 노드들

- **`classify_node`**: 질문 분류 및 유형 분석
- **`answer_node`**: 기본 답변 생성
- **`quality_node`**: 답변 품질 평가

### RAG 노드들 (`rag/`)

- **`search_node`**: 문서 검색
- **`answer_node`**: RAG 기반 답변 생성
- **`quality_node`**: RAG 답변 품질 확인

### 웹 검색 노드들 (`search/`)

- **`web_node`**: 웹 검색 수행
- **`answer_node`**: 검색 결과 기반 답변 생성

### 로직 노드들

- **`classify_question`**: 질문 분류 로직
- **`decide_next`**: 다음 단계 결정 로직

## 📊 상태 관리 (QAState)

```python
class QAState(TypedDict):
    question: str                    # 사용자 질문
    answer: Optional[str]            # 생성된 답변
    satisfied: Optional[bool]        # 만족도
    tries: int                       # 시도 횟수

    # 검색 관련
    search_type: Optional[str]       # 검색 유형 (web, rag, None)
    retrieved_documents: Optional[List[str]]  # 검색된 문서들
    document_sources: Optional[List[str]]     # 문서 출처들
    search_query: Optional[str]      # 검색 쿼리
    
    # 웹 검색 관련
    web_search_results: Optional[List[str]]  # 웹 검색 결과
    
    # 품질 관리
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

# uv를 사용한 의존성 설치
uv pip install -r requirements.txt

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
🧠 답변: [웹 검색 기반 답변] 2024년 AI 기술 동향에 대해...

❓ 질문: 파이썬으로 웹 스크래핑하는 방법
🧠 답변: [RAG 기반 답변] 파이썬 웹 스크래핑에 대해...
```

## 🔧 설정

### config.py 주요 설정

```python
# LLM 모델 설정
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 환경변수
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

### 의존성 관리 (uv 사용)

현재 프로젝트는 `uv`를 사용하여 패키지 관리를 합니다:

```bash
# 패키지 설치
uv pip install 패키지명

# requirements.txt 생성
uv pip freeze > requirements.txt
```

### 로직 커스터마이징

- **분류 로직**: `graph/logic/classification.py`
- **의사결정 로직**: `graph/logic/decision.py`
- **노드 추가**: `graph/nodes/` 폴더에 새 노드 추가
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
   - 품질 지표 추적

6. **멀티미디어 지원**
   - 이미지 분석
   - 음성 인식/합성

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 문의

프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 생성해 주세요. 