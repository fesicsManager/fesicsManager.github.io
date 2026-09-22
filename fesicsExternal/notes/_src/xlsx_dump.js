// 압축 해제된 xlsx 폴더에서 시트별 텍스트 덤프
// node xlsx_dump.js <unzipped_dir> <out_dir>
const fs = require('fs'), path = require('path');
const [,, dir, out] = process.argv;
fs.mkdirSync(out, { recursive: true });
const dec = s => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&amp;/g, '&').replace(/_x000D_/g, '');
const ssXml = fs.readFileSync(path.join(dir, 'xl/sharedStrings.xml'), 'utf8');
const ss = [];
for (const m of ssXml.matchAll(/<si>([\s\S]*?)<\/si>/g)) {
  ss.push(dec([...m[1].matchAll(/<t[^>]*>([\s\S]*?)<\/t>/g)].map(x => x[1]).join('')));
}
const wb = fs.readFileSync(path.join(dir, 'xl/workbook.xml'), 'utf8');
const rels = fs.readFileSync(path.join(dir, 'xl/_rels/workbook.xml.rels'), 'utf8');
const relMap = {};
for (const m of rels.matchAll(/<Relationship [^>]*Id="([^"]+)"[^>]*Target="([^"]+)"/g)) relMap[m[1]] = m[2];
for (const m of rels.matchAll(/<Relationship [^>]*Target="([^"]+)"[^>]*Id="([^"]+)"/g)) relMap[m[2]] = m[1];
for (const m of wb.matchAll(/<sheet [^>]*name="([^"]+)"[^>]*r:id="([^"]+)"/g)) {
  const name = dec(m[1]), target = relMap[m[2]];
  const xml = fs.readFileSync(path.join(dir, 'xl', target.replace(/^\/xl\//, '')), 'utf8');
  const lines = [];
  for (const r of xml.matchAll(/<row [^>]*>([\s\S]*?)<\/row>/g)) {
    const cells = [];
    for (const c of r[1].matchAll(/<c r="([A-Z]+)\d+"([^>]*)>([\s\S]*?)<\/c>/g)) {
      const t = (c[2].match(/t="([^"]+)"/) || [])[1];
      let v = (c[3].match(/<v>([\s\S]*?)<\/v>/) || [])[1];
      if (t === 's') v = ss[parseInt(v, 10)];
      else if (t === 'inlineStr') v = dec([...c[3].matchAll(/<t[^>]*>([\s\S]*?)<\/t>/g)].map(x => x[1]).join(''));
      if (v != null && String(v).trim()) cells.push(String(v).replace(/\s*\n\s*/g, ' / ').trim());
    }
    if (cells.length) lines.push(cells.join(' | '));
  }
  const fn = path.join(out, name.replace(/[\\/:*?"<>|]/g, '_') + '.txt');
  fs.writeFileSync(fn, lines.join('\n'), 'utf8');
  console.log(name, lines.length, 'rows');
}
