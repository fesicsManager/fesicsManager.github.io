# -*- coding: utf-8 -*-
"""중1 '자료와 가능성' 실험 4종"""
import os, re, random

OUT = "/mnt/user-data/outputs"
src = open("/home/claude/gen_math_labs.py", encoding="utf-8").read()
TPL = re.search(r'TPL = r"""(.*?)"""\n', src, re.S).group(1)

random.seed(31415)
DATA = sorted(max(40, min(99, int(random.gauss(72, 14)))) for _ in range(30))
DATA_JS = "var DATA=" + str(DATA).replace(" ", "") + ";"

BASE = r"""
function lbl(ctx,t,x,y,c,sz,al){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
function box(ctx,x,y,w,h){ctx.fillStyle='#f1f6fd';ctx.fillRect(x,y,w,h);ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(x,y,w,h);}
function r1(v){return Math.round(v*10)/10;}
function r2(v){return Math.round(v*100)/100;}
function r3(v){return Math.round(v*1000)/1000;}
""" + DATA_JS + r"""
var LO=40, HI=100;
function bins(w){
  var n=Math.ceil((HI-LO)/w), f=[],i,j;
  for(i=0;i<n;i++) f.push(0);
  for(j=0;j<DATA.length;j++){
    var k=Math.floor((DATA[j]-LO)/w);
    if(k>=n) k=n-1;
    f[k]++;
  }
  return {n:n,f:f,w:w};
}
function realMean(){
  var s=0,i;
  for(i=0;i<DATA.length;i++) s+=DATA[i];
  return s/DATA.length;
}
"""

WS = "var WS=[5,10,20];"

