## acceptance — publication (G2RR-02)
| label | Codex status · full_q · I_bottom | ours status · full_q · I_bottom | ours τ hertz | ours stop verdict (first reason) |
| baseline | done · 0.00400538 · 0.0200268809166404 | done · 0.00400538 · 0.0200268809166404 | OK 10.980805104698454 | True · ok |
| missing_full_cert | failed · None · None | failed · None · None | NOT_COMPUTED None | False · ① hertzian: 파일 없음; physics: 파일 없음; per-mode 산출물이 하나도 없다; 읽기 실패 (FileNotFoundError) |
| full_cert_from_cf | done · 0.00400538 · 0.1963495408493623 | failed · None · None | NOT_COMPUTED None | False · ① hertzian: 파일 없음; physics: 파일 없음; per-mode 산출물이 하나도 없다; 읽기 실패 (FileNotFoundError) |
| full_cert_from_h12 | done · 0.00400538 · 0.025675122317963317 | failed · None · None | NOT_COMPUTED None | False · ① hertzian: 파일 없음; physics: 파일 없음; per-mode 산출물이 하나도 없다; 읽기 실패 (FileNotFoundError) |
| missing_cf_cert | done · 0.00400538 · 0.0200268809166404 | failed · None · None | NOT_COMPUTED None | False · ① hertzian: 파일 없음; physics: 파일 없음; per-mode 산출물이 하나도 없다; 읽기 실패 (FileNotFoundError) |
| cf_bad_conservation | done · 0.00400538 · 0.0200268809166404 | failed · None · None | NOT_COMPUTED None | False · ① hertzian: 파일 없음; physics: 파일 없음; per-mode 산출물이 하나도 없다; 읽기 실패 (FileNotFoundError) |
| missing_constr_cert | done · 0.00400538 · 0.0200268809166404 | failed · None · None | NOT_COMPUTED None | False · ① hertzian: 파일 없음; physics: 파일 없음; per-mode 산출물이 하나도 없다; 읽기 실패 (FileNotFoundError) |

## acceptance — stamp (G2RR-01)
| label | Codex accepted · generation | ours accepted · generation · problem |
| control | True · g2 | True · g2 ·  |
| all_unknown | True · g2 | False · None · FillRefusal: lhs00_000: τ P4 — 세대 도장 대조 (G2RR-01 · pipeline_service.provenance_generation_problem): 레코드 세대 'g2' · 도장 psi_placement_physics='unrecognized' ≠ 레코드에서 유도한 'multiply' · 도장 electrode_model='u… |
| all_null | True · g2 | False · None · FillRefusal: lhs00_000: τ P4 — 세대 도장 대조 (G2RR-01 · pipeline_service.provenance_generation_problem): 레코드 세대 'g2' · 도장 psi_placement_physics=None ≠ 레코드에서 유도한 'multiply' · 도장 electrode_model=None ≠ 레코드에서… |
| one_null_legacy_shape | True · inferred_legacy | False · None · FillRefusal: lhs00_000: τ P4 — 세대 도장 대조 (G2RR-01 · pipeline_service.provenance_generation_problem): 레코드 세대 'inferred_legacy' · 확인된 역사 도장 스키마 (194 v1.2 · 8 키) 가 아니다 — 남는 키 ['electrode_model'] · 없는 키 []… |
| g2_declares_legacy | True · g2 | False · None · FillRefusal: lhs00_000: τ P4 — 세대 도장 대조 (G2RR-01 · pipeline_service.provenance_generation_problem): 레코드 세대 'g2' · 도장 psi_placement_physics='legacy_divide' ≠ 레코드에서 유도한 'multiply' · 도장 electrode_model='… |
| stamp_absent_keys | False · None | False · None · FillRefusal: lhs00_000: τ P4 — 세대 도장 대조 (G2RR-01 · pipeline_service.provenance_generation_problem): 레코드 세대 'g2' · 도장에 psi_placement_physics 없음 (부분 결손) · 도장에 electrode_model 없음 (부분 결손) · 도장에 area_rule_… |

## reread_extra (G2RR-03)
| label | Codex rc · verdict · queue_n | ours rc · verdict · queue_n · queue_n_unique · first C8 fail |
| baseline | 0 · PASS · 194 | 0 · PASS · 194 · 194 ·  |
| queue_empty | 0 · PASS · 0 | 1 · FAIL · 0 · 0 · C8 봉인 감사 (30: 등록 manifest plan.queue 가 비었다 (빈 목록)) |
| plan_absent | 0 · PASS · 0 | 1 · FAIL · 0 · 0 · C8 봉인 감사 (30: 등록 manifest 에 plan 이 없다) |
| queue_duplicate | 0 · PASS · 194 | 1 · FAIL · 195 · 194 · C8 봉인 감사 (3: 등록 큐 행 수 195 ≠ 194) |

