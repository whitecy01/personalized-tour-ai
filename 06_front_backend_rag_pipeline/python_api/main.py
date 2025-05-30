from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import chromadb
import openai
from sentence_transformers import SentenceTransformer
from typing import Optional
import pandas as pd
from dotenv import load_dotenv
import os
from more_itertools import chunked  # pip install more-itertools

# .env 파일 로드
load_dotenv()

# 환경변수에서 API 키 읽기
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트 생성 (최신 API 방식)
client = openai.OpenAI(api_key=api_key) 

model = SentenceTransformer("intfloat/multilingual-e5-base")

app = FastAPI()


CSV_PATH = "/Users/jeongjaeyoon/Documents/GitHub/personalized-tour-ai/All_reviews_04_trust_score_V2.csv"
CHROMA_PATH = "/Users/jeongjaeyoon/Documents/GitHub/personalized-tour-ai/05_vector_db/chroma_storageV2"
COLLECTION_NAME = "trusted_reviews"


# 요청 바디 모델 정의
class TrustScoreWeights(BaseModel):
    reviewLength: Optional[float] = 0.0
    reviewCount: Optional[float] = 0.0
    sentiment: Optional[float] = 0.0
    photo: Optional[float] = 0.0
    recentness: Optional[float] = 0.0
    threshold: Optional[float] = 0.6

