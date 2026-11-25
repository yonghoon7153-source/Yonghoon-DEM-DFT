---
title: "EG 회신 — b2o3 9 단계 DFT 도구 v2: NO-GO (P0 0 · P1 2 · P2 4) · 출력 상태 결속 (끼워 넣은 압력 · 좌표 · 힘 조각) · reject 대상 목록 · G5 캐시 · GPU 조회 종료코드 · 버전 혼합 복구 · DY 확인 4 아직 해제 못 함 · k 격자 대조 찬성"
date: 2026-11-13
updated: 2026-11-13
tags: [review, b2o3, dft, qe, eos, kprobe, readout, codex, reply, letter]
letter: EG
track: b2o3
channel: codex
kind: reply
status: 수령 2026-11-13 (사용자 붙여넣기) · NO-GO · 기준 328cf95b (도구 sha256 4e865e5c · 실행기 9157ca2c · 변이 도구 0c8ef487) · 고침 → 다음 편지 EH
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> 원문 그대로 보존 (사용자 붙여넣기 2026-11-13). 링크의 C:/ 경로는 Codex 쪽 작업 폴더다 (저장소 밖).

NO-GO — P1 2건과 P2 4건이 남았습니다. 사용자 비준만 남은 상태는 아닙니다.

기준 커밋 328cf95b에서 요청한 도구·실행기·변이시험의 SHA256을 확인했습니다. Windows에서 selftest 119/119, Git Bash에서 실행기 20/20, 전체 변이시험 73/73 적색을 재현했습니다. 생산 UMA·DFT·MD는 실행하지 않았습니다.

그런데 추가 시험에서 EOS 보류가 해제되는 잘못된 경로가 실제로 통과했습니다. 아래 지적은 모두 재현한 것이며, 추측으로 올린 항목은 없습니다.

P1-1. 한 실행인지 세지만, 마지막 에너지·힘·압력·좌표가 같은 상태의 결과인지는 묶지 못합니다.

위치: [b2o3_bo_dft.py (line 452)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_v2_20261113/source/tools/doping/b2o3_bo_dft.py:452), 같은 파일 463, 473, 622.

판독기는 마지막 힘 블록·마지막 압력·마지막 최종 좌표를 각각 고릅니다. 따라서 JOB DONE 앞에 머리 없는 조각을 넣으면 실행 수와 설정 줄 개수는 그대로인데 소비하는 값만 달라집니다.

전체 read_relax 경로에서 다음을 재현했습니다.
- 세 가족 모두 P=2.5 GPa → EOS 필요 → 후속 대상 null인 정상 시험 출력에 P=0 응력 블록을 JOB DONE 앞에 추가했습니다. 결과는 EOS 생략·안정성 대상 생성·전자구조 대상 3개 생성으로 바뀌었습니다.
- 최종 좌표 블록을 하나 더 넣고 Li 하나의 분수좌표를 0.01 바꿨습니다. 기존 에너지와 바뀐 좌표가 함께 통과하여 전자구조 대상으로 나갔습니다.
- 마지막 힘 0.05 Ry/Bohr로 거부된 출력에 작은 힘 블록을 추가하면 통과했습니다.
합성 출력만의 문제도 아닙니다. 실제 MLi_04_x108 출력에 압력 조각을 추가했을 때 −10.88 kbar 대신 0 kbar를 읽고 검사 통과했습니다.

힘 블록의 완전성 검사도 줄 수만 봅니다. 같은 실제 출력에서 마지막 힘의 원자 1 행을 삭제하고 원자 2 행을 복제해도 58개 판독으로 통과했습니다.

최소 수정: 마지막 SCF와 BFGS 종료를 경계로 에너지·힘·응력을 묶고, 그 종료에 대응하는 최종 좌표 블록을 하나만 허용하세요. 중복·경계 밖 조각은 거부하고, 힘은 원자 번호 1…nat의 누락·중복까지 검사해야 합니다. 위 반례를 전체 read_relax 음성시험에 넣어야 합니다.

P1-2. reject는 판정의 계획 링크만 확인하고, 실제 이동할 잡 목록은 그대로 믿습니다.

위치: [b2o3_bo_dft.py (line 1204)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_v2_20261113/source/tools/doping/b2o3_bo_dft.py:1204), 668.

정상 탐침 판정의 jobs_relax[0].job만 ../unrelated로 바꿨습니다. 그 폴더에는 원래 잡과 같은 입력 바이트, 검사에 걸리는 별도 출력을 두었습니다.

reject는 변경된 목록을 받아 선언된 relax 잡 밖의 scf.out을 scf.out.rejected.1로 이동했습니다. 계획 링크와 입력 해시는 모두 기존 값으로 통과했습니다.

