#!/usr/bin/env python
from scraping import Scraping
from datetime import datetime
from lib.analyze import Analyze
from joblib import Parallel, delayed


def main():
    providers = [
        'naver',
    ]

    """スクレイピングした内容をテーブルに保存する"""
    Parallel(n_jobs=1, verbose=0)([
        delayed(Scraping.run)(Scraping(), provider) for provider in providers
    ])

    """スクレイピング結果から名詞をテーブルに保存する"""
    Analyze.save_words(Analyze())


if __name__ == '__main__':
    print('start: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    main()
    print('end: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
