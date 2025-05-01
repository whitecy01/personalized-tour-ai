import pandas as pd

# CSV 파일 로드
df = pd.read_csv("C:/Users/NM333-67/Desktop/personalized-tour-ai/All_reviews.csv")



# 문자열로 변환 후 길이 계산
df["리뷰내용"] = df["리뷰내용"].astype(str)
df["리뷰_길이"] = df["리뷰내용"].apply(len)

# 최대 길이 찾기
max_length = df["리뷰_길이"].max()
longest_review = df.loc[df["리뷰_길이"].idxmax(), "리뷰내용"]

print(f"가장 긴 리뷰 길이: {max_length}자")
print(f"실제 리뷰 길이(len): {len(longest_review)}자") 
print("\n리뷰 내용:")
print(longest_review)