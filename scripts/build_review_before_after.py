#!/usr/bin/env python3
"""리뷰 비포/애프터 페이지를 **원장에서 생성**한다 → `docs/reviews/review_before_after.html`.

★ 왜 생성기인가: 손으로 적은 초안이 하루 만에 "고침 7 / 열림 57" 로 낡았다 (실제는 고침 20).
  규율 ④ — *정본은 밖으로 강제되지 않으면 새어나간다*.  집계·고친 목록·SHA 는 전부
  `docs/reviews/findings.json` 에서 읽고, 서술 행이 인용하는 **숫자마다 그 항목의 note 안에
  실재하는지** selftest 가 확인한다 (인용은 원장에 닻을 내린다).
★ 산출 HTML 은 `check_review_findings.py --ban-sweep` 범위(`docs/**/*.html`)에 든다.

사용:
  python3 scripts/build_review_before_after.py            # 생성
  python3 scripts/build_review_before_after.py --selftest
"""
from __future__ import annotations
import argparse
import collections
import html
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEDGER = ROOT / 'docs' / 'reviews' / 'findings.json'
OUT = ROOT / 'docs' / 'reviews' / 'review_before_after.html'

LAYERS = [('L1', '접촉 기하 · 피복률', '면적을 무엇으로 세나'),
          ('L2', '접촉망 수송', '그 면적을 저항으로'),
          ('L3', '스케일링법칙', '그 σ 를 타깃으로'),
          ('L4', '등급 · 검증 플래그', '그 값을 판정으로'),
          ('L5', '구조 ML', '그 코퍼스를 학습으로')]

