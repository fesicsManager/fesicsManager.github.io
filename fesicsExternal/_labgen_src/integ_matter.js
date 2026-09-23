// 고1 통합과학 — Ⅱ. 물질과 규칙성 (3·4·6·7·8화) 실험 정의
module.exports = {
  folder: 'high1Integ',
  suffix: '고1 통합과학',
  principle: '과학 원리',
  anim: 1800,
  labs: [

/* ===================== 22. 주기율표의 주기성 (Matter Ep03) ===================== */
{
  file: '22_periodic_trend_lab_IntegSci1_Matter_Ep03.html',
  title: '번호 순서에 숨은 주기성',
  intro: '원소를 하나씩 골라 원자 반지름과 첫 번째 이온화 에너지를 조사합니다. 여러 원소를 기록해 원자 번호 순서로 늘어놓으면, 같은 성질이 일정한 간격으로 되풀이되는 모습이 보입니다.',
  sceneNote: '값은 실제 측정값을 반올림한 교육용 자료입니다. 비활성 기체의 전기 음성도는 보통 정의하지 않아 “—”로 두었습니다.',
  runLabel: '이 원소 조사하기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 원자가 전자가 만드는 되풀이</h3>
<p>주기율표는 원소를 <b>원자 번호 순서</b>로 늘어놓은 표예요. 같은 <b>족</b>(세로줄)에 있는 원소는 <b>원자가 전자 수가 같아서</b> 성질이 비슷하고, 같은 <b>주기</b>(가로줄)에서는 오른쪽으로 갈수록 원자핵의 전하가 커져 전자를 더 세게 당겨요. 그래서 원자 반지름은 <b>오른쪽으로 갈수록 작아지고 아래로 갈수록 커지며</b>, 이온화 에너지는 그 반대 경향을 보여요.</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>같은 주기: Na(186 pm) → Cl(99 pm)로 반지름이 줄어요. 전자 껍질 수는 같은데 핵전하가 +11에서 +17로 커지기 때문이에요.</li>
<li>같은 족: F(71 pm) → Cl(99 pm) → Br(114 pm)로 커져요. 전자 껍질이 한 층씩 늘기 때문이에요.</li>
<li>이온화 에너지는 각 주기의 <b>1족에서 가장 작고 18족에서 가장 커요</b>. Na 496 kJ/mol, Ar 1521 kJ/mol.</li>
<li>금속은 전자를 잃기 쉬워 이온화 에너지가 작고, 비금속은 전자를 얻으려 해 전기 음성도가 커요.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p>원소마다 정해진 값을 불러와 기록하고, 검증 탭에서 <span class="fx-formula">원자 번호 ↔ 이온화 에너지</span>, <span class="fx-formula">족 번호 ↔ 원자 반지름</span>으로 다시 늘어놓아 되풀이를 찾습니다.</p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 원자 반지름은 재는 방법(공유 반지름·금속 반지름·판데르발스 반지름)에 따라 값이 달라져요. 여기서는 한 가지 기준으로 통일한 어림값을 썼어요.<br>
· 4주기는 3~12족(전이 원소)을 건너뛰고 1·2·13~18족만 넣었어요. 전이 원소는 안쪽 껍질을 채워 경향이 더 완만해요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>멘델레예프는 이 되풀이를 믿고 빈칸을 남겨 두어, 아직 발견되지 않은 저마늄의 성질을 미리 예측했어요.</li>
<li>같은 1족인 Li·Na·K는 모두 물과 세게 반응하고, 같은 17족인 F·Cl·Br은 모두 1가 음이온을 만들어요.</li>
</ul>`,
  js: `
var GNAME = ['1족', '2족', '13족', '14족', '15족', '16족', '17족', '18족'];
var GNUM = [1, 2, 13, 14, 15, 16, 17, 18];
var EL = [
 [{s:'Li',n:'리튬',z:3,r:152,ie:520,en:0.98,c:'금속'},{s:'Be',n:'베릴륨',z:4,r:112,ie:900,en:1.57,c:'금속'},{s:'B',n:'붕소',z:5,r:85,ie:801,en:2.04,c:'준금속'},{s:'C',n:'탄소',z:6,r:77,ie:1086,en:2.55,c:'비금속'},{s:'N',n:'질소',z:7,r:75,ie:1402,en:3.04,c:'비금속'},{s:'O',n:'산소',z:8,r:73,ie:1314,en:3.44,c:'비금속'},{s:'F',n:'플루오린',z:9,r:71,ie:1681,en:3.98,c:'비금속'},{s:'Ne',n:'네온',z:10,r:69,ie:2081,en:null,c:'비금속'}],
 [{s:'Na',n:'나트륨',z:11,r:186,ie:496,en:0.93,c:'금속'},{s:'Mg',n:'마그네슘',z:12,r:160,ie:738,en:1.31,c:'금속'},{s:'Al',n:'알루미늄',z:13,r:143,ie:578,en:1.61,c:'금속'},{s:'Si',n:'규소',z:14,r:118,ie:787,en:1.90,c:'준금속'},{s:'P',n:'인',z:15,r:110,ie:1012,en:2.19,c:'비금속'},{s:'S',n:'황',z:16,r:103,ie:1000,en:2.58,c:'비금속'},{s:'Cl',n:'염소',z:17,r:99,ie:1251,en:3.16,c:'비금속'},{s:'Ar',n:'아르곤',z:18,r:97,ie:1521,en:null,c:'비금속'}],
 [{s:'K',n:'칼륨',z:19,r:227,ie:419,en:0.82,c:'금속'},{s:'Ca',n:'칼슘',z:20,r:197,ie:590,en:1.00,c:'금속'},{s:'Ga',n:'갈륨',z:31,r:135,ie:579,en:1.81,c:'금속'},{s:'Ge',n:'저마늄',z:32,r:122,ie:762,en:2.01,c:'준금속'},{s:'As',n:'비소',z:33,r:120,ie:947,en:2.18,c:'준금속'},{s:'Se',n:'셀레늄',z:34,r:119,ie:941,en:2.55,c:'비금속'},{s:'Br',n:'브로민',z:35,r:114,ie:1140,en:2.96,c:'비금속'},{s:'Kr',n:'크립톤',z:36,r:110,ie:1351,en:null,c:'비금속'}]
];
var CCOL = {'금속':'#A8702F', '준금속':'#7657B3', '비금속':'#2B5FA3'};
return {
  sceneHeight: 470,
  minRec: 5,
  idle: '주기와 족을 골라 <b>이 원소 조사하기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 여러 원소를 기록하세요. 같은 주기·같은 족을 고루 모으면 경향이 잘 보입니다.',
  params: [
    {key:'p', type:'seg', label:'주기 (가로줄)', cols:3, value:1, options:['2주기', '3주기', '4주기']},
    {key:'g', type:'seg', label:'족 (세로줄)', cols:4, value:0, options:GNAME,
      note:'4주기는 3~12족(전이 원소)을 뺀 1·2·13~18족만 다룹니다. 같은 족을 세로로, 같은 주기를 가로로 비교해 보세요.'}
  ],
  compute: function(p){
    var e = EL[p.p][p.g];
    return {e:e, per:p.p + 2, gnum:GNUM[p.g], gi:p.g, pi:p.p};
  },
  draw: function(c, W, H, p, r, tau){
    var cw = Math.min(64, (W - 60) / 8), ch = 50, ox = 30, oy = 56;
    txt(c, '주기율표 (1·2·13~18족)', ox, 34, {bold:true, color:'#4A5868'});
    for (var i = 0; i < 3; i++) for (var j = 0; j < 8; j++){
      var el = EL[i][j], x = ox + j * cw, y = oy + i * ch;
      var on = (i === p.p && j === p.g);
      c.fillStyle = on ? '#EAF1FA' : '#F7F9FC'; c.fillRect(x, y, cw - 4, ch - 4);
      c.strokeStyle = on ? '#2B5FA3' : '#D4DCE5'; c.lineWidth = on ? 3 : 1; c.strokeRect(x, y, cw - 4, ch - 4);
      txt(c, el.s, x + (cw - 4) / 2, y + 22, {align:'center', bold:true, color:CCOL[el.c]});
      txt(c, String(el.z), x + (cw - 4) / 2, y + 40, {align:'center', color:'#4A5868'});
    }
    var ly = oy + 3 * ch + 26;
    ['금속', '준금속', '비금속'].forEach(function(k, i){
      c.fillStyle = CCOL[k]; c.fillRect(ox + i * 110, ly - 12, 14, 14);
      txt(c, k, ox + i * 110 + 20, ly, {color:'#4A5868'});
    });
    if (!r){ txt(c, '칸을 고르고 조사 단추를 누르면 값을 재어 기록해요.', ox, H - 18, {color:'#4A5868'}); return; }
    var e = r.e, by = ly + 44, bw = Math.min(360, W - ox - 220), k = Math.min(tau / 0.8, 1);
    txt(c, e.n + ' ' + e.s + ' (원자 번호 ' + e.z + ', ' + r.per + '주기 ' + r.gnum + '족, ' + e.c + ')', ox, by - 10, {bold:true});
    txt(c, '원자 반지름', ox, by + 26, {color:'#4A5868'});
    c.fillStyle = '#E6EBF1'; c.fillRect(ox + 130, by + 12, bw, 20);
    c.fillStyle = '#2B5FA3'; c.fillRect(ox + 130, by + 12, bw * (e.r / 240) * k, 20);
    txt(c, f(e.r, 0) + ' pm', ox + 130 + bw + 10, by + 28, {bold:true, color:'#2B5FA3'});
    txt(c, '이온화 에너지', ox, by + 62, {color:'#4A5868'});
    c.fillStyle = '#E6EBF1'; c.fillRect(ox + 130, by + 48, bw, 20);
    c.fillStyle = '#C8463D'; c.fillRect(ox + 130, by + 48, bw * (e.ie / 2200) * k, 20);
    txt(c, f(e.ie, 0) + ' kJ/mol', ox + 130 + bw + 10, by + 64, {bold:true, color:'#C8463D'});
    txt(c, '전기 음성도 ' + (e.en === null ? '— (비활성 기체)' : f(e.en, 2)), ox, by + 98, {color:'#4A5868'});
  },
  stats: function(p, r){
    var e = r.e;
    return [['원소', e.n + ' (' + e.s + ')'], ['원자 번호', String(e.z)], ['자리', r.per + '주기 ' + r.gnum + '족'],
      ['원자가 전자 수', String(r.gnum <= 2 ? r.gnum : (r.gnum - 10))],
      ['원자 반지름', f(e.r, 0) + ' pm', PAL[0]], ['첫 번째 이온화 에너지', f(e.ie, 0) + ' kJ/mol', PAL[4]],
      ['전기 음성도', e.en === null ? '—' : f(e.en, 2)], ['분류', e.c]];
  },
  columns: ['원소', '원자 번호', '주기', '족', '원자가 전자', '반지름 (pm)', '이온화 E (kJ/mol)', '전기 음성도', '분류'],
  record: function(p, r){
    var e = r.e;
    return {sym:e.s, nm:e.n, z:e.z, per:r.per, g:r.gnum, gi:r.gi, pi:r.pi, ve:r.gnum <= 2 ? r.gnum : r.gnum - 10, rad:e.r, ie:e.ie, en:e.en, cls:e.c};
  },
  row: function(d){ return [d.nm + ' ' + d.sym, d.z, d.per + '주기', d.g + '족', d.ve, d.rad, d.ie, d.en === null ? '—' : f(d.en, 2), d.cls]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('원자 번호 순서와 이온화 에너지', '<canvas class="chart" id="ch1" role="img" aria-label="원자 번호와 이온화 에너지 산점도"></canvas><ul class="readout" id="ro1"></ul><p class="ask">값이 커졌다 작아졌다를 되풀이합니다. 갑자기 값이 뚝 떨어지는 자리는 주기율표의 어디인가요?</p>') +
      card('같은 주기에서 오른쪽으로 갈수록', '<canvas class="chart" id="ch2" role="img" aria-label="족과 원자 반지름 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">전자 껍질 수가 같은데 반지름이 줄어드는 까닭은 무엇일까요? 이온화 에너지와는 반대 방향인 것도 설명해 보세요.</p>') +
      card('같은 족은 성질이 닮는다', '<div id="ro3"></div><p class="ask">같은 족 원소의 원자가 전자 수를 비교해 보세요. 성질이 닮는 진짜 이유가 무엇인지 말할 수 있나요?</p>') + '</div>';
    var bp = groupBy(rec, function(d){ return d.pi; }), s1 = [], s2 = [], r1 = [], r2 = [];
    Object.keys(bp).sort(function(a,b){ return a - b; }).forEach(function(k){
      var g = bp[k], col = PAL[+k];
      s1.push({color:col, pts:g.map(function(d){ return {x:d.z, y:d.ie}; })});
      s2.push({color:col, pts:g.map(function(d){ return {x:d.g > 2 ? d.g - 10 : d.g, y:d.rad}; })});
      var mn = g.slice().sort(function(a,b){ return a.ie - b.ie; })[0], mx = g.slice().sort(function(a,b){ return b.ie - a.ie; })[0];
      r1.push('<li>' + dot(col) + (+k + 2) + '주기 기록 ' + g.length + '개 — 가장 작은 값 ' + mn.sym + ' ' + mn.ie + ' (' + mn.g + '족), 가장 큰 값 ' + mx.sym + ' ' + mx.ie + ' (' + mx.g + '족)</li>');
      if (distinct(g.map(function(d){ return d.g; })) >= 2){
        var srt = g.slice().sort(function(a,b){ return a.g - b.g; });
        r2.push('<li>' + dot(col) + (+k + 2) + '주기: ' + srt[0].sym + ' ' + srt[0].rad + ' pm → ' + srt[srt.length-1].sym + ' ' + srt[srt.length-1].rad + ' pm</li>');
      }
    });
    drawScatter($('ch1'), {xLabel:'원자 번호 Z', yLabel:'첫 번째 이온화 에너지 (kJ/mol)', tightX:true, series:s1});
    $('ro1').innerHTML = r1.join('') + '<li>각 주기에서 <b>1족이 가장 작고 18족이 가장 커요</b>. 다음 주기 1족으로 넘어가는 순간 값이 뚝 떨어지며 같은 모양이 되풀이돼요.</li>';
    drawScatter($('ch2'), {xLabel:'원자가 전자 수 (1족=1 … 18족=8)', yLabel:'원자 반지름 (pm)', tightX:true, series:s2});
    $('ro2').innerHTML = (r2.length ? r2.join('') : '<li>같은 주기에서 족을 2가지 이상 바꿔 기록해 보세요.</li>') +
      '<li>껍질 수는 그대로인데 핵전하가 커져 전자를 더 세게 당기므로 반지름이 <b>작아져요</b>. 그만큼 전자를 떼기 어려워 이온화 에너지는 <b>대체로 커져요</b>.</li>' + '<li>다만 Mg(738) → Al(578), P(1012) → S(1000)처럼 <b>중간에 값이 내려가는 예외</b>가 있어요. 전자가 어느 자리에 들어가 있느냐에 따라 떼어 내기 쉬워지기 때문이에요. 경향은 &lsquo;대체로&rsquo;이지 예외 없는 법칙이 아니에요.</li>';
    var bg = groupBy(rec, function(d){ return d.g; }), rows = [];
    Object.keys(bg).sort(function(a,b){ return a - b; }).forEach(function(k){
      var g = bg[k].slice().sort(function(a,b){ return a.z - b.z; });
      rows.push([k + '족', String(g[0].ve), g.map(function(d){ return d.sym; }).join(' → '),
        g.map(function(d){ return d.rad; }).join(' → ') + ' pm', g[0].cls]);
    });
    $('ro3').innerHTML = tableHTML(['족', '원자가 전자', '기록한 원소(번호순)', '원자 반지름', '분류'], rows, 'wrap') +
      '<p class="note">같은 족이면 원자가 전자 수가 같아 화학 반응에서 같은 방식으로 전자를 주고받아요. 그래서 성질이 닮아요.</p>';
  }
};`
},

/* ===================== 23. 옥텟과 이온 결합 (Matter Ep04) ===================== */
{
  file: '23_octet_ionic_formula_lab_IntegSci1_Matter_Ep04.html',
  title: '8을 채우려고 주고받는 전자',
  intro: '금속 원소와 비금속 원소를 하나씩 골라 반응시킵니다. 전자가 몇 개 옮겨 가는지, 어떤 화학식이 만들어지는지, 금속을 몇 g 넣으면 화합물이 몇 g 생기는지 재어 보세요.',
  sceneNote: '원자가 전자만 그렸습니다. 금속은 전자를 잃고 비금속은 얻어, 둘 다 가장 가까운 비활성 기체와 같은 전자 배치가 됩니다.',
  runLabel: '반응시키기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 옥텟 규칙과 이온 결합</h3>
<p>원자는 가장 바깥 껍질에 전자가 <b>8개(수소·헬륨은 2개)</b> 있을 때 안정해요. 그래서 원자가 전자가 적은 <b>금속</b>은 그만큼 <b>잃어</b> 양이온이 되고, 8에 가까운 <b>비금속</b>은 모자란 수만큼 <b>얻어</b> 음이온이 돼요. 두 이온이 전기적 인력으로 붙는 것이 <b>이온 결합</b>이고, 화합물 전체의 전하는 0이어야 하므로 이온 수의 비가 자동으로 정해져요.</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>Na는 1족이라 전자 1개를 잃어 Na⁺(네온과 같은 배치), Cl은 17족이라 1개를 얻어 Cl⁻(아르곤과 같은 배치) → <b>NaCl</b>.</li>
<li>Mg²⁺와 Cl⁻은 전하를 맞추려면 1 : 2 → <b>MgCl₂</b>. Al³⁺와 O²⁻은 2 : 3 → <b>Al₂O₃</b>.</li>
<li>전하 맞추기는 <span class="fx-formula">x × (양이온 전하) = y × (음이온 전하)</span>를 푸는 일이고, 결과는 전하를 서로 바꿔 쓴 뒤 약분한 값이에요.</li>
<li>질량은 화학식량으로 계산해요. Mg 24.3 g이 모두 반응하면 MgCl₂ 95.3 g이 생기고, 필요한 Cl₂는 71.0 g이에요.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p><span class="fx-formula">첨자 = 상대 전하 ÷ 최대공약수</span>, <span class="fx-formula">n(금속) = m ÷ M</span>, <span class="fx-formula">화합물 질량 = (n ÷ x) × 화학식량</span>, 질량 보존으로 필요한 비금속 질량을 구합니다.</p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 반응이 <b>100 % 진행된다</b>고 봤어요. 실제 실험에서는 금속 표면의 산화막, 날아가는 기체, 덜 반응한 알갱이 때문에 수율이 100 %보다 작아요.<br>
· 옥텟 규칙은 2·3주기 대표 원소에서 잘 맞아요. 전이 원소나 3주기 이후의 일부 화합물은 예외가 있어요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>소금(NaCl)은 물에 녹으면 Na⁺와 Cl⁻로 흩어져 전류가 흐르게 해요. 링거액과 땀에 들어 있는 것도 이 이온이에요.</li>
<li>알루미늄 창틀의 표면은 Al₂O₃ 막이라 속까지 녹슬지 않아요.</li>
</ul>`,
  js: `
var MET = [{s:'Na',n:'나트륨',g:1,ch:1,M:23.0,ne:'네온 Ne'},{s:'Mg',n:'마그네슘',g:2,ch:2,M:24.3,ne:'네온 Ne'},
           {s:'Al',n:'알루미늄',g:13,ch:3,M:27.0,ne:'네온 Ne'},{s:'K',n:'칼륨',g:1,ch:1,M:39.1,ne:'아르곤 Ar'}];
var NON = [{s:'F',n:'플루오린',g:17,ch:1,M:19.0,ne:'네온 Ne'},{s:'Cl',n:'염소',g:17,ch:1,M:35.5,ne:'아르곤 Ar'},
           {s:'O',n:'산소',g:16,ch:2,M:16.0,ne:'네온 Ne'},{s:'S',n:'황',g:16,ch:2,M:32.1,ne:'아르곤 Ar'}];
var SUB = ['', '', '₂', '₃', '₄'];
function gcd(a, b){ return b ? gcd(b, a % b) : a; }
return {
  sceneHeight: 450,
  minRec: 4,
  idle: '금속과 비금속, 금속의 질량을 정하고 <b>반응시키기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 원소 짝과 금속 질량을 바꿔 가며 기록하세요.',
  params: [
    {key:'a', type:'seg', label:'금속 원소', cols:4, value:1, options:MET.map(function(x){ return x.s + '<small>' + x.g + '족</small>'; })},
    {key:'b', type:'seg', label:'비금속 원소', cols:4, value:1, options:NON.map(function(x){ return x.s + '<small>' + x.g + '족</small>'; })},
    {key:'m', type:'range', label:'넣은 금속의 질량', min:1, max:30, step:1, value:10, fmt:function(v){ return v + ' g'; },
      note:'금속이 모두 반응하고 비금속은 충분히 있다고 봅니다. 화합물의 전하 합은 항상 0이어야 합니다.'}
  ],
  compute: function(p){
    var A = MET[p.a], B = NON[p.b], gg = gcd(A.ch, B.ch);
    var x = B.ch / gg, y = A.ch / gg;                 // AxBy
    var fw = x * A.M + y * B.M;
    var nA = p.m / A.M, nUnit = nA / x;
    var mB = nUnit * y * B.M, mP = nUnit * fw;
    var form = A.s + SUB[x] + B.s + SUB[y];
    return {A:A, B:B, x:x, y:y, fw:fw, form:form, mA:p.m, nA:nA, nUnit:nUnit, mB:mB, mP:mP,
      moved:x * A.ch, gg:gg};
  },
  draw: function(c, W, H, p, r, tau){
    var A = MET[p.a], B = NON[p.b];
    var cxA = Math.max(130, W * 0.24), cxB = Math.min(W - 130, W * 0.72), cy = 170, R = 58;
    function atom(x, sym, col, ve, lost){
      c.strokeStyle = col; c.lineWidth = 2; c.beginPath(); c.arc(x, cy, R, 0, Math.PI * 2); c.stroke();
      c.fillStyle = '#fff'; c.beginPath(); c.arc(x, cy, 26, 0, Math.PI * 2); c.fill();
      c.strokeStyle = col; c.beginPath(); c.arc(x, cy, 26, 0, Math.PI * 2); c.stroke();
      txt(c, sym, x, cy + 7, {align:'center', bold:true, color:col});
      for (var i = 0; i < ve; i++){
        var ang = -Math.PI / 2 + i * 2 * Math.PI / Math.max(ve, 1);
        var fade = (lost && i >= ve - lost) ? 0.18 : 1;
        c.globalAlpha = fade; c.fillStyle = '#D98E04';
        c.beginPath(); c.arc(x + R * Math.cos(ang), cy + R * Math.sin(ang), 7, 0, Math.PI * 2); c.fill();
        c.globalAlpha = 1;
      }
    }
    var k = r ? tau : 0;
    var veA = A.g <= 2 ? A.g : A.g - 10, veB = B.g - 10;
    atom(cxA, A.s + (k > 0.9 ? (A.ch === 1 ? '⁺' : A.ch === 2 ? '²⁺' : '³⁺') : ''), '#A8702F', veA, k > 0.5 ? A.ch : 0);
    atom(cxB, B.s + (k > 0.9 ? (B.ch === 1 ? '⁻' : '²⁻') : ''), '#2B5FA3', veB + (k > 0.5 ? B.ch : 0), 0);
    if (k > 0.1 && k < 0.95){
      for (var j = 0; j < A.ch; j++){
        var t = Math.min(1, Math.max(0, (k - 0.1 - j * 0.08) / 0.5));
        c.fillStyle = '#D98E04';
        c.beginPath(); c.arc(cxA + R + (cxB - cxA - 2 * R) * t, cy - 80 + j * 16, 7, 0, Math.PI * 2); c.fill();
      }
      txt(c, '전자 ' + A.ch + '개 이동', (cxA + cxB) / 2, cy - 96, {align:'center', color:'#D98E04', bold:true});
    }
    txt(c, A.n + ' (' + A.g + '족, 원자가 전자 ' + veA + '개)', cxA, cy + R + 30, {align:'center', color:'#4A5868'});
    txt(c, B.n + ' (' + B.g + '족, 원자가 전자 ' + veB + '개)', cxB, cy + R + 30, {align:'center', color:'#4A5868'});
    if (!r || tau < 0.95){ if (!r) txt(c, '주황 점이 원자가 전자예요. 금속은 잃고 비금속은 얻어요.', 16, H - 18, {color:'#4A5868'}); return; }
    var yy = cy + R + 76;
    txt(c, '생긴 화합물: ' + r.form + ' (화학식량 ' + f(r.fw, 1) + ')', 16, yy, {bold:true, color:'#2E9E78'});
    txt(c, '전하 맞추기: (' + sgn(r.A.ch, 0) + ') × ' + r.x + ' + (' + sgn(-r.B.ch, 0) + ') × ' + r.y + ' = 0', 16, yy + 30, {});
    txt(c, r.A.s + ' ' + f(r.mA, 1) + ' g + ' + r.B.s + ' ' + f(r.mB, 1) + ' g → ' + r.form + ' ' + f(r.mP, 1) + ' g', 16, yy + 60, {bold:true, color:'#2B5FA3'});
    txt(c, '두 이온 모두 ' + r.A.ne + ' · ' + r.B.ne + '과 같은 전자 배치가 됐어요.', 16, H - 14, {color:'#4A5868'});
  },
  stats: function(p, r){
    return [['금속', r.A.n + ' ' + r.A.s + ' (' + r.A.g + '족)'], ['비금속', r.B.n + ' ' + r.B.s + ' (' + r.B.g + '족)'],
      ['만든 이온', r.A.s + (r.A.ch === 1 ? '⁺' : r.A.ch === 2 ? '²⁺' : '³⁺') + ' + ' + r.B.s + (r.B.ch === 1 ? '⁻' : '²⁻'), PAL[6]],
      ['화학식', r.form, PAL[1]], ['이온 수의 비', r.x + ' : ' + r.y],
      ['화학식량', f(r.fw, 1)], ['옮겨 간 전자 (화학식 단위당)', r.moved + '개'],
      ['넣은 금속', f(r.mA, 1) + ' g = ' + f(r.nA, 3) + ' mol'],
      ['필요한 비금속', f(r.mB, 1) + ' g', PAL[0]], ['생긴 화합물', f(r.mP, 1) + ' g', PAL[4]],
      ['전자 배치', r.A.s + (r.A.ch === 1 ? '⁺' : r.A.ch === 2 ? '²⁺' : '³⁺') + '는 ' + r.A.ne + ', ' + r.B.s + (r.B.ch === 1 ? '⁻' : '²⁻') + '는 ' + r.B.ne + '와 같음']];
  },
  columns: ['금속', '비금속', '양이온', '음이온', '화학식', '화학식량', '금속 (g)', '비금속 (g)', '화합물 (g)'],
  record: function(p, r){
    return {am:r.A.s, bm:r.B.s, ach:r.A.ch, bch:r.B.ch, x:r.x, y:r.y, form:r.form, fw:r.fw,
      mA:r.mA, mB:r.mB, mP:r.mP, aM:r.A.M, ag:r.A.g, bg:r.B.g, ave:r.A.g <= 2 ? r.A.g : r.A.g - 10, bve:r.B.g - 10};
  },
  row: function(d){ return [d.am, d.bm, d.am + (d.ach === 1 ? '⁺' : d.ach === 2 ? '²⁺' : '³⁺'), d.bm + (d.bch === 1 ? '⁻' : '²⁻'),
    d.form, f(d.fw, 1), f(d.mA, 1), f(d.mB, 1), f(d.mP, 1)]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('넣은 금속과 생긴 화합물', '<canvas class="chart" id="ch1" role="img" aria-label="금속 질량과 화합물 질량 산점도"></canvas><ul class="readout" id="ro1"></ul><p class="ask">각 직선의 기울기가 다른 까닭은 무엇일까요? 화학식량과 어떻게 연결되나요?</p>') +
      card('족 번호와 이온의 전하', '<canvas class="chart" id="ch2" role="img" aria-label="원자가 전자 수와 이온 전하 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">1족은 +1, 2족은 +2, 17족은 −1, 16족은 −2입니다. 8에서 얼마나 떨어져 있는지로 설명할 수 있나요?</p>') +
      card('전하를 맞춘 화학식', '<div id="ro3"></div><p class="ask">전하를 서로 바꿔 아래첨자로 쓰면 화학식이 됩니다. 약분이 필요한 짝은 어떤 경우인가요?</p>') + '</div>';
    var bf = groupBy(rec, function(d){ return d.form; }), s1 = [], r1 = [], ci = 0;
    Object.keys(bf).forEach(function(k){
      var g = bf[k], col = PAL[ci++ % PAL.length];
      s1.push({color:col, pts:g.map(function(d){ return {x:d.mA, y:d.mP}; })});
      if (distinct(g.map(function(d){ return d.mA; })) >= 2){
        var kk = fit0(g.map(function(d){ return {x:d.mA, y:d.mP}; }));
        r1.push('<li>' + dot(col) + k + ': 기울기 <b>' + f(kk, 2) + '</b> = 화학식량 ' + f(g[0].fw, 1) + ' ÷ (' + g[0].x + ' × ' + f(g[0].aM, 1) + ') = ' + f(g[0].fw / (g[0].x * g[0].aM), 2) + '</li>');
      }
    });
    drawScatter($('ch1'), {xLabel:'넣은 금속의 질량 (g)', yLabel:'생긴 화합물의 질량 (g)', series:s1});
    $('ro1').innerHTML = (r1.length ? r1.join('') : '<li>같은 원소 짝에서 금속 질량만 2가지 이상 바꿔 기록해 보세요.</li>') +
      '<li>모두 원점을 지나는 직선이에요. 반응하는 질량비가 <b>일정</b>하다는 뜻이에요(일정 성분비).</li>';
    var pa = [], pb = [], seen = {};
    rec.forEach(function(d){
      if (!seen['a' + d.am]){ seen['a' + d.am] = 1; pa.push({x:d.ave, y:d.ach}); }
      if (!seen['b' + d.bm]){ seen['b' + d.bm] = 1; pb.push({x:d.bve, y:-d.bch}); }
    });
    drawScatter($('ch2'), {xLabel:'원자가 전자 수', yLabel:'이온의 전하', tightX:true,
      series:[{color:PAL[2], pts:pa}, {color:PAL[0], pts:pb}]});
    $('ro2').innerHTML = '<li>' + dot(PAL[2]) + '금속: 원자가 전자를 <b>모두 잃어</b> 전하 = 원자가 전자 수예요.</li>' +
      '<li>' + dot(PAL[0]) + '비금속: 8에서 모자란 수만큼 <b>얻어</b> 전하 = −(8 − 원자가 전자 수)예요.</li>' +
      '<li>둘 다 결과적으로 가장 가까운 비활성 기체와 같은 전자 배치가 돼요.</li>';
    var seen2 = {}, rows = [];
    rec.forEach(function(d){ if (seen2[d.form]) return; seen2[d.form] = 1;
      rows.push([d.am + (d.ach === 1 ? '⁺' : d.ach === 2 ? '²⁺' : '³⁺'), d.bm + (d.bch === 1 ? '⁻' : '²⁻'),
        d.ach + ' : ' + d.bch, d.x + ' : ' + d.y, d.form, f(d.fw, 1)]); });
    $('ro3').innerHTML = tableHTML(['양이온', '음이온', '전하 크기의 비', '이온 수의 비', '화학식', '화학식량'], rows, 'center') +
      '<p class="note">예: Mg²⁺와 O²⁻은 전하를 바꿔 쓰면 Mg₂O₂지만 2로 약분해 MgO가 돼요.</p>';
  }
};`
},

/* ===================== 24. 규산염 사면체 (Matter Ep06) ===================== */
{
  file: '24_silicate_tetrahedra_lab_IntegSci1_Matter_Ep06.html',
  title: '사면체를 몇 개씩 이어 붙일까',
  intro: '규산염 사면체(SiO₄)가 산소를 몇 개 나눠 쓰느냐에 따라 광물의 구조와 화학식이 달라집니다. 공유하는 산소 수를 바꿔 가며 규소와 산소의 개수 비, 그리고 필요한 양이온 수를 세어 보세요.',
  sceneNote: '삼각형 하나가 SiO₄ 사면체 하나입니다. 빨간 점은 이웃과 함께 쓰는 산소, 파란 점은 혼자 쓰는 산소입니다.',
  runLabel: '구조 만들기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — SiO₄ 사면체의 연결 방식</h3>
<p>지각을 이루는 광물의 대부분은 <b>규산염 광물</b>이고, 그 기본 단위는 규소 1개를 산소 4개가 둘러싼 <b>SiO₄ 사면체</b>예요. 사면체는 꼭짓점의 산소를 이웃과 <b>나눠 쓰면서</b> 이어지는데, 몇 개를 나눠 쓰느냐에 따라 독립형·단사슬·복사슬·판상·망상 구조가 되고 산소와 규소의 개수 비가 달라져요. 구조가 달라지면 쪼개지는 방향과 단단함도 달라져요.</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>산소 하나를 둘이 나눠 쓰면 규소 1개 몫은 ½개예요. 그래서 규소 1개당 산소 수는 <span class="fx-formula">4 − s ÷ 2</span> (s = 공유 산소 수)예요.</li>
<li>s = 0 → SiO₄ (감람석), s = 2 → SiO₃ (휘석), s = 2.5 → Si₄O₁₁ (각섬석), s = 3 → Si₂O₅ (흑운모), s = 4 → SiO₂ (석영).</li>
<li>전하: Si⁴⁺ 1개 + O²⁻ (4 − s/2)개 → 덩어리의 전하는 <span class="fx-formula">4 − 2(4 − s÷2) = s − 4</span>. 즉 규소 1개당 <b>(4 − s)</b>만큼 음전하가 남아요.</li>
<li>남은 음전하는 Mg²⁺·Fe²⁺ 같은 양이온이 메워요. 규소 1개당 2가 양이온 <span class="fx-formula">(4 − s) ÷ 2</span>개가 필요해요.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p><span class="fx-formula">O ÷ Si = 4 − s ÷ 2</span>, <span class="fx-formula">남은 음전하 = 4 − s</span>, <span class="fx-formula">2가 양이온 수 = (4 − s) ÷ 2</span>, 사면체 n개의 산소 수 = n × (4 − s ÷ 2)</p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 사면체를 평면 삼각형으로 그렸어요. 실제 SiO₄는 <b>입체</b>이고, 산소는 사면체의 네 꼭짓점에 있어요.<br>
· 사면체 n개의 산소 수를 n × (4 − s/2)로 계산했어요. 이는 사슬이나 판이 <b>충분히 길 때</b> 맞는 값이고, 짧은 조각에서는 끝부분 때문에 조금 달라요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>흑운모가 종잇장처럼 얇게 벗겨지는 것은 판과 판 사이가 약하기 때문이고, 석영이 특정 방향으로 쪼개지지 않는 것은 사방으로 다 이어져 있기 때문이에요.</li>
<li>석면(각섬석류)은 사슬 구조라 가늘고 긴 섬유로 쪼개져 폐에 박히기 쉬워 지금은 사용이 금지됐어요.</li>
</ul>`,
  js: `
var STR = [
  {s:0,   n:'독립형',  m:'감람석',   c:'쪼개짐이 뚜렷하지 않음'},
  {s:2,   n:'단사슬형', m:'휘석',    c:'두 방향 쪼개짐 (약 87°·93°)'},
  {s:2.5, n:'복사슬형', m:'각섬석',   c:'두 방향 쪼개짐 (약 56°·124°)'},
  {s:3,   n:'판상형',  m:'흑운모',   c:'한 방향으로 얇게 벗겨짐'},
  {s:4,   n:'망상형',  m:'석영',    c:'쪼개짐 없이 깨짐'}
];
var CAT = [{s:'Mg²⁺',n:'마그네슘',M:24.3,el:'Mg'},{s:'Fe²⁺',n:'철',M:55.8,el:'Fe'},{s:'Ca²⁺',n:'칼슘',M:40.1,el:'Ca'}];
var FORM = ['SiO₄', 'SiO₃', 'Si₄O₁₁', 'Si₂O₅', 'SiO₂'];        // 규산염 골격(음이온)의 단위식
var FULL = ['M₂SiO₄', 'MSiO₃', 'M₃Si₄O₁₁', 'MSi₂O₅', 'SiO₂'];   // 양이온까지 넣어 전하를 맞춘 단순 화학식
return {
  sceneHeight: 470,
  minRec: 4,
  idle: '연결 방식과 사면체 개수를 정하고 <b>구조 만들기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 연결 방식을 여러 가지로 바꿔 기록하세요.',
  params: [
    {key:'k', type:'seg', label:'사면체 연결 방식', cols:3, value:0, options:STR.map(function(x){ return x.n + '<small>공유 산소 ' + f(x.s, 1) + '개</small>'; })},
    {key:'c', type:'seg', label:'전하를 메우는 양이온', cols:3, value:0, options:CAT.map(function(x){ return x.s + '<small>' + x.n + '</small>'; })},
    {key:'n', type:'range', label:'사면체 개수', min:2, max:16, step:2, value:6, fmt:function(v){ return v + '개'; },
      note:'사면체가 산소를 나눠 쓸수록 규소 1개가 차지하는 산소 수가 줄어듭니다. SiO₄·SiO₃ 같은 식은 <b>규산염 골격(음이온)의 단위식</b>이고, 양이온까지 넣어야 광물의 화학식이 됩니다. 실제 광물은 여러 양이온과 OH가 섞여 이보다 복잡합니다.'}
  ],
  compute: function(p){
    var S = STR[p.k], C = CAT[p.c], n = p.n;
    var oPer = 4 - S.s / 2, neg = 4 - S.s, cat = neg / 2;
    var totO = n * oPer, totCat = n * cat;
    var mass = n * (28.1 + oPer * 16.0) + totCat * C.M;
    return {S:S, C:C, n:n, oPer:oPer, neg:neg, cat:cat, totO:totO, totCat:totCat,
      form:FORM[p.k], full:FULL[p.k].replace('M', C.el), mass:mass, share:S.s};
  },
  draw: function(c, W, H, p, r, tau){
    var S = STR[p.k], n = p.n, k = r ? tau : 1;
    var show = Math.max(1, Math.round(n * k));
    var oy = 130;
    var cols = S.s >= 3 ? Math.ceil(Math.sqrt(n)) : n;
    var spread = S.s >= 3 ? 0.98 : S.s >= 2 ? 0.62 : 1.5;
    var size = Math.min(48, (W - 110) / Math.max(1, (cols - 1) * spread + 1.2));
    var stepX = size * spread, startX = 40;
    function tri(x, y, up, idx){
      c.beginPath();
      if (up){ c.moveTo(x, y - size * 0.6); c.lineTo(x - size * 0.58, y + size * 0.4); c.lineTo(x + size * 0.58, y + size * 0.4); }
      else { c.moveTo(x, y + size * 0.6); c.lineTo(x - size * 0.58, y - size * 0.4); c.lineTo(x + size * 0.58, y - size * 0.4); }
      c.closePath();
      c.fillStyle = 'rgba(43,95,163,.13)'; c.fill();
      c.strokeStyle = '#2B5FA3'; c.lineWidth = 2; c.stroke();
      c.fillStyle = '#2B5FA3'; c.beginPath(); c.arc(x, y, 5, 0, Math.PI * 2); c.fill();
      txt(c, 'Si', x + 8, y + 5, {color:'#2B5FA3'});
    }
    var pos = [];
    for (var i = 0; i < show; i++){
      var gx, gy;
      if (S.s >= 3){ gx = startX + (i % cols) * stepX + 30; gy = oy + Math.floor(i / cols) * (size * 0.86) + 20; }
      else if (S.s >= 2){ gx = startX + i * stepX + 30; gy = oy + (i % 2) * 18 + 40; }
      else { gx = startX + i * stepX + 30; gy = oy + 40; }
      pos.push({x:gx, y:gy});
      tri(gx, gy, i % 2 === 0, i);
    }
    // 공유 산소 표시
    for (var j = 0; j < pos.length; j++){
      var shared = Math.min(S.s, 4);
      c.fillStyle = '#C8463D';
      if (S.s > 0 && j < pos.length - 1){
        var mx = (pos[j].x + pos[j + 1].x) / 2, my = (pos[j].y + pos[j + 1].y) / 2;
        c.beginPath(); c.arc(mx, my, 6, 0, Math.PI * 2); c.fill();
      }
      if (S.s >= 3 && j + cols < pos.length){
        var mx2 = (pos[j].x + pos[j + cols].x) / 2, my2 = (pos[j].y + pos[j + cols].y) / 2;
        c.beginPath(); c.arc(mx2, my2, 6, 0, Math.PI * 2); c.fill();
      }
    }
    txt(c, S.n + ' (' + S.m + ') · 사면체 ' + show + '개', 16, 40, {bold:true});
    c.fillStyle = '#C8463D'; c.beginPath(); c.arc(24, 66, 6, 0, Math.PI * 2); c.fill();
    txt(c, '나눠 쓰는 산소', 36, 72, {color:'#4A5868'});
    c.fillStyle = '#2B5FA3'; c.beginPath(); c.arc(184, 66, 6, 0, Math.PI * 2); c.fill();
    txt(c, '규소', 196, 72, {color:'#4A5868'});
    if (!r) return;
    var yy = H - 116;
    txt(c, '규소 1개가 차지하는 산소 = 4 − ' + f(r.share, 1) + ' ÷ 2 = ' + f(r.oPer, 2) + '개 → 골격 ' + r.form + ' · 전하까지 맞추면 ' + r.full, 16, yy, {bold:true, color:'#2B5FA3'});
    txt(c, '사면체 ' + r.n + '개 → 규소 ' + r.n + '개 · 산소 ' + f(r.totO, 1) + '개', 16, yy + 30, {});
    txt(c, '남은 음전하 규소 1개당 ' + f(r.neg, 1) + ' → ' + r.C.s + ' ' + f(r.cat, 2) + '개 필요 (전체 ' + f(r.totCat, 1) + '개)', 16, yy + 60,
      {bold:true, color:'#2E9E78'});
    txt(c, r.S.c, 16, H - 14, {color:'#4A5868'});
  },
  stats: function(p, r){
    return [['연결 방식', r.S.n], ['대표 광물(계열)', r.S.m], ['공유하는 산소 수 s', f(r.share, 1) + '개'],
      ['규소 1개당 산소 수', f(r.oPer, 2) + '개', PAL[0]], ['규산염 골격의 Si : O 비 (단위식)', r.form, PAL[1]],
      ['사면체 개수', r.n + '개'], ['전체 산소 수', f(r.totO, 1) + '개'],
      ['규소 1개당 남은 음전하', f(r.neg, 1)], ['필요한 ' + r.C.s + ' (규소 1개당)', f(r.cat, 2) + '개', PAL[4]],
      ['전체 ' + r.C.s + ' 수', f(r.totCat, 1) + '개'], ['전하를 맞춘 단순 화학식', r.full, PAL[2]], ['쪼개짐', r.S.c]];
  },
  columns: ['연결 방식', '대표 광물(계열)', '공유 산소 s', 'O ÷ Si', '골격 단위식', '전하 맞춘 식', '사면체 수', '양이온 수 / Si'],
  record: function(p, r){
    return {nm:r.S.n, mi:r.S.m, s:r.share, oPer:r.oPer, form:r.form, full:r.full, n:r.n, cat:r.C.s, catN:r.cat, neg:r.neg, totO:r.totO, cl:r.S.c};
  },
  row: function(d){ return [d.nm, d.mi, f(d.s, 1), f(d.oPer, 2), d.form, d.full, d.n, f(d.catN, 2)]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('공유 산소 수와 O : Si 비', '<canvas class="chart" id="ch1" role="img" aria-label="공유 산소 수와 산소 대 규소 비 산점도"></canvas><ul class="readout" id="ro1"></ul><p class="ask">산소 하나를 둘이 나눠 쓰면 규소 1개 몫은 몇 개일까요? 기울기가 −0.5인 까닭을 설명해 보세요.</p>') +
      card('남은 음전하와 필요한 양이온', '<canvas class="chart" id="ch2" role="img" aria-label="공유 산소 수와 필요한 양이온 수 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">석영(s = 4)에는 왜 다른 양이온이 거의 들어가지 않을까요?</p>') +
      card('구조가 정하는 쪼개짐', '<div id="ro3"></div><p class="ask">흑운모는 얇게 벗겨지고 석영은 그렇지 않습니다. 사면체 연결 방식으로 설명해 보세요.</p>') + '</div>';
    var pts1 = rec.map(function(d){ return {x:d.s, y:d.oPer}; });
    drawScatter($('ch1'), {xLabel:'공유하는 산소 수 s', yLabel:'규소 1개당 산소 수 (O ÷ Si)', tightX:true, tightY:true,
      series:[{color:PAL[0], pts:pts1}]});
    var r1 = [];
    if (distinct(rec.map(function(d){ return d.s; })) >= 2){
      var L = linfit(pts1);
      r1.push('<li>직선의 기울기 <b>' + f(L.k, 2) + '</b>, 세로축 절편 <b>' + f(L.b, 2) + '</b> — 식 O ÷ Si = 4 − s ÷ 2와 같아요.</li>');
    } else r1.push('<li>연결 방식을 2가지 이상 바꿔 기록해 보세요.</li>');
    r1.push('<li>s = 0이면 SiO₄, s = 4이면 SiO₂. 다 이어 붙일수록 산소가 <b>절반씩</b> 줄어요.</li>');
    $('ro1').innerHTML = r1.join('');
    var bc = groupBy(rec, function(d){ return d.cat; }), s2 = [], ci = 0, leg = [];
    Object.keys(bc).forEach(function(k){
      var col = PAL[ci++ % PAL.length];
      s2.push({color:col, pts:bc[k].map(function(d){ return {x:d.s, y:d.catN}; })});
      leg.push('<li>' + dot(col) + k + ' 기록 ' + bc[k].length + '개</li>');
    });
    drawScatter($('ch2'), {xLabel:'공유하는 산소 수 s', yLabel:'규소 1개당 2가 양이온 수', tightX:true, series:s2});
    $('ro2').innerHTML = leg.join('') +
      '<li>필요한 양이온 수 = (4 − s) ÷ 2예요. s가 커질수록 <b>남는 음전하가 줄어</b> 양이온이 덜 필요해요.</li>' +
      '<li>s = 4인 석영은 남는 음전하가 0이라 SiO₂만으로 완결돼요.</li>';
    var seen = {}, rows = [];
    rec.forEach(function(d){ if (seen[d.nm]) return; seen[d.nm] = 1; rows.push([d.nm, d.mi, f(d.s, 1), d.form, d.full, d.cl]); });
    rows.sort(function(a, b){ return parseFloat(a[2]) - parseFloat(b[2]); });
    $('ro3').innerHTML = tableHTML(['연결 방식', '대표 광물(계열)', '공유 산소 s', '골격 단위식', '전하 맞춘 식', '쪼개짐'], rows, 'wrap') +
      '<p class="note">사슬과 판 사이는 약한 결합이라 그 방향으로 잘 쪼개지고, 사방으로 이어진 망상 구조는 쪼개지는 방향이 없어요.</p>';
  }
};`
},

/* ===================== 25. 반도체와 도핑 (Matter Ep07) ===================== */
{
  file: '25_semiconductor_doping_lab_IntegSci1_Matter_Ep07.html',
  title: '불순물을 넣으면 더 잘 통한다',
  intro: '구리·규소·고무에 전압을 걸어 전류를 잽니다. 순수한 규소에 인이나 붕소를 아주 조금 섞고 온도도 바꿔 가며, 도체·반도체·절연체가 어떻게 다르게 반응하는지 확인해 보세요.',
  sceneNote: '길이 1 cm, 단면적 1 cm²인 막대에 1.5 V를 걸었다고 가정했습니다. 캐리어 농도와 이동도는 교육용 어림값입니다.',
  runLabel: '전류 재기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 자유 전자의 수가 전도성을 정한다</h3>
<p>전기가 잘 통하는지는 <b>움직일 수 있는 전하(캐리어)가 얼마나 많은가</b>로 정해져요. 금속은 자유 전자가 원자 수만큼 많아 잘 통하고, 절연체는 거의 없어요. 규소 같은 <b>반도체</b>는 그 중간인데, 여기에 원자가 전자가 하나 많은 <b>인(15족)</b>을 섞으면 남는 전자가 생겨 n형, 하나 적은 <b>붕소(13족)</b>를 섞으면 전자가 빈 자리(양공)가 생겨 p형이 돼요. 백만 분의 1 수준만 넣어도 캐리어가 수백만 배로 늘어요.</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>전도도 <span class="fx-formula">σ = q × n × μ</span> (q = 1.6 × 10⁻¹⁹ C, n = 캐리어 농도, μ = 이동도). 저항 <span class="fx-formula">R = 1 ÷ σ × L ÷ A</span>.</li>
<li>규소 1 cm³에는 원자가 약 5 × 10²² 개 있어요. 1 ppm 도핑이면 캐리어가 5 × 10¹⁶ 개/cm³ — 순수 규소(약 10¹⁰)의 <b>500만 배</b>예요.</li>
<li>온도를 올리면 금속은 원자의 진동이 심해져 저항이 <b>커지고</b>, 반도체는 전자가 더 많이 튀어나와 저항이 <b>작아져요</b>.</li>
<li>같은 농도라도 n형(전자, μ ≈ 1350)이 p형(양공, μ ≈ 480)보다 잘 통해요.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p><span class="fx-formula">n = 도핑 농도(ppm) × 5 × 10¹⁶</span>, <span class="fx-formula">σ = 1.6×10⁻¹⁹ × n × μ</span>, <span class="fx-formula">R = 1 ÷ σ</span> (L = 1 cm, A = 1 cm²), <span class="fx-formula">I = 1.5 ÷ R</span></p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 도핑한 원자가 모두 캐리어를 내놓는다고 봤어요. 실제로는 저온에서 일부만 활성화되고, 농도가 매우 높으면 이동도가 떨어져요.<br>
· 금속의 온도 계수는 상온 근처에서만 직선에 가깝고, 순수 규소의 캐리어 농도는 온도에 지수적으로 변해 여기서 쓴 어림식보다 훨씬 가파르게 바뀌어요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>n형과 p형을 붙이면 한쪽으로만 전류가 흐르는 다이오드가 되고, 셋을 겹치면 트랜지스터가 돼요. 스마트폰 하나에 이 스위치가 수백억 개 들어 있어요.</li>
<li>태양 전지, LED, 온도 센서도 모두 도핑한 반도체로 만들어요.</li>
</ul>`,
  js: `
var Q = 1.6e-19, V = 1.5;
var MAT = [{n:'구리',t:'도체',metal:true,r300:1.7e-6},{n:'규소',t:'반도체',metal:false},{n:'고무',t:'절연체',metal:false,ins:true}];
var DOP = [{n:'없음',mu:1350,k:0},{n:'인 P (15족)',mu:1350,k:1,type:'n형 (전자)'},{n:'붕소 B (13족)',mu:480,k:1,type:'p형 (양공)'}];
var PPM = [0.01, 0.1, 1, 10];
function siIntrinsic(T){ return 1.0e10 * Math.pow(T / 300, 1.5) * Math.exp(-6496 * (1 / T - 1 / 300)); }
return {
  sceneHeight: 460,
  minRec: 4,
  idle: '재료와 도핑, 온도를 정하고 <b>전류 재기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 도핑 농도와 온도를 바꿔 가며 기록하세요.',
  params: [
    {key:'m', type:'seg', label:'막대 재료', cols:3, value:1, options:MAT.map(function(x){ return x.n + '<small>' + x.t + '</small>'; })},
    {key:'d', type:'seg', label:'섞는 원소 (규소일 때만)', cols:3, value:1, options:DOP.map(function(x){ return x.n; })},
    {key:'c', type:'seg', label:'도핑 농도', cols:4, value:2, options:PPM.map(function(v){ return v + ' ppm'; })},
    {key:'T', type:'range', label:'온도', min:200, max:500, step:20, value:300, fmt:function(v){ return v + ' K (' + f(v - 273, 0) + ' °C)'; },
      note:'구리와 고무를 고르면 도핑 설정은 계산에 쓰이지 않습니다. 규소 원자는 1 cm³에 약 5 × 10²² 개 있습니다. 전원의 내부 저항과 접촉 저항을 0으로 둔 <b>이론값</b>이라 도체에서는 전류가 실제로는 나올 수 없을 만큼 크게 표시됩니다.'}
  ],
  compute: function(p){
    var M = MAT[p.m], D = DOP[p.d], ppm = PPM[p.c], T = p.T, n, mu, sigma, kind;
    if (M.metal){
      var rho = M.r300 * (1 + 0.0039 * (T - 300));
      sigma = 1 / rho; n = 8.5e22; mu = 43; kind = '자유 전자 (금속)';
    } else if (M.ins){
      sigma = 1e-14 * Math.pow(T / 300, 2); n = 1e4; mu = 1; kind = '거의 없음 (절연체)';
    } else {
      var ni = siIntrinsic(T);
      var nd = D.k ? ppm * 5e16 : 0;
      n = nd + ni; mu = D.mu; sigma = Q * n * mu;
      kind = D.k ? D.type : '순수 규소 (열로 생긴 전자·양공)';
    }
    var R = 1 / sigma;                                   // L=1cm, A=1cm²
    return {M:M, D:D, ppm:ppm, T:T, n:n, mu:mu, sigma:sigma, R:R, I:V / R, kind:kind,
      doped:(!M.metal && !M.ins && D.k === 1), ni:M.metal || M.ins ? 0 : siIntrinsic(T)};
  },
  draw: function(c, W, H, p, r, tau){
    var M = MAT[p.m], bx = 60, by = 110, bw = Math.min(380, W - 260), bh = 120;
    c.fillStyle = M.metal ? '#E3C9A8' : M.ins ? '#DCD6E6' : '#D6E2EE';
    c.fillRect(bx, by, bw, bh);
    c.strokeStyle = '#5B6776'; c.lineWidth = 2; c.strokeRect(bx, by, bw, bh);
    txt(c, M.n + ' (' + M.t + ') 막대 · 1 cm × 1 cm²', bx, by - 14, {bold:true, color:'#4A5868'});
    // 결정 격자 점
    if (!M.metal){
      for (var i = 0; i < 6; i++) for (var j = 0; j < 3; j++){
        c.fillStyle = '#8C99A8'; c.beginPath(); c.arc(bx + 34 + i * (bw - 68) / 5, by + 26 + j * (bh - 52) / 2, 5, 0, Math.PI * 2); c.fill();
      }
      if (!M.ins && DOP[p.d].k){
        c.fillStyle = DOP[p.d].mu > 1000 ? '#2E9E78' : '#C8463D';
        c.beginPath(); c.arc(bx + 34 + 2 * (bw - 68) / 5, by + 26 + (bh - 52) / 2, 9, 0, Math.PI * 2); c.fill();
        txt(c, DOP[p.d].mu > 1000 ? 'P' : 'B', bx + 34 + 2 * (bw - 68) / 5, by + 26 + (bh - 52) / 2 + 6, {align:'center', color:'#fff', bold:true});
      }
    }
    // 전지와 전구
    txt(c, '1.5 V', bx + bw / 2, by + bh + 34, {align:'center', color:'#4A5868'});
    seg(c, bx, by + bh + 14, bx, by + bh + 46, '#5B6776', 2);
    seg(c, bx + bw, by + bh + 14, bx + bw, by + bh + 46, '#5B6776', 2);
    seg(c, bx, by + bh + 46, bx + bw, by + bh + 46, '#5B6776', 2);
    if (!r){ txt(c, '전류가 흐를 만큼 움직이는 전하가 있는지 재어 봐요.', 16, H - 18, {color:'#4A5868'}); return; }
    // 캐리어 애니메이션
    var nn = Math.min(14, Math.max(0, Math.round(Math.log10(Math.max(r.n, 1)) - 8)));
    for (var k = 0; k < nn; k++){
      var t2 = ((tau * 1.6 + k * 0.13) % 1);
      c.fillStyle = 'rgba(43,95,163,.8)';
      c.beginPath(); c.arc(bx + 12 + (bw - 24) * t2, by + 20 + (k % 5) * (bh - 40) / 4, 4.5, 0, Math.PI * 2); c.fill();
    }
    var mx = bx + bw + 24;
    if (mx < W - 170){
      txt(c, '전류', mx, by + 20, {color:'#4A5868'});
      meter(c, mx, by + 30, Math.min(170, W - mx - 12), r.I >= 1000 ? (r.I).toExponential(1) + ' A' : r.I < 1e-6 ? r.I.toExponential(1) + ' A' : f(r.I, 3) + ' A');
    }
    var yy = by + bh + 82;
    txt(c, '캐리어 농도 ' + r.n.toExponential(1) + ' /cm³ (' + r.kind + ')', 16, yy, {bold:true, color:'#2B5FA3'});
    txt(c, '전도도 ' + r.sigma.toExponential(2) + ' S/cm → 저항 ' + r.R.toExponential(2) + ' Ω', 16, yy + 30, {});
    txt(c, r.I > 1e-3 ? '전구가 밝게 켜졌어요.' : r.I > 1e-9 ? '아주 약한 전류만 흘러요.' : '전류가 거의 흐르지 않아요.',
      16, H - 14, {bold:true, color:r.I > 1e-3 ? '#2E9E78' : '#C8463D'});
  },
  stats: function(p, r){
    return [['재료', r.M.n + ' (' + r.M.t + ')'], ['온도', r.T + ' K'],
      ['섞은 원소', r.doped ? r.D.n : '해당 없음'], ['도핑 농도', r.doped ? r.ppm + ' ppm' : '—'],
      ['캐리어 종류', r.kind, PAL[6]], ['캐리어 농도', r.n.toExponential(2) + ' /cm³', PAL[0]],
      ['이동도 μ', r.mu + ' cm²/(V·s)'], ['전도도 σ', r.sigma.toExponential(2) + ' S/cm', PAL[1]],
      ['저항 R', r.R.toExponential(2) + ' Ω', PAL[4]], ['전류 I (1.5 V, 이론값)', r.I.toExponential(2) + ' A'],
      ['순수 규소 캐리어(참고)', r.ni ? r.ni.toExponential(2) + ' /cm³' : '—']];
  },
  columns: ['재료', '도핑', '농도 (ppm)', 'T (K)', '캐리어 /cm³', 'σ (S/cm)', 'R (Ω)', 'I (A)'],
  record: function(p, r){
    return {mi:p.m, mat:r.M.n, dop:r.doped ? r.D.n : '없음', di:p.d, ppm:r.doped ? r.ppm : 0, T:r.T,
      n:r.n, sigma:r.sigma, R:r.R, I:r.I, metal:!!r.M.metal, ins:!!r.M.ins};
  },
  row: function(d){ return [d.mat, d.dop, d.ppm ? d.ppm : '—', d.T, d.n.toExponential(1), d.sigma.toExponential(2), d.R.toExponential(2), d.I.toExponential(2)]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('도핑 농도와 전도도', '<canvas class="chart" id="ch1" role="img" aria-label="도핑 농도 로그값과 전도도 로그값 산점도"></canvas><ul class="readout" id="ro1"></ul><p class="ask">가로·세로 모두 10의 거듭제곱으로 그린 그래프입니다. 기울기가 1이라는 것은 무슨 뜻일까요?</p>') +
      card('온도를 올리면', '<canvas class="chart" id="ch2" role="img" aria-label="온도와 상대 저항 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">금속과 반도체의 방향이 반대입니다. 각각 무엇이 늘어나서 그럴까요?</p>') +
      card('세 부류 비교', '<div id="ro3"></div><p class="ask">순수할수록 좋은 재료일까요? 반도체에서 불순물이 하는 일을 설명해 보세요.</p>') + '</div>';
    var dp = rec.filter(function(d){ return d.ppm > 0 && !d.metal && !d.ins; });
    var bd = groupBy(dp, function(d){ return d.di; }), s1 = [], r1 = [], ci = 0;
    Object.keys(bd).forEach(function(k){
      var g = bd[k], col = PAL[ci++ % PAL.length];
      s1.push({color:col, pts:g.map(function(d){ return {x:Math.log10(d.ppm), y:Math.log10(d.sigma)}; })});
      if (distinct(g.map(function(d){ return d.ppm; })) >= 2){
        var L = linfit(g.map(function(d){ return {x:Math.log10(d.ppm), y:Math.log10(d.sigma)}; }));
        r1.push('<li>' + dot(col) + g[0].dop + ': 기울기 <b>' + f(L.k, 2) + '</b> — 농도를 10배로 하면 전도도도 약 10배가 돼요.</li>');
      }
    });
    drawScatter($('ch1'), {xLabel:'log₁₀(도핑 농도 / ppm)', yLabel:'log₁₀(전도도 / S·cm⁻¹)', tightX:true, tightY:true, series:s1});
    $('ro1').innerHTML = (r1.length ? r1.join('') : '<li>규소에 인이나 붕소를 넣고 농도를 2가지 이상 바꿔 기록해 보세요.</li>') +
      '<li>기울기 1은 <b>정비례</b>를 뜻해요. 넣은 불순물 원자 하나가 캐리어 하나를 내놓기 때문이에요.</li>' +
      (dp.length && distinct(dp.map(function(d){ return d.di; })) >= 2 ? '<li>같은 농도라도 인(n형, 전자)이 붕소(p형, 양공)보다 전도도가 커요. 전자가 더 빠르기 때문이에요.</li>' : '');
    var bm = groupBy(rec, function(d){ return d.mi + '-' + d.di + '-' + d.ppm; }), s2 = [], r2 = [], ci2 = 0;
    Object.keys(bm).forEach(function(k){
      var g = bm[k];
      if (distinct(g.map(function(d){ return d.T; })) < 2) return;
      var base = g.slice().sort(function(a, b){ return Math.abs(a.T - 300) - Math.abs(b.T - 300); })[0];
      var col = PAL[ci2++ % PAL.length];
      s2.push({color:col, pts:g.map(function(d){ return {x:d.T, y:d.R / base.R}; })});
      var srt = g.slice().sort(function(a, b){ return a.T - b.T; });
      r2.push('<li>' + dot(col) + srt[0].mat + (srt[0].ppm ? ' (' + srt[0].dop + ' ' + srt[0].ppm + ' ppm)' : '') + ': ' +
        srt[0].T + ' K → ' + srt[srt.length - 1].T + ' K 에서 저항이 ' +
        (srt[srt.length - 1].R > srt[0].R ? '<b>커졌어요</b>' : '<b>작아졌어요</b>') + '</li>');
    });
    drawScatter($('ch2'), {xLabel:'온도 (K)', yLabel:'상대 저항 (300 K 근처 = 1)', tightX:true, series:s2.length ? s2 : [{color:PAL[0], pts:[]}]});
    $('ro2').innerHTML = (r2.length ? r2.join('') : '<li>같은 재료·같은 도핑에서 온도만 2가지 이상 바꿔 기록해 보세요.</li>') +
      '<li>금속은 캐리어 수가 이미 최대라 온도가 오르면 <b>충돌만 늘어</b> 저항이 커져요.</li>' +
      '<li>반도체는 온도가 오르면 <b>캐리어가 새로 생겨</b> 저항이 작아져요. 이 성질로 온도 센서를 만들어요.</li>';
    var seen = {}, rows = [];
    rec.forEach(function(d){ var k = d.mat + d.dop + d.ppm; if (seen[k]) return; seen[k] = 1;
      rows.push([d.mat + (d.ppm ? ' + ' + d.dop + ' ' + d.ppm + ' ppm' : ''), d.metal ? '도체' : d.ins ? '절연체' : '반도체',
        d.n.toExponential(1), d.sigma.toExponential(1), d.R.toExponential(1)]); });
    $('ro3').innerHTML = tableHTML(['재료', '분류', '캐리어 /cm³', 'σ (S/cm)', 'R (Ω)'], rows, 'wrap') +
      '<p class="note">도체와 절연체 사이의 전도도 차이는 10²⁰배가 넘어요. 반도체는 그 사이를 <b>사람이 정한 값으로 맞출 수 있는</b> 재료예요.</p>';
  }
};`
},

/* ===================== 26. 초전도 (Matter Ep08) ===================== */
{
  file: '26_superconductor_critical_temp_lab_IntegSci1_Matter_Ep08.html',
  title: '저항이 0이 되는 온도',
  intro: '송전선 길이 100 m짜리 시료를 여러 냉각제로 식히며 저항과 손실 전력을 잽니다. 물질마다 정해진 임계 온도보다 낮아지는 순간 무슨 일이 일어나는지 확인해 보세요.',
  sceneNote: '단면적 1 mm², 길이 100 m인 도선을 가정했습니다. 임계 온도는 실제 값이고, 상전도 상태의 저항은 온도에 비례한다고 단순화했습니다.',
  runLabel: '식히고 전류 흘리기',
  principle: `<h2>📖 과학 원리 — 어떤 원리로 이렇게 될까?</h2>
<h3>🔑 핵심 원리 — 임계 온도 아래에서 저항이 사라진다</h3>
<p>보통 금속은 온도를 낮추면 저항이 줄지만 0이 되지는 않아요. 그런데 어떤 물질은 <b>임계 온도(T<sub>c</sub>)</b> 아래로 내려가는 순간 저항이 <b>정확히 0</b>이 돼요. 이것이 <b>초전도</b>예요. 초전도 상태에서는 전류가 흘러도 열이 전혀 나지 않고(P = I²R = 0), 자기장을 밀어내는 <b>마이스너 효과</b> 때문에 자석이 공중에 떠요. 다만 그 온도까지 식히는 데 비용이 들어요.</p>

<h3>⚙️ 계산해 보기</h3>
<ul>
<li>손실 전력 <span class="fx-formula">P = I²R</span> — 구리 도선 100 m(1 mm²)의 저항은 상온에서 약 1.7 Ω, 여기에 50 A를 흘리면 4 250 W가 열로 사라져요.</li>
<li>납은 T<sub>c</sub> = 7.2 K, 니오븀은 9.3 K이라 액체 헬륨(4.2 K)이 필요하지만, YBCO는 T<sub>c</sub> = 92 K이라 훨씬 싼 <b>액체 질소(77 K)</b>로 충분해요.</li>
<li>구리는 아무리 식혀도 초전도가 되지 않아요. 잘 통하는 금속이 곧 초전도체는 아니에요.</li>
<li>초전도 상태의 손실은 0이므로, 같은 전류로 1년을 보내도 잃는 전기 에너지가 없어요.</li>
</ul>

<h3>🧮 이 실험의 계산 방법</h3>
<p><span class="fx-formula">T &lt; T<sub>c</sub> → R = 0</span>, 그렇지 않으면 <span class="fx-formula">R = R₃₀₀ × T ÷ 300</span>, <span class="fx-formula">P = I²R</span>, 1년 손실 = P × 8 760 h</p>

<div class="fx-model"><b>📌 실험 모형과 실제의 차이</b><br>
· 상전도 상태의 저항을 <b>온도에 정비례</b>한다고 단순화했어요. 실제 금속은 아주 낮은 온도에서 일정한 잔류 저항이 남아요.<br>
· 초전도에는 온도 말고도 <b>임계 전류</b>와 <b>임계 자기장</b>이라는 한계가 있어요. 너무 큰 전류를 흘리면 임계 온도 아래여도 초전도가 깨져요. 이 실험에는 그 한계를 넣지 않았어요.</div>

<h3>🌍 생활 속에서</h3>
<ul>
<li>병원의 MRI는 초전도 전자석으로 강한 자기장을 만들고, 액체 헬륨으로 식혀요.</li>
<li>자기 부상 열차와 핵융합 장치의 전자석도 초전도선을 써요. 상온 초전도체를 찾는 연구가 계속되는 이유예요.</li>
</ul>`,
  js: `
var MATS = [
  {n:'구리',      tc:0,    r300:1.7, sc:false, note:'좋은 도체지만 초전도가 되지 않음'},
  {n:'납 Pb',     tc:7.2,  r300:21,  sc:true,  note:'1911년 수은에서 초전도가 처음 발견된 뒤 곧이어 확인된 초기 초전도체'},
  {n:'니오븀 Nb', tc:9.3,  r300:15,  sc:true,  note:'MRI 전자석 선재(NbTi)의 바탕'},
  {n:'YBCO',     tc:92,   r300:900, sc:true,  note:'고온 초전도체, 액체 질소로 충분'}
];
var COOL = [{n:'상온',T:300},{n:'드라이아이스',T:195},{n:'액체 질소',T:77},{n:'액체 헬륨',T:4.2}];
return {
  sceneHeight: 460,
  minRec: 4,
  idle: '물질과 냉각제, 전류를 정하고 <b>식히고 전류 흘리기</b>를 누르세요.',
  shortHint: '자유 탐구 탭에서 물질과 냉각제를 바꿔 가며 기록하세요.',
  params: [
    {key:'m', type:'seg', label:'시료 물질', cols:4, value:3, options:MATS.map(function(x){ return x.n + '<small>' + (x.sc ? 'T' + 'ᴄ' + ' ' + f(x.tc, 1) + ' K' : '초전도 없음') + '</small>'; })},
    {key:'c', type:'seg', label:'냉각제', cols:4, value:2, options:COOL.map(function(x){ return x.n + '<small>' + f(x.T, 1) + ' K</small>'; })},
    {key:'I', type:'range', label:'흘리는 전류', min:5, max:100, step:5, value:50, fmt:function(v){ return v + ' A'; },
      note:'길이 100 m, 단면적 1 mm²인 도선입니다. 임계 온도보다 낮으면 저항이 0이 됩니다.'}
  ],
  compute: function(p){
    var M = MATS[p.m], T = COOL[p.c].T, I = p.I;
    var superOn = M.sc && T < M.tc;
    var R = superOn ? 0 : M.r300 * T / 300;
    var P = I * I * R;
    return {M:M, cool:COOL[p.c], T:T, I:I, R:R, P:P, superOn:superOn,
      kwh:P * 8760 / 1000, levit:superOn, margin:M.sc ? M.tc - T : null};
  },
  draw: function(c, W, H, p, r, tau){
    var M = MATS[p.m], T = COOL[p.c].T;
    var bx = 50, by = 150, bw = Math.min(400, W - 230), bh = 40;
    // 냉각 용기
    c.fillStyle = '#EAF3F9'; c.fillRect(bx - 24, by - 74, bw + 48, bh + 150);
    c.strokeStyle = '#8C99A8'; c.lineWidth = 2; c.strokeRect(bx - 24, by - 74, bw + 48, bh + 150);
    txt(c, COOL[p.c].n + ' ' + f(T, 1) + ' K', bx - 20, by - 84, {color:'#2B5FA3', bold:true});
    // 시료
    var on = r && r.superOn && tau > 0.5;
    c.fillStyle = on ? '#BFE3D3' : '#D8DEE6'; c.fillRect(bx, by, bw, bh);
    c.strokeStyle = '#5B6776'; c.lineWidth = 2; c.strokeRect(bx, by, bw, bh);
    txt(c, M.n + ' 도선 100 m', bx + 8, by + 26, {bold:true, color:'#2E3945'});
    // 전자 흐름
    if (r){
      var nn = 10;
      for (var k = 0; k < nn; k++){
        var t2 = ((tau * (on ? 2.2 : 0.9) + k / nn) % 1);
        c.fillStyle = on ? '#2E9E78' : '#C8463D';
        c.beginPath(); c.arc(bx + 10 + (bw - 20) * t2, by + bh / 2, 5, 0, Math.PI * 2); c.fill();
      }
    }
    // 자석 부상
    var magY = by - 40 - (on ? 22 * Math.min(1, (tau - 0.5) * 3) : 0);
    c.fillStyle = on ? '#C8463D' : '#A8B3BF'; c.fillRect(bx + bw / 2 - 26, magY, 52, 22);
    txt(c, '자석', bx + bw / 2, magY + 16, {align:'center', color:'#fff', bold:true});
    if (on){
      txt(c, '마이스너 효과로 떠 있어요', bx + bw / 2, magY - 10, {align:'center', color:'#2E9E78', bold:true});
    }
    var mx = bx + bw + 28;
    if (mx < W - 170 && r){
      txt(c, '저항', mx, by - 10, {color:'#4A5868'});
      meter(c, mx, by, Math.min(170, W - mx - 12), r.R === 0 ? '0 Ω' : f(r.R, 2) + ' Ω');
      txt(c, '손실 전력', mx, by + 70, {color:'#4A5868'});
      meter(c, mx, by + 80, Math.min(170, W - mx - 12), r.P === 0 ? '0 W' : Math.round(r.P).toLocaleString() + ' W');
    }
    if (!r){ txt(c, '임계 온도보다 낮게 식히면 저항이 0이 돼요.', 16, H - 18, {color:'#4A5868'}); return; }
    var yy = by + bh + 92;
    txt(c, M.sc ? ('임계 온도 ' + f(M.tc, 1) + ' K, 지금 ' + f(T, 1) + ' K → ' + (r.superOn ? '초전도 상태' : '보통(상전도) 상태'))
      : (M.n + '은 임계 온도가 없어요 → 늘 보통 상태'), 16, yy, {bold:true, color:r.superOn ? '#2E9E78' : '#C8463D'});
    txt(c, '전류 ' + r.I + ' A · 저항 ' + (r.R === 0 ? '0 Ω' : f(r.R, 2) + ' Ω') + ' · 손실 P = I²R = ' + Math.round(r.P).toLocaleString() + ' W', 16, yy + 32, {});
    txt(c, '1년 내내 흘리면 ' + (r.kwh === 0 ? '잃는 전기 에너지가 없어요.' : Math.round(r.kwh).toLocaleString() + ' kWh를 열로 잃어요.'),
      16, H - 14, {color:'#4A5868'});
  },
  stats: function(p, r){
    return [['시료', r.M.n], ['임계 온도 Tᴄ', r.M.sc ? f(r.M.tc, 1) + ' K' : '없음'],
      ['냉각제', r.cool.n + ' (' + f(r.T, 1) + ' K)'],
      ['상태', r.superOn ? '초전도' : '보통(상전도)', r.superOn ? PAL[1] : PAL[4]],
      ['저항 R', r.R === 0 ? '0 Ω' : f(r.R, 2) + ' Ω', PAL[0]],
      ['전류 I', r.I + ' A'], ['손실 전력 P = I²R', r.P === 0 ? '0 W' : Math.round(r.P).toLocaleString() + ' W', PAL[4]],
      ['1년 손실 에너지', Math.round(r.kwh).toLocaleString() + ' kWh'],
      ['자석 부상', r.levit ? '뜸 (마이스너 효과)' : '뜨지 않음'],
      ['임계 온도까지 여유', r.margin === null ? '—' : sgn(r.margin, 1) + ' K'], ['메모', r.M.note]];
  },
  columns: ['시료', 'Tᴄ (K)', '냉각제', 'T (K)', '상태', 'I (A)', 'R (Ω)', 'P (W)', '1년 손실 (kWh)'],
  record: function(p, r){
    return {mi:p.m, mat:r.M.n, tc:r.M.sc ? r.M.tc : 0, sc:r.M.sc, cool:r.cool.n, T:r.T, I:r.I, R:r.R, P:r.P, kwh:r.kwh, on:r.superOn};
  },
  row: function(d){ return [d.mat, d.sc ? f(d.tc, 1) : '—', d.cool, f(d.T, 1), d.on ? '초전도' : '보통', d.I, d.R === 0 ? '0' : f(d.R, 2),
    d.P === 0 ? '0' : Math.round(d.P).toLocaleString(), Math.round(d.kwh).toLocaleString()]; },
  verify: function(rec, box){
    box.innerHTML = '<div class="vgrid">' +
      card('온도와 저항', '<canvas class="chart" id="ch1" role="img" aria-label="온도와 저항 산점도"></canvas><ul class="readout" id="ro1"></ul><p class="ask">저항이 서서히 줄다가 어느 온도에서 뚝 떨어집니다. 그 온도를 물질마다 비교해 보세요.</p>') +
      card('전류와 손실 전력', '<canvas class="chart" id="ch2" role="img" aria-label="전류 제곱과 손실 전력 산점도"></canvas><ul class="readout" id="ro2"></ul><p class="ask">손실이 전류의 제곱에 비례한다면, 전류를 절반으로 줄이면 손실은 몇 분의 1이 될까요?</p>') +
      card('어떤 냉각제를 쓸 수 있나', '<div id="ro3"></div><p class="ask">액체 헬륨은 액체 질소보다 훨씬 비쌉니다. YBCO의 발견이 왜 중요한 사건이었을까요?</p>') + '</div>';
    var bm = groupBy(rec, function(d){ return d.mi; }), s1 = [], r1 = [];
    Object.keys(bm).forEach(function(k){
      var g = bm[k], col = PAL[+k % PAL.length];
      s1.push({color:col, pts:g.map(function(d){ return {x:d.T, y:d.R}; })});
      var zero = g.filter(function(d){ return d.on; });
      r1.push('<li>' + dot(col) + g[0].mat + ': ' + (g[0].sc ? '임계 온도 ' + f(g[0].tc, 1) + ' K' : '임계 온도 없음') +
        ' — 저항 0인 기록 <b>' + zero.length + '개</b> / ' + g.length + '개</li>');
    });
    drawScatter($('ch1'), {xLabel:'온도 (K)', yLabel:'저항 (Ω)', series:s1});
    $('ro1').innerHTML = r1.join('') +
      '<li>보통 상태에서는 온도가 낮아질수록 저항이 <b>조금씩</b> 줄지만, 임계 온도 아래에서는 <b>정확히 0</b>이 돼요. 서서히 줄어든 것이 아니라 성질이 바뀐 거예요.</li>';
    var norm = rec.filter(function(d){ return !d.on; });
    var bn = groupBy(norm, function(d){ return d.mi + '-' + d.T; }), s2 = [], r2 = [], ci = 0;
    Object.keys(bn).forEach(function(k){
      var g = bn[k];
      if (distinct(g.map(function(d){ return d.I; })) < 2) return;
      var col = PAL[ci++ % PAL.length];
      s2.push({color:col, pts:g.map(function(d){ return {x:d.I * d.I, y:d.P}; })});
      var kk = fit0(g.map(function(d){ return {x:d.I * d.I, y:d.P}; }));
      r2.push('<li>' + dot(col) + g[0].mat + ' ' + f(g[0].T, 1) + ' K: 기울기 <b>' + f(kk, 2) + '</b> ≈ 저항 ' + f(g[0].R, 2) + ' Ω</li>');
    });
    drawScatter($('ch2'), {xLabel:'전류의 제곱 I² (A²)', yLabel:'손실 전력 P (W)', series:s2.length ? s2 : [{color:PAL[0], pts:[]}]});
    $('ro2').innerHTML = (r2.length ? r2.join('') : '<li>보통 상태(저항이 0이 아닌 기록)에서 전류만 2가지 이상 바꿔 기록해 보세요.</li>') +
      '<li>P–I² 그래프가 원점을 지나는 직선이므로 <b>P = I²R</b>이에요. 전류를 절반으로 줄이면 손실은 <b>1/4</b>이 돼요.</li>' +
      '<li>초전도 상태에서는 R = 0이라 손실이 0이에요. 다만 실제로는 <b>임계 전류</b>와 <b>임계 자기장</b>도 있어서, 온도가 T꜀ 아래여도 전류나 자기장이 너무 크면 초전도가 깨져요. 이 실험은 그 한계를 넘지 않는다고 가정했어요.</li>';
    var rows = MATS.map(function(M){
      return [M.n, M.sc ? f(M.tc, 1) + ' K' : '—',
        M.sc && M.tc > 195 ? '가능' : '불가', M.sc && M.tc > 77 ? '가능' : '불가', M.sc && M.tc > 4.2 ? '가능' : '불가', M.note];
    });
    $('ro3').innerHTML = tableHTML(['물질', 'Tᴄ', '드라이아이스 195 K', '액체 질소 77 K', '액체 헬륨 4.2 K', '메모'], rows, 'wrap') +
      '<p class="note">액체 질소는 공기에서 얻을 수 있어 값이 싸요. 임계 온도를 77 K 위로 올린 것이 고온 초전도체 연구의 큰 성과예요.</p>';
  }
};`
}

  ]
};
