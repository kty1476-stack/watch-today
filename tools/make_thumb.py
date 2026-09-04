#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""오늘 뭐보지 — 1200x630 SVG 썸네일 생성기

사용:
  python3 tools/make_thumb.py --cat ott --badge "OTT 신작" \
      --line1 "메이드 인 코리아 시즌2" --line2 "9월 9일 디즈니+" \
      --sub "현빈·정우성·우도환, 9년 만의 재대결" \
      --out assets/img/posts/thumb-made-in-korea-2.svg

레이아웃 규칙(고정): 왼쪽 텍스트 / 오른쪽 일러스트 2단.
카테고리 색은 _data/categories.yml 과 동일하게 유지할 것.
"""
import argparse, html, os

PALETTE = {
    "drama": ("#E11D48", "#7F1030"),
    "movie": ("#7C3AED", "#3B1C7A"),
    "ott":   ("#0EA5E9", "#08506F"),
    "issue": ("#F59E0B", "#7C4A05"),
    "pick":  ("#10B981", "#065F46"),
    "etc":   ("#64748B", "#26303D"),
}

# 오른쪽에 들어가는 카테고리별 일러스트 (0,0 기준 400x400 박스 안에서 그림)
ART = {
    # TV 수상기
    "drama": """
      <rect x="20" y="60" width="360" height="230" rx="22" fill="rgba(255,255,255,.16)" stroke="rgba(255,255,255,.55)" stroke-width="6"/>
      <rect x="52" y="92" width="296" height="166" rx="10" fill="rgba(255,255,255,.10)"/>
      <path d="M172 140 L240 175 L172 210 Z" fill="rgba(255,255,255,.85)"/>
      <rect x="150" y="300" width="100" height="14" rx="7" fill="rgba(255,255,255,.5)"/>
      <path d="M200 290 L200 300" stroke="rgba(255,255,255,.5)" stroke-width="10"/>
      <path d="M120 30 L165 72 M280 30 L235 72" stroke="rgba(255,255,255,.45)" stroke-width="8" stroke-linecap="round"/>
    """,
    # 필름 릴
    "movie": """
      <circle cx="200" cy="180" r="130" fill="none" stroke="rgba(255,255,255,.55)" stroke-width="8"/>
      <circle cx="200" cy="180" r="26" fill="rgba(255,255,255,.7)"/>
      <circle cx="200" cy="92" r="30" fill="rgba(255,255,255,.22)"/>
      <circle cx="200" cy="268" r="30" fill="rgba(255,255,255,.22)"/>
      <circle cx="288" cy="180" r="30" fill="rgba(255,255,255,.22)"/>
      <circle cx="112" cy="180" r="30" fill="rgba(255,255,255,.22)"/>
      <rect x="40" y="322" width="320" height="48" rx="8" fill="rgba(255,255,255,.16)" stroke="rgba(255,255,255,.45)" stroke-width="4"/>
      <path d="M76 322 v48 M132 322 v48 M188 322 v48 M244 322 v48 M300 322 v48" stroke="rgba(255,255,255,.45)" stroke-width="4"/>
    """,
    # 재생 버튼 + 화면들
    "ott": """
      <rect x="60" y="40" width="290" height="180" rx="16" fill="rgba(255,255,255,.12)" stroke="rgba(255,255,255,.45)" stroke-width="5"/>
      <rect x="30" y="90" width="290" height="180" rx="16" fill="rgba(255,255,255,.18)" stroke="rgba(255,255,255,.6)" stroke-width="6"/>
      <circle cx="175" cy="180" r="56" fill="rgba(255,255,255,.85)"/>
      <path d="M158 152 L206 180 L158 208 Z" fill="var(--c1)" opacity="0.95"/>
      <rect x="60" y="310" width="230" height="12" rx="6" fill="rgba(255,255,255,.4)"/>
      <rect x="60" y="342" width="150" height="12" rx="6" fill="rgba(255,255,255,.25)"/>
    """,
    # 상승 그래프
    "issue": """
      <rect x="30" y="60" width="340" height="270" rx="18" fill="rgba(255,255,255,.12)" stroke="rgba(255,255,255,.5)" stroke-width="6"/>
      <path d="M70 280 L150 210 L210 240 L330 110" fill="none" stroke="rgba(255,255,255,.9)" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="70" cy="280" r="12" fill="#fff"/><circle cx="150" cy="210" r="12" fill="#fff"/>
      <circle cx="210" cy="240" r="12" fill="#fff"/><circle cx="330" cy="110" r="14" fill="#fff"/>
      <path d="M296 110 h48 v46" fill="none" stroke="rgba(255,255,255,.6)" stroke-width="6" stroke-linecap="round"/>
    """,
    # 별 + 리스트
    "pick": """
      <path d="M200 40 L232 128 L326 132 L252 190 L278 282 L200 228 L122 282 L148 190 L74 132 L168 128 Z"
            fill="rgba(255,255,255,.85)"/>
      <rect x="60" y="316" width="280" height="14" rx="7" fill="rgba(255,255,255,.45)"/>
      <rect x="60" y="348" width="200" height="14" rx="7" fill="rgba(255,255,255,.3)"/>
      <rect x="60" y="380" width="240" height="14" rx="7" fill="rgba(255,255,255,.2)"/>
    """,
}
ART["etc"] = ART["ott"]

TPL = """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-label="{alt}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
    <linearGradient id="scrim" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000" stop-opacity="0.34"/>
      <stop offset="62%" stop-color="#000" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect width="1200" height="630" fill="url(#bg)"/>
  <g opacity="0.10">
    <circle cx="1080" cy="70" r="200" fill="#fff"/>
    <circle cx="90" cy="600" r="150" fill="#fff"/>
  </g>
  <rect width="1200" height="630" fill="url(#scrim)"/>

  <g transform="translate(810,118)" style="--c1:{c1}">{art}</g>

  <g font-family="'Noto Sans KR','Noto Sans CJK KR','Apple SD Gothic Neo','Malgun Gothic','Nanum Gothic',sans-serif">
    <rect x="72" y="66" rx="20" height="40" width="{badge_w}" fill="rgba(255,255,255,.92)"/>
    <text x="{badge_tx}" y="94" font-size="22" font-weight="700" fill="{c2}" text-anchor="middle">{badge}</text>

    <text x="72" y="288" font-size="{fs1}" font-weight="900" fill="#fff" letter-spacing="-1.5">{line1}</text>
    {line2_el}

    <rect x="72" y="{rule_y}" width="86" height="6" rx="3" fill="rgba(255,255,255,.75)"/>
    <text x="72" y="{sub_y}" font-size="34" font-weight="500" fill="rgba(255,255,255,.92)">{sub}</text>

    <text x="72" y="574" font-size="24" font-weight="700" fill="rgba(255,255,255,.7)">▶ 오늘 뭐보지</text>
  </g>
