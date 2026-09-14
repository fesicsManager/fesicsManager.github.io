# -*- coding: utf-8 -*-
"""중2 ③ 일차함수 4종"""
import os, re

OUT = "/mnt/user-data/outputs"
src = open("/home/claude/gen_math_labs.py", encoding="utf-8").read()
TPL = re.search(r'TPL = r"""(.*?)"""\n', src, re.S).group(1)

BASE = r"""
function lbl(ctx,t,x,y,c,sz,al){ctx.fillStyle=c;ctx.font='bold '+(sz||18)+'px sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);}
function box(ctx,x,y,w,h){ctx.fillStyle='#f1f6fd';ctx.fillRect(x,y,w,h);ctx.strokeStyle='#c7d8ee';ctx.lineWidth=2;ctx.strokeRect(x,y,w,h);}
function r1(v){return Math.round(v*10)/10;}
function r2(v){return Math.round(v*100)/100;}
function eqStr(a,b){ return 'y = '+a+'x'+((b===0)?'':((b<0)?(' − '+(-b)):(' + '+b))); }
var CX=220, CY=200, U=20;
function grid(ctx,xr,yr){
  var i;
  ctx.strokeStyle='#eef2f7';ctx.lineWidth=1;
  for(i=-xr;i<=xr;i++){ ctx.beginPath();ctx.moveTo(CX+i*U,CY-yr*U);ctx.lineTo(CX+i*U,CY+yr*U);ctx.stroke(); }
  for(i=-yr;i<=yr;i++){ ctx.beginPath();ctx.moveTo(CX-xr*U,CY+i*U);ctx.lineTo(CX+xr*U,CY+i*U);ctx.stroke(); }
  ctx.strokeStyle='#334155';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(CX-xr*U,CY);ctx.lineTo(CX+xr*U,CY);ctx.stroke();
  ctx.beginPath();ctx.moveTo(CX,CY-yr*U);ctx.lineTo(CX,CY+yr*U);ctx.stroke();
}
function drawFn(ctx,a,b,col,xr,yr,alpha){
  var i,started=false;
  ctx.globalAlpha=(alpha===undefined)?1:alpha;
  ctx.strokeStyle=col;ctx.lineWidth=3;ctx.beginPath();
  for(i=-xr*10;i<=xr*10;i++){
    var xx=i/10, yy=a*xx+b;
    if(yy<-yr||yy>yr){ started=false; continue; }
    var Px=CX+xx*U, Py=CY-yy*U;
    if(!started){ ctx.moveTo(Px,Py); started=true; } else ctx.lineTo(Px,Py);
  }
  ctx.stroke();ctx.globalAlpha=1;
}
"""

