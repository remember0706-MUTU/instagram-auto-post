# =============================================
# Claude API - 인스타그램 콘텐츠 생성 모듈
# =============================================

import anthropic
import json
import re
from config import CLAUDE_API_KEY

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

CATEGORY_STYLE = {
    "명언": {
        "tone": "짧고 강렬한 한 줄 명언 스타일. 읽자마자 저장하고 싶은 문장.",
        "structure": "핵심 명언 1~2줄 → 짧은 공감 문장 2~3줄 → 질문 또는 공감 유도",
    },
    "깨달음": {
        "tone": "살면서 뒤늦게 깨달은 듯한, 솔직하고 담담한 어조.",
        "structure": "후회 또는 깨달음 상황 묘사 → 그때와 지금의 대비 → 독자에게 전하는 말",
    },
    "동기부여": {
        "tone": "지친 사람의 등을 토닥여주는 따뜻하고 진심 어린 어조.",
        "structure": "공감 → 위로 또는 응원 메시지 → 오늘 하루를 버티게 하는 한 마디",
    },
    "인생조언": {
        "tone": "경험에서 우러나온 진솔한 조언. 꼰대 느낌 없이 친구처럼.",
        "structure": "핵심 조언 제시 → 이유 또는 경험담 → 독자에게 적용 권유",
    },
}

HASHTAG_MAP = {
    "명언": "#명언 #오늘의명언 #좋은글 #인생명언 #짧은명언 #감성글 #공감 #글스타그램 #감성스타그램 #마음에새기는말 #인생글 #오늘의글 #좋은말 #힐링글 #마음글 #생각하게만드는글 #삶 #위로 #공감글 #감동 #quote #inspiration #mindset #wisdom #lifeadvice",
    "깨달음": "#깨달음 #후회 #인생교훈 #살면서배운것 #삶의진리 #공감 #좋은글 #감성글 #인생글 #나이들며 #어른이되면 #솔직한이야기 #현실공감 #마음글 #위로 #인생 #삶 #생각 #reflection #lifeLesson #growth #wisdom #selfgrowth #realtalk",
    "동기부여": "#동기부여 #파이팅 #오늘도화이팅 #긍정에너지 #자기계발 #응원 #위로 #힘내 #오늘하루 #버텨내기 #포기하지마 #천천히가도괜찮아 #나를믿어 #오늘도수고했어 #긍정적인생각 #성장 #motivation #inspiration #keepgoing #selfcare #youcanDoit #positivevibes #dailymotivation #growth",
    "인생조언": "#인생조언 #20대조언 #30대조언 #살면서느낀것 #진짜중요한것 #좋은글 #공감 #인생 #어른의말 #진심조언 #자존감 #관계 #인간관계 #돈관리 #건강 #후회없는삶 #현명한삶 #lifeadvice #adulting #selfimprovement #mindset #growthmindset #lifetips #wisdom",
}


def generate_instagram_content(keyword: str, category: str = "명언") -> dict:
    """
    키워드/테마 기반으로 인스타그램 캡션 + 해시태그 생성
    """
    style = CATEGORY_STYLE.get(category, CATEGORY_STYLE["명언"])

    prompt = f"""당신은 인스타그램에서 인생조언과 감성 명언으로 큰 반향을 얻는 콘텐츠 크리에이터입니다.

오늘의 주제: {keyword}
카테고리: {category}
글쓰기 톤: {style["tone"]}
구성 방식: {style["structure"]}

다음 조건을 지켜 인스타그램 캡션을 작성해주세요:
- 한국어로 작성, 총 5~8줄
- 이모지 2~3개 자연스럽게 포함
- 읽는 사람이 "이거 내 얘기다" 느낄 만큼 공감 가능하게
- 마지막 줄은 저장하거나 공유하고 싶게 만드는 한 문장
- 광고나 홍보 느낌 없이, 진심 어린 글처럼
- "👉 프로필 링크 참고" 문구 마지막에 추가

반드시 아래 JSON 형식으로만 반환 (다른 텍스트 없이):
{{
  "caption": "캡션 전체 내용",
  "keyword": "{keyword}"
}}"""

    try:
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        text = message.content[0].text
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            result["hashtags"] = HASHTAG_MAP.get(category, HASHTAG_MAP["명언"])
            print(f"[콘텐츠 생성 완료] 카테고리: {category} / 키워드: {keyword}")
            return result
        else:
            raise ValueError("JSON 파싱 실패")

    except Exception as e:
        print(f"[콘텐츠 생성 오류] {e}")
        return {
            "caption": f"지나고 나서야 보이는 것들이 있습니다 ✨\n{keyword}\n그때는 몰랐지만, 지금은 압니다.\n천천히 가도 괜찮아요. 당신은 잘 하고 있습니다.\n\n👉 프로필 링크 참고",
            "hashtags": HASHTAG_MAP.get(category, HASHTAG_MAP["명언"]),
            "keyword": keyword
        }


if __name__ == "__main__":
    for cat in ["명언", "깨달음", "동기부여", "인생조언"]:
        print(f"\n===[ {cat} ]===")
        result = generate_instagram_content(f"테스트 테마", cat)
        print("캡션:", result["caption"])
        print("해시태그:", result["hashtags"][:50], "...")
