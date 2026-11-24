#!/usr/bin/env python3
"""TTS script exports from scenes.json.

  tts_typecast.tsv   (primary)  one row = one sentence: scene · no · text as read ·
                                pause after (s) · speed (x1.0) · emotion · emphasis · memo
  tts_elevenlabs.txt (backup)   per scene block, sentences joined by <break time="0.6s" />
  tts_plain.txt                 human-readable, bracket hints explained at the top
  tts_ssml.xml                  W3C SSML 1.1 (secondary)
  script.md                     scene-by-scene narration + on-screen plan + sources
"""
import html
import os

from korean_text import syllables


def _scene_no(sc):
    return sc["id"].upper()


def export_typecast(ep, path):
    cols = ["장면 번호", "문장 번호", "문장 (읽는 꼴)", "뒤 쉼 (초)", "빠르기 (1.0 기준 배수)", "감정", "강조 낱말", "메모"]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\t".join(cols) + "\n")
        for sc in ep["scenes"]:
            for k, ln in enumerate(sc["lines"], 1):
                f.write("\t".join([_scene_no(sc), f"{k:02d}", ln["say"], f"{ln['pause_after']:.2f}",
                                   f"{ln.get('speed', 1.0):.2f}", ln.get("emotion", "차분"),
                                   " · ".join(ln.get("emphasis", [])), ln.get("memo", "")]) + "\n")
    return path