## adversarial (G2R-02 · G2R-03 · GEN2-01 regression)
| dead-end high | Codex G · method · first attempt | ours G · method · first attempt |
| 1e+06 | 15000.5 · cg · pass | 15000.5 · cg · pass |
| 1e+08 | 15000.5 · cg · pass | 15000.500000014901 · cg · pass |
| 1e+10 | 15000.499998092651 · cg · pass | 15000.499998092651 · cg · pass |
| 1e+12 | 15000.5 · cg · pass | 15000.5 · cg · pass |
| 1e+14 | 15000.5 · spsolve_fallback · certificate_failed | 15000.5 · spsolve_fallback · certificate_failed |
| direct high | Codex G · status/reason | ours G · status/reason |
| 1e+06 | 0.9999990001088008 · computed/None | 0.9999990001088008 · computed/None |
| 1e+08 | 1.0 · computed/None | 1.0 · computed/None |
| 1e+10 | 1.0 · computed/None | 1.0 · computed/None |
| 1e+12 | 1.0 · computed/None | 1.0 · computed/None |
| 1e+14 | 1.0 · computed/None | 1.0 · computed/None |
| 1e+15 | 1.0 · computed/None | 1.0 · computed/None |
| 1e+16 | None · not_computed/current_conservation_failed | None · not_computed/current_conservation_failed |
| zero_Rc (GEN2-01) | None · zero_resistance_requires_contraction | None · zero_resistance_requires_contraction |
| baseline statuses · tau2 | {'hertz': 'OK', 'physics': 'OK', 'hertz_h12': 'OK'} · {'hertz': 32.302633834659325, 'physics': 6.348896384761871, 'hertz_h12': 29.803150343048397} | {'hertz': 'OK', 'physics': 'OK', 'hertz_h12': 'OK'} · {'hertz': 32.302633834659325, 'physics': 6.348896384761871, 'hertz_h12': 29.803150343048397} |
| generation mutant | Codex statuses · stop9 n | ours statuses · stop9 n |
| H0 bulk relabelled sphere_segment | ['NOT_COMPUTED'] · 1 | ['NOT_COMPUTED'] · 1 |
| H0 constriction relabelled Mikic | ['NOT_COMPUTED'] · 1 | ['NOT_COMPUTED'] · 1 |
| unknown electrode all | ['NOT_COMPUTED'] · 3 | ['NOT_COMPUTED'] · 3 |
| unknown area | ['NOT_COMPUTED'] · 1 | ['NOT_COMPUTED'] · 1 |
| unknown psi | ['NOT_COMPUTED'] · 1 | ['NOT_COMPUTED'] · 1 |
| missing psi | ['NOT_COMPUTED'] · 1 | ['NOT_COMPUTED'] · 1 |
| missing area | ['NOT_COMPUTED'] · 1 | ['NOT_COMPUTED'] · 1 |
| physics bulk relabelled sphere_segment | ['NOT_COMPUTED'] · 1 | ['NOT_COMPUTED'] · 1 |

## numerics (G2R-03 regression · exact G 1.45)
| high | Codex G · method · rel_err · cert_problem | ours G · method · rel_err · cert_problem | same G bits |
| 1e+09 | 1.4499997615814209 · cg · -1.6442660633053663e-07 · None | 1.4499997615814209 · cg · -1.6442660633053663e-07 · None | True |
| 1e+10 | 1.45 · cg · 0.0 · None | 1.45 · cg · 0.0 · None | True |
| 1.15e+10 | 1.45 · cg · 0.0 · None | 1.45 · cg · 0.0 · None | True |
| 1.16e+10 | 1.45 · spsolve_fallback · 0.0 · None | 1.45 · spsolve_fallback · 0.0 · None | True |
| 1.165e+10 | 1.45 · cg · 0.0 · None | 1.45 · cg · 0.0 · None | True |
| 1.17e+10 | 1.45 · cg · 0.0 · None | 1.45 · cg · 0.0 · None | True |
| 1.18e+10 | 1.45 · spsolve_fallback · 0.0 · None | 1.45 · spsolve_fallback · 0.0 · None | True |
| 1.2e+10 | 1.45 · spsolve_fallback · 0.0 · None | 1.45 · spsolve_fallback · 0.0 · None | True |
| 1.3e+10 | 1.45 · spsolve_fallback · 0.0 · None | 1.45 · spsolve_fallback · 0.0 · None | True |
| 1.4e+10 | 1.45 · spsolve_fallback · 0.0 · None | 1.45 · spsolve_fallback · 0.0 · None | True |
| 1.5e+10 | 1.45 · spsolve_fallback · 0.0 · None | 1.45 · spsolve_fallback · 0.0 · None | True |
| 1e+11 | 1.45 · spsolve_fallback · 0.0 · None | 1.45 · spsolve_fallback · 0.0 · None | True |
| 1e+14 | 1.45 · spsolve_fallback · 0.0 · None | 1.45 · spsolve_fallback · 0.0 · None | True |
worst |rel_err| Codex 1.6442660633053663e-07 · ours 1.6442660633053663e-07

