# PTFE/LiNiO2 VASP 검증 단계

이 단계는 Gabia UMA 스크린이 끝난 뒤 실행해. UMA가 만든 `DFT_HANDOFF.json`과
`DFT_HANDOFF/*.vasp`를 받아서, 외주처나 VASP 서버에 바로 전달할 입력 묶음을 만든다.

## 무엇을 계산하나

- clean LiNiO2(104) slab
- 고립 dimer와 C10 fragment
- UMA에서 보존한 dimer/C10 접촉 자세
- 같은 azimuth/roll에서 만든 Li-start/Ni-start 대조쌍
- 각 slab/complex의 독립 자기 초기값 `afm_balanced`, `afm_net2`

`afm_balanced`는 임의의 줄무늬가 아니라 정본 QE slab의 Ni1/Ni2 12-Ni 부호 패턴을
1x4 방향으로 네 번 반복한 24+/24- 초기값이야. `afm_net2`는 같은 부호 topology에서
양·음 크기를 비대칭화한 두 번째 시작점이고, 가능한 모든 자기해를 닫았다는 뜻은 아니야.

ORCA 에너지는 흡착에너지 식에 쓰지 않아. ORCA 최적화 좌표만 gas-phase VASP-D3
이완의 시작 구조로 쓴다.

```text
E_ads = E_complex - E_clean_slab - E_fragment
DeltaE_sampled(Ni-Li) = min_(pose,spin) E_Ni-contact - min_(pose,spin) E_Li-contact
DeltaE_matched-start(Ni-Li) = min_spin E_Ni-start - min_spin E_Li-start
```

`E_ads < 0`이면 0 K 전자에너지 기준 흡착이 유리하고, `DeltaE(Ni-Li) > 0`이면
Li-contact 쪽이 낮다. ZPE·진동·회전·온도 엔트로피를 넣은 자유에너지는 아니야.
`matched-start`는 시작 azimuth/roll을 맞춘 endpoint contrast이고, DFT 이완 뒤에도
두 orientation이 완전히 같다는 뜻은 아니야.

## 계산 규약

- PAW-PBE: `Li_sv / Ni_pv / O / C / F / H`
- Dudarev `U_eff(Ni)=6.2 eV`
- `IVDW=11` (D3), `ENCUT=520 eV`, `PREC=Accurate`
- `LASPH=.TRUE.`, `LREAL=.FALSE.`, `ISYM=0`
- `ISMEAR=0`, `SIGMA=0.05 eV`
- surface/complex: `2x3x1`; dense check: `3x4x1`
- molecule: Gamma only, `IDIPOL=4`
- surface/complex: `LDIPOL=.TRUE.`, `IDIPOL=3`
- 모든 surface 계의 c축을 Cartesian 좌표를 움직이지 않고 `34.6 A`로 통일
- slab 아래 96원자 고정, 위 96원자와 PTFE는 이완
- 최종 자유원자 최대힘 기준: `0.02 eV/A`

각 job은 `relax -> static` 순서로 돈다. static은 반드시 relax의 `CONTCAR`,
`WAVECAR`, `CHGCAR`를 승계한다. dense는 k점이 달라지므로 coarse WAVECAR를 쓰지
않고, static CHGCAR만 받아 `ISTART=0, ICHARG=1`로 시작한다.

## 1단계: pilot

UMA 출력 폴더를 `UMA_OUT`이라고 할 때:

```bash
python3 vasp_stage.py prepare \
  --uma-out "$UMA_OUT" \
  --vasp-out "$PWD/ptfe_vasp_pilot" \
  --scope pilot
```

pilot은 18개 template이야.

- slab 2 magnetic starts
- gas dimer/C10 각 1개
- matched Li/Ni 구조 4개 x magnetic starts 2개
- relaxed dimer 후보 1개 x 2개
- relaxed C10 후보 2개 x 2개

template마다 relax와 static을 실행하므로 VASP 실행은 36회다. pilot은 실행성,
수렴, 분자 보존, Li/Ni registry 유지 여부를 보는 단계이고 site preference 결론은 내지 않아.

## 2단계: 전체 후보

```bash
python3 vasp_stage.py prepare \
  --uma-out "$UMA_OUT" \
  --vasp-out "$PWD/ptfe_vasp_all" \
  --scope all
```

`all`은 UMA handoff에서 geometry gate를 통과한 relaxed 후보와 matched counterfactual
4개를 전부 보존하고, UMA 점수로 더 자르지 않는다. 20/20 relaxed가 eligible이면
complex 24개 x magnetic starts 2개, slab 2개, gas 기준 2개, gas box-check 2개로
총 54 template, relax+static 108회다. UMA가 일부를 안전하지 않다고 격리했다면 실제 수는
`14 + 2 x eligible_relaxed_count`이고 `VASP_PLAN.json`이 정본이야. fragment별 relaxed
후보가 3개 미만이면 VASP package를 만들지 않는다. coarse 결과가
끝나면 analyzer가 matched 쌍, 최저 Li/Ni registry, 최저점에서 0.15 eV 이내 후보와
각 registry 대표를 dense-k 대상으로 자동 선택한다.

## VASP 서버에서 실행

생성된 폴더 안에서:

