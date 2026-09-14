# -*- coding: utf-8 -*-
"""고등 공통수학1 실험 5종 (2)"""
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
function sgc(v,s){ if(v===0) return ''; return (v<0)?(' − '+(-v)+s):(' + '+v+s); }
"""

# ============================================================
# 1. 산술평균과 기하평균
# ============================================================
LAB_AMGM = BASE + r"""
var LAB = {
  cw:440, ch:400, cvTitle:'반원 모델판',
  action:'반원을 그려 비교하기',
  hint0:'두 양수를 정하고, 산술평균과 기하평균을 길이로 비교해 보자.',
  sliders:[
    {id:'a',label:'a',min:1,max:20,value:4,color:'#2563eb',unit:''},
    {id:'b',label:'b',min:1,max:20,value:16,color:'#16a34a',unit:''}
  ],
  calc:function(S){
    var am=(S.a+S.b)/2, gm=Math.sqrt(S.a*S.b);
    return {am:am,gm:gm,gap:am-gm,eq:(Math.abs(am-gm)<1e-12)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'산술평균 (a+b)/2',v:r3(c.am)},
            {k:'기하평균 √(ab)',v:ran?r3(c.gm):'그려 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '산술평균 '+r3(c.am)+', 기하평균 '+r3(c.gm)+'.  차이 '+r3(c.gap)+'.  '+(c.eq?'두 값이 같다 (a = b).':'산술평균이 더 크다.')+' 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    var U=Math.min(11, 340/(S.a+S.b));
    var X0=50, Y=270;
    var A=X0, B=X0+(S.a+S.b)*U, M=X0+(S.a+S.b)/2*U, P=X0+S.a*U;
    ctx.strokeStyle='#334155';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(A,Y);ctx.lineTo(B,Y);ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    ctx.beginPath();ctx.arc(M,Y,c.am*U,Math.PI,Math.PI+Math.PI*grow);
    ctx.strokeStyle='#94a3b8';ctx.lineWidth=2.5;ctx.stroke();
    ctx.strokeStyle='#2563eb';ctx.lineWidth=4;
    ctx.beginPath();ctx.moveTo(A,Y+10);ctx.lineTo(P,Y+10);ctx.stroke();
    ctx.strokeStyle='#16a34a';ctx.lineWidth=4;
    ctx.beginPath();ctx.moveTo(P,Y+10);ctx.lineTo(B,Y+10);ctx.stroke();
    lbl(ctx,'a = '+S.a,(A+P)/2,Y+30,'#1d4ed8',14,'center');
    lbl(ctx,'b = '+S.b,(P+B)/2,Y+30,'#15803d',14,'center');
    if(grow>=1){
      ctx.strokeStyle='#dc2626';ctx.lineWidth=4;
      ctx.beginPath();ctx.moveTo(P,Y);ctx.lineTo(P,Y-c.gm*U);ctx.stroke();
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=3;
      ctx.beginPath();ctx.moveTo(M,Y);ctx.lineTo(M,Y-c.am*U);ctx.stroke();
      lbl(ctx,'√(ab) = '+r2(c.gm),P+8,Y-c.gm*U-8,'#b91c1c',14);
      lbl(ctx,'반지름 = '+r2(c.am),M+8,Y-c.am*U-8,'#b45309',14);
    }
    lbl(ctx,'지름이 a+b 인 반원. 반지름과 수선의 길이를 비교',24,34,'#52627a',15);
    box(ctx,20,300,400,84);
    lbl(ctx,(t===null)?'어느 쪽이 더 클까?':('산술평균 '+r3(c.am)+'      기하평균 '+r3(c.gm)),38,332,'#1f2937',19);
    lbl(ctx,(t===null)?'':('차이 '+r3(c.gap)+'   '+(c.eq?'(a = b 이라 같다)':'(산술평균이 더 크다)')),38,366,c.eq?'#b45309':'#15803d',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,am:r3(c.am),gm:r3(c.gm),gap:r3(c.gap),
            eq:c.eq,ge:(c.am>=c.gm-1e-12),same:(S.a===S.b)};
  },
  headA:['번호','a, b','산술평균','기하평균','차이','산술 ≥ 기하?','a = b?'],
  rowA:function(r,i){
    return [i+1,r.a+', '+r.b,'<b>'+r.am+'</b>',r.gm,r.gap,
            '<span class="'+(r.ge?'ok':'no')+'">'+(r.ge?'○':'×')+'</span>',
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ge=0,eq=0,eqSame=0,mn=999,mnP='';
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.ge) ge++;
      if(r.eq){ eq++; if(r.same) eqSame++; }
      if(r.gap<mn){ mn=r.gap; mnP=r.a+', '+r.b; }
      rows.push([r.a+', '+r.b, r.am, r.gm, r.gap,
                 '<span class="'+(r.ge?'ok':'no')+'">'+(r.ge?'○':'×')+'</span>',
                 '<span class="'+(r.eq?'ok':'no')+'">'+(r.eq?'○':'×')+'</span>',
                 r.same?'○':'×']);
    }
    var stats=[
      {t:'산술평균 ≥ 기하평균',big:ge+' / '+rec.length,p:'예외가 있었는지 확인한 결과.'},
      {t:'두 값이 같았던 횟수',big:eq+' / '+rec.length,
       p:eq?('그중 a = b 였던 것 '+eqSame+'개.'):'a와 b를 같게 해 보자.'},
      {t:'차이가 가장 작았던 경우',big:mn+'',p:mnP?('a, b = '+mnP):''}
    ];
    var concl;
    if(eq===0){
      concl='<b>더 해 보자</b> — a와 b를 <b>같은 값</b>으로도 해 보자. 그때 두 평균이 어떻게 되는지가 핵심이다.';
    } else if(ge===rec.length&&eq===eqSame){
      concl='<b>정리</b> — 산술평균이 기하평균보다 작았던 적은 <b>한 번도 없었고</b>, 두 값이 같아진 것은 <b>a = b일 때뿐</b>이었다. '
           +'반원에서 보면 산술평균은 반지름, 기하평균은 지름 위 한 점에서 세운 수선의 길이다. '
           +'수선은 아무리 길어도 반지름을 넘을 수 없고, 정중앙일 때만 반지름과 같아진다. '
           +'그래서 a + b ≥ 2√(ab) (등호는 a = b일 때)이다.';
    } else {
      concl='<b>확인 필요</b> — 부등호가 어긋난 기록이 있다.';
    }
    return {head:['a, b','산술평균','기하평균','차이','산술≥기하?','같은가?','a=b?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 순열과 조합
# ============================================================
LAB_PERM = BASE + r"""
function fact(n){ var v=1,i; for(i=2;i<=n;i++) v*=i; return v; }
var LAB = {
  cw:440, ch:430, cvTitle:'뽑기 세기판',
  action:'모두 나열해 세기',
  hint0:'전체 개수와 뽑는 개수를 정해 보자.',
  sliders:[
    {id:'n',label:'전체 개수 n',min:2,max:8,value:4,color:'#2563eb',unit:''},
    {id:'r',label:'뽑는 개수 r',min:1,max:4,value:2,color:'#16a34a',unit:''}
  ],
  calc:function(S){
    var r=Math.min(S.r,S.n);
    var perms=[],combs=[];
    function rec(cur,used){
      if(cur.length===r){ perms.push(cur.slice()); return; }
      for(var i=0;i<S.n;i++){
        if(used[i]) continue;
        used[i]=1; cur.push(i); rec(cur,used); cur.pop(); used[i]=0;
      }
    }
    rec([],[]);
    function rec2(start,cur){
      if(cur.length===r){ combs.push(cur.slice()); return; }
      for(var i=start;i<S.n;i++){ cur.push(i); rec2(i+1,cur); cur.pop(); }
    }
    rec2(0,[]);
    return {r:r,P:perms.length,C:combs.length,perms:perms,combs:combs,
            fr:fact(r),ratio:perms.length/combs.length};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'순서를 따질 때',v:ran?(c.P+'가지'):'세어 보자'},
            {k:'순서를 안 따질 때',v:ran?(c.C+'가지'):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '순열 '+c.P+'가지, 조합 '+c.C+'가지.  '+c.P+' ÷ '+c.C+' = '+c.ratio+' 이고 '+c.r+'! = '+c.fr+'이다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var NAMES=['A','B','C','D','E','F','G','H'];
    var shown=(t===null)?0:Math.ceil(Math.min(1,t)*c.P);
    lbl(ctx,'서로 다른 '+S.n+'개에서 '+c.r+'개 뽑기',24,34,'#1d4ed8',18);
    lbl(ctx,'순서를 따지면 (순열)',24,66,'#b91c1c',16);
    var perRow=Math.max(4,Math.floor(400/((c.r*16)+22)));
    var cw2=Math.floor(392/perRow);
    for(i=0;i<c.P&&i<60;i++){
      var x=24+(i%perRow)*cw2, y=84+Math.floor(i/perRow)*22;
      if(y>210) break;
      var s='';
      for(var j=0;j<c.r;j++) s+=NAMES[c.perms[i][j]];
      ctx.fillStyle=(i<shown)?'#b91c1c':'#e2e8f0';
      ctx.font='bold 14px sans-serif';ctx.textAlign='left';
      ctx.fillText(s,x,y);
    }
    if(c.P>60) lbl(ctx,'... 등 모두 '+c.P+'가지',24,214,'#94a3b8',14);
    lbl(ctx,'순서를 안 따지면 (조합)',24,244,'#15803d',16);
    for(i=0;i<c.C&&i<40;i++){
      var x2=24+(i%perRow)*cw2, y2=262+Math.floor(i/perRow)*22;
      if(y2>320) break;
      var s2='';
      for(var j2=0;j2<c.r;j2++) s2+=NAMES[c.combs[i][j2]];
      ctx.fillStyle=(shown>=c.P)?'#15803d':'#e2e8f0';
      ctx.font='bold 14px sans-serif';
      ctx.fillText(s2,x2,y2);
    }
    if(c.C>40) lbl(ctx,'... 등 모두 '+c.C+'가지',24,326,'#94a3b8',14);
    box(ctx,20,338,400,80);
    lbl(ctx,(t===null)?'두 수는 어떤 관계일까?':('순열 '+c.P+'가지      조합 '+c.C+'가지'),38,370,'#1f2937',19);
    lbl(ctx,(t===null)?'':('순열 ÷ 조합 = '+c.ratio+'      '+c.r+'! = '+c.fr),38,402,'#15803d',18);
  },
  record:function(S){
    var c=this.calc(S);
    return {n:S.n,r:c.r,P:c.P,C:c.C,ratio:c.ratio,fr:c.fr,
            ok:(c.ratio===c.fr),
            same:(c.P===c.C),one:(c.r===1)};
  },
  headA:['번호','n','r','순열','조합','순열÷조합','r!','같은가?'],
  rowA:function(r,i){
    return [i+1,r.n,r.r,'<b>'+r.P+'</b>',r.C,r.ratio,r.fr,
            '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ok=0,same=0,sameOne=0,rs={},rn=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.ok) ok++;
      if(r.same){ same++; if(r.one) sameOne++; }
      if(!rs[r.r]){ rs[r.r]=true; rn++; }
      rows.push([r.n+' 중 '+r.r+'개', '<b>'+r.P+'</b>', r.C, r.ratio, r.fr,
                 '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'순열 ÷ 조합 = r!',big:ok+' / '+rec.length,
       p:'직접 나열해 센 두 수의 비를 r!과 비교한 결과.'},
      {t:'두 값이 같았던 횟수',big:same+' / '+rec.length,
       p:same?('그중 r = 1이었던 것 '+sameOne+'개. 한 개만 뽑으면 순서가 의미 없다.'):'r = 1로도 해 보자.'},
      {t:'시험한 r',big:rn+'가지',p:'r이 커질수록 두 수의 차이가 커진다.'}
    ];
    var concl;
    if(rn<2){
      concl='<b>더 해 보자</b> — r을 1, 2, 3으로 바꿔 가며 기록해야 관계가 보인다.';
    } else if(ok===rec.length){
      concl='<b>정리</b> — 같은 것을 뽑아도 <b>순서를 따지느냐</b>에 따라 가짓수가 달랐고, 그 비는 언제나 <b>r!</b>이었다. '
           +'조합 하나마다 그 r개를 늘어놓는 방법이 r!가지씩 있기 때문이다. 그래서 nPr = nCr × r! 이다. '
           +'r = 1일 때만 둘이 같아진다. 문제에서 <b>“순서가 결과를 바꾸는가”</b>를 먼저 판단해야 한다.';
    } else {
      concl='<b>확인 필요</b> — 나열해 센 수와 계산이 어긋난 기록이 있다.';
    }
    return {head:['뽑기','순열','조합','비','r!','같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. 이차부등식
# ============================================================
LAB_INEQ2 = BASE + r"""
var DIRS=['> 0 (양수)','< 0 (음수)'];
var LAB = {
  cw:440, ch:430, cvTitle:'이차부등식 판',
  action:'그래프에서 해 찾기',
  hint0:'계수와 부등호 방향을 정하고, 그래프에서 조건을 만족하는 구간을 보자.',
  sliders:[
    {id:'a',label:'a',min:-3,max:3,value:1,color:'#2563eb',unit:''},
    {id:'b',label:'b',min:-8,max:8,value:-2,color:'#16a34a',unit:''},
    {id:'c',label:'c',min:-8,max:8,value:-3,color:'#f59e0b',unit:''},
    {id:'dir',label:'부등호',min:0,max:1,value:0,color:'#dc2626',fmt:function(v){return DIRS[v];}}
  ],
  f:function(S,x){ return S.a*x*x+S.b*x+S.c; },
  calc:function(S){
    if(S.a===0) return {zero:true};
    var D=S.b*S.b-4*S.a*S.c;
    var x1=null,x2=null;
    if(D>=0){ var s=Math.sqrt(D); x1=(-S.b-s)/(2*S.a); x2=(-S.b+s)/(2*S.a); if(x1>x2){var tmp=x1;x1=x2;x2=tmp;} }
    var kind;
    var pos=(S.dir===0);
    if(D>1e-9){
      if((S.a>0)===pos) kind='두 근의 바깥';
      else kind='두 근의 사이';
    } else if(D<-1e-9){
      kind=((S.a>0)===pos)?'모든 실수':'해 없음';
    } else {
      kind=((S.a>0)===pos)?'중근을 뺀 모든 실수':'해 없음';
    }
    var hit=0,i;
    for(i=-100;i<=100;i++){
      var x=i/10, y=this.f(S,x);
      if(pos?(y>0):(y<0)) hit++;
    }
    return {zero:false,D:D,x1:x1,x2:x2,kind:kind,hit:hit,pos:pos};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    if(c.zero) return [{k:'a = 0',v:'이차부등식이 아니다'},{k:'',v:'a를 바꾸자'}];
    return [{k:'부등식',v:S.a+'x²'+sgc(S.b,'x')+sg(S.c)+' '+DIRS[S.dir].split(' ')[0]+' 0'},
            {k:'해의 모양',v:ran?c.kind:'찾아보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.zero) return 'a가 0이면 이차부등식이 아니다.';
    return '해는 「'+c.kind+'」이다. −10에서 10까지 201개 점 중 '+c.hit+'개가 조건을 만족했다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var CX=220, CY=250, U=22;
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=-9;i<=9;i++){ ctx.beginPath();ctx.moveTo(CX+i*U,CY-8*U);ctx.lineTo(CX+i*U,CY+4*U);ctx.stroke(); }
    for(i=-4;i<=8;i++){ ctx.beginPath();ctx.moveTo(CX-9*U,CY-i*U);ctx.lineTo(CX+9*U,CY-i*U);ctx.stroke(); }
    if(c.zero){ lbl(ctx,'a = 0 이면 이차부등식이 아니다',24,38,'#b91c1c',19); return; }
    var grow=(t===null)?0:Math.min(1,t);
    if(grow>0){
      ctx.fillStyle=c.pos?'rgba(34,197,94,0.18)':'rgba(239,68,68,0.16)';
      for(i=-90;i<=90;i++){
        var x=i/10, y=this.f(S,x);
        var okv=c.pos?(y>0):(y<0);
        if(okv) ctx.fillRect(CX+x*U-1.2,CY-8*U,2.4,12*U);
      }
    }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(CX-9*U,CY);ctx.lineTo(CX+9*U,CY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(CX,CY-8*U);ctx.lineTo(CX,CY+4*U);ctx.stroke();
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    var st=false;
    for(i=-90;i<=90;i++){
      var xx=i/10, yy=this.f(S,xx);
      if(yy<-4||yy>8){ st=false; continue; }
      if(!st){ ctx.moveTo(CX+xx*U,CY-yy*U); st=true; } else ctx.lineTo(CX+xx*U,CY-yy*U);
    }
    ctx.stroke();
    if(grow>=1&&c.x1!==null){
      [c.x1,c.x2].forEach(function(x){
        if(Math.abs(x)>9) return;
        ctx.beginPath();ctx.arc(CX+x*U,CY,7,0,Math.PI*2);
        ctx.fillStyle='#f59e0b';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
        lbl(ctx,r2(x),CX+x*U,CY+24,'#b45309',13,'center');
      });
    }
    lbl(ctx,S.a+'x²'+sgc(S.b,'x')+sg(S.c)+'  '+DIRS[S.dir].split(' ')[0]+'  0',24,32,'#1d4ed8',18);
    box(ctx,20,344,400,74);
    lbl(ctx,(t===null)?'어느 구간이 해일까?':('해 : '+c.kind),38,376,'#1f2937',20);
    lbl(ctx,(t===null)?'':('a = '+S.a+' ('+((S.a>0)?'아래로 볼록':'위로 볼록')+')   판별식 '+c.D),38,406,'#52627a',17);
  },
  record:function(S){
    var c=this.calc(S);
    if(c.zero) return {zero:true};
    return {zero:false,a:S.a,b:S.b,c:S.c,dir:S.dir,dirName:DIRS[S.dir].split(' ')[0],
            D:c.D,kind:c.kind,hit:c.hit,
            x1:(c.x1===null)?'-':r2(c.x1),x2:(c.x2===null)?'-':r2(c.x2),
            between:(c.kind==='두 근의 사이'),
            aPos:(S.a>0)};
  },
  headA:['번호','부등식','a의 부호','판별식','두 근','해의 모양','만족한 점'],
  rowA:function(r,i){
    if(r.zero) return [i+1,'a=0','-','-','-','-','-'];
    return [i+1,r.a+'x²'+sgc(r.b,'x')+sg(r.c)+' '+r.dirName+' 0',(r.aPos?'양수':'음수'),r.D,
            (r.x1==='-')?'없음':(r.x1+', '+r.x2),'<b>'+r.kind+'</b>',r.hit+' / 201'];
  },
  analyze:function(rec){
    var rows=[],valid=0,kinds={},kn=0,g={},match=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.zero){ rows.push(['a=0','-','-','-','-']); continue; }
      valid++;
      if(!kinds[r.kind]){ kinds[r.kind]=true; kn++; }
      var expect;
      if(r.D>1e-9) expect=((r.aPos)===(r.dir===0))?'두 근의 바깥':'두 근의 사이';
      else expect=null;
      if(expect===null||expect===r.kind) match++;
      var key=(r.aPos?'a>0':'a<0')+' , '+r.dirName;
      if(!g[key]) g[key]=r.kind;
      rows.push([r.a+'x²'+sgc(r.b,'x')+sg(r.c)+' '+r.dirName+' 0', (r.aPos?'양수':'음수'), r.D,
                 (r.x1==='-')?'없음':(r.x1+', '+r.x2), '<b>'+r.kind+'</b>']);
    }
    var lines=[],k;
    for(k in g){ lines.push(k+' → '+g[k]); }
    var stats=[
      {t:'나타난 해의 모양',big:kn+'가지',p:Object.keys(kinds).join(', ')},
      {t:'a의 부호와 부등호 조합',big:lines.length+'가지',p:lines.join(' / ')},
      {t:'판별식이 양수인 기록에서 예상과 일치',big:match+' / '+valid,
       p:'a의 부호와 부등호 방향만으로 “사이/바깥”을 맞힐 수 있는지 확인한 결과.'}
    ];
    var concl;
    if(lines.length<3){
      concl='<b>더 해 보자</b> — a가 양수·음수인 경우와 부등호 두 방향을 <b>모두 조합해</b> 기록해야 규칙이 보인다.';
    } else {
      concl='<b>정리</b> — 해가 “두 근 사이”인지 “바깥”인지는 부등호 방향만으로 정해지지 않았다. '
           +'<b>a의 부호와 부등호 방향을 함께</b> 봐야 한다. a > 0이고 &lt; 0 이면 두 근 사이, a > 0이고 &gt; 0 이면 바깥이고, '
           +'a가 음수면 반대가 된다. 판별식이 음수면 해가 모든 실수이거나 아예 없었다. '
           +'외우지 말고 <b>그래프가 x축 위에 있는지 아래에 있는지</b>를 보면 된다.';
    }
    return {head:['부등식','a','판별식','두 근','해의 모양'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 삼차방정식의 근과 계수
# ============================================================
LAB_CUBIC = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'삼차식 판',
  action:'전개하고 비교하기',
  hint0:'세 근을 정하면 삼차식이 만들어진다. 계수와 근의 관계를 보자.',
  sliders:[
    {id:'p',label:'첫 번째 근',min:-4,max:4,value:-1,color:'#2563eb',unit:''},
    {id:'q',label:'두 번째 근',min:-4,max:4,value:2,color:'#16a34a',unit:''},
    {id:'r',label:'세 번째 근',min:-4,max:4,value:3,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var b=-(S.p+S.q+S.r);
    var c=S.p*S.q+S.q*S.r+S.r*S.p;
    var d=-(S.p*S.q*S.r);
    return {b:b,c:c,d:d,sum:S.p+S.q+S.r,pair:c,prod:S.p*S.q*S.r};
  },
  f:function(S,x){ var c=this.calc(S); return x*x*x+c.b*x*x+c.c*x+c.d; },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'세 근',v:S.p+', '+S.q+', '+S.r},
            {k:'전개한 식',v:ran?('x³'+sgc(c.b,'x²')+sgc(c.c,'x')+sg(c.d)):'전개해 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return '전개하면 x³'+sgc(c.b,'x²')+sgc(c.c,'x')+sg(c.d)+' 이다. 근의 합 '+c.sum+'과 −b, 곱 '+c.prod+'와 −d를 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    var CX=220, CY=230, U=26;
    ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
    for(i=-6;i<=6;i++){ ctx.beginPath();ctx.moveTo(CX+i*U,CY-5*U);ctx.lineTo(CX+i*U,CY+5*U);ctx.stroke(); }
    for(i=-5;i<=5;i++){ ctx.beginPath();ctx.moveTo(CX-6*U,CY+i*U);ctx.lineTo(CX+6*U,CY+i*U);ctx.stroke(); }
    ctx.strokeStyle='#334155';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(CX-6*U,CY);ctx.lineTo(CX+6*U,CY);ctx.stroke();
    ctx.beginPath();ctx.moveTo(CX,CY-5*U);ctx.lineTo(CX,CY+5*U);ctx.stroke();
    var grow=(t===null)?0:Math.min(1,t);
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;ctx.beginPath();
    var st=false;
    for(i=-60;i<=60;i++){
      var xx=i/10, yy=this.f(S,xx)/4;
      if(yy<-5||yy>5){ st=false; continue; }
      if(!st){ ctx.moveTo(CX+xx*U,CY-yy*U); st=true; } else ctx.lineTo(CX+xx*U,CY-yy*U);
    }
    if(grow>0) ctx.stroke();
    if(grow>=1){
      [S.p,S.q,S.r].forEach(function(x){
        if(Math.abs(x)>6) return;
        ctx.beginPath();ctx.arc(CX+x*U,CY,7,0,Math.PI*2);
        ctx.fillStyle='#dc2626';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      });
    }
    lbl(ctx,'(x'+sg(-S.p)+')(x'+sg(-S.q)+')(x'+sg(-S.r)+') = 0',24,32,'#1d4ed8',17);
    lbl(ctx,'(그래프는 세로를 1/4로 줄여 그림)',24,56,'#94a3b8',13);
    box(ctx,20,368,400,50);
    lbl(ctx,(t===null)?'전개하면 어떤 식이 될까?':('x³'+sgc(c.b,'x²')+sgc(c.c,'x')+sg(c.d)),38,400,'#1f2937',20);
  },
  record:function(S){
    var c=this.calc(S);
    return {p:S.p,q:S.q,r:S.r,b:c.b,c:c.c,d:c.d,
            sum:c.sum,pair:c.pair,prod:c.prod,
            sOk:(c.sum===-c.b),pOk:(c.pair===c.c),prOk:(c.prod===-c.d)};
  },
  headA:['번호','세 근','전개한 식','근의 합','−b','같나?','두 개씩 곱의 합','c','같나?','세 근의 곱','−d','같나?'],
  rowA:function(r,i){
    return [i+1,r.p+', '+r.q+', '+r.r,'x³'+sgc(r.b,'x²')+sgc(r.c,'x')+sg(r.d),
            '<b>'+r.sum+'</b>',-r.b,
            '<span class="'+(r.sOk?'ok':'no')+'">'+(r.sOk?'○':'×')+'</span>',
            r.pair,r.c,
            '<span class="'+(r.pOk?'ok':'no')+'">'+(r.pOk?'○':'×')+'</span>',
            r.prod,-r.d,
            '<span class="'+(r.prOk?'ok':'no')+'">'+(r.prOk?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],s=0,p=0,pr=0,dup=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.sOk) s++;
      if(r.pOk) p++;
      if(r.prOk) pr++;
      if(r.p===r.q||r.q===r.r||r.p===r.r) dup++;
      rows.push([r.p+', '+r.q+', '+r.r, 'x³'+sgc(r.b,'x²')+sgc(r.c,'x')+sg(r.d),
                 r.sum+' / '+(-r.b),
                 '<span class="'+(r.sOk?'ok':'no')+'">'+(r.sOk?'○':'×')+'</span>',
                 r.pair+' / '+r.c,
                 '<span class="'+(r.pOk?'ok':'no')+'">'+(r.pOk?'○':'×')+'</span>',
                 r.prod+' / '+(-r.d),
                 '<span class="'+(r.prOk?'ok':'no')+'">'+(r.prOk?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'세 근의 합 = −b',big:s+' / '+rec.length,p:'x² 계수의 부호를 바꾼 값과 비교했다.'},
      {t:'두 개씩 곱의 합 = c',big:p+' / '+rec.length,p:'x 계수와 비교했다.'},
      {t:'세 근의 곱 = −d',big:pr+' / '+rec.length,
       p:dup?('중근이 있는 기록 '+dup+'개도 포함했다.'):'중근이 있는 경우도 해 보자.'}
    ];
    var concl;
    if(s===rec.length&&p===rec.length&&pr===rec.length){
      concl='<b>정리</b> — 세 근을 전개해 만든 삼차식에서 <b>근의 합은 −b, 두 개씩 곱한 것의 합은 c, 세 근의 곱은 −d</b>였다. '
           +'예외는 없었다. 이차식에서 본 근과 계수의 관계가 차수가 올라가도 같은 방식으로 이어진다. '
           +'전개 과정을 보면 x²의 계수는 근들이 하나씩 빠지며 더해진 것이고, 상수항은 근을 모두 곱한 것에 부호가 붙은 것이다.';
    } else {
      concl='<b>확인 필요</b> — 근과 계수의 관계가 어긋난 기록이 있다.';
    }
    return {head:['세 근','전개한 식','합 / −b','같나?','두 곱의 합 / c','같나?','곱 / −d','같나?'],
            rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 5. 행렬의 곱셈
# ============================================================
LAB_MAT = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'행렬 곱셈판',
  action:'AB 와 BA 계산하기',
  hint0:'두 행렬의 성분을 정하고, 곱하는 순서를 바꿔 보자.',
  sliders:[
    {id:'a',label:'A의 (1,1)',min:-3,max:3,value:1,color:'#2563eb',unit:''},
    {id:'b',label:'A의 (1,2)',min:-3,max:3,value:2,color:'#60a5fa',unit:''},
    {id:'c',label:'B의 (1,1)',min:-3,max:3,value:0,color:'#dc2626',unit:''},
    {id:'d',label:'B의 (1,2)',min:-3,max:3,value:1,color:'#f87171',unit:''}
  ],
  calc:function(S){
    var A=[[S.a,S.b],[1,2]];
    var B=[[S.c,S.d],[2,1]];
    function mul(X,Y){
      var Z=[[0,0],[0,0]],i,j,k;
      for(i=0;i<2;i++)for(j=0;j<2;j++){ var s=0; for(k=0;k<2;k++) s+=X[i][k]*Y[k][j]; Z[i][j]=s; }
      return Z;
    }
    var AB=mul(A,B), BA=mul(B,A);
    var same=(AB[0][0]===BA[0][0]&&AB[0][1]===BA[0][1]&&AB[1][0]===BA[1][0]&&AB[1][1]===BA[1][1]);
    return {A:A,B:B,AB:AB,BA:BA,same:same};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'AB',v:ran?('['+c.AB[0][0]+' '+c.AB[0][1]+' ; '+c.AB[1][0]+' '+c.AB[1][1]+']'):'계산해 보자'},
            {k:'BA',v:ran?('['+c.BA[0][0]+' '+c.BA[0][1]+' ; '+c.BA[1][0]+' '+c.BA[1][1]+']'):'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'AB 와 BA 를 계산했다. 두 결과가 '+(c.same?'같다':'다르다')+'. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    function mat(x,y,M,col,name,show){
      lbl(ctx,name,x-24,y+34,col,20);
      ctx.strokeStyle=col;ctx.lineWidth=2.5;
      ctx.beginPath();ctx.moveTo(x+6,y);ctx.lineTo(x,y);ctx.lineTo(x,y+66);ctx.lineTo(x+6,y+66);
      ctx.moveTo(x+72,y);ctx.lineTo(x+78,y);ctx.lineTo(x+78,y+66);ctx.lineTo(x+72,y+66);
      ctx.stroke();
      ctx.font='bold 18px sans-serif';ctx.textAlign='center';
      var i,j;
      for(i=0;i<2;i++)for(j=0;j<2;j++){
        ctx.fillStyle=show?'#1f2937':'#cbd5e1';
        ctx.fillText(show?M[i][j]:'?',x+22+j*36,y+24+i*30);
      }
      ctx.textAlign='left';
    }
    var show=(t===null)?0:Math.min(1,t);
    mat(70,70,c.A,'#2563eb','A',true);
    mat(240,70,c.B,'#dc2626','B',true);
    mat(70,200,c.AB,'#7c3aed','AB',show>0.4);
    mat(240,200,c.BA,'#059669','BA',show>=1);
    lbl(ctx,'곱하는 순서를 바꾸면?',24,34,'#1d4ed8',18);
    box(ctx,20,300,400,110);
    if(show>=1){
      lbl(ctx,'AB = ['+c.AB[0][0]+' '+c.AB[0][1]+' ; '+c.AB[1][0]+' '+c.AB[1][1]+']',38,336,'#6d28d9',19);
      lbl(ctx,'BA = ['+c.BA[0][0]+' '+c.BA[0][1]+' ; '+c.BA[1][0]+' '+c.BA[1][1]+']',38,368,'#047857',19);
      lbl(ctx,c.same?'두 결과가 같다':'두 결과가 다르다',38,398,c.same?'#b45309':'#b91c1c',18);
    } else {
      lbl(ctx,'AB 와 BA 는 같을까?',38,344,'#1f2937',20);
      lbl(ctx,'A의 (2,1),(2,2)는 1, 2 / B의 (2,1),(2,2)는 2, 1 로 고정',38,378,'#52627a',15);
    }
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,c:S.c,d:S.d,
            AB:'['+c.AB[0][0]+' '+c.AB[0][1]+' ; '+c.AB[1][0]+' '+c.AB[1][1]+']',
            BA:'['+c.BA[0][0]+' '+c.BA[0][1]+' ; '+c.BA[1][0]+' '+c.BA[1][1]+']',
            same:c.same,
            zeroA:(S.a===0&&S.b===0)};
  },
  headA:['번호','A의 1행','B의 1행','AB','BA','같은가?'],
  rowA:function(r,i){
    return [i+1,'('+r.a+', '+r.b+')','('+r.c+', '+r.d+')','<b>'+r.AB+'</b>',r.BA,
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],same=0,diff=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++; else diff++;
      rows.push(['('+r.a+', '+r.b+') / ('+r.c+', '+r.d+')', r.AB, r.BA,
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'AB = BA 였던 횟수',big:same+' / '+rec.length,
       p:'곱하는 순서를 바꿔도 같았던 기록 수.'},
      {t:'달랐던 횟수',big:diff+'개',
       p:diff?'행렬 곱셈에는 교환법칙이 성립하지 않는다.':'성분을 바꿔 다른 결과가 나오게 해 보자.'},
      {t:'기록 수',big:rec.length+'개',p:'우연히 같아지는 조합도 있다.'}
    ];
    var concl;
    if(diff===0){
      concl='<b>더 해 보자</b> — 아직 AB와 BA가 다른 경우를 못 만났다. 성분을 여러 가지로 바꿔 보자.';
    } else if(same>0){
      concl='<b>정리</b> — AB와 BA가 <b>다른 경우가 '+diff+'번</b> 나왔다. 수의 곱셈과 달리 행렬 곱셈에는 <b>교환법칙이 성립하지 않는다</b>. '
           +'같아진 경우도 '+same+'번 있었지만 그것은 특별한 조합일 뿐, 일반적으로 성립하는 성질이 아니다. '
           +'행렬 계산에서 (A+B)² = A² + 2AB + B² 같은 전개를 함부로 쓰면 안 되는 이유다.';
    } else {
      concl='<b>정리</b> — 기록한 모든 경우에서 AB ≠ BA 였다. 행렬 곱셈에는 교환법칙이 성립하지 않는다. '
           +'우연히 같아지는 조합이 있는지도 찾아보자.';
    }
    return {head:['A / B 의 1행','AB','BA','같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("h1_am_gm_lab_CommonMath1.html",
     "평균 부등식 실험실 — 산술평균과 기하평균 중 어느 쪽이 클까?",
     "평균 부등식 실험실 — 산술평균과 기하평균 중 어느 쪽이 클까?",
     "지름이 a+b인 반원에서 반지름과 수선의 길이를 비교하며 두 평균의 관계를 기록한다.",
     LAB_AMGM),
    ("h1_permutation_combination_lab_CommonMath1_PermComb_Ep05.html",
     "뽑기 실험실 — 순서를 따지면 몇 배가 될까?",
     "뽑기 실험실 — 순서를 따지면 몇 배가 될까?",
     "실제로 모든 경우를 나열해 순열과 조합의 수를 세고, 두 수의 비를 확인한다.",
     LAB_PERM),
    ("h1_quadratic_inequality_lab_CommonMath1_Quad_Ep07.html",
     "이차부등식 실험실 — 해는 두 근 사이일까 바깥일까?",
     "이차부등식 실험실 — 해는 두 근 사이일까 바깥일까?",
     "a의 부호와 부등호 방향을 조합해 가며 그래프에서 조건을 만족하는 구간을 기록한다.",
     LAB_INEQ2),
    ("h1_cubic_roots_lab_CommonMath1_Complex_Ep06.html",
     "삼차식 실험실 — 근과 계수의 관계는 이어질까?",
     "삼차식 실험실 — 근과 계수의 관계는 이어질까?",
     "세 근으로 삼차식을 만들어 전개하고, 근의 합·곱과 계수를 대조한다.",
     LAB_CUBIC),
    ("h1_matrix_product_lab_CommonMath1_Matrix_Ep05.html",
     "행렬 실험실 — AB와 BA는 같을까?",
     "행렬 실험실 — AB와 BA는 같을까?",
     "두 행렬의 성분을 바꿔 가며 곱하는 순서에 따라 결과가 어떻게 달라지는지 기록한다.",
     LAB_MAT),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c22_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
