# lottery — 로또 6/45 · 연금복권720+ 전 회차 분석과 번호 생성기

브랜치 `claude/lottery-site` 의 독립 프로젝트다. 이 모노레포의 배터리 연구 코드와 아무것도
공유하지 않고, 이 디렉터리 밖을 고치지 않는다.

## 결론 (숫자의 정본은 `results/analysis.json` · 요약은 `RESULTS.md`)

1. **추첨기는 무작위와 구분되지 않는다.** 로또 19개 · 연금 8개 질문 모두 다중비교 보정 후 p = 1.00.
   궁합수 990쌍 중 보정 후 유의한 쌍은 0개다.
2. **머신러닝은 다음 번호를 맞히지 못한다.** 로지스틱 회귀 · 선형/RBF SVM · 나이브 베이즈 · 신경망 2종 ·
   부스팅 · 랜덤 포레스트 · 빈도 전략 7개를 walk-forward 로 951회차 평가했고, 평균 적중이 모두
   무작위 기대 0.8개와 같다. 같은 파이프라인을 진짜 무작위 가상 역사에 돌려도 같은 모양이 나온다.
3. **사람들의 번호 선택에는 뚜렷한 패턴이 있다.** 회차별 5등 당첨자 수(매주 수십만~백만 건)로 추정한
   번호별 인기도가 처음 보는 회차의 5등 비율을 66% 설명하고, 독립 자료인 1등 자동/수동 비율과
   1등 당첨자 수를 예측한다. 1등 당첨금은 나눠 가지므로, 덜 인기 있는 조합을 고르면 1등 시 기대
   수령액이 커진다 (당첨 확률은 모든 조합이 같다).

## 구성

| 파일 | 하는 일 |
|---|---|
| `fetch_data.py` | 동행복권 공식 API 에서 전 회차를 받는다 (요청 2번). 원본 bytes 그대로 `data/raw/` + `MANIFEST.json` (URL · 시각 · sha256). 검증 실패 시 기존 파일 보존 |
| `dataset.py` | 원본 → 검증된 레코드. 회차 연속 · 요일 · 번호 범위 · 1회 기준값 · 판매액 × 확률 = 5등 당첨자 수(±2%) |
| `combos.py` | 8,145,060 조합 전수 열거로 총합·홀짝·연번·AC값 등의 **정확한** 분포 |
| `stats_tests.py` | 무작위성 검정 (몬테카를로 귀무분포 · Holm/BH 보정) |
| `ml_backtest.py` | walk-forward 예측 백테스트 (sklearn) |
| `popularity.py` | 등수별 당첨자 수 → 번호 선택 인기도 (OLS·HAC, 포아송·이항 GLM, SVR 비교, 양성 대조) |
| `generative.py` | 확산 모델(DDPM, 강의 설정 그대로) · EM 베르누이 혼합 |
| `build_results.py` | 위 전부 → `results/analysis.json` + `RESULTS.md` |
| `webapp/` | 결과 열람 + 번호 생성기 (Flask, 본체 webapp 형식) — `webapp/README.md` |
| `tests/` | 검증기 변형 테스트 · 검정 도구 귀무 보정 · 누수 검사 · JS↔파이썬 대조 · 웹앱 라우트 |

## 다시 만들기

```bash
pip install -r lottery/requirements.txt
python lottery/fetch_data.py
python lottery/build_results.py
python -m pytest lottery/tests -q
lottery/webapp/lotto.sh
```

## 쓰지 않는 것

당첨 확률을 올린다는 주장. 이 프로젝트의 모든 결과는 "과거 번호로 미래 번호를 맞힐 수 없다"와
"사람들이 고르는 번호는 고르게 퍼져 있지 않다" 두 가지다. 로또는 판매액의 절반을 당첨금으로 돌려주는
게임이라 한 장의 기대값은 구입액보다 작다. 도박 문제 상담: 한국도박문제예방치유원 1336.
