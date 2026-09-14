# -*- coding: utf-8 -*-
"""중1 보강 5종 (2)"""
import os, re, random

OUT = "/mnt/user-data/outputs"
src = open("/home/claude/gen_math_labs.py", encoding="utf-8").read()
TPL = re.search(r'TPL = r"""(.*?)"""\n', src, re.S).group(1)

random.seed(777)
DATA = sorted(max(41, min(98, int(random.gauss(68, 13)))) for _ in range(20))
DATA_JS = "var DATA=" + str(DATA).replace(" ", "") + ";"

BASE = r"""
function lbl(ctx,t,x,y,c,sz,al){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
function box(ctx,x,y,w,h){ctx.fillStyle='#f1f6fd';ctx.fillRect(x,y,w,h);ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(x,y,w,h);}
function r1(v){return Math.round(v*10)/10;}
function r2(v){return Math.round(v*100)/100;}
function r3(v){return Math.round(v*1000)/1000;}
"""

# ============================================================
# 1. 삼각형의 결정조건
# ============================================================
LAB_DET = BASE + r"""
var KINDS=['두 변과 끼인각','두 변과 끼이지 않은 각'];
var LAB = {
  cw:440, ch:430, cvTitle:'삼각형 작도판',
  action:'만들 수 있는 삼각형 찾기',
  hint0:'조건의 종류와 두 변, 각을 정해 보자.',
  sliders:[
    {id:'kind',label:'조건',min:0,max:1,value:1,color:'#2563eb',fmt:function(v){return KINDS[v];}},
    {id:'A',label:'주어진 각',min:20,max:150,value:40,color:'#f59e0b',unit:'°'},
    {id:'c',label:'각에 붙은 변 c',min:3,max:10,value:8,color:'#16a34a',unit:''},
    {id:'a',label:'다른 변 a',min:1,max:12,value:6,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var rad=S.A*Math.PI/180;
    if(S.kind===0) return {n:1,h:null,note:'두 변 사이의 각이라 꼭짓점이 하나로 정해진다'};
    var h=S.c*Math.sin(rad);
    var n;
    if(S.a<h-1e-9) n=0;
    else if(Math.abs(S.a-h)<1e-9) n=1;
    else if(S.a<S.c-1e-9) n=2;
    else n=1;
    return {n:n,h:h,note:(n===0)?'변이 너무 짧아 닿지 않는다':((n===2)?'두 곳에서 닿는다':'한 곳에서만 닿는다')};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'조건',v:KINDS[S.kind]},
            {k:'만들 수 있는 삼각형',v:ran?(c.n+'개'):'찾아보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '만들 수 있는 삼각형은 '+c.n+'개다. '+c.note+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var U=Math.min(30,300/Math.max(S.c,S.a,6));
    var OX=80, OY=320;
    var rad=S.A*Math.PI/180;
    var grow=(t===null)?0:Math.min(1,t);
    ctx.strokeStyle='#94a3b8';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(OX,OY);ctx.lineTo(OX+340,OY);ctx.stroke();
    var Cp=[OX+S.c*U*Math.cos(rad),OY-S.c*U*Math.sin(rad)];
    ctx.strokeStyle='#16a34a';ctx.lineWidth=5;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(OX,OY);ctx.lineTo(Cp[0],Cp[1]);ctx.stroke();
    ctx.lineCap='butt';
    ctx.beginPath();ctx.arc(OX,OY,32,-rad,0);
    ctx.strokeStyle='#b45309';ctx.lineWidth=2;ctx.stroke();
    lbl(ctx,S.A+'°',OX+38,OY-12,'#b45309',15);
    lbl(ctx,'c = '+S.c,(OX+Cp[0])/2-34,(OY+Cp[1])/2,'#15803d',14);
    if(S.kind===0){
      var B=[OX+S.a*U,OY];
      ctx.strokeStyle='#dc2626';ctx.lineWidth=5;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(OX,OY);ctx.lineTo(B[0],B[1]);ctx.stroke();ctx.lineCap='butt';
      if(grow>0){
        ctx.strokeStyle='#334155';ctx.lineWidth=3;
        ctx.beginPath();ctx.moveTo(B[0],B[1]);
        ctx.lineTo(B[0]+(Cp[0]-B[0])*grow,B[1]+(Cp[1]-B[1])*grow);ctx.stroke();
      }
      lbl(ctx,'a = '+S.a,(OX+B[0])/2,OY+22,'#b91c1c',14,'center');
    } else {
      if(grow>0){
        ctx.strokeStyle='#cbd5e1';ctx.lineWidth=1.8;
        ctx.beginPath();ctx.arc(Cp[0],Cp[1],S.a*U,0,Math.PI*2);ctx.stroke();
        ctx.strokeStyle='#f59e0b';ctx.lineWidth=2;ctx.setLineDash([4,4]);
        ctx.beginPath();ctx.moveTo(Cp[0],Cp[1]);ctx.lineTo(Cp[0],OY);ctx.stroke();ctx.setLineDash([]);
        lbl(ctx,'높이 '+r2(c.h),Cp[0]+8,(Cp[1]+OY)/2,'#b45309',13);
      }
      if(grow>=1&&c.n>0){
        var dx=Math.sqrt(Math.max(0,S.a*S.a-c.h*c.h));
        var xs=(c.n===2)?[Cp[0]-dx*U,Cp[0]+dx*U]:[(Math.abs(S.a-c.h)<1e-9)?Cp[0]:(Cp[0]+dx*U)];
        for(i=0;i<xs.length;i++){
          ctx.strokeStyle=(i===0)?'#dc2626':'#7c3aed';ctx.lineWidth=3;
          ctx.beginPath();ctx.moveTo(OX,OY);ctx.lineTo(xs[i],OY);ctx.stroke();
          ctx.beginPath();ctx.moveTo(Cp[0],Cp[1]);ctx.lineTo(xs[i],OY);ctx.stroke();
          ctx.beginPath();ctx.arc(xs[i],OY,6,0,Math.PI*2);
          ctx.fillStyle=(i===0)?'#dc2626':'#7c3aed';ctx.fill();
        }
      }
    }
    lbl(ctx,KINDS[S.kind]+'  (각 '+S.A+'°, c = '+S.c+', a = '+S.a+')',24,32,'#1d4ed8',15);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'삼각형이 몇 개나 될까?':('만들 수 있는 삼각형 : '+c.n+'개'),38,376,
        (c.n===1)?'#15803d':((c.n===0)?'#b91c1c':'#b45309'),19);
    lbl(ctx,(t===null)?'':c.note,38,406,'#52627a',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {kind:S.kind,name:KINDS[S.kind],A:S.A,c:S.c,a:S.a,
            n:c.n,h:(c.h===null)?'-':r2(c.h),note:c.note,
            one:(c.n===1)};
  },
  headA:['번호','조건','각','c','a','높이 c·sinA','만들 수 있는 삼각형','하나로 정해지나?'],
  rowA:function(r,i){
    return [i+1,r.name,r.A+'°',r.c,r.a,r.h,'<b>'+r.n+'개</b>',
            '<span class="'+(r.one?'ok':'no')+'">'+(r.one?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],sas=0,sasOne=0,ssa=0,ssaOne=0,zero=0,two=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.kind===0){ sas++; if(r.one) sasOne++; }
      else { ssa++; if(r.one) ssaOne++; if(r.n===0) zero++; if(r.n===2) two++; }
      rows.push([r.name, r.A+'°', r.c+' , '+r.a, r.h, '<b>'+r.n+'개</b>',
                 '<span class="'+(r.one?'ok':'no')+'">'+(r.one?'○':'×')+'</span>', r.note]);
    }
    var stats=[
      {t:'끼인각 조건에서 하나로 정해진 횟수',big:sas?(sasOne+' / '+sas):'기록 없음',
       p:sas?'두 변 사이의 각이 주어진 경우.':'끼인각 조건도 기록해 보자.'},
      {t:'끼이지 않은 각에서 하나로 정해진 횟수',big:ssa?(ssaOne+' / '+ssa):'기록 없음',
       p:ssa?('그중 0개였던 것 '+zero+'개, 2개였던 것 '+two+'개.'):'끼이지 않은 각 조건도 기록해 보자.'},
      {t:'전체 기록',big:rec.length+'개',p:'각과 두 변의 «위치 관계»가 갈림길이다.'}
    ];
    var concl;
    if(sas===0||ssa===0){
      concl='<b>더 해 보자</b> — 두 조건을 <b>모두</b> 기록해 비교해 보자.';
    } else if(sasOne===sas&&(zero>0||two>0)){
      concl='<b>정리</b> — 두 변과 <b>끼인각</b>이 주어지면 삼각형이 언제나 하나로 정해졌다. '
           +'하지만 각이 두 변 사이에 있지 않으면 <b>0개, 1개, 2개</b>가 모두 나왔다. '
           +'변이 높이보다 짧으면 닿지 않고, 높이보다 길고 다른 변보다 짧으면 두 곳에서 닿기 때문이다. '
           +'«두 변과 한 각»이라는 말만으로는 부족하고, 그 각이 <b>어디에 있는지</b>가 결정조건을 가른다.';
    } else {
      concl='<b>정리</b> — 끼인각 조건은 하나로 정해졌다. 끼이지 않은 각에서 0개나 2개가 나오는 경우도 찾아보자.';
    }
    return {head:['조건','각','두 변','높이','개수','하나?','설명'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 부채꼴의 넓이와 호
# ============================================================
LAB_SEC = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'부채꼴 넓이판',
  action:'호와 넓이 재기',
  hint0:'반지름과 중심각을 정하고, 넓이를 두 방법으로 구해 보자.',
  sliders:[
    {id:'r',label:'반지름',min:2,max:10,value:6,color:'#2563eb',unit:''},
    {id:'th',label:'중심각',min:10,max:350,value:120,color:'#f59e0b',unit:'°'}
  ],
  calc:function(S){
    var rad=S.th*Math.PI/180;
    var l=S.r*rad;
    var S1=Math.PI*S.r*S.r*S.th/360;
    var S2=0.5*S.r*l;
    return {rad:rad,l:l,S1:S1,S2:S2,
            circleArea:Math.PI*S.r*S.r,
            circleLen:2*Math.PI*S.r};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'호의 길이',v:ran?r3(c.l):'재 보자'},
            {k:'넓이',v:ran?r3(c.S1):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '호 '+r3(c.l)+', 넓이 '+r3(c.S1)+'.  ½ × 반지름 × 호 = '+r3(c.S2)+'와 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var CXX=170, CYY=200, U=Math.min(13,120/S.r);
    var R=S.r*U;
    var grow=(t===null)?0:Math.min(1,t);
    ctx.beginPath();ctx.arc(CXX,CYY,R,0,Math.PI*2);
    ctx.strokeStyle='#e2e8f0';ctx.lineWidth=2;ctx.stroke();
    ctx.beginPath();ctx.moveTo(CXX,CYY);
    ctx.arc(CXX,CYY,R,0,c.rad*grow);ctx.closePath();
    ctx.fillStyle='rgba(37,99,235,0.20)';ctx.fill();
    ctx.strokeStyle='#2563eb';ctx.lineWidth=2;ctx.stroke();
    ctx.beginPath();ctx.arc(CXX,CYY,R,0,c.rad*grow);
    ctx.strokeStyle='#dc2626';ctx.lineWidth=5;ctx.stroke();
    ctx.strokeStyle='#16a34a';ctx.lineWidth=4;
    ctx.beginPath();ctx.moveTo(CXX,CYY);ctx.lineTo(CXX+R,CYY);ctx.stroke();
    lbl(ctx,'r = '+S.r,CXX+R/2-14,CYY-8,'#15803d',14);
    if(grow>=1){
      var BX=40, BY=330;
      ctx.strokeStyle='#dc2626';ctx.lineWidth=5;
      ctx.beginPath();ctx.moveTo(BX,BY);ctx.lineTo(BX+c.l*U,BY);ctx.stroke();
      lbl(ctx,'펼친 호 l = '+r3(c.l),BX,BY-12,'#b91c1c',14);
      ctx.strokeStyle='#16a34a';ctx.lineWidth=4;
      ctx.beginPath();ctx.moveTo(BX,BY+16);ctx.lineTo(BX+R,BY+16);ctx.stroke();
      lbl(ctx,'r',BX+R+8,BY+21,'#15803d',13);
    }
    lbl(ctx,'반지름 '+S.r+', 중심각 '+S.th+'°',24,32,'#1d4ed8',18);
    box(ctx,20,364,400,54);
    lbl(ctx,(t===null)?'넓이를 호로 나타낼 수 있을까?':('넓이 '+r3(c.S1)+'      ½ × r × l = '+r3(c.S2)),
        34,392,'#1f2937',17);
    lbl(ctx,(t===null)?'':('호 l = '+r3(c.l)+'      원 전체 넓이 '+r3(c.circleArea)),34,412,'#52627a',14);
  },
  record:function(S){
    var c=this.calc(S);
    return {r:S.r,th:S.th,l:r3(c.l),S1:r3(c.S1),S2:r3(c.S2),
            same:(Math.abs(c.S1-c.S2)<1e-9),
            ratioL:r3(c.l/c.circleLen),
            ratioS:r3(c.S1/c.circleArea),
            ratioSame:(Math.abs(c.l/c.circleLen-c.S1/c.circleArea)<1e-9)};
  },
  headA:['번호','r','중심각','호 l','넓이','½ r l','같나?','호의 비','넓이의 비','같나?'],
  rowA:function(r,i){
    return [i+1,r.r,r.th+'°',r.l,'<b>'+r.S1+'</b>',r.S2,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            r.ratioL,r.ratioS,
            '<span class="'+(r.ratioSame?'ok':'no')+'">'+(r.ratioSame?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,rs=0,rn={},kn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.ratioSame) rs++;
      if(!rn[r.r]){ rn[r.r]=true; kn++; }
      rows.push([r.r, r.th+'°', r.l, '<b>'+r.S1+'</b>', r.S2,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 r.ratioL+' / '+r.ratioS,
                 '<span class="'+(r.ratioSame?'ok':'no')+'">'+(r.ratioSame?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'넓이 = ½ × 반지름 × 호',big:same+' / '+rec.length,
       p:'중심각으로 구한 넓이와 비교한 결과.'},
      {t:'호의 비 = 넓이의 비',big:rs+' / '+rec.length,
       p:'원 전체에 대한 비율이 같은지 확인한 결과.'},
      {t:'시험한 반지름',big:kn+'가지',p:'반지름을 바꿔도 관계가 유지되었다.'}
    ];
    var concl;
    if(same===rec.length&&rs===rec.length){
      concl='<b>정리</b> — 부채꼴의 넓이는 언제나 <b>½ × 반지름 × 호의 길이</b>와 같았다. '
           +'중심각을 몰라도 반지름과 호만 알면 넓이를 구할 수 있다는 뜻이다. '
           +'부채꼴을 아주 잘게 잘라 붙이면 밑변이 호, 높이가 반지름인 삼각형에 가까워지기 때문이다. '
           +'또 호가 원 둘레에서 차지하는 비율과 넓이가 원 넓이에서 차지하는 비율이 언제나 같았다.';
    } else {
      concl='<b>확인 필요</b> — 두 계산이 어긋난 기록이 있다.';
    }
    return {head:['r','중심각','호','넓이','½rl','같나?','호/넓이 비','같나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 원뿔과 원기둥의 부피
# ============================================================
LAB_CONE = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'부피 비교판',
  action:'물을 부어 보기',
  hint0:'밑면 반지름과 높이를 정해 보자. 같은 밑면·높이의 원뿔과 원기둥을 비교한다.',
  sliders:[
    {id:'r',label:'밑면 반지름',min:1,max:5,value:3,color:'#2563eb',unit:''},
    {id:'h',label:'높이',min:1,max:6,value:4,color:'#16a34a',unit:''}
  ],
  calc:function(S){
    var cyl=Math.PI*S.r*S.r*S.h;
    var cone=cyl/3;
    var sph=4/3*Math.PI*S.r*S.r*S.r;
    return {cyl:cyl,cone:cone,sph:sph,ratio:cyl/cone};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'원기둥 부피',v:r2(c.cyl)},
            {k:'원뿔 부피',v:ran?r2(c.cone):'부어 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '원기둥 '+r2(c.cyl)+', 원뿔 '+r2(c.cone)+'.  원기둥 ÷ 원뿔 = '+r3(c.ratio)+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var U=Math.min(26, 110/Math.max(S.r,1), 150/Math.max(S.h,1));
    var RW=S.r*U, HH=S.h*U;
    var grow=(t===null)?0:Math.min(1,t);
    var CY0=320;
    function ell(cx,cy,rx,ry,col,fill){
      ctx.beginPath();ctx.ellipse(cx,cy,rx,ry,0,0,Math.PI*2);
      if(fill){ ctx.fillStyle=fill;ctx.fill(); }
      ctx.strokeStyle=col;ctx.lineWidth=2;ctx.stroke();
    }
    var C1=120;
    ctx.fillStyle='rgba(37,99,235,0.10)';
    ctx.fillRect(C1-RW,CY0-HH,2*RW,HH);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(C1-RW,CY0-HH);ctx.lineTo(C1-RW,CY0);
    ctx.moveTo(C1+RW,CY0-HH);ctx.lineTo(C1+RW,CY0);ctx.stroke();
    ell(C1,CY0,RW,RW*0.3,'#2563eb',null);
    ell(C1,CY0-HH,RW,RW*0.3,'#2563eb','rgba(37,99,235,0.10)');
    lbl(ctx,'원기둥',C1,CY0+34,'#1d4ed8',15,'center');
    var C2=320;
    ctx.beginPath();
    ctx.moveTo(C2-RW,CY0);ctx.lineTo(C2,CY0-HH);ctx.lineTo(C2+RW,CY0);
    ctx.closePath();
    ctx.fillStyle='rgba(220,38,38,0.10)';ctx.fill();
    ctx.strokeStyle='#dc2626';ctx.lineWidth=2;ctx.stroke();
    ell(C2,CY0,RW,RW*0.3,'#dc2626',null);
    lbl(ctx,'원뿔',C2,CY0+34,'#b91c1c',15,'center');
    if(grow>0){
      var fill=Math.min(1,grow*3);
      var fh=HH*fill/3;
      ctx.fillStyle='rgba(59,130,246,0.45)';
      ctx.fillRect(C1-RW,CY0-fh,2*RW,fh);
      ell(C1,CY0-fh,RW,RW*0.3,'#2563eb','rgba(59,130,246,0.45)');
      if(grow>=1){
        lbl(ctx,'원뿔 1번 분량',C1,CY0-fh-14,'#1d4ed8',13,'center');
        lbl(ctx,'3번 부으면 가득',C1,CY0-HH-16,'#b45309',14,'center');
      }
    }
    lbl(ctx,'밑면 반지름 '+S.r+', 높이 '+S.h+'  (같은 조건)',24,32,'#334155',16);
    box(ctx,20,364,400,54);
    lbl(ctx,(t===null)?'원뿔을 몇 번 부으면 가득 찰까?':('원기둥 '+r2(c.cyl)+'      원뿔 '+r2(c.cone)),34,390,'#1f2937',17);
    lbl(ctx,(t===null)?'':('원기둥 ÷ 원뿔 = '+r3(c.ratio)+'      같은 반지름의 구 '+r2(c.sph)),34,412,'#15803d',14);
  },
  record:function(S){
    var c=this.calc(S);
    return {r:S.r,h:S.h,cyl:r2(c.cyl),cone:r2(c.cone),sph:r2(c.sph),
            ratio:r3(c.ratio),
            three:(Math.abs(c.ratio-3)<1e-9),
            halfEq:(Math.abs(c.cone-c.cyl/2)<1e-9)};
  },
  headA:['번호','r, h','원기둥','원뿔','원기둥 ÷ 원뿔','3인가?','원뿔 = 절반?','같은 r의 구'],
  rowA:function(r,i){
    return [i+1,r.r+', '+r.h,r.cyl,'<b>'+r.cone+'</b>',r.ratio,
            '<span class="'+(r.three?'ok':'no')+'">'+(r.three?'○':'×')+'</span>',
            '<span class="'+(r.halfEq?'ok':'no')+'">'+(r.halfEq?'○':'×')+'</span>',
            r.sph];
  },
  analyze:function(rec){
    var rows=[],three=0,half=0,rs={},hs={},rn=0,hn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.three) three++;
      if(r.halfEq) half++;
      if(!rs[r.r]){ rs[r.r]=true; rn++; }
      if(!hs[r.h]){ hs[r.h]=true; hn++; }
      rows.push([r.r+', '+r.h, r.cyl, '<b>'+r.cone+'</b>', r.ratio,
                 '<span class="'+(r.three?'ok':'no')+'">'+(r.three?'○':'×')+'</span>',
                 '<span class="'+(r.halfEq?'ok':'no')+'">'+(r.halfEq?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'원기둥 ÷ 원뿔 = 3',big:three+' / '+rec.length,
       p:'밑면과 높이가 같을 때의 부피 비.'},
      {t:'“원뿔은 원기둥의 절반”이 맞은 횟수',big:half+' / '+rec.length,
       p:'절반이라고 생각하기 쉽지만 실제로는 3분의 1이다.'},
      {t:'시험한 반지름 / 높이',big:rn+'가지 / '+hn+'가지',
       p:'크기를 바꿔도 비는 달라지지 않았다.'}
    ];
    var concl;
    if(three===rec.length&&half===0){
      concl='<b>정리</b> — 밑면과 높이가 같으면 원뿔의 부피는 언제나 원기둥의 <b>3분의 1</b>이었다. '
           +'반지름과 높이를 아무리 바꿔도 비는 정확히 3으로 고정되었다. '
           +'원뿔에 물을 채워 원기둥에 부으면 <b>세 번</b>만에 가득 찬다. «절반»이 아니다. '
           +'각뿔과 각기둥 사이에서도 같은 관계가 성립한다.';
    } else {
      concl='<b>확인 필요</b> — 비가 3이 아닌 기록이 있다.';
    }
    return {head:['r, h','원기둥','원뿔','비','3인가?','절반인가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 줄기와 잎 vs 도수분포표
# ============================================================
LAB_STEM = BASE + DATA_JS + r"""
var WS=[5,10,20];
var LO=40;
function bins(w){
  var n=Math.ceil(60/w), f=[],i,j;
  for(i=0;i<n;i++) f.push(0);
  for(j=0;j<DATA.length;j++){
    var k=Math.floor((DATA[j]-LO)/w);
    if(k>=n) k=n-1;
    if(k<0) k=0;
    f[k]++;
  }
  return {n:n,f:f,w:w};
}
var LAB = {
  cw:440, ch:430, cvTitle:'자료 표현 비교판',
  action:'두 방법으로 정리하기',
  hint0:'같은 자료 20개를 줄기와 잎, 그리고 도수분포표로 정리해 보자.',
  sliders:[
    {id:'wi',label:'도수분포표의 계급 크기',min:0,max:2,value:1,color:'#2563eb',fmt:function(v){return WS[v]+'점';}}
  ],
  calc:function(S){
    var w=WS[S.wi], b=bins(w);
    var mx=DATA[DATA.length-1], mn=DATA[0];
    var top=b.n-1;
    while(top>0&&b.f[top]===0) top--;
    var bot=0;
    while(bot<b.n-1&&b.f[bot]===0) bot++;
    var est=LO+(top+1)*w;
    var mid=(DATA[9]+DATA[10])/2;
    return {w:w,b:b,mx:mx,mn:mn,est:est,estLo:LO+bot*w,mid:mid,
            gap:est-mx};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'줄기와 잎에서 최댓값',v:c.mx},
            {k:'도수분포표에서는',v:ran?('최대 '+c.est+' 미만'):'정리해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '줄기와 잎에서는 최댓값 '+c.mx+'을 정확히 읽을 수 있지만, 계급 '+c.w+'점 도수분포표에서는 '+c.estLo+' 이상 '+c.est+' 미만이라는 것만 안다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i, j;
    var grow=(t===null)?0:Math.min(1,t);
    lbl(ctx,'줄기와 잎 그림 (자료 20개)',24,32,'#1d4ed8',17);
    var stems={};
    for(i=0;i<DATA.length;i++){
      var st=Math.floor(DATA[i]/10);
      if(!stems[st]) stems[st]=[];
      stems[st].push(DATA[i]%10);
    }
    var keys=[];
    for(var k in stems) keys.push(parseInt(k,10));
    keys.sort(function(x,y){return x-y;});
    var Y0=58;
    for(i=0;i<keys.length;i++){
      var y=Y0+i*24;
      ctx.fillStyle='#334155';ctx.font='bold 15px sans-serif';ctx.textAlign='right';
      ctx.fillText(keys[i],62,y);
      ctx.textAlign='left';
      ctx.strokeStyle='#94a3b8';ctx.lineWidth=1.4;
      ctx.beginPath();ctx.moveTo(70,y-14);ctx.lineTo(70,y+6);ctx.stroke();
      var arr=stems[keys[i]];
      for(j=0;j<arr.length;j++){
        ctx.fillStyle='#1d4ed8';ctx.font='15px sans-serif';
        ctx.fillText(arr[j],80+j*18,y);
      }
    }
    var Y1=Y0+keys.length*24+22;
    lbl(ctx,'도수분포표 (계급 '+c.w+'점)',24,Y1,'#b45309',17);
    var shown=(t===null)?0:Math.ceil(grow*c.b.n);
    var GX=40, GY=Y1+16, CW=Math.min(70,360/c.b.n);
    for(i=0;i<c.b.n;i++){
      var x=GX+i*CW;
      ctx.fillStyle=(i<shown)?'#fed7aa':'#f5f7fa';
      ctx.fillRect(x,GY,CW-3,26);
      ctx.strokeStyle='#cbd5e1';ctx.lineWidth=1.2;ctx.strokeRect(x,GY,CW-3,26);
      ctx.fillStyle='#7c2d12';ctx.font='11px sans-serif';ctx.textAlign='center';
      ctx.fillText((LO+i*c.w)+'~',x+(CW-3)/2,GY-4);
      if(i<shown){
        ctx.fillStyle='#1f2937';ctx.font='bold 14px sans-serif';
        ctx.fillText(c.b.f[i],x+(CW-3)/2,GY+18);
      }
    }
    ctx.textAlign='left';
    box(ctx,20,352,400,66);
    lbl(ctx,'실제 최댓값 '+c.mx+'      실제 중앙값 '+c.mid,34,378,'#15803d',16);
    lbl(ctx,(t===null)?'도수분포표에서 최댓값을 알 수 있을까?':('도수분포표로는 '+c.estLo+' 이상 '+c.est+' 미만 (오차 최대 '+c.w+')'),
        34,404,'#b91c1c',15);
  },
  record:function(S){
    var c=this.calc(S);
    return {w:c.w,n:c.b.n,mx:c.mx,est:c.est,estLo:c.estLo,
            gap:c.gap,mid:c.mid,
            exact:(c.gap===0),
            f:c.b.f.join(', ')};
  },
  headA:['번호','계급 크기','계급 수','도수','줄기와 잎의 최댓값','도수분포표의 범위','오차','정확히 알 수 있나?'],
  rowA:function(r,i){
    return [i+1,r.w+'점',r.n+'개',r.f,'<b>'+r.mx+'</b>',r.estLo+' ~ '+r.est,r.gap,
            '<span class="'+(r.exact?'ok':'no')+'">'+(r.exact?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],exact=0,ws={},wn=0,mx=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.exact) exact++;
      if(!ws[r.w]){ ws[r.w]=true; wn++; }
      if(r.gap>mx) mx=r.gap;
      rows.push([r.w+'점', r.n+'개', r.f, '<b>'+r.mx+'</b>', r.estLo+' ~ '+r.est, r.gap,
                 '<span class="'+(r.exact?'ok':'no')+'">'+(r.exact?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'도수분포표로 최댓값을 정확히 알 수 있던 횟수',big:exact+' / '+rec.length,
       p:'계급으로 묶는 순간 원래 값이 사라진다.'},
      {t:'시험한 계급 크기',big:wn+'가지',p:'계급이 클수록 정보가 더 많이 사라졌다.'},
      {t:'가장 컸던 오차',big:mx+'점',p:'줄기와 잎에서는 오차가 없다.'}
    ];
    var concl;
    if(wn<2){
      concl='<b>더 해 보자</b> — 계급 크기를 5점과 20점으로 모두 바꿔 기록해 비교해 보자.';
    } else {
      concl='<b>정리</b> — 줄기와 잎 그림은 <b>원래 자료를 하나도 잃지 않아서</b> 최댓값도 중앙값도 정확히 읽을 수 있었다. '
           +'반면 도수분포표는 계급으로 묶는 순간 «어느 구간에 몇 개»만 남아 원래 값을 되찾을 수 없었다. '
           +'계급이 클수록 오차가 커졌다(최대 '+mx+'점). '
           +'대신 도수분포표는 자료가 많을 때 흩어진 모습을 한눈에 보여 준다. 목적에 따라 골라 써야 한다.';
    }
    return {head:['계급 크기','계급 수','도수','실제 최댓값','표의 범위','오차','정확?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 도수분포다각형
# ============================================================
LAB_POLY = BASE + DATA_JS + r"""
var WS=[5,10,20];
var LO=40;
function bins(w){
  var n=Math.ceil(60/w), f=[],i,j;
  for(i=0;i<n;i++) f.push(0);
  for(j=0;j<DATA.length;j++){
    var k=Math.floor((DATA[j]-LO)/w);
    if(k>=n) k=n-1;
    if(k<0) k=0;
    f[k]++;
  }
  return {n:n,f:f,w:w};
}
var LAB = {
  cw:440, ch:430, cvTitle:'도수분포다각형 판',
  action:'중점을 이어 보기',
  hint0:'계급의 크기를 정하고, 히스토그램의 중점을 이어 보자.',
  sliders:[
    {id:'wi',label:'계급의 크기',min:0,max:2,value:1,color:'#2563eb',fmt:function(v){return WS[v]+'점';}}
  ],
  calc:function(S){
    var w=WS[S.wi], b=bins(w);
    var histA=0,i;
    for(i=0;i<b.n;i++) histA+=b.f[i]*w;
    var pts=[[LO-w/2,0]];
    for(i=0;i<b.n;i++) pts.push([LO+i*w+w/2,b.f[i]]);
    pts.push([LO+b.n*w+w/2,0]);
    var polyA=0;
    for(i=0;i<pts.length-1;i++){
      polyA+=(pts[i][1]+pts[i+1][1])/2*(pts[i+1][0]-pts[i][0]);
    }
    var sum=0;
    for(i=0;i<b.n;i++) sum+=b.f[i];
    return {w:w,b:b,pts:pts,histA:histA,polyA:polyA,sum:sum};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'히스토그램 넓이',v:c.histA},
            {k:'다각형 아래 넓이',v:ran?r2(c.polyA):'이어 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '히스토그램 넓이 '+c.histA+', 다각형 아래 넓이 '+r2(c.polyA)+'.  도수의 합 '+c.sum+' × 계급 '+c.w+' 과 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var GX=54, GY=310, GW=346, GH=210;
    var mx=1;
    for(i=0;i<c.b.n;i++){ if(c.b.f[i]>mx) mx=c.b.f[i]; }
    function px(v){ return GX+GW*(v-(LO-c.w))/((c.b.n+2)*c.w); }
    function py(v){ return GY-v/mx*GH; }
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+GW,GY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX,GY-GH-10);ctx.stroke();
    for(i=0;i<c.b.n;i++){
      var x0=px(LO+i*c.w), x1=px(LO+(i+1)*c.w);
      var h=GY-py(c.b.f[i]);
      ctx.fillStyle='rgba(147,197,253,0.55)';
      ctx.fillRect(x0,py(c.b.f[i]),x1-x0,h);
      ctx.strokeStyle='#2563eb';ctx.lineWidth=1.6;
      ctx.strokeRect(x0,py(c.b.f[i]),x1-x0,h);
      ctx.fillStyle='#475569';ctx.font='10px sans-serif';ctx.textAlign='center';
      ctx.fillText(LO+i*c.w,x0,GY+14);
    }
    ctx.textAlign='left';
    var grow=(t===null)?0:Math.min(1,t);
    var n=Math.ceil(grow*(c.pts.length-1));
    if(grow>0){
      ctx.strokeStyle='#dc2626';ctx.lineWidth=3;ctx.beginPath();
      for(i=0;i<c.pts.length&&i<=n;i++){
        var X=px(c.pts[i][0]), Y=py(c.pts[i][1]);
        if(i===0) ctx.moveTo(X,Y); else ctx.lineTo(X,Y);
      }
      ctx.stroke();
      for(i=0;i<c.pts.length&&i<=n;i++){
        ctx.beginPath();ctx.arc(px(c.pts[i][0]),py(c.pts[i][1]),4,0,Math.PI*2);
        ctx.fillStyle='#dc2626';ctx.fill();
      }
    }
    lbl(ctx,'계급 '+c.w+'점,  자료 20개',24,32,'#1d4ed8',18);
    lbl(ctx,'빨강 = 각 직사각형 윗변의 중점을 이은 선',24,56,'#52627a',14);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'두 넓이는 같을까?':('히스토그램 '+c.histA+'      다각형 아래 '+r2(c.polyA)),38,376,'#1f2937',18);
    lbl(ctx,'도수의 합 '+c.sum+' × 계급 '+c.w+' = '+(c.sum*c.w),38,406,'#15803d',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {w:c.w,n:c.b.n,sum:c.sum,
            hist:c.histA,poly:r2(c.polyA),
            same:(Math.abs(c.histA-c.polyA)<1e-9),
            prod:c.sum*c.w,
            prodOk:(c.histA===c.sum*c.w),
            f:c.b.f.join(', ')};
  },
  headA:['번호','계급 크기','계급 수','도수','도수의 합','히스토그램 넓이','다각형 넓이','같나?','도수합 × 계급'],
  rowA:function(r,i){
    return [i+1,r.w+'점',r.n+'개',r.f,r.sum,'<b>'+r.hist+'</b>',r.poly,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            r.prod];
  },
  analyze:function(rec){
    var rows=[],same=0,prod=0,ws={},wn=0,sums={},sn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.prodOk) prod++;
      if(!ws[r.w]){ ws[r.w]=true; wn++; }
      if(!sums[r.sum]){ sums[r.sum]=true; sn++; }
      rows.push([r.w+'점', r.n+'개', r.f, r.sum, '<b>'+r.hist+'</b>', r.poly,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 r.prod]);
    }
    var stats=[
      {t:'히스토그램 넓이 = 다각형 아래 넓이',big:same+' / '+rec.length,
       p:'중점을 이을 때 잘려 나간 만큼이 그대로 채워진다.'},
      {t:'넓이 = 도수의 합 × 계급 크기',big:prod+' / '+rec.length,
       p:'계급이 모두 같은 폭이기 때문이다.'},
      {t:'시험한 계급 크기 / 도수의 합',big:wn+'가지 / '+sn+'가지',
       p:'계급을 바꿔도 도수의 합은 20으로 같았다.'}
    ];
    var concl;
    if(wn<2){
      concl='<b>더 해 보자</b> — 계급 크기를 바꿔 여러 번 기록해 보자.';
    } else if(same===rec.length){
      concl='<b>정리</b> — 히스토그램의 직사각형 넓이 합과 도수분포다각형 아래 넓이가 <b>언제나 같았다.</b> '
           +'중점을 이을 때 직사각형에서 잘려 나간 삼각형과 새로 생긴 삼각형이 정확히 짝을 이루기 때문이다. '
           +'그래서 두 그림은 같은 자료를 다르게 보여 줄 뿐이고, 다각형은 <b>여러 자료를 겹쳐 비교</b>할 때 편하다. '
           +'양 끝에 도수 0인 계급을 하나씩 두는 이유도 선을 닫아 넓이를 맞추기 위해서다.';
    } else {
      concl='<b>확인 필요</b> — 두 넓이가 다른 기록이 있다.';
    }
    return {head:['계급','계급 수','도수','합','히스토그램','다각형','같나?','합×계급'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("m1_triangle_determination_lab.html",
     "삼각형 결정조건 실험실 — 각의 위치가 왜 중요할까?",
     "삼각형 결정조건 실험실 — 각의 위치가 왜 중요할까?",
     "두 변과 한 각이 주어질 때 각의 위치를 바꿔 가며 만들 수 있는 삼각형의 개수를 센다.",
     LAB_DET),
    ("m1_sector_area_lab.html",
     "부채꼴 넓이 실험실 — 호만 알아도 넓이를 구할까?",
     "부채꼴 넓이 실험실 — 호만 알아도 넓이를 구할까?",
     "반지름과 중심각을 바꿔 가며 호의 길이와 넓이를 재고, ½ × 반지름 × 호와 비교한다.",
     LAB_SEC),
    ("m1_cone_volume_lab.html",
     "부피 실험실 — 원뿔은 원기둥의 절반일까?",
     "부피 실험실 — 원뿔은 원기둥의 절반일까?",
     "같은 밑면과 높이의 원뿔과 원기둥의 부피를 계산해 비를 기록한다.",
     LAB_CONE),
    ("m1_stem_leaf_lab.html",
     "자료 표현 실험실 — 묶으면 무엇이 사라질까?",
     "자료 표현 실험실 — 묶으면 무엇이 사라질까?",
     "같은 자료를 줄기와 잎, 도수분포표로 정리해 원래 값을 얼마나 되찾을 수 있는지 기록한다.",
     LAB_STEM),
    ("m1_frequency_polygon_lab.html",
     "도수분포다각형 실험실 — 넓이는 달라질까?",
     "도수분포다각형 실험실 — 넓이는 달라질까?",
     "히스토그램의 중점을 이어 다각형을 만들고, 두 그림의 넓이를 비교한다.",
     LAB_POLY),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c38_" + fname + ".js", "w", encoding="utf-8").write(js)

print("DATA =", DATA)
print("\n".join(made))
