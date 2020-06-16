# 이력서 크롤링 자동화 코드 
import requests
from bs4 import BeautifulSoup
import asyncio
import mariaDB_coverletter02 as maria
from time import sleep

# 요청
def getRequest(url):
    request = requests.get(url)
    return request

# 파서
def getParser(request):
    soup = BeautifulSoup(request.content, "html.parser")
    return soup



# 탐색
def tagSearch_lis(parser):
    ul = parser.find("ul", {"class":"selfLists"})
    return ul.findAll("li") # ul 밑의 모든 li


# [회사명, 기간, 대상, 카테고리]
def columnList(li):     # li 한개를 받는다
    p = li.find("p", {"class":"tit"})
    company = p.find("span").text
    spans = p.find("span", {"class":"linkArray"})
    columns = [i.text for i in spans.findAll("span")]
    columns.insert(0, company)
    return columns


# 새로 파싱할 url을 얻는다.
def getUrl(li): # li 한개를 받는다
    url = "http://www.jobkorea.co.kr"
    a = li.findAll("a", {"class": "logo"})
    back_url = a[0]["href"]
    return url + back_url




# 스팩
def getSpec(parser):
    container = parser.find("div", {"id" : "container"})
    specUL = container.find("ul", {"class" : "specLists"})
    specList = specUL.findAll("li")
    specList = [i.text for i in specList if i != specList[len(specList)-1]]     # 마지막 원소 하나 제거
    specS = "&".join(specList)
    return specS

# 질문 리스트
def getQuestionList(parser):
    container = parser.find("div", {"id" : "container"})
    PnA = container.find("dl", {"class" : "qnaLists"})
    questionList = PnA.findAll("span", {"class" :"tx"})
    questionList = [i.text for i in questionList]
    return questionList

# 답변 리스트
def getAnswerList(parser):
    container = parser.find("div", {"id" : "container"})
    PnA = container.find("dl", {"class" : "qnaLists"})
    answerList = PnA.findAll("div", {"class" : "tx"})
    answerList = [i.text for i in answerList]
    return answerList
    

if __name__ == '__main__':
    INTERBAL = 2
    groupno = 1
    page = 1;
    while page < 309: # 페이지 308까지 있음
        page += 1
        print(page)
        url = "http://www.jobkorea.co.kr/starter/PassAssay?FavorCo_Stat=0&Pass_An_Stat=0&OrderBy=0&EduType=0&WorkType=0&isSaved=0&Page="+str(page)
        parser = getParser(getRequest(url))
        
        lis = tagSearch_lis(parser)
        for li in lis:
            # [기간, 대상, 카테고리, 회사명]
            columns = columnList(li)
            # 새로운 파서
            newParser = getParser(getRequest(getUrl(li)))
            # 스펙 추가
            columns.append(getSpec(newParser))
            # 질문리스트
            questions = getQuestionList(newParser)
            # 답리스트
            answers = getAnswerList(newParser)
            #print(columns)
            
            for i in range(len(questions)):
                #maria.insertOne(groupno, company, period, target, category, spec, question, context)
                maria.insertOne(groupno, columns[0], columns[1], columns[2], columns[3], columns[4], questions[i], answers[i])
                #print(groupno, columns[0], columns[1], columns[2], columns[3], columns[4], questions[i], answers[i])
            groupno += 1
            sleep(INTERBAL) 
             




        





    






