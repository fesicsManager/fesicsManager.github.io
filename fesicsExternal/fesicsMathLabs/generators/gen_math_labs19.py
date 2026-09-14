# -*- coding: utf-8 -*-
"""중3 보강 5종"""
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
function r6(v){return Math.round(v*1000000)/1000000;}
function sg(v){return (v<0)?(' − '+(-v)):(' + '+v);}
function isSq(n){ var s=Math.round(Math.sqrt(n)); return s*s===n; }
"""

# ============================================================
# 1. 무리수 작도
# ============================================================
LAB_IRR = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'무리수 작도판',
  action:'빗변을 수직선으로 옮기기',
  hint0:'직각을 낀 두 변을 정하면 빗변의 길이가 정해진다. 그 길이를 수직선에 옮겨 보자.',
  sliders:[
    {id:'a',label:'밑변',min:1,max:6,value:1,color:'#2563eb',unit:''},
    {id:'b',label:'높이',min:1,max:6,value:1,color:'#16a34a',unit:''}
  ],
  calc:function(S){
    var n=S.a*S.a+S.b*S.b;
    var v=Math.sqrt(n);
    return {n:n,v:v,rational:isSq(n),digits:v.toFixed(9)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'빗변의 길이',v:'√'+c.n},
            {k:'소수로',v:ran?c.digits:'옮겨 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '빗변은 √'+c.n+' = '+c.digits+'…  '+(c.rational?('딱 '+Math.round(c.v)+'이라 유리수다.'):'끝나지도 되풀이되지도 않는 무리수다.')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var U=42, X0=50, Y=300;
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(20,Y);ctx.lineTo(420,Y);ctx.stroke();
    for(i=0;i<=8;i++){
      var x=X0+i*U;
      if(x>418) break;
      ctx.beginPath();ctx.moveTo(x,Y-7);ctx.lineTo(x,Y+7);
      ctx.strokeStyle='#64748b';ctx.lineWidth=1.8;ctx.stroke();
      ctx.fillStyle='#94a3b8';ctx.font='12px sans-serif';ctx.textAlign='center';
      ctx.fillText(i,x,Y+24);
    }
    ctx.textAlign='left';
    var A=[X0,Y], B=[X0+S.a*U,Y], C=[X0+S.a*U,Y-S.b*U];
    ctx.beginPath();ctx.moveTo(A[0],A[1]);ctx.lineTo(B[0],B[1]);ctx.lineTo(C[0],C[1]);ctx.closePath();
    ctx.fillStyle='rgba(37,99,235,0.12)';ctx.fill();
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;ctx.stroke();
    ctx.strokeStyle='#dc2626';ctx.lineWidth=4;
    ctx.beginPath();ctx.moveTo(A[0],A[1]);ctx.lineTo(C[0],C[1]);ctx.stroke();
    lbl(ctx,'√'+c.n,(A[0]+C[0])/2-30,(A[1]+C[1])/2-8,'#b91c1c',16);
    var sw=(t===null)?0:Math.min(1,t);
    if(sw>0){
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=2;
      ctx.beginPath();ctx.arc(X0,Y,c.v*U,-Math.PI*0.5*sw,0);ctx.stroke();
      if(sw>=1){
        ctx.beginPath();ctx.arc(X0+c.v*U,Y,7,0,Math.PI*2);
        ctx.fillStyle='#dc2626';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
        lbl(ctx,'√'+c.n,X0+c.v*U,Y+44,'#b91c1c',15,'center');
      }
    }
    lbl(ctx,'밑변 '+S.a+', 높이 '+S.b+' 인 직각삼각형',24,34,'#1d4ed8',18);
    box(ctx,20,336,400,80);
    lbl(ctx,'빗변² = '+(S.a*S.a)+' + '+(S.b*S.b)+' = '+c.n,38,366,'#1f2937',19);
    lbl(ctx,(t===null)?'√'+c.n+'은 어떤 수일까?':('√'+c.n+' = '+c.digits+(c.rational?'':'…')+'   →   '+(c.rational?'유리수':'무리수')),
        38,398,c.rational?'#15803d':'#b91c1c',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,n:c.n,v:c.digits,rational:c.rational,
            sq:c.rational?Math.round(c.v):null};
  },
  headA:['번호','밑변','높이','빗변²','빗변','완전제곱수?','유리수?'],
  rowA:function(r,i){
    return [i+1,r.a,r.b,r.n,'√'+r.n+' = '+r.v,
            '<span class="'+(r.rational?'ok':'no')+'">'+(r.rational?'○':'×')+'</span>',
            '<span class="'+(r.rational?'ok':'no')+'">'+(r.rational?'○ ('+r.sq+')':'× (무리수)')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],rat=0,irr=0,match=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.rational) rat++; else irr++;
      match++;
      rows.push([r.a+', '+r.b, r.n, '√'+r.n+' = '+r.v,
                 '<span class="'+(r.rational?'ok':'no')+'">'+(r.rational?'○':'×')+'</span>',
                 r.rational?('유리수 '+r.sq):'무리수']);
    }
    var stats=[
      {t:'빗변²이 완전제곱수였던 기록',big:rat+'개',
       p:rat?'그때만 빗변이 유리수였다.':'밑변 3, 높이 4처럼 완전제곱이 되는 경우도 만들어 보자.'},
      {t:'무리수가 나온 기록',big:irr+'개',
       p:irr?'소수가 끝나지도, 되풀이되지도 않는다.':'밑변 1, 높이 1로 √2를 만들어 보자.'},
      {t:'수직선 위에 찍을 수 있었나',big:'모두 가능',
       p:'무리수도 컴퍼스로 정확한 한 점에 대응된다.'}
    ];
    var concl;
    if(rat===0||irr===0){
      concl='<b>더 해 보자</b> — 유리수가 되는 경우(3, 4)와 무리수가 되는 경우(1, 1)를 <b>모두</b> 기록해 보자.';
    } else {
      concl='<b>정리</b> — 빗변²이 완전제곱수일 때만 빗변이 유리수였고, 나머지는 <b>끝나지도 되풀이되지도 않는 무리수</b>였다. '
           +'그런데 무리수도 컴퍼스로 <b>수직선 위의 정확한 한 점</b>에 옮길 수 있었다. '
           +'√2는 “정확히 알 수 없는 수”가 아니라 분수로 쓸 수 없을 뿐 자기 자리가 분명히 있는 수다. '
           +'유리수와 무리수를 합쳐 수직선을 빈틈없이 채운 것이 실수다.';
    }
    return {head:['두 변','빗변²','빗변','완전제곱?','수의 종류'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 제곱근의 대소 비교
# ============================================================
LAB_CMP = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'제곱근 비교판',
  action:'근호 안으로 넣어 비교하기',
  hint0:'두 수 p√q 와 r√s 를 만들어 크기를 비교해 보자.',
  sliders:[
    {id:'p',label:'① 근호 밖 수 p',min:1,max:6,value:2,color:'#2563eb',unit:''},
    {id:'q',label:'① 근호 안 수 q',min:2,max:9,value:5,color:'#60a5fa',unit:''},
    {id:'r',label:'② 근호 밖 수 r',min:1,max:6,value:3,color:'#dc2626',unit:''},
    {id:'s',label:'② 근호 안 수 s',min:2,max:9,value:2,color:'#f87171',unit:''}
  ],
  calc:function(S){
    var A=S.p*Math.sqrt(S.q), B=S.r*Math.sqrt(S.s);
    var ia=S.p*S.p*S.q, ib=S.r*S.r*S.s;
    return {A:A,B:B,ia:ia,ib:ib,
            big:(A>B)?'①':((B>A)?'②':'같음'),
            outBig:(S.p>S.r)?'①':((S.r>S.p)?'②':'같음'),
            inBig:(S.q>S.s)?'①':((S.s>S.q)?'②':'같음')};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'① / ②',v:S.p+'√'+S.q+' / '+S.r+'√'+S.s},
            {k:'근호 안으로',v:ran?('√'+c.ia+' / √'+c.ib):'넣어 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '√'+c.ia+' 와 √'+c.ib+'를 비교하면 더 큰 쪽은 '+c.big+'이다. 근호 밖 수가 큰 쪽은 '+c.outBig+'이었다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var mx=Math.max(c.A,c.B), U=Math.min(28, 300/mx);
    var X0=60;
    var grow=(t===null)?0:Math.min(1,t);
    function bar(y,len,col,edge,label){
      ctx.fillStyle=col;ctx.fillRect(X0,y,len*U*grow,30);
      ctx.strokeStyle=edge;ctx.lineWidth=2.5;ctx.strokeRect(X0,y,len*U*grow,30);
      if(grow>=1) lbl(ctx,label,X0+len*U+8,y+22,edge,15);
    }
    lbl(ctx,'① '+S.p+'√'+S.q+'      ② '+S.r+'√'+S.s,24,38,'#1d4ed8',19);
    bar(80,c.A,'#bfdbfe','#2563eb',r3(c.A));
    bar(130,c.B,'#fecaca','#dc2626',r3(c.B));
    lbl(ctx,'①',30,102,'#1d4ed8',16);
    lbl(ctx,'②',30,152,'#b91c1c',16);
    if(grow>0){
      lbl(ctx,'① = √('+S.p+'² × '+S.q+') = √'+c.ia,40,208,'#1d4ed8',19);
      lbl(ctx,'② = √('+S.r+'² × '+S.s+') = √'+c.ib,40,240,'#b91c1c',19);
    }
    box(ctx,20,262,400,122);
    lbl(ctx,(t===null)?'어느 쪽이 클까?':('더 큰 쪽 : '+c.big+'   (√'+c.ia+' vs √'+c.ib+')'),38,294,'#1f2937',20);
    lbl(ctx,'근호 밖 수가 큰 쪽 : '+c.outBig,38,328,'#52627a',18);
    lbl(ctx,'근호 안 수가 큰 쪽 : '+c.inBig,38,358,'#52627a',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {p:S.p,q:S.q,r:S.r,s:S.s,A:r3(c.A),B:r3(c.B),ia:c.ia,ib:c.ib,
            big:c.big,outBig:c.outBig,inBig:c.inBig,
            outOk:(c.big===c.outBig),inOk:(c.big===c.inBig)};
  },
  headA:['번호','①','②','근호 안으로','실제 값','더 큰 쪽','근호 밖 큰 쪽','일치?','근호 안 큰 쪽','일치?'],
  rowA:function(r,i){
    return [i+1,r.p+'√'+r.q,r.r+'√'+r.s,'√'+r.ia+' / √'+r.ib,r.A+' / '+r.B,'<b>'+r.big+'</b>',r.outBig,
            '<span class="'+(r.outOk?'ok':'no')+'">'+(r.outOk?'○':'×')+'</span>',r.inBig,
            '<span class="'+(r.inOk?'ok':'no')+'">'+(r.inOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],outOk=0,inOk=0,cnt=0,outFail=0,inFail=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      cnt++;
      if(r.outOk) outOk++; else outFail++;
      if(r.inOk) inOk++; else inFail++;
      rows.push([r.p+'√'+r.q+' vs '+r.r+'√'+r.s, '√'+r.ia+' vs √'+r.ib, r.A+' / '+r.B,
                 '<b>'+r.big+'</b>', r.outBig,
                 '<span class="'+(r.outOk?'ok':'no')+'">'+(r.outOk?'○':'×')+'</span>',
                 r.inBig,
                 '<span class="'+(r.inOk?'ok':'no')+'">'+(r.inOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'“근호 밖 수가 크면 크다”가 맞은 횟수',big:outOk+' / '+cnt,
       p:outFail?('틀린 경우 '+outFail+'개.'):'아직 반례가 없다.'},
      {t:'“근호 안 수가 크면 크다”가 맞은 횟수',big:inOk+' / '+cnt,
       p:inFail?('틀린 경우 '+inFail+'개.'):'아직 반례가 없다.'},
      {t:'기록 수',big:cnt+'개',p:'2√5와 3√2처럼 밖과 안이 서로 엇갈리는 짝을 만들어 보자.'}
    ];
    var concl;
    if(outFail===0&&inFail===0){
      concl='<b>더 해 보자</b> — 아직 두 방법 모두 맞았다. 2√5(=√20)와 3√2(=√18)처럼 <b>근호 밖 수가 작은데 값은 큰</b> 짝을 만들어 보자.';
    } else {
      concl='<b>정리</b> — 근호 밖 수만 보고 판단하면 '+outFail+'번, 근호 안 수만 보고 판단하면 '+inFail+'번 틀렸다. '
           +'2√5는 √20, 3√2는 √18이므로 근호 밖 수가 작은 2√5가 더 크다. '
           +'제곱근의 크기는 <b>근호 안으로 모두 넣어 하나의 수로 만든 뒤</b> 비교해야 한다. '
           +'a > 0, b > 0일 때 a < b ⟺ √a < √b이기 때문이다.';
    }
    return {head:['비교','근호 안으로','실제 값','더 큰 쪽','밖이 큰 쪽','일치?','안이 큰 쪽','일치?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 분모의 유리화
# ============================================================
LAB_RAT = BASE + r"""
function gcd(x,y){x=Math.abs(x);y=Math.abs(y);while(y){var t=x%y;x=y;y=t;}return x;}
var LAB = {
  cw:440, ch:400, cvTitle:'유리화 실험판',
  action:'분모를 유리수로 만들기',
  hint0:'분자와 분모 속 수를 정하고, 유리화 전후의 값을 비교해 보자.',
  sliders:[
    {id:'a',label:'분자',min:1,max:9,value:3,color:'#2563eb',unit:''},
    {id:'b',label:'분모의 근호 안 수',min:2,max:20,value:5,color:'#16a34a',unit:''}
  ],
  calc:function(S){
    var orig=S.a/Math.sqrt(S.b);
    var rat=S.a*Math.sqrt(S.b)/S.b;
    var wrong=Math.sqrt(S.a/S.b);
    var g=gcd(S.a,S.b);
    return {orig:orig,rat:rat,wrong:wrong,g:g,
            num:S.a/g,den:S.b/g};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'원래 식',v:S.a+' / √'+S.b},
            {k:'유리화한 식',v:ran?(S.a+'√'+S.b+' / '+S.b):'해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '유리화 전 '+r6(c.orig)+', 유리화 후 '+r6(c.rat)+'.  값이 같다. √(a/b)는 '+r6(c.wrong)+'로 다르다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var p1=(t===null)?0:Math.min(1,t/0.5);
    var p2=(t===null)?0:Math.max(0,(t-0.5)/0.5);
    lbl(ctx,'분모에 근호가 있으면 값을 가늠하기 어렵다',24,38,'#52627a',16);
    lbl(ctx,S.a+' / √'+S.b,50,96,'#1f2937',28);
    if(p1>0){
      ctx.globalAlpha=p1;
      lbl(ctx,'분모와 분자에 √'+S.b+'를 곱하면',50,138,'#b45309',17);
      lbl(ctx,'= '+S.a+'√'+S.b+' / '+S.b,50,182,'#15803d',26);
      ctx.globalAlpha=1;
    }
    if(p2>0){
      ctx.globalAlpha=p2;
      lbl(ctx,'분모가 유리수 '+S.b+'가 되었다',50,218,'#15803d',17);
      ctx.globalAlpha=1;
    }
    box(ctx,20,240,400,144);
    lbl(ctx,(t===null)?'값은 달라질까?':('유리화 전 : '+r6(c.orig)),38,272,'#1f2937',19);
    lbl(ctx,(t===null)?'':('유리화 후 : '+r6(c.rat)),38,304,'#15803d',19);
    lbl(ctx,(t===null)?'':('두 값이 '+((Math.abs(c.orig-c.rat)<1e-12)?'같다':'다르다')),38,334,'#334155',18);
    lbl(ctx,(t===null)?'':('√('+S.a+'/'+S.b+') = '+r6(c.wrong)+' (다른 수다)'),38,368,'#b91c1c',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,orig:r6(c.orig),rat:r6(c.rat),wrong:r6(c.wrong),
            same:(Math.abs(c.orig-c.rat)<1e-12),
            wsame:(Math.abs(c.orig-c.wrong)<1e-12)};
  },
  headA:['번호','원래 식','유리화한 식','원래 값','유리화 후 값','같은가?','√(a/b)','같은가?'],
  rowA:function(r,i){
    return [i+1,r.a+'/√'+r.b,r.a+'√'+r.b+'/'+r.b,r.orig,'<b>'+r.rat+'</b>',
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            r.wrong,
            '<span class="'+(r.wsame?'ok':'no')+'">'+(r.wsame?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,wsame=0,one=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.wsame){ wsame++; if(r.a===1) one++; }
      rows.push([r.a+'/√'+r.b, r.a+'√'+r.b+'/'+r.b, r.orig, '<b>'+r.rat+'</b>',
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 r.wrong,
                 '<span class="'+(r.wsame?'ok':'no')+'">'+(r.wsame?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'유리화 전후의 값이 같았던 횟수',big:same+' / '+rec.length,
       p:'분모와 분자에 같은 수를 곱했으니 값은 변하지 않는다.'},
      {t:'√(a/b)와 같았던 횟수',big:wsame+' / '+rec.length,
       p:wsame?('그중 분자가 1이었던 것 '+one+'개.'):'a/√b 와 √(a/b)는 다른 수다.'},
      {t:'기록 수',big:rec.length+'개',p:'분자를 1로도, 1이 아닌 수로도 해 보자.'}
    ];
    var concl;
    if(same===rec.length&&wsame===one){
      concl='<b>정리</b> — 유리화를 해도 값은 <b>한 번도 달라지지 않았다.</b> 분모와 분자에 같은 수를 곱한 것뿐이라 '
           +'모양만 바뀌고 수 자체는 그대로다. 분모가 유리수가 되면 어림하거나 계산하기 훨씬 쉬워진다. '
           +'한편 a/√b 와 √(a/b)는 분자가 1일 때만 같고 <b>일반적으로는 다른 수</b>였다. 근호를 통째로 옮겨 쓰면 안 된다.';
    } else if(same===rec.length){
      concl='<b>정리</b> — 유리화는 값을 바꾸지 않았다. 분자를 1이 아닌 수로도 기록해 √(a/b)와 비교해 보자.';
    } else {
      concl='<b>확인 필요</b> — 유리화 전후 값이 다른 기록이 있다.';
    }
    return {head:['원래 식','유리화','원래 값','유리화 후','같은가?','√(a/b)','같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 근과 계수의 관계
# ============================================================
LAB_VIETA = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'근과 계수 판',
  action:'두 근 구하고 더해 보기',
  hint0:'이차방정식의 계수를 정하고 두 근을 구해 보자.',
  sliders:[
    {id:'a',label:'a',min:1,max:4,value:1,color:'#2563eb',unit:''},
    {id:'b',label:'b',min:-8,max:8,value:-5,color:'#16a34a',unit:''},
    {id:'c',label:'c',min:-8,max:8,value:6,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var D=S.b*S.b-4*S.a*S.c;
    if(D<0) return {none:true,D:D};
    var sq=Math.sqrt(D);
    var x1=(-S.b-sq)/(2*S.a), x2=(-S.b+sq)/(2*S.a);
    return {none:false,D:D,x1:x1,x2:x2,sum:x1+x2,prod:x1*x2,
            bs:-S.b/S.a,cp:S.c/S.a};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    if(c.none) return [{k:'실근',v:'없음 (b²−4ac < 0)'},{k:'',v:'계수를 바꾸자'}];
    return [{k:'두 근',v:ran?(r3(c.x1)+' , '+r3(c.x2)):'구해 보자'},
            {k:'두 근의 합 / 곱',v:ran?(r3(c.sum)+' / '+r3(c.prod)):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.none) return '실근이 없다. 계수를 바꿔 보자.';
    return '두 근의 합 '+r3(c.sum)+', 곱 '+r3(c.prod)+'.  −b/a = '+r3(c.bs)+', c/a = '+r3(c.cp)+'와 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var CX=220, CY=250, U=22;
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=-9;i<=9;i++){ ctx.beginPath();ctx.moveTo(CX+i*U,CY-9*U);ctx.lineTo(CX+i*U,CY+3*U);ctx.stroke(); }
    for(i=-3;i<=9;i++){ ctx.beginPath();ctx.moveTo(CX-9*U,CY-i*U);ctx.lineTo(CX+9*U,CY-i*U);ctx.stroke(); }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(CX-9*U,CY);ctx.lineTo(CX+9*U,CY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(CX,CY-9*U);ctx.lineTo(CX,CY+3*U);ctx.stroke();
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    var st=false;
    for(i=-90;i<=90;i++){
      var xx=i/10, yy=S.a*xx*xx+S.b*xx+S.c;
      if(yy<-3||yy>9){ st=false; continue; }
      if(!st){ ctx.moveTo(CX+xx*U,CY-yy*U); st=true; } else ctx.lineTo(CX+xx*U,CY-yy*U);
    }
    ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    if(!c.none&&grow>=1){
      [c.x1,c.x2].forEach(function(rr){
        if(Math.abs(rr)>9) return;
        ctx.beginPath();ctx.arc(CX+rr*U,CY,8,0,Math.PI*2);
        ctx.fillStyle='#dc2626';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
        lbl(ctx,r2(rr),CX+rr*U,CY+26,'#b91c1c',14,'center');
      });
    }
    lbl(ctx,S.a+'x²'+sg(S.b)+'x'+sg(S.c)+' = 0',24,32,'#1d4ed8',18);
    box(ctx,20,332,400,90);
    if(c.none){
      lbl(ctx,'b²−4ac = '+c.D+' < 0 이라 실근이 없다',38,372,'#b91c1c',20);
      return;
    }
    lbl(ctx,(t===null)?'두 근의 합과 곱은?':('합 '+r3(c.sum)+'      곱 '+r3(c.prod)),38,364,'#1f2937',19);
    lbl(ctx,(t===null)?'':('−b/a = '+r3(c.bs)+'      c/a = '+r3(c.cp)),38,398,'#15803d',19);
  },
  record:function(S){
    var c=this.calc(S);
    if(c.none) return {none:true,a:S.a,b:S.b,c:S.c,D:c.D};
    return {none:false,a:S.a,b:S.b,c:S.c,
            x1:r3(c.x1),x2:r3(c.x2),sum:r3(c.sum),prod:r3(c.prod),
            bs:r3(c.bs),cp:r3(c.cp),
            sOk:(Math.abs(c.sum-c.bs)<1e-9),pOk:(Math.abs(c.prod-c.cp)<1e-9)};
  },
  headA:['번호','식','두 근','합','−b/a','같나?','곱','c/a','같나?'],
  rowA:function(r,i){
    if(r.none) return [i+1,r.a+'x²'+sg(r.b)+'x'+sg(r.c),'실근 없음','-','-','-','-','-','-'];
    return [i+1,r.a+'x²'+sg(r.b)+'x'+sg(r.c),r.x1+' , '+r.x2,'<b>'+r.sum+'</b>',r.bs,
            '<span class="'+(r.sOk?'ok':'no')+'">'+(r.sOk?'○':'×')+'</span>',
            '<b>'+r.prod+'</b>',r.cp,
            '<span class="'+(r.pOk?'ok':'no')+'">'+(r.pOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],valid=0,sOk=0,pOk=0,none=0,as={},an=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.none){ none++; rows.push([r.a+'x²'+sg(r.b)+'x'+sg(r.c),'실근 없음','-','-','-','-']); continue; }
      valid++;
      if(r.sOk) sOk++;
      if(r.pOk) pOk++;
      if(!as[r.a]){ as[r.a]=true; an++; }
      rows.push([r.a+'x²'+sg(r.b)+'x'+sg(r.c), r.x1+' , '+r.x2, r.sum+' / '+r.bs,
                 '<span class="'+(r.sOk?'ok':'no')+'">'+(r.sOk?'○':'×')+'</span>',
                 r.prod+' / '+r.cp,
                 '<span class="'+(r.pOk?'ok':'no')+'">'+(r.pOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'두 근의 합 = −b/a',big:sOk+' / '+valid,p:'근을 실제로 구해 더한 값과 계수로 구한 값을 비교했다.'},
      {t:'두 근의 곱 = c/a',big:pOk+' / '+valid,p:'곱도 계수만으로 알 수 있는지 확인한 결과.'},
      {t:'시험한 a의 값 / 실근 없는 기록',big:an+'가지 / '+none+'개',
       p:'a가 1이 아닌 경우도 확인해야 −b/a, c/a의 의미가 드러난다.'}
    ];
    var concl;
    if(valid===0){
      concl='<b>더 해 보자</b> — 실근이 있는 계수로 기록해 보자. b²−4ac ≥ 0이어야 한다.';
    } else if(sOk===valid&&pOk===valid){
      concl='<b>정리</b> — 근을 일일이 구해 더하고 곱한 값이, 계수만으로 구한 <b>−b/a와 c/a</b>와 언제나 같았다. '
           +'a가 1이 아닐 때도 성립했다. 그래서 근을 구하지 않고도 두 근의 합과 곱을 알 수 있고, '
           +'반대로 합과 곱을 알면 그 두 수를 근으로 하는 이차방정식을 바로 만들 수 있다.';
    } else {
      concl='<b>확인 필요</b> — 근의 합·곱과 계수 관계가 어긋난 기록이 있다.';
    }
    return {head:['식','두 근','합 / −b/a','같나?','곱 / c/a','같나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 이차함수의 최댓값·최솟값
# ============================================================
LAB_MINMAX = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'최댓값·최솟값 판',
  action:'그래프에서 가장 높은/낮은 점 찾기',
  hint0:'y = ax² + bx + c 의 계수를 정해 보자.',
  sliders:[
    {id:'a',label:'a',min:-3,max:3,value:1,color:'#2563eb',unit:''},
    {id:'b',label:'b',min:-8,max:8,value:-4,color:'#16a34a',unit:''},
    {id:'c',label:'c',min:-8,max:8,value:1,color:'#f59e0b',unit:''}
  ],
  f:function(S,x){ return S.a*x*x+S.b*x+S.c; },
  scan:function(S){
    var best=null,bx=0,i;
    for(i=-1200;i<=1200;i++){
      var x=i/100, y=this.f(S,x);
      if(best===null||((S.a>0)?(y<best):(y>best))){ best=y; bx=x; }
    }
    return {vx:Math.round(bx*100)/100,vy:Math.round(best*100)/100};
  },
  readout:function(S,ran){
    if(S.a===0) return [{k:'a = 0',v:'이차함수가 아니다'},{k:'',v:'a를 바꾸자'}];
    var v=this.scan(S);
    return [{k:(S.a>0)?'최솟값':'최댓값',v:ran?v.vy:'찾아보자'},
            {k:'그때의 x',v:ran?v.vx:'-'}];
  },
  doneMsg:function(S){
    if(S.a===0) return 'a가 0이면 이차함수가 아니다.';
    var v=this.scan(S);
    return (S.a>0?'최솟값':'최댓값')+'은 '+v.vy+' (x = '+v.vx+').  −b/2a = '+r2(-S.b/(2*S.a))+', c = '+S.c+'와 비교해 보자.';
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
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    var st=false;
    for(i=-90;i<=90;i++){
      var xx=i/10, yy=this.f(S,xx);
      if(yy<-3||yy>9){ st=false; continue; }
      if(!st){ ctx.moveTo(CX+xx*U,CY-yy*U); st=true; } else ctx.lineTo(CX+xx*U,CY-yy*U);
    }
    ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    var v=this.scan(S);
    if(Math.abs(S.c)<=9){
      ctx.beginPath();ctx.arc(CX,CY-S.c*U,6,0,Math.PI*2);
      ctx.fillStyle='#f59e0b';ctx.fill();
      lbl(ctx,'y절편 c = '+S.c,CX+10,CY-S.c*U-8,'#b45309',14);
    }
    if(grow>=1&&Math.abs(v.vx)<=9&&v.vy>=-3&&v.vy<=9){
      ctx.beginPath();ctx.arc(CX+v.vx*U,CY-v.vy*U,8,0,Math.PI*2);
      ctx.fillStyle='#dc2626';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      lbl(ctx,'('+v.vx+', '+v.vy+')',CX+v.vx*U+12,CY-v.vy*U+18,'#b91c1c',14);
    }
    lbl(ctx,'y = '+S.a+'x²'+sg(S.b)+'x'+sg(S.c),24,32,'#1d4ed8',18);
    box(ctx,20,338,400,84);
    lbl(ctx,(t===null)?'가장 낮은(높은) 점은 어디일까?':((S.a>0?'최솟값 ':'최댓값 ')+v.vy+'  (x = '+v.vx+')'),38,370,'#1f2937',19);
    lbl(ctx,(t===null)?'':('−b/2a = '+r2(-S.b/(2*S.a))+'      c = '+S.c),38,402,'#52627a',18);
  },
  record:function(S){
    if(S.a===0) return {zero:true};
    var v=this.scan(S);
    var xv=-S.b/(2*S.a);
    return {zero:false,a:S.a,b:S.b,c:S.c,vx:v.vx,vy:v.vy,
            xv:r2(xv),up:(S.a>0),
            xOk:(Math.abs(v.vx-xv)<0.02),
            cOk:(Math.abs(v.vy-S.c)<0.02),
            b0:(S.b===0)};
  },
  headA:['번호','식','최댓값/최솟값','그때의 x','−b/2a','같나?','c','최적값 = c?'],
  rowA:function(r,i){
    if(r.zero) return [i+1,'a=0','-','-','-','-','-','-'];
    return [i+1,r.a+'x²'+sg(r.b)+'x'+sg(r.c),(r.up?'최솟값 ':'최댓값 ')+'<b>'+r.vy+'</b>',r.vx,r.xv,
            '<span class="'+(r.xOk?'ok':'no')+'">'+(r.xOk?'○':'×')+'</span>',
            r.c,
            '<span class="'+(r.cOk?'ok':'no')+'">'+(r.cOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],valid=0,xOk=0,cOk=0,b0=0,up=0,down=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.zero){ rows.push(['a=0','-','-','-','-','-']); continue; }
      valid++;
      if(r.xOk) xOk++;
      if(r.cOk){ cOk++; if(r.b0) b0++; }
      if(r.up) up++; else down++;
      rows.push([r.a+'x²'+sg(r.b)+'x'+sg(r.c), (r.up?'최솟값':'최댓값'), r.vy, r.vx+' / '+r.xv,
                 '<span class="'+(r.xOk?'ok':'no')+'">'+(r.xOk?'○':'×')+'</span>',
                 r.c,
                 '<span class="'+(r.cOk?'ok':'no')+'">'+(r.cOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'최적값이 나오는 x = −b/2a',big:xOk+' / '+valid,
       p:'그래프에서 직접 찾은 x와 계수로 구한 값을 비교했다.'},
      {t:'“최솟값(최댓값) = c”가 맞은 횟수',big:cOk+' / '+valid,
       p:cOk?('그중 b가 0이었던 것 '+b0+'개. b=0일 때만 우연히 맞는다.'):'c는 y절편일 뿐이다.'},
      {t:'아래로 볼록 / 위로 볼록',big:up+'개 / '+down+'개',
       p:'a>0이면 최솟값, a<0이면 최댓값을 가진다.'}
    ];
    var concl;
    if(valid===0){
      concl='<b>더 해 보자</b> — a를 0이 아닌 값으로 두어야 한다.';
    } else if(xOk===valid&&cOk===b0){
      concl='<b>정리</b> — 최댓값·최솟값이 나오는 x는 언제나 <b>−b/2a</b>였고, 그 값은 c가 아니라 '
           +'그 x를 식에 넣은 결과였다. c는 x=0일 때의 값, 즉 <b>y절편</b>일 뿐이다(b=0일 때만 둘이 겹친다). '
           +'a>0이면 아래로 볼록해 최솟값을, a<0이면 위로 볼록해 최댓값을 가진다.';
    } else {
      concl='<b>정리</b> — 최적값의 위치는 −b/2a였다. b가 0인 경우와 아닌 경우를 모두 기록해 c와의 관계를 확인해 보자.';
    }
    return {head:['식','종류','값','x / −b/2a','같나?','c','= c?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("m3_irrational_construction_lab.html",
     "무리수 실험실 — √2는 수직선 위에 있을까?",
     "무리수 실험실 — √2는 수직선 위에 있을까?",
     "직각삼각형의 빗변을 컴퍼스로 수직선에 옮기고, 그 길이가 유리수인지 무리수인지 확인한다.",
     LAB_IRR),
    ("m3_sqrt_compare_lab.html",
     "제곱근 비교 실험실 — 앞의 수가 크면 큰 수일까?",
     "제곱근 비교 실험실 — 앞의 수가 크면 큰 수일까?",
     "p√q 꼴 두 수를 근호 안으로 넣어 비교하고, 근호 밖·안 수만 보고 판단할 때의 반례를 찾는다.",
     LAB_CMP),
    ("m3_rationalize_lab.html",
     "유리화 실험실 — 분모를 바꾸면 값도 바뀔까?",
     "유리화 실험실 — 분모를 바꾸면 값도 바뀔까?",
     "분모의 근호를 없앤 뒤 값이 그대로인지 확인하고, √(a/b)와도 비교한다.",
     LAB_RAT),
    ("m3_root_coefficient_lab.html",
     "근과 계수 실험실 — 근을 구하지 않고 합을 알 수 있을까?",
     "근과 계수 실험실 — 근을 구하지 않고 합을 알 수 있을까?",
     "이차방정식의 두 근을 실제로 구해 합과 곱을 계산하고, −b/a·c/a와 대조한다.",
     LAB_VIETA),
    ("m3_quadratic_extremum_lab.html",
     "최댓값 실험실 — c가 최솟값일까?",
     "최댓값 실험실 — c가 최솟값일까?",
     "y = ax²+bx+c의 그래프에서 가장 낮은(높은) 점을 직접 찾아 −b/2a, c와 비교한다.",
     LAB_MINMAX),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c19_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
