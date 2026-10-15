# v3.3 수식·승계 독립 종결 점검

판정: **SEMV32-01 내용 수정 종결. 원 수식 덱 대비 8/8 OMML C14N + 8/8 fallback 이미지 + 2/2 일반 그림 동일성 재현.** 수식·승계 범위에서 새 P1/P2 없음. 실제 발표 PC의 PowerPoint 네이티브 표시 검사는 미실시이며 별도로 남는다.

범위는 제출 PPTX 세 개를 직접 ZIP/XML로 읽은 비교다. 제작자 빌더·selftest·대조 스크립트는 실행하거나 import하지 않았다. 새 시뮬레이션·Git 변경·제출 파일 수정 없음. `agents/equations_probe.py`와 JSON은 이 리뷰의 독립 증거다.

## 1. 고정과 읽기 규칙

| 대상 | 실제 SHA-256 | 논리적 장 수 |
|---|---|---:|
| v3.3 | `e787298ef657d516f43c8255e80cf1a61bbc52ffe94c6fbfbea57faca14dbb8c` | 18 |
| 비교 v3.2 | `1b6988f3e55dc6bcf7e81d0ba4ec35b11ed2a0790a1357ba6e6185d22b08f28d` | 18 |
| 원 수식 덱 | `8e76819a9f89516d75c7bd40c529cd65ce055e31a2c8b777d1b8e8edfc669223` | 1 |

셋 모두 요청서 고정값과 같다. `ppt/presentation.xml`의 `p:sldIdLst`에서 관계표를 따라 논리적 순서를 결정했다. v3.2의 논리적 3장은 `ppt/slides/slide18.xml`, v3.3은 `ppt/slides/slide3.xml`, 원 수식 덱은 `ppt/slides/slide1.xml`이다. 단순히 같은 번호의 XML 파일을 대조하면 잘못된 차이가 생긴다.

## 2. SEMV32-01의 실제 수정 위치와 의미

v3.3 논리적 3장, `ppt/slides/slide3.xml`, shape id `70`, name `TextBox 69`:

- 첫 줄: `/p:sld/p:cSld/p:spTree/p:sp[3]/p:txBody/a:p[1]/a:r/a:t`
- 둘째 줄: `/p:sld/p:cSld/p:spTree/p:sp[3]/p:txBody/a:p[2]/a:r/a:t`

화면 원문:

> This work — representative equations based on LIGGGHTS-PUBLIC 3.8.0 [2]; linear hysteretic law [1].
>
> Equation ② uses the small-overlap approximation ℓᵢⱼ ≈ Rᵢnᵢⱼ.

notes는 `ppt/notesSlides/notesSlide15.xml`, `/p:notes/p:cSld/p:spTree/p:sp[2]/p:txBody/a:p`에 있다. 실제 문장에 대표식이라는 지위, ②의 작은 겹침 근사, 구형 입자 경로의 구현 지렛대 크기 `Rᵢ − δᵢⱼ/2`, `cri = radi − 0.5·deltan`이 함께 들어 있다. 따라서 원래 지적한 “반지름 근사를 구현식 전체와 동일시”하는 함의가 제거됐다. 수식 자체를 바꾸지 않는 승인된 해결 방식과 일치한다.

CDT notes에는 상대 각속도가 0이면 토크가 0이고 `ω_r/‖ω_r‖`는 `‖ω_r‖ > 0`에서만 쓰며 `torsion torque off`라는 조건도 있다. 이전 리뷰가 고정한 소스 보존본을 다시 읽었다:

- `surface_model_default.h:173–188`: 벽 및 입자 경로에서 반지름에서 반 겹침을 뺀 `cr`, `cri`, `crj`.
- `tangential_model_history.h:254–261`: 구형 경로의 실제 토크에 `sidata.cri`·`sidata.crj`를 곱함.
- `rolling_model_cdt.h:94,133–157`: 토크를 먼저 0으로 초기화하고 상대 각속도의 크기가 양수일 때만 방향 정규화 및 토크를 계산함.

소스 파일 SHA와 해당 줄 전체를 JSON의 `local_pinned_source_code_checks`에 남겼다. 이 로컬 보존본의 기존 핀은 `3d5c00f20519e6bb6eb6756f51f1ad36564e649d`이며 이번 점검에서 새 원격 소스를 받지 않았다.

