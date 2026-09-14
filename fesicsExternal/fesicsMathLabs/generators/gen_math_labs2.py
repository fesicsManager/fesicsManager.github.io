# -*- coding: utf-8 -*-
"""초등 3-4학년군 '변화와 관계' 실험 5종 — 공통 템플릿 재사용"""
import os, re

OUT = "/mnt/user-data/outputs"
src = open("/home/claude/gen_math_labs.py", encoding="utf-8").read()
TPL = re.search(r'TPL = r"""(.*?)"""\n', src, re.S).group(1)

# ============================================================
# LAB 1 : 양팔저울과 등호
# ============================================================
LAB_SCALE = r"""
function lbl(ctx,t,x,y,c,sz,al){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
function pan(ctx,cx,cy,val,e1,e2,col){
  ctx.strokeStyle='#94a3b8';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(cx,cy-46);ctx.lineTo(cx-52,cy);ctx.moveTo(cx,cy-46);ctx.lineTo(cx+52,cy);ctx.stroke();
  ctx.fillStyle='#eef4fc';ctx.fillRect(cx-60,cy,120,96);
  ctx.strokeStyle=col;ctx.lineWidth=2.5;ctx.strokeRect(cx-60,cy,120,96);
  var i;
  for(i=0;i<val && i<40;i++){
    var x=cx-54+(i%10)*11, y=cy+82-Math.floor(i/10)*13;
    ctx.fillStyle=col;ctx.fillRect(x,y,8,8);
  }
  lbl(ctx,e1+' + '+e2,cx,cy-8,'#334155',18,'center');
}

var LAB = {
  cw:440, ch:430, cvTitle:'양팔저울',
  action:'저울에 올려 보기',
  hint0:'양쪽 접시에 올릴 수를 정하고 저울에 올려 보자.',
  sliders:[
    {id:'la',label:'왼쪽 첫 번째 수',min:1,max:20,value:5,color:'#2563eb',unit:''},
    {id:'lb',label:'왼쪽 두 번째 수',min:0,max:20,value:8,color:'#60a5fa',unit:''},
    {id:'ra',label:'오른쪽 첫 번째 수',min:1,max:20,value:9,color:'#dc2626',unit:''},
    {id:'rb',label:'오른쪽 두 번째 수',min:0,max:20,value:4,color:'#f87171',unit:''}
  ],
  readout:function(S,ran){
    return [{k:'왼쪽',v:S.la+' + '+S.lb+' = '+(S.la+S.lb)},
            {k:'오른쪽',v:S.ra+' + '+S.rb+' = '+(S.ra+S.rb)}];
  },
  doneMsg:function(S){
    var L=S.la+S.lb,R=S.ra+S.rb;
    if(L===R) return '저울이 평평하다. 두 식은 생김새가 달라도 값이 같다. 기록해 보자.';
    return '저울이 '+(L>R?'왼쪽':'오른쪽')+'으로 기울었다. 값이 '+(L>R?L:R)+'인 쪽이 무겁다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var L=S.la+S.lb, R=S.ra+S.rb, d=R-L;
    var full=Math.max(-0.22,Math.min(0.22,d*0.028));
    var e=(t===null)?0:(1-Math.pow(1-t,3));
    var th=full*e;
    var px=220, py=132, arm=150;
    ctx.fillStyle='#cbd5e1';
    ctx.beginPath();ctx.moveTo(px,py);ctx.lineTo(px-40,py+180);ctx.lineTo(px+40,py+180);ctx.closePath();ctx.fill();
    ctx.strokeStyle='#94a3b8';ctx.lineWidth=2;ctx.stroke();
    var lx=px-arm*Math.cos(th), ly=py-arm*Math.sin(th);
    var rx=px+arm*Math.cos(th), ry=py+arm*Math.sin(th);
    ctx.strokeStyle='#475569';ctx.lineWidth=7;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(lx,ly);ctx.lineTo(rx,ry);ctx.stroke();
    ctx.lineCap='butt';
    ctx.beginPath();ctx.arc(px,py,10,0,Math.PI*2);ctx.fillStyle='#334155';ctx.fill();
    pan(ctx,lx,ly+46,L,S.la,S.lb,'#2563eb');
    pan(ctx,rx,ry+46,R,S.ra,S.rb,'#dc2626');

    ctx.fillStyle='#f1f6fd';ctx.fillRect(20,352,400,60);
    ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(20,352,400,60);
    var txt;
    if(t===null) txt=S.la+' + '+S.lb+'  ?  '+S.ra+' + '+S.rb;
    else if(t<1) txt='저울이 움직이는 중...';
    else txt=S.la+' + '+S.lb+(L===R?'  =  ':(L>R?'  >  ':'  <  '))+S.ra+' + '+S.rb;
    lbl(ctx,txt,38,390,'#1f2937',22);
  },
  record:function(S){
    var L=S.la+S.lb,R=S.ra+S.rb;
    return {la:S.la,lb:S.lb,ra:S.ra,rb:S.rb,L:L,R:R,bal:(L===R),
            sameForm:(S.la===S.ra&&S.lb===S.rb)};
  },
  headA:['번호','왼쪽 식','왼쪽 값','오른쪽 식','오른쪽 값','저울'],
  rowA:function(r,i){
    return [i+1,r.la+' + '+r.lb,r.L,r.ra+' + '+r.rb,r.R,
            '<span class="'+(r.bal?'ok':'no')+'">'+(r.bal?'평평':'기울어짐')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],bal=0,match=0,diffForm=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var same=(r.L===r.R);
      var ok=(same===r.bal);
      if(r.bal) bal++;
      if(ok) match++;
      if(r.bal && !r.sameForm) diffForm++;
      rows.push([r.la+' + '+r.lb+'  vs  '+r.ra+' + '+r.rb, r.L, r.R,
                 '<span class="'+(same?'ok':'no')+'">'+(same?'○':'×')+'</span>',
                 r.bal?'평평':'기울어짐',
                 '<span class="'+(ok?'ok':'no')+'">'+(ok?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'평평했던 횟수',big:bal+' / '+rec.length,p:'저울이 균형을 이룬 기록 수.'},
      {t:'값이 같을 때만 평평했나',big:match+' / '+rec.length,p:'양쪽 값이 같은지와 저울 상태가 일치한 횟수.'},
      {t:'식은 다른데 평평했던 경우',big:diffForm+'개',
       p:diffForm?'생김새가 다른 두 식도 값만 같으면 평평했다.':'5+8과 9+4처럼 모양이 다른 짝을 만들어 보자.'}
    ];
    var concl;
    if(match!==rec.length){
      concl='<b>확인 필요</b> — 값이 같은데 기울었거나, 값이 다른데 평평했던 기록이 있다. 수를 다시 확인해 보자.';
    } else if(diffForm>0){
      concl='<b>정리</b> — 5 + 8과 9 + 4처럼 <b>생김새가 전혀 다른 식도 값이 같으면 저울은 평평했다.</b> '
           +'=는 “이제 답을 쓰시오”라는 신호가 아니라, <b>양쪽이 똑같다</b>는 뜻이다. '
           +'그래서 5 + 8 = 9 + 4라고 쓸 수 있고, 5 + 8 = □ + 4의 □도 찾을 수 있다.';
    } else {
      concl='<b>정리</b> — 양쪽 값이 같을 때만 저울이 평평했다. 이번엔 5+8과 9+4처럼 <b>모양이 다른데 값은 같은</b> 짝을 만들어 다시 확인해 보자.';
    }
    return {head:['비교','왼쪽 값','오른쪽 값','값이 같은가?','저울','예상과 맞나?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# LAB 2 : 뛰어세기 규칙
# ============================================================
LAB_SKIP = r"""
function lbl(ctx,t,x,y,c,sz,al){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
function seq(s,k){var a=[],v=s,i;for(i=0;i<8;i++){a.push(v);v+=k;}return a;}

var LAB = {
  cw:440, ch:380, cvTitle:'뛰어세기 수직선',
  action:'규칙대로 8번 뛰기',
  hint0:'시작하는 수와 뛰는 수를 정하고 뛰어 보자.',
  sliders:[
    {id:'s',label:'시작하는 수',min:0,max:20,value:3,color:'#2563eb',unit:''},
    {id:'k',label:'뛰는 수',min:1,max:12,value:4,color:'#16a34a',unit:'씩'}
  ],
  readout:function(S,ran){
    var a=seq(S.s,S.k);
    return [{k:'수 배열',v:a[0]+', '+a[1]+', '+a[2]+' ...'},
            {k:'8번째 수',v:ran?a[7]:'뛰어 보자'}];
  },
  doneMsg:function(S){
    var a=seq(S.s,S.k);
    return '8번째 수는 '+a[7]+'이다. 시작 '+S.s+'에 '+S.k+'을(를) 7번 더한 값과 같은지 확인해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var a=seq(S.s,S.k), lo=a[0], hi=a[7];
    var X0=32, X1=408, Y=250;
    function px(v){ return X0+(X1-X0)*(v-lo)/Math.max(1,(hi-lo)); }
    ctx.strokeStyle='#334155';ctx.lineWidth=3;
    ctx.beginPath();ctx.moveTo(X0-12,Y);ctx.lineTo(X1+12,Y);ctx.stroke();
    var shown=(t===null)?1:Math.max(1,Math.min(8,Math.floor(t*8)+1));
    var i;
    for(i=0;i<8;i++){
      var x=px(a[i]), on=(i<shown);
      ctx.beginPath();ctx.moveTo(x,Y-8);ctx.lineTo(x,Y+8);
      ctx.strokeStyle=on?'#334155':'#cbd5e1';ctx.lineWidth=2;ctx.stroke();
      ctx.beginPath();ctx.arc(x,Y,on?9:5,0,Math.PI*2);
      ctx.fillStyle=on?'#f59e0b':'#e2e8f0';ctx.fill();
      if(on){ctx.strokeStyle='#b45309';ctx.lineWidth=2;ctx.stroke();}
      ctx.font='bold 15px sans-serif';ctx.textAlign='center';
      ctx.fillStyle=on?'#1f2937':'#b6c2d2';
      ctx.fillText(a[i],x,Y+30);
      ctx.fillStyle='#94a3b8';ctx.font='13px sans-serif';
      ctx.fillText((i+1)+'번째',x,Y+48);
    }
    for(i=0;i<7;i++){
      if(i>=shown-1) break;
      var x1=px(a[i]), x2=px(a[i+1]);
      ctx.beginPath();
      ctx.moveTo(x1,Y-10);
      ctx.quadraticCurveTo((x1+x2)/2,Y-64,x2,Y-10);
      ctx.strokeStyle='#16a34a';ctx.lineWidth=2.6;ctx.stroke();
      ctx.fillStyle='#15803d';ctx.font='bold 14px sans-serif';ctx.textAlign='center';
      ctx.fillText('+'+S.k,(x1+x2)/2,Y-42);
    }
    ctx.textAlign='left';
    lbl(ctx,'시작 '+S.s+'에서 '+S.k+'씩 뛰어세기',32,44,'#1d4ed8',19);
    ctx.fillStyle='#f1f6fd';ctx.fillRect(20,296,400,66);
    ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(20,296,400,66);
    lbl(ctx,(t===null)?'아직 뛰지 않았다':(shown+'번째 수 : '+a[shown-1]),38,326,'#1f2937',21);
    lbl(ctx,'이웃한 두 수의 차 : '+S.k,38,352,'#52627a',18);
  },
  record:function(S){
    var a=seq(S.s,S.k);
    var pred=S.s; var i;
    for(i=0;i<7;i++){ pred+=S.k; }
    return {s:S.s,k:S.k,n3:a[2],n8:a[7],gap:a[7]-a[0],times:(a[7]-a[0])/S.k,pred:pred};
  },
  headA:['번호','시작','뛰는 수','3번째 수','8번째 수','8번째 − 시작','÷ 뛰는 수','시작 + 뛰는수×7'],
  rowA:function(r,i){
    var ok=(r.pred===r.n8);
    return [i+1,r.s,r.k,r.n3,'<b>'+r.n8+'</b>',r.gap,r.times,
            r.pred+' <span class="'+(ok?'ok':'no')+'">'+(ok?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ok7=0,okPred=0,ks={};
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var a=(r.times===7), b=(r.pred===r.n8);
      if(a) ok7++;
      if(b) okPred++;
      ks[r.k]=true;
      rows.push([r.s+'에서 '+r.k+'씩', r.n8, r.gap, r.times,
                 '<span class="'+(a?'ok':'no')+'">'+(a?'○':'×')+'</span>',
                 r.pred,
                 '<span class="'+(b?'ok':'no')+'">'+(b?'○':'×')+'</span>']);
    }
    var kn=0; for(var k in ks){ kn++; }
    var stats=[
      {t:'(8번째 − 시작) ÷ 뛰는 수 = 7',big:ok7+' / '+rec.length,
       p:'8번째까지 가려면 몇 번 뛰어야 하는지 확인한 결과.'},
      {t:'시작 + 뛰는수 × 7 = 8번째 수',big:okPred+' / '+rec.length,
       p:'한 칸씩 세지 않고 바로 계산해 본 값과 실제 8번째 수 비교.'},
      {t:'시험해 본 뛰는 수',big:kn+'가지',p:'뛰는 수를 바꿔도 규칙이 그대로인지 확인했다.'}
    ];
    var concl;
    if(ok7===rec.length && okPred===rec.length){
      concl='<b>정리</b> — 몇에서 시작하든, 몇씩 뛰든 <b>8번째 수 = 시작 + (뛰는 수 × 7)</b>이었다. '
           +'8번째까지 가려면 뛰는 횟수는 7번(=8−1)이다. 그래서 20번째 수도 하나씩 세지 않고 바로 구할 수 있다.';
    } else {
      concl='<b>확인 필요</b> — 규칙과 맞지 않는 기록이 있다. 뛰는 수가 도중에 바뀌지 않았는지 확인해 보자.';
    }
    return {head:['배열','8번째 수','8번째 − 시작','÷ 뛰는 수','7인가?','시작+뛰는수×7','같은가?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# LAB 3 : 성냥개비 도형 패턴
# ============================================================
LAB_STICK = r"""
function lbl(ctx,t,x,y,c,sz,al){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
function key(p){return Math.round(p[0])+','+Math.round(p[1]);}
function addSeg(list,seen,p,q){
  var k1=key(p)+'|'+key(q), k2=key(q)+'|'+key(p);
  if(seen[k1]||seen[k2]) return;
  seen[k1]=true; list.push([p,q]);
}
function buildSegs(shape,n){
  var list=[],seen={},i;
  if(shape===4){
    var u=34, x0=34, y0=120;
    for(i=0;i<n;i++){
      var x=x0+i*u;
      addSeg(list,seen,[x,y0],[x+u,y0]);
      addSeg(list,seen,[x,y0],[x,y0+u]);
      addSeg(list,seen,[x,y0+u],[x+u,y0+u]);
      addSeg(list,seen,[x+u,y0],[x+u,y0+u]);
    }
  } else {
    var s=36, h=31, bx=48, yb=162, yt=162-h;
    for(i=0;i<n;i++){
      var x=bx+(s/2)*i;
      if(i%2===0){
        addSeg(list,seen,[x,yb],[x+s,yb]);
        addSeg(list,seen,[x,yb],[x+s/2,yt]);
        addSeg(list,seen,[x+s,yb],[x+s/2,yt]);
      } else {
        addSeg(list,seen,[x,yt],[x+s,yt]);
        addSeg(list,seen,[x,yt],[x+s/2,yb]);
        addSeg(list,seen,[x+s,yt],[x+s/2,yb]);
      }
    }
  }
  return list;
}

var LAB = {
  cw:440, ch:400, cvTitle:'성냥개비 도형판',
  action:'한 개씩 이어 붙이기',
  hint0:'모양과 개수를 정하고 이어 붙여 보자. 붙은 도형은 변을 함께 쓴다.',
  sliders:[
    {id:'shape',label:'모양 (3 = 삼각형 / 4 = 사각형)',min:3,max:4,value:4,color:'#2563eb',
     fmt:function(v){return v===3?'삼각형':'사각형';}},
    {id:'n',label:'도형 개수',min:1,max:10,value:4,color:'#16a34a',unit:'개'}
  ],
  readout:function(S,ran){
    var segs=buildSegs(S.shape,S.n);
    return [{k:'따로따로 만들면',v:(S.shape*S.n)+'개'},
            {k:'이어 붙이면',v:ran?(segs.length+'개'):'붙여 보자'}];
  },
  doneMsg:function(S){
    var segs=buildSegs(S.shape,S.n);
    return (S.shape===3?'삼각형 ':'사각형 ')+S.n+'개를 이어 붙이니 성냥개비 '+segs.length+'개가 들었다. 따로 만들 때보다 '+(S.shape*S.n-segs.length)+'개 적다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var segs=buildSegs(S.shape,S.n);
    var shown=(t===null)?0:Math.ceil(t*segs.length);
    if(t!==null&&t>=1) shown=segs.length;
    var i;
    for(i=0;i<segs.length;i++){
      var a=segs[i][0], b=segs[i][1];
      var on=(i<shown);
      ctx.beginPath();ctx.moveTo(a[0],a[1]);ctx.lineTo(b[0],b[1]);
      ctx.strokeStyle=on?'#d97706':'#e5e9f0';
      ctx.lineWidth=on?6:4;ctx.lineCap='round';ctx.stroke();
      if(on){
        ctx.beginPath();ctx.arc(a[0],a[1],3.4,0,Math.PI*2);
        ctx.fillStyle='#7c2d12';ctx.fill();
      }
    }
    ctx.lineCap='butt';
    lbl(ctx,(S.shape===3?'삼각형 ':'사각형 ')+S.n+'개 이어 붙이기',34,44,'#1d4ed8',19);
    lbl(ctx,'놓인 성냥개비 : '+shown+'개',34,70,'#b45309',18);

    ctx.fillStyle='#f1f6fd';ctx.fillRect(20,268,400,114);
    ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(20,268,400,114);
    lbl(ctx,'따로 만들면 : '+S.shape+' × '+S.n+' = '+(S.shape*S.n)+'개',38,300,'#52627a',19);
    lbl(ctx,'이어 붙이면 : '+((t===null)?'?':segs.length+'개'),38,330,'#1f2937',21);
    lbl(ctx,'함께 쓴 변 : '+((t===null)?'?':(S.shape*S.n-segs.length)+'개'),38,360,'#b45309',19);
  },
  record:function(S){
    var segs=buildSegs(S.shape,S.n);
    return {shape:S.shape,n:S.n,used:segs.length,naive:S.shape*S.n,
            shared:S.shape*S.n-segs.length,
            perShape:(segs.length-1)/S.n};
  },
  headA:['번호','모양','개수','따로 만들면','이어 붙이면','함께 쓴 변','(성냥−1) ÷ 개수'],
  rowA:function(r,i){
    return [i+1,(r.shape===3?'삼각형':'사각형'),r.n,r.naive,'<b>'+r.used+'</b>',r.shared,r.perShape];
  },
  analyze:function(rec){
    var rows=[],sharedOk=0,ruleOk=0,tri=0,sq=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var a=(r.shared===r.n-1);
      var want=r.shape-1;
      var b=(r.perShape===want);
      if(a) sharedOk++;
      if(b) ruleOk++;
      if(r.shape===3) tri++; else sq++;
      rows.push([(r.shape===3?'삼각형':'사각형')+' '+r.n+'개', r.used, r.naive, r.shared,
                 '<span class="'+(a?'ok':'no')+'">'+(a?'○':'×')+'</span>',
                 r.perShape,
                 '<span class="'+(b?'ok':'no')+'">'+(b?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'함께 쓴 변 = 도형 개수 − 1',big:sharedOk+' / '+rec.length,
       p:'도형이 붙은 자리마다 변 하나를 아꼈다.'},
      {t:'(성냥개비 − 1) ÷ 도형 개수',big:ruleOk+' / '+rec.length,
       p:'삼각형은 2, 사각형은 3이 나오는지 확인한 결과.'},
      {t:'시험한 모양',big:'삼각형 '+tri+' / 사각형 '+sq,
       p:tri&&sq?'두 모양 모두 확인했다.':'다른 모양도 해 보면 규칙을 더 확실히 알 수 있다.'}
    ];
    var concl;
    if(sharedOk===rec.length && ruleOk===rec.length){
      concl='<b>정리</b> — 도형을 따로 만들면 (변의 수 × 개수)만큼 필요하지만, 이어 붙이면 붙는 자리마다 변 하나를 함께 써서 '
           +'<b>도형 개수 − 1</b>개만큼 줄었다. 그래서 성냥개비 수는 <b>(변의 수 − 1) × 도형 개수 + 1</b>이다. '
           +'삼각형은 2씩, 사각형은 3씩 늘어난다.';
    } else {
      concl='<b>확인 필요</b> — 규칙과 어긋난 기록이 있다. 도형이 한 줄로 이어졌는지 확인해 보자.';
    }
    return {head:['모양과 개수','성냥개비','따로 만들면','함께 쓴 변','개수−1인가?','(성냥−1)÷개수','변의 수−1인가?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# LAB 4 : 반복 무늬의 규칙
# ============================================================
LAB_PATTERN = r"""
function lbl(ctx,t,x,y,c,sz,al){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
var COLS=['#ef4444','#f59e0b','#3b82f6','#22c55e','#a855f7','#ec4899'];
var NAMES=['빨강','노랑','파랑','초록','보라','분홍'];

var LAB = {
  cw:440, ch:420, cvTitle:'반복 무늬판',
  action:'무늬를 늘어놓기',
  hint0:'몇 개짜리 무늬를 반복할지, 몇 번째를 찾을지 정해 보자.',
  sliders:[
    {id:'p',label:'반복되는 무늬의 길이',min:2,max:6,value:3,color:'#2563eb',unit:'칸'},
    {id:'n',label:'찾을 순서',min:1,max:40,value:17,color:'#16a34a',unit:'번째'}
  ],
  readout:function(S,ran){
    var idx=(S.n-1)%S.p;
    return [{k:'무늬',v:'['+NAMES.slice(0,S.p).join(' ')+'] 반복'},
            {k:S.n+'번째 색',v:ran?NAMES[idx]:'늘어놓아 보자'}];
  },
  doneMsg:function(S){
    var idx=(S.n-1)%S.p;
    return S.n+'번째는 '+NAMES[idx]+'이다. ('+S.n+'−1)을 '+S.p+'로 나눈 나머지가 '+idx+'이기 때문이다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var p=S.p, n=S.n;
    var shown=(t===null)?0:Math.ceil(t*n);
    if(t!==null&&t>=1) shown=n;
    var cell=34, per=10, x0=36, y0=80;
    for(var i=0;i<n;i++){
      var cx=x0+(i%per)*(cell+4), cy=y0+Math.floor(i/per)*(cell+16);
      var on=(i<shown);
      ctx.fillStyle=on?COLS[i%p]:'#eef1f6';
      ctx.fillRect(cx,cy,cell,cell);
      ctx.strokeStyle=(i===n-1&&on)?'#111827':'#cbd5e1';
      ctx.lineWidth=(i===n-1&&on)?4:1.5;
      ctx.strokeRect(cx,cy,cell,cell);
      ctx.fillStyle='#94a3b8';ctx.font='12px sans-serif';ctx.textAlign='center';
      ctx.fillText(i+1,cx+cell/2,cy+cell+13);
    }
    ctx.textAlign='left';
    lbl(ctx,p+'칸 무늬를 반복해서 '+n+'번째까지',36,44,'#1d4ed8',19);

    ctx.fillStyle='#f1f6fd';ctx.fillRect(20,318,400,86);
    ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(20,318,400,86);
    if(t===null){
      lbl(ctx,'아직 늘어놓지 않았다',38,352,'#1f2937',21);
      lbl(ctx,'하나씩 세지 않고 알 수 있을까?',38,382,'#52627a',18);
    } else {
      var idx=(n-1)%p;
      lbl(ctx,'('+n+' − 1) ÷ '+p+' 의 나머지 = '+idx,38,352,'#52627a',19);
      lbl(ctx,n+'번째 색 : '+NAMES[idx],38,382,'#1f2937',21);
      ctx.fillStyle=COLS[idx];ctx.fillRect(300,364,26,26);
      ctx.strokeStyle='#334155';ctx.lineWidth=2;ctx.strokeRect(300,364,26,26);
    }
  },
  record:function(S){
    var idx=(S.n-1)%S.p;
    var cnt=0,i;
    for(i=1;i<=S.n;i++){ cnt++; }
    return {p:S.p,n:S.n,idx:idx,name:NAMES[idx],cnt:cnt};
  },
  headA:['번호','무늬 길이','순서','(순서−1) ÷ 무늬길이 나머지','색'],
  rowA:function(r,i){
    return [i+1,r.p+'칸',r.n+'번째',r.idx,'<b>'+r.name+'</b>'];
  },
  analyze:function(rec){
    var rows=[],map={},pairs=0,agree=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var k=r.p+'-'+r.idx;
      var note='첫 기록';
      if(map[k]){
        pairs++;
        var same=(map[k]===r.name);
        if(same) agree++;
        note='<span class="'+(same?'ok':'no')+'">'+(same?'같은 색':'다른 색')+'</span>';
      } else { map[k]=r.name; }
      rows.push([r.p+'칸 무늬', r.n+'번째', r.idx, '<b>'+r.name+'</b>', note]);
    }
    var maxn=0; for(i=0;i<rec.length;i++){ if(rec[i].n>maxn) maxn=rec[i].n; }
    var stats=[
      {t:'나머지가 같은 짝',big:pairs+'쌍',
       p:pairs?'무늬 길이와 나머지가 같은 기록끼리 비교했다.':'같은 무늬 길이로 순서만 바꿔 기록하면 비교할 수 있다.'},
      {t:'그중 색이 같았던 짝',big:pairs?(agree+' / '+pairs):'비교 없음',
       p:'나머지가 같으면 색도 같은지 확인한 결과.'},
      {t:'가장 멀리 본 순서',big:maxn+'번째',
       p:'하나씩 세지 않고 나눗셈으로 바로 찾을 수 있었다.'}
    ];
    var concl;
    if(pairs===0){
      concl='<b>더 해 보자</b> — 같은 무늬 길이에서 순서를 바꿔 기록해 보자. 3칸 무늬라면 5번째와 17번째처럼 나머지가 같은 짝을 만들면 규칙이 보인다.';
    } else if(agree===pairs){
      concl='<b>정리</b> — 무늬 길이가 같고 (순서−1)을 나눈 <b>나머지가 같으면 색도 항상 같았다.</b> '
           +'반복되는 무늬에서는 몇 번째인지 하나씩 세지 않아도, 나머지만 구하면 무슨 색인지 바로 알 수 있다.';
    } else {
      concl='<b>확인 필요</b> — 나머지가 같은데 색이 다른 기록이 있다. 무늬 길이를 다시 확인해 보자.';
    }
    return {head:['무늬 길이','순서','나머지','색','같은 나머지끼리'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# LAB 5 : □가 있는 식
# ============================================================
LAB_BOX = r"""
function lbl(ctx,t,x,y,c,sz,al){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}

var LAB = {
  cw:440, ch:420, cvTitle:'구슬 가리기판',
  action:'가리고 □ 구하기',
  hint0:'구슬을 두 묶음으로 나눠 놓자. 한 묶음을 가린 뒤 □를 구해 본다.',
  sliders:[
    {id:'a',label:'보이는 묶음',min:1,max:20,value:7,color:'#2563eb',unit:'개'},
    {id:'b',label:'가릴 묶음',min:1,max:20,value:9,color:'#f59e0b',unit:'개'}
  ],
  readout:function(S,ran){
    return [{k:'전체',v:(S.a+S.b)+'개'},
            {k:'식',v:S.a+' + □ = '+(S.a+S.b)}];
  },
  doneMsg:function(S){
    return '전체 '+(S.a+S.b)+'개에서 보이는 '+S.a+'개를 빼면 □ = '+S.b+'. 가린 구슬 수와 같은지 확인해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var a=S.a,b=S.b,T=a+b;
    var per=10, cell=34, x0=36, y0=92;
    for(var i=0;i<T;i++){
      var cx=x0+(i%per)*cell+cell/2, cy=y0+Math.floor(i/per)*cell+cell/2;
      ctx.beginPath();ctx.arc(cx,cy,12,0,Math.PI*2);
      ctx.fillStyle=(i<a)?'#60a5fa':'#fbbf24';
      ctx.fill();
      ctx.lineWidth=2;ctx.strokeStyle=(i<a)?'#1d4ed8':'#b45309';ctx.stroke();
    }
    if(t!==null){
      var cover=Math.min(1,t/0.6);
      var startIdx=a;
      var x1=x0+(startIdx%per)*cell;
      var row1=Math.floor(startIdx/per), row2=Math.floor((T-1)/per);
      ctx.globalAlpha=0.94*cover;
      ctx.fillStyle='#475569';
      for(var r=row1;r<=row2;r++){
        var from=(r===row1)?(startIdx%per):0;
        var to=(r===row2)?((T-1)%per):(per-1);
        ctx.fillRect(x0+from*cell-2, y0+r*cell-2, (to-from+1)*cell+4, cell+4);
      }
      ctx.globalAlpha=1;
      if(cover>=1){
        ctx.fillStyle='#fff';ctx.font='bold 26px sans-serif';ctx.textAlign='center';
        ctx.fillText('□', x0+(row1===row2? ((startIdx%per)+(((T-1)%per)))/2*cell+cell/2 : 200), y0+row1*cell+cell/2+9);
        ctx.textAlign='left';
      }
    }
    lbl(ctx,'구슬 전체 '+T+'개 중 '+a+'개만 보인다',36,44,'#1d4ed8',19);
    lbl(ctx,(t===null)?'아직 가리지 않았다':'가린 묶음이 □',36,68,'#52627a',17);

    ctx.fillStyle='#f1f6fd';ctx.fillRect(20,296,400,108);
    ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(20,296,400,108);
    lbl(ctx,a+' + □ = '+T,38,330,'#1f2937',24);
    if(t===null){
      lbl(ctx,'□는 얼마일까?',38,362,'#52627a',19);
      lbl(ctx,'= 뒤의 수를 그냥 쓰면 될까?',38,390,'#94a3b8',17);
    } else {
      lbl(ctx,'□ = '+T+' − '+a+' = '+(T-a),38,362,'#1d4ed8',21);
      lbl(ctx,'가려 둔 구슬 : '+b+'개',38,390,'#b45309',19);
    }
  },
  record:function(S){
    var T=S.a+S.b;
    return {a:S.a,b:S.b,T:T,byMinus:T-S.a,byEnd:T};
  },
  headA:['번호','식','가려 둔 수','전체 − 보이는 수','맞았나?','= 뒤의 수로 답했다면'],
  rowA:function(r,i){
    var ok=(r.byMinus===r.b);
    var wrong=(r.byEnd===r.b);
    return [i+1,r.a+' + □ = '+r.T,'<b>'+r.b+'</b>',r.byMinus,
            '<span class="'+(ok?'ok':'no')+'">'+(ok?'○':'×')+'</span>',
            r.byEnd+' <span class="'+(wrong?'ok':'no')+'">'+(wrong?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ok=0,endOk=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var a=(r.byMinus===r.b), b2=(r.byEnd===r.b);
      if(a) ok++;
      if(b2) endOk++;
      rows.push([r.a+' + □ = '+r.T, '<b>'+r.b+'</b>', r.byMinus,
                 '<span class="'+(a?'ok':'no')+'">'+(a?'○':'×')+'</span>',
                 r.byEnd,
                 '<span class="'+(b2?'ok':'no')+'">'+(b2?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'“전체 − 보이는 수”가 맞은 횟수',big:ok+' / '+rec.length,
       p:'뺄셈으로 거꾸로 구한 값과 실제 가린 수를 비교했다.'},
      {t:'“= 뒤의 수”가 맞은 횟수',big:endOk+' / '+rec.length,
       p:'등호 뒤의 수를 그대로 답으로 쓰면 어떻게 되는지 확인했다.'},
      {t:'기록한 식',big:rec.length+'개',p:'보이는 묶음과 가린 묶음을 바꿔 가며 확인했다.'}
    ];
    var concl;
    if(ok===rec.length && endOk===0){
      concl='<b>정리</b> — □는 언제나 <b>전체에서 보이는 수를 뺀 값</b>이었고, = 뒤의 수를 그대로 쓴 답은 한 번도 맞지 않았다. '
           +'덧셈식의 □는 뺄셈으로 거꾸로 구한다. 7 + □ = 16이면 □ = 16 − 7이다.';
    } else if(ok===rec.length){
      concl='<b>정리</b> — □는 항상 전체에서 보이는 수를 뺀 값이었다. = 뒤의 수를 그대로 쓴 답이 맞은 경우도 있는데, 보이는 묶음이 아주 작을 때뿐인 우연이다. 값을 바꿔 더 확인해 보자.';
    } else {
      concl='<b>확인 필요</b> — 뺄셈으로 구한 값이 가린 수와 다른 기록이 있다. 수를 다시 확인해 보자.';
    }
    return {head:['식','가려 둔 수','전체 − 보이는 수','맞았나?','= 뒤의 수','맞았나?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("elem34_balance_equal_sign_lab.html",
     "양팔저울 실험실 — 등호는 “답을 쓰시오”라는 뜻일까?",
     "양팔저울 실험실 — 등호는 “답을 쓰시오”라는 뜻일까?",
     "양쪽 접시에 서로 다른 식을 올려 저울이 언제 평평해지는지 기록하고, 등호의 뜻을 확인한다.",
     LAB_SCALE),
    ("elem34_skip_counting_lab.html",
     "뛰어세기 실험실 — 8번째 수를 바로 알 수 있을까?",
     "뛰어세기 실험실 — 8번째 수를 바로 알 수 있을까?",
     "수직선 위에서 일정하게 뛰어 세고, 몇 번째 수를 한 칸씩 세지 않고 구할 수 있는지 확인한다.",
     LAB_SKIP),
    ("elem34_matchstick_pattern_lab.html",
     "성냥개비 실험실 — 사각형 10개엔 40개가 필요할까?",
     "성냥개비 실험실 — 사각형 10개엔 40개가 필요할까?",
     "도형을 한 줄로 이어 붙이며 실제로 쓰인 성냥개비를 세고, 늘어나는 규칙을 찾는다.",
     LAB_STICK),
    ("elem34_repeating_pattern_lab.html",
     "반복 무늬 실험실 — 30번째 색을 세지 않고 알 수 있을까?",
     "반복 무늬 실험실 — 30번째 색을 세지 않고 알 수 있을까?",
     "무늬를 반복해 늘어놓고 몇 번째 색을 기록해, 나머지로 색을 예측할 수 있는지 확인한다.",
     LAB_PATTERN),
    ("elem34_unknown_box_lab.html",
     "□ 구하기 실험실 — □는 = 뒤의 수일까?",
     "□ 구하기 실험실 — □는 = 뒤의 수일까?",
     "구슬 한 묶음을 가려 □를 만들고, 전체에서 빼서 구한 값이 실제 가린 수와 같은지 확인한다.",
     LAB_BOX),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html, "토큰 누수: " + fname
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c2_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
