import sys
import os
import schedule
import time
import random
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

POST_TIMES = os.getenv("POST_TIMES", "08:00,20:00").split(",")

from keyword_collector import get_trending_keywords, get_fallback_keywords, CATEGORIES
from content_generator import generate_instagram_content
from image_fetcher import search_pexels_image
from instagram_poster import post_to_instagram, check_api_connection


def run_daily_post(category=None):
    print("\n" + "="*50)
    print("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] 자동 포스팅 시작")
    print("="*50)

    if not check_api_connection():
        print("[중단] Instagram API 연결 실패")
        sys.exit(1)

    if category is None:
        day_index = datetime.now().weekday() % len(CATEGORIES)
        category = CATEGORIES[day_index]
    print("[오늘의 카테고리] " + category)

    try:
        keywords = get_trending_keywords(category=category, top_n=5)
    except Exception:
        keywords = get_fallback_keywords(category)

    print("[수집된 키워드] " + str(keywords))
    keyword = random.choice(keywords[:3]) if len(keywords) >= 3 else keywords[0]

    content = generate_instagram_content(keyword, category)
    if not content:
        print("[중단] 콘텐츠 생성 실패")
        sys.exit(1)

    image_info = search_pexels_image(keyword)
    if not image_info:
        image_info = search_pexels_image(category)
    if not image_info:
        print("[중단] 이미지 검색 실패")
        sys.exit(1)

    success = post_to_instagram(
        image_url=image_info["url"],
        caption=content["caption"],
        hashtags=content["hashtags"]
    )

    if success:
        print("[완료] " + keyword + " 게시 성공!")
        log_post(keyword, content, image_info)
    else:
        print("[실패] 게시 실패")
        sys.exit(1)

    print("="*50 + "\n")


def log_post(keyword, content, image_info):
    with open("post_log.txt", "a", encoding="utf-8") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write("\n[" + now + "]\n")
        f.write("키워드: " + keyword + "\n")
        f.write("이미지: " + image_info["url"] + "\n")
        f.write("-"*40 + "\n")


def setup_schedule():
    for i, post_time in enumerate(POST_TIMES):
        category = CATEGORIES[i % len(CATEGORIES)]
        schedule.every().day.at(post_time.strip()).do(run_daily_post, category=category)
        print("[스케줄] 매일 " + post_time.strip() + "에 " + category + " 카테고리 게시 예약됨")


def main():
    print("인스타그램 자동 포스팅 시스템 시작!")
    print("카테고리: " + str(CATEGORIES))
    print("게시 시간: " + str(POST_TIMES))
    check_api_connection()
    setup_schedule()
    print("\n[대기 중] 예약된 시간에 자동으로 게시됩니다...")
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("[테스트 모드] 지금 바로 포스팅 실행...")
        run_daily_post()
    else:
        main()