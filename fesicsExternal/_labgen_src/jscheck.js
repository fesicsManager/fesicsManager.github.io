// Inline <script> syntax check for HTML files. Usage: node jscheck.js <file|dir> ...
const fs = require('fs'), path = require('path'), vm = require('vm');
let files = [];
for (const a of process.argv.slice(2)) {
  const st = fs.statSync(a);
  if (st.isDirectory()) {
    const walk = d => { for (const e of fs.readdirSync(d, { withFileTypes: true })) { const p = path.join(d, e.name); if (e.isDirectory()) walk(p); else if (p.endsWith('.html')) files.push(p); } };
    walk(a);
  } else files.push(a);
}
let bad = 0, ok = 0;
for (const f of files) {
  const html = fs.readFileSync(f, 'utf8');
  const re = /<script(\s[^>]*)?>([\s\S]*?)<\/script>/gi;
  let m, i = 0, errs = [];
  while ((m = re.exec(html))) {
    i++;
    const attrs = m[1] || '';
    if (/\bsrc\s*=/.test(attrs)) continue;
    if (/type\s*=\s*["'](?!(text\/javascript|module|application\/javascript)["'])/i.test(attrs)) continue;
    try { new vm.Script(m[2], { filename: f + '#' + i }); } catch (e) { errs.push(`script#${i}: ${e.message}`); }
  }
  // duplicate ids
  const ids = {}; const idRe = /\sid\s*=\s*["']([^"']+)["']/g; let dm;
  while ((dm = idRe.exec(html))) { ids[dm[1]] = (ids[dm[1]] || 0) + 1; }
  const dups = Object.keys(ids).filter(k => ids[k] > 1);
  if (dups.length) errs.push('dup ids: ' + dups.join(','));
  if (errs.length) { bad++; console.log('FAIL ' + f + '\n  ' + errs.join('\n  ')); } else ok++;
}
console.log(`checked ${files.length}: ok ${ok}, fail ${bad}`);
