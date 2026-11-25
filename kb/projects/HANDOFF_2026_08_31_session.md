---
title: "인수인계 — 2026-08-31 세션 (외주 C-12 AR→AV · 폴라론 S0 · nscf 사고)"
date: 2026-08-31
updated: 2026-09-03
tags: [handoff, sdcp, c12, polaron, nscf, session, zinc, alzib]
status: 활성
kind: project
system: sdcp
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-31
verifiedBy: agent
explored: false
authoredBy: agent
claimType: mixed
evidenceScope: multi-source-primary
---

> 📍 브랜치 전체 지도: `kb/results/branch_state_2026_08_31.md` (2026-08-31 전수 조사)

# 인수인계 — 2026-08-31 세션

> 이 문서 하나로 이어받을 수 있게 썼다. **§0 을 먼저 실행**하고 §1 부터 읽는다.

## 0. 먼저 — 밀린 것 당기기

```bash
cd ~/Yonghoon-DEM-DFT
git fetch origin claude/friendly-meitner-lldvar
git log --oneline -1                                   # 지금 어디인가
git rev-list --count HEAD..origin/claude/friendly-meitner-lldvar   # 몇 개 뒤처졌나
git status --short                                     # 더러운 게 있나
```

**뒤처진 커밋이 있으면 그냥 당기지 말 것.** 이 세션에서 두 기계가 같은 함정에 빠졌다:

- gabia 가 839 커밋 뒤처진 채로 옛 코드를 돌고 있었다 (`git pull` 이 `cannot pull
  with rebase: You have unstaged changes` 로 **조용히** 실패한 뒤 방치)
- WSL 은 165 커밋 뒤처져 있고 `scripts/heckel_analysis.py` ·
  `make_heckel_manifest.py` · `oat_sensitivity.py` 세 개가 **staged 인데 커밋 안 됨**
  (⚠ 어느 트랙 건지 1저자 확인 필요 — manuscript-track 일 가능성)

정리 순서: `git status --short` → 더러운 게 **실제 작업물**이면 브랜치를 정한 뒤
커밋/이동, 실행 산출물이면 `git stash push -u -m "..."` → `git pull --rebase` →
`git stash list` 로 남아 있는지 확인.

파일 하나만 필요하면 작업트리를 건드리지 말고:

```bash
git fetch origin claude/friendly-meitner-lldvar
git show origin/claude/friendly-meitner-lldvar:<경로> > <출력>
```

**기준점**: 이 세션 HEAD = `895af2ed`, 브랜치 `claude/friendly-meitner-lldvar`.
세션 시작점은 `4934c2e6` (AT 프롬프트) 직후.

## 1. 이 세션에서 한 일 — 커밋 22개

### 1-A. 외주 C-12 (VASP 핸드오프) — AT → v18 → AV

| 커밋 | 무엇 |
|---|---|
| `9ff27e35` | **AT P0-1** 기체 3잡의 정본 그래프가 POSCAR 순서와 어긋나 VASP 전부터 영구 게이트. `_mol_graph_canon(at,0,idx)` + 빌드 preflight 에 **배포 POSCAR 되읽기 대조** |
| `97d48e3f` | **AT P0-2** dense 의 INCAR·k 감사 fail-open. `incar_expected.dense` + KPOINTS 제목에 `phase/k/shift` 실어 정확 대조 |
| `7903ae54` | AT P0-2 음성 6건을 **배포본 분석기 안**(`_selftest_closure`)으로 |
| `f939f159` | **AT P0-3** POTCAR 를 매번 PP 원본에서 재조립 + SHA·TITEL·allowlist 독립 재계산 |
| `7dd0ba3b` | **AT P0-4** seal/attestation schema·불리언·시각 정확 검사 + root seal 없이 attestation 금지 |
| `3d942314` | **AT P0-5/6** launcher 검사 · 잡별 `EXECUTABLE_RECEIPT.tsv` · INT/TERM 진짜 종료 · SEAL/MAKE 도 lock 참여 |
| `3e5ff643` | **AT 해제7** README/SUBMIT 에서 `VASP_CMD=` 대입문·수동 run_job·sbatch 배열 삭제 |
| `c193565f` | **AT Q1/Q2/Q5** `B_num` 오차예산 · 자세 role 분리 · pooled 영구 비인용 · 낡은 claim_policy 삭제 |
| `06902dcf` | AT 해제8 사전등록 `db/properties/sdcp_c12_claim_prereg_2026_08_31.json` |
| `9bbf22de` | **v18 봉인 + AU 프롬프트** |
| `895af2ed` | **AV P0-1** `planned[*].meta` 화이트리스트에 `species_order` 가 없어 root seal 이 실물에서 영구 실패 |

