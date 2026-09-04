# 매일 자동 발행용 프롬프트

데스크톱 앱의 **예약 작업 만들기** 창에 아래 내용을 그대로 붙여넣는다.
빈도는 **매일**, 시각은 **오전 9시(KST)**, 권한은 **자동 승인**, 폴더는 `클로드전용` 을 지정한다.

> 세션 안에서 만든 예약 작업은 컴퓨터에 바인딩되지 않아(클라우드 전용) 이 작업에는 쓸 수 없다.
> 클라우드 컨테이너는 github.com에 push 할 수 없기 때문에, 반드시 데스크톱 앱에서 직접 만들어야 한다.

---

"오늘 뭐보지" 블로그(https://kty1476-stack.github.io/watch-today/)에 오늘자 글 3편을 발행해줘.
GitHub 작업은 반드시 사용자 컴퓨터(device_bash)에서 해야 한다. 클라우드 컨테이너는 github.com에 push 할 수 없다.

## 1. 준비
- 토큰 파일: `$HOME/mnt/클로드전용/watch-today-token.txt`
- 저장소를 새로 clone 한다:
  `TOK=$(cat "$HOME/mnt/클로드전용/watch-today-token.txt"); rm -rf "$HOME/wt"; mkdir -p "$HOME/wt"; cd "$HOME/wt"; git clone -q "https://kty1476-stack:$TOK@github.com/kty1476-stack/watch-today.git"`
- `README.md`, `_data/categories.yml`, 그리고 `_posts/` 의 최근 글 목록을 먼저 읽어 형식과 **이미 다룬 소재**를 파악한다.

## 2. 소재 조사 (WebSearch / WebFetch — 클라우드 쪽 도구 사용)
오늘 발행할 3편을 아래 축에서 고른다. 이미 `_posts` 에 있는 작품은 같은 각도로 다시 쓰지 않는다.
- **드라마 리뷰** — 지금 방영 중인 한국 드라마의 최근 회차 (연재 중인 작품은 이어서 쓴다)
- **영화 평론** 또는 **OTT 신작** 중 1편
- 나머지 1편은 **이슈·시청률** 또는 **추천 리스트**

**절대 원칙**: 작품명, 방영일, 공개 일정, 출연진, 배역명, 시청률 수치는 공식 발표·보도자료에서
**최소 두 곳 이상 교차 확인**한 것만 쓴다. 확인이 안 되면 그 소재를 버리고 다른 소재로 간다.
3편을 못 채우면 억지로 채우지 말고 확인된 편수만 발행한다.

## 3. 글 작성
- 톤: **30년차 미디어 평론가**. 줄거리 요약이 아니라 판단을 쓴다. 좋게만 쓰지 않고, 아쉬운 점은 이유와 함께 적는다.
- 분량: 본문 1,200~2,000자. 소제목 3~4개.
- front matter 형식은 `README.md` 를 그대로 따른다. `categories` 는 `_data/categories.yml` 의 `name` 과 정확히 일치해야 한다.
- `date` 는 오늘 날짜의 09:00 / 09:30 / 10:00 (+0900).
- 파일명: `_posts/YYYY-MM-DD-영문슬러그.md` (영문·숫자·하이픈만)
- 결말 스포일러는 쓰지 않는다. 불가피하면 글 첫머리에 고지한다.
- 사실과 평가를 섞지 않는다.

## 4. 썸네일 (글마다 1장)
```
python3 tools/make_thumb.py --cat <slug> --badge "<카테고리 이름>" \
  --line1 "제목 앞줄" --line2 "제목 뒷줄" --sub "설명 한 줄" \
  --out assets/img/posts/thumb-<슬러그>.svg
```
`--cat` 은 `drama` `movie` `ott` `issue` `pick` 중 하나. line1/line2 는 각각 한글 12자 안쪽이 보기 좋다.

## 5. 커밋 · 푸시 · 확인
```
git add -A
git commit -m "2026-MM-DD 발행: <제목 3개 요약>"
git push origin main
```
푸시 후 40초쯤 기다렸다가 빌드 상태를 확인한다:
```
curl -s -H "Authorization: Bearer $TOK" \
  https://api.github.com/repos/kty1476-stack/watch-today/pages/builds/latest
```
`status` 가 `built` 가 아니면 `error.message` 를 보고 고친 뒤 다시 푸시한다.

## 6. 마무리
발행한 글의 제목과 URL을 알려준다. 건너뛴 소재가 있으면 그 이유도 한 줄로 적는다.
