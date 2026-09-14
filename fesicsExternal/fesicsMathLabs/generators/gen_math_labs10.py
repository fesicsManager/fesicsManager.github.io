# -*- coding: utf-8 -*-
"""중1 '변화와 관계' 실험 5종"""
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
function pn(v){return (v<0)?('('+v+')'):(''+v);}
function sgnStr(v){return (v<0)?(' − '+(-v)):(' + '+v);}
"""

# ============================================================
# 1. 동류항
# ============================================================
LAB_LIKE = BASE + r"""
var LAB = {
  cw:440, ch:420, cvTitle:'문자 타일판',
  action:'타일로 확인하기',
  hint0:'식의 계수와 문자에 넣을 수를 정하고, 두 계산을 비교해 보자.',
  sliders:[
    {id:'p',label:'a의 계수',min:1,max:9,value:3,color:'#2563eb',unit:''},
    {id:'q',label:'b의 계수',min:1,max:9,value:2,color:'#16a34a',unit:''},
    {id:'av',label:'a에 넣을 수',min:1,max:9,value:4,color:'#60a5fa',unit:''},
    {id:'bv',label:'b에 넣을 수',min:1,max:9,value:5,color:'#4ade80',unit:''}
  ],
  calc:function(S){
    return {real:S.p*S.av+S.q*S.bv, wrong:(S.p+S.q)*S.av*S.bv};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'식',v:S.p+'a + '+S.q+'b'},
            {k:'a='+S.av+', b='+S.bv,v:ran?(c.real+' / '+c.wrong):'확인해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '실제 값은 '+c.real+', '+(S.p+S.q)+'ab로 계산하면 '+c.wrong+'다. '
      +((c.real===c.wrong)?'우연히 같다.':'다르다. a와 b는 서로 다른 타일이라 합칠 수 없다.')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var U=16, X0=40;
    var show=(t===null)?0:Math.min(1,t);
    lbl(ctx,S.p+'a + '+S.q+'b   (a='+S.av+', b='+S.bv+')',24,38,'#1d4ed8',19);
    var y=64;
    for(i=0;i<S.p;i++){
      ctx.fillStyle='#bfdbfe';ctx.fillRect(X0,y,S.av*U,20);
      ctx.strokeStyle='#2563eb';ctx.lineWidth=2;ctx.strokeRect(X0,y,S.av*U,20);
      if(show>0){ lbl(ctx,''+S.av,X0+S.av*U+8,y+16,'#1d4ed8',14); }
      y+=26;
    }
    y+=10;
    for(i=0;i<S.q;i++){
      ctx.fillStyle='#bbf7d0';ctx.fillRect(X0,y,S.bv*U,20);
      ctx.strokeStyle='#16a34a';ctx.lineWidth=2;ctx.strokeRect(X0,y,S.bv*U,20);
      if(show>0){ lbl(ctx,''+S.bv,X0+S.bv*U+8,y+16,'#15803d',14); }
      y+=26;
    }
    lbl(ctx,'a 타일 '+S.p+'개',260,84,'#1d4ed8',17);
    lbl(ctx,'b 타일 '+S.q+'개',260,112,'#15803d',17);
    if(show>0){
      lbl(ctx,'길이가 다른 타일은',260,150,'#52627a',16);
      lbl(ctx,'한 종류로 묶을 수 없다',260,174,'#52627a',16);
    }
    box(ctx,20,304,400,102);
    lbl(ctx,(t===null)?'값을 넣어 보면?':(S.p+'×'+S.av+' + '+S.q+'×'+S.bv+' = '+c.real),38,336,'#1f2937',20);
    lbl(ctx,(t===null)?'':((S.p+S.q)+'ab = '+(S.p+S.q)+'×'+S.av+'×'+S.bv+' = '+c.wrong),38,366,'#b91c1c',19);
    lbl(ctx,(t===null)?'3a + 2b = 5ab 일까?':((c.real===c.wrong)?'두 값이 같다':'두 값이 다르다'),
        38,394,(c.real===c.wrong)?'#b45309':'#15803d',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {p:S.p,q:S.q,av:S.av,bv:S.bv,real:c.real,wrong:c.wrong,same:(c.real===c.wrong),
            one:(S.av===1||S.bv===1)};
  },
  headA:['번호','식','a','b','바르게 계산','5ab식으로 계산','같은가?'],
  rowA:function(r,i){
    return [i+1,r.p+'a + '+r.q+'b',r.av,r.bv,'<b>'+r.real+'</b>',r.wrong,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,combos={},cn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      combos[r.av+','+r.bv]=true;
      rows.push([r.p+'a + '+r.q+'b', 'a='+r.av+', b='+r.bv, '<b>'+r.real+'</b>', r.wrong,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>']);
    }
    for(var k in combos) cn++;
    var stats=[
      {t:'“계수를 더하고 문자를 붙이는” 방법이 맞은 횟수',big:same+' / '+rec.length,
       p:'3a + 2b = 5ab 처럼 계산했을 때 실제 값과 같았던 기록 수.'},
      {t:'시험한 a, b 값의 조합',big:cn+'가지',
       p:cn>1?'값을 바꿔도 결과가 같았는지 확인했다.':'a와 b에 다른 수도 넣어 보자.'},
      {t:'기록 수',big:rec.length+'개',p:'문자에 어떤 수를 넣어도 성립해야 식이 같다고 할 수 있다.'}
    ];
    var concl;
    if(same===0){
      concl='<b>정리</b> — 3a + 2b를 5ab로 바꾼 계산은 <b>한 번도 맞지 않았다.</b> '
           +'a 타일과 b 타일은 길이가 달라서 한 종류로 셀 수 없다. 계수를 더할 수 있는 것은 <b>문자 부분이 완전히 같은 동류항</b>뿐이다. '
           +'3a + 2a = 5a는 되지만 3a + 2b는 더 줄일 수 없다.';
    } else {
      concl='<b>정리</b> — 대부분 두 값이 달랐다. 우연히 같아지는 경우가 있어도 <b>모든 값에서 같아야</b> 식이 같은 것이다. '
           +'a와 b에 다른 수를 넣어 다시 확인해 보자.';
    }
    return {head:['식','대입','바른 값','5ab식 값','같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 등식의 성질
# ============================================================
LAB_EQ = BASE + r"""
var OPS=['양변에 더하기','왼쪽에만 더하기','양변에 곱하기','왼쪽에만 곱하기'];
var LAB = {
  cw:440, ch:420, cvTitle:'등식 저울판',
  action:'조작하고 저울 보기',
  hint0:'양쪽 값과 조작 방법을 정해 보자. 등식이 유지될까?',
  sliders:[
    {id:'L',label:'왼쪽 값',min:1,max:20,value:8,color:'#2563eb',unit:''},
    {id:'R',label:'오른쪽 값',min:1,max:20,value:8,color:'#dc2626',unit:''},
    {id:'op',label:'조작',min:0,max:3,value:0,color:'#16a34a',fmt:function(v){return OPS[v];}},
    {id:'k',label:'조작에 쓸 수',min:-9,max:9,value:3,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var L2,R2;
    if(S.op===0){ L2=S.L+S.k; R2=S.R+S.k; }
    else if(S.op===1){ L2=S.L+S.k; R2=S.R; }
    else if(S.op===2){ L2=S.L*S.k; R2=S.R*S.k; }
    else { L2=S.L*S.k; R2=S.R; }
    return {L2:L2,R2:R2,before:(S.L===S.R),after:(L2===R2)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'조작 전',v:S.L+' vs '+S.R+(c.before?' (같음)':' (다름)')},
            {k:'조작 후',v:ran?(c.L2+' vs '+c.R2):'해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '조작 후 '+c.L2+' 와 '+c.R2+'. 등식이 '+(c.after?'유지되었다':'깨졌다')+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var mv=(t===null)?0:Math.min(1,t);
    var curL=S.L+(c.L2-S.L)*mv, curR=S.R+(c.R2-S.R)*mv;
    var d=curR-curL;
    var th=Math.max(-0.2,Math.min(0.2,d*0.012));
    var px=220, py=140, arm=140;
    ctx.fillStyle='#cbd5e1';
    ctx.beginPath();ctx.moveTo(px,py);ctx.lineTo(px-36,py+140);ctx.lineTo(px+36,py+140);ctx.closePath();ctx.fill();
    var lx=px-arm*Math.cos(th), ly=py-arm*Math.sin(th);
    var rx=px+arm*Math.cos(th), ry=py+arm*Math.sin(th);
    ctx.strokeStyle='#475569';ctx.lineWidth=7;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(lx,ly);ctx.lineTo(rx,ry);ctx.stroke();ctx.lineCap='butt';
    function pan(cx,cy,v,col){
      ctx.strokeStyle='#94a3b8';ctx.lineWidth=2;
      ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(cx-42,cy+40);ctx.moveTo(cx,cy);ctx.lineTo(cx+42,cy+40);ctx.stroke();
      ctx.fillStyle='#eef4fc';ctx.fillRect(cx-50,cy+40,100,46);
      ctx.strokeStyle=col;ctx.lineWidth=2.5;ctx.strokeRect(cx-50,cy+40,100,46);
      lbl(ctx,''+r1(v),cx,cy+72,col,22,'center');
    }
    pan(lx,ly,curL,'#2563eb');
    pan(rx,ry,curR,'#dc2626');
    lbl(ctx,OPS[S.op]+'  ( '+S.k+' )',24,36,'#1d4ed8',19);
    box(ctx,20,318,400,88);
    lbl(ctx,'조작 전 : '+S.L+' , '+S.R+'  →  '+(c.before?'같음':'다름'),38,350,'#52627a',18);
    lbl(ctx,(t===null)?'조작하면 등식은 어떻게 될까?':('조작 후 : '+c.L2+' , '+c.R2+'  →  '+(c.after?'같음':'다름')),
        38,382,c.after?'#15803d':'#b91c1c',19);
  },
  record:function(S){
    var c=this.calc(S);
    return {L:S.L,R:S.R,op:S.op,opName:OPS[S.op],k:S.k,L2:c.L2,R2:c.R2,
            before:c.before,after:c.after,both:(S.op===0||S.op===2),
            keep:(c.before===c.after)};
  },
  headA:['번호','조작 전','조작','수','조작 후','조작 전 등식','조작 후 등식'],
  rowA:function(r,i){
    return [i+1,r.L+' = '+r.R,r.opName,r.k,r.L2+' , '+r.R2,
            '<span class="'+(r.before?'ok':'no')+'">'+(r.before?'성립':'불성립')+'</span>',
            '<span class="'+(r.after?'ok':'no')+'">'+(r.after?'성립':'불성립')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],bothN=0,bothKeep=0,oneN=0,oneKeep=0,startEq=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.before) startEq++;
      if(!r.before){ rows.push([r.L+' , '+r.R, r.opName+' '+r.k, r.L2+' , '+r.R2, '처음부터 등식 아님', '-']); continue; }
      if(r.both){ bothN++; if(r.after) bothKeep++; }
      else { oneN++; if(r.after) oneKeep++; }
      rows.push([r.L+' = '+r.R, r.opName+' '+r.k, r.L2+' , '+r.R2,
                 r.both?'양변':'한쪽만',
                 '<span class="'+(r.after?'ok':'no')+'">'+(r.after?'성립':'깨짐')+'</span>']);
    }
    var stats=[
      {t:'처음부터 등식이었던 기록',big:startEq+' / '+rec.length,
       p:'양쪽 값을 같게 맞춘 기록만 등식의 성질을 확인할 수 있다.'},
      {t:'양변에 똑같이 했을 때 유지',big:bothN?(bothKeep+' / '+bothN):'기록 없음',
       p:bothN?'양변에 같은 조작을 한 기록 중 등식이 유지된 수.':'양변 조작도 기록해 보자.'},
      {t:'한쪽에만 했을 때 유지',big:oneN?(oneKeep+' / '+oneN):'기록 없음',
       p:oneN?'한쪽만 조작한 기록 중 등식이 유지된 수. 0을 더하거나 1을 곱하면 사실 아무것도 안 한 것이다.':'한쪽만 조작한 경우도 기록해 보자.'}
    ];
    var concl;
    if(startEq===0){
      concl='<b>더 해 보자</b> — 양쪽 값을 같게 맞춰 등식을 만든 뒤 조작해야 성질을 확인할 수 있다.';
    } else if(bothN===0||oneN===0){
      concl='<b>더 해 보자</b> — 양변에 조작한 경우와 한쪽만 조작한 경우를 <b>모두</b> 기록해 비교해 보자.';
    } else if(bothKeep===bothN){
      concl='<b>정리</b> — 등식의 양변에 같은 수를 더하거나 곱하면 '+bothN+'번 모두 등식이 유지되었지만, '
           +'한쪽에만 하면 '+(oneN-oneKeep)+'번 깨졌다. 저울에서 한쪽에만 무게를 얹으면 기울어지는 것과 같다. '
           +'방정식을 풀 때 <b>반드시 양변에 똑같이</b> 해야 하는 이유다.';
    } else {
      concl='<b>확인 필요</b> — 양변에 같은 조작을 했는데 등식이 깨진 기록이 있다.';
    }
    return {head:['조작 전','조작','조작 후','범위','조작 후 등식'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 이항
# ============================================================
LAB_MOVE = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'이항 실험판',
  action:'옮겨서 풀고 검산하기',
  hint0:'방정식의 계수를 정하고, 상수항을 옮겨 풀어 보자.',
  sliders:[
    {id:'a',label:'x의 계수',min:1,max:9,value:3,color:'#2563eb',unit:''},
    {id:'b',label:'왼쪽 상수항',min:-9,max:9,value:5,color:'#f59e0b',unit:''},
    {id:'c',label:'오른쪽 값',min:-20,max:20,value:14,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var x1=(S.c-S.b)/S.a, x2=(S.c+S.b)/S.a;
    return {x1:x1,x2:x2,chk1:S.a*x1+S.b,chk2:S.a*x2+S.b};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'방정식',v:S.a+'x'+sgnStr(S.b)+' = '+S.c},
            {k:'해',v:ran?r2(c.x1):'풀어 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'x = '+r2(c.x1)+'. 검산하면 '+r2(c.chk1)+'로 오른쪽 값 '+S.c+'와 같다. 부호를 그대로 옮긴 답 '+r2(c.x2)+'도 검산해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var p1=(t===null)?0:Math.min(1,t/0.5);
    var p2=(t===null)?0:Math.max(0,(t-0.5)/0.5);
    lbl(ctx,'상수항을 오른쪽으로 옮기기',24,38,'#1d4ed8',19);
    lbl(ctx,S.a+'x'+sgnStr(S.b)+' = '+S.c,40,92,'#1f2937',26);
    if(p1>0){
      ctx.globalAlpha=p1;
      lbl(ctx,'양변에서 '+S.b+'를 빼면',40,128,'#52627a',17);
      lbl(ctx,S.a+'x = '+S.c+sgnStr(-S.b)+' = '+(S.c-S.b),40,166,'#1d4ed8',24);
      ctx.globalAlpha=1;
    }
    if(p2>0){
      ctx.globalAlpha=p2;
      lbl(ctx,'양변을 '+S.a+'로 나누면',40,204,'#52627a',17);
      lbl(ctx,'x = '+r2(c.x1),40,242,'#15803d',26);
      ctx.globalAlpha=1;
    }
    box(ctx,20,266,400,118);
    lbl(ctx,(t===null)?'부호를 그대로 옮기면 어떻게 될까?':('검산 : '+S.a+'×'+r2(c.x1)+sgnStr(S.b)+' = '+r2(c.chk1)+'   (오른쪽 '+S.c+')'),
        38,298,'#15803d',17);
    lbl(ctx,(t===null)?'':('부호 그대로 옮긴 답 : x = '+r2(c.x2)),38,328,'#b91c1c',18);
    lbl(ctx,(t===null)?'':('검산 : '+S.a+'×'+r2(c.x2)+sgnStr(S.b)+' = '+r2(c.chk2)+'   (오른쪽 '+S.c+')'),38,356,'#b91c1c',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,c:S.c,x1:r2(c.x1),x2:r2(c.x2),
            ok1:(Math.abs(c.chk1-S.c)<1e-9),ok2:(Math.abs(c.chk2-S.c)<1e-9),
            chk1:r2(c.chk1),chk2:r2(c.chk2),bZero:(S.b===0)};
  },
  headA:['번호','방정식','부호 바꿔 옮긴 해','검산','맞나?','부호 그대로 옮긴 해','검산','맞나?'],
  rowA:function(r,i){
    return [i+1,r.a+'x'+sgnStr(r.b)+' = '+r.c,'<b>'+r.x1+'</b>',r.chk1,
            '<span class="'+(r.ok1?'ok':'no')+'">'+(r.ok1?'○':'×')+'</span>',
            r.x2,r.chk2,
            '<span class="'+(r.ok2?'ok':'no')+'">'+(r.ok2?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ok1=0,ok2=0,bz=0,bzOk=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.ok1) ok1++;
      if(r.ok2) ok2++;
      if(r.bZero){ bz++; if(r.ok2) bzOk++; }
      rows.push([r.a+'x'+sgnStr(r.b)+' = '+r.c, '<b>'+r.x1+'</b>', r.chk1,
                 '<span class="'+(r.ok1?'ok':'no')+'">'+(r.ok1?'○':'×')+'</span>',
                 r.x2, r.chk2,
                 '<span class="'+(r.ok2?'ok':'no')+'">'+(r.ok2?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'부호를 바꿔 옮긴 해가 맞은 횟수',big:ok1+' / '+rec.length,p:'검산해서 오른쪽 값과 같았던 기록 수.'},
      {t:'부호를 그대로 옮긴 해가 맞은 횟수',big:ok2+' / '+rec.length,p:'검산이 통과된 기록 수.'},
      {t:'상수항이 0이었던 기록',big:bz+'개',
       p:bz?('그중 그대로 옮긴 답도 맞은 것 '+bzOk+'개. 0은 부호를 바꿔도 0이다.'):'상수항이 0인 경우도 넣어 보자.'}
    ];
    var concl;
    if(ok1===rec.length && ok2===bz){
      concl='<b>정리</b> — 부호를 바꿔 옮긴 해는 언제나 검산을 통과했고, 부호를 그대로 옮긴 해는 상수항이 0일 때를 빼면 모두 틀렸다. '
           +'이항은 새로운 규칙이 아니라 <b>양변에서 같은 수를 빼는 것</b>을 짧게 쓴 것이다. 그래서 넘어가면 부호가 바뀐다.';
    } else if(ok1===rec.length){
      concl='<b>정리</b> — 부호를 바꿔 옮긴 해는 항상 맞았다. 상수항이 0이 아닌 경우도 더 기록해 비교해 보자.';
    } else {
      concl='<b>확인 필요</b> — 검산이 통과되지 않은 기록이 있다.';
    }
    return {head:['방정식','바른 해','검산','맞나?','그대로 옮긴 해','검산','맞나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 좌표평면
# ============================================================
LAB_COORD = BASE + r"""
function quad(x,y){
  if(x===0||y===0) return '축 위';
  if(x>0&&y>0) return '제1사분면';
  if(x<0&&y>0) return '제2사분면';
  if(x<0&&y<0) return '제3사분면';
  return '제4사분면';
}
var LAB = {
  cw:440, ch:430, cvTitle:'좌표평면판',
  action:'두 점 찍어 보기',
  hint0:'두 수를 정하고, (a, b)와 (b, a)를 함께 찍어 보자.',
  sliders:[
    {id:'a',label:'a',min:-6,max:6,value:3,color:'#2563eb',unit:''},
    {id:'b',label:'b',min:-6,max:6,value:-5,color:'#dc2626',unit:''}
  ],
  readout:function(S,ran){
    return [{k:'( a , b )',v:'( '+S.a+' , '+S.b+' )'+(ran?('  '+quad(S.a,S.b)):'')},
            {k:'( b , a )',v:'( '+S.b+' , '+S.a+' )'+(ran?('  '+quad(S.b,S.a)):'')}];
  },
  doneMsg:function(S){
    if(S.a===S.b) return 'a와 b가 같아서 두 점이 같은 자리에 찍혔다. 다른 값도 해 보자.';
    return '( '+S.a+' , '+S.b+' )는 '+quad(S.a,S.b)+', ( '+S.b+' , '+S.a+' )는 '+quad(S.b,S.a)+'에 있다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var CX=220, CY=180, U=24, i;
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=-7;i<=7;i++){
      ctx.beginPath();ctx.moveTo(CX+i*U,CY-7*U);ctx.lineTo(CX+i*U,CY+7*U);ctx.stroke();
      ctx.beginPath();ctx.moveTo(CX-7*U,CY+i*U);ctx.lineTo(CX+7*U,CY+i*U);ctx.stroke();
    }
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(CX-7*U,CY);ctx.lineTo(CX+7*U,CY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(CX,CY-7*U);ctx.lineTo(CX,CY+7*U);ctx.stroke();
    ctx.strokeStyle='#c4b5fd';ctx.lineWidth=2;ctx.setLineDash([5,5]);
    ctx.beginPath();ctx.moveTo(CX-7*U,CY+7*U);ctx.lineTo(CX+7*U,CY-7*U);ctx.stroke();ctx.setLineDash([]);
    ctx.fillStyle='#94a3b8';ctx.font='12px sans-serif';ctx.textAlign='center';
    for(i=-6;i<=6;i+=2){
      if(i!==0){ ctx.fillText(i,CX+i*U,CY+16); ctx.fillText(i,CX-16,CY-i*U+4); }
    }
    ctx.textAlign='left';
    var p1=(t===null)?0:Math.min(1,t/0.5);
    var p2=(t===null)?0:Math.max(0,(t-0.5)/0.5);
    function pt(x,y,col,label,al){
      ctx.beginPath();ctx.arc(CX+x*U,CY-y*U,9,0,Math.PI*2);
      ctx.fillStyle=col;ctx.fill();
      ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      lbl(ctx,label,CX+x*U+12,CY-y*U-10,col,15);
    }
    if(p1>0){ ctx.globalAlpha=p1; pt(S.a,S.b,'#2563eb','('+S.a+', '+S.b+')'); ctx.globalAlpha=1; }
    if(p2>0){ ctx.globalAlpha=p2; pt(S.b,S.a,'#dc2626','('+S.b+', '+S.a+')'); ctx.globalAlpha=1; }
    lbl(ctx,'( a , b )와 ( b , a )는 같은 점일까?',24,32,'#1d4ed8',18);
    box(ctx,20,354,400,58);
    lbl(ctx,(t===null)?'점선은 두 점을 바꿔 놓는 대칭축':
        ((S.a===S.b)?'a = b 이므로 같은 점':(quad(S.a,S.b)+'  vs  '+quad(S.b,S.a))),
        38,388,(S.a===S.b)?'#b45309':'#1f2937',20);
  },
  record:function(S){
    return {a:S.a,b:S.b,q1:quad(S.a,S.b),q2:quad(S.b,S.a),
            same:(S.a===S.b),sameQ:(quad(S.a,S.b)===quad(S.b,S.a))};
  },
  headA:['번호','( a , b )','사분면','( b , a )','사분면','같은 점?','같은 사분면?'],
  rowA:function(r,i){
    return [i+1,'( '+r.a+' , '+r.b+' )',r.q1,'( '+r.b+' , '+r.a+' )',r.q2,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            '<span class="'+(r.sameQ?'ok':'no')+'">'+(r.sameQ?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,sameQ=0,diffQ=0,eq=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same){ same++; eq++; }
      if(r.sameQ) sameQ++; else diffQ++;
      rows.push(['( '+r.a+' , '+r.b+' )', r.q1, '( '+r.b+' , '+r.a+' )', r.q2,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 '<span class="'+(r.sameQ?'ok':'no')+'">'+(r.sameQ?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'두 점이 같은 자리였던 횟수',big:same+' / '+rec.length,
       p:'순서를 바꿔도 같은 점이 되는 경우.'},
      {t:'사분면까지 같았던 횟수',big:sameQ+' / '+rec.length,
       p:'부호가 같으면 사분면은 같아도 자리는 다르다.'},
      {t:'사분면이 달라진 횟수',big:diffQ+'개',
       p:diffQ?'부호가 서로 다른 두 수일 때 생긴다.':'a와 b의 부호를 다르게 해 보자.'}
    ];
    var concl;
    if(eq===rec.length){
      concl='<b>더 해 보자</b> — 지금까지는 a와 b가 같은 경우만 기록했다. 서로 다른 값으로 해 보자.';
    } else {
      concl='<b>정리</b> — a와 b가 다르면 (a, b)와 (b, a)는 <b>언제나 다른 점</b>이었다. '
           +'같은 자리에 오는 것은 a = b일 때뿐이고, 그때 두 점은 점선(대칭축) 위에 있다. '
           +'좌표는 두 수를 모은 것이 아니라 <b>순서가 있는 짝</b>이다. 부호가 다르면 사분면까지 달라진다.';
    }
    return {head:['(a, b)','사분면','(b, a)','사분면','같은 점?','같은 사분면?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 정비례와 반비례 판별
# ============================================================
LAB_PROP2 = BASE + r"""
var KINDS=['y = ax (정비례)','y = a/x (반비례)','y = ax + b'];
var LAB = {
  cw:440, ch:430, cvTitle:'관계 판별판',
  action:'표와 그래프 그리기',
  hint0:'관계와 상수를 정하고, x가 1·2·3·4일 때 y를 구해 보자.',
  sliders:[
    {id:'kind',label:'관계',min:0,max:2,value:2,color:'#2563eb',fmt:function(v){return KINDS[v];}},
    {id:'a',label:'a',min:1,max:6,value:2,color:'#16a34a',unit:''},
    {id:'b',label:'b (셋째 관계에만)',min:1,max:6,value:3,color:'#f59e0b',unit:''}
  ],
  f:function(S,x){
    if(S.kind===0) return S.a*x;
    if(S.kind===1) return S.a/x;
    return S.a*x+S.b;
  },
  vals:function(S){
    var v=[],i;
    for(i=1;i<=4;i++){ v.push(this.f(S,i)); }
    return v;
  },
  readout:function(S,ran){
    var v=this.vals(S);
    return [{k:'식',v:(S.kind===0)?('y = '+S.a+'x'):((S.kind===1)?('y = '+S.a+'/x'):('y = '+S.a+'x + '+S.b))},
            {k:'y 값',v:ran?v.map(function(z){return r2(z);}).join(', '):'구해 보자'}];
  },
  doneMsg:function(S){
    var v=this.vals(S),i;
    var qs=[],ps=[];
    for(i=0;i<4;i++){ qs.push(r3(v[i]/(i+1))); ps.push(r3(v[i]*(i+1))); }
    var qc=(qs[0]===qs[1]&&qs[1]===qs[2]&&qs[2]===qs[3]);
    var pc=(ps[0]===ps[1]&&ps[1]===ps[2]&&ps[2]===ps[3]);
    return 'y÷x가 '+(qc?'일정':'일정하지 않음')+', x×y가 '+(pc?'일정':'일정하지 않음')+'. '
      +(qc?'정비례다.':(pc?'반비례다.':'정비례도 반비례도 아니다.'))+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var v=this.vals(S), i;
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*4);
    var X0=44, Y0=76, CW=60;
    lbl(ctx,(S.kind===0)?('y = '+S.a+'x'):((S.kind===1)?('y = '+S.a+' / x'):('y = '+S.a+'x + '+S.b)),24,40,'#1d4ed8',20);
    var rows=['x','y','y ÷ x','x × y'];
    for(i=0;i<4;i++){ lbl(ctx,rows[i],X0-6,Y0+i*30+20,'#475569',14,'right'); }
    for(i=0;i<4;i++){
      var x=X0+i*CW, on=(i<shown);
      ctx.fillStyle='#fff';
      ctx.strokeStyle='#94a3b8';ctx.lineWidth=1.4;
      var j;
      for(j=0;j<4;j++){
        ctx.fillStyle=(j===0)?'#f1f5f9':'#fff';
        ctx.fillRect(x,Y0+j*30,CW,30);
        ctx.strokeRect(x,Y0+j*30,CW,30);
      }
      ctx.font='bold 14px sans-serif';ctx.textAlign='center';
      ctx.fillStyle='#1f2937';ctx.fillText(i+1,x+CW/2,Y0+20);
      ctx.fillStyle=on?'#1d4ed8':'#cbd5e1';
      ctx.fillText(on?r2(v[i]):'?',x+CW/2,Y0+50);
      ctx.fillStyle=on?'#b45309':'#cbd5e1';
      ctx.fillText(on?r3(v[i]/(i+1)):'?',x+CW/2,Y0+80);
      ctx.fillStyle=on?'#15803d':'#cbd5e1';
      ctx.fillText(on?r3(v[i]*(i+1)):'?',x+CW/2,Y0+110);
    }
    ctx.textAlign='left';
    var GX=60, GY=330, GW=320, GH=110;
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+GW,GY);ctx.moveTo(GX,GY);ctx.lineTo(GX,GY-GH);ctx.stroke();
    var mx=0;
    for(i=0;i<4;i++){ if(v[i]>mx) mx=v[i]; }
    if(mx<=0) mx=1;
    ctx.strokeStyle='#dc2626';ctx.lineWidth=2.5;ctx.beginPath();
    var started=false;
    for(i=0;i<40;i++){
      var xx=0.4+i*0.14;
      if(xx>4.4) break;
      var yy=this.f(S,xx);
      var px2=GX+GW*xx/4.6, py2=GY-GH*yy/(mx*1.15);
      if(py2<GY-GH) continue;
      if(!started){ ctx.moveTo(px2,py2); started=true; } else ctx.lineTo(px2,py2);
    }
    if(shown>0&&started) ctx.stroke();
    lbl(ctx,'그래프 모양만 보고 정비례라고 할 수 있을까?',GX,GY+22,'#52627a',15);
  },
  record:function(S){
    var v=this.vals(S),i,qs=[],ps=[];
    for(i=0;i<4;i++){ qs.push(r3(v[i]/(i+1))); ps.push(r3(v[i]*(i+1))); }
    var qc=(qs[0]===qs[1]&&qs[1]===qs[2]&&qs[2]===qs[3]);
    var pc=(ps[0]===ps[1]&&ps[1]===ps[2]&&ps[2]===ps[3]);
    var line=(S.kind!==1);
    return {kind:S.kind,name:KINDS[S.kind],a:S.a,b:S.b,
            v:v.map(function(z){return r2(z);}).join(', '),
            q:qs.join(', '),p:ps.join(', '),qc:qc,pc:pc,line:line,
            verdict:qc?'정비례':(pc?'반비례':'둘 다 아님')};
  },
  headA:['번호','식','y 값','y ÷ x','일정?','x × y','일정?','판정','그래프가 직선?'],
  rowA:function(r,i){
    var eq=(r.kind===0)?('y='+r.a+'x'):((r.kind===1)?('y='+r.a+'/x'):('y='+r.a+'x+'+r.b));
    return [i+1,eq,r.v,r.q,
            '<span class="'+(r.qc?'ok':'no')+'">'+(r.qc?'○':'×')+'</span>',
            r.p,
            '<span class="'+(r.pc?'ok':'no')+'">'+(r.pc?'○':'×')+'</span>',
            '<b>'+r.verdict+'</b>',r.line?'○':'×'];
  },
  analyze:function(rec){
    var rows=[],lineN=0,lineProp=0,kinds={},kn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.line){ lineN++; if(r.qc) lineProp++; }
      kinds[r.kind]=true;
      var eq=(r.kind===0)?('y='+r.a+'x'):((r.kind===1)?('y='+r.a+'/x'):('y='+r.a+'x+'+r.b));
      rows.push([eq, r.v, r.q,
                 '<span class="'+(r.qc?'ok':'no')+'">'+(r.qc?'○':'×')+'</span>',
                 r.p,
                 '<span class="'+(r.pc?'ok':'no')+'">'+(r.pc?'○':'×')+'</span>',
                 '<b>'+r.verdict+'</b>', r.line?'직선':'곡선']);
    }
    for(var k in kinds) kn++;
    var stats=[
      {t:'그래프가 직선이었던 기록',big:lineN+'개',
       p:lineN?('그중 정비례였던 것 '+lineProp+'개.'):'직선이 되는 관계도 기록해 보자.'},
      {t:'시험한 관계의 종류',big:kn+'가지',p:kn>2?'세 관계를 모두 확인했다.':'세 가지 관계를 모두 기록해 보자.'},
      {t:'전체 기록',big:rec.length+'개',p:'판정은 표의 y÷x, x×y가 일정한지로 한다.'}
    ];
    var concl;
    if(kn<3){
      concl='<b>더 해 보자</b> — y = ax, y = a/x, y = ax + b <b>세 가지를 모두</b> 기록해야 비교할 수 있다.';
    } else if(lineProp<lineN){
      concl='<b>정리</b> — y = ax + b도 그래프는 <b>직선</b>이었지만 y ÷ x가 일정하지 않아 정비례가 아니었다. '
           +'그래프 모양만으로는 판단할 수 없다. <b>y ÷ x가 일정하면 정비례, x × y가 일정하면 반비례</b>이고, '
           +'정비례 그래프는 반드시 원점을 지난다.';
    } else {
      concl='<b>정리</b> — 표의 y÷x와 x×y로 관계를 판정했다. y = ax + b 형태도 기록해 직선이지만 정비례가 아닌 경우를 확인해 보자.';
    }
    return {head:['식','y 값','y÷x','일정?','x×y','일정?','판정','그래프'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("m1_like_terms_lab.html",
     "동류항 실험실 — 3a + 2b는 5ab일까?",
     "동류항 실험실 — 3a + 2b는 5ab일까?",
     "문자에 여러 값을 넣어 두 계산의 값을 비교하고, 타일 모델로 왜 합칠 수 없는지 확인한다.",
     LAB_LIKE),
    ("m1_equation_property_lab.html",
     "등식 실험실 — 한쪽에만 하면 안 될까?",
     "등식 실험실 — 한쪽에만 하면 안 될까?",
     "저울 양변에 같은 조작과 한쪽만 하는 조작을 비교하며 등식이 유지되는 조건을 기록한다.",
     LAB_EQ),
    ("m1_transposition_lab.html",
     "이항 실험실 — 넘어가면 왜 부호가 바뀔까?",
     "이항 실험실 — 넘어가면 왜 부호가 바뀔까?",
     "상수항을 옮겨 방정식을 풀고, 부호를 바꾼 답과 그대로 옮긴 답을 각각 검산해 기록한다.",
     LAB_MOVE),
    ("m1_coordinate_plane_lab.html",
     "좌표평면 실험실 — (a, b)와 (b, a)는 같은 점일까?",
     "좌표평면 실험실 — (a, b)와 (b, a)는 같은 점일까?",
     "두 수의 순서를 바꿔 점을 찍고, 위치와 사분면이 어떻게 달라지는지 기록한다.",
     LAB_COORD),
    ("m1_proportion_graph_lab.html",
     "정비례 실험실 — 그래프가 직선이면 정비례일까?",
     "정비례 실험실 — 그래프가 직선이면 정비례일까?",
     "세 가지 관계의 표를 만들어 y÷x와 x×y가 일정한지 확인하고, 그래프 모양과 비교한다.",
     LAB_PROP2),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c10_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
