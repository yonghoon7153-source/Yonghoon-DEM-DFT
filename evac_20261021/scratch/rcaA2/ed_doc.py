p = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/impl/carbon_junction.py'
s = open(p, encoding='utf-8').read()


def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)


rep('''  자기 접합 = 같은 fid 의 비연속 두 위치가 면으로 닿거나 (설계 §4-1 J1) 같은 셀을 다시 지남 (재방문) — 이웃 위치로 무리 지은 후보 하나.
    ★ 꺾임 거르기: 후보마다 두 쪽 (항목의 앞 · 뒤 위치) 셀 조각 (그 셀 닫힌 상자로 자른 중심선) 사이 **최근접점 쌍** (거리² ε 띠 ·
      띠 안 동률 = 호 길이가 작은 쪽) 의 경로 호 길이 s (fid 경로를 정준 방향으로 누적 · 조각 사이 간격 현 포함 · 점 역순 불변) ·
      s < s_min = 같은 가닥의 연속 (접합 아님 · 면 = 옛 융합 그대로) · s ≥ s_min = 진짜 접힘 · 고리 접촉 (절단 + R_j 간선 · 같은 길이 법칙 ·
      같은 분산판).  s_min = 필수 · 기본값 없음 (None = 미등록 → 정량 거부 · 시험 모드 = 거르지 않음).
    ★★ 멤버십 열쇠 = (cell, fid, branch) (`CJUNC_BRANCH_RULE` · 10-21 Codex RCA-03 · 1저자 Q1 (가)): branch = 그 셀을 지나는 연속 경로 구간
      (위치 하나) — 같은 셀의 같은 fid 다른 가지는 **합치지 않는다** (옛 판: s < s_min 재방문 = 옛 셀 한 노드 = 비연속 가닥 단락 · 반증됨).
      s < s_min 재방문 = 접합 없음 (경로로만 이어진다 · 수 기록 `n_self_revisits_path_only`) · s ≥ s_min = 두 가지 사이 R_j 간선.
    자기 접합 L_c = 닿음 규칙을 두 쪽 셀 조각 사이에 (구현 B 의 '위치 수 × vox' 셈을 대체 — 배율이 σ 에 들어가므로 격자 셈을 쓰지 않는다) ·
      자기 접합 접점 = s 를 정한 최근접점 쌍 (띠 안 · 같은 s 면 중점 사전식) · 포트 = 그 두 점의 기하 정준 포트 (각 쪽 위치 중).''',
    '''  ★★ 조각 = 섬유 (`CJUNC_PIECE_RULE` · 10-21 사전 리뷰 (구현) PRE-impl-01 · 06 · 1저자 Q-A): 생산 끊기 규칙 (`fibre_pieces`) 이 가른 같은 fid 의
    두 조각은 경로로 이어지지 않는다 → 서로 다른 섬유와 같은 접합 규칙 (중심선 d ≤ D → R_j · s 규칙 없음 · 옛: 같은 fid = 자기 후보 · 조각
    사이 간격 현을 지나는 s 로 '연속' → 같은 셀 끝 = 경로로만 (σ 0) · 면 인접 끝 = 옛 융합).  호 좌표 = 조각 안 누적 (조각마다 0 부터).
    닫힌 경로 (첫 점 = 끝 점 · 비트) 의 이음매 = 연속: 끊김이 있으면 끝 조각 + 첫 조각을 이음매를 지나 한 조각으로 · 없으면 고리 조각 (s =
    둘레 짧은 쪽 · 첫 · 끝 위치 같은 셀 = 별칭 한 dof · 면 이웃 = 축방향 둘레).
  ★★ 자기 접합 (`CJUNC_SELF_RULE` · 10-21 PRE-impl-02 · 1저자 Q-B) = 서로 다른 섬유와 같은 탐지 — 같은 조각 중심선 선분 쌍 (최근접 d ≤ D) 마다
    s = 최근접점 사이 조각 호 길이 · 바닥 (`_self_floor`: s > D 그리고 s > (π/2)·d — 곧은 이웃 · 꼭짓각 ≥ 79° 꺾임 모서리 = 어느 s_min 에서도
    연속) · 접합 쌍 = 바닥 쌍 중 s ≥ s_min (s < s_min = 같은 가닥의 연속 · 접합 아님) · 이웃 선분 쌍 무리 (union-find · 고리 = 둘레) 하나 =
    instance 하나 (접점 · d0 = 서로 다른 섬유와 같은 CP 규칙 · L_c = 그 무리 접합 쌍의 닿음 · 같은 길이 법칙 · 같은 분산판 (맞은편 = 그 쌍만)).
    셀 인접 (면 · 같은 셀) 은 후보를 만들지 않는다 (옛: 셀 인접 = 후보 · 중심선 거리 검사 없음 → 닿지 않는 다리에 접합 · 닿는 모서리 인접 다리에
    없음).  같은 조각 면 (축방향 아님) = 두 위치가 연속 (`_continuity` — 같은 바닥 · s_min) 이면 옛 융합 · 아니면 자기 instance 발자국 = 절단 ·
    아니면 미등록.  s_min = 필수 · 기본값 없음 (None = 미등록 → 정량 거부 · 시험 모드 = 바닥만).
    ★ 멤버십 열쇠 = (cell, fid, branch) (`CJUNC_BRANCH_RULE` · 10-21 Codex RCA-03 · 1저자 Q1 (가)): branch = 그 셀을 지나는 연속 경로 구간
      (위치 하나) — 같은 셀의 같은 조각 다른 가지는 **합치지 않는다**.  접합 쌍이 잇지 않은 재방문 = 경로로만 (`n_self_revisits_path_only` ·
      사이에 덮인 위치가 있으면 `n_self_revisits_path_broken`).
  ★★ 포트 = 옮기지 않음 (`CJUNC_PORT_RULE` v3 · 10-21 PRE-impl-03 · 1저자 Q-C): 후보 = 그 조각 (자기 접합 = 그 쪽) 의 위치 **살았든 덮였든** ·
    고른 위치가 덮였으면 (SDCP · PTFE · 상자 밖) 미실현 (covered_<상> · out_of_box) — 덮은 상의 법칙만 (SDCP = SV 융합 · S3 c · PTFE =
    face_alpha P0/P1) · 같은 접촉을 두 번 세지 않는다 (옛: 살아있는 이웃 셀로 옮겨 SV 융합과 병렬 · centerline 은 절연체를 더해 σ 상승).
    접합 + ptfe_stamp centerline = 거부 (계획 · 솔브 입구 · `ca_ext_cjunc` protocol).''')

