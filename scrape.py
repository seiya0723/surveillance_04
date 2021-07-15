#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import requests,bs4


ID      = ""
PASS    = ""


URL     = "http://127.0.0.1:8000/"
LOGIN   = URL + "admin/login/"
TARGET  = URL + "admin/surveillance/information/"
TIMEOUT = 10
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'}


#TIPS:Djangoに対してrequestsライブラリからPOST文を送信する方法
# https://www.it-swarm-ja.com/ja/python/python-requests%e3%81%a7csrftoken%e3%82%92%e6%b8%a1%e3%81%99/1070253083/



#セッションを維持する(セッションメソッドからオブジェクトを作る)
client = requests.session()
client.get(LOGIN,timeout=TIMEOUT,headers=HEADERS)

#CSRFトークンを手に入れる
if 'csrftoken' in client.cookies:
    csrftoken = client.cookies['csrftoken']

login_data   = { "csrfmiddlewaretoken":csrftoken,
                 "username":ID,
                 "password":PASS
                 }

#ログインする
r   = client.post(LOGIN,data=login_data,headers={"Referer":LOGIN})
print(r)



#一覧ページ(TARGET)へアクセス、URLとメールアドレスのリストを手に入れる。
result  = client.get(TARGET,timeout=TIMEOUT,headers=HEADERS)
soup    = bs4.BeautifulSoup(result.content,"html.parser")

urls    = soup.select(".field-url")
emails  = soup.select(".field-email")


#URLとメールを全て表示
for url in urls:
    print(url.text)

for email in emails:
    print(email.text)



#urlとemailを辞書型のリスト型にする。
length  = len(urls)
data    = []

for i in range(length):
    data.append( { "url":urls[i].text, "email":emails[i].text } )
    
print(data)

