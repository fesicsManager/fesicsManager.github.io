# -*- coding: utf-8 -*-
"""초등 5-6학년군 '도형과 측정' 실험 5종"""
import os, re

OUT = "/mnt/user-data/outputs"
src = open("/home/claude/gen_math_labs.py", encoding="utf-8").read()
TPL = re.search(r'TPL = r"""(.*?)"""\n', src, re.S).group(1)

BASE = r"""
function lbl(ctx,t,x,y,c,sz,al){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
function box(ctx,x,y,w,h){ctx.fillStyle='#f1f6fd';ctx.fillRect(x,y,w,h);ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(x,y,w,h);}
function r1(v){return Math.round(v*10)/10;}
function r2(v){return Math.round(v*100)/100;}
function shoelace(p){var s=0,i;for(i=0;i<p.length;i++){var a=p[i],b=p[(i+1)%p.length];s+=a[0]*b[1]-b[0]*a[1];}return Math.abs(s)/2;}
function perim(p){var s=0,i;for(i=0;i<p.length;i++){var a=p[i],b=p[(i+1)%p.length];s+=Math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]));}return s;}
function poly(ctx,p,fill,stroke,dash){
  ctx.beginPath();
  for(var i=0;i<p.length;i++){ if(i===0) ctx.moveTo(p[i][0],p[i][1]); else ctx.lineTo(p[i][0],p[i][1]); }
  ctx.closePath();
  if(dash) ctx.setLineDash([6,5]);
  if(fill){ctx.fillStyle=fill;ctx.fill();}
  ctx.strokeStyle=stroke;ctx.lineWidth=3;ctx.stroke();ctx.setLineDash([]);
}
"""

