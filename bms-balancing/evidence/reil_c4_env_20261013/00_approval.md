# C4-ENV 승인 원문 사본 (실행 기록용)

- 사용자 원문 (2026-10-13): "권고대로"
- 해석 기록: `bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md` §36 (커밋 `e5b7a254cfabc21047673d715bffc53b26350dd8`) — (A) C4-ENV 승인 (요청 §6) · (B) C4-0 범위 재확인 (v2 §8 · 효력은 새 봉인 검토 수용 뒤)
- 요청 문서: `bms-balancing/docs/REIL_C4_ENV_APPROVAL_REQUEST_20261013.md` · sha256 `47af94d1eba4a8be885566aada162afbeb5fa8a792105dce19650b84cd76554d` (요청 커밋 `98dec16a59497f1633e58ef449bf6747dd398eb8`)
- C4 요청 v2: `bms-balancing/docs/REIL_C4_APPROVAL_REQUEST_v2_20261013.md` · sha256 `22dcc8e5ef6430253f55834743e10808b0c3547c8fb560d0ad415dce77da8f87`
- t0: 2026-10-13T06:06:16.882Z (monotonic 원점 · 각 meta 의 *_rel 은 이 원점에서 잰 초)

## 요청 §6 채택 문구 (요청 문서에서 그대로 옮김)

> 이 문서 (`bms-balancing/docs/REIL_C4_ENV_APPROVAL_REQUEST_20261013.md`) §1 의 고정 표와 이 문서의 범위로 C4-ENV 새 환경 준비 1건만 승인합니다. 기존 환경의 동일 복원이라고 표현하지 않습니다.
>
> 지정된 새 경로에서 확인된 interpreter에 기존 과학 lock의 전체 30개 배포판을 같은 판으로 준비합니다. 사전에 명시된 별도 시험 도구 범위만 포함합니다. 기존 환경·코드·봉인·C5 원문을 덮어쓰거나 삭제하지 않습니다.
>
> **emit 1회와 check 1회만** 허용합니다. check 내부의 emit을 포함하여 **합성 COBYQA 최적화 총 2회, 전체 Sobol 생성 경로 총 2회**임을 수용합니다. 여기에는 seed/rng 비교 생성과 check의 임시 파일 쓰기도 포함됩니다. pytest·변이 시험·C5 재측정은 포함하지 않습니다.
>
> 전체 1,800초·디스크 2,000,000,000 B를 한도로 합니다. venv·다운로드/캐시·별도 시험 도구·봉인·임시 파일·기록의 새 파일을 합산합니다. 이 수치는 메모리 한도가 아니며 설치 완료 보증도 아닙니다. 미측정은 0 또는 PASS로 바꾸지 않습니다.
>
> 설치 실패·배포판 집합/판 불일치·기존 경로 충돌·예산 초과·예상 밖 차이는 최초 오류와 확보된 기록을 남기고 중지합니다. 임의 재시도·패키지 판 완화·다른 interpreter·새 경로 fallback·코드 수정은 하지 않습니다.
>
> old→new 차이표와 새 MANIFEST를 제출하고 멈춥니다. 새 emit/check 성공만으로 새 봉인을 자동 채택하지 않습니다. 차이 검토 수용과 정정된 C4-0 범위 확인 뒤 그 봉인을 C4 환경으로 명시 연결합니다.
>
> REIL 원자료·pickle·노트북 개봉, 실측 자료 맞춤, E3a/H 실행, COMSOL, 기존 사본 정리는 승인하지 않습니다.
