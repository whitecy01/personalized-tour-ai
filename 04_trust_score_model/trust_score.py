import pandas as pd

# CSV 불러오기
df = pd.read_csv("C:/Users/NM333-67/Desktop/personalized-tour-ai/All_reviews_03_fin.csv")

# 필요한 컬럼 확인
required_columns = ["리뷰길이_점수", "작성자리뷰수_점수", "감정분석_점수", "사진유무", "날짜_최신성_점수"]
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"누락된 컬럼: {col}")

# trust_score 계산
df["trust_score"] = (
    0.2 * df["리뷰길이_점수"] +
    0.3 * df["작성자리뷰수_점수"] +
    0.25 * df["감정분석_점수"] +
    0.2 * df["사진유무"] +
    0.05 * df["날짜_최신성_점수"]
).round(3)

# 신뢰라벨 부여
df["신뢰라벨"] = df["trust_score"].apply(lambda x: 1 if x >= 0.6 else 0)

# 결과 확인
print(df[["trust_score", "신뢰라벨"]].value_counts())

# 저장
df.to_csv("C:/Users/NM333-67/Desktop/personalized-tour-ai/All_reviews_04_trust_score.csv", index=False, encoding="utf-8-sig")
print("trust_score 및 신뢰라벨 생성 및 저장 완료")

# import pandas as pd

# # CSV 불러오기
# df = pd.read_csv("C:/Users/NM333-67/Desktop/personalized-tour-ai/All_reviews_03_fin.csv")

# # 필요한 컬럼 확인
# required_columns = ["리뷰길이_점수", "작성자리뷰수_점수", "감정분석_점수", "사진유무", "날짜_최신성_점수"]
# for col in required_columns:
#     if col not in df.columns:
#         raise ValueError(f" 누락된 컬럼: {col}")

# # trust_score 계산 없이 바로 신뢰라벨 부여
# def compute_label(row):
#     score = (
#         0.2 * row["리뷰길이_점수"] +
#         0.3 * row["작성자리뷰수_점수"] +
#         0.25 * row["감정분석_점수"] +
#         0.2 * row["사진유무"] +
#         0.05 * row["날짜_최신성_점수"]
#     )
#     return 1 if score >= 0.6 else 0

# df["신뢰라벨"] = df.apply(compute_label, axis=1)

# # 결과 확인
# print(df[["신뢰라벨"]].value_counts())

# # 저장
# df.to_csv("C:/Users/NM333-67/Desktop/personalized-tour-ai/All_reviews_04_trust_score.csv", index=False, encoding="utf-8-sig")
# print("신뢰라벨 생성 및 저장 완료")
