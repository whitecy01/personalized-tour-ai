import pandas as pd

# CSV 파일 불러오기
file_path = "/Users/jeongjaeyoon/Documents/GitHub/personalized-tour-ai/All_review.csv"
df = pd.read_csv(file_path)

# 중복 검사 대상 컬럼
target_cols = ["가게명", "작성자", "리뷰내용"]

# 완전히 같은 (가게명, 작성자) 조합이 있는 행 찾기
duplicates = df[df.duplicated(subset=target_cols, keep=False)]

# 결과 출력
if not duplicates.empty:
    print(f"중복된 조합 {len(duplicates)}개 발견됨. 그룹별로 출력:\n")
    grouped = duplicates.groupby(target_cols)

    for (store, author, ine), group in grouped:
        print(f"\n📌 가게명: {store}, 작성자: {author}")
        print(group[["리뷰내용", "주소", "작성시간"]])  # 필요시 다른 컬럼도 추가 가능
else:
    print("중복된 행 없음.")
