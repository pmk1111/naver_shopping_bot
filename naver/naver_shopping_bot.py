from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# 시간과 관련된 다양한 기능을 제공하는 모듈. 시간을 측정하고 제어하는 데 사용
import time
# 임의의 난수 발생을 위해 사용하는 random 모듈
import random

options = ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# 상품명을 입력받으면 네이버 쇼핑 이동. 공백 또는 아무 값도 입력받지 않았느면 올바른 값을 입력받을 때 까지 반복
while True:
    item_name = input("상품명을 입력하세요> ")
    
    if item_name and item_name.strip() != '' :
        driver.get("https://shopping.naver.com/home")
        break

# 3~5 사이의 난수 생성
random_sec = random.uniform(2, 4)
time.sleep(random_sec)

# 네이버 쇼핑은 브라우저 크기 별로 검색 영역을 나타내는 태그가 다른 방식으로 표시된다.
# 셀레니움으로 브라우저를 열었을 때의 브라우저 넓이를 구한 다음, 그 값에 따라 다른 방식으로 검색 영역을 찾아준다.
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
else:
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