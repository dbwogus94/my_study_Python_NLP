import requests     # 주소를 요청하는 모듈
from bs4 import BeautifulSoup


request  = requests.get("http://www.saramin.co.kr/zf_user/public-recruit/coverletter?real_seq=1");  #seq=14596
soup = BeautifulSoup(request.content, "html.parser")
print(request.status_code)

print(soup.find("body"))

divList = soup.findAll("div", {"class" : "box_ty3"})


#print(len(divList))

# for i in range(len(divList)):
#     print(i, "번 ")        
#     print(divList[i])     # [0] 성격의 장단점, [1] 지원동기, [2] 입사 후 포부, [3] 자신이 지원한 직무의 역할에 대해 기술  


#print(divList[0])     # 내용


'''
div_logo = soup.findAll("div", {"class": "logo"})
#print(div_logo)
company_name = div_logo[0].find("span").text
print(company_name)
'''


