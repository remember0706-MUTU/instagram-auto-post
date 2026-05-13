# =============================================
# Instagram Graph API - 자동 게시 모듈
# =============================================

import requests
import time
from config import INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_ACCOUNT_ID

GRAPH_API_BASE = "https://graph.instagram.com/v19.0"

def upload_image_to_instagram(image_url: str, caption: str) -> str:
    """
    1단계: 이미지 컨테이너 생성
    image_url: 공개 접근 가능한 이미지 URL (Pexels URL 직접 사용)
    """
    url = f"{GRAPH_API_BASE}/{INSTAGRAM_ACCOUNT_ID}/media"
    data = {
        "image_url": image_url,
        "caption": caption,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        data = response.json()
        container_id = data.get("id")
        print(f"[업로드] 컨테이너 생성 완료: {container_id}")
        return container_id
    except Exception as e:
        print(f"[업로드 오류] {e}")
        print(f"응답: {response.text if 'response' in locals() else 'N/A'}")
        return None


def publish_instagram_post(container_id: str) -> str:
    """
    2단계: 컨테이너를 실제 게시물로 발행
    """
    url = f"{GRAPH_API_BASE}/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    data = {
        "creation_id": container_id,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }

    try:
        # 컨테이너 처리 대기 (최대 30초)
        time.sleep(5)

        response = requests.post(url, data=data)
        response.raise_for_status()
        data = response.json()
        post_id = data.get("id")
        print(f"[발행 완료] 게시물 ID: {post_id}")
        return post_id
    except Exception as e:
        print(f"[발행 오류] {e}")
        return None


def post_to_instagram(image_url: str, caption: str, hashtags: str) -> bool:
    """
    인스타그램에 이미지 + 캡션 + 해시태그 게시
    """
    if not INSTAGRAM_ACCESS_TOKEN or not INSTAGRAM_ACCOUNT_ID:
        print("[오류] Access Token 또는 Account ID가 설정되지 않았습니다.")
        print("config.py에서 INSTAGRAM_ACCESS_TOKEN과 INSTAGRAM_ACCOUNT_ID를 설정해주세요.")
        return False

    # 캡션 + 해시태그 합치기
    full_caption = f"{caption}\n\n{hashtags}"

    print(f"[게시 시작] 이미지: {image_url[:50]}...")
    print(f"[캡션 미리보기] {full_caption[:100]}...")

    # 1단계: 컨테이너 생성
    container_id = upload_image_to_instagram(image_url, full_caption)
    if not container_id:
        return False

    # 2단계: 발행
    post_id = publish_instagram_post(container_id)
    if post_id:
        print(f"[성공] 인스타그램 게시 완료!")
        return True
    return False


def check_api_connection() -> bool:
    """API 연결 상태 확인"""
    if not INSTAGRAM_ACCESS_TOKEN:
        print("[확인] Access Token이 없습니다. config.py를 설정해주세요.")
        return False

    url = f"{GRAPH_API_BASE}/{INSTAGRAM_ACCOUNT_ID}"
    params = {
        "fields": "id,username,account_type",
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if "username" in data:
            print(f"[연결 확인] 계정: @{data['username']} ({data.get('account_type', '')})")
            return True
        else:
            print(f"[연결 실패] {data}")
            return False
    except Exception as e:
        print(f"[연결 오류] {e}")
        return False


if __name__ == "__main__":
    check_api_connection()
