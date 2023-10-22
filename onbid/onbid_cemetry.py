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

'''
1. 크롬드라이버 로딩
2. 브라우저 옵션 및 초기화
3. 물건 검색 페이지 조건 설정 
    타겟페이지의 html 요소는 css selector를 기준으로 한다. 
    요소의 css selector를 쉽게 가져오기 위해서 크롭 브라우저에서 타겟 페이지를 열고, 
    이어서 개발자 도구를 열어서 해당 항목의 css selector를 추출한다. 
'''
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
    매각버튼 = browser.find_element(By.CSS_SELECTOR, '#dpslMtd2').click() #체크는 클릭이벤트로 처리
    검색시작일 = browser.find_element(By.CSS_SELECTOR, '#searchBegnDtm')
    검색시작일.clear()
    검색시작일.send_keys('2023-10-23') #input type text는 send_keys() 이용하여 사용자가 타이핑하듯이 입력
    검색종료일 = browser.find_element(By.CSS_SELECTOR, '#searchClsDtm')
    검색종료일.clear() 
    검색종료일.send_keys('2023-10-27')

    #select box는 값을 바로 찍을 수 없다. 실제 내가 입력하는 상황이라고 생각하고 최소가격 요소 선택해서 선택 item 나오면 값을 선택한다. 아래 소스 활용
    # 최소 조건 선택박스 선택해서(Expected Condition) 나올 때까지 3초를 기다려서 아이템 항목 선택한다.
    try:
        Select(WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#searchFromMinBidPrc')))).select_by_value('20000000') #2천만원
        Select(WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#searchToMinBidPrc')))).select_by_value('100000000') #1억원
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

    '''
    implicitly_wait(10) vs time.sleep(10)
    전자는 10초가 되기 전에 로딩이 되면 바로 넘어감. 후자는 무조건 10초를 기다림
    그러므로 성능 관점에서 전자를 선택해야 함
    '''    
    browser.implicitly_wait(60) # seconds

    return browser

'''
모든 작업이 마무리 되면 브라우저 종료
'''
def closeBrowser(browser):
    browser.quit()

'''
텔레그램 봇
동적 페이지 스크래핑을 완료하고 그 결과를 텔레그램으로 전송하여 자동화 체계를 완성시킨다.
'''
async def bot():
    bot = telegram.Bot(token = '6152505971:AAFgtAFyaA4Z53TEA0rsuoj9is7Ml4suKpQ')
    await bot.send_message('-1001935205192',
        '*** 온비드 지분분묘 물건번호 ***\n'
        '처분방식: 매각\n'
        '입찰기간: 2023-10-23 ~ 2023-10-27\n'
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
총건수 = browser.find_element(By.CSS_SELECTOR, '#collateralSearchForm > div.cm_paging.cl > p').text[3:-3] #추출요소값 [총 269 건]
전체페이지 = math.ceil(int(총건수) / 10) #결과 27
현재페이지 = 1
페이지인덱스 = 1

while True:
    #tr을 전부가져와서 len함수로 전체 로우 개수 구하고 전체 로우만큼 for문 돌리면서 분석한다
    매각물건rows = browser.find_elements(By.CSS_SELECTOR, '#collateralSearchForm > table > tbody > tr')
    for i in range(1, len(매각물건rows)+1):
    # for i in range(1, 11):
        # for k in range(1, 6):#검색결과리스트
        #     col= tbody.find_element(By.CSS_SELECTOR, '#collateralSearchForm > table > tbody > tr:nth-child('+str(i)+') > td:nth-child('+str(k)+')')
        #     print(col.text)
        # time.sleep( random.uniform(3,10) ) # 랜덤한 시간으로 쉬어줘 ==> 타겟 시스템이 스크래핑 봇인줄 모르게 하기 위하여 사용
        try:
            #해당 물건 상세 페이지로 이동
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
        
        #압류재산정보탭으로 이동하여 유의사항 체크
        압류재산정보 = browser.find_elements(By.CSS_SELECTOR, '#dtbuttontab')[1]
        browser.execute_script("arguments[0].click();", 압류재산정보)
        browser.implicitly_wait(30) # seconds

        유의사항 = browser.find_element(By.CSS_SELECTOR, '#pytnMtrs')
        
        #예시 물건관리번호 : 2022-05637-003
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

                if 등기사항전체페이지 == 등기사항현재페이지: #마지막페이지면 종료
                    break
                elif (len(공유자) > 10): #공유자10명 이상이면 패스
                    break
                else:
                    등기사항현재페이지 = 등기사항현재페이지+1
                    등기사항페이지인덱스 = 등기사항페이지인덱스+1
                    등기사항페이지 = browser.find_element(By.CSS_SELECTOR, '#paging2 > a:nth-child('+str(등기사항페이지인덱스)+')')
                    browser.execute_script("arguments[0].click();", 등기사항페이지)
                    browser.implicitly_wait(20) # seconds
                    # WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#resultRgstImfoList > tr:nth-child(1) > td:nth-child(2)')))

            #DataFrame은 엑셀처럼 사용하기 편하고 컬럼별 혹은 로우별 다양한 연산 기능을 제공함
            if (len(공유자) > 0):
                df = pd.DataFrame({'공유자':공유자, '개수':개수})
                # print(df)
                # print(df.groupby('공유자').size())
                # print(df.groupby('공유자').sum())
                
                '''
                지분분묘에서 최종 의사 판단은 공유자가 가족이나 친인척 관게인지를 확인하는 것이다.
                아래와 같이 공유자를 그룹별로 나누면 김** 8, 이** 1, 서** 1 와 같은 형태의 결과가 나온다.(예시))
                그러면 이 경우에는 70프로가 넘는 사람이 동일 성씨를 가지고 있으니 가족묘라고 생각하고 입찰을 할 수 있다.
                '''
                #공유자별로 합계를 낸다
                s = df.groupby('공유자').sum()
                tot = s.sum() #전체 공유자 수
                top = s.iloc[0] #가장 많은 공유자 그룹의 수
                # print(tot)
                # print(top)

                ret = (top/tot) 
                # print(ret)

                if ret.iloc[0] > 0.7:
                    # print('공유자매수진입')
                    print('분묘 : '+물건관리번호.text)
                    지분분묘물건번호.append(물건관리번호.text) #텔레그램으로 대상 물건을 보내기 위하여 추가
                # else:
                #     print('공유자매수포기')
        # else:
            # print('no 분묘')
        
        #물건을 분석하였으면 다시 목록으로 이동한다. 
        목록 = browser.find_element(By.CSS_SELECTOR, '#Contents > div.btn_C.mt20 > a')
        browser.execute_script("arguments[0].click();", 목록)
        browser.implicitly_wait(30) # seconds
        # time.sleep( random.uniform(3,10) ) # 랜덤한 시간으로  쉬어줘

    print('전체페이지'+str(전체페이지))
    print('현재페이지'+str(현재페이지))
    if 전체페이지 == 현재페이지:
        break
    else:
        '''
        온비드만의 특성으로 페이지를 오래도록 스크래핑하면 통신이 끊어진다. 
        이것은 서버측에서 봇 회피를 위한 설정으로 인해 끊어버리는 것으로 의심된다.
        이를 파훼하기 위하여 10페이지마다 기존 브라우저는 종료시키고 
        신규로 브라우저를 여는데 앞뒤로 랜덤하게 5~10초 지연시키고 요청한다.
        '''
        if 현재페이지%10 == 0:
            browser.quit()
            time.sleep( random.uniform(5,10) ) # 랜덤한 시간으로  쉬어줘
            browser = openBrowser()
            time.sleep( random.uniform(5,10) ) # 랜덤한 시간으로  쉬어줘

        현재페이지 = 현재페이지+1
        '''
        특정 화면 텍스트에 자바스크립트를 엮어서 호출하는 경우에 아래 execute_script를 사용한다. 
        대표적으로 페이징 처리시 페이지 텍스트에 연결된 자바스크립트를 호출하기 위하여 아래와 같이 사용한다. 
        '''
        browser.execute_script("fn_paging({0})".format(현재페이지))        
        browser.implicitly_wait(30) # seconds

#asyncio.run(bot()) #텔레그램 봇 실행하는 코드
print(time.strftime('%Y.%m.%d - %H:%M:%S')) # 년.월.일 - 시간