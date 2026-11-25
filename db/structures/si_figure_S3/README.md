# SI Figure S3 — 산화(탈양성자) 올리고머 구조

원고 SI Note 2 의 구조 그림 원본. **계산된 구조 그대로**이고 재최적화·재중심 외의 손질은 없다.

| 파일 | 계 | 원자 | 도핑 자리 | 원본 |
|---|---|---:|---|---|
| `n2_doped.*` | n = 2 (dimer, D•) | 67 | A-ring | `db/structures/sdcp_v7c_dimer_doped.xyz` |
| `n3end_doped.*` | n = 3, 말단 고리 산화 | 100 | end(A) | `db/structures/sdcp_v7c_trimer_doped_end.xyz` |
| `n3mid_doped.*` | n = 3, 내부 고리 산화 | 100 | mid(B) | `db/structures/sdcp_v7c_trimer_doped_mid.xyz` |
| `n6_doped.*` | n = 6 (D•) | 199 | **ring3** | `db/structures/sdcp_n6_doped_ring3.xyz` (sha256 `0863121a…` — db 기록과 일치) |

n=6 도핑 자리는 라벨이 아니라 **구조에서 찾은 값**이다 — 탈양성자 sulfonate(S=72)에서 곁사슬을
따라가 원자 43(C)이 ring3 에 속한다 (`nseries_n6.py --analyze`, 2026-09-08).

## ⚠ 상자는 계산 셀이 아니다

이 계들은 **비주기 기체상 분자**다. `.vasp`/`.vesta` 의 격자는 VESTA 가 격자를 요구해서 씌운
**보기용 상자**(여백 8 Å/면)이고, 계산에는 셀이 없었다. 상자 크기를 물성으로 인용하지 않는다.

## 배포 규약 (CLAUDE.md)

- `.vesta` 는 ASCII 전용 + CRLF (비ASCII 가 IMPORT 파싱을 깨뜨린 사례가 있다). 생성 시 확인함.
- 구조는 `xyz` + `POSCAR(.vasp)` 쌍으로 배포한다. xyz 에는 격자가 없어 Boundary 타일링은 vasp 로.
- 같은 폴더에 셋을 함께 둔다 (VESTA 가 짝 파일을 같은 경로에서 찾는다).
