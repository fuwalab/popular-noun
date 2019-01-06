# -*- coding: utf-8 -*-
import MeCab
from database import DB
from datetime import datetime
from typing import List
import collections


class Analyze:
    """
    形態素解析して名詞を保存する
    """

    """名詞を保存する"""
    def save_words(self):
        print('start save_words...')
        conn = DB.conn()

        """今日スクレイピングしたデータのみが対象"""
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

        del rows
        print('done save_words')

    @staticmethod
    def __analyze(text: str) -> List:
        """
        形態素解析して名詞のリストを返す
        :param text: テキスト
        :return: 名詞のリスト
        """

        """
        mecab の辞書に以下を使う
        https://github.com/neologd/mecab-ipadic-neologd/blob/master/README.ja.md
        """
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

    @staticmethod
    def __save(keywords: List):
        """
        保存する
        :param keywords: 名詞のリスト
        """
        keyword_list = []

        """
        キーに要素、値に重複数をもつ辞書型サブクラスを返す
        Counter({'名詞1': 10, '名詞2': 5, '名詞3': 1})
        """
        words = collections.Counter(keywords)
        current_date = datetime.today().strftime('%Y-%m-%d')

        for word in words:
            keyword_list.append([word, words[word], current_date])

        conn = DB.conn()
        """同名の `name` があったときに数を加算していく"""
        query = 'INSERT INTO keywords (`name`, `num`, `create_date`) VALUES (%s, %s, %s) ' \
                'ON DUPLICATE KEY UPDATE `num` = `num` + VALUES(`num`)'

        cursor = conn.cursor()

        try:
            cursor.executemany(query, keyword_list)
            conn.commit()

            del keyword_list
            del words
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
