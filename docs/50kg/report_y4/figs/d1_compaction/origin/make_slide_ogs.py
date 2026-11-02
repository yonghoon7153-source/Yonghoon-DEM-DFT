"""슬라이드 칸 크기 (3.50 × 3.85 in · 1저자 11-03 *"이 사이즈로 origin 도 만들꺼니까"*) 용 .ogs — 같은 폴더의 .ogs 를 읽어
그림 영역 크기 · 눈금 길이 · 축 이름 크기만 바꿔 slide_350x385/ 에 쓴다 (값 · 범위 · 경계선 · 색 · 선 굵기 = 그대로).
1저자 11-03 BML 서식 유지: 눈금 글씨 28 pt · 축 이름 34 pt · Copy Page fixed factor 0.7 (붙인 뒤 칸에 맞춰 줄임).
그림 영역 = 슬라이드 칸 (생성기 --figsize 3.5 3.85 에서 잰 6.89 × 2.40 cm · 패널 사이 0.43 cm) × 3.556 배 = 24.5 × 8.5 cm · 패널 사이 1.53 cm
(축 이름 34 pt 한 줄 'Measured pressure' 가 패널 높이를 1.2 배 넘지 않는 배율 = 옛 ps73 발표 그림과 같은 비율) → 칸에 맞추면 눈금 ≈ 7.9 pt · 축 이름 ≈ 9.6 pt.
⚠ Origin 이 이 기계에 없어 실행 확인 안 함 (기존 .ogs 와 같은 명령만 씀 · fsize 두 줄 추가).
usage: python3 -I make_slide_ogs.py"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / 'slide_350x385'
W_CM, H_CM = 24.5, 8.5
REP = [(r'layer\.width = 10; layer\.height = 8;', 'layer.width = %.2f; layer.height = %.2f;' % (W_CM, H_CM)),
       (r'font\(Aptos\)', 'font(Arial)'),                          # 1저자 11-03 *"arial이고"*
       (r'\.ticklength = 6', '.ticklength = 12'),
       (r'\.mticklength = 3', '.mticklength = 6')]


def convert(text):
    for pat, new in REP:
        text, n = re.subn(pat, new, text)
        assert n >= 1, pat
    text = re.sub(r'(label -xb [^;]*;)', r'\1 xb.font = font(Arial); xb.fsize = 34;', text)
    text = re.sub(r'(label -yl [^;]*;)', r'\1 yl.font = font(Arial); yl.fsize = 34;', text)
    return text


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    for f in sorted(HERE.glob('*.ogs')):
        t = convert(f.read_text(encoding='utf-8'))
        head = ('// [슬라이드 칸 3.50 × 3.85 in 판 · make_slide_ogs.py 가 %s 에서 만듦 · 그림 영역 %.2f × %.2f cm · Arial · 눈금 28 pt · 축 이름 34 pt · fixed factor 0.7]\n'
                % (f.name, W_CM, H_CM))
        (OUT / f.name).write_text(head + t, encoding='utf-8')
        print('wrote', (OUT / f.name).relative_to(HERE))
