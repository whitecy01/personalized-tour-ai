import pandas as pd
import os
import time

# CSV 파일 경로
FILE_PATH = os.getenv("FILE_PATH")

# CSV 읽기
df = pd.read_csv(FILE_PATH, encoding='utf-8-sig')

# 조건: 사진유무 == "없음" AND 사용자총리뷰수이 비어 있거나 NaN
condition = (df['사진유무'] == '없음') & (df['사용자총리뷰수'].isna() | (df['사용자총리뷰수'].astype(str).str.strip() == ''))

# 해당 조건을 만족하는 행에 대해 값 수정
df.loc[condition, '사진유무'] = 0
df.loc[condition, '사용자총리뷰수'] = 0

# 저장
df.to_csv(FILE_PATH, index=False, encoding='utf-8-sig')
print(f"{condition.sum()}개의 행이 수정되어 저장되었습니다.")
