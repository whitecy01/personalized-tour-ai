import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# CSV 파일 불러오기
file_path = "/Users/jeongjaeyoon/Documents/GitHub/personalized-tour-ai/google_maps_review.csv"
df = pd.read_csv(file_path)

# 작성시간 변환 함수
def convert_relative_time_to_date(text):
    now = datetime.now()
    try:
        if "달 전" in text:
            months_ago = int(text.replace("달 전", "").strip())
            converted = now - relativedelta(months=months_ago)
            return converted.strftime("%Y.%m.%d.")  # 마침표 포함
        elif "년 전" in text:
            years_ago = int(text.replace("년 전", "").strip())
            converted = now - relativedelta(years=years_ago)
            return converted.strftime("%Y.%m.%d.")  # 마침표 포함
        elif "주 전" in text:
            weeks_ago = int(text.replace("주 전", "").strip())
            converted = now - timedelta(weeks=weeks_ago)
            return converted.strftime("%Y.%m.%d.")
        else:
            return text  # 변환할 수 없는 경우 원본 유지
    except:
        return text  # 예외 시 원본 유지

# 기존 작성시간 컬럼 덮어쓰기
df["작성시간"] = df["작성시간"].astype(str).apply(convert_relative_time_to_date)

# 덮어쓴 결과를 저장
df.to_csv(file_path, index=False, encoding="utf-8-sig")
print("작성시간 컬럼 덮어쓰기 및 저장 완료")
