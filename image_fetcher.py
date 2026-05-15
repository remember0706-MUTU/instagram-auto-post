# =============================================
# Pexels 이미지 자동 검색 및 다운로드 모듈
# =============================================

import requests
import os
import random
import json
from config import PEXELS_API_KEY

DOWNLOAD_DIR = "images"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
USED_PHOTOS_FILE = "used_photos.json"

def load_used_photos() -> set:
    if os.path.exists(USED_PHOTOS_FILE):
        with open(USED_PHOTOS_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_used_photo(photo_id: int):
    used = load_used_photos()
    used.add(photo_id)
    # 최근 200개만 유지
    used_list = list(used)[-200:]
    with open(USED_PHOTOS_FILE, "w") as f:
        json.dump(used_list, f)

def search_pexels_image(keyword: str, orientation: str = "portrait") -> dict:
    """
    Pexels에서 키워드로 이미지 검색
    orientation: portrait(세로), landscape(가로), square(정사각형)
    """
    headers = {"Authorization": PEXELS_API_KEY}

    # 한국어 키워드를 영어로 변환
    keyword_map = {
        "라이프스타일": "lifestyle",
        "건강": "healthy lifestyle",
        "웰빙": "wellness",
        "일상": "daily life",
        "월요일동기부여": "motivation monday",
        "한주시작": "monday motivation",
        "건강습관": "healthy habits",
        "건강식단": "healthy food diet",
        "운동루틴": "workout fitness routine",
        "미드위크": "midweek motivation",
        "웰빙라이프": "wellness lifestyle",
        "건강음식": "healthy food",
        "주말준비": "weekend lifestyle",
        "주말일상": "weekend lifestyle",
        "카페투어": "cafe coffee",
        "일요일": "sunday relaxation",
        "주말마무리": "weekend relaxation",
        "한주준비": "weekly planning",
        "화요일": "tuesday motivation",
        "수요일": "wellness wednesday",
        "목요일": "healthy thursday",
        "금요일": "friday lifestyle",
        "토요일": "saturday lifestyle",
        "힐링": "relaxation healing",
        "운동": "workout fitness",
        "식단": "healthy food",
        "카페": "cafe coffee",
        "자연": "nature",
        "명상": "meditation",
        "요가": "yoga",
        "아침루틴": "morning routine",
        "월요일동기부여": "motivation monday",
        "주말일상": "weekend lifestyle",
    }

    en_keyword = keyword_map.get(keyword, keyword)

    params = {
        "query": en_keyword,
        "orientation": orientation,
        "size": "large",
        "per_page": 80,
        "locale": "ko-KR"
    }

    try:
        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        data = response.json()

        photos = data.get("photos", [])
        if not photos:
            # 영어로 재시도
            params["query"] = "lifestyle healthy"
            response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
            data = response.json()
            photos = data.get("photos", [])

        # 사용한 사진 제외 후 랜덤 선택
        used = load_used_photos()
        fresh_photos = [p for p in photos if p["id"] not in used]
        if not fresh_photos:
            print(f"[이미지 검색] 새 사진 없음 - 기록 초기화 후 재선택")
            fresh_photos = photos  # 모두 사용했으면 초기화
        photo = random.choice(fresh_photos) if fresh_photos else None
        if photo:
            save_used_photo(photo["id"])
            print(f"[이미지 검색] 키워드: {keyword} → 이미지 찾음 (ID: {photo['id']})")
            return {
                "id": photo["id"],
                "url": photo["src"]["large2x"],
                "photographer": photo["photographer"],
                "alt": photo.get("alt", keyword)
            }
        else:
            print(f"[이미지 검색] 이미지를 찾지 못했습니다: {keyword}")
            return None

    except Exception as e:
        print(f"[이미지 검색 오류] {e}")
        return None


def download_image(image_info: dict, filename: str = None) -> str:
    """이미지 다운로드 후 로컬 경로 반환"""
    if not image_info:
        return None

    if not filename:
        filename = f"photo_{image_info['id']}.jpg"

    filepath = os.path.join(DOWNLOAD_DIR, filename)

    try:
        response = requests.get(image_info["url"], stream=True)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"[이미지 다운로드 완료] {filepath}")
        return os.path.abspath(filepath)

    except Exception as e:
        print(f"[이미지 다운로드 오류] {e}")
        return None


def get_image_for_keyword(keyword: str) -> str:
    """키워드로 이미지 검색 + 다운로드 한번에"""
    image_info = search_pexels_image(keyword)
    if image_info:
        filepath = download_image(image_info, f"{keyword}_{image_info['id']}.jpg")
        return filepath
    return None


if __name__ == "__main__":
    path = get_image_for_keyword("건강")
    print("저장 경로:", path)
