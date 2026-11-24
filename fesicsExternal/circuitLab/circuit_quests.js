/* 회로 실험실 — 문제 풀기 (261124)
   답을 넣기 전에는 부품 값(전류·전압 숫자)과 측정값 칸을 가린다. 밝기를 견주는 문제는
   스위치를 열어 둔 채 시작하고, 답을 넣으면 스위치를 닫아 실제로 켜 본다.
   circuit_lab.html 의 전역(els, addPart, addWire, changed, showValues …)을 그대로 쓴다. */
(function(){
  var mc = document.getElementById('roI').closest('.card');
  if (mc && !mc.id) mc.id = 'measCard';
})();
function cqValues(on){
  showValues = on;
  var b = document.getElementById('btnValues');
  if (b) b.textContent = on ? '부품 값 숨기기' : '부품 값 보기';
}
function cqScene(fn){
  snapshot(); els = []; selId = null; simTime = 0; scope = [];
  fn(); cqValues(false); changed();
}
function cqSwitches(closed){
  els.forEach(function(e){ if (e.type === 'switch') e.props.closed = closed; });
  changed();
}
function cqRing(top, bottom, right){   /* 왼쪽 세로선·위·오른쪽·아래로 두르는 선 */
  addWire(right, top, right, bottom); addWire(right, bottom, 3, bottom);
}
var CIR_QUESTS = [
  {id:'cir-series-bright', lv:1, title:'전구 한 개 vs 두 개', kind:'choice', answer:0,
   choices:['위 회로(전구 한 개)의 전구', '아래 회로(전구 두 개를 한 줄로)의 전구', '둘 다 똑같다'],
   text:'똑같은 전지에 위 회로는 전구를 <b>한 개</b>, 아래 회로는 같은 전구를 <b>두 개 한 줄로(직렬)</b> 이었어요. 스위치를 닫으면 어느 쪽 전구가 더 밝을까요?',
   hint:'전구를 한 줄로 더 이으면 전류가 지나가기 더 힘들어져요.',
   explain:'전구를 직렬로 두 개 이으면 저항이 두 배가 되어 전류가 절반으로 줄어요. 그래서 <b>전구 한 개짜리가 더 밝아요</b>. 스위치가 닫힌 회로에서 밝기를 견주어 보세요.',
   setup:function(){ cqScene(function(){
     addPart('battery', 3, 2, 3, 5); addWire(3, 5, 3, 6); addWire(3, 6, 6, 6);
     addPart('bulb', 6, 6, 9, 6); addWire(9, 6, 16, 6); addWire(16, 6, 16, 1); addWire(16, 1, 11, 1);
     addPart('switch', 11, 1, 8, 1).props.closed = false; addWire(8, 1, 3, 1); addWire(3, 1, 3, 2);
     addPart('battery', 3, 9, 3, 12); addWire(3, 12, 3, 13); addWire(3, 13, 5, 13);
     addPart('bulb', 5, 13, 8, 13); addWire(8, 13, 10, 13); addPart('bulb', 10, 13, 13, 13);
     addWire(13, 13, 16, 13); addWire(16, 13, 16, 8); addWire(16, 8, 11, 8);
     addPart('switch', 11, 8, 8, 8).props.closed = false; addWire(8, 8, 3, 8); addWire(3, 8, 3, 9);
   }); },
   reveal:function(){ cqSwitches(true); }},
  {id:'cir-two-batt', lv:1, title:'전지 한 개 vs 두 개', kind:'choice', answer:1,
   choices:['위 회로(전지 한 개)의 전구', '아래 회로(전지 두 개를 한 줄로)의 전구', '둘 다 똑같다'],
   text:'같은 전구에 위 회로는 전지 <b>한 개</b>, 아래 회로는 전지 <b>두 개를 한 줄로(직렬)</b> 이었어요. 스위치를 닫으면 어느 쪽 전구가 더 밝을까요?',
   hint:'전지를 한 줄로 이으면 전구에 걸리는 전압이 어떻게 될까요?',
   explain:'전지를 직렬로 두 개 이으면 전압이 두 배(1.5 V → 3 V)가 되어 전류도 두 배가 흘러요. 그래서 <b>아래 전구가 더 밝아요</b>. 대신 전지는 더 빨리 닳아요.',
   setup:function(){ cqScene(function(){
     addPart('battery', 3, 2, 3, 5); addWire(3, 5, 3, 6); addWire(3, 6, 6, 6);
     addPart('bulb', 6, 6, 9, 6); addWire(9, 6, 16, 6); addWire(16, 6, 16, 1); addWire(16, 1, 11, 1);
     addPart('switch', 11, 1, 8, 1).props.closed = false; addWire(8, 1, 3, 1); addWire(3, 1, 3, 2);
     addPart('battery', 3, 9, 3, 11); addPart('battery', 3, 11, 3, 13); addWire(3, 13, 6, 13);
     addPart('bulb', 6, 13, 9, 13); addWire(9, 13, 16, 13); addWire(16, 13, 16, 8); addWire(16, 8, 11, 8);
     addPart('switch', 11, 8, 8, 8).props.closed = false; addWire(8, 8, 3, 8); addWire(3, 8, 3, 9);
   }); },
   reveal:function(){ cqSwitches(true); }},
  {id:'cir-parallel-off', lv:1, title:'한 전구를 끄면', kind:'choice', answer:2,
   choices:['오른쪽 전구도 꺼진다', '오른쪽 전구가 더 밝아진다', '오른쪽 전구는 그대로 켜져 있다', '오른쪽 전구가 깜빡인다'],
   text:'전구 두 개를 <b>갈라서(병렬)</b> 이었어요. 왼쪽 전구 아래 스위치를 열어 왼쪽 전구만 끄면, 오른쪽 전구는 어떻게 될까요?',
   hint:'병렬에서는 전구마다 전지로 돌아가는 길이 따로 있어요.',
   explain:'병렬 회로는 전구마다 길이 따로 있어서, 한 길을 끊어도 다른 전구는 <b>그대로 켜져 있어요</b>. 집의 전등과 콘센트가 이렇게 이어져 있어서 방 불을 꺼도 냉장고는 돌아가요.',
   setup:function(){ cqScene(function(){
     addPart('battery', 3, 9, 3, 6); addWire(3, 6, 3, 3); addWire(3, 3, 13, 3);
     addPart('bulb', 8, 3, 8, 6); addPart('switch', 8, 6, 8, 9); addWire(8, 9, 8, 12);
     addPart('bulb', 13, 3, 13, 6); addWire(13, 6, 13, 12);
     addWire(13, 12, 3, 12); addWire(3, 12, 3, 9);
   }); },
   reveal:function(){ cqSwitches(false); }},
  {id:'cir-ohm', lv:2, title:'옴의 법칙', kind:'num', unit:'mA', answer:150, tol:4,
   text:'3 V 전지에 <b>20 Ω</b> 저항을 이었어요. 전류계에는 몇 mA 가 나올까요? (1 A = 1000 mA)',
   hint:'전류 I = 전압 V ÷ 저항 R 이에요.',
   explain:'I = V ÷ R = 3 ÷ 20 = 0.15 A = <b>150 mA</b>. 저항이 두 배가 되면 전류는 절반이 돼요.',
   setup:function(){ cqScene(function(){
     addPart('battery', 3, 9, 3, 6).props.V = 3; addWire(3, 6, 3, 3); addWire(3, 3, 6, 3);
     addPart('ammeter', 6, 3, 9, 3); addWire(9, 3, 11, 3);
     addPart('resistor', 11, 3, 14, 3).props.R = 20;
     addWire(14, 3, 17, 3); cqRing(3, 12, 17); addWire(3, 12, 3, 9);
   }); },
   reveal:function(){ cqValues(true); }},
  {id:'cir-series-current', lv:2, title:'직렬 전류', kind:'num', unit:'mA', answer:75, tol:3,
   text:'1.5 V 전지에 <b>10 Ω</b> 전구 두 개를 한 줄로(직렬) 이었어요. 전류계에는 몇 mA 가 나올까요?',
   hint:'직렬로 이으면 전체 저항은 두 저항을 더한 값이에요.',
   explain:'전체 저항 = 10 + 10 = 20 Ω, I = 1.5 ÷ 20 = 0.075 A = <b>75 mA</b>. 직렬에서는 어느 자리에서 재도 전류가 같아요.',
   setup:function(){ cqScene(function(){
     addPart('battery', 3, 9, 3, 6); addWire(3, 6, 3, 4); addWire(3, 4, 4, 4);
     addPart('ammeter', 4, 4, 6, 4); addWire(6, 4, 7, 4);
     addPart('bulb', 7, 4, 10, 4); addWire(10, 4, 11, 4); addPart('bulb', 11, 4, 14, 4);
     addWire(14, 4, 17, 4); cqRing(4, 12, 17); addWire(3, 12, 3, 9);
   }); },
   reveal:function(){ cqValues(true); }},
  {id:'cir-parallel-total', lv:2, title:'병렬 전체 전류', kind:'num', unit:'mA', answer:300, tol:8,
   text:'1.5 V 전지에 <b>10 Ω</b> 전구 두 개를 갈라서(병렬) 이었어요. 전지에서 나오는 전체 전류(전류계)는 몇 mA 일까요?',
   hint:'병렬에서는 전구마다 전지 전압 1.5 V 가 그대로 걸려요. 각 전구의 전류를 구해 더해 보세요.',
   explain:'전구 하나에 1.5 ÷ 10 = 150 mA, 두 갈래를 더하면 <b>300 mA</b>. 병렬로 이을수록 전체 전류가 커져서, 멀티탭에 너무 많이 꽂으면 위험해요.',
   setup:function(){ cqScene(function(){
     addPart('battery', 3, 9, 3, 6); addPart('ammeter', 3, 6, 3, 4); addWire(3, 4, 3, 3); addWire(3, 3, 13, 3);
     addPart('bulb', 8, 3, 8, 6); addWire(8, 6, 8, 12);
     addPart('bulb', 13, 3, 13, 6); addWire(13, 6, 13, 12);
     addWire(13, 12, 3, 12); addWire(3, 12, 3, 9);
   }); },
   reveal:function(){ cqValues(true); }},
  {id:'cir-voltmeter', lv:2, title:'전압 나누기', kind:'num', unit:'V', answer:2, tol:0.08,
   text:'3 V 전지에 <b>10 Ω</b> 과 <b>20 Ω</b> 저항을 한 줄로 이었어요. 20 Ω 저항에 이은 전압계는 몇 V 를 가리킬까요?',
   hint:'먼저 전체 전류를 구하세요(3 ÷ 30). 그다음 V = I × R.',
   explain:'전류 = 3 ÷ 30 = 0.1 A, 20 Ω 에 걸리는 전압 = 0.1 × 20 = <b>2 V</b>. 직렬에서는 저항이 큰 쪽에 전압이 더 많이 걸려요(10 Ω 에는 1 V).',
   setup:function(){ cqScene(function(){
     addPart('battery', 3, 9, 3, 6).props.V = 3; addWire(3, 6, 3, 3); addWire(3, 3, 5, 3);
     addPart('resistor', 5, 3, 8, 3).props.R = 10; addWire(8, 3, 11, 3);
     addPart('resistor', 11, 3, 14, 3).props.R = 20; addWire(14, 3, 17, 3);
     cqRing(3, 12, 17); addWire(3, 12, 3, 9);
     addPart('voltmeter', 11, 7, 14, 7); addWire(11, 3, 11, 7); addWire(14, 3, 14, 7);
   }); },
   reveal:function(){ cqValues(true); }},
  {id:'cir-rc-tau', lv:3, title:'축전기 시간 상수', kind:'num', unit:'초', answer:1, tol:0.06,
   text:'<b>20 Ω</b> 저항과 <b>50 mF</b> 축전기를 1.5 V 전지에 이었어요. 스위치를 닫은 뒤, 축전기 전압이 최대의 약 63% 가 될 때까지 몇 초 걸릴까요? (시간 상수)',
   hint:'시간 상수 τ = R × C 예요. 50 mF = 0.05 F.',
   explain:'τ = RC = 20 × 0.05 = <b>1 초</b>. 1τ 에 63%, 2τ 에 86%, 3τ 에 95% 차요. 측정값 칸에서 1초쯤 축전기 전압이 0.95 V 근처인지 보세요.',
   setup:function(){ cqScene(function(){
     addPart('battery', 3, 9, 3, 6); addWire(3, 6, 3, 3); addWire(3, 3, 6, 3);
     addPart('switch', 6, 3, 9, 3).props.closed = false; addWire(9, 3, 11, 3);
     addPart('resistor', 11, 3, 14, 3).props.R = 20;
     addWire(14, 3, 16, 3); addWire(16, 3, 16, 6);
     addPart('capacitor', 16, 6, 16, 9).props.C = 0.05;
     addWire(16, 9, 16, 12); addWire(16, 12, 3, 12); addWire(3, 12, 3, 9);
   }); },
   reveal:function(){
     cqValues(true);
     els.forEach(function(e){ if (e.type === 'capacitor') e.state = {vc:0}; });
     simTime = 0; cqSwitches(true);
   }}
];
LabQuest.init({
  lab:'circuit', quests:CIR_QUESTS,
  mount:document.querySelector('main.layout'), button:document.querySelector('.levels'),
  level:function(){ return level; }, setLevel:setLevel, hide:['measCard'],
  onSolved:function(){ save(); }
});