def export_elevenlabs(ep, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("# ElevenLabs 붙여 넣기용 (예비)\n")
        f.write("# '=== S01 ...' 줄과 '#' 줄은 붙여 넣지 않는다 — 그 아래 한 덩어리를 장면 하나로 생성해 ep01_s01.wav 로 받는다.\n")
        f.write("# <break time=\"0.6s\" /> = 그 자리에서 쉼 (ElevenLabs 쉼 태그).  문장 끝 쉼은 우리 파이프라인이 다시 맞추므로 대략이면 된다.\n")
        f.write("# 쉼 태그를 너무 많이 쓰면 소리가 흔들릴 수 있다 — 이상하면 태그를 빼고 마침표만으로도 생성해 본다.\n\n")
        for sc in ep["scenes"]:
            f.write(f"=== {_scene_no(sc)} · {sc['title']} → 파일 이름 {ep['episode'].split('_')[0]}_{sc['id']}.wav ===\n")
            parts = []
            for ln in sc["lines"]:
                parts.append(ln["say"])
                p = min(3.0, float(ln["pause_after"]))
                parts.append(f'<break time="{p:.2f}s" />')
            f.write(" ".join(parts[:-1]) + "\n\n")
    return path


def export_plain(ep, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("""# TTS 사이트에 붙여 넣는 판 (한 줄 = 한 문장)
# 표기 (사람이 보는 표시 — 붙여 넣을 때는 대괄호 · 꺾쇠를 지운다):
#   [쉼 0.45]   이 문장 뒤 쉼 (초)
#   [느리게 0.92] / [빠르게 1.05]   빠르기 배수 (1.0 = 그 목소리의 기본 빠르기)
#   《낱말》     조금 힘주어 읽을 낱말
#   {궁금}       감정 · 말투 (차분 · 가벼움 · 강조 · 궁금 · 진지 · 정리 · 밝게)
# 숫자 · 영어는 읽는 꼴로 이미 풀어 썼다 (예: 오 점 일 퍼센트 · 본드 수).
""")
        for sc in ep["scenes"]:
            f.write(f"\n## {_scene_no(sc)} · {sc['title']}\n")
            for ln in sc["lines"]:
                say = ln["say"]
                for w in ln.get("emphasis", []):
                    if w in say:
                        say = say.replace(w, f"《{w}》", 1)
                sp = float(ln.get("speed", 1.0))
                tag = ""
                if sp < 0.99:
                    tag = f"[느리게 {sp:.2f}] "
                elif sp > 1.01:
                    tag = f"[빠르게 {sp:.2f}] "
                emo = ln.get("emotion", "차분")
                f.write(f"{tag}{{{emo}}} {say} [쉼 {ln['pause_after']:.2f}]\n")
    return path


def export_ssml(ep, path):
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<!-- SSML 1.1 (예비 · 1순위 아님). 엔진마다 지원하는 태그가 다르다 — prosody rate / break / emphasis 만 썼다. -->',
           '<speak version="1.1" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ko-KR">']
    for sc in ep["scenes"]:
        out.append(f'  <!-- {_scene_no(sc)} · {html.escape(sc["title"])} -->')
        out.append("  <p>")
        for ln in sc["lines"]:
            say = html.escape(ln["say"])
            for w in ln.get("emphasis", []):
                we = html.escape(w)
                if we in say:
                    say = say.replace(we, f'<emphasis level="moderate">{we}</emphasis>', 1)
            rate = int(round(float(ln.get("speed", 1.0)) * 100))
            out.append(f'    <s><prosody rate="{rate}%">{say}</prosody></s><break time="{int(round(ln["pause_after"] * 1000))}ms"/>')
        out.append("  </p>")
    out.append("</speak>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    return path


AUDITION = """# 목소리 고르기용 시험 문장 (Typecast 에서 후보 목소리마다 같은 문장을 생성해 비교)
# 파일 이름: audition_<목소리 이름>.wav  →  <편 폴더>/audio_in/ 에 넣으면
#            python3 -I tools/avi.py audio-qc ep01_mixer --wav <파일> 로 빠르기 · 쉼 · 억양을 잴 수 있다.

1. 전고체 배터리의 양극은, 두 가지 가루를 섞어서 만듭니다.                       (평서 · ~습니다 · 첫 문장)
2. 손으로 섞으면 오 점 일 퍼센트, 기계로 흔들어 섞으면 일 점 사 퍼센트였습니다.     (소수 · 퍼센트 읽기)
3. 작은 가루가 큰 가루를 덮을까요, 아니면 자기들끼리 뭉칠까요?                     (두 물음 · 끝 올림)
4. 이 비율을 본드 수라고 부릅니다.                                               (짧은 문장 · 용어 또박또박)
5. 그리고 이천사 년, 영국 연구진이 AFM, 원자힘현미경으로 그 힘을 직접 쟀습니다.      (연도 · 영어 약자 · 긴 용어)
6. 한 쌍마다, 사천구십육 번씩이요.                                                (큰 수 · 끝 '요')
7. 표면 끈적함의 차이가 사라지는 거죠.                                            (~죠 · 가볍게 내림)
8. 하지만 고체는 스며들지 않거든요.                                               (~거든요 · 설명하는 말투)
9. 한 연구에서 쓴 가루를 보면, 활물질은 사 점 삼 마이크로미터, 고체전해질은 영 점 칠 마이크로미터였어요.   (긴 문장 · 외래어 단위 · 쉼표에서 쉬는지)
10. 여러분이라면, 가루 사이의 힘부터 재시겠어요, 아니면 일단 섞어 보시겠어요?        (시청자에게 묻기)

## 고를 때 들을 점
- 끝 억양: 1 · 4 · 7 · 8 의 끝이 모두 같은 높이 · 같은 꼴로 떨어지면 기계처럼 들린다 — 문장마다 조금씩 달라야 한다.
  3 · 10 의 물음은 끝이 올라가거나 적어도 평평해야 한다 (레퍼런스 영상은 물음도 평서처럼 −4.9 반음 떨어졌다).
- 숫자 읽기: 2 의 "오 점 일" · "일 점 사", 5 의 "이천사 년", 6 의 "사천구십육", 9 의 "사 점 삼" 을 끊김 없이 읽는가 · 숫자 앞에서 아주 조금 느려지는가.
- 영어 · 외래어: 5 의 'AFM' 을 '에이에프엠' 으로 또박또박 읽는가 (영문 그대로 넣었을 때) · 9 의 '마이크로미터' 가 뭉개지지 않는가.  약자를 이상하게 읽는 목소리면 대본처럼 한글로 풀어 쓴 꼴만 쓴다 (1 편 대본에는 영문이 없다 · 다음 편의 DEM · MPM · NCM 도 이 결과로 정한다).
- 쉼: 9 처럼 긴 문장에서 쉼표 자리에 짧게 (0.15–0.3 초) 숨을 쉬는가 · 문장 사이 쉼이 늘 똑같지 않은가.
- 빠르기: 기본 빠르기에서 1 초에 7 음절 안팎 (레퍼런스는 8.4 음절로 빠른 편) · 같은 빠르기가 끝까지 이어지지 않게 문장마다 0.9–1.1 배로 바꿀 수 있는가.
- 소리: 문장 시작 · 끝이 잘리지 않는가 · 쉿 소리 (ㅅ · ㅆ) 가 날카롭지 않은가 · 숨소리를 넣는 옵션이 있으면 한 번 들어 본다.
- 감정 프리셋: '차분 · 궁금 · 진지' 셋만 확실히 구분되면 충분하다 (프리셋 이름은 캐릭터마다 다르다 — 1저자가 화면에서 가장 가까운 것을 고른다).
- 가격 · 상업 이용 조건 · 유튜브 수익화 허용 여부는 1저자가 사이트에서 확인한다 (여기에 적지 않는다).
"""


def export_audition(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(AUDITION)
    return path


def _elem_summary(e):
    t = e.get("type")
    if t in ("text", "source"):
        return None
    if t == "number":
        return f"숫자 {e.get('display') or e['value']}{(' ' + e['unit']) if e.get('unit') else ''}"
    if t == "circle":
        return f"원{(' ' + e['label']) if e.get('label') else ''}"
    if t == "dots":
        return f"점 {len(e['points'])} 개"
    if t == "line":
        return "선" + (" (화살표)" if e.get("arrow") else "")
    if t == "rect":
        return "상자" + ((" " + e["label"]) if e.get("label") else "")
    if t == "mixer":
        return "혼합기 (칼날 회전)"
    if t == "group":
        return "원자힘현미경 탐침"
    if t == "area":
        return "칠한 영역"
    if t == "person":
        return "사람"
    return t


def export_script_md(ep, tl, path, extra=None):
    lid = {ln["id"]: ln for ln in tl["lines"]}
    lines = [f"# {ep['title']} — 대본 · 화면 계획 · 출처", "",
             f"- 시리즈: {ep.get('series', '')} · 에피소드 `{ep['episode']}` · 부제: {ep.get('subtitle', '')}",
             f"- 길이 (무음 미리보기 · 말 빠르기 모형 {ep['voice_model']['base_rate']} 음절/s 가정): "
             f"{tl['duration'] / 60:.1f} 분 ({tl['duration']:.0f} s) · 문장 {len(tl['lines'])} · 자막 {len(tl['captions'])} · "
             f"음절 {sum(syllables(l['say']) for l in tl['lines'])}",
             "- 이 파일은 `build_scenes.py` → `scenes.json` 에서 만든다 (내용을 바꾸려면 build_scenes.py 를 고치고 `avi.py tts` 를 다시 돌린다).",
             "- 줄 표기: **화면 글** (자막 · 숫자) / *읽는 꼴* (TTS 에 넣는 말) · 뒤 쉼 · 빠르기 · 감정.", ""]
    if extra:
        lines += extra + [""]
    lines += ["## 챕터 (무음 미리보기 시간 기준 · TTS 를 넣은 뒤 다시 계산)", ""]
    for sc in ep["scenes"]:
        t0 = lid[sc["lines"][0]["id"]]["t0"]
        mm, ss_ = divmod(int(max(0, t0 - 0.7)), 60)
        lines.append(f"- {mm:d}:{ss_:02d} {sc['title']}")
    lines.append("")
    for sc in ep["scenes"]:
        lns = [lid[l["id"]] for l in sc["lines"]]
        t0 = lns[0]["t0"]
        t1 = lns[-1]["t1"] + lns[-1]["pause"]
        lines.append(f"## {sc['id'].upper()} · {sc['title']}  ({t0:.0f}–{t1:.0f} s)")
        lines.append("")
        lines.append("### 내레이션")
        for k, ln in enumerate(sc["lines"], 1):
            say = ln["say"]
            sp = ln.get("speed", 1.0)
            lines.append(f"{k}. **{ln['text']}**  ")
            if say != ln["text"]:
                lines.append(f"   *{say}*  ")
            lines.append(f"   쉼 {ln['pause_after']:.2f} s · 빠르기 ×{sp:.2f} · {ln.get('emotion', '차분')}"
                         + (f" · 강조: {' · '.join(ln['emphasis'])}" if ln.get("emphasis") else "")
                         + (f" · {ln['memo']}" if ln.get("memo") else ""))
        lines.append("")
        lines.append("### 화면")
        for sh in sc["shots"]:
            texts = [e["text"].replace("\n", " ") for e in sh["elements"] if e.get("type") == "text"]
            objs = [s for s in (_elem_summary(e) for e in sh["elements"] if not e.get("keep")) if s]
            keeps = [e["id"] for e in sh["elements"] if e.get("keep")]
            lines.append(f"- **{sh['id']}** (문장 {sh['from'].split('_l')[1]}부터): "
                         + (f"이어 옴: {', '.join(keeps)} · " if keeps else "")
                         + (f"개체: {', '.join(objs)}" if objs else "")
                         + (f" · 글: {' / '.join(texts)}" if texts else ""))
        srcs = [e["text"].replace("\n", " ") for sh in sc["shots"] for e in sh["elements"] if e.get("type") == "source"]
        if srcs:
            lines.append("")
            lines.append("### 화면 출처 줄")
            for s in srcs:
                lines.append(f"- {s}")
        lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path


def export_all(ep, tl, ep_dir, script_extra=None):
    paths = [export_typecast(ep, os.path.join(ep_dir, "tts_typecast.tsv")),
             export_elevenlabs(ep, os.path.join(ep_dir, "tts_elevenlabs.txt")),
             export_plain(ep, os.path.join(ep_dir, "tts_plain.txt")),
             export_ssml(ep, os.path.join(ep_dir, "tts_ssml.xml")),
             export_audition(os.path.join(ep_dir, "voice_audition.txt"))]
    extra_path = os.path.join(ep_dir, "script_header.md")
    extra = None
    if os.path.exists(extra_path):
        with open(extra_path, encoding="utf-8") as f:
            extra = f.read().rstrip("\n").split("\n")
    paths.append(export_script_md(ep, tl, os.path.join(ep_dir, "script.md"), extra))
    return paths
