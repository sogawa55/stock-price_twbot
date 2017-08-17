# 株価予測Twitterbot

## botの特徴
* 東証一部上場企業上位50社の明日の株価を予測して自動ツイートするTwitterbot
* 一定時間ごとに50社の中からランダムで企業を選定して予測株価をツイート
* 過去1年間分の初値、終値、最安値、最高値、出来高の数値を教師データとして使用
* Google finane APIからデータを取得
* サポートベクタ回帰分析アルゴリズムを使用した統計的な予測
* ランダムでbotのコメントも付与

<img src="https://user-images.githubusercontent.com/26180642/29406391-e3a24966-837b-11e7-97d0-66dd39eabdbb.jpg" width="400px">
<img src="https://user-images.githubusercontent.com/26180642/29406417-fbba50ac-837b-11e7-8d83-a1008f35cc77.jpg" width="400px">
<img src="https://user-images.githubusercontent.com/26180642/29406453-0f413834-837c-11e7-879c-fd5620eb9dd4.jpg" width="400px">


## 使用技術
* python 3.6.0
* Anaconda 4.0
* Paas：heroku
* lib：scikit-learn,pandas,tweepy..etc
* Twitter API
* Google finance API

