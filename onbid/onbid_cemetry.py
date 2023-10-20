# coding=utf-8
import time
import random
import math
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
    options.add_argument('--no-sandbox') #Linux계열에서 GUI라이브러리 미존재 등으로 크롬드라이버 정상 구동 안될 때  사용
    options.add_argument('--disable-dev-shm-usage') #Linux계열에서 크롬드라이버 정상 구동 안될 때  사용
    #크롤링 대상 서버가 봇이 아닌 정상적인 접근으로 인지되도록 하기 위해 user-agent 조작
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41')
    
    browser= webdriver.Chrome('./chromedriver',options=options)
    browser.maximize_window() # 브라우저 창 최대화 
    browser.get('https://www.onbid.co.kr/op/cta/cltrdtl/collateralDetailRealEstateList.do') #최초 진입 페이지

    #검색 조건 설정
    매각버튼 = browser.find_element(By.CSS_SELECTOR, '#dpslMtd2').click()
    검색시작일 = browser.find_element(By.CSS_SELECTOR, '#searchBegnDtm')
    검색시작일.clear()
    검색시작일.send_keys('2023-10-23')
    검색종료일 = browser.find_element(By.CSS_SELECTOR, '#searchClsDtm')
    검색종료일.clear()
    검색종료일.send_keys('2023-10-27')

    try:
        Select(WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#searchFromMinBidPrc')))).select_by_value('20000000')
        Select(WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#searchToMinBidPrc')))).select_by_value('100000000')
    except TimeoutException as te: # 실패 시에는 에러메시지로 Time Out 출력
        print(te)
    finally:
        pass

    browser.find_element(By.CSS_SELECTOR, '#firstCtgrId2').click() #용도
    #browser.find_element(By.CSS_SELECTOR, '#secondCtgrId_10100').click() #전체선택
    browser.find_element(By.CSS_SELECTOR, '#secondCtgrId_10101').click() #대지
    browser.find_element(By.CSS_SELECTOR, '#secondCtgrId_10102').click() #임야
    browser.find_element(By.CSS_SELECTOR, '#secondCtgrId_10103').click() #전
    browser.find_element(By.CSS_SELECTOR, '#secondCtgrId_10104').click() #답
    browser.find_element(By.CSS_SELECTOR, '#secondCtgrId_10105').click() #과수원
    browser.find_element(By.CSS_SELECTOR, '#secondCtgrId_10106').click() #잡종지
    browser.find_element(By.CSS_SELECTOR, '#searchShrYn2').click() #지분
    browser.find_element(By.CSS_SELECTOR, '#searchBtn > span').click() #검색버튼

    browser.implicitly_wait(60) # seconds

    return browser

def closeBrowser(browser):
    browser.quit()

async def bot(): #실행시킬 함수명 임의지정
    bot = telegram.Bot(token = '6152505971:AAFgtAFyaA4Z53TEA0rsuoj9is7Ml4suKpQ')
    await bot.send_message('-1001935205192',
        '*** 온비드 지분분묘 물건번호 ***\n'
        '처분방식: 매각\n'
        '입찰기간: 2023-05-15 ~ 2023-06-12\n'
        '최저입찰가: 2천만원 ~ 1억원\n'
        '용도선택: 토지\n'
        '상세용도: 대지, 임야, 전, 답, 과수원, 잡종지\n'
        '소재지: 전국\n'
        '토지면적: 전체\n'
        # '건물면적: 0~10,000m2\n'
        '지분여부: 지분\n'
        '자산구분: 전체\n'
        '추가검색조건: 유의사항에 분묘 안내 포함하고, 10명 이내 공유자 중 동일 성씨가 70% 이상인 경우(예, 5명중 4명이 동일 성씨)만 추출'
    )
    await bot.send_message('-1001935205192',지분분묘물건번호)

print(time.strftime('%Y.%m.%d - %H:%M:%S')) # 년.월.일 - 시간

browser = openBrowser()

지분분묘물건번호 = []
총건수 = browser.find_element(By.CSS_SELECTOR, '#collateralSearchForm > div.cm_paging.cl > p').text[3:-3]
전체페이지 = math.ceil(int(총건수) / 10)
현재페이지 = 1
페이지인덱스 = 1

while True:
    # tbody = browser.find_element(By.CSS_SELECTOR, '#collateralSearchForm > table > tbody')
    매각물건rows = browser.find_elements(By.CSS_SELECTOR, '#collateralSearchForm > table > tbody > tr')
    for i in range(1, len(매각물건rows)+1):
    # for i in range(1, 11):
        # for k in range(1, 6):#검색결과리스트
        #     col= tbody.find_element(By.CSS_SELECTOR, '#collateralSearchForm > table > tbody > tr:nth-child('+str(i)+') > td:nth-child('+str(k)+')')
        #     print(col.text)
        # time.sleep( random.uniform(3,10) ) # 랜덤한 시간으로  쉬어줘
        try:
            물건관리번호링크 = browser.find_element(By.CSS_SELECTOR, '#collateralSearchForm > table > tbody > tr:nth-child('+str(i)+') > td.al.pos_rel > div > dl > dt > a').click()
            browser.implicitly_wait(30) # seconds
        except WebDriverException as we: # 실패 시에는 에러메시지로 Time Out 출력
            print(we)
            # if browser is not None : 
            #     print('browser is not None')
            #     browser.quit()
            #     time.sleep(3)
            # browser = openBrowser()
            # browser.implicitly_wait(30) # seconds
        finally:
            # browser.quit()
            pass
        
        압류재산정보 = browser.find_elements(By.CSS_SELECTOR, '#dtbuttontab')[1]
        browser.execute_script("arguments[0].click();", 압류재산정보)
        browser.implicitly_wait(30) # seconds

        유의사항 = browser.find_element(By.CSS_SELECTOR, '#pytnMtrs')
        
        if '분묘' in 유의사항.text:
            물건관리번호 = browser.find_element(By.CSS_SELECTOR, '#Contents > div.tab_wrap1.pos_rel > div.finder03 > div > div.txt_top > p.fl.fwb > span:nth-child(2)')            
            
            등기사항총건수 = browser.find_element(By.CSS_SELECTOR, '#paging2 > p').text[3:-2]
            등기사항전체페이지 = math.ceil(int(등기사항총건수) / 10)
            등기사항현재페이지 = 1
            등기사항페이지인덱스 = 2
            공유자 = []
            개수 = []
            # print('물건관리번호'+물건관리번호.text)
            # print('등기사항총건수'+str(등기사항총건수))
            # print('등기사항전체페이지'+str(등기사항전체페이지))
            # print('등기사항현재페이지'+str(등기사항현재페이지))
            # print('등기사항페이지인덱스'+str(등기사항페이지인덱스))
            while True:
                등기사항rows = browser.find_elements(By.CSS_SELECTOR, '#resultRgstImfoList > tr')
                # print('등기사항rows'+str(len(등기사항rows)))
                for j in range(1, len(등기사항rows)+1):
                    # print('J : '+str(j))
                    권리종류 = browser.find_element(By.CSS_SELECTOR, '#resultRgstImfoList > tr:nth-child('+str(j)+') > td:nth-child(2)').get_attribute("innerText")
                    if 권리종류 in '공유자':
                        권리자 = browser.find_element(By.CSS_SELECTOR, '#resultRgstImfoList > tr:nth-child('+str(j)+') > td:nth-child(3)').get_attribute("innerText")
                        공유자.append(권리자)
                        개수.append(1)

                if 등기사항전체페이지 == 등기사항현재페이지:
                    break
                \
                elif (len(공유자) > 10):
                    break
                else:
                    등기사항현재페이지 = 등기사항현재페이지+1
                    등기사항페이지인덱스 = 등기사항페이지인덱스+1
                    등기사항페이지 = browser.find_element(By.CSS_SELECTOR, '#paging2 > a:nth-child('+str(등기사항페이지인덱스)+')')
                    browser.execute_script("arguments[0].click();", 등기사항페이지)
                    browser.implicitly_wait(20) # seconds
                    # WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#resultRgstImfoList > tr:nth-child(1) > td:nth-child(2)')))

            if (len(공유자) > 0):
                df = pd.DataFrame({'공유자':공유자, '개수':개수})
                # print(df)
                # print(df.groupby('공유자').size())
                # print(df.groupby('공유자').sum())
                
                s = df.groupby('공유자').sum()
                tot = s.sum()
                top = s.iloc[0]
                # print(tot)
                # print(top)

                ret = (top/tot) 
                # print(ret)

                if ret.iloc[0] > 0.7:
                    # print('공유자매수진입')
                    print('분묘 : '+물건관리번호.text)
                    지분분묘물건번호.append(물건관리번호.text)
                # else:
                #     print('공유자매수포기')
        # else:
            # print('no 분묘')
        
        목록 = browser.find_element(By.CSS_SELECTOR, '#Contents > div.btn_C.mt20 > a')
        browser.execute_script("arguments[0].click();", 목록)
        browser.implicitly_wait(30) # seconds
        # time.sleep( random.uniform(3,10) ) # 랜덤한 시간으로  쉬어줘

    print('전체페이지'+str(전체페이지))
    print('현재페이지'+str(현재페이지))
    if 전체페이지 == 현재페이지:
        break
    else:        
        # 페이지인덱스값 = browser.find_element(By.CSS_SELECTOR, '#pageIndex').get_attribute("value")
        # 페이지인덱스 = (int(페이지인덱스값)+3) % 10
        # 페이지번호 = browser.find_element(By.CSS_SELECTOR, '#collateralSearchForm > div.cm_paging.cl > a:nth-child('+str(페이지인덱스)+')')
        # browser.execute_script("arguments[0].click();", 페이지번호)
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