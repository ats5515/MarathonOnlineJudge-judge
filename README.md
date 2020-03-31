# MarathonOnlineJudge judge

Marathon Online Judge (https://judge.ats5515.net) のジャッジコード

ジャッジを実行するたびにAWS EC2のインスタンスを新たに作成し、その中でテストケース実行するな形式

## ローカルで動かす
TBD

## Amazon EC2上で動かす
Amazon EC2 のイメージ Amazon Linux2 上で動かす想定です。

あらかじめ'python3'コマンドが使えるようにして下さい。

以下では、デフォルトユーザ（ec2-user）を使ってホームディレクトリ直下にプロジェクトを展開するものとします。

#### clone
~~~
cd ~
git clone https://github.com/ats5515/MarathonOnlineJudge-judge.git .
~~~
#### 問題セットアップ
~~~
mkdir problems
git clone https://github.com/ats5515/MarathonOnlineJudge-problems.git ./problems
~~~
#### AWS接続情報の設定
~/.aws/credentialsに以下の形式で接続情報を書く
~~~
[default]
aws_access_key_id = xxxxxxxx
aws_secret_access_key = xxxxxxxx
region=xxxxxxxx(ap-northeast-1等)
~~~

judge/judge.py にハードコードされている情報を適宜書き換える。

#### 実行
テスト実行
~~~
python3 judge/judge.py example/EuclideanTSP_test
~~~

引数にはジャッジしたいソースファイルと言語・問題情報が書かれたjsonファイルが入ったディレクトリを指定。
~~~
python3 judge/judge.py path/to/submission
~~~

ソースコード名はmain.(拡張子)、info.jsonに言語と問題を設定。形式はexample/EuclideanTSP_testを参照してください。
