from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.chrome.service import Service
import os, requests
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Chrome WebDriver 설정
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

wait = WebDriverWait(driver, 10)  # 최대 10초 대기

# articleImg 요소가 클릭 가능해질 때까지 대기
# article_img = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.articleImg')))
#article_img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.articleImg')))

# articleImg 요소를 클릭
#article_img.click()

page_num = 1 # 크롤링 시작 페이지
last_page_num = 10 # 마지막 페이지 설정
ordw = 'best' # 정렬 순서(최고로 설정)

styles = ['americancasual', 'casual', 'chic', 'formal', 'girlish', 'romantic', 'street'] # 크롤링 할 스타일 설정

for style in styles:
    while page_num <= last_page_num: # 자동으로 페이지가 이동되게 while문 사용
        url = 'https://www.musinsa.com/mz/streetsnap?style_type={}&ordw={}&p={}'.format(style, ordw, page_num)
        driver.get(url) # url 접속

        img_num = 0
        while img_num < 60: # 60 고정: 무신사 스트릿 스냅 페이지의 이미지 수 60장
            time.sleep(3) # 페이지가 로드될 때까지 기다리기
            element = driver.find_elements(By.CSS_SELECTOR,'.articleImg')[img_num] # 클릭하려는 요소
            driver.execute_script("arguments[0].scrollIntoView();", element) # 요소가 화면에 보이도록 스크롤 조정

            element.click() # 이미지 접속
            
            img_url = driver.find_elements(By.CSS_SELECTOR,'.lbox')[0].get_attribute('href') # url 파싱 
            
            if not os.path.isdir(style): # 기본적으로 스타일 번호를 폴더로 지정, 폴더 없으면 생성
                os.mkdir(style)
                
            try:
                urlretrieve(img_url, '{}/{}-{}.jpg'.format(style, page_num, img_num)) # img_url에서 이미지 다운로드, style 폴더에 'page_num-img_num.jpg' 형태로 저장 
            except : # 오류 시 오류 선언하고 pass
                print('some error!(style: {}, page num: {}, img num: {})'.format(style, page_num, img_num))
                pass
            
            driver.get(url) # 뒤로가기 대신 url 재접속을 사용(오류 최소화)
            img_num += 1
        page_num += 1
    page_num = 1 # 하나의 스타일에 대한 cycle이 다 돌고 재설정
