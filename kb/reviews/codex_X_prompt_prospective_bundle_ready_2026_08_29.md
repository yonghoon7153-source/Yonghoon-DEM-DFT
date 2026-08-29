---
title: "Codex 회신 X 요청 — prospective 번들 40잡, 던지기 전 최종 감사 (실물 첨부)"
date: 2026-08-29
updated: 2026-08-29
tags: [review, codex, sdcp, vasp, prereg, closure, bundle]
status: 발송 대기
confidence: medium
verificationStatus: partial
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 회신 X 요청 — 던지기 전 최종 감사

> 회신 V 때 *"묶음 자체가 첨부되지 않아 해시를 독립 재검산하지 못했다"* 는 지적을 받았다.
> 이번엔 **번들 zip 과 INCAR 전문**을 같이 낸다.

---

## 첨부할 것

1. `/data/work/runs/sdcp_prospective_v1.zip` (0.4 MB · POTCAR 미포함)
2. 아래 명령이 만드는 `INCAR_DIGEST.txt` (전 INCAR + 해시표)

```bash
B=/data/work/runs/sdcp_prospective_v1
{ echo "════════ 파일 해시 ════════"
  find $B \( -name INCAR -o -name POSCAR -o -name KPOINTS -o -name job.json \) \
    | sort | while read f; do
      printf "%s  %s\n" "$(sha256sum $f | cut -c1-16)" "${f#$B/}"; done
  echo; echo "════════ 고유 INCAR 전문 ════════"
  find $B -name INCAR | xargs -I{} sh -c 'echo "── {}"; cat {}' \
    | awk '/^── /{p=$2} {print}' | head -400
  echo; echo "════════ MANIFEST 핵심 ════════"
  python3 -c "
import json; m=json.load(open('$B/MANIFEST.json'))
for k in ('candidate_set','from_basins','d3_off_twins','clean_slab','n_jobs','fragments'):
    print(k, '=', json.dumps(m.get(k), ensure_ascii=False)[:400])"
} > /data/work/runs/INCAR_DIGEST.txt
wc -l /data/work/runs/INCAR_DIGEST.txt
```

---

## 붙여넣을 프롬프트

