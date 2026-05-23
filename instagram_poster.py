import requests
import time
import os

INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "")

GRAPH_API_BASE = "https://graph.instagram.com/v19.0"


def upload_image_to_instagram(image_url, caption):
    url = GRAPH_API_BASE + "/" + INSTAGRAM_ACCOUNT_ID + "/media"
    data = {
        "image_url": image_url,
        "caption": caption,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        container_id = response.json().get("id")
        print("[업로드] 컨테이너 생성 완료: " + str(container_id))
        return container_id
    except Exception as e:
        print("[업로드 오류] " + str(e))
        return None


def publish_instagram_post(container_id):
    url = GRAPH_API_BASE + "/" + INSTAGRAM_ACCOUNT_ID + "/media_publish"
    data = {
        "creation_id": container_id,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    try:
        time.sleep(5)
        response = requests.post(url, data=data)
        response.raise_for_status()
        post_id = response.json().get("id")
        print("[발행 완료] 게시물 ID: " + str(post_id))
        return post_id
    except Exception as e:
        print("[발행 오류] " + str(e))
        return None


def post_to_instagram(image_url, caption, hashtags):
    if not INSTAGRAM_ACCESS_TOKEN or not INSTAGRAM_ACCOUNT_ID:
        print("[오류] INSTAGRAM_ACCESS_TOKEN 또는 INSTAGRAM_ACCOUNT_ID 환경변수가 없습니다.")
        return False

    full_caption = caption + "\n\n" + hashtags
    print("[게시 시작] 이미지: " + image_url[:50] + "...")
    print("[캡션 미리보기] " + full_caption[:100] + "...")

    container_id = upload_image_to_instagram(image_url, full_caption)
    if not container_id:
        return False

    post_id = publish_instagram_post(container_id)
    if post_id:
        print("[성공] 인스타그램 게시 완료!")
        return True
    return False


def check_api_connection():
    if not INSTAGRAM_ACCESS_TOKEN:
        print("[확인] INSTAGRAM_ACCESS_TOKEN 환경변수가 없습니다.")
        return False

    url = GRAPH_API_BASE + "/" + INSTAGRAM_ACCOUNT_ID
    params = {
        "fields": "id,username,account_type",
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if "username" in data:
            print("[연결 확인] 계정: @" + data["username"] + " (" + data.get("account_type", "") + ")")
            return True
        else:
            print("[연결 실패] " + str(data))
            return False
    except Exception as e:
        print("[연결 오류] " + str(e))
        return False


if __name__ == "__main__":
    check_api_connection()