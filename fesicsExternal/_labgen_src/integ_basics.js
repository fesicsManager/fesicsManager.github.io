// 고1 통합과학 — Ⅰ. 과학의 기초 (2·3·4화) 실험 정의
module.exports = {
  folder: 'high1Integ',
  suffix: '고1 통합과학',
  principle: '과학 원리',
  anim: 1800,
  labs: [

/* ===================== 19. 기본량과 유도량 (Basics Ep02) ===================== */
{
  file: '19_units_derived_quantity_lab_IntegSci1_Basics_Ep02.html',
  title: '기본량으로 조립하는 유도량',
  intro: '수레가 달린 거리와 걸린 시간, 수레의 질량과 바닥에 닿는 넓이를 바꿔 가며 속력·운동량·운동 에너지·압력을 구합니다. 기본량 세 개(길이·시간·질량)만 재면 나머지 양이 어떻게 조립되는지 확인해 보세요.',
  sceneNote: '길이(m)·시간(s)·질량(kg)은 기본량이고, 속력·운동량·운동 에너지·압력은 이 셋을 곱하고 나눠 만든 유도량입니다. 중력 가속도는 9.8 m/s²로 두었습니다.',
  runLabel: '수레 출발',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 기본량 7개와 유도량</h3>
<p>국제단위계(SI)는 <b>길이(m)·질량(kg)·시간(s)·전류(A)·온도(K)·물질량(mol)·광도(cd)</b> 7개를 <b>기본량</b>으로 정하고, 나머지 모든 물리량은 이 7개를 곱하고 나눠 만든 <b>유도량</b>으로 봐요. 그래서 속력을 재는 새로운 기본 단위를 따로 두지 않고 <span class="fx-formula">m/s</span>처럼 조립해서 써요. 단위를 조립해 보면 그 양이 무엇을 곱하고 나눈 것인지가 그대로 드러나요.</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>속력 <span class="fx-formula">v = L ÷ t</span> — 3.0 m를 1.5 s에 가면 2.0 m/s. 단위 m/s.</li>
<li>같은 속력을 km/h로 쓰면 2.0 × 3.6 = 7.2 km/h. 1 km = 1000 m, 1 h = 3600 s이므로 <b>3.6배</b>가 돼요.</li>
<li>운동량 <span class="fx-formula">p = m·v</span> (kg·m/s), 운동 에너지 <span class="fx-formula">E = ½·m·v²</span> (J = kg·m²/s²).</li>
<li>무게 <span class="fx-formula">W = m·g</span> (N = kg·m/s²), 압력 <span class="fx-formula">P = W ÷ A</span> (Pa = N/m² = kg/(m·s²)).</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p><span class="fx-formula">v = L ÷ t</span>, <span class="fx-formula">v[km/h] = 3.6 v</span>, <span class="fx-formula">p = m v</span>, <span class="fx-formula">E = ½ m v²</span>, <span class="fx-formula">P = m·9.8 ÷ A</span></p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 수레가 처음부터 끝까지 <b>일정한 속력</b>으로 간다고 봤어요. 실제 수레는 출발할 때 가속되므로 L ÷ t는 그 구간의 <b>평균 속력</b>이에요.<br>
· 마찰과 공기 저항을 넣지 않았고, 접촉 넓이에 압력이 고르게 걸린다고 가정했어요. 실제로는 바퀴가 닿는 부분에 압력이 몰려요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>자동차 계기판의 km/h, 태풍 속보의 m/s는 같은 양을 다른 단위로 쓴 것이라 3.6만 곱하면 서로 바뀌어요.</li>
<li>눈 위를 걷는 스키와 압정 끝은 같은 무게라도 닿는 넓이가 달라 압력이 크게 달라져요.</li>
</ul>`,
  js: `
var MASS = [0.5, 1.0, 2.0, 5.0];
var AREA = [10, 25, 50];          // cm²
return {
  sceneHeight: 440,
  minRec: 4,
  idle: '거리·시간·질량·닿는 넓이를 정하고 <b>수레 출발</b>을 누르세요.',
  shortHint: '자유 탐구 탭에서 거리와 시간을 바꿔 가며 기록하세요.',
  params: [
    {key:'L', type:'range', label:'달린 거리 L', min:0.5, max:6, step:0.5, value:3, fmt:function(v){ return f(v,1) + ' m'; }},
    {key:'t', type:'range', label:'걸린 시간 t', min:0.5, max:6, step:0.5, value:1.5, fmt:function(v){ return f(v,1) + ' s'; }},
    {key:'m', type:'seg', label:'수레 질량 m', cols:4, value:1, options:MASS.map(function(v){ return f(v,1) + ' kg'; })},
    {key:'a', type:'seg', label:'바닥에 닿는 넓이 A', cols:3, value:1, options:AREA.map(function(v){ return v + ' cm²'; }),
      note:'질량과 넓이는 압력 계산에 쓰입니다. 같은 무게라도 닿는 넓이가 좁으면 압력이 커집니다.'}
  ],
  compute: function(p){
    var L = p.L, t = p.t, m = MASS[p.m], A = AREA[p.a] * 1e-4;
    var v = L / t, W = m * 9.8;
    return {L:L, t:t, m:m, Acm:AREA[p.a], A:A, v:v, kmh:v * 3.6, mom:m * v, E:0.5 * m * v * v, W:W, P:W / A};
  },
  draw: function(c, W, H, p, r, tau){
    var padL = 60, padR = 40, y = 210;
    var x0 = padL, x1 = W - padR;
    c.fillStyle = '#E6EBF1'; c.fillRect(0, y + 26, W, 10);
    seg(c, x0, y + 26, x0, y - 70, '#8C99A8', 2);
    seg(c, x1, y + 26, x1, y - 70, '#8C99A8', 2);
    txt(c, '출발선', x0 + 4, y - 78, {color:'#4A5868'});
    txt(c, '도착선', x1 - 4, y - 78, {color:'#4A5868', align:'right'});
    arrow(c, x0, y - 54, x1, y - 54, '#2B5FA3', 2);
    txt(c, 'L = ' + f(p.L, 1) + ' m', (x0 + x1) / 2, y - 62, {align:'center', bold:true, color:'#2B5FA3'});
    // 수레
    var k = r ? tau : 0, cx = x0 + (x1 - x0 - 70) * k, mm = MASS[p.m];
    var bw = 54 + mm * 4, bh = 26 + mm * 3;
    c.fillStyle = '#A8702F'; c.fillRect(cx, y + 24 - bh, bw, bh);
    c.strokeStyle = '#6E4A1E'; c.lineWidth = 2; c.strokeRect(cx, y + 24 - bh, bw, bh);
    c.fillStyle = '#2E3945';
    c.beginPath(); c.arc(cx + 14, y + 28, 9, 0, Math.PI * 2); c.fill();
    c.beginPath(); c.arc(cx + bw - 14, y + 28, 9, 0, Math.PI * 2); c.fill();
    txt(c, f(mm, 1) + ' kg', cx + bw / 2, y + 22 - bh / 2, {align:'center', color:'#fff', bold:true, base:'middle'});
    // 시계
    txt(c, '스톱워치', W - 16, 40, {align:'right', color:'#4A5868'});
    meter(c, W - 196, 50, 180, f(r ? p.t * tau : 0, 2) + ' s');
    if (!r) { txt(c, '기본량: 길이 L(m) · 시간 t(s) · 질량 m(kg)', 16, H - 20, {color:'#4A5868'}); return; }
    var yy = 300;
    txt(c, '속력 v = L ÷ t = ' + f(r.L, 1) + ' ÷ ' + f(r.t, 1) + ' = ' + f(r.v, 2) + ' m/s = ' + f(r.kmh, 1) + ' km/h', 16, yy, {bold:true, color:'#2B5FA3'});
    txt(c, '운동량 p = m v = ' + f(r.mom, 2) + ' kg·m/s · 운동 에너지 E = ½ m v² = ' + f(r.E, 2) + ' J', 16, yy + 32, {});
    txt(c, '무게 W = m g = ' + f(r.W, 1) + ' N · 압력 P = W ÷ A = ' + Math.round(r.P).toLocaleString() + ' Pa', 16, yy + 62, {color:'#2E9E78', bold:true});
    txt(c, '기본량 3개(m, s, kg)만 재서 유도량 4개를 얻었어요.', 16, H - 16, {color:'#4A5868'});
  },
  stats: function(p, r){
    return [['거리 L (기본량)', f(r.L, 1) + ' m'], ['시간 t (기본량)', f(r.t, 1) + ' s'], ['질량 m (기본량)', f(r.m, 1) + ' kg'],
      ['속력 v', f(r.v, 2) + ' m/s', PAL[0]], ['같은 속력을 km/h로', f(r.kmh, 1) + ' km/h', PAL[0]],
      ['운동량 p = m v', f(r.mom, 2) + ' kg·m/s', PAL[1]], ['운동 에너지 E = ½ m v²', f(r.E, 2) + ' J', PAL[1]],
      ['무게 W = m g', f(r.W, 1) + ' N'], ['닿는 넓이 A', r.Acm + ' cm² = ' + f(r.A, 4) + ' m²'],
      ['압력 P = W ÷ A', Math.round(r.P).toLocaleString() + ' Pa', PAL[4]]];
  },
  columns: ['L (m)', 't (s)', 'm (kg)', 'v (m/s)', 'v (km/h)', 'p (kg·m/s)', 'E (J)', 'A (cm²)', 'P (Pa)'],
  record: function(p, r){ return {L:r.L, t:r.t, m:r.m, v:r.v, kmh:r.kmh, mom:r.mom, E:r.E, Acm:r.Acm, P:r.P}; },
  row: function(d){ return [f(d.L,1), f(d.t,1), f(d.m,1), f(d.v,2), f(d.kmh,1), f(d.mom,2), f(d.E,2), d.Acm, Math.round(d.P).toLocaleString()]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('같은 속력, 다른 단위', '<canvas class="chart" id="ch1" role="img" aria-label="m/s와 km/h 산점도 — 아래 글에서 기울기를 확인할 수 있어요"></canvas><ul class="readout" id="ro1"></ul><p class="ask">단위를 바꾸면 수는 달라지지만 속력 자체는 그대로입니다. 두 값의 비는 왜 항상 같을까요?</p>') +
      card('속력과 운동 에너지', '<canvas class="chart" id="ch2" role="img" aria-label="속력 제곱과 운동 에너지 산점도 — 아래 글에서 기울기를 확인할 수 있어요"></canvas><ul class="readout" id="ro2"></ul><p class="ask">속력이 2배가 되면 운동 에너지는 몇 배가 될까요? 운동량과 비교해 보세요.</p>') +
      card('유도량은 기본량의 조립', '<div id="ro3"></div><p class="ask">표의 마지막 칸처럼 단위를 기본량으로 풀어 쓰면, 그 양이 무엇을 곱하고 나눈 것인지 보입니다. 새로 배우는 물리량도 이렇게 확인해 보세요.</p>') + '</div>';
    drawScatter($('ch1'), {xLabel:'속력 (m/s)', yLabel:'속력 (km/h)', series:[{color:PAL[0], pts:rec.map(function(d){ return {x:d.v, y:d.kmh}; })}]});
    var r1 = [];
    if (distinct(rec.map(function(d){ return d.v; })) >= 2){
      var k1 = fit0(rec.map(function(d){ return {x:d.v, y:d.kmh}; }));
      r1.push('<li>원점을 지나는 직선의 기울기 <b>' + f(k1, 2) + '</b> — 1 km = 1000 m, 1 h = 3600 s이므로 3600 ÷ 1000 = <b>3.6</b>배예요.</li>');
    } else r1.push('<li>거리나 시간을 바꿔 서로 다른 속력을 2가지 이상 기록해 보세요.</li>');
    r1.push('<li>단위 환산은 값을 곱해 주는 일일 뿐, 속력이라는 <b>양 자체</b>는 변하지 않아요.</li>');
    $('ro1').innerHTML = r1.join('');
    var bm = groupBy(rec, function(d){ return d.m; }), s2 = [], r2 = [], ci = 0;
    Object.keys(bm).sort(function(a,b){ return a - b; }).forEach(function(k){
      var g = bm[k], col = PAL[ci++ % PAL.length];
      s2.push({color:col, pts:g.map(function(d){ return {x:d.v * d.v, y:d.E}; })});
      if (distinct(g.map(function(d){ return d.v; })) >= 2){
        var kk = fit0(g.map(function(d){ return {x:d.v * d.v, y:d.E}; }));
        r2.push('<li>' + dot(col) + '질량 ' + f(+k, 1) + ' kg: 기울기 <b>' + f(kk, 3) + '</b> ≈ m ÷ 2 = ' + f(+k / 2, 3) + '</li>');
      }
    });
    drawScatter($('ch2'), {xLabel:'속력의 제곱 v² (m²/s²)', yLabel:'운동 에너지 E (J)', series:s2});
    $('ro2').innerHTML = (r2.length ? r2.join('') : '<li>같은 질량에서 속력만 2가지 이상 바꿔 기록해 보세요.</li>') +
      '<li>E–v² 그래프가 직선이므로 E는 v의 <b>제곱</b>에 비례해요. 속력이 2배면 에너지는 4배, 운동량은 2배예요.</li>';
    var ex = rec[rec.length - 1];
    $('ro3').innerHTML = tableHTML(['물리량', '식', '단위', '기본량으로 풀면'], [
      ['속력', 'L ÷ t', 'm/s', 'm · s⁻¹'],
      ['운동량', 'm × v', 'kg·m/s', 'kg · m · s⁻¹'],
      ['운동 에너지', '½ × m × v²', 'J', 'kg · m² · s⁻²'],
      ['힘(무게)', 'm × g', 'N', 'kg · m · s⁻²'],
      ['압력', 'W ÷ A', 'Pa', 'kg · m⁻¹ · s⁻²']
    ], 'wrap') + '<p class="note">마지막 기록 확인: 무게 ' + f(ex.m * 9.8, 1) + ' N ÷ 넓이 ' + f(ex.Acm * 1e-4, 4) + ' m² = ' + Math.round(ex.P).toLocaleString() + ' Pa</p>';
  }
};`
},

/* ===================== 20. 반복 측정과 오차 (Basics Ep03) ===================== */
{
  file: '20_measure_error_standard_lab_IntegSci1_Basics_Ep03.html',
  title: '반복해서 재면 참값에 가까워질까',
  intro: '길이 152.4 mm인 연필을 여러 자로 반복해서 잽니다. 자의 최소 눈금과 반복 횟수, 그리고 자의 영점이 어긋난 정도를 바꿔 가며 평균이 참값에 얼마나 가까워지는지 확인해 보세요.',
  sceneNote: '잴 때마다 값이 조금씩 흔들리는 것이 우연 오차, 자가 애초에 어긋나 늘 같은 방향으로 밀리는 것이 계통 오차입니다. 측정값은 난수로 만들어 매번 달라집니다.',
  runLabel: '반복해서 재기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 우연 오차와 계통 오차</h3>
<p>측정에는 늘 오차가 있어요. 읽는 사람의 눈, 손 떨림처럼 <b>매번 방향이 바뀌는</b> 오차를 우연 오차라 하고, 자의 영점이 어긋났거나 저울이 틀어진 것처럼 <b>늘 같은 방향으로</b> 밀리는 오차를 계통 오차라고 해요. 우연 오차는 여러 번 재서 평균을 내면 서로 상쇄되어 줄어들지만, <b>계통 오차는 아무리 반복해도 줄지 않아요</b>. 그래서 표준(기준기)으로 기기를 맞추는 일(교정)이 필요해요.</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>평균 <span class="fx-formula">x̄ = (x₁+x₂+…+xₙ) ÷ n</span> — 우연 오차가 서로 상쇄되는 값이에요.</li>
<li>표준 편차 s — 측정값이 평균에서 흩어진 정도. 자의 최소 눈금이 작을수록 s가 작아요.</li>
<li>평균의 표준 오차 <span class="fx-formula">SE = s ÷ √n</span> — 4번 재면 절반, 100번 재면 1/10로 줄어요. 4배 정밀하게 하려면 16배 많이 재야 해요.</li>
<li>영점이 +2 mm 어긋난 자로 100번을 재도 평균은 참값보다 약 +2 mm 큰 채로 남아요.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p>측정값 = 참값 152.4 + 영점 어긋남 + (표준 편차 σ인 우연 오차), <span class="fx-formula">SE = s ÷ √n</span>, <span class="fx-formula">치우침 = x̄ − 참값</span></p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 우연 오차를 <b>정규 분포 난수</b>로 만들었어요. 실제 측정에는 눈금을 한쪽으로만 읽는 버릇, 온도에 따른 자의 늘어남처럼 정규 분포로 설명되지 않는 요인도 섞여요.<br>
· 참값을 알고 있다고 두었지만, 실제 실험에서는 참값을 모르기 때문에 표준기와 비교하거나 여러 방법으로 재서 서로 견줘요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>체중계를 올라서기 전에 0으로 맞추는 것, 저울을 정기적으로 검정하는 것이 계통 오차를 없애는 일이에요.</li>
<li>선거 여론 조사에서 표본이 많아질수록 오차 범위가 줄지만, 표본을 잘못 고르면(계통 오차) 아무리 많이 조사해도 빗나가요.</li>
</ul>`,
  js: `
var TRUE = 152.4;                       // 참값 (mm)
var TOOL = [{n:'눈금 1 cm 자', sd:2.5}, {n:'눈금 1 mm 자', sd:0.30}, {n:'버니어 캘리퍼스', sd:0.04}];
var NREP = [3, 5, 10, 30];
var BIAS = [0, 2, -3];
var lastVals = [];
function gauss(){ var u = 1 - Math.random(), v = Math.random(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
return {
  sceneHeight: 460,
  minRec: 4,
  idle: '자와 반복 횟수, 영점 어긋남을 정하고 <b>반복해서 재기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 반복 횟수와 영점 어긋남을 바꿔 가며 기록하세요.',
  params: [
    {key:'k', type:'seg', label:'재는 도구', cols:3, value:1, options:TOOL.map(function(x){ return x.n + '<small>흩어짐 σ ≈ ' + f(x.sd, 2) + ' mm</small>'; })},
    {key:'n', type:'seg', label:'반복 횟수 n', cols:4, value:1, options:NREP.map(function(v){ return v + '번'; })},
    {key:'b', type:'seg', label:'자의 영점 어긋남', cols:3, value:0, options:['맞음 0 mm', '+2 mm 밀림', '−3 mm 밀림'],
      note:'참값은 152.4 mm입니다. 영점이 어긋난 자는 모든 측정값을 같은 방향으로 밀어 놓습니다.'}
  ],
  compute: function(p){
    var T = TOOL[p.k], n = NREP[p.n], b = BIAS[p.b], vals = [];
    for (var i = 0; i < n; i++) vals.push(TRUE + b + gauss() * T.sd);
    var mu = mean(vals), sum = 0;
    vals.forEach(function(v){ sum += (v - mu) * (v - mu); });
    var sd = n > 1 ? Math.sqrt(sum / (n - 1)) : 0;
    lastVals = vals;
    return {T:T, n:n, b:b, vals:vals, mu:mu, sd:sd, se:sd / Math.sqrt(n),
      lo:Math.min.apply(null, vals), hi:Math.max.apply(null, vals), dev:mu - TRUE};
  },
  draw: function(c, W, H, p, r, tau){
    var T = TOOL[p.k], padL = 70, padR = 30, y0 = 210;
    var half = Math.max(3 * T.sd + Math.abs(BIAS[p.b]) + 1, 4);
    var lo = TRUE - half, hi = TRUE + half;
    var X = function(v){ return padL + (v - lo) / (hi - lo) * (W - padL - padR); };
    // 눈금 자
    c.fillStyle = '#F2F5F9'; c.fillRect(padL, y0 - 26, W - padL - padR, 52);
    c.strokeStyle = '#8C99A8'; c.lineWidth = 1.5; c.strokeRect(padL, y0 - 26, W - padL - padR, 52);
    var stp = half > 6 ? 2 : 1;
    for (var v = Math.ceil(lo / stp) * stp; v <= hi; v += stp){
      seg(c, X(v), y0 - 26, X(v), y0 - 8, '#8C99A8', 1);
      txt(c, f(v, 0), X(v), y0 + 4, {align:'center', color:'#4A5868'});
    }
    seg(c, X(TRUE), y0 - 60, X(TRUE), y0 + 26, '#C8463D', 2.5, [6, 4]);
    txt(c, '참값 ' + f(TRUE, 1) + ' mm', X(TRUE), y0 - 66, {align:'center', color:'#C8463D', bold:true});
    if (!r){ txt(c, '자를 고르고 반복 횟수를 정한 뒤 재어 보세요.', 16, H - 20, {color:'#4A5868'}); return; }
    var show = Math.max(1, Math.round(r.vals.length * tau));
    for (var i = 0; i < show; i++){
      var yy = y0 + 56 + (i % 10) * 15, xx = X(r.vals[i]);
      c.fillStyle = 'rgba(43,95,163,.72)'; c.beginPath(); c.arc(xx, yy, 5, 0, Math.PI * 2); c.fill();
    }
    var partial = r.vals.slice(0, show), mu = mean(partial);
    seg(c, X(mu), y0 - 60, X(mu), y0 + 26, '#2E9E78', 2.5);
    txt(c, '평균 ' + f(mu, 2), X(mu), y0 - 90, {align:'center', color:'#2E9E78', bold:true});
    txt(c, show + ' / ' + r.vals.length + ' 번째 측정', W - 16, 34, {align:'right', color:'#4A5868'});
    if (tau < 1) return;
    txt(c, '평균 ' + f(r.mu, 2) + ' mm · 표준 편차 s = ' + f(r.sd, 2) + ' mm · 표준 오차 s÷√n = ' + f(r.se, 3) + ' mm', 16, H - 44, {bold:true});
    txt(c, '참값과의 차이 ' + sgn(r.dev, 2) + ' mm (영점 어긋남 ' + sgn(r.b, 0) + ' mm)', 16, H - 16,
      {color:Math.abs(r.dev) > 1 ? '#C8463D' : '#2E9E78', bold:true});
  },
  stats: function(p, r){
    return [['재는 도구', r.T.n], ['반복 횟수 n', r.n + '번'], ['영점 어긋남', sgn(r.b, 0) + ' mm'],
      ['가장 작은 값', f(r.lo, 2) + ' mm'], ['가장 큰 값', f(r.hi, 2) + ' mm'],
      ['평균 x̄', f(r.mu, 2) + ' mm', PAL[1]], ['표준 편차 s', f(r.sd, 2) + ' mm', PAL[0]],
      ['평균의 표준 오차 s÷√n', f(r.se, 3) + ' mm', PAL[0]],
      ['참값(152.4)과의 차이', sgn(r.dev, 2) + ' mm', PAL[4]]];
  },
  columns: ['도구', 'n', '영점 (mm)', '평균 (mm)', 's (mm)', 's÷√n (mm)', '참값과의 차이 (mm)'],
  record: function(p, r){ return {k:p.k, tool:r.T.n, tsd:r.T.sd, n:r.n, b:r.b, mu:r.mu, sd:r.sd, se:r.se, dev:r.dev}; },
  row: function(d){ return [d.tool, d.n, sgn(d.b, 0), f(d.mu, 2), f(d.sd, 2), f(d.se, 3), sgn(d.dev, 2)]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('많이 잴수록 줄어드는 것', '<canvas class="chart" id="ch1" role="img" aria-label="1÷√n과 표준 오차 산점도 — 아래 글에서 관계를 확인할 수 있어요"></canvas><ul class="readout" id="ro1"></ul><p class="ask">표준 오차를 절반으로 줄이려면 몇 번을 재야 할까요? 반복 횟수를 100배로 늘리면 몇 배 정밀해질까요?</p>') +
      card('반복해도 줄지 않는 것', '<canvas class="chart" id="ch2" role="img" aria-label="영점 어긋남과 평균의 치우침 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">영점이 어긋난 자로 1000번을 재면 평균은 참값에 가까워질까요? 이런 오차는 어떻게 없앨 수 있을까요?</p>') +
      card('도구가 정하는 흩어짐', '<div id="ro3"></div><p class="ask">같은 횟수를 재도 도구에 따라 표준 편차가 다릅니다. 더 정밀한 도구와 더 많은 반복 중 무엇이 먼저 필요할지 생각해 보세요.</p>') + '</div>';
    var bt = groupBy(rec, function(d){ return d.k; }), s1 = [], r1 = [];
    Object.keys(bt).forEach(function(k){
      var g = bt[k], col = PAL[+k];
      s1.push({color:col, pts:g.map(function(d){ return {x:1 / Math.sqrt(d.n), y:d.se}; })});
      if (distinct(g.map(function(d){ return d.n; })) >= 2){
        var kk = fit0(g.map(function(d){ return {x:1 / Math.sqrt(d.n), y:d.se}; }));
        r1.push('<li>' + dot(col) + g[0].tool + ': 기울기 <b>' + f(kk, 2) + ' mm</b> — 도구의 흩어짐 σ ≈ ' + f(g[0].tsd, 2) + ' mm와 비슷해요.</li>');
      }
    });
    drawScatter($('ch1'), {xLabel:'1 ÷ √n', yLabel:'평균의 표준 오차 (mm)', series:s1});
    $('ro1').innerHTML = (r1.length ? r1.join('') : '<li>같은 도구로 반복 횟수를 2가지 이상 바꿔 기록해 보세요.</li>') +
      '<li>점들이 원점을 지나는 직선 위에 놓여요. 표준 오차는 <b>1 ÷ √n</b>에 비례하므로, 절반으로 줄이려면 <b>4배</b> 많이 재야 해요.</li>';
    drawScatter($('ch2'), {xLabel:'자의 영점 어긋남 (mm)', yLabel:'평균 − 참값 (mm)', square:true,
      series:[{color:PAL[4], pts:rec.map(function(d){ return {x:d.b, y:d.dev}; })}], lines:[{k:1, b:0, color:'#8C99A8', dash:[6,4]}]});
    var bb = groupBy(rec, function(d){ return d.b; }), r2 = [];
    Object.keys(bb).sort(function(a,b){ return a - b; }).forEach(function(k){
      var g = bb[k], mv = mean(g.map(function(d){ return d.dev; }));
      r2.push('<li>영점 ' + sgn(+k, 0) + ' mm인 기록 ' + g.length + '개의 평균 치우침 <b>' + sgn(mv, 2) + ' mm</b></li>');
    });
    $('ro2').innerHTML = r2.join('') + '<li>점들이 기울기 1인 회색 선 가까이 놓여요. 평균의 치우침은 <b>영점 어긋남과 거의 같아</b> 반복해도 사라지지 않아요.</li>';
    var rows = [];
    Object.keys(bt).forEach(function(k){
      var g = bt[k];
      rows.push([g[0].tool, f(g[0].tsd, 2) + ' mm', g.length + '개', f(mean(g.map(function(d){ return d.sd; })), 2) + ' mm', f(mean(g.map(function(d){ return d.se; })), 3) + ' mm']);
    });
    $('ro3').innerHTML = tableHTML(['도구', '도구의 σ', '기록 수', '평균 표준 편차 s', '평균 표준 오차'], rows) +
      '<p class="note">계통 오차가 큰 상황에서는 반복 횟수를 늘려도 정확해지지 않아요. 먼저 영점을 맞춰야 해요.</p>';
  }
};`
},

/* ===================== 21. 아날로그를 0과 1로 (Basics Ep04) ===================== */
{
  file: '21_analog_to_digital_lab_IntegSci1_Basics_Ep04.html',
  title: '아날로그를 0과 1로 바꾸기',
  intro: '센서가 받은 매끄러운 파형을 정해진 간격으로 찍고(표본화) 정해진 계단으로 반올림해(양자화) 숫자로 바꿉니다. 표본화 주파수와 비트 수를 바꿔 가며 원래 신호와 얼마나 달라지는지 재어 보세요.',
  sceneNote: '회색 곡선이 원래 아날로그 신호, 파란 점이 표본, 주황 계단이 숫자로 저장한 뒤 되살린 신호입니다. 오차는 1초 구간을 촘촘히 비교해 계산합니다.',
  runLabel: '디지털로 바꾸기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 표본화와 양자화</h3>
<p>센서가 만든 전압은 시간에 따라 끊김 없이 변하는 <b>아날로그</b> 신호예요. 이것을 컴퓨터가 다루려면 <b>표본화</b>(일정한 시간 간격으로 값을 찍기)와 <b>양자화</b>(그 값을 정해진 단계 중 가장 가까운 것으로 반올림)를 거쳐 0과 1의 수로 바꿔야 해요. 신호 주파수의 <b>2배보다 높은 표본화 주파수</b>가 필요하다는 것이 나이퀴스트 조건이고, 이를 어기면 원래 없던 낮은 주파수가 나타나는 <b>에일리어싱</b>이 생겨요.</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>나이퀴스트 조건 <span class="fx-formula">f<sub>s</sub> &gt; 2f</span> — 20 Hz 신호는 40 Hz보다 촘촘히 찍어야 해요. 사람 귀의 20 kHz 때문에 CD는 44.1 kHz를 써요.</li>
<li>양자화 단계 수 = 2<sup>b</sup>. 8비트는 256단계, 12비트는 4096단계예요.</li>
<li>신호 대 잡음비 <span class="fx-formula">SNR ≈ 6.02 b + 1.76 (dB)</span> — 비트가 1개 늘면 잡음이 약 <b>절반</b>이 돼요.</li>
<li>데이터율 = f<sub>s</sub> × b (bit/s). 촘촘하고 정밀할수록 용량이 커져 저장과 전송에 비용이 들어요.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p>표본값 = sin(2π f t<sub>k</sub>) → 가장 가까운 계단으로 반올림 → 다음 표본까지 그 값 유지, <span class="fx-formula">오차 RMS = √(평균((원래 − 되살린)²))</span>, <span class="fx-formula">겉보기 주파수 = |f − f<sub>s</sub>×round(f ÷ f<sub>s</sub>)|</span></p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 되살릴 때 표본값을 그대로 유지하는 <b>계단 방식</b>을 썼어요. 실제 기기는 저역 통과 필터로 매끄럽게 이어 붙여 오차가 더 작아요.<br>
· 표본화 전에 높은 주파수를 걸러 내는 필터를 두지 않았어요. 실제 장치는 이 필터로 에일리어싱을 미리 막아요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>디지털 신호는 복사해도 계단 값이 그대로라 100번을 복사해도 나빠지지 않지만, 아날로그 테이프는 복사할수록 잡음이 쌓여요.</li>
<li>바퀴가 뒤로 도는 것처럼 보이는 영상이 에일리어싱이에요. 초당 프레임 수가 바퀴의 회전보다 느려서 생겨요.</li>
</ul>`,
  js: `
var FS = [8, 16, 40, 100];
var BIT = [2, 4, 8, 12];
var NDENSE = 1200;
function quant(x, b){
  var lv = Math.pow(2, b), d = 2 / lv;
  var q = Math.floor((x + 1) / d) * d + d / 2 - 1;
  return Math.max(-1 + d / 2, Math.min(1 - d / 2, q));
}
return {
  sceneHeight: 460,
  minRec: 4,
  idle: '신호 주파수와 표본화 주파수, 비트 수를 정하고 <b>디지털로 바꾸기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 표본화 주파수와 비트 수를 바꿔 가며 기록하세요.',
  params: [
    {key:'fr', type:'range', label:'신호 주파수 f', min:1, max:20, step:1, value:5, fmt:function(v){ return v + ' Hz'; }},
    {key:'s', type:'seg', label:'표본화 주파수 fₛ', cols:4, value:2, options:FS.map(function(v){ return v + ' Hz'; })},
    {key:'b', type:'seg', label:'양자화 비트 수', cols:4, value:1, options:BIT.map(function(v){ return v + ' bit<small>' + Math.pow(2, v) + '단계</small>'; }),
      note:'표본화는 시간을 쪼개는 일, 양자화는 크기를 쪼개는 일입니다. 둘 다 부족하면 되살린 신호가 원래와 달라집니다.'}
  ],
  compute: function(p){
    var fr = p.fr, fs = FS[p.s], b = BIT[p.b];
    var ns = Math.round(fs), samp = [], i;
    for (i = 0; i < ns; i++){ var t = i / fs; samp.push({t:t, x:Math.sin(2 * Math.PI * fr * t), q:quant(Math.sin(2 * Math.PI * fr * t), b)}); }
    var e2 = 0, eq2 = 0;
    for (i = 0; i < NDENSE; i++){
      var tt = i / NDENSE, x = Math.sin(2 * Math.PI * fr * tt);
      var idx = Math.min(ns - 1, Math.floor(tt * fs));
      var rec2 = samp[idx].q, d1 = x - rec2, d2 = x - quant(x, b);
      e2 += d1 * d1; eq2 += d2 * d2;
    }
    var rms = Math.sqrt(e2 / NDENSE), rmsq = Math.sqrt(eq2 / NDENSE);
    var alias = Math.abs(fr - fs * Math.round(fr / fs));
    return {fr:fr, fs:fs, b:b, samp:samp, lv:Math.pow(2, b), step:2 / Math.pow(2, b),
      rms:rms, rmsq:rmsq, snrq:20 * Math.log10(Math.SQRT1_2 / rmsq), snrTh:6.02 * b + 1.76,
      alias:alias, ok:fs > 2 * fr, rate:fs * b, kb:fs * b * 60 / 8 / 1000};
  },
  draw: function(c, W, H, p, r, tau){
    var padL = 56, padR = 24, top = 60, hgt = 200, mid = top + hgt / 2;
    var X = function(t){ return padL + t * (W - padL - padR); };
    var Y = function(v){ return mid - v * hgt / 2; };
    seg(c, padL, mid, W - padR, mid, '#C3CDD9', 1.5);
    seg(c, padL, top, padL, top + hgt, '#8C99A8', 1.5);
    txt(c, '+1', padL - 8, top + 6, {align:'right', color:'#4A5868'});
    txt(c, '−1', padL - 8, top + hgt + 6, {align:'right', color:'#4A5868'});
    txt(c, '0', padL - 8, mid + 6, {align:'right', color:'#4A5868'});
    txt(c, '시간 (1초 구간)', (W + padL) / 2, top + hgt + 34, {align:'center', color:'#4A5868'});
    // 양자화 계단
    if (r){
      var d = r.step;
      for (var v = -1 + d / 2; v < 1; v += d){
        if (r.lv > 64) break;
        seg(c, padL, Y(v), W - padR, Y(v), '#EDF1F6', 1);
      }
    }
    // 원 신호
    c.strokeStyle = '#8C99A8'; c.lineWidth = 2; c.beginPath();
    for (var i = 0; i <= 600; i++){ var t = i / 600, x = X(t), y = Y(Math.sin(2 * Math.PI * p.fr * t)); if (i) c.lineTo(x, y); else c.moveTo(x, y); }
    c.stroke();
    if (!r){ txt(c, '회색 곡선이 센서가 받은 아날로그 신호예요.', 16, H - 20, {color:'#4A5868'}); return; }
    var show = Math.max(1, Math.round(r.samp.length * tau));
    // 계단 재구성
    c.strokeStyle = '#D98E04'; c.lineWidth = 2.5; c.beginPath();
    for (var k = 0; k < show; k++){
      var t0 = r.samp[k].t, t1 = Math.min(1, (k + 1) / r.fs), yq = Y(r.samp[k].q);
      if (!k) c.moveTo(X(t0), yq); else c.lineTo(X(t0), yq);
      c.lineTo(X(t1), yq);
    }
    c.stroke();
    for (var j = 0; j < show; j++){
      c.fillStyle = '#2B5FA3'; c.beginPath(); c.arc(X(r.samp[j].t), Y(r.samp[j].x), 3.5, 0, Math.PI * 2); c.fill();
    }
    txt(c, '표본 ' + show + ' / ' + r.samp.length + '개', W - 16, 34, {align:'right', color:'#4A5868'});
    if (tau < 1) return;
    txt(c, '되살린 신호의 오차 RMS ' + f(r.rms, 3) + ' (신호 크기 0.707 기준 ' + f(r.rms / Math.SQRT1_2 * 100, 1) + ' %)', 16, top + hgt + 76, {bold:true});
    txt(c, r.ok ? '표본화 조건 만족: fₛ = ' + r.fs + ' Hz > 2f = ' + (2 * r.fr) + ' Hz'
      : '에일리어싱! fₛ = ' + r.fs + ' Hz ≤ 2f = ' + (2 * r.fr) + ' Hz → 겉보기 주파수 ' + f(r.alias, 1) + ' Hz로 보여요',
      16, top + hgt + 108, {bold:true, color:r.ok ? '#2E9E78' : '#C8463D'});
    txt(c, '데이터율 ' + r.rate + ' bit/s · 1분 저장 ' + f(r.kb, 1) + ' KB', 16, H - 16, {color:'#4A5868'});
  },
  stats: function(p, r){
    return [['신호 주파수 f', r.fr + ' Hz'], ['표본화 주파수 fₛ', r.fs + ' Hz'], ['1초당 표본 수', r.samp.length + '개'],
      ['양자화 비트', r.b + ' bit (' + r.lv + '단계)'], ['계단 한 칸 크기', f(r.step, 4), PAL[6]],
      ['양자화만의 오차 RMS', f(r.rmsq, 4), PAL[6]], ['양자화 SNR (측정)', f(r.snrq, 1) + ' dB', PAL[1]],
      ['양자화 SNR (이론 6.02b+1.76)', f(r.snrTh, 1) + ' dB'],
      ['되살린 신호의 전체 오차 RMS', f(r.rms, 3), PAL[4]],
      ['표본화 조건', r.ok ? '만족 (fₛ > 2f)' : '위반 → 에일리어싱', r.ok ? PAL[1] : PAL[4]],
      ['겉보기 주파수', f(r.alias, 1) + ' Hz'], ['데이터율', r.rate + ' bit/s (1분 ' + f(r.kb, 1) + ' KB)']];
  },
  columns: ['f (Hz)', 'fₛ (Hz)', 'bit', 'fₛ ÷ f', '겉보기 f (Hz)', '양자화 SNR (dB)', '전체 오차 RMS', 'bit/s'],
  record: function(p, r){ return {fr:r.fr, fs:r.fs, b:r.b, ratio:r.fs / r.fr, alias:r.alias, snrq:r.snrq, snrTh:r.snrTh, rms:r.rms, rate:r.rate, kb:r.kb, ok:r.ok}; },
  row: function(d){ return [d.fr, d.fs, d.b, f(d.ratio, 1), f(d.alias, 1), f(d.snrq, 1), f(d.rms, 3), d.rate]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('비트 수와 양자화 잡음', '<canvas class="chart" id="ch1" role="img" aria-label="비트 수와 신호 대 잡음비 산점도"></canvas><ul class="readout" id="ro1"></ul><p class="ask">비트를 1개 늘리면 계단 수는 2배가 됩니다. 잡음은 몇 분의 1이 될까요?</p>') +
      card('표본화 주파수와 겉보기 주파수', '<canvas class="chart" id="ch2" role="img" aria-label="표본화 주파수 비와 겉보기 주파수 비 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">fₛ ÷ f가 2보다 작은 기록에서 무슨 일이 일어났나요? 영상 속 바퀴가 거꾸로 도는 현상과 어떻게 연결될까요?</p>') +
      card('정밀함의 값: 데이터 크기', '<div id="ro3"></div><p class="ask">품질을 높이면 용량이 늘어납니다. 음성 통화와 음악 감상에 같은 설정을 써야 할까요?</p>') + '</div>';
    var pts1 = rec.map(function(d){ return {x:d.b, y:d.snrq}; });
    drawScatter($('ch1'), {xLabel:'양자화 비트 수 b', yLabel:'양자화 SNR (dB)', tightX:true, tightY:true,
      series:[{color:PAL[1], pts:pts1}]});
    var r1 = [];
    if (distinct(rec.map(function(d){ return d.b; })) >= 2){
      var L = linfit(pts1);
      r1.push('<li>직선의 기울기 <b>' + f(L.k, 2) + ' dB/bit</b> — 이론값 6.02 dB/bit와 비교해 보세요.</li>');
      r1.push('<li>6 dB는 잡음 크기가 <b>절반</b>이 된다는 뜻이에요. 비트 1개가 정밀도를 2배로 올려요.</li>');
    } else r1.push('<li>비트 수를 2가지 이상 바꿔 기록해 보세요.</li>');
    $('ro1').innerHTML = r1.join('');
    var good = rec.filter(function(d){ return d.ok; }), bad = rec.filter(function(d){ return !d.ok; });
    drawScatter($('ch2'), {xLabel:'fₛ ÷ f', yLabel:'겉보기 주파수 ÷ f',
      series:[{color:PAL[1], pts:good.map(function(d){ return {x:d.ratio, y:d.alias / d.fr}; })},
              {color:PAL[4], pts:bad.map(function(d){ return {x:d.ratio, y:d.alias / d.fr}; })}],
      lines:[{h:1, color:'#8C99A8', dash:[6,4]}]});
    $('ro2').innerHTML = '<li>' + dot(PAL[1]) + 'fₛ > 2f인 기록 <b>' + good.length + '개</b> — 겉보기 주파수가 원래 주파수와 같아 회색 선(비 = 1) 위에 놓여요.</li>' +
      '<li>' + dot(PAL[4]) + 'fₛ ≤ 2f인 기록 <b>' + bad.length + '개</b> — 회색 선에서 벗어났어요. 원래 없던 낮은 주파수로 보이는 <b>에일리어싱</b>이에요.</li>' +
      (bad.length ? '<li>예: f = ' + bad[0].fr + ' Hz를 ' + bad[0].fs + ' Hz로 찍으면 ' + f(bad[0].alias, 1) + ' Hz처럼 보여요.</li>'
                  : '<li>표본화 주파수를 낮춰(8 Hz) 높은 주파수를 찍으면 에일리어싱을 볼 수 있어요.</li>');
    var seen = {}, rows = [];
    rec.forEach(function(d){ var k = d.fs + '/' + d.b; if (seen[k]) return; seen[k] = 1;
      rows.push([d.fs + ' Hz', d.b + ' bit', d.rate + ' bit/s', f(d.kb, 1) + ' KB', f(d.snrTh, 1) + ' dB']); });
    rows.sort(function(a, b){ return parseFloat(a[2]) - parseFloat(b[2]); });
    $('ro3').innerHTML = tableHTML(['표본화 주파수', '비트 수', '데이터율', '1분 용량', '이론 SNR'], rows) +
      '<p class="note">1 KB = 1,000 B로 계산했어요. 참고로 CD 음질은 44.1 kHz · 16 bit · 2채널이라 1분에 약 10 MB예요.</p>';
  }
};`
}

  ]
};
