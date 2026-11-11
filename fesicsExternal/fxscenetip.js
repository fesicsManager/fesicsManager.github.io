/* 실험 그림(#scene 캔버스)은 눌러도 반응하지 않으므로, 누르면 '아래에서 조작해 주세요' 안내를 잠깐 띄운다.
 * 그림을 직접 다루지 않는 실험 틀(sizeScene)에만 넣는다.
 * 실험 HTML 에서는 <script src="/fesicsExternal/fxscenetip.js" defer></script> 한 줄로 불러온다.
 */
(function () {
  'use strict';
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  function init() {
    var scene = document.getElementById('scene');
    if (!scene) return;
    var tip = null, timer = 0;
    scene.style.cursor = 'help';
    scene.addEventListener('click', function () {
      var box = scene.parentNode;
      if (getComputedStyle(box).position === 'static') box.style.position = 'relative';
      if (!tip) {
        tip = document.createElement('div');
        tip.setAttribute('role', 'status');
        tip.textContent = '그림은 보는 곳이에요. 아래 버튼으로 조작해 주세요 👇';
        tip.style.cssText = 'position:absolute;left:50%;transform:translate(-50%,-50%);max-width:86%;' +
          'padding:10px 14px;border-radius:10px;background:rgba(30,40,51,.9);color:#fff;font-size:15px;' +
          'line-height:1.45;text-align:center;pointer-events:none;opacity:0;transition:opacity .25s;z-index:5';
        box.appendChild(tip);
      }
      tip.style.top = (scene.offsetTop + scene.offsetHeight / 2) + 'px';
      tip.style.opacity = '1';
      clearTimeout(timer);
      timer = setTimeout(function () { tip.style.opacity = '0'; }, 1800);
    });
  }
})();
