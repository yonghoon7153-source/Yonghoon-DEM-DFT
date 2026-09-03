# manifests — 원본을 나르지 않고 "무엇을 봤는가" 를 고정한다

`mode-observability/data/` 는 `.gitignore` 대상이다. 3자 데이터셋의 재배포
권리가 불명확하고, 원본이 크다 (Su 2024 SI 의 EIS 176파일 = 90 MB).

대신 여기에 **manifest** 를 커밋한다: 파일별 sha256·크기·행수·스펙트럼 수와
파일명에서 푼 좌표. 다른 사람이 같은 zip 을 받아

    python3 tools/eis_ingest.py --verify

로 **바이트까지 같은 것을 봤는지** 확인할 수 있다. 수치 결과의 근거가
"내 컴퓨터에 있던 어떤 파일" 이 아니라 **이름 붙은 바이트**가 된다.

| 파일 | 무엇 |
|---|---|
| `su2024_eis.tsv` | Su 2024 (J. Energy Storage 90, 111770) SI 의 EIS 데이터. 생성: `tools/eis_ingest.py --scan` |

## 원본을 어디서 받나

논문 SI 의 zip (`EIS data.zip`) 을 `data/su2024/` 에 푼다. 폴더 구조는
`data/su2024/EIS data/*.txt`.

**출처 주의**: 파일 명명(`EIS_state_I~IX_{25,35,45}C{01..08}`)과 1C = 45 mA 로
보아 Su 2024 가 **선행 공개 데이터셋을 재사용**했을 가능성이 있다. 원 출처는
논문 digest (`wiki/raw/papers/su2024_*.md`) 가 확정한다 — 확정 전에는 이
데이터로 낸 어떤 수치도 출처를 "Su 2024 SI" 로만 적는다.