# ── 서술 행: (id, 제목, 믿은 것, 잰 것, 숫자 인용들, 한 줄 결론[, 접히는 본문]) ─────
#    ⚠ `nums` 의 모든 문자열은 그 항목의 note 또는 title 에 **그대로** 있어야 한다 (selftest ①).
#    ★ 7번째 원소는 **선택**이다.  길어진 서술은 여기로 내린다 — 카드 표면에는 한 줄 결론만
#      남기고 나머지는 `<details>` 로 접는다 (2026-09-15: 행마다 산문을 덧붙여 페이지가
#      벽이 됐다는 1저자 지적).
ROWS = [
    ('L1-01', '체적·Tabor 상한이 비물리 면적을 차단한다',
     '세 cap 의 min 이 상한이고 Hertz/LIGGGHTS 가 하한이니, 면적은 언제나 물리적으로 가능한 구간 안에 있다.',
     '얕은 겹침에서 하한 &gt; 상한인데 <b>거부하지 않고 하한을 돌려준다</b>.  코퍼스(LHS 30, 간선 3,619,759)에서 그 접촉이 <b>5.240 %</b>.',
     ['1.784757', '8.016722', '5.240 %', '3,619,759'],
     '값은 안 바꿨다 — 판정문의 최소 방어(기록하고 승격하지 않기) 중 <b>기록</b>만 했다.  하류가 아직 그 플래그를 안 읽는다.'),
    ('L1-02', 'V_overlap 은 두 구의 겹침 부피다',
     '체적 보존 cap 이 실제 lens 부피로 면적을 제한한다.',
     '단일 구면 cap 공식에 R* 를 넣은 것이라 얕으면 참값의 <b>0.493724배</b>, 깊으면 <b>음수</b>.  그런데 정확 lens 로 바꿔도 코퍼스에서 <b>0 / 3,619,759</b> 간선이 바뀐다.',
     ['0.493724', '0/3,619,759'],
     '항등인 이유가 물리가 아니다 — <b>DESC-03</b>(mm 를 m 로 읽음)이 A_volume 을 1000배 부풀려 volume cap 이 <b>원리적으로 결속 불가</b>.  "무해" 로 닫지 않았다.'),
    ('L2-01', '협착저항이 문헌식을 구현한다',
     '코드 주석 "Mikić 1974" — 보정계수 ψ 를 적용한 Holm 협착 저항.',
     '문헌은 ψ 를 <b>곱하고</b> 코드는 <b>나눈다</b>.  독립 기준해가 곱셈 우위를 확정했고, 코드는 곱식의 (1−s)<sup>−3</sup> 배 — s=0.9 에서 <b>1,620배</b>다.  코드가 <b>자기 주석과도</b> 어긋난다.',
     ['1,620배', '1.02491228', '44.31250962', '150.90474195844345', '0.0024068935279540635',
      '99.436 %'],
     '<b>σ 는 올라간다</b> (cutoff 분기는 반대도 허용).  전환은 2026-09-15 에 생산 솔버에 배선됐지만 <b>아직 못 돌린다</b> — baseline 봉인이 런 앞이고 그 봉인은 09-17 창 안에서만 된다.',
     '<p><b>기준해 수치</b> — 기하평균 |ln 비| (nr600, 바른 구간): s≤0.3 에서 곱함 <b>1.02491228</b> vs 나눔 1.69510941 · s&gt;0.3 에서 곱함 1.18902836 vs 나눔 <b>44.31250962</b>.</p>'
     '<p>⚠ Codex 2라운드: 첫 집계는 s=0.3 이 반올림으로 범위 밖에 들어간 3/7 이었다 — 출력에 경고가 찍혀 있었는데 못 봤다.  "참값" 이 아니라 <b>모델 내 비</b>다.</p>'
     '<p><b>2026-09-15 배선</b> — <span class="m">psi_placement</span> 깃발 신설, 기본값은 변경 전 코드와 <b>비트 동일</b>(모르는 값은 거부).  전환이 <b>감사 안의 소스 문자열 치환</b>으로만 있어서 코호트를 두 팔로 돌릴 수가 없었다.</p>'
     '<p><b>재현</b> — 같은 픽스처로 δ 를 키우면 legacy 는 저항이 <b>오르는 구간</b>을 갖고 floor 직전 <b>150.90474195844345</b> 에서 0 으로 떨어진다(절벽).  곱셈은 단조 비증가이고 그 자리가 <b>0.0024068935279540635</b> 로 크게 낮다.  ⛔ 내가 여기 처음 적은 "연속의 끝점" 은 <b>과장이었다</b> — AREA5-07 참조.</p>'
     '<p><b>크기</b> — 계약이 등록한 세 번째 핀(clamp 경계)도 채웠다.  거기서는 양쪽이 다 0 이라 S3 가 <b>항등</b>이고, 삭제분의 <b>99.436 %</b> 가 그 부류이므로 <b>S3 는 "협착이 삭제된 접촉" 의 거의 전부를 안 건드린다</b>.</p>'),
    ('AREA-12', '면적을 둘로 쪼개면 삭제된 협착 항이 되살아난다',
     '피복용 A_surface(상한 2πR²)와 수송용 A_transport(상한 πR²)를 분리하면 σ 가 하향한다 — 계약의 전제.',
     '솔버의 clamp <span class="m">a_eff = min(a, r_min)</span> 이 <b>이미 같은 상한</b>이다.  무작위 20,000 접촉에서 A 는 <b>15.56 %</b> 바뀌는데 a_eff 는 설명 안 되는 차이 <b>0</b>.',
     ['15.56 %', '1 ULP'],
     'S2 의 σ 변화는 <b>산술적으로 0</b>.  살아남는 건 타입 분리의 구조적 가치뿐이고, σ 를 움직이는 축은 S3(ψ 배치) 하나다.'),
    ('AREA-11', 'min(σ₁,σ₂) 는 이종쌍의 보수적 협착 규약이다',
     '두 재료가 만나는 접촉에서 낮은 σ 를 쓰면 안전하다.',
     '직렬 모델 ψ/(4a)(1/σ₁+1/σ₂) 대비 계수비 2·maxσ/(σ₁+σ₂) 만큼 크다.  실제 기준해(σ 1:8) 대비 min 식은 <b>1.6856916312690349</b>배.  생산 AM_P 6 µm–AM_S 2 µm 에서 <b>1.722074배</b>, AM_P 6–AM_P 2 µm 에서도 <b>1.511966128287415</b>배.',
     ['1.6856916312690349', '1.722074', '1.511966128287415'],
     '⚠ Codex 2라운드: 내가 "16/9 와 일치" 라 적은 것은 수치해가 약분되는 <b>계수비</b>였다 — 독립 증거가 아니다.  직렬식도 모델이지 참값이 아니고, 열의 k_weight 는 이미 조화평균이라 이중 보정 금지.  간선 하나당 배수이지 σ_e 의 배수가 아니다.'),
    ('SELF-28', 'geom cap 은 명목상이라 걸리는 값이 없다',
     '2πR_min² 상한은 실제로 도달하지 않는다.',
     '<b>반대였다</b> — 163/163 케이스에서 결속하고, 결속하면 ψ=0 으로 협착 항이 <b>삭제</b>된다.  S0 실측: 이온 <b>20.728 %</b> · 전자 <b>0.000 %</b> · 열 <b>26.850 %</b> 간선.',
     ['163/163', '20.728 %', '0.000 %', '26.850 %', '0.102338~0.102633'],
     '★ 해석은 하향됐다 — <b>원통에서 a=b 면</b> 협착 몫 0 은 맞다.  ⚠ 그러나 생산의 clamp 0 은 a=b 의 독립 측정이 아니라 A_surface 를 원판으로 읽어 강제된 s=1 이라 "참값 0" 으로 면책하지 않는다 (Codex 2라운드).  tabor 결속 구간 대부분도 이미 clamp 로 s=1 — floor 만이 양수를 지우는 띠는 <b>0.102338~0.102633</b> µm 뿐.'),
    ('L3-08', '적합 함수는 데이터가 없으면 멈춘다',
     'EXCL 로 다 걸러지면 적합이 실패하고 그 사실이 보인다.',
     'n=12 전부 EXCL 이어도 <span class="m">n_fit 0 · r2 0.0 · loocv 0.0</span> 으로 <b>정상처럼</b> 돌아오고 예측값 <b>0.07688995743054786</b> 을 낸다.',
     ['0.07688995743054786'],
     '행 수·LIVE 랭크·LOO 폴드 랭크에서 <b>fail-closed</b> 로 고쳤다 (None 반환, 호출자 4곳 처리).'),
    ('L4-11', 'porosity 단위는 자명하다',
     '0~1 분율이든 % 든 함수가 알아서 읽는다.',
     'porosity <b>1</b> → R_ct <b>128462895.60746863</b> · <b>1.000001</b> → <b>4.805944515715439</b>.  1 에서 불연속 — 단위 계약이 없었다.',
     ['128462895.60746863', '4.805944515715439'],
     '명시적 단위 계약(<span class="m">porosity_to_fraction(unit=)</span>)으로 고쳤다.  수정 후 1 % = 4.805944467170544 로 판정문 값과 일치.'),
    ('R4-10', '마감 전에는 S3 를 기계적으로 시작할 수 없다',
     'dry-run 이 봉인을 안 쓰므로 마감(09-17) 전에는 S3 가 시작될 수 없다.',
     '<b>반증됐다</b> — 좁은 주장(dry-run 이 안 쓴다)만 맞고, <b>봉인을 요구하는 러너가 없어서</b> 기계적 차단이 <b>존재하지 않았다</b>.  게다가 날짜 selftest 는 <b>오늘만 초록</b>이라 허용일을 주입하면 도구가 <b>정작 일해야 하는 날에</b> 자기검사가 깨졌다.',
     ['23 PASS', '오늘만 초록'],
     '<b>기계적 차단이 존재하지 않았다.</b>  2026-09-15 에 러너를 만들어 실재하게 했다.',
     '<p><span class="m">--now</span> 로 날짜를 <b>고정 입력</b>으로 주입해 09-16·17·18 을 <b>매번 함께</b> 시험한다 — 창 안에서는 <b>날짜가 통과하고 내용이 막는다</b>.  ⛔ 파일 부재 검사를 지워서 초록으로 만든 것이 아니다.</p>'
     '<p><span class="m">run_s3_psi.py</span>: 봉인이 없거나·창 <b>밖에서</b> 만들어졌거나·B_ch 가 비었거나·ρ 가 없으면 <b>rc=2 로 아무것도 안 한다</b>.</p>'),
    ('AREA5-01', 'S3 러너는 봉인된 코호트에 등록된 절차를 적용한다',
     '실패한 행은 <span class="m">ERROR</span> 게이트가 잡고, 미정값은 계약 A-4 의 0/+∞ 경계로 센다.',
     '<b>실패 행을 빼고 남은 것만으로 중앙값을 낸다</b> — <span class="m">new</span> 하나가 None 이면 정의역 3 · 쓴 것 2 · <b>median=11.0 · h1 · rc=0</b> 으로 발행한다.  등록된 계산은 하한 2 / 상한 20 ⇒ <b>UNDETERMINED_COHORT</b> 다.  게다가 예외가 <span class="m">sigma_of</span> <b>안</b>에서 나면 <span class="m">(None, 1)</span> 로 삼켜져 ERROR 게이트에 <b>도달하지 않는다</b>.',
     ['median=11.0', 'UNDETERMINED_COHORT', '(None, 1)'],
     '⚠ 이것은 Codex 5라운드가 낸 반례이고, <b>내가 내 러너로 직접 재현했다</b>.  내가 커밋 메시지에 적은 "ERROR 가 있으면 판정을 발행하지 않는다" 는 <b>솔버 내부 예외에는 거짓</b>이었다.'),
    ('AREA5-02', '--limit 는 진단 옵션이다',
     '봉인된 B_ch 가 판정 정의역이고, limit 는 몇 건만 돌려 보는 편의 기능이다.',
     '<b>판정 집합 선택기가 됐다</b> — 같은 봉인·같은 데이터에서 <span class="m">--limit 1</span> 만 넣으면 median 이 <b>2.0000000000000018</b> 로 떨어져 <b>h1 → h0</b> 로 뒤집히고, 그래도 <span class="m">rc=0</span> 으로 정상 JSON 을 낸다.  음수 limit 도 받는다.',
     ['2.0000000000000018', '--limit 1'],
     '<span class="m">n_in_domain</span> 도 봉인된 N 이 아니라 <b>처리한 수</b>를 보고하므로 요약만 읽으면 부분집합인 것을 모른다.'),
    ('AREA5-04', '"ρ 필수" 가 판정을 지킨다',
     'ρ 에 기본값을 안 두고 필수로 받으면 친절한 답이 공짜로 나오는 자리가 막힌다.',
     '<b>필수이기만 하고 봉인되지 않았다</b> — 같은 봉인·같은 <span class="m">d = 12.00000000000001</span> 에서 CLI 수치만 7→0 으로 바꾸면 <b>UNRESOLVED_NUMERIC → h1</b> 이다.  현행 봉인기는 ρ <b>수치 필드 자체를 내지 않는다</b>.',
     ['12.00000000000001'],
     '★ 그리고 내가 사용자에게 시킨 ρ 명령이 <b>두 번 틀렸다</b> — 사다리 파일은 09-13 자로 <b>이미 있고</b>, 그것들은 전부 <span class="m">lhs00_100</span>~129 = mono 30 이라 계약이 새 130 에 <b>대입을 금지</b>한 것이다.'),
    ('AREA5-03', '봉인기가 지문을 대조하니 봉인 뒤 바뀐 원자료는 못 들어온다',
     '봉인기가 <span class="m">atom·contact·deck</span> 의 SHA 와 본문 step 을 실제 바이트로 대조한다 (R4-02 수리).',
     '<b>러너가 그 검증을 이어받지 않았다</b> — 봉인은 step 100 을 가리키는데 같은 폴더에 step 200 쌍을 넣으니 <b>step 200 을 읽고 다른 σ 를 rc=0 으로 발행</b>했다.  게다가 봉인이 케이스별 σ_old <b>수치를 보존하지 않아</b> "positive 가 다른 positive 로 바뀐 것" 을 잡을 장치가 아예 없었다.',
     ['BASELINE_VALUE_CHANGED', '52 → 70', '50 → 59'],
     '★ 이제 러너가 소비 직전에 <b>다섯 가지</b>를 다시 본다 — 코드 bundle · 등록부 SHA · 케이스 지문 · <b>봉인된 σ_old 의 재현</b> · 양팔 동결축.  회귀는 러너 <b>52 → 70</b> · 봉인기 <b>50 → 59</b>.',
     '<p><b>봉인이 들고 나가는 것</b> — 읽은 파일의 실제 바이트 SHA 셋, <span class="m">B_ch</span> 케이스의 baseline σ 수치, 그리고 <b>수치 모듈 4개</b>의 지문 묶음.  "현재 HEAD = 기록 SHA" 만으로는 dirty working tree 도 커밋 안 된 의존 변경도 못 잡는다.</p>'
     '<p><b>⛔ 내가 넣은 false-green 을 잡았다</b> — 옛 ⑥c·⑥d 가 <span class="m">code_bundle</span> 없는 <b>가짜 봉인</b>을 써서, 새 게이트가 생기자 "ρ 가 없어서" 가 아니라 "코드 신원이 없어서" rc=2 가 났다.  <b>검사가 이름과 다른 것을 재고 있었다</b> (규율 ⑤).  소비 가능한 봉인으로 고치고 <b>판별력 검사(⑨d)</b> 를 같이 세웠다.</p>'
     '<p>⬜ 남은 것: <span class="m">generation_git_sha</span> 가 가리키는 커밋의 <b>트리</b>가 code_bundle 과 맞는지는 아직 안 본다.</p>'),
    ('AREA5-05', '⑦f 가 기본값 비트 동일을 회귀로 지킨다',
     '<span class="m">git show HEAD:</span> 와 대조하니 도입 전과 같음이 상주 검사로 고정된다.',
     '<b>커밋하면 기준이 같이 움직인다</b> — 커밋 후 working source 와 HEAD 가 같아져 검사가 <b>동어반복</b>이 된다.  열 조화평균을 1 로 바꾼 소스를 "새 HEAD 에도 커밋됨" 으로 모사하니 감사 <b>18/18</b> 인데 같은 픽스처의 old R_total 은 <b>5.812108579096786 → 9.8929507729307</b> 로 바뀐다.',
     ['1,926', '9.8929507729307', '2d9ce3e87', '7,680', '552'],
     '★ 기준을 <b>도입 직전 커밋</b><span class="m">2d9ce3e87</span>(내용 SHA까지 핀)로 옮기고, 그 소스로 만든 <b>봉인된 기대값 파일</b>을 커밋했다.  기준을 못 읽으면 <b>실패</b>한다.',
     '<p><b>동결 격자를 넓혔다</b> — 채널 3 × 상쌍 8(순서 뒤집은 쌍 포함) × 반지름 순서 4(큰 쪽이 먼저인 것 포함) × δ 8 = <b>768 픽스처 × 10 필드 = 7,680 대조</b>, 그 중 Rc&gt;0 픽스처 <b>552</b>.  실측 차이 <b>0</b>.</p>'
     '<p><b>교차검증</b> — 고정 커밋을 읽을 수 있으면 거기서 기대값을 <b>재생성</b>해 봉인 파일과 비트 대조한다.  "봉인 파일만 고쳐 초록을 만드는 길" 을 막는다 (CI 는 <span class="m">fetch-depth: 0</span>).</p>'),
    ('AREA5-06', 'oracle 이 ψ 축을 못박으면 그 계산이 지켜진다',
     'ψ 를 기하에서 독립 계산하는 oracle 을 넣었으니 협착 계산이 고정된다 (R4-08 수리).',
     '<b>반지름 순서와 전자 접촉계수가 자유로웠다</b> — 픽스처가 <span class="m">r1=0.5 &lt; r2=6</span> 하나뿐이라 <span class="m">r_min</span> 을 <span class="m">r1</span> 로 바꿔도 <b>우연히 일치</b>하고, 열 채널뿐이라 <span class="m">min(σ)</span> 를 <span class="m">σ₁</span> 로 바꿔도 둘 다 1.0 이다.',
     ['864', '384'],
     '⚠ <b>판정문보다 나빴다</b> — Codex 는 "변이를 새 HEAD 에도 커밋한 것으로 모사하면" 통과한다고 했는데, 내 재현에서는 <b>기준을 옮기지 않아도</b> 둘 다 초록이었다.',
     '<p><b>수리</b> — 픽스처에 상 조합·채널 축을 신설하고 ψ oracle 을 격자 전체로 넓혔다(활성 <b>864</b>건).  그리고 <b>⑦j 재료계수 oracle</b> 을 신설해 <span class="m">R_Maxwell</span> 로 <span class="m">min(σ)</span> 규약을, <span class="m">R_bulk</span> 로 <b>면별 σ 배정</b>을 각각 못박는다(<b>384</b> 픽스처).  ⑦k 는 상수를 <b>import 하지 않고 대조</b>한다 — import 하면 상수 변이가 기대값과 같이 움직인다.</p>'
     '<p><b>판별력 실측 — 변이 5종이 전부 빨간불</b>이고, 각각 <b>독립된 두 검사</b>에서 걸린다:</p>'
     '<p><span class="m">r_min→r1</span> = ⑦f + ⑦i · <span class="m">min(σ)→σ₁</span> = ⑦f + ⑦j · <span class="m">열 조화평균→1</span> = ⑦f + ⑦j · <span class="m">ψ 지수 1.5→1.0</span> = ⑦d·⑦f·⑦h·⑦i · <span class="m">floor 1e-4→0</span> = ⑦d·⑦f·⑦h·⑦i.  감사 검사 18 → <b>21</b>.</p>'
     '<p>⬜ 남은 것: <b>AM–AM 이 z 를 잇는 실제 침대</b>(전자 채널 코퍼스 픽스처)는 아직 없다.</p>'),
    ('AREA5-07', '곱셈 배치는 floor 자리가 연속이다',
     'legacy 의 절벽(150.9 → 0)이 곱셈에서는 연속의 끝점이 된다.',
     '<b>과장이었다</b> — floor 가 유한한 1e-4 로 동결돼 있어 곱셈판도 <b>불연속</b>이다.  cutoff 인접 float 에서 좌극한이 <b>0.00005010795431502282</b> 이고 그 다음이 0 이다.  ⑦h 가 실제로 검사한 것은 "이산 스윕의 마지막 양수가 legacy 보다 작다" 이지 연속성이 아니다.',
     ['0.00005010795431502282', '0.00010000000000000524', '2943.8423160074362',
      '2.943842316007745e-05'],
     '바른 문장: "곱셈 배치는 legacy 의 큰 저항 급락을 크게 줄이지만, 동결된 finite floor 때문에 작은 불연속은 남는다."  ⛔ floor 를 지금 바꾸라는 뜻이 아니다 — 검사의 이름과 서술만 고친다.',
     '<p><b>단언을 실제 측정으로 바꿨다</b> — 절단면을 실제 솔버로 200회 이분해 좌극한을 재고, 그 값이 <span class="m">R_Maxwell·ψ*</span> 와 같은지, legacy 대비 비가 <span class="m">1/ψ*²</span> 인지, <b>그 다음 값이 둘 다 0</b> 인지를 본다.</p>'
     '<p>실측(r1=r2=1 µm): ψ* = <b>0.00010000000000000524</b> · 좌극한 legacy <b>2943.8423160074362</b> vs 곱셈 <b>2.943842316007745e-05</b> (= R_M·ψ*) · 다음 값 0.0/0.0 · 비 <b>1e+08 = 1/ψ*²</b> 정확히.</p>'
     '<p>⚠ 좌극한이 판정문의 값과 다른 것은 <b>픽스처 기하가 달라</b> R_Maxwell 이 다르기 때문이다.  ψ* 와 관계식은 같다.</p>'),
    ('AREA5-08', '활성 간선 개수가 같으면 두 팔은 같은 망이다',
     'ψ 만 바꾸는 전환이니 활성 개수가 같은지 세면 범위 위반을 잡을 수 있다.',
     '<b>양방향으로 틀렸다</b> — 개수가 <span class="m">1 → 0</span> 이어도 <span class="m">status=ok · h1 · rc=0</span> 으로 발행했고(수용 과잉), 반대로 <b>유효한 전체 무변화</b>(두 팔이 같은 유효 σ, Δ=0)는 rc=3 으로 <b>버렸다</b>(거부 과잉).  개수가 같아도 <b>자리</b>가 바뀌면 다른 실험이다.',
     ['FROZEN_AXIS_CHANGED', 'NO_ACTIVE_EDGES'],
     '★ 이제 두 팔의 <b>간선 ID 집합</b>·면적·R_bulk·재료계수·기하·<b>floor 지원집합</b>이 전부 같아야 한다 — 다르면 <span class="m">FROZEN_AXIS_CHANGED</span>.  무변화는 <span class="m">NO_ACTIVE_EDGES</span> 한정을 달아 <b>보존</b>한다.',
     '<p><b>회귀 4건</b>: 두 팔의 동결 축이 같다 · <b>한 간선의 R_bulk 만 바꿔도 잡는다</b>(개수만 보던 옛 판은 못 잡았다) · 간선 ID 집합이 달라지면 잡는다 · <b>floor 지원집합</b>이 달라지면 잡는다.</p>'),
    ('AREA5-09', '봉인 창이 닫혀 있으니 발행 시점을 고를 수 없다',
     '09-17 23:59 KST 고정 마감을 코드가 강제하니 "언제 멈출지" 의 여지가 사라진다.',
     '<b>둘 다 틀렸다</b> — ① <span class="m">--now</span> 로 만든 <b>시험 봉인이 생산 봉인과 구별되지 않아</b> 09-15 에 만든 것을 러너가 rc=0 으로 받았다 (내 주장 "손으로 만든 봉인만 걸린다" 가 <b>REFUTED</b>).  ② <b>고정 cutoff ≠ 발행 창</b> — 저자가 정한 것은 <i>수신 종료</i> 인데 코드는 그날 <b>아무 때나</b> 발행을 허용했다.',
     ['test_only', 'PENDING_BASELINE'],
     '★ 이제 <span class="m">--now</span> 산물은 <span class="m">test_only</span> 로 낙인찍혀 생산 판정에서 거부되고, <b>수신 동결</b>과 <b>봉인 발행</b>이 두 단계로 갈렸다.',
     '<p><span class="m">--freeze-inventory</span> 는 σ 를 <b>한 건도 풀지 않고</b> 원자료 지문만 cutoff 기준으로 못박는다(마감 전에만).  <span class="m">--inventory</span> 로 봉인하면 <b>그 inventory 가 정의역</b>이고 뒤에 온 것은 <span class="m">PENDING_BASELINE</span> 이며, 동결 뒤 원자료가 바뀌면 발행이 멈춘다.</p>'
     '<p>★ 그리고 <b>마감 전에 동결해 뒀으면 계산이 마감 뒤에 끝나도 발행된다</b> — 판정문의 "cutoff 이후에 계산이 끝났다는 이유만으로 cutoff 이전에 확정된 원자료를 거부하지 않는다".  <b>판별력</b>: inventory 없이 마감 뒤면 여전히 거부다(창이 느슨해진 게 아니다).</p>'
     '<p>★★ 내 프레이밍도 정정했다 — "봉인 뒤 검사기 수정은 무조건 결과를 보고 심판을 바꾼 것" 은 <b>과했다</b>.  결과를 보지 않은 상태의 수정은 구별할 수 있고, deadline 이 알려진 결함을 그대로 실행할 이유가 되어선 안 된다.</p>'),
    ('LHS-03', '코호트 131 이 그대로 세 채널의 판정 대상이다',
     '<span class="m">RAW_OK</span> 면 세 채널 다 σ 가 나오고, 봉인이 정한 <span class="m">B_ch</span> 가 곧 코호트 크기다.',
     '<b>이온만 25/127 (19.7 %) 이 관통하지 않는다</b> — 전자·열은 0건.  ⇒ <b>S3 이온 판정 정의역은 최대 102</b> 다.  그리고 이온 σ 가 <b>7,059배</b> 산포한다 (전자 27배 · 열 3.2배) — 이온만 퍼콜 경계를 가로지르기 때문이다.',
     ['25/127', '7,059배', '42.9 %', '29 ~ 2,324', '20.2 %', '0건'],
     '★★ <b>기전 확정</b> — 24/25 는 SE 망이 <b>수백~수천 조각</b>으로 부서진 진짜 단절이다 (성분 29~2,324 · 고립 SE 입자 중앙 <b>20.2 %</b>).  경계 artifact 는 <b>1건</b>뿐이다 (LHS-04).',
     '<p>⚠ 이 σ 는 전부 <b>legacy 팔 = 생산 기본값</b>이고 <b>S3 결과가 아니다</b>.  ρ 리허설이 127 케이스 × 3 채널에 생산 솔버를 돌린 <b>부산물</b>로 코호트가 처음 보인 것이다.</p>'
     '<p>⚠ 전자 채널 최소 <span class="m">n_nodes = 30</span> — 30 노드짜리 AM–AM 망이 관통 판정을 받았다 (미확인).</p>'
     '<p>★★★ <b>그리고 이것이 φc 서술을 정밀화한다 — 내 문장을 고친다.</b>  옛 표현 <i>"φ_SE 로 안 갈린다, 완전히 겹친다"</i> 에서 <b>그 겹침을 만든 유일한 케이스가 lhs00_009 이고 그것은 경계 artifact</b> 다.  빼면 <b>φ_SE ≥ 0.20 인 진짜 단절은 0건</b>.</p>'
     '<p>⇒ 바른 문장: 동결 문턱 <span class="m">φc = 0.20</span> 은 <b>"위면 뚫린다" 쪽에서는 맞다</b>.  틀린 것은 <b>"아래면 안 뚫린다" 쪽뿐</b>이다 (φ_SE 0.1720 에서 17/17 뚫림) — <b>충분조건으로는 성립하고 필요조건으로는 성립하지 않는다</b>.</p>'
     '<p>⬜ <b>새 관측</b> — 고립 SE 입자가 많다.  <span class="m">lhs00_093</span> 은 1,570개 중 <b>774개(49.3 %)가 접촉이 하나도 없다</b>.  φ_SE ≈ 0.09 라 그럴듯하지만 300 MPa 압밀 뒤 절반이 무접촉인 것이 정상인지는 <b>확인된 바 없다</b> — 접촉 검출 쪽 가능성도 배제 못 한다.</p>'
     '<p>⬜ 봉인기가 이 25건을 <span class="m">OLD_NONE</span> 으로 분류해야 봉인과 ρ 가 <b>같은 데이터를 본 것</b>이다.</p>'
     '<p>★★★ <b>정정 2026-09-15 — 판독문 ④ <i>"유한크기가 φ 보다 잘 가른다"</i> 를 철회한다.</b>  같은 척도(군별 막힘률)로 재면 φ 쪽 <b>45.3배</b>(1.2 % vs 54.5 %) vs 유한크기 <b>5.1배</b>(42.9/13.7/8.3/25.0 %, <b>단조도 아니다</b>) ⇒ <b>φ 쪽이 9배 더 잘 가른다</b>.  LHS-04 가 lhs00_009 를 경계 artifact 로 판정해 φ 서술을 뒤집은 뒤 <b>④ 를 같이 고치지 않아</b> 문서 안에서 하루 동안 서로 모순이었다.  ⚠ 유한크기가 무정보인 것은 아니다 — 둘을 함께 쓰면 정밀도 54.5 → <b>61.1 %</b>(재현율은 96.0 → 44.0 %).  ⚠ 두 축은 <b>교락</b>돼 있다 (얇은 침대 ↔ SE 희박 침대).</p>'),
    ('LHS-01', '설계의 <span class="m">se_percolation</span> 열이 퍼콜레이션 여부를 말해 준다',
     '<span class="m">phi_se_est</span> 를 문턱 0.20 에 대서 만든 라벨이니, 코호트를 거를 때 그것을 보면 된다.',
     '<b>선별기이지 필터가 아니다</b> — <span class="m">BELOW_phic</span> 44건 중 <b>20건이 실제로는 뚫린다</b>(정밀도 54.5 %).  <b>그러나 재현율은 96.0 %</b> 다: 막힌 25건 중 24건을 잡고, 놓친 1건은 <span class="m">lhs00_009</span> = 경계 artifact 라 <b>물리적으로는 25/25</b> 다.',
     ['54.5', '96.0', '0.1720'],
     '⛔ <b>그 열로 코호트를 거르면 실제로 뚫리는 20건을 잘못 버린다.</b>  ⇒ 결함은 <i>"쓸모없다"</i> 가 아니라 <b>이름과 용법</b>이다.',
     '<p>★★★ <b>수리 완료 (2026-09-15)</b> — 개명 <span class="m">se_percolation → se_percolation_est_meanfield</span> · <span class="m">finite_size_flag</span> 에서 <span class="m">se_*</span> 조각을 <span class="m">se_perc_est_flag</span> 자기 열로 분리 · 운용 특성을 <span class="m">LHS_PERC_MEASURED</span> 에 동결.  회귀 검사 ⑬–⑬d 4개가 상주하고 <b>옛 코드에 걸면 ⑬·⑬b 가 둘 다 FAIL</b> 한다 (판별 확인).</p>'
     '<p>★ <b>새 규칙이 아니라 기존 규칙의 미적용</b>이었다 — 같은 파일이 이미 <i>"타깃 이름에 규약을 박는다"</i>(리뷰 HIGH-F)를 규칙으로 세워 뒀는데 <b>이 열만 예외</b>로 남아 있었다.</p>'
     '<p>★ 분리의 크기: 설계 130 행 중 44 행이 접합으로 켜졌고 그 중 <b>22 행은 유한크기가 깨끗</b>한데도 플래그가 서 있었다 = 기하와 물리추정이 한 열에서 <b>구별 불가</b>였다.</p>'
     '<p>⛔⛔ <b>동결 CSV 는 한 바이트도 안 건드렸다</b> — <span class="m">seal_s3_prerun.py</span> 가 그 파일의 sha256 을 봉인에 박고 러너가 소비 직전에 재검증한다.  지금 고치면 09-17 봉인이 <b>다른 파일을 가리킨다</b> = <b>AREA5-05</b>(기준이 함께 이동한다)와 같은 자리.  ⇒ 개명은 <b>생성기에만</b> 적용되고 실측은 <b>별도 파일</b>로 조인한다 (<span class="m">docs/data/lhs_percolation_measured_20260915.csv</span>).  ⚠ 그 결과 <b>헤더가 두 세대</b>가 된다.</p>'
     '<p>⚠⚠ 이것은 σ_ionic 폼의 <span class="m">φc_P = 0.200 · φc_S = 0.195</span> 가 <b>틀렸다는 뜻이 아니다</b>.  그 값은 <b>σ 함수형에 들어가는 평균장 상수</b>로 코퍼스에 적합·동결된 것이고, <i>"이 침대가 벽에서 벽까지 뚫리는가"</i> 의 판정선이 아니다.  무너지는 것은 <b>그 둘을 같은 것으로 읽는 것</b>뿐이다.</p>'
     '<p>⚠ 그리고 <span class="m">phi_se_est</span> 는 <b>설계 추정치</b>다 — 실측 φ_SE 열이 LHS-02 대로 비어 있어서, 어긋남 중 얼마가 추정 오차인지 <b>아직 못 가른다</b>.</p>'),
    ('LHS-05', 'ρ 가 작으니 코호트가 수치적으로 안정적이다',
     'ρ 가 3 % 차단의 20만~42만배 아래니 이 코퍼스의 σ 는 안정적이라고 읽는다.',
     '<b>세 채널의 ρ 를 지배한 케이스가 전부 같은 설계점</b>이다 — φ_SE 0.0916 · am_pct 95 = 코호트에서 <b>SE 가 가장 적은 점</b>.  이온은 <span class="m">lhs00_020</span> 이고 그 σ 는 이온 채널 <b>전체 최소</b>다.',
     ['7.117172448780858e-06', '1.4629494790028302e-05', '1.385157665230787e-05'],
     '⇒ 바른 문장은 <b>"최악의 설계점에서도 그만큼"</b> 이다.  퍼콜 문턱 근처에서 망은 <b>가는 실 하나</b>가 되고, 그때 σ 가 행렬 순서·허용오차에 가장 민감해진다.',
     '<p>★ 채널 최대를 잡는 집계 규약이 <b>의도대로</b> 작동한 것이다 (보수적).  중앙값이나 분포를 보고 싶으면 그것은 <b>다른 양</b>이고 따로 등록해야 한다.</p>'),
    ('LHS-04', '문턱 위면 관통한다',
     'φ_SE 가 평균장 문턱보다 충분히 크면 SE 망은 벽에서 벽까지 이어진다.',
     '<span class="m">lhs00_009</span> 는 φ_SE <b>0.3064</b> 로 문턱 한참 위이고, <b>같은 φ_SE 형제 20건이 전부 뚫리는데 혼자 막혔다</b>.  솔버가 노드 <b>59,616개</b>를 만들고도 관통 성분을 못 찾았다.',
     ['0.3064', '59,616', '2.719', 'bottom=2720, top=4', 'n_components=1', '477분의 1', '1/127'],
     '★★ <b>진단 완료 — 물리가 아니라 경계 규칙이다.</b>  망은 <b>하나로 이어져 있고</b>(<span class="m">n_components=1 · 크기 59,612</span>), 상단 전극으로 뽑힌 <b>4개가 접촉이 하나도 없는 고립 입자</b>다.',
     '<p><b>진단 인쇄</b> (저자 기계, 생산 경로):</p>'
     '<p><span class="m">n_target_nodes=59616 · n_graph_nodes=59612 · n_edges=245707<br>'
     'bottom=2720 · top=4 (plate_z=0.0372)<br>'
     'n_components=1 · top-5 sizes=[59612]<br>'
     'components reaching bottom=1 · top=0</span></p>'
     '<p><b>세 줄이 서로를 닫는다</b> — ① 성분이 <b>하나</b>고 침대 전체를 덮는다 (SE 가 끊긴 게 아니다) ② <span class="m">59616 − 59612 = 4</span> = <b>접촉 없는 고립 입자 정확히 4개</b> ③ <span class="m">top=4</span> 인데 <span class="m">reaching top=0</span> ⇒ <b>상단 전극 4개가 바로 그 고립 입자</b>다 (다른 해가 없다).</p>'
     '<p><span class="m">bottom 2720</span> vs <span class="m">top 4</span> = <b>680배 비대칭</b>.  d_am_p 15 µm 인 침대에서 상단 띠가 큰 AM_P 에 점령돼 SE 가 거의 안 남고, 남은 넷은 압밀 위에 뜬 낱개다.</p>'
     '<p>⇒ 열린 P1 <b>L2-04</b> 와 <b>같은 축의 반대쪽 면</b>이고 <b>실물 증거</b>다.  L2-04 는 경계가 <b>너무 느슨</b>한 쪽을, 이 케이스는 <b>너무 엄격</b>한 쪽을 보여 준다.  ⇒ 등급 P2 → <b>P1</b>.</p>'
     '<p>★★★ <b>범위 확정 — 25건 중 이것 하나뿐이다.</b>  나머지 24건에 같은 진단을 전부 돌렸더니 <b>성분 29~2,324개</b>(중앙 629) · <b>고립 SE 입자 3.2~49.3 %</b>(중앙 20.2 %) 로 <b>진짜 단절</b>이었다.  lhs00_009 는 고립 비율이 단절군 최소의 <b>477분의 1</b>, 성분 수는 <b>29배 아래</b> — 모든 축에서 다른 동물이다.  ⇒ <b>내 걱정은 반증됐다</b>.  경계 규칙이 정의역에서 빼는 것은 <b>1/127</b> 이다.</p>'
     '<p>⛔ <b>이것이 S3 를 멈추지 않는다</b> — 봉인이 OLD_NONE 으로 분류하면 정의역 밖이고 봉인과 ρ 가 일관된 상태다.  경계 수정은 L2-04 의 일이고 <b>세대 2</b> 다.</p>'),
    ('LHS-02', '설계 CSV 의 측정 열은 실측을 담고 있다',
     '<span class="m">phi_se</span> · <span class="m">tortuosity_dijkstra_SE</span> · <span class="m">coverage_AM_*</span> 열이 있으니 실측이 들어 있다.',
     '<b>130/130 전부 비어 있다</b> — <span class="m">_est</span> 추정치만 채워져 있고 측정 쪽은 <b>한 번도 안 채워졌다</b>.',
     ['0 / 130'],
     '그 열을 읽는 코드가 있으면 <b>결측을 만나거나 0 으로 채운다</b> — <b>GAP2-05</b>(결측을 0 으로 채워 양의 주장으로 렌더)와 같은 자리다.  ⬜ 소비자 유무 미확인.'),
    ('R4-08', '양성 대조가 ψ 정정을 지킨다',
     'no-op 변이를 잡으니 대조가 유효하다.',
     '<b>ψ 를 솔버에서 받아 기대식에도 써서</b> 잘못 바뀐 ψ 가 기대값을 <b>같이 움직였다</b> — <span class="m">floor 1e-4→0</span> 과 <span class="m">ψ 지수 1.5→1.0</span> 두 변이가 <b>13/13 초록</b>.  floor 대조 좌표도 실제로는 clamp 라 <b>floor-only 영역을 시험하지 않았다</b>.',
     ['13/13 PASS', '0.102338~0.102633'],
     'ψ 를 <b>기하에서 독립 계산</b>하는 oracle 을 넣고, 변이를 <b>실제로 돌려</b> 확인했다.',
     '<p>두 변이 모두 이제 <b>15/18 로 실패</b>한다.  floor-only 는 실측 띠 <b>0.102338~0.102633</b> 안의 좌표로 옮기고 clamp 경계는 따로 핀해 세 영역이 <b>독립</b> 핀이 됐다.</p>'
     '<p>⚠ clamp 제거 변이는 여전히 초록인데 그건 구멍이 아니라 <b>진짜 no-op</b> 이다 — <span class="m">max(1−s,0)</span> 이 같은 일을 한다.  Codex 도 CONFIRMED 했다.</p>'),
]