**v18 실물** (gabia `/data/work/runs/sdcp_c12_v18`):
```
ZIP      b094a899cf08919b1be7285fb51715aa7ca8e8ef83687ae4eecd33e0f002529c
MANIFEST d6ce4d943eee842f1307c0ff1b1a253ca93e535a24a57b25a83241dcb1478f00
```
잡 16 · 단계 {1:10, 2:6} · 배포본 selftest 274/274 · D3-off 쌍둥이 0개 ·
분자-이미지 최단(primary) sdcp **4.894** / ptfe **5.646**.
생성 인자는 v17 MANIFEST 의 `generated_argv` 그대로 (`runs/sdcp_c12_2026_08_30/IDENTITY_v18.json`).

⛔ **v18 은 NO-GO 다. 돌리지 않는다.**

### 1-B. 폴라론 S0 (자가도핑 확인 · ORCA) — 회신 T 이행

| 커밋 | 무엇 |
|---|---|
| `689bc1dc` | **생성기·seed 생성기가 둘 다 죽어 있었다** (UnboundLocalError · 4-튜플 언팩). 합성 다이머로 실물 e2e |
| `cf88fb9c` | **T Q4** 4층 판정 (초기 개입 probe · 최종 분해 · 안정성 재판정 · basin 군집). 분석기도 죽어 있던 것(`_spin_block` 리스트를 dict 로) 같이 고침 |
| `f58b8e5f` | census 에 probe 수·총 ORCA 실행수 |
| `42f609a9` | **T Q1** S0 격하판 사전등록 + 거버넌스 결정 등록 |
| `69f75d67` | ORCA `%maxcore` 를 인자로 (6000 하드코딩이 남의 잡을 죽일 뻔) |
| `d6001c96` | **리뷰 요청 U** + 입력 번들 |

**S0 번들** (`bundles/sdcp_polaron_S0_inputs.zip`, gitignore 됨):
```
sha256 39dcc959a7a30cd87e64b8d84fe37b609f4fca2392123cf07e507eeb29ac0c4d
MANIFEST_PILOT e264e5578692599df6702d12e14c4aaf77322a234443b66b6fa65f3eb50c7740
builder 3faca7ced14043848f47250924ff91b3029ef3090d26d416f8b1da65e89c1b72 @ 9bbf22de
```
gabia `/data/work/runs/sdcp_polaron_S0` 에 생성돼 **코어 대기 중** (nprocs 4 · maxcore 3000 = 11.7 GB).
selftest 152건. ORCA 실행 32회 예정 (측정 16 + probe 13 + L 2 + L2 2), Opt 없음.

### 1-C. gap nscf 사고 — **2주를 날린 원인 넷**

| 커밋 | 무엇 |
|---|---|
| `e21eafa3` | 러너가 BTL 미지정 → OpenMPI 가 단일 노드에서 **TCP** 를 골랐고 소켓이 끊겨 31시간 좀비. `--mca btl self,vader` 기본값 + `MPI_OVERSUB` 로 오버서브 끄기 |
| `ea274133` | watch 가 mpirun 런처를 랭크로 세어 오경보 |
| `46eb1067`·`ad0e7835` | watch_gabia `--relax` 로 힘 감쇠 **이력** |

