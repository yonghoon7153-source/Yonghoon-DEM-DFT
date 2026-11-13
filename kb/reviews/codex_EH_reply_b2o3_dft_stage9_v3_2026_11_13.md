---
title: "EH 회신 — b2o3 9 단계 DFT 도구 v3: NO-GO (P1 2 · P2 2) · EG 여섯 반례 닫힘 확인 · 유한하지 않은 힘·좌표 승격 · 압력 토큰 앞부분 판독 · BFGS 판독 실패 시 대조 건너뜀 + 판정 저장 뒤 CLI 오류 · 응력 행렬 본문 미검사 · 블록 문법 ≠ 같은 실행 인증 · 판 문자열 ≠ 바이너리 동일성 · DY 확인 4 아직 해제 못 함"
date: 2026-11-13
updated: 2026-11-13
tags: [review, b2o3, dft, qe, eos, kprobe, readout, codex, reply, letter]
letter: EH
track: b2o3
channel: codex
kind: reply
status: 수령 2026-11-13 (사용자 붙여넣기) · NO-GO · 기준 f6b9d3a6 (도구 sha256 f6105cfc · 실행기 e2d6f728 · 변이 도구 760a0fb1) · 고침 → 다음 편지 EI
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> 원문 그대로 보존 (사용자 붙여넣기 2026-11-13). 링크의 C:/ 경로는 Codex 쪽 작업 폴더다 (저장소 밖).

NO-GO — EG의 여섯 반례는 막혔지만, 추가로 재현된 P1 두 묶음·P2 두 건이 남았습니다.

기준 커밋 f6b9d3a6의 도구·실행기·변이 도구와 고정 판독기 지문을 확인했습니다. selftest 142/142, 실행기 24/24, 변이 87/87 빨강을 재현했습니다.

추가 검증은 합성 출력·8단계 시험 자료와 기존 QE 실측 출력의 변형으로 수행했습니다. 생산 UMA·QE·MD는 실행하지 않았습니다. gabia의 실제 궤적 재판독과 실측 출력 217개 전수 검사는 이번에 독립 재현하지 않았습니다.

P1-1 — 유한하지 않은 힘·좌표가 후속 대상으로 승격됩니다.

위치: [b2o3_bo_dft.py (line 508)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EG_v3_20261113/source/tools/doping/b2o3_bo_dft.py:508), 같은 파일 497·692·1236행.

블록 개수·순서·원자 번호를 유지하고 다음을 각각 적용했습니다.
- 마지막 힘 블록의 원자 1, 첫 성분을 NaN으로 변경.
- 최종 좌표의 Li 하나를 NaN 또는 Inf로 변경.
모두 out_problems=[]였고, read_relax가 정상 반환하면서 skip_eos=true, 10단계 대상, 전자구조 대상 3개를 생성했습니다. 힘 Inf는 막히지만 NaN은 fm > threshold가 거짓이 되어 빠져나갑니다. 좌표도 float() 변환 성공을 유효성으로 받아들입니다.

최소 수정: 힘 배열과 최종 좌표 전체에 유한성 검사를 적용하고, 구조 파일·판정·대상을 쓰기 전에 거부하세요. 유효한 구조의 골격 변화는 G7처럼 기록만 해도 되지만, 숫자로 정의되지 않은 구조는 별개입니다. JSON 저장의 allow_nan=False도 방어선으로 추가할 수 있습니다.

P1-2 — 압력 숫자의 앞부분만 읽어 EOS 보류가 풀립니다.

위치: [b2o3_bo_dft.py (line 480)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EG_v3_20261113/source/tools/doping/b2o3_bo_dft.py:480).

세 가족 모두 P=25.00 kbar, 즉 2.5 GPa인 정상 시험 출력에서는 EOS가 보류됩니다. 마지막 압력 토큰만 바꾸면 다음처럼 됩니다.
압력 토큰	판독 결과	후속 결과
2.50E+01	2.5 kbar	EOS 생략·대상 생성
0.00BROKEN	0 kbar	EOS 생략·대상 생성
0.00 뒤 NUL	0 kbar	EOS 생략·대상 생성


블록 개수와 순서는 그대로입니다. 지수 표기를 지원할 의무는 없지만, 지원하지 않는 토큰을 다른 숫자로 읽으면 안 됩니다.

최소 수정: 압력 헤더의 값 전체를 검사하세요. 허용한 표기라면 끝까지 변환하고, 나머지는 거부해야 합니다. 이 반례는 파서 반환값뿐 아니라 보류 대상이 계속 null인지까지 시험해야 합니다.

P2-1 — BFGS 횟수를 못 읽으면 대조를 건너뛰고, 판정 저장 뒤 CLI가 터집니다.

위치: [b2o3_bo_dft.py (line 694)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EG_v3_20261113/source/tools/doping/b2o3_bo_dft.py:694), 같은 파일 482·1273·2279행.

bfgs converged in 2 scf cycles …의 2를 ???로 바꾸면 표지는 남지만 bfgs=None이 됩니다. 현재 if o["bfgs"] and …는 SCF 횟수 대조를 생략합니다.

재현 결과:
- 판독 함수는 정상 반환.
- EOS 생략·후속 대상이 담긴 판정 JSON 저장.
- 그 뒤 CLI 화면 출력에서 None['steps']로 TypeError.
따라서 명령의 비정상 종료만으로 안전하게 거부됐다고 볼 수 없습니다. 사용 가능한 모양의 판정 파일이 이미 남습니다.

최소 수정: 읽을 수 있는 BFGS 기록을 필수로 요구한 뒤 SCF 횟수를 대조하세요. v2의 명시적인 bfgs is None 거부가 표지 개수 검사로 완전히 대체되지는 않았습니다.

P2-2 — 응력 블록은 헤더만 검사하고 행렬 본문은 검사하지 않습니다.

위치: [b2o3_bo_dft.py (line 480)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EG_v3_20261113/source/tools/doping/b2o3_bo_dft.py:480), 같은 파일 526·1353행.

실측 MLi_04_x108 원문으로 다음을 확인했습니다.
- 마지막 응력 행렬 세 행을 전부 삭제해도 상태 문법·출력 검사가 통과.
- 행렬은 그대로 두고 헤더의 P=-10.88만 P=0.00으로 바꿔도 통과.
원래 행렬의 kbar 대각합/3은 정확히 −10.88입니다. QE 7.4.1도 압력과 행렬을 같은 sigma에서 함께 출력합니다. 이는 출력 내부에서 대조 가능한 관계입니다. QE 7.4.1 출력 구현

최소 수정: 마지막 응력 블록의 3행×6개 값과 유한성을 확인하고, 헤더 압력과 kbar 행렬의 대각합/3을 출력 반올림 정밀도에 맞춰 대조하세요. 현재 양성 fixture인 _frag_stress()도 행렬을 한 행만 만들므로 함께 고쳐야 합니다.

이 항목은 위조 방지 요구가 아니라 빠진 본문·내부적으로 모순된 조각을 잡는 검사입니다.

Q1 — EG 여섯 항목은 닫혔나?

기존에 제시했던 반례 기준으로는 모두 닫혔습니다.
EG 항목	이번 확인
P1-1 상태 결속	추가 압력·힘·좌표 조각, 원자 번호 손상 등을 거부
P1-2 reject 대상	변조한 잡 목록을 이동 전에 거부
P2-1 G5 캐시	계획의 순서를 바꾸면 재판독 대조에서 거부
P2-2 GPU 조회 종료코드	숫자·빈 목록을 출력하고 exit 9인 조회를 거부
P2-3 nvidia-smi 없음 시험	해당 이유로 거부하며, 존재 검사를 끈 변이가 해당 시험에서 실패
P2-4 판 혼합 복구	7.3.1 출력만 실패 처리하고 보존 이동


