# GATE94 영수증 정적 대조

판정: 두 leg의 history 보존, core의 제한된 변경, 원장 앵커를 수용한다. 새 차단 결함은 발견하지 못했다. 영수증 생성·복원·재채점·시험·수신 코드 import는 0회다. 저장된 영수증의 사실과 텍스트 동일성을 확인한 것이며, 수신자가 생성 계산을 재현한 것은 아니다.

## 대상과 기준

- 고정 요청 HEAD: `2345051aadf7c9e5f764fa76966bd4e3ad9a02eb`.
- 재생성 직전 HEAD: `27b0917e2a2cb05a629206472d6ed6f7b6be99f6`.
- history 세대: `c7f48918ff971e91`.
- 현행 validator source_digest: `044e4f5513011a9b`.
- 이전 코드 HEAD `d7a97aa57ea926916d56c985ee4bc2bed96fa81a`의 현행 영수증은 아직 `f0175fff71132003` 세대다. 이번 c7f history 바이트 보존의 직접 비교 기준은 그보다 뒤의 재생성 직전 `27b0917e2` 현행본이다. 오래된 코드 HEAD의 영수증을 잘못된 보존 기준으로 삼지 않았다.

요청 HEAD의 루트에서 degradation-degeneracy → docs → 22p_gap → receipts의 Git tree를 따라 경로와 파일을 확인했다. 각 tree는 truncated=false다. receipts tree는 `3f6f6aa597d797ca9ad8fa4c782021e6bd50158e`, history tree는 `444b1820c50338ba84b75ed196787a2d07ce85ee`다. history tree는 재생성 직전 HEAD와 요청 HEAD에서 같다.

## history 보존과 core

| leg | 현행 blob | history = 재생성 직전 현행 blob | 검사 수 |
|---|---|---|---:|
| paired_fixed5_v4 | b926861617279f2abd8e5a1003b0c6f9d7d12aee | 656329a8f24d0e2dfed01828b2ce018d6a7ab496 | 35 |
| grid_fit_v5 | be194a41dd71758c447ed69f0315040cf38f9a68 | 2889e80daa34a5d3d666ae214eab611ba35b0d74 | 34 |

각 history 파일은 `27b0917e2`의 현행 영수증과 Git blob 및 전체 텍스트가 동일하다. paired는 9,661 B, grid는 9,596 B다. 두 현행 core와 history core에서 다음 두 identity 줄만 제외하면 텍스트가 정확히 같다.

- `validator_source_digest: c7f48918ff971e91 → 044e4f5513011a9b`
- `src_io_sha256: cde0be140cabc8dc → 32506d8816b9152a`

bundle·restore·validation 검사 집합·outputs·semantic digest·outputs_agree는 그대로다. 실제 기록된 검사 키를 별도 집계해 35/34를 확인했으며 모든 기록값은 통과다. 현행 io.py 수신 바이트의 전체 SHA256은 `32506d8816b9152abb8cdb4be8a1bc68d290c9c4deda51aab2097ec52f6980fd`여서 영수증 접두와 일치한다.

| leg | 이전에 기록된 core SHA256 | 현행에 기록된 core SHA256 |
|---|---|---|
| paired_fixed5_v4 | d527cde9fc7251a285d5e753048235f1c3aff54661c7588733cc0ffcd63ad9f7 | 68a74c60b219db4421f834c6b7756e9f741f611a4bf4bd8963cdb4f96d048bf9 |
| grid_fit_v5 | 8de4e4aff4d4550bc4e093949407cf748c540fc42b256d88bff44673cd45292d | 16d3be2555fd6a4ef745ca4ed3f651be61afcd74c3ebeb5965cdd60f4c524856 |

위 core SHA는 영수증에 기록된 선언값이다. 수신자는 make_receipt의 core 생성/직렬화 코드를 실행하지 않았다. 대신 전체 수신 사본의 SHA256·Git blob 해시를 독립 계산하고, core 텍스트 변경과 원장 결속을 확인했다.