# ============================================================
# 1. 등적변형 — 평행사변형의 넓이
# ============================================================
LAB_PARA = BASE + r"""
var X0=90, Y0=90, SC=20;
function shape(b,h,s){
  return [[X0,Y0+h],[X0+b,Y0+h],[X0+b+s,Y0],[X0+s,Y0]];
}
var LAB = {
  cw:440, ch:400, cvTitle:'평행사변형 넓이판',
  action:'밀어서 직사각형 만들기',
  hint0:'밑변·높이·기울기를 정해 보자. 기울여도 넓이가 같을까?',
  sliders:[
    {id:'b',label:'밑변',min:40,max:200,value:120,color:'#2563eb',fmt:function(v){return (v/20).toFixed(1)+'cm';}},
    {id:'h',label:'높이',min:30,max:170,value:100,color:'#16a34a',fmt:function(v){return (v/20).toFixed(1)+'cm';}},
    {id:'s',label:'기울인 정도',min:-100,max:100,value:70,color:'#f59e0b',fmt:function(v){return (v/20).toFixed(1)+'cm';}}
  ],
  readout:function(S,ran){
    var p=shape(S.b,S.h,S.s);
    return [{k:'넓이',v:r2(shoelace(p)/400)+'cm²'},
            {k:'둘레',v:r2(perim(p)/20)+'cm'}];
  },
  doneMsg:function(S){
    var p=shape(S.b,S.h,S.s), q=shape(S.b,S.h,0);
    return '밀어서 직사각형으로 만들어도 넓이는 '+r2(shoelace(p)/400)+'cm² 그대로다. 둘레는 '+r2(perim(p)/20)+'cm에서 '+r2(perim(q)/20)+'cm로 바뀌었다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var i;
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=0;i<=20;i++){ ctx.beginPath();ctx.moveTo(20+i*SC,60);ctx.lineTo(20+i*SC,290);ctx.stroke(); }
    for(i=0;i<=11;i++){ ctx.beginPath();ctx.moveTo(20,60+i*SC);ctx.lineTo(420,60+i*SC);ctx.stroke(); }
    var cur=(t===null)?S.s:S.s*(1-t);
    poly(ctx,shape(S.b,S.h,S.s),null,'#cbd5e1',true);
    poly(ctx,shape(S.b,S.h,cur),'rgba(37,99,235,0.20)','#2563eb',false);
    ctx.strokeStyle='#16a34a';ctx.lineWidth=2.5;ctx.setLineDash([4,4]);
    ctx.beginPath();ctx.moveTo(X0+cur,Y0);ctx.lineTo(X0+cur,Y0+S.h);ctx.stroke();ctx.setLineDash([]);
    lbl(ctx,'높이 '+(S.h/20).toFixed(1)+'cm',X0+cur+8,Y0+S.h/2,'#15803d',15);
    lbl(ctx,'밑변 '+(S.b/20).toFixed(1)+'cm',X0+S.b/2,Y0+S.h+22,'#1d4ed8',15,'center');
    lbl(ctx,'점선 = 처음 모양',24,44,'#64748b',16);
    var p=shape(S.b,S.h,S.s), pc=shape(S.b,S.h,cur);
    box(ctx,20,304,400,80);
    lbl(ctx,'넓이 : '+r2(shoelace(pc)/400)+'cm²   (밑변 × 높이 = '+r2(S.b*S.h/400)+')',38,336,'#1f2937',19);
    lbl(ctx,'둘레 : '+r2(perim(pc)/20)+'cm'+((t===null)?'':('   처음 둘레 '+r2(perim(p)/20)+'cm')),38,366,'#52627a',18);
  },
  record:function(S){
    var p=shape(S.b,S.h,S.s), q=shape(S.b,S.h,0);
    return {b:r1(S.b/20),h:r1(S.h/20),s:r1(S.s/20),
            area:r2(shoelace(p)/400),bh:r2(S.b*S.h/400),
            per:r2(perim(p)/20),perRect:r2(perim(q)/20)};
  },
  headA:['번호','밑변','높이','기울인 정도','넓이','밑변×높이','둘레','폈을 때 둘레'],
  rowA:function(r,i){
    return [i+1,r.b+'cm',r.h+'cm',r.s+'cm','<b>'+r.area+'cm²</b>',r.bh,r.per+'cm',r.perRect+'cm'];
  },
  analyze:function(rec){
    var rows=[],ok=0,map={},pairs=0,agree=0,perDiff=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var a=(Math.abs(r.area-r.bh)<0.02);
      if(a) ok++;
      if(Math.abs(r.per-r.perRect)>0.02) perDiff++;
      var k=r.b+'x'+r.h, note='첫 기록';
      if(map[k]!==undefined){
        pairs++;
        var same=(Math.abs(map[k]-r.area)<0.02);
        if(same) agree++;
        note='<span class="'+(same?'ok':'no')+'">'+(same?'넓이 같음':'넓이 다름')+'</span>';
      } else { map[k]=r.area; }
      rows.push([r.b+' × '+r.h, r.s+'cm', '<b>'+r.area+'cm²</b>', r.bh,
                 '<span class="'+(a?'ok':'no')+'">'+(a?'○':'×')+'</span>',
                 r.per+'cm', note]);
    }
    var stats=[
      {t:'넓이 = 밑변 × 높이',big:ok+' / '+rec.length,p:'기울인 정도와 상관없이 성립했는지 확인한 결과.'},
      {t:'밑변·높이가 같고 기울기만 다른 짝',big:pairs+'쌍',
       p:pairs?('그중 넓이가 같았던 것 '+agree+'쌍.'):'밑변과 높이를 그대로 두고 기울기만 바꿔 기록해 보자.'},
      {t:'둘레가 달라진 기록',big:perDiff+'개',
       p:'기울이면 빗변이 길어져 둘레는 늘어난다. 넓이는 그대로인데도.'}
    ];
    var concl;
    if(pairs===0){
      concl='<b>더 해 보자</b> — 밑변과 높이를 고정하고 기울기만 바꿔 기록하면, 기울기가 넓이에 영향을 주는지 알 수 있다.';
    } else if(ok===rec.length && agree===pairs){
      concl='<b>정리</b> — 아무리 기울여도 넓이는 <b>밑변 × 높이</b> 그대로였다. 밀어서 직사각형으로 펴도 잘려 나가거나 늘어난 부분이 없기 때문이다. '
           +'반면 <b>둘레는 기울일수록 늘어났다.</b> 둘레가 크다고 넓이가 큰 것이 아니다.';
    } else {
      concl='<b>확인 필요</b> — 넓이가 밑변×높이와 다른 기록이 있다.';
    }
    return {head:['밑변×높이','기울기','넓이','밑변×높이','같은가?','둘레','같은 밑변·높이끼리'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 원주율
# ============================================================
LAB_PI = BASE + r"""
var Y=180, X0=34;
var LAB = {
  cw:440, ch:400, cvTitle:'원 굴리기판',
  action:'한 바퀴 굴려 보기',
  hint0:'원의 지름을 정하고 한 바퀴 굴려서 굴러간 거리를 재 보자.',
  sliders:[
    {id:'d',label:'원의 지름',min:40,max:110,value:80,color:'#2563eb',fmt:function(v){return (v/20).toFixed(1)+'cm';}}
  ],
  readout:function(S,ran){
    var C=Math.PI*S.d;
    return [{k:'지름',v:(S.d/20).toFixed(1)+'cm'},
            {k:'굴러간 거리',v:ran?(r2(C/20)+'cm'):'굴려 보자'}];
  },
  doneMsg:function(S){
    var C=Math.PI*S.d;
    return '한 바퀴 굴러간 거리는 '+r2(C/20)+'cm였다. 지름으로 나누면 '+r2(C/S.d)+'이다. 지름을 바꿔 다시 굴려 보자.';
  },
  draw:function(ctx,S,t,ran){
    var R=S.d/2, C=Math.PI*S.d;
    var run=(t===null)?0:Math.min(1,t);
    ctx.strokeStyle='#334155';ctx.lineWidth=3;
    ctx.beginPath();ctx.moveTo(X0,Y+R);ctx.lineTo(X0+C+40,Y+R);ctx.stroke();
    ctx.strokeStyle='#f59e0b';ctx.lineWidth=6;
    ctx.beginPath();ctx.moveTo(X0,Y+R+8);ctx.lineTo(X0+C*run,Y+R+8);ctx.stroke();
    var cx=X0+R+C*run, th=2*Math.PI*run;
    ctx.beginPath();ctx.arc(cx,Y,R,0,Math.PI*2);
    ctx.fillStyle='rgba(37,99,235,0.12)';ctx.fill();
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.stroke();
    ctx.strokeStyle='#1d4ed8';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(cx,Y);ctx.lineTo(cx+R*Math.sin(th),Y+R*Math.cos(th));ctx.stroke();
    ctx.beginPath();ctx.arc(cx+R*Math.sin(th),Y+R*Math.cos(th),5,0,Math.PI*2);
    ctx.fillStyle='#dc2626';ctx.fill();
    ctx.strokeStyle='#16a34a';ctx.lineWidth=2.5;ctx.setLineDash([5,4]);
    ctx.beginPath();ctx.moveTo(cx-R,Y);ctx.lineTo(cx+R,Y);ctx.stroke();ctx.setLineDash([]);
    lbl(ctx,'지름 '+(S.d/20).toFixed(1)+'cm 인 원을 한 바퀴 굴리면?',24,40,'#1d4ed8',18);
    box(ctx,20,286,400,98);
    lbl(ctx,(t===null)?'굴러간 거리는 지름의 몇 배일까?':('굴러간 거리(원주) : '+r2(C/20)+'cm'),38,318,'#1f2937',20);
    lbl(ctx,'지름 : '+(S.d/20).toFixed(1)+'cm',38,348,'#52627a',18);
    lbl(ctx,(t===null)?'':('원주 ÷ 지름 = '+r2(C/S.d)),38,376,'#15803d',19);
  },
  record:function(S){
    var C=Math.PI*S.d;
    return {d:r2(S.d/20),c:r2(C/20),ratio:r2(C/S.d),ratio3:Math.round(C/S.d*1000)/1000};
  },
  headA:['번호','지름','원주','원주 ÷ 지름','지름 × 3.14'],
  rowA:function(r,i){
    return [i+1,r.d+'cm','<b>'+r.c+'cm</b>',r.ratio3,r2(r.d*3.14)+'cm'];
  },
  analyze:function(rec){
    var rows=[],same=0,mn=99,mx=0,ds={};
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var ok=(Math.abs(r.ratio-3.14)<0.005);
      if(ok) same++;
      if(r.ratio3<mn) mn=r.ratio3;
      if(r.ratio3>mx) mx=r.ratio3;
      ds[r.d]=true;
      rows.push([r.d+'cm', r.c+'cm', r.ratio3, r2(r.d*3.14)+'cm',
                 '<span class="'+(ok?'ok':'no')+'">'+(ok?'○':'×')+'</span>']);
    }
    var dn=0; for(var k in ds) dn++;
    var stats=[
      {t:'원주 ÷ 지름 ≒ 3.14',big:same+' / '+rec.length,p:'소수 둘째 자리까지 3.14였던 기록 수.'},
      {t:'비의 가장 작은 값 ~ 가장 큰 값',big:mn+' ~ '+mx,p:'원 크기를 바꿔도 비는 움직이지 않았다.'},
      {t:'시험한 지름',big:dn+'가지',p:dn>1?'크기가 다른 원들에서 같은 값이 나왔다.':'지름을 바꿔 더 기록해 보자.'}
    ];
    var concl;
    if(dn<2){
      concl='<b>더 해 보자</b> — 지름을 바꿔 여러 원을 굴려 봐야 비가 정말 일정한지 알 수 있다.';
    } else if(same===rec.length){
      concl='<b>정리</b> — 큰 원이든 작은 원이든 <b>원주 ÷ 지름은 언제나 같은 값(3.14…)</b>이었다. 이 값을 원주율이라고 한다. '
           +'그래서 원주 = 지름 × 3.14로 구할 수 있다. 원의 크기와 상관없이 정해진 수라는 점이 핵심이다.';
    } else {
      concl='<b>확인 필요</b> — 비가 3.14와 다르게 나온 기록이 있다.';
    }
    return {head:['지름','원주','원주÷지름','지름×3.14','3.14인가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 원의 넓이와 배율
# ============================================================
LAB_CAREA = BASE + r"""
var LAB = {
  cw:440, ch:420, cvTitle:'원 확대판',
  action:'반지름을 늘려 보기',
  hint0:'처음 원의 반지름과 몇 배로 늘릴지 정해 보자.',
  sliders:[
    {id:'r',label:'처음 반지름',min:10,max:30,value:20,color:'#2563eb',fmt:function(v){return (v/10).toFixed(1)+'cm';}},
    {id:'k',label:'몇 배로 늘리기',min:2,max:4,value:2,color:'#f59e0b',unit:'배'}
  ],
  readout:function(S,ran){
    var r=S.r/10, A1=Math.PI*r*r, A2=Math.PI*(r*S.k)*(r*S.k);
    return [{k:'처음 넓이',v:r2(A1)+'cm²'},
            {k:'늘린 뒤 넓이',v:ran?(r2(A2)+'cm²'):'늘려 보자'}];
  },
  doneMsg:function(S){
    return '반지름을 '+S.k+'배로 늘리니 넓이는 '+(S.k*S.k)+'배가 되었다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var CX=220, CY=190;
    var r=S.r, R=S.r*S.k;
    var grow=(t===null)?0:Math.min(1,t);
    var cur=r+(R-r)*grow;
    ctx.beginPath();ctx.arc(CX,CY,cur*4,0,Math.PI*2);
    ctx.fillStyle='rgba(245,158,11,0.22)';ctx.fill();
    ctx.strokeStyle='#d97706';ctx.lineWidth=3;ctx.stroke();
    ctx.beginPath();ctx.arc(CX,CY,r*4,0,Math.PI*2);
    ctx.fillStyle='rgba(37,99,235,0.22)';ctx.fill();
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.stroke();
    ctx.strokeStyle='#1f2937';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(CX,CY);ctx.lineTo(CX+cur*4,CY);ctx.stroke();
    lbl(ctx,'반지름을 '+S.k+'배로 늘리면 넓이는 몇 배?',24,36,'#1d4ed8',18);
    var rr=S.r/10, A1=Math.PI*rr*rr, A2=Math.PI*(rr*S.k)*(rr*S.k);
    box(ctx,20,318,400,90);
    lbl(ctx,'처음 : 반지름 '+rr.toFixed(1)+'cm, 넓이 '+r2(A1)+'cm²',38,348,'#1d4ed8',18);
    lbl(ctx,(t===null)?('늘린 뒤 : 반지름 '+(rr*S.k).toFixed(1)+'cm, 넓이 ?'):('늘린 뒤 : 반지름 '+(rr*S.k).toFixed(1)+'cm, 넓이 '+r2(A2)+'cm²'),38,376,'#b45309',18);
    lbl(ctx,(t===null)?'':('넓이는 '+r2(A2/A1)+'배  ( '+S.k+' × '+S.k+' )'),38,400,'#15803d',17);
  },
  record:function(S){
    var r=S.r/10, A1=Math.PI*r*r, A2=Math.PI*(r*S.k)*(r*S.k);
    var C1=2*Math.PI*r, C2=2*Math.PI*r*S.k;
    return {r:r1(r),k:S.k,a1:r2(A1),a2:r2(A2),ar:r2(A2/A1),kk:S.k*S.k,cr:r2(C2/C1)};
  },
  headA:['번호','처음 반지름','배율','처음 넓이','늘린 넓이','넓이는 몇 배','배율 × 배율','원주는 몇 배'],
  rowA:function(r,i){
    return [i+1,r.r+'cm',r.k+'배',r.a1,r.a2,'<b>'+r.ar+'배</b>',r.kk,r.cr+'배'];
  },
  analyze:function(rec){
    var rows=[],sq=0,lin=0,cok=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var a=(Math.abs(r.ar-r.kk)<0.02);
      var b=(Math.abs(r.ar-r.k)<0.02);
      var c=(Math.abs(r.cr-r.k)<0.02);
      if(a) sq++;
      if(b) lin++;
      if(c) cok++;
      rows.push([r.r+'cm → '+r.k+'배', r.a1+' → '+r.a2, '<b>'+r.ar+'배</b>', r.kk,
                 '<span class="'+(a?'ok':'no')+'">'+(a?'○':'×')+'</span>',
                 r.cr+'배',
                 '<span class="'+(c?'ok':'no')+'">'+(c?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'넓이 배율 = 배율 × 배율',big:sq+' / '+rec.length,p:'반지름을 k배 하면 넓이가 k×k배인지 확인한 결과.'},
      {t:'“넓이도 그냥 k배”가 맞은 횟수',big:lin+' / '+rec.length,p:'반지름 배율과 넓이 배율이 같았던 기록 수.'},
      {t:'원주 배율 = 배율',big:cok+' / '+rec.length,p:'길이는 그대로 k배, 넓이만 k×k배가 된다.'}
    ];
    var concl;
    if(sq===rec.length && lin===0){
      concl='<b>정리</b> — 반지름을 2배로 하면 넓이는 2배가 아니라 <b>4배</b>, 3배로 하면 9배가 되었다. '
           +'넓이는 가로 방향으로도 세로 방향으로도 함께 늘어나기 때문이다. 반면 <b>원주(길이)는 정확히 배율만큼</b>만 늘었다. '
           +'길이의 배율과 넓이의 배율은 다르다.';
    } else if(sq===rec.length){
      concl='<b>정리</b> — 넓이 배율은 항상 배율의 제곱이었다. 배율이 1보다 큰 값들로 더 기록해 보자.';
    } else {
      concl='<b>확인 필요</b> — 규칙과 어긋난 기록이 있다.';
    }
    return {head:['변화','넓이','넓이 배율','배율×배율','같은가?','원주 배율','배율과 같은가?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 직육면체 부피·겉넓이 배율
# ============================================================
LAB_VOL = BASE + r"""
function drawBox(ctx,ox,oy,a,b,c,u,fill,edge){
  var dx=u*0.5, dy=-u*0.34;
  var W=a*u, H=c*u, D=b;
  var p0=[ox,oy], p1=[ox+W,oy], p2=[ox+W,oy-H], p3=[ox,oy-H];
  var q0=[ox+D*dx,oy+D*dy], q1=[ox+W+D*dx,oy+D*dy], q2=[ox+W+D*dx,oy-H+D*dy], q3=[ox+D*dx,oy-H+D*dy];
  poly(ctx,[p3,q3,q2,p2],fill,edge,false);
  poly(ctx,[p1,q1,q2,p2],fill,edge,false);
  poly(ctx,[p0,p1,p2,p3],fill,edge,false);
}
var LAB = {
  cw:440, ch:420, cvTitle:'직육면체 확대판',
  action:'모서리를 늘려 보기',
  hint0:'직육면체의 세 모서리와 몇 배로 늘릴지 정해 보자.',
  sliders:[
    {id:'a',label:'가로',min:1,max:5,value:2,color:'#2563eb',unit:'cm'},
    {id:'b',label:'세로',min:1,max:5,value:3,color:'#16a34a',unit:'cm'},
    {id:'c',label:'높이',min:1,max:5,value:2,color:'#f59e0b',unit:'cm'},
    {id:'k',label:'몇 배로 늘리기',min:2,max:3,value:2,color:'#dc2626',unit:'배'}
  ],
  calc:function(S){
    var V=S.a*S.b*S.c, A=2*(S.a*S.b+S.b*S.c+S.c*S.a);
    var k=S.k, V2=(S.a*k)*(S.b*k)*(S.c*k);
    var A2=2*((S.a*k)*(S.b*k)+(S.b*k)*(S.c*k)+(S.c*k)*(S.a*k));
    return {V:V,A:A,V2:V2,A2:A2,vr:V2/V,ar:A2/A};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'처음 부피',v:c.V+'cm³'},
            {k:'늘린 뒤 부피',v:ran?(c.V2+'cm³'):'늘려 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '모서리를 '+S.k+'배로 늘리니 부피는 '+c.vr+'배, 겉넓이는 '+c.ar+'배가 되었다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var cc=this.calc(S);
    var grow=(t===null)?0:Math.min(1,t);
    var u=Math.min(26, 240/(S.a*S.k+S.b*S.k*0.5));
    drawBox(ctx,60,250,S.a,S.b,S.c,u,'rgba(37,99,235,0.22)','#2563eb');
    if(grow>0){
      ctx.globalAlpha=grow;
      var kk=1+(S.k-1)*grow;
      drawBox(ctx,60,250,S.a*kk,S.b*kk,S.c*kk,u,'rgba(245,158,11,0.16)','#d97706');
      ctx.globalAlpha=1;
    }
    lbl(ctx,'모서리를 '+S.k+'배로 늘리면 부피는 몇 배?',24,36,'#1d4ed8',18);
    lbl(ctx,'처음 : '+S.a+' × '+S.b+' × '+S.c,24,286,'#1d4ed8',17);
    box(ctx,20,300,400,108);
    lbl(ctx,'처음 부피 '+cc.V+'cm³   겉넓이 '+cc.A+'cm²',38,330,'#1d4ed8',18);
    lbl(ctx,(t===null)?'늘린 뒤는?':('늘린 뒤 부피 '+cc.V2+'cm³   겉넓이 '+cc.A2+'cm²'),38,360,'#b45309',18);
    lbl(ctx,(t===null)?'':('부피 '+cc.vr+'배 ( '+S.k+'×'+S.k+'×'+S.k+' )    겉넓이 '+cc.ar+'배 ( '+S.k+'×'+S.k+' )'),38,390,'#15803d',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,c:S.c,k:S.k,V:c.V,A:c.A,V2:c.V2,A2:c.A2,
            vr:c.vr,ar:c.ar,k2:S.k*S.k,k3:S.k*S.k*S.k};
  },
  headA:['번호','모서리','배율','처음 부피','늘린 부피','부피 배율','배율³','겉넓이 배율','배율²'],
  rowA:function(r,i){
    return [i+1,r.a+'×'+r.b+'×'+r.c,r.k+'배',r.V,r.V2,'<b>'+r.vr+'배</b>',r.k3,r.ar+'배',r.k2];
  },
  analyze:function(rec){
    var rows=[],v3=0,a2=0,lin=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var x=(r.vr===r.k3), y=(r.ar===r.k2), z=(r.vr===r.k);
      if(x) v3++;
      if(y) a2++;
      if(z) lin++;
      rows.push([r.a+'×'+r.b+'×'+r.c+' → '+r.k+'배', r.V+' → '+r.V2, '<b>'+r.vr+'배</b>', r.k3,
                 '<span class="'+(x?'ok':'no')+'">'+(x?'○':'×')+'</span>',
                 r.ar+'배', r.k2,
                 '<span class="'+(y?'ok':'no')+'">'+(y?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'부피 배율 = 배율 × 배율 × 배율',big:v3+' / '+rec.length,p:'모서리를 k배 했을 때 부피가 k³배인지 확인한 결과.'},
      {t:'겉넓이 배율 = 배율 × 배율',big:a2+' / '+rec.length,p:'겉넓이는 넓이니까 k²배가 되는지 확인한 결과.'},
      {t:'“부피도 그냥 k배”가 맞은 횟수',big:lin+' / '+rec.length,p:'모서리 배율과 부피 배율이 같았던 기록 수.'}
    ];
    var concl;
    if(v3===rec.length && a2===rec.length && lin===0){
      concl='<b>정리</b> — 모서리를 2배로 늘리면 부피는 2배가 아니라 <b>8배</b>, 겉넓이는 <b>4배</b>가 되었다. '
           +'길이는 k배, 넓이는 k×k배, 부피는 k×k×k배로 늘어난다. 늘어나는 방향의 수만큼 배율이 곱해지는 것이다.';
    } else if(v3===rec.length){
      concl='<b>정리</b> — 부피 배율은 항상 배율의 세제곱이었다. 겉넓이 쪽도 함께 확인해 보자.';
    } else {
      concl='<b>확인 필요</b> — 규칙과 어긋난 기록이 있다.';
    }
    return {head:['변화','부피','부피 배율','배율³','같은가?','겉넓이 배율','배율²','같은가?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 선대칭과 점대칭
# ============================================================
LAB_SYM = BASE + r"""
var SHAPES=[
  {name:'정사각형',p:[[-1,-1],[1,-1],[1,1],[-1,1]]},
  {name:'정삼각형',p:[[0,-1.15],[1,0.58],[-1,0.58]]},
  {name:'평행사변형',p:[[-1.4,-0.7],[0.6,-0.7],[1.4,0.7],[-0.6,0.7]]},
  {name:'등변사다리꼴',p:[[-1.4,0.7],[1.4,0.7],[0.8,-0.7],[-0.8,-0.7]]}
];
var METHODS=['세로선 대칭','가로선 대칭','점대칭 (180° 돌리기)'];
function tf(p,m){
  var o=[],i;
  for(i=0;i<p.length;i++){
    var q=p[i];
    if(m===0) o.push([-q[0],q[1]]);
    else if(m===1) o.push([q[0],-q[1]]);
    else o.push([-q[0],-q[1]]);
  }
  return o;
}
function keyOf(p){
  var a=[],i;
  for(i=0;i<p.length;i++){ a.push(Math.round(p[i][0]*100)+','+Math.round(p[i][1]*100)); }
  a.sort();
  return a.join(';');
}
function sc(p,cx,cy,u){
  var o=[],i;
  for(i=0;i<p.length;i++){ o.push([cx+p[i][0]*u,cy+p[i][1]*u]); }
  return o;
}
var LAB = {
  cw:440, ch:400, cvTitle:'대칭 실험판',
  action:'대칭시켜 겹쳐 보기',
  hint0:'도형과 대칭 방법을 고르고, 처음 도형과 완전히 겹치는지 확인해 보자.',
  sliders:[
    {id:'sh',label:'도형',min:0,max:3,value:2,color:'#2563eb',fmt:function(v){return SHAPES[v].name;}},
    {id:'m',label:'대칭 방법',min:0,max:2,value:0,color:'#16a34a',fmt:function(v){return METHODS[v];}}
  ],
  readout:function(S,ran){
    var s=SHAPES[S.sh];
    var same=(keyOf(tf(s.p,S.m))===keyOf(s.p));
    return [{k:'도형 / 방법',v:s.name+' · '+METHODS[S.m]},
            {k:'결과',v:ran?(same?'완전히 겹침':'겹치지 않음'):'해 보자'}];
  },
  doneMsg:function(S){
    var s=SHAPES[S.sh];
    var same=(keyOf(tf(s.p,S.m))===keyOf(s.p));
    return s.name+'을(를) '+METHODS[S.m]+'하면 처음 도형과 '+(same?'완전히 겹친다':'겹치지 않는다')+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var s=SHAPES[S.sh], CX=220, CY=170, U=64;
    var move=(t===null)?0:Math.min(1,t);
    ctx.strokeStyle='#e2e8f0';ctx.lineWidth=1.4;
    ctx.beginPath();ctx.moveTo(40,CY);ctx.lineTo(400,CY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(CX,40);ctx.lineTo(CX,300);ctx.stroke();
    if(S.m===0){ ctx.strokeStyle='#f59e0b';ctx.lineWidth=2.5;ctx.setLineDash([7,5]);
      ctx.beginPath();ctx.moveTo(CX,40);ctx.lineTo(CX,300);ctx.stroke();ctx.setLineDash([]); }
    else if(S.m===1){ ctx.strokeStyle='#f59e0b';ctx.lineWidth=2.5;ctx.setLineDash([7,5]);
      ctx.beginPath();ctx.moveTo(40,CY);ctx.lineTo(400,CY);ctx.stroke();ctx.setLineDash([]); }
    else { ctx.beginPath();ctx.arc(CX,CY,7,0,Math.PI*2);ctx.fillStyle='#f59e0b';ctx.fill(); }
    poly(ctx,sc(s.p,CX,CY,U),'rgba(148,163,184,0.16)','#94a3b8',true);
    var cur=[],i;
    for(i=0;i<s.p.length;i++){
      var q=s.p[i], w=tf(s.p,S.m)[i];
      cur.push([q[0]+(w[0]-q[0])*move, q[1]+(w[1]-q[1])*move]);
    }
    poly(ctx,sc(cur,CX,CY,U),'rgba(37,99,235,0.24)','#2563eb',false);
    lbl(ctx,s.name+' — '+METHODS[S.m],24,34,'#1d4ed8',19);
    lbl(ctx,'점선 = 처음 도형',24,320,'#64748b',16);
    var same=(keyOf(tf(s.p,S.m))===keyOf(s.p));
    box(ctx,20,332,400,52);
    lbl(ctx,(t===null)?'처음 도형과 겹칠까?':(same?'완전히 겹친다':'겹치지 않는다'),38,364,same?'#15803d':'#b91c1c',21);
  },
  record:function(S){
    var s=SHAPES[S.sh];
    var same=(keyOf(tf(s.p,S.m))===keyOf(s.p));
    return {sh:S.sh,name:s.name,m:S.m,method:METHODS[S.m],same:same};
  },
  headA:['번호','도형','대칭 방법','처음 도형과 겹치나?'],
  rowA:function(r,i){
    return [i+1,r.name,r.method,'<span class="'+(r.same?'ok':'no')+'">'+(r.same?'겹침':'안 겹침')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],g={},i,k;
    for(i=0;i<rec.length;i++){
      var r=rec[i];
      if(!g[r.sh]) g[r.sh]={name:r.name,line:false,point:false,hasLine:false,hasPoint:false};
      if(r.m===2){ g[r.sh].hasPoint=true; if(r.same) g[r.sh].point=true; }
      else { g[r.sh].hasLine=true; if(r.same) g[r.sh].line=true; }
      rows.push([r.name, r.method, r.same?'<span class="ok">겹침</span>':'<span class="no">안 겹침</span>']);
    }
    var lineOnly=[],pointOnly=[],both=[],neither=[],tested=0;
    for(k in g){
      var x=g[k];
      if(!(x.hasLine&&x.hasPoint)) continue;
      tested++;
      if(x.line&&x.point) both.push(x.name);
      else if(x.line) lineOnly.push(x.name);
      else if(x.point) pointOnly.push(x.name);
      else neither.push(x.name);
    }
    var stats=[
      {t:'선대칭·점대칭을 모두 확인한 도형',big:tested+'개',
       p:tested?'같은 도형에 두 방법을 모두 적용해 봤다.':'한 도형에 선대칭과 점대칭을 모두 시험해 보자.'},
      {t:'선대칭만 되는 도형',big:lineOnly.length+'개',p:lineOnly.length?lineOnly.join(', '):'등변사다리꼴을 확인해 보자.'},
      {t:'점대칭만 되는 도형',big:pointOnly.length+'개',p:pointOnly.length?pointOnly.join(', '):'평행사변형을 확인해 보자.'}
    ];
    var concl;
    if(tested===0){
      concl='<b>더 해 보자</b> — 한 도형에 대해 선대칭과 점대칭을 모두 기록해야 두 성질을 비교할 수 있다.';
    } else if(lineOnly.length&&pointOnly.length){
      concl='<b>정리</b> — 선대칭과 점대칭은 <b>서로 다른 성질</b>이었다. '
           +pointOnly.join(', ')+'은(는) 접어서는 겹치지 않지만 180° 돌리면 겹쳤고, '
           +lineOnly.join(', ')+'은(는) 그 반대였다. 둘 다 되는 도형도, 둘 다 안 되는 도형도 있다.';
    } else {
      concl='<b>정리</b> — 도형마다 겹치는 방법이 달랐다. 평행사변형(점대칭만)과 등변사다리꼴(선대칭만)을 모두 기록하면 차이가 뚜렷해진다.';
    }
    return {head:['도형','대칭 방법','결과'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("elem56_parallelogram_area_lab.html",
     "평행사변형 실험실 — 기울이면 넓이가 커질까?",
     "평행사변형 실험실 — 기울이면 넓이가 커질까?",
     "밑변과 높이를 고정한 채 기울기만 바꿔 넓이와 둘레를 기록하고, 밀어서 직사각형으로 펴 본다.",
     LAB_PARA),
    ("elem56_pi_rolling_lab.html",
     "원 굴리기 실험실 — 원주는 지름의 몇 배일까?",
     "원 굴리기 실험실 — 원주는 지름의 몇 배일까?",
     "크기가 다른 원을 한 바퀴 굴려 굴러간 거리를 재고, 지름으로 나눈 값을 기록한다.",
     LAB_PI),
    ("elem56_circle_scale_lab.html",
     "원 확대 실험실 — 반지름 2배면 넓이도 2배일까?",
     "원 확대 실험실 — 반지름 2배면 넓이도 2배일까?",
     "반지름을 여러 배로 늘리며 넓이와 원주가 각각 몇 배가 되는지 기록해 비교한다.",
     LAB_CAREA),
    ("elem56_volume_scale_lab.html",
     "직육면체 확대 실험실 — 모서리 2배면 부피도 2배일까?",
     "직육면체 확대 실험실 — 모서리 2배면 부피도 2배일까?",
     "세 모서리를 같은 배율로 늘리며 부피와 겉넓이가 각각 몇 배가 되는지 기록한다.",
     LAB_VOL),
    ("elem56_symmetry_lab.html",
     "대칭 실험실 — 선대칭이면 점대칭일까?",
     "대칭 실험실 — 선대칭이면 점대칭일까?",
     "여러 도형에 선대칭과 점대칭을 적용해 처음 도형과 겹치는지 기록하고, 두 성질을 비교한다.",
     LAB_SYM),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c7_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
