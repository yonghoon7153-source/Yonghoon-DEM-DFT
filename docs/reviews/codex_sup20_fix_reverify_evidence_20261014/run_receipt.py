from run_checks import *
tests.update(receipt_selftest=['scripts/supp20_input_receipt.py','--selftest'],receipt_default=['scripts/supp20_input_receipt.py','--json',str(E/'receipt_default.json')])
for name in ('receipt_selftest','receipt_default'):run(name)
