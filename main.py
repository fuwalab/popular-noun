#!/usr/bin/env python
from scraping import Scraping
from datetime import datetime
from analyze import Analyze


def main():
    enable_providers = [
        'naver',
    ]

    """スクレイピングした内容をテーブルに保存する"""
    for provider in enable_providers:
        Scraping.run(Scraping(), provider)

    """スクレイピング結果から名詞をテーブルに保存する"""
    Analyze.save_words(Analyze())


if __name__ == '__main__':
    print('start: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    main()
    print('end: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
