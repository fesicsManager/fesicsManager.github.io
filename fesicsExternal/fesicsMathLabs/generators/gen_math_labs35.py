# -*- coding: utf-8 -*-
"""중2 보강 5종"""
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
function sg(v){return (v<0)?(' − '+(-v)):(' + '+v);}
function sgc(v,s){ if(v===0) return ''; return (v<0)?(' − '+(-v)+s):(' + '+v+s); }
var CX=220, CY=210, U=22;
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
# 1. 순환마디의 길이
# ============================================================
LAB_CYCLE = BASE + r"""
function expand(a,b){
  var r=a%b, seen={}, digs=[], pos=0, start=-1;
  while(r!==0 && pos<40){
    if(seen[r]!==undefined){ start=seen[r]; break; }
    seen[r]=pos; r*=10; digs.push(Math.floor(r/b)); r=r%b; pos++;
  }
  return {digs:digs,start:start,finite:(start<0)};
}
function strip25(n){ while(n%2===0) n/=2; while(n%5===0) n/=5; return n; }
var LAB = {
  cw:440, ch:400, cvTitle:'순환마디 판',
  action:'끝까지 나누기',
  hint0:'분자와 분모를 정하고, 되풀이되는 자리가 몇 개인지 세어 보자.',
  sliders:[
    {id:'a',label:'분자',min:1,max:9,value:1,color:'#2563eb',unit:''},
    {id:'b',label:'분모',min:2,max:30,value:7,color:'#16a34a',unit:''}
  ],
  calc:function(S){
    var g=gcd(S.a,S.b), ra=S.a/g, rb=S.b/g;
    var e=expand(S.a,S.b);
    var len=e.finite?0:(e.digs.length-e.start);
    return {ra:ra,rb:rb,m:strip25(rb),e:e,len:len,
            pre:e.finite?e.digs.length:e.start};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'기약분수',v:c.ra+'/'+c.rb},
            {k:'순환마디 길이',v:ran?(c.e.finite?'유한소수':(c.len+'자리')):'나눠 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.e.finite) return S.a+'/'+S.b+'는 유한소수다. 분모에서 2와 5를 걷어내면 1만 남는다. 기록해 보자.';
    return '순환마디는 '+c.len+'자리다. 분모에서 2와 5를 걷어내면 '+c.m+'이 남는다. 분자를 바꿔도 같을까?';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*Math.max(1,c.e.digs.length));
    lbl(ctx,S.a+' / '+S.b+'  =  기약분수 '+c.ra+' / '+c.rb,24,38,'#1d4ed8',18);
    lbl(ctx,'분모에서 2와 5를 걷어내면 : '+c.m,24,66,'#15803d',17);
    ctx.font='bold 22px sans-serif';ctx.textAlign='left';
    var px=40, py=132;
    ctx.fillStyle='#1f2937';ctx.fillText('0.',px,py);
    px+=ctx.measureText('0.').width;
    for(i=0;i<c.e.digs.length&&i<shown;i++){
      var rep=(c.e.start>=0&&i>=c.e.start);
      var ch=''+c.e.digs[i];
      ctx.fillStyle=rep?'#dc2626':'#1f2937';
      ctx.fillText(ch,px,py);
      if(rep){
        ctx.strokeStyle='#dc2626';ctx.lineWidth=2;
        ctx.beginPath();ctx.moveTo(px,py-22);ctx.lineTo(px+ctx.measureText(ch).width,py-22);ctx.stroke();
      }
      px+=ctx.measureText(ch).width;
      if(px>390) break;
    }
    if(!c.e.finite&&shown>=c.e.digs.length){ ctx.fillStyle='#dc2626';ctx.fillText(' …',px,py); }
    ctx.font='bold 18px sans-serif';
    lbl(ctx,'빨간 부분이 되풀이되는 자리',40,164,'#94a3b8',15);
    box(ctx,20,196,400,188);
    lbl(ctx,(t===null)?'몇 자리가 되풀이될까?':(c.e.finite?'유한소수 — 되풀이가 없다':('순환마디 '+c.len+'자리')),
        38,232,c.e.finite?'#15803d':'#b91c1c',20);
    lbl(ctx,'되풀이 전 자리 수 : '+c.pre,38,268,'#52627a',17);
    lbl(ctx,'2·5를 걷어낸 분모 : '+c.m,38,302,'#334155',17);
    lbl(ctx,(t===null)?'':'분자를 바꿔도 순환마디 길이가 같은지 확인해 보자',38,344,'#94a3b8',15);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,ra:c.ra,rb:c.rb,m:c.m,
            len:c.len,pre:c.pre,finite:c.e.finite};
  },
  headA:['번호','분수','기약분수','2·5 걷어낸 분모','유한소수?','되풀이 전 자리','순환마디 길이'],
  rowA:function(r,i){
    return [i+1,r.a+'/'+r.b,r.ra+'/'+r.rb,r.m,
            '<span class="'+(r.finite?'ok':'no')+'">'+(r.finite?'○':'×')+'</span>',
            r.pre,'<b>'+(r.finite?'-':(r.len+'자리'))+'</b>'];
  },
  analyze:function(rec){
    var rows=[],g={},pairs=0,agree=0,fin=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.finite) fin++;
      var k='m'+r.m, note='첫 기록';
      if(g[k]!==undefined){
        pairs++;
        var s=(g[k]===r.len);
        if(s) agree++;
        note='<span class="'+(s?'ok':'no')+'">'+(s?'길이 같음':'길이 다름')+'</span>';
      } else { g[k]=r.len; }
      rows.push([r.a+'/'+r.b, r.ra+'/'+r.rb, r.m,
                 '<span class="'+(r.finite?'ok':'no')+'">'+(r.finite?'○':'×')+'</span>',
                 '<b>'+(r.finite?'-':(r.len+'자리'))+'</b>', note]);
    }
    var lines=[],k2,cnt=0;
    for(k2 in g){ cnt++; if(lines.length<6) lines.push(k2.slice(1)+' → '+g[k2]+'자리'); }
    var stats=[
      {t:'2·5를 걷어낸 분모가 같은 짝',big:pairs+'쌍',
       p:pairs?('그중 순환마디 길이가 같았던 것 '+agree+'쌍.'):'분자만 바꾸거나 분모에 2를 곱해 같은 값이 되게 해 보자.'},
      {t:'나타난 분모별 순환마디 길이',big:cnt+'가지',p:lines.join(' / ')},
      {t:'유한소수였던 기록',big:fin+'개',p:'걷어낸 분모가 1이면 유한소수다.'}
    ];
    var concl;
    if(pairs===0){
      concl='<b>더 해 보자</b> — 1/7 과 3/7 처럼 <b>분자만 다른</b> 분수, 또는 1/7 과 1/14 처럼 <b>2를 곱한 분모</b>를 함께 기록해 보자.';
    } else if(agree===pairs){
      concl='<b>정리</b> — 순환마디의 길이는 <b>분자와 상관없었고</b>, 분모에서 2와 5를 걷어낸 수에만 달려 있었다. '
           +'7이면 6자리, 3이면 1자리, 11이면 2자리처럼 정해진다. '
           +'2와 5는 10의 약수라 자리만 밀어낼 뿐 되풀이를 만들지 않기 때문이다. '
           +'그래서 1/7과 1/14는 순환마디 길이가 같고, 시작 위치만 한 칸 밀린다.';
    } else {
      concl='<b>확인 필요</b> — 같은 분모인데 길이가 다른 기록이 있다.';
    }
    return {head:['분수','기약분수','걷어낸 분모','유한?','순환마디','같은 분모끼리'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 순환소수의 계산
# ============================================================
LAB_RSUM = BASE + r"""
function dec(n,d,k){
  var s='',r=n%d,i;
  for(i=0;i<k;i++){ r*=10; s+=Math.floor(r/d); r=r%d; }
  return Math.floor(n/d)+'.'+s;
}
var LAB = {
  cw:440, ch:400, cvTitle:'순환소수 계산판',
  action:'분수로 바꿔 더하기',
  hint0:'두 순환소수 0.p… 와 0.q… 를 정해 보자. (순환마디 한 자리)',
  sliders:[
    {id:'p',label:'첫 번째 순환마디',min:1,max:9,value:3,color:'#2563eb',unit:''},
    {id:'q',label:'두 번째 순환마디',min:1,max:9,value:6,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var n=S.p+S.q;
    var g=gcd(n,9)||1;
    return {n:n,num:n/g,den:9/g,val:n/9,
            whole:(n%9===0),
            dstr:dec(n,9,8)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'식',v:'0.'+S.p+'̇ + 0.'+S.q+'̇'},
            {k:'합',v:ran?(c.num+'/'+c.den+((c.den===1)?(' = '+c.num):'')):'더해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return (S.p+'/9 + '+S.q+'/9 = '+c.n+'/9')+((c.den===1)?(' = '+c.num+' — 정수가 되었다!'):(' = '+c.num+'/'+c.den))+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var p1=(t===null)?0:Math.min(1,t/0.4);
    var p2=(t===null)?0:Math.max(0,Math.min(1,(t-0.4)/0.3));
    var p3=(t===null)?0:Math.max(0,(t-0.7)/0.3);
    lbl(ctx,'0.'+S.p+S.p+S.p+'…  +  0.'+S.q+S.q+S.q+'…',40,80,'#1f2937',24);
    if(p1>0){
      ctx.globalAlpha=p1;
      lbl(ctx,'분수로 바꾸면',40,120,'#52627a',17);
      lbl(ctx,S.p+'/9  +  '+S.q+'/9',40,160,'#1d4ed8',24);
      ctx.globalAlpha=1;
    }
    if(p2>0){
      ctx.globalAlpha=p2;
      lbl(ctx,'=  '+c.n+' / 9',40,204,'#15803d',24);
      ctx.globalAlpha=1;
    }
    if(p3>0){
      ctx.globalAlpha=p3;
      lbl(ctx,(c.den===1)?('=  '+c.num+'  (정수)'):('=  '+c.num+' / '+c.den),40,246,
          (c.den===1)?'#b45309':'#15803d',24);
      ctx.globalAlpha=1;
    }
    lbl(ctx,'순환소수끼리 그냥 더해도 될까?',24,38,'#1d4ed8',18);
    box(ctx,20,266,400,118);
    lbl(ctx,'소수로 이어 쓰면 0.'+(S.p+S.q>9?'…':(''+(S.p+S.q)))+'… 가 될까?',38,298,'#b91c1c',16);
    lbl(ctx,(t===null)?'분수로 바꿔 더해 보자':('정확한 합 = '+c.num+((c.den===1)?'':('/'+c.den))),38,332,'#1f2937',20);
    lbl(ctx,(t===null)?'':('소수로 다시 쓰면 '+c.dstr+'…'),38,366,'#52627a',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {p:S.p,q:S.q,sum9:c.n,num:c.num,den:c.den,
            val:r3(c.val),whole:c.whole,
            naive:(S.p+S.q),
            naiveOk:(S.p+S.q<=9),
            nine:(c.n===9)};
  },
  headA:['번호','식','p/9 + q/9','합','기약분수','정수?','자리끼리 더하면','한 자리인가?'],
  rowA:function(r,i){
    return [i+1,'0.'+r.p+'̇ + 0.'+r.q+'̇',r.p+'/9 + '+r.q+'/9','<b>'+r.sum9+'/9</b>',
            r.num+((r.den===1)?'':('/'+r.den)),
            '<span class="'+(r.whole?'ok':'no')+'">'+(r.whole?'○':'×')+'</span>',
            r.naive,
            '<span class="'+(r.naiveOk?'ok':'no')+'">'+(r.naiveOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],whole=0,nine=0,over=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.whole) whole++;
      if(r.nine) nine++;
      if(!r.naiveOk) over++;
      rows.push(['0.'+r.p+'̇ + 0.'+r.q+'̇', r.p+'/9 + '+r.q+'/9', '<b>'+r.sum9+'/9</b>',
                 r.num+((r.den===1)?'':('/'+r.den)),
                 '<span class="'+(r.whole?'ok':'no')+'">'+(r.whole?'○':'×')+'</span>',
                 r.naive,
                 '<span class="'+(r.naiveOk?'ok':'no')+'">'+(r.naiveOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'합이 정수가 된 기록',big:whole+'개',
       p:whole?('그중 p + q = 9 였던 것 '+nine+'개.'):'p + q 가 9가 되도록 맞춰 보자.'},
      {t:'자리끼리 더한 값이 한 자리를 넘은 기록',big:over+'개',
       p:over?'소수점 아래에서 받아올림이 생겨 그냥 이어 쓸 수 없다.':'p + q 를 10 이상으로도 해 보자.'},
      {t:'전체 기록',big:rec.length+'개',p:'0.ṗ = p/9 로 바꾸면 계산이 정확해진다.'}
    ];
    var concl;
    if(nine===0){
      concl='<b>더 해 보자</b> — p + q = 9 가 되도록 (예: 3과 6) 맞춰 보자. 합이 무엇이 되는지가 핵심이다.';
    } else {
      concl='<b>정리</b> — 순환소수는 <b>분수로 바꿔 계산</b>해야 정확했다. 0.ṗ = p/9 이므로 두 수의 합은 (p+q)/9 다. '
           +'특히 <b>0.3̇ + 0.6̇ = 9/9 = 1</b> 이었다. 소수 자리를 그냥 이어 쓰면 0.9̇ 가 되는데, 이 값이 곧 1이다. '
           +'p + q 가 10 이상이면 받아올림이 생겨 자리끼리 더하는 방법은 아예 통하지 않는다.';
    }
    return {head:['식','분수로','합','기약분수','정수?','자리끼리','한 자리?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 연립방정식의 해
# ============================================================
LAB_SYSCHK = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'연립방정식 검산판',
  action:'두 식에 대입해 보기',
  hint0:'후보로 삼을 x와 y를 정해 보자. 식은 2x + y = 8 과 x − y = 1 이다.',
  sliders:[
    {id:'x',label:'x',min:-3,max:8,value:4,color:'#2563eb',unit:''},
    {id:'y',label:'y',min:-3,max:8,value:0,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var e1=2*S.x+S.y, e2=S.x-S.y;
    return {e1:e1,e2:e2,ok1:(e1===8),ok2:(e2===1),
            both:(e1===8&&e2===1)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'2x + y',v:c.e1+' (8이어야 함)'},
            {k:'x − y',v:ran?(c.e2+' (1이어야 함)'):'대입해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '2x+y = '+c.e1+', x−y = '+c.e2+'.  '+(c.both?'두 식을 모두 만족한다 — 연립방정식의 해다.':(c.ok1||c.ok2)?'한 식만 만족한다 — 연립방정식의 해가 아니다.':'둘 다 만족하지 않는다.')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,7,6);
    function line(a,b,cc,col){
      ctx.strokeStyle=col;ctx.lineWidth=3;ctx.beginPath();
      var st=false;
      for(i=-70;i<=70;i++){
        var x=i/10, y=(cc-a*x)/b;
        if(y<-6||y>6){ st=false; continue; }
        if(!st){ ctx.moveTo(CX+x*U,CY-y*U); st=true; } else ctx.lineTo(CX+x*U,CY-y*U);
      }
      ctx.stroke();
    }
    line(2,1,8,'#2563eb');
    line(1,-1,1,'#dc2626');
    ctx.beginPath();ctx.arc(CX+3*U,CY-2*U,6,0,Math.PI*2);
    ctx.fillStyle='#f59e0b';ctx.fill();
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0&&Math.abs(S.x)<=7&&Math.abs(S.y)<=6){
      ctx.beginPath();ctx.arc(CX+S.x*U,CY-S.y*U,8,0,Math.PI*2);
      ctx.fillStyle=c.both?'#15803d':'#94a3b8';ctx.fill();
      ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      lbl(ctx,'('+S.x+', '+S.y+')',CX+S.x*U+12,CY-S.y*U-8,c.both?'#15803d':'#64748b',14);
    }
    lbl(ctx,'파랑 2x + y = 8      빨강 x − y = 1',24,32,'#334155',16);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'두 식을 모두 만족할까?':('2x+y = '+c.e1+' '+(c.ok1?'✔':'✘')+'      x−y = '+c.e2+' '+(c.ok2?'✔':'✘')),
        38,376,'#1f2937',18);
    lbl(ctx,(t===null)?'':(c.both?'연립방정식의 해다':'연립방정식의 해가 아니다'),
        38,406,c.both?'#15803d':'#b91c1c',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {x:S.x,y:S.y,e1:c.e1,e2:c.e2,ok1:c.ok1,ok2:c.ok2,both:c.both,
            one:((c.ok1&&!c.ok2)||(!c.ok1&&c.ok2))};
  },
  headA:['번호','(x, y)','2x+y','8인가?','x−y','1인가?','둘 다 만족?'],
  rowA:function(r,i){
    return [i+1,'('+r.x+', '+r.y+')',r.e1,
            '<span class="'+(r.ok1?'ok':'no')+'">'+(r.ok1?'○':'×')+'</span>',
            r.e2,
            '<span class="'+(r.ok2?'ok':'no')+'">'+(r.ok2?'○':'×')+'</span>',
            '<span class="'+(r.both?'ok':'no')+'">'+(r.both?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],both=0,one=0,none=0,pts={},bn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.both){ both++; pts[r.x+','+r.y]=true; }
      else if(r.one) one++;
      else none++;
      rows.push(['('+r.x+', '+r.y+')', r.e1,
                 '<span class="'+(r.ok1?'ok':'no')+'">'+(r.ok1?'○':'×')+'</span>',
                 r.e2,
                 '<span class="'+(r.ok2?'ok':'no')+'">'+(r.ok2?'○':'×')+'</span>',
                 '<span class="'+(r.both?'ok':'no')+'">'+(r.both?'○':'×')+'</span>']);
    }
    var k;
    for(k in pts) bn++;
    var stats=[
      {t:'두 식을 모두 만족한 기록',big:both+' / '+rec.length,
       p:both?('서로 다른 해는 '+bn+'개.'):'교점 (3, 2)를 넣어 보자.'},
      {t:'한 식만 만족한 기록',big:one+'개',
       p:one?'한 직선 위에는 있지만 교점은 아니다.':'(4, 0)처럼 한 식만 맞는 점도 넣어 보자.'},
      {t:'둘 다 아닌 기록',big:none+'개',p:'두 직선 어디에도 없는 점이다.'}
    ];
    var concl;
    if(both===0||one===0){
      concl='<b>더 해 보자</b> — 한 식만 만족하는 점(예: (4, 0))과 두 식을 모두 만족하는 점을 <b>모두</b> 넣어 보자.';
    } else if(bn===1){
      concl='<b>정리</b> — 한 식만 만족하는 점은 여러 개였지만, <b>두 식을 모두 만족하는 점은 단 하나 (3, 2)</b>뿐이었다. '
           +'각 식은 직선 하나를 나타내고, 연립방정식의 해는 <b>두 직선이 만나는 점</b>이다. '
           +'그래서 답을 구한 뒤에는 반드시 <b>두 식 모두에</b> 대입해 확인해야 한다.';
    } else {
      concl='<b>확인 필요</b> — 두 식을 모두 만족하는 점이 여러 개로 기록되었다.';
    }
    return {head:['(x, y)','2x+y','8?','x−y','1?','둘 다?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 일차부등식의 해
# ============================================================
LAB_INEQSOL = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'부등식 해 판',
  action:'하나씩 넣어 보기',
  hint0:'ax + b > 0 의 계수를 정하고, 어떤 x가 만족하는지 보자.',
  sliders:[
    {id:'a',label:'a',min:-5,max:5,value:-2,color:'#2563eb',unit:''},
    {id:'b',label:'b',min:-10,max:10,value:6,color:'#16a34a',unit:''}
  ],
  calc:function(S){
    var hits=[],i;
    for(i=-10;i<=10;i++){ if(S.a*i+S.b>0) hits.push(i); }
    var bd=(S.a===0)?null:(-S.b/S.a);
    var kind;
    if(S.a===0) kind=(S.b>0)?'모든 x':'해 없음';
    else if(S.a>0) kind='x > '+r2(bd);
    else kind='x < '+r2(bd);
    return {hits:hits,bd:bd,kind:kind,
            naive:(S.a===0)?null:(-S.b/S.a),
            wrongKind:(S.a===0)?null:('x > '+r2(-S.b/S.a))};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'식',v:S.a+'x'+sg(S.b)+' > 0'},
            {k:'해',v:ran?c.kind:'넣어 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '−10부터 10까지 중 '+c.hits.length+'개가 만족했다. 해는 「'+c.kind+'」다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var X0=36, X1=404, LO=-11, HI=11;
    function px(v){ return X0+(X1-X0)*(v-LO)/(HI-LO); }
    var Y=180;
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(X0,Y);ctx.lineTo(X1,Y);ctx.stroke();
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*21);
    for(i=-10;i<=10;i++){
      var on=(i+10<shown);
      var hit=(S.a*i+S.b>0);
      var x=px(i);
      ctx.beginPath();ctx.moveTo(x,Y-7);ctx.lineTo(x,Y+7);
      ctx.strokeStyle='#cbd5e1';ctx.lineWidth=1.2;ctx.stroke();
      if(on){
        ctx.beginPath();ctx.arc(x,Y-22,7,0,Math.PI*2);
        ctx.fillStyle=hit?'#22c55e':'#fecaca';ctx.fill();
        ctx.strokeStyle=hit?'#15803d':'#dc2626';ctx.lineWidth=1.6;ctx.stroke();
      }
      if(i%5===0){
        ctx.fillStyle='#94a3b8';ctx.font='12px sans-serif';ctx.textAlign='center';
        ctx.fillText(i,x,Y+24);
      }
    }
    ctx.textAlign='left';
    if(shown>=21&&c.bd!==null&&Math.abs(c.bd)<=11){
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=2.4;ctx.setLineDash([5,4]);
      ctx.beginPath();ctx.moveTo(px(c.bd),Y-58);ctx.lineTo(px(c.bd),Y+16);ctx.stroke();ctx.setLineDash([]);
      lbl(ctx,'경계 '+r2(c.bd),px(c.bd),Y-64,'#b45309',14,'center');
    }
    lbl(ctx,S.a+'x'+sg(S.b)+' > 0',24,38,'#1d4ed8',20);
    lbl(ctx,'초록 = 만족,  빨강 = 만족 안 함',24,66,'#52627a',14);
    box(ctx,20,236,400,148);
    lbl(ctx,(t===null)?'어떤 x가 만족할까?':('만족한 정수 '+c.hits.length+'개'),38,270,'#1f2937',19);
    lbl(ctx,(t===null)?'':(c.hits.length?('가장 작은 값 '+c.hits[0]+'  가장 큰 값 '+c.hits[c.hits.length-1]):'없음'),
        38,304,'#52627a',17);
    lbl(ctx,(t===null)?'':('해 : '+c.kind),38,340,'#15803d',20);
    lbl(ctx,(t===null)?'':((S.a<0)?'a가 음수라 부등호가 뒤집혔다':'a가 양수라 부등호가 그대로다'),
        38,372,(S.a<0)?'#b91c1c':'#52627a',15);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,kind:c.kind,cnt:c.hits.length,
            bd:(c.bd===null)?'-':r2(c.bd),
            wrong:(c.wrongKind===null)?'-':c.wrongKind,
            wOk:(S.a>0),neg:(S.a<0),zero:(S.a===0),
            lo:c.hits.length?c.hits[0]:'-',
            hi:c.hits.length?c.hits[c.hits.length-1]:'-'};
  },
  headA:['번호','부등식','a의 부호','경계','만족한 정수','가장 작은/큰 값','해','부호 그대로 두면'],
  rowA:function(r,i){
    return [i+1,r.a+'x'+sg(r.b)+' > 0',r.zero?'0':(r.neg?'음수':'양수'),r.bd,r.cnt+'개',
            r.lo+' ~ '+r.hi,'<b>'+r.kind+'</b>',
            '<span class="'+(r.wOk?'ok':'no')+'">'+r.wrong+'</span>'];
  },
  analyze:function(rec){
    var rows=[],pos=0,posOk=0,neg=0,negFlip=0,zero=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.zero) zero++;
      else if(r.neg){ neg++; if(r.kind.indexOf('<')>=0) negFlip++; }
      else { pos++; if(r.kind.indexOf('>')>=0) posOk++; }
      rows.push([r.a+'x'+sg(r.b)+' > 0', r.zero?'0':(r.neg?'음수':'양수'), r.bd, r.cnt+'개',
                 r.lo+' ~ '+r.hi, '<b>'+r.kind+'</b>']);
    }
    var stats=[
      {t:'a가 양수였던 기록',big:pos+'개',
       p:pos?('그중 해가 x > 인 것 '+posOk+'개.'):'a를 양수로도 해 보자.'},
      {t:'a가 음수였던 기록',big:neg+'개',
       p:neg?('그중 해가 x < 인 것 '+negFlip+'개.'):'a를 음수로도 해 보자.'},
      {t:'a = 0 이었던 기록',big:zero+'개',
       p:zero?'x가 사라져 모든 x이거나 해가 없다.':'a = 0 도 해 보자.'}
    ];
    var concl;
    if(pos===0||neg===0){
      concl='<b>더 해 보자</b> — a가 <b>양수인 경우와 음수인 경우</b>를 모두 기록해야 부등호 방향의 규칙이 보인다.';
    } else if(posOk===pos&&negFlip===neg){
      concl='<b>정리</b> — 실제로 수를 하나씩 넣어 보니, a가 양수면 해가 <b>x > 경계</b>, 음수면 <b>x < 경계</b>였다. '
           +'경계값 −b/a 는 두 경우 모두 같은데 <b>부등호 방향만 반대</b>다. '
           +'a로 나눌 때 a가 음수면 부등호를 뒤집어야 하기 때문이다. '
           +(zero?'a = 0 이면 x가 사라져 «모든 x» 또는 «해 없음»이 된다.':'');
    } else {
      concl='<b>확인 필요</b> — 규칙과 어긋난 기록이 있다.';
    }
    return {head:['부등식','a','경계','만족 개수','범위','해'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 그래프가 지나는 사분면
# ============================================================
LAB_QUAD = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'사분면 판',
  action:'지나는 사분면 찾기',
  hint0:'기울기와 y절편의 부호를 바꿔 보자.',
  sliders:[
    {id:'a',label:'기울기 a',min:-4,max:4,value:2,color:'#2563eb',unit:''},
    {id:'b',label:'y절편 b',min:-6,max:6,value:3,color:'#16a34a',unit:''}
  ],
  calc:function(S){
    var q=[false,false,false,false],i;
    for(i=-2000;i<=2000;i++){
      var x=i/100, y=S.a*x+S.b;
      if(Math.abs(x)<1e-9||Math.abs(y)<1e-9) continue;
      if(x>0&&y>0) q[0]=true;
      else if(x<0&&y>0) q[1]=true;
      else if(x<0&&y<0) q[2]=true;
      else q[3]=true;
    }
    var list=[];
    for(i=0;i<4;i++){ if(q[i]) list.push(i+1); }
    var miss=[];
    for(i=0;i<4;i++){ if(!q[i]) miss.push(i+1); }
    return {q:q,list:list,miss:miss,
            xi:(S.a===0)?null:(-S.b/S.a)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'a, b의 부호',v:((S.a>0)?'+':((S.a<0)?'−':'0'))+' , '+((S.b>0)?'+':((S.b<0)?'−':'0'))},
            {k:'지나는 사분면',v:ran?('제 '+c.list.join(', ')+' 사분면'):'찾아보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '제 '+c.list.join(', ')+' 사분면을 지난다. '+(c.miss.length?('제 '+c.miss.join(', ')+' 사분면은 지나지 않는다.'):'네 사분면을 모두 지난다.')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var grow=(t===null)?0:Math.min(1,t);
    var labels=[[1,1],[-1,1],[-1,-1],[1,-1]];
    for(i=0;i<4;i++){
      if(grow>0&&c.q[i]){
        ctx.fillStyle='rgba(37,99,235,0.07)';
        ctx.fillRect(CX+((labels[i][0]>0)?0:-7*U),CY+((labels[i][1]>0)?-6*U:0),7*U,6*U);
      }
    }
    grid(ctx,7,6);
    ctx.font='bold 15px sans-serif';ctx.textAlign='center';
    for(i=0;i<4;i++){
      var lx=CX+labels[i][0]*4.6*U, ly=CY-labels[i][1]*4.2*U;
      ctx.fillStyle=(grow>0&&c.q[i])?'#1d4ed8':'#cbd5e1';
      ctx.fillText('제'+(i+1)+'사분면',lx,ly);
    }
    ctx.textAlign='left';
    ctx.strokeStyle='#dc2626';ctx.lineWidth=3;ctx.beginPath();
    var st=false;
    for(i=-70;i<=70;i++){
      var x=i/10, y=S.a*x+S.b;
      if(y<-6||y>6){ st=false; continue; }
      if(!st){ ctx.moveTo(CX+x*U,CY-y*U); st=true; } else ctx.lineTo(CX+x*U,CY-y*U);
    }
    ctx.stroke();
    if(Math.abs(S.b)<=6){
      ctx.beginPath();ctx.arc(CX,CY-S.b*U,6,0,Math.PI*2);
      ctx.fillStyle='#16a34a';ctx.fill();
    }
    if(c.xi!==null&&Math.abs(c.xi)<=7){
      ctx.beginPath();ctx.arc(CX+c.xi*U,CY,6,0,Math.PI*2);
      ctx.fillStyle='#f59e0b';ctx.fill();
    }
    lbl(ctx,'y = '+S.a+'x'+sg(S.b),24,32,'#1d4ed8',18);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'어느 사분면을 지날까?':('지나는 곳 : 제 '+c.list.join(', ')+' 사분면'),38,376,'#1f2937',18);
    lbl(ctx,(t===null)?'':(c.miss.length?('지나지 않는 곳 : 제 '+c.miss.join(', ')+' 사분면'):'네 사분면 모두 지난다'),
        38,406,'#b91c1c',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,
            sa:(S.a>0)?'+':((S.a<0)?'−':'0'),
            sb:(S.b>0)?'+':((S.b<0)?'−':'0'),
            list:c.list.join(', '),miss:c.miss.length?c.miss.join(', '):'없음',
            n:c.list.length,
            all4:(c.list.length===4)};
  },
  headA:['번호','식','a 부호','b 부호','지나는 사분면','지나지 않는 곳','개수'],
  rowA:function(r,i){
    return [i+1,r.a+'x'+sg(r.b),r.sa,r.sb,'<b>제 '+r.list+'</b>',r.miss,r.n+'개'];
  },
  analyze:function(rec){
    var rows=[],g={},gn=0,pairs=0,agree=0,three=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.n===3) three++;
      var k=r.sa+r.sb, note='첫 기록';
      if(g[k]!==undefined){
        pairs++;
        var s=(g[k]===r.list);
        if(s) agree++;
        note='<span class="'+(s?'ok':'no')+'">'+(s?'같은 결과':'다른 결과')+'</span>';
      } else { g[k]=r.list; gn++; }
      rows.push([r.a+'x'+sg(r.b), r.sa+' , '+r.sb, '<b>제 '+r.list+'</b>', r.miss, note]);
    }
    var lines=[],k2;
    for(k2 in g){ lines.push('('+k2.charAt(0)+', '+k2.charAt(1)+') → 제 '+g[k2]); }
    var stats=[
      {t:'시험한 부호 조합',big:gn+'가지',p:lines.join(' / ')},
      {t:'같은 부호 조합끼리 결과가 같았던 짝',big:pairs?(agree+' / '+pairs):'비교 없음',
       p:pairs?'a, b의 크기가 달라도 부호만 같으면 같은 결과였다.':'같은 부호 조합으로 값만 바꿔 기록해 보자.'},
      {t:'세 사분면만 지난 기록',big:three+'개',p:'기울기가 0이 아니면 보통 세 사분면을 지난다.'}
    ];
    var concl;
    if(gn<4){
      concl='<b>더 해 보자</b> — a와 b의 부호 조합 <b>네 가지</b>를 모두 만들어 기록해 보자.';
    } else if(agree===pairs){
      concl='<b>정리</b> — 지나는 사분면은 a와 b의 <b>부호만으로</b> 정해졌다. 크기를 바꿔도 결과가 같았다. '
           +'외울 것이 아니라, y절편이 어디 있고 오른쪽으로 오르는지 내리는지만 보면 바로 알 수 있다. '
           +'기울기가 0이 아니면 직선은 보통 <b>세 사분면</b>을 지나고, 지나지 않는 한 곳이 답이 되는 문제가 많다.';
    } else {
      concl='<b>확인 필요</b> — 같은 부호 조합인데 결과가 다른 기록이 있다.';
    }
    return {head:['식','a, b 부호','지나는 사분면','지나지 않는 곳','같은 조합끼리'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("m2_repeating_cycle_lab.html",
     "순환마디 실험실 — 되풀이 길이는 무엇이 정할까?",
     "순환마디 실험실 — 되풀이 길이는 무엇이 정할까?",
     "분수를 끝까지 나누어 순환마디의 길이를 세고, 분자와 분모 중 무엇에 달렸는지 확인한다.",
     LAB_CYCLE),
    ("m2_repeating_arithmetic_lab.html",
     "순환소수 계산 실험실 — 0.3̇ + 0.6̇ 은 얼마일까?",
     "순환소수 계산 실험실 — 0.3̇ + 0.6̇ 은 얼마일까?",
     "두 순환소수를 분수로 바꿔 더하고, 소수 자리끼리 더한 결과와 비교한다.",
     LAB_RSUM),
    ("m2_system_check_lab.html",
     "연립방정식 실험실 — 한 식만 맞으면 해일까?",
     "연립방정식 실험실 — 한 식만 맞으면 해일까?",
     "여러 점을 두 식에 각각 대입해 보고, 연립방정식의 해가 무엇인지 확인한다.",
     LAB_SYSCHK),
    ("m2_inequality_solution_lab.html",
     "부등식 해 실험실 — 경계는 같은데 방향은 왜 다를까?",
     "부등식 해 실험실 — 경계는 같은데 방향은 왜 다를까?",
     "−10부터 10까지 하나씩 대입해 만족하는 수를 찾고, a의 부호와 해의 방향을 대조한다.",
     LAB_INEQSOL),
    ("m2_quadrant_lab.html",
     "사분면 실험실 — 어느 사분면을 지나지 않을까?",
     "사분면 실험실 — 어느 사분면을 지나지 않을까?",
     "기울기와 y절편의 부호를 바꿔 가며 직선이 지나는 사분면을 기록한다.",
     LAB_QUAD),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c35_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