**원인 넷**: ① GPU 가 08-20 에 막혀 CPU 로 갔고 아무도 재확인 안 함 ② 20/20 코어 포화
(랭크 누적 CPU 평균 31~60%) ③ 08-30 09:14 에 죽었는데 31시간 몰랐음 ④ 죽은 이유가
BTL 미지정. **계산이 무거워서가 아니다.**

watch 가 이제 생사를 **판정**한다 — 로그의 MPI 오류 줄 수 + `/proc/<pid>/stat` 을
5초 간격으로 재서 전진한 랭크 수. `ps -o pcpu` 는 **생애 평균**이라 "지금 도는지" 를
못 본다 (이걸로 오판할 뻔했다).

## 2. 지금 열려 있는 것

### 2-A. 🔴 AV 회신 (외주) — P0 4건 중 1건만 이행

원문은 `kb/reviews/codex_AV_reply_c12_v18_2026_08_31.md`. **2026-08-31 후속 세션에서 P0-2~P1-5 전건 이행** (해제조건 ①~⑦ 닫힘). 잔여는 ⑧ — v19 재생성과 실물형 e2e 뿐이다.

| | 내용 | 상태 |
|---|---|---|
| **P0-1** | `planned[*].meta.species_order` 부재 → root seal 영구 실패 | ✅ `895af2ed` |
| **P0-2** ✅ `1b3fbefc` | launcher 우회가 **여전히** 뚫린다: `mpirun -np 48 other_vasp`(PATH) · `/tmp/evil/mpirun -np 48`(basename 만 봄) · `env --split-string=...`. `run_job.sh` 를 직접 부르면 lock·봉인·receipt 를 전부 우회. receipt 를 analyzer 가 **한 번도 안 읽음** | ✅ |
| **P0-3** | `closure_C3()` 가 clean slab 0개 번들에서 clean slab 을 요구. 빼도 `vacconv` c2 를 일반 pose 로 세어 조각당 3행 vs 기대 2행 → `unresolved`. **C3 는 slab Edisp 가 소거되므로 잡 추가 불필요** — `vacconv` 제외하고 `(Edisp_C,sdcp − Edisp_G,sdcp) − (Edisp_C,ptfe − Edisp_G,ptfe)` 를 직접 계산. `closure_C1()` 도 같은 문제 → 필요 없으면 명시적 `n/a` | ⏳ |
| **P0-4** | 반송 계약이 셋(README·MANIFEST·SUBMIT)이 서로 다름. 실제 필요: dense 두 상의 `dense/OUTCAR` · 부모/canary 의 실행된 `static/POSCAR` · 수정 후 `EXECUTABLE_RECEIPT.tsv`. 그대로 반송하면 `KCONV_NOT_MEASURED` 또는 `CANARY_GEOM_UNCHECKED` | ✅ `4aed52ff` |
| **P1-5** | `B_num` 문구와 코드가 **반대**. 문구는 "넘어도 raw D 보존, 0.01 eV 주장만 철회" 인데 코드는 estimand block 으로 넣어 D 계산 전에 `NO_VALUE`. 결과 객체가 없는 축이 `missing_axes` 에 안 들어가는 경로도 있음 | ✅ `290513d3`+`ddc6d7ca` |

**P1-5 처방** (리뷰어 문구):
- 입력·상태·provenance 가 유효하면 `D_raw` 와 축별 변화 **보존**
- `B_num > 5 meV` 이면 `citable_at_0.01eV=false`
- `[D−B_num, D+B_num]` 이 0 이나 사전 guard 를 가로지르면 방향 결론 `NO_CLAIM`
- 축 결측·상태 전이·기하/계약 실패일 때만 estimand 자체를 `NO_VALUE`
- `B_num` 을 "총 오차 상한" 이 아니라 **"시험한 세 축의 보수적 sensitivity envelope"** 로 부른다

