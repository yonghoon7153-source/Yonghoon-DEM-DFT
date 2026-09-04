# 원고 본문 스냅샷 — 2026-09-03

⚠ **이 파일의 목적은 하나: 다음 판과 diff 할 기준선을 만드는 것.**
저자가 보내온 텍스트를 **한 글자도 고치지 않고** 그대로 둔다.  논평은 다른 문서에 쓴다
(`docs/reviews/ms_si_v7_edit_sheet_20260901.md`).

★ **왜 이 파일이 오늘에야 생겼나** — 8월 말~9월 초에 문단별로 같이 읽었는데 그 읽기가
**대화에만 있었고 파일로 안 내려갔다.**  컨텍스트 압축에서 전부 소실됐고, 그래서
2026-09-03 에 저자가 *"달라진 거 알려줘"* 라고 했을 때 **대조할 기준선이 없었다.**
규칙 ④(정본은 밖으로 강제되지 않으면 새어나간다)의 실례다.
⇒ **앞으로 문단을 받으면 논평 전에 이 파일부터 갱신한다.**

⚠ 범위: **초록 · §1 서론 · §2 결과 (Figure 2 물성·펠릿 σ → Figure 3 SEM·SAICAS 까지)**.
이후 문단(수송 시뮬·집전체·셀 성능)은 미수록.
★ 문장별 판정은 `docs/reviews/ms_readthrough_20260903.md`.

---

## Abstract

Dry electrode fabrication eliminates solvent-based slurry preparation and the subsequent drying step, offering a sustainable route to all-solid-state battery (ASSB) cathodes. Polytetrafluoroethylene (PTFE), while enabling dry electrode fabrication through shear-induced fibrillation, is electronically insulating, prone to agglomeration during processing, and exhibits poor interfacial affinity toward metallic current collectors. Herein, we develop an integrated cathode architecture based on a multifunctional self-doped conducting polymer (SDCP) featuring a poly(3,4-ethylenedioxythiophene) backbone with covalently tethered sulfonate groups. At a fixed total binder content of 1 wt%, partial replacement of PTFE with SDCP preserves the essential fibrillar framework while simultaneously reinforcing electronic transport, recovering electrode cohesion, and improving mechanical resilience. Furthermore, the stainless steel current collector is coated with an SDCP–graphene composite layer to enhance interfacial adhesion and maintain efficient electron transport across the cathode/current collector interface. The integrated design delivers 83 mAh g−1 at 4C and 96.8% capacity retention over 1000 cycles at 2C, while sustaining stable cycling at 5 MPa and in a 5 mAh cm−2 anode-free pouch cell under a practical stack pressure of 2 MPa. The coordinated control of electronic transport, mechanical integrity, and interfacial adhesion offers a general design principle for high-performance dry-processed ASSBs under practical operating conditions.

## 1. Introduction

All-solid-state batteries (ASSBs) based on solid electrolytes (SEs) have emerged as promising next-generation energy-storage systems, offering improved safety and the potential for higher energy density than conventional lithium-ion batteries (LIBs).[1,2] Among the various inorganic SEs, sulfide-based materials are particularly attractive owing to their room-temperature ionic conductivities approaching those of liquid electrolytes and their favorable mechanical deformability, which enables intimate particle-to-particle contact through cold pressing without high-temperature sintering.[3–5] These characteristics make sulfide SEs well-suited for composite cathodes containing high fractions of active material (AM) and for the thick, high-loading electrode architectures required to maximize cell-level energy density.[6,7] However, unlike conventional porous electrodes permeated by a liquid electrolyte, sulfide-based composite cathodes rely entirely on solid–solid contacts among the AM, SE, conductive additive (CA), and binder to establish continuous ionic, electronic, and mechanical networks.[8–11] Consequently, seemingly minor inactive components can exert a disproportionate influence on electrode-level transport and structural integrity.[12]

Accordingly, the fabrication strategy of composite cathodes is as critical as the properties of their constituent materials. Conventional wet processing typically involves dispersing the electrode constituents and polymer binder in a solvent, casting the resulting slurry onto a current collector, and removing the solvent through a subsequent drying step.[13] For sulfide-based ASSBs, wet processing is particularly challenging because sulfide SEs are susceptible to chemical degradation upon exposure to conventional processing solvents, while binder migration and redistribution of CAs during drying can introduce local compositional heterogeneity.[14] In addition, solvent recovery and energy-intensive drying steps increase both the manufacturing complexity and environmental burden.[15] Dry processing therefore offers a compelling alternative by eliminating solvent use and subsequent drying, thereby minimizing solvent-induced degradation and enabling the direct fabrication of thick, freestanding composite cathodes.[16,17] This solvent-free approach, however, relies critically on a binder capable of providing sufficient mechanical integrity during electrode formation.

