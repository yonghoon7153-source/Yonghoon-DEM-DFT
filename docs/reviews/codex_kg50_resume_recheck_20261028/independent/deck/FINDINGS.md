# KG50 재개 도구 — 독립 덱 의미론 검토

핀 `f118c1fd1e3eb1a558299663dcee6a0bf83b9942`. 제품 파일은 수정하지 않았다. 실제 DEM·MPI·SLURM·WSL 실행은 하지 않았다.

검증 방법: `scripts/resume_ckpt.sh` SHA-256 `e59c43e688b2b9a6c23a337ceee2b28214ed3f6c76bd69b7f2402f926336dae8`을 단언하고, 포함된 Python 본문을 바이트 그대로 분리하여 원래 CLI 분기까지 실행했다. Bash 시작이 환경에서 막혀 있어 전체 `test_resume_ckpt.py`의 87개를 실행한 결과라고 주장하지 않는다. 시험 덱 절단은 이번 한 줄 ASCII run 픽스처에 한해 원본 693행 awk의 동작을 그대로 적용하여 바이트를 대조했다.

재현:

```powershell
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -I -X utf8 -B 'C:/Users/Administrator/Documents/Codex/kg28/independent/deck/reproduce_deck.py'
```

세부 stdout·rc·입력 경로·trial-prefix SHA-256은 같은 폴더 `results.json`에 있다. 아래 ID는 부모 검토의 최종 ID 배정 전 임시 ID다.

## DECK-01 / P1 — 제공된 압축 재개 정상례가 압력 확인을 4,998 step 늦춘다

- 위치: `scripts/resume_ckpt.sh:367-385`, 특히 `385`의 루프 몸 전체 명령 일치.
- 원자료: `docs/data/pure_se_r075_20260927/input_pse_r075_a.liggghts:71,85,90,123,130-136`; 재개판 `input_pse_r075_a_r30.liggghts`.
- 실제 CLI: 요청서와 같은 original/resume/`restart_compress_1500000.bin`/`S0=1500000`를 넣으면 **rc=0**, `루프 몸 run 같음`이다.
- 원 덱의 루프 시작 = `1+200000+1+200000 = 400002`. 루프 몸 첫 긴 run은 5,000 step이므로 압력 확인 시점은 `400002 + 5000*n`이다.
- checkpoint `1500000`은 해당 몸 run의 4,998번째 step이다. 원 덱 다음 압력 확인은 **1500002**, 남은 길이는 **2**다. 재개판은 `run 5000`을 실행하므로 다음 확인은 **1505000**이다.
- 원 덱 18·20행 dt=`1.0e-6`이므로 이 차이는 계산 시간 **4.998 ms**다. 첫 run 숫자만 2로 바꾼 후보는 rc=1(루프 몸 run 순서 다름)이다. 이 숫자-only 후보 자체가 완성된 수정안은 아니다. 이후 반복까지 2가 되지 않도록 첫 부분 반복과 정상 5,000 step 반복을 분리해야 한다.
- 무너지는 결론: 이 루프가 지원 범위 안에서 원 덱의 남은 실행 순서를 보존한다는 주장. 이는 명시된 한계인 ‘루프 몸 둘째 긴 run 도중’이 아니라 **첫 긴 run 도중**, 그리고 요청서가 정상으로 제시한 바로 그 덱이다.
- 한계: 실제 압력·최종 두께의 변화량은 계산하지 않았다. 4,998 step 지연은 덱 산술이며 압력 오차의 측정값은 아니다.
- 최소 해결: restart step의 루프 내 위치와 다음 원래 판단 시점을 결정할 수 있어야 한다. 첫 부분 run의 나머지만 수행한 뒤 원래 압력 조건을 검사하고 이후 반복은 원래 5,000 step으로 돌아가야 한다. 이를 입증하지 못하는 압축 checkpoint는 pretrial에서 거부한다. 단순히 원본의 `run 5000` 문자열과 일치시키는 것은 충분하지 않다.

## DECK-02 / P1 — 첫 run의 동작을 trial이 삭제하고 정적 검사가 허용한다

- 위치: `scripts/resume_ckpt.sh:351-365`, `693`, `703-706`.
- 정상 settling의 첫 `run 180000`을 다음 한 줄로 바꿨다.

```text
run 180000 every 1000 "velocity all set 1.0 0.0 0.0"
```

- 원래 embedded CLI **rc=0**, `남은 step 같음: 끝 200001`이다. 이 분기는 숫자와 끝 step만 검사하고 run의 나머지 인자를 검사하지 않는다.
- 693행은 해당 줄 전체를 `run 2000`으로 바꾼다. 변이 trial은 정상 trial과 **바이트 전체가 동일**하고 `--trial-steps`도 rc=0이다. 따라서 짧은 시험에서 every의 속도 변경은 한 번도 실행되지 않는다.
- 추가 대조: `run 180000 pre no`도 rc=0 및 trial 바이트 동일. `run 180000 upto`는 정상적으로 rc=1(끝 step 불일치)이고, `run 200001 upto`는 올바른 절대 종료값으로 rc=0이다. upto를 잡지 못한다고 주장하지 않는다.
- 무너지는 결론: trial의 의미·동작이 본 제출 첫 run의 의미와 같다는 주장. `--trial-steps`는 잘라낸 뒤의 줄을 검사하므로 이미 삭제된 옵션을 복구하지 못한다.
- 최소 해결: 첫 run의 원래 명령을 trial 생성 **전에** 동일 parser로 검증한다. 지원하지 않는 every/start/stop 등은 거부한다. pre/post 등을 허용한다면 trial에도 같은 의미를 보존하는 규칙이 필요하다. 숫자만 뽑아 원래 꼬리를 없애는 변환은 허용 목록으로 입증된 경우에만 적용한다.

