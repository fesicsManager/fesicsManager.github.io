// 고1 통합과학2 — Ⅱ. 환경과 에너지 (1·4·5·7화), Ⅲ. 과학과 미래 사회 (3·4화) 실험 정의
module.exports = {
  folder: 'high1Integ',
  suffix: '고1 통합과학',
  principle: '과학 원리',
  anim: 1800,
  labs: [

/* ===================== 34. 표면적과 부피의 비 (EnvEnergy Ep01) ===================== */
{
  file: '34_surface_volume_heat_lab_IntegSci2_EnvEnergy_Ep01.html',
  title: '사막여우의 큰 귀',
  intro: '몸의 크기와 귀의 크기, 바깥 기온을 바꿔 가며 몸에서 빠져나가는 열을 잽니다. 같은 모양이라도 크기가 달라지면 표면적과 부피의 비가 달라진다는 것을 확인해 보세요.',
  sceneNote: '몸을 공 모양으로 단순화한 교육용 모형입니다. 체온은 38 °C로 두고, 열은 표면적에 비례해 빠져나간다고 계산합니다.',
  runLabel: '열 손실 재기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 표면적 대 부피의 비</h3>
<p>열은 <b>표면</b>을 통해 빠져나가고, 열을 만드는 일은 <b>부피(몸집)</b> 전체에서 일어나요. 그런데 크기가 커질 때 표면적은 길이의 제곱, 부피는 세제곱으로 늘어요. 그래서 <b>몸이 커질수록 부피에 비해 표면이 작아져</b> 열을 덜 잃어요. 구라면 <span class="fx-formula">S ÷ V = 3 ÷ r</span>로, 반지름이 2배면 이 비는 절반이 돼요. 추운 곳의 동물이 몸집이 크고 귀가 작은 것, 더운 곳의 동물이 귀와 다리가 큰 것이 같은 원리예요(알렌·베르그만 규칙).</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>공의 표면적 <span class="fx-formula">S = 4πr²</span>, 부피 <span class="fx-formula">V = (4÷3)πr³</span> → <span class="fx-formula">S ÷ V = 3 ÷ r</span>.</li>
<li>열 손실 <span class="fx-formula">Q = h × A × (체온 − 기온)</span>. 귀는 표면적을 늘려 A를 키워요.</li>
<li>기온이 체온보다 <b>높으면</b> 부호가 뒤집혀 열이 들어와요. 사막여우가 낮에는 굴에 숨는 까닭이에요.</li>
<li>같은 몸집이라도 귀가 몸 표면의 35 %만큼 되면, 방열 면적이 35 % 늘어 그만큼 더 식힐 수 있어요.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p><span class="fx-formula">A = 4πr² × (1 + 귀 비율)</span>, <span class="fx-formula">Q = 8 × A × (38 − 기온)</span> W, <span class="fx-formula">단위 질량당 = Q ÷ (부피 × 1000 kg/m³)</span></p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 몸을 <b>공</b>으로 보고 열전달 계수를 8 W/(m²·K)로 고정했어요. 실제 동물은 털·지방층·혈류 조절로 열전달을 스스로 바꾸고, 바람이 불면 훨씬 빨리 식어요.<br>
· 땀·호흡으로 물이 증발하며 잃는 열은 넣지 않았어요. 더운 곳에서는 이 몫이 커요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>사막여우는 몸이 작고 귀가 크며, 북극여우는 몸이 크고 귀가 작아요. 같은 여우 무리인데 사는 곳에 따라 모양이 달라요. 다만 이런 경향(알렌·베르그만 규칙)은 <b>모든 생물에 그대로 들어맞는 법칙이 아니라</b> 털·혈류·행동·계통까지 함께 작용한 결과예요.</li>
<li>아기가 어른보다 체온을 빨리 잃는 것, 감자를 잘게 썰면 빨리 익는 것도 같은 비(S ÷ V)로 설명돼요.</li>
</ul>`,
  js: `
var EAR = [{n:'작은 귀', k:0.05}, {n:'보통 귀', k:0.15}, {n:'큰 귀', k:0.35}];
var AIR = [-10, 5, 25, 40];
var TB = 38, HC = 8;
return {
  sceneHeight: 460,
  minRec: 4,
  idle: '몸 크기와 귀 크기, 기온을 정하고 <b>열 손실 재기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 몸 크기와 귀 크기를 바꿔 가며 기록하세요.',
  params: [
    {key:'r', type:'range', label:'몸의 반지름', min:5, max:30, step:2.5, value:12.5, fmt:function(v){ return f(v, 1) + ' cm'; }},
    {key:'e', type:'seg', label:'귀의 크기', cols:3, value:1, options:EAR.map(function(x){ return x.n + '<small>몸 표면의 ' + Math.round(x.k * 100) + ' %</small>'; })},
    {key:'a', type:'seg', label:'바깥 기온', cols:4, value:1, options:AIR.map(function(v){ return sgn(v, 0) + ' °C'; }),
      note:'체온은 38 °C입니다. 기온이 체온보다 높으면 열이 오히려 몸으로 들어옵니다.'}
  ],
  compute: function(p){
    var r = p.r / 100, E = EAR[p.e], Ta = AIR[p.a];
    var S = 4 * Math.PI * r * r, V = 4 / 3 * Math.PI * r * r * r;
    var A = S * (1 + E.k), m = V * 1000;
    var Q = HC * A * (TB - Ta);
    return {rcm:p.r, r:r, E:E, Ta:Ta, S:S, V:V, sv:S / V, A:A, m:m, Q:Q, per:Q / m,
      earArea:S * E.k, gain:Q < 0};
  },
  draw: function(c, W, H, p, r, tau){
    var cx = Math.min(240, W * 0.3), cy = 200, scale = 3.6;
    var R = p.r * scale, E = EAR[p.e];
    // 배경 온도
    var Ta = AIR[p.a];
    c.fillStyle = Ta <= 0 ? '#E6F0F7' : Ta <= 10 ? '#EDF3F8' : Ta <= 25 ? '#F5F7F2' : '#FBF0E4';
    c.fillRect(0, 60, W, H - 60);
    txt(c, '바깥 기온 ' + sgn(Ta, 0) + ' °C', W - 16, 84, {align:'right', color:'#4A5868', bold:true});
    // 귀
    var ew = R * (0.5 + E.k * 1.6), eh = R * (0.7 + E.k * 2.2);
    c.fillStyle = '#C9A882'; c.strokeStyle = '#8A6A44'; c.lineWidth = 2;
    [-1, 1].forEach(function(s){
      c.beginPath();
      c.ellipse(cx + s * R * 0.62, cy - R * 0.85, ew * 0.42, eh * 0.55, s * 0.35, 0, Math.PI * 2);
      c.fill(); c.stroke();
    });
    // 몸
    c.fillStyle = '#D8B78F'; c.beginPath(); c.arc(cx, cy, R, 0, Math.PI * 2); c.fill();
    c.strokeStyle = '#8A6A44'; c.lineWidth = 2.5; c.stroke();
    c.fillStyle = '#2E3945';
    c.beginPath(); c.arc(cx - R * 0.3, cy - R * 0.15, 4, 0, Math.PI * 2); c.fill();
    c.beginPath(); c.arc(cx + R * 0.3, cy - R * 0.15, 4, 0, Math.PI * 2); c.fill();
    // 열 화살표
    if (r){
      var n = Math.min(16, Math.max(2, Math.round(Math.abs(r.Q) / 6)));
      for (var i = 0; i < n; i++){
        var ang = -Math.PI / 2 + i * 2 * Math.PI / n + tau * 0.6;
        var x1 = cx + Math.cos(ang) * (R + 6), y1 = cy + Math.sin(ang) * (R + 6);
        var len = 16 + 16 * ((tau + i / n) % 1);
        var x2 = cx + Math.cos(ang) * (R + 6 + len), y2 = cy + Math.sin(ang) * (R + 6 + len);
        if (r.gain) arrow(c, x2, y2, x1, y1, '#C8463D', 2);
        else arrow(c, x1, y1, x2, y2, '#D98E04', 2);
      }
    }
    txt(c, '반지름 ' + f(p.r, 1) + ' cm · ' + E.n, cx, cy + R + 70, {align:'center', color:'#4A5868'});
    if (!r){ txt(c, '몸에서 빠져나가는 열의 양을 재어 봐요.', 20, H - 18, {color:'#4A5868'}); return; }
    var lx = Math.max(cx + R + 60, W * 0.56);
    if (lx < W - 200){
      txt(c, r.gain ? '들어오는 열' : '나가는 열', lx, 130, {color:'#4A5868'});
      meter(c, lx, 140, Math.min(190, W - lx - 12), f(Math.abs(r.Q), 1) + ' W');
      txt(c, '표면적 ÷ 부피', lx, 208, {color:'#4A5868'});
      meter(c, lx, 218, Math.min(190, W - lx - 12), f(r.sv, 1) + ' /m');
    }
    if (tau < 1) return;
    var yy = H - 100;
    txt(c, '표면적 ' + f(r.S * 10000, 0) + ' cm² · 부피 ' + f(r.V * 1e6, 0) + ' cm³ · S ÷ V = ' + f(r.sv, 1) + ' /m', 20, yy, {bold:true, color:'#2B5FA3'});
    txt(c, '귀가 더해 준 방열 면적 ' + f(r.earArea * 10000, 0) + ' cm² (몸 표면의 ' + Math.round(r.E.k * 100) + ' %)', 20, yy + 30, {});
    txt(c, r.gain ? '기온이 체온보다 높아 열이 몸으로 들어와요 — 이때는 큰 귀가 불리해요.'
      : '몸무게 1 kg당 ' + f(r.per, 2) + ' W를 잃어요. 작을수록 이 값이 커요.',
      20, H - 14, {bold:true, color:r.gain ? '#C8463D' : '#2E9E78'});
  },
  stats: function(p, r){
    return [['몸의 반지름', f(r.rcm, 1) + ' cm'], ['귀의 크기', r.E.n], ['바깥 기온', sgn(r.Ta, 0) + ' °C'],
      ['표면적 S', f(r.S * 10000, 0) + ' cm²'], ['부피 V', f(r.V * 1e6, 0) + ' cm³'],
      ['S ÷ V', f(r.sv, 1) + ' /m', PAL[0]], ['몸무게(어림)', f(r.m, 2) + ' kg'],
      ['귀를 더한 방열 면적', f(r.A * 10000, 0) + ' cm²'],
      [r.gain ? '들어오는 열' : '나가는 열', f(Math.abs(r.Q), 1) + ' W', PAL[4]],
      ['몸무게 1 kg당', f(Math.abs(r.per), 2) + ' W/kg', PAL[1]]];
  },
  columns: ['반지름 (cm)', '귀', '기온 (°C)', 'S (cm²)', 'V (cm³)', 'S÷V (/m)', '열 (W)', 'W/kg'],
  record: function(p, r){
    return {rcm:r.rcm, ear:r.E.n, ek:r.E.k, Ta:r.Ta, S:r.S, V:r.V, sv:r.sv, Q:r.Q, per:r.per, m:r.m};
  },
  row: function(d){ return [f(d.rcm, 1), d.ear, sgn(d.Ta, 0), f(d.S * 10000, 0), f(d.V * 1e6, 0), f(d.sv, 1), sgn(d.Q, 1), sgn(d.per, 2)]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('크기와 S ÷ V', '<canvas class="chart" id="ch1" role="img" aria-label="반지름의 역수와 표면적 대 부피 비 산점도"></canvas><ul class="readout" id="ro1"></ul><p class="ask">가로축은 반지름의 역수입니다. 기울기 3이 나오는 까닭을 식으로 설명해 보세요.</p>') +
      card('귀가 하는 일', '<canvas class="chart" id="ch2" role="img" aria-label="기온과 열 손실 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">기온이 체온보다 높아지면 선이 가로축 아래로 내려갑니다. 그때 큰 귀는 도움이 될까요?</p>') +
      card('추운 곳과 더운 곳의 동물', '<div id="ro3"></div><p class="ask">북극여우와 사막여우의 생김새를 이 표로 설명해 보세요. 같은 종 안에서도 사는 곳에 따라 달라지는 까닭은 무엇일까요?</p>') + '</div>';
    var pts1 = rec.map(function(d){ return {x:1 / (d.rcm / 100), y:d.sv}; });
    drawScatter($('ch1'), {xLabel:'1 ÷ 반지름 (1/m)', yLabel:'표면적 ÷ 부피 (1/m)', series:[{color:PAL[0], pts:pts1}]});
    var r1 = [];
    if (distinct(rec.map(function(d){ return d.rcm; })) >= 2){
      var k1 = fit0(pts1);
      r1.push('<li>원점을 지나는 직선의 기울기 <b>' + f(k1, 2) + '</b> — 공에서는 S ÷ V = 3 ÷ r이므로 3이 나와요.</li>');
    } else r1.push('<li>몸 크기를 2가지 이상 바꿔 기록해 보세요.</li>');
    var sm = rec.slice().sort(function(a, b){ return a.rcm - b.rcm; });
    r1.push('<li>가장 작은 몸(' + f(sm[0].rcm, 1) + ' cm)의 S÷V는 <b>' + f(sm[0].sv, 1) + '</b>, 가장 큰 몸(' + f(sm[sm.length-1].rcm, 1) + ' cm)은 <b>' + f(sm[sm.length-1].sv, 1) + '</b>예요.</li>');
    r1.push('<li>몸이 작을수록 부피에 비해 표면이 넓어 열을 <b>빨리</b> 잃어요.</li>');
    $('ro1').innerHTML = r1.join('');
    var be = groupBy(rec, function(d){ return d.ear; }), s2 = [], r2 = [], ci = 0;
    Object.keys(be).forEach(function(k){
      var g = be[k], col = PAL[ci++ % PAL.length];
      s2.push({color:col, pts:g.map(function(d){ return {x:d.Ta, y:d.Q}; })});
      r2.push('<li>' + dot(col) + k + ': 기록 ' + g.length + '개, 평균 ' + sgn(mean(g.map(function(d){ return d.Q; })), 1) + ' W</li>');
    });
    drawScatter($('ch2'), {xLabel:'바깥 기온 (°C)', yLabel:'나가는 열 (W, 음수는 들어옴)', series:s2, lines:[{h:0, color:'#8C99A8', dash:[6,4]}]});
    $('ro2').innerHTML = r2.join('') +
      '<li>기온이 낮을수록 열을 많이 잃어요. 체온 38 °C를 넘는 40 °C에서는 부호가 뒤집혀 <b>열이 들어와요</b>.</li>' +
      '<li>큰 귀는 방열 면적을 늘리는 장치라, 더운 곳에서는 <b>밤에</b> 열을 버리는 데 유리해요.</li>';
    var rows = [
      ['사막여우', '작음 (약 1 kg)', '매우 큼', '큼', '큼 — 열을 잘 버림', '덥고 건조한 사막'],
      ['붉은여우', '중간 (약 6 kg)', '보통', '보통', '보통', '온대'],
      ['북극여우', '큼 (약 4~9 kg, 뭉툭함)', '작음', '작음', '작음 — 열을 아낌', '춥고 바람 부는 북극']
    ];
    $('ro3').innerHTML = tableHTML(['동물', '몸집', '귀', 'S ÷ V', '열 손실', '사는 곳'], rows, 'wrap') +
      '<p class="note">환경이 생물의 모양을 <b>정해 주는</b> 것이 아니라, 그 환경에서 살아남기 쉬운 모양이 오래 남은 결과예요(자연 선택).</p>';
  }
};`
},

/* ===================== 35. 엘니뇨 (EnvEnergy Ep04) ===================== */
{
  file: '35_elnino_trade_wind_lab_IntegSci2_EnvEnergy_Ep04.html',
  title: '무역풍이 약해지면',
  intro: '태평양 적도 부근에서 무역풍의 세기를 바꿔 가며 서·동 태평양의 해수면 온도와 용승, 강수 위치, 페루 앞바다의 어획량이 어떻게 달라지는지 확인해 보세요.',
  sceneNote: '적도 태평양을 옆에서 본 단면 모형입니다. 수온·용승·어획량·비구름 위치는 평년을 기준으로 삼은 개념 비교용 어림값이며, 실제 예측값이 아닙니다.',
  runLabel: '바람 불게 하기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 대기와 해양은 함께 움직인다</h3>
<p>적도 부근에서는 동쪽에서 서쪽으로 <b>무역풍</b>이 불어요. 이 바람이 따뜻한 표층 해수를 서태평양으로 밀어 쌓기 때문에, 동태평양(페루 앞바다)에서는 아래의 <b>차갑고 영양분 많은 물이 올라와요</b>(용승). 그래서 서쪽은 따뜻하고 비가 많으며 동쪽은 서늘하고 건조해요. 그런데 무역풍이 약해지면 따뜻한 물이 동쪽으로 되돌아와 용승이 막히고 동태평양이 따뜻해져요. 이것이 <b>엘니뇨</b>예요. 반대로 무역풍이 세지면 <b>라니냐</b>가 돼요.</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>평년에는 서태평양 약 29 °C, 동태평양 약 22 °C로 <b>7 °C</b>쯤 차이가 나요.</li>
<li>실제 판정에 쓰는 ONI는 니뇨 3.4 해역 수온 편차의 <b>3개월 이동 평균</b>이 <b>±0.5 °C</b>를 5개월 이상 넘을 때 엘니뇨·라니냐로 봐요. 이 실험은 그 조건을 단순화해 <b>한 시점의 편차</b>만으로 판정해요.</li>
<li>용승이 약해지면 영양분이 줄어 플랑크톤이 줄고, 멸치 어획량이 크게 떨어져요.</li>
<li>바다가 바뀌면 비구름의 자리도 옮겨 가, 인도네시아·호주에는 가뭄이, 페루에는 폭우가 오기도 해요.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p>무역풍 세기 w에 대해 <span class="fx-formula">동태평양 = 22 + 6(1 − w)</span>, <span class="fx-formula">서태평양 = 29 + 1.2(w − 1)</span>로 평형값을 정하고, <span class="fx-formula">현재 = 평년 + (평형 − 평년)(1 − e<sup>−t÷3</sup>)</span>로 t개월 뒤를 구합니다.</p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 태평양을 두 상자(서·동)로 줄인 <b>아주 단순한 모형</b>이에요. 실제 엘니뇨는 바다의 파동(켈빈파)과 바람이 서로를 키우는 되먹임으로 생기고, 2~7년 주기로 오락가락해요.<br>
· 바람이 수온을 바꾸면 그 수온이 다시 바람을 바꾸는 <b>되먹임</b>을 넣지 않았어요. 실제로는 이 되먹임 때문에 한번 시작되면 스스로 커져요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>엘니뇨가 오면 페루 어부들이 잡는 멸치가 크게 줄어 사료값과 물가가 세계적으로 올라요.</li>
<li>'엘니뇨(아기 예수)'라는 이름은 이 현상이 크리스마스 무렵에 두드러지는 데서 왔어요.</li>
</ul>`,
  js: `
var BASE_E = 22, BASE_W = 29;
return {
  sceneHeight: 470,
  minRec: 4,
  idle: '무역풍 세기와 유지 기간을 정하고 <b>바람 불게 하기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 무역풍 세기를 여러 값으로 바꿔 기록하세요.',
  params: [
    {key:'w', type:'range', label:'무역풍 세기 (평년 = 100 %)', min:0, max:150, step:10, value:100, fmt:function(v){ return v + ' %'; }},
    {key:'t', type:'range', label:'그 상태가 이어진 기간', min:1, max:12, step:1, value:6, fmt:function(v){ return v + '개월'; },
      note:'평년 상태(서 29 °C, 동 22 °C)에서 출발합니다. 바다는 바람의 변화를 몇 달에 걸쳐 따라갑니다.'}
  ],
  compute: function(p){
    var w = p.w / 100, t = p.t, k = 1 - Math.exp(-t / 3);
    var eqE = BASE_E + 6 * (1 - w), eqW = BASE_W + 1.2 * (w - 1);
    var sstE = BASE_E + (eqE - BASE_E) * k, sstW = BASE_W + (eqW - BASE_W) * k;
    var up = 100 * w, oni = sstE - BASE_E;
    var fish = 100 * Math.pow(Math.max(up, 1) / 100, 0.8);
    var phase = oni >= 0.5 ? '엘니뇨' : oni <= -0.5 ? '라니냐' : '평년';
    var rainLon = Math.min(200, Math.max(120, 140 + (1 - w) * 60));   // °E, 커질수록 동쪽 (그림과 같은 식)
    return {w:w, wp:p.w, t:t, sstE:sstE, sstW:sstW, diff:sstW - sstE, up:up, oni:oni,
      fish:fish, phase:phase, rainLon:rainLon, slope:60 * w};
  },
  draw: function(c, W, H, p, r, tau){
    var padL = 40, padR = 40, top = 80, sea = 172, seaH = 145;
    var x0 = padL, x1 = W - padR;
    var w = r ? 1 + (p.w / 100 - 1) * tau : p.w / 100;
    // 하늘
    c.fillStyle = '#EAF3FA'; c.fillRect(x0, top, x1 - x0, sea - top);
    // 바다
    var tilt = 26 * w;
    c.fillStyle = '#9EC3DE';
    c.beginPath(); c.moveTo(x0, sea + tilt); c.lineTo(x1, sea - tilt); c.lineTo(x1, sea + seaH); c.lineTo(x0, sea + seaH); c.closePath(); c.fill();
    // 따뜻한 층
    c.fillStyle = '#E3A66B';
    c.beginPath(); c.moveTo(x0, sea + tilt); c.lineTo(x1, sea - tilt);
    c.lineTo(x1, sea - tilt + 20 + 40 * (1 - w)); c.lineTo(x0, sea + tilt + 90 * w + 20); c.closePath(); c.fill();
    c.strokeStyle = '#5B6776'; c.lineWidth = 2;
    c.beginPath(); c.moveTo(x0, sea + tilt); c.lineTo(x1, sea - tilt); c.stroke();
    txt(c, '서태평양 (인도네시아)', x0 + 6, top - 14, {color:'#4A5868'});
    txt(c, '동태평양 (페루)', x1 - 6, top - 14, {align:'right', color:'#4A5868'});
    // 무역풍 화살표
    var n = Math.max(1, Math.round(w * 6));
    for (var i = 0; i < n; i++){
      var yy = top + 10 + i * 7;
      arrow(c, x1 - 20, yy, x0 + 40, yy, '#2B5FA3', 2);
    }
    txt(c, '무역풍 ' + p.w + ' %', x1 - 24, top + 10 + n * 7 + 16, {align:'right', color:'#2B5FA3', bold:true});
    // 용승
    if (w > 0.05){
      var un = Math.max(1, Math.round(w * 4));
      for (var j = 0; j < un; j++) arrow(c, x1 - 40 - j * 16, sea + seaH - 10, x1 - 40 - j * 16, sea - tilt + 14, '#2E9E78', 2);
      txt(c, '용승', x1 - 40, sea + seaH + 22, {align:'center', color:'#2E9E78', bold:true});
    } else txt(c, '용승 거의 없음', x1 - 60, sea + seaH + 22, {align:'center', color:'#C8463D', bold:true});
    // 비구름
    if (r){
      var lon = Math.min(200, Math.max(120, 140 + (1 - w) * 60));      // compute의 rainLon과 같은 식
      var cxr = x0 + 70 + (lon - 120) / 80 * (x1 - x0 - 140);
      c.fillStyle = '#A8B3BF';
      c.beginPath(); c.arc(cxr, top + 56, 17, 0, Math.PI * 2); c.arc(cxr + 19, top + 59, 13, 0, Math.PI * 2); c.fill();
      for (var q = 0; q < 5; q++) seg(c, cxr - 14 + q * 9, top + 72, cxr - 17 + q * 9, top + 84, '#5B8FB9', 2);
      txt(c, '비구름', Math.min(cxr + 40, x1 - 60), top + 52, {color:'#4A5868'});
    }
    if (!r){ txt(c, '무역풍이 따뜻한 물을 서쪽으로 밀어요.', x0, H - 18, {color:'#4A5868'}); return; }
    if (tau < 1) return;
    var yy2 = sea + seaH + 56;
    txt(c, '서태평양 ' + f(r.sstW, 1) + ' °C · 동태평양 ' + f(r.sstE, 1) + ' °C (차이 ' + f(r.diff, 1) + ' °C)', x0, yy2, {bold:true, color:'#2B5FA3'});
    txt(c, '수온 편차(단순 지수) ' + sgn(r.oni, 2) + ' °C → ' + r.phase + ' · 용승 ' + f(r.up, 0) + ' % · 어획량 ' + f(r.fish, 0) + ' %', x0, yy2 + 30,
      {bold:true, color:r.phase === '엘니뇨' ? '#C8463D' : r.phase === '라니냐' ? '#2B5FA3' : '#2E9E78'});
    txt(c, r.phase === '엘니뇨' ? '비구름이 동쪽으로 옮겨 가 페루에는 폭우, 인도네시아·호주에는 가뭄이 들기 쉬워요.'
      : r.phase === '라니냐' ? '용승이 세져 동태평양이 더 차가워지고 서쪽에 비가 더 많이 와요.'
      : '평년에 가까운 상태예요.', x0, H - 14, {color:'#4A5868'});
  },
  stats: function(p, r){
    return [['무역풍 세기', r.wp + ' %'], ['이어진 기간', r.t + '개월'],
      ['서태평양 수온', f(r.sstW, 2) + ' °C', PAL[2]], ['동태평양 수온', f(r.sstE, 2) + ' °C', PAL[0]],
      ['동서 수온 차이', f(r.diff, 2) + ' °C'], ['해수면 높이 차(어림)', f(r.slope, 0) + ' cm'],
      ['용승 강도', f(r.up, 0) + ' %', PAL[1]], ['동태평양 수온 편차 (단순 지수)', sgn(r.oni, 2) + ' °C', PAL[4]],
      ['모형 판정 (단순 기준)', r.phase, r.phase === '평년' ? PAL[1] : PAL[4]],
      ['페루 앞바다 어획량', f(r.fish, 0) + ' %'], ['비구름 중심(어림)', f(r.rainLon, 0) + ' °E']];
  },
  columns: ['무역풍 (%)', '기간 (개월)', '서태평양 (°C)', '동태평양 (°C)', '차이 (°C)', '용승 (%)', '지수 (°C)', '판정', '어획량 (%)'],
  record: function(p, r){
    return {wp:r.wp, t:r.t, sstW:r.sstW, sstE:r.sstE, diff:r.diff, up:r.up, oni:r.oni, phase:r.phase, fish:r.fish};
  },
  row: function(d){ return [d.wp, d.t, f(d.sstW, 2), f(d.sstE, 2), f(d.diff, 2), f(d.up, 0), sgn(d.oni, 2), d.phase, f(d.fish, 0)]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('무역풍과 동서 수온', '<canvas class="chart" id="ch1" role="img" aria-label="무역풍 세기와 동서 해수면 온도 산점도"></canvas><ul class="readout" id="ro1"></ul><p class="ask">두 선이 서로 반대 방향으로 움직입니다. 따뜻한 물이 어디로 갔는지로 설명해 보세요.</p>') +
      card('용승과 어획량', '<canvas class="chart" id="ch2" role="img" aria-label="용승 강도와 어획량 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">바다 아래에서 올라오는 물이 왜 물고기를 부를까요? 기권·수권·생물권이 어떻게 이어지나요?</p>') +
      card('평년 · 엘니뇨 · 라니냐', '<div id="ro3"></div><p class="ask">같은 바다인데 몇 달 만에 날씨가 지구 반대편까지 달라집니다. 이것이 지구 시스템의 무엇을 보여 줄까요?</p>') + '</div>';
    var full = rec.filter(function(d){ return d.t >= 6; });
    var use = full.length >= 2 ? full : rec;
    drawScatter($('ch1'), {xLabel:'무역풍 세기 (%)', yLabel:'해수면 온도 (°C)', tightX:true, tightY:true,
      series:[{color:PAL[2], pts:use.map(function(d){ return {x:d.wp, y:d.sstW}; })},
              {color:PAL[0], pts:use.map(function(d){ return {x:d.wp, y:d.sstE}; })}]});
    var r1 = ['<li>' + dot(PAL[2]) + '서태평양 · ' + dot(PAL[0]) + '동태평양' + (full.length >= 2 ? ' (6개월 이상 이어진 기록)' : '') + '</li>'];
    if (distinct(use.map(function(d){ return d.wp; })) >= 2){
      var Le = linfit(use.map(function(d){ return {x:d.wp, y:d.sstE}; }));
      r1.push('<li>동태평양: 무역풍이 10 % 약해질 때마다 약 <b>' + f(-Le.k * 10, 2) + ' °C</b> 따뜻해져요.</li>');
    } else r1.push('<li>무역풍 세기를 2가지 이상 바꿔 기록해 보세요.</li>');
    r1.push('<li>바람이 약해지면 서쪽에 쌓여 있던 따뜻한 물이 <b>동쪽으로 되돌아와</b> 동서 온도 차가 줄어요.</li>');
    $('ro1').innerHTML = r1.join('');
    drawScatter($('ch2'), {xLabel:'용승 강도 (%)', yLabel:'페루 앞바다 어획량 (%)', series:[{color:PAL[1], pts:rec.map(function(d){ return {x:d.up, y:d.fish}; })}]});
    var weak = rec.filter(function(d){ return d.up < 60; });
    $('ro2').innerHTML = '<li>용승이 셀수록 어획량이 많아요. 깊은 물에는 <b>영양 염류</b>가 많아 플랑크톤이 늘고, 그것을 먹는 물고기가 모이기 때문이에요.</li>' +
      (weak.length ? '<li>용승이 60 % 아래였던 기록 ' + weak.length + '개의 평균 어획량은 <b>' + f(mean(weak.map(function(d){ return d.fish; })), 0) + ' %</b>예요.</li>' : '') +
      '<li>기권(바람) → 수권(해류·용승) → 생물권(플랑크톤·물고기)으로 이어지는 상호작용이에요.</li>';
    var bp = groupBy(rec, function(d){ return d.phase; }), rows = [];
    ['라니냐', '평년', '엘니뇨'].forEach(function(k){
      var g = bp[k];
      if (!g) { rows.push([k, '0개', '—', '—', '—', '—']); return; }
      rows.push([k, g.length + '개', f(mean(g.map(function(d){ return d.wp; })), 0) + ' %',
        f(mean(g.map(function(d){ return d.sstE; })), 2) + ' °C', f(mean(g.map(function(d){ return d.diff; })), 2) + ' °C',
        f(mean(g.map(function(d){ return d.fish; })), 0) + ' %']);
    });
    $('ro3').innerHTML = tableHTML(['상태', '내 기록', '평균 무역풍', '평균 동태평양 수온', '평균 동서 차', '평균 어획량'], rows) +
      '<p class="note">지구 시스템의 한 곳이 바뀌면 멀리 떨어진 곳까지 영향을 줘요. 엘니뇨는 남아메리카·동남아시아·아프리카의 날씨를 한꺼번에 바꿔요.</p>';
  }
};`
},

/* ===================== 36. 태양의 핵융합 (EnvEnergy Ep05) ===================== */
{
  file: '36_solar_fusion_mass_defect_lab_IntegSci2_EnvEnergy_Ep05.html',
  title: '태양은 무엇을 태우고 있을까',
  intro: '별의 질량과 태울 수 있는 수소의 비율을 바꿔 가며, 초마다 사라지는 질량과 그 별이 빛날 수 있는 시간을 계산합니다. 질량이 에너지로 바뀐다는 식을 직접 확인해 보세요.',
  sceneNote: '수소 4개가 헬륨 1개로 합쳐질 때 질량의 약 0.7 %가 에너지로 바뀝니다. 별의 밝기는 질량의 3.5제곱에 비례한다고 두었습니다.',
  runLabel: '1초 동안 계산하기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 수소 핵융합과 질량 결손</h3>
<p>태양은 장작처럼 <b>타는</b> 것이 아니에요. 중심의 1 500만 K, 엄청난 압력에서 수소 원자핵 4개가 헬륨 원자핵 1개로 합쳐지는 <b>핵융합</b>이 일어나요. 그런데 합쳐진 헬륨의 질량은 원래 수소 4개보다 약 <b>0.7 % 작아요</b>. 사라진 질량이 <span class="fx-formula">E = mc²</span>에 따라 에너지로 바뀐 거예요. 빛의 속력을 제곱한 값이 워낙 커서, 아주 적은 질량으로도 어마어마한 에너지가 나와요.</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>태양의 밝기 3.85 × 10²⁶ W. 1초에 필요한 질량 결손은 <span class="fx-formula">m = E ÷ c² = 3.85×10²⁶ ÷ 9×10¹⁶ ≈ 4.3 × 10⁹ kg</span> — 약 <b>430만 t</b>이에요.</li>
<li>그만큼을 내려면 수소 <span class="fx-formula">4.3×10⁹ ÷ 0.007 ≈ 6 × 10¹¹ kg</span>, 즉 <b>6억 t</b>이 1초마다 헬륨으로 바뀌어요.</li>
<li>태양 질량의 10 %를 쓸 수 있다고 보면 수명은 약 <b>100억 년</b>이고, 지금 약 46억 년이 지났어요.</li>
<li>무거운 별은 밝기가 질량의 3.5제곱으로 커져 연료를 훨씬 빨리 써요: <span class="fx-formula">수명 ∝ M ÷ M³·⁵ = M⁻²·⁵</span>.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p><span class="fx-formula">L = L<sub>☉</sub> × M³·⁵</span>, <span class="fx-formula">초당 질량 결손 = L ÷ c²</span>, <span class="fx-formula">초당 수소 소모 = 결손 ÷ 0.007</span>, <span class="fx-formula">수명 = 0.007 × 비율 × M × c² ÷ L</span></p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 질량–광도 관계 <b>L ∝ M³·⁵</b>는 주계열성에서 대략 맞는 경험식이에요. 아주 가볍거나 무거운 별에서는 지수가 달라져요.<br>
· 태울 수 있는 수소를 전체 질량의 몇 %로 두었어요. 실제로는 중심핵에서만 융합이 일어나고, 별의 구조에 따라 그 몫이 달라져요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>지구에 도달하는 태양 에너지는 전체의 22억 분의 1인데도, 그것이 바람·해류·비·광합성을 모두 움직여요.</li>
<li>핵융합 발전은 이 반응을 땅 위에서 흉내 내려는 시도예요. 연료가 흔하고 오래가는 방사성 폐기물이 적은 것이 장점이에요.</li>
</ul>`,
  js: `
var C2 = 8.98755e16, LSUN = 3.846e26, MSUN = 1.989e30, YR = 3.156e7;
var MASS = [0.5, 1, 2, 10];
return {
  sceneHeight: 460,
  minRec: 4,
  idle: '별의 질량과 태울 수 있는 수소 비율을 정하고 <b>1초 동안 계산하기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 별의 질량을 바꿔 가며 기록하세요.',
  params: [
    {key:'m', type:'seg', label:'별의 질량', cols:4, value:1, options:MASS.map(function(v){ return f(v, 1) + ' M☉'; })},
    {key:'p', type:'range', label:'태울 수 있는 수소의 비율', min:5, max:15, step:1, value:10, fmt:function(v){ return v + ' %'; },
      note:'태양 질량 M☉ = 1.989 × 10³⁰ kg, 태양 밝기 L☉ = 3.846 × 10²⁶ W입니다.'}
  ],
  compute: function(p){
    var M = MASS[p.m], frac = p.p / 100;
    var L = LSUN * Math.pow(M, 3.5);
    var dm = L / C2;                       // kg/s 질량 결손
    var dh = dm / 0.007;                   // kg/s 수소 소모
    var E = 0.007 * frac * M * MSUN * C2;
    var life = E / L;                      // s
    return {M:M, frac:frac, L:L, Lrel:Math.pow(M, 3.5), dm:dm, dh:dh, E:E,
      lifeYr:life / YR, lifeRel:Math.pow(M, -2.5) * (frac / 0.10),
      dmT:dm / 1000, dhT:dh / 1000, checkE:dm * C2};
  },
  draw: function(c, W, H, p, r, tau){
    var cx = Math.min(210, W * 0.26), cy = 200;
    var R = 40 + Math.log(MASS[p.m] + 1) * 34;
    // 별
    var grd = c.createRadialGradient(cx, cy, R * 0.2, cx, cy, R);
    grd.addColorStop(0, '#FFF3C4'); grd.addColorStop(0.6, '#F7C14B'); grd.addColorStop(1, '#E08A2E');
    c.fillStyle = grd; c.beginPath(); c.arc(cx, cy, R, 0, Math.PI * 2); c.fill();
    if (r){
      for (var i = 0; i < 14; i++){
        var ang = i * Math.PI * 2 / 14 + tau * 0.5, len = R + 14 + 14 * ((tau + i / 14) % 1);
        seg(c, cx + Math.cos(ang) * (R + 6), cy + Math.sin(ang) * (R + 6), cx + Math.cos(ang) * len, cy + Math.sin(ang) * len, 'rgba(216,142,4,.6)', 2);
      }
    }
    txt(c, f(MASS[p.m], 1) + ' M☉', cx, cy + 6, {align:'center', bold:true, color:'#6E4A1E'});
    txt(c, '별 중심의 핵융합', cx, cy + R + 34, {align:'center', color:'#4A5868'});
    // 반응식
    var rx = cx + R + 60;
    if (rx < W - 260){
      txt(c, '4 ¹H → ⁴He + 에너지', rx, 120, {bold:true, color:'#2B5FA3'});
      txt(c, '질량의 0.7 %가 사라져 빛이 돼요', rx, 150, {color:'#4A5868'});
      if (r){
        txt(c, '초당 질량 결손', rx, 194, {color:'#4A5868'});
        meter(c, rx, 204, Math.min(230, W - rx - 12), f(r.dm * tau / 1e9, 2) + ' × 10⁹ kg');
        txt(c, '초당 수소 소모', rx, 266, {color:'#4A5868'});
        meter(c, rx, 276, Math.min(230, W - rx - 12), f(r.dh * tau / 1e11, 2) + ' × 10¹¹ kg');
      }
    }
    if (!r){ txt(c, '별의 질량이 클수록 훨씬 밝게 빛나요.', 20, H - 18, {color:'#4A5868'}); return; }
    if (tau < 1) return;
    var yy = H - 104;
    txt(c, '밝기 L = ' + r.L.toExponential(2) + ' W (태양의 ' + f(r.Lrel, 1) + '배)', 20, yy, {bold:true, color:'#D98E04'});
    txt(c, 'E = mc² 확인: ' + r.dm.toExponential(2) + ' kg × c² = ' + r.checkE.toExponential(2) + ' J — 1초 동안 낸 에너지와 같아요.', 20, yy + 30, {});
    txt(c, '수명 약 ' + (r.lifeYr / 1e9).toFixed(2) + '십억 년 (태양의 ' + f(r.lifeRel, 2) + '배)', 20, H - 14,
      {bold:true, color:'#2E9E78'});
  },
  stats: function(p, r){
    return [['별의 질량', f(r.M, 1) + ' M☉ = ' + (r.M * MSUN).toExponential(2) + ' kg'],
      ['밝기 L', r.L.toExponential(3) + ' W', PAL[6]], ['태양 대비 밝기', f(r.Lrel, 2) + '배'],
      ['초당 질량 결손', r.dm.toExponential(3) + ' kg/s', PAL[4]],
      ['초당 질량 결손(톤)', Math.round(r.dmT / 1e4).toLocaleString() + ' 만 t/s'],
      ['초당 수소 → 헬륨', r.dh.toExponential(3) + ' kg/s', PAL[0]],
      ['E = mc² 검산', r.checkE.toExponential(3) + ' J (1초분 에너지)'],
      ['태울 수 있는 수소', f(r.frac * 100, 0) + ' %'],
      ['쓸 수 있는 에너지', r.E.toExponential(3) + ' J'],
      ['수명', (r.lifeYr / 1e9).toFixed(2) + ' 십억 년', PAL[1]],
      ['태양 대비 수명', f(r.lifeRel, 3) + '배']];
  },
  columns: ['질량 (M☉)', '수소 비율 (%)', '밝기 (W)', '태양 대비 밝기', '질량 결손 (kg/s)', '수소 소모 (kg/s)', '수명 (십억 년)'],
  record: function(p, r){
    return {M:r.M, frac:r.frac, L:r.L, Lrel:r.Lrel, dm:r.dm, dh:r.dh, life:r.lifeYr / 1e9, lifeRel:r.lifeRel};
  },
  row: function(d){ return [f(d.M, 1), f(d.frac * 100, 0), d.L.toExponential(2), f(d.Lrel, 2), d.dm.toExponential(2),
    d.dh.toExponential(2), (d.life).toFixed(2)]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('질량과 밝기', '<canvas class="chart" id="ch1" role="img" aria-label="질량 로그값과 밝기 로그값 산점도"></canvas><ul class="readout" id="ro1"></ul><p class="ask">가로·세로 모두 10의 거듭제곱으로 그렸습니다. 기울기 3.5는 무엇을 뜻할까요?</p>') +
      card('질량과 수명', '<canvas class="chart" id="ch2" role="img" aria-label="질량 로그값과 수명 로그값 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">연료가 10배 많은 별이 왜 더 빨리 죽을까요? 밝기와 연결해 설명해 보세요.</p>') +
      card('E = mc² 검산', '<div id="ro3"></div><p class="ask">1초에 사라지는 질량이 이렇게 적은데 에너지가 어마어마한 까닭은 무엇일까요?</p>') + '</div>';
    var pts1 = rec.map(function(d){ return {x:Math.log10(d.M), y:Math.log10(d.Lrel)}; });
    drawScatter($('ch1'), {xLabel:'log₁₀(질량 ÷ M☉)', yLabel:'log₁₀(밝기 ÷ L☉)', tightX:true, tightY:true, series:[{color:PAL[6], pts:pts1}]});
    var r1 = [];
    if (distinct(rec.map(function(d){ return d.M; })) >= 2){
      var L1 = linfit(pts1);
      r1.push('<li>직선의 기울기 <b>' + f(L1.k, 2) + '</b> — 질량이 2배면 밝기는 2<sup>3.5</sup> ≈ <b>11배</b>가 돼요.</li>');
    } else r1.push('<li>별의 질량을 2가지 이상 바꿔 기록해 보세요.</li>');
    r1.push('<li>무거울수록 중심의 압력과 온도가 높아 핵융합이 훨씬 격렬하게 일어나기 때문이에요.</li>');
    $('ro1').innerHTML = r1.join('');
    var pts2 = rec.map(function(d){ return {x:Math.log10(d.M), y:Math.log10(d.lifeRel)}; });
    drawScatter($('ch2'), {xLabel:'log₁₀(질량 ÷ M☉)', yLabel:'log₁₀(수명 ÷ 태양 수명)', tightX:true, tightY:true, series:[{color:PAL[1], pts:pts2}]});
    var r2 = [];
    if (distinct(rec.map(function(d){ return d.M; })) >= 2){
      var L2 = linfit(pts2);
      r2.push('<li>직선의 기울기 <b>' + f(L2.k, 2) + '</b> — 수명 ∝ M ÷ M³·⁵ = M<sup>−2.5</sup>예요.</li>');
    } else r2.push('<li>별의 질량을 2가지 이상 바꿔 기록해 보세요.</li>');
    var hv = rec.slice().sort(function(a, b){ return b.M - a.M; })[0];
    r2.push('<li>내 기록 중 가장 무거운 ' + f(hv.M, 1) + ' M☉ 별의 수명은 <b>' + (hv.life).toFixed(3) + ' 십억 년</b>이에요.</li>');
    r2.push('<li>연료는 많지만 <b>훨씬 빨리</b> 써요. 큰 차가 기름통이 커도 연비가 나빠 금방 비는 것과 같아요.</li>');
    $('ro2').innerHTML = r2.join('');
    var seen = {}, rows = [];
    rec.forEach(function(d){ if (seen[d.M]) return; seen[d.M] = 1;
      rows.push([f(d.M, 1) + ' M☉', d.L.toExponential(2) + ' W', d.dm.toExponential(2) + ' kg',
        (d.dm * C2).toExponential(2) + ' J', d.dh.toExponential(2) + ' kg']); });
    rows.sort(function(a, b){ return parseFloat(a[0]) - parseFloat(b[0]); });
    $('ro3').innerHTML = tableHTML(['질량', '밝기(1초당 에너지)', '1초당 사라진 질량 m', 'm × c²', '1초당 수소 소모'], rows, 'wrap') +
      '<p class="note">세 번째 칸에 c² = 9 × 10¹⁶을 곱하면 두 번째 칸과 같아요. c²가 워낙 커서 <b>1 g만 사라져도 9 × 10¹³ J</b>이 나와요. 4인 가구가 한 달에 300 kWh(약 1.08 × 10⁹ J)를 쓴다고 하면 <b>약 8만 가구의 한 달치</b>예요.</p>';
  }
};`
},

/* ===================== 37. 발전소의 열효율 (EnvEnergy Ep07) ===================== */
{
  file: '37_power_plant_efficiency_lab_IntegSci2_EnvEnergy_Ep07.html',
  title: '발전소는 결국 물을 끓인다',
  intro: '석탄·천연가스·원자력·지열 발전소에서 증기의 온도와 냉각수 온도를 바꿔 가며 효율과 버려지는 열을 계산합니다. 연료가 달라도 구조가 같다는 것을 확인해 보세요.',
  sceneNote: '전기 출력 1 000 MW로 맞춘 모형입니다. 카르노 효율은 이론 최대값이고, 실제 효율은 방식별 기술 계수를 곱해 어림했습니다.',
  runLabel: '발전소 돌리기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 열기관에는 넘을 수 없는 한계가 있다</h3>
<p>석탄·천연가스·원자력·지열은 연료가 달라 보이지만, <b>열을 받아 터빈을 돌려 전기를 만든다</b>는 점은 같아요. 석탄·원자력은 물을 끓여 <b>증기 터빈</b>을 돌리고, 천연가스 복합 화력은 연소 가스로 <b>가스 터빈</b>을 먼저 돌린 뒤 그 배기열로 증기를 만들어 증기 터빈까지 돌려요(지열도 증기 직접 이용·플래시·바이너리 방식이 있어요). 이런 장치를 <b>열기관</b>이라 하는데, 높은 온도에서 열을 받아 일부를 일로 바꾸고 <b>나머지는 반드시 낮은 온도로 버려야</b> 해요. 버리지 않으면 계속 돌 수 없어요. 그래서 이론적인 최대 효율이 <span class="fx-formula">1 − T<sub>저온</sub> ÷ T<sub>고온</sub></span>(절대 온도)로 정해져요. 효율을 올리려면 증기를 더 뜨겁게 하거나 냉각수를 더 차게 해야 해요.</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>증기 600 °C(873 K), 냉각수 20 °C(293 K)면 카르노 효율 = 1 − 293 ÷ 873 = <b>66 %</b>. 실제 석탄 화력은 40 % 안팎이에요.</li>
<li>원자력은 안전상 증기 온도를 약 330 °C로 낮게 써서 효율이 33 % 정도로 더 낮아요.</li>
<li>1 000 MW를 내는 효율 40 % 발전소는 2 500 MW의 열을 넣고 <b>1 500 MW를 버려요</b>. 그 열이 냉각탑의 수증기와 바닷물의 온도로 나가요.</li>
<li>태양광·풍력은 열기관이 아니라 이 한계를 받지 않아요.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p><span class="fx-formula">카르노 = 1 − T<sub>저온</sub> ÷ T<sub>고온</sub></span>, <span class="fx-formula">실제 = 카르노 × 기술 계수</span>, <span class="fx-formula">투입 열 = 1000 ÷ 실제</span>, <span class="fx-formula">폐열 = 투입 − 1000</span> (MW)</p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 실제 효율을 <b>카르노 × 고정 계수</b>로 단순화했어요. 실제 발전소는 재열·재생 사이클, 복합 발전처럼 구조를 바꿔 효율을 올려요(최신 LNG 복합은 60 % 이상).<br>
· 이산화 탄소 배출 계수는 연료를 태울 때만이 아니라 건설·채굴까지 포함한 <b>수명 주기 어림값</b>이에요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>발전소가 강이나 바다 옆에 있는 까닭은 버릴 열을 식힐 물이 필요하기 때문이에요.</li>
<li>버리는 열을 난방에 쓰는 것이 열병합 발전이에요. 전기 효율은 같아도 전체 에너지 이용률이 훨씬 높아져요.</li>
</ul>`,
  js: `
var PLANT = [
  {n:'석탄 화력', k:0.62, co2:820, th:[400, 620], note:'값싸지만 배출이 가장 많음'},
  {n:'천연가스', k:0.72, co2:490, th:[400, 620], note:'배출이 석탄의 약 60 %'},
  {n:'원자력',  k:0.65, co2:12,  th:[300, 350], note:'안전상 증기 온도가 낮아 효율도 낮음'},
  {n:'지열',   k:0.50, co2:38,  th:[150, 250], note:'열원의 온도가 낮아 효율이 크게 낮음'}
];
var COLD = [10, 20, 30];
var POUT = 1000;
return {
  sceneHeight: 460,
  minRec: 4,
  idle: '발전 방식과 증기 온도, 냉각수 온도를 정하고 <b>발전소 돌리기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 증기 온도와 냉각수 온도를 바꿔 가며 기록하세요.',
  params: [
    {key:'p', type:'seg', label:'발전 방식', cols:4, value:0, options:PLANT.map(function(x){ return x.n + '<small>' + x.co2 + ' g/kWh</small>'; })},
    {key:'h', type:'range', label:'증기(고온부) 온도', min:150, max:650, step:25, value:550, fmt:function(v){ return v + ' °C'; }},
    {key:'c', type:'seg', label:'냉각수 온도', cols:3, value:1, options:COLD.map(function(v){ return v + ' °C'; }),
      note:'전기 출력은 1 000 MW로 맞췄습니다. 방식마다 실제로 쓰는 증기 온도 범위가 달라 그 밖으로 나가면 안내가 뜹니다.'}
  ],
  compute: function(p){
    var P = PLANT[p.p], Th = p.h + 273.15, Tc = COLD[p.c] + 273.15;
    if (p.h <= COLD[p.c] + 20) return {fail:'증기 온도가 냉각수 온도보다 충분히 높아야 발전할 수 있어요. 증기 온도를 올려 보세요.'};
    var carnot = 1 - Tc / Th, eff = carnot * P.k;
    var qin = POUT / eff, waste = qin - POUT;
    var inRange = p.h >= P.th[0] && p.h <= P.th[1];
    var kwhYr = POUT * 1000 * 8760 * 0.8;               // kWh/년 (이용률 80 %)
    return {P:P, Th:p.h, Tc:COLD[p.c], ThK:Th, TcK:Tc, ratio:Tc / Th, carnot:carnot, eff:eff,
      qin:qin, waste:waste, inRange:inRange, co2:P.co2 * kwhYr / 1e9, wasteFrac:waste / qin};
  },
  draw: function(c, W, H, p, r, tau){
    var P = PLANT[p.p];
    var bx = 40, by = 110;
    // 보일러
    c.fillStyle = '#F6E2CE'; c.fillRect(bx, by, 120, 110);
    c.strokeStyle = '#C8463D'; c.lineWidth = 2; c.strokeRect(bx, by, 120, 110);
    txt(c, '보일러', bx + 60, by - 12, {align:'center', bold:true, color:'#C8463D'});
    txt(c, p.h + ' °C', bx + 60, by + 62, {align:'center', bold:true});
    // 터빈
    var tx = bx + 170;
    c.fillStyle = '#E4EAF1'; c.fillRect(tx, by + 10, 110, 90);
    c.strokeStyle = '#2B5FA3'; c.lineWidth = 2; c.strokeRect(tx, by + 10, 110, 90);
    txt(c, '터빈·발전기', tx + 55, by - 12, {align:'center', bold:true, color:'#2B5FA3'});
    if (r){
      c.save(); c.translate(tx + 55, by + 55); c.rotate(tau * 8);
      c.strokeStyle = '#2B5FA3'; c.lineWidth = 3;
      for (var i = 0; i < 4; i++){ c.beginPath(); c.moveTo(0, 0); c.lineTo(Math.cos(i * Math.PI / 2) * 28, Math.sin(i * Math.PI / 2) * 28); c.stroke(); }
      c.restore();
    }
    // 냉각탑
    var cx2 = tx + 160;
    c.fillStyle = '#E3EDF3'; c.fillRect(cx2, by + 30, 110, 80);
    c.strokeStyle = '#3A8FB7'; c.lineWidth = 2; c.strokeRect(cx2, by + 30, 110, 80);
    txt(c, '냉각탑 ' + COLD[p.c] + ' °C', cx2 + 55, by + 20, {align:'center', color:'#3A8FB7', bold:true});
    arrow(c, bx + 120, by + 55, tx - 4, by + 55, '#C8463D', 2.5);
    arrow(c, tx + 110, by + 70, cx2 - 4, by + 70, '#3A8FB7', 2.5);
    arrow(c, tx + 55, by + 10, tx + 55, by - 40, '#2E9E78', 2.5);
    txt(c, '전기 1 000 MW', tx + 55, by - 48, {align:'center', color:'#2E9E78', bold:true});
    if (!r){ txt(c, '연료가 달라도 구조는 같아요 — 물을 끓여 터빈을 돌려요.', bx, H - 18, {color:'#4A5868'}); return; }
    // 에너지 막대
    var by2 = by + 150, bwAll = Math.min(W - 80, 620);
    c.fillStyle = '#E6EBF1'; c.fillRect(bx, by2, bwAll, 34);
    var we = bwAll * r.eff * tau;
    c.fillStyle = '#2E9E78'; c.fillRect(bx, by2, we, 34);
    c.fillStyle = '#C8463D'; c.fillRect(bx + we, by2, (bwAll - we) * tau, 34);
    txt(c, '전기 ' + f(r.eff * 100, 1) + ' %', bx + 8, by2 + 23, {color:'#fff', bold:true});
    txt(c, '버려지는 열 ' + f((1 - r.eff) * 100, 1) + ' %', bx + bwAll - 8, by2 + 23, {align:'right', color:'#fff', bold:true});
    if (tau < 1) return;
    var yy = by2 + 68;
    txt(c, '카르노 최대 효율 = 1 − ' + f(r.TcK, 0) + ' ÷ ' + f(r.ThK, 0) + ' = ' + f(r.carnot * 100, 1) + ' % → 실제 ' + f(r.eff * 100, 1) + ' %',
      bx, yy, {bold:true, color:'#2B5FA3'});
    txt(c, '넣은 열 ' + Math.round(r.qin).toLocaleString() + ' MW · 전기 1 000 MW · 버린 열 ' + Math.round(r.waste).toLocaleString() + ' MW', bx, yy + 30, {});
    txt(c, r.inRange ? P.n + '의 실제 증기 온도 범위(' + P.th[0] + '~' + P.th[1] + ' °C) 안이에요.'
      : P.n + '에서는 보통 ' + P.th[0] + '~' + P.th[1] + ' °C를 써요. 지금 값은 그 범위 밖이에요.',
      bx, H - 14, {color:r.inRange ? '#4A5868' : '#A8702F'});
  },
  stats: function(p, r){
    return [['발전 방식', r.P.n], ['증기 온도', r.Th + ' °C = ' + f(r.ThK, 0) + ' K'],
      ['냉각수 온도', r.Tc + ' °C = ' + f(r.TcK, 0) + ' K'], ['T저온 ÷ T고온', f(r.ratio, 3)],
      ['카르노 최대 효율', f(r.carnot * 100, 1) + ' %', PAL[0]],
      ['실제 효율(모형)', f(r.eff * 100, 1) + ' %', PAL[1]],
      ['넣은 열', Math.round(r.qin).toLocaleString() + ' MW'],
      ['전기 출력', '1 000 MW'], ['버려지는 열', Math.round(r.waste).toLocaleString() + ' MW', PAL[4]],
      ['버려지는 몫', f(r.wasteFrac * 100, 1) + ' %'],
      ['1년 이산화 탄소(어림)', f(r.co2, 2) + ' 백만 t'], ['메모', r.P.note]];
  },
  columns: ['방식', 'T고온 (°C)', 'T저온 (°C)', 'Tc÷Th', '카르노 (%)', '실제 (%)', '넣은 열 (MW)', '폐열 (MW)'],
  record: function(p, r){
    return {pi:p.p, plant:r.P.n, Th:r.Th, Tc:r.Tc, ratio:r.ratio, carnot:r.carnot, eff:r.eff,
      qin:r.qin, waste:r.waste, co2:r.co2, k:r.P.k, co2f:r.P.co2};
  },
  row: function(d){ return [d.plant, d.Th, d.Tc, f(d.ratio, 3), f(d.carnot * 100, 1), f(d.eff * 100, 1),
    Math.round(d.qin).toLocaleString(), Math.round(d.waste).toLocaleString()]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('온도비와 최대 효율', '<canvas class="chart" id="ch1" role="img" aria-label="온도비와 카르노 효율 산점도"></canvas><ul class="readout" id="ro1"></ul><p class="ask">기울기가 −1인 직선이 나옵니다. 효율을 100 %로 만들려면 어떤 조건이 필요할까요? 그것이 가능할까요?</p>') +
      card('효율과 버려지는 열', '<canvas class="chart" id="ch2" role="img" aria-label="효율과 폐열 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">같은 1 000 MW를 내면서 폐열을 줄이려면 무엇을 바꿔야 할까요?</p>') +
      card('방식별 비교', '<div id="ro3"></div><p class="ask">효율이 높은 것과 배출이 적은 것이 늘 같지는 않습니다. 무엇을 기준으로 발전 방식을 고를지 생각해 보세요.</p>') + '</div>';
    var pts1 = rec.map(function(d){ return {x:d.ratio, y:d.carnot}; });
    drawScatter($('ch1'), {xLabel:'T저온 ÷ T고온', yLabel:'카르노 최대 효율', tightX:true, tightY:true, series:[{color:PAL[0], pts:pts1}]});
    var r1 = [];
    if (distinct(rec.map(function(d){ return d.ratio; })) >= 2){
      var L1 = linfit(pts1);
      r1.push('<li>기울기 <b>' + f(L1.k, 2) + '</b>, 절편 <b>' + f(L1.b, 2) + '</b> — 식 효율 = 1 − Tc ÷ Th와 같아요.</li>');
    } else r1.push('<li>증기 온도나 냉각수 온도를 바꿔 2개 이상 기록해 보세요.</li>');
    r1.push('<li>효율 100 %가 되려면 Tc = 0 K여야 해요. <b>불가능</b>하죠. 열기관은 반드시 일부를 버려야 해요.</li>');
    $('ro1').innerHTML = r1.join('');
    var bp = groupBy(rec, function(d){ return d.pi; }), s2 = [], r2 = [];
    Object.keys(bp).forEach(function(k){
      var g = bp[k], col = PAL[+k % PAL.length];
      s2.push({color:col, pts:g.map(function(d){ return {x:d.eff * 100, y:d.waste}; })});
      var best = g.slice().sort(function(a, b){ return b.eff - a.eff; })[0];
      r2.push('<li>' + dot(col) + g[0].plant + ': 가장 높은 효율 <b>' + f(best.eff * 100, 1) + ' %</b> (증기 ' + best.Th + ' °C, 냉각수 ' + best.Tc + ' °C) → 폐열 ' + Math.round(best.waste).toLocaleString() + ' MW</li>');
    });
    drawScatter($('ch2'), {xLabel:'실제 효율 (%)', yLabel:'버려지는 열 (MW)', tightX:true, tightY:true, series:s2});
    $('ro2').innerHTML = r2.join('') +
      '<li>효율이 오르면 폐열이 줄어요. 증기를 더 뜨겁게(재료의 한계까지), 냉각수를 더 차게 하는 것이 방법이에요.</li>' +
      '<li>버리는 열을 난방에 쓰면(열병합) 같은 효율에서도 <b>전체 이용률</b>이 올라가요.</li>';
    var rows = PLANT.map(function(P){
      var g = rec.filter(function(d){ return d.plant === P.n; });
      return [P.n, P.th[0] + '~' + P.th[1] + ' °C', f(P.k * 100, 0) + ' %', P.co2 + ' g/kWh',
        g.length ? f(mean(g.map(function(d){ return d.eff * 100; })), 1) + ' %' : '—', P.note];
    });
    $('ro3').innerHTML = tableHTML(['방식', '실제 증기 온도', '기술 계수', 'CO₂(수명 주기)', '내 기록 평균 효율', '메모'], rows, 'wrap') +
      '<p class="note">원자력은 효율이 낮지만 배출이 적고, 석탄은 효율이 비교적 높아도 배출이 가장 많아요. 태양광·풍력은 열기관이 아니라 카르노 한계를 받지 않아요.</p>';
  }
};`
},

/* ===================== 38. 인공지능과 데이터 편향 (Future Ep03) ===================== */
{
  file: '38_ai_training_bias_lab_IntegSci2_Future_Ep03.html',
  title: '흰 고양이만 본 인공지능',
  intro: '고양이와 개를 구별하는 작은 인공지능을 실제로 학습시킵니다. 학습에 쓰는 사진의 수와 그중 흰 고양이의 비율을 바꿔 가며, 시험 사진에서 얼마나 맞히는지 확인해 보세요.',
  sceneNote: '사진을 밝기와 귀의 뾰족한 정도라는 두 값으로 나타냈습니다. 시험 자료는 흰 고양이와 검은 고양이를 반반 섞어 공정하게 만듭니다.',
  runLabel: '학습시키기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 기계 학습과 데이터 편향</h3>
<p>예전 인공지능은 사람이 규칙을 하나하나 적어 주는 방식이었어요. 하지만 '고양이'를 규칙으로 적기는 어려워요. 지금의 인공지능은 <b>많은 예시를 보고 스스로 규칙을 찾아내요</b>(기계 학습). 문제는 인공지능이 <b>보여 준 자료 안에서만</b> 규칙을 찾는다는 거예요. 학습 사진의 고양이가 모두 하얗다면, 인공지능은 '고양이 = 흰색'이라는 <b>엉뚱한 단서</b>를 배우고 검은 고양이를 개라고 말해요. 인공지능의 잘못이 아니라 <b>자료의 편향</b>이 만든 결과예요.</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>이 인공지능은 <span class="fx-formula">점수 = w₁ × 밝기 + w₂ × 귀 + b</span>를 계산해 0보다 크면 고양이로 판단해요. 학습이란 w₁·w₂·b를 <b>조금씩 고치는 일</b>이에요.</li>
<li>진짜 규칙은 '귀가 뾰족하면 고양이'예요. 밝기는 아무 상관이 없어요.</li>
<li>학습 자료가 공정하면 w₂(귀)가 커지고 w₁(밝기)은 0 가까이 가요. 편향되면 반대로 w₁이 커져요.</li>
<li>자료 수를 늘리면 정확도가 오르지만, <b>빠진 집단은 자료를 늘려도 채워지지 않아요</b>. 흰 고양이만 100만 장 모아도 검은 고양이는 여전히 배우지 못해요. 양이 아니라 <b>다양성</b>이 문제예요.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p>사진마다 (밝기, 귀) 두 값을 만들고, 경사 하강법으로 가중치를 갱신합니다. 시험 자료에서 <span class="fx-formula">정확도 = 맞힌 수 ÷ 전체</span>를 흰 고양이·검은 고양이로 나눠 따로 잽니다.</p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 사진 대신 두 개의 숫자로 줄인 <b>아주 작은 모형</b>이에요. 실제 이미지 인식은 수백만 개의 가중치를 쓰는 신경망이지만, <b>자료에 있는 단서를 붙잡는다</b>는 성질은 똑같아요.<br>
· 난수를 쓰므로 같은 설정에서도 결과가 조금씩 달라요. 여러 번 기록해 평균으로 보세요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>피부색이 밝은 얼굴 사진만으로 학습한 얼굴 인식이 어두운 피부에서 훨씬 자주 틀린 일이 실제로 있었어요.</li>
<li>채용·대출 심사에 쓰이는 인공지능이 과거의 차별이 담긴 자료를 학습하면 그 차별을 그대로 되풀이해요.</li>
</ul>`,
  js: `
var NTR = [20, 50, 200, 1000];
var EPO = [5, 20, 100];
function rng(seed){ var s = seed >>> 0; return function(){ s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
function make(n, whiteFrac, rnd){
  var d = [];
  for (var i = 0; i < n; i++){
    var isCat = rnd() < 0.5;
    // 귀 모양은 겹치는 구간(0.45~0.55)이 있어 그것만으로는 완벽히 가를 수 없다
    var ear = isCat ? 0.45 + rnd() * 0.55 : rnd() * 0.55;
    var bright = isCat ? (rnd() < whiteFrac ? 0.6 + rnd() * 0.4 : rnd() * 0.4) : rnd();
    d.push({x1:bright, x2:ear, y:isCat ? 1 : 0, white:bright >= 0.5});
  }
  return d;
}
return {
  sceneHeight: 470,
  minRec: 4,
  idle: '학습 사진 수와 흰 고양이 비율, 학습 반복을 정하고 <b>학습시키기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 학습 사진 수와 흰 고양이 비율을 바꿔 가며 기록하세요.',
  params: [
    {key:'n', type:'seg', label:'학습에 쓰는 사진 수', cols:4, value:1, options:NTR.map(function(v){ return v + '장'; })},
    {key:'w', type:'range', label:'학습 사진 속 고양이가 흰 고양이일 비율', min:50, max:100, step:5, value:50, fmt:function(v){ return v + ' %'; }},
    {key:'e', type:'seg', label:'학습 반복 횟수', cols:3, value:1, options:EPO.map(function(v){ return v + '회'; }),
      note:'시험 자료 400장은 흰 고양이와 검은 고양이를 반반 섞은 <b>고정된 자료</b>라, 조건을 바꿔도 같은 문제로 채점합니다. 귀 모양은 0.45~0.55 구간이 겹쳐 그것만으로는 완벽히 가를 수 없습니다.'}
  ],
  compute: function(p){
    var n = NTR[p.n], wf = p.w / 100, ep = EPO[p.e];
    var rnd = rng(Math.floor(Math.random() * 1e9));
    // 시험 자료는 조건을 바꿔도 늘 같은 400장(고정 씨앗) — 결과 차이가 학습 조건 때문임을 보장
    var tr = make(n, wf, rnd), te = make(400, 0.5, rng(20260922));
    var w1 = 0, w2 = 0, b = 0, lr = 0.5;
    for (var e = 0; e < ep; e++){
      for (var i = 0; i < tr.length; i++){
        var d = tr[i], z = w1 * d.x1 + w2 * d.x2 + b;
        var pr = 1 / (1 + Math.exp(-z)), g = (pr - d.y);
        w1 -= lr * g * d.x1; w2 -= lr * g * d.x2; b -= lr * g;
      }
    }
    var ok = 0, cw = 0, cwN = 0, cb = 0, cbN = 0, dg = 0, dgN = 0;
    te.forEach(function(d){
      var hit = ((w1 * d.x1 + w2 * d.x2 + b) > 0 ? 1 : 0) === d.y;
      if (hit) ok++;
      if (d.y === 1){ if (d.white){ cwN++; if (hit) cw++; } else { cbN++; if (hit) cb++; } }
      else { dgN++; if (hit) dg++; }
    });
    var tot = Math.abs(w1) + Math.abs(w2) || 1;
    return {n:n, wf:wf, ep:ep, w1:w1, w2:w2, b:b, tr:tr,
      acc:ok / te.length * 100, accW:cwN ? cw / cwN * 100 : 0, accB:cbN ? cb / cbN * 100 : 0,
      accD:dgN ? dg / dgN * 100 : 0, share2:Math.abs(w2) / tot * 100, gap:(cwN ? cw / cwN * 100 : 0) - (cbN ? cb / cbN * 100 : 0)};
  },
  draw: function(c, W, H, p, r, tau){
    var padL = 80, top = 74, size = Math.min(250, W - 320, H - 180);
    var X = function(v){ return padL + v * size; }, Y = function(v){ return top + size - v * size; };
    c.fillStyle = '#F7F9FC'; c.fillRect(padL, top, size, size);
    c.strokeStyle = '#8C99A8'; c.lineWidth = 1.5; c.strokeRect(padL, top, size, size);
    txt(c, '밝기 →', padL + size / 2, top + size + 26, {align:'center', color:'#4A5868'});
    c.save(); c.translate(padL - 26, top + size / 2); c.rotate(-Math.PI / 2);
    txt(c, '귀의 뾰족함 →', 0, 0, {align:'center', color:'#4A5868'}); c.restore();
    if (r){
      var show = Math.round(r.tr.length * Math.min(tau * 1.4, 1));
      for (var i = 0; i < show; i++){
        var d = r.tr[i];
        c.fillStyle = d.y ? 'rgba(43,95,163,.75)' : 'rgba(200,70,61,.75)';
        c.beginPath(); c.arc(X(d.x1), Y(d.x2), 3.6, 0, Math.PI * 2); c.fill();
      }
      // 학습한 경계선
      if (tau > 0.6 && Math.abs(r.w2) > 1e-6){
        c.strokeStyle = '#2E9E78'; c.lineWidth = 2.5; c.beginPath();
        var y0 = -(r.w1 * 0 + r.b) / r.w2, y1 = -(r.w1 * 1 + r.b) / r.w2;
        c.moveTo(X(0), Y(Math.max(-0.2, Math.min(1.2, y0)))); c.lineTo(X(1), Y(Math.max(-0.2, Math.min(1.2, y1)))); c.stroke();
        txt(c, '학습한 기준선', X(0.5), Y(1.08), {align:'center', color:'#2E9E78', bold:true});
      }
    }
    var lx = padL + size + 40;
    c.fillStyle = 'rgba(43,95,163,.75)'; c.beginPath(); c.arc(lx + 6, top + 8, 6, 0, Math.PI * 2); c.fill();
    txt(c, '고양이', lx + 20, top + 14, {color:'#4A5868'});
    c.fillStyle = 'rgba(200,70,61,.75)'; c.beginPath(); c.arc(lx + 6, top + 34, 6, 0, Math.PI * 2); c.fill();
    txt(c, '개', lx + 20, top + 40, {color:'#4A5868'});
    if (!r){ txt(c, '학습 사진을 뿌리고 기준선을 찾아요.', padL, H - 18, {color:'#4A5868'}); return; }
    if (lx < W - 200){
      txt(c, '전체 정확도', lx, top + 84, {color:'#4A5868'});
      meter(c, lx, top + 94, Math.min(190, W - lx - 12), f(r.acc * tau, 1) + ' %');
      txt(c, '검은 고양이 정확도', lx, top + 156, {color:'#4A5868'});
      meter(c, lx, top + 166, Math.min(190, W - lx - 12), f(r.accB * tau, 1) + ' %');
    }
    if (tau < 1) return;
    var yy = top + size + 58;
    txt(c, '학습한 규칙: 점수 = ' + f(r.w1, 2) + ' × 밝기 + ' + f(r.w2, 2) + ' × 귀 + ' + f(r.b, 2), padL - 40, yy, {bold:true, color:'#2B5FA3'});
    txt(c, '흰 고양이 ' + f(r.accW, 1) + ' % · 검은 고양이 ' + f(r.accB, 1) + ' % · 개 ' + f(r.accD, 1) + ' %', padL - 40, yy + 30,
      {bold:true, color:r.gap > 20 ? '#C8463D' : '#2E9E78'});
    txt(c, r.gap > 20 ? '흰 고양이만 잘 맞히고 검은 고양이는 자주 틀려요 — 밝기를 단서로 잘못 배웠어요.'
      : '두 종류를 비슷하게 맞혀요 — 귀를 단서로 제대로 배웠어요.', padL - 40, H - 14, {color:'#4A5868'});
  },
  stats: function(p, r){
    return [['학습 사진 수', r.n + '장'], ['흰 고양이 비율', f(r.wf * 100, 0) + ' %'], ['학습 반복', r.ep + '회'],
      ['밝기의 가중치 w₁', f(r.w1, 2), PAL[4]], ['귀의 가중치 w₂', f(r.w2, 2), PAL[1]],
      ['귀가 차지하는 몫', f(r.share2, 1) + ' %'],
      ['전체 정확도', f(r.acc, 1) + ' %', PAL[0]],
      ['흰 고양이 정확도', f(r.accW, 1) + ' %'], ['검은 고양이 정확도', f(r.accB, 1) + ' %', PAL[4]],
      ['개 정확도', f(r.accD, 1) + ' %'],
      ['흰 − 검은 차이', sgn(r.gap, 1) + ' %p', r.gap > 20 ? PAL[4] : PAL[1]]];
  },
  columns: ['사진 수', '흰 비율 (%)', '반복', 'w₁(밝기)', 'w₂(귀)', '전체 (%)', '흰 고양이 (%)', '검은 고양이 (%)', '차이 (%p)'],
  record: function(p, r){
    return {n:r.n, wf:r.wf * 100, ep:r.ep, w1:r.w1, w2:r.w2, acc:r.acc, accW:r.accW, accB:r.accB, gap:r.gap, share2:r.share2};
  },
  row: function(d){ return [d.n, f(d.wf, 0), d.ep, f(d.w1, 2), f(d.w2, 2), f(d.acc, 1), f(d.accW, 1), f(d.accB, 1), sgn(d.gap, 1)]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('자료가 많으면 똑똑해질까', '<canvas class="chart" id="ch1" role="img" aria-label="학습 사진 수와 전체 정확도 산점도"></canvas><ul class="readout" id="ro1"></ul><p class="ask">공정한 자료와 편향된 자료를 나눠 보세요. 자료를 늘리는 것만으로 해결되나요?</p>') +
      card('편향이 만드는 차별', '<canvas class="chart" id="ch2" role="img" aria-label="흰 고양이 비율과 검은 고양이 정확도 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">전체 정확도는 높은데 특정 집단에서만 크게 틀릴 수 있습니다. 왜 전체 정확도만 보면 안 될까요?</p>') +
      card('무엇을 단서로 배웠나', '<div id="ro3"></div><p class="ask">인공지능이 “틀렸다”기보다 “자료가 가르친 대로 배웠다”고 말하는 편이 정확합니다. 그렇다면 책임은 누구에게 있을까요?</p>') + '</div>';
    var fair = rec.filter(function(d){ return d.wf <= 60; }), bias = rec.filter(function(d){ return d.wf > 60; });
    drawScatter($('ch1'), {xLabel:'학습 사진 수 (장)', yLabel:'전체 정확도 (%)',
      series:[{color:PAL[1], pts:fair.map(function(d){ return {x:d.n, y:d.acc}; })},
              {color:PAL[4], pts:bias.map(function(d){ return {x:d.n, y:d.acc}; })}]});
    $('ro1').innerHTML = '<li>' + dot(PAL[1]) + '공정한 자료(흰 비율 60 % 이하) ' + fair.length + '개' +
      (fair.length ? ', 평균 정확도 <b>' + f(mean(fair.map(function(d){ return d.acc; })), 1) + ' %</b>' : '') + '</li>' +
      '<li>' + dot(PAL[4]) + '편향된 자료(흰 비율 65 % 이상) ' + bias.length + '개' +
      (bias.length ? ', 평균 정확도 <b>' + f(mean(bias.map(function(d){ return d.acc; })), 1) + ' %</b>' : '') + '</li>' +
      (function(){
        if (!fair.length || !bias.length) return '<li>공정한 자료와 편향된 자료를 모두 기록하면 두 경우를 견줄 수 있어요.</li>';
        var mf = mean(fair.map(function(d){ return d.acc; })), mb = mean(bias.map(function(d){ return d.acc; }));
        var d0 = mf - mb;
        return '<li>내 기록에서는 공정한 자료가 편향된 자료보다 전체 정확도가 <b>' + f(Math.abs(d0), 1) + ' %p ' + (d0 >= 0 ? '높' : '낮') + '게</b> 나왔어요.' +
          (Math.abs(d0) < 2 ? ' 차이가 작다면 <b>전체 정확도만으로는 편향이 잘 드러나지 않는다</b>는 뜻이니, 옆 그래프에서 집단별로 나눠 보세요.' : '') + '</li>';
      })();
    drawScatter($('ch2'), {xLabel:'학습 자료의 흰 고양이 비율 (%)', yLabel:'정확도 (%)', tightX:true,
      series:[{color:PAL[0], pts:rec.map(function(d){ return {x:d.wf, y:d.accW}; })},
              {color:PAL[4], pts:rec.map(function(d){ return {x:d.wf, y:d.accB}; })}]});
    var hi = rec.filter(function(d){ return d.wf >= 90; });
    $('ro2').innerHTML = '<li>' + dot(PAL[0]) + '흰 고양이 정확도 · ' + dot(PAL[4]) + '검은 고양이 정확도</li>' +
      (hi.length ? '<li>흰 비율 90 % 이상인 기록 ' + hi.length + '개: 흰 고양이 <b>' + f(mean(hi.map(function(d){ return d.accW; })), 1) +
        ' %</b> vs 검은 고양이 <b>' + f(mean(hi.map(function(d){ return d.accB; })), 1) + ' %</b></li>'
        : '<li>흰 고양이 비율을 90~100 %로 올려 기록해 보세요.</li>') +
      '<li>전체 정확도는 <b>수가 많은 쪽</b>에 끌려가요. 그래서 집단을 나눠 따로 재야 숨은 차별이 보여요.</li>';
    var bw = groupBy(rec, function(d){ return d.wf >= 90 ? '90~100 %' : d.wf >= 70 ? '70~85 %' : '50~65 %'; }), rows = [];
    ['50~65 %', '70~85 %', '90~100 %'].forEach(function(k){
      var g = bw[k];
      if (!g){ rows.push([k, '0개', '—', '—', '—']); return; }
      rows.push([k, g.length + '개', f(mean(g.map(function(d){ return d.w1; })), 2), f(mean(g.map(function(d){ return d.w2; })), 2),
        f(mean(g.map(function(d){ return d.share2; })), 0) + ' %']);
    });
    $('ro3').innerHTML = tableHTML(['학습 자료의 흰 비율', '기록 수', '평균 w₁(밝기)', '평균 w₂(귀)', '귀가 차지하는 몫'], rows) +
      '<p class="note">진짜 규칙은 <b>귀</b>인데, 흰 고양이만 보여 주면 w₁(밝기)이 커져요. 자료를 고르고 확인하는 사람의 책임이 그만큼 커요.</p>';
  }
};`
},

/* ===================== 39. 유전자 가위의 정확도 (Future Ep04) ===================== */
{
  file: '39_gene_scissors_offtarget_lab_IntegSci2_Future_Ep04.html',
  title: '유전자 가위는 얼마나 정확할까',
  intro: '유전자 가위가 찾아갈 표적 서열의 길이와 허용할 불일치 수를 바꿔 가며, 유전체 안에서 잘못 잘릴 만한 자리가 몇 군데나 되는지 계산합니다. 길게 정할수록, 까다롭게 볼수록 어떻게 달라지는지 확인해 보세요.',
  sceneNote: '염기 4종이 무작위로 늘어서 있다고 보고 기댓값을 계산한 교육용 모형입니다. 실제 유전체는 반복 서열이 많아 이 값과 달라집니다.',
  runLabel: '유전체 훑어보기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 표적 서열의 길이가 정확도를 정한다</h3>
<p>유전자 가위(CRISPR)는 <b>안내 RNA</b>가 짝을 이루는 서열을 찾아가 그 자리에서 DNA를 자르는 도구예요. 그런데 유전체는 아주 길어서, 표적과 <b>비슷한</b> 서열이 우연히 다른 곳에도 있을 수 있어요. 그런 자리를 <b>비표적(off-target)</b>이라고 해요. 표적 서열을 길게 잡을수록 우연히 같을 확률이 4분의 1씩 줄어들지만, 몇 개쯤 다른 것까지 눈감아 주면 후보가 급격히 늘어요. 그래서 이 기술의 안전성은 <b>계산할 수 있는 문제</b>이면서 동시에 <b>어디까지 허용할지</b>를 사람이 정해야 하는 문제예요.</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>길이 L인 서열이 우연히 똑같을 확률은 <span class="fx-formula">1 ÷ 4<sup>L</sup></span>예요. L = 20이면 약 1조 분의 1이에요.</li>
<li>사람 유전체는 약 31억 염기쌍, 양쪽 가닥을 세면 62억 자리를 볼 수 있어요. 20염기면 우연히 걸리는 자리의 <b>기대 개수가 1보다 작아요</b> — 비표적이 반드시 없다는 뜻이 아니라, 같은 조건을 아주 여러 번 되풀이했을 때의 <b>평균</b>이 1보다 작다는 뜻이에요.</li>
<li>불일치 k개까지 봐주면 후보 서열이 <span class="fx-formula">C(L,k) × 3<sup>k</sup></span>가지로 늘어요. L = 20, k = 3이면 30 780가지예요.</li>
<li>기대 개수 = <span class="fx-formula">2N × Σ C(L,i)·3<sup>i</sup> ÷ 4<sup>L</sup></span>. 길이는 지수로 줄이고, 불일치 허용은 지수로 늘려요.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p>표적 길이 L, 허용 불일치 k, 유전체 크기 N으로 <span class="fx-formula">기대 자리 수 = 2N × Σ<sub>i=0..k</sub> C(L,i)·3<sup>i</sup> ÷ 4<sup>L</sup></span>을 구하고, 표적 1곳을 뺀 나머지를 비표적으로 셉니다.</p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 염기가 <b>무작위로</b> 늘어서 있다고 봤어요. 실제 유전체에는 반복 서열과 유전자군이 있어 특정 서열이 훨씬 자주 나와요.<br>
· 실제로는 불일치의 <b>위치</b>도 중요해요(자르는 자리 가까이의 불일치가 훨씬 치명적). 또 PAM 서열 조건이 있어 후보가 더 줄어요.<br>· 표적을 실제로 얼마나 잘 자르는지(절단 효율)는 안내 RNA 설계·PAM·염색질 접근성·효소 종류·세포 조건이 정해요. <b>비표적을 어디까지 셀지 정한 기준(허용 불일치 수)과는 별개</b>라, 이 실험에서는 절단 효율을 다루지 않아요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>유전자 가위로 겸상 적혈구 빈혈을 치료하는 방법이 실제로 승인됐어요. 치료 전에 비표적 절단을 유전체 전체에서 확인해요.</li>
<li>2018년 유전자를 편집한 아기가 태어난 일이 세계적 문제가 됐어요. 기술의 정확도와 별개로 <b>무엇을 해도 되는가</b>는 사회가 정해야 해요.</li>
</ul>`,
  js: `
var LEN = [12, 16, 20, 24];
var MIS = [0, 1, 2, 3];
var GEN = [{n:'대장균', N:4.6e6}, {n:'초파리', N:1.4e8}, {n:'사람', N:3.1e9}];
function comb(n, k){ var r = 1; for (var i = 0; i < k; i++) r = r * (n - i) / (i + 1); return r; }
return {
  sceneHeight: 460,
  minRec: 4,
  idle: '표적 길이와 허용 불일치 수, 유전체를 정하고 <b>유전체 훑어보기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 표적 길이와 허용 불일치 수를 바꿔 가며 기록하세요.',
  params: [
    {key:'l', type:'seg', label:'표적 서열의 길이', cols:4, value:2, options:LEN.map(function(v){ return v + '염기'; })},
    {key:'k', type:'seg', label:'눈감아 주는 불일치 수', cols:4, value:0, options:MIS.map(function(v){ return v + '개'; })},
    {key:'g', type:'seg', label:'대상 유전체', cols:3, value:2, options:GEN.map(function(x){ return x.n + '<small>' + (x.N / 1e6).toLocaleString() + ' Mb</small>'; }),
      note:'염기 4종이 무작위로 늘어서 있다고 보고 기대 개수를 셉니다. 표적 1곳은 원래 자르려던 자리입니다.'}
  ],
  compute: function(p){
    var L = LEN[p.l], k = MIS[p.k], G = GEN[p.g];
    var ways = 0;
    for (var i = 0; i <= k; i++) ways += comb(L, i) * Math.pow(3, i);
    var prob = ways / Math.pow(4, L);
    // 의도한 표적 1곳은 이미 정해져 있고, 나머지 후보 자리에서 우연히 걸리는 것이 비표적이다
    var off = (2 * G.N - 1) * prob;
    var hits = 1 + off;                       // 표적 1곳 + 비표적 기대 개수
    return {L:L, k:k, G:G, ways:ways, prob:prob, hits:hits, off:off,
      prec:1 / hits * 100, single:1 / Math.pow(4, L), logOff:Math.log10(Math.max(off, 1e-12))};
  },
  draw: function(c, W, H, p, r, tau){
    var padL = 40, top = 96, bw = Math.min(W - 80, 640), bh = 34;
    var BASE = ['A', 'T', 'G', 'C'], COL = {A:'#2E9E78', T:'#C8463D', G:'#2B5FA3', C:'#D98E04'};
    txt(c, '유전체를 훑으며 표적과 비슷한 자리를 찾는 중', padL, 56, {bold:true, color:'#4A5868'});
    // 표적 서열
    var n = LEN[p.l], cw = Math.min(26, bw / (n + 2));
    for (var i = 0; i < n; i++){
      var b = BASE[(i * 7 + 3) % 4];
      c.fillStyle = COL[b]; c.fillRect(padL + i * cw, top, cw - 2, bh);
      txt(c, b, padL + i * cw + (cw - 2) / 2, top + 24, {align:'center', color:'#fff', bold:true});
    }
    txt(c, '표적 서열 ' + n + '염기', padL, top - 10, {color:'#2B5FA3'});
    // 훑는 자리
    var sy = top + 70;
    txt(c, '유전체에서 찾은 비슷한 자리 — ' + (MIS[p.k] === 0 ? '완전 일치만 인정' : '불일치 ' + MIS[p.k] + '개까지 눈감음'), padL, sy - 10, {color:'#4A5868'});
    var rows = 4;
    for (var rI = 0; rI < rows; rI++){
      for (var j = 0; j < n; j++){
        var mm = ((j * (rI + 3) + rI * 5) % 11) < MIS[p.k] ? true : false;
        var b2 = BASE[(j * 7 + 3 + (mm ? 1 : 0)) % 4];
        var vis = r ? (tau * rows > rI) : true;
        c.globalAlpha = vis ? 1 : 0.15;
        c.fillStyle = mm ? '#B9C2CC' : COL[b2];
        c.fillRect(padL + j * cw, sy + rI * (bh - 6), cw - 2, bh - 10);
        txt(c, b2, padL + j * cw + (cw - 2) / 2, sy + rI * (bh - 6) + 18, {align:'center', color:'#fff', bold:true});
        c.globalAlpha = 1;
      }
    }
    if (!r){ txt(c, '회색 칸이 표적과 다른 염기예요.', padL, H - 18, {color:'#4A5868'}); return; }
    if (tau < 1) return;
    var yy = sy + rows * (bh - 6) + 42;
    txt(c, '우연히 맞을 확률 ' + r.prob.toExponential(2) + ' · 후보 서열 ' + Math.round(r.ways).toLocaleString() + '가지', padL, yy, {});
    txt(c, r.G.n + ' 유전체(' + (r.G.N / 1e6).toLocaleString() + ' Mb)에서 잘릴 만한 자리 ' +
      (r.hits >= 1000 ? r.hits.toExponential(2) : f(r.hits, 2)) + '곳(기대) = 표적 1곳 + 비표적 ' +
      (r.off >= 1000 ? r.off.toExponential(2) : (r.off < 0.01 ? r.off.toExponential(2) : f(r.off, 3))) + '곳', padL, yy + 32,
      {bold:true, color:r.off > 1 ? '#C8463D' : '#2E9E78'});
    txt(c, '표적 1곳 중 제대로 맞힌 비율(정밀도) ' + f(r.prec, 1) + ' % · 무작위 서열·PAM 제외 모형', padL, H - 14, {color:'#4A5868'});
  },
  stats: function(p, r){
    return [['표적 길이 L', r.L + '염기'], ['허용 불일치 k', r.k + '개'], ['대상 유전체', r.G.n + ' (' + (r.G.N / 1e6).toLocaleString() + ' Mb)'],
      ['완전 일치 확률 1÷4^L', r.single.toExponential(2)],
      ['후보 서열 가짓수', Math.round(r.ways).toLocaleString() + '가지', PAL[6]],
      ['한 자리가 맞을 확률', r.prob.toExponential(3), PAL[0]],
      ['잘릴 만한 자리 (기대 개수)', (r.hits >= 1000 ? r.hits.toExponential(3) : f(r.hits, 3)) + '곳 (표적 1 + 비표적)'],
      ['비표적 자리(기대)', (r.off >= 1000 ? r.off.toExponential(3) : f(r.off, 3)) + '곳', PAL[4]],
      ['정밀도 = 표적 ÷ 전체', f(r.prec, 2) + ' %']];
  },
  columns: ['길이 L', '불일치 k', '유전체', '후보 가짓수', '맞을 확률', '비표적 (기대 개수)', '정밀도 (%)'],
  record: function(p, r){
    return {L:r.L, k:r.k, gn:r.G.n, N:r.G.N, ways:r.ways, prob:r.prob, hits:r.hits, off:r.off, prec:r.prec};
  },
  row: function(d){ return [d.L, d.k, d.gn, Math.round(d.ways).toLocaleString(), d.prob.toExponential(2),
    d.off >= 1000 ? d.off.toExponential(2) : (d.off < 0.01 ? d.off.toExponential(2) : f(d.off, 3)), f(d.prec, 2)]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('길게 정할수록 안전해진다', '<canvas class="chart" id="ch1" role="img" aria-label="표적 길이와 비표적 수 로그값 산점도"></canvas><ul class="readout" id="ro1"></ul><p class="ask">염기 하나를 더 붙일 때마다 후보가 몇 분의 1이 될까요? 기울기와 연결해 설명해 보세요.</p>') +
      card('눈감아 주면 급격히 늘어난다', '<canvas class="chart" id="ch2" role="img" aria-label="허용 불일치 수와 비표적 수 로그값 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">표적을 잘 자르는 것과 엉뚱한 곳을 안 자르는 것은 서로 부딪힙니다. 어디서 타협해야 할까요?</p>') +
      card('정답이 없는 문제', '<div id="ro3"></div><p class="ask">계산으로 정할 수 있는 것과, 사회가 합의해야 하는 것을 나눠 적어 보세요. 치료와 능력 향상의 경계는 어디일까요?</p>') + '</div>';
    var bk = groupBy(rec.filter(function(d){ return d.gn === rec[rec.length - 1].gn; }), function(d){ return d.k; });
    var s1 = [], r1 = [], ci = 0;
    Object.keys(bk).sort(function(a, b){ return a - b; }).forEach(function(k){
      var g = bk[k], col = PAL[ci++ % PAL.length];
      s1.push({color:col, pts:g.map(function(d){ return {x:d.L, y:Math.log10(Math.max(d.off, 1e-8))}; })});
      if (distinct(g.map(function(d){ return d.L; })) >= 2){
        var L1 = linfit(g.map(function(d){ return {x:d.L, y:Math.log10(Math.max(d.off, 1e-8))}; }));
        r1.push('<li>' + dot(col) + '불일치 ' + k + '개 허용: 기울기 <b>' + f(L1.k, 2) + '</b> — 염기 1개마다 약 ' + f(Math.pow(10, -L1.k), 1) + '분의 1이 돼요.</li>');
      }
    });
    drawScatter($('ch1'), {xLabel:'표적 서열의 길이 (염기)', yLabel:'log₁₀(비표적 자리 수)', tightX:true, tightY:true,
      series:s1.length ? s1 : [{color:PAL[0], pts:[]}]});
    $('ro1').innerHTML = (r1.length ? r1.join('') : '<li>같은 불일치 조건에서 길이를 2가지 이상 바꿔 기록해 보세요.</li>') +
      '<li><b>완전 일치만</b> 인정할 때(불일치 0개) 염기를 하나 더 보면 경우의 수가 4배가 되어 우연히 맞을 자리가 정확히 <b>4분의 1</b>이 돼요(log 기울기 −0.60). 불일치를 허용하면 허용되는 서열 수도 함께 늘어 감소 폭이 <b>그보다 작아져요</b> — 위에 계산된 기울기로 확인해 보세요.</li>' +
      '<li>실제로 20염기를 쓰는 까닭이 여기 있어요 — 사람 유전체(31억)보다 4²⁰(약 1조)이 훨씬 크기 때문이에요.</li>';
    var bl = groupBy(rec, function(d){ return d.L + '-' + d.gn; }), s2 = [], r2 = [], ci2 = 0;
    Object.keys(bl).forEach(function(k){
      var g = bl[k];
      if (distinct(g.map(function(d){ return d.k; })) < 2) return;
      var col = PAL[ci2++ % PAL.length];
      s2.push({color:col, pts:g.map(function(d){ return {x:d.k, y:Math.log10(Math.max(d.off, 1e-8))}; })});
      var srt = g.slice().sort(function(a, b){ return a.k - b.k; });
      r2.push('<li>' + dot(col) + g[0].L + '염기 · ' + g[0].gn + ': 불일치 ' + srt[0].k + '개 → ' +
        (srt[0].off >= 1000 ? srt[0].off.toExponential(1) : f(srt[0].off, 2)) + '곳, ' +
        srt[srt.length-1].k + '개 → ' + (srt[srt.length-1].off >= 1000 ? srt[srt.length-1].off.toExponential(1) : f(srt[srt.length-1].off, 2)) + '곳</li>');
    });
    drawScatter($('ch2'), {xLabel:'눈감아 주는 불일치 수 (개)', yLabel:'log₁₀(비표적 자리 수)', tightX:true, tightY:true,
      series:s2.length ? s2 : [{color:PAL[4], pts:rec.map(function(d){ return {x:d.k, y:Math.log10(Math.max(d.off, 1e-8))}; })}]});
    $('ro2').innerHTML = (r2.length ? r2.join('') : '<li>같은 길이에서 허용 불일치 수를 2가지 이상 바꿔 기록해 보세요.</li>') +
      '<li>불일치를 눈감아 줄수록 <b>비표적으로 세어야 할 후보가 급격히 늘어요</b>. 반대로 까다롭게 보면 후보는 줄지만, 실제 세포에서 그 자리들이 정말 안 잘리는지는 <b>실험으로 확인해야</b> 알 수 있어요.</li>' +
      '<li>치료에서는 예측되는 비표적 후보를 <b>최대한 줄이고</b> 실제 세포에서 여러 방법으로 확인해요. 다만 모든 검사에는 검출 한계가 있어서, 찾지 못했다고 위험이 <b>0이라고 단정할 수는 없어요</b>.</li>';
    var best = rec.slice().sort(function(a, b){ return a.off - b.off; })[0];
    var rows = [
      ['계산으로 정할 수 있는 것', '표적 길이, 허용 불일치, 비표적 기대 개수'],
      ['실험으로 확인해야 하는 것', '실제 세포에서 어디가 잘렸는지, 반복 서열의 영향, 오래 뒤의 부작용'],
      ['사회가 합의해야 하는 것', '어떤 질병까지 고칠지, 자손에게 물려주는 편집을 허용할지, 비용을 누가 낼지'],
      ['내 기록 중 가장 안전했던 조건', best.L + '염기 · 불일치 ' + best.k + '개 · ' + best.gn + ' → 비표적 ' +
        (best.off >= 1000 ? best.off.toExponential(1) : f(best.off, 2)) + '곳(기대 개수)']
    ];
    $('ro3').innerHTML = tableHTML(['구분', '내용'], rows, 'wrap') +
      '<p class="note">숫자가 답을 다 주지는 않아요. 다만 숫자가 있어야 <b>무엇을 두고 다투는지</b>가 분명해져요. 과학 기술 쟁점을 토론할 때 근거와 가치를 나눠 말하는 연습을 해 보세요.</p>';
  }
};`
}

  ]
};