최소 수정: 이동 전에 유효한 계획·앞 단계 근거에서 기대 잡 목록과 입력을 다시 만들고 대조하세요. 대상 경로도 해당 단계의 선언된 잡 폴더로 제한해야 합니다. 거부할 출력 자체가 유효해야 한다는 순환 조건을 걸 필요는 없습니다. 출력 검사와 대상 목록 검증을 분리하면 됩니다.

P2-1. G5의 UMA 순서는 원자료를 재판독하고도 계획의 캐시를 사용합니다.

위치: [b2o3_bo_dft.py (line 930)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_v2_20261113/source/tools/doping/b2o3_bo_dft.py:930), 1020.

_rebind_plan은 실제 8단계 판독 A100을 다시 얻지만, _build_sp_verdict는 plan["stage8"]["order"]를 읽습니다.

원자료·선택 구조·DFT 출력을 그대로 두고 계획의 순서만 뒤집은 뒤 새 판정을 만들면, G5가 same_order=True에서 False로 바뀝니다. 기존 판정 파일의 G5 수정은 막았지만, 그 G5를 만드는 입력 캐시의 변경은 남았습니다.

최소 수정: 재계산한 A100의 순서를 직접 사용하거나, 계획의 8단계 요약 전체를 재계산 결과와 대조하세요.

P2-2. VRAM 조회가 숫자를 출력하고 실패하면 실행을 허용합니다.

위치: [run_force_check_scf.sh (line 77)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_v2_20261113/source/tools/doping/run_force_check_scf.sh:77).

메모리 조회의 파이프라인이 nvidia-smi의 종료코드를 보존하지 않습니다.

모의 명령을 46000 출력 후 exit 9, compute 프로세스 조회는 정상·빈 목록으로 만들었습니다. MIN_FREE_MIB=45000 GPU_EXCLUSIVE=1인데 _gpu_guard는 rc=0을 반환했습니다.

최소 수정: 조회 원문과 종료코드를 먼저 받고, 성공한 경우에만 숫자를 가공하세요. 숫자 출력 + 비정상 종료 음성시험도 필요합니다.

P2-3. “nvidia-smi 없음” 시험은 검사 함수가 실행되지 않아도 통과합니다.

위치: [run_force_check_scf.sh (line 146)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_v2_20261113/source/tools/doping/run_force_check_scf.sh:146).

시험은 PATH를 비운 뒤 상대 명령 env를 실행합니다. 따라서 env: command not found, rc=127이 나고 바깥의 ! 때문에 성공합니다.

_gpu_guard를 항상 허용하는 함수로 바꿔도 이 시험은 통과했습니다.

최소 수정: 시험을 띄우는 env·Bash는 절대경로로 지정하고, 함수가 낸 거부 코드·메시지를 확인하세요. nvidia-smi 존재 검사를 끄면 이 시험이 실패해야 합니다.

P2-4. 버전 혼합으로 거부된 출력은 reject로 복구되지 않습니다.

위치: [b2o3_bo_dft.py (line 662)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_v2_20261113/source/tools/doping/b2o3_bo_dft.py:662), 668.

단일점 여섯 중 하나만 QE 버전을 7.3.1, 나머지는 7.4.1로 만들었습니다.
- read_sp: 버전 혼합으로 거부.
- reject: 이동 목록 [].
- 실행기: 각 출력은 완료 조건을 만족하므로 다시 건너뛸 수 있음.
단계 전체에서 생기는 거부 사유가 개별 출력만 검사하는 복구 함수에 전달되지 않습니다.

최소 수정: 승인한 QE 버전과 다른 출력을 보존·재실행 대상으로 정하거나, 버전 혼합 시 별도 복구 절차를 명시하세요. 어느 출력을 버릴지 도구가 임의로 골라서는 안 됩니다.

P0·P3로 별도 올릴 항목은 없습니다.

Q1. EF의 반례가 닫혔나?
EF 항목	이번 판정
P1-1 실행 섞임	부분 해제. 완전한 실행 이어붙임·설정 중복은 차단. 종료 전 압력·힘·좌표 조각은 통과
P1-2 구조·k 판 자격	닫힘. 구조와 입력 해시 동시 변경, 근거 없는 dense 판 모두 차단
P1-3 실제 k 격자	닫힘. 다른 격자·shift·누락·잘못된 가중치 차단
P1-4 이완 기준	부분 해제. 느슨한 기준·큰 힘 자체는 차단. 뒤의 힘 조각으로 대체 가능
P1-5 전자 수	닫힘. 전자 수·Zval 불일치와 결측 차단
P1-6 EOS 보류 대상	닫힘. 올바르게 읽은 EOS 보류에서는 두 대상 모두 null
P2 판정 증거 소비	부분 해제. 판정 파일 수정은 차단하지만 계획의 UMA 순서 캐시 문제 잔존
P2 경로 기준·깨진 바이트·CRLF	닫힘
P2 GPU 확인	부분 해제. 조회 종료코드와 음성시험 문제 잔존
P2 거부 잡 재실행	부분 해제. 일반 실패 출력 보존은 작동. 대상 목록 검증·버전 혼합 복구 미완료


