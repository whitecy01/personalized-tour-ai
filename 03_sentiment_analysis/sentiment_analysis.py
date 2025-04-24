from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax
import torch

MODEL_NAME = "beomi/KcELECTRA-base-v2022"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()

def get_sentiment_score(text):
    try:
        with torch.no_grad():
            inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=256)
            outputs = model(**inputs)
            probs = softmax(outputs.logits, dim=-1)
            return round(probs[0][1].item(), 2)  # 클래스 1: 긍정
    except Exception as e:
        print(f"감정 분석 오류: {e}")
        return 0.0

def get_sentiment_score_safe(text):
    text = str(text).strip()
    if not text or text in ["리뷰 없음", "없음", "리뷰없음"] or len(text) < 5:
        return 0.0  # 또는 return None
    return get_sentiment_score(text)