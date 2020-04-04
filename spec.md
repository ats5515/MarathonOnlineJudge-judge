## s3
#### 提出　
各提出： s3://BUCKET/submissions/SUBMISSION_ID/
提出全体:　s3://BUCKET/submissions/submissions.json

#### ユーザー情報
s3://BUCKET/user/USER_ID
s3://BUCKET/user/USER_ID/u_result
s3://BUCKET/user/USER_ID/ranks.json
s3://BUCKET/user/user_ranking.json
#### 順位表のための情報
問題に対する順位表: s3://BUCKET/cache/PROBLEM_ID/standings.json
全提出result s3://BUCKET/cache/PROBLEM_ID/USER_ID/pu_result.json
ユーザごとの提出要約 s3://BUCKET/cache/PROBLEM_ID/USER_ID/best.json

## 提出登録手順

result.jsonを
s3://BUCKET/cache/PROBLEM_ID/USER_ID/pu_result.jsonへ追加
s3://BUCKET/user/USER_ID/u_resultへ追加

提出がACなら、
$ update_standings PROBLEM_ID USER_ID
提出から最も良いものを選びbest.jsonに保存
standings.json追加変更、ソートしなおし、順位を変更。
s3://BUCKET/user/USER_ID/ranks.jsonの更新
ファイル　basedir/user/update/USER_ID　を作成

$ update_ranking
basedir/user/update/*から更新が必要なユーザを見て、user/USER_ID/ranksにアクセス
userscoreの計算、user_ranking.jsonへ反映
すべて反映したらbasedir/user/update/*を削除しuser_ranking.jsonをソート