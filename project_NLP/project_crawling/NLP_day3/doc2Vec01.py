from konlpy.tag import Twitter          # 단어토큰화 모듈
import pickle                           # 파일 입출력 내장 모튤
from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument      # doc to vec에 사용되는 모듈
import mariaDB_coverletter02 as mariaDB                         # DB접근 모듈
from functools import reduce
from sklearn.feature_extraction.text import TfidfVectorizer             # pip install sklearn   tf-idf                                                                                                                                                                                               
from sklearn.feature_extraction.text import CountVectorizer                                                                                                                                                                                                             


# doc2vec는 태그가 중요

# 종료 
def sysExit():
    from sys import exit
    exit(0)


def selectAll():
    return mariaDB.selectAll()


#  return >>> [
#               (#1, [pk 1번 context의 단어, pk 1번 context의 단어, pk 1번 context의 단어, ...]),
#               (#2, [pk 2번 context의 단어, pk 2번 context의 단어, pk 2번 context의 단어, ...]),
#               (#3, [pk 3번 context의 단어, pk 3번 context의 단어, pk 3번 context의 단어, ...])              
#              ]
def getTokenization(date):
    all = date                  # 훈련에 사용될 데이터(코퍼스)
    tw = Twitter()              # Twitter 인스턴스화, 단어토큰화 라이브러리
    res = []                    

    for doc in all:
        # context 칼럼 가져오기
        context = doc[8]                 
        # 품사태깅 단어 토큰화
        tuple_List = tw.pos(context)     
        
        # tuple_List = [(단어,태깅), (단어,태깅), (단어,태깅)]에서 태킹이 Noun(명사)인 item 가져오기 
        # filter(함수 , 이터레이터) == 걸러내는것 => 제네래이터 , reduce(함수, 이터레이터, 초기값) => 값이나온다
        tem_Noun = list(filter(lambda x : x[1] == "Noun", tuple_List))      

        # 파싱
            #1. res[n][0] >>> "res[n][0] = #프라이머리키" 넣는다.
            #2. res[n][1] >>> tem_Noun = [(단어, "Noun"), (단어, "Noun") ... ]에서 res[n][1] 단어만 모두 넣는다.
        res.append(("#"+str(doc[0]),[i[0] for i in tem_Noun]))           
            # 결과. all 한 번 반복 되었을 때 >>> res[0][1] = [("#1", [프라이머리키1의 context 단어, 프라이머리키1의 context 단어]... )] 
    return res


# doc2Vec 훈련전에 태깅 적용
def tagging(tokenization_corpus):   # 태그된 단어토큰화 코퍼스를 인자로 받는다
    tag_List =[]
    for tagId, textList in tokenization_corpus:
        # 빈 list에 gensim.models.doc2vec.TaggedDocument(코퍼스, 태그list) 사용하여 훈련에 사용 될 코퍼스에 태깅 적용
            # tags = 태그를 부여함[] >>> 태그는 여러개가 가능하고, 키워드를 넣어서 머신이 훈련할때 참조시킨다(백터영역에 임베딩 참조)
        tag_List.append(TaggedDocument(words=textList, tags=[tagId]))  
    return tag_List
 
# 태깅이 적용된 코퍼스(명사 단어 토큰화되어 있음)로 doc2Vec 임베딩(훈련) 
def training(tagging_corpus):
    # 훈련 
    # >>> Doc2Vec(태깅된 코퍼스(이중배열), vector_size(백터차원), window(가져올 주변 백터 영역), min_conut=3(3번이하로 반복되는 단어 제외), workers=4(cpu 코어))
    model = Doc2Vec(tagging_corpus, vector_size=100, window=8, min_conut=3, workers=4)
    return model

# 훈련된 모델을 파일로 저장(객체 직열화)
def saveModel(model, file_name):
    model.save(file_name)

# 훈련된 모델 파일 load
def loadModel(file_name):
    return Doc2Vec.load(file_name)

# 훈려된 모델 테스트
def testModel(model, positiveList):
    #return model.docvecs.most_similar(positive=["#1010"])
    return model.docvecs.most_similar(positive=positiveList)

if __name__ == '__main__':

    # pk 테그를 넣은 명사 토큰화
    #token = getTokenization(selectAll())
    
    # 훈련전 코퍼스에 넣어놓은 테그 적용(훈련에 참고됨)
    #tagging_token = tagging(token)

    # 훈련된 모델 파일로 저장
    #saveModel(training(tagging_token), "doc2vec_model")


    # 모델파일 읽어 오기 
    model = loadModel("doc2vec_model")


    # 테스트
    testRes = testModel(model, "#11111")
    print(testRes)


    