</svg>
"""


def esc(s):
    return html.escape(s or "", quote=False)


def width_of(s):
    """한글은 넓게, 영문/숫자는 좁게 잡은 대략적인 글자폭 추정."""
    w = 0.0
    for ch in s:
        w += 1.0 if ord(ch) > 0x2000 else 0.55
    return w


def build(cat, badge, line1, line2, sub):
    c1, c2 = PALETTE.get(cat, PALETTE["etc"])
    art = ART.get(cat, ART["etc"]).replace("var(--c1)", c1)

    bw = int(width_of(badge) * 22 + 44)
    # 왼쪽 텍스트 영역은 x=72부터 오른쪽 일러스트 앞(약 772px)까지만 쓴다.
    longest = max(width_of(line1), width_of(line2 or ""), 1.0)
    fs1 = int(min(66, 700.0 / longest))
    fs1 = max(38, fs1)

    if line2:
        line2_el = ('<text x="72" y="%d" font-size="%d" font-weight="900" fill="#fff" '
                    'letter-spacing="-1.5">%s</text>') % (288 + fs1 + 16, fs1, esc(line2))
        rule_y, sub_y = 288 + fs1 + 66, 288 + fs1 + 146
    else:
        line2_el = ""
        rule_y, sub_y = 340, 420

    return TPL.format(
        alt=esc("%s - %s" % (badge, line1)),
        c1=c1, c2=c2, art=art,
        badge=esc(badge), badge_w=bw, badge_tx=72 + bw // 2,
        line1=esc(line1), line2_el=line2_el, fs1=fs1,
        rule_y=rule_y, sub_y=sub_y, sub=esc(sub),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cat", required=True, choices=list(PALETTE.keys()))
    ap.add_argument("--badge", required=True)
    ap.add_argument("--line1", required=True)
    ap.add_argument("--line2", default="")
    ap.add_argument("--sub", default="")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(build(a.cat, a.badge, a.line1, a.line2, a.sub))
    print("wrote", a.out)


if __name__ == "__main__":
    main()
