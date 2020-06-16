from konlpy.tag import Twitter          # 단어토큰화 모듈
import pickle                           # 파일 입출력 내장 모튤
from gensim.test.utils import common_texts
#from gensim.models.doc2vec import Word2Vec, TaggedDocument      # doc to vec에 사용되는 모듈
import mariaDB_coverletter02 as mariaDB                         # DB접근 모듈
from functools import reduce
from sklearn.feature_extraction.text import TfidfVectorizer             # pip install sklearn                                                                                                                                                                                                  
from sklearn.feature_extraction.text import CountVectorizer                                                                                                                                                                                                             

'''
 tf_idf 설치순서
 인스톨 : pip install sklearn      
 import : from sklearn.feature_extraction.text import TfidfVectorizer   
 

 tf-idf 란?
 전체 문서에서 많이 나오는 단어는 스코어를 낮게준다
 한 문서에서 많이 나오는 단어는 스코어를 높게


 사용순서
 1. 데이터 저리 훈련
 데이터불러오기 >  전처리 > 품사태깅(Twitter) > 토큰화(Twitter)
 > 토큰화 2차원 배열을 1차원 배열 변환 > fit(data)함수를 통해 머신학습에 사용될 데이터의 기반 설정을 잡는다(학습데이터의 최소/최대 값 등등)
 > 전단계에서 만든 학습기반에 transform(data)함수를 이용해 훈련실행
 > tocoo()함수를 이용해 데이터를 사용하기 좋게 반환한다.  
 
 2. 훈련된 데이터 후처리
 > 1차. model는 키가 단어, value가 인덱스라서 사용하기 어려움 둘이 변경
 > 2차. 데이터 사용하기 좋게 처리     
    >>> # resDict = {문서1번 : [(단어인덱스, 스코어), (단어인덱스, 스코어), (단어인덱스, 스코어)...], ..., 문서2번 : [(단어인덱스, 스코어), (단어인덱스, 스코어),...]
 > 3차. 모델을 DB와 동기화 
    >>>  2차의 결과 resDict 내부에 순서에 따라 부여된 "문서n번"(이하 '문서id'로 칭함) "DB 프라이머리 키"로 변경  
 
 결과 : resDict = { DB프라이머리키1번:[(1번 key의 단어, 스코어), (1번 key의 단어, 스코어)...],  DB프라이머리키2번:[(2번 key의 단어, 스코어), (2번 key의 단어, 스코어)...], ...}

    # 프라이머리키를 통해 해당 문서의 단어 인덱스와 스코어 접근

'''


# db에서 불러오기
def selectAll():
    return mariaDB.selectAll()

# 종료 
def sysExit():
    from sys import exit
    exit(0)


# tf-idf 결과 파일 읽어오기 > dict
def loadFile():
    with open("tf_idfRes", "rb") as f:
        return pickle.load(f)




#품사 태깅 토큰화, enumerate
def getTokenization(input):
    tw = Twitter()
    corpus = []
    DBKey_dict = {}                           # 루프의 순서와 : db의 프라이머리 키를 {}로 만듬 > enumerate(이터레이터)

    for count, doc in enumerate(input):        # == zip(range(len(x),x))
        
        # 루프의 순서와 DB key를 대응시킨다(동기화) >>> {루프의 반복변수와 : DB의 프라이머리키}
        DBKey_dict[count] = doc[0]     
        
        # context 칼럼 가져오기
        context = doc[8]                 
        # 단어 토큰화
        tuple_List = tw.pos(context)    # tw.nouns() > 단순 단어 토큰화, tw.pos() 품사태깅 단어토큰화
        
        # 명사만 추출
        # 품사태깅된 단어 토큰화된 리스트에서  [(명사단어, Noun), ...] 명사를 의미하는 "Noun"만 추출
        tem = list(filter(lambda x : x[1] == "Noun", tuple_List))       
        
        # 코퍼스 1차원 배열로 변환
        # TF-IDF라이브러리인 sklearn는 코퍼스를 1차원 배열로 줘야함   <==> word2Vec는 코퍼스 2차원 배열로 받는다.
        corpus.append(" ".join([i[0] for i in tem]))   # >>> 1차원 배열   
    
    # 1차원 배열 코퍼스, 동기화에 사용될 dict({반복변수 : db Key})
    return  corpus, DBKey_dict     
        

    
