> 현재 작업 폴더 정정: 비교 기준 메타데이터를 실제 Caps300R80H0500 소스·작업 ID로 교정했다. 수치·CSV·MPH·그림은 바뀌지 않았다. [정정 내역과 전후 SHA](../radial160_timecap/corrections/CORRECTION_LOG_KO.md), [현재 메타데이터 명세](current_metadata_manifest.json)를 참조한다.
>
> 이 폴더의 package_manifest.json 및 기존 ZIP·영수증은 **원래 전달 ZIP의 불변 기록**이다. 정정된 현재 파일 트리의 명세로 사용하지 않는다. 현재 메타데이터는 위 정정 ledger와 새 전달 패키지 manifest로 검증한다.

# COMSOL 6.3 — 300/160 단일 5초 진단 전달본

새300/160 계산 한 번만 수행했다. 기존 Caps300R80H0500은 비교 기준, Caps300R40H0500은 같은 시각의 추세 참조이며 재실행하지 않았다.

80→160의 최대 전압 차는1.248218114 mV @.01초로1 mV 기준을 넘었다. 최대 표면 x 차는2.091183902e-5 @.01초, 음극 z52 µm로 기준 안이다. .04초의 차이 .690286131 mV만으로 통과시키지 않았다. 전체 수렴과160 시간 정확도는 미입증이며 장시간 GO는 아니다.

- [결과·동시 분해·같은 시각 세 수준 추세](RADIAL160_RESULTS_KO.md)
- [정확한 수치 및 CSV 목록](results/analysis.json), [독립 수치 검토](results/independent_review.md)
- [실제 메시·자유도·accepted step](native_steps_summary.json), [독립 native 감사](INDEPENDENT_NATIVE_AUDIT.md)
- [소스 SHA](source_configs.json), [고정 설정 및 현지 보존 확인](final_checks.json)
- [ZIP 생성본·수신본 식별](zip_identity/TIME_CAPS_ZIP_IDENTITY_KO.md)
- [NEXT_RUN_PLAN](../NEXT_RUN_PLAN.md), [그림 PNG](figures/radial160_comparison.png), [PDF](figures/radial160_comparison.pdf)

## 구성과 재현 범위

ZIP은 작업 폴더의 상대 경로를 유지한다. 새160의 소스·CSV14개·전체 로그·request/status·staged/generated Java·저장 MPH를 포함한다. 기존40/80 비교용 원시CSV·로그·소스·설정도 포함하며 그 모델 MPH는 중복 전송하지 않는다. 새 분석 코드는 기본적으로 동봉된 세job만 읽고 새 solver를 실행하지 않는다.

```text
python work/radial160/analyze_results.py
python work/radial160/extract_steps.py
```

첫 명령은187개 정확한 공통 저장 시각의80→160 비교와 같은 시각40/80/160 추세를 재계산한다. 두 번째는 새160의 실제step을 확인한다. 결과는 outputs/radial160/에 다시 쓰므로 전달 원본을 보존하려면 작업용 사본에서 실행한다. 기본 분석은 Python 표준 라이브러리, 그림은 Matplotlib/NumPy를 사용한다. 설치·캐시·임시 fixture는 포함하지 않았다.

과거333 보관 바이트의 검증용으로 현지 PREFLIGHT ZIP·외부manifest·SHA영수증·이전333 ledger와 work/time_caps/zip_identity_verify.py를 포함한다. `python work/time_caps/zip_identity_verify.py --root .`로 검증할 수 있다. 이는 보관 바이트의 검증이며 현지 현재468/663 파일 전체의 원격 검증이 아니다.

이전 TIME_CAPS 생성본 raw ZIP(325,347,218 bytes / beac1f1d…3f0268)은 중복 전송하지 않는다. 그 식별 영수증·manifest 및 직접 검사 결과는 포함한다. zip_identity_time_caps.py로 당시 생성본 전체를 다시 검사하려면 해당 이전 생성본 ZIP이 별도로 필요하다. 사용자 수신본325,367,172 bytes /74aa78d2659ed0f4a915a9a4150ccacf4a7f8976a5ad4dd4d38e48c6ace6d0b7의 raw 식별과201 payload·manifest 성공은 사용자 보고로 구분한다. 두 raw ZIP의 차이 원인은 미확인이다.

준비·현지 보존 검사 스크립트는 기존 작업 폴더의 전체663개 원본을 필요로 하므로 새 전달본만으로 해당 현지 검사 전체를 재현할 수 있다는 뜻은 아니다. 비교에 필요한40/80/160 원자료는 모두 동봉했다.

## 보호와 실행 종료

OCP 표·초기 조성·Li 재고·입자 물리 반경을 유지했다. OCP 외삽 금지와 기존 OCP입력·고체표면조성 StopCondition은 유지한다. 전해질 양수는 후처리 검사이며 실시간 음수 중단은 미구현이다. 과거 failed·INCOMPLETE_RANGE_STOP은 보존하고 다른 실패를 같은 분류로 자동 처리하지 않는다.

이번 한 번 밖의320요소·다른 시간상한·600/80·전체 프로토콜·12시간 휴지·기준값 외 sigma·sweep은 실행하지 않았다.

## 포장 무결성

package_manifest.json은 자기 자신을 제외한 모든 payload의 경로·크기·SHA를 기록한다. 생성 후 전체 ZIP의CRC와각payload SHA를 확인하고, 최종 ZIP에 든 네 과거 입력으로333개 보관 바이트도 다시 확인한다. 생성본 ZIP 자신의 SHA와 manifest SHA는 ZIP 옆 영수증에 적는다. 이것은 **이 PC에서 생성한 포장본의 식별**이며 아직 관측하지 않은 새 수신본의 SHA라고 주장하지 않는다. ZIP 압축이나 메타데이터가 바뀌면 raw SHA와 내용manifest 검증을 별도로 기록해야 한다.
