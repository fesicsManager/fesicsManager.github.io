// 폴더 단위 일괄 적용
//   node apply_batch.js <fesicsExternal 루트> <백업 루트> <폴더1> [폴더2 ...]
// 1) content/<폴더>/<이름>.json → <루트>/notes/<폴더>/<이름>.html 생성
// 2) <루트>/<폴더>/<이름>.html 에 '📝 자습 노트' 탭 링크 + 마무리 안내 주입 (수정 전 사본을 백업 루트에 보관)
// 3) <루트>/index.html 의 해당 실험 항목에 노트 링크 추가 (수정 전 사본 백업)
// 여러 번 실행해도 결과가 같다 (마커 블록을 찾아 교체).
const fs = require('fs'), path = require('path'), cp = require('child_process');
const [,, root, backupRoot, ...folders] = process.argv;
if (!root || !backupRoot || !folders.length) { console.error('usage: node apply_batch.js <root> <backupRoot> <folder...>'); process.exit(1); }
const here = __dirname;

function backup(rel) {
  const src = path.join(root, rel), dst = path.join(backupRoot, rel);
  if (fs.existsSync(dst)) return; // 최초 1회만 (원본 상태 보존)
  fs.mkdirSync(path.dirname(dst), { recursive: true });
  fs.copyFileSync(src, dst);
}

// ---------- 2) 실험 파일 주입 ----------
function labInjection(noteRel) {
  return `<!-- fxNoteLink:start -->
<style>
.fx-note-cta{margin-top:18px;padding:16px 18px;border-radius:14px;background:#fff8ee;border:1px dashed #d98e3b;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;font-size:.98rem;line-height:1.6}
.fx-note-cta a{display:inline-block;background:#173238;color:#fff;text-decoration:none;font-weight:700;padding:10px 18px;border-radius:10px;white-space:nowrap}
.fx-note-cta a:hover{filter:brightness(1.15)}
</style>
<script>
(function(){
  var href='${noteRel}';
  var ok=function(el){ return el && !/^(BUTTON|A|INPUT|NAV)$/.test(el.tagName) ? el : null; };
  var host=ok(document.getElementById('validationContent'))||ok(document.getElementById('verifyContent'))||ok(document.getElementById('verifyTab'))
    ||ok(document.getElementById('panel-verify'))||ok(document.getElementById('panel-validate'))||ok(document.getElementById('verifyBody'))
    ||ok(document.querySelector('#tab-validate .card, #tab-validate, #tab-verify .card, #tab-verify'))
    ||ok(document.querySelector('section#verify, section#validate, #verify.panel, #validate.panel'))
    ||ok(document.querySelector('#paneB .card, #paneB'))
    ||ok(document.querySelector('#panelB .card, #panelB'))
    ||ok(document.querySelector('.app, main, .wrap'))||document.body;
  if(host){
    var d=document.createElement('div'); d.className='fx-note-cta';
    d.innerHTML='<div>📝 실험을 마쳤다면 <b>자습 노트</b>에서 개념을 정리하고 확인 문제를 풀어 보세요.</div><a href="'+href+'">자습 노트 열기 →</a>';
    host.appendChild(d);
  }
})();
</script>
<!-- fxNoteLink:end -->`;
}

function injectLab(labRel, noteRel) {
  backup(labRel);
  const p = path.join(root, labRel);
  let html = fs.readFileSync(p, 'utf8');
  html = html.replace(/<!-- fxNoteLink:start -->[\s\S]*?<!-- fxNoteLink:end -->\n?/, '');
  html = html.replace('</body>', labInjection(noteRel) + '\n</body>');
  fs.writeFileSync(p, html, 'utf8');
}

// ---------- 3) index.html ----------
const INDEX_CSS = `/*<!-- fxNoteLink:css:start -->*/
.lab{position:relative}
.lab a.note{position:absolute;right:6px;top:8px;display:inline-block;padding:2px 8px;border-radius:6px;font-size:.78rem;line-height:1.5;background:#e7f4f5;color:var(--teal-dark);text-decoration:none;border:1px solid transparent}
.lab a.note:hover{border-color:var(--teal);background:#d8eef0}
.lab:has(a.note) > a:first-child{padding-right:70px}
@media (max-width:520px){.lab a.note{font-size:.72rem;padding:1px 6px}.lab:has(a.note) > a:first-child{padding-right:56px}}
/*<!-- fxNoteLink:css:end -->*/
`;
function updateIndex(entries) {
  backup('index.html');
  const p = path.join(root, 'index.html');
  let html = fs.readFileSync(p, 'utf8');
  html = html.replace(/\/\*<!-- fxNoteLink:css:start -->\*\/[\s\S]*?\/\*<!-- fxNoteLink:css:end -->\*\/\n?/, '');
  html = html.replace('</style>', INDEX_CSS + '</style>');
  let added = 0, missing = [];
  for (const { labRel, noteRel } of entries) {
    const key = labRel.replace(/\\/g, '/');
    const re = new RegExp(`(<li class="lab[^"]*"><a href="${key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}">[\\s\\S]*?</a>)(<a class="note"[^>]*>[^<]*</a>)?(</li>)`);
    if (!re.test(html)) { missing.push(key); continue; }
    html = html.replace(re, `$1<a class="note" href="${noteRel}" title="자습 노트: 개념 정리와 확인 문제">📝 노트</a>$3`);
    added++;
  }
  fs.writeFileSync(p, html, 'utf8');
  return { added, missing };
}

// ---------- main ----------
const entries = [];
for (const folder of folders) {
  const cdir = path.join(here, 'content', folder);
  if (!fs.existsSync(cdir)) { console.warn('no content dir:', cdir); continue; }
  const outDir = path.join(root, 'notes', folder);
  fs.mkdirSync(outDir, { recursive: true });
  for (const f of fs.readdirSync(cdir).filter(f => f.endsWith('.json')).sort()) {
    const name = f.replace(/\.json$/, '');
    const labRel = path.join(folder, name + '.html');
    if (!fs.existsSync(path.join(root, labRel))) { console.warn('lab not found, skip:', labRel); continue; }
    const noteOut = path.join(outDir, name + '.html');
    cp.execFileSync('node', [path.join(here, 'build_note.js'), path.join(cdir, f), noteOut], { stdio: 'inherit' });
    const noteRelFromLab = `../notes/${folder}/${name}.html`;
    const noteRelFromIndex = `notes/${folder}/${name}.html`;
    injectLab(labRel, noteRelFromLab);
    entries.push({ labRel, noteRel: noteRelFromIndex });
    console.log('lab linked:', labRel);
  }
}
const r = updateIndex(entries);
console.log(`index: ${r.added} linked` + (r.missing.length ? `, missing: ${r.missing.join(', ')}` : ''));