def training(corpus): 
# 훈련 >> tf-Idf : 빈도수, 스파스매트릭스 ,, 1차원 배열로 할 것
    vector = TfidfVectorizer().fit(data)    # 훈련하기 전에 데이터를 통해 훈련 기반을 만든다(단어를 인덱싱..등등)

    v0 = vector.transform(data)             # transform(값): 훈련, 파씽한 배열(여기서는 자소서한개) 빈도수를 분석해서 
                                            # 결과 >> "(docID, 단어인덱스)  스코어(빈도에 따른점수를 출력)"         
                                                                                                                                                                                                              
    model = v0.tocoo()                      # .tocoo() 사용자가 핸들링하기 좋은 형식으로 변환(? 근데 v0, v1 차이없음)

    corpusIndexing = vector.vocabulary_     # 훈련기반 데이터에서 인덱싱된 단어를 dict({단어:인덱스...})로 반환해준다   

    return model, corpusIndexing


# 1차. model는 키가 단어, value가 인덱스라서 사용하기 어려움 둘이 변경
# 2차. 데이터 사용하기 좋게 처리     
#   >>> # resDict = {문서1번 : [(단어, 스코어), (단어, 스코어), (단어, 스코어)...], ..., 문서2번 : [(단어, 스코어), (단어, 스코어),...]
# 3차. 모델을 DB와 동기화 
#   >>>  2차의 결과 resDict 내부에 순서에 따라 부여된 "문서n번"(이하 '문서id'로 칭함) "DB 프라이머리 키"로 변경  
def postprocessing(model, DBKey_dict):
    # 1차
    newCorpus = {}     
    for i in model:         # i key
        var = model[i]
        newCorpus[var] = i     # >> {키(단어index) : value(단어)} 

  
    # 2차, 3차 동시실행
    resDict = {}
    arrTem = []
    docID = 0

   
    # zip() >>> 각각의 배열의 인덱스끼리 역어준다 
    for i, j, k in zip(model.row, model.col, model.data):    # 문서id, 단어index, 스코어(단어의 빈도에 따른 스코어)
        
        # 문서id가 다르면 실행 
        if docID != i:   
            # 같은 문서끼리 묵인 배열[(단어index, 스코어)...]에서 스코어 기준으로 내림차순 정렬(높은게 위로)
            arrTem = sorted(arrTem, key=lambda x : -x[1])[:3]   
                                                  # - 를 붙여서 양수 음수 변환 >>> 내림차순한다. 그리고 상위 3개만 가져온다.
            
        # 3차 : 문서id를 바꿔서 모델을 DB키로 동기화
            # DBKey_dict에서 문서id(docID)를 key로 넣으면 "DB 프라이머리키"를 반환
            # 즉, 최종 결과 딕셔너리에 
            #     Key를 "DB프라이머리키"로 하고 
            #     value를 그 프라이머리키에 대응한 문서로 훈련된 [(단어, 스코어), (단어, 스코어)...]배열을 넣는다
            resDict[DBKey_dict[docID]] = arrTem             
            
            # 해당 문서번호를 전부 파싱했으면 tem을 다음 문서번호로 변경
            docID = i
            
            # 같은 문서를 배열로 묶는 임시 배열 초기화
            arrTem = []    
        else:   
            # 문서id가 같으면 >>> 같은 문서라면 하나의 배열에 추가  
            # 추가할 때 키를 단어인덱스로 값을 단어로 가진 newCorpus를 사용해 단어를 넣는다.
            # j = 단어 인덱스
            arrTem += [(newCorpus[j], k)]
    
    return resDict      # resDict = { DB프라이머리키1번:[(단어, 스코어), (단어, 스코어)...],  DB프라이머리키2번:[(단어, 스코어), (단어, 스코어)...], ...}

def modelSave(resDict):         
    with open("tf_idfRes", "wb") as f:
        pickle.dump(resDict, f)


if __name__ == '__main__':
    print(loadFile())
    