Polytetrafluoroethylene (PTFE) is widely used in dry-processed electrodes because shear-induced fibrillation forms a continuous fibrillar network that consolidates the electrode into a mechanically robust freestanding film, even at low binder contents.[16,18] However, this advantage is accompanied by intrinsic limitations. PTFE is electronically insulating, prone to binder-rich aggregation because of its low surface energy and nonpolar character, and susceptible to excessive fibrillation that partially covers AM and SE surfaces.[19,20] These features disrupt local electronic and ionic pathways and lead to heterogeneous particle contacts.[8,21] Moreover, its weak affinity toward metallic current collectors results in poor electrode–current collector adhesion and increased susceptibility to interfacial delamination.[22,23] These drawbacks become particularly detrimental at high current densities and low stack pressures, where continuous transport pathways and stable mechanical contact are critical.[24–27] Lowering the PTFE content alleviates these limitations but weakens the fibrillar network essential for the mechanical integrity of dry-processed electrodes.

Functional binders have emerged as an effective means of overcoming the passive and insulating nature of conventional binders by introducing additional transport or interfacial functions.[28] Hong et al. demonstrated that a Li+-conducting ionomer can facilitate ionic transport and strengthen interparticle adhesion in solvent-free sulfide composite cathodes, thereby improving contact retention during cycling.[29] Conductive-polymer binders provide a complementary approach by allowing the binder itself to participate in the electronic network rather than serving solely as a mechanical adhesive.[30–32] However, these individual functionalities do not fully satisfy the coupled requirements of dry-processed sulfide cathodes, where the binder must simultaneously preserve the fibrillar framework required for freestanding electrode formation, maintain continuous ionic and electronic pathways,[25,28] reinforce particle-level cohesion, and ensure stable contact with the metallic current collector.[23,33] Complete replacement of PTFE is therefore undesirable because its shear-induced fibrillation remains essential for dry-electrode integrity. A more effective strategy is to retain PTFE for long-range fibrillation while introducing a complementary binder that provides additional mechanical and electronic functions and can also stabilize the cathode/current collector interface.

Herein, we develop an integrated dry-processed cathode architecture based on a multifunctional self-doped conducting polymer (SDCP) that resolves the coupled transport and mechanical limitations of PTFE-bound sulfide composite cathodes through spatially coordinated function integration. SDCP consists of a conjugated poly(3,4-ethylenedioxythiophene) backbone bearing covalently tethered sulfonate groups, enabling intrinsic electronic conduction without a separately incorporated insulating polyanion. Rather than fully replacing PTFE, half of the PTFE is substituted with SDCP at a fixed total binder content of 1 wt%, thereby preserving the long-range fibrillar network required for freestanding electrode formation while introducing particle-level cohesion, reinforced electronic connectivity, and improved elastic recovery. The same polymer is further incorporated into an ultrathin SDCP–graphene composite coating on the stainless steel current collector, extending its functionality from the electrode interior to the cathode/current collector interface. This integrated design delivers 83 mAh g−1 at 4C and 96.8% capacity retention over 1000 cycles at 2C, while sustaining stable operation at 5 MPa and in a 5 mAh cm−2 anode-free pouch cell under 2 MPa.

## 2. Results and Discussion

Dry-processed sulfide composite cathodes rely on PTFE fibrillation to form mechanically robust freestanding films, but this function is accompanied by two inherent limitations (Figure 1). Within the electrode, electronically insulating PTFE can agglomerate into fibril-rich domains, disrupting uniform particle contact and electronic conduction. At the cathode/current collector interface, the weak affinity of nonpolar PTFE toward stainless steel (SUS) leads to poor adhesion and increased susceptibility to delamination and contact-resistance growth. To address both bulk and interfacial limitations, we introduced an integrated SDCP-based design in which half of the PTFE was replaced with SDCP at a fixed total binder content of 1 wt%, retaining the fibrillar network while reinforcing particle-level cohesion and electronic connectivity. In parallel, the SUS current collector was coated with an ultrathin SDCP–graphene layer to reinforce cathode–current collector adhesion without sacrificing electronic transport. This architecture therefore assigns complementary functions to PTFE and SDCP within the cathode while extending the same conducting polymer to stabilize the current collector interface.

