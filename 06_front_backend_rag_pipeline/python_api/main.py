from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import chromadb
import openai
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 환경변수에서 API 키 읽기
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트 생성 (최신 API 방식)
client = openai.OpenAI(api_key=api_key) 

app = FastAPI()

# Pydantic 모델 정의
class QuerySelectResponse(BaseModel):
    queryId: int
    age: str
    gender: str
    friendType: str
    purposes: List[str]
    interests: List[str]
    tastes: List[str]
    locations: List[str]
    amenities: List[str]
    priorities: str

class RequestData(BaseModel):
    survey: QuerySelectResponse
    message: str

# Prompt 작성 함수
def build_prompt(survey: QuerySelectResponse, reviews: List[str], metadatas: List[dict], user_message: str):
    sb = []
    sb.append("사용자 정보:")
    sb.append(f"- 나이대: {survey.age}")
    sb.append(f"- 성별: {survey.gender}")
    sb.append(f"- 동행 유형: {survey.friendType}")
    sb.append(f"- 여행 목적: {', '.join(survey.purposes)}")
    sb.append(f"- 관심사: {', '.join(survey.interests)}")
    sb.append(f"- 음식 취향: {', '.join(survey.tastes)}")
    sb.append(f"- 방문 희망 지역: {', '.join(survey.locations)}")
    sb.append(f"- 알레르기: {', '.join(survey.amenities)}")
    sb.append(f"- 최우선 조건: {survey.priorities}\n")

    sb.append("추천 기반 유사 리뷰 3개:")
    # for meta, doc in zip(metadatas, reviews):
    #     sb.append(f"- [{meta['가게명']}]")
    #     sb.append(f"  주소: {meta['주소']}")
    #     sb.append(f"  별점: {meta['별점']} / 가게 총평점: {meta['총평점']}")
    #     sb.append(f"  작성자: {meta['작성자']} (사용자 총리뷰수: {meta['사용자총리뷰수']})")
    #     sb.append(f"  리뷰 페이지: {meta['리뷰 페이지']}")
    #     sb.append(f"  trust_score: {meta['trust_score']}")
    #     sb.append(f"  리뷰 내용: {doc}\n")

    for meta, doc in zip(metadatas, reviews):
        sb.append(f"[{meta['가게명']}]")
        sb.append(f"주소: {meta['주소']}")
        sb.append(f"별점: {meta['별점']} / 총평점: {meta['총평점']}")
        sb.append(f"작성자: {meta['작성자']} (총리뷰수: {meta['사용자총리뷰수']})")
        sb.append(f"trust_score: {meta['trust_score']}")
        sb.append(f"리뷰 페이지: {meta['리뷰 페이지']}")
        sb.append(f"리뷰 내용: {doc}")
        sb.append("===")


    sb.append(f"\n사용자 질문: {user_message}")
    sb.append("\n위 데이터를 기반으로 부산 여행지 3곳을 추천해줘.")
    
    return "\n".join(sb)

# LLM 추천 API 엔드포인트
@app.post("/llm-recommend")
def llm_recommend(data: RequestData):
    # VectorDB 연결
    chroma_client = chromadb.PersistentClient(path="../../05_vector_db/chroma_storage")
    print("컬렉션 목록:", chroma_client.list_collections())
    collection = chroma_client.get_collection(name="trusted_reviews")

    # 임베딩 모델 로드
    model = SentenceTransformer("intfloat/multilingual-e5-base")

    # 사용자 message 임베딩
    query_embedding = model.encode(f"query: {data.message}", convert_to_tensor=False)

    # VectorDB 검색
    results = collection.query(query_embeddings=[query_embedding], n_results=3)

    # debug 출력
    print(f"VectorDB 검색 결과 문서 수: {len(results['documents'][0])}")
    
    # Prompt 작성
    prompt = build_prompt(
        data.survey,
        results['documents'][0],
        results['metadatas'][0],
        data.message
    )

    print("\n==== PROMPT ====\n", prompt)

    # OpenAI API 호출 (최신 openai>=1.0.0 방식)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 여행지 추천 도우미야."},
            {"role": "user", "content": prompt}
        ]
    )

    response_text = completion.choices[0].message.content

    print("\n==== OPENAI 응답 ====\n", response_text)

    # 응답 반환
    return {"response": response_text}

