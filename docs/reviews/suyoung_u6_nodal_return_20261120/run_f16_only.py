"""Run only F16 from its initial state with the original nodal solver."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PIN = "00f0a1758349079a10d9c3fe9d1424620117dd27"
F12_SHA = "17ba7c13bb857fb399c004933a1f0fd85a54cd8f32e0847d4852c46aa4b87cc0"
F16_PRIOR_TRACE = "f36f83d73488946b8b4958f85ae403712972ff15e77022ee794db32beaf87326"
GO = "GO_F16_1200_ONCE"


def single(output, reference, run, assess):
    if hashlib.sha256(reference).hexdigest() != F12_SHA:
        raise ValueError("F12 returned bytes differ")
    output.mkdir(exist_ok=False)
    (output/"F12_returned.json").write_bytes(reference)
    arm = output/"F16"
    run(16, arm, 1170.)
    a = json.loads(reference)
    b = json.loads((arm/"result.json").read_bytes())
    assessment = assess(a,b)
    # A CRC-free numerical comparison on the repeated trajectory is provided as
    # a separate bitwise check of unchanged bytes at the previous endpoint.
    with (arm/"trace.csv").open("rb") as stream:
        lines = list(itertools.islice(stream,5244))  # header + steps 0..5242
        prefix_status = ("PRIOR_ENDPOINT_NOT_REACHED" if len(lines)<5244 else
                         "IDENTICAL" if hashlib.sha256(b"".join(lines)).hexdigest()==F16_PRIOR_TRACE
                         else "DIFFERENT")
    record = dict(label="DEVELOPMENT_ONLY", solver_pin=PIN, setting=1, assessment=assessment,
                  F12_source="accepted_return_20261120", F12_sha256=F12_SHA,
                  F12_phi=a["phi_m"], F16_phi=b["phi_m"], F16_previous_trace_prefix=prefix_status,
                  previous_F16_status="TIME_LIMIT", selected_setting=None, u6_qualified=False)
    (output/"comparison.json").write_text(json.dumps(record,indent=2)+"\n",encoding="ascii")
    print(json.dumps(record,sort_keys=True))
    return 4 if assessment=="INCOMPLETE" else 0


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("approval",choices=(GO,))
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    sys.path.insert(0,str(HERE))
    import suyoung_u6_first_dev as model
    return single(args.output,(HERE/"f12_result.json").read_bytes(),model.run,model.assess)


if __name__=="__main__":
    raise SystemExit(main())