The molecular structure and physicochemical characteristics of SDCP were first examined to establish the basis for its multifunctional binder behavior. As illustrated in Figure 2a, the polymer was designed by introducing a covalently tethered sulfonate side chain onto an EDOT precursor, followed by oxidative polymerization and ion exchange to obtain the final self-doped conducting polymer. Detailed synthetic procedures and intermediate structures are provided in Supplementary Note 1 (Figures S1 and S2). The as-synthesized polymer consists of micrometer-sized granular particles prior to electrode processing (Figure 2b). Raman spectroscopy confirms formation of the conjugated PEDOT backbone, as evidenced by the characteristic symmetric and asymmetric Cα=Cβ stretching modes together with the Cβ–Cβ stretching and Cα–Cαʹ inter-ring vibrations (Figure 2c).[34,35] Additional C–O–C and CH2 bands are consistent with the ethylenedioxy bridge and the alkyl side chain bearing the sulfonate functionality. The chemical state of this side chain was further examined by Fourier transform infrared (FT-IR) spectroscopy in Figure 2d. Asymmetric and symmetric SO3− stretching bands appear at 1185 and 1042 cm−1, respectively, together with an S=O band characteristic of the undissociated SO3H group,[32] while only weak absorption is observed in the O–H region (3500–2500 cm−1). The coexistence of these bands indicates that the tethered sulfonic acid side chains are partially dissociated, so that a fraction of them is present as fixed SO3− anions. These fixed anionic groups provide internal charge compensation for the oxidized conjugated backbone, consistent with the self-doped conducting character of SDCP.[36]

The tethered sulfonate functionality also provides a chemical basis for stronger interaction with the AM surface. Density functional theory (DFT) calculations comparing representative SDCP and PTFE segments adsorbed on AMs are shown in Figure 2e, with the corresponding computational models and calculation parameters provided in Figure S3 and Table S1, respectively.[28] The stronger interaction expected for SDCP originates from its polar sulfonate moieties, which can interact more effectively with exposed surface sites of LiNi0.8Co0.1Mn0.1O2 (NCM811) than non-polar PTFE.[19] Additional text related to DFT. This stronger surface affinity is also reflected in the post-mixing morphology. Ball milling breaks the initially micrometer-sized SDCP particles into finer domains that become uniformly distributed over the NCM surface (Figures 2f and S5). Such surface-associated dispersion suggests that SDCP preferentially occupies particle-level contact regions, minimizing segregation into binder-rich domains and thereby promoting more effective interparticle binding.


### §2 계속 — Figure 2g (기계) · 2h/2i (펠릿 σ)

Beyond its favorable particle-level distribution, SDCP also exhibits mechanical properties distinct from those of PTFE. Atomic force microscopy (AFM) force–distance measurements on compacted binder films reveal a substantially higher Young's modulus (E) for SDCP than for PTFE (Figure 2g), with the corresponding PTFE modulus map and statistical distributions provided in Figures S6 and S7. The average E increases from 1.8 GPa for PTFE to 9.0 GPa for SDCP, indicating that SDCP can serve as a mechanically reinforcing binder phase within the composite cathode and provide greater resistance to local deformation. Importantly, this mechanical reinforcement is not achieved at the expense of ionic and electronic transport. To directly assess the influence of each binder on the SE, Li6PS5Cl (LPSCl) electrolyte was mixed with PTFE or SDCP at a fixed 9:1 weight ratio, and the ionic and electronic conductivities were evaluated by electrochemical impedance spectroscopy (EIS) and direct current (DC) polarization, respectively. Pristine LPSCl exhibits an ionic conductivity (σion) of 3.57 mS cm−1, which decreases markedly to 0.97 mS cm−1 upon mixing with PTFE, whereas the LPSCl–SDCP mixture retains a substantially higher σion of 2.86 mS cm−1 (Figures 2h and S8).[37] An even more pronounced contrast is observed for electronic transport. The electronic conductivity (σele) decreases from 0.30 × 10−7 S cm−1 for pristine LPSCl to 0.12 × 10−7 S cm−1 with PTFE, but increases more than fivefold to 1.53 × 10−7 S cm−1 in the presence of SDCP (Figures 2i and S9). These results underscore the complementary roles of the two binders. PTFE primarily provides fibrillar mechanical integrity, whereas SDCP adds mechanical reinforcement while preserving Li+ transport and enhancing electronic connectivity. Combined with its strong affinity for NCM and particle-level dispersion, SDCP effectively compensates for the transport and cohesion losses associated with reduced PTFE content.

