# Seminar v3.2 Q3 독립 점검

검토 범위: 실제 배포 PPTX의 논리적 3장, 그 장의 OMML·notes, 제공 PDF용 `png/slide-03.png`, LIGGGHTS-PUBLIC `3d5c00f20519e6bb6eb6756f51f1ad36564e649d` 소스. 제작자 검사 A8을 독립 증거로 사용하지 않았다. 시뮬레이션 및 생산 코드 변경 없음. PowerPoint 앱에서의 렌더는 이 분담 작업에서 수행하지 않았다.

## 결론

**Q3 = 부분.** 감쇠 숫자와 ③·④·⑤의 주요 산술은 근거가 있다. 그러나 ②의 반지름 근사를 포함한 전체 판을 `implemented equations`라고 부르는 것은 정확하지 않다. 네이티브 PowerPoint 표시 미확인은 범위 제한이다. 새 P1은 이 범위에서 발견하지 않았다. 아래 초기 EQ32-02 의심은 코드포인트 검산으로 **철회**했다.

## EQ32-01 · P2 · 반지름 근사를 구현식이라고 표시

- 위치: 3장 ② Rotation, 상단 출처 문구 `This work — implemented equations ...`, 해당 장 notes. 실제 PPTX XML 위치는 `ppt/slides/slide18.xml`의 이름 `eq2`인 `mc:Choice` 내부 `m:oMathPara`이다. 원본 XML 토큰은 `R_i n_ij × F_t,ij`이다.
- 고정 버전의 실제 구형 입자 토크 지렛대는 `cri = radi - 0.5*deltan`이다. `surface_model_default.h:173–188`, `tangential_model_history.h:254–261`에서 이 길이를 곱한다. 법선 방향을 i→j로 정의하면 표시 형식은 `(R_i−δ_ij/2)n_ij × F_t,ij`로 쓸 수 있고, j→i 정의를 사용하면 부호를 바꿔야 한다. 현재 슬라이드는 n의 방향을 정의하지 않으므로 **부호가 반드시 틀렸다고 판정하지 않는다.** 지렛대 크기 불일치는 방향과 무관하다.
- 수치 반례: `R_i=0.5 µm`, `δ=0.1 µm`, `|F_t|=1 µN`, 접선력이 직교하면 실제 토크 크기는 `0.45 µN·µm`, 현재 표현은 `0.50 µN·µm`, 상대 차이는 `11.111111 %`이다. 이는 식을 구분하는 합성 입력이지, 실침대 평균 오차가 11.1 %라는 뜻이 아니다.
- 리포 배경 정본도 `docs/dem_governing_equations_background_20261011.md:103–105`에서 구현식의 `c_r`와 발표용 근사 `R_i`를 명시적으로 구분한다. 이번 notes는 다른 생략은 적지만 이 근사는 적지 않았다.
- 최소 해결: (a) `l_ij × F_t,ij`로 쓰고 `|l_ij|=R_i−δ_ij/2`와 방향을 정의하거나, (b) `implemented equations`를 `representative equations based on the implementation`로 바꾸고 화면/notes에 `② uses the small-overlap approximation l≈R`를 명시한다. 기존 운동방정식의 일반 원리나 이력 모델 전체가 무너지는 결함은 아니다.
- 부수 보완: ④의 구름식은 `||ω_r||>0`에서의 식이다. 소스는 0에서 토크를 0으로 둔다. `torsionTorque off; M_r=0 if ω_r=0`를 notes 또는 식 옆에 두면 경계 조건까지 닫힌다.

고정 소스:

