import re, sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, old[:80])
    s = s.replace(old, new)

# 1. title
rep('(2026-11-12 · 내부 반박 리뷰 1 · 2 · 3 회차 반영판)', '(2026-11-12 · 내부 반박 리뷰 1 · 2 · 3 · 4 회차 반영판)')
# 2. target line
rep('> 대상: `memo_v3_2.md` (같은 폴더 · 1124 줄 · sha256 앞 16 자리 `3aae76fc2e89f2e0` = 이 표를 고칠 때 값 · 내부 반박 리뷰 3 회차까지 반영한 판 · 반입 전).  2 회차를 반영한 판 =',
    '> 대상: `memo_v3_2.md` (같은 폴더 · 1205 줄 · sha256 앞 16 자리 `fe315298b6a1d6b7` = 이 표를 고칠 때 값 · 내부 반박 리뷰 4 회차 재확인까지 반영한 판 · 마지막 고침 회차 · 반입 전).  3 회차를 반영한 판 = `memo_v3_2_before_review4.md` (1124 줄 · `3aae76fc2e89f2e0`) · 그때의 이 표 = `docs/reviews/dem_redesign_direction_20261109/fix/drd_table_before_review4.md`.  2 회차를 반영한 판 =')
# 3. reviews line
rep('3 회차 = `docs/reviews/dem_redesign_direction_20261109/review/review3_memo32.md` (독립 조수 · Codex 아님 · 11-12 · P1 0 · P2 4 · P3 5 · 2 회차 일부 3) · 처분 = `docs/reviews/dem_redesign_direction_20261109/review/disposition3.md`.',
    '3 회차 = `docs/reviews/dem_redesign_direction_20261109/review/review3_memo32.md` (독립 조수 · Codex 아님 · 11-12 · P1 0 · P2 4 · P3 5 · 2 회차 일부 3) · 처분 = `docs/reviews/dem_redesign_direction_20261109/review/disposition3.md`.  4 회차 재확인 = `docs/reviews/dem_redesign_direction_20261109/review/review4_recheck_memo32.md` (독립 조수 · Codex 아님 · 11-12 · 고친 곳만 · P1 0 · P2 3 · P3 6 · 3 회차 일부 1) · 처분 = `docs/reviews/dem_redesign_direction_20261109/review/disposition4.md`.')
# 4. numbers line
rep('못 닿음을 확인하는 Φ_cap 팔의 δ · τ · U6 (b) 의 촉발 문턱) 는 모두 [제안 · 봉인 전] 이다.',
    '못 닿음을 확인하는 Φ_cap 팔의 δ · τ · U6 (b) 의 두 신호 문턱 (치우침 τ · 잡음 τ/2 · 4 회차) · 띠 팔의 큰 변화 문턱 (띠 폭의 1/4 · 4 회차)) 는 모두 [제안 · 봉인 전] 이다.  치우침 신호의 기대 범위 d₁ × [1.46 , 4.23] 은 겉보기 차수 0.1 – 3.08 에서 유도한 값이라 따로 정하지 않는다.')
# 5. 집계
rep('> - 이 판 (3 회차 지적을 고친 뒤 · 재확인 전 · 우리 판단): DRD 13 = **닫힘 12** · **일부 1** (DRD-10 그대로) · **안 닫힘 0**.  `SELF-160` · `SELF-161` = 메모 범위 닫힘 2 (원장 open).  MR3 아홉 = 고침 9 · 2 회차 일부 셋 = 고침 3 (처분 `docs/reviews/dem_redesign_direction_20261109/review/disposition3.md`).',
    '> - 3 회차 고친 판 (3 회차 지적을 고친 뒤 · 우리 판단): DRD 13 = **닫힘 12** · **일부 1** (DRD-10 그대로) · **안 닫힘 0**.  `SELF-160` · `SELF-161` = 메모 범위 닫힘 2 (원장 open).  MR3 아홉 = 고침 9 · 2 회차 일부 셋 = 고침 3 (처분 `docs/reviews/dem_redesign_direction_20261109/review/disposition3.md`).\n'
    '> - 내부 반박 리뷰 4 회차 재확인의 판정 (그 리뷰 §1 · §2 · 고친 곳만): 3 회차 지적 12 = 닫힘 11 · 일부 1 (MR3-03 → DRD-01 의 U6 (b) 촉발 · Q13) · 안 닫힘 0.  새 지적 P1 0 · P2 3 · P3 6 (MR4-01 … 09).  DRD 와의 대응은 아래 표의 "4 회차" 글 (MR4-02 · 03 · 04 · 07 · 08 · 09 → DRD-01 · MR4-01 · 04 → DRD-02 · MR4-01 · 05 → DRD-03 · MR4-06 → DRD-04 · MR4-01 → DRD-06).\n'
    '> - 이 판 (4 회차 지적을 고친 뒤 · 마지막 고침 회차 · 짧은 확인 전 · 우리 판단): DRD 13 = **닫힘 12** · **일부 1** (DRD-10 그대로) · **안 닫힘 0**.  `SELF-160` · `SELF-161` = 메모 범위 닫힘 2 (원장 open).  MR4 아홉 = 고침 9 (MR4-06 은 지시서대로 한정으로 적고 규칙 그대로) · 3 회차 일부 하나 = 고침 1 (처분 `docs/reviews/dem_redesign_direction_20261109/review/disposition4.md`).  다음 짧은 확인의 지적은 메모를 더 고치지 않고 메모 §8 "알려진 한정" 에 적어 Codex 재리뷰 (리셋 뒤) 로 넘긴다.')

