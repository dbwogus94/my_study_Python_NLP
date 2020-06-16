import requests
from bs4 import BeautifulSoup
import mariaDB
import pickle
from time import sleep

'''
잡코리아 it(웹프로그래밍, 응용프로그래밍)부분 자소서 크롤링, DB추가
'''

# 요청
def getRequest(url):
    request = requests.get(url)
    return request

# 파서
def getParser(request):
    soup = BeautifulSoup(request.content, "html.parser")
    return soup

# 회사
def getCompany(parser):
    mata = parser.findAll("meta")
    company = mata[7].findAll("meta")[0]
    return company.get("content")

# 분류(기간)
def getPeriod(parser):
    mata = parser.findAll("meta")
    period = mata[7].findAll("meta")[1]
    return period.get("content")

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


def Run(url, groupno):
    request = getRequest(url)
   
    # 응답되었다면 실행
    if(request.status_code == 200):
        parser = getParser(request)  # 정상 응답되었다면 파서 
        if(len(parser.findAll("meta")) == 0):       # 예외처리 
            print("페이지가 없습니다.")
        else:
            # 테이블 칼럼 : 시퀀스  그룹번호(같은자소서)  회사   분류(시기)   스팩(/)    질문    내용
            
            # 하나의 그룹마다 QnA개수 만큼 반복 >>> (질문 / 답) 이 2가지만 바뀌면서 할 것임

            # 같은 그룹번호(main에서 선언)
            # 회사 
            company = getCompany(parser)
            # 분류(기간) 
            period = getPeriod(parser)
            # 스팩
            spec = getSpec(parser)
            # 질문
            questionList = getQuestionList(parser)
            # 답
            answerList = getAnswerList(parser)  
            
            # DB 추가
            print(groupno, company, period, spec, questionList[0], answerList[0])
            for i in range(len(questionList)):
                mariaDB.insertOne(groupno, company, period, spec, questionList[i], answerList[i])
                print(groupno, " 추가!")
    else:
        print("접속실패 : ", request.status_code)


# url 리스트 파일로 쓰기
'''
def urlWrite():
    url = []
    with open("url_list", "wb") as f:
        pickle.dump(url, f)
'''        
# 파일 읽어 오기
def urlRead():
    with open("url_list", "rb") as f:
        urlList = pickle.load(f)
    return urlList


if __name__ == '__main__':
    print("잡코리아 it(웹프로그래밍, 응용프로그래밍)부분 자소서 크롤링 시작")
    url = urlRead()
    groupno = 1
    INTERBAL = 10

    for i in url:
        Run(i, str(groupno))
        groupno += 1
        sleep(INTERBAL)

     
    #  자동화 업그래이드 해야함