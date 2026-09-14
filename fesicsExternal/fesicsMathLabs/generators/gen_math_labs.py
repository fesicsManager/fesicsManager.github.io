# -*- coding: utf-8 -*-
"""초등 3-4학년군 수와 연산 실험 2~6 일괄 생성"""
import os, re

OUT = "/mnt/user-data/outputs"
os.makedirs(OUT, exist_ok=True)

TPL = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>@@TITLE@@</title>
<style>
:root{
  --bg:#f6f9fc; --ink:#1f2937; --sub:#52627a; --line:#d7e0ec;
  --card:#ffffff; --accent:#2563eb; --ok:#0f9d58; --no:#dc2626;
}
html{font-size:20px}
@media (max-width:760px){html{font-size:19.5px}}
@media (max-width:420px){html{font-size:19px}}
*{box-sizing:border-box}
body{
  margin:0; padding:1.2rem 0 3rem;
  font-family:"Pretendard","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;
  color:var(--ink); line-height:1.6;
  background-color:var(--bg);
  background-image:radial-gradient(circle,#ccd7e6 1.3px,transparent 1.3px);
  background-size:22px 22px;
}
.wrap{width:97%;max-width:1840px;margin:0 auto}
h1{font-size:1.5rem;margin:0 0 .3rem}
.lead{font-size:1rem;color:var(--sub);margin:0 0 1.1rem}
.tabs{display:flex;gap:.5rem;margin-bottom:1rem;flex-wrap:wrap}
.tab-btn{font-family:inherit;font-size:1rem;font-weight:700;padding:.6rem 1.1rem;
  border:2px solid var(--line);border-radius:.7rem;background:#fff;color:var(--sub);cursor:pointer;
  transition:background .15s,color .15s,border-color .15s,transform .1s,filter .15s}
.tab-btn:hover{filter:brightness(.97);border-color:#b9c8dc}
.tab-btn:active{transform:translateY(2px) scale(.98)}
.tab-btn.on{background:var(--accent);border-color:var(--accent);color:#fff}
.grid{display:grid;grid-template-columns:minmax(400px,480px) 1fr;gap:1rem;align-items:start}
@media (max-width:640px){.grid{grid-template-columns:1fr}}
.card{background:var(--card);border:2px solid var(--line);border-radius:1rem;padding:1rem}
.card h2{font-size:1.1rem;margin:0 0 .7rem}
canvas{width:100%;height:auto;display:block;border-radius:.7rem;background:#fff}
.ctrl{margin:.9rem 0}
.ctrl .row{display:flex;justify-content:space-between;align-items:baseline;font-size:1rem;font-weight:700;margin-bottom:.1rem}
.ctrl .val{font-variant-numeric:tabular-nums}
.chip{display:inline-block;width:.95rem;height:.95rem;border-radius:.25rem;margin-right:.4rem;vertical-align:-.1rem}
input[type=range]{-webkit-appearance:none;appearance:none;width:100%;height:30px;background:transparent;
  cursor:pointer;touch-action:manipulation;margin:0}
input[type=range]::-webkit-slider-runnable-track{height:12px;border-radius:6px;background:#e3eaf4;border:1px solid #cfdbea}
input[type=range]::-moz-range-track{height:12px;border-radius:6px;background:#e3eaf4;border:1px solid #cfdbea}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:24px;height:24px;border-radius:50%;
  background:#fff;border:4px solid var(--accent);margin-top:-7px;transition:transform .12s,box-shadow .12s}
input[type=range]::-moz-range-thumb{width:24px;height:24px;border-radius:50%;background:#fff;
  border:4px solid var(--accent);transition:transform .12s,box-shadow .12s}
input[type=range]:hover::-webkit-slider-thumb{transform:scale(1.12)}
input[type=range]:hover::-moz-range-thumb{transform:scale(1.12)}
input[type=range]:active::-webkit-slider-thumb{transform:scale(.94);box-shadow:0 0 0 7px rgba(37,99,235,.18)}
input[type=range]:active::-moz-range-thumb{transform:scale(.94);box-shadow:0 0 0 7px rgba(37,99,235,.18)}
input[type=range]:disabled{opacity:.45;cursor:not-allowed}
.btns{display:flex;gap:.6rem;flex-wrap:wrap;margin-top:.9rem}
.btn{font-family:inherit;font-size:1rem;font-weight:700;padding:.65rem 1.15rem;border:none;
  border-radius:.7rem;background:var(--accent);color:#fff;cursor:pointer;transition:filter .15s,transform .1s}
.btn.alt{background:#0f9d58}
.btn:hover{filter:brightness(1.1)}
.btn:active{transform:translateY(2px) scale(.98)}
.btn:disabled{background:#aebdd0;cursor:not-allowed;filter:none;transform:none}
.readout{display:grid;grid-template-columns:1fr 1fr;gap:.6rem;margin-top:.9rem}
.readout div{background:#f1f6fd;border:1px solid var(--line);border-radius:.6rem;padding:.55rem .7rem;font-size:.95rem}
.readout b{display:block;font-size:1.25rem;font-variant-numeric:tabular-nums}
.hint{font-size:.95rem;color:var(--sub);margin-top:.7rem}
.tablewrap{max-height:26rem;overflow:auto;border:1px solid var(--line);border-radius:.7rem}
table{border-collapse:collapse;width:100%;font-size:.95rem;font-variant-numeric:tabular-nums}
th,td{padding:.5rem .45rem;text-align:center;border-bottom:1px solid var(--line);white-space:nowrap}
th{position:sticky;top:0;background:#eaf1fa;font-weight:700;z-index:2}
tbody tr:nth-child(even){background:#fafcff}
.empty{padding:1.6rem;text-align:center;color:var(--sub);font-size:1rem}
.ok{color:var(--ok);font-weight:700}
.no{color:var(--no);font-weight:700}
.concl{background:#eef7ff;border:2px solid #a9cff5;border-radius:.8rem;padding:.9rem 1rem;font-size:1.05rem;margin-top:1rem}
.hidden{display:none}
.statgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:.8rem;margin-top:.9rem}
.stat{background:#f4f8fe;border:1px solid var(--line);border-radius:.7rem;padding:.8rem}
.stat h3{margin:0 0 .3rem;font-size:1rem}
.stat p{margin:0;font-size:.95rem;color:var(--sub)}
.stat .big{font-size:1.3rem;font-weight:800;color:var(--ink);margin-bottom:.2rem}
</style>
</head>
<body>
<div class="wrap">
  <h1>@@H1@@</h1>
  <p class="lead">@@LEAD@@</p>

  <div class="tabs">
    <button class="tab-btn on" id="tabA">🔬 자유 탐구</button>
    <button class="tab-btn" id="tabB">✅ 데이터 확인</button>
  </div>

  <section id="paneA">
    <div class="grid">
      <div class="card">
        <h2 id="cvTitle">실험판</h2>
        <canvas id="cv"></canvas>
      </div>
      <div class="card">
        <h2>조절하기</h2>
        <div id="controls"></div>
        <div class="btns">
          <button class="btn" id="btnAct">실행</button>
          <button class="btn alt" id="btnRec" disabled>기록하기</button>
        </div>
        <div class="readout" id="readout"></div>
        <p class="hint" id="hint"></p>
      </div>
    </div>
    <div class="card" style="margin-top:1rem">
      <h2>기록표 <span style="font-weight:400;font-size:.95rem;color:var(--sub)">(<span id="cntA">0</span>개 기록됨)</span></h2>
      <div class="tablewrap"><table><thead id="thA"></thead><tbody id="tbA"></tbody></table></div>
    </div>
  </section>

  <section id="paneB" class="hidden">
    <div class="card">
      <h2>내가 기록한 데이터 분석</h2>
      <div id="lack" class="empty">데이터 부족 — 기록이 4개 이상 있어야 분석할 수 있다. (지금 <span id="cntB">0</span>개)</div>
      <div id="analysis" class="hidden">
        <div class="tablewrap"><table><thead id="thB"></thead><tbody id="tbB"></tbody></table></div>
        <div class="statgrid" id="statgrid"></div>
        <div class="concl" id="concl"></div>
      </div>
    </div>
  </section>
</div>

<script>
@@LABJS@@

/* ================= 공통 엔진 ================= */
(function(){
  "use strict";
  var cv = document.getElementById('cv');
  cv.width = LAB.cw; cv.height = LAB.ch;
  cv.style.maxWidth = LAB.cw + 'px';
  var ctx = cv.getContext('2d');
  document.getElementById('cvTitle').textContent = LAB.cvTitle;

  var S = {}, records = [], animating = false, ran = false;
  var DUR = 2400, MIN = 4;

  var h = '', i;
  for(i=0;i<LAB.sliders.length;i++){
    var s = LAB.sliders[i];
    h += '<div class="ctrl"><div class="row"><span><span class="chip" style="background:' + s.color + '"></span>'
       + s.label + '</span><span class="val" id="v_' + s.id + '"></span></div>'
       + '<input type="range" id="s_' + s.id + '" min="' + s.min + '" max="' + s.max
       + '" step="' + (s.step || 1) + '" value="' + s.value + '"></div>';
  }
  document.getElementById('controls').innerHTML = h;

  var btnAct = document.getElementById('btnAct');
  var btnRec = document.getElementById('btnRec');
  var hint = document.getElementById('hint');
  btnAct.textContent = LAB.action;

  function readSliders(){
    for(var i=0;i<LAB.sliders.length;i++){
      var s = LAB.sliders[i];
      var el = document.getElementById('s_' + s.id);
      S[s.id] = parseFloat(el.value);
      document.getElementById('v_' + s.id).textContent = s.fmt ? s.fmt(S[s.id]) : (S[s.id] + (s.unit || ''));
    }
  }
  function lock(on){
    for(var i=0;i<LAB.sliders.length;i++){ document.getElementById('s_' + LAB.sliders[i].id).disabled = on; }
    btnAct.disabled = on || ran;
    btnRec.disabled = on || !ran;
  }
  function readout(){
    var arr = LAB.readout(S, ran), s = '';
    for(var i=0;i<arr.length;i++){ s += '<div>' + arr[i].k + '<b>' + arr[i].v + '</b></div>'; }
    document.getElementById('readout').innerHTML = s;
  }
  function paint(t){
    ctx.clearRect(0,0,LAB.cw,LAB.ch);
    ctx.fillStyle = '#fff'; ctx.fillRect(0,0,LAB.cw,LAB.ch);
    ctx.strokeStyle = '#e5ecf5'; ctx.lineWidth = 2; ctx.strokeRect(1,1,LAB.cw-2,LAB.ch-2);
    LAB.draw(ctx, S, t, ran);
  }
  function onSlide(){
    if(animating) return;
    readSliders(); ran = false;
    btnAct.disabled = false; btnRec.disabled = true;
    hint.textContent = LAB.hint0;
    readout(); paint(null);
  }
  for(i=0;i<LAB.sliders.length;i++){
    document.getElementById('s_' + LAB.sliders[i].id).addEventListener('input', onSlide);
  }

  btnAct.addEventListener('click', function(){
    if(animating || ran) return;
    cv.scrollIntoView({behavior:'smooth', block:'center'});
    animating = true; lock(true);
    var t0 = performance.now();
    function frame(now){
      var p = (now - t0) / DUR;
      if(p > 1) p = 1;
      paint(p);
      if(p < 1){ requestAnimationFrame(frame); }
      else {
        animating = false; ran = true; lock(false);
        hint.textContent = LAB.doneMsg(S);
        readout(); paint(1);
      }
    }
    requestAnimationFrame(frame);
  });

  btnRec.addEventListener('click', function(){
    if(!ran) return;
    records.push(LAB.record(S));
    renderA(); renderB();
    hint.textContent = '기록했다! 다른 값으로도 해 보자. (' + records.length + '개 기록됨)';
  });

  function th(list){
    var s = '<tr>';
    for(var i=0;i<list.length;i++){ s += '<th>' + list[i] + '</th>'; }
    return s + '</tr>';
  }
  function renderA(){
    document.getElementById('cntA').textContent = records.length;
    document.getElementById('thA').innerHTML = th(LAB.headA);
    var tb = document.getElementById('tbA');
    if(records.length === 0){
      tb.innerHTML = '<tr><td colspan="' + LAB.headA.length + '" class="empty">아직 기록이 없다.</td></tr>';
      return;
    }
    var s = '';
    for(var i=0;i<records.length;i++){
      var cells = LAB.rowA(records[i], i);
      s += '<tr>';
      for(var j=0;j<cells.length;j++){ s += '<td>' + cells[j] + '</td>'; }
      s += '</tr>';
    }
    tb.innerHTML = s;
  }
  function renderB(){
    document.getElementById('cntB').textContent = records.length;
    var lack = document.getElementById('lack'), an = document.getElementById('analysis');
    if(records.length < MIN){ lack.classList.remove('hidden'); an.classList.add('hidden'); return; }
    lack.classList.add('hidden'); an.classList.remove('hidden');
    var res = LAB.analyze(records);
    document.getElementById('thB').innerHTML = th(res.head);
    var s = '';
    for(var i=0;i<res.rows.length;i++){
      s += '<tr>';
      for(var j=0;j<res.rows[i].length;j++){ s += '<td>' + res.rows[i][j] + '</td>'; }
      s += '</tr>';
    }
    document.getElementById('tbB').innerHTML = s;
    var g = '';
    for(var k=0;k<res.stats.length;k++){
      g += '<div class="stat"><h3>' + res.stats[k].t + '</h3><p class="big">' + res.stats[k].big
         + '</p><p>' + res.stats[k].p + '</p></div>';
    }
    document.getElementById('statgrid').innerHTML = g;
    document.getElementById('concl').innerHTML = res.concl;
  }

  var tabA = document.getElementById('tabA'), tabB = document.getElementById('tabB');
  var paneA = document.getElementById('paneA'), paneB = document.getElementById('paneB');
  tabA.addEventListener('click', function(){
    tabA.classList.add('on'); tabB.classList.remove('on');
    paneA.classList.remove('hidden'); paneB.classList.add('hidden');
  });
  tabB.addEventListener('click', function(){
    tabB.classList.add('on'); tabA.classList.remove('on');
    paneB.classList.remove('hidden'); paneA.classList.add('hidden');
    renderB();
  });

  readSliders(); readout(); paint(null);
  hint.textContent = LAB.hint0;
  renderA(); renderB();
})();
</script>
</body>
</html>
"""

# ============================================================
# LAB 2 : 받아올림 덧셈
# ============================================================
LAB2 = r"""
function lbl(ctx,t,x,y,c){ctx.fillStyle=c;ctx.font='bold 18px sans-serif';ctx.textAlign='left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
function pad(ctx,x,y,a,hl){
  ctx.globalAlpha=a;ctx.fillStyle=hl?'#fde68a':'#dbeafe';ctx.fillRect(x,y,36,36);
  ctx.strokeStyle=hl?'#d97706':'#2563eb';ctx.lineWidth=.8;
  for(var i=1;i<10;i++){var d=36*i/10;
    ctx.beginPath();ctx.moveTo(x+d,y);ctx.lineTo(x+d,y+36);ctx.stroke();
    ctx.beginPath();ctx.moveTo(x,y+d);ctx.lineTo(x+36,y+d);ctx.stroke();}
  ctx.lineWidth=2.2;ctx.strokeRect(x,y,36,36);ctx.globalAlpha=1;
}
function rod(ctx,x,y,a,hl){
  ctx.globalAlpha=a;ctx.fillStyle=hl?'#fde68a':'#dcfce7';ctx.fillRect(x,y,14,36);
  ctx.strokeStyle=hl?'#d97706':'#16a34a';ctx.lineWidth=.8;
  for(var i=1;i<10;i++){var d=36*i/10;ctx.beginPath();ctx.moveTo(x,y+d);ctx.lineTo(x+14,y+d);ctx.stroke();}
  ctx.lineWidth=2.2;ctx.strokeRect(x,y,14,36);ctx.globalAlpha=1;
}
function sq(ctx,x,y,a,hl){
  ctx.globalAlpha=a;ctx.fillStyle=hl?'#fde68a':'#fef3c7';ctx.fillRect(x,y,15,15);
  ctx.strokeStyle=hl?'#d97706':'#f59e0b';ctx.lineWidth=2.2;ctx.strokeRect(x,y,15,15);ctx.globalAlpha=1;
}
function items(n,a,hl){var r=[];for(var i=0;i<n;i++)r.push({a:a,hl:hl});return r;}
function rowLine(ctx,x,y,ts,os){
  var cx=x,i;
  for(i=0;i<ts.length;i++){rod(ctx,cx,y,ts[i].a,ts[i].hl);cx+=21;}
  cx+=8;
  for(i=0;i<os.length;i++){sq(ctx,cx,y+11,os[i].a,os[i].hl);cx+=20;}
}
function parts(n){return {t:Math.floor(n/10),o:n%10};}

var LAB = {
  cw:440, ch:450, cvTitle:'수 모형 덧셈판',
  action:'합치고 10개씩 묶기',
  hint0:'두 수를 정한 뒤 합치기 버튼을 눌러 보자.',
  sliders:[
    {id:'a',label:'첫 번째 수',min:10,max:89,value:27,color:'#2563eb',unit:''},
    {id:'b',label:'두 번째 수',min:10,max:89,value:15,color:'#0ea5e9',unit:''}
  ],
  readout:function(S,ran){
    var A=parts(S.a),B=parts(S.b);
    return [{k:'식',v:S.a+' + '+S.b},
            {k:'일의 자리 합',v:(A.o+B.o)}];
  },
  doneMsg:function(S){
    var A=parts(S.a),B=parts(S.b),oo=A.o+B.o;
    return oo>=10 ? '일의 자리가 '+oo+'개라서 10개를 묶어 십의 자리로 올렸다. 기록해 보자.'
                  : '일의 자리가 '+oo+'개뿐이라 묶을 것이 없었다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var A=parts(S.a),B=parts(S.b);
    var TT=A.t+B.t, TO=A.o+B.o;
    var c1=Math.floor(TO/10), o2=TO%10;
    var tMid=TT+c1, c2=Math.floor(tMid/10), t2=tMid%10, hh=c2;
    var val=S.a+S.b;

    lbl(ctx,'첫 번째 수  '+S.a,22,44,'#1d4ed8');
    lbl(ctx,'두 번째 수  '+S.b,22,116,'#0369a1');
    lbl(ctx,'합친 뒤',22,188,'#334155');

    var fa=1;
    if(t!==null&&t<0.5) fa=1-t/0.5;
    else if(t!==null) fa=0;
    if(fa>0){
      rowLine(ctx,22,52,items(A.t,fa,false),items(A.o,fa,false));
      rowLine(ctx,22,124,items(B.t,fa,false),items(B.o,fa,false));
    }

    var hs=[],ts=[],os=[];
    if(t===null){
      ctx.setLineDash([6,5]);ctx.strokeStyle='#c2cede';ctx.lineWidth=2;
      ctx.strokeRect(22,198,396,110);ctx.setLineDash([]);
      ctx.fillStyle='#94a3b8';ctx.font='bold 18px sans-serif';ctx.textAlign='center';
      ctx.fillText('아직 합치지 않았다',220,258);
    } else if(t<0.5){
      var p=t/0.5;
      ts=items(TT,p,false); os=items(TO,p,false);
    } else {
      var q=(t-0.5)/0.5;
      if(q<0.5){
        var r=q/0.5;
        ts=items(TT,1,false).concat(items(c1,r,true));
        os=items(o2,1,false).concat(items(c1*10,1-r,true));
      } else {
        var r2=(q-0.5)/0.5;
        hs=items(hh,r2,true);
        ts=items(t2,1,false).concat(items(c2*10,1-r2,true));
        os=items(o2,1,false);
      }
    }
    var i,cx;
    cx=22; for(i=0;i<hs.length;i++){pad(ctx,cx,198,hs[i].a,hs[i].hl);cx+=44;}
    cx=(hs.length>0?22+hs.length*44+6:22);
    for(i=0;i<ts.length;i++){rod(ctx,cx,198,ts[i].a,ts[i].hl);cx+=21;}
    cx=22; for(i=0;i<os.length;i++){sq(ctx,cx,246,os[i].a,os[i].hl);cx+=20;}

    ctx.fillStyle='#f1f6fd';ctx.fillRect(20,300,400,130);
    ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(20,300,400,130);
    ctx.textAlign='left';
    ctx.fillStyle='#1f2937';ctx.font='bold 21px sans-serif';
    ctx.fillText('십의 자리 합 : '+TT+'개',38,332);
    ctx.fillText('일의 자리 합 : '+TO+'개',38,362);
    ctx.fillStyle=(t===null)?'#94a3b8':'#1d4ed8';
    ctx.fillText('묶은 뒤 : 백 '+(t===null?'?':hh)+' · 십 '+(t===null?'?':t2)+' · 일 '+(t===null?'?':o2),38,392);
    ctx.fillStyle='#334155';ctx.font='bold 19px sans-serif';
    ctx.fillText(t===null?('만들 값 : ?'):('합 : '+val),38,418);
  },
  record:function(S){
    var A=parts(S.a),B=parts(S.b);
    var TT=A.t+B.t, TO=A.o+B.o;
    return {a:S.a,b:S.b,ts:TT,os:TO,
            cat:parseInt(String(TT)+String(TO),10),
            real:S.a+S.b};
  },
  headA:['번호','첫 수','둘째 수','십의 자리 합','일의 자리 합','자리끼리 이어쓴 수','묶어서 구한 값','같은가?'],
  rowA:function(r,i){
    var same=(r.cat===r.real);
    return [i+1,r.a,r.b,r.ts,r.os,r.cat,'<b>'+r.real+'</b>',
            '<span class="'+(same?'ok':'no')+'">'+(same?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,over=0,overSame=0,gapSum=0,gapN=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i], s=(r.cat===r.real);
      if(s) same++;
      if(r.os>=10){ over++; if(s) overSame++; }
      if(!s){ gapSum+=Math.abs(r.cat-r.real); gapN++; }
      rows.push([r.a+' + '+r.b, r.os, r.cat, '<b>'+r.real+'</b>',
                 '<span class="'+(s?'ok':'no')+'">'+(s?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'이어쓰기가 맞은 횟수',big:same+' / '+rec.length,
       p:'자리끼리 더한 값을 그냥 이어 쓰면 맞을 때도 있고 틀릴 때도 있었다.'},
      {t:'일의 자리 합이 10 이상이었던 기록',big:over+'개',
       p:'그중 이어쓰기가 맞은 것은 '+overSame+'개.'},
      {t:'틀렸을 때 벌어진 차이',big:gapN?('평균 '+(gapSum/gapN).toFixed(1)):'없음',
       p:gapN?'이어쓴 수와 실제 합의 차이 평균.':'아직 틀린 기록이 없다. 일의 자리 합이 10을 넘게 만들어 보자.'}
    ];
    var concl;
    if(over===0){
      concl='<b>더 해 보자</b> — 아직 일의 자리 합이 10을 넘은 기록이 없다. 7+5처럼 일의 자리가 10을 넘도록 만들어서 다시 확인해 보자.';
    } else if(overSame===0){
      concl='<b>정리</b> — 일의 자리 합이 10보다 작을 때는 자리끼리 더해 이어 써도 맞았지만, '
           +'<b>10 이상이 된 '+over+'번 모두 틀렸다.</b> 낱개 10개는 반드시 십막대 1개로 묶어 윗자리로 올려야 하기 때문이다. 이것이 받아올림이다.';
    } else {
      concl='<b>확인 필요</b> — 일의 자리 합이 10 이상인데도 이어쓰기가 맞은 기록이 있다. 값을 다시 확인해 보자.';
    }
    return {head:['식','일의 자리 합','이어쓴 수','실제 합','같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# LAB 3 : 곱셈 배열 모형
# ============================================================
LAB3 = r"""
function lbl(ctx,t,x,y,c,sz){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign='left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}

var LAB = {
  cw:440, ch:476, cvTitle:'점 배열판',
  action:'세어 보고 90° 돌리기',
  hint0:'가로줄 수와 세로줄 수를 정하고 세어 보자.',
  sliders:[
    {id:'a',label:'가로 (한 줄에 놓는 점)',min:1,max:12,value:4,color:'#2563eb',unit:'개'},
    {id:'b',label:'세로 (줄 수)',min:1,max:12,value:3,color:'#16a34a',unit:'줄'}
  ],
  readout:function(S,ran){
    return [{k:'곱셈식',v:S.a+' × '+S.b},{k:'점의 수',v:(ran? (S.a*S.b)+'개' : '세어 보자')}];
  },
  doneMsg:function(S){
    return '가로줄로 세도 '+(S.a*S.b)+'개, 90° 돌려 세도 '+(S.b*S.a)+'개였다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var a=S.a,b=S.b,total=a*b;
    var cell=Math.min(26, Math.floor(300/Math.max(a,b)));
    var gw=a*cell, gh=b*cell;
    var cxm=220, cym=208;
    var counted=0, rot=0, phase=0;
    if(t===null){ counted=0; }
    else if(t<0.45){ counted=Math.ceil((t/0.45)*total); phase=1; }
    else if(t<0.60){ counted=total; rot=Math.PI/2*((t-0.45)/0.15); phase=2; }
    else { counted=Math.ceil(((t-0.60)/0.40)*total); rot=Math.PI/2; phase=3; }
    if(counted>total) counted=total;

    ctx.save();
    ctx.translate(cxm,cym);
    ctx.rotate(rot);
    ctx.translate(-gw/2,-gh/2);
    for(var r=0;r<b;r++){
      for(var c=0;c<a;c++){
        var idx, on;
        if(phase===3){ idx = c*b + r; } else { idx = r*a + c; }
        on = (phase>0) && (idx < counted);
        var x=c*cell+cell/2, y=r*cell+cell/2, rad=Math.max(5,cell*0.32);
        ctx.beginPath();ctx.arc(x,y,rad,0,Math.PI*2);
        ctx.fillStyle = on ? '#f59e0b' : '#cbd5e1';
        ctx.fill();
        ctx.lineWidth=2;ctx.strokeStyle= on ? '#b45309' : '#94a3b8';ctx.stroke();
      }
    }
    ctx.restore();

    ctx.fillStyle='#f1f6fd';ctx.fillRect(20,374,400,84);
    ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(20,374,400,84);
    var line1, line2;
    if(phase===0){ line1='아직 세지 않았다'; line2='가로 '+a+' · 세로 '+b; }
    else if(phase===1){ line1='가로줄로 세는 중 : '+counted+'개'; line2=a+'개씩 '+b+'줄'; }
    else if(phase===2){ line1='90° 돌리는 중...'; line2='점의 개수는 그대로!'; }
    else { line1='세로줄로 세는 중 : '+counted+'개'; line2=b+'개씩 '+a+'줄'; }
    lbl(ctx,line1,38,410,'#1f2937',22);
    lbl(ctx,line2,38,440,'#52627a',19);
  },
  record:function(S){
    var a=S.a,b=S.b,c1=0,c2=0,add=0,i,j;
    for(i=0;i<b;i++){ for(j=0;j<a;j++){ c1++; } }
    for(i=0;i<a;i++){ for(j=0;j<b;j++){ c2++; } }
    for(i=0;i<b;i++){ add+=a; }
    return {a:a,b:b,c1:c1,c2:c2,add:add};
  },
  headA:['번호','가로','세로','가로줄로 센 수','돌려서 센 수','가로 수를 세로 수만큼 더한 값','모두 같은가?'],
  rowA:function(r,i){
    var same=(r.c1===r.c2 && r.c2===r.add);
    return [i+1,r.a,r.b,r.c1,r.c2,r.a+'×'+r.b+' → '+r.add,
            '<span class="'+(same?'ok':'no')+'">'+(same?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,addSame=0,maxN=0,maxTxt='',pairs={};
    for(var i=0;i<rec.length;i++){
      var r=rec[i], s=(r.c1===r.c2), s2=(r.add===r.c1);
      if(s) same++;
      if(s2) addSame++;
      if(r.c1>maxN){ maxN=r.c1; maxTxt=r.a+'×'+r.b; }
      var key=Math.min(r.a,r.b)+'x'+Math.max(r.a,r.b);
      pairs[key]=true;
      rows.push([r.a+' × '+r.b, r.c1, r.b+' × '+r.a, r.c2,
                 '<span class="'+(s?'ok':'no')+'">'+(s?'○':'×')+'</span>',
                 r.add,
                 '<span class="'+(s2?'ok':'no')+'">'+(s2?'○':'×')+'</span>']);
    }
    var kinds=0; for(var k in pairs){ kinds++; }
    var stats=[
      {t:'돌려도 개수가 같았던 횟수',big:same+' / '+rec.length,
       p:'가로줄로 센 수와 90° 돌려 센 수를 비교한 결과.'},
      {t:'더하기로 구한 값과 같았던 횟수',big:addSame+' / '+rec.length,
       p:'곱셈은 같은 수를 여러 번 더한 것과 같은지 확인한 결과.'},
      {t:'서로 다른 곱셈식',big:kinds+'가지',
       p:'가장 큰 배열은 '+(maxTxt||'-')+' = '+maxN+'개였다.'}
    ];
    var concl;
    if(same===rec.length && addSame===rec.length){
      concl='<b>정리</b> — 점의 배열을 돌려도 개수는 한 번도 달라지지 않았다. 즉 <b>a × b = b × a</b>. '
           +'또 가로 수를 세로 수만큼 더한 값과도 항상 같았으니, 곱셈은 <b>같은 수를 여러 번 더한 것</b>을 짧게 쓴 식이다. '
           +'4×3과 3×4는 “세는 방향”만 다르고 점의 수는 하나다.';
    } else {
      concl='<b>확인 필요</b> — 개수가 달라진 기록이 있다. 세는 도중에 슬라이더를 움직이지 않았는지 확인해 보자.';
    }
    return {head:['곱셈식','센 수','돌린 식','센 수','같은가?','더하기로 구한 값','같은가?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# LAB 4 : 나눗셈과 나머지
# ============================================================
LAB4 = r"""
function lbl(ctx,t,x,y,c,sz){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign='left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
function marble(ctx,x,y,col){
  ctx.beginPath();ctx.arc(x,y,7,0,Math.PI*2);
  ctx.fillStyle=col;ctx.fill();
  ctx.lineWidth=2;ctx.strokeStyle='#b45309';ctx.stroke();
}

var LAB = {
  cw:440, ch:520, cvTitle:'구슬 나누기판',
  action:'접시에 똑같이 나누기',
  hint0:'구슬 수와 접시 수를 정하고 나누어 보자.',
  sliders:[
    {id:'n',label:'구슬',min:1,max:40,value:23,color:'#f59e0b',unit:'개'},
    {id:'d',label:'접시',min:2,max:9,value:4,color:'#2563eb',unit:'개'}
  ],
  readout:function(S,ran){
    var q=Math.floor(S.n/S.d), r=S.n%S.d;
    return [{k:'나눗셈식',v:S.n+' ÷ '+S.d},
            {k:'결과',v:ran?(q+' … '+r):'나누어 보자'}];
  },
  doneMsg:function(S){
    var q=Math.floor(S.n/S.d), r=S.n%S.d;
    return '한 접시에 '+q+'개씩, 남은 구슬은 '+r+'개. 남은 것으로는 더 이상 모든 접시에 하나씩 줄 수 없다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var n=S.n, d=S.d, q=Math.floor(n/d), r=n%d, dist=q*d;
    var placed = (t===null)?0:Math.floor(t*dist+0.0001);
    if(t!==null && t>=1) placed=dist;
    var left = n - placed;

    lbl(ctx,'아직 안 나눈 구슬 : '+left+'개',20,34,'#b45309');
    var i,x,y;
    for(i=0;i<left;i++){
      x=28+(i%14)*24; y=56+Math.floor(i/14)*22;
      marble(ctx,x,y,'#fbbf24');
    }

    var top=140;
    lbl(ctx,'접시 '+d+'개',20,top-8,'#1d4ed8');
    var pw=Math.floor(400/d), inner=Math.min(pw-8,46);
    for(i=0;i<d;i++){
      var px=20+i*pw+(pw-inner)/2;
      var ph=280;
      ctx.fillStyle='#eef4fc';ctx.fillRect(px,top,inner,ph);
      ctx.strokeStyle='#94b4dd';ctx.lineWidth=2.5;ctx.strokeRect(px,top,inner,ph);
      var cnt=Math.floor(placed/d)+((placed%d)>i?1:0);
      var perRow=Math.max(1,Math.floor(inner/18));
      for(var j=0;j<cnt;j++){
        var cx=px+9+(j%perRow)*18;
        var cy=top+ph-14-Math.floor(j/perRow)*18;
        marble(ctx,cx,cy,'#f59e0b');
      }
      ctx.fillStyle='#334155';ctx.font='bold 17px sans-serif';ctx.textAlign='center';
      ctx.fillText(cnt+'개',px+inner/2,top+ph+22);
    }
    ctx.textAlign='left';

    ctx.fillStyle='#f1f6fd';ctx.fillRect(20,462,400,46);
    ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(20,462,400,46);
    var txt;
    if(t===null) txt=n+' ÷ '+d+' = ?';
    else if(placed<dist) txt='한 개씩 차례로 나누는 중...';
    else txt=n+' ÷ '+d+' = '+q+' … '+r;
    lbl(ctx,txt,38,492,'#1f2937',21);
  },
  record:function(S){
    var q=Math.floor(S.n/S.d), r=S.n%S.d;
    return {n:S.n,d:S.d,q:q,r:r,chk:q*S.d+r};
  },
  headA:['번호','구슬','접시','한 접시에','남은 구슬','접시수 × 한접시 + 남은 수'],
  rowA:function(r,i){
    return [i+1,r.n,r.d,r.q,'<b>'+r.r+'</b>',r.q+'×'+r.d+'+'+r.r+' = '+r.chk];
  },
  analyze:function(rec){
    var rows=[],less=0,chk=0,maxR=0,maxD=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i], l=(r.r<r.d), c=(r.chk===r.n);
      if(l) less++;
      if(c) chk++;
      if(r.r>maxR) maxR=r.r;
      if(r.d>maxD) maxD=r.d;
      rows.push([r.n+' ÷ '+r.d, r.q, '<b>'+r.r+'</b>', r.d,
                 '<span class="'+(l?'ok':'no')+'">'+(l?'○':'×')+'</span>',
                 r.chk,
                 '<span class="'+(c?'ok':'no')+'">'+(c?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'남은 수 < 접시 수',big:less+' / '+rec.length,
       p:'남은 구슬이 접시 수보다 작았던 횟수.'},
      {t:'원래 구슬 수로 되돌아오나',big:chk+' / '+rec.length,
       p:'(한 접시 개수 × 접시 수) + 남은 수가 처음 구슬 수와 같았던 횟수.'},
      {t:'내가 본 가장 큰 남은 수',big:maxR+'개',
       p:'기록에서 가장 접시가 많았던 경우는 '+maxD+'개. 남은 수는 접시 수보다 항상 작다.'}
    ];
    var concl;
    if(less===rec.length && chk===rec.length){
      concl='<b>정리</b> — 남은 구슬이 접시 수와 같거나 더 많았던 적은 한 번도 없었다. '
           +'남은 것이 접시 수만큼 있으면 모든 접시에 하나씩 더 줄 수 있으니까, 그건 아직 다 나눈 것이 아니다. '
           +'그래서 <b>나머지는 항상 나누는 수보다 작다.</b> 또 (몫 × 나누는 수) + 나머지는 언제나 처음 수로 돌아왔다.';
    } else {
      concl='<b>확인 필요</b> — 나머지가 나누는 수보다 크거나 같은 기록이 있다. 끝까지 나누었는지 확인해 보자.';
    }
    return {head:['나눗셈식','몫','나머지','나누는 수','나머지가 더 작은가?','되돌린 값','처음 수와 같은가?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# LAB 5 : 단위분수 크기 비교
# ============================================================
LAB5 = r"""
function lbl(ctx,t,x,y,c,sz){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign='left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
var BARW=360, BARX=40, TOTAL=12; /* 기준 띠 = 12cm */

function bar(ctx,x,y,n,cuts,col,edge){
  ctx.fillStyle='#f8fafc';ctx.fillRect(x,y,BARW,44);
  ctx.strokeStyle=edge;ctx.lineWidth=2.5;ctx.strokeRect(x,y,BARW,44);
  var w=BARW/n,i;
  ctx.fillStyle=col;ctx.fillRect(x,y,w,44);
  ctx.strokeStyle=edge;ctx.lineWidth=2.5;ctx.strokeRect(x,y,w,44);
  ctx.lineWidth=1.6;ctx.strokeStyle='#9aa8bb';
  var shown=Math.ceil(cuts*(n-1));
  for(i=1;i<=shown && i<n;i++){
    ctx.beginPath();ctx.moveTo(x+w*i,y);ctx.lineTo(x+w*i,y+44);ctx.stroke();
  }
}

var LAB = {
  cw:440, ch:430, cvTitle:'분수 띠 비교판',
  action:'등분하고 한 칸 비교하기',
  hint0:'두 띠를 몇 등분할지 정하고 잘라 보자. 두 띠의 원래 길이는 똑같이 12cm다.',
  sliders:[
    {id:'na',label:'위 띠 등분 수 (분모)',min:1,max:12,value:3,color:'#2563eb',unit:'등분'},
    {id:'nb',label:'아래 띠 등분 수 (분모)',min:1,max:12,value:6,color:'#16a34a',unit:'등분'}
  ],
  readout:function(S,ran){
    return [{k:'위 띠 한 칸',v:ran?((TOTAL/S.na).toFixed(2)+'cm'):('1/'+S.na)},
            {k:'아래 띠 한 칸',v:ran?((TOTAL/S.nb).toFixed(2)+'cm'):('1/'+S.nb)}];
  },
  doneMsg:function(S){
    var la=TOTAL/S.na, lb=TOTAL/S.nb;
    if(Math.abs(la-lb)<1e-9) return '두 띠의 한 칸 길이가 같았다. 분모가 같으니 당연하다. 기록해 보자.';
    var big=(la>lb)?('1/'+S.na):('1/'+S.nb);
    return '한 칸이 더 긴 쪽은 '+big+'이다. 분모가 작은 쪽이 더 길었다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var na=S.na, nb=S.nb;
    var la=TOTAL/na, lb=TOTAL/nb;
    var cuts=(t===null)?0:Math.min(1,t/0.5);
    var move=(t===null||t<0.5)?0:(t-0.5)/0.5;

    lbl(ctx,'위 띠 : 12cm를 '+na+'등분  →  1/'+na,BARX,36,'#1d4ed8');
    bar(ctx,BARX,46,na,cuts,'#bfdbfe','#2563eb');
    lbl(ctx,'아래 띠 : 12cm를 '+nb+'등분  →  1/'+nb,BARX,132,'#15803d');
    bar(ctx,BARX,142,nb,cuts,'#bbf7d0','#16a34a');

    lbl(ctx,'한 칸끼리 나란히 대어 보기',BARX,236,'#334155');
    ctx.setLineDash([5,5]);ctx.strokeStyle='#c8d3e2';ctx.lineWidth=1.6;
    ctx.beginPath();ctx.moveTo(BARX,250);ctx.lineTo(BARX,346);ctx.stroke();
    ctx.setLineDash([]);

    if(move>0){
      var wa=BARW/na*move, wb=BARW/nb*move;
      ctx.fillStyle='#bfdbfe';ctx.fillRect(BARX,254,wa,36);
      ctx.strokeStyle='#2563eb';ctx.lineWidth=2.5;ctx.strokeRect(BARX,254,wa,36);
      ctx.fillStyle='#bbf7d0';ctx.fillRect(BARX,300,wb,36);
      ctx.strokeStyle='#16a34a';ctx.lineWidth=2.5;ctx.strokeRect(BARX,300,wb,36);
      if(move>=1){
        ctx.font='bold 17px sans-serif';ctx.textAlign='left';
        ctx.fillStyle='#1d4ed8';ctx.fillText('1/'+na+' = '+la.toFixed(2)+'cm',BARX+wa+8,278);
        ctx.fillStyle='#15803d';ctx.fillText('1/'+nb+' = '+lb.toFixed(2)+'cm',BARX+wb+8,324);
      }
    }

    ctx.fillStyle='#f1f6fd';ctx.fillRect(20,358,400,56);
    ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(20,358,400,56);
    var txt;
    if(t===null) txt='아직 자르지 않았다';
    else if(move<1) txt='자르는 중...';
    else if(Math.abs(la-lb)<1e-9) txt='1/'+na+' = 1/'+nb;
    else txt=(la>lb)?('1/'+na+' > 1/'+nb):('1/'+na+' < 1/'+nb);
    lbl(ctx,txt,38,392,'#1f2937',22);
  },
  record:function(S){
    var la=TOTAL/S.na, lb=TOTAL/S.nb;
    var big = (Math.abs(la-lb)<1e-9)?'같음':((la>lb)?('1/'+S.na):('1/'+S.nb));
    var bigDen = (Math.abs(la-lb)<1e-9)?0:Math.max(S.na,S.nb);
    var shortSide = (Math.abs(la-lb)<1e-9)?0:((la<lb)?S.na:S.nb);
    return {na:S.na,nb:S.nb,la:la,lb:lb,big:big,bigDen:bigDen,shortDen:shortSide};
  },
  headA:['번호','위 띠','아래 띠','위 한 칸(cm)','아래 한 칸(cm)','한 칸이 더 긴 쪽'],
  rowA:function(r,i){
    return [i+1,'1/'+r.na,'1/'+r.nb,r.la.toFixed(2),r.lb.toFixed(2),'<b>'+r.big+'</b>'];
  },
  analyze:function(rec){
    var rows=[],diff=0,ruleOk=0,prodOk=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var isDiff=(r.na!==r.nb);
      var bigDen=Math.max(r.na,r.nb);
      var shorter=(r.la<r.lb)?r.na:r.nb;
      var rule=(!isDiff)||(bigDen===shorter);
      if(isDiff){ diff++; if(rule) ruleOk++; }
      var p1=(r.na*r.la), p2=(r.nb*r.lb);
      var pk=(Math.abs(p1-12)<1e-6 && Math.abs(p2-12)<1e-6);
      if(pk) prodOk++;
      rows.push(['1/'+r.na+' 와 1/'+r.nb,
                 isDiff?bigDen:'-',
                 isDiff?shorter:'-',
                 isDiff?('<span class="'+(rule?'ok':'no')+'">'+(rule?'○':'×')+'</span>'):'같음',
                 r.la.toFixed(2)+' / '+r.lb.toFixed(2),
                 '<span class="'+(pk?'ok':'no')+'">'+(pk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'분모가 큰 쪽이 한 칸도 짧았나',big:diff?(ruleOk+' / '+diff):'비교 없음',
       p:diff?'분모가 서로 다른 기록만 셈.':'분모가 다른 경우를 만들어 보자.'},
      {t:'(분모) × (한 칸 길이) = 12cm',big:prodOk+' / '+rec.length,
       p:'몇 등분을 하든 조각을 다 모으면 원래 띠 길이로 돌아온다.'},
      {t:'기록한 비교 수',big:rec.length+'번',
       p:'분모가 클수록 조각이 잘게 쪼개진다는 뜻이다.'}
    ];
    var concl;
    if(diff===0){
      concl='<b>더 해 보자</b> — 아직 분모가 서로 다른 기록이 없다. 1/3과 1/8처럼 다르게 잘라 비교해 보자.';
    } else if(ruleOk===diff){
      concl='<b>정리</b> — 분모가 큰 쪽이 한 칸이 짧았던 경우가 '+diff+'번 중 '+ruleOk+'번, 즉 <b>모두</b>였다. '
           +'같은 띠를 더 많이 나눌수록 한 조각은 작아지니까 <b>1/3 &gt; 1/8</b>이다. '
           +'분모의 숫자가 크다고 분수가 큰 것이 아니다.';
    } else {
      concl='<b>확인 필요</b> — 규칙에 어긋난 기록이 있다. 한 칸 길이를 다시 재어 보자.';
    }
    return {head:['비교','큰 분모','한 칸이 짧은 쪽 분모','분모 큰 쪽이 짧은가?','한 칸 길이(cm)','분모×한칸=12cm'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# LAB 6 : 소수 크기 비교
# ============================================================
LAB6 = r"""
function lbl(ctx,t,x,y,c,sz){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign='left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
function fmtd(v){
  var s=(v/100).toFixed(2);
  if(s.charAt(s.length-1)==='0') s=s.substring(0,s.length-1);
  if(s.charAt(s.length-1)==='0') s=s.substring(0,s.length-1);
  if(s.charAt(s.length-1)==='.') s=s.substring(0,s.length-1);
  return s;
}
function decs(v){
  var s=fmtd(v), p=s.indexOf('.');
  return (p<0)?0:(s.length-p-1);
}
var LX=40, LW=360, LY=210;

var LAB = {
  cw:440, ch:400, cvTitle:'소수 수직선',
  action:'수직선에 찍어 보기',
  hint0:'두 소수를 정하고 수직선 위에 찍어 보자. 오른쪽에 있는 수가 더 큰 수다.',
  sliders:[
    {id:'a',label:'첫 번째 소수',min:0,max:100,value:70,color:'#2563eb',step:1,fmt:function(v){return fmtd(v);}},
    {id:'b',label:'두 번째 소수',min:0,max:100,value:65,color:'#dc2626',step:1,fmt:function(v){return fmtd(v);}}
  ],
  readout:function(S,ran){
    return [{k:'첫 번째 수',v:fmtd(S.a)+' (소수 '+decs(S.a)+'자리)'},
            {k:'두 번째 수',v:fmtd(S.b)+' (소수 '+decs(S.b)+'자리)'}];
  },
  doneMsg:function(S){
    if(S.a===S.b) return '두 수가 같은 자리에 찍혔다. 같은 수다. 기록해 보자.';
    var big=(S.a>S.b)?fmtd(S.a):fmtd(S.b);
    return '오른쪽에 있는 '+big+'이(가) 더 큰 수다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var i;
    ctx.strokeStyle='#94a3b8';ctx.lineWidth=1.4;
    for(i=0;i<=100;i++){
      var x=LX+LW*i/100;
      var big=(i%10===0);
      ctx.beginPath();ctx.moveTo(x,LY-(big?14:6));ctx.lineTo(x,LY+(big?14:6));
      ctx.strokeStyle=big?'#475569':'#cbd5e1';ctx.lineWidth=big?2:1;ctx.stroke();
    }
    ctx.strokeStyle='#334155';ctx.lineWidth=3;
    ctx.beginPath();ctx.moveTo(LX,LY);ctx.lineTo(LX+LW,LY);ctx.stroke();
    ctx.font='bold 16px sans-serif';ctx.fillStyle='#475569';ctx.textAlign='center';
    for(i=0;i<=10;i++){
      ctx.fillText((i/10).toFixed(1),LX+LW*i/10,LY+36);
    }
    ctx.textAlign='left';

    var pa=(t===null)?0:Math.min(1,t/0.6);
    var pb=(t===null)?0:Math.max(0,Math.min(1,(t-0.4)/0.6));
    if(pa>0){
      var xa=LX+LW*(S.a/100)*pa;
      ctx.beginPath();ctx.arc(xa,LY-42,11,0,Math.PI*2);
      ctx.fillStyle='#2563eb';ctx.fill();
      ctx.strokeStyle='#1e40af';ctx.lineWidth=2;ctx.stroke();
      ctx.beginPath();ctx.moveTo(xa,LY-31);ctx.lineTo(xa,LY-4);
      ctx.strokeStyle='#2563eb';ctx.lineWidth=2.4;ctx.stroke();
      if(pa>=1){ctx.fillStyle='#1d4ed8';ctx.font='bold 18px sans-serif';ctx.textAlign='center';ctx.fillText(fmtd(S.a),xa,LY-60);}
    }
    if(pb>0){
      var xb=LX+LW*(S.b/100)*pb;
      ctx.beginPath();ctx.arc(xb,LY+62,11,0,Math.PI*2);
      ctx.fillStyle='#dc2626';ctx.fill();
      ctx.strokeStyle='#991b1b';ctx.lineWidth=2;ctx.stroke();
      ctx.beginPath();ctx.moveTo(xb,LY+51);ctx.lineTo(xb,LY+4);
      ctx.strokeStyle='#dc2626';ctx.lineWidth=2.4;ctx.stroke();
      if(pb>=1){ctx.fillStyle='#b91c1c';ctx.font='bold 18px sans-serif';ctx.textAlign='center';ctx.fillText(fmtd(S.b),xb,LY+92);}
    }
    ctx.textAlign='left';

    lbl(ctx,'0에서 1까지, 작은 눈금 한 칸 = 0.01',LX,40,'#52627a',17);
    ctx.fillStyle='#f1f6fd';ctx.fillRect(20,326,400,56);
    ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(20,326,400,56);
    var txt;
    if(t===null) txt='아직 찍지 않았다';
    else if(pb<1) txt='수직선 위를 이동하는 중...';
    else if(S.a===S.b) txt=fmtd(S.a)+' = '+fmtd(S.b);
    else txt=(S.a>S.b)?(fmtd(S.a)+' > '+fmtd(S.b)):(fmtd(S.a)+' < '+fmtd(S.b));
    lbl(ctx,txt,38,360,'#1f2937',22);
  },
  record:function(S){
    var da=decs(S.a), db=decs(S.b);
    var bigger=(S.a===S.b)?'같음':((S.a>S.b)?fmtd(S.a):fmtd(S.b));
    var moreDigit=(da===db)?'같음':((da>db)?fmtd(S.a):fmtd(S.b));
    return {a:S.a,b:S.b,sa:fmtd(S.a),sb:fmtd(S.b),da:da,db:db,bigger:bigger,moreDigit:moreDigit};
  },
  headA:['번호','첫 수','둘째 수','첫 수 소수 자릿수','둘째 수 소수 자릿수','더 큰 수','자릿수가 더 많은 수'],
  rowA:function(r,i){
    return [i+1,r.sa,r.sb,r.da,r.db,'<b>'+r.bigger+'</b>',r.moreDigit];
  },
  analyze:function(rec){
    var rows=[],cmp=0,hit=0,miss=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var judge='-';
      if(r.da!==r.db && r.bigger!=='같음'){
        cmp++;
        var ok=(r.moreDigit===r.bigger);
        if(ok) hit++; else miss++;
        judge='<span class="'+(ok?'ok':'no')+'">'+(ok?'맞음':'틀림')+'</span>';
      }
      rows.push([r.sa+' 와 '+r.sb, r.da+' / '+r.db, '<b>'+r.bigger+'</b>', r.moreDigit, judge]);
    }
    var stats=[
      {t:'자릿수로 판단해 본 기록',big:cmp+'개',
       p:'소수 자릿수가 서로 다르고 크기도 다른 기록만 셈.'},
      {t:'“자릿수가 많으면 크다”가 맞은 횟수',big:cmp?(hit+' / '+cmp):'비교 없음',
       p:'맞은 적도 있다면 그건 우연이다.'},
      {t:'반례',big:miss+'개',
       p:miss?'자릿수가 더 많은데도 더 작았던 경우.':'아직 반례가 없다. 0.7과 0.65를 비교해 보자.'}
    ];
    var concl;
    if(cmp===0){
      concl='<b>더 해 보자</b> — 아직 소수 자릿수가 다른 두 수를 비교한 기록이 없다. 0.7과 0.65처럼 자릿수가 다른 짝을 만들어 보자.';
    } else if(miss>0){
      concl='<b>정리</b> — 자릿수가 더 많은 쪽이 더 큰 수였던 경우도 있지만, <b>'+miss+'번은 반대였다.</b> '
           +'0.65는 0.7보다 뒤에 숫자가 하나 더 있지만 수직선에서는 더 왼쪽에 있다. '
           +'소수는 <b>자릿수의 개수가 아니라 소수 첫째 자리부터 차례로</b> 비교해야 한다.';
    } else {
      concl='<b>아직 부족</b> — 지금까지는 자릿수가 많은 쪽이 항상 컸다. 하지만 0.7과 0.65를 비교하면 어떻게 될까? 반례를 찾아보자.';
    }
    return {head:['비교','소수 자릿수','더 큰 수','자릿수 많은 수','“자릿수 많으면 크다”'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("elem34_carry_addition_lab.html",
     "받아올림 덧셈 실험실 — 자리끼리 더해서 이어 쓰면 될까?",
     "받아올림 덧셈 실험실 — 자리끼리 더해서 이어 쓰면 될까?",
     "두 수를 블록으로 놓고 합친 다음, 낱개 10개를 묶어 보자. 자리끼리 더한 값을 그냥 이어 쓴 수와 비교해 본다.",
     LAB2),
    ("elem34_multiplication_array_lab.html",
     "점 배열 실험실 — 3×4와 4×3은 다른 계산일까?",
     "점 배열 실험실 — 3×4와 4×3은 다른 계산일까?",
     "점을 가로·세로로 늘어놓고 직접 세어 본 뒤, 판을 90° 돌려 다시 세어 개수를 비교한다.",
     LAB3),
    ("elem34_division_remainder_lab.html",
     "구슬 나누기 실험실 — 남은 구슬은 얼마나 클 수 있을까?",
     "구슬 나누기 실험실 — 남은 구슬은 얼마나 클 수 있을까?",
     "구슬을 접시에 하나씩 똑같이 나누고, 남은 구슬 수를 기록해 나머지의 규칙을 찾아본다.",
     LAB4),
    ("elem34_unit_fraction_lab.html",
     "분수 띠 실험실 — 분모가 크면 큰 수일까?",
     "분수 띠 실험실 — 분모가 크면 큰 수일까?",
     "길이가 똑같은 12cm 띠를 서로 다르게 등분하고, 한 칸의 길이를 직접 대어 비교한다.",
     LAB5),
    ("elem34_decimal_numberline_lab.html",
     "소수 수직선 실험실 — 뒤에 숫자가 많으면 큰 수일까?",
     "소수 수직선 실험실 — 뒤에 숫자가 많으면 큰 수일까?",
     "두 소수를 수직선에 직접 찍어 위치를 비교하고, 소수 자릿수 개수로 크기를 판단할 수 있는지 확인한다.",
     LAB6),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL
    html = html.replace("@@TITLE@@", title)
    html = html.replace("@@H1@@", h1)
    html = html.replace("@@LEAD@@", lead)
    html = html.replace("@@LABJS@@", labjs)
    assert "@@" not in html, "토큰 누수: " + fname
    path = os.path.join(OUT, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    made.append(path)

# JS 문법 검사용 추출
for p in made:
    src = open(p, encoding="utf-8").read()
    js = re.search(r"<script>(.*?)</script>", src, re.S).group(1)
    open("/home/claude/_chk_" + os.path.basename(p) + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
