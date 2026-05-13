# =============================================
# 인스타그램 자동 포스팅 시스템 - 설정 파일
# =============================================

import os

# Pexels API 키
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")

# Instagram Graph API
INSTAGRAM_ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "")
INSTAGRAM_ACCOUNT_ID = os.environ.get("INSTAGRAM_ACCOUNT_ID", "")

# 네이버 API (MCP 연동 사용 - 별도 키 불필요)

# Claude API 키
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY", "")

# 포스팅 설정
POST_COUNT_PER_DAY = 4        # 하루 게시 횟수
POST_TIMES = ["09:00", "13:00", "17:00", "21:00"]  # 게시 시간 (24시간 형식)

# 콘텐츠 카테고리
CATEGORIES = ["라이프스타일", "건강", "웰빙", "일상"]

# 이미지 설정
IMAGE_ORIENTATION = "portrait"  # portrait(세로), landscape(가로), square(정사각형)
IMAGE_SIZE = "large"
