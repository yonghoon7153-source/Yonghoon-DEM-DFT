"""P3-a 한정 점검 — 큰 정수의 JSON 읽기 (`_json_strict`) · 사유 표시 (`_show`) 가 이 인터프리터에서 어떻게 되나 (자리 수 401 · 5001).
쓰임: python3 int_digits_check.py <scripts 뿌리>"""
import sys

sys.path.insert(0, sys.argv[1])
import rint_r_chain as R  # noqa: E402

print('python', sys.version.split()[0])
for nd in (401, 5001):
    raw = ('{"x": 1' + '0' * (nd - 1) + '}').encode()
    try:
        v = R._json_strict(raw)['x']
        print(f'_json_strict 정수 {nd} 자리: 읽음 ({type(v).__name__})')
    except ValueError as e:
        print(f'_json_strict 정수 {nd} 자리: ValueError ({str(e)[:48]})')
    try:
        print(f'_show(10**{nd - 1}): {R._show(10 ** (nd - 1))}')
    except ValueError as e:
        print(f'_show(10**{nd - 1}): ValueError ({str(e)[:48]})')