## DECK-03 / P1 — 선택된 명령 목록 밖의 상태 변경과 앞쪽 label이 보이지 않는다

- 위치: `scripts/resume_ckpt.sh:40-43`, `274-295`, `326-332`, `395-402`.
- 첫 긴 run 바로 뒤에 각각 다음 명령을 추가하면 모두 **rc=0**이다: `velocity all set 1.0 0.0 0.0`, `set group all density 1.0`, `delete_atoms group all`, `include extra.in`.
- 네 경우 모두 trial은 정상 trial과 바이트 동일하고 `--trial-steps` rc=0이다. B는 FWD에 없는 명령을 건너뛰고, E는 SEQ에 없는 명령을 버려서 비교한다. ‘뒤 순서 동일’은 모든 물리 명령의 동일성이 아니다.
- Q9 반례: 첫 settling run **앞**에 기존 압축 루프와 같은 `label loop_press`를 추가해도 rc=0, trial-steps rc=0이다. 뒤쪽 원래 `label loop_press`·`jump SELF loop_press`는 그대로다. `jump SELF`는 파일을 되감고 처음 만나는 같은 label에서 검색을 끝내므로, 본 제출이 압축 루프에서 settling 구간으로 돌아간다. label 단독이 평소 아무 동작을 안 한다는 사실은 label 이름의 중복이 무해하다는 증명이 아니다.
- Q2 보조 반례: 원래의 `variable target_press equal 0.30` 줄을 삭제해도 rc=0이다. 뒤 압축 if에서 `${target_press}`를 사용한다. F의 존재 검사는 c_/f_에만 있다. 변경 timestep·missing c_zmax 대조군은 rc=1이므로 검사가 전부 꺼진 상황이 아니다.
- 최소 해결: checkpoint 뒤 실행 가능한 명령 전체를 기준으로 비교하고 예외를 좁게 열어 둔다. group·set·velocity·fix_modify·compute_modify·variable 등의 상태/순서/존재가 빠져서는 안 된다. unknown 실행 명령을 비교 대상에서 제거하지 말고 거부한다. label은 전체 파일의 유일성 및 jump 목적지를 대조한다. 이 한계가 남으면 KG50-10의 B+C+E 조합은 충분하지 않다.

label 의미 참고: [고정 LIGGGHTS 소스 Input::jump/label](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/input.cpp#L809-L849). `rewind` 뒤 label 검색 상태를 켜고 첫 일치에서 검색 상태를 해제한다. 현재 ibb 바이너리로 이를 실행한 것은 아니다.

## 좁은 수정 자체의 판정

| 항목 | 독립 결과 | 판정 경계 |
|---|---|---|
| KG50-17 / Q4 | 179999→180000 한 줄만 변경 rc=0, 두 step 부족 rc=1·바이트 보존, timestep 변경 동반 rc=1·바이트 보존 | 산술 보정은 좁고 타당하다. 외부 도구의 원인 증명은 아니다. DECK-03의 suffix 변이를 함께 넣으면 여전히 보정 rc=0이므로 ‘다른 문제 없음’ 전제는 미충족 |
| KG50-16 / Q5 | CRLF·탭 주석을 제거하면서 인라인·따옴표 안 # 및 나머지 바이트 보존 rc=0. continuation 사이 주석 제거는 rc=1·파일 미변경 | 시험한 규약에서 보존 타당. LIGGGHTS 모든 문법을 인증한 것은 아니다. 인라인 이름이 남아 후속 도구에서 거부되는 한계는 안전한 거부로 수용 가능 |
| KG50-19 write_restart | after_settling baseline rc=0, 첫 긴 run 300000으로 변경 rc=1, 감쇠 mismatch rc=1 | 해당 세 반례는 닫혔다. 압축 루프의 시간 위상은 DECK-01 때문에 별도 열림 |
| Q9 | print/quit의 좁은 허용은 endpoint 검사와 함께 조건부 수용. label 무조건 허용은 위 중복 반례 때문에 수정 필요 | pretrial 거부 이유는 최종 영수증에도 남겨야 한다. stdout만으로는 모든 거부 사례가 감사 가능하지 않음 |

## 재현 범위

13개 정적 덱 사례 + 4개 fix_run 사례 + 2개 strip_comments 사례 + 3개 after_settling 사례 + 제공된 압축 덱 1개 + 첫 잔여 숫자 2 후보 1개. ‘24개 안전성 PASS’라는 뜻이 아니라, 각 사례의 실제 rc와 반례 결과를 남긴 24개 관측이다. false-pass 사례는 수정 후 실패해야 한다. 실제 본 제출을 했다고 주장하지 않는다.