### §2 계속 — DBE/SBE 정의 + 대조 실험

Given these complementary roles, a dual-binder electrode (DBE) containing 0.5 wt% PTFE and 0.5 wt% SDCP was compared with a conventional single-binder electrode (SBE) containing 1.0 wt% PTFE at the same total binder content. Control experiments further demonstrate that both components are necessary for successful dry-electrode formation and stable operation. SDCP alone cannot produce a mechanically coherent freestanding electrode during hot rolling (Figure S10), confirming that PTFE fibrillation remains indispensable for establishing the long-range structural framework. Conversely, reducing the PTFE content to 0.5 wt% without SDCP results in incomplete dough formation and progressive capacity decay during cycling (Figures S11 and S12), indicating insufficient mechanical cohesion and contact retention. These observations establish a clear division of roles between the two binders, with PTFE providing the fibrillar backbone required for electrode formation and SDCP compensating for the cohesion and transport penalties associated with reduced PTFE content.[38] This complementary binder architecture therefore enables a lower PTFE fraction without sacrificing the structural integrity required for subsequent electrode processing and cycling.

### §2 계속 — Figure 3a,b (XRD · SEM · AFM 나노압입)

X-ray diffraction (XRD) analysis confirmed that incorporation of SDCP does not induce detectable crystalline secondary phases during processing, with both SBE and DBE retaining only the characteristic reflections of NCM and LPSCl (Figure S13). The effect of binder redistribution on the electrode structure is evident from the scanning electron microscopy (SEM) analyses in Figure 3a,b. Top-view images and corresponding F elemental maps show extended F-rich fibrillar domains in the SBE, whereas the DBE exhibits a markedly more homogeneous F distribution. Reducing the PTFE content therefore suppresses localized fibril-rich regions, while the dispersed SDCP compensates for the reduced fibrillar fraction through particle-level binding. This more balanced binder distribution translates into a denser electrode architecture, as cross-sectional SEM images reveal fewer voids and more intimate interparticle contacts in the DBE than in the SBE (Figure 3b).[39] The improved microstructural contact is accompanied by a more elastic mechanical response. AFM nanoindentation shows a smaller irreversible penetration depth for the DBE (Figure S14), increasing the elastic recovery from 0.69 for the SBE to 0.82 for the DBE (Figure S15).[25] These results indicate that the dual-binder design not only redistributes the binder phase more uniformly but also improves the ability of the electrode to recover from local deformation and maintain particle contacts.

### §2 계속 — Figure 3c,d (SAICAS)

The improvement in electrode-level mechanical integrity was further quantified by SAICAS, which probes the resistance of the electrode interior to horizontal cutting at a fixed depth (Figure 3c). Reducing the PTFE content from 1.0 to 0.5 wt% nearly halves the horizontal force from 0.33 to 0.17 N mm−1, directly demonstrating the loss of internal cohesion caused by weakening the fibrillar network (Figure 3d). Remarkably, introducing 0.5 wt% SDCP increases the force to 0.37 N mm−1, exceeding even that of the 1.0 wt% PTFE electrode despite containing only half as much PTFE. This quantitative recovery shows that SDCP does more than compensate for reduced fibrillation; it reinforces the particle-level contact network sufficiently to restore, and slightly enhance, the overall cohesive integrity of the dry-processed electrode.

---

## 참고문헌 번호 — 이 판에서 관측된 자리 (⚠ 목록 미확보)

| 번호 | 이 판에서 달린 자리 |
|---|---|
| [19] | PTFE 비극성 · 과도 fibrillation (서론) · DFT 문단의 NCM811 대비 |
| [23] | 집전체 접착 · 계면 |
| [28] | *"Functional binders have emerged…"* · **DFT 계산 파라미터** (Figure S3/Table S1) |
| [29] | **Hong et al.** Li⁺-conducting ionomer |
| [30–32] | 전도성 고분자 바인더 |
| [32] | FT-IR 의 미해리 SO₃H |
| **[34,35]** | **Raman** (PEDOT 백본 귀속) |
| **[36]** | **self-doped conducting character** |

