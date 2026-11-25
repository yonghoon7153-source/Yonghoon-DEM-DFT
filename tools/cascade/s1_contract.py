#!/usr/bin/env python3
"""s1_contract.py — cascade **S1 계약** (BJ2 재심 조건 #3) + **대표 배열 선택** (#2 이행)

네 가지를 한 곳에 모은다. 넷 다 지금까지 **조용히 넘어가던 것**을 **멈추게** 만드는 계약이다.
따로 흩어 두면 생성기마다 다르게 복사되고, 그러면 계약이 아니다 (repo 의 실제 사고 유형).

  ① `freeze_parent_sites` / `SiteCarrier` — **치환 전** 부모 자리 지도를 동결하고 승계한다.
     지금 생성기는 P 를 먼저 치환한 뒤 *남은 P* 와의 결합으로 S_16e/S_4a 를 가른다 →
     원래 PS₄ 의 S 가 free S 로 재분류된다 (BJ2 P0-2). 자리는 **부모 host 의 성질**이고,
     현재 배위는 **관측값**이다. 둘을 같은 이름으로 부르지 않는다.
  ② `charge_ledger` — 양이온만이 아니라 **음이온·공공·침입까지** 더한 전체 보상 수지.
  ③ `quantize_concentration` — 요청 농도의 **분자·분모**를 명시하고, 유한 셀에서 표현 못 하면
     **승인받거나 거부한다**. `max(1, round(...))` 처럼 묵시적으로 1 unit 을 넣지 않는다 (BJ2 Q6).
  ④ `select_representative` — ΔE 중앙값 대표 **실재 행**
     (결정 `D-2026-09-12-cascade-representative-selection`, active).

⛔ 이 도구가 못 하는 것
  · 물리를 판정하지 않는다 — 계약 위반에서 멈출 뿐이다. 통과가 "좋은 후보" 를 뜻하지 않는다.
  · 부모 지도를 **추정하지 않는다**. 치환 전 host 를 안 주면 시작하지 않는다.
  · 형성에너지를 계산하지 않는다 — 이미 계산된 행을 받는다. 행이 어떻게 나왔는지는 못 본다.
  · 전하를 DFT 로 확인하지 않는다 — **형식전하 수지**다. 수지가 0 이라고 안정하다는 뜻이 아니다.
  · 코드 계약 실패를 "물리적으로 나쁜 후보의 탈락" 으로 세지 않는다 — 호출자가 분리해 센다
    (`is_doped_candidate` · `refusals` 를 그래서 따로 준다).

  python3 tools/cascade/s1_contract.py --selftest
"""
from __future__ import annotations
import argparse, hashlib, json, math, pathlib, sys

CONTRACT_RECORD = "db/properties/cascade_d_rel_amendment_2026_09_12.json"
CONTRACT_DECISION = "D-2026-09-12-cascade-representative-selection"
CONTRACT_EXPECT = {                      # 결정문 그대로 — 다르면 시작하지 않는다
    "rank_by": "delta_E_formation",
    "statistic": "median",
    "tie_break": "coord_sha256_lexicographic_first",
    "representative_must_be_real_row": True,
}


class S1ContractError(RuntimeError):
    """계약 위반 — 조용히 넘어가지 않고 여기서 멈춘다."""


# ─────────────────── ① 부모 자리 지도 ───────────────────
INTERSTITIAL = "interstitial"

def freeze_parent_sites(symbols, site_of_index):
    """치환 **전** host 에서 원자별 부모 자리를 굳힌다 → 승계용 기록.

    `site_of_index`: {원자 index → 자리 이름}. 전 원자를 덮어야 한다 (빠지면 멈춘다) —
    "분류가 안 되는 원자는 나중에 배위로 보면 된다" 가 바로 P0-2 의 실패 경로다.
    """
    n = len(symbols)
    missing = [i for i in range(n) if i not in site_of_index]
    if missing:
        raise S1ContractError(
            f"⛔ 부모 자리 지도가 원자 {len(missing)}개를 안 덮는다 (예: {missing[:5]}) — "
            "치환 전 host 에서 전 원자를 분류해야 승계할 수 있다 (BJ2 P0-2)")
    sites = [site_of_index[i] for i in range(n)]
    payload = json.dumps({"symbols": list(symbols), "sites": sites}, ensure_ascii=False, sort_keys=True)
    return {"kind": "parent_site_map", "n_atoms": n, "sites": sites,
            "host_symbols": list(symbols),
            "counts": {s: sites.count(s) for s in sorted(set(sites))},
            "digest": "sha256:" + hashlib.sha256(payload.encode()).hexdigest(),
            "⛔": "자리는 부모 host 의 성질이다. 현재 배위는 별도 관측값으로 따로 기록한다."}


