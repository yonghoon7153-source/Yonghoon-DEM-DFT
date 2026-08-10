// Research Seminar v3 deck — house style inherited from Research_Seminar_2026_08_cascade.pptx
// 4:3 · Arial · navy 1F4E79 · ink 262626 · muted 7F7F7F · rule D9D9D9 · accent 9E2A2B
const pptxgen = require("pptxgenjs");
const REPO = "/home/user/Yonghoon-DEM-DFT/";
const SCR  = "/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/82ea256b-12bc-5a75-994e-7718d79c71ba/scratchpad/";

const NAVY="1F4E79", INK="262626", MUT="7F7F7F", RULE="D9D9D9", RED="9E2A2B", LIGHT="EEF3F9", SOFT="F7F7F7";
const W=10, H=7.5;

const p = new pptxgen();
p.defineLayout({ name:"L43", width:W, height:H });
p.layout = "L43";

let pageNo = 0;
function newSlide(){ pageNo += 1; return p.addSlide(); }

function footer(s){
  s.addText([{text:"HANYANG UNIVERSITY", options:{bold:true, color:NAVY}},
             {text:"   Battery Materials Lab.", options:{color:MUT}}],
    {x:0.5, y:7.08, w:5.5, h:0.3, fontFace:"Arial", fontSize:8, margin:0});
  s.addText(String(pageNo), {x:9.3, y:7.08, w:0.35, h:0.3, fontFace:"Arial", fontSize:9, color:MUT, align:"right", margin:0});
}
function kickerTitle(s, kicker, title, refRight){
  s.addText(kicker, {x:0.5, y:0.26, w:3.5, h:0.28, fontFace:"Arial", fontSize:11, bold:true, color:NAVY, margin:0});
  if(refRight) s.addText(refRight, {x:4.2, y:0.24, w:5.3, h:0.32, fontFace:"Arial", fontSize:8.5, italic:true, color:MUT, align:"right", margin:0});
  s.addText(title, {x:0.5, y:0.56, w:9.0, h:0.62, fontFace:"Arial", fontSize:20, bold:true, color:INK, margin:0});
  s.addShape(p.ShapeType.line, {x:0.5, y:1.22, w:9.0, h:0, line:{color:RULE, width:1}});
}
function bullets(s, items, x,y,w,h, size){
  const arr=[];
  items.forEach((it,i)=>{
    const o = { fontFace:"Arial", fontSize:(it.size|| size || 11.5), color:(it.color|| (it.sub?MUT:INK)),
                bold:!!it.b, italic:!!it.i, breakLine:true, paraSpaceAfter:(it.gap==null?5:it.gap),
                bullet: it.nobul? false : {code: it.sub? "2013" : "00B7", indent: 10},
                indentLevel: it.sub?1:0 };
    arr.push({text:it.t, options:o});
  });
  s.addText(arr, {x:x, y:y, w:w, h:h, margin:0, valign:"top"});
}
function caption(s, txt, x,y,w){
  s.addText(txt, {x:x, y:y, w:w, h:0.3, fontFace:"Arial", fontSize:8.5, italic:true, color:MUT, align:"center", margin:0});
}
function img(s, path, x,y,w,h, capt){
  s.addImage({path:path, x:x, y:y, w:w, h:h, sizing:{type:"contain", w:w, h:h}});
  if(capt) caption(s, capt, x, y+h+0.02, w);
}
function placeholder(s, x,y,w,h, label, capt){
  s.addShape(p.ShapeType.rect, {x:x,y:y,w:w,h:h, fill:{color:SOFT}, line:{color:MUT, width:1, dashType:"dash"}});
  s.addText([{text:"PASTE SCREENSHOT\n", options:{bold:true, color:MUT, fontSize:11, breakLine:true}},
             {text:label, options:{color:MUT, fontSize:9}}],
    {x:x, y:y+h/2-0.45, w:w, h:0.9, align:"center", fontFace:"Arial", margin:0});
  if(capt) caption(s, capt, x, y+h+0.02, w);
}
// ── the talk map ────────────────────────────────────────────────────────────
const STOPS=[["(1) ASK","too many candidates","ask"],["(2) TOOLS","DFT + MLIP limits","measure"],
             ["(3) ORIGIN","LPSCl: disorder","learn"],["(4) SCREEN","273 calcs, 5 gates","gate"],
             ["(5) COMBINE","co-doping ML","combine"],["(6) VERIFY","11 audited verdicts","doubt"]];
function mapDiagram(s, x, y, w, active, big){
  const bw=(w-5*0.22)/6, bh= big?0.86:0.62, gap=0.22;
  for(let i=0;i<6;i++){
    const bx=x+i*(bw+gap);
    const isA=(i===active);
    s.addShape(p.ShapeType.roundRect, {x:bx,y:y,w:bw,h:bh, rectRadius:0.06,
      fill:{color: isA? (i===5?RED:NAVY):"FFFFFF"}, line:{color: i===5?RED:NAVY, width: isA?2:1.25}});
    s.addText([{text:STOPS[i][0]+"\n", options:{bold:true, fontSize:big?10:8, breakLine:true}},
               {text:STOPS[i][1], options:{fontSize:big?8:6.5}}],
      {x:bx, y:y, w:bw, h:bh, align:"center", valign:"middle", fontFace:"Arial",
       color:isA?"FFFFFF":(i===5?RED:NAVY), margin:0});
    if(big) s.addText(STOPS[i][2], {x:bx, y:y+bh+0.05, w:bw, h:0.22, align:"center",
      fontFace:"Arial", fontSize:8.5, italic:true, bold:isA, color:isA?(i===5?RED:NAVY):MUT, margin:0});
    if(i<5) s.addShape(p.ShapeType.line, {x:bx+bw+0.015, y:y+bh/2, w:gap-0.03, h:0,
      line:{color:MUT, width:1.75, endArrowType:"triangle"}});
  }
  // return arrows: VERIFY -> SCREEN (solid, below) and VERIFY -> TOOLS (dashed, above)
  const x6=x+5*(bw+gap)+bw/2, x4=x+3*(bw+gap)+bw/2, x2=x+1*(bw+gap)+bw/2;
  const yb=y+bh, dropB= big?0.34:0.24;
  s.addShape(p.ShapeType.line,{x:x4, y:yb+dropB, w:x6-x4, h:0, line:{color:NAVY, width:1.5, beginArrowType:"triangle"}});
  s.addShape(p.ShapeType.line,{x:x6, y:yb, w:0, h:dropB, line:{color:NAVY, width:1.5}});
  s.addShape(p.ShapeType.line,{x:x4, y:yb, w:0, h:dropB, line:{color:NAVY, width:1.5}});
  s.addText("new labels, new sims", {x:(x4+x6)/2-1.1, y:yb+dropB+0.01, w:2.2, h:0.22, fontSize:big?8:6.5, italic:true, color:NAVY, align:"center", fontFace:"Arial", margin:0});
  const dropT= big?0.30:0.22;
  s.addShape(p.ShapeType.line,{x:x2, y:y-dropT, w:x6-x2, h:0, line:{color:MUT, width:1.25, dashType:"dash", beginArrowType:"triangle"}});
  s.addShape(p.ShapeType.line,{x:x6, y:y-dropT, w:0, h:dropT, line:{color:MUT, width:1.25, dashType:"dash"}});
  s.addShape(p.ShapeType.line,{x:x2, y:y-dropT, w:0, h:dropT, line:{color:MUT, width:1.25, dashType:"dash"}});
  s.addText("tool limits exposed", {x:(x2+x6)/2-1.0, y:y-dropT-0.22, w:2.0, h:0.2, fontSize:big?8:6.5, italic:true, color:MUT, align:"center", fontFace:"Arial", margin:0});
}
function divider(partLabel, bigNum, title, sub, active, notes){
  const s=newSlide();
  s.background={color:"FFFFFF"};
  s.addText(partLabel, {x:0.55, y:1.45, w:3.0, h:0.6, fontFace:"Arial", fontSize:30, bold:true, color:NAVY, margin:0});
  s.addText(bigNum, {x:6.4, y:0.75, w:3.1, h:2.0, fontFace:"Arial", fontSize:120, bold:true, color:LIGHT, align:"right", margin:0});
  s.addText(title, {x:0.55, y:2.25, w:8.9, h:0.55, fontFace:"Arial", fontSize:20, bold:true, color:INK, margin:0});
  if(sub) s.addText(sub, {x:0.55, y:2.85, w:8.9, h:0.5, fontFace:"Arial", fontSize:12.5, color:MUT, margin:0});
  mapDiagram(s, 0.55, 4.6, 8.9, active, true);
  footer(s);
  if(notes) s.addNotes(notes);
  return s;
}

