import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# 셀레니움 드라이버 설정
options = Options()
options.add_argument('--start-maximized')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# options.add_argument("--headless=new")
driver = webdriver.Chrome(service=Service(), options=options)

# CSV 파일 경로
file_path = r'C:\Users\NM333-67\Desktop\persoanlized-tour-ai\google_maps_review.csv'
df = pd.read_csv(file_path, encoding='utf-8-sig')

for idx in range(7471, len(df)):
    row = df.iloc[idx]
    if pd.notna(row['사용자총리뷰수']):
        continue

    target_name = row['가게명']
    review_url = row['리뷰 페이지']

    print(f"\n[{idx + 1}] 접속 중: {review_url}")
    driver.get(review_url)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'jftiEf')))
    except:
        print("❌ 리뷰 블록이 로드되지 않음")
        continue

    found = False
    scroll_try = 0
    scroll_amount = 10000
    
    while not found and scroll_try < 40:
        try:
            review_blocks = driver.find_elements(By.CLASS_NAME, 'jftiEf')
        except Exception as e:
            print(f"❌ jftiEf 요소 탐색 중 예외 발생: {e}")
            break
        time.sleep(3)  # 최소 2초 이상 대기 (기존엔 없었음)
        if not review_blocks:
            print(f"[{idx+1}] jftiEf 요소 없음 → 리뷰 없음으로 간주하고 중단")
            break

        for block in review_blocks:
            try:
                store_name = block.find_element(By.CSS_SELECTOR, 'div.d4r55.YJxk2d').text.strip()
                if store_name != target_name:
                    continue

                print(f"✅ 가게명 일치: {store_name}")
                time.sleep(3)  # 최소 2초 이상 대기 (기존엔 없었음)
                content = block.find_element(By.CLASS_NAME, 'RfnDt').text
                time.sleep(3)  # 최소 2초 이상 대기 (기존엔 없었음)
                time_text = block.find_element(By.CLASS_NAME, 'kvMYJc').text
                time.sleep(3)  # 최소 2초 이상 대기 (기존엔 없었음)
                rating_div = block.find_element(By.CSS_SELECTOR, 'span[aria-label]')
                time.sleep(3)  # 최소 2초 이상 대기 (기존엔 없었음
                rating = rating_div.get_attribute('aria-label')
                time.sleep(3)  # 최소 2초 이상 대기 (기존엔 없었음
                has_photo = 1 if block.find_elements(By.CLASS_NAME, "KtCyie") else 0

                try:
                    container = driver.find_element(By.CLASS_NAME, 'TiFmlb')
                    qha3nb_text = container.find_element(By.CLASS_NAME, 'Qha3nb').text.strip()
                    match = re.search(r'리뷰\s+(\d+)', qha3nb_text)
                    review_count = int(match.group(1)) if match else 0
                    print(f"📊 리뷰 수: {review_count}")
                except Exception as e:
                    review_count = 0
                    print(f"❌ 리뷰 수 추출 실패: {e}")

                print(f"사진 유무 : {has_photo}")
                print("----------------------------")

                try:
                    driver.execute_script("arguments[0].click();", block)
                    print("🖱️ 리뷰 블록 클릭 성공")
                except Exception as click_error:
                    print(f"❌ 리뷰 블록 클릭 실패: {click_error}")
                time.sleep(3)  # 최소 2초 이상 대기 (기존엔 없었음
                try:
                    header_div = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@jsaction="pane.placeNameHeader.open"]'))
                    )
                    driver.execute_script("arguments[0].click();", header_div)
                    print("🖱️ 장소명 헤더 클릭 성공")
                except Exception as e:
                    print(f"❌ 장소명 헤더 클릭 실패: {e}")
                time.sleep(3)  # 최소 2초 이상 대기 (기존엔 없었음
                try:
                    total_rating_span = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//span[@role="img" and contains(@class, "ceNzKf")]'))
                    )
                    total_rating = total_rating_span.get_attribute('aria-label').strip()
                    total_rating_cleaned = total_rating.replace('별표', '').replace('개', '').strip()
                    print(f"🌟 총별점: {total_rating_cleaned}")
                except Exception as e:
                    total_rating_cleaned = "0"
                    print(f"❌ 총별점 가져오기 실패: {e}")

                try:
                    category_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "DkEaL")]'))
                    )
                    category = category_button.text.strip()
                    print(f"🏷️ 업종명: {category}")
                except Exception as e:
                    category = "없음"
                    print(f"❌ 업종명 가져오기 실패: {e}")

                # ✅ 데이터 저장
                df.at[idx, '사진유무'] = has_photo
                df.at[idx, '총평점'] = float(total_rating_cleaned)
                df.at[idx, '업종'] = category
                df.at[idx, '사용자총리뷰수'] = review_count
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
                print(f"💾 [행 {idx}] 저장 완료")

                found = True
                break

            except Exception as e:
                print(f"❌ 리뷰 블럭 처리 중 예외 발생: {e}")
                continue
        if not found:
            try:
                time.sleep(2)  # 최소 2초 이상 대기 (기존엔 없었음)
                scroll_origin = ScrollOrigin.from_element(review_blocks[-1])
                actions = ActionChains(driver)
                actions.scroll_from_origin(scroll_origin, 0, scroll_amount).perform()
                scroll_amount += 100000
                scroll_try += 1
            except Exception as e:
                print(f"❌ 스크롤 중 예외 발생: {e}")
                break

    if not found:
        print(f"❌ {target_name} 관련 리뷰를 찾지 못했습니다.")

driver.quit()