**재승인 해제조건 8** (원문): ① root-seal 계획 variant 를 실제 job 스키마에서 계산
② launcher 고정 argv + direct `run_job.sh` 차단 + receipt hard gate
③ production 의 `.SELFTEST_FIXTURE` 우회 제거 ④ C3 에서 clean slab·vacconv 의존 제거
⑤ `D_raw` 와 0.01 eV 인용 자격 분리 ⑥ README·MANIFEST·SUBMIT 반송 목록·용어 통일
⑦ 철회했다던 "공통 주기영상 항 소거" 문구 삭제 ⑧ 새 ZIP/MANIFEST 로 실물형 e2e 재검증

**AV 의 Q 판정 요약**: Q2 우리 판단 맞음(pooled 는 basin 분리·재정의 필요, 영구 비인용
유지가 안전) · Q3 5 meV 초과가 곧 폐기는 아니나 소수점만 줄이는 것도 불충분 ·
Q4 detached signature 는 선행조건 아니나 **runner 가 실제 ZIP 경로를 직접 해시하고
외부 anchor 검사를 SEAL 앞에** 두어야 함 · Q5 이름 목록은 좁아도 됨, 문제는 **인자
문법이 넓은 것**, `env` 제거 · Q6 신규 VASP 잡 불필요, analyzer·runner·반송계약 수정과
재생성만 필요

### 2-B. 폴라론 S0 — U 리뷰 발송 대기/진행

`kb/reviews/codex_U_prompt_polaron_S0_2026_08_31.md` + 위 ZIP. 회신 오면 이행.
⚠ **실물 ORCA 미검증** — `%loc` 출력 형식 · `Rotate` 동작 · `NoIter` probe 가 스핀
인구를 찍는지 전부 모른다. phase L 첫 실행이 곧 smoke test.

### 2-C. 돌고 있는 것

| 어디 | 무엇 | 상태 |
|---|---|---|
| gabia CPU | `gap_nscf` modelc nscf **재시작** (`--mca btl self,vader`, np 10 -nk 10) | 08-31 16:51 시작. `CPU 전진 10/10 ✅`. comp1 은 이미 `JOB DONE` (gap 2.0656 = 재현 목표 일치) |
| gabia GPU | Li₃Nd P0-2 control `li3nd_mp-976264_p333_r0..r3` (rattle) | r0 ✓(무섭동 기준, 1스텝) · r1·r2 진행 · **r3 미착수**. ⚠ r1(−14652.03534)·r2(−14652.03576)가 r0(−14652.03511)보다 **낮다** = r0 는 정지점이지 최소가 아니다. 8.8 meV/108원자 = 0.08 meV/원자라 잡음과 구별 안 됨. **결정적 관측량은 에너지가 아니라 Nd 변위 패턴** — r1~r3 가 서로 같은 방향인지, 공공 계산의 재배열과 같은지 |
| gabia CPU | ORCA Stage A gs0..gs7 (중성 8개) | DONE 2 · gs2 진행. ⚠ **gs2 가 gs0 보다 137 meV 낮다**(미수렴). S0 은 gs0 로 간다 — 지금 갈아타면 사후선택. 8개 완주 뒤 확장 규칙이 흡수 |
| kgy | LPSOCl 3×3×1 MD | DONE 8/9, T800_s4 진행. T800 끝나면 ① 아레니우스 직선성 ② 두 구간 Ea 양립 ③ 가중 3점 적합. **그 전에 `msd_diffusive_check.py --mto --scan` 으로 D_inc plateau 먼저** |
| gabia | 폴라론 S0 | 번들 생성 완료, **코어 대기** |

## 3. 이번 세션에서 배운 함정 — 재발 방지

