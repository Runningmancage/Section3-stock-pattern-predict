from ast import Str
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
browser = webdriver.Chrome()
browser.maximize_window()

url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
browser.get(url)

#초기 조건 체크해제
checkboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in checkboxes:
     if checkbox.is_selected():
        checkbox.click()

#원하는 조건 체크
items_to_select = ['영업이익', 'PER', '자산총계', '매출액']
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, '..') 
    label = parent.find_element(By.TAG_NAME, 'label')
    if label.text in items_to_select:
        checkbox.click()

#적용하기 버튼 클릭
btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]')
btn_apply.click()

for idx in range(1, 40): #1이상 40미만
    #사전작업 : 페이지 이동
    browser.get(url + str(idx))
    #데이터 추출
    df = pd.read_html(browser.page_source)[1]  #url 넣어도 되고, html page
    df.dropna(axis='index', how='all', inplace=True)
    df.dropna(axis='columns', how='all', inplace=True)
    if len(df)==0: #더 이상 가져올 데이터가 없으면?
        break

    #파일저장
    f_name = 'stocks_price(0827).csv'
    if os.path.exists(f_name):
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)
    else:
        df.to_csv(f_name, encoding='utf-8-sig', index=False)
    print(f'{idx} 페이지 완료')

browser.quit() #browser 종료