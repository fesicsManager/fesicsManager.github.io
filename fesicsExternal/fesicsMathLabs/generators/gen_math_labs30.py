# -*- coding: utf-8 -*-
"""고등 확률과 통계 — 이항분포·정규분포·표준화·표본평균·신뢰구간"""
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
function phi(z){ return Math.exp(-z*z/2)/Math.sqrt(2*Math.PI); }
function Phi(z){
  if(z<-8) return 0;
  if(z>8) return 1;
  var n=2000, a=-8, h=(z-a)/n, s=phi(a)+phi(z), i;
  for(i=1;i<n;i++){ s+=(i%2?4:2)*phi(a+i*h); }
  return s*h/3;
}
function randn(){
  var u=0,v=0;
  while(u===0) u=Math.random();
  while(v===0) v=Math.random();
  return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);
}
"""

# ============================================================
# 1. 이항분포
# ============================================================
LAB_BINOM = BASE + r"""
function nCrBig(n,r){
  var v=1,i;
  for(i=0;i<r;i++){ v=v*(n-i)/(i+1); }
  return v;
}
var LAB = {
  cw:440, ch:430, cvTitle:'이항분포 판',
  action:'분포 만들고 평균 구하기',
  hint0:'시행 횟수와 한 번의 성공 확률을 정해 보자.',
  sliders:[
    {id:'n',label:'시행 횟수 n',min:1,max:30,value:10,color:'#2563eb',unit:'회'},
    {id:'p',label:'성공 확률 (÷10)',min:1,max:9,value:3,color:'#dc2626',
     fmt:function(v){return (v/10).toFixed(1);}}
  ],
  calc:function(S){
    var p=S.p/10, pk=[], E=0, E2=0, i;
    for(i=0;i<=S.n;i++){
      var v=nCrBig(S.n,i)*Math.pow(p,i)*Math.pow(1-p,S.n-i);
      pk.push(v); E+=i*v; E2+=i*i*v;
    }
    var sum=0;
    for(i=0;i<=S.n;i++) sum+=pk[i];
    var mode=0;
    for(i=1;i<=S.n;i++){ if(pk[i]>pk[mode]) mode=i; }
    return {p:p,pk:pk,E:E,V:E2-E*E,sum:sum,mode:mode,
            np:S.n*p,npq:S.n*p*(1-p)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'직접 구한 평균',v:ran?r3(c.E):'만들어 보자'},
            {k:'np',v:r3(c.np)}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '평균 '+r3(c.E)+' (np = '+r3(c.np)+'), 분산 '+r3(c.V)+' (np(1−p) = '+r3(c.npq)+'). 확률의 합은 '+r4(c.sum)+'이다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var GX=40, GY=290, GW=370, GH=210;
    var bw=GW/(S.n+1);
    var mp=0;
    for(i=0;i<=S.n;i++){ if(c.pk[i]>mp) mp=c.pk[i]; }
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*(S.n+1));
    for(i=0;i<=S.n;i++){
      var on=(i<shown);
      var h=c.pk[i]/mp*GH;
      var x=GX+i*bw;
      ctx.fillStyle=on?((i===c.mode)?'#f59e0b':'#93c5fd'):'#eef2f7';
      ctx.fillRect(x,GY-h,Math.max(2,bw-2),h);
      ctx.strokeStyle=on?'#2563eb':'#e8edf3';ctx.lineWidth=1;
      ctx.strokeRect(x,GY-h,Math.max(2,bw-2),h);
      if(S.n<=15&&on){
        ctx.fillStyle='#64748b';ctx.font='10px sans-serif';ctx.textAlign='center';
        ctx.fillText(i,x+bw/2,GY+14);
      }
    }
    ctx.textAlign='left';
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+GW,GY);ctx.stroke();
    if(shown>S.n){
      var ex=GX+c.E*bw+bw/2;
      ctx.strokeStyle='#7c3aed';ctx.lineWidth=3;
      ctx.beginPath();ctx.moveTo(ex,GY-GH-10);ctx.lineTo(ex,GY+8);ctx.stroke();
      lbl(ctx,'평균 '+r2(c.E),ex+6,GY-GH-14,'#6d28d9',14);
    }
    lbl(ctx,'B('+S.n+', '+c.p+')',24,32,'#1d4ed8',18);
    box(ctx,20,318,400,100);
    lbl(ctx,(t===null)?'평균과 분산은?':('평균 '+r3(c.E)+'      np = '+r3(c.np)),38,350,'#1f2937',18);
    lbl(ctx,(t===null)?'':('분산 '+r3(c.V)+'      np(1−p) = '+r3(c.npq)),38,382,'#15803d',18);
    lbl(ctx,(t===null)?'':('확률의 합 = '+r4(c.sum)+'      가장 높은 막대 : '+c.mode),38,410,'#52627a',15);
  },
  record:function(S){
    var c=this.calc(S);
    return {n:S.n,p:c.p,E:r3(c.E),np:r3(c.np),V:r3(c.V),npq:r3(c.npq),
            sum:r4(c.sum),mode:c.mode,
            eOk:(Math.abs(c.E-c.np)<1e-6),
            vOk:(Math.abs(c.V-c.npq)<1e-6),
            sumOk:(Math.abs(c.sum-1)<1e-6),
            modeEq:(Math.abs(c.mode-c.E)<1e-9)};
  },
  headA:['번호','n, p','평균','np','같나?','분산','np(1−p)','같나?','확률의 합','최빈값'],
  rowA:function(r,i){
    return [i+1,r.n+', '+r.p,'<b>'+r.E+'</b>',r.np,
            '<span class="'+(r.eOk?'ok':'no')+'">'+(r.eOk?'○':'×')+'</span>',
            r.V,r.npq,
            '<span class="'+(r.vOk?'ok':'no')+'">'+(r.vOk?'○':'×')+'</span>',
            r.sum,r.mode];
  },
  analyze:function(rec){
    var rows=[],e=0,v=0,s=0,me=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.eOk) e++;
      if(r.vOk) v++;
      if(r.sumOk) s++;
      if(r.modeEq) me++;
      rows.push([r.n+', '+r.p, '<b>'+r.E+'</b>', r.np,
                 '<span class="'+(r.eOk?'ok':'no')+'">'+(r.eOk?'○':'×')+'</span>',
                 r.V, r.npq,
                 '<span class="'+(r.vOk?'ok':'no')+'">'+(r.vOk?'○':'×')+'</span>',
                 r.mode]);
    }
    var stats=[
      {t:'평균 = np',big:e+' / '+rec.length,p:'모든 k에 대해 k·P(k)를 더한 값과 비교했다.'},
      {t:'분산 = np(1−p)',big:v+' / '+rec.length,p:'직접 계산한 분산과 공식을 비교했다.'},
      {t:'확률의 합 = 1',big:s+' / '+rec.length,
       p:'평균이 최빈값과 같았던 횟수 '+me+'.'}
    ];
    var concl;
    if(e===rec.length&&v===rec.length){
      concl='<b>정리</b> — 모든 경우의 확률을 직접 더해 구한 평균과 분산이 <b>np, np(1−p)</b> 와 정확히 일치했다. '
           +'한 번의 시행에서 평균 p, 분산 p(1−p) 인 것이 n번 더해진 결과다. '
           +'분포는 p = 0.5 에서 좌우 대칭이고 p가 0이나 1에 가까울수록 한쪽으로 치우쳤다. '
           +'평균이 정수가 아닐 때는 <b>가장 높은 막대와 평균이 서로 다른 자리</b>에 있다.';
    } else {
      concl='<b>확인 필요</b> — 직접 계산한 값과 공식이 어긋난 기록이 있다.';
    }
    return {head:['n, p','평균','np','같나?','분산','np(1−p)','같나?','최빈값'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 정규분포의 68-95-99.7
# ============================================================
LAB_NORM = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'정규분포 판',
  action:'구간 확률 구하기',
  hint0:'평균과 표준편차를 정하고, 평균에서 몇 배 떨어진 구간의 확률을 구해 보자.',
  sliders:[
    {id:'mu',label:'평균 μ',min:0,max:100,value:50,color:'#2563eb',unit:''},
    {id:'sd',label:'표준편차 σ',min:2,max:20,value:10,color:'#16a34a',unit:''},
    {id:'k',label:'몇 배 구간 (÷2)',min:2,max:6,value:2,color:'#f59e0b',
     fmt:function(v){return (v/2).toFixed(1)+'σ';}}
  ],
  calc:function(S){
    var k=S.k/2;
    return {k:k,p:Phi(k)-Phi(-k),
            p1:Phi(1)-Phi(-1),p2:Phi(2)-Phi(-2),p3:Phi(3)-Phi(-3)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'구간',v:'μ ± '+c.k+'σ = '+r1(S.mu-c.k*S.sd)+' ~ '+r1(S.mu+c.k*S.sd)},
            {k:'그 안에 있을 확률',v:ran?r4(c.p):'구해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'μ ± '+c.k+'σ 안에 있을 확률은 '+r4(c.p)+'다. μ와 σ를 바꿔도 같은지 확인해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var GX=40, GY=290, GW=370, GH=200;
    function px(z){ return GX+GW*(z+4)/8; }
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      var lo=-c.k, hi=c.k;
      ctx.fillStyle='rgba(37,99,235,0.22)';
      for(i=0;i<200;i++){
        var z=lo+(hi-lo)*i/200;
        if(i/200>grow) break;
        var h=phi(z)/phi(0)*GH;
        ctx.fillRect(px(z),GY-h,Math.max(1,px(z+(hi-lo)/200)-px(z)+1),h);
      }
    }
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    for(i=0;i<=200;i++){
      var z2=-4+8*i/200;
      var h2=phi(z2)/phi(0)*GH;
      if(i===0) ctx.moveTo(px(z2),GY-h2); else ctx.lineTo(px(z2),GY-h2);
    }
    ctx.stroke();
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+GW,GY);ctx.stroke();
    ctx.font='12px sans-serif';ctx.textAlign='center';
    for(i=-3;i<=3;i++){
      ctx.strokeStyle='#cbd5e1';ctx.lineWidth=1;
      ctx.beginPath();ctx.moveTo(px(i),GY-4);ctx.lineTo(px(i),GY+4);ctx.stroke();
      ctx.fillStyle='#64748b';
      ctx.fillText((i===0)?'μ':('μ'+((i>0)?'+':'−')+Math.abs(i)+'σ'),px(i),GY+18);
    }
    ctx.textAlign='left';
    lbl(ctx,'N('+S.mu+', '+S.sd+'²)',24,32,'#1d4ed8',18);
    box(ctx,20,318,400,100);
    lbl(ctx,(t===null)?'몇 %가 이 구간에 있을까?':('μ ± '+c.k+'σ  →  '+r4(c.p)),38,350,'#1f2937',19);
    lbl(ctx,(t===null)?'':('1σ '+r4(c.p1)+'   2σ '+r4(c.p2)+'   3σ '+r4(c.p3)),38,384,'#15803d',17);
    lbl(ctx,'구간의 실제 범위 : '+r1(S.mu-c.k*S.sd)+' ~ '+r1(S.mu+c.k*S.sd),38,410,'#52627a',15);
  },
  record:function(S){
    var c=this.calc(S);
    return {mu:S.mu,sd:S.sd,k:c.k,p:r4(c.p),
            lo:r1(S.mu-c.k*S.sd),hi:r1(S.mu+c.k*S.sd),
            is68:(Math.abs(c.k-1)<1e-9&&Math.abs(c.p-0.6827)<0.002),
            is95:(Math.abs(c.k-2)<1e-9&&Math.abs(c.p-0.9545)<0.002),
            is997:(Math.abs(c.k-3)<1e-9&&Math.abs(c.p-0.9973)<0.002)};
  },
  headA:['번호','μ, σ','배수 k','구간','확률'],
  rowA:function(r,i){
    return [i+1,r.mu+', '+r.sd,r.k+'σ',r.lo+' ~ '+r.hi,'<b>'+r.p+'</b>'];
  },
  analyze:function(rec){
    var rows=[],g={},kn=0,pairs=0,agree=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var note='첫 기록';
      if(g[r.k]!==undefined){
        pairs++;
        var same=(Math.abs(g[r.k]-r.p)<0.002);
        if(same) agree++;
        note='<span class="'+(same?'ok':'no')+'">'+(same?'확률 같음':'확률 다름')+'</span>';
      } else { g[r.k]=r.p; kn++; }
      rows.push([r.mu+', '+r.sd, r.k+'σ', r.lo+' ~ '+r.hi, '<b>'+r.p+'</b>', note]);
    }
    var lines=[],k;
    for(k in g){ lines.push(k+'σ → '+g[k]); }
    var stats=[
      {t:'시험한 배수',big:kn+'가지',p:lines.join(' / ')},
      {t:'같은 배수로 μ·σ만 바꾼 짝',big:pairs+'쌍',
       p:pairs?('그중 확률이 같았던 것 '+agree+'쌍.'):'μ와 σ를 바꿔 같은 배수로 다시 기록해 보자.'},
      {t:'구간의 실제 범위',big:'매번 다름',p:'범위는 달라져도 확률은 배수에만 달려 있다.'}
    ];
    var concl;
    if(pairs===0){
      concl='<b>더 해 보자</b> — 같은 배수(예: 2σ)로 μ와 σ를 바꿔 두 번 이상 기록해야 “확률이 배수에만 달렸는지”를 확인할 수 있다.';
    } else if(agree===pairs){
      concl='<b>정리</b> — μ와 σ가 달라져 구간의 <b>실제 범위는 매번 바뀌었지만 확률은 똑같았다.</b> '
           +'정규분포는 모양이 하나뿐이고 위치와 폭만 다르기 때문이다. '
           +'그래서 <b>1σ 안에 약 68%, 2σ 안에 약 95%, 3σ 안에 약 99.7%</b> 라는 값이 어떤 정규분포에서든 통한다. '
           +'이것이 표준화를 할 수 있는 이유다.';
    } else {
      concl='<b>확인 필요</b> — 같은 배수인데 확률이 다른 기록이 있다.';
    }
    return {head:['μ, σ','배수','구간','확률','같은 배수끼리'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 표준화
# ============================================================
LAB_Z = BASE + r"""
var M1=70, S1=10, M2=60, S2=5;
var LAB = {
  cw:440, ch:430, cvTitle:'표준점수 판',
  action:'표준점수로 바꾸기',
  hint0:'두 시험의 원점수를 정해 보자. 시험1은 평균 70·표준편차 10, 시험2는 평균 60·표준편차 5다.',
  sliders:[
    {id:'x1',label:'시험1 점수',min:40,max:100,value:80,color:'#2563eb',unit:'점'},
    {id:'x2',label:'시험2 점수',min:40,max:80,value:72,color:'#dc2626',unit:'점'}
  ],
  calc:function(S){
    var z1=(S.x1-M1)/S1, z2=(S.x2-M2)/S2;
    return {z1:z1,z2:z2,
            p1:Phi(z1),p2:Phi(z2),
            rawHigh:(S.x1>S.x2)?'시험1':((S.x2>S.x1)?'시험2':'같음'),
            zHigh:(z1>z2)?'시험1':((z2>z1)?'시험2':'같음')};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'표준점수 z',v:ran?(r2(c.z1)+' / '+r2(c.z2)):'바꿔 보자'},
            {k:'상위 비율',v:ran?(r3(1-c.p1)+' / '+r3(1-c.p2)):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'z 점수는 '+r2(c.z1)+'와 '+r2(c.z2)+'다. 원점수가 높은 쪽은 '+c.rawHigh+', z가 높은 쪽은 '+c.zHigh+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var grow=(t===null)?0:Math.min(1,t);
    function curve(GY,mu,sd,x,col,name){
      var GX=40, GW=370, GH=100;
      function px(z){ return GX+GW*(z+3.5)/7; }
      ctx.strokeStyle=col;ctx.lineWidth=2.6;ctx.beginPath();
      for(i=0;i<=160;i++){
        var z=-3.5+7*i/160;
        var h=phi(z)/phi(0)*GH;
        if(i===0) ctx.moveTo(px(z),GY-h); else ctx.lineTo(px(z),GY-h);
      }
      ctx.stroke();
      ctx.strokeStyle='#334155';ctx.lineWidth=1.6;
      ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+GW,GY);ctx.stroke();
      var zz=(x-mu)/sd;
      if(grow>0&&Math.abs(zz)<=3.5){
        ctx.strokeStyle='#f59e0b';ctx.lineWidth=3;
        ctx.beginPath();ctx.moveTo(px(zz),GY-GH-6);ctx.lineTo(px(zz),GY+6);ctx.stroke();
        if(grow>=1) lbl(ctx,'z = '+r2(zz),px(zz)+6,GY-GH-10,'#b45309',13);
      }
      lbl(ctx,name+'  평균 '+mu+', 표준편차 '+sd,GX,GY-GH-22,col,14);
      ctx.font='11px sans-serif';ctx.textAlign='center';
      for(i=-3;i<=3;i++){
        ctx.fillStyle='#94a3b8';
        ctx.fillText(mu+i*sd,px(i),GY+16);
      }
      ctx.textAlign='left';
    }
    curve(160,M1,S1,S.x1,'#2563eb','시험1');
    curve(320,M2,S2,S.x2,'#dc2626','시험2');
    box(ctx,20,344,400,74);
    lbl(ctx,(t===null)?'어느 쪽이 더 잘한 걸까?':('원점수 높은 쪽 : '+c.rawHigh+'      z 높은 쪽 : '+c.zHigh),38,374,'#1f2937',18);
    lbl(ctx,(t===null)?'':('z = '+r2(c.z1)+' / '+r2(c.z2)+'      상위 '+r1((1-c.p1)*100)+'% / '+r1((1-c.p2)*100)+'%'),
        38,404,'#52627a',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {x1:S.x1,x2:S.x2,z1:r2(c.z1),z2:r2(c.z2),
            top1:r1((1-c.p1)*100),top2:r1((1-c.p2)*100),
            rawHigh:c.rawHigh,zHigh:c.zHigh,
            agree:(c.rawHigh===c.zHigh)};
  },
  headA:['번호','시험1 / 시험2','z1','z2','상위 %','원점수 높은 쪽','z 높은 쪽','같은 답?'],
  rowA:function(r,i){
    return [i+1,r.x1+' / '+r.x2,r.z1,r.z2,r.top1+'% / '+r.top2+'%',r.rawHigh,'<b>'+r.zHigh+'</b>',
            '<span class="'+(r.agree?'ok':'no')+'">'+(r.agree?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],agree=0,flip=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.agree) agree++; else flip++;
      rows.push([r.x1+' / '+r.x2, r.z1+' / '+r.z2, r.top1+'% / '+r.top2+'%', r.rawHigh, '<b>'+r.zHigh+'</b>',
                 '<span class="'+(r.agree?'ok':'no')+'">'+(r.agree?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'두 판단이 같았던 횟수',big:agree+' / '+rec.length,p:'원점수로 고른 답과 z로 고른 답이 같았던 경우.'},
      {t:'뒤집힌 경우',big:flip+'개',
       p:flip?'원점수는 낮은데 상대적 위치는 더 높았던 경우다.':'시험1에서 80점, 시험2에서 72점처럼 비교해 보자.'},
      {t:'기준',big:'평균과 표준편차',p:'시험마다 평균과 흩어진 정도가 달라 원점수를 바로 비교할 수 없다.'}
    ];
    var concl;
    if(flip===0){
      concl='<b>더 해 보자</b> — 아직 판단이 뒤집힌 기록이 없다. 시험1에서 80점, 시험2에서 72점처럼 잡아 보자.';
    } else {
      concl='<b>정리</b> — 원점수가 더 높은데 <b>상대적 위치는 더 낮은 경우가 '+flip+'번</b> 나왔다. '
           +'시험마다 평균과 표준편차가 다르기 때문이다. '
           +'z = (x − μ)/σ 로 바꾸면 “평균에서 표준편차 몇 개만큼 떨어졌는가”가 되어 <b>서로 다른 시험도 같은 자로 비교</b>할 수 있다.';
    }
    return {head:['원점수','z','상위 %','원점수 높은 쪽','z 높은 쪽','같은 답?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 표본평균의 분포
# ============================================================
LAB_SAMP = BASE + r"""
var MU=50, SD=10, REP=200;
var LAB = {
  cw:440, ch:430, cvTitle:'표본평균 판',
  action:'표본 200개 뽑기',
  hint0:'모집단은 평균 50, 표준편차 10 인 정규분포다. 표본의 크기를 정해 보자.',
  _trial:null,
  sliders:[
    {id:'n',label:'표본의 크기 n',min:1,max:50,value:4,color:'#2563eb',unit:'개'}
  ],
  gen:function(S){
    var means=[],i,j;
    for(i=0;i<REP;i++){
      var s=0;
      for(j=0;j<S.n;j++){ s+=MU+SD*randn(); }
      means.push(s/S.n);
    }
    var m=0;
    for(i=0;i<REP;i++) m+=means[i];
    m/=REP;
    var v=0;
    for(i=0;i<REP;i++) v+=(means[i]-m)*(means[i]-m);
    v/=REP;
    this._trial={means:means,mean:m,sd:Math.sqrt(v)};
  },
  readout:function(S,ran){
    var tr=this._trial;
    return [{k:'이론값 σ/√n',v:r3(SD/Math.sqrt(S.n))},
            {k:'표본평균의 표준편차',v:(ran&&tr)?r3(tr.sd):'뽑아 보자'}];
  },
  doneMsg:function(S){
    var tr=this._trial;
    return '표본평균 200개의 평균은 '+r2(tr.mean)+', 표준편차는 '+r3(tr.sd)+'다. σ/√n = '+r3(SD/Math.sqrt(S.n))+'와 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    if(t===null){ this._trial=null; }
    else if(!this._trial){ this.gen(S); }
    var tr=this._trial, i;
    var GX=40, GY=300, GW=370, GH=210;
    var lo=MU-25, hi=MU+25;
    function px(v){ return GX+GW*(v-lo)/(hi-lo); }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+GW,GY);ctx.stroke();
    ctx.font='11px sans-serif';ctx.textAlign='center';
    for(i=lo;i<=hi;i+=10){
      ctx.fillStyle='#94a3b8';ctx.fillText(i,px(i),GY+16);
    }
    ctx.textAlign='left';
    if(tr){
      var bins=50, cnt=[],j;
      for(i=0;i<bins;i++) cnt.push(0);
      var shown=Math.ceil(Math.min(1,t)*REP);
      for(i=0;i<shown;i++){
        var b=Math.floor((tr.means[i]-lo)/(hi-lo)*bins);
        if(b>=0&&b<bins) cnt[b]++;
      }
      var mx=1;
      for(i=0;i<bins;i++){ if(cnt[i]>mx) mx=cnt[i]; }
      for(i=0;i<bins;i++){
        var h=cnt[i]/mx*GH;
        ctx.fillStyle='#93c5fd';
        ctx.fillRect(GX+GW*i/bins,GY-h,GW/bins-1,h);
      }
      ctx.strokeStyle='#7c3aed';ctx.lineWidth=2.4;
      ctx.beginPath();ctx.moveTo(px(MU),GY-GH-8);ctx.lineTo(px(MU),GY+8);ctx.stroke();
      lbl(ctx,'μ = 50',px(MU)+6,GY-GH-12,'#6d28d9',13);
      if(Math.min(1,t)>=1){
        ctx.strokeStyle='#dc2626';ctx.lineWidth=2.4;
        ctx.beginPath();ctx.moveTo(px(MU-tr.sd),GY+22);ctx.lineTo(px(MU+tr.sd),GY+22);ctx.stroke();
        lbl(ctx,'± '+r2(tr.sd),px(MU+tr.sd)+6,GY+27,'#b91c1c',13);
      }
    } else {
      lbl(ctx,'표본을 뽑으면 표본평균이 여기 쌓인다',GX,GY-100,'#94a3b8',15);
    }
    lbl(ctx,'표본 크기 n = '+S.n,24,32,'#1d4ed8',18);
    lbl(ctx,'모집단 : 평균 50, 표준편차 10',24,56,'#52627a',14);
    box(ctx,20,336,400,80);
    lbl(ctx,(t===null)?'표본평균은 얼마나 흩어질까?':('표본평균의 평균 '+r2(tr.mean)+'      표준편차 '+r3(tr.sd)),38,366,'#1f2937',17);
    lbl(ctx,'σ/√n = '+r3(SD/Math.sqrt(S.n))+'      (모표준편차 10)',38,398,'#15803d',17);
  },
  record:function(S){
    var tr=this._trial;
    var theory=SD/Math.sqrt(S.n);
    return {n:S.n,mean:r2(tr.mean),sd:r3(tr.sd),theory:r3(theory),
            gap:r3(Math.abs(tr.sd-theory)),
            close:(Math.abs(tr.sd-theory)<theory*0.15),
            meanOk:(Math.abs(tr.mean-MU)<1.5)};
  },
  headA:['번호','n','표본평균의 평균','표준편차','σ/√n','차이','비슷한가?','평균이 50 근처?'],
  rowA:function(r,i){
    return [i+1,r.n,r.mean,'<b>'+r.sd+'</b>',r.theory,r.gap,
            '<span class="'+(r.close?'ok':'no')+'">'+(r.close?'○':'×')+'</span>',
            '<span class="'+(r.meanOk?'ok':'no')+'">'+(r.meanOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],close=0,mok=0,arr=[],mono=true;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.close) close++;
      if(r.meanOk) mok++;
      arr.push([r.n,parseFloat(r.sd)]);
      rows.push([r.n, r.mean, '<b>'+r.sd+'</b>', r.theory, r.gap,
                 '<span class="'+(r.close?'ok':'no')+'">'+(r.close?'○':'×')+'</span>']);
    }
    arr.sort(function(x,y){return x[0]-y[0];});
    for(i=1;i<arr.length;i++){ if(arr[i][1]>arr[i-1][1]*1.2) mono=false; }
    var stats=[
      {t:'표본평균의 표준편차 ≈ σ/√n',big:close+' / '+rec.length,
       p:'200개 표본평균으로 실제 재어 본 값과 이론값을 비교했다(오차 15% 이내).'},
      {t:'표본평균의 평균이 50 근처',big:mok+' / '+rec.length,
       p:'표본을 아무리 뽑아도 중심은 모평균에서 움직이지 않았다.'},
      {t:'n이 커질수록 흩어짐이 줄어듦',big:(arr.length<2)?'비교 없음':(mono?'그렇다':'들쭉날쭉'),
       p:'n을 1, 4, 16, 36 처럼 바꿔 기록하면 뚜렷하다.'}
    ];
    var concl;
    if(arr.length<3){
      concl='<b>더 해 보자</b> — n을 1, 4, 16, 36 처럼 여러 값으로 기록해야 흩어짐의 변화가 보인다.';
    } else if(close>=rec.length-1&&mono){
      concl='<b>정리</b> — 표본평균들의 중심은 언제나 <b>모평균 50 근처</b>였고, 흩어진 정도는 <b>σ/√n</b> 에 맞아떨어졌다. '
           +'n을 4배로 하면 표준편차는 절반이 된다. n에 비례해 줄어드는 것이 아니라 <b>√n 에 반비례</b>한다. '
           +'표본을 두 배로 늘려도 정확도가 두 배가 되지는 않는다는 뜻이다.';
    } else {
      concl='<b>정리</b> — 표본평균의 흩어짐은 σ/√n 근처였다. 난수라 매번 조금씩 달라지니 기록을 더 모아 보자.';
    }
    return {head:['n','표본평균의 평균','표준편차','σ/√n','차이','비슷한가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 신뢰구간의 뜻
# ============================================================
LAB_CI = BASE + r"""
var MU=50, SD=10, TRIALS=100;
var LEVELS=[[90,1.645],[95,1.96],[99,2.576]];
var LAB = {
  cw:440, ch:430, cvTitle:'신뢰구간 판',
  action:'표본 100개로 구간 만들기',
  hint0:'표본의 크기와 신뢰도를 정해 보자. 모평균은 50이지만 모른다고 하자.',
  _trial:null,
  sliders:[
    {id:'n',label:'표본의 크기 n',min:5,max:50,value:25,color:'#2563eb',unit:'개'},
    {id:'lv',label:'신뢰도',min:0,max:2,value:1,color:'#dc2626',fmt:function(v){return LEVELS[v][0]+'%';}}
  ],
  gen:function(S){
    var z=LEVELS[S.lv][1];
    var half=z*SD/Math.sqrt(S.n);
    var arr=[],hit=0,i,j;
    for(i=0;i<TRIALS;i++){
      var s=0;
      for(j=0;j<S.n;j++) s+=MU+SD*randn();
      var m=s/S.n;
      var lo=m-half, hi=m+half;
      var ok=(lo<=MU&&MU<=hi);
      if(ok) hit++;
      arr.push([m,lo,hi,ok]);
    }
    this._trial={arr:arr,hit:hit,half:half,z:z};
  },
  readout:function(S,ran){
    var tr=this._trial;
    return [{k:'신뢰도',v:LEVELS[S.lv][0]+'%'},
            {k:'모평균을 포함한 구간',v:(ran&&tr)?(tr.hit+' / '+TRIALS):'만들어 보자'}];
  },
  doneMsg:function(S){
    var tr=this._trial;
    return '100개의 신뢰구간 중 '+tr.hit+'개가 모평균 50을 품었다. 신뢰도 '+LEVELS[S.lv][0]+'%와 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    if(t===null){ this._trial=null; }
    else if(!this._trial){ this.gen(S); }
    var tr=this._trial, i;
    var GX=40, GW=370, TOP=70, H=250;
    var lo=MU-14, hi=MU+14;
    function px(v){ return GX+GW*(v-lo)/(hi-lo); }
    ctx.strokeStyle='#7c3aed';ctx.lineWidth=2.6;
    ctx.beginPath();ctx.moveTo(px(MU),TOP-10);ctx.lineTo(px(MU),TOP+H+10);ctx.stroke();
    lbl(ctx,'모평균 50',px(MU)+6,TOP-14,'#6d28d9',13);
    if(tr){
      var shown=Math.ceil(Math.min(1,t)*TRIALS);
      for(i=0;i<shown;i++){
        var y=TOP+H*i/TRIALS;
        var a=tr.arr[i];
        ctx.strokeStyle=a[3]?'#93c5fd':'#ef4444';
        ctx.lineWidth=a[3]?1.6:2.2;
        ctx.beginPath();ctx.moveTo(px(a[1]),y);ctx.lineTo(px(a[2]),y);ctx.stroke();
      }
    } else {
      lbl(ctx,'표본마다 구간이 하나씩 만들어진다',GX,TOP+120,'#94a3b8',15);
    }
    ctx.font='11px sans-serif';ctx.textAlign='center';
    for(i=-12;i<=12;i+=6){
      ctx.fillStyle='#94a3b8';ctx.fillText(MU+i,px(MU+i),TOP+H+26);
    }
    ctx.textAlign='left';
    lbl(ctx,'n = '+S.n+',  신뢰도 '+LEVELS[S.lv][0]+'%',24,32,'#1d4ed8',18);
    lbl(ctx,'파랑 = 모평균을 품은 구간,  빨강 = 놓친 구간',24,52,'#52627a',13);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'몇 개가 모평균을 품을까?':('품은 구간 '+tr.hit+' / '+TRIALS+'  ('+tr.hit+'%)'),38,376,'#1f2937',18);
    lbl(ctx,(t===null)?'':('구간의 폭 : ± '+r2(tr.half)+'      z = '+tr.z),38,406,'#52627a',16);
  },
  record:function(S){
    var tr=this._trial;
    return {n:S.n,level:LEVELS[S.lv][0],hit:tr.hit,half:r2(tr.half),
            gap:Math.abs(tr.hit-LEVELS[S.lv][0]),
            close:(Math.abs(tr.hit-LEVELS[S.lv][0])<=6)};
  },
  headA:['번호','n','신뢰도','구간의 폭 ±','모평균을 품은 개수','신뢰도와 차이','비슷한가?'],
  rowA:function(r,i){
    return [i+1,r.n,r.level+'%',r.half,'<b>'+r.hit+' / 100</b>',r.gap,
            '<span class="'+(r.close?'ok':'no')+'">'+(r.close?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],close=0,lv={},ln=0,arr=[],mono=true,ns={},nn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.close) close++;
      if(!lv[r.level]){ lv[r.level]=true; ln++; }
      if(!ns[r.n]){ ns[r.n]=true; nn++; }
      arr.push([r.n,parseFloat(r.half)]);
      rows.push([r.n, r.level+'%', r.half, '<b>'+r.hit+' / 100</b>', r.gap,
                 '<span class="'+(r.close?'ok':'no')+'">'+(r.close?'○':'×')+'</span>']);
    }
    arr.sort(function(x,y){return x[0]-y[0];});
    for(i=1;i<arr.length;i++){ if(arr[i][1]>arr[i-1][1]*1.02) mono=false; }
    var stats=[
      {t:'품은 개수가 신뢰도와 비슷',big:close+' / '+rec.length,
       p:'차이가 6개 이내였던 기록 수(난수라 매번 흔들린다).'},
      {t:'시험한 신뢰도',big:ln+'가지',p:ln>1?'신뢰도를 높이면 구간이 넓어진다.':'90%, 99%도 해 보자.'},
      {t:'n이 클수록 구간이 좁아짐',big:(nn<2)?'비교 없음':(mono?'그렇다':'들쭉날쭉'),
       p:'시험한 n '+nn+'가지.'}
    ];
    var concl;
    if(ln<2||nn<2){
      concl='<b>더 해 보자</b> — 신뢰도와 표본 크기를 <b>둘 다</b> 바꿔 가며 기록해 보자.';
    } else {
      concl='<b>정리</b> — 100개의 표본에서 만든 신뢰구간 중 <b>신뢰도에 해당하는 개수만큼</b>이 모평균을 품었고, 나머지는 놓쳤다. '
           +'즉 신뢰도 95%는 “모평균이 이 구간에 있을 확률이 95%”가 아니라 '
           +'<b>“같은 방법으로 구간을 계속 만들면 그중 95%가 모평균을 품는다”</b>는 뜻이다. '
           +'모평균은 고정된 값이고 움직이는 것은 구간 쪽이다. 신뢰도를 높이면 구간이 넓어지고, n을 키우면 좁아졌다.';
    }
    return {head:['n','신뢰도','폭 ±','품은 개수','차이','비슷한가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("hp_binomial_lab_ProbStat_Dist_Ep06.html",
     "이항분포 실험실 — 평균과 분산은 어디서 올까?",
     "이항분포 실험실 — 평균과 분산은 어디서 올까?",
     "모든 경우의 확률을 직접 더해 평균과 분산을 구하고 np, np(1−p)와 대조한다.",
     LAB_BINOM),
    ("hp_normal_distribution_lab_ProbStat_Dist_Ep07.html",
     "정규분포 실험실 — 68·95·99.7은 어디서 나올까?",
     "정규분포 실험실 — 68·95·99.7은 어디서 나올까?",
     "평균과 표준편차를 바꿔 가며 μ ± kσ 구간의 확률을 구해, 무엇에 달려 있는지 확인한다.",
     LAB_NORM),
    ("hp_standardization_lab_ProbStat_Dist_Ep08.html",
     "표준점수 실험실 — 원점수가 높으면 더 잘한 걸까?",
     "표준점수 실험실 — 원점수가 높으면 더 잘한 걸까?",
     "평균과 표준편차가 다른 두 시험의 점수를 z 점수로 바꿔 비교한다.",
     LAB_Z),
    ("hp_sample_mean_lab_ProbStat_Estim_Ep02.html",
     "표본평균 실험실 — 표본을 키우면 무엇이 달라질까?",
     "표본평균 실험실 — 표본을 키우면 무엇이 달라질까?",
     "표본 200개를 실제로 뽑아 표본평균의 흩어진 정도를 재고 σ/√n과 비교한다.",
     LAB_SAMP),
    ("hp_confidence_interval_lab_ProbStat_Estim_Ep04.html",
     "신뢰구간 실험실 — 95%는 무엇의 확률일까?",
     "신뢰구간 실험실 — 95%는 무엇의 확률일까?",
     "표본 100개로 신뢰구간을 100개 만들어, 그중 몇 개가 모평균을 품는지 세어 본다.",
     LAB_CI),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c30_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
