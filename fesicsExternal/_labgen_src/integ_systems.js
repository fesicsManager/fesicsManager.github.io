// 고1 통합과학 — Ⅲ. 시스템과 상호작용 (3·6화) 실험 정의
module.exports = {
  folder: 'high1Integ',
  suffix: '고1 통합과학',
  principle: '과학 원리',
  anim: 1800,
  labs: [

/* ===================== 27. 탄소 순환 (Systems Ep03) ===================== */
{
  file: '27_carbon_cycle_reservoir_lab_IntegSci1_Systems_Ep03.html',
  title: '탄소를 따라가 보기',
  intro: '지권에 묻혀 있던 탄소를 태우면 기권으로 올라가고, 그중 일부는 수권과 생물권으로 옮겨 갑니다. 화석 연료 사용량과 숲의 면적을 바꿔 가며 몇십 년 뒤 대기 이산화 탄소 농도가 어떻게 되는지 계산해 보세요.',
  sceneNote: '지권·기권·수권·생물권을 상자 네 개로 나타낸 교육용 모형입니다. 저장량은 GtC(기가톤 탄소) 단위이고, 대기 탄소 2.13 GtC가 약 1 ppm에 해당합니다.',
  runLabel: '시간 보내기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 네 개의 권을 오가는 탄소</h3>
<p>지구 시스템은 <b>지권·기권·수권·생물권</b>이 서로 물질과 에너지를 주고받는 구조예요. 탄소는 그 사이를 끊임없이 오가는데, 원래는 들어오는 양과 나가는 양이 균형을 이뤄 대기 농도가 거의 일정했어요. 그런데 수억 년 동안 <b>지권에 묻혀 있던</b> 화석 연료를 태우면서 기권으로 탄소가 빠르게 더해졌어요. 수권(바다)과 생물권(숲)이 그중 절반쯤을 받아 주지만 나머지는 대기에 남아 농도가 올라가요.</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>대기 탄소 2.13 GtC = 약 1 ppm. 산업화 이전 280 ppm(약 596 GtC)에서 지금은 420 ppm 가까이 올라왔어요.</li>
<li>해마다 배출한 탄소의 약 <b>절반</b>만 대기에 남고, 나머지는 바다와 육상 생태계가 흡수해요.</li>
<li>흡수는 농도가 높을수록 빨라져요: <span class="fx-formula">흡수량 = (A − A₀) ÷ τ</span>. 이 실험은 τ = 50년으로 두었어요.</li>
<li>숲을 베면 나무에 저장된 탄소가 기권으로 나오고, 흡수해 주던 능력도 함께 줄어 두 배로 불리해져요.</li>
<li>기온은 농도의 로그에 비례해요: <span class="fx-formula">ΔT = 3.0 × log₂(C ÷ 280)</span>.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p>해마다 <span class="fx-formula">A ← A + 배출 + 숲손실 − (A − A₀) ÷ τ<sub>숲</sub></span>로 갱신하고, <span class="fx-formula">ppm = A ÷ 2.13</span>, <span class="fx-formula">ΔT = 3.0 × log₂(ppm ÷ 280)</span>로 바꿉니다.</p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 저장고를 네 상자로 줄이고 흡수를 하나의 시간 상수 τ로 뭉뚱그린 <b>아주 단순한 모형</b>이에요. 실제 기후 모형은 바다의 깊이별 순환, 해양 산성화로 흡수 능력이 떨어지는 효과, 토양 탄소 등을 따로 다뤄요.<br>
· 기온 민감도 3.0 °C는 현재 연구에서 대략 2~5 °C로 폭이 있는 값이에요. 실제 기온은 늦게 따라오는 지연도 있어요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>석회암(지권)은 아주 오랜 시간 바다 생물의 껍데기가 쌓여 만들어진 탄소 저장고예요. 시멘트를 만들 때 이 탄소가 다시 기권으로 나와요.</li>
<li>화산 폭발은 기권에 이산화 탄소와 함께 햇빛을 가리는 먼지를 뿜어, 몇 해 동안 여름 기온을 낮추기도 했어요.</li>
</ul>`,
  js: `
var A0 = 596, PPMC = 2.13, TAU = 50, BIO0 = 550;
var EMIT = [0, 5, 10, 15];
var FOR = [{n:'숲 10 % 늘림', k:1.1}, {n:'그대로', k:1.0}, {n:'숲 20 % 벰', k:0.8}];
return {
  sceneHeight: 470,
  minRec: 4,
  idle: '화석 연료 사용량과 숲의 변화, 흘려보낼 햇수를 정하고 <b>시간 보내기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 배출량과 햇수를 바꿔 가며 기록하세요.',
  params: [
    {key:'e', type:'seg', label:'해마다 태우는 화석 연료(탄소)', cols:4, value:2, options:EMIT.map(function(v){ return v + ' GtC'; })},
    {key:'k', type:'seg', label:'숲(생물권)의 변화', cols:3, value:1, options:FOR.map(function(x){ return x.n; })},
    {key:'y', type:'range', label:'흘려보낼 햇수', min:10, max:200, step:10, value:100, fmt:function(v){ return v + '년'; },
      note:'산업화 이전 대기 탄소 596 GtC(280 ppm)에서 출발합니다. 숲을 베면 저장된 탄소가 기권으로 나옵니다.'}
  ],
  compute: function(p){
    var E = EMIT[p.e], F = FOR[p.k], yr = p.y;
    var A = 875, ocean = 0, bio = 0;                    // 2020년 무렵(약 411 ppm)에서 시작
    var start = A;
    var bioLoss = BIO0 * (1 - F.k), perYear = bioLoss / Math.min(yr, 50);
    var tau = TAU / F.k, absorbed = 0, fossil = 0, land = 0;
    for (var t = 0; t < yr; t++){
      var extra = t < Math.min(yr, 50) ? perYear : 0;
      var sink = (A - A0) / tau;
      A = A + E + extra - sink;
      absorbed += sink; fossil += E; land += extra;        // 화석 연료와 토지 이용을 따로 센다
      ocean += sink * 0.6; bio += sink * 0.4;
    }
    var released = fossil + land;
    var ppm = A / PPMC, dT = 3.0 * Math.log(ppm / 280) / Math.log(2);
    return {E:E, F:F, yr:yr, A:A, start:start, dA:A - start, ppm:ppm, ppm0:start / PPMC,
      dT:dT, dT0:3.0 * Math.log(start / PPMC / 280) / Math.log(2),
      released:released, fossil:fossil, land:land, absorbed:absorbed, ocean:ocean, bio:bio,
      stay:released > 0 ? (A - start) / released : 0, bioLoss:bioLoss};
  },
  draw: function(c, W, H, p, r, tau){
    var bw = Math.min(190, (W - 80) / 4), gap = (W - 60 - bw * 4) / 3, oy = 70;
    var boxes = [
      {n:'기권 (대기)', v:r ? r.start + (r.A - r.start) * tau : 875, col:'#3A8FB7', unit:'GtC'},
      {n:'수권 (바다)', v:38000 + (r ? r.ocean * tau : 0), col:'#2B5FA3', unit:'GtC'},
      {n:'생물권 (숲·흙)', v:BIO0 + (r ? (r.bio - r.bioLoss) * tau : 0), col:'#2E9E78', unit:'GtC'},
      {n:'지권 (화석 연료)', v:4000 - (r ? r.fossil * tau : 0), col:'#A8702F', unit:'GtC'}
    ];
    boxes.forEach(function(b, i){
      var x = 30 + i * (bw + gap);
      c.fillStyle = '#F7F9FC'; c.fillRect(x, oy, bw, 120);
      c.strokeStyle = b.col; c.lineWidth = 2; c.strokeRect(x, oy, bw, 120);
      txt(c, b.n, x + bw / 2, oy - 12, {align:'center', color:b.col, bold:true});
      txt(c, Math.round(b.v).toLocaleString(), x + bw / 2, oy + 60, {align:'center', bold:true});
      txt(c, b.unit, x + bw / 2, oy + 86, {align:'center', color:'#4A5868'});
      if (i < 3) arrow(c, x + bw + 4, oy + 60, x + bw + gap - 4, oy + 60, '#8C99A8', 2);
    });
    arrow(c, 30 + 3 * (bw + gap) + bw / 2, oy + 128, 30 + bw / 2, oy + 128, '#C8463D', 2.5);
    txt(c, '태우면 지권 → 기권', W / 2, oy + 152, {align:'center', color:'#C8463D', bold:true});
    if (!r){ txt(c, '화석 연료를 태우면 오랫동안 갇혀 있던 탄소가 대기로 나와요.', 30, H - 18, {color:'#4A5868'}); return; }
    var yy = oy + 198;
    txt(c, Math.round(r.yr * tau) + '년 경과 · 대기 ' + f(r.ppm0 + (r.ppm - r.ppm0) * tau, 0) + ' ppm', 30, yy, {bold:true, color:'#3A8FB7'});
    if (tau < 1) return;
    txt(c, '화석 연료 ' + Math.round(r.fossil).toLocaleString() + ' GtC + 숲 ' + (r.land >= 0 ? '방출 ' : '흡수 ') + Math.round(Math.abs(r.land)).toLocaleString() + ' GtC · 수권·생물권이 흡수 ' + Math.round(r.absorbed).toLocaleString() + ' GtC', 30, yy + 32, {});
    txt(c, '대기 탄소 변화 ' + sgn(r.dA, 0) + ' GtC' + (r.released > 0 ? ' (더해진 양의 ' + f(r.stay * 100, 0) + ' %)' : '') + ' → ' + f(r.ppm, 0) + ' ppm', 30, yy + 62,
      {bold:true, color:'#C8463D'});
    txt(c, '산업화 이전 대비 기온 ' + sgn(r.dT, 2) + ' °C (지금 시작점은 ' + sgn(r.dT0, 2) + ' °C)', 30, H - 14, {color:'#4A5868'});
  },
  stats: function(p, r){
    return [['해마다 배출(탄소)', r.E + ' GtC'], ['숲의 변화', r.F.n], ['흘려보낸 햇수', r.yr + '년'],
      ['숲이 잃은 탄소', f(r.bioLoss, 0) + ' GtC'],
      ['화석 연료 배출 누적', Math.round(r.fossil).toLocaleString() + ' GtC', PAL[4]],
      ['숲의 변화로 드나든 탄소', sgn(r.land, 0) + ' GtC (+는 방출, −는 흡수)'],
      ['수권·생물권 흡수 합계', Math.round(r.absorbed).toLocaleString() + ' GtC', PAL[1]],
      ['대기 탄소 변화', sgn(r.dA, 0) + ' GtC'],
      ['더해진 양 중 대기 잔류 비율', r.released > 0 ? f(r.stay * 100, 1) + ' %' : '—', PAL[6]],
      ['처음 대기 농도', f(r.ppm0, 0) + ' ppm'], ['나중 대기 농도', f(r.ppm, 0) + ' ppm', PAL[0]],
      ['기온 변화 (산업화 이전 대비)', sgn(r.dT, 2) + ' °C', PAL[4]]];
  },
  columns: ['배출 (GtC/년)', '숲', '햇수', '화석 누적 (GtC)', '숲 (GtC)', '흡수 (GtC)', '대기 변화 (GtC)', '잔류율 (%)', '농도 (ppm)', 'ΔT (°C)'],
  record: function(p, r){
    return {E:r.E, forest:r.F.n, fk:r.F.k, yr:r.yr, rel:r.released, fossil:r.fossil, land:r.land, abs:r.absorbed, dA:r.dA, stay:r.stay, ppm:r.ppm, dT:r.dT};
  },
  row: function(d){ return [d.E, d.forest, d.yr, Math.round(d.fossil).toLocaleString(), sgn(d.land, 0), Math.round(d.abs).toLocaleString(),
    sgn(d.dA, 0), d.rel > 0 ? f(d.stay * 100, 1) : '—', f(d.ppm, 0), sgn(d.dT, 2)]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('배출한 양과 대기에 남은 양', '<canvas class="chart" id="ch1" role="img" aria-label="배출 합계와 대기 증가량 산점도"></canvas><ul class="readout" id="ro1"></ul><p class="ask">배출한 탄소가 모두 대기에 남지는 않습니다. 나머지는 어느 권으로 갔을까요?</p>') +
      card('농도와 기온', '<canvas class="chart" id="ch2" role="img" aria-label="농도의 로그와 기온 변화 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">가로축은 농도를 2배씩 센 값입니다. 농도가 2배가 되면 기온은 몇 도 오를까요?</p>') +
      card('숲이 하는 두 가지 일', '<div id="ro3"></div><p class="ask">숲을 베면 왜 두 가지로 불리해질까요? 배출을 늘린 것과 흡수를 줄인 것을 나눠 설명해 보세요.</p>') + '</div>';
    var bf = groupBy(rec, function(d){ return d.forest; }), s1 = [], r1 = [], ci = 0;
    Object.keys(bf).forEach(function(k){
      var g = bf[k], col = PAL[ci++ % PAL.length];
      s1.push({color:col, pts:g.map(function(d){ return {x:d.fossil, y:d.dA}; })});
      var sm = mean(g.filter(function(d){ return d.rel > 0; }).map(function(d){ return d.stay; }));
      if (!isNaN(sm)) r1.push('<li>' + dot(col) + k + ': 평균 잔류율 <b>' + f(sm * 100, 1) + ' %</b></li>');
    });
    drawScatter($('ch1'), {xLabel:'화석 연료 누적 배출 (GtC)', yLabel:'대기 탄소 변화 (GtC)', series:s1});
    $('ro1').innerHTML = (r1.length ? r1.join('') : '<li>배출량을 바꿔 기록해 보세요.</li>') +
      '<li>나머지는 <b>수권(바다)</b>과 <b>생물권(숲·흙)</b>이 흡수했어요. 네 권이 서로 주고받는다는 뜻이에요.</li>' +
      '<li>흡수는 농도 차이에 비례하므로, 배출을 멈춰도 농도가 곧바로 산업화 이전으로 돌아가지는 않아요.</li>';
    var pts2 = rec.map(function(d){ return {x:Math.log(d.ppm / 280) / Math.log(2), y:d.dT}; });
    drawScatter($('ch2'), {xLabel:'log₂(농도 ÷ 280 ppm)', yLabel:'기온 변화 (°C)', tightX:true, tightY:true,
      series:[{color:PAL[4], pts:pts2}]});
    var r2 = [];
    if (distinct(rec.map(function(d){ return d.ppm; })) >= 2){
      var L = linfit(pts2);
      r2.push('<li>직선의 기울기 <b>' + f(L.k, 2) + ' °C</b> — 농도가 <b>2배</b>가 될 때마다 그만큼 오른다는 뜻이에요.</li>');
    } else r2.push('<li>배출량이나 햇수를 바꿔 농도가 다른 기록을 2개 이상 모아 보세요.</li>');
    var mx = rec.slice().sort(function(a, b){ return b.ppm - a.ppm; })[0];
    r2.push('<li>내 기록 중 가장 높은 농도: <b>' + f(mx.ppm, 0) + ' ppm</b> (ΔT ' + sgn(mx.dT, 2) + ' °C, 배출 ' + mx.E + ' GtC/년 · ' + mx.yr + '년)</li>');
    $('ro2').innerHTML = r2.join('');
    var rows = [];
    Object.keys(bf).forEach(function(k){
      var g = bf[k];
      rows.push([k, g.length + '개', f(mean(g.map(function(d){ return d.fossil; })), 0) + ' GtC',
        f(mean(g.map(function(d){ return d.abs; })), 0) + ' GtC', f(mean(g.map(function(d){ return d.ppm; })), 0) + ' ppm',
        sgn(mean(g.map(function(d){ return d.dT; })), 2) + ' °C']);
    });
    $('ro3').innerHTML = tableHTML(['숲의 변화', '기록 수', '평균 화석 누적 배출', '평균 흡수', '평균 농도', '평균 ΔT'], rows) +
      '<p class="note">숲을 베면 ① 나무에 저장된 탄소가 기권으로 나오고 ② 흡수 능력(τ)까지 줄어요. 반대로 숲을 늘리면 두 가지가 함께 좋아져요.</p>';
  }
};`
},

/* ===================== 28. 효소 (Systems Ep06) ===================== */
{
  file: '28_enzyme_catalase_lab_IntegSci1_Systems_Ep06.html',
  title: '감자즙과 과산화 수소',
  intro: '감자즙에 든 카탈레이스는 과산화 수소를 물과 산소로 빠르게 분해합니다. 온도와 pH, 과산화 수소의 농도와 감자즙의 양을 바꿔 가며 2분 동안 모인 산소 부피를 재어 보세요.',
  sceneNote: '2분 동안 모은 산소 부피로 반응 속도를 잽니다. 60 °C를 넘으면 효소 단백질이 변성되어 식혀도 되살아나지 않습니다.',
  runLabel: '2분 동안 반응시키기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 효소는 활성화 에너지를 낮추는 생체 촉매</h3>
<p>과산화 수소는 스스로도 물과 산소로 분해되지만 아주 느려요. <b>효소</b>는 반응이 넘어야 할 언덕(활성화 에너지)을 낮춰 같은 반응을 수만 배 빠르게 만들어요. 효소는 <b>기질과 모양이 맞는 자리</b>에서만 작용하므로 한 효소는 한 종류의 반응만 도와요(기질 특이성). 효소는 단백질이라 <b>온도와 pH</b>에 민감해서, 최적 조건에서 가장 빠르고 너무 뜨겁거나 산·염기가 세면 <b>구조가 풀려 되돌릴 수 없어요</b>(변성).</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>온도를 올리면 분자 충돌이 늘어 빨라지지만, 약 40 °C를 넘으면 변성이 이기기 시작해 속도가 <b>꺾여요</b>.</li>
<li>카탈레이스의 최적 pH는 7 근처예요. pH 3이나 pH 9에서는 활성이 크게 떨어져요.</li>
<li>기질(과산화 수소) 농도를 올리면 처음에는 빨라지다가 효소의 자리가 모두 차서 더는 빨라지지 않아요(포화).</li>
<li>효소 양을 2배로 하면 속도는 거의 2배가 돼요. 효소는 반응에서 <b>소모되지 않기</b> 때문이에요.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p><span class="fx-formula">속도 = V<sub>max</sub> × [S] ÷ (K<sub>m</sub> + [S]) × 온도인자 × pH인자</span>, V<sub>max</sub> ∝ 감자즙 양, K<sub>m</sub> = 1.0 %, <span class="fx-formula">산소 부피 = 속도 × 2분</span></p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 온도 인자와 pH 인자를 종 모양 곡선으로 단순화했어요. 실제로는 반응 속도 증가(아레니우스)와 변성 속도가 겹친 결과이고, 변성은 <b>시간에도</b> 의존해요.<br>
· 2분 동안 기질이 줄어드는 것을 넣지 않아 속도를 일정하다고 봤어요. 실제 측정에서는 처음 30초의 기울기(초기 속도)를 씁니다.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>상처에 소독약(과산화 수소)을 바르면 거품이 이는 것은 우리 몸의 카탈레이스가 분해하며 산소를 내기 때문이에요.</li>
<li>열이 40 °C를 넘으면 위험한 까닭, 김치가 냉장고에서 천천히 익는 까닭도 효소의 온도 의존성으로 설명돼요.</li>
</ul>`,
  js: `
var PH = [3, 5, 7, 9];
var SUB = [0.5, 1, 2, 4];
var ENZ = [1, 2, 4];
var KM = 1.0, VMAX1 = 14;
function fT(T){
  var g = Math.exp(-Math.pow(T - 40, 2) / (2 * 18 * 18));
  if (T > 60) g *= Math.exp(-(T - 60) / 8);
  return g;
}
function fPH(ph){ return Math.exp(-Math.pow(ph - 7, 2) / (2 * 1.5 * 1.5)); }
return {
  sceneHeight: 470,
  minRec: 4,
  idle: '온도·pH·농도·감자즙 양을 정하고 <b>2분 동안 반응시키기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 온도와 농도를 바꿔 가며 기록하세요.',
  params: [
    {key:'T', type:'range', label:'온도', min:0, max:90, step:5, value:40, fmt:function(v){ return v + ' °C'; }},
    {key:'p', type:'seg', label:'pH', cols:4, value:2, options:PH.map(function(v){ return 'pH ' + v; })},
    {key:'s', type:'seg', label:'과산화 수소 농도', cols:4, value:1, options:SUB.map(function(v){ return v + ' %'; })},
    {key:'e', type:'seg', label:'감자즙(효소) 양', cols:3, value:1, options:ENZ.map(function(v){ return v + ' mL'; }),
      note:'2분 동안 모인 산소 부피로 반응 속도를 잽니다. 60 °C가 넘으면 효소가 변성되며, 한 번 변성된 효소는 식혀도 돌아오지 않습니다. <b>실행할 때마다 새 감자즙을 쓴다고 가정</b>하므로, 다음 실행에서 온도를 낮추면 다시 정상 효소로 시작합니다.'}
  ],
  compute: function(p){
    var T = p.T, ph = PH[p.p], S = SUB[p.s], E = ENZ[p.e];
    var tf = fT(T), pf = fPH(ph), sf = S / (KM + S);
    var rate = VMAX1 * E * tf * pf * sf;
    return {T:T, ph:ph, S:S, E:E, tf:tf, pf:pf, sf:sf, rate:rate, vol:rate * 2,
      denat:T > 60, vmax:VMAX1 * E * tf * pf};
  },
  draw: function(c, W, H, p, r, tau){
    var bx = 50, by = 90, bw = 150, bh = 170;
    // 비커
    c.fillStyle = '#EAF3F9'; c.fillRect(bx, by + 40, bw, bh - 40);
    c.strokeStyle = '#5B6776'; c.lineWidth = 2; c.strokeRect(bx, by + 40, bw, bh - 40);
    txt(c, '과산화 수소 ' + SUB[p.s] + ' % + 감자즙 ' + ENZ[p.e] + ' mL', bx, by + 26, {color:'#4A5868'});
    txt(c, p.T + ' °C · pH ' + PH[p.p], bx, by + bh + 34, {color:'#4A5868'});
    // 거품
    if (r){
      var n = Math.min(40, Math.round(r.rate * 1.4));
      for (var i = 0; i < n; i++){
        var ph2 = ((tau * 1.4 + i * 0.09) % 1);
        c.fillStyle = 'rgba(46,158,120,' + (0.25 + 0.5 * (1 - ph2)) + ')';
        c.beginPath();
        c.arc(bx + 16 + ((i * 37) % (bw - 32)), by + bh - ph2 * (bh - 50), 3 + (i % 3), 0, Math.PI * 2);
        c.fill();
      }
    }
    // 눈금 실린더
    var gx = bx + bw + 70, gw = 66, gh = 210, gy = by - 10;
    c.fillStyle = '#F7F9FC'; c.fillRect(gx, gy, gw, gh);
    c.strokeStyle = '#5B6776'; c.lineWidth = 2; c.strokeRect(gx, gy, gw, gh);
    for (var v = 0; v <= 60; v += 10){
      var yy = gy + gh - (v / 60) * gh;
      seg(c, gx, yy, gx + 12, yy, '#8C99A8', 1);
      txt(c, String(v), gx - 6, yy + 6, {align:'right', color:'#4A5868'});
    }
    txt(c, '모인 산소 (mL)', gx + gw / 2, gy - 18, {align:'center', color:'#4A5868'});
    if (r){
      var vv = Math.min(60, r.vol * tau);
      c.fillStyle = 'rgba(46,158,120,.45)';
      c.fillRect(gx + 2, gy + gh - (vv / 60) * gh, gw - 4, (vv / 60) * gh);
      txt(c, f(vv, 1) + ' mL', gx + gw / 2, gy + gh - (vv / 60) * gh - 8, {align:'center', bold:true, color:'#2E9E78'});
    }
    var mx = gx + gw + 40;
    if (mx < W - 180 && r){
      txt(c, '반응 속도', mx, gy + 20, {color:'#4A5868'});
      meter(c, mx, gy + 30, Math.min(180, W - mx - 12), f(r.rate, 1) + ' mL/분');
    }
    if (!r){ txt(c, '효소가 과산화 수소를 물과 산소로 분해해요.', bx, H - 18, {color:'#4A5868'}); return; }
    if (tau < 1) return;
    var yy2 = by + bh + 76;
    txt(c, '온도 인자 ' + f(r.tf, 2) + ' × pH 인자 ' + f(r.pf, 2) + ' × 기질 인자 ' + f(r.sf, 2) + ' × 효소 ' + r.E + ' mL', bx, yy2, {});
    txt(c, r.denat ? '60 °C를 넘겨 효소가 변성됐어요. 식혀도 되살아나지 않아요.'
      : (r.T >= 30 && r.T <= 50 && r.ph === 7 ? '최적 조건에 가까워 가장 빠르게 분해돼요.' : '최적 조건에서 벗어나 느려요.'),
      bx, H - 14, {bold:true, color:r.denat ? '#C8463D' : (r.T >= 30 && r.T <= 50 && r.ph === 7 ? '#2E9E78' : '#A8702F')});
  },
  stats: function(p, r){
    return [['온도', r.T + ' °C'], ['pH', 'pH ' + r.ph], ['과산화 수소 농도', r.S + ' %'], ['감자즙(효소)', r.E + ' mL'],
      ['온도 인자', f(r.tf, 3), PAL[4]], ['pH 인자', f(r.pf, 3), PAL[3]], ['기질 인자 [S]÷(Kₘ+[S])', f(r.sf, 3), PAL[0]],
      ['반응 속도', f(r.rate, 2) + ' mL/분', PAL[1]], ['2분 동안 모인 산소', f(r.vol, 1) + ' mL', PAL[1]],
      ['이 조건의 최대 속도(기질 충분할 때)', f(r.vmax, 2) + ' mL/분'],
      ['효소 상태', r.denat ? '변성 (되돌릴 수 없음)' : '정상', r.denat ? PAL[4] : PAL[1]]];
  },
  columns: ['T (°C)', 'pH', '[H₂O₂] (%)', '효소 (mL)', '속도 (mL/분)', '산소 (mL)', '상태'],
  record: function(p, r){ return {T:r.T, ph:r.ph, S:r.S, E:r.E, rate:r.rate, vol:r.vol, denat:r.denat}; },
  row: function(d){ return [d.T, d.ph, d.S, d.E, f(d.rate, 2), f(d.vol, 1), d.denat ? '변성' : '정상']; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('온도와 반응 속도', '<canvas class="chart" id="ch1" role="img" aria-label="온도와 반응 속도 산점도"></canvas><ul class="readout" id="ro1"></ul><p class="ask">온도를 올리면 처음에는 빨라지다가 어느 지점부터 뚝 떨어집니다. 이 두 구간에서 서로 다른 일이 일어나는 까닭은 무엇일까요?</p>') +
      card('기질 농도와 반응 속도', '<canvas class="chart" id="ch2" role="img" aria-label="과산화 수소 농도와 반응 속도 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">농도를 2배로 해도 속도가 2배가 되지 않는 구간이 있습니다. 효소의 어떤 성질 때문일까요?</p>') +
      card('pH와 효소 양', '<div id="ro3"></div><p class="ask">효소는 반응 뒤에도 그대로 남습니다. 효소 양과 속도의 관계가 기질 농도와 다른 까닭을 설명해 보세요.</p>') + '</div>';
    var be = groupBy(rec, function(d){ return d.E + '-' + d.ph + '-' + d.S; }), s1 = [], ci = 0, r1 = [];
    Object.keys(be).forEach(function(k){
      var g = be[k];
      if (g.length < 2) return;
      var col = PAL[ci++ % PAL.length];
      s1.push({color:col, pts:g.map(function(d){ return {x:d.T, y:d.rate}; })});
      var best = g.slice().sort(function(a, b){ return b.rate - a.rate; })[0];
      r1.push('<li>' + dot(col) + 'pH ' + g[0].ph + ' · ' + g[0].S + ' % · 효소 ' + g[0].E + ' mL: 가장 빠른 온도 <b>' + best.T + ' °C</b></li>');
    });
    if (!s1.length) s1 = [{color:PAL[4], pts:rec.map(function(d){ return {x:d.T, y:d.rate}; })}];
    drawScatter($('ch1'), {xLabel:'온도 (°C)', yLabel:'반응 속도 (mL/분)', series:s1});
    var hot = rec.filter(function(d){ return d.denat; });
    $('ro1').innerHTML = (r1.length ? r1.join('') : '<li>다른 조건은 그대로 두고 온도만 여러 번 바꿔 기록해 보세요.</li>') +
      '<li>40 °C 근처까지는 <b>분자 운동이 활발해져</b> 빨라지고, 그 위에서는 <b>효소 단백질이 풀려</b> 느려져요.</li>' +
      (hot.length ? '<li>60 °C를 넘긴 기록 ' + hot.length + '개는 <b>변성</b>이라 식혀도 되살아나지 않아요.</li>'
                  : '<li>70~90 °C로도 재어 보면 변성을 확인할 수 있어요.</li>');
    var bs = groupBy(rec.filter(function(d){ return !d.denat; }), function(d){ return d.E + '-' + d.ph + '-' + d.T; }), s2 = [], ci2 = 0, r2 = [];
    Object.keys(bs).forEach(function(k){
      var g = bs[k];
      if (distinct(g.map(function(d){ return d.S; })) < 2) return;
      var col = PAL[ci2++ % PAL.length];
      s2.push({color:col, pts:g.map(function(d){ return {x:d.S, y:d.rate}; })});
      var srt = g.slice().sort(function(a, b){ return a.S - b.S; });
      r2.push('<li>' + dot(col) + g[0].T + ' °C · pH ' + g[0].ph + ': ' + srt[0].S + ' % → ' + srt[srt.length-1].S + ' %일 때 속도 ' +
        f(srt[0].rate, 1) + ' → ' + f(srt[srt.length-1].rate, 1) + ' mL/분 (' + f(srt[srt.length-1].rate / Math.max(srt[0].rate, 1e-6), 1) + '배)</li>');
    });
    if (!s2.length) s2 = [{color:PAL[0], pts:rec.map(function(d){ return {x:d.S, y:d.rate}; })}];
    drawScatter($('ch2'), {xLabel:'과산화 수소 농도 (%)', yLabel:'반응 속도 (mL/분)', series:s2});
    $('ro2').innerHTML = (r2.length ? r2.join('') : '<li>온도·pH·효소 양은 그대로 두고 농도만 바꿔 기록해 보세요.</li>') +
      '<li>농도가 낮을 때는 거의 비례하다가, 높아지면 효소의 자리가 모두 차서 더 빨라지지 않아요(<b>포화</b>).</li>';
    var bp = groupBy(rec, function(d){ return d.ph; }), rows = [];
    Object.keys(bp).sort(function(a, b){ return a - b; }).forEach(function(k){
      var g = bp[k];
      rows.push(['pH ' + k, g.length + '개', f(mean(g.map(function(d){ return d.rate; })), 2) + ' mL/분',
        f(Math.max.apply(null, g.map(function(d){ return d.rate; })), 2) + ' mL/분']);
    });
    var bE = groupBy(rec, function(d){ return d.E; }), rows2 = [];
    Object.keys(bE).sort(function(a, b){ return a - b; }).forEach(function(k){
      var g = bE[k];
      rows2.push([k + ' mL', g.length + '개', f(mean(g.map(function(d){ return d.rate; })), 2) + ' mL/분']);
    });
    $('ro3').innerHTML = '<div class="mtable"><h3>pH별</h3>' + tableHTML(['pH', '기록 수', '평균 속도', '가장 빠른 값'], rows) +
      '<h3>효소 양별</h3>' + tableHTML(['감자즙', '기록 수', '평균 속도'], rows2) + '</div>' +
      '<p class="note">카탈레이스의 최적 pH는 7 근처예요. 효소 양을 2배로 하면 속도도 거의 2배가 되는데, 직접적인 까닭은 <b>기질과 결합할 활성 부위 수가 2배</b>가 되기 때문이에요. 효소가 반응에서 소모되지 않는다는 것은 촉매의 또 다른 성질이고요.</p>';
  }
};`
}

  ]
};
