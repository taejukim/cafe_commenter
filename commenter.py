import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime

from get_driver import get_driver

class CafeCommenter:

    def __init__(self):
        self.comment_flag = False
        self.driver = get_driver()
        
        login_url = 'https://nid.naver.com/nidlogin.login?mode=form'
        self.driver.get(login_url)
        input('네이버 로그인 후 엔터키를 입력해주세요....')

        # self.cafe_id = int(input('cafe id 를 입력해주세요 : '))
        self.cafe_id = 27549420
        # self.board_id = int(input('게시판 id 를 입력해주세요 : '))
        self.board_id = 103
        self.comment_msg = input('댓글 내용을 입력해주세요 : ')
        
        view_type = 'L'
        self.base_url = 'https://cafe.naver.com/ArticleList.nhn'
        self.base_url += '?search.clubid={}&search.menuid={}&search.boardtype={}'.format(self.cafe_id, self.board_id, view_type)
        self.cookies = self.get_cookies_for_requests(self.driver.get_cookies())

        self.driver.get(self.base_url)


    def get_cookies_for_requests(self, cookies):
        """
        Selenium으로 접속한 Browser cookie를 requests 모듈에 적용할 수 있도록 변환하여 반환
        :param cookies: 
        :return:
        """
        cookies_for_requests = dict()
        for cookie in cookies:
            key = cookie.get('name')
            value = cookie.get('value')
            cookies_for_requests[key]=value
        return cookies_for_requests

    def get_first_article(self):
        r = requests.get(
            self.base_url, 
            cookies = self.cookies,
            )
        soup = bs(r.text, 'html.parser')
        tbodys = soup.find_all('tbody')
        first_article_id = tbodys[1].find_all('div', {'class':'inner_number'})[0].text # ID
        return int(first_article_id)

    def search_target_article(self, target):
        first_article_id = self.get_first_article()
        print(datetime.now().strftime('[%y-%m-%d %H:%M:%S.%f]'),\
             '게시글 ID {} 보다 최신 게시글 찾고 있습니다...'.format(target))
        if int(target) < int(first_article_id):
            if self.comment_flag:
                return True
            self.write_comment(first_article_id)
            print(datetime.now().strftime('[%y-%m-%d %H:%M:%S.%f]'), '완료', first_article_id)
            return True

    def write_comment(self, article_id):
        self.enter_article(article_id)
        if self.comment_flag:
            return True
        self.comment_flag = True
        comment_post = 'https://apis.naver.com/cafe-web/cafe-mobile/CommentPost.json'
        comment_data = {
                'content':self.comment_msg,  'stickerId':'', 
                'cafeId':self.cafe_id, 
                'articleId':article_id, 
                'requestFrom':'A'
            }
        comment = requests.post(comment_post,
          cookies=(self.cookies),
          data=comment_data)
        print(datetime.now().strftime('[%y-%m-%d %H:%M:%S.%f]'), '댓글 작성 성공! ({})'.format(self.comment_msg))
        self.enter_article(article_id)
        return article_id

    def enter_article(self, article_id):
        url = 'https://cafe.naver.com/ArticleRead.nhn'
        url += '?clubid={}&page=1&boardtype=L&articleid={}&referrerAllArticles=false'\
        .format(self.cafe_id, article_id)
        self.driver.get(url)
