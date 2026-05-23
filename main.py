# =============================================
# 인스타그램 자동 포스팅 시스템 - 메인 실행
# =============================================

import sys
import schedule
import time
import random
from datetime import datetime

# Windows 콘솔 UTF-8 출력 설정
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

from config import POST_TIMES
from keyword_collector import get_trending_keywords, get_fallback_keywords, CATEGORIES
from content_generator import generate_instagram_content
from image_fetcher import search_pexels_image
from instagram_poster import post_to_instagram, check_api_connection

_post_failed = False


def run_daily_post(category=None):
    """자동 포스팅 함수 - 카테고리 지정 가능"""
    print(f"\n{'='*50}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 자동 포스팅 시작")
    print(f"{'='*50}")

    # 1. API 연결 확인
    if not check_api_connection():
        print("[중단] Instagram API 연결 실패")
        sys.exit(1)

    # 2. 카테고리 설정 (요일별 순환)
    if category is None:
        day_index = datetime.now().weekday() % len(CATEGORIES)
        category = CATEGORIES[day_index]
    print(f"[오늘의 카테고리] {category}")

    # 3. 키워드/테마 수집
    try:
        keywords = get_trending_keywords(category=category, top_n=5)
    except Exception:
        keywords = get_fallback_keywords(category)

    print(f"[수집된 키워드] {keywords}")

    # 4. 키워드 1개 선택
    keyword = random.choice(keywords[:3]) if len(keywords) >= 3 else keywords[0]

    # 5. 콘텐츠 생성
    content = generate_instagram_content(keyword, category)
    if not content:
        print("[중단] 콘텐츠 생성 실패")
        sys.exit(1)

    # 6. 이미지 검색 (Pexels)
    image_info = search_pexels_image(keyword)
    if not image_info:
        # 카테고리 기본 이미지로 재시도
        image_info = search_pexels_image(category)
    if not image_info:
        print("[중단] 이미지 검색 실패")
        sys.exit(1)

    # 7. 인스타그램 게시
    success = post_to_instagram(
        image_url=image_info["url"],
        caption=content["caption"],
        hashtags=content["hashtags"]
    )

    if success:
        print(f"[완료] '{keyword}' 게시 성공!")
        log_post(keyword, content, image_info)
    else:
        print(f"[실패] 게시 실패 - 로그 확인하세요.")
        sys.exit(1)

    print(f"{'='*50}\n")


def log_post(keyword, content, image_info):
    """게시 로그 저장"""
    with open("post_log.txt", "a", encoding="utf-8") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"\n[{now}]\n")
        f.write(f"키워드: {keyword}\n")
        f.write(f"캡션: {content['caption'][:50]}...\n")
        f.write(f"이미지: {image_info['url']}\n")
        f.write("-" * 40 + "\n")


def setup_schedule():
    """스케줄 설정 - 시간대별 카테고리 순환"""
    for i, post_time in enumerate(POST_TIMES):
        category = CATEGORIES[i % len(CATEGORIES)]
        schedule.every().day.at(post_time).do(run_daily_post, category=category)
        print(f"[스케줄] 매일 {post_time}에 '{category}' 카테고리 게시 예약됨")


def main():
    print("인스타그램 자동 포스팅 시스템 시작!")
    print(f"카테고리: {CATEGORIES}")
    print(f"게시 시간: {POST_TIMES}")

    check_api_connection()
    setup_schedule()

    print("\n[대기 중] 예약된 시간에 자동으로 게시됩니다...")
    print("종료하려면 Ctrl+C를 누르세요.\n")

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("[테스트 모드] 지금 바로 포스팅 실행...")
        run_daily_post()
    else:
        main()
