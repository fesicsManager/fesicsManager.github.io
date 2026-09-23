// 고1 통합과학 자습 노트 content 생성기 (mathgen.js의 원리 섹션 추출 + 흐름·다음 링크 직접 지정)
// usage: node integgen.js <seeds.json> <folder>
// seed: {name, unit, title, lead, intro, table{caption,head,rows}, note, cuts[{who,quote,src}],
//        eq?, units?, concepts?, examples[2], quiz[4], checklist[5], flow[labels], next{text,href,label}, index?}
const fs = require('fs'), path = require('path');
const [, , seedFile, folder] = process.argv;
if (!seedFile || !folder) { console.error('usage: node integgen.js <seeds.json> <folder>'); process.exit(1); }
const here = __dirname;
const labDir = path.join(here, '..', '..', folder);        // notes/_src → fesicsExternal/<folder>
const outDir = path.join(here, 'content', folder);
fs.mkdirSync(outDir, { recursive: true });
const seeds = JSON.parse(fs.readFileSync(seedFile, 'utf8'));

const clean = h => h.replace(/\s+/g, ' ').trim();
const h1Of = s => clean((s.match(/<h1[^>]*>([\s\S]*?)<\/h1>/) || ['', ''])[1].replace(/<[^>]+>/g, ''));
// 받침이 있으면 '으로', 없으면 '로'
function ro(w) {
  const c = w.charCodeAt(w.length - 1) - 0xAC00;
  return (c >= 0 && c < 11172 && c % 28 !== 0) ? '으로' : '로';
}

function sections(s) {
  const pr = (s.match(/<section[^>]*id="fxPrinciple"[\s\S]*?<\/section>/) || [''])[0];
  let inner = pr.replace(/<section[^>]*>|<\/section>/g, '').replace(/<div class="fx-p-card">/, '').replace(/<\/div>\s*$/, '');
  inner = inner.replace(/<h2[^>]*>[\s\S]*?<\/h2>/, '');
  const model = (inner.match(/<div class="fx-model">([\s\S]*?)<\/div>/) || ['', ''])[1];
  inner = inner.replace(/<div class="fx-model">[\s\S]*?<\/div>/, '');
  const parts = inner.split(/<h3[^>]*>/).slice(1).map(p => {
    const i = p.indexOf('</h3>');
    return { h: clean(p.slice(0, i).replace(/<[^>]+>/g, '')), body: p.slice(i + 5).trim() };
  });
  const get = re => parts.filter(p => re.test(p.h));
  return { key: get(/^🔑/)[0], why: get(/^⚙️/)[0], calc: get(/^🧮/)[0], life: get(/^🌍/)[0], model: model.trim() };
}

let n = 0, miss = [];
for (const sd of seeds) {
  const p = path.join(labDir, sd.name + '.html');
  if (!fs.existsSync(p)) { miss.push(sd.name); continue; }
  const s = fs.readFileSync(p, 'utf8');
  const sec = sections(s);
  const labTitle = h1Of(s);

  const concepts = [];
  if (sec.key) concepts.push({
    h: sec.key.h.replace(/^🔑\s*핵심 원리\s*[—–]?\s*/, ''),
    html: sec.key.body + (sec.why ? `<p><b>${sec.why.h.replace(/^⚙️\s*/, '')}</b></p>` + sec.why.body : '')
  });
  if (sec.model) concepts.push({
    h: '실험 모형과 실제의 차이',
    html: '<p>' + sec.model.replace(/<b>📌[^<]*<\/b>\s*(<br>)?/, '').replace(/<br>\s*·/g, '</p><p>·').replace(/^\s*·/, '·') + '</p>'
  });
  if (sec.life) concepts.push({ h: '생활 속에서 · 이어지는 개념', html: sec.life.body });
  const eq = sec.calc ? clean(sec.calc.body.replace(/<span class="fx-formula">|<\/span>/g, '').replace(/<\/?p>/g, '').replace(/<[^>]+>/g, '')) : '';

  const flow = (sd.flow || []).map((l, i, a) => {
    const nowAt = a.findIndex(x => /자습 노트/.test(x));
    if (/자습 노트/.test(l)) return { label: l, state: 'now' };
    return i < nowAt ? { label: l, state: 'done' } : { label: l };
  });

  const out = {
    unit: sd.unit,
    title: sd.title,
    lead: sd.lead,
    flow,
    lab: { href: `../../${folder}/${sd.name}.html`, label: `실험 「${labTitle}」${ro(labTitle)}` },
    index: sd.index || '../../index.html',
    recall: { intro: sd.intro || '', table: sd.table, note: sd.note },
    concepts: sd.concepts || concepts,
    formula: { eq: sd.eq || eq || '—', units: sd.units || '' },
    cuts: sd.cuts || [],
    examples: sd.examples,
    quiz: sd.quiz,
    checklist: sd.checklist,
    next: sd.next
  };
  fs.writeFileSync(path.join(outDir, sd.name + '.json'), JSON.stringify(out, null, 1), 'utf8');
  n++;
}
console.log('generated', n, 'of', seeds.length, '->', outDir);
if (miss.length) console.warn('lab html not found:', miss.join(', '));
