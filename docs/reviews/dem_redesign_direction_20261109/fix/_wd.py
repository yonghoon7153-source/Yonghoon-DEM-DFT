import difflib, sys
A = open('memo_v3_2_before_review5.md', encoding='utf-8').read().split('\n')
B = open('memo_v3_2.md', encoding='utf-8').read().split('\n')
sm = difflib.SequenceMatcher(a=A, b=B, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    a = '\n'.join(A[i1:i2]).split(' ')
    b = '\n'.join(B[j1:j2]).split(' ')
    s2 = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    out = []
    for t2, x1, x2, y1, y2 in s2.get_opcodes():
        if t2 == 'equal':
            continue
        ctx = ' '.join(a[max(0, x1 - 4):x1])
        out.append(f'   …{ctx} [-{" ".join(a[x1:x2])}-] {{+{" ".join(b[y1:y2])}+}}')
    print(f'== 옛 {i1+1}-{i2} → 새 {j1+1}-{j2}')
    print('\n'.join(out))
