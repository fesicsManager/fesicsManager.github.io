# -*- coding: utf-8 -*-
"""초등 5-6학년군 '변화와 관계' 실험 5종"""
import os, re

OUT = "/mnt/user-data/outputs"
src = open("/home/claude/gen_math_labs.py", encoding="utf-8").read()
TPL = re.search(r'TPL = r"""(.*?)"""\n', src, re.S).group(1)

BASE = r"""
function lbl(ctx,t,x,y,c,sz,al){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
function box(ctx,x,y,w,h){ctx.fillStyle='#f1f6fd';ctx.fillRect(x,y,w,h);ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(x,y,w,h);}
function r1(v){return Math.round(v*10)/10;}
function r2(v){return Math.round(v*100)/100;}
function r3(v){return Math.round(v*1000)/1000;}
function gcd(x,y){while(y){var t=x%y;x=y;y=t;}return x;}
"""

# ============================================================
# 1. 두 양의 대응 관계
# ============================================================
LAB_CORR = BASE + r"""
var KINDS=[
  {name:'자동차와 바퀴',x:'자동차(대)',y:'바퀴(개)',f:function(n){return n*4;}},
  {name:'동생과 형의 나이',x:'동생(살)',y:'형(살)',f:function(n){return n+3;}},
  {name:'사각형과 성냥개비',x:'사각형(개)',y:'성냥개비(개)',f:function(n){return 3*n+1;}}
];
var LAB = {
  cw:440, ch:400, cvTitle:'대응 관계 표',
  action:'표를 채워 규칙 찾기',
  hint0:'두 양의 관계를 고르고 표를 채워 보자.',
  sliders:[
    {id:'kind',label:'관계',min:0,max:2,value:0,color:'#2563eb',fmt:function(v){return KINDS[v].name;}},
    {id:'n',label:'왼쪽 양의 값',min:1,max:12,value:5,color:'#16a34a',unit:''}
  ],
  readout:function(S,ran){
    var K=KINDS[S.kind];
    return [{k:K.x+' '+S.n,v:ran?(K.y+' '+K.f(S.n)):'채워 보자'},
            {k:'차 / 몫',v:ran?((K.f(S.n)-S.n)+' / '+r2(K.f(S.n)/S.n)):'-'}];
  },
  doneMsg:function(S){
    var K=KINDS[S.kind], y=K.f(S.n);
    return K.x+' '+S.n+'일 때 '+K.y+'는 '+y+'. 차는 '+(y-S.n)+', 몫은 '+r2(y/S.n)+'이다. 다른 값도 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var K=KINDS[S.kind], i;
    var cols=8, cw=44, x0=52, y0=110;
    var shown=(t===null)?0:Math.ceil(t*cols);
    lbl(ctx,K.name,24,40,'#1d4ed8',20);
    lbl(ctx,K.x,x0-8,y0+22,'#334155',15,'right');
    lbl(ctx,K.y,x0-8,y0+62,'#334155',15,'right');
    for(i=0;i<cols;i++){
      var x=x0+i*cw, on=(i<shown), v=i+1;
      ctx.fillStyle=(v===S.n)?'#dbeafe':'#fff';
      ctx.fillRect(x,y0,cw,40);ctx.fillRect(x,y0+40,cw,40);
      ctx.strokeStyle='#94a3b8';ctx.lineWidth=1.6;
      ctx.strokeRect(x,y0,cw,40);ctx.strokeRect(x,y0+40,cw,40);
      ctx.fillStyle='#1f2937';ctx.font='bold 17px sans-serif';ctx.textAlign='center';
      ctx.fillText(v,x+cw/2,y0+26);
      ctx.fillStyle=on?'#1d4ed8':'#cbd5e1';
      ctx.fillText(on?K.f(v):'?',x+cw/2,y0+66);
    }
    ctx.textAlign='left';
    if(shown>=2){
      lbl(ctx,'옆으로 갈 때 늘어나는 양 : '+(K.f(2)-K.f(1)),x0,y0+96,'#52627a',17);
    }
    box(ctx,20,238,400,142);
    var y=K.f(S.n);
    lbl(ctx,(t===null)?'표를 채우면 규칙이 보일까?':(K.x+' '+S.n+'  →  '+K.y+' '+y),38,272,'#1f2937',21);
    if(t!==null){
      lbl(ctx,'두 값의 차 : '+y+' − '+S.n+' = '+(y-S.n),38,304,'#b45309',18);
      lbl(ctx,'두 값의 몫 : '+y+' ÷ '+S.n+' = '+r2(y/S.n),38,332,'#15803d',18);
      lbl(ctx,'차와 몫 중 어느 쪽이 항상 같을까? 여러 번 기록해 보자.',38,362,'#52627a',16);
    }
  },
  record:function(S){
    var K=KINDS[S.kind], y=K.f(S.n);
    return {kind:S.kind,name:K.name,n:S.n,y:y,diff:y-S.n,q:r3(y/S.n)};
  },
  headA:['번호','관계','왼쪽 값','오른쪽 값','차','몫'],
  rowA:function(r,i){ return [i+1,r.name,r.n,'<b>'+r.y+'</b>',r.diff,r.q]; },
  analyze:function(rec){
    var rows=[],groups={},i,k;
    for(i=0;i<rec.length;i++){
      var r=rec[i];
      if(!groups[r.kind]) groups[r.kind]={name:r.name,diffs:{},qs:{},n:0};
      groups[r.kind].diffs[r.diff]=true;
      groups[r.kind].qs[r.q]=true;
      groups[r.kind].n++;
      rows.push([r.name, r.n, r.y, r.diff, r.q]);
    }
    var judged=[],dOnly=0,qOnly=0,neither=0,tested=0;
    for(k in groups){
      var g=groups[k], dn=0,qn=0,kk;
      for(kk in g.diffs) dn++;
      for(kk in g.qs) qn++;
      if(g.n<2) continue;
      tested++;
      var verdict;
      if(dn===1&&qn>1){ verdict='차가 일정 (더하는 관계)'; dOnly++; }
      else if(qn===1&&dn>1){ verdict='몫이 일정 (곱하는 관계)'; qOnly++; }
      else if(dn===1&&qn===1){ verdict='값이 하나뿐 — 더 기록 필요'; }
      else { verdict='차도 몫도 일정하지 않음 (곱하고 더하는 관계)'; neither++; }
      judged.push(g.name+' : '+verdict);
    }
    var stats=[
      {t:'2번 이상 기록한 관계',big:tested+'가지',
       p:tested?judged.join(' / '):'같은 관계로 값을 바꿔 두 번 이상 기록해야 규칙을 판정할 수 있다.'},
      {t:'차가 일정한 관계',big:dOnly+'가지',p:'왼쪽 값에 같은 수를 더하면 오른쪽 값이 나오는 관계.'},
      {t:'몫이 일정한 관계',big:qOnly+'가지',p:'왼쪽 값에 같은 수를 곱하면 오른쪽 값이 나오는 관계.'}
    ];
    var concl;
    if(tested===0){
      concl='<b>더 해 보자</b> — 같은 관계에서 왼쪽 값을 바꿔 두 번 이상 기록해야 차가 일정한지 몫이 일정한지 알 수 있다.';
    } else if(neither>0){
      concl='<b>정리</b> — 관계마다 규칙의 종류가 달랐다. 차가 일정한 것, 몫이 일정한 것, 그리고 <b>차도 몫도 일정하지 않은 것</b>까지 있었다. '
           +'사각형과 성냥개비는 3을 곱하고 1을 더하는 관계라서, 한 칸 차이만 보고 “+3 규칙”이라고 하면 사각형 10개일 때 값을 틀리게 된다. '
           +'대응 관계는 <b>왼쪽 값에서 오른쪽 값을 바로 구하는 식</b>으로 써야 한다.';
    } else {
      concl='<b>정리</b> — 지금까지 확인한 관계는 차가 일정하거나 몫이 일정했다. 사각형과 성냥개비 관계도 기록해 보면 다른 종류가 나온다.';
    }
    return {head:['관계','왼쪽 값','오른쪽 값','차','몫'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 비례식
# ============================================================
LAB_PROP = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'비례식 판',
  action:'외항과 내항 곱해 보기',
  hint0:'네 수를 정해 비례식을 만들고, 바깥끼리·안끼리 곱해 보자.',
  sliders:[
    {id:'a',label:'첫째 항',min:1,max:12,value:2,color:'#2563eb',unit:''},
    {id:'b',label:'둘째 항',min:1,max:12,value:3,color:'#60a5fa',unit:''},
    {id:'c',label:'셋째 항',min:1,max:12,value:4,color:'#16a34a',unit:''},
    {id:'d',label:'넷째 항',min:1,max:12,value:6,color:'#4ade80',unit:''}
  ],
  readout:function(S,ran){
    return [{k:'식',v:S.a+' : '+S.b+' = '+S.c+' : '+S.d},
            {k:'두 비율',v:r3(S.a/S.b)+' / '+r3(S.c/S.d)}];
  },
  doneMsg:function(S){
    var ad=S.a*S.d, bc=S.b*S.c;
    return '외항의 곱 '+ad+', 내항의 곱 '+bc+'. '+((ad===bc)?'같으므로 비례식이 성립한다.':'다르므로 비례식이 아니다.')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var y=120;
    ctx.font='bold 40px sans-serif';ctx.textAlign='center';
    var xs=[80,150,220,290,360];
    var txt=[S.a,':',S.b,'=',S.c];
    ctx.fillStyle='#1f2937';
    ctx.fillText(S.a,72,y); ctx.fillText(':',116,y);
    ctx.fillText(S.b,160,y); ctx.fillText('=',216,y);
    ctx.fillText(S.c,272,y); ctx.fillText(':',316,y);
    ctx.fillText(S.d,360,y);
    ctx.textAlign='left';
    var p1=(t===null)?0:Math.min(1,t/0.5);
    var p2=(t===null)?0:Math.max(0,(t-0.5)/0.5);
    if(p1>0){
      ctx.strokeStyle='#dc2626';ctx.lineWidth=3;ctx.globalAlpha=p1;
      ctx.beginPath();ctx.moveTo(72,y+14);
      ctx.quadraticCurveTo(216,y+70,360,y+14);ctx.stroke();
      ctx.globalAlpha=1;
      lbl(ctx,'외항의 곱  '+S.a+' × '+S.d+' = '+(S.a*S.d),24,y+96,'#b91c1c',19);
    }
    if(p2>0){
      ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.globalAlpha=p2;
      ctx.beginPath();ctx.moveTo(160,y-46);
      ctx.quadraticCurveTo(216,y-92,272,y-46);ctx.stroke();
      ctx.globalAlpha=1;
      lbl(ctx,'내항의 곱  '+S.b+' × '+S.c+' = '+(S.b*S.c),24,y+124,'#1d4ed8',19);
    }
    box(ctx,20,268,400,112);
    var ad=S.a*S.d, bc=S.b*S.c, ok=(ad===bc);
    lbl(ctx,(t===null)?'비례식이 성립할까?':(ok?'외항의 곱 = 내항의 곱':'외항의 곱 ≠ 내항의 곱'),38,302,ok?'#15803d':'#b91c1c',21);
    lbl(ctx,'왼쪽 비율 '+r3(S.a/S.b)+'   오른쪽 비율 '+r3(S.c/S.d),38,334,'#52627a',18);
    lbl(ctx,(t===null)?'':((Math.abs(S.a/S.b-S.c/S.d)<1e-9)?'두 비율이 같다 → 비례식이다':'두 비율이 다르다 → 비례식이 아니다'),
        38,364,'#334155',18);
  },
  record:function(S){
    var ad=S.a*S.d, bc=S.b*S.c;
    return {a:S.a,b:S.b,c:S.c,d:S.d,ad:ad,bc:bc,eq:(ad===bc),
            ratioEq:(Math.abs(S.a/S.b-S.c/S.d)<1e-9),
            r1v:r3(S.a/S.b),r2v:r3(S.c/S.d)};
  },
  headA:['번호','식','외항의 곱','내항의 곱','두 곱이 같나?','두 비율','비례식인가?'],
  rowA:function(r,i){
    return [i+1,r.a+':'+r.b+' = '+r.c+':'+r.d,r.ad,r.bc,
            '<span class="'+(r.eq?'ok':'no')+'">'+(r.eq?'○':'×')+'</span>',
            r.r1v+' / '+r.r2v,
            '<span class="'+(r.ratioEq?'ok':'no')+'">'+(r.ratioEq?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],match=0,tr=0,fa=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i], m=(r.eq===r.ratioEq);
      if(m) match++;
      if(r.ratioEq) tr++; else fa++;
      rows.push([r.a+':'+r.b+' = '+r.c+':'+r.d, r.ad, r.bc,
                 '<span class="'+(r.eq?'ok':'no')+'">'+(r.eq?'○':'×')+'</span>',
                 '<span class="'+(r.ratioEq?'ok':'no')+'">'+(r.ratioEq?'○':'×')+'</span>',
                 '<span class="'+(m?'ok':'no')+'">'+(m?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'“두 곱이 같다”와 “비례식이다”가 일치',big:match+' / '+rec.length,
       p:'곱만 비교해서 비례식인지 판단할 수 있는지 확인한 결과.'},
      {t:'비례식이 성립한 기록',big:tr+'개',p:tr?'두 비율이 같았던 경우.':'2:3 = 4:6처럼 성립하는 식도 만들어 보자.'},
      {t:'성립하지 않은 기록',big:fa+'개',p:fa?'두 비율이 달랐던 경우.':'2:3 = 4:7처럼 성립하지 않는 식도 만들어 보자.'}
    ];
    var concl;
    if(tr===0||fa===0){
      concl='<b>더 해 보자</b> — 성립하는 식과 성립하지 않는 식을 <b>둘 다</b> 기록해야 규칙을 확인할 수 있다.';
    } else if(match===rec.length){
      concl='<b>정리</b> — 비례식이 성립할 때는 언제나 <b>외항의 곱 = 내항의 곱</b>이었고, 성립하지 않을 때는 두 곱도 달랐다. '
           +'그래서 2 : 3 = 4 : □ 처럼 모르는 항이 있어도, 2 × □ = 3 × 4로 바꿔 풀 수 있다.';
    } else {
      concl='<b>확인 필요</b> — 두 판단이 어긋난 기록이 있다. 값을 다시 확인해 보자.';
    }
    return {head:['비례식','외항의 곱','내항의 곱','두 곱이 같나?','비례식인가?','일치하나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 비례배분
# ============================================================
LAB_SHARE = BASE + r"""
var LAB = {
  cw:440, ch:420, cvTitle:'비례배분판',
  action:'비대로 나누기',
  hint0:'전체 개수와 나눌 비를 정하고, 비대로 나누어 보자.',
  sliders:[
    {id:'T',label:'전체 사탕',min:4,max:60,value:20,color:'#f59e0b',unit:'개'},
    {id:'a',label:'첫째 몫의 비',min:1,max:9,value:3,color:'#dc2626',unit:''},
    {id:'b',label:'둘째 몫의 비',min:1,max:9,value:2,color:'#2563eb',unit:''}
  ],
  calc:function(S){
    var s=S.a+S.b, unit=S.T/s;
    return {s:s,unit:unit,pa:S.T*S.a/s,pb:S.T*S.b/s};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'한 묶음',v:ran?(r2(c.unit)+'개'):'나누어 보자'},
            {k:'나눈 결과',v:ran?(r2(c.pa)+' / '+r2(c.pb)):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '전체를 '+c.s+'묶음으로 보면 한 묶음은 '+r2(c.unit)+'개. '+S.a+'묶음과 '+S.b+'묶음이니 '+r2(c.pa)+'개와 '+r2(c.pb)+'개다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var split=(t===null)?0:Math.min(1,t);
    var n=Math.min(S.T,60);
    for(i=0;i<n;i++){
      var col=i%12, row=Math.floor(i/12);
      var isA=(i<Math.round(c.pa));
      var gapx=split*(isA?-26:26);
      var x=52+col*28+gapx, y=90+row*28;
      ctx.beginPath();ctx.arc(x,y,10,0,Math.PI*2);
      ctx.fillStyle=isA?'#f87171':'#93c5fd';ctx.fill();
      ctx.strokeStyle=isA?'#b91c1c':'#1d4ed8';ctx.lineWidth=1.6;ctx.stroke();
    }
    lbl(ctx,'전체 '+S.T+'개를 '+S.a+' : '+S.b+'로 나누기',24,44,'#1d4ed8',19);
    var BX=40,BW=360,BY=248;
    ctx.fillStyle='#f87171';ctx.fillRect(BX,BY,BW*S.a/c.s,30);
    ctx.fillStyle='#93c5fd';ctx.fillRect(BX+BW*S.a/c.s,BY,BW*S.b/c.s,30);
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    for(i=1;i<c.s;i++){ ctx.beginPath();ctx.moveTo(BX+BW*i/c.s,BY);ctx.lineTo(BX+BW*i/c.s,BY+30);ctx.stroke(); }
    ctx.strokeRect(BX,BY,BW,30);
    lbl(ctx,'전체 = '+c.s+'묶음',BX,BY+50,'#52627a',17);
    box(ctx,20,296,400,110);
    lbl(ctx,(t===null)?'비대로 나누면 각각 몇 개일까?':('한 묶음 '+r2(c.unit)+'개  →  '+r2(c.pa)+'개 와 '+r2(c.pb)+'개'),38,328,'#1f2937',20);
    lbl(ctx,(t===null)?'':('두 몫의 합 : '+r2(c.pa+c.pb)+'개  (전체 '+S.T+'개)'),38,358,'#15803d',18);
    lbl(ctx,(t===null)?'':('전체를 비의 수로 그냥 나누면 : '+r2(S.T/S.a)+' , '+r2(S.T/S.b)+'  (합 '+r2(S.T/S.a+S.T/S.b)+')'),38,388,'#b91c1c',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {T:S.T,a:S.a,b:S.b,s:c.s,unit:r2(c.unit),pa:r2(c.pa),pb:r2(c.pb),
            sum:r2(c.pa+c.pb),
            wa:r2(S.T/S.a),wb:r2(S.T/S.b),wsum:r2(S.T/S.a+S.T/S.b)};
  },
  headA:['번호','전체','비','묶음 수','한 묶음','첫째 몫','둘째 몫','두 몫의 합'],
  rowA:function(r,i){
    return [i+1,r.T+'개',r.a+' : '+r.b,r.s,r.unit,'<b>'+r.pa+'</b>','<b>'+r.pb+'</b>',r.sum];
  },
  analyze:function(rec){
    var rows=[],ok=0,wok=0,ratioOk=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var a=(Math.abs(r.sum-r.T)<0.02);
      var w=(Math.abs(r.wsum-r.T)<0.02);
      var rr=(Math.abs(r.pa/r.pb-r.a/r.b)<0.001);
      if(a) ok++;
      if(w) wok++;
      if(rr) ratioOk++;
      rows.push([r.T+'개를 '+r.a+':'+r.b, r.pa+' / '+r.pb, r.sum,
                 '<span class="'+(a?'ok':'no')+'">'+(a?'○':'×')+'</span>',
                 r.wa+' / '+r.wb, r.wsum,
                 '<span class="'+(w?'ok':'no')+'">'+(w?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'두 몫의 합 = 전체',big:ok+' / '+rec.length,p:'비례배분이 제대로 되었는지 검사하는 방법이다.'},
      {t:'“전체 ÷ 비의 수”로 나눈 방법이 맞은 횟수',big:wok+' / '+rec.length,
       p:'전체를 비의 각 수로 그냥 나누면 합이 전체가 되는지 확인했다.'},
      {t:'나눈 두 몫의 비 = 처음 비',big:ratioOk+' / '+rec.length,p:'결과가 정해진 비를 지키는지 확인한 결과.'}
    ];
    var concl;
    if(ok===rec.length && wok===0){
      concl='<b>정리</b> — 비대로 나눈 두 몫의 합은 언제나 전체와 같았지만, <b>전체를 비의 수로 그냥 나눈 방법은 한 번도 맞지 않았다.</b> '
           +'3 : 2로 나눌 때는 전체를 5묶음으로 보고, 한 묶음을 구한 뒤 3묶음·2묶음을 가져가야 한다.';
    } else if(ok===rec.length){
      concl='<b>정리</b> — 비대로 나눈 두 몫의 합은 항상 전체와 같았다. 전체를 (비의 합)묶음으로 나누는 것이 핵심이다.';
    } else {
      concl='<b>확인 필요</b> — 두 몫의 합이 전체와 다른 기록이 있다.';
    }
    return {head:['문제','나눈 몫','합','전체와 같나?','그냥 나눈 값','그 합','전체와 같나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 백분율과 기준량
# ============================================================
LAB_PCT = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'성공률 비교판',
  action:'성공률 계산하기',
  hint0:'두 사람의 던진 횟수와 성공 횟수를 정하고 성공률을 비교해 보자.',
  sliders:[
    {id:'sa',label:'가 성공',min:0,max:30,value:8,color:'#dc2626',unit:'번'},
    {id:'ta',label:'가 던진 횟수',min:1,max:30,value:10,color:'#f87171',unit:'번'},
    {id:'sb',label:'나 성공',min:0,max:30,value:15,color:'#2563eb',unit:'번'},
    {id:'tb',label:'나 던진 횟수',min:1,max:30,value:25,color:'#60a5fa',unit:'번'}
  ],
  calc:function(S){
    var sa=Math.min(S.sa,S.ta), sb=Math.min(S.sb,S.tb);
    return {sa:sa,ta:S.ta,sb:sb,tb:S.tb,pa:sa/S.ta*100,pb:sb/S.tb*100};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'가',v:c.sa+'/'+c.ta+(ran?(' = '+r1(c.pa)+'%'):'')},
            {k:'나',v:c.sb+'/'+c.tb+(ran?(' = '+r1(c.pb)+'%'):'')}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    var more=(c.sa>c.sb)?'가':((c.sb>c.sa)?'나':'같음');
    var high=(c.pa>c.pb)?'가':((c.pb>c.pa)?'나':'같음');
    return '성공 횟수가 많은 쪽은 '+more+', 성공률이 높은 쪽은 '+high+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var grow=(t===null)?0:Math.min(1,t);
    function person(y,name,s,tt,pct,col){
      lbl(ctx,name+'  '+s+' / '+tt,36,y-10,'#334155',18);
      var BX=36,BW=368;
      for(i=0;i<tt;i++){
        var w=BW/tt;
        ctx.fillStyle=(i<s)?col:'#e8eef7';
        ctx.fillRect(BX+i*w,y,w-1.5,32);
      }
      ctx.strokeStyle='#334155';ctx.lineWidth=2;ctx.strokeRect(BX,y,BW,32);
      if(grow>0){
        ctx.fillStyle=col;ctx.font='bold 19px sans-serif';ctx.textAlign='right';
        ctx.fillText(r1(pct*grow)+'%',BX+BW,y+58);ctx.textAlign='left';
      }
    }
    lbl(ctx,'누가 더 잘 던졌을까?',24,36,'#1d4ed8',19);
    person(70,'가',c.sa,c.ta,c.pa,'#ef4444');
    person(180,'나',c.sb,c.tb,c.pb,'#3b82f6');
    box(ctx,20,268,400,112);
    var more=(c.sa>c.sb)?'가':((c.sb>c.sa)?'나':'같음');
    var high=(c.pa>c.pb)?'가':((c.pb>c.pa)?'나':'같음');
    lbl(ctx,'성공 횟수가 많은 쪽 : '+more+'  ('+c.sa+' vs '+c.sb+')',38,300,'#52627a',18);
    lbl(ctx,(t===null)?'성공률은 누가 높을까?':('성공률이 높은 쪽 : '+high+'  ('+r1(c.pa)+'% vs '+r1(c.pb)+'%)'),38,332,'#1f2937',19);
    lbl(ctx,(t===null)?'':((more!==high&&more!=='같음'&&high!=='같음')?'두 답이 다르다!':'두 답이 같다'),
        38,362,(more!==high)?'#b91c1c':'#15803d',18);
  },
  record:function(S){
    var c=this.calc(S);
    var more=(c.sa>c.sb)?'가':((c.sb>c.sa)?'나':'같음');
    var high=(c.pa>c.pb)?'가':((c.pb>c.pa)?'나':'같음');
    return {sa:c.sa,ta:c.ta,sb:c.sb,tb:c.tb,pa:r1(c.pa),pb:r1(c.pb),more:more,high:high,
            agree:(more===high)};
  },
  headA:['번호','가','나','가 성공률','나 성공률','성공 횟수 많은 쪽','성공률 높은 쪽','같은 답?'],
  rowA:function(r,i){
    return [i+1,r.sa+'/'+r.ta,r.sb+'/'+r.tb,r.pa+'%',r.pb+'%',r.more,'<b>'+r.high+'</b>',
            '<span class="'+(r.agree?'ok':'no')+'">'+(r.agree?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],agree=0,counter=0,sameBase=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.agree) agree++; else counter++;
      if(r.ta===r.tb) sameBase++;
      rows.push([r.sa+'/'+r.ta+' vs '+r.sb+'/'+r.tb, r.pa+'% / '+r.pb+'%', r.more, '<b>'+r.high+'</b>',
                 (r.ta===r.tb)?'같음':'다름',
                 '<span class="'+(r.agree?'ok':'no')+'">'+(r.agree?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'두 판단이 같았던 횟수',big:agree+' / '+rec.length,p:'성공 횟수로 고른 답과 성공률로 고른 답이 같았던 경우.'},
      {t:'뒤집힌 경우',big:counter+'개',
       p:counter?'성공 횟수는 적은데 성공률은 높았던 경우다.':'던진 횟수를 크게 다르게 해서 다시 비교해 보자.'},
      {t:'던진 횟수가 같았던 기록',big:sameBase+'개',
       p:'기준량이 같을 때는 성공 횟수만 비교해도 된다.'}
    ];
    var concl;
    if(counter===0){
      concl='<b>더 해 보자</b> — 아직 판단이 뒤집힌 기록이 없다. 8/10과 15/25처럼 <b>던진 횟수를 다르게</b> 해서 비교해 보자.';
    } else {
      concl='<b>정리</b> — 성공 횟수가 더 많은데 성공률은 더 낮은 경우가 '+counter+'번 나왔다. '
           +'횟수만으로는 잘한 정도를 비교할 수 없다. <b>기준량(던진 횟수)이 다르면 반드시 비율로 바꿔서</b> 비교해야 한다. '
           +'반대로 던진 횟수가 같다면 횟수만 비교해도 된다.';
    }
    return {head:['비교','성공률','횟수 많은 쪽','성공률 높은 쪽','기준량','같은 답?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 속력
# ============================================================
LAB_SPEED = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'달리기 비교판',
  action:'같은 시간 동안 달려 보기',
  hint0:'두 사람이 간 거리와 걸린 시간을 정하고, 누가 더 빠른지 확인해 보자.',
  sliders:[
    {id:'da',label:'가 간 거리',min:1,max:30,value:12,color:'#dc2626',unit:'km'},
    {id:'ta',label:'가 걸린 시간',min:1,max:10,value:3,color:'#f87171',unit:'시간'},
    {id:'db',label:'나 간 거리',min:1,max:30,value:20,color:'#2563eb',unit:'km'},
    {id:'tb',label:'나 걸린 시간',min:1,max:10,value:8,color:'#60a5fa',unit:'시간'}
  ],
  readout:function(S,ran){
    return [{k:'가의 속력',v:ran?(r2(S.da/S.ta)+' km/시'):'달려 보자'},
            {k:'나의 속력',v:ran?(r2(S.db/S.tb)+' km/시'):'-'}];
  },
  doneMsg:function(S){
    var va=S.da/S.ta, vb=S.db/S.tb;
    var far=(S.da>S.db)?'가':((S.db>S.da)?'나':'같음');
    var fast=(va>vb)?'가':((vb>va)?'나':'같음');
    return '멀리 간 쪽은 '+far+', 빠른 쪽은 '+fast+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var va=S.da/S.ta, vb=S.db/S.tb;
    var vmax=Math.max(va,vb,1);
    var run=(t===null)?0:Math.min(1,t);
    function track(y,name,v,col,d,tt){
      var TX=52,TW=340;
      ctx.strokeStyle='#cbd5e1';ctx.lineWidth=2;
      ctx.beginPath();ctx.moveTo(TX,y+22);ctx.lineTo(TX+TW,y+22);ctx.stroke();
      lbl(ctx,name,24,y+28,col,17);
      var x=TX+TW*(v/vmax)*run;
      ctx.beginPath();ctx.arc(x,y+10,11,0,Math.PI*2);
      ctx.fillStyle=col;ctx.fill();
      ctx.strokeStyle='#1f2937';ctx.lineWidth=1.6;ctx.stroke();
      lbl(ctx,d+'km / '+tt+'시간',TX,y-8,'#52627a',15);
      if(run>=1){ lbl(ctx,r2(v)+' km/시',TX+TW,y+52,col,17,'right'); }
    }
    lbl(ctx,'1시간 동안 누가 더 멀리 갈까?',24,36,'#1d4ed8',19);
    track(80,'가',va,'#ef4444',S.da,S.ta);
    track(180,'나',vb,'#3b82f6',S.db,S.tb);
    lbl(ctx,'같은 시간(1시간) 동안 간 거리로 비교한다',52,268,'#64748b',16);
    box(ctx,20,282,400,98);
    var far=(S.da>S.db)?'가':((S.db>S.da)?'나':'같음');
    var fast=(va>vb)?'가':((vb>va)?'나':'같음');
    lbl(ctx,'더 멀리 간 쪽 : '+far+'  ('+S.da+'km vs '+S.db+'km)',38,314,'#52627a',18);
    lbl(ctx,(t===null)?'더 빠른 쪽은?':('더 빠른 쪽 : '+fast+'  ('+r2(va)+' vs '+r2(vb)+' km/시)'),38,344,'#1f2937',19);
    lbl(ctx,(t===null)?'':((far!==fast&&far!=='같음'&&fast!=='같음')?'두 답이 다르다!':'두 답이 같다'),
        38,372,(far!==fast)?'#b91c1c':'#15803d',18);
  },
  record:function(S){
    var va=S.da/S.ta, vb=S.db/S.tb;
    var far=(S.da>S.db)?'가':((S.db>S.da)?'나':'같음');
    var fast=(va>vb)?'가':((vb>va)?'나':'같음');
    return {da:S.da,ta:S.ta,db:S.db,tb:S.tb,va:r2(va),vb:r2(vb),far:far,fast:fast,
            agree:(far===fast),sameT:(S.ta===S.tb)};
  },
  headA:['번호','가','나','가의 속력','나의 속력','멀리 간 쪽','빠른 쪽','같은 답?'],
  rowA:function(r,i){
    return [i+1,r.da+'km/'+r.ta+'시간',r.db+'km/'+r.tb+'시간',r.va,r.vb,r.far,'<b>'+r.fast+'</b>',
            '<span class="'+(r.agree?'ok':'no')+'">'+(r.agree?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],agree=0,counter=0,st=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.agree) agree++; else counter++;
      if(r.sameT) st++;
      rows.push([r.da+'km/'+r.ta+'h vs '+r.db+'km/'+r.tb+'h', r.va+' / '+r.vb, r.far, '<b>'+r.fast+'</b>',
                 r.sameT?'같음':'다름',
                 '<span class="'+(r.agree?'ok':'no')+'">'+(r.agree?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'두 판단이 같았던 횟수',big:agree+' / '+rec.length,p:'거리로 고른 답과 속력으로 고른 답이 같았던 경우.'},
      {t:'뒤집힌 경우',big:counter+'개',
       p:counter?'더 멀리 갔는데 더 느렸던 경우다.':'걸린 시간을 크게 다르게 해서 비교해 보자.'},
      {t:'걸린 시간이 같았던 기록',big:st+'개',p:'시간이 같으면 거리만 비교해도 된다.'}
    ];
    var concl;
    if(counter===0){
      concl='<b>더 해 보자</b> — 아직 판단이 뒤집힌 기록이 없다. 12km를 3시간, 20km를 8시간처럼 <b>시간을 다르게</b> 해서 비교해 보자.';
    } else {
      concl='<b>정리</b> — 더 멀리 갔는데 더 느렸던 경우가 '+counter+'번 나왔다. 거리만으로는 빠르기를 비교할 수 없다. '
           +'<b>속력 = 거리 ÷ 시간</b>으로 “1시간 동안 가는 거리”를 맞춰 놓고 비교해야 한다. 걸린 시간이 같다면 거리만 비교해도 된다.';
    }
    return {head:['비교','속력(km/시)','멀리 간 쪽','빠른 쪽','걸린 시간','같은 답?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("elem56_correspondence_lab.html",
     "대응 관계 실험실 — 한 칸 차이만 보면 될까?",
     "대응 관계 실험실 — 한 칸 차이만 보면 될까?",
     "여러 관계의 표를 채우고 두 양의 차와 몫을 기록해, 어떤 규칙이 항상 성립하는지 판정한다.",
     LAB_CORR),
    ("elem56_proportion_equation_lab.html",
     "비례식 실험실 — 외항과 내항의 곱은 왜 같을까?",
     "비례식 실험실 — 외항과 내항의 곱은 왜 같을까?",
     "네 수로 비례식을 만들어 바깥끼리·안끼리 곱하고, 비례식 성립 여부와 비교해 기록한다.",
     LAB_PROP),
    ("elem56_proportional_sharing_lab.html",
     "비례배분 실험실 — 전체를 비의 수로 나누면 될까?",
     "비례배분 실험실 — 전체를 비의 수로 나누면 될까?",
     "전체를 정해진 비로 나누고, 두 몫의 합이 전체와 같은지 확인하며 잘못된 방법과 비교한다.",
     LAB_SHARE),
    ("elem56_percentage_base_lab.html",
     "성공률 실험실 — 많이 성공하면 더 잘한 걸까?",
     "성공률 실험실 — 많이 성공하면 더 잘한 걸까?",
     "던진 횟수가 다른 두 사람의 성공 횟수와 성공률을 비교해, 판단이 뒤집히는 경우를 찾는다.",
     LAB_PCT),
    ("elem56_speed_lab.html",
     "속력 실험실 — 멀리 간 사람이 더 빠를까?",
     "속력 실험실 — 멀리 간 사람이 더 빠를까?",
     "간 거리와 걸린 시간을 바꿔 가며 속력을 구하고, 거리만으로 빠르기를 비교할 수 있는지 확인한다.",
     LAB_SPEED),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c6_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