# ── 남은 저자 결정 (원장이 못 정하는 것) ──────────────────────────────────────
DECISIONS = [
    ('caps 의 뜻', '<b>전체 접촉면적의 한계</b>인가 <b>추가로 퍼진 막의 한계</b>인가 — 정해지기 전에는 cap_conflict 5.24 % 를 값으로 바꿀 수 없다 (L1-01).'),
    ('lens 의 몫', '정확 교집합을 <b>전체</b>로 쓰나, <b>한 상에 할당된 몫</b>으로 쓰나 (L1-02).  DESC-03 을 고치면 σ 에 들어가는 자리다.'),
    ('flux-tube b', '현행 <span class="m">b = r_min</span> 은 배위수 <b>Z ≈ 4</b> 가정이다.  <span class="m">2r/√Z</span> 로 갈지 — 별도 축, S3 와 섞지 않는다 (AREA-09 7-1c).'),
    ('S3 런', 'ψ 배치 정정은 <b>세대 2</b> 다.  런 전에 수치 재현성 바닥 ρ 를 재고(prereg v2 ⑤) median(|Δ|) 로 세 채널 판정.  예상 부호 <b>상향 가설</b> — cutoff 분기는 반대도 허용 (v3 ⑥).'),
    ('DESC-03', '단위 교란(mm→m)은 σ 를 움직이는 수정이다 — <b>자체 사전등록</b> 뒤에 고치고, 고친 직후 L1-02 를 같은 L1 블록으로 재측정.'),
]


