// Claude draft — 27장, 기준본(cascade_revised, 24장) 스타일 모사 + 편집 지시서 반영판.
// 스타일: 큰 navy 섹션 타이틀 / 우상단 이탤릭 부제 / ■ 헤드라인 / 파스텔 박스 / 하단 navy 테이크어웨이.
const pptxgen = require("pptxgenjs");
const REPO="/home/user/Yonghoon-DEM-DFT/";
const M="/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/82ea256b-12bc-5a75-994e-7718d79c71ba/scratchpad/media/";
const NAVY="1F4E79", INK="262626", MUT="7F7F7F", RED="9E2A2B", AMB="B26A00", GRN="2E7D32", BLU="0070C0";
const TB="D9E1F2", TA="FFF4E0", TG="E5F2E6", TSOFT="F2F2F2", RULE="BFBFBF";
const W=10,H=7.5;
const p=new pptxgen(); p.defineLayout({name:"L43",width:W,height:H}); p.layout="L43";
let pg=0;
function base(section, topright, headline, notes){
  pg+=1; const s=p.addSlide();
  s.addText(section,{x:0.6,y:0.28,w:5.5,h:0.6,fontFace:"Arial",fontSize:28,bold:true,color:NAVY,margin:0});
  if(topright) s.addText(topright,{x:5.0,y:0.34,w:4.4,h:0.3,fontFace:"Arial",fontSize:9,italic:true,color:MUT,align:"right",margin:0});
  s.addShape(p.ShapeType.line,{x:0.6,y:0.95,w:8.8,h:0,line:{color:RULE,width:1}});
  if(headline){
    s.addShape(p.ShapeType.rect,{x:0.62,y:1.13,w:0.12,h:0.12,fill:{color:RED}});
    s.addText(headline,{x:0.88,y:1.02,w:8.5,h:0.35,fontFace:"Arial",fontSize:14,bold:true,color:INK,margin:0});
  }
  s.addText("HANYANG UNIVERSITY",{x:0.6,y:7.05,w:2.6,h:0.3,fontFace:"Arial",fontSize:8.5,bold:true,color:NAVY,margin:0});
  s.addText("Battery Materials Lab.",{x:3.6,y:7.05,w:2.8,h:0.3,fontFace:"Arial",fontSize:8.5,color:MUT,align:"center",margin:0});
  s.addText(String(pg),{x:9.15,y:7.05,w:0.4,h:0.3,fontFace:"Arial",fontSize:9,color:MUT,align:"right",margin:0});
  if(notes) s.addNotes(notes);
  return s;
}
function take(s,txt,y){ s.addText(txt,{x:0.6,y:(y||6.35),w:8.8,h:0.4,fontFace:"Arial",fontSize:12.5,bold:true,color:NAVY,align:"center",margin:0}); }
function soft(s,x,y,w,h,fill,line){ s.addShape(p.ShapeType.roundRect,{x:x,y:y,w:w,h:h,rectRadius:0.07,fill:{color:fill},line:{color:line||NAVY,width:1}}); }
function img(s,path,x,y,w,h,capt){ s.addImage({path:path,x:x,y:y,w:w,h:h,sizing:{type:"contain",w:w,h:h}});
  if(capt) s.addText(capt,{x:x,y:y+h+0.03,w:w,h:0.28,fontFace:"Arial",fontSize:8.5,italic:true,color:MUT,align:"center",margin:0}); }
const SRC=(s,t)=>s.addText(t,{x:5.0,y:6.78,w:4.4,h:0.24,fontFace:"Arial",fontSize:7.5,color:MUT,align:"right",margin:0});

