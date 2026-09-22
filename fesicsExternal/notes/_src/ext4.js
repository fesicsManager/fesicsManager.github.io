// usage: node ext4.js src\zerolabMathHigh out.txt [start] [end] — h1, controls, table head, analysis strings (zerolab family)
const fs = require('fs'), path = require('path');
const [,, dir, out, s0, e0] = process.argv;
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && f !== 'index.html').sort();
const start = +(s0 || 0), end = +(e0 || files.length);
const clean = h => h.replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/\s+/g, ' ').trim();
let o = '';
for (const f of files.slice(start, end)) {
  const s = fs.readFileSync(path.join(dir, f), 'utf8');
  const h1 = clean((s.match(/<h1[^>]*>([\s\S]*?)<\/h1>/) || ['', ''])[1]);
  const ctl = [...s.matchAll(/<div class="ctl">([\s\S]*?)<\/div>/g)].map(m => clean(m[1])).join(' | ');
  const th = [...s.matchAll(/<th[^>]*>([\s\S]*?)<\/th>/g)].map(m => clean(m[1])).join(' | ');
  const need = clean((s.match(/<div class="need"[^>]*>([\s\S]*?)<\/div>/) || ['', ''])[1]);
  const sc = (s.match(/<script>([\s\S]*)<\/script>/) || ['', ''])[1];
  const strs = [...sc.matchAll(/(['"`])((?:(?!\1)[^\\]|\\.){20,400})\1/g)].map(m => m[2]).filter(t => /[가-힣]/.test(t) && !/^\s*</.test(t.slice(0, 1)) || /정리|결론|분석|기록/.test(t));
  const hint = [...s.matchAll(/class="hint[^"]*"[^>]*>([\s\S]*?)<\//g)].map(m => clean(m[1])).join(' | ');
  o += `\n\n########## ${f} ##########\n[h1] ${h1}\n[ctl] ${ctl}\n[th] ${th}\n[hint] ${hint}\n[need] ${need}\n[strings]\n\n`;
}
fs.writeFileSync(out, o, 'utf8');
console.log('written', out, o.length, end - start);

