import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import time
import re
# 셀레니움 드라이버 설정
options = Options()
# options.add_argument('--headless=new')
options.add_argument('--start-maximized')
options.add_argument('--no-sandbox')             # sandbox 환경 오류 방지
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless=new")

driver = webdriver.Chrome(service=Service(), options=options)

# CSV 파일 경로
file_path = '/Users/jeongjaeyoon/Documents/GitHub/personalized-tour-ai/google_maps_review.csv'
df = pd.read_csv(file_path, encoding='utf-8-sig')

# 리뷰 페이지 순회 
# for idx, row in df.iterrows():
# for idx, row in df[df['사용자총리뷰수'].isna()].iterrows():
for idx in range(7460, len(df)):
    row = df.iloc[idx] # 추가
        
    if pd.notna(row['사용자총리뷰수']): # 만약 사용자총리뷰수가 비어있지 않으면 패스 == 추가
        continue

    target_name = row['가게명']
    review_url = row['리뷰 페이지']

    print(f"\n[{idx + 1}] 접속 중: {review_url}")
    driver.get(review_url)
    time.sleep(3)

    found = False
    scroll_try = 0
    scroll_amount = 30000  # 초기 스크롤 양

    while not found and scroll_try < 50:  # 최대 20회 시도
        # review_blocks = driver.find_elements(By.CLASS_NAME, 'jftiEf')
        try:
            review_blocks = driver.find_elements(By.CLASS_NAME, 'jftiEf')
        except Exception as e:
            print(f"❌ jftiEf 요소 탐색 중 예외 발생: {e}")
            break  # 요소 탐색 자체에 실패한 경우 중단

        

        if not review_blocks:
            print(f"[{idx+1}] jftiEf 요소 없음 → 리뷰 없음으로 간주하고 중단")
            break  # jftiEf 요소가 없으면 리뷰 블럭이 없는 것으로 간주하고 중단
        current_count = len(review_blocks)

        if not review_blocks:
            print(f"[{idx+1}] 리뷰 블럭이 비어있음 → 스크롤 시도 {scroll_try+1}회")
        else:
            for block in review_blocks:
                try:
                    store_name = block.find_element(By.CSS_SELECTOR, 'div.d4r55.YJxk2d').text.strip()
                    # print("검색 : " + store_name)
                    if store_name == target_name:
                        print(f"✅ 가게명 일치: {store_name}")

                        # 리뷰 내용
                        content = block.find_element(By.CLASS_NAME, 'RfnDt').text

                        # 작성 시간
                        time_text = block.find_element(By.CLASS_NAME, 'kvMYJc').text

                        # 별점
                        rating_div = block.find_element(By.CSS_SELECTOR, 'span[aria-label]')
                        rating = rating_div.get_attribute('aria-label')

                        # 사진 개수
                        # image_count = block.find_element(By.CLASS_NAME, 'KtCyie')
                        has_photo = 1 if block.find_elements(By.CLASS_NAME, "KtCyie") else 0


                        # 작성자 총리뷰수
                        try:
                            container = driver.find_element(By.CLASS_NAME, 'TiFmlb')
                            qha3nb_text = container.find_element(By.CLASS_NAME, 'Qha3nb').text.strip()

                            # 정규식으로 "리뷰 158개" 중 숫자만 추출
                            import re
                            match = re.search(r'리뷰\s+(\d+)', qha3nb_text)
                            review_count = int(match.group(1)) if match else 0

                            print(f"📊 리뷰 수: {review_count}")
                        except Exception as e:
                            review_count = 0
                            print(f"❌ 리뷰 수 추출 실패: {e}")

                        # time.sleep(100)



                        # print(f"내용: {content}")
                        # print(f"작성 시간: {time_text}")
                        # print(f"별점: {rating}")
                        print(f"사진 유무 : {has_photo}")
                        print("----------------------------")

                        try:
                            driver.execute_script("arguments[0].click();", block)
                            print("🖱️ 리뷰 블록 클릭 성공 (JS 방식)")
                        except:
                            try:
                                actions = ActionChains(driver)
                                actions.move_to_element(block).click().perform()
                                print("🖱️ 리뷰 블록 클릭 성공 (ActionChains 방식)")
                            except Exception as click_error:
                                print(f"❌ 리뷰 블록 클릭 실패: {click_error}")
                        time.sleep(2)

                        # ✅ 전환된 화면에서 jsaction="pane.placeNameHeader.open" 클릭 시도
                        try:
                            header_div = driver.find_element(By.XPATH, '//div[@jsaction="pane.placeNameHeader.open"]')
                            driver.execute_script("arguments[0].click();", header_div)
                            print("🖱️ 장소명 헤더 클릭 성공 (pane.placeNameHeader.open)")
                        except Exception as e:
                            print(f"❌ 장소명 헤더 클릭 실패: {e}")
                        time.sleep(2)

                        # try:
                        #     # 총별점 가져오기 (aria-hidden="true" span)
                        #     total_rating_div = driver.find_element(By.XPATH, '//span[@aria-hidden="true"]')
                        #     total_rating = total_rating_div.text.strip()
                        #     print(f"🌟 총별점: {total_rating}")
                        # except Exception as e:
                        #     print(f"❌ 총별점 가져오기 실패: {e}")
                        # time.sleep(3)
                        try:
                            total_rating_span = driver.find_element(By.XPATH, '//span[@role="img" and contains(@class, "ceNzKf")]')
                            total_rating = total_rating_span.get_attribute('aria-label').strip()
                            #별표, 개 단어 지우기
                            total_rating_cleaned = total_rating.replace('별표', '').replace('개', '').strip()
                            print(f"🌟 총별점: {total_rating_cleaned}")
                        except Exception as e:
                            print(f"❌ 총별점 가져오기 실패: {e}")
                        time.sleep(2)

                        try:
                            # 업종명 가져오기 (class="DkEaL"인 button 태그)
                            category_button = driver.find_element(By.XPATH, '//button[contains(@class, "DkEaL")]')
                            category = category_button.text.strip()
                            print(f"🏷️ 업종명: {category}")
                        except Exception as e:
                            category = "없음"
                            print(f"❌ 업종명 가져오기 실패: {e}")

                        time.sleep(3)
                        # ✅ 추출된 정보를 DataFrame에 반영
                        df.at[idx, '사진유무'] = has_photo
                        df.at[idx, '총평점'] = float(total_rating_cleaned)
                        df.at[idx, '업종'] = category
                        df.at[idx, '사용자총리뷰수'] = review_count
                        # ✅ 각 행 처리 후 즉시 저장
                        df.to_csv(file_path, index=False, encoding='utf-8-sig')
                        print(f"💾 [행 {idx}] 저장 완료")

                        found = True
                        break
                except:
                    continue

        if not found:
            try:
                # 마지막 리뷰 요소 기준으로 스크롤
                if review_blocks:
                    scroll_origin = ScrollOrigin.from_element(review_blocks[-1])
                    actions = ActionChains(driver)
                    actions.scroll_from_origin(scroll_origin, 0, scroll_amount).perform()
                    scroll_amount += 100000  # 스크롤 양 점진 증가
                    scroll_try += 1
                    # print(f"[{idx+1}] 스크롤 시도 {scroll_try}회, 스크롤 양: {scroll_amount}px")
                    time.sleep(2)
                else:
                    print("❌ 스크롤 기준 리뷰 요소 없음")
                    break
            except Exception as e:
                print(f"❌ 스크롤 중 에러 발생: {e}")
                break

    if not found:
        print(f"❌ {target_name} 관련 리뷰를 찾지 못했습니다.")

