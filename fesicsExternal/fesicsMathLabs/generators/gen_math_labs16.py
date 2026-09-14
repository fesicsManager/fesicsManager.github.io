# -*- coding: utf-8 -*-
"""중2 ⑤ 닮음·피타고라스 3종 + ⑥ 경우의 수와 확률 3종"""
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
function gcd(x,y){x=Math.abs(x);y=Math.abs(y);while(y){var t=x%y;x=y;y=t;}return x;}
function dist(p,q){return Math.sqrt((p[0]-q[0])*(p[0]-q[0])+(p[1]-q[1])*(p[1]-q[1]));}
function poly(ctx,p,fill,stroke){
  ctx.beginPath();
  for(var i=0;i<p.length;i++){ if(i===0) ctx.moveTo(p[i][0],p[i][1]); else ctx.lineTo(p[i][0],p[i][1]); }
  ctx.closePath();
  if(fill){ctx.fillStyle=fill;ctx.fill();}
  ctx.strokeStyle=stroke;ctx.lineWidth=3;ctx.stroke();
}
"""

# ============================================================
# 1. 닮음 조건 (SAS)
# ============================================================
LAB_SIM = BASE + r"""
function third(a,b,th){ return Math.sqrt(a*a+b*b-2*a*b*Math.cos(th*Math.PI/180)); }
var LAB = {
  cw:440, ch:420, cvTitle:'닮음 조건 판',
  action:'세 번째 변 재기',
  hint0:'두 변의 길이와 낀각을 정해 보자. ②는 ①의 두 변을 2배로 한 삼각형이다.',
  sliders:[
    {id:'a',label:'① 첫 번째 변',min:2,max:9,value:4,color:'#2563eb',unit:'cm'},
    {id:'b',label:'① 두 번째 변',min:2,max:9,value:6,color:'#60a5fa',unit:'cm'},
    {id:'t1',label:'① 낀각',min:20,max:160,value:60,color:'#16a34a',unit:'°'},
    {id:'t2',label:'② 낀각',min:20,max:160,value:100,color:'#dc2626',unit:'°'}
  ],
  calc:function(S){
    var c1=third(S.a,S.b,S.t1);
    var c2=third(2*S.a,2*S.b,S.t2);
    return {c1:c1,c2:c2,ratio:c2/c1,sim:(Math.abs(c2/c1-2)<1e-6)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'세 번째 변',v:ran?(r2(c.c1)+' / '+r2(c.c2)):'재 보자'},
            {k:'세 번째 변의 비',v:ran?r2(c.ratio):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '세 번째 변의 비는 '+r2(c.ratio)+'다. 두 변의 비 2와 '+(c.sim?'같으므로 닮음이다':'다르므로 닮음이 아니다')+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var U=Math.min(18, 150/Math.max(S.a,S.b));
    function tri(ox,oy,a,b,th,col,scale){
      var A=[ox,oy];
      var B=[ox+a*scale,oy];
      var rad=th*Math.PI/180;
      var C=[ox+b*scale*Math.cos(rad), oy-b*scale*Math.sin(rad)];
      poly(ctx,[A,B,C],'rgba(37,99,235,0.10)',col);
      return {A:A,B:B,C:C};
    }
    var t1=tri(50,180,S.a,S.b,S.t1,'#2563eb',U);
    var t2=tri(240,320,S.a,S.b,S.t2,'#dc2626',U);
    var show=(t===null)?0:Math.min(1,t);
    lbl(ctx,'① 두 변 '+S.a+', '+S.b+' 낀각 '+S.t1+'°',24,34,'#1d4ed8',17);
    lbl(ctx,'② 두 변 '+(2*S.a)+', '+(2*S.b)+' 낀각 '+S.t2+'°',240,214,'#b91c1c',17);
    if(show>0){
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=4;
      ctx.beginPath();ctx.moveTo(t1.B[0],t1.B[1]);ctx.lineTo(t1.C[0],t1.C[1]);ctx.stroke();
      ctx.beginPath();ctx.moveTo(t2.B[0],t2.B[1]);ctx.lineTo(t2.C[0],t2.C[1]);ctx.stroke();
      lbl(ctx,r2(c.c1),(t1.B[0]+t1.C[0])/2+6,(t1.B[1]+t1.C[1])/2,'#b45309',14);
      lbl(ctx,r2(c.c2),(t2.B[0]+t2.C[0])/2+6,(t2.B[1]+t2.C[1])/2,'#b45309',14);
    }
    box(ctx,20,336,400,74);
    lbl(ctx,'두 변의 비 : 2 : 1',38,366,'#52627a',18);
    lbl(ctx,(t===null)?'세 번째 변의 비도 2일까?':('세 번째 변의 비 : '+r2(c.ratio)+'  →  '+(c.sim?'닮음':'닮음 아님')),
        38,396,c.sim?'#15803d':'#b91c1c',19);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,t1:S.t1,t2:S.t2,c1:r2(c.c1),c2:r2(c.c2),ratio:r2(c.ratio),
            sim:c.sim,sameAng:(S.t1===S.t2)};
  },
  headA:['번호','① 두 변','① 낀각','② 낀각','① 세 번째 변','② 세 번째 변','세 번째 변의 비','닮음?'],
  rowA:function(r,i){
    return [i+1,r.a+', '+r.b,r.t1+'°',r.t2+'°',r.c1,r.c2,'<b>'+r.ratio+'</b>',
            '<span class="'+(r.sim?'ok':'no')+'">'+(r.sim?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],eq=0,eqSim=0,ne=0,neSim=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.sameAng){ eq++; if(r.sim) eqSim++; }
      else { ne++; if(r.sim) neSim++; }
      rows.push([r.a+', '+r.b, r.t1+'° / '+r.t2+'°',
                 r.sameAng?'같음':'다름', r.c1+' / '+r.c2, '<b>'+r.ratio+'</b>',
                 '<span class="'+(r.sim?'ok':'no')+'">'+(r.sim?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'낀각이 같았던 기록',big:eq+'개',
       p:eq?('그중 닮음이었던 것 '+eqSim+'개.'):'두 낀각을 같게 맞춰 보자.'},
      {t:'낀각이 달랐던 기록',big:ne+'개',
       p:ne?('그중 닮음이었던 것 '+neSim+'개.'):'두 낀각을 다르게도 해 보자.'},
      {t:'두 변의 비',big:'항상 2 : 1',p:'두 변만 비례해도 닮음이라고 할 수 있는지 확인했다.'}
    ];
    var concl;
    if(eq===0||ne===0){
      concl='<b>더 해 보자</b> — 낀각이 같은 경우와 다른 경우를 <b>모두</b> 기록해야 조건이 드러난다.';
    } else if(eqSim===eq && neSim===0){
      concl='<b>정리</b> — 두 변의 비가 항상 2:1이었는데도, 낀각이 다르면 세 번째 변의 비가 2가 아니어서 <b>닮음이 아니었다</b>('+ne+'번 모두). '
           +'두 변의 비만으로는 부족하고 <b>끼인각까지 같아야</b> 닮음이다(SAS 닮음). '
           +'각이 다르면 삼각형의 모양 자체가 달라진다.';
    } else {
      concl='<b>확인 필요</b> — 규칙과 어긋난 기록이 있다.';
    }
    return {head:['① 두 변','두 낀각','낀각 같음','세 번째 변','비','닮음?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 피타고라스 정리
# ============================================================
LAB_PYTH = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'피타고라스 판',
  action:'세 정사각형 넓이 재기',
  hint0:'두 변의 길이와 그 사이 각을 정해 보자.',
  sliders:[
    {id:'a',label:'변 a',min:2,max:9,value:3,color:'#2563eb',unit:''},
    {id:'b',label:'변 b',min:2,max:9,value:4,color:'#16a34a',unit:''},
    {id:'th',label:'두 변 사이 각',min:30,max:150,value:90,color:'#f59e0b',unit:'°'}
  ],
  calc:function(S){
    var c2=S.a*S.a+S.b*S.b-2*S.a*S.b*Math.cos(S.th*Math.PI/180);
    return {c:Math.sqrt(c2),c2:c2,sum:S.a*S.a+S.b*S.b,
            eq:(Math.abs(c2-(S.a*S.a+S.b*S.b))<1e-6)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'a² + b²',v:c.sum},
            {k:'c²',v:ran?r2(c.c2):'재 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'a²+b² = '+c.sum+', c² = '+r2(c.c2)+'.  '+(c.eq?'두 값이 같다 — 직각삼각형이다.':(c.c2<c.sum?'c²이 더 작다 (예각).':'c²이 더 크다 (둔각).'))+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var U=Math.min(15, 110/Math.max(S.a,S.b,c.c));
    var A=[170,250];
    var B=[170+S.a*U,250];
    var rad=S.th*Math.PI/180;
    var C=[170+S.b*U*Math.cos(rad),250-S.b*U*Math.sin(rad)];
    poly(ctx,[A,B,C],'rgba(148,163,184,0.18)','#334155');
    var show=(t===null)?0:Math.min(1,t);
    function sq(P,Q,col,label,alpha){
      var dx=Q[0]-P[0], dy=Q[1]-P[1];
      var p3=[Q[0]-dy,Q[1]+dx], p4=[P[0]-dy,P[1]+dx];
      ctx.globalAlpha=alpha;
      poly(ctx,[P,Q,p3,p4],col,'#64748b');
      ctx.globalAlpha=1;
      if(alpha>0.9){
        ctx.fillStyle='#334155';ctx.font='bold 14px sans-serif';ctx.textAlign='center';
        ctx.fillText(label,(P[0]+p3[0])/2,(P[1]+p3[1])/2+4);
        ctx.textAlign='left';
      }
    }
    if(show>0){
      sq(B,A,'rgba(37,99,235,0.30)','a² = '+(S.a*S.a),Math.min(1,show*3));
      sq(A,C,'rgba(22,163,74,0.30)','b² = '+(S.b*S.b),Math.min(1,Math.max(0,show*3-1)));
      sq(C,B,'rgba(245,158,11,0.35)','c² = '+r2(c.c2),Math.min(1,Math.max(0,show*3-2)));
    }
    lbl(ctx,'a = '+S.a+',  b = '+S.b+',  사이 각 '+S.th+'°',24,32,'#1d4ed8',18);
    box(ctx,20,346,400,72);
    lbl(ctx,'a² + b² = '+(S.a*S.a)+' + '+(S.b*S.b)+' = '+c.sum,38,376,'#1f2937',19);
    lbl(ctx,(t===null)?'c²은 얼마일까?':('c² = '+r2(c.c2)+'   →   '+(c.eq?'같다':(c.c2<c.sum?'a²+b² 보다 작다':'a²+b² 보다 크다'))),
        38,404,c.eq?'#15803d':'#b91c1c',19);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,th:S.th,sum:c.sum,c2:r2(c.c2),cc:r2(c.c),
            eq:c.eq,right:(S.th===90),
            cmp:c.eq?'=':(c.c2<c.sum?'<':'>')};
  },
  headA:['번호','a, b','사이 각','a² + b²','c²','비교','직각?','같은가?'],
  rowA:function(r,i){
    return [i+1,r.a+', '+r.b,r.th+'°',r.sum,'<b>'+r.c2+'</b>','a²+b² '+r.cmp.replace('<','>').replace('>','<')+' c²',
            r.right?'○':'×',
            '<span class="'+(r.eq?'ok':'no')+'">'+(r.eq?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],eq=0,rt=0,rtEq=0,acute=0,acuteLt=0,obt=0,obtGt=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.eq) eq++;
      if(r.right){ rt++; if(r.eq) rtEq++; }
      else if(r.th<90){ acute++; if(r.cmp==='<') acuteLt++; }
      else { obt++; if(r.cmp==='>') obtGt++; }
      rows.push([r.a+', '+r.b, r.th+'°', r.sum, '<b>'+r.c2+'</b>',
                 (r.cmp==='=')?'a²+b² = c²':((r.cmp==='<')?'a²+b² > c²':'a²+b² < c²'),
                 '<span class="'+(r.eq?'ok':'no')+'">'+(r.eq?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'a² + b² = c² 였던 횟수',big:eq+' / '+rec.length,
       p:'세 정사각형의 넓이 관계가 성립한 기록 수.'},
      {t:'사이 각이 90°였던 기록',big:rt+'개',
       p:rt?('그중 등식이 성립한 것 '+rtEq+'개.'):'사이 각을 90°로 맞춰 보자.'},
      {t:'예각 / 둔각이었던 기록',big:acute+'개 / '+obt+'개',
       p:'예각에서 c²이 더 작았던 횟수 '+acuteLt+', 둔각에서 더 컸던 횟수 '+obtGt+'.'}
    ];
    var concl;
    if(rt===0||(acute===0&&obt===0)){
      concl='<b>더 해 보자</b> — 사이 각을 90°인 경우와 아닌 경우를 <b>모두</b> 기록해야 조건이 드러난다.';
    } else if(rtEq===rt && eq===rt){
      concl='<b>정리</b> — a² + b² = c²이 성립한 것은 <b>사이 각이 정확히 90°일 때뿐</b>이었다. '
           +'각이 90°보다 작으면 c²이 더 작아지고('+acuteLt+'번), 크면 더 커졌다('+obtGt+'번). '
           +'피타고라스 정리는 모든 삼각형이 아니라 <b>직각삼각형에서만</b> 성립한다. 그리고 c는 반드시 직각의 맞은편 변(빗변)이다.';
    } else {
      concl='<b>확인 필요</b> — 직각이 아닌데 등식이 성립한 기록이 있다.';
    }
    return {head:['a, b','사이 각','a²+b²','c²','비교','같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 평행선과 선분의 비
# ============================================================
LAB_SEG = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'삼각형 평행선 판',
  action:'평행선 긋고 재기',
  hint0:'삼각형 모양과 평행선의 위치를 정해 보자.',
  sliders:[
    {id:'ax',label:'꼭짓점 A의 좌우',min:60,max:380,value:150,color:'#2563eb',unit:''},
    {id:'ay',label:'꼭짓점 A의 높이',min:50,max:150,value:70,color:'#16a34a',unit:''},
    {id:'tt',label:'평행선의 위치',min:1,max:9,value:4,color:'#f59e0b',
     fmt:function(v){return 'A에서 '+(v*10)+'%';}}
  ],
  calc:function(S){
    var A=[S.ax,S.ay], B=[70,340], C=[380,340];
    var k=S.tt/10;
    var D=[A[0]+(B[0]-A[0])*k, A[1]+(B[1]-A[1])*k];
    var E=[A[0]+(C[0]-A[0])*k, A[1]+(C[1]-A[1])*k];
    var AB=dist(A,B), AC=dist(A,C), BC=dist(B,C);
    var AD=dist(A,D), AE=dist(A,E), DE=dist(D,E);
    return {A:A,B:B,C:C,D:D,E:E,AB:AB,AC:AC,BC:BC,AD:AD,AE:AE,DE:DE,
            DB:AB-AD, EC:AC-AE};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'AD : AB',v:ran?r3(c.AD/c.AB):'재 보자'},
            {k:'DE : BC',v:ran?r3(c.DE/c.BC):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'AD:AB = '+r3(c.AD/c.AB)+', DE:BC = '+r3(c.DE/c.BC)+', AD:DB = '+r3(c.AD/c.DB)+'.  어느 것이 서로 같은지 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    poly(ctx,[c.A,c.B,c.C],'rgba(37,99,235,0.08)','#334155');
    var show=(t===null)?0:Math.min(1,t);
    if(show>0){
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=4;
      ctx.beginPath();ctx.moveTo(c.D[0],c.D[1]);
      ctx.lineTo(c.D[0]+(c.E[0]-c.D[0])*show,c.D[1]+(c.E[1]-c.D[1])*show);ctx.stroke();
      [[c.D,'D'],[c.E,'E']].forEach(function(q){
        ctx.beginPath();ctx.arc(q[0][0],q[0][1],5,0,Math.PI*2);ctx.fillStyle='#b45309';ctx.fill();
        lbl(ctx,q[1],q[0][0]-14,q[0][1]-8,'#b45309',15);
      });
    }
    lbl(ctx,'A',c.A[0]-6,c.A[1]-10,'#1d4ed8',16);
    lbl(ctx,'B',c.B[0]-18,c.B[1]+6,'#334155',16);
    lbl(ctx,'C',c.C[0]+8,c.C[1]+6,'#334155',16);
    lbl(ctx,'DE는 BC와 평행하게 그었다',24,32,'#52627a',16);
    box(ctx,20,352,400,64);
    lbl(ctx,(t===null)?'어떤 비가 서로 같을까?':
        ('AD:AB = '+r3(c.AD/c.AB)+'    DE:BC = '+r3(c.DE/c.BC)+'    AD:DB = '+r3(c.AD/c.DB)),
        38,382,'#1f2937',16);
    lbl(ctx,(t===null)?'':('AE:AC = '+r3(c.AE/c.AC)+'    AE:EC = '+r3(c.AE/c.EC)),38,406,'#52627a',15);
  },
  record:function(S){
    var c=this.calc(S);
    return {tt:S.tt,
            adab:r3(c.AD/c.AB),aeac:r3(c.AE/c.AC),debc:r3(c.DE/c.BC),
            addb:r3(c.AD/c.DB),aeec:r3(c.AE/c.EC),
            m1:(Math.abs(c.AD/c.AB-c.DE/c.BC)<0.002),
            m2:(Math.abs(c.AD/c.DB-c.AE/c.EC)<0.002),
            m3:(Math.abs(c.AD/c.DB-c.DE/c.BC)<0.002)};
  },
  headA:['번호','위치','AD:AB','AE:AC','DE:BC','AD:AB = DE:BC?','AD:DB','AE:EC','AD:DB = AE:EC?'],
  rowA:function(r,i){
    return [i+1,(r.tt*10)+'%',r.adab,r.aeac,'<b>'+r.debc+'</b>',
            '<span class="'+(r.m1?'ok':'no')+'">'+(r.m1?'○':'×')+'</span>',
            r.addb,r.aeec,
            '<span class="'+(r.m2?'ok':'no')+'">'+(r.m2?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],m1=0,m2=0,m3=0,half=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.m1) m1++;
      if(r.m2) m2++;
      if(r.m3){ m3++; if(r.tt===5) half++; }
      rows.push([(r.tt*10)+'%', r.adab, r.debc,
                 '<span class="'+(r.m1?'ok':'no')+'">'+(r.m1?'○':'×')+'</span>',
                 r.addb, r.aeec,
                 '<span class="'+(r.m2?'ok':'no')+'">'+(r.m2?'○':'×')+'</span>',
                 '<span class="'+(r.m3?'ok':'no')+'">'+(r.m3?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'AD:AB = DE:BC',big:m1+' / '+rec.length,
       p:'꼭짓점에서부터 잰 비와 밑변에 대한 비가 같았는지 확인한 결과.'},
      {t:'AD:DB = AE:EC',big:m2+' / '+rec.length,
       p:'평행선이 두 변을 같은 비로 나누는지 확인한 결과.'},
      {t:'AD:DB = DE:BC 였던 횟수',big:m3+' / '+rec.length,
       p:m3?('그중 위치가 50%였던 것 '+half+'개. 한가운데일 때만 우연히 같아진다.'):'두 비는 서로 다른 값이다.'}
    ];
    var concl;
    if(m1===rec.length && m2===rec.length){
      concl='<b>정리</b> — DE ∥ BC일 때 <b>AD:AB = AE:AC = DE:BC</b>가 언제나 성립했고, <b>AD:DB = AE:EC</b>도 항상 성립했다. '
           +'하지만 <b>AD:DB와 DE:BC는 서로 다른 비</b>다'
           +(m3?('(한가운데인 50%일 때만 우연히 같았다)'):'')+'. '
           +'DE:BC를 구할 때는 <b>전체 변(AB)에 대한 비</b>를 써야 한다. 나눠진 조각끼리의 비를 그대로 쓰면 틀린다.';
    } else {
      concl='<b>확인 필요</b> — 비가 어긋난 기록이 있다.';
    }
    return {head:['위치','AD:AB','DE:BC','같은가?','AD:DB','AE:EC','같은가?','AD:DB = DE:BC?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 경우의 수 — 합의 법칙과 곱의 법칙
# ============================================================
LAB_COUNT = BASE + r"""
var MODES=['A 또는 B 하나 고르기','A 하나 고르고 B 하나 고르기'];
var LAB = {
  cw:440, ch:420, cvTitle:'경우의 수 판',
  action:'모두 세어 보기',
  hint0:'두 묶음의 개수와 상황을 정해 보자.',
  sliders:[
    {id:'mode',label:'상황',min:0,max:1,value:1,color:'#2563eb',fmt:function(v){return MODES[v];}},
    {id:'m',label:'A의 가짓수',min:1,max:8,value:3,color:'#16a34a',unit:'가지'},
    {id:'n',label:'B의 가짓수',min:1,max:8,value:4,color:'#f59e0b',unit:'가지'}
  ],
  calc:function(S){
    var cnt=0,i,j;
    if(S.mode===0){
      for(i=0;i<S.m;i++) cnt++;
      for(j=0;j<S.n;j++) cnt++;
    } else {
      for(i=0;i<S.m;i++){ for(j=0;j<S.n;j++){ cnt++; } }
    }
    return {cnt:cnt,sum:S.m+S.n,prod:S.m*S.n};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'상황',v:MODES[S.mode]},
            {k:'세어 본 경우의 수',v:ran?c.cnt:'세어 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '하나씩 세어 보니 '+c.cnt+'가지다. m+n = '+c.sum+', m×n = '+c.prod+'와 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i, j;
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*c.cnt);
    lbl(ctx,MODES[S.mode],24,34,'#1d4ed8',18);
    if(S.mode===0){
      lbl(ctx,'A ('+S.m+'가지)',50,80,'#15803d',17);
      lbl(ctx,'B ('+S.n+'가지)',250,80,'#b45309',17);
      for(i=0;i<S.m;i++){
        var on=(i<shown);
        ctx.fillStyle=on?'#bbf7d0':'#eef2f7';
        ctx.fillRect(50,96+i*30,120,24);
        ctx.strokeStyle=on?'#16a34a':'#cbd5e1';ctx.lineWidth=2;ctx.strokeRect(50,96+i*30,120,24);
        ctx.fillStyle=on?'#14532d':'#cbd5e1';ctx.font='bold 14px sans-serif';ctx.textAlign='center';
        ctx.fillText('A'+(i+1),110,113+i*30);
      }
      for(j=0;j<S.n;j++){
        var on2=((S.m+j)<shown);
        ctx.fillStyle=on2?'#fed7aa':'#eef2f7';
        ctx.fillRect(250,96+j*30,120,24);
        ctx.strokeStyle=on2?'#f59e0b':'#cbd5e1';ctx.lineWidth=2;ctx.strokeRect(250,96+j*30,120,24);
        ctx.fillStyle=on2?'#7c2d12':'#cbd5e1';ctx.font='bold 14px sans-serif';ctx.textAlign='center';
        ctx.fillText('B'+(j+1),310,113+j*30);
      }
      ctx.textAlign='left';
    } else {
      var cw2=Math.min(44,340/S.n), chh=Math.min(30,190/S.m);
      for(i=0;i<S.m;i++){
        for(j=0;j<S.n;j++){
          var idx=i*S.n+j, on3=(idx<shown);
          var x=70+j*cw2, y=90+i*chh;
          ctx.fillStyle=on3?'#dbeafe':'#f4f6fa';
          ctx.fillRect(x,y,cw2-2,chh-2);
          ctx.strokeStyle=on3?'#2563eb':'#e2e8f0';ctx.lineWidth=1.4;ctx.strokeRect(x,y,cw2-2,chh-2);
          if(on3&&S.m*S.n<=42){
            ctx.fillStyle='#1d4ed8';ctx.font='11px sans-serif';ctx.textAlign='center';
            ctx.fillText('A'+(i+1)+'B'+(j+1),x+cw2/2-1,y+chh/2+3);
          }
        }
      }
      ctx.textAlign='left';
      lbl(ctx,'A '+S.m+'가지 × B '+S.n+'가지',70,78,'#1d4ed8',16);
    }
    box(ctx,20,320,400,88);
    lbl(ctx,(t===null)?'몇 가지일까?':('세어 본 경우의 수 : '+c.cnt+'가지'),38,352,'#1f2937',21);
    lbl(ctx,'m + n = '+c.sum+'      m × n = '+c.prod,38,384,'#52627a',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {mode:S.mode,name:MODES[S.mode],m:S.m,n:S.n,cnt:c.cnt,sum:c.sum,prod:c.prod,
            isSum:(c.cnt===c.sum),isProd:(c.cnt===c.prod)};
  },
  headA:['번호','상황','A','B','세어 본 수','m+n','맞나?','m×n','맞나?'],
  rowA:function(r,i){
    return [i+1,r.name,r.m,r.n,'<b>'+r.cnt+'</b>',r.sum,
            '<span class="'+(r.isSum?'ok':'no')+'">'+(r.isSum?'○':'×')+'</span>',
            r.prod,
            '<span class="'+(r.isProd?'ok':'no')+'">'+(r.isProd?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],or0=0,or0Sum=0,and1=0,and1Prod=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.mode===0){ or0++; if(r.isSum) or0Sum++; }
      else { and1++; if(r.isProd) and1Prod++; }
      rows.push([r.name, r.m+' , '+r.n, '<b>'+r.cnt+'</b>', r.sum,
                 '<span class="'+(r.isSum?'ok':'no')+'">'+(r.isSum?'○':'×')+'</span>',
                 r.prod,
                 '<span class="'+(r.isProd?'ok':'no')+'">'+(r.isProd?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'“또는” 상황에서 m+n이 맞은 횟수',big:or0?(or0Sum+' / '+or0):'기록 없음',
       p:or0?'하나만 고르는 상황의 기록.':'“또는” 상황도 기록해 보자.'},
      {t:'“그리고” 상황에서 m×n이 맞은 횟수',big:and1?(and1Prod+' / '+and1):'기록 없음',
       p:and1?'둘 다 고르는 상황의 기록.':'“그리고” 상황도 기록해 보자.'},
      {t:'전체 기록',big:rec.length+'개',p:'상황에 따라 더할지 곱할지가 갈린다.'}
    ];
    var concl;
    if(or0===0||and1===0){
      concl='<b>더 해 보자</b> — “또는” 상황과 “그리고” 상황을 <b>모두</b> 기록해야 두 법칙을 구별할 수 있다.';
    } else if(or0Sum===or0&&and1Prod===and1){
      concl='<b>정리</b> — 둘 중 <b>하나만 고르는</b> 상황에서는 경우의 수가 m + n이었고, '
           +'<b>둘 다 고르는</b> 상황에서는 m × n이었다. '
           +'세어 본 결과가 그대로 말해 준다. “또는”이면 더하고 “그리고”면 곱한다. '
           +'문제에서 두 일이 동시에 일어나는지 아닌지를 먼저 읽어야 한다.';
    } else {
      concl='<b>확인 필요</b> — 세어 본 수와 계산이 어긋난 기록이 있다.';
    }
    return {head:['상황','A, B','세어 본 수','m+n','맞나?','m×n','맞나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 확률의 합과 여사건
# ============================================================
LAB_PROB = BASE + r"""
var NAMES=['빨강','파랑','노랑'], COLS=['#ef4444','#3b82f6','#eab308'];
var LAB = {
  cw:440, ch:400, cvTitle:'확률 주머니판',
  action:'확률 구하기',
  hint0:'주머니에 넣을 색깔별 구슬 수를 정해 보자.',
  sliders:[
    {id:'r',label:'빨강',min:0,max:12,value:3,color:'#ef4444',unit:'개'},
    {id:'b',label:'파랑',min:0,max:12,value:5,color:'#3b82f6',unit:'개'},
    {id:'y',label:'노랑',min:0,max:12,value:4,color:'#eab308',unit:'개'}
  ],
  calc:function(S){
    var tot=S.r+S.b+S.y;
    if(tot===0) return null;
    return {tot:tot,p:[S.r/tot,S.b/tot,S.y/tot],
            sum:(S.r+S.b+S.y)/tot,
            notR:(S.b+S.y)/tot, oneMinus:1-S.r/tot};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    if(!c) return [{k:'주머니',v:'비어 있음'},{k:'',v:'구슬을 넣자'}];
    return [{k:'세 확률의 합',v:ran?r3(c.sum):'구해 보자'},
            {k:'빨강이 아닐 확률',v:ran?r3(c.notR):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(!c) return '주머니가 비어 있다. 구슬을 넣어 보자.';
    return '세 확률의 합은 '+r3(c.sum)+'.  빨강이 아닐 확률은 '+r3(c.notR)+'이고 1 − P(빨강) = '+r3(c.oneMinus)+'이다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    if(!c){ lbl(ctx,'주머니가 비어 있다',24,200,'#b91c1c',20); return; }
    var v=[S.r,S.b,S.y];
    var idx=0;
    for(i=0;i<3;i++){
      var j;
      for(j=0;j<v[i];j++){
        var x=50+(idx%9)*38, y=80+Math.floor(idx/9)*38;
        ctx.beginPath();ctx.arc(x,y,14,0,Math.PI*2);
        ctx.fillStyle=COLS[i];ctx.fill();
        ctx.strokeStyle='#1f2937';ctx.lineWidth=1.6;ctx.stroke();
        idx++;
      }
    }
    var grow=(t===null)?0:Math.min(1,t);
    var BX=40,BW=360,BY=232,ax=0;
    for(i=0;i<3;i++){
      var w=BW*c.p[i]*grow;
      ctx.fillStyle=COLS[i];ctx.fillRect(BX+ax,BY,w,32);
      ax+=w;
    }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;ctx.strokeRect(BX,BY,BW,32);
    if(grow>=1){
      for(i=0;i<3;i++){ lbl(ctx,NAMES[i]+' '+r3(c.p[i]),BX+i*126,BY+52,COLS[i],15); }
    }
    lbl(ctx,'전체 '+c.tot+'개에서 하나 꺼내기',24,36,'#1d4ed8',18);
    box(ctx,20,290,400,94);
    lbl(ctx,(t===null)?'세 확률을 모두 더하면?':('세 확률의 합 : '+r3(c.sum)),38,322,'#1f2937',20);
    lbl(ctx,(t===null)?'':('빨강이 아닐 확률 : '+r3(c.notR)+'      1 − P(빨강) = '+r3(c.oneMinus)),38,354,'#15803d',17);
    lbl(ctx,(t===null)?'':'막대 전체 길이 = 1',38,378,'#52627a',15);
  },
  record:function(S){
    var c=this.calc(S);
    if(!c) return {empty:true};
    return {r:S.r,b:S.b,y:S.y,tot:c.tot,
            pr:r3(c.p[0]),pb:r3(c.p[1]),py:r3(c.p[2]),
            sum:r3(c.sum),notR:r3(c.notR),oneMinus:r3(c.oneMinus),
            sumOne:(Math.abs(c.sum-1)<1e-9),
            compOk:(Math.abs(c.notR-c.oneMinus)<1e-9),
            zero:(S.r===0)};
  },
  headA:['번호','구슬','P(빨강)','P(파랑)','P(노랑)','합','합이 1?','빨강 아님','1−P(빨강)','같은가?'],
  rowA:function(r,i){
    if(r.empty) return [i+1,'빈 주머니','-','-','-','-','-','-','-','-'];
    return [i+1,r.r+'/'+r.b+'/'+r.y,r.pr,r.pb,r.py,'<b>'+r.sum+'</b>',
            '<span class="'+(r.sumOne?'ok':'no')+'">'+(r.sumOne?'○':'×')+'</span>',
            r.notR,r.oneMinus,
            '<span class="'+(r.compOk?'ok':'no')+'">'+(r.compOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],one=0,comp=0,zero=0,valid=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.empty){ rows.push(['빈 주머니','-','-','-','-']); continue; }
      valid++;
      if(r.sumOne) one++;
      if(r.compOk) comp++;
      if(r.zero) zero++;
      rows.push([r.r+'/'+r.b+'/'+r.y, r.pr+' / '+r.pb+' / '+r.py, '<b>'+r.sum+'</b>',
                 '<span class="'+(r.sumOne?'ok':'no')+'">'+(r.sumOne?'○':'×')+'</span>',
                 r.notR+' vs '+r.oneMinus,
                 '<span class="'+(r.compOk?'ok':'no')+'">'+(r.compOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'모든 확률의 합 = 1',big:one+' / '+valid,
       p:'어떤 경우가 일어날 확률을 모두 더하면 반드시 1이다.'},
      {t:'“빨강이 아닐 확률” = 1 − P(빨강)',big:comp+' / '+valid,
       p:'여사건의 확률을 두 방법으로 구해 비교한 결과.'},
      {t:'빨강이 0개였던 기록',big:zero+'개',
       p:zero?'확률이 0인 경우도 확인했다.':'한 색을 0개로 두어 확률 0도 만들어 보자.'}
    ];
    var concl;
    if(valid===0){
      concl='<b>더 해 보자</b> — 구슬을 넣어야 확률을 구할 수 있다.';
    } else if(one===valid&&comp===valid){
      concl='<b>정리</b> — 세 확률의 합은 언제나 <b>1</b>이었고, “빨강이 아닐 확률”은 직접 세어 구한 값과 '
           +'<b>1 − P(빨강)</b>이 언제나 같았다. 어떤 사건이 일어나거나 일어나지 않거나 둘 중 하나뿐이기 때문이다. '
           +'복잡한 사건은 여사건을 구해 1에서 빼는 편이 빠를 때가 많다.';
    } else {
      concl='<b>확인 필요</b> — 합이 1이 아니거나 여사건이 어긋난 기록이 있다.';
    }
    return {head:['구슬','각 확률','합','1인가?','여사건 비교','같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 6. 주사위 두 개의 합
# ============================================================
LAB_DICE = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'주사위 두 개 표',
  action:'해당하는 칸 세기',
  hint0:'두 주사위 눈의 합을 정하고, 그 합이 되는 경우를 세어 보자.',
  sliders:[
    {id:'s',label:'두 눈의 합',min:2,max:12,value:7,color:'#2563eb',unit:''}
  ],
  calc:function(S){
    var cnt=0,i,j;
    for(i=1;i<=6;i++){ for(j=1;j<=6;j++){ if(i+j===S.s) cnt++; } }
    var g=gcd(cnt,36)||1;
    return {cnt:cnt,num:cnt/g,den:36/g,p:cnt/36};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'합이 '+S.s+'인 경우',v:ran?(c.cnt+'가지'):'세어 보자'},
            {k:'확률',v:ran?(c.num+'/'+c.den):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '합이 '+S.s+'인 경우는 '+c.cnt+'가지, 확률은 '+c.num+'/'+c.den+'이다. 1/11과 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i, j;
    var CS=44, X0=76, Y0=76;
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*36);
    ctx.font='bold 14px sans-serif';ctx.textAlign='center';
    for(i=1;i<=6;i++){
      ctx.fillStyle='#475569';
      ctx.fillText(i,X0+(i-1)*CS+CS/2,Y0-10);
      ctx.fillText(i,X0-16,Y0+(i-1)*CS+CS/2+5);
    }
    for(i=1;i<=6;i++){
      for(j=1;j<=6;j++){
        var idx=(i-1)*6+(j-1);
        var on=(idx<shown);
        var hit=(i+j===S.s);
        var x=X0+(j-1)*CS, y=Y0+(i-1)*CS;
        ctx.fillStyle=on?(hit?'#fbbf24':'#f1f5f9'):'#fafbfd';
        ctx.fillRect(x,y,CS-2,CS-2);
        ctx.strokeStyle=on&&hit?'#b45309':'#e2e8f0';ctx.lineWidth=on&&hit?2.4:1.2;
        ctx.strokeRect(x,y,CS-2,CS-2);
        if(on){
          ctx.fillStyle=hit?'#7c2d12':'#94a3b8';ctx.font='bold 13px sans-serif';
          ctx.fillText(i+j,x+CS/2-1,y+CS/2+4);
        }
      }
    }
    ctx.textAlign='left';
    lbl(ctx,'두 주사위의 눈 (모두 36가지)',24,34,'#1d4ed8',18);
    box(ctx,20,350,400,66);
    lbl(ctx,(t===null)?('합이 '+S.s+'인 경우는 몇 가지일까?'):('합이 '+S.s+'인 경우 : '+c.cnt+'가지  →  확률 '+c.num+'/'+c.den),
        38,380,'#1f2937',19);
    lbl(ctx,'합은 2부터 12까지 11가지 — 확률은 모두 1/11일까?',38,406,'#b91c1c',15);
  },
  record:function(S){
    var c=this.calc(S);
    return {s:S.s,cnt:c.cnt,num:c.num,den:c.den,p:r3(c.p),
            eleven:(Math.abs(c.p-1/11)<0.001)};
  },
  headA:['번호','합','경우의 수','확률','소수로','1/11과 같은가?'],
  rowA:function(r,i){
    return [i+1,r.s,'<b>'+r.cnt+'가지</b>',r.num+'/'+r.den,r.p,
            '<span class="'+(r.eleven?'ok':'no')+'">'+(r.eleven?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ss={},sn=0,eleven=0,mx=0,mxs=0,mn=99,mns=0,tot=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(!ss[r.s]){ ss[r.s]=r.cnt; sn++; tot+=r.cnt; }
      if(r.eleven) eleven++;
      if(r.cnt>mx){ mx=r.cnt; mxs=r.s; }
      if(r.cnt<mn){ mn=r.cnt; mns=r.s; }
      rows.push([r.s, '<b>'+r.cnt+'가지</b>', r.num+'/'+r.den, r.p, r3(1/11),
                 '<span class="'+(r.eleven?'ok':'no')+'">'+(r.eleven?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'“모든 합이 1/11”이 맞은 횟수',big:eleven+' / '+rec.length,
       p:'합이 11가지이니 확률이 모두 같다고 보면 어떻게 되는지 확인했다.'},
      {t:'기록한 서로 다른 합',big:sn+'가지',
       p:sn>1?('경우의 수 합계 '+tot+'가지 (전체는 36가지).'):'여러 합을 기록해 비교해 보자.'},
      {t:'가장 많은 합 / 가장 적은 합',big:(mxs?(mxs+' ('+mx+'가지)'):'-')+' / '+(mns?(mns+' ('+mn+'가지)'):'-'),
       p:'합마다 만들 수 있는 방법의 수가 달랐다.'}
    ];
    var concl;
    if(sn<2){
      concl='<b>더 해 보자</b> — 여러 합을 기록해 경우의 수를 비교해야 한다. 2와 7을 모두 기록해 보자.';
    } else if(eleven===0){
      concl='<b>정리</b> — 두 눈의 합은 2부터 12까지 11가지지만 <b>각각의 확률은 전혀 같지 않았다.</b> '
           +'합이 2가 되는 방법은 (1,1) 하나뿐이고 7이 되는 방법은 6가지다. '
           +'확률을 구할 때 세어야 하는 것은 <b>“결과의 종류”가 아니라 “똑같이 일어날 수 있는 경우”</b>다. '
           +'그래서 분모는 11이 아니라 36이다.';
    } else {
      concl='<b>정리</b> — 합마다 경우의 수가 달랐다. 합 2와 합 7을 함께 기록하면 차이가 뚜렷해진다.';
    }
    return {head:['합','경우의 수','확률','소수','1/11','같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("m2_similarity_sas_lab.html",
     "닮음 실험실 — 두 변의 비만 같으면 닮음일까?",
     "닮음 실험실 — 두 변의 비만 같으면 닮음일까?",
     "두 변을 2배로 하되 낀각을 바꿔 가며 세 번째 변의 비를 재고, 닮음이 되는 조건을 찾는다.",
     LAB_SIM),
    ("m2_pythagoras_lab.html",
     "피타고라스 실험실 — 모든 삼각형에서 성립할까?",
     "피타고라스 실험실 — 모든 삼각형에서 성립할까?",
     "두 변 사이 각을 바꿔 가며 세 변 위 정사각형의 넓이를 재고, a²+b²와 c²을 비교한다.",
     LAB_PYTH),
    ("m2_segment_ratio_lab.html",
     "평행선 실험실 — 어떤 비가 서로 같을까?",
     "평행선 실험실 — 어떤 비가 서로 같을까?",
     "삼각형에 밑변과 평행한 선을 긋고 여러 선분의 비를 재어, 서로 같은 비와 다른 비를 구별한다.",
     LAB_SEG),
    ("m2_counting_rules_lab.html",
     "경우의 수 실험실 — 더할까, 곱할까?",
     "경우의 수 실험실 — 더할까, 곱할까?",
     "두 상황에서 경우를 하나씩 모두 세어 보고, m+n과 m×n 중 무엇이 맞는지 기록한다.",
     LAB_COUNT),
    ("m2_probability_complement_lab.html",
     "확률 실험실 — 모두 더하면 1일까?",
     "확률 실험실 — 모두 더하면 1일까?",
     "주머니 속 구슬 구성을 바꿔 각 색의 확률과 그 합, 여사건의 확률을 두 방법으로 구해 비교한다.",
     LAB_PROB),
    ("m2_two_dice_sum_lab.html",
     "주사위 실험실 — 합이 2일 확률과 7일 확률은 같을까?",
     "주사위 실험실 — 합이 2일 확률과 7일 확률은 같을까?",
     "36가지 경우를 모두 표에 놓고 각 합이 되는 경우의 수를 세어 확률을 비교한다.",
     LAB_DICE),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c16_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
