# -*- coding: utf-8 -*-
"""중3 보강 5종 (2)"""
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
# 1. 접현각
# ============================================================
LAB_TCH = BASE + r"""
var CX=220, CY=200, R=130;
function pt(deg){ var r=deg*Math.PI/180; return [CX+R*Math.cos(r),CY+R*Math.sin(r)]; }
var LAB = {
  cw:440, ch:430, cvTitle:'접현각 판',
  action:'세 각 재기',
  hint0:'호의 중심각과, 원 위 점 B의 위치를 정해 보자. T는 접점이다.',
  sliders:[
    {id:'th',label:'호 TA의 중심각',min:30,max:300,value:100,color:'#2563eb',unit:'°'},
    {id:'u',label:'점 B의 위치',min:5,max:95,value:50,color:'#f59e0b',
     fmt:function(v){return '남은 호의 '+v+'%';}}
  ],
  calc:function(S){
    var T=pt(0);
    var A=pt(S.th);
    var rest=360-S.th;
    var B=pt(S.th+rest*S.u/100);
    var Tan=[T[0],T[1]+60];
    var tch=angDeg(Tan,T,A);
    var ins=angDeg(A,B,T);
    return {T:T,A:A,B:B,Tan:Tan,tch:tch,ins:ins,cen:S.th,
            half:S.th/2};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'중심각',v:S.th+'°'},
            {k:'접현각',v:ran?(r1(c.tch)+'°'):'재 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '접현각 '+r1(c.tch)+'°, 원주각 '+r1(c.ins)+'°, 중심각의 절반 '+r1(c.half)+'°. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    ctx.beginPath();ctx.arc(CX,CY,R,0,Math.PI*2);
    ctx.strokeStyle='#94a3b8';ctx.lineWidth=2;ctx.stroke();
    ctx.beginPath();ctx.arc(CX,CY,R,0,S.th*Math.PI/180);
    ctx.strokeStyle='#dc2626';ctx.lineWidth=5;ctx.stroke();
    ctx.strokeStyle='#334155';ctx.lineWidth=3;
    ctx.beginPath();ctx.moveTo(c.T[0],c.T[1]-90);ctx.lineTo(c.T[0],c.T[1]+90);ctx.stroke();
    lbl(ctx,'접선',c.T[0]+8,c.T[1]+86,'#334155',13);
    var grow=(t===null)?0:Math.min(1,t);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;
    ctx.beginPath();ctx.moveTo(c.T[0],c.T[1]);
    ctx.lineTo(c.T[0]+(c.A[0]-c.T[0])*grow,c.T[1]+(c.A[1]-c.T[1])*grow);ctx.stroke();
    if(grow>0.5){
      var g=(grow-0.5)/0.5;
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=2.6;
      ctx.beginPath();ctx.moveTo(c.B[0],c.B[1]);
      ctx.lineTo(c.B[0]+(c.T[0]-c.B[0])*g,c.B[1]+(c.T[1]-c.B[1])*g);
      ctx.moveTo(c.B[0],c.B[1]);
      ctx.lineTo(c.B[0]+(c.A[0]-c.B[0])*g,c.B[1]+(c.A[1]-c.B[1])*g);ctx.stroke();
    }
    [[c.T,'T','#334155'],[c.A,'A','#1d4ed8'],[c.B,'B','#b45309']].forEach(function(q){
      ctx.beginPath();ctx.arc(q[0][0],q[0][1],6,0,Math.PI*2);
      ctx.fillStyle=q[2];ctx.fill();
      lbl(ctx,q[1],q[0][0]+9,q[0][1]-8,q[2],15);
    });
    ctx.beginPath();ctx.arc(CX,CY,4,0,Math.PI*2);ctx.fillStyle='#1f2937';ctx.fill();
    lbl(ctx,'빨간 호 TA 에 대한 각들',24,32,'#1d4ed8',17);
    box(ctx,20,336,400,84);
    lbl(ctx,'중심각 '+S.th+'°      절반 '+r1(c.half)+'°',38,368,'#52627a',17);
    lbl(ctx,(t===null)?'접현각과 원주각은 어떤 관계일까?':('접현각 '+r1(c.tch)+'°      원주각 '+r1(c.ins)+'°'),
        38,402,'#1f2937',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {th:S.th,u:S.u,tch:r1(c.tch),ins:r1(c.ins),half:r1(c.half),
            eq:(Math.abs(c.tch-c.ins)<0.05),
            halfOk:(Math.abs(c.tch-c.half)<0.05)};
  },
  headA:['번호','중심각','B의 위치','접현각','원주각','같나?','중심각의 절반','같나?'],
  rowA:function(r,i){
    return [i+1,r.th+'°',r.u+'%','<b>'+r.tch+'°</b>',r.ins+'°',
            '<span class="'+(r.eq?'ok':'no')+'">'+(r.eq?'○':'×')+'</span>',
            r.half+'°',
            '<span class="'+(r.halfOk?'ok':'no')+'">'+(r.halfOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],eq=0,half=0,g={},pairs=0,agree=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.eq) eq++;
      if(r.halfOk) half++;
      var note='첫 기록';
      if(g[r.th]!==undefined){
        pairs++;
        var s=(Math.abs(g[r.th]-parseFloat(r.ins))<0.05);
        if(s) agree++;
        note='<span class="'+(s?'ok':'no')+'">'+(s?'원주각 같음':'원주각 다름')+'</span>';
      } else { g[r.th]=parseFloat(r.ins); }
      rows.push([r.th+'°', r.u+'%', '<b>'+r.tch+'°</b>', r.ins+'°',
                 '<span class="'+(r.eq?'ok':'no')+'">'+(r.eq?'○':'×')+'</span>',
                 r.half+'°',
                 '<span class="'+(r.halfOk?'ok':'no')+'">'+(r.halfOk?'○':'×')+'</span>', note]);
    }
    var stats=[
      {t:'접현각 = 원주각',big:eq+' / '+rec.length,p:'같은 호에 대한 두 각을 비교한 결과.'},
      {t:'접현각 = 중심각의 절반',big:half+' / '+rec.length,p:'접선을 «지나가 버린 현»으로 볼 수 있다.'},
      {t:'같은 호에서 B만 옮긴 짝',big:pairs+'쌍',
       p:pairs?('그중 원주각이 같았던 것 '+agree+'쌍.'):'중심각을 고정하고 B만 옮겨 기록해 보자.'}
    ];
    var concl;
    if(eq===rec.length&&half===rec.length){
      concl='<b>정리</b> — 접선과 현이 이루는 각은 <b>그 현이 잘라낸 호에 대한 원주각과 언제나 같았고</b>, 중심각의 절반이었다. '
           +'점 B를 어디에 두어도 원주각이 같으니 접현각도 그대로다. '
           +'접선을 «두 점이 겹칠 때까지 가까워진 현»으로 보면, 접현각도 원주각의 한 경우임을 알 수 있다.';
    } else {
      concl='<b>확인 필요</b> — 두 각이 다른 기록이 있다.';
    }
    return {head:['중심각','B 위치','접현각','원주각','같나?','절반','같나?','같은 호끼리'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 원에 내접하는 사각형
# ============================================================
LAB_CYC = BASE + r"""
var CX=220, CY=200, R=130;
function pt(deg){ var r=deg*Math.PI/180; return [CX+R*Math.cos(r),CY+R*Math.sin(r)]; }
var LAB = {
  cw:440, ch:430, cvTitle:'내접사각형 판',
  action:'네 내각 재기',
  hint0:'원 위 네 점의 위치를 정해 보자. A는 고정이다.',
  sliders:[
    {id:'b',label:'B의 위치',min:30,max:120,value:80,color:'#2563eb',unit:'°'},
    {id:'c',label:'C의 위치',min:130,max:230,value:180,color:'#16a34a',unit:'°'},
    {id:'d',label:'D의 위치',min:240,max:340,value:280,color:'#f59e0b',unit:'°'}
  ],
  calc:function(S){
    var A=pt(0), B=pt(S.b), C=pt(S.c), D=pt(S.d);
    var a1=angDeg(D,A,B), a2=angDeg(A,B,C), a3=angDeg(B,C,D), a4=angDeg(C,D,A);
    return {A:A,B:B,C:C,D:D,a1:a1,a2:a2,a3:a3,a4:a4,
            s13:a1+a3,s24:a2+a4,tot:a1+a2+a3+a4};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'네 내각',v:ran?(r1(c.a1)+' / '+r1(c.a2)+' / '+r1(c.a3)+' / '+r1(c.a4)):'재 보자'},
            {k:'A + C',v:ran?(r1(c.s13)+'°'):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'A+C = '+r1(c.s13)+'°, B+D = '+r1(c.s24)+'°.  네 각의 합은 '+r1(c.tot)+'°다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    ctx.beginPath();ctx.arc(CX,CY,R,0,Math.PI*2);
    ctx.strokeStyle='#94a3b8';ctx.lineWidth=2;ctx.stroke();
    var pts=[c.A,c.B,c.C,c.D];
    ctx.beginPath();
    for(var i=0;i<4;i++){ if(i===0) ctx.moveTo(pts[i][0],pts[i][1]); else ctx.lineTo(pts[i][0],pts[i][1]); }
    ctx.closePath();
    ctx.fillStyle='rgba(37,99,235,0.10)';ctx.fill();
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    var names=['A','B','C','D'];
    var angs=[c.a1,c.a2,c.a3,c.a4];
    var cols=['#dc2626','#2563eb','#dc2626','#2563eb'];
    for(i=0;i<4;i++){
      ctx.beginPath();ctx.arc(pts[i][0],pts[i][1],6,0,Math.PI*2);
      ctx.fillStyle='#334155';ctx.fill();
      lbl(ctx,names[i],pts[i][0]+10,pts[i][1]-8,'#334155',15);
      if(grow>=1){
        var dx=(CX-pts[i][0])*0.22, dy=(CY-pts[i][1])*0.22;
        lbl(ctx,r1(angs[i])+'°',pts[i][0]+dx,pts[i][1]+dy,cols[i],14,'center');
      }
    }
    ctx.beginPath();ctx.arc(CX,CY,4,0,Math.PI*2);ctx.fillStyle='#94a3b8';ctx.fill();
    lbl(ctx,'원 위 네 점으로 만든 사각형',24,32,'#1d4ed8',17);
    box(ctx,20,336,400,84);
    lbl(ctx,(t===null)?'마주보는 두 각을 더하면?':('A + C = '+r1(c.s13)+'°      B + D = '+r1(c.s24)+'°'),
        38,368,'#1f2937',18);
    lbl(ctx,(t===null)?'':('네 각의 합 = '+r1(c.tot)+'°'),38,402,'#52627a',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {b:S.b,cc:S.c,d:S.d,
            a1:r1(c.a1),a2:r1(c.a2),a3:r1(c.a3),a4:r1(c.a4),
            s13:r1(c.s13),s24:r1(c.s24),tot:r1(c.tot),
            ok13:(Math.abs(c.s13-180)<0.1),
            ok24:(Math.abs(c.s24-180)<0.1),
            tot360:(Math.abs(c.tot-360)<0.1)};
  },
  headA:['번호','B, C, D','네 내각','A + C','180°?','B + D','180°?','네 각의 합'],
  rowA:function(r,i){
    return [i+1,r.b+', '+r.cc+', '+r.d,r.a1+'/'+r.a2+'/'+r.a3+'/'+r.a4,
            '<b>'+r.s13+'°</b>',
            '<span class="'+(r.ok13?'ok':'no')+'">'+(r.ok13?'○':'×')+'</span>',
            '<b>'+r.s24+'°</b>',
            '<span class="'+(r.ok24?'ok':'no')+'">'+(r.ok24?'○':'×')+'</span>',
            r.tot+'°'];
  },
  analyze:function(rec){
    var rows=[],o13=0,o24=0,tot=0,shapes={},sn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.ok13) o13++;
      if(r.ok24) o24++;
      if(r.tot360) tot++;
      var k=r.b+','+r.cc+','+r.d;
      if(!shapes[k]){ shapes[k]=true; sn++; }
      rows.push([r.b+', '+r.cc+', '+r.d, r.a1+'/'+r.a2+'/'+r.a3+'/'+r.a4,
                 '<b>'+r.s13+'°</b>',
                 '<span class="'+(r.ok13?'ok':'no')+'">'+(r.ok13?'○':'×')+'</span>',
                 '<b>'+r.s24+'°</b>',
                 '<span class="'+(r.ok24?'ok':'no')+'">'+(r.ok24?'○':'×')+'</span>',
                 r.tot+'°']);
    }
    var stats=[
      {t:'A + C = 180°',big:o13+' / '+rec.length,p:'마주보는 두 각의 합을 잰 결과.'},
      {t:'B + D = 180°',big:o24+' / '+rec.length,p:'다른 쌍도 확인한 결과.'},
      {t:'서로 다른 사각형',big:sn+'가지',
       p:'네 각의 합이 360°였던 기록 '+tot+'개. 사각형이면 원 위에 없어도 360°다.'}
    ];
    var concl;
    if(sn<3){
      concl='<b>더 해 보자</b> — 점의 위치를 여러 가지로 바꿔 <b>모양이 아주 다른 사각형</b>도 기록해 보자.';
    } else if(o13===rec.length&&o24===rec.length){
      concl='<b>정리</b> — 원에 내접하는 사각형은 모양을 아무리 바꿔도 <b>마주보는 두 각의 합이 언제나 180°</b>였다. '
           +'각 내각이 마주보는 호에 대한 원주각이고, 두 호를 합치면 원 전체(360°)가 되기 때문이다. '
           +'네 각의 합 360°는 모든 사각형에서 성립하지만, <b>마주보는 각의 합 180°는 원 위에 있을 때만</b> 성립한다.';
    } else {
      concl='<b>확인 필요</b> — 합이 180°가 아닌 기록이 있다.';
    }
    return {head:['B, C, D','네 내각','A+C','180°?','B+D','180°?','합'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 원 밖의 한 점에서 그은 두 할선
# ============================================================
LAB_SEC2 = BASE + r"""
var CX=250, CY=210, R=110;
function hit(P,th){
  var ux=Math.cos(th), uy=Math.sin(th);
  var ox=P[0]-CX, oy=P[1]-CY;
  var b=ox*ux+oy*uy;
  var cc=ox*ox+oy*oy-R*R;
  var disc=b*b-cc;
  if(disc<0) return null;
  var s=Math.sqrt(disc);
  var t1=-b-s, t2=-b+s;
  if(t1<0||t2<0) return null;
  return {A:[P[0]+ux*t1,P[1]+uy*t1],B:[P[0]+ux*t2,P[1]+uy*t2],t1:t1,t2:t2};
}
var LAB = {
  cw:440, ch:430, cvTitle:'두 할선 판',
  action:'두 할선 긋고 재기',
  hint0:'원 밖 점 P의 거리와 두 할선의 방향을 정해 보자.',
  sliders:[
    {id:'d',label:'중심에서 P까지',min:130,max:230,value:180,color:'#2563eb',unit:''},
    {id:'t1',label:'첫 번째 할선 각',min:-30,max:30,value:-12,color:'#dc2626',unit:'°'},
    {id:'t2',label:'두 번째 할선 각',min:-30,max:30,value:14,color:'#f59e0b',unit:'°'}
  ],
  calc:function(S){
    var P=[CX-S.d,CY];
    var h1=hit(P,S.t1*Math.PI/180), h2=hit(P,S.t2*Math.PI/180);
    var pw=S.d*S.d-R*R;
    return {P:P,h1:h1,h2:h2,pw:pw,
            p1:h1?(h1.t1*h1.t2):null,
            p2:h2?(h2.t1*h2.t2):null,
            tan:Math.sqrt(pw)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'PA × PB',v:(ran&&c.p1!==null)?r1(c.p1/400):'재 보자'},
            {k:'PC × PD',v:(ran&&c.p2!==null)?r1(c.p2/400):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.p1===null||c.p2===null) return '할선이 원을 지나지 않는다. 각을 줄여 보자.';
    return 'PA×PB = '+r1(c.p1/400)+', PC×PD = '+r1(c.p2/400)+'.  접선 길이의 제곱은 '+r1(c.pw/400)+'이다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    ctx.beginPath();ctx.arc(CX,CY,R,0,Math.PI*2);
    ctx.strokeStyle='#94a3b8';ctx.lineWidth=2.5;ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    function sec(h,col,names){
      if(!h) return;
      ctx.strokeStyle=col;ctx.lineWidth=3;
      ctx.beginPath();ctx.moveTo(c.P[0],c.P[1]);
      ctx.lineTo(c.P[0]+(h.B[0]-c.P[0])*grow,c.P[1]+(h.B[1]-c.P[1])*grow);ctx.stroke();
      if(grow>=1){
        [[h.A,names[0]],[h.B,names[1]]].forEach(function(q){
          ctx.beginPath();ctx.arc(q[0][0],q[0][1],5,0,Math.PI*2);ctx.fillStyle=col;ctx.fill();
          lbl(ctx,q[1],q[0][0]+7,q[0][1]-6,col,13);
        });
      }
    }
    sec(c.h1,'#dc2626',['A','B']);
    sec(c.h2,'#f59e0b',['C','D']);
    ctx.beginPath();ctx.arc(c.P[0],c.P[1],7,0,Math.PI*2);
    ctx.fillStyle='#1f2937';ctx.fill();
    lbl(ctx,'P',c.P[0]-6,c.P[1]-14,'#1f2937',16);
    ctx.beginPath();ctx.arc(CX,CY,4,0,Math.PI*2);ctx.fillStyle='#94a3b8';ctx.fill();
    lbl(ctx,'원 밖의 점에서 그은 두 할선',24,32,'#1d4ed8',17);
    box(ctx,20,336,400,84);
    if(c.p1===null||c.p2===null){
      lbl(ctx,'할선이 원을 지나지 않는다. 각을 줄여 보자.',38,382,'#b91c1c',17);
      return;
    }
    lbl(ctx,(t===null)?'두 곱은 같을까?':('PA × PB = '+r1(c.p1/400)+'      PC × PD = '+r1(c.p2/400)),
        38,368,'#1f2937',17);
    lbl(ctx,(t===null)?'':('중심거리² − 반지름² = '+r1(c.pw/400)+'      (접선 길이 '+r2(c.tan/20)+')'),
        38,402,'#15803d',16);
  },
  record:function(S){
    var c=this.calc(S);
    if(c.p1===null||c.p2===null) return {bad:true,d:r2(S.d/20)};
    return {bad:false,d:r2(S.d/20),t1:S.t1,t2:S.t2,
            p1:r1(c.p1/400),p2:r1(c.p2/400),pw:r1(c.pw/400),
            same:(Math.abs(c.p1-c.p2)<0.6),
            powOk:(Math.abs(c.p1-c.pw)<0.6),
            tan:r2(c.tan/20)};
  },
  headA:['번호','중심~P','두 각','PA×PB','PC×PD','같나?','거리²−반지름²','일치?','접선 길이'],
  rowA:function(r,i){
    if(r.bad) return [i+1,r.d,'-','원을 지나지 않음','-','-','-','-','-'];
    return [i+1,r.d,r.t1+'° / '+r.t2+'°','<b>'+r.p1+'</b>',r.p2,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            r.pw,
            '<span class="'+(r.powOk?'ok':'no')+'">'+(r.powOk?'○':'×')+'</span>',
            r.tan];
  },
  analyze:function(rec){
    var rows=[],valid=0,same=0,pow=0,g={},pairs=0,agree=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.bad){ rows.push([r.d,'-','원을 지나지 않음','-','-','-']); continue; }
      valid++;
      if(r.same) same++;
      if(r.powOk) pow++;
      var note='첫 기록';
      if(g[r.d]!==undefined){
        pairs++;
        var s=(Math.abs(g[r.d]-parseFloat(r.p1))<0.6);
        if(s) agree++;
        note='<span class="'+(s?'ok':'no')+'">'+(s?'값 같음':'값 다름')+'</span>';
      } else { g[r.d]=parseFloat(r.p1); }
      rows.push([r.d, r.t1+'° / '+r.t2+'°', r.p1+' / '+r.p2,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 r.pw,
                 '<span class="'+(r.powOk?'ok':'no')+'">'+(r.powOk?'○':'×')+'</span>', note]);
    }
    var stats=[
      {t:'PA×PB = PC×PD',big:same+' / '+valid,p:'같은 점에서 그은 두 할선을 비교한 결과.'},
      {t:'그 값 = 거리² − 반지름²',big:pow+' / '+valid,p:'P의 위치만으로 값이 정해지는지 확인했다.'},
      {t:'같은 P에서 방향만 바꾼 짝',big:pairs+'쌍',
       p:pairs?('그중 값이 같았던 것 '+agree+'쌍.'):'거리를 고정하고 각만 바꿔 기록해 보자.'}
    ];
    var concl;
    if(valid===0){
      concl='<b>더 해 보자</b> — 할선이 원을 지나도록 각을 작게 잡아 보자.';
    } else if(same===valid&&pow===valid){
      concl='<b>정리</b> — 원 밖 한 점에서 그은 두 할선에서도 <b>PA × PB 와 PC × PD 가 언제나 같았다.</b> '
           +'그 값은 <b>중심거리² − 반지름²</b> 로 P의 위치만으로 정해졌고, 이는 <b>접선 길이의 제곱</b>과 같다. '
           +'원 안의 두 현에서 본 관계가 원 밖에서도 그대로 이어진다. △PAC ∽ △PDB 인 것이 근거다.';
    } else {
      concl='<b>확인 필요</b> — 두 곱이 다른 기록이 있다.';
    }
    return {head:['중심~P','두 각','두 곱','같나?','거리²−반지름²','일치?','같은 P끼리'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 편차의 합
# ============================================================
LAB_DEV = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'편차 판',
  action:'편차 구해 더하기',
  hint0:'네 사람의 점수를 정해 보자. 다섯 번째는 10으로 고정이다.',
  sliders:[
    {id:'a',label:'① 점수',min:1,max:20,value:6,color:'#60a5fa',unit:''},
    {id:'b',label:'② 점수',min:1,max:20,value:9,color:'#60a5fa',unit:''},
    {id:'c',label:'③ 점수',min:1,max:20,value:12,color:'#60a5fa',unit:''},
    {id:'d',label:'④ 점수',min:1,max:20,value:18,color:'#60a5fa',unit:''}
  ],
  calc:function(S){
    var v=[S.a,S.b,S.c,S.d,10];
    var s=0,i;
    for(i=0;i<5;i++) s+=v[i];
    var m=s/5;
    var dev=[],sum=0,abs=0,sq=0;
    for(i=0;i<5;i++){ var e=v[i]-m; dev.push(e); sum+=e; abs+=Math.abs(e); sq+=e*e; }
    return {v:v,m:m,dev:dev,sum:sum,abs:abs,sq:sq,
            varr:sq/5,sd:Math.sqrt(sq/5)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'평균',v:r2(c.m)},
            {k:'편차의 합',v:ran?r3(c.sum):'더해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '편차의 합은 '+r3(c.sum)+'이다. 절댓값의 합은 '+r2(c.abs)+', 제곱의 합은 '+r2(c.sq)+'다. 점수를 바꿔 다시 해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var GX=44, GY=250, GW=356, GH=150;
    var lo=0, hi=21;
    function px(v){ return GX+GW*(v-lo)/(hi-lo); }
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+GW,GY);ctx.stroke();
    for(i=0;i<=20;i+=5){
      ctx.fillStyle='#94a3b8';ctx.font='11px sans-serif';ctx.textAlign='center';
      ctx.fillText(i,px(i),GY+18);
    }
    ctx.textAlign='left';
    ctx.strokeStyle='#7c3aed';ctx.lineWidth=3;
    ctx.beginPath();ctx.moveTo(px(c.m),GY-GH-6);ctx.lineTo(px(c.m),GY+8);ctx.stroke();
    lbl(ctx,'평균 '+r2(c.m),px(c.m),GY-GH-12,'#6d28d9',14,'center');
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*5);
    for(i=0;i<5;i++){
      var y=GY-24-i*26;
      var e=c.dev[i];
      if(i<shown){
        ctx.strokeStyle=(e>=0)?'#16a34a':'#dc2626';ctx.lineWidth=6;
        ctx.beginPath();ctx.moveTo(px(c.m),y);ctx.lineTo(px(c.v[i]),y);ctx.stroke();
        lbl(ctx,(e>0?'+':'')+r1(e),px(c.v[i])+((e>=0)?8:-38),y+5,(e>=0)?'#15803d':'#b91c1c',13);
      }
      ctx.beginPath();ctx.arc(px(c.v[i]),y,5,0,Math.PI*2);
      ctx.fillStyle=(i===4)?'#f59e0b':'#2563eb';ctx.fill();
    }
    lbl(ctx,'자료 : '+c.v.join(', '),24,32,'#1d4ed8',17);
    lbl(ctx,'초록 = 평균보다 큼,  빨강 = 평균보다 작음',24,56,'#52627a',13);
    box(ctx,20,286,400,132);
    lbl(ctx,'평균 '+r2(c.m),38,318,'#6d28d9',18);
    lbl(ctx,(t===null)?'편차를 모두 더하면?':('편차의 합 = '+r3(c.sum)),38,352,'#1f2937',20);
    lbl(ctx,(t===null)?'':('절댓값의 합 '+r2(c.abs)+'      제곱의 합 '+r2(c.sq)),38,386,'#52627a',17);
    lbl(ctx,(t===null)?'':('분산 '+r2(c.varr)+'      표준편차 '+r2(c.sd)),38,412,'#15803d',15);
  },
  record:function(S){
    var c=this.calc(S);
    return {v:c.v.join(', '),m:r2(c.m),
            sum:r3(c.sum),abs:r2(c.abs),sq:r2(c.sq),
            varr:r2(c.varr),sd:r2(c.sd),
            zero:(Math.abs(c.sum)<1e-9),
            absZero:(Math.abs(c.abs)<1e-9),
            allSame:(c.sq===0)};
  },
  headA:['번호','자료','평균','편차의 합','0인가?','절댓값의 합','0인가?','제곱의 합','분산','표준편차'],
  rowA:function(r,i){
    return [i+1,r.v,r.m,'<b>'+r.sum+'</b>',
            '<span class="'+(r.zero?'ok':'no')+'">'+(r.zero?'○':'×')+'</span>',
            r.abs,
            '<span class="'+(r.absZero?'ok':'no')+'">'+(r.absZero?'○':'×')+'</span>',
            r.sq,r.varr,r.sd];
  },
  analyze:function(rec){
    var rows=[],zero=0,absZero=0,allSame=0,mx=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.zero) zero++;
      if(r.absZero){ absZero++; }
      if(r.allSame) allSame++;
      if(parseFloat(r.abs)>mx) mx=parseFloat(r.abs);
      rows.push([r.v, r.m, '<b>'+r.sum+'</b>',
                 '<span class="'+(r.zero?'ok':'no')+'">'+(r.zero?'○':'×')+'</span>',
                 r.abs,
                 '<span class="'+(r.absZero?'ok':'no')+'">'+(r.absZero?'○':'×')+'</span>',
                 r.sq, r.sd]);
    }
    var stats=[
      {t:'편차의 합 = 0',big:zero+' / '+rec.length,
       p:'평균보다 큰 만큼과 작은 만큼이 정확히 상쇄된다.'},
      {t:'절댓값의 합도 0이었던 횟수',big:absZero+' / '+rec.length,
       p:'가장 컸던 절댓값의 합은 '+mx+'. 흩어진 정도는 0이 아니다.'},
      {t:'모든 값이 같았던 기록',big:allSame+'개',
       p:allSame?'그때만 제곱의 합도 0이다.':'다섯 값을 모두 10으로 맞춰 보자.'}
    ];
    var concl;
    if(zero===rec.length&&absZero===allSame){
      concl='<b>정리</b> — 편차의 합은 자료를 아무리 바꿔도 <b>언제나 0</b>이었다. '
           +'평균은 «위로 넘친 만큼과 아래로 모자란 만큼이 맞아떨어지는 자리»이기 때문이다. '
           +'그래서 <b>편차를 그냥 더해서는 흩어진 정도를 잴 수 없다.</b> '
           +'대신 절댓값이나 제곱을 씌워 더하는데, 제곱을 쓴 것이 분산이고 그 제곱근이 표준편차다.';
    } else {
      concl='<b>확인 필요</b> — 편차의 합이 0이 아닌 기록이 있다.';
    }
    return {head:['자료','평균','편차의 합','0인가?','절댓값 합','0인가?','제곱 합','표준편차'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 산점도의 이상값
# ============================================================
LAB_OUT = BASE + r"""
var BASEP=[[1,2.2],[2,2.8],[3,3.4],[4,4.1],[5,4.6],[6,5.4],[7,5.9],[8,6.6],[9,7.1]];
function corr(p){
  var n=p.length,i,sx=0,sy=0;
  for(i=0;i<n;i++){ sx+=p[i][0]; sy+=p[i][1]; }
  var mx=sx/n,my=sy/n,num=0,dx=0,dy=0;
  for(i=0;i<n;i++){
    num+=(p[i][0]-mx)*(p[i][1]-my);
    dx+=(p[i][0]-mx)*(p[i][0]-mx);
    dy+=(p[i][1]-my)*(p[i][1]-my);
  }
  if(dx===0||dy===0) return 0;
  return num/Math.sqrt(dx*dy);
}
var LAB = {
  cw:440, ch:430, cvTitle:'이상값 판',
  action:'점 하나 더 넣기',
  hint0:'아홉 점은 그대로 두고, 열 번째 점의 위치만 정해 보자.',
  sliders:[
    {id:'ox',label:'열 번째 점의 x',min:1,max:20,value:18,color:'#dc2626',unit:''},
    {id:'oy',label:'열 번째 점의 y',min:1,max:20,value:2,color:'#f87171',unit:''}
  ],
  calc:function(S){
    var all=BASEP.slice();
    all.push([S.ox,S.oy]);
    var r0=corr(BASEP), r1v=corr(all);
    function dir(r){ return (r>0.2)?'양':((r<-0.2)?'음':'거의 없음'); }
    return {all:all,r0:r0,r1:r1v,d0:dir(r0),d1:dir(r1v),
            flip:(dir(r0)!==dir(r1v))};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'아홉 점의 경향',v:c.d0+' ('+r2(c.r0)+')'},
            {k:'열 점의 경향',v:ran?(c.d1+' ('+r2(c.r1)+')'):'넣어 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '경향의 세기가 '+r2(c.r0)+' 에서 '+r2(c.r1)+' 로 바뀌었다. '+(c.flip?'방향까지 달라졌다!':'방향은 그대로다.')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var GX=56, GY=320, GW=340, GH=250;
    function px(v){ return GX+GW*v/21; }
    function py(v){ return GY-GH*v/21; }
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=5;i<=20;i+=5){
      ctx.beginPath();ctx.moveTo(GX,py(i));ctx.lineTo(GX+GW,py(i));ctx.stroke();
      ctx.beginPath();ctx.moveTo(px(i),GY);ctx.lineTo(px(i),GY-GH);ctx.stroke();
    }
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+GW,GY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX,GY-GH);ctx.stroke();
    for(i=0;i<BASEP.length;i++){
      ctx.beginPath();ctx.arc(px(BASEP[i][0]),py(BASEP[i][1]),6,0,Math.PI*2);
      ctx.fillStyle='#2563eb';ctx.fill();
      ctx.strokeStyle='#fff';ctx.lineWidth=1.6;ctx.stroke();
    }
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      ctx.beginPath();ctx.arc(px(S.ox),py(S.oy),8*grow,0,Math.PI*2);
      ctx.fillStyle='#dc2626';ctx.fill();
      ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
    }
    if(grow>=1){
      lbl(ctx,(c.d0==='양')?'↗':'→',GX+GW-30,GY-GH+22,'#2563eb',20);
      lbl(ctx,(c.d1==='양')?'↗':((c.d1==='음')?'↘':'→'),GX+GW-30,GY-GH+48,
          c.flip?'#dc2626':'#94a3b8',20);
    }
    lbl(ctx,'파랑 아홉 점 + 빨강 한 점',24,32,'#1d4ed8',17);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'점 하나가 경향을 바꿀 수 있을까?':('아홉 점 '+r2(c.r0)+' ('+c.d0+')  →  열 점 '+r2(c.r1)+' ('+c.d1+')'),
        38,376,'#1f2937',17);
    lbl(ctx,(t===null)?'':(c.flip?'방향이 뒤집혔다':'방향은 그대로지만 세기가 달라졌다'),
        38,406,c.flip?'#b91c1c':'#52627a',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {ox:S.ox,oy:S.oy,
            r0:r2(c.r0),r1:r2(c.r1),d0:c.d0,d1:c.d1,
            flip:c.flip,
            gap:r2(Math.abs(c.r1-c.r0)),
            near:(S.ox<=10&&Math.abs(S.oy-(S.ox*0.62+1.6))<1.2)};
  },
  headA:['번호','열 번째 점','아홉 점의 세기','열 점의 세기','차이','아홉 점 방향','열 점 방향','뒤집혔나?'],
  rowA:function(r,i){
    return [i+1,'('+r.ox+', '+r.oy+')',r.r0,'<b>'+r.r1+'</b>',r.gap,r.d0,r.d1,
            '<span class="'+(r.flip?'no':'ok')+'">'+(r.flip?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],flip=0,near=0,nearFlip=0,mx=0,mxp='';
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.flip) flip++;
      if(r.near){ near++; if(r.flip) nearFlip++; }
      if(parseFloat(r.gap)>mx){ mx=parseFloat(r.gap); mxp='('+r.ox+', '+r.oy+')'; }
      rows.push(['('+r.ox+', '+r.oy+')', r.r0, '<b>'+r.r1+'</b>', r.gap, r.d0+' → '+r.d1,
                 '<span class="'+(r.flip?'no':'ok')+'">'+(r.flip?'뒤집힘':'그대로')+'</span>']);
    }
    var stats=[
      {t:'방향이 뒤집힌 기록',big:flip+' / '+rec.length,
       p:flip?'점 하나가 전체 경향을 바꿨다.':'멀리 떨어진 점을 넣어 보자.'},
      {t:'흐름에 맞는 자리에 넣은 기록',big:near+'개',
       p:near?('그중 뒤집힌 것 '+nearFlip+'개.'):'다른 점들과 같은 흐름 위에도 놓아 보자.'},
      {t:'세기가 가장 많이 바뀐 경우',big:mx+'',p:mxp?('점 '+mxp):''}
    ];
    var concl;
    if(flip===0){
      concl='<b>더 해 보자</b> — 열 번째 점을 (18, 2)처럼 <b>흐름에서 크게 벗어난 자리</b>에 놓아 보자.';
    } else {
      concl='<b>정리</b> — 아홉 점은 뚜렷한 양의 관계였는데, <b>멀리 떨어진 점 하나만 더해도 경향이 크게 흔들렸고 방향이 뒤집히기도 했다</b>('+flip+'번). '
           +'반대로 흐름에 맞는 자리에 넣으면 거의 달라지지 않았다. '
           +'그래서 산점도를 읽을 때는 <b>동떨어진 점이 있는지 먼저 살펴야</b> 한다. '
           +'그런 점은 잘못 적힌 값일 수도 있고, 특별한 사정이 있는 진짜 값일 수도 있어 함부로 지우면 안 된다.';
    }
    return {head:['열 번째 점','아홉 점','열 점','차이','방향 변화','뒤집힘?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("m3_tangent_chord_lab.html",
     "접현각 실험실 — 접선과 현이 이루는 각은?",
     "접현각 실험실 — 접선과 현이 이루는 각은?",
     "같은 호에 대한 접현각과 원주각을 재어 비교하고, 중심각과의 관계를 확인한다.",
     LAB_TCH),
    ("m3_cyclic_quadrilateral_lab.html",
     "내접사각형 실험실 — 마주보는 각을 더하면?",
     "내접사각형 실험실 — 마주보는 각을 더하면?",
     "원 위 네 점의 위치를 바꿔 가며 네 내각을 재고 마주보는 각의 합을 기록한다.",
     LAB_CYC),
    ("m3_secant_lab.html",
     "할선 실험실 — 원 밖에서도 곱이 같을까?",
     "할선 실험실 — 원 밖에서도 곱이 같을까?",
     "원 밖 한 점에서 두 할선을 긋고 PA×PB와 PC×PD를 재어 비교한다.",
     LAB_SEC2),
    ("m3_deviation_sum_lab.html",
     "편차 실험실 — 편차를 그냥 더하면 될까?",
     "편차 실험실 — 편차를 그냥 더하면 될까?",
     "각 값의 편차를 구해 더해 보고, 절댓값과 제곱을 씌운 합과 비교한다.",
     LAB_DEV),
    ("m3_outlier_lab.html",
     "이상값 실험실 — 점 하나가 경향을 바꿀 수 있을까?",
     "이상값 실험실 — 점 하나가 경향을 바꿀 수 있을까?",
     "아홉 점은 그대로 두고 열 번째 점의 자리만 바꿔 가며 산점도의 경향을 기록한다.",
     LAB_OUT),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c40_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
