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
function r4(v){return Math.round(v*10000)/10000;}
function r6(v){return Math.round(v*1000000)/1000000;}
function sg(v){return (v<0)?(' − '+(-v)):(' + '+v);}
function sgc(v,s){ if(v===0) return ''; return (v<0)?(' − '+(-v)+s):(' + '+v+s); }
function isSq(n){ var s=Math.round(Math.sqrt(n)); return s*s===n; }
"""

# ============================================================
# 1. 제곱근의 덧셈
# ============================================================
LAB_SQADD = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'제곱근 길이 더하기',
  action:'이어 붙여 재기',
  hint0:'두 항 p√q 와 r√s 를 정하고, 더한 길이를 재 보자.',
  sliders:[
    {id:'p',label:'① 계수 p',min:1,max:6,value:2,color:'#2563eb',unit:''},
    {id:'q',label:'① 근호 안 q',min:2,max:9,value:3,color:'#60a5fa',unit:''},
    {id:'r',label:'② 계수 r',min:1,max:6,value:3,color:'#dc2626',unit:''},
    {id:'s',label:'② 근호 안 s',min:2,max:9,value:3,color:'#f87171',unit:''}
  ],
  calc:function(S){
    var A=S.p*Math.sqrt(S.q), B=S.r*Math.sqrt(S.s);
    var sum=A+B;
    var merge=(S.q===S.s)?((S.p+S.r)*Math.sqrt(S.q)):null;
    var wrong=Math.sqrt(S.q+S.s)*(S.p+S.r);
    var wrong2=Math.sqrt(S.p*S.p*S.q+S.r*S.r*S.s);
    return {A:A,B:B,sum:sum,merge:merge,wrong:wrong,wrong2:wrong2,
            same:(S.q===S.s)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'근호 안',v:(S.q===S.s)?'같다':'다르다'},
            {k:'합의 길이',v:ran?r4(c.sum):'재 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.same) return '근호 안이 같아 계수끼리 더하면 '+(S.p+S.r)+'√'+S.q+' = '+r4(c.merge)+'이고 실제 길이와 같다. 기록해 보자.';
    return '근호 안이 달라 하나로 합칠 수 없다. 실제 길이는 '+r4(c.sum)+'이다. 근호 안을 더한 값과 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var mx=Math.max(c.sum,c.wrong,1);
    var U=Math.min(30, 320/mx);
    var X0=50;
    var grow=(t===null)?0:Math.min(1,t);
    lbl(ctx,S.p+'√'+S.q+'  +  '+S.r+'√'+S.s,24,38,'#1d4ed8',20);
    ctx.fillStyle='#bfdbfe';ctx.fillRect(X0,72,c.A*U,28);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=2;ctx.strokeRect(X0,72,c.A*U,28);
    ctx.fillStyle='#fecaca';ctx.fillRect(X0+c.A*U,72,c.B*U*grow,28);
    ctx.strokeStyle='#dc2626';ctx.strokeRect(X0+c.A*U,72,c.B*U*grow,28);
    if(grow>=1) lbl(ctx,'합 '+r3(c.sum),X0+(c.A+c.B)*U+8,92,'#334155',15);
    if(grow>=1&&c.same){
      ctx.fillStyle='#bbf7d0';ctx.fillRect(X0,116,c.merge*U,28);
      ctx.strokeStyle='#16a34a';ctx.lineWidth=2;ctx.strokeRect(X0,116,c.merge*U,28);
      lbl(ctx,(S.p+S.r)+'√'+S.q+' = '+r3(c.merge),X0+c.merge*U+8,136,'#15803d',15);
    }
    if(grow>=1){
      ctx.fillStyle='#fde68a';ctx.fillRect(X0,160,c.wrong*U,28);
      ctx.strokeStyle='#d97706';ctx.lineWidth=2;ctx.strokeRect(X0,160,c.wrong*U,28);
      lbl(ctx,'('+(S.p+S.r)+')√'+(S.q+S.s)+' = '+r3(c.wrong),X0+c.wrong*U+8,180,'#b45309',14);
    }
    box(ctx,20,206,400,178);
    lbl(ctx,'① = '+r4(c.A)+'      ② = '+r4(c.B),38,240,'#52627a',17);
    lbl(ctx,(t===null)?'하나로 합칠 수 있을까?':('실제 합 = '+r4(c.sum)),38,276,'#1f2937',19);
    lbl(ctx,(t===null)?'':(c.same?('계수끼리 더하면 '+(S.p+S.r)+'√'+S.q+' = '+r4(c.merge)):'근호 안이 달라 계수끼리 더할 수 없다'),
        38,312,c.same?'#15803d':'#b91c1c',17);
    lbl(ctx,(t===null)?'':('근호 안을 더하면 √'+(S.q+S.s)+' 을 써서 '+r4(c.wrong)),38,348,'#b45309',16);
    lbl(ctx,(t===null)?'':'세 값을 견주어 보자',38,374,'#94a3b8',14);
  },
  record:function(S){
    var c=this.calc(S);
    return {p:S.p,q:S.q,r:S.r,s:S.s,
            A:r4(c.A),B:r4(c.B),sum:r4(c.sum),
            merge:(c.merge===null)?'-':r4(c.merge),
            wrong:r4(c.wrong),
            same:c.same,
            mergeOk:(c.merge!==null&&Math.abs(c.sum-c.merge)<1e-9),
            wrongOk:(Math.abs(c.sum-c.wrong)<1e-9)};
  },
  headA:['번호','①','②','근호 안 같음','실제 합','계수끼리 더함','맞나?','근호 안을 더함','맞나?'],
  rowA:function(r,i){
    return [i+1,r.p+'√'+r.q,r.r+'√'+r.s,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            '<b>'+r.sum+'</b>',r.merge,
            '<span class="'+(r.mergeOk?'ok':'no')+'">'+(r.mergeOk?'○':'×')+'</span>',
            r.wrong,
            '<span class="'+(r.wrongOk?'ok':'no')+'">'+(r.wrongOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,sameOk=0,diff=0,wrongOk=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same){ same++; if(r.mergeOk) sameOk++; }
      else diff++;
      if(r.wrongOk) wrongOk++;
      rows.push([r.p+'√'+r.q+' + '+r.r+'√'+r.s,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 '<b>'+r.sum+'</b>', r.merge,
                 '<span class="'+(r.mergeOk?'ok':'no')+'">'+(r.mergeOk?'○':'×')+'</span>',
                 r.wrong,
                 '<span class="'+(r.wrongOk?'ok':'no')+'">'+(r.wrongOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'근호 안이 같았던 기록',big:same+'개',
       p:same?('그중 계수끼리 더한 값이 맞은 것 '+sameOk+'개.'):'근호 안을 같게 맞춰 보자.'},
      {t:'근호 안이 달랐던 기록',big:diff+'개',
       p:diff?'하나로 합칠 수 없었다.':'근호 안을 다르게도 해 보자.'},
      {t:'근호 안을 더한 값이 맞은 횟수',big:wrongOk+' / '+rec.length,
       p:'√q + √s 를 √(q+s) 로 쓰면 맞지 않는다.'}
    ];
    var concl;
    if(same===0||diff===0){
      concl='<b>더 해 보자</b> — 근호 안이 <b>같은 경우와 다른 경우</b>를 모두 기록해 보자.';
    } else if(sameOk===same&&wrongOk===0){
      concl='<b>정리</b> — 근호 안이 <b>같을 때만</b> 계수끼리 더할 수 있었다(2√3 + 3√3 = 5√3). '
           +'문자식에서 동류항끼리만 더하는 것과 같은 원리다. √3 을 하나의 «덩어리»로 보면 된다. '
           +'근호 안이 다르면 하나로 합쳐지지 않고, <b>근호 안끼리 더하는 것은 한 번도 맞지 않았다.</b> '
           +'√2 + √3 은 √5 가 아니다.';
    } else {
      concl='<b>확인 필요</b> — 계산이 어긋난 기록이 있다.';
    }
    return {head:['식','근호 안 같음','실제 합','계수끼리','맞나?','근호 안끼리','맞나?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 실수의 조밀성
# ============================================================
LAB_DENSE = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'수직선 확대판',
  action:'사이를 뒤져 보기',
  hint0:'두 유리수 사이를 얼마나 좁힐지 정해 보자.',
  sliders:[
    {id:'c',label:'중심 (÷100)',min:100,max:300,value:141,color:'#2563eb',
     fmt:function(v){return (v/100).toFixed(2);}},
    {id:'e',label:'구간 폭 (10^−?)',min:1,max:5,value:2,color:'#dc2626',
     fmt:function(v){return '±'+Math.pow(10,-v).toFixed(v);}}
  ],
  calc:function(S){
    var c=S.c/100, w=Math.pow(10,-S.e);
    var lo=c-w, hi=c+w;
    var k=Math.pow(10,S.e+3);
    var n1=Math.ceil(lo*lo*k*k), n2=Math.floor(hi*hi*k*k);
    var irr=0, first=null, i;
    for(i=n1;i<=n2&&i-n1<400000;i++){
      if(!isSq(i)){ irr++; if(first===null) first=i; }
    }
    var rats=Math.floor(hi*1000000)-Math.ceil(lo*1000000)+1;
    return {c:c,w:w,lo:lo,hi:hi,k:k,irr:irr,first:first,
            mid:(lo+hi)/2,rats:Math.max(0,rats),
            fv:(first===null)?null:(Math.sqrt(first)/k)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'구간',v:r6(c.lo)+' ~ '+r6(c.hi)},
            {k:'찾은 무리수',v:ran?(c.irr+'개 이상'):'뒤져 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.first===null) return '이 구간에서는 못 찾았다. 구간을 조금 넓혀 보자.';
    return '구간 안에서 무리수를 '+c.irr+'개 이상 찾았다. 예: √'+c.first+' / '+c.k+' = '+r6(c.fv)+'. 더 좁혀 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var X0=44, X1=396;
    function px(v){ return X0+(X1-X0)*(v-c.lo)/(c.hi-c.lo); }
    var Y=170;
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(X0,Y);ctx.lineTo(X1,Y);ctx.stroke();
    [[c.lo,'#2563eb'],[c.hi,'#2563eb']].forEach(function(q){
      ctx.beginPath();ctx.moveTo(px(q[0]),Y-14);ctx.lineTo(px(q[0]),Y+14);
      ctx.strokeStyle=q[1];ctx.lineWidth=3;ctx.stroke();
    });
    lbl(ctx,r6(c.lo),X0,Y+34,'#1d4ed8',13);
    lbl(ctx,r6(c.hi),X1,Y+34,'#1d4ed8',13,'right');
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      var show=Math.min(60,Math.floor(c.irr*grow));
      var cnt=0;
      for(i=c.first;i<=c.first+400000&&cnt<show;i++){
        if(isSq(i)) continue;
        var v=Math.sqrt(i)/c.k;
        if(v<c.lo||v>c.hi) continue;
        ctx.beginPath();ctx.arc(px(v),Y-24,3.5,0,Math.PI*2);
        ctx.fillStyle='#dc2626';ctx.fill();
        cnt++;
      }
      ctx.beginPath();ctx.arc(px(c.mid),Y+24,5,0,Math.PI*2);
      ctx.fillStyle='#16a34a';ctx.fill();
      if(grow>=1) lbl(ctx,'유리수 '+r6(c.mid),px(c.mid),Y+50,'#15803d',13,'center');
    }
    lbl(ctx,'두 수 사이를 확대해서 들여다보기',24,32,'#1d4ed8',18);
    lbl(ctx,'빨강 = 찾은 무리수,  초록 = 가운데 유리수',24,56,'#52627a',14);
    box(ctx,20,236,400,148);
    lbl(ctx,'구간 폭 '+r6(2*c.w),38,268,'#52627a',17);
    lbl(ctx,(t===null)?'이 좁은 구간에도 무리수가 있을까?':('찾은 무리수 '+c.irr+'개 이상'),38,304,'#b91c1c',19);
    lbl(ctx,(t===null)?'':((c.first===null)?'못 찾음':('예 : √'+c.first+' / '+c.k+' = '+r6(c.fv))),38,340,'#334155',16);
    lbl(ctx,(t===null)?'':('가운데 유리수 '+r6(c.mid)),38,372,'#15803d',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {c:c.c,w:r6(2*c.w),lo:r6(c.lo),hi:r6(c.hi),
            irr:c.irr,found:(c.irr>0),
            ex:(c.first===null)?'-':('√'+c.first+'/'+c.k),
            mid:r6(c.mid)};
  },
  headA:['번호','구간','구간 폭','찾은 무리수','있었나?','예','가운데 유리수'],
  rowA:function(r,i){
    return [i+1,r.lo+' ~ '+r.hi,r.w,'<b>'+r.irr+'개</b>',
            '<span class="'+(r.found?'ok':'no')+'">'+(r.found?'○':'×')+'</span>',
            r.ex,r.mid];
  },
  analyze:function(rec){
    var rows=[],found=0,mnw=1e9,mnwv='';
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.found) found++;
      var w=parseFloat(r.w);
      if(w<mnw){ mnw=w; mnwv=r.w; }
      rows.push([r.lo+' ~ '+r.hi, r.w, '<b>'+r.irr+'개</b>',
                 '<span class="'+(r.found?'ok':'no')+'">'+(r.found?'○':'×')+'</span>',
                 r.ex, r.mid]);
    }
    var stats=[
      {t:'무리수를 찾은 횟수',big:found+' / '+rec.length,
       p:'구간을 좁혀도 무리수가 남아 있었는지 확인한 결과.'},
      {t:'가장 좁게 잡은 구간',big:mnwv,p:'그렇게 좁혀도 무리수가 있었다.'},
      {t:'유리수도 언제나',big:'있었다',p:'두 수의 가운데는 언제나 유리수다.'}
    ];
    var concl;
    if(rec.length<3){
      concl='<b>더 해 보자</b> — 구간 폭을 ±0.1, ±0.001, ±0.00001 로 줄여 가며 기록해 보자.';
    } else if(found===rec.length){
      concl='<b>정리</b> — 구간을 아무리 좁혀도 그 안에는 <b>유리수도 무리수도 언제나 있었다.</b> '
           +'두 수 사이의 가운데는 늘 유리수이고, 완전제곱수가 아닌 n으로 만든 √n / 10ᵏ 은 무리수다. '
           +'즉 실수는 수직선을 <b>빈틈없이</b> 채우고 있고, «다음 수»라는 것이 존재하지 않는다. '
           +'정수와 가장 크게 다른 점이다.';
    } else {
      concl='<b>정리</b> — 좁은 구간에서도 무리수를 찾을 수 있었다. 구간을 더 좁혀 확인해 보자.';
    }
    return {head:['구간','폭','무리수','있었나?','예','가운데 유리수'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 완전제곱식
# ============================================================
LAB_CSQ = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'완전제곱 넓이판',
  action:'모자란 칸 채우기',
  hint0:'x² + bx 에 무엇을 더해야 정사각형이 될까? b와 검산할 x를 정해 보자.',
  sliders:[
    {id:'b',label:'b',min:2,max:12,value:6,color:'#2563eb',unit:''},
    {id:'x',label:'검산할 x',min:-6,max:8,value:3,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var h=S.b/2, need=h*h;
    var orig=S.x*S.x+S.b*S.x+need;
    var sq=(S.x+h)*(S.x+h);
    return {h:h,need:need,orig:orig,sq:sq,
            wrongH:h,wrongB:S.b*S.b};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'더해야 할 수',v:ran?c.need:'채워 보자'},
            {k:'완전제곱식',v:ran?('(x + '+c.h+')²'):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '(b/2)² = '+c.need+'을 더하면 (x + '+c.h+')² 이 된다. x = '+S.x+'에서 양쪽 모두 '+c.orig+'이다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var U=Math.min(24, 200/(4+c.h));
    var A=4*U, H=c.h*U;
    var X=70, Y=80;
    var grow=(t===null)?0:Math.min(1,t);
    ctx.fillStyle='rgba(37,99,235,0.28)';ctx.fillRect(X,Y,A,A);
    ctx.strokeStyle='#334155';ctx.lineWidth=2;ctx.strokeRect(X,Y,A,A);
    ctx.fillStyle='#1d4ed8';ctx.font='bold 15px sans-serif';ctx.textAlign='center';
    ctx.fillText('x²',X+A/2,Y+A/2+5);
    ctx.fillStyle='rgba(148,163,184,0.35)';
    ctx.fillRect(X+A,Y,H,A);
    ctx.fillRect(X,Y+A,A,H);
    ctx.strokeStyle='#64748b';ctx.lineWidth=1.6;
    ctx.strokeRect(X+A,Y,H,A);ctx.strokeRect(X,Y+A,A,H);
    ctx.fillStyle='#475569';ctx.font='13px sans-serif';
    ctx.fillText((c.h)+'x',X+A+H/2,Y+A/2+4);
    ctx.fillText((c.h)+'x',X+A/2,Y+A+H/2+4);
    if(grow>0){
      ctx.globalAlpha=grow;
      ctx.fillStyle='rgba(245,158,11,0.45)';ctx.fillRect(X+A,Y+A,H,H);
      ctx.strokeStyle='#d97706';ctx.lineWidth=2;ctx.strokeRect(X+A,Y+A,H,H);
      ctx.fillStyle='#b45309';ctx.font='bold 13px sans-serif';
      ctx.fillText(c.need,X+A+H/2,Y+A+H/2+4);
      ctx.globalAlpha=1;
    }
    ctx.textAlign='left';
    if(grow>=1){
      ctx.strokeStyle='#16a34a';ctx.lineWidth=3;
      ctx.strokeRect(X,Y,A+H,A+H);
      lbl(ctx,'한 변 x + '+c.h,X,Y-12,'#15803d',15);
    }
    lbl(ctx,'x² + '+S.b+'x  +  ?',24,42,'#1d4ed8',19);
    box(ctx,20,320,400,98);
    lbl(ctx,(t===null)?'무엇을 더해야 정사각형이 될까?':('더할 수 = (b/2)² = '+c.h+'² = '+c.need),38,352,'#1f2937',19);
    lbl(ctx,(t===null)?'':('x = '+S.x+' 검산 :  원래 식 '+c.orig+'  /  (x+'+c.h+')² = '+c.sq),38,386,'#15803d',16);
    lbl(ctx,(t===null)?'':('b/2 = '+c.h+' 나 b² = '+c.wrongB+' 을 더하면 어떻게 될까?'),38,412,'#b91c1c',14);
  },
  record:function(S){
    var c=this.calc(S);
    return {b:S.b,x:S.x,h:c.h,need:c.need,orig:c.orig,sq:c.sq,
            ok:(c.orig===c.sq),
            hOk:(c.h===c.need),bOk:(S.b*S.b===c.need)};
  },
  headA:['번호','b','더할 수 (b/2)²','완전제곱식','검산 x','원래 식','제곱식','같나?','b/2를 더하면?','b²을 더하면?'],
  rowA:function(r,i){
    return [i+1,r.b,'<b>'+r.need+'</b>','(x + '+r.h+')²',r.x,r.orig,r.sq,
            '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
            '<span class="'+(r.hOk?'ok':'no')+'">'+(r.hOk?'○':'×')+'</span>',
            '<span class="'+(r.bOk?'ok':'no')+'">'+(r.bOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ok=0,h=0,b=0,bs={},bn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.ok) ok++;
      if(r.hOk) h++;
      if(r.bOk) b++;
      if(!bs[r.b]){ bs[r.b]=true; bn++; }
      rows.push([r.b, '<b>'+r.need+'</b>', '(x + '+r.h+')²', r.x, r.orig+' / '+r.sq,
                 '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
                 '<span class="'+(r.hOk?'ok':'no')+'">'+(r.hOk?'○':'×')+'</span>',
                 '<span class="'+(r.bOk?'ok':'no')+'">'+(r.bOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'검산이 맞은 횟수',big:ok+' / '+rec.length,
       p:'(b/2)² 을 더한 식과 (x + b/2)² 의 값을 비교한 결과.'},
      {t:'b/2 를 더하면 맞았던 횟수',big:h+' / '+rec.length,
       p:'b = 4 일 때만 우연히 같아진다.'},
      {t:'b² 을 더하면 맞았던 횟수',big:b+' / '+rec.length,
       p:'시험한 b '+bn+'가지.'}
    ];
    var concl;
    if(ok===rec.length){
      concl='<b>정리</b> — x² + bx 를 정사각형으로 만들려면 <b>(b/2)²</b> 을 더해야 했다. 어떤 x를 넣어 검산해도 맞았다. '
           +'그림에서 보면 x² 옆에 붙은 두 직사각형이 각각 (b/2)x 이고, 모퉁이의 빈 칸이 정확히 (b/2)² 이다. '
           +'b/2 나 b² 을 더하는 것은 대부분 맞지 않았다. 이 «모퉁이 채우기»가 근의 공식을 만드는 첫 단계다.';
    } else {
      concl='<b>확인 필요</b> — 검산이 어긋난 기록이 있다.';
    }
    return {head:['b','(b/2)²','완전제곱식','x','원래 식 / 제곱식','같나?','b/2?','b²?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 근의 공식
# ============================================================
LAB_QF = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'근의 공식 검산판',
  action:'공식으로 풀고 대입하기',
  hint0:'이차방정식의 계수를 정해 보자.',
  sliders:[
    {id:'a',label:'a',min:1,max:4,value:2,color:'#2563eb',unit:''},
    {id:'b',label:'b',min:-9,max:9,value:-5,color:'#16a34a',unit:''},
    {id:'c',label:'c',min:-9,max:9,value:1,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var D=S.b*S.b-4*S.a*S.c;
    if(D<0) return {none:true,D:D};
    var s=Math.sqrt(D);
    var x1=(-S.b-s)/(2*S.a), x2=(-S.b+s)/(2*S.a);
    function f(x){ return S.a*x*x+S.b*x+S.c; }
    var nice=(Math.abs(x1-Math.round(x1*100)/100)<1e-12&&Math.abs(s-Math.round(s))<1e-9);
    return {none:false,D:D,s:s,x1:x1,x2:x2,f1:f(x1),f2:f(x2),
            intRoot:(Math.abs(x1-Math.round(x1))<1e-9&&Math.abs(x2-Math.round(x2))<1e-9),
            sqInt:(Math.abs(s-Math.round(s))<1e-9)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    if(c.none) return [{k:'b² − 4ac',v:c.D+' < 0'},{k:'',v:'실근이 없다'}];
    return [{k:'두 근',v:ran?(r4(c.x1)+' , '+r4(c.x2)):'풀어 보자'},
            {k:'대입한 값',v:ran?(r6(c.f1)+' , '+r6(c.f2)):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.none) return 'b²−4ac가 음수라 실근이 없다. 계수를 바꿔 보자.';
    return '두 근 '+r4(c.x1)+', '+r4(c.x2)+'.  식에 넣으면 '+r6(c.f1)+', '+r6(c.f2)+'이다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var p1=(t===null)?0:Math.min(1,t/0.4);
    var p2=(t===null)?0:Math.max(0,Math.min(1,(t-0.4)/0.3));
    var p3=(t===null)?0:Math.max(0,(t-0.7)/0.3);
    lbl(ctx,S.a+'x²'+sgc(S.b,'x')+sg(S.c)+' = 0',24,44,'#1d4ed8',20);
    lbl(ctx,'x = ( −b ± √(b²−4ac) ) / 2a',24,80,'#52627a',17);
    if(c.none){
      lbl(ctx,'b² − 4ac = '+c.D+' < 0 이라 실근이 없다',40,150,'#b91c1c',20);
      return;
    }
    if(p1>0){
      ctx.globalAlpha=p1;
      lbl(ctx,'b² − 4ac = '+(S.b*S.b)+' − '+(4*S.a*S.c)+' = '+c.D,40,126,'#334155',18);
      lbl(ctx,'√'+c.D+' = '+r4(c.s),40,158,'#334155',18);
      ctx.globalAlpha=1;
    }
    if(p2>0){
      ctx.globalAlpha=p2;
      lbl(ctx,'x = ( '+(-S.b)+' ± '+r4(c.s)+' ) / '+(2*S.a),40,200,'#1d4ed8',19);
      lbl(ctx,'= '+r4(c.x1)+'  ,  '+r4(c.x2),40,236,'#15803d',22);
      ctx.globalAlpha=1;
    }
    if(p3>0){
      ctx.globalAlpha=p3;
      lbl(ctx,'식에 넣어 검산 : '+r6(c.f1)+' , '+r6(c.f2),40,278,'#b45309',18);
      ctx.globalAlpha=1;
    }
    box(ctx,20,296,400,124);
    lbl(ctx,(t===null)?'공식으로 구한 값이 정말 해일까?':('두 근 '+r4(c.x1)+' , '+r4(c.x2)),38,328,'#1f2937',18);
    lbl(ctx,(t===null)?'':('대입한 값 '+r6(c.f1)+' , '+r6(c.f2)),38,362,'#15803d',18);
    lbl(ctx,(t===null)?'':(c.sqInt?'√ 안이 완전제곱수 — 인수분해로도 풀린다':'√ 안이 완전제곱수가 아니다 — 인수분해로는 어렵다'),
        38,396,'#52627a',15);
  },
  record:function(S){
    var c=this.calc(S);
    if(c.none) return {none:true,a:S.a,b:S.b,c:S.c,D:c.D};
    return {none:false,a:S.a,b:S.b,c:S.c,D:c.D,
            x1:r4(c.x1),x2:r4(c.x2),
            f1:r6(c.f1),f2:r6(c.f2),
            zero:(Math.abs(c.f1)<1e-9&&Math.abs(c.f2)<1e-9),
            sqInt:c.sqInt,intRoot:c.intRoot};
  },
  headA:['번호','식','b²−4ac','두 근','대입한 값','0인가?','√ 안이 완전제곱?','근이 정수?'],
  rowA:function(r,i){
    if(r.none) return [i+1,r.a+'x²'+sgc(r.b,'x')+sg(r.c),r.D,'실근 없음','-','-','-','-'];
    return [i+1,r.a+'x²'+sgc(r.b,'x')+sg(r.c),r.D,'<b>'+r.x1+' , '+r.x2+'</b>',r.f1+' , '+r.f2,
            '<span class="'+(r.zero?'ok':'no')+'">'+(r.zero?'○':'×')+'</span>',
            '<span class="'+(r.sqInt?'ok':'no')+'">'+(r.sqInt?'○':'×')+'</span>',
            '<span class="'+(r.intRoot?'ok':'no')+'">'+(r.intRoot?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],valid=0,zero=0,sq=0,notsq=0,notsqZero=0,none=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.none){ none++; rows.push([r.a+'x²'+sgc(r.b,'x')+sg(r.c),r.D,'실근 없음','-','-']); continue; }
      valid++;
      if(r.zero) zero++;
      if(r.sqInt) sq++;
      else { notsq++; if(r.zero) notsqZero++; }
      rows.push([r.a+'x²'+sgc(r.b,'x')+sg(r.c), r.D, '<b>'+r.x1+' , '+r.x2+'</b>', r.f1+' , '+r.f2,
                 '<span class="'+(r.zero?'ok':'no')+'">'+(r.zero?'○':'×')+'</span>',
                 '<span class="'+(r.sqInt?'ok':'no')+'">'+(r.sqInt?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'대입한 값이 0이었던 횟수',big:zero+' / '+valid,
       p:'공식으로 구한 값이 정말 해인지 확인한 결과.'},
      {t:'√ 안이 완전제곱수였던 기록',big:sq+'개',
       p:'그때는 인수분해로도 풀 수 있다.'},
      {t:'완전제곱수가 아니었던 기록',big:notsq+'개',
       p:notsq?('그중 검산이 맞은 것 '+notsqZero+'개. 인수분해로는 어려워도 공식은 통했다.'):'√ 안이 완전제곱수가 아닌 경우도 만들어 보자.'}
    ];
    var concl;
    if(valid===0){
      concl='<b>더 해 보자</b> — b² − 4ac 가 0 이상이 되도록 계수를 잡아 보자.';
    } else if(zero===valid&&notsq>0){
      concl='<b>정리</b> — 근의 공식으로 구한 값을 식에 넣으면 <b>언제나 0</b>이 되었다. 진짜 해가 맞다. '
           +'특히 √ 안이 완전제곱수가 아니어서 <b>인수분해로는 풀 수 없는 경우에도</b> 공식은 그대로 통했다('+notsq+'번). '
           +'근의 공식은 완전제곱식으로 고치는 과정을 문자로 한 번에 해 둔 것이라, 계수만 넣으면 항상 답이 나온다. '
           +(none?('b²−4ac가 음수인 '+none+'번은 실근이 없었다.'):'');
    } else {
      concl='<b>정리</b> — 공식으로 구한 값이 해가 맞았다. √ 안이 완전제곱수가 아닌 경우도 기록해 보자.';
    }
    return {head:['식','b²−4ac','두 근','대입한 값','0인가?','완전제곱?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 삼각비의 활용
# ============================================================
LAB_TRIGUSE = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'높이 재기 판',
  action:'높이 구하기',
  hint0:'나무까지의 거리, 올려본각, 눈높이를 정해 보자.',
  sliders:[
    {id:'d',label:'나무까지 거리',min:4,max:20,value:10,color:'#2563eb',unit:'m'},
    {id:'th',label:'올려본각',min:15,max:70,value:35,color:'#f59e0b',unit:'°'},
    {id:'e',label:'눈높이',min:1,max:2,value:2,color:'#16a34a',unit:'m'}
  ],
  calc:function(S){
    var rad=S.th*Math.PI/180;
    var up=S.d*Math.tan(rad);
    var h=up+S.e;
    var hyp=Math.sqrt(S.d*S.d+up*up);
    return {rad:rad,up:up,h:h,hyp:hyp,
            wrongSin:S.d*Math.sin(rad)+S.e,
            wrongCos:S.d*Math.cos(rad)+S.e,
            noEye:up};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'눈높이 위쪽',v:ran?r3(c.up):'구해 보자'},
            {k:'나무의 높이',v:ran?r3(c.h):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '눈높이 위쪽이 '+r3(c.up)+'m, 나무 전체는 '+r3(c.h)+'m다. sin을 쓰면 '+r3(c.wrongSin)+'m가 나온다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var U=Math.min(16, 300/S.d, 200/Math.max(c.h,1));
    var GX=60, GY=360;
    var TX=GX+S.d*U;
    var EY=GY-S.e*U;
    ctx.strokeStyle='#94a3b8';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(30,GY);ctx.lineTo(410,GY);ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    ctx.strokeStyle='#16a34a';ctx.lineWidth=6;
    ctx.beginPath();ctx.moveTo(TX,GY);ctx.lineTo(TX,GY-c.h*U*Math.max(grow,0.05));ctx.stroke();
    if(grow>=1){
      ctx.beginPath();ctx.arc(TX,GY-c.h*U,14*U/12,0,Math.PI*2);
      ctx.fillStyle='rgba(22,163,74,0.35)';ctx.fill();
    }
    ctx.strokeStyle='#334155';ctx.lineWidth=3;
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX,EY);ctx.stroke();
    ctx.beginPath();ctx.arc(GX,EY-6,6,0,Math.PI*2);ctx.fillStyle='#334155';ctx.fill();
    ctx.strokeStyle='#cbd5e1';ctx.lineWidth=1.6;ctx.setLineDash([4,4]);
    ctx.beginPath();ctx.moveTo(GX,EY);ctx.lineTo(TX,EY);ctx.stroke();ctx.setLineDash([]);
    ctx.strokeStyle='#dc2626';ctx.lineWidth=2.4;
    ctx.beginPath();ctx.moveTo(GX,EY);ctx.lineTo(TX,EY-c.up*U);ctx.stroke();
    ctx.beginPath();ctx.arc(GX,EY,30,-c.rad,0);
    ctx.strokeStyle='#b45309';ctx.lineWidth=2;ctx.stroke();
    lbl(ctx,S.th+'°',GX+36,EY-10,'#b45309',14);
    lbl(ctx,'거리 '+S.d+'m',(GX+TX)/2,EY+18,'#64748b',13,'center');
    if(grow>=1){
      lbl(ctx,r2(c.up)+'m',TX+8,EY-c.up*U/2,'#b91c1c',14);
      lbl(ctx,'눈높이 '+S.e+'m',GX-52,(GY+EY)/2,'#15803d',12);
    }
    lbl(ctx,'거리와 올려본각으로 나무 높이 구하기',24,32,'#1d4ed8',17);
    box(ctx,20,376,400,44);
    lbl(ctx,(t===null)?'어떤 삼각비를 써야 할까?':('높이 = '+S.d+' × tan'+S.th+'° + '+S.e+' = '+r3(c.h)+'m'),34,402,'#1f2937',17);
    lbl(ctx,(t===null)?'':('sin을 쓰면 '+r3(c.wrongSin)+'m'),34,418,'#b91c1c',13);
  },
  record:function(S){
    var c=this.calc(S);
    return {d:S.d,th:S.th,e:S.e,
            up:r3(c.up),h:r3(c.h),
            sin:r3(c.wrongSin),cos:r3(c.wrongCos),noEye:r3(c.noEye),
            sinOk:(Math.abs(c.h-c.wrongSin)<1e-9),
            eyeGap:S.e,
            tanUse:true};
  },
  headA:['번호','거리','올려본각','눈높이','d·tanθ','나무 높이','sin을 쓰면','같나?','눈높이를 빼먹으면'],
  rowA:function(r,i){
    return [i+1,r.d+'m',r.th+'°',r.e+'m',r.up,'<b>'+r.h+'m</b>',r.sin,
            '<span class="'+(r.sinOk?'ok':'no')+'">'+(r.sinOk?'○':'×')+'</span>',
            r.noEye];
  },
  analyze:function(rec){
    var rows=[],sin=0,ths={},tn=0,mx=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.sinOk) sin++;
      if(!ths[r.th]){ ths[r.th]=true; tn++; }
      var g=parseFloat(r.h)-parseFloat(r.sin);
      if(g>mx) mx=g;
      rows.push([r.d+'m', r.th+'°', r.e+'m', r.up, '<b>'+r.h+'m</b>', r.sin,
                 '<span class="'+(r.sinOk?'ok':'no')+'">'+(r.sinOk?'○':'×')+'</span>',
                 r.noEye]);
    }
    var stats=[
      {t:'sin을 써서 맞은 횟수',big:sin+' / '+rec.length,
       p:'밑변과 높이의 관계는 tan이 맡는다.'},
      {t:'시험한 올려본각',big:tn+'가지',p:'각이 클수록 두 값의 차이가 커졌다.'},
      {t:'가장 큰 차이',big:r2(mx)+'m',p:'sin으로 잘못 구하면 이만큼 어긋난다.'}
    ];
    var concl;
    if(rec.length<4){
      concl='<b>더 해 보자</b> — 각을 15°에서 70°까지 바꿔 가며 기록해 두 값의 차이를 확인해 보자.';
    } else if(sin===0){
      concl='<b>정리</b> — 밑변(거리)을 알고 높이를 구할 때는 <b>tan</b>을 쓴다. sin은 빗변과 높이의 관계라 여기서는 맞지 않았고, '
           +'각이 클수록 차이가 벌어졌다(최대 '+r2(mx)+'m). '
           +'또 눈높이에서 잰 각이므로 <b>눈높이를 더해야</b> 나무 전체 높이가 된다. '
           +'어떤 두 변이 주어졌는지를 보고 삼각비를 고르는 것이 핵심이다.';
    } else {
      concl='<b>정리</b> — 거리와 각으로 높이를 구할 때는 tan을 쓴다. 각을 더 바꿔 가며 확인해 보자.';
    }
    return {head:['거리','각','눈높이','d·tanθ','높이','sin 사용','같나?','눈높이 뺀 값'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("m3_sqrt_addition_lab.html",
     "제곱근 덧셈 실험실 — √2 + √3 은 √5 일까?",
     "제곱근 덧셈 실험실 — √2 + √3 은 √5 일까?",
     "두 항을 길이로 이어 붙여 실제 합을 재고, 계수끼리 더한 값·근호 안끼리 더한 값과 비교한다.",
     LAB_SQADD),
    ("m3_real_density_lab.html",
     "실수 실험실 — 아무리 좁혀도 무리수가 있을까?",
     "실수 실험실 — 아무리 좁혀도 무리수가 있을까?",
     "구간을 점점 좁혀 가며 그 안에 있는 무리수와 유리수를 실제로 찾아본다.",
     LAB_DENSE),
    ("m3_complete_square_lab.html",
     "완전제곱 실험실 — 무엇을 더해야 정사각형이 될까?",
     "완전제곱 실험실 — 무엇을 더해야 정사각형이 될까?",
     "넓이 그림에서 모퉁이 빈 칸을 채우며 (b/2)² 을 찾고, 값을 대입해 검산한다.",
     LAB_CSQ),
    ("m3_quadratic_formula_lab.html",
     "근의 공식 실험실 — 공식으로 구한 값이 정말 해일까?",
     "근의 공식 실험실 — 공식으로 구한 값이 정말 해일까?",
     "근의 공식으로 두 근을 구해 원래 식에 대입하고, 인수분해로 풀리는지도 함께 확인한다.",
     LAB_QF),
    ("m3_trig_application_lab.html",
     "삼각비 활용 실험실 — 어떤 삼각비를 써야 할까?",
     "삼각비 활용 실험실 — 어떤 삼각비를 써야 할까?",
     "거리와 올려본각으로 나무 높이를 구하고, sin을 썼을 때와 비교한다.",
     LAB_TRIGUSE),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c39_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
