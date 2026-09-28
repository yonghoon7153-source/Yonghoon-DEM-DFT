# 출처와 증거 경계

## 제출물

사용자 첨부 `d3cf1ea4-c9de-4bc7-801a-0e9c7558e850/붙여넣은 텍스트.txt`, 2026-09-29 초안. 새 코드 커밋은 지정되지 않았다. 원본/정규화 사본의 해시는 README와 MANIFEST에 기록한다.

## 기준 소스

Repository: yonghoon7153-source/Yonghoon-DEM-DFT.
Pinned commit: `18787ab98a13361c37b2343bd07ae276142d0953` (6차 리뷰 기준).

- `scripts/make_mixer_deck.py`: Git blob `033fac54d73566ac1dad54f24cc28b9d0510ccbc`, SHA256 `2c12184e9d803e1a9fc4d58b5e32d2de0800b11f637797f68e637d3f85507251`. 매 audit 실행에서 blob을 대조한다.
- `scripts/measure_mixing_index.py`: 해당 핀의 보존 소스. line 279 분모 가드, line 317 M 식. 새 패치 인증이 아니다.
- `baseline/prior_r6_verdict.md`: 독립 6차 판정문. 이번 §7은 그 §5-3⑩의 무조건 코호트 분리 문구를 명시적으로 정정한다.

## 1차 외부 근거 (2026-09-29 열람)

- [NIST mean confidence limits](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm): t 평균 CI의 형식/가정. 실제 seed ensemble의 정규성을 입증하지 않는다.
- [Lakens 2017, author-institution publisher PDF](https://pure.tue.nl/ws/portalfiles/portal/80918653/lakeequi2017.pdf): 동등성/비유의성 구분, 두 단측 검정과 CI. 원문 재배포하지 않는다.
- [Slurm sbatch](https://slurm.schedmd.com/sbatch.html): 처음부터 --hold 제출의 의미. 실제 ibb 설정 확인은 아님.
- [Slurm scontrol](https://slurm.schedmd.com/scontrol.html): hold/release 및 이미 실행 중인 job에 hold할 때의 한계.
- [LIGGGHTS-PUBLIC SJKR implementation](https://raw.githubusercontent.com/CFDEMproject/LIGGGHTS-PUBLIC/master/src/cohesion_model_sjkr.h): 구 교차 면적/벽 면적의 유한 겹침 및 area_ratio. upstream master는 실제 ibb 바이너리의 해시/동일성 증거가 아니다.

외부 문헌은 수치 반례의 입력 자료가 아니다. 모든 표의 F0 역산, CI, 검정력, 판정 반례는 audit 스크립트가 재계산한다. 합성 반례가 실제 DEM 궤적에서 발생했다는 주장을 하지 않는다.