## stamp 변화와 clean 표현의 범위

각 영수증 전체에서 바뀐 줄은 6개다: 바깥 core_sha256, core identity 2개, stamp validator_commit·generated_at_utc·platform 3개.

- validator_commit: 두 leg 모두 `68350322592f400e3ef2655972d5d35f14851b60 → 27b0917e2a2cb05a629206472d6ed6f7b6be99f6`.
- paired 시각: `2026-10-06T13:06:34Z → 2026-10-07T00:58:17Z`.
- grid 시각: `2026-10-06T13:08:21Z → 2026-10-07T00:59:52Z`.
- platform: 두 leg 모두 `Linux-6.18.44-fc-v70-x86_64-with-glibc2.39 → Linux-6.18.44-fc-v77-x86_64-with-glibc2.39`.
- Python `3.11.15`는 그대로다.
- validator_tree_dirty는 paired=false, grid=true로 이전과 현행 모두 같다.

원 로그 06의 첫 줄은 `head 27b0917e2... dirty 0`이고 뒤에 paired와 grid의 rc=0이 순서대로 기록되어 있다. 이는 전체 작업 시작이 clean이었다는 증거다. 각 영수증의 stamp까지 둘 다 clean이었다는 뜻은 아니다. 특히 [grid stamp 96행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/2345051aadf7c9e5f764fa76966bd4e3ad9a02eb/degradation-degeneracy/docs/22p_gap/receipts/grid_fit_v5.validate.yaml#L96)의 true는 그대로 보고해야 한다. 이를 새 실패로 분류하지는 않으며 사실을 좁게 기술한다.

environment_profile_C 블록 전체는 history와 정확히 같다. lock SHA `d886f30ff675fef723fb9bcedd98297910fb1f8f1809370c18d8980dc5e63b39`, MISMATCH, 34건(dist_extra 4·dist_record 16·dist_version 13·shadowed 1), unverifiable·counts가 모두 보존됐다. fc-v77 플랫폼 기록은 정본 환경 MATCH의 증거가 아니다.

## 원장 앵커

LEG_PRESERVATION.yaml의 요청 HEAD blob은 `ee4b72a030985eae2e4c337a3b10ca5b55486089`, 재생성 직전 blob은 `fb62d88a3ffab8df1416485459068a06eb8b2df3`다. 전체 텍스트 대조에서 차이는 정확히 네 줄이다.

- paired core anchor: 809행, 현행 receipt.core_sha256과 일치.
- paired validator source_digest: 814행, `044e4f5513011a9b`.
- grid core anchor: 1013행, 현행 receipt.core_sha256과 일치.
- grid validator source_digest: 1019행, `044e4f5513011a9b`.

검사 수 앵커 815행/1020행은 35/34로 영수증과 같고 ok=true도 유지됐다. bundle·fit·출력 digest 등 다른 원장 내용은 변경되지 않았다.

고정 링크: [paired 앵커](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/2345051aadf7c9e5f764fa76966bd4e3ad9a02eb/degradation-degeneracy/docs/22p_gap/LEG_PRESERVATION.yaml#L809), [grid 앵커](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/2345051aadf7c9e5f764fa76966bd4e3ad9a02eb/degradation-degeneracy/docs/22p_gap/LEG_PRESERVATION.yaml#L1013).

## 보존한 검토 자료

이 영역의 reference/*.txt 11개 모두 실제 바이트에서 계산한 Git blob SHA가 connector가 반환한 고정 blob SHA와 일치했다(11/11). 상세 전체 SHA·크기는 REFERENCE_BYTE_VERIFICATION.json, core/stamp/원장 비교와 tree 증거는 RECEIPT_STATIC_COMPARISON.json에 있다. 모든 추가 자료는 outputs/gate94_review_20261007/evidence/receipts 아래에만 썼다.

수용 범위는 영수증의 정적 보존·identity 변경·원장 결속이다. 새 연구 leg·묶음 6 전체 종결·실행 GO로 확대하지 않는다.

