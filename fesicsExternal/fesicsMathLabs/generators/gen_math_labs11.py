# -*- coding: utf-8 -*-
"""중1 '도형과 측정' 실험 5종"""
import os, re

OUT = "/mnt/user-data/outputs"
src = open("/home/claude/gen_math_labs.py", encoding="utf-8").read()
TPL = re.search(r'TPL = r"""(.*?)"""\n', src, re.S).group(1)

BASE = r"""
function lbl(ctx,t,x,y,c,sz,al){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
function box(ctx,x,y,w,h){ctx.fillStyle='#f1f6fd';ctx.fillRect(x,y,w,h);ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(x,y,w,h);}
function r1(v){return Math.round(v*10)/10;}
function r2(v){return Math.round(v*100)/100;}
function angDeg(p,q,r){
  var ax=p[0]-q[0],ay=p[1]-q[1],bx=r[0]-q[0],by=r[1]-q[1];
  var d=ax*bx+ay*by,m=Math.sqrt(ax*ax+ay*ay)*Math.sqrt(bx*bx+by*by);
  var c=(m===0)?1:d/m; if(c>1)c=1; if(c<-1)c=-1;
  return Math.acos(c)*180/Math.PI;
}
"""

# ============================================================
# 1. 평행선과 동위각
# ============================================================
LAB_PARALLEL = BASE + r"""
var LAB = {
  cw:440, ch:420, cvTitle:'평행선과 각',
  action:'각을 재 보기',
  hint0:'아래 직선의 기울기와 가로지르는 선의 각을 정해 보자.',
  sliders:[
    {id:'th',label:'아래 직선의 기울기',min:-30,max:30,value:12,color:'#16a34a',
     fmt:function(v){return (v===0)?'0° (평행)':(v+'°');}},
    {id:'ph',label:'가로지르는 선의 각',min:30,max:150,value:60,color:'#f59e0b',unit:'°'}
  ],
  calc:function(S){
    var A=S.ph, B=S.ph-S.th;
    return {A:A,B:B,same:(Math.abs(A-B)<1e-9),vert:true,par:(S.th===0)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'위쪽 동위각',v:ran?(r1(c.A)+'°'):'재 보자'},
            {k:'아래쪽 동위각',v:ran?(r1(c.B)+'°'):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '동위각은 '+r1(c.A)+'°와 '+r1(c.B)+'°다. '+(c.same?'같다 — 두 직선이 평행하기 때문이다.':'다르다 — 두 직선이 평행하지 않다.')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var y1=130, y2=270, CX=220;
    function line(y,ang,col){
      var rad=ang*Math.PI/180;
      var dx=200*Math.cos(rad), dy=-200*Math.sin(rad);
      ctx.beginPath();ctx.moveTo(CX-dx,y-dy);ctx.lineTo(CX+dx,y+dy);
      ctx.strokeStyle=col;ctx.lineWidth=3;ctx.stroke();
    }
    line(y1,0,'#2563eb');
    line(y2,S.th,'#16a34a');
    var rad=S.ph*Math.PI/180;
    var tx=(y2-y1)/Math.tan(rad);
    ctx.beginPath();
    ctx.moveTo(CX-40-(-40)*0,y1-70);
    var x1=CX+70-(70)/Math.tan(rad)*0;
    var px1=CX+ (y1-200)/Math.tan(rad)*0;
    ctx.beginPath();
    var xA=CX, xB=CX+tx;
    ctx.moveTo(xA-(70)/Math.tan(rad), y1-70);
    ctx.lineTo(xB+(70)/Math.tan(rad), y2+70);
    ctx.strokeStyle='#f59e0b';ctx.lineWidth=3;ctx.stroke();
    var show=(t===null)?0:Math.min(1,t);
    function arc(cx,cy,a0,a1,col,al){
      ctx.globalAlpha=al;
      ctx.beginPath();ctx.moveTo(cx,cy);ctx.arc(cx,cy,34,a0,a1);ctx.closePath();
      ctx.fillStyle=col;ctx.fill();ctx.globalAlpha=1;
    }
    if(show>0){
      arc(xA,y1,-rad,0,'rgba(37,99,235,0.30)',show);
      arc(xB,y2,-rad,-S.th*Math.PI/180,'rgba(22,163,74,0.30)',show);
      lbl(ctx,r1(c.A)+'°',xA+40,y1-10,'#1d4ed8',16);
      lbl(ctx,r1(c.B)+'°',xB+40,y2-10,'#15803d',16);
    }
    lbl(ctx,'두 직선을 한 직선이 가로지를 때',24,36,'#1d4ed8',18);
    lbl(ctx,(S.th===0)?'두 직선은 평행하다':'두 직선은 평행하지 않다',24,62,(S.th===0)?'#15803d':'#b91c1c',17);
    box(ctx,20,336,400,72);
    lbl(ctx,(t===null)?'동위각의 크기는 같을까?':('동위각 : '+r1(c.A)+'°  와  '+r1(c.B)+'°'),38,368,'#1f2937',20);
    lbl(ctx,(t===null)?'':((c.same?'같다':'다르다')+'    맞꼭지각은 언제나 같다'),38,396,c.same?'#15803d':'#b91c1c',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {th:S.th,ph:S.ph,A:r1(c.A),B:r1(c.B),same:c.same,par:c.par,vert:true};
  },
  headA:['번호','아래 직선 기울기','평행?','가로지르는 각','위 동위각','아래 동위각','같은가?','맞꼭지각'],
  rowA:function(r,i){
    return [i+1,r.th+'°',r.par?'평행':'아님',r.ph+'°',r.A+'°',r.B+'°',
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            '<span class="ok">항상 같음</span>'];
  },
  analyze:function(rec){
    var rows=[],par=0,parSame=0,np=0,npSame=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.par){ par++; if(r.same) parSame++; }
      else { np++; if(r.same) npSame++; }
      rows.push([r.par?'평행':'평행 아님', r.ph+'°', r.A+'°', r.B+'°',
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'평행일 때 동위각이 같았던 횟수',big:par?(parSame+' / '+par):'기록 없음',
       p:par?'두 직선이 평행한 기록만 셈.':'기울기를 0°로 맞춰 평행인 경우도 기록해 보자.'},
      {t:'평행이 아닐 때 같았던 횟수',big:np?(npSame+' / '+np):'기록 없음',
       p:np?'평행이 아닌 기록 중 동위각이 같았던 수.':'기울기를 0이 아닌 값으로도 해 보자.'},
      {t:'맞꼭지각',big:'항상 같음',p:'한 점에서 만난 두 직선의 맞꼭지각은 조건 없이 언제나 같다.'}
    ];
    var concl;
    if(par===0||np===0){
      concl='<b>더 해 보자</b> — 평행한 경우와 평행하지 않은 경우를 <b>모두</b> 기록해야 조건이 보인다.';
    } else if(parSame===par && npSame===0){
      concl='<b>정리</b> — 동위각이 같았던 것은 <b>두 직선이 평행할 때뿐</b>이었다. 평행하지 않으면 '+np+'번 모두 달랐다. '
           +'“가로지르는 선이 있으면 동위각은 같다”가 아니라 <b>평행일 때만</b> 같다. '
           +'반면 맞꼭지각은 평행과 상관없이 언제나 같다. 두 성질을 구별해야 한다.';
    } else {
      concl='<b>확인 필요</b> — 규칙과 어긋난 기록이 있다.';
    }
    return {head:['두 직선','가로지르는 각','위 동위각','아래 동위각','같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 삼각형이 되는 조건
# ============================================================
LAB_TRIIN = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'삼각형 작도판',
  action:'세 변으로 작도해 보기',
  hint0:'세 변의 길이를 정하고, 삼각형이 만들어지는지 확인해 보자.',
  sliders:[
    {id:'a',label:'밑변',min:1,max:15,value:8,color:'#2563eb',unit:'cm'},
    {id:'b',label:'두 번째 변',min:1,max:15,value:5,color:'#16a34a',unit:'cm'},
    {id:'c',label:'세 번째 변',min:1,max:15,value:6,color:'#f59e0b',unit:'cm'}
  ],
  calc:function(S){
    var a=S.a,b=S.b,c=S.c;
    var x=(c*c-b*b+a*a)/(2*a);
    var y2=c*c-x*x;
    var mx=Math.max(a,b,c), rest=a+b+c-mx;
    return {x:x,y:(y2>0)?Math.sqrt(y2):0,ok:(y2>1e-9),
            mx:mx,rest:rest,deg:(Math.abs(y2)<=1e-9)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'가장 긴 변',v:c.mx+'cm'},
            {k:'나머지 두 변의 합',v:c.rest+'cm'+(ran?(c.ok?'  → 삼각형':'  → 안 됨'):'')}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.ok) return '삼각형이 만들어졌다. 나머지 두 변의 합 '+c.rest+'cm가 가장 긴 변 '+c.mx+'cm보다 크다. 기록해 보자.';
    return '삼각형이 만들어지지 않았다. 나머지 두 변의 합 '+c.rest+'cm가 가장 긴 변 '+c.mx+'cm보다 크지 않다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var cc=this.calc(S);
    var U=Math.min(22, 340/Math.max(S.a,S.b+S.c));
    var BX=(440-S.a*U)/2, BY=250;
    var grow=(t===null)?0:Math.min(1,t);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=5;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(BX,BY);ctx.lineTo(BX+S.a*U,BY);ctx.stroke();
    if(grow>0){
      ctx.strokeStyle='#cbd5e1';ctx.lineWidth=1.6;
      ctx.beginPath();ctx.arc(BX,BY,S.c*U,Math.PI,2*Math.PI);ctx.stroke();
      ctx.beginPath();ctx.arc(BX+S.a*U,BY,S.b*U,Math.PI,2*Math.PI);ctx.stroke();
    }
    if(grow>0.4){
      var g=(grow-0.4)/0.6;
      if(cc.ok){
        var ax=BX+cc.x*U, ay=BY-cc.y*U;
        ctx.strokeStyle='#16a34a';ctx.lineWidth=5;
        ctx.beginPath();ctx.moveTo(BX+S.a*U,BY);
        ctx.lineTo(BX+S.a*U+(ax-(BX+S.a*U))*g,BY+(ay-BY)*g);ctx.stroke();
        ctx.strokeStyle='#f59e0b';ctx.lineWidth=5;
        ctx.beginPath();ctx.moveTo(BX,BY);
        ctx.lineTo(BX+(ax-BX)*g,BY+(ay-BY)*g);ctx.stroke();
      } else {
        ctx.strokeStyle='#f59e0b';ctx.lineWidth=5;
        ctx.beginPath();ctx.moveTo(BX,BY);ctx.lineTo(BX+S.c*U*g,BY);ctx.stroke();
        ctx.strokeStyle='#16a34a';ctx.lineWidth=5;
        ctx.beginPath();ctx.moveTo(BX+S.a*U,BY);ctx.lineTo(BX+S.a*U-S.b*U*g,BY);ctx.stroke();
        if(g>0.9) lbl(ctx,'두 변이 만나지 못한다',BX,BY-24,'#b91c1c',17);
      }
    }
    ctx.lineCap='butt';
    lbl(ctx,'세 변  '+S.a+' , '+S.b+' , '+S.c+' cm',24,36,'#1d4ed8',19);
    box(ctx,20,286,400,98);
    lbl(ctx,'가장 긴 변 '+cc.mx+'cm     나머지 두 변의 합 '+cc.rest+'cm',38,318,'#52627a',18);
    lbl(ctx,(t===null)?'삼각형이 될까?':(cc.ok?'삼각형이 된다':'삼각형이 되지 않는다'),38,350,cc.ok?'#15803d':'#b91c1c',21);
    lbl(ctx,(t===null)?'':(cc.rest>cc.mx?'(나머지 합) > (가장 긴 변)':'(나머지 합) ≤ (가장 긴 변)'),38,376,'#334155',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,c:S.c,mx:c.mx,rest:c.rest,ok:c.ok,
            rule:(c.rest>c.mx),deg:c.deg};
  },
  headA:['번호','세 변','가장 긴 변','나머지 두 변의 합','삼각형?','합 > 가장 긴 변?','두 판단 일치?'],
  rowA:function(r,i){
    var m=(r.ok===r.rule);
    return [i+1,r.a+', '+r.b+', '+r.c,r.mx,r.rest,
            '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
            '<span class="'+(r.rule?'ok':'no')+'">'+(r.rule?'○':'×')+'</span>',
            '<span class="'+(m?'ok':'no')+'">'+(m?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],match=0,yes=0,no=0,deg=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i], m=(r.ok===r.rule);
      if(m) match++;
      if(r.ok) yes++; else no++;
      if(r.deg) deg++;
      rows.push([r.a+', '+r.b+', '+r.c, r.mx, r.rest,
                 '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
                 '<span class="'+(r.rule?'ok':'no')+'">'+(r.rule?'○':'×')+'</span>',
                 '<span class="'+(m?'ok':'no')+'">'+(m?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'작도 결과와 부등식 판정이 일치',big:match+' / '+rec.length,
       p:'실제로 그려 본 결과와 (나머지 합) > (가장 긴 변) 판정이 같았던 횟수.'},
      {t:'삼각형이 된 기록',big:yes+'개',p:yes?'':'삼각형이 되는 경우도 기록해 보자.'},
      {t:'되지 않은 기록',big:no+'개',
       p:no?(deg?(deg+'번은 딱 일직선이 되어 삼각형이 되지 못했다.'):'두 변이 만나지 못한 경우다.'):'8, 3, 4처럼 안 되는 경우도 기록해 보자.'}
    ];
    var concl;
    if(yes===0||no===0){
      concl='<b>더 해 보자</b> — 삼각형이 <b>되는 경우와 안 되는 경우</b>를 모두 기록해야 조건을 찾을 수 있다.';
    } else if(match===rec.length){
      concl='<b>정리</b> — 세 변의 길이가 주어졌다고 항상 삼각형이 되는 것은 아니었다. '
           +'<b>가장 긴 변보다 나머지 두 변의 합이 커야</b>만 두 변이 만나 꼭짓점을 만들었다. '
           +'딱 같으면 일직선이 되어 삼각형이 되지 못한다.';
    } else {
      concl='<b>확인 필요</b> — 작도 결과와 부등식 판정이 어긋난 기록이 있다.';
    }
    return {head:['세 변','가장 긴 변','나머지 합','삼각형?','부등식','일치?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 다각형의 내각과 외각
# ============================================================
LAB_POLY = BASE + r"""
function verts(n){
  var p=[],i;
  for(i=0;i<n;i++){
    var a=(-90+360*i/n+9*Math.sin(i*2.1+n))*Math.PI/180;
    p.push([220+120*Math.cos(a),178+120*Math.sin(a)]);
  }
  return p;
}
var LAB = {
  cw:440, ch:430, cvTitle:'다각형 분할판',
  action:'대각선으로 나누기',
  hint0:'변의 수를 정하고, 한 꼭짓점에서 대각선을 그어 삼각형으로 나눠 보자.',
  sliders:[
    {id:'n',label:'변의 수',min:3,max:12,value:6,color:'#2563eb',unit:'각형'}
  ],
  angs:function(S){
    var p=verts(S.n), a=[],i;
    for(i=0;i<S.n;i++){ a.push(angDeg(p[(i+S.n-1)%S.n],p[i],p[(i+1)%S.n])); }
    return a;
  },
  readout:function(S,ran){
    var a=this.angs(S), s=0,i;
    for(i=0;i<a.length;i++) s+=a[i];
    return [{k:'삼각형 개수',v:ran?((S.n-2)+'개'):'나눠 보자'},
            {k:'내각의 합',v:ran?(r1(s)+'°'):'-'}];
  },
  doneMsg:function(S){
    var a=this.angs(S), s=0,i;
    for(i=0;i<a.length;i++) s+=a[i];
    return '삼각형 '+(S.n-2)+'개로 나뉘었고 내각의 합은 '+r1(s)+'°다. ('+S.n+'−2)×180 = '+((S.n-2)*180)+'와 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var p=verts(S.n), a=this.angs(S), i;
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*(S.n-3));
    ctx.beginPath();
    for(i=0;i<S.n;i++){ if(i===0) ctx.moveTo(p[i][0],p[i][1]); else ctx.lineTo(p[i][0],p[i][1]); }
    ctx.closePath();
    ctx.fillStyle='rgba(37,99,235,0.10)';ctx.fill();
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.stroke();
    for(i=2;i<S.n-1;i++){
      if((i-2)>=shown) break;
      ctx.beginPath();ctx.moveTo(p[0][0],p[0][1]);ctx.lineTo(p[i][0],p[i][1]);
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=2.2;ctx.stroke();
    }
    for(i=0;i<S.n;i++){
      ctx.beginPath();ctx.arc(p[i][0],p[i][1],4.5,0,Math.PI*2);
      ctx.fillStyle='#1f2937';ctx.fill();
    }
    if(t!==null&&t>=1&&S.n<=8){
      ctx.font='bold 12px sans-serif';ctx.textAlign='center';
      for(i=0;i<S.n;i++){
        var dx=(220-p[i][0])*0.18, dy=(178-p[i][1])*0.18;
        ctx.fillStyle='#334155';
        ctx.fillText(r1(a[i])+'°',p[i][0]+dx,p[i][1]+dy+4);
      }
      ctx.textAlign='left';
    }
    lbl(ctx,S.n+'각형을 한 꼭짓점에서 대각선으로 나누기',24,34,'#1d4ed8',18);
    var s=0; for(i=0;i<a.length;i++) s+=a[i];
    box(ctx,20,318,400,94);
    lbl(ctx,(t===null)?'삼각형 몇 개로 나뉠까?':('삼각형 '+(S.n-2)+'개  →  180° × '+(S.n-2)+' = '+((S.n-2)*180)+'°'),38,350,'#1f2937',19);
    lbl(ctx,(t===null)?'':('실제 내각의 합 : '+r1(s)+'°'),38,380,'#15803d',19);
    lbl(ctx,(t===null)?'':('외각의 합 : '+r1(S.n*180-s)+'°'),38,404,'#b45309',17);
  },
  record:function(S){
    var a=this.angs(S), s=0,i;
    for(i=0;i<a.length;i++) s+=a[i];
    return {n:S.n,tri:S.n-2,formula:(S.n-2)*180,sum:r1(s),ext:r1(S.n*180-s)};
  },
  headA:['번호','다각형','삼각형 개수','(n−2)×180','실제 내각의 합','같은가?','외각의 합'],
  rowA:function(r,i){
    var ok=(Math.abs(r.sum-r.formula)<0.3);
    return [i+1,r.n+'각형',r.tri,r.formula+'°','<b>'+r.sum+'°</b>',
            '<span class="'+(ok?'ok':'no')+'">'+(ok?'○':'×')+'</span>',r.ext+'°'];
  },
  analyze:function(rec){
    var rows=[],ok=0,ext=0,ns={};
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var a=(Math.abs(r.sum-r.formula)<0.3), b=(Math.abs(r.ext-360)<0.5);
      if(a) ok++;
      if(b) ext++;
      ns[r.n]=true;
      rows.push([r.n+'각형', r.tri+'개', r.formula+'°', '<b>'+r.sum+'°</b>',
                 '<span class="'+(a?'ok':'no')+'">'+(a?'○':'×')+'</span>',
                 r.ext+'°',
                 '<span class="'+(b?'ok':'no')+'">'+(b?'○':'×')+'</span>']);
    }
    var kn=0; for(var k in ns) kn++;
    var stats=[
      {t:'내각의 합 = (n−2)×180°',big:ok+' / '+rec.length,p:'좌표에서 직접 잰 각의 합과 공식이 일치했는지 확인한 결과.'},
      {t:'외각의 합 = 360°',big:ext+' / '+rec.length,p:'변의 수와 상관없이 일정했는지 확인한 결과.'},
      {t:'시험한 다각형',big:kn+'가지',p:kn>1?'변의 수를 바꿔도 규칙이 유지되었다.':'변의 수를 바꿔 더 기록해 보자.'}
    ];
    var concl;
    if(ok===rec.length && ext===rec.length){
      concl='<b>정리</b> — n각형은 한 꼭짓점에서 대각선을 그으면 <b>(n−2)개의 삼각형</b>으로 나뉘었고, '
           +'내각의 합은 언제나 180° × (n−2)였다. 반대로 <b>외각의 합은 변의 수와 상관없이 항상 360°</b>였다. '
           +'변이 늘면 내각의 합은 커지지만 외각의 합은 그대로다.';
    } else {
      concl='<b>확인 필요</b> — 공식과 다른 기록이 있다.';
    }
    return {head:['다각형','삼각형','(n−2)×180','내각의 합','같은가?','외각의 합','360°인가?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 부채꼴
# ============================================================
LAB_SECTOR = BASE + r"""
var LAB = {
  cw:440, ch:420, cvTitle:'부채꼴 실험판',
  action:'호와 넓이 재기',
  hint0:'반지름과 중심각을 정하고, 호의 길이·넓이·현의 길이를 재 보자.',
  sliders:[
    {id:'r',label:'반지름',min:30,max:120,value:80,color:'#2563eb',fmt:function(v){return (v/20).toFixed(1)+'cm';}},
    {id:'th',label:'중심각',min:10,max:350,value:90,color:'#f59e0b',unit:'°'}
  ],
  calc:function(S){
    var r=S.r/20, th=S.th;
    var arc=2*Math.PI*r*th/360;
    var area=Math.PI*r*r*th/360;
    var chord=2*r*Math.sin(th/2*Math.PI/180);
    return {r:r,arc:arc,area:area,chord:chord};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'호의 길이',v:ran?(r2(c.arc)+'cm'):'재 보자'},
            {k:'넓이',v:ran?(r2(c.area)+'cm²'):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '호 '+r2(c.arc)+'cm, 넓이 '+r2(c.area)+'cm², 현 '+r2(c.chord)+'cm. 같은 반지름에서 중심각만 바꿔 다시 재 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var CX=220, CY=190, R=S.r;
    var grow=(t===null)?0:Math.min(1,t);
    var th=S.th*grow;
    ctx.beginPath();ctx.arc(CX,CY,R,0,Math.PI*2);
    ctx.strokeStyle='#e2e8f0';ctx.lineWidth=2;ctx.stroke();
    ctx.beginPath();ctx.moveTo(CX,CY);
    ctx.arc(CX,CY,R,-Math.PI/2,-Math.PI/2+th*Math.PI/180);
    ctx.closePath();
    ctx.fillStyle='rgba(37,99,235,0.20)';ctx.fill();
    ctx.strokeStyle='#2563eb';ctx.lineWidth=2.5;ctx.stroke();
    ctx.beginPath();
    ctx.arc(CX,CY,R,-Math.PI/2,-Math.PI/2+th*Math.PI/180);
    ctx.strokeStyle='#dc2626';ctx.lineWidth=5;ctx.stroke();
    var a2=-Math.PI/2+th*Math.PI/180;
    ctx.beginPath();ctx.moveTo(CX,CY-R);ctx.lineTo(CX+R*Math.cos(a2),CY+R*Math.sin(a2));
    ctx.strokeStyle='#16a34a';ctx.lineWidth=3;ctx.setLineDash([6,4]);ctx.stroke();ctx.setLineDash([]);
    lbl(ctx,'빨강 = 호,  초록 점선 = 현',24,36,'#52627a',16);
    lbl(ctx,'반지름 '+c.r.toFixed(1)+'cm, 중심각 '+S.th+'°',24,60,'#1d4ed8',18);
    box(ctx,20,326,400,84);
    lbl(ctx,(t===null)?'중심각이 2배가 되면 호도 2배일까?':
        ('호 '+r2(c.arc)+'cm   넓이 '+r2(c.area)+'cm²   현 '+r2(c.chord)+'cm'),38,356,'#1f2937',18);
    lbl(ctx,(t===null)?'':('호÷중심각 '+r2(c.arc/S.th*100)/100+'   현÷중심각 '+Math.round(c.chord/S.th*1000)/1000),
        38,388,'#52627a',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {r:r2(c.r),th:S.th,arc:r2(c.arc),area:r2(c.area),chord:r2(c.chord),
            aq:Math.round(c.arc/S.th*1000)/1000,
            sq:Math.round(c.area/S.th*1000)/1000,
            cq:Math.round(c.chord/S.th*1000)/1000};
  },
  headA:['번호','반지름','중심각','호','넓이','현','호÷중심각','넓이÷중심각','현÷중심각'],
  rowA:function(r,i){
    return [i+1,r.r+'cm',r.th+'°','<b>'+r.arc+'</b>',r.area,r.chord,r.aq,r.sq,r.cq];
  },
  analyze:function(rec){
    var rows=[],g={},i,k;
    for(i=0;i<rec.length;i++){
      var r=rec[i];
      if(!g[r.r]) g[r.r]={a:{},s:{},c:{},n:0};
      g[r.r].a[r.aq]=true; g[r.r].s[r.sq]=true; g[r.r].c[r.cq]=true; g[r.r].n++;
      rows.push([r.r+'cm', r.th+'°', r.arc, r.area, r.chord, r.aq, r.sq, r.cq]);
    }
    var tested=0,arcOk=0,areaOk=0,chordOk=0;
    for(k in g){
      var x=g[k]; if(x.n<2) continue;
      tested++;
      var an=0,sn=0,cn=0,kk;
      for(kk in x.a) an++;
      for(kk in x.s) sn++;
      for(kk in x.c) cn++;
      if(an===1) arcOk++;
      if(sn===1) areaOk++;
      if(cn===1) chordOk++;
    }
    var stats=[
      {t:'같은 반지름으로 2번 이상 기록한 경우',big:tested+'가지',
       p:tested?'반지름을 고정하고 중심각만 바꾼 묶음.':'같은 반지름에서 중심각만 바꿔 두 번 이상 기록해 보자.'},
      {t:'호 ÷ 중심각이 일정했던 묶음',big:tested?(arcOk+' / '+tested):'비교 없음',
       p:'넓이 ÷ 중심각이 일정했던 묶음은 '+areaOk+'가지.'},
      {t:'현 ÷ 중심각이 일정했던 묶음',big:tested?(chordOk+' / '+tested):'비교 없음',
       p:'현은 중심각에 정비례하지 않는다.'}
    ];
    var concl;
    if(tested===0){
      concl='<b>더 해 보자</b> — 반지름을 그대로 두고 중심각만 바꿔 여러 번 기록해야 비교할 수 있다.';
    } else if(arcOk===tested && areaOk===tested && chordOk===0){
      concl='<b>정리</b> — 같은 원에서 <b>호의 길이와 넓이는 중심각에 정비례</b>했다(÷중심각이 일정). '
           +'하지만 <b>현의 길이는 정비례하지 않았다.</b> 중심각이 2배가 되어도 현은 2배가 되지 않는다. '
           +'중심각이 180°를 넘으면 현은 오히려 짧아지기까지 한다.';
    } else {
      concl='<b>정리</b> — 호와 넓이는 중심각에 정비례하는지, 현도 그런지 묶음별로 확인해 보자. 기록을 더 모으면 뚜렷해진다.';
    }
    return {head:['반지름','중심각','호','넓이','현','호÷각','넓이÷각','현÷각'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 다면체와 오일러 공식
# ============================================================
LAB_EULER = BASE + r"""
var KINDS=['각기둥','각뿔','각뿔대'];
function vef(kind,n){
  if(kind===0) return {v:2*n,e:3*n,f:n+2};
  if(kind===1) return {v:n+1,e:2*n,f:n+1};
  return {v:2*n,e:3*n,f:n+2};
}
var LAB = {
  cw:440, ch:420, cvTitle:'다면체 세기판',
  action:'꼭짓점·모서리·면 세기',
  hint0:'입체도형의 종류와 밑면의 변의 수를 정해 보자.',
  sliders:[
    {id:'kind',label:'입체도형',min:0,max:2,value:0,color:'#2563eb',fmt:function(v){return KINDS[v];}},
    {id:'n',label:'밑면의 변의 수',min:3,max:8,value:5,color:'#16a34a',unit:'각'}
  ],
  readout:function(S,ran){
    var x=vef(S.kind,S.n);
    return [{k:'도형',v:S.n+'각'+KINDS[S.kind]},
            {k:'꼭짓점·모서리·면',v:ran?(x.v+' , '+x.e+' , '+x.f):'세어 보자'}];
  },
  doneMsg:function(S){
    var x=vef(S.kind,S.n);
    return '꼭짓점 '+x.v+', 모서리 '+x.e+', 면 '+x.f+'. (꼭짓점) − (모서리) + (면) = '+(x.v-x.e+x.f)+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var n=S.n, i;
    var CX=200, CY=200, RX=90, RY=30, H=110;
    var topScale=(S.kind===2)?0.55:1;
    function ring(cy,rx,ry){
      var p=[],i2;
      for(i2=0;i2<n;i2++){
        var a=(-90+360*i2/n)*Math.PI/180;
        p.push([CX+rx*Math.cos(a),cy+ry*Math.sin(a)]);
      }
      return p;
    }
    var bot=ring(CY+H/2,RX,RY);
    var top=(S.kind===1)?null:ring(CY-H/2,RX*topScale,RY*topScale);
    var apex=[CX,CY-H/2-14];
    var prog=(t===null)?0:Math.min(1,t);
    function edge(p,q,col,w){
      ctx.beginPath();ctx.moveTo(p[0],p[1]);ctx.lineTo(q[0],q[1]);
      ctx.strokeStyle=col;ctx.lineWidth=w||2;ctx.stroke();
    }
    for(i=0;i<n;i++){ edge(bot[i],bot[(i+1)%n],'#94a3b8',2.2); }
    if(top){ for(i=0;i<n;i++){ edge(top[i],top[(i+1)%n],'#94a3b8',2.2); } }
    for(i=0;i<n;i++){
      if(top) edge(bot[i],top[i],'#cbd5e1',2);
      else edge(bot[i],apex,'#cbd5e1',2);
    }
    var pts=bot.concat(top?top:[apex]);
    var shown=Math.ceil(prog*pts.length);
    for(i=0;i<pts.length;i++){
      ctx.beginPath();ctx.arc(pts[i][0],pts[i][1],(i<shown)?6:3,0,Math.PI*2);
      ctx.fillStyle=(i<shown)?'#dc2626':'#e2e8f0';ctx.fill();
    }
    var x=vef(S.kind,S.n);
    lbl(ctx,n+'각'+KINDS[S.kind],24,36,'#1d4ed8',20);
    lbl(ctx,'꼭짓점 '+((prog>0)?shown:'?')+' / '+x.v,320,120,'#b91c1c',16);
    if(prog>=1){
      lbl(ctx,'모서리 '+x.e,320,148,'#475569',16);
      lbl(ctx,'면 '+x.f,320,176,'#475569',16);
    }
    box(ctx,20,318,400,90);
    lbl(ctx,(t===null)?'꼭짓점 − 모서리 + 면 은 얼마일까?':(x.v+' − '+x.e+' + '+x.f+' = '+(x.v-x.e+x.f)),38,352,'#1f2937',21);
    lbl(ctx,(t===null)?'':'도형을 바꿔도 같은 값이 나올까?',38,384,'#52627a',18);
  },
  record:function(S){
    var x=vef(S.kind,S.n);
    return {kind:S.kind,name:S.n+'각'+KINDS[S.kind],n:S.n,v:x.v,e:x.e,f:x.f,
            euler:x.v-x.e+x.f};
  },
  headA:['번호','도형','꼭짓점','모서리','면','꼭짓점−모서리+면'],
  rowA:function(r,i){
    return [i+1,r.name,r.v,r.e,r.f,'<b>'+r.euler+'</b>'];
  },
  analyze:function(rec){
    var rows=[],two=0,kinds={},kn=0,mx=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i], ok=(r.euler===2);
      if(ok) two++;
      kinds[r.kind]=true;
      if(r.e>mx) mx=r.e;
      rows.push([r.name, r.v, r.e, r.f, '<b>'+r.euler+'</b>',
                 '<span class="'+(ok?'ok':'no')+'">'+(ok?'○':'×')+'</span>']);
    }
    for(var k in kinds) kn++;
    var stats=[
      {t:'꼭짓점 − 모서리 + 면 = 2',big:two+' / '+rec.length,p:'모든 기록에서 같은 값이 나왔는지 확인한 결과.'},
      {t:'시험한 도형의 종류',big:kn+'가지',p:kn>1?'각기둥·각뿔·각뿔대를 비교했다.':'다른 종류도 기록해 보자.'},
      {t:'가장 모서리가 많았던 도형',big:mx+'개',p:'크기가 달라도 결과는 변하지 않았다.'}
    ];
    var concl;
    if(two===rec.length && kn>1){
      concl='<b>정리</b> — 각기둥이든 각뿔이든, 밑면이 삼각형이든 팔각형이든 <b>(꼭짓점) − (모서리) + (면)은 언제나 2</b>였다. '
           +'이것을 오일러의 다면체 정리라고 한다. 셋 중 둘만 알면 나머지 하나를 계산으로 구할 수 있다.';
    } else if(two===rec.length){
      concl='<b>정리</b> — 지금까지 모두 2가 나왔다. 다른 종류의 다면체로도 확인해 보자.';
    } else {
      concl='<b>확인 필요</b> — 2가 아닌 기록이 있다. 세는 방법을 다시 확인해 보자.';
    }
    return {head:['도형','꼭짓점','모서리','면','V−E+F','2인가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("m1_parallel_angles_lab.html",
     "평행선 실험실 — 동위각은 항상 같을까?",
     "평행선 실험실 — 동위각은 항상 같을까?",
     "두 직선의 기울기를 바꿔 가며 동위각을 재고, 같아지는 조건이 무엇인지 기록한다.",
     LAB_PARALLEL),
    ("m1_triangle_inequality_lab.html",
     "삼각형 작도 실험실 — 세 변만 있으면 삼각형이 될까?",
     "삼각형 작도 실험실 — 세 변만 있으면 삼각형이 될까?",
     "세 변의 길이로 실제 작도를 시도하고, 삼각형이 되는 경우와 안 되는 경우의 조건을 찾는다.",
     LAB_TRIIN),
    ("m1_polygon_angles_lab.html",
     "다각형 실험실 — 변이 늘면 외각의 합도 늘까?",
     "다각형 실험실 — 변이 늘면 외각의 합도 늘까?",
     "다각형을 대각선으로 삼각형으로 나누며 내각의 합과 외각의 합을 각각 기록한다.",
     LAB_POLY),
    ("m1_sector_lab.html",
     "부채꼴 실험실 — 중심각이 2배면 무엇이 2배일까?",
     "부채꼴 실험실 — 중심각이 2배면 무엇이 2배일까?",
     "반지름을 고정하고 중심각만 바꿔 호·넓이·현을 재고, 무엇이 중심각에 정비례하는지 확인한다.",
     LAB_SECTOR),
    ("m1_euler_polyhedron_lab.html",
     "다면체 실험실 — 꼭짓점·모서리·면 사이의 관계는?",
     "다면체 실험실 — 꼭짓점·모서리·면 사이의 관계는?",
     "각기둥·각뿔·각뿔대의 꼭짓점·모서리·면을 세어 세 수 사이의 관계를 찾는다.",
     LAB_EULER),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c11_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