# ============================================================
# 1. 계급의 크기와 히스토그램
# ============================================================
LAB_HIST = BASE + WS + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'히스토그램판',
  action:'히스토그램 그리기',
  hint0:'같은 자료 30개를 몇 점 단위로 묶을지 정해 보자.',
  sliders:[
    {id:'wi',label:'계급의 크기',min:0,max:2,value:1,color:'#2563eb',fmt:function(v){return WS[v]+'점';}}
  ],
  readout:function(S,ran){
    var b=bins(WS[S.wi]);
    return [{k:'계급의 크기',v:WS[S.wi]+'점'},
            {k:'계급의 개수',v:ran?(b.n+'개'):'그려 보자'}];
  },
  doneMsg:function(S){
    var b=bins(WS[S.wi]),i,mx=0,mi=0,s=0;
    for(i=0;i<b.n;i++){ s+=b.f[i]; if(b.f[i]>mx){ mx=b.f[i]; mi=i; } }
    return '계급 '+b.n+'개, 도수의 합 '+s+'명. 가장 많은 계급은 '+(LO+mi*b.w)+'~'+(LO+(mi+1)*b.w)+'점('+mx+'명)이다. 계급 크기를 바꿔 다시 그려 보자.';
  },
  draw:function(ctx,S,t,ran){
    var b=bins(WS[S.wi]), i;
    var grow=(t===null)?0:Math.min(1,t);
    var GX=54, GY=300, GW=350, GH=210;
    var mx=1;
    for(i=0;i<b.n;i++){ if(b.f[i]>mx) mx=b.f[i]; }
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+GW,GY);ctx.moveTo(GX,GY);ctx.lineTo(GX,GY-GH-10);ctx.stroke();
    for(i=0;i<=mx;i++){
      if(mx>10&&i%2!==0) continue;
      var y=GY-GH*i/mx;
      ctx.strokeStyle='#eef2f7';ctx.lineWidth=1.2;
      ctx.beginPath();ctx.moveTo(GX,y);ctx.lineTo(GX+GW,y);ctx.stroke();
      ctx.fillStyle='#64748b';ctx.font='12px sans-serif';ctx.textAlign='right';
      ctx.fillText(i,GX-6,y+4);
    }
    var bw=GW/b.n;
    for(i=0;i<b.n;i++){
      var h=GH*b.f[i]/mx*grow;
      ctx.fillStyle='#93c5fd';ctx.fillRect(GX+i*bw,GY-h,bw-1,h);
      ctx.strokeStyle='#2563eb';ctx.lineWidth=2;ctx.strokeRect(GX+i*bw,GY-h,bw-1,h);
      ctx.fillStyle='#475569';ctx.font=(b.n>8)?'10px sans-serif':'12px sans-serif';ctx.textAlign='center';
      ctx.fillText(LO+i*b.w,GX+i*bw+bw/2,GY+16);
      if(grow>=1){ ctx.fillStyle='#1d4ed8';ctx.font='bold 12px sans-serif';ctx.fillText(b.f[i],GX+i*bw+bw/2,GY-h-6); }
    }
    ctx.textAlign='left';
    lbl(ctx,'수학 점수 30명 (계급의 크기 '+b.w+'점)',24,32,'#1d4ed8',18);
    var s=0,mi=0,mm=0;
    for(i=0;i<b.n;i++){ s+=b.f[i]; if(b.f[i]>mm){ mm=b.f[i]; mi=i; } }
    box(ctx,20,332,400,80);
    lbl(ctx,(t===null)?'계급을 어떻게 묶어야 할까?':('계급 '+b.n+'개    도수의 합 '+s+'명'),38,364,'#1f2937',19);
    lbl(ctx,(t===null)?'':('가장 많은 계급 : '+(LO+mi*b.w)+' ~ '+(LO+(mi+1)*b.w)+'점 ('+mm+'명)'),38,394,'#b45309',18);
  },
  record:function(S){
    var b=bins(WS[S.wi]),i,s=0,mm=0,mi=0;
    for(i=0;i<b.n;i++){ s+=b.f[i]; if(b.f[i]>mm){ mm=b.f[i]; mi=i; } }
    return {w:b.w,n:b.n,sum:s,top:(LO+mi*b.w)+'~'+(LO+(mi+1)*b.w),topF:mm,
            f:b.f.join(', ')};
  },
  headA:['번호','계급의 크기','계급 개수','도수','도수의 합','가장 많은 계급','그 도수'],
  rowA:function(r,i){
    return [i+1,r.w+'점',r.n+'개',r.f,'<b>'+r.sum+'</b>',r.top+'점',r.topF+'명'];
  },
  analyze:function(rec){
    var rows=[],ok=0,tops={},tn=0,ws={},wn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i], a=(r.sum===30);
      if(a) ok++;
      tops[r.top]=true; ws[r.w]=true;
      rows.push([r.w+'점', r.n+'개', '<b>'+r.sum+'</b>',
                 '<span class="'+(a?'ok':'no')+'">'+(a?'○':'×')+'</span>',
                 r.top+'점', r.topF+'명']);
    }
    for(var k in tops) tn++;
    for(var k2 in ws) wn++;
    var stats=[
      {t:'도수의 합 = 자료 수(30)',big:ok+' / '+rec.length,
       p:'어떻게 묶어도 자료의 개수는 변하지 않는다.'},
      {t:'시험한 계급의 크기',big:wn+'가지',p:wn>1?'같은 자료를 다르게 묶어 봤다.':'계급의 크기를 바꿔 더 기록해 보자.'},
      {t:'가장 많은 계급이 달라진 종류',big:tn+'가지',
       p:tn>1?'묶는 방법에 따라 “가장 많은 구간”이 달라졌다.':'계급 크기를 5점과 20점으로 바꿔 비교해 보자.'}
    ];
    var concl;
    if(wn<2){
      concl='<b>더 해 보자</b> — 계급의 크기를 바꿔 <b>같은 자료를 여러 방법으로</b> 묶어 봐야 한다.';
    } else {
      concl='<b>정리</b> — 자료는 하나도 바뀌지 않았고 도수의 합도 언제나 30이었지만, '
           +'계급의 크기에 따라 히스토그램의 <b>모양과 계급의 개수가 달라졌다.</b>'
           +(tn>1?' “가장 많은 구간”까지 바뀌었다.':'')
           +' 계급이 너무 크면 자료의 흩어진 모습이 뭉개지고, 너무 작으면 들쭉날쭉해진다. '
           +'그래서 히스토그램을 읽을 때는 계급의 크기를 먼저 봐야 한다.';
    }
    return {head:['계급 크기','계급 개수','도수의 합','30인가?','가장 많은 계급','도수'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 도수분포표에서의 평균
# ============================================================
LAB_TMEAN = BASE + WS + r"""
var LAB = {
  cw:440, ch:420, cvTitle:'계급값 평균판',
  action:'계급값으로 평균 구하기',
  hint0:'계급의 크기를 정하고, 계급값으로 평균을 어림해 보자.',
  sliders:[
    {id:'wi',label:'계급의 크기',min:0,max:2,value:1,color:'#2563eb',fmt:function(v){return WS[v]+'점';}}
  ],
  calc:function(S){
    var b=bins(WS[S.wi]),i,s=0,n=0;
    for(i=0;i<b.n;i++){
      var mid=LO+b.w*i+b.w/2;
      s+=mid*b.f[i]; n+=b.f[i];
    }
    return {b:b,est:s/n,real:realMean(),n:n};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'계급값으로 어림한 평균',v:ran?(r2(c.est)+'점'):'구해 보자'},
            {k:'원자료의 실제 평균',v:r2(c.real)+'점'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '어림한 평균 '+r2(c.est)+'점, 실제 평균 '+r2(c.real)+'점. 차이는 '+r2(Math.abs(c.est-c.real))+'점이다. 계급 크기를 바꿔 다시 해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), b=c.b, i;
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*b.n);
    var X0=40, Y0=76, RH=28;
    var cw2=[100,66,66,100];
    var head=['계급(점)','도수','계급값','계급값×도수'];
    var x=X0;
    for(i=0;i<4;i++){
      ctx.fillStyle='#eaf1fa';ctx.fillRect(x,Y0,cw2[i],RH);
      ctx.strokeStyle='#94a3b8';ctx.lineWidth=1.4;ctx.strokeRect(x,Y0,cw2[i],RH);
      ctx.fillStyle='#334155';ctx.font='bold 13px sans-serif';ctx.textAlign='center';
      ctx.fillText(head[i],x+cw2[i]/2,Y0+19);
      x+=cw2[i];
    }
    var rows=Math.min(b.n,8);
    for(i=0;i<rows;i++){
      var y=Y0+RH+i*RH, on=(i<shown);
      var mid=LO+b.w*i+b.w/2;
      var vals=[(LO+b.w*i)+'~'+(LO+b.w*(i+1)), ''+b.f[i], on?(''+mid):'?', on?(''+(mid*b.f[i])):'?'];
      x=X0;
      var j;
      for(j=0;j<4;j++){
        ctx.fillStyle='#fff';ctx.fillRect(x,y,cw2[j],RH);
        ctx.strokeStyle='#cbd5e1';ctx.lineWidth=1.2;ctx.strokeRect(x,y,cw2[j],RH);
        ctx.fillStyle=(j>=2&&!on)?'#cbd5e1':'#1f2937';
        ctx.font='13px sans-serif';ctx.textAlign='center';
        ctx.fillText(vals[j],x+cw2[j]/2,y+19);
        x+=cw2[j];
      }
    }
    ctx.textAlign='left';
    if(b.n>8) lbl(ctx,'... 아래 '+(b.n-8)+'개 계급 생략',X0,Y0+RH+8*RH+18,'#94a3b8',14);
    lbl(ctx,'계급의 크기 '+b.w+'점',24,40,'#1d4ed8',19);
    box(ctx,20,326,400,84);
    lbl(ctx,(t===null)?'계급값으로 구한 평균은 정확할까?':('어림한 평균 : '+r2(c.est)+'점'),38,356,'#1f2937',20);
    lbl(ctx,'실제 평균 : '+r2(c.real)+'점'+((t===null)?'':('     차이 '+r2(Math.abs(c.est-c.real))+'점')),
        38,388,'#b45309',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {w:WS[S.wi],n:c.b.n,est:r2(c.est),real:r2(c.real),gap:r2(Math.abs(c.est-c.real)),
            same:(Math.abs(c.est-c.real)<0.005)};
  },
  headA:['번호','계급의 크기','계급 개수','어림한 평균','실제 평균','차이','같은가?'],
  rowA:function(r,i){
    return [i+1,r.w+'점',r.n+'개','<b>'+r.est+'</b>',r.real,r.gap,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,mn=999,mnw=0,mx=0,mxw=0,ws={},wn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.gap<mn){ mn=r.gap; mnw=r.w; }
      if(r.gap>mx){ mx=r.gap; mxw=r.w; }
      ws[r.w]=true;
      rows.push([r.w+'점', r.n+'개', '<b>'+r.est+'</b>', r.real, r.gap,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>']);
    }
    for(var k in ws) wn++;
    var stats=[
      {t:'어림한 평균이 실제와 같았던 횟수',big:same+' / '+rec.length,
       p:'계급값은 그 계급의 한가운데 값일 뿐, 실제 자료값이 아니다.'},
      {t:'차이가 가장 작았던 경우',big:mn+'점',p:mnw?('계급의 크기 '+mnw+'점일 때.'):''},
      {t:'차이가 가장 컸던 경우',big:mx+'점',p:mxw?('계급의 크기 '+mxw+'점일 때.'):''}
    ];
    var concl;
    if(wn<2){
      concl='<b>더 해 보자</b> — 계급의 크기를 바꿔 여러 번 기록해야 차이의 변화를 볼 수 있다.';
    } else if(same===0){
      concl='<b>정리</b> — 계급값으로 구한 평균은 <b>한 번도 실제 평균과 정확히 같지 않았다.</b> '
           +'도수분포표는 원자료를 계급값 하나로 대신하기 때문에 정보가 조금 사라진다. '
           +'내 기록에서는 계급의 크기가 '+mnw+'점일 때 차이가 가장 작았고('+mn+'점), '+mxw+'점일 때 가장 컸다('+mx+'점). '
           +'계급이 작다고 항상 더 정확한 것은 아니다. 계급값이 그 계급 자료들의 실제 평균과 얼마나 가까운지에 달려 있기 때문이다. '
           +'어느 쪽이든 도수분포표의 평균은 <b>정확한 값이 아니라 어림값</b>이다.';
    } else {
      concl='<b>정리</b> — 계급값 평균은 어림값이다. 우연히 실제와 같아지는 경우도 있지만 일반적으로는 다르다.';
    }
    return {head:['계급 크기','계급 개수','어림 평균','실제 평균','차이','같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 상대도수
# ============================================================
LAB_REL = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'상대도수 비교판',
  action:'상대도수 구하기',
  hint0:'두 반의 전체 인원과 해당 계급의 도수를 정해 보자.',
  sliders:[
    {id:'fa',label:'1반 해당 계급 도수',min:0,max:30,value:9,color:'#dc2626',unit:'명'},
    {id:'na',label:'1반 전체',min:1,max:30,value:20,color:'#f87171',unit:'명'},
    {id:'fb',label:'2반 해당 계급 도수',min:0,max:30,value:12,color:'#2563eb',unit:'명'},
    {id:'nb',label:'2반 전체',min:1,max:30,value:30,color:'#60a5fa',unit:'명'}
  ],
  calc:function(S){
    var fa=Math.min(S.fa,S.na), fb=Math.min(S.fb,S.nb);
    return {fa:fa,fb:fb,ra:fa/S.na,rb:fb/S.nb};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'1반 상대도수',v:ran?r3(c.ra):'구해 보자'},
            {k:'2반 상대도수',v:ran?r3(c.rb):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    var more=(c.fa>c.fb)?'1반':((c.fb>c.fa)?'2반':'같음');
    var high=(c.ra>c.rb)?'1반':((c.rb>c.ra)?'2반':'같음');
    return '도수가 많은 쪽은 '+more+', 상대도수가 큰 쪽은 '+high+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var grow=(t===null)?0:Math.min(1,t);
    function row(y,name,f,n,rel,col){
      lbl(ctx,name+'   '+f+' / '+n,36,y-10,'#334155',18);
      var BX=36,BW=368;
      for(i=0;i<n;i++){
        var w=BW/n;
        ctx.fillStyle=(i<f)?col:'#e8eef7';
        ctx.fillRect(BX+i*w,y,w-1.2,30);
      }
      ctx.strokeStyle='#334155';ctx.lineWidth=2;ctx.strokeRect(BX,y,BW,30);
      if(grow>0){
        ctx.fillStyle=col;ctx.font='bold 18px sans-serif';ctx.textAlign='right';
        ctx.fillText('상대도수 '+r3(rel*grow),BX+BW,y+54);ctx.textAlign='left';
      }
    }
    lbl(ctx,'어느 반에 이 계급 학생이 더 많을까?',24,36,'#1d4ed8',19);
    row(70,'1반',c.fa,S.na,c.ra,'#ef4444');
    row(180,'2반',c.fb,S.nb,c.rb,'#3b82f6');
    var more=(c.fa>c.fb)?'1반':((c.fb>c.fa)?'2반':'같음');
    var high=(c.ra>c.rb)?'1반':((c.rb>c.ra)?'2반':'같음');
    box(ctx,20,272,400,110);
    lbl(ctx,'도수가 많은 쪽 : '+more+'  ('+c.fa+' vs '+c.fb+')',38,304,'#52627a',18);
    lbl(ctx,(t===null)?'상대도수는 어느 쪽이 클까?':('상대도수가 큰 쪽 : '+high+'  ('+r3(c.ra)+' vs '+r3(c.rb)+')'),
        38,336,'#1f2937',19);
    lbl(ctx,(t===null)?'':((more!==high&&more!=='같음'&&high!=='같음')?'두 답이 다르다!':'두 답이 같다'),
        38,366,(more!==high)?'#b91c1c':'#15803d',18);
  },
  record:function(S){
    var c=this.calc(S);
    var more=(c.fa>c.fb)?'1반':((c.fb>c.fa)?'2반':'같음');
    var high=(c.ra>c.rb)?'1반':((c.rb>c.ra)?'2반':'같음');
    return {fa:c.fa,na:S.na,fb:c.fb,nb:S.nb,ra:r3(c.ra),rb:r3(c.rb),
            more:more,high:high,agree:(more===high),sameN:(S.na===S.nb)};
  },
  headA:['번호','1반','2반','1반 상대도수','2반 상대도수','도수 많은 쪽','상대도수 큰 쪽','같은 답?'],
  rowA:function(r,i){
    return [i+1,r.fa+'/'+r.na,r.fb+'/'+r.nb,r.ra,r.rb,r.more,'<b>'+r.high+'</b>',
            '<span class="'+(r.agree?'ok':'no')+'">'+(r.agree?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],agree=0,counter=0,sameN=0,sameNagree=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.agree) agree++; else counter++;
      if(r.sameN){ sameN++; if(r.agree) sameNagree++; }
      rows.push([r.fa+'/'+r.na+' vs '+r.fb+'/'+r.nb, r.ra+' / '+r.rb, r.more, '<b>'+r.high+'</b>',
                 r.sameN?'같음':'다름',
                 '<span class="'+(r.agree?'ok':'no')+'">'+(r.agree?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'두 판단이 같았던 횟수',big:agree+' / '+rec.length,p:'도수로 고른 답과 상대도수로 고른 답이 같았던 경우.'},
      {t:'뒤집힌 경우',big:counter+'개',
       p:counter?'도수는 적은데 상대도수는 큰 경우다.':'전체 인원을 크게 다르게 해서 비교해 보자.'},
      {t:'전체 인원이 같았던 기록',big:sameN+'개',
       p:sameN?('그중 두 판단이 같았던 것 '+sameNagree+'개. 전체가 같으면 도수만 봐도 된다.'):'전체 인원이 같은 경우도 기록해 보자.'}
    ];
    var concl;
    if(counter===0){
      concl='<b>더 해 보자</b> — 아직 판단이 뒤집힌 기록이 없다. 9/20과 12/30처럼 <b>전체 인원을 다르게</b> 해서 비교해 보자.';
    } else {
      concl='<b>정리</b> — 도수가 더 큰데 상대도수는 더 작은 경우가 '+counter+'번 나왔다. '
           +'전체 인원이 다르면 도수만으로는 비교할 수 없다. <b>상대도수 = (그 계급의 도수) ÷ (전체 도수)</b>로 '
           +'기준을 1로 맞춰야 두 집단을 견줄 수 있다. 전체 인원이 같다면 도수만 비교해도 된다.';
    }
    return {head:['비교','상대도수','도수 큰 쪽','상대도수 큰 쪽','전체 인원','같은 답?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 상대도수의 합과 도수 복원
# ============================================================
LAB_RELSUM = BASE + r"""
var NAMES=['1계급','2계급','3계급','4계급'];
var COLS=['#ef4444','#f59e0b','#22c55e','#3b82f6'];
var LAB = {
  cw:440, ch:420, cvTitle:'상대도수 분포판',
  action:'상대도수 구하기',
  hint0:'네 계급의 도수를 정하고, 상대도수와 그 합을 확인해 보자.',
  sliders:[
    {id:'a',label:'1계급 도수',min:1,max:20,value:3,color:'#ef4444',unit:'명'},
    {id:'b',label:'2계급 도수',min:1,max:20,value:7,color:'#f59e0b',unit:'명'},
    {id:'c',label:'3계급 도수',min:1,max:20,value:11,color:'#22c55e',unit:'명'},
    {id:'d',label:'4계급 도수',min:1,max:20,value:6,color:'#3b82f6',unit:'명'}
  ],
  calc:function(S){
    var v=[S.a,S.b,S.c,S.d], tot=v[0]+v[1]+v[2]+v[3], r=[],rr=[],back=[],i;
    for(i=0;i<4;i++){
      r.push(v[i]/tot);
      rr.push(Math.round(v[i]/tot*100)/100);
      back.push(Math.round(Math.round(v[i]/tot*100)/100*tot));
    }
    var exact=r[0]+r[1]+r[2]+r[3];
    var rsum=Math.round((rr[0]+rr[1]+rr[2]+rr[3])*100)/100;
    return {v:v,tot:tot,r:r,rr:rr,back:back,exact:exact,rsum:rsum};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'전체 도수',v:c.tot+'명'},
            {k:'반올림한 상대도수의 합',v:ran?c.rsum:'구해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '반올림하지 않은 상대도수의 합은 '+c.exact.toFixed(2)+', 소수 둘째 자리로 반올림한 합은 '+c.rsum+'이다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var grow=(t===null)?0:Math.min(1,t);
    var X0=40, Y0=76, RH=30, cw2=[70,70,110,110];
    var head=['계급','도수','상대도수','상대도수×전체'];
    var x=X0;
    for(i=0;i<4;i++){
      ctx.fillStyle='#eaf1fa';ctx.fillRect(x,Y0,cw2[i],RH);
      ctx.strokeStyle='#94a3b8';ctx.lineWidth=1.4;ctx.strokeRect(x,Y0,cw2[i],RH);
      ctx.fillStyle='#334155';ctx.font='bold 13px sans-serif';ctx.textAlign='center';
      ctx.fillText(head[i],x+cw2[i]/2,Y0+20);
      x+=cw2[i];
    }
    var shown=Math.ceil(grow*4);
    for(i=0;i<4;i++){
      var y=Y0+RH+i*RH, on=(i<shown);
      var vals=[NAMES[i], ''+c.v[i], on?c.rr[i].toFixed(2):'?', on?(''+c.back[i]):'?'];
      x=X0;
      var j;
      for(j=0;j<4;j++){
        ctx.fillStyle='#fff';ctx.fillRect(x,y,cw2[j],RH);
        ctx.strokeStyle='#cbd5e1';ctx.lineWidth=1.2;ctx.strokeRect(x,y,cw2[j],RH);
        ctx.fillStyle=(j>=2&&!on)?'#cbd5e1':((j===0)?COLS[i]:'#1f2937');
        ctx.font='13px sans-serif';ctx.textAlign='center';
        ctx.fillText(vals[j],x+cw2[j]/2,y+20);
        x+=cw2[j];
      }
    }
    var yS=Y0+RH*5;
    x=X0;
    var sv=['합계',''+c.tot,(grow>=1)?c.rsum.toFixed(2):'?',(grow>=1)?(''+(c.back[0]+c.back[1]+c.back[2]+c.back[3])):'?'];
    for(i=0;i<4;i++){
      ctx.fillStyle='#f1f6fd';ctx.fillRect(x,yS,cw2[i],RH);
      ctx.strokeStyle='#94a3b8';ctx.lineWidth=1.6;ctx.strokeRect(x,yS,cw2[i],RH);
      ctx.fillStyle='#1f2937';ctx.font='bold 13px sans-serif';ctx.textAlign='center';
      ctx.fillText(sv[i],x+cw2[i]/2,yS+20);
      x+=cw2[i];
    }
    ctx.textAlign='left';
    lbl(ctx,'전체 '+c.tot+'명의 도수분포표',24,40,'#1d4ed8',19);
    box(ctx,20,286,400,120);
    lbl(ctx,(t===null)?'상대도수를 모두 더하면 얼마일까?':('반올림 전 합 : '+c.exact.toFixed(4)),38,318,'#15803d',19);
    lbl(ctx,(t===null)?'':('소수 둘째 자리로 반올림한 합 : '+c.rsum),38,350,(c.rsum===1)?'#1f2937':'#b91c1c',19);
    lbl(ctx,(t===null)?'':('상대도수 × 전체로 되돌린 도수의 합 : '+(c.back[0]+c.back[1]+c.back[2]+c.back[3])+'  (실제 '+c.tot+')'),
        38,382,'#52627a',16);
  },
  record:function(S){
    var c=this.calc(S);
    var bs=c.back[0]+c.back[1]+c.back[2]+c.back[3];
    return {v:c.v.join(', '),tot:c.tot,rr:c.rr.map(function(z){return z.toFixed(2);}).join(' / '),
            exact:Math.round(c.exact*10000)/10000,rsum:c.rsum,
            back:c.back.join(', '),bsum:bs,
            one:(c.rsum===1),bok:(bs===c.tot)};
  },
  headA:['번호','도수','전체','반올림 상대도수','반올림 전 합','반올림 후 합','되돌린 도수','합 일치?'],
  rowA:function(r,i){
    return [i+1,r.v,r.tot,r.rr,r.exact,'<b>'+r.rsum+'</b>',r.back,
            '<span class="'+(r.bok?'ok':'no')+'">'+(r.bok?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],exact1=0,round1=0,bok=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var e=(Math.abs(r.exact-1)<1e-9);
      if(e) exact1++;
      if(r.one) round1++;
      if(r.bok) bok++;
      rows.push([r.v+' (전체 '+r.tot+')', r.exact, '<b>'+r.rsum+'</b>',
                 '<span class="'+(e?'ok':'no')+'">'+(e?'○':'×')+'</span>',
                 '<span class="'+(r.one?'ok':'no')+'">'+(r.one?'○':'×')+'</span>',
                 r.bsum+' / '+r.tot,
                 '<span class="'+(r.bok?'ok':'no')+'">'+(r.bok?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'반올림 전 상대도수의 합 = 1',big:exact1+' / '+rec.length,
       p:'상대도수는 도수를 전체로 나눈 값이라 합이 반드시 1이다.'},
      {t:'반올림한 뒤에도 합이 1',big:round1+' / '+rec.length,
       p:round1<rec.length?'반올림하면 합이 1이 아닐 수 있다.':'아직 어긋난 경우가 없다.'},
      {t:'상대도수 × 전체로 도수를 되돌린 결과',big:bok+' / '+rec.length,
       p:'반올림한 상대도수로 되돌리면 원래 도수와 다를 수 있다.'}
    ];
    var concl;
    if(exact1===rec.length && round1<rec.length){
      concl='<b>정리</b> — 상대도수는 (도수) ÷ (전체 도수)이므로 <b>반올림하기 전에는 합이 언제나 정확히 1</b>이었다. '
           +'그런데 소수 둘째 자리로 반올림하면 합이 1이 아닌 경우가 '+(rec.length-round1)+'번 나왔다. '
           +'표에 적힌 상대도수는 <b>반올림한 값</b>이라는 점을 알고 읽어야 한다. '
           +'도수를 되돌릴 때도 (상대도수) × (전체 도수)가 원래 도수와 조금 어긋날 수 있다.';
    } else if(exact1===rec.length){
      concl='<b>정리</b> — 상대도수의 합은 반올림 전에는 언제나 1이었다. 도수를 바꿔 가며 반올림 후 합이 어긋나는 경우를 찾아보자.';
    } else {
      concl='<b>확인 필요</b> — 반올림 전 합이 1이 아닌 기록이 있다.';
    }
    return {head:['자료','반올림 전 합','반올림 후 합','1인가?','반올림 후 1?','되돌린 합','일치?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("m1_histogram_class_width_lab.html",
     "히스토그램 실험실 — 계급을 어떻게 묶느냐에 따라 달라질까?",
     "히스토그램 실험실 — 계급을 어떻게 묶느냐에 따라 달라질까?",
     "같은 자료 30개를 계급의 크기만 바꿔 묶고, 히스토그램 모양과 도수의 합을 기록한다.",
     LAB_HIST),
    ("m1_grouped_mean_lab.html",
     "계급값 평균 실험실 — 도수분포표의 평균은 정확할까?",
     "계급값 평균 실험실 — 도수분포표의 평균은 정확할까?",
     "계급값으로 어림한 평균과 원자료의 실제 평균을 비교하며 계급의 크기에 따른 차이를 기록한다.",
     LAB_TMEAN),
    ("m1_relative_frequency_lab.html",
     "상대도수 실험실 — 도수가 많으면 더 많은 걸까?",
     "상대도수 실험실 — 도수가 많으면 더 많은 걸까?",
     "전체 인원이 다른 두 반의 도수와 상대도수를 비교해, 판단이 뒤집히는 경우를 찾는다.",
     LAB_REL),
    ("m1_relative_frequency_sum_lab.html",
     "상대도수 합 실험실 — 모두 더하면 정확히 1일까?",
     "상대도수 합 실험실 — 모두 더하면 정확히 1일까?",
     "네 계급의 도수로 상대도수를 구해 합을 확인하고, 반올림했을 때 무엇이 달라지는지 기록한다.",
     LAB_RELSUM),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c12_" + fname + ".js", "w", encoding="utf-8").write(js)

print("DATA=", DATA)
print("\n".join(made))
