# -*- coding: utf-8 -*-
"""초등 3-4학년군 '자료와 가능성' 실험 4종"""
import os, re, random

OUT = "/mnt/user-data/outputs"
src = open("/home/claude/gen_math_labs.py", encoding="utf-8").read()
TPL = re.search(r'TPL = r"""(.*?)"""\n', src, re.S).group(1)

BASE = r"""
function lbl(ctx,t,x,y,c,sz,al){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
function box(ctx,x,y,w,h){ctx.fillStyle='#f1f6fd';ctx.fillRect(x,y,w,h);ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(x,y,w,h);}
function r1(v){return Math.round(v*10)/10;}
"""

# --- 카드 자료 4묶음 (결정적으로 미리 생성) ---
random.seed(20260913)
SETS = []
for s in range(4):
    cards = [[random.randint(0, 2), random.randint(0, 2), random.randint(0, 1)] for _ in range(16)]
    SETS.append(cards)
SETS_JS = "var SETS=" + str(SETS).replace(" ", "") + ";"

# ============================================================
# 1. 분류하고 표 만들기
# ============================================================
LAB_SORT = BASE + SETS_JS + r"""
var SHAPES=['동그라미','세모','네모'], COLORS=['빨강','파랑','노랑'], SIZES=['큰 것','작은 것'];
var CCOL=['#ef4444','#3b82f6','#eab308'];
var CRIT=['모양','색깔','크기'];
function names(c){ return c===0?SHAPES:(c===1?COLORS:SIZES); }
function counts(set,crit){
  var arr=SETS[set], n=names(crit), out=[],i;
  for(i=0;i<n.length;i++) out.push(0);
  for(i=0;i<arr.length;i++){ out[arr[i][crit]]++; }
  return out;
}
function drawCard(ctx,card,x,y,sz){
  var col=CCOL[card[1]], s=sz*(card[2]===0?1:0.66);
  ctx.fillStyle=col;ctx.strokeStyle='#334155';ctx.lineWidth=2;
  if(card[0]===0){ ctx.beginPath();ctx.arc(x,y,s/2,0,Math.PI*2);ctx.fill();ctx.stroke(); }
  else if(card[0]===1){ ctx.beginPath();ctx.moveTo(x,y-s/2);ctx.lineTo(x+s/2,y+s/2);ctx.lineTo(x-s/2,y+s/2);ctx.closePath();ctx.fill();ctx.stroke(); }
  else { ctx.fillRect(x-s/2,y-s/2,s,s);ctx.strokeRect(x-s/2,y-s/2,s,s); }
}

var LAB = {
  cw:440, ch:430, cvTitle:'자료 분류판',
  action:'기준에 따라 나누어 세기',
  hint0:'자료 묶음과 분류 기준을 고른 뒤 나누어 세어 보자.',
  sliders:[
    {id:'set',label:'자료 묶음',min:0,max:3,value:0,color:'#2563eb',fmt:function(v){return (v+1)+'번 묶음';}},
    {id:'crit',label:'분류 기준',min:0,max:2,value:0,color:'#16a34a',fmt:function(v){return CRIT[v];}}
  ],
  readout:function(S,ran){
    var c=counts(S.set,S.crit), s=0,i;
    for(i=0;i<c.length;i++) s+=c[i];
    return [{k:'기준',v:CRIT[S.crit]+'(으)로 분류'},{k:'합계',v:ran?(s+'개'):'세어 보자'}];
  },
  doneMsg:function(S){
    var c=counts(S.set,S.crit), n=names(S.crit), t=[],i,s=0;
    for(i=0;i<c.length;i++){ t.push(n[i]+' '+c[i]); s+=c[i]; }
    return t.join(', ')+' — 합계 '+s+'개. 기준을 바꿔 다시 세어 보자.';
  },
  draw:function(ctx,S,t,ran){
    var arr=SETS[S.set], n=names(S.crit), c=counts(S.set,S.crit), i;
    var move=(t===null)?0:Math.min(1,t/0.7);
    var slot=[0,0,0];
    for(i=0;i<16;i++){
      var hx=40+(i%8)*48, hy=76+Math.floor(i/8)*46;
      var g=arr[i][S.crit];
      var col=g, idx=0, j;
      for(j=0;j<i;j++){ if(arr[j][S.crit]===g) idx++; }
      var gw=440/n.length;
      var tx=gw*g+gw/2-((n.length===2)?36:26)+(idx%3)*30;
      var ty=250+Math.floor(idx/3)*34;
      drawCard(ctx,arr[i],hx+(tx-hx)*move,hy+(ty-hy)*move,30);
    }
    lbl(ctx,(S.set+1)+'번 묶음 — 카드 16장',24,40,'#1d4ed8',19);
    if(move>0.4){
      for(i=0;i<n.length;i++){
        var gw2=440/n.length;
        ctx.strokeStyle='#cbd5e1';ctx.setLineDash([5,5]);ctx.lineWidth=1.6;
        ctx.beginPath();ctx.moveTo(gw2*i,214);ctx.lineTo(gw2*i,340);ctx.stroke();ctx.setLineDash([]);
        lbl(ctx,n[i]+' '+((t!==null&&t>=1)?c[i]+'개':''),gw2*i+gw2/2,232,'#334155',17,'center');
      }
    }
    box(ctx,20,352,400,64);
    var s=0; for(i=0;i<c.length;i++) s+=c[i];
    var txt=[]; for(i=0;i<c.length;i++) txt.push(n[i]+' '+c[i]);
    lbl(ctx,(t===null)?'아직 나누지 않았다':txt.join('   '),38,382,'#1f2937',19);
    lbl(ctx,(t===null)?('기준 : '+CRIT[S.crit]):('합계 : '+s+'개 (처음 카드 16장)'),38,408,'#52627a',18);
  },
  record:function(S){
    var c=counts(S.set,S.crit), n=names(S.crit), s=0,i,t=[];
    for(i=0;i<c.length;i++){ s+=c[i]; t.push(n[i]+' '+c[i]); }
    return {set:S.set,crit:S.crit,critName:CRIT[S.crit],detail:t.join(', '),sum:s,total:16,
            groups:c.length};
  },
  headA:['번호','자료 묶음','기준','나눈 칸 수','칸별 개수','합계','처음 카드 수'],
  rowA:function(r,i){
    return [i+1,(r.set+1)+'번',r.critName,r.groups+'칸',r.detail,'<b>'+r.sum+'</b>',r.total];
  },
  analyze:function(rec){
    var rows=[],ok=0,map={},pairs=0,agree=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i], good=(r.sum===r.total);
      if(good) ok++;
      var k='s'+r.set, note='첫 기록';
      if(map[k]!==undefined){
        pairs++;
        var same=(map[k]===r.sum);
        if(same) agree++;
        note='<span class="'+(same?'ok':'no')+'">'+(same?'합계 같음':'합계 다름')+'</span>';
      } else { map[k]=r.sum; }
      rows.push([(r.set+1)+'번 묶음, '+r.critName, r.groups+'칸', r.detail, '<b>'+r.sum+'</b>',
                 '<span class="'+(good?'ok':'no')+'">'+(good?'○':'×')+'</span>', note]);
    }
    var stats=[
      {t:'합계 = 처음 카드 수',big:ok+' / '+rec.length,p:'빠뜨리거나 두 번 센 칸이 없는지 확인하는 방법이다.'},
      {t:'같은 묶음을 다른 기준으로',big:pairs+'번',
       p:pairs?'같은 자료를 다른 기준으로 나눠 봤다.':'같은 묶음을 기준만 바꿔 다시 세어 보자.'},
      {t:'그때 합계가 같았던 횟수',big:pairs?(agree+' / '+pairs):'비교 없음',
       p:'기준이 달라도 전체 수는 그대로인지 확인한 결과.'}
    ];
    var concl;
    if(ok!==rec.length){
      concl='<b>확인 필요</b> — 합계가 처음 카드 수와 다른 기록이 있다. 세는 과정을 다시 확인해 보자.';
    } else if(pairs>0 && agree===pairs){
      concl='<b>정리</b> — 모양으로 나누든 색으로 나누든, 칸의 수는 달라져도 <b>합계는 언제나 16개</b>였다. '
           +'분류는 자료를 보기 좋게 나눌 뿐 자료를 늘리거나 줄이지 않는다. 그래서 표를 만들면 <b>합계로 셈이 맞는지 검사</b>할 수 있다.';
    } else {
      concl='<b>정리</b> — 어떤 기준으로 나눠도 합계는 처음 카드 수와 같았다. 같은 묶음을 다른 기준으로도 세어 보면 더 확실해진다.';
    }
    return {head:['묶음과 기준','칸 수','칸별 개수','합계','16인가?','같은 묶음끼리'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 그림그래프의 단위
# ============================================================
LAB_PICTO = BASE + r"""
var LAB = {
  cw:440, ch:420, cvTitle:'그림그래프판',
  action:'그림으로 나타내기',
  hint0:'나타낼 값과 큰 그림 하나의 크기를 정해 보자.',
  sliders:[
    {id:'v',label:'나타낼 값',min:0,max:300,step:10,value:230,color:'#2563eb',unit:'개'},
    {id:'u',label:'큰 그림 하나의 크기',min:0,max:1,value:1,color:'#16a34a',
     fmt:function(x){return x===1?'100개':'10개';}}
  ],
  calc:function(S){
    var unit=(S.u===1)?100:10, small=unit/10;
    var big=Math.floor(S.v/unit), rest=S.v-big*unit, sm=Math.round(rest/small);
    return {unit:unit,small:small,big:big,sm:sm,read:big*unit+sm*small,total:big+sm};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'그림 개수',v:ran?(c.big+'개 + '+c.sm+'개 = '+c.total+'개'):'그려 보자'},
            {k:'그림으로 읽은 값',v:ran?(c.read+'개'):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '큰 그림 '+c.big+'개, 작은 그림 '+c.sm+'개로 모두 '+c.total+'개를 그렸다. 읽은 값은 '+c.read+'개다. 큰 그림 크기를 바꿔 다시 그려 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var shown=(t===null)?0:Math.ceil(t*c.total);
    if(t!==null&&t>=1) shown=c.total;
    lbl(ctx,'큰 그림 ● = '+c.unit+'개,  작은 그림 ○ = '+c.small+'개',24,38,'#1d4ed8',18);
    var x0=36,y0=80;
    for(i=0;i<c.big;i++){
      var bx=x0+(i%10)*38, by=y0+Math.floor(i/10)*40;
      var on=(i<shown);
      ctx.beginPath();ctx.arc(bx+14,by+14,15,0,Math.PI*2);
      ctx.fillStyle=on?'#2563eb':'#e8eef7';ctx.fill();
      ctx.strokeStyle=on?'#1d4ed8':'#d5dde8';ctx.lineWidth=2;ctx.stroke();
    }
    var rows=Math.ceil(c.big/10);
    var y1=y0+rows*40+16;
    for(i=0;i<c.sm;i++){
      var sx=x0+(i%10)*30, sy=y1+Math.floor(i/10)*30;
      var on2=((c.big+i)<shown);
      ctx.beginPath();ctx.arc(sx+9,sy+9,8,0,Math.PI*2);
      ctx.fillStyle=on2?'#93c5fd':'#f0f4f9';ctx.fill();
      ctx.strokeStyle=on2?'#2563eb':'#d5dde8';ctx.lineWidth=2;ctx.stroke();
    }
    box(ctx,20,330,400,80);
    lbl(ctx,(t===null)?('나타낼 값 : '+S.v+'개'):('그림 '+c.total+'개 → '+c.big+'×'+c.unit+' + '+c.sm+'×'+c.small+' = '+c.read+'개'),
        38,362,'#1f2937',19);
    lbl(ctx,(t===null)?'그림은 몇 개가 필요할까?':('원래 값 '+S.v+'개와 '+((c.read===S.v)?'같다':'다르다')),
        38,392,(c.read===S.v)?'#15803d':'#b91c1c',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {v:S.v,unit:c.unit,big:c.big,sm:c.sm,total:c.total,read:c.read};
  },
  headA:['번호','나타낸 값','큰 그림 크기','큰 그림','작은 그림','그림 총 개수','읽은 값'],
  rowA:function(r,i){
    return [i+1,r.v+'개',r.unit+'개',r.big,r.sm,'<b>'+r.total+'개</b>',r.read+'개'];
  },
  analyze:function(rec){
    var rows=[],ok=0,pairs=0,diffCnt=0,counter=0,i,j;
    for(i=0;i<rec.length;i++){
      var r=rec[i], good=(r.read===r.v);
      if(good) ok++;
      rows.push([r.v+'개', r.unit+'개', r.big+' + '+r.sm, '<b>'+r.total+'개</b>', r.read+'개',
                 '<span class="'+(good?'ok':'no')+'">'+(good?'○':'×')+'</span>']);
    }
    for(i=0;i<rec.length;i++){
      for(j=i+1;j<rec.length;j++){
        if(rec[i].v===rec[j].v && rec[i].unit!==rec[j].unit){
          pairs++;
          if(rec[i].total!==rec[j].total) diffCnt++;
        }
        if((rec[i].total>rec[j].total && rec[i].v<rec[j].v)||(rec[j].total>rec[i].total && rec[j].v<rec[i].v)) counter++;
      }
    }
    var stats=[
      {t:'그림으로 읽은 값 = 원래 값',big:ok+' / '+rec.length,p:'그림을 값으로 되돌려 읽어 본 결과.'},
      {t:'같은 값을 다른 단위로 그린 짝',big:pairs+'쌍',
       p:pairs?('그중 그림 개수가 달랐던 경우 '+diffCnt+'쌍.'):'같은 값을 큰 그림 크기만 바꿔 그려 보자.'},
      {t:'그림은 많은데 값은 작았던 짝',big:counter+'쌍',
       p:counter?'그림 개수만 보고 크기를 비교하면 틀린다.':'단위가 다른 두 값을 비교해 보자.'}
    ];
    var concl;
    if(ok!==rec.length){
      concl='<b>확인 필요</b> — 그림으로 읽은 값이 원래 값과 다른 기록이 있다.';
    } else if(counter>0){
      concl='<b>정리</b> — 같은 값이라도 큰 그림 하나의 크기를 바꾸면 그림 개수가 달라졌고, '
           +'<b>그림이 더 많은데 값은 더 작은 경우도 '+counter+'번</b> 나왔다. 그림그래프는 개수가 아니라 <b>그림 하나가 얼마인지</b>를 먼저 봐야 한다.';
    } else {
      concl='<b>정리</b> — 그림으로 읽은 값은 언제나 원래 값과 같았다. 이번엔 단위가 다른 두 값을 비교해서, 그림이 더 많은데 값은 더 작은 경우를 찾아보자.';
    }
    return {head:['값','큰 그림 크기','큰+작은','그림 총 개수','읽은 값','값이 맞나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 막대그래프의 눈금
# ============================================================
LAB_BAR = BASE + r"""
var DATA=[12,15,9,18], NAMES=['1반','2반','3반','4반'];
var LAB = {
  cw:440, ch:430, cvTitle:'막대그래프판',
  action:'막대 그리기',
  hint0:'세로 눈금 한 칸을 몇 권으로 할지 정하고 그려 보자. 자료는 항상 같다.',
  sliders:[
    {id:'s',label:'눈금 한 칸의 크기',min:2,max:10,value:2,color:'#2563eb',unit:'권'},
    {id:'pick',label:'비교할 반',min:0,max:3,value:0,color:'#16a34a',
     fmt:function(v){return NAMES[v]+' 와 4반';}}
  ],
  readout:function(S,ran){
    return [{k:'눈금 한 칸',v:S.s+'권'},
            {k:NAMES[S.pick]+' 막대 칸 수',v:ran?(r1(DATA[S.pick]/S.s)+'칸'):'그려 보자'}];
  },
  doneMsg:function(S){
    return '눈금 한 칸이 '+S.s+'권일 때 '+NAMES[S.pick]+'은 '+r1(DATA[S.pick]/S.s)+'칸, 4반은 '+r1(DATA[3]/S.s)+'칸이다. 칸 수를 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var CELL=24, BX=64, BY=330, i;
    var cells=Math.ceil(18/S.s);
    var grow=(t===null)?0:Math.min(1,t);
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(BX,BY);ctx.lineTo(400,BY);ctx.moveTo(BX,BY);ctx.lineTo(BX,BY-cells*CELL-14);ctx.stroke();
    for(i=0;i<=cells;i++){
      var y=BY-i*CELL;
      ctx.strokeStyle='#e2e8f0';ctx.lineWidth=1.4;
      ctx.beginPath();ctx.moveTo(BX,y);ctx.lineTo(400,y);ctx.stroke();
      ctx.fillStyle='#475569';ctx.font='13px sans-serif';ctx.textAlign='right';
      ctx.fillText(i*S.s,BX-6,y+4);
    }
    ctx.textAlign='center';
    for(i=0;i<4;i++){
      var w=52, x=BX+22+i*80;
      var h=DATA[i]/S.s*CELL*grow;
      ctx.fillStyle=(i===3||i===S.pick)?'#2563eb':'#bfdbfe';
      ctx.fillRect(x,BY-h,w,h);
      ctx.strokeStyle='#1d4ed8';ctx.lineWidth=2;ctx.strokeRect(x,BY-h,w,h);
      ctx.fillStyle='#334155';ctx.font='bold 15px sans-serif';
      ctx.fillText(NAMES[i],x+w/2,BY+20);
      if(grow>=1){ ctx.fillStyle='#1f2937';ctx.font='bold 14px sans-serif';ctx.fillText(DATA[i],x+w/2,BY-h-8); }
    }
    ctx.textAlign='left';
    lbl(ctx,'반별 읽은 책 수 (눈금 한 칸 = '+S.s+'권)',24,32,'#1d4ed8',18);
    box(ctx,20,352,400,64);
    var d=r1(DATA[3]/S.s-DATA[S.pick]/S.s);
    lbl(ctx,(t===null)?'막대 길이는 어떻게 될까?':('칸 수 차이 : '+d+'칸'),38,382,'#1f2937',20);
    lbl(ctx,'실제 권 수 차이 : '+(DATA[3]-DATA[S.pick])+'권',38,408,'#52627a',18);
  },
  record:function(S){
    var a=DATA[S.pick], b=DATA[3];
    return {s:S.s,pick:S.pick,name:NAMES[S.pick],va:a,vb:b,
            ca:r1(a/S.s),cb:r1(b/S.s),cd:r1(b/S.s-a/S.s),vd:b-a,
            px:r1((b-a)/S.s*24)};
  },
  headA:['번호','눈금 한 칸','비교','칸 수','4반 칸 수','칸 수 차이','실제 권 수 차이','막대 높이 차(px)'],
  rowA:function(r,i){
    return [i+1,r.s+'권',r.name+' vs 4반',r.ca,r.cb,'<b>'+r.cd+'칸</b>',r.vd+'권',r.px];
  },
  analyze:function(rec){
    var rows=[],ok=0,mn=9999,mx=0,ss={};
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      var good=(Math.abs(r.cd*r.s-r.vd)<0.05);
      if(good) ok++;
      if(r.px<mn) mn=r.px;
      if(r.px>mx) mx=r.px;
      ss[r.s]=true;
      rows.push([r.s+'권', r.name+' vs 4반', r.cd+'칸', r.vd+'권', r.px+'px',
                 '<span class="'+(good?'ok':'no')+'">'+(good?'○':'×')+'</span>']);
    }
    var sn=0; for(var k in ss) sn++;
    var stats=[
      {t:'칸 수 × 눈금 한 칸 = 실제 차이',big:ok+' / '+rec.length,
       p:'칸 수만으로는 값을 알 수 없고, 눈금 크기를 곱해야 한다.'},
      {t:'막대 높이 차이의 범위',big:mn+'px ~ '+mx+'px',
       p:'같은 자료인데 눈금만 바꿔서 이만큼 달라 보였다.'},
      {t:'시험한 눈금 크기',big:sn+'가지',
       p:sn>1?'눈금을 바꿔도 실제 권 수 차이는 그대로였다.':'눈금 크기를 바꿔 더 기록해 보자.'}
    ];
    var concl;
    if(sn<2){
      concl='<b>더 해 보자</b> — 아직 한 가지 눈금만 써 봤다. 눈금 한 칸을 2권과 10권으로 바꿔 같은 자료를 그려 보자.';
    } else if(ok===rec.length){
      concl='<b>정리</b> — 자료는 한 번도 바뀌지 않았는데 막대 높이 차이는 '+mn+'px에서 '+mx+'px까지 달라졌다. '
           +'<b>막대가 길다고 값이 큰 것이 아니다.</b> 그래프를 볼 때는 눈금 한 칸이 얼마인지부터 확인해야 한다. '
           +'칸 수 × 눈금 한 칸 = 실제 값이다.';
    } else {
      concl='<b>확인 필요</b> — 칸 수와 실제 차이가 맞지 않는 기록이 있다.';
    }
    return {head:['눈금 한 칸','비교','칸 수 차이','실제 차이','높이 차(px)','칸수×눈금=실제?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 꺾은선그래프와 물결선
# ============================================================
LAB_LINE = BASE + r"""
var TEMP=[21.2,21.5,21.8,22.0,21.7], DAYS=['월','화','수','목','금'];
var TOP=22.4;
var LAB = {
  cw:440, ch:430, cvTitle:'꺾은선그래프판',
  action:'그래프 그리기',
  hint0:'세로눈금을 0부터 시작할지, 21도부터 시작할지 정해 보자. 기온 자료는 항상 같다.',
  sliders:[
    {id:'st',label:'세로눈금 시작 온도',min:0,max:21,value:0,color:'#2563eb',unit:'도'}
  ],
  readout:function(S,ran){
    var span=TOP-S.st;
    return [{k:'세로눈금 범위',v:S.st+'도 ~ '+TOP+'도'},
            {k:'선의 오르내림',v:ran?(r1(0.8/span*240)+'px'):'그려 보자'}];
  },
  doneMsg:function(S){
    var span=TOP-S.st;
    return '실제 기온 차는 0.8도인데, 그래프에서는 '+r1(0.8/span*240)+'px 차이로 보인다. 시작 온도를 바꿔 다시 그려 보자.';
  },
  draw:function(ctx,S,t,ran){
    var GX=70, GY=316, GW=320, GH=240, i;
    var span=TOP-S.st;
    function py(v){ return GY-(v-S.st)/span*GH; }
    var grow=(t===null)?0:Math.min(1,t);
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(GX,GY);ctx.lineTo(GX+GW,GY);ctx.moveTo(GX,GY);ctx.lineTo(GX,GY-GH-10);ctx.stroke();
    var ticks=6;
    for(i=0;i<=ticks;i++){
      var v=S.st+span*i/ticks, y=py(v);
      ctx.strokeStyle='#e2e8f0';ctx.lineWidth=1.4;
      ctx.beginPath();ctx.moveTo(GX,y);ctx.lineTo(GX+GW,y);ctx.stroke();
      ctx.fillStyle='#475569';ctx.font='13px sans-serif';ctx.textAlign='right';
      ctx.fillText(r1(v),GX-6,y+4);
    }
    if(S.st>0){
      ctx.strokeStyle='#f97316';ctx.lineWidth=2.5;
      ctx.beginPath();
      for(i=0;i<=10;i++){
        var wx=GX-8+i*3.4, wy=GY-8+((i%2===0)?-4:4);
        if(i===0) ctx.moveTo(wx,wy); else ctx.lineTo(wx,wy);
      }
      ctx.stroke();
      lbl(ctx,'물결선',GX+8,GY-4,'#c2410c',13);
    }
    ctx.textAlign='center';
    for(i=0;i<5;i++){
      var x=GX+40+i*60;
      ctx.fillStyle='#334155';ctx.font='bold 15px sans-serif';
      ctx.fillText(DAYS[i],x,GY+22);
    }
    var n=Math.max(1,Math.ceil(grow*5));
    ctx.strokeStyle='#dc2626';ctx.lineWidth=3;ctx.beginPath();
    for(i=0;i<n;i++){
      var x2=GX+40+i*60, y2=py(TEMP[i]);
      if(i===0) ctx.moveTo(x2,y2); else ctx.lineTo(x2,y2);
    }
    if(grow>0) ctx.stroke();
    for(i=0;i<n;i++){
      var x3=GX+40+i*60, y3=py(TEMP[i]);
      ctx.beginPath();ctx.arc(x3,y3,5,0,Math.PI*2);ctx.fillStyle='#dc2626';ctx.fill();
      if(grow>=1){ ctx.fillStyle='#7f1d1d';ctx.font='bold 13px sans-serif';ctx.fillText(TEMP[i],x3,y3-12); }
    }
    ctx.textAlign='left';
    lbl(ctx,'요일별 낮 기온 (세로눈금 '+S.st+'도부터)',24,32,'#1d4ed8',18);
    box(ctx,20,352,400,64);
    lbl(ctx,(t===null)?'변화가 얼마나 커 보일까?':('그래프에서 오르내린 높이 : '+r1(0.8/span*240)+'px'),38,382,'#1f2937',19);
    lbl(ctx,'실제 기온 차 : 21.2도 ~ 22.0도 = 0.8도',38,408,'#52627a',18);
  },
  record:function(S){
    var span=TOP-S.st;
    return {st:S.st,span:r1(span),real:0.8,px:r1(0.8/span*240),wave:(S.st>0)};
  },
  headA:['번호','세로눈금 시작','눈금 범위','실제 기온 차','그래프에서 높이 차','물결선'],
  rowA:function(r,i){
    return [i+1,r.st+'도',r.span+'도',r.real+'도','<b>'+r.px+'px</b>',r.wave?'있음':'없음'];
  },
  analyze:function(rec){
    var rows=[],mn=99999,mx=0,sameReal=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(Math.abs(r.real-0.8)<0.001) sameReal++;
      if(r.px<mn) mn=r.px;
      if(r.px>mx) mx=r.px;
      rows.push([r.st+'도부터', r.span+'도', r.real+'도', '<b>'+r.px+'px</b>', r.wave?'있음':'없음']);
    }
    var ratio=(mn>0)?r1(mx/mn):0;
    var stats=[
      {t:'실제 기온 차가 그대로였던 횟수',big:sameReal+' / '+rec.length,p:'자료는 한 번도 바뀌지 않았다.'},
      {t:'그래프 높이 차의 범위',big:mn+'px ~ '+mx+'px',p:'세로눈금 시작만 바꿨을 때 보이는 변화의 크기.'},
      {t:'가장 크게 보였을 때 / 가장 작게 보였을 때',big:ratio+'배',
       p:ratio>1?'같은 0.8도가 이만큼 다르게 보였다.':'시작 온도를 0도와 21도로 바꿔 비교해 보자.'}
    ];
    var concl;
    if(ratio<=1){
      concl='<b>더 해 보자</b> — 아직 시작 온도를 한 가지로만 그렸다. 0도부터와 21도부터를 모두 기록해 비교해 보자.';
    } else {
      concl='<b>정리</b> — 기온 자료는 하나도 바뀌지 않았는데, 세로눈금을 어디서 시작하느냐에 따라 변화가 <b>'+ratio+'배</b>까지 다르게 보였다. '
           +'물결선을 쓰면 작은 변화를 자세히 볼 수 있지만, <b>변화가 실제보다 커 보인다</b>는 점을 알고 읽어야 한다. '
           +'그래프를 볼 때는 세로눈금이 0부터 시작하는지 먼저 확인하자.';
    }
    return {head:['시작 온도','눈금 범위','실제 차','높이 차','물결선'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("elem34_sorting_table_lab.html",
     "자료 분류 실험실 — 기준을 바꾸면 자료도 달라질까?",
     "자료 분류 실험실 — 기준을 바꾸면 자료도 달라질까?",
     "같은 카드 묶음을 모양·색·크기로 나누어 세고, 표의 합계가 어떻게 되는지 확인한다.",
     LAB_SORT),
    ("elem34_pictograph_unit_lab.html",
     "그림그래프 실험실 — 그림이 많으면 큰 값일까?",
     "그림그래프 실험실 — 그림이 많으면 큰 값일까?",
     "같은 값을 큰 그림 크기만 바꿔 나타내고, 그림 개수와 실제 값의 관계를 기록한다.",
     LAB_PICTO),
    ("elem34_bar_scale_lab.html",
     "막대그래프 실험실 — 막대가 길면 큰 값일까?",
     "막대그래프 실험실 — 막대가 길면 큰 값일까?",
     "자료는 그대로 두고 세로 눈금 한 칸의 크기만 바꿔 가며 막대 길이와 실제 값을 비교한다.",
     LAB_BAR),
    ("elem34_line_graph_wave_lab.html",
     "꺾은선그래프 실험실 — 물결선을 쓰면 무엇이 달라질까?",
     "꺾은선그래프 실험실 — 물결선을 쓰면 무엇이 달라질까?",
     "같은 기온 자료를 세로눈금 시작만 바꿔 그리고, 변화가 얼마나 다르게 보이는지 기록한다.",
     LAB_LINE),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c4_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
