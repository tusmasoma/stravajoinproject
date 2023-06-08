# stravajoinproject
## 注意点
ユーザーのStravaのアカウント情報をサイト内で用いるため、フィッシング詐欺と思われてしまうことを恐れ、現在サイトは閉鎖しております。

## 開発動機
Stravaというアプリで、複数のアクティビティを一つのアクティビティに結合したい場合がありますが、残念ながらStravaはそのようなサービスを提供していません。インターネット上には、アクティビティを結合する方法がたくさん紹介されていますが、これらはアクティビティの生のgpxコードを取得して編集する必要があり、非常に手間がかかります。

そこで、私は結合したいアクティビティを選択するだけで簡単に結合できるサービスを作成しました。

## サイトの使い方
### ①stravaのアカウントでloginします
![login画面](S__91938818.jpg)
### ②login情報をもとにStravaからアクティビティの情報を取得してきます

- アクティビティを二つ以上選択しないと結合ボタンは押せないようにしてあります
- 選択したアクティビティのファイルの合計サイズが25MB以上の場合、結合ボタンは押せないようにしてあります[^1].

[^1]:Stravaでは25MB以上のファイルをアップロードできないため

![アクティビティの選択画面](S__91938821.jpg)

### ③結合したアクティビティをStravaにアップロード

- Stravaへのアップロードは手動で行います。なぜ自動化しないかというと、Stravaでは、同時期のアクティビティを持てないため、結合前のデータは削除しなくてはいけません。そのため、削除するかどうかはユーザーに任せることにしています。

![結合後の画面](S__91938822.jpg)


## 制作環境（サーバー環境や使用ツール）と使用言語
- フロントエンド言語 (HTML,CSS,JavaScript)
- バックエンド言語 (Python)
- フレームワーク (Django)
- データベース (PostgreSQL)
- webサーバー (Nginx)
- クラウドサービス (AWS)

## なぜPythonなのか？
Stravaからアクティビティデータをスクレイピングする必要があるため、Pythonのようにウェブスクレイピングに役立つ豊富なライブラリやモジュールがある言語を使用することにしました。

## 工夫点
- 20MB前後のファイル処理を行う際に、なるべくメモリの消費を抑えるために、readメソッドで一気にファイルを読み込むのではなく、以下のように1024byteづつ読み込むようにしました。
```
 with open(filename,"w+", encoding="utf-8") as f:

                gpxfile=self.session.get(self.data.gpx_url,stream=True)

                metadata_bool=False
                for chunk in gpxfile.iter_content(chunk_size=1024,decode_unicode=True):
                    chunk=chunk.decode('utf-8')
                    if chunk:
                        if '<metadata>' in chunk:
                            metadata_bool=True
                        if metadata_bool and '<time>' in chunk:
                            timedata=re.search(r'<metadata>\s*<time>(.*)</time>\s*</metadata>',chunk).group(1)
                            metadata_bool=False
                        
                        f.write(chunk)
                gpxurl_obj.save() #gpxurlだけ保存され、gpxfileが保存されない場合があるので、保存のタイミングを同じにする
                GpxFile.objects.create(url=gpxurl_obj,file=File(f),time=timedata)
```
