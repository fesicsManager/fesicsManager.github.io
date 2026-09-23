// 실험 생성기 (gen_labs.js 기반) — 출력 폴더를 인자로 덮어쓸 수 있게 함
// 사용: node gen2.js <labs 모듈 경로> [출력폴더 절대경로]
const fs = require('fs'), path = require('path');
const ROOT = 'G:\\내 드라이브\\Misodle Software\\fesicsExternal';
const TPL = fs.readFileSync(path.join(ROOT, 'high3ChemReaction', '08_fuel_cell_lab_ChemReaction_Ep10.html'), 'utf8');

const mod = require(path.resolve(process.argv[2]));
const OUT = process.argv[3] ? path.resolve(process.argv[3]) : path.join(ROOT, mod.folder);
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });
const PRIN = mod.principle || '과학 원리';

function build(L) {
  let t = TPL;
  const rep = (re, s, label) => { if (!re.test(t)) throw new Error('template part not found: ' + label); t = t.replace(re, () => s); };
  rep(/<title>[^<]*<\/title>/, `<title>${L.title} | ${mod.suffix}</title>`, 'title');
  rep(/<header>[\s\S]*?<\/header>/, `<header>\n    <h1>${L.title}</h1>\n    <p>${L.intro}</p>\n  </header>`, 'header');
  rep(/<section id="fxPrinciple"[\s\S]*?<\/section>/, `<section id="fxPrinciple" class="fx-principle" hidden aria-label="${PRIN}">\n<div class="fx-p-card">\n${L.principle}\n</div>\n</section>`, 'principle');
  rep(/<canvas id="scene"[^>]*><\/canvas>\s*<p class="note">[\s\S]*?<\/p>/, `<canvas id="scene" aria-label="${L.title} 실험 장면"></canvas>\n          <p class="note">${L.sceneNote}</p>`, 'canvas');
  rep(/<button class="btn" id="runBtn">[^<]*<\/button>/, `<button class="btn" id="runBtn">${L.runLabel}</button>`, 'runBtn');
  rep(/var LAB = \(function\(\)\{[\s\S]*?\n\}\)\(\);\n\n\/\* ================= 엔진/, `var LAB = (function(){\n${L.js}\n})();\n\n/* ================= 엔진`, 'LAB');
  t = t.replace(/\s*<!-- fxNoteLink:start -->[\s\S]*?<!-- fxNoteLink:end -->/, '');   // 자습 노트 버튼 제거 (notes 파일 없음)
  // 캔버스 글자가 좁은 화면에서 잘리지 않도록 자동 축소 (최소 11px)
  const OLD_TXT = `function txt(c, s, x, y, o){
  o = o || {}; c.font = (o.bold ? '700 ' : '') + '18px ' + FONT; c.fillStyle = o.color || '#1E2833';
  c.textAlign = o.align || 'left'; c.textBaseline = o.base || 'alphabetic'; c.fillText(s, x, y);
}`;
  if (!t.includes(OLD_TXT)) throw new Error('txt() not found');
  t = t.replace(OLD_TXT, `function txt(c, s, x, y, o){
  o = o || {}; var al = o.align || 'left', sz = o.size || 18;
  c.fillStyle = o.color || '#1E2833'; c.textAlign = al; c.textBaseline = o.base || 'alphabetic';
  c.font = (o.bold ? '700 ' : '') + sz + 'px ' + FONT;
  var CW = (c.canvas && c.canvas.clientWidth) || 0;
  var avail = CW ? (al === 'left' ? CW - x - 4 : al === 'right' ? x - 4 : 2 * Math.min(x, CW - x) - 4) : 0;
  if (avail > 40){
    var w = c.measureText(s).width;
    if (w > avail){ sz = Math.max(11, Math.floor(sz * avail / w)); c.font = (o.bold ? '700 ' : '') + sz + 'px ' + FONT; }
  }
  c.fillText(s, x, y);
}`);
  t = t.replace('ANIM_MS = 2400', 'ANIM_MS = ' + (L.anim || mod.anim || 2000));
  if (!/id="scene"/.test(t)) throw new Error('scene lost');
  return t;
}

mod.labs.forEach(L => {
  const html = build(L);
  fs.writeFileSync(path.join(OUT, L.file), html, 'utf8');
  console.log('wrote', L.file, html.length);
});
console.log('out =', OUT);
