# -*- coding: utf-8 -*-
import MeCab
from database import DB
from datetime import datetime
from typing import List


class Analyze:
    """ update_date が本日のものだけ保存する"""
    def save_words(self):
        print('start save_words...')
        conn = DB.conn()
        query = 'SELECT content FROM scraping WHERE `update_date` = %s'
        current_date = datetime.today().strftime('%Y-%m-%d')

        cursor = conn.cursor()
        cursor.execute(query, [current_date])

        rows = cursor.fetchall()

        for row in rows:
            keywords = self.__analyze(str(row[0]))
            self.__save(keywords)

        cursor.close()
        conn.close()
        print('done save_words')

    """形態素解析して名詞のリストを返す"""
    @staticmethod
    def __analyze(text: str) -> List:
        tagger = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        tagger.parse('')
        node = tagger.parseToNode(text)

        words = []

        while node:
            """名詞だけ抽出する"""
            if node.feature.split(',')[0] == '名詞':
                words.append(node.surface)
            node = node.next

        return words

    """保存する"""
    @staticmethod
    def __save(keywords: List):
        keyword_list = []

        for keyword in keywords:
            keyword_list.append([keyword])

        conn = DB.conn()
        query = 'INSERT INTO keywords (`name`) VALUES (%s)'

        cursor = conn.cursor()

        try:
            cursor.executemany(query, keyword_list)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