#: 행을 묶는다 — 15행을 한 줄로 늘어놓으면 읽히지 않는다 (id 접두사 → 묶음).
GROUPS = [
    ('L1~L5 스택', '웹앱 계산 스택을 다섯 층으로 나눈 첫 라운드.',
     ('L1-', 'L2-', 'L3-', 'L4-')),
    ('면적 계약', 'L2 판정이 낳은 계약 한 장 — 무엇을 면적이라 부르는가.',
     ('AREA-',)),
    ('SELF · 자기감사', '리뷰가 아니라 우리가 스스로 찾은 것.', ('SELF-', 'DESC-')),
    ('R4 · R5 라운드', 'S3(ψ 배치)를 돌리기 위한 장치를 검토에 부친 결과.',
     ('R4-', 'AREA5-')),
    ('LHS 코호트 판독', 'ρ 런이 127 케이스 × 3 채널에 생산 솔버를 돌린 부산물 — 코호트 자체가 처음 보였다.',
     ('LHS-',)),
]


def _md(t: str) -> str:
    """원장 제목의 **마크다운 흔적**을 HTML 로 — `코드` 와 **굵게** 만.

    ⚠ 원장 제목은 사람이 쓴 문장이라 백틱과 `**` 가 섞여 있다.  옛 판은 `html.escape` 만
      해서 화면에 **백틱과 별표가 그대로** 찍혔다 (2026-09-15 에 1저자가 볼 페이지에서 확인).
    ⛔ 일반 마크다운 파서를 쓰지 않는다 — 제목에 들어갈 수 있는 것은 이 둘뿐이고, 그 밖의
      것을 해석하면 원장 문자열이 조용히 달라 보인다.
    """
    out = html.escape(t)
    out = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', out)
    out = re.sub(r'`([^`]+)`', r'<span class="m">\1</span>', out)
    return out


