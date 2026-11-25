/* labA11y.js — 실험실 셋이 함께 쓰는 '보기·듣기 도움' (261125)
   18차 외부 평가(보조공학)에서 아직 없다고 적어 둔 넷을 넣는다.
     · 글자 크게            · 고대비
     · 소리로 알려 주기      · 키 바꾸기
   실험실 쪽에서는 FxA11y.setup({...}) 한 번만 부르면 된다.          */
(function (global) {
  'use strict';

  var KEY = 'fxA11y.v1';
  var state = {font: 1, hi: false, sound: false, keys: {}};
  var cfg = {lab: '', actions: [], sonify: null};
  var ctx = null, lastTone = -1;   /* 0 으로 두면 갓 만든 소리틀에서 첫 소리가 막힌다 */

  /* ---------- 남겨 두기 ---------- */
  function load() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return;
      var o = JSON.parse(raw);
      if (o && typeof o === 'object') {
        state.font  = +o.font || 1;
        state.hi    = !!o.hi;
        state.sound = !!o.sound;
        state.keys  = (o.keys && typeof o.keys === 'object') ? o.keys : {};
      }
    } catch (e) { /* 사생활 보호 창에서는 그냥 기본값으로 */ }
  }
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {}
  }

  /* ---------- 글자 크기·고대비 ---------- */
  function applyView() {
    var r = document.documentElement;
    r.setAttribute('data-a11y-font', state.font === 1 ? 'n' : (state.font === 1.25 ? 'b' : 'xb'));
    r.setAttribute('data-a11y-hi', state.hi ? '1' : '0');
    document.body.style.zoom = state.font === 1 ? '' : String(state.font);
    /* 글자를 키우면 상자 너비가 달라진다 — 캔버스를 다시 맞춰야 한다 */
    setTimeout(function () { try { window.dispatchEvent(new Event('resize')); } catch (e) {} }, 30);
  }

  var CSS = [
    '.fxa11y-bar{display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin:8px 0 0;font-size:13px;}',
    '.fxa11y-bar>button{font-size:12.5px;font-family:inherit;background:#fff;border:1px solid #c8d8d5;',
    '  border-radius:999px;padding:4px 11px;cursor:pointer;color:#173238;}',
    '.fxa11y-bar>button[aria-pressed="true"]{background:#246d78;border-color:#246d78;color:#fff;}',
    '.fxa11y-bar>button:focus-visible,.fxa11y-panel button:focus-visible,.fxa11y-panel select:focus-visible',
    '  {outline:3px solid #2f8f9d;outline-offset:2px;}',
    '.fxa11y-panel{margin:7px 0 0;padding:10px 12px;border:1px solid #c8d8d5;border-radius:12px;',
    '  background:#f6faf9;font-size:13px;color:#2c4a50;max-width:620px;}',
    '.fxa11y-panel h4{margin:0 0 6px;font-size:13.5px;color:#173238;}',
    '.fxa11y-panel table{border-collapse:collapse;width:100%;}',
    '.fxa11y-panel td{padding:3px 4px;border-bottom:1px solid #dbe8e6;}',
    '.fxa11y-panel td:last-child{text-align:right;}',
    '.fxa11y-panel .kcur{font-family:"IBM Plex Mono",monospace;background:#eef4f3;border:1px solid #c8d8d5;',
    '  border-radius:5px;padding:1px 7px;}',
    '.fxa11y-panel button{font-size:12.5px;font-family:inherit;background:#fff;border:1px solid #c8d8d5;',
    '  border-radius:8px;padding:3px 9px;cursor:pointer;color:#173238;}',
    /* 고대비 — 글씨와 테두리를 또렷하게, 초점은 반드시 보이게 */
    'html[data-a11y-hi="1"] body{background:#fff;}',
    'html[data-a11y-hi="1"] *{color:#000 !important;}',
    'html[data-a11y-hi="1"] .fxa11y-bar>button[aria-pressed="true"]{background:#000;color:#fff !important;}',
    'html[data-a11y-hi="1"] button,html[data-a11y-hi="1"] select,html[data-a11y-hi="1"] input,',
    'html[data-a11y-hi="1"] .card,html[data-a11y-hi="1"] .readout,html[data-a11y-hi="1"] .hint,',
    'html[data-a11y-hi="1"] .kbwrap>summary,html[data-a11y-hi="1"] .fxa11y-panel',
    '  {border:2px solid #000 !important;background:#fff !important;}',
    'html[data-a11y-hi="1"] .tool.on,html[data-a11y-hi="1"] .act.on,html[data-a11y-hi="1"] .lv.on',
    '  {background:#000 !important;color:#fff !important;}',
    'html[data-a11y-hi="1"] .tool.on *,html[data-a11y-hi="1"] .act.on *,html[data-a11y-hi="1"] .lv.on *',
    '  {color:#fff !important;}',
    'html[data-a11y-hi="1"] a{text-decoration:underline !important;}',
    'html[data-a11y-hi="1"] :focus-visible{outline:4px solid #000 !important;outline-offset:2px !important;}',
    'html[data-a11y-hi="1"] canvas:focus{outline:4px solid #000 !important;outline-offset:2px !important;}',
    /* 그림 안쪽까지 다시 칠하지는 못한다 — 또렷하게만 만든다.
       밝은 판과 어두운 판이 섞여 있어, 실험실이 어느 쪽인지 알려 준다 */
    'html[data-a11y-hi="1"] canvas[data-a11y-canvas="light"]{filter:contrast(1.45) saturate(1.25);}',
    'html[data-a11y-hi="1"] canvas[data-a11y-canvas="dark"]{filter:brightness(1.18) contrast(1.3);}',
    /* 키보드로 들어온 캔버스는 어느 판에서나 테가 보여야 한다 */
    'canvas:focus-visible{outline:3px solid #2f8f9d;outline-offset:2px;}'
  ].join('\n');

  /* ---------- 소리 ---------- */
  function audio() {
    if (ctx) return ctx;
    var AC = global.AudioContext || global.webkitAudioContext;
    if (!AC) return null;
    try { ctx = new AC(); } catch (e) { ctx = null; }
    return ctx;
  }
  /* 값 하나를 높낮이로 — 낮으면 낮은 소리, 높으면 높은 소리 (220~1200Hz) */
  function tone(v, lo, hi, ms) {
    if (!state.sound) return;
    var ac = audio();
    if (!ac) return;
    if (ac.state === 'suspended') { try { ac.resume(); } catch (e) {} }
    var now = ac.currentTime;
    if (now - lastTone < 0.05) return;      /* 너무 자주 울리지 않게 */
    lastTone = now;
    var t = (hi === lo) ? 0 : (v - lo) / (hi - lo);
    t = Math.max(0, Math.min(1, isFinite(t) ? t : 0));
    var f = 220 * Math.pow(1200 / 220, t);
    var o = ac.createOscillator(), g = ac.createGain();
    o.type = 'sine'; o.frequency.value = f;
    g.gain.setValueAtTime(0.0001, now);
    g.gain.exponentialRampToValueAtTime(0.09, now + 0.012);
    g.gain.exponentialRampToValueAtTime(0.0001, now + (ms || 180) / 1000);
    o.connect(g); g.connect(ac.destination);
    o.start(now); o.stop(now + (ms || 180) / 1000 + 0.02);
  }
  /* 아무 값도 없을 때의 '없음' 소리 — 짧고 낮은 두 번 */
  function none() {
    if (!state.sound) return;
    tone(0, 0, 1, 90);
    setTimeout(function () { lastTone = -1; tone(0, 0, 1, 90); }, 120);
  }

  /* ---------- 키 바꾸기 ---------- */
  /* 실험실은 ev.key 를 그대로 보지 않고 이 함수를 거친다.
     학생이 바꾼 키를 '본디 키' 로 되돌려 준다. */
  function map(k) {
    if (!k) return k;
    var m = state.keys;
    for (var user in m) if (m[user] === k) return null;   /* 본디 키는 넘겨준 자리를 잃는다 */
    return m[k] || k;
  }
  function keyLabel(k) {
    if (k === ' ') return 'Space';
    if (k === 'ArrowLeft') return '←'; if (k === 'ArrowRight') return '→';
    if (k === 'ArrowUp') return '↑';   if (k === 'ArrowDown') return '↓';
    return k;
  }
  function curKeyFor(def) {
    for (var user in state.keys) if (state.keys[user] === def) return user;
    return def;
  }

  /* ---------- 화면 ---------- */
  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    return e;
  }
  function buildPanel(host) {
    var panel = el('div', 'fxa11y-panel');
    panel.id = 'fxa11yPanel';
    panel.hidden = true;
    function row(label, html) {
      return '<tr><td>' + label + '</td><td>' + html + '</td></tr>';
    }
    var keyRows = cfg.actions.map(function (a, i) {
      return row(a.name, '<span class="kcur" id="fxk' + i + '">' + keyLabel(curKeyFor(a.key)) +
                 '</span> <button type="button" data-k="' + i + '">바꾸기</button>');
    }).join('');
    panel.innerHTML =
      '<h4>보기·듣기 도움</h4>' +
      '<table><tbody>' +
      row('글자 크기',
          '<button type="button" data-f="1">보통</button> ' +
          '<button type="button" data-f="1.25">크게</button> ' +
          '<button type="button" data-f="1.5">아주 크게</button>') +
      row('고대비 (검정·흰색만)', '<button type="button" id="fxHi">끔</button>') +
      row('소리로 알려 주기', '<button type="button" id="fxSnd">끔</button>') +
      '</tbody></table>' +
      (cfg.actions.length
        ? '<h4 style="margin-top:9px">키 바꾸기</h4>' +
          '<p style="margin:0 0 5px">바꾸기를 누른 뒤 쓰고 싶은 키를 한 번 누르세요.</p>' +
          '<table><tbody>' + keyRows + '</tbody></table>' +
          '<p style="margin:6px 0 0"><button type="button" id="fxKeyReset">키를 처음으로</button></p>'
        : '') +
      '<p style="margin:8px 0 0;color:#5b7b80">이 설정은 이 기기의 이 브라우저에만 남습니다.</p>';
    host.appendChild(panel);
    return panel;
  }

  function refresh(panel) {
    panel.querySelectorAll('[data-f]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(+b.getAttribute('data-f') === state.font));
      b.style.fontWeight = (+b.getAttribute('data-f') === state.font) ? '700' : '';
    });
    var hi = panel.querySelector('#fxHi'), sn = panel.querySelector('#fxSnd');
    hi.textContent = state.hi ? '켬' : '끔';
    hi.setAttribute('aria-pressed', String(state.hi));
    sn.textContent = state.sound ? '켬' : '끔';
    sn.setAttribute('aria-pressed', String(state.sound));
    cfg.actions.forEach(function (a, i) {
      var s = panel.querySelector('#fxk' + i);
      if (s) s.textContent = keyLabel(curKeyFor(a.key));
    });
  }

  function setup(opts) {
    cfg.lab = opts.lab || '';
    cfg.actions = opts.actions || [];
    cfg.sonify = opts.sonify || null;
    if (opts.canvas){
      var cvs = document.querySelector(opts.canvas);
      if (cvs) cvs.setAttribute('data-a11y-canvas', opts.canvasTone || 'light');
    }
    var host = typeof opts.into === 'string' ? document.querySelector(opts.into) : opts.into;
    if (!host) return;

    load();

    var st = document.createElement('style');
    st.textContent = CSS;
    document.head.appendChild(st);

    var bar = el('div', 'fxa11y-bar');
    var btn = el('button', null, '보기·듣기 도움');
    btn.type = 'button';
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-controls', 'fxa11yPanel');
    bar.appendChild(btn);
    host.appendChild(bar);

    var panel = buildPanel(host);

    btn.onclick = function () {
      panel.hidden = !panel.hidden;
      btn.setAttribute('aria-expanded', String(!panel.hidden));
      if (!panel.hidden) refresh(panel);
    };

    panel.addEventListener('click', function (ev) {
      var t = ev.target;
      if (!t || t.tagName !== 'BUTTON') return;
      if (t.hasAttribute('data-f')) {
        state.font = +t.getAttribute('data-f');
        save(); applyView(); refresh(panel);
        say('글자 크기를 ' + t.textContent + ' 로 바꿨어요.');
      } else if (t.id === 'fxHi') {
        state.hi = !state.hi; save(); applyView(); refresh(panel);
        say('고대비를 ' + (state.hi ? '켰어요' : '껐어요') + '.');
      } else if (t.id === 'fxSnd') {
        state.sound = !state.sound; save(); refresh(panel);
        if (state.sound) { audio(); tone(0.7, 0, 1, 200); }
        say('소리로 알려 주기를 ' + (state.sound ? '켰어요' : '껐어요') + '.');
      } else if (t.id === 'fxKeyReset') {
        state.keys = {}; save(); refresh(panel);
        say('키를 처음으로 되돌렸어요.');
      } else if (t.hasAttribute('data-k')) {
        grab(+t.getAttribute('data-k'), t, panel);
      }
    });

    applyView();
  }

  /* 키 하나를 받아 적는다 */
  function grab(i, btn, panel) {
    var a = cfg.actions[i];
    if (!a) return;
    var old = btn.textContent;
    btn.textContent = '키를 누르세요…';
    say(a.name + ' 에 쓸 키를 누르세요. 그만두려면 Esc.');
    function off() {
      window.removeEventListener('keydown', on, true);
      btn.textContent = old;
      refresh(panel);
    }
    function on(ev) {
      ev.preventDefault(); ev.stopPropagation();
      if (ev.key === 'Escape') { say('그만뒀어요.'); off(); return; }
      if (ev.key === 'Tab') return;                 /* 탭은 늘 빠져나가는 키로 남긴다 */
      for (var u in state.keys) if (state.keys[u] === a.key) delete state.keys[u];
      if (ev.key !== a.key) state.keys[ev.key] = a.key;
      save();
      say(eul(a.name) + ' ' + keyLabel(ev.key) + ' 키로 바꿨어요.');
      off();
    }
    window.addEventListener('keydown', on, true);
  }

  /* 받침을 가려 '을/를' 을 바르게 — '을(를)' 은 읽어 주는 장치에서 흉하다 */
  function eul(w) {
    for (var i = w.length - 1; i >= 0; i--) {
      var c = w.charCodeAt(i);
      if (c >= 0xAC00 && c <= 0xD7A3) return w + (((c - 0xAC00) % 28) ? '을' : '를');
    }
    return w + '를';
  }

  function say(msg) {
    var b = document.getElementById('say');
    if (!b) return;
    b.textContent = (b.textContent === msg) ? msg + ' ' : msg;
  }

  global.FxA11y = {
    setup: setup,
    map: map,
    tone: tone,
    none: none,
    get sound() { return state.sound; },
    get hiContrast() { return state.hi; }
  };
})(window);
