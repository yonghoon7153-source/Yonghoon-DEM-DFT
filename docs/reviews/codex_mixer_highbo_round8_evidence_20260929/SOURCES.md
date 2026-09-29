# 출처와 범위

검토일: 2026-09-29.

## 사용자 제공 정본

첨부: codex_mixer_highbo_round8_bundle_20260929.md.
원문은 bundle_original.md에 보존했다. PART 1은 v2.1 핀을, PART 2는 v2.2 본문을 담고 있다. PART 2의 실제 바이트 해시가 v2.2 선언과 일치함을 독립 대조했다. 새 코드 커밋은 발송 메시지에 없었으므로 임의로 최신 HEAD를 가져오지 않았다.

## 고정 기준 소스

이전 7차 증거 폴더에서 make_mixer_deck.py, measure_mixing_index.py를 복사했다. 기준 commit은 18787ab98a13361c37b2343bd07ae276142d0953이다. 생성기는 실제 Git blob 산술로 033fac54d73566ac1dad54f24cc28b9d0510ccbc임을 감사 프로그램에서 강제한다. baseline/prior_r7_verdict.md는 이전 회신을 대조하기 위한 참고 문서이며 과학적 사실의 독립 증거가 아니다.

생성기 plan(), ced_matrix(), deck()의 호출은 함수 산술·메모리 문자열 계산이다. 실제 DEM 실행이 아니다. 해당 출력은 기준 소스의 반례이며, 아직 제출되지 않은 새 stiffening 구현의 검증 결과로 승격하지 않는다.

## 직접 열어 확인한 외부 1차 자료

- Nosek et al. (2018), The preregistration revolution, PNAS.
  https://www.pnas.org/doi/10.1073/pnas.1708274114
  관련 근거: 결과 관측 전 분석 계획과 확인/탐색 구분. 이번 설계의 구체적인 허용 조건은 리뷰어의 적용·추론이다.
- LIGGGHTS 공식 run 문서.
  https://www.cfdem.com/media/DEM/docu/run.html
  관련 근거: run 분할과 start/stop, pre/post 제어.
- LIGGGHTS 공식 read_restart 문서.
  https://www.cfdem.com/media/DEM/docu/read_restart.html
  관련 근거: processor 변경, 재시작 정확성의 제약, granular 속도 의존 힘과 fix 상태.
- LIGGGHTS 공식 fix insert/pack 문서.
  https://www.cfdem.com/media/DEM/docu/fix_insert_pack.html
  관련 근거: 병렬 삽입 분배·부분영역 경계·겹침 검사.

이 문서들은 이번 서버의 특정 바이너리/컴파일 옵션이나 NP 간 실제 M 차이를 측정한 증거가 아니다. 본문에서 그 점을 분리했다.

## 수행하지 않은 것

DEM/MPI/SLURM/ibb 접속·발사·해제, 실제 캠페인 M/겹침 열람, 생산 코드 수정, Git 메타데이터 변경, 원격 최신 코드 수집, 새 기술 선행조건의 인증.

