# -*- coding: utf-8 -*-
"""중1 '수와 연산' 실험 5종"""
import os, re

OUT = "/mnt/user-data/outputs"
src = open("/home/claude/gen_math_labs.py", encoding="utf-8").read()
TPL = re.search(r'TPL = r"""(.*?)"""\n', src, re.S).group(1)

BASE = r"""
function lbl(ctx,t,x,y,c,sz,al){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
function box(ctx,x,y,w,h){ctx.fillStyle='#f1f6fd';ctx.fillRect(x,y,w,h);ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(x,y,w,h);}
function r1(v){return Math.round(v*10)/10;}
function sgn(v){return (v>0)?'+':(v<0?'−':'');}
function pn(v){return (v<0)?('('+v+')'):(''+v);}
"""

# ============================================================
# 1. 소인수분해와 약수의 개수
# ============================================================
LAB_FACTOR = BASE + r"""
function factorize(n){
  var f=[],p=2,m=n;
  while(p*p<=m){
    if(m%p===0){ var e=0; while(m%p===0){ m/=p; e++; } f.push([p,e]); }
    p++;
  }
  if(m>1) f.push([m,1]);
  return f;
}
function fstr(f){
  var s=[],i;
  for(i=0;i<f.length;i++){ s.push(f[i][0]+(f[i][1]>1?('^'+f[i][1]):'')); }
  return s.join(' × ');
}
function countDiv(n){ var c=0,i; for(i=1;i<=n;i++){ if(n%i===0) c++; } return c; }
function divisors(n){ var a=[],i; for(i=1;i<=n;i++){ if(n%i===0) a.push(i); } return a; }

var LAB = {
  cw:440, ch:420, cvTitle:'소인수분해판',
  action:'소수로 계속 나누기',
  hint0:'수를 정하고 더 나눌 수 없을 때까지 소수로 나누어 보자.',
  sliders:[
    {id:'n',label:'수',min:2,max:200,value:72,color:'#2563eb',unit:''}
  ],
  readout:function(S,ran){
    var f=factorize(S.n);
    return [{k:'소인수분해',v:ran?fstr(f):'나누어 보자'},
            {k:'약수의 개수',v:ran?countDiv(S.n)+'개':'-'}];
  },
  doneMsg:function(S){
    var f=factorize(S.n), pr=1,i;
    for(i=0;i<f.length;i++){ pr*=(f[i][1]+1); }
    return S.n+' = '+fstr(f)+'. (지수+1)을 모두 곱하면 '+pr+', 실제 약수는 '+countDiv(S.n)+'개다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var f=factorize(S.n), i;
    var steps=[],m=S.n;
    for(i=0;i<f.length;i++){ var e; for(e=0;e<f[i][1];e++){ steps.push(f[i][0]); } }
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*steps.length);
    lbl(ctx,S.n+'을 소수로 계속 나누기',24,38,'#1d4ed8',19);
    var y=76, cur=S.n;
    for(i=0;i<steps.length;i++){
      if(i>=shown) break;
      lbl(ctx,steps[i]+' )',48,y,'#dc2626',20,'right');
      lbl(ctx,''+cur,58,y,'#1f2937',20);
      ctx.strokeStyle='#94a3b8';ctx.lineWidth=1.6;
      ctx.beginPath();ctx.moveTo(52,y-18);ctx.lineTo(130,y-18);ctx.stroke();
      cur=cur/steps[i];
      y+=30;
    }
    if(shown>=steps.length && steps.length>0){
      lbl(ctx,''+cur,58,y,'#15803d',20);
      lbl(ctx,'← 더 나눌 수 없다',96,y,'#15803d',16);
    }
    if(shown>0){
      lbl(ctx,S.n+' = '+fstr(f),210,90,'#1d4ed8',20);
      var pr=1;
      for(i=0;i<f.length;i++){ pr*=(f[i][1]+1); }
      if(shown>=steps.length){
        var t2=[];
        for(i=0;i<f.length;i++){ t2.push('('+f[i][1]+'+1)'); }
        lbl(ctx,'(지수+1)의 곱',210,128,'#52627a',16);
        lbl(ctx,t2.join(' × ')+' = '+pr,210,154,'#b45309',19);
      }
    }
    var dv=divisors(S.n);
    box(ctx,20,290,400,116);
    lbl(ctx,'약수를 하나씩 세어 보면',38,318,'#52627a',17);
    var line=dv.join(', ');
    if(line.length>44) line=line.substring(0,42)+'...';
    lbl(ctx,line,38,346,'#334155',16);
    lbl(ctx,(t===null)?'약수는 몇 개일까?':('약수의 개수 : '+dv.length+'개'),38,380,'#1f2937',20);
  },
  record:function(S){
    var f=factorize(S.n), pr=1,i,ex=[];
    for(i=0;i<f.length;i++){ pr*=(f[i][1]+1); ex.push(f[i][1]); }
    return {n:S.n,f:fstr(f),ex:ex.join(', '),pr:pr,cnt:countDiv(S.n),
            prime:(f.length===1&&f[0][1]===1)};
  },
  headA:['번호','수','소인수분해','지수','(지수+1)의 곱','실제 약수 개수','같은가?','소수?'],
  rowA:function(r,i){
    var ok=(r.pr===r.cnt);
    return [i+1,r.n,r.f,r.ex,r.pr,'<b>'+r.cnt+'</b>',
            '<span class="'+(ok?'ok':'no')+'">'+(ok?'○':'×')+'</span>',
            r.prime?'○':'×'];
  },
  analyze:function(rec){
    var rows=[],ok=0,primes=0,pr2=0,mx=0,mxn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i], a=(r.pr===r.cnt);
      if(a) ok++;
      if(r.prime){ primes++; if(r.cnt===2) pr2++; }
      if(r.cnt>mx){ mx=r.cnt; mxn=r.n; }
      rows.push([r.n, r.f, r.ex, r.pr, '<b>'+r.cnt+'</b>',
                 '<span class="'+(a?'ok':'no')+'">'+(a?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'(지수+1)의 곱 = 약수의 개수',big:ok+' / '+rec.length,
       p:'하나씩 센 약수 개수와 계산이 일치했는지 확인한 결과.'},
      {t:'소수였던 기록',big:primes+'개',
       p:primes?('그중 약수가 2개였던 것 '+pr2+'개.'):'소수도 기록해 보자. 지수가 1뿐이면 (1+1)=2개다.'},
      {t:'약수가 가장 많았던 수',big:mx+'개',p:mxn?(mxn+'의 약수 개수.'):''}
    ];
    var concl;
    if(ok===rec.length){
      concl='<b>정리</b> — 하나씩 세어 구한 약수의 개수는 언제나 <b>(지수+1)을 모두 곱한 값</b>과 같았다. '
           +'약수는 각 소인수를 0개부터 지수 개까지 골라 곱해 만든 것이라서, 고르는 방법의 수가 곧 약수의 개수다. '
           +'그래서 200 정도가 아니라 아주 큰 수도 하나씩 세지 않고 개수를 구할 수 있다.';
    } else {
      concl='<b>확인 필요</b> — 두 값이 다른 기록이 있다. 소인수분해를 다시 확인해 보자.';
    }
    return {head:['수','소인수분해','지수','(지수+1)의 곱','약수 개수','같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 정수의 덧셈
# ============================================================
LAB_INTADD = BASE + r"""
var LAB = {
  cw:440, ch:380, cvTitle:'수직선 덧셈판',
  action:'수직선에서 이동하기',
  hint0:'두 정수를 정하고, 수직선 위에서 이동해 보자.',
  sliders:[
    {id:'a',label:'첫 번째 수',min:-10,max:10,value:-3,color:'#2563eb',unit:''},
    {id:'b',label:'더하는 수',min:-10,max:10,value:7,color:'#f59e0b',unit:''}
  ],
  readout:function(S,ran){
    return [{k:'식',v:pn(S.a)+' + '+pn(S.b)},
            {k:'결과',v:ran?(S.a+S.b):'이동해 보자'}];
  },
  doneMsg:function(S){
    var s=S.a+S.b, abs=Math.abs(S.a)+Math.abs(S.b);
    var sameSign=(S.a>0&&S.b>0)||(S.a<0&&S.b<0);
    return pn(S.a)+' + '+pn(S.b)+' = '+s+'. 절댓값을 더하면 '+abs+'인데 '
      +(sameSign?'부호가 같아 절댓값의 합과 크기가 같다.':'부호가 달라 절댓값의 차가 되었다.')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var X0=30, X1=410, LO=-20, HI=20, i;
    function px(v){ return X0+(X1-X0)*(v-LO)/(HI-LO); }
    var Y=190;
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(X0,Y);ctx.lineTo(X1,Y);ctx.stroke();
    for(i=LO;i<=HI;i++){
      var x=px(i), big=(i%5===0);
      ctx.beginPath();ctx.moveTo(x,Y-(big?9:4));ctx.lineTo(x,Y+(big?9:4));
      ctx.strokeStyle=big?'#475569':'#cbd5e1';ctx.lineWidth=big?2:1;ctx.stroke();
      if(big){ ctx.fillStyle='#475569';ctx.font='12px sans-serif';ctx.textAlign='center';ctx.fillText(i,x,Y+26); }
    }
    ctx.textAlign='left';
    var p1=(t===null)?0:Math.min(1,t/0.45);
    var p2=(t===null)?0:Math.max(0,(t-0.45)/0.55);
    if(p1>0){
      var xa=px(0)+(px(S.a)-px(0))*p1;
      ctx.strokeStyle='#2563eb';ctx.lineWidth=4;
      ctx.beginPath();ctx.moveTo(px(0),Y-16);ctx.lineTo(xa,Y-16);ctx.stroke();
      lbl(ctx,pn(S.a),(px(0)+xa)/2,Y-26,'#1d4ed8',15,'center');
    }
    if(p2>0){
      var xb=px(S.a)+(px(S.a+S.b)-px(S.a))*p2;
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=4;
      ctx.beginPath();ctx.moveTo(px(S.a),Y-40);ctx.lineTo(xb,Y-40);ctx.stroke();
      lbl(ctx,pn(S.b),(px(S.a)+xb)/2,Y-50,'#b45309',15,'center');
      ctx.beginPath();ctx.arc(xb,Y,8,0,Math.PI*2);ctx.fillStyle='#dc2626';ctx.fill();
    }
    lbl(ctx,'0에서 출발해 두 번 이동하기',24,36,'#1d4ed8',19);
    var s=S.a+S.b, abs=Math.abs(S.a)+Math.abs(S.b), dif=Math.abs(Math.abs(S.a)-Math.abs(S.b));
    var sameSign=(S.a>0&&S.b>0)||(S.a<0&&S.b<0);
    box(ctx,20,254,400,112);
    lbl(ctx,pn(S.a)+' + '+pn(S.b)+' = '+((t===null)?'?':s),38,288,'#1f2937',22);
    lbl(ctx,'절댓값의 합 : '+abs+'      절댓값의 차 : '+dif,38,320,'#52627a',18);
    lbl(ctx,(t===null)?'두 수의 부호는 '+(sameSign?'같다':'다르다'):
        (sameSign?'부호가 같다 → 절댓값을 더하고 그 부호':'부호가 다르다 → 절댓값을 빼고 큰 쪽 부호'),
        38,350,'#15803d',17);
  },
  record:function(S){
    var s=S.a+S.b;
    var sameSign=(S.a>0&&S.b>0)||(S.a<0&&S.b<0);
    return {a:S.a,b:S.b,s:s,abs:Math.abs(S.a)+Math.abs(S.b),
            dif:Math.abs(Math.abs(S.a)-Math.abs(S.b)),
            same:sameSign,as:Math.abs(s),
            ruleSum:(Math.abs(s)===Math.abs(S.a)+Math.abs(S.b)),
            hasZero:(S.a===0||S.b===0)};
  },
  headA:['번호','식','결과','절댓값의 합','절댓값의 차','결과의 절댓값','부호'],
  rowA:function(r,i){
    return [i+1,pn(r.a)+' + '+pn(r.b),'<b>'+r.s+'</b>',r.abs,r.dif,r.as,r.same?'같음':'다름'];
  },
  analyze:function(rec){
    var rows=[],alwaysSum=0,sameN=0,sameOk=0,diffN=0,diffOk=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.ruleSum) alwaysSum++;
      if(r.same){ sameN++; if(r.as===r.abs) sameOk++; }
      else if(!r.hasZero){ diffN++; if(r.as===r.dif) diffOk++; }
      rows.push([pn(r.a)+' + '+pn(r.b), '<b>'+r.s+'</b>', r.same?'같음':'다름', r.abs, r.dif, r.as,
                 '<span class="'+((r.as===(r.same?r.abs:r.dif))?'ok':'no')+'">'
                 +((r.as===(r.same?r.abs:r.dif))?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'“절댓값을 더하면 된다”가 맞은 횟수',big:alwaysSum+' / '+rec.length,
       p:'항상 절댓값을 더하는 방법이 통했는지 확인한 결과.'},
      {t:'부호가 같았던 기록',big:sameN+'개',
       p:sameN?('그중 결과의 절댓값 = 절댓값의 합인 것 '+sameOk+'개.'):'부호가 같은 경우도 기록해 보자.'},
      {t:'부호가 달랐던 기록',big:diffN+'개',
       p:diffN?('그중 결과의 절댓값 = 절댓값의 차인 것 '+diffOk+'개.'):'부호가 다른 경우도 기록해 보자.'}
    ];
    var concl;
    if(sameN===0||diffN===0){
      concl='<b>더 해 보자</b> — 부호가 <b>같은 경우와 다른 경우</b>를 모두 기록해야 규칙을 나눌 수 있다.';
    } else if(sameOk===sameN && diffOk===diffN){
      concl='<b>정리</b> — 부호가 같으면 절댓값을 <b>더하고</b> 공통 부호를 붙였고, 부호가 다르면 절댓값을 <b>빼고</b> 절댓값이 큰 쪽 부호를 붙였다. '
           +'수직선에서 보면 같은 방향으로 두 번 가느냐, 반대 방향으로 되돌아오느냐의 차이다. 언제나 절댓값을 더하는 것이 아니다.';
    } else {
      concl='<b>확인 필요</b> — 규칙과 어긋난 기록이 있다.';
    }
    return {head:['식','결과','부호','절댓값 합','절댓값 차','결과의 절댓값','규칙과 맞나?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 뺄셈은 더하기로
# ============================================================
LAB_INTSUB = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'뺄셈 바꾸기판',
  action:'부호 바꿔 더해 보기',
  hint0:'두 정수를 정하고, 빼기를 더하기로 바꿔 계산해 보자.',
  sliders:[
    {id:'a',label:'앞의 수',min:-10,max:10,value:-4,color:'#2563eb',unit:''},
    {id:'b',label:'빼는 수',min:-10,max:10,value:-7,color:'#f59e0b',unit:''}
  ],
  readout:function(S,ran){
    return [{k:'식',v:pn(S.a)+' − '+pn(S.b)},
            {k:'결과',v:ran?(S.a-S.b):'계산해 보자'}];
  },
  doneMsg:function(S){
    return pn(S.a)+' − '+pn(S.b)+' = '+pn(S.a)+' + '+pn(-S.b)+' = '+(S.a-S.b)
      +'.  순서를 바꾼 '+pn(S.b)+' − '+pn(S.a)+'는 '+(S.b-S.a)+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var X0=30, X1=410, LO=-20, HI=20, i;
    function px(v){ return X0+(X1-X0)*(v-LO)/(HI-LO); }
    var Y=246;
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(X0,Y);ctx.lineTo(X1,Y);ctx.stroke();
    for(i=LO;i<=HI;i++){
      var x=px(i), big=(i%5===0);
      ctx.beginPath();ctx.moveTo(x,Y-(big?9:4));ctx.lineTo(x,Y+(big?9:4));
      ctx.strokeStyle=big?'#475569':'#cbd5e1';ctx.lineWidth=big?2:1;ctx.stroke();
      if(big){ ctx.fillStyle='#475569';ctx.font='12px sans-serif';ctx.textAlign='center';ctx.fillText(i,x,Y+26); }
    }
    ctx.textAlign='left';
    lbl(ctx,'빼기를 더하기로 바꿔 보자',24,36,'#1d4ed8',19);
    var p1=(t===null)?0:Math.min(1,t/0.5);
    var p2=(t===null)?0:Math.max(0,(t-0.5)/0.5);
    lbl(ctx,pn(S.a)+'  −  '+pn(S.b),40,92,'#1f2937',26);
    if(p1>0){
      ctx.globalAlpha=p1;
      lbl(ctx,'↓  빼는 수의 부호를 바꾸고 더하기',40,126,'#b45309',17);
      lbl(ctx,pn(S.a)+'  +  '+pn(-S.b),40,166,'#b45309',26);
      ctx.globalAlpha=1;
    }
    if(p2>0){
      var xa=px(S.a), xb=px(S.a)+(px(S.a-S.b)-px(S.a))*p2;
      ctx.strokeStyle='#2563eb';ctx.lineWidth=4;
      ctx.beginPath();ctx.moveTo(px(0),Y-16);ctx.lineTo(xa,Y-16);ctx.stroke();
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=4;
      ctx.beginPath();ctx.moveTo(xa,Y-38);ctx.lineTo(xb,Y-38);ctx.stroke();
      ctx.beginPath();ctx.arc(xb,Y,8,0,Math.PI*2);ctx.fillStyle='#dc2626';ctx.fill();
    }
    box(ctx,20,286,400,98);
    lbl(ctx,(t===null)?'결과는?':(pn(S.a)+' − '+pn(S.b)+' = '+(S.a-S.b)),38,318,'#1f2937',21);
    lbl(ctx,(t===null)?'':('순서를 바꾸면 : '+pn(S.b)+' − '+pn(S.a)+' = '+(S.b-S.a)),38,348,'#b91c1c',19);
    lbl(ctx,(t===null)?'':((S.a-S.b===S.b-S.a)?'두 값이 같다 (두 수가 같을 때만)':'두 값이 다르다'),38,374,'#52627a',17);
  },
  record:function(S){
    return {a:S.a,b:S.b,sub:S.a-S.b,addNeg:S.a+(-S.b),rev:S.b-S.a,
            same:((S.a-S.b)===(S.a+(-S.b))),
            comm:((S.a-S.b)===(S.b-S.a))};
  },
  headA:['번호','식','빼기로 계산','부호 바꿔 더하기','같은가?','순서 바꾼 값','순서 바꿔도 같은가?'],
  rowA:function(r,i){
    return [i+1,pn(r.a)+' − '+pn(r.b),'<b>'+r.sub+'</b>',r.addNeg,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            r.rev,
            '<span class="'+(r.comm?'ok':'no')+'">'+(r.comm?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,comm=0,eq=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.comm){ comm++; if(r.a===r.b) eq++; }
      rows.push([pn(r.a)+' − '+pn(r.b), '<b>'+r.sub+'</b>', pn(r.a)+' + '+pn(-r.b)+' = '+r.addNeg,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 r.rev,
                 '<span class="'+(r.comm?'ok':'no')+'">'+(r.comm?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'“부호 바꿔 더하기”가 맞은 횟수',big:same+' / '+rec.length,
       p:'a − b 와 a + (−b)를 비교한 결과.'},
      {t:'순서를 바꿔도 같았던 횟수',big:comm+' / '+rec.length,
       p:comm?('그중 두 수가 같았던 경우 '+eq+'개.'):'뺄셈은 순서를 바꾸면 값이 달라진다.'},
      {t:'기록 수',big:rec.length+'개',p:'음수끼리 빼는 경우도 넣어 확인해 보자.'}
    ];
    var concl;
    if(same===rec.length && comm===eq){
      concl='<b>정리</b> — 뺄셈은 언제나 <b>빼는 수의 부호를 바꿔 더하는 것</b>과 같았다. (−4) − (−7)은 (−4) + 7이 되어 3이다. '
           +'반면 순서를 바꾸면 값이 달라졌다. 뺄셈에는 교환법칙이 성립하지 않는다(두 수가 같을 때만 우연히 같다).';
    } else if(same===rec.length){
      concl='<b>정리</b> — 뺄셈은 부호를 바꿔 더하는 것과 항상 같았다. 순서를 바꾼 경우도 함께 확인해 보자.';
    } else {
      concl='<b>확인 필요</b> — 두 계산이 다른 기록이 있다.';
    }
    return {head:['식','빼기','부호 바꿔 더하기','같은가?','순서 바꾼 값','같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 음수의 곱셈
# ============================================================
LAB_NEGMUL = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'곱셈표판',
  action:'표를 채워 규칙 찾기',
  hint0:'두 정수를 정하고 곱셈표에서 규칙을 확인해 보자.',
  sliders:[
    {id:'a',label:'첫 번째 수',min:-5,max:5,value:-3,color:'#2563eb',unit:''},
    {id:'b',label:'두 번째 수',min:-5,max:5,value:-4,color:'#f59e0b',unit:''}
  ],
  readout:function(S,ran){
    return [{k:'식',v:pn(S.a)+' × '+pn(S.b)},
            {k:'결과',v:ran?(S.a*S.b):'채워 보자'}];
  },
  doneMsg:function(S){
    var p=S.a*S.b;
    var same=((S.a>0&&S.b>0)||(S.a<0&&S.b<0));
    if(S.a===0||S.b===0) return '0을 곱하면 결과는 0이다. 기록해 보자.';
    return pn(S.a)+' × '+pn(S.b)+' = '+p+'. 부호가 '+(same?'같아서 양수':'달라서 음수')+'가 되었다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var i,j;
    var CS=34, X0=76, Y0=76;
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*11);
    lbl(ctx,'곱셈표에서 규칙 찾기',24,38,'#1d4ed8',19);
    for(i=-5;i<=5;i++){
      var cx=X0+(i+5)*CS;
      ctx.fillStyle='#475569';ctx.font='bold 13px sans-serif';ctx.textAlign='center';
      ctx.fillText(i,cx+CS/2,Y0-8);
      ctx.fillText(i,X0-14,Y0+(i+5)*CS+CS/2+4);
    }
    for(i=-5;i<=5;i++){
      if((i+5)>=shown) break;
      for(j=-5;j<=5;j++){
        var v=i*j;
        var x=X0+(j+5)*CS, y=Y0+(i+5)*CS;
        ctx.fillStyle=(v>0)?'#dbeafe':((v<0)?'#fee2e2':'#f1f5f9');
        ctx.fillRect(x,y,CS-1,CS-1);
        if(i===S.a&&j===S.b){
          ctx.strokeStyle='#f59e0b';ctx.lineWidth=3;ctx.strokeRect(x,y,CS-1,CS-1);
        }
        ctx.fillStyle=(v>0)?'#1d4ed8':((v<0)?'#b91c1c':'#94a3b8');
        ctx.font='bold 12px sans-serif';ctx.textAlign='center';
        ctx.fillText(v,x+CS/2,y+CS/2+4);
      }
    }
    ctx.textAlign='left';
    var p=S.a*S.b;
    var same=((S.a>0&&S.b>0)||(S.a<0&&S.b<0));
    box(ctx,20,332,400,80);
    lbl(ctx,pn(S.a)+' × '+pn(S.b)+' = '+((t===null)?'?':p),38,364,'#1f2937',22);
    lbl(ctx,(t===null)?'부호는 어떻게 정해질까?':
        ((S.a===0||S.b===0)?'0을 곱하면 0':('부호가 '+(same?'같으면 양수(+)':'다르면 음수(−)'))),
        38,394,same?'#1d4ed8':'#b91c1c',18);
  },
  record:function(S){
    var p=S.a*S.b;
    var same=((S.a>0&&S.b>0)||(S.a<0&&S.b<0));
    var zero=(S.a===0||S.b===0);
    return {a:S.a,b:S.b,p:p,same:same,zero:zero,
            absOk:(Math.abs(p)===Math.abs(S.a)*Math.abs(S.b)),
            signOk:zero?(p===0):(same?(p>0):(p<0)),
            bothNeg:(S.a<0&&S.b<0)};
  },
  headA:['번호','식','결과','부호','절댓값의 곱','부호 규칙과 맞나?'],
  rowA:function(r,i){
    return [i+1,pn(r.a)+' × '+pn(r.b),'<b>'+r.p+'</b>',r.zero?'0':(r.same?'같음':'다름'),
            Math.abs(r.a)*Math.abs(r.b),
            '<span class="'+(r.signOk?'ok':'no')+'">'+(r.signOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],signOk=0,absOk=0,neg=0,negPos=0,mix=0,mixNeg=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.signOk) signOk++;
      if(r.absOk) absOk++;
      if(r.bothNeg){ neg++; if(r.p>0) negPos++; }
      if(!r.zero&&!r.same){ mix++; if(r.p<0) mixNeg++; }
      rows.push([pn(r.a)+' × '+pn(r.b), '<b>'+r.p+'</b>', r.zero?'0':(r.same?'같음':'다름'),
                 Math.abs(r.a)*Math.abs(r.b),
                 '<span class="'+(r.absOk?'ok':'no')+'">'+(r.absOk?'○':'×')+'</span>',
                 '<span class="'+(r.signOk?'ok':'no')+'">'+(r.signOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'부호 규칙이 맞은 횟수',big:signOk+' / '+rec.length,
       p:'부호가 같으면 +, 다르면 − 규칙과 결과가 일치했는지 확인한 결과.'},
      {t:'음수 × 음수 기록',big:neg+'개',
       p:neg?('그중 결과가 양수였던 것 '+negPos+'개.'):'음수끼리 곱한 경우도 기록해 보자.'},
      {t:'부호가 다른 곱셈 기록',big:mix+'개',
       p:mix?('그중 결과가 음수였던 것 '+mixNeg+'개.'):'부호가 다른 경우도 기록해 보자.'}
    ];
    var concl;
    if(neg===0||mix===0){
      concl='<b>더 해 보자</b> — 음수끼리 곱한 경우와 부호가 다른 경우를 <b>모두</b> 기록해야 규칙이 보인다.';
    } else if(signOk===rec.length && absOk===rec.length){
      concl='<b>정리</b> — 절댓값은 언제나 그냥 곱한 값이었고, 부호만 규칙을 따랐다. '
           +'<b>부호가 같으면 +, 다르면 −</b>. 표에서 한 줄을 따라가 보면 3×(−1)=−3, 3×(−2)=−6처럼 3씩 줄어들고, '
           +'같은 흐름을 음수 줄로 이어가면 (−3)×(−4)가 +12가 되는 것이 자연스럽게 이어진다.';
    } else {
      concl='<b>확인 필요</b> — 규칙과 어긋난 기록이 있다.';
    }
    return {head:['식','결과','부호','절댓값의 곱','절댓값 맞나?','부호 규칙 맞나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 거듭제곱과 괄호
# ============================================================
LAB_POWER = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'거듭제곱 비교판',
  action:'풀어 써서 계산하기',
  hint0:'밑과 지수를 정하고, 괄호가 있을 때와 없을 때를 비교해 보자.',
  sliders:[
    {id:'a',label:'밑의 절댓값',min:1,max:5,value:2,color:'#2563eb',unit:''},
    {id:'n',label:'지수',min:1,max:5,value:2,color:'#f59e0b',unit:'제곱'}
  ],
  calc:function(S){
    var v1=Math.pow(-S.a,S.n);
    var v2=-Math.pow(S.a,S.n);
    return {v1:v1,v2:v2,same:(v1===v2),even:(S.n%2===0)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'(−'+S.a+')^'+S.n,v:ran?c.v1:'계산해 보자'},
            {k:'−'+S.a+'^'+S.n,v:ran?c.v2:'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '(−'+S.a+')^'+S.n+' = '+c.v1+',  −'+S.a+'^'+S.n+' = '+c.v2+'. 두 값이 '
      +(c.same?'같다 (지수가 홀수)':'다르다 (지수가 짝수)')+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var p1=(t===null)?0:Math.min(1,t/0.5);
    var p2=(t===null)?0:Math.max(0,(t-0.5)/0.5);
    lbl(ctx,'괄호가 있을 때와 없을 때',24,38,'#1d4ed8',19);
    lbl(ctx,'( −'+S.a+' )'+'^'+S.n,40,92,'#1d4ed8',26);
    if(p1>0){
      var s1=[];
      for(i=0;i<S.n;i++){ s1.push('(−'+S.a+')'); }
      ctx.globalAlpha=p1;
      lbl(ctx,'= '+s1.join(' × '),40,128,'#334155',(S.n>=4)?15:18);
      lbl(ctx,'= '+c.v1,40,160,'#1d4ed8',22);
      ctx.globalAlpha=1;
    }
    lbl(ctx,'−'+S.a+'^'+S.n,40,216,'#b91c1c',26);
    if(p2>0){
      var s2=[];
      for(i=0;i<S.n;i++){ s2.push(''+S.a); }
      ctx.globalAlpha=p2;
      lbl(ctx,'= −( '+s2.join(' × ')+' )',40,250,'#334155',(S.n>=4)?15:18);
      lbl(ctx,'= '+c.v2,40,282,'#b91c1c',22);
      ctx.globalAlpha=1;
    }
    box(ctx,20,304,400,80);
    lbl(ctx,(t===null)?'두 값은 같을까?':((c.same?'두 값이 같다':'두 값이 다르다')+'   '+c.v1+' / '+c.v2),
        38,336,c.same?'#15803d':'#b91c1c',21);
    lbl(ctx,(t===null)?'괄호는 무엇까지 묶을까?':('지수 '+S.n+'은 '+(c.even?'짝수':'홀수')),38,366,'#52627a',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,n:S.n,v1:c.v1,v2:c.v2,same:c.same,even:c.even};
  },
  headA:['번호','(−a)^n','값','−a^n','값','같은가?','지수'],
  rowA:function(r,i){
    return [i+1,'(−'+r.a+')^'+r.n,'<b>'+r.v1+'</b>','−'+r.a+'^'+r.n,r.v2,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            r.even?'짝수':'홀수'];
  },
  analyze:function(rec){
    var rows=[],same=0,ev=0,evSame=0,od=0,odSame=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.even){ ev++; if(r.same) evSame++; }
      else { od++; if(r.same) odSame++; }
      rows.push(['(−'+r.a+')^'+r.n+' 와 −'+r.a+'^'+r.n, r.v1, r.v2, r.even?'짝수':'홀수',
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'두 값이 같았던 횟수',big:same+' / '+rec.length,p:'괄호가 있을 때와 없을 때가 같았던 기록 수.'},
      {t:'지수가 짝수였던 기록',big:ev+'개',p:ev?('그중 두 값이 같았던 것 '+evSame+'개.'):'지수를 짝수로도 해 보자.'},
      {t:'지수가 홀수였던 기록',big:od+'개',p:od?('그중 두 값이 같았던 것 '+odSame+'개.'):'지수를 홀수로도 해 보자.'}
    ];
    var concl;
    if(ev===0||od===0){
      concl='<b>더 해 보자</b> — 지수를 <b>짝수와 홀수 모두</b> 기록해야 규칙이 보인다.';
    } else if(evSame===0 && odSame===od){
      concl='<b>정리</b> — (−2)²은 (−2)×(−2) = 4이고, −2²은 −(2×2) = −4였다. '
           +'괄호가 있으면 <b>음의 부호까지 거듭제곱</b>하고, 없으면 <b>양수만 거듭제곱한 뒤 부호를 붙인다.</b> '
           +'지수가 홀수일 때는 우연히 값이 같아 보이지만, 짝수일 때는 '+ev+'번 모두 달랐다.';
    } else {
      concl='<b>확인 필요</b> — 규칙과 어긋난 기록이 있다.';
    }
    return {head:['비교','(−a)^n','−a^n','지수','같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("m1_prime_factorization_lab.html",
     "소인수분해 실험실 — 약수의 개수를 세지 않고 구할 수 있을까?",
     "소인수분해 실험실 — 약수의 개수를 세지 않고 구할 수 있을까?",
     "수를 소수로 나누어 소인수분해하고, (지수+1)의 곱과 실제로 센 약수의 개수를 비교한다.",
     LAB_FACTOR),
    ("m1_integer_addition_lab.html",
     "정수 덧셈 실험실 — 절댓값을 더하면 될까?",
     "정수 덧셈 실험실 — 절댓값을 더하면 될까?",
     "수직선 위에서 두 번 이동해 정수의 합을 구하고, 부호가 같을 때와 다를 때를 나누어 기록한다.",
     LAB_INTADD),
    ("m1_integer_subtraction_lab.html",
     "정수 뺄셈 실험실 — 빼기는 왜 더하기가 될까?",
     "정수 뺄셈 실험실 — 빼기는 왜 더하기가 될까?",
     "빼는 수의 부호를 바꿔 더한 값과 직접 뺀 값을 비교하고, 순서를 바꾸면 어떻게 되는지 확인한다.",
     LAB_INTSUB),
    ("m1_negative_multiplication_lab.html",
     "음수 곱셈 실험실 — 음수 × 음수는 왜 양수일까?",
     "음수 곱셈 실험실 — 음수 × 음수는 왜 양수일까?",
     "곱셈표를 채워 부호가 정해지는 규칙을 찾고, 절댓값과 부호를 나누어 기록한다.",
     LAB_NEGMUL),
    ("m1_power_sign_lab.html",
     "거듭제곱 실험실 — (−2)²과 −2²은 같을까?",
     "거듭제곱 실험실 — (−2)²과 −2²은 같을까?",
     "밑과 지수를 바꿔 가며 두 식을 풀어 쓰고, 괄호가 무엇까지 묶는지 확인한다.",
     LAB_POWER),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c9_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