⚠⚠ **원장(CL-61·CL-62)과 편집 시트 §2-6·§2-7 은 옛 번호로 못박혀 있다**:
`[34] Raman · [35] self-doping 원전(Patil) · [36] Jung · [37] Hong`.
이 판에서는 **Raman 이 [34,35] 로 둘**이고 **self-doping 이 [36]** 이다
⇒ **[35] 이후가 한 칸씩 밀린 것으로 보인다** (Patil [35]→[36] · Jung [36]→[37]).
★ **인용 위치로 한 역추정이다.  참고문헌 목록을 받아 확정한 뒤 원장·시트를 일괄 정정할 것.**

---

# ★★ 판간 diff — 옛 판(09-01/09-02) → 이 판(09-03)

옛 판 원문은 **세션 전사 기록에서 복구**했다 (`_transcript_recovered_paragraphs_20260903.txt`,
39,061 줄에서 원고 산문 48 문단 추출; 항목 38 = 09-01 23:05 Results 도입 · 39 = 09-02 01:19
Figure 2 분자 문단).  ⚠ 압축으로 대화에서 사라졌던 것을 전사에서 되살린 것이다 —
**전사 기록이 실질적 백업이라는 사실을 기록해 둔다.**

## ⓵ ★★ FT-IR 해석이 약해졌다 — **가장 큰 변화이고 우리에게 직접 걸린다**

| | 09-02 판 | **09-03 판** |
|---|---|---|
| S=O 밴드 | (없음) | **`an S=O band characteristic of the undissociated SO3H group`[32]** 추가 |
| 해리 상태 | *"exist **predominantly in the deprotonated state**"* | *"**partially dissociated**, so that **a fraction** of them is present as fixed SO3− anions"* |
| 결론 강도 | *"thereby **establishing** the self-doped conducting character"* | *"**consistent with** the self-doped conducting character"* |

⇒ **`predominantly deprotonated` → `partially dissociated`.**  주장이 크게 약해졌고,
`establishing` → `consistent with` 로 결론 동사도 내려갔다.

### 이것이 우리에게 갖는 함의 셋

**ⓐ ★ 오늘 Patil 카드와 같은 방향이다.**  `patil1987_self_doped_conducting_polymers` §ESR:
Curie 스핀 **1 spin / 1500 monomer** ⇒ as-synthesized 는 **사실상 중성**.  CL-61 이 이것을
*"`sdcp_master.md` §3.2 의 'doped 가 실물의 기본 상태' 와 **긴장 관계**"* 로 기록했는데,
**원고가 이미 그쪽으로 물러섰다.**  긴장이 아니라 **원고가 먼저 정정한 것**이다.

**ⓑ ⛔ 따라서 `docs/sdcp_master.md` §3.2 를 원고에 맞춰야 한다.**  원고가 *"partially
dissociated / a fraction"* 이라고 쓰는데 우리 문서가 *"doped 가 기본 상태"* 라고 하면 어긋난다.
⇒ **원고가 앞서 있고 우리 문서가 뒤처진 상태다** (규칙 ④ 의 반대 방향 사례).

**ⓒ ⚠ `σ_SDCP = 250 S/cm` 에도 함의가 있다.**  부분 도핑이면 완전 도핑 가정에서 나온 값보다
**낮은 전도도**가 물리적으로 자연스럽다.  ⇒ 250 이 저자 지정값(CL-61)이라는 지위는 그대로지만,
**이 문장 변화가 그 값을 지지하는 방향은 아니다.**  σ_SDCP 감도 스윕(3×3 C₂ 축 · 판별 팔)의
필요성이 한 겹 더 강해진다.

## ⓶ ✅ 참고문헌 `[35] → [36]` 이 **원문으로 확정됐다**

