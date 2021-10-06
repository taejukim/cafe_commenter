from commenter import CafeCommenter

if __name__ == '__main__':
    commenter = CafeCommenter()
    fisrt_article = commenter.get_first_article()
    input('시작 하시려면 엔터키를 입력해주세요....')
    while True:
        if commenter.search_target_article(fisrt_article):
            input("엔터키를 입력하면 종료됩니다.")
            break