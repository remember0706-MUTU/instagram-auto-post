# =============================================
# 네이버 DataLab 핫키워드 수집 모듈
# =============================================

import requests
import json
from datetime import datetime, timedelta
import os

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "")

def get_trending_keywords(category="라이프스타일", top_n=5):
    """
    네이버 DataLab에서 오늘의 핫 키워드 수집
    카테고리: 라이프스타일, 건강, 뷰티 등
    """
    today = datetime.now()
    start_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    # 카테고리별 검색 키워드 매핑
    keyword_map = {
        "라이프스타일": ["라이프스타일", "일상", "데일리", "인테리어", "취미"],
        "건강": ["건강", "헬스", "운동", "다이어트", "웰빙", "영양"],
        "웰빙": ["웰빙", "마음챙김", "명상", "요가", "힐링"],
        "일상": ["일상", "데일리룩", "오늘뭐입지", "카페", "맛집"],
    }

    keywords = keyword_map.get(category, ["라이프스타일"])

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

        # 최근 트렌드 기준 정렬
        results = data.get("results", [])
        keyword_scores = []
        for result in results:
            name = result["title"]
            # 최근 3일 평균 ratio 계산
            recent_data = result["data"][-3:] if len(result["data"]) >= 3 else result["data"]
            avg_ratio = sum(d["ratio"] for d in recent_data) / len(recent_data)
            keyword_scores.append((name, avg_ratio))

        # 점수 높은 순 정렬
        keyword_scores.sort(key=lambda x: x[1], reverse=True)
        top_keywords = [k[0] for k in keyword_scores[:top_n]]

        print(f"[키워드 수집] 오늘의 TOP {top_n} 키워드: {top_keywords}")
        return top_keywords

    except Exception as e:
        print(f"[키워드 수집 오류] {e}")
        # 기본 키워드 반환
        return ["라이프스타일", "건강", "일상", "웰빙", "힐링"]


def get_fallback_keywords():
    """네이버 API 없을 때 사용할 기본 핫 키워드"""
    from datetime import datetime
    weekday = datetime.now().weekday()

    weekday_keywords = {
        0: ["월요일동기부여", "한주시작", "건강습관"],       # 월
        1: ["화요일", "건강식단", "운동루틴"],               # 화
        2: ["수요일", "미드위크", "힐링"],                   # 수
        3: ["목요일", "웰빙라이프", "건강음식"],             # 목
        4: ["금요일", "주말준비", "라이프스타일"],           # 금
        5: ["토요일", "주말일상", "카페투어"],               # 토
        6: ["일요일", "주말마무리", "한주준비"],             # 일
    }
    return weekday_keywords.get(weekday, ["라이프스타일", "건강", "웰빙"])


if __name__ == "__main__":
    keywords = get_trending_keywords()
    print("수집된 키워드:", keywords)