1. **픽스처 ≠ 실물.** 이 세션에서 같은 실패가 **세 번** 났다: AT P0-1(기체 그래프),
   AV P0-1(`species_order`), 그리고 새 게이트가 픽스처의 정상 잡을 막은 것.
   ⇒ **빌더가 실제로 만든 산출물**로 시험한다. 손으로 만든 dict 는 그 모양이 실물에
   있는지부터 확인한다.
2. **함수를 부르지 않는 selftest 는 그 함수가 죽었는지 모른다.** 폴라론에서 생성기·
   seed 생성기·분석기가 **셋 다** 예외로 죽어 있는데 40건이 전부 통과했다.
3. **`potcar_identity_gates` · `phase_gates` · `_final_verdict` 는 배포본 분석기
   함수다** — 생성기 selftest 스코프에 없다. 이걸로 `NameError` 를 **세 번** 냈다.
   배포본 시험은 `_selftest_closure` 안에 넣거나 `_ns[...]` 로 부른다.
4. **`ps -o pcpu` 는 생애 평균이다.** "지금 도는지" 는 `/proc/<pid>/stat` 를 두 번
   재야 안다.
5. **`grep -c` 는 0건에도 "0" 을 찍고 exit 1** 이다. `|| echo 0` 을 붙이면 `"0\n0"` 이
   되어 숫자 비교가 깨진다.
6. **생성기가 ZIP 을 이미 만든다.** `rm -f *.zip` 후 재압축하라고 시키지 말 것
   (gabia 에 `zip` 이 없어 산출물을 날렸다).
7. **`%maxcore` 는 proc 당 MB** 다. `nprocs` 를 곱해야 총량이다.
8. **단일 노드 MPI 는 `--mca btl self,vader`.** 안 정하면 TCP 를 골라 조용히 죽는다.

## 4. 다음 한 수

1. **AV P0-2** launcher 자유형 폐지 → `VASP_LAUNCHER_KIND`(mpirun|srun|none|wrapper) +
   `VASP_NPROC` 로 argv 를 러너가 조립. `env` 제거. `run_job.sh` 는 lock-owner 토큰
   없으면 거부. phase 직전 VASP 해시를 root seal 과 hard gate. receipt 를 analyzer 가
   **읽고** 필수 반송물로.
2. **AV P0-3** `closure_C3` 에서 clean slab·vacconv 의존 제거, Edisp 이중차분 직접 계산.
   `closure_C1` 은 필요 없으면 `n/a`.
3. **AV P0-4** 반송 목록을 세 문서에서 **한 곳**으로 통일.
4. **AV P1-5** `D_raw` 와 인용 자격 분리.
5. **해제조건 ③ `.SELFTEST_FIXTURE` production 우회 제거**, ⑦ 문구 삭제 확인.
6. v19 재생성 (gabia, v17 `generated_argv` 그대로) → AW 프롬프트.

⛔ **v18 을 돌리지 않는다.** 계산 추가는 필요 없다 — analyzer·runner·반송계약 수정과
재생성만이다 (AV Q6).

## 5. 지켜야 하는 것 (이 세션에서 확인된 것만)

- 브랜치 `claude/friendly-meitner-lldvar` 에만 커밋/푸시. PR 금지.
- 커밋 메시지에 모델 ID 금지.
- 원고·슬라이드·사용자 설명에 `estimand` · `claim ceiling` · 코드 필드명을 쓰지 않는다
  (코드 내부 이름으로만 유지).
- doped 마감(`db/properties/sdcp_doped_closed_2026_08_28.json`)의 금지 서술은 구속력이
  있다 — **"무선호" 도 자리선호 방향 서술이라 금지**. MLIP 스크린의 doped 부분은
  원고에 안 쓴다.
- pooled 최솟값·`secondary_G` 는 **영구 비인용** (AV Q2 로 확인됨).
- 원격 작업은 "붙여넣기 블록 제공 → 사용자 실행 → 출력 회수". ssh 로 감싸지 않는다.

---

## 6. 추가 — 2026-09-03 세션 (Zn ALZIB 스코핑)