OMML ②의 `R_i n_ij × F_t,ij`는 그대로이며 이 표현을 이제 근사로 명시한다. 법선 방향을 새로 정의하지 않았으므로 부호를 새로 판정하지 않는다. 단위·벡터·첨자·재료 상수를 바꾼 흔적은 없다. ③의 비포화 가지, ④의 접선 spring만 표시한다는 기존 제한도 유지된다.

## 3. 원 수식 덱과의 8 + 8 + 2 동일성

`mc:AlternateContent`마다 `mc:Choice`의 `m:oMathPara`와 `mc:Fallback`의 관계를 따랐다. 모든 수식은 원본과 inclusive C14N 및 exclusive C14N에서 일치하고, 모든 수학 토큰도 동일하다. fallback은 파일명보다 실제 매체 바이트의 SHA로 비교했다.

| 수식 객체 | OMML C14N SHA-256 (원본 = v3.2 = v3.3) | 원본 fallback |
|---|---|---|
| eq1 | `08b8b22976446439d9f8b90e6fa4b6d191564d4c31f7e3321e4f2ee8ac9947a2` | 동일 |
| eq2 | `ae8c9401a694325bee45a02ca849f86a8cfdaabfb2b4b9f2bd137d23b035b631` | 동일 |
| eq3_1 | `8f3c663ffd9d8a9fcc8505aaf2ea7c7de3fe406bd7750d82fd7ea61100ed6a5d` | 동일 |
| eq3_2 | `0004fb16d61f1a5965cce942b5826148f55f5d7d9091d37f23d065c7cf6ff936` | 동일 |
| eq4_1 | `bf145ccd2543feb2186eaa317cf9148e852b136c5243772d0b29e300e296aac0` | 동일 |
| eq4_2 | `051227ff00ea96548dfd43cc7db54bb8485a20d41780ee792185812c57d54729` | 동일 |
| eq5_1 | `14d59e762e96dc29eee2dda1f2f56b23c9d1997af0615ed16f7981fb06f3933f` | 동일 |
| eq5_2 | `5300c831fa686d7c37f32b2903457483813ab9a1c4d8f876cca271a97ab737f6` | 동일 |

위 객체는 v3.3의 `/p:sld/p:cSld/p:spTree/p:grpSp[1]/mc:AlternateContent[1]`부터 `[8]`에 순서대로 있다. 각 네이티브 수식의 이어지는 XPath는 `/mc:Choice/p:sp/p:txBody/a:p/a14:m/m:oMathPara`다. 8개 fallback의 전체 SHA와 원본·v3.3의 연결 대상은 JSON에 있다.

일반 그림 2개:

| v3.3 객체 | 매체 SHA-256 | 원본과 일치 |
|---|---|---|
| id 3001 `Panel frame picture`, `p:grpSp[1]/p:grpSp/p:pic`, `ppt/media/image8.png` | `dc54549f4fd847ebc9aa276865e06ce43aedcbf42b6a1f9aa88a7d2f4f0cb720` | 예 |
| id 3034 `Force diagram picture`, `p:grpSp[2]/p:pic`, `ppt/media/image29.png` | `6a884298e0661f4df6c51760e9a2fa6511858956d0d9ce27900cb89f4611b0fe` | 예 |

표현의 정확한 경계: **원본 대비는 OMML 정규화 XML(C14N)의 동일성**이다. `lxml`로 직렬화한 원본 수식 문자열과 v3.3 문자열은 namespace 선언 순서 및 중복 `xmlns:m` 때문에 문자 단위로는 다르지만 C14N이 같으며 내용·수식 서식 차이가 아니다. **v3.2 대비는 8개 수식 직렬화 문자열도 같고**, 네이티브 `mc:Choice`, fallback XML, 전체 `mc:AlternateContent`의 C14N도 8/8 동일하다. 원본 PPTX 전체 파일의 raw XML 바이트가 같다고 과장하지 않는다.

과거에 철회한 `\\u2003` 오독도 되살리지 않는다. 실제 `eq3_2`·`eq4_1`의 공백 토큰은 쉼표와 U+2003, 코드포인트 `[44,8195]`이며 v3.2 및 원본과 같다.

