from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys  # ← 이거 추가 필수!
import csv
import os


def save_to_csv(place_name, category, address, score, reviewer_name, review_text, has_photo, star_rating, review_date, review_link, review_count):
    key = (place_name, address, reviewer_name)

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8-sig") as f:
            line_count = sum(1 for _ in f)
            if line_count >= 190001:  # 헤더 포함 10,000줄 제한
                print("CSV 줄 수가 10,000줄을 초과하여 프로그램을 종료합니다.")
                driver.quit()
                exit()

    if key not in existing_keys:
        with open(filename, "a", newline="", encoding="utf-8-sig") as f:
            fieldnames = ["가게명", "업종", "주소", "총평점", "작성자", "리뷰내용", "사진유무", "별점", "작성시간", "리뷰 페이지", "사용자총리뷰수"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if os.stat(filename).st_size == 0:
                writer.writeheader()

            writer.writerow({
                "가게명": place_name,
                "업종": category,
                "주소": address,
                "총평점": score,
                "작성자": reviewer_name,
                "리뷰내용": review_text,
                "사진유무": has_photo,
                "별점": star_rating,
                "작성시간": review_date,
                "리뷰 페이지": review_link,
                "사용자총리뷰수" : review_count
            })
            
        existing_keys.add(key)
    else:
        print(f"중복으로 저장 생략: {place_name} - {reviewer_name}")


# 저장할 파일명
filename = "kakao_maps_review.csv"


# 저장할 데이터 구조 예시 (이걸 for 루프 내에서 반복)
# place_name = "해운대암소갈비집"
# category = "한식"
# address = "부산 해운대구 구남로..."
# score = "4.2"
# reviewer_name = "효도왕이승민"
# review_text = "고기가 맛있다!"
# has_photo = 1
# star_rating = "5.0"
# review_date = "2024.10.10"
# review_link = "https://place.map.kakao.com/123456"

# 기존 데이터 로드
existing_keys = set()
if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["가게명"], row["주소"], row["작성자"])
            existing_keys.add(key)


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # 필요 시 UI 없이 실행

driver = webdriver.Chrome(options=options)