driver.quit()








### 컬럼 추가와 변경된 내요
# # 새 컬럼 추가
# df['업종'] = '카페'               # 모든 가게를 카페로 설정 (필요 시 변경 가능)
# df['총평점'] = df['별점']        # 총평점 = 별점
# df['사진유무'] = '없음'          # 기본값 '없음' (나중에 조건으로 '있음'도 가능)

# # 컬럼 순서 변경
# df = df[['가게명', '업종', '주소', '총평점', '작성자', '리뷰내용', '사진유무', '별점', '작성시간', '리뷰 페이지']]

# # 변경된 내용 저장 (선택)
# df.to_csv('busan_reviews_reordered.csv', index=False, encoding='utf-8-sig')

# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
# import time
# import re
# # 셀레니움 드라이버 설정
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--start-maximized')
# driver = webdriver.Chrome(service=Service(), options=options)

# # CSV 파일 경로
# file_path = '/Users/jeongjaeyoon/Documents/GitHub/personalized-tour-ai/google_maps_review.csv'
# df = pd.read_csv(file_path, encoding='utf-8-sig')

# # 리뷰 페이지 순회 
# # for idx, row in df.iterrows():
# # for idx, row in df[df['사용자총리뷰수'].isna()].iterrows():
# for idx in range(6400, len(df)):
#     row = df.iloc[idx] # 추가
        
