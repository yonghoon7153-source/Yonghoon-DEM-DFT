#!/usr/bin/env python3
"""IDENTITY_v35.json — 번들 증서 (IDENTITY_v34.json 과 같은 스키마).

  python3 tools/sdcp/c12_make_identity.py --bundle <dir> --zip <zip> --commit <sha> --argv-json <json list> \
      --out runs/sdcp_c12_2026_08_30/IDENTITY_v35.json [--checks "전부 PASS — …"] [--variant A]
"""
import argparse, datetime, hashlib, json, pathlib, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("--bundle", required=True)
ap.add_argument("--zip", required=True)
ap.add_argument("--commit", required=True)
ap.add_argument("--argv-json", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--checks", default="미실행")
ap.add_argument("--variant", default="?")
ap.add_argument("--repo", default=".")
a = ap.parse_args()

B = pathlib.Path(a.bundle)
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def git_show_sha(path):
    b = subprocess.run(["git", "-C", a.repo, "show", "%s:%s" % (a.commit, path)],
                       capture_output=True).stdout
    return hashlib.sha256(b).hexdigest() if b else None

man = json.loads((B / "MANIFEST.json").read_text(encoding="utf-8"))
kp = man.get("kconv_pair") or {}
reopen = next((v for k, v in kp.items() if "재개_조건" in str(k)), None)
refs = ["tools/sdcp/vasp_handoff_bundle.py",
        "db/properties/sdcp_c12_claim_prereg_2026_08_31.json",
        "db/properties/sdcp_c12_protocol_2026_08_30.json",
        "db/properties/c12_poses_2026_08_30.json",
        "db/governance/decisions.json"]
rec = {
    "schema": "bundle_identity/v1",
    "date": datetime.date.today().isoformat(),
    "bundle": B.name,
    "zip_sha256": sha(a.zip),
    "manifest_sha256": sha(B / "MANIFEST.json"),
    "analyzer_in_bundle_sha256": sha(B / "analyze_results.py"),
    "census_in_bundle_sha256": sha(B / "census.py"),
    "run_staged_in_bundle_sha256": sha(B / "run_staged.sh"),
    "seal_in_bundle_sha256": sha(B / "SEAL_POTCAR_ROOT.sh"),
    "make_attestation_in_bundle_sha256": sha(B / "MAKE_POTCAR_ATTESTATION.sh"),
    "repo_commit": a.commit,
    "repo_commit_reachable_from": "origin/claude/friendly-meitner-lldvar (생성 시점에 푸시된 커밋)",
    "repo_files_sha256_from_commit": dict({"⚠_출처": "`git show %s:<path>`" % a.commit[:8]},
                                          **{r: git_show_sha(r) for r in refs}),
    "generated_argv": json.loads(a.argv_json),
    "v34_대비": {
        "① attestation 버전 토큰": ("MAKE 가 stdout 전문을 적고 SEAL 은 토큰만 봉인 → 분석기 `raw not in banner` 가 "
                                   "실물에서 항상 불일치(1단계 뒤 potcar_identity 차단). 둘 다 토큰 · post_hoc 이라도 "
                                   "증서가 있으면 생산 전 검증 (렌즈4 P0-1)."),
        "② δ_k 설계 제외의 근거": ("사전등록 49행 인용 → 50행에 대한 **비준된 예외** `3_오차예산.%s` 로. 생성기가 그 항의 "
                                  "재개 조건을 MANIFEST 로 복사하고 분석기가 대조(UNRATIFIED/DRIFT/UNDECLARED 차단). "
                                  "종전 '|ΔE_ads|<50 meV → dense 추가' 폐기 (프로토콜 §7·§8 과 반대) — 안 %s"
                                  % (kp.get("prereg_entry"), a.variant)),
        "③ 재개 조건 기계 평가": "판정량 D_raw_eV · 문턱 · 비교 · 충족시 → 분석기 reopen_eval + advisory (렌즈2 P1-2)",
        "④ overall_citable_at_0.01eV": "사전등록 축이 빠지면 False (None 아님) · verdict 꼬리 · numeric_budget.정의 실제 축",
        "⑤ not_applicable 우회": "primary 조각이 둘인데 not_applicable 이면 KCONV_STATUS_INVALID (렌즈2 P1-1)",
        "⑥ preflight": "kconv 생략의 비준·형식·드리프트를 --check_governance 에서 정적 판정 (렌즈2 P1-3)",
        "⑦ 문서": ("반송 목록에 MANIFEST/job.json/RESULTS.json + 통째로 압축 · walltime 한 문장(세 문서) · 종 순서 실물 · "
                  "dense 잔존 문구 제거 · attestation 명령 완전형/순서/효과 통일 · unzip 순서 · 8축 · 기동 횟수 · "
                  "bundle_label (렌즈4 P1/P2)"),
    },
    "🔁_재개_조건_결과_보기_전에_선언": reopen,
    "재개_조건_출처": "비준 사전등록 3_오차예산.%s (생성기가 복사 · 분석기가 대조)" % kp.get("prereg_entry"),
    "사람_확인_8가지": a.checks,
    "⛔_이_증서가_보증하지_않는_것": [
        "과학적 보고량의 타당성 (D 가 맞는 양인가)",
        "외주처의 실제 PP 트리·VASP build·스케줄러 환경",
        "SCF 수렴·OUTCAR 형식",
        "POTCAR 신원 (post_hoc 정책 — 원고 인용 자격은 별도 판정)",
        "실물 VASP 의 stdout 순서·버전 토큰 형식 (ASE 표본에 근거한 추론 · 외주처 첫 실행에서 확인됨)",
    ],
}
pathlib.Path(a.out).write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("→", a.out, "| zip", rec["zip_sha256"][:12], "| manifest", rec["manifest_sha256"][:12])
