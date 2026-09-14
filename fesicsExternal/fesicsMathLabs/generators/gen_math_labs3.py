# -*- coding: utf-8 -*-
"""초등 3-4학년군 '도형과 측정' 실험 6종 — 공통 템플릿 재사용"""
import os, re

OUT = "/mnt/user-data/outputs"
src = open("/home/claude/gen_math_labs.py", encoding="utf-8").read()
TPL = re.search(r'TPL = r"""(.*?)"""\n', src, re.S).group(1)

GEO = r"""
function lbl(ctx,t,x,y,c,sz,al){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
function angDeg(p,q,r){
  var ax=p[0]-q[0], ay=p[1]-q[1], bx=r[0]-q[0], by=r[1]-q[1];
  var d=ax*bx+ay*by, m=Math.sqrt(ax*ax+ay*ay)*Math.sqrt(bx*bx+by*by);
  var c=(m===0)?1:d/m;
  if(c>1)c=1; if(c<-1)c=-1;
  return Math.acos(c)*180/Math.PI;
}
function r1(v){ return Math.round(v*10)/10; }
function box(ctx,x,y,w,h){
  ctx.fillStyle='#f1f6fd';ctx.fillRect(x,y,w,h);
  ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(x,y,w,h);
}
"""

# ============================================================
# 1. 각도기 — 변의 길이와 각의 크기
# ============================================================
LAB_ANGLE = GEO + r"""
var VX=96, VY=306;
var LAB = {
  cw:440, ch:400, cvTitle:'각도기 실험판',
  action:'각도기로 재기',
  hint0:'각의 벌어진 정도와 두 변의 길이를 따로 정할 수 있다. 재 보자.',
  sliders:[
    {id:'ang',label:'벌어진 정도',min:10,max:170,value:40,color:'#2563eb',unit:'칸'},
    {id:'l1',label:'아래 변의 길이',min:30,max:150,value:60,color:'#16a34a',
     fmt:function(v){return (v/20).toFixed(1)+'cm';}},
    {id:'l2',label:'위 변의 길이',min:30,max:150,value:140,color:'#f59e0b',
     fmt:function(v){return (v/20).toFixed(1)+'cm';}}
  ],
  pts:function(S){
    var th=S.ang*Math.PI/180;
    return {v:[VX,VY], p1:[VX+S.l1,VY], p2:[VX+S.l2*Math.cos(th), VY-S.l2*Math.sin(th)]};
  },
  readout:function(S,ran){
    var P=this.pts(S);
    return [{k:'변의 길이',v:(S.l1/20).toFixed(1)+'cm / '+(S.l2/20).toFixed(1)+'cm'},
            {k:'잰 각도',v:ran?(r1(angDeg(P.p1,P.v,P.p2))+'°'):'재 보자'}];
  },
  doneMsg:function(S){
    var P=this.pts(S);
    return '각도기로 재니 '+r1(angDeg(P.p1,P.v,P.p2))+'°였다. 변의 길이를 바꿔서 다시 재 보자.';
  },
  draw:function(ctx,S,t,ran){
    var P=this.pts(S), i;
    var show=(t===null)?0:Math.min(1,t/0.6);
    if(show>0){
      ctx.globalAlpha=0.85*show;
      ctx.beginPath();ctx.arc(VX,VY,116,Math.PI,2*Math.PI);ctx.closePath();
      ctx.fillStyle='#eef4fc';ctx.fill();
      ctx.strokeStyle='#93b4dc';ctx.lineWidth=2;ctx.stroke();
      for(i=0;i<=180;i+=10){
        var a=i*Math.PI/180, big=(i%30===0);
        var r0=big?96:106;
        ctx.beginPath();
        ctx.moveTo(VX+r0*Math.cos(Math.PI+a),VY+r0*Math.sin(Math.PI+a));
        ctx.lineTo(VX+116*Math.cos(Math.PI+a),VY+116*Math.sin(Math.PI+a));
        ctx.strokeStyle='#64748b';ctx.lineWidth=big?2:1;ctx.stroke();
        if(big){
          ctx.fillStyle='#475569';ctx.font='bold 12px sans-serif';ctx.textAlign='center';
          ctx.fillText(i,VX+84*Math.cos(Math.PI+a),VY+84*Math.sin(Math.PI+a)+4);
        }
      }
      ctx.globalAlpha=1;
    }
    var th=S.ang*Math.PI/180;
    ctx.beginPath();ctx.arc(VX,VY,44,-th,0);ctx.lineTo(VX,VY);ctx.closePath();
    ctx.fillStyle='rgba(37,99,235,0.18)';ctx.fill();
    ctx.strokeStyle='#16a34a';ctx.lineWidth=5;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(P.v[0],P.v[1]);ctx.lineTo(P.p1[0],P.p1[1]);ctx.stroke();
    ctx.strokeStyle='#f59e0b';
    ctx.beginPath();ctx.moveTo(P.v[0],P.v[1]);ctx.lineTo(P.p2[0],P.p2[1]);ctx.stroke();
    ctx.lineCap='butt';
    ctx.beginPath();ctx.arc(VX,VY,6,0,Math.PI*2);ctx.fillStyle='#1f2937';ctx.fill();

    lbl(ctx,'변의 길이를 바꿔도 각의 크기는?',24,36,'#1d4ed8',19);
    box(ctx,20,332,400,52);
    var m=r1(angDeg(P.p1,P.v,P.p2));
    lbl(ctx,(t===null)?'아직 재지 않았다':('잰 각도 : '+m+'°     변 '+(S.l1/20).toFixed(1)+'cm · '+(S.l2/20).toFixed(1)+'cm'),
        38,364,'#1f2937',20);
  },
  record:function(S){
    var P=this.pts(S);
    return {ang:S.ang,l1:r1(S.l1/20),l2:r1(S.l2/20),m:r1(angDeg(P.p1,P.v,P.p2)),
            lsum:r1((S.l1+S.l2)/20)};
  },
  headA:['번호','벌어진 정도','아래 변','위 변','잰 각도','두 변 길이 합'],
  rowA:function(r,i){ return [i+1,r.ang,r.l1+'cm',r.l2+'cm','<b>'+r.m+'°</b>',r.lsum+'cm']; },
  analyze:function(rec){
    var rows=[],map={},pairs=0,agree=0,i;
    var longIdx=0,bigIdx=0;
    for(i=0;i<rec.length;i++){
      if(rec[i].lsum>rec[longIdx].lsum) longIdx=i;
      if(rec[i].m>rec[bigIdx].m) bigIdx=i;
    }
    for(i=0;i<rec.length;i++){
      var r=rec[i], k=String(r.ang), note='첫 기록';
      if(map[k]){
        var prev=map[k];
        if(prev.l1!==r.l1||prev.l2!==r.l2){
          pairs++;
          var same=(Math.abs(prev.m-r.m)<0.15);
          if(same) agree++;
          note='<span class="'+(same?'ok':'no')+'">'+(same?'각도 같음':'각도 다름')+'</span>';
        } else { note='같은 조건'; }
      } else { map[k]=r; }
      rows.push([r.ang, r.l1+' / '+r.l2, r.lsum, '<b>'+r.m+'°</b>', note]);
    }
    var lw=(longIdx===bigIdx);
    var stats=[
      {t:'변 길이만 바꾼 짝',big:pairs+'쌍',
       p:pairs?'벌어진 정도는 같고 변 길이만 다른 기록끼리 비교했다.':'같은 벌어진 정도에서 변 길이만 바꿔 기록해 보자.'},
      {t:'그중 각도가 같았던 짝',big:pairs?(agree+' / '+pairs):'비교 없음',
       p:'변을 길게 그려도 잰 각도가 같은지 확인한 결과.'},
      {t:'변이 가장 긴 기록이 각도도 가장 컸나',big:lw?'예':'아니오',
       p:'가장 긴 기록은 '+rec[longIdx].lsum+'cm('+rec[longIdx].m+'°), 가장 큰 각은 '+rec[bigIdx].m+'°였다.'}
    ];
    var concl;
    if(pairs===0){
      concl='<b>더 해 보자</b> — 아직 같은 벌어짐에서 변 길이만 바꾼 기록이 없다. 벌어진 정도를 그대로 두고 변만 길게 늘여 다시 재 보자.';
    } else if(agree===pairs){
      concl='<b>정리</b> — 변을 아무리 길게 그려도 잰 각도는 하나도 달라지지 않았다. '
           +'<b>각의 크기는 두 변이 벌어진 정도</b>이지, 변의 길이가 아니다. 변이 짧은 각이 더 클 수도 있다.';
    } else {
      concl='<b>확인 필요</b> — 같은 벌어짐인데 각도가 다르게 나온 기록이 있다. 값을 다시 확인해 보자.';
    }
    return {head:['벌어진 정도','두 변(cm)','길이 합','잰 각도','같은 벌어짐끼리'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 삼각형 세 각의 합
# ============================================================
LAB_TRI = GEO + r"""
var A=[62,268], B=[382,268];
var LAB = {
  cw:440, ch:430, cvTitle:'삼각형 각 모으기판',
  action:'세 각을 잘라 모으기',
  hint0:'꼭짓점을 옮겨 삼각형 모양을 바꿔 보자. 세 각을 잘라 한 줄로 모아 본다.',
  sliders:[
    {id:'cx',label:'위 꼭짓점 좌우',min:20,max:420,value:180,color:'#2563eb',unit:''},
    {id:'cy',label:'위 꼭짓점 높이',min:40,max:230,value:70,color:'#16a34a',unit:''}
  ],
  angs:function(S){
    var C=[S.cx,S.cy];
    return {a:angDeg(B,A,C), b:angDeg(C,B,A), c:angDeg(A,C,B), C:C};
  },
  readout:function(S,ran){
    var g=this.angs(S);
    return [{k:'세 각',v:r1(g.a)+'° / '+r1(g.b)+'° / '+r1(g.c)+'°'},
            {k:'세 각의 합',v:ran?(r1(g.a+g.b+g.c)+'°'):'모아 보자'}];
  },
  doneMsg:function(S){
    var g=this.angs(S);
    return '세 각을 모으니 딱 한 줄(직선)이 되었다. 합은 '+r1(g.a+g.b+g.c)+'°다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var g=this.angs(S), C=g.C;
    var cols=['#3b82f6','#ef4444','#22c55e'];
    ctx.beginPath();ctx.moveTo(A[0],A[1]);ctx.lineTo(B[0],B[1]);ctx.lineTo(C[0],C[1]);ctx.closePath();
    ctx.fillStyle='#f8fafc';ctx.fill();
    ctx.strokeStyle='#334155';ctx.lineWidth=3;ctx.stroke();
    var show=(t===null)?1:Math.max(0,1-Math.max(0,(t-0.45)/0.25));
    function sector(p,q,r,col,al){
      var a1=Math.atan2(q[1]-p[1],q[0]-p[0]), a2=Math.atan2(r[1]-p[1],r[0]-p[0]);
      var d=a2-a1;
      while(d<=-Math.PI) d+=2*Math.PI;
      while(d>Math.PI) d-=2*Math.PI;
      ctx.globalAlpha=al;
      ctx.beginPath();ctx.moveTo(p[0],p[1]);
      ctx.arc(p[0],p[1],34,a1,a1+d,d<0);
      ctx.closePath();ctx.fillStyle=col;ctx.fill();
      ctx.globalAlpha=1;
    }
    sector(A,B,C,cols[0],0.55*show);
    sector(B,C,A,cols[1],0.55*show);
    sector(C,A,B,cols[2],0.55*show);
    ctx.font='bold 15px sans-serif';ctx.textAlign='center';ctx.fillStyle='#1f2937';
    ctx.fillText(r1(g.a)+'°',A[0]+34,A[1]-14);
    ctx.fillText(r1(g.b)+'°',B[0]-38,B[1]-14);
    ctx.fillText(r1(g.c)+'°',C[0],C[1]+40);
    ctx.textAlign='left';

    var MX=220, MY=352;
    ctx.strokeStyle='#94a3b8';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(MX-170,MY);ctx.lineTo(MX+170,MY);ctx.stroke();
    if(t!==null && t>0.45){
      var q=Math.min(1,(t-0.45)/0.55);
      var arr=[g.a,g.b,g.c], acc=0;
      for(var i=0;i<3;i++){
        var span=arr[i]*Math.PI/180;
        var start=Math.PI+acc, end=start+span;
        var lim=Math.PI+q*Math.PI;
        if(start>=lim) break;
        if(end>lim) end=lim;
        ctx.beginPath();ctx.moveTo(MX,MY);
        ctx.arc(MX,MY,66,start,end);
        ctx.closePath();
        ctx.globalAlpha=0.65;ctx.fillStyle=cols[i];ctx.fill();ctx.globalAlpha=1;
        ctx.strokeStyle='#fff';ctx.lineWidth=1.5;ctx.stroke();
        acc+=span;
      }
    } else {
      lbl(ctx,'여기에 세 각을 모아 본다',MX,MY-14,'#94a3b8',16,'center');
    }
    box(ctx,20,376,400,44);
    lbl(ctx,(t===null)?'아직 모으지 않았다':(r1(g.a)+'° + '+r1(g.b)+'° + '+r1(g.c)+'° = '+r1(g.a+g.b+g.c)+'°'),
        38,404,'#1f2937',20);
  },
  record:function(S){
    var g=this.angs(S);
    var sum=g.a+g.b+g.c;
    var kind=(Math.max(g.a,g.b,g.c)>90.5)?'둔각삼각형':((Math.max(g.a,g.b,g.c)>89.5)?'직각삼각형':'예각삼각형');
    return {a:r1(g.a),b:r1(g.b),c:r1(g.c),sum:r1(sum),kind:kind};
  },
  headA:['번호','각 1','각 2','각 3','세 각의 합','종류'],
  rowA:function(r,i){ return [i+1,r.a+'°',r.b+'°',r.c+'°','<b>'+r.sum+'°</b>',r.kind]; },
  analyze:function(rec){
    var rows=[],ok=0,kinds={},mn=999,mx=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i], good=(Math.abs(r.sum-180)<0.25);
      if(good) ok++;
      kinds[r.kind]=true;
      if(r.sum<mn) mn=r.sum;
      if(r.sum>mx) mx=r.sum;
      rows.push([r.a+'° · '+r.b+'° · '+r.c+'°', r.kind, '<b>'+r.sum+'°</b>',
                 '<span class="'+(good?'ok':'no')+'">'+(good?'○':'×')+'</span>']);
    }
    var kn=0,names=[]; for(var k in kinds){ kn++; names.push(k); }
    var stats=[
      {t:'세 각의 합이 180°였던 횟수',big:ok+' / '+rec.length,p:'모은 각이 정확히 한 줄(직선)이 되었는지 확인한 결과.'},
      {t:'합의 가장 작은 값 ~ 가장 큰 값',big:mn+'° ~ '+mx+'°',p:'모양을 아무리 바꿔도 합은 움직이지 않았다.'},
      {t:'시험해 본 삼각형 종류',big:kn+'가지',p:names.join(', ')}
    ];
    var concl;
    if(ok===rec.length){
      concl='<b>정리</b> — 뾰족하든 넓적하든, 예각·직각·둔각 어느 삼각형이든 세 각을 잘라 모으면 언제나 <b>딱 한 줄, 180°</b>였다. '
           +'그래서 두 각만 알면 나머지 한 각은 180°에서 빼서 구할 수 있다.';
    } else {
      concl='<b>확인 필요</b> — 180°가 아닌 기록이 있다. 꼭짓점이 밑변 위에 겹치지 않았는지 확인해 보자.';
    }
    return {head:['세 각','종류','합','180°인가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 사각형 네 각의 합
# ============================================================
LAB_QUAD = GEO + r"""
var P1=[54,98], P2=[386,98], YB=316;
var LAB = {
  cw:440, ch:430, cvTitle:'사각형 각 실험판',
  action:'대각선으로 잘라 보기',
  hint0:'아래 두 꼭짓점을 옮겨 사각형 모양을 바꿔 보자.',
  sliders:[
    {id:'dx',label:'왼쪽 아래 꼭짓점',min:26,max:190,value:96,color:'#2563eb',unit:''},
    {id:'cx',label:'오른쪽 아래 꼭짓점',min:200,max:414,value:330,color:'#16a34a',unit:''}
  ],
  quad:function(S){ return [P1,P2,[S.cx,YB],[S.dx,YB]]; },
  angs:function(S){
    var q=this.quad(S), r=[];
    for(var i=0;i<4;i++){ r.push(angDeg(q[(i+3)%4],q[i],q[(i+1)%4])); }
    return r;
  },
  readout:function(S,ran){
    var a=this.angs(S);
    return [{k:'네 각',v:r1(a[0])+'/'+r1(a[1])+'/'+r1(a[2])+'/'+r1(a[3])},
            {k:'네 각의 합',v:ran?(r1(a[0]+a[1]+a[2]+a[3])+'°'):'잘라 보자'}];
  },
  doneMsg:function(S){
    var a=this.angs(S);
    return '대각선 하나로 삼각형 2개가 되었다. 네 각의 합은 '+r1(a[0]+a[1]+a[2]+a[3])+'°다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var q=this.quad(S), a=this.angs(S), i;
    var split=(t===null)?0:Math.min(1,t/0.6);
    var off=split*16;
    ctx.beginPath();
    ctx.moveTo(q[0][0]-off,q[0][1]-off);ctx.lineTo(q[1][0],q[1][1]);ctx.lineTo(q[2][0],q[2][1]);ctx.closePath();
    ctx.fillStyle='rgba(59,130,246,0.20)';ctx.fill();
    ctx.strokeStyle='#2563eb';ctx.lineWidth=2.6;ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(q[0][0]+off*0.4,q[0][1]+off);ctx.lineTo(q[2][0]+off*0.4,q[2][1]+off);ctx.lineTo(q[3][0]+off*0.4,q[3][1]+off);ctx.closePath();
    ctx.fillStyle='rgba(34,197,94,0.20)';ctx.fill();
    ctx.strokeStyle='#16a34a';ctx.lineWidth=2.6;ctx.stroke();
    ctx.font='bold 15px sans-serif';ctx.textAlign='center';ctx.fillStyle='#1f2937';
    var lp=[[q[0][0]+26,q[0][1]+26],[q[1][0]-28,q[1][1]+26],[q[2][0]-24,q[2][1]-16],[q[3][0]+26,q[3][1]-16]];
    for(i=0;i<4;i++){ ctx.fillText(r1(a[i])+'°',lp[i][0],lp[i][1]); }
    ctx.textAlign='left';
    lbl(ctx,'사각형을 대각선으로 자르면?',24,44,'#1d4ed8',19);
    if(split>0){
      lbl(ctx,'삼각형 1 : 180°',24,68,'#2563eb',17);
      lbl(ctx,'삼각형 2 : 180°',170,68,'#16a34a',17);
    }
    box(ctx,20,352,400,64);
    var s=a[0]+a[1]+a[2]+a[3];
    lbl(ctx,(t===null)?'아직 자르지 않았다':('네 각의 합 : '+r1(s)+'°'),38,382,'#1f2937',21);
    lbl(ctx,(t===null)?'네 각의 합은 얼마일까?':'180° × 2 = 360°',38,408,'#52627a',18);
  },
  record:function(S){
    var a=this.angs(S);
    var s=a[0]+a[1]+a[2]+a[3];
    return {a:r1(a[0]),b:r1(a[1]),c:r1(a[2]),d:r1(a[3]),sum:r1(s)};
  },
  headA:['번호','각 1','각 2','각 3','각 4','네 각의 합','삼각형 2개의 합'],
  rowA:function(r,i){ return [i+1,r.a+'°',r.b+'°',r.c+'°',r.d+'°','<b>'+r.sum+'°</b>','180×2 = 360°']; },
  analyze:function(rec){
    var rows=[],ok=0,mn=9999,mx=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i], good=(Math.abs(r.sum-360)<0.3);
      if(good) ok++;
      if(r.sum<mn) mn=r.sum;
      if(r.sum>mx) mx=r.sum;
      rows.push([r.a+'° · '+r.b+'° · '+r.c+'° · '+r.d+'°','<b>'+r.sum+'°</b>',360,
                 '<span class="'+(good?'ok':'no')+'">'+(good?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'네 각의 합이 360°였던 횟수',big:ok+' / '+rec.length,p:'사각형 모양을 바꿔 가며 확인한 결과.'},
      {t:'합의 가장 작은 값 ~ 가장 큰 값',big:mn+'° ~ '+mx+'°',p:'꼭짓점을 옮겨도 합은 변하지 않았다.'},
      {t:'삼각형으로 나눈 개수',big:'2개',p:'대각선 하나로 삼각형 2개가 되고, 180° × 2 = 360°다.'}
    ];
    var concl;
    if(ok===rec.length){
      concl='<b>정리</b> — 어떤 사각형이든 네 각의 합은 <b>360°</b>였다. 대각선 하나를 그으면 삼각형 2개로 나뉘고, '
           +'삼각형 하나의 세 각이 180°이므로 180° × 2 = 360°가 된다. 외워서가 아니라 잘라 보면 알 수 있다.';
    } else {
      concl='<b>확인 필요</b> — 360°가 아닌 기록이 있다. 사각형이 찌그러져 겹치지 않았는지 확인해 보자.';
    }
    return {head:['네 각','합','예상','360°인가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 원 — 반지름과 지름
# ============================================================
LAB_CIRCLE = GEO + r"""
var OX=220, OY=196;
var LAB = {
  cw:440, ch:400, cvTitle:'컴퍼스 실험판',
  action:'원을 그리고 재기',
  hint0:'컴퍼스를 벌린 만큼 원을 그리고, 원 위 한 점까지의 거리를 재 보자.',
  sliders:[
    {id:'r',label:'컴퍼스를 벌린 길이',min:30,max:150,value:100,color:'#2563eb',
     fmt:function(v){return (v/20).toFixed(1)+'cm';}},
    {id:'th',label:'원 위 점의 위치',min:0,max:350,value:40,color:'#f59e0b',unit:'칸'}
  ],
  readout:function(S,ran){
    var t=S.th*Math.PI/180;
    var px=OX+S.r*Math.cos(t), py=OY-S.r*Math.sin(t);
    var d=Math.sqrt((px-OX)*(px-OX)+(py-OY)*(py-OY));
    return [{k:'중심에서 점까지',v:ran?((d/20).toFixed(1)+'cm'):'재 보자'},
            {k:'지름',v:ran?((2*S.r/20).toFixed(1)+'cm'):'재 보자'}];
  },
  doneMsg:function(S){
    return '중심에서 점까지는 '+(S.r/20).toFixed(1)+'cm, 원을 가로지른 지름은 '+(2*S.r/20).toFixed(1)+'cm였다. 점의 위치를 바꿔 다시 재 보자.';
  },
  draw:function(ctx,S,t,ran){
    var th=S.th*Math.PI/180;
    var px=OX+S.r*Math.cos(th), py=OY-S.r*Math.sin(th);
    var qx=OX-S.r*Math.cos(th), qy=OY+S.r*Math.sin(th);
    var grow=(t===null)?0:Math.min(1,t/0.55);
    ctx.beginPath();ctx.arc(OX,OY,S.r,-Math.PI/2,-Math.PI/2+2*Math.PI*Math.max(grow,0.0001));
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.stroke();
    if(t===null){
      ctx.setLineDash([5,6]);ctx.beginPath();ctx.arc(OX,OY,S.r,0,2*Math.PI);
      ctx.strokeStyle='#cbd5e1';ctx.lineWidth=2;ctx.stroke();ctx.setLineDash([]);
    }
    var meas=(t===null)?0:Math.max(0,Math.min(1,(t-0.55)/0.45));
    if(meas>0){
      ctx.beginPath();ctx.moveTo(qx,qy);ctx.lineTo(qx+(px-qx)*meas,qy+(py-qy)*meas);
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=4;ctx.stroke();
    }
    ctx.beginPath();ctx.moveTo(OX,OY);ctx.lineTo(px,py);
    ctx.strokeStyle='#16a34a';ctx.lineWidth=4;ctx.stroke();
    ctx.beginPath();ctx.arc(OX,OY,6,0,Math.PI*2);ctx.fillStyle='#1f2937';ctx.fill();
    ctx.beginPath();ctx.arc(px,py,7,0,Math.PI*2);ctx.fillStyle='#f59e0b';ctx.fill();
    ctx.strokeStyle='#b45309';ctx.lineWidth=2;ctx.stroke();
    lbl(ctx,'중심',OX+10,OY+22,'#334155',15);
    lbl(ctx,'반지름 '+(S.r/20).toFixed(1)+'cm',(OX+px)/2+8,(OY+py)/2-8,'#15803d',15);
    lbl(ctx,'컴퍼스를 '+(S.r/20).toFixed(1)+'cm 벌려 그린 원',24,36,'#1d4ed8',19);
    box(ctx,20,348,400,44);
    var d=Math.sqrt((px-OX)*(px-OX)+(py-OY)*(py-OY));
    lbl(ctx,(t===null)?'아직 그리지 않았다':('중심~점 '+(d/20).toFixed(1)+'cm     지름 '+(2*S.r/20).toFixed(1)+'cm'),
        38,376,'#1f2937',20);
  },
  record:function(S){
    var th=S.th*Math.PI/180;
    var px=OX+S.r*Math.cos(th), py=OY-S.r*Math.sin(th);
    var qx=OX-S.r*Math.cos(th), qy=OY+S.r*Math.sin(th);
    var d=Math.sqrt((px-OX)*(px-OX)+(py-OY)*(py-OY))/20;
    var dia=Math.sqrt((px-qx)*(px-qx)+(py-qy)*(py-qy))/20;
    return {r:r1(S.r/20),th:S.th,d:r1(d),dia:r1(dia),ratio:r1(dia/(S.r/20))};
  },
  headA:['번호','컴퍼스를 벌린 길이','점의 위치','중심~점 거리','지름','지름 ÷ 반지름'],
  rowA:function(r,i){ return [i+1,r.r+'cm',r.th,'<b>'+r.d+'cm</b>',r.dia+'cm',r.ratio]; },
  analyze:function(rec){
    var rows=[],same=0,two=0,ths={},rs={};
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var a=(Math.abs(r.d-r.r)<0.05), b=(Math.abs(r.ratio-2)<0.02);
      if(a) same++;
      if(b) two++;
      ths[r.th]=true; rs[r.r]=true;
      rows.push([r.r+'cm', r.th, r.d+'cm',
                 '<span class="'+(a?'ok':'no')+'">'+(a?'○':'×')+'</span>',
                 r.dia+'cm', r.ratio,
                 '<span class="'+(b?'ok':'no')+'">'+(b?'○':'×')+'</span>']);
    }
    var tn=0,rn=0; for(var k in ths) tn++; for(var k2 in rs) rn++;
    var stats=[
      {t:'중심~점 거리 = 컴퍼스를 벌린 길이',big:same+' / '+rec.length,
       p:'점을 원 위 어디에 잡아도 거리가 같은지 확인한 결과.'},
      {t:'지름 ÷ 반지름 = 2',big:two+' / '+rec.length,p:'원을 가로지른 길이와 반지름을 비교했다.'},
      {t:'시험한 점의 위치 / 원 크기',big:tn+'곳 / '+rn+'가지',
       p:tn>1?'위치를 바꿔도 결과가 같았다.':'점의 위치를 바꿔 더 확인해 보자.'}
    ];
    var concl;
    if(same===rec.length && two===rec.length){
      concl='<b>정리</b> — 원 위의 점을 어디에 잡아도 중심까지의 거리는 <b>항상 같았다.</b> 그것이 반지름이다. '
           +'또 중심을 지나 원을 가로지른 지름은 언제나 <b>반지름의 2배</b>였다. 컴퍼스가 원을 그릴 수 있는 이유가 여기 있다.';
    } else {
      concl='<b>확인 필요</b> — 거리나 비가 다르게 나온 기록이 있다. 값을 다시 확인해 보자.';
    }
    return {head:['반지름','점의 위치','중심~점','반지름과 같은가?','지름','지름÷반지름','2인가?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 밀기·뒤집기·돌리기
# ============================================================
LAB_MOVE = GEO + r"""
var BASE=[[0,0],[3,0],[3,1],[1,1],[1,3],[0,3]];
var U=34, OXX=60, OYY=76, CXU=1.5, CYU=1.5;
var OPS=['밀기','좌우 뒤집기','위아래 뒤집기','시계 방향 90° 돌리기'];
function apply(pts,op){
  var out=[],i,p;
  for(i=0;i<pts.length;i++){
    p=pts[i];
    if(op===0) out.push([p[0]+2,p[1]]);
    else if(op===1) out.push([2*CXU-p[0],p[1]]);
    else if(op===2) out.push([p[0],2*CYU-p[1]]);
    else out.push([CXU-(p[1]-CYU),CYU+(p[0]-CXU)]);
  }
  return out;
}
function applyN(op,k){
  var p=BASE,i;
  for(i=0;i<k;i++){ p=apply(p,op); }
  return p;
}
function perim(p){
  var s=0,i;
  for(i=0;i<p.length;i++){
    var a=p[i], b=p[(i+1)%p.length];
    s+=Math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]));
  }
  return s;
}
function area(p){
  var s=0,i;
  for(i=0;i<p.length;i++){
    var a=p[i], b=p[(i+1)%p.length];
    s+=a[0]*b[1]-b[0]*a[1];
  }
  return Math.abs(s)/2;
}
function normKey(p){
  var arr=[],i;
  for(i=0;i<p.length;i++){ arr.push(Math.round(p[i][0]*100)/100+','+Math.round(p[i][1]*100)/100); }
  arr.sort();
  return arr.join(';');
}
function poly(ctx,p,fill,stroke,dash){
  ctx.beginPath();
  for(var i=0;i<p.length;i++){
    var x=OXX+p[i][0]*U, y=OYY+p[i][1]*U;
    if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
  }
  ctx.closePath();
  if(dash) ctx.setLineDash([6,5]);
  if(fill){ ctx.fillStyle=fill; ctx.fill(); }
  ctx.strokeStyle=stroke;ctx.lineWidth=3;ctx.stroke();
  ctx.setLineDash([]);
}

var LAB = {
  cw:440, ch:420, cvTitle:'도형 이동판',
  action:'차례로 이동하기',
  hint0:'어떤 이동을 몇 번 할지 정해 보자. 모양과 크기가 변하는지 확인한다.',
  sliders:[
    {id:'op',label:'이동 방법',min:0,max:3,value:1,color:'#2563eb',
     fmt:function(v){return OPS[v];}},
    {id:'k',label:'반복 횟수',min:1,max:4,value:1,color:'#16a34a',unit:'번'}
  ],
  readout:function(S,ran){
    var p=applyN(S.op,S.k);
    return [{k:'둘레',v:ran?(r1(perim(p))+'cm'):'이동해 보자'},
            {k:'넓이',v:ran?(r1(area(p))+'cm²'):'이동해 보자'}];
  },
  doneMsg:function(S){
    var p=applyN(S.op,S.k);
    var back=(normKey(p)===normKey(BASE));
    return OPS[S.op]+'를 '+S.k+'번 했다. 둘레 '+r1(perim(p))+'cm, 넓이 '+r1(area(p))+'cm²로 처음과 같다.'
      +(back?' 게다가 처음 자리로 돌아왔다!':'');
  },
  draw:function(ctx,S,t,ran){
    var i,j;
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=0;i<=12;i++){
      ctx.beginPath();ctx.moveTo(OXX-40+i*U,40);ctx.lineTo(OXX-40+i*U,300);ctx.stroke();
    }
    for(j=0;j<=7;j++){
      ctx.beginPath();ctx.moveTo(20,40+j*U);ctx.lineTo(420,40+j*U);ctx.stroke();
    }
    poly(ctx,BASE,'rgba(148,163,184,0.14)','#94a3b8',true);
    var step=(t===null)?0:Math.min(S.k,Math.floor(t*S.k)+1);
    if(t!==null && t>=1) step=S.k;
    if(step>0){
      var p=applyN(S.op,step);
      poly(ctx,p,'rgba(245,158,11,0.28)','#d97706',false);
    }
    lbl(ctx,OPS[S.op]+'  ×  '+S.k+'번',24,32,'#1d4ed8',19);
    lbl(ctx,(t===null)?'점선 = 처음 도형':('점선 = 처음 도형   /   진한 색 = '+step+'번 이동한 도형'),24,326,'#52627a',16);
    box(ctx,20,338,400,74);
    var pf=applyN(S.op,S.k);
    var back=(normKey(pf)===normKey(BASE));
    lbl(ctx,(t===null)?'둘레 · 넓이는 어떻게 될까?':('둘레 '+r1(perim(pf))+'cm    넓이 '+r1(area(pf))+'cm²'),38,368,'#1f2937',20);
    lbl(ctx,(t===null)?'처음 도형 : 둘레 '+r1(perim(BASE))+'cm, 넓이 '+r1(area(BASE))+'cm²'
        :(back?'처음 자리로 돌아왔다':'처음과 다른 자리에 있다'),38,396,back?'#15803d':'#52627a',18);
  },
  record:function(S){
    var p=applyN(S.op,S.k);
    return {op:S.op,name:OPS[S.op],k:S.k,per:r1(perim(p)),ar:r1(area(p)),
            back:(normKey(p)===normKey(BASE)),
            p0:r1(perim(BASE)),a0:r1(area(BASE))};
  },
  headA:['번호','이동 방법','횟수','둘레','넓이','처음 자리로?'],
  rowA:function(r,i){
    return [i+1,r.name,r.k+'번',r.per+'cm',r.ar+'cm²',
            '<span class="'+(r.back?'ok':'no')+'">'+(r.back?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],pk=0,ak=0,backs=[],ops={};
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var a=(Math.abs(r.per-r.p0)<0.01), b=(Math.abs(r.ar-r.a0)<0.01);
      if(a) pk++;
      if(b) ak++;
      if(r.back) backs.push(r.name+' '+r.k+'번');
      ops[r.name]=true;
      rows.push([r.name+' '+r.k+'번', r.per+'cm', r.p0+'cm',
                 '<span class="'+(a?'ok':'no')+'">'+(a?'○':'×')+'</span>',
                 r.ar+'cm²',
                 '<span class="'+(b?'ok':'no')+'">'+(b?'○':'×')+'</span>',
                 r.back?'<span class="ok">돌아옴</span>':'-']);
    }
    var on=0; for(var k in ops) on++;
    var stats=[
      {t:'둘레가 그대로였던 횟수',big:pk+' / '+rec.length,p:'이동해도 변의 길이 합이 변하지 않았는지 확인했다.'},
      {t:'넓이가 그대로였던 횟수',big:ak+' / '+rec.length,p:'이동해도 도형이 차지한 넓이가 같았는지 확인했다.'},
      {t:'처음 자리로 돌아온 경우',big:backs.length+'개',
       p:backs.length?backs.join(', '):'뒤집기를 2번, 돌리기를 4번 해 보면 어떻게 될까?'}
    ];
    var concl;
    if(pk===rec.length && ak===rec.length){
      concl='<b>정리</b> — 밀거나 뒤집거나 돌려도 <b>둘레와 넓이는 한 번도 변하지 않았다.</b> '
           +'위치와 방향만 바뀔 뿐 도형 자체는 그대로다. 그래서 뒤집기를 2번, 90° 돌리기를 4번 하면 처음 도형과 완전히 겹친다.';
    } else {
      concl='<b>확인 필요</b> — 둘레나 넓이가 달라진 기록이 있다. 값을 다시 확인해 보자.';
    }
    return {head:['이동','둘레','처음 둘레','같은가?','넓이','같은가?','제자리'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 6. 시계 바늘이 이루는 각
# ============================================================
LAB_CLOCK = GEO + r"""
var CX=220, CY=192, R=140;
function hourAng(h,m){ return (h%12)*30 + m*0.5; }
function minAng(m){ return m*6; }
function gap(a,b){ var d=Math.abs(a-b); if(d>180) d=360-d; return d; }
var LAB = {
  cw:440, ch:420, cvTitle:'시계판',
  action:'두 바늘 사이 각 재기',
  hint0:'시각을 정하고 두 바늘이 이루는 각을 재 보자.',
  sliders:[
    {id:'h',label:'시',min:1,max:12,value:3,color:'#2563eb',unit:'시'},
    {id:'m',label:'분',min:0,max:55,step:5,value:15,color:'#dc2626',unit:'분'}
  ],
  readout:function(S,ran){
    return [{k:'시각',v:S.h+'시 '+S.m+'분'},
            {k:'두 바늘 사이 각',v:ran?(r1(gap(hourAng(S.h,S.m),minAng(S.m)))+'°'):'재 보자'}];
  },
  doneMsg:function(S){
    var real=gap(hourAng(S.h,S.m),minAng(S.m));
    var naive=gap((S.h%12)*30,minAng(S.m));
    if(S.m===0) return '정각이라 시침이 숫자에 정확히 있다. 각은 '+r1(real)+'°. 다른 시각도 재 보자.';
    return '실제 각은 '+r1(real)+'°다. 시침이 '+S.h+'에 그대로 멈춰 있다고 보면 '+r1(naive)+'°가 나오는데, 시침도 '+r1(S.m*0.5)+'° 움직였다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var i;
    ctx.beginPath();ctx.arc(CX,CY,R,0,Math.PI*2);
    ctx.fillStyle='#fff';ctx.fill();
    ctx.strokeStyle='#334155';ctx.lineWidth=4;ctx.stroke();
    for(i=0;i<60;i++){
      var a=(i*6-90)*Math.PI/180, big=(i%5===0);
      ctx.beginPath();
      ctx.moveTo(CX+(R-(big?14:7))*Math.cos(a),CY+(R-(big?14:7))*Math.sin(a));
      ctx.lineTo(CX+R*Math.cos(a),CY+R*Math.sin(a));
      ctx.strokeStyle=big?'#475569':'#cbd5e1';ctx.lineWidth=big?3:1.4;ctx.stroke();
    }
    ctx.font='bold 19px sans-serif';ctx.textAlign='center';ctx.fillStyle='#1f2937';
    for(i=1;i<=12;i++){
      var a2=(i*30-90)*Math.PI/180;
      ctx.fillText(i,CX+(R-34)*Math.cos(a2),CY+(R-34)*Math.sin(a2)+7);
    }
    ctx.textAlign='left';
    var ha=hourAng(S.h,S.m), ma=minAng(S.m);
    var e=(t===null)?0:Math.min(1,t/0.6);
    if(e>0){
      var a1=(Math.min(ha,ma)-90)*Math.PI/180;
      var sw=gap(ha,ma)*Math.PI/180;
      var wide=(Math.abs(ha-ma)>180);
      ctx.beginPath();ctx.moveTo(CX,CY);
      if(wide) ctx.arc(CX,CY,72,(Math.max(ha,ma)-90)*Math.PI/180,(Math.max(ha,ma)-90)*Math.PI/180+sw*e);
      else ctx.arc(CX,CY,72,a1,a1+sw*e);
      ctx.closePath();
      ctx.fillStyle='rgba(37,99,235,0.20)';ctx.fill();
    }
    function hand(ang,len,w,col){
      var a=(ang-90)*Math.PI/180;
      ctx.beginPath();ctx.moveTo(CX,CY);ctx.lineTo(CX+len*Math.cos(a),CY+len*Math.sin(a));
      ctx.strokeStyle=col;ctx.lineWidth=w;ctx.lineCap='round';ctx.stroke();ctx.lineCap='butt';
    }
    hand(ha,80,9,'#2563eb');
    hand(ma,118,6,'#dc2626');
    ctx.beginPath();ctx.arc(CX,CY,8,0,Math.PI*2);ctx.fillStyle='#1f2937';ctx.fill();
    lbl(ctx,S.h+'시 '+S.m+'분',24,34,'#1d4ed8',20);
    box(ctx,20,344,400,68);
    var real=gap(ha,ma), naive=gap((S.h%12)*30,ma);
    lbl(ctx,(t===null)?'두 바늘 사이 각은 몇 도일까?':('두 바늘 사이 각 : '+r1(real)+'°'),38,374,'#1f2937',21);
    lbl(ctx,(t===null)?('시침은 '+S.h+'에 정확히 있을까?'):('시침 '+r1(ha)+'°   분침 '+r1(ma)+'°'),38,400,'#52627a',18);
  },
  record:function(S){
    var ha=hourAng(S.h,S.m), ma=minAng(S.m);
    return {h:S.h,m:S.m,ha:r1(ha),ma:r1(ma),real:r1(gap(ha,ma)),
            naive:r1(gap((S.h%12)*30,ma)),
            onNum:(S.m===0),
            shift:r1(ha-(S.h%12)*30)};
  },
  headA:['번호','시각','시침 각도','분침 각도','두 바늘 사이 각','시침이 숫자 위?','시침이 움직인 정도'],
  rowA:function(r,i){
    return [i+1,r.h+'시 '+r.m+'분',r.ha+'°',r.ma+'°','<b>'+r.real+'°</b>',
            '<span class="'+(r.onNum?'ok':'no')+'">'+(r.onNum?'○':'×')+'</span>',r.shift+'°'];
  },
  analyze:function(rec){
    var rows=[],on=0,naiveOk=0,notOclock=0,maxGap=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var eq=(Math.abs(r.real-r.naive)<0.05);
      if(r.onNum) on++; else notOclock++;
      if(eq) naiveOk++;
      var d=Math.abs(r.real-r.naive);
      if(d>maxGap) maxGap=r1(d);
      rows.push([r.h+'시 '+r.m+'분', r.naive+'°', '<b>'+r.real+'°</b>', r1(Math.abs(r.real-r.naive))+'°',
                 '<span class="'+(eq?'ok':'no')+'">'+(eq?'○':'×')+'</span>',
                 r.shift+'°']);
    }
    var stats=[
      {t:'시침이 숫자에 정확히 있던 시각',big:on+' / '+rec.length,
       p:on===rec.length?'모두 정각이었다. 정각이 아닌 시각도 재 보자.':'분이 0일 때만 시침이 숫자 위에 있었다.'},
      {t:'“시침은 숫자에 고정” 계산이 맞은 횟수',big:naiveOk+' / '+rec.length,
       p:'시침이 움직이지 않는다고 보고 구한 각이 실제와 같았던 횟수.'},
      {t:'가장 크게 어긋난 정도',big:maxGap+'°',
       p:notOclock?'분침이 돌아가는 동안 시침도 조금씩 움직였기 때문이다.':'정각이 아닌 시각을 기록해 보자.'}
    ];
    var concl;
    if(notOclock===0){
      concl='<b>더 해 보자</b> — 아직 정각만 기록했다. 3시 15분처럼 분이 0이 아닌 시각을 재 보면 시침의 비밀이 보인다.';
    } else if(naiveOk<rec.length){
      concl='<b>정리</b> — 시침은 숫자 위에 가만히 있지 않았다. 1시간에 30°를 도니까 <b>1분에 0.5°씩</b> 조금씩 움직인다. '
           +'3시 15분에 시침이 3에 그대로 있다고 보면 분침과 겹쳐 0°여야 하지만, 실제로는 7.5° 벌어져 있다. '
           +'시침 각도 = (시 × 30) + (분 × 0.5)로 구해야 한다.';
    } else {
      concl='<b>확인 필요</b> — 정각이 아닌데도 두 계산이 같게 나온 기록이 있다. 값을 다시 확인해 보자.';
    }
    return {head:['시각','시침 고정으로 계산','실제 각','차이','같은가?','시침이 움직인 정도'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("elem34_angle_measure_lab.html",
     "각도기 실험실 — 변이 길면 큰 각일까?",
     "각도기 실험실 — 변이 길면 큰 각일까?",
     "벌어진 정도는 그대로 두고 두 변의 길이만 바꿔 가며 각도를 재고, 무엇이 각의 크기를 정하는지 확인한다.",
     LAB_ANGLE),
    ("elem34_triangle_angle_sum_lab.html",
     "삼각형 각 실험실 — 세 각을 모으면 무엇이 될까?",
     "삼각형 각 실험실 — 세 각을 모으면 무엇이 될까?",
     "꼭짓점을 옮겨 삼각형 모양을 바꾸고, 세 각을 잘라 한 줄로 모아 합을 기록한다.",
     LAB_TRI),
    ("elem34_quadrilateral_angle_sum_lab.html",
     "사각형 각 실험실 — 네 각의 합은 왜 360°일까?",
     "사각형 각 실험실 — 네 각의 합은 왜 360°일까?",
     "사각형을 대각선으로 잘라 삼각형 두 개로 나누고, 네 각의 합을 직접 기록해 확인한다.",
     LAB_QUAD),
    ("elem34_circle_radius_lab.html",
     "컴퍼스 실험실 — 원 위의 점은 모두 같은 거리일까?",
     "컴퍼스 실험실 — 원 위의 점은 모두 같은 거리일까?",
     "컴퍼스를 벌린 만큼 원을 그리고, 원 위 여러 점까지의 거리와 지름을 재어 기록한다.",
     LAB_CIRCLE),
    ("elem34_shape_motion_lab.html",
     "도형 이동 실험실 — 뒤집으면 도형이 달라질까?",
     "도형 이동 실험실 — 뒤집으면 도형이 달라질까?",
     "도형을 밀고 뒤집고 돌리면서 둘레와 넓이가 변하는지, 언제 처음 자리로 돌아오는지 기록한다.",
     LAB_MOVE),
    ("elem34_clock_angle_lab.html",
     "시계 실험실 — 3시 15분에 시침은 3에 있을까?",
     "시계 실험실 — 3시 15분에 시침은 3에 있을까?",
     "시각을 바꿔 가며 두 바늘이 이루는 각을 재고, 시침이 숫자에 고정되어 있다는 생각을 확인한다.",
     LAB_CLOCK),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html, "토큰 누수: " + fname
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c3_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
