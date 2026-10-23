# 최종 패키지 감사 후 설명 보강

v17 CLI에 `-I`를 추가하고 새 협업 쪽지에 기존 원장 제안 JSON 원문을 넣었다. 별도 JSON은 그대로 유지했다. `file_changes.json`은 두 문서의 전후 SHA256과 요청서 hash 불변을 기록한다. 생산 생성기 및 독립 v1/v2 원자료는 바꾸지 않았다.

`check_devlog.py`는 실제 웹앱의 문서 조회와 쓰기 디렉터리만 새 scratch로 지정한다. `python -I`로 실행해 페이지9/9와 `python3 -I` CLI·필수 밀도/벽·schema·HOLD 표시를 확인했다. 원 로그는 `devlog-isolated-render.log`, 결과는 `render-summary.json`이다. 이전 렌더 로그를 새 실행으로 소급하지 않았다.

재현은 다음처럼 저장소 밖의 새 출력 폴더를 사용한다. REPO는 checkout, E는 이 증거 폴더, OUT은 미존재 새 scratch 폴더다.

```bash
python -I "$E/package_followup/check_devlog.py" \
  --repo "$REPO" --devlog "$REPO/docs/mixer_devlog/v17_20261023.md" --out "$OUT"
```

전체 저장소 gate·외부 GO·새 실행은 이 렌더 검사와 별도이며 여전히 최종 반입 담당자가 확정한다.