```
당신은 계산재료 리뷰어다. 회신 W 절차 1~5 를 실행해 **40잡 번들**을 만들었고,
던지기 전에 실물을 감사받으려 한다. zip 과 INCAR digest 를 첨부한다.
GO / 조건부 GO / NO-GO 와 P0(던지기 차단) / P1 로 답해 달라.

━━━ 🔴 우리가 스스로 찾은 P0 부터 ━━━
회신 W 5단계는 *"알려진 **두** magnetic seed 및 최종 국소모멘트 gate"*, P0-2 는
*"각 pose 에서 **최소 두 자기 초기조건**의 최종 topology 를 확인"* 이라고 했다.
그런데 이 번들의 복합체는 **`afm2424_pm1` 하나뿐**이다 (`--both_seeds` 미지정).
clean slab 만 pm1/net4 둘 다 있다.

  · 두 seed 로 가면: 복합체 12 → 24, D3 쌍 포함 **40 → 64잡**
  · 우리 질문: pose×basin 상호작용을 재려면 **전 pose 두 seed** 가 필요한가,
    아니면 **calibration 4 만 두 seed** 로 하고 audit 2 는 pm1 으로 충분한가?
    (audit 은 regret 판정용이라 primary protocol 하나면 된다고 봤는데 확신이 없다)

━━━ 무엇을 만들었나 ━━━
[1단계] UMA 이완 확대 `--top-per-site 16` (양 조각 동일 예산) → 조각당 112 자세.
        sdcp_neutral 통과 109 / 게이트 3 · ptfe_c10 통과 112 / 게이트 0.
[2단계] basin 중복제거 — cutoff 3.2 Å **전체 접촉 graph** + 높이 + PBC 최소이미지
        heavy-atom RMSD(0.75 Å). sdcp 109→101 · ptfe 112→96.
        ⚠ 거의 안 묶인다. 원인 실측: **이완 중 분자 무거운원자 변위가 0.04–0.09 Å**
        (FIRE 는 정상 작동 — fmax 1.13→0.04, ΔE 0.21 eV, 34–45 스텝).
        자세쌍 RMSD 최소 3.33 Å. ⇒ **"basin" 이 과한 표현이고 사실상 "자세" 다.**
[3·4단계] calibration 4 + sealed audit 2 (조각당). audit 은 **창 W0=0.15 바깥**에서.
        층화 난수 seed `20260829` 를 DFT 전에 기록·동결.
        동결 해시 `94675e66e02c855a`, 커밋됨.
[5단계] `--from_basins` 로 **동결본이 지정한 자세만** 생성 (champion/cross 경로 미사용,
        `쌍 0개` 로 확인). `--d3_pairs` 로 각 endpoint 의 D3-off 쌍둥이.

  선정된 것 (UMA E_pose):
    sdcp_neutral  cal b00 +0.0200 · b01 +0.0425 · b07 +0.1661 · b08 +0.1982
                  AUDIT b09 +0.2691 · b62 +0.3856
    ptfe_c10      cal b00 −0.2660 · b01 −0.2603 · b74 −0.1224 · b75 −0.1146
                  AUDIT b76 −0.1119 · b21 −0.1983

━━━ 검증한 것 ━━━
· D3 쌍: `diff` 가 **`< IVDW     = 11`** 한 줄만. POSCAR 해시 동일(675dbbb7…).
· `candidate_set = prospective_lowE (frozen 94675e66e02c855a)` — 동결본과 일치.
· `audit_seed = 20260829` manifest 승계.
· 전 endpoint `LREAL=.FALSE.` · `IBRION=-1` · `NSW=0` · `IVDW=11`(D3-off 쌍은 없음).
· 기체 기준 `NUPDOWN=-1` · `ICHARG=2`(closure 에서 CHGCAR 가 없으므로) · relax 상 없음.
· 기체 비영 MAGMOM 대조 `__nzmag` 포함.
· clean slab 두 조각 동일 `d5f18feb1570`.

━━━ 🔴 우리가 아는 미해결 3 ━━━
M1. **clean slab 이 바뀌었다.** 오늘 재이완한 두 조각은 `d5f18feb`, 8월 11일 그대로인
    두 조각은 `daf71160` 이다. 같은 UMA 모델·task 인데 다르다. **왜인지 모른다**
    (비결정성? 시작구조? fmax 경로?). 이 번들 안에서는 두 조각이 같으니 대비는
    성립하지만, **legacy wave1 값과는 슬랩 기준이 다르다** — 섞으면 안 된다.
M2. **basin 중복제거가 사실상 작동 안 한다** (위 2단계). 회신 W 가 basin 단위 절차를
    설계했는데 우리 풀은 basin 이 자세와 거의 1:1 이다. 절차가 여전히 유효한가?
M3. `box20` 을 뺄지. 회신 V Q3 는 "선행 증거 승계가 machine-readable 하면 생략 가능"
    이라 했는데 우리는 승계를 구현하지 않아 그냥 넣었다 (기체라 싸다).

━━━ 묻고 싶은 것 ━━━
Q1. 위 self-P0(두 자기 seed)의 처리 — 전 pose 두 seed 인가, calibration 만인가?
Q2. M1(clean slab 변경)이 이 번들을 막나? 아니면 legacy 와의 분리만 지키면 되나?
    그리고 재현성 자체를 어떻게 확인해야 하나?
Q3. M2 — basin 이 자세와 1:1 이면 회신 W 의 "4 calibration basin + 2 audit basin"
    설계가 의도한 다양성을 확보하나? calibration 4 의 역할 배정
    (최저 / 다른 지문 최저 / 창 안쪽 경계 / 창 바깥 최근접)이 이 상황에 맞나?
Q4. D3-off 쌍을 **기체·슬랩에도** 만들었다(20쌍). 복합체에만 있으면 되나,
    아니면 A = E_C − E_M 의 양쪽 다 필요한가? (우리는 후자로 봤다)
Q5. 첨부한 INCAR 에 **던지기 전에 고쳐야 할 것**이 있나?
Q6. 우리가 **안 물어본 것 중** 이 번들로 판정 가능한 위험이 있으면 그것도.

━━━ 답변 형식 ━━━
· GO / 조건부 GO / NO-GO + P0 목록 (던지기를 막는 것만)
· Q1~Q6 각각: 답 + 그 답이 틀렸을 때 우리가 관측할 증거 하나
· 마지막에: **실제로 던질 잡 목록**을 명시해 달라 (40 그대로인지, 64 로 늘리는지,
  일부를 빼는지)
```

---

## 배경 (프롬프트 밖)

- 이 번들이 **원고 숫자로 가는 마지막 계산**이다. 회수하면 분석기가 사전등록 판정
  (`min−min` primary · `G` secondary · guard −0.10 eV · 0.01 반올림 · 자기상태 대조 차단)을
  자동 재현한다.
- Q1 이 이 요청의 핵심이다. 우리가 스스로 찾았지만 **범위를 못 정한다** —
  64잡은 40잡의 1.6배이고, 전부 필요한지 아닌지가 예산을 가른다.
