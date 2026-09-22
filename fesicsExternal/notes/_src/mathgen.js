// usage: node mathgen.js <seeds.json> <folder>   — builds content/<folder>/<name>.json from seed + lab HTML
// seed: {name, unit?, title, lead, table{caption,head,rows}, note, examples[2], quiz[4], checklist[5], next: "<name>"|"index"|{href,label,text}}
const fs = require('fs'), path = require('path');
const [,, seedFile, folder] = process.argv;
const here = __dirname;
const srcDir = path.join(here, 'src', folder);
const outDir = path.join(here, 'content', folder);
fs.mkdirSync(outDir, { recursive: true });
const seeds = JSON.parse(fs.readFileSync(seedFile, 'utf8'));
const GROUP = { elem34: '초등 3~4학년 수학', elem56: '초등 5~6학년 수학', m1: '중학교 1학년 수학', m2: '중학교 2학년 수학', m3: '중학교 3학년 수학',
  h1: '고등학교 공통수학1', h2: '고등학교 공통수학2', hd: '고등학교 대수', hc: '고등학교 미적분Ⅰ', hp: '고등학교 확률과 통계', hg: '고등학교 기하', hm: '고등학교 미적분Ⅱ',
  hs_c1: '고등학교 공통수학1', hs_c2: '고등학교 공통수학2', hs_alg: '고등학교 대수', hs_calc: '고등학교 미적분Ⅰ', hs_stat: '고등학교 확률과 통계' };
