# -*- coding: utf-8 -*-
"""고등 대수 — 삼각함수 활용 2종 + 수열 3종"""
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
function sg(v){return (v<0)?(' − '+(-v)):(' + '+v);}
function dist(p,q){return Math.sqrt((p[0]-q[0])*(p[0]-q[0])+(p[1]-q[1])*(p[1]-q[1]));}
function angDeg(p,q,r){
  var ax=p[0]-q[0],ay=p[1]-q[1],bx=r[0]-q[0],by=r[1]-q[1];
  var d=ax*bx+ay*by,m=Math.sqrt(ax*ax+ay*ay)*Math.sqrt(bx*bx+by*by);
  var c=(m===0)?1:d/m; if(c>1)c=1; if(c<-1)c=-1;
  return Math.acos(c)*180/Math.PI;
}
"""

# ============================================================
# 1. 사인법칙
# ============================================================
LAB_SINE = BASE + r"""
var A=[80,330], B=[370,330];
function circum(A,B,C){
  var d=2*(A[0]*(B[1]-C[1])+B[0]*(C[1]-A[1])+C[0]*(A[1]-B[1]));
  if(Math.abs(d)<1e-9) return null;
  var ux=((A[0]*A[0]+A[1]*A[1])*(B[1]-C[1])+(B[0]*B[0]+B[1]*B[1])*(C[1]-A[1])+(C[0]*C[0]+C[1]*C[1])*(A[1]-B[1]))/d;
  var uy=((A[0]*A[0]+A[1]*A[1])*(C[0]-B[0])+(B[0]*B[0]+B[1]*B[1])*(A[0]-C[0])+(C[0]*C[0]+C[1]*C[1])*(B[0]-A[0]))/d;
  return [ux,uy];
}
var LAB = {
  cw:440, ch:430, cvTitle:'사인법칙 판',
  action:'세 변과 세 각 재기',
  hint0:'꼭짓점 C를 옮겨 삼각형 모양을 바꿔 보자.',
  sliders:[
    {id:'cx',label:'C의 좌우',min:20,max:420,value:180,color:'#2563eb',unit:''},
    {id:'cy',label:'C의 높이',min:50,max:280,value:120,color:'#16a34a',unit:''}
  ],
  calc:function(S){
    var C=[S.cx,S.cy];
    var a=dist(B,C), b=dist(C,A), c=dist(A,B);
    var AA=angDeg(B,A,C), BB=angDeg(C,B,A), CC=angDeg(A,C,B);
    var O=circum(A,B,C);
    var R=O?dist(O,A):0;
    function s(d){ return Math.sin(d*Math.PI/180); }
    return {C:C,a:a,b:b,c:c,A:AA,B:BB,C2:CC,O:O,R:R,
            ra:a/s(AA),rb:b/s(BB),rc:c/s(CC),twoR:2*R};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'세 각',v:r1(c.A)+'° / '+r1(c.B)+'° / '+r1(c.C2)+'°'},
            {k:'a / sin A',v:ran?r2(c.ra/20):'재 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '세 비는 '+r2(c.ra/20)+', '+r2(c.rb/20)+', '+r2(c.rc/20)+'.  외접원 지름 2R = '+r2(c.twoR/20)+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var grow=(t===null)?0:Math.min(1,t);
    if(c.O&&grow>0.5){
      ctx.beginPath();ctx.arc(c.O[0],c.O[1],c.R,0,Math.PI*2);
      ctx.strokeStyle='#cbd5e1';ctx.lineWidth=2;ctx.stroke();
    }
    ctx.beginPath();ctx.moveTo(A[0],A[1]);ctx.lineTo(B[0],B[1]);ctx.lineTo(c.C[0],c.C[1]);ctx.closePath();
    ctx.fillStyle='rgba(37,99,235,0.10)';ctx.fill();
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;ctx.stroke();
    lbl(ctx,'A',A[0]-18,A[1]+8,'#334155',16);
    lbl(ctx,'B',B[0]+8,B[1]+8,'#334155',16);
    lbl(ctx,'C',c.C[0]-6,c.C[1]-12,'#334155',16);
    if(grow>=1){
      lbl(ctx,r1(c.A)+'°',A[0]+30,A[1]-12,'#1d4ed8',14);
      lbl(ctx,r1(c.B)+'°',B[0]-42,B[1]-12,'#1d4ed8',14);
      lbl(ctx,r1(c.C2)+'°',c.C[0]-10,c.C[1]+28,'#1d4ed8',14);
      lbl(ctx,'c = '+r2(c.c/20),(A[0]+B[0])/2-24,A[1]+22,'#b45309',13);
    }
    lbl(ctx,'삼각형과 외접원',24,32,'#1d4ed8',18);
    box(ctx,20,344,400,74);
    lbl(ctx,(t===null)?'a/sinA, b/sinB, c/sinC 는?':
        ('a/sinA '+r2(c.ra/20)+'   b/sinB '+r2(c.rb/20)+'   c/sinC '+r2(c.rc/20)),38,374,'#1f2937',16);
    lbl(ctx,(t===null)?'':('외접원 지름 2R = '+r2(c.twoR/20)),38,404,'#15803d',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:r2(c.a/20),b:r2(c.b/20),c:r2(c.c/20),
            A:r1(c.A),B:r1(c.B),C:r1(c.C2),
            ra:r2(c.ra/20),rb:r2(c.rb/20),rc:r2(c.rc/20),twoR:r2(c.twoR/20),
            eq:(Math.abs(c.ra-c.rb)<0.5&&Math.abs(c.rb-c.rc)<0.5),
            rOk:(Math.abs(c.ra-c.twoR)<0.5),
            sum:r1(c.A+c.B+c.C2)};
  },
  headA:['번호','세 각','a/sinA','b/sinB','c/sinC','세 비 같나?','2R','같나?','각의 합'],
  rowA:function(r,i){
    return [i+1,r.A+'/'+r.B+'/'+r.C,'<b>'+r.ra+'</b>',r.rb,r.rc,
            '<span class="'+(r.eq?'ok':'no')+'">'+(r.eq?'○':'×')+'</span>',
            r.twoR,
            '<span class="'+(r.rOk?'ok':'no')+'">'+(r.rOk?'○':'×')+'</span>',
            r.sum+'°'];
  },
  analyze:function(rec){
    var rows=[],eq=0,rok=0,mn=9999,mx=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.eq) eq++;
      if(r.rOk) rok++;
      if(r.ra<mn) mn=r.ra;
      if(r.ra>mx) mx=r.ra;
      rows.push([r.A+'/'+r.B+'/'+r.C, r.ra+' / '+r.rb+' / '+r.rc,
                 '<span class="'+(r.eq?'ok':'no')+'">'+(r.eq?'○':'×')+'</span>',
                 r.twoR,
                 '<span class="'+(r.rOk?'ok':'no')+'">'+(r.rOk?'○':'×')+'</span>',
                 r.sum+'°']);
    }
    var stats=[
      {t:'세 비가 모두 같았던 횟수',big:eq+' / '+rec.length,
       p:'좌표에서 잰 변의 길이와 각으로 직접 계산한 결과.'},
      {t:'그 비가 외접원 지름과 같았던 횟수',big:rok+' / '+rec.length,
       p:'a/sinA 의 값이 무엇인지 확인한 결과.'},
      {t:'비의 범위',big:mn+' ~ '+mx,
       p:'삼각형 모양을 바꾸면 비 자체는 달라지지만, 한 삼각형 안에서는 셋이 같다.'}
    ];
    var concl;
    if(eq===rec.length&&rok===rec.length){
      concl='<b>정리</b> — 어떤 삼각형이든 <b>a/sinA = b/sinB = c/sinC</b> 였고, 그 공통값은 <b>외접원의 지름 2R</b>이었다. '
           +'큰 각의 맞은편에 긴 변이 오는 관계가 sin으로 정확히 맞물린다. '
           +'그래서 두 각과 한 변만 알면 나머지 변을 모두 구할 수 있다.';
    } else {
      concl='<b>확인 필요</b> — 세 비가 어긋난 기록이 있다.';
    }
    return {head:['세 각','세 비','같나?','2R','같나?','각의 합'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 코사인법칙
# ============================================================
LAB_COS = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'코사인법칙 판',
  action:'남은 변 재기',
  hint0:'두 변과 그 사이 각을 정하고, 나머지 한 변을 재 보자.',
  sliders:[
    {id:'b',label:'변 b',min:2,max:10,value:5,color:'#2563eb',unit:''},
    {id:'c',label:'변 c',min:2,max:10,value:7,color:'#16a34a',unit:''},
    {id:'A',label:'끼인각 A',min:20,max:160,value:60,color:'#f59e0b',unit:'°'}
  ],
  calc:function(S){
    var rad=S.A*Math.PI/180;
    var P=[0,0], Q=[S.c,0], R=[S.b*Math.cos(rad),S.b*Math.sin(rad)];
    var a=dist(Q,R);
    var formula=Math.sqrt(S.b*S.b+S.c*S.c-2*S.b*S.c*Math.cos(rad));
    return {P:P,Q:Q,R:R,a:a,a2:a*a,formula:formula,
            f2:S.b*S.b+S.c*S.c-2*S.b*S.c*Math.cos(rad),
            pyth:S.b*S.b+S.c*S.c};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'잰 변 a',v:ran?r3(c.a):'재 보자'},
            {k:'b²+c²−2bc cosA 의 제곱근',v:ran?r3(c.formula):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'a = '+r3(c.a)+', 공식값 '+r3(c.formula)+'.  a² = '+r2(c.a2)+', b²+c² = '+c.pyth+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var U=Math.min(30, 300/Math.max(S.b,S.c,c.a));
    var OX=90, OY=300;
    function P(p){ return [OX+p[0]*U, OY-p[1]*U]; }
    var p0=P(c.P), p1=P(c.Q), p2=P(c.R);
    ctx.beginPath();ctx.moveTo(p0[0],p0[1]);ctx.lineTo(p1[0],p1[1]);ctx.lineTo(p2[0],p2[1]);ctx.closePath();
    ctx.fillStyle='rgba(37,99,235,0.10)';ctx.fill();
    ctx.strokeStyle='#334155';ctx.lineWidth=2;ctx.stroke();
    ctx.strokeStyle='#16a34a';ctx.lineWidth=5;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(p0[0],p0[1]);ctx.lineTo(p1[0],p1[1]);ctx.stroke();
    ctx.strokeStyle='#2563eb';
    ctx.beginPath();ctx.moveTo(p0[0],p0[1]);ctx.lineTo(p2[0],p2[1]);ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      ctx.strokeStyle='#dc2626';
      ctx.beginPath();ctx.moveTo(p1[0],p1[1]);
      ctx.lineTo(p1[0]+(p2[0]-p1[0])*grow,p1[1]+(p2[1]-p1[1])*grow);ctx.stroke();
    }
    ctx.lineCap='butt';
    ctx.beginPath();ctx.arc(p0[0],p0[1],32,-S.A*Math.PI/180,0);
    ctx.strokeStyle='#b45309';ctx.lineWidth=2;ctx.stroke();
    lbl(ctx,S.A+'°',p0[0]+38,p0[1]-12,'#b45309',15);
    lbl(ctx,'c = '+S.c,(p0[0]+p1[0])/2,p0[1]+22,'#15803d',14,'center');
    lbl(ctx,'b = '+S.b,(p0[0]+p2[0])/2-34,(p0[1]+p2[1])/2,'#1d4ed8',14);
    if(grow>=1) lbl(ctx,'a = '+r3(c.a),(p1[0]+p2[0])/2+8,(p1[1]+p2[1])/2,'#b91c1c',14);
    lbl(ctx,'두 변과 끼인각으로 남은 변 구하기',24,32,'#1d4ed8',17);
    box(ctx,20,338,400,84);
    lbl(ctx,(t===null)?'a는 얼마일까?':('잰 a = '+r3(c.a)+'      a² = '+r2(c.a2)),38,368,'#1f2937',18);
    lbl(ctx,(t===null)?'':('b²+c²−2bc·cosA = '+r2(c.f2)+'      b²+c² = '+c.pyth),38,400,'#15803d',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {b:S.b,c:S.c,A:S.A,a:r3(c.a),a2:r2(c.a2),f2:r2(c.f2),pyth:c.pyth,
            ok:(Math.abs(c.a2-c.f2)<0.01),
            right:(S.A===90),
            pythOk:(Math.abs(c.a2-c.pyth)<0.01),
            cmp:(c.a2<c.pyth-0.01)?'<':((c.a2>c.pyth+0.01)?'>':'=')};
  },
  headA:['번호','b, c','각 A','잰 a','a²','b²+c²−2bc cosA','같나?','b²+c²','a²와 비교'],
  rowA:function(r,i){
    return [i+1,r.b+', '+r.c,r.A+'°','<b>'+r.a+'</b>',r.a2,r.f2,
            '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
            r.pyth,'a² '+r.cmp+' b²+c²'];
  },
  analyze:function(rec){
    var rows=[],ok=0,rt=0,rtP=0,ac=0,acLt=0,ob=0,obGt=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.ok) ok++;
      if(r.right){ rt++; if(r.pythOk) rtP++; }
      else if(r.A<90){ ac++; if(r.cmp==='<') acLt++; }
      else { ob++; if(r.cmp==='>') obGt++; }
      rows.push([r.b+', '+r.c, r.A+'°', '<b>'+r.a+'</b>', r.a2+' / '+r.f2,
                 '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
                 r.pyth, 'a² '+r.cmp+' b²+c²']);
    }
    var stats=[
      {t:'a² = b²+c²−2bc cosA',big:ok+' / '+rec.length,
       p:'좌표로 잰 변의 길이와 공식을 비교한 결과.'},
      {t:'각이 90°였던 기록',big:rt+'개',
       p:rt?('그중 a² = b²+c² 이었던 것 '+rtP+'개. cos90° = 0 이라 보정항이 사라진다.'):'각을 90°로도 해 보자.'},
      {t:'예각 / 둔각 기록',big:ac+'개 / '+ob+'개',
       p:'예각에서 a²이 더 작았던 횟수 '+acLt+', 둔각에서 더 컸던 횟수 '+obGt+'.'}
    ];
    var concl;
    if(rt===0){
      concl='<b>더 해 보자</b> — 끼인각을 <b>90°</b>로도 기록해 보자. 그때 공식이 무엇으로 바뀌는지가 핵심이다.';
    } else if(ok===rec.length){
      concl='<b>정리</b> — a² = b² + c² − 2bc·cosA 는 <b>모든 삼각형에서</b> 성립했다. '
           +'각이 90°이면 cos A = 0이라 보정항이 사라져 <b>피타고라스 정리 그 자체</b>가 된다. '
           +'예각이면 cos A > 0 이라 a²이 b²+c²보다 작아지고, 둔각이면 커졌다. '
           +'코사인법칙은 피타고라스 정리를 임의의 삼각형으로 넓힌 것이다.';
    } else {
      concl='<b>확인 필요</b> — 잰 값과 공식이 어긋난 기록이 있다.';
    }
    return {head:['b, c','각 A','a','a² / 공식','같나?','b²+c²','비교'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 등차수열
# ============================================================
LAB_ARI = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'등차수열 판',
  action:'항을 늘어놓고 더하기',
  hint0:'첫째항과 공차, 그리고 몇 번째까지 볼지 정해 보자.',
  sliders:[
    {id:'a',label:'첫째항',min:-10,max:10,value:3,color:'#2563eb',unit:''},
    {id:'d',label:'공차',min:-5,max:5,value:4,color:'#16a34a',unit:''},
    {id:'n',label:'항의 개수 n',min:1,max:20,value:8,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var arr=[],v=S.a,s=0,i;
    for(i=0;i<S.n;i++){ arr.push(v); s+=v; v+=S.d; }
    var an=arr[S.n-1];
    return {arr:arr,an:an,sum:s,
            fa:S.a+(S.n-1)*S.d,
            fs1:S.n*(S.a+an)/2,
            fs2:S.n*(2*S.a+(S.n-1)*S.d)/2};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'n번째 항',v:ran?c.an:'늘어놓아 보자'},
            {k:'합 Sₙ',v:ran?c.sum:'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'aₙ = '+c.an+' (공식 '+c.fa+'), Sₙ = '+c.sum+' (공식 '+r2(c.fs1)+'). 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*S.n);
    var mx=1,mn=0;
    for(i=0;i<S.n;i++){ if(c.arr[i]>mx) mx=c.arr[i]; if(c.arr[i]<mn) mn=c.arr[i]; }
    var GX=44, GY=280, GW=356, GH=200;
    var span=(mx-mn)||1;
    var bw=Math.min(30,GW/S.n);
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    var zeroY=GY-(0-mn)/span*GH;
    ctx.beginPath();ctx.moveTo(GX,zeroY);ctx.lineTo(GX+GW,zeroY);ctx.stroke();
    for(i=0;i<S.n;i++){
      var on=(i<shown);
      var h=(c.arr[i]-0)/span*GH;
      var x=GX+i*bw;
      ctx.fillStyle=on?'#93c5fd':'#eef2f7';
      ctx.fillRect(x,zeroY-Math.max(h,0),bw-3,Math.abs(h));
      ctx.strokeStyle=on?'#2563eb':'#e2e8f0';ctx.lineWidth=1.4;
      ctx.strokeRect(x,zeroY-Math.max(h,0),bw-3,Math.abs(h));
      if(on&&S.n<=12){
        ctx.fillStyle='#1d4ed8';ctx.font='bold 12px sans-serif';ctx.textAlign='center';
        ctx.fillText(c.arr[i],x+bw/2-1,(h>=0)?(zeroY-h-6):(zeroY-h+14));
      }
    }
    ctx.textAlign='left';
    lbl(ctx,'첫째항 '+S.a+', 공차 '+S.d,24,32,'#1d4ed8',18);
    if(shown>1) lbl(ctx,'이웃한 항의 차 : '+S.d,24,56,'#15803d',15);
    box(ctx,20,296,400,120);
    lbl(ctx,(t===null)?'n번째 항과 합은?':('a'+S.n+' = '+c.an+'      a + (n−1)d = '+c.fa),38,328,'#1f2937',18);
    lbl(ctx,(t===null)?'':('직접 더한 합 = '+c.sum),38,360,'#15803d',18);
    lbl(ctx,(t===null)?'':('n(a + aₙ)/2 = '+r2(c.fs1)+'      n(2a+(n−1)d)/2 = '+r2(c.fs2)),38,392,'#52627a',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,d:S.d,n:S.n,an:c.an,fa:c.fa,sum:c.sum,
            fs1:r2(c.fs1),fs2:r2(c.fs2),
            aOk:(c.an===c.fa),
            sOk:(Math.abs(c.sum-c.fs1)<1e-9),
            s2Ok:(Math.abs(c.sum-c.fs2)<1e-9)};
  },
  headA:['번호','첫째항, 공차','n','직접 구한 aₙ','a+(n−1)d','같나?','직접 더한 Sₙ','n(a+aₙ)/2','같나?'],
  rowA:function(r,i){
    return [i+1,r.a+', '+r.d,r.n,'<b>'+r.an+'</b>',r.fa,
            '<span class="'+(r.aOk?'ok':'no')+'">'+(r.aOk?'○':'×')+'</span>',
            '<b>'+r.sum+'</b>',r.fs1,
            '<span class="'+(r.sOk?'ok':'no')+'">'+(r.sOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],a=0,s=0,s2=0,ns={},nn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.aOk) a++;
      if(r.sOk) s++;
      if(r.s2Ok) s2++;
      if(!ns[r.n]){ ns[r.n]=true; nn++; }
      rows.push([r.a+', '+r.d, r.n, '<b>'+r.an+'</b>', r.fa,
                 '<span class="'+(r.aOk?'ok':'no')+'">'+(r.aOk?'○':'×')+'</span>',
                 '<b>'+r.sum+'</b>', r.fs1,
                 '<span class="'+(r.sOk?'ok':'no')+'">'+(r.sOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'aₙ = a + (n−1)d',big:a+' / '+rec.length,p:'하나씩 더해 만든 항과 공식을 비교한 결과.'},
      {t:'Sₙ = n(a + aₙ)/2',big:s+' / '+rec.length,p:'직접 더한 합과 비교한 결과.'},
      {t:'Sₙ = n(2a + (n−1)d)/2',big:s2+' / '+rec.length,
       p:'시험한 n '+nn+'가지. 두 합 공식은 같은 식을 다르게 쓴 것이다.'}
    ];
    var concl;
    if(a===rec.length&&s===rec.length){
      concl='<b>정리</b> — 공차 d를 (n−1)번 더한 것이 n번째 항이라서 <b>aₙ = a + (n−1)d</b> 였다. n번이 아니라 <b>n−1번</b>이다. '
           +'합은 첫 항과 끝 항을 짝지으면 그 합이 언제나 같아지므로 <b>Sₙ = n(a + aₙ)/2</b> 가 된다. '
           +'aₙ 자리에 공식을 넣으면 n(2a + (n−1)d)/2 로 같은 값이 나왔다.';
    } else {
      concl='<b>확인 필요</b> — 공식과 어긋난 기록이 있다.';
    }
    return {head:['첫째항, 공차','n','aₙ','공식','같나?','Sₙ','공식','같나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 등비수열
# ============================================================
LAB_GEO = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'등비수열 판',
  action:'항을 늘어놓고 더하기',
  hint0:'첫째항과 공비, 항의 개수를 정해 보자.',
  sliders:[
    {id:'a',label:'첫째항',min:1,max:5,value:2,color:'#2563eb',unit:''},
    {id:'r',label:'공비 (÷2)',min:-6,max:6,value:3,color:'#16a34a',
     fmt:function(v){return (v/2).toFixed(1);}},
    {id:'n',label:'항의 개수 n',min:1,max:12,value:6,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var r=S.r/2;
    if(r===0) return {zero:true,r:r};
    var arr=[],v=S.a,s=0,i;
    for(i=0;i<S.n;i++){ arr.push(v); s+=v; v*=r; }
    var an=arr[S.n-1];
    var fa=S.a*Math.pow(r,S.n-1);
    var fs=(Math.abs(r-1)<1e-12)?(S.n*S.a):(S.a*(Math.pow(r,S.n)-1)/(r-1));
    return {zero:false,r:r,arr:arr,an:an,sum:s,fa:fa,fs:fs};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    if(c.zero) return [{k:'공비 0',v:'등비수열이 아니다'},{k:'',v:'공비를 바꾸자'}];
    return [{k:'n번째 항',v:ran?r3(c.an):'늘어놓아 보자'},
            {k:'합 Sₙ',v:ran?r3(c.sum):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.zero) return '공비가 0이면 등비수열이 아니다.';
    return 'aₙ = '+r3(c.an)+' (공식 '+r3(c.fa)+'), Sₙ = '+r3(c.sum)+' (공식 '+r3(c.fs)+'). 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    if(c.zero){ lbl(ctx,'공비가 0이면 등비수열이 아니다',24,200,'#b91c1c',19); return; }
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*S.n);
    var mx=1,mn=0;
    for(i=0;i<S.n;i++){ if(c.arr[i]>mx) mx=c.arr[i]; if(c.arr[i]<mn) mn=c.arr[i]; }
    var GX=44, GY=270, GW=356, GH=190;
    var span=(mx-mn)||1;
    var bw=Math.min(30,GW/S.n);
    var zeroY=GY-(0-mn)/span*GH;
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(GX,zeroY);ctx.lineTo(GX+GW,zeroY);ctx.stroke();
    for(i=0;i<S.n;i++){
      var on=(i<shown);
      var h=c.arr[i]/span*GH;
      var x=GX+i*bw;
      ctx.fillStyle=on?'#bbf7d0':'#eef2f7';
      ctx.fillRect(x,(h>=0)?(zeroY-h):zeroY,bw-3,Math.abs(h));
      ctx.strokeStyle=on?'#16a34a':'#e2e8f0';ctx.lineWidth=1.4;
      ctx.strokeRect(x,(h>=0)?(zeroY-h):zeroY,bw-3,Math.abs(h));
      if(on&&S.n<=8){
        ctx.fillStyle='#15803d';ctx.font='bold 11px sans-serif';ctx.textAlign='center';
        ctx.fillText(r2(c.arr[i]),x+bw/2-1,(h>=0)?(zeroY-h-6):(zeroY-h+14));
      }
    }
    ctx.textAlign='left';
    lbl(ctx,'첫째항 '+S.a+', 공비 '+c.r,24,32,'#1d4ed8',18);
    if(shown>1) lbl(ctx,'이웃한 항의 비 : '+c.r,24,56,'#15803d',15);
    box(ctx,20,290,400,124);
    lbl(ctx,(t===null)?'n번째 항과 합은?':('a'+S.n+' = '+r3(c.an)+'      a·r^(n−1) = '+r3(c.fa)),38,322,'#1f2937',17);
    lbl(ctx,(t===null)?'':('직접 더한 합 = '+r3(c.sum)),38,354,'#15803d',17);
    lbl(ctx,(t===null)?'':((Math.abs(c.r-1)<1e-12)?('공비가 1이라 Sₙ = n·a = '+r3(c.fs)):('a(rⁿ−1)/(r−1) = '+r3(c.fs))),
        38,386,'#52627a',16);
  },
  record:function(S){
    var c=this.calc(S);
    if(c.zero) return {zero:true};
    return {zero:false,a:S.a,r:c.r,n:S.n,
            an:r3(c.an),fa:r3(c.fa),sum:r3(c.sum),fs:r3(c.fs),
            aOk:(Math.abs(c.an-c.fa)<1e-9),
            sOk:(Math.abs(c.sum-c.fs)<1e-9),
            one:(Math.abs(c.r-1)<1e-12)};
  },
  headA:['번호','첫째항, 공비','n','직접 구한 aₙ','a·r^(n−1)','같나?','직접 더한 Sₙ','공식','같나?','공비 1?'],
  rowA:function(r,i){
    if(r.zero) return [i+1,'공비 0','-','-','-','-','-','-','-','-'];
    return [i+1,r.a+', '+r.r,r.n,'<b>'+r.an+'</b>',r.fa,
            '<span class="'+(r.aOk?'ok':'no')+'">'+(r.aOk?'○':'×')+'</span>',
            '<b>'+r.sum+'</b>',r.fs,
            '<span class="'+(r.sOk?'ok':'no')+'">'+(r.sOk?'○':'×')+'</span>',
            r.one?'○':'×'];
  },
  analyze:function(rec){
    var rows=[],valid=0,a=0,s=0,one=0,neg=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.zero){ rows.push(['공비 0','-','-','-','-','-']); continue; }
      valid++;
      if(r.aOk) a++;
      if(r.sOk) s++;
      if(r.one) one++;
      if(r.r<0) neg++;
      rows.push([r.a+', '+r.r, r.n, '<b>'+r.an+'</b>', r.fa,
                 '<span class="'+(r.aOk?'ok':'no')+'">'+(r.aOk?'○':'×')+'</span>',
                 '<b>'+r.sum+'</b>', r.fs,
                 '<span class="'+(r.sOk?'ok':'no')+'">'+(r.sOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'aₙ = a·r^(n−1)',big:a+' / '+valid,p:'하나씩 곱해 만든 항과 공식을 비교한 결과.'},
      {t:'합 공식이 맞은 횟수',big:s+' / '+valid,p:'직접 더한 합과 비교한 결과.'},
      {t:'공비가 1이었던 기록 / 음수였던 기록',big:one+'개 / '+neg+'개',
       p:one?'공비가 1이면 분모가 0이 되어 다른 식(n·a)을 써야 한다.':'공비를 1로도 해 보자.'}
    ];
    var concl;
    if(valid===0){
      concl='<b>더 해 보자</b> — 공비를 0이 아닌 값으로 두어야 등비수열이 된다.';
    } else if(a===valid&&s===valid&&one>0){
      concl='<b>정리</b> — 공비를 (n−1)번 곱한 것이 n번째 항이라 <b>aₙ = a·r^(n−1)</b> 였고, '
           +'합은 <b>a(rⁿ−1)/(r−1)</b> 로 맞아떨어졌다. '
           +'다만 <b>공비가 1일 때는 분모가 0</b>이 되어 이 식을 쓸 수 없고, 모든 항이 같으므로 Sₙ = n·a 다. '
           +'공비가 음수면 항의 부호가 번갈아 바뀌지만 공식은 그대로 성립했다.';
    } else if(a===valid&&s===valid){
      concl='<b>정리</b> — 두 공식이 모두 맞았다. 공비를 1로 두면 어떻게 되는지도 확인해 보자.';
    } else {
      concl='<b>확인 필요</b> — 공식과 어긋난 기록이 있다.';
    }
    return {head:['첫째항, 공비','n','aₙ','공식','같나?','Sₙ','공식','같나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 시그마 공식
# ============================================================
LAB_SIGMA = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'시그마 공식판',
  action:'하나씩 더해 보기',
  hint0:'몇까지 더할지 정하고, 직접 더한 값과 공식을 비교해 보자.',
  sliders:[
    {id:'n',label:'n',min:1,max:30,value:10,color:'#2563eb',unit:''}
  ],
  calc:function(S){
    var s1=0,s2=0,s3=0,i;
    for(i=1;i<=S.n;i++){ s1+=i; s2+=i*i; s3+=i*i*i; }
    var f1=S.n*(S.n+1)/2;
    var f2=S.n*(S.n+1)*(2*S.n+1)/6;
    var f3=f1*f1;
    return {s1:s1,s2:s2,s3:s3,f1:f1,f2:f2,f3:f3};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'1+2+…+n',v:ran?c.s1:'더해 보자'},
            {k:'n(n+1)/2',v:c.f1}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'Σk = '+c.s1+', Σk² = '+c.s2+', Σk³ = '+c.s3+'.  공식값과 비교하고, Σk³과 (Σk)²도 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*S.n);
    var GX=40, GY=250, bw=Math.min(22,340/S.n);
    var mx=S.n;
    for(i=1;i<=S.n;i++){
      var on=(i<=shown);
      var h=i/mx*160;
      var x=GX+(i-1)*bw;
      ctx.fillStyle=on?'#93c5fd':'#eef2f7';
      ctx.fillRect(x,GY-h,bw-2,h);
      ctx.strokeStyle=on?'#2563eb':'#e2e8f0';ctx.lineWidth=1.2;
      ctx.strokeRect(x,GY-h,bw-2,h);
    }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+S.n*bw,GY);ctx.stroke();
    lbl(ctx,'1부터 '+S.n+'까지 막대로 쌓기',24,32,'#1d4ed8',18);
    if(shown>0) lbl(ctx,'지금까지 더한 값 : '+(shown*(shown+1)/2),GX,GY+24,'#1d4ed8',15);
    box(ctx,20,272,400,112);
    lbl(ctx,(t===null)?'세 가지 합의 공식을 확인해 보자':('Σk = '+c.s1+'   /   n(n+1)/2 = '+c.f1),38,302,'#1f2937',17);
    lbl(ctx,(t===null)?'':('Σk² = '+c.s2+'   /   n(n+1)(2n+1)/6 = '+c.f2),38,334,'#15803d',17);
    lbl(ctx,(t===null)?'':('Σk³ = '+c.s3+'   /   (Σk)² = '+c.f3),38,366,'#b45309',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {n:S.n,s1:c.s1,f1:c.f1,s2:c.s2,f2:c.f2,s3:c.s3,f3:c.f3,
            o1:(c.s1===c.f1),o2:(c.s2===c.f2),o3:(c.s3===c.f3),
            wrong2:(c.s2===c.f1*c.f1)};
  },
  headA:['번호','n','Σk','n(n+1)/2','같나?','Σk²','n(n+1)(2n+1)/6','같나?','Σk³','(Σk)²','같나?'],
  rowA:function(r,i){
    return [i+1,r.n,'<b>'+r.s1+'</b>',r.f1,
            '<span class="'+(r.o1?'ok':'no')+'">'+(r.o1?'○':'×')+'</span>',
            '<b>'+r.s2+'</b>',r.f2,
            '<span class="'+(r.o2?'ok':'no')+'">'+(r.o2?'○':'×')+'</span>',
            '<b>'+r.s3+'</b>',r.f3,
            '<span class="'+(r.o3?'ok':'no')+'">'+(r.o3?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],o1=0,o2=0,o3=0,w=0,one=0,mx=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.o1) o1++;
      if(r.o2) o2++;
      if(r.o3) o3++;
      if(r.wrong2){ w++; if(r.n===1) one++; }
      if(r.n>mx) mx=r.n;
      rows.push([r.n, r.s1+' / '+r.f1,
                 '<span class="'+(r.o1?'ok':'no')+'">'+(r.o1?'○':'×')+'</span>',
                 r.s2+' / '+r.f2,
                 '<span class="'+(r.o2?'ok':'no')+'">'+(r.o2?'○':'×')+'</span>',
                 r.s3+' / '+r.f3,
                 '<span class="'+(r.o3?'ok':'no')+'">'+(r.o3?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'Σk = n(n+1)/2',big:o1+' / '+rec.length,p:'가장 큰 n = '+mx+'까지 확인했다.'},
      {t:'Σk² = n(n+1)(2n+1)/6',big:o2+' / '+rec.length,p:'제곱의 합은 다른 공식을 쓴다.'},
      {t:'Σk³ = (Σk)²',big:o3+' / '+rec.length,
       p:w?('“Σk² = (Σk)²”가 맞은 경우 '+w+'개 (그중 n=1이 '+one+'개).'):'세제곱의 합만 제곱과 같아진다.'}
    ];
    var concl;
    if(o1===rec.length&&o2===rec.length&&o3===rec.length){
      concl='<b>정리</b> — 하나씩 더한 값이 세 공식과 모두 정확히 일치했다. '
           +'특히 <b>Σk³ = (Σk)²</b> 라는 관계가 성립하지만, <b>Σk²은 (Σk)²과 전혀 다르다.</b> '
           +'“합의 제곱”과 “제곱의 합”을 섞어 쓰면 안 된다. n이 커질수록 두 값의 차이는 급격히 벌어진다.';
    } else {
      concl='<b>확인 필요</b> — 직접 더한 값과 공식이 어긋난 기록이 있다.';
    }
    return {head:['n','Σk / 공식','같나?','Σk² / 공식','같나?','Σk³ / (Σk)²','같나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("hd_sine_law_lab_Algebra_TrigApp_Ep02.html",
     "사인법칙 실험실 — a/sinA 는 무엇일까?",
     "사인법칙 실험실 — a/sinA 는 무엇일까?",
     "꼭짓점을 옮겨 삼각형을 바꿔 가며 세 비를 재고, 외접원의 지름과 비교한다.",
     LAB_SINE),
    ("hd_cosine_law_lab_Algebra_TrigApp_Ep03.html",
     "코사인법칙 실험실 — 피타고라스는 어디로 갔을까?",
     "코사인법칙 실험실 — 피타고라스는 어디로 갔을까?",
     "두 변과 끼인각으로 남은 변을 재고, a²과 b²+c²−2bc·cosA, b²+c²을 비교한다.",
     LAB_COS),
    ("hd_arithmetic_sequence_lab_Algebra_Seq_Ep02.html",
     "등차수열 실험실 — n번째 항은 d를 몇 번 더한 걸까?",
     "등차수열 실험실 — n번째 항은 d를 몇 번 더한 걸까?",
     "항을 하나씩 만들어 더하고, 일반항과 합의 공식이 맞는지 확인한다.",
     LAB_ARI),
    ("hd_geometric_sequence_lab_Algebra_Seq_Ep07.html",
     "등비수열 실험실 — 합 공식은 언제나 쓸 수 있을까?",
     "등비수열 실험실 — 합 공식은 언제나 쓸 수 있을까?",
     "공비를 바꿔 가며 항을 만들어 더하고, 합 공식이 통하지 않는 경우를 찾는다.",
     LAB_GEO),
    ("hd_sigma_formula_lab_Algebra_Series_Ep03.html",
     "시그마 실험실 — 제곱의 합과 합의 제곱은 같을까?",
     "시그마 실험실 — 제곱의 합과 합의 제곱은 같을까?",
     "1부터 n까지의 합·제곱합·세제곱합을 직접 더해 세 공식과 대조한다.",
     LAB_SIGMA),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c26_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
