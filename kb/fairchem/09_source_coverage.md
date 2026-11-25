# Source coverage and limits

## 이번에 “빠짐없이” 본 범위

공식 GitHub default branch의 한 commit을 기준으로 아래를 전수 색인했어.

- tracked file 944개
- tracked-path directory 246개
- source 453개
- config 128개
- docs asset 95개
- Markdown 66개
- package manifest 13개
- test file 187개
- pretrained registry entry 13개
- official paper-index entry 42개
- live docs route 64개
- live docs internal target 83개

`repo_files.json`에 944개 경로·바이트·SHA256이 있으므로 “어느 파일을 빠뜨렸나”를 기계적으로 확인할 수 있어.

## 포함하지 않은 것

- pinned commit 이전의 전체 Git history
- unmerged branches
- GitHub Issues, Pull Requests, Discussions, Wiki
- GitHub release attachment와 PyPI wheel 내부 전체
- Hugging Face model weight와 dataset payload
- gated token
- third-party paper PDF와 figure image
- model을 실제 다운로드해 돌린 runtime validation

따라서 이 bundle은 “current official tracked source와 live documentation의 exhaustive snapshot”이지, Fair-Chem 생태계의 모든 과거 대화·weight·data byte를 복제한 archive가 아니야.

## Static inventory와 runtime의 경계

공식 test file과 config는 전수 색인했지만 upstream dependency/checkpoint를 설치해 840개 test 정의를 실행한 건 아니야. 현재 live tutorial 실행 오류를 따로 기록한 이유도 같은 경계 때문이야.

## 저작권·용량 경계

ZIP에는 official source code 원문을 복제하지 않아. 경로, hash, source link, 짧은 구조화 metadata와 우리 해석만 담아. 이 방식은 나중에 source drift를 검증하면서도 gated checkpoint, dataset, PDF, figure의 무단 재배포를 피할 수 있어.

## Audit fingerprint

```text
Official repository: https://github.com/facebookresearch/fairchem
Commit: 93a03d656806a55f08c7cd126cfaa40ef18181fb
Commit time: 2026-08-20T23:19:48Z
Live checked: 2026-08-21
```

정본: [snapshot.json](../../db/knowledge/fairchem/snapshot.json).