// ═══ 1. COVER ═══════════════════════════════════════════════════════════════
{
  const s=newSlide();
  s.addText("August 2026", {x:0.55, y:0.5, w:3, h:0.3, fontFace:"Arial", fontSize:11, color:MUT, margin:0});
  s.addText("Research Seminar", {x:0.55, y:1.35, w:8.9, h:0.7, fontFace:"Arial", fontSize:34, bold:true, color:NAVY, margin:0});
  s.addText("Self-Auditing Computational Screening of\nSulfide Solid Electrolytes", {x:0.55, y:2.5, w:8.9, h:1.3, fontFace:"Arial", fontSize:24, bold:true, color:INK, margin:0});
  s.addText("— from DFT gates to dopant combinations", {x:0.55, y:3.8, w:8.9, h:0.4, fontFace:"Arial", fontSize:15, italic:true, color:MUT, margin:0});
  s.addText("Yonghoon An", {x:0.55, y:5.0, w:8.9, h:0.35, fontFace:"Arial", fontSize:15, bold:true, color:INK, margin:0});
  s.addText("Division of Materials Science & Engineering, Hanyang University\n(E-mail : yonghoon71@hanyang.ac.kr)", {x:0.55, y:5.38, w:8.9, h:0.6, fontFace:"Arial", fontSize:11, color:MUT, margin:0});
  s.addText("게이트가 걸러낸 것들의 기록 — 판정 11건을 감사해 9건을 철회시킨 파이프라인",
    {x:0.55, y:4.25, w:8.9, h:0.3, fontFace:"Arial", fontSize:10.5, color:MUT, margin:0});
  s.addText("HANYANG UNIVERSITY", {x:0.55, y:6.9, w:4, h:0.3, fontFace:"Arial", fontSize:10, bold:true, color:NAVY, margin:0});
  s.addNotes("재료공학과 안용훈입니다. 오늘은 황화물 고체전해질을 계산으로 스크리닝한 이야기인데, '무엇을 찾았나'만큼 '무엇을 저희 손으로 철회했나'를 같이 보여드리겠습니다. 철회 기록이 왜 숨길 일이 아니라 보여드릴 성과인지, 오늘 그걸 설득해 보겠습니다.\n[용어] sulfide solid electrolyte(황화물 고체전해질): 액체 전해질을 대체하는 이온전도성 고체. 우리 대상은 아지로다이트 Li6PS5Cl 계열.");
}
// ═══ 2. MAP ═════════════════════════════════════════════════════════════════
{
  const s=newSlide();
  kickerTitle(s, "Roadmap", "One loop, six stops");
  mapDiagram(s, 0.55, 3.0, 8.9, -1, true);
  bullets(s,[
    {t:"ASK → TOOLS → ORIGIN → SCREEN → COMBINE → VERIFY → (back)", b:true},
    {t:"The last stop feeds the first ones — that returning arrow IS the method", color:RED, b:true},
    {t:"Each part opens by lighting its stop on this map", sub:true},
  ], 0.55, 1.5, 8.9, 1.2, 13);
  s.addText("ask · measure · learn · gate · combine · doubt",
    {x:0.55, y:6.3, w:8.9, h:0.35, fontFace:"Arial", fontSize:12, italic:true, color:NAVY, align:"center", margin:0});
  s.addNotes("발표 전체가 이 한 바퀴입니다. 여섯 정거장 - 묻고, 재고, 배우고, 거르고, 엮고, 마지막에 의심합니다. 그리고 의심에서 나온 화살표가 다시 앞으로 돌아갑니다. 이 되돌아가는 화살표가 오늘 발표의 핵심 주장입니다. 각 Part 시작마다 이 지도에 지금 어디인지 표시하겠습니다.\n[Q] 왜 지도부터? -> 마지막 정거장(VERIFY)이 논지라서, 구조를 먼저 보여야 앞 다섯이 왜 필요한지 보입니다.");
  footer(s);
}
// ═══ Part 1 ═════════════════════════════════════════════════════════════════
divider("Part 1","1","ASK — why compute at all","Too many candidates, experiments are slow — and what makes a screen trustworthy",0,
 "1부. 문제 정의와 논지입니다.");
{ // S1
  const s=newSlide();
  kickerTitle(s,"Motivation","The screening problem","Sendek et al., EES 2017 · EIS = impedance spectroscopy");
  // left: fanout diagram drawn with shapes
  const bx=0.55, by=1.7;
  s.addShape(p.ShapeType.roundRect,{x:bx,y:by+1.05,w:1.5,h:0.6,rectRadius:0.06,fill:{color:NAVY}});
  s.addText("Li₆PS₅Cl\nhost",{x:bx,y:by+1.05,w:1.5,h:0.6,align:"center",valign:"middle",color:"FFFFFF",fontSize:10,bold:true,fontFace:"Arial",margin:0});
  const knobs=["halogen species","halogen ratio","dopant (47)","dose x (3)"];
  knobs.forEach((k,i)=>{
    const ky=by+i*0.72;
    s.addShape(p.ShapeType.line,{x:bx+1.5,y:by+1.35,w:0.55,h:ky+0.27-(by+1.35),line:{color:MUT,width:1}});
    s.addShape(p.ShapeType.roundRect,{x:bx+2.05,y:ky,w:1.75,h:0.54,rectRadius:0.05,fill:{color:LIGHT},line:{color:NAVY,width:1}});
    s.addText(k,{x:bx+2.05,y:ky,w:1.75,h:0.54,align:"center",valign:"middle",color:NAVY,fontSize:9.5,fontFace:"Arial",margin:0});
  });
  s.addText("× multiplicative",{x:bx+2.05,y:by+3.0,w:1.75,h:0.3,fontSize:9.5,italic:true,color:RED,align:"center",fontFace:"Arial",margin:0});
  caption(s,"Four independent knobs on one host — the space grows as a product",bx,by+3.45,3.35);
  // right bullets + mini funnel preview
  bullets(s,[
    {t:"One experiment = synthesis + XRD + EIS + cell ≈ weeks", b:true},
    {t:"One calculation = hours–days", b:true},
    {t:"Computation does not replace experiments — it narrows where they go", color:NAVY, b:true},
    {t:"Preview of our funnel (drawn the field's way):", gap:2},
  ],4.35,1.6,5.1,2.2,12.5);
  const fun=[47,43,25,11,1], labs=["pool","G2","G3","G4","G5"];
  fun.forEach((v,i)=>{
    const fw=2.6*(v/47)+0.25, fy=3.9+i*0.52;
    s.addShape(p.ShapeType.rect,{x:4.6,y:fy,w:fw,h:0.4,fill:{color:i===4?RED:NAVY}});
    s.addText(labs[i]+"  "+v,{x:4.6+fw+0.08,y:fy+0.04,w:1.3,h:0.32,fontSize:10,color:INK,fontFace:"Arial",margin:0});
  });
  s.addNotes("아지로다이트 하나에도 조절 손잡이가 네 개고 이건 곱으로 늘어납니다. 실험 한 점이 몇 주, 계산 한 점이 몇 시간이면 - 계산의 일은 대체가 아니라 실험이 갈 곳을 좁히는 것입니다.\n[Q] 계산이 몇 시간이라는 근거? -> SCF/relax 급 기준. MD/NEB는 며칠 - 그래서 3-tier로 싼 것부터 겁니다.\n[용어] argyrodite: Ag8GeS6 광물형 구조족, Li6PS5Cl이 대표. EIS: 교류 임피던스로 이온전도도 측정.");
  footer(s);
}
{ // S2
  const s=newSlide();
  kickerTitle(s,"Motivation","Screening is only as good as its gates");
  bullets(s,[
    {t:"Screening talks end with “we found X out of N” — the pass side", b:true},
    {t:"The harder question: did the wrong ones actually fail?  That is rarely reported", b:true, color:NAVY},
    {t:"This talk puts 11 of our own verdicts under audit — 9 retracted — with the gate that caught each", b:true, color:RED},
    {t:"One of the 11 was presented as a conclusion in our previous seminar deck", i:true},
  ],0.55,1.5,8.9,2.0,13);
  // contrast boxes
  const y0=3.8;
  s.addShape(p.ShapeType.roundRect,{x:0.55,y:y0,w:4.25,h:2.5,rectRadius:0.08,fill:{color:SOFT},line:{color:RULE,width:1}});
  s.addText("usual funnel",{x:0.75,y:y0+0.15,w:3.9,h:0.3,bold:true,fontSize:12,color:MUT,fontFace:"Arial",margin:0});
  [2.6,1.9,1.2,0.5].forEach((fw,i)=>{ s.addShape(p.ShapeType.rect,{x:0.85+(2.6-fw)/2,y:y0+0.62+i*0.32,w:fw,h:0.22,fill:{color:"C9CDD3"}}); });
  s.addText("pass counts only\nfalse rejects invisible",{x:0.75,y:y0+1.95,w:3.9,h:0.5,fontSize:10.5,color:MUT,fontFace:"Arial",margin:0});
  s.addShape(p.ShapeType.roundRect,{x:5.2,y:y0,w:4.25,h:2.5,rectRadius:0.08,fill:{color:LIGHT},line:{color:NAVY,width:1.5}});
  s.addText("ours",{x:5.4,y:y0+0.15,w:3.9,h:0.3,bold:true,fontSize:12,color:NAVY,fontFace:"Arial",margin:0});
  [2.6,1.9,1.2,0.5].forEach((fw,i)=>{ s.addShape(p.ShapeType.rect,{x:5.5+(2.6-fw)/2,y:y0+0.62+i*0.32,w:fw,h:0.22,fill:{color:NAVY}});
    s.addText("×",{x:5.5+(2.6-fw)/2+fw+0.05,y:y0+0.56+i*0.32,w:0.3,h:0.3,fontSize:13,bold:true,color:RED,fontFace:"Arial",margin:0}); });
  s.addText("every rejection carries its reason\n9 retractions + 2 flags published",{x:5.4,y:y0+1.95,w:3.9,h:0.5,fontSize:10.5,color:INK,fontFace:"Arial",margin:0});
  s.addNotes("스크리닝 발표는 보통 '몇 개에서 몇 개를 찾았다'로 끝납니다. 더 어려운 질문은 '떨어져야 할 게 정말 떨어졌나'인데, 이걸 보고하는 발표가 드뭅니다. 저희는 그걸 표로 보여드리겠습니다 - 저희 판정 열한 건을 감사대에 올렸고 아홉 건을 철회했습니다. 그리고 이 열한 개 중 하나는 실제로 지난 세미나에서 결론으로 발표됐던 숫자입니다. 오늘 그 철회부터 보여드립니다.\n[Q 핵심 1합] 철회가 많다 = 부실? -> 철회 건수는 신뢰도의 반대 지표가 아니라 게이트 밀도의 지표입니다. 게이트 없는 파이프라인은 철회가 0건입니다 - 틀린 게 없어서가 아니라 못 찾아서입니다.\n[Q 핵심 2합 - 사후 명명 공격] '오류를 발견한 뒤에 게이트라고 이름 붙인 것 아닌가' -> 절반은 인정합니다. 오류가 규칙을 낳았습니다. 하지만 규칙이 코드에 박힌 뒤에는 사람이 아니라 규칙이 잡습니다: 7번(SDCP)은 'UMA는 전하 분리를 판정할 수 없다'를 사고 전에 미리 코드에 박아둔 규칙이 잡았고, 11번은 자동 감사기가 잡았고, 11건 중 6건이 지난 사흘간 돌던 게이트에서 나왔습니다.\n[EN] Isn't that a red flag? -> A pipeline with no gates reports zero retractions - not because nothing is wrong but because nothing is checked.");
  footer(s);
}
// ═══ Part 2 ═════════════════════════════════════════════════════════════════
divider("Part 2","2","TOOLS — what they give, what they cannot","DFT and MLIP, each closed with “so what do we not trust”",1,
 "2부는 DFT 강의가 아닙니다. 뒤에 나올 게이트들이 왜 필요한지 물리로 정당화하는 것뿐입니다. 7분 안에 끝냅니다.");
{ // S3
  const s=newSlide();
  kickerTitle(s,"Tools · DFT","Where the approximation enters","He et al., EEM 2019 · XC = exchange–correlation");
  // left diagram
  const dx=0.55, dy=1.7, dw=3.6;
  const box=(y,txt,fill,line,color)=>{ s.addShape(p.ShapeType.roundRect,{x:dx,y:y,w:dw,h:0.72,rectRadius:0.06,fill:{color:fill},line:{color:line,width:1.25}});
    s.addText(txt,{x:dx,y:y,w:dw,h:0.72,align:"center",valign:"middle",fontSize:10.5,color:color,fontFace:"Arial",margin:0}); };
  box(dy,"Ψ(r₁…r_N) — 3N dimensions\n(unstorable)",SOFT,MUT,MUT);
  s.addShape(p.ShapeType.line,{x:dx+dw/2,y:dy+0.72,w:0,h:0.34,line:{color:NAVY,width:1.75,endArrowType:"triangle"}});
  s.addText("Hohenberg–Kohn",{x:dx+dw/2+0.1,y:dy+0.76,w:2.0,h:0.25,fontSize:8.5,italic:true,color:NAVY,fontFace:"Arial",margin:0});
  box(dy+1.06,"electron density n(r) — 3-D",LIGHT,NAVY,NAVY);
  s.addShape(p.ShapeType.line,{x:dx+dw/2,y:dy+1.78,w:0,h:0.34,line:{color:NAVY,width:1.75,endArrowType:"triangle"}});
  s.addText("Kohn–Sham",{x:dx+dw/2+0.1,y:dy+1.82,w:2.0,h:0.25,fontSize:8.5,italic:true,color:NAVY,fontFace:"Arial",margin:0});
  box(dy+2.12,"KS orbitals + E_xc[n]\n← the ONLY approximation",("FFFFFF"),RED,RED);
  caption(s,"One place of approximation ⇒ predictable error character",dx,dy+3.0,dw);
  bullets(s,[
    {t:"Semi-local (PBE) underestimates gaps 30–50% — missing derivative discontinuity, not “inaccuracy”", b:true},
    {t:"DFT+U for localized d/f states — our Ni 3d, U = 6.2 eV", b:true},
    {t:"U is an empirical parameter — fix it, quote only same-U differences", sub:true},
  ],4.5,1.7,5.0,2.6,12);
  s.addShape(p.ShapeType.roundRect,{x:0.55,y:5.6,w:8.9,h:0.8,rectRadius:0.08,fill:{color:LIGHT},line:{color:NAVY,width:1.25}});
  s.addText("If one line survives from this part: the approximation enters once, so error character is predictable, so we never quote absolute gaps",
    {x:0.8,y:5.6,w:8.4,h:0.8,fontSize:12.5,bold:true,color:NAVY,fontFace:"Arial",align:"center",valign:"middle",margin:0});
  s.addNotes("전자가 백 개면 파동함수가 삼백 차원이라 저장이 안 됩니다. 첫 도약이 Hohenberg-Kohn이고요, 바닥상태는 3차원 밀도만으로 결정됩니다. 두 번째 도약이 Kohn-Sham인데요, 같은 밀도를 주는 가짜 전자계로 바꿔서 풉니다. 모르는 부분은 전부 한 항 - 교환상관 항에 몰아넣고요. 요점은 하나입니다: 근사가 한 곳에만 들어가니까 오차의 성격을 예측할 수 있고, 그래서 저희는 갭 절대값을 안 씁니다. Ni 3d의 U 6.2도 경험 파라미터라서 고정하고 같은 U 안의 차이만 인용합니다. (90초 컷)\n[질문 대비 - 미분 불연속 1분 설명] 전자 수 N을 연속으로 늘리면 총에너지 곡선이 정수마다 꺾여야 하고, 그 꺾임(도함수의 점프)이 갭의 일부입니다. PBE 같은 semi-local 범함수는 이 점프가 0이라 그만큼 갭이 작게 나옵니다 - 부정확이 아니라 구조적 부재.\n[Q] 왜 hybrid 안 쓰나 -> 273계산 스크리닝에 비용 두 자릿수. 순위 문제라 같은 방법 안 차이면 충분.\n[Q] U=6.2 출처 -> MP VASP GGA+U 관례값과 동일 계보. 인용 전 원전 확인 조건을 입력 주석에 박아둠.");
  footer(s);
}
{ // S4
  const s=newSlide();
  kickerTitle(s,"Tools · DFT","From total energy to observables — and into which gate","EOS · VRH · ESW · BVSE defined in Appendix A1–A2");
  s.addTable([
    [{text:"Quantity",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}},{text:"Judges",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}},{text:"Used in gate",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}}],
    ["E(V) → BM3 EOS","B₀ (stiffness)","G5 mechanical"],
    ["C_ij → VRH","E, G, Pugh ratio","G5 mechanical"],
    ["grand-potential hull","ESW window · oxidation onset","G2 window + G3 oxidation"],
    ["BVSE (bond valence)","channels, bottlenecks (cheap)","G4 transport — the gate engine"],
    ["MLIP-MD → MSD → Arrhenius","Ea, D","champion validation (after the gates)"],
    ["fixed-occupation nscf eigenvalues","band gap = e⁻ insulation","diagnostic axis, not a gate"],
    ["ICOHP / ELF / Bader","bonding character","not a gate; explanation only"],
  ],{x:0.55,y:1.5,w:8.9,fontFace:"Arial",fontSize:10.5,color:INK,border:{type:"solid",color:RULE,pt:0.75},
     colW:[3.4,3.2,2.3],rowH:0.34,valign:"middle",margin:0.04});
  bullets(s,[
    {t:"Gap rule: fixed-occupation eigenvalues ONLY — DOS-threshold reading under-estimates by ~0.3 eV (we did it once; see the retraction table)", b:true, color:RED},
    {t:"ICOHP sign convention: negative = bonding — always printed on the table", sub:true},
    {t:"Nothing on this ladder reaches particle/electrode scale", b:true},
  ],0.55,4.7,8.9,1.7,11.5);
  s.addNotes("총에너지 하나에서 사다리처럼 내려옵니다. 여기 규율 하나 - 갭을 DOS 문턱으로 읽지 않습니다. 0.3 eV 과소평가, 실제로 겪었고 철회 목록에 있습니다. ICOHP/ELF는 게이트가 아니라 설명 변수. 이 사다리 어디에도 입자 스케일은 없습니다 - 원자 계산으로 전극 성능을 직접 말할 수 없습니다.\n[Q] BVSE로 왜 Ea를 안 내나 -> 정적 격자 프록시라 순위/병목 판독용. 정량은 MD로만.\n[용어] fixed occupations: 정수 점유 고정 계산, 절연체 갭의 정본 판독법. grand potential: Li 화학퍼텐셜을 변수로 둔 퍼텐셜 - 전압축 안정성 판정.");
  footer(s);
}
{ // S5
  const s=newSlide();
  kickerTitle(s,"Tools · MLIP","Machine-learned potentials: what they buy, what they cannot","kb/results/mlip_md_diffusive_gate · UMA = universal MLIP (Meta)");
  bullets(s,[
    {t:"UMA (omat head): 200 ps MD, hundreds of atoms — impossible with DFT-MD", b:true},
    {t:"Three failures measured in OUR systems:", b:true, gap:2},
    {t:"① no explicit charge states — bit us in SDCP (Part 6)", sub:true},
    {t:"② cannot select magnetic states — Ni oxides AFM/FM", sub:true},
    {t:"③ no dispersion in training — fatal for physisorption", sub:true},
    {t:"Banned on Li₃N (deterministic bias, 2026-06); validated standard on LPSCl family", b:true},
    {t:"⇒ MLIP = screening-stage surrogate; champions go back to DFT", color:NAVY, b:true},
  ],0.55,1.5,4.7,4.6,11.5);
  img(s, SCR+"msd_crop.png", 5.4,1.6,4.1,3.0,
      "MLIP-MD Li MSD, LPSCl vs LPSCl₁.₆ (multi-T; 100 ps window shown)");
  s.addNotes("[그림 단서] 이 그림의 피팅 음영은 표시용 창이고 정본 MSD 창은 2-50 ps 고정 - 질문 나오면 그렇게 답한다.\nDFT로 200 ps MD는 불가능합니다. 그래서 MLIP. 다만 저희 계에서 실측으로 확인된 한계가 셋: 전하 상태를 못 다루고(이게 Part 6에서 제일 비싼 교훈으로 돌아옵니다), 자기 상태를 못 고르고, 분산력이 훈련에 없습니다. Li3N에는 금지 - 결정론적 편향 확인. 원칙은 하나: MLIP는 스크리닝 대체 모델, 챔피언은 반드시 DFT 재검.\n[Q] MLIP 오차? -> 계/물성마다 달라 오차 '값'보다 실패 유형(전하/자기/분산)으로 관리 - 유형에 걸리는 질문은 MLIP로 안 닫습니다.\n[용어] omat: UMA 무기재료 헤드. deterministic bias: 시드를 바꿔도 같은 방향으로 틀리는 오차.");
  footer(s);
}
// ═══ Part 3 ═════════════════════════════════════════════════════════════════
divider("Part 3","3","ORIGIN — where our axes came from","Li₆PS₅Cl vs Li₅.₄PS₄.₄Cl₁.₆: the lesson that designed the screen",2,
 "3부. 축 설계의 기원입니다. '결과 자랑'이 아니라 '이 결과가 축 설계를 바꿨다'가 요지.");
{ // S6
  const s=newSlide();
  kickerTitle(s,"Origin","The electronic structure barely moves","gap = fixed-occ eigenvalues · ICOHP: negative = bonding");
  img(s, REPO+"docs/figures/deck_extracted/elf_comp1.png", 0.55,1.6,4.3,2.85, "ELF, Li₆PS₅Cl");
  img(s, REPO+"docs/figures/deck_extracted/elf_modelc.png", 5.15,1.6,4.3,2.85, "ELF, Li₅.₄PS₄.₄Cl₁.₆ — near-identical topology");
  s.addTable([
    [{text:"",options:{fill:{color:NAVY}}},{text:"Li₆PS₅Cl",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}},{text:"Li₅.₄PS₄.₄Cl₁.₆",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}},{text:"Δ",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}}],
    ["gap (eV)","2.066","2.099",{text:"0.033",options:{bold:true,color:RED}}],
    ["ICOHP PS₄ (eV/bond)","−5.938","−6.000","≈0"],
  ],{x:1.7,y:4.85,w:6.6,fontFace:"Arial",fontSize:10.5,color:INK,border:{type:"solid",color:RULE,pt:0.75},rowH:0.3,valign:"middle",margin:0.04});
  bullets(s,[{t:"Absolute values not quoted (PBE); within-method differences only — and the smallness IS the result", b:true, color:NAVY}],0.55,5.9,8.9,0.5,11.5);
  s.addNotes("출발점. Cl을 늘리면 전도도가 오르는데, 왜? 전자구조 가설부터 봤습니다. 갭 차이 0.033 eV, ICOHP 거의 동일, ELF 두 장도 사실상 같은 그림. 차이가 작다는 것 자체가 결론입니다 - 이득은 여기서 오지 않았습니다.\n(질문 오면) 이 갭 4종은 지금 재현성 감사 중 - P30에서 정면으로 다룹니다.\n[Q] 0.033이 오차보다 큰가 -> 같은 프로토콜 안의 차이라 방법 오차는 공통 모드로 상쇄. 어느 쪽이든 '작다' 판정은 불변.\n[용어] ELF: 전자 국재도(0-1), 결합의 모양을 보는 지도.");
  footer(s);
}
{ // S7
  const s=newSlide();
  kickerTitle(s,"Origin","The gain is structural, not electronic");
  img(s, REPO+"docs/figures/bv_path_annotated_modelc.png", 0.55,1.5,5.0,4.6,
      "BV percolation path, LPSCl₁.₆ — vacancy sites line the hop network (empty-lattice proxy; ranking by MLIP-MD)");
  bullets(s,[
    {t:"More Cl → Li vacancies (charge balance) + 4d Cl anti-site → hop network opens", b:true},
    {t:"The static BVSE channel actually shrinks (−15%) — the gain is dynamic: vacancies in motion", sub:true},
    {t:"Substitution acts through disorder, not bands", b:true, color:NAVY},
    {t:"⇒ screening axes = structural descriptors:", b:true, gap:2},
    {t:"disorder promotion · Li transport · dose robustness · structural stability", sub:true},
    {t:"Electronic axis kept as a gate only — never a ranking variable", color:RED, b:true},
  ],5.85,1.6,3.65,4.4,11.5);
  s.addNotes("바뀐 건 구조입니다. Cl이 늘면 전하 균형 때문에 Li 공공이 늘고, anti-site 무질서가 커져서 홉 네트워크가 열립니다. 왼쪽 그림이 그 네트워크인데요, 경로를 따라 늘어선 자리들이 전부 vacancy 자리입니다. 그래서 스크리닝 축을 전자 기술자가 아니라 구조 기술자로 세웠습니다. 전자절연은 게이트로만 씁니다. 이 한 장이 cascade의 설계 이유입니다.\n[Q] 무질서가 이득이라는 직접 증거 -> MD에서 공공 농도와 D의 동반 상승이 직접 증거입니다(beta 게이트 통과분만 인용). ⚠ BVSE 채널%는 여기서 근거로 쓰지 않는다 - 채널 부피는 D0쪽(prefactor) 지표라 Ea/σ 순위를 못 매긴다는 걸 저희 CSV 헤더에 직접 박아 뒀다(LPSOCl은 채널 +43%인데 Ea가 더 높음). '채널% 증가' 답변 금지.\n[용어] anti-site: 원소가 남의 자리(Cl-S)에 앉는 점결함. percolation: 경로가 셀 전체를 관통하게 이어지는 문턱 현상. empty-lattice proxy: 빈 격자에 Li 탐침 하나 - 지형 모양 기술용, 측정 Ea 아님(그림 하단 단서 그대로).");
  footer(s);
}
// ═══ Part 4 ═════════════════════════════════════════════════════════════════
divider("Part 4","4","SCREEN — the field's way, then ours","47 dopants · 273 calculations · 5 gates · 14 axes — and why the funnel cannot close it",3,
 "4부가 제일 깁니다. 문헌 실물 2장 -> 우리 파이프라인 -> 게이트 -> 워터폴 -> 그리고 반박.");
{ // S8 sendek
  const s=newSlide();
  kickerTitle(s,"Screen · the field","How the field screens ①: 12,831 → 21","Sendek et al., EES 2017, 10, 306");
  img(s, REPO+"litdb/figures/sendek2017_ml_screening_12k_conductors/fig_1.png", 0.55,1.5,8.9,3.3,
      "Two tracks: structure screening (12,831 candidates) + model building on 40 measured conductors (Sendek 2017)");
  bullets(s,[
    {t:"4 prerequisite gates (E_hull = 0 · gap ≥ 1 eV · V_ox ≥ 4 V · no TM) → 317; logistic classifier trained on 40 measured σ → 21 (0.16%)", b:true},
    {t:"Their lesson: prerequisite gates cut harder than the conductivity screen (model alone leaves 1,408)", color:NAVY, b:true},
    {t:"Remember “40” — our dopant pool is 47: same weight class, we inherit their small-sample defenses", color:RED, b:true},
  ],0.55,5.05,8.9,1.5,11);
  s.addNotes("실물부터. Sendek은 만이천여 종에서 전제조건 게이트 4개로 317, 실측 전도도 40종으로 훈련한 분류기로 21종. 교훈: 전도도 스크린보다 전제조건 게이트가 더 세게 거릅니다. 분류기만 쓰면 1,408종이 남아요. '40종 훈련셋'을 기억해 두세요 - 저희 47종과 체급이 같아 소표본 방어 절차를 계승합니다.\n[Q] 40개로 훈련한 모델을 믿나 -> LOOCV, 전수 조합 특징선택, X-randomization으로 방어했고 우리도 같은 절차(P24). 핵심은 '맞다'가 아니라 '방어 절차가 문서화됐다'.\n[용어] LOOCV: 표본 1개를 빼고 학습-예측을 전 표본 반복. 소표본 표준 검증.");
  footer(s);
}
{ // S9 xiao + richards
  const s=newSlide();
  kickerTitle(s,"Screen · the field","How the field screens ②: thermodynamic gates at scale","Xiao et al., Joule 2019 · Richards et al., Chem. Mater. 2016");
  img(s, REPO+"litdb/figures/xiao2019_cathode_coating_screening/fig_2.png", 0.55,1.55,4.6,2.9,
      "Survivors per filter, by chemistry (Xiao 2019: 104,082 → 184)");
  img(s, SCR+"richards_fig2_annot.png", 5.5,1.4,3.95,4.6,
      "Stability windows by anion — sulfides are the narrow bars (Richards 2016; box added)");
  bullets(s,[
    {t:"Same skeleton everywhere: cheap gates first, expensive validation last", b:true},
    {t:"The narrow sulfide windows (incl. Li₆PS₅Cl) are exactly why we hunt dopants", color:NAVY, b:true},
  ],0.55,4.9,4.6,1.6,11);
  s.addNotes("Ceder 계열 실물 둘. Xiao는 십만 종을 hull/안정창/반응성 게이트로 184까지. Richards의 오른쪽 그림 - 음이온별 안정창인데 황화물이 저 좁은 막대들입니다. Li6PS5Cl도 저기 있습니다. 이 좁은 창이 저희가 도펀트를 찾는 이유 그 자체. 구조는 어디나 같습니다: 싼 게이트 먼저, 비싼 검증 나중.\n[스킵라인] 'Xiao/Richards도 같은 깔때기 구조입니다 - 그림은 부록에'.\n[Q] 코팅 논문이 왜 비교되나 -> 대상은 다르지만 게이트 축/임계값 설계가 1:1 벤치마크. force-fit은 안 합니다.");
  footer(s);
}
{ // S10 common + advantage
  const s=newSlide();
  kickerTitle(s,"Screen · the field","The common funnel, and the two boxes it rarely fills");
  bullets(s,[
    {t:"Rarely reported ①: failure rates of the gates themselves — false rejects invisible", b:true},
    {t:"Rarely entered ②: single-dopant frame — combinations left unexplored", b:true},
  ],0.55,1.5,8.9,1.0,12.5);
  s.addTable([
    [{text:"Ours",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}},{text:"Receipt",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}}],
    ["Gate failure record — 11 self-retractions published","Part 6 of this talk"],
    ["Combinatorial step — co-doping ML on top of ranking","Part 5"],
    ["Provenance registry — 28/28 wired, drift-checked on every run","live validator"],
    ["One repo: 188 property files · 164 literature digests · web app","reproducible"],
  ],{x:0.55,y:2.8,w:8.9,fontFace:"Arial",fontSize:11,color:INK,border:{type:"solid",color:RULE,pt:0.75},
     colW:[5.9,3.0],rowH:0.42,valign:"middle",margin:0.05});
  bullets(s,[
    {t:"Not “others don't verify” — the difference is publishing the failures and wiring the checks into the used path", i:true, color:MUT},
  ],0.55,5.3,8.9,0.6,11);
  s.addNotes("공통 구조에서 안 채워지는 칸이 둘. 게이트 자체의 실패율 - 잘못 떨어뜨린 걸 아무도 못 봅니다. 그리고 전부 단일 도펀트 프레임이라 조합이 못 들어옵니다. 저희가 채우려는 게 정확히 이 두 칸. 철회 기록 공개, 그리고 랭킹 위 co-doping 단계. 받치는 인프라 - 정본 레지스트리 28항목이 실시간 드리프트 검사.\n[Q] 남들도 내부 검증은 할 텐데 -> 맞습니다. 차이는 공개와 배선입니다. 우리는 철회를 지표로 발표하고, 검사기가 화면과 같은 경로를 봅니다.");
  footer(s);
}
{ // S11 our pipeline
  const s=newSlide();
  kickerTitle(s,"Screen · ours","Our pipeline: 273 run slots (91 × 3 labels) → 47 dopants with complete axes");
  // tier strip
  const tiers=[["Tier 1","UMA relax","all 273"],["Tier 2","property battery","EOS · window · transport · …"],["Tier 3","gates & axes","5 gates · 14 axes"]];
  tiers.forEach((t,i)=>{
    const tx=0.55+i*3.05;
    s.addShape(p.ShapeType.roundRect,{x:tx,y:1.55,w:2.75,h:0.95,rectRadius:0.07,fill:{color:i===2?NAVY:LIGHT},line:{color:NAVY,width:1.25}});
    s.addText([{text:t[0]+" — "+t[1]+"\n",options:{bold:true,fontSize:11,breakLine:true}},{text:t[2],options:{fontSize:9}}],
      {x:tx,y:1.55,w:2.75,h:0.95,align:"center",valign:"middle",color:i===2?"FFFFFF":NAVY,fontFace:"Arial",margin:0});
    if(i<2) s.addShape(p.ShapeType.line,{x:tx+2.78,y:2.02,w:0.24,h:0,line:{color:MUT,width:1.75,endArrowType:"triangle"}});
  });
  s.addText("91 curated compounds ran first (1–3 forms per dopant) → 47 dopants have all three axes populated; the other 44 fell to pipeline gaps, never counted as gate fails",
    {x:0.55,y:2.58,w:8.9,h:0.26,fontSize:9.5,italic:true,color:MUT,fontFace:"Arial",align:"center",margin:0});
  bullets(s,[
    {t:"⚠ x002/x005/x010 are campaign labels: the canonical CSV records concentration = 0.25, so nominal x is unresolved; every Δ is still referenced to the same undoped host cell", b:true, color:RED},
    {t:"Honesty header, shipped inside the data file (translated from its Korean original):", b:true, gap:2},
  ],0.55,2.95,8.9,0.85,11);
  s.addShape(p.ShapeType.roundRect,{x:0.8,y:3.8,w:8.4,h:1.05,rectRadius:0.07,fill:{color:SOFT},line:{color:RED,width:1.25}});
  s.addText("“Pass counts are NOT discovery metrics. This is a curated 47-dopant pool re-expressed through\nliterature-standard gates — not ‘we filtered N thousands’.”",
    {x:1.0,y:3.9,w:8.0,h:0.85,fontSize:11.5,italic:true,color:RED,fontFace:"Arial",valign:"middle",margin:0});
  placeholder(s,0.8,5.05,8.4,1.35,"web app  /cascade  (funnel card area)","Live cascade view (web app, synced to db/)");
  s.addNotes("저희 풀은 큐레이션된 47종. 화합물 91 x 농도 3점 = 273계산. 싼 것부터 - UMA 이완 전수, 물성 배터리, 게이트. 그리고 데이터 파일 맨 위 문장을 그대로 읽겠습니다: '이 통과 수는 발견 성능 지표가 아니다.' 저희는 만 종을 거른 게 아니라 사람이 고른 47종을 문헌 표준 게이트로 재표현한 겁니다. 이 구분을 흐리면 아까 Sendek 쪽과 억지 비교가 돼 버립니다. 그리고 47종이 왜 화합물 91개가 되는지 - 도펀트마다 산화물, Cl-rich 같은 화합물 형태가 하나에서 셋이라 91개입니다.\n[Q] 왜/어떻게 47종 -> 코팅 문헌/전구체/원자가 다양성 기준 화학 큐레이션 + 리뷰어 권고 확장. 선정 이력이 JSON pool_provenance에 단계별로.\n[용어] dose: 치환 분율 x. 도펀트마다 3점 강제 - 농도 내성 축의 재료.");
  footer(s);
}
{ // S11b — 화합물 전체 로스터 (사용자 요청 2026-08-11)
  const s=newSlide();
  kickerTitle(s,"Screen · ours","Every compound in this campaign, classified","source: cascade_seminar_scorecard_47.csv (groups, first-stop, deep-DFT)");
  const SUBD={"0":"₀","1":"₁","2":"₂","3":"₃","4":"₄","5":"₅","6":"₆","7":"₇","8":"₈","9":"₉"};
  const fsub=x=>x.replace(/\d/g,d=>SUBD[d]);
  const PASS=new Set(["Ag2O","CaF2","CaO","Li2O","LiF","MgF2","MgO","SiO2","SnO2","WO3","ZnO"]);
  const DEEP=new Set(["B2O3","Nd2O3"]);
  const GROUPS=[
    ["Transition metal (23)",["Ag2O","CoO","Cr2O3","CrO3","Cu2O","Fe2O3","HfO2","MnO","MoO3","Nb2O5","NiO","Sc2O3","ScF3","Ta2O5","TiF4","TiO2","V2O5","WO3","Y2O3","YF3","ZnO","ZrF4","ZrO2"]],
    ["Main group (9)",["Al2O3","AlF3","B2O3","Ga2O3","GeO2","In2O3","Sb2O5","SiO2","SnO2"]],
    ["Alkaline earth (6)",["BaO","CaF2","CaO","MgF2","MgO","SrO"]],
    ["Lanthanide (6)",["Gd2O3","La2O3","LaF3","Nd2O3","NdF3","Sm2O3"]],
    ["Alkali (3)",["Li2O","LiF","Na2O"]],
  ];
  function runs(list){
    const out=[];
    list.forEach((c,i)=>{
      out.push({text:fsub(c)+(DEEP.has(c)?"†":""), options:{fontSize:9.5, bold:PASS.has(c),
        color:PASS.has(c)?NAVY:INK}});
      if(i<list.length-1) out.push({text:"  ·  ",options:{fontSize:9.5,color:RULE}});
    });
    return out;
  }
  const boxes=[[0.55,1.55,3.15,3.5],[3.9,1.55,5.55,1.28],[3.9,2.98,2.7,1.05],[6.75,2.98,2.7,1.05],[3.9,4.18,2.7,0.87]];
  GROUPS.forEach((g,i)=>{
    const [bx,by,bw,bh]=boxes[i];
    s.addShape(p.ShapeType.roundRect,{x:bx,y:by,w:bw,h:bh,rectRadius:0.06,fill:{color:i===0?LIGHT:"FFFFFF"},line:{color:NAVY,width:1}});
    s.addText(g[0],{x:bx+0.12,y:by+0.06,w:bw-0.24,h:0.24,fontSize:9.5,bold:true,color:MUT,fontFace:"Arial",margin:0});
    s.addText(runs(g[1]),{x:bx+0.12,y:by+0.3,w:bw-0.24,h:bh-0.38,fontFace:"Arial",valign:"top",margin:0});
  });
  s.addText([{text:"bold navy",options:{bold:true,color:NAVY,fontSize:9}},{text:" = through G4 (11)   ",options:{color:MUT,fontSize:9}},
             {text:"†",options:{color:INK,fontSize:9,bold:true}},{text:" = deep-DFT validated (2/47: B₂O₃, Nd₂O₃)",options:{color:MUT,fontSize:9}}],
    {x:6.75,y:4.25,w:2.75,h:0.75,fontFace:"Arial",margin:0});
  s.addShape(p.ShapeType.line,{x:0.55,y:5.28,w:8.9,h:0,line:{color:RULE,width:1}});
  s.addText([
    {text:"Hosts:  ",options:{bold:true,color:NAVY,fontSize:9.5}},
    {text:"Li₆PS₅Cl (comp1) · Li₅.₄PS₄.₄Cl₁.₆ (modelc) · +B₂O₃ · LPSOCl (+O)\n",options:{color:INK,fontSize:9.5,breakLine:true}},
    {text:"SEI decomposition phases:  ",options:{bold:true,color:NAVY,fontSize:9.5}},
    {text:"Li₂O · Li₂S · Li₃P · Li₃PO₄ · Li₃PO₄γ · LiCl (6 citable gaps)  +  ",options:{color:INK,fontSize:9.5}},
    {text:"LiNdO₂ · Nd₂O₃ · Nd₂S₃ (gap undefined in PBE+U → cite MP frozen-4f)\n",options:{color:RED,fontSize:9.5,breakLine:true}},
    {text:"Co-doping hypothesis pairs:  ",options:{bold:true,color:NAVY,fontSize:9.5}},
    {text:"Cr₂O₃+HfO₂ · Al₂O₃+Cr₂O₃ · HfO₂+In₂O₃ · Ga₂O₃+HfO₂ (not validated)",options:{color:INK,fontSize:9.5}},
  ],{x:0.55,y:5.42,w:8.9,h:1.15,fontFace:"Arial",valign:"top",margin:0});
  s.addNotes("발표에 나오는 화합물 전부를 한 장에 분류해 둔 로스터입니다. 전이금속 23, 주족 9, 알칼리토 6, 란타나이드 6, 알칼리 3 - 합쳐서 47이고, 진한 남색이 G4까지 통과한 11종, 단검 표시가 deep DFT까지 간 2종입니다. 아래 줄은 host 4계, SEI 분해상 9종(인용 가능 6 + Nd 3종은 MP 인용), co-doping 상위 4쌍입니다.\n[Q] 어느 게 최종 후보냐 -> 이 장은 후보 명단이 아니라 출연진 명단입니다. 판정은 각 파트에서.\n[Q] 빠진 원소는? -> A5b 마지막 문항 - Si/Sn/Zr 계는 있고, 예: P-site 치환계(Ge는 있음), S-site 계열(Se, Te), 그리고 Rb/Cs 같은 무거운 알칼리가 없습니다. pool_provenance 에 선정 이력.");
  footer(s);
}
{ // S12 gates detail
  const s=newSlide();
  kickerTitle(s,"Screen · ours","Five gates: metric, threshold, and why","G4 lineage: Kahle et al. 2020 (HT-AIMD)");
  s.addTable([
    [{text:"Gate",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}},{text:"Metric",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}},{text:"Threshold",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}},{text:"Physical basis",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}},{text:"Lit. analog",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}}],
    ["G1 structural","mean over x of Δe = E(doped)−E(host), UMA","Δe < 0  (zero = the host itself)","favorability vs the host — not an arbitrary cut","Xiao F2 · Sendek P1"],
    ["G2 window","grand-potential ESW width","window ≥ 0.05 V","a window must exist at all","Zhu 2015 · Xiao F3"],
    ["G3 oxidation","oxidation onset (V vs Li)","V_ox ≥ 2.14 V  (= undoped host onset)","must not be worse than the host","Richards windows"],
    ["G4 transport","BVSE proxy (x005 label), min–max norm","norm > 0.3 AND blocking < 0.6*","the property we exist for","Kahle HT-AIMD"],
    ["G5 mechanical","E (UMA) and G/B","E ≤ 46.9 GPa AND G/B ≤ 0.78  (roster medians)","soft + ductile keeps contact in SSB","—"],
  ],{x:0.55,y:1.5,w:8.9,fontFace:"Arial",fontSize:9,color:INK,border:{type:"solid",color:RULE,pt:0.75},
     colW:[1.2,2.35,2.15,2.0,1.2],rowH:0.56,valign:"middle",margin:0.04});
  bullets(s,[
    {t:"Two of five gates use the host as the zero point (G1, G3) — the cut is physics, not taste", b:true, color:NAVY},
    {t:"Δe uses the mean of 3 label champions (verified 47/47) — label-blind cherry-picking is structurally blocked", b:true},
    {t:"* blocking < 0.6 is a heuristic with no host/literature anchor; G5 is roster-relative ranking — so the physical funnel ends at G4", sub:true},
  ],0.55,5.35,8.9,1.2,11);
  s.addNotes("다섯 게이트를 한 표로. 컷 값을 그대로 읽어드리면 - 구조안정은 0인데 이게 host 자기 자신이고요, 산화 게이트의 2.14 V도 undoped host의 onset입니다. 다섯 중 둘이 host를 영점으로 씁니다. 창 게이트는 0.05 V - 창이 존재하기는 해야 한다는 최소 조건. 수송은 BVSE 프록시 정규화 0.3, 역학은 로스터 중앙값 이하(연질+연성). 그리고 농도 3점 챔피언 평균이라 제일 좋은 농도 하나만 골라 자랑하는 체리피킹이 구조적으로 막혀 있습니다.\n[Q] 임계값 민감도 -> 민감합니다. 그래서 다음 장 '1'을 결론으로 안 씁니다. 중앙값 컷(G5)은 정의상 로스터 의존이고, 그래서 게이트 상태와 값이 교차 못하게 평탄화 + 동점군 내 순위 무의미 명시.\n[Q] G4가 왜 MD가 아니라 BVSE 프록시? -> 273계산 전수에 MD는 불가능. 프록시로 거르고 챔피언만 MD/DFT 재검 - 3-tier의 요지.");
  footer(s);
}
{ // S13 waterfall
  const s=newSlide();
  kickerTitle(s,"Screen · ours","The waterfall, drawn the field's way");
  s.addChart(p.ChartType.bar, [{name:"survivors", labels:["pool","G1 structural","G2 window","G3 oxidation","G4 transport","G5 mechanical"], values:[47,47,43,25,11,1]}],
    {x:0.55,y:1.5,w:5.6,h:4.4, barDir:"col", chartColors:[NAVY], showValue:true, dataLabelPosition:"outEnd",
     dataLabelColor:INK, dataLabelFontSize:11, dataLabelFontFace:"Arial",
     catAxisLabelColor:INK, catAxisLabelFontSize:9, catAxisLabelFontFace:"Arial",
     valAxisHidden:true, valGridLine:{style:"none"}, catGridLine:{style:"none"}, showLegend:false, showTitle:false,
     valAxisMaxVal:52, valAxisLabelColor:MUT, valAxisLabelFontSize:8});
  bullets(s,[
    {t:"G1 47/47 = curated pool, not gate power (flagged vacuous in the JSON itself)", b:true},
    {t:"Unique-kill audit: G2's 4 kills (late-TM oxides) ALL also fail G3 — unique kill = 0", b:true},
    {t:"All 5! = 120 gate orders enumerated: terminal set invariant — the waterfall shape is narrative, not result", b:true, color:NAVY},
    {t:"G5 is ranking-only → the defensible physical endpoint is the G4 set of 11, not “1”", color:RED, b:true, gap:2},
  ],6.4,1.6,3.1,4.5,10.5);
  s.addNotes("문헌 방식 그대로 그리면 이렇게 됩니다. 이 깔때기를 감사하면 세 가지가 나옵니다. 첫째, 구조안정 47/47은 게이트가 세서가 아니라 풀이 안정 위주로 큐레이션된 결과 - 데이터 파일이 스스로 vacuous 플래그를 답니다. 둘째, 창 게이트 탈락 4종(late-TM 산화물)은 전부 산화 게이트에서도 떨어집니다 - unique kill 0, 중복 게이트. 셋째가 제일 중요한데, 다섯 게이트의 120개 순서를 전부 돌렸습니다. 최종 집합은 순서 불변입니다. waterfall 모양은 결과가 아니라 설명 순서입니다. 그리고 G4 blocking 컷은 휴리스틱, G5는 로스터 중앙값 정렬이라 물리적으로 방어 가능한 끝은 '1'이 아니라 G4 통과 11종입니다.\n[Q] WO3가 뭐가 좋았나 -> 다섯 게이트를 모두 통과한 유일 후보라는 사실뿐. G5 자체가 랭킹 전용이라 그 '1'을 후보 확정으로 안 씁니다.\n[출처] 120 순열: docs/cascade_pipeline_guide.md 366행(정본). unique kill: cascade_seminar_scorecard_47.csv 검산(G2 first-stop = CoO/Fe2O3/MnO/NiO, 전부 Vox<2.14).");
  footer(s);
}
{ // S14 why funnel fails
  const s=newSlide();
  kickerTitle(s,"Screen · ours","Why the funnel is the wrong endpoint for our question","Zhu et al., Angew. 2020 (hydrolysis map)");
  bullets(s,[
    {t:"① “1 survivor” is a property of the thresholds, not of chemistry — nudge a cut, the count moves", b:true},
    {t:"② Sequential AND destroys complementarity:", b:true, color:NAVY},
    {t:"a weak-transport / superb-oxidation dopant dies at G4 — exactly the one most valuable when paired", sub:true},
    {t:"③ Axes really collide — our own data, three ways at once:", b:true, color:RED},
    {t:"+B₂O₃: best MD free-energy barrier (PMF ΔF 0.16 eV @600 K, 4 systems) — yet the static transport axis rejects it, and air stability is worst-group (B₂S₃ hydrolysis −0.90 eV, 3rd-worst of 46 [Zhu20])", sub:true},
    {t:"One composite score cannot represent this candidate — high is a lie, low is a lie", b:true},
    {t:"⇒ ranking stays multi-objective (14 axes); the next step is combination, not elimination", b:true, color:NAVY, gap:2},
  ],0.55,1.5,5.3,4.9,11);
  img(s, SCR+"zhu_fig3a_annot.png", 6.0,1.55,3.5,3.4,
      "Hydrolysis vs reduction map (Zhu 2020; circle added) — B³⁺ at the bottom is the same B our MD landscape ranks best");
  s.addNotes("세 가지 이유. 첫째, 마지막 '1'은 화학이 아니라 임계값의 성질. 둘째가 핵심 - 순차 AND는 상보성을 구조적으로 파괴합니다. 수송이 약한데 산화안정이 뛰어난 후보는 수송 게이트에서 죽는데요, 그런 후보일수록 수송이 강한 후보와 짝지었을 때 제일 아깝습니다. 깔때기는 그 짝을 만들어 보기도 전에 버립니다. 셋째, 실제로 충돌합니다. 저희 B2O3는 수송 축 1등이면서, Zhu 그림 맨 아래 저 B3+ - 가수분해 -0.9로 공기안정 최악군. 이 후보를 점수 하나로 표현할 방법이 없습니다. 그래서 지우지 않고 엮는 쪽으로 갑니다.\n[Q] 다목적이면 결정 회피 아닌가 -> 용도가 축 가중을 정합니다. 드라이룸 공정이면 공기축 가중 다운. 결정권을 용도에 돌려주는 것.\n[EN] Isn't multi-objective just indecision? -> No - the application picks the weights; a funnel picks them for you, silently.\n[용어] PMF dF_perc: 시간평균 Li 밀도 자유에너지 지형의 퍼콜레이션 문턱(이 온도의 자유에너지, Ea 아님).");
  footer(s);
}
{ // S14b — the trade-off is systematic (Codex 대조에서 채택)
  const s=newSlide();
  kickerTitle(s,"Screen · ours","The trade-off is systematic: six for six","source: cascade_seminar_oxidation_transport_47.csv");
  img(s, REPO+"docs/figures/cascade/cascade_seminar_oxidation_transport_47.png", 0.55,1.5,6.2,4.7,
      "All six oxidation-raising candidates stop at the same transport gate (static proxy; not conductivity)");
  bullets(s,[
    {t:"Every candidate that raises the oxidation onset (Cr₂O₃/Ga₂O₃/In₂O₃/Sc₂O₃ +0.22 V · B₂O₃ +0.18 · Y₂O₃ +0.14) fails G4", b:true, color:RED},
    {t:"This is not one unlucky dopant — it is the shape of the chemistry", b:true},
    {t:"And it is why co-doping exists: these six are exactly the cathode-side halves of our top pairs (Cr₂O₃+HfO₂, Ga₂O₃+HfO₂, HfO₂+In₂O₃…)", b:true, color:NAVY},
  ],6.95,1.6,2.55,4.6,10.5);
  s.addNotes("한 장 더 - 이 충돌이 B2O3 하나의 불운이 아니라는 걸 보여드립니다. 산화 onset 을 host 위로 올린 후보가 여섯인데, 여섯 전부가 같은 수송 게이트에서 멈춥니다. 화학의 모양 자체가 이렇습니다 - 산화를 막는 강한 M-O 결합이 Li 경로도 막습니다. 그리고 이게 co-doping 이 존재하는 이유입니다. 이 여섯이 정확히 저희 상위 쌍의 양극측 절반입니다. Cr2O3+HfO2, Ga2O3+HfO2, HfO2+In2O3. 깔때기가 버린 후보들이 조합의 재료가 됩니다.\n[주의] G4는 정적 BVSE 프록시 - 전도도가 아니라 경로 위험 플래그. 그림 하단에 명기돼 있습니다.\n[출처] Codex 판 세미나 자료에서 채택, CSV 검산 완료(6/6 G4_pass=0).");
  footer(s);
}
// ═══ Part 5 ═════════════════════════════════════════════════════════════════
divider("Part 5","5","COMBINE — ranking to co-doping","Complementarity as the design variable — and an honest audit of the model",4,
 "5부. 다목적 랭킹 위에 조합을 얹습니다. R2 두 개를 정직하게 깝니다.");
{ // S15 14 axes
  const s=newSlide();
  kickerTitle(s,"Combine","Ranking without a funnel: strengths trade across axes","source: cascade_seminar_scorecard_47.csv");
  img(s, REPO+"docs/figures/cascade/cascade_seminar_scorecard_47.png", 0.55,1.45,8.9,3.35,
      "Per-axis percentiles + first-stop gate — no composite score, no winner (live 14-theme view: web app /cascade)");
  bullets(s,[
    {t:"14 themes: oxidative · reduction · e⁻-insulation · transport · disorder · dose-robustness · lightweight · low-cost · soft · ductile · air ×2 · structural · balanced", sub:true},
    {t:"Geometric mean = AND-like: one zero floors the composite  ·  Missing ≠ bad — excluded & flagged, never zero-filled", b:true, color:NAVY},
  ],0.55,5.35,8.9,1.1,10.5);
  s.addNotes("깔때기 대신 이렇게 둡니다. 축 열넷, 조합은 기하평균 - 한 축이 바닥이면 종합도 바닥인 AND 성질. 데이터 없는 축은 0이 아니라 제외 후 명시 - 0으로 깔면 '모름'이 '나쁨'으로 둔갑합니다. 축마다 챔피언이 다른 게 화면에서 바로 보입니다 - 그게 조합으로 가는 이유입니다.\n[용어] geometric mean: 곱의 n제곱근. 한 축의 0을 다른 축이 못 가려 줌.");
  footer(s);
}
{ // S16 co-doping
  const s=newSlide();
  kickerTitle(s,"Combine","Co-doping: complementarity as the design variable","synergy = max(joint-window gain, 0) × radius-match × stability");
  s.addTable([
    [{text:"Pair",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}},{text:"joint window (V)",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}},{text:"vs best single",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}},{text:"radius match",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}},{text:"tag",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}}],
    [{text:"Cr₂O₃ + HfO₂",options:{bold:true}},"1.114",{text:"+0.360",options:{bold:true,color:RED}},"0.87","anode↔cathode"],
    ["Al₂O₃ + Cr₂O₃","0.984","+0.216","0.90","anode↔cathode"],
    ["HfO₂ + In₂O₃","1.114","+0.323","0.88","anode↔cathode"],
    ["Ga₂O₃ + HfO₂","1.114","+0.336","0.88","anode↔cathode"],
  ],{x:0.55,y:1.5,w:8.9,fontFace:"Arial",fontSize:10.5,color:INK,border:{type:"solid",color:RULE,pt:0.75},
     colW:[2.2,1.9,1.7,1.5,1.6],rowH:0.34,valign:"middle",margin:0.04});
  s.addText("rows 1/3/4 share 1.114 V because the oxidation end is set by HfO₂ (common) — the reduction end is the partner's job",
    {x:0.55,y:3.28,w:8.9,h:0.24,fontSize:8.5,italic:true,color:MUT,fontFace:"Arial",margin:0});
  bullets(s,[
    {t:"Top pairs are ALL anode↔cathode — complementarity is doing the work", b:true, color:NAVY},
    {t:"Is it even makeable?  Three checks before believing:", b:true, gap:2},
    {t:"① site competition — do Cr³⁺ and Hf⁴⁺ target the same host site?  (InF₃ precedent: In→P 4b, F→Cl 4a — different sites = the success pattern)", sub:true},
    {t:"② charge arithmetic — M³⁺→P gives +2 Li, M⁴⁺→P gives +1 Li; the Li count must close", sub:true},
    {t:"③ co-substituted formation energy — needs the supercell calculation (next slide)", sub:true},
    {t:"File header, verbatim: “co-doping synergy HYPOTHESES (single-dopant proxy, not validated)”", i:true, color:RED, gap:2},
  ],0.55,3.6,8.9,3.0,10.5);
  s.addNotes("조합의 아이디어는 단순합니다. 양극 쪽 막는 도펀트 + 음극 쪽 막는 도펀트로 합동 창을 넓히자. 반경 정합을 곱하고요. 1등 Cr2O3+HfO2 - 단일 최고보다 0.36 V 넓고 상위가 전부 anode-cathode 태그. 상보성이 실제로 구동 변수로 잡혔습니다. 그런데 - 만들 수는 있나? 세 점검: 자리 경쟁(InF3 선례는 서로 다른 자리 = 성공 패턴), 전하 산술, 공동 치환 형성에너지. 앞 둘은 지금 데이터로 점검 가능, 셋째가 계산 필요. 파일 첫 줄에 '가설, 미검증' 박아둔 이유.\n[Q] 실험 선례 -> 아지로다이트 한 염 두 도펀트 계보가 litdb에 있습니다 - 연도순 CuCl(2021), MgF2(2023), InF3(2024), CuBr2/La2O3(2025), GaF3(2026). InF3(2024)가 이 그룹 자리배정의 원본입니다.\n[Q] 비율은? -> 다음 장 - 지금 모델엔 비율 축이 없다는 게 정직한 답.\n[용어] joint window: max(산화한계)-min(환원한계) - 두 상이 양쪽을 각각 커버한다는 상보 가정.");
  footer(s);
}
{ // S17 ML anatomy
  const s=newSlide();
  kickerTitle(s,"Combine","What the model actually knows","ridge · λ by 1-SE rule · LOOCV");
  s.addTable([
    [{text:"Stage",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}},{text:"Target",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}},{text:"n",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}},{text:"LOOCV R²",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}},{text:"Reading",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}}],
    ["1  ridge","our cascade score (composite)","47",{text:"0.9998",options:{bold:true}},"not success: it dissected our own formula"],
    [{text:"2  pair features",options:{color:MUT}},{text:"feature construction (min/max/avg + quadratic)",options:{color:MUT}},{text:"—",options:{color:MUT}},{text:"—",options:{color:MUT}},{text:"construction stage — no CV target",options:{color:MUT}}],
    ["3  interaction","pair synergy","1,081 pairs",{text:"0.089",options:{bold:true,color:RED}},"honest number — interactions essentially unlearned"],
  ],{x:0.55,y:1.5,w:8.9,fontFace:"Arial",fontSize:10,color:INK,border:{type:"solid",color:RULE,pt:0.75},
     colW:[1.1,2.6,1.0,1.2,3.0],rowH:0.5,valign:"middle",margin:0.04});
  bullets(s,[
    {t:"And 0.089 is the OPTIMISTIC number: dopant-level CV (LODO/L2DO) drives R² negative (−0.18 / −0.25) — optimism bias +0.34 quantified", b:true, color:RED},
    {t:"v1→v2 method change: top-10 overlap 2/10 (Spearman 0.672) — pair ranking not stable across versions", b:true},
    {t:"Root cause: no co-doping labels; dopant–dopant chemistry (vacancy compensation, phase separation, interphases) absent from features", b:true},
    {t:"Small-sample defense (Sendek procedure, 40 ≈ 47): LOOCV · label-shuffle / X-randomization · applicability domain · dopant-level CV — they classify cross-material; we regress within-host", sub:true},
    {t:"Showing only R² = 0.9998 would be a lie — we show both numbers", b:true, color:NAVY, gap:2},
  ],0.55,3.1,8.9,3.3,10.5);
  s.addNotes("이 모델의 두 단은 성적이 완전히 다릅니다. 1단 R2 0.9998 - 성공이 아닙니다. 타깃이 저희가 만든 합성 점수라 모델은 저희 공식을 해부한 것뿐. 이것만 보여드리면 거짓말. 진짜 숫자는 3단 - 쌍 천여 개 상호작용 항 R2 0.089. 거의 못 배웁니다. 누수 감사: 폴드 밖 재표준화로 3.4% - 무시 수준, 낮은 성적은 누수 탓이 아닙니다. 방법 한 판 바꾸니 top10 중 2개만 겹칩니다. 원인은 명확 - co-doping 라벨이 없고 도펀트끼리의 화학이 특징에 없습니다. 소표본 방어는 Sendek 계승 - 절차만.\n[Q] 0.089면 버려야 -> 예측기로는 그렇습니다. 가설 생성기로 격하해 쓰고, 상위 가설의 라벨 계산이 다음 단계. 숨기는 것보다 격하가 낫습니다.\n[Q] 왜 ridge/1-SE -> 47 표본 과적합 방지 최소 복잡도 + CV 최저점보다 한 단계 보수적인 관례.\n[용어] X-randomization: 라벨을 섞어 재학습 - 우연 적합 검사.");
  footer(s);
}
{ // S18 label plan
  const s=newSlide();
  kickerTitle(s,"Combine","Making the labels the model is missing");
  // dose grid
  const gx=0.95, gy=2.35, cell=0.52;
  s.addText("dose grid per pair:  3 × 3 labels (actual x to be resolved first — see the label caveat)",{x:0.55,y:1.55,w:4.6,h:0.3,fontSize:10.5,bold:true,color:INK,fontFace:"Arial",margin:0});
  for(let i=0;i<3;i++)for(let j=0;j<3;j++){
    s.addShape(p.ShapeType.rect,{x:gx+j*cell,y:gy+i*cell,w:cell,h:cell,fill:{color:LIGHT},line:{color:NAVY,width:1}});
  }
  ["0.02","0.05","0.10"].forEach((v,j)=>s.addText(v,{x:gx+j*cell,y:gy-0.26,w:cell,h:0.22,fontSize:8.5,color:MUT,align:"center",fontFace:"Arial",margin:0}));
  ["0.02","0.05","0.10"].forEach((v,i)=>s.addText(v,{x:gx-0.52,y:gy+i*cell+0.14,w:0.48,h:0.24,fontSize:8.5,color:MUT,align:"right",fontFace:"Arial",margin:0}));
  s.addText("= 9 compositions / pair — the ratio axis the current model does not have",
    {x:0.55,y:gy+3*cell+0.15,w:4.4,h:0.6,fontSize:10.5,color:RED,bold:true,fontFace:"Arial",margin:0});
  bullets(s,[
    {t:"Co-substituted supercells for top pairs (start: Cr₂O₃+HfO₂): joint formation energy · site assignment · Li-count closure", b:true},
    {t:"Success = interaction R² moves off 0.089 with real labels", b:true},
    {t:"Failure = complementarity assumption falsified — either way we learn", b:true},
    {t:"ML roadmap (queued):", b:true, gap:2},
    {t:"M1 TabPFN bench vs ridge · M2 leave-one-dopant-out CV · M3 inverse-design loop → first labels · M4 active-learning disorder surrogate", sub:true},
  ],5.35,1.5,4.15,4.8,10.5);
  s.addNotes("라벨을 만드는 계획입니다. 상위 쌍부터 공동 치환 슈퍼셀 - 형성에너지, 자리 배정, Li 개수 닫힘. 그리고 비율 그리드. 지금 모델엔 비율 축이 아예 없습니다. 단일 도펀트 농도 3점을 쌍으로 확장하면 쌍당 9개 조성 - 비율 축의 최소 라벨. 성공하면 0.089가 움직이고 실패하면 상보성 가정이 기각 - 어느 쪽이든 배웁니다. ML 쪽은 TabPFN 벤치, dopant 단위 leave-one-out, 역설계 루프, 능동학습이 줄 서 있습니다.\n[스킵라인] '요지는 하나 - 라벨 없는 축은 계산으로 라벨을 만든다, 비율 축 포함.'\n[Q] TabPFN 왜 -> 소표본 표형 전용 사전학습 모델, 47 체급에 맞음. ridge 대비 이득은 벤치(M1)로 확인 후.\n[용어] leave-one-dopant-out: 행이 아니라 도펀트 단위로 빼는 CV - 같은 도펀트 다른 농도가 훈련에 남는 누수 차단.");
  footer(s);
}
// ═══ Part 6 ═════════════════════════════════════════════════════════════════
divider("Part 6","6","VERIFY — what the gates actually did","11 audited verdicts — 9 retracted, one of them twice · one systematic bias · one provenance audit",5,
 "6부, 발표의 심장입니다. 여기서 시간을 씁니다.");
{ // S19 retraction table
  const s=newSlide();
  kickerTitle(s,"Verify","Retracted verdicts, and the gates that caught them");
  const hdr=(t)=>({text:t,options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}});
  s.addTable([
    [hdr("#"),hdr("Retracted claim"),hdr("What was wrong"),hdr("Caught by")],
    ["1","σ ratio 1.33×","single seed","multi-seed rule"],
    ["2","comp1 Ea 0.253 eV","MSD not in diffusive regime","β-gate (0/6 pass)"],
    ["3","LPSOCl Ea 0.287 eV","600 K β = 0.61 (caged)","β-gate → on hold"],
    ["4","gaps read from DOS threshold","~0.3 eV under","fixed-occ eigenvalue rule"],
    ["5","air_hsab grades","wrong driver (softness ≠ oxophilicity)","[Zhu20] SI check — 9/35 off"],
    ["6","SDCP E_ads −0.26 eV","frozen slab blocked relaxation","constraint variation → −1.27 (5×)"],
    [{text:"7",options:{color:RED,bold:true}},{text:"the “Li-extraction” reading of −1.27",options:{color:RED}},"MLIP has no charge states",{text:"DFT+U → +0.34 eV",options:{bold:true,color:RED}}],
    ["8","SDCP Δ “1.77 eV stronger”","poses not matched (rotation/site/contact)","matched-pose rule → 32 meV, confounded"],
    ["9","Nd gaps (3 phases)","quantity undefined (metallic SCF)","fixed-occ validity condition"],
    ["10","Nd₂S₃ gap 1.79 eV","metastable theoretical polymorph (mp-32586) picked","material-id pinning → 0.760 (obs. Pnma)"],
    ["11","4 canonical gaps","values fine — run files missing","provenance audit (Part 6 close)"],
  ],{x:0.55,y:1.45,w:8.9,fontFace:"Arial",fontSize:8.8,color:INK,border:{type:"solid",color:RULE,pt:0.75},
     colW:[0.4,2.6,3.0,2.9],rowH:0.335,valign:"middle",margin:0.03});
  bullets(s,[{t:"Ledger: 9 retracted · 1 on hold (#3) · 1 provenance-flagged (#11) — and 5 of 11 landed within the last four days", b:true, color:NAVY}],0.55,6.0,8.9,0.4,11);
  s.addNotes("이 표가 오늘의 중심입니다. 2번 - MSD 기울기로 Ea를 냈는데 그 구간이 확산 영역이 아니었습니다. 케이지 진동을 확산으로 착각. beta 게이트가 6중 6을 떨어뜨렸습니다. 10번 - Nd2S3 갭 1.79, 알고 보니 hull 위 20 meV의 '예측만' 다형체(mp-32586) 값이었습니다. id를 박으니 관측상은 0.76. 그림에 이미 들어가 있던 숫자입니다. 6-7-8번이 한 덩어리 - 다음 장. 장부로 읽으면 아홉 건 철회, 한 건 보류, 한 건 재현성 플래그이고, 다섯 건이 지난 나흘 사이입니다. 게이트는 지금도 돌고 있습니다.\n[Q] 각 철회의 원자료 -> 전부 repo에 있습니다 - open_items 항목 번호와 커밋으로 추적되고, 7-8번(SDCP DFT+U)은 runs/sdcp_phaseB_vasp_v1_2026_08_08/ + db/properties/sdcp_phaseB_dftu_v1.json 에 2026-08-10 등재했습니다.");
  footer(s);
}
{ // S20 retraction of retraction
  const s=newSlide();
  kickerTitle(s,"Verify","We retracted a retraction","the pre-registered rule that forced step ③ is quoted below");
  const steps=[
    ["① UMA, frozen slab (ff = 1.0)","E_ads = −0.26 eV","“weak physisorption”",LIGHT,NAVY],
    ["② unfreeze (0.85 / 0.6)","−1.27 / −1.465 eV — surface Li pulled out","“not adsorption — Li extraction”  (our previous deck)",SOFT,MUT],
    ["③ DFT+U single points","dE_extract = +0.336 eV (sign holds at σ→0)","extraction is uphill — ② was an MLIP artifact","FFFFFF",RED],
  ];
  steps.forEach((st,i)=>{
    const bx=0.55+i*3.05;
    s.addShape(p.ShapeType.roundRect,{x:bx,y:1.6,w:2.8,h:1.85,rectRadius:0.08,fill:{color:st[3]},line:{color:st[4],width:1.5}});
    s.addText([{text:st[0]+"\n",options:{bold:true,fontSize:10.5,breakLine:true}},
               {text:st[1]+"\n",options:{fontSize:10, breakLine:true}},
               {text:st[2],options:{fontSize:9.5, italic:true}}],
      {x:bx+0.12,y:1.68,w:2.56,h:1.7,color:(st[4]===MUT?INK:st[4]),fontFace:"Arial",valign:"top",margin:0});
    if(i<2) s.addShape(p.ShapeType.line,{x:bx+2.82,y:2.5,w:0.21,h:0,line:{color:INK,width:2,endArrowType:"triangle"}});
  });
  placeholder(s,0.55,3.75,4.3,2.0,"VESTA render: db/structures/sdcp_poses_qe/complex_doped.vesta  (mark O···Li 3.077 Å)","Physisorbed endpoint — display geometry; energies: runs/sdcp_phaseB_vasp_v1");
  placeholder(s,5.15,3.75,4.3,2.0,"VESTA render: Li-transfer endpoint  (mark O···Li 1.935 Å)","Li-transfer endpoint (display) — the +0.34 eV side");
  bullets(s,[
    {t:"Lesson 1: one constraint flips a conclusion (①→②).  Lesson 2: the flipped conclusion can be wrong too (②→③)", b:true, color:RED},
    {t:"Pre-registered in code, before the fact: “UMA cannot judge charge separation — this path is decided by DFT only”", i:true},
  ],0.55,6.0,8.9,0.75,10.5);
  s.addNotes("시간 순서대로. 슬랩을 얼리고 재니 -0.26, 약한 물리흡착. 얼린 게 걸려 풀고 재니 -1.27, 다섯 배 - 구조를 여니 표면 리튬이 뽑혀 나와 있었습니다. '흡착이 아니라 추출'로 판정을 바꿨습니다 - 이게 저희 이전 발표의 결론이었습니다. DFT+U로 재검하니 추출 반응에너지 +0.34 eV, 양수. 추출은 오르막. 두 번째 판정이 MLIP 아티팩트였습니다. 철회를 철회했습니다. 교훈 둘 - 제약 하나가 결론을 뒤집는다, 그리고 뒤집힌 결론도 틀릴 수 있다. 이걸 잡은 건 'UMA는 전하 분리를 판정할 수 없다, DFT로만 닫는다'를 미리 코드에 박아 둔 규칙이었습니다.\n[Q] 최종 결합에너지는 -> 아직 인용 불가 - 자세 불일치/전자설정 문제로 v2 프로토콜 재계산 발주됨. 오늘 확정은 추출 불리(+0.34)의 부호뿐.\n[용어] charge separation: Li+가 떠나며 전자가 남는 사건 - 정수 전하 상태를 모르는 퍼텐셜은 이 비용을 오산.");
  footer(s);
}
{ // S21 zhu bias
  const s=newSlide();
  kickerTitle(s,"Verify","Systematic bias found by cross-checking [Zhu 2020]","Zhu et al., Angew. 2020 · our transcription: 99 SI rows");
  bullets(s,[
    {t:"Transcribed their SI in full (99 rows), matched oxidation states, compared to our qualitative air grades", b:true},
    {t:"99 rows → matched to our 47-dopant pool: 35 overlap (26 + 9) + 12 absent", b:true},
    {t:"All 9 disagreements point the SAME way (we under-rated) — that is bias, not noise", b:true, color:RED},
    {t:"Root cause: we graded by HSAB softness; the operative variable is oxophilicity", b:true},
    {t:"Fix queued: replace the qualitative axis with computed ΔG_hyd (their recipe + answer key in hand)", b:true, color:NAVY},
  ],0.55,1.5,5.3,3.6,11.5);
  s.addShape(p.ShapeType.roundRect,{x:6.0,y:1.6,w:3.45,h:3.3,rectRadius:0.08,fill:{color:SOFT},line:{color:RULE,width:1}});
  s.addText([
    {text:"agree      ",options:{fontSize:12,color:INK}},{text:"26\n",options:{fontSize:26,bold:true,color:NAVY,breakLine:true}},
    {text:"disagree  ",options:{fontSize:12,color:INK}},{text:"9",options:{fontSize:26,bold:true,color:RED}},{text:"  (all one-directional)\n",options:{fontSize:10,italic:true,color:RED,breakLine:true}},
    {text:"absent     ",options:{fontSize:12,color:INK}},{text:"12",options:{fontSize:26,bold:true,color:MUT}},
  ],{x:6.25,y:1.85,w:3.0,h:2.9,fontFace:"Arial",valign:"top",margin:0});
  caption(s,"Our grade vs [Zhu20] ΔE_hydrolysis, matched by oxidation state",6.0,4.95,3.45);
  s.addNotes("공기 축을 문헌과 정면 대조. SI를 99행 전부 옮기고 산화수까지 맞춰서. 일치 26, 어긋남 9, 문헌 없음 12. 숫자보다 중요한 건 - 어긋난 아홉이 전부 같은 방향, 전부 과소평가였습니다. 무작위면 양쪽으로 흩어집니다. 한쪽으로 몰리면 체계 편향. 원인은 축의 물리를 잘못 잡은 것 - softness가 아니라 oxophilicity. 처방은 정성 축을 계산 축으로 대체 - 레시피와 정답지 확보됨.\n[용어] HSAB: 굳고 무른 산염기 이론. oxophilicity: 양이온이 O와 결합하려는 경향 - 가수분해 구동의 실제 변수.");
  footer(s);
}
{ // S22 provenance
  const s=newSlide();
  kickerTitle(s,"Verify","Our own canonical values fail a provenance audit");
  placeholder(s,0.55,1.55,4.55,3.3,"terminal:  python3 tools/db/validate_canonical.py  (warning block visible)","Registry validator output — the warning ships with the numbers");
  bullets(s,[
    {t:"Rule: gaps = fixed-occupation nscf eigenvalues ONLY", b:true},
    {t:"The 4 canonical gaps (2.066 / 2.099 / 1.967 / 2.231 eV): values match the canon files — but the runs that produced them cannot be located", b:true, color:RED},
    {t:"Surviving inputs are DOS-mode — not valid evidence", sub:true},
    {t:"Not doubting the values — doubting our ability to reproduce them", b:true},
    {t:"Response: keep values, flag provenance_open, make the validator print the warning on EVERY run", b:true, color:NAVY},
    {t:"Lesson: notes in documents guard nothing — the checked path must be the used path", b:true, gap:2},
  ],5.4,1.5,4.1,4.9,10.5);
  s.addNotes("제일 불편한 장입니다. 규율은 '갭은 고정 점유수 고윳값만'인데, 정본 네 값을 만든 실행 파일을 못 찾았습니다. 남은 입력은 전부 DOS용. 값을 의심하는 게 아닙니다 - 재현 능력을 의심하는 겁니다. 값은 유지하되 플래그를 달고 검증기가 돌 때마다 경고를 찍게 했습니다. 처음엔 문서에만 적었는데 검사를 돌리면 초록불이 떴어요. 문서는 검사 경로가 아니니까. 검사하는 경로가 곧 쓰이는 경로여야 한다 - 이 감사의 교훈입니다.\n[Q] 재현 안 되면 -> 순서대로: 서버/백업 수색 -> 동일 조건 재계산 -> 그때까지 플래그 유지. 감사 항목으로 등록돼 절차가 돌고 있습니다.");
  footer(s);
}
// ═══ Conclusions ════════════════════════════════════════════════════════════
divider("Closing","↺","Closing the loop","Deliverables · queued simulations · the scale ladder",5,
 "결론부입니다. 내놓은 것을 먼저, 그 다음 한 문장.");
{ // S23
  const s=newSlide();
  kickerTitle(s,"Conclusions","What we deliver, then the one sentence");
  s.addTable([
    [{text:"Deliverable",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}},{text:"State",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}}],
    ["LPSCl mechanism: gain = disorder, not bands","confirmed in-house (consistent with literature) — drives axis design"],
    ["47-dopant relative screen (273 run slots) + 14-axis ranking","complete as a screen; deep-DFT coverage 2/47 (B₂O₃, Nd₂O₃)"],
    ["Co-doping hypothesis set (+0.36 V top pair) + honest model audit","hypotheses; supercell labels queued (dose-grid design fixed)"],
    ["SEI phases: 6 citable gaps + Li₂S NEB converged (0.27 eV, fwd = bwd)","gaps in db; NEB registration syncing (cell-size caveat)"],
    ["Provenance infrastructure (28/28 wired, drift-checked)","live"],
    ["11 documented retractions with gate attribution","this talk"],
  ],{x:0.55,y:1.5,w:8.9,fontFace:"Arial",fontSize:10.5,color:INK,border:{type:"solid",color:RULE,pt:0.75},
     colW:[6.1,2.8],rowH:0.38,valign:"middle",margin:0.04});
  s.addShape(p.ShapeType.roundRect,{x:0.55,y:4.6,w:8.9,h:1.15,rectRadius:0.08,fill:{color:NAVY}});
  s.addText("Screening is only as good as its gates — ours audited 11 of our own verdicts, retracted 9, one of them twice.",
    {x:0.85,y:4.6,w:8.3,h:1.15,fontSize:14.5,bold:true,color:"FFFFFF",fontFace:"Arial",align:"center",valign:"middle",margin:0});
  bullets(s,[
    {t:"The funnel view exists (47→1) but is not the answer — AND kills complementarity", sub:true},
    {t:"We do not do: K_IC, µm particle mechanics, space-charge quantification, absolute σ", sub:true},
  ],0.55,5.95,8.9,0.8,10.5);
  s.addNotes("내놓은 걸 먼저 표로 - 기전 하나, 스크리닝과 다목적 랭킹, 조합 가설과 정직한 감사, SEI 갭 여섯에 NEB 하나, 인프라, 그리고 철회 열한 건의 기록. 그 위에 오늘의 한 문장: 스크리닝의 값어치는 게이트에 있다. 저희 게이트는 저희 자신의 판정 열한 건을 잡았고, 그중 하나는 두 번 잡았다.\n[Q] 실험 검증은 -> 아직. DFT 재검 2계열(B2O3/Nd2O3), 실험은 다음 단계. 그래서 절대값 표를 만들지 않고 순위/가설로만.");
  footer(s);
}
{ // S24 future
  const s=newSlide();
  kickerTitle(s,"Future plan","Queued simulations: recipes in hand vs in design");
  bullets(s,[
    {t:"Recipes in hand (queued):", b:true, color:NAVY},
    {t:"ΔG_hyd direct for the air axis — [Zhu20] method + their SI as the answer key", sub:true},
    {t:"Co-doping labels: co-substituted supercells, dose grid {0.02,0.05,0.10}² (site · charge · formation E)", sub:true},
    {t:"SEI NEB finish: Li₃P, Li₃PO₄γ  (Li₂S converged — 0.27 eV, cell-size caveat)", sub:true},
    {t:"Nd frozen-4f pseudopotential route → 7 Nd phases become our own numbers", sub:true},
    {t:"β-gate rescue: comp1 2×2×2 cell (Li 24→192) · Arrhenius extension 700/900 K first (500 K after feasibility)", sub:true},
  ],0.55,1.5,4.7,4.6,10.5);
  bullets(s,[
    {t:"In design:", b:true, color:NAVY},
    {t:"ΔV_rxn × C_ij → Griffith K_IC chemo-mechanical bridge (all three pieces already in repo)", sub:true},
    {t:"SDCP Phase-B v2 protocol (ISMEAR 0 · dipole corr. · LASPH · 3 magnetic seeds) — outsourced package ready", sub:true},
    {t:"MLIP committee: UMA + MACE + SevenNet cross-check", sub:true},
  ],5.45,1.5,4.05,4.6,10.5);
  s.addNotes("계획은 레시피가 손에 있는 것부터 - 공기 축 직접 계산은 정답지까지 있고, co-doping 라벨은 방금 그 그리드, SEI NEB 두 개, Nd는 frozen-4f로 일곱 상이 저희 숫자가 됩니다. beta 게이트에 걸린 계는 셀을 여덟 배로 키워 구조적으로 풉니다. 설계 중: 화학-역학 다리, SDCP 재계산, 퍼텐셜 위원회.\n[스킵라인] 확정 큐 다섯 줄만 읽고 넘어감.\n[Q] 우선순위 -> 협업 마감 걸린 SEI NEB -> co-doping 라벨 -> dG_hyd. 근거는 요청 기한과 재사용 빈도.");
  footer(s);
}
{ // S25 ladder + closing
  const s=newSlide();
  kickerTitle(s,"Closing","One ladder, our two rungs, and the loop");
  const rungs=[["Å–nm","DFT · MLIP\n(this talk)",NAVY,"FFFFFF"],["µm","DEM: contacts,\ntortuosity, eff. σ",LIGHT,NAVY],["mm","electrode\n(continuum)",SOFT,MUT]];
  rungs.forEach((r,i)=>{
    const rx=0.7+i*3.1;
    s.addShape(p.ShapeType.roundRect,{x:rx,y:1.7,w:2.7,h:1.15,rectRadius:0.08,fill:{color:r[2]},line:{color:(r[3]==="FFFFFF"?NAVY:r[3]),width:1.25}});
    s.addText([{text:r[0]+"\n",options:{bold:true,fontSize:13,breakLine:true}},{text:r[1],options:{fontSize:10}}],
      {x:rx,y:1.7,w:2.7,h:1.15,align:"center",valign:"middle",color:(i===0?"FFFFFF":(i===1?NAVY:MUT)),fontFace:"Arial",margin:0});
    if(i<2) s.addShape(p.ShapeType.line,{x:rx+2.73,y:2.27,w:0.31,h:0,line:{color:MUT,width:2,endArrowType:"triangle"}});
  });
  s.addText("we hand over E · G · γ · ΔV — DEM takes it from there (a different talk)",
    {x:0.7,y:3.0,w:8.6,h:0.3,fontSize:10.5,italic:true,color:MUT,align:"center",fontFace:"Arial",margin:0});
  mapDiagram(s, 0.55, 4.35, 8.9, 5, true);
  s.addText("Today was one lap of this loop.  Thank you.",
    {x:0.55,y:6.35,w:8.9,h:0.4,fontSize:14,bold:true,color:NAVY,align:"center",fontFace:"Arial",margin:0});
  s.addNotes("저희는 이 사다리의 왼쪽 두 칸에 있습니다. 재료 상수를 저희가 대면 입자 스케일은 DEM이 받습니다 - 그건 다른 발표의 주제. 오늘 발표는 처음 보여드린 지도를 한 바퀴 돈 것입니다. 마지막 정거장의 화살표가 앞으로 돌아간다는 것 - 그게 저희 파이프라인이 자기를 감사하는 방식입니다. 감사합니다.");
  footer(s);
}
// ═══ Appendix ═══════════════════════════════════════════════════════════════
divider("Appendix","A","Defense material","terms · conditions · the 12 questions · references · ML backup",-1,
 "부록은 발표하지 않습니다. 질문 방어용.");
