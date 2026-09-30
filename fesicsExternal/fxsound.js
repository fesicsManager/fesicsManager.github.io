/* fesics 실험 공통 효과음 (fxSound)
 * - 소리 파일 없이 Web Audio로 짧은 효과음을 합성한다.
 * - 버튼·슬라이더·탭·선택 조작, 기록표에 줄이 추가될 때(✅/❌ 포함 여부 반영) 소리를 낸다.
 * - 오른쪽 위 🔊 버튼으로 켜고 끈다(브라우저에 기억, 기본값 켜짐).
 * - 실험 HTML에서는 <script src="../fxsound.js" defer></script> 한 줄로 불러온다.
 */
(function () {
  if (window.__fxSound) return;
  window.__fxSound = true;

  var KEY = 'fxSoundOn';
  var on = true;
  try { on = localStorage.getItem(KEY) !== '0'; } catch (e) {}
  var VOL = 0.07;
  var ctx = null, last = 0, lastSlide = 0;

  function ac() {
    if (!ctx) {
      var C = window.AudioContext || window.webkitAudioContext;
      if (!C) return null;
      ctx = new C();
    }
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }

  // 음 하나: 주파수, 시작 지연(초), 길이(초), 파형, 음량 배율, 끝 주파수(글리산도)
  function tone(f, t0, dur, type, g, f2) {
    var a = ac(); if (!a) return;
    var t = a.currentTime + (t0 || 0);
    var o = a.createOscillator(), v = a.createGain();
    o.type = type || 'sine';
    o.frequency.setValueAtTime(f, t);
    if (f2) o.frequency.exponentialRampToValueAtTime(f2, t + dur);
    var peak = VOL * (g == null ? 1 : g);
    v.gain.setValueAtTime(0.0001, t);
    v.gain.exponentialRampToValueAtTime(peak, t + 0.008);
    v.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(v); v.connect(a.destination);
    o.start(t); o.stop(t + dur + 0.02);
  }

  function whoosh() {
    var a = ac(); if (!a) return;
    var n = Math.floor(a.sampleRate * 0.12), b = a.createBuffer(1, n, a.sampleRate), d = b.getChannelData(0);
    for (var i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / n);
    var s = a.createBufferSource(), f = a.createBiquadFilter(), v = a.createGain(), t = a.currentTime;
    s.buffer = b; f.type = 'bandpass'; f.Q.value = 1.2;
    f.frequency.setValueAtTime(700, t); f.frequency.exponentialRampToValueAtTime(2400, t + 0.12);
    v.gain.setValueAtTime(VOL * 0.9, t); v.gain.exponentialRampToValueAtTime(0.0001, t + 0.12);
    s.connect(f); f.connect(v); v.connect(a.destination); s.start(t);
  }

  var SFX = {
    tick:   function () { tone(1400, 0, 0.035, 'sine', 0.55); },
    press:  function () { tone(520, 0, 0.07, 'triangle', 0.9); tone(780, 0.05, 0.09, 'triangle', 0.8); },
    reset:  function () { tone(660, 0, 0.08, 'sine', 0.7, 330); },
    tab:    function () { whoosh(); },
    record: function () { tone(880, 0, 0.08, 'sine', 0.8); tone(1175, 0.06, 0.12, 'sine', 0.7); },
    good:   function () { tone(784, 0, 0.09, 'sine', 0.8); tone(988, 0.07, 0.09, 'sine', 0.8); tone(1319, 0.14, 0.16, 'sine', 0.75); },
    bad:    function () { tone(330, 0, 0.12, 'triangle', 0.7); tone(262, 0.1, 0.16, 'triangle', 0.6); },
    slide:  function (r) { tone(300 + 900 * r, 0, 0.03, 'sine', 0.35); }
  };

  function play(name, arg, force) {
    if (!on) return;
    var now = Date.now();
    if (!force && now - last < 70) return; // 겹침 방지
    last = now;
    try { SFX[name](arg); } catch (e) {}
  }
  window.fxSound = { play: function (n, a) { play(n, a, true); } };

  function label(el) { return ((el.id || '') + ' ' + (el.className || '') + ' ' + (el.textContent || '')).toLowerCase(); }

  // 클릭: 탭 / 초기화 / 주요 실행 / 그 밖의 버튼
  document.addEventListener('click', function (e) {
    var el = e.target.closest && e.target.closest('button, [role=tab], .tab, .tab-btn, a.btn, input[type=button], input[type=submit]');
    if (!el || el.id === 'fxSoundBtn' || el.disabled) return;
    var s = label(el);
    if (el.matches('[role=tab], .tab, .tab-btn') || /^tab[a-z0-9]/i.test(el.id || '')) return play('tab');
    if (/clr|clear|reset|초기화|지우|비우/.test(s)) return play('reset');
    if (/go|run|rec|act|start|측정|기록|실험|시작|발사|재생|계산|확인|굴리|던지|넣기|만들/.test(s)) return play('press');
    play('tick');
  }, true);

  // 슬라이더: 위치에 따라 음높이가 달라지는 짧은 틱(너무 잦지 않게)
  document.addEventListener('input', function (e) {
    var el = e.target;
    if (!el || el.type !== 'range') return;
    var now = Date.now();
    if (now - lastSlide < 60) return;
    lastSlide = now;
    var min = +el.min || 0, max = el.max === '' ? 100 : +el.max, r = max > min ? (+el.value - min) / (max - min) : 0.5;
    if (on) try { SFX.slide(Math.max(0, Math.min(1, r))); } catch (err) {}
  }, true);

  document.addEventListener('change', function (e) {
    var el = e.target;
    if (el && (el.type === 'radio' || el.type === 'checkbox' || el.tagName === 'SELECT')) play('tick');
  }, true);

  // 기록표에 줄이 추가되면: ✅ 포함 → 성공음, ❌ 포함 → 낮은 음, 그 외 → 기록음
  function watch() {
    var ready = false;
    setTimeout(function () { ready = true; }, 800); // 첫 화면 그릴 때는 조용히
    new MutationObserver(function (list) {
      if (!ready || !on) return;
      var added = 0, good = 0, bad = 0;
      for (var i = 0; i < list.length; i++) {
        var m = list[i];
        if (!m.target.closest || !m.target.closest('tbody, table')) continue;
        for (var j = 0; j < m.addedNodes.length; j++) {
          var n = m.addedNodes[j];
          if (n.nodeType !== 1 || n.tagName !== 'TR') continue;
          added++;
          var t = n.textContent || '';
          if (/✅|⭕/.test(t)) good++;
          if (/❌|✗/.test(t)) bad++;
        }
      }
      if (!added) return;
      // 표를 통째로 다시 그리는 경우(여러 줄)에는 기록음 한 번만
      if (added === 1 && bad && !good) play('bad');
      else if (added === 1 && good && !bad) play('good');
      else play('record');
    }).observe(document.body, { childList: true, subtree: true });
  }

  function button() {
    var b = document.createElement('button');
    b.type = 'button'; b.id = 'fxSoundBtn';
    b.setAttribute('aria-label', '효과음 켜기/끄기');
    b.style.cssText = 'position:fixed;right:8px;top:8px;z-index:2147483000;width:30px;height:30px;border-radius:50%;' +
      'border:1px solid rgba(0,0,0,.15);background:rgba(255,255,255,.85);font-size:14px;line-height:1;cursor:pointer;' +
      'box-shadow:0 1px 4px rgba(0,0,0,.15);padding:0;opacity:.75';
    function paint() { b.textContent = on ? '🔊' : '🔇'; b.title = on ? '효과음 끄기' : '효과음 켜기'; }
    paint();
    b.addEventListener('click', function () {
      on = !on;
      try { localStorage.setItem(KEY, on ? '1' : '0'); } catch (e) {}
      paint();
      if (on) play('press', null, true);
    });
    b.addEventListener('mouseenter', function () { b.style.opacity = '1'; });
    b.addEventListener('mouseleave', function () { b.style.opacity = '.75'; });
    document.body.appendChild(b);
  }

  function init() { button(); watch(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
