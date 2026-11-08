#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RR3-01 시험 먼저 — scripts/test_rint_r_chain.py 에 (1) 정직 고정물 = 생산자 성공 꼴 (ct06_pub · CT06_PUB) (2) CT06 · PC12C 의 정직한 앞 런 고정물 바꿈
(옛 CT06_ARM = 판독 실패 꼴 {file · index · sha256}) (3) 새 시험 블록 RR3A–E · RR3P (rr3_tests_block.txt) 를 넣는다.  바꿈마다 옛 글이 정확히 한 번 있어야
한다 (아니면 아무것도 쓰지 않고 멈춤) · 원자적 쓰기.

  python3 docs/reviews/rint2_rr2_fix_evidence_20261105/rr3_fix/apply_tests.py <리포 뿌리>
"""
import os
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
T = ROOT / 'scripts' / 'test_rint_r_chain.py'
BLOCK = Path(__file__).resolve().parent / 'rr3_tests_block.txt'

PUB_DEF = '''CT06_ARM = [{'file': 'p2_SBE_vgcf100_a0.json', 'index': 0, 'sha256': 'a' * 64}]


#: ★ 11-08 RR3-01 (Codex 회차 ③ · 수정 계획 Q1 (가)) — 판독 완료 팔 기록 = 생산자 성공 꼴 (`arms_read_record` = `ARM_PUBLIC` 칸 정확히 · 요청 팔 차례) · 값 = 시험 값
#:   (σ 아님) · 칸 이름 = 글자로 (RR3C 가 사슬 ARM_PUBLIC 과 대조 · 사본 금지의 짝).  정직한 앞 런 고정물 = 이 꼴 (옛 CT06_ARM = 칸 셋 {file · index · sha256} =
#:   생산자의 판독 실패 꼴 `arm_file_shas` 라 이제 끝난 런이 아니다 — 멈춘 런 기록에 팔 읽음을 넣은 행 (f_*_arms · CT06_ARMS) 은 그대로 둔다).
def ct06_pub(i=0, kit=SBE_KIT):
    return {'file': f'p2_{kit[len("kit_"):]}_sph_fa_cj0_c0_a{i}.json', 'index': i, 'sha256': hashlib.sha256(f'{kit}|{i}'.encode()).hexdigest(),
            'protocol_id': 'p3ca-test', 'state': 'positive', 'cg_info': 0, 'cg_resid': 1e-12, 'imbalance': 1e-9, 'cert_pass': [True, True, True, True],
            'sid_fp': 'f' * 16, 'cg_iters': 10, 'resolve_iters': 2, 'sv_cf_status': None, 'err_rel': 1e-6}


CT06_PUB = [ct06_pub(0)]
'''

EDITS = [
    ("CT06_ARM = [{'file': 'p2_SBE_vgcf100_a0.json', 'index': 0, 'sha256': 'a' * 64}]\n", PUB_DEF),
    ("    ('c_prev_record', 'TIME_LIMIT', [ct06_rec('L00_prev', group_cause=None, rc=0, arms_read=CT06_ARM), ct06_rec(**TL0)], 'plain', LG_RUN, None, (),\n",
     "    ('c_prev_record', 'TIME_LIMIT', [ct06_rec('L00_prev', group_cause=None, rc=0, arms=1, arm_list=None, kit=SBE_KIT, arms_read=CT06_PUB), ct06_rec(**TL0)],\n"
     "     'plain', LG_RUN, None, (),\n"),
    ("    OK0 = R(group_cause=None, rc=0, arms=1, arm_list=None, arms_read=CT06_ARM)          # 끝난 런 (팔 읽음)\n",
     "    OK0 = R(group_cause=None, rc=0, arms=1, arm_list=None, kit=SBE_KIT, arms_read=CT06_PUB)   # 끝난 런 (팔 읽음 · ★ 11-08 RR3-01 = 생산자 성공 꼴)\n"),
    ("    add('rr_after_copied', 'RUNNER_RC', [R(group_cause=None, rc=0, arms=1, arm_list=None, arms_read=CT06_ARM, copied_from=1),\n",
     "    add('rr_after_copied', 'RUNNER_RC', [R(group_cause=None, rc=0, arms=1, arm_list=None, kit=SBE_KIT, arms_read=CT06_PUB, copied_from=1),\n"),
    ("    add('rr_after_prior_no_gc', 'RUNNER_RC', [R(rc=0, arms=1, arm_list=None, arms_read=CT06_ARM),\n",
     "    add('rr_after_prior_no_gc', 'RUNNER_RC', [R(rc=0, arms=1, arm_list=None, kit=SBE_KIT, arms_read=CT06_PUB),\n"),
    ("                '(앞 런 끝남 · 첫 런 전 · 재실행 복사 기록 · GU · signal 뒤 런) = 그대로 · 실경로 (실제 git 원장 · 탐침 p4 둘 = RESUME_NOT_ALLOWED · 정직 런 전 TIME_LIMIT = 자격)')\n",
     "                '(앞 런 끝남 · 첫 런 전 · 재실행 복사 기록 · GU · signal 뒤 런) = 그대로 · 실경로 (실제 git 원장 · 탐침 p4 둘 = RESUME_NOT_ALLOWED · 정직 런 전 TIME_LIMIT = 자격) · '\n"
     "                '★ 11-08 RR3-01 — \"비지 않은 목록\" → 판독 완료 꼴 (`arms_read_kind` verified · RR3A–E · RR3P) · 정직 앞 런 고정물 = 생산자 성공 꼴 (CT06_PUB · 옛 CT06_ARM = '\n"
     "                '판독 실패 꼴 {file · index · sha256})')\n"),
    ('# ═════════════════════════ 실행 ═════════════════════════\n', None),     # 앞에 새 블록
]


def main():
    src = T.read_text(encoding='utf-8')
    block = BLOCK.read_text(encoding='utf-8')
    for old, new in EDITS:
        n = src.count(old)
        if n != 1:
            print(f'STOP — 옛 글이 {n} 번 (정확히 한 번이어야): {old[:90]!r}')
            return 2
        src = src.replace(old, (block + old) if new is None else new)
    tmp = T.with_name(T.name + '.tmp_rr3')
    tmp.write_text(src, encoding='utf-8')
    os.replace(tmp, T)
    print(f'바꿈 {len(EDITS)} (새 블록 {block.count(chr(10))} 줄) → {T}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
