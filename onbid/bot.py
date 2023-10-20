import asyncio
import telegram

지분분묘물건번호 = ['1', '1', '2']
async def main(): #실행시킬 함수명 임의지정
    token = "텔레그램 봇 API" 
    bot = telegram.Bot(token = '6152505971:AAFgtAFyaA4Z53TEA0rsuoj9is7Ml4suKpQ')
    # await bot.send_message('-1001935205192',지분분묘물건번호)
    await bot.send_message('-1001935205192',
        '검색일: 2023-04-10 ~ 2023-04-14\n'
        '입찰가: 0~1억\n'
        '용도선택: 토지\n'
        '상세용도: 대지, 임야, 전, 답, 과수원, 잡종지\n'
        '지역: 전체\n'
        '지분여부: 지분\n'
        '추가검색조건: 유의사항에 분묘 안내 포함하고, 공유자 중 동일 성씨가 70% 이상인 경우(가령, 5명중 4명이 동일 성씨)만 추출'
    )

asyncio.run(main()) #봇 실행하는 코드