rep('''  ★ SV (10-21 Codex RCA-06 · 1저자 Q4 (가)): 옛 `sv_dominant` (SV 면 + SDCP 셀 소산 ≥ VV 접합 소산 = '지배' 표지) **철회** — 소산 몫은
    국소 저항 민감도이지 경로 지배 · 우회 크기가 아니다 (판정문 반례: SV 경로 전류 90.5 % 인데 가드 false).  남는 것 = 진단
    `sv_local_dissipation` (몫만) · 반사실 대조 (선택 노브 `cjunc_plan(sv_counterfactual={'threshold': t})` — 같은 침대 · 같은 R_j 에서
    SV 융합 면 (SDCP–VGCF 면) 을 끊은 판의 단자 G 와의 비 `sv_counterfactual_ratio` · 문턱 = 기본값 없음 (등록이 채운다) · 표지
    `SV_DEPENDENT` 는 문턱이 주어질 때만).''',
    '''  ★ SV (10-21 Codex RCA-06 · 1저자 Q4 (가)): 옛 `sv_dominant` (SV 면 + SDCP 셀 소산 ≥ VV 접합 소산 = '지배' 표지) **철회** — 소산 몫은
    국소 저항 민감도이지 경로 지배 · 우회 크기가 아니다 (판정문 반례: SV 경로 전류 90.5 % 인데 가드 false).  남는 것 = 진단
    `sv_local_dissipation` (몫만) · 반사실 대조 (선택 노브 `cjunc_plan(sv_counterfactual={'threshold': t})` — 같은 침대 · 같은 R_j 에서
    ★ 10-21 (PRE-impl-04 · 1저자 Q-D · `CJUNC_SV_CF_RULE`) **SV 다리만** 끊은 판 (서로 다른 섬유 · 접합으로 갈린 가지를 잇는 SDCP 성분의 SV
    면 · SDCP 를 지나는 섬유의 자기 연속은 남긴다 · 끊기만 = 비 ≥ 1) 의 단자 G 와의 비 `sv_counterfactual_ratio` (기록 종류
    `CJUNC_SV_CF_KIND` · 옛 'SV 면 전부' = SDCP 를 지나는 섬유 하나도 비 ∞) · 문턱 = 기본값 없음 (등록이 채운다) · 표지 `SV_DEPENDENT` 는
    문턱이 주어질 때만).''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
