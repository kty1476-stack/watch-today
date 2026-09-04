# 오늘 뭐보지 (watch-today)

드라마·영화·OTT를 골라 소개하는 블로그. Jekyll + GitHub Pages.

- 사이트: https://kty1476-stack.github.io/watch-today/
- 빌드: GitHub Pages 기본 Jekyll 빌드 (별도 Actions 워크플로 없음)

## 구조

```
_config.yml              사이트 설정 (baseurl: /watch-today)
_data/categories.yml     카테고리 정의 — 이름·색·아이콘·설명. 여기만 고치면 전 페이지 반영
_includes/catmeta.html   카테고리 이름 → 색/슬러그/아이콘 변환
_includes/card.html      목록 카드 마크업 (홈·카테고리·관련글 공용)
_layouts/                default / post / page / category
categories/*.html        카테고리별 목록 페이지 (slug 하나당 파일 하나)
_posts/                  글
assets/img/posts/        글별 1200x630 SVG 썸네일
tools/make_thumb.py      썸네일 생성기
```

## 글 하나 올리는 법

1. 썸네일부터 만든다.

```bash
python3 tools/make_thumb.py \
  --cat ott --badge "OTT 신작" \
  --line1 "작품 제목" --line2 "부제 한 줄" \
  --sub "설명 한 줄" \
  --out assets/img/posts/thumb-슬러그.svg
```

`--cat` 은 `drama` `movie` `ott` `issue` `pick` 중 하나. 카테고리 색은 이 값으로 정해진다.

2. `_posts/YYYY-MM-DD-슬러그.md` 를 만든다. 파일명 슬러그는 영문·숫자·하이픈만 쓴다(URL이 된다).

```yaml
---
layout: post
title: "제목"
date: 2026-09-04 09:00:00 +0900
categories: [OTT 신작]          # _data/categories.yml 의 name 과 정확히 일치해야 함
tags: [태그1, 태그2]
image: /assets/img/posts/thumb-슬러그.svg
platform: "Netflix"             # 선택 — 카드와 상단에 뱃지로 표시
airing: "토·일 밤 9시 10분"      # 선택 — 방영 정보
summary: "카드와 상단에 들어갈 두 줄 요약"
verdict: "한 줄 평"              # 선택
watch_if: "이런 분께"            # 선택
skip_if: "넘겨도 좋은 분"         # 선택
---
```

3. 커밋 후 1~2분이면 반영된다.

## 카테고리를 새로 만들 때

1. `_data/categories.yml` 의 `fixed:` 아래에 `slug/name/color/c2/icon/desc` 여섯 줄을 추가한다.
   색은 이미 쓰고 있는 색과 색상환에서 확실히 떨어진 계열로 고른다.
2. `categories/<slug>.html` 파일을 하나 만든다.

```
---
layout: category
title: "화면에 보일 이름"
permalink: /categories/<slug>/
cat_slug: <slug>
---
```

3. `tools/make_thumb.py` 의 `PALETTE` 와 `ART` 에도 같은 slug 를 추가한다.

## 지키는 원칙

작품명·방영일·공개일정·출연진·시청률 수치는 **공식 발표와 보도자료를 교차 확인한 것만** 쓴다.
확인되지 않으면 그날은 그 소재를 건너뛴다. 평가와 해석은 사실과 분리해서 적는다.