```
09-02 판:  ... establishing the self-doped conducting character of SDCP.[35]
09-03 판:  ... consistent with the self-doped conducting character of SDCP.[36]
```
그리고 Raman 이 `[34]` → **`[34,35]`** 로 하나 늘었다.
⇒ **[35] 자리에 문헌 하나가 삽입되어 이후가 +1 밀렸다** — 추정이 아니라 **원문 대조로 확정**이다.
· Patil(self-doping 원전) **[35] → [36]**
· Jung(선례) **[36] → [37]**  (이 판 본문에서 `[37]` 로 확인)
· Hong(역할분담) **[37] → [38]**  (이 판 본문에서 `[38]` 로 확인)
⇒ **CL-61 · CL-62 · 편집 시트 §2-6 · §2-7 의 번호를 +1 한다.**

## ⓷ DFT 문단이 **신설**됐다 (09-02 판에는 없었다)

`Figure 2e` + `Figure S3` + `Table S1` + `[28]` + 자리표시자 `Additional text related to DFT.`
⚠ 우리 `E_bind` 는 `INVALID_WRONG_MONOMER_recompute_pending` 이다 — Figure 2e 가 어느 계산인지
확인이 필요하다 (CL-61 §확인대기).

## ⓸ Ball milling 문장이 **신설**됐다 (09-02 판에는 없었다)

> *"Ball milling breaks the initially micrometer-sized SDCP particles into finer domains that
> become uniformly distributed over the NCM surface (Figures 2f and S5)."*

⚠ 우리 `seed_sdcp` docstring 이 **그 그림 번호를 이미 참조**하는데(`Figure 2f · S5`),
**문장 자체는 09-03 에 새로 생겼다.**  ⇒ 우리 코드가 원고보다 먼저 그 그림을 읽고 있었다 —
정합이지만, **`surface_frac` 이 이미지에서 읽히지 않는다는 사실은 그대로**다.

## ⓹ 표기·문장 다듬기 (판정 무관)

· `Cα–Cα` → `Cα–Cαʹ` (프라임 추가)
· `further verify the ethylenedioxy moiety` → `are consistent with the ethylenedioxy bridge` (약화)
· `Oxidative polymerization and subsequent ion exchange then yielded the final SDCP.` 문장이
  Figure 2a 문장에 **병합**됨

---

### §2 계속 — ★ 우리 파트 (DEM/MPM + 복셀 수송)  [저자 제공 2026-09-04]

Beyond this mechanical role, the electronically conducting SDCP is expected to modify charge-transport pathways within the composite cathode. To directly evaluate this effect, three-dimensional SBE and DBE microstructures were reconstructed using a discrete element method (DEM) coupled with the material point method (MPM), in which DEM generated the particle packing and MPM resolved its subsequent plastic densification; the model geometries and material parameters are summarized in Figure S16 and Table S2, respectively.[40,41] The effective conductivities of the reconstructed microstructures were subsequently computed using a voxel-based finite-volume transport solver. Because both electrodes share an identical DEM-generated particle skeleton, the differences described below arise solely from their binder phases. Although both electrodes maintain fully percolated electronic networks owing to their identical vapor-grown carbon fiber (VGCF) contents, replacing half of the electronically insulating PTFE with uniformly dispersed, electronically conducting SDCP increases the CA density around the AM particles, as visualized by the local CA density normalized to the SBE median (Figure 4a). Indeed, most AM particles in the DBE exhibit CA densities above the SBE median, indicating that this enrichment extends throughout the electrode rather than being confined to localized regions. Correspondingly, the median number of CA contacts per AM particle, defined as the number of distinct CA entities within a 0.15 μm shell around each particle, increases from 74 for the SBE to 86 for the DBE (Figure 4b), reflecting the additional conductive phase introduced by SDCP.[42] Consistently, the simulated effective σele increases from 53.99 to 70.61 mS cm−1 (Figure 4b). The corresponding ionic and electronic current-density fields are presented in Figures S17 and S18, respectively, revealing comparable ionic current distributions in the two electrodes but an overall higher electronic current density in the DBE. Taken together, these results demonstrate that partially replacing insulating PTFE with conducting SDCP increases the local CA density around the AM particles, thereby reinforcing electronic transport throughout the composite cathode.

**저자 1차 개정 (2026-09-04, 문장 ②)** — `reconstructed` → `constructed` · `coupled with` → `followed by`:

> To directly evaluate this effect, three-dimensional SBE and DBE microstructures were constructed by a discrete element method (DEM) simulation of powder packing followed by a material point method (MPM) simulation of plastic densification

⇒ 잔여 권고: `powder packing` **`and compaction`** 추가 · 뒷절(`Figure S16`/`Table S2`/`[40,41]`) 복원.
