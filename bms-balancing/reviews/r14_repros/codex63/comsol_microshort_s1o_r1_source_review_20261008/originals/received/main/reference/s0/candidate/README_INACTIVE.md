# S1 Java 후보 — INACTIVE / REVIEW ONLY

이 폴더는 S0 설계 산출물이다. 실행 승인·검증 release·native 승인·launcher·consumer 연결을 제공하지 않는다. COMSOL, JVM, Java compile, supplied-program import/execution, 테스트 실행은 모두 0이다.

- `MicroshortS1RestCandidate.java.inactive.txt`: 전 원본을 보존적으로 복제하여 제안 변경을 구체화한 텍스트. main/run, private model sketch, preflight entry 모두 거부한다. 실제 runAll 호출을 제거했고 파일 export와 기존 환경 경로도 제거했다. 활성화 스위치가 없다.
- `S1_REVIEW_ONLY.diff.txt`: 원본 대비 unified diff. 저장소/생산 원본에 적용하지 않았다.
- `LITERAL_CHANGE_MAP.json`: 변경 전·후 정확 문자열과 원본/후보 시작 줄. 20개 치환이며 각 원문이 단 한 번 존재함을 텍스트 대조했다.
- `REQUESTED_TIMES_S1_3600.txt`: 401개 요청 시각.
- `SOURCE_PROVENANCE.json`: 원본 pin/바이트/hash.
- `LIMITED_STATIC_REVIEW_PLAN.md`: 변경부 검토와 후속 검증의 분리.

제안 config: xN=.445, xP=(nLi_target-epss_el*L_el*cs_Gr_max*xN)/(epss_pos*L_pos*cs_NCM_max)=.5811516557009895 (부모 오프라인 산술); sigma 1e−20 / 1.7e−8 / 1.7e−7 / 1.7e−6 S/m. 후보 상수의 기본값은 단일 1.7e−7이며 sweep를 실행하는 코드는 없다. i_app=0, T=3600s. 원래 LLI/LAM·epss_short=.55·NoCorr·물성/OCP·mesh/입자·CDI 생성은 유지한다.

401 시각 = 기존0–5s187 +5.5:.5:30의50 +35:5:300의54 +330:30:3600의110. 요청격자는 파일로 고정했다. tstepsbdf=strict, tout=tlist, cap=.000125s(t<.1), .1s(.1≤t<5), .5s(5≤t<30), 5s(30≤t<300),30s(t≥300); rtol=1e−6. 저장은 full solution fields이며 선택 변수 저장 API는 추가하지 않았다. 공간 프로파일·guard·재고·반응 출력은 유지한다.

새 출력은 기존 field `liion.Isx` 기반 j_leak, 모델 면적 A_c를 곱한 I_leak(A), sigma, RN/RP 및 boundary2/3의 phis다. 분리막 단면류를 길이방향 적분한 양을 그대로 I(A)로 부르지 않는다.

**native-ready가 아닌 이유:** finite-sigma CDI/consistency 미검증, 새 rest 초기값 미검증, cap/storage bridge 미실행, 새 출력 설치본 평가/consumer contract 미검증, 예산/중단을 집행하는 실행 패키지 미준비. 원 NORMAL480 launcher/consumer는480s dense grid 계약이므로 그대로 연결할 수 없다. 이후 작업은 사용자 별도 승인 범위에서 새 고정 실행본·계약을 준비해야 한다.

정적 원본 hash: `c70526cf6884eabc57b63dd43dce4b47fb0decf59af68d3f550f1b987d053797` /99,959B.
후보 hash: `a90d1e66db796f6b8077fa1d158620d1ec548265a1508b698e35da8ef6e3492c` /77,277B.
diff hash: `ae8d8246e010b8bdb310e03e34d2bfcb6bc506922c5a9ee9d1e8949b06b52791` /42,205B.

