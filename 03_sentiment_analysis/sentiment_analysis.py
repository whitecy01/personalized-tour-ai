
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

# 모델 로드
model_path = "C:/Users/NM333-67/Desktop/personalized-tour-ai/03_sentiment_analysis/finetuned/klue-roberta-nsmc-finetuned"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.eval()

# 토큰 직접 입력 버전 감정 점수 함수
def get_sentiment_score_from_tokens(tokens):
    input_ids = torch.tensor([tokens])
    attention_mask = torch.ones_like(input_ids)
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        return round(probs[0][1].item(), 3)

#긴 텍스트 청크 분할 및 평균 점수
def get_chunked_sentiment(text, max_chunk_len=256):
    tokens = tokenizer.encode(text, add_special_tokens=False)
    chunks = [tokens[i:i + max_chunk_len] for i in range(0, len(tokens), max_chunk_len)]

    scores = []
    lengths = []
    for chunk in chunks:
        chunk = chunk[:512]  # 안전 처리
        score = get_sentiment_score_from_tokens(chunk)
        scores.append(score)
        lengths.append(len(chunk))

    return round(np.average(scores, weights=lengths), 3)  # 가중 평균


# 토큰 길이에 따라 자동 분기 처리
def get_adaptive_sentiment_score(text, index=None):
    token_len = len(tokenizer.encode(text, add_special_tokens=False))
    if token_len > 512:
        score = get_chunked_sentiment(text)
        print(f"[경고] index={index}, 토큰수={token_len}, 점수={score} \n리뷰 일부: {text[:100]}...\n")
        return score
    elif token_len <= 256:
        tokens = tokenizer.encode(text, add_special_tokens=True, max_length=512, truncation=True)
        return get_sentiment_score_from_tokens(tokens)
    else:
        return get_chunked_sentiment(text)

# CSV 파일 읽기
df = pd.read_csv("C:/Users/NM333-67/Desktop/personalized-tour-ai/All_reviews_second.csv")
df["리뷰내용"] = df["리뷰내용"].astype(str)

# 감정 점수 계산
df["감정분석_점수"] = [get_adaptive_sentiment_score(text, idx) for idx, text in enumerate(df["리뷰내용"])]

# 저장
df.to_csv("C:/Users/NM333-67/Desktop/personalized-tour-ai/All_reviews_third_weight.csv", index=False, encoding="utf-8-sig")
print("감정분석_점수 컬럼 추가 및 저장 완료")
