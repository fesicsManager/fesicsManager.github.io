/* 심화 레이어 — 시뮬은 그대로 두고 과제만 얹는다.
   페이지에서 window.FX_DEEP 를 정한 뒤 이 파일을 불러온다.
   FX_DEEP = {
     predict: { ask, options:[{v,label}], actual(row)→v, hide:['#why',...], go:'#goBtn' },
     tasks:   [{ title, desc, check(rows)→{done, msg}, q?:{ask, choices:[...], answer:index, why} }],
     problems:[{ q, choices:[...], answer:index, hint, sol }]
   }
   페이지 쪽 전역 rows·autoRec 를 그대로 쓴다. */
(function(){
  var C = window.FX_DEEP; if(!C) return;
  function $(s){ return document.querySelector(s); }
  function el(tag, cls, html){ var e=document.createElement(tag); if(cls) e.className=cls; if(html!=null) e.innerHTML=html; return e; }
  /* 페이지는 let rows 로 선언 → window 에 없고 전역 이름으로만 보인다 */
  function getRows(){ try{ return (typeof rows !== 'undefined' && rows) || window.rows || []; }catch(e){ return []; } }

  var css = el('style', null,
    '.dp-bar{display:none;margin:.6rem 0;padding:.7rem .85rem;border-radius:12px;border:1px dashed var(--warn,#ffb86b);background:rgba(255,184,107,.08)}'+
    'body.dp-on .dp-bar{display:block}'+
    '.dp-cover{position:relative}'+
    'body.dp-on.dp-hide .dp-blur{filter:blur(9px) brightness(.6)}'+
    'body.dp-on.dp-hide .dp-cover::after{content:"🔒 예측을 고르고 실험하면 그림이 보여요";position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;padding:1rem;font-weight:700;color:#fff;pointer-events:none}'+
    '.dp-bar .dp-ask{font-weight:700;margin-bottom:.45rem}'+
    '.dp-opts{display:flex;gap:.5rem;flex-wrap:wrap}'+
    '.dp-opt{flex:1 1 9rem;padding:.55rem .7rem;border-radius:10px;border:1px solid var(--line,#2b3550);background:var(--pan2,#1b2436);color:var(--tx,#e9eefb);font:inherit;cursor:pointer}'+
    '.dp-opt.sel{border-color:var(--warn,#ffb86b);background:rgba(255,184,107,.18);font-weight:700}'+
    '.dp-msg{margin-top:.45rem;font-size:.93rem;color:var(--mut,#9db0d4)}'+
    '.dp-msg.hit{color:var(--ac,#5ee0c8)} .dp-msg.miss{color:var(--bad,#ff7a8a)}'+
    '.dp-score{float:right;font-size:.85rem;color:var(--mut,#9db0d4)}'+
    '#deep .dp-card{background:var(--pan,#151d2d);border:1px solid var(--line,#2b3550);border-radius:14px;padding:1rem 1.1rem;margin-bottom:1rem}'+
    '#deep h3{margin:.1rem 0 .5rem;font-size:1.1rem}'+
    '#deep .dp-lead{color:var(--mut,#9db0d4);font-size:.95rem;margin:.2rem 0 .7rem}'+
    '.dp-task{border-top:1px solid var(--line,#2b3550);padding:.75rem 0}'+
    '.dp-task:first-of-type{border-top:0}'+
    '.dp-task .dp-st{display:inline-block;min-width:3.2rem;font-size:.82rem;padding:.1rem .45rem;border-radius:999px;margin-right:.4rem;background:#2a3350;color:var(--mut,#9db0d4);text-align:center}'+
    '.dp-task.done .dp-st{background:rgba(94,224,200,.18);color:var(--ac,#5ee0c8)}'+
    '.dp-prog{font-size:.9rem;color:var(--mut,#9db0d4);margin:.3rem 0}'+
    '.dp-q{margin-top:.5rem;padding:.6rem .75rem;border-radius:10px;background:var(--pan2,#1b2436)}'+
    '.dp-q.locked{opacity:.5}'+
    '.dp-ch{display:block;width:100%;text-align:left;margin:.3rem 0;padding:.45rem .65rem;border-radius:9px;border:1px solid var(--line,#2b3550);background:transparent;color:var(--tx,#e9eefb);font:inherit;cursor:pointer}'+
    '.dp-ch.ok{border-color:var(--ac,#5ee0c8);background:rgba(94,224,200,.12)}'+
    '.dp-ch.no{border-color:var(--bad,#ff7a8a);background:rgba(255,122,138,.1)}'+
    '.dp-ch:disabled{cursor:default}'+
    '.dp-fb{font-size:.93rem;margin-top:.35rem;line-height:1.65}'+
    '.dp-prob{border-top:1px solid var(--line,#2b3550);padding:.85rem 0}'+
    '.dp-prob:first-of-type{border-top:0}'+
    '.dp-prob .dp-qt{font-weight:600;margin-bottom:.35rem}'+
    '.dp-btns{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.4rem}'+
    '.dp-sm{padding:.35rem .7rem;border-radius:8px;border:1px solid var(--line,#2b3550);background:transparent;color:var(--mut,#9db0d4);font:inherit;font-size:.88rem;cursor:pointer}'+
    '.dp-go{padding:.55rem 1rem;border-radius:10px;border:0;background:var(--warn,#ffb86b);color:#1a1205;font:inherit;font-weight:700;cursor:pointer}'+
    '.dp-tag{display:inline-block;font-size:.78rem;padding:.05rem .45rem;border-radius:6px;background:rgba(122,162,255,.18);color:var(--ac2,#7aa2ff);margin-left:.3rem;vertical-align:middle}');
  document.head.appendChild(css);

  /* ---------- 탭 ---------- */
  var tabs = $('.tabs'); if(!tabs) return;
  var tab = el('button', 'tab', '🎯 심화 도전'); tab.dataset.t = 'deep'; tabs.appendChild(tab);
  var panel = el('section', 'panel'); panel.id = 'deep';
  var lastPanel = document.querySelectorAll('section.panel'); lastPanel = lastPanel[lastPanel.length-1];
  lastPanel.parentNode.insertBefore(panel, lastPanel.nextSibling);
  function show(id){
    document.querySelectorAll('.tab').forEach(function(x){ x.classList.toggle('on', x.dataset.t===id); });
    document.querySelectorAll('section.panel').forEach(function(p){ p.classList.toggle('on', p.id===id); });
    window.scrollTo({top:0, behavior:'smooth'});
  }
  tab.addEventListener('click', function(){ show('deep'); renderTasks(); });

  /* ---------- 1. 예측 → 검증 ---------- */
  var P = C.predict, pick = null, hits = 0, tries = 0, streak = 0, best = 0, waiting = false;
  var bar, msgEl, scoreEl;
  if(P){
    /* 페이지가 className 을 통째로 바꾸는 상자가 있어 클래스 대신 선택자 규칙으로 숨긴다 */
    if((P.hide||[]).length) document.head.appendChild(el('style', null, P.hide.map(function(s){ return 'body.dp-on.dp-hide '+s; }).join(',')+'{display:none!important}'));
    /* 그림(캔버스)에도 답이 적혀 있으면 흐리게 가리고 안내를 띄운다 */
    (P.cover||[]).forEach(function(s){ var e=$(s); if(!e) return; e.classList.add('dp-blur'); if(e.parentNode) e.parentNode.classList.add('dp-cover'); });
    var go = $(P.go||'#goBtn');
    bar = el('div', 'dp-bar',
      '<span class="dp-score"></span><div class="dp-ask">🎯 먼저 예측: '+P.ask+'</div>'+
      '<div class="dp-opts">'+P.options.map(function(o,i){ return '<button type="button" class="dp-opt" data-i="'+i+'">'+o.label+'</button>'; }).join('')+'</div>'+
      '<div class="dp-msg">예측을 고른 뒤 실험 버튼을 누르세요. 설명은 기록한 뒤에 열려요.</div>');
    var host = go ? go.closest('.row') : null;
    (host||$('#explore .side')||document.body).parentNode.insertBefore(bar, host||null);
    msgEl = bar.querySelector('.dp-msg'); scoreEl = bar.querySelector('.dp-score');
    bar.querySelectorAll('.dp-opt').forEach(function(b){ b.addEventListener('click', function(){
      if(waiting) return;  /* 실험이 돌아가는 동안은 예측을 바꿀 수 없음 */
      bar.querySelectorAll('.dp-opt').forEach(function(x){ x.classList.remove('sel'); });
      b.classList.add('sel'); pick = P.options[+b.dataset.i].v;
      msgEl.className='dp-msg'; msgEl.textContent='예측: '+P.options[+b.dataset.i].label.replace(/<[^>]*>/g,'')+' — 이제 실험 버튼을 눌러 확인하세요.';
    }); });
    if(go) go.addEventListener('click', function(ev){
      if(!document.body.classList.contains('dp-on')) return;
      if(pick===null){ ev.stopImmediatePropagation(); ev.preventDefault();
        msgEl.className='dp-msg miss'; msgEl.textContent='먼저 위에서 예측을 골라 주세요.'; return; }
      waiting = true;
      document.body.classList.remove('dp-hide');  /* 예측을 정했으니 실험 그림부터 보여 준다 */
    }, true);
    function hideAgain(){
      if(!document.body.classList.contains('dp-on') || waiting) return;
      if(!document.body.classList.contains('dp-hide')){ msgEl.className='dp-msg'; msgEl.textContent='새 설정이에요. 예측을 고른 뒤 실험 버튼을 누르세요.'; }
      document.body.classList.add('dp-hide');
    }
    document.querySelectorAll('#explore input').forEach(function(s){
      s.addEventListener('input', hideAgain); s.addEventListener('change', hideAgain);
    });
    var orig = window.autoRec;
    if(typeof orig === 'function') window.autoRec = function(){
      var n = getRows().length; orig.apply(this, arguments);
      var rs = getRows(); if(rs.length === n) { waiting=false; return; }
      document.body.classList.remove('dp-hide');
      if(document.body.classList.contains('dp-on') && waiting && pick!==null){
        var real = P.actual(rs[rs.length-1]); tries++;
        var ok = real === pick; if(ok){ hits++; streak++; best = Math.max(best, streak); } else streak = 0;
        var lab = P.options.filter(function(o){ return o.v===real; })[0];
        msgEl.className = 'dp-msg '+(ok?'hit':'miss');
        msgEl.innerHTML = ok ? '🎉 예측 적중! 아래 설명으로 왜 그런지 확인해 보세요.'
                             : '😮 빗나갔어요. 실제는 <b>'+(lab?lab.label:real)+'</b> — 아래 설명에서 어디서 갈렸는지 찾아보세요.';
        scoreEl.textContent = '적중 '+hits+' / '+tries+' · 연속 '+streak;
        var g = $('#dpGoal'); if(g) g.innerHTML = best>=5 ? '🏆 목표 달성! 최고 연속 적중 '+best+'번' : '지금 연속 '+streak+'번 · 최고 '+best+'번';
        pick = null; bar.querySelectorAll('.dp-opt').forEach(function(x){ x.classList.remove('sel'); });
        renderTasks();
      }
      waiting = false; renderTasks();
    };
  }
  function setPredict(on){
    document.body.classList.toggle('dp-on', on);
    document.body.classList.toggle('dp-hide', on);
    var cb = $('#dpToggle'); if(cb) cb.checked = on;
  }

  /* ---------- 화면: 심화 탭 ---------- */
  var html = '';
  if(P) html +=
    '<div class="dp-card"><h3>1. 예측하고 검증하기</h3>'+
    '<p class="dp-lead">설명을 보기 전에 결과를 먼저 예측하고, 실험으로 맞는지 확인해요. 예측 모드에서는 설정을 바꿀 때마다 설명이 숨겨졌다가 기록하면 열려요.</p>'+
    '<label style="display:flex;gap:.5rem;align-items:center;margin-bottom:.6rem"><input type="checkbox" id="dpToggle"> 예측 모드 켜기</label>'+
    '<button class="dp-go" id="dpStart">예측 모드로 자유 탐구 시작 →</button>'+
    '<p class="dp-lead" style="margin-top:.6rem">목표: <b>5번 연속</b> 적중 · <span id="dpGoal">아직 예측 기록 없음</span></p></div>';
  if(C.tasks && C.tasks.length) html +=
    '<div class="dp-card"><h3>2. 분석 과제 <span class="dp-tag">여러 변수</span></h3>'+
    '<p class="dp-lead">자유 탐구에서 조건에 맞게 기록하면 과제가 풀리고, 규칙을 묻는 질문이 열려요.</p><div id="dpTasks"></div></div>';
  if(C.problems && C.problems.length) html +=
    '<div class="dp-card"><h3>3. 수능·내신형 문제 <span class="dp-tag">고난도</span></h3>'+
    '<p class="dp-lead">이 실험에서 본 원리로 푸는 문제예요. 페직스가 만든 문제이며 기출 문항이 아니에요.</p><div id="dpProbs"></div></div>';
  panel.innerHTML = html;

  if(P){
    $('#dpToggle').addEventListener('change', function(){ setPredict(this.checked); });
    $('#dpStart').addEventListener('click', function(){ setPredict(true); show('explore'); });
  }

  /* 선택지 공통 */
  function choiceBlock(box, q, onDone){
    var fb = el('div', 'dp-fb');
    q.choices.forEach(function(c, i){
      var b = el('button', 'dp-ch', (i+1)+'. '+c); b.type='button';
      b.addEventListener('click', function(){
        var ok = i === q.answer;
        b.classList.add(ok?'ok':'no');
        if(ok){ box.querySelectorAll('.dp-ch').forEach(function(x){ x.disabled = true; });
          fb.innerHTML = '✅ 맞아요. '+(q.why||q.sol||''); if(onDone) onDone(); }
        else fb.innerHTML = '❌ 다시 생각해 보세요.'+(q.hint?' 힌트: '+q.hint:'');
      });
      box.appendChild(b);
    });
    box.appendChild(fb);
  }

  /* 분석 과제 */
  var solved = {};
  function renderTasks(){
    var wrap = $('#dpTasks'); if(!wrap) return;
    var rs = getRows();
    if(!wrap.dataset.built){
      wrap.dataset.built = 1;
      C.tasks.forEach(function(t, i){
        var d = el('div', 'dp-task'); d.id = 'dpT'+i;
        d.innerHTML = '<div><span class="dp-st">진행 중</span><b>'+t.title+'</b></div><div class="dp-lead" style="margin:.25rem 0">'+t.desc+'</div><div class="dp-prog"></div>';
        if(t.q){ var q = el('div', 'dp-q locked', '<div style="font-weight:600;margin-bottom:.2rem">🔒 '+t.q.ask+'</div>'); q.dataset.ask = t.q.ask; d.appendChild(q); }
        wrap.appendChild(d);
      });
    }
    C.tasks.forEach(function(t, i){
      var d = $('#dpT'+i), r;
      try{ r = t.check(rs) || {}; }catch(e){ r = {done:false, msg:''}; }
      d.querySelector('.dp-prog').innerHTML = r.msg || '';
      if(r.done && !d.classList.contains('done')){
        d.classList.add('done'); d.querySelector('.dp-st').textContent = '달성';
        var q = d.querySelector('.dp-q');
        if(q && !q.dataset.open){ q.dataset.open = 1; q.classList.remove('locked');
          q.innerHTML = '<div style="font-weight:600;margin-bottom:.2rem">'+q.dataset.ask+'</div>';
          choiceBlock(q, t.q, function(){ solved[i] = 1; }); }
      }
    });
  }

  /* 문제 */
  var pb = $('#dpProbs');
  if(pb) C.problems.forEach(function(p, i){
    var d = el('div', 'dp-prob', '<div class="dp-qt">문제 '+(i+1)+'. '+p.q+'</div>');
    var box = el('div'); d.appendChild(box);
    choiceBlock(box, {choices:p.choices, answer:p.answer, hint:p.hint, why:'<br>'+p.sol});
    var btns = el('div', 'dp-btns');
    var sb = el('button', 'dp-sm', '풀이 보기'); sb.type='button';
    sb.addEventListener('click', function(){ var f = box.querySelector('.dp-fb'); f.innerHTML = '📘 풀이: '+p.sol; });
    btns.appendChild(sb); d.appendChild(btns);
    pb.appendChild(d);
  });

  renderTasks();
})();
