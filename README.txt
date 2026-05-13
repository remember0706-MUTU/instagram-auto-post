=============================================
인스타그램 자동 포스팅 시스템 사용 방법
=============================================

[설치]
pip install -r requirements.txt

[설정 - config.py 열어서 아래 항목 입력]
1. INSTAGRAM_ACCESS_TOKEN  ← Meta Developer에서 발급
2. INSTAGRAM_ACCOUNT_ID    ← 인스타 비즈니스 계정 ID
3. CLAUDE_API_KEY          ← console.anthropic.com 에서 발급
(Pexels API 키는 이미 설정되어 있음)

[테스트 실행 - 지금 바로 1개 게시]
python main.py test

[정식 실행 - 매일 자동 게시]
python main.py

[게시 시간 변경]
config.py에서 POST_TIMES 수정
예) POST_TIMES = ["08:00", "20:00"]

[파일 구조]
- config.py          : API 키 및 설정
- main.py            : 메인 실행 파일
- keyword_collector.py : 네이버 DataLab 키워드 수집
- content_generator.py : Claude AI 콘텐츠 생성
- image_fetcher.py   : Pexels 이미지 검색/다운로드
- instagram_poster.py  : 인스타그램 게시
- post_log.txt       : 게시 기록 (자동 생성)