# 6. row segments (column 6 = "이 판에서 더 고친 것")
segs = {
 'DRD-01': ' · **4 회차 (MR4-02 · 03 · 04 · 07 · 08 · 09)**: U6 (b) 를 두 신호로 (치우침 = 8 셀 변화가 0 과 한 항 꼴 기대 d₁ × [1.46 , 4.23] 양쪽에서 τ 넘게 떨어짐 · 메모 자신의 해상도 숫자에서 모두 꺼짐 · 참 8 셀 치우침에서 켜짐 / 잡음 = A 아닌 팔 · 부호 엇갈림 · 큰 쪽 > τ/2) · 치우침 → Q13 (사다리 한 단 올림 · 3.29 배 · (나) 0.003 → 0.40) · 잡음 → 등록된 (마) 처리 (사다리 · τ 그대로 · 원점 앙상블은 쓰지 않음) · 검정력 표를 신호와 무관하게 늘 등록 · 두 사다리와 전환 조건을 단계 0 · D-1 에 등록 · B 문장을 D-1 에 맞춤 (d₀ = 0 · 상수 팔도 B) · 반례의 끝 없음 (참 R 2.00 → 같음 · 위 끝 2.99 · 9.6 · p → 0 끝 없음 · 참 반대 → 다름 · "최악" 을 뺌) · 검정력 문구 넷 · §8 알려진 한정 · D-4⁗',
 'DRD-02': ' · **4 회차 (MR4-01 · 04)**: F 대조의 여는 순서 맨 앞에 ⓪ 2D 띠 상태 (띠 미정 이력이면 미정이던 띠 점만 한 단 올려 한 번 다시 봄 · 안 → 엶 · 밖 · 큰 변화 → "열지 않음 (F 바깥 점검 불합격)" + F 구현 조사 · 다시 미정 → 엶 + "채택 금지") · 열지 않음의 이름표 셋 (비용 · 바깥 점검 · 3D 문) · F-(i) · (ii) · (iii) 의 채택 금지 처리 · (다) 문장에 채택 금지 · (가) · (나) 꼬리 ("가정 밖이면 등급이 참값과 무관할 수 있다") · §5 Q6 바뀐 권고 · §6 42 · D-3 · D-4⁗',
 'DRD-03': ' · **4 회차 (MR4-01 · 05)**: 띠 팔 미수렴을 둘로 (큰 변화 = 판정 두 변화 가운데 하나가 띠 폭의 1/4 (3a ln σ 0.173 · 3b κ 1 Φ_d 0.015 · κ 0.2 0.020) 을 넘거나 세 단 상태가 다름 → 밖 칸 → (라) · 작은 변화 → 미정 → (마)) · 3a 한쪽 충전 (확인된 못 닿음 · 잡음) → 밖 (2 회차 판으로 되돌림 · 3 회차의 소리 없는 바꿈을 본문에 적음) · 띠 미정 이력 → 단계 4 F 대조 ⓪ · 같은 표본에서 갈림 비율 불변 · 큰 변화 0 (문턱 τ 면 (라) 0.10 · 0.97 이라 쓰지 않음) · D-2 · D-4⁗',
 'DRD-04': ' · **4 회차 (MR4-06)**: ⑤ 의 칼날이 탐색 폭 문턱 2.2 %p 로 옮겨 간 것을 한정으로 적음 (2.1 %p → 보류 · 2.3 %p → 범위 끝 값 (4-i) · 규칙 그대로 · 범위 끝 값 한정과 탐색 폭을 함께 보고 · §8)',
 'DRD-06': ' · **4 회차 (MR4-01)**: 띠 미정 이력에서 다시 보기가 다시 미정이면 "채택 금지" — F-(i) · F-(ii) 가 나와도 F 를 생산 재료로 쓰지 않고 다음 걸음은 F-보류와 같다 · F-(iii) 도 (다) 로 저절로 가지 않고 1저자 (D-3)',
}
def split_cells(line):
    # split on unescaped |
    cells, cur, i = [], '', 0
    while i < len(line):
        ch = line[i]
        if ch == '\\' and i + 1 < len(line) and line[i+1] == '|':
            cur += '\\|'; i += 2; continue
        if ch == '|':
            cells.append(cur); cur = ''; i += 1; continue
        cur += ch; i += 1
    cells.append(cur)
    return cells
lines = s.split('\n')
done = set()
for k, line in enumerate(lines):
    for key, seg in segs.items():
        if line.startswith('| ' + key + ' |'):
            cells = split_cells(line)
            # cells[0]='' , [1]=#, [2]=등급, [3]=지적, [4]=초안 처분, [5]=리뷰판정, [6]=더 고친 것, [7]=지금 처분, [8]=''
            assert len(cells) == 9, (key, len(cells))
            c6 = cells[6].rstrip()
            cells[6] = c6 + seg + ' '
            if key == 'DRD-04':
                assert cells[7].strip() == '**닫힘**', cells[7]
                cells[7] = ' **닫힘** (⑤ 의 폭 문턱 칼날은 한정 · 4 회차 MR4-06) '
            lines[k] = '|'.join(cells)
            done.add(key)
assert done == set(segs), done
s = '\n'.join(lines)
open(p, 'w', encoding='utf-8').write(s)
print('ok', sorted(done))
