// 실험 HTML에서 노트 작성용 원자료(제목·소개·과학 원리·확인 문제·수치)를 추출해 텍스트로 덤프
// 사용: node extract_sources.js <folder> <out.txt>
const fs = require('fs'), path = require('path');
const [,, dir, out] = process.argv;
const strip = h => h.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<style[\s\S]*?<\/style>/g, '')
  .replace(/<br\s*\/?>/g, '\n').replace(/<\/(p|li|h[1-6]|div|tr)>/g, '\n').replace(/<[^>]+>/g, '')
  .replace(/&nbsp;/g, ' ').replace(/&lsquo;|&rsquo;/g, "'").replace(/&ldquo;|&rdquo;/g, '"').replace(/&amp;/g, '&')
  .replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
let buf = '';
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort()) {
  const s = fs.readFileSync(path.join(dir, f), 'utf8');
  const title = (s.match(/<title>(.*?)<\/title>/) || [])[1] || '';
  const head = (s.match(/<header class="page-head">([\s\S]*?)<\/header>/) || [])[1] || '';
  const pr = (s.match(/<section id="fxPrinciple"[\s\S]*?<\/section>/) || [])[0] || '';
  const val = (s.match(/<div class="tab-panel" id="tab-validate">([\s\S]*?)<div class="mini-toast"/) || [])[1] || '';
  const ctrl = (s.match(/<div class="control-block">([\s\S]*?)<\/div>\s*<\/div>/) || [])[1] || '';
  const insight = (s.match(/<div class="insight-box[^"]*"[^>]*>([\s\S]*?)<\/div>/) || [])[1] || '';
  // 스크립트 안의 주요 상수/피드백 문자열
  const js = s.match(/<script>([\s\S]*?)<\/script>/g) || [];
  const big = js.map(x => x).sort((a, b) => b.length - a.length)[0] || '';
  const consts = (big.match(/(?:var|const|let)\s+[A-Za-z_]\w*\s*=\s*[-\d.]+[^;\n]*/g) || []).slice(0, 25).join('\n');
  const fb = (big.match(/['"][^'"\n]{12,120}(정답|맞아|틀렸|아쉽|다시|입니다|이에요|예요|해요)[^'"\n]*['"]/g) || []).slice(0, 20).join('\n');
  buf += `\n\n########## ${f} ##########\n[title] ${title}\n[head]\n${strip(head)}\n[control]\n${strip(ctrl)}\n[insight]\n${strip(insight)}\n[principle]\n${strip(pr)}\n[validate]\n${strip(val)}\n[consts]\n${consts}\n[feedback]\n${fb}\n`;
}
fs.writeFileSync(out, buf, 'utf8');
console.log('written', out, buf.length);
