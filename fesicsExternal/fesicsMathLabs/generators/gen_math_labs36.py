# -*- coding: utf-8 -*-
"""중2 보강 5종 (2)"""
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
function sgc(v,s){ if(v===0) return ''; return (v<0)?(' − '+(-v)+s):(' + '+v+s); }
function dist(p,q){return Math.sqrt((p[0]-q[0])*(p[0]-q[0])+(p[1]-q[1])*(p[1]-q[1]));}
function distLine(P,A,B){
  var vx=B[0]-A[0], vy=B[1]-A[1];
  var L=Math.sqrt(vx*vx+vy*vy);
  if(L===0) return dist(P,A);
  return Math.abs(vx*(A[1]-P[1])-vy*(A[0]-P[0]))/L;
}
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
# 1. 일차방정식의 그래프
# ============================================================
LAB_LINEQ = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'일차방정식 그래프판',
  action:'그래프 그리기',
  hint0:'ax + by + c = 0 의 계수를 정해 보자.',
  sliders:[
    {id:'a',label:'a',min:-4,max:4,value:2,color:'#2563eb',unit:''},
    {id:'b',label:'b',min:-4,max:4,value:1,color:'#16a34a',unit:''},
    {id:'c',label:'c',min:-6,max:6,value:-4,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    if(S.a===0&&S.b===0) return {none:true,ok:(S.c===0)};
    if(S.b===0) return {none:false,vertical:true,x:-S.c/S.a,func:false};
    if(S.a===0) return {none:false,vertical:false,horiz:true,m:0,n:-S.c/S.b,func:true};
    return {none:false,vertical:false,m:-S.a/S.b,n:-S.c/S.b,func:true};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    if(c.none) return [{k:'a = b = 0',v:(c.ok?'모든 점':'그래프 없음')},{k:'',v:'계수를 바꾸자'}];
    if(c.vertical) return [{k:'y = 꼴로',v:'쓸 수 없다'},{k:'그래프',v:ran?('x = '+r2(c.x)+' (세로선)'):'그려 보자'}];
    return [{k:'y = 꼴로',v:'y = '+r2(c.m)+'x'+sg(r2(c.n))},
            {k:'함수인가',v:ran?'예':'그려 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.none) return 'a와 b가 모두 0이라 직선이 되지 않는다.';
    if(c.vertical) return 'b = 0 이라 x = '+r2(c.x)+' 인 세로선이다. 한 x에 y가 여러 개라 <b>함수가 아니다</b>. 기록해 보자.';
    return 'y = '+r2(c.m)+'x'+sg(r2(c.n))+' 로 쓸 수 있다. 함수다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,7,6);
    if(c.none){ lbl(ctx,'a와 b가 모두 0이다',24,32,'#b91c1c',18); return; }
    var grow=(t===null)?0:Math.min(1,t);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;
    if(c.vertical){
      ctx.beginPath();ctx.moveTo(CX+c.x*U,CY-6*U);ctx.lineTo(CX+c.x*U,CY+6*U);ctx.stroke();
    } else {
      ctx.beginPath();
      var st=false;
      for(i=-70;i<=70;i++){
        var x=i/10, y=c.m*x+c.n;
        if(y<-6||y>6){ st=false; continue; }
        if(!st){ ctx.moveTo(CX+x*U,CY-y*U); st=true; } else ctx.lineTo(CX+x*U,CY-y*U);
      }
      ctx.stroke();
    }
    if(grow>0){
      var tx=c.vertical?c.x:1;
      ctx.strokeStyle='#dc2626';ctx.lineWidth=2.4;ctx.setLineDash([5,4]);
      ctx.beginPath();ctx.moveTo(CX+tx*U,CY-6*U);ctx.lineTo(CX+tx*U,CY+6*U);ctx.stroke();ctx.setLineDash([]);
      lbl(ctx,'세로선 x = '+r2(tx),CX+tx*U+8,CY-5.5*U,'#b91c1c',13);
      if(c.vertical&&grow>=1){
        for(i=-5;i<=5;i++){
          ctx.beginPath();ctx.arc(CX+tx*U,CY-i*U,5,0,Math.PI*2);
          ctx.fillStyle='#dc2626';ctx.fill();
        }
        lbl(ctx,'y가 여러 개!',CX+tx*U+10,CY+30,'#b91c1c',14);
      } else if(grow>=1){
        var yy=c.m*tx+c.n;
        if(Math.abs(yy)<=6){
          ctx.beginPath();ctx.arc(CX+tx*U,CY-yy*U,7,0,Math.PI*2);
          ctx.fillStyle='#15803d';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
          lbl(ctx,'y 하나',CX+tx*U+10,CY-yy*U-8,'#15803d',14);
        }
      }
    }
    lbl(ctx,S.a+'x'+sgc(S.b,'y')+sg(S.c)+' = 0',24,32,'#1d4ed8',18);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'y = 꼴로 쓸 수 있을까?':(c.vertical?('x = '+r2(c.x)+' — y = 꼴로 쓸 수 없다'):('y = '+r2(c.m)+'x'+sg(r2(c.n)))),
        38,376,c.vertical?'#b91c1c':'#15803d',18);
    lbl(ctx,(t===null)?'':(c.vertical?'세로선이라 함수가 아니다':'한 x에 y가 하나 — 함수다'),
        38,406,'#52627a',17);
  },
  record:function(S){
    var c=this.calc(S);
    if(c.none) return {none:true,a:S.a,b:S.b,c:S.c};
    return {none:false,a:S.a,b:S.b,c:S.c,
            vertical:!!c.vertical,func:!!c.func,
            form:c.vertical?('x = '+r2(c.x)):('y = '+r2(c.m)+'x'+sg(r2(c.n))),
            line:true,bZero:(S.b===0)};
  },
  headA:['번호','식','b','직선인가?','y = 꼴','함수인가?'],
  rowA:function(r,i){
    if(r.none) return [i+1,'a=b=0','-','×','-','-'];
    return [i+1,r.a+'x'+sgc(r.b,'y')+sg(r.c)+'=0',r.b,
            '<span class="ok">○</span>','<b>'+r.form+'</b>',
            '<span class="'+(r.func?'ok':'no')+'">'+(r.func?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],valid=0,line=0,func=0,bz=0,bzFunc=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.none){ rows.push(['a=b=0','-','×','-','-']); continue; }
      valid++;
      if(r.line) line++;
      if(r.func) func++;
      if(r.bZero){ bz++; if(r.func) bzFunc++; }
      rows.push([r.a+'x'+sgc(r.b,'y')+sg(r.c)+'=0', r.b,
                 '<span class="ok">○</span>', '<b>'+r.form+'</b>',
                 '<span class="'+(r.func?'ok':'no')+'">'+(r.func?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'그래프가 직선이었던 횟수',big:line+' / '+valid,p:'일차방정식의 그래프는 언제나 직선이다.'},
      {t:'일차함수이기도 했던 횟수',big:func+' / '+valid,p:'y = 꼴로 쓸 수 있었는지 확인한 결과.'},
      {t:'b = 0 이었던 기록',big:bz+'개',
       p:bz?('그중 함수였던 것 '+bzFunc+'개.'):'b를 0으로 두어 세로선을 만들어 보자.'}
    ];
    var concl;
    if(bz===0){
      concl='<b>더 해 보자</b> — <b>b = 0</b> 으로 두면 그래프가 어떤 모양이 되는지 확인해 보자.';
    } else if(line===valid&&bzFunc===0){
      concl='<b>정리</b> — ax + by + c = 0 의 그래프는 <b>언제나 직선</b>이었지만, <b>b = 0 일 때는 함수가 아니었다.</b> '
           +'세로선은 한 x에 y가 무수히 대응해 «하나로 정해진다»는 함수의 조건을 어긴다. '
           +'b ≠ 0 일 때만 y = (−a/b)x + (−c/b) 로 고쳐 쓸 수 있고 그때 일차함수가 된다. '
           +'«직선의 방정식»과 «일차함수»는 같은 말이 아니다.';
    } else {
      concl='<b>확인 필요</b> — 판정이 어긋난 기록이 있다.';
    }
    return {head:['식','b','직선?','y = 꼴','함수?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 삼각형의 내심
# ============================================================
LAB_INC = BASE + r"""
var A=[86,330], B=[354,330];
var LAB = {
  cw:440, ch:430, cvTitle:'내심 실험판',
  action:'내접원 그리기',
  hint0:'꼭짓점을 옮겨 삼각형 모양을 바꾸고, 내심의 위치를 보자.',
  sliders:[
    {id:'cx',label:'위 꼭짓점 좌우',min:20,max:420,value:160,color:'#2563eb',unit:''},
    {id:'cy',label:'위 꼭짓점 높이',min:60,max:280,value:120,color:'#16a34a',unit:''}
  ],
  calc:function(S){
    var C=[S.cx,S.cy];
    var a=dist(B,C), b=dist(C,A), c=dist(A,B);
    var s=a+b+c;
    var I=[(a*A[0]+b*B[0]+c*C[0])/s,(a*A[1]+b*B[1]+c*C[1])/s];
    var d1=distLine(I,A,B), d2=distLine(I,B,C), d3=distLine(I,C,A);
    var sign=function(p,q,r){ return (p[0]-r[0])*(q[1]-r[1])-(q[0]-r[0])*(p[1]-r[1]); };
    var s1=sign(I,A,B), s2=sign(I,B,C), s3=sign(I,C,A);
    var neg=(s1<0)||(s2<0)||(s3<0), pos=(s1>0)||(s2>0)||(s3>0);
    var angs=[0,0,0];
    return {C:C,I:I,r:d1,d1:d1,d2:d2,d3:d3,
            inside:!(neg&&pos),
            area:Math.abs((B[0]-A[0])*(C[1]-A[1])-(C[0]-A[0])*(B[1]-A[1]))/2,
            peri:s};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'세 변까지 거리',v:ran?(r2(c.d1/20)+' / '+r2(c.d2/20)+' / '+r2(c.d3/20)):'그려 보자'},
            {k:'내심의 위치',v:ran?(c.inside?'내부':'외부'):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '세 변까지의 거리가 모두 '+r2(c.d1/20)+'cm로 같다. 내심은 삼각형 '+(c.inside?'내부':'외부')+'에 있다. 모양을 바꿔 다시 해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var grow=(t===null)?0:Math.min(1,t);
    ctx.beginPath();ctx.moveTo(A[0],A[1]);ctx.lineTo(B[0],B[1]);ctx.lineTo(c.C[0],c.C[1]);ctx.closePath();
    ctx.fillStyle='rgba(37,99,235,0.08)';ctx.fill();
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;ctx.stroke();
    if(grow>0){
      ctx.beginPath();ctx.arc(c.I[0],c.I[1],c.r*grow,0,Math.PI*2);
      ctx.strokeStyle='#16a34a';ctx.lineWidth=2.5;ctx.stroke();
    }
    if(grow>0.5){
      var g=(grow-0.5)/0.5;
      [[A,B],[B,c.C],[c.C,A]].forEach(function(sd){
        var vx=sd[1][0]-sd[0][0], vy=sd[1][1]-sd[0][1];
        var L=Math.sqrt(vx*vx+vy*vy);
        var tt=((c.I[0]-sd[0][0])*vx+(c.I[1]-sd[0][1])*vy)/(L*L);
        var F=[sd[0][0]+vx*tt,sd[0][1]+vy*tt];
        ctx.strokeStyle='#f59e0b';ctx.lineWidth=2.4;
        ctx.beginPath();ctx.moveTo(c.I[0],c.I[1]);
        ctx.lineTo(c.I[0]+(F[0]-c.I[0])*g,c.I[1]+(F[1]-c.I[1])*g);ctx.stroke();
      });
      ctx.beginPath();ctx.arc(c.I[0],c.I[1],7,0,Math.PI*2);
      ctx.fillStyle='#dc2626';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      lbl(ctx,'내심',c.I[0]+10,c.I[1]-10,'#b91c1c',15);
    }
    lbl(ctx,'내심은 삼각형 밖으로 나갈까?',24,32,'#1d4ed8',18);
    box(ctx,20,346,400,74);
    lbl(ctx,'세 변까지 거리 '+r2(c.d1/20)+' / '+r2(c.d2/20)+' / '+r2(c.d3/20)+'cm',38,376,'#1f2937',17);
    lbl(ctx,(t===null)?'내심은 어디에 있을까?':('내심의 위치 : '+(c.inside?'내부':'외부')+'      내접원 반지름 '+r2(c.r/20)+'cm'),
        38,406,c.inside?'#15803d':'#b91c1c',16);
  },
  record:function(S){
    var c=this.calc(S);
    var same=(Math.abs(c.d1-c.d2)<0.5&&Math.abs(c.d2-c.d3)<0.5);
    return {cx:S.cx,cy:S.cy,
            d1:r2(c.d1/20),d2:r2(c.d2/20),d3:r2(c.d3/20),
            same:same,inside:c.inside,
            r:r2(c.r/20),
            areaOk:(Math.abs(c.r*c.peri/2-c.area)<2)};
  },
  headA:['번호','위 꼭짓점','세 변까지 거리','모두 같은가?','내심의 위치','내접원 반지름','넓이 = r·둘레/2?'],
  rowA:function(r,i){
    return [i+1,'('+r.cx+', '+r.cy+')',r.d1+' / '+r.d2+' / '+r.d3,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            '<b>'+(r.inside?'내부':'외부')+'</b>',r.r,
            '<span class="'+(r.areaOk?'ok':'no')+'">'+(r.areaOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,inside=0,area=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.inside) inside++;
      if(r.areaOk) area++;
      rows.push(['('+r.cx+', '+r.cy+')', r.d1+' / '+r.d2+' / '+r.d3,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 '<b>'+(r.inside?'내부':'외부')+'</b>', r.r,
                 '<span class="'+(r.areaOk?'ok':'no')+'">'+(r.areaOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'세 변까지 거리가 모두 같음',big:same+' / '+rec.length,p:'내심의 정의대로 되는지 확인한 결과.'},
      {t:'내심이 삼각형 내부에 있었던 횟수',big:inside+' / '+rec.length,
       p:'모양을 아무리 바꿔도 밖으로 나갔는지 확인했다.'},
      {t:'삼각형 넓이 = (내접원 반지름 × 둘레) ÷ 2',big:area+' / '+rec.length,
       p:'세 개의 작은 삼각형으로 나누면 나오는 관계다.'}
    ];
    var concl;
    if(same===rec.length&&inside===rec.length){
      concl='<b>정리</b> — 내심은 세 변에서 <b>같은 거리</b>에 있었고, 삼각형 모양을 아무리 바꿔도 <b>언제나 내부</b>에 있었다. '
           +'외심이 둔각삼각형에서 밖으로 나갔던 것과 대조된다. '
           +'내심은 «세 내각의 이등분선이 만나는 점»이고 각의 이등분선은 삼각형 안을 지나기 때문이다. '
           +'그 거리가 곧 내접원의 반지름이고, 삼각형 넓이는 (반지름 × 둘레) ÷ 2 로도 구해졌다.';
    } else {
      concl='<b>확인 필요</b> — 거리가 다르거나 내심이 밖으로 나간 기록이 있다.';
    }
    return {head:['위 꼭짓점','세 거리','같은가?','위치','반지름','넓이 관계'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 삼각형의 무게중심
# ============================================================
LAB_CENT = BASE + r"""
var A=[86,330], B=[354,330];
var LAB = {
  cw:440, ch:430, cvTitle:'무게중심 판',
  action:'중선 긋고 재기',
  hint0:'꼭짓점을 옮겨 삼각형 모양을 바꿔 보자.',
  sliders:[
    {id:'cx',label:'위 꼭짓점 좌우',min:20,max:420,value:180,color:'#2563eb',unit:''},
    {id:'cy',label:'위 꼭짓점 높이',min:60,max:280,value:110,color:'#16a34a',unit:''}
  ],
  calc:function(S){
    var C=[S.cx,S.cy];
    var G=[(A[0]+B[0]+C[0])/3,(A[1]+B[1]+C[1])/3];
    var Ma=[(B[0]+C[0])/2,(B[1]+C[1])/2];
    var Mb=[(A[0]+C[0])/2,(A[1]+C[1])/2];
    var Mc=[(A[0]+B[0])/2,(A[1]+B[1])/2];
    return {C:C,G:G,Ma:Ma,Mb:Mb,Mc:Mc,
            ag:dist(A,G),gm:dist(G,Ma),
            bg:dist(B,G),gm2:dist(G,Mb),
            ratio:dist(A,G)/dist(G,Ma)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'A에서 G까지 : G에서 중점까지',v:ran?(r2(c.ag/20)+' : '+r2(c.gm/20)):'재 보자'},
            {k:'비',v:ran?r3(c.ratio):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '중선을 '+r2(c.ag/20)+' : '+r2(c.gm/20)+' = '+r3(c.ratio)+' : 1 로 나눈다. 모양을 바꿔 다시 재 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var grow=(t===null)?0:Math.min(1,t);
    ctx.beginPath();ctx.moveTo(A[0],A[1]);ctx.lineTo(B[0],B[1]);ctx.lineTo(c.C[0],c.C[1]);ctx.closePath();
    ctx.fillStyle='rgba(37,99,235,0.08)';ctx.fill();
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;ctx.stroke();
    var meds=[[A,c.Ma,'#dc2626'],[B,c.Mb,'#f59e0b'],[c.C,c.Mc,'#16a34a']];
    var n=Math.floor(grow*3)+((grow>0)?1:0);
    for(var i=0;i<3;i++){
      if(i>=Math.ceil(grow*3)) break;
      ctx.strokeStyle=meds[i][2];ctx.lineWidth=2.4;
      ctx.beginPath();ctx.moveTo(meds[i][0][0],meds[i][0][1]);ctx.lineTo(meds[i][1][0],meds[i][1][1]);ctx.stroke();
      ctx.beginPath();ctx.arc(meds[i][1][0],meds[i][1][1],5,0,Math.PI*2);
      ctx.fillStyle=meds[i][2];ctx.fill();
    }
    if(grow>=1){
      ctx.beginPath();ctx.arc(c.G[0],c.G[1],8,0,Math.PI*2);
      ctx.fillStyle='#7c3aed';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      lbl(ctx,'G',c.G[0]+12,c.G[1]-8,'#6d28d9',16);
      lbl(ctx,r2(c.ag/20),(A[0]+c.G[0])/2-16,(A[1]+c.G[1])/2,'#b91c1c',13);
      lbl(ctx,r2(c.gm/20),(c.G[0]+c.Ma[0])/2+6,(c.G[1]+c.Ma[1])/2,'#b91c1c',13);
    }
    lbl(ctx,'세 중선은 한 점에서 만날까?',24,32,'#1d4ed8',18);
    box(ctx,20,346,400,74);
    lbl(ctx,'A~G : G~중점 = '+r2(c.ag/20)+' : '+r2(c.gm/20),38,376,'#1f2937',18);
    lbl(ctx,(t===null)?'중선을 어떤 비로 나눌까?':('비 = '+r3(c.ratio)+' : 1      B쪽도 '+r3(c.bg/c.gm2)+' : 1'),
        38,406,'#15803d',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {cx:S.cx,cy:S.cy,
            ag:r2(c.ag/20),gm:r2(c.gm/20),ratio:r3(c.ratio),
            ratio2:r3(c.bg/c.gm2),
            two:(Math.abs(c.ratio-2)<0.01),
            two2:(Math.abs(c.bg/c.gm2-2)<0.01),
            gx:r1(c.G[0]),gy:r1(c.G[1])};
  },
  headA:['번호','위 꼭짓점','A~G','G~중점','비','2:1인가?','B쪽 비','2:1인가?'],
  rowA:function(r,i){
    return [i+1,'('+r.cx+', '+r.cy+')',r.ag,r.gm,'<b>'+r.ratio+'</b>',
            '<span class="'+(r.two?'ok':'no')+'">'+(r.two?'○':'×')+'</span>',
            r.ratio2,
            '<span class="'+(r.two2?'ok':'no')+'">'+(r.two2?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],two=0,two2=0,mn=9,mx=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.two) two++;
      if(r.two2) two2++;
      var v=parseFloat(r.ratio);
      if(v<mn) mn=v;
      if(v>mx) mx=v;
      rows.push(['('+r.cx+', '+r.cy+')', r.ag+' : '+r.gm, '<b>'+r.ratio+'</b>',
                 '<span class="'+(r.two?'ok':'no')+'">'+(r.two?'○':'×')+'</span>',
                 r.ratio2,
                 '<span class="'+(r.two2?'ok':'no')+'">'+(r.two2?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'A쪽 중선이 2 : 1 로 나뉨',big:two+' / '+rec.length,p:'꼭짓점에서 무게중심까지가 두 배인지 확인한 결과.'},
      {t:'B쪽 중선도 2 : 1',big:two2+' / '+rec.length,p:'어느 중선을 재도 같은 비였다.'},
      {t:'비의 범위',big:mn+' ~ '+mx,p:'삼각형 모양을 바꿔도 비는 움직이지 않았다.'}
    ];
    var concl;
    if(two===rec.length&&two2===rec.length){
      concl='<b>정리</b> — 세 중선은 언제나 <b>한 점에서 만났고</b>, 그 점은 각 중선을 <b>꼭짓점 쪽부터 2 : 1</b> 로 나눴다. '
           +'삼각형 모양을 아무리 바꿔도 비가 변하지 않았다. 이 점이 무게중심이고, 판지로 삼각형을 오려 이 점을 받치면 균형이 잡힌다. '
           +'중점(1:1)과 헷갈리기 쉽지만 무게중심은 <b>중점이 아니라 2:1 지점</b>이다.';
    } else {
      concl='<b>확인 필요</b> — 비가 2 : 1 이 아닌 기록이 있다.';
    }
    return {head:['위 꼭짓점','A~G : G~중점','비','2:1?','B쪽 비','2:1?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 닮음비와 넓이비·부피비
# ============================================================
LAB_SIMR = BASE + r"""
var KINDS=['삼각형','직육면체'];
var LAB = {
  cw:440, ch:430, cvTitle:'닮음 확대판',
  action:'k배로 늘려 보기',
  hint0:'도형과 닮음비를 정해 보자.',
  sliders:[
    {id:'kind',label:'도형',min:0,max:1,value:0,color:'#2563eb',fmt:function(v){return KINDS[v];}},
    {id:'k',label:'닮음비 k',min:2,max:4,value:2,color:'#f59e0b',unit:'배'},
    {id:'s',label:'처음 크기',min:2,max:5,value:3,color:'#16a34a',unit:''}
  ],
  calc:function(S){
    var s=S.s, k=S.k;
    if(S.kind===0){
      var a1=s*s*Math.sqrt(3)/4, a2=(s*k)*(s*k)*Math.sqrt(3)/4;
      var p1=3*s, p2=3*s*k;
      return {len1:s,len2:s*k,per1:p1,per2:p2,ar1:a1,ar2:a2,
              perR:p2/p1,arR:a2/a1,vol:false};
    }
    var A1=6*s*s, A2=6*(s*k)*(s*k);
    var V1=s*s*s, V2=(s*k)*(s*k)*(s*k);
    return {len1:s,len2:s*k,per1:12*s,per2:12*s*k,ar1:A1,ar2:A2,
            v1:V1,v2:V2,perR:(12*s*k)/(12*s),arR:A2/A1,volR:V2/V1,vol:true};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'넓이비',v:ran?r3(c.arR):'늘려 보자'},
            {k:c.vol?'부피비':'둘레비',v:ran?(c.vol?r3(c.volR):r3(c.perR)):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '길이는 '+S.k+'배, 넓이는 '+r3(c.arR)+'배'+(c.vol?(', 부피는 '+r3(c.volR)+'배'):'')+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var grow=(t===null)?0:Math.min(1,t);
    var cur=S.s*(1+(S.k-1)*grow);
    if(S.kind===0){
      var u=Math.min(26,300/(S.s*S.k));
      function tri(side,col,fill){
        var h=side*Math.sqrt(3)/2*u;
        var X=60, Y=320;
        ctx.beginPath();ctx.moveTo(X,Y);ctx.lineTo(X+side*u,Y);ctx.lineTo(X+side*u/2,Y-h);ctx.closePath();
        if(fill){ ctx.fillStyle=fill;ctx.fill(); }
        ctx.strokeStyle=col;ctx.lineWidth=2.6;ctx.stroke();
      }
      tri(cur,'#d97706','rgba(245,158,11,0.18)');
      tri(S.s,'#2563eb','rgba(37,99,235,0.25)');
    } else {
      var u2=Math.min(30,260/(S.s*S.k*1.5));
      function boxd(side,col,fill){
        var X=70, Y=320, d=side*u2*0.45;
        var w=side*u2;
        ctx.fillStyle=fill;
        ctx.fillRect(X,Y-w,w,w);
        ctx.strokeStyle=col;ctx.lineWidth=2.4;ctx.strokeRect(X,Y-w,w,w);
        ctx.beginPath();
        ctx.moveTo(X,Y-w);ctx.lineTo(X+d,Y-w-d);
        ctx.lineTo(X+w+d,Y-w-d);ctx.lineTo(X+w,Y-w);
        ctx.moveTo(X+w,Y);ctx.lineTo(X+w+d,Y-d);ctx.lineTo(X+w+d,Y-w-d);
        ctx.stroke();
      }
      boxd(cur,'#d97706','rgba(245,158,11,0.18)');
      boxd(S.s,'#2563eb','rgba(37,99,235,0.25)');
    }
    lbl(ctx,KINDS[S.kind]+' 을 '+S.k+'배로 확대',24,32,'#1d4ed8',18);
    box(ctx,20,340,400,80);
    lbl(ctx,'길이 '+c.len1+' → '+c.len2+'   ('+S.k+'배)',38,370,'#52627a',17);
    lbl(ctx,(t===null)?'넓이와 부피는 몇 배가 될까?':
        ('넓이 '+r2(c.ar1)+' → '+r2(c.ar2)+' ('+r3(c.arR)+'배)'+(c.vol?('   부피 '+c.v1+' → '+c.v2+' ('+r3(c.volR)+'배)'):'')),
        38,402,'#1f2937',15);
  },
  record:function(S){
    var c=this.calc(S);
    return {kind:S.kind,name:KINDS[S.kind],k:S.k,s:S.s,
            lenR:S.k,arR:r3(c.arR),volR:c.vol?r3(c.volR):'-',
            k2:S.k*S.k,k3:S.k*S.k*S.k,
            arOk:(Math.abs(c.arR-S.k*S.k)<0.01),
            volOk:c.vol?(Math.abs(c.volR-S.k*S.k*S.k)<0.01):true,
            linOk:(Math.abs(c.arR-S.k)<0.01),
            vol:c.vol};
  },
  headA:['번호','도형','k','넓이비','k²','같나?','부피비','k³','같나?','넓이비 = k?'],
  rowA:function(r,i){
    return [i+1,r.name,r.k+'배','<b>'+r.arR+'</b>',r.k2,
            '<span class="'+(r.arOk?'ok':'no')+'">'+(r.arOk?'○':'×')+'</span>',
            r.volR,r.vol?r.k3:'-',
            '<span class="'+(r.volOk?'ok':'no')+'">'+(r.volOk?'○':'×')+'</span>',
            '<span class="'+(r.linOk?'ok':'no')+'">'+(r.linOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ar=0,vo=0,lin=0,vn=0,kinds={},kn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.arOk) ar++;
      if(r.vol){ vn++; if(r.volOk) vo++; }
      if(r.linOk) lin++;
      if(!kinds[r.name]){ kinds[r.name]=true; kn++; }
      rows.push([r.name, r.k+'배', '<b>'+r.arR+'</b>', r.k2,
                 '<span class="'+(r.arOk?'ok':'no')+'">'+(r.arOk?'○':'×')+'</span>',
                 r.volR, r.vol?r.k3:'-',
                 '<span class="'+(r.volOk?'ok':'no')+'">'+(r.volOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'넓이비 = k²',big:ar+' / '+rec.length,p:'실제 넓이를 계산해 비교한 결과.'},
      {t:'부피비 = k³',big:vn?(vo+' / '+vn):'기록 없음',
       p:vn?'직육면체 기록만 셈.':'직육면체도 기록해 보자.'},
      {t:'넓이비 = k 였던 횟수',big:lin+' / '+rec.length,
       p:'길이비를 그대로 쓰면 어떻게 되는지 확인한 결과. 시험한 도형 '+kn+'가지.'}
    ];
    var concl;
    if(vn===0){
      concl='<b>더 해 보자</b> — <b>직육면체</b>도 기록해 부피비가 어떻게 되는지 확인해 보자.';
    } else if(ar===rec.length&&vo===vn&&lin===0){
      concl='<b>정리</b> — 닮음비가 k일 때 <b>길이는 k배, 넓이는 k²배, 부피는 k³배</b>였다. '
           +'넓이는 두 방향, 부피는 세 방향으로 함께 늘어나기 때문이다. '
           +'2배로 확대하면 넓이는 4배, 부피는 8배가 되므로 «두 배»라고 답하면 크게 틀린다. '
           +'둘레처럼 길이인 양만 k배 그대로다.';
    } else {
      concl='<b>확인 필요</b> — 계산한 비와 공식이 어긋난 기록이 있다.';
    }
    return {head:['도형','k','넓이비','k²','같나?','부피비','k³','같나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 적어도 하나의 확률
# ============================================================
LAB_ATLEAST = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'적어도 하나 판',
  action:'여사건으로 구하기',
  hint0:'주사위를 몇 번 던질지 정해 보자. 1의 눈이 «적어도 한 번» 나올 확률을 구한다.',
  sliders:[
    {id:'n',label:'던지는 횟수',min:1,max:12,value:6,color:'#2563eb',unit:'번'}
  ],
  calc:function(S){
    var none=Math.pow(5/6,S.n);
    return {none:none,at:1-none,naive:S.n/6,
            over:(S.n/6>1)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'한 번도 안 나올 확률',v:ran?r4(c.none):'구해 보자'},
            {k:'적어도 한 번',v:ran?r4(c.at):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '한 번도 안 나올 확률 '+r4(c.none)+', 적어도 한 번 '+r4(c.at)+'.  n/6 = '+r3(c.naive)+'와 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var BX=40, BW=360, BY=110;
    var grow=(t===null)?0:Math.min(1,t);
    ctx.fillStyle='#f1f5f9';ctx.fillRect(BX,BY,BW,40);
    ctx.fillStyle='#bfdbfe';ctx.fillRect(BX,BY,BW*c.none*grow,40);
    ctx.strokeStyle='#334155';ctx.lineWidth=2;ctx.strokeRect(BX,BY,BW,40);
    if(grow>=1){
      lbl(ctx,'한 번도 안 나옴 '+r3(c.none),BX+6,BY+26,'#1d4ed8',14);
      ctx.fillStyle='rgba(34,197,94,0.35)';
      ctx.fillRect(BX+BW*c.none,BY+50,BW*c.at,40);
      ctx.strokeStyle='#15803d';ctx.lineWidth=2;ctx.strokeRect(BX,BY+50,BW,40);
      lbl(ctx,'적어도 한 번 '+r3(c.at),BX+BW*c.none+6,BY+76,'#15803d',14);
    } else {
      ctx.strokeStyle='#cbd5e1';ctx.lineWidth=2;ctx.strokeRect(BX,BY+50,BW,40);
    }
    var GX=40, GY=330, GW=360, GH=140;
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+GW,GY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(GX,GY-GH-10);ctx.lineTo(GX,GY);ctx.stroke();
    ctx.strokeStyle='#c4b5fd';ctx.lineWidth=1.8;ctx.setLineDash([4,4]);
    ctx.beginPath();ctx.moveTo(GX,GY-GH);ctx.lineTo(GX+GW,GY-GH);ctx.stroke();ctx.setLineDash([]);
    lbl(ctx,'1',GX-16,GY-GH+5,'#6d28d9',12);
    ctx.strokeStyle='#15803d';ctx.lineWidth=2.6;ctx.beginPath();
    for(i=1;i<=12;i++){
      var v=1-Math.pow(5/6,i);
      var x=GX+GW*i/12;
      if(i===1) ctx.moveTo(x,GY-v*GH); else ctx.lineTo(x,GY-v*GH);
    }
    ctx.stroke();
    ctx.strokeStyle='#dc2626';ctx.lineWidth=2;ctx.setLineDash([5,4]);ctx.beginPath();
    for(i=1;i<=12;i++){
      var v2=Math.min(i/6,1.15);
      var x2=GX+GW*i/12;
      if(i===1) ctx.moveTo(x2,GY-v2*GH); else ctx.lineTo(x2,GY-v2*GH);
    }
    ctx.stroke();ctx.setLineDash([]);
    if(grow>=1){
      var xx=GX+GW*S.n/12;
      ctx.beginPath();ctx.arc(xx,GY-c.at*GH,6,0,Math.PI*2);
      ctx.fillStyle='#15803d';ctx.fill();
    }
    lbl(ctx,'주사위를 '+S.n+'번 던져 1의 눈이 적어도 한 번',24,32,'#1d4ed8',17);
    lbl(ctx,'초록 = 실제 확률,  빨강 점선 = n/6',24,56,'#52627a',13);
    box(ctx,20,366,400,54);
    lbl(ctx,(t===null)?'n/6 으로 구하면 될까?':('적어도 한 번 = 1 − (5/6)^'+S.n+' = '+r4(c.at)),34,392,'#1f2937',16);
    lbl(ctx,(t===null)?'':('n/6 = '+r3(c.naive)+(c.over?'  ← 1을 넘는다!':'')),34,414,'#b91c1c',15);
  },
  record:function(S){
    var c=this.calc(S);
    return {n:S.n,none:r4(c.none),at:r4(c.at),naive:r3(c.naive),
            gap:r4(Math.abs(c.at-c.naive)),
            same:(Math.abs(c.at-c.naive)<1e-9),
            over:c.over,one:(S.n===1),
            sumOne:(Math.abs(c.none+c.at-1)<1e-12)};
  },
  headA:['번호','n','한 번도 안 나옴','적어도 한 번','두 확률의 합','n/6','같나?','1을 넘나?'],
  rowA:function(r,i){
    return [i+1,r.n,r.none,'<b>'+r.at+'</b>',
            '<span class="'+(r.sumOne?'ok':'no')+'">'+(r.sumOne?'1':'×')+'</span>',
            r.naive,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            '<span class="'+(r.over?'no':'ok')+'">'+(r.over?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],sum=0,same=0,sameOne=0,over=0,mx=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.sumOne) sum++;
      if(r.same){ same++; if(r.one) sameOne++; }
      if(r.over) over++;
      if(parseFloat(r.gap)>mx) mx=parseFloat(r.gap);
      rows.push([r.n, r.none, '<b>'+r.at+'</b>',
                 '<span class="'+(r.sumOne?'ok':'no')+'">'+(r.sumOne?'○':'×')+'</span>',
                 r.naive, r.gap,
                 '<span class="'+(r.over?'no':'ok')+'">'+(r.over?'1 초과':'-')+'</span>']);
    }
    var stats=[
      {t:'두 확률의 합 = 1',big:sum+' / '+rec.length,
       p:'«한 번도 안 나옴»과 «적어도 한 번»은 여사건이다.'},
      {t:'n/6 이 맞은 횟수',big:same+' / '+rec.length,
       p:same?('그중 n = 1 이었던 것 '+sameOne+'개.'):'n을 곱하는 방법은 맞지 않는다.'},
      {t:'n/6 이 1을 넘은 기록',big:over+'개',
       p:over?'확률이 1을 넘을 수는 없다. 가장 큰 차이 '+mx+'.':'n을 7 이상으로도 해 보자.'}
    ];
    var concl;
    if(over===0){
      concl='<b>더 해 보자</b> — n을 <b>7 이상</b>으로 두어 n/6 이 어떻게 되는지 확인해 보자.';
    } else if(sum===rec.length&&same===sameOne){
      concl='<b>정리</b> — «적어도 한 번»은 <b>1 − (한 번도 안 나올 확률)</b> 로 구했다. '
           +'각 번마다 안 나올 확률 5/6 을 n번 곱한 것이 여사건이다. '
           +'반면 n/6 은 n = 1 일 때만 맞았고, n이 6을 넘으면 <b>확률이 1을 넘어</b> 말이 되지 않았다. '
           +'«적어도»가 나오면 <b>여사건</b>을 먼저 떠올리는 것이 훨씬 빠르고 안전하다.';
    } else {
      concl='<b>확인 필요</b> — 두 확률의 합이 1이 아닌 기록이 있다.';
    }
    return {head:['n','안 나옴','적어도 한 번','합 = 1?','n/6','차이','비고'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("m2_linear_equation_graph_lab.html",
     "일차방정식 그래프 실험실 — 직선이면 다 일차함수일까?",
     "일차방정식 그래프 실험실 — 직선이면 다 일차함수일까?",
     "ax+by+c=0 의 계수를 바꿔 그래프를 그리고, y = 꼴로 쓸 수 있는지 확인한다.",
     LAB_LINEQ),
    ("m2_incenter_lab.html",
     "내심 실험실 — 내심도 밖으로 나갈까?",
     "내심 실험실 — 내심도 밖으로 나갈까?",
     "삼각형 모양을 바꿔 가며 내심에서 세 변까지의 거리와 내심의 위치를 기록한다.",
     LAB_INC),
    ("m2_centroid_lab.html",
     "무게중심 실험실 — 중선을 어떤 비로 나눌까?",
     "무게중심 실험실 — 중선을 어떤 비로 나눌까?",
     "세 중선을 긋고 만나는 점이 중선을 나누는 비를 재어 기록한다.",
     LAB_CENT),
    ("m2_similarity_ratio_lab.html",
     "닮음비 실험실 — 2배로 늘리면 넓이도 2배일까?",
     "닮음비 실험실 — 2배로 늘리면 넓이도 2배일까?",
     "도형을 k배로 확대하며 길이·넓이·부피가 각각 몇 배가 되는지 계산해 기록한다.",
     LAB_SIMR),
    ("m2_at_least_one_lab.html",
     "여사건 실험실 — «적어도 한 번»은 어떻게 구할까?",
     "여사건 실험실 — «적어도 한 번»은 어떻게 구할까?",
     "던지는 횟수를 바꿔 가며 여사건으로 구한 확률과 n/6 을 비교한다.",
     LAB_ATLEAST),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c36_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