class SiteCarrier:
    """동결된 부모 지도를 치환·공공삭제·침입추가를 지나 **승계**한다.

    치환은 자리를 바꾸지 않는다 — 점유자(occupant)만 바뀐다. 삭제는 번호를 밀고, 추가는
    `interstitial` 로 붙는다. 길이가 원자 수와 어긋나면 그 자리에서 멈춘다.
    """

    def __init__(self, parent_map, symbols):
        if len(symbols) != parent_map["n_atoms"]:
            raise S1ContractError(f"⛔ 지도({parent_map['n_atoms']}) 와 구조({len(symbols)}) 의 원자 수가 다르다")
        self.sites = list(parent_map["sites"])
        self.occupant = list(symbols)
        self.parent_symbol = list(parent_map["host_symbols"])
        self.log = []
        self.digest_in = parent_map["digest"]

    def _check(self, symbols):
        if symbols is not None and len(symbols) != len(self.sites):
            raise S1ContractError(f"⛔ 승계 어긋남: 자리 {len(self.sites)} · 원자 {len(symbols)}")

    def substitute(self, indices, element, symbols=None):
        self._check(symbols)
        for i in indices:
            if not 0 <= i < len(self.sites):
                raise S1ContractError(f"⛔ 치환 index {i} 가 범위 밖")
            if self.sites[i] == INTERSTITIAL:
                raise S1ContractError(f"⛔ 침입 원자 {i} 를 자리 치환 대상으로 삼았다 — 부모 자리가 없다")
            self.occupant[i] = element
        self.log.append({"op": "substitute", "element": element, "n": len(indices),
                         "sites": sorted({self.sites[i] for i in indices})})
        return self

    def delete(self, indices, symbols=None):
        self._check(symbols)
        drop = set(indices)
        bad = [i for i in drop if not 0 <= i < len(self.sites)]
        if bad:
            raise S1ContractError(f"⛔ 삭제 index {bad[:5]} 가 범위 밖")
        removed = sorted({self.sites[i] for i in drop})
        keep = [i for i in range(len(self.sites)) if i not in drop]
        self.sites = [self.sites[i] for i in keep]
        self.occupant = [self.occupant[i] for i in keep]
        self.parent_symbol = [self.parent_symbol[i] for i in keep]
        self.log.append({"op": "delete", "n": len(drop), "sites": removed})
        return self

    def append(self, elements, label=INTERSTITIAL):
        for el in elements:
            self.sites.append(label); self.occupant.append(el); self.parent_symbol.append(None)
        self.log.append({"op": "append", "n": len(elements), "label": label})
        return self

    def indices_of_parent_site(self, site):
        """**부모 자리**로 고른다 — 현재 배위로 다시 분류하지 않는다."""
        return [i for i, s in enumerate(self.sites) if s == site]

    def as_record(self, current_coordination=None):
        rec = {"kind": "carried_parent_sites", "n_atoms": len(self.sites),
               "parent_map_digest": self.digest_in, "ops": self.log,
               "sites": self.sites, "occupant": self.occupant,
               "counts": {s: self.sites.count(s) for s in sorted(set(self.sites))},
               "⛔": "`sites` 는 부모 자리다. 치환 뒤 현재 배위는 `current_coordination` 에 따로 있다."}
        if current_coordination is not None:
            rec["current_coordination"] = current_coordination
            rec["reclassified_by_coordination"] = [
                {"index": i, "parent_site": self.sites[i], "now": current_coordination[i]}
                for i in range(len(self.sites))
                if i < len(current_coordination) and current_coordination[i] not in (None, self.sites[i])]
        return rec


