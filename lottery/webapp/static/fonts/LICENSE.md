# 이 디렉터리의 폰트 — 출처·판본·우리가 손댄 것

이 앱은 CSP 가 `default-src 'self'` 라 폰트 CDN 을 쓸 수 없다. 그래서 폰트를
**저장소에 넣고 우리가 서빙**한다. 둘 다 SIL Open Font License 1.1 이므로
재배포할 수 있고, 라이선스 전문을 같은 디렉터리에 함께 둔다 (OFL 요구사항).

| 파일 | 원본 | 판본 | 라이선스 |
|---|---|---|---|
| `Pretendard.subset.woff2` | [orioncactus/pretendard](https://github.com/orioncactus/pretendard) `dist/web/variable/woff2/PretendardVariable.woff2` | v1.3.9 | OFL 1.1 — `OFL-Pretendard.txt` |
| `JetBrainsMono-Regular.woff2` · `-Bold.woff2` | [JetBrains/JetBrainsMono](https://github.com/JetBrains/JetBrainsMono) `JetBrainsMono-{Regular,Bold}.ttf` | master (컨테이너 동봉본) | OFL 1.1 — `OFL-JetBrainsMono.txt` |

## 왜 이 둘인가

- **Pretendard** — 이 앱의 주 화면은 한글·영문·수식·코드가 **한 문단에 섞이는**
  논문 digest 다. 시스템 폰트 스택은 한글과 라틴이 서로 다른 폰트로 그려져
  한 줄 안에서 굵기와 기준선이 흔들린다. Pretendard 는 둘을 한 벌로 그렸다.
  가변축(45–920)이라 CSS 의 `font-weight: 430` · `640` 같은 중간값이 합성이
  아니라 **진짜로 그려진다**.
- **JetBrains Mono** — digest 본문에 인라인 코드가 아주 많다. `l/1/I`,
  `0/O` 가 확실히 갈라지는 폰트가 필요했다. 한글 글리프는 없고(그럴 필요도
  없다) 코드 안의 한글은 `--mono` 스택 뒤쪽으로 넘어간다.

## 잘라낸 범위 (subset)

원본을 그대로 두지 않고 이 위키가 실제로 쓰는 문자만 남겼다. 재현 명령:

```sh
# Pretendard — 2.06 MB → 1.80 MB
pyftsubset PretendardVariable.woff2 --output-file=Pretendard.subset.woff2 \
  --flavor=woff2 --no-hinting --desubroutinize --name-IDs='*' \
  --layout-features='kern,liga,calt,ccmp,locl,mark,mkmk' \
  --unicodes="U+0020-007E,U+00A0-00FF,U+0100-017F,U+0370-03FF,U+2000-206F,\
U+2070-209F,U+20A0-20BF,U+2100-214F,U+2150-218F,U+2190-21FF,U+2200-22FF,\
U+2300-23FF,U+2460-24FF,U+25A0-25FF,U+2600-26FF,U+2700-27BF,U+3000-303F,\
U+1100-11FF,U+3130-318F,U+AC00-D7A3,U+FF01-FF60"

# JetBrains Mono — 각 ~200 KB → 9 KB
pyftsubset JetBrainsMono-Regular.ttf --output-file=JetBrainsMono-Regular.woff2 \
  --flavor=woff2 --no-hinting --layout-features='kern,ccmp' \
  --unicodes="U+0020-007E,U+00A0-00FF,U+2000-206F,U+2190-21FF,U+2200-22FF"
```

한글 음절 전체(U+AC00–D7A3, 11,172자)를 남긴 것은 의도다. 실제로 쓰인 음절만
남기면 300 KB 대로 줄지만, **앞으로 쓸 글자**를 모르므로 새 문서에서 한 글자가
빠지는 순간 그 글자만 다른 폰트로 그려진다. 로컬에서 서빙하는 1.8 MB 는
한 번 받고 캐시되므로, 그 위험과 바꿀 값이 아니다.

CJK 한자(U+4E00–9FFF)는 **뺐다** — 2만 자가 넘고 이 위키에는 거의 안 나온다.
드물게 나오면 시스템 폰트로 떨어진다.

폰트 파일에 손댄 것은 글리프 제거뿐이고 자형·메트릭·이름은 그대로다.
OFL 의 Reserved Font Name 조항에 걸리지 않도록 **이름을 바꾸지 않았고**
(`Pretendard`, `JetBrains Mono`), 개조본이 아니라 부분집합임을 여기 적어 둔다.
