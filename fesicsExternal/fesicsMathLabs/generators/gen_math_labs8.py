# -*- coding: utf-8 -*-
"""초등 5-6학년군 '자료와 가능성' 실험 5종"""
import os, re

OUT = "/mnt/user-data/outputs"
src = open("/home/claude/gen_math_labs.py", encoding="utf-8").read()
TPL = re.search(r'TPL = r"""(.*?)"""\n', src, re.S).group(1)

BASE = r"""
function lbl(ctx,t,x,y,c,sz,al){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
function box(ctx,x,y,w,h){ctx.fillStyle='#f1f6fd';ctx.fillRect(x,y,w,h);ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(x,y,w,h);}
function r1(v){return Math.round(v*10)/10;}
function r2(v){return Math.round(v*100)/100;}
function gcd(x,y){while(y){var t=x%y;x=y;y=t;}return x;}
"""

# ============================================================
# 1. 평균 — 고르게 하기
# ============================================================
LAB_MEAN = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'평균 고르기판',
  action:'평평하게 고르기',
  hint0:'네 사람이 모은 딱지 수를 정하고, 똑같이 나누어 보자.',
  sliders:[
    {id:'a',label:'가',min:0,max:20,value:2,color:'#ef4444',unit:'개'},
    {id:'b',label:'나',min:0,max:20,value:4,color:'#f59e0b',unit:'개'},
    {id:'c',label:'다',min:0,max:20,value:6,color:'#22c55e',unit:'개'},
    {id:'d',label:'라',min:0,max:20,value:20,color:'#3b82f6',unit:'개'}
  ],
  vals:function(S){ return [S.a,S.b,S.c,S.d]; },
  readout:function(S,ran){
    var v=this.vals(S), s=v[0]+v[1]+v[2]+v[3];
    return [{k:'합계',v:s+'개'},{k:'평균',v:ran?(r2(s/4)+'개'):'고르게 해 보자'}];
  },
  doneMsg:function(S){
    var v=this.vals(S), s=v[0]+v[1]+v[2]+v[3], m=s/4;
    var sorted=v.slice().sort(function(x,y){return x-y;});
    var mid=(sorted[1]+sorted[2])/2;
    return '평균은 '+r2(m)+'개다. 가운데 값은 '+r2(mid)+'개로 '+((Math.abs(m-mid)<0.005)?'마침 같다':'다르다')+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var v=this.vals(S), NAMES=['가','나','다','라'], COLS=['#ef4444','#f59e0b','#22c55e','#3b82f6'];
    var s=v[0]+v[1]+v[2]+v[3], m=s/4, i;
    var lvl=(t===null)?0:Math.min(1,t);
    var CELL=12, BX=70, BY=270;
    for(i=0;i<4;i++){
      var cur=v[i]+(m-v[i])*lvl;
      var x=BX+i*76, h=cur*CELL;
      ctx.fillStyle=COLS[i];ctx.fillRect(x,BY-h,52,h);
      ctx.strokeStyle='#334155';ctx.lineWidth=2;ctx.strokeRect(x,BY-h,52,h);
      ctx.fillStyle='#334155';ctx.font='bold 16px sans-serif';ctx.textAlign='center';
      ctx.fillText(NAMES[i],x+26,BY+22);
      ctx.fillStyle='#1f2937';ctx.font='bold 14px sans-serif';
      ctx.fillText(r1(cur),x+26,BY-h-8);
    }
    ctx.textAlign='left';
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(BX-14,BY);ctx.lineTo(400,BY);ctx.stroke();
    if(lvl>0){
      ctx.strokeStyle='#7c3aed';ctx.lineWidth=2.5;ctx.setLineDash([6,5]);
      ctx.beginPath();ctx.moveTo(BX-14,BY-m*CELL);ctx.lineTo(400,BY-m*CELL);ctx.stroke();ctx.setLineDash([]);
      lbl(ctx,'평균 '+r2(m),BX-16,BY-m*CELL-8,'#6d28d9',15);
    }
    lbl(ctx,'네 사람의 딱지를 똑같이 나누면?',24,36,'#1d4ed8',19);
    box(ctx,20,308,400,76);
    lbl(ctx,'합계 '+s+'개  ÷  사람 수 4  =  '+((t===null)?'?':r2(m)),38,340,'#1f2937',20);
    var sorted=v.slice().sort(function(x,y){return x-y;});
    lbl(ctx,(t===null)?'':('가운데 값 : '+r2((sorted[1]+sorted[2])/2)+'개    가장 큰 값 : '+sorted[3]+'개'),38,370,'#52627a',17);
  },
  record:function(S){
    var v=this.vals(S), s=v[0]+v[1]+v[2]+v[3], m=s/4;
    var so=v.slice().sort(function(x,y){return x-y;});
    var mid=(so[1]+so[2])/2;
    var inData=(v.indexOf(m)>=0);
    return {v:v.join(', '),sum:s,mean:r2(m),mid:r2(mid),
            same:(Math.abs(m-mid)<0.005),range:so[3]-so[0],inData:inData,
            chk:r2(s/4)};
  },
  headA:['번호','자료','합계','평균','가운데 값','평균=가운데 값?','자료 중에 평균이 있나?'],
  rowA:function(r,i){
    return [i+1,r.v,r.sum,'<b>'+r.mean+'</b>',r.mid,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            '<span class="'+(r.inData?'ok':'no')+'">'+(r.inData?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ok=0,same=0,inData=0,maxRange=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var a=(Math.abs(r.mean-r.chk)<0.005);
      if(a) ok++;
      if(r.same) same++;
      if(r.inData) inData++;
      if(r.range>maxRange) maxRange=r.range;
      rows.push([r.v, r.sum, '<b>'+r.mean+'</b>', r.mid,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 '<span class="'+(r.inData?'ok':'no')+'">'+(r.inData?'○':'×')+'</span>',
                 r.range]);
    }
    var stats=[
      {t:'평균 = 합계 ÷ 개수',big:ok+' / '+rec.length,p:'막대를 평평하게 고른 높이와 계산이 일치했는지 확인한 결과.'},
      {t:'평균이 가운데 값과 같았던 횟수',big:same+' / '+rec.length,p:'평균은 가운데 값과 다를 수 있다.'},
      {t:'평균이 자료 안에 실제로 있었던 횟수',big:inData+' / '+rec.length,
       p:'가장 큰 값과 작은 값의 차가 가장 컸던 기록은 '+maxRange+'.'}
    ];
    var concl;
    if(same<rec.length){
      concl='<b>정리</b> — 평균은 <b>합계를 개수로 나눈 값</b>, 즉 모두 똑같이 나눠 가졌을 때의 값이었다. '
           +'가운데 값과 같을 때도 있었지만 '+(rec.length-same)+'번은 달랐다. 특히 한 명이 아주 많이 가지면 평균이 그쪽으로 끌려간다. '
           +'평균은 자료 중 하나가 아닐 수도 있다.';
    } else {
      concl='<b>정리</b> — 평균은 합계를 개수로 나눈 값이었다. 한 사람만 값을 크게 올려서 평균이 가운데 값과 달라지는 경우도 만들어 보자.';
    }
    return {head:['자료','합계','평균','가운데 값','같은가?','자료에 있나?','최대−최소'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 전체 평균
# ============================================================
LAB_TOTMEAN = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'두 모둠 평균판',
  action:'두 모둠을 합쳐 보기',
  hint0:'두 모둠의 인원과 평균 점수를 정하고, 합쳤을 때 전체 평균을 구해 보자.',
  sliders:[
    {id:'na',label:'가 모둠 인원',min:1,max:20,value:5,color:'#dc2626',unit:'명'},
    {id:'ma',label:'가 모둠 평균',min:1,max:20,value:16,color:'#f87171',unit:'점'},
    {id:'nb',label:'나 모둠 인원',min:1,max:20,value:15,color:'#2563eb',unit:'명'},
    {id:'mb',label:'나 모둠 평균',min:1,max:20,value:8,color:'#60a5fa',unit:'점'}
  ],
  calc:function(S){
    var tot=(S.na*S.ma+S.nb*S.mb)/(S.na+S.nb);
    return {sa:S.na*S.ma,sb:S.nb*S.mb,tot:tot,naive:(S.ma+S.mb)/2,n:S.na+S.nb};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'두 평균의 평균',v:r2(c.naive)+'점'},
            {k:'전체 평균',v:ran?(r2(c.tot)+'점'):'합쳐 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '전체 평균은 '+r2(c.tot)+'점이다. 두 평균의 평균 '+r2(c.naive)+'점과 '+((Math.abs(c.tot-c.naive)<0.005)?'같다':'다르다')+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var mv=(t===null)?0:Math.min(1,t);
    function group(y,n,m,col,name){
      lbl(ctx,name+'  '+n+'명 · 평균 '+m+'점',36,y-8,'#334155',17);
      for(i=0;i<n;i++){
        var x=40+(i%20)*18, yy=y+Math.floor(i/20)*20;
        ctx.beginPath();ctx.arc(x+7,yy+7,6.5,0,Math.PI*2);
        ctx.fillStyle=col;ctx.fill();
      }
    }
    group(60,S.na,S.ma,'#ef4444','가');
    group(130,S.nb,S.mb,'#3b82f6','나');
    var BX=40,BW=360,BY=210;
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(BX,BY+30);ctx.lineTo(BX+BW,BY+30);ctx.stroke();
    function mark(v,col,label,dy){
      var x=BX+BW*(v-0)/21;
      ctx.beginPath();ctx.moveTo(x,BY+30);ctx.lineTo(x,BY+30-24);
      ctx.strokeStyle=col;ctx.lineWidth=3;ctx.stroke();
      lbl(ctx,label,x,BY+30-30+dy,col,14,'center');
    }
    mark(S.ma,'#ef4444','가 '+S.ma,0);
    mark(S.mb,'#3b82f6','나 '+S.mb,0);
    if(mv>0){
      var vv=c.naive+(c.tot-c.naive)*mv;
      var x=BX+BW*vv/21;
      ctx.beginPath();ctx.moveTo(x,BY+30);ctx.lineTo(x,BY+62);
      ctx.strokeStyle='#7c3aed';ctx.lineWidth=3;ctx.stroke();
      lbl(ctx,'전체 '+r2(vv),x,BY+80,'#6d28d9',15,'center');
    }
    lbl(ctx,'두 모둠을 합치면 평균은?',24,36,'#1d4ed8',19);
    box(ctx,20,306,400,80);
    lbl(ctx,(t===null)?'두 평균을 그냥 더해 2로 나누면 될까?':('전체 평균 = ('+c.sa+' + '+c.sb+') ÷ '+c.n+' = '+r2(c.tot)),38,338,'#1f2937',19);
    lbl(ctx,'두 평균의 평균 = ('+S.ma+' + '+S.mb+') ÷ 2 = '+r2(c.naive),38,368,'#b91c1c',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {na:S.na,ma:S.ma,nb:S.nb,mb:S.mb,tot:r2(c.tot),naive:r2(c.naive),
            same:(Math.abs(c.tot-c.naive)<0.005),sameN:(S.na===S.nb),n:c.n,sum:c.sa+c.sb};
  },
  headA:['번호','가 모둠','나 모둠','전체 인원','전체 점수 합','전체 평균','두 평균의 평균','같은가?'],
  rowA:function(r,i){
    return [i+1,r.na+'명·'+r.ma+'점',r.nb+'명·'+r.mb+'점',r.n,r.sum,'<b>'+r.tot+'</b>',r.naive,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,eqN=0,eqNsame=0,diffN=0,diffNsame=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++;
      if(r.sameN){ eqN++; if(r.same) eqNsame++; }
      else { diffN++; if(r.same) diffNsame++; }
      rows.push([r.na+'명('+r.ma+'점) + '+r.nb+'명('+r.mb+'점)', r.sameN?'같음':'다름',
                 '<b>'+r.tot+'</b>', r.naive,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'“두 평균의 평균”이 맞은 횟수',big:same+' / '+rec.length,p:'전체 평균과 같았던 기록 수.'},
      {t:'인원이 같았던 기록',big:eqN+'개',p:eqN?('그중 두 값이 같았던 것 '+eqNsame+'개.'):'인원을 같게 한 경우도 기록해 보자.'},
      {t:'인원이 달랐던 기록',big:diffN+'개',p:diffN?('그중 두 값이 같았던 것 '+diffNsame+'개.'):'인원을 다르게 한 경우도 기록해 보자.'}
    ];
    var concl;
    if(eqN===0||diffN===0){
      concl='<b>더 해 보자</b> — 인원이 <b>같은 경우와 다른 경우</b>를 모두 기록해야 규칙이 보인다.';
    } else if(diffNsame===0 && eqNsame===eqN){
      concl='<b>정리</b> — 두 모둠의 인원이 같을 때만 “두 평균의 평균”이 전체 평균과 같았고, '
           +'인원이 다른 '+diffN+'번은 모두 틀렸다. 평균은 사람 수를 업고 다니는 값이라서, '
           +'<b>전체 평균 = 전체 합계 ÷ 전체 인원</b>으로 다시 구해야 한다. 인원이 많은 쪽 평균에 더 가깝게 끌려간다.';
    } else {
      concl='<b>확인 필요</b> — 규칙과 어긋난 기록이 있다. 값을 다시 확인해 보자.';
    }
    return {head:['두 모둠','인원','전체 평균','두 평균의 평균','같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 띠그래프·원그래프와 백분율
# ============================================================
LAB_PIE = BASE + r"""
var NAMES=['축구','농구','피구','기타'], COLS=['#ef4444','#3b82f6','#22c55e','#a855f7'];
var LAB = {
  cw:440, ch:430, cvTitle:'원그래프판',
  action:'백분율 구하고 그리기',
  hint0:'항목별 학생 수를 정하고, 백분율과 원그래프 조각을 구해 보자.',
  sliders:[
    {id:'a',label:'축구',min:1,max:40,value:12,color:'#ef4444',unit:'명'},
    {id:'b',label:'농구',min:1,max:40,value:9,color:'#3b82f6',unit:'명'},
    {id:'c',label:'피구',min:1,max:40,value:7,color:'#22c55e',unit:'명'},
    {id:'d',label:'기타',min:1,max:40,value:2,color:'#a855f7',unit:'명'}
  ],
  calc:function(S){
    var v=[S.a,S.b,S.c,S.d], tot=v[0]+v[1]+v[2]+v[3], p=[],rp=[],ang=[],i;
    for(i=0;i<4;i++){ p.push(v[i]/tot*100); rp.push(Math.round(v[i]/tot*100)); ang.push(v[i]/tot*360); }
    var rsum=rp[0]+rp[1]+rp[2]+rp[3];
    return {v:v,tot:tot,p:p,rp:rp,ang:ang,rsum:rsum};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'전체',v:c.tot+'명'},
            {k:'반올림한 백분율 합',v:ran?(c.rsum+'%'):'구해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '반올림한 백분율의 합은 '+c.rsum+'%다. '+((c.rsum===100)?'딱 100%가 되었다.':'100%가 아니다! 반올림 때문이다.')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var grow=(t===null)?0:Math.min(1,t);
    var CX=140, CY=150, R=98, acc=-Math.PI/2;
    for(i=0;i<4;i++){
      var sw=c.ang[i]*Math.PI/180*grow;
      ctx.beginPath();ctx.moveTo(CX,CY);ctx.arc(CX,CY,R,acc,acc+sw);ctx.closePath();
      ctx.fillStyle=COLS[i];ctx.fill();
      ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      acc+=c.ang[i]*Math.PI/180;
    }
    ctx.beginPath();ctx.arc(CX,CY,R,0,Math.PI*2);
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;ctx.stroke();
    for(i=0;i<4;i++){
      var y=70+i*30;
      ctx.fillStyle=COLS[i];ctx.fillRect(276,y-12,18,18);
      ctx.strokeStyle='#334155';ctx.lineWidth=1.5;ctx.strokeRect(276,y-12,18,18);
      lbl(ctx,NAMES[i]+' '+c.v[i]+'명'+((grow>=1)?('  '+c.rp[i]+'%'):''),302,y+2,'#334155',16);
    }
    var BX=40,BW=360,BY=282,ax=0;
    for(i=0;i<4;i++){
      var w=BW*c.v[i]/c.tot*grow;
      ctx.fillStyle=COLS[i];ctx.fillRect(BX+ax,BY,w,30);
      ax+=w;
    }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;ctx.strokeRect(BX,BY,BW,30);
    lbl(ctx,'띠그래프',BX,BY-8,'#52627a',15);
    lbl(ctx,'좋아하는 운동 (전체 '+c.tot+'명)',24,34,'#1d4ed8',18);
    box(ctx,20,326,400,84);
    lbl(ctx,(t===null)?'백분율의 합은 정확히 100%가 될까?':('반올림한 백분율의 합 : '+c.rsum+'%'),38,356,(c.rsum===100)?'#15803d':'#b91c1c',20);
    lbl(ctx,(t===null)?'':('중심각의 합 : '+r1(c.ang[0]+c.ang[1]+c.ang[2]+c.ang[3])+'°   (1% = 3.6°)'),38,388,'#52627a',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {v:c.v.join(', '),tot:c.tot,rp:c.rp.join(' / '),rsum:c.rsum,
            angsum:r1(c.ang[0]+c.ang[1]+c.ang[2]+c.ang[3]),
            a1:r1(c.ang[0]),p1:c.rp[0],
            exact:(Math.abs(c.p[0]-c.rp[0])<0.0001&&Math.abs(c.p[1]-c.rp[1])<0.0001&&Math.abs(c.p[2]-c.rp[2])<0.0001&&Math.abs(c.p[3]-c.rp[3])<0.0001)};
  },
  headA:['번호','학생 수','전체','반올림한 백분율','백분율 합','중심각 합','축구 중심각','축구 % × 3.6'],
  rowA:function(r,i){
    return [i+1,r.v,r.tot+'명',r.rp,'<b>'+r.rsum+'%</b>',r.angsum+'°',r.a1+'°',r1(r.p1*3.6)+'°'];
  },
  analyze:function(rec){
    var rows=[],hundred=0,three60=0,exact=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var a=(r.rsum===100), b=(Math.abs(r.angsum-360)<0.5);
      if(a) hundred++;
      if(b) three60++;
      if(r.exact) exact++;
      rows.push([r.v+' (전체 '+r.tot+'명)', r.rp, '<b>'+r.rsum+'%</b>',
                 '<span class="'+(a?'ok':'no')+'">'+(a?'○':'×')+'</span>',
                 r.angsum+'°',
                 '<span class="'+(b?'ok':'no')+'">'+(b?'○':'×')+'</span>',
                 r.exact?'나누어떨어짐':'반올림함']);
    }
    var stats=[
      {t:'반올림한 백분율의 합이 100%',big:hundred+' / '+rec.length,
       p:'항상 100%가 되지는 않았다.'},
      {t:'중심각의 합이 360°',big:three60+' / '+rec.length,
       p:'반올림하지 않은 값으로 계산하면 언제나 360°다.'},
      {t:'딱 나누어떨어진 기록',big:exact+'개',
       p:exact<rec.length?'나머지가 있으면 반올림이 필요하고, 그때 합이 어긋날 수 있다.':'전체 인원을 20명이나 30명처럼 바꿔 반올림이 생기게 해 보자.'}
    ];
    var concl;
    if(hundred===rec.length){
      concl='<b>정리</b> — 지금까지는 백분율의 합이 모두 100%였다. 전체 인원을 나누어떨어지지 않게 바꿔서 반올림이 생기면 어떻게 되는지 확인해 보자.';
    } else {
      concl='<b>정리</b> — 중심각의 합은 언제나 360°였지만, <b>반올림한 백분율의 합은 100%가 아닐 때가 '+(rec.length-hundred)+'번</b> 있었다. '
           +'백분율은 반올림한 값이라서 그렇다. 원그래프를 만들 때는 반올림한 %가 아니라 실제 비율로 중심각을 정해야 하고, '
           +'1%는 3.6°다.';
    }
    return {head:['자료','반올림한 %','% 합','100%인가?','중심각 합','360°인가?','비고'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 동전 던지기와 가능성
# ============================================================
LAB_COIN = BASE + r"""
var LAB = {
  cw:440, ch:420, cvTitle:'동전 던지기판',
  action:'던지기',
  hint0:'몇 번 던질지 정하고 던져 보자. 던질 때마다 결과가 달라진다.',
  _trial:null,
  sliders:[
    {id:'n',label:'던지는 횟수',min:10,max:200,step:10,value:20,color:'#2563eb',unit:'번'}
  ],
  gen:function(S){
    var arr=[],i,h=0;
    for(i=0;i<S.n;i++){ var f=(Math.random()<0.5)?1:0; arr.push(f); h+=f; }
    this._trial={arr:arr,h:h,n:S.n};
  },
  readout:function(S,ran){
    var tr=this._trial;
    return [{k:'앞면',v:(ran&&tr)?(tr.h+'번'):'던져 보자'},
            {k:'앞면 비율',v:(ran&&tr)?(r1(tr.h/tr.n*100)+'%'):'-'}];
  },
  doneMsg:function(S){
    var tr=this._trial;
    return S.n+'번 중 앞면 '+tr.h+'번 ('+r1(tr.h/tr.n*100)+'%). 50%에서 '+r1(Math.abs(tr.h/tr.n*100-50))+'%p 벗어났다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    if(t===null){ this._trial=null; }
    else if(!this._trial){ this.gen(S); }
    var tr=this._trial, i;
    lbl(ctx,'동전을 '+S.n+'번 던지면 앞면은 몇 번?',24,36,'#1d4ed8',19);
    if(!tr){
      lbl(ctx,'가능성으로는 앞면이 나올 가능성이 1/2 이다.',24,70,'#52627a',17);
      lbl(ctx,'정말 절반이 나올까? 던져서 확인해 보자.',24,98,'#52627a',17);
    } else {
      var shown=Math.ceil(Math.min(1,t)*tr.n);
      var per=20, cell=Math.min(18, 380/per);
      var run=0;
      ctx.strokeStyle='#e2e8f0';ctx.lineWidth=1.4;
      for(i=0;i<shown;i++){
        var x=34+(i%per)*cell, y=60+Math.floor(i/per)*cell;
        ctx.beginPath();ctx.arc(x+cell/2,y+cell/2,cell*0.36,0,Math.PI*2);
        ctx.fillStyle=tr.arr[i]?'#f59e0b':'#cbd5e1';ctx.fill();
      }
      var hh=0;
      for(i=0;i<shown;i++){ hh+=tr.arr[i]; }
      var GY=330, GX=34, GW=372;
      ctx.strokeStyle='#334155';ctx.lineWidth=2;
      ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+GW,GY);ctx.stroke();
      ctx.strokeStyle='#7c3aed';ctx.lineWidth=2;ctx.setLineDash([5,4]);
      ctx.beginPath();ctx.moveTo(GX,GY-40);ctx.lineTo(GX+GW,GY-40);ctx.stroke();ctx.setLineDash([]);
      lbl(ctx,'50%',GX+GW+2,GY-36,'#6d28d9',13);
      ctx.strokeStyle='#dc2626';ctx.lineWidth=2.4;ctx.beginPath();
      var acc=0;
      for(i=0;i<shown;i++){
        acc+=tr.arr[i];
        var ratio=acc/(i+1);
        var x2=GX+GW*(i+1)/tr.n, y2=GY-ratio*80;
        if(i===0) ctx.moveTo(x2,y2); else ctx.lineTo(x2,y2);
      }
      if(shown>1) ctx.stroke();
      lbl(ctx,'던진 횟수가 늘어날수록 앞면 비율',GX,GY+20,'#52627a',15);
      lbl(ctx,'앞면 '+hh+' / '+shown,GX,GY-96,'#b45309',17);
    }
    box(ctx,20,354,400,58);
    lbl(ctx,(!tr)?'가능성 1/2 = 50%':(tr.h+' / '+tr.n+' = '+r1(tr.h/tr.n*100)+'%    (50%와의 차 '+r1(Math.abs(tr.h/tr.n*100-50))+'%p)'),
        38,388,'#1f2937',19);
  },
  record:function(S){
    var tr=this._trial;
    return {n:tr.n,h:tr.h,pct:r1(tr.h/tr.n*100),gap:r1(Math.abs(tr.h/tr.n*100-50)),
            exact:(tr.h*2===tr.n)};
  },
  headA:['번호','던진 횟수','앞면','앞면 비율','50%와의 차','정확히 절반?'],
  rowA:function(r,i){
    return [i+1,r.n+'번',r.h+'번','<b>'+r.pct+'%</b>',r.gap+'%p',
            '<span class="'+(r.exact?'ok':'no')+'">'+(r.exact?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],exact=0,sm=0,smN=0,lg=0,lgN=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.exact) exact++;
      if(r.n<=50){ sm+=r.gap; smN++; }
      if(r.n>=100){ lg+=r.gap; lgN++; }
      rows.push([r.n+'번', r.h+'번', '<b>'+r.pct+'%</b>', r.gap+'%p',
                 '<span class="'+(r.exact?'ok':'no')+'">'+(r.exact?'○':'×')+'</span>']);
    }
    var sa=smN?r1(sm/smN):null, la=lgN?r1(lg/lgN):null;
    var stats=[
      {t:'정확히 절반이 나온 횟수',big:exact+' / '+rec.length,
       p:'가능성이 1/2이라고 해서 매번 절반이 나오지는 않았다.'},
      {t:'50번 이하로 던졌을 때 평균 오차',big:(sa===null)?'기록 없음':(sa+'%p'),
       p:smN?(smN+'번의 기록 평균.'):'적게 던진 경우도 기록해 보자.'},
      {t:'100번 이상 던졌을 때 평균 오차',big:(la===null)?'기록 없음':(la+'%p'),
       p:lgN?(lgN+'번의 기록 평균.'):'많이 던진 경우도 기록해 보자.'}
    ];
    var concl;
    if(sa===null||la===null){
      concl='<b>더 해 보자</b> — 적게 던진 경우(10~50번)와 많이 던진 경우(100~200번)를 <b>모두</b> 기록해야 비교할 수 있다.';
    } else if(la<sa){
      concl='<b>정리</b> — 앞면이 나올 가능성은 1/2이지만 <b>매번 정확히 절반이 나오지는 않았다.</b> '
           +'그런데 많이 던질수록 50%에서 벗어난 정도가 줄었다(적게 던질 때 평균 '+sa+'%p → 많이 던질 때 '+la+'%p). '
           +'가능성은 “몇 번 중 몇 번”을 정해 주는 약속이 아니라, 많이 반복했을 때 다가가는 값이다.';
    } else {
      concl='<b>정리</b> — 이번 기록에서는 많이 던진 쪽이 더 가깝지 않았다. 우연히 그럴 수 있으니 기록을 더 모아 보자. '
           +'가능성 1/2은 매번 절반을 보장하지 않는다.';
    }
    return {head:['던진 횟수','앞면','비율','50%와의 차','정확히 절반?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 가능성을 수로 나타내기
# ============================================================
LAB_CHANCE = BASE + r"""
var LAB = {
  cw:440, ch:420, cvTitle:'구슬 주머니판',
  action:'20번 꺼내 보기',
  hint0:'주머니에 넣을 빨간 구슬과 파란 구슬 수를 정해 보자.',
  _trial:null,
  sliders:[
    {id:'r',label:'빨간 구슬',min:0,max:10,value:5,color:'#dc2626',unit:'개'},
    {id:'b',label:'파란 구슬',min:0,max:10,value:5,color:'#2563eb',unit:'개'}
  ],
  chance:function(S){ var t=S.r+S.b; return (t===0)?null:(S.r/t); },
  fracStr:function(S){
    var t=S.r+S.b;
    if(t===0) return '주머니가 비었다';
    if(S.r===0) return '0 (불가능)';
    if(S.b===0) return '1 (확실)';
    var g=gcd(S.r,t);
    return (S.r/g)+'/'+(t/g);
  },
  gen:function(S){
    var t=S.r+S.b, arr=[],i,c=0;
    if(t===0){ this._trial={arr:[],c:0,n:0}; return; }
    for(i=0;i<20;i++){ var pick=(Math.random()*t<S.r)?1:0; arr.push(pick); c+=pick; }
    this._trial={arr:arr,c:c,n:20};
  },
  readout:function(S,ran){
    var p=this.chance(S);
    return [{k:'빨강이 나올 가능성',v:this.fracStr(S)},
            {k:'20번 중 빨강',v:(ran&&this._trial)?(this._trial.c+'번'):'꺼내 보자'}];
  },
  doneMsg:function(S){
    var tr=this._trial;
    if(!tr||tr.n===0) return '주머니가 비어 있어 꺼낼 수 없다. 구슬을 넣어 보자.';
    var p=this.chance(S);
    if(p===0) return '20번 모두 빨강이 나오지 않았다. 가능성이 0이면 절대 일어나지 않는다. 기록해 보자.';
    if(p===1) return '20번 모두 빨강이었다. 가능성이 1이면 반드시 일어난다. 기록해 보자.';
    return '20번 중 빨강이 '+tr.c+'번 나왔다. 가능성 '+this.fracStr(S)+'과 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    if(t===null){ this._trial=null; }
    else if(!this._trial){ this.gen(S); }
    var tr=this._trial, i, tot=S.r+S.b;
    ctx.strokeStyle='#94a3b8';ctx.lineWidth=3;
    ctx.beginPath();ctx.moveTo(60,80);ctx.quadraticCurveTo(40,190,150,196);
    ctx.quadraticCurveTo(260,190,240,80);ctx.stroke();
    for(i=0;i<tot;i++){
      var x=76+(i%5)*32, y=110+Math.floor(i/5)*30;
      ctx.beginPath();ctx.arc(x,y,12,0,Math.PI*2);
      ctx.fillStyle=(i<S.r)?'#ef4444':'#3b82f6';ctx.fill();
      ctx.strokeStyle='#1f2937';ctx.lineWidth=1.6;ctx.stroke();
    }
    lbl(ctx,'주머니 (빨강 '+S.r+' · 파랑 '+S.b+')',60,64,'#1d4ed8',18);
    lbl(ctx,'꺼낸 결과',288,64,'#334155',17);
    if(tr&&tr.n>0){
      var shown=Math.ceil(Math.min(1,t)*20);
      for(i=0;i<shown;i++){
        var cx=298+(i%4)*30, cy=90+Math.floor(i/4)*30;
        ctx.beginPath();ctx.arc(cx,cy,11,0,Math.PI*2);
        ctx.fillStyle=tr.arr[i]?'#ef4444':'#3b82f6';ctx.fill();
        ctx.strokeStyle='#1f2937';ctx.lineWidth=1.4;ctx.stroke();
      }
    } else {
      lbl(ctx,'아직 꺼내지 않았다',288,96,'#94a3b8',15);
    }
    var BX=40,BW=360,BY=250;
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(BX,BY);ctx.lineTo(BX+BW,BY);ctx.stroke();
    var labels=['0\n불가능','1/2\n반반','1\n확실'];
    for(i=0;i<3;i++){
      var x2=BX+BW*i/2;
      ctx.beginPath();ctx.moveTo(x2,BY-8);ctx.lineTo(x2,BY+8);
      ctx.strokeStyle='#475569';ctx.lineWidth=2;ctx.stroke();
      lbl(ctx,['0','1/2','1'][i],x2,BY+26,'#334155',15,'center');
      lbl(ctx,['불가능','반반','확실'][i],x2,BY+44,'#94a3b8',13,'center');
    }
    var p=this.chance(S);
    if(p!==null){
      ctx.beginPath();ctx.arc(BX+BW*p,BY,9,0,Math.PI*2);
      ctx.fillStyle='#7c3aed';ctx.fill();
      ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
    }
    box(ctx,20,304,400,102);
    lbl(ctx,'가능성 : '+this.fracStr(S),38,336,'#6d28d9',20);
    if(tr&&tr.n>0&&t!==null){
      lbl(ctx,'20번 중 빨강 '+tr.c+'번  ('+r1(tr.c/20*100)+'%)',38,368,'#1f2937',19);
      lbl(ctx,(p===0||p===1)?'가능성이 0 또는 1이면 결과가 확실하다':'가능성이 0과 1 사이면 결과는 그때그때 달라진다',
          38,396,(p===0||p===1)?'#15803d':'#b45309',17);
    } else {
      lbl(ctx,'20번 꺼내면 어떤 결과가 나올까?',38,368,'#52627a',18);
    }
  },
  record:function(S){
    var tr=this._trial, p=this.chance(S);
    var c=(tr&&tr.n>0)?tr.c:0;
    return {r:S.r,b:S.b,tot:S.r+S.b,pstr:this.fracStr(S),p:(p===null)?-1:r2(p),
            c:c,pct:r1(c/20*100),n:(tr&&tr.n>0)?20:0,
            certain:(p===0||p===1)};
  },
  headA:['번호','주머니','가능성','가능성(소수)','20번 중 빨강','비율','확실한 경우?'],
  rowA:function(r,i){
    if(r.n===0) return [i+1,'빈 주머니','-','-','-','-','-'];
    return [i+1,'빨강'+r.r+'·파랑'+r.b,'<b>'+r.pstr+'</b>',r.p,r.c+'번',r.pct+'%',
            '<span class="'+(r.certain?'ok':'no')+'">'+(r.certain?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],certain=0,certainOk=0,mid=0,midExact=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.n===0){ rows.push(['빈 주머니','-','-','-','-']); continue; }
      var predicted=r.p*20;
      var ok=(Math.abs(r.c-predicted)<0.001);
      if(r.certain){ certain++; if(ok) certainOk++; }
      else { mid++; if(ok) midExact++; }
      rows.push(['빨강'+r.r+'·파랑'+r.b, r.pstr, r2(predicted)+'번', r.c+'번',
                 '<span class="'+(ok?'ok':'no')+'">'+(ok?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'가능성이 0 또는 1이었던 기록',big:certain+'개',
       p:certain?('그중 예상과 정확히 같았던 것 '+certainOk+'개.'):'한 색만 넣어 가능성 0과 1도 만들어 보자.'},
      {t:'가능성이 0과 1 사이였던 기록',big:mid+'개',
       p:mid?('그중 예상 횟수와 정확히 같았던 것 '+midExact+'개.'):'두 색을 섞어서도 해 보자.'},
      {t:'전체 기록',big:rec.length+'개',p:'가능성은 0에서 1 사이의 수로 나타낸다.'}
    ];
    var concl;
    if(certain===0||mid===0){
      concl='<b>더 해 보자</b> — 가능성이 <b>0 또는 1인 경우</b>와 <b>그 사이인 경우</b>를 모두 기록해야 차이를 볼 수 있다.';
    } else if(certainOk===certain){
      concl='<b>정리</b> — 가능성이 <b>0이면 한 번도 일어나지 않았고 1이면 20번 모두 일어났다.</b> 결과가 확실하다. '
           +'하지만 가능성이 0과 1 사이일 때는 예상 횟수와 딱 맞은 경우가 '+mid+'번 중 '+midExact+'번뿐이었다. '
           +'가능성은 “반드시 이만큼 나온다”가 아니라 <b>일어날 정도를 0과 1 사이의 수로 나타낸 것</b>이다.';
    } else {
      concl='<b>확인 필요</b> — 가능성이 0 또는 1인데 결과가 다른 기록이 있다. 값을 다시 확인해 보자.';
    }
    return {head:['주머니','가능성','예상 횟수','실제 횟수','정확히 같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("elem56_mean_leveling_lab.html",
     "평균 실험실 — 평균은 가운데 값일까?",
     "평균 실험실 — 평균은 가운데 값일까?",
     "네 사람의 자료를 평평하게 고르며 평균을 구하고, 가운데 값과 어떻게 다른지 기록한다.",
     LAB_MEAN),
    ("elem56_combined_mean_lab.html",
     "전체 평균 실험실 — 두 평균을 더해 2로 나누면 될까?",
     "전체 평균 실험실 — 두 평균을 더해 2로 나누면 될까?",
     "인원이 다른 두 모둠을 합쳐 전체 평균을 구하고, 두 평균의 평균과 비교해 기록한다.",
     LAB_TOTMEAN),
    ("elem56_pie_chart_lab.html",
     "원그래프 실험실 — 백분율의 합은 항상 100%일까?",
     "원그래프 실험실 — 백분율의 합은 항상 100%일까?",
     "항목별 학생 수로 백분율과 중심각을 구해 원그래프·띠그래프를 그리고, 합이 얼마가 되는지 기록한다.",
     LAB_PIE),
    ("elem56_coin_toss_lab.html",
     "동전 던지기 실험실 — 가능성이 1/2이면 절반이 나올까?",
     "동전 던지기 실험실 — 가능성이 1/2이면 절반이 나올까?",
     "던지는 횟수를 바꿔 가며 실제로 던지고, 앞면 비율이 50%에서 얼마나 벗어나는지 기록한다.",
     LAB_COIN),
    ("elem56_chance_number_lab.html",
     "구슬 주머니 실험실 — 가능성을 수로 나타내면?",
     "구슬 주머니 실험실 — 가능성을 수로 나타내면?",
     "주머니 속 구슬 구성을 바꿔 가능성을 0~1의 수로 나타내고, 20번 꺼낸 결과와 비교한다.",
     LAB_CHANCE),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c8_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
