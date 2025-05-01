from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import os

# 학습된 모델 로드 (KLUE-RoBERTa + NSMC fine-tuned 모델)
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "../klue-roberta-nsmc-finetuned")

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.eval()

# 감정 점수 계산 함수
def get_sentiment_score(text, max_length=256):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=max_length)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        return round(probs[0][1].item(), 3)  # 긍정 점수 반환

# 긴 리뷰를 청크 단위로 나눈 후 평균 점수
def get_chunked_sentiment(text, max_chunk_len=256):
    words = text.split()
    chunks = []
    chunk = []

    for word in words:
        chunk.append(word)
        encoded = tokenizer(" ".join(chunk), truncation=True, return_tensors="pt", max_length=max_chunk_len)
        if encoded.input_ids.shape[1] >= max_chunk_len:
            chunk.pop()
            chunks.append(" ".join(chunk))
            chunk = [word]
    if chunk:
        chunks.append(" ".join(chunk))

    scores = [get_sentiment_score(chunk) for chunk in chunks]
    return round(np.mean(scores), 3)

# 길이에 따라 자동 선택
def get_adaptive_sentiment_score(text):
    if len(tokenizer.encode(text)) <= 256:
        return get_sentiment_score(text)
    else:
        return get_chunked_sentiment(text)

# 테스트용 리뷰 데이터
test_reviews = [
    # 256자 이하
    "분위기도 좋고 음식도 맛있었어요! 다음에 또 오고 싶네요.",
    "웨이팅이 길고 서비스가 느렸습니다. 음식은 그냥 그랬어요.",
    "정말 맛있고 만족스러웠습니다. 직원도 친절했어요.",
    
    # 500자 내외
    "가게 내부가 넓고 쾌적하며 음식이 빨리 나왔어요. 전체적으로 가격대비 퀄리티가 좋다고 생각합니다. 다만 주차 공간이 부족하다는 점은 아쉬웠습니다. 친구들과 대화 나누기 좋은 분위기였고 재방문 의사 있습니다.",
    "전반적으로 만족스러운 경험이었습니다. 특히 스테이크가 정말 부드럽고 맛있었어요. 분위기도 좋고, 조용해서 가족 단위 방문에도 좋을 것 같아요. 추천합니다.",
    "웨이팅은 있었지만 음식이 훌륭해서 기다린 보람이 있었어요. 디저트가 다양하고 커피도 맛있었습니다. 내부가 깔끔하고 서비스가 친절했어요.",

    # 2800자 수준 (긴 리뷰)
    "주말에 가족들과 함께 방문했는데, 전반적으로 만족스러웠습니다. 음식 맛도 좋고, 특히 회와 해산물이 신선했어요. 서빙 속도도 적당하고 종업원들도 친절했는데 다만 주차 공간이 협소해서 조금 불편했습니다. 그래도 다음에 또 올 생각이 들 만큼 좋은 경험이었습니다. 음식 가격도 적절했고, 아이들이 놀 수 있는 공간이 있다는 점도 장점이에요. 다양한 반찬과 음식이 계속 리필되는 점이 마음에 들었습니다. 주변 경관도 좋아서 사진 찍기에도 좋았고, 위치도 찾기 쉬웠습니다. 추천합니다. " * 3,
    "친구들과 여행 중 들른 식당인데, 이 지역에 이렇게 훌륭한 곳이 있다는 게 놀라웠어요. 음식이 정말 맛있고, 특히 해산물 요리가 일품이었습니다. 서빙 직원들도 매우 친절하고, 요청사항도 바로바로 반영해줘서 기분 좋게 식사할 수 있었습니다. 다만 대기 시간이 좀 긴 편이라 예약하고 가는 걸 추천드립니다. 내부는 꽤 넓고 청결했으며, 자리 간격도 넓어서 프라이버시가 보장되는 느낌이 들었어요. " * 3,
    "실망스러운 경험이었습니다. 음식은 기대 이하였고, 서비스도 매우 느렸습니다. 특히 주문 실수가 있었는데도 제대로 된 사과조차 받지 못했습니다. 웨이팅이 길었음에도 테이블 세팅이 엉망이었고, 전반적인 위생 상태도 불만족스러웠습니다. 다시 방문하고 싶은 생각이 들지 않네요. " * 5
]

# 실행
if __name__ == "__main__":
    for i, review in enumerate(test_reviews, 1):
        score = get_adaptive_sentiment_score(review)
        print(f"[리뷰 {i}] {review[:100]}{'...' if len(review) > 100 else ''}")
        print(f"→ 감정 점수: {score}\\n")
