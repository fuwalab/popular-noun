import mysql.connector


class DB:
    @classmethod
    def conn(cls):
        """
        DB への接続情報は適宜変更してください
        """
        return mysql.connector.connect(
            user='root',
            password='',
            host='localhost',
            database='scraping',
        )
