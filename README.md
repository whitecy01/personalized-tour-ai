# 개인맞춤형 관광을 위한 LLM 기반 RAG를 활용한 신뢰도 리뷰 추천 시스템
- Personalized Tour AI System (LLM + RAG 기반 맞춤형 관광 추천 시스템)

이 프로젝트는 지역 관광 활성화를 위한 **LLM 기반 맞춤형 추천 시스템**을 구축하는 것을 목표로 합니다.  
특히, **부산 지역 소상공인을 중심으로**, 사용자 맞춤 관광지/맛집/체험을 추천하고,  
리뷰 신뢰도 기반으로 정확하고 신뢰할 수 있는 정보를 제공합니다.


</br>

## 프로젝트 목적

- **부산 소상공인의 급격한 감소** 및 상권 공실률 증가 대응
- 기존 **부산투어패스의 한계**(대형 관광지 중심, 접근성 부족 등) 보완
- 바가지요금, 체류시간 짧음 등 **부산 관광의 구조적 한계 해결**
- **신뢰 리뷰 기반 개인화된 관광 추천**을 통해 지역경제 활성화


</br>

## 핵심 기술 요소

| 기술 | 설명 |
|------|------|
| **LLM (GPT-3.5-turbo)** | 사용자 사전 질의 + 질문을 기반으로 개인화된 응답 생성 |
| **RAG (Retrieval Augmented Generation)** | Vector DB에서 리뷰 정보 검색 후 LLM이 참고 |
| **감정 분석 (KLUE-RoBERTa)** | 리뷰의 감정 극성 점수 추출 |
| **신뢰도 평가 (XGBoost)** | 리뷰의 정량적 지표 기반 신뢰도 라벨 예측 |
| **Vector DB (FAISS)** | 유사도 기반의 의미 검색 지원 |
| **MySQL** | 사용자 사전 질의 정보 저장 (나이, 취향, 여행 목적 등) |



</br>

## 시스템 아키텍처 요약

```plaintext
1. 사용자 사전 질의 수집 (성별, 나이, 관심사 등)
2. 외부 리뷰 수집 (Google Maps, Naver Blog, Instagram 등)
3. 감성 분석 및 정량화 (리뷰 길이, 활동성, 이미지 포함 등)
4. XGBoost 기반 신뢰도 평가 → trust_score ≥ 0.75 → 저장
5. RAG로 Vector DB에서 유사 리뷰 검색
6. LLM이 질의 + 사전 정보 + 리뷰 결과를 바탕으로 개인화된 응답 생성
```
![alt text](./image/image.png)


</br>

## 수집 데이터 출처
Google Maps API 리뷰
카카오맵 크롤링 리뷰
네이버 블로그 리뷰 (문화 빅데이터 플랫폼 활용)
Instagram 해시태그 기반 리뷰 크롤링 


</br>

## 기대 효과
- 개인 맞춤형 관광지/맛집/체험 정보 추천
- 신뢰도 높은 리뷰만 기반으로 한 정확한 추천
- 대형 관광지 외 지역 소상공인 매출 증대
- 바가지 요금 예방, 불신 해소
- 지역 경제 활성화 + 타 지역 확장 가능성


</br>

## 폴더 구조(예정)

```bash
personalized-tour-ai
├── 01_data_collection/       # 리뷰 수집 (Google Maps 등)
├── 02_data_cleaning/         # 전처리
├── 03_sentiment_analysis/    # 감정 분석 모델 추론
├── 04_trust_score_model/     # 정량화 + XGBoost
├── 05_vector_db/             # FAISS / Chroma 저장
├── 06_rag_pipeline/          # RAG 응답 구조
├── 07_llm_response/          # GPT 응답 생성
├── 08_front_ui_mockup/       # 시각화 결과 예시
├── 09_docs/                  # 보고서, 다이어그램
├── image                     # README 사진 
└── README.md
```

</br>

### Git 브랜치 전략

```plaintext
main               ← 최종 안정 버전
│
└── dev            ← 전체 개발 통합 브랜치
     ├── 01_data_collection
     ├── 02_data_cleaning
     ├── 03_sentiment_analysis
     ├── 04_trust_score_model
     ├── 05_vector_db
     ├── 06_rag_pipeline
     ├── 07_llm_response
     ├── 08_front_ui_mockup
     └── 09_docs
```

 

</br>