## real_beds (graph solves · Codex direct build/solve)
| bed | arm | mode | Codex [G, q] | ours [G, q] | rel diff q | bits same |
| real14 | H0 | full | [1.7352982093338443, 0.02102105544822832] | [1.7352982093338438, 0.021021055448228312] | 3.3306690738754696e-16 | False |
| real14 | H0 | bulk_only | [9.141475432595136, 0.11073800509537093] | [9.141475432595128, 0.11073800509537082] | 9.992007221626409e-16 | False |
| real14 | H0 | constriction_only | [2.2224946363858944, 0.026922855526251444] | [2.2224946363858895, 0.026922855526251382] | 2.3314683517128287e-15 | False |
| real14 | g1_mul | full | [3.071795744444935, 0.03721111928905704] | [3.071795744444918, 0.03721111928905684] | 5.440092820663267e-15 | False |
| real14 | g1_mul | bulk_only | [9.141475432595136, 0.11073800509537093] | [9.141475432595128, 0.11073800509537082] | 9.992007221626409e-16 | False |
| real14 | g1_mul | constriction_only | [None, None] | [None, None] | None | True |
| real14 | g2 | full | [2.611904685098846, 0.031640090974350395] | [2.611904685098844, 0.03164009097435037] | 8.881784197001252e-16 | False |
| real14 | g2 | bulk_only | [9.141475432595136, 0.11073800509537093] | [9.141475432595128, 0.11073800509537082] | 9.992007221626409e-16 | False |
| real14 | g2 | constriction_only | [None, None] | [None, None] | None | True |
| real14 | H12 | full | [2.0589229236560325, 0.02494138051258444] | [2.0589229236560413, 0.024941380512584547] | 4.218847493575595e-15 | False |
| real14 | H12 | bulk_only | [6.311858113864062, 0.07646058681972646] | [6.311858113864064, 0.07646058681972648] | 2.220446049250313e-16 | False |
| real14 | H12 | constriction_only | [3.456724270370308, 0.04187406646641182] | [3.456724270370286, 0.041874066466411564] | 6.106226635438361e-15 | False |
| case15 | H0 | full | [0.1704582413153875, 0.0003263508259103751] | [0.1704582411149847, 0.00032635082552669387] | 1.175671004993717e-09 | False |
| case15 | H0 | bulk_only | [2.0482865289973162, 0.003921546974091811] | [2.048286528780592, 0.003921546973676881] | 1.0580780696045622e-10 | False |
| case15 | H0 | constriction_only | [0.18629207582381926, 0.00035666549376849304] | [0.1862920759779336, 0.0003566654940635527] | 8.272726947922138e-10 | False |
| case15 | g1_mul | full | [0.18953847622782305, 0.0003628808896619785] | [0.189538475721984, 0.0003628808886935244] | 2.6687932974667206e-09 | False |
| case15 | g1_mul | bulk_only | [2.0482865289973162, 0.003921546974091811] | [2.048286528780592, 0.003921546973676881] | 1.0580780696045622e-10 | False |
| case15 | g1_mul | constriction_only | [None, None] | [None, None] | None | True |
| case15 | g2 | full | [0.189207513265139, 0.00036224724452177176] | [0.1892075130340654, 0.00036224724407936984] | 1.2212706401726336e-09 | False |
| case15 | g2 | bulk_only | [2.0482865289973162, 0.003921546974091811] | [2.048286528780592, 0.003921546973676881] | 1.0580780696045622e-10 | False |
| case15 | g2 | constriction_only | [None, None] | [None, None] | None | True |
| case15 | H12 | full | [0.18065214400217935, 0.0003458675622993724] | [0.1806521436939834, 0.00034586756170931586] | 1.7060187706974261e-09 | False |
| case15 | H12 | bulk_only | [1.369817908401033, 0.002622584876529197] | [1.369817908500988, 0.0026225848767205662] | 7.296963033809334e-11 | False |
| case15 | H12 | constriction_only | [0.2088999082862266, 0.000399949319409395] | [0.20889990916624163, 0.00039994932109422784] | 4.212615811738374e-09 | False |
| bed | arm | Codex clamp · floor · n_zero_R (constr) | ours |
| real14 | H0 | 0 · 0 · 0 | 0 · 0 · 0 |
| real14 | g1_mul | 7487 · 43 · 7528 | 7487 · 43 · 7528 |
| real14 | g2 | 2607 · 22 · 2628 | 2607 · 22 · 2628 |
| real14 | H12 | 0 · 0 · 0 | 0 · 0 · 0 |
| case15 | H0 | 0 · 0 · 0 | 0 · 0 · 0 |
| case15 | g1_mul | 1524 · 19 · 1543 | 1524 · 19 · 1543 |
| case15 | g2 | 304 · 8 · 312 | 304 · 8 · 312 |
| case15 | H12 | 0 · 0 · 0 | 0 · 0 · 0 |
