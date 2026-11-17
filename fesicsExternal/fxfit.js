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
