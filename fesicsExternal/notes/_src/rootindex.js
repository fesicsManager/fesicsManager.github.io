// usage: node rootindex.js <root>
// 루트 index.html 에 (a) #univ 카드 추가(일반생물·고전역학·전자기학), (b) #highSoc 섹션(경제·통합사회·기후×2·정보),
// (c) #mathHigh 섹션(zerolabMathHigh, 과목별 카드) 을 추가하고, 각 항목에 📝 노트 배지를 붙인다. 총 개수·점프 메뉴도 갱신.
const fs = require('fs'), path = require('path');
const root = process.argv[2];
const p = path.join(root, 'index.html');
let html = fs.readFileSync(p, 'utf8');
const mode = process.argv[3] || 'main';
if (mode === 'main' && /id="highSoc"|id="mathHigh"|univGenBio\//.test(html)) { console.log('already has new sections — abort'); process.exit(0); }
if (mode === 'mid' && /id="midSoc"/.test(html)) { console.log('already has midSoc — abort'); process.exit(0); }

const esc = s => s.replace(/&(?!(amp|lt|gt|nbsp|quot|#\d+);)/g, '&amp;');
const strip = s => s.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
function labInfo(folder, file) {
  const s = fs.readFileSync(path.join(root, folder, file), 'utf8');
  const h1 = strip((s.match(/<h1[^>]*>([\s\S]*?)<\/h1>/) || ['', ''])[1]);
  const after = s.slice(s.indexOf('</h1>') + 5);
  let ds = strip((after.match(/<p[^>]*>([\s\S]*?)<\/p>/) || ['', ''])[1]).replace(/※.*$/, '').trim();
  if (ds.length > 170) ds = ds.slice(0, 168).replace(/\s\S*$/, '') + '…';
  return { h1, ds };
}
function li(folder, file, no) {
  const { h1, ds } = labInfo(folder, file);
  const name = file.replace(/\.html$/, '');
  const note = fs.existsSync(path.join(root, 'notes', folder, file)) ? `<a class="note" href="notes/${folder}/${file}" title="자습 노트: 개념 정리와 확인 문제">📝 노트</a>` : '';
  return `<li class="lab"><a href="${folder}/${file}"><span class="no">${String(no).padStart(2, '0')}</span><span class="tt">${esc(h1)}</span><span class="ds">${esc(ds)}</span></a>${note}</li>`;
}
function card(color, level, title, folder, files) {
  return `<section class="card ${color}" data-level="${level}"><h3><span class="dot"></span>${title}<span class="cnt">${files.length}</span></h3><ul>` + files.map((f, i) => li(folder, f, i + 1)).join('') + `</ul></section>`;
}
const list = (folder, filt) => fs.readdirSync(path.join(root, folder)).filter(f => f.endsWith('.html') && f !== 'index.html' && (!filt || filt.test(f))).sort();
const numSort = (a, b) => (+a.match(/_(\d+)_/)[1]) - (+b.match(/_(\d+)_/)[1]);

if (mode === 'mid2') {
  // midSoc 섹션 재구성(정보·환경·지리 16·경제) + elem56 에 환경 카드 추가
  const midCards = [
    card('teal', 'midSoc', '정보', 'midInfo', list('midInfo')),
    card('blue', 'midSoc', '환경', 'midEnv', list('midEnv')),
    card('green', 'midSoc', '지리', 'midGeo', list('midGeo')),
    card('brass', 'midSoc', '경제', 'midEcon', list('midEcon')),
  ];
  const midN = midCards.reduce((n, c) => n + (c.match(/<li class="lab"/g) || []).length, 0);
  const midSec = `<section class="level" id="midSoc"><h2>중학교 · 정보 · 환경 · 지리 · 경제<span class="cnt">${midN}개</span></h2><div class="cards">${midCards.join('')}</div></section>\n`;
  html = html.replace(/<section class="level" id="midSoc">[\s\S]*?<\/div><\/section>\n/, midSec);
  html = html.replace('중 정보·환경·지리</a>', '중 정보·환경·지리·경제</a>');
  if (!/elem56Env\//.test(html)) {
    const envCard = card('blue', 'elem56', '환경', 'elem56Env', list('elem56Env'));
    const envN = (envCard.match(/<li class="lab"/g) || []).length;
    const s = html.indexOf('<section class="level" id="elem56">');
    const e = html.indexOf('</div></section>', s);
    html = html.slice(0, e) + envCard + html.slice(e);
    html = html.replace(/(<section class="level" id="elem56"><h2>[^<]*<span class="cnt">)(\d+)(개<\/span>)/, (m, a, n, b) => a + (+n + envN) + b);
  }
  const total = (html.match(/<li class="lab/g) || []).length;
  html = html.replace(/<span class="mono">\d+<\/span>개/, `<span class="mono">${total}</span>개`);
  fs.writeFileSync(p, html, 'utf8');
  console.log(`midSoc ${midN}, total labs ${total}, badges ${(html.match(/<a class="note"/g) || []).length}`);
  process.exit(0);
}
if (mode === 'tech') {
  // 기술 카드: milddle1/2/3 + elem56 실과 5세트 + 새 섹션 highTech(기술·가정 6세트)
  if (/id="highTech"/.test(html)) { console.log('already has highTech — abort'); process.exit(0); }
  const addCard = (level, cardHtml) => {
    const n = (cardHtml.match(/<li class="lab"/g) || []).length;
    const s = html.indexOf(`<section class="level" id="${level}">`);
    const e = html.indexOf('</div></section>', s);
    html = html.slice(0, e) + cardHtml + html.slice(e);
    html = html.replace(new RegExp(`(<section class="level" id="${level}"><h2>[^<]*<span class="cnt">)(\\d+)(개<\\/span>)`), (m, a, k, b) => a + (+k + n) + b);
    return n;
  };
  const m1 = addCard('milddle1', card('brass', 'milddle1', '기술', 'milddle1Tech', list('milddle1Tech')));
  const m2 = addCard('milddle2', card('brass', 'milddle2', '기술', 'milddle2Tech', list('milddle2Tech')));
  const m3 = addCard('milddle3', card('brass', 'milddle3', '기술', 'milddle3Tech', list('milddle3Tech')));
  const sets56 = [['s1', '실과 ① 나와 가족의 생활'], ['s2', '실과 ② 생활 자원과 관리'], ['s3', '실과 ③ 발명과 문제 해결'], ['s4', '실과 ④ 기술·로봇·생명'], ['s5', '실과 ⑤ 소프트웨어']];
  let e56 = 0;
  for (const [pre, title] of sets56) e56 += addCard('elem56', card('brass', 'elem56', title, 'elem56Tech', list('elem56Tech', new RegExp(`_${pre}_`))));
  const setsHT = [['s1', '① 생활문화와 디지털 환경', 'green'], ['s2', '② 소비자와 생활복지', 'brass'], ['s3', '③ 인간과 성장하는 관계', 'blue'], ['s4', '④ 공학의 기초', 'teal'], ['s5', '⑤ 미래를 여는 공학 혁신', 'teal'], ['s6', '⑥ 지속가능한 융합 공학', 'green']];
  const htCards = setsHT.map(([pre, title, color]) => card(color, 'highTech', title, 'highTechHome', list('highTechHome', new RegExp(`_${pre}_`))));
  const htN = htCards.reduce((n, c) => n + (c.match(/<li class="lab"/g) || []).length, 0);
  const htSec = `<section class="level" id="highTech"><h2>고등학교 · 기술·가정<span class="cnt">${htN}개</span></h2><div class="cards">${htCards.join('')}</div></section>\n`;
  html = html.replace('<section class="level" id="univ">', htSec + '<section class="level" id="univ">');
  html = html.replace('<a href="#univ">대학</a>', '<a href="#highTech">고 기술·가정</a><a href="#univ">대학</a>');
  const total = (html.match(/<li class="lab/g) || []).length;
  html = html.replace(/<span class="mono">\d+<\/span>개/, `<span class="mono">${total}</span>개`);
  fs.writeFileSync(p, html, 'utf8');
  console.log(`tech: mid1 +${m1}, mid2 +${m2}, mid3 +${m3}, elem56 +${e56}, highTech ${htN}, total labs ${total}, badges ${(html.match(/<a class="note"/g) || []).length}`);
  process.exit(0);
}
if (mode === 'mid') {
  // 중학교 · 정보·환경·지리 섹션 — 중3 뒤(고1 앞)에 삽입
  const midCards = [
    card('teal', 'midSoc', '정보', 'midInfo', list('midInfo')),
    card('blue', 'midSoc', '환경', 'midEnv', list('midEnv')),
    card('green', 'midSoc', '지리', 'midGeo', list('midGeo')),
  ];
  const midN = midCards.reduce((n, c) => n + (c.match(/<li class="lab"/g) || []).length, 0);
  const midSec = `<section class="level" id="midSoc"><h2>중학교 · 정보 · 환경 · 지리<span class="cnt">${midN}개</span></h2><div class="cards">${midCards.join('')}</div></section>\n`;
  html = html.replace('<section class="level" id="high1">', midSec + '<section class="level" id="high1">');
  html = html.replace('<a href="#high1">고1</a>', '<a href="#midSoc">중 정보·환경·지리</a><a href="#high1">고1</a>');
  const total = (html.match(/<li class="lab/g) || []).length;
  html = html.replace(/<span class="mono">\d+<\/span>개/, `<span class="mono">${total}</span>개`);
  fs.writeFileSync(p, html, 'utf8');
  console.log(`midSoc ${midN}, total labs ${total}, badges ${(html.match(/<a class="note"/g) || []).length}`);
  process.exit(0);
}

// (a) univ
const univCards = [
  card('green', 'univ', '일반생물', 'univGenBio', list('univGenBio')),
  card('teal', 'univ', '고전역학', 'univMechanics', list('univMechanics')),
  card('teal', 'univ', '전자기학', 'univEM', list('univEM')),
];
const univAdd = univCards.reduce((n, c) => n + (c.match(/<li class="lab"/g) || []).length, 0);
const univStart = html.indexOf('<section class="level" id="univ">');
const univEnd = html.indexOf('</div></section>', univStart);
html = html.slice(0, univEnd) + univCards.join('') + html.slice(univEnd);
html = html.replace(/(<section class="level" id="univ"><h2>[^<]*<span class="cnt">)(\d+)(개<\/span>)/, (m, a, n, b) => a + (+n + univAdd) + b);

// (b) highSoc
const socCards = [
  card('brass', 'highSoc', '경제', 'highEcon', list('highEcon')),
  card('green', 'highSoc', '통합사회', 'highIntegSoc', list('highIntegSoc')),
  card('blue', 'highSoc', '기후변화와 환경생태', 'highClimateEco', list('highClimateEco')),
  card('blue', 'highSoc', '기후변화와 지속가능한 세계', 'highClimateSoc', list('highClimateSoc')),
  card('teal', 'highSoc', '정보', 'highInfo', list('highInfo')),
];
const socN = socCards.reduce((n, c) => n + (c.match(/<li class="lab"/g) || []).length, 0);
const socSec = `<section class="level" id="highSoc"><h2>고등학교 · 사회 · 정보 선택<span class="cnt">${socN}개</span></h2><div class="cards">${socCards.join('')}</div></section>\n`;
html = html.replace('<section class="level" id="univ">', socSec + '<section class="level" id="univ">');

// (c) mathHigh
const zl = list('zerolabMathHigh');
const grp = (pre, title, color) => card(color, 'mathHigh', title, 'zerolabMathHigh', zl.filter(f => f.startsWith(pre + '_')).sort(numSort));
const mathCards = [grp('hs_c1', '공통수학1', 'teal'), grp('hs_c2', '공통수학2', 'teal'), grp('hs_alg', '대수', 'brass'), grp('hs_calc', '미적분Ⅰ', 'green'), grp('hs_stat', '확률과 통계', 'blue')];
const mathN = mathCards.reduce((n, c) => n + (c.match(/<li class="lab"/g) || []).length, 0);
const mathSec = `<section class="level" id="mathHigh"><h2>고등학교 수학 · 제로 랩<span class="cnt">${mathN}개</span></h2><p style="margin:-4px 0 12px;color:var(--ink-soft)">초등·중학·고등 수학 실험 201개는 <a href="fesicsMathLabs/index.html" style="color:var(--teal-dark);font-weight:700">수학 실험실 목록</a>에 따로 정리되어 있습니다.</p><div class="cards">${mathCards.join('')}</div></section>\n`;
html = html.replace('<p class="empty" id="empty">', mathSec + '<p class="empty" id="empty">');

// jump nav + total
html = html.replace('<a href="#univ">대학</a>', '<a href="#highSoc">고 사회·정보</a><a href="#univ">대학</a><a href="#mathHigh">고 수학</a>');
const total = (html.match(/<li class="lab/g) || []).length;
html = html.replace(/<span class="mono">\d+<\/span>개/, `<span class="mono">${total}</span>개`);
html = html.replace('브라우저에서 바로 여는 가상 실험', '브라우저에서 바로 여는 가상 실험');
fs.writeFileSync(p, html, 'utf8');
console.log(`univ +${univAdd}, highSoc ${socN}, mathHigh ${mathN}, total labs ${total}, badges ${(html.match(/<a class="note"/g) || []).length}`);
