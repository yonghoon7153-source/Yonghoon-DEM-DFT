"""Concatenate the per-case CLI logs written by run_d2_cli_cases.py (one file per case × consumer) into one
text file with a header per log, then remove the per-case files.  Content is copied byte-for-byte (decoded UTF-8).

Usage: python3 -I concat_cli_logs.py <dir with *__*.log> <out.txt>
"""
import os
import sys


def main(folder, out):
    names = sorted(n for n in os.listdir(folder) if n.endswith('.log') and '__' in n)
    blocks = []
    for name in names:
        path = os.path.join(folder, name)
        with open(path, 'rb') as g:
            blocks.append(f'=== {name} ===\n' + g.read().decode('utf-8', 'replace').rstrip('\n') + '\n')
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(blocks))
    for name in names:
        os.remove(os.path.join(folder, name))
    print(len(names), 'logs ->', out)


if __name__ == '__main__':
    main(*sys.argv[1:])
