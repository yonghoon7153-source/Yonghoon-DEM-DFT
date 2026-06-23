# 모델에서 cuDSS(GPU 직접 솔버) 켜기

> **핵심:** 배터리 FEM의 GPU 스위치는 CLI 플래그가 아니라 **모델에 저장된 Direct 솔버 종류**다.
> `comsol batch`로 그냥 돌리면 모델에 저장된 솔버(보통 CPU MUMPS/PARDISO)로 돈다.
> scp로 올려서 실행만 하면 **GPU로 안 돈다.** 먼저 cuDSS로 바꿔 저장해야 한다.

COMSOL 6.4부터 Direct 솔버 선택지에 기존 3종(MUMPS / PARDISO / SPOOLES)과 함께
**cuDSS (CUDA Direct Sparse Solver)** 가 추가됐다. 단독 솔버, 전처리기, 비선형·암시적
시간의존 해석 어디에나 쓸 수 있다.

---

## 방법 1 — GUI (가장 확실, 권장)

1. COMSOL Desktop에서 모델(.mph) 열기
2. 모델 트리: **Study ▸ Solver Configurations ▸ Solution N ▸
   Stationary Solver(또는 Time-Dependent Solver) ▸ Direct**
   - (Direct 노드가 안 보이면, 현재 반복(Iterative) 솔버를 쓰는 것. 직접솔버로 바꾸거나
     반복솔버의 전처리기를 Direct로 두고 그 Direct를 cuDSS로 설정)
3. **Direct** 노드 선택 → Settings 창의 **Solver** 드롭다운을
   **"CUDA Direct Sparse Solver (cuDSS)"** 로 변경
4. (선택) 정밀도(precision) 등 cuDSS 옵션 확인
5. **저장**(Ctrl+S). 이 저장된 .mph를 서버로 보낸다.

> GPU 없는 PC(예: 노트북)에서도 cuDSS를 *선택해 저장*하는 것은 가능하다(설정값일 뿐).
> 실제 GPU 실행은 GPU 서버에서 일어난다. 단, GPU 없는 곳에서 풀면 경고가 날 수 있다.

검증: `File ▸ Preferences ▸ Computing ▸ GPU Acceleration ▸ Verify CUDA Installation`,
같은 화면에서 **cuDSS 라이브러리 경로**도 확인.

---

## 방법 2 — Record Method (자동화용, 정확한 API 코드 확보)

모델마다 솔버 노드 태그(`s1`, `d1`, `sol1` …)가 다르므로, **정확한 코드는 직접 녹화해서**
얻는 게 안전하다(임의 추정 금지).

1. **Developer 탭 ▸ Record Method** 클릭(녹화 시작)
2. 위 *방법 1*의 드롭다운 변경을 한 번 수행
3. 녹화 중지 → COMSOL이 생성한 **정확한** 자바 형식 코드를 확인
   (대략 아래와 비슷하지만, 노드 태그/속성명은 **네 모델에서 나온 값을 그대로** 쓸 것)

```java
// 예시(반드시 Record 결과로 대체). sol/feature 태그는 모델마다 다름.
model.sol("sol1").feature("s1").feature("dDef").set("linsolver", "cudss");
// 또는 Direct 노드가 "d1" 인 경우:
// model.sol("sol1").feature("s1").feature("d1").set("linsolver", "cudss");
```

4. 이 코드를 **모델 메서드**로 저장하거나, 빌드 시 호출하도록 두면 배치에서 재현 가능.

> 속성명(`linsolver`)과 값 문자열(`cudss`)이 버전/노드에 따라 다를 수 있어 **추정하지 말고
> Record로 확인**하는 것을 권장. 이 파이프라인의 `parse_log.py`가 실행 후 로그/`nvidia-smi`로
> "GPU 실제 사용 여부"를 검증하므로, 설정이 틀리면 경고로 바로 잡힌다.

---

## 벤치마크용 쌍둥이 파일 만들기

CPU vs GPU를 공정 비교하려면 **물리/메시는 같고 솔버만 다른** 두 파일을 두는 게 깔끔하다.

- `0.1C_31x31x40_LPSCl_5e-6_bulk.mph`      → Direct = **cuDSS** 로 저장 (GPU)
- `0.1C_31x31x40_LPSCl_5e-6_bulk_cpu.mph`  → Direct = **PARDISO** 로 저장 (CPU 기준선)

그 후:

```bash
bash scripts/benchmark.sh --cpu lpscl_3d_bulk_cpu --gpu lpscl_3d_bulk
```

---

## 잘 안 될 때

| 증상 | 원인/조치 |
|------|-----------|
| nvidia-smi 사용률 0% | 모델 Direct 솔버가 cuDSS가 아님(저장 누락) 또는 반복솔버 사용 중 |
| `out of memory` (GPU) | 3D 인수분해가 VRAM 초과 → 메시/물리 축소, 또는 CPU iterative로 전환 |
| cuDSS 항목이 드롭다운에 없음 | 6.4 미만이거나 GPU Compute Components 미설치 → 재설치/버전 확인 |
| 작은 모델인데 안 빨라짐 | 정상(P2D/1D). GPU 대신 배치 스윕 throughput 사용 |
