/* 좁은 화면에서 '자유 탐구 / 데이터 검증 / 과학 원리' 버튼이 세로로 쌓이지 않고 한 줄 탭처럼 보이게 한다.
 * 실험마다 탭 줄 클래스가 달라서 '자유 탐구' 버튼의 부모를 찾아 표시한다. 과학 원리 버튼은 나중에 같은 줄에 붙는다.
 * 실험 HTML 에서는 <script src="/fesicsExternal/fxtabbar.js" defer></script> 한 줄로 불러온다.
 */
(function () {
  'use strict';
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', markTabbar);
  else markTabbar();

  function markTabbar() {
    if (document.getElementById('fxTabbarStyle')) return;
    var buttons = document.querySelectorAll('button');
    var bar = null;
    for (var i = 0; i < buttons.length; i++) {
      if (buttons[i].textContent.indexOf('자유 탐구') >= 0) { bar = buttons[i].parentElement; break; }
    }
    if (!bar || bar.querySelectorAll(':scope > button').length < 2) return;
    bar.classList.add('fx-tabbar');
    var s = document.createElement('style');
    s.id = 'fxTabbarStyle';
    s.textContent =
      '@media (max-width:640px){' +
      '.fx-tabbar{display:flex!important;flex-wrap:nowrap!important;gap:4px!important;padding:4px!important;background:rgba(15,23,42,.06)!important;border-radius:14px!important}' +
      '.fx-tabbar>button{flex:1 1 0!important;min-width:0!important;margin:0!important;padding:.6em .25em!important;font-size:.72rem!important;line-height:1.2!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important;border-radius:10px!important;transform:none!important;box-shadow:none!important}' +
      '}';
    document.head.appendChild(s);
  }
})();
