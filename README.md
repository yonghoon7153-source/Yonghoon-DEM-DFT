# Yonghoon-DEM-DFT

배터리 시뮬레이션 연구용 레포지토리.

## 구성

- [`comsol-gpu/`](comsol-gpu/) — **COMSOL 6.4를 원격 GPU 서버에서 배치 실행**하는 파이프라인.
  git/scp로 모델·설정을 연계하고, 배터리 FEM(1D/P2D/2D/3D + phase field)을
  CPU vs GPU(cuDSS)로 실측 비교합니다. 시작은 [`comsol-gpu/README.md`](comsol-gpu/README.md).

> COMSOL의 GPU 가속은 특정 솔버(cuDSS 직접솔버, 시간영역 음향, DNN 대리모델)에만 적용됩니다.
> 배터리 FEM은 **cuDSS 직접 솔버** 경로를 사용하며, 모델 규모에 따라 효과가 크게 다릅니다
> (P2D/1D는 효과 거의 없음, 3D/phase-field는 이득 가능). 자세한 내용은 위 파이프라인 문서 참고.
