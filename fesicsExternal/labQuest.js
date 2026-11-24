/* ===========================================================
   labQuest.js — 엔진형 실험실(빛·하늘·회로)에 붙이는 '문제 풀기' 상자 (261124)
   사용:
     LabQuest.init({
       lab: 'optics',               // 기록 이름
       mount: 요소,                  // 이 요소 앞에 상자를 넣는다
       level: function(){...},      // 지금 수준(1 초등·2 중등·3 고등)
       setLevel: function(lv){...}, // 문제 수준으로 바꾸기
       hide: ['imgCard'],           // 풀기 전까지 가릴 칸(답이 보이는 칸)
       quests: [{id, lv, title, text, kind:'num'|'choice', unit, answer, tol,
                 choices:[..], hint, explain, setup(), reveal(ok, value)}]
     });
   주소에 ?quest=<id> 를 붙이면 그 문제로 바로 연다. ?quest=list 는 목록부터.
   =========================================================== */
(function(){
  var css = '' +
  '.lq{background:#fff8ec;border:2px solid #d98e3b;border-radius:14px;padding:12px 14px;margin:0 0 12px;}' +
  '.lq h2{font-size:17px;margin:0 0 6px;display:flex;align-items:center;gap:8px;flex-wrap:wrap;}' +
  '.lq .lqTop{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;}' +
  '.lq .lqStars{font-size:14px;color:#a86825;font-weight:700;}' +
  '.lq .lqChips{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0 4px;}' +
  '.lq .lqChip{font-size:13px;font-weight:700;padding:5px 10px;border-radius:999px;border:1.5px solid #e3c79f;background:#fff;color:#7a5420;cursor:pointer;}' +
  '.lq .lqChip.on{background:#d98e3b;color:#fff;border-color:#d98e3b;}' +
  '.lq .lqChip.done{border-color:#2f8f9d;color:#1f6d78;}' +
  '.lq .lqText{font-size:16px;line-height:1.6;margin:8px 0;color:#173238;}' +
  '.lq .lqRow{display:flex;gap:7px;flex-wrap:wrap;align-items:center;}' +
  '.lq input.lqNum{font:600 17px "IBM Plex Mono",monospace;width:120px;padding:8px 10px;border-radius:9px;border:2px solid #cddad6;}' +
  '.lq .lqUnit{font-weight:700;color:#4a636a;}' +
  '.lq button.lqBtn{font-weight:700;font-size:14.5px;padding:9px 14px;border-radius:9px;border:1.5px solid #cddad6;background:#fff;color:#4a636a;cursor:pointer;}' +
  '.lq button.lqGo{background:#d98e3b;border-color:#d98e3b;color:#fff;}' +
  '.lq .lqChoice{display:block;width:100%;text-align:left;margin:5px 0;font-size:15px;padding:9px 12px;border-radius:9px;border:1.5px solid #cddad6;background:#fff;cursor:pointer;color:#173238;}' +
  '.lq .lqChoice.pick{border-color:#d98e3b;background:#fff1dc;}' +
  '.lq .lqChoice.right{border-color:#2f8f9d;background:#e4f5f6;}' +
  '.lq .lqChoice.wrong{border-color:#c1443c;background:#fbeceb;text-decoration:line-through;}' +
  '.lq .lqMsg{margin-top:9px;font-size:15px;line-height:1.55;border-radius:10px;padding:9px 12px;display:none;}' +
  '.lq .lqMsg.ok{display:block;background:#e4f5f6;color:#1f6d78;animation:lqPop .35s;}' +
  '.lq .lqMsg.no{display:block;background:#fbeceb;color:#9c2f28;animation:lqShake .35s;}' +
  '.lq .lqMsg.info{display:block;background:#f6faf9;color:#4a636a;border:1px dashed #b7cdc9;}' +
  '@keyframes lqPop{0%{transform:scale(.92)}60%{transform:scale(1.03)}100%{transform:scale(1)}}' +
  '@keyframes lqShake{0%,100%{transform:translateX(0)}25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}' +
  '.lqOpen{font-weight:700;font-size:14.5px;padding:8px 14px;border-radius:999px;border:2.5px solid #d98e3b;background:#fff8ec;color:#a86825;cursor:pointer;}';

  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  var LQ = window.LabQuest = {};
  var cfg, box, cur = null, tries = 0, solved = false, pick = null, rec = {};

  function key(){ return 'fxLabQuest_' + cfg.lab; }
  function loadRec(){ try { rec = JSON.parse(localStorage.getItem(key()) || '{}') || {}; } catch (e) { rec = {}; } }
  function saveRec(){ try { localStorage.setItem(key(), JSON.stringify(rec)); } catch (e) {} }
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function val(q, k){ return typeof q[k] === 'function' ? q[k]() : q[k]; }
  function setHidden(on){
    (cfg.hide || []).forEach(function(id){
      var e = document.getElementById(id);
      if (e) e.classList.toggle('lqHide', on);
    });
  }
  var hs = document.createElement('style'); hs.textContent = '.lqHide{visibility:hidden !important;max-height:0;overflow:hidden;margin:0 !important;padding:0 !important;border:0 !important;}';
  document.head.appendChild(hs);

  function starsOf(t){ return t <= 1 ? 3 : (t === 2 ? 2 : 1); }
  function total(){ var s = 0; for (var k in rec) s += rec[k] || 0; return s; }

  function fmt(x){
    if (typeof x !== 'number') return x;
    return Math.abs(x - Math.round(x)) < 1e-9 ? String(Math.round(x)) : String(Math.round(x * 10) / 10);
  }

  function render(){
    var qs = cfg.quests;
    var h = '<div class="lqTop"><h2>🎮 문제 풀기</h2><span class="lqStars">⭐ ' + total() + ' / ' + (qs.length * 3) + '</span></div>';
    h += '<div class="lqChips">';
    qs.forEach(function(q, i){
      var d = rec[q.id] ? ' done' : '';
      h += '<button class="lqChip' + (cur === q ? ' on' : '') + d + '" data-i="' + i + '">' + (i + 1) + '. ' + esc(q.title) +
           (rec[q.id] ? ' ' + '★'.repeat(rec[q.id]) : '') + '</button>';
    });
    h += '<button class="lqChip" data-i="-1">✕ 닫기</button></div>';
    if (cur){
      h += '<div class="lqText">' + val(cur, 'text') + '</div>';
      if (cur.kind === 'choice'){
        cur.choices.forEach(function(c, i){
          h += '<button class="lqChoice" data-c="' + i + '">' + String.fromCharCode(9312 + i) + ' ' + esc(c) + '</button>';
        });
        h += '<div class="lqRow" style="margin-top:6px">';
      } else {
        h += '<div class="lqRow"><input class="lqNum" type="number" inputmode="decimal" step="any" placeholder="답"> <span class="lqUnit">' + esc(cur.unit || '') + '</span>';
      }
      h += '<button class="lqBtn lqGo" data-a="go">확인</button>' +
           '<button class="lqBtn" data-a="hint">힌트</button>' +
           '<button class="lqBtn" data-a="show">정답·해설</button>' +
           '<button class="lqBtn" data-a="next">다음 문제 ▶</button></div>';
      h += '<div class="lqMsg"></div>';
    } else {
      h += '<div class="lqText" style="font-size:14.5px;color:#4a636a">번호를 누르면 실험대가 문제 장면으로 바뀌어요. 먼저 생각하고 답을 넣은 뒤, 실험으로 맞는지 확인해 보세요. 한 번에 맞히면 별 3개예요.</div>';
    }
    box.innerHTML = h;
    var chips = box.querySelectorAll('.lqChip');
    for (var i = 0; i < chips.length; i++) chips[i].onclick = function(){
      var n = +this.dataset.i;
      if (n < 0){ LQ.close(); return; }
      LQ.open(cfg.quests[n].id);
    };
    var cs = box.querySelectorAll('.lqChoice');
    for (var j = 0; j < cs.length; j++) cs[j].onclick = function(){
      if (solved) return;
      pick = +this.dataset.c;
      for (var k = 0; k < cs.length; k++) cs[k].classList.toggle('pick', k === pick);
    };
    var bs = box.querySelectorAll('.lqBtn');
    for (var b = 0; b < bs.length; b++) bs[b].onclick = function(){ act(this.dataset.a); };
    var inp = box.querySelector('.lqNum');
    if (inp) inp.onkeydown = function(e){ if (e.key === 'Enter') act('go'); };
  }

  function msg(cls, html){
    var m = box.querySelector('.lqMsg');
    if (!m) return;
    m.className = 'lqMsg'; void m.offsetWidth; m.className = 'lqMsg ' + cls; m.innerHTML = html;
  }
  function answerText(q){
    if (q.kind === 'choice') return String.fromCharCode(9312 + q.answer) + ' ' + q.choices[q.answer];
    return fmt(val(q, 'answer')) + ' ' + (q.unit || '');
  }

  function act(a){
    var q = cur; if (!q) return;
    if (a === 'next'){
      var i = cfg.quests.indexOf(q);
      LQ.open(cfg.quests[(i + 1) % cfg.quests.length].id);
      return;
    }
    if (a === 'hint'){ msg('info', '💡 ' + val(q, 'hint')); return; }
    if (a === 'show'){
      solved = true; setHidden(false);
      if (q.kind === 'choice') markChoices(q);
      if (q.reveal) q.reveal(true, q.kind === 'choice' ? q.answer : val(q, 'answer'));
      msg('info', '정답: <b>' + esc(answerText(q)) + '</b><br>' + val(q, 'explain'));
      return;
    }
    if (a !== 'go' || solved) return;
    var ok, v;
    if (q.kind === 'choice'){
      if (pick === null){ msg('info', '보기 하나를 먼저 골라 주세요.'); return; }
      v = pick; ok = (pick === q.answer);
    } else {
      var s = (box.querySelector('.lqNum').value || '').trim();
      v = parseFloat(s);
      if (!isFinite(v)){ msg('info', '숫자로 넣어 주세요.'); return; }
      var ans = val(q, 'answer'), tol = q.tol === undefined ? Math.max(0.5, Math.abs(ans) * 0.03) : val(q, 'tol');
      ok = Math.abs(v - ans) <= tol;
    }
    tries++;
    if (q.reveal) q.reveal(ok, v);
    if (ok){
      solved = true; setHidden(false);
      var s3 = starsOf(tries);
      if (!rec[q.id] || rec[q.id] < s3){ rec[q.id] = s3; saveRec(); }
      if (q.kind === 'choice') markChoices(q);
      msg('ok', '🎉 정답! ' + '⭐'.repeat(s3) + '<br>' + val(q, 'explain'));
      var st2 = box.querySelector('.lqStars'); if (st2) st2.textContent = '⭐ ' + total() + ' / ' + (cfg.quests.length * 3);
      if (cfg.onSolved) try { cfg.onSolved(q); } catch (e) {}
      try { parent.postMessage({type:'fesicsLabQuest', lab:cfg.lab, id:q.id, stars:s3}, '*'); } catch (e) {}
    } else {
      if (q.kind === 'choice'){
        var cs = box.querySelectorAll('.lqChoice'); if (cs[v]) cs[v].classList.add('wrong');
        pick = null;
        msg('no', '아쉬워요. 다른 보기를 골라 보세요.' + (tries >= 2 ? ' 힌트를 눌러 봐도 좋아요.' : ''));
      } else {
        var ans2 = val(q, 'answer');
        msg('no', '아쉬워요. 실험대를 보면 실제 결과가 나와 있어요. ' + (v < ans2 ? '조금 더 큰' : '조금 더 작은') + ' 값이에요.' + (tries >= 2 ? ' 힌트를 눌러 봐도 좋아요.' : ''));
      }
    }
  }
  function markChoices(q){
    var cs = box.querySelectorAll('.lqChoice');
    for (var k = 0; k < cs.length; k++){ cs[k].classList.remove('pick'); if (k === q.answer) cs[k].classList.add('right'); }
  }

  LQ.open = function(id){
    var q = null;
    cfg.quests.forEach(function(x){ if (x.id === id) q = x; });
    if (!q) return;
    cur = q; tries = 0; solved = false; pick = null;
    box.style.display = '';
    if (cfg.setLevel && q.lv && cfg.level && cfg.level() !== q.lv) cfg.setLevel(q.lv);
    if (q.setup) q.setup();
    setHidden(true);
    render();
    try { box.scrollIntoView({block:'nearest', behavior:'smooth'}); } catch (e) {}
  };
  LQ.list = function(){ cur = null; box.style.display = ''; setHidden(false); render(); };
  LQ.close = function(){ cur = null; box.style.display = 'none'; setHidden(false); };
  LQ.active = function(){ return !!cur && !solved; };
  LQ.current = function(){ return cur; };

  LQ.init = function(c){
    cfg = c; loadRec();
    box = document.createElement('div'); box.className = 'lq'; box.style.display = 'none';
    c.mount.parentNode.insertBefore(box, c.mount);
    if (c.button){
      var b = document.createElement('button'); b.className = 'lqOpen'; b.type = 'button';
      b.textContent = '🎮 문제 풀기';
      b.onclick = function(){ if (box.style.display === 'none') LQ.list(); else LQ.close(); };
      c.button.appendChild(b);
    }
    var m = /[?&]quest=([^&#]+)/.exec(location.search);
    if (m){
      var id = decodeURIComponent(m[1]);
      if (id === 'list') LQ.list(); else LQ.open(id);
    }
  };
})();
