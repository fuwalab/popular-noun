from typing import List
from joblib import Parallel, delayed
from lib.request import Request


class Naver:
    """
    Naverまとめからコンテンツを取得する
    """
    BASE_URL = 'https://matome.naver.jp'

    def get_link(self) -> List:
        return self.__get_link()

    """リンクを取得する"""
    def __get_link(self) -> List:
        links = []
        nav_list = self.__get_category_list()
        max_page_num = 50
        current_page = 1

        results = Parallel(n_jobs=5, backend='threading', verbose=0)([
            delayed(self.__get_link_in_category)(current_page, path, max_page_num) for path in nav_list
        ])

        """メモリ解放"""
        del nav_list

        for link in results:
            links.extend(link)

        """メモリ解放"""
        del results

        return list(set(links))

    """カテゴリーリストを取得する"""
    def __get_category_list(self) -> List:
        """一旦カテゴリーリストを取得する"""
        nav_list = []
        soup = Request.exec(self.BASE_URL)
        li_tags = soup.find_all('li')

        """カテゴリーだけ取得する"""
        for li in li_tags:
            li_class_array = li.get('class')
            if li_class_array and 'mdTopNav01Item' in li_class_array:
                nav = li.find_all('a')[0]
                nav_link = nav.get('href')
                nav_list.append(self.BASE_URL + nav_link)

        return nav_list

    """カテゴリーごとのリンクを取得する"""
    def __get_link_in_category(self, current_page: int, path: str, max_page_num: int = 50) -> List:
        links = []
        page_list = []  # type: List[int]

        while current_page <= max_page_num:
            request_path = path + '?page=' + str(current_page)
            soup = Request.exec(request_path)
            a_tags = soup.find_all("a")

            """トップページにある有効なリンクを配列に詰める"""
            for a in a_tags:
                href = a.get("href")
                text = a.get_text(strip=True)

                """
                - /odai/ で始まるリンク
                - a タグ内が空でない
                - /odai/new 以外
                """
                if '/odai/' in href and text and href != '/odai/new':
                    links.append(self.BASE_URL + href)

                """ページ数を取得する"""
                if len(page_list) == 0 and href == '#' and 'goPage' in a.get('onclick'):
                    page_list.append(int(text))

            if len(page_list) == 0:
                max_page_num = max(page_list)

            current_page += 1

        return links

    @staticmethod
    def get_detail_list(link: str, callback) -> None:
        detail_list = []
        """url ごとにテキストを詰める"""
        text_array = []
        detail = {}

        max_page_num = 10
        current_page = 1

        while current_page <= max_page_num:
            request_path = link + '?page=' + str(current_page)

            html = Request.exec(request_path)
            contents = html.select(
                '.mdMTMWidget01ItemTweet01View,.mdMTMWidget01Content01Txt,'
                '.mdMTMWidget01ItemQuote01Txt,.mdMTMWidget01ItemComment01View,'
                '.mdMTMWidget01ItemDesc01View'
            )

            for content in contents:
                text = content.get_text(strip=True)
                if text:
                    text_array.append(text)

            page_element = html.select('.MdPagination03 a')
            page_list = []

            if len(page_list) == 0:
                for page in page_element:
                    page_list.append(int(page.string))

                max_page_num = max(page_list) if page_list else 1

            current_page += 1

        detail['link'] = link
        detail['content'] = text_array
        detail_list.append(detail)

        callback(detail_list)
