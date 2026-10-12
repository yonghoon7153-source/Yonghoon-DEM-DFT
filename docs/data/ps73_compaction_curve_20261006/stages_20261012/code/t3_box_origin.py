"""ps73 SE von Mises — Origin 상자그림 입력 CSV (접촉 상대별 네 열 · 벽 아닌 SE 만).

입력 (읽기만): ../t3_vm_se/ps73_se_vm_3220000.csv.gz  (SE 별 Love–Weber σ_VM · t3_vm_se.py 출력)
출력:          ../t3_vm_se/ps73_se_vm_by_class_boxdata_origin.csv.gz  (gzip mtime 0 = 같은 입력이면 같은 바이트 · 풀면 utf-8-sig CSV)
검산:          열마다 개수 · 중앙값 = ../t3_vm_se/ps73_se_vm_class_summary.csv (n_nonwall · median_MPa 4 유효숫자) — 어긋나면 멈춘다.
실행:          cd <이 폴더> && python3 -I -B t3_box_origin.py      (표준 라이브러리만)
"""
import csv
import gzip
import io
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
T3 = HERE.parent / 't3_vm_se'
SRC = T3 / 'ps73_se_vm_3220000.csv.gz'
SUMMARY = T3 / 'ps73_se_vm_class_summary.csv'
#: 리포에는 .csv.gz (숫자 15만 개가 철회값 스윕의 문자열과 우연히 겹친다 — 원자료 CSV.gz 와 같은 처리) · Origin 에 넣을 때 `gunzip -k`
OUT = T3 / 'ps73_se_vm_by_class_boxdata_origin.csv.gz'

CLASSES = [('SE_only', 'SE only'), ('PC_only', 'PC only'), ('SC_only', 'SC only'), ('PC_and_SC', 'PC + SC')]


def sig4(x):
    return float(f'{x:.4g}')


def main():
    cols = {k: [] for k, _ in CLASSES}
    with gzip.open(SRC, 'rt', encoding='utf-8', newline='') as fh:
        for row in csv.DictReader(fh):
            if row['wall_flag'] != '0':
                continue
            if row['class'] in cols:
                cols[row['class']].append(row['vm_MPa'])
    with open(SUMMARY, encoding='utf-8', newline='') as fh:
        summ = {r['class']: r for r in csv.DictReader(fh)}
    for k, label in CLASSES:
        n = len(cols[k])
        med = sig4(statistics.median(float(v) for v in cols[k]))
        want_n = int(summ[k]['n_nonwall'])
        want_med = float(summ[k]['median_MPa'])
        if n != want_n or med != want_med:
            raise SystemExit(f'검산 실패 {label}: n {n} ≠ {want_n} 또는 중앙값 {med} ≠ {want_med}')
        print(f'{label}: n {n} · 중앙값 {med} MPa = 요약표')
    rows = max(len(v) for v in cols.values())
    buf = io.StringIO(newline='')
    if True:
        w = csv.writer(buf, lineterminator='\n')
        w.writerow([label for _, label in CLASSES])
        w.writerow(['MPa'] * len(CLASSES))
        w.writerow([f'n = {len(cols[k])} · Love–Weber σ_VM · step 3220000 · walls excluded' for k, _ in CLASSES])
        for i in range(rows):
            w.writerow([cols[k][i] if i < len(cols[k]) else '' for k, _ in CLASSES])
    with open(OUT, 'wb') as fb, gzip.GzipFile(filename='', mode='wb', fileobj=fb, mtime=0) as gz:
        gz.write(('\ufeff' + buf.getvalue()).encode('utf-8'))
    print(f'쓴 파일 {OUT.name} · 자료 행 {rows}')


if __name__ == '__main__':
    main()
