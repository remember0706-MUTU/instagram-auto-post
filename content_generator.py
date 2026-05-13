# =============================================
# Claude API - 인스타그램 콘텐츠 생성 모듈
# =============================================

import anthropic
from config import CLAUDE_API_KEY

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

def generate_instagram_content(keyword: str, category: str = "라이프스타일") -> dict:
    """
    키워드 기반으로 인스타그램 캡션 + 해시태그 생성
    """
    prompt = f"""당신은 인스타그램 콘텐츠 전문가입니다.
아래 키워드를 기반으로 인스타그램 게시물을 작성해주세요.

키워드: {keyword}
카테고리: {category}

다음 형식으로 작성해주세요:

[캡션]
- 감성적이고 공감가는 한국어 문장 3~5줄
- 이모지 2~3개 포함
- 마지막에 질문이나 공감 유도 문장 포함

[해시태그]
- 관련 해시태그 20~25개
- 인기 해시태그와 틈새 해시태그 혼합
- 한국어 해시태그 위주, 영어 2~3개 포함

JSON 형식으로 반환:
{{
  "caption": "캡션 내용",
  "hashtags": "#해시태그1 #해시태그2 ...",
  "keyword": "{keyword}"
}}"""

    try:
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        import re
        text = message.content[0].text
        # JSON 추출
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            print(f"[콘텐츠 생성 완료] 키워드: {keyword}")
            return result
        else:
            raise ValueError("JSON 파싱 실패")

    except Exception as e:
        print(f"[콘텐츠 생성 오류] {e}")
        # 기본 콘텐츠 반환
        return {
            "caption": f"오늘도 건강하고 행복한 하루 보내세요 ✨\n{keyword}으로 가득한 하루!\n여러분의 오늘은 어떤가요?",
            "hashtags": f"#{keyword} #라이프스타일 #건강 #일상 #힐링 #웰빙 #오늘 #daily #lifestyle #health",
            "keyword": keyword
        }


def generate_multiple_contents(keywords: list, category: str = "라이프스타일") -> list:
    """여러 키워드에 대한 콘텐츠 생성"""
    contents = []
    for keyword in keywords[:2]:  # 하루 2개
        content = generate_instagram_content(keyword, category)
        contents.append(content)
    return contents


if __name__ == "__main__":
    result = generate_instagram_content("건강한 아침루틴", "건강")
    print("캡션:", result["caption"])
    print("해시태그:", result["hashtags"])
