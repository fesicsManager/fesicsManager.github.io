/* 하늘 실험실 — 문제 풀기 (261124)
   정답은 모두 이 실험실의 천문 계산(sunDay·fullMoonDay)에서 바로 꺼낸다. 답을 넣으면
   그 날·그 위도로 하늘을 돌려 보여 주고, 가려 두었던 해·달 칸을 연다.
   sky_lab.html 의 전역 함수·변수(day, minute, lat, showSeason …)를 그대로 쓴다. */
(function(){
  var sc = document.getElementById('roNoon').closest('.card');
  if (sc && !sc.id) sc.id = 'sunCard';
})();
function skyGo(d, m, la, opt){
  playDay = false; playYear = false;
  document.getElementById('btnPlay').classList.remove('on');
  document.getElementById('btnYear').classList.remove('on');
  day = d; dayF = d; minute = m; lat = la;
  if (opt){
    if ('showSeason' in opt) showSeason = opt.showSeason;
    if ('showStars' in opt) showStars = opt.showStars;
    if ('showTrail' in opt) showTrail = opt.showTrail;
    if ('showMoon' in opt) showMoon = opt.showMoon;
  }
  ['btnSeason','btnStars','btnTrail','btnMoon'].forEach(function(id, i){
    document.getElementById(id).classList.toggle('on', [showSeason, showStars, showTrail, showMoon][i]);
  });
  dayKey = ''; syncLabels(); render();
}
function skyDayLenText(d, la){ var m = sunDay(d, la).dayMin; return Math.floor(m/60) + '시간 ' + (m%60) + '분'; }
function skyDec1(){ return dayOf(12, 1); }
var SKY_QUESTS = [
  {id:'sky-noon-dir', lv:1, title:'해가 가장 높을 때', kind:'choice', answer:2,
   choices:['동쪽', '서쪽', '남쪽', '북쪽'],
   text:'우리나라(서울)에서 하루 중 해가 <b>가장 높이</b> 떴을 때, 해는 하늘의 어느 쪽에 있을까요?',
   hint:'해는 동쪽에서 떠서 서쪽으로 져요. 그 가운데쯤, 가장 높이 올라갈 때를 생각해 보세요.',
   explain:'우리나라처럼 북반구 중위도에서는 해가 동쪽에서 떠서 <b>남쪽 하늘</b>을 지나 서쪽으로 져요. 가장 높을 때 해가 남쪽에 있어서 이때의 높이를 <b>남중 고도</b>라고 해요. 그래서 집을 남향으로 짓지요.',
   setup:function(){ skyGo(172, 400, 37.5, {showSeason:false}); },
   reveal:function(){ skyGo(172, sunDay(172, 37.5).noonMin, 37.5, {showSeason:false}); }},
  {id:'sky-polar', lv:1, title:'북극의 여름', kind:'choice', answer:1,
   choices:['해가 하루 종일 뜨지 않는다', '해가 하루 종일 지지 않는다', '우리나라와 똑같이 뜨고 진다', '해가 북쪽에서 떠서 남쪽으로 진다'],
   text:'6월 21일(하지), <b>북극 가까이</b>(북위 89°)에서는 해가 어떻게 움직일까요?',
   hint:'여름에는 북반구가 해 쪽으로 기울어 있어요. 북극은 그 맨 꼭대기예요.',
   explain:'하지 무렵 북극에서는 해가 지평선 아래로 내려가지 않고 하늘을 빙빙 돌아요. 밤에도 환한 이런 날을 <b>백야</b>라고 해요. 반대로 겨울에는 하루 종일 해가 안 뜨는 <b>극야</b>가 와요.',
   setup:function(){ skyGo(172, 60, 37.5, {showSeason:false}); },
   reveal:function(){ skyGo(172, 60, 89, {showSeason:true}); playDay = true; document.getElementById('btnPlay').classList.add('on'); }},
  {id:'sky-daylen', lv:1, title:'하지의 낮 길이', kind:'choice', answer:2,
   choices:['약 10시간', '약 12시간', '약 14시간 반', '약 18시간'],
   text:'6월 21일(하지) 서울에서 해가 떠 있는 시간(낮의 길이)은 얼마쯤일까요?',
   hint:'춘분·추분에는 낮과 밤이 거의 12시간씩이에요. 여름에는 낮이 길어져요. 하지만 서울은 북극이 아니에요.',
   explain:function(){ return '이 실험실 계산으로 서울 하지의 낮은 <b>' + skyDayLenText(172, 37.5) + '</b>이에요. 동지에는 ' + skyDayLenText(356, 37.5) + '밖에 안 돼요. 지구 자전축이 23.5° 기울어 있어서 계절마다 낮 길이가 달라져요.'; },
   setup:function(){ skyGo(80, 720, 37.5, {showSeason:false}); },
   reveal:function(){ skyGo(172, 720, 37.5, {showSeason:true}); }},
  {id:'sky-summer-noon', lv:2, title:'하지 남중 고도', kind:'num', unit:'°',
   answer:function(){ return sunDay(172, 37.5).maxAlt; }, tol:1.5,
   text:'서울(북위 37.5°)에서 <b>하지</b>(6월 21일)에 해의 남중 고도는 몇 도일까요?',
   hint:'남중 고도 ≈ 90° − 위도 + 23.5° (하지). 춘분·추분에는 90° − 위도예요.',
   explain:function(){ return '90 − 37.5 + 23.5 = 76° 쯤이에요. 이 실험실의 실제 계산값은 <b>' + sunDay(172, 37.5).maxAlt.toFixed(1) + '°</b> 예요. 여름 한낮의 해는 높이 떠서 그림자가 짧아요.'; },
   setup:function(){ skyGo(172, 480, 37.5, {showSeason:false}); },
   reveal:function(){ skyGo(172, sunDay(172, 37.5).noonMin, 37.5, {showSeason:true}); }},
  {id:'sky-winter-noon', lv:2, title:'동지 남중 고도', kind:'num', unit:'°',
   answer:function(){ return sunDay(356, 37.5).maxAlt; }, tol:1.5,
   text:'서울(북위 37.5°)에서 <b>동지</b>(12월 22일)에 해의 남중 고도는 몇 도일까요?',
   hint:'동지에는 해가 23.5° 만큼 남쪽으로 내려가요. 남중 고도 ≈ 90° − 위도 − 23.5°.',
   explain:function(){ return '90 − 37.5 − 23.5 = 29° 쯤이에요. 실제 계산값은 <b>' + sunDay(356, 37.5).maxAlt.toFixed(1) + '°</b>. 겨울 해는 낮게 떠서 햇빛이 비스듬히 들어오니 땅이 덜 데워져 추워요.'; },
   setup:function(){ skyGo(356, 540, 37.5, {showSeason:false}); },
   reveal:function(){ skyGo(356, sunDay(356, 37.5).noonMin, 37.5, {showSeason:true}); }},
  {id:'sky-equator', lv:2, title:'적도의 춘분', kind:'num', unit:'°',
   answer:function(){ return sunDay(80, 0).maxAlt; }, tol:1.5,
   text:'<b>적도</b>(위도 0°)에서 <b>춘분</b>(3월 21일)에 해의 남중 고도는 몇 도일까요?',
   hint:'춘분에는 남중 고도 ≈ 90° − 위도 예요. 위도가 0° 라면?',
   explain:function(){ return '90 − 0 = 90°, 해가 <b>거의 머리 위</b>를 지나요. 실험실 계산값은 ' + sunDay(80, 0).maxAlt.toFixed(1) + '° 예요(춘분 순간과 한낮이 딱 겹치지 않아 조금 차이가 나요). 이때는 한낮에 그림자가 거의 안 생겨요.'; },
   setup:function(){ skyGo(80, 480, 0, {showSeason:false}); },
   reveal:function(){ skyGo(80, sunDay(80, 0).noonMin, 0, {showSeason:true}); }},
  {id:'sky-fullmoon-rise', lv:2, title:'보름달이 뜨는 때', kind:'choice', answer:0,
   choices:['해 질 무렵', '한밤중(자정)', '해 뜰 무렵', '한낮(정오)'],
   text:'보름달은 하루 중 <b>언제</b> 동쪽 하늘에서 떠오를까요?',
   hint:'보름달은 지구를 사이에 두고 해의 <b>반대편</b>에 있어요.',
   explain:'보름달은 해와 정반대 쪽에 있어서, 해가 서쪽으로 질 때 동쪽에서 떠올라 밤새 보이고 해 뜰 무렵 서쪽으로 져요. 실험실에서 시각을 움직여 확인해 보세요.',
   setup:function(){ var d = fullMoonDay(dayOf(9, 1)); skyGo(d, 720, 37.5, {showMoon:true, showStars:false}); },
   reveal:function(){ var d = fullMoonDay(dayOf(9, 1)); var s = sunDay(d, 37.5).set; skyGo(d, (s || 1100) + 15, 37.5, {showMoon:true, showStars:true}); }},
  {id:'sky-dec-fullmoon', lv:2, title:'12월 보름달', kind:'num', unit:'일',
   answer:function(){ return monthDay(fullMoonDay(skyDec1()))[1]; }, tol:1,
   text:'2026년 <b>12월</b>의 보름달은 며칠일까요? 날짜 손잡이를 움직이며 하늘 그림의 달 모양을 살펴보세요.',
   hint:'달은 약 29.5일마다 같은 모양이 돼요. 2026년 첫 보름달은 1월 3일이에요. 그 뒤로 29.5일씩 더해 보세요.',
   explain:function(){ var md = monthDay(fullMoonDay(skyDec1())); return '2026년 12월 보름달은 <b>' + md[0] + '월 ' + md[1] + '일</b>이에요. 1월 3일에서 29.5일씩 11번 더하면 약 325일 뒤라 12월 하순이 돼요. 보름달은 음력 15일 무렵이라 양력 날짜는 해마다 달라요.'; },
   setup:function(){ skyGo(skyDec1(), 1260, 37.5, {showMoon:true, showStars:true}); },
   reveal:function(ok, v){ var d = ok ? fullMoonDay(skyDec1()) : dayOf(12, Math.max(1, Math.min(31, Math.round(v)))); skyGo(d, 1260, 37.5, {showMoon:true}); }}
];
LabQuest.init({
  lab:'sky', quests:SKY_QUESTS,
  mount:document.querySelector('main.layout'), button:document.querySelector('.levels'),
  level:function(){ return level; }, setLevel:setLevel, hide:['sunCard', 'moonCard'],
  onSolved:function(){ save(); }
});
