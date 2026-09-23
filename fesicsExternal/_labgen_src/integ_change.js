// 고1 통합과학2 — Ⅰ. 변화와 다양성 (1·2·4·5·6화) 실험 정의
module.exports = {
  folder: 'high1Integ',
  suffix: '고1 통합과학',
  principle: '과학 원리',
  anim: 1800,
  labs: [

/* ===================== 29. 표준 화석으로 연대 좁히기 (Change Ep01) ===================== */
{
  file: '29_index_fossil_dating_lab_IntegSci2_Change_Ep01.html',
  title: '화석으로 지층의 나이 좁히기',
  intro: '한 지층에서 나온 화석을 하나씩 감정할 때마다 지층이 쌓인 시기의 후보가 좁아집니다. 살았던 기간이 짧은 화석부터 볼 때와 긴 화석부터 볼 때, 어느 쪽이 더 빨리 좁혀지는지 비교해 보세요.',
  sceneNote: '가로줄은 각 화석이 지구에 살았던 기간(단위: 백만 년 전)입니다. 여러 화석이 함께 나오면 그 기간이 모두 겹치는 구간에 지층이 쌓인 것입니다.',
  runLabel: '화석 감정하기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 표준 화석과 지층 대비</h3>
<p>지층은 아래에서 위로 쌓이므로(<b>지층 누중의 법칙</b>) 아래층이 더 오래됐어요. 하지만 그것만으로는 <b>언제</b> 쌓였는지 알 수 없어요. 이때 쓰는 것이 <b>표준 화석</b>이에요. 표준 화석은 <b>짧은 기간만 살았고</b> 넓은 지역에 <b>많이</b> 분포한 생물의 화석이라, 그 화석이 나오면 지층이 쌓인 시기를 좁게 정할 수 있어요. 반대로 <b>시상 화석</b>은 오래 살았지만 특정 환경에서만 살아 <b>당시 환경</b>을 알려 줘요.</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>화석 A가 521~252 Ma, 화석 B가 359~252 Ma에 살았다면 둘이 함께 나온 지층은 <b>359~252 Ma</b> 사이예요.</li>
<li>화석이 늘어날수록 후보 구간은 <b>겹치는 부분</b>만 남아 점점 좁아져요. 절대로 넓어지지 않아요.</li>
<li>생존 기간이 5 Ma인 화석 하나가, 생존 기간이 300 Ma인 화석 열 개보다 훨씬 강력해요.</li>
<li>삼엽충(고생대)·암모나이트(중생대)·화폐석(신생대)이 대표적인 표준 화석이에요.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p>고른 화석들의 생존 구간을 모두 겹칩니다. <span class="fx-formula">추정 구간 = [가장 늦은 시작, 가장 이른 끝]</span>, <span class="fx-formula">구간의 폭 = 시작 − 끝 (Ma)</span></p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 화석의 생존 구간을 딱 떨어지는 숫자로 두었어요. 실제 화석 기록은 처음과 마지막 발견 시점이 계속 갱신되고, 오차 범위가 있어요.<br>
· 실제 연대 결정은 화석만이 아니라 <b>방사성 동위 원소 연대 측정</b>, 지층의 구조, 고지자기 자료를 함께 써요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>석유 탐사에서는 아주 작은 미화석(유공충 등)으로 시추한 지층의 시기를 맞춰 멀리 떨어진 시추공끼리 대비해요.</li>
<li>히말라야 산꼭대기에서 바다 생물 화석이 나오는 것은, 그 지층이 바다였던 시기와 그 뒤 솟아오른 과정을 함께 알려 줘요.</li>
</ul>`,
  js: `
var LAYER = [
  {n:'① 회색 셰일층', age:'고생대 캄브리아기', fs:[
    {n:'삼엽충', lo:521, hi:252, k:'표준 화석'},
    {n:'완족류', lo:541, hi:0, k:'오래 산 무리'},
    {n:'고배류', lo:530, hi:510, k:'표준 화석'}]},
  {n:'② 검은 석탄층', age:'고생대 석탄기', fs:[
    {n:'방추충', lo:359, hi:252, k:'표준 화석'},
    {n:'인목(양치식물)', lo:383, hi:299, k:'표준 화석'},
    {n:'속새류', lo:383, hi:0, k:'오래 산 무리'}]},
  {n:'③ 흰 석회암층', age:'중생대 백악기', fs:[
    {n:'암모나이트', lo:201, hi:66, k:'표준 화석'},
    {n:'공룡 뼈', lo:252, hi:66, k:'표준 화석'},
    {n:'은행나무', lo:270, hi:0, k:'오래 산 무리'}]},
  {n:'④ 노란 사암층', age:'신생대 팔레오기', fs:[
    {n:'화폐석', lo:56, hi:34, k:'표준 화석'},
    {n:'말 조상(에오히푸스)', lo:56, hi:45, k:'표준 화석'},
    {n:'참나무', lo:66, hi:0, k:'오래 산 무리'}]}
];
var ORD = [{n:'짧게 산 화석부터', desc:true}, {n:'오래 산 화석부터', desc:false}];
var NF = [1, 2, 3];
function width(x){ return x.lo - x.hi; }
return {
  sceneHeight: 470,
  minRec: 4,
  idle: '지층과 감정할 화석 수, 고르는 순서를 정하고 <b>화석 감정하기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 화석 수와 고르는 순서를 바꿔 가며 기록하세요.',
  params: [
    {key:'L', type:'seg', label:'조사할 지층', cols:2, value:0, options:LAYER.map(function(x){ return x.n + '<small>화석 3종 발견</small>'; })},
    {key:'n', type:'seg', label:'감정한 화석 수', cols:3, value:1, options:NF.map(function(v){ return v + '종'; })},
    {key:'o', type:'seg', label:'고르는 순서', cols:2, value:0, options:ORD.map(function(x){ return x.n; }),
      note:'Ma는 백만 년 전입니다. 화석이 살았던 기간이 모두 겹치는 구간이 지층이 쌓인 시기입니다.'}
  ],
  compute: function(p){
    var L = LAYER[p.L], n = NF[p.n], desc = ORD[p.o].desc;
    var sorted = L.fs.slice().sort(function(a, b){ return desc ? width(a) - width(b) : width(b) - width(a); });
    var use = sorted.slice(0, n);
    var lo = Math.min.apply(null, use.map(function(x){ return x.lo; }));
    var hi = Math.max.apply(null, use.map(function(x){ return x.hi; }));
    return {L:L, n:n, ord:ORD[p.o], use:use, all:sorted, lo:lo, hi:hi, span:lo - hi,
      narrow:use.filter(function(x){ return x.k === '표준 화석'; }).length};
  },
  draw: function(c, W, H, p, r, tau){
    var L = LAYER[p.L];
    var padL = 150, padR = 40, top = 96;
    var maxLo = 560, X = function(v){ return padL + (maxLo - v) / maxLo * (W - padL - padR); };
    txt(c, L.n + ' 에서 나온 화석', 20, 40, {bold:true});
    txt(c, '← 오래된 쪽 (Ma)', padL, 68, {color:'#4A5868'});
    txt(c, '현재 →', W - padR, 68, {align:'right', color:'#4A5868'});
    for (var t = 0; t <= 500; t += 100){
      seg(c, X(t), top - 10, X(t), top + 3 * 44 + 16, '#E3E8EE', 1);
      txt(c, String(t), X(t), top - 16, {align:'center', color:'#8C99A8'});
    }
    var list = r ? r.all : L.fs;
    var used = r ? Math.max(1, Math.round(r.n * Math.min(tau / 0.8, 1))) : 0;
    list.forEach(function(fo, i){
      var y = top + i * 44;
      var on = i < used;
      txt(c, fo.n, padL - 10, y + 22, {align:'right', color:on ? '#1E2833' : '#8C99A8', bold:on});
      c.fillStyle = on ? (fo.k === '표준 화석' ? '#2B5FA3' : '#A8B3BF') : '#E6EBF1';
      c.fillRect(X(fo.lo), y + 6, X(fo.hi) - X(fo.lo), 22);
      c.strokeStyle = '#8C99A8'; c.lineWidth = 1; c.strokeRect(X(fo.lo), y + 6, X(fo.hi) - X(fo.lo), 22);
      var bx0 = X(fo.lo), bx1 = X(fo.hi), lab = fo.lo + '~' + fo.hi + ' Ma';
      if (bx1 - bx0 > 130) txt(c, lab, (bx0 + bx1) / 2, y + 22, {align:'center', color:on ? '#fff' : '#4A5868', bold:on});
      else txt(c, lab, Math.min(bx1 + 8, W - 120), y + 22, {color:'#4A5868'});
    });
    if (!r){ txt(c, '파란 막대가 표준 화석(짧게 산 무리)이에요.', 20, H - 18, {color:'#4A5868'}); return; }
    var use = r.all.slice(0, used);
    var lo = Math.min.apply(null, use.map(function(x){ return x.lo; }));
    var hi = Math.max.apply(null, use.map(function(x){ return x.hi; }));
    var yb = top + 3 * 44 + 28;
    c.fillStyle = 'rgba(46,158,120,.30)'; c.fillRect(X(lo), top - 6, X(hi) - X(lo), 3 * 44 + 26);
    c.strokeStyle = '#2E9E78'; c.lineWidth = 2; c.strokeRect(X(lo), top - 6, X(hi) - X(lo), 3 * 44 + 26);
    txt(c, '겹치는 구간 ' + lo + ' ~ ' + hi + ' Ma (폭 ' + (lo - hi) + ' Ma)', 20, yb + 34, {bold:true, color:'#2E9E78'});
    if (tau < 1) return;
    txt(c, '감정한 화석 ' + r.n + '종 (' + r.ord.n + ') · 그중 표준 화석 ' + r.narrow + '종', 20, yb + 64, {});
    txt(c, '실제 지층: ' + r.L.age, 20, H - 14, {color:'#4A5868'});
  },
  stats: function(p, r){
    return [['지층', r.L.n], ['감정한 화석 수', r.n + '종'], ['고르는 순서', r.ord.n],
      ['감정한 화석', r.use.map(function(x){ return x.n; }).join(', ')],
      ['그중 표준 화석', r.narrow + '종', PAL[0]],
      ['추정 시기(시작)', r.lo + ' Ma'], ['추정 시기(끝)', r.hi + ' Ma'],
      ['추정 구간의 폭', r.span + ' Ma', PAL[1]], ['실제 지질 시대', r.L.age]];
  },
  columns: ['지층', '화석 수', '순서', '감정한 화석', '시작 (Ma)', '끝 (Ma)', '구간 폭 (Ma)'],
  record: function(p, r){
    return {Li:p.L, layer:r.L.n, age:r.L.age, n:r.n, ord:r.ord.n, desc:r.ord.desc,
      names:r.use.map(function(x){ return x.n; }).join(' + '), lo:r.lo, hi:r.hi, span:r.span, narrow:r.narrow};
  },
  row: function(d){ return [d.layer, d.n, d.ord, d.names, d.lo, d.hi, d.span]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('화석이 늘수록 좁아지는 구간', '<canvas class="chart" id="ch1" role="img" aria-label="화석 수와 추정 구간 폭 산점도"></canvas><ul class="readout" id="ro1"></ul><p class="ask">두 색 선의 줄어드는 속도가 다릅니다. 어떤 화석을 먼저 보는 것이 이득일까요?</p>') +
      card('생존 기간이 짧을수록 쓸모 있다', '<canvas class="chart" id="ch2" role="img" aria-label="화석 1종만 썼을 때 생존 기간과 구간 폭 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">표준 화석의 조건 두 가지(짧은 생존 기간, 넓은 분포) 중 이 그래프가 보여 주는 것은 무엇인가요?</p>') +
      card('지층마다 다른 시대', '<div id="ro3"></div><p class="ask">멀리 떨어진 두 지역의 지층이 같은 시기에 쌓였는지 어떻게 알 수 있을까요?</p>') + '</div>';
    var bo = groupBy(rec, function(d){ return d.ord; }), s1 = [], r1 = [], ci = 0;
    Object.keys(bo).forEach(function(k){
      var g = bo[k], col = PAL[ci++ % PAL.length];
      s1.push({color:col, pts:g.map(function(d){ return {x:d.n, y:d.span}; })});
      var bn = groupBy(g, function(d){ return d.n; }), parts = [];
      Object.keys(bn).sort(function(a, b){ return a - b; }).forEach(function(nn){
        parts.push(nn + '종 → 평균 ' + f(mean(bn[nn].map(function(d){ return d.span; })), 0) + ' Ma');
      });
      r1.push('<li>' + dot(col) + k + ': ' + parts.join(' · ') + '</li>');
    });
    drawScatter($('ch1'), {xLabel:'감정한 화석 수 (종)', yLabel:'추정 구간의 폭 (Ma)', tightX:true, series:s1});
    $('ro1').innerHTML = r1.join('') +
      '<li>화석이 늘면 구간은 <b>절대로 넓어지지 않아요</b>. 겹치는 부분만 남기기 때문이에요.</li>' +
      '<li><b>짧게 산 화석(표준 화석)을 먼저</b> 보면 한 종만으로도 크게 좁혀져요.</li>';
    var one = rec.filter(function(d){ return d.n === 1; });
    drawScatter($('ch2'), {xLabel:'그 화석의 생존 기간 (Ma)', yLabel:'추정 구간의 폭 (Ma)', square:true,
      series:[{color:PAL[0], pts:one.map(function(d){ return {x:d.span, y:d.span}; })}]});
    $('ro2').innerHTML = (one.length ? '<li>화석 1종만 쓴 기록 ' + one.length + '개 — 구간의 폭이 곧 그 화석의 <b>생존 기간</b>이에요.</li>' +
        '<li>가장 좁은 기록: ' + one.slice().sort(function(a, b){ return a.span - b.span; })[0].names + ' (' +
        one.slice().sort(function(a, b){ return a.span - b.span; })[0].span + ' Ma)</li>'
      : '<li>화석 수를 1종으로 두고 여러 지층을 기록해 보세요.</li>') +
      '<li>이 그래프가 보여 주는 것은 <b>짧은 생존 기간</b>이에요. 넓은 분포는 여러 지역에서 같은 화석이 나오는지로 확인해요.</li>';
    var bl = groupBy(rec, function(d){ return d.Li; }), rows = [];
    Object.keys(bl).sort(function(a, b){ return a - b; }).forEach(function(k){
      var g = bl[k], best = g.slice().sort(function(a, b){ return a.span - b.span; })[0];
      rows.push([g[0].layer, g[0].age, g.length + '개', best.lo + '~' + best.hi + ' Ma', best.span + ' Ma', best.names]);
    });
    $('ro3').innerHTML = tableHTML(['지층', '실제 지질 시대', '기록 수', '가장 좁힌 구간', '폭', '그때 쓴 화석'], rows, 'wrap') +
      '<p class="note">같은 표준 화석이 나온 지층은 그 화석이 살던 기간과 겹치는 <b>비슷한 시기에 쌓였을 가능성이 커요</b>. 이렇게 떨어진 지층의 시기를 맞추는 일을 <b>지층 대비</b>라고 해요. 다만 화석이 다른 곳에서 떠내려와 다시 쌓인 경우도 있어 따로 살펴야 해요.</p>';
  }
};`
},

/* ===================== 30. 대멸종과 회복 (Change Ep02) ===================== */
{
  file: '30_mass_extinction_recovery_lab_IntegSci2_Change_Ep02.html',
  title: '사라진 뒤 얼마나 걸려 돌아올까',
  intro: '지질 시대의 다섯 차례 대멸종에서 생물 과(科)의 수가 얼마나 줄었고, 다시 원래 수준으로 돌아오는 데 얼마나 걸렸는지 계산합니다. 회복 조건을 바꿔 가며 기다려 보세요.',
  sceneNote: '멸종 전 과의 수를 1 000으로 둔 교육용 모형입니다. 회복은 로지스틱 성장으로 계산하며, 종 수준 멸종률은 실제 추정값입니다.',
  runLabel: '멸종 뒤 기다리기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 대멸종과 그 뒤의 재편</h3>
<p>지질 시대에는 짧은 기간에 많은 생물이 한꺼번에 사라진 <b>대멸종</b>이 다섯 번 있었어요. 가장 큰 페름기 말에는 바다 생물 종의 약 96 %가 사라졌어요. 멸종은 <b>생물 다양성을 크게 줄이지만</b>, 빈 생태적 지위를 차지한 생물이 새롭게 퍼지는 계기도 돼요. 공룡이 사라진 뒤 포유류가 번성한 것이 그 예예요. 다만 회복에는 <b>수백만~수천만 년</b>이 걸려요.</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>멸종률 51 %면 과 1 000개 중 490개만 남아요. 이 남은 수에서 다시 늘어나기 시작해요.</li>
<li>회복은 로지스틱 성장으로 봐요: <span class="fx-formula">N(t) = K ÷ (1 + (K÷N₀ − 1)·e<sup>−rt</sup>)</span>.</li>
<li>90 % 수준까지 걸리는 시간은 <span class="fx-formula">t = (1÷r)·ln(9 × (K÷N₀ − 1))</span> — 많이 사라질수록 <b>오래</b> 걸려요.</li>
<li>지금의 멸종 속도는 화석 기록의 배경 멸종률보다 100~1 000배 빠르다고 추정돼요. 이것을 여섯 번째 대멸종이라고 부르는 이유예요.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p><span class="fx-formula">N₀ = 1000 × (1 − 과 멸종률)</span> → 로지스틱 회복으로 t년 뒤 N을 구하고, 90 % 회복 시점을 계산합니다.</p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 회복을 하나의 로지스틱 곡선으로 단순화했어요. 실제 회복은 처음에 몇몇 <b>재난 분류군</b>이 폭발적으로 늘었다가 오래 정체하는 등 훨씬 울퉁불퉁해요.<br>
· 회복한 뒤의 생물 구성은 멸종 전과 <b>완전히 달라요</b>. 수가 돌아왔다고 같은 생태계가 된 것은 아니에요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>백악기 말 운석 충돌로 공룡이 사라지자 작은 포유류가 살아남아 오늘날의 다양한 포유류로 퍼졌어요.</li>
<li>지금의 멸종은 서식지 파괴·기후 변화·남획처럼 사람이 원인이라, 원인을 줄이는 선택이 남아 있다는 점이 과거와 달라요.</li>
</ul>`,
  js: `
var EVT = [
  {n:'오르도비스기 말', t:444, sp:85, fam:26, cause:'급격한 빙하기와 해수면 하강'},
  {n:'데본기 후기',   t:372, sp:75, fam:22, cause:'바다의 산소 부족(무산소 사건)'},
  {n:'페름기 말',     t:252, sp:96, fam:51, cause:'대규모 화산 활동, 온난화와 산성화'},
  {n:'트라이아스기 말', t:201, sp:80, fam:22, cause:'대서양이 열리며 일어난 대규모 화산 활동'},
  {n:'백악기 말',     t:66,  sp:76, fam:16, cause:'운석 충돌과 뒤이은 기후 급변'}
];
var RATE = [{n:'느린 회복', r:0.10}, {n:'보통', r:0.20}, {n:'빠른 회복', r:0.35}];
var K = 1000;
return {
  sceneHeight: 470,
  minRec: 4,
  idle: '대멸종 사건과 회복 조건, 기다릴 시간을 정하고 <b>멸종 뒤 기다리기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 사건과 기다리는 시간을 바꿔 가며 기록하세요.',
  params: [
    {key:'e', type:'seg', label:'대멸종 사건 (5대 대멸종)', cols:2, value:2, options:EVT.map(function(x){ return x.n + '<small>' + x.t + ' Ma · 종 ' + x.sp + ' % 멸종</small>'; })},
    {key:'r', type:'seg', label:'회복 조건(환경 안정도)', cols:3, value:1, options:RATE.map(function(x){ return x.n + '<small>r = ' + f(x.r, 2) + '</small>'; })},
    {key:'t', type:'range', label:'기다릴 시간', min:1, max:40, step:1, value:10, fmt:function(v){ return v + ' 백만 년'; },
      note:'멸종 전 과의 수 1 000과 회복률 r은 사건끼리 견주기 위한 <b>가상값</b>입니다. 멸종률은 화석 기록에서 추정한 값이고, 과 수준 멸종률이 종 수준보다 작게 나타납니다.'}
  ],
  compute: function(p){
    var E = EVT[p.e], R = RATE[p.r], t = p.t;
    var N0 = K * (1 - E.fam / 100);
    var N = K / (1 + (K / N0 - 1) * Math.exp(-R.r * t));
    var t90 = Math.log(9 * (K / N0 - 1)) / R.r;
    return {E:E, R:R, t:t, N0:N0, N:N, lost:K - N0, t90:t90, frac:N / K,
      done:t >= t90, back:(N - N0) / Math.max(K - N0, 1)};
  },
  draw: function(c, W, H, p, r, tau){
    var E = EVT[p.e], padL = 90, padR = 40, top = 80, hgt = 230;
    var tmax = 40, X = function(v){ return padL + (v + 8) / (tmax + 8) * (W - padL - padR); };
    var Y = function(v){ return top + hgt - v / K * hgt; };
    for (var v = 0; v <= K; v += 250){ seg(c, padL, Y(v), W - padR, Y(v), '#E3E8EE', 1); txt(c, String(v), padL - 8, Y(v) + 6, {align:'right', color:'#8C99A8'}); }
    seg(c, padL, top, padL, top + hgt, '#8C99A8', 1.5);
    seg(c, padL, top + hgt, W - padR, top + hgt, '#8C99A8', 1.5);
    txt(c, '생물 과(科)의 수', padL - 8, top - 14, {align:'right', color:'#4A5868'});
    txt(c, '멸종 뒤 흐른 시간 (백만 년)', (padL + W - padR) / 2, top + hgt + 34, {align:'center', color:'#4A5868'});
    // 멸종 전 수평선
    seg(c, padL, Y(K), W - padR, Y(K), '#8C99A8', 1.5, [6, 4]);
    txt(c, '멸종 전 1 000', W - padR, Y(K) - 8, {align:'right', color:'#4A5868'});
    if (!r){ txt(c, E.n + ' — 과 ' + E.fam + ' % 멸종 (종 ' + E.sp + ' %)', 20, 44, {bold:true}); txt(c, '사건을 고르고 기다려 보세요.', 20, H - 18, {color:'#4A5868'}); return; }
    // 멸종 순간
    c.strokeStyle = '#C8463D'; c.lineWidth = 2.5;
    c.beginPath(); c.moveTo(X(-8), Y(K)); c.lineTo(X(-2), Y(K)); c.lineTo(X(0), Y(r.N0)); c.stroke();
    txt(c, '멸종', X(-5), Y(K) - 12, {align:'center', color:'#C8463D', bold:true});
    // 회복 곡선
    var tt = r.t * tau;
    c.strokeStyle = '#2E9E78'; c.lineWidth = 2.5; c.beginPath();
    for (var i = 0; i <= 120; i++){
      var x = tt * i / 120, y = K / (1 + (K / r.N0 - 1) * Math.exp(-r.R.r * x));
      if (i) c.lineTo(X(x), Y(y)); else c.moveTo(X(x), Y(y));
    }
    c.stroke();
    var Nn = K / (1 + (K / r.N0 - 1) * Math.exp(-r.R.r * tt));
    c.fillStyle = '#2E9E78'; c.beginPath(); c.arc(X(tt), Y(Nn), 6, 0, Math.PI * 2); c.fill();
    txt(c, E.n + ' (' + E.t + ' Ma)', 20, 44, {bold:true});
    txt(c, f(tt, 1) + ' 백만 년 뒤 과 ' + Math.round(Nn) + '개 (' + f(Nn / K * 100, 0) + ' %)', 20, 68, {color:'#2E9E78', bold:true});
    if (tau < 1) return;
    var yy = top + hgt + 64;
    txt(c, '멸종 직후 ' + Math.round(r.N0) + '개 (' + r.E.fam + ' % 사라짐) → ' + r.t + ' 백만 년 뒤 ' + Math.round(r.N) + '개', 20, yy, {});
    txt(c, '90 % 수준(900개)까지 걸리는 시간 ' + f(r.t90, 1) + ' 백만 년 → ' + (r.done ? '이미 지났어요' : '아직 ' + f(r.t90 - r.t, 1) + ' 백만 년 더 필요해요'),
      20, yy + 30, {bold:true, color:r.done ? '#2E9E78' : '#C8463D'});
    txt(c, '원인: ' + r.E.cause, 20, H - 14, {color:'#4A5868'});
  },
  stats: function(p, r){
    return [['사건', r.E.n + ' (' + r.E.t + ' Ma)'], ['종 수준 멸종률', r.E.sp + ' %'], ['과 수준 멸종률', r.E.fam + ' %', PAL[4]],
      ['멸종 직후 과의 수', Math.round(r.N0) + '개'], ['사라진 과의 수', Math.round(r.lost) + '개'],
      ['회복 조건', r.R.n + ' (r = ' + f(r.R.r, 2) + ')'], ['기다린 시간', r.t + ' 백만 년'],
      ['그때 과의 수', Math.round(r.N) + '개 (' + f(r.frac * 100, 1) + ' %)', PAL[1]],
      ['잃은 몫 중 되찾은 비율', f(r.back * 100, 1) + ' %'],
      ['90 % 회복까지', f(r.t90, 1) + ' 백만 년', PAL[0]], ['원인(추정)', r.E.cause]];
  },
  columns: ['사건', '종 멸종률 (%)', '과 멸종률 (%)', '회복 조건', '기다린 시간 (Myr)', '과의 수', '회복률 (%)', '90 % 회복 (Myr)'],
  record: function(p, r){
    return {ei:p.e, ev:r.E.n, sp:r.E.sp, fam:r.E.fam, rn:r.R.n, rr:r.R.r, t:r.t, N0:r.N0, N:r.N, frac:r.frac, t90:r.t90};
  },
  row: function(d){ return [d.ev, d.sp, d.fam, d.rn, d.t, Math.round(d.N), f(d.frac * 100, 1), f(d.t90, 1)]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('시간에 따른 회복', '<canvas class="chart" id="ch1" role="img" aria-label="기다린 시간과 과의 수 산점도"></canvas><ul class="readout" id="ro1"></ul><p class="ask">회복 곡선은 처음에 천천히, 그다음 빠르게, 마지막에 다시 천천히 올라갑니다. 마지막이 느린 까닭은 무엇일까요?</p>') +
      card('많이 사라질수록 오래 걸린다', '<canvas class="chart" id="ch2" role="img" aria-label="멸종률과 90 % 회복 시간 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">페름기 말과 백악기 말의 회복 시간을 비교해 보세요. 지금의 멸종에 어떤 뜻이 있을까요?</p>') +
      card('다섯 번의 대멸종', '<div id="ro3"></div><p class="ask">대멸종은 나쁘기만 할까요? 빈 생태적 지위가 생긴 뒤 어떤 일이 일어났는지 말해 보세요.</p>') + '</div>';
    var bg = groupBy(rec, function(d){ return d.ei + '-' + d.rn; }), s1 = [], r1 = [], ci = 0;
    Object.keys(bg).forEach(function(k){
      var g = bg[k], col = PAL[ci++ % PAL.length];
      s1.push({color:col, pts:g.map(function(d){ return {x:d.t, y:d.N}; })});
      if (g.length >= 2){
        var srt = g.slice().sort(function(a, b){ return a.t - b.t; });
        r1.push('<li>' + dot(col) + g[0].ev + ' · ' + g[0].rn + ': ' + srt[0].t + ' Myr에 ' + Math.round(srt[0].N) + '개 → ' +
          srt[srt.length-1].t + ' Myr에 ' + Math.round(srt[srt.length-1].N) + '개</li>');
      }
    });
    drawScatter($('ch1'), {xLabel:'멸종 뒤 흐른 시간 (백만 년)', yLabel:'생물 과(科)의 수', series:s1, lines:[{h:900, color:'#8C99A8', dash:[6,4]}]});
    $('ro1').innerHTML = (r1.length ? r1.join('') : '<li>같은 사건에서 기다리는 시간만 바꿔 2번 이상 기록해 보세요.</li>') +
      '<li>회색 점선이 90 % 수준이에요. 마지막이 느린 까닭은 <b>빈 자리가 거의 없어</b> 더 늘기 어렵기 때문이에요(환경 수용력).</li>';
    var seen = {}, pts2 = [];
    rec.forEach(function(d){ var k = d.ei + '-' + d.rn; if (seen[k]) return; seen[k] = 1; pts2.push({x:d.fam, y:d.t90, ev:d.ev, rn:d.rn}); });
    drawScatter($('ch2'), {xLabel:'과 수준 멸종률 (%)', yLabel:'90 % 회복까지 걸리는 시간 (백만 년)', tightX:true, tightY:true,
      series:[{color:PAL[4], pts:pts2}]});
    var srt2 = pts2.slice().sort(function(a, b){ return a.x - b.x; });
    $('ro2').innerHTML = srt2.map(function(q){ return '<li>' + q.ev + ' (' + q.rn + '): 멸종률 ' + q.x + ' % → 회복 <b>' + f(q.y, 1) + ' 백만 년</b></li>'; }).join('') +
      '<li>많이 사라질수록 다시 시작할 <b>밑천</b>이 적어 회복이 오래 걸려요.</li>' +
      '<li>회복에 걸리는 수백만 년은 사람의 시간으로는 사실상 <b>되돌릴 수 없는</b> 길이예요.</li>';
    var rows = EVT.map(function(E){
      var mine = rec.filter(function(d){ return d.ev === E.n; });
      return [E.n, E.t + ' Ma', E.sp + ' %', E.fam + ' %', E.cause, mine.length + '개'];
    });
    $('ro3').innerHTML = tableHTML(['사건', '시기', '종 멸종률', '과 멸종률', '원인(추정)', '내 기록'], rows, 'wrap') +
      '<p class="note">멸종 뒤에는 빈 생태적 지위를 차지한 무리가 크게 퍼졌어요. 공룡이 사라진 뒤의 포유류가 대표적이에요. 다만 그 자리에 우리가 있으리란 보장은 없어요.</p>';
  }
};`
},

/* ===================== 31. 유전적 다양성과 병 확산 (Change Ep04) ===================== */
{
  file: '31_crop_diversity_blight_lab_IntegSci2_Change_Ep04.html',
  title: '다 똑같은 감자밭',
  intro: '20 × 20칸 밭에 감자를 심고 한가운데에 마름병을 들여놓습니다. 심는 품종 수와 병원체의 힘을 바꿔 가며, 밭의 몇 %가 병에 걸리는지 세어 보세요.',
  sceneNote: '칸마다 품종을 같은 확률로 무작위로 심습니다. 병원체는 <b>품종 1을 노리도록 적응한 균주</b>라 품종 1은 늘 걸리며, 같은 품종 이웃으로 잘 옮고 다른 품종에는 잘 옮지 않습니다. 나머지 품종은 35 % 확률로 이 병에 저항성을 가지므로, 결과에는 다양성 효과와 저항성 효과가 함께 들어 있습니다.',
  runLabel: '병 퍼뜨리기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 유전적 다양성이 방어벽이 된다</h3>
<p>생물 다양성에는 <b>유전적 다양성·종 다양성·생태계 다양성</b>의 세 층이 있어요. 그중 <b>유전적 다양성</b>은 같은 종 안에서 유전자가 얼마나 다양한가를 뜻해요. 한 품종만 심은 밭은 모든 개체가 <b>똑같은 약점</b>을 가지므로, 그 약점을 파고드는 병원체가 나타나면 밭 전체가 한꺼번에 무너져요. 여러 품종을 섞어 심으면 병에 걸린 포기 옆에 <b>옮기 어려운 포기</b>가 있어 확산이 중간에 끊겨요.</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>품종이 n가지면 이웃이 같은 품종일 확률은 약 <span class="fx-formula">1 ÷ n</span>이에요. 품종이 늘수록 옮을 기회가 줄어요.</li>
<li>확산이 이어지려면 한 포기가 평균 1포기 넘게 옮겨야 해요. 그 경계를 넘지 못하면 확산이 <b>갑자기</b> 멈춰요(임계 현상).</li>
<li>1845년 아일랜드는 거의 한 품종(럼퍼)만 심었다가 감자마름병으로 수확이 거의 사라졌고, 100만 명 넘게 굶어 죽었어요.</li>
<li>오늘날 바나나(캐번디시)도 사실상 한 품종이라 같은 위험을 안고 있어요.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p>칸마다 품종을 무작위로 심고, 가운데에서 시작해 상하좌우로 <span class="fx-formula">옮을 확률 = 기본 확률 × (같은 품종 1, 다른 품종 0.25, 저항성 0.05)</span>로 번지게 합니다.</p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 밭을 <b>격자</b>로, 확산을 상하좌우 이웃으로만 단순화했어요. 실제 병원체는 바람·물·농기구·사람을 타고 멀리 건너뛰어요.<br>
· 난수를 쓰므로 같은 설정에서도 결과가 조금씩 달라요. 여러 번 기록해 평균으로 보는 것이 맞아요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>종자 은행은 사라진 재래 품종의 씨앗을 보관해 두었다가 새로운 병이 돌 때 저항성 유전자를 찾는 데 써요.</li>
<li>농사에서 여러 작물을 돌려짓기·섞어짓기 하는 것도 같은 원리예요.</li>
</ul>`,
  js: `
var N = 20;
var VAR = [1, 2, 4, 8];
function build(nv, rnd){
  var g = [], res = [];
  // 품종 1은 이 병원체가 노리도록 적응한 기준 품종 — 늘 감수성
  for (var v = 0; v < nv; v++) res.push(v === 0 ? false : rnd() < 0.35);
  for (var i = 0; i < N * N; i++) g.push(Math.floor(rnd() * nv));
  return {g:g, res:res};
}
function rng(seed){ var s = seed >>> 0; return function(){ s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
return {
  sceneHeight: 470,
  minRec: 4,
  idle: '품종 수와 병원체의 힘을 정하고 <b>병 퍼뜨리기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 품종 수와 병원체의 힘을 바꿔 가며 기록하세요.',
  params: [
    {key:'v', type:'seg', label:'심는 품종 수', cols:4, value:0, options:VAR.map(function(x){ return x + '가지'; })},
    {key:'p', type:'range', label:'병원체의 힘(옮을 기본 확률)', min:0.2, max:0.9, step:0.05, value:0.6, fmt:function(x){ return f(x, 2); },
      note:'품종 1은 이 병원체가 노리도록 적응한 기준 품종이라 늘 걸립니다. 나머지 품종은 35 % 확률로 저항성을 가지므로 결과에는 <b>다양성 효과와 저항성 효과가 섞여</b> 있습니다. 매번 무작위로 다시 심어 값이 조금씩 달라집니다.'}
  ],
  compute: function(p){
    var nv = VAR[p.v], base = p.p, rnd = rng(Math.floor(Math.random() * 1e9));
    var F = build(nv, rnd), g = F.g, res = F.res;
    var sick = new Array(N * N).fill(false);
    var start = (N / 2) * N + N / 2;
    sick[start] = true;
    var q = [start], order = [start];
    while (q.length){
      var cur = q.shift(), cx = cur % N, cy = Math.floor(cur / N);
      var nb = [[cx+1,cy],[cx-1,cy],[cx,cy+1],[cx,cy-1]];
      for (var k = 0; k < 4; k++){
        var x = nb[k][0], y = nb[k][1];
        if (x < 0 || y < 0 || x >= N || y >= N) continue;
        var id = y * N + x;
        if (sick[id]) continue;
        var mult = res[g[id]] ? 0.05 : (g[id] === g[cur] ? 1 : 0.25);
        if (rnd() < base * mult){ sick[id] = true; q.push(id); order.push(id); }
      }
    }
    var cnt = sick.reduce(function(s, x){ return s + (x ? 1 : 0); }, 0);
    var nres = res.reduce(function(s, x){ return s + (x ? 1 : 0); }, 0);
    return {nv:nv, base:base, g:g, res:res, sick:sick, order:order, cnt:cnt,
      loss:cnt / (N * N) * 100, yield:(1 - cnt / (N * N)) * 100, nres:nres, start:start};
  },
  draw: function(c, W, H, p, r, tau){
    var cell = Math.max(8, Math.min(13, Math.floor((W - 70) / N)));
    var ox = 30, oy = 70, VC = ['#5C8A3A', '#8AA84C', '#C2B04A', '#7A9E7E', '#A88C4A', '#6FA3A0', '#9C8FB0', '#B0865A'];
    txt(c, '감자밭 ' + N + ' × ' + N + '칸 · 품종 ' + VAR[p.v] + '가지', ox, 44, {bold:true});
    var shown = r ? Math.round(r.order.length * tau) : 0;
    var sickNow = {};
    if (r) for (var i = 0; i < shown; i++) sickNow[r.order[i]] = 1;
    for (var y = 0; y < N; y++) for (var x = 0; x < N; x++){
      var id = y * N + x, vi = r ? r.g[id] : (x * 7 + y * 3) % VAR[p.v];
      c.fillStyle = sickNow[id] ? '#8A3A32' : VC[vi % VC.length];
      c.fillRect(ox + x * cell, oy + y * cell, cell - 1, cell - 1);
      if (r && r.res[vi] && !sickNow[id]){
        c.fillStyle = 'rgba(255,255,255,.65)';
        c.fillRect(ox + x * cell + cell / 2 - 1.5, oy + y * cell + cell / 2 - 1.5, 3, 3);
      }
    }
    // 범례 (격자 아래 한 줄)
    var ly = oy + N * cell + 24, lx = ox;
    for (var v2 = 0; v2 < VAR[p.v] && v2 < 8; v2++){
      c.fillStyle = VC[v2 % VC.length]; c.fillRect(lx, ly - 11, 13, 13);
      if (r && r.res[v2]){ c.fillStyle = 'rgba(255,255,255,.8)'; c.fillRect(lx + 5, ly - 6, 3, 3); }
      txt(c, String(v2 + 1), lx + 17, ly, {color:'#4A5868', size:15});
      lx += 32;
    }
    txt(c, '= 품종 번호 (흰 점은 저항성)', lx + 4, ly, {color:'#4A5868', size:15});
    c.fillStyle = '#8A3A32'; c.fillRect(ox, ly + 13, 13, 13);
    txt(c, '병에 걸린 칸', ox + 18, ly + 24, {color:'#8A3A32', size:15});
    if (!r){ txt(c, '가운데 한 포기에서 병이 시작돼요.', ox, H - 18, {color:'#4A5868'}); return; }
    var yy = oy + N * cell + 66;
    txt(c, '병에 걸린 칸 ' + shown + ' / ' + (N * N) + '칸', ox, yy, {bold:true, color:'#8A3A32'});
    if (tau < 1) return;
    txt(c, '피해율 ' + f(r.loss, 1) + ' % → 수확량 ' + f(r.yield, 1) + ' % (저항성 품종 ' + r.nres + ' / ' + r.nv + '가지)', ox, yy + 30,
      {bold:true, color:r.loss > 50 ? '#C8463D' : '#2E9E78'});
    txt(c, r.nv === 1 ? '한 품종만 심으면 약점도 하나예요 — 병이 밭 전체로 번지기 쉬워요.'
      : '품종이 섞여 있어 번지다가 막히는 자리가 생겨요.', ox, H - 14, {color:'#4A5868'});
  },
  stats: function(p, r){
    return [['품종 수', r.nv + '가지'], ['그중 저항성 품종', r.nres + '가지'],
      ['병원체의 힘', f(r.base, 2)], ['밭의 칸 수', (N * N) + '칸'],
      ['병에 걸린 칸', r.cnt + '칸', PAL[4]], ['피해율', f(r.loss, 1) + ' %', PAL[4]],
      ['남은 수확량', f(r.yield, 1) + ' %', PAL[1]],
      ['이웃이 같은 품종일 확률(어림)', f(100 / r.nv, 1) + ' %']];
  },
  columns: ['품종 수', '저항성 품종', '병원체 힘', '걸린 칸', '피해율 (%)', '수확량 (%)'],
  record: function(p, r){ return {nv:r.nv, nres:r.nres, base:r.base, cnt:r.cnt, loss:r.loss, yld:r.yield}; },
  row: function(d){ return [d.nv + '가지', d.nres + '가지', f(d.base, 2), d.cnt, f(d.loss, 1), f(d.yld, 1)]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('품종 수와 피해율', '<canvas class="chart" id="ch1" role="img" aria-label="품종 수와 피해율 산점도"></canvas><ul class="readout" id="ro1"></ul><p class="ask">품종을 1가지에서 2가지로 늘렸을 때와, 4가지에서 8가지로 늘렸을 때 중 어느 쪽 효과가 컸나요?</p>') +
      card('병원체가 세지면', '<canvas class="chart" id="ch2" role="img" aria-label="병원체 힘과 피해율 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">어떤 품종 수에서는 병원체가 세져도 피해가 크게 늘지 않습니다. 확산이 이어지는 조건을 생각해 보세요.</p>') +
      card('품종 수별 요약', '<div id="ro3"></div><p class="ask">수확량이 가장 많은 품종을 딱 하나 골라 심는 것이 늘 이득일까요? 아일랜드 감자 기근과 연결해 말해 보세요.</p>') + '</div>';
    var bv = groupBy(rec, function(d){ return d.nv; }), pts1 = [], r1 = [];
    Object.keys(bv).sort(function(a, b){ return a - b; }).forEach(function(k){
      var g = bv[k], m = mean(g.map(function(d){ return d.loss; }));
      pts1.push({x:+k, y:m});
      r1.push('<li>품종 <b>' + k + '가지</b>: 기록 ' + g.length + '개, 평균 피해율 <b>' + f(m, 1) + ' %</b></li>');
    });
    drawScatter($('ch1'), {xLabel:'품종 수 (가지)', yLabel:'평균 피해율 (%)', tightX:true,
      series:[{color:PAL[4], pts:pts1}, {color:PAL[5], pts:rec.map(function(d){ return {x:d.nv, y:d.loss}; })}]});
    $('ro1').innerHTML = r1.join('') +
      '<li>' + dot(PAL[4]) + '큰 점이 평균, ' + dot(PAL[5]) + '작은 점이 각 기록이에요. 난수를 쓰므로 같은 설정에서도 값이 흔들려요.</li>' +
      (function(){
        var ks = Object.keys(bv).map(Number).sort(function(a, b){ return a - b; });
        if (ks.length < 2) return '<li>품종 수를 2가지 이상으로 바꿔 기록하면 어느 구간에서 효과가 가장 큰지 알 수 있어요.</li>';
        var best = null;
        for (var i = 1; i < ks.length; i++){
          var d0 = mean(bv[ks[i-1]].map(function(x){ return x.loss; })) - mean(bv[ks[i]].map(function(x){ return x.loss; }));
          if (!best || d0 > best.d) best = {a:ks[i-1], b:ks[i], d:d0};
        }
        return '<li>내 기록에서는 품종을 <b>' + best.a + ' → ' + best.b + '가지</b>로 늘릴 때 평균 피해율이 <b>' + f(best.d, 1) + ' %p</b>로 가장 많이 줄었어요.</li>';
      })();
    var bv2 = groupBy(rec, function(d){ return d.nv; }), s2 = [], ci = 0, r2 = [];
    Object.keys(bv2).sort(function(a, b){ return a - b; }).forEach(function(k){
      var g = bv2[k], col = PAL[ci++ % PAL.length];
      s2.push({color:col, pts:g.map(function(d){ return {x:d.base, y:d.loss}; })});
      r2.push('<li>' + dot(col) + '품종 ' + k + '가지: 병원체 힘 ' + f(Math.min.apply(null, g.map(function(d){ return d.base; })), 2) +
        '~' + f(Math.max.apply(null, g.map(function(d){ return d.base; })), 2) + ' 구간에서 피해율 ' +
        f(Math.min.apply(null, g.map(function(d){ return d.loss; })), 1) + '~' + f(Math.max.apply(null, g.map(function(d){ return d.loss; })), 1) + ' %</li>');
    });
    drawScatter($('ch2'), {xLabel:'병원체의 힘 (옮을 기본 확률)', yLabel:'피해율 (%)', tightX:true, series:s2});
    $('ro2').innerHTML = r2.join('') +
      '<li>한 포기가 평균 1포기 넘게 옮기지 못하면 확산이 <b>중간에 끊겨요</b>. 품종이 많을수록 그 문턱을 넘기 어려워요.</li>';
    var rows = [];
    Object.keys(bv).sort(function(a, b){ return a - b; }).forEach(function(k){
      var g = bv[k];
      rows.push([k + '가지', g.length + '개', f(mean(g.map(function(d){ return d.loss; })), 1) + ' %',
        f(Math.max.apply(null, g.map(function(d){ return d.loss; })), 1) + ' %',
        f(mean(g.map(function(d){ return d.yld; })), 1) + ' %']);
    });
    $('ro3').innerHTML = tableHTML(['품종 수', '기록 수', '평균 피해율', '가장 나빴던 피해율', '평균 수확량'], rows) +
      '<p class="note">한 품종만 심으면 좋은 해에는 수확이 가장 많을 수 있어요. 하지만 나쁜 해에 <b>전부</b>를 잃어요. 유전적 다양성은 평균을 조금 낮추는 대신 <b>최악을 막는 보험</b>이에요.</p>';
  }
};`
},

/* ===================== 32. 금속의 반응성 (Change Ep05) ===================== */
{
  file: '32_metal_reactivity_redox_lab_IntegSci2_Change_Ep05.html',
  title: '금속을 이온 용액에 담그면',
  intro: '금속 조각을 다른 금속의 이온이 녹아 있는 용액에 담급니다. 어떤 짝에서 반응이 일어나고 어떤 짝에서는 아무 일도 없는지, 그리고 금속이 몇 g 녹고 몇 g이 석출되는지 재어 보세요.',
  sceneNote: '용액 속 금속 이온은 충분히 많다고 가정했습니다. 반응이 일어나면 담근 금속은 전자를 잃어 녹고, 용액 속 이온은 전자를 얻어 금속으로 달라붙습니다.',
  runLabel: '담그기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 전자를 잃으면 산화, 얻으면 환원</h3>
<p>산화와 환원은 <b>항상 함께</b> 일어나요. 어떤 물질이 전자를 잃으면(산화) 다른 물질이 그 전자를 얻어요(환원). 금속마다 <b>전자를 내놓으려는 정도</b>가 달라서 순서를 매길 수 있는데, 이것이 <b>금속의 반응성 서열</b>이에요. 반응성이 큰 금속을 반응성이 작은 금속의 이온 용액에 담그면, 담근 금속이 <b>녹으면서</b> 용액 속 금속이 <b>석출</b>돼요. 반대 짝에서는 아무 일도 일어나지 않아요.</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>반응성 순서: <b>Mg &gt; Zn &gt; Fe &gt; Cu &gt; Ag</b>. 왼쪽 금속은 오른쪽 금속의 이온을 밀어낼 수 있어요.</li>
<li>Zn + Cu²⁺ → Zn²⁺ + Cu. 아연 65.4 g(1 mol)이 녹으면 전자 2 mol이 나오고 구리 63.5 g(1 mol)이 석출돼요.</li>
<li>Cu + 2Ag⁺ → Cu²⁺ + 2Ag. 전자 2 mol당 은은 <b>2 mol</b>(215.8 g)이 석출돼요. 전하가 +1이기 때문이에요.</li>
<li>전자 1 mol이 석출시키는 질량은 <span class="fx-formula">몰 질량 ÷ 이온의 전하</span>예요.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p><span class="fx-formula">전자 mol = (담근 금속 g ÷ 몰 질량) × 전하</span>, <span class="fx-formula">석출 g = 전자 mol ÷ 상대 전하 × 상대 몰 질량</span>, 질량 변화 = 석출 − 녹음</p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 담근 금속이 <b>전부 녹는다</b>고 봤어요. 실제로는 표면에 석출물이 덮여 반응이 도중에 느려지거나 멈춰요.<br>
· 용액 속 이온이 무제한이라고 두었어요. 실제로는 이온이 떨어지면 반응이 멈추고, 금속에 따라 물이나 산과도 반응해요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>철제 배의 선체에 아연 덩어리를 붙여 두면, 반응성이 큰 아연이 먼저 산화되어 철이 녹스는 것을 막아요(희생 양극).</li>
<li>도금은 반응성 차이를 이용해 다른 금속을 얇게 입히는 기술이에요.</li>
</ul>`,
  js: `
var MET = [{s:'Mg',n:'마그네슘',M:24.3,v:2,rk:5},{s:'Zn',n:'아연',M:65.4,v:2,rk:4},
           {s:'Fe',n:'철',M:55.8,v:2,rk:3},{s:'Cu',n:'구리',M:63.5,v:2,rk:2}];
var ION = [{s:'Zn²⁺',m:'Zn',n:'아연',M:65.4,v:2,rk:4,col:'#CFD6DD'},{s:'Fe²⁺',m:'Fe',n:'철',M:55.8,v:2,rk:3,col:'#B9CBB0'},
           {s:'Cu²⁺',m:'Cu',n:'구리',M:63.5,v:2,rk:2,col:'#6FA8C8'},{s:'Ag⁺',m:'Ag',n:'은',M:107.9,v:1,rk:1,col:'#DCDCE4'}];
return {
  sceneHeight: 460,
  minRec: 4,
  idle: '금속과 용액, 금속의 질량을 정하고 <b>담그기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 금속과 용액의 짝을 여러 가지로 바꿔 기록하세요.',
  params: [
    {key:'m', type:'seg', label:'담그는 금속', cols:4, value:1, options:MET.map(function(x){ return x.s + '<small>' + x.n + '</small>'; })},
    {key:'i', type:'seg', label:'용액 속 이온', cols:4, value:2, options:ION.map(function(x){ return x.s + '<small>' + x.n + ' 이온</small>'; })},
    {key:'g', type:'range', label:'담그는 금속의 질량', min:1, max:20, step:1, value:6.5, fmt:function(v){ return f(v, 1) + ' g'; },
      note:'같은 금속을 자기 이온 용액에 담그면 겉보기 변화가 없습니다. 반응성이 작은 금속을 큰 금속의 이온에 담가도 반응하지 않습니다.'}
  ],
  compute: function(p){
    var M = MET[p.m], I = ION[p.i], g = p.g;
    var same = (M.s === I.m);
    var react = !same && M.rk > I.rk;
    var nM = g / M.M, e = nM * M.v, dep = e / I.v * I.M;
    return {M:M, I:I, g:g, same:same, react:react, nM:nM,
      e:react ? e : 0, dep:react ? dep : 0, dissolved:react ? g : 0,
      dmass:react ? dep - g : 0, eqI:I.M / I.v, eqM:M.M / M.v};
  },
  draw: function(c, W, H, p, r, tau){
    var M = MET[p.m], I = ION[p.i];
    var bx = 70, by = 96, bw = Math.min(260, W - 300), bh = 190;
    c.fillStyle = '#F7F9FC'; c.fillRect(bx, by, bw, bh);
    c.strokeStyle = '#5B6776'; c.lineWidth = 2; c.strokeRect(bx, by, bw, bh);
    var fade = r && r.react ? Math.max(0.25, 1 - tau * 0.75) : 1;
    c.globalAlpha = fade; c.fillStyle = I.col; c.fillRect(bx + 2, by + 40, bw - 4, bh - 42); c.globalAlpha = 1;
    txt(c, I.s + ' 용액', bx + 8, by + 28, {color:'#4A5868'});
    // 금속 조각
    var sw = 46, sh = 120, sx = bx + bw / 2 - sw / 2, sy = by + 30;
    var eaten = r && r.react ? Math.min(0.55, tau * 0.55) : 0;
    c.fillStyle = '#9AA6B2'; c.fillRect(sx, sy + sh * eaten, sw, sh * (1 - eaten));
    c.strokeStyle = '#5B6776'; c.lineWidth = 2; c.strokeRect(sx, sy + sh * eaten, sw, sh * (1 - eaten));
    txt(c, M.s, sx + sw / 2, sy + sh / 2 + 30, {align:'center', bold:true, color:'#2E3945'});
    // 석출물
    if (r && r.react && tau > 0.25){
      var k = (tau - 0.25) / 0.75;
      c.fillStyle = I.m === 'Cu' ? '#A8702F' : I.m === 'Ag' ? '#B6BCC6' : '#8C99A8';
      for (var i = 0; i < 26; i++){
        var xx = sx - 12 + (i % 6) * (sw + 24) / 5, yy2 = sy + 20 + Math.floor(i / 6) * 22;
        if (yy2 > by + bh - 10) break;
        c.beginPath(); c.arc(xx, yy2, 4.5 * Math.min(1, k * 1.4), 0, Math.PI * 2); c.fill();
      }
    }
    var lx = bx + bw + 36;
    if (lx < W - 200){
      txt(c, '반응성 서열', lx, by + 6, {bold:true, color:'#4A5868'});
      ['Mg', 'Zn', 'Fe', 'Cu', 'Ag'].forEach(function(s, i){
        var on = (s === M.s) || (s === I.m);
        txt(c, (i === 0 ? '큼  ' : i === 4 ? '작음 ' : '    ') + s, lx, by + 34 + i * 26, {bold:on, color:on ? '#2B5FA3' : '#8C99A8'});
      });
    }
    if (!r){ txt(c, '반응성이 큰 금속이 작은 금속의 이온을 밀어내요.', bx, H - 18, {color:'#4A5868'}); return; }
    if (tau < 0.9) return;
    var yy = by + bh + 40;
    if (r.same) txt(c, M.s + '을(를) ' + I.s + ' 용액에 담갔어요 — 같은 금속이라 겉보기 변화가 없어요.', bx - 40, yy, {bold:true, color:'#A8702F'});
    else if (!r.react) txt(c, M.s + '은(는) ' + I.m + '보다 반응성이 작아요 — 아무 일도 일어나지 않아요.', bx - 40, yy, {bold:true, color:'#C8463D'});
    else {
      var gc = (function(a, b){ while (b){ var t2 = b; b = a % b; a = t2; } return a; })(M.v, I.v);
      var cM = I.v / gc, cI = M.v / gc;     // 주고받는 전자 수를 맞춘 계수
      var co = function(k){ return k === 1 ? '' : k; };
      txt(c, co(cM) + M.s + ' + ' + co(cI) + I.s + ' → ' + co(cM) + M.s + (M.v === 2 ? '²⁺' : '⁺') + ' + ' + co(cI) + I.m + ' (산화: ' + M.s + ', 환원: ' + I.m + ')', bx - 40, yy, {bold:true, color:'#2E9E78'});
      txt(c, M.s + ' ' + f(r.g, 1) + ' g 녹음 → 전자 ' + f(r.e, 3) + ' mol → ' + I.m + ' ' + f(r.dep, 2) + ' g 석출', bx - 40, yy + 30, {});
    }
    txt(c, '질량 변화 ' + (r.react ? sgn(r.dmass, 2) + ' g' : '0 g'), bx - 40, H - 14, {color:'#4A5868'});
  },
  stats: function(p, r){
    return [['담근 금속', r.M.n + ' ' + r.M.s], ['용액', r.I.s + ' (' + r.I.n + ' 이온)'],
      ['반응성 비교', r.same ? '같은 금속' : (r.react ? r.M.s + ' > ' + r.I.m : r.M.s + ' < ' + r.I.m), r.react ? PAL[1] : PAL[4]],
      ['반응 여부', r.react ? '일어남' : '일어나지 않음', r.react ? PAL[1] : PAL[4]],
      ['담근 질량', f(r.g, 1) + ' g = ' + f(r.nM, 4) + ' mol'],
      ['산화된 물질', r.react ? r.M.s + ' → ' + r.M.s + (r.M.v === 2 ? '²⁺' : '⁺') : '—'],
      ['환원된 물질', r.react ? r.I.s + ' → ' + r.I.m : '—'],
      ['이동한 전자', f(r.e, 4) + ' mol', PAL[6]],
      ['석출된 금속', f(r.dep, 2) + ' g', PAL[0]],
      ['질량 변화(석출 − 녹음)', sgn(r.dmass, 2) + ' g'],
      ['전자 1 mol이 석출시키는 양', f(r.eqI, 1) + ' g (' + r.I.m + ')']];
  },
  columns: ['금속', '용액', '반응', '담근 (g)', '전자 (mol)', '석출 (g)', '질량 변화 (g)'],
  record: function(p, r){
    return {mi:p.m, ii:p.i, met:r.M.s, ion:r.I.s, dep:r.I.m, react:r.react, same:r.same,
      g:r.g, e:r.e, depg:r.dep, dm:r.dmass, eq:r.eqI, mrk:r.M.rk, irk:r.I.rk};
  },
  row: function(d){ return [d.met, d.ion, d.same ? '같은 금속' : (d.react ? '일어남' : '없음'), f(d.g, 1),
    f(d.e, 4), f(d.depg, 2), sgn(d.dm, 2)]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('어떤 짝에서 반응했나', '<div id="ro1"></div><p class="ask">표의 ○ 표시를 보고 금속을 반응성이 큰 순서로 늘어놓아 보세요. 표의 모양에 규칙이 보이나요?</p>') +
      card('전자와 석출 질량', '<canvas class="chart" id="ch2" role="img" aria-label="전자 몰수와 석출 질량 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">은이 구리보다 훨씬 많이 석출되는 까닭은 무엇일까요? 이온의 전하와 연결해 설명해 보세요.</p>') +
      card('산화와 환원은 함께', '<div id="ro3"></div><p class="ask">한쪽이 전자를 잃으면 반드시 다른 쪽이 얻습니다. 내 기록에서 산화된 물질과 환원된 물질을 짝지어 보세요.</p>') + '</div>';
    var rows = MET.map(function(M){
      return [M.s].concat(ION.map(function(I){
        var hit = rec.filter(function(d){ return d.met === M.s && d.dep === I.m; });
        if (!hit.length) return '·';
        return hit[0].same ? '=' : (hit[0].react ? '<b style="color:#2E9E78">○</b>' : '<span style="color:#C8463D">×</span>');
      }));
    });
    $('ro1').innerHTML = tableHTML(['금속 \\ 용액'].concat(ION.map(function(I){ return I.s; })), rows, 'center') +
      '<p class="note">○ 반응함 · × 반응 없음 · = 같은 금속 · · 아직 안 해 봄<br>표의 왼쪽 아래가 ○로 채워지면, 왼쪽 금속일수록 반응성이 크다는 뜻이에요. 서열: <b>Mg &gt; Zn &gt; Fe &gt; Cu &gt; Ag</b></p>';
    var ok = rec.filter(function(d){ return d.react; });
    var bd = groupBy(ok, function(d){ return d.dep; }), s2 = [], r2 = [], ci = 0;
    Object.keys(bd).forEach(function(k){
      var g = bd[k], col = PAL[ci++ % PAL.length];
      s2.push({color:col, pts:g.map(function(d){ return {x:d.e, y:d.depg}; })});
      if (distinct(g.map(function(d){ return d.e; })) >= 2){
        var kk = fit0(g.map(function(d){ return {x:d.e, y:d.depg}; }));
        r2.push('<li>' + dot(col) + k + ' 석출: 기울기 <b>' + f(kk, 1) + ' g/mol</b> = 몰 질량 ÷ 전하 = ' + f(g[0].eq, 1) + '</li>');
      } else r2.push('<li>' + dot(col) + k + ' 석출: 기록 ' + g.length + '개 (담근 질량을 바꿔 2개 이상 모아 보세요)</li>');
    });
    drawScatter($('ch2'), {xLabel:'이동한 전자 (mol)', yLabel:'석출된 금속 (g)', series:s2.length ? s2 : [{color:PAL[0], pts:[]}]});
    $('ro2').innerHTML = (r2.length ? r2.join('') : '<li>반응이 일어나는 짝으로 2번 이상 기록해 보세요.</li>') +
      '<li>Ag⁺는 전자 <b>1개</b>만 받으면 되므로 같은 전자로 2배 많은 개수가 석출돼요. 몰 질량도 커서 질량 차이가 더 벌어져요.</li>';
    var seen = {}, rows3 = [];
    ok.forEach(function(d){ var k = d.met + d.dep; if (seen[k]) return; seen[k] = 1;
      rows3.push([d.met + ' → ' + d.met + '²⁺', d.ion + ' → ' + d.dep, '전자를 잃음(산화)', '전자를 얻음(환원)', f(d.e, 4) + ' mol']); });
    $('ro3').innerHTML = rows3.length ? tableHTML(['산화된 물질', '환원된 물질', '왼쪽에서', '오른쪽에서', '주고받은 전자'], rows3, 'wrap') +
      '<p class="note">잃은 전자의 수와 얻은 전자의 수는 <b>언제나 같아요</b>. 그래서 산화와 환원은 따로 일어날 수 없어요.</p>'
      : '<p class="note">반응이 일어나는 짝(반응성이 큰 금속 + 작은 금속의 이온)으로 기록해 보세요.</p>';
  }
};`
},

/* ===================== 33. 철의 제련 (Change Ep06) ===================== */
{
  file: '33_iron_smelting_reduction_lab_IntegSci2_Change_Ep06.html',
  title: '철광석에서 철을 꺼내기',
  intro: '철광석과 코크스(탄소)를 용광로에 넣고 가열합니다. 광석의 종류와 양, 넣은 탄소의 양을 바꿔 가며 철이 몇 kg 나오고 이산화 탄소가 얼마나 배출되는지 계산해 보세요.',
  sceneNote: '광석 속 산소를 탄소가 떼어 가는 환원 반응입니다. 산소 1 mol을 떼는 데 탄소 1 mol이 든다고 보고 계산했습니다.',
  runLabel: '용광로 가열하기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 제련은 거대한 환원 반응</h3>
<p>자연에서 철은 대부분 <b>산소와 결합한 상태</b>(산화 철)로 있어요. 철을 얻으려면 이 산소를 떼어 내야 하는데, 산소를 더 좋아하는 물질인 <b>탄소</b>를 함께 넣고 높은 온도로 가열하면 탄소가 산소를 가져가요. 철은 <b>환원</b>되고 탄소는 <b>산화</b>되는 거예요. 이 기술을 얻은 순간이 철기 시대의 시작이고, 지금도 제철소는 같은 원리로 돌아가요. 다만 그만큼 이산화 탄소가 나와요.</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>Fe₂O₃ + 3C → 2Fe + 3CO↑ — 적철석 160 g에서 철 111.6 g(69.9 %)이 나오고, 산소 3 mol을 떼는 데 탄소 3 mol(36 g)이 들어요.</li>
<li>광석 속 철의 질량비: 적철석 Fe₂O₃ <b>69.9 %</b>, 자철석 Fe₃O₄ <b>72.4 %</b>, 갈철석 FeO(OH) <b>62.9 %</b>.</li>
<li>탄소가 모자라면 산소를 다 떼지 못해 철이 그만큼 적게 나와요(<b>제한 반응물</b>).</li>
<li>철 1 t을 만들 때 나오는 이산화 탄소는 대략 1.8 t이에요. 제철이 세계 이산화 탄소 배출의 약 7 %를 차지하는 까닭이에요.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p><span class="fx-formula">산소 mol = 광석 mol × 산소 개수</span>, <span class="fx-formula">쓸 수 있는 산소 = min(광석의 산소, 넣은 탄소)</span>, <span class="fx-formula">철 = 그 비율만큼</span>, CO₂ 환산으로 배출량을 구합니다.</p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 실제 고로에서는 탄소가 먼저 <b>일산화 탄소(CO)</b>가 되어 철을 환원해요. 이 실험은 산소 1 mol당 탄소 1 mol로 단순화했고, 배출은 모두 CO₂로 환산했어요.<br>
· 광석의 순도를 100 %로 두었어요. 실제 광석에는 규산염 같은 맥석이 섞여 있어 석회석을 넣어 슬래그로 걷어내요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>수소로 산소를 떼어 내면 물만 나오는 <b>수소 환원 제철</b>이 연구되고 있어요. 같은 환원 반응이지만 배출이 달라져요.</li>
<li>고철을 전기로에서 다시 녹여 쓰면 광석을 환원하는 과정이 필요 없어 배출이 훨씬 적어요.</li>
</ul>`,
  js: `
var ORE = [
  {n:'적철석 Fe₂O₃', fe:2, o:3, M:159.7, eq:'Fe₂O₃ + 3C → 2Fe + 3CO'},
  {n:'자철석 Fe₃O₄', fe:3, o:4, M:231.5, eq:'Fe₃O₄ + 4C → 3Fe + 4CO'},
  {n:'갈철석 FeO(OH)', fe:1, o:2, M:88.9, eq:'2FeO(OH) + 3C → 2Fe + 3CO + H₂O'}
];
var MFE = 55.8, MC = 12.0, MCO2 = 44.0;
return {
  sceneHeight: 460,
  minRec: 4,
  idle: '광석 종류와 양, 넣을 탄소의 양을 정하고 <b>용광로 가열하기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 광석과 탄소의 양을 바꿔 가며 기록하세요.',
  params: [
    {key:'o', type:'seg', label:'철광석 종류', cols:3, value:0, options:ORE.map(function(x){ return x.n + '<small>Fe ' + f(x.fe * MFE / x.M * 100, 1) + ' %</small>'; })},
    {key:'m', type:'range', label:'넣은 광석의 양', min:20, max:300, step:20, value:160, fmt:function(v){ return v + ' kg'; }},
    {key:'c', type:'range', label:'넣은 코크스(탄소)의 양', min:5, max:120, step:5, value:40, fmt:function(v){ return v + ' kg'; },
      note:'광석 속 산소를 모두 떼려면 산소 1 mol당 탄소 1 mol이 필요합니다. 탄소가 모자라면 철이 덜 나옵니다. 환원으로 나온 CO가 공기 중 산소와 만나 모두 CO₂가 된다고 보고(2CO + O₂ → 2CO₂) 배출량을 <b>CO₂로 환산</b>했습니다.'}
  ],
  compute: function(p){
    var O = ORE[p.o], m = p.m, cm = p.c;
    var nOre = m / O.M * 1000;                       // mol (kg → g)
    var needO = nOre * O.o, haveC = cm / MC * 1000;
    var usedO = Math.min(needO, haveC);
    var ratio = needO > 0 ? usedO / needO : 0;
    var feMol = nOre * O.fe * ratio, feKg = feMol * MFE / 1000;
    var feMax = nOre * O.fe * MFE / 1000;
    var co2 = usedO * MCO2 / 1000, cUsed = usedO * MC / 1000;
    return {O:O, m:m, cm:cm, needC:needO * MC / 1000, usedC:cUsed, leftC:cm - cUsed,
      feKg:feKg, feMax:feMax, pct:ratio * 100, co2:co2,
      limit:haveC < needO ? '탄소' : '광석', grade:O.fe * MFE / O.M * 100,
      co2PerFe:feKg > 0 ? co2 / feKg : 0, slag:m - feKg};
  },
  draw: function(c, W, H, p, r, tau){
    var O = ORE[p.o];
    var fx = 60, fy = 80, fw = 170, fh = 210;
    // 용광로
    c.fillStyle = '#E6D5C3'; c.fillRect(fx, fy, fw, fh);
    c.strokeStyle = '#6E4A1E'; c.lineWidth = 3; c.strokeRect(fx, fy, fw, fh);
    txt(c, '용광로', fx + fw / 2, fy - 12, {align:'center', bold:true, color:'#6E4A1E'});
    // 장입물
    var lv = r ? 1 - tau * 0.55 : 1;
    c.fillStyle = '#8C7B6B'; c.fillRect(fx + 8, fy + fh - 150 * lv, fw - 16, 150 * lv);
    txt(c, '광석 + 코크스', fx + fw / 2, fy + fh - 150 * lv - 8, {align:'center', color:'#4A5868'});
    // 불꽃
    if (r && tau > 0.15){
      for (var i = 0; i < 14; i++){
        var t2 = ((tau * 2 + i * 0.07) % 1);
        c.fillStyle = 'rgba(216,142,4,' + (0.7 - 0.55 * t2) + ')';
        c.beginPath(); c.arc(fx + 20 + ((i * 29) % (fw - 40)), fy + fh - 20 - t2 * (fh - 60), 5 + (i % 3), 0, Math.PI * 2); c.fill();
      }
    }
    // 쇳물
    if (r && tau > 0.5){
      var k = (tau - 0.5) / 0.5;
      c.fillStyle = '#C8463D'; c.fillRect(fx + 10, fy + fh - 34, (fw - 20) * k, 26);
      txt(c, '쇳물', fx + fw / 2, fy + fh - 14, {align:'center', color:'#fff', bold:true});
    }
    // 배출 기체
    if (r && tau > 0.3){
      arrow(c, fx + fw / 2, fy - 20, fx + fw / 2, fy - 58, '#8C99A8', 2);
      txt(c, 'CO → (공기 중 산소와 만나) CO₂', fx + fw / 2, fy - 64, {align:'center', color:'#8C99A8'});
    }
    txt(c, O.eq, fx + fw + 30, fy + 16, {bold:true, color:'#2B5FA3'});
    txt(c, '광석 ' + p.m + ' kg + 탄소 ' + p.c + ' kg', fx + fw + 30, fy + 48, {color:'#4A5868'});
    if (!r){ txt(c, '탄소가 산소를 가져가면 철이 남아요.', fx, H - 18, {color:'#4A5868'}); return; }
    if (tau < 0.95) return;
    var yy = fy + fh + 44;
    txt(c, '나온 철 ' + f(r.feKg, 1) + ' kg (이 광석의 최대 ' + f(r.feMax, 1) + ' kg 중 ' + f(r.pct, 0) + ' %)', fx, yy,
      {bold:true, color:r.pct >= 99.5 ? '#2E9E78' : '#C8463D'});
    txt(c, '쓴 탄소 ' + f(r.usedC, 1) + ' kg · 남은 탄소 ' + f(r.leftC, 1) + ' kg · 이산화 탄소 ' + f(r.co2, 1) + ' kg', fx, yy + 30, {});
    txt(c, r.limit === '탄소' ? '탄소가 모자라 산소를 다 떼지 못했어요. 탄소를 ' + f(r.needC, 1) + ' kg까지 넣어 보세요.'
      : '탄소가 충분해 광석을 모두 환원했어요. 남은 탄소는 그대로 남아요.', fx, H - 14, {color:'#4A5868'});
  },
  stats: function(p, r){
    return [['광석', r.O.n], ['반응식', r.O.eq], ['광석 속 철의 비율', f(r.grade, 1) + ' %'],
      ['넣은 광석', r.m + ' kg'], ['넣은 탄소', r.cm + ' kg'], ['필요한 탄소', f(r.needC, 1) + ' kg', PAL[6]],
      ['제한 반응물', r.limit, r.limit === '탄소' ? PAL[4] : PAL[1]],
      ['나온 철', f(r.feKg, 1) + ' kg', PAL[1]], ['이 광석의 최대 철', f(r.feMax, 1) + ' kg'],
      ['수율', f(r.pct, 1) + ' %'], ['배출 탄소를 CO₂로 환산', f(r.co2, 1) + ' kg', PAL[4]],
      ['철 1 kg당 배출', f(r.co2PerFe, 2) + ' kg CO₂']];
  },
  columns: ['광석', 'Fe 비율 (%)', '광석 (kg)', '탄소 (kg)', '필요 탄소 (kg)', '제한 반응물', '철 (kg)', 'CO₂ (kg)'],
  record: function(p, r){
    return {oi:p.o, ore:r.O.n, grade:r.grade, m:r.m, cm:r.cm, needC:r.needC, limit:r.limit,
      fe:r.feKg, feMax:r.feMax, co2:r.co2, pct:r.pct, per:r.co2PerFe};
  },
  row: function(d){ return [d.ore, f(d.grade, 1), d.m, d.cm, f(d.needC, 1), d.limit, f(d.fe, 1), f(d.co2, 1)]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('광석의 양과 나온 철', '<canvas class="chart" id="ch1" role="img" aria-label="광석 질량과 철 질량 산점도"></canvas><ul class="readout" id="ro1"></ul><p class="ask">탄소가 충분한 기록만 보면 직선이 됩니다. 그 기울기는 무엇과 같나요?</p>') +
      card('철과 함께 나오는 이산화 탄소', '<canvas class="chart" id="ch2" role="img" aria-label="철 질량과 이산화 탄소 배출 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">철을 많이 만들수록 배출도 늘어납니다. 배출을 줄이려면 어디를 바꿔야 할까요?</p>') +
      card('광석별 비교', '<div id="ro3"></div><p class="ask">철의 비율이 높은 광석이 늘 유리할까요? 산소를 떼는 데 드는 탄소도 함께 생각해 보세요.</p>') + '</div>';
    var full = rec.filter(function(d){ return d.limit !== '탄소'; });
    var bo = groupBy(full, function(d){ return d.oi; }), s1 = [], r1 = [];
    Object.keys(bo).forEach(function(k){
      var g = bo[k], col = PAL[+k % PAL.length];
      s1.push({color:col, pts:g.map(function(d){ return {x:d.m, y:d.fe}; })});
      if (distinct(g.map(function(d){ return d.m; })) >= 2){
        var kk = fit0(g.map(function(d){ return {x:d.m, y:d.fe}; }));
        r1.push('<li>' + dot(col) + g[0].ore + ': 기울기 <b>' + f(kk * 100, 1) + ' %</b> — 광석 속 철의 비율 ' + f(g[0].grade, 1) + ' %와 같아요.</li>');
      }
    });
    var short = rec.filter(function(d){ return d.limit === '탄소'; });
    if (short.length) s1.push({color:PAL[4], pts:short.map(function(d){ return {x:d.m, y:d.fe}; })});
    drawScatter($('ch1'), {xLabel:'넣은 광석 (kg)', yLabel:'나온 철 (kg)', series:s1.length ? s1 : [{color:PAL[0], pts:[]}]});
    $('ro1').innerHTML = (r1.length ? r1.join('') : '<li>탄소를 넉넉히 넣고 광석의 양만 2가지 이상 바꿔 기록해 보세요.</li>') +
      (short.length ? '<li>' + dot(PAL[4]) + '탄소가 모자랐던 기록 ' + short.length + '개는 직선 아래로 떨어져요. 광석을 더 넣어도 철이 그만큼 늘지 않아요.</li>' : '') +
      '<li>직선의 기울기가 곧 <b>광석의 품위(철 함량)</b>예요.</li>';
    var pts2 = rec.filter(function(d){ return d.fe > 0; }).map(function(d){ return {x:d.fe, y:d.co2}; });
    drawScatter($('ch2'), {xLabel:'나온 철 (kg)', yLabel:'CO₂로 환산한 배출량 (kg)', series:[{color:PAL[4], pts:pts2}]});
    var r2 = [];
    if (pts2.length >= 2){
      var kk2 = fit0(pts2);
      r2.push('<li>기울기 <b>' + f(kk2, 2) + ' kg CO₂ / kg Fe</b> — 실제 제철소의 값(약 1.8)과 견주어 보세요.</li>');
    }
    r2.push('<li>산소를 떼는 일 자체가 탄소를 산화시키는 일이라, 이 방식에서는 배출을 0으로 만들 수 없어요.</li>');
    r2.push('<li>줄이려면 ① 고철 재활용 ② 수소로 환원 ③ 나온 이산화 탄소 포집 같은 방법을 써야 해요.</li>');
    $('ro2').innerHTML = r2.join('');
    var rows = ORE.map(function(O){
      var g = rec.filter(function(d){ return d.ore === O.n; });
      var need = O.o * MC / O.M * 100;
      return [O.n, f(O.fe * MFE / O.M * 100, 1) + ' %', f(need, 1) + ' kg', O.eq, g.length + '개'];
    });
    $('ro3').innerHTML = tableHTML(['광석', '철의 비율', '광석 100 kg당 필요한 탄소', '반응식', '내 기록'], rows, 'wrap') +
      '<p class="note">철의 비율이 높은 자철석이 유리해 보이지만, 산소가 많으면 떼는 데 드는 탄소와 배출도 함께 늘어요. 품위와 환원에 드는 비용을 같이 따져야 해요.</p>';
  }
};`
}

  ]
};
