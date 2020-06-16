import requests     # 주소를 요청하는 모듈
from bs4 import BeautifulSoup


request  = requests.get("http://www.jobkorea.co.kr/starter/PassAssay/View/200000?Page=1&OrderBy=0&FavorCo_Stat=0&schPart=1000100%2C1000101&Pass_An_Stat=0");  #seq=14596
soup = BeautifulSoup(request.content, "html.parser")
print(request.status_code)
print(soup.find("body"))



# # 메타데이터
meta = soup.findAll("meta")
print(meta)
# # 메인 컨테이너
# container = soup.find("div", {"id" : "container"})

# # 회사
# company = mata[7].findAll("meta")[0]
# #print(company.get("content"))

# # 분류(기간)
# period = mata[7].findAll("meta")[1]
# #print(period.get("content"))




# # 스팩 
# specUL = container.find("ul", {"class" : "specLists"})
# specList = specUL.findAll("li")
# specList = [i.text for i in specList if i != specList[len(specList)-1]]     # 마지막 원소 하나 제거
# specS = "&".join(specList)
# #print(specS)


# # 질문
# PnA = container.find("dl", {"class" : "qnaLists"})
# questionList = PnA.findAll("span", {"class" :"tx"})
# answerList = PnA.findAll("div", {"class" : "tx"})
# questionList = [i.text for i in questionList]
# answerList = [i.text for i in answerList]
# print(len(answerList))

# print(answerList[0])
# #print(questionList[0].text)
# #print(answerList[0].text)

# # time = soup.find("meta", {"property" : "og:description"})


'''
시퀀스  그룹번호(같은자소서)  회사   분류(시기)   스팩(/)    질문    내용


'''




