# -*- coding: utf-8 -*-
"""고등 대수 — 지수와 로그 3종 + 삼각함수 2종"""
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
function r4(v){return Math.round(v*10000)/10000;}
function sg(v){return (v<0)?(' − '+(-v)):(' + '+v);}
var CX=220, CY=210, U=22;
function grid(ctx,xr,yr){
  var i;
  ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
  for(i=-xr;i<=xr;i++){ ctx.beginPath();ctx.moveTo(CX+i*U,CY-yr*U);ctx.lineTo(CX+i*U,CY+yr*U);ctx.stroke(); }
  for(i=-yr;i<=yr;i++){ ctx.beginPath();ctx.moveTo(CX-xr*U,CY+i*U);ctx.lineTo(CX+xr*U,CY+i*U);ctx.stroke(); }
  ctx.strokeStyle='#334155';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(CX-xr*U,CY);ctx.lineTo(CX+xr*U,CY);ctx.stroke();
  ctx.beginPath();ctx.moveTo(CX,CY-yr*U);ctx.lineTo(CX,CY+yr*U);ctx.stroke();
}
"""

# ============================================================
# 1. 지수의 확장
# ============================================================
LAB_EXP = BASE + r"""
function powLoop(a,k){ var v=1,i; for(i=0;i<k;i++) v*=a; return v; }
var LAB = {
  cw:440, ch:430, cvTitle:'지수 사다리판',
  action:'한 칸씩 내려가 보기',
  hint0:'밑을 정하고, 지수를 하나씩 줄이며 값이 어떻게 변하는지 보자.',
  sliders:[
    {id:'a',label:'밑 a',min:2,max:5,value:3,color:'#2563eb',unit:''},
    {id:'n',label:'지수 n',min:1,max:5,value:2,color:'#16a34a',unit:''}
  ],
  calc:function(S){
    var pn=powLoop(S.a,S.n);
    var neg=1/pn;
    return {pn:pn,neg:neg,prod:pn*neg,zero:1};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'a^'+S.n,v:c.pn},
            {k:'a^(−'+S.n+')',v:ran?r4(c.neg):'내려가 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'a^'+S.n+' = '+c.pn+', a^(−'+S.n+') = '+r4(c.neg)+'.  두 값을 곱하면 '+r3(c.prod)+'이다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var rows=[];
    for(i=S.n;i>=-S.n;i--){
      var v=(i>0)?powLoop(S.a,i):((i===0)?1:(1/powLoop(S.a,-i)));
      rows.push([i,v]);
    }
    var shown=(t===null)?1:Math.ceil(Math.min(1,t)*rows.length);
    lbl(ctx,'밑 a = '+S.a+' 인 지수 사다리',24,34,'#1d4ed8',18);
    lbl(ctx,'한 칸 내려갈 때마다 '+S.a+'로 나눈다',24,58,'#52627a',15);
    var Y0=88, RH=Math.min(30,290/rows.length);
    for(i=0;i<rows.length;i++){
      var on=(i<shown);
      var y=Y0+i*RH;
      var e=rows[i][0], v2=rows[i][1];
      ctx.fillStyle=on?((e===0)?'#fde68a':((e<0)?'#fecaca':'#dbeafe')):'#f5f7fa';
      ctx.fillRect(60,y,300,RH-3);
      ctx.strokeStyle=on?'#94a3b8':'#e8edf3';ctx.lineWidth=1.2;
      ctx.strokeRect(60,y,300,RH-3);
      if(on){
        ctx.fillStyle='#1f2937';ctx.font='bold 15px sans-serif';ctx.textAlign='left';
        ctx.fillText(S.a+'^'+e,76,y+RH/2+3);
        ctx.textAlign='right';
        ctx.fillText((Math.abs(v2)>=1)?v2:r4(v2),348,y+RH/2+3);
      }
      if(on&&i>0){
        ctx.fillStyle='#b45309';ctx.font='12px sans-serif';ctx.textAlign='left';
        ctx.fillText('÷'+S.a,368,y+RH/2+3);
      }
    }
    ctx.textAlign='left';
    box(ctx,20,392,400,26);
    lbl(ctx,(t===null)?'0과 음수 지수는 어떻게 정해질까?':(S.a+'^'+S.n+' × '+S.a+'^(−'+S.n+') = '+r3(c.prod)),
        30,410,'#1f2937',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,n:S.n,pn:c.pn,neg:r4(c.neg),prod:r3(c.prod),
            recip:r4(1/c.pn),
            negOk:(Math.abs(c.neg-1/c.pn)<1e-12),
            prodOne:(Math.abs(c.prod-1)<1e-12),
            zeroOne:true};
  },
  headA:['번호','a','n','a^n','a^(−n)','1 / a^n','같은가?','두 값의 곱','a^0'],
  rowA:function(r,i){
    return [i+1,r.a,r.n,'<b>'+r.pn+'</b>',r.neg,r.recip,
            '<span class="'+(r.negOk?'ok':'no')+'">'+(r.negOk?'○':'×')+'</span>',
            r.prod,'1'];
  },
  analyze:function(rec){
    var rows=[],ok=0,one=0,as={},an=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.negOk) ok++;
      if(r.prodOne) one++;
      if(!as[r.a]){ as[r.a]=true; an++; }
      rows.push([r.a+'^'+r.n, '<b>'+r.pn+'</b>', r.neg, r.recip,
                 '<span class="'+(r.negOk?'ok':'no')+'">'+(r.negOk?'○':'×')+'</span>',
                 r.prod,
                 '<span class="'+(r.prodOne?'ok':'no')+'">'+(r.prodOne?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'a^(−n) = 1 / a^n',big:ok+' / '+rec.length,p:'음수 지수의 정의가 사다리와 맞는지 확인한 결과.'},
      {t:'a^n × a^(−n) = 1',big:one+' / '+rec.length,p:'지수법칙 a^n · a^m = a^(n+m) 에서 m = −n 인 경우.'},
      {t:'시험한 밑',big:an+'가지',p:'밑을 바꿔도 규칙은 같았다.'}
    ];
    var concl;
    if(ok===rec.length&&one===rec.length){
      concl='<b>정리</b> — 지수를 1씩 내릴 때마다 값이 a로 나누어졌고, 그 흐름을 그대로 이으면 '
           +'<b>a⁰ = 1</b>, <b>a^(−n) = 1/a^n</b> 이 자연스럽게 나왔다. '
           +'0제곱과 음수 제곱은 “억지로 정한 약속”이 아니라 <b>지수법칙이 계속 성립하도록 이어 붙인 결과</b>다. '
           +'실제로 a^n × a^(−n) 은 언제나 1이었고, 이는 a^(n + (−n)) = a⁰ = 1 과 맞아떨어진다.';
    } else {
      concl='<b>확인 필요</b> — 정의와 어긋난 기록이 있다.';
    }
    return {head:['식','a^n','a^(−n)','1/a^n','같은가?','두 값의 곱','1인가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 로그의 성질
# ============================================================
LAB_LOG = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'로그 계산판',
  action:'세 가지 값 구하기',
  hint0:'밑과 두 진수를 정하고, 곱과 합에 로그를 씌워 보자.',
  sliders:[
    {id:'a',label:'밑 a',min:2,max:6,value:2,color:'#2563eb',unit:''},
    {id:'x',label:'진수 x',min:1,max:24,value:4,color:'#16a34a',unit:''},
    {id:'y',label:'진수 y',min:1,max:24,value:8,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    function L(v){ return Math.log(v)/Math.log(S.a); }
    return {lx:L(S.x),ly:L(S.y),
            lxy:L(S.x*S.y),sum:L(S.x)+L(S.y),
            lplus:L(S.x+S.y),
            ldiv:L(S.x/S.y),diff:L(S.x)-L(S.y)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'log(xy)',v:ran?r4(c.lxy):'구해 보자'},
            {k:'log x + log y',v:ran?r4(c.sum):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'log(xy) = '+r4(c.lxy)+', log x + log y = '+r4(c.sum)+', log(x+y) = '+r4(c.lplus)+'. 어느 것이 같은지 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var p1=(t===null)?0:Math.min(1,t/0.4);
    var p2=(t===null)?0:Math.max(0,Math.min(1,(t-0.4)/0.3));
    var p3=(t===null)?0:Math.max(0,(t-0.7)/0.3);
    lbl(ctx,'밑 '+S.a+',  x = '+S.x+',  y = '+S.y,24,38,'#1d4ed8',18);
    var U2=Math.min(58, 300/Math.max(c.lxy,c.lplus,1));
    var X0=60;
    function bar(y,len,col,label,alpha){
      ctx.globalAlpha=alpha;
      ctx.fillStyle=col;ctx.fillRect(X0,y,Math.max(0,len)*U2,26);
      ctx.strokeStyle='#334155';ctx.lineWidth=2;ctx.strokeRect(X0,y,Math.max(0,len)*U2,26);
      lbl(ctx,label,X0+Math.max(0,len)*U2+8,y+19,'#334155',14);
      ctx.globalAlpha=1;
    }
    bar(76,c.lx,'#bfdbfe','log x = '+r3(c.lx),1);
    bar(112,c.ly,'#fed7aa','log y = '+r3(c.ly),1);
    if(p1>0){
      ctx.globalAlpha=p1;
      ctx.fillStyle='#bfdbfe';ctx.fillRect(X0,160,c.lx*U2,26);
      ctx.fillStyle='#fed7aa';ctx.fillRect(X0+c.lx*U2,160,c.ly*U2,26);
      ctx.strokeStyle='#334155';ctx.lineWidth=2;ctx.strokeRect(X0,160,(c.lx+c.ly)*U2,26);
      lbl(ctx,'log x + log y = '+r3(c.sum),X0+(c.lx+c.ly)*U2+8,179,'#334155',14);
      ctx.globalAlpha=1;
    }
    if(p2>0) bar(200,c.lxy,'#bbf7d0','log(xy) = '+r3(c.lxy),p2);
    if(p3>0) bar(240,c.lplus,'#fecaca','log(x+y) = '+r3(c.lplus),p3);
    box(ctx,20,282,400,102);
    lbl(ctx,(t===null)?'어느 것이 같을까?':('log(xy) = '+r4(c.lxy)+'      log x + log y = '+r4(c.sum)),38,314,'#15803d',17);
    lbl(ctx,(t===null)?'':('log(x+y) = '+r4(c.lplus)),38,344,'#b91c1c',17);
    lbl(ctx,(t===null)?'':('log(x/y) = '+r4(c.ldiv)+'      log x − log y = '+r4(c.diff)),38,374,'#52627a',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,x:S.x,y:S.y,
            lxy:r4(c.lxy),sum:r4(c.sum),lplus:r4(c.lplus),
            ldiv:r4(c.ldiv),diff:r4(c.diff),
            mulOk:(Math.abs(c.lxy-c.sum)<1e-9),
            addOk:(Math.abs(c.lplus-c.sum)<1e-9),
            divOk:(Math.abs(c.ldiv-c.diff)<1e-9)};
  },
  headA:['번호','밑','x, y','log(xy)','log x + log y','같나?','log(x+y)','같나?','log(x/y)','log x − log y','같나?'],
  rowA:function(r,i){
    return [i+1,r.a,r.x+', '+r.y,'<b>'+r.lxy+'</b>',r.sum,
            '<span class="'+(r.mulOk?'ok':'no')+'">'+(r.mulOk?'○':'×')+'</span>',
            r.lplus,
            '<span class="'+(r.addOk?'ok':'no')+'">'+(r.addOk?'○':'×')+'</span>',
            r.ldiv,r.diff,
            '<span class="'+(r.divOk?'ok':'no')+'">'+(r.divOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],mul=0,add=0,div=0,one=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.mulOk) mul++;
      if(r.addOk){ add++; if(r.x===1||r.y===1) one++; }
      if(r.divOk) div++;
      rows.push([r.a, r.x+', '+r.y, '<b>'+r.lxy+'</b>', r.sum,
                 '<span class="'+(r.mulOk?'ok':'no')+'">'+(r.mulOk?'○':'×')+'</span>',
                 r.lplus,
                 '<span class="'+(r.addOk?'ok':'no')+'">'+(r.addOk?'○':'×')+'</span>',
                 '<span class="'+(r.divOk?'ok':'no')+'">'+(r.divOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'log(xy) = log x + log y',big:mul+' / '+rec.length,p:'곱을 로그로 바꾼 결과.'},
      {t:'log(x+y) = log x + log y',big:add+' / '+rec.length,
       p:add?('그중 x나 y가 1이었던 것 '+one+'개.'):'덧셈은 로그로 나눠지지 않는다.'},
      {t:'log(x/y) = log x − log y',big:div+' / '+rec.length,p:'나눗셈은 뺄셈이 되는지 확인한 결과.'}
    ];
    var concl;
    if(mul===rec.length&&div===rec.length&&add===0){
      concl='<b>정리</b> — 로그는 <b>곱셈을 덧셈으로, 나눗셈을 뺄셈으로</b> 바꿔 주었다. 예외가 없었다. '
           +'하지만 <b>log(x + y)는 log x + log y 와 한 번도 같지 않았다.</b> '
           +'지수법칙 a^m · a^n = a^(m+n)을 뒤집은 것이 로그의 성질이라서, 원래 자리에 곱셈이 있어야 한다. '
           +'덧셈에는 대응하는 지수법칙이 없다.';
    } else if(mul===rec.length&&div===rec.length){
      concl='<b>정리</b> — 곱은 합으로, 나눗셈은 차로 바뀌었다. log(x+y)가 맞은 경우는 진수가 1인 특수한 경우다.';
    } else {
      concl='<b>확인 필요</b> — 로그 성질이 어긋난 기록이 있다.';
    }
    return {head:['밑','x, y','log(xy)','log x+log y','같나?','log(x+y)','같나?','나눗셈도?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 지수함수와 로그함수
# ============================================================
LAB_EXPLOG = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'지수·로그 그래프판',
  action:'두 그래프 그리기',
  hint0:'밑과 확인할 값을 정해 보자.',
  sliders:[
    {id:'a',label:'밑 a',min:2,max:5,value:2,color:'#2563eb',unit:''},
    {id:'x0',label:'확인할 값 (÷2)',min:1,max:14,value:8,color:'#dc2626',
     fmt:function(v){return (v/2).toFixed(1);}}
  ],
  calc:function(S){
    var x=S.x0/2;
    var ax=Math.pow(S.a,x);
    var lx=Math.log(x)/Math.log(S.a);
    return {x:x,ax:ax,lx:lx,
            back1:Math.pow(S.a,lx),
            back2:Math.log(ax)/Math.log(S.a)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'a^x',v:ran?r3(c.ax):'그려 보자'},
            {k:'logₐx',v:ran?r3(c.lx):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'a^x = '+r3(c.ax)+', logₐx = '+r3(c.lx)+'.  a^(logₐx) = '+r3(c.back1)+', logₐ(a^x) = '+r3(c.back2)+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,8,7);
    ctx.strokeStyle='#c4b5fd';ctx.lineWidth=2;ctx.setLineDash([5,5]);
    ctx.beginPath();ctx.moveTo(CX-7*U,CY+7*U);ctx.lineTo(CX+7*U,CY-7*U);ctx.stroke();ctx.setLineDash([]);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    var st=false;
    for(i=-80;i<=80;i++){
      var x=i/10, y=Math.pow(S.a,x);
      if(y<-7||y>7){ st=false; continue; }
      if(!st){ ctx.moveTo(CX+x*U,CY-y*U); st=true; } else ctx.lineTo(CX+x*U,CY-y*U);
    }
    ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      ctx.strokeStyle='#dc2626';ctx.lineWidth=3;ctx.beginPath();
      st=false;
      for(i=1;i<=80;i++){
        var x2=i/10, y2=Math.log(x2)/Math.log(S.a);
        if(y2<-7||y2>7){ st=false; continue; }
        if(!st){ ctx.moveTo(CX+x2*U,CY-y2*U); st=true; } else ctx.lineTo(CX+x2*U,CY-y2*U);
      }
      ctx.stroke();
    }
    if(grow>=1){
      if(Math.abs(c.ax)<=7){
        ctx.beginPath();ctx.arc(CX+c.x*U,CY-c.ax*U,7,0,Math.PI*2);
        ctx.fillStyle='#2563eb';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      }
      if(Math.abs(c.lx)<=7){
        ctx.beginPath();ctx.arc(CX+c.x*U,CY-c.lx*U,7,0,Math.PI*2);
        ctx.fillStyle='#dc2626';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      }
    }
    lbl(ctx,'y = '+S.a+'^x      y = log_'+S.a+' x      점선 y = x',24,32,'#334155',15);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'두 그래프는 어떤 관계일까?':('a^(logₐx) = '+r3(c.back1)+'      logₐ(a^x) = '+r3(c.back2)),
        38,376,'#1f2937',18);
    lbl(ctx,'확인한 값 x = '+c.x,38,406,'#52627a',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,x:c.x,ax:r3(c.ax),lx:r3(c.lx),
            back1:r3(c.back1),back2:r3(c.back2),
            ok1:(Math.abs(c.back1-c.x)<1e-9),
            ok2:(Math.abs(c.back2-c.x)<1e-9),
            same:(Math.abs(c.ax-c.lx)<1e-9)};
  },
  headA:['번호','밑','x','a^x','logₐx','a^(logₐx)','x로 돌아옴?','logₐ(a^x)','x로 돌아옴?'],
  rowA:function(r,i){
    return [i+1,r.a,r.x,r.ax,r.lx,'<b>'+r.back1+'</b>',
            '<span class="'+(r.ok1?'ok':'no')+'">'+(r.ok1?'○':'×')+'</span>',
            r.back2,
            '<span class="'+(r.ok2?'ok':'no')+'">'+(r.ok2?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],o1=0,o2=0,same=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.ok1) o1++;
      if(r.ok2) o2++;
      if(r.same) same++;
      rows.push([r.a, r.x, r.ax, r.lx, '<b>'+r.back1+'</b>',
                 '<span class="'+(r.ok1?'ok':'no')+'">'+(r.ok1?'○':'×')+'</span>',
                 r.back2,
                 '<span class="'+(r.ok2?'ok':'no')+'">'+(r.ok2?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'a^(logₐx) = x',big:o1+' / '+rec.length,p:'로그를 씌운 뒤 다시 지수로 올리면 원래 값으로 돌아오는지 확인했다.'},
      {t:'logₐ(a^x) = x',big:o2+' / '+rec.length,p:'반대 순서로도 확인한 결과.'},
      {t:'a^x = logₐx 였던 횟수',big:same+' / '+rec.length,p:'두 함수는 서로 다른 함수다.'}
    ];
    var concl;
    if(o1===rec.length&&o2===rec.length){
      concl='<b>정리</b> — 지수함수와 로그함수는 <b>서로를 되돌리는 함수</b>였다. 어느 순서로 통과시켜도 x로 돌아왔다. '
           +'그래서 두 그래프는 <b>y = x 에 대해 대칭</b>이다. logₐx 는 “a를 몇 제곱해야 x가 되는가”를 답하는 값이고, '
           +'지수함수가 하는 일을 거꾸로 되짚는 것이다. 지수함수가 일대일이라 역함수가 존재한다.';
    } else {
      concl='<b>확인 필요</b> — 되돌린 값이 x와 다른 기록이 있다.';
    }
    return {head:['밑','x','a^x','logₐx','a^(logₐx)','x로?','logₐ(a^x)','x로?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 호도법과 부채꼴
# ============================================================
LAB_RAD = BASE + r"""
var OX=170, OY=210;
var LAB = {
  cw:440, ch:430, cvTitle:'호도법 판',
  action:'호를 펴서 재기',
  hint0:'반지름과 중심각을 정하고, 호의 길이를 두 방법으로 구해 보자.',
  sliders:[
    {id:'r',label:'반지름',min:40,max:130,value:100,color:'#2563eb',unit:''},
    {id:'deg',label:'중심각',min:10,max:350,value:60,color:'#f59e0b',unit:'°'}
  ],
  calc:function(S){
    var rad=S.deg*Math.PI/180;
    var arcDeg=2*Math.PI*S.r*S.deg/360;
    var arcRad=S.r*rad;
    var areaDeg=Math.PI*S.r*S.r*S.deg/360;
    var areaRad=0.5*S.r*S.r*rad;
    return {rad:rad,arcDeg:arcDeg,arcRad:arcRad,areaDeg:areaDeg,areaRad:areaRad,
            ratio:arcRad/S.r};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'라디안',v:r4(c.rad)},
            {k:'호의 길이',v:ran?r2(c.arcRad/20)+'cm':'재 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '호의 길이는 rθ = '+r2(c.arcRad/20)+'cm, 2πr×θ/360 = '+r2(c.arcDeg/20)+'cm.  호 ÷ 반지름 = '+r4(c.ratio)+'이다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var grow=(t===null)?0:Math.min(1,t);
    ctx.beginPath();ctx.arc(OX,OY,S.r,0,Math.PI*2);
    ctx.strokeStyle='#e2e8f0';ctx.lineWidth=2;ctx.stroke();
    ctx.beginPath();ctx.moveTo(OX,OY);
    ctx.arc(OX,OY,S.r,0,c.rad);ctx.closePath();
    ctx.fillStyle='rgba(37,99,235,0.16)';ctx.fill();
    ctx.strokeStyle='#2563eb';ctx.lineWidth=2;ctx.stroke();
    ctx.beginPath();ctx.arc(OX,OY,S.r,0,c.rad);
    ctx.strokeStyle='#dc2626';ctx.lineWidth=5;ctx.stroke();
    ctx.strokeStyle='#16a34a';ctx.lineWidth=4;
    ctx.beginPath();ctx.moveTo(OX,OY);ctx.lineTo(OX+S.r,OY);ctx.stroke();
    lbl(ctx,'r',OX+S.r/2,OY-8,'#15803d',15,'center');
    if(grow>0){
      var Y2=380;
      ctx.strokeStyle='#dc2626';ctx.lineWidth=5;
      ctx.beginPath();ctx.moveTo(40,Y2);ctx.lineTo(40+c.arcRad*grow,Y2);ctx.stroke();
      ctx.strokeStyle='#16a34a';ctx.lineWidth=4;
      var nr=Math.floor(c.ratio);
      for(i=0;i<nr;i++){
        ctx.beginPath();ctx.moveTo(40+i*S.r,Y2+12);ctx.lineTo(40+(i+1)*S.r-3,Y2+12);ctx.stroke();
      }
      if(grow>=1) lbl(ctx,'펼친 호 = 반지름의 '+r3(c.ratio)+'배',40,Y2-12,'#b91c1c',15);
    }
    lbl(ctx,'중심각 '+S.deg+'° = '+r4(c.rad)+' 라디안',24,32,'#1d4ed8',17);
    box(ctx,20,288,400,74);
    lbl(ctx,'r θ = '+r2(c.arcRad/20)+'cm      2πr × θ/360 = '+r2(c.arcDeg/20)+'cm',38,318,'#1f2937',17);
    lbl(ctx,(t===null)?'두 방법의 결과는 같을까?':('½r²θ = '+r2(c.areaRad/400)+'cm²      πr²×θ/360 = '+r2(c.areaDeg/400)+'cm²'),
        38,348,'#15803d',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {r:r2(S.r/20),deg:S.deg,rad:r4(c.rad),
            arcRad:r3(c.arcRad/20),arcDeg:r3(c.arcDeg/20),
            areaRad:r3(c.areaRad/400),areaDeg:r3(c.areaDeg/400),
            arcOk:(Math.abs(c.arcRad-c.arcDeg)<1e-9),
            areaOk:(Math.abs(c.areaRad-c.areaDeg)<1e-9),
            ratio:r4(c.ratio),
            ratioOk:(Math.abs(c.ratio-c.rad)<1e-9)};
  },
  headA:['번호','반지름','중심각','라디안','rθ','2πr·θ/360','같나?','호÷반지름','라디안과 같나?'],
  rowA:function(r,i){
    return [i+1,r.r,r.deg+'°',r.rad,'<b>'+r.arcRad+'</b>',r.arcDeg,
            '<span class="'+(r.arcOk?'ok':'no')+'">'+(r.arcOk?'○':'×')+'</span>',
            r.ratio,
            '<span class="'+(r.ratioOk?'ok':'no')+'">'+(r.ratioOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],arc=0,area=0,ratio=0,rs={},rn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.arcOk) arc++;
      if(r.areaOk) area++;
      if(r.ratioOk) ratio++;
      if(!rs[r.r]){ rs[r.r]=true; rn++; }
      rows.push([r.r, r.deg+'°', r.rad, r.arcRad+' / '+r.arcDeg,
                 '<span class="'+(r.arcOk?'ok':'no')+'">'+(r.arcOk?'○':'×')+'</span>',
                 r.ratio,
                 '<span class="'+(r.ratioOk?'ok':'no')+'">'+(r.ratioOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'rθ = 2πr·θ/360',big:arc+' / '+rec.length,p:'호의 길이를 두 방법으로 구해 비교한 결과.'},
      {t:'½r²θ = πr²·θ/360',big:area+' / '+rec.length,p:'부채꼴 넓이도 같은지 확인한 결과.'},
      {t:'호 ÷ 반지름 = 라디안 값',big:ratio+' / '+rec.length,
       p:'시험한 반지름 '+rn+'가지. 반지름이 달라도 비는 각에만 달렸다.'}
    ];
    var concl;
    if(arc===rec.length&&ratio===rec.length){
      concl='<b>정리</b> — 호를 펴서 반지름으로 나눈 값은 <b>반지름과 상관없이 각에만 달려</b> 있었고, 그 값이 곧 라디안이다. '
           +'라디안을 쓰면 호의 길이가 <b>rθ</b>, 부채꼴 넓이가 <b>½r²θ</b> 로 간단해진다. '
           +'360이나 π/180 같은 변환 상수가 사라지는 이유는, 라디안이 “호가 반지름의 몇 배인가”로 각을 재기 때문이다.';
    } else {
      concl='<b>확인 필요</b> — 두 계산이 어긋난 기록이 있다.';
    }
    return {head:['반지름','중심각','라디안','rθ / 도수법','같나?','호÷반지름','라디안?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 삼각함수의 그래프
# ============================================================
LAB_TRIGG = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'사인 그래프판',
  action:'그래프 그리고 재기',
  hint0:'y = a sin(bx) 의 a와 b를 정해 보자.',
  sliders:[
    {id:'a',label:'a',min:-4,max:4,value:2,color:'#2563eb',unit:''},
    {id:'b',label:'b',min:1,max:4,value:2,color:'#dc2626',unit:''}
  ],
  f:function(S,x){ return S.a*Math.sin(S.b*x); },
  calc:function(S){
    var mx=-1e9,mn=1e9,i;
    for(i=0;i<=6280;i++){
      var x=i/1000;
      var y=this.f(S,x);
      if(y>mx) mx=y;
      if(y<mn) mn=y;
    }
    var period=2*Math.PI/S.b;
    var found=null;
    for(i=50;i<=6400;i++){
      var p=i/1000;
      var ok=true;
      for(var j=0;j<12;j++){
        var xx=j*0.4;
        if(Math.abs(this.f(S,xx+p)-this.f(S,xx))>0.005){ ok=false; break; }
      }
      if(ok){ found=p; break; }
    }
    return {mx:mx,mn:mn,period:period,found:found,amp:(mx-mn)/2};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'최댓값 / 최솟값',v:ran?(r2(c.mx)+' / '+r2(c.mn)):'재 보자'},
            {k:'되풀이되는 길이',v:ran?((c.found===null)?'-':r3(c.found)):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '최댓값 '+r2(c.mx)+', 최솟값 '+r2(c.mn)+', 되풀이되는 길이 '+((c.found===null)?'-':r3(c.found))+'.  2π/b = '+r3(c.period)+'와 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var GX=40, GY=180, XU=44, YU=32;
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=0;i<=8;i++){ ctx.beginPath();ctx.moveTo(GX+i*XU,GY-4.5*YU);ctx.lineTo(GX+i*XU,GY+4.5*YU);ctx.stroke(); }
    for(i=-4;i<=4;i++){ ctx.beginPath();ctx.moveTo(GX,GY+i*YU);ctx.lineTo(GX+8*XU,GY+i*YU);ctx.stroke(); }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+8*XU,GY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(GX,GY-4.5*YU);ctx.lineTo(GX,GY+4.5*YU);ctx.stroke();
    ctx.fillStyle='#94a3b8';ctx.font='12px sans-serif';ctx.textAlign='center';
    for(i=1;i<=2;i++){ ctx.fillText((i===1)?'π':'2π',GX+i*Math.PI*XU,GY+18); }
    ctx.textAlign='left';
    var grow=(t===null)?0:Math.min(1,t);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    for(i=0;i<=Math.floor(grow*800);i++){
      var x=i/100;
      if(x>8*XU/XU) break;
      var y=this.f(S,x);
      var Px=GX+x*XU, Py=GY-y*YU;
      if(i===0) ctx.moveTo(Px,Py); else ctx.lineTo(Px,Py);
    }
    if(grow>0) ctx.stroke();
    if(grow>=1){
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=1.8;ctx.setLineDash([4,4]);
      ctx.beginPath();ctx.moveTo(GX,GY-c.mx*YU);ctx.lineTo(GX+8*XU,GY-c.mx*YU);ctx.stroke();
      ctx.beginPath();ctx.moveTo(GX,GY-c.mn*YU);ctx.lineTo(GX+8*XU,GY-c.mn*YU);ctx.stroke();
      ctx.setLineDash([]);
      if(c.found!==null&&c.found*XU<8*XU){
        ctx.strokeStyle='#dc2626';ctx.lineWidth=3;
        ctx.beginPath();ctx.moveTo(GX,GY+4.2*YU);ctx.lineTo(GX+c.found*XU,GY+4.2*YU);ctx.stroke();
        lbl(ctx,'되풀이 '+r3(c.found),GX+c.found*XU+6,GY+4.6*YU,'#b91c1c',13);
      }
    }
    lbl(ctx,'y = '+S.a+' sin('+S.b+'x)',24,32,'#1d4ed8',18);
    box(ctx,20,314,400,70);
    lbl(ctx,(t===null)?'최댓값과 주기는?':('최댓값 '+r2(c.mx)+'   최솟값 '+r2(c.mn)+'   |a| = '+Math.abs(S.a)),38,344,'#1f2937',17);
    lbl(ctx,(t===null)?'':('되풀이 길이 '+((c.found===null)?'-':r3(c.found))+'      2π/b = '+r3(c.period)),38,374,'#15803d',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,mx:r2(c.mx),mn:r2(c.mn),amp:r2(c.amp),
            found:(c.found===null)?'-':r3(c.found),period:r3(c.period),
            ampOk:(Math.abs(c.amp-Math.abs(S.a))<0.01),
            perOk:(c.found!==null&&Math.abs(c.found-c.period)<0.01)};
  },
  headA:['번호','a, b','최댓값','최솟값','(최대−최소)/2','|a|','같나?','되풀이 길이','2π/b','같나?'],
  rowA:function(r,i){
    return [i+1,r.a+', '+r.b,r.mx,r.mn,r.amp,Math.abs(r.a),
            '<span class="'+(r.ampOk?'ok':'no')+'">'+(r.ampOk?'○':'×')+'</span>',
            '<b>'+r.found+'</b>',r.period,
            '<span class="'+(r.perOk?'ok':'no')+'">'+(r.perOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],amp=0,per=0,bs={},bn=0,mono=true,arr=[];
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.ampOk) amp++;
      if(r.perOk) per++;
      if(!bs[r.b]){ bs[r.b]=r.period; bn++; arr.push([r.b,parseFloat(r.period)]); }
      rows.push([r.a+', '+r.b, r.mx+' / '+r.mn, r.amp, Math.abs(r.a),
                 '<span class="'+(r.ampOk?'ok':'no')+'">'+(r.ampOk?'○':'×')+'</span>',
                 '<b>'+r.found+'</b>', r.period,
                 '<span class="'+(r.perOk?'ok':'no')+'">'+(r.perOk?'○':'×')+'</span>']);
    }
    arr.sort(function(x,y){return x[0]-y[0];});
    for(i=1;i<arr.length;i++){ if(arr[i][1]>=arr[i-1][1]) mono=false; }
    var stats=[
      {t:'(최대−최소)/2 = |a|',big:amp+' / '+rec.length,p:'그래프에서 직접 잰 값과 비교한 결과.'},
      {t:'되풀이 길이 = 2π/b',big:per+' / '+rec.length,p:'수치로 찾은 주기와 공식을 비교한 결과.'},
      {t:'b가 커질수록 주기는',big:(arr.length<2)?'비교 없음':(mono?'짧아짐':'일정하지 않음'),
       p:'시험한 b '+bn+'가지.'}
    ];
    var concl;
    if(bn<2){
      concl='<b>더 해 보자</b> — b를 바꿔 여러 값으로 기록해야 주기와의 관계가 보인다.';
    } else if(amp===rec.length&&per===rec.length&&mono){
      concl='<b>정리</b> — a는 그래프의 <b>세로 크기(진폭)</b>를 정했고, b는 <b>가로로 얼마나 촘촘한지</b>를 정했다. '
           +'주기는 2π/b 이므로 <b>b가 커질수록 주기는 짧아졌다.</b> b를 “주기”라고 착각하기 쉽지만 반대다. '
           +'a가 음수면 위아래가 뒤집히지만 최댓값·최솟값의 크기는 |a| 그대로였다.';
    } else {
      concl='<b>정리</b> — 진폭은 |a|, 주기는 2π/b였다. b를 더 여러 값으로 기록해 관계를 확인해 보자.';
    }
    return {head:['a, b','최대/최소','진폭','|a|','같나?','되풀이 길이','2π/b','같나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("hd_exponent_extension_lab_Algebra_ExpLog_Ep02.html",
     "지수 실험실 — a⁰ = 1 은 왜 그럴까?",
     "지수 실험실 — a⁰ = 1 은 왜 그럴까?",
     "지수를 한 칸씩 내리며 값의 변화를 따라가, 0제곱과 음수 제곱의 정의가 어디서 오는지 확인한다.",
     LAB_EXP),
    ("hd_log_property_lab_Algebra_ExpLog_Ep05.html",
     "로그 실험실 — log(x+y)는 log x + log y 일까?",
     "로그 실험실 — log(x+y)는 log x + log y 일까?",
     "곱·합·나눗셈에 로그를 씌워 값을 길이로 비교하고, 어떤 것이 성립하는지 기록한다.",
     LAB_LOG),
    ("hd_exp_log_inverse_lab_Algebra_ExpLogFunc_Ep05.html",
     "지수·로그 실험실 — 두 그래프는 어떤 관계일까?",
     "지수·로그 실험실 — 두 그래프는 어떤 관계일까?",
     "지수함수와 로그함수를 한 좌표평면에 그리고, 서로를 되돌리는지 값으로 확인한다.",
     LAB_EXPLOG),
    ("hd_radian_lab_Algebra_Trig_Ep02.html",
     "호도법 실험실 — 라디안은 무엇을 재는 걸까?",
     "호도법 실험실 — 라디안은 무엇을 재는 걸까?",
     "호를 펴서 반지름의 몇 배인지 재고, 도수법 계산과 rθ를 비교한다.",
     LAB_RAD),
    ("hd_sine_graph_lab_Algebra_Trig_Ep06.html",
     "삼각함수 실험실 — b가 크면 주기도 클까?",
     "삼각함수 실험실 — b가 크면 주기도 클까?",
     "y = a sin(bx)의 최댓값과 되풀이되는 길이를 그래프에서 직접 재어 공식과 대조한다.",
     LAB_TRIGG),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c25_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