## 4. 승계 12장과 바뀐 6장

변경 없음으로 지정한 **1·2·4·6·8·9·10·12·14·16·17·18장**에서 본문/run·notes·모든 연결 이미지 매체·수식 해시 5개 범주가 전부 같다(60/60). 더 강하게는 논리적 장을 대응시킨 **12/12 slide XML 원시 바이트와 12/12 notes XML 원시 바이트도 같다.**

| 논리적 장 | 실제 변경 범주 | 내용 위치 |
|---:|---|---|
| 3 | text/run, notes | 출처 shape 70의 두 줄. 수식·그림은 그대로 |
| 5 | notes만 | `notesSlide4.xml`: 대립 LPSCl pellet 승인 상태 갱신 |
| 7 | text/run만 | `slide7.xml`, shape 5 `Rectangle 4`: 첫 300 MPa에 nominal stopping pressure 한정 추가 |
| 11 | text/run, notes, 그림 | `slide11.xml`, shape 5의 본문2와 shape 287의 해석 줄(b); `notesSlide14.xml`; F_p4 이미지 교체 |
| 13 | notes만 | `notesSlide20.xml`: Kissel 강도와 횟수 문장 교체 |
| 15 | text/run, notes | `slide15.xml`, id 298 `Gen2 box 6`, id 300 `Gen2 box 7`, id 301 `Gen2 note`; `notesSlide22.xml` |

실제 차이 범주는 이 여섯 장의 요청된 범주와 정확히 같다. 5·13장은 notes만 바뀌어 **slide XML 자체는 동일**하다. 11장 이미지 객체는 id 71에서 id 289로 교체됐다. 표 id 72는 위치만 조정됐고 텍스트·run·문단 서식은 같다. 이 표의 이력 초기화와 13 SE 소실 행은 보존됐다. 그림 객체 교체/배치 조정을 “모든 shape XML이 그대로”라고 부르지는 않는다.

## 5. 공유 스타일 자원과 PowerPoint 한계

슬라이드 XML 밖에서 스타일이 바뀌는 경우도 확인했다. 다음 **19개 전역 자원 모두 v3.2와 raw SHA-256 동일**이다:

- `presentation.xml`(기본 text style 포함), `presProps.xml`, `viewProps.xml`, `tableStyles.xml`.
- slide master 1개와 그 관계표, slide layout 3개와 각 관계표.
- theme 3개.
- notes master와 handout master 및 각 관계표.

18/18 논리적 장의 layout 관계 ID·대상·대상 SHA도 같다. 양쪽 모두 embedded font 매체는 0개다. 변경 없는 장의 theme/layout/font 설정이 전역 편집으로 달라진 증거는 없다. 전체 자원명 및 양쪽 해시는 JSON `global_style_comparison`에 있다.

**PowerPoint 앱에서 열고 검사하지 않았다.** 위 결과는 파일 내용과 네이티브 객체 보존을 확인한다. PDF나 PNG의 fallback 수식이 읽힌다는 사실만으로 PowerPoint의 OMML 줄바꿈·잘림·글꼴 대체를 통과시킬 수 없다. 특히 새 출처 줄의 `ⱼ`는 실제 U+2C7C(11388)이며 발표 PC의 설치 글꼴/대체 글꼴 표시를 보아야 한다. 이 장의 네이티브 수식 8개 및 새 출처 둘째 줄은 발표 PC에서 최종 화면 확인할 항목으로 남긴다. 이 미실시는 새 내용 결함의 발견과 구별한다.

## 6. 증거와 재현

`agents/equations_probe.json`은 세 파일의 고정 SHA, 모든 논리적 장/part 대응, 8개 수식의 전체 XML과 토큰·해시, 모든 그림의 연결 관계·해시, 18장 비교, 전역 스타일 비교, 실제 notes 전문, 수정 위치의 XPath를 보존한다.

```powershell
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' 'seminar_closure_v33_20261015/agents/equations_probe.py'
```

Q1: 내용 수정 종결. Q7 중 원 수식 자료와 A8 동일성: 재현 완료. 묶음 전체 manifest/목록 점검과 PPTX/PDF 표시 검토는 다른 분담 증거와 합쳐 판단한다.