#     if pd.notna(row['사용자총리뷰수']): # 만약 사용자총리뷰수가 비어있지 않으면 패스 == 추가
#         continue

#     target_name = row['가게명']
#     review_url = row['리뷰 페이지']

#     print(f"\n[{idx + 1}] 접속 중: {review_url}")
#     driver.get(review_url)
#     time.sleep(3)

#     found = False
#     scroll_try = 0
#     scroll_amount = 30000  # 초기 스크롤 양

#     while not found and scroll_try < 500:  # 최대 20회 시도
#         review_blocks = driver.find_elements(By.CLASS_NAME, 'jftiEf')
#         current_count = len(review_blocks)

#         if not review_blocks:
#             print(f"[{idx+1}] 리뷰 블럭이 비어있음 → 스크롤 시도 {scroll_try+1}회")
#         else:
#             for block in review_blocks:
#                 try:
#                     store_name = block.find_element(By.CSS_SELECTOR, 'div.d4r55.YJxk2d').text.strip()
#                     # print("검색 : " + store_name)
#                     if store_name == target_name:
#                         print(f"✅ 가게명 일치: {store_name}")

#                         # 리뷰 내용
#                         content = block.find_element(By.CLASS_NAME, 'RfnDt').text

#                         # 작성 시간
#                         time_text = block.find_element(By.CLASS_NAME, 'kvMYJc').text

#                         # 별점
#                         rating_div = block.find_element(By.CSS_SELECTOR, 'span[aria-label]')
#                         rating = rating_div.get_attribute('aria-label')

#                         # 사진 개수
#                         # image_count = block.find_element(By.CLASS_NAME, 'KtCyie')
#                         has_photo = 1 if block.find_elements(By.CLASS_NAME, "KtCyie") else 0


#                         # 작성자 총리뷰수
#                         try:
#                             container = driver.find_element(By.CLASS_NAME, 'TiFmlb')
#                             qha3nb_text = container.find_element(By.CLASS_NAME, 'Qha3nb').text.strip()

#                             # 정규식으로 "리뷰 158개" 중 숫자만 추출
#                             import re
#                             match = re.search(r'리뷰\s+(\d+)', qha3nb_text)
#                             review_count = int(match.group(1)) if match else 0

#                             print(f"📊 리뷰 수: {review_count}")
#                         except Exception as e:
#                             review_count = 0
#                             print(f"❌ 리뷰 수 추출 실패: {e}")

#                         # time.sleep(100)



#                         # print(f"내용: {content}")
#                         # print(f"작성 시간: {time_text}")
#                         # print(f"별점: {rating}")
#                         print(f"사진 유무 : {has_photo}")
#                         print("----------------------------")

#                         try:
#                             driver.execute_script("arguments[0].click();", block)
#                             print("🖱️ 리뷰 블록 클릭 성공 (JS 방식)")
#                         except:
#                             try:
#                                 actions = ActionChains(driver)
#                                 actions.move_to_element(block).click().perform()
#                                 print("🖱️ 리뷰 블록 클릭 성공 (ActionChains 방식)")
#                             except Exception as click_error:
#                                 print(f"❌ 리뷰 블록 클릭 실패: {click_error}")
#                         time.sleep(2)

