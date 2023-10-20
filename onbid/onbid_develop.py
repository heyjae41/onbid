# coding=utf-8
import time
import random
import math
import re 
import pandas as pd
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
import telegram
import asyncio

def openBrowser():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41')
    
    browser= webdriver.Chrome('./chromedriver',options=options)
    browser.maximize_window() # 창 최대화 
    browser.get('https://www.onbid.co.kr/op/cta/cltrdtl/collateralDetailRealEstateList.do')

    매각버튼 = browser.find_element(By.CSS_SELECTOR, '#dpslMtd2').click()
    검색시작일 = browser.find_element(By.CSS_SELECTOR, '#searchBegnDtm')
    검색시작일.clear()
    검색시작일.send_keys('2023-05-15')
    검색종료일 = browser.find_element(By.CSS_SELECTOR, '#searchClsDtm')
    검색종료일.clear()
    검색종료일.send_keys('2023-06-12')

    # try:
    #     Select(WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#searchToMinBidPrc')))).select_by_value('100000000')
    # except TimeoutException as te: # 실패 시에는 에러메시지로 Time Out 출력
    #     print(te)
    # finally:
    #     pass

    browser.find_element(By.CSS_SELECTOR, '#firstCtgrId33').click() #주거용건물
    #browser.find_element(By.CSS_SELECTOR, '##secondCtgrId_10200').click() #전체선택
    browser.find_element(By.CSS_SELECTOR, '#secondCtgrId_10201').click() #아파트
    browser.find_element(By.CSS_SELECTOR, '#secondCtgrId_10202').click() #주상복합
    browser.find_element(By.CSS_SELECTOR, '#secondCtgrId_10203').click() #빌라
    browser.find_element(By.CSS_SELECTOR, '#secondCtgrId_10204').click() #단독주택
    browser.find_element(By.CSS_SELECTOR, '#secondCtgrId_10205').click() #다가구주택
    browser.find_element(By.CSS_SELECTOR, '#secondCtgrId_10206').click() #다세대주택
    browser.find_element(By.CSS_SELECTOR, '#secondCtgrId_10207').click() #다중주택
    browser.find_element(By.CSS_SELECTOR, '#secondCtgrId_10208').click() #도시형생활주택
    browser.find_element(By.CSS_SELECTOR, '#secondCtgrId_10209').click() #연립주택

    # browser.find_element(By.CSS_SELECTOR, '#searchFromLandSqms').send_keys('10,000'); #토지면적From
    # browser.find_element(By.CSS_SELECTOR, '#searchToLandSqms').send_keys('999,999,999') #토지면적To
    # try:
    #     Select(WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#searchFromUsbdCnt')))).select_by_value('2') #유찰횟수From
    # except TimeoutException as te: # 실패 시에는 에러메시지로 Time Out 출력
    #     print(te)
    # finally:
    #     pass
    # browser.find_element(By.CSS_SELECTOR, '#searchToUsbdCnt').click() #유찰횟수To    
    # browser.find_element(By.CSS_SELECTOR, '#searchShrYn2').click() #지분
    browser.find_element(By.CSS_SELECTOR, '#searchShrYn3').click() #지분제외
    browser.find_element(By.CSS_SELECTOR, '#businessTypeAll').click() #자산구분전체
    browser.find_element(By.CSS_SELECTOR, '#searchBtn > span').click() #검색버튼

    browser.implicitly_wait(60) # seconds

    return browser

def closeBrowser(browser):
    browser.quit()