def _group_of(fid):
    for i, (_t, _s, pref) in enumerate(GROUPS):
        if fid.startswith(pref):
            return i
    return len(GROUPS) - 1


def _sh(*a):
    return subprocess.run(a, cwd=ROOT, capture_output=True, text=True).stdout.strip()


def load():
    d = json.loads(LEDGER.read_text(encoding='utf-8'))
    fs = d['findings']
    by = {x['id']: x for x in fs}
    L = [x for x in fs if re.match(r'^L[1-5]-', x['id'])]
    A = [x for x in fs if x['id'].startswith('AREA-')]
    return fs, by, L, A


def tally(grp):
    c = collections.Counter()
    for x in grp:
        c[x['severity']] += 1
        c['fixed' if x['status'] in ('claimed_fixed', 'verified') else 'open'] += 1
    c['total'] = len(grp)
    return c


def render(nav_home: str = '') -> str:
    """비포/애프터 페이지 HTML.

    `nav_home` 을 주면 **돌아가는 길**을 맨 위에 단다 — 웹앱이 이 페이지를 띄울 때 쓴다.
    ⚠ 이 페이지는 `base.html` 을 상속하지 않는 **독립 HTML** 이라 항해가 없다.  링크를 안
      달면 들어가서 못 나온다 (2026-09-15 에 실제로 그 상태로 붙였다가 잡혔다).
    ⛔ 커밋되는 `docs/` 사본에는 **안 단다** (`nav_home=''`) — 파일로 열 때 `/ledger` 는
      해석되지 않는 죽은 링크다.
    """
    fs, by, L, A = load()
    #  ⚠ R4·R5 라운드는 **집계에 없었다** — 페이지에 그 묶음이 통째로 있는데 머리 숫자가
    #    세지 않아, 읽는 사람이 "고침 17 / 열림 31" 을 전체로 오해한다 (2026-09-15 에 잡음).
    R = [x for x in fs if x['id'].startswith('R4-') or x['id'].startswith('AREA5-')]
    tL, tA, tR = tally(L), tally(A), tally(R)
    head_sha = _sh('git', 'rev-parse', '--short=9', 'HEAD')
    E = html.escape
    o = []
    o.append('<title>DEM 스택 적대 리뷰</title>\n')
    o.append(pathlib.Path(__file__).with_name('_review_page_css.html').read_text(encoding='utf-8'))
    if nav_home:
        o.append('<div style="position:sticky;top:0;z-index:9;background:var(--panel);'
                 'border-bottom:1px solid var(--rule);padding:.55rem 1rem;font-size:.85rem">'
                 f'<a href="{E(nav_home)}" style="color:var(--accent);text-decoration:none">'
                 '&#8592; 판정 원장</a>'
                 '<span style="color:var(--ink-3);margin-left:.75rem">'
                 '요청마다 원장에서 다시 렌더한다 — 낡은 사본이 아니다</span></div>\n')
    o.append('<div class="wrap">\n<header>\n')
    o.append(f'  <div class="eyebrow">Codex 적대 리뷰 · L1~L5 + 면적 계약 · 원장 {LEDGER.name} @ {head_sha}</div>\n')
    o.append('  <h1>DEM 스택 적대 리뷰</h1>\n')
    o.append('  <p class="sub">웹앱의 계산 스택을 다섯 층으로 나눠 독립 검토에 부쳤고, 그 대응이 다시 <em>면적 계약</em> 한 장을 낳았다. '
             '아래는 우리가 믿고 있던 것과, 실제 함수·코퍼스·독립 기준해가 보여준 것이다 — 모든 숫자는 원장에 있고 이 페이지는 거기서 생성된다.</p>\n')
    #  ★ 익명 숫자 8개를 한 줄로 늘어놓지 않는다 — **트랙 × 지표** 표로 읽는다.
    o.append('  <div class="tally">\n')
    o.append('    <div class="th"></div><div class="th">등재</div><div class="th">P1</div>'
             '<div class="th">고침</div><div class="th">열림</div>\n')
    for _nm, _t in (('L1~L5 스택', tL), ('면적 계약 (AREA)', tA), ('R4 · R5 라운드', tR)):
        o.append(f'    <div class="rw">{_nm}</div>'
                 f'<div class="n">{_t["total"]}</div>'
                 f'<div class="n p1">{_t["P1"]}</div>'
                 f'<div class="n fx">{_t["fixed"]}</div>'
                 f'<div class="n">{_t["open"]}</div>\n')
    o.append('  </div>\n</header>\n')

    # 사슬
    o.append('<section>\n  <h2>왜 한 층만 고쳐선 안 닫히나</h2>\n')
    o.append('  <p class="lede">다섯 판정문이 각각 같은 말을 했다 — 앞 층을 고쳐도 뒤 층이 값을 다시 바꾼다. '
             '그래서 이 다섯은 독립 항목이 아니라 <strong>하나의 사슬</strong>이고, 순서가 곧 처방이다.</p>\n  <div class="chain">\n')
    for lv, nm, sub in LAYERS:
        grp = [x for x in L if x['id'].startswith(lv + '-')]
        op1 = sum(1 for x in grp if x['status'] == 'open' and x['severity'] == 'P1')
        opn = sum(1 for x in grp if x['status'] == 'open')
        fx = len(grp) - opn
        st = f'Hold · P1 {op1} 열림' if op1 else ('열림 없음' if not opn else f'P2 {opn} 열림')
        o.append(f'    <div class="link"><div class="lv">{lv}</div><div class="nm">{E(nm)}<br>{E(sub)}</div>'
                 f'<div class="st">{E(st)}</div><div class="nm" style="margin-top:6px">고침 {fx} / {len(grp)}</div></div>\n')
    o.append('  </div>\n')
    o.append('  <div class="caveat"><b>단, 전면 재작성은 아니다.</b> 판정문: <i>"선형대수 엔진 자체의 전면 재작성 근거는 없다 — '
             '분산된 getter·feature·설명 생성부가 문제다."</i>  그리고 오늘 그 엔진 옆에 <b>독립 기준해</b>가 하나 생겼다 — '
             '협착 저항을 문헌 인용이 아니라 직접 풀어서 가른다.</div>\n</section>\n')

    # 반례
    o.append('<section>\n  <h2>믿은 것 → 잰 것</h2>\n')
    o.append('  <p class="lede">왼쪽은 우리가 코드·문서·계약에 적어 둔 것이다. 오른쪽은 같은 함수에 실제 입력을 넣거나, 코퍼스를 세거나, 기준해를 풀어 나온 값이다.</p>\n  <div class="ba">\n')
    _cur = -1
    #  ⚠ 묶음별로 **정렬해서** 돈다 — ROWS 순서를 그대로 쓰면 묶음을 오가며 머리가
    #    여러 번 찍힌다 (실측: 묶음 4개인데 머리 5개).  정렬은 안정적이라 묶음 안 순서는 그대로다.
    for row in sorted(ROWS, key=lambda r: _group_of(r[0])):
        fid, ttl, bef, aft, nums, note = row[:6]
        detail = row[6] if len(row) > 6 else ''
        gi = _group_of(fid)
        if gi != _cur:
            if _cur >= 0:
                o.append('  </div>\n')
            gt, gs, _pref = GROUPS[gi]
            o.append(f'  <div class="grp"><h3>{E(gt)}</h3><div class="gsub">{E(gs)}</div></div>\n'
                     '  <div class="ba">\n')
            _cur = gi
        f = by[fid]
        sev = f['severity']
        fixed = f['status'] in ('claimed_fixed', 'verified')
        tag2 = '<span class="tag FIX">고침</span>' if fixed else '<span class="tag P2">열림</span>'
        cls = 'row fixed' if fixed else ('row p1' if sev == 'P1' else 'row')
        o.append(f'    <div class="{cls}" id="{fid}">\n      <div class="rid">'
                 f'<span class="tag {sev}">{fid}</span>{tag2}'
                 f'<span class="ttl">{ttl}</span></div>\n      <div class="pair">\n')
        o.append(f'        <div class="cell before"><div class="lbl">믿은 것</div><p>{bef}</p></div>\n')
        o.append(f'        <div class="cell after"><div class="lbl">잰 것</div><p>{aft}</p></div>\n')
        o.append(f'      </div>\n      <p class="note">{note}</p>\n')
        if detail:
            o.append('      <details class="more"><summary>자세히 — 근거·한정·이력</summary>'
                     f'<div class="body">{detail}</div></details>\n')
        o.append('    </div>\n')
    o.append('  </div>\n</section>\n')

    # 고친 것 (원장에서)
    o.append('<section>\n  <h2>고친 것 — 원장이 claimed_fixed 로 적은 것</h2>\n')
    o.append('  <p class="lede">전부 <span class="m">claimed_fixed</span> 다 — "정말 고쳐졌는가" 는 회귀와 독립 검증자의 몫이고, '
             '<span class="m">verified</span> 는 구현자와 다른 검증자가 있어야 붙는다.  SHA 는 리포에 실재하는 커밋이다.</p>\n  <div class="fixed-list">\n')
    for x in sorted(L + A, key=lambda z: (z['id'].split('-')[0], int(re.sub(r'\D', '', z['id'].split('-')[1]) or 0))):
        if x['status'] not in ('claimed_fixed', 'verified'):
            continue
        sha = (x.get('claimed_fixed_sha') or '')[:9]
        o.append(f'    <div class="fx-row"><div class="id">{x["id"]}</div><div class="wt">{_md(x["title"])}</div>'
                 f'<div class="sha">{sha}</div></div>\n')
    o.append('  </div>\n</section>\n')

    # 남은 결정
    o.append('<section>\n  <h2>원장이 못 정하는 것 — 저자 결정</h2>\n')
    o.append('  <p class="lede">아래는 값이 아니라 <strong>정의</strong>가 비어 있는 자리다.  정해지기 전에는 코드가 "계측만" 한다 — 기본 동작은 비트 단위로 불변이고, 회귀 핀이 그것을 강제한다.</p>\n')
    o.append('  <div class="decide"><div class="hd">결정 대기</div><ol>\n')
    for k, v in DECISIONS:
        o.append(f'    <li><b>{k}</b> — {v}</li>\n')
    o.append('  </ol></div>\n')
    o.append('  <div class="caveat"><b>오늘 내가 세 번 틀린 자리.</b> 기준해에서 축대칭 면적의 2π 를 통째로 빠뜨렸는데 단조·수렴·극한 검사가 전부 초록이었다(일률 배수는 비를 안 바꾼다) · '
             '회귀 핀을 재지 않고 추측해 적었다 · 감사가 "최종 결속 라벨" 과 "가장 작은 cap" 을 섞어 불가능한 결과를 냈다.  '
             '셋 다 <b>결과가 그럴듯해서</b> 넘어갈 뻔했고, 셋 다 배수·핀·단조성을 <b>실제로 재는</b> 검사 하나가 잡았다.</div>\n</section>\n')

    o.append(f'<footer>이 페이지는 <span class="m">scripts/build_review_before_after.py</span> 가 <span class="m">{LEDGER.relative_to(ROOT)}</span> 에서 생성한다 '
             f'(HEAD <span class="m">{head_sha}</span>).  집계·고친 목록·SHA 는 원장 값이고, 서술이 인용하는 숫자는 selftest 가 해당 항목의 note 에서 찾는다.  '
             f'인용 금지값 스윕(<span class="m">check_review_findings.py --ban-sweep</span>)이 이 파일을 포함한다.</footer>\n</div>\n')
    return ''.join(o)


