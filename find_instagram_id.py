"""
Instagram 비즈니스 계정 ID 자동 탐색 스크립트
"""
import requests
from config import INSTAGRAM_ACCESS_TOKEN

def find_instagram_account_id():
    print("Instagram 계정 ID 탐색 중...\n")

    # 방법 1: me/accounts (Facebook 페이지 통해서)
    url = f"https://graph.facebook.com/v19.0/me/accounts"
    params = {
        "fields": "id,name,instagram_business_account",
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    pages = data.get("data", [])

    if pages:
        print(f"Facebook 페이지 {len(pages)}개 발견!")
        for page in pages:
            ig = page.get("instagram_business_account", {})
            if ig:
                ig_id = ig.get("id")
                print(f"✅ Instagram 계정 ID 발견: {ig_id}")
                print(f"   페이지명: {page.get('name')}")
                update_config(ig_id)
                return ig_id
    else:
        print("Facebook 페이지 없음. 직접 Instagram API 시도...")

    # 방법 2: Instagram Basic Display API
    url2 = "https://graph.instagram.com/me"
    params2 = {
        "fields": "id,username",
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    resp2 = requests.get(url2, params=params2)
    data2 = resp2.json()

    if "id" in data2:
        ig_id = data2["id"]
        print(f"✅ Instagram 계정 ID 발견: {ig_id}")
        print(f"   사용자명: {data2.get('username', '')}")
        update_config(ig_id)
        return ig_id
    else:
        print(f"Instagram API 응답: {data2}")

    # 방법 3: Facebook User ID로 직접 조회
    url3 = "https://graph.facebook.com/v19.0/me"
    params3 = {
        "fields": "id,name",
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    resp3 = requests.get(url3, params=params3)
    data3 = resp3.json()
    fb_id = data3.get("id")
    print(f"\nFacebook User ID: {fb_id}")
    print(f"이름: {data3.get('name')}")

    print("\n⚠️  Instagram 계정 ID를 자동으로 찾지 못했어요.")
    print("Instagram 앱 → 설정 → 계정 → 링크드 계정에서 확인해주세요.")
    return None

def update_config(ig_id):
    """config.py의 INSTAGRAM_ACCOUNT_ID 자동 업데이트"""
    with open("config.py", "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace(
        'INSTAGRAM_ACCOUNT_ID = ""     # 아래 스크립트로 자동 탐색 가능',
        f'INSTAGRAM_ACCOUNT_ID = "{ig_id}"  # 자동 탐색됨'
    )
    with open("config.py", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n✅ config.py에 Instagram 계정 ID 저장 완료: {ig_id}")

if __name__ == "__main__":
    find_instagram_account_id()
