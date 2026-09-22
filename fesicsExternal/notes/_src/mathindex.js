// usage: node mathindex.js <root> <backupRoot>  — adds 📝 노트 badges to fesicsMathLabs/index.html for existing notes
const fs = require('fs'), path = require('path');
const [,, root, bakRoot] = process.argv;
const rel = path.join('fesicsMathLabs', 'index.html');
const p = path.join(root, rel);
const bp = path.join(bakRoot, rel);
if (!fs.existsSync(bp)) { fs.mkdirSync(path.dirname(bp), { recursive: true }); fs.copyFileSync(p, bp); }
const notesDir = path.join(root, 'notes', 'fesicsMathLabs');
const files = fs.existsSync(notesDir) ? fs.readdirSync(notesDir).filter(f => f.endsWith('.html')) : [];
let html = fs.readFileSync(p, 'utf8');
html = html.replace(/<!-- fxNoteLink:start -->[\s\S]*?<!-- fxNoteLink:end -->\n?/, '');
const block = `<!-- fxNoteLink:start -->
<style>
.fx-card-wrap{position:relative}
.fx-card-wrap > a.card{padding-right:5.2rem}
.fx-note-badge{position:absolute;right:.7rem;top:.7rem;font-size:.78rem;font-weight:700;padding:.15rem .5rem;border-radius:.5rem;background:#e7f4f5;color:#12595f;text-decoration:none;border:1px solid transparent}
.fx-note-badge:hover{border-color:#2c8a94;background:#d8eef0}
</style>
<script>
(function(){
  var NOTES = ${JSON.stringify(Object.fromEntries(files.map(f => [f, 1])))};
  function decorate(){
    var cards = document.querySelectorAll('#list a.card');
    for (var i = 0; i < cards.length; i++) {
      var c = cards[i], f = c.getAttribute('href');
      if (!NOTES[f] || c.parentNode.classList.contains('fx-card-wrap')) continue;
      var w = document.createElement('div'); w.className = 'fx-card-wrap';
      c.parentNode.insertBefore(w, c); w.appendChild(c);
      var b = document.createElement('a'); b.className = 'fx-note-badge'; b.href = '../notes/fesicsMathLabs/' + f; b.title = '자습 노트: 개념 정리와 확인 문제'; b.textContent = '📝 노트';
      w.appendChild(b);
    }
  }
  if (typeof render === 'function') { var orig = render; render = function(){ orig(); decorate(); }; }
  decorate();
})();
</script>
<!-- fxNoteLink:end -->
`;
html = html.replace('</body>', block + '</body>');
fs.writeFileSync(p, html, 'utf8');
console.log('math index badges:', files.length);
