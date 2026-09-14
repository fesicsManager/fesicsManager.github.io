# -*- coding: utf-8 -*-
"""중3 보강 5종 — 원의 성질 3종 + 삼각비 1종 + 자료 1종"""
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
function dist(p,q){return Math.sqrt((p[0]-q[0])*(p[0]-q[0])+(p[1]-q[1])*(p[1]-q[1]));}
function angDeg(p,q,r){
  var ax=p[0]-q[0],ay=p[1]-q[1],bx=r[0]-q[0],by=r[1]-q[1];
  var d=ax*bx+ay*by,m=Math.sqrt(ax*ax+ay*ay)*Math.sqrt(bx*bx+by*by);
  var c=(m===0)?1:d/m; if(c>1)c=1; if(c<-1)c=-1;
  return Math.acos(c)*180/Math.PI;
}
"""

# ============================================================
# 1. 현과 중심에서의 거리
# ============================================================
LAB_CHORD = BASE + r"""
var CX=220, CY=200;
var LAB = {
  cw:440, ch:400, cvTitle:'현 실험판',
  action:'수선을 내려 재기',
  hint0:'원의 반지름과, 중심에서 현까지의 거리를 정해 보자.',
  sliders:[
    {id:'r',label:'반지름',min:60,max:150,value:120,color:'#2563eb',fmt:function(v){return (v/20).toFixed(1)+'cm';}},
    {id:'d',label:'중심에서 현까지 거리',min:0,max:140,value:60,color:'#f59e0b',fmt:function(v){return (v/20).toFixed(1)+'cm';}}
  ],
  calc:function(S){
    var d=Math.min(S.d,S.r-2);
    var half=Math.sqrt(S.r*S.r-d*d);
    var A=[CX-half,CY-d], B=[CX+half,CY-d];
    var M=[CX,CY-d];
    return {d:d,half:half,len:2*half,A:A,B:B,M:M,
            ang:angDeg([CX,CY],M,A),
            ma:dist(M,A),mb:dist(M,B)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'중심에서의 거리',v:(c.d/20).toFixed(2)+'cm'},
            {k:'현의 길이',v:ran?((c.len/20).toFixed(2)+'cm'):'재 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '현의 길이는 '+(c.len/20).toFixed(2)+'cm이고, 수선의 발에서 양 끝까지가 '+(c.ma/20).toFixed(2)+'cm로 같다. 거리를 바꿔 다시 재 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    ctx.beginPath();ctx.arc(CX,CY,S.r,0,Math.PI*2);
    ctx.strokeStyle='#94a3b8';ctx.lineWidth=2.5;ctx.stroke();
    ctx.strokeStyle='#2563eb';ctx.lineWidth=4;
    ctx.beginPath();ctx.moveTo(c.A[0],c.A[1]);ctx.lineTo(c.B[0],c.B[1]);ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=3;
      ctx.beginPath();ctx.moveTo(CX,CY);
      ctx.lineTo(CX,CY+(c.M[1]-CY)*grow);ctx.stroke();
    }
    if(grow>=1){
      ctx.strokeStyle='#dc2626';ctx.lineWidth=2;
      ctx.strokeRect(c.M[0],c.M[1],12,12);
      ctx.beginPath();ctx.arc(c.M[0],c.M[1],5,0,Math.PI*2);ctx.fillStyle='#dc2626';ctx.fill();
      lbl(ctx,(c.ma/20).toFixed(2),(c.A[0]+c.M[0])/2,c.M[1]-10,'#1d4ed8',14,'center');
      lbl(ctx,(c.mb/20).toFixed(2),(c.B[0]+c.M[0])/2,c.M[1]-10,'#1d4ed8',14,'center');
    }
    ctx.beginPath();ctx.arc(CX,CY,5,0,Math.PI*2);ctx.fillStyle='#1f2937';ctx.fill();
    lbl(ctx,'중심에서 현에 수선을 내리면?',24,34,'#1d4ed8',18);
    box(ctx,20,314,400,70);
    lbl(ctx,'현의 길이 '+(c.len/20).toFixed(2)+'cm      거리 '+(c.d/20).toFixed(2)+'cm',38,344,'#1f2937',18);
    lbl(ctx,(t===null)?'수선의 발은 현의 어디일까?':('수선의 발에서 양끝까지 : '+(c.ma/20).toFixed(2)+' / '+(c.mb/20).toFixed(2)+'cm'),
        38,374,'#15803d',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {r:r2(S.r/20),d:r2(c.d/20),len:r2(c.len/20),
            ma:r2(c.ma/20),mb:r2(c.mb/20),
            mid:(Math.abs(c.ma-c.mb)<0.05),
            perp:(Math.abs(c.ang-90)<0.05),
            calc:r2(2*Math.sqrt(S.r*S.r-c.d*c.d)/20)};
  },
  headA:['번호','반지름','거리','현의 길이','왼쪽 반','오른쪽 반','이등분?','수직?'],
  rowA:function(r,i){
    return [i+1,r.r,r.d,'<b>'+r.len+'</b>',r.ma,r.mb,
            '<span class="'+(r.mid?'ok':'no')+'">'+(r.mid?'○':'×')+'</span>',
            '<span class="'+(r.perp?'ok':'no')+'">'+(r.perp?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],mid=0,perp=0,g={},pairs=0,mono=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.mid) mid++;
      if(r.perp) perp++;
      if(!g[r.r]) g[r.r]=[];
      g[r.r].push([r.d,r.len]);
      rows.push([r.r, r.d, '<b>'+r.len+'</b>', r.ma+' / '+r.mb,
                 '<span class="'+(r.mid?'ok':'no')+'">'+(r.mid?'○':'×')+'</span>',
                 '<span class="'+(r.perp?'ok':'no')+'">'+(r.perp?'○':'×')+'</span>']);
    }
    var k,ok=0,tot=0;
    for(k in g){
      var arr=g[k];
      if(arr.length<2) continue;
      arr.sort(function(x,y){return x[0]-y[0];});
      var j,good=true;
      for(j=1;j<arr.length;j++){ if(arr[j][1]>arr[j-1][1]+0.02) good=false; }
      tot++;
      if(good) ok++;
    }
    var stats=[
      {t:'수선의 발이 현을 이등분',big:mid+' / '+rec.length,p:'양쪽 조각의 길이가 같았던 기록 수.'},
      {t:'수선이 현과 수직',big:perp+' / '+rec.length,p:'중심에서 내린 선이 현과 직각을 이루었는지 확인한 결과.'},
      {t:'같은 반지름에서 거리가 멀수록 현이 짧아짐',big:tot?(ok+' / '+tot):'비교 없음',
       p:tot?'반지름을 고정하고 거리만 바꾼 묶음.':'같은 반지름에서 거리만 바꿔 두 번 이상 기록해 보자.'}
    ];
    var concl;
    if(mid===rec.length&&perp===rec.length){
      concl='<b>정리</b> — 중심에서 현에 내린 수선은 언제나 <b>현을 정확히 이등분</b>했다. '
           +'중심에서 양 끝까지의 거리가 반지름으로 같아 이등변삼각형이 되기 때문이다. '
           +'또 같은 원에서 <b>중심에서 멀수록 현이 짧아졌고</b>, 중심을 지날 때(거리 0) 가장 긴 현인 지름이 되었다. '
           +'현의 길이는 (반지름² − 거리²)의 제곱근의 2배로 계산된다.';
    } else {
      concl='<b>확인 필요</b> — 이등분되지 않거나 수직이 아닌 기록이 있다.';
    }
    return {head:['반지름','거리','현의 길이','양쪽 조각','이등분?','수직?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 원 밖의 점에서 그은 접선
# ============================================================
LAB_TAN = BASE + r"""
var CX=180, CY=200;
var LAB = {
  cw:440, ch:400, cvTitle:'접선 실험판',
  action:'접선 두 개 긋기',
  hint0:'원의 반지름과, 원 밖 점 P까지의 거리를 정해 보자.',
  sliders:[
    {id:'r',label:'반지름',min:40,max:110,value:70,color:'#2563eb',fmt:function(v){return (v/20).toFixed(1)+'cm';}},
    {id:'d',label:'중심에서 P까지',min:120,max:240,value:180,color:'#f59e0b',fmt:function(v){return (v/20).toFixed(1)+'cm';}}
  ],
  calc:function(S){
    var d=Math.max(S.d,S.r+20);
    var P=[CX+d,CY];
    var L=Math.sqrt(d*d-S.r*S.r);
    var a=Math.acos(S.r/d);
    var T1=[CX+S.r*Math.cos(a),CY-S.r*Math.sin(a)];
    var T2=[CX+S.r*Math.cos(a),CY+S.r*Math.sin(a)];
    return {P:P,d:d,L:L,T1:T1,T2:T2,
            l1:dist(P,T1),l2:dist(P,T2),
            ang1:angDeg([CX,CY],T1,P),ang2:angDeg([CX,CY],T2,P)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'두 접선의 길이',v:ran?((c.l1/20).toFixed(2)+' / '+(c.l2/20).toFixed(2)+'cm'):'그어 보자'},
            {k:'반지름과 이루는 각',v:ran?(r1(c.ang1)+'° / '+r1(c.ang2)+'°'):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '두 접선의 길이는 '+(c.l1/20).toFixed(2)+'cm와 '+(c.l2/20).toFixed(2)+'cm로 같고, 접점에서 반지름과 '+r1(c.ang1)+'°를 이룬다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    ctx.beginPath();ctx.arc(CX,CY,S.r,0,Math.PI*2);
    ctx.strokeStyle='#94a3b8';ctx.lineWidth=2.5;ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    ctx.beginPath();ctx.arc(c.P[0],c.P[1],7,0,Math.PI*2);
    ctx.fillStyle='#dc2626';ctx.fill();
    lbl(ctx,'P',c.P[0]+10,c.P[1]+5,'#b91c1c',16);
    if(grow>0){
      [c.T1,c.T2].forEach(function(T){
        ctx.strokeStyle='#f59e0b';ctx.lineWidth=3;
        ctx.beginPath();ctx.moveTo(c.P[0],c.P[1]);
        ctx.lineTo(c.P[0]+(T[0]-c.P[0])*grow,c.P[1]+(T[1]-c.P[1])*grow);ctx.stroke();
      });
    }
    if(grow>=1){
      [c.T1,c.T2].forEach(function(T){
        ctx.strokeStyle='#2563eb';ctx.lineWidth=2;
        ctx.beginPath();ctx.moveTo(CX,CY);ctx.lineTo(T[0],T[1]);ctx.stroke();
        ctx.beginPath();ctx.arc(T[0],T[1],5,0,Math.PI*2);ctx.fillStyle='#1d4ed8';ctx.fill();
      });
      lbl(ctx,(c.l1/20).toFixed(2)+'cm',(c.P[0]+c.T1[0])/2,(c.P[1]+c.T1[1])/2-8,'#b45309',14,'center');
      lbl(ctx,(c.l2/20).toFixed(2)+'cm',(c.P[0]+c.T2[0])/2,(c.P[1]+c.T2[1])/2+18,'#b45309',14,'center');
    }
    ctx.beginPath();ctx.arc(CX,CY,5,0,Math.PI*2);ctx.fillStyle='#1f2937';ctx.fill();
    lbl(ctx,'원 밖의 점에서 접선을 두 개 그으면?',24,34,'#1d4ed8',18);
    box(ctx,20,314,400,70);
    lbl(ctx,'두 접선 : '+(c.l1/20).toFixed(2)+'cm , '+(c.l2/20).toFixed(2)+'cm',38,344,'#1f2937',18);
    lbl(ctx,(t===null)?'두 접선의 길이는 같을까?':('접점에서 반지름과 이루는 각 : '+r1(c.ang1)+'°'),38,374,'#15803d',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {r:r2(S.r/20),d:r2(c.d/20),l1:r2(c.l1/20),l2:r2(c.l2/20),
            same:(Math.abs(c.l1-c.l2)<0.05),
            perp:(Math.abs(c.ang1-90)<0.05&&Math.abs(c.ang2-90)<0.05),
            calc:r2(Math.sqrt(c.d*c.d-S.r*S.r)/20),
            pyth:(Math.abs(c.l1-Math.sqrt(c.d*c.d-S.r*S.r))<0.05)};
  },
  headA:['번호','반지름','중심~P','접선 1','접선 2','같은가?','수직?','√(d²−r²)','일치?'],
  rowA:function(r,i){
    return [i+1,r.r,r.d,'<b>'+r.l1+'</b>',r.l2,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            '<span class="'+(r.perp?'ok':'no')+'">'+(r.perp?'○':'×')+'</span>',
            r.calc,
            '<span class="'+(r.pyth?'ok':'no')+'">'+(r.pyth?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,perp=0,pyth=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.perp) perp++;
      if(r.pyth) pyth++;
      rows.push([r.r, r.d, r.l1+' / '+r.l2,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 '<span class="'+(r.perp?'ok':'no')+'">'+(r.perp?'○':'×')+'</span>',
                 r.calc,
                 '<span class="'+(r.pyth?'ok':'no')+'">'+(r.pyth?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'두 접선의 길이가 같았던 횟수',big:same+' / '+rec.length,p:'원 밖 한 점에서 그은 두 접선을 비교한 결과.'},
      {t:'접점에서 반지름과 수직',big:perp+' / '+rec.length,p:'접선과 반지름이 이루는 각을 잰 결과.'},
      {t:'접선 길이 = √(d² − r²)',big:pyth+' / '+rec.length,p:'직각삼각형이므로 피타고라스 정리로 구할 수 있다.'}
    ];
    var concl;
    if(same===rec.length&&perp===rec.length&&pyth===rec.length){
      concl='<b>정리</b> — 원 밖 한 점에서 그은 두 접선의 길이는 <b>언제나 같았고</b>, 접점에서 반지름과 <b>수직</b>이었다. '
           +'그래서 중심·접점·P를 이으면 직각삼각형이 되고, 접선의 길이는 √(d² − r²)로 구할 수 있다. '
           +'두 직각삼각형이 합동이라서 접선 길이가 같아지는 것이다.';
    } else {
      concl='<b>확인 필요</b> — 두 접선의 길이나 수직 조건이 어긋난 기록이 있다.';
    }
    return {head:['반지름','중심~P','두 접선','같은가?','수직?','√(d²−r²)','일치?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 특수각의 삼각비
# ============================================================
LAB_SPEC = BASE + r"""
var ANGS=[15,30,45,60,75];
var LAB = {
  cw:440, ch:420, cvTitle:'삼각비 값 판',
  action:'세 비 구하기',
  hint0:'각을 골라 sin, cos, tan 값을 구해 보자.',
  sliders:[
    {id:'i',label:'각',min:0,max:4,value:2,color:'#2563eb',fmt:function(v){return ANGS[v]+'°';}}
  ],
  calc:function(S){
    var th=ANGS[S.i], rad=th*Math.PI/180;
    var si=Math.sin(rad), co=Math.cos(rad), ta=Math.tan(rad);
    return {th:th,si:si,co:co,ta:ta,
            sum:si*si+co*co,
            coComp:Math.cos((90-th)*Math.PI/180),
            siComp:Math.sin((90-th)*Math.PI/180),
            ratio:si/co};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'sin / cos',v:ran?(r3(c.si)+' / '+r3(c.co)):'구해 보자'},
            {k:'tan',v:ran?r3(c.ta):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return ANGS[S.i]+'°에서 sin '+r3(c.si)+', cos '+r3(c.co)+', tan '+r3(c.ta)+'.  sin²+cos² = '+r3(c.sum)+'이다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var R=170, OX=60, OY=290;
    var rad=c.th*Math.PI/180;
    var P=[OX+R*Math.cos(rad),OY-R*Math.sin(rad)];
    var F=[P[0],OY];
    ctx.beginPath();ctx.moveTo(OX,OY);ctx.lineTo(F[0],F[1]);ctx.lineTo(P[0],P[1]);ctx.closePath();
    ctx.fillStyle='rgba(37,99,235,0.10)';ctx.fill();
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;ctx.stroke();
    ctx.strokeStyle='#dc2626';ctx.lineWidth=4;
    ctx.beginPath();ctx.moveTo(F[0],F[1]);ctx.lineTo(P[0],P[1]);ctx.stroke();
    ctx.strokeStyle='#16a34a';ctx.lineWidth=4;
    ctx.beginPath();ctx.moveTo(OX,OY);ctx.lineTo(F[0],F[1]);ctx.stroke();
    ctx.beginPath();ctx.arc(OX,OY,36,-rad,0);
    ctx.strokeStyle='#1d4ed8';ctx.lineWidth=2;ctx.stroke();
    lbl(ctx,c.th+'°',OX+42,OY-12,'#1d4ed8',16);
    var show=(t===null)?0:Math.min(1,t);
    if(show>=1){
      lbl(ctx,'높이 '+r1(R*c.si),F[0]+8,(F[1]+P[1])/2,'#b91c1c',14);
      lbl(ctx,'밑변 '+r1(R*c.co),(OX+F[0])/2,OY+20,'#15803d',14,'center');
      lbl(ctx,'빗변 '+R,(OX+P[0])/2-30,(OY+P[1])/2-8,'#334155',14);
    }
    lbl(ctx,'빗변을 '+R+'로 고정한 직각삼각형',24,34,'#52627a',16);
    box(ctx,20,308,400,104);
    lbl(ctx,(t===null)?'sin, cos, tan은 얼마일까?':('sin '+r3(c.si)+'    cos '+r3(c.co)+'    tan '+r3(c.ta)),38,340,'#1f2937',19);
    lbl(ctx,(t===null)?'':('sin² + cos² = '+r3(c.sum)),38,372,'#15803d',18);
    lbl(ctx,(t===null)?'':('sin ÷ cos = '+r3(c.ratio)+'    (tan과 비교)'),38,400,'#52627a',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {th:c.th,si:r3(c.si),co:r3(c.co),ta:r3(c.ta),
            sum:r3(c.sum),ratio:r3(c.ratio),
            sumOne:(Math.abs(c.sum-1)<1e-9),
            tanOk:(Math.abs(c.ratio-c.ta)<1e-9),
            coComp:r3(c.coComp),
            compOk:(Math.abs(c.si-c.coComp)<1e-9),
            eq45:(c.th===45)};
  },
  headA:['번호','각','sin','cos','tan','sin²+cos²','1인가?','sin÷cos','tan과 같나?','cos(90°−θ)','sin과 같나?'],
  rowA:function(r,i){
    return [i+1,r.th+'°','<b>'+r.si+'</b>',r.co,r.ta,r.sum,
            '<span class="'+(r.sumOne?'ok':'no')+'">'+(r.sumOne?'○':'×')+'</span>',
            r.ratio,
            '<span class="'+(r.tanOk?'ok':'no')+'">'+(r.tanOk?'○':'×')+'</span>',
            r.coComp,
            '<span class="'+(r.compOk?'ok':'no')+'">'+(r.compOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],one=0,tanOk=0,compOk=0,ths={},tn=0,e45=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.sumOne) one++;
      if(r.tanOk) tanOk++;
      if(r.compOk) compOk++;
      if(!ths[r.th]){ ths[r.th]=true; tn++; }
      if(r.eq45&&Math.abs(r.si-r.co)<1e-9) e45++;
      rows.push([r.th+'°', r.si, r.co, r.ta, r.sum,
                 '<span class="'+(r.sumOne?'ok':'no')+'">'+(r.sumOne?'○':'×')+'</span>',
                 r.coComp,
                 '<span class="'+(r.compOk?'ok':'no')+'">'+(r.compOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'sin² + cos² = 1',big:one+' / '+rec.length,p:'피타고라스 정리를 빗변으로 나눈 결과와 같다.'},
      {t:'sin ÷ cos = tan',big:tanOk+' / '+rec.length,p:'세 비가 서로 독립이 아님을 확인한 결과.'},
      {t:'sin θ = cos(90°−θ)',big:compOk+' / '+rec.length,
       p:'시험한 각 '+tn+'가지'+(e45?', 45°에서는 sin과 cos이 같았다.':'.')}
    ];
    var concl;
    if(tn<3){
      concl='<b>더 해 보자</b> — 여러 각을 기록해야 관계가 우연이 아님을 확인할 수 있다. 30°, 45°, 60°를 모두 기록해 보자.';
    } else if(one===rec.length&&tanOk===rec.length&&compOk===rec.length){
      concl='<b>정리</b> — 어떤 각에서도 <b>sin² + cos² = 1</b>이었고 <b>tan = sin ÷ cos</b>이었다. '
           +'앞의 것은 직각삼각형에 피타고라스 정리를 쓰고 빗변²으로 나눈 것과 같다. '
           +'또 <b>sin θ = cos(90° − θ)</b>였다. 한 각의 sin은 나머지 각의 cos이기 때문이다. '
           +'45°에서는 두 변이 같아 sin과 cos이 일치한다.';
    } else {
      concl='<b>확인 필요</b> — 관계가 어긋난 기록이 있다.';
    }
    return {head:['각','sin','cos','tan','sin²+cos²','1인가?','cos(90−θ)','sin과 같나?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 산점도와 상관관계
# ============================================================
LAB_SCAT = BASE + r"""
var NOISE=[1.2,-0.8,0.5,-1.5,0.9,-0.3,1.4,-1.1,0.2,0.7,-0.9,-0.4];
var LAB = {
  cw:440, ch:430, cvTitle:'산점도판',
  action:'점을 찍어 경향 보기',
  hint0:'두 양 사이의 관계 세기를 정해 보자.',
  sliders:[
    {id:'k',label:'관계의 세기와 방향',min:-10,max:10,value:6,color:'#2563eb',unit:''}
  ],
  pts:function(S){
    var p=[],i;
    for(i=0;i<12;i++){
      var x=i+1;
      var y=6+S.k*(x-6.5)/12+NOISE[i];
      p.push([x,y]);
    }
    return p;
  },
  corr:function(p){
    var n=p.length,i,sx=0,sy=0;
    for(i=0;i<n;i++){ sx+=p[i][0]; sy+=p[i][1]; }
    var mx=sx/n,my=sy/n,num=0,dx=0,dy=0;
    for(i=0;i<n;i++){
      num+=(p[i][0]-mx)*(p[i][1]-my);
      dx+=(p[i][0]-mx)*(p[i][0]-mx);
      dy+=(p[i][1]-my)*(p[i][1]-my);
    }
    return num/Math.sqrt(dx*dy);
  },
  readout:function(S,ran){
    var p=this.pts(S), r=this.corr(p);
    return [{k:'관계 세기 설정',v:S.k},
            {k:'점들의 경향',v:ran?((r>0.2)?'오른쪽 위':((r<-0.2)?'오른쪽 아래':'뚜렷하지 않음')):'찍어 보자'}];
  },
  doneMsg:function(S){
    var p=this.pts(S), r=this.corr(p);
    return '점들이 '+((r>0.2)?'오른쪽 위로 올라간다 — 양의 상관관계':((r<-0.2)?'오른쪽 아래로 내려간다 — 음의 상관관계':'뚜렷한 방향이 없다 — 상관관계가 거의 없다'))+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var p=this.pts(S), i, r=this.corr(p);
    var GX=60, GY=320, GW=340, GH=250;
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+GW,GY);ctx.moveTo(GX,GY);ctx.lineTo(GX,GY-GH);ctx.stroke();
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=1;i<=6;i++){
      ctx.beginPath();ctx.moveTo(GX,GY-GH*i/6);ctx.lineTo(GX+GW,GY-GH*i/6);ctx.stroke();
    }
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*12);
    for(i=0;i<12;i++){
      if(i>=shown) break;
      var x=GX+GW*p[i][0]/13;
      var y=GY-GH*(p[i][1])/13;
      ctx.beginPath();ctx.arc(x,y,7,0,Math.PI*2);
      ctx.fillStyle='#2563eb';ctx.fill();
      ctx.strokeStyle='#fff';ctx.lineWidth=1.6;ctx.stroke();
    }
    lbl(ctx,'가로 = 공부 시간,  세로 = 점수 (예시 자료)',24,32,'#52627a',15);
    if(shown>=12){
      lbl(ctx,(r>0.2)?'↗ 오른쪽 위로':((r<-0.2)?'↘ 오른쪽 아래로':'→ 뚜렷하지 않음'),GX+GW-10,GY-GH+18,
          (r>0.2)?'#15803d':((r<-0.2)?'#b91c1c':'#64748b'),18,'right');
    }
    box(ctx,20,336,400,80);
    lbl(ctx,(t===null)?'점들이 어떤 경향을 보일까?':('경향 : '+((r>0.2)?'양의 상관관계':((r<-0.2)?'음의 상관관계':'상관관계가 거의 없음'))),
        38,368,'#1f2937',19);
    lbl(ctx,(t===null)?'':('설정한 세기 '+S.k+'    경향의 세기 '+r2(r)),38,400,'#52627a',17);
  },
  record:function(S){
    var p=this.pts(S), r=this.corr(p);
    return {k:S.k,r:r2(r),
            dir:(r>0.2)?'양':((r<-0.2)?'음':'거의 없음'),
            setDir:(S.k>2)?'양':((S.k<-2)?'음':'거의 없음'),
            strong:(Math.abs(r)>0.7)};
  },
  headA:['번호','설정 세기','경향의 세기','방향','설정과 같은 방향?','뚜렷한가?'],
  rowA:function(r,i){
    var m=(r.dir===r.setDir);
    return [i+1,r.k,r.r,'<b>'+r.dir+'</b>',
            '<span class="'+(m?'ok':'no')+'">'+(m?'○':'×')+'</span>',
            r.strong?'뚜렷함':'약함'];
  },
  analyze:function(rec){
    var rows=[],pos=0,neg=0,none=0,match=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.dir==='양') pos++; else if(r.dir==='음') neg++; else none++;
      if(r.dir===r.setDir) match++;
      rows.push([r.k, r.r, '<b>'+r.dir+'</b>', r.strong?'뚜렷함':'약함',
                 '<span class="'+((r.dir===r.setDir)?'ok':'no')+'">'+((r.dir===r.setDir)?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'양 / 음 / 거의 없음',big:pos+' / '+neg+' / '+none,
       p:(pos&&neg&&none)?'세 경우를 모두 기록했다.':'세기를 크게, 작게, 0 근처로 모두 해 보자.'},
      {t:'설정한 방향과 경향이 일치',big:match+' / '+rec.length,
       p:'점들의 흩어진 모습만 보고 방향을 읽을 수 있는지 확인한 결과.'},
      {t:'기록 수',big:rec.length+'개',p:'같은 점 개수(12개)로 세기만 바꿨다.'}
    ];
    var concl;
    if(!(pos&&neg&&none)){
      concl='<b>더 해 보자</b> — 세기를 양수·음수·0 근처로 <b>모두</b> 설정해 세 가지 경향을 기록해 보자.';
    } else {
      concl='<b>정리</b> — 점들이 오른쪽 위로 몰리면 <b>양의 상관관계</b>, 오른쪽 아래면 <b>음의 상관관계</b>, '
           +'흩어져 있으면 상관관계가 거의 없다고 한다. 점의 개수는 12개로 늘 같았는데도 경향은 달라졌으니, '
           +'<b>점이 많다고 관계가 강한 것이 아니다.</b> '
           +'또 상관관계가 있다고 해서 한쪽이 다른 쪽의 <b>원인</b>이라는 뜻은 아니다. 두 양이 함께 움직인다는 사실만 말해 준다.';
    }
    return {head:['설정 세기','경향의 세기','방향','뚜렷한가?','일치?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 원 안에서 만나는 두 현
# ============================================================
LAB_POW = BASE + r"""
var CX=220, CY=210, R=140;
function hit(P,th){
  var ux=Math.cos(th), uy=Math.sin(th);
  var ox=P[0]-CX, oy=P[1]-CY;
  var b=ox*ux+oy*uy;
  var cc=ox*ox+oy*oy-R*R;
  var disc=b*b-cc;
  if(disc<0) return null;
  var s=Math.sqrt(disc);
  var t1=-b-s, t2=-b+s;
  return {A:[P[0]+ux*t1,P[1]+uy*t1],B:[P[0]+ux*t2,P[1]+uy*t2],t1:t1,t2:t2};
}
var LAB = {
  cw:440, ch:430, cvTitle:'두 현 실험판',
  action:'두 현 긋고 재기',
  hint0:'원 안의 점 P 위치와 두 현의 방향을 정해 보자.',
  sliders:[
    {id:'px',label:'P의 좌우 위치',min:-90,max:90,value:40,color:'#2563eb',unit:''},
    {id:'py',label:'P의 위아래 위치',min:-90,max:90,value:-30,color:'#60a5fa',unit:''},
    {id:'t1',label:'첫 번째 현의 방향',min:0,max:170,value:20,color:'#dc2626',unit:'°'},
    {id:'t2',label:'두 번째 현의 방향',min:0,max:170,value:110,color:'#f59e0b',unit:'°'}
  ],
  calc:function(S){
    var P=[CX+S.px,CY+S.py];
    var h1=hit(P,S.t1*Math.PI/180), h2=hit(P,S.t2*Math.PI/180);
    var op=Math.sqrt(S.px*S.px+S.py*S.py);
    return {P:P,h1:h1,h2:h2,op:op,
            p1:h1?Math.abs(h1.t1*h1.t2):0,
            p2:h2?Math.abs(h2.t1*h2.t2):0,
            pw:R*R-op*op};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'PA × PB',v:ran?r1(c.p1/400):'재 보자'},
            {k:'PC × PD',v:ran?r1(c.p2/400):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'PA×PB = '+r1(c.p1/400)+', PC×PD = '+r1(c.p2/400)+'.  두 값이 같은지 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    ctx.beginPath();ctx.arc(CX,CY,R,0,Math.PI*2);
    ctx.strokeStyle='#94a3b8';ctx.lineWidth=2.5;ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    function chord(h,col,names){
      if(!h) return;
      ctx.strokeStyle=col;ctx.lineWidth=3;
      ctx.beginPath();ctx.moveTo(h.A[0],h.A[1]);
      ctx.lineTo(h.A[0]+(h.B[0]-h.A[0])*grow,h.A[1]+(h.B[1]-h.A[1])*grow);ctx.stroke();
      if(grow>=1){
        [[h.A,names[0]],[h.B,names[1]]].forEach(function(q){
          ctx.beginPath();ctx.arc(q[0][0],q[0][1],5,0,Math.PI*2);ctx.fillStyle=col;ctx.fill();
          lbl(ctx,q[1],q[0][0]+8,q[0][1]-6,col,14);
        });
      }
    }
    chord(c.h1,'#dc2626',['A','B']);
    chord(c.h2,'#f59e0b',['C','D']);
    ctx.beginPath();ctx.arc(c.P[0],c.P[1],7,0,Math.PI*2);
    ctx.fillStyle='#1f2937';ctx.fill();
    lbl(ctx,'P',c.P[0]+10,c.P[1]-8,'#1f2937',16);
    ctx.beginPath();ctx.arc(CX,CY,4,0,Math.PI*2);ctx.fillStyle='#94a3b8';ctx.fill();
    lbl(ctx,'P를 지나는 두 현',24,32,'#1d4ed8',18);
    box(ctx,20,348,400,72);
    lbl(ctx,(t===null)?'PA×PB 와 PC×PD 는?':('PA × PB = '+r1(c.p1/400)+'      PC × PD = '+r1(c.p2/400)),
        38,378,'#1f2937',18);
    lbl(ctx,(t===null)?'':('반지름² − OP² = '+r1(c.pw/400)),38,408,'#15803d',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {px:S.px,py:S.py,t1:S.t1,t2:S.t2,
            op:r2(c.op/20),
            p1:r1(c.p1/400),p2:r1(c.p2/400),pw:r1(c.pw/400),
            same:(Math.abs(c.p1-c.p2)<0.6),
            powOk:(Math.abs(c.p1-c.pw)<0.6)};
  },
  headA:['번호','P 위치','두 방향','PA×PB','PC×PD','같은가?','반지름²−OP²','일치?'],
  rowA:function(r,i){
    return [i+1,'('+r.px+', '+r.py+')',r.t1+'° / '+r.t2+'°','<b>'+r.p1+'</b>',r.p2,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            r.pw,
            '<span class="'+(r.powOk?'ok':'no')+'">'+(r.powOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,pow=0,g={},pairs=0,agree=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.powOk) pow++;
      var k=r.px+','+r.py, note='첫 기록';
      if(g[k]!==undefined){
        pairs++;
        var s=(Math.abs(g[k]-r.p1)<0.6);
        if(s) agree++;
        note='<span class="'+(s?'ok':'no')+'">'+(s?'같은 값':'다른 값')+'</span>';
      } else { g[k]=r.p1; }
      rows.push(['('+r.px+', '+r.py+')', r.t1+'° / '+r.t2+'°', r.p1+' / '+r.p2,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 r.pw,
                 '<span class="'+(r.powOk?'ok':'no')+'">'+(r.powOk?'○':'×')+'</span>', note]);
    }
    var stats=[
      {t:'PA×PB = PC×PD',big:same+' / '+rec.length,p:'같은 점을 지나는 두 현에서 곱이 같았는지 확인한 결과.'},
      {t:'그 곱 = 반지름² − OP²',big:pow+' / '+rec.length,p:'곱의 값이 P의 위치만으로 정해지는지 확인한 결과.'},
      {t:'같은 P에서 방향만 바꾼 짝',big:pairs+'쌍',
       p:pairs?('그중 값이 같았던 것 '+agree+'쌍.'):'P를 그대로 두고 현의 방향만 바꿔 기록해 보자.'}
    ];
    var concl;
    if(same===rec.length&&pow===rec.length){
      concl='<b>정리</b> — 한 점 P를 지나는 두 현에서 <b>PA × PB 와 PC × PD가 언제나 같았다.</b> '
           +'현을 어느 방향으로 긋든 값이 변하지 않았고, 그 값은 <b>반지름² − OP²</b>로 P의 위치만으로 정해졌다. '
           +'이는 △PAC와 △PDB가 닮음이기 때문이다(같은 호에 대한 원주각이 같고 맞꼭지각이 같다). '
           +'닮음에서 대응변의 비가 같다는 사실이 이 곱셈 관계를 만든다.';
    } else {
      concl='<b>확인 필요</b> — 두 곱이 다른 기록이 있다. P가 원 안에 있는지 확인해 보자.';
    }
    return {head:['P 위치','두 방향','PA×PB / PC×PD','같은가?','반지름²−OP²','일치?','같은 P끼리'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("m3_chord_perpendicular_lab.html",
     "현 실험실 — 중심에서 내린 수선은 현을 어떻게 나눌까?",
     "현 실험실 — 중심에서 내린 수선은 현을 어떻게 나눌까?",
     "중심에서 현까지의 거리를 바꿔 가며 현의 길이와 수선의 발 위치를 기록한다.",
     LAB_CHORD),
    ("m3_tangent_length_lab.html",
     "접선 실험실 — 두 접선의 길이는 같을까?",
     "접선 실험실 — 두 접선의 길이는 같을까?",
     "원 밖 한 점에서 접선 두 개를 긋고 길이와 접점에서의 각을 재어 기록한다.",
     LAB_TAN),
    ("m3_special_angle_trig_lab.html",
     "삼각비 값 실험실 — sin과 cos은 서로 무슨 관계일까?",
     "삼각비 값 실험실 — sin과 cos은 서로 무슨 관계일까?",
     "여러 각에서 sin, cos, tan을 구해 sin²+cos²과 여각 관계를 확인한다.",
     LAB_SPEC),
    ("m3_scatter_correlation_lab.html",
     "산점도 실험실 — 점이 많으면 관계가 강한 걸까?",
     "산점도 실험실 — 점이 많으면 관계가 강한 걸까?",
     "점의 개수는 그대로 두고 관계의 세기만 바꿔 가며 산점도의 경향을 읽고 기록한다.",
     LAB_SCAT),
    ("m3_intersecting_chords_lab.html",
     "두 현 실험실 — 방향을 바꿔도 곱이 같을까?",
     "두 현 실험실 — 방향을 바꿔도 곱이 같을까?",
     "원 안의 한 점을 지나는 두 현을 긋고 PA×PB와 PC×PD를 재어 비교한다.",
     LAB_POW),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c20_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