Q2. “한 출력 = 한 실행” 규칙에 남은 구멍이 있나?

있습니다. 머리와 종료 표지가 하나라는 사실은 본문의 모든 조각이 한 상태에 속한다는 증거가 아닙니다. P1-1의 세 조각 모두 기존 개수 검사를 통과했습니다. 설정 줄 목록을 조금 더 늘리는 것보다 마지막 계산 상태의 블록 경계를 검사하는 쪽이 필요합니다.

Q3. k 격자 대조는 맞나?

이번 셀·격자·nspin=1 범위에서는 찬성입니다.

실제 QE 7.4.1 출력 MLi_04_x108, MP_07_x100, host의 격자 검사가 모두 통과했습니다. MLi 출력은 해당 잡의 설정에 맞춘 전체 출력 검사도 통과했습니다. 이는 파서 호환성 확인이며, 그 잡의 PP 원본을 별도로 인증한 것은 아닙니다.

nosym의 시간반전 축소와 noinv의 전체 목록을 모두 받는 것은 적절합니다. QE 공식 설명도 이 차이를 명시합니다. QE nosym/noinv 설명

출력 축을 이용한 좌표 변환은 QE 7.4.1의 변환식과 같고, nspin=1에서 가중치 합 2를 사용하는 것도 맞습니다. QE 좌표 출력·변환 구현, 가중치 처리

캠페인 host 셀에서 전체 격자를 독립 생성하고 축 6자리·k 좌표 7자리로 반올림했습니다. 정수 격자 잔차는 최대 8.3×10⁻⁷, 출력 반올림의 보수적 오차 한계도 1.9×10⁻⁶ 미만이어서 1e-4는 충분했습니다. 이를 임의의 심하게 찌그러진 셀까지 보장하는 수치로 확대하지 않으면 됩니다.

Q4. DY 확인 4, EOS (E,P,V) 결속을 해제할 수 있나?

아직 불가합니다. 출력 파일의 해시는 연결됐지만, 그 파일 안에서 E와 P가 같은 계산 상태에서 왔는지는 보장하지 못합니다. P1-1에서 실제로 EOS 판정이 뒤집혔습니다.

Q5. 범위 문장·EOS 다음 판·GPU 보장 범위는 맞나?

문구는 찬성입니다.

대표 구조·고정 셀·현재 수렴 설정에 조건부라는 제한, 0.10 eV를 정확도 보증으로 쓰지 않는 제한, 이미 본 값을 공개하고 다음 EOS 절차를 정한다는 원칙은 적절합니다. GPU 확인을 시작 시점으로 한정한 설명도 맞습니다. 다만 실제 조회 실패 처리는 P2-2를 고쳐야 그 문구와 일치합니다.

Q6. reject로 P2-6이 닫혔나?

부분적으로만 닫혔습니다. 일반적인 개별 실패 출력의 순번 보존은 작동합니다. 그러나 P1-2와 P2-4 때문에 전체 복구 절차를 승인할 수는 없습니다.

Q7. DFT 진입 전에 무엇이 남았나?

다음 확인까지 필요합니다.
1. 출력 상태 결속: 압력·힘·좌표 조각 삽입과 원자 번호 누락·중복을 거부하고, 정상 실제 QE 출력은 계속 통과할 것.
2. reject 대상 결속: 변경된 잡 목록·단계 밖 경로를 이동 전에 거부하고, 버전 혼합 복구 경로를 정할 것.
3. G5 원자료 대조: 계획의 UMA 순서를 바꿔도 거부되거나 원자료의 올바른 순서만 사용할 것.
4. GPU 검사와 시험: 숫자를 출력한 실패 조회도 거부하고, 존재 검사를 끈 변이는 해당 음성시험에서 실패할 것.
5. 고친 도구로 정상 연결 경로와 위 반례를 재확인한 뒤, 고친 판을 사용자가 비준할 것.
재현 자료는 [전체 경로 시험 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_v2_20261113/probes_v2_results.json), [실제 QE 출력 대조 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_v2_20261113/raw_results.json), [변이시험 기록](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_v2_20261113/mutations.log)에 있습니다. 단계 연결 시험의 8단계 자료는 합성 fixture를 사용했으며, gabia의 원본 md.traj를 통한 실물 8단계 재판독은 이번 환경에서 독립 재현하지 않았습니다.

