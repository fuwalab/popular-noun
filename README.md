# popular-noun

## 概要
PIXTA や Adobe Stock などのストック系サイトで売れそうな素材のキーワードを抽出する


## 動作環境
```
Python version 3 以上
MySQL 5.7 以上
```

## 事前準備
- Mecab のインストール
    ```
    $ brew install macab
    ```
    
- swig のインストール
    ```
    $ brew install swig
    ```

- 必要パッケージのインストール
    ```
    $ pip install mysql-connector-python joblib beautifulsoup4 mecab-python3==0.7
    ```
    - ※最新版だと parseToNode に不具合があるため古いバージョンを指定

- mecab-ipadic-neologd のインストール
    ```
    $ git clone --depth 1 git@github.com:neologd/mecab-ipadic-neologd.git
    $ cd mecab-ipadic-neologd
    $ ./bin/install-mecab-ipadic-neologd -n
    ```
    - 詳細は[こちら](https://github.com/neologd/mecab-ipadic-neologd/blob/master/README.ja.md)

- マイグレーション
    ```
    $ echo 'create database scraping;' | mysql -uroot -p
    $ mysql -uroot -p < migrations.sql
    ```
    - [DDL](https://github.com/fuwalab/popular-noun/blob/master/migrations.sql)
## 実行方法
```
$ ./main.py
```

## データ
- スクレイピングデータ
    - `scraping.scraping`
- 形態素解析データ
    - `scraping.keywords`