#                         # ✅ 전환된 화면에서 jsaction="pane.placeNameHeader.open" 클릭 시도
#                         try:
#                             header_div = driver.find_element(By.XPATH, '//div[@jsaction="pane.placeNameHeader.open"]')
#                             driver.execute_script("arguments[0].click();", header_div)
#                             print("🖱️ 장소명 헤더 클릭 성공 (pane.placeNameHeader.open)")
#                         except Exception as e:
#                             print(f"❌ 장소명 헤더 클릭 실패: {e}")
#                         time.sleep(2)

#                         # try:
#                         #     # 총별점 가져오기 (aria-hidden="true" span)
#                         #     total_rating_div = driver.find_element(By.XPATH, '//span[@aria-hidden="true"]')
#                         #     total_rating = total_rating_div.text.strip()
#                         #     print(f"🌟 총별점: {total_rating}")
#                         # except Exception as e:
#                         #     print(f"❌ 총별점 가져오기 실패: {e}")
#                         # time.sleep(3)
#                         try:
#                             total_rating_span = driver.find_element(By.XPATH, '//span[@role="img" and contains(@class, "ceNzKf")]')
#                             total_rating = total_rating_span.get_attribute('aria-label').strip()
#                             #별표, 개 단어 지우기
#                             total_rating_cleaned = total_rating.replace('별표', '').replace('개', '').strip()
#                             print(f"🌟 총별점: {total_rating_cleaned}")
#                         except Exception as e:
#                             print(f"❌ 총별점 가져오기 실패: {e}")
#                         time.sleep(2)

#                         try:
#                             # 업종명 가져오기 (class="DkEaL"인 button 태그)
#                             category_button = driver.find_element(By.XPATH, '//button[contains(@class, "DkEaL")]')
#                             category = category_button.text.strip()
#                             print(f"🏷️ 업종명: {category}")
#                         except Exception as e:
#                             category = "없음"
#                             print(f"❌ 업종명 가져오기 실패: {e}")

#                         time.sleep(3)
#                         # ✅ 추출된 정보를 DataFrame에 반영
#                         df.at[idx, '사진유무'] = has_photo
#                         df.at[idx, '총평점'] = float(total_rating_cleaned)
#                         df.at[idx, '업종'] = category
#                         df.at[idx, '사용자총리뷰수'] = review_count
#                         # ✅ 각 행 처리 후 즉시 저장
#                         df.to_csv(file_path, index=False, encoding='utf-8-sig')
#                         print(f"💾 [행 {idx}] 저장 완료")

#                         found = True
#                         break
#                 except:
#                     continue

#         if not found:
#             try:
#                 # 마지막 리뷰 요소 기준으로 스크롤
#                 if review_blocks:
#                     scroll_origin = ScrollOrigin.from_element(review_blocks[-1])
#                     actions = ActionChains(driver)
#                     actions.scroll_from_origin(scroll_origin, 0, scroll_amount).perform()
#                     scroll_amount += 100000  # 스크롤 양 점진 증가
#                     scroll_try += 1
#                     # print(f"[{idx+1}] 스크롤 시도 {scroll_try}회, 스크롤 양: {scroll_amount}px")
#                     time.sleep(2)
#                 else:
#                     print("❌ 스크롤 기준 리뷰 요소 없음")
#                     break
#             except Exception as e:
#                 print(f"❌ 스크롤 중 에러 발생: {e}")
#                 break

#     if not found:
#         print(f"❌ {target_name} 관련 리뷰를 찾지 못했습니다.")

# driver.quit()








# ### 컬럼 추가와 변경된 내요
# # # 새 컬럼 추가
# # df['업종'] = '카페'               # 모든 가게를 카페로 설정 (필요 시 변경 가능)
# # df['총평점'] = df['별점']        # 총평점 = 별점
# # df['사진유무'] = '없음'          # 기본값 '없음' (나중에 조건으로 '있음'도 가능)

# # # 컬럼 순서 변경
# # df = df[['가게명', '업종', '주소', '총평점', '작성자', '리뷰내용', '사진유무', '별점', '작성시간', '리뷰 페이지']]

# # # 변경된 내용 저장 (선택)
# # df.to_csv('busan_reviews_reordered.csv', index=False, encoding='utf-8-sig')