# ─────────────────── ② 전체 보상 수지 ───────────────────
def charge_ledger(placements, charges, site_charges, *, n_li_vacancy=0, n_li_interstitial=0,
                  li_charge=1):
    """양이온·**음이온**·공공·침입을 모두 더한 형식전하 수지.

    `placements`: [{"element", "site", "n"}] — cation_site 든 anion_site 든 **전부** 넣는다.
    지금 생성기는 양이온만 더해서, S²⁻→Cl⁻ 같은 음이온 치환의 Δq 가 수지에서 빠진다.
    """
    terms, net = [], 0
    for p in placements:
        el, site, n = p["element"], p["site"], int(p["n"])
        if el not in charges:
            raise S1ContractError(f"⛔ {el} 의 형식전하를 모른다 — 추측하지 않는다")
        if site not in site_charges:
            raise S1ContractError(f"⛔ 자리 {site} 의 host 형식전하를 모른다 — 추측하지 않는다")
        dq = (charges[el] - site_charges[site]) * n
        net += dq
        terms.append({"element": el, "site": site, "n": n, "q": charges[el],
                      "q_host_site": site_charges[site], "dq_total": dq})
    net += -li_charge * int(n_li_vacancy) + li_charge * int(n_li_interstitial)
    out = {"kind": "charge_ledger", "terms": terms,
           "n_li_vacancy": int(n_li_vacancy), "n_li_interstitial": int(n_li_interstitial),
           "net_charge": net, "balanced": net == 0,
           "⛔": "형식전하 수지다. 0 이라고 안정·실재를 뜻하지 않는다."}
    if net != 0:
        # net > 0 = 양전하 과잉 → Li⁺ 를 **뺀다**(공공).  net < 0 = 부족 → Li⁺ 를 **넣는다**(침입).
        out["required"] = {"li_vacancy": net} if net > 0 else {"li_interstitial": -net}
    return out


def require_balanced(ledger):
    if not ledger["balanced"]:
        raise S1ContractError(
            f"⛔ 전하 수지가 안 맞는다 (Σq={ledger['net_charge']:+d}) — 보상 경로를 선언하거나 생성을 거부한다. "
            f"필요: {ledger.get('required')}. 불균형 셀을 'UMA 가 알아서 낮게 매길 것' 으로 넘기지 않는다.")
    return ledger


# ─────────────────── ③ 농도의 분자·분모 ───────────────────
def quantize_concentration(x_request, n_fu, *, multiplicity=1, policy="exact",
                           approved_by=None, max_rel_error=None, label=None):
    """요청 농도 x 를 유한 셀의 **정수 원자수**로 옮긴다. 분자·분모를 명시한다.

      분자 = 실제로 넣은 도펀트 식단위 수 × multiplicity (원자 수)
      분모 = 셀 안 host 식단위 수 `n_fu`
      x_actual = 분자 / (분모 × multiplicity)

    policy
      "exact"           정수로 안 떨어지면 **거부**(기본). 계약 실패이지 물리적 탈락이 아니다.
      "approve_nearest" 가장 가까운 정수로 양자화하되 `approved_by` 가 있어야 하고, 기록에
                        x_request·x_actual·상대오차를 남긴다. `max_rel_error` 를 넘으면 거부.
      "refuse"          양자화가 필요하면 무조건 거부 (사전 선언용).

    ⛔ `max(1, ...)` 은 없다. x 가 작아 0 이 나오면 그것은 **무도핑 대조군**이고
       도핑 후보 수에 넣지 않는다 (`is_doped_candidate=False`).
    """
    if n_fu <= 0:
        raise S1ContractError("⛔ n_fu 가 0 이하다 — 분모가 없으면 농도가 정의되지 않는다")
    if x_request < 0:
        raise S1ContractError("⛔ 음수 농도")
    exact = x_request * n_fu
    n_units = int(round(exact))
    is_int = abs(exact - round(exact)) < 1e-9
    out = {"kind": "concentration_quantization", "x_request": x_request, "n_fu": n_fu,
           "multiplicity": multiplicity, "policy": policy, "label": label,
           "n_units_exact": exact, "quantized": not is_int}
    if not is_int:
        if policy in ("exact", "refuse"):
            raise S1ContractError(
                f"⛔ x={x_request} 는 n_fu={n_fu} 셀에서 정수 식단위가 아니다 (필요 {exact:.4f}). "
                f"policy='{policy}' 이므로 **생성을 거부한다** — 묵시적 반올림·최소 1 unit 을 넣지 않는다. "
                "쓰려면 policy='approve_nearest' 와 approved_by 를 명시해 사전 승인하라 (BJ2 Q6).")
        if not approved_by:
            raise S1ContractError("⛔ policy='approve_nearest' 는 approved_by(승인자) 가 있어야 한다")
        out["approved_by"] = approved_by
    n_atoms = n_units * multiplicity
    x_actual = n_units / n_fu
    rel = abs(x_actual - x_request) / x_request if x_request > 0 else 0.0
    out.update({"n_units": n_units, "numerator_atoms": n_atoms, "denominator_host_fu": n_fu,
                "x_actual": x_actual, "rel_error": rel,
                "is_doped_candidate": n_units > 0,
                "role": ("doped" if n_units > 0 else "undoped_control")})
    if max_rel_error is not None and rel > max_rel_error:
        raise S1ContractError(
            f"⛔ 양자화 오차 {rel:.3f} > 허용 {max_rel_error} (x {x_request} → {x_actual:.4f}) — 거부")
    if n_units == 0 and x_request > 0:
        out["⛔"] = ("요청 x>0 인데 정수 0 이다 → 이것은 **무도핑 대조군**이다. 도핑 후보 수에서 분리하고, "
                    "'도펀트가 나쁘다' 로 읽지 않는다 (BJ2 Q6).")
    return out