async def bot(): #실행시킬 함수명 임의지정
    bot = telegram.Bot(token = '6152505971:AAFgtAFyaA4Z53TEA0rsuoj9is7Ml4suKpQ')
    await bot.send_message('-1001935205192',
        '*** 온비드 재개발/재건축 물건번호 ***\n'
        '처분방식: 매각\n'
        '입찰기간: 2023-05-15 ~ 2023-06-12\n'
        #'최저입찰가: 0~1억\n'
        '용도선택: 주거용건물\n'
        '상세용도: 아파트,주상복합,빌라,단독주택,다가구주택,다세대주택,다중주택,도시형생활주택,연립주택\n'
        #'소재지: 서울, 경기, 부산, 인천, 광주, 세종\n'
        '소재지: 전국\n'
        # '토지면적: 10,000㎡ 이상\n'
        # '건물면적: 0~10,000㎡\n'
        '지분여부: 지분 제외\n'
        '자산구분: 전체\n'
        '추가검색조건: 정비계획,안전진단,정비사업,정비구역,재건축,재개발,조합,관리처분계획,사업시행 문자열 추출'
    )
    if len(재개발물건번호) > 0:
        await bot.send_message('-1001935205192','대상 없음')
    else:
        await bot.send_message('-1001935205192',재개발물건번호)

print(time.strftime('%Y.%m.%d - %H:%M:%S')) # 년.월.일 - 시간

browser = openBrowser()

재개발물건번호 = []
총건수 = browser.find_element(By.CSS_SELECTOR, '#collateralSearchForm > div.cm_paging.cl > p').text[3:-3]
전체페이지 = math.ceil(int(총건수) / 10)
현재페이지 = 1
페이지인덱스 = 1

재개발문자열 = ['정비계획','안전진단','정비사업','정비구역','재건축','재개발','조합','관리처분계획','사업시행']
while True:
    매각물건rows = browser.find_elements(By.CSS_SELECTOR, '#collateralSearchForm > table > tbody > tr')
    for i in range(1, len(매각물건rows)+1):
        try:
            #물건 상세정보 클릭
            물건관리번호링크 = browser.find_element(By.CSS_SELECTOR, '#collateralSearchForm > table > tbody > tr:nth-child('+str(i)+') > td.al.pos_rel > div > dl > dt > a').click()
            browser.implicitly_wait(30) # seconds
        except WebDriverException as we: # 실패 시에는 에러메시지로 Time Out 출력
            print(we)
        finally:
            # browser.quit()
            pass
        
        # 물건관리번호 = browser.find_element(By.CSS_SELECTOR, '#Contents > div.tab_wrap1.pos_rel > div.finder03 > div > div.txt_top > p.fl.fwb > span:nth-child(2)').get_attribute("innerText") #이상하게인식못함
        물건관리번호 = browser.find_element(By.XPATH, '//*[@id="Contents"]/div[3]/div[2]/div/div[1]/p[1]/span[2]').get_attribute("innerText")
        
        부근현황 = browser.find_element(By.CSS_SELECTOR, '#posiEnvPscd > p').get_attribute("innerText") #위치 및 부근현황
        이용현황 = browser.find_element(By.CSS_SELECTOR, '#utlzPscd > p').get_attribute("innerText") #이용현황

        py_list = [부근현황,이용현황]
        q = 재개발문자열
        r = [s for s in py_list if any(xs in s for xs in q)]

        if len(r) > 0:
            print(r)
            재개발물건번호.append(물건관리번호)

        목록 = browser.find_element(By.CSS_SELECTOR, '#Contents > div.btn_C.mt20 > a')
        browser.execute_script("arguments[0].click();", 목록)
        browser.implicitly_wait(30) # seconds
        # time.sleep( random.uniform(3,10) ) # 랜덤한 시간으로  쉬어줘

    # print('전체페이지:'+str(전체페이지))
    # print('현재페이지:'+str(현재페이지))
    if 전체페이지 == 현재페이지:
        break
    else:
        if 현재페이지%10 == 0:
            browser.quit()
            time.sleep( random.uniform(5,10) ) # 랜덤한 시간으로  쉬어줘
            browser = openBrowser()
            time.sleep( random.uniform(5,10) ) # 랜덤한 시간으로  쉬어줘

        현재페이지 = 현재페이지+1
        
        browser.execute_script("fn_paging({0})".format(현재페이지))
        browser.implicitly_wait(30) # seconds

asyncio.run(bot()) #봇 실행하는 코드

print(time.strftime('%Y.%m.%d - %H:%M:%S')) # 년.월.일 - 시간