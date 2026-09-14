# -*- coding: utf-8 -*-
"""초등 5-6학년군 '수와 연산' 실험 5종"""
import os, re

OUT = "/mnt/user-data/outputs"
src = open("/home/claude/gen_math_labs.py", encoding="utf-8").read()
TPL = re.search(r'TPL = r"""(.*?)"""\n', src, re.S).group(1)

BASE = r"""
function lbl(ctx,t,x,y,c,sz,al){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
function box(ctx,x,y,w,h){ctx.fillStyle='#f1f6fd';ctx.fillRect(x,y,w,h);ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(x,y,w,h);}
function r1(v){return Math.round(v*10)/10;}
function r3(v){return Math.round(v*1000)/1000;}
function gcd(x,y){ while(y){ var t=x%y; x=y; y=t; } return x; }
"""

# ============================================================
# 1. 최소공배수
# ============================================================
LAB_LCM = BASE + r"""
function lcmOf(a,b){ var m=a; while(m%b!==0){ m+=a; } return m; }
var LAB = {
  cw:440, ch:400, cvTitle:'배수 만나기판',
  action:'배수를 차례로 놓기',
  hint0:'두 수를 정하고, 두 수의 배수가 처음 만나는 곳을 찾아보자.',
  sliders:[
    {id:'a',label:'첫 번째 수',min:2,max:12,value:4,color:'#2563eb',unit:''},
    {id:'b',label:'두 번째 수',min:2,max:12,value:6,color:'#16a34a',unit:''}
  ],
  readout:function(S,ran){
    return [{k:'두 수의 곱',v:(S.a*S.b)},
            {k:'최소공배수',v:ran?lcmOf(S.a,S.b):'찾아보자'}];
  },
  doneMsg:function(S){
    var L=lcmOf(S.a,S.b), P=S.a*S.b;
    return '처음 만난 수는 '+L+'이다. 두 수의 곱은 '+P+'인데 '+(L===P?'마침 같았다':('그보다 작다'))+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var L=lcmOf(S.a,S.b), i;
    var X0=40, X1=404;
    function px(v){ return X0+(X1-X0)*v/L; }
    var show=(t===null)?0:Math.min(1,t);
    var upto=show*L;
    function track(y,step,col,name){
      ctx.strokeStyle='#cbd5e1';ctx.lineWidth=2.5;
      ctx.beginPath();ctx.moveTo(X0,y);ctx.lineTo(X1,y);ctx.stroke();
      lbl(ctx,name,X0-16,y+6,col,15,'right');
      for(var v=step; v<=L; v+=step){
        var on=(v<=upto);
        var x=px(v);
        ctx.beginPath();ctx.arc(x,y,on?8:4,0,Math.PI*2);
        ctx.fillStyle=on?col:'#e2e8f0';ctx.fill();
        if(on){ ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke(); }
      }
    }
    track(120,S.a,'#2563eb',S.a+'의 배수');
    track(200,S.b,'#16a34a',S.b+'의 배수');
    if(show>=1){
      var xm=px(L);
      ctx.setLineDash([5,5]);ctx.strokeStyle='#f59e0b';ctx.lineWidth=3;
      ctx.beginPath();ctx.moveTo(xm,96);ctx.lineTo(xm,232);ctx.stroke();ctx.setLineDash([]);
      lbl(ctx,'처음 만난 수 '+L,xm,86,'#b45309',17,'center');
    }
    lbl(ctx,S.a+'의 배수와 '+S.b+'의 배수는 어디서 처음 만날까?',24,44,'#1d4ed8',18);
    box(ctx,20,262,400,120);
    var g=gcd(S.a,S.b), P=S.a*S.b;
    lbl(ctx,(t===null)?'아직 찾지 않았다':('최소공배수 : '+L),38,294,'#1f2937',21);
    lbl(ctx,'두 수의 곱 : '+S.a+' × '+S.b+' = '+P,38,322,'#52627a',18);
    lbl(ctx,(t===null)?'':('최대공약수 : '+g+'    곱 ÷ 최대공약수 = '+(P/g)),38,350,'#15803d',18);
    lbl(ctx,(t===null)?'':((L===P)?'이번엔 곱과 같다':'곱보다 작다'),38,374,(L===P)?'#b45309':'#b91c1c',17);
  },
  record:function(S){
    var L=lcmOf(S.a,S.b), g=gcd(S.a,S.b), P=S.a*S.b;
    return {a:S.a,b:S.b,lcm:L,g:g,prod:P,pg:P/g,isProd:(L===P)};
  },
  headA:['번호','두 수','최소공배수','두 수의 곱','최대공약수','곱 ÷ 최대공약수','곱이 최소공배수?'],
  rowA:function(r,i){
    return [i+1,r.a+', '+r.b,'<b>'+r.lcm+'</b>',r.prod,r.g,r.pg,
            '<span class="'+(r.isProd?'ok':'no')+'">'+(r.isProd?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],prodOk=0,ruleOk=0,g1=0,g1prod=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var a=(r.lcm===r.prod), b=(r.lcm===r.pg);
      if(a) prodOk++;
      if(b) ruleOk++;
      if(r.g===1){ g1++; if(a) g1prod++; }
      rows.push([r.a+', '+r.b, r.g, '<b>'+r.lcm+'</b>', r.prod,
                 '<span class="'+(a?'ok':'no')+'">'+(a?'○':'×')+'</span>',
                 r.pg,
                 '<span class="'+(b?'ok':'no')+'">'+(b?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'“두 수의 곱 = 최소공배수”가 맞은 횟수',big:prodOk+' / '+rec.length,
       p:'곱을 그대로 답으로 쓰면 맞을 때도 있고 틀릴 때도 있었다.'},
      {t:'최대공약수가 1이었던 기록',big:g1+'개',
       p:g1?('그중 곱이 최소공배수였던 것 '+g1prod+'개.'):'서로소인 두 수도 시험해 보자.'},
      {t:'“곱 ÷ 최대공약수 = 최소공배수”',big:ruleOk+' / '+rec.length,
       p:'최대공약수로 나눈 값이 항상 최소공배수와 같았는지 확인한 결과.'}
    ];
    var concl;
    if(ruleOk!==rec.length){
      concl='<b>확인 필요</b> — 규칙에 어긋난 기록이 있다. 값을 다시 확인해 보자.';
    } else if(prodOk<rec.length){
      concl='<b>정리</b> — 두 수의 곱이 최소공배수인 경우는 <b>최대공약수가 1일 때뿐</b>이었다. '
           +'4와 6처럼 공약수가 있으면 곱(24)보다 훨씬 작은 12에서 이미 만난다. '
           +'언제나 성립한 규칙은 <b>최소공배수 = 두 수의 곱 ÷ 최대공약수</b>였다.';
    } else {
      concl='<b>더 해 보자</b> — 지금까지는 곱이 곧 최소공배수였다. 4와 6처럼 <b>공약수가 있는 두 수</b>로도 해 보자.';
    }
    return {head:['두 수','최대공약수','최소공배수','두 수의 곱','곱=최소공배수?','곱÷최대공약수','최소공배수와 같나?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 분수의 덧셈 (통분)
# ============================================================
LAB_FRAC_ADD = BASE + r"""
function red(n,d){ var g=gcd(n,d); return [n/g,d/g]; }
function fstr(n,d){ if(d===1) return ''+n; if(n===d) return '1'; return n+'/'+d; }
var LAB = {
  cw:440, ch:430, cvTitle:'분수 띠 덧셈판',
  action:'같은 크기로 다시 잘라 더하기',
  hint0:'두 단위분수를 정하고, 같은 크기 조각으로 다시 잘라 더해 보자.',
  sliders:[
    {id:'a',label:'첫 번째 분수의 분모',min:2,max:10,value:2,color:'#2563eb',
     fmt:function(v){return '1/'+v;}},
    {id:'b',label:'두 번째 분수의 분모',min:2,max:10,value:3,color:'#16a34a',
     fmt:function(v){return '1/'+v;}}
  ],
  readout:function(S,ran){
    var rr=red(S.a+S.b,S.a*S.b);
    return [{k:'분모끼리 더하면',v:'1/'+(S.a+S.b)},
            {k:'실제 합',v:ran?fstr(rr[0],rr[1]):'더해 보자'}];
  },
  doneMsg:function(S){
    var rr=red(S.a+S.b,S.a*S.b);
    return '실제 합은 '+fstr(rr[0],rr[1])+'이다. 분모끼리 더한 1/'+(S.a+S.b)+'보다 훨씬 크다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var BX=40, BW=360, i;
    var a=S.a, b=S.b, D=a*b;
    function bar(y,n,fill,col,edge){
      ctx.fillStyle='#f8fafc';ctx.fillRect(BX,y,BW,40);
      ctx.fillStyle=col;ctx.fillRect(BX,y,BW*fill/n,40);
      ctx.strokeStyle='#9aa8bb';ctx.lineWidth=1.4;
      for(i=1;i<n;i++){ ctx.beginPath();ctx.moveTo(BX+BW*i/n,y);ctx.lineTo(BX+BW*i/n,y+40);ctx.stroke(); }
      ctx.strokeStyle=edge;ctx.lineWidth=2.5;ctx.strokeRect(BX,y,BW,40);
    }
    var cut=(t===null)?0:Math.min(1,t/0.5);
    var merge=(t===null)?0:Math.max(0,(t-0.5)/0.5);
    bar(70,a,1,'#bfdbfe','#2563eb');
    lbl(ctx,'1/'+a,BX-8,96,'#1d4ed8',17,'right');
    bar(140,b,1,'#bbf7d0','#16a34a');
    lbl(ctx,'1/'+b,BX-8,166,'#15803d',17,'right');
    var nSub=Math.round(a+(D-a)*cut), nSub2=Math.round(b+(D-b)*cut);
    if(cut>0){
      ctx.strokeStyle='#94a3b8';ctx.lineWidth=1;
      for(i=1;i<nSub;i++){ ctx.beginPath();ctx.moveTo(BX+BW*i/nSub,70);ctx.lineTo(BX+BW*i/nSub,110);ctx.stroke(); }
      for(i=1;i<nSub2;i++){ ctx.beginPath();ctx.moveTo(BX+BW*i/nSub2,140);ctx.lineTo(BX+BW*i/nSub2,180);ctx.stroke(); }
    }
    lbl(ctx,(cut>0.2)?('둘 다 '+D+'등분으로 다시 자르기'):'두 조각의 크기가 다르다',BX,232,'#334155',17);
    var total=b+a;
    var showN=Math.round(total*merge);
    ctx.fillStyle='#f8fafc';ctx.fillRect(BX,246,BW,44);
    for(i=0;i<showN;i++){
      ctx.fillStyle=(i<b)?'#bfdbfe':'#bbf7d0';
      ctx.fillRect(BX+BW*i/D,246,BW/D,44);
    }
    ctx.strokeStyle='#9aa8bb';ctx.lineWidth=1;
    for(i=1;i<D;i++){ ctx.beginPath();ctx.moveTo(BX+BW*i/D,246);ctx.lineTo(BX+BW*i/D,290);ctx.stroke(); }
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;ctx.strokeRect(BX,246,BW,44);
    lbl(ctx,'합',BX-8,274,'#334155',17,'right');
    var rr=red(a+b,D);
    box(ctx,20,306,400,108);
    lbl(ctx,'1/'+a+' + 1/'+b,38,338,'#1f2937',22);
    lbl(ctx,'분모끼리 더하면 → 1/'+(a+b),38,368,'#b91c1c',18);
    lbl(ctx,(t===null)?'실제 합은?':('실제 합 → '+(b)+'/'+D+' + '+(a)+'/'+D+' = '+fstr(a+b,D)+((rr[1]!==D)?(' = '+fstr(rr[0],rr[1])):'')),
        38,396,'#15803d',18);
  },
  record:function(S){
    var a=S.a,b=S.b,D=a*b,N=a+b;
    var rr=red(N,D);
    return {a:a,b:b,wrong:'1/'+(a+b),wv:r3(1/(a+b)),
            real:fstr(rr[0],rr[1]),rv:r3(N/D),
            bigPart:r3(1/Math.min(a,b)),smallPart:r3(1/Math.max(a,b))};
  },
  headA:['번호','식','분모끼리 더한 답','그 값','실제 합','그 값','같은가?'],
  rowA:function(r,i){
    var same=(Math.abs(r.wv-r.rv)<0.0005);
    return [i+1,'1/'+r.a+' + 1/'+r.b,r.wrong,r.wv,'<b>'+r.real+'</b>',r.rv,
            '<span class="'+(same?'ok':'no')+'">'+(same?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],wrongOk=0,bigger=0,smaller=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var same=(Math.abs(r.wv-r.rv)<0.0005);
      var gt=(r.rv>r.bigPart+0.0005);
      var lt=(r.wv<r.smallPart-0.0005);
      if(same) wrongOk++;
      if(gt) bigger++;
      if(lt) smaller++;
      rows.push(['1/'+r.a+' + 1/'+r.b, r.wrong+' ('+r.wv+')', '<b>'+r.real+' ('+r.rv+')</b>',
                 '<span class="'+(same?'ok':'no')+'">'+(same?'○':'×')+'</span>',
                 '<span class="'+(gt?'ok':'no')+'">'+(gt?'○':'×')+'</span>',
                 '<span class="'+(lt?'ok':'no')+'">'+(lt?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'분모끼리 더한 답이 맞은 횟수',big:wrongOk+' / '+rec.length,
       p:'1/2 + 1/3 = 2/5 처럼 계산하면 어떻게 되는지 확인한 결과.'},
      {t:'실제 합이 두 분수보다 컸던 횟수',big:bigger+' / '+rec.length,
       p:'무언가를 더했으니 합은 각각보다 커야 한다.'},
      {t:'분모끼리 더한 답이 오히려 작았던 횟수',big:smaller+' / '+rec.length,
       p:'분모가 커지면 조각이 작아지기 때문이다.'}
    ];
    var concl;
    if(wrongOk===0 && bigger===rec.length){
      concl='<b>정리</b> — 분모끼리 더한 답은 <b>한 번도 맞지 않았고</b>, 오히려 더한 두 분수보다 <b>작아졌다.</b> '
           +'분모는 “조각의 크기”를 말하는 자리라서 더할 수 없다. 조각 크기를 같게 맞춘 뒤(통분) <b>분자만 더해야</b> 한다.';
    } else if(wrongOk>0){
      concl='<b>확인 필요</b> — 분모끼리 더한 답이 맞은 기록이 있다. 값을 다시 확인해 보자.';
    } else {
      concl='<b>정리</b> — 분모끼리 더하는 방법은 맞지 않았다. 조각 크기를 같게 만든 뒤 분자만 더해야 한다.';
    }
    return {head:['식','분모끼리 더한 답','실제 합','같은가?','합이 각각보다 큰가?','잘못된 답이 더 작은가?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 곱하면 항상 커질까
# ============================================================
LAB_MUL_SIZE = BASE + r"""
var LAB = {
  cw:440, ch:420, cvTitle:'넓이 모델판',
  action:'직사각형 만들어 보기',
  hint0:'가로와 세로를 정해 직사각형을 만들고, 넓이가 가로보다 커지는지 확인해 보자.',
  sliders:[
    {id:'a',label:'처음 수 (가로)',min:1,max:30,value:20,color:'#2563eb',
     fmt:function(v){return (v/10).toFixed(1);}},
    {id:'b',label:'곱하는 수 (세로)',min:1,max:30,value:6,color:'#f59e0b',
     fmt:function(v){return (v/10).toFixed(1);}}
  ],
  readout:function(S,ran){
    var A=S.a/10,B=S.b/10;
    return [{k:'식',v:A.toFixed(1)+' × '+B.toFixed(1)},
            {k:'결과',v:ran?r3(A*B):'만들어 보자'}];
  },
  doneMsg:function(S){
    var A=S.a/10,B=S.b/10,P=r3(A*B);
    var cmp=(P>A)?'커졌다':((P<A)?'오히려 작아졌다':'그대로다');
    return A.toFixed(1)+' × '+B.toFixed(1)+' = '+P+' — 처음 수 '+A.toFixed(1)+'보다 '+cmp+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var A=S.a/10, B=S.b/10, U=96, OXx=64, OYy=300, i;
    var grow=(t===null)?0:Math.min(1,t);
    for(i=0;i<=3;i++){
      ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
      ctx.beginPath();ctx.moveTo(OXx+i*U,OYy);ctx.lineTo(OXx+i*U,OYy-3*U);ctx.stroke();
      ctx.beginPath();ctx.moveTo(OXx,OYy-i*U);ctx.lineTo(OXx+3*U,OYy-i*U);ctx.stroke();
    }
    ctx.strokeStyle='#94a3b8';ctx.setLineDash([5,5]);ctx.lineWidth=2;
    ctx.strokeRect(OXx,OYy-U,A*U,U);
    ctx.setLineDash([]);
    ctx.fillStyle='rgba(245,158,11,0.30)';
    ctx.fillRect(OXx,OYy-B*U*grow,A*U,B*U*grow);
    ctx.strokeStyle='#d97706';ctx.lineWidth=3;
    ctx.strokeRect(OXx,OYy-B*U*grow,A*U,B*U*grow);
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(OXx,OYy);ctx.lineTo(OXx+3*U+10,OYy);ctx.moveTo(OXx,OYy);ctx.lineTo(OXx,OYy-3*U-10);ctx.stroke();
    lbl(ctx,'가로 '+A.toFixed(1),OXx+A*U/2,OYy+22,'#1d4ed8',16,'center');
    lbl(ctx,'세로 '+B.toFixed(1),OXx-10,OYy-B*U*grow/2,'#b45309',16,'right');
    lbl(ctx,'점선 = 세로가 1일 때 (넓이 '+A.toFixed(1)+')',24,36,'#64748b',16);
    box(ctx,20,326,400,80);
    var P=r3(A*B);
    lbl(ctx,(t===null)?(A.toFixed(1)+' × '+B.toFixed(1)+' = ?'):(A.toFixed(1)+' × '+B.toFixed(1)+' = '+P),38,358,'#1f2937',22);
    if(t!==null){
      var cmp=(P>A)?'처음 수보다 커졌다':((P<A)?'처음 수보다 작아졌다':'처음 수와 같다');
      lbl(ctx,cmp+'   (곱하는 수 '+B.toFixed(1)+(B>1?' > 1)':(B<1?' < 1)':' = 1)')),38,388,(P<A)?'#b91c1c':'#15803d',18);
    } else {
      lbl(ctx,'곱하면 항상 커질까?',38,388,'#52627a',18);
    }
  },
  record:function(S){
    var A=S.a/10,B=S.b/10,P=r3(A*B);
    return {a:r1(A),b:r1(B),p:P,bigger:(P>A+1e-9),same:(Math.abs(P-A)<1e-9),bgt1:(B>1),beq1:(Math.abs(B-1)<1e-9)};
  },
  headA:['번호','식','결과','처음 수보다','곱하는 수'],
  rowA:function(r,i){
    var s=r.same?'그대로':(r.bigger?'커짐':'작아짐');
    return [i+1,r.a+' × '+r.b,'<b>'+r.p+'</b>',
            '<span class="'+(r.bigger?'ok':(r.same?'':'no'))+'">'+s+'</span>',
            r.beq1?'= 1':(r.bgt1?'> 1':'< 1')];
  },
  analyze:function(rec){
    var rows=[],claim=0,lt1=0,lt1small=0,gt1=0,gt1big=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.bigger) claim++;
      if(!r.bgt1 && !r.beq1){ lt1++; if(!r.bigger && !r.same) lt1small++; }
      if(r.bgt1){ gt1++; if(r.bigger) gt1big++; }
      rows.push([r.a+' × '+r.b, r.p, r.beq1?'= 1':(r.bgt1?'> 1':'< 1'),
                 r.same?'그대로':(r.bigger?'커짐':'작아짐'),
                 '<span class="'+(r.bigger?'ok':'no')+'">'+(r.bigger?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'“곱하면 커진다”가 맞은 횟수',big:claim+' / '+rec.length,
       p:'결과가 처음 수보다 컸던 기록의 수.'},
      {t:'1보다 작은 수를 곱한 기록',big:lt1+'개',
       p:lt1?('그중 결과가 작아진 것 '+lt1small+'개.'):'0.6처럼 1보다 작은 수를 곱해 보자.'},
      {t:'1보다 큰 수를 곱한 기록',big:gt1+'개',
       p:gt1?('그중 결과가 커진 것 '+gt1big+'개.'):'1보다 큰 수도 곱해 보자.'}
    ];
    var concl;
    if(lt1===0){
      concl='<b>더 해 보자</b> — 아직 1보다 작은 수를 곱한 기록이 없다. 2.0 × 0.6처럼 곱해 보면 결과가 어떻게 되는지 확인할 수 있다.';
    } else if(lt1small===lt1 && gt1big===gt1){
      concl='<b>정리</b> — 곱하면 항상 커지는 것이 아니었다. <b>1보다 작은 수를 곱하면 '+lt1+'번 모두 작아졌다.</b> '
           +'세로가 1보다 짧으면 직사각형이 가로 길이보다 좁아지기 때문이다. 곱하는 수가 1보다 크면 커지고, 1이면 그대로, 1보다 작으면 작아진다.';
    } else {
      concl='<b>확인 필요</b> — 규칙과 어긋난 기록이 있다. 값을 다시 확인해 보자.';
    }
    return {head:['식','결과','곱하는 수','처음 수와 비교','커졌나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 소수의 곱셈과 소수점
# ============================================================
LAB_DEC_MUL = BASE + r"""
function dv(n,d){ return n/Math.pow(10,d); }
function dstr(n,d){ return dv(n,d).toFixed(d); }
function decCount(x){
  var s=String(x);
  var p=s.indexOf('.');
  return (p<0)?0:(s.length-p-1);
}
var LAB = {
  cw:440, ch:400, cvTitle:'소수점 이동판',
  action:'정수처럼 곱하고 소수점 옮기기',
  hint0:'두 소수를 정하고, 정수처럼 곱한 뒤 소수점을 옮겨 보자.',
  sliders:[
    {id:'a',label:'첫 번째 수의 숫자',min:1,max:999,value:25,color:'#2563eb',unit:''},
    {id:'da',label:'첫 번째 수의 소수 자릿수',min:0,max:3,value:1,color:'#60a5fa',unit:'자리'},
    {id:'b',label:'두 번째 수의 숫자',min:1,max:999,value:4,color:'#16a34a',unit:''},
    {id:'db',label:'두 번째 수의 소수 자릿수',min:0,max:3,value:1,color:'#4ade80',unit:'자리'}
  ],
  readout:function(S,ran){
    var ip=S.a*S.b, k=S.da+S.db;
    return [{k:'식',v:dstr(S.a,S.da)+' × '+dstr(S.b,S.db)},
            {k:'결과',v:ran?String(r3(dv(ip,k))):'계산해 보자'}];
  },
  doneMsg:function(S){
    var ip=S.a*S.b, k=S.da+S.db;
    return '정수처럼 곱하면 '+ip+', 소수점을 왼쪽으로 '+k+'칸 옮기면 '+dv(ip,k).toFixed(k)+'이다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var ip=S.a*S.b, k=S.da+S.db, i;
    lbl(ctx,'소수 곱셈, 소수점은 어디로?',24,40,'#1d4ed8',19);
    lbl(ctx,dstr(S.a,S.da)+'  (소수 '+S.da+'자리)',40,92,'#1d4ed8',22);
    lbl(ctx,'×  '+dstr(S.b,S.db)+'  (소수 '+S.db+'자리)',40,128,'#15803d',22);
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(40,142);ctx.lineTo(400,142);ctx.stroke();
    var p1=(t===null)?0:Math.min(1,t/0.4);
    var p2=(t===null)?0:Math.max(0,(t-0.4)/0.6);
    if(p1>0){
      lbl(ctx,'정수처럼 곱하면  '+S.a+' × '+S.b+' = '+ip,40,180,'#334155',20);
    }
    var str=String(ip);
    ctx.font='bold 34px sans-serif';ctx.textAlign='left';
    var cw=22, sx=54;
    if(p1>0){
      for(i=0;i<str.length;i++){
        ctx.fillStyle='#1f2937';
        ctx.fillText(str.charAt(i),sx+i*cw,254);
      }
    }
    if(p2>0){
      var from=sx+str.length*cw;
      var to=sx+(str.length-k)*cw;
      var x=from+(to-from)*p2;
      ctx.fillStyle='#dc2626';ctx.font='bold 40px sans-serif';
      ctx.fillText('.',x-3,258);
      ctx.strokeStyle='#dc2626';ctx.lineWidth=2;
      ctx.beginPath();ctx.moveTo(from,272);ctx.lineTo(x,272);ctx.stroke();
      lbl(ctx,'왼쪽으로 '+S.da+' + '+S.db+' = '+k+'칸',sx,296,'#b91c1c',17);
    }
    ctx.font='bold 18px sans-serif';
    box(ctx,20,312,400,72);
    lbl(ctx,(t===null)?'소수점은 몇 칸 옮겨야 할까?':('결과 : '+dv(ip,k).toFixed(k)),38,344,'#1f2937',21);
    lbl(ctx,'소수 자릿수 : '+S.da+' + '+S.db+' = '+k+'자리',38,372,'#52627a',18);
  },
  record:function(S){
    var ip=S.a*S.b, k=S.da+S.db;
    var res=dv(ip,k);
    var real=dv(S.a,S.da)*dv(S.b,S.db);
    var naive=dv(ip,Math.max(S.da,S.db));
    return {v1:dstr(S.a,S.da),v2:dstr(S.b,S.db),ip:ip,k:k,
            res:Number(res.toFixed(6)),ok:(Math.abs(res-real)<1e-9),
            naive:Number(naive.toFixed(6)),naiveOk:(Math.abs(naive-real)<1e-9),
            shown:decCount(Number(res.toFixed(6)))};
  },
  headA:['번호','식','정수처럼 곱한 값','옮길 칸 수','결과','실제 곱과 같은가?','더 많은 쪽 자릿수만 옮기면'],
  rowA:function(r,i){
    return [i+1,r.v1+' × '+r.v2,r.ip,r.k+'칸','<b>'+r.res+'</b>',
            '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
            r.naive+' <span class="'+(r.naiveOk?'ok':'no')+'">'+(r.naiveOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ok=0,nok=0,zeroCut=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.ok) ok++;
      if(r.naiveOk) nok++;
      var cut=(r.shown<r.k);
      if(cut) zeroCut++;
      rows.push([r.v1+' × '+r.v2, r.ip, r.k+'칸', '<b>'+r.res+'</b>',
                 '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
                 r.naive,
                 '<span class="'+(r.naiveOk?'ok':'no')+'">'+(r.naiveOk?'○':'×')+'</span>',
                 cut?('끝자리 0 (표기 '+r.shown+'자리)'):'-']);
    }
    var stats=[
      {t:'“자릿수를 더한 만큼 옮기기”가 맞은 횟수',big:ok+' / '+rec.length,
       p:'두 수의 소수 자릿수를 더한 칸만큼 옮긴 결과.'},
      {t:'“더 많은 쪽만큼 옮기기”가 맞은 횟수',big:nok+' / '+rec.length,
       p:'두 자릿수 중 큰 쪽만큼만 옮기면 어떻게 되는지 확인했다.'},
      {t:'끝자리가 0이라 짧게 쓰인 기록',big:zeroCut+'개',
       p:zeroCut?'0.2 × 0.5 = 0.10 → 0.1처럼 표기 자릿수가 줄어든 경우다. 옮긴 칸 수는 그대로다.':'0.2 × 0.5처럼 끝이 0이 되는 곱도 해 보자.'}
    ];
    var concl;
    if(ok===rec.length && nok<rec.length){
      concl='<b>정리</b> — 두 수의 소수 자릿수를 <b>더한 만큼</b> 소수점을 옮긴 답은 언제나 맞았고, 큰 쪽만큼만 옮긴 답은 틀렸다. '
           +'0.1은 1/10이므로 0.1 × 0.1 = 1/100, 곧 소수점이 두 칸 옮겨간다. '
           +(zeroCut?'끝자리가 0이면 짧게 쓰지만(0.10 → 0.1) 옮긴 칸 수 자체는 변하지 않는다.':'');
    } else if(ok===rec.length){
      concl='<b>정리</b> — 자릿수를 더한 만큼 옮기는 방법은 항상 맞았다. 두 수의 자릿수가 다른 경우도 기록해 두 방법을 구별해 보자.';
    } else {
      concl='<b>확인 필요</b> — 규칙과 다른 기록이 있다. 값을 다시 확인해 보자.';
    }
    return {head:['식','정수 곱','옮길 칸','결과','맞나?','큰 쪽만 옮기면','맞나?','비고'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 비와 비율
# ============================================================
LAB_RATIO = BASE + r"""
var LAB = {
  cw:440, ch:420, cvTitle:'비율 비교판',
  action:'비를 간단히 하고 비율 구하기',
  hint0:'두 묶음의 개수를 정하고, 비와 비율을 구해 보자.',
  sliders:[
    {id:'a',label:'빨간 구슬',min:1,max:20,value:4,color:'#dc2626',unit:'개'},
    {id:'b',label:'파란 구슬',min:1,max:20,value:6,color:'#2563eb',unit:'개'}
  ],
  readout:function(S,ran){
    var g=gcd(S.a,S.b);
    return [{k:'비',v:S.a+' : '+S.b},
            {k:'간단히 한 비',v:ran?((S.a/g)+' : '+(S.b/g)):'구해 보자'}];
  },
  doneMsg:function(S){
    var g=gcd(S.a,S.b);
    return S.a+' : '+S.b+' 를 간단히 하면 '+(S.a/g)+' : '+(S.b/g)+', 비율은 '+r3(S.a/S.b)+'이다. 개수를 바꿔 같은 비율을 찾아보자.';
  },
  draw:function(ctx,S,t,ran){
    var g=gcd(S.a,S.b), i;
    var group=(t===null)?0:Math.min(1,t);
    lbl(ctx,'빨강 '+S.a+'개, 파랑 '+S.b+'개',24,38,'#1d4ed8',19);
    function row(y,n,col,gn){
      for(i=0;i<n;i++){
        var per=10;
        var x=40+(i%per)*30, yy=y+Math.floor(i/per)*30;
        var gi=Math.floor(i/gn);
        var shift=group*(gi*10);
        ctx.beginPath();ctx.arc(x+shift,yy,11,0,Math.PI*2);
        ctx.fillStyle=col;ctx.fill();
        ctx.strokeStyle='#1f2937';ctx.lineWidth=1.6;ctx.stroke();
      }
    }
    row(80,S.a,'#ef4444',S.a/g);
    row(160,S.b,'#3b82f6',S.b/g);
    if(group>0.3){
      lbl(ctx,g+'개씩 묶음으로 나누면  빨강 '+(S.a/g)+'묶음, 파랑 '+(S.b/g)+'묶음',24,232,'#334155',17);
    }
    var BX=40, BW=360;
    var tot=S.a+S.b;
    ctx.fillStyle='#ef4444';ctx.fillRect(BX,252,BW*S.a/tot,32);
    ctx.fillStyle='#3b82f6';ctx.fillRect(BX+BW*S.a/tot,252,BW*S.b/tot,32);
    ctx.strokeStyle='#334155';ctx.lineWidth=2;ctx.strokeRect(BX,252,BW,32);
    lbl(ctx,'전체에서 빨강이 차지하는 비율 : '+r3(S.a/tot),BX,304,'#52627a',17);
    box(ctx,20,318,400,86);
    lbl(ctx,(t===null)?(S.a+' : '+S.b+' 는 얼마나 간단해질까?'):(S.a+' : '+S.b+'  =  '+(S.a/g)+' : '+(S.b/g)),38,350,'#1f2937',22);
    lbl(ctx,(t===null)?'':('빨강 ÷ 파랑 = '+r3(S.a/S.b)+'    (최대공약수 '+g+')'),38,382,'#15803d',18);
  },
  record:function(S){
    var g=gcd(S.a,S.b);
    return {a:S.a,b:S.b,g:g,sa:S.a/g,sb:S.b/g,
            ratio:r3(S.a/S.b),
            dbl:r3((2*S.a)/(2*S.b)),
            part:r3(S.a/(S.a+S.b))};
  },
  headA:['번호','비','최대공약수','간단히 한 비','비율(빨강÷파랑)','2배 한 비의 비율','전체 중 빨강 비율'],
  rowA:function(r,i){
    return [i+1,r.a+' : '+r.b,r.g,'<b>'+r.sa+' : '+r.sb+'</b>',r.ratio,r.dbl,r.part];
  },
  analyze:function(rec){
    var rows=[],dblOk=0,map={},pairs=0,agree=0,i;
    for(i=0;i<rec.length;i++){
      var r=rec[i];
      var d=(Math.abs(r.ratio-r.dbl)<0.0005);
      if(d) dblOk++;
      var k=r.sa+':'+r.sb, note='첫 기록';
      if(map[k]!==undefined){
        pairs++;
        var same=(Math.abs(map[k]-r.ratio)<0.0005);
        if(same) agree++;
        note='<span class="'+(same?'ok':'no')+'">'+(same?'비율 같음':'비율 다름')+'</span>';
      } else { map[k]=r.ratio; }
      rows.push([r.a+' : '+r.b, r.sa+' : '+r.sb, r.ratio, r.dbl,
                 '<span class="'+(d?'ok':'no')+'">'+(d?'○':'×')+'</span>', note]);
    }
    var stats=[
      {t:'2배 해도 비율이 같았던 횟수',big:dblOk+' / '+rec.length,
       p:'두 수를 똑같이 늘려도 비율은 그대로였는지 확인한 결과.'},
      {t:'간단히 한 비가 같았던 짝',big:pairs+'쌍',
       p:pairs?'개수는 다른데 간단히 한 비가 같은 기록을 찾았다.':'2:3과 4:6처럼 개수만 다른 짝을 기록해 보자.'},
      {t:'그때 비율도 같았던 짝',big:pairs?(agree+' / '+pairs):'비교 없음',
       p:'양이 달라도 비율이 같은지 확인한 결과.'}
    ];
    var concl;
    if(pairs===0){
      concl='<b>더 해 보자</b> — 아직 간단히 한 비가 같은 짝이 없다. 2:3과 4:6, 6:9처럼 개수만 다르게 기록해 비교해 보자.';
    } else if(agree===pairs && dblOk===rec.length){
      concl='<b>정리</b> — 구슬 수가 4:6이든 6:9든 간단히 하면 같은 2:3이었고, <b>비율도 완전히 같았다.</b> '
           +'비는 “몇 개인가”가 아니라 <b>몇 배인가</b>를 나타낸다. 그래서 양이 달라도 비율이 같으면 같은 관계다.';
    } else {
      concl='<b>확인 필요</b> — 간단히 한 비는 같은데 비율이 다른 기록이 있다. 값을 다시 확인해 보자.';
    }
    return {head:['비','간단히 한 비','비율','2배 한 비의 비율','같은가?','간단히 한 비가 같은 기록끼리'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("elem56_lcm_lab.html",
     "배수 만나기 실험실 — 두 수의 곱이 최소공배수일까?",
     "배수 만나기 실험실 — 두 수의 곱이 최소공배수일까?",
     "두 수의 배수를 차례로 놓아 처음 만나는 수를 찾고, 두 수의 곱·최대공약수와 어떤 관계인지 기록한다.",
     LAB_LCM),
    ("elem56_fraction_addition_lab.html",
     "분수 덧셈 실험실 — 분모끼리 더하면 될까?",
     "분수 덧셈 실험실 — 분모끼리 더하면 될까?",
     "두 단위분수를 같은 크기 조각으로 다시 잘라 더하고, 분모끼리 더한 답과 비교한다.",
     LAB_FRAC_ADD),
    ("elem56_multiplication_size_lab.html",
     "넓이 모델 실험실 — 곱하면 항상 커질까?",
     "넓이 모델 실험실 — 곱하면 항상 커질까?",
     "가로와 세로를 바꿔 직사각형을 만들며, 곱한 결과가 처음 수보다 커지는지 작아지는지 기록한다.",
     LAB_MUL_SIZE),
    ("elem56_decimal_multiplication_lab.html",
     "소수점 실험실 — 소수점은 몇 칸 옮길까?",
     "소수점 실험실 — 소수점은 몇 칸 옮길까?",
     "소수를 정수처럼 곱한 뒤 소수점을 옮기며, 옮길 칸 수를 정하는 규칙을 확인한다.",
     LAB_DEC_MUL),
    ("elem56_ratio_lab.html",
     "비율 실험실 — 개수가 다르면 비율도 다를까?",
     "비율 실험실 — 개수가 다르면 비율도 다를까?",
     "두 묶음의 개수를 바꿔 가며 비를 간단히 하고, 양이 달라도 비율이 같아지는 경우를 찾는다.",
     LAB_RATIO),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c5_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
