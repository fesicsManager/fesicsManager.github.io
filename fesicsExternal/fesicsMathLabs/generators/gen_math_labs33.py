# -*- coding: utf-8 -*-
"""고등 미적분Ⅱ — 수열의 극한 3종 + e 1종 + 미분 1종"""
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
"""

# ============================================================
# 1. 수열의 극한
# ============================================================
LAB_SEQ = BASE + r"""
var KINDS=['1/n','(−1)ⁿ','n/(n+1)','√(n+1) − √n','(−1)ⁿ · n/(n+1)'];
function an(kind,n){
  if(kind===0) return 1/n;
  if(kind===1) return (n%2===0)?1:-1;
  if(kind===2) return n/(n+1);
  if(kind===3) return Math.sqrt(n+1)-Math.sqrt(n);
  return ((n%2===0)?1:-1)*n/(n+1);
}
var LAB = {
  cw:440, ch:430, cvTitle:'수열 관찰판',
  action:'큰 n까지 가 보기',
  hint0:'수열을 고르고, 확인할 항의 번호를 정해 보자.',
  sliders:[
    {id:'kind',label:'수열',min:0,max:4,value:3,color:'#2563eb',fmt:function(v){return KINDS[v];}},
    {id:'n',label:'항의 번호 n',min:1,max:60,value:10,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var a=an(S.kind,S.n);
    var big1=an(S.kind,9999), big2=an(S.kind,10000);
    var conv=(Math.abs(big1-big2)<1e-4);
    return {a:a,big1:big1,big2:big2,conv:conv,
            lim:conv?big2:null};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'a'+S.n,v:r6(c.a)},
            {k:'a₁₀₀₀₀',v:ran?r6(c.big2):'가 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'a'+S.n+' = '+r6(c.a)+', a₁₀₀₀₀ = '+r6(c.big2)+'.  '+(c.conv?('한 값 '+r4(c.lim)+'에 다가간다.'):'한 값으로 다가가지 않는다.')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var GX=44, GY=250, GW=356, GH=170;
    var lo=-1.2, hi=1.2;
    function py(v){ return GY-(v-lo)/(hi-lo)*GH; }
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=-1;i<=1;i++){
      ctx.beginPath();ctx.moveTo(GX,py(i));ctx.lineTo(GX+GW,py(i));ctx.stroke();
      lbl(ctx,''+i,GX-14,py(i)+4,'#94a3b8',12);
    }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(GX,py(0));ctx.lineTo(GX+GW,py(0));ctx.stroke();
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*S.n);
    for(i=1;i<=S.n;i++){
      if(i>shown) break;
      var v=an(S.kind,i);
      if(v<lo||v>hi) continue;
      var x=GX+GW*i/S.n;
      ctx.beginPath();ctx.arc(x,py(v),4,0,Math.PI*2);
      ctx.fillStyle='#2563eb';ctx.fill();
    }
    if(shown>=S.n&&c.conv){
      ctx.strokeStyle='#7c3aed';ctx.lineWidth=2;ctx.setLineDash([5,4]);
      ctx.beginPath();ctx.moveTo(GX,py(c.lim));ctx.lineTo(GX+GW,py(c.lim));ctx.stroke();ctx.setLineDash([]);
      lbl(ctx,'다가가는 값 '+r4(c.lim),GX+GW-8,py(c.lim)-8,'#6d28d9',13,'right');
    }
    lbl(ctx,'aₙ = '+KINDS[S.kind],24,32,'#1d4ed8',18);
    box(ctx,20,286,400,130);
    lbl(ctx,'a₁ = '+r6(an(S.kind,1))+'      a'+S.n+' = '+r6(c.a),38,318,'#52627a',16);
    lbl(ctx,(t===null)?'큰 n에서는 어떻게 될까?':('a₉₉₉₉ = '+r6(c.big1)+'      a₁₀₀₀₀ = '+r6(c.big2)),38,352,'#1f2937',16);
    lbl(ctx,(t===null)?'':(c.conv?('수렴 — 다가가는 값 '+r4(c.lim)):'수렴하지 않음'),38,388,c.conv?'#15803d':'#b91c1c',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {kind:S.kind,name:KINDS[S.kind],n:S.n,a:r6(c.a),
            big:r6(c.big2),conv:c.conv,
            lim:c.conv?r4(c.lim):'없음',
            zero:(c.conv&&Math.abs(c.lim)<1e-4)};
  },
  headA:['번호','수열','n','aₙ','a₁₀₀₀₀','수렴?','다가가는 값'],
  rowA:function(r,i){
    return [i+1,r.name,r.n,r.a,'<b>'+r.big+'</b>',
            '<span class="'+(r.conv?'ok':'no')+'">'+(r.conv?'○':'×')+'</span>',
            r.lim];
  },
  analyze:function(rec){
    var rows=[],g={},kn=0,conv=[],div=[],zero=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(!g[r.name]){ g[r.name]=r; kn++; if(r.conv) conv.push(r.name+'→'+r.lim); else div.push(r.name); }
      if(r.zero) zero++;
      rows.push([r.name, r.n, r.a, '<b>'+r.big+'</b>',
                 '<span class="'+(r.conv?'ok':'no')+'">'+(r.conv?'○':'×')+'</span>', r.lim]);
    }
    var stats=[
      {t:'시험한 수열',big:kn+'가지',p:'다섯 가지를 모두 기록하면 비교가 완성된다.'},
      {t:'수렴한 수열',big:conv.length+'가지',p:conv.join(', ')||'-'},
      {t:'수렴하지 않은 수열',big:div.length+'가지',p:div.join(', ')||'아직 없음'}
    ];
    var concl;
    if(kn<4){
      concl='<b>더 해 보자</b> — 다섯 수열을 <b>모두</b> 기록해야 수렴과 발산의 차이가 드러난다.';
    } else {
      concl='<b>정리</b> — 수렴은 “한 값에 한없이 가까워지는 것”이었다. '
           +(div.length?('  '+div.join(', ')+'처럼 값이 계속 튀면 수렴하지 않는다. '):'')
           +'√(n+1) − √n 은 ∞ − ∞ 꼴이라 얼핏 알 수 없어 보이지만 유리화하면 1/(√(n+1)+√n) 이라 <b>0으로 수렴</b>했다. '
           +'꼴만 보고 판단하지 말고 실제로 큰 n을 넣어 보거나 식을 변형해야 한다.';
    }
    return {head:['수열','n','aₙ','a₁₀₀₀₀','수렴?','다가가는 값'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 등비급수
# ============================================================
LAB_GEOS = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'등비급수 판',
  action:'항을 더해 나가기',
  hint0:'첫째항과 공비, 더할 항의 개수를 정해 보자.',
  sliders:[
    {id:'a',label:'첫째항',min:1,max:5,value:1,color:'#2563eb',unit:''},
    {id:'r',label:'공비 (÷10)',min:-15,max:15,value:5,color:'#dc2626',
     fmt:function(v){return (v/10).toFixed(1);}},
    {id:'n',label:'항의 개수 n',min:1,max:40,value:10,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var r=S.r/10;
    var parts=[],s=0,v=S.a,i;
    for(i=0;i<S.n;i++){ s+=v; parts.push(s); v*=r; }
    var conv=(Math.abs(r)<1);
    var lim=conv?(S.a/(1-r)):null;
    var big=0,v2=S.a;
    for(i=0;i<200;i++){ big+=v2; v2*=r; if(!isFinite(big)) break; }
    return {r:r,parts:parts,S:s,conv:conv,lim:lim,big:big};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'부분합 S'+S.n,v:ran?r4(c.S):'더해 보자'},
            {k:'a/(1−r)',v:c.conv?r4(c.lim):'수렴하지 않음'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'S'+S.n+' = '+r4(c.S)+'.  '+(c.conv?('a/(1−r) = '+r4(c.lim)+'에 다가간다.'):'|r| ≥ 1 이라 다가가는 값이 없다.')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var GX=44, GY=280, GW=356, GH=200;
    var mx=0,mn=0;
    for(i=0;i<S.n;i++){ if(c.parts[i]>mx) mx=c.parts[i]; if(c.parts[i]<mn) mn=c.parts[i]; }
    if(c.conv){ if(c.lim>mx) mx=c.lim; if(c.lim<mn) mn=c.lim; }
    var span=(mx-mn)||1;
    function py(v){ return GY-(v-mn)/span*GH; }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(GX,py(0));ctx.lineTo(GX+GW,py(0));ctx.stroke();
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*S.n);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=2.4;ctx.beginPath();
    for(i=0;i<S.n&&i<shown;i++){
      var x=GX+GW*(i+1)/S.n;
      if(i===0) ctx.moveTo(x,py(c.parts[i])); else ctx.lineTo(x,py(c.parts[i]));
    }
    if(shown>1) ctx.stroke();
    for(i=0;i<S.n&&i<shown;i++){
      var x2=GX+GW*(i+1)/S.n;
      ctx.beginPath();ctx.arc(x2,py(c.parts[i]),4,0,Math.PI*2);
      ctx.fillStyle='#2563eb';ctx.fill();
    }
    if(c.conv){
      ctx.strokeStyle='#7c3aed';ctx.lineWidth=2;ctx.setLineDash([5,4]);
      ctx.beginPath();ctx.moveTo(GX,py(c.lim));ctx.lineTo(GX+GW,py(c.lim));ctx.stroke();ctx.setLineDash([]);
      lbl(ctx,'a/(1−r) = '+r3(c.lim),GX+GW-8,py(c.lim)-8,'#6d28d9',13,'right');
    }
    lbl(ctx,'첫째항 '+S.a+', 공비 '+c.r,24,32,'#1d4ed8',18);
    lbl(ctx,'점 = 부분합 S₁, S₂, …',24,56,'#52627a',14);
    box(ctx,20,316,400,100);
    lbl(ctx,(t===null)?'계속 더하면 어떻게 될까?':('S'+S.n+' = '+r4(c.S)),38,348,'#1f2937',18);
    lbl(ctx,'|r| = '+r2(Math.abs(c.r))+'  →  '+(c.conv?'1보다 작다':'1 이상이다'),38,380,c.conv?'#15803d':'#b91c1c',17);
    lbl(ctx,(t===null)?'':(c.conv?('a/(1−r) = '+r4(c.lim)):'부분합이 한 값으로 다가가지 않는다'),38,408,'#52627a',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,r:c.r,n:S.n,S:r4(c.S),
            conv:c.conv,lim:c.conv?r4(c.lim):'없음',
            gap:c.conv?r4(Math.abs(c.S-c.lim)):'-',
            close:(c.conv&&Math.abs(c.S-c.lim)<0.01),
            absr:r2(Math.abs(c.r))};
  },
  headA:['번호','첫째항, 공비','|r|','n','부분합','a/(1−r)','수렴?','차이','0.01 이내?'],
  rowA:function(r,i){
    return [i+1,r.a+', '+r.r,r.absr,r.n,'<b>'+r.S+'</b>',r.lim,
            '<span class="'+(r.conv?'ok':'no')+'">'+(r.conv?'○':'×')+'</span>',
            r.gap,
            '<span class="'+(r.close?'ok':'no')+'">'+(r.close?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],conv=0,div=0,match=0,close=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.conv) conv++; else div++;
      if(r.conv===(parseFloat(r.absr)<1)) match++;
      if(r.close) close++;
      rows.push([r.a+', '+r.r, r.absr, r.n, '<b>'+r.S+'</b>', r.lim,
                 '<span class="'+(r.conv?'ok':'no')+'">'+(r.conv?'○':'×')+'</span>',
                 r.gap]);
    }
    var stats=[
      {t:'|r| < 1 일 때만 수렴',big:match+' / '+rec.length,
       p:'공비의 절댓값만 보고 수렴 여부를 판정할 수 있는지 확인한 결과.'},
      {t:'수렴 / 수렴 안 함',big:conv+'개 / '+div+'개',
       p:(conv&&div)?'두 경우를 모두 기록했다.':'|r|을 1보다 크게도 해 보자.'},
      {t:'부분합이 극한에 0.01 이내로 접근',big:close+' / '+rec.length,
       p:'n을 키울수록 가까워졌다.'}
    ];
    var concl;
    if(conv===0||div===0){
      concl='<b>더 해 보자</b> — 공비를 0.5처럼 작게, 1.2처럼 크게 <b>모두</b> 두고 기록해 보자.';
    } else if(match===rec.length){
      concl='<b>정리</b> — 등비급수는 <b>|r| < 1 일 때만</b> 부분합이 한 값 a/(1−r) 에 다가갔다. '
           +'|r| ≥ 1 이면 항이 줄어들지 않아 부분합이 계속 커지거나 튀었다. '
           +'r이 음수여도 |r| < 1 이면 위아래로 흔들리며 수렴했다. 판정 기준은 부호가 아니라 <b>절댓값</b>이다.';
    } else {
      concl='<b>확인 필요</b> — 판정이 어긋난 기록이 있다.';
    }
    return {head:['첫째항, 공비','|r|','n','부분합','a/(1−r)','수렴?','차이'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 일반항이 0인데 발산하는 급수
# ============================================================
LAB_HARM = BASE + r"""
var KINDS=['1/n','1/n²','1/√n'];
function term(kind,k){
  if(kind===0) return 1/k;
  if(kind===1) return 1/(k*k);
  return 1/Math.sqrt(k);
}
var LAB = {
  cw:440, ch:430, cvTitle:'급수 부분합 판',
  action:'끝까지 더해 보기',
  hint0:'수열을 고르고, 몇 번째 항까지 더할지 정해 보자.',
  sliders:[
    {id:'kind',label:'일반항',min:0,max:2,value:0,color:'#2563eb',fmt:function(v){return KINDS[v];}},
    {id:'e',label:'항의 개수 (10^?)',min:1,max:5,value:3,color:'#dc2626',
     fmt:function(v){return Math.pow(10,v)+'개';}}
  ],
  calc:function(S){
    var N=Math.pow(10,S.e), s=0, i;
    for(i=1;i<=N;i++) s+=term(S.kind,i);
    return {N:N,sum:s,last:term(S.kind,N),
            marks:[10,100,1000,10000,100000]};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'마지막 항',v:r6(c.last)},
            {k:'부분합',v:ran?r4(c.sum):'더해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return c.N+'개까지 더하면 '+r4(c.sum)+'이고 마지막 항은 '+r6(c.last)+'다. 항의 개수를 더 늘려 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var GX=54, GY=280, GW=340, GH=200;
    var vals=[],mx=0;
    for(i=1;i<=5;i++){
      var N=Math.pow(10,i), s=0, j;
      if(i>S.e){ vals.push(null); continue; }
      for(j=1;j<=N;j++) s+=term(S.kind,j);
      vals.push(s);
      if(s>mx) mx=s;
    }
    if(mx===0) mx=1;
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*S.e);
    for(i=0;i<5;i++){
      var x=GX+i*66;
      ctx.fillStyle='#94a3b8';ctx.font='11px sans-serif';ctx.textAlign='center';
      ctx.fillText('10^'+(i+1),x+22,GY+18);
      if(vals[i]===null||i>=shown) continue;
      var h=vals[i]/mx*GH;
      ctx.fillStyle='#93c5fd';ctx.fillRect(x,GY-h,44,h);
      ctx.strokeStyle='#2563eb';ctx.lineWidth=1.6;ctx.strokeRect(x,GY-h,44,h);
      ctx.fillStyle='#1d4ed8';ctx.font='bold 11px sans-serif';
      ctx.fillText(r2(vals[i]),x+22,GY-h-6);
    }
    ctx.textAlign='left';
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(GX-8,GY);ctx.lineTo(GX+340,GY);ctx.stroke();
    lbl(ctx,'aₙ = '+KINDS[S.kind]+' 의 부분합',24,32,'#1d4ed8',18);
    lbl(ctx,'가로 = 더한 항의 개수',24,56,'#52627a',14);
    box(ctx,20,306,400,110);
    lbl(ctx,'마지막 항 a'+c.N+' = '+r6(c.last)+'  (0에 가깝다)',38,338,'#52627a',16);
    lbl(ctx,(t===null)?'항이 0에 가까우면 합도 멈출까?':(c.N+'개까지의 합 = '+r4(c.sum)),38,372,'#1f2937',18);
    lbl(ctx,(t===null)?'':'항의 개수를 10배로 늘려 비교해 보자',38,404,'#94a3b8',15);
  },
  record:function(S){
    var c=this.calc(S);
    return {kind:S.kind,name:KINDS[S.kind],N:c.N,
            sum:r4(c.sum),last:r6(c.last),
            small:(c.last<0.01)};
  },
  headA:['번호','일반항','항의 개수','마지막 항','부분합','마지막 항 < 0.01?'],
  rowA:function(r,i){
    return [i+1,r.name,r.N,r.last,'<b>'+r.sum+'</b>',
            '<span class="'+(r.small?'ok':'no')+'">'+(r.small?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],g={},kn=0,grow=[],stop=[];
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(!g[r.kind]) g[r.kind]={name:r.name,pts:[]};
      g[r.kind].pts.push([r.N,parseFloat(r.sum)]);
      rows.push([r.name, r.N, r.last, '<b>'+r.sum+'</b>',
                 '<span class="'+(r.small?'ok':'no')+'">'+(r.small?'○':'×')+'</span>']);
    }
    var k;
    for(k in g){
      kn++;
      var p=g[k].pts;
      if(p.length<2) continue;
      p.sort(function(x,y){return x[0]-y[0];});
      var d=p[p.length-1][1]-p[0][1];
      if(d>0.5) grow.push(g[k].name+' (+'+r2(d)+')');
      else stop.push(g[k].name+' (+'+r2(d)+')');
    }
    var stats=[
      {t:'시험한 일반항',big:kn+'가지',p:'세 가지를 모두 기록해 비교하자.'},
      {t:'항을 늘릴수록 합이 계속 커진 것',big:grow.length+'가지',p:grow.join(', ')||'아직 없음'},
      {t:'합이 거의 멈춘 것',big:stop.length+'가지',p:stop.join(', ')||'아직 없음'}
    ];
    var concl;
    if(kn<3||(grow.length===0||stop.length===0)){
      concl='<b>더 해 보자</b> — 세 일반항 각각에서 항의 개수를 10개와 10만 개로 <b>모두</b> 기록해 비교해 보자.';
    } else {
      concl='<b>정리</b> — 세 수열 모두 일반항은 0에 가까워졌지만 <b>합의 운명은 갈렸다.</b> '
           +'1/n² 은 합이 거의 멈췄고, <b>1/n 과 1/√n 은 항의 개수를 10배로 늘릴 때마다 합이 계속 커졌다.</b> '
           +'즉 <b>aₙ → 0 은 급수가 수렴하기 위한 필요조건일 뿐 충분조건이 아니다.</b> '
           +'항이 0으로 가는 «속도»가 충분히 빨라야 합이 멈춘다.';
    }
    return {head:['일반항','개수','마지막 항','부분합','0에 가깝나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. e의 정의
# ============================================================
LAB_E = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'e 관찰판',
  action:'n을 키워 보기',
  hint0:'(1 + 1/n)ⁿ 에서 n을 얼마나 키울지 정해 보자.',
  sliders:[
    {id:'e',label:'n = 10^?',min:0,max:7,value:2,color:'#2563eb',
     fmt:function(v){return Math.pow(10,v)+'';}}
  ],
  calc:function(S){
    var n=Math.pow(10,S.e);
    var v=Math.pow(1+1/n,n);
    var wrong=1;
    var series=0,f=1,i;
    for(i=0;i<15;i++){ if(i>0) f*=i; series+=1/f; }
    return {n:n,v:v,e:Math.E,gap:Math.abs(Math.E-v),
            wrong:wrong,series:series};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'(1 + 1/n)ⁿ',v:ran?r6(c.v):'키워 보자'},
            {k:'e',v:r6(c.e)}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'n = '+c.n+' 일 때 (1+1/n)ⁿ = '+r6(c.v)+'.  e = '+r6(c.e)+'와의 차이는 '+r6(c.gap)+'다. n을 더 키워 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var GX=54, GY=250, GW=340, GH=170;
    var lo=2, hi=2.9;
    function py(v){ return GY-(v-lo)/(hi-lo)*GH; }
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=0;i<=9;i++){
      var v=2+i*0.1;
      ctx.beginPath();ctx.moveTo(GX,py(v));ctx.lineTo(GX+GW,py(v));ctx.stroke();
      if(i%2===0) lbl(ctx,r1(v),GX-30,py(v)+4,'#94a3b8',12);
    }
    ctx.strokeStyle='#7c3aed';ctx.lineWidth=2.4;ctx.setLineDash([5,4]);
    ctx.beginPath();ctx.moveTo(GX,py(Math.E));ctx.lineTo(GX+GW,py(Math.E));ctx.stroke();ctx.setLineDash([]);
    lbl(ctx,'e = 2.718…',GX+GW-6,py(Math.E)-8,'#6d28d9',13,'right');
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*(S.e+1));
    for(i=0;i<=S.e;i++){
      if(i>=shown) break;
      var n=Math.pow(10,i);
      var val=Math.pow(1+1/n,n);
      var x=GX+GW*i/7;
      if(val>=lo&&val<=hi){
        ctx.beginPath();ctx.arc(x,py(val),6,0,Math.PI*2);
        ctx.fillStyle='#2563eb';ctx.fill();
        ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      }
      ctx.fillStyle='#94a3b8';ctx.font='11px sans-serif';ctx.textAlign='center';
      ctx.fillText('10^'+i,x,GY+18);
    }
    ctx.textAlign='left';
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+GW,GY);ctx.stroke();
    lbl(ctx,'(1 + 1/n)ⁿ 의 값',24,32,'#1d4ed8',18);
    box(ctx,20,282,400,102);
    lbl(ctx,'n = '+c.n,38,314,'#52627a',17);
    lbl(ctx,(t===null)?'n을 키우면 어디로 갈까?':('(1+1/n)ⁿ = '+r6(c.v)),38,348,'#1f2937',18);
    lbl(ctx,(t===null)?'':('e = '+r6(c.e)+'      차이 '+r6(c.gap)),38,376,'#15803d',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {n:c.n,v:r6(c.v),e:r6(c.e),gap:r6(c.gap),
            close:(c.gap<0.01),
            over:(c.v>Math.E),
            one:(Math.abs(c.v-1)<1e-9)};
  },
  headA:['번호','n','(1+1/n)ⁿ','e','차이','0.01 이내?','e보다 큰가?'],
  rowA:function(r,i){
    return [i+1,r.n,'<b>'+r.v+'</b>',r.e,r.gap,
            '<span class="'+(r.close?'ok':'no')+'">'+(r.close?'○':'×')+'</span>',
            '<span class="'+(r.over?'ok':'no')+'">'+(r.over?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],close=0,over=0,arr=[],mono=true;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.close) close++;
      if(r.over) over++;
      arr.push([r.n,parseFloat(r.gap)]);
      rows.push([r.n, '<b>'+r.v+'</b>', r.gap,
                 '<span class="'+(r.close?'ok':'no')+'">'+(r.close?'○':'×')+'</span>',
                 '<span class="'+(r.over?'ok':'no')+'">'+(r.over?'○':'×')+'</span>']);
    }
    arr.sort(function(x,y){return x[0]-y[0];});
    for(i=1;i<arr.length;i++){ if(arr[i][1]>arr[i-1][1]+1e-12) mono=false; }
    var stats=[
      {t:'e와의 차이가 0.01 이내',big:close+' / '+rec.length,p:'n이 클수록 가까워졌다.'},
      {t:'n이 커질수록 차이가 줄어듦',big:(arr.length<2)?'비교 없음':(mono?'그렇다':'들쭉날쭉'),
       p:'n을 1, 10, 100, … 로 키워 가며 기록했다.'},
      {t:'e보다 컸던 기록',big:over+'개',
       p:over?'계산 오차로 넘을 수 있다.':'값은 아래에서 e로 다가간다.'}
    ];
    var concl;
    if(arr.length<3){
      concl='<b>더 해 보자</b> — n을 1, 10, 100, 10000 처럼 여러 값으로 기록해 보자.';
    } else if(mono){
      concl='<b>정리</b> — 1보다 아주 조금 큰 수를 아주 여러 번 거듭제곱하면 <b>1도 무한대도 아닌 일정한 값 e = 2.718…</b> 로 다가갔다. '
           +'밑은 1에 가까워지고 지수는 커지는 두 힘이 균형을 이루기 때문이다. '
           +'e는 이렇게 «극한으로 정의된 수»이고, 이 정의 덕분에 (eˣ)′ = eˣ 라는 성질이 나온다.';
    } else {
      concl='<b>정리</b> — 값이 e로 다가갔다. n이 너무 크면 컴퓨터 계산 오차가 생길 수 있으니 함께 살펴보자.';
    }
    return {head:['n','(1+1/n)ⁿ','차이','0.01 이내?','e보다 큰가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 지수·로그함수의 미분
# ============================================================
LAB_EXPD = BASE + r"""
var KINDS=['eˣ','ln x','2ˣ','x²'];
function fx(kind,x){
  if(kind===0) return Math.exp(x);
  if(kind===1) return Math.log(x);
  if(kind===2) return Math.pow(2,x);
  return x*x;
}
function theory(kind,x){
  if(kind===0) return Math.exp(x);
  if(kind===1) return 1/x;
  if(kind===2) return Math.pow(2,x)*Math.log(2);
  return 2*x;
}
var LAB = {
  cw:440, ch:430, cvTitle:'도함수 확인판',
  action:'수치로 미분하기',
  hint0:'함수와 확인할 x를 정해 보자.',
  sliders:[
    {id:'kind',label:'함수',min:0,max:3,value:0,color:'#2563eb',fmt:function(v){return KINDS[v];}},
    {id:'x0',label:'x (÷10)',min:2,max:30,value:10,color:'#dc2626',
     fmt:function(v){return (v/10).toFixed(1);}}
  ],
  calc:function(S){
    var x=S.x0/10, h=1e-6;
    var num=(fx(S.kind,x+h)-fx(S.kind,x-h))/(2*h);
    var th=theory(S.kind,x);
    return {x:x,f:fx(S.kind,x),num:num,th:th,
            ratio:(fx(S.kind,x)===0)?null:(num/fx(S.kind,x))};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'수치 미분값',v:ran?r4(c.num):'미분해 보자'},
            {k:'f(x)',v:r4(c.f)}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return "f′("+c.x+') = '+r4(c.num)+', f('+c.x+') = '+r4(c.f)+'.  두 값의 비는 '+((c.ratio===null)?'-':r4(c.ratio))+'다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var GX=50, GY=290, XU=100, YU=28;
    function px(x){ return GX+x*XU; }
    function py(y){ return GY-y*YU; }
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=0;i<=3;i++){ ctx.beginPath();ctx.moveTo(px(i),GY-8*YU);ctx.lineTo(px(i),GY+2*YU);ctx.stroke(); }
    for(i=-2;i<=8;i++){ ctx.beginPath();ctx.moveTo(GX,py(i));ctx.lineTo(GX+3.4*XU,py(i));ctx.stroke(); }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+3.4*XU,GY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(GX,GY-8*YU);ctx.lineTo(GX,GY+2*YU);ctx.stroke();
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    var st=false;
    for(i=1;i<=340;i++){
      var x=i/100, y=fx(S.kind,x);
      if(y<-2||y>8){ st=false; continue; }
      if(!st){ ctx.moveTo(px(x),py(y)); st=true; } else ctx.lineTo(px(x),py(y));
    }
    ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0&&Math.abs(c.f)<=8){
      ctx.strokeStyle='#dc2626';ctx.lineWidth=3;
      ctx.beginPath();
      ctx.moveTo(px(c.x-0.6),py(c.f-c.num*0.6));
      ctx.lineTo(px(c.x+0.6),py(c.f+c.num*0.6));ctx.stroke();
      ctx.beginPath();ctx.arc(px(c.x),py(c.f),6,0,Math.PI*2);
      ctx.fillStyle='#1f2937';ctx.fill();
    }
    lbl(ctx,'f(x) = '+KINDS[S.kind],24,32,'#1d4ed8',18);
    box(ctx,20,318,400,100);
    lbl(ctx,(t===null)?'도함수는 무엇일까?':("수치 미분 f′("+c.x+') = '+r4(c.num)),38,350,'#1f2937',18);
    lbl(ctx,'f('+c.x+') = '+r4(c.f)+"      f′/f = "+((c.ratio===null)?'-':r4(c.ratio)),38,382,'#52627a',17);
    lbl(ctx,(t===null)?'':('이론값 '+r4(c.th)),38,410,'#15803d',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {kind:S.kind,name:KINDS[S.kind],x:c.x,
            f:r4(c.f),num:r4(c.num),th:r4(c.th),
            ok:(Math.abs(c.num-c.th)<1e-3*Math.max(1,Math.abs(c.th))),
            selfEq:(Math.abs(c.num-c.f)<1e-3*Math.max(1,Math.abs(c.f))),
            inv:(Math.abs(c.num-1/c.x)<1e-6)};
  },
  headA:['번호','함수','x','f(x)','수치 미분','이론값','같나?','f′ = f?','f′ = 1/x?'],
  rowA:function(r,i){
    return [i+1,r.name,r.x,r.f,'<b>'+r.num+'</b>',r.th,
            '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
            '<span class="'+(r.selfEq?'ok':'no')+'">'+(r.selfEq?'○':'×')+'</span>',
            '<span class="'+(r.inv?'ok':'no')+'">'+(r.inv?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ok=0,g={},kn=0,selfList=[],invList=[];
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.ok) ok++;
      if(!g[r.name]){ g[r.name]={self:true,inv:true}; kn++; }
      if(!r.selfEq) g[r.name].self=false;
      if(!r.inv) g[r.name].inv=false;
      rows.push([r.name, r.x, r.f, '<b>'+r.num+'</b>', r.th,
                 '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
                 '<span class="'+(r.selfEq?'ok':'no')+'">'+(r.selfEq?'○':'×')+'</span>']);
    }
    var k;
    for(k in g){ if(g[k].self) selfList.push(k); if(g[k].inv) invList.push(k); }
    var stats=[
      {t:'수치 미분 = 이론값',big:ok+' / '+rec.length,p:'중앙차분으로 구한 값과 공식을 비교한 결과.'},
      {t:'f′ = f 인 함수',big:selfList.length+'가지',p:selfList.join(', ')||'아직 없음'},
      {t:'f′ = 1/x 인 함수',big:invList.length+'가지',p:invList.join(', ')||'아직 없음'}
    ];
    var concl;
    if(kn<3){
      concl='<b>더 해 보자</b> — 네 함수를 <b>모두</b> 기록해야 차이가 드러난다.';
    } else if(ok===rec.length){
      concl='<b>정리</b> — 수치 미분과 공식이 모두 일치했다. '
           +'특히 <b>eˣ 은 미분해도 자기 자신</b>이었고, <b>ln x 는 1/x</b> 가 되었다. '
           +'2ˣ 도 자기 자신의 상수배지만 그 상수가 ln 2 라서 정확히 자기 자신은 아니다. '
           +'e를 밑으로 쓰는 이유가 바로 이 성질 때문이다.';
    } else {
      concl='<b>확인 필요</b> — 수치 미분과 이론값이 어긋난 기록이 있다.';
    }
    return {head:['함수','x','f(x)','수치 미분','이론값','같나?',"f′=f?"],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("hm_sequence_limit_lab_Calculus2_SeqLimit_Ep02.html",
     "수열의 극한 실험실 — ∞ − ∞ 는 얼마일까?",
     "수열의 극한 실험실 — ∞ − ∞ 는 얼마일까?",
     "여러 수열의 항을 큰 n까지 따라가며 수렴하는지 판정한다.",
     LAB_SEQ),
    ("hm_geometric_series_lab_Calculus2_SeqLimit_Ep06.html",
     "등비급수 실험실 — 언제 합이 멈출까?",
     "등비급수 실험실 — 언제 합이 멈출까?",
     "공비를 바꿔 가며 부분합이 한 값에 다가가는지 확인하고 a/(1−r)과 비교한다.",
     LAB_GEOS),
    ("hm_harmonic_series_lab_Calculus2_SeqLimit_Ep05.html",
     "급수 실험실 — 항이 0으로 가면 합도 멈출까?",
     "급수 실험실 — 항이 0으로 가면 합도 멈출까?",
     "일반항이 0에 가까워지는 세 급수를 10만 항까지 더해 합의 운명을 비교한다.",
     LAB_HARM),
    ("hm_number_e_lab_Calculus2_FuncLimit_Ep01.html",
     "e 실험실 — 1의 무한제곱은 1일까?",
     "e 실험실 — 1의 무한제곱은 1일까?",
     "(1 + 1/n)ⁿ 에서 n을 키워 가며 값이 어디로 다가가는지 기록한다.",
     LAB_E),
    ("hm_exp_log_derivative_lab_Calculus2_FuncLimit_Ep05.html",
     "도함수 실험실 — 미분해도 그대로인 함수가 있을까?",
     "도함수 실험실 — 미분해도 그대로인 함수가 있을까?",
     "네 함수를 수치로 미분해 f′와 f, 1/x 를 비교한다.",
     LAB_EXPD),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c33_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
