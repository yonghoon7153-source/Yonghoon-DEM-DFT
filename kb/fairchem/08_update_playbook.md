# Update and rebuild playbook

## 1. Official source 고정

깨끗한 임시 폴더에 공식 repo를 clone해.

```powershell
git clone --depth 1 --filter=blob:none https://github.com/facebookresearch/fairchem.git .codex_tmp/fairchem_official
git -C .codex_tmp/fairchem_official rev-parse HEAD
```

Git SHA가 바뀌면 새 snapshot이야. 기존 DB를 덮어쓰기 전에 diff를 검토해.

## 2. Machine DB 재생성

```powershell
python tools/fairchem_kb/build_fairchem_kb.py `
  --source-repo .codex_tmp/fairchem_official `
  --repo-root .
```

생성 뒤:

```powershell
python tools/fairchem_kb/build_fairchem_kb.py --repo-root . --validate-only
git diff -- db/knowledge/fairchem kb/fairchem tools/fairchem_kb
```

Builder는 standard library만 사용해. Fair-Chem 설치나 model download가 필요하지 않아.

## 3. Live docs 재감사

`live_doc_status.json`과 `live_link_audit.json`은 web observation이므로 자동 source build와 분리돼 있어.

확인할 것:

- MyST 64개 route HTTP status
- external demo 2개
- source orphan
- rendered notebook error
- sitemap/robots host
- `/autoapi/`
- internal broken links

새 URL을 발견해도 live slug를 primary key로 바꾸지 마.

## 4. Curated knowledge 검토

다음 drift를 사람이 봐야 해.

- task docs vs `UMATask` enum
- prose-advertised models vs `pretrained_models.json`
- current package/version vs release tag
- model/data license
- legacy config link
- 우리 LPSCl policy와 충돌하는 공식 upgrade

## 5. 논문 추가

새 UMA/Fair-Chem paper는 이 builder가 아니라 litdb-curator workflow로 넣어. 이후 verified claim/insight만 Fair-Chem registry에 링크해.

## 6. ZIP 생성

```powershell
python tools/fairchem_kb/package_fairchem_kb.py --repo-root .
```

ZIP은 deterministic timestamp, per-file SHA256, exclusion list를 가진 manifest를 포함해야 해.

## Promotion rule

자동화는 새 evidence를 `proposed`로만 만들 수 있어. `verified`, `citable=yes`, project validation `pass` 승격은 사람이 검토한 뒤에만 해.

