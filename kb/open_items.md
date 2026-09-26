# 미결 리스트 (Open Items)

> 세션이 바뀌어도 유지되는 미결 사항 추적. 닫을 때 날짜+근거를 남기고 ✅로 옮긴다.
> 등록: 2026-07-27 (MAX 감사 후속).

## ⏭ 다음 세션이 **바로 이어서 할 것** (2026-08-28 등록 · **최종 갱신 2026-09-26 저녁 — ⏭-NOW-x 가 최신 (A′ S4-1 첫 잡 실패 → 개정 2 쌍극자 구간 · S3v2 proposed · 탄성 modelc_2x 재개 · Oginni 리뷰 digest). 앞 블록 ⏭-NOW-w 는 09-24 아침 (li2s 유리 MD: seed5 · 파일럿 · final.xyz=relax 정오 · SE|SE V100 · b2o3 s6 kgy · Nd k-탐침 · webapp 점착 화면 · BW 결정 3건). 앞 블록 ⏭-NOW-v 는 09-22 낮(논문 4편 · 원장 정정 3건), ⏭-NOW-u 는 같은 날 오전**)

> 순서가 있다. 앞이 끝나야 뒤가 뜻이 있다.
>
> ⚠ **이 절의 상태 문장은 실측으로만 쓴다.** 2026-09-07 까지 여기 머리가 "ORCA 8잡 실행 중"
> 이었는데 같은 날 실측은 **프로세스 0개**였다 — 워처·기억이 아니라 `ps`·receipt·git log 로
> 받친다(`kb/projects/restart_runbook_2026_09_07.md`). 세션을 닫을 때 이 절을 갱신한다.

### ⏭-NOW-x. 2026-09-26 저녁 — **A′ S4-1 첫 잡 실패(기술) → 개정 2 · S3v2 비준 대기 · gabia 탄성 재개 · 논문 에이전트 1편**

- 🔴 **A′ (W_ad · 사용자 1저자) — S4-1 `V2_top_fcc_relax` (V100 · 00:17–03:12 UTC · 10069 s) 가 nstep 200 을 헛돌았다**: 199/199 스텝 `energy_new > energy_old` · bfgs 이력 초기화 22 회 ·
  Total force 0.1297–0.1322 Ry/Bohr 제자리 · 고정 Ag 바닥층 3 원자(z 0.50) 에 **+0.195 Ry/Bohr 씩 같은 +z 힘** = 에너지·힘 불일치. 러너는 "미완료 · 뒤 잡 안 돌림" 으로 멈춤 (뒤 3 잡 미착수 · GPU 유휴).
  · **원인** = 쌍극자 보정 톱니 불연속 구간 `[c−1.5, c−0.5] Å` 가 기판 바닥층의 **주기 영상(z = c+0.5) 1.0 Å 아래** — QE 문서 *"change of slope must be located in the empty region, or else unphysical forces"*.
    종전 `make_endpoints` 검사는 흡착층 쪽만 보고 `empty_in_both_endpoints: True` 를 **상수**로 적었다 (한쪽 검사 + 상수 깃발 · 내 설계 오류 · `silent_wrong_path` 사례 8).
  · ✅ 고침 `build_aprime_interfaces.dip_region` (집합의 진공 중앙 · 양쪽 핵 ≥ 4 Å · 폭 1 Å · 미달 SlabError · selftest **26/26** · s3 **16/16** · 음성 3) → **S3v2 패키지** `db/inputs/wad_aprime_s3v2_2026_09_26`
    (구조 sha 38 = v1 동일 · pw.in 38/38 emaxpos/eopreg 만 · 후보 9 여유 4.0/4.0 Å · manifest `069894c6…`). v1 패키지는 보존 · 실행 금지.
  · 📄 **개정 2** `wad_aprime_pilot_prereg_v5_amendment_2_2026_09_26.json` · **S3v2 봉인** `wad_aprime_s3v2_seal_2026_09_26.json` · 결정 `D-2026-09-26-wad-aprime-amend-2-dipole-region` ·
    `D-2026-09-26-wad-aprime-s3v2-seal` — ✅ **1저자 '비준' (09-26 저녁)** → 전부 active · 개정 2 digest e2bec8f0a7f9eac0… · 봉인 v2 6df8c01382a17b61… · v1 봉인 결정 superseded. 진단 기록 `db/raw/wad_aprime_s4_v2_2026_09_26/…_fail1_dipreg_diag_2026_09_26.json` (실패 실행 값 사용 금지).
  · ⏭ 비준되면: 개정 2 · 봉인 v2 · 결정 2 를 active/ratified 로 (digest 기입 · v1 seal 결정 superseded) → 커밋·푸시 → **V100 코드 갱신은 kgy `v100-serve` 경로** (kgy fetch → update-ref → V100 `git archive | tar`) →
    V100 에서 실패 폴더 `V2_top_fcc_relax_fail1_dipreg` 보관 확인 → 러너 `IN=db/inputs/wad_aprime_s3v2_2026_09_26/qe` 로 4 잡 재발사 → **재개 규칙**(첫 10 BFGS 스텝 Total force 감소 · energy_new < energy_old 다수) 확인.
  · ⚠ V4 GPU 시험(gabia) 은 **탄성(modelc_2x · 41 GB) 이 끝난 뒤** — GPU pw.x 둘을 겹치지 않는다.
  · ✅ **S4 V2 결과 (09-26 22:4x)** — `db/properties/wad_aprime_pilot_result_v2_2026_09_26.json` (citable false): registry 4 W 폭 0.0004 · d₀ 격자 안 국소 최소 · **G3 FAIL**(직접 8→10 Å ΔW > 0.01 · D3 꼬리) · **G4 수치 미검증(k)** · e70·smearing ½ 통과 · UMA Δ 참고. ⚠ 첫 집계의 끝점 조각 문턱 오독 정정(조각 = V3·V4 모델). ✅ 1저자 '권장하는걸로' (09-26): 8 Å 값 + G3 FAIL 라벨 + 10 Å 병기 · 게이트 읽기 확정 · DEM 회신 5 발송 ✅ → **DEM 5차 회신 수령**(V2 두 값·라벨 수령 · SE 쌍 보류 확정 · 질문: 48 GB 안의 더 작은 SE 소모델 → **프로브 3 변형 전부 불합격(61–80 GB) · 없음 확정** · 회신 6 발송 ✅) · 결정 `D-2026-09-26-wad-aprime-v2-report`. ✅ **DEM 6차 확인 수령 (09-26 밤)** — SE 쌍(질문 ①) 보류 유지 · Ag–C 두 값(라벨 그대로)으로 질문 ② 기하(Ag–C ↔ VGCF 호스트)부터 설계 · C–C 쌍은 DEM 쪽 문헌 카드 · 벤젠 조각 참고로 수령 → **열린 질문 0** (원문 `wad_dem_reply_draft_2026_09_23.md` §DEM 6차 확인). 🟡 **V4 GPU 시험 대기 (09-26 23:50 → 09-27 재발사)** — 패키지 `db/inputs/wad_aprime_v4_gpu_trial_2026_09_26` (far 셀 · G3 c+2 셀 · 52 Ry · electron_maxstep 2) · gabia tmux `v4trial` · worktree `/data/work/repo_wad` · `WAIT_PIDS=248767`(23_p) · START 2048 · KILL 44,000 · 런 `/data/work/runs/wad_aprime_v4_trial_2026_09_26` · DRY_RUN ✓ (PP 6 해시 · GPU 런타임). ⚠ **결과 전 정정**: 첫 발사판은 calc=scf 라 첫 시험 뒤 러너가 멈출 판이었고 PASS 의 'rc 0' 도 틀렸다 (잘린 SCF = exit 2) → calc probe · rc 판정 제외 · 러너 ⑪ 가드 (조용히 틀린 경로 10번째). 판정 = 완료(probe 규칙) · killed 0 · peak ≤ 44,000 → 그 셀 종류 본 잡. ⏭ **DEM 에 남은 인계 1 건 = V4_s_outer_A 9 잡**(gabia · GPU 시험 `electron_maxstep 2` scf → 피크 ≤ 44,000 MiB 면 본 실행 · CPU 추정 33.6/35.4 GB @52 Ry · 순서 bound·far → G3 3 → G4 k1 2 · s05 2 · e70 은 RESOURCE_BLOCKED) — 조각 모델이라 G3/G4 는 ΔE_frag 변화 5·10 meV · eV/조각 · J/m² 환산 금지.
  · ✅ **S4-1 완료 (09-26 19:16 · V100 · S3v2)** — 4 잡 모두 1 BFGS 스텝에 수렴 · 톱니 진폭 0.0035 Ry · 재개 규칙 통과. ✅ 원출력 회수 (43cf9c6fe) · ✅ `--v2_ed` ×4 → `db/inputs/wad_aprime_s4_v2_stage2_2026_09_26` (29 잡 · d₀ 3.3017/3.3045) · **부록 봉인 ✅ 비준** (`wad_aprime_s4_v2_stage2_seal_2026_09_26.json` · 9085cb4aec2bf184…) → kgy serve → V100 29 잡 실행 (tmux `s4v2c` · 4 세트 순차) → S4 집계기(미작성) → G3·G4 판정 · 결과 기록.
- ✅ **b2o3 사건빈도 — 15 런 통합 완료 (09-26 22:3x)**: kgy s5 3/3 끝 → gabia `s5.incoming` rsync → `rsync -c --dry-run` 빈 출력(바이트 동일) → 막는 파일(107 B) `s5.blocker_removed_0926` 로 치우고 mv → **s2–s6 전부 3/3 msd.json + ensemble** (s2·3·4 gabia · s5·6 kgy · 개정 1·2).
  ⚠ 카드대로 다음은 **전도도 자격(--mto)이 아니라** ① 무효조건(512 · [2,2,1] · 조성 · 400 ps · save_fs 100 · turbo 전 15 런) ② 런마다 `framework_site_census.py --card lpsocl_box331_closure_amendment_2026_09_11.json` ③ 온도별 사건 빈도(Garwood 95 % · 0 이면 단측 상한) · k/5 · t₁ 중앙값(절단) · 움직인 원자 비율(P 32 · 자유 S 48 · Cl 64) · 겉보기 활성화는 10 사건 이상 온도 2 개 이상일 때만. ⛔ D·Ea·σ 재개 금지 (카드 금지 서술).
  ✅ **결과 (09-26 23:0x)** `db/properties/b2o3_framework_event_rate_result_2026_09_26.json`: 무효 0 · P 결합 음이온 이탈 **0** (15 런) · 세 온도 모두 사건 있음 (자유 S 42–71 · Cl 8.5–52 · P 중심 2–19 /ns/셀 vs 대조군 0 · 상한 0.75) · ⚠ 과분산(분산/평균 2–17) · 650 K 비단조 · 겉보기 활성화 χ²/dof 15·33 (서술). 봉인 문장만 인용.
- ⏭ **탄성 modelc_2x (사용자 1저자) 재개 — 1저자 09-26 "b2o3 끝나서 modelC 영률 다시 이어가자"** (09-23 순서 b2o3 → 탄성 → Li₂S 그대로). 러너 `run_elastic_relaxedion_gabia.sh`
  **`SYS=modelc_2x` 명시**(09-23 함정: SYS 없이 comp2 기본값으로 대기했었다) · 수렴점 skip · 소진점(23_p 등) nstep 200 · trust 0.05 재실행 · VRAM 가드 32000 · host 30 GB.
  ✅ **발사 09-26 18:11:49** (tmux `el_mc2x` · repo `/data/work/repo` @30e1e90eb · 로그 `/root/logs/el_modelc2x_0926.log`): 점검 = GPU 1 MiB · host 55 GB · 러너 최신판 ✓ · V0 ✓ · 6/12 수렴 ·
  `23_p` 옛 .out → `strain_23_p.out.exhausted_0926_1811` 보관 · **`restart_mode='restart'`(BFGS 이력 승계) · nstep 200 · trust 0.05** · 18:19 실측 SCF 11 반복 · pw.x **30,018 MiB**(PID 248767).
  남은 순서 23_p → 23_m(찌꺼기 덮어씀) → 13_p/m → 12_p/m → 12/12 면 fit → `elastic_fit.txt` 붙여받기. watch: `ALL=1 bash tools/elastic/watch_elastic.sh`.
  ⏸ **러너 동결 (09-26 밤 · 1저자 'stop해도돼' + '아쉬운데' → 23_p 는 끝까지 · 다음 점은 V4 뒤)**: 23_p pw.x **248767** 은 계속 (bfgs 55 · Total force 0.0048 · 5h43m) ·
  러너 스크립트 bash **248598** 만 STOP (창 셸 248597 까지 STOP 하면 tmux 가 CONT 해서 두 번 헛발질 — CLAUDE.md 공통). 23_p 가 끝나도 23_m 을 안 띄운다.
  ▶ **재개 = `kill -CONT 248598`** (V4 가 GPU 를 비운 뒤 · cmdline 이 run_elastic_relaxedion 인지 먼저) — 러너가 23_p 상태(수렴이면 skip · 소진이면 FAIL 표시)를 보고 23_m 부터 이어 간다.
  ⚠ watch 의 "진행 strain_23_m · 반복 1" 은 **9일 전 찌꺼기 파일**이다 (진행 점을 마지막 '진행' 파일로 고름) — 진짜 도는 점은 23_p. watch 고칠 것.
  ⏹ **분할 취소 (09-26 밤 · 1저자 'v100 관련해서 안 옮겨도 돼')** — 탄성은 gabia 에서 끝까지. 아래 패키지는 만들어 뒀지만 **미사용**. 옛 계획:  strain_12_p · 12_m 을 **V100** 에서 (`db/inputs/elastic_modelc_2x_split_2026_09_26/qe` · gabia 러너 패치본 그대로 · PP sha 4 종 정본 일치 · run_sese_gpu.sh · KILL 32,200 MiB — gabia 실측 30.0 GB 라 빠듯). ⚠ **gabia 가 12_p 에 닿기 전에** V100 pw.out 을 gabia `$WORK/strain_12_{p,m}.out` 로 넣는다 (안 넣으면 gabia 가 다시 돈다).
- 🟢 **li2s 회신 CC 후속 (09-26 저녁 · 추석 끝 · 사용자 '바로 하면 됨')** — B 실측 3 건 ✅: T550 β STO 0.805 · MTO 0.856 · **σ(β) 0.010** (b=12 · 사다리 성김) → STO 는 '경계·구분 불가' · T400 β 0.641 = 9.9 σ 아래 · seed5 궤적: P30 이 49 ps(용융)에 S32 잃고 PS₃ · S–S 는 388 ps 냉각 중(설정 912 K) S54–S59 **P30–S59–S54 말단 과황화** · 300 K 까지 97.9 % 유지 (raw `db/raw/lpscl_smallcell_glass_cc_2026_09_26/seed5_ss_event_cc.json`).
  기록 `db/properties/lpscl_smallcell_glass_md_cc_followup_2026_09_26.json` (B1–B3 · A1 C2 원인별 · A2 점유환산 장부 67.4 h vs 벽시계 156.9 · A3 카드 개정 초안 9 항 · C 400 K 연장 미결). ✅ **C 채택 (사용자 '채택 ㄱㄱ' · 400 K prod **800 ps** · 파일럿 재실행 → 재판독 → 본 런)** · 개정 초안 `lpscl_smallcell_glass_md_amendment_cc_2026_09_26.json` + 결정 `D-2026-09-26-lpscl-smallcell-glass-amend-cc` (proposed · 외부 1저자 확인 대기) · **최종 보고판 `kb/projects/li2s_glass_external_first_author_report_2026_09_26.md`** (4 수정 반영 · Q-CC-1~3) → ⏳ 사용자 검토 → 발송 → 회신 CD. 🟢 **파일럿 400 K 800 ps 발사 (09-26 20:11 · kgy tmux `gp400x` · PID 2826487 · 초기구조 relax 판 final.xyz f7d95f98… · run_meta 무효조건 전건 ✅ · 3-way 공유라 ≈ 1 일)** → 끝나면 `--beta_boot` 재판독(추정자 둘 다) → 본 15런은 회신 CD 뒤.
- 📚 **논문 에이전트** — Oginni et al., *Next Materials* 13 (2026) 103432 (리뷰 · 계산 설계 방법론) → litdb-curator 진행 중 (inbox `0926-1.`) → 끝나면 litdb 파일만 커밋.

### ⏭-NOW-w. 2026-09-23 새벽 — **SDCP/PTFE 세미나 정리 · [Li26MCI] 병합 · 🔴 웹앱 cascade 화면이 어제부터 닫혀 있다**

- 🟢 **li2s 소셀 유리 MD (⛔ 외부 1저자 트랙 · 사용자 'ㄲ' = 실행 승인만) — 2026-09-24 아침** · 카드 `lpscl_smallcell_glass_md_estimand_2026_09_21.json`
  · 담금질: seed1·2 kgy ✅ · seed3·4 gabia ✅ (09-24 05:04 · 1050/1050 ps) · **seed5 gabia 발사 블록 전달** (tmux `q5` · `/data/work/repo` ·
    도구 sha `d94403bc1d61fbce` = seed3·4 와 같은 코드) → ⏳ plan.json 대조 (seed3 대비 차이 = `seed` 하나여야).
  · 🔴 **발견 — `final.xyz` 는 relax 본이다** (`run_melt_quench` 가 FIRE fmax 0.05 · 고정셀 **뒤에** 쓴다 · 개정 ③ 과 plan.json 은 원래 그렇게 적었다).
    카드 해명 1 의 *"final.xyz = 원시 · 게이트 A 는 원시에서"* 가 틀렸다 → 정오 기록 `lpscl_smallcell_glass_md_gateA_erratum_2026_09_24.json`
    (카드는 안 고친다 · 지문 1e35b1e7). seed1 기준값(ρ 1.6212 · PS₄ 1.0 · 최단 2.037 = P–S)도 relax 본 · 밀도 칸은 **문턱이 없다**.
    ⇒ 게이트 A 는 **두 판 다 재고 판정은 외부 1저자에게** (Q1–Q5). 새 플래그 `melt_quench_uma.py --seed_gate` (원시·relax 두 판 · `md_init_raw.xyz`).
  · 🟢 **파일럿 2런 kgy 발사 (09-24 오전 · tmux `gp400` · `gp550`)** (seed1 · 400/550 K · 400 ps · turbo · 초기구조 **원시 잠정**
    `md_init_raw.xyz` sha `573371c2…` · `--seed 1` → 난수 401/551 · GPU 여유 ≥ 9 GB 가드 통과 · worktree `~/li2s_glass_src` @3b0338081)
    `~/work/runs/lpscl_glass_md_2026_09_24/pilot/T{400,550}` — ✅ **run_meta 무효조건 전건 통과** (PID 1760069 · 1760075 · turbo · free-S=0 Cl=12 ·
    kgy 16.2/24.6 GB 100 %). ✅ **seed5 gabia 발사** (재전달 블록 · tmux `q5` · repo eed064c59 · 도구 sha `d94403bc…` = seed3·4 같은 코드 ·
    watch `/data/work/runs/q5_watch.sh`) — ⏳ plan 줄 `120 원자 · turbo · 900 ps` 확인 대기.
    ✅ seed3·4 `--seed_gate` (단일 파일 `git show c238f3cdf:` · sha 47c7e0aa): 원시 최단 P–S **1.965 · 1.964** · relax 2.006 · 2.032 ·
    ρ 1.5933 · 1.5910 · 🟡 **seed3 다리 S 1** (P₂S₇ 형 · PS₄ 보존율은 1.0000) → **Q7**. ⇒ 네 시드 전부 원시 P–S < 2.0 (Q2 근거).
    게이트 읽는 법은 결과 전에 정오 기록 §6 (STO · P-1 D비 < 2 · P-2 MSD@50 < 48.88).
  · `--seed_gate` 실측 (kgy seed1·2): **seed1 relax 가 기준값 재현** (PS₄ 1.0000 · 2.037 P-S · ρ 1.6212) · 🔴 **원시 최단 P–S seed1 1.988 · seed2 1.943 < 2.0**
    (P–S 제외면 2.197 / 2.184) — 원시로 재면 기준 자신이 떨어진다 = Q2 실측 확인. seed2 ρ 1.5782 (−2.65 %). 원시↔relax 변위 rms 0.24–0.30 · max 0.59–0.67 Å
    (정오 기록의 '~0.1 Å' 추정 정정). 🟡 **Q6 새로**: 총상한 180 GPU-h 를 공유 GPU 에서 어떻게 세나 (cascade 선례 = 벽시계) → 시드별 wall_min 장부.
    장부: seed1 **35.1 h** (카드 이전 런) · seed2 **47.0** · seed3 **28.7** · seed4 **28.9 h** → 카드 몫 지금까지 **104.6 h** (견적 60 h) + seed5 · 파일럿 진행 중
  · 🔴 **파일럿 결과 (09-25 저녁 · kgy · 각 9.6/9.7 h)** — §6 잠정 읽기: **P-2 (550 K)** C1 ✓ · MSD@50 30.7 < 48.88 ✓ · C2 beta* **0.80 경계** (미반올림 필요) / **P-1 (400 K)** C1 ✓ · **C2 ✗ beta* 0.64** → 카드대로면 본 15런 **보류**.
    ⛔ **§6 정정**: 도구의 D 열은 STO 모드에서 `msd.json` 저장값(2–50 창)을 읽기만 한다 — 350–398 창의 D 로 못 쓴다 (두 창 D 가 1.050e-06 으로 같았다) → D₃₅₀₋₃₉₈ 는 자유절편 재적합 (정오 기록 `⛔_정정_§6_D열`). 판정·갈래는 **외부 1저자** (Q8 셋).
    ✅ 재적합 (09-25): T400 D₂₋₅₀ 1.050e-06 · D₃₅₀₋₃₉₈ **3.944e-07 → 비 2.66 > 2 ✗** · beta* 0.641 ✗ / T550 beta* **0.805** (경계 ✓) · MSD@50 30.0 ✓. `--scan`: 늦은 창 c ↑ · m ↓ · β ↓ = sub-diffusion 쪽.
    🔎 **MTO 확정 (09-25 · traj 에서 되살림 · lag ≤ 200)**: c 상수(0.6–1.0) · m 상수 · β → 1.0 · D_inc ≈ 1.05e-06 일정 = **케이지 절편형** — STO 의 sub-diffusion 신호와 어긋남 (STO 늦은 창 요동 가능). C2 미통과는 두 곡선 다 같음(0.641/0.56). P-1 은 그대로 미통과 · Q8-④ 를 이 어긋남으로 갱신.
    ⇒ **P-1 미통과 · P-2 경계 통과 → 본 15런 보류 (잠정)** — 판정·갈래는 외부 1저자 (Q1–Q9 편지 `kb/projects/li2s_glass_external_first_author_letter_2026_09_25.md`).
    ✅ **seed5 담금질 끝 (09-25 20:12 · 33.0 h · plan 차이 seed 만)** — `--seed_gate`: **두 판 모두 PS₄ 0.9167** (12 P 중 1) · P–S 제외 최단 **S–S 2.031/2.099 Å** (S–S 결합 형성 의심) · ρ 1.6181 · 변위 max 1.03 → Q9 (기록·제외 vs 재담금질).
    Q6 장부: seed2–5 + 파일럿 = **156.9 h** (견적 69 · 상한 180 의 87 %). ⏸ **추석 — 편지 발송·외부 1저자 회신은 연휴 뒤** (1저자 09-25). 우리 쪽 li2s 실행 큐는 비었다 · 회신 전 어떤 li2s 계산도 던지지 않는다.
    → 벽시계로 세면 본 15런 전에 상한 근처 ⇒ **Q6 은 본 캠페인 전 필수**. 외부 1저자 질문은 이제 **Q1–Q7** (정오 기록 §4).
- ✅ **SDCP/PTFE (C-12 v41, 1저자 = 사용자)** — 사람용 정리 `kb/results/sdcp_ptfe_c12_eads_brief_2026_09_23.md`
  (숫자의 지위 · 1.83/2.54 Å 와 DFT 힘 · PTFE −0.79 크기 검증 · Kang 2025 대비 · 대기 12잡 · 세미나 멘트·예상 질문).
  수치 정본은 `db/properties/sdcp_c12_v41_eads_ungated_2026_09_21.json` §9 (D3 독립재현 0.5/2.6 meV · 분산모델 4종
  PTFE −0.66~−0.79 · D 부호 불변). 값은 여전히 `citable: false` — **v42 mirae 회신 대기**(1단계 5잡 → 2단계 7잡).
  ⚠ 1저자가 9/23 내부 연구세미나 슬라이드에 −0.96(TOTEN F)/−0.79 를 쓰려 했다 — 정본은 −0.955, Preliminary 각주 권고.
- ✅ **세미나 3편 (Li₂S · Li–S ASSB · 2026-09-23 밤)** — litdb-curator 3 + **메인 PDF 재대조 통과**. digest ·
  INDEX · comparison §J-44/45/46 · DEM §I-7/8. 트랙별 판정 (값을 섞지 않는다):
  · [Zhang26PI3] CP2K AIMD 231원자 · 800 K 1점 · 40 ps · 궤적 1 · **담금질 램프 없음** → li2s 유리 트랙엔 *정반대 규율 사례*로만
    (외부 1저자 트랙 — 판단은 그쪽 몫) · W_ad BW (B) 근거 **안 됨** (자원·기저 수준 미기재 · 벌크 · A′ 판정 불변).
  · [Wang25MIEC] 계산은 LPS·MIEC 유리 4셀뿐 (Li₂S 계산 없음). 🔴 figshare 구조를 **메인이 독립 재현**: PS₄ 0/13 · 0/12 · 2/10 · 0/9
    (NMR 84–100 %) · 형식전하 +1/+4/0/+2 — P–S 문턱 2.4→3.0 Å 불변 ⇒ 갭·ICOHP·AIMD Ea 는 **비교 금지**. UMA↔DFT 시험세트 **부적합**.
  · [Liu26Sn] "Li⁺ 추출 장벽" **계산 안 됨** (Tafel 상대 Ea · 본문 10.46 vs `Fig. 3f` 25 kJ/mol) · Bader *"1.32 e⁻ S→Sn"* =
    `Fig. S6` 의 **Sn 원자 라벨** 오독 (메인 그림 확인: 옆 S +1.65 vs 벌크 +1.68) · 그래핀 흡착 −0.46 eV/분자는 **W_ad P2 기준점 아님**.
    ⭐ 살아남는 한 줄: *"양이온–S 가 센 S 자리에서 Li–S 가 약하다"* 는 **우리 comp1 per-site ICOHP 에 이미 있다**
    (Li–S(PS₄) −1.3438 vs Li–S(4d) −2.5677 eV · `per_bond_json/bonds_comp1_k444.json`) → Nd·O·B 근처로 **계산 0** 확장 가능 (제안 · 결정 아님).
  · 🔧 문장 출처: *"DFT and mesoscale … nucleation-growth"* 는 첫 docx SI 의 **숨은 인용 메타데이터** 안의 SI ref [5] 초록
    (Adv. Mater. 2023, 2206762) — 출판 PDF 엔 없다. ⚠ docx 에서 뽑은 문장은 PDF 로 다시 확인한다.
  · 🔴 **도구 결함** `tools/litdb/extract_figures.py` `_side_rect` — 2단 조판(Nature 식)에서 그림을 **캡션 단 폭으로만** 자른다
    (Wang Fig. 1–5 잘림 · Fig. 3i 갭 패널 · 5a–c 누락). 에이전트가 이 논문만 손으로 다시 잘랐고 **도구는 그대로** — `--refresh` 하면 다시 잘린다.
- ✅ **[Li26MCI] (Li·Jeon·Persson 2026 MLST, Na₃PS₄‖Na)** digest·그림 25·병합(INDEX · Ref key · §E · §H · §J-42) 완료.
  `kb/concepts/cv_vs_dqdv_and_two_windows.md` §8-4 부분 정정(kim2026·lomeli2024 누락, "분야 전체의 공백" 과장).
  🔎 확보 1순위 = **ref 19 Li et al. *J. Phys. Chem. C* 129, 16043 (2025)** (Li₇P₃S₁₁‖Li — "평탄" 의 원전).
- 🔴 **웹앱 cascade 화면이 fail-closed 다 (2026-09-22 ESW 가장자리 수정의 부작용).** `cascade_audit_manifest.json` 이
  해시를 박은 4파일(`oxidation_stability_cascade_v3_pinned.json` · `b2o3_esw.json` · `cascade_screening_funnel{,_v2}.json`)을
  어제 고쳐서 불일치 → 헤드라인 타일·감사 그림 0개. `webapp/tests/test_webapp.py` 3건 빨간불(정상 경보다).
  ⛔ **원장 해시만 다시 박지 않는다** — `rebuild_pool_inputs.py:119` 가 `window_V` 를 읽어 퍼널 게이트로 넘기므로
  **풀 입력 → `build_screening_funnel.py` → 감사 그림 → `build_cascade_audit_manifest.py`** 순서로 다시 만들어야 하고,
  **퍼널 통과 목록이 바뀔 수 있다**(ESW 트랙 = 1저자 사용자 결정). 세미나 뒤 따로 한다.
- ✅ **box331 시드 확장 끝 (2026-09-23 낮)** — 새 시드 s5·s6 12런 C1·C2·C2b·C6 전건 기록
  (`box331_seedext_c2b_c6_2026_09_23.json` · C2b 20.1–99.6/이온 · C6 12/12 rigid).
  · **lpsocl** — 600 K 새 시드 둘 다 C2 탈락(11·15 %) · C3 compatible → 개정문 R5 **규칙 A 적용**:
    레지스트리 Ea **0.1804 → 0.1809 [0.1790, 0.1829]** · 허용문 0.180 → **0.181 ± 0.002** · 평가 A-09-11 → A-09-23(15런) 대체.
  · **modelc** — 5시드 C3(09-18, A: compatible)의 C2b·C6 빈칸이 닫혔다. ⏳ **HOLD 해제·canonical 승격은 1저자 비준 대기**(사전등록 §3 A).
  · 러너 `--label modelc` 하드코딩 → `$SYS` (lpsocl s5·s6 run_meta label 이 'modelc' — 원본 보존, 원장에 정정 기록).
- ⏭ **b2o3 MD — 전도도는 닫힌 채로, 질문을 바꿔 두 가지** (1저자 2026-09-23 "우선 해보자"):
  · ✅ **09-25 s6 옮김 완료** (kgy 3/3 → gabia `s6.incoming` → 막는 파일(246 B) 치우고 mv · json 8개 sha 찍힘 — kgy 쪽 대조 대기) · gabia 는 지금 **s4**.
  · ✅ **개정 2 (1저자 09-25 '바로 돌리자') — s5 도 kgy** → `b2o3_framework_event_rate_amendment_2_2026_09_25.json` + `D-2026-09-25-b2o3-eventrate-machine-amend-2`
    (gabia OUTROOT 에 `s5` **파일**을 먼저 놓아 s4 뒤 멈춤 · kgy tmux `b2o3_s5` · worktree `~/b2o3_s6_src` · 끝나면 s6 과 같은 옮김). ⏳ 막는 파일 · 발사 블록 전달.
  · ✅ **kgy 분할 = s6 만 (1저자 09-24 선택)** → 개정문 `db/properties/b2o3_framework_event_rate_amendment_2026_09_24.json`
    (카드 원문·원결정 불변 · 카드 지문 e40a5ee5 를 가리킨다) + 결정 `D-2026-09-24-b2o3-eventrate-machine-amend`.
    s6 정본 = kgy 런 · 세 온도 끝나 `ensemble_results.json` 이 생기면 통째로 gabia `/root/work/runs/b2o3_221_eventrate_400ps/s6/` 로.
    ⏰ **옮김 마감 ≈ 09-27 18:00** (gabia 가 s6 에 닿는 시각) — 넘기면 gabia 의 s6 을 결과 열람 없이 PID 로 멈춘다.
  ① ✅ **완료** — `b2o3_c6_census_512_2026_09_23.json`: 4/4 **framework_mobile**, 런당 사건 30–56 (200 ps) vs modelc·lpsocl 30런 0.
    PS₄ 는 안 깨지고(P결합 음이온 이탈 0) P 중심이 통째로 옮기며(3.7–6.5 Å) 자유 S·Cl 이 흐른다(최대 10.6·16.0 Å). 진단. ⚠ census 는 P 중심 규칙이라
    **B 를 안 세고** BS₃ 의 S 는 '자유 S'(2.0 Å)로 분류된다 — 결과와 같이 적는다.
  ② ✅ **카드 비준·발사 준비 (2026-09-23)** — `b2o3_framework_event_rate_prereg_2026_09_23.json` · 결정 `D-2026-09-23-b2o3-framework-event-rate`
    (active·ratified). 512원자 · 600/650/700 K · 400 ps · 시드 2–6 · **turbo** · **gabia**(탄성은 이 뒤로). 보고량 = 원소군별 사건 수·움직인 원자 수·첫 사건 시각.
    러너 `run_box331_seed_extension.sh SYS=b2o3`(가드 0 음성 2건 통과). ⏳ 발사 후 run_meta 무효조건 즉시 확인 → 끝나면 census 15런.
    ⛔ **발사 취소 (1저자 2026-09-23 "gpu여야 된다니까 취소취소")** — gabia 블록 실행 보류. 카드·결정은 봉인된 채 그대로(기계를 바꾸면 개정문+재비준).
    ✅ **재발사 2026-09-23 13:29 (1저자 "다시 gpu로 수정해서 돌리자")** — 취소 원인은 CPU 가 아니었다: 내 블록의 안전장치가 repo 셸
    스크립트(탄성 러너) 실행 중이라 pull 을 건너뛰었고 옛 러너가 b2o3 를 몰랐다. ⇒ **새 worktree** `/root/work/repo_b2o3_evt` @aac448854 에서
    발사 · tmux `b2o3_evt` · 드라이버 PID 3322562 · GPU 5.6 GB(컴파일 중) · 로그 `/root/logs/b2o3_221_eventrate.log`.
    run_meta ✓ 512 · [2,2,1] · [600,650,700] · 400 ps · save_traj · turbo · label b2o3 · **save_fs 100**(명령줄 확인 — run_meta 필드가 아니다) ⇒ **무효 조건 전건 통과**.
  · 🔴 **탄성 러너를 멈췄다 (PID 3014241, 대기 45 h)** — b2o3 UMA 와 GPU pw.x 동시 금지(1저자 선택 '탄성 뒤로'). ⚠ **발견: 그 러너는 SYS 가 없어
    기본값 `comp2` 로 대기 중이었다** (cwd /data/work/runs/elastic_comp2 · MINFREE 6000 · 로그 이름만 el_modelc2x.log). 9/10 원래 계획은
    `SYS=modelc_2x → b2o3` — 그대로 뒀어도 modelc_2x 영률은 시작되지 않았다(조용히 틀린 경로). 상태 저장 `/root/logs/elastic_runner_saved_0923.txt`.
    ⏭ b2o3 끝나면(≈5–6일) **`SYS=modelc_2x`** 를 명시해 재개한다 (수렴한 strain 은 러너가 건너뛴다).
- ✅ **Nd ICOHP 판정 = C1 (PP 가 원인)** — Nd79 가장 가까운 S 5개 **−3.779 eV** (6월 −0.481 · 문턱 −2.0) · 대조군 P–S −5.669/Li–S −1.658 은 6월과 같다 · spilling 1.19 %.
  기록 `db/properties/nd_icohp_frozen4f_result_2026_09_23.json` · 6월 Nd–S **영구 비인용**(`nd_icohp.json` 표시 · `HZ-nd-icohp-june-nds-pp`).
  ⏭ 원자료(ICOHPLIST · ICOBILIST · lobsterout) 회수 → `db/raw/nd_lobster_frozen4f_2026_09_23/`.
  ✅ **k-탐침 끝 (09-24 10:31 KST 확인 · SCF 15 iteration · JOB DONE)** — **ΔE(k331−k221) = −0.028316 Ry = −3.210 meV/atom > 문턱 1** ⇒
    `D-2026-09-18-nd-icohp-kmesh` **재개 조건 2 발화 · dense-k LOBSTER 재개** (규칙이라 선택 아님). C1 은 유지 + 한계 1줄 (여유 1.78 eV 는 뒤집힐 크기 아님 — 예상).
    ⏳ **1저자 결정 대기**: k 값 (권고 k 3 3 1 — 탐침 outdir 이 그 SCF 전하밀도라 SCF 생략 · ⛔ 지우지 말 것) · 기계 (GPU 규칙 09-23) · nbnd ≥ 546 (920 과다).
    기록 `nd_icohp_frozen4f_result_2026_09_23.json` `enforcement_④_k_탐침_2026_09_24` · `!` 원문 **E_k331 −6399.21429237 Ry** (차 −0.02831583 Ry).
    ✅ **닫음 (1저자 · 선택지 b · '그 이상은 지금 nd 건은 과투자')** → `D-2026-09-24-nd-icohp-close` · 기록 `nd_icohp_pp_swap_closed_2026_09_24.json`.
    남긴 것 한 줄: *PP 를 frozen-4f PAW 로 바꾸자 Nd–S −0.48 → −3.78 eV (약 8 배) · 대조군 P–S·Li–S 1 % 안 그대로 ⇒ 6월 약한 Nd–S 는 PP 탓*.
    dense-k 는 **안 돌린다** (k 3 3 1 결정은 같은 날 superseded) · k 2 2 1 미수렴은 한계로 · 재개 = Nd–S 를 정량으로 써야 할 때만.
    탐침 outdir `tmp_kprobe` 4.4 GB 는 재개하면 SCF 를 아낀다 — 디스크 필요하면 지워도 됨.
  (옛 기록) 🟢 **k-탐침 도는 중 (enforcement ④ · 1저자 "이것도 진행하고" · k 3 3 1)** — gabia CPU `/data/work/runs/nd_ppswap_2026_09_16/kprobe_k331`
  · 16:42 KST 발사 · 8랭크 npool 2 · k 5개 · 총 RAM 34.2 GB (원 SCF 32.5) · pw.x PID 3364447–3364453·3364457 · 원본과 다른 줄 3줄(prefix·outdir·K_POINTS).
  · watch `kprobe_k331/kprobe_watch.sh` (PID 고정 · CPU 는 직전 표본 대비). 판정: 원 SCF **−6399.18597654 Ry** 대비 |ΔE| ≤ **0.0088 Ry (1 meV/atom · nat 120)**
    → 넘으면 C1 판정의 한계에 *"k 2 2 1 → 조밀 k LOBSTER 필요"* 를 단다. 원 SCF 10 h 33 m.
  · 09-24 00:08 — 8/8 랭크 · CPU 800 % · 경과 07:26 · SCF iteration 8 · 오차 0.0118 → 0.00112 → 0.000298 Ry.
    ⚠ `kprobe.err` 끝에 `btl_tcp … recv(24) failed: Connection reset by peer (104)` (rank 1) — MPI 가 멈춰도 CPU 는 100 % 라
    **CPU 로는 못 가른다**. 판별 = err 이후에도 out 이 자라는가 (붙여넣기 블록 전달 · 결과 전 판정: 한 반복 ≈55 분 넘게 out 정지면 멈춤 의심 → 1저자 결정).
    ✅ **판별 00:23 — 무해**: err 23:21:40 (그 1줄뿐) · out 00:03:39 (**err 뒤**) · 누적 cpu 18635 → 22174 → 26478 s = 반복당 59–72 분 ·
    iteration 8 (≈22:52 시작)이 오류를 지나 00:03 에 끝났다 · mpirun 3364444 `btl 지정 없음`. 08-31 좀비(9/10 랭크 CPU 0)와 다르다.
    ⏭ watch CPU 가 800 → ≈100 % 로 떨어지면 그게 좀비 신호 → PID 로 끊고 `--mca btl self,vader` 재시작(1저자 결정). 다음 반복 끝 ≈01:05–01:15.
- ⏭ **kgy Li₂S P1 탐침 (li2s 셀수렴 카드 §3 · 공유 GPU 라 벽시계는 상한)** — worktree `~/lldvar_p1` @c8f0f2db ·
  GBRV 해시 kgy = gabia (Li `02cc4b38…` · S `84ad7318…`) · kgy `~/work/pseudo` 의 Li·S 는 GBRV 뿐(PAW 없음 → 전용 폴더 불요).
  ⛔ kgy 에 Li₂S 이완본이 없어 빌더가 멈췄다 → gabia `sei_dft/li2s*/01_vcrelax.out` (sha `0bcb294b19b23c24`, v2 NEB 가 쓴 것)을 rsync 로 옮겼다
  (`~/work/runs/sei_dft/li2s_mp-1153/`). ✅ 입력 생성 `~/work/runs/li2s_p1_probe_2026_09_23/li2s/scf_probe/scf_probe.in` —
  4×4×4 · **191원자** · λ₁ 16.14 Å · 전자 766 · q −1 · k 2×2×2 · 60/480 · maxstep 3 · GBRV Li/S.
  ⛔ **P1 불통과 (17:38)** — 러너 `calc=probe`: QE 추정 **45.15 GB/랭크** · 15 s 만에 합계 23 964 MiB → KILL 23 000 가드가 우리 PID 만 멈춤
  (VRAM 하한 21.1 GB · 벽시계 못 잼). UMA MD 1392411(cascade eprime_P2_Al2S3_B) **생존**(2902 MiB · 92 %). 카드 §3b 기록.
  ⚠ 러너 버그 1건 발견·수정 `c6d120d01`: kgy nvidia-smi 는 프로세스 목록 대신 *"Process-level GPU information is restricted."* 문장을 준다 → PID 로 읽던 것.
  ✅ 1저자 결정 **"영률 끝내고 li2S 끝내자 나중에"** → gabia 탄성(modelc_2x) 뒤 단독 재프로브(ppcg/paro) → 통과 시 NEB. kgy 는 이 입력에 불가.
- 🔴 **cascade 산물 갭 원장이 비바닥 다형 (2026-09-23 발견 · cascade 트랙 = 사용자 1저자)** — `db/properties/cascade_product_gaps.json`(08-19 생성)의 산물 **352종 중 241종이 E_hull > 0 항목**
  (Li₂S mp-1125 Pnma · LiCl · LiF · Li₃PS₄ · AlCl₃ 0.0 eV/E_hull 0.91 · NiO 0.0 eV/E_hull 1.31 …). 생성 도구 `sei_product_gaps.py` 의 `or 9e9` 버그는 09-13 에 고쳤는데 **이 파일은 재생성 안 됨**.
  위에 선 문장: *"693 반응 중 481개(69 %) 금속 산물"* (`kb/results/interface_axes_90_2026_08_19.md` — 머리에 ⛔ 달았다). 인용위험 **HOLD** `HZ-cascade-product-gaps-nonground-polymorph`.
  ⏭ gabia: `bash tools/oxidation/run_cascade_extras.sh` (MP API · uma env) 로 재생성 → 693 반응 병목·금속 비율·주범 재계산 → `cascade_product_bvse.json` 도 새 mp-id 로. 결과 보고 전 역할 분류가 바뀌는지 먼저 본다.
- ✅ **결정 3건 비준** (`97edeb233` · 형식 복원 뒤 172줄 추가만): W_ad SE 대칭 두 장 · D3 2체 + ATM 따로 · QE D3 3체 표기. `vgcf_hbn_*.json` 표기 정정 · QE 생성기 4곳 `dftd3_threebody = .true.` 명시(결과 불변).
  ⏭ SDCP 옛 QE 기록(phaseB · wave1.5 — 닫힌 캠페인)의 같은 표기 정정은 **아직** (우선순위 낮음).
  ⚠ 내 실수: `decisions.json` 을 indent 2 로 다시 써서 7146줄 diff 를 냈다 → 원래 형식(indent 1)으로 복원. JSON 원장을 고칠 때는 **원래 형식을 먼저 재현**하고 쓴다.
- 🟢 (끝남 — 위 판정) **gabia Nd frozen-4f LOBSTER** (`/data/work/runs/nd_ppswap_2026_09_16/lobster_frozen4f`) — nscf **JOB DONE 14:33** (2 d 0 h 36 m · k 4 · nbnd 920 · wfc 09-23 확인) →
  LOBSTER 5.1.1 **PID 3337949** (14:44 KST 발사 · OMP 8 · 래퍼가 끝나면 `lobster_scf.in` 을 `.orig` 로 되돌린다).
  · 판정량은 **결과 전에** 카드에 고정: Nd79 의 가장 가까운 S 5개 평균 (C1 < −2.0 / C2 > −1.0 eV) — `nd_icohp_pp_swap_card_2026_09_16.json` §2b.
  · 실측(결과 전 기록 §2c): 실제 기저 **546 함수**(P/S/Cl 3d 미사용) → 밴드 547+ 무시 · 사면체법 불가로 Gaussian smearing. **nbnd 920 은 과다** — 다음 LOBSTER 는 실제 기저 수로 잡는다.
  · ⏭ `rc=` 가 찍히면 완료 블록(원복 확인 · spilling · 원소쌍 평균 · Nd 원자별 이웃) → C1/C2/C3 판정 → enforcement ③ 한계 기록 → ④ k-탐침(SCF 10.5 h 급이라 k 값·실행 여부 1저자).
  · ⚠ q_watch 의 *"LOBSTER CPU 0 % ← 700 미만이면 seed4 중단"* 은 **끝난 nscf(pw.x)** 를 보는 문턱이다 — LOBSTER 프로그램과 무관하니 seed4 를 죽이지 않는다.
- ⏭ **새 캠페인: LPSCl | Ag–C | VGCF 점착일 (DEM 쪽 요청 · 트랙 = 우리 DFT → 1저자 = 사용자)** — **계산 0, 리뷰 대기.**
  계획·카드 **v3** `kb/projects/wad_lpscl_agc_vgcf_plan_2026_09_23.md` (**§0′ 이 유효판**) · Codex **BV 회신 수령 = NO-GO** (`kb/reviews/codex_BV_reply_wad_lpscl_ag_c_vgcf_2026_09_23.md`).
  1저자 지시: **두 리뷰 받기 전에 파이프라인을 걸지 않는다** → 두 리뷰 다 왔고 둘 다 NO-GO. 본 계산은 Codex 재개 조건 5묶음 뒤.
  · 🔴 Codex 새 P0 두 건 — **우리 재계산으로 재현**: ① 러너 `build_ncm_1L` 은 LiNiO₂ 가 아니다 (R-centering 누락 → Ni–O 최단 3.667 Å · 2.5 Å 안 O 0개;
    정상은 1.973 Å · 6) — v6 stage 11 이 이 빌더를 썼다. 러너 docstring ⛔ · `adhesion.json` 발견 블록 ② SE 단순 z 절단은 PS₄ 8/48 을 끊는다 —
    PS₄ 보존 창 z = 1.26–3.78 · 6.28–8.80 Å 가 있으나 비대칭(Li 면 vs S 면) 슬랩이 된다.
  · ⏭ **다음**: 구조 빌더·검증기(재개 조건 1) · 1저자 결정 4건(계획 §0′: SE 종결 · LiNiO₂ 종결·두께 · 상태 정책/U · DEM 접촉법칙 문의) — Codex 잘린 두 칸은 받음(≤ 0.10 J/m² 표본별 · registry ≥ 4).
  · ✅ **SE 대칭 슬랩 빌더·검증기 (재개 조건 1 의 SE 절반)** `tools/wad/se_sym_slab.py` — selftest 45 (음성 포함 · 돌연변이 11종 전부 빨간불 확인).
    구조 `db/structures/wad_se_slabs_2026_09_23/` (.vasp + .xyz + manifest): **s_outer Li₇₆P₁₂S₆₂Cl₁₂ 162원자 · li_outer Li₆₈P₁₂S₅₈Cl₁₂ 150원자**
    (= Pustorino 6층 조성) · PS₄ 12/12 부모 S 일치 · 전하 0 · 양면 동일 = **x 축 C2 (편차 9e-5 Å)**.
    ⚠ 발견: comp1_V0_k444 는 **−4 축이 없다** (Li 정렬이 입방 대칭을 깬다 — 벌크에서 z 를 뒤집는 연산은 C2x 하나). 계획 §0′ 의 *"−4 회전반전이 z → −z"* 는 이 구조에 안 맞는다.
  · ✅ **SE|SE 대조 입력 5잡** `db/inputs/wad_sese_control_2026_09_23/` (벌크 SCF · 두 슬랩 SCF = 무이완 W_sep PBE/PBE+D3 2체 · 두 슬랩 PBE 이완 = Pustorino 대조)
    — comp1 정본 설정(GBRV Li/S/Cl + P rrkjus · 52/520 · 슬랩 k 4 4 1 · 벌크 k 4 4 4). 식은 결과 전에 코드로 고정: `se_sym_slab.py --collect <RUN>`
    (W = [E_s + E_li − n·E_bulk]/2A, n = P 합/4, μ 상쇄). ✅ **경보 운영값 봉인 (결과 전 · 1저자 "너가 권장하는대로")** `D-2026-09-23-wad-sese-alarm-band`
    → **v2 로 대체 (2026-09-23 밤 · "ㄱㄱ")** `D-2026-09-23-wad-sese-alarm-band-v2` — 구간 그대로, 결정문 벽개식 계수만 일반형 (6층 6 · 4층 4)
    — 이완 PBE W_cleave 0.3–0.7 J/m² 밖 = 원인 미분류 경보 · > 1 = PS₄ 절단·wrap 먼저 점검 · 무이완 < 이완 = 경보. **합격선 아님**. `--collect` 가 출력.
  · ⏸ **gabia 러너 — 잡 0 확인 (1저자 붙여넣기 2026-09-23 밤: 로그가 17:23:58 시작 대기 줄에서 끝남 · 실행 폴더에 runner.log 뿐)** · ✅ **러너 정지 확인 (2026-09-24 00:08 · PID 3374935 · tmux `wad_sese` 닫음 · 남은 bash 없음)** · tmux `wad_sese` · worktree `/data/work/repo_wad` @265faeff · 로그 `/data/work/runs/wad_sese_2026_09_23/runner.log`
    · `WAIT_PIDS` 3207227·3210946 (li2s 담금질 seed 3·4) · `ONLY_PIDS` 3322562 (b2o3) · 시작 때 GPU 15.3 GB · 호스트 27 GB.
    ⛔ 도는 동안 `/data/work/repo_wad` 를 갱신하지 않는다. 집계는 다른 clone 에서 `se_sym_slab.py --collect`.
  · ⛔ **gabia GPU 예외 — 실행 전 철회 · 미사용 종료 (2026-09-23 밤 · 1저자 "ㄱㄱ" · BW Q8 네 가지 기록 · 비준 revoked)**. 러너에 ⑧ 게이트: `ALLOW_UMA_COEXIST=1` 이어도 원장 active 결정 ID 가 아니면 시작 안 함.
    (옛 기록) **gabia GPU 예외 (1저자 "이거 하돼")** `D-2026-09-23-gabia-gpu-exception-sese` — 러너 `tools/wad/run_sese_gpu.sh`: li2s 시드 종료 대기(PID·cmdline) ·
    합계 VRAM < 40 GB 시작 · > 44 GB 즉시 중단(우리 PID 만) · 호스트 여유 ≥ 16 GB 시작 · < 4 GB 중단 · `ALLOW_UMA_COEXIST=1` 필수. CLAUDE.md gabia 절에 한 줄.
    ~~⏭ gabia: worktree → DRY_RUN → tmux 발사~~ (발사는 했고 잡은 0 개 — 예외 철회로 끝)
  · 📨 **DEM 회신 수령 (2026-09-23 저녁)** — 정정 넷 전부 수용 · w = W · 헤드라인 = 고정기하 W_sep (+ DFT@UMA 값도 → G_c 띠) · 종결 두 면 그대로 ·
    🆕 **P2 LPSCl|graphite(0001) 을 P1 우선순위로** 요청(Ag 5.7 vol% · 16배 규칙) · 같은 SE 슬랩 요구 · 848원자 5점 비용 요청.
    원문·읽기·**회신 2 초안** `kb/projects/wad_dem_reply_draft_2026_09_23.md`. ✅ **P2 수용 (1저자 "ㅇㅇ 그러자")** → `D-2026-09-23-wad-p2-lpscl-graphite-scope`.
    격자 정합 후보(메인 재계산): **P2 = SE 1×3 + 흑연 직사각 4×7 (+2.19/+1.14 %) ≈ 820원자** · **P1 = SE 1×2 + Ag(111) 2×7 (a 4.086: +0.46/−0.57 %) ≈ 436원자**.
    ⏳ 회신 2 발송(사용자 · **정정본** — Ag 셀 표기·층수 가정·820원자는 GPU 불가 → KISTI) · 결정 7 격자 정합 규칙(어느 쪽을 변형) 봉인.
    ⛔ **SE|SE 슬랩은 gabia GPU 에 안 들어간다 (CPU 1랭크 추정 · 2026-09-23 밤)**: 벌크 6.7 GB · **S 바깥 슬랩 55.8 GB · Li 바깥 50.2 GB** (k 9) > A6000 48 GB.
    그대로 두면 슬랩 pw.x 가 수 초에 수십 GB 를 잡아 2 s 가드보다 빨리 b2o3 UMA 를 칠 수 있다 → gabia 러너(tmux wad_sese) 정지 블록 전달.
    → ~~KISTI A100 4장 평면파 분산으로 이전 제안~~ ⛔ **철회 (rejected)** — **KISTI 는 2026-09-15 에 접근 종료**. CLAUDE.md 계산 자원 절이 09-08 판이라 KISTI 가 살아 있었다 → 고침.
    ⏭ **SE|SE = 4층(110/98원자) · 진공 15 Å · k 3×3×1 로 축소** (추정 6층의 0.40–0.48 · Pustorino 3층↔6층 차 0.02 J/m²) → CPU 추정 확인 → gabia GPU.
    ⏭ **P1·P2 전체 계면 평면파 DFT 는 우리 기계로 불가** → (A) 작은 모델 DFT 로 UMA+D3 검증(li2s 선례 · MLIP 금지 규칙 예외 필요) vs (B) CP2K 가우스 기저 — **1저자 결정** (계획 §0′ *KISTI 없이*).
    (스크립트 `tools/wad/sbatch_sese_kisti.sh` 는 기록으로 남김 — 쓰지 않는다)
  · 📨 **Codex BW 회신 수령 (2026-09-23 밤)** `kb/reviews/codex_BW_reply_wad_validation_without_cluster_2026_09_23.md` — (A) 를 *검증된 전체 계면 절대 W* 로 넘기는 것 **NO-GO** ·
    제한 파일럿 **조건부 GO** · CP2K 필수 아님 · 권고 경로 **A′** (작은 주기 모델 DFT 값 ↔ 전체 계면 UMA+D3 예측 분리 · 큰 계면 값은 DEM 민감도 시나리오로만).
    V3·V4 조각형은 **진단용**(eV/조각 · J/m² 문턱 이전 불허) · SE|SE 4층 식 계수 **4** · 분리 참조는 두 끝점 같은 셀 · 대표 registry E(d) 대조 · 보고량 이름 *"SE 에 정합되도록 변형된 박막의 고정기하 분리일"*.
    반영: 계획 §0′ *BW 회신 반영* · DEM 발송판 **회신 2‴** (2·2′ 폐기). ✅ **1저자 "ㄱㄱ" (2026-09-23 밤)** → `D-2026-09-23-wad-a-prime-scope` (active) ·
    `D-2026-09-23-wad-sese-alarm-band-v2` (active · v1 superseded) · gabia 예외 retracted · 회신 2‴ 발송 승인 (근거 줄 ID 만 v2·A′ 로) — ⏳ **발송 확인 대기**.
    ⏭ **A′ 파일럿 사전등록** (작은 주기 모델 5점 · 운영 기준 ≤0.10/|MSE|≤0.05/수치≤0.02 J/m² · 분리 참조 같은 셀) → **4층 SE|SE 입력 + CPU 추정** (새 잡 = 자원 적합성 별도 확인).
    ✅ **4층 SE|SE 입력 생성 (09-24 새벽)** `db/inputs/wad_sese_control_4L_2026_09_24/` · 구조 `db/structures/wad_se_slabs_4L_2026_09_24/` —
    S 바깥 Li₅₂Cl₈P₈S₄₂ **110** · Li 바깥 Li₄₄Cl₈P₈S₃₈ **98** (합 = 벌크 셀 4개 → 계수 4) · 진공 15 Å · 슬랩 k 3 3 1 · **벌크 k 3 3 3 (면내 밀도 맞춤)** ·
    검증 7/7 · C2 9e-5 Å. jobs.json 에 경보 v2 · A′ 결정과 **PP 내용 해시** — 러너 ⑨ 게이트가 실행 기계 파일과 대조(불일치면 시작 안 함).
    ⏭ **실행 기계 = V100 (1저자 "v100은 비었어" · rsync)** — gabia 는 b2o3 UMA 가 GPU 를 쓰고 있고 공존 예외는 닫혔다.
    ⚠ V100 의 옛 계산(static_ab)은 PP 를 **밑줄 이름**으로 썼다 — 우리 입력은 점 이름. 내용 해시로 확인 후 점 이름 링크.
    🔧 **V100 컨테이너가 다시 만들어져 QE-GPU·NVHPC·pseudo 가 없었다 (09-24)** → kgy 에서 NVHPC 13 GB·QE 소스·pseudo rsync ·
    makelocalrc · configure ✓ (`-D__CUDA` · GPU_ARCH=70). ⏭ build → **빌드 검증** (static_ab/a 09-13 값 −1022.94654233 Ry · |ΔE| ≤ 1e-5)
    → DRY_RUN (⑨ PP 해시 ×4) → tmux `wad4l` 실행 + 30 분 $STORE 백업. 레시피 `kb/platforms/v100_uma_setup_2026_09_14.md` 함정 ⑨.
    ⚠ 1차 빌드 실패 (09-24): 내가 rsync 에서 cc86 산출물을 거른 탓에 devXlib 이 반쪽(`install/libcuda_devxlib` 표시만) →
    `device_fbuff_m.mod` 없음. 처방 = `make clean` (upstream 이 표시·FoX·MBD 까지 지운다) 뒤 재빌드.
    ✅ **재빌드 성공 (09-24 01:29)** — pw.x sha256 `912d8c8fdbfb3a8a` · hpcx-2.20 · CUDA 12.6 · libnvomp 만 · STORE 백업.
    ✅ **빌드 검증 통과** — static_ab/a −1022.94654233 Ry = 09-13 값 (|ΔE| < 1e-8 · 봉인 1e-5) · 6m14s.
    🟢 **V100 tmux `wad4l` 실행 중 (09-24 01:44~)** · DRY_RUN ✓ (PP ⑨ ×4 기준과 같음). 잡별 (wall · 피크 VRAM 합계):
    벌크 SCF 104 s · 10,350 MiB · **S 바깥 SCF 693 s · 32,038 MiB (한도 32,768 — 여유 730 MiB, 힘 계산 포함 통과)** · Li 바깥 SCF 556 s · 29,724 MiB ·
    S 바깥 PBE 이완 02:07 시작 → Li 바깥 이완. 이완 도중 OOM 이면 diagonalization 만 ppcg 로 (물리 설정 불변).
    ⚠ 09-24 10:31 watch: runner.log 마지막 줄이 **03 S 바깥 이완 시작(02:07)** 이고 완료표에 03 이 없다 · GPU 30,834 MiB 점유 · 순간 0 % ·
    pw.out 1,625 줄 매치 ⇒ **끝난 것으로 안 읽는다** (사용자 '끝남' 보고 → 이온 스텝 수 · Total force · JOB DONE · GPU 표본 확인 블록 전달).
    ✅ 10:44 확인: **돌고 있다** — 이온 스텝 82 · Total force 0.019–0.024 Ry/Bohr · pw.out 13 초 전 수정 · GPU 86–98 % · 10.7 GB (nstep 200 · forc 1e-3).
    ✅ **23:13 S 바깥 이완 끝** (rc 0 · 완료 판정 통과 · 21.1 h · 피크 **32,378 / 32,768 MiB = 98.8 %** — 여유 390 MiB) → **Li 바깥 이완 23:13 시작**
    (30.3 GB · 89 % · 끝 ≈ 09-25 저녁 추정). 판정은 두 이완 뒤 `--collect`. ⏭ BFGS 스텝·마지막 힘·$STORE 백업 확인 블록 전달.
    ⏭ 다 끝나면 `test_adhesion.py::test_missing_vram_is_dash_not_zero` 를 합성 원장 주입으로 (지금 전제 = 빈 VRAM 잡이 원장에 있다).
    ✅ S 바깥 수렴 내역: **199 bfgs 스텝 / nstep 200** (한 스텝 남기고) · Total force 0.0018 · 원자료 E(이완 · PBE) −2152.35487740 Ry (W 아님 · 원장·화면 미게재) ·
    $STORE 백업 `/home/ubuntu/runyourai/1/runs/wad_sese_4L_2026_09_24` (pw.out 23:13:16 — 원본과 **cmp 같음 ✅**).
    ⭐ **결과 전 선언**: Li 바깥이 nstep 200 에서 미수렴이면 마지막 좌표로 이어서 이완 1회 (verified-carry · 설정 불변) → 그래도 미수렴이면 멈추고 보고.
    집계 명령은 **`--qe_in db/inputs/wad_sese_control_4L_2026_09_24`** 필수 (collect 기본 입력은 6층 · 러너 끝 안내문도 고침 — V100 인스턴스는 옛 문구).
    ✅ **09-25 08:12 Li 바깥 이완 끝** (rc 0 · 완료 판정 통과 · 9.0 h · 피크 30,274 MiB) ⇒ **5잡 전부 끝** → ⏳ collect 블록 전달 (경보 v2 판정).
    ⚠ **집계 (09-25 · V100) — 경보 v2 발화**: 이완 PBE W_cleave **0.277** J/m² 가 운영 구간 0.3–0.7 **아래** (원인 미분류 · 합격선 아님) ·
    무이완 PBE 1.103 · PBE+D3 2체 1.518 · 무이완 ≥ 이완 정상 · Li 바깥 105 BFGS · −TS 0 · missing 없음. 문헌 Pustorino 0.47 (= γ_rich + γ_def · **같은 정의** 검산) 보다 0.19 낮다.
    이완이 W 를 75 % 낮췄다 (슬랩 속까지 움직였는지 미상). 결과 기록 `db/properties/wad_sese_4L_result_2026_09_25.json` (인용 불가 · 원인 후보 5 · 점검 제안 2 — 1저자 결정).
    ✅ **1저자: A·B 둘 다 → A 본 뒤 Codex 리뷰.** A = `se_sym_slab.py --relax_check` (새 플래그 · 문턱은 결과 기록과 같은 값 · selftest 58/58) —
    V100 에서 최종 좌표를 찍어 받아 여기서 돌린다. B = 벌크 이완 입력 `db/inputs/wad_sese_bulkrelax_4L_2026_09_25/` (V100 tmux `bulkrelax`) — 첫 SCF 가 −1022.94625093 Ry 와 같아야 한다.
    ✅ **A 결과 (09-25)**: 두 슬랩 다 **PS₄ 온전 · 짝 바뀜 0 · 진공 이탈 0** · Li 가 자리 하나 거리(1.6–2.8 Å) 이동 ·
    **속층 이완 신호** S 바깥 1.241 Å (Li) · Li 바깥 0.302 Å (겨우) — 원인은 안 가른다 (②·①·Li 재배치 열림). 원자료 `db/raw/wad_sese_4L_2026_09_25/`.
    ✅ **B 결과**: 내장 대조 ✅ · **0 BFGS 스텝** (이미 원자 극소) → ΔW 0 < 0.05 ⇒ 후보 ②(원자판) 해당 없음. 🔴 그런데 **벌크 응력 yz 10.8 kbar**
    (xx +13 · yy/zz −6.5 · P ≈ 0) — 셀 모양이 평형 아님. **사후 관찰**: 두 슬랩 뼈대가 z 에 비례해 y 로 밀림 (P dΔy/dz 0.028 · 0.061) = 균일 y–z 전단
    3–6 % ⇒ 가설 **②′ 기준 벌크의 셀 모양** (슬랩이 갇힌 전단을 풀었다). ⏭ **B′** epitaxial_ab vc-relax (입력 `…/05_bulk_vcrelax_epi_pbe` · 실행 전 문턱
    ΔW′ > 0.05) — ✅ **1저자 'b′ 하고 통합해서'** (V100 tmux `bulkvc`) → 결과를 **Codex BX** §4 에 붙여 한 번에 발송.
    ✅ **B′ 결과**: c 가 y 로 3.42° 기울고 z −1.7 % · E_05 −1022.96421634 Ry · **ΔW′ 0.0775 > 0.05** ⇒ **②′ 기준 벌크 셀 모양이 약 0.08 J/m² 설명**.
    사후 보정 **W′ 0.354** (경보 판정 대체 아님 · Pustorino 0.47 대비 −0.12). Li 바깥 슬랩 전단 0.061 ≈ 벌크 0.060 · S 바깥은 절반.
    ⚠ **범위 밖 발견**: comp1 V0 셀이 이 설정에서 전단 10.8 kbar 를 품는다 — 다른 계산 영향은 1저자. **Codex BX 발송 가능** (§4 통합 · Q3′·Q3″ 추가).
    ✅ **Codex BX 회신 수령 (09-25)** `kb/reviews/codex_BX_reply_wad_sese_4L_alarm_2026_09_25.md` — 원인 진단 **조건부 GO** · '방법 검증 완료'·DEM 승격 **NO-GO**.
    Codex 독립 재계산 1.103035 / 0.276958 / 0.354426 (+0.077469) 일치 (⚠ 전체 pw.out 없어 원출력은 미검증).
    🔴 **P0 (재현됨)**: 완료 판정기가 QE 실패 문구 `bfgs failed … convergence not achieved` + 최종 좌표 + JOB DONE 을 **완료로 통과** → ✅ 러너 `_done` · 집계 `parse_pw` 둘 다
    **마지막 실행만 · `bfgs converged` 명시 요구 · 실패 문구 거부** 로 수정 (selftest 62/62 · 54/0 · 음성 5 · 돌연변이 빨간불). ⏳ **이번 두 슬랩 원출력 확인 블록 전달** (Program PWSCF 1개 · bfgs 줄 · NOT achieved 0).
    ✅ **P1 문구 정정 7건** (결과 기록 `⛔_정정_회신BX_2026_09_25`): 4층 값 = '선택한 참조에 대한 슬랩 쌍 초과에너지' · **'Pustorino ±0.16 보고' 철회 (우리 산술)** · '이미 원자 극소' → '힘 기준 만족' ·
    **+0.0775 = 참조 변경 효과 (순수 전단 아님 · 문턱 0.05 는 크기 분류)** · Pulay 등방성 보장 아님 · 절반 전단 ≠ 미수렴 · epitaxial = '같은 면내 격자 · 법선 자유 참조'.
    📝 **DEM 허용 서술 (Q6) 확정** → 결과 기록 `허용_서술_DEM_Q6` (2‴ 에 붙일지는 1저자). ⏭ **1저자 결정**: W′ 새 ID · P1 작은 계산(벌크 cutoff·k 응력 안정성) · Q3″ 3항 점검.
    ✅ **1저자 '권장하는걸로 파이프라인을 다시 짜자' (09-25)** → `D-2026-09-25-wad-reference-state-policy` (active · 정책 · 결과 뒤): 참조·기판 **제약 상태 라벨** 의무 · SE|SE 두 참조 병기 ·
    comp1 V0 정본 불변(응력은 조건) · P1·P2 = '지정 comp1 셀 조건부' · P0 규칙 · 순서 v4. 계획 **§0″** (`wad_lpscl_agc_vgcf_plan_2026_09_23.md` · status v4) · DEM 초안 **§회신 3** (2‴ 부록 or 별도).
    ✅ P0 원출력 확인 — 네 잡 헤더 1 · NOT achieved 0 · `bfgs converged` 마지막 · 성분별 힘 < 1e-3 (`db/raw/wad_sese_4L_2026_09_25/lastrun_check_2026_09_25.txt`).
    ✅ 사후 아핀 분석 — Li 바깥 가운데 = 균일 전단으로 대부분 · **S 바깥 가운데 Li 는 아핀 빼도 1.33 Å** (Li 자리 이동 · 에너지 분해 아님). Q3″ 대조: 끝점 동일 ✅ · 같은 기판 = 정합 (a) 일 때 (권고) · 잔류 응력 = 조건 누락 → 결정으로 명시.
    ⏳ **② 벌크 수치 민감도 7 SCF** `db/inputs/wad_sese_bulk_sensitivity_2026_09_25` (cubic/epi × 52k4·70k3·70k4 + epi 내장 대조 07_epi_e52_k3 = 05 ± 1e-5 Ry) · 집계 `se_sym_slab.py --bulk_sens` (selftest 72/72 · 음성 5 · 돌연변이 3 빨간불) ·
    진단 R1(σ_yz 부호 같고 ≥ 5 kbar) · R2(ΔW′ 스프레드 ≤ 0.02) — **결과 뒤 정한 진단 규칙** · 슬랩 W 수렴 인증 아님. V100 발사 블록 전달. 그 다음 ③ A′ 사전등록.
    ✅ **② 끝 (09-25 18:14 · V100 27 min · 7/7 rc 0)** — 내장 대조 ✅ (2e-8 Ry) · **R1 ✅** σ_yz 10.8 kbar 네 설정 동일 · **R2 ✅** ΔW′ 0.0775 네 설정 동일(스프레드 0) ·
    70 Ry/k4 대비 −0.16 meV/atom (52/k3 가 벌크 에너지 차·응력에 사실상 수렴). 원자료 `db/raw/wad_sese_4L_2026_09_25/bulk_sens_result_2026_09_25.json`. ⛔ 슬랩 W 수렴 인증 아님.
    ⚠ ~/wad4l 은 git 저장소가 아니라 kgy rsync 사본 — 갱신은 플랫폼 문서 함정 ⑦ 식 (kgy `v100-serve` ref → `git archive | tar`) · `CODE_ID` 파일로 커밋 기록. ⏭ **③ A′ 파일럿 사전등록 카드**.
    ✅ **1저자 '이거 하게 전체적으로 하고 DEM 보낼 회신도' (09-25)** → **결정 7 = (a)** `D-2026-09-25-wad-lattice-matching-rule-a` · **A′ 카드 초안** `db/properties/wad_aprime_pilot_prereg_2026_09_25.json`
    (draft · 봉인 전 · 계산 0 — V2 직접 DFT · V3/V4 진단 · V5 프로브 조건 · G1–G6 · 갈래 0–3 · 140 GPU-h 제안) → ⏳ **Codex BY** `codex_BY_prompt_wad_aprime_pilot_prereg_2026_09_25.md` (발송 대기 · Q1–Q8).
    📨 **DEM 회신 2‴+부록 발송판** (`wad_dem_reply_draft_2026_09_23.md` §회신 2‴+부록 · 2‴ 미발송 확인 → 이 판) — 1저자 발송 대기. 선행 확인(카드 §선행): Ag PBE a · Ag/C PP 해시 · 빌더 selftest · V5 CPU 프로브.
    🔴 **Codex BY NO-GO (09-25 저녁)** — 봉인·본계산 보류 · 경로 찬성 · 재승인 최소조건 6 (`codex_BY_reply_wad_aprime_pilot_prereg_2026_09_25.md` · 원문). → **카드 v2** `wad_aprime_pilot_prereg_v2_2026_09_25.json`
    (조성 4층 정정 · SE 부분 고정 마스크 + 결정 7 개정 `D-2026-09-25-wad-lattice-matching-rule-a-amend-1` **proposed** · G5 비자명 W 쌍 5 · 분모 고정 · Ag₁₃·C₂₄H₁₂ 제외 · −TS 삭제 · 끝점 양쪽 ≥ 8 Å + dipfield eamp=0 · G2 `--interface_check` 구현(96/96 · 돌연변이 4 빨간불) ·
    G3/G4 대상군별 · 장치별 한도 · 허용 문구 P1′ 한정 · 단계별 봉인 S1–S4). ⚠ **V5 ≈ 246 GB 추정** (SE|SE 32 GB 스케일 · Ag 19 e) → RESOURCE_BLOCKED 예상 → 갈래0 (G5 NOT_TESTED · UMA 예측 내부 전용). V3/V4 37–42 GB gabia 만.
    ⏭ **1저자 확인 권고 5** (카드 v2 `⭐_1저자_확인_필요`): ① 부분 마스크 + 개정 비준 ② Ag₁₃ 제외 ③ 갈래0 내부 전용 ④ 표본 5 정의 ⑤ V5 자원 현실 → Codex BY 재심 → S1 봉인.
    📨 **DEM 3차 회신 수령** (정합·라벨 수용 · 부록 값 미사용 · 부탁 1 잔류 응력 GPa · 부탁 2 시나리오는 DEM 초안) → 회신 4 초안 (`wad_dem_reply_draft_2026_09_23.md` §회신 4 · PBE 응력 GPa 지금 · PBE+D3 는 선행 배치 12·13 뒤).
    🧪 **선행 배치** `db/inputs/wad_aprime_prep_2026_09_25` (08–11 Ag fcc·그래핀 vc-relax PBE/PBE+D3 · 12·13 comp1 D3 relax/vc-relax · 읽는 규칙 결과 전) · 집계 `se_sym_slab.py --aprime_prep` (음성 6) · ⛔ Ag/C(/H) PP 해시 kgy 에서 받아 채운 뒤 V100 발사.
    🔴 **Codex BZ NO-GO (09-25 밤)** — v2 봉인·S2 보류 · 비준 5 유지 · G2 우회 4경로 실측(마스크 누락/[-1]/흡착층만 통과 · NaN 통과 · 흡착면 뒤집힘 통과 · V2 경로 없음) · G5 종결별 평균 누락(상쇄 반례) · G3 조작 미정의 · G5↔G3/G4 · S1/S3 경계.
    → **G2 재작성** (`interface_check` 마스크 필수 + `fixed_mask_policy` 집합 일치 · 비교 전 유한성 · `normal_sign(init)` · V2 모드 substrate/ads + 측방 제약 · CLI `--fixed_idx` 필수 · `--mask_policy`) selftest **110/110** · BZ 음성 9 · 돌연변이 5 빨간불 · **카드 v3** `wad_aprime_pilot_prereg_v3_2026_09_25.json`
    (G5 종결별 평균 복구 + G3·G4 PASS 전제 · G3 두 셀(영상/거리 분리) · Ag₄ 비영 초기 자화·절대자화 · S3 전 예외 4 · S1 봉인 범위 확대 · registry 결정적 규칙 · 결정 내용 digest · RESOURCE_BLOCKED 예상/실측) · DEM 회신 4 §3 → 확인 요청.
    ⏭ **1저자 확인 3** (`⭐_1저자_확인_v3`: G5 v1 기준 복구 · Ag₄ 절차 · S1 범위) → **Codex CA** `codex_CA_prompt_wad_aprime_pilot_prereg_v3_2026_09_25.md` (발송 대기) → S1 봉인 전 채울 것: UMA 체크포인트 sha·fairchem 버전 · 선행 배치 값 · 흡착층 빌더.
    🔴 **Codex CA NO-GO (09-25 밤)** — BZ 이행 인정 · 남은 것: V2 측방 마스크 **선택 입력**(생략·Ag 만·부분집합 통과 · P0) · `int(i)` 자동 변환(0.9·−0.9·True · P1) · G3 |ΔW|·끝점별 기록·문구 · G5 문구 종결별 · CPU 프로브 예외 누락·electron_maxstep · registry 중점 주기영상 반례.
    → 코드: 금속 기판 모드 측방 마스크 **필수 + 흡착층 전체 집합** · PS₄ 모델 측방 제약 깃발 · `_validate_idx` 타입 검사(변환 없음) · CLI 파싱/검증 분리 — **120/120** · CA 음성 10 · 돌연변이 8 빨간불 · CLI JSON 소수 rc 2. **카드 v4** `wad_aprime_pilot_prereg_v4_2026_09_25.json` (G3 기록·문구 · G5 종결별 · 프로브 CPU/GPU·scf·원출력 보존 · registry Σ·최소영상·동률·감기 · Ag₄ 정책 문구 · S1 빈 항목 봉인 불가).
    ⏭ **Codex CB** `codex_CB_prompt_wad_aprime_pilot_prereg_v4_2026_09_25.md` (발송 대기). S1 결박값은 카드 밖 `db/properties/wad_aprime_s1_bindings_2026_09_25.json` 에 모은다 (재심 중 카드 SHA 불변):
    🔒 **S1 봉인 (09-25 밤 · 1저자 '가장 권장하는거면 비준')** — 카드 v5 content_digest `126aa58ebdc4803b…` · 결정 `D-2026-09-25-wad-aprime-s1-seal` active · UMA 추론 모드 **default** 확정. 본문 불변 (정오·개정은 별도 파일). ⏭ **S2**: 빌더로 기하 생성 → 최적화 전 마스크·registry·좌표 sha 기록 → UMA+D3 이완(gabia uma env · b2o3 끝난 뒤 GPU) → `--interface_check` → 분리 셀 CPU 프로브 → GPU 프로브 → S3 봉인.
    📨 **DEM 회신 4 발송본** `kb/projects/wad_dem_reply_4_send_2026_09_25.md` (09-25 · 1저자 발송).
    ✅ **S2 끝 (09-25 22:40 gabia)** — UMA+D3 이완 12/12 수렴 (default · simple-dftd3 1.6.0 · 첫 발사는 MixedPBCError 로 전부 실패 → 3축 pbc 수정 `e472bef31` 재발사). 후검: **후보 9** (V2×4 · V4_s_outer_A · V5×4) · **INCOMPLETE 3** (V3×2 Ag₄ 개방 +16–17 % · V4_li_outer Li 1.46 Å). gabia 가 산출물 커밋 `30e1e90eb`.
    📦 **S3 패키지** `db/inputs/wad_aprime_s3_2026_09_25` (manifest sha 2a0e9a9b5f5fef4a… · 잡 38) + D3 결박 검사 입력 `wad_aprime_d3check_2026_09_25` (외부 −0.5037974 Ry). ⏭ **1저자 S3 비준** → S4 · 비준 전 가능: gabia CPU 프로브 5 (예외 ③) · V100 D3 결박 검사 (예외 ②).
    🔎 **CPU 프로브 (09-25 밤 · gabia · 70 Ry · 분리 셀)** — V5 ×4 **89–109 GB** → **RESOURCE_BLOCKED (실측)** → G5 **NOT_TESTED** · UMA 예측 내부 전용 (갈래0). V4_s_outer_A 70 Ry 52.4 GB → G4 e70 불가 · 기본 52 Ry 프로브 다음 → GPU 시험은 b2o3 s4 뒤. `db/raw/wad_aprime_s3_probe_2026_09_25/`.
    🔒 **S3 봉인 + 개정 1 비준 (09-26 · 1저자 '비준')** — `db/properties/wad_aprime_s3_seal_2026_09_26.json` (a1074e51b64d98d2…) · manifest 2a0e9a9b5f5fef4a… · 결정 2건 active. **S4 실행 집합**: V2 relax 4 (V100 · 발사 블록 전달) → 2단계 `--v2_ed` → V4_s_outer_A 9 (gabia GPU 시험 · b2o3 s4 뒤). 제외 V5 전부·⑤·V4 e70 → **G5 NOT_TESTED**. W_UMA+D3 := W_UMA + ΔE_D3,QE.
    🔴 **D3 결박 검사 FAIL (09-26 00:01 V100)** — QE −0.50431702 vs 외부 −0.5037974 Ry (|Δ| 5.2e-4 > 1e-5). 컷오프가 ~60 % · 잔차 0.2 mRy 구현 차. 문턱 불변 → **개정 1 proposed** `wad_aprime_pilot_prereg_v5_amendment_1_2026_09_26.json` (UMA+D3 W 의 D3 = QE 출력 · 외부 D3 는 기하 생성 라벨 · 새 계산 0) → 1저자 비준 (S3 비준과 함께).
    📨 **DEM 4차 회신 수령** (라벨 수용 · 한 기하 성립 (a)(b) · 시나리오 i–iv 초안) → **회신 5 초안** (§회신 5): (i) 기준선은 V2 만 · SE 계면 V5 RESOURCE_BLOCKED 예상 → 미리 정정 · (iv) V2 가능 · (ii)(iii) 내부 전용 기본. 1저자 발송 대기.
    🟢 **Codex CB 조건부 GO (09-25 밤)** — 코드 차단 해제 · 조건 4 (UMA 결박 · 선행 값 · 빌더+registry 구현·시험 · registry 전역 d_min 동률/Σ∖{A} 차단) → 전부 이행: **`tools/wad/build_aprime_interfaces.py`** (V2·V3·V4·V5 · `registry_select` · `make_endpoints` · 20/20 · 돌연변이 4) ·
    **카드 v5 = S1 봉인 후보** `wad_aprime_pilot_prereg_v5_2026_09_25.json` (UMA·PP·D3·코드 sha 결박 · 선행 값 · registry 명세 · GPU 프로브 문구). ⏭ **1저자 비준** (카드 + 추론 모드 default) → content_digest 봉인 → **S2** (기하 생성 · 마스크/registry 기록 · UMA 이완 · interface_check · 프로브).
    ✅ **선행 배치 끝 (V100 09-25 21:21 · 9/9 rc 0 · 깃발 0)**: Ag a₀ PBE 4.1448 · **PBE+D3 4.0705** (실험 4.086) · 그래핀 2.4668/2.4660 · **정합 변형률(PBE+D3 격자)** P1 +0.85/−0.19 % · P2 +1.94/+0.89 % · V2 +1.08 % → 3 % 규칙 미발동 ·
    **라벨 응력 PBE+D3** 입방 고정 xx +0.71 · yy +2.65 · zz +2.66 · yz −1.11 · **p −2.01 GPa 인장** / epi c 9.40 (−6.5 %) — ⚠ 지정 셀이 D3 아래 인장 상태 = 라벨 조건 (참조 셀 변경은 새 결정 · 1저자). DEM 회신 4 표 채움 · `db/raw/wad_aprime_prep_2026_09_25/`.
    ✅ **UMA 결박 (gabia 09-25)**: fairchem.core **2.19.0** · torch 2.8.0+cu128 · cuda 12.8 · `uma-s-1p1.pt` **sha 07068e9c76702ca1** (1119 MB · HF snapshot be289645…) · task omat · 추론 모드 제안 default (1저자 확인). ⏳ 선행 배치 값 · 흡착층 빌더(registry 구현).
    🔧 `run_sese_gpu.sh _done`·`parse_pw` **vc-relax 갈래 추가** (옛 판은 vc-relax 를 SCF 기준으로 통과 — 실제 통과한 실패 이완은 없음 · 05 는 bfgs converged 확인) · `watch_lpsocl_400ps.sh` 남은 런 수 표 기준 (kgy b2o3 '남은 0런' 오기 · 음성 2).
    🔴 **러너 결함**: 기록된 `pw.x PID 563677` 이 **없다** (ps 빈 줄) — `pgrep -P mpirun | head -1` 이 pw.x 가 아닌 자식을 잡았거나 사라진 PID 다.
    완료표 `peak_self_MiB` 가 **세 잡 모두 0** = 자기 VRAM 측정이 한 번도 안 됐다 (컨테이너 PID 공간 ≠ nvidia-smi PID 도 의심). 가드는 mpirun 을 죽이므로 안전은 유지 ·
    기록 필드가 거짓 0 이다 ('조용히 틀린 경로'). V100 진단: 트리 = 래퍼 563671 → mpirun 563691 → **pw.x 563705** · nvidia-smi 는 **호스트 PID 3312066**.
    ✅ **러너 수정** (`run_sese_gpu.sh` ⑩): comm 으로 pw.x 찾기 · 트리 통째로 PID+comm 대조 정지 (종전엔 **래퍼만** TERM → pw.x 고아 · 죽은 PID 가 재사용되면 남의 프로세스) ·
    못 잰 칸 '—'. selftest 48/0 · 돌연변이 5종 빨간불. ⚠ V100 의 **지금 인스턴스는 옛 코드** — 가드 발동 조건(44 GB · 호스트 4 GB)이 그 기계에서 사실상 안 걸려 재시작 안 함.
    ⛔ **정정 (09-25)**: 위 '가드 발동 조건이 사실상 안 걸린다' 는 **틀렸다** — V100 발사가 `KILL_MIB=32700` 이었고 S 바깥 이완 피크 32,378 MiB 는 **322 MiB** 차였다.
    발동했으면 옛 `_stop` 이 래퍼만 죽여 pw.x 가 고아로 남았다 (운이었다).
    📊 (09-25 최종은 위 결과 기록) **중간값 (판정 보류 · 인용 금지)** `--collect`: 무이완 W_sep PBE **1.103** · PBE+D3(BJ) 2체 **1.518** J/m² (A 101.10 Å² · n 4.0) ·
    −TS 경고 없음. ⚠ 경보 v2 는 **이완 PBE W_cleave** 에만 건다 — 무이완 1.1 은 경보 대상 아님 (무이완 ≥ 이완 이 정상).
  · 🆕 **웹앱 `/adhesion` — 점착 파이프라인 섹션 (09-24 · 1저자 요청)**: 원장 `db/pipelines/adhesion_pipeline.json` 하나를 읽는다
    (단계 · DFT→DEM 인계 규약 · 계 · 실행 · 리뷰 · 위험 · 열린 것 · **누적 로그**) + 결정은 scope `adhesion.` 실시간.
    ⛔ 판정 전 물리값은 원장·화면에 싣지 않는다 · COMSOL 은 이름만 (관할 밖 — 1저자). 시험 `webapp/tests/test_adhesion.py` 13.
    ⏭ **새 사실은 원장 `log` 에 한 줄씩 덧붙인다** (이완 끝나면: 판정 줄 + 결과 기록 파일 경로).
  · 대시보드 파생 카드 5장 (점착 원장 최신 줄 · b2o3 사건빈도 봉인 · Nd C1 · cascade fail-closed · 세미나 3편) + 축 '점착 · 계면' ·
    worklog 09-23·24 8항목 + 빈 구간(09-15~22 · 커밋 340 실측) 주석 · aJ 오독 다섯 번째 자리(d_rel_targets) 정정.
    (러너에 NP · PSEUDO_DIR · NO_LOCK 추가, GPU 사용량은 장별 최댓값). gabia 예외는 **한 번도 발동하지 않은 채** 소멸.
  · ✅ **문헌 3편 인입·병합** (1저자 제공 PDF · 수치는 메인이 PDF 텍스트로 재대조): `pustorino2025_…`(LPSCl 파괴에너지 = 2γ · (100) 화학량론 벽개 ≈ 0.47 · (110) 0.37 J/m²) ·
    `maurer2015_…`(Ag|그래핀 분산 7방법 0.19–0.45 J/m² — 0.3 경계를 가로지른다) · `giovannetti2008_…`(Ag 약결합군 · LSDA · 화학흡착 Pd ≈ 0.52 J/m² = "구간 ≠ 기전").
    ⚠ 05:38 턴 중단 때 첫 실행 셋이 **같이 취소**됐다(그림만 남음) → 재실행. 도는 동안 Esc 금지.
  · ✅ **comp1 SE 종결 재계산**: PS₄ 보존 창 = Li 8 + free S 2 · Cl 0 → Li 2|6 틈 두 곳만 +2/+2 (Tasker 보상) · 4|4 는 극성. DEM 의 "Cl 쪽" 은 comp1 절단으로 불가.
  · ✅ **QE D3 3체 기본값 = TRUE** (7.4.1 INPUT_PW.def) — repo QE 생성기 어디도 `dftd3_threebody` 를 안 적는다 ⇒ `vgcf_hbn` "D3BJ" 는 실제 D3(BJ)+ATM. 표기 정정 여부 = 1저자.
  · ⏭ **DEM 회신 초안** `kb/projects/wad_dem_reply_draft_2026_09_23.md` — 1저자 검토 후 DEM 세션(`claude/stoic-knuth-NObVQ`)에 붙여 넣기. 그쪽 트랙 §6 의 두 오류(Maurer "mJ/J 판별 영향 없음" · Pustorino 0.20 = 벽개) 정정 포함.
  · ⏭ **1저자 결정**: SE 종결 (가 대칭 두 장 / 나 비대칭 한 장) · "Cl 쪽" 처리 · D3 ATM 끄기 · `vgcf_hbn` 표기 정정 · NCM 상태 정책/U · (DEM 답 오면) 헤드라인 W_sep 수용 여부.
  · 내부 리뷰(Fable) = **NO-GO (v1)** → `kb/reviews/internal_review_wad_agc_fable_2026_09_23.md`. P0 4건 원문 대조 확인 · v2 반영:
    ① 기준값은 **이완만 · uma-s-1p1** (v1 은 800 K MQA 로 읽었다 — 결과 문서 `kb/results/adhesion_final.md` 를 안 봤다)
    ② SE 는 **정방 20.11 Å** 인데 계면 셀은 육방 351.5 Å² — 빌더가 **wrap** (추정, 원본 유실) ⇒ 기준값 숫자 재사용 안 함, 정방 셀에서 NCM 부터 재계산
    ③ 검증 짝 = UMA ↔ **PBE(D3 없음)** · 물리흡착 짝은 DFT+D3 직접 ④ 옛 숫자 병합 금지 (출판 1.277 = 20 중 5 seeds 선별).
  · ⛔ **내 오류 정정**: 커밋 `b27dd3b8e` 에서 실험값을 *"0.194 J/m²"* 로 옮겼다 — **AFM aJ** 다(원장 오독 승계). `adhesion.json` 에 정오표 블록
    (`⛔_정정_2026_09_23_실험값_단위_aJ`). *"v5 는 실험의 5배 · 0.19 → 물리흡착 급"* 철회.
  · ⛔ repo 금지 규칙 *"MLIP 절대값 인용 금지 (σ · W_ad)"* (`webapp/fairchem.py`) — DEM 에 UMA 절대값은 못 넘긴다 → 결정 §6-1 (DFT 값 or 같은 프로토콜 비).
  · ⏭ 1저자 결정 5건 (계획 §6) · V100 백업 슬랩 셀 확인(wrap 가설, 선택) · Codex 회신 오면 v3 → 카드 봉인 → decisions.json proposed.
  · 요청서의 *"Fan 2026 K_IC → G_c 는 CLAUDE.md 에 이미 반영"* 은 **repo 의 어느 CLAUDE.md 에도 없다** (litdb digest 에 K_IC 0.2–0.4 MPa·m½ 은 있다 — 리뷰 논문의 2차 인용).
- ✅ `webapp/tests/test_v3_records.py::test_gallery_carries_hazard_and_policy` — 테스트가 정책 접두어를 **둘만 복사**해 두고
  정책은 셋이라(`oxidation_stability_cascade` 누락) 정상적으로 막힌 파일을 "평범한데 막혔다" 로 읽었다 →
  `artifact_policy.is_governed()` 를 직접 쓰게 고침 · 음성(평범한 파일에 policy 주입 → 잡힘) 확인.

### ⏭-NOW-v. 2026-09-22 낮 — **논문 4편이 우리 원장을 세 군데 고쳤다**

> 앞 블록 ⏭-NOW-u(같은 날 오전, li2s BU)는 **그대로 살아 있다** — 회신·부록 전달과
> 블록규칙 개정 여부가 여전히 막고 있다. 이 블록은 그 위에 얹힌 문헌 트랙이다.

#### 인입 완료 4편 (digest + 병합대기 · 커밋 `3bf606fe4` → `381b161c9`)

| 편 | 한 줄 | 우리 쪽으로 튄 것 |
|---|---|---|
| **schwietert2020** | 2.24 V 는 **층②(골격보존 탈리튬화)**, 우리 2.256 은 **층①(분해 개시)** — 0.016 V 차는 **서로 다른 두 추정량의 우연** | 🔴 **Zhu15 3.4× 감사** (아래) |
| **marcolongo** | LGPS `H_c` = 0.36/0.42/0.61 (전부 <1) | SI `Fig. S3` 의 "2 ps 이후 기울기" 가 **우리 MSD 창 하한의 외부 출처**가 됐다 |
| **haruyama2014** | 우리 v5 기하의 **프로토콜 원전이지 셀 수치 원전이 아니다** | 🔴 SCL 정량 0건 → 방법론 카드 §2 말미 신설 · 🟡 `refs.json[37]` 귀속 정정 제안 |
| **wang2022**(Canepa) | 🟡 **선점 아님**(아르지로다이트 슬랩 0개) · 저자가 공백을 직접 지목 | 🔴 **음극 반응식 방향 뒤집힘 → BLOCKED** (아래) |
| **morgan2021** | 무질서 기전의 정본인데 **D 0 · Ea 0 · 배열 1개 · 시드 1개 · 온도 1점** | ✅ BU 의 "구조 산포" 물음에 **"문헌에도 없다"** 가 답이다 |

#### 🔴 새로 막는 것 3건

1. **`HZ-anode-b2o3-reaction-direction` (BLOCKED)** — `anode_interface_b2o3.json` 의
   `reaction` 문자열 네 줄이 **Li 을 내놓는 방향**이다(0 V 는 흡수 쪽인데).
   그래서 **Li₂S 가 없고 원소 S 와 자유 Li 가 공존**한다. 원인 후보는
   `tools/oxidation/anode_interface_stability.py:78` nearest-V 선택인데,
   도구가 `evolution`(부호 있는 Li 흡수량)을 안 적어 **방향을 가를 수단이 없다.**
   ⏭ **할 일**: `evolution` 기록 + 방향 선언 넣고 재실행 → RESOLVED 로 올린다.
   그때까지 **반응식 문자열 인용 금지**, 산물 목록은 *"재확인 대기"* 단서와 함께.
   ⚠ "결론은 안 바뀐다" 는 **확인된 게 아니다** — "확인 안 됐다" 가 맞다.
2. 🔴🔴 **Schwietert × Zhu15 3.4× 감사 — 같은 날 정체가 드러났다. 우리 코드 버그다.**
   ⛔ **`window_V` 전량 BLOCKED** (`HZ-esw-reduction-limit-label`, 커밋 `2189d6478`).
   · **원인**: `esw_cascade_batch.py:417-421` 과 `constrained_esw.py:91-94` 가 똑같이
     `red = max(V | evolution > 1e-6)` 을 쓴다 ⇒ **Li 교환이 0 인 행**(= 진짜 안정 구간의
     아래 가장자리)이 필터에서 빠져 환원 한계가 **항상 한 계단 아래**로 잡힌다.
   · **실측**: 1.242 V 는 아직 **Li 을 5개 흡수**한다(`+5Li → 5Li₂S + LiCl + P`).
     교환 0 은 **1.717 V**. ⇒ 창은 **1.717–2.256 = 0.539 V** 이지 1.014 V 가 아니다.
     cascade 전수 재유도: **356 행 중 0 행 빼고 전부 넓다** (중앙 **+0.475** · 최대 **+0.676 V**).
   · ✅ **우연이 아니라 같은 양이었다** — 우리 "OCV" **1.717** 이 `[Schw21]`·`[Zhu15]` 의
     환원한계 **1.72** 와 **0.003 V** 차다. 위에 적혀 있던 *"같은 양인지 미확인"* 은 **닫혔다.**
   · ✅ **2026-09-22 실행 완료 (gabia, `--audit_edges`)** — 배제 포함/배제 두 판을 돌렸다.
     **우리 1.717 / 2.256 이 라이브 MP 조회에서 그대로 재현됐다**(저장된 steps 가 아니라 실제 상도).
     **배제 몫 = 정확히 +0.116 V**(`our_dft_baseline.md` 의 "LiS4 포함 시 2.14" 와 소수점까지 일치).
     🔴 그리고 **실제로 빠진 상은 `LiS4` 하나뿐**이다(107 → 106) — `SCl3`·`Li5PS4Cl2` 는
     이 chemsys 에 **없다**. *"상 3개를 뺐다"* 는 서술은 과하다.
     · **환원 가장자리는 배제와 무관**하다(두 판 모두 1.717).
     ⇒ **남은 미해결은 산화 한 변 `0.130 V` 하나**다(2.14 vs 문헌 2.01).
     ⛔ *"MP 판본 탓"* 으로 단정하지 않는다 — 이 계산은 판본을 못 가른다. 0.130 은 **다른 축 전부의 상한**이다.
     ⏭ 산출물 회수: gabia `/data/work/runs/esw_edge_audit_comp1_2026_09_22.json` → repo.
   ⇒ 감사는 **"닫혔다" 가 아니라 "3.4× → 1.86×, 어긋나는 변이 둘에서 하나로"** 다.
   ⏭ 여전히 *"우리 창이 실험 1.25 V 와 잘 맞는다"* **쓰지 않는다.**
   ⏭ **닫는 계산 1건 (이 컨테이너엔 pymatgen 이 없다)**: comp1 프로파일 재실행으로
     `evolution == 0` 구간 양 끝을 직접 출력 + **LiS₄ 포함/배제 두 판**.
     ⚠ 던지기 전에 보고량 카드 — *"환원 한계 ≡ Li 교환이 0 에서 벗어나기 시작하는 가장 높은 φ"*.
   ⏭ **도구 수정은 1저자 결정 후에.** cascade 인쇄값을 전부 움직이는 정의 변경이라
     조용히 고치지 않는다. `constrained_esw.py` 는 그 행을 **계산조차 안 하므로** 먼저 추가.
   ⏭ 라벨 교체(`our_dft_baseline.md` L20 *"환원 한계 1.717(= 종전 OCV) / 두 번째 평탄 1.242"*)는
     **재실행 후에** 인쇄한다. 지금은 값 보존 + 🔴 단서만 붙여 뒀다.
3. **Morgan 의 "협동 운동"** — 본문 축자가 *"concerted ion motions in **all our systems**"*
   인데 그 중 **네 계는 확산이 0** 이다. ⏭ `jeon2026_concerted_li_motion_…` 을 인용할 때
   이 견제를 같이 건다. **"협동 운동 관측" 을 성과로 쓰지 않는다.**

#### ✅ 같은 날 닫힌 것 3건

- **`computational_methods_canonical.md:44`** 가 *"공간전하층 상세는 §2 말미"* 라고
  가리키는데 **그 자리가 비어 있었다** (K_IC·μm 입자역학은 있고 SCL 만 없음).
  Haruyama 실독으로 근거가 생겨 채웠다. 이제 "문헌도 정성뿐" 이 **확인된 사실**이다.
- **`beta-gate.md` §7-3 정정** — *"He 2018 은 원칙만 말하고 창을 고정하지 않는다"* 가
  **틀렸다**. 원문+SI+`pymatgen-analysis-diffusion` 코드 확인: 하한 `0.5a²`(코드 4.5 Å²),
  상한 `<0.7 t_tot`(코드 0.5), **코드에만 있는 최소창 게이트**까지 있다.
  ⚠ β 문턱 0.8 판정은 **안 바뀐다**(He 가 고정한 건 적합 창이지 β 문턱이 아니다).
- **`db/external/PENDING.md` P3 닫음** — `## ✅ 닫힌 것` 절 신설해 옮겼다(지우지 않았다).

#### 🟢 BU 에 쓸 외부 앵커가 생겼다 (카드에 박음 · 규칙은 안 건드림)

`kim2024` Table 1, `Li₆PS₅Cl` 50 % **두 배열**: Ea 차 **AIMD_PBE 9 meV · MTP_optB88 10 meV**
(원문 표로 직접 대조). ⭐ 그런데 **같은 두 배열의 σ_RT 는 23.3 vs 37.1 = 1.59 배**다 —
**Ea 9 meV 인데 σ 1.6 배**. D₀ 가 같이 움직인다 ⇒ *"Ea 산포가 작으니 σ 도 작겠지"* 금지.
⚠ 결정·대칭구별·n=2 라 **유리 시드 산포의 하한 참고점**으로만. ⛔ 이 값으로 R 문턱을
다시 계산하지 않는다(문턱은 χ² 분포에서 나온다).

#### ✅ 인입 트랙은 닫혔다 (2026-09-22 종료)

원 PDF **1~15번 전부** digest + 병합 완료. `build_index --check` 가
**digest 313편 · 어느 인덱스에도 없는 것 0편 · DFT 179/179 전부 편입**을 준다.
화면 시험 `test_recent_digests_are_on_every_litdb_surface` **PASSED**.
신설된 §J 블록: **J-29~J-41** (13개). 커밋 `b0260753a` → `288e42c8a`, 총 72개.

#### ✅ A·B 는 **같은 날 결정되고 적용됐다** · C·D 는 사용자 실행 대기

⛔⛔ **용어 정정 2판 (2026-09-22) — 1판도 틀렸다. 이게 정본이다.**

**`1저자` 는 트랙마다 다르다.**

| 트랙 | 1저자 | 뜻 |
|---|---|---|
| **ESW · cascade · 우리 DFT 기준선** | **사용자 본인** | 결정이 그 자리에서 난다. 통지할 제3자가 **없다** |
| **li2s (소셀 유리 · 회신 letter A→BU)** | **사용자가 아니다** | 규칙·판정을 준 **외부 1저자**가 있고 **회신이 필요하다** |

· 1판(*"넷 다 1저자 결정 대기"*)이 틀렸다 — A·B 는 대기가 아니었고 C·D 는 결정이 아니었다.
· 2판(*"1저자 = 사용자라 통지 대상 없음"*)**도 틀렸다** — 그건 **ESW 트랙에만** 맞는다.
⚠ 그래서 규칙은 이렇게 적는다: **결정 항목을 쓸 때 트랙을 먼저 쓴다.**
트랙 없이 *"1저자 결정"* 이라고만 쓰면 **어느 쪽인지 알 수 없고 실제로 두 번 틀렸다.**

| # | 무엇 | 상태 |
|---|---|---|
| **A** | ESW 환원한계 라벨 (**ESW 트랙 — 사용자가 1저자**) | ✅ **결정·적용 완료**(`8a0e202d3`). 코드 1곳 통합 · 356 행 재유도(82 행은 표시) · hazard **CONDITIONAL** 로 하향 · `our_dft_baseline.md` 라벨 교체 |
| **B** | BU 블록규칙 (**li2s 트랙**) | 🟡 **②로 잠정 적용**(`f418bb6ee`) — **확정 아니다.** 규칙을 준 것은 **외부 1저자**이고 회신 대기다. ②가 ①의 상위집합(연속 정수면 수식 동일)이라 먼저 넣었고, ①로 오면 `/Δb` 한 줄 빼면 되돌아간다. `results_seen` **false** 라 편향 없음 |
| **C** | BU 회신 + 부록 전달 | 🟡 **사용자 실행** — 파일 둘 다 `kb/reviews/` 에 있다 |
| **D** | gabia A6000 확인 | 🟡 **사용자 실행** — 비어 있으면 담금질 4시드가 8일 → 절반 |

**우리 손으로 할 수 있는 것** (결정 없이 진행 가능)
1. **음극 반응식 방향 수정** — `anode_interface_stability.py` 에 `evolution` 기록 +
   방향 선언. **수용 게이트 2줄이 이미 원장에 있다**(Li 계수 양수 · 원소 S 없고 Li₂S 있음).
   ⚠ MP 접근이 필요하다(이 컨테이너는 UA 문제 이력 있음 — CLAUDE.md §MP 참조).
2. **떠 있는 표 행 305건** — `build_index --check` 가 이제 보고한다. ⛔ "빈 줄만 지우면
   된다" 가 아니다: 위쪽이 표가 아닌 자리는 **자기 헤더+구분자가 필요**하다. 편집 판단.
   고친 뒤 `check_orphan_rows` 를 **종료코드에 승격**하고 selftest 음성⑤를 뒤집는다.
3. 원장 후속(급하지 않음): `md_conductivity_protocol.md` §3 · `kb/concepts/md.md` §6 ·
   `haven_ratio_measured_*.json` 문맥 · pranami kb 5건 · `extract_figures.py` 3건
   (**한 쪽에 캡션 2개면 y좌표로 분할** — lomeli `fig_S2` ≡ `fig_S3` 바이트 동일이 실증) ·
   `refs.json` 의 `zhu2015` 엔트리 제목·저자 정정 + `schwietert2021` 신규 ·
   `cascade_screening_funnel*.json` 의 G4 `literature_analog` 에 sjolin2023.
4. 🟡 **`[Dutra25Rev]` ref 218 귀속 재확인** — 거기 달린 `Fig. 5c` 는 그 논문 그림이 아니다.

#### 🧭 이번 라운드의 교훈 (다음 사람용)

- **칸수 검사는 *버려짐*은 보는데 *밀림*은 못 본다.** jung2026 §C·§D 와 schwietert §E 가
  **§B 의 열순서**로 쓰여 있었는데 칸 수가 넷으로 같아 `build_index.py --check` 가 통과했다.
  **하루에 세 번 걸렸다** — 세 번째(lomeli)는 원인이 달랐다: 칸을 더 쓴 게 아니라
  `` `|ΔE_rxn|<100` `` 의 **파이프 미이스케이프**였고, 같은 문구가 같은 파일의 다른 행에는
  **이미 이스케이프돼 있었다**. ⇒ 병합할 때 **헤더 열 순서를 직접 읽는다**. 칸 수로 못 가른다.
- ⛔⛔ **`✅ 0건` 이 지표가 아니었다.** `check_tables()` 는 `헤더+구분자` 로 시작하는 조각만
  본다 — 표가 **빈 줄로 조각나면** 그 뒤 행은 검사에서 통째로 빠진다. 실측 **305건**이고,
  **도구가 생성하는 `INDEX_DEM.md` 만 0건**이었다(사람이 손대는 셋은 전부 걸렸다).
  `check_orphan_rows()` 신설(`288e42c8a`). **초록불을 볼 때마다 "이 검사가 이 줄을 봤나" 를 묻는다.**
- **독립성을 과하게 주장하지 않는다.** 오늘 *"세 번째 독립 확인"* 이라고 썼다가 원문
  참고문헌을 대조하니 **Wang22 ref 14 = Chaney24 ref 11 = 같은 Wenzel 2018** 이었고,
  Wang/Canepa 의 분해식은 **그 Wenzel 소환**이었다 ⇒ 독립은 셋이 아니라 **둘**(실험·동역학).
  ESW 관례 표본 셋도 전부 Zhu 2015 계보라 *"관례가 일관된다"* 까지만 적었다.
- **원장의 `fix`/`what`/`why` 는 기계가 읽는 필드다** — 점 들어간 약어(`f.u.`·`cf.`·`et al.`)를
  쓰면 검사기가 **키 경로로 읽는다**(실측: `f.u` → 최상위 키 `f` 없음으로 빨간불).
- **가리키는 곳이 비어 있으면 경계가 약해진다** (위 SCL 건). 포인터를 쓸 때 대상이
  실재하는지 같이 본다.
- **원문을 못 구해 2차 요약에 기댄 문장은 원문이 오면 반드시 다시 본다** (위 beta-gate 건).
  `PENDING.md` 를 닫을 때 *"이 항목이 막고 있던 문장"* 을 같이 훑어야 한다.

---

### ⏭-NOW-u. 2026-09-22 오전 — **li2s 회신 BS·BT·BU · 합의를 코드로 · 🟡 블록규칙 개정 여부 회신 대기**

#### ✅ **막혀 있던 것이 풀렸다 — 회신 BU 에서 판정 규칙 확정** (2026-09-22)

BT 의 IQR 초안은 **폐기**됐다. 1저자가 분산비 판을 제시했고 검산해 **그대로 받았다**.
카드에 박았다 (`…glass_md_estimand_…json` §`✅_결과전_확정_회신BU_…`).

```
σ̄²_within = 시드별 부트스트랩 σ²(Ea) 의 **평균**   ·   s²_seed = 시드별 Ea 표본분산
R = s²_seed / σ̄²_within          귀무(구조 산포 없음) 아래  R ~ χ²₄ / 4

  R > 4.45          ⇒ 구조 산포 있음      (단측 p < 0.00135 · SD 비 2.110)
  2.37 < R ≤ 4.45   ⇒ 시사적, 판정 보류   (SD 비 1.540)
  R ≤ 2.37          ⇒ 구조 산포 **미검출**. ⛔ *"통계로 설명된다"* 고 쓰지 않는다.
                       검출한계(σ_struct ≈ 2 σ_within)를 같이 적는다
```

🔴 **내 IQR 초안은 두 군데 틀렸다** — ① n=5 의 IQR 이 SD 보다 **더 흔들린다**
(모의 20,000 회: 상대산포 IQR **0.573** vs SD **0.365**) ② `IQR ≈ 1.349 σ` 는 **모집단**
관계인데 **n=5 표본**에 썼다(표본 평균비 **1.053**). 더 나쁜 통계량에 **28 % 틀린 상수**.

**같이 확정된 것 셋**
· **블록 길이 규칙** (값은 나중, 규칙은 지금): `σ(b)` 가 **연속 세 b 에서 상대변화 ≤5 %**
  인 최소 `b`. plateau 안 나오면 **블록을 안 고르고 판정 보류** · `b` 는 **전 시드 하나로 고정**
· **부트스트랩**: 세 온도 블록을 **한 번에 재표본해 Ea 를 직접 적합** (온도별 D 전파 금지 —
  그 단계에서 대칭 가정이 들어온다)
· **`reduced χ²` 열 추가** (dof=1 이라 약하지만 온도 역전은 즉시 드러난다)

#### ✅ 합의 3건을 **코드로 내렸다** — 그리고 🔴 **블록 규칙의 구멍을 찾았다** (`64b6488e0`)

| 합의 | 어디 |
|---|---|
| 3 온도 동시 재표본 → Ea 직접 적합 | `msd_diffusive_check.py:joint_ea_bootstrap()` · CLI `--ea_boot` |
| 블록 plateau 규칙 | 같은 파일 `choose_block_plateau()` · CLI `--block_scan` |
| `reduced χ²` (dof 1) | 같은 함수가 점추정·재표본 양쪽에서 기록 |
| 분산비 판정 | `arrhenius_compat.py:variance_ratio_verdict()` · CLI `--vr` |

⛔ **부트스트랩은 여기까지 "입력을 만드는 코드가 없는 선언"이었다** — `msd_multi_origin()`
이 원점을 이미 평균해 줘서 재표본할 단위가 없었다. 생산자 `msd_per_origin_from_traj()` 를 붙였다.

🔴 **블록 규칙이 부트스트랩 잡음에 걸린다** (합성 궤적 실측). 같은 σ(b) 곡선에서
**B=150 → b=12 · B=3000 → b=7** — **복제 수가 답을 바꿨다.** 원인 둘 —
① σ 의 MC 오차 ≈ `1/√(2B)` 인데 B=150 이면 **0.058 > 문턱 0.05** (문턱이 뜻을 가지려면 **B ≥ 1800**)
② 상대변화는 **b 간격에 비례** ⇒ 성긴 사다리가 문턱을 쉽게 만든다.
⇒ **규칙은 안 바꿨다** (결과 전에 합의한 것이다). 가드 둘을 붙여 그 자리에서 **기권**하게 했다.
규칙 개정 여부는 **`kb/reviews/li2s1a_BU_addendum_block_rule_guards_2026_09_22.md` 로 1저자에게 물었다 — 회신 대기.**

⚠ 합성 궤적에서는 **B=3000 에서도 σ(b) 가 단조 상승**했다. 실제 궤적에서도 그러면
**규칙대로 판정 보류**가 된다 — 그 가능성을 미리 적어 둔다.

⚠ `results_seen` 은 **false 유지** (담금질 seed2 422/1050 ps).

#### ✅ **계보도 닫혔다 — 배포본은 seed1 궤적의 마지막 프레임이다**

1저자가 **정확값 지문**(격자 12 자리 + 첫 원자 좌표)을 줘서 `grep` 한 번에 갈렸다.
· `A/seed1/traj.xyz` **1,051 프레임 중 일치 1 개 = 프레임 1050(마지막)** · `|Δa| = 4.2×10⁻¹³`
· `Cl #1` 을 셀 안으로 감아 대조 → **0.1036 Å** = 예측한 relax 변위 대역(0.1–0.4)의 아래 끝
⇒ **`seed1/traj.xyz` 프레임 1050 을 고정셀 relax 한 것.** provenance §3 미결 해소.
🔴 **내 가변셀 가설 철회** — `|Δa| = 3.9×10⁻⁵` 는 배포본↔**ev01/ev18** 차이였을 뿐이고,
그 근거의 **우연 확률이 3.8 %** 라 애초에 약했다(1저자 지적, 검산 일치).
⚠ *"300 K 50 ps"* 의 **길이는 아직 미확인** — 헤더에 `t_ps` 가 없다. 프레임 수만 안다.

#### ⭐ 오늘 닫힌 것

1. **회신 BS** (`li2s1a_BS_*`) — 600 K 문구 정정. `CLAUDE.md` L44 · `kb/concepts/md.md`
   L179·L330 · `computational_methods_canonical.md` L242 **네 곳에 결정계 한정**을 박았다.
   원인은 **적용 범위 미표기**였고 설계는 멀쩡했다.
2. **회신 BT** (`li2s1a_BT_*`) — 내 BS §6 을 **철회**했다. 창끝 MSD 를 궤적 전체 공식에
   넣어 N_eff 를 8 배 과소평가 → *"셀이 정밀도 천장 25 % 를 정한다"* 가 틀렸다.
   실제 범위는 **34.3 % – 11.5 %**.
   · **relax 프레임 동정 닫힘** — 격자 12자리 **0/36**, 좌표 10⁻⁶ Å **0/36**
     (최근접 0.0179 Å = 기준의 4 자릿수 위) ⇒ **배포 파일은 36 중에 없다. 별도 relax 다.**
     ⚠ 그 relax 의 **로그를 못 찾았다** — 찾으면 계보가 완전히 닫힌다.
   · **C2 의 정체 확정** — 우리 궤적은 **unwrap**(`msd_diffusive_check.py:526` + 음성시험
     `:1820`). 감김 인공물이 아니라 **자기이미지** 기준이고 **1/L 보정**이다.
3. **코드 3 커밋** — 앞선 회신들은 **서술만**이었고 오늘 코드가 바뀌었다:
   · `6ecc482a5` — `msd.json` 이 **두 MSD 를 다른 이름으로** 적는다
     (`msd_max_A2` ↔ `msd_at_fit_window_end_A2`) + `site_distance_A`·`n_eff_he2018`.
     selftest **15 건**, 파괴 4 종 빨간불.
   · `5794ea3f3` — **내 앞 커밋 메시지의 "0 위반" 이 틀렸다는 정정.** EXEMPT 안 쓰고
     정본 창으로 시험을 고쳤다.
   · `cdbb1efca` — `msd_diffusive_check --rsd`: He 식(귀무모형) + 로그정규 구간 +
     **블록 부트스트랩**. **RSD > 0.30 이면 대칭 ± 차단**. `--rsd_block` **기본값 없음**.
     selftest **157 ok**.

#### ⏭ 다음 (순서)

1. 🟡 **위 판정 문턱 합의** — 막고 있는 것
2. **담금질** seed2 `422/1050 ps`(19.8 ps/h · 09-23 밤 예상) → seed3·4·5.
   **시드당 53 h, 4 개면 ≈8 일.** GPU 를 cascade·lpsocl 과 3 등분 중 — **기계 나눌지 결정**
3. **논문 3~12 번 digest — 아직 안 돌렸다.** inbox 25 파일 수령·크로핑 완료 상태.
   순서 **10(Nernst-Einstein) → 6(Schwietert) → 3(Canepa)**. 10 이 1 순위인 이유:
   유리 MD 의 σ 가 전부 `H_R=1` 위에 서 있고 `wang2026` 이 Haven 을 **전문 0 회**로 안 다룬다
4. `jung2026` 선점 판정 **🟡 인접** — §Related work 에 구별선. 구별선은 *"이원"* 이 아니라
   **"전하중성을 어디서 닫느냐"**(그들은 Li 가감, 우리는 염 내부 중성)

---

### ⏭-NOW-t. 2026-09-21 심야 — **보호율 전조건 라운드(120 칸) · 사전등록 k 는 ≤3.5 V 만 맞았다 · 화면 전면 갱신**

1저자 질문 *"NCM 에서는 고전압 안정성을 못 본 거야?"* → 확인해 보니 **NMC811 은 보호율 캠페인에서 한 번도 안 돌았다**
(게이트 탈락이 아니라 **행이 0 개**였다). → *"모든 조건에서 다 돌려볼까"* → gabia 에서 **4 양극 × 6 전압 × 5 농도 = 120 칸** 실행.

**⭐ 결과 보기 전에 사전등록을 커밋했다** — `db/properties/cei_protection_allcells_prereg_2026_09_21.json` (커밋 `7b6744ec2`).
예측 k {2.5:1, 3.0:1, 3.5:4, 4.0:"3 또는 5", 4.3:5, 4.5:5} · 핵심가설 *"k 는 전압이 정하고 양극은 안 정한다"* · 반증조건 셋 · 게이트 동결.

**판정 — 절반은 틀렸고, 그걸 그대로 적었다**
- ✅ **≤3.5 V 는 맞았다.** 2.5 V k=1 · 3.0 V k=1 · 3.5 V k=4, **네 양극에서 같다**.
- ⛔ **≥4.0 V 는 틀렸다.** hull 이 Nd(PO₃)₃(k=3)와 NdP₅O₁₄(k=5)를 **섞어** 내서 실효 k 가 3~5 로 흩어지고 **양극·농도마다 다르다**.
  등록 문구가 *"4.0 V 는 3 또는 5, 1 이나 4 면 틀린 것"* 이었는데 **4 가 나왔다**.
- ✅ 상 사다리는 맞았다(예측 밖 상 **0 개**) · ✅ 통과 열 **2 → 17**.
- 집계: 120 칸 중 **탈락 19**(통과 101) · (양극,전압) 열 **24 중 17** 전 농도 통과 · **NMC811 6/6**.

**⭐ 이 라운드가 새로 알려준 것 — 식과 실측은 다른 양이다**
식이 세는 것은 Nd 가 가로챈 **P** 의 몫, 실측은 인산염을 면한 **양극 TM** 의 몫이다. 둘이 같아지는 것은
**가로챈 P 가 원래 그 TM 에게 갈 P 였을 때뿐**이다. 저전압 NMC811 은 도핑·대조의 TM-인산염 몫이 **둘 다 0.100**
(= **Mn 분율**)이라 Nd 가 P 를 25 % 가져가도 **보호율이 0** 이다. ⇒ §9 에 금지 항목으로 올렸다(29 → **30**).

**깨지는 자리 셋** — ⓐ 저전압 NMC811 Mn 바닥 · ⓑ **단조롭지 않은 열이 셋**(LiMnO₂ 3.00 V 가 크게
1.5 → 44.9 → 9.8 → 100 → 100 %, NMC811 4.00·4.30 V 가 끝에서 1.3·2.3 %p 작게 — 게이트는 통과하지만
곡선으로 읽으면 안 된다) · ⓒ 고전압·고농도 과대예측(NMC811 4.30·4.50 V, x ≥ 0.15).
⚠ **ⓑ 를 보고 단조성 게이트를 지금 넣지 않았다** — 결과를 보고 문턱을 만들면 사전등록이 죽는다. **다음 라운드 후보**로만 적었다.

**화면·그림·도구 갱신**
- `plot_cei_nd_protection.py` **전면 재작성** — 자료를 120 행 CSV 에서 읽고, (b) 를 *P 목적지 막대* → **예측 vs 실측 산점**으로 바꿨다.
  `_column_k` 는 **포화 안 된 점에서만** k 를 읽고(포화점은 hull 이 상을 섞어 k 가 다르다), 갈리면 평균 내지 않고 **죽는다**.
  통과 열 수는 **자료에서 센다**. selftest 양성 16 · **음성 17**.
- ⛔ **조용히 틀린 경로 하나 잡았다** — `write_pred_csv` 가 k 집합 원소가 2 개면 **말없이 그 열을 건너뛰어**,
  그림은 곡선 3 인데 예측선 CSV 는 **2 열**이었다(주연 LiCoO₂ 4.30 V 가 빠졌다). 오류 없음. 이제 `_column_k` 를 같이 쓰고 못 읽으면 죽는다.
- `index.html` — TL;DR · §2b 요지줄 · Fig. 3 alt/캡션 · 읽는 법 세 문단 · §9(항목 30) 를 새 수로 갱신.
  **"24 칸" 정정 상자는 지우지 않고 2 차 층을 얹었다** — 그때 24 는 이 표의 분모가 아니라서 틀렸고,
  지금은 **열의 개수로서 맞다**(전조건 격자를 실제로 다 쟀으므로).
- 시험 `test_interpretation_cards.py` **62 → 69** — 분모 시험을 새 CSV 에 재결속 + 신규 다섯
  (정의되지 않는 열을 0 으로 그리지 않는지 · P/TM 조건이 결속됐는지 · 단조성 게이트가 사후에 안 들어갔는지 ·
  오차 계층이 **예측식 기준**으로 원장과 같은지 · **이 ⏭ 블록이 화면과 같은 수를 말하는지**).
  마지막 것이 이번 리뷰 P2 #3 의 재발방지다 — 종전에는 ⏭ 를 아무것도 안 지키고 있었다.
  **일곱 가지로 깨서 빨간불 확인.**

**⭐ 외부 코드리뷰 라운드 (2026-09-21 심야, 커밋 `ad79ffda1` 대상)**
독립 재계산·실물 변조로 **10 건**이 왔고 **전부 재현됐다**. P1 둘이 내 설계 결함이었다.
- **P1 ① 오차 기준이 틀렸다** — 화면·시험이 식의 오차라면서 `P_taken_by_Nd` 와 뺐다.
  NMC811 4.00 V 가 5.49 ↔ **14.63 %p**. 원장은 처음부터 식 기준이었다 → **화면이 원장과 어긋나 있었다**.
- **P1 ② `_column_k` 의 포화 검사가 공통 k 로 됐다** — 그 행의 자기 k 로 봐야 한다.
  k=3·x=0.20 이면 그 행 예측은 75 % 인데 100 % 곡선을 그렸다. **내 selftest 가 그 입력을 "통과" 로 축복**하고 있었다.
- P2 여덟: 농도 완전성 미검사(행 지우면 승격) · CLEAN 열 결측을 조용히 생략하고 PNG 저장 후 죽음 ·
  캡션 "every comparable column" 이 실제 11/12 · 패널 (c) 상한 0.20 이 0.244·0.288 을 잘라냄 ·
  점선을 전부 혼합비 이동으로 설명(LiMnO₂ 4.5 V 는 Δx ≤ 0.0024) · 고정 문자열 시험 둘 ·
  ⏭ 블록에 철회된 ≤2.5 %p 잔존 · selftest 가 /tmp 하드코딩(Windows 에서 죽음).
- **전부 고쳤다.** selftest 양성 16 · 음성 11 (→ 2차 리뷰 뒤 **17**). 되살린 가드: 빈 패널 선택 · 중복 패널 dedupe · tempdir 정리.

**⭐ 2차 리뷰 — "고친 것이 고쳐졌나" (2026-09-22, 커밋 `8a00827a6` 대상)**
네 변조(k→99 · k→3 · 1.5→20 % · 미정의 열 교체)는 **전부 빨간불** — 10 건은 닫혔다. 그런데 **고치면서 새로 생긴 것 셋 + 잠복 넷**이 나왔고 전부 고쳤다:
- ① `_full_pass` 의 기대 농도를 **자료 합집합**으로 만든 탓에 낯선 농도 **한 행**이 다른 23 열을 조용히 강등시켰다
  (17 → **1**, (c) 제목 "1 of 24", (b) 점 0, PNG 정상 저장). ⇒ 열마다 농도 집합이 같은지 검사하고 다르면 **죽는다** — 조용한 강등도 조용한 승격만큼 나쁘다.
- ② 시험 쪽 쌍둥이 `_prot_counts` 가 P2-4 수정을 안 받아 탈락 행을 지우면 **시험 18 · 생성기 17** 로 갈렸다. ⇒ 전농도통과 판정은 **생성기 함수 한 곳**에서 받는다.
- ③ ⏭ 시험이 철회 문턱(2.5)을 **정확한 굵기 표기 한 가지로만** 금지해, 굵기 없는 재주장은 **통과**하고 `**세 개뿐**` 같은 동의 표기는 **실패**했다. (이 노트에 그 문장을 인용하자 새 검사기가 바로 잡았다 — 이력은 주장 꼴로 적지 않는다.) ⇒ 별표를 벗기고 "≤X %p 로 맞는" 꼴의 모든 주장을 찍어 현행 문턱과 다르면 위반. 검사기를 깨는 음성 시험 동봉.
- ④ (c) 가 `dmax` 로만 축을 잡아 자료가 전부 비교 가능하면 **게이트 선·라벨이 축 밖**으로 나갔다 ⇒ 상한 = max(자료, 게이트×1.3).
- ⑤ CLEAN ⊆ 전농도통과 를 **선언만** 하고 검사 안 해 CLEAN 열의 한 농도가 탈락하면 4 점으로 그렸다 ⇒ `_preflight` 에서 죽인다.
- ⑥ 포화 행의 `k_observed=None` 을 공통 k 로 봐줬다(P1-2 의 반쪽) ⇒ 죽인다 — Nd 인산염이 없으면 k 규칙의 증거가 아니다.
- ⑦ 포화 전 점에 k 가 없으면 "갈린다 `[]`" 라 했다 ⇒ "없다" 로 갈라 말한다.
- 그 밖에: 오차 계산을 `_prot_deviation` 한 곳으로 모았고(오차 계층·⏭ 두 시험이 같은 문턱), 화면 "11 개" 문구를 `len(dev)` 에서 만든다.
  ⚠ 이 diff 밖: LiMnO₂ 4.3 V 는 |Δx| = 0.050423 으로 선 **위** 0.0004 인데 상류 사유 문자열이 `dx=0.050>0.05`(`interface_reactivity_v2.py:1329` 의 `:.3f`) 라 독자가 모순으로 읽는다 — 상류 정밀도 문제, 안 건드렸다.
  ⚠ MP 추론(8a00827a6): Pna2₁ 4 의 배수 논거는 맞지만 **필요조건**이다(어떤 Pna2₁ 구조든 만족). Li₆PS₅Cl "배열이 하나뿐" 은 과하다 — "부분점유를 표현 불가" 까지가 맞는 문장(13 원자 셀에서 Li 6/12 배치는 여럿).

**⛔ 다음 사람용**
- 결과 기록 `cei_protection_allcells_result_2026_09_21.json` 은 **`status: proposed`** 다 — 1저자 판정 전.
- 통과 열 17 개 중 **5 개는 보호율이 정의되지 않는다**(도핑·대조 양쪽에 TM 인산염 없음). 그림은 0 이 아니라 **빈칸**이다.
  식과 견줄 수 있는 것은 **11 개**(LiMnO₂ 3.50 V 는 Nd 인산염이 안 나와 k 가 없다).
  식이 **≤3.1 %p** 로 맞는 열은 **셋뿐**이다(LiCoO₂ 4.30 V · LiNiO₂ 3.50 V · NMC811 3.50 V).
  ⛔ **오차는 예측식 기준이다** — CSV 의 `P_taken_by_Nd` 로 재면 NMC811 4.00 V 가 5.5 %p 로 보이는데
  식 기준은 **14.6 %p** 다. **"17 열 통과" 를 "17 열에서 식이 맞는다" 로 읽지 마라.**
- gabia 에서 돌렸다 — LOBSTER 와 겹치지 않게 **입력/인자 이름으로** 잡았다(`pw.x`·`python3` 같은 공용 이름 금지).

### ⏭-NOW-s. 2026-09-21 저녁 — **CEI 정본 보고서 쇄신 · Li₂S 회신 반박문 · NdP₅O₁₄ 는 이대로**

기계 상태는 ⏭-NOW-r 그대로다 (이 세션에서 재측정하지 않았다 — kgy seed2 담금질·gabia LOBSTER·V100 제외).

**오늘 저녁 끝난 것**
- **CEI 정본 보고서 쇄신** `db/properties/cei_figs/index.html` (1저자 "다 쇄신한다는 느낌으로 재정렬"):
  부제 **"고전압 양극 계면 열화 억제"** · **§0 도입**(Banik(Mo·Zeier) 동의 + 자가반증 onset 표 2.14 → **1.92 V**) ·
  **층 가르기**(open: s0·s2·s2b·s6·s7·sf / 접힘: s1·s3·s4·s5·s8·s8b·s9 + 질문둘 카드 — 요지 한 줄은 접힘 밖) ·
  **Fig 번호 1..8 유일**(보호율 2→3 · 양극별 3→8 — 종전 1,2,2,4,5,6,7,3) · **Fig. 1 2×2 → 1×3**(옛 (c) "×6.58" 패널
  제거 — Li 장부라 철회된 해석을 그림 제목이 광고하고 있었다; 캡션의 취소선 철회문도 걷고 ⛔ 는 읽는 법 상자로) ·
  **§6 10/10**(NdP₅O₁₄ **5.393** 미재현 −0.943 eV · 등록 예측 6.33–6.46 **실패 기록**, 문턱 안 옮김 · 부피 가설 반증) ·
  §9 25 → **28** · 인용위험 **`HZ-cei-gap-ndp5o14-unreproduced`**(CONDITIONAL, 화면 표 행·예측 카드에 data-claim) ·
  시험 8개 추가(`test_interpretation_cards.py`, 일곱 가지로 깨서 빨간불 확인). 생성기 `plot_cei_nd_o_decomposition.py` 는
  이제 **index.html 을 안 덮어쓴다**(참고 조각만) — docstring 에 박았다.
- **Li₂S 검토 회신 반박문** (보낸 파일 `lpscl_smallcell_glass.{vasp,vesta,xyz}`, `D:\QE\10. Li2S\` · repo 밖):
  조성 Li₄PS₄Cl 은 **설계**(0층 hull — Li₃PS₄:LiCl 1:1, Li₂S 는 별상) · packing 아님(1200 K → 1 K/ps NPT 담금질, a 15.46→13.98) ·
  PS₄ 12/12 는 표본 크기 · **밀도 1.62 와 셀 통계는 인정**(우리 경보 −15 %, 원인 미지목, 5 시드 설계). 1저자에게 경어체 회신문 전달.
- **NdP₅O₁₄** — 1저자 "그냥 이대로 가면 되는거야?" → **예.** 남은 건 MP 6.336 의 엔트리·범함수 **조회**(계산 아님).

**⛔ 다음 사람용**
- §6 **G2 산수**(NdCl₃ 4.337 / NdPS₄ 2.264 vs P₂O₅ 5.186 → 등록 문구대로면 "더 좁은 갭 층 추가")는 **결정 원장 미등록**.
  화면에 "판정 미등록 · 인용 금지" 로 박아 뒀다. 등록·비준은 1저자.
- **생성기 드리프트**: `plot_cei_nd_o_decomposition.py` 가 `cei_dual_compat.csv` 의 Li₃PO₄ `mixing_x` 를 빈칸 → **1.0** 으로
  내보낸다(원장·화면은 "x 미실측 · 끝점은 추론"). repo CSV 는 **복사하지 않았다** — 없는 값을 1.0 으로 그리는 경로다. 고칠 것.
- `pending_forbidden_phrases` "축합될수록 갭이 넓어진다" 는 kb 두 문서(open_items · cei_nd_manuscript_framing)에 교육 문장으로
  살아 있다 — 켜려면 그 요소에 `data-claim` 을 먼저 단다.
- ⚠ 리뷰어 에이전트 지적은 이 블록 커밋 뒤 같은 커밋 계열에 반영한다 (미반영이면 아래 줄이 그 목록이다).

**그 뒤 같은 세션에서 더 한 것 (2026-09-21 밤)**
- **Li₂S 계보 판별** — 검토자가 *"P–S σ 0.013 은 300 K 치고 좁다"* 고 지적. repo 안의 원시 36 vs relax 36 으로 갈랐다:
  원시 **0.0451 Å** · relax **0.0127 Å** · 고전 예상 √(kT/k) 0.047–0.055. ⇒ **보낸 파일은 0 K relax 구조**이고
  *"UMA P–S 가 뻣뻣하다"* 는 **기각**. 기록 `lpscl_smallcell_glass_provenance_2026_09_21.json`.
  ⛔ 내가 앞 회신에서 "궤적 최종 프레임" 이라고 **근거 없이 단정했던 것**이 틀렸다.
- **`aimd_jump_stats.py --export_frame`** 신설 — `--export_stage {raw_md,relaxed,time_averaged}` **필수**.
  xyz·vasp 둘 다 stage·t_ps·원본 sha·셀 밖 원자수를 주석에 박는다. selftest 양성 2 · **음성 3**.
  실측: repo 프레임이 **셀 밖 116/120** — 검토자가 본 숫자와 같다(unwrap 좌표).
- **봉인 카드 정정 주석** — `lpscl_li2s_interphase_prereg` 의 *"hull·실측 일치"* 에서 **'실측' 은 실험이 아니다**
  (UMA hull ↔ MP DFT hull 두 계산). 원문은 안 고치고 `⛔_정정_2026_09_21_실측_이라는_말` 로 덧댔다.
- **CEI 자기리뷰 반영** — P0 하나(§3 답 카드가 철회된 6.6 배를 증거로 인용) + P1 열 개. 25 곳.
  ⚠ 리뷰어 지적 중 **하나는 틀렸다** — "Nd 꼴등" 은 원장(`dopant_multiaxis_result` §4) 문구 그대로라 안 고치고 한정만 달았다.

**✅ 1저자 판단 둘 다 닫혔다 (2026-09-21 저녁 · "ㄱㄱ")**
- **"24 칸" 의 분모 — 출처를 찾았다.** 선행 지표 `cei_tm_fate_2026_09_17.json` 의 (양극,전압) 격자가
  **4 × 6 = 24** 이고, 그 수가 산문으로 옮겨와 **다른 표의 분모**가 돼 있었다. 실제 표는
  `cei_nd_protection_curve.csv` **34 행**(통과 22 · 탈락 12 · 열 7). 화면 5 곳을 CSV 수로 바꾸고
  §2b 에 정정 상자를 실었다. **탈락 12 와 "전 농도 통과 열 둘" 은 불변** — 바뀐 건 분모 하나다.
  원장에는 `⛔_정정_2026_09_21_24_칸_의_분모` 로 덧댔다(원문 보존).
- **제목** — "Nd 는 인산염 싱크다" → **"Nd 는 P 를 선점한다"** (탭 `Nd Intercepts Phosphorus`).
  옛 제목이 §3 철회문(*"NdPO₄ 가 Li₃PO₄ 보다 깊은 싱크"*, +1.5035 eV/P 양수)의 축약으로 읽혔다.
  ⚠ 기계 경로(`decisions.json` 의 `scope: cei.phosphate_sink` 등)는 **안 바꿨다**.
- 시험 3 개 추가. ⚠ 그중 하나는 **첫 판이 헛것을 쟀다** — `\b7\b` 같은 맨 숫자는 페이지 어디에나 있어
  열 수를 지워도 통과했다(break-verify 에서 잡음). 문맥에 묶어 다시 썼고 네 가지로 깨서 확인했다.

**다음 (순서)** — ⏭-NOW-r 의 1~3 그대로: 소셀 seed2 첫 실측 → 카드 견적 갱신 → seed3–5 · v42 회신 대기 · lpsocl C-gates.

### ⏭-NOW-r. 2026-09-21 오후 — **v42 발송 준비 끝 · 소셀 재개조건 ① 이 ② G-B7 에 들어갔다 · V100 NFS 함정**

| 기계 | 지금 |
|---|---|
| **V100** | ⛔⛔ **이 캠페인에서 뺀다 — uma env 가 깨졌다.** DEM 이 같은 env 를 공유하는데 오늘 15:45 pip 이 돌아 cu12 payload(nccl·nvshmem·cusparseLt)를 지우고 cu13 으로 갈아엎다 멈췄다 (mtime 확정 · `kb/platforms/v100_uma_setup_2026_09_14.md` 함정 ⑧). 복구 불가(nvshmem 이 kgy 에도 없고 인터넷 차단 · 대안 env 없음). ✅ G-B7 18 사건은 **삭제 직전 15:29 에 끝나** 살았고 원자료는 repo 로 회수 완료 |
| **kgy** | 🟢 lpsocl s6 + cascade v6 **+ 소셀 유리 담금질 seed2 (17:06 발사 · turbo · `~/work/runs/lpscl_smallcell_2026_09_16/A/seed2`)**. ⚠ GPU util 100 % 3-way 공유라 15 h 견적은 늘어난다 — 첫 시드 실측으로 카드 견적을 갈아끼운다 || **kgy** | 🟢 lpsocl s6/T800 재시작 (14:1x · 세 번 실패 뒤 — 아래) + cascade v6 40런. GPU 공유 |
| **gabia** | 🟢 LOBSTER nscf 3차 (PID 3003581 · 13:57 · 15:38 에 1/4 k-점 진행 중) · ETA 09-23 낮. ⏸ **탄성(modelc_2x) 재개는 그 뒤** — GPU 는 비었지만 호스트 available **15 GB** (LOBSTER 40 GB) 에 pw.x 는 >23.8 GB 요구 → OOM 킬러가 LOBSTER 를 잡는다. 러너에 F 선행조건(nstep 200 · trust_radius_max 0.05 · 23_p 재실행 · 완료판정 `bfgs converged`) + 호스트 RAM 가드 넣음 (`793bc03b7`) — 같은 명령으로 재개하면 된다 |

**오늘 오후 끝난 것**
- **SDCP C-12 v42** — 러너 승계(`SKIP_COMPLETE=1` + `CONTINUE_FROM`) · 19잡 입력 v41 과 바이트 동일 ·
  실물 7잡 픽스처 e2e(승계 7·건너뜀 7·nzmag 2 가 승계된 부모 기하로 실행) · 자체리뷰 17항목
  `runs/sdcp_c12_2026_08_30/SELF_REVIEW_v42.md`. 산출물 커밋 `91bdffb35` (zip `9a3976b8b13a…` · IDENTITY · SEND_MAIL).
  ⚠ 첫 렌더는 v40→v41 배너("지우고·멈추고 알려 주십시오")를 그대로 달고 나갈 뻔했다 — 승계 메일은
  **반대 지시**라 렌더러에 `_banner(continuation)` 분기 (`d5d4414e9`). **발송은 1저자.**
  남은 위험: mirae 가 습관대로 §2(처음부터)로 돌리는 것 · `CONTINUE_FROM` 경로가 로그 추정.
- **소셀 합집합 규칙 정정** (`846a2e02e`): 원시 끝점 쌍을 공유하는 사건은 **둘 다** 버린다 (lag 간 겹침은
  구조적으로 0 — 끝점이 (t, t+lag) 라 lag 이 다르면 sha 가 같을 수 없다). 24 → **18**.
- **Li₂S 셀수렴 P1 입력 경로** — `build_neb_inputs.py --scf_probe` (`d81284cc0`). 4×4×4 = 191 원자 · k 2 2 2 ·
  λ₁ 16.04 Å. ⏳ **실측은 아직** — 카드가 kgy 지정인데 kgy GPU 가 MD 로 차 있고, gabia 는 사유가 낡음. 기계 결정 대기.

**⛔ 오늘 밟은 것 (다음 사람용)**
- **lpsocl s6 재시작 세 번 실패**: ① 붙여넣기 훼손 → 한 줄로 · ② `REPO` 기본값 틀림 → `REPO=$HOME/lldvar` ·
  ③ 맨 `python3` 가 `(base)` 로 풀려 `ModuleNotFoundError: ase` (2 분 뒤 traceback). 러너에 `PY=` + import
  사전검사 (`42338fbea`) — 던지기 **전에** 막는다.
- **V100 에서 UMA 가 안 뜨는 것처럼 보인 것**: conda env 가 **NFS** 위(`$STORE/opt/miniforge3/envs/uma`)라
  import 가 파일 개수당 왕복 지연으로 10 분+ (매핑 25 → 1163 파일 / 7.6 분). 두 번을 2·5 분에 죽였다.
  판별은 `read_bytes` 가 아니라 **`rchar`·`/proc/<pid>/maps` 의 NFS 파일 수** (문서 정정 `b9c637c0e`).
  체크포인트는 kgy 에서 scp (11 MB/s) 로 로컬 사본 · 실행은 `env LD_LIBRARY_PATH=$CONDA_PREFIX/lib HF_HUB_OFFLINE=1 $CONDA_PREFIX/bin/python -u`.
- ⛔ `for x in $(pgrep -f disorder_ensemble_diffusion); do kill $x; done` 으로 **lpsocl s6/T800 을 43 % 에서 죽였다**
  (cascade 를 잡으려던 것). CLAUDE.md 금지 이름에 스크립트 이름 추가. 잡은 `--out_root` 로 가른다.

**다음 (순서)**
1. ⭐ **소셀 유리 MD 카드 `proposed` — 1저자 비준 대기.** `lpscl_smallcell_glass_md_estimand_2026_09_21.json` ·
   결정 `D-2026-09-21-lpscl-smallcell-glass-md`. **400/465/550 K · 120 원자 1×1×1 · 독립담금질 5 시드 · 400 ps · default 모드** ·
   보고량은 **N_pass/15 와 Ea 시드 IQR**(절대값 아님 — 대조가 없다. 대조 = Phase B 별도 카드).
   **파일럿 2런 먼저**: 400 K(노화 · 전·후반 D 2배 이내) · 550 K(감김 · MSD < 48.88 Å²). 둘 다 통과해야 본 15런.
   기계 **V100**(유휴 · 긴 MD 는 NFS 판단이 맞는 워크로드) · 총상한 **180 GPU-h** · 견적 ≈137 h.
   ⚠ V100 은 대여 기계다(09-14 소멸 이력) — 시드마다 결과를 $STORE 로 복사한다.
   ⚠ modelc 9런은 turbo 라 **같은 표에 못 놓는다**(V100 은 Volta 라 turbo 불가) — Phase B 도 전부 새로 돈다.
2. ✅ 소셀 재개조건 ① **소진 확정**(1저자 2026-09-21 · 사후 비준 · 결정 active) + `/li2s` 에 **NEB 가지 절 신설**(마감 0/9 · ① 라운드 0/18 · 재개조건 소진/열림). 종전 화면은 사다리 옆 한 줄로 *"9/9 생존 → 다음은 UMA-NEB"* 라 3 일 낡아 있었다. 남는 재개조건 ②·④ 뿐 — 둘 다 새 선언이 필요하고 지금 열 이유 없음.
2. ✅ v42 메일 **발송됨 (2026-09-21 오후)** → mirae 회신 대기. 기대: `✓ 승계 <잡>` 7줄 · nzmag 2 + vacconv 3 실행 · 1단계 통과 → 2단계 7.
3. lpsocl 15/15 → C1/C2 → C3 → A/B/C (⚠ run-mode 미기록 시드 하나 먼저 해소).
4. Li₂S 4×4×4 P1: 기계 정하면 `--scf_probe` 입력 → 단일 SCF 3 iteration → peak VRAM·벽시계 → 카드 §3 기입.

---

### ⏭-NOW-q. 2026-09-21 낮 — **셋 다 다시 섰다. 그리고 cascade 가 v5 로 23 h 헛돌았다.**

| 기계 | 지금 |
|---|---|
| **gabia** | 🟢 **LOBSTER nscf 3차 발사 13:57** (PID 3003581). 게이트 전수 통과 — 전하밀도 101 MB(09-19 SCF) · k `2 2 1 0 0 0`(비준값) · available **55 GB** · pw.x 0. ETA **≈47 h → 09-23 낮**. ⚠ 20 h 씩 출력 0 바이트가 정상이다(nscf 는 k-점이 끝나야 쓴다) |
| **kgy** | 🟢 **cascade v6 진짜 발사 13:55** — out_root `~/work/runs/cascade_v6_40run_0921` · code_id `8e138ba1` · 남은 **41 런**(속도시험 1 + 40) · 상한 320 GPU-h |
| **V100** | 소셀 재개조건 ① — 궤적 회수·census 대기 (⏭-NOW-p 아래 그대로) |

**⛔⛔ 사고: cascade 가 v5 계획으로 23 h · 21.73 GPU-h 를 태웠다**

- `~/work/runs/cascade_v6/` 는 **이름만 v6 이고 내용은 v5** 다 (30 런 · 5 구조 · 3 온도).
  **지우지 않는다**(증거). 진짜 v6 는 `cascade_v6_40run_0921/` 이다.
- 원인은 **kgy 가 pull 을 안 한 채 발사**했고, 내가 준 **발사 블록에 계획 게이트가 없었다**.
  감시 블록에는 넣어 놓고 정작 던질 때 안 넣었다.
- 두 번째 원인: 내가 준 확인 명령 `grep -c "P2_Al2S3_J" run_eprime_pilot.py` 가 **틀렸다.**
  v6 는 부모 이름을 코드에 안 박고 `cascade_v6_parents_2026_09_19.json` 에서 읽는다
  (`load_roster`) — grep 은 영원히 0 이다.
- 세 번째: `run_eprime_pilot.py` **docstring 이 7 일째 v5 를 설명**하고 있었다(코드는 v6).
  2026-09-21 에 고쳤다(커밋 8e138ba1).

**⇒ 계획 확인은 grep 이 아니라 계획을 만들어 보는 것이다**
```
cd ~/lldvar && python3 -c "
import sys; sys.path.insert(0,'tools/doping')
import run_eprime_pilot as R
from collections import Counter
print('MD', len(R.MD_STRUCTURES), R.TEMPS, R.SEEDS, R.TOTAL_CAP_GPU_H)
print(dict(Counter(s['stage'] for s in R.build_plan('/tmp/x'))))"
```
나와야 하는 줄: `MD 20 (600,) (1, 2) 320.0` · `{'prep': 21, 'md_perf': 1, 'md': 40}`
⭐ watch 화면의 **`완료 스텝 N/M`** 도 지표다 — M = `구조수 + 11`. v5 때 **24/16**(분자>분모)이
어긋남의 흔적이었고, v6 는 **1/32** 로 맞는다.

**⏳ 남은 것**
- 21.73 GPU-h 를 어느 예산에 다는가 — v6 상한 320 과 **별개**로 기록한다(다른 캠페인이다)
- LOBSTER 끝나면 `D-2026-09-18-nd-icohp-kmesh` **enforcement ④** — k-탐침 SCF 1 개
- 1~9 / 10~19 분할(논문 vs revision)이 **repo 에 없다** — 1저자는 db 에 있다고 했는데 grep 0.
  ⚠ 그 분할대로면 vacconv(10–12)가 revision 인데, **vacuum_convergence 는 Figure 2e 의 hard gate** 다
  (`|D(c2) − D(c1)| ≤ 0.005 eV`, 실패시 Figure 2e 제거). 분할과 게이트가 어긋난다 — 밤 미팅 안건

---

### ⏭-NOW-p. 2026-09-20 밤 — **LOBSTER nscf 가 두 번 끊겼다. NdP5O14 갭이 끝나야 다시 던진다.**

> 1저자 2026-09-20: *"그래 이거 끝나고 하자"* — **이거 = `/data/work/runs/cei_gap/NdP5O14*/03_nscf_gap`**.
> 그게 끝나고 호스트 메모리가 풀려야 LOBSTER 를 올릴 수 있다.

| | |
|---|---|
| **막는 것** | **호스트 메모리.** LOBSTER nscf 요구 `Estimated total dynamical RAM > **39.68 GB**` vs 실측 `available` **32 GB** (21:00, NdP5O14 갭이 GPU+호스트를 쓰는 중). ⛔ 7.7 GB 모자란다 |
| **선행** | NdP5O14 `03_nscf_gap` 완주 (`JOB DONE` 확인) |
| **판단 대기** | **Γ-only 로 갈 것인가** — 아래 §3 |

**실측 (전부 `/proc`·출력에서 확인한 것)**

- **경로**: `/data/work/runs/nd_ppswap_2026_09_16/lobster_frozen4f` · `lobster_nscf.in`
- **입력 규모**: nat 120 · ecutwfc 70 / ecutrho 560 · **nbnd 920** · `nosym` · K_POINTS `2 2 1 0 0 0` → **k-점 4**
- **원가**: SCF **10h33m**(완주) · nscf **k-점 1 개에 23.6 h**(`total cpu time 84924.5 secs`)
  ⇒ 4 k-점 = **≈47 h**
- **1 차 종료 (09-20 13:46)**: `Computing kpt #: 2 of 2` 찍고 끊김.
  `JOB DONE` 없음 · QE 오류 없음 · **dmesg OOM 기록 없음**(4월·7월 것뿐) · 내 대기 스크립트도 아님
  (NdP5O14 는 **19:47** 시작 = 6 h 뒤). ⇒ **원인 미상.**
  ⛔ `.save/` 가 전부 09-19(SCF) 자다 — **nscf 산출물이 안 나왔다. LOBSTER 가 먹을 게 없다.**
- **2 차 시도 (09-20 20:57)**: `setsid nohup` 으로 재던짐. 8 랭크 `Rl` 로 붙었으나
  ⛔ **`Threads/MPI process: 20`** (8 랭크 × 20 = **160 스레드 / 물리 20 코어**, 8× 과다구독) ·
  ⛔ **메모리 부족**(위) ⇒ **중단 결정.**

**⛔ 내가 만든 손실 하나** — 2 차 시도를 `2> lobster_nscf.err` 로 던져서 **1 차의 stderr 를 덮어썼다.**
어제 끊긴 단서가 거기 있었을 수 있고 이제 없다. ⇒ 다음부터 **`2>>`(append)** 로 간다.

**3. 재시작 전에 정할 것 — Γ-only 로 갈 것인가 (1저자 판단)**

| | A. 2×2×1 그대로 | B. Γ-only |
|---|---|---|
| k-점 | 4 | **1** |
| 벽시계 | ≈47 h | **≈12 h** |
| 위험 노출 | 47 h 를 두 번 잃었다 | **1/4** |
| 대가 | — | ⚠ **ICOHP 가 k-샘플링에 딸린다 — 방법 변경이다** |

- `nbnd=920` 은 **깎을 수 없다** — `build_lobster_nd.py:100` 이 LCAO 기저 함수 수(≈867)에서
  유도한다(`int(nbf*1.05)+10`). LOBSTER 가 기저 수 이상의 밴드를 요구한다.
- **k-점 병렬화(`-nk`)로는 총 일이 안 준다** — 어떻게 쪼개도 47 h (한 k-점 × 4).
  **유일한 레버가 k-점 수 자체**다.
- ⇒ B 로 가면 **개정 기록이 먼저**다 (보고량 눈금 변경).

**4. 재시작 블록 (갭 끝난 뒤 · 메모리 게이트 포함)**

```
W=/data/work/runs/nd_ppswap_2026_09_16/lobster_frozen4f; cd $W
free -g | awk 'NR==2{if($7<45){print "⛔ available "$7" GB < 45 — 던지지 마라"; exit 1} else print "✓ "$7" GB"}' || exit 1
OMP_NUM_THREADS=1 setsid nohup mpirun --allow-run-as-root --bind-to none \
  -x OMP_NUM_THREADS=1 -np 8 \
  /data/apps/qe-7.4.1-cpu/PW/src/pw.x -nk 2 -inp lobster_nscf.in \
  > lobster_nscf.out 2>> lobster_nscf.err < /dev/null &
sleep 60; grep -aE "Parallel version|Threads/MPI|Estimated (max|total)" $W/lobster_nscf.out | head -4
```
나와야 하는 줄: `running on **8** processor cores` · `Threads/MPI process: **1**`

⛔ **죽일 때는 `pkill -f "lobster_nscf.in"`** — `pw.x` 로는 절대 안 된다 (2026-09-19 에 그걸로
NdP5O14 vc-relax 를 같이 죽였다).

---

### ⏭-NOW-o. 2026-09-19 오후 — **cascade v6 가 실행 직전까지 왔다. 막는 것은 숫자 하나.**

| | |
|---|---|
| **막는 것** | **총상한 GPU-h 하나.** 카드 §6 이 비어 있고 *"빈 채로는 배치를 시작하지 않는다"*. ⛔ V100→3090 환산을 추정으로 때우지 않는다 — 추정이 곧 상한이 된다 |
| **절차** | ① kgy 에서 H0 600 K **1 런**(소상한) → ② 실측 × 40 + 준비 21 → ③ 1저자 총상한 기입 → 카드 `ratified` → ④ 배치 40 런 |
| **선행** | kgy 에 `lpsocl_box331_400ps` **4 런**이 남았다. kgy 는 QE 와 GPU 를 공유하니 **그게 끝난 뒤** 시작한다 |

**오늘 끝난 것**
- **부모 배열 10 개 완성** — A·B 승계 + C~J 신규 8 (seed 3~10). 빌더 명령을 A·B 의
  `compound_summary.json` 에서 복원해 인자를 한 글자도 안 바꿨다.
  전수 검증 **5/5**(조성·자리지도 digest·배열 고유성·distinct-parent·P1↔P2 자리).
  기록 `db/properties/cascade_v6_parents_2026_09_19.json` (sha256 20 개).
- **기계 kgy 확정** — V100 컨테이너가 2026-09-14 에 **한 번 소멸한 이력**(이 파일 1165 줄)이
  근거다. 40 런 · 연속 수일을 대여 기계에 안 얹는다. 카드 **§2b** 신설: 바뀌는 것이
  부모 수 **와** 기계 **둘**임을 명시 · kgy 에서도 **default**(turbo 안 켠다) ·
  **섞지 않는다**(kgy·default 는 제3 조합) · 견적 132 GPU-h 는 **V100 숫자라 무효**.
- **화면에 카드 계보** — 1저자 *"12/13 처럼 혼동하는 일 없게"*. 09-12 에 카드 셋 · 09-13 에
  둘인데 화면이 어느 게 지금 것인지 말하지 않았다. `data.cascade_card_lineage()` +
  `/cascade` 밴드. **★말단은 그래프 사실이지 유효 판정이 아니다**(말단인데 `proposed` —
  v6 가 그 상태)를 **화면 텍스트로** 적었다. 시험 3(음성 2) → 33 통과, **셋 다 깨서 빨간불 확인**.

**⚠ 다음 사람이 알아야 할 것**
- **Al 자리가 부모끼리 겹친다** — (93,145) A·D·H · (88,140) E·I. 고유값 10 중 **7 종**.
  `--method spread` 가 결정론적 후보 집합에서 고르기 때문. **그대로 쓴다**(고르면 편향)
  지만 부모 간 SE 가 그만큼 **낙관적**일 수 있다. 미결로 끝나면 이 줄이 근거다.
- **v5 의 30 런은 재활용 못 한다** (궤적 미저장 → 자격 판정 불가). v6 는 전부 새로 돈다.
- **계산은 아직 0 건이다.** 구조만 만들었다.

**딴 기계 상황** — gabia: LOBSTER nscf(k점 2 중 1 째, 8 랭크) + NdP5O14 체인이 tmux
`ndp5o14` 에서 **LOBSTER 종료를 기다렸다가 자동 시작**하도록 예약돼 있다
(`kill -0 <pid>` 대기 — `pgrep -f "lobster_nscf.in"` 은 **자기 자신을 잡아** 영원히 안 깨어난다.
같은 실수 반복 금지). NdP5O14 vc-relax 는 16:37 수렴 · 스플라이스 완료(셀 8.914/9.156/13.180).


### ⏭-NOW-n. 2026-09-18 밤 — **Nd 논지가 무너졌다가 더 단단하게 다시 섰다**

> 같은 날 뒤 블록이다(앞은 ⏭-NOW-m). 한 줄 요약: **Δ 반응에너지 축을 버리고 산물 축으로 옮겼다.**

**① 🔴 §1 Fig. 1 의 주장이 Li 장부였다 — Li-맞춤 대조군으로 확인**
화면 §1 이 *"O 는 전압에 평평, Nd 는 6.6 배 급등, 고전압은 Nd 가 주역"* 이라 적었다.
grand potential 은 **dΦ/dV = +N_Li** 라 Li 를 덜 든 조성이 전압과 함께 유리해 *보인다*.
Nd³⁺↔3Li⁺ 는 f.u. 당 Li 0.6 을 뺀다. **전하중성을 포기한 Li-맞춤 무-Nd 대조군**을 넣으니
Nd 항이 **−50.8 meV/atom**(4.5 V)로 **부호가 뒤집혔다**. ΔN_Li = 0 인 O 치환만 평평(−5.5 meV/V).
· ⚠ 화면 §9 가 *"전하중성 때문에 이 설계로는 못 뗀다"* 고 이미 적어 놨었다 — **그걸 뗀 것**이다.
· 철회: 리드 · Fig. 1 캡션 (c) · R4 · §2 "P₂S₇ 0 %". **원문은 `<s>` 로 남기고 ⛔ 를 텍스트 노드로 붙였다**
  (CSS content 로 그리면 복사·인쇄·추출에 안 나간다 — 화면 규율).

**② ⭐ 새 주논지 — Nd 가 P 를 가로채 양극 TM 소모를 막는다**
`cei_tm_fate_2026_09_17.json` 이 계산해 놓고 그림으로 안 올린 지표가 답이었다.
**예측식을 곡선보다 먼저 세웠다** — x = 0.02·0.20 두 점만 보고 NdP₅O₁₄ 화학식(P/Nd = 5)에서
`보호율 = min(1, k·x/(1−x))` 를 유도한 뒤 0.05·0.10·0.15 를 돌렸다. 맞춘 매개변수 **0 개**:

    LiCoO2 4.30V  10.3/10.2 · 26.6/26.3 · 55.9/55.6 · 88.4/88.2 · 100/100   (k=5, NdP5O14)
    LiNiO2 3.50V   7.2/ 8.2 · 20.9/21.0 · 45.1/44.4 · 71.4/70.6 · 100/100   (k=4, LiNd(PO3)4)

**k 는 §1 패널 (d) 의 상 사다리다.** 전압이 오를수록 hull 이 더 축합된 Nd 인산염을 골라
Nd 하나의 수용력이 커진다(1→4→5) — **필요해지는 구간에서.** (d)는 장식이 아니라 계수다.
· 게이트를 **코드에** 넣었다: |Δmixing_x| ≤ 0.05(분모가 같은 양인가) · 티오인산염 무효 · 끝점.
  24 칸 중 다섯 점 전부 통과한 열은 **정확히 둘**, 양극마다 하나씩. 탈락 12 행도 CSV 에 남긴다.
· 1저자 조성 x=0.02 → 보호 **10.3 %**, 조성식 Li 5.40 → 5.44. P 치환은 전 구간 Li 를 **늘린다**.

**③ 🔴 자가반증 — 산화창은 넓어지지 않는다 (원장에 이미 있었다)**
`cei_esw_Li_2026_09_16.json`: comp1·modelc·lpsocl 전부 **2.14 V** 인데 **modelc_nd 는 1.92 V**.
**Nd 는 창을 0.22 V 좁힌다.** ⇒ 원고 문구를 **"고전압 양극 계면 열화 억제"** 로 바꿔야 한다
("안정성" 을 창으로 읽으면 우리 데이터가 반증). Banik 2022(**Yifei Mo**·**Zeier**)가
*"치환으로는 산화 안정성 못 바꾼다, 코팅이 필요하다"* 로 닫아 놨다 — **동의하면 도입부가 된다.**
· 확정안: `kb/syntheses/cei_nd_manuscript_framing_2026_09_18.md` (반론 8 개 포함, **1저자 승인 대기**)

**④ ⭐ 걱정했던 게 호재로 뒤집혔다 — 양면 호환성**
§7 dual-compat 10 종에 **무도핑 고전압 산물(CoP₄O₁₁·Ni(PO₃)₂)이 하나도 없었다.**
채워 보니 NdP₅O₁₄ **−0.0790** vs CoP₄O₁₁ **−0.1334** · Ni(PO₃)₂ **−0.1270** —
**Nd 산물이 덜 반응한다**(유의폭의 4.8~5.4 배). 무도핑 TM 인산염은 전해질에 환원돼
TM 을 황화물로 **한 번 더** 뺏긴다(CoP₄O₁₁ → CoPS + CoS₂). ⚠ Mn 계는 예외.

**⑤ 도구 셋 — 전부 "조용히 틀린 경로"**
· `interface_reactivity_v2.py` 끝점 게이트가 **x 가 없으면 `False`** 를 돌려줬다. 실측 **7/144 칸**을
  놓치고 있었고 gabia 판은 게이트가 아예 **없었다**(2026-08-19 판). → 반응식 좌변 종 수로 폴백,
  못 읽으면 `None`(모름). `c26ce5152`
· `run_sei_dft.sh` 머리말 *"계가 3–32 원자라 메모리 문제 없다"* 가 **거짓**이 돼 있었다
  (NdP₅O₁₄ **80 원자**). 그날 gabia MemAvailable 은 **2.2 GB**. → fail-closed 프리플라이트. `320fb6895`
· `bvse_standalone.py` 에 .xyz 입력. **그리고 내가 쓴 시험이 헛것을 쟀다** — 회전 fixture 가
  이미 CIF 관례 행렬이라 `return L` 로 깨도 통과했다. fixture 가 회전됐다는 것 자체를 시험에 넣었다. `1ce28a1f6`

**⑥ 지금 돌고 있는 것 (02:13 실측)**
· `NdP5O14` vc-relax (80 원자, SCF 1회) — **결과 보기 전 예측 갭 6.33~6.46 eV**
  (MP 6.336 + 8 종 재현 편차 +0.053). 나오면 10 종 중 최대이고 "축합될수록 갭이 넓어진다" 가 닫힌다.
· `Nd3PO7` vc-relax (66 원자, SCF 6회) · LOBSTER SCF iteration 1 (01:48 이후 무갱신 — 다음에 또 같으면 볼 것)

**⑦ 다음에 할 것**
1. **NdP₅O₁₄ 갭**이 예측 창(6.33~6.46) 안인지. 벗어나면 8 종이 맞은 재현이 이 상에서만 깨진 것이니 논지에 쓰기 전에 원인을 본다.
2. **원고 문구·그림 순서 1저자 승인** — `kb/syntheses/cei_nd_manuscript_framing_2026_09_18.md`.
   새 순서: Fig.1 P 포획 곡선 · Fig.2 상 사다리+갭 · Fig.3 양면 호환성 · 옛 Fig.1(a)(c)는 SI.
3. **webapp 최종본** — 빈 절(§6 갭 결과) 닫고 새 논지 순서로 재구성.
4. ⚠ **안 한 것**: argyrodite CEI 문헌 정밀 훑기(novelty ①이 여기 달렸는데 1저자가 이번엔 뺐다) ·
   **Nd 계 이온전도도**(BVSE 시작했다가 `bvse_nd_doping_2026_09_18.json` status **paused**;
   Nd/O 를 못 갈랐다 — 선행 CSV 가 O 단독으로도 채널 3.32 → 4.74 % 를 보인다).
   둘 다 심사에서 물어올 축이다.

### ⏭-NOW-m. 2026-09-18 — **소셀 NEB 가 열렸다 · 조용한 기본값 세 개를 뽑았다 · G1 기록을 화면에 실었다**

> 오늘 하루치다. **던지기 직전 grep 하나가 캠페인 하나를 살렸다** — 그 얘기부터.

**① 🔴 LOBSTER 를 k = 2 2 1 로 던질 뻔했다 (카드는 6 6 1)**
`build_lobster_paw_inputs.py` 의 `--kpoints` **기본값이 `"2 2 1 0 0 0"`** 이었고 아무도 안 줬다.
빌더 요약이 셀 출처·부피·nbnd·basis 는 다 찍으면서 **k 만 안 찍어서** 화면상 정상이었다.
K_POINTS 를 따로 grep 해서 잡았다. 그대로 돌았으면 PP 와 k 가 같이 바뀌어 **8.5배의 원인을 못 가른다.**
· 고침: 기본값 제거·required·요약에 출력 (`4cc3a5e07`). **형제 도구 둘에도 같은 줄이 있었다**
  (`build_elastic_strain_inputs.py`·`build_v0_relax_input.py`) → 전수로 제거하고 호출부 4곳에
  같은 값을 **명시**했다(거동 불변, `a3d5dcc7a`). 2026-06-04 timelog 가 이미 "나중에 고칠 것" 으로
  적어둔 그 버그다.
· ⚠ **남은 질문**: b2o3 elastic 결과(`kb/results/b2o3_elastic_analysis_2026_07_03.md`)는 k=2 2 1 로
  돌았는데 그 셀에 적정했는지 **확인 안 했다**. 이제 스크립트에 값이 보인다.

**② k-메시 결정 — 6월 LOBSTER 런이 gabia 에 없다**
카드 §4 의 근거 *"6월 ICOHP 는 k661"* 을 실물로 확인하려 했으나 **6월 Nd LOBSTER 런 자체가 없다**
(ICOHPLIST·lobsterin·lobsterout 을 /data/work·/root 전수 검색; 실재 LOBSTER 런 넷은 전부 2 2 x).
repo 사본에는 lobsterout 이 없어 k 를 읽을 수도 없다. **'못 찾음' 이지 '없음' 이 아니다 — KISTI 는 안 봤다.**
⇒ `D-2026-09-18-nd-icohp-kmesh` **active**(1저자 비준): **k = 2 2 1**, 9월 n5fu 와 맞춘다.
6월↔우리 k 일치는 **미상으로 선언**하고 ICOHP 판정문에 한계로 적는다.
· 감사: `db/properties/nd_icohp_k_mesh_audit_2026_09_18.json` · 카드 §4 에 정정 추가(원문 보존)

**③ Nd PP-swap vc-relax 판정 — V0 통과, 그런데 기준선이 DFT 가 아니다**
ΔV/V = **−0.1524 %** (문턱 2 %) → EOS 재개 불필요로 **제안**. 셀 **모양**도 지켜졌다
(길이 0.27 % · 각 0.10° 안, 감소는 거의 전부 c 축 수축).
⛔ **6월 V0 는 UMA-s-1p1 BM3 champion 이지 DFT V0 가 아니다** (`eos.json` v7_DFT 는 여전히 `pending`).
이 한정 없이 −0.15 % 를 인용하면 안 된다. · `nd_ppswap_vcrelax_result_2026_09_18.json`
· **argyrodite 판정**(1저자 질문): 네 조건 다 충족 → `argyrodite-type framework`.
  ⛔ `F-43m` 아님(P1) · PS₄ 8/10 만 pristine(2개는 oxythiophosphate) · S/Cl 4a·4d 혼합은 **표지**다.

**④ 소셀 NEB — §0 의 셋이 채워져 계산 금지가 풀렸다**
`D-2026-09-18-lpscl-smallcell-neb-estimand` **active**. §0b(경로 선택·집계) 비준 —
모집단은 **문턱이 고른다**(사람이 N 을 안 고른다) · 최대변위 내림차순 ·
끝점 게이트 **A ≥ 1.0 Å · B(비-Li RMSD) ≤ 0.5 Å** · 전부 기각이면 분포 안 내고 정지 ·
집계는 중앙값+Q1/Q3, **최저값 금지**, N<3 이면 나열, **Ea 번역 금지**.
· 후보 **9 건** 확정(`neb_candidates_2026_09_18.json`) — 도구 기록에 `truncated=false`,
  `taken == n_total == 9`. 이미지보정 0/9.
· 끝점 게이트 **9/9 생존**(UMA 탐침, `endpoint_gate_2026_09_18.json`) —
  🔴 **내 예상("대부분 기각")이 틀렸다.** 50 ps 순변위 0 은 *"영구 이사"*, 게이트 A 는
  *"그 순간 다른 골짜기"* — 다른 질문이다. Li 가 넘어갔다가 **돌아온** 것이다.
  ⇒ 장벽을 잴 대상이 9 건 있고, 그것은 **가역 나들이의 장벽**이지 순수송 장벽이 아니다.
· ⚠ 골격 RMSD 가 **0 이 아니다**(0.158–0.274) ⇒ NEB 장벽에 **Li 이동 + 골격 이완이 섞인다**.
  ev01 의 단일 원자 최대는 **0.6163 Å** 로 RMSD 문턱이 안 잡는 종류다.

**⏭ 바로 다음 (순서대로)**
1. 🔴 **ⓑ 카드(장벽)의 허용 서술을 UMA-NEB *전에* 봉인한다.** 부모 카드는 "ⓐ 통과 뒤" 라고
   적었지만 **ⓐ 는 UMA-NEB 산물(안장 부근 이미지)을 필요로 한다** — 그 순서대로면 장벽을
   본 뒤에 서술을 쓰게 된다. 카드보다 엄격하게 간다. (§0b-③ 집계는 이미 봉인됨)
2. UMA-NEB 9 건 → 안장 부근 이미지 → QE 단일점 → ⓐ 게이트(G-N1 수렴 · G-N2 F_RMSE ≤ 0.15)
3. kgy 의 `endpoint_gate_uma.json` 을 repo 로 회수 — §2 표의 `non_li_max_A` 열이 **미완**이다
   (ev01 만 있다. '없음' 이 아니라 '아직 안 옮김')
4. LOBSTER 끝나면 **ICOHP C1/C2/C3 판정** (`Nd79` Nd–S: |ICOHP|>2.0 → PP 가 원인, 6월 영구
   비인용 / <1.0 → 9월 −4.080 의심 / 사이면 미판정). + 사전등록된 **k-탐침**
   (k 만 바꾼 SCF 1개, |ΔE|/atom ≤ 1 meV)

**진행 중 (실측)**
· gabia: LOBSTER SCF — 22:13 시작, `Estimated max dynamical RAM > **27.18 GB**`(하한),
  FFT `(100,100,1000)` · 3.62 M G-vector. CPU=경과·GPU 100 % 로 **정상 작동 확인**.
  ⚠ NSCF 는 더 크다. NdPS₄(9.7 GB)가 같은 카드에 있다 — 끝나면 여유가 생긴다.
· kgy: lpsocl 시드연장 6 런 (~95 h)

**오늘 고친 도구 (전부 selftest + 깨보기 확인)**
· `watch_gap_nscf.sh` — ICOHP 집계가 **6월 값을 반으로** 읽고 있었다 (헤더 2줄 · 스핀 열 2개를
  `$(NF)` 가 spin2 만 집음). 우리 frozen-4f 는 **비분극**이라 온값 → 2배 어긋난 비교가 될 뻔했다.
  자리별 Nd–S + C1/C2/C3 판정(문턱은 **카드에서 읽는다**)을 붙였다.
· `aimd_jump_stats.py` — `--hop_events_all`(문턱이 N 을 고른다) · 케이지 0개 궤적에서
  **처리 안 된 채 죽던** `argmin of empty` 수정(이제 건너뛴다고 **말한다**, 0 으로 안 그린다)
· `melt_quench_uma.py` — `--endpoint_gate`. ⚠ 본문의 `_today()` 가 **9 건을 다 이완한 뒤**
  터졌다 — selftest 가 헬퍼만 부르고 **본문을 안 탔다**(이 파일 세 번째). stub 계산기로 전 경로 시험 추가.
· `scfin_to_struct.py` — **`--bulk`**. 벌크 유리에 슬랩+분자 논리가 돌아 120 원자를
  '분자 72/슬랩 48' 로 **지어내 가르고 셀 밖으로 폈다**(.vesta 분율 1.65·−0.16). 오류 없이.
  VBONDS 에 **P–S 가 없어 결합이 하나도 안 그려졌고** VSTYLE 에 P·Cl 이 없어 둘 다 회색이었다.
  ⚠ 붙이면서 **플래그만 만들고 배선을 안 해** `--bulk` 가 아무 일도 안 한 적이 있다 — 내 실수.

**화면**
· `/li2s` G1 단계에 **사실 행이 하나도 없었다** — 제목과 "미실시로 종결" 만 떠서
  "G1 은 실패했다(=UMA 가 틀렸다)" 로 읽히게 돼 있었다. 실제로는 **한 점도 안 돌았다**.
  사다리 5칸·죽은 자리·**종결 ≠ 미결**을 실었다. G1 사전등록도 §6f 로 이틀치를 메웠다
  (⑤ gabia 48 GB OOM 이 마감 카드에만 있었다).
· `/li2s` 에 **L-1~L-4 사다리** 신설 — 그 사다리가 **repo 어디에도 없었다**(채팅에만).
  실제 상태: L-1 done · L-2 **deferred_by_declaration**(← '지금 여기' 아니다) ·
  L-3 **split**(400 원자 영구불가 / 120 원자 통과, ⛔ 둘은 다른 질문) · L-4 blocked(별도 카드 필요).
  NEB 는 **사다리 밖 가지**다. `li2s_track_ladder_2026_09_18.json`

**⚠ 내가 오늘 틀린 것 (다음 사람이 반복하지 않게)**
1. "끝점 대부분 기각될 것" — 9/9 생존. 두 지표를 같은 질문으로 읽었다.
2. `--kpoints` 를 안 줬다 — 도구 기본값이 카드를 이길 뻔했다.
3. `--bulk` 플래그를 만들고 **배선을 안 했다** (CLAUDE.md 가 경고하는 바로 그것).
4. `_today()` — 없는 이름을 썼고 selftest 가 본문을 안 타서 안 잡혔다.
5. `validate_canonical.py` 를 **빨간불로 두고 푸시했다** (검사와 커밋을 `&&` 로 안 묶었다).
6. 새 시험 여럿이 처음에 **내 기대값이 틀려서** 빨간불이었다 (Nd2 평균 −0.341→−0.339 ·
   awk 필드 $4→$5 · lag 5 ps 에 10 ps 램프).

### ⏭-NOW-l. 2026-09-17 — **§2 가설이 다 정정됐고 G1 이 실측으로 닫혔다. Nd PP-swap 진행 중.**

> 하루에 많이 바뀌었다. 순서대로 읽으면 된다.

**A. §2 가설 카드 — 네 항목 전부 한정됐다** (전에는 3 번에만 ⛔ 였다)
- 1·2 번(저전압엔 P 가 PS₄ 에 갇혀 있다) — **산물에 안 보인다.** 2.5 V 에서 이미 Li₃PO₄ 다.
- 4 번(풀려나는 P 의 양이 는다) — **기각.** `P/atom` 이 전압에 평평하다(0.042~0.054).
- 3 번 범위 — P₂S₇ 는 LiMnO₂ 에서만 4.3 V↑. 나머지는 **전이금속 인산염**(전부 Li/P=0).
- 대신 확정: **P 수용상의 Li/P 가 3 → 2 → 1 → 0 으로 내려간다** (전해질 6 종 전부).
- 레코드 `cei_p_host_ladder_*` · `cei_tm_fate_*` · `cei_p_flux_*` · 결정 4 건 **전부 proposed**.

**B. Fig. 2 를 교체했다** — 옛 막대 집계(양극 개수)를 지우고 **교환에너지 그림**으로.
- (a) 전압 vs 교환 ΔE — 2.5 V 0/24 음수 → 3.5 V **100 %** 음수
- (b) ΔE vs Li/P — §3 사다리를 전이금속까지 넓힌 것
- 생성기 `tools/figures/plot_cei_p_host_ladder.py` (새 파일 · 이유는 docstring)

**C. ⛔ 2 상 교환으로 hull 산물을 예측하지 않는다** — 오늘 **세 번** 어긋나서 원장에 박았다
(`D-2026-09-17-pairwise-exchange-resolution-limit`, policy). 금지 서술 셋이 그 카드에 있다.

**D. ⛔ G1 (Li₂S 1층) — gabia 48 GB 도 OOM. 사다리 5 칸 전수 실측.**
- 죽은 자리 `newd_gpu.f90 : newq_gpu : 135` — USPP 증강전하를 320³ 격자에 까는 배열.
  **격자 × 원자 수**로 정해져 nbnd·대각화기와 무관하다 ⇒ 지금까지의 모든 축이 못 건드린다.
- 실측 GPU 33.9/48.5 GB · host rss 29.6/62 GB (**host 는 여유였다** — 내 예상이 틀렸다).
- 재개 조건 ①(gabia 재시도)은 **소진**. ②(보고량 재설계)·③(모델 교체)은 살아 있다.
- ⭐ **1저자 지시: Li₂S 는 소셀로 간다** (`lpscl_smallcell_2026_09_16`, kgy, n_fu 12 · L 14.14 Å).
  담금질 ETA 8.3 h. 끝나면 **새 보고량 카드부터** (재개 조건 ② 경로 — 1 층 결과의 검증이
  아니라 소셀 자신의 질문이다).

**E. 지금 도는 것**
| 무엇 | 어디 | 상태 |
|---|---|---|
| Nd PP-swap (120원자 vc-relax→scf→dos) | gabia GPU 28 GB | 진행 (step 0). 끝나면 §C NdPO₄ 갭 |
| Li₂S 소셀 담금질 | kgy | ETA 8.3 h |
| 탄성 relaxed-ion Cij | gabia | **정지 중** — PP-swap 이 GPU 를 물고 있다 |

**F. ⛔ 탄성 재개 전에 반드시 — `nstep`**
- `strain_23_p` 는 **nstep 50 소진**이라 미수렴이다. **그 응력을 Cij 에 쓰면 안 된다. 재실행.**
- 남은 4 점 + 23_p 에 `nstep = 200` · `trust_radius_max = 0.05` 를 넣고 던진다.
- 끝난 6 점은 `bfgs converged` 로 진짜 통과 — 건드리지 않는다.
- `watch_elastic.sh` 의 거짓 초록은 고쳤다 (`bfgs converged` 로만 판정 · `⛔ 스텝소진` 상태 신설).

**G. 아직 안 닫힌 것** (원장에 열린 채로 둔다)
- Fig. 1 Δ 의 4.0 → 4.5 V **성장** — 교환 ΔE 는 포화(−1.751)하는데 Δ 는 1.9 배 커진다.
  `Nd 포획률`(20 → 57 %)이 유력하나 정량이 안 맞는다(비 0.44~1.08).
- 2.5 V 의 +0.0147 — 교환으로 전혀 설명 안 된다.
- ⛔ 이 둘은 **2 상 교환으로 못 닫는다**(C). 닫으려면 hull 쪽(`interface_reactivity_v2`)이다.
- LiMnO₂ 에서 Nd 가 NdCl₃ 로 가는 것 — 방향은 Mn/Ni 부호가 설명하나 **0.30 eV/P 띠 안**이라 판정 불가.

**H. 비준 대기 (전부 proposed · 1저자가 ratify)**
`D-2026-09-17-cei-p-host-li-ladder` · `-cei-tm-phosphate-exchange` ·
`-nd-channel-preference` · `-pairwise-exchange-resolution-limit`

### ⏭-NOW-k. 2026-09-16 — **논문 방향이 양극 CEI 로 옮겨갔다. Li₃Nd 트랙은 미결인 채 내려놓는다.**

> 📋 **세션 인수인계**: `kb/projects/handoff_2026_09_16_cathode_cei.md`
> (§A–§E 전체 · 철회 3 건 · 이번에 밟은 함정 7 개 · 다음 우선순위 · 예약된 것).
> 새 세션은 **그것부터** 읽는다.

> 1저자 지시 (2026-09-16): *"li3Nd 관련해서는 닫자 … li3Nd 는 **미결** 이라고 적어놔 —
> webapp 이고, **필요성 하** 이런 표시도 넣어놔줘. 논문 방향성이 달라졌으니까."*

- ⬇ **필요성 하 — Li₃Nd 음극계면 트랙 전체** (⏭-4 · ⏭-4b · cc333 재개 · 선행검사 체인).
  **⛔ 닫힌 것이 아니다 — 미결이다.** 해소돼서 내려가는 게 아니라 **논문이 다른 것을
  묻게 돼서** 우선순위가 내려간다. 판정은 여전히 안 났고, 아래 미결은 그대로 살아 있다:
  - ⏭-4 P0-2 control (pristine 3×3×3 rattle): r1·r2 진행, **r3 미착수**.
    *"같은 Nd 재배열이 공공 없이도 나오나"* 는 **아직 답이 없다.**
  - ⏭-4b 선행검사 체인: **재기동 안 됨**.
  - cc333(3×3×3 NEB): 08-27 중단 — **폐기 아님**, restart 가능한 채로 멈춰 있다.
  - ⚠ `db/properties/sei_electronic_class.json` 의 li3nd `neb_gate` 는 여전히
    **"열림"** 이다. 그건 *방법상* 열렸다는 뜻이지 *하라는 뜻이 아니다* —
    거기에도 이 항목을 가리키는 표시를 달았다.
- 🟡 **필요성 중 — Li₂S 4×4×4 셀수렴**. 1저자 2026-09-16: *"li2S 는 4×4×4 는
  해볼 가치는 있을 듯."* 카드 `db/properties/li2s_cellconv_card_2026_09_01.json` 이
  이미 있고 판정(C1 30 meV)도 박혀 있다.
  ⚠ **아직 착수 조건이 다 안 찼다** — 카드의 게이트는 *"1저자 승인 **+ 메모리 실측 통과**"*
  두 개다. 승인 쪽은 이 발언으로 찼고 **메모리 실측(P1)은 아직 안 했다.**
  그걸 하기 전에 던지지 않는다. 기계는 카드대로 kgy.
  ⛔ **2026-09-23 P1 불통과** (카드 §3b): QE 추정 **45.15 GB** · kgy 에서 15 s 만에 VRAM ≥ 21.1 GB(하한) → 가드 중단.
  kgy 3090 에는 공유 여부와 무관하게 안 들어가고, gabia 48 GB 도 45/48 이라 그대로는 비권장.
  ✅ **1저자 결정 (2026-09-23): "영률 끝내고 li2S 끝내자 나중에"** — gabia 순서 b2o3 → 탄성 modelc_2x → **Li₂S** (단독 GPU · ppcg/paro 재프로브 먼저 · 통과해야 NEB).
- ⬇ **필요성 하 — CEI 모델을 캐스케이드로 옮기기**. 1저자 2026-09-16:
  *"지금 발전시키고 있는 이 모델을 나중에 cascade 에도 잘 적용하면 좋겠다."*
  계획 카드: `kb/methodology/cei_model_transfer_to_cascade_2026_09_16.md`.
  🔴 그 카드가 찾아 둔 구멍 하나 — `interface_reactivity_v2.py:225` 가 **캐스케이드
  배치 경로에서만 `want_kinks` 없이** 호출한다. `cascade_interface_90.jsonl` 286 행이
  전부 **최소 kink 산물만** 들고 있다(실측). 고치는 건 한 줄인데 **JSONL 스키마가
  커지므로 결정 사안**이다.
  ⏳ **지금은 안 한다** — 양극 CEI §C 가 한 바퀴 돌고 나서. 반 바퀴에서 옮기면
  아직 안 굳은 것을 옮긴다.

- 🔴 **필요성 상 — 문헌 대조를 계산 **전에** 했어야 했다** (2026-09-16 발견).
  하루 종일 hull 기반 계면 스크리닝을 하고 나서야 litdb 를 봤고, **Xiao 2019 (Joule,
  Ceder)** 이 *"Li 원자분율↑ ⇔ 산화한계↓"* 와 *"ortho < pyro < meta"* 를 **이미 발표**한 것을
  찾았다. 우리 §3 Li/P 사다리는 **같은 세 계열·같은 순서**다. ⇒ 그 관계는 **우리 발견이 아니고**
  독립 확인이다. 기록 `db/properties/lit_xiao2019_li_budget_precedence_2026_09_16.json`.
  · **banik2022**(Yifei Mo = grand-potential 원저자 + Zeier): *"치환으로는 황화물 SE 산화
    안정성을 못 바꾼다 — 양극 코팅이 필요하다."* 우리 §5 *"도펀트 일곱이 에너지 축에서
    구분 안 된다"* 와 **같은 방향**이다.
  · ⚠ **274 편 중 3 편만 봤다.** aykol2016 · anderson2024(LLZO 도펀트 스크리닝) ·
    adeli2019 · cha2024 · 104(dopant engineering) 이 남았다 — **이 대조는 시작이지 완결이 아니다.**
  · ⛔ **원고에서 *"Li 예산이 축이다"* 를 신규 주장으로 쓰지 않는다.** 쓸 수 있는 신규는
    *"3가 도펀트가 그 저-Li 경로를 계면에서 제자리에 연다"* 이고 Xiao 인용 **위에** 세운다.

- 🔴 **필요성 상 — 양극 CEI**. 여기가 지금 논문의 축이다. §A·§B·§D 끝났고
  §E(dual compatibility)가 2026-09-16 에 붙었다 —
  cha2024 를 읽고 찾은 **§B 가 절반만 본 것**(전해질 vs 양극만 봤고, 사이에 생기는
  CEI 상이 **전해질 쪽과도** 괜찮은지는 미검사였다). 닫힌계 0 V 20 쌍.
  결과 `db/properties/dual_compat_result_2026_09_16.json` + 판정
  `dual_compat_amendment_2026_09_16.json`.
  - ⭐ **쓸 수 있는 것**: V_ox ↔ 전해질 적합성이 **정면 충돌**한다 —
    Li₃PO₄ 4.193 V/0.0000 · Li₄P₂O₇ 4.319/−0.0167 · LiPO₃ 4.980/−0.0388 ·
    LiNd(PO₃)₄ 5.013/−0.0434 로 **완전 단조**(ρ = −1, 사전등록 단측 정확순열
    p = 1/24 = 0.042). 전압에 강해질수록 전해질과 더 반응한다.
  - 🔴 **황산염이 계급으로 나쁘다**: Li₂SO₄ −0.0940 · Nd₂(SO₄)₃ −0.1470 으로
    **모든 인산염보다 음수**. 그런데 Li₂SO₄ 는 §B 인구조사 **1 위(65 회)** 다 —
    제일 많이 만든다고 예측하는 상이 전해질 쪽에선 거의 최악이다.
  - ⛔ **철회**: *"O/P 응축도 **하나로** 정렬된다"* 는 사전등록 P1 반증으로 철회됐다
    (Li₄P₂O₇ −0.0167 > NdPO₄ −0.0192). 대체는 **응축도 × 양이온 2 인자**인데
    **post-hoc 가설**이다 — 검정된 것처럼 쓰지 않는다.
  - ⛔ 같은 명령의 **열린계 실행은 무효**다
    (`dual_compat_open_..._INVALID_endpoint_degenerate.json`). 최소 kink 가 x=0 에
    걸려 전해질 자체분해를 여섯 번 다시 쟀고, 그 인구조사가 PCl₅·P₂S₇·SCl 을
    48 회씩 **거짓 꼬리표**로 §C 후보에 올렸다. **그 목록을 §C 대상으로 쓰지 않는다.**
    도구는 고쳤다(`is_endpoint`/`endpoint_meaning`, 인구조사가 퇴화 칸을 뺀다,
    음성 selftest 8 + 깨서 빨간불 3). ⚠ **닫힌계의 끝점은 정상 판정**이다 —
    한 깃발로 읽으면 멀쩡한 판정을 버린다.
  - ⭐ **NdPS₄ 가 양쪽에서 나온다** (양극 쪽 §B · 전해질 쪽 §E) → §C 우선순위 상향 근거.
    mp-id 확보돼 있다 (`gap_targets_mpid_2026_09_16.json`, mp-aaaaafmc).

  §C(분해산물 갭) 대상 규칙이 2026-09-16 에 비준됐다 —
  **판별종 10 종(신규 9)**, `cathode_cei_gap_target_amendment_2026_09_16` ·
  결정 `D-2026-09-16-cathode-cei-gap-target`. 다음 한 수는 **NdPO₄ 파일럿**이고,
  gabia GPU 줄(탄성 → G1 파일럿 → Nd PP-swap vc-relax) 뒤다.
  - 📄 **화면 보고서**: [CEI 계면 반응성 — Nd/O 분해와 Li 예산](https://claude.ai/artifact/JpXxNZwwXt3QgB7f3jMpwo)
    (같은 URL 이 갱신된다 · v3 = §1 분해 · §2 산물 · §3 검증(가설 절반 철회) ·
    §4 x-스캔 · §5 갭 대상 규칙 · 배경 지식 없이 읽는 설명 포함).
    ⚠ `citable: false` — 1저자·리뷰 판정 전이다. 원자료는
    `db/properties/cei_interface_V_2026_09_16.json` · `cei_formation_2026_09_16.json`.
- ⛔ **이 항목은 Li₃Nd 의 과학적 판정을 바꾸지 않는다.** class=metal(measured) 도,
  hull +0.197 eV/atom 도, `cite_with` 조건절도 그대로다. 바뀐 것은 **우리가 무엇을
  다음에 할 것인가** 뿐이다.

### ⏭-NOW-j. 2026-09-15 밤 — **modelc 를 HOLD 로 확정하고, 곧바로 재개 조건 2 를 발동했다.**

> 이 세션도 **원격 기계를 안 건드렸다** (계산 0). 아래 kgy 블록은 **사용자 실행 대기**다.

| 한 일 | 결과 |
|---|---|
| modelc 3×3×1 게이트 사슬 | C1·C2·C2b·C4·C5·C6 통과 · **C3 만 inconclusive** → `modelc_box331_closed_2026_09_15.json` (HOLD) |
| s3/600 `--scan` c 판별 (계산 0) | **판별 불가** — c 1.30→12.51(10배)인데 β 가 흔들리고 잔차 \|Δβ\|max 0.023 은 케이지 쪽. 되살릴 근거 없음 → **제외 유지 · HOLD 확정** |
| 레지스트리 | `modelc_box331_cell_conditioned / MD_Ea_eV = 0.1683` · **provisional · citable false** · `comparison_group` 을 lpsocl 과 **분리** |
| 700 K 검토 (1저자 질문) | 지렛대 기하 계산 — 600→700 교체는 CI **×1.564**, 700 추가는 **×0.976**. ⇒ 온도로는 안 풀린다. 해설 카드 `modelc_arrhenius_temperature_set_2026_09_15.json` (`/composition/modelc` 에 뜬다) |
| **재개 조건 2 발동** | 사전등록 `modelc_box331_seed_extension_prereg_2026_09_15.json` + 결정 `D-2026-09-15-modelc-box331-seed-extension` (**proposed** — 1저자 비준 필요) |
| /governance 렌더 | 재개조건 **파이썬 repr 누출** 6건 수정(목록을 문자열로 다뤘다) · 툴팁 `**` **100개** → 0 (`canonical.plain_text` + `|plain` 필터) · **오래된 비준 9건 토글** |
| litdb | kim2026·hyun_han(수분열화 2편) INDEX·비교표 병합 + 그림 33·22장 · meng2026 그림 6장 · he2026 DEM 비교표 블록 |

> ### ▶ **지금 대기 중인 실행 — kgy: modelc 시드 5·6 (57 h)**
>
> 사전등록이 먼저다(위 카드). 판정 규칙 A/B/C 는 **결과 보기 전에** 박아 뒀다.
> · A: CI95 ⊂ ±0.050 → C3 통과 → HOLD 해제 심사
> · B: 여전히 경계 → **HOLD 유지·종결, 추가 시드 없음**
> · C: 점추정이 ±0.050 밖 → C3 실패 → 3점 단일 Ea 보고 철회
> ⛔ 예산 6런. **7번째 시드는 없다.**
>
> ⚠ **lpsocl 은 여기 없다.** lpsocl 마감(비준됨)의 재개 조건 R1–R4 에 시드 추가가 없고
> *"'한 시드만 더' 는 재개 사유가 아니다"* 가 명시돼 있다 — 대칭을 맞추려면 **개정문 + 재비준**이 필요하다.
> (lpsocl 도 600 K 자격 시드가 **2개**다 — modelc 와 같은 2/3/3 구조.)

> ### 🔴 1저자 비준 대기 (누적)
> ① modelc HOLD 마감 카드 ② Li₂S 1층 마감 카드 ③ **`D-2026-09-15-modelc-box331-seed-extension`**
> ④ lpsocl 시드 확장 여부(개정문을 쓸 것인가) ⑤ SDCP 코드 라벨(QE vs VASP) ⑥ Table S1 ref 48/49 → [51,52]
> ⑦ 원고 "The deprotonated." 두 단어 조각 삭제

### ⏭-NOW-i. 2026-09-15 낮 — **브랜치 병합 트랙을 닫았다. 실행 중인 것은 NOW-h 그대로.**

> 이 세션은 **원격 기계를 안 건드렸다** (계산 0 · V100·kgy·gabia 명령 0). 저장소 안의 일만 했다.
> 원격 상태는 NOW-h 표가 최신이고, 그 뒤 실측은 사용자가 붙여 준 watch 출력이 있어야 갱신된다.

| 닫은 것 | 결과 |
|---|---|
| 인계 §4.1 `windows-reinstall-backup-oducnh` | ✅ 병합 `47e080690`. ⚠ **"SDCP 파일 5개 없음" 은 이름 기준** — 08-23 판이고 우리 쪽에 09-08 Table S1·08-30 Methods v9 가 있었다. **9/16 마감 위협 아님.** 회수본 머리에 대체 표식 |
| 인계 §4.3 `rescue/…nd-pair01` | ✅ 키 단위 대조 `fcfa1fc02` — 저쪽만 있던 34키(`dft_validation_2026_06_16`, pair01 v0·U=8.0) 회수, `⚠_계보`·citable 아님. 세미나 md 는 Axis-3 블록만 부록 R |
| webapp 시험 | ✅ 09-13 부터 떨어져 있던 `/cascade` §4b `|bold` 6슬롯 회복(`5745dcca9`) — 인계 §7 사다리에 webapp 시험이 없어서 아무도 못 봤다 → 사다리에 추가. 현재 **459 passed / 2 skipped** |

> ### ⏰ 예약 — **gabia 탄성이 끝나면, b2o3 로 가기 전에 Li₂S G1 을 한 번 본다** (1저자 지시 2026-09-15)
>
> 탄성 실측 09-15 17:07 = **strain 5/12 완료 · `strain_33_m` 진행 중(8.5 h 경과 · BFGS 9스텝)** · 대기 6.
> 점마다 BFGS 스텝 수가 달라 편차가 크다 — 남은 7점이 **대략 3–5일**(보장 아님).
>
> **끝나면 할 것 (15초)**: gabia 에서 Li₂S G1 파일럿 1점(t=20 ps)을 던져 본다.
> · 되면(`iteration # 2` 이상) → 마감 재개 조건 ① 충족 → 1층 트랙 재개
> · `cuMemAlloc` OOM → device 도 부족 → **완전 종결**
> · host OOM·스왑 폭주 → host 가 벽 → **종결**  (옆 창에서 `free -g` 같이 볼 것)
> ⭐ 근거: 실패한 것은 **단일 device 할당 23.03 GB** 이고 A6000 은 **48 GB** 다.
> 그리고 지금 그 카드에서 pw.x 가 **40 GB 를 점유한 채 돌고 있다**(실물 증거).
> ⚠ 단 host 62 GB vs 추정 110.15 GB 는 **미검증** — 반반이다. 마감은 그때까지 유지.
> 카드: `db/properties/lpscl_li2s_layer1_closed_2026_09_15.json`

> ### 🔴 새로 발견 (2026-09-15) — `/explorer` · `/governance` 에 **본문 별표가 노출된다**
> 렌더 실측: `/explorer` `**` 88개(표본 44 중 **본문 35** · 툴팁 9) · `/governance` 42개.
> `/` 와 `/cascade` 는 0 (오늘 고쳤다). **음성시험이 이 두 표면을 안 본다** —
> `test_no_literal_markdown_asterisks` 는 `/cascade` 3개 URL, 카드 시험은 `/composition/<Nd>` 뿐이다.
> ⇒ ① 두 표면을 음성시험 목록에 추가 ② 본문 35곳에 `|bold` 배선. 툴팁(`title=`)은 **평문으로** 고친다
> (HTML 태그가 안 먹어 `|bold` 로 못 고친다 — 오늘 `non_citable` 범례에서 실측).

**남은 것 (이 트랙)**
- ✅ **SDCP 본문 DFT(슬랩) 문단 확정 (2026-09-15, 1저자 "이걸로 확정")** — 원장 정합 점검 통과. 확정본과 변경 3건은
  `kb/papers/self_doping_dft_paragraph_2026_09_08.md` §확정본. 제출 전 남은 손질 둘: **"The deprotonated." 두 단어 꼬리 삭제** ·
  **Table S1 `Ref. 48/49` → 본문 번호 `[51,52]`** (`table_s1_build.js` 46–47행 → docx 재생성)
- ⏳ **1저자 결정**: ① SDCP 원고 코드 표기 **QE**(원고·Table S1 09-08) vs 값을 낸 코드 **VASP**(methods_dft_v9 08-30) — wave1 값이 BLOCKED 인 지금은 안 보이지만 값 복구 시점에 맞춰야 한다 ② 개정문 사후판정 논리 정정(`lpscl_li2s_layer1_amendment_2026_09_12.json` → 회신 BR) 비준 여부
- 인계 §6-2 `main` 병합 금지 범위 (ADR 0009 는 다른 브랜치 문서) — 1저자 판정 사항, 미판정
- 다른 세션 메모 "체크포인트 로컬 overlay" — **안 했다**: 1.1 GB × 16 호출을 2일 라운드에 펴면 몇 분이고 GPU-h 예산을 안 먹는다(V100 카드 자체 논리). 라운드 사이에 심볼릭 링크 → 로컬 복사 + sha256 대조로 하면 된다

### ⏭-NOW-h. 2026-09-15 새벽 — **E′ 파일럿이 V100 에서 돈다.**

| 트랙 | 상태 |
|---|---|
| **E′ 파일럿** | 🟢 **실행 중** — V100 tmux `eprime`. out_root `$STORE/runs/eprime_2026_09_14`, 로그 `$STORE/runs/eprime_2026_09_14.log`. 준비 5 + MD 11 호출 = **30런**, 상한 10 / 120 GPU-h (비준). code_id `634da438b`. 감시는 `tools/doping/watch_eprime.py --out_root …` |
| **G1 (Li₂S 1층)** | ⛔⛔ **미실시로 종결 · 1층 트랙 마감 (2026-09-15)**. ①② kgy GPU 단독 14–15초 OOM · **pw.x 실측 110.15 GB** (GPU 24.6 · 노드 26 · gabia 48 전부 미달) · ③ MPI 는 분산이지 감축 아님 · **④ KISTI 접근 종료**. 사다리 소진. ⚠ §6c "Davidson 4벌 ≈ 18 GB" 가 틀린 추정이었고 ②③이 그 위에 세워져 있었다. ⇒ 1·2층은 **'UMA 미검증 조성' 표지로만 · 인용 금지**, 남은 시드 4개 **영구 보류**(7.4일 절약). 마감 카드 `db/properties/lpscl_li2s_layer1_closed_2026_09_15.json` (재개 조건 셋 · 1저자 비준 대기) · ✅ **대각화기 축 종결** — `cg` 단독 적용 실측도 110.15 GB 그대로(Davidson·ndim2·cg 셋이 같은 수). 이 추정에 대각화기 작업공간이 안 들어간다 ⇒ 어느 대각화기도 안 내려간다. ⭐ **남은 후보 하나: gabia GPU 48 GB** — 실제로 터진 것은 **단일 device 할당 23.03 GB** 였고 48 GB 카드는 그걸 담는다(⚠ host 62 GB 가 110 추정에 미달이라 host 에서 막힐 수 있다 — 미검증). **탄성 ~6일 끝난 뒤 15초 시험**, 되면 재개 조건 ① 충족 |
| **회신 BR 후속** | ⏸ 300 K hold 연장(동역학 갇힘 진단 ②)은 G1 뒤. 나머지 4시드 보류 유지 |
| **브랜치 병합** | ✅ **§4.1 병합 완료 (2026-09-15 새벽, `47e080690`)** — `claude/windows-reinstall-backup-oducnh` 12커밋 3-way merge. 충돌은 `kb/index.md` 만(재생성). 검증 사다리 통과 — 단 **webapp 시험은 병합 전부터 3건 떨어져 있었다**(`/cascade` §4b 패널 `p4b.*` 6슬롯이 `|bold` 없이 db 문자열을 찍어 `**` 노출 · 09-13 `e6ad796e7` 부터 · 인계 문서 §7 사다리에 webapp 시험이 빠져 있어 아무도 못 봤다) → 이 커밋에서 고침. ⚠ **정정: "파일 5개가 없다" 는 이름 기준이었다 — 실체는 08-23 판이고 우리 쪽에 더 새 판이 있었다** (`Table_S1_DFT_parameters.docx` 09-08 · `methods_dft_v9` 08-30 · 문단 카드 09-08). **9/16 마감 위협 아님.** 회수본 머리에 대체 표식을 달았다(`docs/manuscripts/README.md` · 두 md 머리). 건진 것: `tools/sdcp/check_ldauu_provenance.py`(U 6.2 = MP 세트, 7/7) · 리비전 방어 카드 · VASP↔QE 변환표. ⏳ **1저자 결정 남음: 원고 코드 표기(QE) vs 값을 낸 코드(VASP)** — 값 복구 시 맞춘다. §4.2 는 §4.1 부분집합(안 함) · ✅ **§4.3 rescue 잔여 2건 키 대조 닫음** — `modelc_nd_doped.json` 에 저쪽만 있던 블록 34키(`dft_validation_2026_06_16`, pair01 v0 계보·U=8.0)를 `⚠_계보` 표식과 함께 회수, 세미나 md 는 Axis-3 보강 블록만 부록으로 · §6-2 main 병합 금지 범위 미판정 |

**바로 볼 것 (순서)**
1. **첫 prep 이 rc=0 인가.** `torch 2.14 + fairchem 2.22` 는 공식 조합이 아니고, 확인된 것은
   **단일점 추론 한 번**뿐이다. 수백 스텝 FIRE 가 첫 실사용이라 여기가 첫 위험 자리다.
2. **속도 시험(H0 600 K s1) 실측 GPU-h.** 소상한 10 을 넘으면 러너가 스스로 멈춘다(rc=4).
   넘지 않으면 남은 29런 투영이 총상한 120 과 대조된다.
3. 끝나면 집계·자격 판정은 **러너 밖**이다 (`msd_diffusive_check.aggregation_eligible`).

**V100 접속 규율** (`kb/platforms/v100_uma_setup_2026_09_14.md` 함정 ⑥·⑦)
- `LD_LIBRARY_PATH` 를 **셸에 export 하지 않는다** — `env … python` 앞자리에만. 전역이면 ssh 가 깨진다.
- ssh 는 `env -u LD_LIBRARY_PATH ssh $SSHOPT kgy@59.12.161.91`. `~/.ssh` 가 root 소유라
  설정 파일을 못 쓴다 → 옵션을 명령줄로.
- repo 갱신은 `git archive` 한 스트림. ⛔ **라운드가 도는 중에 `tools/` 를 통째로 덮지 않는다** —
  manifest 의 `code_id` 와 실제 실행 코드가 갈라진다. 필요한 파일만 `git show` 로 집는다.

### ⏭-NOW-g. 2026-09-15 새벽 — **V100 이 열렸다. G1 은 modelc 뒤.**

| 트랙 | 상태 |
|---|---|
| **V100** | ✅ **완료** — `max\|F\| 0.1626 eV/Å · Tesla V100-PCIE-32GB`. 함정 다섯을 `kb/platforms/v100_uma_setup_2026_09_14.md` 로 묶었다 |
| **G1 (kgy)** | ⏸ **modelc 종료 대기**. 파일럿이 GPU OOM 실측을 남겼고 재시도 사다리 4단계가 카드 §6c 에 있다 |
| **modelc** | 돌는 중 (9h+) — 안 건드린다 |

**바로 다음 (순서대로)**

1. **E′ 파일럿** — V100. repo clone(`~/lldvar`, sparse) → `tools/doping/run_eprime_pilot.py`.
   비용 상한 10 / 120 GPU-h 비준됨(`D-2026-09-13-cascade-pilot-estimand-v5-eprime`, active).
   ⚠ 실행 전 매번: `export LD_LIBRARY_PATH="$CONDA_PREFIX/lib:$LD_LIBRARY_PATH"` · `export HF_HUB_OFFLINE=1`.
   ⚠ 초반 출력을 한 번 더 본다 — torch 2.14 + fairchem 2.22 는 공식 조합이 아니고 단일점 하나로만 확인했다.
2. **G1** — modelc 끝나면 `nvidia-smi` 로 여유 확인 후 `run_force_check_scf.sh`.
   또 OOM 이면 사다리 ②(`diago_david_ndim=2`) → ③(CPU NP=8) → ④(KISTI).
3. **리뷰 BR 후속** — 유지시간 연장(갇힘 진단 ②)은 G1 결과 보고 결정. 남은 시드 4개는 계속 보류.

**오늘 닫힌 것**: turbo 응력(10프레임, ΔV/V ≤ 0.0017 % — 원인에서 배제) · 원자료 7파일 해시 회수 ·
G4 를 경보로 강등(비준) · 개정문 사후판정 논리 정정(비준) · 유지구간 +0.39 % 표류 발견.


### ⏭-NOW-f. 2026-09-14 저녁 — **회신 BR 이 내 해석을 반려했다. 순서가 바뀌었다.**

> ⛔ 내가 쓴 *"압력·밀도가 평탄하므로 셀 문제는 배제됐다"* 는 **틀렸다**. 우리가 가진 것은
> 마지막 10 ps(표본 11개)의 **단기** 안정성뿐이다. 철회 기록은
> `db/properties/lpscl_li2s_layer1_g2_seed1_2026_09_14.json` §0·§2·§5.

**회신 BR 권장 순서 (이 순서대로)**

1. **기존 기록 확인** — 유지 구간 **전체**의 블록별 압력·밀도 추세. 새 계산 0, 제일 싸다.
   도구는 됐다: `melt_quench_uma.py --gate_check <run> --hold_blocks 5`.
   ⛔ **thermo.csv 가 아직 없다** — base64 전송이 두 번 깨졌다(263/1051 행만 살아남음). 평문으로 받는다.
2. **같은 프레임 모드별 응력 대조** — turbo − default. 미리 정한 프레임 표본, 새 MD 0 (traj.xyz 에서).
3. **400원자 G1** (QE PBE, 힘 **+ 응력**). 소수 점 선평가 → 명백한 실패면 중단. 단 초기 통과를 전체 통과로 읽지 않고 **사전 지정 표본 범위** 유지.
4. 필요할 때 **제한된 이력 진단** (①시작밀도 짝 ②300 K 유한 연장 ③압축-해제 — 자격은 기록 §7).
5. **남은 시드 4개** — 보류 유지.

**비준 대기 (1저자)**
- `D-2026-09-14-li2s-layer1-density-alert` — **G4 는 합격선이 아니라 적정성 경보**. proposed.
- 개정문 사후판정 논리 정정 (`lpscl_li2s_layer1_amendment_2026_09_12.json` → `⛔_정정_2026_09_14_회신_BR`).
  결과를 보고 정한 기준은 **탐색 기준**이다. 이미 본 자료를 사전등록 합격으로 바꾸지 못한다. G1 응력 문턱도 같다.

**V100**: `/tmp/fix_torch.sh` (torch cu126 **fairchem 뒤에**) → `sm_70 ✅` → E′ 파일럿. kgy 와 안 겹친다.


### ⏭-NOW-e. 2026-09-14 오후 — **1층 g2 seed1 이 끝났다. 다음 한 수는 G1.**

1. **G1 (QE 단일점 대조) 을 먼저 돌린다.** 남은 시드 4개(44.5 h/시드 = **7.4일**)는 **보류**.
   G1 불통과면 1·2층 결과는 'UMA 미검증 조성' 표지로 인용 금지다 — 그 표지 달 구조를 더 만들지 않는다.
   개정 ⑧ 에 따라 **응력**을 포함한다 (문턱은 대조를 돌린 뒤 봉인 — 지금 정하면 사후 맞춤).
2. **turbo 응력 단일점 2번** (스냅샷 1점, turbo vs 기본). 비용 ≈ 0.
   turbo 등가성 카드가 스스로 "힘만 봤다" 고 적었는데 이번에 다투는 양이 응력이다.
3. **원자료 회수**: kgy `<li2s_layer1_g2>/A/seed1/{plan,result}.json · thermo.csv · gr_partials.csv`
   → `db/properties/li2s_layer1_g2_raw/A_seed1/` + sha256 결박.
   그 전까지 `db/properties/lpscl_li2s_layer1_g2_seed1_2026_09_14.json` 의 수치는 **붙여넣기 출처**다.
4. **리뷰 BR 발송 대기** — `kb/reviews/codex_BR_prompt_li2s_layer1_g2_density_2026_09_14.md`
   (결정 기준 밴드가 비정질 합격선이 될 수 있나 · cross-net 의 지위 · 갇힘 vs 평형 · turbo 응력 · G1 셀 크기).
5. **V100**: `/tmp/fix_torch.sh` (torch cu126 **fairchem 뒤에** 강제 재설치) → `sm_70 ✅` 확인 → E′ 파일럿.

> ⚠ 1층 밀도 −17.86 % 는 **G4 가 발화**하지만, 게이트가 적어둔 원인("셀 문제")은 같은 thermo 가
> 배제한다 (⟨P⟩ −0.03 ± 0.08 GPa · ρ 평탄 0.34 %). **멈추는 것은 맞고 원인 이름은 틀렸다.**


### ⏭-NOW. 2026-09-13 기준 (git log · selftest · 회신 원문 · 서버 화면 실측)

> 하루에 바뀐 게 많다. **막고 있는 것은 딱 둘**이다 — 1저자 비준, 그리고 빌더 규칙 하나.

#### ⏭-NOW-b. 같은 날 **저녁 최종** (2026-09-13 18:30 · 위 ⏭-NOW 보다 이게 최신)

> ⏭-NOW 는 회신 BP 시점이다. 그 뒤 **BQ → BQ-2 → BQ-3 세 리뷰가 왔고 스윕이 끝났다.**
> 회신 BQ-3: **§4b 해제 NO-GO 유지 · 다음 진단 10스윕 조건부 GO · MD 승인 아님.**
> 실행 전 최소조건 3개를 **전부 이행**했다. 지금 막고 있는 것은 **V100 에서 10스윕을 돌리는 것**과
> **25줄 원자료를 repo 로 가져오는 것** 둘이다.

**⏭ 바로 다음 (순서대로)**
1. ~~25줄 원자료 회수~~ **완료 (커밋 `214cbcf5d`)** — `db/properties/cascade_pilot_4b_raw/` 26개.
   repo 안에서 재판정 재현: 판정 0/25 · 사유 16/25 · V100 결과와 줄별 **0 차이** ·
   새 규칙(양방향 수렴) 조건별 자격 2/1/3/1/1 — 옛 규칙과 같다. `regate_inrepo_<commit>.json`.
2. **10스윕 실행** — `tools/doping/run_eos_10sweep.py` (동결: 5구조 × W3_f02/W3_f005 · ±3 % 7점 ·
   relax 3000 · `--apply_eos_v0 --fixed_shape_relax --no_anneal --no_elastic`). 한 라운드 고정,
   CLI 로 조건·분율 변경 불가, MD·탄성 자동 진행 없음. ⚠ **선언된 차이**: 25줄 스윕은
   `--fixed_shape_relax` 가 없었다(0단계가 CellFilter=GAP-2) → 그 축은 25줄과 직접 비교 불가.
3. 끝나면 `round_closed.json` 의 조건별 자격 집계를 보고 **사람이** 종료 문구를 고른다:
   "준비 확보(어느 한 조건 5/5)" / "정한 준비법·비용 안에서 v4 파일럿 준비 미확보".
   ⛔ 결과 보고 구조별 유리한 조건을 섞지 않는다 · 실패해도 창·시드·문턱을 넓히지 않는다.
4. 그 다음 BQ-4 — 10스윕 결과 + 원자료로 §4b 최종 해제를 다시 묻는다.

**⛔ 내가 BQ-3 에서 틀린 것 4건** (`cascade_pilot_4b_blocked_2026_09_13.json` → `⛔⛔⛔_회신BQ3`):
§4b① 오인용("per-구조 EOS V₀" 가 아니라 "같은 형상 정책") · "완화 부족이었다" 확정 →
조건부 표현 · "조건 독립성" 프레임 → "설정별 적합 결과와 사용 자격" · 원자료 미제공.

**BQ-3 최소조건 이행 (커밋 `f20875fb7` 이후, selftest 121 → 141 · 드라이버 9)**
- ① 자격에 **양방향 수렴** 요구(하강 0/7 → 거부) · 기록↔부피점 **1:1 대응** · `_conv_verdict`
  **유한 힘 기준만**(반환값·NaN 으로 못 덮음) · 문구 "한 골짜기로 정의되지 않는다" 삭제 ·
  regate 에 `eligibility_changed`.
- ② 점별 extxyz 프레임(셀·PBC·atom_id·힘·E·σ·메타, **미수렴점 포함**, 재독 ≤1e-8 Å) ·
  승계 = 상승 가지 **|Vᵢ−V₀| 최소 수렴점**(동률=낮은 인덱스) + 확인 순서 ①~④ 기록 ·
  `compare_frames`(골격 병진 제거·MIC·Li/골격 RMSD 분리·이웃 ID 집합 — **판정 안 함**) ·
  **결과 폴더 재사용 거부** + 최종 파일 sha256·run_id 결속.
- ③ `run_eos_10sweep.py` — 동결 사양 · flock 가드 · dry_run · 판정 없는 집계.

**§4b 셀 정책 — 스윕 완결, 판정 대기**
- `ALLDONE 18:11:09`. 5조건 × 5구조 = **25/25**. `--regate` 소급 재판정:
  **판정 변경 0/25 · 사유 변경 16/25**.
- ★ **V₀ 조건간 산포 + 자격**: 질서 H0 **0.05 % · 5/5** / P1_B 0.72 %·2/5 /
  P2_A 2.01 %·**0/5** / P1_A 3.38 %·1/5 / P2_B 32.98 %·**0/5**.
  V₀ 는 Å³ 단위라 분모가 없다 — 회신 BQ Q2 의 창 의존 비판에서 자유롭다.
- ⚠ **B₀′ 는 질서 구조에서 fmax 0.005 면 창과 무관해진다**(4.34/4.38, 창이 2배 다른데도).
  f02 의 2.1배 흔들림(4.12/5.82/8.72)은 물리가 아니라 **완화 부족**이었다.
- 원장 `db/properties/cascade_pilot_4b_regate_2026_09_13.json` (**citable: false**) ·
  화면 `/cascade` §4b 패널이 그 파일 **하나만** 읽는다.
- ⛔ 이 런의 `final_v0_applied` 구조는 **검증 전까지 MD 입력으로 쓰지 않는다**(리뷰어 지시).
- **남은 것은 Q1b/Q3 하나** — 점별 셀·좌표 저장 + V₀ 최근접 수렴점 승계. 재실행 필요(1.5 h,
  조건 2개로 줄이면 36분). **이것만 사후 복원이 불가능하고, 하필 골짜기 질문에 답한다.**

**BQ-2 이행 완료 (커밋 `48f78ee0` → `1d4ef323`, selftest 53 → 110)**
- P0-1 `downstream_eligible`(자격 ≠ 적합품질) · P0-3 실패 구조 승격 차단 ·
  Q1a 수렴 정의 오탐 · Q2 shape/offset 배선 · Q5 경계 최소 + `v0_centric_ok` ·
  Q4 `--audit_pressure`(산술 판정, 일괄 반전 금지) · Q6 추론 설정 실기록 + **turbo=TF32 정정** ·
  `--regate` · watch 두 갈래 분리.
- ⛔ **철회 2건** (`cascade_pilot_4b_blocked_2026_09_13.json`): *"7/7 수렴 → 미수렴 가설은
  죽는다"*(상승 갈래만 셌다) · *"창 좁히니 26·247배 → 창 효과로 설명 안 된다"*(공통 부피점에서
  비교해야 한다). **숫자는 실측이고 철회한 것은 추론이다.**

**오늘 잡은 결함 둘 — 같은 부류다 (계산은 했는데 결과가 쓰이는 경로에 안 닿았다)**
- `data.list_papers` 가 머리말 **첫 18줄**만 읽어 `digested` 표기를 놓쳤다 →
  논문 **최소 7편**이 265편 목록 맨 뒤로 **조용히 가라앉았다**. 창 60줄로 넓히고 회귀시험 2건 추가.
- webapp claim 결속이 **장식이었다** — `forbidden_phrases` 가 없어 스캐너가 찾을 문자열이
  없었고, `data-claim` 을 지워도 음성시험이 통과했다. 문구 등록 후 제대로 빨간불.
  ⇒ **표면을 추가하면 음성시험을 반드시 실제로 돌려본다.**

**litdb — 5편 전부 들어왔다**
- #114 Yu · #115 Li-FDI · #116 Li-NaRev · #117 Makino · #118 Wang(Li-rich Mn, 945행).
  전부 digest + INDEX + 그림. webapp 265편.
- ✅ **Li₃N 등재 완료 (2026-09-13)** — MP α P6/mmm **0.984 eV** · β 1.218 → **둘 다 `conductor-LEAK`**.
  [Li26FDI] 의 대체재가 우리 기준으론 개선이 아니다 ⇒ 그들은 **다른 축(이온수송)** 을 말하는 게 맞다.
  ⛔ 그 조회 중 **더 큰 것**을 찾았다: `sei_product_gaps.py` 가 `E_hull or 9e9` 때문에
  **최소 E_hull 항목을 구조적으로 배제**하고 있었다(0.0 은 파이썬에서 거짓). 2026-06-24 이래 전 값이
  준안정 다형의 갭이었다. 재조회로 10개 전부 정정 — **역할 분류는 하나도 안 바뀌었다**(칸 유지).
  `HZ-sei-gaps-pre-20260913-nonground-polymorph` 등록.
- 🔴 **여전히 미해소: Li₃P 4자 충돌 자체.** 우리 `sei_products.json` gap 0.70 eV=`conductor-LEAK` ↔
  `[Xiao20Rev]` *"passivating"* ↔ `[Li26FDI]` *"이온수송이 문제"* ↔ `[Zhu15]` 산화한계 0.85 V.
  그리고 **[Li26FDI] 가 고른 대체재 Li₃N 이 자기 Fig.1g 최협갭**(figure-read ≈1.1 eV)인데
  우리 표에 **Li₃N 이 없다**. ⇒ 결정 실험 1건: **Li₃N 밴드갭을 DFT 로** 재서 등재.
  ⚠ UMA 금지(2026-06 판정) · fixed-occ nscf VBM/CBM 만 인정.
  ⛔ 이 계산이 문헌 논쟁을 끝내지는 않는다 — **우리 원장의 자기정합성**을 메울 뿐이다.

**배포 — 확인 불가 상태로 남아 있다**
- `render.yaml` 에 **`branch:` 도 `autoDeploy:` 도 없다.** 둘 다 Render 대시보드에만 있는
  암묵 설정이라 레포에서 확인할 수 없다. 세션 프록시가 외부 사이트를 막아(403) 라이브 대조도
  불가. 화면 캡처의 "완성 259편" vs 로컬 265편이 배포 지연인지 집계 차이인지 **미확정**.
  ⇒ 대시보드에서 ① 배포 브랜치 ② Auto-Deploy 여부 ③ 마지막 배포 커밋 을 확인해야 한다.

**cascade 재건 — 회신 BP 수령, 파일럿은 "실행 전"**
- **정적대조 ④⑤ 완료.** V100(Tesla V100-32GB)에 QE 7.4.1 GPU 를 새로 세워 돌렸다
  (NVHPC 24.11 · `-gpu=cc70,cuda12.6` · hpcx · 랭크1/`-nk 1` · 점당 7~10분).
  결과 `db/properties/static_pair_dft_2026_09_13.json` · 원본 `runs/static_ab/{a,b}/scf.out` + `compare.json`.
  **δΔE +6.13 meV/atom** · 힘 벡터 RMSE 0.0655/0.0971 **⚠경보 0.05 초과** · 응력차 0.193/0.215 ✅.
  **(a) 고정셀 원자 정상점 후보**(|F_DFT| 0.00093) · **(b) 는 DFT 정상점 아님**(0.0888, S 최대 0.160, 등방압 0.402).
  **오차가 S 에 몰린다** — (b) 에서 DFT 가 S 를 10.6배 세게 당기고 방향은 반대(전체 cos −0.979).
- **회신 BP: 조건 1 이행 인정**(리뷰어가 해시 대조 + δΔE·힘 RMSE 독립 재현). **파일럿 조건부 GO**,
  ⛔ **"지금 코드 그대로의 즉시 실행 승인은 아니다"**. 원문 `kb/reviews/codex_BP_reply_static_pair_result_2026_09_13.md`.
- **카드 v4** `db/properties/cascade_rebuild_estimand_card_v4_2026_09_13.json` (v1·v2·v3 보존).
  보고량이 **"형상 제약을 포함한 처방 총효과"** 로 바뀌었다 — 전단은 P1·P2 에서 **상쇄되지 않는다**.
  §4b 셀 정책 선결조건 5 · §4c Q6 운영 판단(실행 **전에** 기록) 신설.
- **거버넌스 등록** `D-2026-09-13-cascade-pilot-estimand-v4` (proposed). ⚠ 카드 v1·v2·v3 는
  **결정으로 등록된 적이 없었다** — CLAUDE.md 가 요구하는데 빠져 있었고 v4 에서 처음 붙였다.
- ⛔ **셀 정책 3간극** `db/properties/cell_policy_gap_2026_09_13.json` (BP 지적 → 우리가 실물 확인):
  GAP-1 'fixed-cell' 은 **DFT 에만** 걸린 정책(바로 다음 줄이 `UMA full relax`) ·
  GAP-2 UMA 기본 경로가 형상 무제한 `CellFilter` ·
  **GAP-3 `eos_sweep` 이 `atoms_ref` 를 안 바꿔 EOS V₀ 가 후속 탄성에 전달되지 않는다**(post-anneal 구조가 들어간다).
  → GAP-2·3 코드 이행 (`run_mlip_postproc.py --apply_eos_v0 --fixed_shape_relax`, selftest **14/14** 음성 5).
  GAP-1 은 README 에 적용범위 명시. **기본 동작은 안 바꿨다** — 미적용 시 record 에 경고가 박힌다.
- **BO 조건 감사** `db/properties/bo_conditions_audit_2026_09_13.json` — 카드에 **적힌 것**과 코드에 **있는 것**을 갈랐다.
  #1 ✅ · #5 ✅ · #3 🟡(독립 홉 사건 정의를 기존 도구와 **대조 안 함**) · #4 ⬜(분석 단계, 지금 불필요)
  · 🔴 **#2 — 카드 §1b 의 'O 3개가 서로 다른 P 에' 규칙이 빌더에 없다**(grep 0건).
- **⏭ 막고 있는 것 = 이 #2 하나.** 빌더 강제(패치) vs `planA.json` 수동 확인 — **1저자 선택**.
- **⏭ 비준 대기 8건**: 카드 v4 · `D-2026-09-13-…`(결정) · `cell_policy_gap` · `bo_conditions_audit` ·
  `static_pair_dft` · `static_pair_uma` · `cascade_axis_global_audit` · `cascade_reanchor` · `b2o3_mechanism_correction`.

**논문 에이전트 — 계보 9/9 완료 + MERGE 완료**
- #7 Nolan **2018**(*Joule* 2, 2016–2046) · #8 **Xiao** 2020(*Nat. Rev. Mater.* 5, 105–126) · #9 Lu 2024 digest 작성.
- ⚠ **계보 카드 #8 행의 서지가 틀렸었다** — 1저자는 **Yihan Xiao**, 교신은 **Ceder**(Meng 아님),
  "Wang" 은 **Samsung**. ⇒ *"Cronk 2026 과 같은 Meng 그룹"* 연결 **무효**. inbox #104 `Bai2026` 에 이은 **두 번째 파일명 오기**.
- ⚠ **#7 은 2018 이라 #4(2019)·#5(2021)의 *조상*이다** — "방법 교과서" 는 후속이 아니다.
- ★ 우리 `interface_reactivity` 산물 5종이 전부 #8 에 예측으로 있고 **4종은 실험 관측까지** 붙는다 — 계보 8편 중 첫 지점.
- MERGE 완료 (INDEX 3행 · comparison Reference key 3 + 축 A4·B3·E1·F1 + J-7 블록 3 · 계보 카드 3행, `⏳ 대기` 0).
- 🔴 **형제 digest 충돌 3건은 합치지 않고 카드로 뺐다** — `kb/questions/coating_lineage_sibling_conflicts_2026_09_13.md`.
  제일 위험한 것: **1.717 vs 1.72 가 우연인가** (#6 은 우리 1.717 이, #7 은 우리 1.242 가 문헌 limit 자리라 한다).
  **⏭ 다음 수는 계산 0** — 레지스트리에서 `reduction_limit_V`·`ocv_self_decomposition_V` 의 `method` 를 읽는 것.

**화면(webapp)**
- **`/cascade/rebuild` 신설** — `kb/projects/cascade_rebuild_log_2026_09.md` 누적 일지(발표용). `md_html` 서버 렌더라 결속 자동.
- `/methods` **§3-1 신설** + 용어집 `fixed_cell_eos` — 고정셀+EOS 규약, 대가인 편차응력, 탄성 Cij 에 무는 자리.
  ⚠ 초판에 *"모든 구조가 공유하는 성질"* 이라 썼다가 **BP 정정으로 철회**(허용할 뿐 강제 아님).
- ⛔ **webapp 테스트를 못 돌렸다** — 이 컨테이너에 flask 가 없고 V100 sparse checkout 에도 `webapp/` 이 없다.
  **새 화면이라 음성시험을 꼭 통과시켜야 한다.**

**서버 (2026-09-13 03:30 화면 실측)**
- **gabia** `el`(modelc_2x 탄성): **strain 2/12 완료**, `strain_22_p` 진행, 대기 9. **~15 h/점** · GPU **31,824 MiB**.
  ⇒ 남은 ~9점 ≈ **6일**. ⛔ **다른 GPU 작업을 얹지 마라** — 러너 `MINFREE=32000` 가드에 걸려 다음 점이 멈춘다.
- **kgy** `li2s_layer1_g2` seed1 quench 153/1050 ps (23.9 ps/h, ETA 37.5 h, 담금질 **1e+12 K/s**) + `modelc_box331_400ps` 2/9.
  ⚠ **gabia 의 `/data/work/runs/li2s_layer1`(담금질 5e+12) 은 대체된 옛 세대다** — 거기 seed2 가 멈춰 있는 것은 정상이다.
  (2026-09-13 에 이것으로 헛경보를 한 번 울렸다.)
- **V100** (runyour, `ssh v100`): 32코어·125 GB·**V100-PCIE-32GB**·901 GB 여유. QE 7.4.1 GPU + repo `~/lldvar`(sparse) +
  pseudo 4종 해시검증본 `~/work/pseudo`. **GPU 유휴.** ⛔ 탄성은 못 받는다(31.8 GB 필요, 총 32.8 GB) ·
  UMA turbo 도 못 쓴다(Volta 라 bf16/TF32 없음) · SEI 큐 = li3nd(37.7 GB) 도 못 받는다.

**규율 점검**: kb lint **0 errors** · canonical validator **0 위반** · `convention_check` **0 위반** ·
selftest `generate_dft_inputs` 51 · `run_mlip_postproc` 14 · `run_force_check_scf` 6 · `build_qe_neb_gpu` 11 · `nav` 통과.

### ⏭-NOW. 2026-09-12 기준 상태 (git log · selftest · 회신 원문으로 받침 — 서버 실측은 오전 값)

> ⛔ **오늘의 교훈 — 기록을 먼저 읽는다.** cascade 앵커·게이트를 이틀 붙잡았는데
> `cascade_pipeline_anatomy_2026_08_13.md`(게이트 2.8 %)·`uma_relax_check_hosts.json`(comp1_k444 가
> DFT 평형 19.55, UMA 유지 +0.06 %)·`b2o3_ehull_result.json` 2026-09-07 정정(B–O 없음)에 **답이 이미 있었다.**
> 같은 자리에서 §6→§7→§8→§9→§10→§11→§12 정정 7회. 원인은 매번 "원시 파일 전수 전에 결론".

**cascade — 재건 (수리 아님, 1저자 결정 2026-09-12)**
- 회신 **BN NO-GO**(카드 v1·v2) → 회신 **BO 조건부 GO**: 정적대조 2 SCF + 한 대비 파일럿 ≤30 런,
  **'UMA 내부 진단' 한정**. 원문: `kb/reviews/codex_BN_reply_*` · `codex_BO_reply_*`. 카드 정본 **v3**
  `db/properties/cascade_rebuild_estimand_card_v3_2026_09_12.json` (v1·v2 보존, proposed — **1저자 ratify 대기**).
- host 교체: canonical(20.71, DFT 평형 **아님**) → **comp1_V0_k444 (DFT k444 평형 19.55)**. 재앵커 산술
  `cascade_reanchor_comp1k444_2026_09_12.json` — 단 'UMA 편향 ~0'·'가짜 basin'·'B₂O₃만 진짜 basin' 은 **가설**(BO).
- 도구 3종 준비 (selftest 통과): `run_force_check_scf.sh` 응력 완료검사 **6/6** · `substitute_compound.py`
  `--index_plan/--emit_index_plan` **16/16** · `generate_dft_inputs.py --static_pair/--compare_static_pair` **47/47**.
- **⏭ 다음 한 수 = `scratchpad/static_pair_sequence.md` ①→⑤**: gabia 블록(`static_b_geom_gabia.sh`, tmux `sab`)으로
  (b) 기하 + UMA 단일점 → scp → `--static_pair` → 러너 2점(kgy/gabia, pw.x·UMA 동시 금지) → `--compare_static_pair`
  → **회신 BP**. 파일럿(P1 Al₂O₃ / P2 Al₂S₃ @ Li_24g·S_16e, 공통 부모 2·속도 2·온도 3)은 ⑤ 뒤.
  ⚠ 빌더에 '16e O 3개가 서로 다른 P' 규칙 없음 — planA.json 손으로 확인.
- 강등: v23 3,615행 = 탐색 자료. 4축·front 39·`de_post_anneal` 판정 금지. 681 구조는 자산이나 새 표본 아님.
  `cascade_base_strain_2026_09_12.json` **superseded**(§12).

**b2o3 — 기전 서술 정정** (`b2o3_mechanism_correction_2026_09_12.json`, proposed)
- ⛔ 철회 "B 가 사면체를 싫어해 좌절". 실측 B58/B59 = **삼각 BS₃**(S 1.80–1.85, 4번째 이웃 Li), **B–O 0개**, O 는 P 인산염.
  고친 기전 = **B·O 분리**(열역학은 보레이트를 원함). 협업 md **v2** 발송(`BO-LPSCl 기전 제안 v2.md`) — v1 폐기.
- 포논 = **Γ점·셀폭 5.7/5.7/57.6 Å** 한계 명시. 전단 −2.87 은 같은 셀 → 아티팩트 의심. gabia `el`(QE 탄성) 결과 대기.
- cascade 오염과 **격리 확인**: b2o3 는 modelC host·DFT·V/atom 19.03 — canonical 안 거침. cascade 의 B2O3 52원자 행은 별개.

**서버 (오전 실측, 갱신 필요)**: gabia tmux `el`·`qe`·`w` 생존, GPU 100 % 41 GB(QE), UMA 프로세스 0. **⇒ (b) 블록은 QE 끝난 뒤.**
**논문 에이전트**: 계보 9편 중 **6 완료**, 남은 #7 Nolan 리뷰 · #8 Banerjee · #9 Lu 2024(본문 수령).
**비준 대기(1저자)**: 카드 v3 · `cascade_axis_global_audit`(BO 정정 반영) · `cascade_reanchor` · `b2o3_mechanism_correction`.

### ⏭-NOW. 2026-09-11 17:30 기준 **실측** 상태 (ps·nvidia-smi·tmux·git log 로 받침 · 14:40 판을 갱신)

> ⛔ **오늘의 교훈이 하나뿐이다 — 던지기 전에 서버를 본다.**
> 같은 실수를 **두 번** 했다. ① 힘 대조 파일럿을 아침 내내 다시 돌렸는데 tmux `fcgap` 에
> 09-09 완주 기록이 있었다. ② modelc 갭 nscf 를 다시 돌리려 했는데 gabia 에 09-03 완주본이
> 있었다. 둘 다 **계산이 아니라 기록이 밀린 것**이었다. `tmux ls` · `pgrep` · 런 디렉터리
> 전수는 30초다.

**▶ 지금 돌고 있는 것 (셋)**
- **gabia 탄성 — ⏸ 정지 (2026-09-11 18:50).** V0_relax 가 `forc_conv_thr 1e-4` 에 21 BFGS·809 SCF·12 h 동안
  |F| 2.5–3.2e-3 으로 진동만 했다(재점검 2번 갈래 만료). 박제 `/data/work/runs/elastic_modelc_2x/PAUSED_0911_1850/`
  (SHA256 기록). 개정안 `shear_b2o3_vs_lpscl16_2x_amendment_2026_09_11.json`(proposed · 관측 후): forc 1e-3 · etot 1e-5
  **두 계 동일**, PAUSED 기하 승계, strain 점당 60 BFGS 게이트. **1저자 비준 뒤, Li₂S 1층이 끝난 뒤** 재시작 (pw.x·UMA 동시 금지).
- **gabia Li₂S 1층 — ▶ 시작 (18:55 경)** `tmux l1` · `/data/work/runs/li2s_layer1/{A,control_li7ps6}/seed1..5` ·
  `melt_quench_uma.py` NPT 1200 K 100 ps → 10¹² K/s 900 ps → 300 K 50 ps · 시드당 ~6 h → 약 2.5 일. 판정 지표는 카드 §2 (결과 보기 전 고정).
- **kgy lpsocl MD — ✅ 마감 (값).** 9/9 완주 → 게이트 전부 충족 → `lpsocl_box331_closed_2026_09_11.json`.
  **Ea(3×3×1 cell-conditioned) = 0.180 ± 0.002 eV** (gen2 첫 등록, `MD_Ea_eV/lpsocl_box331_cell_conditioned`).
  C2 8/9 (600 K = s2·s3, R1) · C2b inter-cage 20/55/94 홉/이온 · C6 census 9/9 rigid(β 경보 3칸은 '이탈 없는 저β') ·
  C3 compatible (ΔEa −0.024, CI [−0.039, −0.008] ⊂ ±0.050 — 구간이 0 을 벗어나 다르니 '완전 직선' 은 금지) · C4·C5 충족.
  ⚠ 관측 후 개정(BL) 뒤의 마감 · ③ STO Ea 는 1저자가 봤을 가능성(tail -40 기록) — 결과 파일에 명시. 외부 리뷰 아직 없음.
- **kgy 힘 대조 — ✅ 판정 완료 (20/20).** `R = dF(b2o3)/dF(modelc) = **0.951**` (상대 0.943) ≤ 문턱 1.25
  → 봉인문구 **"두 계에서 UMA 의 골격 힘 정확도가 비슷하다"** — 조성 특이 포텐셜 결함 가설이 약해진다.
  b2o3 0.4198 / modelc 0.4417 eV/Å · cos 0.880/0.893. 기록 `b2o3_uma_vs_dft_force_result_2026_09_11.json` ·
  판정원장 `A-2026-09-11-b2o3-uma-force-contrast` (**diagnostic_unbound** — 인용 자격 안 바꾼다).
  ⛔ b2o3 전도도 축 인용 불가·β 게이트 not_assessed 는 **그대로**. ⚠ 봉인 밖 관측: 두 계 **모두** 상대 오차 0.53–0.56 —
  'modelc 는 믿고 b2o3 만 의심' 구도의 한 다리가 빠진다. 다음: ① 원소별 dF 회수(B·O 가 특히 나쁜가) ② MP 완화
  구조(in-distribution) 몇 점으로 0.42 가 온도 탓인지 화학 탓인지 가르기.
- **kgy Nd DOS** — PID 2400966 `run_gap_nscf_gabia.sh DOS=1 ndo_lpscl16_n5fu_O-distributed`.

**⏸ 되살릴 것**
- **SEI 큐** — 어제와 동일. 탄성이 끝나야
  `cd /data/work/repo && tmux new -s sei -d 'bash tools/sei/restart_qe_relax.sh --run'`.
  r2 박제 `/data/work/runs/sei_control/li3nd_mp-976264_p333_r2/PAUSED_0910_2304/`
  (step 40 · |F| 0.032609 · E −14652.33022106 · `.bfgs` sha 3feb4c36).

**✅ 오늘(09-11) 닫힌 것**
- **LPSOCl 3×3×1 캠페인 마감 (값)** — 위 '지금 돌고 있는 것' 항목 참조. 회신 BL 의 GO 항목 전부 이행(개정안 비준 · 도구 2판 · C2b 계수 · C6 census · C3).
- **Li₂S 카드 1층 개정(b)** — 타깃 a-Li₃PS₄·LiCl / a-Li₃PS₄+LiCl, a-Li₇PS₆ 대조잡. 조성 **3:5:2 (2 = VGCF)** 1저자 확인. 1저자: "논문처럼 Li₃PS₄ 쪽을 파자".
- **탄성 modelc_2x V0_relax 정체** — `forc_conv_thr 1e-4` 에 21 BFGS·800+ SCF, |F| 2.5–3.2e-3 진동(12 h). 재점검 2번 갈래 만료. 제안: 박제·정지 → 1층(UMA) → 두 계 모두 1e-3 으로 개정(관측 후·비준) 재시작. ⚠ 탄성 사전등록 무효조건 'pw.x·UMA 동시' 라 1층은 정지 뒤에만.
- **SDCP C-12 v41 발송 (1저자, 17:00 경) — v40 교체·폐기 통지.** v40 은 census/n_total 이 러너 작업폴더
  `_hostpool/` 을 잡 폴더로 세어 **첫 VASP 전에 멈췄다**(수정 `f90e82e63`·`fd16f0c52`, e2e selftest 에 재현 추가).
  v41: 잡 19개 지문 `8a7ae28f` 동일 · **잡 폴더 바이트 동일**(v40 zip 과 diff 0) · zip sha256
  `76d76d50e4da…` · 커밋 `521e18358`(IDENTITY/SEND_MAIL/zip). 차이 파일 = census.py · run_staged.sh ·
  MANIFEST.json · README_REQUEST.md · SUBMIT_CONTRACT.md(시작 전 확인·회신 절, v40 엔 없었음 — 메일에 밝힘) ·
  governance/decisions.json 사본(추가 결정뿐). 렌더러에 `--changes_md` 추가(분기 없는 교체판은 렌더 거부).
  **보고자 회신 대기.** gabia 미추적 `db/properties/neb_*.{log,xyz}`·`prospective_basins_…json` 은 별건.
- **litdb: Cronk 2026 Nat. Commun.** (파일명 'Bai2026' 은 오기) — 같은 DOI 의 두 번째 읽기축
  `cronk2026_lis_cathode_interphase_chemistry` (`19caadd6b`). LPSCl@Li₂S 카드 함의: 결정 Li₇PS₆ 배제 ·
  Li₂S 복합체 σ/Ea 는 문헌 공백 · 1층 조성 후보 2안(비정질 Li₃PS₄·xLiCl / Li₃PS₄+나노 LiCl) 은 1저자 판단 후.
- **gap 원장 4/4 해소 · N 항목 닫음.** modelc 실행본이 gabia
  `/data/work/runs/gap_nscf/modelc/nscf_gap.{in,out}` 에 있었다 — `occupations='fixed'` ·
  `K_POINTS 8 8 2` → **68 irr**(정본 일치) · VBM 2.4447 / CBM 4.5436 / **gap 2.0989**
  (정본 2.099, 소수 넷째 자리). ⇒ 네 계가 같은 `gap-fixedocc-eigenvalue-v1` 등급.
  **논문 표에 단서 없이 나란히 쓸 수 있다.** comp2 2.04 는 여전히 다른 줄.
  ⚠ 사본이 gabia 한 곳뿐(`needs_duplication`).
- **힘 대조 카드 §4 3판 비준** (`content_digest 87091598…`). `fixed` → `smearing/gaussian`.
  근거: b2o3 **0 K −TS 0.000** vs **700 K −TS −0.00318 Ry** matched 대조 —
  갭이 닫힌 건 조성이 아니라 **온도** 탓이다. `fixed` 는 nbnd=nelec/2 로 여유 밴드가 0 이라
  그 상태를 표현할 수 없다. beta 0.05~0.2 · ndim 8~16 · maxstep 400~600 **전부 실패**했다.
  ⛔ **smearing 종류가 갈랐다**: gaussian 49회 수렴 / **mv 118,698 Ry 발산**.
- **도구 3건** — `generate_dft_inputs` `--help` 가 철회된 local-TF 를 권하고 있었다 /
  `--smearing` 기본 mv → **gaussian** · `scf_from_xyz` 의 mv 하드코딩 제거(manifest 가
  호출부 값과 무관하게 "mv" 라고 거짓말했다) / `prereg_ratify` 가 `record` 만 봐서
  `kind:"estimand"`(=`card`) 문서의 **비준 자체를 막고 있었다**.
- **결정문 드리프트** — `D-2026-09-08-b2o3-uma-vs-dft-force` 의 statement 가 1판
  (800·1000 K · 온도 2축)으로 3일간 남아 있었다. 카드 기준으로 맞췄다.

**⏭ 바로 다음 (순서 있다)**
(17:30: 1 대조 잡 ✅ 통과 · 2 v2 20점 ✅ 기동 — 남은 건 3 과 아침 `--collect`.)
1. **대조 잡 판정** — `~/work/runs/fc_control_smear/modelc_2_t10ps` 실행 중(GPU, 회당 ~13 s).
   좌표해시 `bf6710fec368b7b8` 이 본배치와 **일치 확인됨**(§8 무효조건 1번 통과).
   `-TS` ~0 이면 대조군이 안 흔들린 것 → 2번으로. 크면 그 크기를 결과 파일에 적고 진행.
2. **힘 대조 20점** — ⚠ **입력 재생성부터.** 본배치 20점의 scf.in 은 local-TF 철회
   **9분 전** 생성물이다(러너 09-08 22:53:30 / 철회 커밋 23:02:32). 새 디렉터리
   `force_check_700K_v2` 에 만든다 — 옛 배치는 실패 증거라 덮지 않는다.
3. **ICOHP·DOS CSV 원장 등재 + claim 결속** (아래 남은 사무).

**⛔ 남은 사무 (짧다)**
- ICOHP·DOS CSV **원장 등재 + claim 결속** — 인용 제한 셋을 값 요소 *안*에:
  P–S −6.288 을 `ICOHP_PS` 와 못 섞음(방법 대조 안 함) · Rietveld 유래 대조군이라
  main track(cfg141)으로 못 옮김 · frozen-4f 라 4f 주장 불가 · DOS **곡선**은 irr 10 k
  tetrahedra 라 표시용(갭·성분비는 유효).
- `elastic.json` 의 **b2o3_champion 에 setup/strain_step/n_scfs 가 없다** (나머지 넷은 있다).
  2026-07-03 판의 입력이 어디에도 없어 그 Cij(K 27.02 포함)는 설정 미확인으로 남는다.
  canonical B0 24.48 은 별개 EOS 라 무관.
- **`gap2_{b2o3,modelc2x}`(156·160원자)는 세워뒀다** — 힘 대조와 **다른 셀**이라 카드의
  대조 잡이 아니다. kgy GPU 에서 OOM(128원자는 되고 160은 안 된다). 큰 셀 갭은 별건.
- **kgy 클론이 셋**이다: `~/lldvar`(정본) · `~/work/Yonghoon-DEM-DFT`(낡음) ·
  `~/Yonghoon-DEM-DFT`(**SDCP 원고 브랜치**). kgy 블록은 `~/lldvar` 만 쓴다.
  그리고 `python3` 은 `/bin/python3`(시스템)이라 **`$CONDA_PREFIX/bin/python`** 을 쓴다.
  tmux 서버가 7월부터 떠 있어 새 세션이 **옛 환경**을 물려받는다 — env 를 명령 문자열 안에.

<!-- 아래는 2026-09-10 판 (이력) -->
### ⏭-NOW(이력). 2026-09-10 23:20 기준 **실측** 상태 (ps·nvidia-smi·git log 로 받침)

**▶ 지금 돌고 있는 것 (둘)**
- **gabia 탄성 26잡** — `tmux el` · `/data/work/runs/elastic_{modelc_2x,b2o3}` · pw.x 30.9 GB.
  modelc_2x V0 relax SCF 3회차에서 시작. 러너 `tools/elastic/run_elastic_relaxedion_gabia.sh`
  (SYS=modelc_2x → b2o3 순차), 감시 `tools/elastic/watch_elastic.sh`. **2~4일.**
  사전등록: `db/properties/shear_b2o3_vs_lpscl16_2x_prereg_2026_09_10.json` (판정 네 갈래 봉인).
- **kgy 힘대조** — b2o3 9점 재시도 (`~/work/runs/force_check_700K`).
  아침에 `--collect` 20/20 → `force_contrast` R.

**⏸ 오늘 멈춘 것 — 되살려야 한다**
- **SEI 큐 전체 정지.** `tools/sei/restart_qe_relax.sh --run` 드라이버를 죽였고(GPU 양보),
  r2·r3 를 `prefix.EXIT` 로 깔끔히 종료했다. r2 박제:
  `/data/work/runs/sei_control/li3nd_mp-976264_p333_r2/PAUSED_0910_2304/`
  (step 40 · |F| 0.032609 · E −14652.33022106 Ry · `.bfgs` sha 3feb4c36).
  ⛔ **탄성이 끝나야** `cd /data/work/repo && tmux new -s sei -d 'bash tools/sei/restart_qe_relax.sh --run'`.
  먼저 걸면 드라이버 가드(GPU_FREE_MIB=20000)가 탄성 잡 사이 틈에 끼어들어 둘이 서로 민다.

**✅ 오늘 닫힌 것**
- **ndo_lpscl16 n5fu ICOHP** — spilling 1.75 % · **Nd–P 쌍 없음** · 배위수가 조성을 재구성
  (P 3개 전부 PS₃O · Nd 2개 전부 NdS₅Cl) · P–O −8.416 이 lpsocl −8.41 과 일치.
  → `db/properties/ndo_lpscl16_n5fu_icohp_2026_09_10.json`
- **DOS/PDOS** — gap 2.1616 (fixed-occ) · CBM 에 Nd 없음(S p 40 % + P s 25 % + Li p 16 %).
  CSV·PNG 가 `db/properties/ndo_lpscl16_n5fu_*` · `docs/figures/ndo_lpscl16/`.
- **b2o3 셀확장 진단** — 회색(판정 없음). 그리고 같은 날 감사가 그 해석을 좁혔다
  (`b2o3_vs_modelc_framework_fair_2026_09_10.json`): **"b2o3 고유" 는 공정 비교에서도 산다**
  (온도별 대면 4/4 분리) · 인용해 온 800 K 기준선 **0.79 는 P 가 만든 값**이라 modelc 과
  나란히 쓸 때는 {Cl,S} 기준 **0.66** · 온도 단조성 없음(900 K 0.21/0.77/0.29).

**⛔ 남은 사무 (짧다)**
- ICOHP·DOS CSV **원장 등재 + claim 결속** — 인용 제한 셋을 값 요소 *안*에:
  P–S −6.288 을 `ICOHP_PS` 와 못 섞음(방법 대조 안 함) · Rietveld 유래 대조군이라
  main track(cfg141)으로 못 옮김 · frozen-4f 라 4f 주장 불가 · DOS **곡선**은 irr 10 k
  tetrahedra 라 표시용(갭·성분비는 유효).
- `elastic.json` 의 **b2o3_champion 에 setup/strain_step/n_scfs 가 없다** (나머지 넷은 있다).
  2026-07-03 판의 입력이 어디에도 없어 그 Cij(K 27.02 포함)는 설정 미확인으로 남는다.
  canonical B0 24.48 은 별개 EOS 라 무관.

**오늘 고친 도구 (전부 우리 도구끼리 관례가 갈린 것)**
`<prefix>_dos.dat` vs `.dos` · `_pdos.` vs `.pdos.` · `E-EF` vs `E_minus_Ef` · repo 두 벌 ·
plot_dos 가 스무딩 없음(family σ 0.15) · plot_dos 가 y 자동배율을 창 밖 준core 델타에 맡김 ·
plot_dos 가 **DOS-threshold 갭을 인용 가능한 수처럼 라벨에 박음**(→ `[fixed-occ nscf]` 결속) ·
msd_diffusive_check 의 save_fs 가정·thin 표기 죽은 코드·라벨 중복 · 탄성 VRAM 가드 14000→32000(실측).

**2026-09-07~08 에 들어와 이 원장이 모르고 있던 것** (전부 `db/governance/decisions.json` 에 active):
- `D-2026-09-08-lpsocl-box331-closure-conditions` — LPSOCl 3×3×1 400 ps 9런 **닫힘 조건 확정**
  (아레니우스를 하나도 그리기 전에). C3 = ΔEa 직접계산 · δEa 0.050 eV.
  → `db/properties/lpsocl_box331_closure_conditions_2026_09_07.json`
- `D-2026-09-08-cascade-d-rel-estimand` — cascade 보고량 카드 비준 (아래 ⏭-2)
- `D-2026-09-07-b2o3-md-closure-retrospective` — b2o3 **UMA-MD 전도도 축 전체 마감**(D·Ea·σ·구간 Ea
  전부 인용 불가, 인용 가능한 수 0개) · `D-2026-09-07-b2o3-cell-expansion-diagnostic`(재개용 사전등록) ·
  `D-2026-09-08-b2o3-uma-vs-dft-force`(골격 creep 힘 대조, 결과 보기 전 봉인)
- 실측 재기동: `kb/projects/restart_runbook_2026_09_07.md` — **지금 무엇이 어디서 도는지의 정본**
- 규율: QE-GPU 런타임은 **`ldd` 로 바이너리에게 묻는다**(CLAUDE.md · `tools/doping/run_force_check_scf.sh`)

### ⏭-0. SDCP doped 재개 — **회신 R4 조건부 GO · Stage A 는 1저자 결정으로 정지** (2026-08-28 등록 · **2026-09-09 갱신**)

> ⛔ **2026-09-09 정정 — 아래 "▶ ORCA 8잡 실행 중" 은 사실이 아니었다.**
> 2026-09-07 실측(`kb/projects/restart_runbook_2026_09_07.md` §1·§3-2): desktop 의 Stage A
> **ORCA 프로세스 0개**, 재부팅 **전에도** 안 돌고 있었다. 실제로 이 캠페인에서 돈 것은
> `gs4`·`gs5` **둘뿐**이고 — `gs4` 수렴 완료(cyc 138 · `conv=1` · E −10051.702558950057 Eh),
> `gs5` 는 `rc=143`(=128+15 SIGTERM, 09-05 15:44경 밖에서 죽음) — **`gs0`–`gs3`·`gs6`·`gs7`
> 은 시작도 안 했다.** 종전 기록의 "gs0·gs1 완료" 는 **미확인**으로 둔다(0 이라고 적지 않는다).
> ✅ **1저자 결정 (2026-09-07): gs 는 돌리지 않는다** — *"gs는 돌리지말자, 굳이인거잖아"*.
> 근거: gs* 는 Stage B 의 부모 구조용인데 Stage B 가 회신 R4 **NO-GO** 이고, 원고 Figure 2e
> 는 gabia 의 doped n=6 이 답하며 그 경로는 gs* 를 안 읽는다. `gs4` 는 `DONE` 으로 남긴다.
> **재개 조건**: 그 전제(Stage B NO-GO · doped 경로가 gs 를 안 읽음)가 깨지거나 **중성 대조**가
> 필요해질 때. 그 밖의 이유로 다시 열지 않는다.
- 회신 R3: 실측 fail-open 5건 (seed 미강제 · 미이완 부모 수용 · dependency 문장뿐 ·
  analyzer fail-open · hybrid 미배선) + **관측량 회수 계약 P0** (Hirshfeld/UNO 입력 부재).
- ✅ 전건 구현 (`build_v7c_trimer.py` 재작성 3차): receipt 3중 결속 · seed/dmin 강제 ·
  depends_on + DEPENDENCY_NOT_MET · analyzer 양성증거/중복적발/PENDING 비영 ·
  Hirshfeld+UNO UCO 계약 · localization class 사전규칙 + remap validator ·
  hybrid 조성별 그룹 + NoAutoStart · --compare METHOD_DEPENDENT.
  **selftest 40건 = R3 GO 요건 9 의 1:1 봉인.** 실물 8-seed stage A 성공
  (고유 torsion 8벡터 · 전 접합 dmin ≥ 2.04 Å).
- ✅ **회신 R4 접수 (2026-08-29)** — `kb/reviews/codex_R4_doped_reopen_impl2_reply_2026_08_29.md`
  **판정: 중성 Stage A 8개 ORCA Opt 조건부 GO / Stage 0·Stage B·hybrid 전부 NO-GO.**
  검증 고정점 커밋 `096122b`. selftest 40건은 통과했으나 **별도 공격 재현에서 fail-open 다수** —
  R2(문서만 봄) → R3(실행해 봄) → R4(공격해 봄) 로 검사 강도가 한 단계씩 올라왔고 매번 걸렸다.
  - 새 위험 4: hybrid 가 **vertical XYZ 로 SP 생성**(adiabatic 최종구조 아님) · Opt 에
    `StabPerform` 없음(BS 는 SP 도 면제) · 예시 `--neutral_xyz` 경로가 **시작구조를 덮어씀** ·
    실제 cycle 은 4-leg 이 아니라 **6항**(`h1a·h1b·h2_s·h2_t·h2_bs·h0`).
  - P0-0~5 전부 **불충분**. 대표적 통과 사례: Löwdin 블록 없어도 OK · **UHF·+1·doublet 출력이
    neutral RKS 부모로 통과** · 주석 한 줄로 중복검사 우회 · 임의 문자열이 stable 증거.
  - localization 0.5/0.3 은 **라우팅 기준으로만** 조건부 수용. Hirshfeld 병기 + partition
    일치(`PARTITION_DEPENDENT`) + ring 별 집합 + BS 양·음 lobe 분리 필요.
- ~~▶ **ORCA 8잡 실행 중** (2026-08-31 실측: gs0·gs1 완료 · gs2 진행)~~ ⛔ **2026-09-07 실측으로 반증** (위 정정 블록). 🔴 gs2 가 gs0 보다 **137 meV 낮다**(미수렴) — 갈아타면 사후선택이라 gs0 로 간다. 집계는 **conformer 앙상블**이다: 두 극소가 창 0.030 eV 안이면 축퇴 집합이라 **최저값 단일 인용 금지** (`db/properties/sdcp_stageA_conformer_rule_2026_08_31.json`, proposed). ⚠ 실행 기계 표기가 문서마다 다르다(데스크탑 WSL vs gabia CPU) — 확인 필요.
- ▶ 종전 문구(참고): **데스크탑 ORCA 8잡뿐** (조건 6: SHA 동결 · `--allow_*` 전면 금지 ·
  읽기전용 정본 + seed 별 scratch · 시작/최종 XYZ 파일 분리 + SHA·ORCA 버전·명령 기록 ·
  builder 파일 SHA · **이 결과로 Stage B 를 열지 않는다**). GPU 자원과 경합 없음.
- ⛔ Stage B 의 열쇠는 계산이 아니라 **P0-2~5 재수정 + 회귀시험 6**
  (교차-seed/wrong-state receipt · localization 누락·행 재배열 · duplicate→dependency ·
  BS 안정성 · adiabatic 최종구조 hybrid · 빈 method 비교).

### ⏭-1. T13 확인 — ✅ **판정 완료 (2026-08-29)** — 본문은 이 파일 맨 아래 `## ✅ 닫힌 항목` 절로 옮겼다 (2026-09-09). 요지: 창 2–50 ps 는 200 ps 궤적 안이라 **길이는 문제가 아니었고**, 대신 **셀이 D 를 1.79배** 움직인다.

### ⏭-2. 39설계 D_rel 측정 — **회신 AL = NO-GO 유지.** 해제조건 8건 중 **5건 이행(#1·#2·#2b·#5·#6) + #7 봉인**, 남은 것은 **#3·#4·#8** (2026-09-09 갱신)

> ✅ **2026-09-08 비준·이행 (여기 반영, 종전 "7건 미이행" 은 낡았다)**
> - **#1·#2b·#5·#6 = 보고량 카드로 확정** — `db/properties/cascade_d_rel_estimand_2026_09_08.json`
>   (`status: ratified`, 1저자 비준 14:11Z) · 결정 `D-2026-09-08-cascade-d-rel-estimand` **active**.
>   · 보고량 = `D_rel(design, host)` = D*(design)/D*(host), **600 K · 2–50 ps 창 · cell-conditioned**.
>   · 설계의 대표 = **점수 중앙값을 낸 실제 행 하나**(행별 `score_row = 3·m+b` → 그 행의 구조·좌표
>     sha256·anneal seed 를 박고 MD 는 그 구조로 돈다). 짝수 복제본은 좌표 sha256 사전순 앞.
>   · **삭제된 것**: 300 K σ 게이트 · Deng **0.90 문턱** · 2온도 외삽 · `|ρ|<0.2 ⇒ 축 근거 없음`.
>   · 판정은 ρ̂ 단독 금지 — **ρ̂ + Fisher 95 % CI + 유효표본수**(클러스터 보정)로 보고하고,
>     n=39 로는 **±0.2 등가 반증 불가**(n≥69 필요)를 결과 보기 전에 선언했다.
> - **구현**: Step 1 `8c9338c96`(aggregate_designs → 대표 행 선택) · Step 2 `46566ca64`(어닐 seed·구조해시를 축 CSV 까지).
> - **#7 봉인 완료**: `db/properties/cascade_seal_v2_2026_09_08.json` (`label: v2_2026_09_08`,
>   sealed_at 2026-09-08T14:41:28, 미정 규칙 0건) · 커밋 `93d1eb98b`→`3e4e1492b`→`c221ac933`.
> - ⛔ **캠페인은 아직 승인되지 않았다.** 카드가 정한 것은 **무엇을 재는가** 뿐이다.
>   남은 해제조건 **#3(전 시드 end-to-end 재실행) · #4(label-blind v2 동결) · #8(39 밖 sentinel 파일럿)**.
>   금지 서술은 카드 §5 — 300 K σ·σ비·0.90 게이트, 2온도 외삽 300 K, `|ρ|<0.2` 근거,
>   bulk Ea/D, **v1 의 front·순위**, MLIP 순위를 물리 예측으로 읽는 것.

대상·견적: `db/properties/d_rel_targets_2026_08_28.json` (Pareto front 39, CSV sha256 포함).
규약 **600 K · 200 ps · 1시드 · 2×2×2**, 처리량 실측 25 ps/h → **312 GPU-h ≈ 2GPU 6.5일.**
✅ T13(2026-08-29)이 **1시드·200 ps 를 실측 확인**했다 — 길이는 증량 불필요.
🔴 **그러나 2×2×2 셀 수렴은 확인 안 됐다** (2×2×2 vs 3×3×1 = 14.4 %, 정합 두 시점).
전 설계가 같은 셀이면 **공통 편향은 비에서 상당 부분 상쇄**되지만, T13 이 "편향은 계마다
다르다" 를 실측했으므로 그 상쇄는 **가정이지 검증이 아니다** — 착수 전 표기 필요.
⚠ 조건 셋: 전 설계가 **같은 창(2–50 ps)** · **같은 셀(2×2×2)** · **두 창 병기 보고**.
~~축은 `D_rel_vs_host`(host 대비 비), 게이트 **0.90** (Deng 2026 의 σ 손실 7 % 허용 / 31 % 실패 사이).~~
⛔ **폐기 (회신 AL P0-5 · 2026-09-08 비준 카드 §1)** — Deng 의 7 %/31 % 는 **표면 코팅 LPSC 의 상온
pellet EIS** 라 벌크 25 % 치환 문턱으로 옮길 외적 타당성이 없다(물리 게이트가 아니라 임의 운영 cutoff).
tracer D 는 σ 게이트가 아니다. 현행 축은 **`D_rel`(600 K · 2–50 ps · cell-conditioned)** 이고
게이트 문턱은 없다 — 판정은 ρ̂ + CI + 유효표본수다. 정본: `db/properties/cascade_d_rel_estimand_2026_09_08.json`.
⛔ 절대 σ 로 되돌아가지 말 것 — `sigma_300K_S_cm_NE` 는 도구가 거부한다(인용 금지 규율).

🔴🔴 **2026-08-30 — 예측기가 자기 자신을 재현 못 한다 (새 계산 0)**
`db/properties/cascade_axis_retest_2026_08_30.json` · 재현 `axis_corr_csv.py --stability`
- 각 설계에서 점수가 매겨진 행 3개는 **한 시드 안의 x020/x050/x100** 이다 —
  배치가 아니라 **같은 구조의 재평가**다 (`screen_de_per_atom` 7자리 일치가 물증).
- 그런데 재검사 상관이 낮다: 예측기 `li_mobility_score` **ρ ≈ 0.22**,
  `bvs_li_proxy_score` **ρ ≈ 0.08**, 탄성 G 0.31, Pugh 0.26, 이동부피비 0.31.
  ⇒ **사전등록 문턱 |ρ| ≥ 0.35 를 예측기가 자기 자신과도 못 넘는다.**
- 같은 100설계에서 재평가만 바꿔 Pareto 를 다시 뽑으면 front 겹침 **Jaccard 0.23–0.27**
  (크기 33/38/37 vs 정본 median 29). front 구성원 대부분이 바뀐다.
- ⚠ 정본 재현은 정상이다 — median-of-3 재구현 front 가 사전등록 39설계와 **39/39 일치**.
  불안정한 것은 규약이 아니라 **그 규약이 딛는 축**이다.
- ⇒ 지금 던지면 실패 가지(|ρ| < 0.2 ⇒ '이동도 축 근거 소멸')가 **물리가 아니라
  재평가 잡음으로** 켜질 수 있다. 원인 진단(같은 구조에서 G 가 ±12 %) 전에는 안 던진다.
- 부수 실측: 큰 셀 단일시드 D RSD **8.4 %** ⇒ D_rel(1시드/1시드) RSD 11.8 %
  = 게이트 여유 10 % 가 **0.84σ**. 그리고 `D_rel(300)/D_rel(600) = exp(−ΔEa/k·600)` 이라
  600 K 게이트가 300 K σ 대리가 되려면 ΔEa < **5 meV** 여야 한다.
- ⛔⛔ **회신 AL 접수 = NO-GO** (312 GPU-h 본계산 **및 5×2 파일럿 둘 다 금지**).
  `kb/reviews/codex_AL_reply_cascade_d_rel_2026_08_30.md`
  - **내 '같은 구조' 전제가 틀렸다** — 동일성 물증으로 쓴 `screen_de_per_atom` 은
    **anneal 전** 값인데 축(BVS·G)은 anneal 뒤 `post_relax.xyz` 에서 계산된다.
    실측: 227 삼중쌍에서 anneal 전은 110개 일치, **anneal 후는 0개** (중앙 산포 6e-3).
    원인은 `run_anneal.py` 가 Langevin RNG·초기속도 seed 를 안 받는 것.
    ⇒ ρ 0.22·Jaccard 0.23–0.27 은 **파이프라인 재실행 불안정성**이지 metric 재현성이 아니다.
  - **P0-1** 39 target 이 합성 벡터다 (축마다 독립 중앙값 ⇒ 어느 실제 행에도 없다).
    이름을 구조 ID 로 쓰면 predictor(config A)와 D(config B)를 상관시킨다.
  - **P0-2** 집계식 불일치 — `median(3m+b) ≠ 3·median(m)+median(b)`.
    실측 **169/227** 설계가 다르다 (최대차 0.0696).
  - **P0-4** `|ρ|<0.2 ⇒ 축 근거 없음` **삭제**. n=39 에서 ρ̂=0 도 Fisher 95% ±0.31.
    ±0.2 동등성엔 n≥69 필요하고 39개는 독립도 아니다 (30 dopant·10여 구조환경).
  - **P0-5** tracer D 는 σ 게이트가 아니다 — σ비 = (n_Li 비)(D* 비)(H_R 비)이고
    Li 수가 host 24 대비 **18–28** 이다. Deng 7%/31% 는 표면코팅 pellet EIS 라 이식 불가.
    ⇒ 보고량을 **600 K 조건부 tracer D_rel** 로 한정하고 300 K σ·0.90 게이트는 **제거**.
  - **해제조건 8개** (회신 §실행 승인 해제조건) 를 다 채우기 전엔 안 던진다.
    파일럿도 39 밖 sentinel 이거나 blind 여야 한다 — rank-spaced 5×2 는 **격리 실패**.

**⛔ 아직 없는 것 (착수 전 필수)**
0. **재평가 잡음 원인** (위 🔴🔴) — 이게 먼저다.
1. **39설계 구조가 없다.** targets 는 이름·기술자만 있다 (`n_replicates: 15` = 배치 후보 수).
   host 2×2×2 + 39 도핑 셀을 만드는 빌더가 tools/ 에 없다 — `make_md_supercell.py` 확장 검토.
   ⚠ 배치는 `tools/doping/substitute_struct.py` 가 `np.random.default_rng(seed)` 로 만들어
   **시드 재현 가능**하지만 정본 CSV 에 `method` 열이 없다 — 어떤 method 로 만든 건지 모르면
   재생성 구조가 **점수를 매긴 그 구조라는 보장이 없다.**
2. **런처가 없다.** `run_lpsocl_md.sh` 계열은 계 하나짜리다. 39 × (host 1) 큐·중복가드·
   ledger 등재를 하는 캠페인 스크립트 필요.
⇒ "GPU 가 논다 = 바로 던진다" 가 **안 된다**. 던지기 전 준비가 하루치 있다.

### ⏭-3. 사전등록 채점 — **기준을 고치지 말 것**
`db/properties/prereg_d_rel_2026_08_28.json` 에 **라벨이 없는 상태에서** 순위를 얼려 뒀다
(예측기 `li_mobility_score`, 39설계 전부 채점 가능, CSV 해시 포함).
D_rel 이 들어오면 그 파일의 `성공기준_사전확정` **그대로** 채점한다:
- ~~주기준 `Spearman(predicted_rank, D_rel) < 0` 이고 `|ρ| ≥ 0.35 · p < 0.05`~~
  ⛔ **2026-09-08 비준 카드 §3 으로 교체** (`db/properties/cascade_d_rel_estimand_2026_09_08.json`,
  `D-2026-09-08-cascade-d-rel-estimand` active). 점추정 문턱 하나로 판정하지 않는다 —
  **ρ̂ + Fisher 95 % CI + 유효표본수**(환경 단위 블록 부트스트랩/cluster-robust)를 함께 보고한다.
  검정력 사전 고지: n=39 는 **진짜 ρ=0.35 여도 통과확률 약 50 %**, 80 % power 에는 ρ≈**0.47** 이 필요하다.
  ⚠ **이건 "측정 뒤에 기준을 고친 것" 이 아니다** — D_rel 은 **한 런도 돌지 않았고**(#3 미이행),
  카드가 *결과 보기 전* 시점에 비준됐다(status_history 가 순서의 증거). 바뀐 것은 **문턱이 아니라
  판정의 형태**이고, 예측기·순위 동결(`prereg_d_rel_2026_08_28.json`)은 그대로다.
- ~~실패 조건 `|ρ| < 0.2` ⇒ 이동도 축 근거 소멸~~ ⛔ **회신 AL P0-4 로 삭제** (2026-08-31 반영) — n=39 에서는 ρ̂=0 이어도 Fisher 95 % 구간이 ±0.31 이라 이 문턱이 '예측 못 한다' 를 뜻하지 못한다. 등가성을 주장하려면 n≥69 가 필요하다. ⚠ ⏭-2 에는 반영돼 있었는데 여기만 남아 같은 파일 안에서 충돌했다

⛔⛔ **측정 뒤에 기준을 고치면 이 기록의 의미가 통째로 사라진다.** 우리 acquisition 근거
(enrichment 1.22 p=0.43 · ordering 3.35)가 전부 retrospective 라서 만든 장치다 —
그걸 사후에 손보면 같은 자리로 돌아간다.

### ⏭-4. ⬇ **필요성 하 (2026-09-16 · 논문 방향 전환 — ⏭-NOW-k)** · Li₃Nd P0-2 control — **회신 I 가 "가장 급한 한 수" 라 한 것이 장부에 없었다** (2026-08-29 등록)
`kb/reviews/codex_I_reply_neb_hold_2026_08_27.md` §2 P0-2 · 실행순서 3 · §9-4 (L169/L318)
- **내용**: pristine 3×3×3 Li₃Nd 에 **대칭 끄고 rattle 2–3 시드 → 이완**.
  같은 Nd 재배열 패턴이 **공공 없이도** 나오면 ⇒ 원인은 공공이 아니라 **Fm-3m 셀 자체의
  q≈1/3 soft mode** 이고, 그때는 **끝점부터 다시**다 (MD 로 옮겨도 해결 안 됨 —
  같은 불안정 구조에서 낸 MD Ea 도 조건부 값이 된다).
- **왜 급한가**: cc333 3주 재개보다 **먼저**다. 회신 I 원문 — *"다음 한 수는 P0-2 control
  (pristine 3×3×3 rattle). 3주 재개보다 먼저다."* 3주를 던지기 전에 **끝점이 유효한지**를
  이게 가른다. 회신 I 표에도 `⏸ 미착수 — 이제 가장 급한 한 수` 로 적혀 있었다.
- 🔴 **까먹은 이유가 구조적이다**: 회신 I 안에만 있고 **이 파일에 항목이 없었다**
  (2026-08-27 → 08-29 사이 `grep "rattle\|pristine" kb/open_items.md` = 0건).
  리뷰 회신의 처방은 회신 파일에 두지 말고 **장부로 승격**해야 한다.
- **엔진**: cc333 relax 와 **같은 pw.x** 여야 한다. control 에 UMA 를 쓰면 방법이 바뀌어
  대조가 무의미해진다(재현시험 규율과 같은 함정). `tools/cascade/uma_relax_check.py` 에
  `rattle()` 이 이미 있으나 그건 UMA 경로 — DFT 쪽 rattle 생성기는 **없다**(신규 필요).
- **자원**: gabia A6000 유휴 + CPU 19코어 유휴. 돌고 있는 `nscf_gap`(modelc) 과 경합 없음.
- ⚠ **지금 돌고 있는 CPU 는 이게 아니다** — `pw.x -in nscf_gap.in`, cwd `/data/work/runs/gap_nscf/modelc`.
  P0-2 control 은 **한 번도 착수된 적이 없다.** (2026-08-29 시점 기록)
- ✅ **2026-08-30 착수 확인 — 지금 GPU 를 쓰고 있는 것이 이것이다.**
  `li3nd_mp-976264_p333_r0..r3` (rattle 시드 4). 실측: r0 ✓완료 `bfgs=0` ·
  E=−14652.03510974 · Fmax 1.6e-5 / r1 진행 `bfgs=13` · Fmax 0.0126 / r2·r3 대기.
  - ✅ **2026-08-31 갱신**: r1·r2 **진행**, **r3 미착수**.
    🔴 r1(−14652.03534)·r2(−14652.03576)가 r0(−14652.03511)보다 **낮다** ⇒
    r0 는 정지점이지 최소가 아니다. 다만 8.8 meV/108원자 = 0.08 meV/원자라 잡음과
    구별되지 않는다. ⇒ **결정적 관측량은 에너지가 아니라 Nd 변위 패턴이다** —
    r1~r3 가 서로 같은 방향인지, 그리고 공공(vacancy) 계산의 재배열과 같은지.
  GPU pw.x pid 4053765 · **37,736 MiB**.
  ⚠ r0 의 `bfgs=0` 은 이상이 아니다 — 무섭동 기준 구조라 처음부터 힘이 0 에 가깝다.
  ⚠ 화면의 **"van Hove 쓸이" 패널과 헷갈리지 말 것** — 그 캠페인은 08-28 에 끝났고
    GPU 를 잡은 것은 이 rattle control 이다 (2026-08-30 오판 사례).
  ⇒ 판정(같은 Nd 재배열이 공공 없이도 나오나)은 r1~r3 회수 후.

### ⏭-4b. ⬇ **필요성 하 (2026-09-16 — ⏭-NOW-k)** · li3nd 선행검사 체인이 **죽어 있다** — 화면이 이틀 감췄다 (2026-08-30 등록)
- **실측**: `pgrep -af run_prereq_chain` = **빈 출력**. 로그
  `/data/work/runs/prereq_chain_0828_0115.log` 마지막 쓰기 **08-28 02:20**.
  그런데 `watch_all.py` 화면은 08-30 까지 `🔄 진행 중` 이었다.
- **원인이 코드에 있었다**: `alive()` 가 문자열 `"-"` 를 냈고 **파이썬에서 `"-"` 는 참**이라
  그 절은 구조적으로 "안 돌고 있다" 를 낼 수 없었다. `elif not run` 가지(완주 판정·
  재기동 안내)는 **죽은 코드**였다. → 2026-08-30 수정(`Alive.__bool__`) + prereq 패널에
  로그 나이·GPU 3분기 진단 추가.
- **재기동** (⏭-4 의 rattle control 이 GPU 를 비운 뒤 — 리뷰 J5 는 동시 실행을 금지한다.
  여유 20,000 MiB 미만이면 스크립트가 알아서 기다린다):
  `nohup bash tools/sei/run_prereq_chain.sh --wait > /data/work/runs/chain3.log 2>&1 &`
- 🔴 **교훈**: 워처 출력은 **근거가 아니라 주장**이다. 판정에 쓰기 전에 실물
  (`pgrep` · 로그 mtime · `nvidia-smi`)로 받친다. 이번에 나도 화면만 보고
  "GPU 대기 중이니 죽일 필요 없다" 고 틀린 판독을 냈다.

### ⏭-5. 곁가지 (막히면 이것부터)
- **ESW 환원한계 규약** — `kb/questions/esw_reduction_limit_field_2026_08_28.md`.
  pymatgen 소스 확인은 끝났고(경계의 **아래쪽**을 집는다) 필드 분리 결정만 남았다. 정본 수치라 사람 확인 필요.
- **웹앱 서버 pull** — 2026-08-28 메모 UI(2열 배치·그림 첨부·코멘트 서식) 반영하려면 서버에서 pull.

---

### ⏭-6. 🟡 C-12 외주 VASP 번들 — **v41 발송 2026-09-11 (v40 교체·폐기 통지) · 보고자 회신 대기** (2026-08-31 신설 · 2026-09-11 갱신)

⚠ **이 캠페인이 장부에 한 번도 없었다.** Stage A(v2→v13)가 회신 AJ 이후 **C-12 로 개명**
되고 v14→v18 까지 갔는데, 리뷰 30라운드(N~AV)가 장부에 안 올라왔다. ⏭-4 가 적어 둔
교훈("리뷰 처방을 회신 파일에 두지 말고 장부로 승격")이 그대로 재발했다.

- **무엇을 재나**: LiNiO₂(104) 위 SDCP 단량체 vs perfluorodecane 조각의 **조각 간 대비 D**
  (사전 고정한 네 잡의 직접 대입). 개별 절대 흡착에너지는 보고하지 않는다.
- **지금 상태 (2026-09-11)**: **v41 발송** — v40 은 census `_hostpool` 버그로 보고자 쪽에서 시작 전에 멈췄고(잡 0개 실행), v41 은 같은 19잡·같은 입력(잡 폴더 바이트 동일)에 검사 스크립트만 고친 판. 상세는 ⏭-NOW '오늘 닫힌 것'. ⚠ 아래 v18 시점 서술은 이력이다.
- **(이력 2026-08-31) 지금 상태**: `sdcp_c12_v18` 봉인 완료 · **VASP 한 잡도 안 돌았다.**
  회신 AV = NO-GO (P0 4건 · P1 1건).
- **2026-08-31 이행 완료**: P0-1 `895af2ed` · P0-2 `1b3fbefc` · P0-3 `d29c322e` ·
  P0-4 `4aed52ff` · P1-5+해제조건⑦ `290513d3`,`ddc6d7ca`.
  해제조건 ①~⑦ 닫힘.
- ✅ **해제조건 ⑧ 닫힘 (2026-09-01)** — gabia 에서 v19 재생성 완료. v18 argv 를 `--out` 만
  바꿔 그대로 썼다. ZIP `c423b082…` · MANIFEST `6d8dd2f4…` · 커밋 `3817eb5d` · **git_dirty false**
  (v18 은 true 였다). verify_zip PASS(rc 0 · 해시확인 110/110) · 배포본 selftest **294/294**
  (v18 274) · 보고량 판정 검사 94건(v18 87) · 비UTF8 로케일 PASS.
  기록: `runs/sdcp_c12_2026_08_30/IDENTITY_v19.json` · 리뷰 **AY** 발송 대기.
- ✅ **회신 AY = NO-GO (P0 5건) → 전건 이행 · v20 재생성 (2026-09-01)**
  ZIP `e0fb9e14…` · MANIFEST `e1b935e6…` · 커밋 `1d03cae9` · 배포본 selftest
  **300/300**(v19 294 · v18 274). 잡은 16개 그대로 — 계산은 안 늘렸다.
  P0-1 이 핵심: AV 판이 launcher 우회를 **닫은 게 아니라 미룬 것**이었다
  (러너가 PATH 에서 mpirun 을 찾았다). 이제 봉인된 절대경로 + 상별 재해시 +
  영수증 8열 대조. P0-2 는 고치는 대신 **주장을 내렸다**(토큰은 소유권 증명이
  아니다). 보고량 이름은 1저자 결정으로 **E_ads**, 단서는 Methods 가 진다.
  기록: `runs/sdcp_c12_2026_08_30/IDENTITY_v20.json` · 리뷰 **AZ** 발송 대기.
- 🔴 **거버넌스 간선이 아직 안 닫혔다** — `D-2026-08-30-sdcp-c12-path` 가
  proposed 인데 전역 마감정책을 supersede 한다. 회신 AW P0-3 이 불허 판정.
  AZ Q5 로 '발송을 막는가' 를 물어 두었다.
- ⛔ **v18 을 돌리지 않는다.** 계산 추가는 필요 없다 — analyzer·runner·반송계약 수정과
  재생성만이다 (회신 AV Q6).
- ⚠ **잡 수의 정본은 MANIFEST/IDENTITY_v18(16잡)** 이다.
  `sdcp_c12_protocol_2026_08_30.json` 은 12·19 로 적고 있어 낡았다 (citation_hazards 등재됨).
- ⚠ **보고량 이름의 정본은 `sdcp_c12_claim_prereg_2026_08_31.json`** 이다. 프로토콜 §1 은
  "adsorption energy" 라 부르는데 claim prereg 가 그것을 금지어로 지정했다 — 번들에
  모순되는 사전등록 둘이 달려 있다.
- 🔴 **거버넌스 미등록**: C-12 보고량이 `db/governance/decisions.json` 에 없다
  (`grep -c c12` = 0). 세 사전등록 파일이 전부 "proposed — 사람이 ratify" 라 적었지만
  등록 자체가 안 됐다. CLAUDE.md 규율 위반.

### ⏭-7. 폴라론 S0 (ORCA) — 🔴 **회신 V = NO-GO · P0 5건** (2026-09-02 갱신)

- **회신 U (2026-09-01) = NO-GO — phase L 도 돌리지 말 것.**
  기록: `kb/reviews/codex_U_reply_polaron_S0_2026_09_01.md`. 리뷰어가 **직접 빌더를
  돌려 재현**했다 (UTF-8 selftest 152건 PASS · 생성 정상 확인).
- 🔴 **P0 아홉 중 둘이 같은 유형 — 합성 fixture 가 실물과 달라 결함을 숨겼다.**
  · π 판정식이 **좌표축 의존** — 이상적 p_normal 을 넣어도 0.34–0.67 이라 문턱 0.60 이면
    **완전한 π 궤도도 5/6 탈락**. 우리 fixture 가 축 정렬이라 안 보였다.
  · spin parser 가 `0 C:` 콜론을 강제 — 실제 ORCA 6.1 출력엔 콜론이 없다. fixture 가
    인위적으로 콜론을 넣어 가렸다.
  ⇒ **selftest 152건이 전부 통과한 채로** 그랬다. 이 캠페인의 fixture 는 **실물 ORCA
    출력 조각**이어야 한다.
- 나머지 P0: `%loc Randomize 0` → 공식 키는 **`Random 0`** · localized MO 에너지로
  core 거르기 불가(ORCA 가 orbital energy 없다고 명시) · 분석기에 **`ADEQUATE` 경로
  자체가 없음**(폐기한 전체-pilot verdict 를 냄) · basin 수가 **job 이름 순서**에 따라
  1 또는 2 + 전역 α↔β 반전을 다른 상태로 세어 `basin ≥2` 를 **거짓 충족** 가능 ·
  restart 가 에너지를 원래 불안정 출력에서 계속 읽음 · 미관측 positive control 을
  `NO_VALUE` 가 아니라 방법 실패로 바꿈 · 생성물이 S0 사전등록이 아니라 **구판**을 가리킴.
- ✅ **P0 9건 전건 이행 (2026-09-01, `35eb8a9f`) — selftest 152 → 195.**
  · π 는 **MO 계수**로 3×3 `P = Σ vvᵀ` → `n̂ᵀPn̂/tr P` (회전불변, 이상적 π 에서 정확히 1).
    계수 없으면 통과 불가, Cauchy–Schwarz 상한으로 **기각만** 한다.
    신설 시험이 **종전 식이 0.335 로 무너지는 것**을 같은 자리에서 재현해 기록한다.
  · fixture 를 각 블록의 **공식 ORCA 형식**으로 (Loewdin `0 C :` · Hirshfeld 콜론 없음).
  · `Random 0` + `OCC/VIRT/T_CORE` 명시 · 코어는 **국재화 전 canonical 창** + AO 성격.
  · S0 전용 판정: `ADEQUATE` 신설, 최저 에너지 경로 **삭제**, basin 1개면 막는다.
  · basin 군집: 완전연결 + 추이성 검사(`CLUSTER_AMBIGUOUS`) · 게이트 행 제외 ·
    `Σ|s|` 정규화 · 전역 α↔β 정준화 · 링 면제 해는 링 축도 제외.
  · 게이트/결측이 positive control **앞**에 온다 (결측 = `NO_VALUE`).
  · manifest 가 S0 prereg + 그 해시를 봉인하고 러너가 `$BUILDER` 해시를 대조.
    S0 사전등록을 **재발행**했다 (`status_history` 가 순서의 증거).
  · 러너에 `loccheck` 단계 — H₂O 하나로 `%loc` 구문·`.loc` suffix·인쇄 블록 30초 확인.
- 🔴 **아직 안 한 것**: 실물 ORCA 확인 0회 · Q3 `localized_no_rotation` control ·
  `RING_ASSIGNMENT_UNRESOLVED` · `S0_EPS1_ANION_REFERENCE_INADEQUATE` · R0/R1 교차비교.
- 🔴 **회신 V (2026-09-02) = NO-GO · P0 5건.** "P0 9건 전부 이행" 이 실물과 달랐다.
  · **P0-1 은 우리 절차 오류**였다 — 리뷰 V 에 적은 사전등록 해시는 **작업 트리** 것이고
    같이 적은 커밋에는 그 변경이 없었다. 리뷰어가 그 커밋을 받아 옛 파일을 봤다.
    ⇒ `tools/review_manifest.py` 신설: `git show <commit>:<path>` 로만 해시를 계산하고
      **작업 트리를 안 본다.** dirty 거부 · 없는 경로 거부 · `--require_pushed` 로
      원격 포함 확인. selftest 9(음성 4).
  · P0-2 사전등록을 **파일 해시만** 결박했다 → builder·parent·atom_manifest·functional·
    ε·realization·status 를 파싱해 fail-closed 교차검증 (음성 8). 리뷰어 반례
    (미이완 start.xyz)가 시험으로 들어갔다.
  · P0-3 `loccheck → L` 이 문구였다 → `LOCCHECK_PASS.json` 증서를 L·seeds 가 **강제**.
    ORCA 6.1 문서의 **`.loc.gbw`** 도 지원 (L2 가 증서 suffix 로 `%moinp` 를 고친다).
  · P0-4 추이성 검사가 불완전 → **연결성분마다 clique 검사** (반례 재현·수정 확인).
  · P0-5 restart 가 **미완결 출력을 대표로 승격** → 판정 segment 에서 정상종료 요구.
  · Q1 π 를 `pi_orientation_score` 로 제한 · Q2 상한 기각 경로 폐기 ·
    Q6-1 `S0_EPS1_ANION_REFERENCE_INADEQUATE` 기준을 결과 보기 전에 봉인.
  selftest 195 → **212**.
- 🔴 **비준 두 건이 phase L 을 막는다** (사람 몫): S0 사전등록 · 전역 마감정책.
- 🔴 **아직 안 한 것**: Q6-2 `localized_no_rotation` control · Q6-3
  `RING_ASSIGNMENT_UNRESOLVED` · Q6-4 R0/R1 교차비교 · 실물 ORCA 확인 0회.
- ▶ **다음 한 수**: 리뷰 W 발송 (`kb/reviews/codex_W_prompt_polaron_S0_2026_09_02.md`).
  ⚠ phase L 에는 `Rotate` 가 없으므로 L 성공을 Rotate 검증으로 쓰지 않는다.

⚠ 이것도 장부에 없었다.

- **무엇을 묻나**: 자가도핑 SDCP 의 H-제거 n=6 라디칼에서 스핀이 백본에 있나 술폰산에 있나
  (`F_bb` / `F_SO3` / `F_other`). ε=1 적합성 pilot **한정**이다.
- **상태**: `bundles/sdcp_polaron_S0_inputs.zip` gabia `/data/work/runs/sdcp_polaron_S0` 에
  생성 완료, **코어 대기**. ORCA 실행 32회 예정 (측정 16 + probe 13 + L 2 + L2 2), Opt 없음.
- 사전등록 2건 등록됨: `sdcp_polaron_pilot_prereg_2026_08_31.json` ·
  `..._prereg_S0_2026_08_31.json`. 거버넌스 결정 2건 **proposed**
  (`D-2026-08-31-sdcp-polaron-Fbb` · `...-S0-four-layer`) — 사람이 ratify 해야 active.
- ▶ 리뷰 U 발송 대기 (`kb/reviews/codex_U_prompt_polaron_S0_2026_08_31.md`).
- ⚠ **실물 ORCA 미검증** — `%loc` 출력 형식 · `Rotate` 동작 · `NoIter` probe 가 스핀
  인구를 찍는지 전부 모른다. phase L 첫 실행이 곧 smoke test 다.
- ⚠ 이 세션에서 생성기·seed 생성기·분석기가 **셋 다 예외로 죽어 있었는데 selftest 40건이
  전부 통과**했다 (`689bc1dc`·`cf88fb9c`). 함수를 부르지 않는 시험은 그 함수가 죽었는지 모른다.

#### ⏭-NOW-c. 같은 날 **밤 최종** (2026-09-13 22:00 · 위 ⏭-NOW-b 보다 이게 최신)

> 10스윕이 끝났고, **골짜기 질문의 답이 처음 나왔다.** 지금 막고 있는 것은 **1저자의 종료 문구 결정** 하나다.

**⏭ 바로 다음 (순서대로)**
1. **BQ-4 발송** — `kb/reviews/codex_BQ4_prompt_10sweep_basin_2026_09_13.md` (작성 완료, 대상 커밋 `c8dbf3a82`).
   묻는 것 넷: P1-a/P1-b 해제 · 힘 문턱 결론 · **내가 쓰려는 골짜기 문단의 허용 범위** · §4b 최종 판정.
2. **종료 문구 결정 (1저자)** — 두 조건 다 `all_five: false` 라 *"준비 확보"* 는 닫혔다.
   남은 것은 *"정한 준비법·비용 안에서 v4 파일럿 준비 미확보"* 하나. ⛔ 내가 고르지 않는다.
3. 결정 뒤 **마감 기록** `db/properties/cascade_pilot_4b_closed_2026_09_13.json`
   (확정값 · 허용 서술 · 금지 서술 · **재개 조건**). 재개 조건은 BQ-4 Q6 의 답을 받아 쓴다.
4. (선택) 골짜기 표를 webapp §4b 화면에 결속 — 숫자는 레지스트리에서만, 음성시험 표면 목록에도 추가.

**★ 10스윕 결과 (`ALLDONE 20:03:42`, 5구조 × 2조건)**
- **W3_f02 1/5 · W3_f005 1/5 — 둘 다 `all_five: false`.** 자격은 질서 H0 뿐.
- **답: 힘 문턱을 4배(0.02→0.005) 조여도 준비 상태가 안 바뀐다.** BQ-3 이 설계한 질문의 답이다.
- 막는 것은 **전부 이력현상**이다 — 10줄 전부 상승 7/7 **및** 하강 7/7 수렴. 수렴 문제가 아니다.
  적합 품질도 아니다: `W3_f005 P1_Al2O3_B` 는 **r²=0.999999 인데 차단**됐다.
- 모양 기준이 실제로 일한다: `W3_f02 P1_A`(V₀차 0.997 %)·`P2_B`(0.977 %)는 V₀ 기준만 보면 통과인데
  shape 17 %·25 % 로 잡혔다. BQ-2 Q2 분해가 없었으면 자격을 받았을 줄이다.
- H0 두 조건: V₀ 4066.4 vs 4065.3 (**0.029 %**) · B₀ 26.2/27.2 · **B₀′ 4.18 vs 6.43 (54 %)**.
  ⚠ 이번 라운드는 창이 하나뿐이라 BQ-3 의 *"f005 면 창과 무관"* 을 **재확인 못 한다**.
- ⚠ 25줄 대비 **W3_f02 자격 3/5 → 1/5.** 창은 같다(0.97…1.03 7점). 후보 원인은
  `--fixed_shape_relax` 하나로 좁혀지지만 **A/B 를 안 돌렸다 — 분리 안 됨** (BQ-4 Q2).

**★ 골짜기 비교 — BQ-2 Q1·Q3 가 요구했고 25줄로는 못 했던 것**
`db/properties/cascade_pilot_4b_basin_2026_09_13.json` (**citable: false**) · 140 프레임 전수.
- 질서 H0: 두 조건 모두 **7/7 점 이웃 집합 동일**, 0.1 Å 넘게 움직인 Li **0 개**.
- 무질서 넷: 두 조건 모두 **7/7 점 이웃 집합 변화**, 56 점에 걸쳐 90 개 중 **15–45 개**가 이웃을 바꿈.
- **움직이는 것은 Li 다** — 70 점 중 66 점에서 최대변위 원자가 Li (나머지 4 는 전부 H0 이고 ≤0.010 Å 잡음).
  무질서 56 점은 **전부** Li. RMSD(Li)/RMSD(골격) = 2.7–4.5 배.
- 자기검사: 프레임에서 다시 센 이력현상 벡터 20 개가 기록값과 **최대차 0.0 eV**.
- ⛔ **판정 아님.** `neighbor_sets_changed` 는 사실 진술이지 *"다른 골짜기"* 가 아니다 —
  BQ-3 Q5-3 이 RMSD 문턱을 불승인했고 끝점 두 장은 중간 경로를 증명 못 한다.
  골격도 0.115–0.198 Å 움직였다(0 이 아니다).

**⚠ 내가 먼저 신고한 약점 (BQ-4 §6)**
- **`n_steps = 0` 승계 검사가 실패할 수 없는 형태였다** — 자격 통과한 H0 두 줄 모두 V₀ 적용 후
  완화가 0 스텝이라 `4_displacement_vs_scaled_start` 가 *스케일 출발점을 자기 자신과* 비교했다
  (rmsd 0.0 · identical). **이 통과는 증거가 아니다.** 최종힘도 문턱 바로 밑(0.004619/0.005 = 92 %).
- `--fixed_shape_relax` 원인 미분리 · 끝점 비교의 한계.

**도구** `run_mlip_postproc.py` selftest **141 → 153** (`--pair_frames` 추가 — 새 파일 대신 기존 도구 확장).
새 검사 12건 전부 **대상을 일부러 깨서 빨간불 확인**(9종 고장). 그 과정에서 **내가 쓴 시험 하나가
임시폴더를 앞선 시험과 공유해 엉뚱한 것을 재고 있었다** — 양성 검사는 그대로 통과했다.


#### ⏭-NOW-d. 같은 날 **심야 최종** (2026-09-13 23:30 · 위 ⏭-NOW-c 보다 이게 최신)

> **회신 BQ-4 종결 GO.** *"§4b 를 충족해서 해제하는 것이 아니라 이번 준비 라운드를 미확보로 종결하는 것."*
> MD·탄성 진입 NO-GO 유지 · 추가 계산은 종결 조건 아님. 지금 막고 있는 것은 **1저자 비준 하나**다.

**⏭ 바로 다음 (순서대로)**
0. ~~BQ-5 발송~~ → **회신됨: E′ 방향 GO · 카드 NO-GO 세 묶음** → **카드 v5.1 로 닫음** (집계식 기하평균·로그·구간 위치 판정 · β 경보 강등·골격 경보·홉 도구 규약 · 비용 상한 '첫 계산 전 비준' 절차 + 실패 전파 7). BQ-6 회신: ①③ 해제 · **② 미해제** (run_verdict 에 부창 검사 없음 · MSD/d² 는 홉 수 아님 · 골격 경보 범위) → **v5.2**: `msd_diffusive_check.aggregation_eligible` 신설(리뷰어 합성 사례 2건을 selftest 로) · MSD 대용값 경보 강등 · 사건 게이트 유지 · `framework_alarm` 범위 명시. **남은 것 = 1저자 숫자 두 개** (성능 시험 소상한 · 총상한, 제안 10/120 GPU-h) + 비준 (+ 선택 BQ-7 로 ② 닫힘 확인). 원래 항목: 카드 `db/properties/cascade_rebuild_estimand_card_v5_Eprime_2026_09_13.json` · 결정 `D-2026-09-13-cascade-pilot-estimand-v5-eprime` (proposed, v4 supersede 예정). **계산 0건.** 회신 → 1저자 비준 → 비용 상한 GPU-h 기입 → 실행 스크립트(상수 동결) → 직접 완화 5 + MD ≤30. ⛔ 이건 여전히 **파일럿**(UMA 내부 진단)이지 본 cascade 가 아니다.
1. ~~1저자 비준~~ → **✅ 비준 2026-09-13** (지시 '1번 해결', 리뷰어 문구 그대로). 카드 `closed: true` · 결정 active(digest 결속) · validate_canonical ✅. 원래 항목: `db/properties/cascade_pilot_4b_closed_2026_09_13.json` 의
   `종료_문구.proposed_value_from_BQ4` 를 `value` 로 승인(또는 수정). 승인되면
   결정 원장 `D-2026-09-13-cascade-pilot-4b-cell-policy-closure` 를 active 로 올리고 카드 `closed: true`.
   ⛔ 에이전트가 고르지 않는다. ⛔ `closed: false` 인 채로 active 로 올리면 `validate_canonical` 이 거부한다(배선됨).
2. H0 최종 파일(`final_v0_applied.xyz`)을 **쓸 때** V100 에서 회수해 기록의 `final_sha256` 과 대조 (리뷰어 Q1 — 파일 자체는 미대조).
3. ~~litdb 백로그 36건~~ → **INDEX.md 병합 완료 (2026-09-13 심야)**: `_pending_index_*.md` 30건 중 28건의 ① 행을 `INDEX.md` 에 옮김(Digest 완료 23 · MLIP 방법론 5, 4열 행 3건은 3·4열을 합쳐 3열로 — 내용 손실 없음) + ren2026 3차 패스 문단 삽입. `build_index.py --check` 33 → **5** (pranami2015 는 ① 이 INDEX 행이 아니라 comparison 블록이라 행 없음 · 나머지 4 는 `_INDEX_proposals.md` 의 뼈대 — 실물 대기, 등재 안 하는 게 맞다).
   ✅ **②③ 도 병합 완료 (2026-09-13 심야, 지시 '2,3번도 같이')** — `comparison_vs_ours.md` 2053 → 3861 줄. Reference key +10 · J-0 +8 · §A 행 +14 & 끝 블록 6 · §B +4 · §C 블록 2 · §D 1 · §F +2 · §H +3 · **J-7 +21 항목** · J-9c–f 4 소절 · J9-e′ 개정 행(원문 보존) · 신설 **J-12…J-19** 8 절.
   번호 충돌은 §J 머리의 📎 배정표대로 풀었다 (초안 J-11/J-12/J-13 → J-12…J-17, UQ 축 J-18, GB 축 J-19; J-9c ×4 → c·d·e·f 슬러그순). `--check` comparison 미편입 33 → **4**(뼈대).
   ⏳ **미처리 = ④ 이후 항목**: properties/·db/ 갱신 4건(liu_finetuning·maginn·ou·wilson — **db 규율상 원장 경로로만**), talk 역링크 초안 2건, 도구 버그 보고 2건(aqib ⑤ pdf_text 파일명 충돌 · basu ⑤ extract_figures), inbox 확보 후보(zaby·muy·he·zhao), jang ② Reference key 행(표 형식 아님), pranami ① INDEX 행. 각 pending 파일 2행 참조.
4. (선택) 골짜기 표 webapp 결속 — 웹앱은 **로컬 전용**이다 (2026-08-07 `79fd69503` 클라우드 배포 폐지 · `dem-analyzer.onrender.com` 은 그때도 `/` 404). 우리 브랜치의 `render.yaml` 은 죽은 배포를 가리키는 잔재 — 지울지 1저자 결정.
5. **주간 정리 화면 신설 (2026-09-14)** — `/weekly`(작업 기록 하위) ← `kb/reports/weekly_2026_09_14.md` (9/7~9/13 을 슬라이드 양식으로: 섹션 → ■ 결과 → • 근거 → 그림). 그림 2장 신규 `tools/figures/fig_weekly_2026_09_14.py`(selftest 8/8): LPSOCl 3×3×1 아레니우스 · §4b E(V) 이력 5패널(진단). ⚠ 이번 주 **확정값은 LPSOCl Ea 하나** — 나머지 진단값은 `citable: false` 로 적었다. 다음 주는 새 파일 `weekly_<날짜>.md` 를 만들면 화면이 최신을 집는다. ⏳ V100: **재대여 확인(2026-09-14 새 pem `Tesla_V100_20260914_101429.pem`, 옛 컨테이너 소멸)** → 재설정(UMA env cu126 · 체크포인트 해시 · repo sparse) — QE 는 다시 안 세운다(다음 잡은 UMA 만). ⛔ 옛 컨테이너의 H0 `final_v0_applied.xyz`(항목 2)는 repo 에 없어 **회수 불가** — E′ 는 새로 완화하므로 영향 없음.
6. ✅ **E′ 카드 v5.2 비준 (2026-09-14, 지시 "비준 비준 비준")** — 비용 상한 **10 / 120 GPU-h** 확정 · 카드 `ratified` · 결정 `D-2026-09-13-cascade-pilot-estimand-v5-eprime` **active** · v4 `superseded`. `prereg_ratify.py` 로 도장, `validate_canonical` ✅. ⚠ agent 대필(전문 축자검토 기록 없음). ⇒ **실행을 막는 것은 이제 없다.** 다음: 실행 스크립트(상수 동결: V 4066.479695 Å³ · 원본 셀 행렬 · fmax 0.02 · 창 2–50 ps) → 직접 완화 5 → **첫 H0 600 K 속도 시험(소상한 10 GPU-h)** → 남은 29 런. 선행 조건은 V100 환경 검증(sm_70 · 체크포인트 07068e9c… · HEAD).

**★ 회신 BQ-4 가 깎은 내 서술 여섯** (`cascade_pilot_4b_blocked_2026_09_13.json` → `⛔⛔⛔_회신BQ4`)
"모양 기준이 없었으면 통과했을 두 줄"(거짓 — B₀′ −55.94·−27.51 로도 막힘) · "차단은 전부 이력현상"(6줄 B₀′·1줄 r² 도 실패) ·
"힘 문턱은 준비 상태를 바꾸지 않는다"(분류만 같음) · "같은 창"(실제 부피점 다름) · "0스텝이라 수렴 의심"(수렴 유효) ·
"끝점으로 때우지 않는다"(함수는 맞고 **호출부**가 때움). **첫째가 제일 비쌌다 — 상위 사유가 다른 실패를 가리는 구조를 내가 믿었다.**

**같은 날 고침** (selftest 161 · 러너 13 · 6종 고장 전부 빨간불 확인): `_compose_reason`(사유 전부 잇기, 라이브·regate 공용) ·
승계 호출부 끝점 대체 → 차단 · `prepared()`(EOS 자격 ∧ 적용 ∧ 수렴 ∧ 최종 파일) · 0스텝 `zero_update` 꼬리표 ·
`validate_governance` 뼈대 마감 카드 게이트. 원자료 10줄 재판정: 판정 0 · 자격 0 · **사유 6 변경**(가림 해제,
`regate_reason_unmasked_d0a0ba115.json`). 새 집계로도 1/5 · 1/5.

**허용 서술은 카드의 `허용_서술_이대로만_쓴다` 만** — 특히 '움직이는 것은 Li 다' 대신
*'최대 상대변위는 Li 에 나타났고, 골격에도 차이가 남았다'*, '끝점' 대신 *'각 부피점에서 얻은 두 완화 종료 구조'*.


## 🔴 판정 대기

### 1. 🔴 modelc MD Ea 정본 — **닫는 방법이 무효화됐다 (2026-08-01)**

> ⛔ **β=0.8 하드게이트는 2026-08-26/27 폐기됐다** (`kb/concepts/beta-gate.md` §7-5·§7-8b, 회신 F). 아래 '게이트 통과/실패' 문구는 **경보값**으로만 읽는다. 판정축은 자유절편 (c, m) · 홉 수 · 다중 창이고, 도구는 2026-08-30 에 교체됐다(§7-8e). ⚠ **양방향이다** — 문턱을 내리면 '다 통과' 가 아니라 **통과했던 것도 무효**다(§7-6). (2026-08-31 전수 조사에서 붙임)
- **원래 계획**: comp1 멀티시드 보강 → 전 조성 3-seed 통일 → modelc 0.197±0.032 정본 확정.
- **실행함**: kgy 에서 comp1 seed 2/3 완주(6런). 3-seed Ea = 0.2681 ± 0.0576 까지 나왔다.
- **⛔ 그런데 그 값을 쓸 수 없다.** 확산영역 게이트에서 **6/6 전부 케이지**로 판정됐다
  (β 0.17–0.79). 창을 2-50 → 100-200 으로 옮겨도, 시드 MSD 를 평균해도 β 가 0.8 을
  못 넘는다. s3 의 `D(600) 1.36e-06 ≈ D(800) 1.37e-06`(비 1.007) 이 그 증상이었다.
- **따라서 #1 은 '시드를 더 돌면 닫히는' 항목이 아니다.** 저이동도 계에서 200 ps 가
  부족한 게 근본 원인이라, **셀 확대(2×2×2, Li 24→192) 또는 시간 연장** 후에야 닫힌다.
- ~~⚠ 비교 상대인 modelc 0.197±0.032 · b2o3 · LPSOCl 도 **같은 프로토콜**이다(미검사).~~
  → **2026-08-04 일부 판정**: LPSOCl 첫 게이트 검사 — **600 K 이 4시드 앙상블 평균에서
  탈락** (β 0.61, MSD 는 97 Å²@200 ps 로 충분 = 홉 통계 문제; 시드별 0.52~0.98 갈림).
  800 K 0.86 / 1000 K 1.02 통과. → **Ea 0.287±0.024 는 케이지 오염된 600 K 점을 포함** —
  재검토 필요 (paper_first_author_requests_2026_08.md §4 의 선택지 3안).
  **modelc·b2o3 3시드 평균 검사 완료 (v2)**: modelc 0.87/0.93/0.92 · b2o3 0.81/0.83/0.97
  전부 통과 — 단일시드 '아슬' 해소. b2o3 600 K 3시드 D 가 등록 D_600_mean 을 재현(1.039 vs
  1.041e-5). **잔여 이슈는 LPSOCl 600 K 하나** — 30런(lpsocl 600 재실행 포함, 2026-08-04 결정) MTO-β 로 1차 판정, 안 되면 1600 ps 프로브.
  게이트 통과 전까지 전부 인용 보류.
- 근거: `kb/results/mlip_md_diffusive_gate_2026_08_01.md` ·
  `tools/ionic/msd_diffusive_check.py`

#### ⏱ **1600 ps 연장 판정 (2026-08-06) — 시간으로는 안 닫힌다**

`comp1_seeds_p1600` (s2 단일시드, prod 200 → **1600 ps**, 8배). 같은 게이트로 재판정:

| T | 200 ps β | **1600 ps β** | D 변화 | 판정 |
|---|---|---|---|---|
| 600 K | 0.64 | **0.37** | 3.44e-06 → 2.37e-06 (−31 %) | ⛔ **더 나빠졌다** |
| 800 K | 0.31 | **0.61** | 5.20e-06 → 1.04e-05 (+100 %) | ⛔ 크게 올랐지만 미달 |
| 1000 K | 0.69 | **0.97** | 2.11e-05 → 3.78e-05 (+79 %) | ✅ **처음 통과** |

**① 200 ps 값들은 자기 오차막대보다 더 틀려 있었다.** 같은 시드에서 Ea 0.2194 → **0.3526**,
**Δ +0.1331 eV = 3-시드 산포(±0.0576)의 2.3배**. 게이트 규율이 사후로 정당화됐다 —
"숫자가 모였다"와 "인용 가능하다"는 다른 사건이라는 것의 실측 사례다.

**② 창 재적합도 구제가 아니다** (`tools/ionic/msd_refit_window.py --policy both`,
산출 `db/properties/msd_window_scan_comp1_p1600.csv`):
- **600 K = 어떤 창에서도 β∈[0.8,1.2] 창이 없다.** 도구가 `없음` 을 반환 = 확산 영역 부재.
- 800 K 는 창 `1–1600` 에서 β 0.81 이 나오지만 **하한 1 ps 는 ballistic 을 포함**하고
  D 가 **0.59×** 로 떨어진다 → 확산영역을 찾은 게 아니라 억지로 맞춘 것.
- ⚠ **1000 K 의 β-선택창 `없음` 을 실격으로 읽지 말 것** — 그 정책은 **끝점을 1600 ps 에
  고정**하고 시작점만 찾으므로 "꼬리 전체를 포함한 창에서는 안 된다"는 뜻이다.
  규약 창(2–50)의 β 0.97 을 뒤집지 않는다. 꼬리가 지저분한 원인은 **단일 시간원점**이다.

**③ MTO 로도 못 고친다.** `run_comp1_seeds.sh` 는 프레임을 안 남겨 소급 적용이 불가하고,
설령 켜도 MTO 는 β **추정의 산포**를 줄이는 장치지 β **중앙값 0.37** 을 올리지 못한다.
0.37 은 통계 흔들림이 아니라 **진짜 케이지**다.

> **→ 결론: 남은 수는 셀 확대뿐이다.** 62원자 셀에 Li 27개가 근본 원인이고,
> 시간(8배)으로는 1000 K 한 점만 건졌다. **현재 comp1 에는 인용 가능한 Ea 가 없다.**
> 1000 K 단일 점으로는 아레니우스가 성립하지 않는다.

#### 📉 파급 — 6점 아레니우스 500 K 레그를 뒤로 미뤘다 (2026-08-06)

600 K 를 1600 ps 로도 못 뚫었는데 계획의 **500 K 는 100 K 더 낮고 prod 는 1/4(400 ps)** 였다.
`chain_after_c1long.sh` 사슬을 끊고 **700/900 K 선행판**으로 바꿨다
(`TEMP_PROD="700:200 900:200"`, 18런 + lpsocl 600 재실행 3런 ≈ 1일):

- 대상(modelc·lpsocl·b2o3)은 comp1 보다 빠르고, **신규 런은 MTO 를 갖는다** → 700/900 이
  **MTO 효과의 첫 실측**이 된다.
- 그 β 로 **500 K 필요 prod 를 실측 기반으로 정한 뒤** 500 K 를 건다.
  **6점을 포기한 게 아니라 순서를 바꾼 것.**
- ⚠ 부수 검증: `md_temperature_feasibility.py` 가 500 K 필요량을 modelc 103 / b2o3 104 ps 로
  본다. comp1 실측(1000 K 200 ps 조차 탈락)과 나란히 두면 **그 추정이 낙관적일 수 있다** —
  700/900 결과가 이 도구의 검산도 겸한다.

### 2. 🟡 comp2 disorder ensemble — **d=0.5 판정 완료 / d=1.0 측정 실패 (2026-08-01)**

> ⛔ **β=0.8 하드게이트는 2026-08-26/27 폐기됐다** (`kb/concepts/beta-gate.md` §7-5·§7-8b, 회신 F). 아래 '게이트 통과/실패' 문구는 **경보값**으로만 읽는다. 판정축은 자유절편 (c, m) · 홉 수 · 다중 창이고, 도구는 2026-08-30 에 교체됐다(§7-8e). ⚠ **양방향이다** — 문턱을 내리면 '다 통과' 가 아니라 **통과했던 것도 무효**다(§7-6). (2026-08-31 전수 조사에서 붙임)
- **d=0.50 ✅ 인용 가능**: Ea **0.151 ± 0.068 eV** (config 3개). 확산영역 게이트를
  개별 9/9(β 0.81–1.12) + 온도별 평균 3/3(β 0.92/1.00/0.97) 로 **완전히 통과**.
  MSD 45–280 Å² 로 통계도 충분하다.
  ⚠ 다만 **config 산포가 45%** 다 — "ordered(0.276)보다 낮다"까지만 말하고
  값 자체를 정밀 인용하지 말 것. cfg0 의 0.087 은 아티팩트가 아니라 **실제 산포**였다.
- **d=1.00 ⛔ 측정 실패**: 개별 8/9 케이지(β 0.11–0.93), 평균도 0.27/0.46/0.78.
  겉보기 Ea 0.378 은 케이지 진동을 맞춘 값이라 의미가 없다.
  → **"disorder 를 더 늘리면 Ea 가 다시 오른다"는 비단조성을 주장하면 안 된다.**
- **남은 것**: d=1.0 을 셀 확대/시간 연장으로 다시 재야 추세(0 → 0.5 → 1.0)가 완성된다.
- 등록: `db/properties/comp2_disorder_ensemble.json`

### 3. ~~VGCF 2×2 barrier 행렬 + 기전 판정~~ → ✅ **완료 (2026-07-30)** — 본문은 `## ✅ 닫힌 항목` 절. 요지: 209 meV 는 거의 전부 VGCF 쪽이고 기전은 **confinement**.

### 4. SDCP complex_doped_v2 DFT relax — k 2×2×1 재실행 수렴 여부
- k 1×1×1 정체(150 iter, 0.0837 Ry) → 2×2×1로 재시작. accuracy가 0.08을 뚫고
  내려가는지 확인 필요. VRAM 46.9/48 GB로 임계 (OOM 시 diago_david_ndim=2).
- ⛔ **"메모리 큰 다른 기계로 옮기면 되지 않나" 는 아니다 (2026-08-19 재확인).**
  `sbatch_phaseB_v3_kisti.sh` 헤더가 이미 진단해 뒀다 — 226원자 스핀분극 DFT+U 는
  ecutrho 를 내려도 안 된다(파동함수·Davidson 배열은 ecutwfc·nbnd 로 정해짐, 그것만
  30 GB 대). 해법은 **더 큰 메모리 한 장이 아니라 G-벡터를 여러 랭크로 분산**
  (`mpirun -np 4 ... -nk 1` → 랭크당 1/4). 옛 `run_stream <gpu>` 판이 처리량만 늘리고
  메모리는 그대로였던 것과 같은 함정이다.
  · kgy 실측(2026-08-19): available **32 GB**(total 62, MD 가 25 사용) · 16 코어 ·
    `which pw.x` 빈 출력 → **경로 아님**. RTX3090 은 VRAM 24 GB 로 gabia 보다 작다.
  · ⇒ 경로는 **KISTI** (`sbatch_phaseB_v3_kisti.sh`, amd_a100nv_8, GPU 4장).
  · 2026-08-19 1저자 판단: **이 건은 외주**. 우리 쪽에서 더 안 판다.
- reference_dft(절대 binding 기준)는 0 ionic step이라 from-scratch 별도 결정 필요.

### 5. h-BN 시트 굴곡 0.27–0.37 Å (vgcf_hbn_neb.json flag_hbn_corrugation)
- 자유 h-BN 단층은 <0.01 Å 평면이어야 정상. Li-유도 pucker인지 4×4 셀 리플인지
  relax 미완인지 미해결 — h-BN 표면 수치(7 meV) 정량 인용 전 확인.

### 6. ~~LPSOCl COHP 곡선 원자료 회수~~ → ✅ **완료 (2026-07-29)** — 본문(+ 6b 회수 절차)은 `## ✅ 닫힌 항목` 절. ⚠ 인용 제약(곡선 면적 ≠ ICOHP)은 그 절에 그대로 있다.


### 7. ~~litdb 인덱스 정합 — digest 156편 중 67편이 INDEX 어디에도 없다~~ → ✅ **닫음 (2026-08-06)** — 본문은 `## ✅ 닫힌 항목` 절. 남은 것(`comparison_vs_ours.md` 미언급분)은 인덱스 정합이 아니라 내용 작업이다.

### 10. ~~ELF·그림 계 표시명이 4가지로 갈렸다~~ → ✅ **닫음 (2026-08-06)** — 본문은 `## ✅ 닫힌 항목` 절. ⚠ 이미 만든 PNG 는 옛 라벨 그대로다.

### 8. lpscl16 PDOS 의 VB-top DOS 가 비정상적으로 작다 (2026-08-04 발견 · 판별 대기)
- gap 정합 검사 중 발견: lpscl16 DOS/PDOS 파일의 **CB 에지는 정본 2.099 와 정합**하는데,
  **E=0(VBM) 에서 DOS 가 0.019 states/eV** — lpsocl(1.59)·b2o3(2.82)의 **1/80~1/150**.
  원소투영·총DOS 모두 동일 → 투영 문제 아님.
- 두 가설: (a) modelc VB top 이 실제로 뾰족한 단일 밴드 꼭대기(분산 큰 밴드, 물리) —
  anti-site 배치 차이로 가능 (b) VBM 정렬 기준이 이 DOS 런과 다른 런에서 옴(아티팩트).
- **판별**: 서버의 modelc nscf 고유값에서 VBM k-점 근방 밴드 분산 확인, 또는 dos 재생성
  시 자체 고유값 VBM 으로 재정렬. 판별 전까지 **lpscl16 VB-top DOS '모양' 인용 보류**
  (gap·적분량 인용은 무관).
- 맥락: 세 PDOS 파일의 gap 인코딩 자체는 셋 다 정본과 정합 ✅ (2026-08-04 검사).

### 9. 🔴 comp1 PMF 침투 F* 0.20 eV 가 **β 게이트 문제를 그대로 물려받는다** (2026-08-05 발견)

> ⛔ **β=0.8 하드게이트는 2026-08-26/27 폐기됐다** (`kb/concepts/beta-gate.md` §7-5·§7-8b, 회신 F). 아래 '게이트 통과/실패' 문구는 **경보값**으로만 읽는다. 판정축은 자유절편 (c, m) · 홉 수 · 다중 창이고, 도구는 2026-08-30 에 교체됐다(§7-8e). ⚠ **양방향이다** — 문턱을 내리면 '다 통과' 가 아니라 **통과했던 것도 무효**다(§7-6). (2026-08-31 전수 조사에서 붙임)
- **1저자 지적**: "comp1 은 β 값 못 믿는다며?" — 맞다. **같은 궤적에서 나온 값이다.**
  `comp1_Cl1.0_T600_Li.cube` (deck 600 K MLIP-MD) → PMF F* 0.20 eV 이고,
  `comp1 Ea 0.2532` 도 같은 deck 궤적 산출이다. 게이트 문서(2026-08-01) §4 가 이미
  "deck 궤적 msd.json **미검사**"로 적어 뒀고, **같은 프로토콜의 s2·s3 는 6/6 전부 케이지**
  (β 0.17–0.79). 즉 deck 궤적만 아직 검사를 안 했을 뿐 형제들은 전부 탈락했다.
- **영향 방식이 D 와 다르다 (중요)**:
  - $D$·$E_a$ — 케이지면 MSD 기울기가 $D$ 가 아니다. **직접 무효.**
  - $F^*$ — 밀도 $\rho$ 는 *점유* 측정이라 케이지여도 정의는 된다. 하지만 $F^*$ 는
    **연결 경로에서 가장 덜 방문된 voxel** 이 정하는데, 케이지면 그게 바로 안 가본 곳이다.
    → $\rho \to 0$, $F \to$ 큼 → **$F^*$ 는 상한(과대)** 이다.
- ⚠ **비교에 미치는 방향까지 나쁘다**: 표집 부족은 **더 갇힌 계에서 더 심하다**.
  comp1 이 modelc 보다 더 갇혔으므로 comp1 의 $F^*$ 가 더 부풀려진다
  → 보고된 **0.20 → 0.17 (−15%) 감소폭이 과장됐을 수 있다** (부호는 유지될 가능성 큼).
- **독립성 주장 범위 정정**: MASTER 의 "BVSE 와 독립적으로 확인"은 맞다(BVSE 와는 독립).
  그러나 **MD 와는 독립이 아니다** — 같은 궤적을 MSD 대신 밀도로 본 것이라
  "게이트 탈락"과 "케이지 밀도"는 **같은 관측의 두 표현**이다. 상호 검증으로 쓰면 순환논증.
- **판별(둘을 한 번에)**: kgy 의 comp1 **1600 ps** 연장이 정확히 이 검사다.
  궤적이 길어지면 병목 voxel 이 채워지므로 — ① β 가 오르는가 ② **$F^*$ 가 내려가는가**.
  $F^*$ 가 내려가면 0.20 은 표집 상한이었던 것. 둘 다 안 변하면 600 K 에서 실제로 갇힌 것.
- **그때까지**: F* 0.20/0.17 은 **"600 K, 표집 상한"** 딱지와 함께만 인용.
  슬라이드·원고에 온도(600 K)와 이 단서를 반드시 병기.
- 관련: open_items #1 · `kb/results/mlip_md_diffusive_gate_2026_08_01.md` §4 ·
  `kb/results/MASTER_structure_property_logic_2026_06_21.md` · `tools/ionic/li_percolation.py`

### 11. 🔶 **+B₂O₃ 가 축 사이에서 충돌한다 — 전도도 1등 ↔ 공기안정성 최악군** (2026-08-05 신설)

**계기**: [Zhu20] SI 엑셀(2026-08-05 입수)의 **이성분 황화물 가수분해 ΔE** 47종 표에서
`B₂S₃ = **−0.901 eV**` — 47종 중 뒤에서 두 번째다(꼴등 Al₂S₃ −0.910).
부호 규약: **양수 = 흡열 = 가수분해 불리 = 공기 안정**. 우리 host 기준선은 **Li₂S = +0.225 eV**.

**왜 우리 문제인가** — 우리 `+B₂O₃` 는 **다른 축에서는 최선**이다:
- PMF ΔF_perc **0.1607 eV**(4시드) < modelc 0.173 — 4계 중 최선
- MD Ea 0.199±0.034 ≈ modelc 0.197 — 동급 ⛔ **이 값은 2026-08-23 철회다** (레지스트리
  `status: retracted`): 0.199 는 600–1000 K **전구간 단일 직선** 적합인데 아레니우스가
  800 K 위에서 굽는다(구간 Ea 600→800 **0.222** / 800→1000 **0.077**, 145 meV 차).
  대신 쓸 것은 **저온 구간 Ea** 다. 아래 충돌 논증은 이 숫자에 의존하지 않는다 —
  "전도도 축에서 나쁘지 않다" 정도로만 읽는다.
- 그런데 우리 자체 결과가 **"B–S 가 free-S 를 −1.1 → −2.15 eV 로 안정화"** = **B 가 실제로 S 와 결합한다**.
  [Zhu20] 기준이면 **그 B–S 결합이 가장 가수분해되기 쉬운 결합**이라는 뜻이다.

**판정해야 할 것**
1. 이성분 B₂S₃ 값이 **격자 안 B(도핑 농도 x=0.25)** 에 그대로 전사되는가?
   ⚠ 이건 **양이온의 S 친화도 프록시**지 도핑된 LPSCl 의 ΔG_hyd 가 아니다 → **#12 로만 닫힌다.**
2. B 가 O 를 데리고 들어오는 형태(B₂O₃)라 **B–O 가 유지되면** 이 위험이 상쇄되는가?
   (우리 구조에서 B 의 1차 배위가 S 인지 O 인지 — 기존 궤적/구조로 즉시 셀 수 있다)
3. 상쇄가 안 되면 **cascade 점수 체계에 공기안정성 축을 넣어야** 한다 (현재 없음).

**비용**: 2번은 기존 구조 후처리 = 새 계산 0. 1·3번은 #12 에 의존.

**★ 2026-08-05 보강 — B 가 S·Cl 양쪽에서 최악으로 확정**
전사본 전수에서: **B₂S₃ −0.901** · **Li₃BS₃ −0.893** · **BCl₃ −0.120**(HCl 보정 환산 −0.834).
즉 황화물 축에서도, 염화물 축에서도 최하위군이다. → **방어선은 "B 가 B–O 로 남는가" 하나뿐**이고,
그래서 위 판정 2번(우리 구조에서 B 의 1차 배위가 S 인가 O 인가)이 **핵심 계산**으로 승격된다.
계산 목표는 ΔG 값이 아니라 **분해 산물에서 B 의 행선지**다.

**Nd 도 같이 흔들린다**: **LiNdS₂ −0.273**(민감) ↔ **NaNdS₂ +0.221**(안정) — **알칼리 종에 따라
부호가 뒤집힌다.** Li 계에서 "Nd 가 대기 안정을 준다"는 이 표로는 지지되지 않는다.
⚠ **Mg·Co·Ni·Mo 는 데이터셋에 아예 없다** — 프록시 자체가 불가.

---

### 12. 🔶 **가수분해 축(ΔG_hyd) 착수 조건이 갖춰졌다 — [Zhu20] 레시피 + 정답지** (2026-08-05 신설)

§H 의 *"moisture ΔG_hyd 계산 **0건**"* 을 닫는 항목. 종전엔 **레시피만** 있었는데
(SI Methods 의 Step 1–4), 2026-08-05 에 **SI 엑셀 = 정답지**가 들어왔다:

| 시트 | 행 | 내용 |
|---|---|---|
| `M-S` · `M-Cl` | 47 · 54 | 양이온별 **가수분해 반응식 + ΔE (eV)** |
| `Li-M-S` · `Na-M-S` · `Li-M-Cl` · `Na-M-Cl` | 53 · 66 · 15 · 40 | 0 V 환원 / 4.5 V 산화 반응식 + 에너지 |

**단계 (이 순서로)**
1. **파이프라인 재현 검산** — 우리가 구현한 것으로 **문헌 값을 먼저 맞춘다**.
   앵커: `Li₂S +0.225` · `P₂S₅ −0.156` · `GeS₂ +0.412` · `SiS₂ −0.847`.
   ⚠ 이걸 못 맞추면 그다음 숫자는 전부 무의미하다.
2. 우리 조성으로 확장 — comp1 · modelc · **LPSOCl** · **+B₂O₃** · Nd.
3. `air_hsab` **정성 tier → 정량 축**으로 승급, cascade 점수에 편입 여부 판정(#11-3).

**★ 2026-08-05 발견 — [Zhu20] 논문 자체의 규약 불일치 (검산 시 반드시 반영)**
염화물 값이 **SI 본문과 엑셀에서 다르다**: LiCl 본문 **+0.977** vs 엑셀 **1.335**.
차이 **0.357 eV = k_BT·ln(10⁶) @300 K = HCl 1 ppm 부분압 보정항**(HCl 1개당).
증거 3중 — Fig 1b 의 1 ppm 선 위치 · Fig S1 의 **기준선**(≈0.98/1.53, 본문 규약) ·
그런데 **같은 Fig S1 의 데이터 점**(≈1.34/1.88)과 Fig 3c 는 엑셀과 일치.
→ **염화물 표·산점도가 HCl 보정을 빠뜨렸고, Fig S1 한 장 안에서 두 규약이 섞여 있다.**

⚠ **순위가 바뀐다**: Li₂ZrCl₆ 0.632 → **−0.08** · Li₃YCl₆ 0.886 → +0.17(경계) ·
LiAlCl₄ 0.383 → −0.33. 그리고 **환산값 쪽이 실험(LYC/LZC 는 습기에 약하다)과 더 잘 맞는다.**
전사 CSV 에 원본·환산 두 열을 병기했고 **환산은 우리 추론**임을 명시했다.
→ **A2 검산은 반드시 본문값 +0.977 로** 맞춘다(규약 확정용).

**⚠ 규율**
- 엑셀 값은 **문헌 소환값**이다. 전사 CSV 헤더에 그 사실을 박고, 우리 db 절대값과 같은 표에 넣지 않는다.
- 구현 전까지 **"우리가 가수분해를 계산했다"는 서술 금지** — 지금 우리 보유는 0건이다.
- 이성분 프록시(#11-1)와 조성 ΔG_hyd(본 항목)는 **다른 양**이다. 섞어 인용하지 않는다.

**연결**: 심사 중인 리뷰(ECER-D-26-00097)가 §3.1 에서 이 논문을 **ref [84]** 로 인용하고,
같은 절 맺음의 "미래 모델 4요건" 중 **④ 고체–기체 반응 열역학**이 정확히 이 축이다
(→ `kb/reviews/ECERD2600097_review_notes.md` Q6).

### 13. 🔴 **`air_hsab` 등급이 이름·근거 둘 다 부정확하다 — 문헌 대조로 확인** (2026-08-05 신설)

**무엇을 했나**: [Zhu20] SI 전사본(`db/properties/zhu2020_si_hydrolysis_energies.csv`)의
이성분 황화물 가수분해 ΔG 로 우리 cascade 47종 `air_hsab` 등급을 **산화수까지 맞춰** 대조했다.
기준선 = **Li₂S +0.225 eV**(양수 = 가수분해 불리 = 보호적).

| | |
|---|---|
| 대조 가능 | 35종 (M-S 표에 같은 산화수가 있는 것) |
| **맞음** | **26** |
| **어긋남** | **9** — ⚠ **전부 같은 방향**(우리가 0.2 로 깎았는데 문헌은 보호적) |

어긋난 9종: **In³⁺ +0.599** · Sn⁴⁺ +0.441 · Ba²⁺ +0.422 · Na⁺ +0.416 · Ge⁴⁺ +0.412 ·
Ga³⁺ +0.362 · Sr²⁺ +0.359 · Ca²⁺ +0.264(CaO·CaF₂)

**왜 틀렸나** — 이름이 곧 원인이다. 우리 등급은 **Pearson softness** 로 키를 잡는데,
[Zhu20] 이 보인 실제 구동변수는 **oxophilicity**(양이온이 S 대신 O 를 얼마나 원하나)다:
- **Sb³⁺ +0.535 ↔ Sb⁵⁺ −0.167** — 같은 원소가 산화수로 **0.70 eV 뒤집힌다**. HSAB 로는 설명 불가
- **Zn²⁺ +1.081 > Ag⁺ +1.040** — softness 서열과 반대
- 알칼리토(Ca·Sr·Ba)는 **hard acid 인데 보호적** — softness 축에선 나올 수 없는 결과

⚠ **가장 아픈 칸은 In³⁺** 다. 문헌(InF₃ 치환 아지로다이트)이 효과를 보고하는 계열인데
우리 등급은 최하(0.2)로 깎아 놨다 — 심사 중인 리뷰도 §3.2 에서 InF₃ 를 대표 사례로 든다
(→ `kb/reviews/ECERD2600097_review_notes.md` Q9).

✅ **반대로 잘한 것**: **산화수를 등급 키로 쓴 결정(ml-13)은 검산으로 정당화됐다**.
Sb₂O₅→Sb⁵⁺ −0.167 · TiO₂→Ti⁴⁺ −0.304 · ZrO₂ −0.459 · SiO₂ −0.847 · B₂O₃ −0.901 —
전부 우리 0.2 와 일치. 원소 심볼만 썼으면 Sb 를 borderline 으로 잘못 올렸을 것이다.

**조치**
1. ✅ (2026-08-05) 도구 주석·면책 문구에 **검산 결과와 한계**를 박았고, 뜻이 맞는 키
   `air_protect_tier` 를 **병기**했다(기존 `air_hsab` 는 하위호환으로 유지).
2. ✅ (2026-08-05) **테마 축(`air_stability`)의 metric_key 를 `air_protect_tier` 로 이관**했고,
   F 보너스를 뺀 **순수 등급 `hsab_grade_raw`** 를 별도 열로 분리했다(검산은 이 열로 해야 맞는다 —
   검증 대상이 "HSAB 로 가릴 수 있나"이지 "F 화학이 좋은가"가 아니다).
   ⚠ **남은 소비자는 `tools/cascade/codoping_ml.py` 하나인데, 여기선 못 지운다** —
   `air_hsab` 가 학습된 모델의 **피처 이름**이라(`SINGLE_FEATS`, `db/properties/codoping_ml_v2_meta.json`)
   이름을 바꾸면 저장된 메타와 어긋난다. **제거 = 재학습**이 전제다. 그전까지 별칭 유지.
3. ✅ (2026-08-05) **문헌 대조축을 상설화**했다 — 손으로 센 숫자를 문서에만 두지 않는다.
   - 테마 **`air_stability_lit`** 신설 (metric `dG_hyd_MS_lit`, [Zhu20] 소환값, **35/47 커버**)
   - 도펀트 행에 `dG_hyd_MS_lit` · `dG_hyd_MS_ref` · `dG_hyd_MCl_lit_pub` ·
     `dG_hyd_MCl_preset_ours` · `dG_hyd_MCl_ref` 추가
   - **`db/properties/cascade_air_axis_lit_vs_tier.csv`** (Origin-ready) — 47행 전수 대조표.
     빌드마다 재생성되므로 **일치 26 / 과소평가 9 / 문헌 없음 12** 가 검증 가능해졌다.
   - webapp: 소환값 전용 면책 카드(출처·계산수준·조건·매칭·커버리지·염화물 규약·프록시 한계) 노출
   - ⚠ **조합 랭킹의 null 처리를 고쳤다** — 기존 `cascade.html` 은 norm 이 null 이면 **0** 으로 깔았다.
     0 은 "가장 나쁨"이라 기하평균에서 그 도펀트를 말살하는데, **데이터 없음 ≠ 나쁨**이다.
     → 선택 축에 결측이 있는 도펀트는 **랭킹에서 제외**하고 몇 종이 왜 빠졌는지 표시한다.
     (지금까지는 null 이 하나도 없어서 안 터졌을 뿐 — 이 테마가 처음 12개를 만든다.)
4. ⏳ **근본 해결은 #12** — [Zhu20] 레시피로 ΔG_hyd 를 **직접 계산**해 정성 등급을 **대체**한다.
   이제 대조축이 상설이라 #12 산출물이 나오면 **같은 CSV 에 열 하나 더**로 3자 대조가 된다.

**그전까지 읽는 법 (중요)**
- 이 열은 **Cu/Ag/Zn 계열 식별용**으로만 쓴다.
- **낮은 등급을 "공기 불안정"으로 읽지 않는다** — 그건 판정이 아니라 **판정 없음**이다.
- 이 열로 도펀트를 **탈락시키지 않는다**(9종이 부당하게 깎여 있다).
- **문헌축(`air_stability_lit`)과 정성축(`air_stability`)을 합산하지 않는다** — 계산 수준이 다르다.
  둘을 나란히 놓고 **어긋나는 곳을 보는 것**이 이 축의 용도다.

### 14. 🟡 **화학→역학 다리: ΔV_rxn × C_ij (그리고 Griffith K_IC)** (2026-08-05 신설)

**어디서 나왔나** — 심사 중인 리뷰 §3.5 검토(`kb/reviews/ECERD2600097_review_notes.md` Q18–Q22).
원고는 *"분해 산물의 몰부피 차이 → 인장응력 → 미세균열 → 입자 파단 → 단락"* 사슬을 **전부 정성으로만**
쓴다. 그 사슬의 재료 상수를 **우리가 이미 갖고 있다** — 새 대형 계산 없이 조립만 하면 된다.

**세 조각 (전부 repo 안에 있음)**

| 조각 | 소스 | 등급 | 상태 |
|---|---|---|---|
| ① 0 V 환원 산물 집합 (Li₃P·Li₂S·LiCl) | `db/properties/oxidation_stability.json` 계보 · `sei_products.json` | ★ grand-potential | ✅ 있음 |
| ② 탄성상수 full Cij + B₀ | `elastic.json` `dft_0K_relaxed_ion_stress_strain_full_Cij` · `eos.json` | ★ paper-grade DFT (E_VRH 가 실험 ~23 GPa 와 일치) | ✅ 있음 |
| ③ 표면에너지 γ | `adhesion.json` `surface_energies` (`two_gamma`) | ⚠ **UMA 슬랩** — 같은 파일에 vacuum 아티팩트 이력 | ✅ 있음(등급 낮음) |

**할 일**
1. **ΔV_rxn 산출** — ①의 균형 반응식에 MP 셀부피를 넣어 *소모 SE 1 몰당* ΔV 를 낸다.
   ⚠ **정규화 기준을 열 이름에 박는다**(per f.u. / per atom / per anion), 그리고
   **음극에서 소모되는 Li 금속 부피를 포함한 값과 제외한 값을 둘 다** 낸다 — **부호가 갈리는 자리**다.
2. **응력 스케일** σ ≈ B·ε_v, ε_v = ΔV/V. ②의 B₀ 와 도핑계 B₀(`cascade_v23_champions.csv`
   `eos_B0_GPa`)로 범위를 낸다.
3. **Griffith 경로** G_c ≈ 2γ, **K_IC = √(E·G_c)** → 임계 결함 크기 a_c = K_IC²/(πσ²).
   ⚠ **이상취성이라 실제 인성의 하한**이고 γ 가 UMA 라 **자릿수 주장까지만**.
4. 산출물: `db/properties/interface_volume_stress.json` + Origin-ready CSV, 하우스 스타일 그림 1장.

**스코핑 결과 (⚠ 확정 아님 — 이 항목을 실제로 할 이유)**
- ②③ 로 낸 LPSCl 이상취성 **K_IC ≈ 0.2 MPa·m^½ 급**.
- 원고 **§5.1 이 인용하는 K_IC 는 0.2–0.4 MPa·m^½ 급**
  (`litdb/papers/miao2023_role_of_interfaces_solid_state_batteries.md` 대조).
  → 우리 값이 **그 구간 하단**에 앉는다. 이상취성이 하한이어야 한다는 기대와 **부호가 맞는다.**
- 그 K_IC 를 원고의 **임계 입자크기 ~3 μm** 에 되먹이면 필요한 국소 인장응력이 **수십 MPa 급**,
  이를 B₀ 로 나누면 **부피 불일치 ~0.3 %** 면 충분하다는 계산이 나온다.
  ★ **방향 주의 — 이건 원고를 반박하지 않고 지지한다**(기전이 매우 쉽게 성립).

**⚠ 스코핑 해석 정정 (2026-08-05, [Famprikis19] 반영)**
처음엔 *"우리 Griffith 값이 문헌 K_IC 구간 하단에 앉는다"* 를 **좋은 신호**로 적었다. 절반만 맞다.
[Famprikis19](*Nat. Mater.* 18, 1278)가 못박기를, **파괴인성은 탄성계수와 달리 치밀도·입경·불순물·
기존 균열·기공에 강하게 의존하며 실험으로 결정해야 하는 양**이다. 그러면:
- 문헌의 0.2–0.4 는 **특정 시편 미세구조의 값**이지 재료상수가 아니다.
- 우리 Griffith 값은 **이상취성 단결정 하한**이다.
- **둘은 애초에 같은 양이 아니다** → 근접성을 *"자릿수가 맞는다"* 이상으로 해석하면 안 된다.
→ #14 의 산출물은 **"K_IC 를 계산했다"가 아니라 "이상취성 하한을 냈다"** 로만 부른다.
그리고 실제 파괴 판정은 **K_IC 를 sweep 파라미터로 받는 DEM/CZM** 쪽 몫이다
(원전: `bucci2017…czm` — [Famprikis19] 의 K_IC 담론이 기대는 유일 근거).

**규율**
- γ 가 UMA 이므로 **문헌 K_IC 와의 근접성을 검증 논거로 쓰지 않는다** (`litdb` 소환값과 섞지 않기).
- **μm 급 입자 역학은 우리 셀(nm)로 못 다룬다.** 우리가 대는 건 **재료 상수**이고 입자 스케일은
  DEM/연속체 몫 — 이 경계를 흐리지 않는다.
- b2o3_champion 전단은 **withheld** 상태(`kb/results/b2o3_elastic_analysis_2026_07_03.md`) —
  도핑계 G 를 쓰려면 재측정이 먼저다.
- ✅ **탄성 쪽 앵커는 오히려 강해졌다** — [Famprikis19] 소환 thiophosphate glass **E ≈ 20 / G ≈ 7 GPa**
  (McGrogan 나노인덴테이션)가 우리 relaxed-ion 22.06 / 8.13 과 같은 자리이고
  clamped-ion 52.31 / 20.12 는 2.4–2.9 × 어긋나 배제된다.
  ⚠ **유리 vs 결정 아지로다이트**라 *"실험이 검증했다"* 는 금지 — *"같은 자리, clamped 배제"* 까지만.


### N. ✅ **gap 정본 fixed-occ 실행본** — **4/4 해소 · 닫힘** (2026-08-07 신규 · 2026-09-11 닫음)

> ✅ **2026-09-11 — modelc 확인, 이 항목 닫는다.**
> gabia `/data/work/runs/gap_nscf/modelc/nscf_gap.{in,out}`:
> `occupations='fixed'` · `K_POINTS 8 8 2` → **68 irr**(정본 `68 irr` 일치) · nbnd 190 ·
> **VBM 2.4447 / CBM 4.5436 / gap 2.0989**(정본 2.099, 소수 넷째 자리 재현) · `JOB DONE`.
> ⛔ **계산이 아니라 기록이 밀린 것이었다** — 08-31 16:51 시작본이 09-03 02:57 에 완주했는데
> 그 사실이 8일간 원장에 안 올라왔다. 오늘 같은 날 `fcgap`(힘 대조 파일럿)도 같은 이유로
> 다시 돌렸다. **던지기 전에 서버를 본다** 가 이 항목이 남기는 교훈이다.
> → `canonical_registry` modelc `method_integrity_flag` 해소 · `method_id` 에 `__k882` 복원
>   (⚠ 같은 라벨을 2026-08 에 한 번 잘못된 근거로 붙였다 철회한 적이 있다 — 이번엔 실제
>   실행본이 근거다) · `artifacts.json` `A-comp1-modelc-gap-run` → canonical.
> ⚠ 사본이 gabia 한 곳뿐이다(`needs_duplication`). 3중 수색 실패는 **2026-06-16 원본**에
> 대한 것이고 그건 지금도 없다 — 닫는 근거는 원본 발견이 아니라 **재계산 재현**이다.
> ⇒ 네 계(comp1·modelc·b2o3·lpsocl)가 이제 같은 `gap-fixedocc-eigenvalue-v1` 등급이다.
> 한 표에 나란히 쓸 때 더 이상 단서를 달지 않아도 된다.
> ⛔ 단 comp2(2.04)는 여전히 `legacy-dos-threshold__unverified` — 다른 줄이다.

> ✅ **2026-08-31 갱신** — 제목의 "4종 미확보" 는 낡았다.
> · b2o3 ✅ 2026-08-20d (백업 A, `occupations='fixed'`, VBM 2.4717 / CBM 4.4388 — 정본 일치)
> · lpsocl ✅ 2026-08-20g (kgy `03b_nscf_gap`, VBM 2.3870 / CBM 4.6179)
> · comp1 ✅ 2026-08-24 재계산 (VBM 2.1281 / CBM 4.1937 / gap **2.0656** / 170 irr).
>   2026-08-31 재실행도 `JOB DONE` 으로 같은 값.
> · **modelc ✅ 2026-09-03 완주** — 08-31 16:51 재시작(`--mca btl self,vader`, np 10 -nk 10)이
>   그대로 끝났다. 확인은 2026-09-11 (위 참조).
> 근거: `db/governance/artifacts.json` 의 `A-{b2o3,lpsocl,comp1-modelc}-gap-run` ·
> `canonical_registry.json` `_history` 2026-08-20d/g · `kb/methodology/offline_archive_index_2026_08_20.md`
> ⚠ 아래 표의 "(파일 없음)" 은 그 시점 기록이다.

**값을 의심하는 게 아니다** — comp1 2.066 / modelc 2.099 / b2o3 1.9671 은 `electronic.json` 이,
lpsocl 2.2309 는 **`lpsocl_dos_gap.json`** 이 정본으로 기록하고 있다(레지스트리 source_path 참조).
문제는 **재현성**이다.

우리 규율은 "갭은 **fixed-occupations nscf** 의 VBM/CBM 고유값만 인정" 인데,
**계통별 실행본**이 없다. 정확히 말하면:

- ✅ **방법은 repo 에 있다** — `tools/electronic/standard_dos/nscf_gap.in` 이 generic
  fixed-occ 템플릿이고 `occupations='fixed'` 다.
- ⛔ **계통별로 남은 `*_nscf.in` 은 전부 `occupations='tetrahedra_opt'`(DOS 용)** 이라
  fixed-occ 근거로 쓰면 안 된다.
- ⛔ 그래서 정본을 만든 **그 실행**(입력·출력)을 파일로 되짚을 수 없다.

★ 템플릿 주석이 결정적이다 — modelc(rhombo)에 **`6 6 2`** 를 제시한다.
DOS 용 `8 8 2` 와 다르다. 즉 DOS 파일만 보고 method_id 를 정정하면 안 됐다.

| 계 | standard_dos 의 nscf.in | electronic.json 의 kpts 기록 | 판정 |
|---|---|---|---|
| comp1 | `tetrahedra_opt` · k 8 8 8 | `170 irr (k888 nscf)` | k888 강하게 시사, 입력 미확보 |
| modelc | `tetrahedra_opt` · k 8 8 2 | `68 irr` | k-mesh **단정 불가** (템플릿은 6 6 2 제시) |
| b2o3 | (파일 없음) | `25 irr (fixed-occ nscf)` | **fixed-occ 명시** — 근거 제일 강함 |
| lpsocl | (파일 없음) | `lpsocl_dos_gap.json` 의 method 에 fixed-occ 명시 | 방법은 명확, 실행본 없음 |

⚠ 2026-08-07 5라운드에 modelc 의 `method_id` 를 `k882` 로 "정정" 했는데, 그 근거가
바로 저 tetrahedra 파일이었다 — **오류를 정정하면서 같은 종류의 오류를 반복했다.**
철회하고 k 표기를 다시 뺐다.

**닫는 방법 (순서대로)**
1. 실제 fixed-occ 입력·출력을 찾는다 (gabia `/data/work/` · kgy · KISTI 스크래치)
2. 없으면 백업에서 회수
3. 끝까지 없으면 **동일 조건으로 재계산**하거나, 그때까지 `provenance_open` 을 유지하고
   필요하면 status 를 낮춘다

레지스트리 4개 항목에 `provenance_open` 필드로 표시했고, **`validate_canonical.py` 가 매번 찍는다**
(요약 줄 + 전용 경고 블록). 레지스트리·문서에만 있으면 검사를 돌려도 무경고 ✅ 라 놓친다
— Codex 6라운드 후속 지적. 화면 값은 그대로 쓰되 이 사실이 같이 남는다.

- 근거: Codex 6라운드 감사 (comp1) + 확인 결과 4종 전부로 확대


### O. ✅ **Nd 갭 — 3종 자체 측정 완료 (2026-08-12 마감)** — 본문은 `## ✅ 닫힌 항목` 절. 정본값 frozen-4f **Nd₂O₃ 3.948 / LiNdO₂ 3.698 / Nd₂S₃ 0.770 eV** (`db/properties/sei_electronic.json`), MP 우회 폐기.

### P. 🔴 **SDCP·PTFE 자리 선호 — "Li 를 선호한다"는 지금까지 판정된 적이 없다** (2026-08-11 신설)

**✅ 2026-08-28 — `sdcp_neutral` 은 닫혔다.** 확정값·허용서술·금지서술·**재개 조건 4개**를
`db/properties/sdcp_neutral_closed_2026_08_28.json` 에 못박았다. 재개 조건(자리대비 n≥3 ·
쌍 DFT 이완 · k 직접검증 · 피복률 수렴) **밖의 이유로 다시 열지 않는다** — 조건 없이 두 번
닫았다가 두 번 물린 것이 이 문서를 만든 이유다 (CLAUDE.md 「마감 규율」).
~~이 항목에 남은 것은 doped 뿐이다.~~ ⛔ **2026-08-31 정정** — doped 도 2026-08-28 에 **마감됐다**(`sdcp_doped_closed_2026_08_28.json`, active·ratified, `D-2026-08-28-sdcp-doped-scope-closure`). neutral·doped 둘 다 마감이고 남은 것은 **재개 조건뿐**이다 (neutral 4건 / doped 회신 O 7건). ⚠ 아래 표·서술 중 doped 의 **자리선호 방향** 문구는 마감의 금지목록('무선호 를 포함한 방향 서술 일체')에 걸린다 — 원고·슬라이드에 쓰지 않는다.

**★★★ 2026-08-28 wave1.5 + 회신 M — 마감 보류로 정정.**
wave1.5 는 성공(basin A 확정, 3다리 검증)했으나, 그 위에 우리가 세운 **basin-매칭 ΔE_site 가
잘못된 보고량** 이었다(회신 M P0): 혼합-basin 쌍에서 다른 슬랩을 빼면 슬랩 gap 49.718 meV 가
산술적으로 들어와, "두 시드 1 meV 재현"(v2)은 착시였다. 직접 총에너지차가 진실이다:

| 조각 | net4 쌍 basin | 직접차 Ni−Li | 판정 |
|---|---|---:|---|
| ptfe_c10 | A/B 혼합 | +100.22 meV | ⛔ 자리선호 아님 (gap 포함). **pm1 단일 +49.77** |
| ptfe_dimer | **B/B** | +36.16 | ✅ 고정-basin. pm1 36.07 과 **0.087 meV** 재현 |
| sdcp_neutral | B/A 혼합 | −40.70 | ⛔ 동상. pm1 +9.27 — **30 meV 해상도에서 미해결** |
| sdcp_doped | **A/A** | −18.95 | 고정-basin이나 단일 시드·상대 스핀 미열거 — 인용 불가 |

허용 서술 (회신 M): 전부 **"UMA-selected matched pose 에서의 vertical energy contrast"** 로
한정. neutral 은 "무선호" 가 아니라 사전등록 판정바닥(max(30 meV, 쌍 편차) · n<3 NO_VERDICT —
`kb/questions/sdcp_site_preference.md`, **v2 가 이 자체 규약을 안 읽었다**) 아래 미해결.
"105 meV branch 갈림" 도 철회 — pm1 ΔE(+86.45, 미수렴 포함) vs net4 ΔE(−18.95)의 차였다.

라디칼을 닫으려면 (회신 M 설계): **statics 16개** = 2 site × 2 기판상태 × 2 상대스핀 × 2 상.
NUPDOWN 은 라디칼 기여 ±1 (2S_z) — net4 는 3과 5, pm1 은 AFM 배열 정/역 × NUPDOWN=1
(**NUPDOWN=−1 금지** — 해제 예약값). 원고에 핵심 아니면 **③ 제외 + 추출 부호만 유지** 권고.
phaseB 원자료(zip)는

프로토콜 정본: `kb/methodology/site_preference_protocol_2026_08_11.md`
도구: `tools/sdcp/site_screen.py` (게이트 회귀시험 11/11 통과) · 실행기 `run_site_screen_gabia.sh`

**★ 정정 (같은 날, gabia 216자세 전수 실측)** — 배포 자세 2종만 보고 "Ni 를 안 재봤다"고
적었던 것은 틀렸다. freeze 0.85 재스캔 전수를 게이트에 넣으면 **Ni 접촉 자세가 넉넉히 있다**:

| 조각 | 자세 | 게이트 통과 | **Ni 접촉** | 최단 Ni |
|---|---:|---:|---:|---|
| doped | 108 | 75 | **66** | 2.59 Å (H···Ni) |
| neutral | 108 | 90 | **54** | 2.57 Å (H···Ni) |

정확한 서술: **"안 재봤다"가 아니라 "짝을 안 지었다".** 챔피언이 Li 접촉이었을 뿐이고,
Li 자세와 Ni 자세가 같은 방향·roll 로 짝지어져 있지 않다. 게다가 **자리가 분자 방향에 종속**
(`etherO_down` r180/r270 → 거의 전부 Ni, r0 → Li)이라 방향 미고정 비교는 두 효과가 섞인다.
(배포 자세 2종이 Ni 접촉 없이 Li 만 갖는 것 자체는 그대로 사실 — 그 둘로는 비교 불가.)

**★ VASP 단일점 두 자세는 접촉 종류가 다르다** (Δ 인용 금지의 구체적 근거):
doped `r0_g20` 최근접 = **H···Ni 2.89 Å** (Li 3.06, 배위 없음) / neutral `r180_g22` = **O···Li 2.09 Å**
(진짜 배위, Ni 없음). Δ 는 "도핑 효과"가 아니라 "다른 접촉 방식의 차"다.

**★ 레거시 풀 오염**: neutral 18/108 자세가 가로 이미지 **4.01–4.03 Å** (`etherO_down` r90/r270)
— 순위 풀에 주기이미지 겹침 자세가 섞여 있었다.

**★ 게이트 재교정 (우리 초판이 틀렸다)**: "비금속···양이온 < 2.00 Å 일괄 = 반응" 컷이
O···Li 1.75–1.94 Å 를 33건 잘못 죽였다. Li–O 배위는 1.90–2.20 Å 가 정상이고 기체상 LiOH 는
1.58 Å 다 — **짧다고 반응이 아니다.** 원소쌍별 **탈락 <0.80 Σr_cov · 태그 <0.92 Σr_cov** 로 교체.
자체검사 14개(F···Li 1.35 탈락 / 1.60 태그 / 2.00 무태그)로 고정.
재교정 뒤 **같은 33건이 EXTRACTION 으로 다시 잡혔다**(수·격자점 분포 일치) — 짧은 O···Li 는
반응이 아니라 **술포네이트가 표면 Li 를 뽑아 올린 것**이었다. 초판은 맞는 답을 틀린 이유로 냈다.

**★★ 최종 판정 — 레거시 스캔으로는 자리 선호를 물을 수 없다** (검열-왜곡 검사 결과)

| 조각 | 검열 | 검열 최저 | 살아남은 최저보다 낮은 것 | 분포 Δ |
|---|---|---|---|---|
| doped | EXTRACTION 33, **전부 Li** | **−1.267** | Li **33/33** | −0.174 → **무효** |
| neutral | EXTRACT 26(Li) + IMAGE 18(Li9·Ni9) | −0.252 | Li 12/35 · Ni **9/9** | +0.146 → **무효** |

doped 의 "Ni 우세"는 Li 상위 33개를 통째로 잘라낸 뒤 찌꺼기를 비교한 **착시**다.
neutral 은 Ni 강한 자세가 이미지 게이트로 전멸했다. **둘 다 방향을 인용하면 안 된다.**
"가려지지 않았다"도 "졌다"도 아닌 **"이 데이터로는 물을 수 없다"**.

**★ 2차 재교정 후 재실행 결과 (확정)** — 엄격한 규칙(변위 Li>0.80 Å **AND** 기판 O 이웃
2개 이상 상실)으로 216 자세 전수 재판정:

| 조각 | 통과 | EXTRACTION | 변화 |
|---|---:|---:|---|
| doped | 75 | **33** | 그대로 — **진짜 추출로 확정** |
| neutral | 64 → **90** | 26 → **0** | 전부 정상 배위로 되살아남 |

**neutral 의 26건은 오판이었다** (거리 <2.20 Å 만으로 죽었다). Codex 지적이 정확했다.
**doped 의 33건은 엄격한 규칙에서도 그대로다** — 표면 Li 가 실제로 움직였고 배위를 잃었다.

> **★ 자기도핑이 Li 추출 경로를 연다** — −SO₃• 라디칼은 108 자세 중 **33**, −SO₃H 중성형은
> **0**. 단 UMA 기준이고, DFT+U 는 그 추출이 불리(`+0.336 eV`)하다고 이미 쟀다. 즉 이 비대칭은
> "doped 가 Li 를 뽑는다"의 증거이자 **"UMA 가 doped 에서만 추출 끝점을 과안정화한다"** 의
> 증거이기도 하다.

**★★ `champion_report.py` 의 −1.267 eV 정체 확정 → todo #30 닫힘**
freeze 1.0 → 0.85 에서 −0.258 → **−1.267 eV** 로 5배 깊어졌던 그 값이 검열된 33개 Li 접촉
자세의 최저와 **정확히 일치**한다. **−1.267 은 결합이 아니라 Li 추출 끝점**이고,
VASP+U 가 `dE_extract = +0.336 eV`(불리)로 이미 반증한 과정이다.
champion_report 가 사전등록한 세 가설 (a)화학흡착 (b)Li추출 (c)미수렴 슬랩기준선 중
**(b) 로 확정** — 사전등록 덕에 사후 합리화가 아니다.

**★ 별건 — 출처 불일치**: `db/structures/sdcp_poses_phaseB/` 는 freeze **1.0** 의 `r90_g22`/`r180_g01`
인데, `db/properties/sdcp_phaseB_dftu_v1.json` 의 VASP 단일점은 freeze **0.85** 의 `r0_g20`/`r180_g22` 다.
**구조 그림과 그 표를 한 자리에 올리면 안 된다.** 폴더 README 에 박아 뒀다. 0.85 기하는 repo 에 없다.

**막혀 있는 것**: `sdcp_v7c_neutral.xyz`(C₁₁H₁₆O₆S₂, 35) · `sdcp_v7c_doped.xyz`(C₁₁H₁₅O₆S₂, 34)
의 **기체상 ORCA 기하가 repo 에 없다** — gabia `$MOLDIR` 에만. 조성은 Phase-B 자세에서 분자를
떼어 역확인했다. → `run_site_screen_gabia.sh fetch` 로 회수 후 sha 고정.

**설계 요지** (하자 5개를 구조적으로 막음): 7자리 전수 × 피보나치 12방향 × roll 4 = 조각당 364 자세 ·
**Li/Ni 대조쌍 강제 보존** · freeze **1.0 과 0.85 이중 프로토콜** · 세로 이미지 게이트(샌드위치 재발 방지) ·
Li 추출 격리 · 판정 바닥 max(30 meV, 쌍 편차) · 검열(못 잼)과 패배를 분리.

**Codex 교차검증 상태**: 슬랩·PTFE 조각 sha256 동일 / Li·Ni·O_top 앵커 좌표가 독립 구현끼리
소수점까지 일치 / C10 가로이미지 문제를 양쪽이 독립 발견(Codex 는 azimuth 3개로 축소, 우리는 112건
자동 탈락) / 표면 자리 등가성 결론 동일. 우리가 추가한 것 = 추출격리·이중 freeze·SDCP 지원·
카이랄성 불변식·게이트 회귀시험. 아직 없는 것 = **basin 클러스터링(주기 RMSD)** — Codex 쪽을 이식할 것.

### Q. 🔴 **Li₃N(001) 6층 243원자 2점 테스트 — 원고 리비전의 유일한 진짜 구멍** (2026-08-12 신설)

방어 카드: `kb/syntheses/li3n_barrier_revision_defense_2026_08_12.md` (반론 C2·C3 가 여기에 걸려 있다).

- **무엇이 비었나**: 우리 Li₃N 장벽은 전부 **4층 슬랩**(Li₂N 4면 + Li 3면, 135+1 = 136 atoms)에서
  나왔다. 문헌 [54] Kim/Cui 는 6층. 계산 논문 리비전에 거의 반드시 오는
  "slab-thickness convergence?" 질문에 **지금 답이 없다.**
- **동시에 닫히는 두 번째 구멍**: 4층 슬랩에는 보고 최소점보다 **0.085 eV 낮은 2N-bridge pocket**
  이 있다 (drag p0, E_ads −3.073 vs −2.988 eV). 이게 얇은 슬랩 artifact 면 6층에서 사라지고
  문헌의 on-N 우물 순서와 일치하게 된다. `db/properties/diffusion.json` 의
  `li3n_drag_p0_site_identity_2026-07-17` 이 이 실험을 **결정 실험으로 지정해놓고 미실행**.
- **실행 방법**: 6층 3×3 N-노출 슬랩(243원자) 생성 →
  `tools/neb_diffusion/li3n_uma_investigate.py sites --layers 6 --supercell 3 3`
  (빌더 `build_li3n_001` 은 `tools/neb_diffusion/li3n_mlneb_gpaw.py`).
  구속이완 **2점만** (on-N xy · pocket xy, z 자유). kgy·gabia 한 대씩 나누면 병렬.
- **비용**: 243/136 → SCF 스텝당 5–6배. 며칠 규모.
- **왜 지금인가**: 리비전은 통상 2–3개월 뒤에 온다. 지금 걸면 질문이 올 때 답이 손에 있고,
  안 오면 안 쓰면 된다. 결과가 어떻게 나오든 우리에게 불리하지 않다
  (값 유지 → 수렴 확인 / pocket 소멸 → 문헌 일치 / 값 변동 → 투고 중에 알게 된 것).
- **함께 돌릴 것 — 3자리 스캔 (2026-08-12 추가)**: 우리 4층 슬랩의 최소점은 실측상
  **on-Li** 다 (사용자 육안 확인 + 배위 실측 + 2026-06-09 db 판정, 카드 §C7).
  문헌 [54]는 on-N 이 우물. 어느 쪽이 맞는지는 **atop-N / bridge 두 자리 구속이완**이면
  결판난다 (on-Li 는 min4 로 이미 있음). adatom xy: atop-N (7.560252, 0.150836),
  bridge (6.517350, 1.643699). 같은 두 자리를 6층에서 반복하면 두께 축까지 동시에 닫힌다.
- **상태**: 미착수. 입력 미생성. **원고 v5 는 자리 이름을 쓰지 않는 방향으로 회피 중** —
  리비전에서 물어보면 이 4런이 답이다.

---

### R. ✅ **litdb 인덱스 미편입 5편 + MLIP 3부작 비교표 — 닫음 (2026-08-19)** — 본문은 `## ✅ 닫힌 항목` 절. 앵커값 UMA 힘 MAE **30.0 meV/Å** (`db/properties/mlip_bench_li3ps4_uma.json`). ⚠ 구조적 원인(`--check` 를 세션 마감 절차에 넣기)은 **여전히 미결**이다.
---

### S. ✅ **U(Ni 3d) = 6.2 eV 의 원전 — 닫음 (2026-08-23, 신설 당일)**

- **무엇** — SDCP 원고 v5 SI Table S1 의 `Hubbard U (Ni 3d) = 6.2 eV` 만 Source 가 비어 있다.
  `kb/methodology/terminology_register.md` §42 가 이미 *"⚠ 원전 미보유(Dudarev)"* 로 기록.
- **왜 지금 문제인가** — 2026-08-23 지도교수 지시: *"영률 수치같은거 그런거는 뭘 참고해서
  쓴 거면 있어야지."* 정량값에 출처를 요구하는 규칙에 이 한 값이 걸린다.
- ✅ **닫힘 (2026-08-23)** — gabia 에서 `check_ldauu_provenance.py` 실행, **MATCH**:
  ```
  [API.MPRelaxSet.CONFIG]  Ni U = 6.2 (F/ · O/)
  O-group 대조: {'Co': 3.32, 'Mn': 3.9, 'Ni': 6.2, 'Fe': 5.3}
  ```
  O-group 네 값이 **MP 파라미터 세트 그대로**라 우연 일치가 아니다.
  ⇒ Table S1 의 Source 를 `Ref. S3, S4` 로 채웠다 (S4 = Jain 2011).
  Wang–Maxisch–Ceder *PRB* **73**, 195107 (2006) 은 그 U 세트의 방법론 조상 —
  심사에서 더 요구하면 그때 추가한다.
- ⚠ **남는 것** — 이 확인은 "6.2 이 이 계에 옳다" 를 말하지 않는다. U 민감도(4 vs 6.2)는
  여전히 미실시다.
- **닫는 방법 (1분)** — 우리 6.2 가 Materials Project 기본값과 같은 값인지 확인:
  ```bash
  # gabia (SDCP 계산이 있는 곳) — repo 는 /data/work/repo, uma env
  ssh root@121.78.116.27
  cd /data/work/repo && git fetch origin
  git show origin/claude/md-status-monitoring-q2xbu1:tools/sdcp/check_ldauu_provenance.py > /tmp/chk.py
  python3 /tmp/chk.py          # rc 0 MATCH / 1 MISMATCH / 2 확인불가
  ```
  - **MATCH** → 인용 후보 Wang–Maxisch–Ceder *PRB* **73**, 195107 (2006) ·
    Jain *et al.* *PRB* **84**, 045115 (2011). 생성기
    `docs/manuscripts/sdcp_dft_methods_build.js` 의 `ROWS`·`REFS` 각 한 줄만 고치면 끝.
  - **MISMATCH** → 출처가 MP 가 아니다. Source `-` 유지하고 **그 사실을 카드에 기록**.
- ⚠ **이 확인은 "6.2 이 이 계에 옳다" 를 말하지 않는다.** U 민감도(4 vs 6.2)는 미실시 —
  심사에서 물으면 별개 계산이다.
- 관련: 항목 P (SDCP·PTFE 자리 선호) · `kb/syntheses/sdcp_eads_revision_defense_2026_08_23.md`
- 도구: `tools/sdcp/check_ldauu_provenance.py` (`--selftest` 7/7, 음성 경로 포함)

## 📄 PDF 확보 대기 (원전 미보유 — 웹/재인용 딱지 상태)

| # | 서지 | DOI | 왜 필요한가 |
|---|---|---|---|
| ~~1~~ | ✅ **확보·다이제스트 완료 (2026-07-28)** de Klerk et al. | 10.1021/acs.chemmater.6b03630 | digest: deklerk2016_diffusion_site_disorder_argyrodite.md — 75%는 min-rate 지표·비단조·단일 배열이었음이 판명. ✅ SI 통합 완료(2026-07-28) — Tables S1-S3 전표 수록, figure-read 값 SI 정밀값으로 교정(75/50 비 1.99x 확정, 300K σ* Cl 최대 교정) |
| 2 | Adeli et al., Angew. Chem. Int. Ed. 58, 8681 (2019) | 10.1002/anie.201814222 | Li5.5PS4.5Cl1.5 실험 원전 (9.4 mS/cm) — modelc Cl-rich Rietveld 점유율 ground truth |
| 3 | Deng, Wang, Chu, Luo, Ong, J. Electrochem. Soc. 163, A67 (2016) | 10.1149/2.0061602jes | SQS 반례 원전 (A=0.92) — ordered_vs_disordered 문서 '경계 사례' 논증의 원본 |
| ~~4~~ | ✅ **확보·다이제스트 완료 (2026-07-28)** Kim et al., Nano Energy 124, 109436 | 10.1016/j.nanoen.2024.109436 | **신규성 판정 완료**: enumerate 6 특성배열+단일 random supercell, config-분산 오차막대 **없음** → 우리 다중 config×멀티시드 산포 보고는 신규 기여로 원고 기재 가능 (digest: kim2024_mtp_argyrodite_disorder_gb.md) |
| ~~5~~ | ✅ **확보·다이제스트 완료 (2026-07-28) — 단 귀속 오류 판명** Schlem et al. AEM 1903719 | 10.1002/aenm.201903719 | 실물 = **Li3MCl6(Y,Er) 기계화학 논문, LPSCl 데이터 0건** → 'ordered 0.25' 앵커 철회, li_transport 정정 완료. '무질서=공정변수'의 최정밀 외부 실증(Er 무질서 88→2.5% 연속 조절)으로 가치 전환. **신규 미결: LPSCl 0.25/0.22의 진짜 원전 추적** (후보: Schlem 2019 계열 argyrodite 논문 — 서지 확인 필요) |
| (6) | Kim rapid-thermal (10.2 mS/cm, liu2022 재인용) | liu2022 참고문헌에서 확인 | 공정–무질서 관계 보강 (우선순위 낮음) |
| 7 | **Chouchane, Yao, Cronk, Zhang, Meng**, "Improved Rate Capability for Dry Thick Electrodes through Finite Elements Method and Machine Learning Coupling", *ACS Energy Lett.* **2024, 9, 4** | (미확인) | **DEM/미세구조 트랙 직접 선행** — `Library of Real Particles → Stochastic Generation → FEM → 입자별 평균 SOD → Random Forest` 워크플로. Chouchane 은 ARTISTIC(Franco) → Meng 계보. `talks/moon2026_cau_...` 슬 32가 "Reference Work"로 인용. 2026-08-03 덱 재판독으로 발견 |

확보 시 "논문 에이전트"(litdb-curator)로 다이제스트 → 서베이 ⚠딱지 승격.
진행: #1 de Klerk·#2 Adeli·#3 Deng·#35쌍·#36쌍(Schlem 추정) — 2026-07-28 큐레이터 5기 가동.

### 스크리닝 방법론 논문 위시리스트 (지도 피드백 "co-doping screening develop" 지원)

| # | 서지 | DOI | 왜 |
|---|---|---|---|
| S1 | Xiao, Wang, Ceder et al., *Joule* 3, 1252 (2019) "Computational screening of cathode coatings" | 10.1016/j.joule.2019.02.006 | **cascade의 직계 조상** — 양극 코팅 HT 스크리닝의 표준 프레임 (안정성+ESW+수송 게이트) |
| S2 | Zhu, He, Mo, *ACS Appl. Mater. Interfaces* 7, 23685 (2015) | 10.1021/acsami.5b07517 (구기재 5b01004는 오기 — PDF 실물 확인) | **grand-potential ESW 방법 원전** — 우리 oxidation CSV가 쓰는 바로 그 방법 |
| S3 | Richards, Ong, Ceder et al., *Chem. Mater.* 28, 266 (2016) "Interface stability" | 10.1021/acs.chemmater.5b04082 | pseudo-binary 계면 반응성 — MLIP 캠페인 ①(Li\|SE)의 열역학 짝 |
| S4 | Sendek et al., *Energy Environ. Sci.* 10, 306 (2017) "12k candidates" | 10.1039/C6EE02697D | **ML 스크리닝 대표작** — TabPFN 노선의 선행, 발표 인용 앵커 |
| S5 | Kahle, Marcolongo, Marzari, *EES* 13, 928 (2020) HT-AIMD 스크리닝 | 10.1039/C9EE02457C | AIMD 기반 HT의 방법 규율 (수렴·통계) — 우리 MD 규율과 대조 |
| S6 | Fujimura et al., *Adv. Energy Mater.* 3, 980 (2013) | 10.1002/aenm.201300060 | ML×전도도 예측의 원조 — 역사 앵커 |
| S7 | Ong et al., *EES* 6, 148 (2013) Li₁₀±₁MP₂X₁₂ family | 10.1039/C2EE23355J | 조성족 치환 스크리닝 원형 (LGPS M/X 스캔) |

## 🧠 ML 후속 (트리거 대기 — 데이터 나오면 전체 진행)

> 랩 PPT(TabPFN) 판독에서 나온 계획: kb/projects/ml_opportunities_from_lab_ppt_2026_07.md.
> 각 항목은 **트리거 조건**이 충족되면 착수한다.

### M1. TabPFN 벤치 — codoping 비선형 타깃
- **트리거**: 없음 (지금 가능 — 로컬 WSL/kgy GPU 반나절).
- 내용: champions Δe_post_anneal · litransport bvs proxy를 조성 특징에서 TabPFN으로
  예측, 현행 numpy ridge와 LOOCV 성능표 비교 → 사이트 ML 탭에 병기.
  근거: litdb hollmann2025 (≤10k행/500특징 스윗스팟, 튜닝 0).
  + [Sendek17 선례 이식] X-randomization(랜덤 대비 농축배수로 보고) + cR²_p
  유의성 — 소표본(그들 40 ≈ 우리 47) 정직성 지표의 인용 선례 확보.

### M2. pair CV를 leave-one-dopant-out으로 (codoping_ml v2.1)
- **트리거**: 없음 (코드 수정만).
- 내용: 같은 도펀트를 공유하는 쌍(A–B, A–C)은 비독립 — pair 단위 CV는 누수.
  랩 PPT의 Group-CV 관행 대조에서 발견한 우리 구멍.

### M3. TabPFN 역설계 루프 1회전 → 첫 실측 라벨
- **트리거**: M1 완료 + gabia GPU 여유 (comp1 seeds 종료 후).
- 내용: 가상 후보(1081쌍 × 농도축) TabPFN 스코어링 → 불확실성 페널티로 상위 5쌍
  선별(winner's curse 완화 — [Sendek17]의 적용영역 d/ε/A 3지표가 기성 구현체,
  P_LR vs d 그림 양식 그대로 이식) → UMA 공동치환 슈퍼셀 검증 = codoping 첫 라벨.
  mlip_next_campaigns ①(Li|SE 계면)과 후보 공유.

### M4. disorder 서러게이트 (active learning)
- **트리거**: disorder ensemble d×cfg 표본 ≥ 9 (현재 3). ~~Kim 2024 PDF~~ ✅ 확보 완료(2026-07-28) — 기술자 설계 시 그들 E_rel·Boltzmann 가중 방식 참조 가능.
- 내용: 배열 기술자(anti-site 분포·Ewald·BVS 채널%) → D 예측, 다음 cfg 선택에 사용.

### M7. MD 프로토콜 업그레이드 2건 (Kahle 2020 이식)
- **트리거**: comp1 멀티시드 수확 시 함께 적용 (코드 반나절).
- 내용: ① MSD 피팅창 t'-스캔 1회 검증(우리 2-50 ps 고정창이 창 길이에 둔감함을
  데이터로 입증 — Kahle Fig S3 양식) ② Ea에 Bayesian 오차 전파(현행 시드 std 보완).
  근거: kahle2020 digest §3 — per-material 자동 수렴판정·블록 분산 SE의 원전.

### ~~M6~~. ✅ cascade 양극 반응성 게이트 — **완료·판정 완료 (2026-08-20)** — 본문은 `## ✅ 닫힌 항목` 절. 판정 요지: 게이트가 **vacuous**(unique_kill 0) — 맞는 물리가 변별을 주지는 않는다.

### M5. P2D 물성 export 인터페이스 (랩 P2D 데이터셋과 동기화)
- **트리거**: 랩 후막 전고체 P2D 데이터셋 스키마 확정 (다음주 랩 계획).
- 내용: db/properties(σ·E·ESW)를 P2D 입력 파라미터 포맷으로 내보내는 export —
  DFT(우리)→P2D(랩)→TabPFN 멀티스케일 연결. ⚠ σ는 MLIP 상한임을 명시 필수.

## 🎤 심포지엄 대응 (2026-07-28 신설 — T1–T8)

전지기술 심포지엄 2026 기술세션 3-3(이상욱, 성균관대) · 3-4(문장혁, 중앙대) 덱 분석에서 나온 실행 항목.
전체 근거·좌표는 **`kb/projects/symposium_2026_competitive_analysis.md`**,
digest는 `litdb/talks/`, 벤치마크 수치는 `db/properties/external_benchmarks_symposium_2026.json`.

| ID | 항목 | 왜 (우리 약점/기회) | 비용 | 우선 |
|---|---|---|---|---|
| **T1** | **UMA 외삽 대리지표 설계** (재정의 2026-07-28 · **원전 확인 2026-08-26**) | 우리 MLIP-MD는 **스냅샷 수준 외삽 판정이 전무**하다. ⚠ 이상욱 랩의 γ(=γ_select 2 / γ_break 10→5→2)는 **MTP 선형 기저 위 maxvol·D-optimality 정의**라 UMA(비선형 등변 GNN)로 **숫자를 그대로 옮길 수 없다** (⚠ *"정의 자체가 없다"* 는 2026-08-26 에 **과했던 것으로 판정** — 아래 🔴 참조). 이식할 것은 논리뿐: ①대리지표 하나 정한다 ②**선별 문턱과 중단 문턱을 분리** ③중단 문턱을 조여 수렴 판정. 후보 대리지표: 궤적 스냅샷 UMA vs DFT 단일점 오차 분포 / 앙상블 분산. 🆕 **2026-08-26 · Shapeev 2016 본문 확인** (`litdb/papers/shapeev2016_moment_tensor_potentials.md`): **⛔ 그 논문에 γ 는 없다** (전수검색 `active learn`·`maxvol`·`D-optimal`·`extrapolat`·`grade` 전부 0회 — 학습이 100 % passive). ⚠⚠ **그 논문의 `γ` 는 ℓ₂ 정칙화 파라미터**(`Table 5.1` MTP₁ 3·10⁻⁹ / MTP₂ 0) — **외삽등급과 섞으면 T1 이 통째로 틀린다**. **확보한 것 = γ 의 전제**: `V = Σ_α c_α B̃_α(u)` 는 **계수에 선형**이고 학습이 `Xc = g` 라 **설계행렬 `X` 가 존재**한다 ⇒ *"MTP 에는 `X` 가 있다"* 를 **원전으로** 쓸 수 있게 됐다(전엔 덱 숫자뿐). 🔴 **그러나 여기서 *'UMA 에는 정의 불가'* 로 넘어가면 근거를 넘는다** (2026-08-26 정정 — Shapeev 2016 판독만으로 내린 결론이었다): **Gubaev 2019 본문이 정반대를 말한다** — *"As the model in this paper has a **nonlinear dependence on its parameters**, we apply a **generalization of the D-optimality criterion to the nonlinear case**"*. 즉 **비선형 모델로 가는 길이 이미 논문에 있다.** ⇒ 현재 판정: **정의는 일반화될 수 있고, 우리를 막는 것은 `X`의 부재가 아니라 OMat24 훈련셋을 우리가 갖고 있지 않다는 것**(실무적 장벽). 이 편이 T1 에 **유리하다** — *"원리적으로 불가"* 가 아니라 *"대리지표를 세우면 된다"* 가 되기 때문이다. ⚠ 확정은 **Gubaev 2019 · Podryabinkin 2017 본문 판독 뒤**(둘 다 inbox 대기). 그 전까지 어느 쪽도 원고에 쓰지 않는다. **추가 논거**: MTP 는 기저 수 `#A` 를 42→9,300 으로 키워 힘오차를 5배 낮출 수 있는데(`Fig. 5`, `(#A)^−0.227`) **UMA 엔 그 손잡이가 없다** ⇒ 우리 신뢰 논증은 *"수렴을 보였다"* 가 못 되고 *"범위 안임을 보였다"* 여야 한다 = **T1 이 필수인 이유**. **남은 것**: γ 문턱(2 · 10↔5↔2)의 정본 — **Podryabinkin & Shapeev 2017**(CMS 140, 171–180) 유력하나 **본문 미확인**. 확보 전까지 문턱 숫자의 출처는 **덱(citable=no)** 뿐 | 중 | **1** |
| **T7** | **3계층 스킬 로딩** (Level 1 YAML 메타 ~100토큰 신설) | 우리는 Level 2만 있다(CLAUDE.md + tools/). 매 세션 전체를 훑는 구조적 이유 | 소 | **1** |
| **T2** | **ICOHP 기반 P–S 약화 기술자** | `air_hsab` 정성 tier를 정량으로. 그들은 양성자화 시 ICOHP −6.43 → −4.69 eV (27% 약화) | 중 | 2 |
| **T4** | **반응좌표 기반 검증셋** | pre-mixing→reactants→TS→products 단계별 UMA vs DFT 단일점. 학습이 아니라 **검증**으로 전용 | 소 | 2 |
| **T5** | **영역분해 MSD** | 계면/벌크 구획 마스크로 D 분리. 기존 파이프라인 확장만 | 소 | 2 |
| **T3** | **Li\|LPSCl 반응 MD (UMA)** — 프로토콜 확정 | 완전 공백 축. **셀** Li(100)‖LPSCl(100) 직접접촉, 횡단면 ~3 nm², Li 6 nm ‖ LPSCl 10 nm (~7,000원자), NVT **350 K**, **≥20 ns**. ⚠ **우리 표준 200 ps로는 결정 핵생성(11 ns)을 절대 못 본다 = 결과가 없다.** 비용 초과 시 [두께 절반 + 20 ns] > [두께 유지 + 2 ns]. **1순위 관측량은 D가 아니라 잔존 PS₄ 층수 vs 시간**(z-bin + P–S 거리컷; **층 간격 ≈0.5 nm = a/2** 로 nm 환산 — 2026-08-04 검산). 착수 전 게이트: 1 ns UMA MD → 20 ps 스냅샷 → QE 단일점 대조 (UMA는 Li 금속‖황화물 반응 영역에서 검증된 적이 없다 — Li₃N 편향 전례). 벤치마크: interphase ~11 nm · Li₂S 결정화 · D비 0.36. **★★ 2026-08-26 — 벤치마크 3줄에 실험 쪽 불확도를 달았다** (Luo 2022 원논문 본문+SI 정독, `litdb/papers/luo2022_cryotem_li_dendrite_sulfide_interphase.md` §11b): **① interphase ~11 nm** — 대조군인 실험 cryo-TEM `~12 nm` 는 **덴드라이트 1개·시야 1개·측정 화살표 1개**이고 **오차막대·s.d.·N 이 하나도 없다**; 게다가 실험 계는 **평면 Li 슬랩이 아니라 셀을 단락시킨 단일 Li 덴드라이트를 기계적으로 뜯어낸 껍질**(HRTEM 시야에 LPSCl 이 없다 → **12 nm 는 하한일 수 있음**), 조건은 **25 °C·48 h**(우리 350 K 와 다름), 두 온도 시료는 **전착 전하량이 ~4× 다르다**(0.4 vs 0.6 mA cm⁻²). ⇒ 🔴 **"11 vs 12 nm 일치" 를 정량 일치로 쓰지 않는다 — 허용은 "같은 자릿수(10 nm 급)" 까지.** **60 °C 두께 숫자는 원논문에도 없다**(비정질 바깥층 `~3 nm` 뿐). **② Li₂S 결정화** — 여기는 **오히려 단단해졌다**: 실험(0.33 nm (111) fringe + FFT + Raman 372 cm⁻¹)·MTP MD·우리 열역학 3산물이 **서로 다른 이유로 "결정상은 Li₂S 하나"** 로 수렴한다 ⇒ **T3 성공 판정 1순위를 두께가 아니라 이쪽으로 옮긴다.** ⚠ 단 실험의 상 동정은 **d=0.33 nm 하나뿐**(EELS/EDS/SAED 0건)이고 **지지막 graphite (002)=0.335 nm 와 사실상 구별 불가** — 동정을 살리는 것은 TEM 이 아니라 **Raman** 이다. **③ D비 0.36** — 실험 쪽 대조값이 **아예 없다**(Luo 에 확산계수 0건). 계산-계산 대조로만 남는다. **④ 신규 T3 관측량**: Luo 에 따르면 고온(60 °C)은 **다핵 → 다결정 → 입계** 영역이고 우리 350 K 는 그보다 더 높다 ⇒ T3 계면상이 **다결정·비균일이어도 정상**이다. **"결정립 개수/배향 분산"을 관측량에 추가**한다(z–t 밀도 열지도만으로는 안 잡힌다). **⑤ 시간척도 경고**: Luo 의 AIMD 는 500 K·**8 ps** 에 결정 Li₂S 가 생겼다 주장하지만 MTP 는 350 K·**11 ns** — **1,000× 충돌**. 우리는 Luo 계산부를 채택하지 않는다. **★ 2026-08-04 실물 검증 추가**: ① **구획 마스크를 "계면 ±d"로 잡지 말 것** — 결정 Li₂S 핵은 **계면에서 LPSC 쪽 ~3 nm 안쪽(z≈75 Å, 초기 계면 z≈105 Å)**에서 시작한다 → **LPSC 쪽 0–5 nm 를 독립 bin** ② **초기 접촉 간격·평형화 프로토콜을 명시**할 것 (원논문은 *"direct contact"* 한 마디뿐, 이완 절차 0줄 → "즉시 분해"가 초기 배치 의존일 수 있음) | 대 | **2** |
| **T8** | **P2D 파라미터 export** (=M5) | 문장혁 랩 발표로 **소비자가 특정됨**. 우리가 파라미터 생산, 그들이 셀 스케일 소비 | 중 | 3 |
| **T6** | **litdb 그래프층** | 멀티홉 가설 생성 부재. digest **위에** 얹기(대체 아님) — 방법 맥락·인용금지 규칙 보존이 조건 | 중 | 4 |

**하지 않기로 한 것**: CSP(문제설정 다름) · 자체 MLIP 학습(UMA 횡단 속도가 우리 강점) ·
셀 스케일 FEM(상하류 관계 유지).

### T9–T12 — 이상욱 랩 논문 실물에서 추가된 항목 (2026-07-28)

| ID | 항목 | 근거 (논문 실물) | 비용 | 우선 |
|---|---|---|---|---|
| ~~**T9**~~ | ✅ **완료 (2026-07-28)** — 계면 상대 5종 {양극 만충/반충, **SE(LPSCl)**, **Li 음극**, LiNbO₃ 대조} 47종 전수 | **M6의 'vacuous' 판정을 우리 데이터로 확정 반증.** 축별 탈락: 양극 만충 **2** · 반충 **3** · **SE 29** · **Li 음극 35** · LNO 4. 코어 생존자 **11 → 3종**(CaF₂·LiF·MgO). 앵커 재현도 정확 — LPSCl vs Li −541.5 (Lee 2024 Li₆PS₅I −539.2, 0.4% 차) · vs LNO −108.8 (−107.5, 1.2%). 상세: **판정 이력 V1** | — | ✅ |
| ~~**T10**~~ | ⛔ **폐기 (2026-07-28)** — E_hull 필터가 우리 풀에서 무력 | **예측이 빗나갔다.** hull ≥ 50 meV 탈락 **0종**(최대 CrO₃ 46, 나머지 ~0). 원인은 기준이 아니라 **풀**이다 — 47종이 애초에 안정한 흔한 이성분 화합물로 큐레이션돼 있어 어떤 열역학 안정성 기준도 통과한다. → 음성 결과를 `pool_provenance` 논증의 **정량 근거**로 전환. ⚠ '안정성이 안 중요하다'가 **아니다** — 발견 깔때기(Kim 2026은 ECW에서 94.3% 제거)에선 압도적으로 센 게이트고, 우리 풀은 그 단계를 이미 통과한 상태에서 시작할 뿐. 상세: **판정 이력 V2** | — | ⛔ |
| **T11** | 🔶 **부분 완료 (2026-07-28)** — pseudo-binary ΔE_H₂S 47종 계산됨 | 최악군이 전부 알칼리·알칼리토 산화물(Na₂O −192 · BaO −160 · SrO −116 · Li₂O −108 · CaO −74 meV/atom)로 화학적으로 타당. 불화물은 전부 0 근처. Li₂O·CaO는 SE 축에서도 탈락 = 두 축이 같은 화학을 다른 각도에서 본다. **⚠ 남은 것: host LPSCl 자체의 ΔE_H₂S 기준선** — 없으면 '개선인지'를 말할 수 없다. ⚠ 이상욱 랩 반응 MD(SevenNet 500 ps, ICOHP, Sn 유인)와 **같은 것이 아니다**(0 K 열역학 vs 동역학) | 소 | **1** |
| **T12** | **van Hove 상관함수** MSD 파이프라인 추가 | Lee 2024 Fig 3e: "cage에 갇힘 vs 자유 확산"을 MSD 기울기가 아니라 **거리–시간 지도**로 판별. 우리 disorder_ensemble의 "ordered frozen" 판정을 선명하게. **✅ 도구 확정 (2026-08-04 ESI): `pymatgen-diffusion`**(Note S4, Zhu 2015) · G_s/G_d 분해 eq S4 — 그들도 **G_d 결과는 미게재**라 우리가 G_d 를 그리면 그 자체로 신규. ⚠ 도입 시 **컬러 정규화 기준 명시 필수**(§11-N8). ⛔ **2026-08-04 [Jun22] 본문 실물 검증 — 판정축은 self-part 한정**: Jun 2022 Fig 4(c) 는 **σ 가 10⁴ 배 다른 세 배열의 G_d 지도가 육안 구별 불가**였다(§20.7). G_s 는 갇힘을 확실히 가르지만(⚠ 띠 중심 ~4 Å, 5 Å 은 상한) **G_d 는 전도도 판별력이 없다** → 우리 게이트 판정에는 **G_s 만** 쓰고, G_d 는 협동성의 정성 서술로만. `[Lee24MO]`·`[Kim25CSP]` 에 이어 **3건 연속 같은 방향** | 소 | 2 |
| **T14** 🆕 | **Li–(S,Cl)₄ CSM(연속대칭척도)을 기존 UMA-MD 궤적에 후처리** (2026-08-04 신설) | Kim 2025 CSP 본문 실물 검증(`kim2025_csp…` §19 N5): 그들의 인과사슬 `edge-sharing → 왜곡↑ → D↑` 에서 **첫 화살표는 Li₄SiGeS₆에서 끊기고 뒤 고리(CSM↔D)만 남는다** — Fig 5b 최고 CSM(5.5–6.0)은 edge 가 아니라 **corner rank 8·9·10** 이고, 그 셋이 Fig 3d 에서 **corner 중 유일하게 D≠0**. → **CSM 은 연결방식의 부산물이 아니라 독립 기술자**이므로, corner/edge 축이 정의되지 않는 우리 host 에서도 **의미가 있다**. 구현은 pymatgen `chemenv` 또는 SI eq 10 직접(≈30줄), **새 시뮬레이션 0**(기존 600 K 궤적 재사용). BVSE 채널 % 와 **교차검증** — 두 지표가 어긋나는 도펀트 자체가 결과. ⚠ 그들은 **같은 조성 안 폴리모프 줄세우기로만 검증** → 47종 횡단 사용은 논문 미검증 용법, "농도별 상대 지표"로만 | 소 | 2 |
| **T15** 🆕 | **순위·비율 주장에 "시뮬레이션 온도의 D" 를 의무 병기** (2026-08-04 신설) | Kim 2025 LYC 본문 실물 검증(`kim2025_li3ycl6…` §20a·N1): Fig 4 의 600 K 총 MSD 는 기보고 4골격이 **92–115 Å² = ±12 %** 인데 300 K 외삽 σ 는 **3.4–18.8 = 5.5×** 로 벌어지고, **hcp_2 는 600 K 최속인데 300 K 에선 밑에서 둘째로 순위가 뒤집힌다**. 즉 논문 제목 주장("hcp > ccp")이 전부 **외삽이 만든 것**인데 Ea 는 본문에 한 개도 없다. 같은 논문의 antisite 축도 동일(600 K 총 MSD 103 → 108 인데 σ 12.6 → 3.6). **우리도 600/800/1000 K → 300 K 외삽이라 노출이 같다.** → 규율: σ 비교표·그림에 **T_sim(600 K)의 D 열을 함께** 싣고, `D(600 K)` 서열과 `σ(300 K)` 서열이 어긋나면 **그 불일치를 결과로 기술**한다. 첫 적용 대상 = **Nd σ-drop 0.52×**(Ea 0.224≈0.227 불변 → prefactor 지배 서사가 600 K D 에서도 보이는지). 구현은 `tools/ionic/` 기존 산출물 재집계 = **새 시뮬레이션 0** | 소 | **1** |
| **T16** 🛠 | **다원자 음이온 회전 자기상관을 기존 궤적에서 후처리** (2026-08-26 신설 · **2026-08-28 도구 완성** `tools/ionic/anion_rotation_acf.py`, selftest 20건 — 돌리는 것만 남았다. 도구가 τ 를 내는 조건이 셋 다 갖춰져야 한다: 강체 아님 · 고원(libration) 아님 · **τ 가 창의 50 % 이내**. 셋 중 하나라도 걸리면 τ 대신 사유를 낸다) | `shin2026_bh4_reorientation_li_transport_li6ps5x` 실물: ⁷Li 와 ¹¹B 의 SLR **Ea 가 세 시료 모두 0.01 eV 이내로 붙고 함께 움직이는데 ³¹P 만 따로 논다**(Li 0.27/0.29/0.35 · B 0.28/0.30/0.34 · P 0.18/0.16/0.16). 그리고 **회전 자유도만 얼린 대조 MD 에서 D(500 K)가 네 배열 전부 2.0–3.0배 감소** (`Table S9`) — 인과 증거다. **우리 축엔 회전 자유도가 아예 없다**(정적 기술자만: 자리·채널·BVSE·blocking). **구현 = 새 시뮬레이션 0회**: 필요한 것은 P–S 결합벡터 시간열뿐이고 우리 궤적(600/800/1000 K · 200 ps · dt 2 fs)에 이미 있다. 배향 자기상관 C_ℓ(t) → τ_rot → Ea_rot 를 뽑으면 **¹¹B SLR 의 계산 대응물**이 되고 우리 Li Ea 와 **같은 단위로** 비교된다. T12(van Hove)·T14(CSM)와 같은 "기존 궤적 재사용" 계열. ⚠ **한계 — 우리 host 엔 BH₄ 가 없다.** 우리가 잴 수 있는 것은 PS₄ 회전이고 그건 그 논문이 **"안 돈다"고 판정한 대상**이다 ⇒ "PS₄ 느리다"가 나와도 **재확인이지 신규가 아니다**. **신규가 되려면** Cl 함량(comp1→modelc) 의존성이나 **우리 도펀트(B₂O₃·O 치환)가 PS₄ 회전을 바꾸는지**를 재야 한다 — 거기가 문헌 공백이다. ⛔ **BH₄ 를 cascade 도펀트 축에 넣는 것은 별개 문제이고 지금은 못 한다**: BVSE 에 **Li–BH₄ R0 파라미터가 없고**, 다원자 회전체를 점 이온으로 뭉개면 이 논문 결론을 **원리적으로 못 본다**. UMA 도 음성테스트 선행 필요(Li₃N 전례 · B–H 신축 주기 0.01–0.03 ps 라 dt 2 fs 가 아슬아슬) | 소 | **2** |
| ~~**T13**~~ ✅ **완료 (2026-08-29 · ⏭-1)** | ~~MSD 생산길이 200 ps 의 타당성 재검토~~ (2026-08-04 신설) | Lee 2024 ESI 실물: 그들은 **NPT 10 ns = 우리의 50배**. 우리 창(2–50 ps)이 고정이라 길이 자체가 곧바로 치명적이진 않지만, **느린 계에서 창 안의 유효 hop 수가 충분한지** 점검이 필요. 참고로 그들 Fig S5(a) 는 10 ns 에도 MSD 26 Å²(RMS ~5 Å)에 그친다 — **길이만으로 해결되지 않는다**는 반증이기도 하다 | 중 | 3 |

> 🔑 **T9·T10·T11은 셋 다 비용이 작고 셋 다 우리 깔때기의 약점을 직접 친다.** M6 인프라를
> 그대로 재사용하므로 묶어서 한 번에 돌리는 것이 맞다.

> 🔁 **2026-08-04 · Lee 2024 ESI 29 pp 실물 검증이 T10·T11 의 성격을 바꿨다**
> (`litdb/papers/lee2024_multicomponent_argyrodite_mixed_oxidation_mtp.md` §12):
> - **T10 (E_hull)** — 이미 V2 로 폐기됐지만, **애초에 베낄 레시피 자체가 없었다**:
>   ESI 29 pp 전체에서 `hull`·`convex`·`synthesiz` 검색 **0회**. 어떤 상도표·참조 DB·functional 로
>   hull 을 잡았는지 **본문에도 ESI 에도 기술이 없다.** → 폐기 판정과 무관하게, 이 논문을
>   **E_hull 방법 출처로 인용하면 안 된다.**
> - **T11 (ΔE_H₂S)** — ⛔ **'그들 Table S4 값을 이식한다'는 선택지가 사라졌다.**
>   ESI Table S3/S4 를 85행 전수 전사해보니 **할로겐을 분해하지 못한다**: Cl↔Br 8쌍 중 **7쌍 계면
>   3값 완전동일**, D₁.₅ 혼합비 뒤집기 **7/7 완전동일**, I/Cl/Br 3종 통째 동일 골격 4개
>   (그런데 같은 묶음 σ 는 최대 **3.18×** 차). 우리 축은 **Cl-rich** 이므로 **직접 계산 필수로 승격.**
>   ✅ 다만 우리 T9 앵커 재현(−541.5 vs −539.2, −108.8 vs −107.5)은 **여전히 유효**하다 —
>   그 앵커는 **모체 Li₆PS₅I 단일 조성**이라 할로겐 분해 문제와 무관하다.
> - 전수 데이터는 `db/properties/lee2024_si_84_structures.csv`(85행), 재현 코드는
>   `tools/litdb/lee2024_si_tables_transcribe.py`.

### 🔬 T1b — **PBE 가 황화물 골격을 무르게 보는가** (2026-08-26 제안 · Y 앙상블 뒤 착수)

**질문.** b2o3 의 UMA-MD 골격 creep 이 "UMA 라서" 인가, **"PBE 계열이라서"** 인가.

**왜 지금 나왔나.** 사용자가 "MTP 로 돌렸으면 어땠을까"(이상욱 랩 사용 도구)를 물었고,
답을 찾다 `kim2024_mtp_argyrodite_disorder_gb` 가 **정확히 이 실험을 이미 했다**는 것을 확인했다:

| 학습 functional (같은 MTP 아키텍처) | 결과 |
|---|---|
| **optB88-vdW** | ✅ site-disorder 의존성 재현 · σ80 % 2.3 mS/cm (실험 2.3–2.5) |
| **PBE** | ⛔ 실패 |
| **PBE-D3(BJ)** | ⛔ 실패 |

⇒ **포텐셜 형태가 아니라 참조 이론이 갈랐다.** 우리 UMA 는 OMat24 = **PBE 계열**이다.
즉 "MTP 로 바꿨다면" 의 답은 *"PBE 데이터로 훈련했다면 같은 문제를 봤을 것"* 일 수 있다.

**물리적 가설.** 황화물 골격은 **분산력이 S···S 접촉을 잡는** 몫이 크다. PBE 는 그것을
과소평가 → 음이온 부격자가 무름 → 우리가 본 골격 creep. (D3(BJ) 도 실패한 것은
"분산을 아무거나 붙이면 되는 게 아니다" 를 뜻한다 — 아직 미해석.)

**⭐ 싼 검사 (MLIP 훈련 불필요).** 우리 b2o3 0 K DFT 는 **PBE(vdW 없음)** 였다
(`b2o3_eos_dft_result.json` "QE PBE EOS" · elastic 은 QE PAW PBE). 같은 셀을
**vdW 보정 DFT**(optB88-vdW 또는 PBE-D3)로 다시 이완하면 가설이 참일 때:

- S···S 접촉 거리가 **짧아진다**
- B₀ 가 **올라간다** (현재 PBE 값 24.48 GPa)

QE 이완 몇 개면 된다. 나오면 "PBE 계열이 황화물 골격을 무르게 본다" 가 **우리 계에서 직접**
확인되고, 그것이 UMA 아티팩트 판정의 **물리적 근거**가 된다. 지금은 근거가
"같은 UMA 로 modelc 는 7/7 rigid 인데 b2o3 만 움직인다" 는 **대조 논거 하나뿐**이다.

**⛔ 이 검사가 못 하는 것**
- 0 K 이완이 유한온도 creep 을 직접 재는 게 아니다. 부격자 강성의 **대리지표**다.
- vdW 로 B₀ 가 올라가도 "그래서 MD 가 옳아진다" 를 뜻하지 않는다 — 그건 vdW 학습
  MLIP 로 MD 를 다시 돌려야 답한다.
- functional 을 바꾸면 **정본 비교쌍이 깨진다**. 이 검사는 **진단 전용**이고,
  기존 PBE 값들을 대체하지 않는다.

**⚠ MTP 를 실제로 도입한다면의 함정** (같은 조사에서 나옴)
- **전이 안 된다.** 우리 핵심 증거가 "같은 포텐셜·같은 T 에서 modelc rigid vs b2o3 mobile"
  인데, MTP 를 조성마다 따로 훈련하면 그 대조가 깨진다 → **한 MTP 가 두 조성을 같이 덮게**
  훈련해야 한다.
- R_cut 5–6 Å 단거리 · 장거리 정전기 없음.
- 비용(Kim 2024): lev 8 = 1일 / lev 12 = 3.5일 / lev 16 = 9일 + DFT 데이터 생성 별도.
  도달 정확도 E 2.88 meV/atom · F 0.073 eV/Å (Cl 조성).

**연결**: T1(외삽 대리지표)과 같은 뿌리다. T1 은 "우리 포텐셜이 범위 밖인가" 를 재고,
T1b 는 "범위 안이어도 참조 이론이 틀렸나" 를 잰다. 둘 다 있어야 b2o3 판정이 닫힌다.

**🎙 2026-08-26 구술 판독으로 붙은 정황** (`litdb/talks/lee2026_skku_mlip_materials_design.md` §99-3)
사용자가 그 자리에서 **직접 질문**했고(A1), 답은 **"MTP = 동력학 / universal potential = static"** 이었다.
덱 슬 8 이 그 배경을 인쇄해 놓았다 — `DFT PES ──softening──▶ uMLIP PES`,
범례 *노란 점 = 평형 근처 훈련점 / 빨간 점 = 보강이 필요한 고에너지 상태*.

| | |
|---|---|
| 우리 b2o3 β≥0.60 @700 K | **universal potential 로 얻은 동역학 결과** = A1 이 권하지 않는 조합 |
| ⛔ **그런데 판정은 안 바뀐다** | A1 은 **STT 전용**(citable=no)이고, 이유가 **속도인지 PES 품질인지도 미확정**(Q-T2). 우리 근거는 여전히 modelc 12/12 · lpsocl 12/12 · b2o3 만 붕괴 라는 **우리 데이터**다 |
| ⇒ | **정황이 늘었을 뿐 증거는 그대로** → **T1b 를 실제로 돌려야 한다**(우선순위 ↑) |

⭐ **T1b 에 대조군이 하나 더 생겼다**: 슬 22 의 **fine-tuned SevenNet**(MAE_F **0.57 eV/Å**)과
슬 14 의 **MTP**(**0.073 eV/Å**). 계·훈련셋이 달라 우열 비교는 금지지만,
**"GNN 계열이 힘을 얼마나 거칠게 보는가"** 의 자릿수 감각을 준다.
→ 우리 T1 대리지표(스냅샷 UMA vs DFT 단일점)의 **합격선을 정할 때 참고 눈금**이 된다:
`MAE_F ≲ 0.1 eV/Å` 면 MTP 급, `≳ 0.5` 면 반응계 fine-tune 급.

**📄 2026-08-26 — SevenNet 원전을 받아 읽었다** (`litdb/papers/park2024_sevennet_parallel_gnn_md.md`;
Park, Kim, Hwang, Han, *JCTC* **20**, 4857–4868, 2024. 본문 12 pp + SI 5 pp 전수 + 그림 8/8 판독)

> ### 🔴 **판정: 이 논문으로 T1b 는 닫히지 않는다.**
> SevenNet 은 **NequIP 기반 등변 GNN = 우리 UMA(eSEN)와 같은 계열**이 맞다. 그러나 그 논문은
> **PES softening 을 재는 실험을 하나도 하지 않았다**: `soften` **0회** · **NVE/에너지 보존 0** ·
> **장시간 드리프트 0** · **고온 스냅샷의 MLIP↔DFT 재평가 0** · **포논·탄성 0** · **D/Ea/MSD 0** ·
> **fine-tune 전후 비교 0**. 정확도는 오직 **MP 결정 test set = 평형 근처**에서만 잰다.
> ⇒ *"softening 은 GNN 공통 성질이다/아니다"* 를 **이 문헌으로 말할 수 없다.**
> ⚠ Shapeev γ 판독에서 *"UMA 에는 γ 정의가 없다"* 로 근거를 넘어간 전례를 반복하지 않는다.

**그래도 얻은 것 — 정황 2개(둘 다 덱과 반대 방향) + 경고 1개**

| | 내용 |
|---|---|
| **정황 ①** | SevenNet-0 은 **결정 구조만** 학습했는데도(저자 명시 *"liquid or amorphous are not present in the training set"*) **5000 K 초가열 → 3000 K 평형 → −33 K/ps 급랭**으로 112,000원자 비정질 Si₃N₄ 를 만들었고 **Si 4배위·N 3배위·g(r)·g(θ)** 가 DFT 참조와 부합했다. 우리 UMA 의 **OMat24 는 AIMD·Rattled 부분집합을 포함**한다 ⇒ **비평형 방향으로 우리 훈련셋이 더 넓다.** 덱 슬 8 의 *"평형 근처 편중 → 고에너지 연화"* 기구가 결정적이라면 **더 좁게 학습한 SevenNet-0 이 먼저 무너졌어야 한다** |
| **정황 ②** | **평형 근처 힘 정확도는 GNN 과 MTP 가 동급**이다 — SevenNet-0 base **F MAE 0.070 eV/Å** vs 덱 슬 14 MTP 벌크 LPSCl **0.073 eV/Å**. ⇒ 덱 슬 22 의 **0.57 eV/Å 은 fine-tuned + H₂O 반응계**라 **아키텍처가 아니라 계 탓**일 가능성이 크다. **"GNN 계열이라서 힘을 거칠게 본다" 는 읽기는 지지되지 않는다** |
| **⚠ 경고** | **비정질 생성에서 "골격 연화" 는 원리적으로 안 보인다** — 목표 상태가 이미 무질서이기 때문. 우리 b2o3 판정 지표는 **결정 골격이 안 움직여야 하는데 움직인다**(log-log MSD β ≥ 0.60 @700 K)이고, 이건 그 논문의 실험 설계로 **검출 불가능**하다. 계도 다르다(공유결합 네트워크 SiO₂/Si₃N₄ ↔ 이온성 황화물 + 초이온 Li) |

⇒ **원래 계획은 그대로다**: b2o3 셀을 **vdW 보정 DFT**(optB88-vdW / PBE-D3)로 재이완해
S···S 접촉거리·B₀(현 PBE 24.48 GPa)를 비교한다.

⭐ **다만 값싼 최소판이 하나 생겼다 (T1 의 실행 가능한 축소판)**
b2o3 **700 K 궤적 스냅샷 몇 개**를 **UMA 단일점 vs 우리 DFT** 로 재평가해 **힘 MAE** 를 낸다.
합격선 눈금은 위 정황 ② 표가 준다 — **≲0.1 eV/Å 이면 MTP 급 / ≳0.5 면 반응계 fine-tune 급**.
⇒ b2o3 가 modelc·lpsocl 대비 **힘 오차가 유독 크면** "UMA 가 이 조성에서 범위 밖"이 직접 확인되고,
**같으면** 원인이 PES 정확도가 아니라 다른 데(참조 이론 = T1b 본류)에 있다는 뜻이 된다.

🔴 **그 논문을 읽다 새로 생긴 미확인 2건 (우리 쪽 공백)**
- **우리 UMA 의 메시지패싱 층 수 T 를 모른다.** SevenNet-0 은 `T=5 × r_c 5 Å = 유효 수용영역 25 Å`
  이라고 명시하는데, 우리 digest 에는 **6 Å cutoff 만** 있고 층 수가 없다 ⇒ **슬랩·계면 두께 설계의
  하한을 계산할 수 없다.** (확인 비용 0 — 모델 config 한 줄)
- **UMA 에 LAMMPS 다중 GPU 경로가 있는가.** 우리는 **ASE 단일 GPU** 다. T3 계획의 전제가 걸린다.

🔧 **부수 소득 — T3 비용이 처음으로 숫자가 됐다** (우리 산술, 논문 실측에서 유도)
`112,000원자 · 60 ps · 12.7 h · 8×A100` ⇒ **1.58×10⁶ atom·ps/day per A100**
(교차검증 `14,000원자 · 12.5 h · 1 GPU` = 1.61×10⁶, 저자의 효율 0.98 과 일치 ✓)
⇒ **T3-small(7,000원자 × 20 ns) ≈ 89 A100-day** · **T3-large(50 ns) ≈ 500 A100-day**.
⇒ ⛔ **gabia(A6000 1장)·kgy(RTX3090)로는 불가** — KISTI 다중 GPU 필요.
⇒ 단 7,000원자를 8장에 쪼개면 **875원자/GPU = 저이용 구간**(그 논문 `Fig. S1`·`Fig. S2`: 448원자/GPU 에서
효율 0.79, 14,000원자/GPU 에서 0.98) ⇒ **원자/GPU 를 최대화하는 편이 이득**.
⇒ **이상욱 랩이 계면 20/50 ns 를 GNN 이 아니라 MTP 로 돌린 이유의 "속도 쪽" 답**이 확보됐다
(`Q-T2` 는 **절반만** 닫힌다 — PES 품질 쪽은 이 논문이 답하지 않는다).

### ⚠ σ 절대값 규율 — 근거 재정의 (2026-07-28)

지금까지 "MLIP σ 절대값 인용 금지"의 근거는 `kim2024`(훈련 functional에 따라 σ₈₀%가 **8배** 갈림)
하나였다. `lee2024` ESI Table S1이 **반대 방향의 데이터**를 준다:

| 조성 | AIMD | MTP_optB88 | 실험 |
|---|---:|---:|---:|
| Li₆PS₅I | 0.84 | **0.001** | **0.001** |
| Li₆PS₅Cl | 4.6 | **2.46** | **2.3–2.5** |
| Li₃YCl₆ | 14 | **0.56** | **0.51** |

**optB88-MTP는 8개 계에서 실험과 잘 맞고, 크게 틀리는 쪽은 AIMD다**(Li₆PS₅I에서 840배).

→ 정확한 명제: **"MLIP σ 절대값은 (a) 훈련 functional이 그 계에 맞고 (b) 같은 물질군에서
실험 검증을 거친 경우에만 신뢰할 수 있다."**
**우리 UMA는 둘 다 미충족**(OMat24 = PBE 계열이라 optB88 아님 · 우리 계 실험 대조 없음)
→ **인용 금지 규율 유지. 단 이유가 "MLIP는 원래 못 믿는다"가 아니라 "우리 설정이 검증되지
않았다"로 바뀐다.** 규율이 약해지는 게 아니라 정확해지는 것이고, **T1의 필요성이 커진다**.

### 이상욱 랩 논문 확보 위시리스트 (사용자가 탐색·제공 예정)
| 순위 | 논문 | 왜 |
|---|---|---|
| ~~1~~ ✅ | **Nano Convergence 2026, 13, 27** — 코팅 스크리닝 (**17,230 Li·O 산화물** → Li₃Sc₂(PO₄)₃) | **확보·정독 완료** (`litdb/papers/kim2026_hts_li3sc2po43_coating_midni_ncm.md`). ⚠ 종전 표기 '17,233 Li-P-S-O'는 덱 저해상도 전사 오류 — 2026-08-03 철회 |
| 2 | **Adv. Funct. Mater.** (revision) — argyrodite 가수분해 SevenNet | T2 방법 원본. **3부작 중 유일한 공백** — Q4(H₂S 정량)+T2 가 한 번에 닫힌다 |
| **2b** 🆕 | **자료집 목차 페이지** (이상욱 섹션 앞뒤 1–2 pp) | Q-T1(다음 발표자 이름 불일치). 비용 0 |
| ~~**8**~~ 🔶 **절반 완료 2026-08-26** | ~~**Shapeev 2016** MTP (Multiscale Model. Simul. 14, 1153)~~ ✅ **확보·정독** (`litdb/papers/shapeev2016_moment_tensor_potentials.md`) + **Novikov 2021** MLIP package (MLST 2, 025002) ⛔ 미확보 | **Shapeev 2016 에서 얻은 것 = 기저·선형성·설계행렬**(T1 논증의 앞쪽 절반). **얻지 못한 것 = γ 정의 그 자체** — 🔴 **그 논문에 γ 가 없다**(전수검색 0회). ⇒ 다음 표적은 **8b: Podryabinkin & Shapeev 2017** (Comput. Mater. Sci. **140**, 171–180, arXiv 1611.09346) + Novikov 2021 |
| **9** 🆕 | **Merchant 2023 GNoME** (Nature 624, 80) | 강의 서사의 출발점(`[STT 08:02]` 2.2 M / 38만). 자체 digest 없이 참조로만 존재 |
| ~~**10**~~ ✅ | **Park 2024 SevenNet** (JCTC 20, 4857) | **확보·정독 완료 2026-08-26** (`litdb/papers/park2024_sevennet_parallel_gnn_md.md`, 본문 12 pp + SI 5 pp + 그림 8/8). **판정: T1b 는 안 닫힌다**(그 논문도 softening 미측정) · **정황 2개는 반대 방향** · **부수 소득 = T3 비용 1.58×10⁶ atom·ps/day per A100** |
| ~~**11**~~ ✅ | **Luo 2022** ACS Energy Lett. 7, 3064–3071 | **확보·정독 완료 2026-08-26** (`litdb/papers/luo2022_cryotem_li_dendrite_sulfide_interphase.md`, 본문 8 pp + SI 9 pp + 그림 10장 크로핑·5장 판독). **판정: T3 두께 벤치마크는 오차막대가 없다**(시야 1개·화살표 1개) · **60 °C 두께는 원논문에도 숫자 없음** · **부수 소득 = Li₂S 결정화 벤치마크가 오히려 단단해졌다**(실험·MTP·우리 열역학 3중 수렴) + Raman anchor 2점(Li₂S 372 / PS₄³⁻ 425 cm⁻¹) |
| ~~3~~ ✅ | ~~~~**Chem. Eng. J.** (under review)~~ → **J. Power Sources (revision)**~~ → 실물은 **SSRN preprint 6020397 (저널명 없음)** — Li\|argyrodite 계면 MTP | **확보·정독 완료** (`litdb/papers/kim2026_li_argyrodite_sei_reactive_md.md`; **본문 실물 독립 검증 2026-08-04**, inbox #3·폴더 `이상욱`). ⚠ "Chem. Eng. J. under review ⛔→ **J. Power Sources (revision)**"는 **덱 표기일 뿐 논문에 근거 없음** — 인용 시 "[Kim, SSRN preprint 6020397, 미심사]" 병기. **⛔ SI 미확보 확정** (프리프린트의 SI 링크가 공란 → 대안은 figshare 원자료 `10.6084/m9.figshare.30272386.v1`) |
| ~~4~~ ✅ | **JACS 2025, 147, 47381 — 준안정 3기술자** | **확보·정독 완료 + 본문 실물 독립 검증 2026-08-04** (`litdb/papers/kim2025_csp_metastable_edge_sharing_sse.md` §19). ⚠ **SI 24 pp 실물은 아직 미확보** — Table S1·S2, Fig S1–S12, eq 1–11 은 2026-07-28 판독 승계 |
| 5 | **Adv. Energy Mater.** (revision) — Dynamic properties 후속 | **Q5: config-variance 오차막대 추가됐나** — 우리 신규성 주장의 유효범위가 걸림 |
| 6 | Rare Metals 2025, 44, 2366 | CSP 보조 |
| 7 | arXiv:2601.04746 — BEARS 스킬 3계층 | T7 실측치 |

### 🆕 선행연구 대비 위치 규정 — 확보 예정 (2026-08-16 신설 · 사용자 제공 예정)
> 계기: 세미나 6장(`Where prior screening stops`)을 쓰다가 **"LPSCl 도펀트 계산 스크리닝
> 선례 없음" 이 사실이 아님**을 확인했다. "아무도 안 했다" 는 주장은 쓰지 않는다.
> 우리 주장은 **무엇을 바꾸는가**로만 방어한다 — 외부 이성분 화합물을 통째로 넣는다는 점,
> 그리고 기계 물성 축이 있다는 점.

| 순위 | 논문 | 왜 필요한가 | 상태 |
|---|---|---|---|
| **A1** | **Miara, Richards, Wang, Ceder — Chem. Mater. 2015, 27, 4040**<br>LLZO 가넷 **도펀트 45종 × Li/La/Zr 세 자리 결함에너지** | **우리 포지셔닝의 가장 직접적인 비교 대상.** 자리별 계산 도펀트 스크리닝의 직계 선례이고, Anderson 2024 가 이 예측을 받아 59종을 실제 합성했다. 지금은 Anderson digest 안의 **인용값(Fig 3d)** 으로만 있어 방법 세부(code·functional·셀·U)를 모른다 | 🔜 **사용자가 논문 제공 예정** — 받으면 litdb-curator 로 digest |
| A2 | Lee 2024, *J. Mater. Chem. A* **12**, 7272 — argyrodite 84 구조 MTP-MD 전수 | 황화물·MLIP·체급 유사. 이미 digest 있음(`lee2024_multicomponent_argyrodite_mixed_oxidation_mtp`) — **비교표에 이미 반영됨**. 추가 확보 불필요 | ✅ 보유 |
| A3 | Jun 2022, *J. Mater. Chem. A* **10**, 7888 — argyrodite 계산 스크리닝 기술자(ion-cage 균일도, 한양대 ERICA) | 같은 계열의 argyrodite 계산 스크리닝. digest 보유(`jun2022_argyrodite_ion_cage_size_descriptor`) | ✅ 보유 |

**A1 받으면 할 일**
1. digest 생성 → `litdb/papers/miara2015_llzo_dopant_site_defect_energy.md`
2. `litdb/comparison_vs_ours.md` 에 계보 note 추가 — 축은 **"무엇을 바꾸는가"** 하나로 고정
3. 세미나 덱 6장 표의 `Miara 2015 (via Anderson)` 행을 **직접 인용**으로 승격
   (`tools/seminar/rebuild_cascade_deck.py` SPEC 임시키 29 → 6번 슬라이드)
4. 확인할 것: 45종의 **음이온 자리 도핑이 있는지** — 없다면 "우리는 화합물 통째로" 주장이 더 강해지고,
   있다면 그 부분은 주장에서 빼야 한다

### 🔁 판정 정정 이력 (우리가 냈다가 뒤집은 판정)

웹앱 **`/benchmarks` → 판정 정정 이력**에 ①주장 →②무엇이 틀렸나 →③어떻게 알았나 →④지금 무엇을 아나
형식으로 전문 수록. 여기엔 색인만 둔다.

| ID | 무엇을 뒤집었나 | 근거 |
|---|---|---|
| **V1** | M6 계면 게이트 'vacuous' 판정 철회 — 가장 쉬운 상대(양극)만 계산한 결과였다 | Kim 2026 Table S1 + 우리 T9 전수 |
| **V2** | T10(E_hull) 예측 빗나감 — 원인은 기준이 아니라 큐레이션된 풀 | 우리 T10 전수 (음성 결과) |
| **V3** | σ 규율 근거 재정의 — kim2024만으론 절반. AIMD가 840× 틀리는 쪽이다 | lee2024 ESI Table S1 |
| **V4** | T1을 'γ 확보' → 'UMA용 대리지표 설계'로 재정의 — γ는 MTP 전용이라 정의 자체가 없다 | kim2026 SEI 실물 |

> 📌 **덱 정정 원장(외부 6건)과 나란히 둔다.** 한쪽만 있으면 정직성이 아니라 남 탓이 된다.

### 🧪 T1 진행 — 모델 위원회 (UMA + MACE-MP-0 + SevenNet-0)

- 도구 `tools/ionic/mlip_committee.py` (sample → predict×3 → analyze). **새 MD 불필요**, 기존 궤적 후처리.
- 문턱은 임의 상수를 만들지 않고 **표본 분포에서 유도**: 선별 = 중앙값×2 · 중단 = p95.
  (kim2026의 γ_select/γ_break **논리 구조만** 차용)
- 기준선 대상: `/data/work/b2o3md/modelc_full/d0.00_cfg0/T600/traj.xyz` (2000 프레임 × 62원자).
- **CPU 실행** — comp2 disorder MD가 GPU를 쓰고 있어 충돌 회피. 단일점만 하므로 CPU로 충분.
- ⛔ **이 지표는 절대 정확도를 말하지 않는다.** 세 모델이 전부 PBE 계열이라 V3의 functional 각인
  문제를 풀지 못한다 — **일치해도 절대 σ 인용 금지는 그대로**. 재는 것은 "이 배열이 훈련 분포에서
  이상한가"뿐이고, 그 목적에는 같은 functional 계열인 것이 오히려 무해하다.
- **✅ 기준선 교정 완료 (2026-07-28)** — modelc 600 K, 62원자, 200/2000 프레임, 3엔진 CPU.
  프레임 단위 중앙 **0.3175** · p95 **0.3669** eV/Å → `db/properties/mlip_committee_baseline.json`
- ⚠ **위원회 독립성이 보이는 것보다 낮다**: 쌍별 mace|sevennet **0.202** < sevennet|uma 0.215 <
  mace|uma **0.317**. **가장 잘 맞는 쌍이 훈련셋을 공유한다(MPtrj)** — UMA만 OMat24.
  불일치를 지배하는 것은 아키텍처가 아니라 **훈련 데이터**이고, 실질 **3명이 아니라 2진영**이다.
- **원소별(정규화 후)**: P 0.333 > S 0.277 > Li 0.235 > Cl 0.182.
  원시 절대값으로는 P/Cl = 5.9배였는데 정규화하면 **1.8배**로 압축된다 — 원시 순위의 대부분이
  **힘 크기**였다. 단 **순서는 살아남는다**: 모델들이 **PS₄ 골격에서 가장 덜 합의**한다.
- 🔑 **T3에 직결**: T3의 1순위 관측량이 **잔존 PS₄ 층수**인데 위원회가 가장 덜 합의하는 게 바로 그
  PS₄다. → T3 착수 게이트를 **벌크가 아니라 Li 계면 구조에서** 다시 잡아야 하고, QE 단일점 대조를
  병행해야 한다(대리지표는 DFT를 대체하지 않는다).
- 다음: ① 정적 구조(comp1 V0) 기준선 — 평형에서의 하한 ② **Li 계면 슬랩 탐지 모드** (T3 게이트)
  ③ 훈련셋이 다른 4번째 엔진 검토 ④ QE 단일점 대조 ~20 스냅샷

### ⏳ 발표 구술 txt 대기
두 발표 모두 구술 내용 txt를 받기로 함. 받으면 각 digest `§99` 를 채우고
미해결 질문(lee Q1–Q6 / **moon Q1b·Q2·Q3·Q4·Q5·Q6·Q7·Q8** — Q1은 2026-08-03 재판독으로 종결,
Q7·Q8은 재판독으로 신설)을 닫는다. **이 항목은 닫지 말 것.**

### 🆕 BEARS arXiv 확보 대기 (2026-08-03 덱 재판독 발)
`talks/moon2026_cau_...` digest Q3·Q7·Q8이 전부 BEARS/스킬 논문으로만 닫힌다:
**arXiv:2601.04748**(3계층 스킬 로딩 토큰 절감 실측치) + BEARS 본문(Validator의 **"8종 구조 검증 지표"**
목록, "40+ skills"와 에이전트별 [3]/[5]/[6]/[8] 표기의 관계). ⚠ **우리 DEM 산출 구조에도 고정 검증
세트가 없다** — 그들 8종 목록이 나오면 우리 세트 설계의 출발점으로 쓴다.

### 🆕 6월 계보 rescue 브랜치 감사 (2026-08-11, 낮은 우선순위)
컨테이너 교체 중 작업트리가 6월 계보(a90fd1c)로 갈렸다가 복구됨. 고유 커밋 7개를
`rescue/lineage-2026-06-nd-pair01` 브랜치에 보존해 푸시했고, 표본 대조(6.29 μB ·
k441/k661)로는 오늘 계보에 내용이 이미 있음 — 다만 **7커밋 전수 대조는 안 했다**.
한가할 때 rescue 브랜치 diff 를 전수 감사하고 이 항목을 닫는다. 다 있으면 브랜치 삭제.

## ✅ 닫힌 항목

> 본문에서 **원문 그대로 옮겨 온** 것들이다 (이동 2026-09-09). 판정·근거·⚠ 단서는 하나도 지우지 않았다.
> 본문 자리에는 같은 번호의 한 줄 stub 이 남아 있어 `#3`·`#7`·`§O`·`⏭-1` 같은 바깥 인용이 계속 걸린다.
> 여기 들어온 뒤에는 **재개 조건이 따로 적힌 것만** 다시 연다.

| 항목 | 닫은 날 | 한 줄 |
|---|---|---|
| ⏭-1 T13 창·길이 | 2026-08-29 | 길이는 문제가 아니었다 · 셀이 D 를 1.79배 움직인다 |
| 3 VGCF 2×2 barrier | 2026-07-30 | 209 meV 는 VGCF 쪽 98.9 % · 기전 = confinement |
| 6 LPSOCl COHP 회수 | 2026-07-29 | 회수 성공 · 곡선 면적 ≠ ICOHP (인용 제약) |
| 7 litdb 인덱스 정합 | 2026-08-06 | 손 맞춤 → 생성으로 전환 (`build_index.py --check`) |
| 10 계 표시명 통일 | 2026-08-06 | `DISP` / `DISP_LONG` 로 house_style 에 등록 |
| O Nd 갭 3종 | 2026-08-12 | frozen-4f 자체 측정 · MP 우회 폐기 |
| R litdb 미편입 5편 + MLIP 비교 | 2026-08-19 | UMA 힘 MAE 30.0 meV/Å 앵커 |
| M6 cascade 양극 반응성 게이트 | 2026-08-20 | 게이트가 vacuous — unique_kill 0 |

### ⏭-1. T13 확인 — ✅ **판정 완료 (2026-08-29)**

> ⛔ **β=0.8 하드게이트는 2026-08-26/27 폐기됐다** (`kb/concepts/beta-gate.md` §7-5·§7-8b, 회신 F). 아래 '게이트 통과/실패' 문구는 **경보값**으로만 읽는다. 판정축은 자유절편 (c, m) · 홉 수 · 다중 창이고, 도구는 2026-08-30 에 교체됐다(§7-8e). ⚠ **양방향이다** — 문턱을 내리면 '다 통과' 가 아니라 **통과했던 것도 무효**다(§7-6). (2026-08-31 전수 조사에서 붙임)
`db/properties/t13_msd_length_verdict_2026_08_29.json`
- **길이는 문제가 아니었다.** 2–50 ps 창은 200 ps 궤적 안에 들어가므로 805 ps 로 늘려도
  같은 값 — **생산길이 200 ps 는 이 창 규약에서 타당**.
- 대신 **창이 이르다**: D_inc 0.126(2–50) → 0.110(80–400), **−13.5 % 단조**.
  절대 D 인용 시 과대 방향 병기.
- 케이지/느린전이 판별은 **미판정** (잔차 0.049 vs 문턱 0.05 경계 + c↑·β↑ 가 두
  시나리오 어느 쪽과도 불일치). 다만 두 경우 다 D 는 인용 가능.
- 🔴 부수 발견: **셀 크기로 D 가 1.79배** (62원자 6.632e-06 vs 558원자 1.190e-05,
  같은 T600·805 ps). 창 편향보다 훨씬 크다 — ⏭-2 는 전 설계 **같은 셀 크기** 필수.
- ✅ **상쇄 가정 기각 (small800 --scan 완료)**: 창 편향이 계마다 다르다 —
  558원자 **−12.7 %** vs 62원자 **−20.5 %** (7.8 %p 차). 비 D_small/D_long 이
  0.619(2–50) → 0.564(80–400) 로 **9 % 이동** = D_rel 게이트 폭(0.90)과 같은 자릿수.
  ⇒ "비율이라 편향이 상쇄된다" 는 **실측으로 기각**. 처방은 기준 변경이 아니라
  **두 창 병기 민감도 보고**(같은 궤적 후처리 = 추가 GPU 0).
- ✅ **길이 무관을 실측으로 확인** (논증 아님): 62원자·창 2–50 에서 **200 ps 4시드 평균
  6.2705e-06 ± 2.10e-06** vs **805 ps 6.632e-06** = +5.8 %, 시드 산포 안. 길이 4배가
  창 2–50 의 D 를 안 움직인다.
- 🔑 **따름정리 — #1 의 '셀 또는 시간' 이 '셀' 로 좁혀졌다**: 805 ps 로도 62원자 600 K 는
  β 0.75 로 게이트 실패(200 ps 4시드 앙상블도 0.61 탈락). 558원자는 같은 온도 0.82~0.93 통과.
  ⇒ **저이동도 600 K 게이트의 처방은 시간 연장이 아니라 셀 확대다.**

  ✅ **2026-08-31 — 셀 확대를 실제로 쟀다.** LPSOCl 3×3×1(558원자) 두 점 Ea **0.1697 eV**
  vs 62원자 **0.2855 eV** = **−116 meV**. 회신 AK 판정: 3×3×1 은 **새 보고량(셀 조건부)**
  이고 기존 0.287 eV 는 **62원자 조건부 값**이다. 계간 Ea 비교는 `citable:no` 로 잠겼다.
  ⇒ 이 항목의 잔여 이슈는 "600 K 하나" 가 아니다 — **셀이 Ea 를 116 meV 움직인다**
  (예비값, T800 완주 대기). 근거 `db/properties/lpsocl_box331_two_point_2026_08_31.json` ·
  `..._estimand_2026_08_30.json` · `kb/reviews/codex_AK_reply_lpsocl_box331_md_2026_08_30.md` · `e830df80`
- ⛔ **철회 (같은 날)**: "496원자 1.234e-05 vs 558원자 1.190e-05 = 3.7 % ⇒ 2×2×2 수렴" 은
  **길이·창이 다른 값을 뺀 것**이었다 (496 쪽은 `lpsocl_shape_compare_70ps_2026_08_27.json`
  의 70/150 ps · 창 2–30 값과 소수 셋째 자리까지 일치, 805 ps·창 2–50 이 아니다).
  **정합 비교 기존 기록은 2×2×2 vs 3×3×1 Tr/3 = 14.4 %** 이고 70·150 ps 두 시점 모두
  같아 '셀에 붙은 차이' 로 이미 승격돼 있다 (면내 성분은 18.7 %). ⇒ **2×2×2 미수렴.**
  62원자 배제만 유효 (등가축 불일치 + Tr/3 34–42 % 저하 + β 실패, 삼중 근거).

### 3. ~~VGCF 2×2 barrier 행렬 + 기전 판정~~ → ✅ **완료 (2026-07-30)**
- **2×2 행렬**: 1L|1L 0.3567 · 2L|1L(VGCF 2층) 0.1495 · 1L|2L(h-BN 2층) 0.3802 · 2L|2L 0.1473 eV.
  → 209 meV 는 거의 전부 VGCF 쪽 (**−207.2 meV = 98.9%**), h-BN 만 두껍게 하면 **+23.5 meV 악화**.
- **기전 = CONFINEMENT.** 표면 대조군 `Li_on_graphene_2L` = **0.2848 eV** 가 나왔다.
  같은 그래핀 1L→2L 변화가 자유 표면에서는 **+11.9 meV**(NEB 허용오차 ~20 meV 안 → **0**),
  갤러리 안에서는 **−207.2 meV**. 17배 차이 + 부호 반대.
  ⚠ +11.9 meV 를 '약간 악화'로 인용하면 안 된다 — 0 과 구별 안 되는 값이다.
- **논문 문장 확정**: "이중층 탄소 기판이 유리하다"(일반화) ❌ →
  "**갇힌 Li 에 대해** 벽 두께가 유리하다"(VGCF 다발 구조 특화) ✅
- 등록: `db/properties/vgcf_hbn_neb.json` `mechanism_verdict_2026_07_30` ·
  `vgcf_mechanism_origin.csv` · 그림 `docs/figures/vgcf_hbn/vgcf_mechanism.png` ·
  정리 `kb/results/vgcf_hbn_gallery_mechanism_2026_07_30.md`
- **남은 것(별도 항목 아님, 인용 규율)**: 3L 포화 미확인 → 0.147 eV 는 '수렴값'이 아니라
  **2L 값**으로만 인용. h-BN 굴곡은 #5 로 계속.

### 6. ~~LPSOCl COHP 곡선 원자료 회수~~ → ✅ **완료 (2026-07-29)**
- 회수 성공(md5 대조 일치). N 이 `lpsocl_icohp.json` 과 정확히 일치:
  P-S 19 · P-O 1 · Li-S 106 · Li-Cl 42 · Li-O 5 · S-S 54.
  산출: `db/properties/lpsocl_cohp_curves_origin.csv` ·
  `docs/figures/icohp/lpsocl_COHP_curves.png` · webapp Bonding 탭 실시간 렌더.
- **읽을 때 남는 제약(⚠ 인용 전 필독)**: COHPCAR 격자가 −15.03 eV 에서 시작해서
  **곡선 면적 ≠ ICOHP** 다. 창 안 비율 — P-O **30%** · Li-Cl 45% · Li-O 47% ·
  P-S 81% · Li-S 89%. 곡선은 "어느 에너지에서 결합/반결합인가"만 말하고,
  세기는 ICOHP 표(적분값)에서 인용한다. 그림·사이트 모두 이 커버리지를 표기한다.
  더 넓은 창이 필요하면 **LOBSTER 재실행**(COHPstartEnergy 확대)이 필요하다.
- 물리 판독: 모든 패널에서 반결합 상태가 E_F 위(비점유) — host 결합이 깨끗하다.
  P-O σ* 는 +3.5 eV. Li-Cl 은 −4.3 eV 한 봉우리에 몰려 있고 Li-S 는 −2~−9 eV 에
  넓게 퍼진다(같은 세기대, 다른 성격).

### 6b. ⏳ 예전 항목 원문 (참고용 — 회수 절차)
- `COHPCAR.lobster` 가 gabia
  `/data/work/runs/lpsocl_dft/lobster_ext/` 에만 있고 수십 MB라 repo 로 못 옮긴다.
- **회수 경로**: gabia 에서 `tools/figures/extract_cohp_curves.py` 로 패널 곡선만
  압축 CSV(~20 KB)로 뽑아 gzip+base64 전송 → `db/properties/lpsocl_cohp_curves_origin.csv`.
  그러면 webapp Bonding 탭이 자동으로 그리고,
  `tools/figures/fig_lpsocl_cohp_curves.py` 가 논문용 PNG 를 낸다.
- **⚠ 정규화 규약 주의**: 신규 추출기는 **결합당 평균**(∫|E_F = −ICOHP/bond, 자기일관),
  구형 `docs/figures/icohp/*_COHP_curves.csv`(modelc·nd·b2o3)는 **합(sum)** 이다.
  둘을 같은 그림/표에서 높이 비교하면 안 된다 (사이트는 '구형 CSV' 배지로 구분 표시).
- **회수 후 확인**: 추출기가 찍는 N 이 `lpsocl_icohp.json` 의 N(P-S 19 · Li-S 106 ·
  Li-Cl 42 · Li-O 5 · S-S 54 · P-O 1)과 일치해야 한다. 어긋나면 P–S dmax(기본 2.6 Å)를
  조정해야 하는 신호다.

### 7. ~~litdb 인덱스 정합 — digest 156편 중 67편이 INDEX 어디에도 없다~~ → ✅ **닫음 (2026-08-06)**
**해결**: 손으로 맞추면 또 밀리므로 **생성**으로 바꿨다.
- `tools/litdb/build_index.py` → `litdb/INDEX_DEM.md` (DEM·MPM 축 95편, 주제 7묶음, 그림 수 포함).
- `--check` = 두 인덱스 어디에도 없는 digest 보고. **지금 159편 중 0편.**
- 재감사(2026-08-06): 미등재 64편이 **전부 DEM 트랙**이었다 — 아래 '진짜 누락 SE 4편'은
  그새 등재돼 이미 해소. `INDEX.md` 는 SE 축 그대로 두고 머리말에 DEM 축 위치만 안내.
- 남은 것: `comparison_vs_ours.md` 미언급 98편은 **별개 문제**(우리 값 대비가 없는 digest).
  인덱스 정합이 아니라 내용 작업이라 여기서 닫지 않는다.

<details><summary>원래 감사 내용 (2026-07-29)</summary>

- **사이트·db 는 멀쩡하다.** webapp `list_papers()` 는 디렉터리를 직접 읽어 156편 전부 잡는다
  (파일 수 = 사이트 수 = 156). 문제는 **마크다운 인덱스 두 개만** 뒤처져 있다는 것.
- `litdb/INDEX.md` (갱신 2026-06-23 표기, 파일 mtime 07-28): **67편 미등재**.
  `litdb/INDEX_DEM_snapshot_2026-07-16.md` 도 그 67편을 담지 않는다.
- `litdb/comparison_vs_ours.md`: **98편 미언급** (우리 값 대비가 없는 digest).
- 미등재 67편의 대부분(≈63)은 **DEM·기계·건식전극 클러스터** — SE 캠페인과 축이 달라
  argyrodite 전용 INDEX 에 안 들어간 것이 설계상 자연스럽다. 다만 **SE 축 4편은 진짜 누락**:
  `huang2022_li2sis3_anomalous_conductivity_bvse` ·
  ~~`lee2024_multicomponent_argyrodite_mixed_oxidation_mtp`~~ **✅ 해소 2026-08-04** (INDEX 행 + comparison `[Lee24MO]` 키
  + 축 A 4행 신설; 본문 실물 독립 검증 §11 = 교정 6·신규 16) ·
  ~~`kim2026_hts_li3sc2po43_coating_midni_ncm`~~ **✅ 해소 2026-08-03** ·
  `yun2023_deciphering_degradation_halide_vs_sulfide`
  — 앞 3편은 2026-07-28 캠페인에서 우리가 직접 먹인 것들이다. **남은 진짜 누락 2편: huang2022 · yun2023.**
- **판정**: 급하지 않다(사이트가 정본). 다만 논문 에이전트가 digest 를 쓸 때
  **INDEX 갱신을 같이 하도록 되어 있는데 그게 최근 3건에서 안 됐다** — 에이전트 지침 점검 필요.
  DEM 클러스터는 별도 인덱스로 분리 유지가 맞다(축이 다름).
</details>

### 10. ~~ELF·그림 계 표시명이 4가지로 갈렸다~~ → ✅ **닫음 (2026-08-06)**
`LPSOCl` / `LPSOCl1.6` / `LPSOCl (Li27P5S21OCl8)` / `LPSOCl (O-substituted)` 가 섞여 있었다.
**db/properties 가 이미 `LPSOCl1.6`** (hops_per_ion.csv·bv_path_segments_lpsocl.csv) 이므로
**데이터 쪽에 맞춘다** — CSV 열 이름과 그림 범례가 같은 말을 해야 한다.
- `tools/figures/house_style.py` 에 **DISP / DISP_LONG** 등록: 계 비교 그림은 `DISP`
  (LPSCl1.6 · LPSOCl1.6 · B2O3@LPSCl1.6 · comp1), 조성식이 요점인 단일계 그림(ELF·COHP)은
  `DISP_LONG` (`LPSOCl1.6 (Li₂₇P₅S₂₁OCl₈)`).
- 스크립트 5개 라벨 교체 완료. ⚠ **이미 만들어진 PNG 는 옛 라벨 그대로**다 — ELF 는 cube 가
  gabia 에만 있어 재생성이 서버 작업이므로, 다음에 그 그림을 손댈 때 같이 다시 뽑는다.


### O. ✅ **Nd 갭 — 3종 자체 측정 완료 (2026-08-12 마감)** (2026-08-07 신규)

**✅ 마감 (2026-08-12)** — frozen-4f PP 로 3종을 직접 쟀다. `/data/work/runs/sei_dft_frozen4f/`
6단계 완주, spin-unpolarized.

| 상 | 우리 (PBE, frozen-4f) | MP (그동안 인용하던 값) |
|---|---:|---:|
| Nd₂O₃ | **3.948** | 3.81 (+3.6%) |
| LiNdO₂ | **3.698** | 4.21 |
| Nd₂S₃ | **0.770** | 1.79 |

1단계 합격 기준(Nd₂O₃ 가 절연체 · MP 와 정합)을 통과했으므로 **MP 인용 우회를 폐기하고
우리 값을 쓴다**. Li 계 6종과 같은 프로토콜이라 같은 표에 올릴 수 있다
(`comparison_group = gap-fixedocc-frozen4f-v1`). db 등재 완료
(`db/properties/sei_electronic.json` `*_frozen4f` 항목).

**frozen-4f 확인은 헤더가 아니라 전자수로 했다**: LiNdO₂ Li₄Nd₄O₈ → 4×3+4×11+8×6 = 104
= 실제 `nelec 104.0`; Nd₂S₃ Nd₈S₁₂ → 8×11+12×6 = 160 = 실제 `nelec 160.0`.

**남은 것**: 나머지 4종(NdPO₄ · NdOCl · NdCl₃ · NdS)은 아직 MP 소환값이다.
`tools/figures/plot_nd_sei_gaps.py` 의 하드코딩을 고칠 때 **우리 값 3 + MP 4 를 섞지
말고 출처를 표시**할 것. Nd₂S₃ 는 우리 0.77 vs MP 1.79 로 2배 이상 차이나므로,
그림에 MP 값을 남겨 둔 채 우리 값을 얹으면 안 된다.

**아래는 마감 전 기록이다 (경위 보존).**

**지금 상태**: Nd 상 갭은 전부 **MP 소환값**이다. 우리 계산은 두 번 실패했고 원인은 확정됐다 —
4f 를 원자가에 둔 PBE(+U) 의 SCF 해가 **금속**이라 fixed-occ 갭이라는 양이 성립하지 않는다
(`kb/projects/sei_products_2026_08_06.md` §최종 판정).

**⚠ 이건 "숫자 하나" 가 아니다.** repo 안에서 MP 갭에 의존하는 Nd 상이 7종이다 —
NdPO₄ 5.55 · NdOCl 4.77 · NdCl₃ 4.30 · LiNdO₂ 4.21 · Nd₂O₃ 3.81 · Nd₂S₃ 1.79 · NdS 0.00
(`tools/figures/plot_nd_sei_gaps.py` 하드코딩). 여기에 Nd₂O₃@LPSCl1.6 도핑 라인,
cascade Nd 후보, `nd_icohp.json` 이 얹힌다. **PP 하나로 축 전체가 살아난다.**

**닫는 방법**: `tools/sei/nd_frozen4f.py --plan` (0단계 인벤토리 → 확보 경로 A/B/C →
Nd₂O₃ 1단계 검증 → 나머지 → 등재). 판별 기준은 **z_valence** — frozen-4f ≈ 11 vs
4f-in-valence ≈ 14 (지금 우리 것). MP 의 VASP `Nd_3` 가 전자다.

**⛔ 함정 (도구에 가드 넣음)**: `build_dft_inputs.find_pseudos` 는 pseudo 디렉터리에서
**파일명 알파벳 첫 번째를 조용히 고른다**(`setdefault`). 새 PP 를 넣기만 하면
`Nd.paw.z_14…` 가 그대로 이겨서 **똑같은 금속 해**가 나온다. `--inventory` 가
'◀ 실제로 뽑힘' 을 찍고 frozen-4f 가 아니면 ⛔⛔ 경고한다.

**중단 기준**: 1단계(Nd₂O₃) 불합격 + 원인 30분 내 미해결 → MP 인용 유지, 보류로 기록.
⚠ **U 를 돌려 가며 갭이 열릴 때까지 맞추지 않는다** — frozen-4f 는 애초에 U 가 필요 없는 게 요점.

**등재 시 규칙**: 새 `comparison_group` = `gap-fixedocc-frozen4f-v1`. Li 계 6종(4f 무관)과
PP 계열이 달라 **같은 묶음이 아니다**.

**★★ 2026-08-12 재실행 — frozen-4f PP 가 **이미 있다**. 경로 A/B/C 불필요.**

```
Nd.pbe-spdn-kjpaw_psl.1.0.0.UPF   z_valence = 11.0   → frozen-4f   ◀ 실제로 뽑힘
```

08-07 인벤토리는 "Nd UPF 하나뿐이고 z=14.0" 이었다. 그 사이 /data/work/pseudo 가
바뀌었고, 지금 build_dft_inputs 가 **실제로 고르는 것**이 frozen-4f 다(도구의
'◀ 실제로 뽑힘' 표시로 확인). 즉 확보 단계는 끝났고 **1단계(Nd₂O₃ 검증)** 로 바로 간다.
ld1.x 생성도, VASP 외주도 필요 없다.
(참고: `ld1.x` 도 `/data/apps/qe-7.4.1-cpu/bin/` 에 **있다** — 2026-08-12 실측. 지금은 안 쓰지만 경로 B 가 막혀 있지 않다는 뜻이다.)

⚠ 그래도 1단계 합격 전에는 갭을 등재하지 않는다 — PP 가 frozen-4f 라는 것과
  그 PP 로 절연체 해가 나온다는 것은 별개다. 합격 기준(§계획 1단계) 셋을 그대로 적용.

**★ 0단계 실행 결과 (2026-08-07, gabia) — 아래는 그때 기록, 위가 최신**

- 인벤토리: `/data/work/pseudo` 에 Nd UPF 가 **하나뿐이고 z=14.0**(4f-in-valence).
  frozen-4f 없음 → **확보 경로 A/B/C 필요**. (A: 기성품 탐색부터 — 란타나이드는
  "RE-in-core" 세트가 따로 있는 경우가 많다)
- ⚠ **레퍼런스 회수 중에 별개 문제가 나왔다** — `tools/figures/plot_nd_sei_gaps.py` 의
  하드코딩 7종 중 **3종이 방금 받은 MP 값과 어긋난다**:

  | 상 | 그림 하드코딩 | MP 재조회 | material_id |
  |---|---|---|---|
  | NdOCl / NdCl₃ / LiNdO₂ / NdS | 4.77 / 4.30 / 4.21 / 0.00 | 4.769 / 4.300 / 4.212 / 0.000 ✓ | mp-23058 / 23183 / 1222355 / 1748 |
  | **NdPO₄** | 5.55 | **5.679** | mp-3584 |
  | **Nd₂O₃** | 3.81 | **3.708** | **mp-1045**(Ia-3, 40원자) |
  | **Nd₂S₃** | 1.79 | **0.760** | mp-438 |

  그림 주석이 *"numbers hard-coded from run"* 이고 **material_id 를 안 남겼다** —
  그래서 어긋난 3종의 원인(다형체 차이인지 값 갱신인지)을 그 파일만으로는 못 가린다.
  Nd₂S₃ 는 우리 구조(`sei_nd2s3_mp-438.vasp`)와 **ID 가 같은데도 2.4배** 차이라 특히 수상하다.

- ⛔ **도구 버그도 함께 잡았다**: `--reference` 가 조성만으로 "MP 최안정" 을 고르는 바람에
  Nd₂O₃ 를 **mp-1045(40원자)** 로 잡았다. 우리 실물은 **mp-2763(5원자)** 다. 다형체가 다르면
  갭도 다르므로 그대로 두면 표적이 아니라 **오답지**가 된다. → `PINNED` 로 우리 구조 ID 를
  고정하고, MP 최안정과 다르면 `mp_most_stable` 로 그 사실을 같이 기록하게 고쳤다.

**닫기 전에 할 것 (추가)**: `plot_nd_sei_gaps.py` 의 7종에 **material_id 를 박고**, 어긋난
3종의 출처를 가린다. 그림이 이미 쓰이고 있으므로 이건 frozen-4f 확보와 **독립적으로** 급하다.

**★ 출처 규명 완료 (2026-08-07 gabia `--polymorphs` 실행, 08-10 등재)** — 어긋난 2종 다
**준안정 '예측만' 다형체를 골랐던 것**으로 확정:
- Nd₂S₃ 1.79 = **mp-32586** (I-42d, 40원자, hull +0.020, ⚠예측만) ★그림 값과 일치.
  관측 바닥상은 mp-438(Pnma) 0.760. 화학적으로도 가벼운 Ln 은 α-사방정(Pnma)이 맞다.
- NdPO₄ 5.55 = **mp-1103387** (I4₁/amd 제논타임형, hull +0.018, ⚠예측만) ★일치.
  관측상은 mp-3584(P2₁/c 모나자이트) 5.679 — Nd 는 모나자이트가 맞다.
→ 남은 일: `plot_nd_sei_gaps.py` 값 교체(1.79→0.760, 5.55→5.679) + 7종 전부 material_id
  주석 (todo #32). `db/properties/sei_products.json` 의 1.79 도 같이.

### R. ✅ **litdb 인덱스 미편입 5편 + MLIP 3부작 비교표 — 닫음 (2026-08-19, 신설 당일)**

> **닫은 방법**: kgy 본 실행이 끝나 **UMA 힘 MAE 30.0 meV/Å** 이 확정 → 그 값을 앵커로
> `INDEX.md` 새 절 3개(🤖 MLIP 방법론 / 🧰 방법론(ML) 추가분 / 🧪 자체·공저) + `comparison_vs_ours.md`
> **새 축 J** 를 한 번에 썼다. `build_index.py --check`: **어느 인덱스에도 없는 것 0편 · DFT 76/76 ✅**.
> 판정 카드 `kb/results/uma_force_accuracy_li3ps4_2026_08_19.md` 신설, 값 `db/properties/mlip_bench_li3ps4_uma.json`.
>
> **본 실행 결과 (n=243, 시범 n=20 의 26.3 이 버텼다)**: 힘 MAE **30.0 meV/Å**(Li 13.2 / P 36.8 / S 40.9),
> 보정 후 에너지 13.5 meV/atom, 상대에너지 RRMSE 2.4 %, 실패 0/243.
> 같은 test set 공표값 **PET-MAD 기저 63.9 · LoRA 39.2 · bespoke 35.6** ⇒ **범용이 전용을 이겼다.**
> ⭕ 자기적합(낙관치) 13.49 ≈ train-적합 13.45 ⇒ 잔차는 **적합 부족이 아니라 진짜 모델 오차** (결과를 강화).
> ⇒ **"UMA sulfide PES softening" 알리바이 철회.**
> ⚠ **응력·장벽·Cl 은 여전히 미측정** — NEB 0.528 격차는 **별건으로 남는다.**
> ⛔ **2026-08-20 정정 — cascade 부피 편향(+32.7 %)은 여기서 뺀다. 원인이 이미 닫혀 있었다.**
>   fmax 사다리가 primary card 에 있다: `0.05 → 27.478 Å³/atom` (잔류압 +0.1865 GPa) ·
>   `0.01 → 20.442` · `0.002 → 20.415`. **충분히 수렴한 UMA host 는 DFT 대비 +4.4 %** 로 정상이다.
>   ⇒ +32.7 % 는 **모델 편향이 아니라 미수렴**이다 — 이걸 "미측정·별건" 으로 남겨두면
>   닫힌 결론을 다시 논증하게 된다(F5 유형. 실제로 2026-08-20 에 이 실측을 인용해 놓고도
>   stress 파인튜닝을 처방으로 올렸다 — 처방이 진단보다 앞섰다).
>   **올바른 순서**: ① Stage 02 를 `fmax ≤ 0.01` + 충분한 step 으로 고친다 →
>   ② residual stress / volume convergence 게이트 추가 → ③ 재실행 후에도 systematic
>   stress error 가 남을 때만 DFT stress 벤치 → ④ 그 뒤에도 필요할 때만 파인튜닝.
>   ⇒ **지금 DFT 라벨 100–400개를 만드는 것은 낭비다.**
>   근거: `kb/reviews/codex_A_cascade_ml_2026_08_20.md` §2-2 (§2-2b 는 ③ 도달 시까지 보류).
>
> **남은 후속 (여기서 파생 — 전부 미착수, 새 DFT 0)**
> ① UMA 보존성 유한차분 점검 ② 기존 궤적의 **비-Li 골격 MSD @600/800/1000 K**
> (Zhang npj 가 MACE-MP-0 의 LGPS 골격이 1050 K 부터 녹는 걸 잡았고 **우리 앵커가 그 바로 아래**)
> ③ 52 → 416원자 셀 비용 실측 ④ **Li₃P 벌크 UMA 검증** (Li₃N 금지 규율의 자매계 — 계면 작업의 필수 관문)
>
> ⚠ **구조적 원인은 안 닫혔다** — `INDEX.md` 는 사람 큐레이션이라 **에이전트가 digest 를 만들 때마다
> 같은 구멍이 다시 생긴다.** `--check` 를 세션 마감 절차에 넣는 건 **여전히 미결.**

<details><summary>신설 당시 원문 (참고용)</summary>

#### R(원문). 🟡 litdb 인덱스 미편입 5편 + MLIP 3부작 비교표 — kgy 벤치 결과 나오면 한 번에 쓴다

- **상태**: digest·그림은 **전부 커밋·푸시 완료** (`e375c69d` · `1bac12aa` · `4ab86d6f`,
  파일 수 디스크=원격 일치 확인). 남은 것은 **인덱스/비교표 편입 하나뿐**이다.
- `python3 tools/litdb/build_index.py --check` 가 잡는 5편 (전부 **dft 축**):

  | slug | 왜 아직 안 넣었나 |
  |---|---|
  | `petmad2026_lightweight_universal_interatomic_potential_mad` | UMA 힘 MAE 확정 대기 |
  | `zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill` | 〃 |
  | `lai2025_haml_li_metal_lpscl_interface_doping_seFO` | 〃 (γ 게이트 축) |
  | `kauwe2021_ml_materials_properties_dissertation_sparks` | 위 셋과 같은 ML 축 |
  | `lee2026_mechanical_halogen_argyrodite_drycoating` | 이전부터 미편입 |

  `comparison_vs_ours.md` 도 **같은 5편**이 미편입 (DFT 71/76).
  각 digest 안에 `## INDEX·비교표에 넣을 항목 (수동 병합 대기)` 초안이 이미 있다.
- **왜 한 번에 쓰나** — 다섯이 한 논지로 얽혀 있다:
  PET-MAD ↔ Zhang npj 가 둘 다 **"필요한 ab initio 구조 = O(10²)"** 로 수렴하고,
  Lai 는 거기서 **"벌크·수송 = 파인튜닝 노선 / 계면 반응 = HAML(γ 게이트) 노선"** 으로 갈린다.
  ⇒ 세 카드의 비교표에 **UMA 힘 MAE 실측값**이 공통으로 들어가야 하므로,
  값이 확정되기 전에 쓰면 곧바로 다시 고쳐야 한다.
- **막고 있는 것 (2026-08-19 23:5x 현재 kgy 에서 실행 중)**:
  `tools/mlip/bench_against_dft.py --train …/Li3PS4/train.xyz --test …/test.xyz --tag li3ps4_uma`
  → `db/properties/mlip_bench_li3ps4_uma.json`
- **시범(n=20) 예비값** ⚠ *본 실행 전까지 인용 금지* — 힘 MAE **26.3 meV/Å**(Li 11.8 / P 31.0 / S 36.1),
  보정 후 에너지 MAE 9.9 meV/atom, 상대에너지 RRMSE 2.3 %, 참조보정 R² 0.764.
  같은 test set 공표값: **PET-MAD 기저 63.9 · LoRA(N=1940) 39.2 · bespoke(N=1940) 35.6 meV/Å**.
  ⇒ 사실이면 **학습 안 한 UMA 가 이 데이터로 1940개 학습한 전용 모델보다 힘이 정확하다**.
  ⚠ 못 믿는 이유 셋: ① `--limit 20` 은 **앞에서 20개를 자르므로** α/β/γ 3상·온도 16점 중
  한 슬라이스에 몰렸을 수 있다 ② 20개로 원소 3개 적합이라 R² 가 느슨하다
  ③ 보정계수(Li +0.094 / P +0.031 / S +0.125 eV)는 **PBE↔PBEsol 차이를 흡수한 항**이라
  그 자체를 물리로 읽으면 안 된다.
- **닫히면 따라오는 것**: preflight 이 알리바이로 쓰던 **"UMA sulfide PES softening"** 의 근거가
  사라진다 ⇒ NEB 0.528 vs MD 0.253 격차의 남은 후보는 **경로 선택**.
  ⚠ 단 이 벤치는 **응력(라벨 없음)과 장벽을 안 잰다** — 격차를 이걸로 닫을 수는 없고,
  "UMA 힘이 틀려서"라는 설명 하나만 지운다.
- **재발 항목이다** — #7(2026-08-06 "digest 156편 중 67편 미편입") 과 같은 종류.
  그때 닫은 방식은 `build_index.py` 신설이었는데, `INDEX.md` 는 **사람 큐레이션**이라
  도구가 자동 생성하지 않는다 ⇒ **에이전트가 digest 를 만들 때마다 이 구멍이 다시 생긴다.**
  구조적으로 닫으려면 `--check` 를 커밋 훅이나 세션 마감 절차에 넣어야 한다 (미결).

</details>


### ~~M6~~. ✅ cascade 양극 반응성 게이트 — **완료·판정 완료** (2026-08-20)
- **검증 통과**: 닫힌계 pseudo-binary ΔE_rxt로 LPSCl/LCO **만충 −322.7 (Xiao −339, 0.95×) /
  반충 −454.9 (−493, 0.92×)**, 리튬화 순서(반충이 더 발열)까지 재현.
  반응식도 `Li₂S + Li₃PO₄ + Co₉S₈` 로 물리적으로 타당.
- **교훈(기록용)**: 초판을 개방계 `GrandPotentialInterfacialReactivity` + 전위 스캔으로 짰다가
  −810~−1544 meV/atom 이 나왔고, V=4.30 반응식이 `Li6PS5Cl -> 6 Li + SCl + 0.5 P2S7 + 0.5 S` 로
  **양극이 아예 빠진 자체분해**였다. Li 저장소를 열면 코팅 탈리튬 분해가 상호반응을 압도한다.
  xiao2019 digest 227번 줄이 ΔE_rxt를 "**닫힌계**"로, 222번 줄이 만충/반충을 **조성 축**으로
  명시하고 있었다. → **개방계는 Li 음극 쪽 도구, 양극 F4 게이트는 닫힌계**.
- **전수 완주**: 47 코팅 × {LiCoO₂, Li₀.₅CoO₂} = **94쌍** (gabia, 2026-07-28).
- ✅ **회수 완료** (repo `db/properties/cathode_reactivity_cascade.csv`, 94쌍 전수).
- ✅ **판정 완료** (2026-08-20, `tools/cascade/analyze_cathode_reactivity.py` →
  `db/properties/cathode_reactivity_verdict.json`). 결과가 셋인데 **셋 다 예상과 다르다**:

  ① ⛔ **게이트가 vacuous 다.** 89/94 쌍 통과 · 코팅 42/47종 통과. 탈락 5종
     (BaO · MnO · Na₂O · Sb₂O₅ · TiF₄)이 **전부 이미 G1–G4 에서 죽어 있다**
     → `unique_kill = 0`, **완전 중복 게이트**(G2 와 동종). 임의 비율 문턱이 아니라
     깔때기의 unique_kill 규약으로 판정했다. 물리는 맞다 — 황화물 SE↔산화물 양극은
     큰 구동력, 산화물 코팅↔산화물 양극은 작은 구동력. **맞는 물리가 변별을 주지는 않는다.**

  ② ⚠ **S1 성공조건 ②의 답은 YES 지만 자명하다.** "host LPSCl(−322.7)보다 완화되는
     코팅이 있는가" → **47/47 전부** (−107 ~ 0 구간). 그러나 비교가 *황화물 vs 산화물 양극*
     대 *산화물 vs 산화물 양극*이라 **화학이 다르다.** 코팅 개념 자체의 타당성을 재현한
     것이지 **후보 간 변별이 아니다.** 이 문장을 "코팅이 효과 있다"로 읽으면 안 된다.

  ③ ⭐ **진짜 신호는 게이트가 놓친 쪽에 있다 — Li 흡수(scavenging).**
     25행에서 검출, 그중 **게이트를 통과하면서** 흡수하는 것이 **23행**이다:
     Al₂O₃→LiAl₅O₈ · WO₃→Li₂WO₄ · Nb₂O₅→LiNbO₃ · MgF₂→LiF · Ta₂O₅→LiTaO₃ 등.
     전부 |dE_rxt| < 100 meV 로 통과하는데 **양극에서 Li 를 빼앗는다.**
     Al₂O₃ 코팅의 Li inventory 소모는 **실험적으로 알려진 현상**인데 dE_rxt 축은 못 잡는다
     → Xiao F4 게이트의 **사각지대**다.

  ④ **리튬화 비대칭이 기구가 다름을 드러낸다.** host LPSCl 은 반충이 더 나쁘고(−454.9,
     탈리튬 양극이 더 산화적 = S 산화 구동), 산화물/불화물 코팅은 **18종이 반대로 만충이
     더 나쁘다**(Li 흡수 = Li 함유 삼원상 형성 구동). 9종만 host 와 같은 방향이다.
     ⇒ **두 계를 같은 "반응성" 언어로 묶어 서술하면 기구를 뭉갠다.**

- ⛔ **2026-08-20 이름 정정 (codex 리뷰 C)**: 이 축을 **"G6" 라 부르지 않는다.**
  `cascade_stability_axes_verdict.json` 의 `T9_interface_axes` 가 이미 **G6 = SE_LPSCl**,
  **G7 = Li anode** 로 쓰고 있고, `cathode_full/half` 도 **그 파일에 이미 등록**돼 있다
  (kill 2/3, core unique 둘 다 `[]`). 즉 오늘 새로 나온 것은 축이 아니라
  **94쌍 반응식 전수 + Li 흡수 분석**이다. 올바른 구분:
  `historical funnel = G1–G5` · `cathode full/half = post-hoc cathode audit` ·
  `SE / Li = 별도 post-hoc interface diagnostics`. **셋을 하나로 묶지 않는다.**
- **남은 것**: 깔때기 조인은 **하지 않는다** — 추가 축소 기여가 없는 축을 단계로 올리면
  깔때기가 실제보다 촘촘해 보인다. 대신 **Li 흡수를 적용범위가 적힌 별도 진단축으로 등록**
  (③이 근거). ⚠ 컷 근처 ±20 meV 순위 주장 금지.
  ⚠ 컷 근처 ±20 meV 순위 주장 금지 (Xiao 100 meV는 관례컷 + Sundar 2025의 "분해산물 전자전도도
  미고려" 비판을 그대로 받음).