다만 P1-1의 기존 반례 해제와 출력 내용 전체의 유효성 확보는 구분해야 합니다. 위 네 건이 그 잔여 부분입니다.

Q2 — 개수·순서가 같은 내용 교체는 어디까지 잡아야 하나?

위에서 재현한 비유한 값, 숫자 일부 판독, 읽을 수 없는 BFGS 기록, 불완전·모순된 응력 본문은 잡아야 합니다.

반면 형식과 내부 관계까지 일관된 다른 계산의 완전한 블록이나 중간 SCF 묶음을 바꿔 넣는 경우는 현재 검사로 출처를 인증할 수 없습니다. 판정 때 기록한 SHA도 “이 바이트를 읽었다”는 증거이지, 생성 당시 원본이라는 증거는 아닙니다.

선언한 비위조 방지 범위에서는 이 한계를 명시하면 됩니다. 블록 문법 통과를 “실제로 같은 실행에서 생성된 상태임을 인증했다”로 표현하지 마세요.

Q3 — reject의 앞 단계 검증은 순환인가?

아닙니다. 유효한 앞 단계에서 현재 단계의 허용 잡 목록을 복원하고, 그 목록 안에서 현재의 실패 출력을 검사하는 방향입니다.

현재 k 탐침·이완 출력 하나의 QE 버전을 틀리게 만든 양성 복구 시험에서도, 해당 출력만 보존 이동되고 바이트가 유지됐습니다. 앞 단계 자체가 깨졌다면 그 단계부터 복구하는 순서가 맞습니다.

Q4 — QE 7.4.1 고정으로 판 혼합 복구를 닫아도 되나?

찬성입니다. 계약이 허용 판을 정하므로 개별 실패 출력을 객관적으로 고를 수 있고, 실제 복구도 됩니다. 다만 버전 문자열 확인을 실행 바이너리·빌드 전체의 동일성 인증으로 확대하지 않으면 됩니다.

Q5 — DY 확인 4, EOS 입력 결속을 해제할 수 있나?

아직 안 됩니다. 출력 파일 SHA에 (E, P, V)를 연결하는 사슬은 있지만, P1-2처럼 그 파일의 압력을 잘못 읽어 EOS 보류를 해제할 수 있습니다. 파일 결속과 값 판독 유효성이 함께 충족돼야 합니다.

Q6 — 사용자 비준만 남았나?

아닙니다. 위 네 수정과 재검증이 먼저입니다. 수정 범위는 판독기·시험·그에 대응하는 카드 문구입니다. 이번 검토에서 추가 생산 계산이나 새로운 물리 문턱은 요구하지 않습니다.

