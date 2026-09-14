# -*- coding: utf-8 -*-
"""중2 ④ 삼각형과 사각형의 성질 4종"""
import os, re

OUT = "/mnt/user-data/outputs"
src = open("/home/claude/gen_math_labs.py", encoding="utf-8").read()
TPL = re.search(r'TPL = r"""(.*?)"""\n', src, re.S).group(1)

BASE = r"""
function lbl(ctx,t,x,y,c,sz,al){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
function box(ctx,x,y,w,h){ctx.fillStyle='#f1f6fd';ctx.fillRect(x,y,w,h);ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(x,y,w,h);}
function r1(v){return Math.round(v*10)/10;}
function r2(v){return Math.round(v*100)/100;}
function dist(p,q){return Math.sqrt((p[0]-q[0])*(p[0]-q[0])+(p[1]-q[1])*(p[1]-q[1]));}
function angDeg(p,q,r){
  var ax=p[0]-q[0],ay=p[1]-q[1],bx=r[0]-q[0],by=r[1]-q[1];
  var d=ax*bx+ay*by,m=Math.sqrt(ax*ax+ay*ay)*Math.sqrt(bx*bx+by*by);
  var c=(m===0)?1:d/m; if(c>1)c=1; if(c<-1)c=-1;
  return Math.acos(c)*180/Math.PI;
}
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
# 1. 이등변삼각형
# ============================================================
LAB_ISO = BASE + r"""
var LAB = {
  cw:440, ch:420, cvTitle:'이등변삼각형 판',
  action:'삼각형 그리고 각 재기',
  hint0:'밑변과 두 변의 길이를 정하고, 두 밑각을 재 보자.',
  sliders:[
    {id:'base',label:'밑변',min:80,max:240,value:180,color:'#2563eb',fmt:function(v){return (v/20).toFixed(1)+'cm';}},
    {id:'L',label:'왼쪽 변',min:60,max:190,value:150,color:'#16a34a',fmt:function(v){return (v/20).toFixed(1)+'cm';}},
    {id:'R',label:'오른쪽 변',min:60,max:190,value:150,color:'#f59e0b',fmt:function(v){return (v/20).toFixed(1)+'cm';}}
  ],
  calc:function(S){
    var A=[220-S.base/2,320], B=[220+S.base/2,320];
    var x=(S.L*S.L-S.R*S.R+S.base*S.base)/(2*S.base);
    var y2=S.L*S.L-x*x;
    var ok=(y2>1e-6);
    var C=[A[0]+x, 320-(ok?Math.sqrt(y2):0)];
    return {A:A,B:B,C:C,ok:ok,
            angA:ok?angDeg(B,A,C):0, angB:ok?angDeg(C,B,A):0, angC:ok?angDeg(A,C,B):0};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    if(!c.ok) return [{k:'삼각형',v:'만들 수 없음'},{k:'',v:'길이를 바꿔 보자'}];
    return [{k:'두 변',v:(S.L/20).toFixed(1)+' / '+(S.R/20).toFixed(1)+'cm'},
            {k:'두 밑각',v:ran?(r1(c.angA)+'° / '+r1(c.angB)+'°'):'재 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(!c.ok) return '세 변으로 삼각형을 만들 수 없다. 길이를 바꿔 보자.';
    var eqS=(S.L===S.R), eqA=(Math.abs(c.angA-c.angB)<0.05);
    return '두 밑각은 '+r1(c.angA)+'°와 '+r1(c.angB)+'°. 두 변이 '+(eqS?'같고':'다르고')+' 두 각도 '+(eqA?'같다':'다르다')+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    if(!c.ok){
      lbl(ctx,'세 변으로 삼각형을 만들 수 없다',24,200,'#b91c1c',20);
      lbl(ctx,'두 변의 합이 밑변보다 커야 한다',24,232,'#52627a',17);
      return;
    }
    poly(ctx,[c.A,c.B,c.C],'rgba(37,99,235,0.10)','#334155',false);
    ctx.strokeStyle='#16a34a';ctx.lineWidth=5;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(c.A[0],c.A[1]);ctx.lineTo(c.C[0],c.C[1]);ctx.stroke();
    ctx.strokeStyle='#f59e0b';
    ctx.beginPath();ctx.moveTo(c.B[0],c.B[1]);ctx.lineTo(c.C[0],c.C[1]);ctx.stroke();
    ctx.lineCap='butt';
    var show=(t===null)?0:Math.min(1,t);
    function sector(p,q,r,col,al){
      var a1=Math.atan2(q[1]-p[1],q[0]-p[0]), a2=Math.atan2(r[1]-p[1],r[0]-p[0]);
      var d=a2-a1; while(d<=-Math.PI)d+=2*Math.PI; while(d>Math.PI)d-=2*Math.PI;
      ctx.globalAlpha=al;
      ctx.beginPath();ctx.moveTo(p[0],p[1]);ctx.arc(p[0],p[1],32,a1,a1+d,d<0);ctx.closePath();
      ctx.fillStyle=col;ctx.fill();ctx.globalAlpha=1;
    }
    if(show>0){
      sector(c.A,c.B,c.C,'#22c55e',0.5*show);
      sector(c.B,c.C,c.A,'#f59e0b',0.5*show);
      ctx.font='bold 15px sans-serif';ctx.textAlign='center';
      ctx.fillStyle='#15803d';ctx.fillText(r1(c.angA)+'°',c.A[0]+40,c.A[1]-12);
      ctx.fillStyle='#b45309';ctx.fillText(r1(c.angB)+'°',c.B[0]-40,c.B[1]-12);
      ctx.textAlign='left';
    }
    lbl(ctx,'두 변의 길이와 두 밑각',24,36,'#1d4ed8',19);
    box(ctx,20,336,400,72);
    var eqS=(S.L===S.R), eqA=(Math.abs(c.angA-c.angB)<0.05);
    lbl(ctx,'두 변 : '+(S.L/20).toFixed(1)+' , '+(S.R/20).toFixed(1)+'cm  →  '+(eqS?'같음':'다름'),38,366,'#1f2937',18);
    lbl(ctx,(t===null)?'두 밑각은?':('두 밑각 : '+r1(c.angA)+'° , '+r1(c.angB)+'°  →  '+(eqA?'같음':'다름')),
        38,396,eqA?'#15803d':'#b91c1c',18);
  },
  record:function(S){
    var c=this.calc(S);
    if(!c.ok) return {ok:false,L:r1(S.L/20),R:r1(S.R/20)};
    return {ok:true,base:r1(S.base/20),L:r1(S.L/20),R:r1(S.R/20),
            angA:r1(c.angA),angB:r1(c.angB),
            eqS:(S.L===S.R),eqA:(Math.abs(c.angA-c.angB)<0.05)};
  },
  headA:['번호','밑변','왼쪽 변','오른쪽 변','왼쪽 밑각','오른쪽 밑각','두 변 같음','두 각 같음'],
  rowA:function(r,i){
    if(!r.ok) return [i+1,'-',r.L,r.R,'삼각형 아님','-','-','-'];
    return [i+1,r.base,r.L,r.R,r.angA+'°',r.angB+'°',
            '<span class="'+(r.eqS?'ok':'no')+'">'+(r.eqS?'○':'×')+'</span>',
            '<span class="'+(r.eqA?'ok':'no')+'">'+(r.eqA?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],match=0,valid=0,sEq=0,sEqA=0,sNe=0,sNeA=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(!r.ok){ rows.push(['삼각형 아님','-','-','-']); continue; }
      valid++;
      var m=(r.eqS===r.eqA);
      if(m) match++;
      if(r.eqS){ sEq++; if(r.eqA) sEqA++; }
      else { sNe++; if(r.eqA) sNeA++; }
      rows.push([r.L+' / '+r.R, r.angA+'° / '+r.angB+'°',
                 '<span class="'+(r.eqS?'ok':'no')+'">'+(r.eqS?'○':'×')+'</span>',
                 '<span class="'+(r.eqA?'ok':'no')+'">'+(r.eqA?'○':'×')+'</span>',
                 '<span class="'+(m?'ok':'no')+'">'+(m?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'“두 변 같음”과 “두 각 같음”이 일치',big:match+' / '+valid,
       p:'두 조건의 참·거짓이 같았던 기록 수.'},
      {t:'두 변이 같았던 기록',big:sEq+'개',
       p:sEq?('그중 두 각도 같았던 것 '+sEqA+'개.'):'두 변을 같게 한 경우도 기록해 보자.'},
      {t:'두 변이 달랐던 기록',big:sNe+'개',
       p:sNe?('그중 두 각이 같았던 것 '+sNeA+'개.'):'두 변을 다르게 한 경우도 기록해 보자.'}
    ];
    var concl;
    if(sEq===0||sNe===0){
      concl='<b>더 해 보자</b> — 두 변이 같은 경우와 다른 경우를 <b>모두</b> 기록해야 조건을 확인할 수 있다.';
    } else if(sEqA===sEq && sNeA===0){
      concl='<b>정리</b> — 두 변이 같으면 두 밑각도 같았고('+sEq+'번 모두), 두 변이 다르면 두 밑각도 달랐다('+sNe+'번 모두). '
           +'두 조건은 <b>서로를 보장</b>한다. 그래서 “두 각이 같은 삼각형은 이등변삼각형”이라는 역도 성립한다. '
           +'또 긴 변의 맞은편 각이 더 컸다.';
    } else {
      concl='<b>확인 필요</b> — 두 조건이 어긋난 기록이 있다.';
    }
    return {head:['두 변','두 밑각','두 변 같음','두 각 같음','일치?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 외심의 위치
# ============================================================
LAB_CIRC = BASE + r"""
var A=[86,320], B=[354,320];
function circum(A,B,C){
  var d=2*(A[0]*(B[1]-C[1])+B[0]*(C[1]-A[1])+C[0]*(A[1]-B[1]));
  if(Math.abs(d)<1e-9) return null;
  var ux=((A[0]*A[0]+A[1]*A[1])*(B[1]-C[1])+(B[0]*B[0]+B[1]*B[1])*(C[1]-A[1])+(C[0]*C[0]+C[1]*C[1])*(A[1]-B[1]))/d;
  var uy=((A[0]*A[0]+A[1]*A[1])*(C[0]-B[0])+(B[0]*B[0]+B[1]*B[1])*(A[0]-C[0])+(C[0]*C[0]+C[1]*C[1])*(B[0]-A[0]))/d;
  return [ux,uy];
}
function sign(p,q,r){ return (p[0]-r[0])*(q[1]-r[1])-(q[0]-r[0])*(p[1]-r[1]); }
function inTri(P,A,B,C){
  var d1=sign(P,A,B), d2=sign(P,B,C), d3=sign(P,C,A);
  var neg=(d1<-1e-9)||(d2<-1e-9)||(d3<-1e-9);
  var pos=(d1>1e-9)||(d2>1e-9)||(d3>1e-9);
  return !(neg&&pos);
}
var LAB = {
  cw:440, ch:430, cvTitle:'외심 실험판',
  action:'외접원 그리기',
  hint0:'꼭짓점을 옮겨 삼각형 모양을 바꾸고, 외심이 어디 있는지 보자.',
  sliders:[
    {id:'cx',label:'위 꼭짓점 좌우',min:20,max:420,value:160,color:'#2563eb',unit:''},
    {id:'cy',label:'위 꼭짓점 높이',min:60,max:280,value:120,color:'#16a34a',unit:''}
  ],
  calc:function(S){
    var C=[S.cx,S.cy];
    var O=circum(A,B,C);
    var angs=[angDeg(B,A,C),angDeg(C,B,A),angDeg(A,C,B)];
    var mx=Math.max(angs[0],angs[1],angs[2]);
    var kind=(mx>90.3)?'둔각삼각형':((mx>89.7)?'직각삼각형':'예각삼각형');
    var inside=O?inTri(O,A,B,C):false;
    var onEdge=false;
    if(O){
      var eps=3;
      if(Math.abs(sign(O,A,B))/dist(A,B)<eps||Math.abs(sign(O,B,C))/dist(B,C)<eps||Math.abs(sign(O,C,A))/dist(C,A)<eps) onEdge=true;
    }
    var pos=onEdge?'변 위':(inside?'내부':'외부');
    return {C:C,O:O,angs:angs,mx:mx,kind:kind,pos:pos,
            r:O?dist(O,A):0,dA:O?dist(O,A):0,dB:O?dist(O,B):0,dC:O?dist(O,C):0};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'가장 큰 각',v:r1(c.mx)+'° ('+c.kind+')'},
            {k:'외심의 위치',v:ran?c.pos:'그려 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return c.kind+'이고 외심은 삼각형의 '+c.pos+'에 있다. 세 꼭짓점까지의 거리는 모두 '+r1(c.r/20)+'cm다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var grow=(t===null)?0:Math.min(1,t);
    if(c.O&&grow>0){
      ctx.beginPath();ctx.arc(c.O[0],c.O[1],c.r,0,Math.PI*2*grow);
      ctx.strokeStyle='#93c5fd';ctx.lineWidth=2.5;ctx.stroke();
    }
    poly(ctx,[A,B,c.C],'rgba(37,99,235,0.10)','#334155',false);
    if(c.O&&grow>0.5){
      var g=(grow-0.5)/0.5;
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=2;
      [A,B,c.C].forEach(function(P){
        ctx.beginPath();ctx.moveTo(c.O[0],c.O[1]);
        ctx.lineTo(c.O[0]+(P[0]-c.O[0])*g,c.O[1]+(P[1]-c.O[1])*g);ctx.stroke();
      });
      ctx.beginPath();ctx.arc(c.O[0],c.O[1],7,0,Math.PI*2);
      ctx.fillStyle='#dc2626';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      lbl(ctx,'외심',c.O[0]+10,c.O[1]-10,'#b91c1c',15);
    }
    lbl(ctx,'외심은 항상 삼각형 안에 있을까?',24,32,'#1d4ed8',18);
    box(ctx,20,346,400,70);
    lbl(ctx,'가장 큰 각 '+r1(c.mx)+'°  →  '+c.kind,38,376,'#1f2937',19);
    lbl(ctx,(t===null)?'외심은 어디에 있을까?':('외심의 위치 : '+c.pos+'     세 거리 '+r1(c.dA/20)+' / '+r1(c.dB/20)+' / '+r1(c.dC/20)+'cm'),
        38,404,(c.pos==='내부')?'#15803d':'#b91c1c',16);
  },
  record:function(S){
    var c=this.calc(S);
    var same=(Math.abs(c.dA-c.dB)<0.5&&Math.abs(c.dB-c.dC)<0.5);
    return {mx:r1(c.mx),kind:c.kind,pos:c.pos,
            dA:r1(c.dA/20),dB:r1(c.dB/20),dC:r1(c.dC/20),same:same};
  },
  headA:['번호','가장 큰 각','삼각형 종류','외심 위치','세 꼭짓점까지 거리','모두 같은가?'],
  rowA:function(r,i){
    return [i+1,r.mx+'°',r.kind,'<b>'+r.pos+'</b>',r.dA+' / '+r.dB+' / '+r.dC,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,g={},kn=0,match=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      var expect=(r.kind==='예각삼각형')?'내부':((r.kind==='직각삼각형')?'변 위':'외부');
      var m=(expect===r.pos);
      if(m) match++;
      if(!g[r.kind]) g[r.kind]=[];
      g[r.kind].push(r.pos);
      rows.push([r.mx+'°', r.kind, '<b>'+r.pos+'</b>', r.dA+'/'+r.dB+'/'+r.dC,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 '<span class="'+(m?'ok':'no')+'">'+(m?'○':'×')+'</span>']);
    }
    var lines=[],k;
    for(k in g){ kn++; lines.push(k+' → '+g[k].join(', ')); }
    var stats=[
      {t:'세 꼭짓점까지 거리가 모두 같았던 횟수',big:same+' / '+rec.length,
       p:'외심의 정의대로 되는지 확인한 결과.'},
      {t:'시험한 삼각형 종류',big:kn+'가지',
       p:lines.join(' / ')},
      {t:'“예각→내부, 직각→변 위, 둔각→외부” 예상과 일치',big:match+' / '+rec.length,
       p:'삼각형 종류로 외심 위치를 예측할 수 있는지 확인한 결과.'}
    ];
    var concl;
    if(kn<2){
      concl='<b>더 해 보자</b> — 예각·직각·둔각삼각형을 <b>모두</b> 만들어 기록해야 위치 규칙이 보인다. 위 꼭짓점을 옆으로 크게 옮겨 보자.';
    } else if(same===rec.length&&match===rec.length){
      concl='<b>정리</b> — 외심은 언제나 세 꼭짓점에서 <b>같은 거리</b>에 있었지만, <b>항상 삼각형 안에 있지는 않았다.</b> '
           +'예각삼각형에서는 내부, 직각삼각형에서는 빗변의 중점(변 위), 둔각삼각형에서는 바깥에 있었다. '
           +'외심은 “세 변의 수직이등분선이 만나는 점”이지 “한가운데 점”이 아니다.';
    } else {
      concl='<b>정리</b> — 외심은 세 꼭짓점에서 같은 거리에 있다. 삼각형 종류를 바꿔 위치가 어떻게 달라지는지 더 기록해 보자.';
    }
    return {head:['가장 큰 각','종류','외심 위치','세 거리','모두 같은가?','예상과 일치?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 평행사변형이 되는 조건
# ============================================================
LAB_PARA2 = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'사각형 조건 판',
  action:'변의 길이와 방향 재기',
  hint0:'윗변 두 꼭짓점을 좌우로 옮겨 사각형 모양을 바꿔 보자.',
  sliders:[
    {id:'dx',label:'왼쪽 위 꼭짓점 이동',min:-70,max:70,value:-50,color:'#2563eb',unit:''},
    {id:'cx',label:'오른쪽 위 꼭짓점 이동',min:-70,max:70,value:50,color:'#dc2626',unit:''},
    {id:'h',label:'높이',min:60,max:150,value:110,color:'#16a34a',unit:''}
  ],
  calc:function(S){
    var A=[120,320], B=[320,320];
    var D=[120+S.dx,320-S.h], C=[320+S.cx,320-S.h];
    var AD=dist(A,D), BC=dist(B,C);
    var AB=dist(A,B), DC=dist(D,C);
    var sideEq=(Math.abs(AD-BC)<0.5);
    var sidePar=(S.dx===S.cx);
    var isPara=sidePar;
    return {A:A,B:B,C:C,D:D,AD:AD,BC:BC,AB:AB,DC:DC,sideEq:sideEq,sidePar:sidePar,isPara:isPara};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'두 옆변 길이',v:r1(c.AD/20)+' / '+r1(c.BC/20)+'cm'},
            {k:'평행사변형?',v:ran?(c.isPara?'예':'아니오'):'재 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.isPara) return '두 옆변이 평행하고 길이도 같다. 평행사변형이다. 기록해 보자.';
    if(c.sideEq) return '두 옆변의 길이는 같지만 평행하지 않다. 평행사변형이 아니다(등변사다리꼴). 기록해 보자.';
    return '두 옆변의 길이도 다르고 평행하지도 않다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    poly(ctx,[c.A,c.B,c.C,c.D],'rgba(37,99,235,0.10)','#334155',false);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=5;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(c.A[0],c.A[1]);ctx.lineTo(c.D[0],c.D[1]);ctx.stroke();
    ctx.strokeStyle='#dc2626';
    ctx.beginPath();ctx.moveTo(c.B[0],c.B[1]);ctx.lineTo(c.C[0],c.C[1]);ctx.stroke();
    ctx.lineCap='butt';
    var show=(t===null)?0:Math.min(1,t);
    if(show>0){
      lbl(ctx,r1(c.AD/20)+'cm',(c.A[0]+c.D[0])/2-42,(c.A[1]+c.D[1])/2,'#1d4ed8',15);
      lbl(ctx,r1(c.BC/20)+'cm',(c.B[0]+c.C[0])/2+10,(c.B[1]+c.C[1])/2,'#b91c1c',15);
      var vx=(c.D[0]-c.A[0]), vy=(c.D[1]-c.A[1]);
      var wx=(c.C[0]-c.B[0]), wy=(c.C[1]-c.B[1]);
      ctx.strokeStyle='#94a3b8';ctx.lineWidth=1.6;ctx.setLineDash([5,4]);
      ctx.beginPath();ctx.moveTo(c.A[0],c.A[1]);ctx.lineTo(c.A[0]+wx,c.A[1]+wy);ctx.stroke();
      ctx.setLineDash([]);
    }
    lbl(ctx,'아랫변과 윗변은 항상 평행 (한 쌍 평행)',24,32,'#52627a',16);
    lbl(ctx,'회색 점선 = 오른쪽 변을 왼쪽으로 옮겨 본 것',24,56,'#94a3b8',14);
    box(ctx,20,346,400,72);
    lbl(ctx,'옆변 길이 : '+(c.sideEq?'같음':'다름')+'      옆변 평행 : '+(c.sidePar?'평행':'아님'),38,376,'#1f2937',18);
    lbl(ctx,(t===null)?'이 사각형은 평행사변형일까?':(c.isPara?'평행사변형이다':(c.sideEq?'평행사변형이 아니다 (등변사다리꼴)':'평행사변형이 아니다')),
        38,404,c.isPara?'#15803d':'#b91c1c',19);
  },
  record:function(S){
    var c=this.calc(S);
    return {dx:S.dx,cx:S.cx,AD:r1(c.AD/20),BC:r1(c.BC/20),
            top:r1(c.DC/20),bottom:r1(c.AB/20),
            sideEq:c.sideEq,sidePar:c.sidePar,isPara:c.isPara};
  },
  headA:['번호','아랫변','윗변','왼쪽 옆변','오른쪽 옆변','옆변 길이 같음','옆변 평행','평행사변형?'],
  rowA:function(r,i){
    return [i+1,r.bottom,r.top,r.AD,r.BC,
            '<span class="'+(r.sideEq?'ok':'no')+'">'+(r.sideEq?'○':'×')+'</span>',
            '<span class="'+(r.sidePar?'ok':'no')+'">'+(r.sidePar?'○':'×')+'</span>',
            '<span class="'+(r.isPara?'ok':'no')+'">'+(r.isPara?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],eq=0,eqPara=0,counter=0,parN=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.sideEq){ eq++; if(r.isPara) eqPara++; else counter++; }
      if(r.isPara) parN++;
      rows.push([r.bottom+' / '+r.top, r.AD+' / '+r.BC,
                 '<span class="'+(r.sideEq?'ok':'no')+'">'+(r.sideEq?'○':'×')+'</span>',
                 '<span class="'+(r.sidePar?'ok':'no')+'">'+(r.sidePar?'○':'×')+'</span>',
                 '<span class="'+(r.isPara?'ok':'no')+'">'+(r.isPara?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'옆변 길이가 같았던 기록',big:eq+'개',
       p:eq?('그중 평행사변형이었던 것 '+eqPara+'개.'):'옆변 길이를 같게 만들어 보자(좌우 대칭으로).'},
      {t:'“한 쌍 평행 + 다른 쌍 길이 같음”인데 평행사변형이 아닌 경우',big:counter+'개',
       p:counter?'등변사다리꼴이 반례다.':'왼쪽을 −50, 오른쪽을 +50처럼 대칭으로 옮겨 보자.'},
      {t:'평행사변형이었던 기록',big:parN+'개',
       p:'두 옆변이 평행할 때(이동량이 같을 때)만 평행사변형이었다.'}
    ];
    var concl;
    if(eq===0){
      concl='<b>더 해 보자</b> — 두 옆변의 길이가 같아지도록 만들어 봐야 한다. 왼쪽 −50, 오른쪽 +50처럼 대칭으로 옮기면 된다.';
    } else if(counter>0){
      concl='<b>정리</b> — “한 쌍이 평행하고, 다른 한 쌍의 길이가 같다”만으로는 평행사변형이 되지 않았다. '
           +'<b>'+counter+'번은 등변사다리꼴</b>이었다. 평행사변형이 되려면 <b>같은 쌍이 평행하면서 길이도 같아야</b> 한다. '
           +'조건을 서로 다른 쌍에 나눠 쓰면 반례가 생긴다.';
    } else {
      concl='<b>정리</b> — 옆변이 평행할 때만 평행사변형이었다. 좌우 대칭으로 옮겨 등변사다리꼴 반례도 만들어 보자.';
    }
    return {head:['아랫변/윗변','옆변 길이','길이 같음','평행','평행사변형?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 사각형의 대각선 성질
# ============================================================
LAB_DIAG = BASE + r"""
var KINDS=['평행사변형','직사각형','마름모','정사각형','등변사다리꼴'];
function shape(kind,s){
  var k=s/60;
  var p;
  if(kind===0) p=[[-100,-50],[60,-50],[100,50],[-60,50]];
  else if(kind===1) p=[[-100,-60],[100,-60],[100,60],[-100,60]];
  else if(kind===2) p=[[-100,0],[0,-70],[100,0],[0,70]];
  else if(kind===3) p=[[-80,-80],[80,-80],[80,80],[-80,80]];
  else p=[[-110,-55],[110,-55],[65,55],[-65,55]];
  var o=[],i;
  for(i=0;i<4;i++){ o.push([220+p[i][0]*k,190+p[i][1]*k]); }
  return o;
}
var LAB = {
  cw:440, ch:400, cvTitle:'대각선 성질판',
  action:'대각선 그어 재기',
  hint0:'사각형 종류와 크기를 정하고, 두 대각선의 성질을 재 보자.',
  sliders:[
    {id:'kind',label:'사각형',min:0,max:4,value:0,color:'#2563eb',fmt:function(v){return KINDS[v];}},
    {id:'s',label:'크기',min:40,max:75,value:60,color:'#16a34a',unit:''}
  ],
  calc:function(S){
    var p=shape(S.kind,S.s);
    var d1=dist(p[0],p[2]), d2=dist(p[1],p[3]);
    var m1=[(p[0][0]+p[2][0])/2,(p[0][1]+p[2][1])/2];
    var m2=[(p[1][0]+p[3][0])/2,(p[1][1]+p[3][1])/2];
    var bisect=(dist(m1,m2)<0.6);
    var v1=[p[2][0]-p[0][0],p[2][1]-p[0][1]], v2=[p[3][0]-p[1][0],p[3][1]-p[1][1]];
    var dot=v1[0]*v2[0]+v1[1]*v2[1];
    var perp=(Math.abs(dot)/(d1*d2)<0.01);
    return {p:p,d1:d1,d2:d2,eq:(Math.abs(d1-d2)<0.6),bisect:bisect,perp:perp,m1:m1,m2:m2};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'두 대각선 길이',v:ran?(r1(c.d1/20)+' / '+r1(c.d2/20)+'cm'):'재 보자'},
            {k:'서로 이등분 / 수직',v:ran?((c.bisect?'○':'×')+' / '+(c.perp?'○':'×')):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return KINDS[S.kind]+' : 길이 '+(c.eq?'같음':'다름')+', 서로 이등분 '+(c.bisect?'○':'×')+', 수직 '+(c.perp?'○':'×')+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), p=c.p;
    poly(ctx,p,'rgba(37,99,235,0.10)','#334155',false);
    var g=(t===null)?0:Math.min(1,t);
    if(g>0){
      ctx.strokeStyle='#dc2626';ctx.lineWidth=3;
      ctx.beginPath();ctx.moveTo(p[0][0],p[0][1]);
      ctx.lineTo(p[0][0]+(p[2][0]-p[0][0])*g,p[0][1]+(p[2][1]-p[0][1])*g);ctx.stroke();
      ctx.strokeStyle='#f59e0b';
      ctx.beginPath();ctx.moveTo(p[1][0],p[1][1]);
      ctx.lineTo(p[1][0]+(p[3][0]-p[1][0])*g,p[1][1]+(p[3][1]-p[1][1])*g);ctx.stroke();
    }
    if(g>=1){
      ctx.beginPath();ctx.arc(c.m1[0],c.m1[1],5,0,Math.PI*2);ctx.fillStyle='#7c3aed';ctx.fill();
      ctx.beginPath();ctx.arc(c.m2[0],c.m2[1],5,0,Math.PI*2);ctx.fillStyle='#059669';ctx.fill();
      lbl(ctx,r1(c.d1/20)+'cm',p[0][0]+10,p[0][1]-8,'#b91c1c',14);
      lbl(ctx,r1(c.d2/20)+'cm',p[1][0]-40,p[1][1]-8,'#b45309',14);
    }
    lbl(ctx,KINDS[S.kind]+'의 두 대각선',24,32,'#1d4ed8',19);
    box(ctx,20,308,400,76);
    lbl(ctx,(t===null)?'두 대각선은 어떤 성질을 가질까?':
        ('길이 '+(c.eq?'같음':'다름')+'    서로 이등분 '+(c.bisect?'○':'×')+'    수직 '+(c.perp?'○':'×')),
        38,340,'#1f2937',18);
    lbl(ctx,(t===null)?'':('보라·초록 점 = 두 대각선의 중점 ('+(c.bisect?'겹침':'따로')+')'),38,370,'#52627a',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {kind:S.kind,name:KINDS[S.kind],d1:r1(c.d1/20),d2:r1(c.d2/20),
            eq:c.eq,bisect:c.bisect,perp:c.perp};
  },
  headA:['번호','사각형','대각선 1','대각선 2','길이 같음','서로 이등분','수직'],
  rowA:function(r,i){
    return [i+1,'<b>'+r.name+'</b>',r.d1,r.d2,
            '<span class="'+(r.eq?'ok':'no')+'">'+(r.eq?'○':'×')+'</span>',
            '<span class="'+(r.bisect?'ok':'no')+'">'+(r.bisect?'○':'×')+'</span>',
            '<span class="'+(r.perp?'ok':'no')+'">'+(r.perp?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],g={},kn=0,k;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      g[r.name]=r;
      rows.push([r.name,
                 '<span class="'+(r.eq?'ok':'no')+'">'+(r.eq?'○':'×')+'</span>',
                 '<span class="'+(r.bisect?'ok':'no')+'">'+(r.bisect?'○':'×')+'</span>',
                 '<span class="'+(r.perp?'ok':'no')+'">'+(r.perp?'○':'×')+'</span>']);
    }
    var perpOnly=[],eqOnly=[],both=[],noB=[];
    for(k in g){
      kn++;
      var x=g[k];
      if(!x.bisect) noB.push(k);
      else if(x.perp&&x.eq) both.push(k);
      else if(x.perp) perpOnly.push(k);
      else if(x.eq) eqOnly.push(k);
    }
    var stats=[
      {t:'시험한 사각형',big:kn+'가지',p:'다섯 가지를 모두 기록하면 표가 완성된다.'},
      {t:'대각선이 수직인 사각형',big:(perpOnly.concat(both)).length+'가지',
       p:(perpOnly.concat(both)).join(', ')||'마름모와 정사각형을 확인해 보자.'},
      {t:'대각선 길이가 같은 사각형',big:(eqOnly.concat(both)).length+'가지',
       p:(eqOnly.concat(both)).join(', ')||'직사각형과 정사각형을 확인해 보자.'}
    ];
    var concl;
    if(kn<4){
      concl='<b>더 해 보자</b> — 다섯 가지 사각형을 <b>모두</b> 기록해야 성질의 차이가 표로 드러난다.';
    } else {
      concl='<b>정리</b> — 대각선이 <b>서로 이등분</b>하는 것은 평행사변형 계열'
           +(noB.length?('이고, '+noB.join(', ')+'은(는) 그렇지 않았다'):'였다')+'. '
           +'그중 <b>수직</b>이면 마름모, <b>길이가 같으면</b> 직사각형, <b>둘 다면</b> 정사각형이었다. '
           +'대각선 세 가지 성질(이등분·수직·길이)의 조합이 사각형의 종류를 결정한다. '
           +'“대각선이 수직이면 마름모”는 서로 이등분한다는 조건이 함께 있어야 성립한다.';
    }
    return {head:['사각형','길이 같음','서로 이등분','수직'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("m2_isosceles_triangle_lab.html",
     "이등변삼각형 실험실 — 두 변과 두 각은 어떤 관계일까?",
     "이등변삼각형 실험실 — 두 변과 두 각은 어떤 관계일까?",
     "두 변의 길이를 바꿔 가며 두 밑각을 재고, 변이 같은 것과 각이 같은 것이 서로를 보장하는지 확인한다.",
     LAB_ISO),
    ("m2_circumcenter_lab.html",
     "외심 실험실 — 외심은 항상 삼각형 안에 있을까?",
     "외심 실험실 — 외심은 항상 삼각형 안에 있을까?",
     "꼭짓점을 옮겨 예각·직각·둔각삼각형을 만들고, 외심의 위치와 세 꼭짓점까지의 거리를 기록한다.",
     LAB_CIRC),
    ("m2_parallelogram_condition_lab.html",
     "평행사변형 실험실 — 한 쌍 평행 + 한 쌍 같으면 될까?",
     "평행사변형 실험실 — 한 쌍 평행 + 한 쌍 같으면 될까?",
     "윗변 꼭짓점을 옮겨 옆변의 길이와 방향을 재고, 평행사변형이 되는 조건의 반례를 찾는다.",
     LAB_PARA2),
    ("m2_quadrilateral_diagonals_lab.html",
     "대각선 실험실 — 어떤 사각형이 어떤 대각선을 가질까?",
     "대각선 실험실 — 어떤 사각형이 어떤 대각선을 가질까?",
     "다섯 가지 사각형의 두 대각선을 그어 길이·이등분·수직 여부를 재고 표로 정리한다.",
     LAB_DIAG),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c15_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
