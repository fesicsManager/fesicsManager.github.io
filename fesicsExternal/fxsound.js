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

  /* ── 현상 소리: 실험 속 사건(북 치기, 지진 등)에 맞춰 실험 HTML이 직접 부른다 ── */
  var noiseBuf = null;
  function noise(a) {
    if (!noiseBuf) {
      var n = a.sampleRate * 2, d;
      noiseBuf = a.createBuffer(1, n, a.sampleRate); d = noiseBuf.getChannelData(0);
      for (var i = 0; i < n; i++) d[i] = Math.random() * 2 - 1;
    }
    var s = a.createBufferSource(); s.buffer = noiseBuf; s.loop = true;
    return s;
  }

  // 북: power 0~1 (세게 칠수록 크고 조금 더 오래 울림), t0 = 몇 초 뒤
  function drum(power, t0) {
    var a = ac(); if (!a) return;
    var p = Math.max(0, Math.min(1, +power || 0)), t = a.currentTime + (t0 || 0);
    var g = 0.08 + 0.55 * p, ring = 0.6 + 1.2 * p, f0 = 110 + 40 * p;
    function part(f, f2, peak, len) {
      var o = a.createOscillator(), v = a.createGain();
      o.type = 'sine';
      o.frequency.setValueAtTime(f, t); o.frequency.exponentialRampToValueAtTime(f2, t + 0.25);
      v.gain.setValueAtTime(0.0001, t); v.gain.exponentialRampToValueAtTime(peak, t + 0.005);
      v.gain.exponentialRampToValueAtTime(0.0001, t + len);
      o.connect(v); v.connect(a.destination); o.start(t); o.stop(t + len + 0.05);
    }
    part(f0, 68, g, ring);                       // 가죽의 기본 떨림
    part(f0 * 1.59, 68 * 1.59, g * 0.35, ring * 0.35); // 가죽의 두 번째 떨림 모양
    var s = noise(a), f = a.createBiquadFilter(), v = a.createGain();   // 북채가 닿는 소리
    f.type = 'bandpass'; f.frequency.value = 1800; f.Q.value = 0.8;
    v.gain.setValueAtTime(g * 0.6, t); v.gain.exponentialRampToValueAtTime(0.0001, t + 0.05);
    s.connect(f); f.connect(v); v.connect(a.destination); s.start(t); s.stop(t + 0.08);
  }

  // 지진 울림: kind 'P'(짧고 빠르게 덜덜) / 'S'(낮고 크게 출렁), dur 초, t0 몇 초 뒤, stop 0~1 이면 그 지점에서 끊김(S파가 외핵에서 멈출 때)
  function quake(kind, dur, t0, stop) {
    var a = ac(); if (!a) return;
    var S = kind === 'S', t = a.currentTime + (t0 || 0), d = Math.max(0.4, +dur || 1.5);
    var end = stop ? d * stop : d, peak = S ? 0.6 : 0.35;
    var s = noise(a), f = a.createBiquadFilter(), v = a.createGain(), wob = a.createGain(), lfo = a.createOscillator(), depth = a.createGain();
    f.type = 'lowpass'; f.frequency.value = S ? 160 : 380; f.Q.value = 0.9;
    lfo.frequency.value = S ? 5 : 17; depth.gain.value = 0.45;   // 흔들림의 빠르기
    wob.gain.value = 0.55; lfo.connect(depth); depth.connect(wob.gain);
    v.gain.setValueAtTime(0.0001, t);
    v.gain.exponentialRampToValueAtTime(peak, t + (S ? 0.25 : 0.04));
    if (stop) v.gain.setValueAtTime(peak, t + end * 0.6);
    v.gain.exponentialRampToValueAtTime(0.0001, t + end + (stop ? 0.15 : 0.3));
    s.connect(f); f.connect(wob); wob.connect(v); v.connect(a.destination);
    s.start(t); lfo.start(t); s.stop(t + end + 0.4); lfo.stop(t + end + 0.4);
  }

  /* ── 그 밖의 현상 소리 (fxSound.bounce(0.8) 처럼 부른다; power 는 0~1, t0 는 몇 초 뒤) ── */
  function clamp(p, d) { p = +p; return isNaN(p) ? d : Math.max(0, Math.min(1, p)); }
  function at(a, t0) { return a.currentTime + (+t0 || 0); }
  // 걸러진 잡음 한 덩이: 필터 종류, 주파수(→끝 주파수), Q, 음량 배율, 길이, 올라가는 시간
  function burst(a, t, type, f1, f2, q, peak, len, rise) {
    var s = noise(a), f = a.createBiquadFilter(), v = a.createGain();
    f.type = type; f.Q.value = q;
    f.frequency.setValueAtTime(f1, t);
    if (f2 && f2 !== f1) f.frequency.exponentialRampToValueAtTime(f2, t + len);
    v.gain.setValueAtTime(0.0001, t);
    v.gain.exponentialRampToValueAtTime(Math.max(0.0002, VOL * 4 * peak), t + (rise || 0.005));
    v.gain.exponentialRampToValueAtTime(0.0001, t + len);
    s.connect(f); f.connect(v); v.connect(a.destination);
    s.start(t, Math.random()); s.stop(t + len + 0.05);
  }
  // 주파수가 미끄러지는 음 한 번(쿵·통의 몸통, 물방울)
  function body(a, t, f1, f2, peak, len, type) {
    var o = a.createOscillator(), v = a.createGain();
    o.type = type || 'sine';
    o.frequency.setValueAtTime(f1, t); o.frequency.exponentialRampToValueAtTime(f2, t + len);
    v.gain.setValueAtTime(0.0001, t); v.gain.exponentialRampToValueAtTime(Math.max(0.0002, VOL * 4 * peak), t + 0.004);
    v.gain.exponentialRampToValueAtTime(0.0001, t + len);
    o.connect(v); v.connect(a.destination); o.start(t); o.stop(t + len + 0.05);
  }

  var PH = {
    // 통통: 공이 바닥에 튕길 때
    bounce: function (power, t0) {
      var a = ac(); if (!a) return; var p = clamp(power, 0.6), t = at(a, t0);
      body(a, t, 260 + 160 * p, 120, 0.15 + 0.5 * p, 0.12 + 0.08 * p);
      burst(a, t, 'bandpass', 2200, 2200, 1, 0.05 + 0.15 * p, 0.03);
    },
    // 쿵·쾅: 떨어진 물체가 바닥에 닿거나 크게 부딪칠 때(클수록 낮고 길게)
    thud: function (power, t0) {
      var a = ac(); if (!a) return; var p = clamp(power, 0.6), t = at(a, t0);
      body(a, t, 140 - 50 * p, 45, 0.25 + 0.6 * p, 0.18 + 0.3 * p);
      burst(a, t, 'lowpass', 900 + 1500 * p, 200, 0.7, 0.15 + 0.35 * p, 0.12 + 0.25 * p);
    },
    // 딱: 단단한 두 물체가 부딪칠 때(수레·진자 추)
    clack: function (power, t0) {
      var a = ac(); if (!a) return; var p = clamp(power, 0.6), t = at(a, t0);
      body(a, t, 1600, 900, 0.1 + 0.3 * p, 0.05, 'triangle');
      burst(a, t, 'bandpass', 3200, 3200, 3, 0.15 + 0.35 * p, 0.04);
    },
    // 퐁: 물방울 하나
    drip: function (power, t0) {
      var a = ac(); if (!a) return; var p = clamp(power, 0.5), t = at(a, t0);
      body(a, t, 700 + 500 * p, 1700 + 800 * p, 0.2 + 0.2 * p, 0.08);
    },
    // 첨벙: 물에 넣거나 빠질 때
    splash: function (power, t0) {
      var a = ac(); if (!a) return; var p = clamp(power, 0.6), t = at(a, t0);
      body(a, t, 220, 90, 0.2 + 0.3 * p, 0.12);
      burst(a, t, 'bandpass', 1500, 600, 0.6, 0.15 + 0.35 * p, 0.25 + 0.35 * p, 0.01);
      for (var i = 0; i < 3; i++) PH.drip(0.3 + 0.5 * Math.random(), (+t0 || 0) + 0.15 + 0.12 * i + 0.08 * Math.random());
    },
    // 찌릭: 전기 불꽃·정전기 방전
    zap: function (power, t0) {
      var a = ac(); if (!a) return; var p = clamp(power, 0.6), t = at(a, t0);
      burst(a, t, 'highpass', 2500, 2500, 0.7, 0.15 + 0.35 * p, 0.05 + 0.1 * p);
      var o = a.createOscillator(), v = a.createGain();
      o.type = 'sawtooth';
      o.frequency.setValueAtTime(90, t);
      for (var i = 1; i < 8; i++) o.frequency.setValueAtTime(60 + Math.random() * 900, t + i * 0.012);
      v.gain.setValueAtTime(0.0001, t); v.gain.exponentialRampToValueAtTime(VOL * (0.6 + 1.2 * p), t + 0.003);
      v.gain.exponentialRampToValueAtTime(0.0001, t + 0.06 + 0.1 * p);
      o.connect(v); v.connect(a.destination); o.start(t); o.stop(t + 0.2 + 0.1 * p);
    },
    // 웅: 전류가 흐르는 동안 낮게 울림(전자석·전동기). dur 초
    hum: function (power, dur, t0) {
      var a = ac(); if (!a) return; var p = clamp(power, 0.5), t = at(a, t0), d = Math.max(0.2, +dur || 0.8), pk = VOL * (0.4 + 0.9 * p);
      var o = a.createOscillator(), f = a.createBiquadFilter(), v = a.createGain();
      o.type = 'sawtooth'; o.frequency.value = 60 + 60 * p; f.type = 'lowpass'; f.frequency.value = 500;
      v.gain.setValueAtTime(0.0001, t); v.gain.exponentialRampToValueAtTime(pk, t + 0.08);
      v.gain.setValueAtTime(pk, t + Math.max(0.09, d - 0.1)); v.gain.exponentialRampToValueAtTime(0.0001, t + d);
      o.connect(f); f.connect(v); v.connect(a.destination); o.start(t); o.stop(t + d + 0.05);
    },
    // 휘이: 바람. dur 초
    wind: function (power, dur, t0) {
      var a = ac(); if (!a) return; var p = clamp(power, 0.5), t = at(a, t0), d = Math.max(0.4, +dur || 1.5);
      var s = noise(a), f = a.createBiquadFilter(), v = a.createGain(), pk = VOL * (1.5 + 5 * p);
      f.type = 'bandpass'; f.Q.value = 2 + 4 * p;
      f.frequency.setValueAtTime(300 + 300 * p, t);
      f.frequency.linearRampToValueAtTime(600 + 1200 * p, t + d * 0.45);
      f.frequency.linearRampToValueAtTime(350 + 400 * p, t + d);
      v.gain.setValueAtTime(0.0001, t); v.gain.exponentialRampToValueAtTime(pk, t + d * 0.35);
      v.gain.exponentialRampToValueAtTime(0.0001, t + d);
      s.connect(f); f.connect(v); v.connect(a.destination); s.start(t, Math.random()); s.stop(t + d + 0.05);
    },
    // 쏴아: 비. dur 초
    rain: function (power, dur, t0) {
      var a = ac(); if (!a) return; var p = clamp(power, 0.5), t = at(a, t0), d = Math.max(0.5, +dur || 2), pk = VOL * (0.5 + 1.5 * p);
      var s = noise(a), f = a.createBiquadFilter(), v = a.createGain();
      f.type = 'highpass'; f.frequency.value = 1500 - 700 * p;
      v.gain.setValueAtTime(0.0001, t); v.gain.exponentialRampToValueAtTime(pk, t + 0.3);
      v.gain.setValueAtTime(pk, t + Math.max(0.31, d - 0.4)); v.gain.exponentialRampToValueAtTime(0.0001, t + d);
      s.connect(f); f.connect(v); v.connect(a.destination); s.start(t, Math.random()); s.stop(t + d + 0.05);
      for (var i = 0, n = Math.round(d * (3 + 10 * p)); i < n; i++) PH.drip(Math.random() * 0.6, (+t0 || 0) + Math.random() * (d - 0.2));
    },
    // 보글보글: 거품이 생길 때(끓음·기체 발생). dur 초
    fizz: function (power, dur, t0) {
      var a = ac(); if (!a) return; var p = clamp(power, 0.5), d = Math.max(0.3, +dur || 1.2);
      for (var i = 0, n = Math.round(d * (6 + 24 * p)); i < n; i++) {
        var f = 400 + Math.random() * 900;
        body(a, at(a, t0) + Math.random() * d, f, f * (1.6 + Math.random()), 0.08 + 0.12 * Math.random(), 0.03 + 0.03 * Math.random());
      }
      burst(a, at(a, t0), 'highpass', 4000, 4000, 0.5, 0.03 + 0.08 * p, d, d * 0.3);
    },
    // 화르륵: 불이 붙어 탈 때. dur 초
    fire: function (power, dur, t0) {
      var a = ac(); if (!a) return; var p = clamp(power, 0.6), t = at(a, t0), d = Math.max(0.4, +dur || 1.5);
      burst(a, t, 'lowpass', 700 + 800 * p, 400, 0.5, 0.25 + 0.35 * p, d, 0.15);
      for (var i = 0, n = Math.round(d * 12); i < n; i++) burst(a, t + Math.random() * d * 0.9, 'bandpass', 2500, 2500, 2, 0.05 + 0.15 * Math.random(), 0.015);
    },
    // 슝: 로켓 발사·빠르게 날아감. dur 초
    launch: function (power, dur, t0) {
      var a = ac(); if (!a) return; var p = clamp(power, 0.7), t = at(a, t0), d = Math.max(0.4, +dur || 1.5);
      burst(a, t, 'lowpass', 300, 2200, 0.8, 0.3 + 0.35 * p, d, 0.08);
      body(a, t, 50, 30, 0.3 + 0.4 * p, d * 0.7);
    },
    // 쿵쿵: 심장 한 번 뜀
    heart: function (power, t0) {
      var a = ac(); if (!a) return; var p = clamp(power, 0.6), t = at(a, t0);
      body(a, t, 75, 45, 0.35 + 0.5 * p, 0.14); body(a, t + 0.16, 65, 40, 0.25 + 0.4 * p, 0.12);
    },
    // 맑은 음(소리굽쇠·파동): hz 진동수, loud 0~1 (진폭), dur 초, type 파형
    pitch: function (hz, loud, dur, t0, type) {
      var a = ac(); if (!a) return; var t = at(a, t0), d = Math.max(0.1, +dur || 0.8), l = clamp(loud, 0.6), pk = VOL * (0.2 + 2 * l * l);
      var o = a.createOscillator(), v = a.createGain();
      o.type = type || 'sine'; o.frequency.value = Math.max(20, Math.min(12000, +hz || 440));
      v.gain.setValueAtTime(0.0001, t); v.gain.exponentialRampToValueAtTime(pk, t + 0.02);
      v.gain.setValueAtTime(pk, t + d * 0.6); v.gain.exponentialRampToValueAtTime(0.0001, t + d);
      o.connect(v); v.connect(a.destination); o.start(t); o.stop(t + d + 0.05);
    },
    // 쉭: 기체가 새거나 뿜어질 때. dur 초
    hiss: function (power, dur, t0) {
      var a = ac(); if (!a) return; var p = clamp(power, 0.5), d = Math.max(0.2, +dur || 0.8);
      burst(a, at(a, t0), 'highpass', 3000, 5000, 0.7, 0.1 + 0.25 * p, d, d * 0.2);
    },
    // 팡: 작은 터짐(풍선·수소 점화)
    pop: function (power, t0) {
      var a = ac(); if (!a) return; var p = clamp(power, 0.6), t = at(a, t0);
      burst(a, t, 'lowpass', 3000, 300, 0.7, 0.25 + 0.45 * p, 0.12 + 0.12 * p);
      body(a, t, 180, 60, 0.3 + 0.4 * p, 0.1);
    }
  };
  var phLast = {};

  function play(name, arg, force) {
    if (!on) return;
    var now = Date.now();
    if (!force && now - last < 70) return; // 겹침 방지
    last = now;
    try { SFX[name](arg); } catch (e) {}
  }
  window.fxSound = {
    play: function (n, a) { play(n, a, true); },
    drum: function (power, t0) { if (on) try { drum(power, t0); } catch (e) {} },
    quake: function (kind, dur, t0, stop) { if (on) try { quake(kind, dur, t0, stop); } catch (e) {} }
  };
  // fxSound.bounce(0.8), fxSound.wind(0.5, 2) … 같은 소리를 같은 값으로 30ms 안에 또 부르면(매 프레임 호출 등) 한 번만 낸다
  Object.keys(PH).forEach(function (k) {
    window.fxSound[k] = function () {
      if (!on) return;
      var now = Date.now(), id = k + Array.prototype.join.call(arguments, ",");
      if (now - (phLast[id] || 0) < 30) return;
      phLast[id] = now;
      try { PH[k].apply(null, arguments); } catch (e) {}
    };
  });

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
