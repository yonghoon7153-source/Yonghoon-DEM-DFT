# 세션 진행 대피소 — 2026-09-20 (압축 전 기록.  정본은 각 문서·원장)

## 믹서 (정본 `docs/reviews/mixing_model_design_20260919.md` §22~§24 · 원장 MIX-01~10)
- §22 경계 탐침 완료: 전이 **Bo ≈ 0.5** (격자 4점, 폭 (0.21, 1.00)); 런내부 sd 봉우리가 근거.  H/R 은 Bo ≳ 1 천장 (MIX-09).
  측정 규약 `--r-container 0.02056 --axis x --last 100`.  사다리: E0 1.4911 · C1 1.5686 · T1 1.5271 · E1 1.5729 · T2 1.7499 · B5 1.8552 · B10 2.0061 · E2 2.0197 · E4 2.0164.
- §23 자기리뷰: 축은 맞고 순서가 틀렸다.  MIX-10(Bo_c 는 충전율 9.8 %·Fr 0.083 한 점) · MIX-07 추기(Bo 정의: 평형겹침 인력 vs JKR pull-off) · §22-5 코팅 128배(앵커)/900배(E4).
- 1저자 결정: 응집체 분쇄 얘기 제외 · 헤드라인 = "코팅하면 더 잘 섞이나" 대비 조건 · LIGGGHTS 로 가능한 것 전부 · LAMMPS 는 보고 뒤 병행.
- §24 사전등록 완료 (블록 1: L0/LA(Bo 3.0 앵커)/LC(코팅) × 시드 3, 8바퀴, Lacey M, h1 ≥0.30∧2SE, 음성대조 M(L0)≥0.8).
- 코드: `make_mixer_deck.py` 층상 팔 L0/LA/LC (65/65, 골든해시 가드) · `measure_mixing_index.py` (11/11) · 인벤토리 등재.  **미커밋** (게이트 재실행 필요).
- ✅ 스모크 결함(RSA 잼) 해결: AM 원통 전체→정착①→SE+섬유 AM 침대 위 블록→정착②.  스모크 insA 1493·insB 6077·S₀² 0.1768≫S_R² 0.0169·M(t0)=0.  커밋 d8bf00239 (푸시됨).
- ✅ 본 런 9개 **완주** 23:02 (전부 rc=0, 덤프 208, 접촉 유효성 9/9).  시드 32452843 등록칸(8×8×2) 판독: L0 0.956 · LA 0.950 · LC 0.964 (LC−LA 0.014 → h0 쪽).  탐색 칸 사다리: LA 0.950→0.890→0.824, L0/LC ≈0.95 유지 → **§25 사전등록**(16×16×4 주판정, h1 ΔM≥0.10∧2SE, 시드 2·3 미열람).  AA/AS 9런 0.23~0.27 (완전 분산).  (원래 줄: 본 런 9개 가동 중 16:59 시작 (`$SP/lay/{L0,LA,LC}_s*/`, 4병렬, 로그 `$SP/lay_launch.log`, ≈6.5 h → 23:30 전후).  분석: `python3 scripts/measure_mixing_index.py $SP/lay/LA_s32452843 ... --ref $SP/arms3/E0` (ref = 같은 시드의 E0.  32452843 은 arms3/E0; 49979687·91648301 은 `$SP/launch_E0_seeds.sh` 가 본 런 종료 후 자동으로 만든다 → `$SP/lay/E0_s<seed>`, 로그 `$SP/e0_launch.log`).
- 배플 12팔: 정지(T) 상태, 폐기 권고 — 1저자 결정 대기.
- PTFE/VGCF: 덱은 영률·마찰·반발·구름마찰 전 상 공통(1e7/0.5/0.3/0.2), 강체 3구 사슬 → 수동 필러.  블록 2 민감도 팔 등록만.
- ✅ 웹앱 `/mixer` 섹션 완성 (미커밋, 게이트 중): 라우트 app.py `_mixer_devlog_entries`/`mixer_devlog` · `templates/mixer.html` · base.html 메뉴 · `webapp/test_mixer_devlog_page.py` 9/9 · check_all.sh 배선 · `docs/mixer_devlog/v01~v06_*.md` · `webapp/static/mixer/*.png` 8장.  새 버전은 `v07_<날짜>.md` 파일을 mixer_devlog 폴더에 추가 = 누적 (자리표시자를 경로로 적으면 check_doc_refs 가 깨진 참조로 잡는다).

## Phase A (uma 박스)
- 재실행 96팔: ptfe centerline ✓ · LEAN2 ✓ · code_sha null ⛔ · 영수증 0.  원본 .sh 96 (kits/), 로그 96 (rerun_logs/), 재실행 .sh 없음.
- 접미사↔vox: 104577=v015 · 51133=v020 · 21058=v025.  원본 .sh 는 `--step3-vox 0.4` 가 앞, 진짜 값 뒤 (뒤가 이김; 도구가 --expect-physics 로 대조).
- 도구 `phase_a_receipt_from_sh.py` (23/23) 푸시됨 `8cc41d607`.  형이 v015 .sh 재생성 32/32 완료; 세 번째 줄(영수증)은 pull 후 실행 대기.
- 다음: 영수증 3개 → 어댑터 `--code-sha-missing-ok "<이유>"` → 판정.  문턱 근처면 재실행 필요 판단.

## ps (ibb) — 1저자가 직접 관리 (손대지 말 것)
- ps_10_0_r45_r2 11코어 재시작 성공 (step 1900001, atoms 159161 = 원래 런이 6개 흘림).

## 커밋 상태
- 푸시됨: 916648ef0 (§23) · 8cc41d607 (영수증 도구).  미커밋: §24 + 층상 팔 + 측정기 + 인벤토리.

## 23:45 판정 완료
- §26: 등록 칸 애매(Δ0.019, SE0.011) · §25 주판정 16×16×4 h1(Δ0.118, SE0.012; 시드 2·3 만 Δ0.114 h1).  v0.7 devlog · mixing_v07.png · MIX-08 claimed_fixed.  게이트 후 커밋.
