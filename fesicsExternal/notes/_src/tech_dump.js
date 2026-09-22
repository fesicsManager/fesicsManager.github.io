// node tech_dump.js <dir> <out.txt> — Tech 계열(원리 탭 없음) 실험의 본문 텍스트 + JS 안 한국어 문자열 덤프
const fs = require('fs'), path = require('path');
const [,, dir, out] = process.argv;
const strip = h => h.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<style[\s\S]*?<\/style>/g, '')
  .replace(/<br\s*\/?>/g, '\n').replace(/<\/(p|li|h[1-6]|div|tr|section|label|option)>/g, '\n').replace(/<[^>]+>/g, '')
  .replace(/&nbsp;/g, ' ').replace(/&lsquo;|&rsquo;/g, "'").replace(/&ldquo;|&rdquo;/g, '"').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
  .replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
let buf = '';
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html') && f !== 'index.html').sort()) {
  const s = fs.readFileSync(path.join(dir, f), 'utf8');
  buf += `\n\n########## ${f} ##########\n[body]\n${strip(s).replace(/\n\s*\n/g, '\n')}\n[js-text]\n`;
  const js = (s.match(/<script[\s\S]*?<\/script>/g) || []).join('\n');
  const seen = new Set();
  for (const m of js.matchAll(/(["'])((?:\\.|(?!\1)[^\\\n])*?)\1/g)) {
    const t = m[2].replace(/<[^>]+>/g, ' ').replace(/\\n/g, ' ').replace(/\s+/g, ' ').trim();
    if (t.length >= 25 && /[가-힣]/.test(t) && !seen.has(t)) { seen.add(t); buf += t + '\n'; }
  }
  // 템플릿 리터럴 안 텍스트
  for (const m of js.matchAll(/`([\s\S]*?)`/g)) {
    const t = m[1].replace(/<[^>]+>/g, ' ').replace(/\$\{[^}]*\}/g, '…').replace(/\s+/g, ' ').trim();
    if (t.length >= 25 && /[가-힣]/.test(t) && !seen.has(t)) { seen.add(t); buf += t + '\n'; }
  }
}
fs.writeFileSync(out, buf, 'utf8');
console.log('written', out, buf.length);
