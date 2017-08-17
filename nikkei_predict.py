 # -*- coding: utf-8 -*- 

 
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
import urllib
import time
import requests
from datetime import datetime, timedelta
import tweet as tw
import random
from sklearn.svm import SVR

#データの準備
def dataset(get_data):
    data_all = pd.DataFrame(get_data)
	#正解データを用意
    data_answer = data_all['CLOSE']
	#先頭行を削除
    data_answer = data_answer.drop(0)
    data_answer = data_answer.reset_index(drop=True)
    data_answer = np.array(data_answer)
    data_answer = data_answer[::-1]
    data_answer = data_answer.astype(float)
	#末行を削除
    data_all = data_all.drop(len(data_all)-1)	
    data_all = data_all.reset_index(drop=True)
    data_all = np.array(data_all)
    data_all = data_all[::-1]
	#date列の削除
    data_all = np.delete(data_all,0,1)
    data_all = data_all.astype(float)
    return data_all ,data_answer

#APIを読み込んでCSVデータに整える
def getData(url):
    url = url
    url_contents = requests.get(url)
    lines = url_contents.text.splitlines()
	#カラムの取得---"="で区切った後にindex[1]のカラムを","区切りの配列に変換--
    columns = lines[4].split("=")[1].split(",")
	#価格の取得
    prices = lines[8:]

    first_cols = prices[0].split(",")
	#一行目のタイムスタンプを日時表示に変換
    first_date = datetime.fromtimestamp(int(first_cols[0].lstrip('a')))
    result = [[first_date.date(), first_cols[1], first_cols[2], first_cols[3], first_cols[4], first_cols[5]]]
    #カンマ区切りでデータを追加
    for price in prices[1:]:
        cols = price.split(",")
        #timedeltaオブジェクトで表される1行目の日時との差分を加算して日付を表示
        date = first_date + timedelta(int(cols[0]))
        #先に追加した1行目に2行目以降を追加していく
        result.append([date.date(), cols[1], cols[2], cols[3], cols[4], cols[5]])
        df = pd.DataFrame(result, columns=columns)
    return df


code_list = ["7203","9432","9437","8306","9984","9433","2914","6861","7182","6178","8316","7267","6758","7974","7751","8411","4502",
              "7201","6954","6902","4063","9020","8058","3382","6981","5108","9022","6594","6752","6098","6503","6501","9983","8766",
              "4452","6367","7270","4661","8031","4689","8001","4503","7269","6301","8802","1925","4578","6971","5401","7741"]

company_list = ["トヨタ自動車","NTT","ＮＴＴドコモ","三菱ＵＦＪフィナンシャル・グループ","ソフトバンクグループ","ＫＤＤＩ","ＪＴ","キーエンス","ゆうちょ銀行","日本郵政","三井住友フィナンシャルグループ",
                "ホンダ","ソニー","任天堂","キヤノン","みずほフィナンシャルグループ","武田薬品工業","日産自動車","ファナック","デンソー","信越化学工業","JR東日本","三菱商事","セブン＆アイ・ホールディングス",
                "村田製作所","ブリヂストン","JR東海","日本電産","パナソニック","リクルートホールディングス","三菱電機","日立製作所","ファーストリテイリング","東京海上ホールディングス","花王","ダイキン工業","ＳＵＢＡＲＵ",
	            "オリエンタルランド","三井物産","ヤフー","伊藤忠商事","アステラス製薬","スズキ","コマツ","三菱地所","大和ハウス工業","大塚ホールディングス","京セラ","新日鐵住金"]

#ランダムで企業を選定
counter = random.randint(0,49)
search_code = code_list[counter]
search_company = company_list[counter]											
url = "https://www.google.com/finance/getprices?p=1Y&i=86400&x=TYO&q=" + str(search_code)

#APIからデータを取得
get_data = getData(url)
data_all ,data_answer = dataset(get_data)
#訓練用データとテスト用データに分離
X_train, X_test, y_train, y_test = train_test_split(data_all, data_answer, random_state=0)

#モデルを生成して訓練を実行
lr = SVR()
lr.fit(X_train, y_train)

#モデルの精度を算出
score = lr.score(X_test, y_test)
print("テストデータ正解率:"+str(1+score))
#予測を実行
newest = np.array([data_all[0]])
prediction = lr.predict(newest)

#前日データを格納
lastday = round(data_answer[0],1)
#予測データを格納
result = prediction[0]
nextday = round(result,1)

#変化率を算出
rate = nextday / lastday 
rate = round(rate,3)
rate = str(rate)
 
rate_comment = ""
prediction_comment = ""

#前日データと比較してコメントを格納
if prediction > lastday:
    rate_comment = "前日比："+rate+"pt上昇すると予測します！"
    counter1 = random.randint(0,4)
    up_comment_list = ["もしかしたら買い時かもしれません...(*´ω｀*)","予測が外れたらごめんなさい...！( ;∀;)","今がチャンス！？...かもしれません...(; ･`д･´)","結果が楽しみですね...!(*^-^*)","当たるといいなぁ..."(;'∀')]
    prediction_comment = up_comment_list[counter1]
else:
    rate_comment = "前日比："+rate+"pt下落すると予測します！"
    counter1 = random.randint(0,4)
    down_comment_list = ["もしかしたら売り時かもしれません...!(; ･`д･´)","我慢の時かもしれません...!(+_+)","明日はもしかしたら上がるかも...!?(/・ω・)/","あくまで参考の一つにしてくださいね...!(;・∀・)","買うか売るかはあなた次第です...!(。-`ω-)"]
    prediction_comment = down_comment_list[counter1]

#ツイート内容を格納
tweet_contents = "【本日の株価予測】"+"\n"+"コード："+str(search_code)+"\n"+"銘柄名："+str(search_company)+"\n"+"予測終値："+str(nextday)+"円"+"\n"+"前日終値："+str(lastday)+"円"+"\n"+rate_comment+"\n"+"\n"+prediction_comment+"\n"+"#投資"+" "+"#株価"+" "+"#株価予測"+" "+"#人工知能"+" "+"#機械学習"
print(tweet_contents)
#ツイート実行
tw.postTweet(tweet_contents)


