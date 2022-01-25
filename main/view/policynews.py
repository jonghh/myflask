from flask import Blueprint, render_template, request
from konlpy.tag import Okt
from newspaper import Article
from collections import Counter
import numpy as np
import pickle
import re
#from tensorflow.keras.models import load_model
from keras.models import load_model

bp = Blueprint('policynews', __name__, url_prefix='/')  # 파일 이름과 동일하게 policynews.

@bp.route('/policynews_input' )
def ask():
    return render_template('policynews_input.html')

@bp.route('/policynews_output', methods = ['POST'])
def result():
    #os.remove("/home/jongh/flask01/static/wordcloud.jpg") if os.path.exists("/home/jongh/flask01/static/wordcloud.jpg") else None
    try:
        url = request.form["txt1"]
        if "http" in url:
            news = Article(url.strip(), language='ko')
            news.download()
            news.parse()
            target_text = news.text
        else:
            if len(request.form["txt2"]) > 2:
                target_text = request.form["txt2"].strip()
            else:
                target_text = ""
    except:
        target_text = ""

    stopwords = "라고,news,News,기자,논설위원,해설위원,사진,특파원,연합뉴스,단독,오늘,뉴스,데스크,앵커,종합,1보,2보,3보,상보,생방송,종합2보,뉴스검색,통합검색,검색,네이버,다음,개월,가지,기준,\
                 뉴스룸,무단,전재,배포,금지,원본,연합,뉴시스,인턴,가운데,이날,이분,중요,한편,이번,지난달,뉴스1,관계자,오전,오후,인근,시간,신문,이후,이전,해당,답변,질문,인터뷰,\
                 속보,현장,앵커리포트,리포트,르포,뉴스,뉴스피처,피처,인터뷰,특징주,만평,팩트,팩트체크,동안,닷컴".split(",")
    try:
        t1= re.sub(r"[^가-힣a-zA-Z]", " ", target_text)       # re.sub: 문자열 부분 교체. r은 정규표현식 사용한다는 표시. "[^가-힣a-zA-Z1-9]"는 한글 영어 숫자 이외의 문자열 의미.
        t2 = Okt().nouns(t1)
        t3 = [ti for ti in t2 if len(ti)>1 ]          # 2음절 이상의 명사만 선택
        t4 = [ti for ti in t3 if ti not in stopwords] # stopwords에 포함된 단어 삭제
        txt_tokened=",".join(t4)
    except:
        txt_tokened=""

    common_words = Counter(txt_tokened.split(",")).most_common(100)
    common_words = ", ".join([i+":"+str(j) for i,j in common_words])

    model_1 = load_model("main/static/model27.h5")
    with open("main/static/model27_wordct.pickle","rb") as f:
        model27_wordct_loaded = pickle.load(f)

    max_doc_len = 500
    X_input = np.zeros([len(txt_tokened.split(",")), max_doc_len], dtype=np.int32)
    for i, sentence in enumerate([txt_tokened]):
        for t, word in enumerate(sentence.split(",")[:max_doc_len]):
            try:
                X_input[i, t] = model27_wordct_loaded[word]
            except:
                pass
    result = model_1.predict(X_input, batch_size=64)
    result_1 = str(result[0][1])
    if result[0][1] > 0.5: result_2 = "있습니다"
    else: result_2 = "없습니다"

    return render_template('policynews_output.html', target_text=target_text, common_words=common_words, result_1=result_1, result_2=result_2)
