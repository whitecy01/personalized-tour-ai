import pandas as pd
from datetime import datetime
from sentiment_analysis import get_sentiment_score_safe as get_sentiment_score
import time
from tqdm import tqdm



file_path = "/Users/jeongjaeyoon/Documents/GitHub/personalized-tour-ai/All_review.csv"
df = pd.read_csv(file_path)

# 감정 분석 -> tqdm 적용을 위해 리뷰내용 리스트화
reviews = df["리뷰내용"].astype(str).tolist()

#1. 리뷰 길이 ----------------------------------------------------------------------
# df["리뷰내용"] = df["리뷰내용"].astype(str).str.replace("\n", " ").str.strip()

df["리뷰_길이"] = df["리뷰내용"].astype(str).apply(len)
def score_length(length):
    if length >= 300:
        return 1.0
    elif length <= 100:
        return 0.0
    else:
        return (length - 100) / 200  # 100~300 사이 선형 증가

df["리뷰길이_점수"] = df["리뷰_길이"].apply(score_length)

print("리뷰_길이 컬럼이 추가된 파일이 저장")

#2. 작성자 리뷰 수 점수화 ----------------------------------------------------------------------
# 사용자 총 리뷰 수 수치화
df["사용자총리뷰수"] = pd.to_numeric(df["사용자총리뷰수"], errors="coerce").fillna(0)

def score_user_review_count(count):
    if count >= 100:
        return 1.0
    elif count <= 5:
        return 0.0
    else:
        return (count - 5) / 95

df["작성자리뷰수_점수"] = df["사용자총리뷰수"].apply(score_user_review_count)

# 반올림
df["작성자리뷰수_점수"] = df["작성자리뷰수_점수"].round(2)
print("작성자리뷰수_점수 컬럼 추가 완료")

# 3. 작성 시점 최신성 ----------------------------------------------------------------------------
# 날짜 형식 정제 ('.' 제거)
# 오늘 날짜 기준
today = datetime.now()

# 최신성 점수 계산 함수 (작성시간 문자열 바로 입력받음)
def score_recency_from_str(date_str):
    try:
        # "." 제거하고 공백 제거
        date_str = str(date_str).replace(".", "").strip()
        review_date = datetime.strptime(date_str, "%Y%m%d")
        delta = (today - review_date).days
        if delta < 0:
            return 1.0
        elif delta >= 365:
            return 0.0
        else:
            return round(1 - (delta / 365), 2)
    except ValueError:
        return 0.0  # 날짜 파싱 실패 시 0점

# 바로 점수 계산하여 컬럼 생성
df["날짜_최신성_점수"] = df["작성시간"].apply(score_recency_from_str)

print("날짜_최신성_점수 컬럼 생성 완료")

# 4. 사진유무 들고오기 -----------------------------------------------------------
# 사진유무 값만 가져오기
photo_values = df["사진유무"]

# 5. 감정분석 -------------------------------------------------------
print("감정 분석 중...")
scores = []

for i, text in enumerate(reviews):
    print(f"\n[{i+1}/{len(reviews)}] 리뷰 내용:\n{text}")
    score = get_sentiment_score(text)
    print(f"감정 점수: {score}")
    scores.append(score)
    time.sleep(5)
# df["감정점수"] = [get_sentiment_score(text) for text in tqdm(reviews)]



# 저장
df.to_csv("All_review.csv", index=False, encoding="utf-8-sig")
