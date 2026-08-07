# sdcp_poses_qe — QE `scf.in` 유래 자세 (표시용)

`tools/sdcp/scfin_to_struct.py` 가 **계산에 실제로 들어간 기하**를 그대로 꺼낸 것이다.
Phase-A 스캔 xyz 가 아니라 `scf.in` 을 읽는다 — 스캔 셀은 c=40 Å 인데 파이프라인이
슬랩 셀(c=28.79 Å)로 다시 앉히기 때문에, 눈으로 봐야 하는 건 **재배치 후**의 기하다.

## 출처 (xyz 2번째 줄에도 박혀 있다)

| 파일 | nat | 진공 | scf.in |
|---|---|---|---|
| `complex_doped` | 130 | 6.495 Å | `/data/work/runs/sdcp_linio2_binding/phaseB_v7c_slabfirst/complex_doped/scf.in` |
| `complex_neutral` | 131 | 8.014 Å | `…/phaseB_v7c_slabfirst/complex_neutral/scf.in` |
| `slab` | 192 | — | 같은 계열 슬랩 |

셀 공통 a=11.512 · b=18.272 · c=28.790 Å. **UNRELAXED single-point geometry** —
이완된 구조가 아니다. ⚠ `phaseB_v7c` 계열은 `_v2`/`_slabfirst`/`_molfix`/`_refine`/기본
다섯 갈래가 있다. 이 폴더는 **`_slabfirst`** 판이다.

## 표시 프리셋

NiO₆ 팔면체 + **AFM 부격자 색**(NiA 파랑 / NiB 보라). `.vesta` 는 site 단위 색을 쓰므로
원소 Ni 로 뭉개지지 않고 부격자가 살아 있다. 반지름은 분자 `.vesta`(ORCA 판)와 상대
크기가 유지되도록 전체를 상수배 했다(`--vesta_scale`, 기본 1.7).

관례(CLAUDE.md): 구조 배포는 **xyz + POSCAR(.vasp) 페어**. xyz 는 격자가 없으므로
VESTA 에서 Boundary 타일링을 하려면 `.vasp` 쪽을 연다. `.vesta` 는 ASCII 전용 + CRLF
(등재 시점 검증: 비ASCII 0 바이트, 전 줄 CRLF).

## ⚠ 이 자세를 인용하기 전에 읽을 것

`kb/projects/sdcp_phaseB_direction_2026_08_06.md` — 이 자세들로 **Phase-B 를 착수하지
않기로 했다.**

- doped 의 **Li 자리 vs Ni 자리가 9 meV** 차이다(kT 300 K = 26 meV 의 1/3). 즉 어느 자리를
  고르든 **동전 던지기**였다. neutral 만 82 meV 로 갈린다.
- 원인은 `freeze_frac 1.0` — 슬랩을 통째로 얼려서 **표면 Li 가 술폰산 쪽으로 올라올 수
  없다.** 진짜 Li–O 배위(1.90–2.20 Å)는 Li 가 면 밖으로 나오는 것을 동반하는데 그걸
  금지한 채로 216개를 돌렸고, 전부 2.5–2.9 Å 에서 멈췄다.
- 결정: `--freeze_frac 0.85`(최상단 층만 자유)로 **재스캔** 후 판정.

⇒ **이 폴더는 그림/발표용이다. 결합에너지 순위의 근거로 쓰지 말 것.**
