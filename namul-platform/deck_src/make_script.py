import json, re, sys
sys.path.insert(0, ".")
from script_data import SLIDES
from ko_norm import normalize
PACE = 5.0      # 사람 발표 속도: 초당 5음절 ≈ 분당 300음절
GAP = 1.0       # 슬라이드 전환 여유(초)
def syl(t): return len(re.findall(r"[가-힣]", normalize(t)))
def mmss(x): return "%d:%02d" % (int(x) // 60, int(x) % 60)
t = 0.0; out = []
for sl in SLIDES:
    n = sum(syl(s) for s in sl["s"]); dur = (n / PACE + GAP) if sl["s"] else 0
    out.append(dict(n=sl["n"], sec=sl["sec"], title=sl["title"], sentences=sl["s"], syllables=n,
                    start=round(t, 1), dur=round(dur, 1), notes=("[%s–%s] " % (mmss(t), mmss(t + dur)) + " ".join(sl["s"])) if sl["s"] else "(부록 — 발표하지 않음. 질의응답 때 근거로 보여 준다.)"))
    t += dur
json.dump(out, open("script.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
total_syl = sum(o["syllables"] for o in out)
print("total syllables", total_syl, "| est. human talk", mmss(t))
for o in out: print(o["n"], o["sec"], o["syllables"], mmss(o["start"]), "%.0fs" % o["dur"])
# ---- 대본 문서 ----
L = []
L.append("# 나물로 — 발표 대본 (8–10분)\n")
L.append("> 사람이 읽는 속도(분당 약 300음절) 기준 예상 시간 **%s**. 슬라이드 노트에도 같은 대본이 들어 있다 (PowerPoint 발표자 보기·녹화 화면에서 보인다).\n" % mmss(t))
L.append("## 녹화해서 mp4 만들기 (본인 목소리 — 제출용 권장)\n")
L.append("1. PowerPoint(Windows, Microsoft 365)에서 `02_발표자료_나물로.pptx` 열기 → **녹화** 탭 → **녹화 → 처음부터**. (Mac: **슬라이드 쇼 → 슬라이드 쇼 녹화**)")
L.append("2. 녹화 화면 위쪽에 슬라이드 노트(이 대본)가 보인다. 카메라를 켜면 얼굴이 함께 녹화된다.")
L.append("3. 슬라이드마다 아래 시간표를 참고해 말하고 → 방향키로 넘긴다. 실수한 슬라이드는 그 슬라이드만 다시 녹화하면 된다.")
L.append("4. **파일 → 내보내기 → 비디오 만들기** → `Full HD (1080p)` · `기록된 시간 및 내레이션 사용` → 파일 형식 **MP4** 로 저장. (Mac: 파일 → 내보내기 → 파일 형식 MP4)")
L.append("※ 14번 시연 장표의 영상은 PowerPoint 슬라이드 쇼에서 클릭하면 재생된다. 녹화할 때 영상이 끝난 뒤 넘기면 된다.")
L.append("5. 길이가 8–10분 안인지 확인한다. 길면 각 슬라이드의 마지막 보충 문장부터 줄인다. PowerPoint 녹화가 어려우면 화면 녹화(OBS·Zoom 녹화·휴대폰 거치 촬영)도 된다.\n")
L.append("> 함께 제공한 `05_발표영상_초안_AI음성.mp4`(9분 1초)는 **오프라인 AI 음성 + 자막 초안**이다. 14번 시연 장표에는 실제 웹앱 화면 녹화가 들어 있다. 흐름·속도 연습과 비상용이며, 발음이 부자연스러운 부분이 있어(자동 음성인식으로 측정한 글자 오류율 약 33%) 제출은 본인 녹화본을 권한다.\n")
L.append("## 시간표\n")
L.append("| # | 구간 | 슬라이드 | 시작 | 길이 |")
L.append("|---|---|---|---|---|")
for o in out:
    if o["sentences"]: L.append("| %d | %s | %s | %s | %d초 |" % (o["n"], o["sec"], o["title"], mmss(o["start"]), round(o["dur"])))
L.append("")
for o in out:
    if not o["sentences"]: continue
    L.append("## %d. [%s] %s  `%s–%s`\n" % (o["n"], o["sec"], o["title"], mmss(o["start"]), mmss(o["start"] + o["dur"])))
    for s in o["sentences"]: L.append(s + "\n")
L.append("## 예상 질문과 답변 (Q&A 대비)\n")
QA = [
 ("배민·네이버도 전통시장 장보기를 하는데, 왜 나물로가 필요한가요?",
  "그들은 사기로 마음먹은 고객을 배달해 주는 채널입니다. 나물로는 도감·레시피·AI 셰프로 수요 자체를 만들고, 상인에게는 카톡 한 줄 재고 등록·입고 추천·마감 할인 같은 AI 운영 도구를 줍니다. 상인은 배민과 함께 써도 됩니다(독점 요구 없음)."),
 ("AI가 재고나 가격을 잘못 읽으면요?",
  "AI가 정리한 결과는 사장님이 ‘확인’을 눌러야 게시됩니다. 단가·수량은 범위 검증을 하고, AI가 만든 내용에는 ‘AI 정리’ 표시를 붙입니다. 0단계에서는 오류율을 직접 기록합니다."),
 ("AI 비용은 감당할 수 있나요?",
  "Claude Opus 5.5 기준으로 상인 메시지 1건 약 6원, AI 셰프 1회 약 23원입니다. 3년 차 규모에서 월 약 72만 원, 주문당 약 24원으로 매출의 약 1%입니다. 대량 작업에 경량 모델을 쓰면 월 약 20만 원까지 낮출 수 있습니다(1달러=1,400원, 토큰 수는 추정)."),
 ("사진을 찍으면 산에서 캔 나물도 먹어도 되는지 알려 주나요?",
  "아니요. 원추리와 여로, 곰취와 동의나물처럼 독초와 헷갈리는 경우가 있어, AI는 야생 채취 식물의 식용 여부를 판단하지 않습니다. 사진 기능은 냉장고·장바구니 재료 인식에만 씁니다."),
 ("상인들이 앱을 쓰지 않으면요?",
  "앱을 강요하지 않습니다. 평소처럼 카톡으로 보내면 AI가 정리합니다. 0단계는 운영자가 직접 확인하며 돌려 상인 부담을 0에 가깝게 만든 뒤 검증합니다."),
 ("나물은 봄 한철 아닌가요?",
  "시금치·콩나물·배추처럼 사계절 나물이 있고, 묵나물(말린 나물)은 겨울~초봄용입니다. 정월대보름 9나물 꾸러미, 봄 산나물 한정판처럼 시즌 상품으로 비수기를 메웁니다."),
 ("원산지는 어떻게 믿나요?",
  "2023년 중국산 고사리 56톤이 국산으로 섞여 급식에 납품된 사건이 있었습니다. 매장별 원산지 표시를 의무화하고, 위반 매장은 바로 제외하며, 로컬푸드 직매장·산지와 연계합니다."),
 ("3년 차 수치의 근거는?",
  "매장 300곳 × 매장당 월 100건(주문 환산) × 평균 15,000원 × 12개월 = 54억 원입니다. 모두 가정이며, 0단계 검증(주문 100건·재구매 30%)에서 첫 숫자를 실측해 고칩니다."),
]
for q, a in QA: L.append("**Q. %s**\n\nA. %s\n" % (q, a))
open(sys.argv[1], "w", encoding="utf-8").write("\n".join(L))
print("wrote", sys.argv[1])
