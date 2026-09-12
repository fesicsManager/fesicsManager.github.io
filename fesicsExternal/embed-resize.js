(function () {
  'use strict';

  var INIT_MESSAGE = 'fesics:embed-init';
  var HEIGHT_MESSAGE = 'fesics:embed-height';
  var MAX_HEIGHT = 200000;
  var parentWindow = window.parent;
  var parentOrigin = '';
  var requestId = '';
  var active = false;
  var observer = null;
  var resizeHandler = null;
  var pageHideHandler = null;
  var pageShowHandler = null;
  var frameHandle = 0;
  var lastHeight = 0;
  var styleElement = null;
  var MIN_INSET = 16;
  var NARROW_WIDTH = 768;

  if (parentWindow === window) return;

  function referrerOrigin() {
    try {
      if (!document.referrer) return '';
      var origin = new URL(document.referrer).origin;
      return origin.indexOf('http://') === 0 || origin.indexOf('https://') === 0 ? origin : '';
    } catch (error) {
      return '';
    }
  }

  // 부모가 모바일에서 실험 좌우 여백을 0 으로 만들기 때문에, 본문이 화면 끝에 붙지 않도록
  // 좁은 화면에서만 최소 좌우 여백을 보장한다. 이미 16px 이상인 실험은 그대로 둔다.
  // ponytail: 인라인 스타일 1개로 처리. 실험별 레이아웃 차이가 생기면 그때 CSS 로 옮긴다.
  function applyMinInset() {
    var body = document.body;
    if (!body) return;

    body.style.removeProperty('padding-left');
    body.style.removeProperty('padding-right');
    if (window.innerWidth > NARROW_WIDTH) return;

    var style = getComputedStyle(body);
    if ((parseFloat(style.paddingLeft) || 0) < MIN_INSET) {
      body.style.setProperty('padding-left', MIN_INSET + 'px', 'important');
    }
    if ((parseFloat(style.paddingRight) || 0) < MIN_INSET) {
      body.style.setProperty('padding-right', MIN_INSET + 'px', 'important');
    }
  }

  function naturalHeight() {
    var body = document.body;
    if (!body) return 0;

    var bodyRect = body.getBoundingClientRect();
    var bodyStyle = getComputedStyle(body);
    var marginTop = parseFloat(bodyStyle.marginTop) || 0;
    var marginBottom = parseFloat(bodyStyle.marginBottom) || 0;
    var height = Math.max(bodyRect.height, body.scrollHeight);
    var natural = Math.ceil(height + marginTop + marginBottom);
    return natural > MAX_HEIGHT ? 0 : Math.max(0, natural);
  }

  function sendHeight() {
    frameHandle = 0;
    if (!active || !requestId) return;

    applyMinInset();
    var height = naturalHeight();
    if (!height || height === lastHeight) return;
    lastHeight = height;
    parentWindow.postMessage({
      type: HEIGHT_MESSAGE,
      requestId: requestId,
      height: height,
    }, parentOrigin);
  }

  function scheduleHeight() {
    if (!active || frameHandle) return;
    frameHandle = requestAnimationFrame(sendHeight);
  }

  function observe() {
    if (!document.body) return;
    document.documentElement.classList.add('fesics-embed-resize');
    document.body.classList.add('fesics-embed-resize');
    if (!styleElement) {
      styleElement = document.createElement('style');
      styleElement.textContent = 'html.fesics-embed-resize,body.fesics-embed-resize{height:auto!important;min-height:0!important;}';
      document.head.appendChild(styleElement);
    }

    if (observer) observer.disconnect();
    observer = typeof ResizeObserver === 'function' ? new ResizeObserver(scheduleHeight) : null;
    if (observer) observer.observe(document.body);
    if (!resizeHandler) {
      resizeHandler = scheduleHeight;
      window.addEventListener('resize', resizeHandler);
      window.addEventListener('load', resizeHandler);
    }
    if (document.fonts) document.fonts.ready.then(scheduleHeight);
    scheduleHeight();
  }

  function stopObserving() {
    if (observer) observer.disconnect();
    observer = null;
    if (resizeHandler) window.removeEventListener('resize', resizeHandler);
    if (resizeHandler) window.removeEventListener('load', resizeHandler);
    resizeHandler = null;
    if (frameHandle) cancelAnimationFrame(frameHandle);
    frameHandle = 0;
  }

  function onMessage(event) {
    if (event.source !== parentWindow || event.origin !== parentOrigin) return;
    var data = event.data;
    if (!data || data.type !== INIT_MESSAGE || typeof data.requestId !== 'string' || !data.requestId || data.requestId.length > 256) return;

    requestId = data.requestId;
    active = true;
    lastHeight = 0;
    observe();
    scheduleHeight();
  }

  function onPageHide() {
    stopObserving();
  }

  function onPageShow() {
    if (active) {
      lastHeight = 0;
      observe();
    }
  }

  parentOrigin = referrerOrigin();
  if (!parentOrigin) return;
  window.addEventListener('message', onMessage);
  pageHideHandler = onPageHide;
  pageShowHandler = onPageShow;
  window.addEventListener('pagehide', pageHideHandler);
  window.addEventListener('pageshow', pageShowHandler);
}());