# 프로젝트 구조 및 설명
### 01_data_collection

```plaintext
01_data_collection       
│
└── google_maps        
│    ├── google_reivews_api_1.py
│    ├── pharse_reviews_2.py
│    └── change_value_3.py
│
└── kakao_maps_crawling_reviews
     └── kakao_reviews.py
```

- google_maps
     - google_reivews_api_1.py
          - Google Places API를 활용해 장소 및 리뷰 데이터를 수집
          - google_maps_reviews.csv로 결과 저장
          - 부산 내 각 구별 위치좌표 및 키워드를 기반으로 장소 검색
          - 장소의 place_id를 활용하여 상세 리뷰 정보 요청
          - 중복 리뷰 필터링 처리
     - pharse_reviews_2.py
          - 수집된 구글 리뷰 데이터를 Selenium으로 접속하여 추가 정보(총리뷰 수, 업종, 총별점, 사진 유무 등)를 수집
          - 장소명과 일치하는 리뷰 블럭을 찾아 클릭 후 상세 정보 추출
          - 스크롤을 통해 리뷰 영역을 탐색하며 사용자 상세 리뷰 정보를 보강
          - 추출 정보는 기존 CSV(google_maps_reviews.csv)에 반영
     - change_value_3.py
          - 수집된 리뷰 데이터 중 '사진유무' 값이 "없음"이고 '사용자 총리뷰수'가 비어있는 행을 찾아 0으로 수정
          - 리뷰를 미제공하는 곳이 있어서 이 처리를 진행

- kakao_maps_crawling_reviews
     - kakao_reviews.py
          - Selenium을 이용해 카카오맵에서 장소를 검색하고, 리뷰 데이터를 수집하여 CSV 파일로 저장하는 자동화 스크립트
          - 키워드 검색을 통해 특정 지역의 장소 검색
          - 검색 결과 리스트의 각 장소를 순차적으로 클릭하여 리뷰 페이지 진입
          - 각 장소의 리뷰들을 스크립를 통해 모두 로딩한 후 항목 추출(장소명, 업종, 주소, 총평점, 리뷰 작성자명, 리뷰 본문, 별점, 작성일, 사진 유무, 작성자 리뷰수, 리뷰 링크)
          - 중복 방지 로직을 통해 이미 저장된 데이터는 필터링
          - 수집된 리뷰 데이터는 kakao_maps_reviews.csv로 저장
</br>         

카카오맵 maps_crwaling_reviews 키워드
```plaintext
1. 해운대 맛집 
2. 부산 관광 
3. 사하구 디저트 카페 
4. 영도구 맛집 
5. 부산 남구 카페 
6. 부산 북구 놀거리
7. 부산 북구 관광 
8. 부산 전통시장 
9. 부산 연제구 관광
10. 부산 기장 맛집 
11. 부산 냉정 카페
12. 부산 주례 맛집
13. 부산 구서동 맛집
14. 부산 정관 카페
15. 부산 하단 카페
16. 부산 대연동 디저트
17. 부산 명장동 골목식당
18. 부산 서면 카페
19. 부산 온천장 카페
20. 부산 반여동 카페
21. 부산 일광 관광
```




### 수집 데이터 필드 설명

| 필드명             | 설명                                       |
|--------------------|--------------------------------------------|
| 가게명             | 장소 이름                                  |
| 주소               | 장소 주소                                  |
| 작성자             | 리뷰 작성자 이름                           |
| 리뷰내용           | 작성된 리뷰 내용                           |
| 별점               | 개별 리뷰 별점                             |
| 작성시간           | 리뷰가 작성된 상대 시간 (예: 1일 전 등)    |
| 리뷰 페이지        | 리뷰 상세 페이지 URL                       |
| 사진유무           | 해당 리뷰에 사진 포함 여부 (1: 있음 / 0: 없음) |
| 총평점             | 장소의 전체 평균 별점                      |
| 업종               | 업종명 (예: 카페, 음식점 등)               |
| 사용자총리뷰수     | 리뷰 작성자의 누적 리뷰 수                 |

### 02_data_cleaning
- kakao_maps_reviews.csv을 google_maps_reviews.csv 규격 맞추기
- kakao_maps_reviews.csv의 데이터 전처리


### 03_sentiment_analysis
- 리뷰데이터 점수 벡터화
- 감정 분석 모델 추론