try:
    # 1. 카카오맵 접속
    driver.get("https://map.kakao.com/")
    time.sleep(1.5)

    # 2. 검색창에 "해운대 카페" 입력하고 검색
    search_input = driver.find_element(By.ID, "search.keyword.query")
    search_input.send_keys("송정 해수욕장 맛집" + Keys.ENTER)  # ← 엔터를 눌러서 검색
    time.sleep(1.5)

    print("[1] 검색 완료")

    # 3. div#info.main 확인
    info_main = driver.find_element(By.ID, "info.main")
    print("[2] info.main 진입 확인")
    time.sleep(1.5)
    # 4. div#info.search 확인
    info_search = driver.find_element(By.ID, "info.search")
    print("[3] info.search 진입 확인")

    # 5. div#info.search.place 확인
    info_search_place = driver.find_element(By.ID, "info.search.place")
    print("[4] info.search.place 진입 확인")
    time.sleep(1.5)
    # 6. ul#info.search.place.list 확인
    place_list_ul = driver.find_element(By.ID, "info.search.place.list")
    print("[5] info.search.place.list 진입 확인")

    # 7. li 중 첫 번째 가게 클릭
    li_elements = place_list_ul.find_elements(By.TAG_NAME, "li")
    print(f"[6] 검색 결과 {len(li_elements)}개 탐지됨")


    # "더보기" 버튼 클릭으로 200개 이상 li 확보
    li_elements = place_list_ul.find_elements(By.TAG_NAME, "li")
    print(f"[6] 초기 검색 결과: {len(li_elements)}개 탐지됨")
    time.sleep(1.5)
    # '더보기' 버튼이 존재하는 경우 한 번만 클릭
    place_div = driver.find_element(By.ID, "info.search.place")
    more_btns = place_div.find_elements(By.ID, "info.search.place.more")
    

    if more_btns:
        more_btn = more_btns[0]
        driver.execute_script("arguments[0].click();", more_btn)
        time.sleep(1.5)
        
        # 여기서 먼저 각 페이지네이션해주는 버튼의 길이 체크
        # 페이지네이션 루프
        while True:
            # 페이지네이션 버튼 리스트 가져오기
            page_section = driver.find_element(By.ID, "info.search.page")
            page_buttons = page_section.find_elements(By.CSS_SELECTOR, "a[id^='info.search.page.no']")

            for btn in page_buttons:
                if 'HIDDEN' in btn.get_attribute("class"):
                    continue  # 보이지 않는 버튼은 무시

                page_num = btn.text.strip()
                print(f"\n페이지 {page_num} 클릭 중...")

                driver.execute_script("arguments[0].click();", btn)
                time.sleep(1.5)

                # 장소 li 목록 업데이트
                place_list_ul = driver.find_element(By.ID, "info.search.place.list")
                li_elements = place_list_ul.find_elements(By.TAG_NAME, "li")

                print(f"페이지 {page_num} - 장소 수: {len(li_elements)}개")

                for place_idx in range(len(li_elements)):
                    # 리뷰 데이터 글거 오는 코드 삽입
                    print(f"\n장소 {place_idx + 1} 진입 중...")
                    # 매번 새로 ul, li 탐색 (페이지 돌아오면 새로 렌더링됨)
                    place_list_ul = driver.find_element(By.ID, "info.search.place.list")
                    li_elements = place_list_ul.find_elements(By.TAG_NAME, "li")

                    
                    # 현재 li 선택
                    current_li = li_elements[place_idx]
                    try:
                        # 점수 span 태그 탐색
                        score_span = current_li.find_element(By.CSS_SELECTOR, "span[data-id='score']")
                        score_class = score_span.get_attribute("class")

                        if "HIDDEN" in score_class:
                            print(f"장소 {place_idx + 1}: 리뷰 없음 (score 클래스 → HIDDEN) → 건너뜀")
                            continue

                        rating_div = current_li.find_element(By.CSS_SELECTOR, "div[data-id='rating']")
                        review_link = rating_div.find_element(By.TAG_NAME, "a").get_attribute("href")
                    except Exception as e:
                        print(f"장소 {place_idx + 1} 리뷰 링크 추출 실패: {e}")
                        continue

                    #가게이름, 가게 종류(키워드), 총 평점, 위치
                    # 1. 가게명 (a 태그, data-id="name")
                    name_tag = current_li.find_element(By.CSS_SELECTOR, 'a[data-id="name"]')
                    place_name = name_tag.text.strip()

                    # 2. 업종/카테고리 (span 태그, data-id="subcategory")
                    category_tag = current_li.find_element(By.CSS_SELECTOR, 'span[data-id="subcategory"]')
                    category = category_tag.text.strip()

                    # 3. 평점 (em 태그, data-id="scoreNum") - 없을 수도 있음
                    score_tag = current_li.find_element(By.CSS_SELECTOR, 'em[data-id="scoreNum"]')
                    score = score_tag.text.strip()

                    address_tag = current_li.find_element(By.CSS_SELECTOR, 'p[data-id="address"]')
                    address = address_tag.text.strip()

                    print(f"가게명: {place_name}")
                    # print(f"업종: {category}")
                    # print(f"평점: {score}")
                    # print(f"주소: {address}")
                    # print(f"링크: {review_link}")
                    time.sleep(2)

                    # 리뷰 페이지로 이동
                    driver.get(review_link)
                    time.sleep(1.5)
                    print(f"[{place_idx+1}] 리뷰 페이지 진입 완료")

                    # [추가] 리뷰 영역에서 리뷰들 가져오기
                    # 1. main.doc-main
                    main = driver.find_element(By.CLASS_NAME, "doc-main")
                    print("[10] main.doc-main 진입 성공")

                    # 2. article#mainContent
                    article = main.find_element(By.ID, "mainContent")
                    print("[11] article#mainContent 진입 성공")

                    # 3. div.main_detail
                    main_detail = article.find_element(By.CLASS_NAME, "main_detail")
                    print("[12] div.main_detail 진입 성공")

                    # 4. div.detail_cont
                    detail_cont = main_detail.find_element(By.CLASS_NAME, "detail_cont")
                    print("[13] div.detail_cont 진입 성공")

                    # 5. div.section_review
                    try:
                        section_review = detail_cont.find_element(By.CLASS_NAME, "section_review")
                        print("[14] div.section_review 진입 성공")
                    except Exception as e:
                        print(f"section_review 탐색 실패: {e}")
                        driver.back()
                        time.sleep(1.5)
                        print(f"지도 페이지로 복귀 완료")
                        continue  # 다음 장소로 이동

                    # 6. div.group_review
                    group_review = section_review.find_element(By.CLASS_NAME, "group_review")
                    print("[15] div.group_review 진입 성공")

                    # 7. ul.list_review
                    ul_list_review = group_review.find_element(By.CLASS_NAME, "list_review")
                    print("[16] ul.list_review 진입 성공")

                    
                    # 2. ul 안의 모든 div.inner_review 가져오기
                    inner_reviews = ul_list_review.find_elements(By.CLASS_NAME, "inner_review")
                    print(f"inner_review 개수: {len(inner_reviews)}개")


                    SCROLL_PAUSE = 1.5
                    MAX_SCROLL = 10
                    scroll_count = 0

                    # inner_review가 30개 이상 될 때까지 스크롤
                    while len(inner_reviews) < 80 and scroll_count < MAX_SCROLL:
                        print(f"inner_review 개수 {len(inner_reviews)}개 → 스크롤 중... ({scroll_count + 1}회차)")
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(SCROLL_PAUSE)

                        # 다시 가져오기 (초기화)
                        inner_reviews = ul_list_review.find_elements(By.CLASS_NAME, "inner_review")
                        scroll_count += 1

                    print(f"inner_review 개수: {len(inner_reviews)}개 (스크롤 {scroll_count}회 수행 완료)")

                    # 3. 각 inner_review 구조 확인
                    for idx, inner in enumerate(inner_reviews):
                        try:
                            name_span = inner.find_element(By.CLASS_NAME, "name_user")
                            reviewer_name = name_span.text.strip()
                        except:
                            reviewer_name = "SYSTEM_이름없음"
                            print(f"리뷰 {idx+1}: name_user 없음 → 기본값 설정")

                        # 2. 후기 개수: ul.list_detail > 첫 번째 li
                        list_detail = inner.find_element(By.CLASS_NAME, "list_detail")
                        first_li = list_detail.find_elements(By.TAG_NAME, "li")[0]
                        review_count = first_li.text.strip().replace("후기", "").strip()  # "후기 131" → "131"

                        # 3. 별점
                        try:
                            grade_span = inner.find_element(By.CLASS_NAME, "starred_grade")
                        except:
                            print(f"리뷰 {idx+1}: 별점 요소 없음 → 건너뜀")
                            continue

                        screen_outs = grade_span.find_elements(By.CLASS_NAME, "screen_out")

                        # 별점은 두 번째 screen_out에서 추출
                        if len(screen_outs) > 1:
                            # ★ 여기서 .text 대신 innerText로 바꿈!
                            star_rating = screen_outs[1].get_attribute("innerText").strip()
                        else:
                            star_rating = "N/A"

                        # 4. 작성일 추출
                        date_span = inner.find_element(By.CLASS_NAME, "txt_date")
                        review_date = date_span.text.strip()

                        # 5. 사진 유무 확인
                        info_review_div = inner.find_element(By.CLASS_NAME, "info_review")
                        has_photo = 1 if info_review_div.find_elements(By.CLASS_NAME, "review_thumb") else 0

                        # print("here")
                        # 6. 리뷰 본문 추출 (더보기 클릭 포함)
                        desc_p = inner.find_elements(By.CLASS_NAME, "desc_review")

                        if desc_p:
                            desc_p = desc_p[0]

                            try:
                                # 더보기 버튼 있는 경우 클릭
                                more_btn = desc_p.find_element(By.CLASS_NAME, "btn_more")
                                driver.execute_script("arguments[0].click();", more_btn)
                                time.sleep(0.3)
                            except:
                                pass

                            review_text = desc_p.text.strip()
                            if review_text.endswith("접기"):
                                review_text = review_text[:-2].strip()
                        else:
                            review_text = "리뷰 없음"

                        # print(f"\n🧑 리뷰 {idx+1}")
                        # print(f"작성자: {reviewer_name}")
                        # print(f"후기 수: {review_count}")
                        # print(f"⭐ 별점: {star_rating}")
                        # print(f"🗓️ 작성일: {review_date}")
                        # print(f"📷 사진 있음?: {has_photo}")
                        # print(f"📝 내용: {review_text}")
                        
                        # 저장
                        save_to_csv(place_name, category, address, score, reviewer_name, review_text, has_photo, star_rating, review_date, review_link, review_count)


                    # 리뷰 수집 완료 후 → 다시 지도 페이지로 돌아가기
                    print("저장완료")
                    driver.back()
                    time.sleep(1.5)
                    print(f"지도 페이지로 복귀 완료")
                    pass

            # 다음 페이지 버튼 확인
            next_btn = page_section.find_element(By.ID, "info.search.page.next")
            next_class = next_btn.get_attribute("class")

            if "disabled" in next_class:
                print("다음 페이지 없음 → 종료")
                break
            else:
                print("다음 페이지 세트 이동")
                driver.execute_script("arguments[0].click();", next_btn)
                time.sleep(1.5)
    else:
        print("'더보기' 버튼 없음 → 현재 페이지 내 li만 순회")
        print(f"최종 li 개수: {len(li_elements)}개 확보 완료")

        # time.sleep(20)

        if len(li_elements) == 0:
            print("검색 결과가 없습니다.")
            driver.quit()
            exit()
        for place_idx in range(len(li_elements)):
            print(f"\n장소 {place_idx + 1} 진입 중...")
                # 매번 새로 ul, li 탐색 (페이지 돌아오면 새로 렌더링됨)
            place_list_ul = driver.find_element(By.ID, "info.search.place.list")
            li_elements = place_list_ul.find_elements(By.TAG_NAME, "li")


            # 현재 li 선택
            current_li = li_elements[place_idx]
            try:
                # 점수 span 태그 탐색
                score_span = current_li.find_element(By.CSS_SELECTOR, "span[data-id='score']")
                score_class = score_span.get_attribute("class")

                if "HIDDEN" in score_class:
                    print(f"장소 {place_idx + 1}: 리뷰 없음 (score 클래스 → HIDDEN) → 건너뜀")
                    continue                
                rating_div = current_li.find_element(By.CSS_SELECTOR, "div[data-id='rating']")
                review_link = rating_div.find_element(By.TAG_NAME, "a").get_attribute("href")
            except Exception as e:
                print(f"장소 {place_idx + 1} 리뷰 링크 추출 실패: {e}")
                continue

            #가게이름, 가게 종류(키워드), 총 평점, 위치
            # 1. 가게명 (a 태그, data-id="name")
            name_tag = current_li.find_element(By.CSS_SELECTOR, 'a[data-id="name"]')
            place_name = name_tag.text.strip()

            # 2. 업종/카테고리 (span 태그, data-id="subcategory")
            category_tag = current_li.find_element(By.CSS_SELECTOR, 'span[data-id="subcategory"]')
            category = category_tag.text.strip()

            # 3. 평점 (em 태그, data-id="scoreNum") - 없을 수도 있음
            score_tag = current_li.find_element(By.CSS_SELECTOR, 'em[data-id="scoreNum"]')
            score = score_tag.text.strip()

            address_tag = current_li.find_element(By.CSS_SELECTOR, 'p[data-id="address"]')
            address = address_tag.text.strip()

            print(f"가게명: {place_name}")
            # print(f"업종: {category}")
            # print(f"평점: {score}")
            # print(f"주소: {address}")
            # print(f"링크: {review_link}")
            # 리뷰 페이지로 이동
            driver.get(review_link)
            time.sleep(1.5)

            print(f"[{place_idx+1}] 리뷰 페이지 진입 완료")

            # [추가] 리뷰 영역에서 리뷰들 가져오기

            # 1. main.doc-main
            main = driver.find_element(By.CLASS_NAME, "doc-main")
            print("[10] main.doc-main 진입 성공")

            # 2. article#mainContent
            article = main.find_element(By.ID, "mainContent")
            print("[11] article#mainContent 진입 성공")

            # 3. div.main_detail
            main_detail = article.find_element(By.CLASS_NAME, "main_detail")
            print("[12] div.main_detail 진입 성공")

            # 4. div.detail_cont
            detail_cont = main_detail.find_element(By.CLASS_NAME, "detail_cont")
            print("[13] div.detail_cont 진입 성공")

            # 5. div.section_review
            try:
                section_review = detail_cont.find_element(By.CLASS_NAME, "section_review")
                print("[14] div.section_review 진입 성공")
            except Exception as e:
                print(f"section_review 탐색 실패: {e}")
                driver.back()
                time.sleep(1.5)
                print(f"지도 페이지로 복귀 완료")
                continue  # 다음 장소로 이동

            # 6. div.group_review
            group_review = section_review.find_element(By.CLASS_NAME, "group_review")
            print("[15] div.group_review 진입 성공")

            # 7. ul.list_review
            ul_list_review = group_review.find_element(By.CLASS_NAME, "list_review")
            print("[16] ul.list_review 진입 성공")

            
            # 2. ul 안의 모든 div.inner_review 가져오기
            inner_reviews = ul_list_review.find_elements(By.CLASS_NAME, "inner_review")
            print(f"inner_review 개수: {len(inner_reviews)}개")


            SCROLL_PAUSE = 1.5
            MAX_SCROLL = 10
            scroll_count = 0

            # inner_review가 30개 이상 될 때까지 스크롤
            while len(inner_reviews) < 80 and scroll_count < MAX_SCROLL:
                print(f"inner_review 개수 {len(inner_reviews)}개 → 스크롤 중... ({scroll_count + 1}회차)")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL_PAUSE)

                # 다시 가져오기 (초기화)
                inner_reviews = ul_list_review.find_elements(By.CLASS_NAME, "inner_review")
                scroll_count += 1

            print(f"inner_review 개수: {len(inner_reviews)}개 (스크롤 {scroll_count}회 수행 완료)")

            # 3. 각 inner_review 구조 확인
            for idx, inner in enumerate(inner_reviews):
                try:
                    name_span = inner.find_element(By.CLASS_NAME, "name_user")
                    reviewer_name = name_span.text.strip()
                except:
                    reviewer_name = "SYSTEM_이름없음"
                    print(f"리뷰 {idx+1}: name_user 없음 → 기본값 설정")

                # 2. 후기 개수: ul.list_detail > 첫 번째 li
                list_detail = inner.find_element(By.CLASS_NAME, "list_detail")
                first_li = list_detail.find_elements(By.TAG_NAME, "li")[0]
                review_count = first_li.text.strip().replace("후기", "").strip()  # "후기 131" → "131"

                # 3. 별점
                try:
                    grade_span = inner.find_element(By.CLASS_NAME, "starred_grade")
                except:
                    print(f"리뷰 {idx+1}: 별점 요소 없음 → 건너뜀")
                    continue
                screen_outs = grade_span.find_elements(By.CLASS_NAME, "screen_out")

                # 별점은 두 번째 screen_out에서 추출
                if len(screen_outs) > 1:
                    # ★ 여기서 .text 대신 innerText로 바꿈!
                    star_rating = screen_outs[1].get_attribute("innerText").strip()
                else:
                    star_rating = "N/A"

                # 4. 작성일 추출
                date_span = inner.find_element(By.CLASS_NAME, "txt_date")
                review_date = date_span.text.strip()

                # 5. 사진 유무 확인
                info_review_div = inner.find_element(By.CLASS_NAME, "info_review")
                has_photo = 1 if info_review_div.find_elements(By.CLASS_NAME, "review_thumb") else 0

                print("here")
                # 6. 리뷰 본문 추출 (더보기 클릭 포함)
                desc_p = inner.find_elements(By.CLASS_NAME, "desc_review")

                if desc_p:
                    desc_p = desc_p[0]

                    try:
                        # 더보기 버튼 있는 경우 클릭
                        more_btn = desc_p.find_element(By.CLASS_NAME, "btn_more")
                        driver.execute_script("arguments[0].click();", more_btn)
                        time.sleep(0.3)
                    except:
                        pass

                    review_text = desc_p.text.strip()
                    if review_text.endswith("접기"):
                        review_text = review_text[:-2].strip()
                else:
                    review_text = "리뷰 없음"

                # print(f"\n리뷰 {idx+1}")
                # print(f"작성자: {reviewer_name}")
                # print(f"후기 수: {review_count}")
                # print(f"별점: {star_rating}")
                # print(f"작성일: {review_date}")
                # print(f"사진 있음?: {has_photo}")
                # print(f"내용: {review_text}")

                # 저장
                save_to_csv(place_name, category, address, score, reviewer_name, review_text, has_photo, star_rating, review_date, review_link, review_count)


            # 리뷰 수집 완료 후 → 다시 지도 페이지로 돌아가기
            print("저장완료")
            driver.back()
            time.sleep(1.5)
            print(f"지도 페이지로 복귀 완료")
    
    # time.sleep(1000)

except Exception as e:
    print("오류 발생:", e)

finally:
    driver.quit()
