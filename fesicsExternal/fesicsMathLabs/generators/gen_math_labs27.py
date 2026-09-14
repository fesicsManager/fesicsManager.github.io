# -*- coding: utf-8 -*-
"""고등 미적분Ⅰ — 극한·연속·미분 5종"""
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
var CX=220, CY=220, U=26;
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
# 1. 함수의 극한
# ============================================================
LAB_LIM = BASE + r"""
var KINDS=['(x²−1)/(x−1)','|x| / x','x < 0 이면 x+2, x ≥ 0 이면 x−1'];
var AS=[1,0,0];
function fk(kind,x){
  if(kind===0){ if(Math.abs(x-1)<1e-12) return null; return (x*x-1)/(x-1); }
  if(kind===1){ if(Math.abs(x)<1e-12) return null; return Math.abs(x)/x; }
  return (x<0)?(x+2):(x-1);
}
var LAB = {
  cw:440, ch:430, cvTitle:'극한 관찰판',
  action:'양쪽에서 다가가기',
  hint0:'함수를 고르고, 문제의 x에 얼마나 가까이 갈지 정해 보자.',
  sliders:[
    {id:'kind',label:'함수',min:0,max:2,value:0,color:'#2563eb',fmt:function(v){return KINDS[v];}},
    {id:'h',label:'다가가는 거리 (÷1000)',min:1,max:500,value:100,color:'#f59e0b',
     fmt:function(v){return (v/1000).toFixed(3);}}
  ],
  calc:function(S){
    var a=AS[S.kind], h=S.h/1000;
    var L=fk(S.kind,a-h), R=fk(S.kind,a+h);
    var fa=fk(S.kind,a);
    var Lsmall=fk(S.kind,a-0.000001), Rsmall=fk(S.kind,a+0.000001);
    return {a:a,h:h,L:L,R:R,fa:fa,
            exist:(Math.abs(Lsmall-Rsmall)<1e-4),
            lim:(Math.abs(Lsmall-Rsmall)<1e-4)?((Lsmall+Rsmall)/2):null,
            defined:(fa!==null)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'왼쪽에서',v:ran?r4(c.L):'다가가 보자'},
            {k:'오른쪽에서',v:ran?r4(c.R):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'x = '+c.a+'의 왼쪽에서 '+r4(c.L)+', 오른쪽에서 '+r4(c.R)+'.  함숫값은 '+(c.defined?r3(c.fa):'정의되지 않음')+'이다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,7,6);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;
    var st=false;
    ctx.beginPath();
    for(i=-70;i<=70;i++){
      var x=i/10;
      var y=fk(S.kind,x);
      if(y===null||y<-6||y>6){ st=false; continue; }
      if(S.kind===2&&Math.abs(x)<1e-9){ st=false; continue; }
      if(!st){ ctx.moveTo(CX+x*U,CY-y*U); st=true; } else ctx.lineTo(CX+x*U,CY-y*U);
    }
    ctx.stroke();
    if(!c.defined&&c.lim!==null){
      ctx.beginPath();ctx.arc(CX+c.a*U,CY-c.lim*U,6,0,Math.PI*2);
      ctx.fillStyle='#fff';ctx.fill();ctx.strokeStyle='#2563eb';ctx.lineWidth=2.5;ctx.stroke();
    }
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      var hh=c.h+(1-grow)*(1.5-c.h);
      var xl=c.a-hh, xr=c.a+hh;
      var yl=fk(S.kind,xl), yr=fk(S.kind,xr);
      if(yl!==null&&Math.abs(yl)<=6){
        ctx.beginPath();ctx.arc(CX+xl*U,CY-yl*U,7,0,Math.PI*2);
        ctx.fillStyle='#16a34a';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      }
      if(yr!==null&&Math.abs(yr)<=6){
        ctx.beginPath();ctx.arc(CX+xr*U,CY-yr*U,7,0,Math.PI*2);
        ctx.fillStyle='#dc2626';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      }
    }
    ctx.strokeStyle='#c4b5fd';ctx.lineWidth=1.8;ctx.setLineDash([4,4]);
    ctx.beginPath();ctx.moveTo(CX+c.a*U,CY-6*U);ctx.lineTo(CX+c.a*U,CY+6*U);ctx.stroke();ctx.setLineDash([]);
    lbl(ctx,'f(x) = '+KINDS[S.kind]+'      x → '+c.a,24,30,'#1d4ed8',15);
    box(ctx,20,338,400,80);
    lbl(ctx,(t===null)?'양쪽에서 다가가면 같은 값에 갈까?':('왼쪽 '+r4(c.L)+'      오른쪽 '+r4(c.R)),38,368,'#1f2937',18);
    lbl(ctx,(t===null)?'':('함숫값 f('+c.a+') = '+(c.defined?r3(c.fa):'정의되지 않음')+'      극한 '+((c.lim===null)?'없음':r3(c.lim))),
        38,400,c.exist?'#15803d':'#b91c1c',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {kind:S.kind,name:KINDS[S.kind],a:c.a,h:r3(c.h),
            L:r4(c.L),R:r4(c.R),
            exist:c.exist,lim:(c.lim===null)?'없음':r3(c.lim),
            defined:c.defined,fa:c.defined?r3(c.fa):'-',
            match:(c.defined&&c.lim!==null&&Math.abs(c.fa-c.lim)<1e-6)};
  },
  headA:['번호','함수','x →','거리','왼쪽 값','오른쪽 값','극한 존재?','극한값','함숫값','같나?'],
  rowA:function(r,i){
    return [i+1,r.name,r.a,r.h,r.L,r.R,
            '<span class="'+(r.exist?'ok':'no')+'">'+(r.exist?'○':'×')+'</span>',
            '<b>'+r.lim+'</b>',r.fa,
            '<span class="'+(r.match?'ok':'no')+'">'+(r.match?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ex=0,def=0,match=0,g={},kn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.exist) ex++;
      if(r.defined) def++;
      if(r.match) match++;
      if(!g[r.kind]){ g[r.kind]=r; kn++; }
      rows.push([r.name, r.h, r.L+' / '+r.R,
                 '<span class="'+(r.exist?'ok':'no')+'">'+(r.exist?'○':'×')+'</span>',
                 '<b>'+r.lim+'</b>', r.fa,
                 '<span class="'+(r.match?'ok':'no')+'">'+(r.match?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'극한이 존재한 기록',big:ex+' / '+rec.length,p:'왼쪽과 오른쪽에서 다가간 값이 같았는지 확인한 결과.'},
      {t:'함숫값이 정의된 기록',big:def+' / '+rec.length,p:'그 점에서 함수가 값을 가지는지 확인했다.'},
      {t:'극한값 = 함숫값',big:match+' / '+rec.length,p:'시험한 함수 '+kn+'가지.'}
    ];
    var concl;
    if(kn<3){
      concl='<b>더 해 보자</b> — 세 가지 함수를 <b>모두</b> 기록해야 극한의 여러 모습을 볼 수 있다.';
    } else {
      concl='<b>정리</b> — 극한은 그 점에서의 <b>함숫값과 아무 상관이 없었다.</b> '
           +'(x²−1)/(x−1)은 x=1에서 값이 아예 없는데도 극한은 2로 존재했고, '
           +'좌우에서 다가간 값이 다르면(계단함수, |x|/x) 극한 자체가 없었다. '
           +'극한은 “그 점에 도착했을 때의 값”이 아니라 <b>가까이 갈 때 다가가는 값</b>이다. '
           +'그래서 좌극한과 우극한이 모두 있고 서로 같아야 극한이 존재한다.';
    }
    return {head:['함수','거리','좌 / 우','극한 존재?','극한값','함숫값','같나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 연속의 조건
# ============================================================
LAB_CONT = BASE + r"""
function f2(S,x){
  if(x<1) return x+S.k;
  if(Math.abs(x-1)<1e-12) return S.m;
  return 2*x;
}
var LAB = {
  cw:440, ch:430, cvTitle:'연속 판정판',
  action:'세 값 비교하기',
  hint0:'x = 1 에서 이어지도록 상수 k와 함숫값 m을 맞춰 보자.',
  sliders:[
    {id:'k',label:'왼쪽 식 x + k 의 k',min:-3,max:3,value:0,color:'#2563eb',unit:''},
    {id:'m',label:'f(1)의 값',min:-3,max:5,value:1,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var left=1+S.k, right=2;
    return {left:left,right:right,fa:S.m,
            limExist:(Math.abs(left-right)<1e-12),
            cont:(Math.abs(left-right)<1e-12&&Math.abs(S.m-right)<1e-12)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'좌극한 / 우극한',v:c.left+' / '+c.right},
            {k:'f(1)',v:ran?c.fa:'비교해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '좌극한 '+c.left+', 우극한 '+c.right+', f(1) = '+c.fa+'.  '+(c.cont?'세 값이 모두 같아 연속이다.':'세 값이 모두 같지는 않아 불연속이다.')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,5,5);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;
    ctx.beginPath();
    var st=false;
    for(i=-50;i<10;i++){
      var x=i/10, y=x+S.k;
      if(y<-5||y>5){ st=false; continue; }
      if(!st){ ctx.moveTo(CX+x*U,CY-y*U); st=true; } else ctx.lineTo(CX+x*U,CY-y*U);
    }
    ctx.stroke();
    ctx.strokeStyle='#16a34a';ctx.lineWidth=3;
    ctx.beginPath();st=false;
    for(i=10;i<=50;i++){
      var x2=i/10, y2=2*x2;
      if(y2<-5||y2>5){ st=false; continue; }
      if(!st){ ctx.moveTo(CX+x2*U,CY-y2*U); st=true; } else ctx.lineTo(CX+x2*U,CY-y2*U);
    }
    ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      if(Math.abs(c.left)<=5){
        ctx.beginPath();ctx.arc(CX+U,CY-c.left*U,6,0,Math.PI*2);
        ctx.fillStyle='#fff';ctx.fill();ctx.strokeStyle='#2563eb';ctx.lineWidth=2.5;ctx.stroke();
      }
      if(Math.abs(c.right)<=5){
        ctx.beginPath();ctx.arc(CX+U,CY-c.right*U,6,0,Math.PI*2);
        ctx.fillStyle='#fff';ctx.fill();ctx.strokeStyle='#16a34a';ctx.lineWidth=2.5;ctx.stroke();
      }
      if(Math.abs(c.fa)<=5){
        ctx.beginPath();ctx.arc(CX+U,CY-c.fa*U,7,0,Math.PI*2);
        ctx.fillStyle='#dc2626';ctx.fill();
      }
    }
    lbl(ctx,'x<1 : x'+sg(S.k)+'      x>1 : 2x      f(1) = '+S.m,24,30,'#334155',15);
    box(ctx,20,338,400,80);
    lbl(ctx,'좌극한 '+c.left+'      우극한 '+c.right+'      f(1) '+c.fa,38,370,'#1f2937',18);
    lbl(ctx,(t===null)?'세 값이 모두 같아야 할까?':(c.cont?'x = 1 에서 연속':(c.limExist?'극한은 있지만 함숫값이 달라 불연속':'좌우 극한이 달라 불연속')),
        38,402,c.cont?'#15803d':'#b91c1c',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {k:S.k,m:S.m,left:c.left,right:c.right,fa:c.fa,
            limExist:c.limExist,
            valEq:(Math.abs(S.m-c.right)<1e-12),
            cont:c.cont};
  },
  headA:['번호','k, f(1)','좌극한','우극한','극한 존재?','f(1)','극한 = f(1)?','연속?'],
  rowA:function(r,i){
    return [i+1,r.k+', '+r.m,r.left,r.right,
            '<span class="'+(r.limExist?'ok':'no')+'">'+(r.limExist?'○':'×')+'</span>',
            r.fa,
            '<span class="'+(r.limExist&&r.valEq?'ok':'no')+'">'+(r.limExist&&r.valEq?'○':'×')+'</span>',
            '<span class="'+(r.cont?'ok':'no')+'">'+(r.cont?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],cont=0,limOnly=0,noLim=0,match=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.cont) cont++;
      else if(r.limExist) limOnly++;
      else noLim++;
      var expect=(r.limExist&&r.valEq);
      if(expect===r.cont) match++;
      rows.push([r.k+', '+r.m, r.left+' / '+r.right,
                 '<span class="'+(r.limExist?'ok':'no')+'">'+(r.limExist?'○':'×')+'</span>',
                 r.fa,
                 '<span class="'+(r.valEq?'ok':'no')+'">'+(r.valEq?'○':'×')+'</span>',
                 '<span class="'+(r.cont?'ok':'no')+'">'+(r.cont?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'연속이었던 기록',big:cont+' / '+rec.length,p:'세 값이 모두 같았던 경우.'},
      {t:'극한은 있는데 불연속',big:limOnly+'개',
       p:limOnly?'좌우 극한은 같은데 함숫값만 다른 경우다.':'k를 1로 두고 f(1)만 다르게 해 보자.'},
      {t:'극한 자체가 없었던 기록',big:noLim+'개',
       p:noLim?'좌우 극한이 달랐다.':'k를 1이 아닌 값으로 두어 보자.'}
    ];
    var concl;
    if(cont===0||limOnly===0||noLim===0){
      concl='<b>더 해 보자</b> — <b>연속인 경우, 극한만 있는 경우, 극한도 없는 경우</b>를 모두 만들어 보자. '
           +'k = 1, f(1) = 2 로 두면 연속이 된다.';
    } else if(match===rec.length){
      concl='<b>정리</b> — 연속이 되려면 <b>세 가지가 모두</b> 필요했다. '
           +'① f(1)이 정의되고 ② 좌우 극한이 같아 극한이 존재하고 ③ 그 극한값이 f(1)과 같아야 한다. '
           +'셋 중 하나만 어긋나도 그래프가 끊겼다. 특히 극한이 있어도 함숫값이 따로 놀면 점 하나가 떨어져 나온다.';
    } else {
      concl='<b>확인 필요</b> — 판정이 어긋난 기록이 있다.';
    }
    return {head:['k, f(1)','좌 / 우','극한 존재?','f(1)','극한=f(1)?','연속?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 평균변화율과 미분계수
# ============================================================
LAB_DER = BASE + r"""
function fq(x){ return x*x; }
var LAB = {
  cw:440, ch:430, cvTitle:'할선과 접선 판',
  action:'두 점을 가까이 붙이기',
  hint0:'기준점 a와 떨어진 거리 h를 정하고, 할선의 기울기를 재 보자.',
  sliders:[
    {id:'a',label:'기준점 a',min:-3,max:3,value:1,color:'#2563eb',unit:''},
    {id:'h',label:'거리 h (÷100)',min:1,max:200,value:100,color:'#f59e0b',
     fmt:function(v){return (v/100).toFixed(2);}}
  ],
  calc:function(S){
    var h=S.h/100;
    var slope=(fq(S.a+h)-fq(S.a))/h;
    return {h:h,slope:slope,exact:2*S.a,gap:Math.abs(slope-2*S.a)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'할선의 기울기',v:ran?r4(c.slope):'재 보자'},
            {k:'2a',v:c.exact}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'h = '+r2(c.h)+'일 때 할선의 기울기는 '+r4(c.slope)+'이고 2a = '+c.exact+'다. 차이 '+r4(c.gap)+'.  h를 더 줄여 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,6,5);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    var st=false;
    for(i=-60;i<=60;i++){
      var x=i/10, y=fq(x);
      if(y<-5||y>5){ st=false; continue; }
      if(!st){ ctx.moveTo(CX+x*U,CY-y*U); st=true; } else ctx.lineTo(CX+x*U,CY-y*U);
    }
    ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    var hh=(t===null)?c.h:(2*(1-grow)+c.h*grow);
    var x1=S.a, y1=fq(x1), x2=S.a+hh, y2=fq(x2);
    var sl=(y2-y1)/hh;
    ctx.strokeStyle='#dc2626';ctx.lineWidth=2.6;
    ctx.beginPath();
    var xa=-6, xb=6;
    ctx.moveTo(CX+xa*U,CY-(y1+sl*(xa-x1))*U);
    ctx.lineTo(CX+xb*U,CY-(y1+sl*(xb-x1))*U);
    ctx.stroke();
    [[x1,y1,'#16a34a'],[x2,y2,'#dc2626']].forEach(function(p){
      if(Math.abs(p[1])>5) return;
      ctx.beginPath();ctx.arc(CX+p[0]*U,CY-p[1]*U,7,0,Math.PI*2);
      ctx.fillStyle=p[2];ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
    });
    if(grow>=1){
      ctx.strokeStyle='#7c3aed';ctx.lineWidth=2;ctx.setLineDash([5,4]);
      ctx.beginPath();
      ctx.moveTo(CX+xa*U,CY-(y1+c.exact*(xa-x1))*U);
      ctx.lineTo(CX+xb*U,CY-(y1+c.exact*(xb-x1))*U);
      ctx.stroke();ctx.setLineDash([]);
      lbl(ctx,'보라 점선 = 기울기 '+c.exact,24,54,'#6d28d9',14);
    }
    lbl(ctx,'f(x) = x²,  a = '+S.a+',  h = '+r2(hh),24,30,'#1d4ed8',16);
    box(ctx,20,338,400,80);
    lbl(ctx,(t===null)?'h를 줄이면 기울기는 어디로 갈까?':('할선의 기울기 = '+r4(c.slope)),38,368,'#1f2937',18);
    lbl(ctx,'2a = '+c.exact+'      차이 '+r4(c.gap),38,400,'#15803d',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,h:r2(c.h),slope:r4(c.slope),exact:c.exact,gap:r4(c.gap),
            formula:r4(2*S.a+c.h),
            fOk:(Math.abs(c.slope-(2*S.a+c.h))<1e-9),
            close:(c.gap<0.05)};
  },
  headA:['번호','a','h','할선의 기울기','2a + h','같나?','2a','차이','0.05 이내?'],
  rowA:function(r,i){
    return [i+1,r.a,r.h,'<b>'+r.slope+'</b>',r.formula,
            '<span class="'+(r.fOk?'ok':'no')+'">'+(r.fOk?'○':'×')+'</span>',
            r.exact,r.gap,
            '<span class="'+(r.close?'ok':'no')+'">'+(r.close?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],fo=0,close=0,g={},mono=true,arr=[];
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.fOk) fo++;
      if(r.close) close++;
      if(!g[r.a]) g[r.a]=[];
      g[r.a].push([parseFloat(r.h),parseFloat(r.gap)]);
      rows.push([r.a, r.h, '<b>'+r.slope+'</b>', r.formula,
                 '<span class="'+(r.fOk?'ok':'no')+'">'+(r.fOk?'○':'×')+'</span>',
                 r.exact, r.gap,
                 '<span class="'+(r.close?'ok':'no')+'">'+(r.close?'○':'×')+'</span>']);
    }
    var tested=0,ok=0,k;
    for(k in g){
      var a2=g[k];
      if(a2.length<2) continue;
      a2.sort(function(x,y){return x[0]-y[0];});
      tested++;
      var good=true,j;
      for(j=1;j<a2.length;j++){ if(a2[j][1]<a2[j-1][1]-1e-9) good=false; }
      if(good) ok++;
    }
    var stats=[
      {t:'할선의 기울기 = 2a + h',big:fo+' / '+rec.length,
       p:'(f(a+h) − f(a))/h 를 정리하면 2a + h 가 되는지 확인한 결과.'},
      {t:'2a 와의 차이가 0.05 이내',big:close+' / '+rec.length,p:'h가 작을수록 가까워졌다.'},
      {t:'같은 a에서 h가 작을수록 차이도 작아짐',big:tested?(ok+' / '+tested):'비교 없음',
       p:tested?'a를 고정하고 h만 바꾼 묶음.':'같은 a에서 h만 여러 값으로 기록해 보자.'}
    ];
    var concl;
    if(tested===0){
      concl='<b>더 해 보자</b> — a를 고정하고 h를 2, 1, 0.5, 0.1 처럼 줄여 가며 기록해 보자.';
    } else if(fo===rec.length&&ok===tested){
      concl='<b>정리</b> — 두 점을 잇는 할선의 기울기는 언제나 <b>2a + h</b> 였고, h를 줄일수록 <b>2a</b>에 가까워졌다. '
           +'h가 0이면 두 점이 겹쳐 기울기를 잴 수 없지만, <b>다가가는 값</b>은 분명히 2a다. '
           +'이 극한값이 미분계수 f′(a)이고, 그 기울기를 가진 직선이 접선이다.';
    } else {
      concl='<b>확인 필요</b> — 계산이 어긋난 기록이 있다.';
    }
    return {head:['a','h','할선 기울기','2a+h','같나?','2a','차이','가까운가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 곱의 미분법
# ============================================================
LAB_PROD = BASE + r"""
function pw(x,n){ var v=1,i; for(i=0;i<n;i++) v*=x; return v; }
var LAB = {
  cw:440, ch:400, cvTitle:'곱의 미분 판',
  action:'수치로 미분해 보기',
  hint0:'f = x^m, g = x^n 으로 두고, 곱의 도함수를 구해 보자.',
  sliders:[
    {id:'m',label:'m',min:1,max:4,value:2,color:'#2563eb',unit:''},
    {id:'n',label:'n',min:1,max:4,value:3,color:'#16a34a',unit:''},
    {id:'x0',label:'확인할 x (÷10)',min:5,max:30,value:15,color:'#dc2626',
     fmt:function(v){return (v/10).toFixed(1);}}
  ],
  calc:function(S){
    var x=S.x0/10, h=1e-6;
    var F=function(v){ return pw(v,S.m)*pw(v,S.n); };
    var num=(F(x+h)-F(x-h))/(2*h);
    var fp=S.m*pw(x,S.m-1), gp=S.n*pw(x,S.n-1);
    var f=pw(x,S.m), g=pw(x,S.n);
    return {x:x,num:num,wrong:fp*gp,right:fp*g+f*gp,
            power:(S.m+S.n)*pw(x,S.m+S.n-1)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'수치 미분값',v:ran?r3(c.num):'미분해 보자'},
            {k:'f′g + fg′',v:ran?r3(c.right):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '수치로 구한 (fg)′ = '+r3(c.num)+'.  f′g + fg′ = '+r3(c.right)+', f′g′ = '+r3(c.wrong)+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var p1=(t===null)?0:Math.min(1,t/0.4);
    var p2=(t===null)?0:Math.max(0,Math.min(1,(t-0.4)/0.3));
    var p3=(t===null)?0:Math.max(0,(t-0.7)/0.3);
    lbl(ctx,'f(x) = x^'+S.m+',   g(x) = x^'+S.n,24,40,'#1d4ed8',19);
    lbl(ctx,'f(x)g(x) = x^'+(S.m+S.n)+'      x = '+c.x,24,70,'#52627a',17);
    if(p1>0){
      ctx.globalAlpha=p1;
      lbl(ctx,'수치 미분 (f(x+h) − f(x−h)) / 2h',40,116,'#334155',16);
      lbl(ctx,'= '+r3(c.num),40,152,'#1f2937',24);
      ctx.globalAlpha=1;
    }
    if(p2>0){
      ctx.globalAlpha=p2;
      lbl(ctx,'f′g + fg′ = '+r3(c.right),40,196,'#15803d',22);
      ctx.globalAlpha=1;
    }
    if(p3>0){
      ctx.globalAlpha=p3;
      lbl(ctx,'f′ × g′ = '+r3(c.wrong),40,236,'#b91c1c',22);
      ctx.globalAlpha=1;
    }
    box(ctx,20,258,400,126);
    lbl(ctx,(t===null)?'(fg)′ = f′g′ 일까?':('수치 미분 : '+r3(c.num)),38,290,'#1f2937',18);
    lbl(ctx,(t===null)?'':('f′g + fg′ = '+r3(c.right)),38,322,'#15803d',18);
    lbl(ctx,(t===null)?'':('f′ × g′ = '+r3(c.wrong)),38,352,'#b91c1c',18);
    lbl(ctx,(t===null)?'':('(m+n)x^(m+n−1) = '+r3(c.power)),38,378,'#52627a',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {m:S.m,n:S.n,x:c.x,num:r3(c.num),right:r3(c.right),wrong:r3(c.wrong),
            power:r3(c.power),
            rOk:(Math.abs(c.num-c.right)<0.01*Math.max(1,Math.abs(c.num))),
            wOk:(Math.abs(c.num-c.wrong)<0.01*Math.max(1,Math.abs(c.num))),
            pOk:(Math.abs(c.num-c.power)<0.01*Math.max(1,Math.abs(c.num)))};
  },
  headA:['번호','m, n','x','수치 미분','f′g+fg′','같나?','f′g′','같나?','(m+n)x^(m+n−1)','같나?'],
  rowA:function(r,i){
    return [i+1,r.m+', '+r.n,r.x,'<b>'+r.num+'</b>',r.right,
            '<span class="'+(r.rOk?'ok':'no')+'">'+(r.rOk?'○':'×')+'</span>',
            r.wrong,
            '<span class="'+(r.wOk?'ok':'no')+'">'+(r.wOk?'○':'×')+'</span>',
            r.power,
            '<span class="'+(r.pOk?'ok':'no')+'">'+(r.pOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ro=0,wo=0,po=0,one=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.rOk) ro++;
      if(r.wOk){ wo++; if(r.x===1) one++; }
      if(r.pOk) po++;
      rows.push([r.m+', '+r.n, r.x, '<b>'+r.num+'</b>', r.right,
                 '<span class="'+(r.rOk?'ok':'no')+'">'+(r.rOk?'○':'×')+'</span>',
                 r.wrong,
                 '<span class="'+(r.wOk?'ok':'no')+'">'+(r.wOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'(fg)′ = f′g + fg′',big:ro+' / '+rec.length,p:'수치로 구한 도함수와 비교한 결과.'},
      {t:'(fg)′ = f′g′ 였던 횟수',big:wo+' / '+rec.length,
       p:wo?('그중 x = 1 이었던 것 '+one+'개.'):'각각 미분해 곱하면 맞지 않는다.'},
      {t:'지수법칙으로 구한 값과 일치',big:po+' / '+rec.length,
       p:'x^m · x^n = x^(m+n) 을 바로 미분한 값과도 같았다.'}
    ];
    var concl;
    if(ro===rec.length&&wo===0){
      concl='<b>정리</b> — 곱의 도함수는 <b>f′g + fg′</b> 였고, <b>f′g′ 은 한 번도 맞지 않았다.</b> '
           +'미분은 덧셈·상수배와는 잘 어울리지만 곱셈과는 그렇지 않다. '
           +'x^m · x^n 을 x^(m+n) 으로 먼저 정리해 미분한 값과도 같았으니, 곱의 법칙이 지수법칙과 모순 없이 맞물린다.';
    } else if(ro===rec.length){
      concl='<b>정리</b> — 곱의 법칙은 항상 맞았다. f′g′ 이 우연히 맞은 경우도 특수한 값에서만 생긴다.';
    } else {
      concl='<b>확인 필요</b> — 수치 미분과 공식이 어긋난 기록이 있다.';
    }
    return {head:['m, n','x','수치 미분','f′g+fg′','같나?','f′g′','같나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 미분가능성
# ============================================================
LAB_DIFF = BASE + r"""
var KINDS=['x²','|x|','x³','x^(2/3)'];
function fk2(kind,x){
  if(kind===0) return x*x;
  if(kind===1) return Math.abs(x);
  if(kind===2) return x*x*x;
  return Math.pow(Math.abs(x),2/3);
}
var LAB = {
  cw:440, ch:430, cvTitle:'미분가능성 판',
  action:'양쪽 기울기 재기',
  hint0:'함수를 고르고, x = 0 근처에서 얼마나 가까이 갈지 정해 보자.',
  sliders:[
    {id:'kind',label:'함수',min:0,max:3,value:1,color:'#2563eb',fmt:function(v){return KINDS[v];}},
    {id:'h',label:'거리 h (÷1000)',min:1,max:300,value:100,color:'#f59e0b',
     fmt:function(v){return (v/1000).toFixed(3);}}
  ],
  calc:function(S){
    var h=S.h/1000;
    var f0=fk2(S.kind,0);
    var L=(f0-fk2(S.kind,-h))/h;
    var R=(fk2(S.kind,h)-f0)/h;
    var hs=1e-7;
    var Ls=(fk2(S.kind,0)-fk2(S.kind,-hs))/hs;
    var Rs=(fk2(S.kind,hs)-fk2(S.kind,0))/hs;
    var fin=(isFinite(Ls)&&isFinite(Rs)&&Math.abs(Ls)<1e5&&Math.abs(Rs)<1e5);
    return {h:h,L:L,R:R,f0:f0,
            cont:true,
            diff:(fin&&Math.abs(Ls-Rs)<1e-3)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'왼쪽 기울기',v:ran?r3(c.L):'재 보자'},
            {k:'오른쪽 기울기',v:ran?r3(c.R):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '왼쪽 '+r3(c.L)+', 오른쪽 '+r3(c.R)+'.  '+(c.diff?'두 값이 같아 미분가능하다.':'두 값이 달라(또는 무한대로 가서) 미분가능하지 않다.')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,5,4);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    var st=false;
    for(i=-50;i<=50;i++){
      var x=i/10, y=fk2(S.kind,x);
      if(y<-4||y>4){ st=false; continue; }
      if(!st){ ctx.moveTo(CX+x*U,CY-y*U); st=true; } else ctx.lineTo(CX+x*U,CY-y*U);
    }
    ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    var hh=(t===null)?c.h:(1.5*(1-grow)+c.h*grow);
    var yl=fk2(S.kind,-hh), yr=fk2(S.kind,hh), y0=fk2(S.kind,0);
    var sl=(y0-yl)/hh, sr=(yr-y0)/hh;
    if(isFinite(sl)&&Math.abs(sl)<1e4){
      ctx.strokeStyle='#16a34a';ctx.lineWidth=2.4;
      ctx.beginPath();ctx.moveTo(CX-3*U,CY-(y0+sl*(-3))*U);ctx.lineTo(CX+1*U,CY-(y0+sl*1)*U);ctx.stroke();
    }
    if(isFinite(sr)&&Math.abs(sr)<1e4){
      ctx.strokeStyle='#dc2626';ctx.lineWidth=2.4;
      ctx.beginPath();ctx.moveTo(CX-1*U,CY-(y0+sr*(-1))*U);ctx.lineTo(CX+3*U,CY-(y0+sr*3)*U);ctx.stroke();
    }
    ctx.beginPath();ctx.arc(CX,CY-y0*U,7,0,Math.PI*2);
    ctx.fillStyle='#1f2937';ctx.fill();
    lbl(ctx,'f(x) = '+KINDS[S.kind]+'  ,  x = 0 에서',24,30,'#1d4ed8',17);
    lbl(ctx,'초록 = 왼쪽 기울기,  빨강 = 오른쪽 기울기',24,54,'#52627a',14);
    box(ctx,20,338,400,80);
    lbl(ctx,(t===null)?'양쪽 기울기는 같을까?':('왼쪽 '+r3(c.L)+'      오른쪽 '+r3(c.R)),38,368,'#1f2937',18);
    lbl(ctx,(t===null)?'':('x = 0 에서 연속이고, 미분은 '+(c.diff?'가능':'불가능')),38,400,c.diff?'#15803d':'#b91c1c',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {kind:S.kind,name:KINDS[S.kind],h:r3(c.h),
            L:r3(c.L),R:r3(c.R),cont:true,diff:c.diff,
            eq:(Math.abs(c.L-c.R)<1e-6)};
  },
  headA:['번호','함수','h','왼쪽 기울기','오른쪽 기울기','h에서 같나?','연속?','미분가능?'],
  rowA:function(r,i){
    return [i+1,r.name,r.h,r.L,r.R,
            '<span class="'+(r.eq?'ok':'no')+'">'+(r.eq?'○':'×')+'</span>',
            '<span class="ok">○</span>',
            '<span class="'+(r.diff?'ok':'no')+'">'+(r.diff?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],g={},kn=0,d=[],nd=[];
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(!g[r.name]){ g[r.name]=r; kn++; if(r.diff) d.push(r.name); else nd.push(r.name); }
      rows.push([r.name, r.h, r.L+' / '+r.R,
                 '<span class="ok">○</span>',
                 '<span class="'+(r.diff?'ok':'no')+'">'+(r.diff?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'시험한 함수',big:kn+'가지',p:'네 가지를 모두 기록하면 비교가 완성된다.'},
      {t:'x = 0 에서 미분가능',big:d.length+'가지',p:d.join(', ')||'-'},
      {t:'연속이지만 미분 불가능',big:nd.length+'가지',p:nd.join(', ')||'아직 없음'}
    ];
    var concl;
    if(kn<3){
      concl='<b>더 해 보자</b> — 네 함수를 <b>모두</b> 기록해야 연속과 미분가능의 차이가 드러난다.';
    } else if(nd.length>0){
      concl='<b>정리</b> — 네 함수 모두 x = 0 에서 <b>끊기지 않았지만</b>, '+nd.join(', ')+'는 왼쪽과 오른쪽 기울기가 달라(또는 무한대로 가서) '
           +'<b>미분할 수 없었다.</b> |x|는 뾰족하고, x^(2/3)은 접선이 세로로 서 버린다. '
           +'즉 <b>연속은 미분가능의 필요조건일 뿐 충분조건이 아니다.</b> 반대로 미분가능하면 반드시 연속이다.';
    } else {
      concl='<b>정리</b> — 지금까지는 모두 미분가능했다. |x| 처럼 뾰족한 함수도 기록해 보자.';
    }
    return {head:['함수','h','좌 / 우 기울기','연속?','미분가능?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("hc_limit_lab_Calculus1_Limit_Ep01.html",
     "극한 실험실 — 함숫값이 없어도 극한은 있을까?",
     "극한 실험실 — 함숫값이 없어도 극한은 있을까?",
     "양쪽에서 조금씩 다가가며 값을 재고, 함숫값과 극한값을 구별한다.",
     LAB_LIM),
    ("hc_continuity_lab_Calculus1_Continuity_Ep01.html",
     "연속 실험실 — 무엇이 모두 맞아야 이어질까?",
     "연속 실험실 — 무엇이 모두 맞아야 이어질까?",
     "조각함수의 상수와 함숫값을 바꿔 가며 좌극한·우극한·함숫값 세 값을 비교한다.",
     LAB_CONT),
    ("hc_derivative_lab_Calculus1_Deriv_Ep02.html",
     "미분계수 실험실 — 두 점을 붙이면 무엇이 남을까?",
     "미분계수 실험실 — 두 점을 붙이면 무엇이 남을까?",
     "할선의 기울기를 재며 거리 h를 줄여, 접선의 기울기로 다가가는 과정을 기록한다.",
     LAB_DER),
    ("hc_product_rule_lab_Calculus1_Deriv_Ep05.html",
     "곱의 미분 실험실 — (fg)′ = f′g′ 일까?",
     "곱의 미분 실험실 — (fg)′ = f′g′ 일까?",
     "곱한 함수를 수치로 미분해, 곱의 법칙과 각각 미분해 곱한 값을 비교한다.",
     LAB_PROD),
    ("hc_differentiability_lab_Calculus1_Deriv_Ep03.html",
     "미분가능성 실험실 — 이어져 있으면 미분할 수 있을까?",
     "미분가능성 실험실 — 이어져 있으면 미분할 수 있을까?",
     "네 함수의 x = 0에서 좌우 기울기를 재어 연속과 미분가능을 구별한다.",
     LAB_DIFF),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c27_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
