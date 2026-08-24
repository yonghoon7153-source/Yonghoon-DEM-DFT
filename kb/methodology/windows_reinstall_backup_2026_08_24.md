---
title: "Windows 재설치 전 백업 — C: 오판 정정과 실제 위험처"
date: 2026-08-24
updated: 2026-08-24
tags: [backup, archive, wsl, windows, single-point-of-failure, provenance]
status: 진행 — 스크린샷 판독은 확정, C: 실사는 미실시
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: multi-source-mixed
---

# Windows 재설치 전 백업 — C: 오판 정정과 실제 위험처

> **왜 있나**: 2026-08-24 재설치 준비 대화에서 에이전트가 *"repo 폴더 7개가 전부
> `C:\` 루트에 있다 → 재설치 때 날아간다"* 라고 답했다. **이건 틀렸다.** 스크린샷은
> `D:` 였다. 잘못된 전제 위에 "D: 로 옮겨라" 라는 실행 계획이 통째로 얹혀 있었으므로,
> 정정과 **정정 근거**를 남긴다.

## 1. ⛔ 정정 — 그 폴더들은 `D:` (T7 Shield) 다

탐색기 스크린샷 판독:

- 주소 표시줄 `T7 Shield (D:) >`, 좌측 트리에서 **`T7 Shield (D:)` 가 선택·확장** 상태.
- 좌측 트리에 `로컬 디스크 (C:)` 는 **접힌 채 따로** 있다 — 목록의 출처가 아니다.

**결정적 교차검증** — 목록에 있는 항목 3개가 `kb/methodology/offline_archive_index_2026_08_20.md`
에 이미 `D:` 경로로 등재돼 있다:

| 스크린샷 항목 | 인덱스 카드의 기록 |
|---|---|
| `v100` | `/mnt/d/v100/kisti_backup_2026-07-14/` (백업 A, 47 GB) |
| `v100, kisti 백업` | `/mnt/d/v100, kisti 백업/` (백업 B) |
| `archive` | `D:\archive\Linux_Workspace\linux_disk.img` (백업 C, 48.8 GB) |

⇒ 같은 창의 나머지 항목도 `D:\` 루트다. repo 사본 7개
(`Yonghoon-DEM-DFT` · `-codex` · `-codex-bml` · `-codex-dem-mpm` · `-codex-dft` ·
`-friendly` · `-sdcp`)는 **이미 외장 SSD 에 있고, 재설치로 안 날아간다.**

⚠ 이 판독은 **스크린샷 한 장**이 근거다. 실사(`Get-ChildItem C:\ -Directory`)로
확정하지 않았으므로 `verificationStatus: unverified` 로 둔다. C: 루트에 동명 폴더가
**따로 또** 있을 가능성은 배제되지 않았다.

## 2. 그래서 진짜 위험처는 어디인가

repo 가 안전해지면서 위험의 무게중심이 옮겨간다.

### 2-1. ⭐ WSL — 유일하게 확실히 `C:` 에 있다

WSL 배포판 vhdx 는 `%LOCALAPPDATA%\Packages\...` 즉 **C: 사용자 프로필 안**이다.
탐색기 드라이브 목록에 안 보이므로 백업 대상에서 빠지기 쉽다. 여기에만 있는 것:
ORCA r²SCAN-3c 산출물(SDCP 분자 계열) · `~/work/runs/arrhenius_6pt/` MD 런 ·
워치 로그. **재설치 전 `wsl --export` 가 이 카드의 1순위 행동이다.**

⚠ 단 `D:\archive\Linux_Workspace\linux_disk.img`(백업 C)는 **이것과 다른 것**이다 —
2026-08-20 에 "등록된 배포판 두 개가 모두 다른 경로를 가리킨다" 로 **고아 판정**한
DEM 작업환경 이미지다. C 가 있다고 해서 현행 WSL 이 백업된 게 아니다.

### 2-2. C: 에 남아 있을 것들 (미조사)

Windows 쪽 로컬 전용: Origin `.opju` · VESTA 설정 · ssh 키(`%USERPROFILE%\.ssh`) ·
`.claude` 설정/자격증명 · miniconda 환경 · 다운로드/바탕화면/문서. **한 번도 조사 안 했다.**

### 2-3. OneDrive — "동기화됨" 을 눈으로 확인

`OneDrive - 한양대학교` 에 *이 장치에서만 사용 가능* 이거나 동기화 대기 파일이 있으면
클라우드에 없다. 아이콘 상태 확인 전에는 안전하다고 보지 않는다.

## 3. ⛔ 대신 커진 위험 — 단일 실패점이 더 나빠졌다

`offline_archive_index_2026_08_20.md` §4-0/§4-1 이 이미 경고한 것이 이번 판독으로
**한 단계 악화**된 형태로 확인된다:

- 백업 A(KISTI 47 GB) · B · C(DEM 이미지 48.8 GB) — 모두 `D:`
- **그리고 작업 중인 repo 사본 7개도 전부 `D:`**

repo 안에는 `.gitignore` 가 빼는 **되살릴 수 없는 로컬 전용 자산**이 산다:
`litdb/inbox/`(논문 PDF 원본 — repo 엔 digest 만) · `docs/uploads/` ·
`*.cube` · `docs/figures/bvse_cubes/` · `webapp/results/` · `webapp/archive/` ·
`webapp/mpm_lab/`. (재생성 가능한 것: `venv/` `.venv/` `__pycache__/`)

⇒ **T7 Shield 하나가 죽으면 백업 3벌 + 미푸시 커밋 + 커밋 불가 원자료가 동시에 사라진다.**
KISTI 원본은 남아 있지 않다(1저자, 2026-08-20). **재설치보다 이쪽이 더 급한 위험이다.**

## 4. 실행 순서 (재설치 전)

1. **WSL 내보내기** — `wsl --shutdown` → `wsl --export <배포판> D:\wsl_backup\<이름>.tar`.
   배포판 이름은 `wsl -l -v`, 실제 경로는 `HKCU:\Software\Microsoft\Windows\CurrentVersion\Lxss` 로 확인.
   복원: `wsl --import <이름> D:\wsl\<이름> D:\wsl_backup\<이름>.tar`
2. **C: 실사** — `Get-ChildItem C:\ -Directory`. §1 의 판독을 확정하고, §2-2 를 목록화.
3. **미푸시 커밋 회수** — D: 의 repo 7개에서 `git log --branches --not --remotes --oneline`.
   푸시된 커밋은 GitHub 에 있으므로 폴더 자체는 급하지 않다. **미푸시분만 급하다.**
4. **OneDrive 동기화 상태 확인.**
5. **이중화** — §3 때문에, 최소한 `litdb/inbox/` 와 백업 A 의 cube 는 D: 밖 두 번째
   매체/클라우드로. 이건 재설치와 무관하게 항상 해야 하는 것이다.

## 5. ⚠ 한계 (지우지 말 것)

1. **C: 실사 안 했다.** §1 은 스크린샷 1장 판독 + 인덱스 카드 교차검증까지다.
2. **WSL 배포판 개수·이름을 모른다.** `wsl -l -v` 출력을 아직 못 받았다.
3. **§2-2 는 추정 목록**이다. 실제로 뭐가 C: 에 있는지 확인 전이다.
4. 재설치 방식(클린 설치 / "내 파일 유지")을 **못 들었다.** 후자여도 `Windows.old` 는
   10일 후 자동 삭제 — 어느 쪽이든 C: 는 휘발로 취급한다.

## 관련

- 원장: `kb/methodology/offline_archive_index_2026_08_20.md` (§0 백업 A/B/C · §4 한계)
- 아티팩트 원장: `db/governance/artifacts.json`
- 커밋 제외 목록의 원본: `.gitignore`
