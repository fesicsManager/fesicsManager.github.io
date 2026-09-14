# -*- coding: utf-8 -*-
"""고등 미적분Ⅰ — 미분 활용 2종 + 적분 3종"""
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
function sg(v){return (v<0)?(' − '+(-v)):(' + '+v);}
function sgc(v,s){ if(v===0) return ''; return (v<0)?(' − '+(-v)+s):(' + '+v+s); }
var CX=220, CY=230, U=26;
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
# 1. 도함수의 부호와 증가·감소
# ============================================================
LAB_MONO = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'증가·감소 판',
  action:'접선 기울기 재기',
  hint0:'삼차함수의 계수와 확인할 x를 정해 보자.',
  sliders:[
    {id:'a',label:'x² 계수 a',min:-4,max:4,value:0,color:'#2563eb',unit:''},
    {id:'b',label:'x 계수 b',min:-6,max:6,value:-3,color:'#16a34a',unit:''},
    {id:'x0',label:'확인할 x (÷10)',min:-30,max:30,value:5,color:'#dc2626',
     fmt:function(v){return (v/10).toFixed(1);}}
  ],
  f:function(S,x){ return x*x*x+S.a*x*x+S.b*x; },
  calc:function(S){
    var x=S.x0/10;
    var d=3*x*x+2*S.a*x+S.b;
    var eps=0.01;
    var rise=this.f(S,x+eps)-this.f(S,x-eps);
    return {x:x,d:d,rise:rise,
            up:(rise>1e-9),down:(rise<-1e-9),
            dPos:(d>1e-9),dNeg:(d<-1e-9)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:"f′(x)",v:ran?r3(c.d):'재 보자'},
            {k:'그 근처에서',v:ran?(c.up?'증가':(c.down?'감소':'변화 없음')):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return "f′("+c.x+') = '+r3(c.d)+'이고 그 근처에서 '+(c.up?'증가':(c.down?'감소':'거의 변화 없음'))+'한다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,5,5);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    var st=false;
    for(i=-50;i<=50;i++){
      var x=i/10, y=this.f(S,x)/2;
      if(y<-5||y>5){ st=false; continue; }
      if(!st){ ctx.moveTo(CX+x*U,CY-y*U); st=true; } else ctx.lineTo(CX+x*U,CY-y*U);
    }
    ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      var y0=this.f(S,c.x)/2, sl=c.d/2;
      ctx.strokeStyle=(c.d>0)?'#16a34a':((c.d<0)?'#dc2626':'#b45309');
      ctx.lineWidth=3;
      ctx.beginPath();
      ctx.moveTo(CX+(c.x-1.2)*U,CY-(y0+sl*(-1.2))*U);
      ctx.lineTo(CX+(c.x+1.2)*U,CY-(y0+sl*(1.2))*U);
      ctx.stroke();
      ctx.beginPath();ctx.arc(CX+c.x*U,CY-y0*U,7,0,Math.PI*2);
      ctx.fillStyle='#1f2937';ctx.fill();
    }
    lbl(ctx,'f(x) = x³'+sgc(S.a,'x²')+sgc(S.b,'x')+'   (세로 1/2 축소)',24,30,'#334155',15);
    box(ctx,20,338,400,80);
    lbl(ctx,(t===null)?'접선 기울기와 증가·감소는?':("f′("+c.x+') = '+r3(c.d)+'  →  '+(c.dPos?'양수':(c.dNeg?'음수':'0'))),
        38,368,'#1f2937',18);
    lbl(ctx,(t===null)?'':('근처에서 실제로 '+(c.up?'증가':(c.down?'감소':'거의 변화 없음'))),
        38,400,c.up?'#15803d':(c.down?'#b91c1c':'#b45309'),17);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,x:c.x,d:r3(c.d),rise:r4(c.rise),
            dSign:c.dPos?'양수':(c.dNeg?'음수':'0'),
            move:c.up?'증가':(c.down?'감소':'변화 없음'),
            match:((c.dPos&&c.up)||(c.dNeg&&c.down)||(!c.dPos&&!c.dNeg&&!c.up&&!c.down)),
            zero:(!c.dPos&&!c.dNeg)};
  },
  headA:['번호','f(x)','x','f′(x)','부호','실제 변화','일치?'],
  rowA:function(r,i){
    return [i+1,'x³'+sgc(r.a,'x²')+sgc(r.b,'x'),r.x,'<b>'+r.d+'</b>',r.dSign,r.move,
            '<span class="'+(r.match?'ok':'no')+'">'+(r.match?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],match=0,pos=0,posUp=0,neg=0,negDn=0,zero=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.match) match++;
      if(r.dSign==='양수'){ pos++; if(r.move==='증가') posUp++; }
      else if(r.dSign==='음수'){ neg++; if(r.move==='감소') negDn++; }
      else zero++;
      rows.push(['x³'+sgc(r.a,'x²')+sgc(r.b,'x'), r.x, '<b>'+r.d+'</b>', r.dSign, r.move,
                 '<span class="'+(r.match?'ok':'no')+'">'+(r.match?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'부호와 실제 변화가 일치',big:match+' / '+rec.length,
       p:'접선의 기울기 부호로 증가·감소를 판단할 수 있는지 확인한 결과.'},
      {t:"f′ > 0 이었던 기록",big:pos+'개',p:pos?('그중 실제로 증가한 것 '+posUp+'개.'):'양수인 지점도 기록해 보자.'},
      {t:"f′ < 0 이었던 기록",big:neg+'개',
       p:neg?('그중 실제로 감소한 것 '+negDn+'개.'+(zero?(' f′ = 0 인 기록 '+zero+'개.'):'')):'음수인 지점도 기록해 보자.'}
    ];
    var concl;
    if(pos===0||neg===0){
      concl='<b>더 해 보자</b> — f′ 이 양수인 곳과 음수인 곳을 <b>모두</b> 기록해야 규칙이 보인다.';
    } else if(match===rec.length){
      concl='<b>정리</b> — 접선의 기울기가 <b>양수인 곳에서는 증가, 음수인 곳에서는 감소</b>했다. 예외가 없었다. '
           +'도함수는 그 점에서 그래프가 어느 쪽으로 기울었는지를 알려 주므로, '
           +'f′ 의 부호만 조사하면 함수의 오르내림 전체를 알 수 있다. 이것이 증감표를 만드는 이유다.';
    } else {
      concl='<b>확인 필요</b> — 부호와 실제 변화가 어긋난 기록이 있다.';
    }
    return {head:['f(x)','x',"f′(x)",'부호','실제 변화','일치?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 극값
# ============================================================
LAB_EXTR = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'극값 판',
  action:'f′ = 0 인 곳 조사하기',
  hint0:'f(x) = x³ + ax 의 a를 정해 보자.',
  sliders:[
    {id:'a',label:'a',min:-6,max:6,value:0,color:'#2563eb',unit:''}
  ],
  f:function(S,x){ return x*x*x+S.a*x; },
  calc:function(S){
    var crit=[];
    if(S.a<0){ var s=Math.sqrt(-S.a/3); crit=[-s,s]; }
    else if(S.a===0){ crit=[0]; }
    var ext=[],i;
    for(i=0;i<crit.length;i++){
      var x=crit[i], e=0.05;
      var l=this.f(S,x-e), m=this.f(S,x), r=this.f(S,x+e);
      if(m>l+1e-9&&m>r+1e-9) ext.push([x,'극대']);
      else if(m<l-1e-9&&m<r-1e-9) ext.push([x,'극소']);
    }
    return {crit:crit,ext:ext};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:"f′(x) = 0 인 x",v:c.crit.length+'개'},
            {k:'실제 극값',v:ran?(c.ext.length+'개'):'조사해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return "f′(x) = 0 인 x가 "+c.crit.length+'개, 실제 극값은 '+c.ext.length+'개다. '
      +((c.crit.length>0&&c.ext.length===0)?'기울기가 0인데도 극값이 아니었다!':'')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,4,5);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    var st=false;
    for(i=-40;i<=40;i++){
      var x=i/10, y=this.f(S,x)/2;
      if(y<-5||y>5){ st=false; continue; }
      if(!st){ ctx.moveTo(CX+x*U,CY-y*U); st=true; } else ctx.lineTo(CX+x*U,CY-y*U);
    }
    ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      for(i=0;i<c.crit.length;i++){
        var xx=c.crit[i], yy=this.f(S,xx)/2;
        if(Math.abs(yy)>5) continue;
        ctx.strokeStyle='#f59e0b';ctx.lineWidth=3;
        ctx.beginPath();ctx.moveTo(CX+(xx-1)*U,CY-yy*U);ctx.lineTo(CX+(xx+1)*U,CY-yy*U);ctx.stroke();
        var isExt=false,kind2='';
        for(var j=0;j<c.ext.length;j++){ if(Math.abs(c.ext[j][0]-xx)<1e-9){ isExt=true; kind2=c.ext[j][1]; } }
        ctx.beginPath();ctx.arc(CX+xx*U,CY-yy*U,7,0,Math.PI*2);
        ctx.fillStyle=isExt?'#dc2626':'#94a3b8';ctx.fill();
        ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
        if(grow>=1) lbl(ctx,isExt?kind2:'극값 아님',CX+xx*U+10,CY-yy*U-10,isExt?'#b91c1c':'#64748b',14);
      }
    }
    lbl(ctx,'f(x) = x³'+sgc(S.a,'x')+'      f′(x) = 3x²'+sg(S.a)+'   (세로 1/2 축소)',24,30,'#334155',14);
    box(ctx,20,338,400,80);
    lbl(ctx,(t===null)?"f′ = 0 이면 반드시 극값일까?":("f′(x) = 0 인 x : "+c.crit.length+'개'),38,368,'#1f2937',18);
    lbl(ctx,(t===null)?'':('실제 극값 : '+c.ext.length+'개'+((c.crit.length>0&&c.ext.length===0)?'  ← 기울기 0인데 극값이 아니다':'')),
        38,400,(c.crit.length>0&&c.ext.length===0)?'#b91c1c':'#15803d',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,crit:c.crit.length,ext:c.ext.length,
            kinds:c.ext.map(function(e){return e[1];}).join(', ')||'없음',
            same:(c.crit.length===c.ext.length),
            trap:(c.crit.length>0&&c.ext.length===0)};
  },
  headA:['번호','a',"f′(x)=0 인 x 개수",'실제 극값 개수','극값의 종류','개수가 같나?'],
  rowA:function(r,i){
    return [i+1,r.a,'<b>'+r.crit+'</b>',r.ext,r.kinds,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,trap=0,two=0,zero=0,gs={},gn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.trap) trap++;
      if(r.crit===2) two++;
      if(r.crit===0) zero++;
      if(!gs[r.a]){ gs[r.a]=true; gn++; }
      rows.push([r.a, '<b>'+r.crit+'</b>', r.ext, r.kinds,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 r.trap?'<span class="no">기울기 0인데 극값 아님</span>':'-']);
    }
    var stats=[
      {t:"f′ = 0 인 개수와 극값 개수가 같았던 횟수",big:same+' / '+rec.length,
       p:'기울기가 0인 곳이 모두 극값이었는지 확인한 결과.'},
      {t:'기울기 0인데 극값이 아니었던 기록',big:trap+'개',
       p:trap?'a = 0 일 때 x = 0 이 그런 점이다.':'a를 0으로도 해 보자.'},
      {t:"f′ = 0 이 2개 / 0개였던 기록",big:two+'개 / '+zero+'개',
       p:'시험한 a '+gn+'가지. a가 음수면 2개, 양수면 없다.'}
    ];
    var concl;
    if(trap===0){
      concl='<b>더 해 보자</b> — <b>a = 0</b> 으로 두고 확인해 보자. f′(0) = 0 인데 극값인지 아닌지가 핵심이다.';
    } else {
      concl='<b>정리</b> — a가 음수면 f′ = 0 인 두 점이 모두 극대·극소였지만, <b>a = 0 일 때는 f′(0) = 0 인데도 극값이 아니었다.</b> '
           +'기울기가 잠깐 0이 되었다가 다시 같은 방향으로 올라가기 때문이다. '
           +'즉 <b>f′(a) = 0 은 극값의 필요조건일 뿐 충분조건이 아니다.</b> 앞뒤에서 f′ 의 <b>부호가 바뀌는지</b>까지 확인해야 한다.';
    }
    return {head:['a',"f′=0 개수",'극값 개수','종류','같나?','비고'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 리만합과 정적분
# ============================================================
LAB_RIEM = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'구분구적 판',
  action:'직사각형으로 채우기',
  hint0:'구간의 끝과 나누는 개수를 정해 보자.',
  sliders:[
    {id:'b',label:'구간의 끝 b',min:1,max:4,value:2,color:'#2563eb',unit:''},
    {id:'n',label:'나누는 개수 n',min:1,max:60,value:6,color:'#f59e0b',unit:''}
  ],
  f:function(x){ return x*x; },
  calc:function(S){
    var dx=S.b/S.n, L=0,R=0,i;
    for(i=0;i<S.n;i++){
      L+=this.f(i*dx)*dx;
      R+=this.f((i+1)*dx)*dx;
    }
    var exact=S.b*S.b*S.b/3;
    return {dx:dx,L:L,R:R,exact:exact,mid:(L+R)/2,
            gapL:Math.abs(exact-L),gapR:Math.abs(R-exact)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'작은 쪽 합',v:ran?r4(c.L):'채워 보자'},
            {k:'큰 쪽 합',v:ran?r4(c.R):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '작은 쪽 '+r4(c.L)+', 큰 쪽 '+r4(c.R)+', 정적분값 b³/3 = '+r4(c.exact)+'다. n을 키워 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var GX=50, GY=330, GW=340, GH=260;
    var ymax=S.b*S.b;
    function px(x){ return GX+GW*x/S.b; }
    function py(y){ return GY-GH*y/ymax; }
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*S.n);
    for(i=0;i<S.n&&i<shown;i++){
      var x0=i*c.dx, x1=(i+1)*c.dx;
      ctx.fillStyle='rgba(37,99,235,0.20)';
      ctx.fillRect(px(x0),py(this.f(x0)),px(x1)-px(x0),GY-py(this.f(x0)));
      ctx.strokeStyle='#93c5fd';ctx.lineWidth=1;
      ctx.strokeRect(px(x0),py(this.f(x0)),px(x1)-px(x0),GY-py(this.f(x0)));
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=1;
      ctx.strokeRect(px(x0),py(this.f(x1)),px(x1)-px(x0),GY-py(this.f(x1)));
    }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+GW+10,GY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX,GY-GH-10);ctx.stroke();
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    for(i=0;i<=200;i++){
      var x=S.b*i/200;
      if(i===0) ctx.moveTo(px(x),py(this.f(x))); else ctx.lineTo(px(x),py(this.f(x)));
    }
    ctx.stroke();
    lbl(ctx,'y = x²,  0 ≤ x ≤ '+S.b+',  n = '+S.n,24,30,'#1d4ed8',17);
    lbl(ctx,'파랑 = 작은 쪽,  주황 = 큰 쪽',24,54,'#52627a',14);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'직사각형으로 채우면 얼마일까?':('작은 쪽 '+r4(c.L)+'      큰 쪽 '+r4(c.R)),38,376,'#1f2937',17);
    lbl(ctx,'b³/3 = '+r4(c.exact)+'      차이 '+r4(c.gapL)+' / '+r4(c.gapR),38,406,'#15803d',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {b:S.b,n:S.n,L:r4(c.L),R:r4(c.R),exact:r4(c.exact),
            gapL:r4(c.gapL),gapR:r4(c.gapR),
            between:(c.L<=c.exact+1e-9&&c.exact<=c.R+1e-9),
            close:(Math.max(c.gapL,c.gapR)<0.05)};
  },
  headA:['번호','b','n','작은 쪽','큰 쪽','b³/3','사이에 있나?','차이','0.05 이내?'],
  rowA:function(r,i){
    return [i+1,r.b,r.n,r.L,r.R,'<b>'+r.exact+'</b>',
            '<span class="'+(r.between?'ok':'no')+'">'+(r.between?'○':'×')+'</span>',
            r.gapL+' / '+r.gapR,
            '<span class="'+(r.close?'ok':'no')+'">'+(r.close?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],bt=0,close=0,g={},tested=0,ok=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.between) bt++;
      if(r.close) close++;
      if(!g[r.b]) g[r.b]=[];
      g[r.b].push([r.n,parseFloat(r.gapR)]);
      rows.push([r.b, r.n, r.L+' / '+r.R, '<b>'+r.exact+'</b>',
                 '<span class="'+(r.between?'ok':'no')+'">'+(r.between?'○':'×')+'</span>',
                 r.gapR,
                 '<span class="'+(r.close?'ok':'no')+'">'+(r.close?'○':'×')+'</span>']);
    }
    var k;
    for(k in g){
      var arr=g[k];
      if(arr.length<2) continue;
      arr.sort(function(x,y){return x[0]-y[0];});
      tested++;
      var good=true,j;
      for(j=1;j<arr.length;j++){ if(arr[j][1]>arr[j-1][1]+1e-9) good=false; }
      if(good) ok++;
    }
    var stats=[
      {t:'정적분값이 두 합 사이에 있었던 횟수',big:bt+' / '+rec.length,
       p:'작은 쪽 합 ≤ 넓이 ≤ 큰 쪽 합 이 성립했는지 확인한 결과.'},
      {t:'차이가 0.05 이내였던 횟수',big:close+' / '+rec.length,p:'n이 클수록 가까워졌다.'},
      {t:'같은 b에서 n이 클수록 차이가 줄어듦',big:tested?(ok+' / '+tested):'비교 없음',
       p:tested?'b를 고정하고 n만 바꾼 묶음.':'같은 b에서 n을 여러 값으로 기록해 보자.'}
    ];
    var concl;
    if(tested===0){
      concl='<b>더 해 보자</b> — b를 고정하고 n을 2, 6, 20, 60 처럼 키워 가며 기록해 보자.';
    } else if(bt===rec.length&&ok===tested){
      concl='<b>정리</b> — 곡선 아래 넓이는 언제나 <b>작은 쪽 합과 큰 쪽 합 사이</b>에 있었고, '
           +'n을 키울수록 두 합이 <b>같은 값 b³/3 으로 좁혀졌다.</b> '
           +'정적분은 이 “좁혀 들어가는 값”이다. 직사각형이 아무리 많아져도 정확히 맞지는 않지만, '
           +'다가가는 값은 하나로 정해진다.';
    } else {
      concl='<b>확인 필요</b> — 정적분값이 두 합 사이에 있지 않은 기록이 있다.';
    }
    return {head:['b','n','작은/큰 합','b³/3','사이?','차이','가까운가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 정적분과 넓이
# ============================================================
LAB_AREA = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'정적분 부호 판',
  action:'적분값과 넓이 구하기',
  hint0:'구간의 양 끝을 정해 보자. f(x) = x² − 4 는 x = ±2 에서 x축을 지난다.',
  sliders:[
    {id:'p',label:'왼쪽 끝 (÷10)',min:-40,max:20,value:-30,color:'#2563eb',
     fmt:function(v){return (v/10).toFixed(1);}},
    {id:'q',label:'오른쪽 끝 (÷10)',min:-20,max:40,value:10,color:'#dc2626',
     fmt:function(v){return (v/10).toFixed(1);}}
  ],
  f:function(x){ return x*x-4; },
  calc:function(S){
    var p=S.p/10, q=S.q/10;
    if(q<p){ var tmp=p; p=q; q=tmp; }
    var n=4000, dx=(q-p)/n, I=0, A=0, i;
    for(i=0;i<n;i++){
      var x=p+(i+0.5)*dx, y=this.f(x);
      I+=y*dx; A+=Math.abs(y)*dx;
    }
    function F(x){ return x*x*x/3-4*x; }
    return {p:p,q:q,I:I,A:A,F:F(q)-F(p),
            cross:(p<-2&&q>-2)||(p<2&&q>2)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'정적분값',v:ran?r3(c.I):'구해 보자'},
            {k:'넓이',v:ran?r3(c.A):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '정적분값 '+r3(c.I)+', 넓이 '+r3(c.A)+'.  '+((Math.abs(c.I-c.A)<0.01)?'두 값이 같다.':'두 값이 다르다 — x축 아래 부분이 있다.')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var GX=40, GY=250, XU=44, YU=18;
    function px(x){ return GX+(x+4)*XU; }
    function py(y){ return GY-y*YU; }
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=-4;i<=4;i++){ ctx.beginPath();ctx.moveTo(px(i),GY-6*YU);ctx.lineTo(px(i),GY+6*YU);ctx.stroke(); }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(px(-4),GY);ctx.lineTo(px(4),GY);ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      var n=120, dx=(c.q-c.p)/n;
      for(i=0;i<n*grow;i++){
        var x0=c.p+i*dx, y0=this.f(x0);
        ctx.fillStyle=(y0>=0)?'rgba(37,99,235,0.25)':'rgba(220,38,38,0.25)';
        var top=(y0>=0)?py(y0):GY;
        ctx.fillRect(px(x0),top,Math.max(1,px(x0+dx)-px(x0)),Math.abs(py(y0)-GY));
      }
    }
    ctx.strokeStyle='#1d4ed8';ctx.lineWidth=3;ctx.beginPath();
    for(i=-40;i<=40;i++){
      var x=i/10, y=this.f(x);
      if(y<-6||y>6) { continue; }
      if(i===-40) ctx.moveTo(px(x),py(y)); else ctx.lineTo(px(x),py(y));
    }
    ctx.stroke();
    lbl(ctx,'f(x) = x² − 4,   구간 ['+c.p+', '+c.q+']',24,30,'#1d4ed8',17);
    lbl(ctx,'파랑 = x축 위,  빨강 = x축 아래',24,54,'#52627a',14);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'정적분값과 넓이는 같을까?':('정적분값 '+r3(c.I)+'      넓이 '+r3(c.A)),38,376,'#1f2937',18);
    lbl(ctx,(t===null)?'':('F(q) − F(p) = '+r3(c.F)),38,406,'#15803d',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {p:c.p,q:c.q,I:r3(c.I),A:r3(c.A),F:r3(c.F),
            same:(Math.abs(c.I-c.A)<0.01),
            ftc:(Math.abs(c.I-c.F)<0.01),
            neg:(c.I<0),cross:c.cross};
  },
  headA:['번호','구간','정적분값','넓이','같나?','F(q)−F(p)','정적분과 같나?','x축 아래 포함?'],
  rowA:function(r,i){
    return [i+1,'['+r.p+', '+r.q+']','<b>'+r.I+'</b>',r.A,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            r.F,
            '<span class="'+(r.ftc?'ok':'no')+'">'+(r.ftc?'○':'×')+'</span>',
            r.cross?'○':'×'];
  },
  analyze:function(rec){
    var rows=[],same=0,ftc=0,cross=0,crossSame=0,neg=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.ftc) ftc++;
      if(r.cross){ cross++; if(r.same) crossSame++; }
      if(r.neg) neg++;
      rows.push(['['+r.p+', '+r.q+']', '<b>'+r.I+'</b>', r.A,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 r.F,
                 '<span class="'+(r.ftc?'ok':'no')+'">'+(r.ftc?'○':'×')+'</span>',
                 r.cross?'○':'×']);
    }
    var stats=[
      {t:'정적분값 = 넓이',big:same+' / '+rec.length,p:'두 값이 같았던 기록 수.'},
      {t:'x축 아래를 포함한 구간',big:cross+'개',
       p:cross?('그중 두 값이 같았던 것 '+crossSame+'개.'):'−2와 2 사이를 포함하는 구간도 잡아 보자.'},
      {t:'정적분값이 음수였던 기록',big:neg+'개',
       p:'넓이는 음수가 될 수 없지만 정적분값은 될 수 있다.'}
    ];
    var concl;
    if(cross===0){
      concl='<b>더 해 보자</b> — 구간이 x = −2 ~ 2 사이를 지나도록 잡아 보자. 그래프가 x축 아래로 내려가는 부분이 생긴다.';
    } else if(crossSame===0){
      concl='<b>정리</b> — x축 아래 부분이 포함되면 <b>정적분값과 넓이가 달랐다.</b> '
           +'정적분은 아래쪽을 <b>음수</b>로 세기 때문이다. 넓이를 구하려면 x축과 만나는 점에서 구간을 나눠 '
           +'각 조각의 절댓값을 더해야 한다. 한편 <b>F(q) − F(p)</b> 는 언제나 정적분값과 같았다(미적분의 기본정리).';
    } else {
      concl='<b>정리</b> — 정적분은 부호가 있는 값이다. 두 값이 다른 경우를 더 찾아보자.';
    }
    return {head:['구간','정적분값','넓이','같나?','F(q)−F(p)','같나?','아래 포함?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 미적분의 기본정리
# ============================================================
LAB_FTC = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'기본정리 판',
  action:'두 방법으로 구하기',
  hint0:'피적분함수의 계수와 적분 구간을 정해 보자.',
  sliders:[
    {id:'a',label:'x 계수 a',min:-6,max:6,value:2,color:'#2563eb',unit:''},
    {id:'b',label:'상수 b',min:-6,max:6,value:-1,color:'#16a34a',unit:''},
    {id:'p',label:'아래끝 (÷10)',min:-30,max:20,value:-10,color:'#f59e0b',
     fmt:function(v){return (v/10).toFixed(1);}},
    {id:'q',label:'위끝 (÷10)',min:-20,max:30,value:20,color:'#dc2626',
     fmt:function(v){return (v/10).toFixed(1);}}
  ],
  f:function(S,x){ return 3*x*x+S.a*x+S.b; },
  calc:function(S){
    var p=S.p/10, q=S.q/10;
    var n=20000, dx=(q-p)/n, I=0, i;
    for(i=0;i<n;i++){
      var x=p+(i+0.5)*dx;
      I+=this.f(S,x)*dx;
    }
    function F(x){ return x*x*x+S.a*x*x/2+S.b*x; }
    return {p:p,q:q,I:I,F:F(q)-F(p),Fq:F(q),Fp:F(p)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'잘게 나눠 더한 값',v:ran?r3(c.I):'구해 보자'},
            {k:'F(q) − F(p)',v:ran?r3(c.F):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '2만 개로 나눠 더하면 '+r3(c.I)+', F(q) − F(p) = '+r3(c.F)+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var GX=40, GY=250, XU=52, YU=8;
    function px(x){ return GX+(x+3)*XU; }
    function py(y){ return GY-y*YU; }
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=-3;i<=3;i++){ ctx.beginPath();ctx.moveTo(px(i),GY-14*YU);ctx.lineTo(px(i),GY+14*YU);ctx.stroke(); }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(px(-3),GY);ctx.lineTo(px(3),GY);ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      var n=140, dx=(c.q-c.p)/n;
      for(i=0;i<n*grow;i++){
        var x0=c.p+i*dx, y0=this.f(S,x0);
        ctx.fillStyle=(y0>=0)?'rgba(37,99,235,0.22)':'rgba(220,38,38,0.22)';
        var top=(y0>=0)?py(y0):GY;
        ctx.fillRect(px(x0),top,Math.max(1,px(x0+dx)-px(x0)),Math.abs(py(y0)-GY));
      }
    }
    ctx.strokeStyle='#1d4ed8';ctx.lineWidth=3;ctx.beginPath();
    var st=false;
    for(i=-30;i<=30;i++){
      var x=i/10, y=this.f(S,x);
      if(y<-14||y>14){ st=false; continue; }
      if(!st){ ctx.moveTo(px(x),py(y)); st=true; } else ctx.lineTo(px(x),py(y));
    }
    ctx.stroke();
    lbl(ctx,'f(x) = 3x²'+sgc(S.a,'x')+sg(S.b)+'      구간 ['+c.p+', '+c.q+']',24,30,'#1d4ed8',15);
    lbl(ctx,'F(x) = x³'+((S.a===0)?'':(' + '+(S.a/2)+'x²'))+sgc(S.b,'x'),24,54,'#52627a',14);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'두 방법의 결과는 같을까?':('잘게 나눠 더한 값 '+r3(c.I)),38,376,'#1f2937',18);
    lbl(ctx,(t===null)?'':('F('+c.q+') − F('+c.p+') = '+r3(c.Fq)+' − '+r3(c.Fp)+' = '+r3(c.F)),38,406,'#15803d',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,p:c.p,q:c.q,I:r3(c.I),F:r3(c.F),
            Fq:r3(c.Fq),Fp:r3(c.Fp),
            same:(Math.abs(c.I-c.F)<0.01),
            gap:r4(Math.abs(c.I-c.F))};
  },
  headA:['번호','f(x)','구간','잘게 더한 값','F(q)','F(p)','F(q)−F(p)','같나?','차이'],
  rowA:function(r,i){
    return [i+1,'3x²'+sgc(r.a,'x')+sg(r.b),'['+r.p+', '+r.q+']','<b>'+r.I+'</b>',r.Fq,r.Fp,r.F,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',r.gap];
  },
  analyze:function(rec){
    var rows=[],same=0,mx=0,neg=0,rev=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(parseFloat(r.gap)>mx) mx=parseFloat(r.gap);
      if(parseFloat(r.I)<0) neg++;
      if(r.p>r.q) rev++;
      rows.push(['3x²'+sgc(r.a,'x')+sg(r.b), '['+r.p+', '+r.q+']', '<b>'+r.I+'</b>', r.F,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>', r.gap]);
    }
    var stats=[
      {t:'두 방법의 결과가 같았던 횟수',big:same+' / '+rec.length,
       p:'2만 개로 잘게 나눠 더한 값과 원시함수 차를 비교했다.'},
      {t:'가장 큰 차이',big:mx+'',p:'수치 계산의 오차 범위다.'},
      {t:'적분값이 음수였던 기록',big:neg+'개',p:'f(x)가 음수인 부분이 많으면 전체 적분값도 음수가 된다.'}
    ];
    var concl;
    if(same===rec.length){
      concl='<b>정리</b> — 구간을 2만 개로 잘게 나눠 더한 값과 <b>F(q) − F(p)</b> 가 언제나 같았다. '
           +'넓이를 구하는 일(적분)과 도함수를 거꾸로 찾는 일(원시함수)이 <b>같은 답으로 이어진다</b>는 것이 미적분의 기본정리다. '
           +'덕분에 무한히 잘게 나눠 더하는 대신 원시함수를 찾아 두 값을 빼기만 하면 된다.';
    } else {
      concl='<b>확인 필요</b> — 두 방법의 결과가 다른 기록이 있다. 수치 오차 범위를 넘는지 확인해 보자.';
    }
    return {head:['f(x)','구간','잘게 더한 값','F(q)−F(p)','같나?','차이'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("hc_monotonic_lab_Calculus1_DerivApp_Ep01.html",
     "증가·감소 실험실 — 기울기의 부호가 무엇을 말할까?",
     "증가·감소 실험실 — 기울기의 부호가 무엇을 말할까?",
     "여러 지점에서 접선의 기울기를 재고, 그 근처에서 실제로 오르는지 내리는지 대조한다.",
     LAB_MONO),
    ("hc_extremum_lab_Calculus1_DerivApp_Ep02.html",
     "극값 실험실 — 기울기가 0이면 극값일까?",
     "극값 실험실 — 기울기가 0이면 극값일까?",
     "f′(x) = 0 인 점을 찾아 그 앞뒤 값을 비교하며 극값인지 아닌지 판정한다.",
     LAB_EXTR),
    ("hc_riemann_sum_lab_Calculus1_Integral.html",
     "구분구적 실험실 — 직사각형으로 곡선 아래를 채우면?",
     "구분구적 실험실 — 직사각형으로 곡선 아래를 채우면?",
     "직사각형 개수를 늘려 가며 작은 쪽 합과 큰 쪽 합이 어디로 좁혀지는지 기록한다.",
     LAB_RIEM),
    ("hc_integral_area_lab_Calculus1_IntegralApp_Ep01.html",
     "정적분 실험실 — 정적분값이 곧 넓이일까?",
     "정적분 실험실 — 정적분값이 곧 넓이일까?",
     "x축 아래를 지나는 구간에서 정적분값과 실제 넓이를 따로 구해 비교한다.",
     LAB_AREA),
    ("hc_ftc_lab_Calculus1_Integral_Ep04.html",
     "기본정리 실험실 — 잘게 더하기와 원시함수는 왜 같을까?",
     "기본정리 실험실 — 잘게 더하기와 원시함수는 왜 같을까?",
     "구간을 2만 개로 나눠 더한 값과 F(q) − F(p)를 비교한다.",
     LAB_FTC),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c28_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
