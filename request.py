from typing import Any
import urllib.request
from bs4 import BeautifulSoup
from time import sleep


class Request:
    """リクエストを投げる"""
    @staticmethod
    def exec(url: str) -> Any:
        print(url)

        """適当に UA を偽装する"""
        headers = {"User-Agent":  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        req = urllib.request.Request(url=url, headers=headers)
        html = urllib.request.urlopen(req)
        """リクエストしすぎないように一定時間待つ"""
        sleep(1)
        return BeautifulSoup(html, "html.parser")

