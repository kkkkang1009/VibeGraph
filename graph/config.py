from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

# 환경변수 로드
load_dotenv(override=True)

# API 키 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LLM 인스턴스 생성 (공통으로 사용)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 디버깅용 출력
print(f"OPENAI_API_KEY: {OPENAI_API_KEY}") 