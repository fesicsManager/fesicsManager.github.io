# -*- coding: utf-8 -*-
"""중2 ① 수와 연산 2종 + ② 식의 계산·부등식·연립 4종"""
import os, re

OUT = "/mnt/user-data/outputs"
src = open("/home/claude/gen_math_labs.py", encoding="utf-8").read()
TPL = re.search(r'TPL = r"""(.*?)"""\n', src, re.S).group(1)

BASE = r"""
function lbl(ctx,t,x,y,c,sz,al){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
function box(ctx,x,y,w,h){ctx.fillStyle='#f1f6fd';ctx.fillRect(x,y,w,h);ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(x,y,w,h);}
function r1(v){return Math.round(v*10)/10;}
function r2(v){return Math.round(v*100)/100;}
function gcd(x,y){x=Math.abs(x);y=Math.abs(y);while(y){var t=x%y;x=y;y=t;}return x;}
function pn(v){return (v<0)?('('+v+')'):(''+v);}
"""

# ============================================================
# 1. 유한소수가 되는 조건
# ============================================================
LAB_FINITE = BASE + r"""
function expand(a,b){
  var ip=Math.floor(a/b), r=a%b, seen={}, digs=[], pos=0, start=-1;
  while(r!==0 && pos<30){
    if(seen[r]!==undefined){ start=seen[r]; break; }
    seen[r]=pos;
    r*=10;
    digs.push(Math.floor(r/b));
    r=r%b;
    pos++;
  }
  return {ip:ip,digs:digs,start:start,finite:(start<0)};
}
function primesOf(n){
  var f=[],p=2,m=n;
  while(p*p<=m){ if(m%p===0){ f.push(p); while(m%p===0) m/=p; } p++; }
  if(m>1) f.push(m);
  return f;
}
function decStr(e){
  var s=e.ip+'.',i;
  if(e.digs.length===0) return e.ip+'';
  for(i=0;i<e.digs.length;i++){
    if(e.start>=0&&i===e.start) s+='[';
    s+=e.digs[i];
  }
  if(e.start>=0) s+=']';
  return s;
}
var LAB = {
  cw:440, ch:400, cvTitle:'소수 전개판',
  action:'나눗셈으로 소수 만들기',
  hint0:'분자와 분모를 정하고, 실제로 나누어 소수로 나타내 보자.',
  sliders:[
    {id:'a',label:'분자',min:1,max:20,value:3,color:'#2563eb',unit:''},
    {id:'b',label:'분모',min:2,max:40,value:8,color:'#16a34a',unit:''}
  ],
  info:function(S){
    var g=gcd(S.a,S.b), rb=S.b/g, ra=S.a/g;
    var pf=primesOf(rb);
    var only25=true,i;
    for(i=0;i<pf.length;i++){ if(pf[i]!==2&&pf[i]!==5) only25=false; }
    return {ra:ra,rb:rb,pf:pf,only25:only25,e:expand(S.a,S.b)};
  },
  readout:function(S,ran){
    var x=this.info(S);
    return [{k:'기약분수',v:x.ra+'/'+x.rb},
            {k:'소수',v:ran?decStr(x.e):'나눠 보자'}];
  },
  doneMsg:function(S){
    var x=this.info(S);
    return S.a+'/'+S.b+' = '+decStr(x.e)+'.  기약분모 '+x.rb+'의 소인수는 '+(x.pf.join(', ')||'없음')
      +'이고 '+(x.e.finite?'유한소수':'순환소수')+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var x=this.info(S), i;
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*Math.max(1,x.e.digs.length));
    lbl(ctx,S.a+' ÷ '+S.b+' 를 끝까지 나누면?',24,38,'#1d4ed8',19);
    lbl(ctx,'기약분수 : '+x.ra+' / '+x.rb,24,72,'#334155',18);
    lbl(ctx,'분모 '+x.rb+'의 소인수 : '+(x.pf.join(' × ')||'없음'),24,100,'#15803d',18);
    var s=''+x.e.ip+'.';
    ctx.font='bold 24px sans-serif';ctx.textAlign='left';
    var px=40, py=170;
    ctx.fillStyle='#1f2937';ctx.fillText(s,px,py);
    px+=ctx.measureText(s).width;
    for(i=0;i<x.e.digs.length && i<shown;i++){
      var rep=(x.e.start>=0&&i>=x.e.start);
      ctx.fillStyle=rep?'#dc2626':'#1f2937';
      var ch=''+x.e.digs[i];
      ctx.fillText(ch,px,py);
      if(rep){
        ctx.strokeStyle='#dc2626';ctx.lineWidth=2;
        ctx.beginPath();ctx.moveTo(px,py-24);ctx.lineTo(px+ctx.measureText(ch).width,py-24);ctx.stroke();
      }
      px+=ctx.measureText(ch).width;
      if(px>390){ break; }
    }
    if(x.e.start>=0&&shown>=x.e.digs.length){ ctx.fillStyle='#dc2626';ctx.fillText(' ...',px,py); }
    ctx.font='bold 18px sans-serif';
    lbl(ctx,'빨간 부분 = 되풀이되는 자리(순환마디)',40,204,'#94a3b8',15);
    box(ctx,20,230,400,150);
    lbl(ctx,(t===null)?'유한소수일까, 순환소수일까?':(x.e.finite?'유한소수':'순환소수 (순환마디 '+(x.e.digs.length-x.e.start)+'자리)'),
        38,262,x.e.finite?'#15803d':'#b91c1c',21);
    lbl(ctx,'분모의 소인수가 2와 5뿐인가 : '+(x.only25?'예':'아니오'),38,296,'#334155',18);
    lbl(ctx,'분모가 짝수인가 : '+((x.rb%2===0)?'예':'아니오'),38,326,'#52627a',18);
    lbl(ctx,(t===null)?'':(x.e.finite===x.only25?'두 판단이 일치':'두 판단이 어긋남'),38,358,'#334155',17);
  },
  record:function(S){
    var x=this.info(S);
    return {a:S.a,b:S.b,ra:x.ra,rb:x.rb,pf:(x.pf.join(', ')||'없음'),
            only25:x.only25,finite:x.e.finite,
            even:(x.rb%2===0),
            cyc:x.e.finite?0:(x.e.digs.length-x.e.start),
            dec:decStr(x.e)};
  },
  headA:['번호','분수','기약분수','기약분모의 소인수','2와 5뿐?','유한소수?','분모가 짝수?','순환마디'],
  rowA:function(r,i){
    return [i+1,r.a+'/'+r.b,r.ra+'/'+r.rb,r.pf,
            '<span class="'+(r.only25?'ok':'no')+'">'+(r.only25?'○':'×')+'</span>',
            '<span class="'+(r.finite?'ok':'no')+'">'+(r.finite?'○':'×')+'</span>',
            r.even?'○':'×',
            r.finite?'-':(r.cyc+'자리')];
  },
  analyze:function(rec){
    var rows=[],match=0,evenMatch=0,fin=0,inf=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var m=(r.only25===r.finite), em=(r.even===r.finite);
      if(m) match++;
      if(em) evenMatch++;
      if(r.finite) fin++; else inf++;
      rows.push([r.a+'/'+r.b, r.ra+'/'+r.rb, r.pf,
                 '<span class="'+(r.only25?'ok':'no')+'">'+(r.only25?'○':'×')+'</span>',
                 '<span class="'+(r.finite?'ok':'no')+'">'+(r.finite?'○':'×')+'</span>',
                 '<span class="'+(m?'ok':'no')+'">'+(m?'○':'×')+'</span>',
                 '<span class="'+(em?'ok':'no')+'">'+(em?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'“소인수가 2와 5뿐” 판정이 맞은 횟수',big:match+' / '+rec.length,
       p:'실제 나눗셈 결과와 일치했는지 확인했다.'},
      {t:'“분모가 짝수면 유한소수” 판정이 맞은 횟수',big:evenMatch+' / '+rec.length,
       p:'짝수 여부만으로 판단하면 어떻게 되는지 확인했다.'},
      {t:'유한소수 / 순환소수',big:fin+' / '+inf,
       p:(fin&&inf)?'두 경우를 모두 기록했다.':'두 경우를 모두 기록해야 비교할 수 있다.'}
    ];
    var concl;
    if(fin===0||inf===0){
      concl='<b>더 해 보자</b> — 유한소수가 되는 분수와 순환소수가 되는 분수를 <b>모두</b> 기록해야 조건을 확인할 수 있다.';
    } else if(match===rec.length && evenMatch<rec.length){
      concl='<b>정리</b> — <b>기약분수의 분모를 소인수분해했을 때 2와 5만 남으면 유한소수</b>였고, 다른 소인수가 하나라도 있으면 순환소수였다. '
           +'예외는 없었다. 반면 “분모가 짝수면 유한소수”는 '+(rec.length-evenMatch)+'번 틀렸다. 6이나 14처럼 짝수여도 3이나 7이 섞이면 순환한다. '
           +'또 반드시 <b>기약분수로 만든 뒤</b> 분모를 봐야 한다.';
    } else if(match===rec.length){
      concl='<b>정리</b> — 소인수가 2와 5뿐인지로 판정한 결과가 모두 맞았다. 분모가 6이나 14인 경우도 넣어 짝수 판정과 비교해 보자.';
    } else {
      concl='<b>확인 필요</b> — 판정과 실제 결과가 어긋난 기록이 있다.';
    }
    return {head:['분수','기약분수','소인수','2와 5뿐?','유한소수?','일치?','짝수 판정 일치?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 순환소수를 분수로
# ============================================================
LAB_REPEAT = BASE + r"""
function pad(v,n){ var s=''+v; while(s.length<n) s='0'+s; return s; }
var LAB = {
  cw:440, ch:400, cvTitle:'순환소수 변환판',
  action:'식을 세워 분수로 바꾸기',
  hint0:'순환하지 않는 부분과 순환마디를 정해 보자.',
  sliders:[
    {id:'m',label:'순환하지 않는 자릿수',min:0,max:2,value:0,color:'#2563eb',unit:'자리'},
    {id:'p',label:'순환하지 않는 숫자',min:0,max:99,value:0,color:'#60a5fa',unit:''},
    {id:'r',label:'순환마디',min:1,max:99,value:9,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var pre=(S.m===0)?'':pad(S.p%Math.pow(10,S.m),S.m);
    var rep=''+S.r;
    var L=rep.length;
    var big=parseInt((pre+rep),10);
    var small=(pre==='')?0:parseInt(pre,10);
    var num=big-small;
    var den=Math.pow(10,S.m+L)-Math.pow(10,S.m);
    var g=gcd(num,den)||1;
    var val=num/den;
    return {pre:pre,rep:rep,L:L,num:num,den:den,sn:num/g,sd:den/g,val:val,
            disp:'0.'+pre+rep+rep+rep+'...'};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'순환소수',v:c.disp},
            {k:'분수',v:ran?(c.sn+'/'+c.sd+((c.sd===1)?(' = '+c.sn):'')):'바꿔 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.sd===1) return c.disp+' = '+c.sn+'.  분수로 바꾸니 정수가 되었다! 기록해 보자.';
    return c.disp+' = '+c.sn+'/'+c.sd+'.  다시 나눠 보면 같은 순환소수가 나온다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var p1=(t===null)?0:Math.min(1,t/0.4);
    var p2=(t===null)?0:Math.max(0,Math.min(1,(t-0.4)/0.3));
    var p3=(t===null)?0:Math.max(0,(t-0.7)/0.3);
    lbl(ctx,'순환소수를 분수로',24,38,'#1d4ed8',19);
    lbl(ctx,'x = '+c.disp,40,84,'#1f2937',24);
    if(p1>0){
      ctx.globalAlpha=p1;
      lbl(ctx,Math.pow(10,S.m+c.L)+'x = '+((c.pre+c.rep)+'.'+c.rep+c.rep+'...'),40,126,'#334155',20);
      ctx.globalAlpha=1;
    }
    if(p2>0){
      ctx.globalAlpha=p2;
      lbl(ctx,(S.m===0?'':(Math.pow(10,S.m)+'x = '+(c.pre===''?'0':c.pre)+'.'+c.rep+c.rep+'...')),40,164,'#334155',20);
      ctx.globalAlpha=1;
    }
    if(p3>0){
      ctx.globalAlpha=p3;
      ctx.strokeStyle='#94a3b8';ctx.lineWidth=1.6;
      ctx.beginPath();ctx.moveTo(40,182);ctx.lineTo(400,182);ctx.stroke();
      lbl(ctx,'빼면  '+c.den+'x = '+c.num,40,214,'#b91c1c',22);
      lbl(ctx,'x = '+c.num+'/'+c.den+((c.sd!==c.den)?('  =  '+c.sn+'/'+c.sd):''),40,254,'#15803d',24);
      ctx.globalAlpha=1;
    }
    box(ctx,20,272,400,112);
    lbl(ctx,(t===null)?'되풀이되는 부분을 어떻게 없앨까?':('분수 : '+c.sn+'/'+c.sd),38,304,'#1f2937',21);
    lbl(ctx,(t===null)?'':('소수로 다시 계산 : '+(c.sn/c.sd).toFixed(6)),38,336,'#52627a',18);
    lbl(ctx,(t===null)?'':((c.sd===1)?('정수 '+c.sn+'과 같다'):'원래 순환소수와 같은 값'),38,368,(c.sd===1)?'#b45309':'#15803d',18);
  },
  record:function(S){
    var c=this.calc(S);
    var back=c.sn/c.sd;
    var approx=parseFloat('0.'+c.pre+c.rep+c.rep+c.rep+c.rep+c.rep+c.rep);
    return {disp:c.disp,m:S.m,rep:c.rep,num:c.num,den:c.den,sn:c.sn,sd:c.sd,
            val:Math.round(back*1000000)/1000000,
            ok:(Math.abs(back-approx)<1e-5),
            integer:(c.sd===1),
            nine:(c.pre===''&&/^9+$/.test(c.rep))};
  },
  headA:['번호','순환소수','분모 만들기','분수','기약분수','다시 소수로','일치?','정수?'],
  rowA:function(r,i){
    return [i+1,r.disp,r.num+'/'+r.den,r.num+'/'+r.den,'<b>'+r.sn+'/'+r.sd+'</b>',r.val,
            '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
            r.integer?'○':'×'];
  },
  analyze:function(rec){
    var rows=[],ok=0,ints=0,nines=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.ok) ok++;
      if(r.integer) ints++;
      if(r.nine) nines++;
      rows.push([r.disp, r.num+'/'+r.den, '<b>'+r.sn+'/'+r.sd+'</b>', r.val,
                 '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
                 r.integer?'정수':'-']);
    }
    var stats=[
      {t:'분수를 다시 나눴을 때 원래 값과 일치',big:ok+' / '+rec.length,
       p:'변환이 제대로 되었는지 되돌려 확인한 결과.'},
      {t:'분수가 정수가 된 기록',big:ints+'개',
       p:ints?'0.999...처럼 순환마디가 9뿐이면 정수가 된다.':'순환마디를 9로 두고 해 보자.'},
      {t:'순환마디가 9뿐이었던 기록',big:nines+'개',
       p:nines?'9/9 = 1 처럼 딱 떨어졌다.':'0.999...도 시험해 보자.'}
    ];
    var concl;
    if(ok===rec.length && nines>0){
      concl='<b>정리</b> — 10을 곱해 순환 부분을 겹치게 만든 뒤 빼면 되풀이되는 꼬리가 사라져 분수가 되었고, '
           +'되돌려 나눠 보면 언제나 원래 순환소수가 나왔다. 특히 <b>0.999… = 9/9 = 1</b>이었다. '
           +'0.999…는 1에 “가까운 수”가 아니라 1을 다르게 쓴 것이다. 모든 순환소수는 분수로 쓸 수 있으므로 유리수다.';
    } else if(ok===rec.length){
      concl='<b>정리</b> — 순환소수는 모두 분수로 바뀌었고 되돌려도 값이 같았다. 순환마디를 9로 두면 어떻게 되는지도 확인해 보자.';
    } else {
      concl='<b>확인 필요</b> — 되돌린 값이 다른 기록이 있다.';
    }
    return {head:['순환소수','식','기약분수','소수로 되돌림','일치?','정수?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 지수법칙
# ============================================================
LAB_EXP = BASE + r"""
var OPS=['a^m × a^n','(a^m)^n','a^m ÷ a^n'];
function powLoop(a,k){ var v=1,i; for(i=0;i<k;i++){ v*=a; } return v; }
var LAB = {
  cw:440, ch:400, cvTitle:'지수 풀어쓰기판',
  action:'풀어 써서 세어 보기',
  hint0:'밑과 두 지수, 계산 종류를 정해 보자.',
  sliders:[
    {id:'op',label:'계산',min:0,max:2,value:0,color:'#2563eb',fmt:function(v){return OPS[v];}},
    {id:'a',label:'밑 a',min:2,max:5,value:2,color:'#16a34a',unit:''},
    {id:'m',label:'지수 m',min:1,max:6,value:3,color:'#f59e0b',unit:''},
    {id:'n',label:'지수 n',min:1,max:6,value:2,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var a=S.a,m=S.m,n=S.n,real,rule,wrong,rk,wk;
    if(S.op===0){ real=powLoop(a,m)*powLoop(a,n); rk=m+n; wk=m*n; }
    else if(S.op===1){ real=powLoop(powLoop(a,m),n); rk=m*n; wk=m+n; }
    else { real=powLoop(a,m)/powLoop(a,n); rk=m-n; wk=(n===0)?m:m/n; }
    rule=Math.pow(a,rk); wrong=Math.pow(a,wk);
    return {real:real,rule:rule,wrong:wrong,rk:rk,wk:wk};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'식',v:(S.op===0)?(S.a+'^'+S.m+' × '+S.a+'^'+S.n):((S.op===1)?('('+S.a+'^'+S.m+')^'+S.n):(S.a+'^'+S.m+' ÷ '+S.a+'^'+S.n))},
            {k:'직접 계산한 값',v:ran?r2(c.real):'세어 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '직접 계산하면 '+r2(c.real)+'이고, 지수를 '+((S.op===0)?'더한':((S.op===1)?'곱한':'뺀'))+' 규칙으로는 '+S.a+'^'+c.rk+' = '+r2(c.rule)+'이다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var show=(t===null)?0:Math.min(1,t);
    var eq=(S.op===0)?(S.a+'^'+S.m+' × '+S.a+'^'+S.n):((S.op===1)?('('+S.a+'^'+S.m+')^'+S.n):(S.a+'^'+S.m+' ÷ '+S.a+'^'+S.n));
    lbl(ctx,eq,40,74,'#1d4ed8',26);
    lbl(ctx,'a를 몇 번 곱했는지 직접 세어 보자',24,38,'#52627a',17);
    if(show>0){
      var parts=[],s1='',s2='';
      for(i=0;i<S.m;i++) s1+=(i?'×':'')+S.a;
      for(i=0;i<S.n;i++) s2+=(i?'×':'')+S.a;
      var line;
      if(S.op===0) line='('+s1+') × ('+s2+')';
      else if(S.op===1) line='('+s1+') 를 '+S.n+'번 곱하기';
      else line='('+s1+') ÷ ('+s2+')';
      ctx.globalAlpha=show;
      lbl(ctx,line,40,120,'#334155',(line.length>34)?13:16);
      lbl(ctx,'→ a를 모두 '+c.rk+'번 곱한 것',40,156,'#15803d',19);
      lbl(ctx,'= '+S.a+'^'+c.rk+' = '+r2(c.rule),40,192,'#15803d',22);
      ctx.globalAlpha=1;
    }
    box(ctx,20,222,400,162);
    lbl(ctx,(t===null)?'지수는 어떻게 될까?':('직접 계산 : '+r2(c.real)),38,254,'#1f2937',21);
    lbl(ctx,(t===null)?'':('지수 규칙 : '+S.a+'^'+c.rk+' = '+r2(c.rule)),38,288,'#15803d',19);
    lbl(ctx,(t===null)?'':('다른 방법 : '+S.a+'^'+r2(c.wk)+' = '+r2(c.wrong)),38,320,'#b91c1c',19);
    lbl(ctx,(t===null)?'':((Math.abs(c.real-c.rule)<1e-9)?'직접 계산과 지수 규칙이 일치':'어긋남'),38,354,'#334155',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {op:S.op,name:OPS[S.op],a:S.a,m:S.m,n:S.n,
            real:r2(c.real),rule:r2(c.rule),wrong:r2(c.wrong),rk:c.rk,wk:r2(c.wk),
            ok:(Math.abs(c.real-c.rule)<1e-9),
            wok:(Math.abs(c.real-c.wrong)<1e-9)};
  },
  headA:['번호','계산','식','직접 계산','지수 규칙','맞나?','다른 방법','맞나?'],
  rowA:function(r,i){
    var eq=(r.op===0)?(r.a+'^'+r.m+'×'+r.a+'^'+r.n):((r.op===1)?('('+r.a+'^'+r.m+')^'+r.n):(r.a+'^'+r.m+'÷'+r.a+'^'+r.n));
    return [i+1,r.name,eq,'<b>'+r.real+'</b>',r.a+'^'+r.rk+'='+r.rule,
            '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
            r.a+'^'+r.wk+'='+r.wrong,
            '<span class="'+(r.wok?'ok':'no')+'">'+(r.wok?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ok=0,wok=0,ops={},on=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.ok) ok++;
      if(r.wok) wok++;
      ops[r.op]=true;
      var eq=(r.op===0)?(r.a+'^'+r.m+'×'+r.a+'^'+r.n):((r.op===1)?('('+r.a+'^'+r.m+')^'+r.n):(r.a+'^'+r.m+'÷'+r.a+'^'+r.n));
      rows.push([r.name, eq, '<b>'+r.real+'</b>', r.a+'^'+r.rk,
                 '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
                 r.a+'^'+r.wk,
                 '<span class="'+(r.wok?'ok':'no')+'">'+(r.wok?'○':'×')+'</span>']);
    }
    for(var k in ops) on++;
    var stats=[
      {t:'지수 규칙이 맞은 횟수',big:ok+' / '+rec.length,
       p:'풀어 써서 직접 계산한 값과 일치했는지 확인한 결과.'},
      {t:'지수를 바꿔치기한 방법이 맞은 횟수',big:wok+' / '+rec.length,
       p:'곱셈에서 지수를 곱하거나, 거듭제곱에서 지수를 더하면 어떻게 되는지 확인했다.'},
      {t:'시험한 계산 종류',big:on+'가지',p:on>2?'세 가지를 모두 확인했다.':'세 가지 계산을 모두 기록해 보자.'}
    ];
    var concl;
    if(on<3){
      concl='<b>더 해 보자</b> — 곱셈·거듭제곱·나눗셈 <b>세 가지를 모두</b> 기록해야 규칙을 구별할 수 있다.';
    } else if(ok===rec.length){
      concl='<b>정리</b> — 풀어 써서 a를 몇 번 곱했는지 세어 보면 규칙이 그대로 나왔다. '
           +'<b>곱하면 지수를 더하고, 거듭제곱하면 지수를 곱하고, 나누면 지수를 뺀다.</b> '
           +'외운 규칙이 아니라 “몇 번 곱했는가”를 센 결과다. 지수를 바꿔 쓴 방법은 '+(rec.length-wok)+'번 틀렸다.';
    } else {
      concl='<b>확인 필요</b> — 직접 계산과 규칙이 어긋난 기록이 있다.';
    }
    return {head:['계산','식','직접 계산','지수 규칙','맞나?','다른 방법','맞나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 부등식과 음수
# ============================================================
LAB_INEQ = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'부등식 수직선판',
  action:'양변에 곱해 보기',
  hint0:'두 수와 곱할 수를 정하고, 대소 관계가 어떻게 되는지 보자.',
  sliders:[
    {id:'a',label:'왼쪽 수',min:-10,max:10,value:-3,color:'#2563eb',unit:''},
    {id:'b',label:'오른쪽 수',min:-10,max:10,value:5,color:'#dc2626',unit:''},
    {id:'k',label:'양변에 곱할 수',min:-9,max:9,value:-2,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var A=S.a*S.k, B=S.b*S.k;
    var before=(S.a<S.b)?'<':((S.a>S.b)?'>':'=');
    var after=(A<B)?'<':((A>B)?'>':'=');
    return {A:A,B:B,before:before,after:after,keep:(before===after)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'처음',v:S.a+' '+c.before+' '+S.b},
            {k:'곱한 뒤',v:ran?(c.A+' '+c.after+' '+c.B):'곱해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '양변에 '+S.k+'를 곱하니 '+c.A+' '+c.after+' '+c.B+'.  부등호가 '+(c.keep?'그대로다':'바뀌었다')+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var X0=30, X1=410, LO=-90, HI=90;
    function px(v){ return X0+(X1-X0)*(v-LO)/(HI-LO); }
    var mv=(t===null)?0:Math.min(1,t);
    function line(Y,label){
      ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
      ctx.beginPath();ctx.moveTo(X0,Y);ctx.lineTo(X1,Y);ctx.stroke();
      for(i=LO;i<=HI;i+=10){
        var x=px(i), big=(i%30===0);
        ctx.beginPath();ctx.moveTo(x,Y-(big?8:4));ctx.lineTo(x,Y+(big?8:4));
        ctx.strokeStyle=big?'#64748b':'#cbd5e1';ctx.lineWidth=big?1.8:1;ctx.stroke();
        if(big){ ctx.fillStyle='#94a3b8';ctx.font='11px sans-serif';ctx.textAlign='center';ctx.fillText(i,x,Y+22); }
      }
      ctx.textAlign='left';
      lbl(ctx,label,X0,Y-30,'#52627a',15);
    }
    line(120,'처음');
    line(250,'양변에 '+S.k+'를 곱한 뒤');
    function dot(Y,v,col,label){
      ctx.beginPath();ctx.arc(px(v),Y,9,0,Math.PI*2);
      ctx.fillStyle=col;ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      lbl(ctx,label,px(v),Y-14,col,14,'center');
    }
    dot(120,S.a,'#2563eb',''+S.a);
    dot(120,S.b,'#dc2626',''+S.b);
    var ca=S.a+(c.A-S.a)*mv, cb=S.b+(c.B-S.b)*mv;
    if(mv>0){
      dot(250,ca,'#2563eb',''+r1(ca));
      dot(250,cb,'#dc2626',''+r1(cb));
    }
    lbl(ctx,'부등호의 방향은 어떻게 될까?',24,36,'#1d4ed8',19);
    box(ctx,20,296,400,88);
    lbl(ctx,S.a+' '+c.before+' '+S.b,38,330,'#1f2937',22);
    lbl(ctx,(t===null)?'양변에 곱하면?':(c.A+' '+c.after+' '+c.B+'    →  부등호 '+(c.keep?'유지':'뒤집힘')),
        38,366,c.keep?'#15803d':'#b91c1c',21);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,k:S.k,A:c.A,B:c.B,before:c.before,after:c.after,keep:c.keep,
            pos:(S.k>0),zero:(S.k===0)};
  },
  headA:['번호','처음','곱할 수','곱한 뒤','처음 부등호','나중 부등호','유지?'],
  rowA:function(r,i){
    return [i+1,r.a+' '+r.before+' '+r.b,r.k,r.A+' '+r.after+' '+r.B,r.before,'<b>'+r.after+'</b>',
            '<span class="'+(r.keep?'ok':'no')+'">'+(r.keep?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],pos=0,posKeep=0,neg=0,negKeep=0,zero=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.zero) zero++;
      else if(r.pos){ pos++; if(r.keep) posKeep++; }
      else { neg++; if(r.keep) negKeep++; }
      rows.push([r.a+' '+r.before+' '+r.b, r.k, r.A+' '+r.after+' '+r.B,
                 r.zero?'0':(r.pos?'양수':'음수'),
                 '<span class="'+(r.keep?'ok':'no')+'">'+(r.keep?'유지':'뒤집힘')+'</span>']);
    }
    var stats=[
      {t:'양수를 곱했을 때 유지',big:pos?(posKeep+' / '+pos):'기록 없음',
       p:pos?'양수를 곱한 기록만 셈.':'양수를 곱한 경우도 기록해 보자.'},
      {t:'음수를 곱했을 때 유지',big:neg?(negKeep+' / '+neg):'기록 없음',
       p:neg?'음수를 곱한 기록 중 부등호가 그대로였던 수.':'음수를 곱한 경우도 기록해 보자.'},
      {t:'0을 곱한 기록',big:zero+'개',
       p:zero?'0을 곱하면 양변이 모두 0이 되어 등호가 된다.':''}
    ];
    var concl;
    if(pos===0||neg===0){
      concl='<b>더 해 보자</b> — 양수를 곱한 경우와 음수를 곱한 경우를 <b>모두</b> 기록해야 규칙이 보인다.';
    } else if(posKeep===pos && negKeep===0){
      concl='<b>정리</b> — 양수를 곱하면 '+pos+'번 모두 부등호가 그대로였지만, 음수를 곱하면 '+neg+'번 모두 <b>뒤집혔다.</b> '
           +'수직선에서 음수를 곱하는 것은 0을 기준으로 좌우를 뒤집는 일이라서 순서가 반대가 된다. '
           +'부등식을 풀 때 음수로 나누거나 곱하면 반드시 부등호 방향을 바꿔야 한다.';
    } else {
      concl='<b>확인 필요</b> — 규칙과 어긋난 기록이 있다.';
    }
    return {head:['처음','곱할 수','곱한 뒤','곱한 수','부등호'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 연립방정식 해의 개수
# ============================================================
LAB_SYS = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'두 직선 판',
  action:'두 직선 그리기',
  hint0:'두 번째 식의 계수를 정해 보자. 첫 번째 식은 2x + y = 4로 고정이다.',
  sliders:[
    {id:'a2',label:'두 번째 식의 x 계수',min:-6,max:6,value:4,color:'#dc2626',unit:''},
    {id:'b2',label:'두 번째 식의 y 계수',min:-6,max:6,value:2,color:'#f87171',unit:''},
    {id:'c2',label:'두 번째 식의 상수',min:-12,max:12,value:8,color:'#fca5a5',unit:''}
  ],
  calc:function(S){
    var a1=2,b1=1,c1=4;
    var det=a1*S.b2-S.a2*b1;
    var prop=(S.a2*c1===S.c2*a1)&&(S.b2*c1===S.c2*b1);
    var kind, x=0, y=0;
    if(det!==0){ kind='해 1개'; x=(c1*S.b2-S.c2*b1)/det; y=(a1*S.c2-S.a2*c1)/det; }
    else if(S.a2===0&&S.b2===0){ kind=(S.c2===0)?'해가 무수히 많음':'해가 없음'; }
    else if(prop){ kind='해가 무수히 많음'; }
    else { kind='해가 없음'; }
    return {det:det,kind:kind,x:x,y:y,prop:prop};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'두 번째 식',v:S.a2+'x + '+S.b2+'y = '+S.c2},
            {k:'해',v:ran?c.kind:'그려 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.kind==='해 1개') return '두 직선이 한 점 ('+r2(c.x)+', '+r2(c.y)+')에서 만난다. 해가 1개다. 기록해 보자.';
    if(c.kind==='해가 없음') return '두 직선이 평행해서 만나지 않는다. 해가 없다. 기록해 보자.';
    return '두 직선이 완전히 겹친다. 해가 무수히 많다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var CX=220, CY=200, U=24;
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=-8;i<=8;i++){
      ctx.beginPath();ctx.moveTo(CX+i*U,CY-6*U);ctx.lineTo(CX+i*U,CY+6*U);ctx.stroke();
      if(i>=-6&&i<=6){ ctx.beginPath();ctx.moveTo(CX-8*U,CY+i*U);ctx.lineTo(CX+8*U,CY+i*U);ctx.stroke(); }
    }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(CX-8*U,CY);ctx.lineTo(CX+8*U,CY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(CX,CY-6*U);ctx.lineTo(CX,CY+6*U);ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    function drawLine(a,b,cc,col,w){
      if(a===0&&b===0) return;
      ctx.strokeStyle=col;ctx.lineWidth=w;ctx.beginPath();
      var started=false;
      for(i=-80;i<=80;i++){
        var xx=i/10, yy;
        if(b!==0){ yy=(cc-a*xx)/b; }
        else { xx=cc/a; yy=(i/10)*1; }
        var Px=CX+xx*U, Py=CY-yy*U;
        if(Py<CY-6*U||Py>CY+6*U){ started=false; continue; }
        if(!started){ ctx.moveTo(Px,Py); started=true; } else ctx.lineTo(Px,Py);
      }
      ctx.stroke();
    }
    drawLine(2,1,4,'#2563eb',3);
    if(grow>0){
      ctx.globalAlpha=grow;
      drawLine(S.a2,S.b2,S.c2,'#dc2626',3);
      ctx.globalAlpha=1;
    }
    if(grow>=1&&c.kind==='해 1개'){
      ctx.beginPath();ctx.arc(CX+c.x*U,CY-c.y*U,8,0,Math.PI*2);
      ctx.fillStyle='#f59e0b';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
    }
    lbl(ctx,'2x + y = 4   와   '+S.a2+'x + '+S.b2+'y = '+S.c2,24,32,'#1d4ed8',17);
    box(ctx,20,346,400,66);
    lbl(ctx,(t===null)?'두 직선은 몇 번 만날까?':c.kind,38,378,
        (c.kind==='해 1개')?'#15803d':'#b91c1c',21);
    lbl(ctx,(t===null)?'':('계수 판정 : x·y 계수의 비 '+((c.det===0)?'같음':'다름')+', 상수까지 비례 '+(c.prop?'예':'아니오')),
        38,402,'#52627a',15);
  },
  record:function(S){
    var c=this.calc(S);
    return {a2:S.a2,b2:S.b2,c2:S.c2,det:c.det,kind:c.kind,prop:c.prop,
            x:r2(c.x),y:r2(c.y),one:(c.kind==='해 1개')};
  },
  headA:['번호','두 번째 식','계수비 같은가','상수까지 비례','해','교점'],
  rowA:function(r,i){
    return [i+1,r.a2+'x + '+r.b2+'y = '+r.c2,
            '<span class="'+((r.det===0)?'ok':'no')+'">'+((r.det===0)?'○':'×')+'</span>',
            '<span class="'+(r.prop?'ok':'no')+'">'+(r.prop?'○':'×')+'</span>',
            '<b>'+r.kind+'</b>',
            r.one?('('+r.x+', '+r.y+')'):'-'];
  },
  analyze:function(rec){
    var rows=[],one=0,none=0,inf=0,match=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var expect=(r.det!==0)?'해 1개':(r.prop?'해가 무수히 많음':'해가 없음');
      var m=(expect===r.kind);
      if(m) match++;
      if(r.kind==='해 1개') one++;
      else if(r.kind==='해가 없음') none++;
      else inf++;
      rows.push([r.a2+'x + '+r.b2+'y = '+r.c2,
                 (r.det===0)?'같음':'다름', r.prop?'예':'아니오', '<b>'+r.kind+'</b>',
                 '<span class="'+(m?'ok':'no')+'">'+(m?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'계수 판정과 그래프 결과가 일치',big:match+' / '+rec.length,
       p:'계수만 보고 한 판정이 실제 그래프와 맞았는지 확인한 결과.'},
      {t:'해가 1개 / 없음 / 무수히',big:one+' / '+none+' / '+inf,
       p:(one&&none&&inf)?'세 경우를 모두 기록했다.':'세 경우를 모두 만들어 보자.'},
      {t:'전체 기록',big:rec.length+'개',p:'4x+2y=8은 겹치고, 4x+2y=9는 평행하다.'}
    ];
    var concl;
    if(!(one&&none&&inf)){
      concl='<b>더 해 보자</b> — 해가 1개인 경우, 없는 경우, 무수히 많은 경우를 <b>모두</b> 만들어 기록해 보자. '
           +'4x+2y=8과 4x+2y=9를 넣어 보면 두 경우가 나온다.';
    } else if(match===rec.length){
      concl='<b>정리</b> — 연립방정식의 해는 <b>두 직선이 만나는 점</b>이었다. '
           +'x·y 계수의 비가 다르면 한 점에서 만나 해가 1개, 계수비는 같은데 상수비가 다르면 평행해서 해가 없고, '
           +'상수까지 비례하면 같은 직선이라 해가 무수히 많았다. 계수만 봐도 그래프를 그리기 전에 알 수 있다.';
    } else {
      concl='<b>확인 필요</b> — 계수 판정과 그래프 결과가 어긋난 기록이 있다.';
    }
    return {head:['두 번째 식','계수비','상수까지 비례','해','판정 일치?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 6. 분배법칙
# ============================================================
LAB_DIST = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'분배법칙 확인판',
  action:'값을 넣어 확인하기',
  hint0:'k(ax + b) 꼴의 식과 x에 넣을 값을 정해 보자.',
  sliders:[
    {id:'k',label:'괄호 앞의 수 k',min:-5,max:5,value:-3,color:'#2563eb',unit:''},
    {id:'a',label:'x의 계수 a',min:1,max:5,value:2,color:'#16a34a',unit:''},
    {id:'b',label:'상수항 b',min:-5,max:5,value:4,color:'#f59e0b',unit:''},
    {id:'xv',label:'x에 넣을 값',min:-5,max:5,value:2,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var inside=S.a*S.xv+S.b;
    var real=S.k*inside;
    var expand=S.k*S.a*S.xv+S.k*S.b;
    var wrong=S.k*S.a*S.xv+S.b;
    return {inside:inside,real:real,expand:expand,wrong:wrong};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'식',v:S.k+'('+S.a+'x'+((S.b<0)?(' − '+(-S.b)):(' + '+S.b))+')'},
            {k:'x = '+S.xv+'일 때',v:ran?c.real:'확인해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '괄호를 먼저 계산하면 '+c.real+', 바르게 전개하면 '+c.expand+', 상수항을 그대로 두면 '+c.wrong+'이다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var p1=(t===null)?0:Math.min(1,t/0.5);
    var p2=(t===null)?0:Math.max(0,(t-0.5)/0.5);
    var bs=(S.b<0)?(' − '+(-S.b)):(' + '+S.b);
    lbl(ctx,'괄호 앞의 수는 어디까지 곱할까?',24,38,'#1d4ed8',19);
    lbl(ctx,S.k+'( '+S.a+'x'+bs+' )',40,90,'#1f2937',26);
    if(p1>0){
      ctx.globalAlpha=p1;
      ctx.strokeStyle='#dc2626';ctx.lineWidth=2.4;
      ctx.beginPath();ctx.moveTo(58,102);ctx.quadraticCurveTo(90,132,120,102);ctx.stroke();
      ctx.beginPath();ctx.moveTo(58,102);ctx.quadraticCurveTo(120,150,182,102);ctx.stroke();
      lbl(ctx,'두 항 모두에 곱한다',40,168,'#b91c1c',17);
      lbl(ctx,'= '+(S.k*S.a)+'x'+((S.k*S.b<0)?(' − '+(-S.k*S.b)):(' + '+(S.k*S.b))),40,206,'#15803d',24);
      ctx.globalAlpha=1;
    }
    if(p2>0){
      ctx.globalAlpha=p2;
      lbl(ctx,'x = '+S.xv+' 를 넣어 확인',40,244,'#52627a',17);
      ctx.globalAlpha=1;
    }
    box(ctx,20,258,400,126);
    lbl(ctx,(t===null)?'값을 넣어 비교해 보자':('괄호 먼저 : '+S.k+' × '+c.inside+' = '+c.real),38,290,'#1f2937',19);
    lbl(ctx,(t===null)?'':('바르게 전개 : '+c.expand),38,322,'#15803d',19);
    lbl(ctx,(t===null)?'':('상수항을 그대로 두면 : '+c.wrong),38,354,'#b91c1c',19);
  },
  record:function(S){
    var c=this.calc(S);
    return {k:S.k,a:S.a,b:S.b,xv:S.xv,real:c.real,expand:c.expand,wrong:c.wrong,
            ok:(c.real===c.expand),wok:(c.real===c.wrong),
            trivial:(S.k===1||S.b===0)};
  },
  headA:['번호','식','x','괄호 먼저','바른 전개','같나?','상수항 그대로','같나?'],
  rowA:function(r,i){
    var bs=(r.b<0)?(' − '+(-r.b)):(' + '+r.b);
    return [i+1,r.k+'('+r.a+'x'+bs+')',r.xv,'<b>'+r.real+'</b>',r.expand,
            '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
            r.wrong,
            '<span class="'+(r.wok?'ok':'no')+'">'+(r.wok?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ok=0,wok=0,tv=0,wokNT=0,nt=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.ok) ok++;
      if(r.wok) wok++;
      if(r.trivial) tv++;
      else { nt++; if(r.wok) wokNT++; }
      var bs=(r.b<0)?(' − '+(-r.b)):(' + '+r.b);
      rows.push([r.k+'('+r.a+'x'+bs+')', 'x = '+r.xv, '<b>'+r.real+'</b>', r.expand,
                 '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
                 r.wrong,
                 '<span class="'+(r.wok?'ok':'no')+'">'+(r.wok?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'바르게 전개한 값이 맞은 횟수',big:ok+' / '+rec.length,
       p:'괄호를 먼저 계산한 값과 일치했는지 확인한 결과.'},
      {t:'상수항을 그대로 둔 값이 맞은 횟수',big:wok+' / '+rec.length,
       p:'k를 x항에만 곱했을 때의 결과.'},
      {t:'k가 1이거나 b가 0이 아닌 기록',big:nt+'개',
       p:nt?('그중 상수항을 그대로 둔 값이 맞은 것 '+wokNT+'개.'):'k와 b를 둘 다 0이나 1이 아닌 값으로 해 보자.'}
    ];
    var concl;
    if(nt===0){
      concl='<b>더 해 보자</b> — k를 1이 아닌 수로, b를 0이 아닌 수로 두고 기록해야 차이가 드러난다.';
    } else if(ok===rec.length && wokNT===0){
      concl='<b>정리</b> — 괄호를 먼저 계산한 값과 <b>두 항 모두에 곱한 전개</b>는 언제나 같았지만, '
           +'상수항을 그대로 둔 계산은 '+nt+'번 모두 틀렸다. 괄호 앞의 수는 <b>괄호 안의 모든 항</b>에 곱해진다. '
           +'특히 앞의 수가 음수일 때 상수항의 부호까지 바뀐다는 점을 놓치기 쉽다.';
    } else {
      concl='<b>확인 필요</b> — 전개한 값이 괄호를 먼저 계산한 값과 다른 기록이 있다.';
    }
    return {head:['식','대입','괄호 먼저','바른 전개','같나?','상수항 그대로','같나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("m2_finite_decimal_lab.html",
     "유한소수 실험실 — 분모가 짝수면 유한소수일까?",
     "유한소수 실험실 — 분모가 짝수면 유한소수일까?",
     "분수를 실제로 나누어 소수로 펼치고, 기약분모의 소인수와 유한·순환 여부를 대조한다.",
     LAB_FINITE),
    ("m2_repeating_to_fraction_lab.html",
     "순환소수 실험실 — 0.999…는 1일까?",
     "순환소수 실험실 — 0.999…는 1일까?",
     "순환마디를 정해 순환소수를 분수로 바꾸고, 다시 나누어 원래 값과 같은지 확인한다.",
     LAB_REPEAT),
    ("m2_exponent_rules_lab.html",
     "지수법칙 실험실 — 곱하면 지수도 곱할까?",
     "지수법칙 실험실 — 곱하면 지수도 곱할까?",
     "거듭제곱을 풀어 써서 a를 몇 번 곱했는지 직접 세고, 지수 규칙과 대조한다.",
     LAB_EXP),
    ("m2_inequality_sign_lab.html",
     "부등식 실험실 — 음수를 곱하면 무엇이 달라질까?",
     "부등식 실험실 — 음수를 곱하면 무엇이 달라질까?",
     "수직선 위 두 점에 같은 수를 곱하며 부등호 방향이 유지되는 조건을 기록한다.",
     LAB_INEQ),
    ("m2_system_solutions_lab.html",
     "연립방정식 실험실 — 해는 항상 하나일까?",
     "연립방정식 실험실 — 해는 항상 하나일까?",
     "두 번째 식의 계수를 바꿔 두 직선을 그리고, 해가 1개·없음·무수히 많음이 되는 조건을 찾는다.",
     LAB_SYS),
    ("m2_distributive_law_lab.html",
     "분배법칙 실험실 — 괄호 앞의 수는 어디까지 곱할까?",
     "분배법칙 실험실 — 괄호 앞의 수는 어디까지 곱할까?",
     "k(ax+b)에 값을 대입해 괄호를 먼저 계산한 값과 전개한 값을 비교한다.",
     LAB_DIST),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c13_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
