// mo.js — 분자오비탈(MO) 팝업 공용 렌더러 (elements·cascade 페이지 공용).
// 사용법: ① 템플릿에서 window.MO_DB = {{ mo_db|tojson }} 주입 ② templates/_mo_modal.html include
//        ③ 이 파일을 script src 로 로드 ④ openMO(key) 호출 (key = MO_DB 키, 예: 'B2O3').
// HTML 이스케이프 — 속성값 조립에도 쓰이므로 따옴표까지 막는다.
// (litdb 제목 3건이 큰따옴표를 포함: ngandjong2021 / schreiner2020 / shi2019)
// base.html 과 composition.html 의 중복 정의는 이 하나로 위임한다.
function _esc(s){return (s+'').replace(/[&<>"']/g,function(c){
  return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
// formula 표기(아래첨자·괄호·전하) → MO_DB 키 정규화
function moKey(f){var sub={'₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5','₆':'6','₇':'7','₈':'8','₉':'9'};
  return (f+'').replace(/[₀-₉]/g,function(c){return sub[c];})
    .replace(/\([^)]*\)/g,'').replace(/[¹²³⁴⁵⁶⁷⁸⁹⁰⁺⁻]/g,'').replace(/\s*\d*[+\-]\s*$/,'').replace(/[\s·–—\-]/g,'');}
function moHas(key){return !!(window.MO_DB&&window.MO_DB[key]);}
// 테마 토큰 읽기 — SVG는 CSS 상속을 안 받는 속성(stroke/fill)을 쓰므로 값으로 주입한다.
function _tok(name,fb){try{var v=getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return v||fb;}catch(e){return fb;}}
function moSVG(mo){var lv=mo.levels||[],n=lv.length;if(!n)return'';
  var W=280,H=44+n*40,top=26,bot=H-18,gap=n>1?(bot-top)/(n-1):0,midY=(top+bot)/2;
  var col={bonding:_tok('--mo-bonding','#2563eb'),nonbonding:_tok('--mo-nonbonding','#6b7280'),
           antibonding:_tok('--mo-antibonding','#dc2626')};
  var AX=_tok('--muted','#9ca3af'), TXT=_tok('--text2','#374151'), LN=_tok('--border','#d1d5db');
  var s='<svg viewBox="0 0 '+W+' '+H+'" class="mo-svg" xmlns="http://www.w3.org/2000/svg">';
  s+='<defs><marker id="ar" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="'+AX+'"/></marker></defs>';
  s+='<line x1="20" y1="'+bot+'" x2="20" y2="'+(top-8)+'" stroke="'+AX+'" stroke-width="1" marker-end="url(#ar)"/>';
  s+='<text x="7" y="'+midY+'" font-size="8" fill="'+AX+'" transform="rotate(-90 9 '+midY+')">Energy →</text>';
  var aoL=(mo.ao_left||[]).join(', ');
  if(aoL)s+='<text x="30" y="'+(midY+3)+'" font-size="8.5" fill="'+TXT+'">'+_esc(aoL)+'</text>';
  lv.forEach(function(l,i){var y=bot-i*gap,c=col[l.type]||col.nonbonding;
    s+='<line x1="135" y1="'+midY+'" x2="175" y2="'+y+'" stroke="'+LN+'" stroke-width="0.7"/>';
    s+='<line x1="175" y1="'+y+'" x2="235" y2="'+y+'" stroke="'+c+'" stroke-width="3.5"/>';
    s+='<text x="175" y="'+(y-5)+'" font-size="9" fill="'+c+'" font-weight="700">'+_esc(l.label)+'</text>';});
  return s+'</svg>';}
function moText(mo){var tk={bonding:'결합',nonbonding:'비결합',antibonding:'반결합'};
  return (mo.levels||[]).map(function(l){var ty=(l.type||'').replace(/[^a-z]/g,'');return '<div class="mo-lv mo-'+ty+'"><b>'+_esc(l.label)+'</b> <span class="mo-tag">'+(tk[l.type]||_esc(l.type))+'</span>'+
    (l.character?'<div class="mo-ch">'+_esc(l.character)+'</div>':'')+
    (l.dos?'<div class="mo-dos">→ DOS: '+_esc(l.dos)+'</div>':'')+'</div>';}).join('');}
function openMO(key){var mo=(window.MO_DB||{})[key];if(!mo)return;
  document.getElementById('mo-title').innerHTML='⚛ '+_esc(mo.name||key);
  var b='<div class="mo-sum">'+_esc(mo.summary||'')+'</div>'+
    '<div class="mo-grid"><div class="mo-diag">'+moSVG(mo)+'</div><div class="mo-levels">'+moText(mo)+'</div></div>';
  if(mo.dos_link)b+='<div class="mo-doslink"><b>📊 DOS 연결</b> '+_esc(mo.dos_link)+'</div>';
  if(mo.source)b+='<div class="mo-src">'+_esc(mo.source)+'</div>';
  document.getElementById('mo-body').innerHTML=b;
  var _m=document.getElementById('mo-modal');
  _m._opener=document.activeElement;            // Esc/닫기 후 포커스 복귀용
  _m.classList.add('open');
  var _b=_m.querySelector('.modal-head button'); if(_b)_b.focus();}
