import requests
from bs4 import BeautifulSoup
import asyncio

request = requests.get("http://www.jobkorea.co.kr/starter/PassAssay?FavorCo_Stat=0&Pass_An_Stat=0&OrderBy=0&EduType=0&WorkType=0&isSaved=0&Page=1")
soup = BeautifulSoup(request.content, "html.parser")

# http://www.jobkorea.co.kr/starter/PassAssay?FavorCo_Stat=0&Pass_An_Stat=0&OrderBy=0&EduType=0&WorkType=0&isSaved=0&Page=308
# 1~308

ul = soup.find("ul", {"class":"selfLists"}) 

lis = ul.findAll("li")

# li 개수 = 20개
count_li = len(lis)

# 회사명, 기간, 대상, 카테고리
p = lis[1].find("p", {"class":"tit"})
company = p.find("span").text
print(company)

span = p.find("span", {"class":"linkArray"})
span = [i.text for i in span.findAll("span")]
span.append(company)
print(span)


from sys import exit
exit(0)

# url
a = lis[0].findAll("a", {"class": "logo"})
back_url = a[0]["href"]

url = "http://www.jobkorea.co.kr"

# 전체 경로
url = url + back_url

request = requests.get(url)
soup = BeautifulSoup(request.content, "html.parser")


# from sys import exit
# exit(0)

front_url = "http://www.jobkorea.co.kr"
for i in range(len(lis)):
    a = lis[i].findAll("a", {"class": "logo"})
    # 전체 url
    url = front_url + a[0]["href"]
    print(url)

    for j in range(1):
        request = requests.get(url)
        soup = BeautifulSoup(request.content, "html.parser")
        #회사이름
        meta = soup.findAll("meta")
        company = meta[7].findAll("meta")[0]
        print(company.get("content"))
    url = ""

