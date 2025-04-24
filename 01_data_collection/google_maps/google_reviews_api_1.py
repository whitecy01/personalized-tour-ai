import os
from dotenv import load_dotenv
import csv
import time
import requests

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

areas = {
    # "해운대구": "35.1632,129.1631",
    # "동래구": "35.2048,129.0838",
    # "수영구": "35.1454,129.1133",
    # "연제구": "35.1841,129.0797",
    # "남구": "35.1360,129.0842",
    # "금정구": "35.2438,129.0928",
    # "기장군": "35.2441,129.2235",
    "부산진구": "35.1576,129.0592",
    "동구": "35.1341,129.0466",
    "중구": "35.1065,129.0322",
    "서구": "35.0976,129.0245",
    "북구": "35.1979,128.9904",
    "영도구": "35.0917,129.0670",
    "사하구": "35.1043,128.9757",
    "사상구": "35.1534,128.9903",
    "강서구": "35.1918,128.9806"
}

# areas = {
#     "부산진구": "35.1576,129.0592",
#     "동구": "35.1341,129.0466",
#     "중구": "35.1065,129.0322",
#     "서구": "35.0976,129.0245",
#     "북구": "35.1979,128.9904",
#     "영도구": "35.0917,129.0670",
#     "사하구": "35.1043,128.9757",
#     "사상구": "35.1534,128.9903",
#     "강서구": "35.1918,128.9806"
# }

keywords = [
    "카페", "디저트", "음식점", "빵집", "관광지", "맛집", "브런치", "분위기 좋은 곳", "놀거리",
    "조용한 카페", "로컬 맛집", "골목 식당", "시장", "숨은 카페", "로컬 술집", "숨은 맛집", "이색놀거리"
]

# 검색 반경 (m 단위)
RADIUS = 5000


total_reviews_collected = 0

# 중복 방지용 집합
seen_reviews = set()


# 장소 검색 함수
def search_places(keyword, location):
    url = (
        f"https://maps.googleapis.com/maps/api/place/textsearch/json?"
        f"query={keyword}&location={location}&radius={RADIUS}&language=ko&key={API_KEY}"
    )
    response = requests.get(url).json()
    return [(r["name"], r["place_id"]) for r in response.get("results", [])]


# 리뷰 + 주소 수집 함수
def get_reviews(place_id):
    url = (
        f"https://maps.googleapis.com/maps/api/place/details/json?"
        f"place_id={place_id}&fields=name,rating,reviews,formatted_address"
        f"&language=ko&key={API_KEY}"
    )
    response = requests.get(url).json()
    result = response.get("result", {})
    name = result.get("name", "Unknown")
    address = result.get("formatted_address", "")
    reviews = result.get("reviews", [])
    return name, address, reviews

# csv 값 들고오기
def load_existing_keys(filename):
    existing = set()
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 3:
                    existing.add((row[0], row[1], row[2]))
    return existing

#  CSV 저장 함수
def save_reviews(place_name, address, reviews, existing, filename="busan_reviews.csv"):
    global total_reviews_collected
    file_exists = os.path.exists(filename)
    saved_count = 0

    with open(filename, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["가게명", "주소", "작성자", "리뷰내용", "별점", "작성시간", "리뷰 페이지"])

        for r in reviews:
            key = (place_name, address, r.get("author_name", ""))
            if key in seen_reviews or key in existing:
                continue
            seen_reviews.add(key)
            existing.add(key)
            writer.writerow([
                place_name,
                address,
                r.get("author_name", ""),
                r.get("text", "").replace("\n", " "),
                r.get("rating", ""),
                r.get("relative_time_description", ""),
                r.get("author_url", "")
            ])
            saved_count += 1

    total_reviews_collected += saved_count
    return saved_count


# 메인 실행
def run_collection():
    filename = "busan_reviews.csv"
    existing = load_existing_keys(filename)

    for area_name, location in areas.items():
        for keyword in keywords:
            query = f"{area_name} {keyword}"
            print(f"\n 검색: {query}")
            places = search_places(query, location)

            for name, pid in places:
                print(f"장소: {name} | place_id: {pid}")
                try:
                    pname, address, reviews = get_reviews(pid)
                    if reviews:
                        saved = save_reviews(pname, address, reviews, existing)
                        print(f"리뷰 {saved}개 저장 완료")
                        print(f"누적 리뷰 수: {total_reviews_collected}개")
                        if os.path.exists(filename):
                            with open(filename, "r", encoding="utf-8-sig") as f:
                                current_total = sum(1 for _ in f) - 1
                                print(f"현재 저장된 총 리뷰 수: {current_total}개")
                    else:
                        print("리뷰 없음")
                except Exception as e:
                    print(f"오류 발생: {e}")
                time.sleep(1)


if __name__ == "__main__":
    run_collection()