- [surface_model_default.h](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/surface_model_default.h#L173-L188)
- [tangential_model_history.h](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/tangential_model_history.h#L254-L261)

## EQ32-02 · 철회 · Python repr의 공백 escape를 literal로 오독

- 초기 분담 메시지에서 3장 `eq3_2`와 `eq4_1`에 문자 그대로의 `\u2003`가 있다고 의심했으나, 이는 Python list의 `repr` 출력을 오독한 것이다.
- 실제 XML 문자열을 `ord`로 재검산한 결과 두 토큰 모두 **`[44, 8195]`**이다. 즉 comma와 실제 U+2003 공백의 두 글자이며, 백슬래시(U+005C)는 없다.
- 이 항목은 결함이 아니며, 수정을 요구하지 않는다. **최종 finding 수와 HOLD 사유에 포함하지 말 것.** `equations_probe.json`에 `spacing_tokens_codepoints`로 검산을 남겼다.
- PowerPoint 앱 미확인이라는 일반 범위 제한은 남지만, 이 공백 때문에 네이티브 표시가 틀렸다는 주장은 철회한다.

## 확인된 것과 한계

| 항목 | 독립 확인 결과 |
|---|---|
| 배포 PPTX 고정 | SHA-256 `1b6988f3e55dc6bcf7e81d0ba4ec35b11ed2a0790a1357ba6e6185d22b08f28d`, 요청서와 일치 |
| 네이티브 수식 수 | 논리적 3장 `slide18.xml`에 OMML 8개 존재 |
| ③ 비포화 이력식 | `max(min(k1δ,k2(δ−δ0)),−kcδ)−γ_n v_n`은 비포화 소스 분기와 맞음. 화면에 `(non-saturated branch)`가 있으므로 포화 가지 생략을 숨기지 않음. k2 이력 갱신의 전체 알고리즘을 이 한 식이 대체하지는 않음 |
| ④ 접선 마찰 | `F_t,spring`과 그 크기에 적용한 Coulomb 한계는 소스 분기와 맞음. 접선 감쇠 생략은 notes에 있고, 화면도 spring이라고 부름 |
| ④ CDT | 전체 `||ω_r||`로 나눈 후 법선 성분을 제거하는 꼴은 `torsionTorque off` 소스와 맞음. `k1δ`, 실제 이력 법선력 아님. 0일 때의 정의는 보완 필요 |
| ⑤ 강성 | 소스 `normal_model_hooke_hysteresis.h:138–146`의 `kn`, `kt=kn`, 1/5 거듭제곱과 일치. E*는 문서 Y*의 표기 변경이며 식 자체 동일 |
| 전역 감쇠 | 실제 덱 `in.ps_7_3_r45.liggghts:144,191,217`은 settling `1.0e-5`, stabilization/compression `0.5`, relaxation `1.0e-5`. 화면과 일치. 압축 중 감쇠가 적절하다는 보증과는 별개 |
| 그림 | 제공 PDF용 3장에서는 식 라벨/힘 그림/수식이 읽힘. 상단 implemented 표기와 ② 근사 사이의 의미 충돌은 시각 문제와 별도 |
| 원본 8e76819a… | ZIP에 해당 원본 PPTX가 없음. Downloads의 유사 파일 6개도 전체 SHA가 모두 다름. 따라서 원본 대비 XML·그림 8/8 byte 동일 주장은 이번 입력만으로 독립 재현하지 못함. 배포 수식의 의미 점검 자체는 가능 |

## 재현과 증거

`agents/equations_probe.py`를 실행하면 생산자 빌더를 import하거나 실행하지 않고 실제 PPTX의 관계표를 따라 3장 수식/notes/해시를 읽는다. 출력은 `agents/equations_probe.json`이다. 수치 반례도 그 JSON에 있다.

```powershell
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' 'seminar_recheck_v32_20261014/agents/equations_probe.py'
```

참조한 코드 본문은 기존 로컬 보존본 `dem_unloading_kit_reverify_20261014/upstream/`이고, 고정 GitHub 링크를 추가로 직접 조회했다. `normal_model_hooke_hysteresis.h`는 GitHub 연결 도구로 고정 SHA 본문을 읽었고, 다른 세 파일은 고정 raw URL도 읽었다. 로컬 소스와 웹 텍스트 추출의 줄바꿈·표시 방식 차이 때문에 위 링크 줄 번호는 로컬 보존본/원 GitHub 파일 기준이다.