const indexHref = folder === 'fesicsMathLabs' ? '../../fesicsMathLabs/index.html' : '../../index.html';
const clean = h => h.replace(/\s+/g, ' ').trim();
function prefixOf(name) { const m = name.match(/^(hs_[a-z0-9]+|[a-z0-9]+)_/); return m ? m[1] : ''; }
function h1Of(s) { return clean((s.match(/<h1[^>]*>([\s\S]*?)<\/h1>/) || ['', ''])[1].replace(/<[^>]+>/g, '')); }
function sections(s) {
  const pr = (s.match(/<section[^>]*id="fxPrinciple"[\s\S]*?<\/section>/) || s.match(/<details[^>]*id="fxPrinciple"[\s\S]*?<\/details>/) || [''])[0];
  let inner = pr.replace(/<section[^>]*>|<\/section>|<details[^>]*>|<\/details>|<summary[\s\S]*?<\/summary>/g, '').replace(/<div class="fx-p-card">|<\/div>\s*$/g, '');
  inner = inner.replace(/<h2[^>]*>[\s\S]*?<\/h2>/, '');
  const model = (inner.match(/<div class="fx-model">([\s\S]*?)<\/div>/) || ['', ''])[1];
  inner = inner.replace(/<div class="fx-model">[\s\S]*?<\/div>/, '');
  const parts = inner.split(/<h3[^>]*>/).slice(1).map(p => { const i = p.indexOf('</h3>'); return { h: clean(p.slice(0, i).replace(/<[^>]+>/g, '')), body: p.slice(i + 5).trim() }; });
  const get = re => parts.filter(p => re.test(p.h));
  return { key: get(/^🔑/)[0], why: get(/^⚙️/)[0], calc: get(/^🧮/)[0], life: get(/^🌍/)[0], model: model.trim(), rest: get(/^(?!🔑|⚙️|🧮|🌍)/) };
}
function concl(s) {
  const m = [...s.matchAll(/concl\s*=\s*'<b>정리<\/b>\s*—\s*([^']{10,300})/g)].map(x => x[1]);
  if (m[0]) return clean(m[0].replace(/<[^>]+>/g, ''));
  // zerolab family: first "ok" analysis sentence  '<span class="ok">…</span>…':
  const z = s.match(/<span class="ok">([^<]{8,200})<\/span>([^'<]{0,250})/);
  if (z && !/불일치|예외/.test(z[1])) return clean((z[1] + z[2]).replace(/&gt;/g, '>').replace(/&lt;/g, '<').replace(/&amp;/g, '&'));
  return '';
}
function titleOf(name) { const p = path.join(srcDir, name + '.html'); if (!fs.existsSync(p)) return ''; return h1Of(fs.readFileSync(p, 'utf8')).replace(/\s*[—–].*$/, ''); }
let n = 0;
for (const sd of seeds) {
  const p = path.join(srcDir, sd.name + '.html');
  if (!fs.existsSync(p)) { console.warn('no lab:', sd.name); continue; }
  const s = fs.readFileSync(p, 'utf8');
  const sec = sections(s);
  const pre = prefixOf(sd.name);
  const unit = sd.unit || `${GROUP[pre] || '수학'} · 실험 「${h1Of(s).replace(/\s*[—–].*$/, '')}」`;
  const hint0 = (s.match(/hint0\s*:\s*'([^']*)'/) || ['', ''])[1];
  const concepts = [];
  if (sec.key) concepts.push({ h: sec.key.h.replace(/^🔑\s*핵심 원리\s*[—–]?\s*/, ''), html: sec.key.body + (sec.why ? `<p><b>${sec.why.h.replace(/^⚙️\s*/, '')}</b></p>` + sec.why.body : '') });
  if (sec.model) { const mh = (sec.model.match(/<b>📌\s*([^<]*)<\/b>/) || ['', ''])[1].trim(); concepts.push({ h: /오해/.test(mh) || !mh ? '자주 하는 오해 바로잡기' : mh, html: '<p>' + sec.model.replace(/<b>📌[^<]*<\/b>\s*(<br>)?/, '').replace(/<br>\s*·/g, '</p><p>·').replace(/^·/, '·') + '</p>' }); }
  else if (sec.rest.length) concepts.push({ h: sec.rest[0].h.replace(/^[^\w가-힣]+\s*/, ''), html: sec.rest[0].body });
  if (sec.life) concepts.push({ h: '생활 속에서 · 이어지는 개념', html: sec.life.body });
  const eq = sec.calc ? clean(sec.calc.body.replace(/<span class="fx-formula">|<\/span>/g, '').replace(/<[^>]+>/g, '')) : '';
  const c = concl(s);
  const cuts = sd.cuts ? sd.cuts : (c ? [{ who: '📋 데이터 확인 탭의 결론', quote: `&ldquo;${c}&rdquo;`, src: '실험 「데이터 확인」 · 기록 4개 이상일 때 나오는 정리' }] : (sd.cut ? [{ who: '📋 데이터 확인 탭의 결론', quote: `&ldquo;${sd.cut}&rdquo;`, src: '실험 「데이터 확인」 · 기록 4개 이상일 때 나오는 분석' }] : []));
  const idx = sd.index || indexHref;
  let next;
  if (sd.next === 'index' || !sd.next) next = { text: sd.nextText || `${GROUP[pre] || '이 영역'} 실험을 이어서 해 보세요. 실험 목록에서 다음 실험을 골라 같은 방법으로 정리하면 됩니다.`, href: idx, label: '실험 목록으로' };
  else if (typeof sd.next === 'string') next = { text: sd.nextText || `다음 실험 「${titleOf(sd.next)}」으로 이어집니다.`, href: sd.next + '.html', label: `${titleOf(sd.next) || '다음 실험'} 노트로` };
  else next = sd.next;
  const nextLabel = typeof sd.next === 'string' && sd.next !== 'index' ? `다음: ${titleOf(sd.next).replace(/\s*실험실$/, '')}` : `${sd.group || GROUP[pre] || '수학'} 목록`;
  const flow = sd.flow ? sd.flow.map(l => ({ label: l, state: /자습 노트/.test(l) ? 'now' : 'done' })).concat([{ label: nextLabel }]) :
    [{ label: '실험: 기록표', state: 'done' }, { label: '수학 원리', state: 'done' }, { label: '자습 노트', state: 'now' }, { label: nextLabel }];
  const out = {
    unit, title: sd.title, lead: sd.lead,
    flow,
    lab: { href: `../../${folder}/${sd.name}.html`, label: (t => /실험실$/.test(t) ? `${t}로` : `실험 「${t}」으로`)(h1Of(s).replace(/\s*[—–].*$/, '')) },
    index: idx,
    recall: { intro: sd.intro || (hint0 ? `<p>실험 안내: ${hint0}</p>` : ''), table: sd.table, note: sd.note },
    concepts: sd.concepts || concepts,
    formula: { eq: sd.eq || eq || '—', units: sd.units || '' },
    cuts, examples: sd.examples, quiz: sd.quiz, checklist: sd.checklist, next
  };
  fs.writeFileSync(path.join(outDir, sd.name + '.json'), JSON.stringify(out, null, 1), 'utf8');
  n++;
}
console.log('generated', n, 'of', seeds.length, '->', outDir);
