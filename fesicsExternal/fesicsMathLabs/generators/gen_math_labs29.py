# -*- coding: utf-8 -*-
"""고등 확률과 통계 — 경우의 수 2종 + 확률 3종"""
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
function fact(n){var v=1,i;for(i=2;i<=n;i++)v*=i;return v;}
function nCr(n,r){ if(r<0||r>n) return 0; return Math.round(fact(n)/(fact(r)*fact(n-r))); }
"""

# ============================================================
# 1. 중복을 허용할 때와 아닐 때
# ============================================================
LAB_REP = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'뽑기 방식 판',
  action:'모두 나열해 세기',
  hint0:'전체 개수와 뽑는 개수를 정하고, 세 방식을 비교해 보자.',
  sliders:[
    {id:'n',label:'전체 개수 n',min:2,max:5,value:3,color:'#2563eb',unit:''},
    {id:'r',label:'뽑는 개수 r',min:1,max:3,value:2,color:'#16a34a',unit:''}
  ],
  calc:function(S){
    var rep=[],per=[],com=[],i;
    function rec1(cur){
      if(cur.length===S.r){ rep.push(cur.slice()); return; }
      for(i=0;i<S.n;i++){ cur.push(i); rec1(cur); cur.pop(); }
    }
    rec1([]);
    function rec2(cur,used){
      if(cur.length===S.r){ per.push(cur.slice()); return; }
      for(var j=0;j<S.n;j++){ if(used[j]) continue; used[j]=1; cur.push(j); rec2(cur,used); cur.pop(); used[j]=0; }
    }
    rec2([],[]);
    function rec3(start,cur){
      if(cur.length===S.r){ com.push(cur.slice()); return; }
      for(var k=start;k<S.n;k++){ cur.push(k); rec3(k+1,cur); cur.pop(); }
    }
    rec3(0,[]);
    return {rep:rep,per:per,com:com,
            fRep:Math.pow(S.n,S.r),
            fPer:(S.r<=S.n)?(fact(S.n)/fact(S.n-S.r)):0,
            fCom:nCr(S.n,S.r)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'중복 허용, 순서 O',v:ran?(c.rep.length+'가지'):'세어 보자'},
            {k:'중복 없이, 순서 O / X',v:ran?(c.per.length+' / '+c.com.length):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '중복 허용 '+c.rep.length+'가지, 중복 없이 순서 있음 '+c.per.length+'가지, 순서 없음 '+c.com.length+'가지다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i, j;
    var NAMES=['A','B','C','D','E'];
    var shown=(t===null)?0:Math.min(1,t);
    function list(y,label,arr,col,show){
      lbl(ctx,label+' — '+(show?arr.length+'가지':'?'),24,y,col,15);
      var per=8, cw=46;
      for(i=0;i<arr.length&&i<24;i++){
        var s='';
        for(j=0;j<arr[i].length;j++) s+=NAMES[arr[i][j]];
        var x=28+(i%per)*cw, yy=y+20+Math.floor(i/per)*20;
        ctx.fillStyle=show?col:'#e2e8f0';
        ctx.font='bold 13px sans-serif';ctx.textAlign='left';
        ctx.fillText(s,x,yy);
      }
      if(arr.length>24) lbl(ctx,'...',28+8*cw,y+20,'#94a3b8',13);
    }
    list(46,'중복 허용, 순서 있음',c.rep,'#2563eb',shown>0.2);
    list(160,'중복 없이, 순서 있음',c.per,'#dc2626',shown>0.55);
    list(268,'중복 없이, 순서 없음',c.com,'#16a34a',shown>=1);
    box(ctx,20,346,400,74);
    lbl(ctx,(t===null)?'세 방식은 몇 가지씩일까?':(c.rep.length+' / '+c.per.length+' / '+c.com.length+'가지'),38,376,'#1f2937',19);
    lbl(ctx,(t===null)?'':('n^r = '+c.fRep+'      nPr = '+c.fPer+'      nCr = '+c.fCom),38,406,'#52627a',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {n:S.n,r:S.r,rep:c.rep.length,per:c.per.length,com:c.com.length,
            fRep:c.fRep,fPer:c.fPer,fCom:c.fCom,
            ok1:(c.rep.length===c.fRep),ok2:(c.per.length===c.fPer),ok3:(c.com.length===c.fCom),
            allSame:(c.rep.length===c.per.length&&c.per.length===c.com.length)};
  },
  headA:['번호','n, r','중복 허용','n^r','중복 없이 순서 O','nPr','순서 X','nCr','모두 맞나?'],
  rowA:function(r,i){
    var ok=(r.ok1&&r.ok2&&r.ok3);
    return [i+1,r.n+', '+r.r,'<b>'+r.rep+'</b>',r.fRep,r.per,r.fPer,r.com,r.fCom,
            '<span class="'+(ok?'ok':'no')+'">'+(ok?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ok=0,same=0,one=0,order=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.ok1&&r.ok2&&r.ok3) ok++;
      if(r.allSame){ same++; if(r.r===1) one++; }
      if(r.rep>r.per&&r.per>r.com) order++;
      rows.push([r.n+', '+r.r, r.rep+' / '+r.fRep, r.per+' / '+r.fPer, r.com+' / '+r.fCom,
                 '<span class="'+((r.ok1&&r.ok2&&r.ok3)?'ok':'no')+'">'+((r.ok1&&r.ok2&&r.ok3)?'○':'×')+'</span>',
                 (r.rep>r.per&&r.per>r.com)?'중복>순열>조합':'-']);
    }
    var stats=[
      {t:'나열해 센 수가 공식과 모두 일치',big:ok+' / '+rec.length,
       p:'n^r, nPr, nCr 세 공식을 한꺼번에 확인한 결과.'},
      {t:'세 값이 모두 같았던 횟수',big:same+' / '+rec.length,
       p:same?('그중 r = 1 이었던 것 '+one+'개. 하나만 뽑으면 세 방식이 같아진다.'):'r = 1 로도 해 보자.'},
      {t:'중복 > 순열 > 조합 이었던 횟수',big:order+' / '+rec.length,
       p:'조건을 하나씩 붙일수록 가짓수가 줄어든다.'}
    ];
    var concl;
    if(ok===rec.length){
      concl='<b>정리</b> — 같은 “n개에서 r개 뽑기”라도 <b>중복을 허용하는가</b>와 <b>순서를 따지는가</b>에 따라 가짓수가 달랐다. '
           +'중복 허용은 n^r, 중복 없이 순서를 따지면 nPr, 순서를 무시하면 nCr 이고 언제나 <b>n^r ≥ nPr ≥ nCr</b> 이었다. '
           +'문제를 읽을 때 이 두 가지를 먼저 판단해야 한다. r = 1 일 때만 셋이 같아진다.';
    } else {
      concl='<b>확인 필요</b> — 나열한 수와 공식이 어긋난 기록이 있다.';
    }
    return {head:['n, r','중복 허용','순서 O','순서 X','모두 맞나?','대소'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 파스칼 삼각형과 이항정리
# ============================================================
LAB_PASCAL = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'파스칼 삼각형 판',
  action:'한 줄씩 만들기',
  hint0:'몇 번째 줄까지 볼지, 어느 항을 확인할지 정해 보자.',
  sliders:[
    {id:'n',label:'줄 번호 n',min:1,max:9,value:5,color:'#2563eb',unit:''},
    {id:'r',label:'항 번호 r',min:0,max:9,value:2,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var r=Math.min(S.r,S.n);
    var sum=0,i;
    for(i=0;i<=S.n;i++) sum+=nCr(S.n,i);
    return {r:r,val:nCr(S.n,r),
            up:nCr(S.n-1,r-1)+nCr(S.n-1,r),
            sym:nCr(S.n,S.n-r),
            sum:sum,pow:Math.pow(2,S.n)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'nCr',v:c.val},
            {k:'윗줄 두 수의 합',v:ran?c.up:'만들어 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'nCr = '+c.val+', 윗줄 두 수의 합 = '+c.up+', 한 줄 전체의 합 = '+c.sum+' (2^n = '+c.pow+'). 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i, j;
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*(S.n+1));
    var CW=40, TOP=52;
    for(i=0;i<=S.n;i++){
      var on=(i<shown);
      var w=(i+1)*CW;
      for(j=0;j<=i;j++){
        var x=220-w/2+j*CW, y=TOP+i*36;
        var hit=(i===S.n&&j===c.r);
        var src=(i===S.n-1&&(j===c.r-1||j===c.r));
        ctx.fillStyle=on?(hit?'#fde68a':(src?'#dbeafe':'#f8fafc')):'#f8fafc';
        ctx.fillRect(x,y,CW-4,28);
        ctx.strokeStyle=on?(hit?'#f59e0b':(src?'#2563eb':'#e2e8f0')):'#f1f5f9';
        ctx.lineWidth=hit?2.4:1.2;
        ctx.strokeRect(x,y,CW-4,28);
        if(on){
          ctx.fillStyle=hit?'#7c2d12':'#334155';ctx.font='bold 13px sans-serif';ctx.textAlign='center';
          ctx.fillText(nCr(i,j),x+(CW-4)/2,y+19);
        }
      }
    }
    ctx.textAlign='left';
    box(ctx,20,384,400,34);
    lbl(ctx,(t===null)?'윗줄 두 수를 더하면?':(nCr(S.n-1,c.r-1)+' + '+nCr(S.n-1,c.r)+' = '+c.up+'   /   nCr = '+c.val),
        30,406,'#1f2937',16);
    lbl(ctx,'n = '+S.n+', r = '+c.r,24,32,'#1d4ed8',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {n:S.n,r:c.r,val:c.val,up:c.up,sym:c.sym,sum:c.sum,pow:c.pow,
            upOk:(c.val===c.up),symOk:(c.val===c.sym),sumOk:(c.sum===c.pow)};
  },
  headA:['번호','n, r','nCr','윗줄 두 수의 합','같나?','nC(n−r)','같나?','한 줄의 합','2^n','같나?'],
  rowA:function(r,i){
    return [i+1,r.n+', '+r.r,'<b>'+r.val+'</b>',r.up,
            '<span class="'+(r.upOk?'ok':'no')+'">'+(r.upOk?'○':'×')+'</span>',
            r.sym,
            '<span class="'+(r.symOk?'ok':'no')+'">'+(r.symOk?'○':'×')+'</span>',
            r.sum,r.pow,
            '<span class="'+(r.sumOk?'ok':'no')+'">'+(r.sumOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],up=0,sym=0,sum=0,ns={},nn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.upOk) up++;
      if(r.symOk) sym++;
      if(r.sumOk) sum++;
      if(!ns[r.n]){ ns[r.n]=true; nn++; }
      rows.push([r.n+', '+r.r, '<b>'+r.val+'</b>', r.up,
                 '<span class="'+(r.upOk?'ok':'no')+'">'+(r.upOk?'○':'×')+'</span>',
                 r.sym,
                 '<span class="'+(r.symOk?'ok':'no')+'">'+(r.symOk?'○':'×')+'</span>',
                 r.sum+' / '+r.pow,
                 '<span class="'+(r.sumOk?'ok':'no')+'">'+(r.sumOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'nCr = (n−1)C(r−1) + (n−1)Cr',big:up+' / '+rec.length,p:'윗줄 두 수를 더한 값과 비교한 결과.'},
      {t:'nCr = nC(n−r)',big:sym+' / '+rec.length,p:'삼각형이 좌우 대칭인지 확인한 결과.'},
      {t:'한 줄의 합 = 2^n',big:sum+' / '+rec.length,p:'시험한 n '+nn+'가지.'}
    ];
    var concl;
    if(up===rec.length&&sym===rec.length&&sum===rec.length){
      concl='<b>정리</b> — 각 수는 언제나 <b>윗줄 두 수의 합</b>이었다. r개를 뽑을 때 마지막 하나를 “뽑는 경우”와 “안 뽑는 경우”로 나눈 결과다. '
           +'또 삼각형은 <b>좌우 대칭</b>(nCr = nC(n−r))이었고, 한 줄의 합은 언제나 <b>2^n</b> 이었다. '
           +'이는 (1+1)^n 을 이항정리로 펼친 것과 같다.';
    } else {
      concl='<b>확인 필요</b> — 관계가 어긋난 기록이 있다.';
    }
    return {head:['n, r','nCr','윗줄 합','같나?','nC(n−r)','같나?','줄의 합 / 2^n','같나?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 조건부확률
# ============================================================
LAB_COND = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'2×2 분할표',
  action:'조건부확률 구하기',
  hint0:'네 칸의 사람 수를 정해 보자.',
  sliders:[
    {id:'a',label:'A이고 B',min:0,max:40,value:8,color:'#7c3aed',unit:'명'},
    {id:'b',label:'A이고 B 아님',min:0,max:40,value:2,color:'#2563eb',unit:'명'},
    {id:'c',label:'A 아니고 B',min:0,max:40,value:32,color:'#dc2626',unit:'명'},
    {id:'d',label:'둘 다 아님',min:0,max:40,value:8,color:'#94a3b8',unit:'명'}
  ],
  calc:function(S){
    var tot=S.a+S.b+S.c+S.d;
    if(tot===0) return {zero:true};
    var A=S.a+S.b, B=S.a+S.c;
    return {zero:false,tot:tot,A:A,B:B,ab:S.a,
            pA:A/tot,pB:B/tot,pAB:S.a/tot,
            aGb:(B===0)?null:(S.a/B),
            bGa:(A===0)?null:(S.a/A)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    if(c.zero) return [{k:'전체 0명',v:'인원을 넣자'},{k:'',v:''}];
    return [{k:'P(A|B)',v:ran?((c.aGb===null)?'-':r3(c.aGb)):'구해 보자'},
            {k:'P(B|A)',v:ran?((c.bGa===null)?'-':r3(c.bGa)):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.zero) return '전체가 0명이다. 인원을 넣어 보자.';
    return 'P(A|B) = '+((c.aGb===null)?'-':r3(c.aGb))+', P(B|A) = '+((c.bGa===null)?'-':r3(c.bGa))+'. 두 값이 같은지 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    if(c.zero){ lbl(ctx,'전체가 0명이다',24,200,'#b91c1c',20); return; }
    var X0=110, Y0=80, CW=130, CH=60;
    var vals=[[S.a,S.b],[S.c,S.d]];
    var rowL=['A','A 아님'], colL=['B','B 아님'];
    ctx.font='bold 15px sans-serif';ctx.textAlign='center';
    for(i=0;i<2;i++){ ctx.fillStyle='#334155';ctx.fillText(colL[i],X0+i*CW+CW/2,Y0-10); }
    for(i=0;i<2;i++){
      ctx.fillStyle='#334155';ctx.textAlign='right';
      ctx.fillText(rowL[i],X0-10,Y0+i*CH+CH/2+5);
      ctx.textAlign='center';
      for(var j=0;j<2;j++){
        var x=X0+j*CW, y=Y0+i*CH;
        ctx.fillStyle=(i===0&&j===0)?'#ede9fe':'#f8fafc';
        ctx.fillRect(x,y,CW-3,CH-3);
        ctx.strokeStyle='#94a3b8';ctx.lineWidth=1.4;ctx.strokeRect(x,y,CW-3,CH-3);
        ctx.fillStyle='#1f2937';ctx.font='bold 20px sans-serif';
        ctx.fillText(vals[i][j],x+CW/2-1,y+CH/2+7);
      }
    }
    ctx.textAlign='left';
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0.3){
      ctx.strokeStyle='#dc2626';ctx.lineWidth=3;
      ctx.strokeRect(X0-3,Y0-3,CW,2*CH);
      lbl(ctx,'B인 사람 '+c.B+'명',X0+CW+8,Y0+18,'#b91c1c',14);
    }
    if(grow>=1){
      ctx.strokeStyle='#2563eb';ctx.lineWidth=3;
      ctx.strokeRect(X0-3,Y0-3,2*CW,CH);
      lbl(ctx,'A인 사람 '+c.A+'명',X0,Y0+2*CH+24,'#1d4ed8',14);
    }
    lbl(ctx,'전체 '+c.tot+'명',24,32,'#1d4ed8',17);
    box(ctx,20,244,400,174);
    lbl(ctx,'P(A) = '+r3(c.pA)+'      P(B) = '+r3(c.pB)+'      P(A∩B) = '+r3(c.pAB),38,276,'#52627a',16);
    lbl(ctx,(t===null)?'P(A|B)와 P(B|A)는 같을까?':('P(A|B) = '+S.a+' / '+c.B+' = '+((c.aGb===null)?'-':r3(c.aGb))),38,314,'#b91c1c',18);
    lbl(ctx,(t===null)?'':('P(B|A) = '+S.a+' / '+c.A+' = '+((c.bGa===null)?'-':r3(c.bGa))),38,348,'#1d4ed8',18);
    lbl(ctx,(t===null)?'':('두 값이 '+(((c.aGb!==null&&c.bGa!==null)&&Math.abs(c.aGb-c.bGa)<1e-9)?'같다':'다르다')),38,384,'#334155',17);
  },
  record:function(S){
    var c=this.calc(S);
    if(c.zero) return {zero:true};
    return {zero:false,a:S.a,b:S.b,c:S.c,d:S.d,tot:c.tot,A:c.A,B:c.B,
            aGb:(c.aGb===null)?'-':r3(c.aGb),
            bGa:(c.bGa===null)?'-':r3(c.bGa),
            same:(c.aGb!==null&&c.bGa!==null&&Math.abs(c.aGb-c.bGa)<1e-9),
            eqAB:(c.A===c.B),
            mulOk:(c.bGa!==null&&Math.abs(c.pAB-c.pA*c.bGa)<1e-9)};
  },
  headA:['번호','네 칸','A인 수','B인 수','P(A|B)','P(B|A)','같나?','A수 = B수?'],
  rowA:function(r,i){
    if(r.zero) return [i+1,'0명','-','-','-','-','-','-'];
    return [i+1,r.a+'/'+r.b+'/'+r.c+'/'+r.d,r.A,r.B,'<b>'+r.aGb+'</b>',r.bGa,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
            '<span class="'+(r.eqAB?'ok':'no')+'">'+(r.eqAB?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],valid=0,same=0,sameEq=0,mul=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.zero){ rows.push(['0명','-','-','-','-']); continue; }
      valid++;
      if(r.same){ same++; if(r.eqAB) sameEq++; }
      if(r.mulOk) mul++;
      rows.push([r.a+'/'+r.b+'/'+r.c+'/'+r.d, r.A+' / '+r.B, '<b>'+r.aGb+'</b>', r.bGa,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',
                 '<span class="'+(r.eqAB?'ok':'no')+'">'+(r.eqAB?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'P(A|B) = P(B|A) 였던 횟수',big:same+' / '+valid,
       p:same?('그중 A인 수와 B인 수가 같았던 것 '+sameEq+'개.'):'두 조건부확률은 대개 다르다.'},
      {t:'P(A∩B) = P(A)·P(B|A)',big:mul+' / '+valid,
       p:'곱셈정리가 성립하는지 확인한 결과.'},
      {t:'유효한 기록',big:valid+'개',p:'분모가 되는 집단이 무엇인지가 핵심이다.'}
    ];
    var concl;
    if(valid===0){
      concl='<b>더 해 보자</b> — 네 칸에 인원을 넣어야 확률을 구할 수 있다.';
    } else if(same===sameEq){
      concl='<b>정리</b> — P(A|B)와 P(B|A)는 <b>분모가 다른 전혀 다른 확률</b>이었다. '
           +'같아진 것은 A인 사람 수와 B인 사람 수가 우연히 같을 때뿐이었다. '
           +'“B인 사람 중 A의 비율”과 “A인 사람 중 B의 비율”을 바꿔 읽는 것은 흔한 오류다. '
           +'한편 P(A∩B) = P(A)·P(B|A) 는 언제나 성립했다.';
    } else {
      concl='<b>정리</b> — 두 조건부확률은 분모가 다르다. 어떤 집단을 기준으로 삼는지 확인하며 더 기록해 보자.';
    }
    return {head:['네 칸','A수 / B수','P(A|B)','P(B|A)','같나?','A수=B수?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 독립과 배반
# ============================================================
LAB_INDEP = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'독립·배반 판',
  action:'두 조건 확인하기',
  hint0:'네 칸의 인원을 정하고, 독립인지 배반인지 확인해 보자.',
  sliders:[
    {id:'a',label:'A이고 B',min:0,max:30,value:6,color:'#7c3aed',unit:'명'},
    {id:'b',label:'A이고 B 아님',min:0,max:30,value:6,color:'#2563eb',unit:'명'},
    {id:'c',label:'A 아니고 B',min:0,max:30,value:9,color:'#dc2626',unit:'명'},
    {id:'d',label:'둘 다 아님',min:0,max:30,value:9,color:'#94a3b8',unit:'명'}
  ],
  calc:function(S){
    var tot=S.a+S.b+S.c+S.d;
    if(tot===0) return {zero:true};
    var pA=(S.a+S.b)/tot, pB=(S.a+S.c)/tot, pAB=S.a/tot;
    return {zero:false,tot:tot,pA:pA,pB:pB,pAB:pAB,prod:pA*pB,
            indep:(Math.abs(pAB-pA*pB)<1e-9),
            excl:(S.a===0),
            possible:(pA>0&&pB>0)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    if(c.zero) return [{k:'전체 0명',v:'인원을 넣자'},{k:'',v:''}];
    return [{k:'P(A∩B)',v:r3(c.pAB)},
            {k:'P(A)·P(B)',v:ran?r3(c.prod):'확인해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.zero) return '인원을 넣어 보자.';
    return 'P(A∩B) = '+r3(c.pAB)+', P(A)P(B) = '+r3(c.prod)+'.  '+(c.indep?'독립이다.':'독립이 아니다.')+(c.excl?' 그리고 배반이다.':'')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    if(c.zero){ lbl(ctx,'전체가 0명이다',24,200,'#b91c1c',20); return; }
    var X0=60, Y0=70, W=320, H=180;
    var wA=W*c.pA;
    var hB=H*c.pB;
    ctx.fillStyle='#f1f5f9';ctx.fillRect(X0,Y0,W,H);
    ctx.strokeStyle='#334155';ctx.lineWidth=2;ctx.strokeRect(X0,Y0,W,H);
    ctx.fillStyle='rgba(37,99,235,0.20)';ctx.fillRect(X0,Y0,wA,H);
    ctx.fillStyle='rgba(220,38,38,0.20)';ctx.fillRect(X0,Y0,W,hB);
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      ctx.fillStyle='rgba(124,58,237,0.35)';
      ctx.fillRect(X0,Y0,wA,hB);
      ctx.strokeStyle='#7c3aed';ctx.lineWidth=2.4;ctx.strokeRect(X0,Y0,wA,hB);
    }
    lbl(ctx,'A ('+r3(c.pA)+')',X0+wA/2-20,Y0+H+20,'#1d4ed8',14);
    lbl(ctx,'B ('+r3(c.pB)+')',X0-52,Y0+hB/2,'#b91c1c',14);
    if(grow>=1) lbl(ctx,'겹친 넓이 = P(A)P(B) = '+r3(c.prod),X0,Y0-12,'#6d28d9',14);
    lbl(ctx,'실제 P(A∩B) = '+r3(c.pAB),24,32,'#334155',16);
    box(ctx,20,282,400,136);
    lbl(ctx,'P(A) = '+r3(c.pA)+'      P(B) = '+r3(c.pB),38,314,'#52627a',17);
    lbl(ctx,(t===null)?'독립일까? 배반일까?':('P(A∩B) = '+r3(c.pAB)+'      P(A)P(B) = '+r3(c.prod)),38,348,'#1f2937',18);
    lbl(ctx,(t===null)?'':('독립 : '+(c.indep?'예':'아니오')+'      배반 : '+(c.excl?'예':'아니오')),38,382,c.indep?'#15803d':'#b91c1c',18);
    lbl(ctx,(t===null)?'':((c.indep&&c.excl)?'둘 다 성립 — P(A) 또는 P(B)가 0일 때만 가능':''),38,408,'#b45309',14);
  },
  record:function(S){
    var c=this.calc(S);
    if(c.zero) return {zero:true};
    return {zero:false,a:S.a,b:S.b,c:S.c,d:S.d,
            pA:r3(c.pA),pB:r3(c.pB),pAB:r3(c.pAB),prod:r3(c.prod),
            indep:c.indep,excl:c.excl,both:(c.indep&&c.excl),
            possible:c.possible};
  },
  headA:['번호','네 칸','P(A)','P(B)','P(A∩B)','P(A)P(B)','독립?','배반?','둘 다?'],
  rowA:function(r,i){
    if(r.zero) return [i+1,'0명','-','-','-','-','-','-','-'];
    return [i+1,r.a+'/'+r.b+'/'+r.c+'/'+r.d,r.pA,r.pB,'<b>'+r.pAB+'</b>',r.prod,
            '<span class="'+(r.indep?'ok':'no')+'">'+(r.indep?'○':'×')+'</span>',
            '<span class="'+(r.excl?'ok':'no')+'">'+(r.excl?'○':'×')+'</span>',
            '<span class="'+(r.both?'ok':'no')+'">'+(r.both?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],valid=0,ind=0,exc=0,both=0,bothZero=0,indNotExc=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.zero){ rows.push(['0명','-','-','-','-']); continue; }
      valid++;
      if(r.indep) ind++;
      if(r.excl) exc++;
      if(r.both){ both++; if(!r.possible) bothZero++; }
      if(r.indep&&!r.excl) indNotExc++;
      rows.push([r.a+'/'+r.b+'/'+r.c+'/'+r.d, r.pA+' / '+r.pB, '<b>'+r.pAB+'</b>', r.prod,
                 '<span class="'+(r.indep?'ok':'no')+'">'+(r.indep?'○':'×')+'</span>',
                 '<span class="'+(r.excl?'ok':'no')+'">'+(r.excl?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'독립이었던 기록',big:ind+' / '+valid,p:'P(A∩B) = P(A)P(B) 가 성립한 경우.'},
      {t:'배반이었던 기록',big:exc+' / '+valid,p:'A와 B가 동시에 일어나지 않은 경우(겹치는 칸이 0).'},
      {t:'독립이면서 배반',big:both+'개',
       p:both?('그중 P(A) 또는 P(B)가 0이었던 것 '+bothZero+'개.'):'두 성질이 동시에 성립하려면 한쪽 확률이 0이어야 한다.'}
    ];
    var concl;
    if(ind===0||exc===0){
      concl='<b>더 해 보자</b> — <b>독립인 경우</b>(예: 6/6/9/9)와 <b>배반인 경우</b>(겹치는 칸을 0으로)를 모두 만들어 보자.';
    } else if(both===bothZero){
      concl='<b>정리</b> — 독립과 배반은 <b>전혀 다른 개념</b>이었다. '
           +'배반은 “동시에 일어날 수 없다”(P(A∩B) = 0)이고, 독립은 “한쪽이 일어나도 다른 쪽 확률이 그대로다”(P(A∩B) = P(A)P(B))이다. '
           +'오히려 배반이면 한쪽이 일어난 순간 다른 쪽은 불가능해지므로 <b>강하게 종속</b>이다. '
           +'둘 다 성립하는 것은 한쪽 확률이 0인 경우뿐이었다.';
    } else {
      concl='<b>확인 필요</b> — 독립이면서 배반인데 두 확률이 모두 0이 아닌 기록이 있다.';
    }
    return {head:['네 칸','P(A)/P(B)','P(A∩B)','P(A)P(B)','독립?','배반?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 기댓값
# ============================================================
LAB_EV = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'확률분포 판',
  action:'기댓값 구하기',
  hint0:'값 1, 2, 3, 4 가 나오는 횟수를 정해 보자.',
  sliders:[
    {id:'f1',label:'1이 나오는 횟수',min:0,max:20,value:14,color:'#ef4444',unit:''},
    {id:'f2',label:'2가 나오는 횟수',min:0,max:20,value:3,color:'#f59e0b',unit:''},
    {id:'f3',label:'3이 나오는 횟수',min:0,max:20,value:2,color:'#22c55e',unit:''},
    {id:'f4',label:'4가 나오는 횟수',min:0,max:20,value:1,color:'#3b82f6',unit:''}
  ],
  calc:function(S){
    var f=[S.f1,S.f2,S.f3,S.f4], tot=0, i;
    for(i=0;i<4;i++) tot+=f[i];
    if(tot===0) return {zero:true};
    var p=[],E=0,E2=0;
    for(i=0;i<4;i++){ p.push(f[i]/tot); E+=(i+1)*f[i]/tot; E2+=(i+1)*(i+1)*f[i]/tot; }
    var mode=0;
    for(i=1;i<4;i++){ if(f[i]>f[mode]) mode=i; }
    var acc=0,med=0;
    for(i=0;i<4;i++){ acc+=f[i]; if(acc>=tot/2){ med=i+1; break; } }
    return {zero:false,f:f,tot:tot,p:p,E:E,V:E2-E*E,mode:mode+1,med:med,
            isValue:(Math.abs(E-Math.round(E))<1e-9&&E>=1&&E<=4)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    if(c.zero) return [{k:'전체 0',v:'횟수를 넣자'},{k:'',v:''}];
    return [{k:'기댓값 E(X)',v:ran?r3(c.E):'구해 보자'},
            {k:'가장 자주 나온 값',v:c.mode}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.zero) return '횟수를 넣어 보자.';
    return 'E(X) = '+r3(c.E)+', 최빈값 '+c.mode+', 중앙값 '+c.med+'.  기댓값이 실제 나오는 값인지 확인해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    if(c.zero){ lbl(ctx,'전체 횟수가 0이다',24,200,'#b91c1c',20); return; }
    var COLS=['#ef4444','#f59e0b','#22c55e','#3b82f6'];
    var GX=70, GY=280, BW=70, GH=200;
    var mp=0;
    for(i=0;i<4;i++){ if(c.p[i]>mp) mp=c.p[i]; }
    var grow=(t===null)?0:Math.min(1,t);
    for(i=0;i<4;i++){
      var h=c.p[i]/mp*GH*grow;
      var x=GX+i*BW;
      ctx.fillStyle=COLS[i];ctx.fillRect(x,GY-h,BW-14,h);
      ctx.strokeStyle='#334155';ctx.lineWidth=1.6;ctx.strokeRect(x,GY-h,BW-14,h);
      ctx.fillStyle='#334155';ctx.font='bold 15px sans-serif';ctx.textAlign='center';
      ctx.fillText(i+1,x+(BW-14)/2,GY+22);
      if(grow>=1){
        ctx.fillStyle='#1f2937';ctx.font='bold 12px sans-serif';
        ctx.fillText(r3(c.p[i]),x+(BW-14)/2,GY-h-6);
      }
    }
    ctx.textAlign='left';
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(GX-10,GY);ctx.lineTo(GX+4*BW,GY);ctx.stroke();
    if(grow>=1){
      var ex=GX+(c.E-1)*BW+(BW-14)/2;
      ctx.strokeStyle='#7c3aed';ctx.lineWidth=3;
      ctx.beginPath();ctx.moveTo(ex,GY-GH-14);ctx.lineTo(ex,GY+10);ctx.stroke();
      lbl(ctx,'E(X) = '+r3(c.E),ex+6,GY-GH-18,'#6d28d9',14);
    }
    lbl(ctx,'전체 '+c.tot+'회',24,32,'#1d4ed8',17);
    box(ctx,20,308,400,110);
    lbl(ctx,(t===null)?'기댓값은 어디에 있을까?':('E(X) = '+r3(c.E)+'      분산 '+r3(c.V)),38,340,'#1f2937',18);
    lbl(ctx,'가장 자주 나온 값 '+c.mode+'      가운데 값 '+c.med,38,374,'#52627a',17);
    lbl(ctx,(t===null)?'':(c.isValue?'기댓값이 실제 나오는 값과 같다':'기댓값이 실제로는 나오지 않는 값이다'),
        38,404,c.isValue?'#15803d':'#b91c1c',16);
  },
  record:function(S){
    var c=this.calc(S);
    if(c.zero) return {zero:true};
    return {zero:false,f:c.f.join('/'),tot:c.tot,
            E:r3(c.E),V:r3(c.V),mode:c.mode,med:c.med,
            isValue:c.isValue,
            eqMode:(Math.abs(c.E-c.mode)<1e-9),
            eqMed:(Math.abs(c.E-c.med)<1e-9)};
  },
  headA:['번호','횟수','기댓값','최빈값','기댓값 = 최빈값?','중앙값','기댓값 = 중앙값?','실제 나오는 값?'],
  rowA:function(r,i){
    if(r.zero) return [i+1,'0','-','-','-','-','-','-'];
    return [i+1,r.f,'<b>'+r.E+'</b>',r.mode,
            '<span class="'+(r.eqMode?'ok':'no')+'">'+(r.eqMode?'○':'×')+'</span>',
            r.med,
            '<span class="'+(r.eqMed?'ok':'no')+'">'+(r.eqMed?'○':'×')+'</span>',
            '<span class="'+(r.isValue?'ok':'no')+'">'+(r.isValue?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],valid=0,mode=0,med=0,val=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.zero){ rows.push(['0','-','-','-','-']); continue; }
      valid++;
      if(r.eqMode) mode++;
      if(r.eqMed) med++;
      if(r.isValue) val++;
      rows.push([r.f, '<b>'+r.E+'</b>', r.mode,
                 '<span class="'+(r.eqMode?'ok':'no')+'">'+(r.eqMode?'○':'×')+'</span>',
                 r.med,
                 '<span class="'+(r.eqMed?'ok':'no')+'">'+(r.eqMed?'○':'×')+'</span>',
                 '<span class="'+(r.isValue?'ok':'no')+'">'+(r.isValue?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'기댓값 = 최빈값',big:mode+' / '+valid,p:'가장 자주 나오는 값과 같았는지 확인한 결과.'},
      {t:'기댓값 = 중앙값',big:med+' / '+valid,p:'가운데 값과 같았는지 확인한 결과.'},
      {t:'기댓값이 실제 나오는 값',big:val+' / '+valid,
       p:'기댓값이 1, 2, 3, 4 중 하나였던 경우.'}
    ];
    var concl;
    if(valid===0){
      concl='<b>더 해 보자</b> — 횟수를 넣어야 분포가 만들어진다.';
    } else if(mode<valid||val<valid){
      concl='<b>정리</b> — 기댓값은 <b>가장 자주 나오는 값도, 가운데 값도 아니었다.</b> '
           +'값에 확률을 곱해 모두 더한 <b>무게중심</b>이라서, 한쪽에 큰 값이 조금만 있어도 그쪽으로 끌린다. '
           +'그래서 1, 2, 3, 4 중 어느 것도 아닌 값이 기댓값이 되기도 한다. '
           +'“기대되는 값”이라는 이름 때문에 실제로 나올 값이라고 오해하기 쉽다.';
    } else {
      concl='<b>정리</b> — 지금까지는 기댓값이 실제 값과 일치했다. 한쪽에 치우친 분포도 만들어 보자.';
    }
    return {head:['횟수','기댓값','최빈값','같나?','중앙값','같나?','실제 값?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("hp_repetition_lab.html",
     "뽑기 방식 실험실 — 중복과 순서가 무엇을 바꿀까?",
     "뽑기 방식 실험실 — 중복과 순서가 무엇을 바꿀까?",
     "세 가지 방식으로 모든 경우를 나열해 세고, n^r·nPr·nCr과 대조한다.",
     LAB_REP),
    ("hp_pascal_lab.html",
     "파스칼 삼각형 실험실 — 각 수는 어디서 왔을까?",
     "파스칼 삼각형 실험실 — 각 수는 어디서 왔을까?",
     "삼각형을 한 줄씩 만들며 윗줄 두 수의 합, 좌우 대칭, 한 줄의 합을 확인한다.",
     LAB_PASCAL),
    ("hp_conditional_probability_lab.html",
     "조건부확률 실험실 — P(A|B)와 P(B|A)는 같을까?",
     "조건부확률 실험실 — P(A|B)와 P(B|A)는 같을까?",
     "2×2 표에서 분모가 되는 집단을 바꿔 가며 두 조건부확률을 비교한다.",
     LAB_COND),
    ("hp_independence_lab.html",
     "독립·배반 실험실 — 배반이면 독립일까?",
     "독립·배반 실험실 — 배반이면 독립일까?",
     "네 칸의 인원을 바꿔 가며 독립 조건과 배반 조건이 각각 언제 성립하는지 기록한다.",
     LAB_INDEP),
    ("hp_expected_value_lab.html",
     "기댓값 실험실 — 기댓값은 실제로 나오는 값일까?",
     "기댓값 실험실 — 기댓값은 실제로 나오는 값일까?",
     "확률분포를 바꿔 가며 기댓값·최빈값·중앙값을 함께 구해 비교한다.",
     LAB_EV),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c29_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