DFT 진입 전 마지막 확인 목록은 다음과 같습니다.
1. 비유한 힘·좌표, 압력 토큰 손상, BFGS 판독 실패, 응력 본문 손상을 저장·대상 생성 전에 거부.
2. 음성시험에서 거부 이유와 함께 성공 판정 파일·실행 대상이 새로 남지 않는 것을 확인.
3. 정상 연결 경로, EOS 보류 시 대상 null, 실패 출력 보존·재실행 경로를 유지.
4. 수정 코드·카드·시험 지문을 고정하고 재검토한 뒤, 사용자가 개정 5를 비준.
5. 승인된 판으로 실행 직전 입력·환경·GPU 운영 조건 확인.
재현 자료: [값 판독 시험](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EG_v3_20261113/value_results.json), [BFGS CLI 시험](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EG_v3_20261113/bfgs_cli_results.json), [실측 응력 본문 시험](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EG_v3_20261113/stress_body_results.json).{
  "source_sha256": "f6105cfc2ae933eaf321472d232bca47d4512198a3d68c66a62b0b1804c6ab2e",
  "force_nan": {
    "fields": [
      {
        "family": "F_B",
        "problems": [],
        "P_kbar": 0.0,
        "force": NaN,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": true
      },
      {
        "family": "F_P",
        "problems": [],
        "P_kbar": 0.0,
        "force": NaN,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": true
      },
      {
        "family": "F_free",
        "problems": [],
        "P_kbar": 0.0,
        "force": NaN,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": true
      }
    ],
    "read_relax": {
      "accepted": true,
      "value": {
        "skip_eos": true,
        "eos_input": {
          "F_B": {
            "E_eV": -110.00000001844798,
            "P_GPa": 0.0,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_FB_cfg0003\\scf.out",
              "sha256": "2b4d7ed0d7f4f3165d1f02651b57b88bd2559fee480577050c0c4a480c7ced19"
            }
          },
          "F_P": {
            "E_eV": -105.99999998314448,
            "P_GPa": 0.0,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_FP_cfg0004\\scf.out",
              "sha256": "8e3f75ffae665f1ca3810886c5d00af81149fe7d681a0ae2f83c85d4ef0c5263"
            }
          },
          "F_free": {
            "E_eV": -101.99999994784096,
            "P_GPa": 0.0,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_Ffree_cfg0005\\scf.out",
              "sha256": "d46cdc4417db285697be59007cacc41c7d41614e02727f94ec201fca71a0fb2d"
            }
          }
        },
        "stage10": true,
        "electronic_targets": [
          {
            "family": "F_B",
            "rel": "relaxed\\rx_FB_cfg0003.xyz",
            "sha256": "eda6c32a80045b6f7673519271306c31c815d6d9b5d20f6cc2ca3e963392b540",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0003_E-0.000_O-bo4\\post_relax.xyz",
              "sha256": "29be7546b4cffb0eb5c228bbe6f931462288c629b8e5f09fed3852b7a79eb82b"
            }
          },
          {
            "family": "F_P",
            "rel": "relaxed\\rx_FP_cfg0004.xyz",
            "sha256": "b225c25c95e2df97ce33a8bb4c62f44a190cee7c76ae6d69686db36e0e92b5fc",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0004_E-0.000_O-distributed\\post_relax.xyz",
              "sha256": "a8db764164363c341fe3a81219217466e5a836bc51a056f9373d3879f00e9cf8"
            }
          },
          {
            "family": "F_free",
            "rel": "relaxed\\rx_Ffree_cfg0005.xyz",
            "sha256": "896302cc0b8fad4622cf57517a38da0ec01846452de89570a48d6f22a314fa3d",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0005_E-0.000_O-free_s\\post_relax.xyz",
              "sha256": "8b6ded853ebd5c2b3cc07bbeb1728f639967a95d66dd6fa49c4517953cacb054"
            }
          }
        ],
        "relaxed": {
          "F_B": {
            "job": "rx_FB_cfg0003",
            "file": {
              "rel": "relaxed\\rx_FB_cfg0003.xyz",
              "sha256": "eda6c32a80045b6f7673519271306c31c815d6d9b5d20f6cc2ca3e963392b540"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0003_E-0.000_O-bo4\\post_relax.xyz",
              "sha256": "29be7546b4cffb0eb5c228bbe6f931462288c629b8e5f09fed3852b7a79eb82b"
            },
            "parent_sp_job": "sp_FB_1_cfg0003",
            "record": {
              "end_motif": "unclassified",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          },
          "F_P": {
            "job": "rx_FP_cfg0004",
            "file": {
              "rel": "relaxed\\rx_FP_cfg0004.xyz",
              "sha256": "b225c25c95e2df97ce33a8bb4c62f44a190cee7c76ae6d69686db36e0e92b5fc"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0004_E-0.000_O-distributed\\post_relax.xyz",
              "sha256": "a8db764164363c341fe3a81219217466e5a836bc51a056f9373d3879f00e9cf8"
            },
            "parent_sp_job": "sp_FP_1_cfg0004",
            "record": {
              "end_motif": "unclassified",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          },
          "F_free": {
            "job": "rx_Ffree_cfg0005",
            "file": {
              "rel": "relaxed\\rx_Ffree_cfg0005.xyz",
              "sha256": "896302cc0b8fad4622cf57517a38da0ec01846452de89570a48d6f22a314fa3d"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0005_E-0.000_O-free_s\\post_relax.xyz",
              "sha256": "8b6ded853ebd5c2b3cc07bbeb1728f639967a95d66dd6fa49c4517953cacb054"
            },
            "parent_sp_job": "sp_Ffree_1_cfg0005",
            "record": {
              "end_motif": "unclassified",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          }
        }
      }
    }
  },
  "force_inf": {
    "fields": [
      {
        "family": "F_B",
        "problems": [
          "마지막 힘 성분 최대 inf Ry/Bohr > forc_conv_thr 0.001 (모든 성분 기준)"
        ],
        "P_kbar": 0.0,
        "force": Infinity,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": true
      },
      {
        "family": "F_P",
        "problems": [
          "마지막 힘 성분 최대 inf Ry/Bohr > forc_conv_thr 0.001 (모든 성분 기준)"
        ],
        "P_kbar": 0.0,
        "force": Infinity,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": true
      },
      {
        "family": "F_free",
        "problems": [
          "마지막 힘 성분 최대 inf Ry/Bohr > forc_conv_thr 0.001 (모든 성분 기준)"
        ],
        "P_kbar": 0.0,
        "force": Infinity,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": true
      }
    ],
    "read_relax": {
      "accepted": false,
      "error": "SystemExit: ⛔ relax 출력 결속 · 검사 실패 3 건 — 판독하지 않는다:\n  rx_FB_cfg0003: 마지막 힘 성분 최대 inf Ry/Bohr > forc_conv_thr 0.001 (모든 성분 기준)\n  rx_FP_cfg0004: 마지막 힘 성분 최대 inf Ry/Bohr > forc_conv_thr 0.001 (모든 성분 기준)\n  rx_Ffree_cfg0005: 마지막 힘 성분 최대 inf Ry/Bohr > forc_conv_thr 0.001 (모든 성분 기준)\n  → 실패 출력을 보존해 옮긴 뒤 (b2o3_bo_dft.py reject … --stage relax) 같은 실행기로 다시 돌린다"
    }
  },
  "final_coord_nan": {
    "fields": [
      {
        "family": "F_B",
        "problems": [],
        "P_kbar": 0.0,
        "force": 0.0003,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": false
      },
      {
        "family": "F_P",
        "problems": [],
        "P_kbar": 0.0,
        "force": 0.0003,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": false
      },
      {
        "family": "F_free",
        "problems": [],
        "P_kbar": 0.0,
        "force": 0.0003,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": false
      }
    ],
    "read_relax": {
      "accepted": true,
      "value": {
        "skip_eos": true,
        "eos_input": {
          "F_B": {
            "E_eV": -110.00000001844798,
            "P_GPa": 0.0,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_FB_cfg0003\\scf.out",
              "sha256": "35b6b03c754d59d48abfc8202decf7e8b2a494d83e9997cf8e4d4b431c7e0f3a"
            }
          },
          "F_P": {
            "E_eV": -105.99999998314448,
            "P_GPa": 0.0,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_FP_cfg0004\\scf.out",
              "sha256": "f01af7f038b5dd5a0872ccf9b2bf84cc9d25d3879f5aa90d5d260b3eadb73cd0"
            }
          },
          "F_free": {
            "E_eV": -101.99999994784096,
            "P_GPa": 0.0,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_Ffree_cfg0005\\scf.out",
              "sha256": "0a0b71a34868ca9fbc467648058b38dad061f2d8ecf32c4da036ab3c6eb262aa"
            }
          }
        },
        "stage10": true,
        "electronic_targets": [
          {
            "family": "F_B",
            "rel": "relaxed\\rx_FB_cfg0003.xyz",
            "sha256": "2109723bc36acd3c6503cf71cb0f7b240ce69c713aa3d8262b37258be735e740",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0003_E-0.000_O-bo4\\post_relax.xyz",
              "sha256": "29be7546b4cffb0eb5c228bbe6f931462288c629b8e5f09fed3852b7a79eb82b"
            }
          },
          {
            "family": "F_P",
            "rel": "relaxed\\rx_FP_cfg0004.xyz",
            "sha256": "6a76728ea4efe9f126072cbb22d0e4cfafca99cb71c8250bab02acf2a2b40ab0",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0004_E-0.000_O-distributed\\post_relax.xyz",
              "sha256": "a8db764164363c341fe3a81219217466e5a836bc51a056f9373d3879f00e9cf8"
            }
          },
          {
            "family": "F_free",
            "rel": "relaxed\\rx_Ffree_cfg0005.xyz",
            "sha256": "65a62ff36120fa1965987308fa3056202836a7df9ecca5f3ce388ab67fec335e",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0005_E-0.000_O-free_s\\post_relax.xyz",
              "sha256": "8b6ded853ebd5c2b3cc07bbeb1728f639967a95d66dd6fa49c4517953cacb054"
            }
          }
        ],
        "relaxed": {
          "F_B": {
            "job": "rx_FB_cfg0003",
            "file": {
              "rel": "relaxed\\rx_FB_cfg0003.xyz",
              "sha256": "2109723bc36acd3c6503cf71cb0f7b240ce69c713aa3d8262b37258be735e740"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0003_E-0.000_O-bo4\\post_relax.xyz",
              "sha256": "29be7546b4cffb0eb5c228bbe6f931462288c629b8e5f09fed3852b7a79eb82b"
            },
            "parent_sp_job": "sp_FB_1_cfg0003",
            "record": {
              "end_motif": "invalid",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          },
          "F_P": {
            "job": "rx_FP_cfg0004",
            "file": {
              "rel": "relaxed\\rx_FP_cfg0004.xyz",
              "sha256": "6a76728ea4efe9f126072cbb22d0e4cfafca99cb71c8250bab02acf2a2b40ab0"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0004_E-0.000_O-distributed\\post_relax.xyz",
              "sha256": "a8db764164363c341fe3a81219217466e5a836bc51a056f9373d3879f00e9cf8"
            },
            "parent_sp_job": "sp_FP_1_cfg0004",
            "record": {
              "end_motif": "invalid",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          },
          "F_free": {
            "job": "rx_Ffree_cfg0005",
            "file": {
              "rel": "relaxed\\rx_Ffree_cfg0005.xyz",
              "sha256": "65a62ff36120fa1965987308fa3056202836a7df9ecca5f3ce388ab67fec335e"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0005_E-0.000_O-free_s\\post_relax.xyz",
              "sha256": "8b6ded853ebd5c2b3cc07bbeb1728f639967a95d66dd6fa49c4517953cacb054"
            },
            "parent_sp_job": "sp_Ffree_1_cfg0005",
            "record": {
              "end_motif": "invalid",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          }
        }
      }
    }
  },
  "final_coord_inf": {
    "fields": [
      {
        "family": "F_B",
        "problems": [],
        "P_kbar": 0.0,
        "force": 0.0003,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": false
      },
      {
        "family": "F_P",
        "problems": [],
        "P_kbar": 0.0,
        "force": 0.0003,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": false
      },
      {
        "family": "F_free",
        "problems": [],
        "P_kbar": 0.0,
        "force": 0.0003,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": false
      }
    ],
    "read_relax": {
      "accepted": true,
      "value": {
        "skip_eos": true,
        "eos_input": {
          "F_B": {
            "E_eV": -110.00000001844798,
            "P_GPa": 0.0,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_FB_cfg0003\\scf.out",
              "sha256": "3fdd62f51d08a820d8a535132f5181e166bc028e0f738b2e75294b544e2565b9"
            }
          },
          "F_P": {
            "E_eV": -105.99999998314448,
            "P_GPa": 0.0,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_FP_cfg0004\\scf.out",
              "sha256": "ea99cd96b3e3aa43a1ce9dee1f85908df89edd25f79e7f052a6dc267f6ca1f57"
            }
          },
          "F_free": {
            "E_eV": -101.99999994784096,
            "P_GPa": 0.0,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_Ffree_cfg0005\\scf.out",
              "sha256": "48cba2dcf36f38c098764519302f3e0eb0c9cbd3359780a098ec72e22c41d3bf"
            }
          }
        },
        "stage10": true,
        "electronic_targets": [
          {
            "family": "F_B",
            "rel": "relaxed\\rx_FB_cfg0003.xyz",
            "sha256": "327eeb48739f8d1c1119d5e441c8be1d77bbf11219d940f2de9222726b53ba3a",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0003_E-0.000_O-bo4\\post_relax.xyz",
              "sha256": "29be7546b4cffb0eb5c228bbe6f931462288c629b8e5f09fed3852b7a79eb82b"
            }
          },
          {
            "family": "F_P",
            "rel": "relaxed\\rx_FP_cfg0004.xyz",
            "sha256": "b51818f5f48816b110772a914eba022a232cf632ea3ec1933a480af408ebf428",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0004_E-0.000_O-distributed\\post_relax.xyz",
              "sha256": "a8db764164363c341fe3a81219217466e5a836bc51a056f9373d3879f00e9cf8"
            }
          },
          {
            "family": "F_free",
            "rel": "relaxed\\rx_Ffree_cfg0005.xyz",
            "sha256": "4053715d2cad97e1c5f841f56df20ff25059607fe708ee3cf34e272911e5b16f",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0005_E-0.000_O-free_s\\post_relax.xyz",
              "sha256": "8b6ded853ebd5c2b3cc07bbeb1728f639967a95d66dd6fa49c4517953cacb054"
            }
          }
        ],
        "relaxed": {
          "F_B": {
            "job": "rx_FB_cfg0003",
            "file": {
              "rel": "relaxed\\rx_FB_cfg0003.xyz",
              "sha256": "327eeb48739f8d1c1119d5e441c8be1d77bbf11219d940f2de9222726b53ba3a"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0003_E-0.000_O-bo4\\post_relax.xyz",
              "sha256": "29be7546b4cffb0eb5c228bbe6f931462288c629b8e5f09fed3852b7a79eb82b"
            },
            "parent_sp_job": "sp_FB_1_cfg0003",
            "record": {
              "end_motif": "invalid",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          },
          "F_P": {
            "job": "rx_FP_cfg0004",
            "file": {
              "rel": "relaxed\\rx_FP_cfg0004.xyz",
              "sha256": "b51818f5f48816b110772a914eba022a232cf632ea3ec1933a480af408ebf428"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0004_E-0.000_O-distributed\\post_relax.xyz",
              "sha256": "a8db764164363c341fe3a81219217466e5a836bc51a056f9373d3879f00e9cf8"
            },
            "parent_sp_job": "sp_FP_1_cfg0004",
            "record": {
              "end_motif": "invalid",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          },
          "F_free": {
            "job": "rx_Ffree_cfg0005",
            "file": {
              "rel": "relaxed\\rx_Ffree_cfg0005.xyz",
              "sha256": "4053715d2cad97e1c5f841f56df20ff25059607fe708ee3cf34e272911e5b16f"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0005_E-0.000_O-free_s\\post_relax.xyz",
              "sha256": "8b6ded853ebd5c2b3cc07bbeb1728f639967a95d66dd6fa49c4517953cacb054"
            },
            "parent_sp_job": "sp_Ffree_1_cfg0005",
            "record": {
              "end_motif": "invalid",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          }
        }
      }
    }
  },
  "bfgs_unreadable": {
    "fields": [
      {
        "family": "F_B",
        "problems": [],
        "P_kbar": 0.0,
        "force": 0.0003,
        "bfgs": null,
        "final_xyz_finite": true
      },
      {
        "family": "F_P",
        "problems": [],
        "P_kbar": 0.0,
        "force": 0.0003,
        "bfgs": null,
        "final_xyz_finite": true
      },
      {
        "family": "F_free",
        "problems": [],
        "P_kbar": 0.0,
        "force": 0.0003,
        "bfgs": null,
        "final_xyz_finite": true
      }
    ],
    "read_relax": {
      "accepted": true,
      "value": {
        "skip_eos": true,
        "eos_input": {
          "F_B": {
            "E_eV": -110.00000001844798,
            "P_GPa": 0.0,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_FB_cfg0003\\scf.out",
              "sha256": "21baf6f97094d936b969de478f9f8b093683a62bd537f78a4b68248a28e65160"
            }
          },
          "F_P": {
            "E_eV": -105.99999998314448,
            "P_GPa": 0.0,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_FP_cfg0004\\scf.out",
              "sha256": "4ed83572b9ef634dc7d2339fea67b0f8afd61529664a324c585e9c6d093170ca"
            }
          },
          "F_free": {
            "E_eV": -101.99999994784096,
            "P_GPa": 0.0,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_Ffree_cfg0005\\scf.out",
              "sha256": "36c0df5d2f7087d3d44fee93fd6ce68b13a06e6bfcdf912697cf175cfee32d00"
            }
          }
        },
        "stage10": true,
        "electronic_targets": [
          {
            "family": "F_B",
            "rel": "relaxed\\rx_FB_cfg0003.xyz",
            "sha256": "eda6c32a80045b6f7673519271306c31c815d6d9b5d20f6cc2ca3e963392b540",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0003_E-0.000_O-bo4\\post_relax.xyz",
              "sha256": "29be7546b4cffb0eb5c228bbe6f931462288c629b8e5f09fed3852b7a79eb82b"
            }
          },
          {
            "family": "F_P",
            "rel": "relaxed\\rx_FP_cfg0004.xyz",
            "sha256": "b225c25c95e2df97ce33a8bb4c62f44a190cee7c76ae6d69686db36e0e92b5fc",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0004_E-0.000_O-distributed\\post_relax.xyz",
              "sha256": "a8db764164363c341fe3a81219217466e5a836bc51a056f9373d3879f00e9cf8"
            }
          },
          {
            "family": "F_free",
            "rel": "relaxed\\rx_Ffree_cfg0005.xyz",
            "sha256": "896302cc0b8fad4622cf57517a38da0ec01846452de89570a48d6f22a314fa3d",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0005_E-0.000_O-free_s\\post_relax.xyz",
              "sha256": "8b6ded853ebd5c2b3cc07bbeb1728f639967a95d66dd6fa49c4517953cacb054"
            }
          }
        ],
        "relaxed": {
          "F_B": {
            "job": "rx_FB_cfg0003",
            "file": {
              "rel": "relaxed\\rx_FB_cfg0003.xyz",
              "sha256": "eda6c32a80045b6f7673519271306c31c815d6d9b5d20f6cc2ca3e963392b540"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0003_E-0.000_O-bo4\\post_relax.xyz",
              "sha256": "29be7546b4cffb0eb5c228bbe6f931462288c629b8e5f09fed3852b7a79eb82b"
            },
            "parent_sp_job": "sp_FB_1_cfg0003",
            "record": {
              "end_motif": "unclassified",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          },
          "F_P": {
            "job": "rx_FP_cfg0004",
            "file": {
              "rel": "relaxed\\rx_FP_cfg0004.xyz",
              "sha256": "b225c25c95e2df97ce33a8bb4c62f44a190cee7c76ae6d69686db36e0e92b5fc"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0004_E-0.000_O-distributed\\post_relax.xyz",
              "sha256": "a8db764164363c341fe3a81219217466e5a836bc51a056f9373d3879f00e9cf8"
            },
            "parent_sp_job": "sp_FP_1_cfg0004",
            "record": {
              "end_motif": "unclassified",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          },
          "F_free": {
            "job": "rx_Ffree_cfg0005",
            "file": {
              "rel": "relaxed\\rx_Ffree_cfg0005.xyz",
              "sha256": "896302cc0b8fad4622cf57517a38da0ec01846452de89570a48d6f22a314fa3d"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0005_E-0.000_O-free_s\\post_relax.xyz",
              "sha256": "8b6ded853ebd5c2b3cc07bbeb1728f639967a95d66dd6fa49c4517953cacb054"
            },
            "parent_sp_job": "sp_Ffree_1_cfg0005",
            "record": {
              "end_motif": "unclassified",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          }
        }
      }
    }
  },
  "pressure_suffix_junk_baseline": {
    "accepted": true,
    "value": {
      "skip_eos": false,
      "eos_input": {
        "F_B": {
          "E_eV": -110.00000001844798,
          "P_GPa": 2.5,
          "V_A3": 2436.330003077836,
          "output": {
            "rel": "relax\\rx_FB_cfg0003\\scf.out",
            "sha256": "d4e12448e41049589b762922b98ecf70d5c33fd7148c37dcbb429e3788ea3b69"
          }
        },
        "F_P": {
          "E_eV": -105.99999998314448,
          "P_GPa": 2.5,
          "V_A3": 2436.330003077836,
          "output": {
            "rel": "relax\\rx_FP_cfg0004\\scf.out",
            "sha256": "54a21c65918fd532971f378dd2abe6fcf07a771af1d4a51f8904ec4772492674"
          }
        },
        "F_free": {
          "E_eV": -101.99999994784096,
          "P_GPa": 2.5,
          "V_A3": 2436.330003077836,
          "output": {
            "rel": "relax\\rx_Ffree_cfg0005\\scf.out",
            "sha256": "2445182aed6d45ea9934ac4f53913f5283ebd6c670172b877f86fd66f10a7e10"
          }
        }
      },
      "stage10": false,
      "electronic_targets": null,
      "relaxed": {
        "F_B": {
          "job": "rx_FB_cfg0003",
          "file": {
            "rel": "relaxed\\rx_FB_cfg0003.xyz",
            "sha256": "eda6c32a80045b6f7673519271306c31c815d6d9b5d20f6cc2ca3e963392b540"
          },
          "parent_structure": {
            "rel": "..\\s8_anneal\\cfg0003_E-0.000_O-bo4\\post_relax.xyz",
            "sha256": "29be7546b4cffb0eb5c228bbe6f931462288c629b8e5f09fed3852b7a79eb82b"
          },
          "parent_sp_job": "sp_FB_1_cfg0003",
          "record": {
            "end_motif": "unclassified",
            "B_coordination": [
              {
                "S": 3,
                "O": 0
              },
              {
                "S": 3,
                "O": 0
              }
            ],
            "P_coordination": [
              {
                "S": 3,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              }
            ],
            "P_not_4": 1
          }
        },
        "F_P": {
          "job": "rx_FP_cfg0004",
          "file": {
            "rel": "relaxed\\rx_FP_cfg0004.xyz",
            "sha256": "b225c25c95e2df97ce33a8bb4c62f44a190cee7c76ae6d69686db36e0e92b5fc"
          },
          "parent_structure": {
            "rel": "..\\s8_anneal\\cfg0004_E-0.000_O-distributed\\post_relax.xyz",
            "sha256": "a8db764164363c341fe3a81219217466e5a836bc51a056f9373d3879f00e9cf8"
          },
          "parent_sp_job": "sp_FP_1_cfg0004",
          "record": {
            "end_motif": "unclassified",
            "B_coordination": [
              {
                "S": 3,
                "O": 0
              },
              {
                "S": 3,
                "O": 0
              }
            ],
            "P_coordination": [
              {
                "S": 3,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              }
            ],
            "P_not_4": 1
          }
        },
        "F_free": {
          "job": "rx_Ffree_cfg0005",
          "file": {
            "rel": "relaxed\\rx_Ffree_cfg0005.xyz",
            "sha256": "896302cc0b8fad4622cf57517a38da0ec01846452de89570a48d6f22a314fa3d"
          },
          "parent_structure": {
            "rel": "..\\s8_anneal\\cfg0005_E-0.000_O-free_s\\post_relax.xyz",
            "sha256": "8b6ded853ebd5c2b3cc07bbeb1728f639967a95d66dd6fa49c4517953cacb054"
          },
          "parent_sp_job": "sp_Ffree_1_cfg0005",
          "record": {
            "end_motif": "unclassified",
            "B_coordination": [
              {
                "S": 3,
                "O": 0
              },
              {
                "S": 3,
                "O": 0
              }
            ],
            "P_coordination": [
              {
                "S": 3,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              }
            ],
            "P_not_4": 1
          }
        }
      }
    }
  },
  "pressure_suffix_junk": {
    "fields": [
      {
        "family": "F_B",
        "problems": [],
        "P_kbar": 0.0,
        "force": 0.0003,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": true
      },
      {
        "family": "F_P",
        "problems": [],
        "P_kbar": 0.0,
        "force": 0.0003,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": true
      },
      {
        "family": "F_free",
        "problems": [],
        "P_kbar": 0.0,
        "force": 0.0003,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": true
      }
    ],
    "read_relax": {
      "accepted": true,
      "value": {
        "skip_eos": true,
        "eos_input": {
          "F_B": {
            "E_eV": -110.00000001844798,
            "P_GPa": 0.0,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_FB_cfg0003\\scf.out",
              "sha256": "96ab1ecdf94cbdb59ad8d4c67e60c6035a67abaa1a9cb94e0f55d8977d23ed85"
            }
          },
          "F_P": {
            "E_eV": -105.99999998314448,
            "P_GPa": 0.0,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_FP_cfg0004\\scf.out",
              "sha256": "66c975266a614c3f9424cf8999b739b4de29c27fb636ee66b3cca4cff39f768b"
            }
          },
          "F_free": {
            "E_eV": -101.99999994784096,
            "P_GPa": 0.0,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_Ffree_cfg0005\\scf.out",
              "sha256": "aa55b17ef82719b6919e61993c1e9fa0e57895eb1c7944042110d66525c6c16e"
            }
          }
        },
        "stage10": true,
        "electronic_targets": [
          {
            "family": "F_B",
            "rel": "relaxed\\rx_FB_cfg0003.xyz",
            "sha256": "eda6c32a80045b6f7673519271306c31c815d6d9b5d20f6cc2ca3e963392b540",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0003_E-0.000_O-bo4\\post_relax.xyz",
              "sha256": "29be7546b4cffb0eb5c228bbe6f931462288c629b8e5f09fed3852b7a79eb82b"
            }
          },
          {
            "family": "F_P",
            "rel": "relaxed\\rx_FP_cfg0004.xyz",
            "sha256": "b225c25c95e2df97ce33a8bb4c62f44a190cee7c76ae6d69686db36e0e92b5fc",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0004_E-0.000_O-distributed\\post_relax.xyz",
              "sha256": "a8db764164363c341fe3a81219217466e5a836bc51a056f9373d3879f00e9cf8"
            }
          },
          {
            "family": "F_free",
            "rel": "relaxed\\rx_Ffree_cfg0005.xyz",
            "sha256": "896302cc0b8fad4622cf57517a38da0ec01846452de89570a48d6f22a314fa3d",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0005_E-0.000_O-free_s\\post_relax.xyz",
              "sha256": "8b6ded853ebd5c2b3cc07bbeb1728f639967a95d66dd6fa49c4517953cacb054"
            }
          }
        ],
        "relaxed": {
          "F_B": {
            "job": "rx_FB_cfg0003",
            "file": {
              "rel": "relaxed\\rx_FB_cfg0003.xyz",
              "sha256": "eda6c32a80045b6f7673519271306c31c815d6d9b5d20f6cc2ca3e963392b540"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0003_E-0.000_O-bo4\\post_relax.xyz",
              "sha256": "29be7546b4cffb0eb5c228bbe6f931462288c629b8e5f09fed3852b7a79eb82b"
            },
            "parent_sp_job": "sp_FB_1_cfg0003",
            "record": {
              "end_motif": "unclassified",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          },
          "F_P": {
            "job": "rx_FP_cfg0004",
            "file": {
              "rel": "relaxed\\rx_FP_cfg0004.xyz",
              "sha256": "b225c25c95e2df97ce33a8bb4c62f44a190cee7c76ae6d69686db36e0e92b5fc"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0004_E-0.000_O-distributed\\post_relax.xyz",
              "sha256": "a8db764164363c341fe3a81219217466e5a836bc51a056f9373d3879f00e9cf8"
            },
            "parent_sp_job": "sp_FP_1_cfg0004",
            "record": {
              "end_motif": "unclassified",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          },
          "F_free": {
            "job": "rx_Ffree_cfg0005",
            "file": {
              "rel": "relaxed\\rx_Ffree_cfg0005.xyz",
              "sha256": "896302cc0b8fad4622cf57517a38da0ec01846452de89570a48d6f22a314fa3d"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0005_E-0.000_O-free_s\\post_relax.xyz",
              "sha256": "8b6ded853ebd5c2b3cc07bbeb1728f639967a95d66dd6fa49c4517953cacb054"
            },
            "parent_sp_job": "sp_Ffree_1_cfg0005",
            "record": {
              "end_motif": "unclassified",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          }
        }
      }
    }
  },
  "pressure_exponent_baseline": {
    "accepted": true,
    "value": {
      "skip_eos": false,
      "eos_input": {
        "F_B": {
          "E_eV": -110.00000001844798,
          "P_GPa": 2.5,
          "V_A3": 2436.330003077836,
          "output": {
            "rel": "relax\\rx_FB_cfg0003\\scf.out",
            "sha256": "d4e12448e41049589b762922b98ecf70d5c33fd7148c37dcbb429e3788ea3b69"
          }
        },
        "F_P": {
          "E_eV": -105.99999998314448,
          "P_GPa": 2.5,
          "V_A3": 2436.330003077836,
          "output": {
            "rel": "relax\\rx_FP_cfg0004\\scf.out",
            "sha256": "54a21c65918fd532971f378dd2abe6fcf07a771af1d4a51f8904ec4772492674"
          }
        },
        "F_free": {
          "E_eV": -101.99999994784096,
          "P_GPa": 2.5,
          "V_A3": 2436.330003077836,
          "output": {
            "rel": "relax\\rx_Ffree_cfg0005\\scf.out",
            "sha256": "2445182aed6d45ea9934ac4f53913f5283ebd6c670172b877f86fd66f10a7e10"
          }
        }
      },
      "stage10": false,
      "electronic_targets": null,
      "relaxed": {
        "F_B": {
          "job": "rx_FB_cfg0003",
          "file": {
            "rel": "relaxed\\rx_FB_cfg0003.xyz",
            "sha256": "eda6c32a80045b6f7673519271306c31c815d6d9b5d20f6cc2ca3e963392b540"
          },
          "parent_structure": {
            "rel": "..\\s8_anneal\\cfg0003_E-0.000_O-bo4\\post_relax.xyz",
            "sha256": "29be7546b4cffb0eb5c228bbe6f931462288c629b8e5f09fed3852b7a79eb82b"
          },
          "parent_sp_job": "sp_FB_1_cfg0003",
          "record": {
            "end_motif": "unclassified",
            "B_coordination": [
              {
                "S": 3,
                "O": 0
              },
              {
                "S": 3,
                "O": 0
              }
            ],
            "P_coordination": [
              {
                "S": 3,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              }
            ],
            "P_not_4": 1
          }
        },
        "F_P": {
          "job": "rx_FP_cfg0004",
          "file": {
            "rel": "relaxed\\rx_FP_cfg0004.xyz",
            "sha256": "b225c25c95e2df97ce33a8bb4c62f44a190cee7c76ae6d69686db36e0e92b5fc"
          },
          "parent_structure": {
            "rel": "..\\s8_anneal\\cfg0004_E-0.000_O-distributed\\post_relax.xyz",
            "sha256": "a8db764164363c341fe3a81219217466e5a836bc51a056f9373d3879f00e9cf8"
          },
          "parent_sp_job": "sp_FP_1_cfg0004",
          "record": {
            "end_motif": "unclassified",
            "B_coordination": [
              {
                "S": 3,
                "O": 0
              },
              {
                "S": 3,
                "O": 0
              }
            ],
            "P_coordination": [
              {
                "S": 3,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              }
            ],
            "P_not_4": 1
          }
        },
        "F_free": {
          "job": "rx_Ffree_cfg0005",
          "file": {
            "rel": "relaxed\\rx_Ffree_cfg0005.xyz",
            "sha256": "896302cc0b8fad4622cf57517a38da0ec01846452de89570a48d6f22a314fa3d"
          },
          "parent_structure": {
            "rel": "..\\s8_anneal\\cfg0005_E-0.000_O-free_s\\post_relax.xyz",
            "sha256": "8b6ded853ebd5c2b3cc07bbeb1728f639967a95d66dd6fa49c4517953cacb054"
          },
          "parent_sp_job": "sp_Ffree_1_cfg0005",
          "record": {
            "end_motif": "unclassified",
            "B_coordination": [
              {
                "S": 3,
                "O": 0
              },
              {
                "S": 3,
                "O": 0
              }
            ],
            "P_coordination": [
              {
                "S": 3,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              }
            ],
            "P_not_4": 1
          }
        }
      }
    }
  },
  "pressure_exponent": {
    "fields": [
      {
        "family": "F_B",
        "problems": [],
        "P_kbar": 2.5,
        "force": 0.0003,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": true
      },
      {
        "family": "F_P",
        "problems": [],
        "P_kbar": 2.5,
        "force": 0.0003,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": true
      },
      {
        "family": "F_free",
        "problems": [],
        "P_kbar": 2.5,
        "force": 0.0003,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": true
      }
    ],
    "read_relax": {
      "accepted": true,
      "value": {
        "skip_eos": true,
        "eos_input": {
          "F_B": {
            "E_eV": -110.00000001844798,
            "P_GPa": 0.25,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_FB_cfg0003\\scf.out",
              "sha256": "c0095207a9ce08513e1de249b6948130cd5f81afce14d2d2474a842c035c6825"
            }
          },
          "F_P": {
            "E_eV": -105.99999998314448,
            "P_GPa": 0.25,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_FP_cfg0004\\scf.out",
              "sha256": "45290914c3e15deeb8a6de7c41830ad6f2690431dfe2b0fb109308269683562e"
            }
          },
          "F_free": {
            "E_eV": -101.99999994784096,
            "P_GPa": 0.25,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_Ffree_cfg0005\\scf.out",
              "sha256": "d9001f36c23725a8a1ee39364755c23639ecbe03a69f58319d3c1cf147d8acda"
            }
          }
        },
        "stage10": true,
        "electronic_targets": [
          {
            "family": "F_B",
            "rel": "relaxed\\rx_FB_cfg0003.xyz",
            "sha256": "eda6c32a80045b6f7673519271306c31c815d6d9b5d20f6cc2ca3e963392b540",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0003_E-0.000_O-bo4\\post_relax.xyz",
              "sha256": "29be7546b4cffb0eb5c228bbe6f931462288c629b8e5f09fed3852b7a79eb82b"
            }
          },
          {
            "family": "F_P",
            "rel": "relaxed\\rx_FP_cfg0004.xyz",
            "sha256": "b225c25c95e2df97ce33a8bb4c62f44a190cee7c76ae6d69686db36e0e92b5fc",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0004_E-0.000_O-distributed\\post_relax.xyz",
              "sha256": "a8db764164363c341fe3a81219217466e5a836bc51a056f9373d3879f00e9cf8"
            }
          },
          {
            "family": "F_free",
            "rel": "relaxed\\rx_Ffree_cfg0005.xyz",
            "sha256": "896302cc0b8fad4622cf57517a38da0ec01846452de89570a48d6f22a314fa3d",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0005_E-0.000_O-free_s\\post_relax.xyz",
              "sha256": "8b6ded853ebd5c2b3cc07bbeb1728f639967a95d66dd6fa49c4517953cacb054"
            }
          }
        ],
        "relaxed": {
          "F_B": {
            "job": "rx_FB_cfg0003",
            "file": {
              "rel": "relaxed\\rx_FB_cfg0003.xyz",
              "sha256": "eda6c32a80045b6f7673519271306c31c815d6d9b5d20f6cc2ca3e963392b540"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0003_E-0.000_O-bo4\\post_relax.xyz",
              "sha256": "29be7546b4cffb0eb5c228bbe6f931462288c629b8e5f09fed3852b7a79eb82b"
            },
            "parent_sp_job": "sp_FB_1_cfg0003",
            "record": {
              "end_motif": "unclassified",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          },
          "F_P": {
            "job": "rx_FP_cfg0004",
            "file": {
              "rel": "relaxed\\rx_FP_cfg0004.xyz",
              "sha256": "b225c25c95e2df97ce33a8bb4c62f44a190cee7c76ae6d69686db36e0e92b5fc"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0004_E-0.000_O-distributed\\post_relax.xyz",
              "sha256": "a8db764164363c341fe3a81219217466e5a836bc51a056f9373d3879f00e9cf8"
            },
            "parent_sp_job": "sp_FP_1_cfg0004",
            "record": {
              "end_motif": "unclassified",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          },
          "F_free": {
            "job": "rx_Ffree_cfg0005",
            "file": {
              "rel": "relaxed\\rx_Ffree_cfg0005.xyz",
              "sha256": "896302cc0b8fad4622cf57517a38da0ec01846452de89570a48d6f22a314fa3d"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0005_E-0.000_O-free_s\\post_relax.xyz",
              "sha256": "8b6ded853ebd5c2b3cc07bbeb1728f639967a95d66dd6fa49c4517953cacb054"
            },
            "parent_sp_job": "sp_Ffree_1_cfg0005",
            "record": {
              "end_motif": "unclassified",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          }
        }
      }
    }
  },
  "pressure_nul_baseline": {
    "accepted": true,
    "value": {
      "skip_eos": false,
      "eos_input": {
        "F_B": {
          "E_eV": -110.00000001844798,
          "P_GPa": 2.5,
          "V_A3": 2436.330003077836,
          "output": {
            "rel": "relax\\rx_FB_cfg0003\\scf.out",
            "sha256": "d4e12448e41049589b762922b98ecf70d5c33fd7148c37dcbb429e3788ea3b69"
          }
        },
        "F_P": {
          "E_eV": -105.99999998314448,
          "P_GPa": 2.5,
          "V_A3": 2436.330003077836,
          "output": {
            "rel": "relax\\rx_FP_cfg0004\\scf.out",
            "sha256": "54a21c65918fd532971f378dd2abe6fcf07a771af1d4a51f8904ec4772492674"
          }
        },
        "F_free": {
          "E_eV": -101.99999994784096,
          "P_GPa": 2.5,
          "V_A3": 2436.330003077836,
          "output": {
            "rel": "relax\\rx_Ffree_cfg0005\\scf.out",
            "sha256": "2445182aed6d45ea9934ac4f53913f5283ebd6c670172b877f86fd66f10a7e10"
          }
        }
      },
      "stage10": false,
      "electronic_targets": null,
      "relaxed": {
        "F_B": {
          "job": "rx_FB_cfg0003",
          "file": {
            "rel": "relaxed\\rx_FB_cfg0003.xyz",
            "sha256": "eda6c32a80045b6f7673519271306c31c815d6d9b5d20f6cc2ca3e963392b540"
          },
          "parent_structure": {
            "rel": "..\\s8_anneal\\cfg0003_E-0.000_O-bo4\\post_relax.xyz",
            "sha256": "29be7546b4cffb0eb5c228bbe6f931462288c629b8e5f09fed3852b7a79eb82b"
          },
          "parent_sp_job": "sp_FB_1_cfg0003",
          "record": {
            "end_motif": "unclassified",
            "B_coordination": [
              {
                "S": 3,
                "O": 0
              },
              {
                "S": 3,
                "O": 0
              }
            ],
            "P_coordination": [
              {
                "S": 3,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              }
            ],
            "P_not_4": 1
          }
        },
        "F_P": {
          "job": "rx_FP_cfg0004",
          "file": {
            "rel": "relaxed\\rx_FP_cfg0004.xyz",
            "sha256": "b225c25c95e2df97ce33a8bb4c62f44a190cee7c76ae6d69686db36e0e92b5fc"
          },
          "parent_structure": {
            "rel": "..\\s8_anneal\\cfg0004_E-0.000_O-distributed\\post_relax.xyz",
            "sha256": "a8db764164363c341fe3a81219217466e5a836bc51a056f9373d3879f00e9cf8"
          },
          "parent_sp_job": "sp_FP_1_cfg0004",
          "record": {
            "end_motif": "unclassified",
            "B_coordination": [
              {
                "S": 3,
                "O": 0
              },
              {
                "S": 3,
                "O": 0
              }
            ],
            "P_coordination": [
              {
                "S": 3,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              }
            ],
            "P_not_4": 1
          }
        },
        "F_free": {
          "job": "rx_Ffree_cfg0005",
          "file": {
            "rel": "relaxed\\rx_Ffree_cfg0005.xyz",
            "sha256": "896302cc0b8fad4622cf57517a38da0ec01846452de89570a48d6f22a314fa3d"
          },
          "parent_structure": {
            "rel": "..\\s8_anneal\\cfg0005_E-0.000_O-free_s\\post_relax.xyz",
            "sha256": "8b6ded853ebd5c2b3cc07bbeb1728f639967a95d66dd6fa49c4517953cacb054"
          },
          "parent_sp_job": "sp_Ffree_1_cfg0005",
          "record": {
            "end_motif": "unclassified",
            "B_coordination": [
              {
                "S": 3,
                "O": 0
              },
              {
                "S": 3,
                "O": 0
              }
            ],
            "P_coordination": [
              {
                "S": 3,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              },
              {
                "S": 4,
                "O": 0
              }
            ],
            "P_not_4": 1
          }
        }
      }
    }
  },
  "pressure_nul": {
    "fields": [
      {
        "family": "F_B",
        "problems": [],
        "P_kbar": 0.0,
        "force": 0.0003,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": true
      },
      {
        "family": "F_P",
        "problems": [],
        "P_kbar": 0.0,
        "force": 0.0003,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": true
      },
      {
        "family": "F_free",
        "problems": [],
        "P_kbar": 0.0,
        "force": 0.0003,
        "bfgs": {
          "scf_cycles": 2,
          "steps": 1
        },
        "final_xyz_finite": true
      }
    ],
    "read_relax": {
      "accepted": true,
      "value": {
        "skip_eos": true,
        "eos_input": {
          "F_B": {
            "E_eV": -110.00000001844798,
            "P_GPa": 0.0,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_FB_cfg0003\\scf.out",
              "sha256": "c114356a702c830cea64fee32030b49dae0a5ca7c38cc136a883031ed40febb5"
            }
          },
          "F_P": {
            "E_eV": -105.99999998314448,
            "P_GPa": 0.0,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_FP_cfg0004\\scf.out",
              "sha256": "dfc1a81e894701d5088c7f3d684e09b2a671db898629f2d8846351ea8cb21f10"
            }
          },
          "F_free": {
            "E_eV": -101.99999994784096,
            "P_GPa": 0.0,
            "V_A3": 2436.330003077836,
            "output": {
              "rel": "relax\\rx_Ffree_cfg0005\\scf.out",
              "sha256": "1d80269aaaee0152e65d9fe635b7d6d57c32232fe9947dffd41a2d5be9727dd6"
            }
          }
        },
        "stage10": true,
        "electronic_targets": [
          {
            "family": "F_B",
            "rel": "relaxed\\rx_FB_cfg0003.xyz",
            "sha256": "eda6c32a80045b6f7673519271306c31c815d6d9b5d20f6cc2ca3e963392b540",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0003_E-0.000_O-bo4\\post_relax.xyz",
              "sha256": "29be7546b4cffb0eb5c228bbe6f931462288c629b8e5f09fed3852b7a79eb82b"
            }
          },
          {
            "family": "F_P",
            "rel": "relaxed\\rx_FP_cfg0004.xyz",
            "sha256": "b225c25c95e2df97ce33a8bb4c62f44a190cee7c76ae6d69686db36e0e92b5fc",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0004_E-0.000_O-distributed\\post_relax.xyz",
              "sha256": "a8db764164363c341fe3a81219217466e5a836bc51a056f9373d3879f00e9cf8"
            }
          },
          {
            "family": "F_free",
            "rel": "relaxed\\rx_Ffree_cfg0005.xyz",
            "sha256": "896302cc0b8fad4622cf57517a38da0ec01846452de89570a48d6f22a314fa3d",
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0005_E-0.000_O-free_s\\post_relax.xyz",
              "sha256": "8b6ded853ebd5c2b3cc07bbeb1728f639967a95d66dd6fa49c4517953cacb054"
            }
          }
        ],
        "relaxed": {
          "F_B": {
            "job": "rx_FB_cfg0003",
            "file": {
              "rel": "relaxed\\rx_FB_cfg0003.xyz",
              "sha256": "eda6c32a80045b6f7673519271306c31c815d6d9b5d20f6cc2ca3e963392b540"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0003_E-0.000_O-bo4\\post_relax.xyz",
              "sha256": "29be7546b4cffb0eb5c228bbe6f931462288c629b8e5f09fed3852b7a79eb82b"
            },
            "parent_sp_job": "sp_FB_1_cfg0003",
            "record": {
              "end_motif": "unclassified",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          },
          "F_P": {
            "job": "rx_FP_cfg0004",
            "file": {
              "rel": "relaxed\\rx_FP_cfg0004.xyz",
              "sha256": "b225c25c95e2df97ce33a8bb4c62f44a190cee7c76ae6d69686db36e0e92b5fc"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0004_E-0.000_O-distributed\\post_relax.xyz",
              "sha256": "a8db764164363c341fe3a81219217466e5a836bc51a056f9373d3879f00e9cf8"
            },
            "parent_sp_job": "sp_FP_1_cfg0004",
            "record": {
              "end_motif": "unclassified",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          },
          "F_free": {
            "job": "rx_Ffree_cfg0005",
            "file": {
              "rel": "relaxed\\rx_Ffree_cfg0005.xyz",
              "sha256": "896302cc0b8fad4622cf57517a38da0ec01846452de89570a48d6f22a314fa3d"
            },
            "parent_structure": {
              "rel": "..\\s8_anneal\\cfg0005_E-0.000_O-free_s\\post_relax.xyz",
              "sha256": "8b6ded853ebd5c2b3cc07bbeb1728f639967a95d66dd6fa49c4517953cacb054"
            },
            "parent_sp_job": "sp_Ffree_1_cfg0005",
            "record": {
              "end_motif": "unclassified",
              "B_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 3,
                  "O": 0
                }
              ],
              "P_coordination": [
                {
                  "S": 3,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                },
                {
                  "S": 4,
                  "O": 0
                }
              ],
              "P_not_4": 1
            }
          }
        }
      }
    }
  },
  "reject_invalid_target_kprobe": {
    "accepted": true,
    "value": {
      "moves": [
        [
          "kp_FB_cfg0003",
          "scf.out.rejected.1",
          [
            "PWSCF 판 7.3.1 ≠ 계약 7.4.1 (판이 다른 출력은 개별로 거부 · reject 로 보존해 다시)"
          ]
        ]
      ],
      "original_gone": true,
      "preserved": true
    }
  },
  "reject_invalid_target_relax": {
    "accepted": true,
    "value": {
      "moves": [
        [
          "rx_FB_cfg0003",
          "scf.out.rejected.1",
          [
            "PWSCF 판 7.3.1 ≠ 계약 7.4.1 (판이 다른 출력은 개별로 거부 · reject 로 보존해 다시)"
          ]
        ]
      ],
      "original_gone": true,
      "preserved": true
    }
  },
  "source_sha256_after": "f6105cfc2ae933eaf321472d232bca47d4512198a3d68c66a62b0b1804c6ab2e"
}{
  "exception": "TypeError",
  "message": "'NoneType' object is not subscriptable",
  "verdict_written": true,
  "skip_eos": true,
  "stage10_present": true,
  "electronic_targets": 3,
  "bfgs_records": [
    null,
    null,
    null
  ],
  "stdout": "DFT 도구 C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_EG_v3_20261113\\source\\tools\\doping\\b2o3_bo_dft.py · sha256 f6105cfc2ae933eaf321472d232bca47d4512198a3d68c66a62b0b1804c6ab2e\n판독기 C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_EG_v3_20261113\\source\\tools\\doping\\b2o3_bo_readout.py · sha256 872d91f7508ad21c3d67f373bee228bd894994b731a77f69525818db3a8967cf\n-> C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_EG_v3_20261113\\scratch\\eg3_fixture_a6w9zsdk\\bfgs_cli\\cli_relax_verdict.json\n"
}{
  "original_P_kbar": -10.88,
  "matrix_trace_over3_kbar": -10.88,
  "original_matrix_kbar": [
    [
      -5.75,
      -0.58,
      -1.88
    ],
    [
      -0.58,
      -14.91,
      -1.42
    ],
    [
      -1.88,
      -1.42,
      -11.98
    ]
  ],
  "original": {
    "problems": [],
    "state_problems": [],
    "P_kbar": -10.88
  },
  "three_tensor_rows_removed": {
    "problems": [],
    "state_problems": [],
    "P_kbar": -10.88
  },
  "header_changed_tensor_unchanged": {
    "problems": [],
    "state_problems": [],
    "P_kbar": 0.0
  }
}