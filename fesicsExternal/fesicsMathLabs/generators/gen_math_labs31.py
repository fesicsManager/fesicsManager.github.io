# -*- coding: utf-8 -*-
"""고등 기하 — 이차곡선 4종 + 벡터 1종"""
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
"""

# ============================================================
# 1. 포물선
# ============================================================
LAB_PARAB = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'포물선 판',
  action:'두 거리 재기',
  hint0:'초점까지의 거리 p와 곡선 위 점의 위치를 정해 보자.',
  sliders:[
    {id:'p',label:'p (초점 x좌표)',min:1,max:4,value:1,color:'#2563eb',unit:''},
    {id:'ty',label:'점의 y좌표 (÷10)',min:-60,max:60,value:30,color:'#dc2626',
     fmt:function(v){return (v/10).toFixed(1);}}
  ],
  calc:function(S){
    var y=S.ty/10;
    var x=y*y/(4*S.p);
    var P=[x,y], F=[S.p,0];
    return {P:P,F:F,x:x,y:y,
            dF:dist(P,F),dL:Math.abs(x+S.p)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'초점까지',v:ran?r3(c.dF):'재 보자'},
            {k:'준선까지',v:ran?r3(c.dL):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '초점까지 '+r3(c.dF)+', 준선까지 '+r3(c.dL)+'.  점을 옮겨 다시 재 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,9,7);
    ctx.strokeStyle='#f59e0b';ctx.lineWidth=2.4;ctx.setLineDash([6,5]);
    ctx.beginPath();ctx.moveTo(CX-S.p*U,CY-7*U);ctx.lineTo(CX-S.p*U,CY+7*U);ctx.stroke();ctx.setLineDash([]);
    lbl(ctx,'준선 x = −'+S.p,CX-S.p*U-6,CY+7*U-6,'#b45309',13,'right');
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    var st=false;
    for(i=-70;i<=70;i++){
      var yy=i/10, xx=yy*yy/(4*S.p);
      if(xx>9){ st=false; continue; }
      if(!st){ ctx.moveTo(CX+xx*U,CY-yy*U); st=true; } else ctx.lineTo(CX+xx*U,CY-yy*U);
    }
    ctx.stroke();
    ctx.beginPath();ctx.arc(CX+S.p*U,CY,6,0,Math.PI*2);
    ctx.fillStyle='#dc2626';ctx.fill();
    lbl(ctx,'초점',CX+S.p*U+8,CY-10,'#b91c1c',13);
    var grow=(t===null)?0:Math.min(1,t);
    if(Math.abs(c.x)<=9&&Math.abs(c.y)<=7){
      ctx.beginPath();ctx.arc(CX+c.x*U,CY-c.y*U,7,0,Math.PI*2);
      ctx.fillStyle='#1f2937';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      if(grow>0){
        ctx.strokeStyle='#dc2626';ctx.lineWidth=3;
        ctx.beginPath();ctx.moveTo(CX+c.x*U,CY-c.y*U);
        ctx.lineTo(CX+c.x*U+((S.p-c.x)*U)*grow,CY-c.y*U+(c.y*U)*grow);ctx.stroke();
        ctx.strokeStyle='#f59e0b';
        ctx.beginPath();ctx.moveTo(CX+c.x*U,CY-c.y*U);
        ctx.lineTo(CX+c.x*U-((c.x+S.p)*U)*grow,CY-c.y*U);ctx.stroke();
      }
    }
    lbl(ctx,'y² = '+(4*S.p)+'x',24,32,'#1d4ed8',18);
    box(ctx,20,346,400,74);
    lbl(ctx,'점 ( '+r2(c.x)+' , '+r2(c.y)+' )',38,376,'#334155',17);
    lbl(ctx,(t===null)?'두 거리는 같을까?':('초점까지 '+r3(c.dF)+'      준선까지 '+r3(c.dL)),38,406,'#1f2937',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {p:S.p,x:r2(c.x),y:r2(c.y),dF:r3(c.dF),dL:r3(c.dL),
            same:(Math.abs(c.dF-c.dL)<1e-6),
            vertex:(Math.abs(c.y)<1e-9)};
  },
  headA:['번호','p','점','초점까지','준선까지','같은가?','꼭짓점?'],
  rowA:function(r,i){
    return [i+1,r.p,'('+r.x+', '+r.y+')','<b>'+r.dF+'</b>',r.dL,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            r.vertex?'○':'×'];
  },
  analyze:function(rec){
    var rows=[],same=0,ps={},pn=0,mn=999,mx=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(!ps[r.p]){ ps[r.p]=true; pn++; }
      var d=parseFloat(r.dF);
      if(d<mn) mn=d;
      if(d>mx) mx=d;
      rows.push([r.p, '('+r.x+', '+r.y+')', '<b>'+r.dF+'</b>', r.dL,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'초점까지 = 준선까지',big:same+' / '+rec.length,p:'곡선 위 여러 점에서 두 거리를 재어 비교한 결과.'},
      {t:'시험한 p',big:pn+'가지',p:'p를 바꿔도 성질이 유지되는지 확인했다.'},
      {t:'거리의 범위',big:mn+' ~ '+mx,p:'거리 자체는 점마다 다르지만 두 거리는 언제나 서로 같았다.'}
    ];
    var concl;
    if(same===rec.length){
      concl='<b>정리</b> — 포물선 위 어느 점에서 재도 <b>초점까지의 거리와 준선까지의 거리가 언제나 같았다.</b> '
           +'포물선은 “한 점(초점)과 한 직선(준선)에서 같은 거리에 있는 점들의 자취”로 정의되고, '
           +'y² = 4px 라는 식은 그 조건을 좌표로 옮겨 쓴 결과다. 거리 자체는 점마다 달라도 두 거리의 관계는 변하지 않는다.';
    } else {
      concl='<b>확인 필요</b> — 두 거리가 다른 기록이 있다.';
    }
    return {head:['p','점','초점까지','준선까지','같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 타원
# ============================================================
LAB_ELL = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'타원 판',
  action:'두 거리 합 구하기',
  hint0:'긴반지름 a와 짧은반지름 b, 그리고 점의 위치를 정해 보자.',
  sliders:[
    {id:'a',label:'a (가로 반지름)',min:3,max:8,value:5,color:'#2563eb',unit:''},
    {id:'b',label:'b (세로 반지름)',min:1,max:7,value:3,color:'#16a34a',unit:''},
    {id:'th',label:'점의 위치',min:0,max:350,value:50,color:'#dc2626',unit:'°'}
  ],
  calc:function(S){
    var a=S.a, b=Math.min(S.b,S.a-0.5);
    var c=Math.sqrt(Math.abs(a*a-b*b));
    var rad=S.th*Math.PI/180;
    var P=[a*Math.cos(rad),b*Math.sin(rad)];
    var F1=[-c,0], F2=[c,0];
    return {a:a,b:b,c:c,P:P,F1:F1,F2:F2,
            d1:dist(P,F1),d2:dist(P,F2),sum:dist(P,F1)+dist(P,F2),
            twoA:2*a,e:c/a};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'두 거리',v:ran?(r3(c.d1)+' / '+r3(c.d2)):'재 보자'},
            {k:'합',v:ran?r3(c.sum):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '두 거리의 합은 '+r3(c.sum)+'이고 2a = '+c.twoA+'다. 점을 옮겨 다시 재 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,9,7);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    for(i=0;i<=200;i++){
      var th=2*Math.PI*i/200;
      var x=c.a*Math.cos(th), y=c.b*Math.sin(th);
      if(i===0) ctx.moveTo(CX+x*U,CY-y*U); else ctx.lineTo(CX+x*U,CY-y*U);
    }
    ctx.closePath();ctx.stroke();
    [[c.F1,'F₁'],[c.F2,'F₂']].forEach(function(q){
      ctx.beginPath();ctx.arc(CX+q[0][0]*U,CY,6,0,Math.PI*2);
      ctx.fillStyle='#dc2626';ctx.fill();
      lbl(ctx,q[1],CX+q[0][0]*U-6,CY+22,'#b91c1c',13);
    });
    var grow=(t===null)?0:Math.min(1,t);
    ctx.beginPath();ctx.arc(CX+c.P[0]*U,CY-c.P[1]*U,7,0,Math.PI*2);
    ctx.fillStyle='#1f2937';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
    if(grow>0){
      [[c.F1,'#16a34a'],[c.F2,'#f59e0b']].forEach(function(q){
        ctx.strokeStyle=q[1];ctx.lineWidth=3;
        ctx.beginPath();ctx.moveTo(CX+c.P[0]*U,CY-c.P[1]*U);
        ctx.lineTo(CX+c.P[0]*U+((q[0][0]-c.P[0])*U)*grow,CY-c.P[1]*U+((c.P[1]-0)*U)*grow);
        ctx.stroke();
      });
    }
    lbl(ctx,'x²/'+r1(c.a*c.a)+' + y²/'+r1(c.b*c.b)+' = 1',24,32,'#1d4ed8',17);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'두 초점까지 거리의 합은?':('거리 '+r3(c.d1)+' + '+r3(c.d2)+' = '+r3(c.sum)),38,376,'#1f2937',18);
    lbl(ctx,'2a = '+c.twoA+'      c = '+r2(c.c)+'      이심률 '+r3(c.e),38,406,'#52627a',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:c.a,b:r1(c.b),c:r2(c.c),th:S.th,
            d1:r3(c.d1),d2:r3(c.d2),sum:r3(c.sum),twoA:c.twoA,e:r3(c.e),
            same:(Math.abs(c.sum-c.twoA)<1e-6),
            abc:(Math.abs(c.a*c.a-c.b*c.b-c.c*c.c)<1e-6)};
  },
  headA:['번호','a, b','점의 위치','거리 1','거리 2','합','2a','같은가?','a²−b²=c²?'],
  rowA:function(r,i){
    return [i+1,r.a+', '+r.b,r.th+'°',r.d1,r.d2,'<b>'+r.sum+'</b>',r.twoA,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            '<span class="'+(r.abc?'ok':'no')+'">'+(r.abc?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,abc=0,g={},pairs=0,agree=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.abc) abc++;
      var k=r.a+','+r.b, note='첫 기록';
      if(g[k]!==undefined){
        pairs++;
        var s=(Math.abs(g[k]-parseFloat(r.sum))<1e-6);
        if(s) agree++;
        note='<span class="'+(s?'ok':'no')+'">'+(s?'합 같음':'합 다름')+'</span>';
      } else { g[k]=parseFloat(r.sum); }
      rows.push([r.a+', '+r.b, r.th+'°', r.d1+' + '+r.d2, '<b>'+r.sum+'</b>', r.twoA,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>', note]);
    }
    var stats=[
      {t:'두 거리의 합 = 2a',big:same+' / '+rec.length,p:'점의 위치와 상관없이 성립했는지 확인한 결과.'},
      {t:'같은 타원에서 점만 옮긴 짝',big:pairs+'쌍',
       p:pairs?('그중 합이 같았던 것 '+agree+'쌍.'):'a, b를 그대로 두고 점의 위치만 바꿔 보자.'},
      {t:'a² − b² = c²',big:abc+' / '+rec.length,p:'초점의 위치가 a와 b로 정해지는지 확인했다.'}
    ];
    var concl;
    if(pairs===0){
      concl='<b>더 해 보자</b> — a, b를 고정하고 점의 위치만 바꿔 여러 번 기록해야 “합이 일정한지”를 확인할 수 있다.';
    } else if(same===rec.length&&agree===pairs){
      concl='<b>정리</b> — 타원 위 어느 점에서 재도 <b>두 초점까지 거리의 합이 항상 2a</b>로 같았다. '
           +'각각의 거리는 점마다 크게 달라지는데도 합은 움직이지 않았다. '
           +'끈의 양 끝을 두 초점에 고정하고 팽팽하게 당겨 그리면 타원이 되는 이유다. '
           +'초점 위치는 a² − b² = c² 로 정해졌고, c/a(이심률)가 클수록 납작해진다.';
    } else {
      concl='<b>확인 필요</b> — 합이 2a와 다른 기록이 있다.';
    }
    return {head:['a, b','위치','두 거리','합','2a','같은가?','같은 타원끼리'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 쌍곡선
# ============================================================
LAB_HYP = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'쌍곡선 판',
  action:'두 거리 차 구하기',
  hint0:'a와 b, 그리고 곡선 위 점의 위치를 정해 보자.',
  sliders:[
    {id:'a',label:'a',min:1,max:5,value:2,color:'#2563eb',unit:''},
    {id:'b',label:'b',min:1,max:5,value:2,color:'#16a34a',unit:''},
    {id:'tt',label:'점의 위치 (÷10)',min:-16,max:16,value:8,color:'#dc2626',
     fmt:function(v){return (v/10).toFixed(1);}}
  ],
  calc:function(S){
    var a=S.a, b=S.b, c=Math.sqrt(a*a+b*b);
    var u=S.tt/10;
    var P=[a*Math.cosh(u),b*Math.sinh(u)];
    var F1=[-c,0], F2=[c,0];
    return {a:a,b:b,c:c,P:P,F1:F1,F2:F2,
            d1:dist(P,F1),d2:dist(P,F2),
            diff:Math.abs(dist(P,F1)-dist(P,F2)),twoA:2*a};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'두 거리',v:ran?(r3(c.d1)+' / '+r3(c.d2)):'재 보자'},
            {k:'차',v:ran?r3(c.diff):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '두 거리의 차는 '+r3(c.diff)+'이고 2a = '+c.twoA+'다. 점을 옮겨 다시 재 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,9,7);
    ctx.strokeStyle='#cbd5e1';ctx.lineWidth=1.8;ctx.setLineDash([5,4]);
    [1,-1].forEach(function(s){
      ctx.beginPath();
      ctx.moveTo(CX-9*U,CY+s*(c.b/c.a)*9*U);
      ctx.lineTo(CX+9*U,CY-s*(c.b/c.a)*9*U);ctx.stroke();
    });
    ctx.setLineDash([]);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;
    [1,-1].forEach(function(sx){
      ctx.beginPath();
      var st=false;
      for(i=-25;i<=25;i++){
        var u=i/10;
        var x=sx*c.a*Math.cosh(u), y=c.b*Math.sinh(u);
        if(Math.abs(x)>9||Math.abs(y)>7){ st=false; continue; }
        if(!st){ ctx.moveTo(CX+x*U,CY-y*U); st=true; } else ctx.lineTo(CX+x*U,CY-y*U);
      }
      ctx.stroke();
    });
    [[c.F1,'F₁'],[c.F2,'F₂']].forEach(function(q){
      if(Math.abs(q[0][0])>9) return;
      ctx.beginPath();ctx.arc(CX+q[0][0]*U,CY,6,0,Math.PI*2);
      ctx.fillStyle='#dc2626';ctx.fill();
      lbl(ctx,q[1],CX+q[0][0]*U-6,CY+22,'#b91c1c',13);
    });
    var grow=(t===null)?0:Math.min(1,t);
    if(Math.abs(c.P[0])<=9&&Math.abs(c.P[1])<=7){
      ctx.beginPath();ctx.arc(CX+c.P[0]*U,CY-c.P[1]*U,7,0,Math.PI*2);
      ctx.fillStyle='#1f2937';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      if(grow>0){
        [[c.F1,'#16a34a'],[c.F2,'#f59e0b']].forEach(function(q){
          ctx.strokeStyle=q[1];ctx.lineWidth=3;
          ctx.beginPath();ctx.moveTo(CX+c.P[0]*U,CY-c.P[1]*U);
          ctx.lineTo(CX+c.P[0]*U+((q[0][0]-c.P[0])*U)*grow,CY-c.P[1]*U+((c.P[1])*U)*grow);
          ctx.stroke();
        });
      }
    }
    lbl(ctx,'x²/'+(c.a*c.a)+' − y²/'+(c.b*c.b)+' = 1      점선 = 점근선',24,32,'#1d4ed8',15);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'두 초점까지 거리의 차는?':('|'+r3(c.d1)+' − '+r3(c.d2)+'| = '+r3(c.diff)),38,376,'#1f2937',18);
    lbl(ctx,'2a = '+c.twoA+'      c = '+r2(c.c)+'   (a² + b² = c²)',38,406,'#52627a',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:c.a,b:c.b,c:r2(c.c),u:r1(S.tt/10),
            d1:r3(c.d1),d2:r3(c.d2),diff:r3(c.diff),twoA:c.twoA,
            same:(Math.abs(c.diff-c.twoA)<1e-6),
            abc:(Math.abs(c.a*c.a+c.b*c.b-c.c*c.c)<1e-6)};
  },
  headA:['번호','a, b','점의 위치','거리 1','거리 2','차','2a','같은가?','a²+b²=c²?'],
  rowA:function(r,i){
    return [i+1,r.a+', '+r.b,r.u,r.d1,r.d2,'<b>'+r.diff+'</b>',r.twoA,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            '<span class="'+(r.abc?'ok':'no')+'">'+(r.abc?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,abc=0,g={},pairs=0,agree=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.abc) abc++;
      var k=r.a+','+r.b, note='첫 기록';
      if(g[k]!==undefined){
        pairs++;
        var s=(Math.abs(g[k]-parseFloat(r.diff))<1e-6);
        if(s) agree++;
        note='<span class="'+(s?'ok':'no')+'">'+(s?'차 같음':'차 다름')+'</span>';
      } else { g[k]=parseFloat(r.diff); }
      rows.push([r.a+', '+r.b, r.u, r.d1+' / '+r.d2, '<b>'+r.diff+'</b>', r.twoA,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>', note]);
    }
    var stats=[
      {t:'두 거리의 차 = 2a',big:same+' / '+rec.length,p:'점의 위치와 상관없이 성립했는지 확인한 결과.'},
      {t:'같은 쌍곡선에서 점만 옮긴 짝',big:pairs+'쌍',
       p:pairs?('그중 차가 같았던 것 '+agree+'쌍.'):'a, b를 그대로 두고 점만 옮겨 보자.'},
      {t:'a² + b² = c²',big:abc+' / '+rec.length,p:'타원과 달리 <b>더한다</b>는 점이 다르다.'}
    ];
    var concl;
    if(pairs===0){
      concl='<b>더 해 보자</b> — a, b를 고정하고 점만 옮겨 여러 번 기록해 보자.';
    } else if(same===rec.length&&agree===pairs){
      concl='<b>정리</b> — 쌍곡선 위 어느 점에서 재도 <b>두 초점까지 거리의 차가 항상 2a</b>였다. '
           +'타원이 “합이 일정”이라면 쌍곡선은 “차가 일정”이다. '
           +'초점의 위치도 다르다. 타원은 a² − b² = c², 쌍곡선은 <b>a² + b² = c²</b> 이라 초점이 곡선 바깥쪽에 있다.';
    } else {
      concl='<b>확인 필요</b> — 차가 2a와 다른 기록이 있다.';
    }
    return {head:['a, b','위치','두 거리','차','2a','같은가?','같은 쌍곡선끼리'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 점근선
# ============================================================
LAB_ASYM = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'점근선 판',
  action:'멀리 가 보기',
  hint0:'a와 b, 그리고 확인할 x 좌표를 정해 보자.',
  sliders:[
    {id:'a',label:'a',min:1,max:4,value:2,color:'#2563eb',unit:''},
    {id:'b',label:'b',min:1,max:4,value:3,color:'#16a34a',unit:''},
    {id:'x0',label:'확인할 x',min:2,max:200,value:5,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var x=Math.max(S.x0,S.a+0.01);
    var y=S.b*Math.sqrt(x*x/(S.a*S.a)-1);
    var ay=S.b/S.a*x;
    return {x:x,y:y,ay:ay,gap:ay-y,ratio:y/ay};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'곡선의 y',v:ran?r3(c.y):'가 보자'},
            {k:'점근선의 y',v:ran?r3(c.ay):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'x = '+c.x+'에서 곡선은 '+r3(c.y)+', 점근선은 '+r3(c.ay)+'.  차이 '+r3(c.gap)+'.  x를 더 크게 해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,9,7);
    ctx.strokeStyle='#f59e0b';ctx.lineWidth=2.2;ctx.setLineDash([5,4]);
    [1,-1].forEach(function(s){
      ctx.beginPath();
      ctx.moveTo(CX-9*U,CY+s*(S.b/S.a)*9*U);
      ctx.lineTo(CX+9*U,CY-s*(S.b/S.a)*9*U);ctx.stroke();
    });
    ctx.setLineDash([]);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;
    [1,-1].forEach(function(sx){
      ctx.beginPath();
      var st=false;
      for(i=-25;i<=25;i++){
        var u=i/10;
        var x=sx*S.a*Math.cosh(u), y=S.b*Math.sinh(u);
        if(Math.abs(x)>9||Math.abs(y)>7){ st=false; continue; }
        if(!st){ ctx.moveTo(CX+x*U,CY-y*U); st=true; } else ctx.lineTo(CX+x*U,CY-y*U);
      }
      ctx.stroke();
    });
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0&&c.x<=9){
      ctx.strokeStyle='#dc2626';ctx.lineWidth=2.4;
      ctx.beginPath();ctx.moveTo(CX+c.x*U,CY-c.y*U);ctx.lineTo(CX+c.x*U,CY-c.ay*U);ctx.stroke();
      ctx.beginPath();ctx.arc(CX+c.x*U,CY-c.y*U,5,0,Math.PI*2);ctx.fillStyle='#2563eb';ctx.fill();
      ctx.beginPath();ctx.arc(CX+c.x*U,CY-c.ay*U,5,0,Math.PI*2);ctx.fillStyle='#f59e0b';ctx.fill();
    }
    if(c.x>9) lbl(ctx,'x = '+c.x+' 는 화면 밖이다',24,56,'#94a3b8',14);
    lbl(ctx,'x²/'+(S.a*S.a)+' − y²/'+(S.b*S.b)+' = 1,   점근선 y = ±'+r2(S.b/S.a)+'x',24,32,'#1d4ed8',15);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'멀리 가면 곡선은 어디로 갈까?':('x = '+c.x+' 에서 곡선 '+r3(c.y)+', 점근선 '+r3(c.ay)),38,376,'#1f2937',17);
    lbl(ctx,(t===null)?'':('차이 '+r3(c.gap)+'      비 '+r3(c.ratio)),38,406,'#15803d',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,x:c.x,y:r3(c.y),ay:r3(c.ay),
            gap:r3(c.gap),ratio:r3(c.ratio),
            meet:(Math.abs(c.gap)<1e-9),
            near:(c.gap<0.05)};
  },
  headA:['번호','a, b','x','곡선의 y','점근선의 y','차이','비','만나나?','0.05 이내?'],
  rowA:function(r,i){
    return [i+1,r.a+', '+r.b,r.x,'<b>'+r.y+'</b>',r.ay,r.gap,r.ratio,
            '<span class="'+(r.meet?'ok':'no')+'">'+(r.meet?'○':'×')+'</span>',
            '<span class="'+(r.near?'ok':'no')+'">'+(r.near?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],meet=0,near=0,g={},tested=0,ok=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.meet) meet++;
      if(r.near) near++;
      var k=r.a+','+r.b;
      if(!g[k]) g[k]=[];
      g[k].push([r.x,parseFloat(r.gap)]);
      rows.push([r.a+', '+r.b, r.x, '<b>'+r.y+'</b>', r.ay, r.gap, r.ratio,
                 '<span class="'+(r.meet?'ok':'no')+'">'+(r.meet?'○':'×')+'</span>']);
    }
    var k2;
    for(k2 in g){
      var arr=g[k2];
      if(arr.length<2) continue;
      arr.sort(function(x,y){return x[0]-y[0];});
      tested++;
      var good=true,j;
      for(j=1;j<arr.length;j++){ if(arr[j][1]>arr[j-1][1]+1e-9) good=false; }
      if(good) ok++;
    }
    var stats=[
      {t:'곡선이 점근선과 만난 횟수',big:meet+' / '+rec.length,
       p:'차이가 정확히 0이 된 적이 있었는지 확인한 결과.'},
      {t:'차이가 0.05 이내였던 횟수',big:near+' / '+rec.length,p:'x가 클수록 가까워졌다.'},
      {t:'x가 커질수록 차이가 줄어듦',big:tested?(ok+' / '+tested):'비교 없음',
       p:tested?'같은 a, b에서 x만 바꾼 묶음.':'같은 a, b로 x를 5, 20, 100 처럼 키워 보자.'}
    ];
    var concl;
    if(tested===0){
      concl='<b>더 해 보자</b> — a, b를 고정하고 x를 5, 20, 100, 200 으로 키워 가며 기록해 보자.';
    } else if(meet===0&&ok===tested){
      concl='<b>정리</b> — x를 아무리 키워도 곡선과 점근선의 차이는 <b>0에 가까워지기만 하고 0이 되지는 않았다.</b> '
           +'즉 두 그래프는 <b>영원히 만나지 않으면서 한없이 가까워진다.</b> '
           +'y의 비는 1에 다가갔다. 점근선은 곡선이 멀리서 어떤 방향으로 뻗는지를 알려 주고, 기울기는 ±b/a 다.';
    } else {
      concl='<b>확인 필요</b> — 곡선이 점근선과 만난 기록이 있다.';
    }
    return {head:['a, b','x','곡선 y','점근선 y','차이','비','만나나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 벡터의 덧셈과 크기
# ============================================================
LAB_VEC = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'벡터 덧셈 판',
  action:'이어 붙여 보기',
  hint0:'두 벡터의 성분을 정해 보자.',
  sliders:[
    {id:'a1',label:'a의 x성분',min:-6,max:6,value:4,color:'#2563eb',unit:''},
    {id:'a2',label:'a의 y성분',min:-6,max:6,value:1,color:'#60a5fa',unit:''},
    {id:'b1',label:'b의 x성분',min:-6,max:6,value:-1,color:'#dc2626',unit:''},
    {id:'b2',label:'b의 y성분',min:-6,max:6,value:4,color:'#f87171',unit:''}
  ],
  calc:function(S){
    var la=Math.sqrt(S.a1*S.a1+S.a2*S.a2);
    var lb=Math.sqrt(S.b1*S.b1+S.b2*S.b2);
    var sx=S.a1+S.b1, sy=S.a2+S.b2;
    var ls=Math.sqrt(sx*sx+sy*sy);
    return {la:la,lb:lb,sx:sx,sy:sy,ls:ls,sum:la+lb,
            gap:la+lb-ls,
            parallel:(Math.abs(S.a1*S.b2-S.a2*S.b1)<1e-9&&(S.a1*S.b1+S.a2*S.b2)>0)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'|a| + |b|',v:r3(c.sum)},
            {k:'|a + b|',v:ran?r3(c.ls):'이어 붙여 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '|a| + |b| = '+r3(c.sum)+', |a + b| = '+r3(c.ls)+'.  차이 '+r3(c.gap)+'.  기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    grid(ctx,7,6);
    function arrow(x0,y0,dx,dy,col,w){
      var X0=CX+x0*U, Y0=CY-y0*U, X1=CX+(x0+dx)*U, Y1=CY-(y0+dy)*U;
      ctx.strokeStyle=col;ctx.lineWidth=w||3;
      ctx.beginPath();ctx.moveTo(X0,Y0);ctx.lineTo(X1,Y1);ctx.stroke();
      var ang=Math.atan2(Y1-Y0,X1-X0);
      ctx.beginPath();ctx.moveTo(X1,Y1);
      ctx.lineTo(X1-10*Math.cos(ang-0.4),Y1-10*Math.sin(ang-0.4));
      ctx.lineTo(X1-10*Math.cos(ang+0.4),Y1-10*Math.sin(ang+0.4));
      ctx.closePath();ctx.fillStyle=col;ctx.fill();
    }
    var grow=(t===null)?0:Math.min(1,t);
    arrow(0,0,S.a1,S.a2,'#2563eb');
    if(grow>0) arrow(S.a1*grow,S.a2*grow,S.b1*grow,S.b2*grow,'#dc2626');
    if(grow>=1){
      arrow(0,0,c.sx,c.sy,'#7c3aed',4);
      lbl(ctx,'a + b',CX+c.sx*U/2+8,CY-c.sy*U/2,'#6d28d9',14);
    }
    lbl(ctx,'a = ('+S.a1+', '+S.a2+')      b = ('+S.b1+', '+S.b2+')',24,32,'#334155',16);
    box(ctx,20,346,400,74);
    lbl(ctx,'|a| = '+r3(c.la)+'      |b| = '+r3(c.lb),38,376,'#52627a',17);
    lbl(ctx,(t===null)?'|a+b| 는 |a|+|b| 와 같을까?':('|a+b| = '+r3(c.ls)+'      |a|+|b| = '+r3(c.sum)),
        38,406,'#1f2937',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:'('+S.a1+','+S.a2+')',b:'('+S.b1+','+S.b2+')',
            la:r3(c.la),lb:r3(c.lb),s:'('+c.sx+','+c.sy+')',
            ls:r3(c.ls),sum:r3(c.sum),gap:r3(c.gap),
            eq:(Math.abs(c.gap)<1e-9),
            le:(c.ls<=c.sum+1e-9),
            par:c.parallel};
  },
  headA:['번호','a','b','a+b','|a+b|','|a|+|b|','같은가?','|a+b| ≤ |a|+|b|?','같은 방향?'],
  rowA:function(r,i){
    return [i+1,r.a,r.b,r.s,'<b>'+r.ls+'</b>',r.sum,
            '<span class="'+(r.eq?'ok':'no')+'">'+(r.eq?'○':'×')+'</span>',
            '<span class="'+(r.le?'ok':'no')+'">'+(r.le?'○':'×')+'</span>',
            r.par?'○':'×'];
  },
  analyze:function(rec){
    var rows=[],le=0,eq=0,eqPar=0,mx=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.le) le++;
      if(r.eq){ eq++; if(r.par) eqPar++; }
      if(parseFloat(r.gap)>mx) mx=parseFloat(r.gap);
      rows.push([r.a+' + '+r.b, r.s, '<b>'+r.ls+'</b>', r.sum, r.gap,
                 '<span class="'+(r.eq?'ok':'no')+'">'+(r.eq?'○':'×')+'</span>',
                 '<span class="'+(r.le?'ok':'no')+'">'+(r.le?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'|a+b| ≤ |a|+|b|',big:le+' / '+rec.length,p:'예외가 있었는지 확인한 결과.'},
      {t:'두 값이 같았던 횟수',big:eq+' / '+rec.length,
       p:eq?('그중 두 벡터가 같은 방향이었던 것 '+eqPar+'개.'):'같은 방향인 두 벡터로도 해 보자.'},
      {t:'가장 큰 차이',big:mx+'',p:'방향이 어긋날수록 차이가 커진다.'}
    ];
    var concl;
    if(eq===0){
      concl='<b>더 해 보자</b> — 두 벡터를 <b>같은 방향</b>(예: (2,1)과 (4,2))으로 두면 어떻게 되는지 확인해 보자.';
    } else if(le===rec.length&&eq===eqPar){
      concl='<b>정리</b> — <b>|a + b| 가 |a| + |b| 를 넘은 적은 한 번도 없었고</b>, 같아진 것은 두 벡터가 같은 방향일 때뿐이었다. '
           +'벡터를 이어 붙이면 삼각형이 되고, 한 변은 나머지 두 변의 합보다 짧기 때문이다(삼각부등식). '
           +'벡터는 크기와 방향을 함께 가지므로 <b>크기끼리 그냥 더할 수 없다</b>.';
    } else {
      concl='<b>확인 필요</b> — 부등식이 깨진 기록이 있다.';
    }
    return {head:['a + b','합 벡터','|a+b|','|a|+|b|','차이','같은가?','부등식'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("hg_parabola_lab_Geometry_Conic_Ep01.html",
     "포물선 실험실 — 초점과 준선까지 거리는?",
     "포물선 실험실 — 초점과 준선까지 거리는?",
     "포물선 위 여러 점에서 초점까지와 준선까지의 거리를 재어 비교한다.",
     LAB_PARAB),
    ("hg_ellipse_lab_Geometry_Conic_Ep03.html",
     "타원 실험실 — 두 거리의 합은 변할까?",
     "타원 실험실 — 두 거리의 합은 변할까?",
     "타원 위 점을 옮겨 가며 두 초점까지 거리의 합을 재고 2a와 비교한다.",
     LAB_ELL),
    ("hg_hyperbola_lab_Geometry_Conic_Ep05.html",
     "쌍곡선 실험실 — 합이 아니라 차라면?",
     "쌍곡선 실험실 — 합이 아니라 차라면?",
     "쌍곡선 위 점을 옮겨 두 초점까지 거리의 차를 재고, 타원과 무엇이 다른지 확인한다.",
     LAB_HYP),
    ("hg_asymptote_lab_Geometry_Conic_Ep07.html",
     "점근선 실험실 — 언젠가는 만날까?",
     "점근선 실험실 — 언젠가는 만날까?",
     "x를 크게 키워 가며 곡선과 점근선의 y값 차이가 어떻게 되는지 기록한다.",
     LAB_ASYM),
    ("hg_vector_addition_lab_Geometry_Vector_Ep02.html",
     "벡터 실험실 — 크기끼리 더하면 될까?",
     "벡터 실험실 — 크기끼리 더하면 될까?",
     "두 벡터를 이어 붙여 합의 크기를 재고, 크기의 합과 비교한다.",
     LAB_VEC),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c31_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
