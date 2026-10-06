/* fesics 실험 공통 학습 도구 (labKit)
 * 1) 예측 → 관찰 → 설명: 실험 전에 예측을 한 줄 적고, 기록이 모이면 예측과 비교해 되돌아본다.
 * 2) 기록표 그래프·CSV: 기록이 쌓이는 표 아래에 [📊 그래프·CSV] — 두 열을 골라 점 그래프와 추세선, CSV 저장.
 * 3) 활동 요약: 예측·되돌아보기·기록 수·조작 수·활동 시간을 홈페이지(부모 창)에 postMessage 로 알린다.
 *    홈페이지가 로그인한 학생의 학습 기록(learning_events, kind lab_activity)으로 저장한다. 실험만 따로 열면 보내지 않는다.
 * 실험 HTML 에서는 <script src="../labkit.js" defer></script> 한 줄로 불러온다. 실험별 코드는 건드리지 않는다.
 */
(function () {
  'use strict';
  if (window.__labKit) return;
  window.__labKit = true;

  var LAB = decodeURIComponent(location.pathname).replace(/^.*fesicsExternal\//, '').replace(/^\//, '').replace(/\.html?$/, '');
  var KEY = 'labKit:' + LAB;
  var NEED = 3; // 되돌아보기를 여는 기록 수
  var NEED_ACTS = 8; // 기록표가 없는 실험은 조작 수로 대신한다
  var MAX_TEXT = 200;

  function load() { try { return JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { return {}; } }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) {} }
  var st = load(); // { predict, reflect:{match,why}, skip } — 브라우저에 남겨 다시 열어도 이어진다

  var session = (Date.now().toString(36) + Math.random().toString(36).slice(2, 10)).slice(0, 20);
  var act = { records: 0, interactions: 0, graph: false, csv: false, activeMs: 0, lastInput: 0, predict: null, reflect: null };

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function isOurs(node) { return !!(node && node.closest && node.closest('.lk-ui')); }

  // ---------- 스타일 ----------
  function style() {
    var s = document.createElement('style');
    s.id = 'labKitStyle';
    s.textContent = [
      '.lk-ui{font-family:inherit;color:#1f2937;line-height:1.5;box-sizing:border-box}',
      '.lk-ui *{box-sizing:border-box}',
      '.lk-poe{margin:0 0 14px;padding:12px 14px;border:1px solid #f3d27a;background:#fffbea;border-radius:12px;font-size:15px}',
      '.lk-poe.lk-done{border-color:#a7dcb5;background:#f0fbf3}',
      '.lk-poe.lk-mini{padding:6px 10px;background:#fffdf3;font-size:14px}',
      '.lk-poe b.lk-t{display:block;font-size:16px;margin-bottom:4px}',
      '.lk-poe p{margin:2px 0 8px;color:#4b5563;font-size:14px}',
      '.lk-row{display:flex;flex-wrap:wrap;gap:6px;align-items:center}',
      '.lk-in{flex:1 1 220px;min-width:0;padding:8px 10px;border:1px solid #d1d5db;border-radius:8px;font:inherit;font-size:15px;background:#fff;color:#111}',
      '.lk-btn{padding:7px 12px;border:1px solid #d1d5db;border-radius:8px;background:#fff;color:#1f2937;font:inherit;font-size:14px;cursor:pointer;white-space:nowrap}',
      '.lk-btn:hover{background:#f3f4f6}',
      '.lk-btn.lk-main{background:#2563eb;border-color:#2563eb;color:#fff}',
      '.lk-btn.lk-main:hover{background:#1d4ed8}',
      '.lk-btn.lk-on{background:#1f2937;border-color:#1f2937;color:#fff}',
      '.lk-link{border:0;background:none;color:#2563eb;cursor:pointer;font:inherit;font-size:13px;padding:0 4px;text-decoration:underline}',
      '.lk-q{font-style:normal;background:#fff;border-radius:6px;padding:1px 6px;border:1px solid #eee}',
      '.lk-prog{font-size:13px;color:#6b7280}',
      '.lk-tools{margin:8px 0 4px;display:flex;gap:6px;flex-wrap:wrap}',
      '.lk-panel{margin:6px 0 12px;padding:10px;border:1px solid #dbe3ef;border-radius:12px;background:#f8fafc;font-size:14px}',
      '.lk-panel select{font:inherit;font-size:14px;padding:4px 6px;border:1px solid #cbd5e1;border-radius:6px;max-width:100%;background:#fff;color:#111}',
      '.lk-panel label{display:inline-flex;align-items:center;gap:4px;margin-right:8px}',
      '.lk-cv{display:block;width:100%;height:auto;margin:8px 0 4px;background:#fff;border:1px solid #e5e7eb;border-radius:8px}',
      '.lk-fit{font-size:13px;color:#374151}',
      '.lk-note{font-size:12px;color:#6b7280}'
    ].join('\n');
    document.head.appendChild(s);
  }

  // ---------- 활동 요약 보내기 ----------
  var parentOrigin = '';
  try {
    var o = document.referrer ? new URL(document.referrer).origin : '';
    if (/^https:\/\/([a-z0-9-]+\.)*(fesics\.kr|simplesoft\.me)$/.test(o) || /^http:\/\/localhost(:\d+)?$/.test(o)) parentOrigin = o;
  } catch (e) {}
  var sendTimer = 0;
  function snapshot() {
    return {
      session: session,
      lab: LAB.slice(0, 160),
      records: act.records,
      interactions: act.interactions,
      elapsed_ms: Math.round(act.activeMs),
      graph: act.graph,
      csv: act.csv,
      predict: act.predict ? { text: act.predict } : null,
      reflect: act.reflect
    };
  }
  function send(now) {
    if (window.parent === window || !parentOrigin) return;
    clearTimeout(sendTimer);
    var go = function () {
      if (!act.interactions && !act.records && !act.predict) return; // 열기만 한 것은 보내지 않는다
      try { window.parent.postMessage({ src: 'fesics-lab', type: 'activity', activity: snapshot() }, parentOrigin); } catch (e) {}
    };
    if (now) go(); else sendTimer = setTimeout(go, 1500);
  }

  // 활동 시간: 화면이 보이고 마지막 조작 뒤 90초 안이면 5초씩 더한다
  setInterval(function () {
    if (document.visibilityState === 'visible' && act.lastInput && Date.now() - act.lastInput < 90000) act.activeMs += 5000;
  }, 5000);
  document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'hidden') send(true); });
  window.addEventListener('pagehide', function () { send(true); });

  function touched() {
    act.lastInput = Date.now();
    act.interactions++;
    if (act.interactions % 10 === 0) send();
    refreshPoe();
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('button, [role=tab], input[type=button], input[type=submit], input[type=radio], input[type=checkbox], canvas');
    if (b && !isOurs(b) && b.id !== 'fxSoundBtn') touched();
  }, true);
  var lastRange = 0;
  document.addEventListener('input', function (e) {
    if (isOurs(e.target) || e.target.type !== 'range') return;
    var now = Date.now();
    if (now - lastRange > 800) touched(); // 슬라이더 한 번 끌기 = 조작 1번
    lastRange = now;
  }, true);
  document.addEventListener('change', function (e) {
    if (!isOurs(e.target) && (e.target.tagName === 'SELECT' || e.target.type === 'number' || e.target.type === 'text')) touched();
  }, true);

  // ---------- 기록표 ----------
  var tables = []; // { table, tools, panel, rows }

  function headerCells(table) {
    var row = table.tHead && table.tHead.rows.length ? table.tHead.rows[table.tHead.rows.length - 1] : null;
    if (!row) {
      var first = table.rows[0];
      if (first && first.querySelector('th') && !first.querySelector('td')) row = first;
    }
    if (!row) return [];
    var out = [];
    for (var i = 0; i < row.cells.length; i++) {
      var span = row.cells[i].colSpan || 1;
      var t = (row.cells[i].innerText || row.cells[i].textContent || '').replace(/\s+/g, ' ').trim();
      for (var k = 0; k < span; k++) out.push(span > 1 ? t + ' ' + (k + 1) : t);
    }
    return out;
  }
  function dataRows(table) {
    var out = [];
    var bodies = table.tBodies;
    for (var b = 0; b < bodies.length; b++) {
      var rows = bodies[b].rows;
      for (var i = 0; i < rows.length; i++) {
        var r = rows[i];
        if (!r.querySelector('td')) continue;
        if (r.cells.length === 1 && (r.cells[0].colSpan || 1) > 1) continue; // "아직 기록이 없습니다" 줄
        if (r.querySelector('.empty-row, .empty')) continue;
        var cells = [];
        for (var j = 0; j < r.cells.length; j++) cells.push((r.cells[j].innerText || r.cells[j].textContent || '').replace(/\s+/g, ' ').trim());
        out.push(cells);
      }
    }
    return out;
  }
  function num(text) {
    var m = String(text).replace(/[−–]/g, '-').match(/-?\d{1,3}(?:,\d{3})+(?:\.\d+)?|-?\d*\.?\d+(?:[eE][-+]?\d+)?/);
    if (!m) return NaN;
    return parseFloat(m[0].replace(/,/g, ''));
  }
  function numericColumns(head, rows) {
    var n = Math.max(head.length, rows.reduce(function (a, r) { return Math.max(a, r.length); }, 0));
    var cols = [];
    for (var c = 0; c < n; c++) {
      var ok = 0;
      for (var i = 0; i < rows.length; i++) if (isFinite(num(rows[i][c]))) ok++;
      if (rows.length && ok / rows.length >= 0.8) cols.push(c);
    }
    return cols;
  }
  function isIndexCol(name) { return /^(#|no\.?|번호|순서|회|횟수|차례|시도)$/i.test(String(name).trim()); }

  function wrapOf(table) {
    var w = table.parentElement;
    if (w && /table|wrap|box|scroll/i.test(w.className || '') && w.children.length === 1) return w;
    return table;
  }

  function adopt(table) {
    for (var i = 0; i < tables.length; i++) if (tables[i].table === table) return tables[i];
    var t = { table: table, tools: null, panel: null, rows: 0, chosen: null };
    tables.push(t);
    var tools = el('div', 'lk-ui lk-tools');
    var gb = el('button', 'lk-btn', '📊 그래프·CSV');
    gb.type = 'button';
    gb.addEventListener('click', function () { togglePanel(t); });
    tools.appendChild(gb);
    tools.style.display = 'none';
    var w = wrapOf(table);
    w.parentNode.insertBefore(tools, w.nextSibling);
    t.tools = tools;
    return t;
  }

  function candidate(table) {
    if (!table || isOurs(table)) return false;
    if (table.closest('#fxPrinciple, .fx-principle')) return false;
    return !!table.tBodies.length;
  }

  var userTouchedAt = 0;
  document.addEventListener('pointerdown', function () { userTouchedAt = Date.now(); }, true);
  document.addEventListener('keydown', function () { userTouchedAt = Date.now(); }, true);

  function rescan() {
    var maxRows = 0;
    for (var i = 0; i < tables.length; i++) {
      var t = tables[i];
      if (!document.body.contains(t.table)) continue;
      var rows = dataRows(t.table);
      t.rows = rows.length;
      t.tools.style.display = rows.length >= 1 ? '' : 'none';
      if (t.counts && rows.length > maxRows) maxRows = rows.length;
      if (t.panel && t.panel.style.display !== 'none') drawPanel(t);
    }
    if (maxRows > act.records) { act.records = maxRows; send(); }
    refreshPoe();
  }
  var scanTimer = 0;
  function scheduleScan() { clearTimeout(scanTimer); scanTimer = setTimeout(rescan, 250); }

  function watchTables() {
    // 처음부터 id 붙은 tbody 가 있는 표(기록표 틀)는 바로 맡는다
    var all = document.querySelectorAll('table');
    for (var i = 0; i < all.length; i++) {
      if (candidate(all[i]) && all[i].querySelector('tbody[id]')) adopt(all[i]);
    }
    var ready = false;
    setTimeout(function () { ready = true; }, 800);
    new MutationObserver(function (list) {
      if (!ready) return;
      var hit = false;
      for (var k = 0; k < list.length; k++) {
        var m = list[k];
        if (isOurs(m.target)) continue;
        var tb = m.target.closest ? m.target.closest('table') : null;
        if (!tb) {
          // 표를 통째로 다시 그린 경우
          for (var j = 0; j < m.addedNodes.length; j++) {
            var n = m.addedNodes[j];
            if (n.nodeType === 1 && (n.tagName === 'TABLE' || n.querySelector)) {
              var found = n.tagName === 'TABLE' ? [n] : n.querySelectorAll('table');
              for (var q = 0; q < found.length; q++) if (candidate(found[q])) { adopt(found[q]); hit = true; }
            }
          }
          continue;
        }
        if (!candidate(tb)) continue;
        var t = adopt(tb);
        // 학생이 조작한 직후 늘어난 표만 '기록 수'로 센다(검증 탭 표 등 자동으로 그려지는 표는 빼려고)
        if (Date.now() - userTouchedAt < 3000) t.counts = true;
        hit = true;
      }
      if (hit) scheduleScan();
    }).observe(document.body, { childList: true, subtree: true });
    rescan();
  }

  // ---------- 그래프 패널 ----------
  function togglePanel(t) {
    if (!t.panel) {
      t.panel = el('div', 'lk-ui lk-panel');
      t.tools.parentNode.insertBefore(t.panel, t.tools.nextSibling);
      t.panel.style.display = 'none';
    }
    var open = t.panel.style.display === 'none';
    t.panel.style.display = open ? '' : 'none';
    if (open) {
      act.graph = true;
      send();
      drawPanel(t);
    }
  }

  function drawPanel(t) {
    var head = headerCells(t.table);
    var rows = dataRows(t.table);
    var cols = numericColumns(head, rows);
    var p = t.panel;
    p.innerHTML = '';
    var name = function (c) { return head[c] || (c + 1) + '번째 열'; };

    if (rows.length < 2 || cols.length < 2) {
      p.appendChild(el('div', 'lk-note', rows.length < 2
        ? '기록이 2개 이상 모이면 그래프를 그릴 수 있어요.'
        : '이 표에는 숫자로 된 열이 2개보다 적어 그래프 대신 CSV 로 받아 볼 수 있어요.'));
    } else {
      if (!t.chosen || cols.indexOf(t.chosen.x) < 0 || cols.indexOf(t.chosen.y) < 0) {
        var useful = cols.filter(function (c) { return !isIndexCol(name(c)); });
        if (useful.length < 2) useful = cols;
        t.chosen = { x: useful[0], y: useful[useful.length - 1], line: false };
      }
      var bar = el('div', 'lk-row');
      var pick = function (label, key) {
        var lb = el('label', null, label + ' ');
        var s = document.createElement('select');
        cols.forEach(function (c) {
          var op = el('option', null, name(c));
          op.value = c;
          if (c === t.chosen[key]) op.selected = true;
          s.appendChild(op);
        });
        s.addEventListener('change', function () { t.chosen[key] = +s.value; drawPanel(t); });
        lb.appendChild(s);
        return lb;
      };
      bar.appendChild(pick('가로축', 'x'));
      bar.appendChild(pick('세로축', 'y'));
      var lineLb = el('label');
      var cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.checked = !!t.chosen.line;
      cb.addEventListener('change', function () { t.chosen.line = cb.checked; drawPanel(t); });
      lineLb.appendChild(cb);
      lineLb.appendChild(document.createTextNode('점 잇기'));
      bar.appendChild(lineLb);
      p.appendChild(bar);

      var pts = [];
      rows.forEach(function (r) {
        var x = num(r[t.chosen.x]), y = num(r[t.chosen.y]);
        if (isFinite(x) && isFinite(y)) pts.push([x, y]);
      });
      var cv = el('canvas', 'lk-cv');
      p.appendChild(cv);
      var fit = el('div', 'lk-fit');
      p.appendChild(fit);
      plot(cv, pts, name(t.chosen.x), name(t.chosen.y), t.chosen.line, fit, isIndexCol(name(t.chosen.x)));
    }

    var tools = el('div', 'lk-row');
    tools.style.marginTop = '8px';
    var csv = el('button', 'lk-btn', '⬇ CSV 저장');
    csv.type = 'button';
    csv.addEventListener('click', function () { downloadCsv(head, rows); });
    tools.appendChild(csv);
    tools.appendChild(el('span', 'lk-note', '기록 ' + rows.length + '개 · 엑셀이나 구글 시트에서 열 수 있어요'));
    p.appendChild(tools);
  }

  function nice(v) {
    if (!isFinite(v)) return '';
    var a = Math.abs(v);
    if (a !== 0 && (a >= 1e5 || a < 1e-3)) return v.toExponential(2);
    return String(+v.toPrecision(4));
  }

  // 보기 좋은 눈금(1·2·5×10^k 간격). 0 에 가까우면 0 부터 시작한다.
  function ticks(lo, hi) {
    if (lo > 0 && lo < (hi - lo) * 0.5) lo = 0;
    if (hi < 0 && -hi < (hi - lo) * 0.5) hi = 0;
    if (hi === lo) { lo -= Math.abs(lo) * 0.1 || 1; hi += Math.abs(hi) * 0.1 || 1; }
    var raw = (hi - lo) / 5, mag = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10)), f = raw / mag;
    var step = (f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10) * mag;
    var out = [], a = Math.floor(lo / step + 1e-9) * step;
    for (var v = a; v < hi + step * 0.999; v += step) out.push(+v.toPrecision(12));
    if (out[out.length - 1] < hi) out.push(+(out[out.length - 1] + step).toPrecision(12));
    return out;
  }

  function plot(cv, pts, xName, yName, connect, fitBox, xIsIndex) {
    var W = Math.max(280, Math.min(640, (cv.parentNode.clientWidth || 600) - 4));
    var H = Math.round(W * 0.62);
    var dpr = window.devicePixelRatio || 1;
    cv.width = W * dpr;
    cv.height = H * dpr;
    cv.style.maxWidth = W + 'px';
    var g = cv.getContext('2d');
    g.scale(dpr, dpr);
    g.fillStyle = '#fff';
    g.fillRect(0, 0, W, H);
    if (!pts.length) return;

    var L = 58, R = 14, T = 14, B = 44;
    var xs = pts.map(function (p) { return p[0]; }), ys = pts.map(function (p) { return p[1]; });
    var xt = ticks(Math.min.apply(null, xs), Math.max.apply(null, xs));
    var yt = ticks(Math.min.apply(null, ys), Math.max.apply(null, ys));
    var x0 = xt[0], x1 = xt[xt.length - 1], y0 = yt[0], y1 = yt[yt.length - 1];
    var sx = function (x) { return L + (x - x0) / (x1 - x0) * (W - L - R); };
    var sy = function (y) { return H - B - (y - y0) / (y1 - y0) * (H - T - B); };

    g.font = '11px sans-serif';
    g.strokeStyle = '#e5e7eb';
    g.fillStyle = '#6b7280';
    g.lineWidth = 1;
    xt.forEach(function (v) {
      g.beginPath(); g.moveTo(sx(v), T); g.lineTo(sx(v), H - B); g.stroke();
      g.textAlign = 'center'; g.fillText(nice(v), sx(v), H - B + 14);
    });
    yt.forEach(function (v) {
      g.beginPath(); g.moveTo(L, sy(v)); g.lineTo(W - R, sy(v)); g.stroke();
      g.textAlign = 'right'; g.fillText(nice(v), L - 4, sy(v) + 4);
    });
    g.strokeStyle = '#9ca3af';
    g.strokeRect(L, T, W - L - R, H - T - B);
    g.fillStyle = '#374151';
    g.font = '12px sans-serif';
    g.textAlign = 'center';
    g.fillText(xName, L + (W - L - R) / 2, H - 8);
    g.save();
    g.translate(13, T + (H - T - B) / 2);
    g.rotate(-Math.PI / 2);
    g.fillText(yName, 0, 0);
    g.restore();

    if (connect) {
      var sorted = pts.slice().sort(function (a, b) { return a[0] - b[0]; });
      g.strokeStyle = '#93c5fd';
      g.lineWidth = 2;
      g.beginPath();
      sorted.forEach(function (p, k) { if (k) g.lineTo(sx(p[0]), sy(p[1])); else g.moveTo(sx(p[0]), sy(p[1])); });
      g.stroke();
    }

    // 최소제곱 직선
    var n = pts.length, mx = 0, my = 0;
    pts.forEach(function (p) { mx += p[0]; my += p[1]; });
    mx /= n; my /= n;
    var sxx = 0, sxy = 0, syy = 0;
    pts.forEach(function (p) { sxx += (p[0] - mx) * (p[0] - mx); sxy += (p[0] - mx) * (p[1] - my); syy += (p[1] - my) * (p[1] - my); });
    if (xIsIndex) {
      fitBox.textContent = '가로축이 기록 순서예요. 바꾼 값(조건)을 가로축으로 고르면 관계를 볼 수 있어요.';
    } else if (n >= 2 && sxx > 0) {
      var a = sxy / sxx, b = my - a * mx;
      var r2 = syy > 0 ? (sxy * sxy) / (sxx * syy) : 1;
      g.strokeStyle = '#f97316';
      g.lineWidth = 1.5;
      g.setLineDash([6, 4]);
      g.beginPath();
      g.moveTo(sx(x0), sy(a * x0 + b));
      g.lineTo(sx(x1), sy(a * x1 + b));
      g.stroke();
      g.setLineDash([]);
      fitBox.textContent = '추세선(주황 점선): y = ' + nice(a) + 'x ' + (b < 0 ? '− ' + nice(-b) : '+ ' + nice(b)) +
        ' · 결정계수 R² = ' + r2.toFixed(2) + (r2 < 0.8 ? ' — 점들이 직선에서 많이 벗어나 있어요. 곡선 관계이거나 다른 요인이 있을 수 있어요.' : '');
    } else {
      fitBox.textContent = '가로축 값이 모두 같아 추세선을 그릴 수 없어요. 가로축 값을 바꿔 가며 기록해 보세요.';
    }

    g.fillStyle = '#2563eb';
    pts.forEach(function (p) { g.beginPath(); g.arc(sx(p[0]), sy(p[1]), 4, 0, Math.PI * 2); g.fill(); });
  }

  function downloadCsv(head, rows) {
    var q = function (v) { v = String(v == null ? '' : v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
    var lines = [];
    if (head.length) lines.push(head.map(q).join(','));
    rows.forEach(function (r) { lines.push(r.map(q).join(',')); });
    var blob = new Blob(['﻿' + lines.join('\r\n')], { type: 'text/csv;charset=utf-8' });
    var a = document.createElement('a');
    var title = (document.querySelector('h1') || {}).textContent || LAB.split('/').pop();
    a.download = title.replace(/[\\/:*?"<>|]+/g, '').trim().slice(0, 60) + '_기록.csv';
    a.href = URL.createObjectURL(blob);
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
    act.csv = true;
    send();
  }

  // ---------- 예측 → 관찰 → 설명 ----------
  var poe = null;
  var poeMode = '';
  var reflectPick = null;

  function hasRecordTable() { return tables.some(function (t) { return t.counts || t.table.querySelector('tbody[id]'); }); }
  function observed() {
    if (hasRecordTable()) return act.records >= NEED;
    return act.interactions >= NEED_ACTS;
  }

  function poeHost() {
    var sel = ['#tab-explore', '#panel-explore', '#panelA', '[data-panel="explore"]', '.tab-panel', 'section.panel', '.panel'];
    for (var i = 0; i < sel.length; i++) {
      var e = document.querySelector(sel[i]);
      if (e && !e.closest('#fxPrinciple')) return { parent: e, before: e.firstChild };
    }
    var h1 = document.querySelector('h1');
    if (h1) {
      var head = h1.closest('header') || h1;
      var tabs = head.parentNode.querySelector('.tabs, [role=tablist]');
      var after = tabs && tabs.parentNode === head.parentNode ? tabs : head;
      return { parent: after.parentNode, before: after.nextSibling };
    }
    return { parent: document.body, before: document.body.firstChild };
  }

  function mountPoe() {
    poe = el('div', 'lk-ui lk-poe');
    poe.setAttribute('role', 'region');
    poe.setAttribute('aria-label', '예측하고 실험하기');
    var h = poeHost();
    h.parent.insertBefore(poe, h.before);
    refreshPoe(true);
  }

  function mode() {
    if (st.reflect && st.predict) return 'done';
    if (st.predict) return observed() ? 'reflect' : 'watch';
    return st.skip ? 'skipped' : 'ask';
  }

  function refreshPoe(force) {
    if (!poe) return;
    var m = mode();
    if (m === poeMode && !force) {
      if (m === 'watch') { var pg = poe.querySelector('.lk-prog'); if (pg) pg.textContent = progText(); }
      return;
    }
    // 입력 중인 칸이 있으면 화면을 다시 그리지 않는다
    if (!force && poe.contains(document.activeElement) && document.activeElement.tagName === 'INPUT') return;
    poeMode = m;
    poe.innerHTML = '';
    poe.className = 'lk-ui lk-poe' + (m === 'done' ? ' lk-done' : '') + (m === 'skipped' ? ' lk-mini' : '');
    ({ ask: drawAsk, watch: drawWatch, reflect: drawReflect, done: drawDone, skipped: drawSkipped })[m]();
  }

  function progText() {
    return hasRecordTable()
      ? '기록 ' + Math.min(act.records, NEED) + ' / ' + NEED + '개 — 기록이 모이면 예측과 비교해 봐요.'
      : '실험을 더 해 보면 예측과 비교해 볼 수 있어요.';
  }

  function textInput(placeholder, value) {
    var i = el('input', 'lk-in');
    i.type = 'text';
    i.maxLength = MAX_TEXT;
    i.placeholder = placeholder;
    if (value) i.value = value;
    return i;
  }
  function button(text, cls, fn) {
    var b = el('button', 'lk-btn' + (cls ? ' ' + cls : ''), text);
    b.type = 'button';
    b.addEventListener('click', fn);
    return b;
  }

  function drawAsk() {
    poe.appendChild(el('b', 'lk-t', '🤔 실험하기 전에 예측해 보세요'));
    poe.appendChild(el('p', null, '이 실험을 하면 어떤 결과가 나올까요? 생각을 한 줄로 적어 두면, 실험한 뒤 내 예측과 비교해 볼 수 있어요.'));
    var row = el('div', 'lk-row');
    var inp = textInput('예: ○○을 크게 하면 △△도 커질 것 같아요', st.predict);
    var ok = function () {
      var v = inp.value.trim();
      if (!v) { inp.focus(); return; }
      st.predict = v.slice(0, MAX_TEXT);
      st.reflect = null;
      st.skip = false;
      act.predict = st.predict;
      act.reflect = null;
      save();
      send(true);
      refreshPoe(true);
    };
    inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') ok(); });
    row.appendChild(inp);
    row.appendChild(button('예측 저장', 'lk-main', ok));
    row.appendChild(button('건너뛰기', '', function () { st.skip = true; save(); refreshPoe(true); }));
    poe.appendChild(row);
  }

  function quote(text) { return el('q', 'lk-q', text); }

  function drawWatch() {
    var row = el('div', 'lk-row');
    row.appendChild(el('span', null, '📝 내 예측:'));
    row.appendChild(quote(st.predict));
    row.appendChild(button('고치기', 'lk-link', function () { st.predict = null; save(); refreshPoe(true); }));
    poe.appendChild(row);
    poe.appendChild(el('div', 'lk-prog', progText()));
  }

  function drawReflect() {
    poe.appendChild(el('b', 'lk-t', '🔍 실험 결과가 내 예측과 맞았나요?'));
    var r0 = el('div', 'lk-row');
    r0.appendChild(el('span', null, '내 예측:'));
    r0.appendChild(quote(st.predict));
    poe.appendChild(r0);
    var picks = el('div', 'lk-row');
    picks.style.margin = '8px 0';
    var why = textInput('', '');
    var area = el('div', 'lk-row');
    area.style.display = reflectPick ? '' : 'none';
    [['yes', '맞았어요'], ['partly', '일부만 맞았어요'], ['no', '달랐어요']].forEach(function (c) {
      var b = button(c[1], reflectPick === c[0] ? 'lk-on' : '', function () {
        reflectPick = c[0];
        Array.prototype.forEach.call(picks.children, function (x) { x.classList.remove('lk-on'); });
        b.classList.add('lk-on');
        why.placeholder = c[0] === 'yes' ? '왜 그렇게 되는지 한 줄로 설명해 보세요' : '무엇이 달랐나요? 왜 그럴까요?';
        area.style.display = '';
        why.focus();
      });
      picks.appendChild(b);
    });
    poe.appendChild(picks);
    var done = function () {
      if (!reflectPick) return;
      st.reflect = { match: reflectPick, why: why.value.trim().slice(0, MAX_TEXT) || null };
      act.predict = st.predict;
      act.reflect = st.reflect;
      save();
      send(true);
      refreshPoe(true);
    };
    why.addEventListener('keydown', function (e) { if (e.key === 'Enter') done(); });
    area.appendChild(why);
    area.appendChild(button('저장', 'lk-main', done));
    poe.appendChild(area);
  }

  function drawDone() {
    var label = { yes: '맞았어요', partly: '일부만 맞았어요', no: '달랐어요' }[st.reflect.match] || '';
    var row = el('div', 'lk-row');
    row.appendChild(el('span', null, '✅ 예측 → 관찰 → 설명 완료 ·'));
    row.appendChild(quote(st.predict));
    row.appendChild(el('span', null, '→ ' + label));
    poe.appendChild(row);
    if (st.reflect.why) {
      var r2 = el('div', 'lk-row');
      r2.appendChild(el('span', null, '💡'));
      r2.appendChild(el('span', null, st.reflect.why));
      poe.appendChild(r2);
    }
    poe.appendChild(button('새로 예측하기', 'lk-link', function () {
      st.predict = null; st.reflect = null; reflectPick = null; save(); refreshPoe(true);
    }));
  }

  function drawSkipped() {
    poe.appendChild(button('🤔 예측하고 실험하기', 'lk-link', function () { st.skip = false; save(); refreshPoe(true); }));
  }

  function init() {
    style();
    mountPoe();
    watchTables();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  window.labKit = { state: function () { return { st: st, act: snapshot(), tables: tables.length }; } };
})();