앞 세션 토큰 소진 후 이어받은 짧은 세션. **계산은 하나도 돌리지 않았다.** 한 일은 둘.

### 6.1 세미나 PDF 판독

`2026.09.02 …pdf` (Kyungrok Do, "Pre-conditioning Strategy for Highly Reversible
Anode-Less ZIBs", Weekly Report @BML). PDF 는 repo 밖.

⚠ **PDF 읽기 — 2026-09-03 정정. 앞서 "PDF 라이브러리를 못 쓴다" 고 쓴 것은 틀렸다.**
`pip install` 은 실제로 안 된다(`cryptography` 가 `pyo3_runtime.PanicException`).
그런데 **pdfminer 는 이미 설치돼 있었고**, pdfminer 가 cryptography 를 쓰는 곳은
*암호화 PDF 복호화 하나뿐*이라 그 모듈만 스텁으로 막으면 정상 동작한다.
→ `tools/litdb/pdf_text.py` (승격 완료, selftest 27개). 기본 백엔드 pdfminer, 폴백 stdlib.

실측 차이가 크다 — Wiley 논문 1편에서 stdlib 스캐너는 **367자(워터마크만)**,
pdfminer 는 **39,482자(본문 전체)**. Wiley/Elsevier 는 본문이 Form XObject 안에 있어
stdlib 백엔드로는 워터마크만 나온다. **stdlib 로 뽑은 결과를 논문 내용으로 믿으면 안 된다.**

이 환경에 없는 것: poppler(`pdftotext`·`pdftoppm`), mutool, gs, qpdf → Read 툴의 PDF
페이지 렌더링도 안 된다. **스캔/이미지 PDF**(`/Font 0`)는 텍스트가 아예 없으므로
내장 JPEG(DCTDecode)을 바이트로 뽑아 이미지로 Read 하는 우회가 필요하다.

### 6.2 기여 스코핑 카드

`kb/projects/zn_alzib_dft_md_contribution_2026_09_03.md` — 발표자가 **스스로 미해결로 표시한
구멍 7개(G1–G7)** 에 우리 기존 기계를 대응시킨 제안서. 계산 7개(C1–C7), 각각 "못 하는 것" 명시.
권장 순서 **C1(상 지문표) → C2+C3(zincophilicity + ΔG_H*) → C6 → C5(ORCA 용매화) → C7(MD)**.

**상태: proposal.** estimand 카드 미작성, `db/governance/decisions.json` 등록 없음,
BML 과 협업 합의 없음. 착수하려면 그 카드의 §4 게이트부터다.

⚠ 주의할 점 둘:
- `kb/elements/Zn.json` 은 **황화물 SE 도펀트 관점**으로만 쓰여 있다. 수계 Zn 금속 음극
  맥락으로 그대로 인용하면 안 된다.
- 세미나 수치(CE 77.8→98.1 % 등)는 **발표자 값**이다. 우리 db 절대값과 섞지 않는다
  (문헌 수치 규율과 동일).

### 6.3 이 세션에서 **안 건드린 것** — 그리고 §1–§4 는 이미 낡았다

이 Zn 세션은 C-12 · S0 를 전혀 손대지 않았다.

⚠ **§1–§4 는 2026-08-31 시점 기록이다.** 그 사이 다른 세션이 훨씬 멀리 갔다:
C-12 는 **v30 / 회신 BF** 까지, 폴라론 S0 는 **회신 Z-2** 까지 이행됐다
(`c895bbb4` · `341e0d7e` 등). 따라서 §4 "다음 한 수" 의 AV P0-2/3/4 · P1-5 항목을
그대로 집어들면 안 된다 — **`git log --oneline -30` 과 `kb/reviews/` 최신 회신부터
확인**하고, 남은 것이 무엇인지는 거기서 다시 읽는다.

Zn 은 별개 트랙이고 외주 C-12 의 우선순위를 밀지 않는다.