# ============================================================
# 1. 기울기가 크면 항상 위에 있을까
# ============================================================
LAB_TWO = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'두 직선 비교판',
  action:'두 직선 그리기',
  hint0:'두 일차함수의 기울기와 y절편을 정해 보자.',
  sliders:[
    {id:'a1',label:'① 기울기',min:-5,max:5,value:3,color:'#2563eb',unit:''},
    {id:'b1',label:'① y절편',min:-8,max:8,value:-6,color:'#60a5fa',unit:''},
    {id:'a2',label:'② 기울기',min:-5,max:5,value:1,color:'#dc2626',unit:''},
    {id:'b2',label:'② y절편',min:-8,max:8,value:3,color:'#f87171',unit:''}
  ],
  calc:function(S){
    var at1=S.a1*1+S.b1, bt1=S.a2*1+S.b2;
    var at5=S.a1*5+S.b1, bt5=S.a2*5+S.b2;
    var cross=(S.a1!==S.a2)?((S.b2-S.b1)/(S.a1-S.a2)):null;
    return {y1a:at1,y2a:bt1,y1b:at5,y2b:bt5,cross:cross,
            up1:(at1>bt1)?'①':((bt1>at1)?'②':'같음'),
            up5:(at5>bt5)?'①':((bt5>at5)?'②':'같음'),
            steep:(S.a1>S.a2)?'①':((S.a2>S.a1)?'②':'같음')};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'x = 1에서 위',v:ran?c.up1:'그려 보자'},
            {k:'x = 5에서 위',v:ran?c.up5:'-'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    return 'x=1에서는 '+c.up1+'이 위, x=5에서는 '+c.up5+'이 위다. 기울기가 큰 쪽은 '+c.steep+'이다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    grid(ctx,10,9);
    var grow=(t===null)?0:Math.min(1,t);
    drawFn(ctx,S.a1,S.b1,'#2563eb',10,9,1);
    drawFn(ctx,S.a2,S.b2,'#dc2626',10,9,grow);
    var c=this.calc(S);
    if(grow>=1){
      [[1,'#7c3aed'],[5,'#059669']].forEach(function(q){
        var x=q[0];
        ctx.strokeStyle=q[1];ctx.lineWidth=1.6;ctx.setLineDash([4,4]);
        ctx.beginPath();ctx.moveTo(CX+x*U,CY-9*U);ctx.lineTo(CX+x*U,CY+9*U);ctx.stroke();ctx.setLineDash([]);
        lbl(ctx,'x='+x,CX+x*U+4,CY+9*U-4,q[1],13);
      });
      if(c.cross!==null&&Math.abs(c.cross)<=10){
        var cy=S.a1*c.cross+S.b1;
        if(Math.abs(cy)<=9){
          ctx.beginPath();ctx.arc(CX+c.cross*U,CY-cy*U,7,0,Math.PI*2);
          ctx.fillStyle='#f59e0b';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
        }
      }
    }
    lbl(ctx,'① '+eqStr(S.a1,S.b1)+'     ② '+eqStr(S.a2,S.b2),24,32,'#334155',16);
    box(ctx,20,348,400,64);
    lbl(ctx,(t===null)?'기울기가 큰 쪽이 항상 위에 있을까?':
        ('x=1 : '+c.up1+' 위     x=5 : '+c.up5+' 위     기울기 큰 쪽 : '+c.steep),38,378,'#1f2937',17);
    lbl(ctx,(t===null)?'':((c.cross===null)?'두 직선은 평행하다':('교점의 x좌표 : '+r2(c.cross))),38,402,'#52627a',15);
  },
  record:function(S){
    var c=this.calc(S);
    return {a1:S.a1,b1:S.b1,a2:S.a2,b2:S.b2,
            up1:c.up1,up5:c.up5,steep:c.steep,
            same:(c.up1===c.up5),
            steepUp1:(c.steep===c.up1),steepUp5:(c.steep===c.up5),
            cross:(c.cross===null)?'평행':r2(c.cross)};
  },
  headA:['번호','① 식','② 식','x=1에서 위','x=5에서 위','기울기 큰 쪽','두 곳이 같은 답?','교점 x'],
  rowA:function(r,i){
    return [i+1,eqStr(r.a1,r.b1),eqStr(r.a2,r.b2),r.up1,r.up5,'<b>'+r.steep+'</b>',
            '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>',r.cross];
  },
  analyze:function(rec){
    var rows=[],same=0,flip=0,s1=0,s5=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.same) same++; else flip++;
      if(r.steepUp1) s1++;
      if(r.steepUp5) s5++;
      rows.push([eqStr(r.a1,r.b1)+' / '+eqStr(r.a2,r.b2), r.up1, r.up5, '<b>'+r.steep+'</b>',
                 '<span class="'+(r.same?'ok':'no')+'">'+(r.same?'○':'×')+'</span>', r.cross]);
    }
    var stats=[
      {t:'두 위치에서 위아래가 같았던 횟수',big:same+' / '+rec.length,
       p:'x=1과 x=5에서 위에 있는 그래프가 같았던 기록 수.'},
      {t:'위아래가 뒤바뀐 경우',big:flip+'개',
       p:flip?'두 직선이 그 사이에서 교차했기 때문이다.':'y절편을 크게 다르게 해서 교차하도록 만들어 보자.'},
      {t:'기울기 큰 쪽이 위였던 횟수',big:'x=1에서 '+s1+' / x=5에서 '+s5,
       p:'기울기만으로 위아래를 판단할 수 있는지 확인한 결과.'}
    ];
    var concl;
    if(flip===0){
      concl='<b>더 해 보자</b> — 아직 위아래가 뒤바뀐 기록이 없다. 기울기가 큰 직선의 y절편을 아주 작게 잡아 보자.';
    } else {
      concl='<b>정리</b> — 같은 두 직선인데도 x=1에서는 한쪽이 위, x=5에서는 다른 쪽이 위인 경우가 '+flip+'번 나왔다. '
           +'<b>기울기는 “얼마나 가파른가”일 뿐 “어디에 있는가”가 아니다.</b> '
           +'기울기가 다르면 두 직선은 반드시 한 번 만나고, 그 지점을 지나면 위아래가 뒤바뀐다. '
           +'위치는 기울기와 y절편을 함께 봐야 알 수 있다.';
    }
    return {head:['두 식','x=1에서 위','x=5에서 위','기울기 큰 쪽','같은 답?','교점 x'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 2. 변화율은 어디서 재도 같을까
# ============================================================
LAB_RATE = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'변화율 측정판',
  action:'두 점 사이 변화율 재기',
  hint0:'일차함수와 잴 두 점의 x좌표를 정해 보자.',
  sliders:[
    {id:'a',label:'기울기 a',min:-5,max:5,value:2,color:'#2563eb',unit:''},
    {id:'b',label:'y절편 b',min:-8,max:8,value:-3,color:'#60a5fa',unit:''},
    {id:'x1',label:'첫 번째 점의 x',min:-8,max:8,value:-2,color:'#16a34a',unit:''},
    {id:'x2',label:'두 번째 점의 x',min:-8,max:8,value:3,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var y1=S.a*S.x1+S.b, y2=S.a*S.x2+S.b;
    var dx=S.x2-S.x1, dy=y2-y1;
    return {y1:y1,y2:y2,dx:dx,dy:dy,rate:(dx===0)?null:(dy/dx)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'x의 증가량 / y의 증가량',v:c.dx+' / '+c.dy},
            {k:'변화율',v:ran?((c.rate===null)?'잴 수 없음':r2(c.rate)):'재 보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.rate===null) return '두 점의 x좌표가 같아 변화율을 잴 수 없다. 다른 점을 골라 보자.';
    return 'y의 증가량 '+c.dy+' ÷ x의 증가량 '+c.dx+' = '+r2(c.rate)+'.  기울기 '+S.a+'와 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    grid(ctx,10,9);
    drawFn(ctx,S.a,S.b,'#2563eb',10,9,1);
    var mv=(t===null)?0:Math.min(1,t);
    function pt(x,y,col){
      ctx.beginPath();ctx.arc(CX+x*U,CY-y*U,7,0,Math.PI*2);
      ctx.fillStyle=col;ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
    }
    if(Math.abs(c.y1)<=9) pt(S.x1,c.y1,'#16a34a');
    if(Math.abs(c.y2)<=9) pt(S.x2,c.y2,'#dc2626');
    if(mv>0&&c.rate!==null){
      var xa=CX+S.x1*U, ya=CY-c.y1*U, xb=CX+S.x2*U, yb=CY-c.y2*U;
      ctx.strokeStyle='#f59e0b';ctx.lineWidth=2.6;
      ctx.beginPath();ctx.moveTo(xa,ya);ctx.lineTo(xa+(xb-xa)*mv,ya);ctx.stroke();
      if(mv>0.5){
        var m2=(mv-0.5)/0.5;
        ctx.beginPath();ctx.moveTo(xb,ya);ctx.lineTo(xb,ya+(yb-ya)*m2);ctx.stroke();
      }
      lbl(ctx,'x 증가량 '+c.dx,(xa+xb)/2,ya-8,'#b45309',14,'center');
      if(mv>0.9) lbl(ctx,'y 증가량 '+c.dy,xb+8,(ya+yb)/2,'#b45309',14);
    }
    lbl(ctx,eqStr(S.a,S.b),24,32,'#1d4ed8',18);
    box(ctx,20,348,400,66);
    lbl(ctx,(t===null)?'두 점을 어디에 잡느냐에 따라 달라질까?':
        ('('+S.x1+', '+c.y1+') → ('+S.x2+', '+c.y2+')      변화율 '+((c.rate===null)?'-':r2(c.rate))),
        38,378,'#1f2937',17);
    lbl(ctx,'기울기 a = '+S.a,38,402,'#15803d',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,x1:S.x1,x2:S.x2,y1:c.y1,y2:c.y2,dx:c.dx,dy:c.dy,
            rate:(c.rate===null)?null:r2(c.rate),
            ok:(c.rate!==null&&Math.abs(c.rate-S.a)<1e-9),
            valid:(c.rate!==null)};
  },
  headA:['번호','식','두 점','x 증가량','y 증가량','변화율','기울기','같은가?'],
  rowA:function(r,i){
    if(!r.valid) return [i+1,eqStr(r.a,r.b),'x좌표가 같음','-','-','-',r.a,'-'];
    return [i+1,eqStr(r.a,r.b),'('+r.x1+','+r.y1+')→('+r.x2+','+r.y2+')',r.dx,r.dy,'<b>'+r.rate+'</b>',r.a,
            '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ok=0,valid=0,g={},pairs=0,dys={};
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(!r.valid){ rows.push([eqStr(r.a,r.b),'-','-','-',r.a,'-']); continue; }
      valid++;
      if(r.ok) ok++;
      var k=r.a+'|'+r.b;
      if(g[k]) pairs++; else g[k]=true;
      if(!dys[r.dy]) dys[r.dy]=[];
      dys[r.dy].push(r.rate);
      rows.push([eqStr(r.a,r.b), '('+r.x1+','+r.y1+')→('+r.x2+','+r.y2+')', r.dx+' / '+r.dy,
                 '<b>'+r.rate+'</b>', r.a,
                 '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>']);
    }
    var dyConflict=0,k2;
    for(k2 in dys){
      var arr=dys[k2],j;
      for(j=1;j<arr.length;j++){ if(arr[j]!==arr[0]){ dyConflict++; break; } }
    }
    var stats=[
      {t:'변화율 = 기울기',big:ok+' / '+valid,
       p:'두 점을 어디에 잡아도 변화율이 기울기와 같았는지 확인한 결과.'},
      {t:'같은 함수에서 다른 두 점으로 잰 횟수',big:pairs+'번',
       p:pairs?'같은 식에서 점만 바꿔 다시 쟀다.':'같은 식에서 두 점만 바꿔 다시 기록해 보자.'},
      {t:'y 증가량이 같은데 변화율이 달랐던 경우',big:dyConflict+'가지',
       p:dyConflict?'y가 같은 만큼 늘어도 x 증가량이 다르면 변화율이 다르다.':'y 증가량이 같고 x 증가량이 다른 두 기록을 만들어 보자.'}
    ];
    var concl;
    if(valid===0){
      concl='<b>더 해 보자</b> — 두 점의 x좌표를 서로 다르게 잡아야 변화율을 잴 수 있다.';
    } else if(ok===valid && pairs>0){
      concl='<b>정리</b> — 같은 일차함수에서 두 점을 어디에 잡아도 <b>(y의 증가량) ÷ (x의 증가량)은 언제나 기울기 a</b>였다. '
           +'그래서 일차함수의 그래프는 곧은 직선이 된다. '
           +(dyConflict?'반면 y의 증가량만 보고 판단하면 안 된다. 같은 y 증가량이라도 x 증가량이 다르면 변화율이 달랐다.':'');
    } else if(ok===valid){
      concl='<b>정리</b> — 변화율은 모두 기울기와 같았다. 같은 식에서 두 점만 바꿔 다시 기록하면 더 확실해진다.';
    } else {
      concl='<b>확인 필요</b> — 변화율이 기울기와 다른 기록이 있다.';
    }
    return {head:['식','두 점','x/y 증가량','변화율','기울기','같은가?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 3. x절편과 y절편
# ============================================================
LAB_INT = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'절편 실험판',
  action:'축과 만나는 점 찾기',
  hint0:'기울기와 y절편을 정하고, 그래프가 두 축과 만나는 점을 찾아보자.',
  sliders:[
    {id:'a',label:'기울기 a',min:-5,max:5,value:2,color:'#2563eb',unit:''},
    {id:'b',label:'y절편 b',min:-8,max:8,value:6,color:'#f59e0b',unit:''}
  ],
  calc:function(S){
    var xi=(S.a===0)?null:(-S.b/S.a);
    var wrong=(S.a===0)?null:(S.b/S.a);
    return {xi:xi,wrong:wrong,
            chk:(xi===null)?null:(S.a*xi+S.b),
            chkW:(wrong===null)?null:(S.a*wrong+S.b)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'y절편',v:'( 0 , '+S.b+' )'},
            {k:'x절편',v:ran?((c.xi===null)?'없음':('( '+r2(c.xi)+' , 0 )')):'찾아보자'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.xi===null) return '기울기가 0이라 x축과 만나지 않거나 겹친다. 다른 기울기로 해 보자.';
    return 'x절편은 '+r2(c.xi)+', y절편은 '+S.b+'다. b ÷ a = '+r2(c.wrong)+'와 비교해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S);
    grid(ctx,10,9);
    drawFn(ctx,S.a,S.b,'#2563eb',10,9,1);
    var show=(t===null)?0:Math.min(1,t);
    if(show>0&&Math.abs(S.b)<=9){
      ctx.beginPath();ctx.arc(CX,CY-S.b*U,8,0,Math.PI*2);
      ctx.fillStyle='#f59e0b';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      lbl(ctx,'(0, '+S.b+')',CX+12,CY-S.b*U-10,'#b45309',15);
    }
    if(show>0.5&&c.xi!==null&&Math.abs(c.xi)<=10){
      ctx.beginPath();ctx.arc(CX+c.xi*U,CY,8,0,Math.PI*2);
      ctx.fillStyle='#16a34a';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      lbl(ctx,'('+r2(c.xi)+', 0)',CX+c.xi*U+10,CY+22,'#15803d',15);
    }
    if(show>=1&&c.wrong!==null&&Math.abs(c.wrong)<=10&&c.wrong!==c.xi){
      ctx.beginPath();ctx.arc(CX+c.wrong*U,CY,7,0,Math.PI*2);
      ctx.fillStyle='#fecaca';ctx.fill();ctx.strokeStyle='#dc2626';ctx.lineWidth=2;ctx.stroke();
      lbl(ctx,'b÷a',CX+c.wrong*U-6,CY-12,'#b91c1c',13);
    }
    lbl(ctx,eqStr(S.a,S.b),24,32,'#1d4ed8',18);
    box(ctx,20,348,400,66);
    lbl(ctx,(t===null)?'x절편은 어떻게 구할까?':
        ('x절편 '+((c.xi===null)?'없음':r2(c.xi))+'    y절편 '+S.b),38,378,'#1f2937',19);
    lbl(ctx,(t===null)?'':('b ÷ a = '+((c.wrong===null)?'-':r2(c.wrong))+' 를 넣으면 y = '+((c.chkW===null)?'-':r2(c.chkW))),
        38,402,'#b91c1c',16);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b:S.b,xi:(c.xi===null)?null:r2(c.xi),yi:S.b,
            wrong:(c.wrong===null)?null:r2(c.wrong),
            chk:(c.chk===null)?null:r2(c.chk),
            chkW:(c.chkW===null)?null:r2(c.chkW),
            ok:(c.chk!==null&&Math.abs(c.chk)<1e-9),
            wok:(c.chkW!==null&&Math.abs(c.chkW)<1e-9),
            valid:(c.xi!==null)};
  },
  headA:['번호','식','y절편','x절편','대입 결과','맞나?','b÷a','대입 결과','맞나?'],
  rowA:function(r,i){
    if(!r.valid) return [i+1,eqStr(r.a,r.b),r.yi,'없음','-','-','-','-','-'];
    return [i+1,eqStr(r.a,r.b),r.yi,'<b>'+r.xi+'</b>',r.chk,
            '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
            r.wrong,r.chkW,
            '<span class="'+(r.wok?'ok':'no')+'">'+(r.wok?'○':'×')+'</span>'];
  },
  analyze:function(rec){
    var rows=[],ok=0,wok=0,valid=0,bz=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(!r.valid){ rows.push([eqStr(r.a,r.b),r.yi,'없음','-','-','-']); continue; }
      valid++;
      if(r.ok) ok++;
      if(r.wok) wok++;
      if(r.b===0) bz++;
      rows.push([eqStr(r.a,r.b), r.yi, '<b>'+r.xi+'</b>', r.chk,
                 '<span class="'+(r.ok?'ok':'no')+'">'+(r.ok?'○':'×')+'</span>',
                 r.wrong+' → '+r.chkW,
                 '<span class="'+(r.wok?'ok':'no')+'">'+(r.wok?'○':'×')+'</span>']);
    }
    var stats=[
      {t:'x절편 = −b ÷ a 가 맞은 횟수',big:ok+' / '+valid,
       p:'구한 값을 식에 넣어 y가 0이 되는지 확인한 결과.'},
      {t:'b ÷ a 가 맞은 횟수',big:wok+' / '+valid,
       p:'부호를 바꾸지 않으면 어떻게 되는지 확인했다.'},
      {t:'y절편이 0이었던 기록',big:bz+'개',
       p:bz?'b=0이면 두 값이 같아진다(원점을 지난다).':'b=0인 경우도 넣어 보자.'}
    ];
    var concl;
    if(valid===0){
      concl='<b>더 해 보자</b> — 기울기를 0이 아닌 값으로 두어야 x절편이 생긴다.';
    } else if(ok===valid && wok===bz){
      concl='<b>정리</b> — x절편은 <b>y = 0을 넣어 푼 값, 즉 −b ÷ a</b>였고, 넣어 보면 언제나 y가 0이 되었다. '
           +'부호를 바꾸지 않은 b ÷ a는 b가 0일 때만 우연히 맞았다. '
           +'y절편은 x=0일 때의 y값 b이고 점으로는 (0, b), x절편은 점으로 (−b/a, 0)이다. '
           +'둘 다 “축과 만나는 점의 좌표 한 개”라는 점을 기억하자.';
    } else {
      concl='<b>정리</b> — 절편은 축과 만나는 점의 좌표다. 값을 대입해 y가 0이 되는지로 확인할 수 있다.';
    }
    return {head:['식','y절편','x절편','대입 결과','맞나?','b÷a → 대입','맞나?'],rows:rows,stats:stats,concl:concl};
  }
};
"""

# ============================================================
# 4. 평행이동과 평행한 두 직선
# ============================================================
LAB_SHIFT = BASE + r"""
var LAB = {
  cw:440, ch:430, cvTitle:'평행이동판',
  action:'평행하게 옮기기',
  hint0:'기울기가 같고 y절편만 다른 두 직선을 만들어 보자.',
  sliders:[
    {id:'a',label:'두 직선의 기울기',min:-5,max:5,value:2,color:'#2563eb',unit:''},
    {id:'b1',label:'① y절편',min:-8,max:8,value:-4,color:'#60a5fa',unit:''},
    {id:'b2',label:'② y절편',min:-8,max:8,value:3,color:'#dc2626',unit:''}
  ],
  calc:function(S){
    var d=S.b2-S.b1;
    var gaps=[];
    var xs=[-6,-2,2,6],i;
    for(i=0;i<xs.length;i++){ gaps.push((S.a*xs[i]+S.b2)-(S.a*xs[i]+S.b1)); }
    var allSame=true;
    for(i=1;i<gaps.length;i++){ if(gaps[i]!==gaps[0]) allSame=false; }
    return {d:d,gaps:gaps,allSame:allSame,meet:(d===0)};
  },
  readout:function(S,ran){
    var c=this.calc(S);
    return [{k:'세로 간격',v:ran?(Math.abs(c.d)+''):'옮겨 보자'},
            {k:'두 직선',v:c.meet?'완전히 겹침':'평행'}];
  },
  doneMsg:function(S){
    var c=this.calc(S);
    if(c.meet) return 'y절편까지 같아서 두 직선이 완전히 겹쳤다. y절편을 다르게 해 보자.';
    return '어느 x에서 재도 세로 간격이 '+Math.abs(c.d)+'로 같았다. 두 직선은 만나지 않는다. 기록해 보자.';
  },
  draw:function(ctx,S,t,ran){
    var c=this.calc(S), i;
    grid(ctx,10,9);
    drawFn(ctx,S.a,S.b1,'#2563eb',10,9,1);
    var mv=(t===null)?0:Math.min(1,t);
    var cur=S.b1+(S.b2-S.b1)*mv;
    if(mv>0) drawFn(ctx,S.a,cur,'#dc2626',10,9,1);
    if(mv>=1){
      var xs=[-6,-2,2,6];
      for(i=0;i<xs.length;i++){
        var x=xs[i], y1=S.a*x+S.b1, y2=S.a*x+S.b2;
        if(Math.abs(y1)>9||Math.abs(y2)>9) continue;
        ctx.strokeStyle='#f59e0b';ctx.lineWidth=2.4;
        ctx.beginPath();ctx.moveTo(CX+x*U,CY-y1*U);ctx.lineTo(CX+x*U,CY-y2*U);ctx.stroke();
        lbl(ctx,''+Math.abs(c.d),CX+x*U+5,CY-(y1+y2)/2*U+4,'#b45309',13);
      }
    }
    lbl(ctx,'① '+eqStr(S.a,S.b1)+'     ② '+eqStr(S.a,S.b2),24,32,'#334155',16);
    box(ctx,20,348,400,66);
    lbl(ctx,(t===null)?'두 직선은 언젠가 만날까?':
        (c.meet?'두 직선이 완전히 겹친다':('세로 간격 : '+c.gaps.map(function(z){return Math.abs(z);}).join(', ')+' — 모두 같다')),
        38,378,'#1f2937',17);
    lbl(ctx,(t===null)?'':('y절편의 차 : '+Math.abs(c.d)),38,402,'#15803d',17);
  },
  record:function(S){
    var c=this.calc(S);
    return {a:S.a,b1:S.b1,b2:S.b2,d:Math.abs(c.d),
            gaps:c.gaps.map(function(z){return Math.abs(z);}).join(', '),
            allSame:c.allSame,meet:c.meet,
            match:(Math.abs(c.gaps[0])===Math.abs(c.d))};
  },
  headA:['번호','① 식','② 식','네 곳의 세로 간격','모두 같은가?','y절편의 차','두 직선'],
  rowA:function(r,i){
    return [i+1,eqStr(r.a,r.b1),eqStr(r.a,r.b2),r.gaps,
            '<span class="'+(r.allSame?'ok':'no')+'">'+(r.allSame?'○':'×')+'</span>',
            '<b>'+r.d+'</b>',r.meet?'겹침':'평행'];
  },
  analyze:function(rec){
    var rows=[],all=0,match=0,meet=0,as={},an=0;
    for(var i=0;i<rec.length;i++){
      var r=rec[i];
      if(r.allSame) all++;
      if(r.match) match++;
      if(r.meet) meet++;
      as[r.a]=true;
      rows.push([eqStr(r.a,r.b1)+' / '+eqStr(r.a,r.b2), r.gaps,
                 '<span class="'+(r.allSame?'ok':'no')+'">'+(r.allSame?'○':'×')+'</span>',
                 '<b>'+r.d+'</b>',
                 '<span class="'+(r.match?'ok':'no')+'">'+(r.match?'○':'×')+'</span>',
                 r.meet?'겹침':'평행']);
    }
    for(var k in as) an++;
    var stats=[
      {t:'네 곳의 세로 간격이 모두 같았던 횟수',big:all+' / '+rec.length,
       p:'x를 −6, −2, 2, 6으로 바꿔 가며 잰 결과.'},
      {t:'세로 간격 = y절편의 차',big:match+' / '+rec.length,
       p:'평행이동한 거리가 곧 y절편의 차인지 확인한 결과.'},
      {t:'완전히 겹친 기록 / 시험한 기울기',big:meet+'개 / '+an+'가지',
       p:'y절편까지 같으면 같은 직선이 된다.'}
    ];
    var concl;
    if(all===rec.length && match===rec.length){
      concl='<b>정리</b> — 기울기가 같으면 어느 x에서 재도 <b>세로 간격이 언제나 같았고</b>, 그 값은 y절편의 차와 정확히 일치했다. '
           +'간격이 줄어들지 않으니 두 직선은 <b>아무리 멀리 가도 만나지 않는다.</b> '
           +'y = ax + b의 b는 그래프를 위아래로 평행이동시키는 값이고, 기울기가 같고 y절편이 다르면 평행, 둘 다 같으면 같은 직선이다.';
    } else {
      concl='<b>확인 필요</b> — 세로 간격이 일정하지 않은 기록이 있다.';
    }
    return {head:['두 식','세로 간격','모두 같은가?','y절편 차','일치?','두 직선'],rows:rows,stats:stats,concl:concl};
  }
};
"""

LABS = [
    ("m2_two_lines_position_lab.html",
     "두 직선 실험실 — 기울기가 크면 항상 위에 있을까?",
     "두 직선 실험실 — 기울기가 크면 항상 위에 있을까?",
     "두 일차함수를 함께 그려 x=1과 x=5에서 어느 쪽이 위인지 기록하고, 기울기와 비교한다.",
     LAB_TWO),
    ("m2_rate_of_change_lab.html",
     "변화율 실험실 — 두 점을 어디에 잡아도 같을까?",
     "변화율 실험실 — 두 점을 어디에 잡아도 같을까?",
     "같은 일차함수에서 두 점의 위치를 바꿔 가며 (y의 증가량)÷(x의 증가량)을 재고 기울기와 대조한다.",
     LAB_RATE),
    ("m2_intercepts_lab.html",
     "절편 실험실 — x절편은 b ÷ a일까?",
     "절편 실험실 — x절편은 b ÷ a일까?",
     "그래프가 두 축과 만나는 점을 찾아 대입으로 검산하고, 부호를 바꾸지 않은 값과 비교한다.",
     LAB_INT),
    ("m2_parallel_shift_lab.html",
     "평행이동 실험실 — 평행한 두 직선은 언젠가 만날까?",
     "평행이동 실험실 — 평행한 두 직선은 언젠가 만날까?",
     "기울기가 같고 y절편만 다른 두 직선의 세로 간격을 여러 x에서 재어 기록한다.",
     LAB_SHIFT),
]

made = []
for fname, title, h1, lead, labjs in LABS:
    html = TPL.replace("@@TITLE@@", title).replace("@@H1@@", h1).replace("@@LEAD@@", lead).replace("@@LABJS@@", labjs)
    assert "@@" not in html
    path = os.path.join(OUT, fname)
    open(path, "w", encoding="utf-8").write(html)
    made.append(path)
    js = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    open("/home/claude/_c14_" + fname + ".js", "w", encoding="utf-8").write(js)

print("\n".join(made))