{
  "source_sha256": "4e865e5c3e5785b24955b2805d11fe3f3905ca5ae1fc0911acd513f96e2f9048",
  "fixture": "C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_EF_v2_20261113\\scratch\\ef2_fixture_23zjxqix",
  "native_selftest_rc": 0,
  "baseline_eos_hold": {
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
            "sha256": "c16dd6b54b4f5212a35312e81fd8ffe93e6fbaf2606600c751cd1b62396cf977"
          }
        },
        "F_P": {
          "E_eV": -105.99999998314448,
          "P_GPa": 2.5,
          "V_A3": 2436.330003077836,
          "output": {
            "rel": "relax\\rx_FP_cfg0004\\scf.out",
            "sha256": "91c55647536f3b731165d45e0928edb9f1e82f02283758759971106e7fcdc934"
          }
        },
        "F_free": {
          "E_eV": -101.99999994784096,
          "P_GPa": 2.5,
          "V_A3": 2436.330003077836,
          "output": {
            "rel": "relax\\rx_Ffree_cfg0005\\scf.out",
            "sha256": "6d409820b61e506b7798989ff93bd8b3cbb42a47756a24ab1d745d270cedcded"
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
  "extra_pressure_before_done": {
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
            "sha256": "1dbbc2cdcb1171ef2278122aa4d7ce14759130d5a725265b4b665dd0f98eb127"
          }
        },
        "F_P": {
          "E_eV": -105.99999998314448,
          "P_GPa": 0.0,
          "V_A3": 2436.330003077836,
          "output": {
            "rel": "relax\\rx_FP_cfg0004\\scf.out",
            "sha256": "61dc7537a6d748fb8b917e09e36e69def2a7abde2fc349b6f17f9113cad74798"
          }
        },
        "F_free": {
          "E_eV": -101.99999994784096,
          "P_GPa": 0.0,
          "V_A3": 2436.330003077836,
          "output": {
            "rel": "relax\\rx_Ffree_cfg0005\\scf.out",
            "sha256": "5bf7cfec6cfd912c7827bb29bdc60f21e428c0812d55521ea542cab92a952e78"
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
  },
  "extra_coordinates_before_done": {
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
            "sha256": "f2ba973bd06e1b080c4e481128f9accedadfc0f5c26d691bc4262a901bbe6af4"
          }
        },
        "F_P": {
          "E_eV": -105.99999998314448,
          "P_GPa": 0.0,
          "V_A3": 2436.330003077836,
          "output": {
            "rel": "relax\\rx_FP_cfg0004\\scf.out",
            "sha256": "6fde16938df65cea5e8779a21dabaa222c4df5c1f1f430979570c80280c2335a"
          }
        },
        "F_free": {
          "E_eV": -101.99999994784096,
          "P_GPa": 0.0,
          "V_A3": 2436.330003077836,
          "output": {
            "rel": "relax\\rx_Ffree_cfg0005\\scf.out",
            "sha256": "30ddb233a64ddbe5d9587d0bfbcebb743ce48d2b6db2dabed400f12f5bcc1e88"
          }
        }
      },
      "stage10": true,
      "electronic_targets": [
        {
          "family": "F_B",
          "rel": "relaxed\\rx_FB_cfg0003.xyz",
          "sha256": "2d2c08dc9226b6f87bc6179ef6e9eeb01d9114d1885bbbedee6c325ec13fee58",
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
            "sha256": "2d2c08dc9226b6f87bc6179ef6e9eeb01d9114d1885bbbedee6c325ec13fee58"
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
    },
    "two_final_blocks": 2
  },
  "baseline_large_force": {
    "accepted": false,
    "error": "SystemExit: ⛔ relax 출력 결속 · 검사 실패 3 건 — 판독하지 않는다:\n  rx_FB_cfg0003: 마지막 힘 성분 최대 5.00e-02 Ry/Bohr > forc_conv_thr 0.001 (모든 성분 기준)\n  rx_FP_cfg0004: 마지막 힘 성분 최대 5.00e-02 Ry/Bohr > forc_conv_thr 0.001 (모든 성분 기준)\n  rx_Ffree_cfg0005: 마지막 힘 성분 최대 5.00e-02 Ry/Bohr > forc_conv_thr 0.001 (모든 성분 기준)\n  → 실패 출력을 보존해 옮긴 뒤 (b2o3_bo_dft.py reject … --stage relax) 같은 실행기로 다시 돌린다"
  },
  "extra_force_before_done": {
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
            "sha256": "2d79601baf4dae5fc75d3fc03ab33c5d1fd7c900e3872e6ecd6657789e21429d"
          }
        },
        "F_P": {
          "E_eV": -105.99999998314448,
          "P_GPa": 0.0,
          "V_A3": 2436.330003077836,
          "output": {
            "rel": "relax\\rx_FP_cfg0004\\scf.out",
            "sha256": "58a93e48caa710b8aaf490f26ba8099b442345f84fcf4afc56f44d66745b8823"
          }
        },
        "F_free": {
          "E_eV": -101.99999994784096,
          "P_GPa": 0.0,
          "V_A3": 2436.330003077836,
          "output": {
            "rel": "relax\\rx_Ffree_cfg0005\\scf.out",
            "sha256": "e6607aef639235503a0b1a4bb55356fb282b26646c6833b069ae13dd59a0254c"
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
  },
  "cached_stage8_order": {
    "accepted": true,
    "value": {
      "uma_order": [
        "F_free",
        "F_P",
        "F_B"
      ],
      "same_order": false,
      "⚠": "단일점 (UMA 이완 기하) 순서 — 기록 · 'DFT 순위' 가 아니다 (판정은 이온 이완 뒤 · 절차 9_DFT_확인 ⛔)"
    },
    "original": {
      "uma_order": [
        "F_B",
        "F_P",
        "F_free"
      ],
      "same_order": true,
      "⚠": "단일점 (UMA 이완 기하) 순서 — 기록 · 'DFT 순위' 가 아니다 (판정은 이온 이완 뒤 · 절차 9_DFT_확인 ⛔)"
    }
  },
  "reject_changed_job_list": {
    "accepted": true,
    "value": {
      "moved": [
        [
          "../unrelated",
          "scf.out.rejected.1",
          [
            "ecutwfc 40.0 ≠ 52.0"
          ]
        ]
      ],
      "foreign_original_exists": false,
      "foreign_rejected_exists": true
    }
  },
  "mixed_version_read": {
    "accepted": false,
    "error": "SystemExit: ⛔ sp 출력의 PWSCF 판이 갈린다 ['7.3.1', '7.4.1']"
  },
  "mixed_version_reject": {
    "accepted": true,
    "value": []
  },
  "source_sha256_after": "4e865e5c3e5785b24955b2805d11fe3f3905ca5ae1fc0911acd513f96e2f9048"
}
{
  "MLi_04_x108.out": {
    "version": "7.4.1",
    "nat": 58,
    "nelec": 298.0,
    "smearing": "marzari-vanderbilt",
    "nk": 4,
    "n_runs": 1,
    "n_job_done": 1,
    "n_scf": 66,
    "once": {
      "ecutwfc": 1,
      "ecutrho": 1,
      "nelec": 1,
      "nk": 1,
      "conv_thr": 1,
      "xc": 1,
      "axes": 1,
      "initial": 1,
      "volume": 1,
      "alat": 1
    },
    "once_relax": {
      "etot_thr": 1,
      "forc_thr": 1,
      "nstep": 1
    },
    "after_done": [],
    "final_forces_max_comp_RyBohr": 0.00068199,
    "bfgs": {
      "scf_cycles": 66,
      "steps": 65
    },
    "bfgs_criteria": [
      1e-05,
      0.001
    ],
    "kmesh_problems": [],
    "out_problems_with_job_contract": [],
    "nelec_from_composition_and_printed_Z": 298.0
  },
  "real_QE_plus_pressure_fragment": {
    "original_P_kbar": -10.88,
    "parsed_P_kbar": 0.0,
    "problems": []
  },
  "real_QE_duplicate_force_id": {
    "force_rows_count": 58,
    "problems": []
  },
  "MP_07_x100.out": {
    "version": "7.4.1",
    "nat": 66,
    "nelec": 318.0,
    "smearing": "marzari-vanderbilt",
    "nk": 4,
    "n_runs": 1,
    "n_job_done": 1,
    "n_scf": 46,
    "once": {
      "ecutwfc": 1,
      "ecutrho": 1,
      "nelec": 1,
      "nk": 1,
      "conv_thr": 1,
      "xc": 1,
      "axes": 1,
      "initial": 1,
      "volume": 1,
      "alat": 1
    },
    "once_relax": {
      "etot_thr": 1,
      "forc_thr": 1,
      "nstep": 1
    },
    "after_done": [],
    "final_forces_max_comp_RyBohr": 0.00045572,
    "bfgs": {
      "scf_cycles": 46,
      "steps": 45
    },
    "bfgs_criteria": [
      1e-05,
      0.001
    ],
    "kmesh_problems": []
  },
  "host.out": {
    "version": "7.4.1",
    "nat": 62,
    "nelec": 294.0,
    "smearing": "marzari-vanderbilt",
    "nk": 10,
    "n_runs": 1,
    "n_job_done": 1,
    "n_scf": 7,
    "once": {
      "ecutwfc": 1,
      "ecutrho": 1,
      "nelec": 1,
      "nk": 1,
      "conv_thr": 1,
      "xc": 1,
      "axes": 1,
      "initial": 1,
      "volume": 1,
      "alat": 1
    },
    "once_relax": {
      "etot_thr": 1,
      "forc_thr": 1,
      "nstep": 1
    },
    "after_done": [],
    "final_forces_max_comp_RyBohr": 9.903e-05,
    "bfgs": {
      "scf_cycles": 7,
      "steps": 6
    },
    "bfgs_criteria": [
      1e-06,
      0.0001
    ],
    "kmesh_problems": []
  },
  "full_grid_[3, 2, 1]": {
    "accepted": true,
    "residual_max": 5.639739999452331e-07,
    "worst_print_bound": 1.445657282663299e-06,
    "tol": 0.0001
  },
  "full_grid_[4, 2, 1]": {
    "accepted": true,
    "residual_max": 8.257699999347778e-07,
    "worst_print_bound": 1.836154006679132e-06,
    "tol": 0.0001
  }
}
  빨강 바이트 손상 (selftest: 118/119) ✗ [음성] 출력에 깨진 바이트 → 판독 안 함 (조용히 지우지 않는다)
  빨강 실행 수 (selftest: 117/119) ✗ [음성] 단일점 출력 실행이 2 개 어긋남 → 판독 안 함
  빨강 JOB DONE 수 (crash rc=1) ✗ [음성] 단일점 출력 JOB DONE 어긋남 → 판독 안 함
  빨강 설정 줄 한 번 (selftest: 118/119) ✗ [음성] 단일점 출력 설정 줄이 한 번씩이 아니다 어긋남 → 판독 안 함
  빨강 JOB DONE 뒤 기록 (selftest: 118/119) ✗ [음성] 단일점 출력 JOB DONE 뒤에 계산 기록 어긋남 → 판독 안 함
  빨강 SCF '!' 한 번 (crash rc=1) ✗ [음성] 단일점 출력 '!' 총에너지가 2 개 어긋남 → 판독 안 함
  빨강 이완 '!' 수 = BFGS (crash rc=1) ✗ [음성] '!' 줄 수 (2) ≠ BFGS 가 센 SCF 수 (3) — 빠진 · 끼워 넣은 조각 → 판독 안 함
  빨강 SCF 수렴 (crash rc=1) ✗ [음성] 단일점 출력 SCF 수렴 어긋남 → 판독 안 함
  빨강 입력 이름 (crash rc=1) ✗ [음성] 단일점 출력 입력 이름 어긋남 → 판독 안 함
  빨강 ecut (crash rc=1) ✗ [음성] 단일점 출력 ecutwfc 어긋남 → 판독 안 함
  빨강 conv_thr (crash rc=1) ✗ [음성] 단일점 출력 conv_thr 어긋남 → 판독 안 함
  빨강 smearing (crash rc=1) ✗ [음성] 단일점 출력 smearing 어긋남 → 판독 안 함
  빨강 교환상관 (crash rc=1) ✗ [음성] 단일점 출력 교환상관 어긋남 → 판독 안 함
  빨강 스핀 (crash rc=1) ✗ [음성] 단일점 출력 스핀 어긋남 → 판독 안 함
  빨강 PP md5 (crash rc=1) ✗ [음성] 단일점 출력 유사포텐셜 S 어긋남 → 판독 안 함
  빨강 Zval (crash rc=1) ✗ [음성] 단일점 출력 Zval 어긋남 → 판독 안 함
  빨강 전자 수 (crash rc=1) ✗ [음성] 단일점 출력 전자 수 어긋남 → 판독 안 함
  빨강 셀 축 (crash rc=1) ✗ [음성] 단일점 출력 셀 축 어긋남 → 판독 안 함
  빨강 처음 좌표 (crash rc=1) ✗ [음성] 단일점 출력 처음 좌표 어긋남 → 판독 안 함
  빨강 prefix (crash rc=1) ✗ [음성] 단일점 출력 prefix 어긋남 → 판독 안 함
  빨강 k shift (selftest: 118/119) ✗ [음성] 입력 k shift 가 0 0 0 이 아니면 거부 (격자 대조의 전제)
  빨강 k 격자 호출 (crash rc=1) ✗ [음성] 단일점 출력 요청 격자 어긋남 → 판독 안 함
  빨강 힘 블록 (crash rc=1) ✗ [음성] 단일점 출력 힘 블록 어긋남 → 판독 안 함
  빨강 이완 설정 한 번 (crash rc=1) ✗ [음성] 느슨한 이완 문턱 줄이 뒤에 한 번 더 (섞인 출력) → 판독 안 함
  빨강 BFGS 기준 (crash rc=1) ✗ [음성] 느슨한 BFGS 기준 (1e-2 · 1e-1) 의 수렴 (EF P1-4) → 판독 안 함
  빨강 이완 문턱 (crash rc=1) ✗ [음성] 출력 머리의 이완 문턱이 계약과 다름 → 판독 안 함
  빨강 nstep (crash rc=1) ✗ [음성] nstep 50 ≠ 200 → 판독 안 함
  빨강 힘 성분 (crash rc=1) ✗ [음성] 마지막 힘 성분 0.05 Ry/Bohr > 1e-3 (EF P1-4) → 판독 안 함
  빨강 bfgs (selftest: 118/119) ✗ [음성] 이완 미수렴 ('bfgs converged' 없음) → 판독 안 함
  빨강 최종 좌표 (selftest: 118/119) ✗ [음성] 최종 좌표 블록 없음 → 판독 안 함
  빨강 Final energy (crash rc=1) ✗ [음성] Final energy 가 마지막 '!' 와 다름 → 판독 안 함
  빨강 응력 뒤 (crash rc=1) ✗ [음성] 응력이 마지막 SCF 뒤에 없다 (앞 걸음의 압력) → 판독 안 함
  빨강 부피 (crash rc=1) ✗ [음성] 출력 부피 ≠ 기준 셀 V₀ → 판독 안 함
  빨강 격자 밖 (selftest: 116/119) ✗ [음성] k 격자 — 3×2×1 출력을 4×2×1 요청으로 읽으면 거부 (점이 격자 밖)
  빨강 가중치 몫 (selftest: 117/119) ✗ [음성] k 격자 — 가중치가 격자 몫 (2/N · 4/N) 이 아니면 거부
  빨강 −k 둘 몫 (selftest: 118/119) ✗ [음성] k 격자 — 대칭으로 줄인 목록 (자기 짝 점에 둘 몫 가중치) 은 거부 (nosym 이어야)
  빨강 정확히 덮음 (selftest: 118/119) ✗ [음성] k 격자 — 점 하나 빠지면 거부
  빨강 누락 (selftest: 118/119) ✗ [음성] 단일점 출력 하나 없음 → 누락으로 멈춘다 (실패로 세지 않는다)
  빨강 입력 sha (crash rc=1) ✗ [음성] 입력을 계획 뒤 손대면 (sha256) 멈춘다
  빨강 판 갈림 (crash rc=1) ✗ [음성] 단일점 출력 PWSCF 판이 갈린다 어긋남 → 판독 안 함
  빨강 원소 머리 (selftest: 118/119) ✗ [음성] 유사포텐셜 원소 머리가 다르면 멈춘다
  빨강 가전자 못 읽음 (selftest: 118/119) ✗ [음성] 가전자 수를 못 읽으면 멈춘다 (기대 전자 수를 못 낸다)
  빨강 유사포텐셜 다시 기록 (crash rc=1) ✗ [음성] 계획의 가전자 기록을 손대면 (S 6 → 5) 지금 파일과 달라 멈춘다
  빨강 본 판독 core (selftest: 118/119) ✗ [음성] 본 판독 파일을 손대면 (승자 바꿈) 멈춘다
  빨강 보류 (selftest: 118/119) ✗ [음성] 8 단계 본 판독이 보류면 DFT 대상을 고르지 않는다
  빨강 성공 목록 대조 (selftest: 118/119) ✗ [음성] 성공 목록의 최저가 본 판독과 다르면 멈춘다 (성공 정의가 갈림)
  빨강 고르기 대조 (selftest: 118/119) ✗ [음성] 계획의 대상을 손대면 다시 고른 것과 달라 멈춘다
  빨강 구조 다시 찾기 (selftest: 118/119) ✗ [음성] 계획의 구조를 다른 런 것으로 바꾸고 입력 · 해시를 같이 고쳐도 8 단계 기록에서 다시 찾아 멈춘다 (EF P1-2)
  빨강 k_main 자격 (다시 결속) (selftest: 117/119) ✗ [음성] 계획의 k_main 을 4×2×1 로 고치고 입력 · 해시를 같이 고쳐도 탐침 발동 판정이 없어 멈춘다 (EF P1-2)
  빨강 섞인 계획 (selftest: 118/119) ✗ [음성] k_main 3×2×1 계획에 탐침 판정 고리가 붙어 있으면 멈춘다 (섞인 계획)
  빨강 발동 아님 (selftest: 118/119) ✗ [음성] 발동 안 한 탐침 판정으로는 4×2×1 판을 열지 않는다
  빨강 다른 8 단계 결과 (selftest: 118/119) ✗ [음성] 다른 8 단계 결과 파일로 만든 계획에 남의 발동 판정을 붙이지 않는다
  빨강 발동 근거 다시 (selftest: 118/119) ✗ [음성] 발동 안 한 탐침 판정을 '발동' 으로 고쳐 4×2×1 판을 열려 하면 멈춘다 (출력에서 다시 냄)
  빨강 도구 sha (crash rc=1) ✗ [음성] 계획을 만든 도구 판과 다르면 멈춘다
  빨강 계약 같음 (selftest: 118/119) ✗ [음성] 계획에 저장된 계약 (판정 여유 0.10 → 0.05) 을 손대면 멈춘다 (저장된 칸도 참이어야)
  빨강 단일점 입력 다시 (crash rc=1) ✗ [음성] 입력과 계획의 sha 를 같이 고쳐도 (mixing_beta) 다시 만든 입력과 달라 멈춘다
  빨강 단일점 판정 통째 (selftest: 114/119) ✗ [음성] 단일점 판정의 순서 를 손대면 탐침 판독이 멈춘다 (판정을 통째로 다시 내서 대조)
  빨강 탐침 발동 다시 (selftest: 117/119) ✗ [음성] 탐침 판정의 쌍 값을 손대면 이완 판독이 멈춘다 (출력에서 다시 낸 판정과 다름)
  빨강 탐침 판정 통째 (selftest: 117/119) ✗ [음성] 탐침 판정의 이완 잡 목록을 손대면 멈춘다 (판정을 통째로 다시 냄)
  빨강 탐침 변화 (crash rc=1) ✗ [음성] 탐침 — 가족 차 0.06 변함 → 발동
  빨강 탐침 순서 (selftest: 118/119) ✗ [음성] 탐침 — 순서 바뀜 (변화 0.04 라도) → 발동
  빨강 탐침 경계 (selftest: 118/119) ✗ [음성] 탐침 — 0.10 경계 건넘 (변화 0.04 라도) → 발동
  빨강 발동 뒤 이완 거부 (selftest: 118/119) ✗ [음성] 발동한 탐침 뒤 이완은 판독하지 않는다
  빨강 host sha (selftest: 118/119) ✗ [음성] host 파일이 카드 sha256 이 아니면 기준 셀을 만들지 않는다
  빨강 고르기 규칙 (selftest: 118/119) ✗ [양성] 10 단계 — DFT 차 0.05 < 0.10 (|P| ≤ 0.1 GPa · 보정 < 0.004 eV) → 가족마다 UMA 어닐 최저 하나 (셋)
  빨강 stage10 계획 폴더 기준 (selftest: 118/119) ✗ [양성] 10 단계 — DFT 승자 F_B (0.2 ≥ 0.10) → 그 가족 UMA 어닐 최저 셋 · 전자구조 대상 = 이완 셋 · 경로 모두 계획 폴더 기
  빨강 EOS 보류 대상 null (selftest: 117/119) ✗ [음성] |P| 2.5 GPa > 2 (세 가족) → EOS 필요 · 안정성 · 전자구조 대상 둘 다 null · 이완 구조는 진단 자료 (EF P1-6)
  빨강 LF 쓰기 (crash rc=1) ✗ [음성] 단일점 출력 하나 없음 → 누락으로 멈춘다 (실패로 세지 않는다)
  빨강 덮지 않음 prepare (selftest: 118/119) ✗ [음성] 계획이 있는 폴더에 다시 prepare → 덮지 않는다
  빨강 잡 입력 덮지 않음 (selftest: 118/119) ✗ [음성] 잡 입력이 이미 있고 다르면 덮지 않는다
  빨강 이완 구조 덮지 않음 (crash rc=1) ✗ [음성] 이완 구조 파일이 이미 있고 이번 출력에서 만든 것과 다르면 덮지 않는다
  빨강 reject 보존 (selftest: 117/119) ✗ [양성] reject — 검사에 걸린 출력 하나만 scf.out.rejected.1 로 옮김 (지우지 않음 · 통과한 출력은 그대로)
  빨강 reject 계획 고리 (selftest: 118/119) ✗ [음성] reject — 다른 계획의 판정 파일로 잡을 옮기지 않는다
깨기 73/73 빨강
