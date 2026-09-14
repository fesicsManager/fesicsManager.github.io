# -*- coding: utf-8 -*-
"""고등 공통수학1 실험 5종"""
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
function sgc(v,s){ if(v===0) return ''; return (v<0)?(' − '+(-v)+s):(' + '+v+s); }
"""

# ============================================================
# 1. 나머지정리
# ============================================================
LAB_REM = BASE + r"""
var LAB = {
  cw:440, ch:420, cvTitle:'조립제법 판',
  action:'나눠서 나머지 구하기',
  hint0:'삼차식의 계수와 나누는 일차식 x − k 의 k를 정해 보자.',
  sliders:[
    {id:'a',label:'x³의 계수',min:1,max:4,value:1,color:'#2563eb',unit:''},
    {id:'b',label:'x²의 계수',min:-6,max:6,value:-2,color:'#60a5fa',unit:''},
    {id:'c',label:'x의 계수',min:-6,max:6,value:3,color:'#16a34a',unit:''},
    {id:'k',label:'나누는 x − k 의 k',min:-4,max:4,value:2,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var d=1;
    var co=[S.a,S.b,S.c,d];
    var out=[],cur=0,i;
    for(i=0;i<4;i++){
      cur=(i===0)?co[0]:(cur*S.k+co[i]);
      out.push(cur);
    }
    var rem=out[3];
    var fk=S.a*S.k*S.k*S.k+S.b*S.k*S.k+S.c*S.k+d;
    return {co:co,out:out,rem:rem,fk:fk,d:d,
            q:[out[0],out[1],out[2]]};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'f('+S.k+')',v:c.fk},
            {k:'나눗셈의 나머지',v:ran?c.rem:'나눠 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '나머지는 '+c.rem+'이고 f('+S.k+') = '+c.fk+'다. '+((c.rem===c.fk)?'같다.':'다르다!')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*4);
    lbl(ctx,'f(x) = '+S.a+'x³'+sgc(S.b,'x²')+sgc(S.c,'x')+' + 1',24,38,'#1d4ed8',18);
    lbl(ctx,'x − '+S.k+' 로 나누기 (조립제법)',24,66,'#52627a',16);
    var X0=100, Y0=120, CW=72;
    lbl(ctx,''+S.k,X0-34,Y0+26,'#b45309',20);
    ctx.strokeStyle='#94a3b8';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(X0-16,Y0-16);ctx.lineTo(X0-16,Y0+70);ctx.stroke();
    ctx.beginPath();ctx.moveTo(X0-16,Y0+70);ctx.lineTo(X0+4*CW-20,Y0+70);ctx.stroke();
    for(i=0;i<4;i++){
      ctx.fillStyle='#1f2937';ctx.font='bold 19px sans-serif';ctx.textAlign='center';
      ctx.fillText(c.co[i],X0+i*CW,Y0+8);
      if(i>0&&i<shown){
        ctx.fillStyle='#b45309';ctx.font='17px sans-serif';
        ctx.fillText(c.out[i-1]*S.k,X0+i*CW,Y0+48);
      }
      if(i<shown){
        ctx.fillStyle=(i===3)?'#dc2626':'#15803d';ctx.font='bold 20px sans-serif';
        ctx.fillText(c.out[i],X0+i*CW,Y0+98);
      }
    }
    ctx.textAlign='left';
    if(shown>=4){
      lbl(ctx,'몫 : '+c.q[0]+'x²'+sgc(c.q[1],'x')+sg(c.q[2]),X0-40,Y0+140,'#15803d',18);
      lbl(ctx,'나머지 : '+c.rem,X0-40,Y0+170,'#b91c1c',20);
    }
    box(ctx,20,324,400,86);
    lbl(ctx,(t===null)?'나머지는 얼마일까?':('나머지 = '+c.rem),38,356,'#1f2937',20);
    lbl(ctx,'f('+S.k+') = '+c.fk,38,390,'#15803d',20);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,c:S.c,k:S.k,rem:c.rem,fk:c.fk,
            same:(c.rem===c.fk),
            q:c.q[0]+'x²'+sgc(c.q[1],'x')+sg(c.q[2])};
  },
  headA:['번호','f(x)','k','몫','나머지','f(k)','같은가?'],
  rowA:function(r,i){
    return [i+1,r.a+'x³'+sgc(r.b,'x²')+sgc(r.c,'x')+' + 1',r.k,r.q,'<b>'+r.rem+'</b>',r.fk,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,zero=0,ks={},kn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.rem===0) zero++;
      if(!ks[r.k]){ ks[r.k]=true; kn++; }
      rows.push([r.a+'x³'+sgc(r.b,'x²')+sgc(r.c,'x')+' + 1', r.k, r.q, '<b>'+r.rem+'</b>', r.fk,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'나머지 = f(k)',big:same+' / '+rec.length,
       p:'조립제법으로 구한 나머지와 x에 k를 대입한 값을 비교한 결과.'},
      {t:'나머지가 0이었던 기록',big:zero+'개',
       p:zero?'그때 x − k 가 f(x)의 인수다(인수정리).':'나머지가 0이 되는 k도 찾아보자.'},
      {t:'시험한 k',big:kn+'가지',p:'k를 바꿔도 관계가 유지되는지 확인했다.'}
    ];
    var concl;
    if(same===rec.length){
      concl='<b>정리</b> — 나눗셈을 끝까지 하지 않아도, x에 k를 <b>대입한 값이 곧 나머지</b>였다. '
           +'f(x) = (x − k)Q(x) + R 에 x = k를 넣으면 앞의 항이 0이 되어 f(k) = R이 되기 때문이다. '
           +(zero?'나머지가 0이면 x − k 가 인수이고, 이것이 인수정리다.':'나머지가 0이 되는 k를 찾으면 그것이 인수분해의 실마리다.');
    } else {
      concl='<b>확인 필요</b> — 나머지와 f(k)가 다른 기록이 있다.';
    }
    return {head:['f(x)','k','몫','나머지','f(k)','같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 항등식과 방정식
# ============================================================
LAB_IDENT = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'항등식 판정판',
  action:'여러 x를 넣어 보기',
  hint0:'양변의 계수를 정하고, x에 여러 값을 넣어 성립하는지 보자.',
  sliders:[
    {id:'a',label:'왼쪽 x의 계수',min:-5,max:5,value:2,color:'#2563eb',unit:''},
    {id:'b',label:'왼쪽 상수',min:-8,max:8,value:3,color:'#60a5fa',unit:''},
    {id:'c',label:'오른쪽 x의 계수',min:-5,max:5,value:2,color:'#dc2626',unit:''},
    {id:'d',label:'오른쪽 상수',min:-8,max:8,value:3,color:'#f87171',unit:''}
  ],
  calc:function(S){
    var hits=0,i,total=0;
    for(i=-5;i<=5;i++){
      total++;
      if(S.a*i+S.b===S.c*i+S.d) hits++;
    }
    var kind;
    if(S.a===S.c&&S.b===S.d) kind='항등식 (모든 x)';
    else if(S.a===S.c) kind='해가 없음';
    else kind='해가 1개';
    return {hits:hits,total:total,kind:kind,
            sol:(S.a!==S.c)?((S.d-S.b)/(S.a-S.c)):null};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'식',v:S.a+'x'+sg(S.b)+' = '+S.c+'x'+sg(S.d)},
            {k:'−5~5 중 성립',v:ran?(c.hits+' / '+c.total):'넣어 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '−5부터 5까지 11개 중 '+c.hits+'개에서 성립했다. 이 식은 '+c.kind+'이다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*11);
    lbl(ctx,S.a+'x'+sg(S.b)+'  =  '+S.c+'x'+sg(S.d),24,44,'#1d4ed8',24);
    var X0=44, CW=34, Y=110;
    for(i=0;i<11;i++){
      var x=i-5, on=(i<shown);
      var L=S.a*x+S.b, R=S.c*x+S.d;
      var ok=(L===R);
      var cx=X0+i*CW;
      ctx.fillStyle=on?(ok?'#bbf7d0':'#fecaca'):'#f1f5f9';
      ctx.fillRect(cx,Y,CW-3,30);
      ctx.strokeStyle=on?(ok?'#16a34a':'#dc2626'):'#e2e8f0';ctx.lineWidth=1.6;
      ctx.strokeRect(cx,Y,CW-3,30);
      ctx.fillStyle='#334155';ctx.font='bold 13px sans-serif';ctx.textAlign='center';
      ctx.fillText(x,cx+CW/2-1,Y-8);
      if(on){
        ctx.fillStyle=ok?'#14532d':'#7f1d1d';
        ctx.fillText(ok?'○':'×',cx+CW/2-1,Y+20);
      }
      if(on){
        ctx.fillStyle='#94a3b8';ctx.font='10px sans-serif';
        ctx.fillText(L,cx+CW/2-1,Y+46);
        ctx.fillText(R,cx+CW/2-1,Y+60);
      }
    }
    ctx.textAlign='left';
    lbl(ctx,'x = −5 부터 5 까지 넣어 보기  (아래: 좌변 / 우변)',24,196,'#52627a',15);
    box(ctx,20,222,400,162);
    lbl(ctx,(t===null)?'몇 개의 x에서 성립할까?':('성립한 x : '+c.hits+' / '+c.total+'개'),38,256,'#1f2937',20);
    lbl(ctx,'왼쪽 계수 '+S.a+' , 오른쪽 계수 '+S.c+'  →  '+((S.a===S.c)?'같음':'다름'),38,292,'#52627a',18);
    lbl(ctx,'왼쪽 상수 '+S.b+' , 오른쪽 상수 '+S.d+'  →  '+((S.b===S.d)?'같음':'다름'),38,322,'#52627a',18);
    lbl(ctx,(t===null)?'':('판정 : '+c.kind),38,360,(c.kind.indexOf('항등')>=0)?'#15803d':'#b91c1c',20);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,cc:S.c,d:S.d,hits:c.hits,kind:c.kind,
            coefSame:(S.a===S.c),constSame:(S.b===S.d),
            all:(c.hits===11),
            sol:(c.sol===null)?'-':r2(c.sol)};
  },
  headA:['번호','식','계수 같음','상수 같음','성립한 x 개수','판정','해'],
  rowA:function(r,i){
    return [i+1,r.a+'x'+sg(r.b)+' = '+r.cc+'x'+sg(r.d),
            '<span class="'+(r.coefSame?'ok':'no')+'">'+(r.coefSame?'○':'×')+'</span>',
            '<span class="'+(r.constSame?'ok':'no')+'">'+(r.constSame?'○':'×')+'</span>',
            '<b>'+r.hits+' / 11</b>',r.kind,r.sol];
  },
  analyze:function(rec){
    var rows=[],both=0,bothAll=0,coefOnly=0,coefNone=0,diff=0,diffOne=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.coefSame&&r.constSame){ both++; if(r.all) bothAll++; }
      else if(r.coefSame){ coefOnly++; if(r.hits===0) coefNone++; }
      else { diff++; if(r.hits<=1) diffOne++; }
      rows.push([r.a+'x'+sg(r.b)+' = '+r.cc+'x'+sg(r.d),
                 (r.coefSame?'○':'×')+' / '+(r.constSame?'○':'×'),
                 '<b>'+r.hits+' / 11</b>', r.kind, r.sol]);
    }
    var stats=[
      {t:'계수도 상수도 같았던 기록',big:both+'개',
       p:both?('그중 모든 x에서 성립한 것 '+bothAll+'개.'):'양변을 완전히 같게 만들어 보자.'},
      {t:'계수만 같았던 기록',big:coefOnly+'개',
       p:coefOnly?('그중 성립하는 x가 하나도 없던 것 '+coefNone+'개.'):'계수는 같고 상수만 다르게 해 보자.'},
      {t:'계수가 달랐던 기록',big:diff+'개',
       p:diff?('그중 성립한 x가 한 개 이하였던 것 '+diffOne+'개.'):'계수를 다르게도 해 보자.'}
    ];
    var concl;
    if(both===0||coefOnly===0||diff===0){
      concl='<b>더 해 보자</b> — 세 경우(양변 완전히 같음 / 계수만 같음 / 계수 다름)를 <b>모두</b> 기록해야 구별이 된다.';
    } else if(bothAll===both&&coefNone===coefOnly){
      concl='<b>정리</b> — <b>양변의 계수와 상수가 모두 같을 때만</b> 모든 x에서 성립했다. 이것이 항등식이고, '
           +'그래서 항등식은 <b>계수를 비교</b>해서 다룬다. 계수만 같고 상수가 다르면 성립하는 x가 하나도 없었고, '
           +'계수가 다르면 딱 한 x에서만 성립했다(방정식). '
           +'“x에 몇 개 넣어 봤더니 맞더라”는 항등식의 근거가 되지 못한다.';
    } else {
      concl='<b>확인 필요</b> — 판정과 실제 결과가 어긋난 기록이 있다.';
    }
    return {head:['식','계수/상수 같음','성립 개수','판정','해'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 복소수
# ============================================================
LAB_CPLX = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'복소평면 판',
  action:'거듭제곱하고 곱해 보기',
  hint0:'i의 지수와 복소수 a + bi 를 정해 보자.',
  sliders:[
    {id:'n',label:'i의 지수 n',min:1,max:20,value:7,color:'#2563eb',unit:''},
    {id:'a',label:'실수부 a',min:-5,max:5,value:3,color:'#16a34a',unit:''},
    {id:'b',label:'허수부 b',min:-5,max:5,value:2,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var re=1,im=0,i;
    for(i=0;i<S.n;i++){ var nr=re*0-im*1, ni=re*1+im*0; re=nr; im=ni; }
    var names=['1','i','−1','−i'];
    var conj=[S.a*S.a+S.b*S.b,0];
    var sq=[S.a*S.a-S.b*S.b,2*S.a*S.b];
    return {re:Math.round(re),im:Math.round(im),mod:S.n%4,
            name:names[S.n%4],conj:conj,sq:sq};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'i^'+S.n,v:ran?c.name:'구해 보자'},
            {k:'(a+bi)(a−bi)',v:ran?(c.conj[0]+''):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'i^'+S.n+' = '+c.name+' (n을 4로 나눈 나머지 '+c.mod+').  (a+bi)(a−bi) = '+c.conj[0]+'로 실수다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var CX=140, CY=170, U=54;
    ctx.strokeStyle='#e2e8f0';ctx.lineWidth=1.4;
    ctx.beginPath();ctx.moveTo(CX-2.2*U,CY);ctx.lineTo(CX+2.2*U,CY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(CX,CY-2.2*U);ctx.lineTo(CX,CY+2.2*U);ctx.stroke();
    ctx.beginPath();ctx.arc(CX,CY,U,0,Math.PI*2);
    ctx.strokeStyle='#cbd5e1';ctx.lineWidth=1.6;ctx.stroke();
    var pts=[[1,0,'1'],[0,1,'i'],[-1,0,'−1'],[0,-1,'−i']];
    var step=(t===null)?0:Math.min(S.n,Math.floor(Math.min(1,t)*S.n)+1);
    for(i=0;i<4;i++){
      var on=(step>0&&(step%4)===i);
      ctx.beginPath();ctx.arc(CX+pts[i][0]*U,CY-pts[i][1]*U,on?10:6,0,Math.PI*2);
      ctx.fillStyle=on?'#dc2626':'#94a3b8';ctx.fill();
      lbl(ctx,pts[i][2],CX+pts[i][0]*U*1.35-6,CY-pts[i][1]*U*1.35+6,on?'#b91c1c':'#64748b',15);
    }
    if(step>0){
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=2.4;
      ctx.beginPath();ctx.arc(CX,CY,U,-Math.PI/2*((step-1)%4+1)+Math.PI/2,Math.PI/2-Math.PI/2*0);
      ctx.stroke();
    }
    lbl(ctx,'i를 곱할 때마다 90° 돌아간다',24,34,'#52627a',15);
    lbl(ctx,'i^'+S.n+' = '+((t===null)?'?':c.name),260,120,'#1d4ed8',24);
    lbl(ctx,S.n+' ÷ 4 의 나머지 = '+c.mod,260,156,'#52627a',16);
    box(ctx,20,290,400,124);
    lbl(ctx,(t===null)?'i의 거듭제곱은 어떤 규칙일까?':('i^'+S.n+' = '+c.name),38,322,'#1f2937',20);
    lbl(ctx,'a + bi = '+S.a+sgc(S.b,'i'),38,354,'#334155',18);
    lbl(ctx,(t===null)?'':('(a+bi)(a−bi) = '+(S.a*S.a)+' + '+(S.b*S.b)+' = '+c.conj[0]+'  (실수)'),38,384,'#15803d',17);
    lbl(ctx,(t===null)?'':('(a+bi)² = '+c.sq[0]+sgc(c.sq[1],'i')+'  '+((c.sq[1]===0)?'(실수)':'(허수부 있음)')),38,408,'#b45309',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {n:S.n,mod:S.n%4,name:c.name,a:S.a,b:S.b,
            conj:c.conj[0],sqRe:c.sq[0],sqIm:c.sq[1],
            conjReal:(c.conj[0]===S.a*S.a+S.b*S.b),
            sqReal:(c.sq[1]===0)};
  },
  headA:['번호','n','n mod 4','i^n','a + bi','(a+bi)(a−bi)','실수?','(a+bi)²','실수?'],
  rowA:function(r,i){
    return [i+1,r.n,r.mod,'<b>'+r.name+'</b>',r.a+sgc(r.b,'i'),r.conj,
            '<span class="ok">○</span>',
            r.sqRe+((r.sqIm===0)?'':sgc(r.sqIm,'i')),
            '<span class="'+(r.sqReal?'ok':'no')+'">'+(r.sqReal?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],g={},gn=0,ok=0,sqReal=0,zero=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(!g[r.mod]){ g[r.mod]=r.name; gn++; }
      else if(g[r.mod]!==r.name) ok++;
      if(r.sqReal){ sqReal++; if(r.a===0||r.b===0) zero++; }
      rows.push([r.n, r.mod, '<b>'+r.name+'</b>', r.a+sgc(r.b,'i'), r.conj,
                 r.sqRe+((r.sqIm===0)?'':sgc(r.sqIm,'i')),
                 '<span class="'+(r.sqReal?'ok':'no')+'">'+(r.sqReal?'○':'×')+'</span>']);
    }
    var lines=[],k;
    for(k in g){ lines.push('나머지 '+k+' → '+g[k]); }
    var stats=[
      {t:'나머지가 같으면 i^n도 같았나',big:(ok===0)?'모두 일치':(ok+'건 불일치'),
       p:lines.join(' / ')},
      {t:'켤레복소수끼리의 곱',big:'항상 실수',
       p:'(a+bi)(a−bi) = a² + b² 으로 허수부가 사라진다.'},
      {t:'(a+bi)²이 실수였던 기록',big:sqReal+'개',
       p:sqReal?('그중 a나 b가 0이었던 것 '+zero+'개. 제곱은 대개 실수가 아니다.'):'제곱은 대개 허수부가 남는다.'}
    ];
    var concl;
    if(gn<4){
      concl='<b>더 해 보자</b> — n을 바꿔 4로 나눈 나머지 <b>0, 1, 2, 3</b>을 모두 기록해 보자.';
    } else {
      concl='<b>정리</b> — i의 거듭제곱은 <b>1, i, −1, −i 가 4개 주기로 되풀이</b>되었고, n을 4로 나눈 나머지만 보면 바로 알 수 있었다. '
           +'복소평면에서 i를 곱하는 것이 90° 회전이라서 네 번이면 제자리로 돌아온다. '
           +'또 <b>켤레복소수끼리의 곱은 언제나 실수</b>(a²+b²)였지만, 그냥 제곱하면 대개 허수부가 남았다. '
           +'분모를 실수로 만들 때 켤레를 곱하는 이유가 여기 있다.';
    }
    return {head:['n','n mod 4','i^n','a+bi','켤레곱','제곱','실수?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 허근과 켤레근
# ============================================================
LAB_IMROOT = BASE + r"""
var LAB = {
  cw:440, ch:420, cvTitle:'이차방정식 근 판',
  action:'근 구하기',
  hint0:'계수를 정하고 두 근을 구해 보자. 판별식이 음수여도 근은 존재한다.',
  sliders:[
    {id:'a',label:'a',min:1,max:4,value:1,color:'#2563eb',unit:''},
    {id:'b',label:'b',min:-8,max:8,value:-4,color:'#16a34a',unit:''},
    {id:'c',label:'c',min:-8,max:8,value:8,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var D=S.b*S.b-4*S.a*S.c;
    var re=-S.b/(2*S.a);
    if(D>=0){
      var s=Math.sqrt(D);
      return {D:D,real:true,x1:(-S.b-s)/(2*S.a),x2:(-S.b+s)/(2*S.a),re:re,im:0};
    }
    var im=Math.sqrt(-D)/(2*S.a);
    return {D:D,real:false,re:re,im:im};
  },
  fmt:function(c){
    if(c.real) return r3(c.x1)+' , '+r3(c.x2);
    return r3(c.re)+' ± '+r3(c.im)+'i';
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'b² − 4ac',v:c.D},
            {k:'두 근',v:ran?this.fmt(c):'구해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '두 근은 '+this.fmt(c)+'.  '+(c.real?'실근이다.':'서로 켤레인 허근이다.')+' 합과 곱은 여전히 실수인지 확인해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var CX=160, CY=200, U=26;
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=-5;i<=5;i++){ ctx.beginPath();ctx.moveTo(CX+i*U,CY-4*U);ctx.lineTo(CX+i*U,CY+4*U);ctx.stroke(); }
    for(i=-4;i<=4;i++){ ctx.beginPath();ctx.moveTo(CX-5*U,CY+i*U);ctx.lineTo(CX+5*U,CY+i*U);ctx.stroke(); }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(CX-5*U,CY);ctx.lineTo(CX+5*U,CY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(CX,CY-4*U);ctx.lineTo(CX,CY+4*U);ctx.stroke();
    lbl(ctx,'실수축',CX+5*U-40,CY+18,'#94a3b8',12);
    lbl(ctx,'허수축',CX+6,CY-4*U+14,'#94a3b8',12);
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>=1){
      if(c.real){
        [c.x1,c.x2].forEach(function(x){
          if(Math.abs(x)>5) return;
          ctx.beginPath();ctx.arc(CX+x*U,CY,8,0,Math.PI*2);
          ctx.fillStyle='#2563eb';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
        });
      } else {
        [1,-1].forEach(function(s){
          if(Math.abs(c.re)>5||Math.abs(c.im)>4) return;
          ctx.beginPath();ctx.arc(CX+c.re*U,CY-s*c.im*U,8,0,Math.PI*2);
          ctx.fillStyle='#dc2626';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
        });
        ctx.strokeStyle='#f87171';ctx.lineWidth=1.6;ctx.setLineDash([4,4]);
        ctx.beginPath();ctx.moveTo(CX+c.re*U,CY-c.im*U);ctx.lineTo(CX+c.re*U,CY+c.im*U);ctx.stroke();ctx.setLineDash([]);
      }
    }
    lbl(ctx,S.a+'x²'+sgc(S.b,'x')+sg(S.c)+' = 0',24,34,'#1d4ed8',18);
    lbl(ctx,'복소평면 위의 두 근',24,58,'#52627a',15);
    box(ctx,20,326,400,86);
    lbl(ctx,(t===null)?'근은 어디에 있을까?':('두 근 : '+this.fmt(c)),38,358,c.real?'#15803d':'#b91c1c',19);
    lbl(ctx,(t===null)?'':('두 근의 합 '+r3(-S.b/S.a)+'      곱 '+r3(S.c/S.a)+'  (둘 다 실수)'),38,392,'#52627a',17);
  },
  record:function(S){
    var c=this.calc(S);
    var sum=-S.b/S.a, prod=S.c/S.a;
    return {a:S.a,b:S.b,c:S.c,D:c.D,real:c.real,
            roots:this.fmt(c),
            sum:r3(sum),prod:r3(prod),
            conj:(!c.real),
            sumReal:true,prodReal:true,
            xcut:c.real};
  },
  headA:['번호','식','b²−4ac','근의 종류','두 근','합','곱','x축과 만남'],
  rowA:function(r,i){
    return [i+1,r.a+'x²'+sgc(r.b,'x')+sg(r.c),r.D,r.real?'실근':'허근','<b>'+r.roots+'</b>',r.sum,r.prod,
            '<span class="'+(r.xcut?'ok':'no')+'">'+(r.xcut?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],re=0,im=0,conj=0,allReal=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.real) re++; else { im++; if(r.conj) conj++; }
      allReal++;
      rows.push([r.a+'x²'+sgc(r.b,'x')+sg(r.c), r.D, r.real?'실근':'허근', '<b>'+r.roots+'</b>',
                 r.sum, r.prod,
                 '<span class="'+(r.xcut?'ok':'no')+'">'+(r.xcut?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'실근 / 허근',big:re+'개 / '+im+'개',
       p:(re&&im)?'두 경우를 모두 기록했다.':'판별식이 음수인 경우도 만들어 보자.'},
      {t:'허근이 서로 켤레였던 횟수',big:im?(conj+' / '+im):'기록 없음',
       p:'실수 계수 방정식의 허근은 언제나 짝을 이룬다.'},
      {t:'합과 곱이 실수였던 횟수',big:allReal+' / '+rec.length,
       p:'허근이어도 −b/a, c/a는 실수다.'}
    ];
    var concl;
    if(re===0||im===0){
      concl='<b>더 해 보자</b> — 판별식이 <b>양수인 경우와 음수인 경우</b>를 모두 기록해 보자. a=1, b=−4, c=8이면 허근이 나온다.';
    } else {
      concl='<b>정리</b> — 판별식이 음수여도 근이 <b>없는 것이 아니라</b> 복소평면 위에 있었다. '
           +'실수 계수 방정식의 허근은 언제나 <b>a + bi 와 a − bi 로 짝(켤레)</b>을 이루었고, '
           +'그래서 두 근의 합과 곱은 허수부가 상쇄되어 항상 실수(−b/a, c/a)였다. '
           +'“x축과 만나지 않는다”는 실근이 없다는 뜻이지 해가 없다는 뜻이 아니다.';
    }
    return {head:['식','b²−4ac','종류','두 근','합','곱','x축과 만남'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 이차함수와 직선의 위치 관계
# ============================================================
LAB_QLINE = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'포물선과 직선',
  action:'교점 찾기',
  hint0:'포물선 y = x² 과 직선 y = mx + n 의 직선 계수를 정해 보자.',
  sliders:[
    {id:'m',label:'직선의 기울기 m',min:-6,max:6,value:2,color:'#dc2626',unit:''},
    {id:'n',label:'직선의 y절편 n',min:-8,max:8,value:-1,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var D=S.m*S.m+4*S.n;
    var cnt=(D>1e-9)?2:((D<-1e-9)?0:1);
    var x1=null,x2=null;
    if(cnt===2){ x1=(S.m-Math.sqrt(D))/2; x2=(S.m+Math.sqrt(D))/2; }
    else if(cnt===1){ x1=S.m/2; }
    return {D:D,cnt:cnt,x1:x1,x2:x2};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'x² − mx − n = 0 의 판별식',v:c.D},
            {k:'교점의 개수',v:ran?(c.cnt+'개'):'찾아보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '판별식 '+c.D+'이고 교점은 '+c.cnt+'개다. '+((c.cnt===1)?'직선이 포물선에 접한다.':'')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var CX=220, CY=300, U=24;
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=-9;i<=9;i++){ ctx.beginPath();ctx.moveTo(CX+i*U,CY-11*U);ctx.lineTo(CX+i*U,CY+2*U);ctx.stroke(); }
    for(i=-2;i<=11;i++){ ctx.beginPath();ctx.moveTo(CX-9*U,CY-i*U);ctx.lineTo(CX+9*U,CY-i*U);ctx.stroke(); }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(CX-9*U,CY);ctx.lineTo(CX+9*U,CY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(CX,CY-11*U);ctx.lineTo(CX,CY+2*U);ctx.stroke();
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    var st=false;
    for(i=-90;i<=90;i++){
      var xx=i/10, yy=xx*xx;
      if(yy>11){ st=false; continue; }
      if(!st){ ctx.moveTo(CX+xx*U,CY-yy*U); st=true; } else ctx.lineTo(CX+xx*U,CY-yy*U);
    }
    ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      ctx.strokeStyle='#dc2626';ctx.lineWidth=3;ctx.beginPath();
      st=false;
      for(i=-90;i<=90;i++){
        var x2=i/10, y2=S.m*x2+S.n;
        if(y2<-2||y2>11){ st=false; continue; }
        if(!st){ ctx.moveTo(CX+x2*U,CY-y2*U); st=true; } else ctx.lineTo(CX+x2*U,CY-y2*U);
      }
      ctx.stroke();
    }
    if(grow>=1){
      [c.x1,c.x2].forEach(function(x){
        if(x===null||Math.abs(x)>9) return;
        var y=x*x;
        if(y>11) return;
        ctx.beginPath();ctx.arc(CX+x*U,CY-y*U,8,0,Math.PI*2);
        ctx.fillStyle='#f59e0b';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      });
    }
    lbl(ctx,'y = x²   과   y = '+S.m+'x'+sg(S.n),24,32,'#1d4ed8',18);
    box(ctx,20,344,400,74);
    lbl(ctx,'x² = '+S.m+'x'+sg(S.n)+'  →  x²'+sgc(-S.m,'x')+sg(-S.n)+' = 0',38,374,'#334155',17);
    lbl(ctx,(t===null)?'몇 점에서 만날까?':('판별식 '+c.D+'  →  교점 '+c.cnt+'개'+((c.cnt===1)?' (접함)':'')),
        38,404,(c.cnt===1)?'#b45309':((c.cnt===0)?'#b91c1c':'#15803d'),18);
  },
  record:function(S){
    var c=this.calc(S);
    return {m:S.m,n:S.n,D:c.D,cnt:c.cnt,
            x1:(c.x1===null)?'-':r2(c.x1),x2:(c.x2===null)?'-':r2(c.x2),
            tangent:(c.cnt===1)};
  },
  headA:['번호','직선','판별식','교점 개수','교점의 x','접하는가?'],
  rowA:function(r,i){
    return [i+1,'y = '+r.m+'x'+sg(r.n),r.D,'<b>'+r.cnt+'개</b>',
            (r.cnt===0)?'없음':(r.x1+((r.cnt===2)?(', '+r.x2):'')),
            '<span class="'+(r.tangent?'ok':'no')+'">'+(r.tangent?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],two=0,one=0,zero=0,match=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var expect=(r.D>0)?2:((r.D<0)?0:1);
      var m=(expect===r.cnt);
      if(m) match++;
      if(r.cnt===2) two++; else if(r.cnt===1) one++; else zero++;
      rows.push(['y = '+r.m+'x'+sg(r.n), r.D, '<b>'+r.cnt+'개</b>',
                 (r.cnt===0)?'없음':(r.x1+((r.cnt===2)?(', '+r.x2):'')),
                 '<span class="'+(m?'ok':'no')+'">'+(m?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'판별식으로 한 예측이 맞은 횟수',big:match+' / '+rec.length,
       p:'두 식을 연립해 만든 이차방정식의 판별식으로 판단했다.'},
      {t:'두 점 / 접함 / 만나지 않음',big:two+' / '+one+' / '+zero,
       p:(two&&one&&zero)?'세 경우를 모두 기록했다.':'세 경우를 모두 만들어 보자.'},
      {t:'접한 기록',big:one+'개',
       p:one?'판별식이 정확히 0일 때만 접했다.':'m=2, n=−1이면 판별식이 0이 된다.'}
    ];
    var concl;
    if(!(two&&one&&zero)){
      concl='<b>더 해 보자</b> — 두 점에서 만나는 경우, 접하는 경우, 만나지 않는 경우를 <b>모두</b> 만들어 보자. '
           +'m = 2, n = −1 이면 딱 접한다.';
    } else if(match===rec.length){
      concl='<b>정리</b> — 두 그래프의 교점은 <b>연립해서 만든 이차방정식의 실근</b>이었다. '
           +'판별식이 양수면 두 점, 0이면 한 점에서 접하고, 음수면 만나지 않았다. '
           +'“접한다”는 <b>중근을 가진다</b>는 뜻이고, 그래프를 그리지 않아도 판별식으로 판정할 수 있다.';
    } else {
      concl='<b>확인 필요</b> — 판별식과 교점 수가 어긋난 기록이 있다.';
    }
    return {head:['직선','판별식','교점 수','교점의 x','예측 일치?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("h1_remainder_theorem_lab_CommonMath1_Poly_Ep06.html",
     "나머지정리 실험실 — 나눠 보지 않고 나머지를 알 수 있을까?",
     "나머지정리 실험실 — 나눠 보지 않고 나머지를 알 수 있을까?",
     "조립제법으로 실제 나눗셈을 하고, x에 k를 대입한 값과 나머지를 대조한다.",
     LAB_REM),
    ("h1_identity_equation_lab_CommonMath1_Poly_Ep05.html",
     "항등식 실험실 — 몇 개 맞으면 항등식일까?",
     "항등식 실험실 — 몇 개 맞으면 항등식일까?",
     "양변의 계수를 바꿔 가며 x에 여러 값을 넣어 보고, 항등식과 방정식을 구별한다.",
     LAB_IDENT),
    ("h1_complex_number_lab_CommonMath1_Complex_Ep02.html",
     "복소수 실험실 — i를 계속 곱하면 어떻게 될까?",
     "복소수 실험실 — i를 계속 곱하면 어떻게 될까?",
     "복소평면에서 i의 거듭제곱을 따라가고, 켤레복소수의 곱과 제곱을 비교한다.",
     LAB_CPLX),
    ("h1_imaginary_root_lab_CommonMath1_Complex_Ep05.html",
     "허근 실험실 — 판별식이 음수면 근이 없을까?",
     "허근 실험실 — 판별식이 음수면 근이 없을까?",
     "계수를 바꿔 가며 두 근을 복소평면에 찍고, 근의 합과 곱이 실수인지 확인한다.",
     LAB_IMROOT),
    ("h1_parabola_line_lab_CommonMath1_Quad_Ep03.html",
     "접선 실험실 — 접한다는 것은 무슨 뜻일까?",
     "접선 실험실 — 접한다는 것은 무슨 뜻일까?",
     "포물선과 직선을 연립해 만든 이차방정식의 판별식과 실제 교점 개수를 대조한다.",
     LAB_QLINE),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c21_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
