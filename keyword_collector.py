# =============================================
# 인생조언/명언 테마 키워드 모듈
# =============================================

import requests
import json
from datetime import datetime, timedelta
import os

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "")

# 카테고리별 주제 키워드 (네이버 검색 트렌드용)
keyword_map = {
    "명언": ["명언", "좋은글", "인생명언", "오늘의명언", "짧은명언"],
    "깨달음": ["후회", "깨달음", "인생교훈", "살면서배운것", "삶의진리"],
    "동기부여": ["동기부여", "파이팅", "오늘도화이팅", "자기계발", "긍정에너지"],
    "인생조언": ["인생조언", "20대조언", "30대조언", "어른이되면", "살면서느낀것"],
}

# 카테고리별 일별 테마 (fallback용)
daily_themes = {
    "명언": [
        "시간의 소중함",
        "노력과 성장",
        "자신을 믿는 것",
        "작은 것에 감사하기",
        "포기하지 않는 마음",
        "진심의 힘",
        "꾸준함의 기적",
    ],
    "깨달음": [
        "지나고 나서야 보이는 것들",
        "그때 왜 그랬을까",
        "중요한 건 지금 이 순간",
        "사람 관계에서 배운 것",
        "돈보다 소중한 것",
        "건강을 잃고 나서야",
        "나이 들며 알게 된 것",
    ],
    "동기부여": [
        "오늘 포기하고 싶을 때",
        "힘든 날을 버티는 법",
        "작은 한 걸음의 힘",
        "비교하지 말고 나만의 속도로",
        "실패해도 괜찮은 이유",
        "지금 시작해도 늦지 않다",
        "나를 응원하는 연습",
    ],
    "인생조언": [
        "20대에 꼭 해야 할 것들",
        "30대가 후회하는 것들",
        "곁에 있을 때 잘해야 하는 이유",
        "돈 관리, 젊을 때 시작해야 하는 이유",
        "진짜 친구를 알아보는 법",
        "자존감을 지키는 방법",
        "인간관계를 정리해야 할 때",
    ],
}

CATEGORIES = list(keyword_map.keys())


def get_trending_keywords(category="명언", top_n=5):
    """
    네이버 DataLab에서 카테고리 관련 키워드 트렌드 수집
    """
    today = datetime.now()
    start_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    keywords = keyword_map.get(category, keyword_map["명언"])

    url = "https://openapi.naver.com/v1/datalab/search"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
        "Content-Type": "application/json",
    }

    keyword_groups = [{"groupName": kw, "keywords": [kw]} for kw in keywords]

    body = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": "date",
        "keywordGroups": keyword_groups,
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(body))
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        keyword_scores = []
        for result in results:
            name = result["title"]
            recent_data = result["data"][-3:] if len(result["data"]) >= 3 else result["data"]
            avg_ratio = sum(d["ratio"] for d in recent_data) / len(recent_data)
            keyword_scores.append((name, avg_ratio))

        keyword_scores.sort(key=lambda x: x[1], reverse=True)
        top_keywords = [k[0] for k in keyword_scores[:top_n]]

        print(f"[키워드 수집] {category} TOP {top_n}: {top_keywords}")
        return top_keywords

    except Exception as e:
        print(f"[키워드 수집 오류] {e}")
        return get_fallback_keywords(category)


def get_fallback_keywords(category=None):
    """API 없을 때 요일별 테마 반환"""
    today = datetime.now()
    weekday = today.weekday()

    if category is None:
        cat_index = weekday % len(CATEGORIES)
        category = CATEGORIES[cat_index]

    themes = daily_themes.get(category, daily_themes["명언"])
    theme = themes[weekday % len(themes)]

    print(f"[Fallback] 카테고리: {category} / 오늘의 테마: {theme}")
    return [theme]


if __name__ == "__main__":
    for cat in CATEGORIES:
        print(f"\n[{cat}]")
        kw = get_fallback_keywords(cat)
        print("테마:", kw)
