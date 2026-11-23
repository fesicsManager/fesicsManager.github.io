/* 캔버스 글자 맞추기(261117): 아주 좁은 화면(240px 안팎)에서 캔버스 밖으로 나가 잘리던 글자를
 * 글씨를 줄이고(원래의 70%까지, 최소 9px) 안쪽으로 당겨 그린다. 그래도 넓으면 fillText 의 maxWidth 로 좁혀 다 보이게.
 * 기준 위치(x)가 캔버스 밖인 글자는 일부러 밖에 둔 것(들어오는 애니메이션 등)으로 보고 손대지 않는다.
 * 실험 HTML 의 <head> 에서 <script src="/fesicsExternal/fxfit.js"></script> 로 실험 코드보다 먼저 불러야
 * 처음 그리는 화면부터 적용된다(defer 로 늦게 부르면 첫 화면은 잘린 채 남는다).
 */
(function () {
  'use strict';
  var C = window.CanvasRenderingContext2D;
  if (!C || C.prototype.__fxFit) return;
  C.prototype.__fxFit = true;

  function fit(orig) {
    return function (s, x, y, maxW) {
      try {
        var t = this.getTransform();
        var cv = this.canvas;
        if (!cv || Math.abs(t.b) > 1e-3 || Math.abs(t.c) > 1e-3 || t.a <= 0) return orig.apply(this, arguments);
        var cw = cv.width;
        var ax = t.a * x + t.e; // 기준 위치(기기 픽셀)
        if (ax < 0 || ax > cw) return orig.apply(this, arguments);
        var str = String(s);
        var w = this.measureText(str).width;
        if (maxW != null && maxW < w) w = maxW;
        var al = this.textAlign;
        var off = function (ww) { return al === 'center' ? -ww / 2 : (al === 'right' || al === 'end') ? -ww : 0; };
        var L = t.a * (x + off(w)) + t.e, R = L + t.a * w;
        if (L >= -0.5 && R <= cw + 0.5) return orig.apply(this, arguments);

        var m = 2 * (cv.clientWidth ? cw / cv.clientWidth : 1); // 양쪽 2 CSS px 여백
        var avail = (cw - 2 * m) / t.a; // 쓸 수 있는 폭(그리기 단위)
        var font = this.font;
        if (w > avail) {
          var mm = /(\d+(?:\.\d+)?)px/.exec(font);
          if (mm) {
            var sz = +mm[1];
            var nsz = Math.max(sz * avail / w, sz * 0.7, Math.min(sz, 9));
            this.font = font.replace(mm[0], nsz.toFixed(1) + 'px');
            w = this.measureText(str).width;
            if (maxW != null && maxW < w) w = maxW;
          }
        }
        var narrow = w > avail;
        if (narrow) w = avail;
        L = t.a * (x + off(w)) + t.e; R = L + t.a * w;
        var dx = L < m ? (m - L) / t.a : R > cw - m ? (cw - m - R) / t.a : 0;
        var r = narrow ? orig.call(this, str, x + dx, y, avail) : orig.call(this, str, x + dx, y);
        this.font = font;
        return r;
      } catch (e) {
        return orig.apply(this, arguments);
      }
    };
  }
  C.prototype.fillText = fit(C.prototype.fillText);
  C.prototype.strokeText = fit(C.prototype.strokeText);
})();

/* 눈금 숫자 겹침 막기(261122): 같은 줄에 늘어선 눈금 숫자끼리 달라붙으면 뒤에 오는 것을 그리지 않는다.
 * 숫자꼴 글자끼리, 밑줄 위치가 거의 같을 때만 건너뛴다(본문 글자는 손대지 않는다). */
(function () {
  'use strict';
  var C = window.CanvasRenderingContext2D;
  if (!C || C.prototype.__fxTick) return;
  C.prototype.__fxTick = true;
  var NUM = /^[-−+]?[0-9][0-9.,]*\s*%?$/;
  var map = new WeakMap();
  function slot(cv) { var a = map.get(cv); if (!a) { a = []; map.set(cv, a); } return a; }
  function full(ctx, x, y, w, h) {
    try {
      var t = ctx.getTransform(), cv = ctx.canvas;
      var L = t.a * x + t.e, T = t.d * y + t.f;
      return L <= 1 && T <= 1 && L + t.a * w >= cv.width - 1 && T + t.d * h >= cv.height - 1;
    } catch (e) { return false; }
  }
  var ocr = C.prototype.clearRect;
  C.prototype.clearRect = function (x, y, w, h) { if (full(this, x, y, w, h)) map.set(this.canvas, []); return ocr.apply(this, arguments); };
  var ofr = C.prototype.fillRect;
  C.prototype.fillRect = function (x, y, w, h) { if (full(this, x, y, w, h)) map.set(this.canvas, []); return ofr.apply(this, arguments); };
  var oft = C.prototype.fillText;
  C.prototype.fillText = function (s, x, y, mw) {
    try {
      var str = String(s), t = this.getTransform(), cv = this.canvas;
      if (Math.abs(t.b) > 1e-3 || Math.abs(t.c) > 1e-3) return oft.apply(this, arguments);
      var m = this.measureText(str), w = m.width;
      if (mw != null && mw < w) w = mw;
      if (!(w > 0)) return oft.apply(this, arguments);
      var al = this.textAlign;
      var ox = al === 'center' ? -w / 2 : (al === 'right' || al === 'end') ? -w : 0;
      var L = t.a * (x + ox) + t.e, R = L + t.a * w, Y = t.d * y + t.f;
      var a = slot(cv), isn = NUM.test(str.trim()), i, b;
      if (isn) {
        for (i = a.length - 1; i >= 0; i--) {
          b = a[i];
          if (!b.n || Math.abs(b.y - Y) > 3) continue;
          var ix = Math.min(R, b.R) - Math.max(L, b.L);
          if (ix > 1 && ix > 0.25 * Math.min(R - L, b.R - b.L)) return;   // 달라붙으면 안 그림
        }
      }
      if (a.length < 400) a.push({ L: L, R: R, y: Y, n: isn });
    } catch (e) { }
    return oft.apply(this, arguments);
  };
})();
