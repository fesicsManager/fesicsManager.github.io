# -*- coding: utf-8 -*-
"""중3 이차함수 1종 + 도형 2종 + 자료 2종"""
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
function angDeg(p,q,r){
  var ax=p[0]-q[0],ay=p[1]-q[1],bx=r[0]-q[0],by=r[1]-q[1];
  var d=ax*bx+ay*by,m=Math.sqrt(ax*ax+ay*ay)*Math.sqrt(bx*bx+by*by);
  var c=(m===0)?1:d/m; if(c>1)c=1; if(c<-1)c=-1;
  return Math.acos(c)*180/Math.PI;
}
"""

# ============================================================
# 1. 이차함수의 꼭짓점
# ============================================================
LAB_QUAD = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'포물선 이동판',
  action:'그래프 그리고 꼭짓점 찾기',
  hint0:'a, p, q를 정하고 y = a(x − p)² + q의 그래프를 그려 보자.',
  sliders:[
    {id:'a',label:'a',min:-3,max:3,value:1,color:'#2563eb',unit:''},
    {id:'p',label:'p',min:-5,max:5,value:3,color:'#16a34a',unit:''},
    {id:'q',label:'q',min:-5,max:5,value:-2,color:'#f59e0b',unit:''}
  ],
  f:function(S,x){ return S.a*(x-S.p)*(x-S.p)+S.q; },
  scan:function(S){
    var best=null,bx=0,i;
    for(i=-1000;i<=1000;i++){
      var x=i/100, y=this.f(S,x);
      if(best===null||((S.a>0)?(y<best):(y>best))){ best=y; bx=x; }
    }
    return {vx:Math.round(bx*100)/100,vy:Math.round(best*100)/100};
  },
  readout:function(S,ran){
    if(S.a===0) return [{k:'a = 0',v:'이차함수가 아니다'},{k:'',v:'a를 바꾸자'}];
    var v=this.scan(S);
    return [{k:'측정한 꼭짓점',v:ran?('( '+v.vx+' , '+v.vy+' )'):'찾아보자'},
            {k:'볼록 방향',v:(S.a>0)?'아래로 볼록':'위로 볼록'}];
  },
  doneMsg:function(S){
    if(S.a===0) return 'a가 0이면 이차함수가 아니다. a를 바꿔 보자.';
    var v=this.scan(S);
    return '꼭짓점은 ( '+v.vx+' , '+v.vy+' )다. p = '+S.p+', −p = '+(-S.p)+'와 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var i;
    var CX=220, CY=250, U=22;
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=-9;i<=9;i++){ ctx.beginPath();ctx.moveTo(CX+i*U,CY-9*U);ctx.lineTo(CX+i*U,CY+3*U);ctx.stroke(); }
    for(i=-3;i<=9;i++){ ctx.beginPath();ctx.moveTo(CX-9*U,CY-i*U);ctx.lineTo(CX+9*U,CY-i*U);ctx.stroke(); }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(CX-9*U,CY);ctx.lineTo(CX+9*U,CY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(CX,CY-9*U);ctx.lineTo(CX,CY+3*U);ctx.stroke();
    if(S.a===0){ lbl(ctx,'a = 0 이면 이차함수가 아니다',24,38,'#b91c1c',19); return; }
    var grow=(t===null)?0:Math.min(1,t);
    ctx.setLineDash([5,5]);ctx.strokeStyle='#cbd5e1';ctx.lineWidth=2;
    ctx.beginPath();
    var st=false;
    for(i=-90;i<=90;i++){
      var xx=i/10, yy=S.a*xx*xx;
      if(yy<-3||yy>9){ st=false; continue; }
      if(!st){ ctx.moveTo(CX+xx*U,CY-yy*U); st=true; } else ctx.lineTo(CX+xx*U,CY-yy*U);
    }
    ctx.stroke();ctx.setLineDash([]);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    st=false;
    for(i=-90;i<=90;i++){
      var x2=i/10, y2=this.f(S,x2);
      if(y2<-3||y2>9){ st=false; continue; }
      var Px=CX+x2*U, Py=CY-y2*U;
      if(!st){ ctx.moveTo(Px,Py); st=true; } else ctx.lineTo(Px,Py);
    }
    if(grow>0) ctx.stroke();
    var v=this.scan(S);
    if(grow>=1){
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=1.8;ctx.setLineDash([4,4]);
      ctx.beginPath();ctx.moveTo(CX+v.vx*U,CY-9*U);ctx.lineTo(CX+v.vx*U,CY+3*U);ctx.stroke();ctx.setLineDash([]);
      ctx.beginPath();ctx.arc(CX+v.vx*U,CY-v.vy*U,8,0,Math.PI*2);
      ctx.fillStyle='#dc2626';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      lbl(ctx,'('+v.vx+', '+v.vy+')',CX+v.vx*U+12,CY-v.vy*U-10,'#b91c1c',15);
    }
    lbl(ctx,'y = '+S.a+'(x'+sg(-S.p)+')²'+sg(S.q)+'      점선 = y = '+S.a+'x²',24,32,'#1d4ed8',16);
    box(ctx,20,338,400,84);
    lbl(ctx,(t===null)?'꼭짓점은 어디일까?':('측정한 꼭짓점 : ( '+v.vx+' , '+v.vy+' )'),38,370,'#1f2937',19);
    lbl(ctx,(t===null)?'':('p = '+S.p+'      −p = '+(-S.p)+'      q = '+S.q),38,402,'#52627a',18);
  },
  record:function(S){
    if(S.a===0) return {zero:true};
    var v=this.scan(S);
    return {zero:false,a:S.a,p:S.p,q:S.q,vx:v.vx,vy:v.vy,
            okP:(Math.abs(v.vx-S.p)<0.02),okNP:(Math.abs(v.vx+S.p)<0.02),
            okQ:(Math.abs(v.vy-S.q)<0.02),
            up:(S.a>0)};
  },
  headA:['번호','식','측정한 꼭짓점','p','꼭짓점 x = p?','−p','= −p?','q','꼭짓점 y = q?','볼록'],
  rowA:function(r,i){
    if(r.zero) return [i+1,'a=0','-','-','-','-','-','-','-','-'];
    return [i+1,r.a+'(x'+sg(-r.p)+')²'+sg(r.q),'('+r.vx+', '+r.vy+')',r.p,
            '<span class="'+(r.okP?'ok':'no')+'">'+(r.okP?'○':'×')+'</span>',
            -r.p,
            '<span class="'+(r.okNP?'ok':'no')+'">'+(r.okNP?'○':'×')+'</span>',
            r.q,
            '<span class="'+(r.okQ?'ok':'no')+'">'+(r.okQ?'○':'×')+'</span>',
            r.up?'아래로':'위로'];
  },
  analyze:function(rec){
    var rows=[],valid=0,okP=0,okNP=0,okQ=0,p0=0,up=0,upOk=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.zero){ rows.push(['a=0','-','-','-','-','-']); continue; }
      valid++;
      if(r.okP) okP++;
      if(r.okNP){ okNP++; if(r.p===0) p0++; }
      if(r.okQ) okQ++;
      if(r.up){ up++; upOk++; }
      rows.push([r.a+'(x'+sg(-r.p)+')²'+sg(r.q), '('+r.vx+', '+r.vy+')', r.p,
                 '<span class="'+(r.okP?'ok':'no')+'">'+(r.okP?'○':'×')+'</span>',
                 -r.p,
                 '<span class="'+(r.okNP?'ok':'no')+'">'+(r.okNP?'○':'×')+'</span>',
                 r.up?'아래로 볼록':'위로 볼록']);
    }
    var stats=[
      {t:'꼭짓점의 x좌표 = p',big:okP+' / '+valid,p:'그래프에서 직접 찾은 꼭짓점과 비교한 결과.'},
      {t:'꼭짓점의 x좌표 = −p',big:okNP+' / '+valid,
       p:okNP?('그중 p가 0이었던 것 '+p0+'개. p=0이면 두 값이 같아진다.'):'부호를 반대로 보면 맞지 않는다.'},
      {t:'꼭짓점의 y좌표 = q',big:okQ+' / '+valid,p:'위아래 이동은 q 그대로였다.'}
    ];
    var concl;
    if(valid===0){
      concl='<b>더 해 보자</b> — a를 0이 아닌 값으로 두어야 이차함수가 된다.';
    } else if(okP===valid&&okNP===p0){
      concl='<b>정리</b> — 꼭짓점은 언제나 <b>(p, q)</b>였다. y = a(x − p)² + q에서 괄호 안이 (x − p)면 그래프는 <b>오른쪽으로 p만큼</b> 옮겨진다. '
           +'식에 보이는 부호와 이동 방향이 반대라서 −p로 착각하기 쉽지만, x = p일 때 괄호가 0이 되어 그 자리가 꼭짓점이 된다. '
           +'q는 그대로 위아래 이동량이고, a의 부호가 볼록한 방향을 정한다.';
    } else {
      concl='<b>확인 필요</b> — 측정한 꼭짓점과 p, q가 어긋난 기록이 있다.';
    }
    return {head:['식','측정한 꼭짓점','p','= p?','−p','= −p?','볼록'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 삼각비
# ============================================================
LAB_TRIG = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'삼각비 실험판',
  action:'두 삼각형 재기',
  hint0:'각을 정하고, 크기가 다른 두 직각삼각형에서 변의 비를 재 보자.',
  sliders:[
    {id:'th',label:'각의 크기',min:10,max:80,value:35,color:'#2563eb',unit:'°'},
    {id:'c1',label:'작은 삼각형의 빗변',min:60,max:130,value:90,color:'#16a34a',unit:''},
    {id:'c2',label:'큰 삼각형의 빗변',min:140,max:250,value:200,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var rad=S.th*Math.PI/180;
    var b1=S.c1*Math.cos(rad), h1=S.c1*Math.sin(rad);
    var b2=S.c2*Math.cos(rad), h2=S.c2*Math.sin(rad);
    return {b1:b1,h1:h1,b2:b2,h2:h2,
            s1:h1/S.c1,s2:h2/S.c2,cs1:b1/S.c1,cs2:b2/S.c2,t1:h1/b1,t2:h2/b2};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'높이 ÷ 빗변',v:ran?(r3(c.s1)+' / '+r3(c.s2)):'재 보자'},
            {k:'높이 ÷ 밑변',v:ran?(r3(c.t1)+' / '+r3(c.t2)):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '작은 삼각형과 큰 삼각형의 (높이÷빗변)은 '+r3(c.s1)+'과 '+r3(c.s2)+'다. 크기가 달라도 비가 같은지 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var OX=40, OY=300;
    var grow=(t===null)?0:Math.min(1,t);
    function tri(len,col,w){
      var rad=S.th*Math.PI/180;
      var B=[OX+len*Math.cos(rad)*0+len*Math.cos(rad),OY];
      var bx=OX+len*Math.cos(rad), by=OY-len*Math.sin(rad);
      ctx.beginPath();ctx.moveTo(OX,OY);ctx.lineTo(OX+len*Math.cos(rad),OY);
      ctx.lineTo(OX+len*Math.cos(rad),OY-len*Math.sin(rad));ctx.closePath();
      ctx.strokeStyle=col;ctx.lineWidth=w;ctx.stroke();
      return {b:[OX+len*Math.cos(rad),OY],h:[OX+len*Math.cos(rad),OY-len*Math.sin(rad)]};
    }
    var big=tri(S.c2,'#f59e0b',3);
    var sml=tri(S.c1,'#16a34a',3);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;
    ctx.beginPath();ctx.moveTo(OX,OY);ctx.lineTo(big.h[0],big.h[1]);ctx.stroke();
    ctx.beginPath();ctx.arc(OX,OY,34,-S.th*Math.PI/180,0);
    ctx.strokeStyle='#1d4ed8';ctx.lineWidth=2;ctx.stroke();
    lbl(ctx,S.th+'°',OX+40,OY-10,'#1d4ed8',15);
    if(grow>=1){
      lbl(ctx,'작은 : 높이 '+r1(c.h1)+' / 빗변 '+S.c1,24,44,'#15803d',15);
      lbl(ctx,'큰 : 높이 '+r1(c.h2)+' / 빗변 '+S.c2,24,66,'#b45309',15);
    }
    box(ctx,20,326,400,90);
    lbl(ctx,(t===null)?'크기가 다르면 비도 다를까?':
        ('높이÷빗변 : '+r3(c.s1)+'  vs  '+r3(c.s2)),38,356,'#1f2937',19);
    lbl(ctx,(t===null)?'':('밑변÷빗변 : '+r3(c.cs1)+'  vs  '+r3(c.cs2)),38,384,'#52627a',18);
    lbl(ctx,(t===null)?'':('높이÷밑변 : '+r3(c.t1)+'  vs  '+r3(c.t2)),38,410,'#52627a',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {th:S.th,c1:S.c1,c2:S.c2,
            s1:r3(c.s1),s2:r3(c.s2),cs1:r3(c.cs1),cs2:r3(c.cs2),t1:r3(c.t1),t2:r3(c.t2),
            sOk:(Math.abs(c.s1-c.s2)<1e-9),cOk:(Math.abs(c.cs1-c.cs2)<1e-9),tOk:(Math.abs(c.t1-c.t2)<1e-9),
            sizeDiff:(S.c1!==S.c2)};
  },
  headA:['번호','각','두 빗변','높이÷빗변','같은가?','밑변÷빗변','같은가?','높이÷밑변','같은가?'],
  rowA:function(r,i){
    return [i+1,r.th+'°',r.c1+' / '+r.c2,r.s1+' / '+r.s2,
            '<span class="'+(r.sOk?'ok':'no')+'">'+(r.sOk?'○':'×')+'</span>',
            r.cs1+' / '+r.cs2,
            '<span class="'+(r.cOk?'ok':'no')+'">'+(r.cOk?'○':'×')+'</span>',
            r.t1+' / '+r.t2,
            '<span class="'+(r.tOk?'ok':'no')+'">'+(r.tOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],sOk=0,ths={},tn=0,g={},pairs=0,diffTh=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.sOk) sOk++;
      if(!ths[r.th]){ ths[r.th]=r.s1; tn++; }
      else if(Math.abs(ths[r.th]-r.s1)>1e-9) diffTh++;
      rows.push([r.th+'°', r.c1+' / '+r.c2, r.s1+' / '+r.s2,
                 '<span class="'+(r.sOk?'ok':'no')+'">'+(r.sOk?'○':'×')+'</span>',
                 r.t1+' / '+r.t2,
                 '<span class="'+(r.tOk?'ok':'no')+'">'+(r.tOk?'○':'×')+'</span>']);
    }
    var vals=[],k;
    for(k in ths){ vals.push(k+'° → '+r3(ths[k])); }
    var stats=[
      {t:'크기가 달라도 (높이÷빗변)이 같았던 횟수',big:sOk+' / '+rec.length,
       p:'같은 각에서 빗변만 다르게 한 두 삼각형을 비교한 결과.'},
      {t:'시험한 각',big:tn+'가지',p:vals.join(' / ')},
      {t:'같은 각에서 값이 달라진 경우',big:diffTh+'개',
       p:diffTh?'다시 확인해 보자.':'같은 각이면 언제나 같은 값이었다.'}
    ];
    var concl;
    if(tn<2){
      concl='<b>더 해 보자</b> — 각을 바꿔 여러 값을 기록하면, 각마다 비가 정해져 있다는 것이 보인다.';
    } else if(sOk===rec.length&&diffTh===0){
      concl='<b>정리</b> — 직각삼각형의 크기를 바꿔도 <b>변의 비는 하나도 달라지지 않았고</b>, 각이 달라지면 비도 달라졌다. '
           +'즉 이 비는 <b>각의 크기만으로 정해지는 값</b>이다. 그래서 각마다 이름을 붙여 sin, cos, tan이라고 부른다. '
           +'삼각형이 닮음이면 대응변의 비가 같다는 사실이 그 근거다.';
    } else {
      concl='<b>확인 필요</b> — 크기가 다른데 비가 달라진 기록이 있다.';
    }
    return {head:['각','두 빗변','높이÷빗변','같은가?','높이÷밑변','같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 원주각과 중심각
# ============================================================
LAB_INSC = BASE + r"""
var CX=220, CY=200, R=130;
var LAB = {
  cw:440, ch:420, cvTitle:'원주각 실험판',
  action:'원주각 재기',
  hint0:'호의 중심각과, 원 위 점 P의 위치를 정해 보자.',
  sliders:[
    {id:'th',label:'호 AB의 중심각',min:30,max:300,value:110,color:'#2563eb',unit:'°'},
    {id:'u',label:'점 P의 위치',min:5,max:95,value:50,color:'#f59e0b',
     fmt:function(v){return '남은 호의 '+v+'%';}}
  ],
  calc:function(S){
    var aA=-90, aB=-90+S.th;
    var rest=360-S.th;
    var aP=aB+rest*S.u/100;
    function pt(deg){ var r=deg*Math.PI/180; return [CX+R*Math.cos(r),CY+R*Math.sin(r)]; }
    var A=pt(aA), B=pt(aB), P=pt(aP);
    return {A:A,B:B,P:P,ins:angDeg(A,P,B),cen:S.th};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'중심각',v:S.th+'°'},
            {k:'원주각',v:ran?(r1(c.ins)+'°'):'재 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '원주각은 '+r1(c.ins)+'°, 중심각의 '+r2(c.ins/S.th)+'배다. P를 옮겨 다시 재 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    ctx.beginPath();ctx.arc(CX,CY,R,0,Math.PI*2);
    ctx.strokeStyle='#94a3b8';ctx.lineWidth=2;ctx.stroke();
    ctx.beginPath();ctx.arc(CX,CY,R,-Math.PI/2,(-90+S.th)*Math.PI/180);
    ctx.strokeStyle='#dc2626';ctx.lineWidth=5;ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    ctx.beginPath();ctx.moveTo(CX,CY);
    ctx.arc(CX,CY,44,-Math.PI/2,(-90+S.th*grow)*Math.PI/180);
    ctx.closePath();ctx.fillStyle='rgba(37,99,235,0.22)';ctx.fill();
    ctx.strokeStyle='#2563eb';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(CX,CY);ctx.lineTo(c.A[0],c.A[1]);
    ctx.moveTo(CX,CY);ctx.lineTo(c.B[0],c.B[1]);ctx.stroke();
    if(grow>0){
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=2.6;
      ctx.beginPath();ctx.moveTo(c.P[0],c.P[1]);
      ctx.lineTo(c.P[0]+(c.A[0]-c.P[0])*grow,c.P[1]+(c.A[1]-c.P[1])*grow);
      ctx.moveTo(c.P[0],c.P[1]);
      ctx.lineTo(c.P[0]+(c.B[0]-c.P[0])*grow,c.P[1]+(c.B[1]-c.P[1])*grow);
      ctx.stroke();
    }
    [[c.A,'A','#334155'],[c.B,'B','#334155'],[c.P,'P','#b45309']].forEach(function(q){
      ctx.beginPath();ctx.arc(q[0][0],q[0][1],6,0,Math.PI*2);
      ctx.fillStyle=q[2];ctx.fill();
      lbl(ctx,q[1],q[0][0]+10,q[0][1]-8,q[2],15);
    });
    ctx.beginPath();ctx.arc(CX,CY,5,0,Math.PI*2);ctx.fillStyle='#1f2937';ctx.fill();
    lbl(ctx,'빨간 호 AB에 대한 중심각과 원주각',24,32,'#1d4ed8',17);
    box(ctx,20,336,400,74);
    lbl(ctx,'중심각 : '+S.th+'°',38,366,'#1d4ed8',19);
    lbl(ctx,(t===null)?'원주각은 얼마일까?':('원주각 : '+r1(c.ins)+'°      중심각 ÷ 원주각 = '+r2(S.th/c.ins)),
        38,396,'#b45309',19);
  },
  record:function(S){
    var c=this.calc(S);
    return {th:S.th,u:S.u,ins:r1(c.ins),ratio:r2(S.th/c.ins),
            half:(Math.abs(c.ins-S.th/2)<0.05)};
  },
  headA:['번호','중심각','P의 위치','원주각','중심각 ÷ 원주각','원주각 = 중심각의 반?'],
  rowA:function(r,i){
    return [i+1,r.th+'°',r.u+'%','<b>'+r.ins+'°</b>',r.ratio,
            '<span class="'+(r.half?'ok':'no')+'">'+(r.half?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],half=0,g={},pairs=0,agree=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.half) half++;
      var note='첫 기록';
      if(g[r.th]!==undefined){
        pairs++;
        var same=(Math.abs(g[r.th]-r.ins)<0.05);
        if(same) agree++;
        note='<span class="'+(same?'ok':'no')+'">'+(same?'같은 값':'다른 값')+'</span>';
      } else { g[r.th]=r.ins; }
      rows.push([r.th+'°', r.u+'%', '<b>'+r.ins+'°</b>', r.ratio,
                 '<span class="'+(r.half?'ok':'no')+'">'+(r.half?'○':'×')+'</span>', note]);
    }
    var stats=[
      {t:'원주각 = 중심각의 절반',big:half+' / '+rec.length,
       p:'중심각 ÷ 원주각이 2였는지 확인한 결과.'},
      {t:'같은 호에서 P만 옮긴 짝',big:pairs+'쌍',
       p:pairs?('그중 원주각이 같았던 것 '+agree+'쌍.'):'중심각을 그대로 두고 P의 위치만 바꿔 기록해 보자.'},
      {t:'전체 기록',big:rec.length+'개',p:'중심각도 바꿔 가며 확인해 보자.'}
    ];
    var concl;
    if(pairs===0){
      concl='<b>더 해 보자</b> — 중심각을 고정하고 P의 위치만 바꿔 두 번 이상 기록해야 “위치와 상관없다”를 확인할 수 있다.';
    } else if(half===rec.length&&agree===pairs){
      concl='<b>정리</b> — 같은 호에 대한 원주각은 <b>P를 어디에 두어도 똑같았고</b>, 언제나 <b>중심각의 절반</b>이었다. '
           +'그래서 반원에 대한 원주각(중심각 180°)은 항상 90°가 된다. '
           +'원주각의 크기를 정하는 것은 점의 위치가 아니라 <b>어느 호를 보고 있는가</b>다.';
    } else {
      concl='<b>확인 필요</b> — 절반이 아니거나 위치에 따라 달라진 기록이 있다.';
    }
    return {head:['중심각','P의 위치','원주각','중심각÷원주각','절반인가?','같은 호끼리'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 평균과 중앙값
# ============================================================
LAB_MED = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'대푯값 비교판',
  action:'평균과 중앙값 구하기',
  hint0:'네 사람의 값과 한 사람의 값을 정해 보자. 마지막 값만 크게 바꿀 수 있다.',
  sliders:[
    {id:'a',label:'① 값',min:1,max:20,value:6,color:'#60a5fa',unit:''},
    {id:'b',label:'② 값',min:1,max:20,value:8,color:'#60a5fa',unit:''},
    {id:'c',label:'③ 값',min:1,max:20,value:9,color:'#60a5fa',unit:''},
    {id:'e',label:'⑤ 값 (크게 바꿀 수 있음)',min:1,max:100,value:12,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var v=[S.a,S.b,S.c,10,S.e];
    var s=0,i;
    for(i=0;i<5;i++) s+=v[i];
    var so=v.slice().sort(function(x,y){return x-y;});
    return {v:v,so:so,mean:s/5,med:so[2],sum:s};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'평균',v:ran?r2(c.mean):'구해 보자'},
            {k:'중앙값',v:ran?c.med:'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '평균 '+r2(c.mean)+', 중앙값 '+c.med+'.  차이 '+r2(Math.abs(c.mean-c.med))+'.  ⑤의 값을 크게 바꿔 다시 해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var X0=40, X1=410, LO=0, HI=100;
    function px(v){ return X0+(X1-X0)*(v-LO)/(HI-LO); }
    var Y=190;
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(X0,Y);ctx.lineTo(X1,Y);ctx.stroke();
    for(i=0;i<=100;i+=10){
      var x=px(i);
      ctx.beginPath();ctx.moveTo(x,Y-6);ctx.lineTo(x,Y+6);
      ctx.strokeStyle='#94a3b8';ctx.lineWidth=1.4;ctx.stroke();
      ctx.fillStyle='#94a3b8';ctx.font='11px sans-serif';ctx.textAlign='center';
      ctx.fillText(i,x,Y+22);
    }
    ctx.textAlign='left';
    for(i=0;i<5;i++){
      ctx.beginPath();ctx.arc(px(c.v[i]),Y-16,8,0,Math.PI*2);
      ctx.fillStyle=(i===4)?'#ef4444':'#60a5fa';ctx.fill();
      ctx.strokeStyle='#1f2937';ctx.lineWidth=1.4;ctx.stroke();
    }
    var show=(t===null)?0:Math.min(1,t);
    if(show>0){
      ctx.strokeStyle='#7c3aed';ctx.lineWidth=3;
      ctx.beginPath();ctx.moveTo(px(c.mean),Y-46);ctx.lineTo(px(c.mean),Y+6);ctx.stroke();
      lbl(ctx,'평균 '+r2(c.mean),px(c.mean),Y-54,'#6d28d9',14,'center');
      ctx.strokeStyle='#059669';ctx.lineWidth=3;
      ctx.beginPath();ctx.moveTo(px(c.med),Y+6);ctx.lineTo(px(c.med),Y+54);ctx.stroke();
      lbl(ctx,'중앙값 '+c.med,px(c.med),Y+72,'#047857',14,'center');
    }
    lbl(ctx,'다섯 값 : '+c.so.join(', ')+'   (④는 10으로 고정)',24,38,'#1d4ed8',17);
    box(ctx,20,290,400,94);
    lbl(ctx,(t===null)?'평균과 중앙값은 어떻게 다를까?':('평균 '+r2(c.mean)+'      중앙값 '+c.med),38,322,'#1f2937',20);
    lbl(ctx,(t===null)?'':('차이 '+r2(Math.abs(c.mean-c.med))+'      가장 큰 값 '+c.so[4]),38,354,'#52627a',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {v:c.so.join(', '),mean:r2(c.mean),med:c.med,
            gap:r2(Math.abs(c.mean-c.med)),max:c.so[4],e:S.e,
            close:(Math.abs(c.mean-c.med)<1)};
  },
  headA:['번호','자료','⑤ 값','평균','중앙값','차이','가장 큰 값'],
  rowA:function(r,i){
    return [i+1,r.v,r.e,'<b>'+r.mean+'</b>',r.med,r.gap,r.max];
  },
  analyze:function(rec){
    var rows=[],mnG=999,mxG=0,mnE=0,mxE=0,medSet={},mn2=0,meanMin=999,meanMax=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.gap<mnG){ mnG=r.gap; mnE=r.e; }
      if(r.gap>mxG){ mxG=r.gap; mxE=r.e; }
      if(!medSet[r.med]){ medSet[r.med]=true; mn2++; }
      if(r.mean<meanMin) meanMin=r.mean;
      if(r.mean>meanMax) meanMax=r.mean;
      rows.push([r.v, r.e, '<b>'+r.mean+'</b>', r.med, r.gap, r.max]);
    }
    var stats=[
      {t:'평균이 움직인 범위',big:meanMin+' ~ '+meanMax,p:'⑤의 값을 바꿨을 때 평균이 변한 폭.'},
      {t:'중앙값의 서로 다른 값',big:mn2+'가지',
       p:(mn2<=2)?'⑤이 아무리 커져도 중앙값은 거의 움직이지 않았다.':'중앙값도 여러 값이 나왔다.'},
      {t:'평균 − 중앙값 차이',big:mnG+' ~ '+mxG,
       p:'가장 작았을 때 ⑤ = '+mnE+', 가장 컸을 때 ⑤ = '+mxE+'.'}
    ];
    var concl;
    if(rec.length<4||mxG-mnG<0.5){
      concl='<b>더 해 보자</b> — ⑤의 값을 12에서 90처럼 <b>아주 크게</b> 바꿔서 다시 기록해 보자.';
    } else {
      concl='<b>정리</b> — 값 하나만 크게 바꿨을 뿐인데 <b>평균은 '+meanMin+'에서 '+meanMax+'까지 끌려갔고</b>, '
           +'중앙값은 '+mn2+'가지 값에 머물렀다. 평균은 모든 값을 합해 나누므로 극단적인 값 하나에 크게 흔들리지만, '
           +'중앙값은 <b>순서상 가운데</b>만 보기 때문에 잘 흔들리지 않는다. '
           +'자료에 아주 크거나 작은 값이 섞여 있으면 중앙값이 더 나은 대푯값일 수 있다.';
    }
    return {head:['자료','⑤','평균','중앙값','차이','최댓값'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 표준편차
# ============================================================
LAB_STD = BASE + r"""
function stats5(arr){
  var s=0,i;
  for(i=0;i<arr.length;i++) s+=arr[i];
  var m=s/arr.length;
  var v=0;
  for(i=0;i<arr.length;i++) v+=(arr[i]-m)*(arr[i]-m);
  v/=arr.length;
  return {mean:m,varr:v,sd:Math.sqrt(v)};
}
var LAB = {
  cw:440, ch:400, cvTitle:'흩어진 정도 판',
  action:'평균과 표준편차 구하기',
  hint0:'두 모둠의 공통 평균과 각각의 흩어진 정도를 정해 보자.',
  sliders:[
    {id:'m',label:'공통 평균',min:5,max:15,value:10,color:'#7c3aed',unit:'점'},
    {id:'s',label:'A 모둠의 흩어짐',min:0,max:8,value:1,color:'#2563eb',unit:''},
    {id:'u',label:'B 모둠의 흩어짐',min:0,max:8,value:6,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var A=[S.m-S.s,S.m-S.s/2,S.m,S.m+S.s/2,S.m+S.s];
    var B=[S.m-S.u,S.m-S.u/2,S.m,S.m+S.u/2,S.m+S.u];
    return {A:A,B:B,sa:stats5(A),sb:stats5(B)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'두 모둠의 평균',v:r2(c.sa.mean)+' / '+r2(c.sb.mean)},
            {k:'표준편차',v:ran?(r2(c.sa.sd)+' / '+r2(c.sb.sd)):'구해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '평균은 둘 다 '+r2(c.sa.mean)+'인데 표준편차는 '+r2(c.sa.sd)+'와 '+r2(c.sb.sd)+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var X0=40, X1=410, LO=0, HI=24;
    function px(v){ return X0+(X1-X0)*(v-LO)/(HI-LO); }
    var grow=(t===null)?0:Math.min(1,t);
    function row(Y,arr,col,name,sd){
      ctx.strokeStyle='#cbd5e1';ctx.lineWidth=2;
      ctx.beginPath();ctx.moveTo(X0,Y);ctx.lineTo(X1,Y);ctx.stroke();
      lbl(ctx,name,24,Y+6,col,17);
      for(i=0;i<arr.length;i++){
        ctx.beginPath();ctx.arc(px(arr[i]),Y,8,0,Math.PI*2);
        ctx.fillStyle=col;ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=1.6;ctx.stroke();
      }
      ctx.strokeStyle='#7c3aed';ctx.lineWidth=2.6;
      ctx.beginPath();ctx.moveTo(px(S.m),Y-22);ctx.lineTo(px(S.m),Y+22);ctx.stroke();
      if(grow>=1){
        ctx.strokeStyle=col;ctx.lineWidth=2;ctx.setLineDash([4,4]);
        ctx.beginPath();ctx.moveTo(px(S.m-sd),Y+26);ctx.lineTo(px(S.m+sd),Y+26);ctx.stroke();ctx.setLineDash([]);
        lbl(ctx,'표준편차 '+r2(sd),px(S.m+sd)+8,Y+31,col,14);
      }
    }
    row(110,c.A,'#2563eb','A',c.sa.sd);
    row(220,c.B,'#dc2626','B',c.sb.sd);
    lbl(ctx,'보라 선 = 평균 '+S.m+'점',24,38,'#6d28d9',17);
    box(ctx,20,286,400,98);
    lbl(ctx,'평균 : A '+r2(c.sa.mean)+'   B '+r2(c.sb.mean),38,318,'#1f2937',19);
    lbl(ctx,(t===null)?'평균이 같으면 자료도 비슷할까?':('분산 : A '+r2(c.sa.varr)+'   B '+r2(c.sb.varr)),38,348,'#52627a',18);
    lbl(ctx,(t===null)?'':('표준편차 : A '+r2(c.sa.sd)+'   B '+r2(c.sb.sd)),38,376,'#15803d',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {m:S.m,s:S.s,u:S.u,
            mA:r2(c.sa.mean),mB:r2(c.sb.mean),
            vA:r2(c.sa.varr),vB:r2(c.sb.varr),
            sA:r2(c.sa.sd),sB:r2(c.sb.sd),
            meanSame:(Math.abs(c.sa.mean-c.sb.mean)<1e-9),
            sdSame:(Math.abs(c.sa.sd-c.sb.sd)<1e-9),
            wider:(c.sb.sd>c.sa.sd)?'B':((c.sa.sd>c.sb.sd)?'A':'같음'),
            spreadWider:(S.u>S.s)?'B':((S.s>S.u)?'A':'같음')};
  },
  headA:['번호','평균','A 흩어짐','B 흩어짐','A 표준편차','B 표준편차','평균 같음','표준편차 같음','더 퍼진 쪽'],
  rowA:function(r,i){
    return [i+1,r.mA+' / '+r.mB,r.s,r.u,'<b>'+r.sA+'</b>','<b>'+r.sB+'</b>',
            '<span class="'+(r.meanSame?'ok':'no')+'">'+(r.meanSame?'○':'×')+'</span>',
            '<span class="'+(r.sdSame?'ok':'no')+'">'+(r.sdSame?'○':'×')+'</span>',
            r.wider];
  },
  analyze:function(rec){
    var rows=[],meanSame=0,sdDiff=0,match=0,zero=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.meanSame) meanSame++;
      if(!r.sdSame) sdDiff++;
      if(r.wider===r.spreadWider) match++;
      if(r.s===0||r.u===0) zero++;
      rows.push([r.mA+' / '+r.mB, r.s+' / '+r.u, r.sA+' / '+r.sB,
                 '<span class="'+(r.meanSame?'ok':'no')+'">'+(r.meanSame?'○':'×')+'</span>',
                 '<span class="'+(r.sdSame?'ok':'no')+'">'+(r.sdSame?'○':'×')+'</span>',
                 r.wider]);
    }
    var stats=[
      {t:'두 모둠의 평균이 같았던 횟수',big:meanSame+' / '+rec.length,
       p:'평균만 보면 두 모둠을 구별할 수 없다.'},
      {t:'표준편차가 달랐던 횟수',big:sdDiff+' / '+rec.length,
       p:'평균이 같아도 흩어진 정도는 달랐다.'},
      {t:'흩어짐이 큰 쪽이 표준편차도 컸던 횟수',big:match+' / '+rec.length,
       p:zero?('그중 흩어짐이 0인 기록이 '+zero+'개 있었다. 그때 표준편차도 0이다.'):'표준편차가 흩어진 정도를 나타내는지 확인한 결과.'}
    ];
    var concl;
    if(sdDiff===0){
      concl='<b>더 해 보자</b> — 두 모둠의 흩어짐을 다르게(예: 1과 6) 두고 기록해야 차이가 보인다.';
    } else if(meanSame===rec.length&&match===rec.length){
      concl='<b>정리</b> — 두 모둠의 <b>평균이 완전히 같은데도 자료가 퍼진 모습은 전혀 달랐다.</b> '
           +'평균 하나로는 자료를 다 말할 수 없다. 각 값이 평균에서 얼마나 떨어졌는지를 제곱해 평균 낸 것이 분산이고, '
           +'그 제곱근이 <b>표준편차</b>다. 표준편차가 클수록 자료가 넓게 퍼져 있고, 0이면 모든 값이 평균과 같다.';
    } else {
      concl='<b>확인 필요</b> — 평균이나 표준편차가 예상과 다른 기록이 있다.';
    }
    return {head:['평균','흩어짐','표준편차','평균 같음','표준편차 같음','더 퍼진 쪽'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("m3_quadratic_vertex_lab.html",
     "이차함수 실험실 — (x − p)면 어느 쪽으로 옮겨질까?",
     "이차함수 실험실 — (x − p)면 어느 쪽으로 옮겨질까?",
     "y = a(x−p)²+q의 그래프에서 꼭짓점을 직접 찾아 p, −p, q와 대조한다.",
     LAB_QUAD),
    ("m3_trig_ratio_lab.html",
     "삼각비 실험실 — 삼각형이 커지면 비도 커질까?",
     "삼각비 실험실 — 삼각형이 커지면 비도 커질까?",
     "같은 각을 가진 크기가 다른 두 직각삼각형에서 변의 비를 재어 비교한다.",
     LAB_TRIG),
    ("m3_inscribed_angle_lab.html",
     "원주각 실험실 — 점의 위치를 바꾸면 각도 바뀔까?",
     "원주각 실험실 — 점의 위치를 바꾸면 각도 바뀔까?",
     "같은 호에 대한 원주각을 점 P의 위치를 옮겨 가며 재고, 중심각과 비교한다.",
     LAB_INSC),
    ("m3_mean_median_lab.html",
     "대푯값 실험실 — 값 하나가 평균을 흔들 수 있을까?",
     "대푯값 실험실 — 값 하나가 평균을 흔들 수 있을까?",
     "한 값만 크게 바꿔 가며 평균과 중앙값이 각각 얼마나 움직이는지 기록한다.",
     LAB_MED),
    ("m3_standard_deviation_lab.html",
     "표준편차 실험실 — 평균이 같으면 자료도 같을까?",
     "표준편차 실험실 — 평균이 같으면 자료도 같을까?",
     "평균이 같고 퍼진 정도만 다른 두 모둠의 분산과 표준편차를 구해 비교한다.",
     LAB_STD),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c18_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
