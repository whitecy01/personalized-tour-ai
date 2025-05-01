import pandas as pd

# CSV 파일 불러오기
file_path = "/Users/jeongjaeyoon/Documents/GitHub/personalized-tour-ai/fin_data/kakao_maps_review.csv"  # 필요 시 경로 수정
df = pd.read_csv(file_path)

# 리뷰내용에서 '\n'을 공백으로 변환
df["리뷰내용"] = df["리뷰내용"].astype(str).str.replace(r"\n", " ", regex=True)

# 저장
df.to_csv(file_path, index=False, encoding="utf-8-sig")
print("리뷰내용의 줄바꿈 문자 제거 완료 및 저장 완료")
