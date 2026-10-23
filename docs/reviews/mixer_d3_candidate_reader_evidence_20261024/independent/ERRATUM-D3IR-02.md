# Independent reviewer correction — D3IR-02 withdrawn

`REVIEW-v1.md`의 **D3IR-02(Bo_po 누락)는 검토자의 오류로 철회한다.** 구현자가 그 finding을 고쳐서 닫은 것으로 세지 않는다.

첫 live code read에는 Bo_po 병기가 없었지만, 이후 실제 보존한 reader SHA256 `3160506f199983e2ff2bcc00ab8aaa461c0cb6dea82adecd163f7cdd86b1c5ad`에는 이미 `bo_po_approx`와 `bo_po_definition`이 있었다. 검토자가 두 시점을 혼동했다. 추가로 최초 독립 probe가 `bo_po`라는 정확한 키만 검사해 false를 기록한 것은 실제 필드명 `bo_po_approx`를 놓친 검사 오류였다.

`bo-po-correction.json`은 같은 보존 reader에서 다시 얻은 grid 값과 정의를 담는다. v1→v3 reader diff에는 Bo_po 추가가 없고 Decimal 예외 처리와 eligible reason 검사/보존만 있다. `probe_independent_v2.py`는 올바른 키와 정확한 유리수 4/27·8/27·4/9에 대한 표시 오차를 검사한다.

원 보고서·첫 probe·오탐 출력은 삭제하거나 조용히 교체하지 않았다. 최신 판정은 `RECHECK-v3.md`를 따른다. 유효한 D3IR-01 거대 지수 예외 finding과 그 수정 검증은 이 정정과 별개다.