// ═ 1 표지 ═
{ pg+=1; const s=p.addSlide();
  s.addText("August 2026",{x:0.6,y:0.5,w:3,h:0.3,fontFace:"Arial",fontSize:11,color:MUT,margin:0});
  s.addText("Research Seminar",{x:0.6,y:1.5,w:8.8,h:0.7,fontFace:"Arial",fontSize:32,bold:true,color:NAVY,margin:0});
  s.addText("A gated MLIP-to-DFT screening cascade for LPSCl modification",{x:0.6,y:2.7,w:8.8,h:0.9,fontFace:"Arial",fontSize:21,bold:true,color:INK,margin:0});
  s.addText("From curated substitutions to auditable decisions",{x:0.6,y:3.6,w:8.8,h:0.35,fontFace:"Arial",fontSize:13,italic:true,color:MUT,margin:0});
  s.addText("Yonghoon An",{x:0.6,y:4.9,w:8.8,h:0.35,fontFace:"Arial",fontSize:14,bold:true,color:INK,margin:0});
  s.addText("Division of Materials Science & Engineering, Hanyang University\n(E-mail : yonghoon71@hanyang.ac.kr)",{x:0.6,y:5.28,w:8.8,h:0.55,fontFace:"Arial",fontSize:10.5,color:MUT,margin:0});
  s.addText("MLIP screening · physical gates · targeted validation",{x:0.6,y:6.1,w:8.8,h:0.3,fontFace:"Arial",fontSize:10.5,color:NAVY,margin:0});
  s.addText("HANYANG UNIVERSITY",{x:0.6,y:6.95,w:3,h:0.3,fontFace:"Arial",fontSize:9.5,bold:true,color:NAVY,margin:0});
  s.addNotes("오늘 발표의 중심은 특정 도펀트 하나가 아닙니다. LPSCl 을 개선하려고 여러 치환 후보를 계산했을 때, 무엇을 믿고 무엇을 탈락시킬지 결정하는 cascade 를 설명드립니다. 최종 산출물은 승자 선언이 아니라, 다음 DFT 와 실험이 갈 수 있는 짧고 방어 가능한 후보 목록입니다.");
}
// ═ 2 Context (Sundar) ═
{ const s=base("Context","One repair must survive several sulfide interfaces","One repair must survive several sulfide interfaces",
  "Argyrodite LPSCl 은 이온전도성과 가공성이 좋지만 산화, 계면, 접촉·기계 문제를 동시에 만족하지 못합니다. 왼쪽은 Sundar 논문의 coating 개요인데, coating 자체가 우리 lattice substitution 과 같다는 게 아니라 - 하나의 처방도 Li, LPSCl, 양극의 서로 다른 계면을 동시에 통과해야 한다는 문제를 보여줍니다. 무엇을 택해도 여러 물성이 함께 바뀌므로 단일 지표가 아니라 cascade 가 필요합니다.");
  img(s,M+"image.png",0.7,1.7,4.6,3.4,"Literature schematic; coating ≠ lattice substitution (Sundar et al., Adv. Sci. 2025, Fig. 1)");
  const rows=[["Oxidation","S-derived states limit the cathode side."],["Interface","One coating meets Li, LPSCl, and cathode chemistries."],["Contact & mechanics","Pressure and particle contact change the response."]];
  rows.forEach((r,i)=>{ soft(s,5.6,1.75+i*1.05,3.8,0.9,TSOFT,RULE);
    s.addText([{text:r[0]+"\n",options:{bold:true,fontSize:11,color:NAVY,breakLine:true}},{text:r[1],options:{fontSize:9.5,color:INK}}],
      {x:5.75,y:1.83+i*1.05,w:3.5,h:0.75,fontFace:"Arial",valign:"top",margin:0}); });
  take(s,"There is no single repair knob — and no single screening metric.",5.3);
  s.addText("Coating     Substitution     Composite     Processing",{x:0.6,y:5.75,w:8.8,h:0.3,fontFace:"Arial",fontSize:10,color:MUT,align:"center",margin:0});
}
// ═ 3 Motivation 91×3 ═
{ const s=base("Motivation","Campaign design record","Substitution turns one material into hundreds of decisions",
  "도펀트 종류만 바뀌는 게 아니라, 같은 화합물도 배치와 라벨이 달라지면 다른 구조가 됩니다. 현재 funnel 의 x 해석과 canonical CSV 의 concentration=0.25 가 충돌하므로 x002/x005/x010 은 campaign label 이라고만 부릅니다. 273 도 화합물 수가 아니라 91종에 세 label 을 붙인 run slot 수입니다. 실험 한 점에 걸리는 시간이 크기 때문에, 비싼 검증 전에 실패 가능성이 큰 방향부터 줄이는 절차가 필요합니다.");
  const cells=[["Dopant chemistry","Which element or compound?"],["Campaign label","x002 / x005 / x010; actual x unresolved"],["Configuration","Where are defects placed?"],["Target properties","Stability · transport · mechanics"]];
  cells.forEach((c,i)=>{ soft(s,0.7+i*2.32,1.7,2.1,1.15,TB,NAVY);
    s.addText([{text:c[0]+"\n",options:{bold:true,fontSize:10.5,color:NAVY,breakLine:true}},{text:c[1],options:{fontSize:8.5,color:INK}}],
      {x:0.8+i*2.32,y:1.78,w:1.9,h:1.0,fontFace:"Arial",valign:"top",margin:0});
    if(i<3) s.addText("×",{x:2.62+i*2.32,y:2.05,w:0.3,h:0.4,fontSize:16,bold:true,color:MUT,fontFace:"Arial",margin:0}); });
  const nums=[["91","curated compounds"],["3","campaign labels"],["273","campaign run slots"]];
  nums.forEach((n,i)=>{ s.addText([{text:n[0]+"\n",options:{fontSize:30,bold:true,color:NAVY,breakLine:true}},{text:n[1],options:{fontSize:10,color:MUT}}],
      {x:1.5+i*2.6,y:3.4,w:2.2,h:1.2,align:"center",fontFace:"Arial",margin:0});
    if(i<2) s.addText(i===0?"×":"=",{x:3.35+i*2.6,y:3.55,w:0.5,h:0.5,fontSize:20,bold:true,color:MUT,fontFace:"Arial",align:"center",margin:0}); });
  take(s,"Element labels alone do not predict the effect.");
  SRC(s,"Source: cascade_v23_champions.csv · x labels are nominal");
}
// ═ 4 Decision architecture ═
{ const s=base("Cascade","Decision architecture","A cascade spends precision only where it matters",
  "Cascade 는 계산을 많이 돌리는 방법이 아니라 비용 배치 전략입니다. 싼 단계에서 넓게 비교하고, 물리 게이트로 위험한 후보를 제거한 뒤, 비싼 DFT 와 실험을 남은 후보에 집중합니다. 각 단계가 무엇을 판정할 수 있는지 한계를 먼저 정합니다.");
  const st=[["1  CURATE","Chemical priors\nLiterature and database",TB],["2  SCREEN","Same-protocol MLIP\nand low-cost proxies",TB],["3  GATE","Reject physically\nunsafe candidates",TA],["4  VALIDATE","Targeted DFT\nand experiment",TG]];
  st.forEach((t,i)=>{ const bx=1.0+i*0.55, by=1.65+i*1.05; soft(s,bx,by,6.6,0.9,t[2], i===2?AMB:(i===3?GRN:NAVY));
    s.addText(t[0],{x:bx+0.2,y:by+0.25,w:1.6,h:0.4,fontFace:"Arial",fontSize:11.5,bold:true,color:i===2?AMB:(i===3?GRN:NAVY),margin:0});
    s.addText(t[1],{x:bx+2.4,y:by+0.12,w:4.0,h:0.7,fontFace:"Arial",fontSize:9.5,color:INK,align:"center",valign:"middle",margin:0}); });
  s.addText("Candidate count ↓",{x:0.55,y:2.2,w:1.6,h:0.5,fontFace:"Arial",fontSize:10,bold:true,color:MUT,margin:0});
  s.addText("Cost and precision ↑",{x:8.0,y:4.4,w:1.6,h:0.6,fontFace:"Arial",fontSize:10,bold:true,color:MUT,margin:0});
  take(s,"Computation narrows experiments; it does not replace them.",6.0);
}
// ═ 5 Pool provenance ═
{ const s=base("Cascade","Pool provenance · versioned lineage",null,
  "273은 run slot 수입니다. versioned canonical table 은 2026-06-25 스냅샷으로 oxide 37 + fluoride 10, 47종의 141개 record 만 담습니다 - 141 = 47 x 3 은 champions.csv 로 재검산했습니다. 나머지 44종은 물리 탈락이 아니라 개별 실패 manifest 가 없는 미분류입니다(유일 문서화: As2S3 x3, n_structures=0). 그래서 273에서 47로 걸러냈다는 발견 서사는 쓰지 않습니다.");
  img(s,M+"image2.png",0.7,1.25,8.6,4.75,"91 × 3 attempted slots → versioned 47-species snapshot (attrition is provenance, not physics)");
  SRC(s,"Source: cascade_seminar_pool_attrition_273_to_47.csv · champions.csv (141 rows)");
}
// ═ 6 [N1] 후보 지도 ═
{ const s=base("Cascade","The 47-species snapshot, by chemical family","What we actually explored — a cast list, not a ranking",
  "탐색 대상을 이름으로 보여드립니다. 전이금속 23, 주족 9, 알칼리토 6, 란타나이드 6, 알칼리 3 - 산화물 37과 불화물 10의 versioned snapshot 입니다. 진하게 표시한 11종이 사후 G4 감사까지 남은 후보고, 단검 표시 두 종만 targeted DFT 로 더 들어갔습니다. 이 장은 명단이지 순위가 아닙니다. 자세한 축별 값은 부록 heatmap 에 있습니다.");
  const SUBD={"0":"₀","1":"₁","2":"₂","3":"₃","4":"₄","5":"₅"}; const fs=x=>x.replace(/\d/g,d=>SUBD[d]);
  const PASS=new Set(["Ag2O","CaF2","CaO","Li2O","LiF","MgF2","MgO","SiO2","SnO2","WO3","ZnO"]);
  const DEEP=new Set(["B2O3","Nd2O3"]);
  const G=[["Transition metal (23)",["Ag2O","CoO","Cr2O3","CrO3","Cu2O","Fe2O3","HfO2","MnO","MoO3","Nb2O5","NiO","Sc2O3","ScF3","Ta2O5","TiF4","TiO2","V2O5","WO3","Y2O3","YF3","ZnO","ZrF4","ZrO2"],[0.6,1.55,3.3,3.6]],
   ["Main group (9)",["Al2O3","AlF3","B2O3","Ga2O3","GeO2","In2O3","Sb2O5","SiO2","SnO2"],[4.05,1.55,5.35,1.15]],
   ["Alkaline earth (6)",["BaO","CaF2","CaO","MgF2","MgO","SrO"],[4.05,2.85,2.6,1.0]],
   ["Lanthanide (6)",["Gd2O3","La2O3","LaF3","Nd2O3","NdF3","Sm2O3"],[6.8,2.85,2.6,1.0]],
   ["Alkali (3)",["Li2O","LiF","Na2O"],[4.05,4.0,2.6,0.85]]];
  G.forEach(g=>{ const [bx,by,bw,bh]=g[2]; soft(s,bx,by,bw,bh, g[0].startsWith("Transition")?TB:"FFFFFF");
    s.addText(g[0],{x:bx+0.12,y:by+0.06,w:bw-0.24,h:0.24,fontFace:"Arial",fontSize:9.5,bold:true,color:MUT,margin:0});
    const runs=[]; g[1].forEach((c,i)=>{ runs.push({text:fs(c)+(DEEP.has(c)?"†":""),options:{fontSize:9.5,bold:PASS.has(c),color:PASS.has(c)?NAVY:INK}});
      if(i<g[1].length-1) runs.push({text:"  ·  ",options:{fontSize:9.5,color:RULE}}); });
    s.addText(runs,{x:bx+0.12,y:by+0.3,w:bw-0.24,h:bh-0.38,fontFace:"Arial",valign:"top",margin:0}); });
  s.addText([{text:"bold",options:{bold:true,color:NAVY,fontSize:9}},{text:" = retained through the post-hoc G4 audit (11)    ",options:{color:MUT,fontSize:9}},
             {text:"†",options:{bold:true,color:INK,fontSize:9}},{text:" = targeted deep-DFT case study (2)    37 oxides + 10 fluorides, versioned 2026-06-25",options:{color:MUT,fontSize:9}}],
    {x:6.8,y:4.0,w:2.7,h:1.3,fontFace:"Arial",valign:"top",margin:0});
  take(s,"A curated snapshot to explore — membership here is not a gate result.",5.55);
  SRC(s,"Source: cascade_seminar_scorecard_47.csv (dopant · group · pass_G1_G4 · dft_deep)");
}
// ═ 7 Tiers ═
{ const s=base("Pipeline","Same protocol within each tier","Search, validation, and interpretation are different jobs",
  "Tier 1에서 UMA 와 저비용 프록시로 넓게 보고, Tier 2에서 필요한 후보만 matched DFT 로 확인합니다. Tier 3는 질문별 후처리와 실험입니다. 모든 조성이 같은 고비용 계산을 받는 게 아니라, tier 안에서 프로토콜을 고정하고 선택된 후보만 올립니다. 현재 DFT 검증은 두 후보라는 범위를 계속 표시합니다.");
  const t=[["L0","CURATED INPUT","Composition · concentration\nconfiguration · provenance",TSOFT],["L1","LOW-COST SCREEN","UMA relaxation\nBVSE and derived axes",TB],["L2","MATCHED DFT","Selected candidates only\nenergy · force · electronics",TA],["L3","EXPERIMENT","Phase purity · sigma(T)\nstability · processing",TG]];
  t.forEach((r,i)=>{ soft(s,0.7+i*2.32,1.8,2.1,2.0,r[3], i===2?AMB:(i===3?GRN:NAVY));
    s.addText([{text:r[0]+"  ",options:{bold:true,fontSize:13,color:MUT}},{text:r[1]+"\n",options:{bold:true,fontSize:10,color:NAVY,breakLine:true}},{text:r[2],options:{fontSize:8.5,color:INK}}],
      {x:0.82+i*2.32,y:1.95,w:1.9,h:1.7,fontFace:"Arial",valign:"top",margin:0});
    if(i<3) s.addShape(p.ShapeType.line,{x:2.82+i*2.32,y:2.8,w:0.2,h:0,line:{color:MUT,width:1.75,endArrowType:"triangle"}}); });
  s.addText("Protocol tag + source file + status travel with every value",{x:0.6,y:4.3,w:8.8,h:0.3,fontFace:"Arial",fontSize:11,bold:true,color:INK,align:"center",margin:0});
  take(s,"Current scope: 47 relative screens; targeted DFT validation covers 2 candidates.",5.0);
}
// ═ 8 LPSCl descriptors ═
{ const s=base("Evidence","Canonical registry · same-protocol values","LPSCl taught us which descriptors to watch",
  "기존 LPSCl 과 Cl-rich 비교는 cascade 의 결과가 아니라 축 선택의 선행 사례입니다. fixed-occupation gap 차이는 0.033 eV 로 작지만, Cl-rich 구조에는 Li 공공과 4d-Cl anti-site 가 생깁니다. 그래서 구조 안정성, Li 경로, 무질서, 기계 축을 우선 기술자로 잡았습니다. comp1 에는 인용 가능한 멀티시드 Ea 가 없어 두 계의 barrier 비교는 하지 않습니다.");
  const cols=[["Electronic guard","Eg = 2.066 vs 2.099 eV\nΔ = 0.033 eV\nFixed-occupation eigenvalues",TB,NAVY],["Structural contrast","Li vacancies\n4d-Cl anti-sites\nDisorder, not a new chemistry",TA,AMB],["Transport evidence","Cl-rich modelc: Ea = 0.197 ± 0.032 eV\n3-seed, 600/800/1000 K\nNo citable comp1 Ea",TG,GRN]];
  cols.forEach((c,i)=>{ soft(s,0.7+i*3.0,1.75,2.8,2.1,c[2],c[3]);
    s.addText([{text:c[0]+"\n",options:{bold:true,fontSize:11,color:c[3],breakLine:true}},{text:c[1],options:{fontSize:9.5,color:INK}}],
      {x:0.85+i*3.0,y:1.9,w:2.5,h:1.8,fontFace:"Arial",valign:"top",margin:0}); });
  s.addText("Structural descriptors first; electronics remain a guardrail.",{x:0.6,y:4.25,w:8.8,h:0.3,fontFace:"Arial",fontSize:11.5,bold:true,color:INK,align:"center",margin:0});
  take(s,"Gap values are canonical; lineage-specific fixed-occ run files remain provenance-open.",4.75);
  SRC(s,"Source: electronic.json · canonical_registry.json");
}
// ═ 9 Five gates ═
{ const s=base("Cascade","G1-G4 physical · G5 ranking-only","Five gates ask five different questions",
  "G1은 host 대비 구조 안정, G2는 창 붕괴, G3는 host 대비 산화 onset, G4는 BVSE 기하 프록시 두 컷, G5는 로스터 중앙값 순위입니다. G1은 47종 전부 통과라 현재 풀에서 gate power 가 없고, G2의 네 탈락은 전부 G3에도 걸립니다. G4의 blocking 0.6은 anchor 없는 heuristic 이고, G5는 ranking-only 입니다.");
  const g=[["G1","Structure","More stable than host?","mean ΔE < 0",NAVY],["G2","Window","Does the ESW collapse?","window ≥ 0.05 V",BLU],["G3","Oxidation","Worse than host onset?","Vox ≥ 2.14 V",AMB],["G4","Li pathway","Is the pathway retained?","proxy > 0.3 AND blocking < 0.6",GRN],["G5*","Mechanics","How do survivors rank?","roster medians",MUT]];
  g.forEach((r,i)=>{ soft(s,0.7+i*1.79,1.75,1.62,2.3,"FFFFFF",r[4]);
    s.addText([{text:r[0]+"\n",options:{bold:true,fontSize:15,color:r[4],breakLine:true}},{text:r[1]+"\n",options:{bold:true,fontSize:10,color:INK,breakLine:true}},{text:r[2]+"\n",options:{fontSize:8.5,color:INK,breakLine:true}},{text:r[3],options:{fontSize:8.5,bold:true,color:r[4]}}],
      {x:0.82+i*1.79,y:1.9,w:1.4,h:2.05,fontFace:"Arial",valign:"top",margin:0}); });
  take(s,"G4 is also heuristic: blocking < 0.6 has no host/literature anchor.  G5 is roster-relative ranking.",4.5);
  SRC(s,"Source: cascade_screening_funnel.json (gates)");
}
// ═ 10 Waterfall ═
{ const s=base("Cascade","Post-hoc literature-mapped gate view","The auditable hard-gate view stops at 11",
  "기본 결과는 weighted score 이고, 이 hard-gate funnel 은 문헌 기준을 투영한 사후 분석 뷰입니다. 47에서 47, 43, 25, 11로 줄고, G5의 1은 median 정렬 결과라 winner 로 부르지 않습니다. 방어 가능한 보고는 G4 통과 11종과 각 게이트 한계를 함께 제시하는 것입니다.");
  const bars=[["DATA-COMPLETE",47,NAVY],["G1  STRUCTURE",47,"0F5298"],["G2  WINDOW",43,"4A7EBB"],["G3  OXIDATION",25,AMB],["G4  LI TRANSPORT",11,GRN]];
  bars.forEach((b,i)=>{ const bw=6.2*(b[1]/47), by=1.6+i*0.78;
    s.addText(b[0],{x:0.6,y:by+0.12,w:1.9,h:0.3,fontFace:"Arial",fontSize:8.5,bold:true,color:MUT,align:"right",margin:0});
    s.addShape(p.ShapeType.roundRect,{x:2.65,y:by,w:bw,h:0.55,rectRadius:0.05,fill:{color:b[2]}});
    s.addText(String(b[1]),{x:2.65+bw-0.7,y:by+0.08,w:0.6,h:0.4,fontFace:"Arial",fontSize:14,bold:true,color:"FFFFFF",align:"right",margin:0}); });
  soft(s,3.4,5.6,3.2,0.5,TSOFT,RULE);
  s.addText("G5 mechanical ranking → 1*",{x:3.4,y:5.66,w:3.2,h:0.38,fontFace:"Arial",fontSize:10.5,bold:true,color:MUT,align:"center",margin:0});
  take(s,"* This funnel is a post-hoc analysis view. G4 is heuristic; G5 is ranking-only.",6.25);
  SRC(s,"Source: cascade_screening_funnel.json (waterfall)");
}
// ═ 11 Standalone/unique kill ═
{ const s=base("Audit","Standalone kill · unique kill","Two gates reveal more about the pool than the candidates",
  "G1이 아무 후보도 제거하지 못한 것은 모든 후보가 훌륭하다는 뜻이 아니라, 출발 풀이 안정 후보 위주로 큐레이션됐다는 뜻입니다. G2에서 탈락한 late-TM 4종은 G3에도 모두 탈락해 unique kill 이 0입니다. 게이트가 독립 정보를 주는지 감사하는 것 자체가 결과입니다.");
  soft(s,0.8,1.8,4.0,3.2,TB,NAVY);
  s.addText([{text:"G1: 47 / 47 pass\n",options:{bold:true,fontSize:13,color:NAVY,breakLine:true}},{text:"VACUOUS\n",options:{bold:true,fontSize:17,color:RED,breakLine:true}},{text:"No selection pressure in the curated pool.\nThis does not prove universal stability.",options:{fontSize:10,color:INK}}],
    {x:1.0,y:2.1,w:3.6,h:2.6,fontFace:"Arial",valign:"top",margin:0});
  soft(s,5.2,1.8,4.0,3.2,TA,AMB);
  s.addText([{text:"G2: unique kill = 0\n",options:{bold:true,fontSize:13,color:AMB,breakLine:true}},{text:"REDUNDANT\n",options:{bold:true,fontSize:17,color:RED,breakLine:true}},{text:"Four window-collapse failures (CoO, Fe₂O₃, MnO, NiO) also fail G3.\nLate-TM chemistry drives both.",options:{fontSize:10,color:INK}}],
    {x:5.4,y:2.1,w:3.6,h:2.6,fontFace:"Arial",valign:"top",margin:0});
  take(s,"Keep the records. Change the interpretation.  Gate auditing is itself a scientific result.",5.5);
  SRC(s,"Source: cascade_seminar_scorecard_47.csv (first_stop)");
}
// ═ 12 Trade-off ═
{ const s=base("Result","47-species snapshot · static pathway audit",null,
  "산화 onset 을 host 위로 올린 여섯 후보 - B2O3, Cr2O3, Ga2O3, In2O3, Sc2O3, Y2O3 - 가 모두 같은 G4 정적 경로 heuristic 에서 멈췄습니다. 이건 데이터셋 수준의 trade-off 이고 M-O 결합이 Li blocking 을 일으킨다는 인과 증명은 아닙니다. BVSE 는 conductivity 가 아닙니다. 다만 한 후보의 약점과 다른 후보의 강점을 조합해 볼 이유는 충분히 줍니다.");
  img(s,M+"image3.png",0.7,1.2,8.6,4.6,"All six oxidation-raising candidates stop at the same static pathway heuristic — a dataset-level trade-off, not causal proof of M–O blocking");
  SRC(s,"Source: cascade_seminar_oxidation_transport_47.csv (6/6 verified)");
}
// ═ 13 Pareto ═
{ const s=base("Decision model","Conditional Pareto view within post-hoc G1–G4",null,
  "가중점수는 측정 물리량이 아니라 의사결정 함수입니다. 그래서 G1-G4 의 11종 안에서 mean relative energy 와 BVSE proxy 만 놓은 conditional Pareto 를 같이 봅니다. 비지배 4종은 winner 가 아니고 축을 바꾸면 집합도 바뀝니다. 11종은 host onset 2.14 V 에 묶여 산화축 내부 순위가 없습니다.");
  img(s,M+"image4.png",0.7,1.2,8.6,4.6,"Non-dominated set within the 11-member shortlist — axis-dependent, not a winner list");
  SRC(s,"Source: cascade_seminar_pareto_47.csv");
}
// ═ 14 [N2] 질문-축 지도 ═
{ const s=base("Decision model","One snapshot, different deployment questions","Each answer inherits a different evidence level",
  "같은 47종 스냅샷에 질문을 바꿔 던질 수 있습니다. 고전압 양극 쪽이면 산화 onset 과 창 - 저희 계산입니다. 공기 취급이면 문헌 가수분해 proxy 와 정성 등급인데 커버리지가 35/47이고 나머지 12종은 모름이지 불안정이 아닙니다. 비용·무게는 정성 tier 와 질량 proxy, 농도 내성은 세 label 사이 BVS 변화입니다. 축마다 증거 수준이 달라서 화면마다 tag 를 붙였고, 서술 축 단독으로는 어떤 후보도 탈락시키지 않습니다.");
  const hdr=["Deployment question","Axes consulted","Evidence level","Missing handling"];
  const rows=[
   ["High-voltage cathode side?","oxidation onset · ESW window","OURS-CALC (MP grand-potential)","—"],
   ["Survives ambient handling?","ΔG_hyd (lit., binary-sulfide proxy) · HSAB tier","LITERATURE (35/47) · CURATED","12 unknown — excluded, never zero"],
   ["Cheap and light at scale?","cost tier · formula mass per cation","CURATED (2026 tier) · STATIC-PROXY","qualitative — never $/kg or Wh/kg"],
   ["Robust to doping level?","BVS proxy drift across 3 campaign labels","STATIC-PROXY (nominal labels)","labels ≠ resolved x"]];
  const tbl=[hdr.map(h=>({text:h,options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}}))].concat(rows);
  s.addTable(tbl,{x:0.6,y:1.7,w:8.8,fontFace:"Arial",fontSize:9.5,color:INK,border:{type:"solid",color:RULE,pt:0.75},
    colW:[2.3,2.7,2.2,1.6],rowH:0.62,valign:"middle",margin:0.05});
  take(s,"No axis alone rejects a candidate; descriptive axes never gate.",5.35);
  SRC(s,"Source: cascade_v23_themes.json (dG_hyd_MS_lit 35/47 · cost_tier · mass_per_cation · bvs_slope)");
}
// ═ 15 [N3] 레이더 ═
{ const s=base("Decision model","Candidate profiles across eight axes","Strengths trade — they do not add",
  "방금 그 질문-축 지도를 후보 단위로 접으면 이 팔각형이 됩니다. WO3 는 연질 쪽이 크지만 비용 축이 약하고, B2O3 는 산화 쪽이 큰데 Li 경로만 움푹 들어가 있습니다 - 아까 본 트레이드오프가 도형으로 반복됩니다. Cr2O3 와 HfO2 는 서로 반대쪽이 큰데 이 둘을 겹친 그림이 co-doping 절에 나옵니다. 축은 전부 47종 내 상대 percentile 이고, 공기 축은 편향 검증이 끝날 때까지 뺐습니다.");
  img(s,REPO+"docs/figures/cascade/cascade_radar_6panel.png",0.85,1.35,8.3,4.75,
    "Within-pool favorable percentiles (descriptive ranking, not absolute properties) — air axes excluded (provisional); BVSE/blocking are static proxies");
  SRC(s,"Source: cascade_radar_axes_origin.csv · fig_cascade_radar.py");
}
// ═ 16 120 orders ═
{ const s=base("Robustness","All 5! = 120 gate orders enumerated","Gate order changes the story, not the terminal intersection",
  "다섯 게이트의 120개 순열을 모두 시험했습니다. 게이트가 정적 boolean 조건이라 최종 교집합은 순서와 무관했습니다. 대신 중간 생존자 수와 어느 게이트가 탈락시킨 것으로 보이는지는 달라집니다. waterfall 모양은 결과라기보다 설명 순서입니다.");
  soft(s,0.8,1.9,8.4,1.0,TB,NAVY);
  s.addText([{text:"G1 → G2 → G3 → G4 → G5      ",options:{bold:true,fontSize:12,color:NAVY}},{text:"47 → 47 → 43 → 25 → 11 → 1",options:{fontSize:12,color:INK}}],
    {x:1.0,y:2.15,w:8.0,h:0.5,fontFace:"Arial",margin:0});
  soft(s,0.8,3.1,8.4,1.0,TSOFT,RULE);
  s.addText([{text:"G1 → G3 → G2 → G5 → G4      ",options:{bold:true,fontSize:12,color:MUT}},{text:"47 → 47 → 25 → 25 → 7 → 1",options:{fontSize:12,color:INK}}],
    {x:1.0,y:3.35,w:8.0,h:0.5,fontFace:"Arial",margin:0});
  s.addText([{text:"120 / 120",options:{bold:true,fontSize:22,color:NAVY}},{text:"  gate permutations tested — terminal set invariant; intermediate attribution order-dependent",options:{fontSize:11,color:INK}}],
    {x:0.8,y:4.4,w:8.4,h:0.5,fontFace:"Arial",margin:0});
  take(s,"Intermediate waterfall shape and “who killed what” remain order-dependent.",5.4);
  SRC(s,"Source: cascade_pipeline_guide.md (permutation audit)");
}
// ═ 17 Trust boundary ═
{ const s=base("Trust boundary","Method-matched claims only","Claim strength must match the method",
  "같은 프로토콜 안의 통과·탈락과 상대순위, 산화-수송 trade-off, 순서 불변성은 현재 데이터로 지지됩니다. UMA 절대값, BVSE 를 전도도로 환산한 값, 축퇴군 내부 순위, G5 단일 승자는 지지되지 않습니다. 계면 반응과 전자 절연은 아직 완전한 게이트로 들어오지 않았습니다.");
  soft(s,0.8,1.8,4.0,3.3,TG,GRN);
  s.addText([{text:"SUPPORTED\n",options:{bold:true,fontSize:13,color:GRN,breakLine:true}},
    {text:"✓ Gate pass / fail\n✓ Same-protocol relative ranking\n✓ Oxidation–transport trade-off\n✓ Gate-order invariance",options:{fontSize:10.5,color:INK}}],
    {x:1.0,y:2.05,w:3.6,h:2.8,fontFace:"Arial",valign:"top",margin:0});
  soft(s,5.2,1.8,4.0,3.3,"FDECEA",RED);
  s.addText([{text:"NOT SUPPORTED\n",options:{bold:true,fontSize:13,color:RED,breakLine:true}},
    {text:"× UMA absolute energies / moduli\n× BVSE-derived conductivity\n× Ranking inside degenerate groups\n× A unique G5 winner",options:{fontSize:10.5,color:INK}}],
    {x:5.4,y:2.05,w:3.6,h:2.8,fontFace:"Arial",valign:"top",margin:0});
  take(s,"Still missing as full gates: interface reaction + electronic insulation",5.5);
}
// ═ 18 Ledger (SDCP 제거판) ═
{ const s=base("Validation","Retraction ledger","Failures made the cascade more credible",
  "이 파이프라인은 처음부터 완성된 규칙이 아니었습니다. 단일시드 전도도 비교, 확산영역 밖 MSD 피팅, DOS threshold gap 을 철회했고, 공기 정성 축은 문헌 대조에서 아홉 건이 전부 한 방향으로 어긋나 서술 등급으로 강등했습니다. 실패한 주장이 실행 가능한 게이트가 됐습니다 - 감사는 파이프라인의 일부입니다.");
  const rows=[["Single-seed 1.33× conductivity","Multi-seed verdict only"],
              ["MSD fit outside diffusion","β ∈ [0.8, 1.2] gate"],
              ["DOS-threshold band gap","Fixed-occ eigenvalues"],
              ["air_hsab qualitative tier","[Zhu20] cross-check: 9/35 off, all one direction → axis demoted to CURATED"]];
  rows.forEach((r,i)=>{ const by=1.75+i*1.02; soft(s,0.8,by,8.4,0.85,i===3?TA:TSOFT,i===3?AMB:RULE);
    s.addText([{text:r[0]+"   →   ",options:{bold:true,fontSize:11,color:INK}},{text:r[1],options:{fontSize:10.5,color:NAVY,bold:true}}],
      {x:1.0,y:by+0.2,w:8.0,h:0.5,fontFace:"Arial",margin:0}); });
  take(s,"Failed claims became executable gates — the audit is part of the pipeline.",6.05);
  SRC(s,"Source: canonical_registry.json · cascade_air_axis_lit_vs_tier.csv (26/9/12)");
}
// ═ 19 Coverage 2/47 ═
{ const s=base("Validation","Current deep-DFT coverage: 2 / 47","Three coverage counts — not a linear funnel",
  "47종 상대 스크린, G1-G4 통과 11종, 심층 DFT 2건은 한 줄의 funnel 이 아닙니다. 특히 B2O3 는 G4 탈락 후보지만 trade-off 검증을 위해 DFT 로 본 사례라 11종의 부분집합처럼 그리면 틀립니다. 비싼 계산은 게이트 경계, 모델 불일치, Pareto 가치, 새로운 화학을 대표하는 후보에 선택적으로 씁니다.");
  const c=[["47","data-complete relative screens",NAVY],["11","post-hoc G1–G4 survivors",GRN],["2","selected deep-DFT cases",AMB]];
  c.forEach((r,i)=>{ s.addText([{text:r[0]+"\n",options:{fontSize:40,bold:true,color:r[2],breakLine:true}},{text:r[1],options:{fontSize:10,color:MUT}}],
      {x:0.9+i*3.0,y:1.9,w:2.8,h:1.6,align:"center",fontFace:"Arial",margin:0}); });
  s.addText("PARALLEL COVERAGE RECORDS  ·  B₂O₃ is not inside the G4 survivor set",{x:0.6,y:3.6,w:8.8,h:0.3,fontFace:"Arial",fontSize:10.5,bold:true,color:RED,align:"center",margin:0});
  soft(s,0.8,4.15,4.0,1.5,TSOFT,RULE);
  s.addText([{text:"Promote when\n",options:{bold:true,fontSize:10.5,color:NAVY,breakLine:true}},{text:"• Near a gate boundary\n• Model heads disagree\n• Pareto value is high\n• Chemistry is under-sampled",options:{fontSize:9,color:INK}}],
    {x:1.0,y:4.25,w:3.6,h:1.3,fontFace:"Arial",valign:"top",margin:0});
  soft(s,5.2,4.15,4.0,1.5,TSOFT,RULE);
  s.addText([{text:"Matched validation contract\n",options:{bold:true,fontSize:10.5,color:NAVY,breakLine:true}},{text:"Same structure, cell, constraint, k-mesh, reference, and magnetic protocol.\nCompare only inside one protocol lineage.",options:{fontSize:9,color:INK}}],
    {x:5.4,y:4.25,w:3.6,h:1.3,fontFace:"Arial",valign:"top",margin:0});
  take(s,"The 47-candidate result is a relative screen — not 47 DFT confirmations.",5.95);
}
// ═ 20 ML + pair radar ═
{ const s=base("ML roadmap","UMA screen + co-doping hypothesis model","ML is already here — but it is not yet a discovery model",
  "ML 을 둘로 나눠야 합니다. UMA 는 에너지와 힘을 대신하는 MLIP 라 같은 규약으로 넓게 볼 수 있게 해 줍니다. 공동치환 모델은 47개 단일 도펀트 점수를 1,081개 조합에 이식한 가설 생성기입니다. 실제 라벨이 없고 dopant 를 통째로 빼면 R2 가 음수라 discovery predictor 가 아닙니다. 오른쪽 레이더처럼 Cr2O3 와 HfO2 는 서로 반대쪽이 커서 상보성 가설은 그림으로 서지만, 두 champion 의 문헌-유추 자리가 겹칠 수 있어(Cr3+ Li_24g, Hf4+ 양쪽성) site 경쟁이 1차 리스크입니다.");
  const b=[["UMA MLIP","Energy and force surrogate\nFast configuration search\nSame-protocol relative screen",TB,NAVY],
           ["Physics cascade","Gate pass / fail\nTrade-off structure\nShortlist for expensive validation",TG,GRN],
           ["Co-doping ML v2","47 scores → 1,081 pair hypotheses\n0 explicit pair structures / targets\nLODO / L2DO R² < 0",TA,AMB]];
  b.forEach((r,i)=>{ soft(s,0.7,1.75+i*1.35,4.4,1.2,r[2],r[3]);
    s.addText([{text:r[0]+"\n",options:{bold:true,fontSize:10.5,color:r[3],breakLine:true}},{text:r[1],options:{fontSize:8.5,color:INK}}],
      {x:0.85,y:1.85+i*1.35,w:4.1,h:1.0,fontFace:"Arial",valign:"top",margin:0}); });
  img(s,REPO+"docs/figures/cascade/cascade_radar_pair_CrHf.png",5.35,1.5,4.0,4.1,
    "End-member profiles only — the pair itself is uncomputed (site competition unresolved)");
  take(s,"Current role: cost reduction + hypothesis ordering, not discovery certification.",6.1);
  SRC(s,"Source: codoping_ml_v2_meta.json · cascade_radar_axes_origin.csv");
}
// ═ 21 Acquisition loop ═
{ const s=base("Outlook","Pattern: Sendek 2017 · GNoME 2023 · Kim 2025","The next cascade learns where to calculate next",
  "다음 단계는 게이트를 ML 로 없애는 게 아니라, 비싼 계산을 어디에 쓸지 정하는 폐루프입니다. 물리 gate 와 모델을 분리하고, 새 DFT label 을 DB 와 모델로 돌려보냅니다. 상위 예측만 반복하지 않고 불확실하거나 새로운 화학도 선택하며, 게이트 경계는 DFT 로 확인합니다. 최종 판단은 물리 게이트와 실험이 맡습니다.");
  const n=[["CANDIDATE SPACE","dopant × x × configuration",TSOFT,MUT,0.8,1.9],["L1  FAST SCREEN","UMA + BVSE + gate risk",TB,NAVY,3.6,1.9],
           ["L2  DFT","matched validation",TA,AMB,6.4,1.9],["VERSIONED DATABASE","provenance-tagged records",TG,GRN,3.6,3.6],
           ["ACQUISITION","Pareto gain + uncertainty + diversity",TSOFT,NAVY,6.4,3.6],["L3  EXPERIMENT","phase · sigma(T) · stability",TG,GRN,0.8,3.6]];
  n.forEach(r=>{ soft(s,r[4],r[5],2.5,1.1,r[2],r[3]);
    s.addText([{text:r[0]+"\n",options:{bold:true,fontSize:9.5,color:r[3],breakLine:true}},{text:r[1],options:{fontSize:8.5,color:INK}}],
      {x:r[4]+0.15,y:r[5]+0.12,w:2.2,h:0.9,fontFace:"Arial",valign:"top",margin:0}); });
  s.addText("EXPLOIT: predicted Pareto gain     EXPLORE: uncertainty / new chemistry     VALIDATE: gate boundary",
    {x:0.6,y:5.1,w:8.8,h:0.3,fontFace:"Arial",fontSize:9.5,color:MUT,align:"center",margin:0});
  take(s,"ML chooses what to calculate next; physics and experiments decide what is true.",5.7);
  SRC(s,"Source: cascade_ml_integration_guide.md · litdb (Sendek · Kim digests held)");
}
// ═ 22-27 Appendix ═
function app(kicker, headline, notes){ return base(kicker, null, headline, notes); }
{ const s=app("Appendix A1","Terminology and symbol conventions","기호 정의 방어용입니다. 모든 숫자에 method tag 를 붙이고 서로 다른 protocol 절대값을 한 축에 섞지 않습니다.");
  const rows=[["ΔE","Doped − host relative energy","Same engine, cell, composition convention"],
   ["Vox","Grand-potential oxidation onset","V vs Li; ties at 2.14 V remain unresolved"],
   ["window","Vox − Vred","Collapse gate only; not kinetic stability"],
   ["transport_norm","BVSE geometric proxy","Never call it D or conductivity"],
   ["β","d log(MSD) / d log(t)","0.8–1.2 required for diffusive verdict"],
   ["Ea","Arrhenius activation energy","State temperatures, window, seeds"],
   ["missing","Not calculated / incomplete","Not a zero and not a failure"]];
  s.addTable([["Symbol / term","Meaning","Usage rule"].map(h=>({text:h,options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}}))].concat(rows),
    {x:0.6,y:1.6,w:8.8,fontFace:"Arial",fontSize:9.5,color:INK,border:{type:"solid",color:RULE,pt:0.75},colW:[1.8,3.4,3.6],rowH:0.42,valign:"middle",margin:0.04});
}
{ const s=app("Appendix A2","Protocol matrix and allowed claims","이 표는 method-to-claim 계약입니다. screen 값과 DFT case study 를 같은 coverage 처럼 말하지 않습니다.");
  const rows=[["UMA MLIP","Relative E, forces, relaxation","Same-protocol candidate ordering","Absolute thermodynamics"],
   ["BVSE","Static pathway geometry","Pathway retention risk","D or conductivity"],
   ["MLIP-MD","MSD, D(T), Ea","Multiseed verdict at 600/800/1000 K","Single-seed ratio"],
   ["DFT","Matched energy/electronic response","Selected candidate validation","47/47 DFT coverage"],
   ["Literature / experiment","External values","Directional cross-check","Mix with internal absolutes"]];
  s.addTable([["Tier / method","Primary output","Allowed claim","Do not claim"].map(h=>({text:h,options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}}))].concat(rows),
    {x:0.6,y:1.6,w:8.8,fontFace:"Arial",fontSize:9.5,color:INK,border:{type:"solid",color:RULE,pt:0.75},colW:[1.7,2.5,2.5,2.1],rowH:0.5,valign:"middle",margin:0.04});
}
{ const s=app("Appendix A3","47-species scorecard heatmap","후보별 전 축 backup 입니다. percentile 은 표시용 상대 비교고 universal score 는 없습니다. missing 은 제외·flag 처리했습니다.");
  img(s,M+"image5.png",0.8,1.45,8.4,5.0,"Per-axis favorable percentiles + first-stop gate — no composite score, no winner");
  SRC(s,"Source: cascade_seminar_scorecard_47.csv");
}
{ const s=app("Appendix A4","Defense Q&A — cascade and evidence","질문에는 숫자보다 범위를 먼저 답합니다.");
  const rows=[["Is 47 a high-throughput discovery funnel?","No. It is a human-curated, host-specific composition-family scan."],
   ["What happened to the other 44 of 91?","Absent from the versioned canonical snapshot; absence is not physical rejection."],
   ["Why keep vacuous or redundant gates?","Auditability. Their selection pressure is reported and may change with a new pool."],
   ["Why conclude at 11 instead of one?","G5 is roster-median ranking. G4 defines the defensible physical survivor set."],
   ["Does BVSE failure prove low conductivity?","No. It flags pathway risk; multiseed MD or experiment is required."],
   ["Why is the air axis not a gate?","Literature proxy covers 35/47 (12 unknown ≠ unstable) and our qualitative tier failed a one-directional bias check — it stays descriptive."]];
  s.addTable([["Question","Defense answer"].map(h=>({text:h,options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}}))].concat(rows),
    {x:0.6,y:1.6,w:8.8,fontFace:"Arial",fontSize:9,color:INK,border:{type:"solid",color:RULE,pt:0.75},colW:[3.6,5.2],rowH:0.55,valign:"middle",margin:0.04});
}
{ const s=app("Appendix A5","Defense Q&A — validation and ML","UMA 와 후속 예측 모델의 역할을 분리해 답합니다.");
  const rows=[["Are all 47 candidates DFT-validated?","No. Current DFT coverage is 2/47; the rest are relative screens."],
   ["Can 47 rows train a discovery model?","Not a general model. They can seed gate-specific surrogates and active learning."],
   ["Why not trust LOOCV R² = 0.9998?","The target score is constructed from the same inputs; independent dopant splits collapse."],
   ["Why not choose only the predicted top candidate?","Winner's curse. Acquisition must include uncertainty and chemical diversity."],
   ["When can the model be called predictive?","After real co-doped labels, group-CV, and a prospective validation round."]];
  s.addTable([["Question","Defense answer"].map(h=>({text:h,options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}}))].concat(rows),
    {x:0.6,y:1.6,w:8.8,fontFace:"Arial",fontSize:9,color:INK,border:{type:"solid",color:RULE,pt:0.75},colW:[3.6,5.2],rowH:0.55,valign:"middle",margin:0.04});
}
{ const s=app("Appendix A6","Canonical sources held in the repository","숫자를 기억으로 인용하지 않고 정본 파일로 돌아갑니다.");
  const rows=[["docs/cascade_pipeline_guide.md","Canonical narrative, gates, trust limits"],
   ["db/properties/cascade_screening_funnel.json","Waterfall, gate outcomes, permutations"],
   ["db/properties/cascade_seminar_scorecard_47.csv","47-candidate axes + first-stop + deep-DFT flags"],
   ["db/properties/cascade_v23_champions.csv","141 champion records (47 × 3 labels)"],
   ["db/properties/cascade_v23_themes.json","14 design axes incl. air / cost / mass / dose"],
   ["db/properties/cascade_air_axis_lit_vs_tier.csv","[Zhu20] cross-check: 26 agree · 9 off · 12 absent"],
   ["db/properties/cascade_radar_axes_origin.csv","Eight-axis favorable percentiles (radar)"],
   ["db/properties/codoping_ml_v2_meta.json","ML validation limits (LODO/L2DO)"],
   ["db/properties/canonical_registry.json","Canonical values and provenance flags"]];
  s.addTable([["Source","Role"].map(h=>({text:h,options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}}))].concat(rows),
    {x:0.6,y:1.6,w:8.8,fontFace:"Arial",fontSize:9,color:INK,border:{type:"solid",color:RULE,pt:0.75},colW:[4.6,4.2],rowH:0.42,valign:"middle",margin:0.04});
}
p.writeFile({fileName: REPO+"kb/seminars/Research_Seminar_2026_08_draft27_claude.pptx"})
 .then(()=>console.log("WROTE", pg, "slides"));
