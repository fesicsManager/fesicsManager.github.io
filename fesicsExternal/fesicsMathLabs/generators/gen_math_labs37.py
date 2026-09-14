# -*- coding: utf-8 -*-
"""중1 보강 6종"""
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
# 1. 소인수분해로 최대공약수·최소공배수
# ============================================================
LAB_GL = BASE + r"""
function fac(n){
  var f={},p=2,m=n;
  while(p*p<=m){ while(m%p===0){ f[p]=(f[p]||0)+1; m/=p; } p++; }
  if(m>1) f[m]=(f[m]||0)+1;
  return f;
}
function fstr(f){
  var k,s=[];
  for(k in f){ s.push(k+(f[k]>1?('^'+f[k]):'')); }
  return s.join(' × ')||'1';
}
var LAB = {
  cw:440, ch:430, cvTitle:'소인수 지수표',
  action:'소인수로 쪼개기',
  hint0:'두 수를 정하고, 소인수의 지수를 견주어 보자.',
  sliders:[
    {id:'a',label:'첫 번째 수',min:4,max:60,value:24,color:'#2563eb',unit:''},
    {id:'b',label:'두 번째 수',min:4,max:60,value:36,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var fa=fac(S.a), fb=fac(S.b);
    var ps={},k;
    for(k in fa) ps[k]=1;
    for(k in fb) ps[k]=1;
    var keys=[];
    for(k in ps) keys.push(parseInt(k,10));
    keys.sort(function(x,y){return x-y;});
    var g=1,l=1,i;
    for(i=0;i<keys.length;i++){
      var p=keys[i], ea=fa[p]||0, eb=fb[p]||0;
      g*=Math.pow(p,Math.min(ea,eb));
      l*=Math.pow(p,Math.max(ea,eb));
    }
    return {fa:fa,fb:fb,keys:keys,g:g,l:l,prod:S.a*S.b};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'최대공약수',v:ran?c.g:'쪼개 보자'},
            {k:'최소공배수',v:ran?c.l:'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '최대공약수 '+c.g+', 최소공배수 '+c.l+'.  둘을 곱하면 '+(c.g*c.l)+', 두 수의 곱은 '+c.prod+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*c.keys.length);
    lbl(ctx,S.a+' = '+fstr(c.fa),24,38,'#1d4ed8',18);
    lbl(ctx,S.b+' = '+fstr(c.fb),24,66,'#b91c1c',18);
    var X0=70, Y0=104, CW=Math.min(78,340/Math.max(1,c.keys.length));
    var rows=['소인수',S.a+'의 지수',S.b+'의 지수','작은 쪽','큰 쪽'];
    for(i=0;i<5;i++){
      lbl(ctx,rows[i],X0-8,Y0+i*34+22,'#475569',13,'right');
    }
    for(i=0;i<c.keys.length;i++){
      var p=c.keys[i], ea=c.fa[p]||0, eb=c.fb[p]||0;
      var on=(i<shown);
      var vals=[''+p,''+ea,''+eb,''+Math.min(ea,eb),''+Math.max(ea,eb)];
      var cols=['#1f2937','#1d4ed8','#b91c1c','#15803d','#b45309'];
      for(var j=0;j<5;j++){
        var x=X0+i*CW, y=Y0+j*34;
        ctx.fillStyle=(j===0)?'#eef4fc':((j>=3)?'#f8fafc':'#fff');
        ctx.fillRect(x,y,CW-4,30);
        ctx.strokeStyle='#cbd5e1';ctx.lineWidth=1.2;ctx.strokeRect(x,y,CW-4,30);
        if(on){
          ctx.fillStyle=cols[j];ctx.font='bold 15px sans-serif';ctx.textAlign='center';
          ctx.fillText(vals[j],x+(CW-4)/2,y+20);
        }
      }
    }
    ctx.textAlign='left';
    box(ctx,20,288,400,130);
    lbl(ctx,(t===null)?'작은 쪽과 큰 쪽을 곱하면?':('최대공약수 = '+c.g+'      최소공배수 = '+c.l),38,320,'#1f2937',18);
    lbl(ctx,(t===null)?'':('최대공약수 × 최소공배수 = '+(c.g*c.l)),38,356,'#15803d',18);
    lbl(ctx,'두 수의 곱 = '+S.a+' × '+S.b+' = '+c.prod,38,390,'#52627a',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,fa:fstr(c.fa),fb:fstr(c.fb),
            g:c.g,l:c.l,gl:c.g*c.l,prod:c.prod,
            ok:(c.g*c.l===c.prod),
            coprime:(c.g===1),
            lProd:(c.l===c.prod)};
  },
  headA:['번호','두 수','소인수분해','최대공약수','최소공배수','둘의 곱','두 수의 곱','같나?','서로소?'],
  rowA:function(r,i){
    return [i+1,r.a+', '+r.b,r.fa+' / '+r.fb,'<b>'+r.g+'</b>','<b>'+r.l+'</b>',r.gl,r.prod,
            '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
            r.coprime?'○':'×'];
  },
  analyze:function(rec){
    var rows=[],ok=0,cop=0,copL=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.ok) ok++;
      if(r.coprime){ cop++; if(r.lProd) copL++; }
      rows.push([r.a+', '+r.b, r.fa+' / '+r.fb, '<b>'+r.g+'</b>', '<b>'+r.l+'</b>',
                 r.gl+' / '+r.prod,
                 '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
                 r.coprime?'○':'×']);
    }
    var stats=[
      {t:'최대공약수 × 최소공배수 = 두 수의 곱',big:ok+' / '+rec.length,
       p:'지수의 작은 쪽과 큰 쪽을 더하면 원래 지수가 되기 때문이다.'},
      {t:'서로소였던 기록',big:cop+'개',
       p:cop?('그중 최소공배수가 두 수의 곱과 같았던 것 '+copL+'개.'):'서로소인 두 수도 기록해 보자.'},
      {t:'전체 기록',big:rec.length+'개',p:'공통 소인수의 지수를 견주는 것이 핵심이다.'}
    ];
    var concl;
    if(ok===rec.length){
      concl='<b>정리</b> — 소인수의 지수를 나란히 놓고 <b>작은 쪽만 모으면 최대공약수, 큰 쪽만 모으면 최소공배수</b>였다. '
           +'같은 소인수에서 작은 지수와 큰 지수를 더하면 두 지수의 합이 되므로, '
           +'<b>최대공약수 × 최소공배수 = 두 수의 곱</b>이 예외 없이 성립했다. '
           +(cop?'서로소일 때는 공통 소인수가 없어 최대공약수가 1이고 최소공배수가 곧 두 수의 곱이 된다.':'');
    } else {
      concl='<b>확인 필요</b> — 관계가 어긋난 기록이 있다.';
    }
    return {head:['두 수','소인수분해','최대공약수','최소공배수','곱 비교','같나?','서로소?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 계산 순서
# ============================================================
LAB_ORDER = BASE + r"""
var KINDS=['a + b × c','a − b + c','a ÷ b × c'];
var LAB = {
  cw:440, ch:400, cvTitle:'계산 순서 판',
  action:'두 순서로 계산하기',
  hint0:'식의 모양과 세 수를 정해 보자.',
  sliders:[
    {id:'kind',label:'식',min:0,max:2,value:0,color:'#2563eb',fmt:function(v){return KINDS[v];}},
    {id:'a',label:'a',min:1,max:12,value:2,color:'#16a34a',unit:''},
    {id:'b',label:'b',min:1,max:12,value:3,color:'#f59e0b',unit:''},
    {id:'c',label:'c',min:1,max:12,value:4,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var right,left,rs,ls;
    if(S.kind===0){
      right=S.a+S.b*S.c; left=(S.a+S.b)*S.c;
      rs='먼저 '+S.b+'×'+S.c+' = '+(S.b*S.c); ls='먼저 '+S.a+'+'+S.b+' = '+(S.a+S.b);
    } else if(S.kind===1){
      right=S.a-S.b+S.c; left=S.a-(S.b+S.c);
      rs='앞에서부터 '+S.a+'−'+S.b+' = '+(S.a-S.b); ls='뒤를 먼저 '+S.b+'+'+S.c+' = '+(S.b+S.c);
    } else {
      right=S.a/S.b*S.c; left=S.a/(S.b*S.c);
      rs='앞에서부터 '+S.a+'÷'+S.b+' = '+r3(S.a/S.b); ls='뒤를 먼저 '+S.b+'×'+S.c+' = '+(S.b*S.c);
    }
    return {right:right,left:left,rs:rs,ls:ls,same:(Math.abs(right-left)<1e-9)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'식',v:S.a+' '+KINDS[S.kind].replace('a','').replace('b','').replace('c','').trim()},
            {k:'바른 계산',v:ran?r3(c.right):'계산해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '바른 계산 '+r3(c.right)+', 다른 순서로 하면 '+r3(c.left)+'.  '+(c.same?'우연히 같다.':'다르다.')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var expr;
    if(S.kind===0) expr=S.a+' + '+S.b+' × '+S.c;
    else if(S.kind===1) expr=S.a+' − '+S.b+' + '+S.c;
    else expr=S.a+' ÷ '+S.b+' × '+S.c;
    var p1=(t===null)?0:Math.min(1,t/0.5);
    var p2=(t===null)?0:Math.max(0,(t-0.5)/0.5);
    lbl(ctx,expr,40,86,'#1f2937',30);
    if(p1>0){
      ctx.globalAlpha=p1;
      lbl(ctx,'바른 순서',40,132,'#15803d',17);
      lbl(ctx,c.rs,40,164,'#334155',17);
      lbl(ctx,'= '+r3(c.right),40,200,'#15803d',24);
      ctx.globalAlpha=1;
    }
    if(p2>0){
      ctx.globalAlpha=p2;
      lbl(ctx,'다른 순서',250,132,'#b91c1c',17);
      lbl(ctx,c.ls,250,164,'#334155',15);
      lbl(ctx,'= '+r3(c.left),250,200,'#b91c1c',24);
      ctx.globalAlpha=1;
    }
    lbl(ctx,'순서를 바꾸면 답이 달라질까?',24,38,'#1d4ed8',18);
    box(ctx,20,224,400,160);
    lbl(ctx,(t===null)?'어느 것을 먼저 계산해야 할까?':('바른 계산 = '+r3(c.right)),38,258,'#1f2937',19);
    lbl(ctx,(t===null)?'':('다른 순서 = '+r3(c.left)),38,294,'#b91c1c',19);
    lbl(ctx,(t===null)?'':(c.same?'두 값이 같다':'두 값이 다르다'),38,330,c.same?'#b45309':'#15803d',18);
    lbl(ctx,(S.kind===0)?'곱셈·나눗셈이 덧셈·뺄셈보다 먼저':'같은 단계면 왼쪽부터 차례로',38,366,'#52627a',15);
  },
  record:function(S){
    var c=this.calc(S);
    return {kind:S.kind,name:KINDS[S.kind],a:S.a,b:S.b,c:S.c,
            right:r3(c.right),left:r3(c.left),same:c.same,
            one:(S.b===1||S.c===1||S.a===0)};
  },
  headA:['번호','식','a, b, c','바른 계산','다른 순서','같나?'],
  rowA:function(r,i){
    return [i+1,r.name,r.a+', '+r.b+', '+r.c,'<b>'+r.right+'</b>',r.left,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,sameTriv=0,g={},kn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same){ same++; if(r.one) sameTriv++; }
      if(!g[r.kind]){ g[r.kind]=true; kn++; }
      rows.push([r.name, r.a+', '+r.b+', '+r.c, '<b>'+r.right+'</b>', r.left,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'두 순서의 결과가 같았던 횟수',big:same+' / '+rec.length,
       p:same?('그중 1이 섞여 특별했던 것 '+sameTriv+'개.'):'순서를 바꾸면 대개 답이 달라진다.'},
      {t:'시험한 식의 모양',big:kn+'가지',p:'세 가지를 모두 기록해 보자.'},
      {t:'전체 기록',big:rec.length+'개',p:'괄호가 없으면 순서 규칙이 답을 정한다.'}
    ];
    var concl;
    if(kn<3){
      concl='<b>더 해 보자</b> — 세 가지 식 모양을 <b>모두</b> 기록해 보자.';
    } else if(same===sameTriv){
      concl='<b>정리</b> — 계산 순서를 바꾸면 답이 달라졌다. 우연히 같아진 것은 1이 섞인 특별한 경우뿐이었다. '
           +'<b>곱셈·나눗셈을 덧셈·뺄셈보다 먼저</b> 하고, 같은 단계끼리는 <b>왼쪽부터 차례로</b> 한다. '
           +'특히 a − b + c 를 a − (b+c) 로, a ÷ b × c 를 a ÷ (b×c) 로 묶어 버리는 실수가 잦다. '
           +'뺄셈과 나눗셈은 «뒤를 몰아서» 처리하면 안 된다.';
    } else {
      concl='<b>정리</b> — 순서를 바꾸면 대개 답이 달라졌다. 값을 더 바꿔 가며 확인해 보자.';
    }
    return {head:['식','a, b, c','바른 계산','다른 순서','같나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 절댓값과 거리
# ============================================================
LAB_ABS = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'절댓값 수직선판',
  action:'수직선에서 재기',
  hint0:'두 수를 정하고, 절댓값과 두 점 사이 거리를 재 보자.',
  sliders:[
    {id:'a',label:'a',min:-10,max:10,value:-6,color:'#2563eb',unit:''},
    {id:'b',label:'b',min:-10,max:10,value:3,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    return {aa:Math.abs(S.a),ab:Math.abs(S.b),
            d:Math.abs(S.a-S.b),
            diff:Math.abs(S.a)-Math.abs(S.b),
            absdiff:Math.abs(Math.abs(S.a)-Math.abs(S.b)),
            sum:Math.abs(S.a)+Math.abs(S.b)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'|a| , |b|',v:c.aa+' , '+c.ab},
            {k:'|a − b|',v:ran?c.d:'재 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '|a − b| = '+c.d+'이고 수직선에서 두 점 사이 거리도 '+c.d+'다. |a| − |b| = '+c.diff+'와 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var X0=34, X1=406, LO=-11, HI=11;
    function px(v){ return X0+(X1-X0)*(v-LO)/(HI-LO); }
    var Y=170;
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(X0,Y);ctx.lineTo(X1,Y);ctx.stroke();
    for(i=-10;i<=10;i++){
      var x=px(i), big=(i%5===0);
      ctx.beginPath();ctx.moveTo(x,Y-(big?8:4));ctx.lineTo(x,Y+(big?8:4));
      ctx.strokeStyle=big?'#64748b':'#cbd5e1';ctx.lineWidth=big?1.8:1;ctx.stroke();
      if(big){ ctx.fillStyle='#94a3b8';ctx.font='12px sans-serif';ctx.textAlign='center';ctx.fillText(i,x,Y+24); }
    }
    ctx.textAlign='left';
    var grow=(t===null)?0:Math.min(1,t);
    ctx.strokeStyle='#93c5fd';ctx.lineWidth=5;
    ctx.beginPath();ctx.moveTo(px(0),Y-18);ctx.lineTo(px(S.a),Y-18);ctx.stroke();
    ctx.strokeStyle='#fca5a5';
    ctx.beginPath();ctx.moveTo(px(0),Y-32);ctx.lineTo(px(S.b),Y-32);ctx.stroke();
    lbl(ctx,'|a| = '+c.aa,px(S.a/2),Y-24,'#1d4ed8',13,'center');
    lbl(ctx,'|b| = '+c.ab,px(S.b/2),Y-38,'#b91c1c',13,'center');
    if(grow>0){
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=6;
      ctx.beginPath();ctx.moveTo(px(S.a),Y+20);
      ctx.lineTo(px(S.a)+(px(S.b)-px(S.a))*grow,Y+20);ctx.stroke();
      if(grow>=1) lbl(ctx,'거리 '+c.d,px((S.a+S.b)/2),Y+42,'#b45309',15,'center');
    }
    [[S.a,'a','#2563eb'],[S.b,'b','#dc2626']].forEach(function(q){
      ctx.beginPath();ctx.arc(px(q[0]),Y,7,0,Math.PI*2);
      ctx.fillStyle=q[2];ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      lbl(ctx,q[1]+' = '+q[0],px(q[0]),Y-48,q[2],13,'center');
    });
    lbl(ctx,'절댓값은 0에서 떨어진 거리',24,32,'#52627a',15);
    box(ctx,20,248,400,136);
    lbl(ctx,'|a| = '+c.aa+'      |b| = '+c.ab,38,280,'#52627a',17);
    lbl(ctx,(t===null)?'두 점 사이 거리는?':('|a − b| = '+c.d+'   (수직선 거리와 같다)'),38,314,'#1f2937',18);
    lbl(ctx,(t===null)?'':('|a| − |b| = '+c.diff+'      ||a| − |b|| = '+c.absdiff),38,348,'#b91c1c',17);
    lbl(ctx,(t===null)?'':('|a| + |b| = '+c.sum),38,376,'#52627a',15);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,aa:c.aa,ab:c.ab,d:c.d,diff:c.diff,absdiff:c.absdiff,sum:c.sum,
            eqDiff:(c.d===c.absdiff),
            eqSum:(c.d===c.sum),
            sameSign:((S.a>=0&&S.b>=0)||(S.a<=0&&S.b<=0)),
            aNeg:(S.a<0),aEq:(Math.abs(S.a)===S.a)};
  },
  headA:['번호','a, b','|a|','|b|','|a−b|','||a|−|b||','같나?','|a|+|b|','같나?','같은 부호?'],
  rowA:function(r,i){
    return [i+1,r.a+', '+r.b,r.aa,r.ab,'<b>'+r.d+'</b>',r.absdiff,
            '<span class="'+(r.eqDiff?'ok':'no')+'">'+(r.eqDiff?'○':'×')+'</span>',
            r.sum,
            '<span class="'+(r.eqSum?'ok':'no')+'">'+(r.eqSum?'○':'×')+'</span>',
            r.sameSign?'○':'×'];
  },
  analyze:function(rec){
    var rows=[],same=0,sameEq=0,diff=0,diffEq=0,neg=0,negEq=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.sameSign){ same++; if(r.eqDiff) sameEq++; }
      else { diff++; if(r.eqSum) diffEq++; }
      if(r.aNeg){ neg++; if(r.aEq) negEq++; }
      rows.push([r.a+', '+r.b, r.aa+' / '+r.ab, '<b>'+r.d+'</b>', r.absdiff,
                 '<span class="'+(r.eqDiff?'ok':'no')+'">'+(r.eqDiff?'○':'×')+'</span>',
                 r.sum,
                 '<span class="'+(r.eqSum?'ok':'no')+'">'+(r.eqSum?'○':'×')+'</span>',
                 r.sameSign?'같음':'다름']);
    }
    var stats=[
      {t:'부호가 같았던 기록',big:same+'개',
       p:same?('그중 |a−b| = ||a|−|b|| 였던 것 '+sameEq+'개.'):'같은 부호인 두 수도 기록해 보자.'},
      {t:'부호가 달랐던 기록',big:diff+'개',
       p:diff?('그중 |a−b| = |a|+|b| 였던 것 '+diffEq+'개.'):'부호가 다른 두 수도 기록해 보자.'},
      {t:'a가 음수였던 기록',big:neg+'개',
       p:neg?('그중 |a| = a 였던 것 '+negEq+'개.'):'a를 음수로도 해 보자.'}
    ];
    var concl;
    if(same===0||diff===0){
      concl='<b>더 해 보자</b> — 두 수의 부호가 <b>같은 경우와 다른 경우</b>를 모두 기록해 보자.';
    } else if(sameEq===same&&diffEq===diff&&negEq===0){
      concl='<b>정리</b> — |a − b| 는 언제나 수직선에서 <b>두 점 사이의 거리</b>였다. '
           +'부호가 같으면 두 절댓값의 차, 다르면 두 절댓값의 합과 일치했다. '
           +'|a| − |b| 는 이 거리와 다른 값이고, 음수가 되기도 한다(거리는 음수가 될 수 없다). '
           +'또 a가 음수일 때 |a| = a 인 경우는 없었다. 절댓값은 «부호를 떼는 것»이 아니라 «0에서 떨어진 거리»다.';
    } else {
      concl='<b>정리</b> — |a − b| 는 두 점 사이 거리였다. 부호 조합을 더 바꿔 가며 확인해 보자.';
    }
    return {head:['a, b','|a| / |b|','|a−b|','||a|−|b||','같나?','|a|+|b|','같나?','부호'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 계수와 제곱
# ============================================================
LAB_COEF = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'계수와 제곱 판',
  action:'값을 넣어 비교하기',
  hint0:'계수와 x에 넣을 값을 정하고, 두 식을 비교해 보자.',
  sliders:[
    {id:'a',label:'계수 a',min:1,max:5,value:3,color:'#2563eb',unit:''},
    {id:'x',label:'x에 넣을 값',min:-5,max:5,value:2,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var v1=S.a*S.x*S.x;
    var v2=(S.a*S.x)*(S.a*S.x);
    return {v1:v1,v2:v2,ratio:(v1===0)?null:(v2/v1),same:(v1===v2)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'a x²',v:ran?c.v1:'계산해 보자'},
            {k:'(a x)²',v:ran?c.v2:'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'a x² = '+c.v1+', (a x)² = '+c.v2+'.  '+(c.same?'우연히 같다.':('두 번째가 '+((c.ratio===null)?'-':c.ratio)+'배 크다.'))+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var ax=Math.abs(S.x);
    var u=Math.min(26, 150/Math.max(1,S.a*ax));
    var grow=(t===null)?0:Math.min(1,t);
    lbl(ctx,'a = '+S.a+',  x = '+S.x,24,32,'#1d4ed8',18);
    lbl(ctx,'a x²  =  '+S.a+'개의 '+ax+'×'+ax+' 정사각형',24,64,'#52627a',15);
    var X0=40, Y0=90;
    for(i=0;i<S.a;i++){
      if(grow<0.15) break;
      var x=X0+i*(ax*u+8);
      if(x+ax*u>420) break;
      ctx.fillStyle='rgba(37,99,235,0.25)';
      ctx.fillRect(x,Y0,ax*u,ax*u);
      ctx.strokeStyle='#2563eb';ctx.lineWidth=2;ctx.strokeRect(x,Y0,ax*u,ax*u);
    }
    lbl(ctx,'(a x)²  =  한 변이 '+S.a+'×'+ax+' = '+(S.a*ax)+' 인 정사각형',24,Y0+ax*u+34,'#52627a',15);
    if(grow>0.5){
      var s=S.a*ax*u;
      var sc=Math.min(1,150/(S.a*ax*u));
      ctx.fillStyle='rgba(220,38,38,0.20)';
      ctx.fillRect(X0,Y0+ax*u+46,s*sc,s*sc);
      ctx.strokeStyle='#dc2626';ctx.lineWidth=2;ctx.strokeRect(X0,Y0+ax*u+46,s*sc,s*sc);
    }
    box(ctx,20,326,400,92);
    lbl(ctx,(t===null)?'두 식은 같을까?':('a x² = '+S.a+' × '+(S.x*S.x)+' = '+c.v1),38,358,'#1d4ed8',18);
    lbl(ctx,(t===null)?'':('(a x)² = '+(S.a*S.x)+'² = '+c.v2),38,390,'#b91c1c',18);
    lbl(ctx,(t===null)?'':((c.ratio===null)?'':('두 번째가 '+c.ratio+'배 = a배')),38,412,'#52627a',15);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,x:S.x,v1:c.v1,v2:c.v2,
            ratio:(c.ratio===null)?'-':c.ratio,
            same:c.same,
            aOne:(S.a===1),xZero:(S.x===0),
            ratioA:(c.ratio!==null&&Math.abs(c.ratio-S.a)<1e-9)};
  },
  headA:['번호','a','x','a x²','(a x)²','같나?','두 번째 ÷ 첫 번째','a와 같나?'],
  rowA:function(r,i){
    return [i+1,r.a,r.x,'<b>'+r.v1+'</b>',r.v2,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            r.ratio,
            '<span class="'+(r.ratioA?'ok':'no')+'">'+(r.ratioA?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,triv=0,ra=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same){ same++; if(r.aOne||r.xZero) triv++; }
      if(r.ratioA) ra++;
      rows.push([r.a, r.x, '<b>'+r.v1+'</b>', r.v2,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 r.ratio,
                 '<span class="'+(r.ratioA?'ok':'no')+'">'+(r.ratioA?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'두 식의 값이 같았던 횟수',big:same+' / '+rec.length,
       p:same?('그중 a = 1 이거나 x = 0 이었던 것 '+triv+'개.'):'a와 x를 여러 값으로 바꿔 확인했다.'},
      {t:'(a x)² ÷ a x² = a',big:ra+' / '+rec.length,
       p:'차이가 정확히 a배인지 확인한 결과.'},
      {t:'전체 기록',big:rec.length+'개',p:'a x² 에서 제곱은 x에만 걸려 있다.'}
    ];
    var concl;
    if(same===triv&&ra>0){
      concl='<b>정리</b> — a x² 에서 <b>제곱은 x에만 걸린다.</b> 계수 a는 제곱되지 않는다. '
           +'그래서 (a x)² 은 a x² 의 정확히 <b>a배</b>가 되었고, 두 값이 같아진 것은 a = 1 이거나 x = 0 일 때뿐이었다. '
           +'그림으로 보면 a x² 은 «작은 정사각형 a개»이고, (a x)² 은 «한 변이 a배인 큰 정사각형 하나»다.';
    } else {
      concl='<b>정리</b> — 두 식은 대개 달랐다. a와 x를 더 바꿔 가며 배수 관계를 확인해 보자.';
    }
    return {head:['a','x','a x²','(a x)²','같나?','비','a와 같나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 반비례 그래프
# ============================================================
LAB_INV = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'반비례 그래프판',
  action:'점을 찍어 보기',
  hint0:'상수 a와 확인할 x를 정해 보자. y = a / x 이다.',
  sliders:[
    {id:'a',label:'상수 a',min:-12,max:12,value:6,color:'#2563eb',unit:''},
    {id:'x0',label:'확인할 x (÷2)',min:-12,max:12,value:4,color:'#dc2626',
     fmt:function(v){return (v/2).toFixed(1);}}
  ],
  calc:function(S){
    var x=S.x0/2;
    if(S.a===0) return {zero:true};
    if(x===0) return {zero:false,undef:true,x:x};
    var y=S.a/x;
    return {zero:false,undef:false,x:x,y:y,prod:x*y,
            q:(x>0&&y>0)?1:((x<0&&y>0)?2:((x<0&&y<0)?3:4))};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    if(c.zero) return [{k:'a = 0',v:'반비례가 아니다'},{k:'',v:'a를 바꾸자'}];
    if(c.undef) return [{k:'x = 0',v:'y를 정할 수 없다'},{k:'',v:'x를 바꾸자'}];
    return [{k:'y = a / x',v:ran?r3(c.y):'찍어 보자'},
            {k:'x × y',v:ran?r3(c.prod):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.zero) return 'a = 0 이면 반비례가 아니다.';
    if(c.undef) return 'x = 0 에서는 a를 0으로 나눌 수 없어 y가 없다. 다른 x로 해 보자.';
    return 'x = '+c.x+' 일 때 y = '+r3(c.y)+', x × y = '+r3(c.prod)+'다. 다른 x로도 해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,8,7);
    if(c.zero){ lbl(ctx,'a = 0 이면 반비례가 아니다',24,32,'#b91c1c',18); return; }
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;
    [1,-1].forEach(function(s){
      ctx.beginPath();
      var st=false;
      for(i=1;i<=160;i++){
        var x=s*i/20;
        var y=S.a/x;
        if(Math.abs(y)>7||Math.abs(x)>8){ st=false; continue; }
        if(!st){ ctx.moveTo(CX+x*U,CY-y*U); st=true; } else ctx.lineTo(CX+x*U,CY-y*U);
      }
      ctx.stroke();
    });
    ctx.strokeStyle='#f59e0b';ctx.lineWidth=2;ctx.setLineDash([4,4]);
    ctx.beginPath();ctx.moveTo(CX,CY-7*U);ctx.lineTo(CX,CY+7*U);ctx.stroke();ctx.setLineDash([]);
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0&&!c.undef&&Math.abs(c.y)<=7&&Math.abs(c.x)<=8){
      ctx.beginPath();ctx.arc(CX+c.x*U,CY-c.y*U,7,0,Math.PI*2);
      ctx.fillStyle='#dc2626';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      ctx.strokeStyle='#94a3b8';ctx.lineWidth=1.4;ctx.setLineDash([3,3]);
      ctx.beginPath();ctx.moveTo(CX+c.x*U,CY);ctx.lineTo(CX+c.x*U,CY-c.y*U);
      ctx.lineTo(CX,CY-c.y*U);ctx.stroke();ctx.setLineDash([]);
    }
    ctx.beginPath();ctx.arc(CX,CY,5,0,Math.PI*2);ctx.fillStyle='#94a3b8';ctx.fill();
    lbl(ctx,'y = '+S.a+' / x      주황 점선 = y축',24,32,'#1d4ed8',16);
    box(ctx,20,346,400,74);
    if(c.undef){
      lbl(ctx,'x = 0 에서는 y를 정할 수 없다',38,382,'#b91c1c',20);
      return;
    }
    lbl(ctx,(t===null)?'x × y 는 얼마일까?':('점 ( '+c.x+' , '+r3(c.y)+' )      x × y = '+r3(c.prod)),38,376,'#1f2937',17);
    lbl(ctx,(t===null)?'':('제'+c.q+'사분면      그래프는 y축과 만나지 않는다'),38,406,'#52627a',16);
  },
  record:function(S){
    var c=this.calc(S);
    if(c.zero) return {zero:true};
    if(c.undef) return {undef:true,a:S.a,x:c.x};
    return {zero:false,undef:false,a:S.a,x:c.x,y:r3(c.y),prod:r3(c.prod),q:c.q,
            prodA:(Math.abs(c.prod-S.a)<1e-9),
            origin:(Math.abs(c.x)<1e-9&&Math.abs(c.y)<1e-9)};
  },
  headA:['번호','a','x','y','x × y','a와 같나?','사분면','원점을 지나나?'],
  rowA:function(r,i){
    if(r.zero) return [i+1,'0','-','-','-','-','-','-'];
    if(r.undef) return [i+1,r.a,'0','정할 수 없음','-','-','-','-'];
    return [i+1,r.a,r.x,'<b>'+r.y+'</b>',r.prod,
            '<span class="'+(r.prodA?'ok':'no')+'">'+(r.prodA?'○':'×')+'</span>',
            '제'+r.q,
            '<span class="'+(r.origin?'ok':'no')+'">'+(r.origin?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],valid=0,pa=0,undef=0,org=0,qs={},qn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.zero){ rows.push(['a=0','-','-','-','-']); continue; }
      if(r.undef){ undef++; rows.push([r.a,'0','정할 수 없음','-','-']); continue; }
      valid++;
      if(r.prodA) pa++;
      if(r.origin) org++;
      if(!qs[r.q]){ qs[r.q]=true; qn++; }
      rows.push([r.a, r.x, '<b>'+r.y+'</b>', r.prod,
                 '<span class="'+(r.prodA?'ok':'no')+'">'+(r.prodA?'○':'×')+'</span>',
                 '제'+r.q]);
    }
    var stats=[
      {t:'x × y = a',big:pa+' / '+valid,p:'x를 바꿔도 곱이 일정한지 확인한 결과.'},
      {t:'x = 0 을 넣은 기록',big:undef+'개',
       p:undef?'0으로 나눌 수 없어 y가 정해지지 않는다.':'x = 0 도 넣어 보자.'},
      {t:'원점을 지난 기록',big:org+'개',
       p:'나타난 사분면 '+qn+'가지. 반비례 그래프는 원점을 지나지 않는다.'}
    ];
    var concl;
    if(undef===0){
      concl='<b>더 해 보자</b> — <b>x = 0</b> 을 넣어 보자. 정비례와 무엇이 다른지가 거기서 갈린다.';
    } else if(pa===valid&&org===0){
      concl='<b>정리</b> — 반비례에서는 x가 달라져도 <b>x × y 가 언제나 a</b>로 일정했다. '
           +'하지만 <b>x = 0 에서는 y를 정할 수 없어</b> 그래프가 y축과 만나지 않고, <b>원점도 지나지 않았다.</b> '
           +'그래서 그래프가 두 갈래로 끊겨 있다. 원점을 지나는 직선인 정비례와 가장 크게 다른 점이다.';
    } else {
      concl='<b>정리</b> — x × y 가 일정했다. x = 0 근처와 부호를 바꿔 가며 더 확인해 보자.';
    }
    return {head:['a','x','y','x×y','a와 같나?','사분면'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 6. 그래프 위의 점
# ============================================================
LAB_ONGRAPH = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'그래프 위의 점 판',
  action:'대입해 확인하기',
  hint0:'그래프 y = ax 의 a와, 확인할 점을 정해 보자.',
  sliders:[
    {id:'a',label:'a',min:-4,max:4,value:2,color:'#2563eb',unit:''},
    {id:'px',label:'점의 x좌표',min:-6,max:6,value:3,color:'#dc2626',unit:''},
    {id:'py',label:'점의 y좌표',min:-7,max:7,value:5,color:'#f87171',unit:''}
  ],
  calc:function(S){
    var v=S.a*S.px;
    return {v:v,on:(v===S.py),gap:Math.abs(v-S.py)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'a × (점의 x)',v:c.v},
            {k:'점의 y',v:ran?(S.py+(c.on?' — 같다':' — 다르다')):'대입해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'a × '+S.px+' = '+c.v+'이고 점의 y는 '+S.py+'다. '+(c.on?'같으므로 그래프 위의 점이다.':'다르므로 그래프 위의 점이 아니다.')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,7,7);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    var st=false;
    for(i=-70;i<=70;i++){
      var x=i/10, y=S.a*x;
      if(Math.abs(y)>7){ st=false; continue; }
      if(!st){ ctx.moveTo(CX+x*U,CY-y*U); st=true; } else ctx.lineTo(CX+x*U,CY-y*U);
    }
    ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      ctx.strokeStyle='#94a3b8';ctx.lineWidth=1.6;ctx.setLineDash([4,4]);
      ctx.beginPath();ctx.moveTo(CX+S.px*U,CY);ctx.lineTo(CX+S.px*U,CY-7*U);ctx.stroke();
      ctx.setLineDash([]);
      if(Math.abs(c.v)<=7){
        ctx.beginPath();ctx.arc(CX+S.px*U,CY-c.v*U,6,0,Math.PI*2);
        ctx.fillStyle='#2563eb';ctx.fill();
        lbl(ctx,'그래프의 y = '+c.v,CX+S.px*U+10,CY-c.v*U-10,'#1d4ed8',13);
      }
    }
    ctx.beginPath();ctx.arc(CX+S.px*U,CY-S.py*U,8,0,Math.PI*2);
    ctx.fillStyle=c.on?'#15803d':'#dc2626';ctx.fill();
    ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
    lbl(ctx,'('+S.px+', '+S.py+')',CX+S.px*U+12,CY-S.py*U+20,c.on?'#15803d':'#b91c1c',14);
    if(grow>=1&&!c.on&&Math.abs(c.v)<=7){
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=3;
      ctx.beginPath();ctx.moveTo(CX+S.px*U,CY-S.py*U);ctx.lineTo(CX+S.px*U,CY-c.v*U);ctx.stroke();
      lbl(ctx,'차이 '+c.gap,CX+S.px*U+10,CY-(S.py+c.v)/2*U,'#b45309',13);
    }
    lbl(ctx,'y = '+S.a+'x',24,32,'#1d4ed8',18);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'이 점은 그래프 위에 있을까?':('a × '+S.px+' = '+c.v+'      점의 y = '+S.py),38,376,'#1f2937',18);
    lbl(ctx,(t===null)?'':(c.on?'두 값이 같다 — 그래프 위의 점':('차이 '+c.gap+' — 그래프 위의 점이 아니다')),
        38,406,c.on?'#15803d':'#b91c1c',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,px:S.px,py:S.py,v:c.v,on:c.on,gap:c.gap,
            near:(c.gap>0&&c.gap<=1),
            origin:(S.px===0&&S.py===0)};
  },
  headA:['번호','y = ax','점','a × x','점의 y','차이','그래프 위?','원점?'],
  rowA:function(r,i){
    return [i+1,'y = '+r.a+'x','('+r.px+', '+r.py+')',r.v,r.py,r.gap,
            '<span class="'+(r.on?'ok':'no')+'">'+(r.on?'○':'×')+'</span>',
            r.origin?'○':'×'];
  },
  analyze:function(rec){
    var rows=[],on=0,near=0,org=0,orgOn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.on) on++;
      if(r.near) near++;
      if(r.origin){ org++; if(r.on) orgOn++; }
      rows.push(['y = '+r.a+'x', '('+r.px+', '+r.py+')', r.v, r.py, r.gap,
                 '<span class="'+(r.on?'ok':'no')+'">'+(r.on?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'그래프 위의 점이었던 기록',big:on+' / '+rec.length,
       p:'x좌표를 넣은 값과 y좌표가 같았던 경우.'},
      {t:'아슬아슬하게 빗나간 기록',big:near+'개',
       p:near?'차이가 1 이내라 눈으로는 구별하기 어렵다.':'차이가 1인 점도 넣어 보자.'},
      {t:'원점을 넣은 기록',big:org+'개',
       p:org?('그중 그래프 위였던 것 '+orgOn+'개. y = ax 는 언제나 원점을 지난다.'):'원점 (0, 0)도 넣어 보자.'}
    ];
    var concl;
    if(on===0||near===0){
      concl='<b>더 해 보자</b> — 그래프 위의 점과 <b>아슬아슬하게 빗나간 점</b>을 모두 넣어 보자. '
           +'y = 2x 라면 (3, 6)과 (3, 5)를 비교해 보면 된다.';
    } else {
      concl='<b>정리</b> — 어떤 점이 그래프 위에 있는지는 <b>x좌표를 식에 넣어 y좌표와 비교</b>해서 판정했다. '
           +'차이가 1뿐인 점은 그림에서 거의 붙어 보이지만 <b>그래프 위의 점이 아니다.</b> '
           +'눈대중이 아니라 대입이 판단 기준이다. '
           +(orgOn?'또 y = ax 는 a가 무엇이든 원점을 지났다.':'원점 (0, 0)도 넣어 확인해 보자.');
    }
    return {head:['식','점','a × x','점의 y','차이','그래프 위?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("m1_gcd_lcm_lab.html",
     "최대공약수 실험실 — 지수를 견주면 무엇이 나올까?",
     "최대공약수 실험실 — 지수를 견주면 무엇이 나올까?",
     "두 수를 소인수분해해 지수를 나란히 놓고, 최대공약수와 최소공배수를 만들어 본다.",
     LAB_GL),
    ("m1_operation_order_lab.html",
     "계산 순서 실험실 — 왼쪽부터 하면 될까?",
     "계산 순서 실험실 — 왼쪽부터 하면 될까?",
     "같은 식을 두 가지 순서로 계산해 값을 비교하고, 어느 쪽이 규칙인지 확인한다.",
     LAB_ORDER),
    ("m1_absolute_value_lab.html",
     "절댓값 실험실 — |a − b| 는 무엇을 나타낼까?",
     "절댓값 실험실 — |a − b| 는 무엇을 나타낼까?",
     "수직선에서 두 점 사이 거리를 재고, |a|−|b| 와 비교한다.",
     LAB_ABS),
    ("m1_coefficient_square_lab.html",
     "계수 실험실 — 3x² 과 (3x)² 은 같을까?",
     "계수 실험실 — 3x² 과 (3x)² 은 같을까?",
     "값을 대입해 두 식을 비교하고, 넓이 그림으로 차이를 확인한다.",
     LAB_COEF),
    ("m1_inverse_proportion_lab.html",
     "반비례 실험실 — 그래프가 왜 두 갈래일까?",
     "반비례 실험실 — 그래프가 왜 두 갈래일까?",
     "y = a/x 에서 x를 바꿔 가며 x × y 를 재고, x = 0 에서 무슨 일이 생기는지 확인한다.",
     LAB_INV),
    ("m1_point_on_graph_lab.html",
     "그래프 위의 점 실험실 — 눈으로 봐도 될까?",
     "그래프 위의 점 실험실 — 눈으로 봐도 될까?",
     "점의 x좌표를 식에 넣어 y좌표와 비교하며 그래프 위의 점인지 판정한다.",
     LAB_ONGRAPH),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c37_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
