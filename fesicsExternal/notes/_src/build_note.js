// 자습 노트(독립 페이지) 생성기
// 사용: node build_note.js <note.json> <out.html>
// JSON 필드: unit,title,lead,flow[],lab{href,label},recall{intro,table,note},concepts[],formula,cuts[],examples[],quiz[],checklist[],next{text,href,label},index
const fs = require('fs');
const [,, jsonPath, outPath] = process.argv;
if (!jsonPath || !outPath) { console.error('usage: node build_note.js note.json out.html'); process.exit(1); }
const n = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));

const esc = s => String(s == null ? '' : s).replace(/&(?!(amp|lt|gt|quot|#\d+|[a-z]+);)/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const raw = s => String(s == null ? '' : s);

const CSS = `
:root{
  --paper:#EDF0F4; --card:#FFFFFF; --ink:#17253A; --ink-soft:#56657C; --rule:#C9D3DF;
  --marker:#FFD84D; --teal:#2F6F62; --teal-soft:#E2EDE9; --wrong:#B23A48; --brass:#B7791F; --brass-soft:#FFF4DF;
  --r:10px; --serif:"Gowun Batang", serif; --sans:"Noto Sans KR", system-ui, sans-serif;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0; background:var(--paper); color:var(--ink); font-family:var(--sans); font-size:16px; line-height:1.75}
.wrap{max-width:760px; margin:0 auto; padding:0 20px 80px}
.topbar{display:flex; justify-content:space-between; align-items:center; gap:10px; padding:14px 0 0; font-size:13px}
.topbar a{color:var(--teal); text-decoration:none; font-weight:500}
.topbar a:hover{text-decoration:underline}
header{padding:22px 0 22px;
  background:repeating-linear-gradient(to right, rgba(47,111,98,.07) 0 1px, transparent 1px 22px),
             repeating-linear-gradient(to bottom, rgba(47,111,98,.07) 0 1px, transparent 1px 22px);
  border-bottom:1px solid var(--rule); margin-bottom:34px}
.unit{font-size:13px; color:var(--teal); letter-spacing:.02em; margin:0 0 6px}
h1{font-family:var(--serif); font-size:31px; font-weight:700; line-height:1.3; margin:0 0 14px}
.lead{margin:0; color:var(--ink-soft); font-size:15px; max-width:62ch}
.flow{display:flex; flex-wrap:wrap; gap:6px; margin:18px 0 0; padding:0; list-style:none; font-size:13px}
.flow li{display:flex; align-items:center; gap:6px; color:var(--ink-soft)}
.flow li::after{content:"›"; color:var(--rule); margin-left:2px}
.flow li:last-child::after{content:""}
.flow .done{color:var(--teal)}
.flow .now{background:var(--ink); color:#fff; padding:3px 11px; border-radius:99px; font-weight:500}
section{margin:0 0 40px}
h2{font-family:var(--serif); font-size:21px; font-weight:700; margin:0 0 4px; padding-bottom:8px; border-bottom:2px solid var(--ink); display:inline-block}
h3{font-size:16px; font-weight:700; margin:24px 0 6px}
p{margin:10px 0}
ul{padding-left:1.2em}
.mark{background:linear-gradient(transparent 58%, var(--marker) 58%); font-weight:500}
.recall{background:var(--card); border:1px solid var(--rule); border-left:4px solid var(--teal); border-radius:var(--r); padding:18px 20px}
.recall .tag{font-size:13px; color:var(--teal); font-weight:700; margin:0 0 6px}
table{width:100%; border-collapse:collapse; margin:14px 0 4px; font-size:15px}
th,td{padding:8px 10px; border-bottom:1px solid var(--rule); text-align:center}
th{background:var(--teal-soft); font-weight:700}
td:first-child,th:first-child{text-align:left}
caption{caption-side:bottom; font-size:13px; color:var(--ink-soft); padding-top:8px; text-align:left}
.formula{background:var(--card); border:1px solid var(--rule); border-radius:var(--r); padding:20px; text-align:center; margin:18px 0}
.eq{font-family:var(--serif); font-size:22px; font-weight:700}
.units{font-size:14px; color:var(--ink-soft); margin:10px 0 0}
.cut{display:flex; gap:14px; align-items:flex-start; background:var(--card); border:1px dashed var(--rule); border-radius:var(--r); padding:16px 18px; margin:18px 0}
.who{flex:0 0 46px; height:46px; border-radius:50%; background:var(--teal-soft); color:var(--teal); display:grid; place-items:center; font-weight:700; font-size:12px; text-align:center; line-height:1.1}
.cut p{margin:0; font-size:15px}
.cut .src{font-size:13px; color:var(--ink-soft); margin-top:6px}
details{background:var(--card); border:1px solid var(--rule); border-radius:var(--r); padding:14px 18px; margin:14px 0}
summary{cursor:pointer; font-weight:700; list-style:none; line-height:1.6}
summary::-webkit-details-marker{display:none}
summary::after{content:"풀이 보기 +"; color:var(--teal); font-size:14px; font-weight:500; float:right; margin-left:12px}
details[open] summary::after{content:"접기 −"}
details[open]{border-color:var(--teal)}
.solution{margin-top:12px; padding-top:12px; border-top:1px solid var(--rule); font-size:15px}
.q{background:var(--card); border:1px solid var(--rule); border-radius:var(--r); padding:18px 20px; margin:14px 0}
.qnum{font-size:13px; color:var(--teal); font-weight:700; margin:0}
.qnum .kind{font-weight:400; color:var(--ink-soft); margin-left:6px}
.q p.stem{margin:4px 0 12px; font-weight:500}
.opts{display:grid; gap:8px}
.opt{text-align:left; font:inherit; font-size:15px; color:var(--ink); cursor:pointer; background:#fff; border:1px solid var(--rule); border-radius:8px; padding:10px 14px; transition:border-color .15s, background .15s}
.opt:hover:not(:disabled){border-color:var(--teal)}
.opt:focus-visible{outline:2px solid var(--teal); outline-offset:2px}
.opt.correct{border-color:var(--teal); background:var(--teal-soft); font-weight:700}
.opt.wrong{border-color:var(--wrong); color:var(--wrong)}
.opt:disabled{cursor:default}
.explain{display:none; margin-top:12px; padding-top:12px; border-top:1px solid var(--rule); font-size:14.5px; color:var(--ink-soft)}
.explain.show{display:block}
.explain .verdict{font-weight:700; margin:0 0 4px}
.explain .verdict.ok{color:var(--teal)}
.explain .verdict.no{color:var(--wrong)}
.explain .acts{display:flex; gap:8px; flex-wrap:wrap; margin-top:10px}
.explain .acts a,.explain .acts button{font:inherit; font-size:13px; padding:6px 12px; border-radius:8px; border:1px solid var(--rule); background:#fff; color:var(--ink); cursor:pointer; text-decoration:none}
.explain .acts a:hover,.explain .acts button:hover{border-color:var(--teal); color:var(--teal)}
.score{display:none; margin-top:14px; padding:14px 18px; border-radius:var(--r); background:var(--brass-soft); border:1px dashed var(--brass); font-size:15px}
.score.show{display:block}
.check{list-style:none; padding:0; margin:14px 0}
.check li{border-bottom:1px solid var(--rule)}
.check label{display:flex; gap:10px; align-items:flex-start; padding:11px 2px; cursor:pointer}
.check input{margin-top:6px; accent-color:var(--teal); width:17px; height:17px; flex:0 0 auto}
.check input:checked + span{color:var(--ink-soft); text-decoration:line-through}
.next{display:flex; justify-content:space-between; align-items:center; gap:16px; flex-wrap:wrap; background:var(--ink); color:#fff; border-radius:var(--r); padding:22px 24px}
.next h2{color:#fff; border-color:var(--marker); margin:0 0 4px}
.next p{margin:0; color:#C3CCDA; font-size:14.5px}
.next .links{display:flex; gap:8px; flex-wrap:wrap}
.btn{background:var(--marker); color:var(--ink); font:inherit; font-weight:700; font-size:15px; border:0; border-radius:8px; padding:12px 22px; cursor:pointer; text-decoration:none; white-space:nowrap}
.btn.ghost{background:transparent; color:#fff; border:1px solid #66748a}
.btn:focus-visible{outline:2px solid #fff; outline-offset:2px}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
@media (max-width:480px){h1{font-size:26px} body{font-size:15px}}
`;

const JS = `
document.querySelectorAll('.q').forEach(function(q,qi){
  var ans=parseInt(q.dataset.answer,10), opts=q.querySelectorAll('.opt'), ex=q.querySelector('.explain'), verdict=ex.querySelector('.verdict');
  var score=document.getElementById('score'), all=document.querySelectorAll('.q'), done=window.__done=window.__done||{};
  function updateScore(){
    if(Object.keys(done).length<all.length) return;
    var ok=0; for(var k in done) if(done[k]) ok++;
    score.classList.add('show');
    score.innerHTML = ok===all.length
      ? '<b>'+ok+' / '+all.length+' 정답!</b> 아래 점검 목록에 스스로 체크해 보고, 다음 단계로 넘어가세요.'
      : '<b>'+ok+' / '+all.length+' 정답.</b> 틀린 문제는 해설을 읽고 <b>실험으로 다시 확인</b>한 뒤, <b>다시 풀기</b>로 한 번 더 도전해 보세요.';
  }
  opts.forEach(function(btn,i){
    btn.addEventListener('click', function(){
      opts.forEach(function(b,j){ b.disabled=true; if(j===ans) b.classList.add('correct'); });
      var ok=(i===ans); if(!ok) btn.classList.add('wrong');
      verdict.className='verdict '+(ok?'ok':'no');
      verdict.textContent = ok ? '정답이에요.' : ('아직이에요. '+(btn.dataset.w||''));
      ex.classList.add('show'); done[qi]=ok; updateScore();
    });
  });
  ex.querySelector('[data-act=retry]').addEventListener('click', function(){
    opts.forEach(function(b){ b.disabled=false; b.classList.remove('correct','wrong'); });
    ex.classList.remove('show'); delete done[qi]; score.classList.remove('show');
  });
});
`;

function renderTable(t) {
  if (!t) return '';
  return `<table>${t.caption ? `<caption>${esc(t.caption)}</caption>` : ''}
<thead><tr>${t.head.map(h => `<th>${esc(h)}</th>`).join('')}</tr></thead>
<tbody>${t.rows.map(r => `<tr>${r.map(c => `<td>${esc(c)}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
}

const flow = (n.flow || []).map(f => `<li${f.state ? ` class="${f.state}"` : ''}>${esc(f.label)}</li>`).join('');
const concepts = (n.concepts || []).map((c, i) => `<h3>${i + 1}. ${esc(c.h)}</h3>${raw(c.html)}`).join('');
const formula = n.formula ? `<div class="formula"><div class="eq">${raw(n.formula.eq)}</div>${n.formula.units ? `<p class="units">${esc(n.formula.units)}</p>` : ''}</div>` : '';
const cuts = (n.cuts || []).map(c => `<div class="cut"><div class="who">${raw(c.who)}</div><div><p>${raw(c.quote)}</p><p class="src">${raw(c.src)}</p></div></div>`).join('');
const examples = (n.examples || []).map(e => `<details><summary>${raw(e.q)}</summary><div class="solution">${raw(e.solution)}</div></details>`).join('');
const labHref = n.lab ? esc(n.lab.href) : '#';
const quiz = (n.quiz || []).map((q, qi) => {
  const wrong = q.wrong || {};
  const opts = q.opts.map((o, i) => `<button type="button" class="opt" data-w="${esc(wrong[i] || '')}">${raw(o)}</button>`).join('');
  return `<div class="q" data-answer="${q.ans}">
<p class="qnum">${qi + 1}번${q.kind ? `<span class="kind">· ${esc(q.kind)}</span>` : ''}</p>
<p class="stem">${raw(q.stem)}</p>
<div class="opts">${opts}</div>
<div class="explain"><p class="verdict"></p><div>${raw(q.explain)}</div><div class="acts"><a href="${labHref}">🔬 실험으로 다시 확인</a><button type="button" data-act="retry">↺ 다시 풀기</button></div></div>
</div>`;
}).join('');
const checks = (n.checklist || []).map(c => `<li><label><input type="checkbox"><span>${raw(c)}</span></label></li>`).join('');
const nextLinks = [];
if (n.next && n.next.href) nextLinks.push(`<a class="btn" href="${esc(n.next.href)}">${esc(n.next.label || '다음으로')}</a>`);
if (n.lab) nextLinks.push(`<a class="btn ghost" href="${labHref}">실험 다시 하기</a>`);
const next = n.next ? `<section class="next"><div><h2>다음 단계</h2><p>${raw(n.next.text)}</p></div><div class="links">${nextLinks.join('')}</div></section>` : '';

const html = `<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>자습 노트 · ${esc(n.title)} | 제로 랩</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<style>${CSS}</style>
</head>
<body>
<div class="wrap">
<div class="topbar">${n.lab ? `<a href="${labHref}">← ${esc(n.lab.label || '실험실로')}</a>` : '<span></span>'}${n.index ? `<a href="${esc(n.index)}">실험 목록</a>` : ''}</div>
<header>
  <p class="unit">${esc(n.unit)}</p>
  <h1>${esc(n.title)}</h1>
  <p class="lead">${raw(n.lead)}</p>
  <ul class="flow">${flow}</ul>
</header>

<section>
  <h2>실험에서 얻은 것</h2>
  <div class="recall"><p class="tag">실험 데이터 되짚기</p>${raw(n.recall.intro)}${renderTable(n.recall.table)}${raw(n.recall.note)}</div>
</section>

<section>
  <h2>개념 정리</h2>
  ${concepts}${formula}${cuts}
</section>

${examples ? `<section><h2>예제</h2>${examples}</section>` : ''}

<section>
  <h2>확인 문제</h2>
  ${quiz}
  <div class="score" id="score"></div>
</section>

<section>
  <h2>스스로 점검</h2>
  <ul class="check">${checks}</ul>
</section>

${next}
</div>
<script>${JS}</script>
</body>
</html>
`;
fs.writeFileSync(outPath, html, 'utf8');
console.log('ok:', outPath);
