/* 파동판 — 문제 풀기 (261124)
   wave_lab.html 의 전역(dev, nSrc, lam, sep, phase, slitW, slit2, medV, dopV, srcX, srcY, rebuild …)을 그대로 쓴다.
   답을 넣기 전에는 '값' 칸(파장·각도 설명이 나오는 곳)을 가린다. */
(function(){
  var c = document.getElementById('roLam').closest('.card');
  if (c && !c.id) c.id = 'valCard';
})();
function wvGo(o){
  dev = o.dev || 'none'; nSrc = o.nSrc || 1; lam = o.lam || 16; sep = o.sep || 70; phase = o.phase || 0;
  slitW = o.slitW || 10; slit2 = o.slit2 || 56; medV = o.medV || 0.6; dopV = o.dopV || 0;
  srcX = o.srcX || 95; srcY = o.srcY || 120; dopPos = 0;
  if (patternMode !== !!o.pattern){ patternMode = !!o.pattern; document.getElementById('btnPattern').classList.toggle('on', patternMode); }
  running = true; document.getElementById('btnRun').classList.add('on'); document.getElementById('btnRun').textContent = '멈춤';
  rebuild();
}
function wvDeg(x){ return Math.asin(Math.min(1, x)) * 180 / Math.PI; }
var WAVE_QUESTS = [
  {id:'wave-slit-width', lv:1, title:'좁은 틈 vs 넓은 틈', kind:'choice', answer:0,
   choices:['틈이 좁을 때 더 넓게 퍼진다', '틈이 넓을 때 더 넓게 퍼진다', '틈 너비와 상관없이 똑같이 퍼진다'],
   text:'물결이 벽의 틈을 지나갑니다. 틈이 <b>좁을 때</b>와 <b>넓을 때</b>, 틈을 지난 물결이 옆으로 더 넓게 퍼지는 쪽은 어디일까요?',
   hint:'문틈 사이로 소리는 잘 들리는데, 소리의 파장은 꽤 길어요.',
   explain:'파동이 틈을 지나 뒤쪽으로 돌아 퍼지는 것을 <b>회절</b>이라고 해요. 틈이 파장보다 좁거나 비슷할수록 더 넓게 퍼지고, 틈이 파장보다 훨씬 넓으면 거의 곧게 지나가요. 지금은 좁은 틈이에요 — 장치 칸에서 틈 너비를 넓혀 견주어 보세요.',
   setup:function(){ wvGo({dev:'slit1', lam:18, slitW:40}); running = false; document.getElementById('btnRun').textContent = '실행'; },
   reveal:function(){ wvGo({dev:'slit1', lam:18, slitW:8}); }},
  {id:'wave-period', lv:2, title:'몇 걸음마다 한 번?', kind:'num', unit:'걸음', answer:function(){ return 20 / C0; }, tol:1.5,
   text:'이 파동판에서 물결의 속력은 <b>' + 0.5 + '칸/걸음</b>이에요. 파장을 <b>20칸</b>으로 하면, 파원은 몇 걸음마다 한 번씩 출렁일까요? (주기)',
   hint:'속력 = 파장 ÷ 주기 예요. 주기 = 파장 ÷ 속력.',
   explain:'주기 T = λ ÷ v = 20 ÷ 0.5 = <b>40걸음</b>. 진동수는 그 거꾸로 1/40 = 0.025/걸음이에요. v = fλ — 속력이 그대로면 파장이 길수록 천천히 출렁여요.',
   setup:function(){ wvGo({lam:20, srcX:160}); },
   reveal:function(){ wvGo({lam:20, srcX:160}); }},
  {id:'wave-two-source', lv:2, title:'첫 보강 방향', kind:'num', unit:'°', answer:function(){ return wvDeg(14 / 70); }, tol:1.5,
   text:'두 파원이 <b>70칸</b> 떨어져 같은 박자로 물결을 만들어요. 파장은 <b>14칸</b>. 가운데 센 줄 다음으로 나오는 첫 번째 센 줄(보강)은 가운데에서 몇 도 기울어 있을까요?',
   hint:'두 파원에서 온 길이 차가 파장 하나(λ)가 되는 방향이에요. 멀리서 보면 길이 차 = d·sinθ.',
   explain:function(){ return 'd·sinθ = λ → sinθ = 14/70 = 0.2 → θ ≈ <b>' + wvDeg(0.2).toFixed(1) + '°</b>. 무늬 쌓기를 켜면 센 줄(밝게)과 조용한 줄(어둡게)이 번갈아 보여요.'; },
   setup:function(){ wvGo({nSrc:2, lam:14, sep:70}); },
   reveal:function(){ wvGo({nSrc:2, lam:14, sep:70, pattern:true}); }},
  {id:'wave-longer', lv:2, title:'파장을 늘리면', kind:'choice', answer:0,
   choices:['센 줄 사이가 넓어진다', '센 줄 사이가 좁아진다', '무늬가 그대로다', '무늬가 사라진다'],
   text:'벽의 틈 두 개(이중 슬릿)를 지난 물결이 간섭 무늬를 만들어요. 틈 사이는 그대로 두고 <b>파장만 두 배로</b> 늘리면 무늬는 어떻게 될까요?',
   hint:'첫 센 줄 방향은 sinθ = λ/d 예요. λ 가 커지면?',
   explain:'sinθ = λ/d 이므로 파장이 길수록 각이 커져 <b>센 줄 사이가 넓어져요</b>. 빛으로 하면 빨간빛(파장 김) 무늬가 파란빛 무늬보다 넓게 벌어져요.',
   setup:function(){ wvGo({dev:'slit2', lam:9, slitW:7, slit2:56, pattern:true}); },
   reveal:function(){ wvGo({dev:'slit2', lam:18, slitW:7, slit2:56, pattern:true}); }},
  {id:'wave-antiphase', lv:3, title:'반대 박자 두 파원', kind:'choice', answer:1,
   choices:['가장 센 줄(보강)이 된다', '조용한 줄(상쇄)이 된다', '한쪽 파원 물결만 보인다'],
   text:'두 파원이 <b>반대 박자</b>(위상차 180°)로 출렁여요. 두 파원에서 <b>똑같은 거리</b>에 있는 가운데 줄에서는 어떻게 될까요?',
   hint:'길이 차가 0 이면 출발할 때의 박자 차이가 그대로 남아요.',
   explain:'길이 차가 0 이어도 처음부터 반대 박자라 마루와 골이 만나 <b>상쇄</b>돼요. 같은 박자일 때 센 줄이던 자리가 조용한 줄로 바뀌어요 — 소음 제거 헤드폰이 이 원리예요.',
   setup:function(){ wvGo({nSrc:2, lam:16, sep:80, phase:180}); running = false; document.getElementById('btnRun').textContent = '실행'; },
   reveal:function(){ wvGo({nSrc:2, lam:16, sep:80, phase:180, pattern:true}); }},
  {id:'wave-refraction', lv:3, title:'느린 곳의 파장', kind:'num', unit:'칸', answer:function(){ return 16 * 0.6; }, tol:0.6,
   text:'위쪽에서 파장 <b>16칸</b>인 물결이, 빠르기가 <b>0.6배</b>인 아래쪽 매질로 들어가요. 아래쪽에서 파장은 몇 칸일까요?',
   hint:'매질이 바뀌어도 진동수(박자)는 그대로예요. v = fλ.',
   explain:'진동수가 같으니 파장은 빠르기에 비례해요. 16 × 0.6 = <b>9.6칸</b>. 비스듬히 들어가면 이 차이 때문에 진행 방향이 꺾여요(굴절) — sinθ₁/sinθ₂ = v₁/v₂.',
   setup:function(){ wvGo({dev:'medium', lam:16, medV:0.6, srcX:130, srcY:80}); },
   reveal:function(){ wvGo({dev:'medium', lam:16, medV:0.6, srcX:130, srcY:80}); }},
  {id:'wave-doppler', lv:3, title:'다가오는 소리', kind:'choice', answer:0,
   choices:['원래보다 높은 소리(파장 짧음)', '원래보다 낮은 소리(파장 김)', '원래와 같은 소리'],
   text:'소리를 내는 파원이 <b>오른쪽으로</b> 달려요. 오른쪽에 서 있는 사람에게는 어떤 소리로 들릴까요?',
   hint:'파원이 앞으로 가면서 물결을 내면, 앞쪽 마루와 마루 사이는 어떻게 될까요?',
   explain:'파원이 다가오면 앞쪽 마루 사이가 좁아져 파장이 짧아지고 → 진동수가 커져 <b>높은 소리</b>로 들려요. 지나간 뒤에는 낮아져요. 구급차 사이렌이 지나갈 때 소리가 바뀌는 까닭이에요(도플러 효과).',
   setup:function(){ wvGo({lam:14, dopV:0}); },
   reveal:function(){ wvGo({lam:14, dopV:0.45}); }}
];
LabQuest.init({
  lab:'wave', quests:WAVE_QUESTS,
  mount:document.querySelector('main.layout'), button:document.querySelector('.levels'),
  level:function(){ return level; }, setLevel:setLevel, hide:['valCard']
});
