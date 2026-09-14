# -*- coding: utf-8 -*-
"""중3 수와 연산 2종 + 변화와 관계 3종"""
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
function pn(v){return (v<0)?('('+v+')'):(''+v);}
function sg(v){return (v<0)?(' − '+(-v)):(' + '+v);}
"""

# ============================================================
# 1. √a + √b 와 √(a+b)
# ============================================================
LAB_SQSUM = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'제곱근 길이 비교판',
  action:'길이를 재어 비교하기',
  hint0:'두 수를 정하고, 제곱근의 합과 합의 제곱근을 비교해 보자.',
  sliders:[
    {id:'a',label:'a',min:1,max:50,value:9,color:'#2563eb',unit:''},
    {id:'b',label:'b',min:1,max:50,value:16,color:'#16a34a',unit:''}
  ],
  calc:function(S){
    var sa=Math.sqrt(S.a), sb=Math.sqrt(S.b);
    return {sa:sa,sb:sb,sum:sa+sb,sq:Math.sqrt(S.a+S.b),
            prod:Math.sqrt(S.a*S.b),sqprod:Math.sqrt(S.a)*Math.sqrt(S.b),
            gap:(sa+sb)-Math.sqrt(S.a+S.b)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'√a + √b',v:ran?r3(c.sum):'재 보자'},
            {k:'√(a+b)',v:ran?r3(c.sq):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '√a+√b = '+r3(c.sum)+', √(a+b) = '+r3(c.sq)+'.  차이 '+r3(c.gap)+'.  곱은 어떤지도 확인해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var U=Math.min(26, 340/Math.max(c.sum,c.sq));
    var X0=44;
    var grow=(t===null)?0:Math.min(1,t);
    function bar(y,len,col,label){
      ctx.fillStyle=col;ctx.fillRect(X0,y,len*U*grow,26);
      ctx.strokeStyle='#334155';ctx.lineWidth=2;ctx.strokeRect(X0,y,len*U*grow,26);
      if(grow>=1) lbl(ctx,label,X0+len*U+8,y+19,'#334155',15);
    }
    lbl(ctx,'√'+S.a+' = '+r3(c.sa)+'    √'+S.b+' = '+r3(c.sb),24,38,'#1d4ed8',18);
    ctx.fillStyle='#bfdbfe';ctx.fillRect(X0,80,c.sa*U*grow,26);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=2;ctx.strokeRect(X0,80,c.sa*U*grow,26);
    ctx.fillStyle='#bbf7d0';ctx.fillRect(X0+c.sa*U*grow,80,c.sb*U*grow,26);
    ctx.strokeStyle='#16a34a';ctx.strokeRect(X0+c.sa*U*grow,80,c.sb*U*grow,26);
    if(grow>=1) lbl(ctx,'√a + √b = '+r3(c.sum),X0,74,'#334155',15);
    bar(140,c.sq,'#fde68a','√(a+b) = '+r3(c.sq));
    if(grow>=1){
      lbl(ctx,'√(a+b)',X0,134,'#b45309',15);
      ctx.strokeStyle='#dc2626';ctx.lineWidth=2;ctx.setLineDash([4,4]);
      ctx.beginPath();ctx.moveTo(X0+c.sq*U,74);ctx.lineTo(X0+c.sq*U,172);ctx.stroke();ctx.setLineDash([]);
    }
    box(ctx,20,206,400,178);
    lbl(ctx,(t===null)?'두 길이는 같을까?':('√a + √b = '+r3(c.sum)),38,240,'#1f2937',20);
    lbl(ctx,(t===null)?'':('√(a+b) = √'+(S.a+S.b)+' = '+r3(c.sq)),38,272,'#b45309',20);
    lbl(ctx,(t===null)?'':('차이 : '+r3(c.gap)),38,302,'#b91c1c',18);
    lbl(ctx,(t===null)?'':('√a × √b = '+r3(c.sqprod)+'      √(ab) = √'+(S.a*S.b)+' = '+r3(c.prod)),38,338,'#15803d',17);
    lbl(ctx,(t===null)?'':'곱셈에서는 어떤가?',38,368,'#52627a',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,sa:r3(c.sa),sb:r3(c.sb),sum:r3(c.sum),sq:r3(c.sq),
            gap:r3(c.gap),same:(Math.abs(c.gap)<1e-9),
            prod:r3(c.prod),sqprod:r3(c.sqprod),
            prodSame:(Math.abs(c.prod-c.sqprod)<1e-9)};
  },
  headA:['번호','a, b','√a + √b','√(a+b)','같은가?','차이','√a × √b','√(ab)','같은가?'],
  rowA:function(r,i){
    return [i+1,r.a+', '+r.b,'<b>'+r.sum+'</b>',r.sq,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            r.gap,r.sqprod,r.prod,
            '<span class="'+(r.prodSame?'ok':'no')+'">'+(r.prodSame?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,psame=0,mn=999,mx=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.prodSame) psame++;
      if(r.gap<mn) mn=r.gap;
      if(r.gap>mx) mx=r.gap;
      rows.push([r.a+', '+r.b, r.sum, r.sq,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 r.gap, r.sqprod+' / '+r.prod,
                 '<span class="'+(r.prodSame?'ok':'no')+'">'+(r.prodSame?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'√a + √b = √(a+b) 였던 횟수',big:same+' / '+rec.length,
       p:'덧셈에서 근호를 따로 씌워도 되는지 확인한 결과.'},
      {t:'√a × √b = √(ab) 였던 횟수',big:psame+' / '+rec.length,
       p:'곱셈에서는 어떤지 확인한 결과.'},
      {t:'차이의 범위',big:mn+' ~ '+mx,
       p:'항상 √a+√b 쪽이 더 컸다. 차이가 0이 된 적은 없다.'}
    ];
    var concl;
    if(same===0&&psame===rec.length){
      concl='<b>정리</b> — <b>덧셈에서는 √a + √b ≠ √(a+b)</b>였다. 한 번도 같지 않았고, 언제나 왼쪽이 더 컸다. '
           +'(√a+√b)² = a + b + 2√(ab)라서 2√(ab)만큼 더 크기 때문이다. '
           +'반면 <b>곱셈에서는 √a × √b = √(ab)</b>가 언제나 성립했다. 근호는 곱셈·나눗셈과는 자유롭게 오가지만 덧셈과는 그렇지 않다.';
    } else if(same>0){
      concl='<b>확인 필요</b> — 덧셈에서 두 값이 같게 나온 기록이 있다. 값을 다시 확인해 보자.';
    } else {
      concl='<b>정리</b> — 덧셈에서는 두 값이 달랐다. 곱셈도 함께 기록해 비교해 보자.';
    }
    return {head:['a, b','√a+√b','√(a+b)','같은가?','차이','√a×√b / √(ab)','같은가?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. √(a²) 와 a
# ============================================================
LAB_SQABS = BASE + r"""
var LAB = {
  cw:440, ch:380, cvTitle:'제곱근 부호판',
  action:'제곱하고 근호 씌우기',
  hint0:'수를 정하고, 제곱한 뒤 다시 근호를 씌우면 무엇이 되는지 보자.',
  sliders:[
    {id:'a',label:'수 a',min:-10,max:10,value:-6,color:'#2563eb',unit:''}
  ],
  calc:function(S){
    var sq=S.a*S.a;
    return {sq:sq,root:Math.sqrt(sq),abs:Math.abs(S.a),same:(Math.sqrt(sq)===S.a)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'a²',v:c.sq},
            {k:'√(a²)',v:ran?c.root:'구해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'a = '+S.a+' → a² = '+c.sq+' → √(a²) = '+c.root+'.  '+(c.same?'a와 같다.':'a와 다르다! −a와 같다.')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var X0=30, X1=410, LO=-12, HI=12;
    function px(v){ return X0+(X1-X0)*(v-LO)/(HI-LO); }
    var Y=200;
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(X0,Y);ctx.lineTo(X1,Y);ctx.stroke();
    for(i=LO;i<=HI;i++){
      var x=px(i), big=(i%2===0);
      ctx.beginPath();ctx.moveTo(x,Y-(big?8:4));ctx.lineTo(x,Y+(big?8:4));
      ctx.strokeStyle=big?'#64748b':'#cbd5e1';ctx.lineWidth=big?1.8:1;ctx.stroke();
      if(big){ ctx.fillStyle='#94a3b8';ctx.font='11px sans-serif';ctx.textAlign='center';ctx.fillText(i,x,Y+22); }
    }
    ctx.textAlign='left';
    var p1=(t===null)?0:Math.min(1,t/0.5);
    var p2=(t===null)?0:Math.max(0,(t-0.5)/0.5);
    ctx.beginPath();ctx.arc(px(S.a),Y,9,0,Math.PI*2);
    ctx.fillStyle='#2563eb';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
    lbl(ctx,'a = '+S.a,px(S.a),Y-18,'#1d4ed8',15,'center');
    if(p2>0){
      var xr=px(S.a)+(px(c.root)-px(S.a))*p2;
      ctx.beginPath();ctx.arc(xr,Y+36,9,0,Math.PI*2);
      ctx.fillStyle='#dc2626';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      if(p2>=1) lbl(ctx,'√(a²) = '+c.root,xr,Y+68,'#b91c1c',15,'center');
    }
    lbl(ctx,'a를 제곱했다가 근호를 씌우면?',24,38,'#1d4ed8',19);
    lbl(ctx,'a = '+S.a+'   →   a² = '+c.sq+((p1>0)?('   →   √'+c.sq+' = '+c.root):''),24,82,'#334155',20);
    box(ctx,20,286,400,80);
    lbl(ctx,(t===null)?'√(a²)은 언제나 a일까?':('√(a²) = '+c.root+'      |a| = '+c.abs),38,318,'#1f2937',20);
    lbl(ctx,(t===null)?'':(c.same?'a가 0 이상이라 a와 같다':'a가 음수라 −a와 같다'),38,350,c.same?'#15803d':'#b91c1c',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,sq:c.sq,root:c.root,abs:c.abs,same:c.same,
            absOk:(c.root===c.abs),neg:(S.a<0)};
  },
  headA:['번호','a','a²','√(a²)','|a|','√(a²) = a?','√(a²) = |a|?'],
  rowA:function(r,i){
    return [i+1,r.a,r.sq,'<b>'+r.root+'</b>',r.abs,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            '<span class="'+(r.absOk?'ok':'no')+'">'+(r.absOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,absOk=0,neg=0,negSame=0,pos=0,posSame=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.absOk) absOk++;
      if(r.neg){ neg++; if(r.same) negSame++; }
      else { pos++; if(r.same) posSame++; }
      rows.push([r.a, r.sq, '<b>'+r.root+'</b>', r.abs,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 '<span class="'+(r.absOk?'ok':'no')+'">'+(r.absOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'√(a²) = a 였던 횟수',big:same+' / '+rec.length,p:'그냥 a로 두면 되는지 확인한 결과.'},
      {t:'√(a²) = |a| 였던 횟수',big:absOk+' / '+rec.length,p:'절댓값으로 쓰면 어떤지 확인한 결과.'},
      {t:'a가 음수 / 0 이상',big:neg+'개 / '+pos+'개',
       p:'음수에서 a와 같았던 횟수 '+negSame+', 0 이상에서 '+posSame+'.'}
    ];
    var concl;
    if(neg===0||pos===0){
      concl='<b>더 해 보자</b> — a가 음수인 경우와 0 이상인 경우를 <b>모두</b> 기록해야 조건이 보인다.';
    } else if(absOk===rec.length&&negSame===0){
      concl='<b>정리</b> — √(a²)은 a가 0 이상일 때만 a와 같았고, <b>음수일 때는 −a</b>가 되었다. '
           +'근호는 항상 0 이상인 값을 내놓기 때문이다. 그래서 <b>√(a²) = |a|</b>로 써야 언제나 맞는다. '
           +'문자를 다룰 때 a의 부호를 모르면 근호를 함부로 벗길 수 없다.';
    } else {
      concl='<b>확인 필요</b> — 규칙과 어긋난 기록이 있다.';
    }
    return {head:['a','a²','√(a²)','|a|','a와 같나?','|a|와 같나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. (a+b)² 곱셈공식
# ============================================================
LAB_SQEXP = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'정사각형 넓이판',
  action:'넓이를 나누어 세기',
  hint0:'두 길이를 정하고, 한 변이 a+b인 정사각형의 넓이를 나눠 보자.',
  sliders:[
    {id:'a',label:'a',min:1,max:9,value:5,color:'#2563eb',unit:''},
    {id:'b',label:'b',min:1,max:9,value:3,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var whole=(S.a+S.b)*(S.a+S.b);
    return {whole:whole,aa:S.a*S.a,bb:S.b*S.b,ab:S.a*S.b,
            wrong:S.a*S.a+S.b*S.b,gap:whole-(S.a*S.a+S.b*S.b)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'(a+b)²',v:ran?c.whole:'세어 보자'},
            {k:'a² + b²',v:c.wrong}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '(a+b)² = '+c.whole+', a²+b² = '+c.wrong+'.  차이 '+c.gap+'은 직사각형 두 개('+S.a+'×'+S.b+') 넓이다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var U=Math.min(17, 250/(S.a+S.b));
    var X=90, Y=70;
    var A=S.a*U, B=S.b*U;
    var show=(t===null)?0:Math.min(1,t);
    ctx.fillStyle='rgba(37,99,235,0.28)';ctx.fillRect(X,Y,A,A);
    if(show>0.25){ ctx.fillStyle='rgba(148,163,184,0.30)';ctx.fillRect(X+A,Y,B,A); }
    if(show>0.5){ ctx.fillStyle='rgba(148,163,184,0.30)';ctx.fillRect(X,Y+A,A,B); }
    if(show>0.75){ ctx.fillStyle='rgba(245,158,11,0.35)';ctx.fillRect(X+A,Y+A,B,B); }
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.strokeRect(X,Y,A+B,A+B);
    ctx.beginPath();ctx.moveTo(X+A,Y);ctx.lineTo(X+A,Y+A+B);
    ctx.moveTo(X,Y+A);ctx.lineTo(X+A+B,Y+A);ctx.stroke();
    ctx.font='bold 14px sans-serif';ctx.textAlign='center';
    if(show>0){ ctx.fillStyle='#1d4ed8';ctx.fillText('a² = '+c.aa,X+A/2,Y+A/2+5); }
    if(show>0.25){ ctx.fillStyle='#475569';ctx.fillText('ab = '+c.ab,X+A+B/2,Y+A/2+5); }
    if(show>0.5){ ctx.fillStyle='#475569';ctx.fillText('ab = '+c.ab,X+A/2,Y+A+B/2+5); }
    if(show>0.75){ ctx.fillStyle='#b45309';ctx.fillText('b² = '+c.bb,X+A+B/2,Y+A+B/2+5); }
    ctx.textAlign='left';
    lbl(ctx,'한 변이 a+b = '+(S.a+S.b)+'인 정사각형',24,38,'#1d4ed8',18);
    box(ctx,20,330,400,84);
    lbl(ctx,(t===null)?'(a+b)²은 a²+b²일까?':('(a+b)² = '+c.aa+' + '+c.ab+' + '+c.ab+' + '+c.bb+' = '+c.whole),38,362,'#1f2937',18);
    lbl(ctx,(t===null)?'':('a² + b² = '+c.wrong+'      차이 '+c.gap+' = 2ab'),38,394,'#b91c1c',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,whole:c.whole,wrong:c.wrong,gap:c.gap,twoab:2*S.a*S.b,
            same:(c.whole===c.wrong),gapOk:(c.gap===2*S.a*S.b)};
  },
  headA:['번호','a, b','(a+b)²','a² + b²','같은가?','차이','2ab','차이 = 2ab?'],
  rowA:function(r,i){
    return [i+1,r.a+', '+r.b,'<b>'+r.whole+'</b>',r.wrong,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            r.gap,r.twoab,
            '<span class="'+(r.gapOk?'ok':'no')+'">'+(r.gapOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,gapOk=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.gapOk) gapOk++;
      rows.push([r.a+', '+r.b, '<b>'+r.whole+'</b>', r.wrong,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 r.gap, r.twoab,
                 '<span class="'+(r.gapOk?'ok':'no')+'">'+(r.gapOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'(a+b)² = a² + b² 였던 횟수',big:same+' / '+rec.length,
       p:'괄호 안 각 항을 따로 제곱하면 되는지 확인한 결과.'},
      {t:'차이 = 2ab 였던 횟수',big:gapOk+' / '+rec.length,
       p:'빠진 부분이 정확히 직사각형 두 개인지 확인한 결과.'},
      {t:'기록 수',big:rec.length+'개',p:'a와 b를 여러 값으로 바꿔 확인했다.'}
    ];
    var concl;
    if(same===0&&gapOk===rec.length){
      concl='<b>정리</b> — (a+b)²은 <b>한 번도</b> a² + b²과 같지 않았고, 차이는 언제나 정확히 <b>2ab</b>였다. '
           +'그림에서 보면 큰 정사각형은 a², b² 말고도 a×b 직사각형 <b>두 개</b>를 더 포함한다. '
           +'그래서 (a+b)² = a² + 2ab + b²이다. 제곱은 각 항에 따로 나눠 줄 수 없다.';
    } else if(same>0){
      concl='<b>확인 필요</b> — 두 값이 같게 나온 기록이 있다.';
    } else {
      concl='<b>정리</b> — 두 값은 항상 달랐다. 차이가 2ab인지도 함께 확인해 보자.';
    }
    return {head:['a, b','(a+b)²','a²+b²','같은가?','차이','2ab','일치?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 인수분해 확인
# ============================================================
LAB_FACT = BASE + r"""
var FORMS=['x² − b²','x² − 2bx + b²','x² + b²'];
var LAB = {
  cw:440, ch:400, cvTitle:'인수분해 검산판',
  action:'값을 넣어 검산하기',
  hint0:'식의 모양과 b, 그리고 x에 넣을 값을 정해 보자.',
  sliders:[
    {id:'form',label:'식의 모양',min:0,max:2,value:0,color:'#2563eb',fmt:function(v){return FORMS[v];}},
    {id:'b',label:'b',min:1,max:9,value:3,color:'#16a34a',unit:''},
    {id:'x',label:'x에 넣을 값',min:-8,max:8,value:5,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var x=S.x,b=S.b,orig;
    if(S.form===0) orig=x*x-b*b;
    else if(S.form===1) orig=x*x-2*b*x+b*b;
    else orig=x*x+b*b;
    var c1=(x-b)*(x+b);
    var c2=(x-b)*(x-b);
    return {orig:orig,c1:c1,c2:c2,ok1:(orig===c1),ok2:(orig===c2)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'원래 식의 값',v:ran?c.orig:'계산해 보자'},
            {k:'(x−b)(x+b) / (x−b)²',v:ran?(c.c1+' / '+c.c2):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    var which=c.ok1?'(x−b)(x+b)':(c.ok2?'(x−b)²':'둘 다 아님');
    return '원래 식은 '+c.orig+'.  맞는 인수분해는 '+which+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var p1=(t===null)?0:Math.min(1,t/0.4);
    var p2=(t===null)?0:Math.max(0,Math.min(1,(t-0.4)/0.3));
    var p3=(t===null)?0:Math.max(0,(t-0.7)/0.3);
    var es=(S.form===0)?('x² − '+(S.b*S.b)):((S.form===1)?('x² − '+(2*S.b)+'x + '+(S.b*S.b)):('x² + '+(S.b*S.b)));
    lbl(ctx,'식 : '+es+'   (b = '+S.b+')',24,40,'#1d4ed8',19);
    lbl(ctx,'x = '+S.x+' 를 넣어 검산',24,72,'#52627a',17);
    if(p1>0){ ctx.globalAlpha=p1; lbl(ctx,'원래 식 = '+c.orig,40,120,'#1f2937',24); ctx.globalAlpha=1; }
    if(p2>0){
      ctx.globalAlpha=p2;
      lbl(ctx,'(x − '+S.b+')(x + '+S.b+') = '+(S.x-S.b)+' × '+(S.x+S.b)+' = '+c.c1,40,166,
          c.ok1?'#15803d':'#b91c1c',20);
      ctx.globalAlpha=1;
    }
    if(p3>0){
      ctx.globalAlpha=p3;
      lbl(ctx,'(x − '+S.b+')² = '+(S.x-S.b)+'² = '+c.c2,40,208,c.ok2?'#15803d':'#b91c1c',20);
      ctx.globalAlpha=1;
    }
    box(ctx,20,240,400,144);
    lbl(ctx,(t===null)?'어떤 인수분해가 맞을까?':('원래 식 = '+c.orig),38,272,'#1f2937',20);
    lbl(ctx,(t===null)?'':('(x−b)(x+b) → '+c.c1+'  '+(c.ok1?'✔ 일치':'✘ 불일치')),38,308,c.ok1?'#15803d':'#b91c1c',18);
    lbl(ctx,(t===null)?'':('(x−b)² → '+c.c2+'  '+(c.ok2?'✔ 일치':'✘ 불일치')),38,340,c.ok2?'#15803d':'#b91c1c',18);
    lbl(ctx,(t===null)?'':'한 값만 맞았다고 끝이 아니다. 여러 x로 확인하자.',38,372,'#52627a',15);
  },
  record:function(S){
    var c=this.calc(S);
    return {form:S.form,name:FORMS[S.form],b:S.b,x:S.x,orig:c.orig,c1:c.c1,c2:c.c2,
            ok1:c.ok1,ok2:c.ok2};
  },
  headA:['번호','식','b','x','원래 값','(x−b)(x+b)','맞나?','(x−b)²','맞나?'],
  rowA:function(r,i){
    return [i+1,r.name,r.b,r.x,'<b>'+r.orig+'</b>',r.c1,
            '<span class="'+(r.ok1?'ok':'no')+'">'+(r.ok1?'○':'×')+'</span>',
            r.c2,
            '<span class="'+(r.ok2?'ok':'no')+'">'+(r.ok2?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],g={},k,lines=[],forms=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(!g[r.form]) g[r.form]={name:r.name,n:0,a1:0,a2:0};
      g[r.form].n++;
      if(r.ok1) g[r.form].a1++;
      if(r.ok2) g[r.form].a2++;
      rows.push([r.name+' (b='+r.b+')', 'x = '+r.x, '<b>'+r.orig+'</b>', r.c1,
                 '<span class="'+(r.ok1?'ok':'no')+'">'+(r.ok1?'○':'×')+'</span>',
                 r.c2,
                 '<span class="'+(r.ok2?'ok':'no')+'">'+(r.ok2?'○':'×')+'</span>']);
    }
    var alwaysOk=[],neverOk=[];
    for(k in g){
      forms++;
      var x=g[k];
      lines.push(x.name+' → (x−b)(x+b) '+x.a1+'/'+x.n+', (x−b)² '+x.a2+'/'+x.n);
      if(x.a1===x.n) alwaysOk.push(x.name);
    }
    var stats=[
      {t:'시험한 식의 모양',big:forms+'가지',p:lines.join(' / ')},
      {t:'(x−b)(x+b)가 언제나 맞은 식',big:alwaysOk.length+'가지',
       p:alwaysOk.join(', ')||'모든 x에서 맞아야 인수분해가 맞는 것이다.'},
      {t:'기록 수',big:rec.length+'개',p:'같은 식에서 x를 여러 개 넣어야 확실해진다.'}
    ];
    var concl;
    if(forms<2){
      concl='<b>더 해 보자</b> — 세 가지 식 모양을 <b>모두</b> 기록해야 어떤 인수분해가 어디에 맞는지 구별된다.';
    } else {
      concl='<b>정리</b> — x² − b²에는 (x−b)(x+b)가, x² − 2bx + b²에는 (x−b)²가 맞았고, '
           +'<b>x² + b²은 두 후보 어느 쪽도 맞지 않았다.</b>(유리수 범위에서 인수분해되지 않는다) '
           +'x² − b²을 (x−b)²로 쓰면 x를 바꾸는 순간 값이 어긋난다. '
           +'인수분해는 <b>모든 x에서 값이 같아야</b> 하므로, 전개하거나 여러 값을 넣어 검산하면 바로 확인할 수 있다.';
    }
    return {head:['식','대입','원래 값','(x−b)(x+b)','맞나?','(x−b)²','맞나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 이차방정식의 근의 개수
# ============================================================
LAB_DISC = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'포물선과 x축',
  action:'그래프 그리고 교점 찾기',
  hint0:'이차방정식의 계수를 정하고, 그래프가 x축과 몇 번 만나는지 보자.',
  sliders:[
    {id:'a',label:'a',min:-3,max:3,value:1,color:'#2563eb',unit:''},
    {id:'b',label:'b',min:-8,max:8,value:-2,color:'#16a34a',unit:''},
    {id:'c',label:'c',min:-8,max:8,value:-3,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    if(S.a===0) return {zero:true};
    var D=S.b*S.b-4*S.a*S.c;
    var n=(D>1e-9)?2:((D<-1e-9)?0:1);
    var r1v=null,r2v=null;
    if(n===2){ r1v=(-S.b-Math.sqrt(D))/(2*S.a); r2v=(-S.b+Math.sqrt(D))/(2*S.a); }
    else if(n===1){ r1v=-S.b/(2*S.a); }
    return {zero:false,D:D,n:n,r1:r1v,r2:r2v};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    if(c.zero) return [{k:'a = 0',v:'이차식이 아니다'},{k:'',v:'a를 바꾸자'}];
    return [{k:'b² − 4ac',v:c.D},
            {k:'x축과 만나는 횟수',v:ran?(c.n+'번'):'그려 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.zero) return 'a가 0이라 이차식이 아니다. a를 바꿔 보자.';
    return 'b²−4ac = '+c.D+'이고 x축과 '+c.n+'번 만난다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var CX=220, CY=230, U=22;
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=-9;i<=9;i++){ ctx.beginPath();ctx.moveTo(CX+i*U,CY-8*U);ctx.lineTo(CX+i*U,CY+3*U);ctx.stroke(); }
    for(i=-3;i<=8;i++){ ctx.beginPath();ctx.moveTo(CX-9*U,CY-i*U);ctx.lineTo(CX+9*U,CY-i*U);ctx.stroke(); }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(CX-9*U,CY);ctx.lineTo(CX+9*U,CY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(CX,CY-8*U);ctx.lineTo(CX,CY+3*U);ctx.stroke();
    if(c.zero){ lbl(ctx,'a = 0 이면 이차식이 아니다',24,38,'#b91c1c',19); return; }
    var grow=(t===null)?0:Math.min(1,t);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    var started=false;
    for(i=-90;i<=90;i++){
      var xx=i/10, yy=S.a*xx*xx+S.b*xx+S.c;
      if(yy<-3||yy>8){ started=false; continue; }
      var Px=CX+xx*U, Py=CY-yy*U;
      if(!started){ ctx.moveTo(Px,Py); started=true; } else ctx.lineTo(Px,Py);
    }
    if(grow>0) ctx.stroke();
    if(grow>=1){
      [c.r1,c.r2].forEach(function(rr){
        if(rr===null||Math.abs(rr)>9) return;
        ctx.beginPath();ctx.arc(CX+rr*U,CY,8,0,Math.PI*2);
        ctx.fillStyle='#dc2626';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      });
    }
    lbl(ctx,'y = '+S.a+'x²'+sg(S.b)+'x'+sg(S.c),24,32,'#1d4ed8',18);
    box(ctx,20,330,400,86);
    lbl(ctx,'b² − 4ac = '+(S.b*S.b)+' − '+(4*S.a*S.c)+' = '+c.D,38,362,'#1f2937',19);
    lbl(ctx,(t===null)?'x축과 몇 번 만날까?':('x축과 만나는 횟수 : '+c.n+'번'+((c.n>0)?('   x = '+r2(c.r1)+((c.n===2)?(', '+r2(c.r2)):'')):'')),
        38,394,(c.n===0)?'#b91c1c':'#15803d',18);
  },
  record:function(S){
    var c=this.calc(S);
    if(c.zero) return {zero:true,a:S.a,b:S.b,c:S.c};
    return {zero:false,a:S.a,b:S.b,c:S.c,D:c.D,n:c.n,
            r1:(c.r1===null)?'-':r2(c.r1),r2:(c.r2===null)?'-':r2(c.r2),
            sign:(c.D>0)?'양수':((c.D<0)?'음수':'0')};
  },
  headA:['번호','식','b²−4ac','부호','x축과 만나는 횟수','근'],
  rowA:function(r,i){
    if(r.zero) return [i+1,'a=0','-','-','이차식 아님','-'];
    return [i+1,r.a+'x²'+sg(r.b)+'x'+sg(r.c),r.D,r.sign,'<b>'+r.n+'번</b>',
            (r.n===0)?'없음':(r.r1+((r.n===2)?(', '+r.r2):''))];
  },
  analyze:function(rec){
    var rows=[],valid=0,match=0,g={pos:0,zero:0,neg:0};
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.zero){ rows.push(['a = 0','-','-','이차식 아님','-']); continue; }
      valid++;
      var expect=(r.D>0)?2:((r.D<0)?0:1);
      var m=(expect===r.n);
      if(m) match++;
      if(r.D>0) g.pos++; else if(r.D<0) g.neg++; else g.zero++;
      rows.push([r.a+'x²'+sg(r.b)+'x'+sg(r.c), r.D, r.sign, '<b>'+r.n+'번</b>',
                 '<span class="'+(m?'ok':'no')+'">'+(m?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'부호로 한 예측이 맞은 횟수',big:match+' / '+valid,
       p:'b²−4ac의 부호만 보고 교점 수를 맞힐 수 있는지 확인한 결과.'},
      {t:'b²−4ac 양수 / 0 / 음수',big:g.pos+' / '+g.zero+' / '+g.neg,
       p:(g.pos&&g.zero&&g.neg)?'세 경우를 모두 기록했다.':'세 경우를 모두 만들어 보자.'},
      {t:'기록 수',big:rec.length+'개',p:'a의 부호를 바꿔도 규칙이 유지되는지 확인해 보자.'}
    ];
    var concl;
    if(!(g.pos&&g.zero&&g.neg)){
      concl='<b>더 해 보자</b> — b²−4ac가 <b>양수·0·음수</b>인 경우를 모두 만들어야 규칙이 완성된다. '
           +'예를 들어 a=1, b=−2, c=1이면 0이 된다.';
    } else if(match===valid){
      concl='<b>정리</b> — <b>b² − 4ac가 양수면 2번, 0이면 1번, 음수면 만나지 않았다.</b> 예외는 없었다. '
           +'이차방정식의 실근의 개수는 곧 그래프가 x축과 만나는 횟수이고, 근의 공식 속 √ 안의 값이 그것을 결정한다. '
           +'근이 없다고 방정식이 틀린 것이 아니라, 그래프가 x축 위(또는 아래)에만 있는 것이다.';
    } else {
      concl='<b>확인 필요</b> — 부호 예측과 교점 수가 어긋난 기록이 있다.';
    }
    return {head:['식','b²−4ac','부호','교점 수','예측 일치?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("m3_sqrt_sum_lab.html",
     "제곱근 실험실 — √a + √b는 √(a+b)일까?",
     "제곱근 실험실 — √a + √b는 √(a+b)일까?",
     "두 제곱근의 합과 합의 제곱근을 길이로 나란히 재어 비교하고, 곱셈에서는 어떤지 함께 확인한다.",
     LAB_SQSUM),
    ("m3_sqrt_absolute_lab.html",
     "근호 실험실 — √(a²)은 항상 a일까?",
     "근호 실험실 — √(a²)은 항상 a일까?",
     "수를 제곱했다가 다시 근호를 씌우며 수직선에서 위치가 어떻게 되는지 기록한다.",
     LAB_SQABS),
    ("m3_square_expansion_lab.html",
     "곱셈공식 실험실 — (a+b)²은 a²+b²일까?",
     "곱셈공식 실험실 — (a+b)²은 a²+b²일까?",
     "한 변이 a+b인 정사각형의 넓이를 네 조각으로 나누어 세고, a²+b²과 비교한다.",
     LAB_SQEXP),
    ("m3_factorization_check_lab.html",
     "인수분해 실험실 — x² − b²은 (x−b)²일까?",
     "인수분해 실험실 — x² − b²은 (x−b)²일까?",
     "식에 여러 값을 대입해 두 인수분해 후보를 검산하고, 어떤 식에 어떤 꼴이 맞는지 가린다.",
     LAB_FACT),
    ("m3_discriminant_lab.html",
     "이차방정식 실험실 — 근은 항상 두 개일까?",
     "이차방정식 실험실 — 근은 항상 두 개일까?",
     "계수를 바꿔 포물선을 그리고 x축과 만나는 횟수를 b²−4ac의 부호와 대조한다.",
     LAB_DISC),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c17_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
