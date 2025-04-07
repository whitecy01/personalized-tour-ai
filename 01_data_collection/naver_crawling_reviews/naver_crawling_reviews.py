from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 크롬 브라우저 설정
options = Options()
options.add_argument("--start-maximized")

# 드라이버 설정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

# 검색 페이지 열기
driver.get("https://map.naver.com/p/search/해운대구 맛집")
time.sleep(5)

# searchIframe 진입
try:
    wait.until(EC.presence_of_element_located((By.ID, "searchIframe")))
    driver.switch_to.frame("searchIframe")
    print("[✅] searchIframe 진입 성공")
except Exception as e:
    print("[❌] searchIframe 진입 실패:", e)
    driver.quit()
    exit()

# 리스트 컨테이너 확인
try:
    container = wait.until(EC.presence_of_element_located((By.ID, "_pcmap_list_scroll_container")))
    print("[✅] 가게 리스트 컨테이너 진입 성공!")
except Exception as e:
    print("[❌] 가게 리스트 컨테이너 진입 실패:", e)
    driver.quit()
    exit()

# 가게 항목 반복
try:
    store_items = container.find_elements(By.CSS_SELECTOR, 'li.UEzoS.rTjJo')
    print(f"📌 가게 항목 수: {len(store_items)}")

    for i, li in enumerate(store_items[:5]):
        print(f"\n[{i+1}] li element info:")
        print(" - class:", li.get_attribute("class"))
        print(" - text snippet:", li.text[:100])

        # li 클릭
        try:
            li.click()
            time.sleep(3)


            driver.switch_to.default_content()

            # sub_panel 접근 성공
            wait.until(EC.presence_of_element_located((By.ID, "sub_panel")))
            print("[🎯] sub_panel 접근 성공!")
            # 5. entryIframe 진입
            wait.until(EC.presence_of_element_located((By.ID, "entryIframe")))
            driver.switch_to.frame("entryIframe")
            print("[✅] entryIframe 진입 성공")

            # id 속성이 있는 모든 요소 찾기
            # try:
            #     print("[🔍] entryIframe 내부 id 속성 있는 요소 목록:")
            #     elements_with_id = driver.find_elements(By.XPATH, '//*[@id]')

            #     for idx, el in enumerate(elements_with_id):
            #         el_id = el.get_attribute("id")
            #         el_tag = el.tag_name
            #         print(f"  [{idx+1}] tag: {el_tag}, id: {el_id}")
                
            #     print(f"\n[📦] 총 {len(elements_with_id)}개의 id 속성 요소 탐지됨")

            # except Exception as e:
            #     print(f"[❌] id 속성 요소 탐색 실패: {e}")

            # app-root로 들어가기
            app_root = wait.until(EC.presence_of_element_located((By.ID, "app-root")))
            print("[✅] app-root 접근 성공")

            review_tab = app_root.find_element(By.CSS_SELECTOR, "div.place_fixed_maintab")
            veBoZ_spans = review_tab.find_elements(By.CSS_SELECTOR, "span.veBoZ")
            for span in veBoZ_spans:
                if "리뷰" in span.text:
                    print(f"[🧭] 리뷰 탭 발견: {span.text}")
                    span.click()
                    print("[✅] 리뷰 탭 클릭 완료")
                    break
            else:
                print("[❌] 리뷰 탭 span.veBoZ 요소를 찾았지만 '리뷰' 텍스트 없음")
            time.sleep(5)

            #리뷰 탭 클릭 후 entryIframe안에서 리뷰 목록 수집
            # review_section = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.place_section.k1QQ5")))
            try:
                review_section = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.place_section.k1QQ5")))
                print("[✅] place_section.k1QQ5 접근 성공!")

   
                ul_elements = review_section.find_elements(By.TAG_NAME, "ul")

                    # 2. 자식 엘리먼트들 추출
                child_elements = review_section.find_elements(By.XPATH, "./*")
                print(f"[📦] 자식 요소 개수: {len(child_elements)}")

                # 3. 각각의 태그, 클래스, 텍스트 일부 출력
                for idx, elem in enumerate(child_elements):
                    tag = elem.tag_name
                    cls = elem.get_attribute("class")
                    txt = elem.text.strip()
                    print(f"  [{idx+1}] 태그: <{tag}> | class: {cls} | 내용 일부: {txt[:50]}{'...' if len(txt) > 50 else ''}")


    
                # for ul_idx, ul in enumerate(ul_elements):
                #     li_elements = ul.find_elements(By.TAG_NAME, "li")
                #     print(f"\n[🔍 ul {ul_idx+1}] li 개수: {len(li_elements)}")

                #     for idx, li in enumerate(li_elements):
                #         print(f"  [{idx+1}] li 항목 분석")

                #         try:
                #             # lazyload-wrapper 안의 구조 접근
                #             lazyload_div = li.find_element(By.CSS_SELECTOR, "div.lazyload-wrapper")
                #             nggkh_div = lazyload_div.find_element(By.CSS_SELECTOR, "div.ngGKH")
                #             flicking_div = nggkh_div.find_element(By.CSS_SELECTOR, "div.flicking-viewport")

                #             a_tags = flicking_div.find_elements(By.TAG_NAME, "a")
                #             print(f"    🔗 flicking-viewport 안의 <a> 태그 개수: {len(a_tags)}")

                #             for a_idx, a in enumerate(a_tags):
                #                 print(f"      [{a_idx+1}] href: {a.get_attribute('href')} | class: {a.get_attribute('class')}")
                #         except Exception as e:
                #             print(f"    ⚠️ 구조 분석 실패: {e}")
                #             for idx, ul in enumerate(ul_elements):
                #                 print(f"\n[{idx+1}] [ul element]")
                #                 print(" - class:", ul.get_attribute("class"))

                #                 # ul 안에 있는 li 요소들 모두 출력
                #                 li_elements = ul.find_elements(By.TAG_NAME, "li")
                #                 print(f" - li 개수: {len(li_elements)}")






                    # for jdx, li in enumerate(li_elements):
                    #     print(li)
                    #     try:
                    #         # lazyload-wrapper 내부 진입
                    #         lazyload_div = li.find_element(By.CSS_SELECTOR, "div.lazyload-wrapper")
                    #         print(f"    ✅ lazyload-wrapper 진입 성공")
                    #         nggkh_div = lazyload_div.find_element(By.CSS_SELECTOR, "div.ngGKH")
                    #         print("  ✅ ngGKH 접근 성공")

                    #         # 내부 모든 자식 태그 탐색
                    #         inner_elements = lazyload_div.find_elements(By.XPATH, "./*")
                    #         print(f"    📦 내부 태그 개수: {len(inner_elements)}")

                    #         # 각 태그 정보 출력
                    #         for kdx, elem in enumerate(inner_elements):
                    #             tag = elem.tag_name
                    #             cls = elem.get_attribute("class")
                    #             txt = elem.text.strip()
                    #             print(f"      [{kdx+1}] 태그: <{tag}>, class: {cls}, 내용: {txt[:50]}{'...' if len(txt) > 50 else ''}")

                    #     except Exception as e:
                    #         print(f"    ⚠️ lazyload-wrapper 진입 실패: {e}")


            except Exception as e:
                print(f"[❌] 리뷰 섹션 내부 구조 출력 실패: {e}")
            time.sleep(5)

            # review_items = driver.find_elements(By.CSS_SELECTOR, "li.place_apply_pui.EjiAW")

            # print(f"[📋] 리뷰 항목 수: {len(review_items)}")
            # for idx, item in enumerate(review_items[:5]):  # 상위 5개 리뷰만 예시 출력
            #     text = item.text.strip()
            #     print(f"  [{idx+1}] 리뷰 내용 요약: {text[:100]}")

            # driver.switch_to.default_content()

            # # 상세 패널 열림 확인
            # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.Fc1rA")))
            # place_name = driver.find_element(By.CSS_SELECTOR, "span.Fc1rA").text
            # print(f"[✅] 상세 패널 열림 확인됨! 가게명: {place_name}")
            # print(f"[✅] 상세 패널 열림 확인됨! ")

            # # ✅ place_fixed_maintab 내부 요소 출력
            # print("[🔍] place_fixed_maintab 내부 요소 확인 중...")
            # # sub_panel = wait.until(EC.presence_of_element_located((By.ID, "app-layout")))
            # wait.until(EC.presence_of_element_located((By.ID, "sub_panel")))
            # print("[🎯] sub_panel 요소 접근 성공!")

            # maintab = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.place_on_pcmap")))
            print("성공")
            # maintab = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.app-root")))
            # maintab = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.place_fixed_maintab")))
            # children = maintab.find_elements(By.XPATH, "./*")

            # for idx, child in enumerate(children):
            #     tag = child.tag_name
            #     cls = child.get_attribute("class")
            #     text = child.text.strip()
            #     print(f"  [{idx+1}] tag: {tag}, class: {cls}, text: {text[:50]}")
        except Exception as e:
            print(f"[❌] 상세 패널 열기 실패: {e}")
            continue

except Exception as e:
    print("[❌] 가게 항목 처리 실패:", e)

driver.quit()
