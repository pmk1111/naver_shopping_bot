from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# find_element(s)로 요소를 찾지 못했을 때 발생하는 예외
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# 시간과 관련된 다양한 기능을 제공하는 모듈. 시간을 측정하고 제어하는 데 사용
import time
# 임의의 난수 발생을 위해 사용하는 random 모듈
import random
# pandas 모듈 추가
import pandas as pd

options = ChromeOptions()
# 작업이 완료되어도 브라우저 유지
options.add_experimental_option("detach", True)
# 백그라운드에서도 작업 실행
options.add_argument("headless")
options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# 브라우저를 Full Screen으로 연다.
# driver.maximize_window()

# 상품명을 입력받으면 네이버 쇼핑 이동. 공백 또는 아무 값도 입력받지 않았느면 올바른 값을 입력받을 때 까지 반복
while True:
    item_name = input("상품명을 입력하세요> ")

    if item_name and item_name.strip() != '' :
        break

limit_arr = ["20", "40", "60", "80"]
while True:
    limit_per_page = input("페이지 당 상품 갯수> ")
    
    try:
        if limit_per_page in limit_arr or limit_per_page == '':
            driver.get("https://shopping.naver.com/home")
            break
        else:
            print("유효하지 않은 값입니다. 다시 입력하세요.")
    except ValueError:
        print("숫자를 입력하세요.")

# 3~5 사이의 난수 생성
random_sec = random.uniform(2, 4)
driver.implicitly_wait(10)

# 네이버 쇼핑은 브라우저 크기 별로 검색 영역을 나타내는 태그가 다른 방식으로 표시된다.
# 셀레니움으로 브라우저를 열었을 때의 브라우저 넓이를 구한 다음, 그 값에 따라 다른 방식으로 검색 영역을 찾아준다.
# 예제에서는 이미 셀레니움으로 브라우저 오픈 시Full Screen으로 열리도록 설정했지만, 
# 이런 방법으로 웹 브라우저 크기 별로 컨트롤 할 수 있다는 걸 알려주기 위해 작성
window_rect = driver.get_window_rect()
width = window_rect['width']
if width >= 1152:
    try:
        search_input = driver.find_element(By.CSS_SELECTOR, "._searchInput_search_text_3CUDs")
        if search_input:
            search_input.send_keys(item_name)
        time.sleep(2)
        search_input.send_keys(Keys.ENTER)
    except Exception as e:
        print("검색 영역을 찾지 못했습니다.(Full Size Browser)", e)
else: # 브라우저 넓이가 1152px 미만일 경우
    try:
        search_input = driver.find_element(By.CSS_SELECTOR, "._combineHeader_expansion_search_inner_1VxB3")
        search_input.click()
        driver.implicitly_wait(10)
        search_input = driver.find_element(By.CSS_SELECTOR, "#input_text")
        search_input.send_keys(item_name)
        search_input.send_keys(Keys.ENTER)
    except Exception as e:
        print("검색 영역을 찾지 못했습니다.(span tag)", e)

time.sleep(random_sec)

# 네이버 쇼핑은 초기 실행 시 브라우저 넓이에 따라 검색 결과 ui가 결정된다
# 넓이가 1152px 미만으로 한 다음 상품을 검색하면, 이후 브라우저 넓이를 늘려도 특정 태그가 표시되지 않으므로 
# 처음부터 1152px 이상으로 브라우저 크기를 세팅한 다음 실행하는 것이 좋다.
try:
    limit = driver.find_elements(By.CSS_SELECTOR, 'div.subFilter_select_box__dX_vV')[1]
    if limit:
        limit.click()
        driver.implicitly_wait(10)
        try:
            limit_cnt = driver.find_elements(By.CSS_SELECTOR, "div.subFilter_select_box__dX_vV.open ul li")
            time.sleep(random_sec)

            if limit_per_page == "20":
                limit_cnt[0].click()
            elif limit_per_page == "40" or limit_per_page.strip() == '':
                limit_cnt[1].click()
            elif limit_per_page == "60":
                limit_cnt[2].click()
            else:
                limit_cnt[3].click()
        except Exception as e:
            print("페이지 당 상품 갯수 리스트를 찾지 못했습니다.", e)
except Exception as e:
    print("페이지 당 상품 갯수 div를 찾지 못했습니다.")

last_height = driver.execute_script("return document.body.scrollHeight")

time.sleep(2)

# 상품 정보를 항목별로 담을 리스트
product_title_list = []
product_url_list = []
product_price_list = []
product_category_list = []

# 각 리스트에 값을 저장하는 함수
def add_list(product_title, product_url, product_price, product_category):
    product_title_list.append(product_title)
    product_url_list.append(product_url)
    product_price_list.append(product_price)
    product_category_list.append(product_category)

# 스크롤 완료 후 => 현재 페이지의 상품 정보를 가져온 후 => 다음 페이지로 이동
# 마지막 페이지인 경우 루프 중지
while True:
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            print("스크롤 완료")
            break
        last_height = new_height

    # 현재 페이지 상품 목록들
    items = driver.find_elements(By.CSS_SELECTOR, ".basicList_list_basis__uNBZx > div > div")
    print("가져온 상품 수: ", len(items))
    time.sleep(2)

    # 상품 정보 항목 추출
    for item in items:
        try:
            product_info_grp = item.find_element(By.CSS_SELECTOR, ".product_info_area__xxCTi")

            product_title = product_info_grp.find_element(By.CSS_SELECTOR, "a").text
            product_url = product_info_grp.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            product_price = product_info_grp.find_element(By.CSS_SELECTOR, ".price_num__S2p_v em").text
            product_category_grp = product_info_grp.find_elements(By.CSS_SELECTOR, ".product_depth__I4SqY span")

            product_category = ""
            for c in product_category_grp:
                product_category += c.text
            add_list(product_title, product_url, product_price, product_category)
        except NoSuchElementException as e:
            try:
                product_info_grp = item.find_element(By.CSS_SELECTOR, ".adProduct_info_area__dTSZf")

                product_title = product_info_grp.find_element(By.CSS_SELECTOR, "a").text
                product_url = product_info_grp.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                product_price = product_info_grp.find_element(By.CSS_SELECTOR, ".price_num__S2p_v em").text
                product_category_grp = product_info_grp.find_elements(By.CSS_SELECTOR, ".adProduct_depth__s_IUT span")

                product_category = ""
                for c in product_category_grp:
                    product_category += c.text
                add_list(product_title, product_url, product_price, product_category)
            except NoSuchElementException as e:
                print("상품 정보 영역을 찾는 데 문제가 발생했습니다.")


    try:
        next_page = driver.find_element(By.CSS_SELECTOR, ".pagination_next__pZuC6")
        next_page.click()
    except NoSuchElementException as e:
        print("마지막 페이지 입니다.")
        break  


# dataframe으로 변환
data = {"상품명": product_title_list, "판매주소": product_url_list, 
        "가격": product_price_list, "상품분류": product_category_list}
df = pd.DataFrame(data)

df.to_csv("product_info.csv", encoding = "utf-8-sig")