function termSlide(kicker, title, rows, notes){
  const s=newSlide();
  kickerTitle(s,kicker,title);
  const body=[[{text:"Term",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}},{text:"One-line definition (and our setting)",options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}}]];
  rows.forEach(r=>body.push([{text:r[0],options:{bold:true}},r[1]]));
  s.addTable(body,{x:0.55,y:1.5,w:8.9,fontFace:"Arial",fontSize:10,color:INK,border:{type:"solid",color:RULE,pt:0.75},colW:[2.3,6.6],rowH:0.42,valign:"middle",margin:0.04});
  if(notes) s.addNotes(notes);
  footer(s);
  return s;
}
termSlide("Appendix A1","DFT terms",[
 ["SCF","self-consistent field — iterate density↔potential to a fixed point"],
 ["pseudopotential","replace core electrons by an effective potential; valence-only problem"],
 ["k-mesh","Brillouin-zone sampling grid; denser = more accurate band integrals"],
 ["XC functional","the one approximated term E_xc[n]; ours: PBE (GGA)"],
 ["Hubbard U","on-site repulsion for localized d/f; ours: Ni 3d, U = 6.2 eV (empirical)"],
 ["smearing","fractional occupations to stabilize metallic SCF; NEVER for our gap readings (fixed-occ rule)"],
],"A1. 용어 방어용.");
termSlide("Appendix A2","Property terms",[
 ["BM3 EOS","3rd-order Birch–Murnaghan fit of E(V) → B₀"],
 ["C_ij / VRH","elastic tensor / Voigt–Reuss–Hill average → E, G"],
 ["ICOHP","bond-resolved band-energy integral; SIGN: negative = bonding"],
 ["ELF","electron localization function, 0–1"],
 ["Bader charge","charge partitioned by zero-flux surfaces of n(r)"],
 ["ESW","electrochemical stability window from grand-potential hull"],
 ["E_hull","height above convex hull = decomposition driving force"],
],"A2.");
{ // A2b protocol matrix (Codex 대조에서 채택)
  const s=newSlide();
  kickerTitle(s,"Appendix A2b","Protocol matrix: the method tag sets the strongest allowed claim");
  const hdr=(t)=>({text:t,options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}});
  s.addTable([
    [hdr("Tier / method"),hdr("Primary output"),hdr("Allowed claim"),hdr("Do not claim")],
    ["UMA MLIP","relative E, forces, relaxation","same-protocol candidate ordering","absolute thermodynamics"],
    ["BVSE","static pathway geometry","pathway-retention risk","D or conductivity"],
    ["MLIP-MD","MSD, D(T), Ea","multi-seed verdict at 600/800/1000 K (β-gated)","single-seed ratios"],
    ["DFT (+U)","matched energies, electronic response","selected-candidate validation","47/47 DFT coverage"],
    ["Literature / experiment","external values","directional cross-check","mixing with internal absolutes"],
  ],{x:0.55,y:1.5,w:8.9,fontFace:"Arial",fontSize:9.5,color:INK,border:{type:"solid",color:RULE,pt:0.75},
     colW:[1.7,2.4,2.7,2.1],rowH:0.5,valign:"middle",margin:0.04});
  s.addText("One symbol = one method-qualified quantity. Never reuse a label across protocol lineages.",
    {x:0.55,y:4.8,w:8.9,h:0.3,fontSize:10.5,italic:true,color:NAVY,fontFace:"Arial",margin:0});
  s.addNotes("A2b. 방법 태그가 허용 주장 강도를 정합니다 - 질문이 어느 행이든 이 표로 돌아오면 됩니다. (Codex 판 A2에서 채택한 형식)");
  footer(s);
}
{ // A3 transport terms + figs
  const s=newSlide();
  kickerTitle(s,"Appendix A3","Transport terms, and the β-gate");
  bullets(s,[
    {t:"MSD: ⟨r²(t)⟩; diffusive regime ⇔ slope 1 on log–log", b:true},
    {t:"β-gate: β = dlog⟨r²⟩/dlogt ∈ [0.8, 1.2] on the ensemble-averaged MSD — else the “D” is cage rattling", b:true, color:RED},
    {t:"Arrhenius: ln D vs 1/T, 600/800/1000 K (3-point rule)", b:true},
    {t:"Nernst–Einstein (Haven = 1): σ from D — ratios only, never absolutes", b:true},
    {t:"Canonical MSD fit window: 2–50 ps (fixed)", sub:true},
  ],0.55,1.5,4.4,3.6,10.5);
  img(s, SCR+"beta_schematic.png", 5.15,1.6,4.3,3.1,"Schematic only — no measured data. The gate separates rattling from transport");
  s.addNotes("A3. beta 게이트 정의식은 여기 있습니다 - 앙상블 평균 MSD에 적용한다는 게 요점(시드별 beta 평균이 아님). 오른쪽 그림은 모식도라고 제목에 박아 뒀습니다 - 실측 곡선 아님.\n[감사 이력] 원래 이 자리에 있던 Arrhenius 그림 2장은 철회값 0.253 eV와 절대 sigma 주석을 달고 있어 내렸다(자체 리뷰 F3). 재출력 전까지 모식도로 대체.");
  footer(s);
}
{ // A4
  const s=newSlide();
  kickerTitle(s,"Appendix A4","Full calculation conditions (regenerate before the talk)");
  s.addShape(p.ShapeType.roundRect,{x:0.55,y:1.6,w:8.9,h:4.6,rectRadius:0.08,fill:{color:SOFT},line:{color:MUT,width:1,dashType:"dash"}});
  s.addText("PASTE TABLE\n\nper-composition: pseudopotentials · ecutwfc/ecutrho · k-mesh · cell · seeds · thermostat\nsource: canonical_registry.json + method docs (regenerate on talk day so it cannot go stale)",
    {x:0.85,y:2.8,w:8.3,h:2.0,fontSize:11,color:MUT,align:"center",fontFace:"Arial",margin:0});
  s.addNotes("A4. 발표 당일 registry에서 재생성 - 미리 만들면 stale해집니다.");
  footer(s);
}
{ // A5 Q12
  const s=newSlide();
  kickerTitle(s,"Appendix A5","The 12 questions: first sentences to memorize");
  const hdr=(t)=>({text:t,options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}});
  s.addTable([
    [hdr("Q"),hdr("First sentence of the answer")],
    ["Do you trust a PBE gap?","Not the absolute value — only same-method differences."],
    ["Why no absolute σ? ★","Cross-group reproducibility spans an order of magnitude; we retracted our own single-seed 1.33×."],
    ["Does MLIP replace DFT?","No — screening surrogate; champions return to DFT. Charge states failed us, measurably."],
    ["Experimentally validated?","Not yet — DFT re-checks on two systems; hence ranks and hypotheses, no absolute tables."],
    ["Is WO₃ the answer?","It is the most-surviving, not the best — and we reject that frame anyway."],
    ["Why U = 6.2?","Established lineage value, empirical; we fix it and quote same-U differences."],
    ["R² = 0.089 — useless?","As a predictor yes; we demoted it to hypothesis generator and queued the labels."],
    ["11 retractions — can we trust you? ★","Gate density, not carelessness — and the follow-up: rules born from errors now run as code (see #7, pre-registered)."],
    ["Canonical values without run files?","Values pass live drift checks; the missing-provenance flag ships WITH them."],
    ["Why show the funnel at all?","Drawing it the field's way is what reveals where we diverge."],
    ["Is co-doping even makeable?","Precedent lineage exists (InF₃→GaF₃); site/charge checks now, formation E queued."],
    ["Can you predict the ratio?","Not yet — the ratio axis needs the {0.02,0.05,0.10}² label grid first."],
  ],{x:0.55,y:1.45,w:8.9,fontFace:"Arial",fontSize:8.8,color:INK,border:{type:"solid",color:RULE,pt:0.75},
     colW:[2.9,6.0],rowH:0.36,valign:"middle",margin:0.03});
  s.addNotes("A5. 첫 문장만 외웁니다.");
  footer(s);
}
{ // A5b — five hostile questions (자체 리뷰 F24)
  const s=newSlide();
  kickerTitle(s,"Appendix A5b","Five harder questions from our own review");
  const hdr=(t)=>({text:t,options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}});
  s.addTable([
    [hdr("Q (who asks)"),hdr("First sentence of the answer")],
    ["Why must an electrolyte be an electronic insulator? (basics, on purpose)","If electrons leak, Li⁺ keeps reducing inside/at interfaces — SEI never self-limits and dendrite paths grow; ion-only transport is the defining condition."],
    ["What IS Ea physically — where is the hill in the structure? (basics)","Not cage rattling but the inter-cage jump saddle; 4d-site disorder lowers that saddle — exactly what the β-gate separates."],
    ["“UMA is a validated standard” — validated on what, by how much?","Validated for relative ranking and structure reproduction on the LPSCl family (records in repo); absolutes are never quoted — that IS the acknowledged limit."],
    ["Will HfO₂ really enter the lattice in a 550 °C H₂S synthesis? Cost of Hf?","We don't know — that is why formation-energy and phase-separation checks are in the label plan, and synthesis/cost is the experimental team's call. Today it is a hypothesis."],
    ["Name three elements NOT in your 47 — how does curation bias propagate?","Selection history is logged step-by-step (pool_provenance); we did not quantify bias propagation — which is exactly why pass counts are never used as discovery metrics."],
  ],{x:0.55,y:1.5,w:8.9,fontFace:"Arial",fontSize:9,color:INK,border:{type:"solid",color:RULE,pt:0.75},
     colW:[3.6,5.3],rowH:0.62,valign:"middle",margin:0.04});
  s.addText("Note to self: have three excluded elements ready before the talk; the last answer needs them.",
    {x:0.55,y:5.6,w:8.9,h:0.3,fontSize:9.5,italic:true,color:RED,fontFace:"Arial",margin:0});
  s.addNotes("A5b. 자체 레드팀이 만든 5문항 - Q12에 없던 것들. 마지막 답은 빠진 원소 3개를 실제로 외워야 성립한다(발표 전 pool_provenance에서 확인).");
  footer(s);
}
{ // A6 refs
  const s=newSlide();
  kickerTitle(s,"Appendix A6","References: only what we physically hold (litdb)");
  bullets(s,[
    {t:"Sendek et al., Energy Environ. Sci. 2017, 10, 306 — 12,831-candidate ML screening", sub:true},
    {t:"Xiao et al., Joule 2019 — cathode-coating funnel (104,082 → 184)", sub:true},
    {t:"Richards et al., Chem. Mater. 2016 — pseudo-binary interface stability", sub:true},
    {t:"Zhu et al., Angew. Chem. 2020 — air-stability design principles (ΔG_hyd)", sub:true},
    {t:"Kahle et al. 2020 — high-throughput AIMD screening", sub:true},
    {t:"He et al., Energy Environ. Mater. 2019 — DFT for battery materials (review)", sub:true},
    {t:"Famprikis et al., Nat. Mater. 2019 — fundamentals of inorganic SSEs", sub:true},
    {t:"InF₃/GaF₃ co-substitution lineage (AEM 2024 / EMA 2026) — argyrodite two-dopant precedent", sub:true},
    {t:"NOT held (do not cite until PDFs secured): Hohenberg–Kohn 1964 · Kohn–Sham 1965 · Pugh · Dronskowski · Dudarev", b:true, color:RED, gap:8},
  ],0.55,1.6,8.9,4.8,11);
  s.addNotes("A6. 원전 미보유 목록이 핵심 - 기억으로 서지를 쓰지 않습니다.");
  footer(s);
}
{ // A7 ML backup
  const s=newSlide();
  kickerTitle(s,"Appendix A7","ML backup: the numbers behind Part 5");
  const hdr=(t)=>({text:t,options:{bold:true,color:"FFFFFF",fill:{color:NAVY}}});
  s.addTable([
    [hdr("Item"),hdr("Value"),hdr("Note")],
    ["stage-1 λ (1-SE)","0.0794","LOOCV residual σ = 0.0018 score units"],
    ["stage-1 leakage audit","+3.4% σ_loo","fold-out re-standardization"],
    ["stage-3 λ","39.8","weighted LOOCV R² = 0.089"],
    ["stage-3 dopant-level CV","LODO −0.18 · L2DO −0.25","independent folds: R² < 0 (bias +0.34)"],
    ["stage-3 residual","2.33 z-units","interactions unlearned"],
    ["v1 top-40 Spearman","0.672","top-10 overlap 2/10"],
    ["v1-unlisted pairs","synergy ≈ 0 (weight 0.1)","1,041 of 1,081 — weak approximation"],
    ["assumptions","aggregate single-dopant features + quadratic terms","no dopant–dopant chemistry"],
    ["verdict","hypothesis generator — NOT a property predictor","labels queued (dose grid)"],
  ],{x:0.55,y:1.5,w:8.9,fontFace:"Arial",fontSize:9.5,color:INK,border:{type:"solid",color:RULE,pt:0.75},
     colW:[2.6,2.6,3.7],rowH:0.42,valign:"middle",margin:0.04});
  s.addNotes("A7. Part 5 뒤 숫자 백업.");
  footer(s);
}

p.writeFile({fileName: REPO+"kb/seminars/Research_Seminar_2026_08_final.pptx"})
 .then(()=>console.log("WROTE deck, slides:", pageNo));
