# -*- coding: utf-8 -*-
"""고등 공통수학2 — 도형의 방정식 5종"""
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
# 1. 내분점
# ============================================================
LAB_DIV = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'내분점 판',
  action:'나누는 점 찍기',
  hint0:'두 점의 위치와 나누는 비를 정해 보자.',
  sliders:[
    {id:'a',label:'점 A',min:-9,max:9,value:-6,color:'#2563eb',unit:''},
    {id:'b',label:'점 B',min:-9,max:9,value:6,color:'#dc2626',unit:''},
    {id:'m',label:'비 m',min:1,max:6,value:1,color:'#16a34a',unit:''},
    {id:'n',label:'비 n',min:1,max:6,value:3,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var right=(S.m*S.b+S.n*S.a)/(S.m+S.n);
    var wrong=(S.m*S.a+S.n*S.b)/(S.m+S.n);
    return {right:right,wrong:wrong,
            dr1:Math.abs(right-S.a),dr2:Math.abs(S.b-right),
            dw1:Math.abs(wrong-S.a),dw2:Math.abs(S.b-wrong)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'m : n',v:S.m+' : '+S.n},
            {k:'내분점',v:ran?r3(c.right):'찍어 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '내분점은 '+r3(c.right)+'이고 A까지 : B까지 = '+r2(c.dr1)+' : '+r2(c.dr2)+'다. 순서를 바꾼 값 '+r3(c.wrong)+'와 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var X0=36, X1=404, LO=-10, HI=10;
    function px(v){ return X0+(X1-X0)*(v-LO)/(HI-LO); }
    var Y=180;
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(X0,Y);ctx.lineTo(X1,Y);ctx.stroke();
    for(i=LO;i<=HI;i++){
      var x=px(i), big=(i%5===0);
      ctx.beginPath();ctx.moveTo(x,Y-(big?8:4));ctx.lineTo(x,Y+(big?8:4));
      ctx.strokeStyle=big?'#64748b':'#cbd5e1';ctx.lineWidth=big?1.8:1;ctx.stroke();
      if(big){ ctx.fillStyle='#94a3b8';ctx.font='11px sans-serif';ctx.textAlign='center';ctx.fillText(i,x,Y+24); }
    }
    ctx.textAlign='left';
    ctx.strokeStyle='#cbd5e1';ctx.lineWidth=6;
    ctx.beginPath();ctx.moveTo(px(S.a),Y-20);ctx.lineTo(px(S.b),Y-20);ctx.stroke();
    [[S.a,'A','#2563eb'],[S.b,'B','#dc2626']].forEach(function(q){
      ctx.beginPath();ctx.arc(px(q[0]),Y,8,0,Math.PI*2);
      ctx.fillStyle=q[2];ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      lbl(ctx,q[1]+' '+q[0],px(q[0]),Y-32,q[2],14,'center');
    });
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      var xr=px(S.a)+(px(c.right)-px(S.a))*grow;
      ctx.beginPath();ctx.arc(xr,Y,9,0,Math.PI*2);
      ctx.fillStyle='#16a34a';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      if(grow>=1){
        lbl(ctx,'P '+r2(c.right),xr,Y+48,'#15803d',15,'center');
        lbl(ctx,r2(c.dr1),(px(S.a)+xr)/2,Y-26,'#15803d',13,'center');
        lbl(ctx,r2(c.dr2),(px(S.b)+xr)/2,Y-26,'#15803d',13,'center');
      }
    }
    if(grow>=1&&Math.abs(c.wrong-c.right)>1e-9){
      ctx.beginPath();ctx.arc(px(c.wrong),Y+70,7,0,Math.PI*2);
      ctx.fillStyle='#fecaca';ctx.fill();ctx.strokeStyle='#dc2626';ctx.lineWidth=2;ctx.stroke();
      lbl(ctx,'순서 바꾼 값 '+r2(c.wrong),px(c.wrong),Y+92,'#b91c1c',13,'center');
    }
    lbl(ctx,'A와 B를 '+S.m+' : '+S.n+' 으로 나누는 점',24,34,'#1d4ed8',18);
    box(ctx,20,296,400,88);
    lbl(ctx,(t===null)?'어느 쪽에 더 가까울까?':('(m·B + n·A) / (m+n) = '+r3(c.right)),38,328,'#15803d',18);
    lbl(ctx,(t===null)?'':('(m·A + n·B) / (m+n) = '+r3(c.wrong)),38,358,'#b91c1c',18);
  },
  record:function(S){
    var c=this.calc(S);
    var rr=(c.dr2===0)?999:(c.dr1/c.dr2);
    var wr=(c.dw2===0)?999:(c.dw1/c.dw2);
    return {a:S.a,b:S.b,m:S.m,n:S.n,
            right:r3(c.right),wrong:r3(c.wrong),
            d1:r2(c.dr1),d2:r2(c.dr2),
            ratioOk:(Math.abs(rr-S.m/S.n)<1e-9),
            wrongOk:(Math.abs(wr-S.m/S.n)<1e-9),
            same:(Math.abs(c.right-c.wrong)<1e-9)};
  },
  headA:['번호','A, B','m : n','올바른 내분점','A까지 : B까지','비가 맞나?','순서 바꾼 값','비가 맞나?'],
  rowA:function(r,i){
    return [i+1,r.a+', '+r.b,r.m+':'+r.n,'<b>'+r.right+'</b>',r.d1+' : '+r.d2,
            '<span class="'+(r.ratioOk?'ok':'no')+'">'+(r.ratioOk?'○':'×')+'</span>',
            r.wrong,
            '<span class="'+(r.wrongOk?'ok':'no')+'">'+(r.wrongOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ok=0,wok=0,same=0,eqmn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.ratioOk) ok++;
      if(r.wrongOk) wok++;
      if(r.same){ same++; if(r.m===r.n) eqmn++; }
      rows.push([r.a+', '+r.b, r.m+':'+r.n, '<b>'+r.right+'</b>', r.d1+' : '+r.d2,
                 '<span class="'+(r.ratioOk?'ok':'no')+'">'+(r.ratioOk?'○':'×')+'</span>',
                 r.wrong,
                 '<span class="'+(r.wrongOk?'ok':'no')+'">'+(r.wrongOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'(mB + nA)/(m+n) 이 비를 맞춘 횟수',big:ok+' / '+rec.length,
       p:'찍은 점에서 A까지와 B까지의 거리 비를 실제로 재어 확인한 결과.'},
      {t:'순서를 바꾼 식이 맞은 횟수',big:wok+' / '+rec.length,
       p:'분자에서 A와 B를 바꿔 넣으면 어떻게 되는지 확인했다.'},
      {t:'두 값이 같았던 횟수',big:same+' / '+rec.length,
       p:same?('그중 m = n 이었던 것 '+eqmn+'개. 중점일 때만 같아진다.'):'m과 n을 같게 해 보자.'}
    ];
    var concl;
    if(ok===rec.length&&wok===same){
      concl='<b>정리</b> — A와 B를 m : n으로 나누는 점은 <b>(mB + nA)/(m + n)</b>이었다. '
           +'m 쪽 비율에 <b>B의 좌표</b>가 곱해진다는 점이 헷갈리기 쉽다. '
           +'P가 A에 가까울수록 A쪽 조각(m)이 작아지기 때문이다. '
           +'순서를 바꾼 식은 m = n(중점)일 때만 우연히 같았다. 헷갈리면 <b>거리의 비를 직접 재어</b> 확인하면 된다.';
    } else {
      concl='<b>확인 필요</b> — 비가 맞지 않는 기록이 있다.';
    }
    return {head:['A, B','m:n','내분점','거리 비','맞나?','순서 바꾼 값','맞나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 두 직선의 평행과 수직
# ============================================================
LAB_PERP = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'두 직선 판',
  action:'두 직선 사이 각 재기',
  hint0:'두 직선의 기울기를 정하고, 사이 각과 기울기의 곱을 비교해 보자.',
  sliders:[
    {id:'m1',label:'① 기울기 (÷2)',min:-8,max:8,value:2,color:'#2563eb',
     fmt:function(v){return (v/2).toFixed(1);}},
    {id:'m2',label:'② 기울기 (÷2)',min:-8,max:8,value:-1,color:'#dc2626',
     fmt:function(v){return (v/2).toFixed(1);}},
    {id:'n2',label:'② y절편',min:-6,max:6,value:2,color:'#f87171',unit:''}
  ],
  calc:function(S){
    var a=S.m1/2, b=S.m2/2;
    var t1=Math.atan(a), t2=Math.atan(b);
    var d=Math.abs(t1-t2)*180/Math.PI;
    if(d>90) d=180-d;
    return {a:a,b:b,prod:a*b,ang:d,
            perp:(Math.abs(a*b+1)<1e-9),
            par:(Math.abs(a-b)<1e-9)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'기울기의 곱',v:r2(c.prod)},
            {k:'두 직선 사이 각',v:ran?(r1(c.ang)+'°'):'재 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '사이 각은 '+r1(c.ang)+'°이고 기울기의 곱은 '+r2(c.prod)+'다. '
      +(c.perp?'수직이다.':(c.par?'평행하다.':''))+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,9,8);
    function line(m,n,col){
      ctx.strokeStyle=col;ctx.lineWidth=3;ctx.beginPath();
      var st=false;
      for(i=-90;i<=90;i++){
        var x=i/10, y=m*x+n;
        if(y<-8||y>8){ st=false; continue; }
        if(!st){ ctx.moveTo(CX+x*U,CY-y*U); st=true; } else ctx.lineTo(CX+x*U,CY-y*U);
      }
      ctx.stroke();
    }
    line(c.a,0,'#2563eb');
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0) line(c.b,S.n2,'#dc2626');
    lbl(ctx,'① y = '+c.a+'x     ② y = '+c.b+'x'+sg(S.n2),24,32,'#334155',16);
    box(ctx,20,346,400,74);
    lbl(ctx,'기울기의 곱 : '+r2(c.prod),38,376,'#1f2937',19);
    lbl(ctx,(t===null)?'사이 각은 몇 도일까?':('사이 각 '+r1(c.ang)+'°   '+(c.perp?'→ 수직':(c.par?'→ 평행':''))),
        38,406,c.perp?'#15803d':(c.par?'#b45309':'#52627a'),18);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:c.a,b:c.b,prod:r2(c.prod),ang:r1(c.ang),
            perp:c.perp,par:c.par,
            ang90:(Math.abs(c.ang-90)<0.05),
            ang0:(Math.abs(c.ang)<0.05)};
  },
  headA:['번호','① 기울기','② 기울기','기울기의 곱','사이 각','곱 = −1?','각 = 90°?','평행?'],
  rowA:function(r,i){
    return [i+1,r.a,r.b,'<b>'+r.prod+'</b>',r.ang+'°',
            '<span class="'+(r.perp?'ok':'no')+'">'+(r.perp?'○':'×')+'</span>',
            '<span class="'+(r.ang90?'ok':'no')+'">'+(r.ang90?'○':'×')+'</span>',
            '<span class="'+(r.par?'ok':'no')+'">'+(r.par?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],match=0,perp=0,par=0,parMatch=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var m=(r.perp===r.ang90);
      if(m) match++;
      if(r.perp) perp++;
      if(r.par){ par++; if(r.ang0) parMatch++; }
      rows.push([r.a+' , '+r.b, '<b>'+r.prod+'</b>', r.ang+'°',
                 '<span class="'+(r.perp?'ok':'no')+'">'+(r.perp?'○':'×')+'</span>',
                 '<span class="'+(r.ang90?'ok':'no')+'">'+(r.ang90?'○':'×')+'</span>',
                 '<span class="'+(m?'ok':'no')+'">'+(m?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'“곱 = −1”과 “각 = 90°”가 일치',big:match+' / '+rec.length,
       p:'기울기의 곱만 보고 수직인지 판단할 수 있는지 확인한 결과.'},
      {t:'수직이었던 기록',big:perp+'개',
       p:perp?'그때 곱이 정확히 −1이었다.':'기울기를 2와 −0.5처럼 잡아 보자.'},
      {t:'평행이었던 기록',big:par+'개',
       p:par?('그중 사이 각이 0°였던 것 '+parMatch+'개.'):'두 기울기를 같게 해 보자.'}
    ];
    var concl;
    if(perp===0||par===0){
      concl='<b>더 해 보자</b> — 수직인 경우(기울기 2와 −0.5)와 평행인 경우(기울기가 같음)를 <b>모두</b> 기록해 보자.';
    } else if(match===rec.length){
      concl='<b>정리</b> — 두 직선이 수직일 때만 <b>기울기의 곱이 정확히 −1</b>이었고, 평행일 때는 기울기가 같아 사이 각이 0°였다. '
           +'기울기가 커도 −1이 아니면 수직이 아니다. 곱이 −1이라는 조건은 기울어진 방향이 서로 직각이 되도록 맞물린다는 뜻이다.';
    } else {
      concl='<b>확인 필요</b> — 곱과 사이 각의 판정이 어긋난 기록이 있다.';
    }
    return {head:['두 기울기','곱','사이 각','곱=−1?','각=90°?','일치?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 점과 직선 사이의 거리
# ============================================================
LAB_DIST = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'점과 직선 거리판',
  action:'가장 가까운 점 찾기',
  hint0:'직선과 점의 위치를 정하고, 가장 짧은 거리를 재 보자.',
  sliders:[
    {id:'m',label:'직선의 기울기 (÷2)',min:-6,max:6,value:2,color:'#2563eb',
     fmt:function(v){return (v/2).toFixed(1);}},
    {id:'n',label:'직선의 y절편',min:-6,max:6,value:-1,color:'#60a5fa',unit:''},
    {id:'px',label:'점의 x좌표',min:-8,max:8,value:3,color:'#dc2626',unit:''},
    {id:'py',label:'점의 y좌표',min:-7,max:7,value:5,color:'#f87171',unit:''}
  ],
  calc:function(S){
    var m=S.m/2;
    var formula=Math.abs(m*S.px-S.py+S.n)/Math.sqrt(m*m+1);
    var best=1e9,bx=0,i;
    for(i=-2000;i<=2000;i++){
      var x=i/100, y=m*x+S.n;
      var d=Math.sqrt((x-S.px)*(x-S.px)+(y-S.py)*(y-S.py));
      if(d<best){ best=d; bx=x; }
    }
    var foot=[bx,m*bx+S.n];
    var vx=foot[0]-S.px, vy=foot[1]-S.py;
    var lx=1, ly=m;
    var dot=vx*lx+vy*ly;
    return {m:m,formula:formula,best:best,foot:foot,
            perp:(Math.abs(dot)/(Math.sqrt(vx*vx+vy*vy)*Math.sqrt(1+m*m)+1e-9)<0.02)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'공식으로 구한 거리',v:r3(c.formula)},
            {k:'직접 찾은 최단 거리',v:ran?r3(c.best):'찾아보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '공식값 '+r3(c.formula)+', 직접 찾은 최단거리 '+r3(c.best)+'.  가장 가까운 점은 ('+r2(c.foot[0])+', '+r2(c.foot[1])+')다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,9,7);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    var st=false;
    for(i=-90;i<=90;i++){
      var x=i/10, y=c.m*x+S.n;
      if(y<-7||y>7){ st=false; continue; }
      if(!st){ ctx.moveTo(CX+x*U,CY-y*U); st=true; } else ctx.lineTo(CX+x*U,CY-y*U);
    }
    ctx.stroke();
    ctx.beginPath();ctx.arc(CX+S.px*U,CY-S.py*U,8,0,Math.PI*2);
    ctx.fillStyle='#dc2626';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
    lbl(ctx,'P('+S.px+', '+S.py+')',CX+S.px*U+12,CY-S.py*U-10,'#b91c1c',14);
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      var n=Math.floor(grow*24);
      ctx.strokeStyle='#e2e8f0';ctx.lineWidth=1.2;
      for(i=0;i<n;i++){
        var xx=-6+i*0.5, yy=c.m*xx+S.n;
        if(Math.abs(yy)>7) continue;
        ctx.beginPath();ctx.moveTo(CX+S.px*U,CY-S.py*U);ctx.lineTo(CX+xx*U,CY-yy*U);ctx.stroke();
      }
    }
    if(grow>=1){
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=4;
      ctx.beginPath();ctx.moveTo(CX+S.px*U,CY-S.py*U);
      ctx.lineTo(CX+c.foot[0]*U,CY-c.foot[1]*U);ctx.stroke();
      ctx.beginPath();ctx.arc(CX+c.foot[0]*U,CY-c.foot[1]*U,6,0,Math.PI*2);
      ctx.fillStyle='#f59e0b';ctx.fill();
    }
    lbl(ctx,'y = '+c.m+'x'+sg(S.n),24,32,'#1d4ed8',17);
    box(ctx,20,344,400,76);
    lbl(ctx,'공식 |m·x₁ − y₁ + n| / √(m²+1) = '+r3(c.formula),38,374,'#1f2937',17);
    lbl(ctx,(t===null)?'가장 가까운 점은 어디일까?':('직접 찾은 최단거리 '+r3(c.best)+'   수직인가 : '+(c.perp?'예':'아니오')),
        38,404,'#15803d',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {m:c.m,n:S.n,px:S.px,py:S.py,
            formula:r3(c.formula),best:r3(c.best),
            same:(Math.abs(c.formula-c.best)<0.01),
            perp:c.perp,
            foot:'('+r2(c.foot[0])+', '+r2(c.foot[1])+')',
            onLine:(Math.abs(c.formula)<1e-9)};
  },
  headA:['번호','직선','점','공식값','최단거리','같은가?','가장 가까운 점','수직?'],
  rowA:function(r,i){
    return [i+1,'y='+r.m+'x'+sg(r.n),'('+r.px+', '+r.py+')','<b>'+r.formula+'</b>',r.best,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            r.foot,
            '<span class="'+(r.perp?'ok':'no')+'">'+(r.perp?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,perp=0,on=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.perp) perp++;
      if(r.onLine) on++;
      rows.push(['y='+r.m+'x'+sg(r.n), '('+r.px+', '+r.py+')', '<b>'+r.formula+'</b>', r.best,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 r.foot,
                 '<span class="'+(r.perp?'ok':'no')+'">'+(r.perp?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'공식값 = 직접 찾은 최단거리',big:same+' / '+rec.length,
       p:'직선 위 4001개 점까지의 거리를 모두 재어 가장 작은 값과 비교했다.'},
      {t:'최단 선분이 직선과 수직',big:perp+' / '+rec.length,
       p:'가장 가까운 점까지 그은 선분의 방향을 확인한 결과.'},
      {t:'점이 직선 위에 있던 기록',big:on+'개',p:on?'그때 거리는 0이었다.':'점을 직선 위에 놓아 보자.'}
    ];
    var concl;
    if(same===rec.length&&perp===rec.length){
      concl='<b>정리</b> — 점에서 직선까지의 <b>가장 짧은 거리는 언제나 수선의 길이</b>였고, 공식으로 구한 값과 정확히 같았다. '
           +'거리를 잰다는 것은 “직선 위 모든 점 중 가장 가까운 것”을 찾는 일이고, 그 점은 수선의 발이다. '
           +'공식의 절댓값은 점이 직선의 어느 쪽에 있든 거리가 양수여야 하기 때문에 붙는다.';
    } else {
      concl='<b>확인 필요</b> — 공식값과 실제 최단거리가 다른 기록이 있다.';
    }
    return {head:['직선','점','공식값','최단거리','같은가?','수선의 발','수직?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 원과 직선의 위치 관계
# ============================================================
LAB_CIRCLINE = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'원과 직선 판',
  action:'교점 찾기',
  hint0:'원의 반지름과 직선을 정하고, 중심에서 직선까지의 거리와 비교해 보자.',
  sliders:[
    {id:'r',label:'원의 반지름',min:1,max:6,value:3,color:'#2563eb',unit:''},
    {id:'m',label:'직선의 기울기 (÷2)',min:-6,max:6,value:2,color:'#dc2626',
     fmt:function(v){return (v/2).toFixed(1);}},
    {id:'n',label:'직선의 y절편',min:-9,max:9,value:5,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var m=S.m/2;
    var d=Math.abs(S.n)/Math.sqrt(m*m+1);
    var A=1+m*m, B=2*m*S.n, C=S.n*S.n-S.r*S.r;
    var D=B*B-4*A*C;
    var cnt=(D>1e-9)?2:((D<-1e-9)?0:1);
    var xs=[];
    if(cnt===2){ xs=[(-B-Math.sqrt(D))/(2*A),(-B+Math.sqrt(D))/(2*A)]; }
    else if(cnt===1){ xs=[-B/(2*A)]; }
    return {m:m,d:d,D:D,cnt:cnt,xs:xs};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'중심에서 직선까지',v:r3(c.d)},
            {k:'교점의 개수',v:ran?(c.cnt+'개'):'찾아보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '거리 '+r3(c.d)+', 반지름 '+S.r+'.  교점은 '+c.cnt+'개다. '+((c.cnt===1)?'직선이 원에 접한다.':'')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,9,7);
    ctx.beginPath();ctx.arc(CX,CY,S.r*U,0,Math.PI*2);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      ctx.strokeStyle='#dc2626';ctx.lineWidth=3;ctx.beginPath();
      var st=false;
      for(i=-90;i<=90;i++){
        var x=i/10, y=c.m*x+S.n;
        if(y<-7||y>7){ st=false; continue; }
        if(!st){ ctx.moveTo(CX+x*U,CY-y*U); st=true; } else ctx.lineTo(CX+x*U,CY-y*U);
      }
      ctx.stroke();
    }
    if(grow>=1){
      var fx=-c.m*S.n/(1+c.m*c.m), fy=c.m*fx+S.n;
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=3;
      ctx.beginPath();ctx.moveTo(CX,CY);ctx.lineTo(CX+fx*U,CY-fy*U);ctx.stroke();
      lbl(ctx,r2(c.d),CX+fx*U/2+8,CY-fy*U/2,'#b45309',14);
      for(i=0;i<c.xs.length;i++){
        var xx=c.xs[i], yy=c.m*xx+S.n;
        ctx.beginPath();ctx.arc(CX+xx*U,CY-yy*U,7,0,Math.PI*2);
        ctx.fillStyle='#7c3aed';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      }
    }
    ctx.beginPath();ctx.arc(CX,CY,4,0,Math.PI*2);ctx.fillStyle='#1f2937';ctx.fill();
    lbl(ctx,'x² + y² = '+(S.r*S.r)+'   와   y = '+c.m+'x'+sg(S.n),24,32,'#334155',16);
    box(ctx,20,346,400,74);
    lbl(ctx,'중심에서 직선까지 '+r3(c.d)+'      반지름 '+S.r,38,376,'#1f2937',18);
    lbl(ctx,(t===null)?'몇 점에서 만날까?':('교점 '+c.cnt+'개   '+((c.d<S.r-1e-9)?'(거리 < 반지름)':((c.d>S.r+1e-9)?'(거리 > 반지름)':'(거리 = 반지름, 접함)'))),
        38,406,(c.cnt===1)?'#b45309':((c.cnt===0)?'#b91c1c':'#15803d'),17);
  },
  record:function(S){
    var c=this.calc(S);
    return {r:S.r,m:c.m,n:S.n,d:r3(c.d),cnt:c.cnt,
            cmp:(c.d<S.r-1e-9)?'<':((c.d>S.r+1e-9)?'>':'='),
            tangent:(c.cnt===1)};
  },
  headA:['번호','원','직선','거리 d','반지름 r','d와 r','교점 개수','접함?'],
  rowA:function(r,i){
    return [i+1,'x²+y²='+(r.r*r.r),'y='+r.m+'x'+sg(r.n),r.d,r.r,'d '+r.cmp+' r','<b>'+r.cnt+'개</b>',
            '<span class="'+(r.tangent?'ok':'no')+'">'+(r.tangent?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],match=0,two=0,one=0,zero=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var expect=(r.cmp==='<')?2:((r.cmp==='>')?0:1);
      var m=(expect===r.cnt);
      if(m) match++;
      if(r.cnt===2) two++; else if(r.cnt===1) one++; else zero++;
      rows.push(['r='+r.r, 'y='+r.m+'x'+sg(r.n), r.d, 'd '+r.cmp+' r', '<b>'+r.cnt+'개</b>',
                 '<span class="'+(m?'ok':'no')+'">'+(m?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'거리와 반지름 비교로 한 예측이 맞은 횟수',big:match+' / '+rec.length,
       p:'연립방정식을 풀지 않고 거리만으로 판단할 수 있는지 확인한 결과.'},
      {t:'두 점 / 접함 / 만나지 않음',big:two+' / '+one+' / '+zero,
       p:(two&&one&&zero)?'세 경우를 모두 기록했다.':'세 경우를 모두 만들어 보자.'},
      {t:'접한 기록',big:one+'개',
       p:one?'거리가 반지름과 정확히 같을 때만 접했다.':'y절편을 조금씩 바꾸면 접하는 순간이 있다.'}
    ];
    var concl;
    if(!(two&&one&&zero)){
      concl='<b>더 해 보자</b> — 두 점에서 만나는 경우, 접하는 경우, 만나지 않는 경우를 <b>모두</b> 만들어 보자.';
    } else if(match===rec.length){
      concl='<b>정리</b> — 원과 직선의 관계는 <b>중심에서 직선까지의 거리 d와 반지름 r만 비교하면</b> 알 수 있었다. '
           +'d &lt; r 이면 두 점, d = r 이면 접하고, d &gt; r 이면 만나지 않았다. '
           +'연립해서 판별식을 구해도 같은 결과가 나오지만, 거리 공식 쪽이 훨씬 빠르다.';
    } else {
      concl='<b>확인 필요</b> — 거리 판정과 교점 수가 어긋난 기록이 있다.';
    }
    return {head:['원','직선','거리','d와 r','교점 수','예측 일치?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 원의 방정식이 되는 조건
# ============================================================
LAB_CIRCEQ = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'원의 방정식 판',
  action:'완전제곱으로 정리하기',
  hint0:'x² + y² + Ax + By + C = 0 의 계수를 정해 보자.',
  sliders:[
    {id:'A',label:'A',min:-8,max:8,value:-4,color:'#2563eb',unit:''},
    {id:'B',label:'B',min:-8,max:8,value:2,color:'#16a34a',unit:''},
    {id:'C',label:'C',min:-12,max:12,value:-4,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var cx=-S.A/2, cy=-S.B/2;
    var r2v=cx*cx+cy*cy-S.C;
    var kind=(r2v>1e-9)?'원':((r2v<-1e-9)?'그래프 없음':'한 점');
    return {cx:cx,cy:cy,r2:r2v,r:(r2v>0)?Math.sqrt(r2v):0,kind:kind};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'중심',v:'( '+r2(c.cx)+' , '+r2(c.cy)+' )'},
            {k:'반지름²',v:ran?r2(c.r2):'정리해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '중심 ('+r2(c.cx)+', '+r2(c.cy)+'), 반지름² = '+r2(c.r2)+'.  이 방정식은 '+c.kind+'을 나타낸다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    grid(ctx,9,7);
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      if(c.kind==='원'){
        ctx.beginPath();ctx.arc(CX+c.cx*U,CY-c.cy*U,c.r*U*grow,0,Math.PI*2);
        ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.stroke();
      } else if(c.kind==='한 점'){
        ctx.beginPath();ctx.arc(CX+c.cx*U,CY-c.cy*U,7,0,Math.PI*2);
        ctx.fillStyle='#b45309';ctx.fill();
      }
      ctx.beginPath();ctx.arc(CX+c.cx*U,CY-c.cy*U,4,0,Math.PI*2);
      ctx.fillStyle='#dc2626';ctx.fill();
    }
    if(grow>=1&&c.kind==='그래프 없음'){
      lbl(ctx,'그려지는 점이 하나도 없다',CX,CY,'#b91c1c',20,'center');
    }
    lbl(ctx,'x² + y²'+sgc(S.A,'x')+sgc(S.B,'y')+sg(S.C)+' = 0',24,32,'#1d4ed8',17);
    box(ctx,20,344,400,76);
    lbl(ctx,(t===null)?'이 방정식은 원을 나타낼까?':('(x'+sg(-c.cx)+')² + (y'+sg(-c.cy)+')² = '+r2(c.r2)),38,374,'#334155',17);
    lbl(ctx,(t===null)?'':('반지름² = '+r2(c.r2)+'  →  '+c.kind),38,404,
        (c.kind==='원')?'#15803d':((c.kind==='한 점')?'#b45309':'#b91c1c'),18);
  },
  record:function(S){
    var c=this.calc(S);
    return {A:S.A,B:S.B,C:S.C,cx:r2(c.cx),cy:r2(c.cy),r2:r2(c.r2),
            kind:c.kind,isCircle:(c.kind==='원'),
            r:(c.r>0)?r2(c.r):0};
  },
  headA:['번호','방정식','중심','반지름²','반지름','나타내는 것','원인가?'],
  rowA:function(r,i){
    return [i+1,'x²+y²'+sgc(r.A,'x')+sgc(r.B,'y')+sg(r.C)+'=0','('+r.cx+', '+r.cy+')',
            '<b>'+r.r2+'</b>',(r.r?r.r:'-'),r.kind,
            '<span class="'+(r.isCircle?'ok':'no')+'">'+(r.isCircle?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ci=0,pt=0,no=0,match=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var expect=(r.r2>0)?'원':((r.r2<0)?'그래프 없음':'한 점');
      if(expect===r.kind) match++;
      if(r.kind==='원') ci++; else if(r.kind==='한 점') pt++; else no++;
      rows.push(['x²+y²'+sgc(r.A,'x')+sgc(r.B,'y')+sg(r.C), '('+r.cx+', '+r.cy+')', '<b>'+r.r2+'</b>',
                 r.kind,
                 '<span class="'+(r.isCircle?'ok':'no')+'">'+(r.isCircle?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'반지름²의 부호로 한 판정이 맞은 횟수',big:match+' / '+rec.length,
       p:'완전제곱으로 정리한 뒤 우변의 부호만 보면 된다.'},
      {t:'원 / 한 점 / 그래프 없음',big:ci+' / '+pt+' / '+no,
       p:(ci&&pt&&no)?'세 경우를 모두 기록했다.':'세 경우를 모두 만들어 보자.'},
      {t:'중심은 언제나',big:'(−A/2, −B/2)',p:'우변이 음수여도 중심 좌표 계산은 그대로 나온다.'}
    ];
    var concl;
    if(!(ci&&pt&&no)){
      concl='<b>더 해 보자</b> — <b>원이 되는 경우, 한 점이 되는 경우, 아무것도 없는 경우</b>를 모두 만들어 보자. '
           +'C를 크게 키우면 우변이 음수가 된다.';
    } else {
      concl='<b>정리</b> — x² + y² + Ax + By + C = 0 이 <b>항상 원인 것은 아니었다.</b> '
           +'완전제곱으로 정리했을 때 우변이 <b>양수일 때만 원</b>이고, 0이면 점 하나, 음수면 그래프가 아예 없었다. '
           +'중심 (−A/2, −B/2)는 어느 경우에도 계산되어 나오므로, 중심을 구했다고 원이라고 단정하면 안 된다.';
    }
    return {head:['방정식','중심','반지름²','나타내는 것','원인가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("h2_internal_division_lab_CommonMath2_Shapes_Ep02.html",
     "내분점 실험실 — m : n 으로 나누면 어디일까?",
     "내분점 실험실 — m : n 으로 나누면 어디일까?",
     "두 점을 정해진 비로 나누는 점을 찍고, 실제 거리 비를 재어 공식을 확인한다.",
     LAB_DIV),
    ("h2_perpendicular_lines_lab_CommonMath2_Shapes_Ep04.html",
     "직선 실험실 — 기울기의 곱이 −1이면 수직일까?",
     "직선 실험실 — 기울기의 곱이 −1이면 수직일까?",
     "두 직선의 기울기를 바꿔 가며 사이 각을 재고, 기울기의 곱과 대조한다.",
     LAB_PERP),
    ("h2_point_line_distance_lab_CommonMath2_Shapes_Ep06.html",
     "거리 실험실 — 가장 짧은 거리는 어디로 재는 걸까?",
     "거리 실험실 — 가장 짧은 거리는 어디로 재는 걸까?",
     "직선 위 수천 개 점까지의 거리를 모두 재어 최솟값을 찾고, 거리 공식과 비교한다.",
     LAB_DIST),
    ("h2_circle_line_lab_CommonMath2_Shapes_Ep08.html",
     "원과 직선 실험실 — 연립하지 않고 알 수 있을까?",
     "원과 직선 실험실 — 연립하지 않고 알 수 있을까?",
     "중심에서 직선까지의 거리와 반지름을 비교해 교점의 개수를 예측하고 확인한다.",
     LAB_CIRCLINE),
    ("h2_circle_equation_lab_CommonMath2_Shapes_Ep07.html",
     "원의 방정식 실험실 — 언제나 원이 될까?",
     "원의 방정식 실험실 — 언제나 원이 될까?",
     "x²+y²+Ax+By+C=0을 완전제곱으로 정리해 원이 되는 조건을 찾는다.",
     LAB_CIRCEQ),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c23_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
