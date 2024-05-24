class Account:
    connected = 0 #로그인 여부
    name = "" #로그인한 계정 이름
    tag = "" #로그인한 계정 태그
    platform = "NULL" #로그인한 플랫폼
    token = "" #로그인한 토큰

class Content:
    name = "" #컨텐츠를 개시한 유저의 이름 
    platform = "" #컨텐츠를 개시한 유저의 플랫폼
    title = "" #컨텐츠 개시 제목
    text = "" #컨텐츠 내용
    icon = "" #컨텐츠 개시자의 아이콘
    image = "" #컨탠스 내 이미지

class Chat:
    platform = "" #채팅을 요청한 플랫폼
    id = "" #채팅을 요청한 유저의 아이디
    name = "" #채팅을 요청한 유저의 이름
    tag = "" #채팅을 요청한 유저의 태그
    data = [
        {"user": "",
         "text": "",
         "time": ""},

    ] #채팅 내용 (리버스 필요)