```bash
cp vasp_vendor.conf.example vendor.conf
vi vendor.conf
bash vasp_run.sh check
bash vasp_run.sh list
bash vasp_run.sh run-all
bash vasp_run.sh collect
bash vasp_run.sh dense       # all scope에서 필수
bash vasp_run.sh archive-final
```

스케줄러를 쓸 때는 `bash vasp_run.sh run-one JOB_NAME`을 사용해. 한 패키지에는 전역
lock이 있으므로 병렬 실행은 패키지 복사본 또는 별도 스케줄러 adapter를 써야 한다.
기존 실패 파일은 삭제하거나 덮지 말고 `archive-partial`로 돌려줘.
중단된 phase를 같은 폴더에서 임의 재시작하지 말고, partial archive와 로그를 먼저
돌려준 뒤 새 package copy/attempt에서 다시 시작해. 이 규칙은 실패 원인과 입력을 보존하려는 거야.

## 자동 차단 조건

- 전자/이온 수렴 또는 정상 종료 누락
- 최종 자유원자 힘 `>0.02 eV/A`
- C-C/C-F/C-H 결합의 절단·새 결합·비정상 단축
- fragment 탈착, 원자 충돌, 주기 이미지 간격 실패
- dimer의 인공 H cap이 주 접촉점이 됨
- Li-start와 Ni-start가 DFT 이완 뒤 목표 registry를 유지하지 못함
- 48개 Ni local-moment 표 누락
- dense-k에서 `DeltaE(Ni-Li)`가 10 meV보다 크게 변함
- gas box 크기 변화로 고립분자 에너지가 10 meV보다 크게 변함
- headline `E_ads`가 `2x3x1 -> 3x4x1`에서 10 meV보다 크게 변함
- 같은 surface 구조의 자기 초기값 두 개 중 하나라도 분석에서 탈락함
- OUTCAR의 `SYSTEM/NIONS/NKPTS/IVDW/LDAUU`가 생성 계획과 다름
- 고정 96원자 이동 또는 fixed-cell drift
- 같은 자기 seed의 clean slab 대비 상부 Li `>0.8 A`, Ni/O `>0.5 A` 재구성 또는
  Li의 다중 O 배위 상실(흡착이 아니라 reaction/extraction endpoint로 격리)

최종 registry는 시작 폴더 이름이 아니라 DFT `CONTCAR`의 multi-F Li/Ni/O contact count와
nearest-F 거리로 `Li/Ni/O/mixed/other`를 다시 분류한다. O-top·bridge·hollow를 Li/Ni로
강제하지 않는다. 두 시작 구조가 같은 final registry로 합쳐지거나
Li/Ni 목표 registry를 각각 유지하지 못하면 contact contrast는 `BLOCKED`다. 이 자동
registry는 완전한 구조 basin clustering을 대신하지 않으므로 최종 구조도 눈으로 봐야 해.

## 결과 문구의 한계

자동 분석이 수치 gate를 통과해도 상태는
`NUMERIC_PASS_FIXED_U6.2_D3__MANUAL_MAGNETIC_AUDIT_REQUIRED`까지만 올라간다.
Ni occupation matrix와 local moment를 사람이 확인하기 전에는 최종 확정이 아니다.
또한 이 결과는 다음 범위로 써야 한다.

> Within the finite-candidate, fixed-axis, 1x4 fixed-coverage LiNiO2(104) model and the PBE+U(6.2)+D3 protocol.

dimer는 H-cap, C10은 CF3-cap이라 두 `E_ads`를 chain-length trend처럼 직접 빼면 안 돼.
U·dispersion·coverage·slab-thickness 민감도까지 하지 않았다면 방법 독립적인 고유
site preference라고도 쓰면 안 된다. `mixed`/bridge-like basin이 더 낮으면 Li-vs-Ni
수치는 pairwise contact contrast일 뿐, 전역 선호 site가 아니다.

## 반환물

`bash vasp_run.sh archive-final`이 만든
`ptfe_linio2_vasp_results.tar.gz`를 그대로 돌려줘. licensed POTCAR, WAVECAR, CHGCAR,
CHG는 파일명 blacklist가 아니라 명시적 반환 allowlist로 제외한다. `OUTCAR`, `OSZICAR`,
실제 `INCAR/KPOINTS/POSCAR`, `POTCAR.spec`, `SOURCE.json`, 분석 CSV/JSON/MD는 보존한다.
`RUNTIME_METADATA.txt`에는 실제 POTCAR의 SHA-256/TITEL, host, VASP 실행 명령,
상속받은 WAVECAR/CHGCAR 입력 해시가 남는다. POTCAR 본문은 반환하지 않는다.
`POTCAR_LIBRARY_COMPONENTS.sha256`은 최초 확인한 각 PAW component의 uncompressed
content hash를 고정해서 phase/job 사이에 같은 TITEL의 다른 release가 섞이는 것도 막는다.

`archive-final`의 `final`은 **계획한 계산·구조·자기표·protocol 감사가 완결된 반환물**이라는
뜻이야. 두 gas-box나 `E_ads`/Li-Ni contrast의 10 meV gate가 실패해도 그 실패 자체가
중요한 결과라 tarball은 만들고, 분석 상태를 `BLOCKED_*` 또는 `UNRESOLVED_*`로 남긴다.
따라서 archive가 만들어졌다는 사실을 `E_ads`나 site preference의 수치 통과로 읽으면 안 돼.
