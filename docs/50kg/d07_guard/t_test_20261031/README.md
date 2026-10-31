# D0.7 이어 돌리기 `-T` 시험 (10-31 · ibb · 1저자 화면 반입)

- 명령 (1저자 10-31 21:58 KST): 멈춘 폴더 `kg50_d07_b50` → `kg50_d07_b50.main1031` 로 옮긴 뒤 `bash ~/dem_test/scripts/resume_ckpt.sh -T -n 56 -s main1031 -r ~/dem_test kg50_d07_b50` (nohup).
- 결과 = G0–G3 통과 · 본 제출 안 함 (`-T`) · 시험 job 335411 · 끝 step 202,002 (= S0 200,001 + run 1 + run 2,000) · 도구 sha256 = 10-30 GO 판 (`2dc7f693…`).
- 원문 = `report_resume_r56_1031_215830.md` (보고 그대로) · `attempts_and_identity.txt` (시도 폴더 둘의 영수증 · result · job · 신원 줄 그대로).

## 지킴이 v2 승인값 (이 보고에서)

| 자리 | 값 | 출처 |
|---|---|---|
| `-T` 시도 | `attempt_r56_1031_215830_2483798` | 보고 머리 · `ls -d` |
| 이어받은 시도 (10-30 본 job 333911 의 시도 · 멈춘 폴더에서 같이 복사됨) | `attempt_r56_1030_152123_2568313` | `ls -d` (사전 공격 R2-08 실제 확인) |
| 영수증 sha256 (`main_inputs.sha256` 파일 전체) | `a22a9b9fa18782f1a02b5728c05272ef735f46fd3dba8f2441b0213b2b6a94c9` | 붙여 넣은 다섯 줄을 `sha256sum` 꼴 (두 칸 · 줄 끝 개행) 로 다시 만든 값 — **같은 방법으로 10-30 시도의 다섯 줄을 다시 만들면 v1 승인값 `29ff619a…` 와 정확히 같다** (방법 검증) · 지킴이가 시작 때 실제 파일과 다시 대조 |
| 본 덱 sha256 (`input_kg50_d07_b50_r56.liggghts`) | `4bf5ab86f95047e4e5607bba77c4ae75b2d93e3a6a96b776c3c4fe90f04899f3` | 영수증 1 줄 |
| 체크포인트 sha256 (`restart_after_settling.bin`) | `45a838c18d19e3c1399a97f5948d52ad0995490f6a55040e6a6ffec8fecd2d70` | 영수증 5 줄 = 정지 기록 (`docs/50kg/d07_guard/README.md` ⑥) = 시험 신원 줄 |
| lmp_mpi sha256 | `ee2d77261bac9e7fa4e9311c8709e74bf7583a13225a5bc35a791bef9be60a3f` | 시험 신원 줄 (10-30 과 같음) |
| 도구 sha256 (`-A` · `-H`) | `2dc7f693263708d7788ab721386182c6109a8f9278797ecc43f5165d6715f1e8` · `d6e590a18849d10c70dc831d5e8bebabf3a5163d502d5968db9688a70a29d7c8` | 보고 머리 (리포 `scripts/resume_ckpt.sh` 와 같은 sha256) |

- ⛔ 보고 끝 "본 제출 명령" 줄 = Codex 한 건 범위 GO 뒤에만 (지킴이 v2 와 함께) · 요청서 `docs/50kg/report_y4/codex_kg50_y4_draft2_request_20261031.md` Q4.
