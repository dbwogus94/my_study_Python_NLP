from konlpy.tag import Twitter          # 단어토큰화 모듈
import pickle                           # 파일 입출력 내장 모튤
from gensim.models import Word2Vec      # 임베딩에 사용되는 모듈
import mariaDB_coverletter02 as mariaDB                          # DB접근 모듈
from functools import reduce


# conda install -c conda-forge gensim >> 워드 투 백터(Embedding) 모듈 추가함
    # 임베딩(Embedding) 
    # word to Vec >>> 단어 백터화
    # doc to Vec >>> 문장을 백터화


# 단어 토큰화 실행  > return : dict
def Nounsp():
    all = mariaDB.selectAll()   # DB에서 데이터 읽어오기
    tw = Twitter()              # Twitter 인스턴스화
    res = []                    # 결과 res = {seq : content...}

    for doc in all:
        context = doc[8]                # context 칼럼 가져오기
        tuple_List = tw.pos(context)     # 단어 토큰화
        
        
        # for i in range(len(tuple_List[:4])):
        #     if(tuple_List[i][1] == "Noun"):
        #         tem.append(tuple_List[i][0])

        tem = list(filter(lambda x : x[1] == "Noun", tuple_List))       # filter(함수 , 이터레이터) == 걸러내는것=>제네래이터 , reduce(함수, 이터레이터, 초기값) => 값이나온다
                                                                        # filter(lambda x : x[1] == "Noun", tuple_List)
                                                                                # 람다 item : 조건(bool , 0 or 1~ , '' or " "~ , None > false ), 이터레이터
                                                                        # reduce(lambda x, y : x+y, a, 2) >> 17
                                                                        # 머신러닝에서 가장 중요한것은 모든 작업에 불변의 값을 인풋으로 넣는것을 보장 해야한다.
                                                                        #             

        res.append([i[0] for i in tem])            # 시퀀스(Pk) = key, context = value
    return res


'''
태그 > 특수문자 > 오타 > 불용어 >  테깅 >> 토큰화 > 임베딩 >  
'''

# 단어 토큰화 파일 저장
def fileWrite():
    res = Nounsp()                  # 단어 토큰화 실행
    with open("nouns02", "wb") as f:  # with문을 쓰면 io를 자동 close(), "nouns" 새파일이름 / "wb(write byte)" 바이트로 작성
        # pickle : 파이썬 내장 모듈 파일 입출력 스트림
        pickle.dump(res, f)         # res(데이터 객체), f(file객체) >>  파일을 쓰기 실행
                                            # >>> python은 파일을 쓸때 자동으로 해당 파일에 작성된 객체정보를 직열화해 파일을 쓴다.
                                            # >>> 그리고 읽어올 때 직열화된 데이터를 읽어 자동으로 해당 객체로 포메팅하여 읽어온다.


# 토큰화된 파일 읽어오기 : return 토큰(dict)
def fileRead():
    with open("nouns02", "rb") as f:  # with문 스트림 자동닫기, "nouns(읽어올 파일)" / "tb(text byte)"텍스트를 바이트로 읽기
        tokens = pickle.load(f)       # f(file객체) > 파일에서 직열화데이터를 통해 자동으로 python객체로 포메팅(맵핑)하여 읽어온다.
        print(tokens)
    return tokens;




# 임베딩 데이터파일 생성, 쓰기
def EmbedWrite():
    tokens = fileRead()                    
    values = tokens   

    # 단어 임베딩 : from gensim.models import Word2Vec 모듈 사용
    model = Word2Vec(values, size=100, window=12, min_count=3, workers=4)   # 차원이란 >> 정보를 줄이는것
          # Word2Vec(읽어올 단어토큰(이중배열),  100차원,  해당단어 주변 범위, 세번 반복 이하로 나오는 단어는 제외, 코어(pc성능에 따라 다름))
    model.save("WordToVec03")     # 파일이름 "WordToVec"으로 단어토큰을 백터화(임베딩)시킨 데이터 저장


# Embedding 파일 읽어서 객체생성
def getEmbedding():
    return Word2Vec.load("WordToVec03")   # Word2Vec모듈의 함수 .load()에 인자로 읽어올 파일을 넣어준다.


# 긍정 부정 모두 탐색
def RunEmbedding(model, positiveArr, negativeArr, res_count):
    # model = getEmbedding()     # 임베딩한 데이터 가져오기
    # .most_similar(positive=["긍정어1", "긍정어2"...], negative=["부정어1", "부정어2"...], topn=10(상위 몇개를 결과를 가져올지 설정))
    res = model.most_similar(positive=positiveArr, negative=negativeArr, topn=10)
    return res
    
    
    
    # 예시) 다른 파라미터도 추가로 있음.(doc참고)
    #res01 = model.most_similar(positive=["과제"], negative=["도전"], topn=10)
    #res02 = model.most_similar(positive=["도전"], topn=10)
    #res03 = model.most_similar(negative=["도전"], topn=10)

# 긍정어만 탐색    
def RunEmbedding_pos(model, positiveArr, res_count):
    #model = getEmbedding()
    return model.most_similar(positive=positiveArr, topn=res_count)

# 부정어만 탐색
def RunEmbedding_neg(model, negativeArr, res_count):
    #model = getEmbedding()
    return model.most_similar(negative=negativeArr, topn=res_count)



if __name__ == '__main__':

    #print(Nounsp())
    
    
    # 데이터 읽어와서 토큰화 파일저장
    #fileWrite()

    #토큰화된 파일 읽어서 출력
    
    #token = fileRead()
    #print(token)

    # 토큰화된 파일을 읽와서 임베딩(토큰화된 단어를 수치화하여 백터영역 넣기) 임베딩 파일생성 쓰기
    
    #EmbedWrite()

    # 임베딩한 파일 읽어와서 객체 생성
    #Embedding= getEmbedding()
    #print(Embedding)


    # 최종 코드
    # 모델에서 단어 분석 >> 단어 유사도 측정
    model = getEmbedding()
    #a = ["도전"]
    print(model.most_similar(positive=["학위"], topn=10))
    #print("긍정/부정 사용 유사도 측정: ",RunEmbedding(model, ["도전"], ["실패"], 5))

    #print("긍정 사용 유사도 측정: ",RunEmbedding_pos(model, ["도전"], 5))
    #print("부정 사용 유사도 측정: ",RunEmbedding_neg(model, ["실패"], 5))
    

    # 아래 프로세스 종료 코드
    from sys import exit
    exit(0)
    print("종료된 코드")
    




    


    
    
    
