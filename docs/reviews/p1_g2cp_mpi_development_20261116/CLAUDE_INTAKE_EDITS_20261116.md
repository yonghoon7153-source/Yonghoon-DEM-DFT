# 반입 때 Claude 가 고친 곳 (11-16)

받은 Codex 문서 둘에서 상대 경로 참조 하나씩을 리포 전체 경로로 바꿨다. `scripts/check_doc_refs.py` 는 상대 경로를 리포 뿌리와 문서 자기 폴더 기준으로만 찾는다. 두 참조는 한 단계 위 트랙 폴더 기준으로 적혀 있어서 깨진 참조로 잡혔다. 뜻은 바꾸지 않았고 경로 표기만 바꿨다. 안쪽 `SHA256SUMS` 는 바뀐 파일의 줄만 새 값으로 고쳤다.

| 파일 | 바꾼 곳 | Codex 원 sha256 | 지금 sha256 |
|---|---|---|---|
| `metadata_20261116/field_qualification_matrix.md` | 19 행 `results_20261116/next_steps.md` → `docs/reviews/p1_g2cp_mpi_development_20261116/results_20261116/next_steps.md` | `7920dc454f92f078cc6add09036d9925ecd7d6f729cde70cbf57769be0e611f6` | `6fef5cdde139e0a66a6b24d5d60b437aa3afa4669942bbb9a06ea885f8c5dd9e` |
| `failure_path_preparation_20261116/README.md` | 14 행 `metadata_20261116/first_content_selection.json` → `docs/reviews/p1_g2cp_mpi_development_20261116/metadata_20261116/first_content_selection.json` | `1be3948c3a2492d2d31d75ff2c570f83aa2cb1b2b5b9449f955915a46382b8b6` | `500a95a3c177a96cbca5aee0acc15a154885882a2df4fd0a153dbfb08bd5b1dc` |

- 첫 줄은 기록 ③ 커밋에서 고쳤는데, 그때는 `metadata_20261116/SHA256SUMS` 를 같이 고치지 않아 그 파일 하나가 어긋나 있었다. 이번 커밋에서 맞췄다.
- Codex 원 바이트는 원 커밋에 그대로 있다: 첫 파일 = `b24251a78` (반입 `5970454d4`), 둘째 파일 = `85ac45386` (반입 `92affd946`).
- 11-16 Codex 실무 프롬프트에 "문서 참조는 리포 전체 경로로" 를 넣었다.
