# =============================================
# Pexels 이미지 자동 검색 모듈 (인생조언/명언 테마)
# =============================================

import requests
import os
import random
import json
from config import PEXELS_API_KEY

DOWNLOAD_DIR = "images"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
USED_PHOTOS_FILE = "used_photos.json"

# 카테고리/키워드별 Pexels 검색어 매핑
keyword_map = {
    # 카테고리 기본 매핑
    "명언":     "inspirational quote minimal background",
    "깨달음":   "contemplation solitude person thinking",
    "동기부여": "motivation sunrise running energy",
    "인생조언": "life journey path road wisdom",

    # 세부 테마 매핑
    "시간의 소중함":          "clock time hourglass",
    "노력과 성장":             "growth plant sunrise",
    "자신을 믿는 것":          "confident person standing",
    "작은 것에 감사하기":      "peaceful morning coffee",
    "포기하지 않는 마음":      "person climbing mountain",
    "진심의 힘":               "hands heart warmth",
    "꾸준함의 기적":           "consistent effort road",

    "지나고 나서야 보이는 것들": "rearview mirror nostalgia",
    "그때 왜 그랬을까":         "person sitting alone reflection",
    "중요한 건 지금 이 순간":   "present moment mindfulness",
    "사람 관계에서 배운 것":    "people connection friendship",
    "돈보다 소중한 것":         "family love nature peaceful",
    "건강을 잃고 나서야":       "health nature fresh air",
    "나이 들며 알게 된 것":     "older person wisdom nature",

    "오늘 포기하고 싶을 때":    "person perseverance struggle",
    "힘든 날을 버티는 법":      "rainy day window cozy",
    "작은 한 걸음의 힘":        "footstep path forward",
    "비교하지 말고 나만의 속도로": "solo journey own pace",
    "실패해도 괜찮은 이유":     "falling rising phoenix",
    "지금 시작해도 늦지 않다":  "new beginning sunrise fresh",
    "나를 응원하는 연습":       "self care morning routine",

    "20대에 꼭 해야 할 것들":   "young adult adventure explore",
    "30대가 후회하는 것들":     "thoughtful person looking back",
    "곁에 있을 때 잘해야 하는 이유": "family together warm light",
    "돈 관리, 젊을 때 시작해야 하는 이유": "saving planning future",
    "진짜 친구를 알아보는 법":  "true friendship connection",
    "자존감을 지키는 방법":     "self confidence mirror",
    "인간관계를 정리해야 할 때": "minimalist alone peaceful",
}

DEFAULT_QUERIES = [
    "minimalist peaceful nature",
    "morning light calm",
    "sunset reflection",
    "person alone thinking nature",
    "path road forest",
]


def load_used_photos() -> set:
    if os.path.exists(USED_PHOTOS_FILE):
        with open(USED_PHOTOS_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_used_photo(photo_id: int):
    used = load_used_photos()
    used.add(photo_id)
    used_list = list(used)[-200:]
    with open(USED_PHOTOS_FILE, "w") as f:
        json.dump(used_list, f)


def search_pexels_image(keyword: str, orientation: str = "portrait") -> dict:
    """
    Pexels에서 키워드로 이미지 검색
    명언/인생조언 테마에 맞는 감성적 이미지 우선 검색
    """
    headers = {"Authorization": PEXELS_API_KEY}

    en_query = keyword_map.get(keyword, None)
    if not en_query:
        en_query = random.choice(DEFAULT_QUERIES)

    params = {
        "query": en_query,
        "orientation": orientation,
        "size": "large",
        "per_page": 80,
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
            params["query"] = random.choice(DEFAULT_QUERIES)
            response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
            data = response.json()
            photos = data.get("photos", [])

        used = load_used_photos()
        fresh_photos = [p for p in photos if p["id"] not in used]
        if not fresh_photos:
            fresh_photos = photos

        photo = random.choice(fresh_photos) if fresh_photos else None
        if photo:
            save_used_photo(photo["id"])
            print(f"[이미지 검색] '{keyword}' → '{en_query}' (ID: {photo['id']})")
            return {
                "id": photo["id"],
                "url": photo["src"]["large2x"],
                "photographer": photo["photographer"],
                "alt": photo.get("alt", keyword)
            }
        else:
            print(f"[이미지 검색 실패] {keyword}")
            return None

    except Exception as e:
        print(f"[이미지 검색 오류] {e}")
        return None


def download_image(image_info: dict, filename: str = None) -> str:
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


if __name__ == "__main__":
    for kw in ["명언", "깨달음", "동기부여", "인생조언"]:
        result = search_pexels_image(kw)
        if result:
            print(f"{kw} → {result['url'][:60]}...")
