# -*- coding: utf-8 -*-
"""고등 공통수학2 — 집합과 명제 2종 + 함수 3종"""
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
var CX=220, CY=210, U=22;
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
# 1. 드모르간의 법칙
# ============================================================
LAB_DEM = BASE + r"""
var N=12;
var LAB = {
  cw:440, ch:430, cvTitle:'집합 연산판',
  action:'집합을 나누어 세기',
  hint0:'전체집합은 1부터 12까지. 두 집합의 조건을 정해 보자.',
  sliders:[
    {id:'p',label:'A = ( ? )의 배수',min:2,max:6,value:2,color:'#2563eb',unit:''},
    {id:'q',label:'B = ( ? )의 배수',min:2,max:6,value:3,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var A=[],B=[],i;
    for(i=1;i<=N;i++){ if(i%S.p===0) A.push(i); if(i%S.q===0) B.push(i); }
    function has(arr,x){ return arr.indexOf(x)>=0; }
    var un=[],inter=[],unC=[],cAcB=[],interC=[],cAucB=[];
    for(i=1;i<=N;i++){
      var a=has(A,i), b=has(B,i);
      if(a||b) un.push(i);
      if(a&&b) inter.push(i);
      if(!(a||b)) unC.push(i);
      if(!a&&!b) cAcB.push(i);
      if(!(a&&b)) interC.push(i);
      if(!a||!b) cAucB.push(i);
    }
    return {A:A,B:B,un:un,inter:inter,unC:unC,cAcB:cAcB,interC:interC,cAucB:cAucB};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'(A∪B)의 여집합',v:ran?(c.unC.length+'개'):'세어 보자'},
            {k:'A여 ∩ B여',v:ran?(c.cAcB.length+'개'):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '(A∪B)ᶜ 는 '+c.unC.length+'개, Aᶜ∩Bᶜ 는 '+c.cAcB.length+'개, Aᶜ∪Bᶜ 는 '+c.cAucB.length+'개다. 어느 것이 같은지 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*N);
    var X0=40, CW=32;
    lbl(ctx,'A = '+S.p+'의 배수     B = '+S.q+'의 배수',24,34,'#1d4ed8',17);
    function row(y,label,set,col){
      lbl(ctx,label,24,y+20,'#334155',14);
      for(i=1;i<=N;i++){
        var on=(i<=shown);
        var mem=(set.indexOf(i)>=0);
        var x=X0+100+(i-1)*CW;
        ctx.fillStyle=(on&&mem)?col:'#f1f5f9';
        ctx.fillRect(x,y,CW-3,24);
        ctx.strokeStyle=(on&&mem)?'#334155':'#e2e8f0';ctx.lineWidth=1.2;
        ctx.strokeRect(x,y,CW-3,24);
        if(y===60){
          ctx.fillStyle='#94a3b8';ctx.font='11px sans-serif';ctx.textAlign='center';
          ctx.fillText(i,x+CW/2-1,y-6);
        }
      }
      ctx.textAlign='left';
    }
    row(60,'A',c.A,'#93c5fd');
    row(96,'B',c.B,'#fca5a5');
    row(140,'(A∪B)ᶜ',c.unC,'#86efac');
    row(176,'Aᶜ ∩ Bᶜ',c.cAcB,'#86efac');
    row(220,'(A∩B)ᶜ',c.interC,'#fde68a');
    row(256,'Aᶜ ∪ Bᶜ',c.cAucB,'#fde68a');
    box(ctx,20,296,400,120);
    lbl(ctx,(t===null)?'여집합은 어떻게 될까?':('(A∪B)ᶜ = '+(c.unC.join(', ')||'없음')),38,326,'#15803d',16);
    lbl(ctx,(t===null)?'':('Aᶜ ∩ Bᶜ = '+(c.cAcB.join(', ')||'없음')),38,352,'#15803d',16);
    lbl(ctx,(t===null)?'':('Aᶜ ∪ Bᶜ = '+(c.cAucB.join(', ')||'없음')),38,382,'#b45309',15);
    lbl(ctx,(t===null)?'':'같은 것끼리 짝지어 보자',38,408,'#52627a',14);
  },
  record:function(S){
    var c=this.calc(S);
    function eq(x,y){ return x.length===y.length&&x.join(',')===y.join(','); }
    return {p:S.p,q:S.q,
            unC:c.unC.join(', ')||'없음',
            cAcB:c.cAcB.join(', ')||'없음',
            cAucB:c.cAucB.join(', ')||'없음',
            interC:c.interC.join(', ')||'없음',
            law1:eq(c.unC,c.cAcB),
            law2:eq(c.interC,c.cAucB),
            wrong:eq(c.unC,c.cAucB)};
  },
  headA:['번호','A, B','(A∪B)ᶜ','Aᶜ∩Bᶜ','같나?','(A∩B)ᶜ','Aᶜ∪Bᶜ','같나?','(A∪B)ᶜ = Aᶜ∪Bᶜ?'],
  rowA:function(r,i){
    return [i+1,r.p+'의 배수, '+r.q+'의 배수,',r.unC,r.cAcB,
            '<span class="'+(r.law1?'ok':'no')+'">'+(r.law1?'○':'×')+'</span>',
            r.interC,r.cAucB,
            '<span class="'+(r.law2?'ok':'no')+'">'+(r.law2?'○':'×')+'</span>',
            '<span class="'+(r.wrong?'ok':'no')+'">'+(r.wrong?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],l1=0,l2=0,w=0,same=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.law1) l1++;
      if(r.law2) l2++;
      if(r.wrong){ w++; if(r.p===r.q) same++; }
      rows.push([r.p+', '+r.q, r.unC+'  /  '+r.cAcB,
                 '<span class="'+(r.law1?'ok':'no')+'">'+(r.law1?'○':'×')+'</span>',
                 r.interC+'  /  '+r.cAucB,
                 '<span class="'+(r.law2?'ok':'no')+'">'+(r.law2?'○':'×')+'</span>',
                 '<span class="'+(r.wrong?'ok':'no')+'">'+(r.wrong?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'(A∪B)ᶜ = Aᶜ ∩ Bᶜ',big:l1+' / '+rec.length,p:'합집합의 여집합과 여집합의 교집합을 비교한 결과.'},
      {t:'(A∩B)ᶜ = Aᶜ ∪ Bᶜ',big:l2+' / '+rec.length,p:'교집합의 여집합과 여집합의 합집합을 비교한 결과.'},
      {t:'(A∪B)ᶜ = Aᶜ ∪ Bᶜ 였던 횟수',big:w+' / '+rec.length,
       p:w?('그중 A = B 였던 것 '+same+'개.'):'∪를 그대로 두면 맞지 않는다.'}
    ];
    var concl;
    if(l1===rec.length&&l2===rec.length&&w===same){
      concl='<b>정리</b> — 여집합을 취하면 <b>∪와 ∩이 서로 바뀌었다</b>. '
           +'(A∪B)ᶜ = Aᶜ ∩ Bᶜ, (A∩B)ᶜ = Aᶜ ∪ Bᶜ 가 예외 없이 성립했다. '
           +'“A에도 B에도 속하지 않는다”와 “A에 속하지 않고 또 B에도 속하지 않는다”가 같은 말이기 때문이다. '
           +'기호만 그대로 두고 여집합을 씌우면 틀린다.';
    } else {
      concl='<b>확인 필요</b> — 법칙이 성립하지 않은 기록이 있다.';
    }
    return {head:['A, B','(A∪B)ᶜ / Aᶜ∩Bᶜ','같나?','(A∩B)ᶜ / Aᶜ∪Bᶜ','같나?','∪ 그대로 두면?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 명제의 역·이·대우
# ============================================================
LAB_PROP = BASE + r"""
var N=24;
var LAB = {
  cw:440, ch:430, cvTitle:'명제 판정판',
  action:'모든 수를 확인하기',
  hint0:'1부터 24까지의 자연수 x에 대한 명제를 만들어 보자.',
  sliders:[
    {id:'p',label:'가정 : x는 ( ? )의 배수',min:2,max:8,value:6,color:'#2563eb',unit:''},
    {id:'q',label:'결론 : x는 ( ? )의 배수',min:2,max:8,value:3,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var i,orig=true,conv=true,inv=true,contra=true;
    var co=null,cc=null,ci=null,cn=null;
    for(i=1;i<=N;i++){
      var P=(i%S.p===0), Q=(i%S.q===0);
      if(P&&!Q){ orig=false; if(co===null) co=i; }
      if(Q&&!P){ conv=false; if(cc===null) cc=i; }
      if(!P&&Q){ inv=false; if(ci===null) ci=i; }
      if(!Q&&P){ contra=false; if(cn===null) cn=i; }
    }
    return {orig:orig,conv:conv,inv:inv,contra:contra,co:co,cc:cc,ci:ci,cn:cn};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'원명제',v:ran?(c.orig?'참':'거짓'):'확인해 보자'},
            {k:'대우',v:ran?(c.contra?'참':'거짓'):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '원명제 '+(c.orig?'참':'거짓')+', 역 '+(c.conv?'참':'거짓')+', 이 '+(c.inv?'참':'거짓')+', 대우 '+(c.contra?'참':'거짓')+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*N);
    lbl(ctx,'x가 '+S.p+'의 배수이면 x는 '+S.q+'의 배수이다',24,34,'#1d4ed8',17);
    var X0=32, CW=32;
    for(i=1;i<=N;i++){
      var on=(i<=shown);
      var P=(i%S.p===0), Q=(i%S.q===0);
      var col='#f1f5f9', tc='#94a3b8';
      if(on){
        if(P&&Q){ col='#bbf7d0'; tc='#14532d'; }
        else if(P&&!Q){ col='#fecaca'; tc='#7f1d1d'; }
        else if(!P&&Q){ col='#fde68a'; tc='#7c2d12'; }
        else { col='#e2e8f0'; tc='#64748b'; }
      }
      var x=X0+((i-1)%12)*CW, y=64+Math.floor((i-1)/12)*36;
      ctx.fillStyle=col;ctx.fillRect(x,y,CW-3,30);
      ctx.strokeStyle='#cbd5e1';ctx.lineWidth=1.2;ctx.strokeRect(x,y,CW-3,30);
      ctx.fillStyle=tc;ctx.font='bold 13px sans-serif';ctx.textAlign='center';
      ctx.fillText(i,x+CW/2-1,y+20);
    }
    ctx.textAlign='left';
    lbl(ctx,'초록 = 가정·결론 모두 참    빨강 = 가정 참·결론 거짓(반례)',24,158,'#52627a',13);
    lbl(ctx,'노랑 = 가정 거짓·결론 참    회색 = 둘 다 거짓',24,176,'#52627a',13);
    var items=[['원명제  p → q',c.orig,c.co],['역  q → p',c.conv,c.cc],
               ['이  ~p → ~q',c.inv,c.ci],['대우  ~q → ~p',c.contra,c.cn]];
    for(i=0;i<4;i++){
      var yy=210+i*30;
      var show=(shown>=N);
      lbl(ctx,items[i][0],32,yy,'#334155',16);
      lbl(ctx,show?(items[i][1]?'참':'거짓'):'?',210,yy,show?(items[i][1]?'#15803d':'#b91c1c'):'#cbd5e1',17);
      if(show&&!items[i][1]&&items[i][2]!==null) lbl(ctx,'반례 x = '+items[i][2],262,yy,'#b91c1c',14);
    }
    box(ctx,20,340,400,76);
    lbl(ctx,(t===null)?'원명제와 대우는 어떤 관계일까?':('원명제 '+(c.orig?'참':'거짓')+'  /  대우 '+(c.contra?'참':'거짓')),
        38,372,'#1f2937',18);
    lbl(ctx,(t===null)?'':('역 '+(c.conv?'참':'거짓')+'  /  이 '+(c.inv?'참':'거짓')),38,402,'#52627a',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {p:S.p,q:S.q,orig:c.orig,conv:c.conv,inv:c.inv,contra:c.contra,
            oc:(c.orig===c.contra),ci:(c.conv===c.inv),
            oconv:(c.orig===c.conv)};
  },
  headA:['번호','명제','원명제','역','이','대우','원=대우?','역=이?','원=역?'],
  rowA:function(r,i){
    function tf(v){ return '<span class="'+(v?'ok':'no')+'">'+(v?'참':'거짓')+'</span>'; }
    return [i+1,r.p+'의 배수 → '+r.q+'의 배수',tf(r.orig),tf(r.conv),tf(r.inv),tf(r.contra),
            '<span class="'+(r.oc?'ok':'no')+'">'+(r.oc?'○':'×')+'</span>',
            '<span class="'+(r.ci?'ok':'no')+'">'+(r.ci?'○':'×')+'</span>',
            '<span class="'+(r.oconv?'ok':'no')+'">'+(r.oconv?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],oc=0,ci=0,oconv=0,diff=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.oc) oc++;
      if(r.ci) ci++;
      if(r.oconv) oconv++; else diff++;
      function tf(v){ return '<span class="'+(v?'ok':'no')+'">'+(v?'참':'거짓')+'</span>'; }
      rows.push([r.p+' → '+r.q, tf(r.orig), tf(r.conv), tf(r.inv), tf(r.contra),
                 '<span class="'+(r.oc?'ok':'no')+'">'+(r.oc?'○':'×')+'</span>',
                 '<span class="'+(r.oconv?'ok':'no')+'">'+(r.oconv?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'원명제와 대우의 참·거짓이 같았던 횟수',big:oc+' / '+rec.length,
       p:'1부터 24까지 모두 확인해 판정한 결과.'},
      {t:'역과 이가 같았던 횟수',big:ci+' / '+rec.length,
       p:'역과 이도 서로 대우 관계다.'},
      {t:'원명제와 역이 달랐던 횟수',big:diff+'개',
       p:diff?'참인 명제의 역이 거짓인 경우가 있었다.':'6의 배수 → 3의 배수 처럼 역이 거짓인 예를 만들어 보자.'}
    ];
    var concl;
    if(diff===0){
      concl='<b>더 해 보자</b> — 아직 원명제와 역의 참·거짓이 갈린 기록이 없다. '
           +'“6의 배수이면 3의 배수”처럼 <b>참인데 역은 거짓</b>인 명제를 만들어 보자.';
    } else if(oc===rec.length&&ci===rec.length){
      concl='<b>정리</b> — 원명제와 <b>대우의 참·거짓은 언제나 같았고</b>, 역과 이도 서로 같았다. '
           +'반면 원명제와 역은 '+diff+'번 갈렸다. 참인 명제의 역이 참이라는 보장은 없다. '
           +'대우가 원명제와 같다는 사실 덕분에 <b>증명하기 어려운 명제를 대우로 바꿔 증명</b>할 수 있다.';
    } else {
      concl='<b>확인 필요</b> — 원명제와 대우의 판정이 어긋난 기록이 있다.';
    }
    return {head:['명제','원명제','역','이','대우','원=대우?','원=역?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 함수의 판정
# ============================================================
LAB_FUNC = BASE + r"""
var KINDS=['y = x²','x = y²','x² + y² = 16','y = 2x − 1','y = |x|'];
function ys(kind,x){
  if(kind===0) return [x*x];
  if(kind===1){ if(x<0) return []; if(x===0) return [0]; return [Math.sqrt(x),-Math.sqrt(x)]; }
  if(kind===2){ var v=16-x*x; if(v<0) return []; if(Math.abs(v)<1e-12) return [0]; return [Math.sqrt(v),-Math.sqrt(v)]; }
  if(kind===3) return [2*x-1];
  return [Math.abs(x)];
}
var LAB = {
  cw:440, ch:430, cvTitle:'수직선 판정판',
  action:'세로선으로 훑어보기',
  hint0:'그래프를 고르고, 세로선을 옮기며 만나는 점의 개수를 세어 보자.',
  sliders:[
    {id:'kind',label:'그래프',min:0,max:4,value:1,color:'#2563eb',fmt:function(v){return KINDS[v];}},
    {id:'xx',label:'세로선의 위치 (÷2)',min:-10,max:10,value:4,color:'#dc2626',
     fmt:function(v){return (v/2).toFixed(1);}}
  ],
  calc:function(S){
    var x=S.xx/2;
    var cur=ys(S.kind,x).length;
    var maxc=0,i,vals={},oneToOne=true;
    for(i=-100;i<=100;i++){
      var xv=i/10;
      var arr=ys(S.kind,xv);
      if(arr.length>maxc) maxc=arr.length;
      for(var j=0;j<arr.length;j++){
        var key=Math.round(arr[j]*100)/100;
        if(vals[key]) oneToOne=false;
        vals[key]=true;
      }
    }
    return {x:x,cur:cur,maxc:maxc,isFn:(maxc<=1),oneToOne:(maxc<=1&&oneToOne)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'x = '+c.x+' 에서 만나는 점',v:ran?(c.cur+'개'):'훑어 보자'},
            {k:'함수인가',v:ran?(c.isFn?'예':'아니오'):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '어떤 세로선과도 최대 '+c.maxc+'개에서 만났다. 따라서 '+(c.isFn?'함수다':'함수가 아니다')
      +(c.isFn?(c.oneToOne?' (일대일 함수)':' (일대일은 아니다)'):'')+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,8,7);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;
    if(S.kind===2){
      ctx.beginPath();ctx.arc(CX,CY,4*U,0,Math.PI*2);ctx.stroke();
    } else {
      ctx.beginPath();
      var st=false;
      for(i=-80;i<=80;i++){
        var x=i/10, arr=ys(S.kind,x);
        if(arr.length!==1){ st=false; continue; }
        var y=arr[0];
        if(y<-7||y>7){ st=false; continue; }
        if(!st){ ctx.moveTo(CX+x*U,CY-y*U); st=true; } else ctx.lineTo(CX+x*U,CY-y*U);
      }
      ctx.stroke();
      if(S.kind===1){
        ['up','dn'].forEach(function(dir){
          ctx.beginPath();var s2=false;
          for(i=0;i<=80;i++){
            var x2=i/10, y2=(dir==='up')?Math.sqrt(x2):-Math.sqrt(x2);
            if(y2<-7||y2>7){ s2=false; continue; }
            if(!s2){ ctx.moveTo(CX+x2*U,CY-y2*U); s2=true; } else ctx.lineTo(CX+x2*U,CY-y2*U);
          }
          ctx.stroke();
        });
      }
    }
    var sweep=(t===null)?null:(-5+10*Math.min(1,t));
    var lines=(sweep===null)?[c.x]:[sweep,c.x];
    lines.forEach(function(xv,idx){
      ctx.strokeStyle=(idx===0&&sweep!==null)?'#f59e0b':'#dc2626';
      ctx.lineWidth=(idx===0&&sweep!==null)?2:3;
      ctx.setLineDash([5,4]);
      ctx.beginPath();ctx.moveTo(CX+xv*U,CY-7*U);ctx.lineTo(CX+xv*U,CY+7*U);ctx.stroke();
      ctx.setLineDash([]);
      var arr=ys(S.kind,xv);
      for(var j=0;j<arr.length;j++){
        if(Math.abs(arr[j])>7) continue;
        ctx.beginPath();ctx.arc(CX+xv*U,CY-arr[j]*U,6,0,Math.PI*2);
        ctx.fillStyle='#7c3aed';ctx.fill();
      }
    });
    lbl(ctx,KINDS[S.kind],24,32,'#1d4ed8',18);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'세로선과 몇 개에서 만날까?':('x = '+c.x+' 에서 '+c.cur+'개    전체 최대 '+c.maxc+'개'),38,376,'#1f2937',18);
    lbl(ctx,(t===null)?'':(c.isFn?('함수다'+(c.oneToOne?' — 일대일 함수':' — 일대일은 아니다')):'함수가 아니다'),
        38,406,c.isFn?'#15803d':'#b91c1c',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {kind:S.kind,name:KINDS[S.kind],x:c.x,cur:c.cur,maxc:c.maxc,
            isFn:c.isFn,oneToOne:c.oneToOne};
  },
  headA:['번호','그래프','확인한 x','그 x에서 만난 점','최대 만난 점','함수?','일대일?'],
  rowA:function(r,i){
    return [i+1,r.name,r.x,r.cur+'개','<b>'+r.maxc+'개</b>',
            '<span class="'+(r.isFn?'ok':'no')+'">'+(r.isFn?'○':'×')+'</span>',
            '<span class="'+(r.oneToOne?'ok':'no')+'">'+(r.oneToOne?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],g={},kn=0,fn=[],notFn=[],oto=[];
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(!g[r.name]){ g[r.name]=r; kn++;
        if(r.isFn){ fn.push(r.name); if(r.oneToOne) oto.push(r.name); } else notFn.push(r.name); }
      rows.push([r.name, r.x, r.cur+'개', '<b>'+r.maxc+'개</b>',
                 '<span class="'+(r.isFn?'ok':'no')+'">'+(r.isFn?'○':'×')+'</span>',
                 '<span class="'+(r.oneToOne?'ok':'no')+'">'+(r.oneToOne?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'시험한 그래프',big:kn+'가지',p:'다섯 가지를 모두 기록하면 표가 완성된다.'},
      {t:'함수였던 그래프',big:fn.length+'가지',p:fn.join(', ')||'-'},
      {t:'일대일 함수였던 그래프',big:oto.length+'가지',p:oto.join(', ')||'아직 없음'}
    ];
    var concl;
    if(kn<4){
      concl='<b>더 해 보자</b> — 다섯 가지 그래프를 <b>모두</b> 기록해야 함수와 함수가 아닌 것을 구별할 수 있다.';
    } else {
      concl='<b>정리</b> — 그래프가 그려진다고 모두 함수인 것은 아니었다. '
           +'<b>어떤 세로선과도 두 점 이상에서 만나지 않아야</b> 함수다'+(notFn.length?('('+notFn.join(', ')+'는 함수가 아니다)'):'')+'. '
           +'한 x에 y가 둘 이상 대응하면 “정해진 값”이 없기 때문이다. '
           +'함수 중에서도 <b>가로선과도 한 번만 만나면</b> 일대일 함수이고, 그때만 역함수를 만들 수 있다.';
    }
    return {head:['그래프','x','만난 점','최대','함수?','일대일?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 합성함수
# ============================================================
LAB_COMP = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'합성함수 판',
  action:'두 순서로 넣어 보기',
  hint0:'두 일차함수를 정하고, 넣는 순서를 바꿔 보자.',
  sliders:[
    {id:'a',label:'f의 기울기 a',min:-4,max:4,value:2,color:'#2563eb',unit:''},
    {id:'b',label:'f의 상수 b',min:-6,max:6,value:1,color:'#60a5fa',unit:''},
    {id:'c',label:'g의 기울기 c',min:-4,max:4,value:3,color:'#dc2626',unit:''},
    {id:'d',label:'g의 상수 d',min:-6,max:6,value:-2,color:'#f87171',unit:''}
  ],
  calc:function(S){
    var fg={m:S.a*S.c,k:S.a*S.d+S.b};
    var gf={m:S.c*S.a,k:S.c*S.b+S.d};
    return {fg:fg,gf:gf,same:(fg.m===gf.m&&fg.k===gf.k)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'(f∘g)(x)',v:ran?(c.fg.m+'x'+sg(c.fg.k)):'계산해 보자'},
            {k:'(g∘f)(x)',v:ran?(c.gf.m+'x'+sg(c.gf.k)):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'f(g(x)) = '+c.fg.m+'x'+sg(c.fg.k)+',  g(f(x)) = '+c.gf.m+'x'+sg(c.gf.k)+'.  두 식이 '+(c.same?'같다':'다르다')+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var p1=(t===null)?0:Math.min(1,t/0.5);
    var p2=(t===null)?0:Math.max(0,(t-0.5)/0.5);
    lbl(ctx,'f(x) = '+S.a+'x'+sg(S.b)+'      g(x) = '+S.c+'x'+sg(S.d),24,36,'#1d4ed8',18);
    function chain(y,order,col,res,alpha){
      ctx.globalAlpha=alpha;
      var names=order;
      var X=44;
      lbl(ctx,'x',X,y+26,'#334155',18);
      for(i=0;i<2;i++){
        var bx=X+40+i*130;
        ctx.strokeStyle=col;ctx.lineWidth=2.4;
        ctx.beginPath();ctx.moveTo(bx-24,y+20);ctx.lineTo(bx-4,y+20);ctx.stroke();
        ctx.beginPath();ctx.moveTo(bx-10,y+15);ctx.lineTo(bx-4,y+20);ctx.lineTo(bx-10,y+25);ctx.stroke();
        ctx.fillStyle='#fff';ctx.fillRect(bx,y,74,42);
        ctx.strokeStyle=col;ctx.lineWidth=2.4;ctx.strokeRect(bx,y,74,42);
        ctx.fillStyle=col;ctx.font='bold 16px sans-serif';ctx.textAlign='center';
        ctx.fillText(names[i],bx+37,y+26);
        ctx.textAlign='left';
      }
      ctx.strokeStyle=col;ctx.lineWidth=2.4;
      ctx.beginPath();ctx.moveTo(X+40+130+74,y+20);ctx.lineTo(X+40+130+94,y+20);ctx.stroke();
      lbl(ctx,res,X+40+130+100,y+26,col,16);
      ctx.globalAlpha=1;
    }
    chain(90,['g','f'],'#2563eb',(p1>=1)?(c.fg.m+'x'+sg(c.fg.k)):'?',Math.max(p1,0.15));
    chain(180,['f','g'],'#dc2626',(p2>=1)?(c.gf.m+'x'+sg(c.gf.k)):'?',Math.max(p2,0.15));
    lbl(ctx,'f∘g : g를 먼저',24,80,'#52627a',13);
    lbl(ctx,'g∘f : f를 먼저',24,170,'#52627a',13);
    box(ctx,20,246,400,138);
    lbl(ctx,(t===null)?'순서를 바꾸면 같을까?':('(f∘g)(x) = '+c.fg.m+'x'+sg(c.fg.k)),38,280,'#1d4ed8',19);
    lbl(ctx,(t===null)?'':('(g∘f)(x) = '+c.gf.m+'x'+sg(c.gf.k)),38,314,'#b91c1c',19);
    lbl(ctx,(t===null)?'':('x의 계수는 둘 다 '+c.fg.m+' (ac로 같다)'),38,346,'#52627a',16);
    lbl(ctx,(t===null)?'':(c.same?'두 합성함수가 같다':'상수항이 달라 두 합성함수가 다르다'),38,374,c.same?'#b45309':'#15803d',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,c:S.c,d:S.d,
            fg:c.fg.m+'x'+sg(c.fg.k),gf:c.gf.m+'x'+sg(c.gf.k),
            fgk:c.fg.k,gfk:c.gf.k,mSame:true,same:c.same};
  },
  headA:['번호','f','g','f∘g','g∘f','x 계수 같음','상수항','같은가?'],
  rowA:function(r,i){
    return [i+1,r.a+'x'+sg(r.b),r.c+'x'+sg(r.d),'<b>'+r.fg+'</b>',r.gf,
            '<span class="ok">○</span>',r.fgk+' / '+r.gfk,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,diff=0,triv=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same){ same++; if(r.a===r.c&&r.b===r.d) triv++; }
      else diff++;
      rows.push([r.a+'x'+sg(r.b)+' , '+r.c+'x'+sg(r.d), '<b>'+r.fg+'</b>', r.gf,
                 r.fgk+' / '+r.gfk,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'f∘g = g∘f 였던 횟수',big:same+' / '+rec.length,
       p:same?('그중 f와 g가 같은 함수였던 것 '+triv+'개.'):'순서가 바뀌면 대개 결과가 다르다.'},
      {t:'달랐던 횟수',big:diff+'개',
       p:diff?'x의 계수는 같아도 상수항이 달랐다.':'계수를 바꿔 다른 경우를 만들어 보자.'},
      {t:'x의 계수',big:'항상 ac',p:'두 순서 모두 기울기끼리 곱해진다. 차이는 상수항에서 생긴다.'}
    ];
    var concl;
    if(diff===0){
      concl='<b>더 해 보자</b> — 아직 두 합성이 다른 경우를 못 만났다. f와 g의 상수항을 다르게 해 보자.';
    } else {
      concl='<b>정리</b> — 합성함수는 <b>넣는 순서에 따라 결과가 달랐다</b>('+diff+'번). '
           +'f∘g는 g를 먼저 통과시킨 뒤 f에 넣는 것이고, g∘f는 그 반대다. '
           +'일차함수끼리는 x의 계수가 둘 다 ac로 같지만 <b>상수항이 달라진다</b>. '
           +'f∘g = g∘f 가 되는 것은 특별한 경우뿐이고, 일반적으로 <b>교환법칙이 성립하지 않는다</b>.';
    }
    return {head:['f , g','f∘g','g∘f','상수항','같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 역함수
# ============================================================
LAB_INV = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'역함수 판',
  action:'되돌려 보기',
  hint0:'일차함수와 넣을 값을 정하고, 역함수와 역수를 구별해 보자.',
  sliders:[
    {id:'a',label:'기울기 a',min:-4,max:4,value:2,color:'#2563eb',unit:''},
    {id:'b',label:'상수 b',min:-6,max:6,value:-3,color:'#60a5fa',unit:''},
    {id:'x0',label:'넣을 값 x',min:-6,max:6,value:4,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    if(S.a===0) return {zero:true};
    var fx=S.a*S.x0+S.b;
    var inv=(S.x0-S.b)/S.a;
    var recip=(fx===0)?null:(1/fx);
    var back=S.a*inv+S.b;
    var round=(fx-S.b)/S.a;
    return {zero:false,fx:fx,inv:inv,recip:recip,back:back,round:round};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    if(c.zero) return [{k:'a = 0',v:'역함수가 없다'},{k:'',v:'a를 바꾸자'}];
    return [{k:'f(x)',v:c.fx},
            {k:'f⁻¹(x)',v:ran?r3(c.inv):'구해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.zero) return 'a = 0 이면 일대일이 아니라 역함수가 없다.';
    return 'f('+S.x0+') = '+c.fx+', f⁻¹('+S.x0+') = '+r3(c.inv)+', 1/f('+S.x0+') = '+((c.recip===null)?'정의 안 됨':r3(c.recip))+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,8,7);
    if(c.zero){ lbl(ctx,'a = 0 이면 역함수가 없다',24,36,'#b91c1c',19); return; }
    ctx.strokeStyle='#c4b5fd';ctx.lineWidth=2;ctx.setLineDash([5,5]);
    ctx.beginPath();ctx.moveTo(CX-7*U,CY+7*U);ctx.lineTo(CX+7*U,CY-7*U);ctx.stroke();ctx.setLineDash([]);
    function line(m,k,col){
      ctx.strokeStyle=col;ctx.lineWidth=3;ctx.beginPath();
      var st=false;
      for(i=-80;i<=80;i++){
        var x=i/10, y=m*x+k;
        if(y<-7||y>7){ st=false; continue; }
        if(!st){ ctx.moveTo(CX+x*U,CY-y*U); st=true; } else ctx.lineTo(CX+x*U,CY-y*U);
      }
      ctx.stroke();
    }
    line(S.a,S.b,'#2563eb');
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0) line(1/S.a,-S.b/S.a,'#dc2626');
    if(grow>=1){
      if(Math.abs(S.x0)<=8&&Math.abs(c.fx)<=7){
        ctx.beginPath();ctx.arc(CX+S.x0*U,CY-c.fx*U,7,0,Math.PI*2);
        ctx.fillStyle='#2563eb';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      }
      if(Math.abs(c.fx)<=8&&Math.abs(S.x0)<=7){
        ctx.beginPath();ctx.arc(CX+c.fx*U,CY-S.x0*U,7,0,Math.PI*2);
        ctx.fillStyle='#dc2626';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      }
    }
    lbl(ctx,'f(x) = '+S.a+'x'+sg(S.b)+'      f⁻¹(x) = (x'+sg(-S.b)+') / '+S.a,24,32,'#334155',15);
    lbl(ctx,'보라 점선 = y = x',24,54,'#8b5cf6',13);
    box(ctx,20,336,400,84);
    lbl(ctx,(t===null)?'역함수는 역수와 같을까?':('f('+S.x0+') = '+c.fx+'      f⁻¹('+S.x0+') = '+r3(c.inv)),38,366,'#1f2937',18);
    lbl(ctx,(t===null)?'':('1 / f('+S.x0+') = '+((c.recip===null)?'정의 안 됨':r3(c.recip))+'      f(f⁻¹('+S.x0+')) = '+r3(c.back)),
        38,398,'#b91c1c',17);
  },
  record:function(S){
    var c=this.calc(S);
    if(c.zero) return {zero:true};
    return {zero:false,a:S.a,b:S.b,x0:S.x0,
            fx:r3(c.fx),inv:r3(c.inv),
            recip:(c.recip===null)?'-':r3(c.recip),
            back:r3(c.back),
            backOk:(Math.abs(c.back-S.x0)<1e-9),
            invEqRecip:(c.recip!==null&&Math.abs(c.inv-c.recip)<1e-9)};
  },
  headA:['번호','f(x)','x','f(x) 값','f⁻¹(x)','1/f(x)','f(f⁻¹(x))','x로 돌아옴?','역함수 = 역수?'],
  rowA:function(r,i){
    if(r.zero) return [i+1,'a=0','-','-','-','-','-','-','-'];
    return [i+1,r.a+'x'+sg(r.b),r.x0,r.fx,'<b>'+r.inv+'</b>',r.recip,r.back,
            '<span class="'+(r.backOk?'ok':'no')+'">'+(r.backOk?'○':'×')+'</span>',
            '<span class="'+(r.invEqRecip?'ok':'no')+'">'+(r.invEqRecip?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],valid=0,back=0,eq=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.zero){ rows.push(['a=0','-','-','-','-','-']); continue; }
      valid++;
      if(r.backOk) back++;
      if(r.invEqRecip) eq++;
      rows.push([r.a+'x'+sg(r.b), r.x0, '<b>'+r.inv+'</b>', r.recip, r.back,
                 '<span class="'+(r.backOk?'ok':'no')+'">'+(r.backOk?'○':'×')+'</span>',
                 '<span class="'+(r.invEqRecip?'ok':'no')+'">'+(r.invEqRecip?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'f(f⁻¹(x)) = x',big:back+' / '+valid,
       p:'역함수를 통과시킨 뒤 다시 f에 넣으면 처음 값으로 돌아오는지 확인한 결과.'},
      {t:'f⁻¹(x) = 1/f(x) 였던 횟수',big:eq+' / '+valid,
       p:'역함수 기호를 역수로 읽으면 어떻게 되는지 확인했다.'},
      {t:'유효한 기록',big:valid+'개',p:'a = 0이면 일대일이 아니라 역함수가 없다.'}
    ];
    var concl;
    if(valid===0){
      concl='<b>더 해 보자</b> — a를 0이 아닌 값으로 두어야 역함수가 존재한다.';
    } else if(back===valid&&eq===0){
      concl='<b>정리</b> — f⁻¹은 <b>f를 되돌리는 함수</b>였다. f(f⁻¹(x))는 언제나 x로 돌아왔다. '
           +'반면 <b>1/f(x)와는 한 번도 같지 않았다.</b> f⁻¹의 −1은 지수가 아니라 “거꾸로”라는 표시다. '
           +'그래프에서도 f와 f⁻¹은 <b>y = x에 대해 대칭</b>으로 놓였다. x와 y의 역할을 맞바꾼 것이기 때문이다.';
    } else {
      concl='<b>정리</b> — 역함수는 f를 되돌리는 함수다. 역수와 혼동하지 않도록 여러 값으로 확인해 보자.';
    }
    return {head:['f','x','f⁻¹(x)','1/f(x)','f(f⁻¹(x))','x로 돌아옴?','역수와 같나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("h2_de_morgan_lab.html",
     "집합 실험실 — 여집합을 씌우면 ∪는 어떻게 될까?",
     "집합 실험실 — 여집합을 씌우면 ∪는 어떻게 될까?",
     "1부터 12까지에서 두 집합을 만들어 여집합 연산 결과를 원소 단위로 대조한다.",
     LAB_DEM),
    ("h2_proposition_converse_lab.html",
     "명제 실험실 — 참인 명제의 역도 참일까?",
     "명제 실험실 — 참인 명제의 역도 참일까?",
     "1부터 24까지 모든 수를 확인해 원명제·역·이·대우의 참거짓을 판정하고 반례를 찾는다.",
     LAB_PROP),
    ("h2_function_test_lab.html",
     "함수 판정 실험실 — 그래프면 다 함수일까?",
     "함수 판정 실험실 — 그래프면 다 함수일까?",
     "세로선을 옮기며 그래프와 만나는 점의 개수를 세어 함수와 일대일 함수를 판정한다.",
     LAB_FUNC),
    ("h2_composite_function_lab.html",
     "합성함수 실험실 — 넣는 순서를 바꾸면?",
     "합성함수 실험실 — 넣는 순서를 바꾸면?",
     "두 일차함수를 서로 다른 순서로 합성해 식과 값을 비교한다.",
     LAB_COMP),
    ("h2_inverse_function_lab.html",
     "역함수 실험실 — f⁻¹은 1/f 일까?",
     "역함수 실험실 — f⁻¹은 1/f 일까?",
     "역함수와 역수를 나란히 계산하고, f(f⁻¹(x))가 x로 돌아오는지 확인한다.",
     LAB_INV),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c24_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
