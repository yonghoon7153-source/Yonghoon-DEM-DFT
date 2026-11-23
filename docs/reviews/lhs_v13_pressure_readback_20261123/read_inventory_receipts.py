"""Read five fixed public metadata blobs, returning WSL30 structural counts only."""
import base64
import hashlib
import json
import zlib

BASE = "9352c4ece10a64a04ffd620062894bd616589582"
BLOBS = {
    "docs/data/lhs_wsl30_inventory_20261108/lhs_wsl30_inventory_received_20261108.json":
        "590db9cc8dcaf0802f48a720159435d0631a6e11ac005152f0137b756cb35158",
    "docs/data/lhs_wsl30_inventory_20261108/lhs_wsl30_inventory_receipt_20261108.json":
        "566a6323317257215a852b9b3cdd7d4bc370a0afb307ab3cdb79528027eac9c8",
    "docs/data/lhs_o1_current_identity_20261116/current_identity.json":
        "9c3d1aedebcd54a1265f224017cea8a61876eb0ae38f920172c63b9b2a86ceb1",
    "docs/data/lhs_o1_current_identity_20261116/receipt.json":
        "348814e1ee8afc7bced7e3d8f5db66e91f7f478ff7139b932d6ed76f8f48c0e7",
    "docs/reviews/nonrint_development_returns_20261118/lhs_v13_author_source_lead.json":
        "0871162eb4508ee0911b29e9ccf45416c660389ed0344637fe21f78d7f18b15f",
}


def unique(pairs):
    obj = dict(pairs)
    if len(obj) != len(pairs):
        raise ValueError("duplicate metadata key")
    return obj


def require(condition):
    if not condition:
        raise ValueError("fixed metadata contract mismatch")


def readback(raw):
    require(raw.keys() == BLOBS.keys())
    for path, expected in BLOBS.items():
        require(hashlib.sha256(raw[path]).hexdigest() == expected)
    inv, receipt, decks, o1, lead = [
        json.loads(raw[path], object_pairs_hook=unique) for path in BLOBS
    ]

    require(inv["mode"] == "wsl" and inv["status"] == "INVENTORY_COMPLETE")
    require(inv["rc"] == receipt["reported_process_rc"] == 0)
    require(receipt["extracted_json_sha256"] == next(iter(BLOBS.values())))
    require(o1["json_sha256"] == BLOBS["docs/data/lhs_o1_current_identity_20261116/current_identity.json"])
    require(o1["operator_reported_rc"] == o1["operator_reported_command_rc"] == 0)
    require(o1["cohort_deck_hash_matches"] == 30)
    require(lead["source_kind"] == "NONE_KNOWN" and lead["source_verified"] is False)
    require(lead["execution_identity"] == decks["execution_identity_status"] == "NOT_ESTABLISHED")
    require(lead["value_access_authorized_by_this_record"] is False)
    require(receipt["canonical_log_selected"] is False and receipt["pressure_qualification_established"] is False)

    names = {"lhs00_%03d" % n for n in range(100, 130)}
    require({r["case"] for r in inv["cases"]} == names and len(inv["cases"]) == 30)
    require({r["alias"] for r in decks["cases"]} == {"current_deck_" + n for n in names})
    require(len(decks["cases"]) == 30)
    rows = []
    for record in sorted(inv["cases"], key=lambda r: r["case"]):
        require(record["status"] == "COUNTED" and record["root"] == "local")
        logs = record["logs"]
        require(set(logs) == {"log.liggghts", "log.txt"})
        left, right = logs["log.liggghts"], logs["log.txt"]
        require(left["status"] == right["status"] == "COUNTED")
        require(left["b7_matches"] == right["b7_matches"] > 0 and left["bytes"] != right["bytes"])
        rows.append({"case": record["case"], "b7_rows_each": left["b7_matches"],
                     "log_liggghts_bytes": left["bytes"], "log_txt_bytes": right["bytes"]})
    require(len(rows) * 2 == receipt["counted_required_logs"])
    return {"status": "RECEIVED_METADATA_READBACK_OK", "input_commit": BASE,
            "inventory_observation_date": "2026-11-08", "cases": rows, "cases_counted": len(rows),
            "logs_counted": len(rows) * 2, "current_deck_matches_recorded_2026_11_16": 30,
            "source_lead_as_reported": lead["source_kind"], "execution_identity": lead["execution_identity"],
            "canonical_run_segment": "UNSELECTED", "A_or_C": "UNSELECTED",
            "section5_pressure_qualification": "UNRESOLVED", "tau": "NOT_EVALUATED",
            "release_v13": "NOT_AUTHORIZED", "study_files_opened": 0, "value_access": "NOT_GRANTED"}


def unpack_metadata(encoded):
    entries = json.loads(zlib.decompress(base64.b64decode(encoded, validate=True)),
                         object_pairs_hook=unique)
    return {name: base64.b64decode(value, validate=True) for name, value in entries.items()}
