![git에 시크릿키 노출](https://github.com/user-attachments/assets/3f2088fb-d166-4083-b3d8-3ebf8caf5f7f)<img src="https://capsule-render.vercel.app/api?type=waving&color=auto&height=200&section=header&text=spartamarket_DRF&fontSize=90" />

<div align=center>
	<h3>📚 Tech Stack 📚</h3>
</div>
<div align="center">
	<img src="https://img.shields.io/badge/django-092E20?style=flat&logo=django&logoColor=white" />
	<img src="https://img.shields.io/badge/sqlite-003B57?style=plastic&logo=sqlite&logoColor=white" />
	<img src="https://img.shields.io/badge/python-3776AB?style=flat&logo=python&logoColor=white" />
	<img src="https://img.shields.io/badge/pycharm-000000?style=flat&logo=pycharm&logoColor=white" />
	<img src="https://img.shields.io/badge/github-181717?style=flat&logo=github&logoColor=white" />
	<img src="https://img.shields.io/badge/google-4285F4?style=flat&logo=google&logoColor=white" />
</div>



# ERD
![ERD](static/image/ERD.png)

# 프로젝트 소개
스파르타 뉴스 API 서버를 DRF로 구현

# 쉽죠? 팀과제
김동용(팀장),정성원(서기), 김나현(멤버), 임선오(멤버)


# 프로젝트 주요기능

accounts

- 회원가입
- 로그인(RefreshToken 발급)
- 회원 프로필 조회
- 회원 정보 수정
- 로그아웃(TokenBlacklist 추가)
- 회원탈퇴


articles

- 뉴스 목록 조회(메인페이지)

- 뉴스 작성
- 뉴스 상세페이지 조회
- 뉴스 수정
- 뉴스 삭제

- 댓글 작성
- 댓글 조회
- 댓글 수정
- 댓글 삭제

- 뉴스 좋아요
- 댓글 좋아요

- 뉴스 url 입력시 뉴스 내용 요약하는 ai 기능
- 네이버 야구 뉴스 크롤링 후 뉴스 목록 제공(클릭시 본문 이동)
- 뉴스목록 크롤링 후 목록 제공 (클릭시 기사내용 요약 제공)


- 회원이 작성한 뉴스 조회
- 회원이 좋아요한 뉴스 조회
- 회원이 좋아요한 댓글 조회


# 트러블 슈팅

- git repositories 작성 후 최초 push 할때 소통문제로 인해 SECRET_KEY가 들어있는 파일도 함께 git에 올라감 
    ![git에 시크릿키 노출](https://github.com/user-attachments/assets/43cadd42-9452-4c2c-b0ca-abac60684320)
    - 해결: repositories를 제거 후 다시 시작