def _selftest() -> int:
    ok = True

    def chk(name, cond, extra=''):
        nonlocal ok
        print(('  ✓ ' if cond else '  ✗ ') + name + (f'   {extra}' if extra else ''))
        ok = ok and bool(cond)

    print('리뷰 비포/애프터 생성기')
    fs, by, L, A = load()
    page = render()

    # ① 서술이 인용하는 숫자마다 그 항목의 note/title 에 실재한다 (인용이 원장에 닻을 내린다)
    missing = []
    for _row in ROWS:
        fid, nums = _row[0], _row[4]
        hay = by[fid].get('note', '') + by[fid].get('title', '')
        for s in nums:
            if s not in hay:
                missing.append((fid, s))
    chk('① 서술의 인용 숫자가 전부 해당 원장 항목에 실재', not missing, f'{missing}')

    # ② 집계가 원장과 같다 (HTML 안의 tally 숫자를 다시 파싱)
    #    ⚠ 2026-09-15: 머리 집계가 **R4·R5 라운드를 아예 안 세고 있었다** — 페이지에 그 묶음이
    #      통째로 있는데 숫자가 없어, 읽는 사람이 L1~L5 집계를 전체로 오해한다.
    #      ⇒ 트랙 × 지표 표로 바꾸고 이 검사도 **세 트랙 12칸**을 본다.
    R = [x for x in fs if x['id'].startswith('R4-') or x['id'].startswith('AREA5-')]
    tL, tA, tR = tally(L), tally(A), tally(R)
    nums = re.findall(r'<div class="n(?: [a-z0-9]+)?">(\d+)</div>', page)
    want = [t[k] for t in (tL, tA, tR) for k in ('total', 'P1', 'fixed', 'open')]
    chk('② 머리 집계 — 세 트랙 12칸이 원장 집계와 일치 (R4·R5 가 빠져 있었다)',
        [int(x) for x in nums[:12]] == want, f'{nums[:12]} vs {want}')
    chk('②b ★ 그 표가 실제로 R4·R5 트랙을 담는다 (빈 트랙을 성공으로 내지 않는다)',
        tR['total'] > 0 and 'R4 · R5 라운드' in page, f"R4·R5 등재 {tR['total']}")

    # ③ 페이지의 SHA 가 전부 리포에 실재
    shas = re.findall(r'<div class="sha">([0-9a-f]{7,9})</div>', page)
    bad = [s for s in shas if _sh('git', 'rev-parse', '--verify', '--quiet', s + '^{commit}') == '']
    chk('③ 고친 목록의 SHA 가 전부 실재하는 커밋', shas and not bad, f'{len(shas)}개 · 실재 안 함 {bad}')

    # ④ 인용 금지값 스윕 — 생성 파일이 스윕 **범위 안**이고 누수 0
    import importlib.util
    spec = importlib.util.spec_from_file_location('crf', ROOT / 'scripts' / 'check_review_findings.py')
    crf = importlib.util.module_from_spec(spec); spec.loader.exec_module(crf)
    chk('④a 스윕 글롭이 docs/**/*.html 을 포함한다', 'docs/**/*.html' in crf.BAN_SCAN_GLOBS)
    tmp = OUT.with_name('review_before_after.selftest.html')
    try:
        tmp.write_text(page, encoding='utf-8')
        leak = [ln for ln in page.splitlines() if any(b in ln for b in ('+52.0 %', '+42.15 %', 'f_artifact = 0.147'))]
        chk('④b 페이지에 철회 헤드라인 문자열이 없다 (표본 3개)', not leak, f'{len(leak)}줄')
    finally:
        tmp.unlink(missing_ok=True)

    # ⑤ 판별력 — 집계 하나를 어긋나게 만들면 ② 가 반드시 빨간불
    page_bad = page.replace(f'<div class="n">{tL["fixed"]}</div>', f'<div class="n">{tL["fixed"] + 1}</div>', 1)
    nums2 = re.findall(r'<div class="n">(\d+)</div>', page_bad)
    chk('⑤ 판별력: 고침 수를 +1 하면 ② 가 잡는다', [int(x) for x in nums2[:8]] != want)

    # ⑥ 원장 외 손숫자 금지 — ROWS 밖의 숫자를 본문에 새로 적지 않았는지 (초안 낡음의 원인)
    chk('⑥ 결정 목록의 인용(5.24 %)이 원장에 실재', '5.240 %' in by['L1-01']['note'])

    print('리뷰 비포/애프터 생성기 SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description='리뷰 비포/애프터 페이지 생성 (원장 기반)')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--out', default=str(OUT))
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    p = pathlib.Path(a.out)
    p.write_text(render(), encoding='utf-8')
    print(f'→ {p} ({p.stat().st_size:,} B)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