# ─────────────────── ④ 대표 배열 선택 ───────────────────
def load_representative_contract(record_path=CONTRACT_RECORD):
    """개정 기록에서 `기계_판독` 블록을 읽는다. 없거나 결정문과 다르면 **시작하지 않는다**."""
    p = pathlib.Path(record_path)
    if not p.is_file():
        raise S1ContractError(f"⛔ 대표 선택 계약 기록이 없다: {record_path}")
    doc = json.loads(p.read_text(encoding="utf-8"))

    def find(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "기계_판독":
                    return v
                r = find(v)
                if r is not None:
                    return r
        elif isinstance(o, list):
            for v in o:
                r = find(v)
                if r is not None:
                    return r
        return None

    blk = find(doc)
    if blk is None:
        raise S1ContractError(f"⛔ {record_path} 에 `기계_판독` 블록이 없다 — 대표 선택을 시작하지 않는다")
    for k, v in CONTRACT_EXPECT.items():
        if blk.get(k) != v:
            raise S1ContractError(
                f"⛔ 대표 선택 계약 불일치: {k}={blk.get(k)!r} 인데 결정 {CONTRACT_DECISION} 은 {v!r} 이다 — 멈춘다")
    if "design" not in (blk.get("applies_to") or []) or "host" not in (blk.get("applies_to") or []):
        raise S1ContractError(f"⛔ applies_to 가 design·host 를 둘 다 담지 않는다: {blk.get('applies_to')!r}")
    return dict(blk)


def _row_key(row, i):
    return row.get("id") or row.get("arrangement_id") or f"row{i}"


def select_representative(rows, contract, *, kind="design"):
    """같은 조성의 배열 행들 중 **ΔE 중앙값을 낸 실재 행 하나**를 고른다.

    짝수면 가운데 두 행 중 `coord_sha256` 사전순 앞. **평균을 내지 않는다** — 평균은 어떤 행도
    아니어서 그 좌표로 MD 를 돌릴 수 없다(합성 벡터). 그게 `representative_must_be_real_row` 다.
    """
    if kind not in contract.get("applies_to", []):
        raise S1ContractError(f"⛔ 계약이 kind={kind!r} 를 덮지 않는다 (applies_to={contract.get('applies_to')})")
    if not rows:
        raise S1ContractError(f"⛔ kind={kind}: 배열 행이 없다 — 대표를 지어내지 않는다")
    key = contract["rank_by"]
    clean = []
    for i, r in enumerate(rows):
        if r.get("synthetic") or r.get("source") in ("aggregate", "mean", "fit"):
            raise S1ContractError(
                f"⛔ {_row_key(r, i)} 은 합성/집계 행이다 (source={r.get('source')!r}) — 대표는 실재 행이어야 한다")
        if key not in r or r[key] is None:
            raise S1ContractError(f"⛔ {_row_key(r, i)} 에 {key} 가 없다 — 결측을 최악·최선 어느 쪽으로도 채우지 않는다")
        v = float(r[key])
        if not math.isfinite(v):
            raise S1ContractError(f"⛔ {_row_key(r, i)} 의 {key} 가 유한하지 않다 ({r[key]!r})")
        h = r.get("coord_sha256")
        if not h or not isinstance(h, str):
            raise S1ContractError(
                f"⛔ {_row_key(r, i)} 에 coord_sha256 이 없다 — 대표는 좌표해시로 MD 에 넘어간다 (카드 §7)")
        clean.append((v, h, i, r))
    clean.sort(key=lambda t: (t[0], t[1]))
    n = len(clean)
    if n % 2 == 1:
        pick = clean[n // 2]; tie = None
    else:
        a, b = clean[n // 2 - 1], clean[n // 2]
        pick = a if a[1] <= b[1] else b                     # 사전순 앞 — 평균 금지
        tie = {"between": [_row_key(a[3], a[2]), _row_key(b[3], b[2])],
               "delta_E": [a[0], b[0]], "rule": contract["tie_break"]}
    return {"kind": "representative_selection", "for": kind, "n_rows": n,
            "rank_by": key, "statistic": contract["statistic"],
            "selected_id": _row_key(pick[3], pick[2]), "selected_index": pick[2],
            "delta_E_formation": pick[0], "coord_sha256": pick[1],
            "tie_break_applied": tie,
            "contract": {k: contract.get(k) for k in ("rank_by", "statistic", "tie_break", "applies_to")},
            "decision": CONTRACT_DECISION,
            "⛔": "대표 선택일 뿐이다 — 캠페인 실행 승인도, 이 배열이 옳다는 뜻도 아니다."}


def select_design_and_host(design_rows, host_rows, contract=None):
    """설계와 **host 에 같은 규칙**. host 행이 없으면 시작하지 않는다 (결정문의 'host 에도')."""
    contract = contract or load_representative_contract()
    if not host_rows:
        raise S1ContractError(
            "⛔ host 대표 행이 없다 — 결정은 'host 에도 같은 규칙' 이다. host 를 다른 규칙(최저·첫 행)으로 "
            "두면 D_rel 의 분모가 설계와 다른 정책으로 뽑힌 것이 된다. 멈춘다.")
    return {"design": select_representative(design_rows, contract, kind="design"),
            "host": select_representative(host_rows, contract, kind="host")}


# ─────────────────── selftest ───────────────────
def _selftest():
    ok = bad = 0

    def chk(c, m):
        nonlocal ok, bad
        print(("  ⭕ " if c else "  ⛔ ") + m); ok += bool(c); bad += (not c)

    def fails(fn, needle=""):
        try:
            fn()
        except S1ContractError as e:
            return needle in str(e)
        except Exception:
            return False
        return False

    # ① 부모 자리 지도 — P0-2 재현
    #    host: P(0) + PS₄ 의 S(1..4) + free S(5) + Li(6,7).  P→B 치환 뒤 배위로 다시 분류하면
    #    1..4 가 free S 로 넘어간다. 부모 지도는 안 넘어가야 한다.
    sym = ["P", "S", "S", "S", "S", "S", "Li", "Li"]
    smap = {0: "P_4b", 1: "S_16e", 2: "S_16e", 3: "S_16e", 4: "S_16e", 5: "S_4a", 6: "Li_24g", 7: "Li_24g"}
    pm = freeze_parent_sites(sym, smap)
    chk(pm["counts"]["S_16e"] == 4 and pm["digest"].startswith("sha256:"), "부모 지도 동결 — S_16e 4개 · digest")
    chk(fails(lambda: freeze_parent_sites(sym, {0: "P_4b"}), "안 덮는다"),
        "⛔음성: 지도가 전 원자를 안 덮으면 멈춘다 (배위로 나중에 보면 된다 = P0-2 경로)")

    car = SiteCarrier(pm, sym).substitute([0], "B")
    coord_now = ["B_site"] + ["S_free"] * 5 + ["Li_24g", "Li_24g"]   # 배위로 다시 분류하면 이렇게 된다
    rec = car.as_record(current_coordination=coord_now)
    chk(car.indices_of_parent_site("S_16e") == [1, 2, 3, 4],
        "P→B 치환 뒤에도 부모 S_16e 는 [1,2,3,4] — 배위 재분류를 따라가지 않는다 (P0-2 고침)")
    chk(len(rec["reclassified_by_coordination"]) == 6,
        f"현재 배위가 부모와 다른 원자 {len(rec['reclassified_by_coordination'])}개를 **관측값으로 따로** 기록")
    car.delete([6])
    chk(car.indices_of_parent_site("S_16e") == [1, 2, 3, 4] and car.sites[-1] == "Li_24g" and len(car.sites) == 7,
        "Li 공공 삭제 뒤 번호 재배열을 승계한다")
    car.append(["Li"])
    chk(car.sites[-1] == INTERSTITIAL and fails(lambda: car.substitute([7], "Na"), "침입"),
        "⛔음성: 침입 원자는 부모 자리가 없으므로 자리 치환 대상이 될 수 없다")
    chk(fails(lambda: SiteCarrier(pm, sym[:3]), "원자 수가 다르다"), "⛔음성: 지도와 구조의 원자 수가 다르면 멈춘다")
    chk(fails(lambda: SiteCarrier(pm, sym).delete([99]), "범위 밖"), "⛔음성: 범위 밖 index 삭제 거부")

    # ② 전체 보상 수지 — 음이온이 빠지던 것
    Q = {"Li": 1, "P": 5, "S": -2, "Cl": -1, "Nd": 3, "B": 3}
    SQ = {"P_4b": 5, "S_16e": -2, "S_4a": -2, "Li_24g": 1, "Cl_4d": -1}
    pl = [{"element": "Nd", "site": "P_4b", "n": 1}, {"element": "Cl", "site": "S_4a", "n": 1}]
    cat_only = charge_ledger(pl[:1], Q, SQ)
    both = charge_ledger(pl, Q, SQ)
    chk(cat_only["net_charge"] == -2 and both["net_charge"] == -1,
        f"음이온 항이 수지에 들어간다 — 양이온만 {cat_only['net_charge']:+d} → 전체 {both['net_charge']:+d}")
    chk(both["required"] == {"li_interstitial": 1}, "불균형이면 필요한 보상량을 말한다 (Li 침입 1)")
    fixed = charge_ledger(pl, Q, SQ, n_li_interstitial=1)
    chk(fixed["balanced"] and require_balanced(fixed) is fixed, "보상을 넣으면 수지 0")
    chk(fails(lambda: require_balanced(both), "수지가 안 맞는다"),
        "⛔음성: 불균형 셀을 'UMA 가 낮게 매길 것' 으로 흘려보내지 않고 멈춘다")
    chk(fails(lambda: charge_ledger([{"element": "Zz", "site": "P_4b", "n": 1}], Q, SQ), "형식전하를 모른다"),
        "⛔음성: 모르는 원소의 전하를 추측하지 않는다")
    chk(fails(lambda: charge_ledger([{"element": "Nd", "site": "X_9z", "n": 1}], Q, SQ), "자리"),
        "⛔음성: 모르는 자리의 host 전하를 추측하지 않는다")

    # ③ 농도의 분자·분모
    q = quantize_concentration(0.25, 8, label="x=0.25")
    chk(q["n_units"] == 2 and q["numerator_atoms"] == 2 and q["denominator_host_fu"] == 8
        and abs(q["x_actual"] - 0.25) < 1e-12 and q["is_doped_candidate"], "정수로 떨어지는 농도: 분자 2 / 분모 8")
    chk(fails(lambda: quantize_concentration(0.1, 4), "거부한다"),
        "⛔음성: x=0.1·n_fu=4 (0.4 unit) 는 기본 policy 에서 **생성 거부** — 묵시적 반올림 없음")
    chk(fails(lambda: quantize_concentration(0.1, 4, policy="approve_nearest"), "approved_by"),
        "⛔음성: 승인자 없이 양자화 못 한다")
    qa = quantize_concentration(0.1, 4, policy="approve_nearest", approved_by="1저자")
    chk(qa["n_units"] == 0 and not qa["is_doped_candidate"] and qa["role"] == "undoped_control",
        "⛔핵심: 0.4 → **0 unit (무도핑 대조군)**. 옛 max(1,round) 이면 1 을 넣어 x=0.25 로 둔갑했다")
    chk(fails(lambda: quantize_concentration(0.1, 4, policy="approve_nearest", approved_by="1저자",
                                             max_rel_error=0.2), "양자화 오차"),
        "⛔음성: 허용 상대오차를 넘으면 거부")
    chk(fails(lambda: quantize_concentration(0.1, 0), "분모"), "⛔음성: n_fu=0 이면 농도가 정의되지 않는다")

    # ④ 대표 배열 — 실재 기록의 계약으로
    root = pathlib.Path(__file__).resolve().parents[2]
    con = load_representative_contract(root / CONTRACT_RECORD)
    chk(con["rank_by"] == "delta_E_formation" and con["statistic"] == "median",
        f"실재 개정 기록에서 계약을 읽는다 ({CONTRACT_RECORD})")
    rows = [{"id": f"a{i}", "delta_E_formation": e, "coord_sha256": h}
            for i, (e, h) in enumerate([(-0.30, "cc"), (-0.10, "aa"), (-0.20, "bb")])]
    r = select_representative(rows, con)
    chk(r["selected_id"] == "a2" and abs(r["delta_E_formation"] + 0.20) < 1e-12,
        "홀수 3행: 중앙값 행(−0.20) 이 대표 — 최저(−0.30) 가 아니다")
    ev = [{"id": "x", "delta_E_formation": 1.0, "coord_sha256": "ff"},
          {"id": "y", "delta_E_formation": 2.0, "coord_sha256": "0a"}]
    r2 = select_representative(ev, con)
    chk(r2["selected_id"] == "y" and r2["delta_E_formation"] in (1.0, 2.0) and r2["tie_break_applied"],
        "짝수 2행: 평균 1.5 를 만들지 않고 사전순 앞('0a') 실재 행을 고른다")
    chk(fails(lambda: select_representative(
        [{"id": "s", "delta_E_formation": 1.0, "coord_sha256": "aa", "source": "mean"}], con), "실재 행"),
        "⛔음성: 합성·집계 행은 대표가 될 수 없다 (합성 벡터로 MD 를 못 돌린다)")
    chk(fails(lambda: select_representative([{"id": "n", "delta_E_formation": 1.0}], con), "coord_sha256"),
        "⛔음성: 좌표해시 없는 행 거부")
    chk(fails(lambda: select_representative([{"id": "m", "coord_sha256": "aa"}], con), "delta_E_formation"),
        "⛔음성: ΔE 결측을 최악·최선으로 채우지 않는다")
    chk(fails(lambda: select_representative([], con), "행이 없다"), "⛔음성: 빈 목록에서 대표를 지어내지 않는다")
    chk(fails(lambda: select_design_and_host(rows, [], con), "host 대표 행이 없다"),
        "⛔음성: host 행이 없으면 멈춘다 (host 에도 같은 규칙)")
    both_sel = select_design_and_host(rows, ev, con)
    chk(both_sel["design"]["selected_id"] == "a2" and both_sel["host"]["selected_id"] == "y",
        "설계·host 에 같은 규칙을 적용한다")
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = pathlib.Path(td) / "tampered.json"
        p.write_text(json.dumps({"x": {"기계_판독": {**CONTRACT_EXPECT, "statistic": "min",
                                                    "applies_to": ["design", "host"]}}}, ensure_ascii=False))
        chk(fails(lambda: load_representative_contract(p), "계약 불일치"),
            "⛔음성: 기록이 statistic=min 으로 바뀌어 있으면 시작하지 않는다 (최저 정책 되살아나기 차단)")
        p2 = pathlib.Path(td) / "noblock.json"; p2.write_text("{}")
        chk(fails(lambda: load_representative_contract(p2), "기계_판독"), "⛔음성: 기계_판독 블록이 없으면 멈춘다")
        chk(fails(lambda: load_representative_contract(pathlib.Path(td) / "nope.json"), "없다"),
            "⛔음성: 계약 기록 파일이 없으면 멈춘다")
    print(f"selftest: ⭕ {ok} · ⛔ {bad}")
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description="cascade S1 계약 + 대표 배열 선택")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--show_contract", action="store_true", help="대표 선택 계약을 읽어 찍는다")
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if a.show_contract:
        root = pathlib.Path(__file__).resolve().parents[2]
        print(json.dumps(load_representative_contract(root / CONTRACT_RECORD), ensure_ascii=False, indent=1))
        return
    ap.print_help()


if __name__ == "__main__":
    main()
