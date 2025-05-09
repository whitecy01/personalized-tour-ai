import pandas as pd

# CSV 파일 불러오기
file_path = "/Users/jeongjaeyoon/Documents/GitHub/personalized-tour-ai/01_data_collection/fin_data/All_reviews.csv"  # 필요 시 경로 수정
df = pd.read_csv(file_path)


# 업종 컬럼의 NaN 값을 '없음'으로 채움
df['업종'] = df['업종'].fillna('없음')

# 빈 문자열도 '없음'으로 대체
df['업종'] = df['업종'].replace('', '없음')

# 결과 저장
df.to_csv(file_path, index=False,  encoding="utf-8-sig")
