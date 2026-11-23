/* 넓은 화면에서 실험 장면을 통째로 키운다 (261123).
 *
 * 휴대폰에서는 캔버스가 화면 폭을 다 써서 글씨가 알맞게 보이지만, PC 에서는 장면 칸이
 * 좁게 묶여 있어 그림도 글씨도 작게 보였다. 여기서 정한 배율 k 만큼 그리기 좌표계를
 * 통째로 확대하므로, 휴대폰에서 확인한 배치가 그대로 유지되고 글자 겹침이 새로 생기지 않는다.
 *
 * 쓰는 곳: 실험 HTML 의 fitCanvas()·sizeScene() 이 window.fxZoom(폭) 을 불러 쓴다.
 * 이 파일이 없어도 실험은 그대로 돌아간다(그때는 k = 1).
 */
(function () {
  'use strict';
  var BASE = 430;   // 휴대폰에서 보던 기준 폭(이보다 넓어지면 그만큼 키운다)
  var MAX = 1.75;   // 너무 커지지 않게 막는다

  window.fxZoom = function (w) {
    w = +w || 0;
    if (!(w > BASE)) return 1;
    var k = w / BASE;
    return k > MAX ? MAX : k;
  };
})();
