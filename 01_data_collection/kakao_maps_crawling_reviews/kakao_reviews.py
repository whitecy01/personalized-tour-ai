from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys  # ← 이거 추가 필수!


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # 필요 시 UI 없이 실행

driver = webdriver.Chrome(options=options)

try:
    # 1. 카카오맵 접속
    driver.get("https://map.kakao.com/")
    time.sleep(2)

    # 2. 검색창에 "해운대 카페" 입력하고 검색
    search_input = driver.find_element(By.ID, "search.keyword.query")
    search_input.send_keys("해운대 맛집" + Keys.ENTER)  # ← 엔터를 눌러서 검색
    time.sleep(2)

    print("[1] 검색 완료")

    # 3. div#info.main 확인
    info_main = driver.find_element(By.ID, "info.main")
    print("[2] info.main 진입 확인")

    # 4. div#info.search 확인
    info_search = driver.find_element(By.ID, "info.search")
    print("[3] info.search 진입 확인")

    # 5. div#info.search.place 확인
    info_search_place = driver.find_element(By.ID, "info.search.place")
    print("[4] info.search.place 진입 확인")

    # 6. ul#info.search.place.list 확인
    place_list_ul = driver.find_element(By.ID, "info.search.place.list")
    print("[5] info.search.place.list 진입 확인")

    # 7. li 중 첫 번째 가게 클릭
    li_elements = place_list_ul.find_elements(By.TAG_NAME, "li")
    print(f"[6] 검색 결과 {len(li_elements)}개 탐지됨")


    # "더보기" 버튼 클릭으로 200개 이상 li 확보

    li_elements = place_list_ul.find_elements(By.TAG_NAME, "li")
    print(f"[6] 초기 검색 결과: {len(li_elements)}개 탐지됨")

    # '더보기' 버튼이 존재하는 경우 한 번만 클릭
    place_div = driver.find_element(By.ID, "info.search.place")
    more_btns = place_div.find_elements(By.ID, "info.search.place.more")
    
    if more_btns:
        more_btn = more_btns[0]
        print("🔎 '더보기' 버튼 존재 → 클릭 시도")
        driver.execute_script("arguments[0].click();", more_btn)
        time.sleep(1.5)

        # li 다시 업데이트
        li_elements = place_list_ul.find_elements(By.TAG_NAME, "li")
        print(f"✅ '더보기' 클릭 후 li 개수: {len(li_elements)}개")
    else:
        print("ℹ️ '더보기' 버튼 없음 → 클릭 생략")

    print(f"✅ 최종 li 개수: {len(li_elements)}개 확보 완료")

    # time.sleep(20)

    if len(li_elements) == 0:
        print("검색 결과가 없습니다.")
        driver.quit()
        exit()
    
    for place_idx in range(len(li_elements)):
        print(f"\n🏪 장소 {place_idx + 1} 진입 중...")
            # 매번 새로 ul, li 탐색 (페이지 돌아오면 새로 렌더링됨)
        place_list_ul = driver.find_element(By.ID, "info.search.place.list")
        li_elements = place_list_ul.find_elements(By.TAG_NAME, "li")


        # 현재 li 선택
        current_li = li_elements[place_idx]
        try:
            rating_div = current_li.find_element(By.CSS_SELECTOR, "div[data-id='rating']")
            review_link = rating_div.find_element(By.TAG_NAME, "a").get_attribute("href")
        except Exception as e:
            print(f"❌ 장소 {place_idx + 1} 리뷰 링크 추출 실패: {e}")
            continue
        # 리뷰 페이지로 이동
        driver.get(review_link)
        time.sleep(2)
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
        section_review = detail_cont.find_element(By.CLASS_NAME, "section_review")
        print("[14] div.section_review 진입 성공")

        # 6. div.group_review
        group_review = section_review.find_element(By.CLASS_NAME, "group_review")
        print("[15] div.group_review 진입 성공")

        # 7. ul.list_review
        ul_list_review = group_review.find_element(By.CLASS_NAME, "list_review")
        print("[16] ul.list_review 진입 성공")

        
        # 2. ul 안의 모든 div.inner_review 가져오기
        inner_reviews = ul_list_review.find_elements(By.CLASS_NAME, "inner_review")
        print(f"✅ inner_review 개수: {len(inner_reviews)}개")


        SCROLL_PAUSE = 1.5
        MAX_SCROLL = 10
        scroll_count = 0

        # inner_review가 30개 이상 될 때까지 스크롤
        while len(inner_reviews) < 30 and scroll_count < MAX_SCROLL:
            print(f"🔁 inner_review 개수 {len(inner_reviews)}개 → 스크롤 중... ({scroll_count + 1}회차)")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE)

            # 다시 가져오기 (초기화)
            inner_reviews = ul_list_review.find_elements(By.CLASS_NAME, "inner_review")
            scroll_count += 1

        print(f"✅ inner_review 개수: {len(inner_reviews)}개 (스크롤 {scroll_count}회 수행 완료)")

        # 3. 각 inner_review 구조 확인
        for idx, inner in enumerate(inner_reviews):
            print(f"\n🔍 리뷰 {idx+1} 구조:")
            # print(inner.get_attribute("outerHTML"))
            name_span = inner.find_element(By.CLASS_NAME, "name_user")
            reviewer_name = name_span.text.strip()

            # 2. 후기 개수: ul.list_detail > 첫 번째 li
            list_detail = inner.find_element(By.CLASS_NAME, "list_detail")
            first_li = list_detail.find_elements(By.TAG_NAME, "li")[0]
            review_count = first_li.text.strip().replace("후기", "").strip()  # "후기 131" → "131"

            # 3. 별점
            grade_span = inner.find_element(By.CLASS_NAME, "starred_grade")
            print(f"\n🔎 리뷰 {idx+1} - grade_span 구조:")
            # print(grade_span.get_attribute("outerHTML"))
            screen_outs = grade_span.find_elements(By.CLASS_NAME, "screen_out")
            # for i, tag in enumerate(screen_outs):
            #     print(f"  🔹 screen_out {i+1}: {tag.get_attribute('outerHTML')}")

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
            # try:
            #     # "더보기" 버튼이 있는지 확인
            #     more_btn = desc_p.find_element(By.CLASS_NAME, "btn_more")
            #     driver.execute_script("arguments[0].click();", more_btn)  # JS로 클릭 (숨김 요소 대비)
            #     time.sleep(0.3)  # 클릭 후 리뷰 확장 대기
            # except:
            #     pass  # 더보기 버튼이 없으면 넘어감
            # review_text = desc_p.text.strip()

            # if review_text.endswith("접기"):
            #     review_text = review_text[:-2].strip()  # "접기" 제거

            print(f"\n🧑 리뷰 {idx+1}")
            print(f"작성자: {reviewer_name}")
            print(f"후기 수: {review_count}")
            print(f"⭐ 별점: {star_rating}")
            print(f"🗓️ 작성일: {review_date}")
            print(f"📷 사진 있음?: {has_photo}")
            print(f"📝 내용: {review_text}")



        # 리뷰 수집 완료 후 → 다시 지도 페이지로 돌아가기
        driver.back()
        time.sleep(2)
        print(f"🔙 지도 페이지로 복귀 완료")




        
 




except Exception as e:
    print("오류 발생:", e)

finally:
    driver.quit()
