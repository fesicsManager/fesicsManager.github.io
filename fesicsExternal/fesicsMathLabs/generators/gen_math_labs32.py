# -*- coding: utf-8 -*-
"""고등 기하 — 내적 1종 + 공간도형 4종"""
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
var CX=220, CY=215, U=22;
function grid(ctx,xr,yr){
  var i;
  ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
  for(i=-xr;i<=xr;i++){ ctx.beginPath();ctx.moveTo(CX+i*U,CY-yr*U);ctx.lineTo(CX+i*U,CY+yr*U);ctx.stroke(); }
  for(i=-yr;i<=yr;i++){ ctx.beginPath();ctx.moveTo(CX-xr*U,CY+i*U);ctx.lineTo(CX+xr*U,CY+i*U);ctx.stroke(); }
  ctx.strokeStyle='#334155';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(CX-xr*U,CY);ctx.lineTo(CX+xr*U,CY);ctx.stroke();
  ctx.beginPath();ctx.moveTo(CX,CY-yr*U);ctx.lineTo(CX,CY+yr*U);ctx.stroke();
}
function iso(p,ox,oy,s){
  return [ox + (p[0]-p[1])*0.87*s, oy - p[2]*s - (p[0]+p[1])*0.5*s];
}
"""

# ============================================================
# 1. 벡터의 내적
# ============================================================
LAB_DOT = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'내적 판',
  action:'두 방법으로 내적 구하기',
  hint0:'두 벡터의 성분을 정해 보자.',
  sliders:[
    {id:'a1',label:'a의 x성분',min:-6,max:6,value:4,color:'#2563eb',unit:''},
    {id:'a2',label:'a의 y성분',min:-6,max:6,value:2,color:'#60a5fa',unit:''},
    {id:'b1',label:'b의 x성분',min:-6,max:6,value:-1,color:'#dc2626',unit:''},
    {id:'b2',label:'b의 y성분',min:-6,max:6,value:2,color:'#f87171',unit:''}
  ],
  calc:function(S){
    var dot=S.a1*S.b1+S.a2*S.b2;
    var la=Math.sqrt(S.a1*S.a1+S.a2*S.a2);
    var lb=Math.sqrt(S.b1*S.b1+S.b2*S.b2);
    var cos=(la*lb===0)?0:(dot/(la*lb));
    if(cos>1)cos=1; if(cos<-1)cos=-1;
    var th=Math.acos(cos)*180/Math.PI;
    return {dot:dot,la:la,lb:lb,th:th,geo:la*lb*cos,
            perp:(Math.abs(dot)<1e-9&&la>0&&lb>0),
            proj:(lb===0)?0:(dot/lb)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'성분으로',v:c.dot},
            {k:'|a||b|cosθ',v:ran?r3(c.geo):'구해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '성분 내적 '+c.dot+', |a||b|cosθ = '+r3(c.geo)+', 각 '+r1(c.th)+'°.  '+(c.perp?'내적이 0이라 수직이다.':'')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    grid(ctx,7,6);
    function arrow(dx,dy,col,w){
      var X1=CX+dx*U, Y1=CY-dy*U;
      ctx.strokeStyle=col;ctx.lineWidth=w||3;
      ctx.beginPath();ctx.moveTo(CX,CY);ctx.lineTo(X1,Y1);ctx.stroke();
      var ang=Math.atan2(Y1-CY,X1-CX);
      ctx.beginPath();ctx.moveTo(X1,Y1);
      ctx.lineTo(X1-10*Math.cos(ang-0.4),Y1-10*Math.sin(ang-0.4));
      ctx.lineTo(X1-10*Math.cos(ang+0.4),Y1-10*Math.sin(ang+0.4));
      ctx.closePath();ctx.fillStyle=col;ctx.fill();
    }
    arrow(S.a1,S.a2,'#2563eb');
    arrow(S.b1,S.b2,'#dc2626');
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0&&c.lb>0){
      var ux=S.b1/c.lb, uy=S.b2/c.lb;
      var px=c.proj*ux, py=c.proj*uy;
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=4;
      ctx.beginPath();ctx.moveTo(CX,CY);ctx.lineTo(CX+px*U*grow,CY-py*U*grow);ctx.stroke();
      ctx.strokeStyle='#94a3b8';ctx.lineWidth=1.6;ctx.setLineDash([4,4]);
      ctx.beginPath();ctx.moveTo(CX+S.a1*U,CY-S.a2*U);ctx.lineTo(CX+px*U,CY-py*U);ctx.stroke();
      ctx.setLineDash([]);
      if(grow>=1) lbl(ctx,'a의 그림자 '+r2(c.proj),CX+px*U+8,CY-py*U+18,'#b45309',13);
    }
    if(grow>0&&c.la>0&&c.lb>0){
      ctx.beginPath();
      var a1=Math.atan2(-S.a2,S.a1), a2=Math.atan2(-S.b2,S.b1);
      ctx.arc(CX,CY,34,Math.min(a1,a2),Math.max(a1,a2));
      ctx.strokeStyle='#7c3aed';ctx.lineWidth=2;ctx.stroke();
    }
    lbl(ctx,'a = ('+S.a1+', '+S.a2+')      b = ('+S.b1+', '+S.b2+')',24,32,'#334155',16);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'두 방법의 결과는 같을까?':('성분 '+c.dot+'      |a||b|cosθ = '+r3(c.geo)),38,376,'#1f2937',18);
    lbl(ctx,'|a| = '+r2(c.la)+'   |b| = '+r2(c.lb)+'   각 '+r1(c.th)+'°'+(c.perp?'   (수직)':''),
        38,406,c.perp?'#15803d':'#52627a',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:'('+S.a1+','+S.a2+')',b:'('+S.b1+','+S.b2+')',
            dot:c.dot,geo:r3(c.geo),la:r2(c.la),lb:r2(c.lb),th:r1(c.th),
            same:(Math.abs(c.dot-c.geo)<1e-6),
            perp:c.perp,
            th90:(Math.abs(c.th-90)<0.05),
            neg:(c.dot<0),obtuse:(c.th>90)};
  },
  headA:['번호','a','b','성분 내적','|a||b|cosθ','같나?','각','내적 0?','각 90°?'],
  rowA:function(r,i){
    return [i+1,r.a,r.b,'<b>'+r.dot+'</b>',r.geo,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            r.th+'°',
            '<span class="'+(r.perp?'ok':'no')+'">'+(r.perp?'○':'×')+'</span>',
            '<span class="'+(r.th90?'ok':'no')+'">'+(r.th90?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,match=0,neg=0,negObt=0,perp=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.perp===r.th90) match++;
      if(r.perp) perp++;
      if(r.neg){ neg++; if(r.obtuse) negObt++; }
      rows.push([r.a+' · '+r.b, '<b>'+r.dot+'</b>', r.geo,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 r.th+'°',
                 '<span class="'+(r.perp?'ok':'no')+'">'+(r.perp?'○':'×')+'</span>',
                 '<span class="'+(r.th90?'ok':'no')+'">'+(r.th90?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'성분 내적 = |a||b|cosθ',big:same+' / '+rec.length,p:'두 계산 방법이 같은 값을 주는지 확인한 결과.'},
      {t:'“내적 0”과 “각 90°”가 일치',big:match+' / '+rec.length,
       p:perp?('수직이었던 기록 '+perp+'개.'):'수직인 두 벡터도 만들어 보자.'},
      {t:'내적이 음수였던 기록',big:neg+'개',
       p:neg?('그중 각이 90°보다 컸던 것 '+negObt+'개.'):'둔각을 이루는 두 벡터도 해 보자.'}
    ];
    var concl;
    if(perp===0||neg===0){
      concl='<b>더 해 보자</b> — <b>수직인 경우</b>와 <b>둔각을 이루는 경우</b>를 모두 만들어 보자. (4,2)와 (−1,2)는 수직이다.';
    } else if(same===rec.length&&match===rec.length){
      concl='<b>정리</b> — 성분끼리 곱해 더한 값과 |a||b|cosθ 가 언제나 같았다. '
           +'내적은 “b 방향으로 본 a의 그림자 × |b|” 이므로, <b>내적이 0인 것은 그림자가 없다는 뜻, 즉 수직</b>이다. '
           +'각이 둔각이면 그림자가 반대쪽으로 생겨 내적이 음수가 되었다. 내적의 부호만으로 예각·직각·둔각을 판정할 수 있다.';
    } else {
      concl='<b>확인 필요</b> — 두 계산이 어긋난 기록이 있다.';
    }
    return {head:['a · b','성분','|a||b|cosθ','같나?','각','내적 0?','각 90°?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 공간에서 두 점 사이 거리
# ============================================================
LAB_SPACE = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'공간 거리 판',
  action:'두 번 피타고라스',
  hint0:'점 P의 좌표를 정해 보자. 원점 O에서 P까지의 거리를 잰다.',
  sliders:[
    {id:'x',label:'x',min:0,max:6,value:3,color:'#2563eb',unit:''},
    {id:'y',label:'y',min:0,max:6,value:4,color:'#16a34a',unit:''},
    {id:'z',label:'z',min:0,max:6,value:5,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var flat=Math.sqrt(S.x*S.x+S.y*S.y);
    var d=Math.sqrt(S.x*S.x+S.y*S.y+S.z*S.z);
    return {flat:flat,d:d,step:Math.sqrt(flat*flat+S.z*S.z)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'xy평면 위 그림자까지',v:ran?r3(c.flat):'재 보자'},
            {k:'O에서 P까지',v:ran?r3(c.d):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '그림자까지 '+r3(c.flat)+', P까지 '+r3(c.d)+'.  √(그림자² + z²) = '+r3(c.step)+'와 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var ox=150, oy=300, s=32;
    function P(p){ return iso(p,ox,oy,s); }
    ctx.strokeStyle='#e2e8f0';ctx.lineWidth=1;
    for(i=0;i<=6;i++){
      var a=P([i,0,0]), b=P([i,6,0]);
      ctx.beginPath();ctx.moveTo(a[0],a[1]);ctx.lineTo(b[0],b[1]);ctx.stroke();
      var a2=P([0,i,0]), b2=P([6,i,0]);
      ctx.beginPath();ctx.moveTo(a2[0],a2[1]);ctx.lineTo(b2[0],b2[1]);ctx.stroke();
    }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    [[6,0,0],[0,6,0],[0,0,6]].forEach(function(v,k){
      var o=P([0,0,0]), e=P(v);
      ctx.beginPath();ctx.moveTo(o[0],o[1]);ctx.lineTo(e[0],e[1]);ctx.stroke();
      lbl(ctx,['x','y','z'][k],e[0]+6,e[1]+4,'#64748b',14);
    });
    var grow=(t===null)?0:Math.min(1,t);
    var O=P([0,0,0]), F=P([S.x,S.y,0]), Q=P([S.x,S.y,S.z]);
    if(grow>0){
      ctx.strokeStyle='#16a34a';ctx.lineWidth=3;
      ctx.beginPath();ctx.moveTo(O[0],O[1]);
      ctx.lineTo(O[0]+(F[0]-O[0])*Math.min(1,grow*2),O[1]+(F[1]-O[1])*Math.min(1,grow*2));ctx.stroke();
    }
    if(grow>0.5){
      var g2=(grow-0.5)/0.5;
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=3;
      ctx.beginPath();ctx.moveTo(F[0],F[1]);
      ctx.lineTo(F[0]+(Q[0]-F[0])*g2,F[1]+(Q[1]-F[1])*g2);ctx.stroke();
    }
    if(grow>=1){
      ctx.strokeStyle='#dc2626';ctx.lineWidth=3;
      ctx.beginPath();ctx.moveTo(O[0],O[1]);ctx.lineTo(Q[0],Q[1]);ctx.stroke();
    }
    [[F,'#16a34a'],[Q,'#dc2626']].forEach(function(q){
      ctx.beginPath();ctx.arc(q[0][0],q[0][1],6,0,Math.PI*2);
      ctx.fillStyle=q[1];ctx.fill();
    });
    lbl(ctx,'P ( '+S.x+' , '+S.y+' , '+S.z+' )',24,32,'#1d4ed8',18);
    lbl(ctx,'초록 = 평면 위 그림자,  주황 = 높이,  빨강 = 직접',24,56,'#52627a',13);
    box(ctx,20,346,400,74);
    lbl(ctx,'그림자까지 √('+(S.x*S.x)+'+'+(S.y*S.y)+') = '+r3(c.flat),38,376,'#15803d',17);
    lbl(ctx,(t===null)?'공간에서의 거리는?':('O에서 P까지 = '+r3(c.d)+'      √(그림자²+z²) = '+r3(c.step)),38,406,'#1f2937',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {x:S.x,y:S.y,z:S.z,flat:r3(c.flat),d:r3(c.d),step:r3(c.step),
            same:(Math.abs(c.d-c.step)<1e-9),
            wrong:r3(S.x+S.y+S.z),
            wOk:(Math.abs(c.d-(S.x+S.y+S.z))<1e-9)};
  },
  headA:['번호','P','그림자까지','O~P','√(그림자²+z²)','같나?','x+y+z','같나?'],
  rowA:function(r,i){
    return [i+1,'('+r.x+','+r.y+','+r.z+')',r.flat,'<b>'+r.d+'</b>',r.step,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            r.wrong,
            '<span class="'+(r.wOk?'ok':'no')+'">'+(r.wOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,w=0,zero=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.wOk){ w++; if((r.x===0&&r.y===0)||(r.y===0&&r.z===0)||(r.x===0&&r.z===0)) zero++; }
      rows.push(['('+r.x+','+r.y+','+r.z+')', r.flat, '<b>'+r.d+'</b>', r.step,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 r.wrong,
                 '<span class="'+(r.wOk?'ok':'no')+'">'+(r.wOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'√(그림자² + z²) = O~P',big:same+' / '+rec.length,p:'피타고라스를 두 번 쓴 결과와 직접 거리를 비교했다.'},
      {t:'x + y + z 가 맞은 횟수',big:w+' / '+rec.length,
       p:w?('그중 두 좌표가 0이었던 것 '+zero+'개.'):'좌표를 그냥 더하면 맞지 않는다.'},
      {t:'기록 수',big:rec.length+'개',p:'공간 거리는 √(x²+y²+z²) 이다.'}
    ];
    var concl;
    if(same===rec.length&&w===zero){
      concl='<b>정리</b> — 공간에서의 거리는 <b>피타고라스를 두 번</b> 쓴 것과 같았다. '
           +'먼저 xy평면 위 그림자까지의 거리를 구하고, 그것과 높이 z로 다시 직각삼각형을 만들면 √(x²+y²+z²) 가 된다. '
           +'좌표를 그냥 더한 x + y + z 는 두 좌표가 0일 때만 우연히 맞았다.';
    } else {
      concl='<b>확인 필요</b> — 두 계산이 어긋난 기록이 있다.';
    }
    return {head:['P','그림자','O~P','√(그림자²+z²)','같나?','x+y+z','같나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 꼬인 위치
# ============================================================
LAB_SKEW = BASE + r"""
var V=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]];
var E=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]];
var ENAME=['AB','BC','CD','DA','EF','FG','GH','HE','AE','BF','CG','DH'];
function relate(i,j){
  if(i===j) return '같은 모서리';
  var p=E[i], q=E[j];
  var d1=[V[p[1]][0]-V[p[0]][0],V[p[1]][1]-V[p[0]][1],V[p[1]][2]-V[p[0]][2]];
  var d2=[V[q[1]][0]-V[q[0]][0],V[q[1]][1]-V[q[0]][1],V[q[1]][2]-V[q[0]][2]];
  var cx=d1[1]*d2[2]-d1[2]*d2[1], cy=d1[2]*d2[0]-d1[0]*d2[2], cz=d1[0]*d2[1]-d1[1]*d2[0];
  var par=(Math.abs(cx)+Math.abs(cy)+Math.abs(cz)<1e-9);
  var share=(p[0]===q[0]||p[0]===q[1]||p[1]===q[0]||p[1]===q[1]);
  if(par) return '평행';
  if(share) return '한 점에서 만남';
  return '꼬인 위치';
}
var LAB = {
  cw:440, ch:430, cvTitle:'정육면체 모서리 판',
  action:'두 모서리 살펴보기',
  hint0:'정육면체의 두 모서리를 골라 보자.',
  sliders:[
    {id:'e1',label:'첫 번째 모서리',min:0,max:11,value:0,color:'#2563eb',fmt:function(v){return ENAME[v];}},
    {id:'e2',label:'두 번째 모서리',min:0,max:11,value:10,color:'#dc2626',fmt:function(v){return ENAME[v];}}
  ],
  readout:function(S,ran){
    return [{k:'두 모서리',v:ENAME[S.e1]+' 와 '+ENAME[S.e2]},
            {k:'위치 관계',v:ran?relate(S.e1,S.e2):'살펴보자'}];
  },
  doneMsg:function(S){
    var rel=relate(S.e1,S.e2);
    return ENAME[S.e1]+'와 '+ENAME[S.e2]+'는 「'+rel+'」이다. 다른 짝도 골라 보자.';
  },
  draw:function(ctx,S,t,ran){
    var i;
    var ox=210, oy=290, s=110;
    function P(p){ return iso(p,ox,oy,s); }
    var NM=['A','B','C','D','E','F','G','H'];
    for(i=0;i<12;i++){
      var a=P(V[E[i][0]]), b=P(V[E[i][1]]);
      var hit=(i===S.e1||i===S.e2);
      ctx.strokeStyle=hit?((i===S.e1)?'#2563eb':'#dc2626'):'#cbd5e1';
      ctx.lineWidth=hit?5:2;
      ctx.beginPath();ctx.moveTo(a[0],a[1]);ctx.lineTo(b[0],b[1]);ctx.stroke();
    }
    for(i=0;i<8;i++){
      var p=P(V[i]);
      ctx.beginPath();ctx.arc(p[0],p[1],4,0,Math.PI*2);ctx.fillStyle='#334155';ctx.fill();
      lbl(ctx,NM[i],p[0]+7,p[1]-6,'#64748b',13);
    }
    var rel=relate(S.e1,S.e2);
    lbl(ctx,'파랑 '+ENAME[S.e1]+' ,  빨강 '+ENAME[S.e2],24,32,'#334155',16);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'두 모서리는 어떤 관계일까?':('위치 관계 : '+rel),38,378,
        (rel==='꼬인 위치')?'#b91c1c':'#1f2937',20);
    lbl(ctx,(t===null)?'':'만나지 않는다고 평행인 것은 아니다',38,406,'#52627a',15);
  },
  record:function(S){
    var rel=relate(S.e1,S.e2);
    return {e1:ENAME[S.e1],e2:ENAME[S.e2],rel:rel,
            skew:(rel==='꼬인 위치'),par:(rel==='평행'),meet:(rel==='한 점에서 만남'),
            noMeet:(rel==='평행'||rel==='꼬인 위치')};
  },
  headA:['번호','모서리 1','모서리 2','위치 관계','만나나?','평행?'],
  rowA:function(r,i){
    return [i+1,r.e1,r.e2,'<b>'+r.rel+'</b>',
            '<span class="'+(r.meet?'ok':'no')+'">'+(r.meet?'○':'×')+'</span>',
            '<span class="'+(r.par?'ok':'no')+'">'+(r.par?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],par=0,meet=0,skew=0,noMeet=0,noMeetPar=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.par) par++;
      if(r.meet) meet++;
      if(r.skew) skew++;
      if(r.noMeet){ noMeet++; if(r.par) noMeetPar++; }
      rows.push([r.e1+' , '+r.e2, '<b>'+r.rel+'</b>',
                 '<span class="'+(r.meet?'ok':'no')+'">'+(r.meet?'○':'×')+'</span>',
                 '<span class="'+(r.par?'ok':'no')+'">'+(r.par?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'평행 / 한 점에서 만남 / 꼬인 위치',big:par+' / '+meet+' / '+skew,
       p:(par&&meet&&skew)?'세 경우를 모두 기록했다.':'세 관계를 모두 찾아보자.'},
      {t:'만나지 않았던 기록',big:noMeet+'개',
       p:noMeet?('그중 평행이었던 것 '+noMeetPar+'개.'):'만나지 않는 두 모서리를 골라 보자.'},
      {t:'꼬인 위치',big:skew+'개',
       p:skew?'만나지도 않고 평행하지도 않은 경우다.':'AB와 CG처럼 골라 보자.'}
    ];
    var concl;
    if(!(par&&meet&&skew)){
      concl='<b>더 해 보자</b> — 평행(AB와 CD), 한 점에서 만남(AB와 BC), 꼬인 위치(AB와 CG)를 <b>모두</b> 기록해 보자.';
    } else {
      concl='<b>정리</b> — 공간에서 두 직선의 관계는 세 가지였다. '
           +'평면에서는 “만나거나 평행”뿐이지만, 공간에서는 <b>만나지 않으면서 평행하지도 않은 «꼬인 위치»</b>가 있다. '
           +'만나지 않는 '+noMeet+'번 중 평행은 '+noMeetPar+'번뿐이었다. '
           +'두 직선이 한 평면 위에 있어야만 평행을 말할 수 있다.';
    }
    return {head:['두 모서리','위치 관계','만나나?','평행?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 정사영
# ============================================================
LAB_PROJ = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'정사영 판',
  action:'그림자 넓이 재기',
  hint0:'직사각형의 크기와 기울인 각을 정해 보자.',
  sliders:[
    {id:'w',label:'가로',min:1,max:6,value:4,color:'#2563eb',unit:''},
    {id:'h',label:'세로',min:1,max:6,value:3,color:'#16a34a',unit:''},
    {id:'th',label:'기울인 각',min:0,max:85,value:60,color:'#f59e0b',unit:'°'}
  ],
  calc:function(S){
    var rad=S.th*Math.PI/180;
    var pts=[[0,0,0],[S.w,0,0],[S.w,S.h*Math.cos(rad),S.h*Math.sin(rad)],[0,S.h*Math.cos(rad),S.h*Math.sin(rad)]];
    var sh=0,i;
    for(i=0;i<4;i++){
      var a=pts[i], b=pts[(i+1)%4];
      sh+=a[0]*b[1]-b[0]*a[1];
    }
    var area=Math.abs(sh)/2;
    return {pts:pts,S:S.w*S.h,proj:area,formula:S.w*S.h*Math.cos(rad),rad:rad};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'원래 넓이',v:c.S},
            {k:'그림자 넓이',v:ran?r3(c.proj):'재 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '원래 넓이 '+c.S+', 그림자 넓이 '+r3(c.proj)+', S cosθ = '+r3(c.formula)+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var ox=170, oy=300, s=40;
    function P(p){ return iso(p,ox,oy,s); }
    ctx.strokeStyle='#e2e8f0';ctx.lineWidth=1;
    for(i=0;i<=7;i++){
      var a=P([i,0,0]), b=P([i,7,0]);
      ctx.beginPath();ctx.moveTo(a[0],a[1]);ctx.lineTo(b[0],b[1]);ctx.stroke();
      var a2=P([0,i,0]), b2=P([7,i,0]);
      ctx.beginPath();ctx.moveTo(a2[0],a2[1]);ctx.lineTo(b2[0],b2[1]);ctx.stroke();
    }
    var grow=(t===null)?0:Math.min(1,t);
    ctx.beginPath();
    for(i=0;i<4;i++){
      var q=P(c.pts[i]);
      if(i===0) ctx.moveTo(q[0],q[1]); else ctx.lineTo(q[0],q[1]);
    }
    ctx.closePath();
    ctx.fillStyle='rgba(37,99,235,0.25)';ctx.fill();
    ctx.strokeStyle='#2563eb';ctx.lineWidth=2.5;ctx.stroke();
    if(grow>0){
      ctx.beginPath();
      for(i=0;i<4;i++){
        var q2=P([c.pts[i][0],c.pts[i][1],0]);
        if(i===0) ctx.moveTo(q2[0],q2[1]); else ctx.lineTo(q2[0],q2[1]);
      }
      ctx.closePath();
      ctx.globalAlpha=grow;
      ctx.fillStyle='rgba(245,158,11,0.35)';ctx.fill();
      ctx.strokeStyle='#d97706';ctx.lineWidth=2.5;ctx.stroke();
      ctx.globalAlpha=1;
      ctx.strokeStyle='#94a3b8';ctx.lineWidth=1.2;ctx.setLineDash([3,3]);
      for(i=0;i<4;i++){
        var u=P(c.pts[i]), d=P([c.pts[i][0],c.pts[i][1],0]);
        ctx.beginPath();ctx.moveTo(u[0],u[1]);ctx.lineTo(d[0],d[1]);ctx.stroke();
      }
      ctx.setLineDash([]);
    }
    lbl(ctx,'가로 '+S.w+' × 세로 '+S.h+' 를 '+S.th+'° 기울임',24,32,'#1d4ed8',17);
    lbl(ctx,'파랑 = 원래 도형,  주황 = 바닥에 생긴 그림자',24,56,'#52627a',13);
    box(ctx,20,346,400,74);
    lbl(ctx,'원래 넓이 '+c.S,38,376,'#1d4ed8',18);
    lbl(ctx,(t===null)?'그림자 넓이는 얼마일까?':('그림자 '+r3(c.proj)+'      S cos'+S.th+'° = '+r3(c.formula)),
        38,406,'#1f2937',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {w:S.w,h:S.h,th:S.th,S:c.S,proj:r3(c.proj),formula:r3(c.formula),
            same:(Math.abs(c.proj-c.formula)<1e-6),
            ratio:r3(c.proj/c.S),
            cos:r3(Math.cos(c.rad)),
            flat:(S.th===0)};
  },
  headA:['번호','가로×세로','각','원래 넓이','그림자 넓이','S cosθ','같나?','비','cosθ'],
  rowA:function(r,i){
    return [i+1,r.w+'×'+r.h,r.th+'°',r.S,'<b>'+r.proj+'</b>',r.formula,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            r.ratio,r.cos];
  },
  analyze:function(rec){
    var rows=[],same=0,rat=0,flat=0,mn=9,mnT=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(Math.abs(parseFloat(r.ratio)-parseFloat(r.cos))<1e-6) rat++;
      if(r.flat) flat++;
      if(parseFloat(r.ratio)<mn){ mn=parseFloat(r.ratio); mnT=r.th; }
      rows.push([r.w+'×'+r.h, r.th+'°', r.S, '<b>'+r.proj+'</b>', r.formula,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 r.ratio+' / '+r.cos]);
    }
    var stats=[
      {t:'그림자 넓이 = S cosθ',big:same+' / '+rec.length,
       p:'좌표에서 직접 잰 그림자 넓이와 공식을 비교한 결과.'},
      {t:'그림자 ÷ 원래 = cosθ',big:rat+' / '+rec.length,
       p:'줄어드는 비율이 각에만 달렸는지 확인한 결과.'},
      {t:'가장 많이 줄어든 경우',big:mn+'배',p:'각 '+mnT+'° 일 때. 각이 0°이면 그대로였던 기록 '+flat+'개.'}
    ];
    var concl;
    if(same===rec.length&&rat===rec.length){
      concl='<b>정리</b> — 기울인 도형의 그림자 넓이는 언제나 <b>원래 넓이 × cosθ</b> 였다. '
           +'기울이는 방향으로만 짧아지고 그 직각 방향은 그대로라서, 넓이가 cosθ 배가 된다. '
           +'각이 0°면 그대로, 90°에 가까울수록 그림자가 선처럼 얇아졌다. 도형의 모양과 상관없이 성립한다.';
    } else {
      concl='<b>확인 필요</b> — 잰 넓이와 공식이 어긋난 기록이 있다.';
    }
    return {head:['크기','각','원래 넓이','그림자','S cosθ','같나?','비 / cosθ'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 구와 평면
# ============================================================
LAB_SPHERE = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'구와 평면 판',
  action:'잘라 보기',
  hint0:'구의 반지름과, 중심에서 평면까지의 거리를 정해 보자.',
  sliders:[
    {id:'r',label:'구의 반지름',min:2,max:7,value:5,color:'#2563eb',unit:''},
    {id:'d',label:'중심에서 평면까지',min:0,max:9,value:3,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var inside=S.r*S.r-S.d*S.d;
    var kind=(inside>1e-9)?'원':((inside<-1e-9)?'만나지 않음':'한 점(접함)');
    return {rr:(inside>0)?Math.sqrt(inside):0,kind:kind,
            area:(inside>0)?Math.PI*inside:0};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'d와 r',v:S.d+' vs '+S.r},
            {k:'잘린 자리',v:ran?c.kind:'잘라 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '거리 '+S.d+', 반지름 '+S.r+'.  잘린 자리는 '+c.kind
      +((c.kind==='원')?(' (반지름 '+r3(c.rr)+')'):'')+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var OX=220, OY=190, sc=22;
    ctx.beginPath();ctx.arc(OX,OY,S.r*sc,0,Math.PI*2);
    ctx.fillStyle='rgba(37,99,235,0.10)';ctx.fill();
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.stroke();
    ctx.beginPath();ctx.arc(OX,OY,4,0,Math.PI*2);ctx.fillStyle='#1f2937';ctx.fill();
    var grow=(t===null)?0:Math.min(1,t);
    var py=OY+S.d*sc;
    ctx.strokeStyle='#f59e0b';ctx.lineWidth=3;
    ctx.beginPath();ctx.moveTo(40,py);ctx.lineTo(400,py);ctx.stroke();
    ctx.strokeStyle='#94a3b8';ctx.lineWidth=1.8;ctx.setLineDash([4,4]);
    ctx.beginPath();ctx.moveTo(OX,OY);ctx.lineTo(OX,py);ctx.stroke();ctx.setLineDash([]);
    lbl(ctx,'d = '+S.d,OX+8,(OY+py)/2,'#b45309',14);
    if(grow>0&&c.rr>0){
      ctx.strokeStyle='#dc2626';ctx.lineWidth=4;
      ctx.beginPath();ctx.moveTo(OX-c.rr*sc*grow,py);ctx.lineTo(OX+c.rr*sc*grow,py);ctx.stroke();
      if(grow>=1){
        ctx.beginPath();
        ctx.ellipse(OX,py,c.rr*sc,c.rr*sc*0.3,0,0,Math.PI*2);
        ctx.strokeStyle='#dc2626';ctx.lineWidth=2;ctx.stroke();
        lbl(ctx,'잘린 원의 반지름 '+r3(c.rr),OX+c.rr*sc+8,py-8,'#b91c1c',14);
      }
    }
    lbl(ctx,'반지름 '+S.r+'인 구를 평면으로 자르기',24,32,'#1d4ed8',17);
    box(ctx,20,346,400,74);
    lbl(ctx,'d = '+S.d+'      r = '+S.r+'      d '+((S.d<S.r)?'<':((S.d>S.r)?'>':'='))+' r',38,376,'#52627a',18);
    lbl(ctx,(t===null)?'잘린 자리는 무엇이 될까?':('잘린 자리 : '+c.kind+((c.rr>0)?('   반지름 '+r3(c.rr)):'')),
        38,406,(c.kind==='원')?'#15803d':((c.kind==='만나지 않음')?'#b91c1c':'#b45309'),17);
  },
  record:function(S){
    var c=this.calc(S);
    return {r:S.r,d:S.d,kind:c.kind,rr:r3(c.rr),
            cmp:(S.d<S.r)?'<':((S.d>S.r)?'>':'='),
            pyth:(c.rr>0)?(Math.abs(c.rr*c.rr+S.d*S.d-S.r*S.r)<1e-6):true,
            circle:(c.kind==='원')};
  },
  headA:['번호','r','d','d와 r','잘린 자리','잘린 원의 반지름','r² = d² + (반지름)²?'],
  rowA:function(r,i){
    return [i+1,r.r,r.d,'d '+r.cmp+' r','<b>'+r.kind+'</b>',(r.rr>0)?r.rr:'-',
            '<span class="'+(r.pyth?'ok':'no')+'">'+(r.pyth?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],match=0,ci=0,pt=0,no=0,pyth=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var expect=(r.cmp==='<')?'원':((r.cmp==='>')?'만나지 않음':'한 점(접함)');
      if(expect===r.kind) match++;
      if(r.kind==='원') ci++; else if(r.kind==='만나지 않음') no++; else pt++;
      if(r.pyth) pyth++;
      rows.push([r.r, r.d, 'd '+r.cmp+' r', '<b>'+r.kind+'</b>', (r.rr>0)?r.rr:'-',
                 '<span class="'+(r.pyth?'ok':'no')+'">'+(r.pyth?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'d와 r 비교로 한 예측이 맞은 횟수',big:match+' / '+rec.length,
       p:'거리만으로 잘린 자리를 판정할 수 있는지 확인한 결과.'},
      {t:'원 / 접함 / 만나지 않음',big:ci+' / '+pt+' / '+no,
       p:(ci&&pt&&no)?'세 경우를 모두 기록했다.':'세 경우를 모두 만들어 보자.'},
      {t:'r² = d² + (잘린 원의 반지름)²',big:pyth+' / '+rec.length,
       p:'중심·평면·원 위 한 점이 직각삼각형을 이룬다.'}
    ];
    var concl;
    if(!(ci&&pt&&no)){
      concl='<b>더 해 보자</b> — d를 r보다 작게, 같게, 크게 하여 <b>세 경우를 모두</b> 만들어 보자.';
    } else if(match===rec.length&&pyth===rec.length){
      concl='<b>정리</b> — 구와 평면의 관계는 <b>중심에서 평면까지의 거리 d와 반지름 r만 비교</b>하면 알 수 있었다. '
           +'d &lt; r 이면 원, d = r 이면 한 점(접함), d &gt; r 이면 만나지 않는다. '
           +'잘린 원의 반지름은 <b>r² = d² + (반지름)²</b> 로 정해졌다. 원과 직선의 관계가 한 차원 올라간 모습이다.';
    } else {
      concl='<b>확인 필요</b> — 예측과 결과가 어긋난 기록이 있다.';
    }
    return {head:['r','d','d와 r','잘린 자리','반지름','피타고라스'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("hg_dot_product_lab_Geometry_DotProduct_Ep05.html",
     "내적 실험실 — 내적이 0이면 무슨 뜻일까?",
     "내적 실험실 — 내적이 0이면 무슨 뜻일까?",
     "성분으로 구한 내적과 |a||b|cosθ를 비교하고, 내적의 부호와 각의 관계를 확인한다.",
     LAB_DOT),
    ("hg_space_distance_lab_Geometry_SpaceCoord_Ep02.html",
     "공간 거리 실험실 — 좌표를 그냥 더하면 될까?",
     "공간 거리 실험실 — 좌표를 그냥 더하면 될까?",
     "평면 위 그림자까지의 거리와 높이로 피타고라스를 두 번 써서 공간 거리를 구한다.",
     LAB_SPACE),
    ("hg_skew_lines_lab_Geometry_Solid_Ep01.html",
     "꼬인 위치 실험실 — 만나지 않으면 평행일까?",
     "꼬인 위치 실험실 — 만나지 않으면 평행일까?",
     "정육면체의 두 모서리를 골라 평행·만남·꼬인 위치를 판정하고 기록한다.",
     LAB_SKEW),
    ("hg_projection_lab_Geometry_Solid_Ep06.html",
     "정사영 실험실 — 그림자는 얼마나 줄어들까?",
     "정사영 실험실 — 그림자는 얼마나 줄어들까?",
     "직사각형을 기울여 바닥에 생긴 그림자의 넓이를 좌표로 재고 S cosθ와 비교한다.",
     LAB_PROJ),
    ("hg_sphere_plane_lab_Geometry_SpaceCoord_Ep06.html",
     "구와 평면 실험실 — 자르면 무엇이 나올까?",
     "구와 평면 실험실 — 자르면 무엇이 나올까?",
     "중심에서 평면까지의 거리를 바꿔 가며 잘린 자리의 모양과 크기를 기록한다.",
     LAB_SPHERE),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c32_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
