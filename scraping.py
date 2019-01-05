from typing import List
from database import DB
from datetime import datetime
from lib.scraping.naver import Naver
from joblib import Parallel, delayed


class Scraping:
    """スクレイピング結果をテーブルに格納する"""

    """スクレイピングを開始"""
    def run(self, target: str):
        print('start scraping...')

        if target == 'naver':

            """コンテンツを取得して保存する"""
            link_list = Naver().get_link()
            self.__save_page_detail(link_list, Naver)

        print('done scraping')

    """詳細を取得する"""
    def __save_page_detail(self, links: List, provider) -> None:
        Parallel(n_jobs=5, backend='threading', verbose=0)([
            delayed(provider.get_detail_list)(link, self.save) for link in links
        ])

        """メモリ解放"""
        del links

    """保存する"""
    @staticmethod
    def save(detail_list: List):
        conn = DB.conn()
        query = 'INSERT INTO scraping (`url`, `content`, `create_date`, `update_date`) VALUES (%s, %s, %s, %s) ' \
                'ON DUPLICATE KEY UPDATE `content` = VALUES (`content`), `update_date` = VALUES (`update_date`)'
        values = []
        current_date = datetime.today().strftime('%Y-%m-%d')

        for detail in detail_list:
            value = [detail['link'], '\n'.join(detail['content']), current_date, current_date]
            values.append(value)

        cursor = conn.cursor()

        try:
            cursor.executemany(query, values)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
