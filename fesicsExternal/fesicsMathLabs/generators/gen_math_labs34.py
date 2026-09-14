# -*- coding: utf-8 -*-
"""고등 미적분Ⅱ — 삼각함수 극한·미분법 3종 + 활용 2종"""
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
"""

# ============================================================
# 1. sin x / x 의 극한
# ============================================================
LAB_SINX = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'삼각함수 극한판',
  action:'0에 다가가기',
  hint0:'x를 얼마나 0에 가깝게 할지 정해 보자. (라디안)',
  sliders:[
    {id:'x0',label:'x (÷1000)',min:1,max:1500,value:500,color:'#2563eb',
     fmt:function(v){return (v/1000).toFixed(3);}}
  ],
  calc:function(S){
    var x=S.x0/1000;
    return {x:x,s:Math.sin(x)/x,
            c:(1-Math.cos(x))/x,
            tn:Math.tan(x)/x,
            deg:Math.sin(x*Math.PI/180)/x};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'sin x / x',v:ran?r6(c.s):'다가가 보자'},
            {k:'(1 − cos x) / x',v:ran?r6(c.c):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'x = '+c.x+' 에서 sin x / x = '+r6(c.s)+', (1−cos x)/x = '+r6(c.c)+'다. x를 더 줄여 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var GX=50, GY=250, GW=340, GH=170;
    var lo=0, hi=1.6;
    function px(x){ return GX+GW*x/hi; }
    function py(v){ return GY-(v-0)/(1.3)*GH; }
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=0;i<=13;i++){
      ctx.beginPath();ctx.moveTo(GX,py(i/10));ctx.lineTo(GX+GW,py(i/10));ctx.stroke();
    }
    ctx.strokeStyle='#7c3aed';ctx.lineWidth=2;ctx.setLineDash([5,4]);
    ctx.beginPath();ctx.moveTo(GX,py(1));ctx.lineTo(GX+GW,py(1));ctx.stroke();ctx.setLineDash([]);
    lbl(ctx,'1',GX-16,py(1)+4,'#6d28d9',13);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    for(i=1;i<=160;i++){
      var x=i/100;
      var v=Math.sin(x)/x;
      if(i===1) ctx.moveTo(px(x),py(v)); else ctx.lineTo(px(x),py(v));
    }
    ctx.stroke();
    ctx.strokeStyle='#f59e0b';ctx.lineWidth=2.4;ctx.beginPath();
    for(i=1;i<=160;i++){
      var x2=i/100;
      var v2=(1-Math.cos(x2))/x2;
      if(i===1) ctx.moveTo(px(x2),py(v2)); else ctx.lineTo(px(x2),py(v2));
    }
    ctx.stroke();
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+GW,GY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(GX,GY-GH-8);ctx.lineTo(GX,GY+8);ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      var cur=c.x+(1.5-c.x)*(1-grow);
      var vv=Math.sin(cur)/cur;
      ctx.beginPath();ctx.arc(px(cur),py(vv),7,0,Math.PI*2);
      ctx.fillStyle='#dc2626';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
    }
    lbl(ctx,'파랑 = sin x / x,   주황 = (1 − cos x) / x',24,32,'#334155',15);
    box(ctx,20,286,400,130);
    lbl(ctx,'x = '+c.x+' (라디안)',38,318,'#52627a',17);
    lbl(ctx,(t===null)?'0에 다가가면 어디로 갈까?':('sin x / x = '+r6(c.s)),38,352,'#1f2937',18);
    lbl(ctx,(t===null)?'':('(1 − cos x) / x = '+r6(c.c)+'      tan x / x = '+r6(c.tn)),38,386,'#52627a',16);
    lbl(ctx,(t===null)?'':('x를 «도»로 보면 sin x° / x = '+r6(c.deg)),38,412,'#b91c1c',14);
  },
  record:function(S){
    var c=this.calc(S);
    return {x:c.x,s:r6(c.s),c:r6(c.c),tn:r6(c.tn),deg:r6(c.deg),
            near1:(Math.abs(c.s-1)<0.001),
            near0:(Math.abs(c.c)<0.001),
            degOne:(Math.abs(c.deg-1)<0.001)};
  },
  headA:['번호','x','sin x / x','1에 가깝나?','(1−cos x)/x','0에 가깝나?','tan x / x','도로 볼 때'],
  rowA:function(r,i){
    return [i+1,r.x,'<b>'+r.s+'</b>',
            '<span class="'+(r.near1?'ok':'no')+'">'+(r.near1?'○':'×')+'</span>',
            r.c,
            '<span class="'+(r.near0?'ok':'no')+'">'+(r.near0?'○':'×')+'</span>',
            r.tn,r.deg];
  },
  analyze:function(rec){
    var rows=[],n1=0,n0=0,dg=0,arr=[],mono=true;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.near1) n1++;
      if(r.near0) n0++;
      if(r.degOne) dg++;
      arr.push([parseFloat(r.x),Math.abs(parseFloat(r.s)-1)]);
      rows.push([r.x, '<b>'+r.s+'</b>',
                 '<span class="'+(r.near1?'ok':'no')+'">'+(r.near1?'○':'×')+'</span>',
                 r.c,
                 '<span class="'+(r.near0?'ok':'no')+'">'+(r.near0?'○':'×')+'</span>',
                 r.tn, r.deg]);
    }
    arr.sort(function(x,y){return x[0]-y[0];});
    for(i=1;i<arr.length;i++){ if(arr[i][1]<arr[i-1][1]-1e-12) mono=false; }
    var stats=[
      {t:'sin x / x 가 1에 가까웠던 횟수',big:n1+' / '+rec.length,p:'차이가 0.001 이내였던 기록 수.'},
      {t:'(1 − cos x)/x 가 0에 가까웠던 횟수',big:n0+' / '+rec.length,p:'같은 0/0 꼴인데 극한이 다르다.'},
      {t:'x가 작을수록 1에 가까워짐',big:(arr.length<2)?'비교 없음':(mono?'그렇다':'들쭉날쭉'),
       p:'도 단위로 보면 1이 된 기록 '+dg+'개.'}
    ];
    var concl;
    if(arr.length<3){
      concl='<b>더 해 보자</b> — x를 1.5, 0.5, 0.1, 0.01 처럼 줄여 가며 기록해 보자.';
    } else if(n1>0&&n0>0){
      concl='<b>정리</b> — x → 0 일 때 <b>sin x / x 는 1</b>에 다가갔지만, 같은 0/0 꼴인 (1 − cos x)/x 는 <b>0</b>으로 갔다. '
           +'꼴이 같아도 극한은 다르다. 또 이 값이 1이 되는 것은 <b>라디안일 때뿐</b>이다. '
           +'도 단위로 재면 sin x°/x 는 π/180 ≒ 0.01745 로 간다. 미적분에서 라디안을 쓰는 이유다.';
    } else {
      concl='<b>정리</b> — x를 더 작게 해서 두 극한이 각각 어디로 가는지 확인해 보자.';
    }
    return {head:['x','sin x/x','1에 가깝나?','(1−cos x)/x','0에 가깝나?','tan x/x','도 단위'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 연쇄법칙
# ============================================================
LAB_CHAIN = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'연쇄법칙 판',
  action:'수치로 미분하기',
  hint0:'(ax + b)ⁿ 의 계수와 확인할 x를 정해 보자.',
  sliders:[
    {id:'a',label:'a',min:1,max:5,value:3,color:'#2563eb',unit:''},
    {id:'b',label:'b',min:-4,max:4,value:1,color:'#60a5fa',unit:''},
    {id:'n',label:'지수 n',min:2,max:5,value:3,color:'#16a34a',unit:''},
    {id:'x0',label:'x (÷10)',min:-10,max:20,value:10,color:'#dc2626',
     fmt:function(v){return (v/10).toFixed(1);}}
  ],
  calc:function(S){
    var x=S.x0/10, h=1e-6;
    function F(v){ return Math.pow(S.a*v+S.b,S.n); }
    var num=(F(x+h)-F(x-h))/(2*h);
    var inner=S.a*x+S.b;
    var chain=S.n*Math.pow(inner,S.n-1)*S.a;
    var wrong=S.n*Math.pow(inner,S.n-1);
    return {x:x,inner:inner,num:num,chain:chain,wrong:wrong};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'수치 미분값',v:ran?r4(c.num):'미분해 보자'},
            {k:'n(ax+b)ⁿ⁻¹ · a',v:ran?r4(c.chain):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '수치 미분 '+r4(c.num)+', 연쇄법칙 '+r4(c.chain)+', 안쪽 미분을 빠뜨리면 '+r4(c.wrong)+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var p1=(t===null)?0:Math.min(1,t/0.4);
    var p2=(t===null)?0:Math.max(0,Math.min(1,(t-0.4)/0.3));
    var p3=(t===null)?0:Math.max(0,(t-0.7)/0.3);
    lbl(ctx,'y = ('+S.a+'x'+sg(S.b)+')^'+S.n+'      x = '+c.x,24,42,'#1d4ed8',19);
    lbl(ctx,'안쪽 '+S.a+'x'+sg(S.b)+' = '+r3(c.inner),24,74,'#52627a',17);
    if(p1>0){
      ctx.globalAlpha=p1;
      lbl(ctx,'수치 미분 = '+r4(c.num),40,124,'#1f2937',24);
      ctx.globalAlpha=1;
    }
    if(p2>0){
      ctx.globalAlpha=p2;
      lbl(ctx,'바깥 미분 × 안쪽 미분',40,166,'#334155',16);
      lbl(ctx,S.n+'·('+r3(c.inner)+')^'+(S.n-1)+' × '+S.a+' = '+r4(c.chain),40,200,'#15803d',20);
      ctx.globalAlpha=1;
    }
    if(p3>0){
      ctx.globalAlpha=p3;
      lbl(ctx,'안쪽 미분을 빠뜨리면 : '+r4(c.wrong),40,244,'#b91c1c',20);
      ctx.globalAlpha=1;
    }
    box(ctx,20,264,400,120);
    lbl(ctx,(t===null)?'안쪽도 미분해야 할까?':('수치 미분 '+r4(c.num)),38,296,'#1f2937',18);
    lbl(ctx,(t===null)?'':('연쇄법칙 '+r4(c.chain)),38,330,'#15803d',18);
    lbl(ctx,(t===null)?'':('안쪽 미분 빠뜨림 '+r4(c.wrong)+'   (a = '+S.a+'배 차이)'),38,364,'#b91c1c',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,n:S.n,x:c.x,
            num:r4(c.num),chain:r4(c.chain),wrong:r4(c.wrong),
            ok:(Math.abs(c.num-c.chain)<1e-3*Math.max(1,Math.abs(c.num))),
            wOk:(Math.abs(c.num-c.wrong)<1e-3*Math.max(1,Math.abs(c.num))),
            aOne:(S.a===1),
            trivial:(S.a===1||Math.abs(c.num)<1e-9)};
  },
  headA:['번호','식','x','수치 미분','연쇄법칙','같나?','안쪽 미분 빠뜨림','같나?','a'],
  rowA:function(r,i){
    return [i+1,'('+r.a+'x'+sg(r.b)+')^'+r.n,r.x,'<b>'+r.num+'</b>',r.chain,
            '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
            r.wrong,
            '<span class="'+(r.wOk?'ok':'no')+'">'+(r.wOk?'○':'×')+'</span>',r.a];
  },
  analyze:function(rec){
    var rows=[],ok=0,w=0,one=0,aNot1=0,triv=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.ok) ok++;
      if(r.wOk){ w++; if(r.trivial) triv++; if(r.aOne) one++; }
      if(!r.aOne) aNot1++;
      rows.push(['('+r.a+'x'+sg(r.b)+')^'+r.n, r.x, '<b>'+r.num+'</b>', r.chain,
                 '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
                 r.wrong,
                 '<span class="'+(r.wOk?'ok':'no')+'">'+(r.wOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'연쇄법칙이 맞은 횟수',big:ok+' / '+rec.length,p:'바깥 미분 × 안쪽 미분과 수치 미분을 비교했다.'},
      {t:'안쪽 미분을 빠뜨린 값이 맞은 횟수',big:w+' / '+rec.length,
       p:w?('그중 a = 1 이거나 도함수가 0이었던 것 '+triv+'개.'):'a가 1이 아니면 반드시 틀린다.'},
      {t:'a ≠ 1 인 기록',big:aNot1+'개',p:'a배만큼 차이가 난다.'}
    ];
    var concl;
    if(aNot1===0){
      concl='<b>더 해 보자</b> — a를 1이 아닌 값으로 두고 기록해야 차이가 드러난다.';
    } else if(ok===rec.length&&w===triv){
      concl='<b>정리</b> — 합성함수의 도함수는 <b>바깥 함수의 미분 × 안쪽 함수의 미분</b>이었다. '
           +'안쪽 미분 a 를 빠뜨리면 정확히 <b>a배만큼</b> 어긋났고, 맞은 것은 a = 1 이거나 도함수가 0이라 배수가 의미 없는 경우뿐이었다. '
           +'x가 조금 변할 때 안쪽이 a배로 변하고 그것이 다시 바깥으로 전달되기 때문이다.';
    } else {
      concl='<b>확인 필요</b> — 수치 미분과 공식이 어긋난 기록이 있다.';
    }
    return {head:['식','x','수치 미분','연쇄법칙','같나?','빠뜨림','같나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 몫의 미분법
# ============================================================
LAB_QUOT = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'몫의 미분 판',
  action:'수치로 미분하기',
  hint0:'분자와 분모의 계수, 확인할 x를 정해 보자.',
  sliders:[
    {id:'a',label:'분자 ax + b 의 a',min:-4,max:4,value:2,color:'#2563eb',unit:''},
    {id:'b',label:'분자의 b',min:-4,max:4,value:1,color:'#60a5fa',unit:''},
    {id:'c',label:'분모 cx + 1 의 c',min:-4,max:4,value:1,color:'#dc2626',unit:''},
    {id:'x0',label:'x (÷10)',min:5,max:30,value:15,color:'#f59e0b',
     fmt:function(v){return (v/10).toFixed(1);}}
  ],
  calc:function(S){
    var x=S.x0/10, h=1e-6;
    function F(v){ return (S.a*v+S.b)/(S.c*v+1); }
    var den=S.c*x+1;
    if(Math.abs(den)<1e-6) return {bad:true,x:x};
    var num=(F(x+h)-F(x-h))/(2*h);
    var f=S.a*x+S.b, g=den, fp=S.a, gp=S.c;
    return {bad:false,x:x,num:num,
            right:(fp*g-f*gp)/(g*g),
            wrong:(gp===0)?null:(fp/gp),
            f:f,g:g};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    if(c.bad) return [{k:'분모 0',v:'x를 바꾸자'},{k:'',v:''}];
    return [{k:'수치 미분값',v:ran?r4(c.num):'미분해 보자'},
            {k:'(f′g − fg′)/g²',v:ran?r4(c.right):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.bad) return '분모가 0이 되는 x다. 값을 바꿔 보자.';
    return '수치 미분 '+r4(c.num)+', 몫의 법칙 '+r4(c.right)+', f′/g′ = '+((c.wrong===null)?'-':r4(c.wrong))+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    if(c.bad){ lbl(ctx,'분모가 0이 되는 x다',24,200,'#b91c1c',20); return; }
    var p1=(t===null)?0:Math.min(1,t/0.4);
    var p2=(t===null)?0:Math.max(0,Math.min(1,(t-0.4)/0.3));
    var p3=(t===null)?0:Math.max(0,(t-0.7)/0.3);
    lbl(ctx,'y = ('+S.a+'x'+sg(S.b)+') / ('+S.c+'x + 1)      x = '+c.x,24,42,'#1d4ed8',17);
    lbl(ctx,'f = '+r3(c.f)+',  g = '+r3(c.g)+',  f′ = '+S.a+',  g′ = '+S.c,24,74,'#52627a',16);
    if(p1>0){ ctx.globalAlpha=p1; lbl(ctx,'수치 미분 = '+r4(c.num),40,124,'#1f2937',24); ctx.globalAlpha=1; }
    if(p2>0){
      ctx.globalAlpha=p2;
      lbl(ctx,"(f′g − fg′) / g² = "+r4(c.right),40,176,'#15803d',22);
      ctx.globalAlpha=1;
    }
    if(p3>0){
      ctx.globalAlpha=p3;
      lbl(ctx,"f′ / g′ = "+((c.wrong===null)?'정의 안 됨':r4(c.wrong)),40,222,'#b91c1c',22);
      ctx.globalAlpha=1;
    }
    box(ctx,20,248,400,136);
    lbl(ctx,(t===null)?"(f/g)′ = f′/g′ 일까?":('수치 미분 '+r4(c.num)),38,280,'#1f2937',18);
    lbl(ctx,(t===null)?'':("(f′g − fg′)/g² = "+r4(c.right)),38,314,'#15803d',18);
    lbl(ctx,(t===null)?'':("f′/g′ = "+((c.wrong===null)?'-':r4(c.wrong))),38,348,'#b91c1c',18);
  },
  record:function(S){
    var c=this.calc(S);
    if(c.bad) return {bad:true};
    return {bad:false,a:S.a,b:S.b,c:S.c,x:c.x,
            num:r4(c.num),right:r4(c.right),
            wrong:(c.wrong===null)?'-':r4(c.wrong),
            ok:(Math.abs(c.num-c.right)<1e-3*Math.max(1,Math.abs(c.num))),
            wOk:(c.wrong!==null&&Math.abs(c.num-c.wrong)<1e-3*Math.max(1,Math.abs(c.num)))};
  },
  headA:['번호','식','x','수치 미분','(f′g−fg′)/g²','같나?','f′/g′','같나?'],
  rowA:function(r,i){
    if(r.bad) return [i+1,'분모 0','-','-','-','-','-','-'];
    return [i+1,'('+r.a+'x'+sg(r.b)+')/('+r.c+'x+1)',r.x,'<b>'+r.num+'</b>',r.right,
            '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
            r.wrong,
            '<span class="'+(r.wOk?'ok':'no')+'">'+(r.wOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],valid=0,ok=0,w=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.bad){ rows.push(['분모 0','-','-','-','-']); continue; }
      valid++;
      if(r.ok) ok++;
      if(r.wOk) w++;
      rows.push(['('+r.a+'x'+sg(r.b)+')/('+r.c+'x+1)', r.x, '<b>'+r.num+'</b>', r.right,
                 '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
                 r.wrong,
                 '<span class="'+(r.wOk?'ok':'no')+'">'+(r.wOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'몫의 법칙이 맞은 횟수',big:ok+' / '+valid,p:'수치 미분과 (f′g − fg′)/g² 를 비교했다.'},
      {t:'f′/g′ 가 맞은 횟수',big:w+' / '+valid,p:'각각 미분해 나누면 맞지 않는다.'},
      {t:'유효한 기록',big:valid+'개',p:'분모가 0이 되는 x는 제외했다.'}
    ];
    var concl;
    if(valid===0){
      concl='<b>더 해 보자</b> — 분모가 0이 되지 않는 x로 기록해 보자.';
    } else if(ok===valid&&w===0){
      concl='<b>정리</b> — 몫의 도함수는 <b>(f′g − fg′) / g²</b> 였고, <b>f′/g′ 은 한 번도 맞지 않았다.</b> '
           +'분자에서 <b>빼는 순서</b>도 중요하다. 곱의 법칙을 f = (f/g)·g 에 적용해 정리하면 이 식이 나온다. '
           +'미분은 나눗셈과도 그대로 어울리지 않는다.';
    } else if(ok===valid){
      concl='<b>정리</b> — 몫의 법칙은 항상 맞았다. f′/g′ 이 우연히 맞는 경우가 있는지도 더 살펴보자.';
    } else {
      concl='<b>확인 필요</b> — 수치 미분과 공식이 어긋난 기록이 있다.';
    }
    return {head:['식','x','수치 미분','몫의 법칙','같나?','f′/g′','같나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 변곡점
# ============================================================
LAB_INFL = BASE + r"""
var KINDS=['x³','x⁴','x⁴ − 6x²','sin x'];
function fk(kind,x){
  if(kind===0) return x*x*x;
  if(kind===1) return x*x*x*x;
  if(kind===2) return x*x*x*x-6*x*x;
  return Math.sin(x);
}
function f2(kind,x){
  var h=1e-3;
  return (fk(kind,x+h)-2*fk(kind,x)+fk(kind,x-h))/(h*h);
}
var LAB = {
  cw:440, ch:430, cvTitle:'변곡점 판',
  action:'볼록함이 바뀌는지 보기',
  hint0:'함수를 고르고, 확인할 x를 정해 보자.',
  sliders:[
    {id:'kind',label:'함수',min:0,max:3,value:1,color:'#2563eb',fmt:function(v){return KINDS[v];}},
    {id:'x0',label:'확인할 x (÷10)',min:-30,max:30,value:0,color:'#dc2626',
     fmt:function(v){return (v/10).toFixed(1);}}
  ],
  calc:function(S){
    var x=S.x0/10;
    var d2=f2(S.kind,x);
    var L=f2(S.kind,x-0.3), R=f2(S.kind,x+0.3);
    var sign=(Math.abs(d2)<0.05)?0:(d2>0?1:-1);
    var change=((L>0&&R<0)||(L<0&&R>0));
    return {x:x,d2:d2,L:L,R:R,sign:sign,change:change,
            zero:(Math.abs(d2)<0.05)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:"f″(x)",v:ran?r3(c.d2):'재 보자'},
            {k:'좌우 볼록함',v:ran?((c.L>0?'아래로':'위로')+' / '+(c.R>0?'아래로':'위로')):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return "f″("+c.x+') = '+r3(c.d2)+'.  좌우의 볼록함이 '+(c.change?'바뀌었다 — 변곡점이다.':'바뀌지 않았다.')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var CX=220, CY=250, U=44, YU=14;
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=-4;i<=4;i++){ ctx.beginPath();ctx.moveTo(CX+i*U,CY-14*YU);ctx.lineTo(CX+i*U,CY+6*YU);ctx.stroke(); }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(CX-4*U,CY);ctx.lineTo(CX+4*U,CY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(CX,CY-14*YU);ctx.lineTo(CX,CY+6*YU);ctx.stroke();
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    var st=false;
    for(i=-40;i<=40;i++){
      var x=i/10, y=fk(S.kind,x);
      if(y<-6||y>14){ st=false; continue; }
      if(!st){ ctx.moveTo(CX+x*U,CY-y*YU); st=true; } else ctx.lineTo(CX+x*U,CY-y*YU);
    }
    ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      [[c.x-0.3,c.L,'#16a34a'],[c.x+0.3,c.R,'#f59e0b']].forEach(function(q){
        var y=fk(S.kind,q[0]);
        if(y<-6||y>14) return;
        ctx.beginPath();ctx.arc(CX+q[0]*U,CY-y*YU,6,0,Math.PI*2);
        ctx.fillStyle=q[2];ctx.fill();
        lbl(ctx,(q[1]>0)?'아래로 볼록':'위로 볼록',CX+q[0]*U-30,CY-y*YU-14,q[2],12);
      });
      var y0=fk(S.kind,c.x);
      if(y0>=-6&&y0<=14){
        ctx.beginPath();ctx.arc(CX+c.x*U,CY-y0*YU,7,0,Math.PI*2);
        ctx.fillStyle=c.change?'#dc2626':'#94a3b8';ctx.fill();
        ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      }
    }
    lbl(ctx,'f(x) = '+KINDS[S.kind],24,32,'#1d4ed8',18);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?"f″ = 0 이면 변곡점일까?":("f″("+c.x+') = '+r3(c.d2)+(c.zero?'  (거의 0)':'')),38,376,'#1f2937',17);
    lbl(ctx,(t===null)?'':('좌우 볼록함 '+(c.L>0?'아래로':'위로')+' → '+(c.R>0?'아래로':'위로')+'   '+(c.change?'변곡점':'변곡점 아님')),
        38,406,c.change?'#15803d':'#b91c1c',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {kind:S.kind,name:KINDS[S.kind],x:c.x,d2:r3(c.d2),
            zero:c.zero,change:c.change,
            L:(c.L>0)?'아래로':'위로',R:(c.R>0)?'아래로':'위로',
            trap:(c.zero&&!c.change)};
  },
  headA:['번호','함수','x','f″(x)','거의 0?','왼쪽','오른쪽','볼록함 바뀜?','변곡점?'],
  rowA:function(r,i){
    return [i+1,r.name,r.x,'<b>'+r.d2+'</b>',
            '<span class="'+(r.zero?'ok':'no')+'">'+(r.zero?'○':'×')+'</span>',
            r.L,r.R,
            '<span class="'+(r.change?'ok':'no')+'">'+(r.change?'○':'×')+'</span>',
            '<span class="'+(r.change?'ok':'no')+'">'+(r.change?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],zero=0,zeroInfl=0,trap=0,infl=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.zero){ zero++; if(r.change) zeroInfl++; }
      if(r.trap) trap++;
      if(r.change) infl++;
      rows.push([r.name, r.x, '<b>'+r.d2+'</b>',
                 '<span class="'+(r.zero?'ok':'no')+'">'+(r.zero?'○':'×')+'</span>',
                 r.L+' → '+r.R,
                 '<span class="'+(r.change?'ok':'no')+'">'+(r.change?'○':'×')+'</span>']);
    }
    var stats=[
      {t:"f″ 가 거의 0이었던 기록",big:zero+'개',
       p:zero?('그중 변곡점이었던 것 '+zeroInfl+'개.'):'f″ = 0 이 되는 x를 찾아보자.'},
      {t:'f″ = 0 인데 변곡점이 아니었던 경우',big:trap+'개',
       p:trap?'x⁴ 의 x = 0 이 그런 점이다.':'x⁴ 을 골라 x = 0 을 확인해 보자.'},
      {t:'변곡점이었던 기록',big:infl+'개',p:'좌우의 볼록함이 실제로 바뀐 경우.'}
    ];
    var concl;
    if(zero===0){
      concl='<b>더 해 보자</b> — f″ 가 0이 되는 x를 찾아보자. x³ 과 x⁴ 은 x = 0 에서 f″ = 0 이다.';
    } else if(trap>0){
      concl='<b>정리</b> — f″(a) = 0 인 점 중에도 <b>변곡점이 아닌 경우가 '+trap+'번</b> 있었다. '
           +'x⁴ 은 x = 0 에서 f″ = 0 이지만 좌우 모두 아래로 볼록이라 <b>휘는 방향이 바뀌지 않았다.</b> '
           +'즉 f″(a) = 0 은 변곡점의 <b>필요조건일 뿐</b>이고, 앞뒤에서 f″ 의 <b>부호가 실제로 바뀌어야</b> 변곡점이다. '
           +'극값에서 f′(a) = 0 이 충분조건이 아니었던 것과 같은 구조다.';
    } else {
      concl='<b>정리</b> — f″ = 0 인 점에서 좌우 볼록함을 확인해야 한다. x⁴ 의 x = 0 도 확인해 보자.';
    }
    return {head:['함수','x','f″','거의 0?','좌 → 우','변곡점?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 회전체의 부피
# ============================================================
LAB_VOL = BASE + r"""
var KINDS=['√x','x','x²'];
function fk3(kind,x){
  if(kind===0) return Math.sqrt(x);
  if(kind===1) return x;
  return x*x;
}
function exact(kind,b){
  if(kind===0) return Math.PI*b*b/2;
  if(kind===1) return Math.PI*b*b*b/3;
  return Math.PI*Math.pow(b,5)/5;
}
var LAB = {
  cw:440, ch:430, cvTitle:'회전체 판',
  action:'원판으로 쌓기',
  hint0:'곡선과 구간의 끝, 나누는 개수를 정해 보자.',
  sliders:[
    {id:'kind',label:'곡선 y =',min:0,max:2,value:0,color:'#2563eb',fmt:function(v){return KINDS[v];}},
    {id:'b',label:'구간의 끝 b',min:1,max:4,value:2,color:'#16a34a',unit:''},
    {id:'n',label:'원판 개수 n',min:1,max:60,value:8,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var dx=S.b/S.n, sum=0, i;
    for(i=0;i<S.n;i++){
      var x=(i+0.5)*dx;
      var r=fk3(S.kind,x);
      sum+=Math.PI*r*r*dx;
    }
    return {dx:dx,sum:sum,exact:exact(S.kind,S.b),
            gap:Math.abs(sum-exact(S.kind,S.b))};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'원판을 쌓은 부피',v:ran?r4(c.sum):'쌓아 보자'},
            {k:'π∫f²dx',v:r4(c.exact)}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '원판 '+S.n+'개로 '+r4(c.sum)+', 정확한 값 '+r4(c.exact)+'.  차이 '+r4(c.gap)+'.  n을 키워 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var GX=54, GY=250, XU=76, YU=44;
    function px(x){ return GX+x*XU; }
    function py(y){ return GY-y*YU; }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+4.4*XU,GY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(GX,GY-4.4*YU);ctx.lineTo(GX,GY+4.4*YU);ctx.stroke();
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*S.n);
    for(i=0;i<S.n&&i<shown;i++){
      var x0=i*c.dx, xm=(i+0.5)*c.dx;
      var r=fk3(S.kind,xm);
      var h=Math.min(r,4.2);
      ctx.fillStyle='rgba(37,99,235,0.18)';
      ctx.fillRect(px(x0),py(h),Math.max(1,px(x0+c.dx)-px(x0)),2*h*YU);
      ctx.strokeStyle='#93c5fd';ctx.lineWidth=1;
      ctx.strokeRect(px(x0),py(h),Math.max(1,px(x0+c.dx)-px(x0)),2*h*YU);
    }
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;
    [1,-1].forEach(function(s){
      ctx.beginPath();
      for(i=0;i<=200;i++){
        var x=S.b*i/200, y=s*fk3(S.kind,x);
        if(Math.abs(y)>4.3) continue;
        if(i===0) ctx.moveTo(px(x),py(y)); else ctx.lineTo(px(x),py(y));
      }
      ctx.stroke();
    });
    lbl(ctx,'y = '+KINDS[S.kind]+' 를 x축 둘레로 회전  (0 ≤ x ≤ '+S.b+')',24,32,'#1d4ed8',15);
    lbl(ctx,'원판 '+S.n+'개',24,56,'#52627a',14);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'원판을 쌓으면 부피는?':('원판 합 '+r4(c.sum)),38,376,'#1f2937',18);
    lbl(ctx,'π∫f²dx = '+r4(c.exact)+'      차이 '+r4(c.gap),38,406,'#15803d',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {kind:S.kind,name:KINDS[S.kind],b:S.b,n:S.n,
            sum:r4(c.sum),exact:r4(c.exact),gap:r4(c.gap),
            close:(c.gap<c.exact*0.01)};
  },
  headA:['번호','곡선','b','n','원판 합','π∫f²dx','차이','1% 이내?'],
  rowA:function(r,i){
    return [i+1,r.name,r.b,r.n,'<b>'+r.sum+'</b>',r.exact,r.gap,
            '<span class="'+(r.close?'ok':'no')+'">'+(r.close?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],close=0,g={},tested=0,ok=0,kn={},knn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.close) close++;
      if(!kn[r.name]){ kn[r.name]=true; knn++; }
      var k=r.name+'|'+r.b;
      if(!g[k]) g[k]=[];
      g[k].push([r.n,parseFloat(r.gap)]);
      rows.push([r.name, r.b, r.n, '<b>'+r.sum+'</b>', r.exact, r.gap,
                 '<span class="'+(r.close?'ok':'no')+'">'+(r.close?'○':'×')+'</span>']);
    }
    var k2;
    for(k2 in g){
      var arr=g[k2];
      if(arr.length<2) continue;
      arr.sort(function(x,y){return x[0]-y[0];});
      tested++;
      var good=true,j;
      for(j=1;j<arr.length;j++){ if(arr[j][1]>arr[j-1][1]+1e-9) good=false; }
      if(good) ok++;
    }
    var stats=[
      {t:'차이가 1% 이내였던 횟수',big:close+' / '+rec.length,p:'원판 개수가 많을수록 정확해졌다.'},
      {t:'n이 커질수록 차이가 줄어듦',big:tested?(ok+' / '+tested):'비교 없음',
       p:tested?'같은 곡선·구간에서 n만 바꾼 묶음.':'같은 곡선에서 n을 여러 값으로 기록해 보자.'},
      {t:'시험한 곡선',big:knn+'가지',p:'세 곡선 모두 같은 방식이 통했다.'}
    ];
    var concl;
    if(tested===0){
      concl='<b>더 해 보자</b> — 같은 곡선과 구간에서 n을 2, 8, 30, 60 처럼 키워 가며 기록해 보자.';
    } else if(ok===tested){
      concl='<b>정리</b> — 회전체를 <b>얇은 원판으로 잘라 쌓으면</b> 부피가 나왔다. '
           +'원판 하나의 부피는 π·(반지름)²·(두께) = πf(x)²dx 이고, 이것을 모두 더한 것이 <b>π∫f²dx</b> 다. '
           +'n을 키울수록 원판 합이 정확한 값으로 좁혀졌다. 넓이를 직사각형으로 구한 것과 같은 생각을 한 차원 올린 것이다.';
    } else {
      concl='<b>정리</b> — 원판 합은 정적분값에 다가갔다. n을 더 키워 기록해 보자.';
    }
    return {head:['곡선','b','n','원판 합','π∫f²dx','차이','1% 이내?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("hm_sinx_over_x_lab.html",
     "삼각함수 극한 실험실 — sin x / x 는 어디로 갈까?",
     "삼각함수 극한 실험실 — sin x / x 는 어디로 갈까?",
     "x를 0에 가깝게 줄여 가며 sin x/x 와 (1−cos x)/x 를 재고, 라디안과 도의 차이를 확인한다.",
     LAB_SINX),
    ("hm_chain_rule_lab.html",
     "연쇄법칙 실험실 — 안쪽도 미분해야 할까?",
     "연쇄법칙 실험실 — 안쪽도 미분해야 할까?",
     "합성함수를 수치로 미분해, 안쪽 미분을 포함한 값과 빠뜨린 값을 비교한다.",
     LAB_CHAIN),
    ("hm_quotient_rule_lab.html",
     "몫의 미분 실험실 — (f/g)′ = f′/g′ 일까?",
     "몫의 미분 실험실 — (f/g)′ = f′/g′ 일까?",
     "분수 함수를 수치로 미분해 몫의 법칙과 각각 미분해 나눈 값을 비교한다.",
     LAB_QUOT),
    ("hm_inflection_lab.html",
     "변곡점 실험실 — f″ = 0 이면 변곡점일까?",
     "변곡점 실험실 — f″ = 0 이면 변곡점일까?",
     "여러 함수에서 f″ 를 재고, 좌우의 볼록함이 실제로 바뀌는지 확인한다.",
     LAB_INFL),
    ("hm_volume_revolution_lab.html",
     "회전체 실험실 — 원판을 쌓으면 부피가 될까?",
     "회전체 실험실 — 원판을 쌓으면 부피가 될까?",
     "회전체를 얇은 원판으로 잘라 부피를 더하고, π∫f²dx 와 비교한다.",
     LAB_VOL),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c34_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
