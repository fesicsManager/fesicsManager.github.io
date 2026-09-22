// usage: node ext3.js <srcdir> <out.txt> [startIdx] [endIdx] — math labs: principle + sliders + headA + conclusions
const fs = require('fs'), path = require('path');
const [,, dir, out, a0, a1] = process.argv;
const strip = h => h.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<style[\s\S]*?<\/style>/g, '')
  .replace(/<br\s*\/?>/g, '\n').replace(/<\/(p|li|h[1-6]|div|tr|summary)>/g, '\n').replace(/<[^>]+>/g, '')
  .replace(/&nbsp;/g, ' ').replace(/&lsquo;|&rsquo;/g, "'").replace(/&ldquo;|&rdquo;/g, '"').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
  .replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
let buf = '';
let files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && f !== 'index.html').sort();
if (a0 !== undefined) files = files.slice(+a0, a1 !== undefined ? +a1 : undefined);
for (const f of files) {
  const s = fs.readFileSync(path.join(dir, f), 'utf8');
  const h1 = (s.match(/<h1[^>]*>([\s\S]*?)<\/h1>/) || [])[1] || '';
  const lead = (s.match(/<p class="lead"[^>]*>([\s\S]*?)<\/p>/) || [])[1] || '';
  const pr = (s.match(/<section[^>]*id="fxPrinciple"[\s\S]*?<\/section>/) || s.match(/<details[^>]*id="fxPrinciple"[\s\S]*?<\/details>/) || [])[0] || '';
  const sl = (s.match(/sliders\s*:\s*\[([\s\S]*?)\n\s*\]/) || [])[1] || '';
  const sliders = [...sl.matchAll(/\{[^}]*\}/g)].map(m => m[0].replace(/\s+/g, ' ')).join('\n');
  const headA = (s.match(/headA\s*:\s*(\[[^\]]*\])/) || [])[1] || '';
  const conc = [...s.matchAll(/concl\s*=\s*'([^']{20,400})'/g)].map(m => m[1]).slice(0, 4).join('\n');
  const stats = [...s.matchAll(/\{t:'([^']+)'/g)].map(m => m[1]).join(' | ');
  const hint0 = (s.match(/hint0\s*:\s*'([^']*)'/) || [])[1] || '';
  buf += `\n\n########## ${f} ##########\n[h1] ${strip(h1)}\n[lead] ${strip(lead)}\n[hint0] ${hint0}\n[sliders]\n${sliders}\n[headA] ${headA}\n[stats] ${stats}\n[concl]\n${conc}\n[principle]\n${strip(pr).replace(/^📖.*\n?/, '')}\n`;
}
fs.writeFileSync(out, buf, 'utf8');
console.log('written', out, buf.length, files.length);