@app.post("/update-trust-score")
def update_trust_score(data: TrustScoreWeights):
    try:
        weights = {
            "reviewLength": data.reviewLength,
            "reviewCount": data.reviewCount,
            "sentiment": data.sentiment,
            "photo": data.photo,
            "recentness": data.recentness,
        }

        print("가중치 목록 확인:", weights)

        if not os.path.exists(CSV_PATH):
            return {"error": "CSV 파일이 존재하지 않습니다."}

        df = pd.read_csv(CSV_PATH, dtype=str)  # 모든 열을 문자열로 로딩 (중간 타입 문제 방지)
        
        # 안전한 형 변환
        for col in ["리뷰길이_점수", "작성자리뷰수_점수", "감정분석_점수", "사진유무", "날짜_최신성_점수"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # trust_score 계산
        df["trust_score"] = (
            weights["reviewLength"] * df["리뷰길이_점수"] +
            weights["reviewCount"] * df["작성자리뷰수_점수"] +
            weights["sentiment"] * df["감정분석_점수"] +
            weights["photo"] * df["사진유무"] +
            weights["recentness"] * df["날짜_최신성_점수"]
        ).round(3)

        df["신뢰라벨"] = df["trust_score"].apply(lambda x: 1 if x >= data.threshold else 0)
        print(df[["trust_score", "신뢰라벨"]].head(3))
        df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")



        # 신뢰 리뷰 필터링
        trusted_df = df[df['신뢰라벨'] == 1].dropna(subset=['리뷰내용']).reset_index(drop=True)
        texts = trusted_df['리뷰내용'].tolist()
        prefixed_texts = [f"passage: {t}" for t in texts]

        # 임베딩 생성 (배치 분할)
        BATCH_LIMIT = 500
        all_embeddings = []
        for chunk in chunked(prefixed_texts, BATCH_LIMIT):
            chunk_embeddings = model.encode(
                chunk,
                convert_to_tensor=False,
                show_progress_bar=True,
            )
            all_embeddings.extend(chunk_embeddings)

        # ChromaDB 초기화
        chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
        if COLLECTION_NAME in [c.name for c in chroma_client.list_collections()]:
            chroma_client.delete_collection(name=COLLECTION_NAME)
        collection = chroma_client.create_collection(name=COLLECTION_NAME)

        # 메타데이터 정의
        metadata_columns = [
            '가게명', '별점', '작성자',
            '사용자총리뷰수', '총평점', '주소',
            '리뷰 페이지', 'trust_score'
        ]

        # 벡터 DB 삽입 데이터 준비
        documents_list = []
        embeddings_list = []
        metadatas_list = []
        ids_list = []

        for i, (text, embedding) in enumerate(zip(texts, all_embeddings)):
            documents_list.append(text)
            embeddings_list.append(embedding)
            metadatas_list.append(trusted_df.iloc[i][metadata_columns].to_dict())
            ids_list.append(str(i))

        # ChromaDB에 배치로 삽입
        CHUNK_SIZE = 500
        for docs_chunk, embeds_chunk, metas_chunk, ids_chunk in zip(
            chunked(documents_list, CHUNK_SIZE),
            chunked(embeddings_list, CHUNK_SIZE),
            chunked(metadatas_list, CHUNK_SIZE),
            chunked(ids_list, CHUNK_SIZE)
        ):
            collection.add(
                documents=docs_chunk,
                embeddings=embeds_chunk,
                metadatas=metas_chunk,
                ids=ids_chunk
            )

        print(f"총 {len(texts)}개의 신뢰 리뷰가 벡터 DB에 저장되었습니다.")
        print("저장된 벡터 수:", collection.count())


      



        #vectorDB
        # # 1. 신뢰 리뷰만 필터링
        # trusted_df = df[df['신뢰라벨'] == 1].dropna(subset=['리뷰내용']).reset_index(drop=True)
        # texts = trusted_df['리뷰내용'].tolist()
        # # 2. E5 모델 로딩
        # model = SentenceTransformer("intfloat/multilingual-e5-base")
        # # 3. prefix 붙이기
        # prefixed_texts = [f"passage: {text}" for text in texts]
        # # 4. 임베딩 생성
        # embeddings = model.encode(prefixed_texts, convert_to_tensor=False)
        # # 5. ChromaDB 연결 및 기존 컬렉션 삭제 후 생성
        # chroma_client = chromadb.PersistentClient(path="C:/Users/NM333-67/Desktop/personalized-tour-ai/05_vector_db/chroma_storageV2")

        # if "trusted_reviews" in [c.name for c in chroma_client.list_collections()]:
        #     chroma_client.delete_collection(name="trusted_reviews")

        # collection = chroma_client.create_collection(name="trusted_reviews")

        # # 6. 메타데이터 컬럼 지정 및 삽입
        # metadata_columns = [
        #     '가게명', '별점', '작성자',
        #     '사용자총리뷰수', '총평점', '주소',
        #     '리뷰 페이지', 'trust_score'
        # ]

        # for i, (text, embedding) in enumerate(zip(texts, embeddings)):
        #     metadata = trusted_df.iloc[i][metadata_columns].to_dict()
        #     collection.add(
        #         embeddings=[embedding],
        #         documents=[text],
        #         metadatas=[metadata],
        #         ids=[str(i)]
        #     )

        # print(f"총 {len(texts)}개의 신뢰 리뷰가 벡터 DB에 저장되었습니다.")


        return {
            "message": "trust_score 및 신뢰라벨 갱신 완료",
            "preview": df[["trust_score", "신뢰라벨"]].head(3).to_dict(orient="records")
        }

    except Exception as e:
        return {"error": str(e)}














# Pydantic 모델 정의
class QuerySelectResponse(BaseModel):
    queryId: int
    age: str
    friendType: str
    purposes: List[str]
    # interests: List[str]
    # tastes: List[str]
    # locations: List[str]
    # amenities: List[str]
    # priorities: str

class RequestData(BaseModel):
    survey: QuerySelectResponse
    message: str

# Prompt 작성 함수
def build_prompt(survey: QuerySelectResponse, reviews: List[str], metadatas: List[dict], user_message: str):
    sb = []
    sb.append("사용자 정보:")
    sb.append(f"- 나이대: {survey.age}")
    # sb.append(f"- 성별: {survey.gender}")
    sb.append(f"- 동행 유형: {survey.friendType}")
    sb.append(f"- 여행 목적: {', '.join(survey.purposes)}")
    # sb.append(f"- 관심사: {', '.join(survey.interests)}")
    # sb.append(f"- 음식 취향: {', '.join(survey.tastes)}")
    # sb.append(f"- 방문 희망 지역: {', '.join(survey.locations)}")
    # sb.append(f"- 알레르기: {', '.join(survey.amenities)}")
    # sb.append(f"- 최우선 조건: {survey.priorities}\n")

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
        # model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 부산 여행지 추천 도우미야."},
            {"role": "user", "content": prompt}
        ]
    )

    response_text = completion.choices[0].message.content

    print("\n==== OPENAI 응답 ====\n", response_text)

    # 응답 반환
    return {"response": response_text}

