/* Shared notation for plain-text laboratory content. Existing TeX/MathML is left to its renderer. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/1998/Math/MathML';
  var excluded = 'script,style,textarea,input,select,option,pre,code,svg,canvas,math,mjx-container,.MathJax,.katex,[contenteditable="true"],[data-math-typography="off"]';
  var blocks = 'p,li,td,th,label,button,summary,dt,dd,h1,h2,h3,h4,figcaption,caption,.eq,.fx-formula,.formula';
  var subs = {'₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5','₆':'6','₇':'7','₈':'8','₉':'9','₊':'+','₋':'−','ₖ':'k','ₛ':'s','ₙ':'n','ₘ':'m','ₜ':'t','ᵢ':'i','ⱼ':'j','ₐ':'a','ₑ':'e','ₒ':'o','ₓ':'x'};
  var sups = {'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9','⁺':'+','⁻':'−','ⁿ':'n'};
  function element(name, text) {
    var e = document.createElementNS(NS, name);
    if (text !== undefined) e.textContent = text;
    // Match the upright letters of the surrounding plain text instead of MathML's default italic.
    if (name === 'mi') e.setAttribute('mathvariant', 'normal');
    return e;
  }
  function eligible(node) {
    return node.parentElement && !node.parentElement.closest(excluded) &&
      !/\$|\\\(|\\\[/.test((node.parentElement.closest(blocks) || node.parentElement).textContent);
  }
  function textNodes(root) {
    var nodes = [], walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) if (eligible(walker.currentNode)) nodes.push(walker.currentNode);
    return nodes;
  }
  function normalize(node) {
    var s = node.nodeValue.replace(/μk/g, 'μₖ');
    // An explicit underscore is required; words and JavaScript identifiers are never guessed.
    var re = /(?<![A-Za-z0-9_α-ωΑ-Ω])([A-Za-zα-ωΑ-Ω])_(\{[A-Za-z0-9+−-]{1,12}\}|(?:net|rms|eff|esc|max|min|cm|eq|[A-Za-z]|\d+))(?![A-Za-z0-9_])/g;
    var fragment = document.createDocumentFragment(), last = 0, match, changed = false;
    while ((match = re.exec(s))) {
      fragment.appendChild(document.createTextNode(s.slice(last, match.index) + match[1]));
      var sub = document.createElement('sub');
      sub.textContent = match[2].replace(/[{}]/g, '');
      fragment.appendChild(sub);
      last = re.lastIndex; changed = true;
    }
    if (changed) {
      fragment.appendChild(document.createTextNode(s.slice(last)));
      node.replaceWith(fragment);
    } else if (s !== node.nodeValue) node.nodeValue = s;
  }
  function attach(row, tag, script) {
    var base = row.lastChild;
    if (!base) { row.appendChild(script); return; }
    var e = element(tag); row.removeChild(base); e.append(base, script); row.appendChild(e);
  }
  function tokens(text, row) {
    for (var i = 0; i < text.length;) {
      var c = text[i], map = subs[c] ? subs : sups[c] ? sups : null;
      if (map) {
        var value = '', kind = map === subs ? 'msub' : 'msup';
        while (i < text.length && map[text[i]]) value += map[text[i++]];
        attach(row, kind, element(/^\d+$/.test(value) ? 'mn' : 'mtext', value));
      } else if (c === '√') {
        var nested = rootEnd(text, i);
        if (nested) { var radical = element('msqrt'), inside = element('mrow'); tokens(text.slice(nested.from, nested.to), inside); radical.appendChild(inside); row.appendChild(radical); i = nested.end; }
        else { row.appendChild(element('mo', c)); i++; }
      } else if (/\d/.test(c)) {
        var num = text.slice(i).match(/^\d+(?:\.\d+)?/)[0]; row.appendChild(element('mn', num)); i += num.length;
      } else if (/[A-Za-zα-ωΑ-Ω]/.test(c)) {
        var fn = text.slice(i).match(/^(sin|cos|tan|ln|log|exp)(?![a-z])/);
        row.appendChild(element('mi', fn ? fn[0] : c)); i += fn ? fn[0].length : 1;
      } else if (/\s/.test(c)) { i++; }
      else if (/[가-힣]/.test(c)) {
        var word = text.slice(i).match(/^[가-힣]+/)[0]; row.appendChild(element('mtext', word)); i += word.length;
      } else { row.appendChild(element('mo', c)); i++; }
    }
  }
  function toMath(fragment) {
    var row = element('mrow');
    function add(nodes, target) {
      Array.from(nodes).forEach(function (node) {
        if (node.nodeType === Node.TEXT_NODE) tokens(node.nodeValue, target);
        else if (node.nodeType === Node.ELEMENT_NODE) {
          var tag = node.localName;
          if (tag === 'sub' || tag === 'sup') attach(target, tag === 'sub' ? 'msub' : 'msup', toMath(node));
          else if (tag === 'math') Array.from(node.childNodes).forEach(function (child) { target.appendChild(child.cloneNode(true)); });
          else add(node.childNodes, target);
        }
      });
    }
    add(fragment.childNodes, row); return row;
  }
  function rootEnd(text, start) {
    var i = start + 1;
    while (text[i] === ' ') i++;
    var begin = i, opener = text[i], stack = [];
    if (opener === '|') { var close = text.indexOf('|', i + 1); return close > i + 1 ? {from:i, to:close + 1, end:close + 1} : null; }
    if (opener === '(' || opener === '[' || opener === '{') {
      for (; i < text.length && i - begin < 300; i++) {
        var c = text[i];
        if (c === '(' || c === '[' || c === '{') stack.push(c);
        else if (c === ')' || c === ']' || c === '}') {
          if (stack.pop() !== {')':'(',']':'[','}':'{'}[c]) return null;
          if (!stack.length) return {from:begin + 1, to:i, end:i + 1};
        }
      }
      return null;
    }
    // A bare radical covers one number or one contiguous symbolic product, never a following sum.
    var atom = text.slice(i).match(/^(?:\d+(?:\.\d+)?|[A-Za-zα-ωΑ-Ω]+|절대온도|부품 수|분자량|지름|경사|분산|평균|우변|값)/);
    if (!atom) return null;
    i += atom[0].length;
    while (subs[text[i]] || sups[text[i]] || /[\u0300-\u036f]/.test(text[i] || '\0')) i++;
    return {from:begin, to:i, end:i};
  }
  function renderPowers(container) {
    if (/\$|\\\(|\\\[|프로그래밍|엑셀/.test(container.textContent)) return;
    var nodes = textNodes(container), text = '', spans = [];
    nodes.forEach(function (node) { spans.push({node:node, start:text.length, end:text.length + node.length}); text += node.nodeValue; });
    var matches = [];
    for (var i = 1; i < text.length; i++) if (text[i] === '^' && /[A-Za-zα-ωΑ-Ω0-9)]/.test(text[i - 1])) {
      var b;
      if ('([{'.includes(text[i + 1])) b = rootEnd(text, i);
      else {
        var atom = text.slice(i + 1).match(/^(?:[+−-]?\d+(?:\.\d+)?|[A-Za-zα-ωΑ-Ω])(?![A-Za-z0-9])/);
        if (atom) b = {from:i + 1, to:i + 1 + atom[0].length, end:i + 1 + atom[0].length};
      }
      if (b) { matches.push({start:i, bounds:b}); i = b.end - 1; }
    }
    function point(offset, end) {
      for (var j = 0; j < spans.length; j++) if (offset < spans[j].end || (end && offset === spans[j].end)) return {node:spans[j].node, offset:offset - spans[j].start};
    }
    matches.reverse().forEach(function (match) {
      var b = match.bounds, a = point(match.start), z = point(b.end, true), c = point(b.from), d = point(b.to, true);
      if (!a || !z || !c || !d || !a.node.isConnected) return;
      var inner = document.createRange(); inner.setStart(c.node, c.offset); inner.setEnd(d.node, d.offset);
      var sup = document.createElement('sup'); sup.appendChild(inner.cloneContents());
      var range = document.createRange(); range.setStart(a.node, a.offset); range.setEnd(z.node, z.offset);
      range.deleteContents(); range.insertNode(sup); renderPowers(sup);
    });
  }
  function renderRoots(container) {
    var nodes = textNodes(container), text = '', spans = [];
    nodes.forEach(function (node) { spans.push({node:node, start:text.length, end:text.length + node.length}); text += node.nodeValue; });
    // TeX delimiters can be split between inline elements. Leave the whole container to MathJax.
    if (/\$|\\\(|\\\[/.test(container.textContent)) return;
    var matches = [];
    for (var i = 0; i < text.length; i++) if (text[i] === '√') {
      var bounds = rootEnd(text, i);
      if (bounds && bounds.to > bounds.from) {
        if (!'([{'.includes(text.slice(i + 1).trimStart()[0])) {
          for (var j = 0; j < spans.length; j++) if (spans[j].start === bounds.end && spans[j].node.parentElement.closest('sub,sup')) {
            bounds.end = spans[j].end; bounds.to = bounds.end;
          }
        }
        var indexStart = i, index = '';
        while (indexStart > 0 && sups[text[indexStart - 1]]) index = sups[text[--indexStart]] + index;
        if (index && /[A-Za-zα-ωΑ-Ω0-9∫₀-₉⁰-⁹]/.test(text[indexStart - 1] || '')) { index = ''; indexStart = i; }
        matches.push({start:indexStart, index:index, bounds:bounds}); i = bounds.end - 1; }
    }
    function point(offset, end) {
      for (var j = 0; j < spans.length; j++) if (offset < spans[j].end || (end && offset === spans[j].end))
        return {node:spans[j].node, offset:offset - spans[j].start};
      return null;
    }
    matches.reverse().forEach(function (match) {
      var bounds = match.bounds, a = point(match.start), b = point(bounds.end, true), c = point(bounds.from), d = point(bounds.to, true);
      if (!a || !b || !c || !d || !a.node.isConnected) return;
      var inner = document.createRange(); inner.setStart(c.node, c.offset); inner.setEnd(d.node, d.offset);
      var radicand = toMath(inner.cloneContents());
      var math = element('math'), root = element(match.index ? 'mroot' : 'msqrt');
      math.setAttribute('aria-label', (match.index ? match.index + '제곱근 ' : '√') + '(' + text.slice(bounds.from, bounds.to) + ')');
      root.appendChild(radicand); if (match.index) root.appendChild(element(/^\d+$/.test(match.index) ? 'mn' : 'mi', match.index)); math.appendChild(root);
      var range = document.createRange(); range.setStart(a.node, a.offset); range.setEnd(b.node, b.offset);
      range.deleteContents(); range.insertNode(math);
    });
  }
  function format(root) {
    if (!root || !root.isConnected || (root.nodeType === 1 && root.closest(excluded))) return;
    textNodes(root).forEach(normalize);
    var containers = new Set();
    textNodes(root).forEach(function (node) {
      if (/[√^]/.test(node.nodeValue)) containers.add(node.parentElement.closest(blocks) || node.parentElement);
    });
    containers.forEach(renderPowers); containers.forEach(renderRoots);
  }
  function installCanvasMath() {
    if (!window.CanvasRenderingContext2D) return;
    var proto = CanvasRenderingContext2D.prototype, native = proto.fillText;
    if (native.fxMathTypography) return;
    function expression(text) {
      var runs = [], plain = '';
      function flush() { if (plain) runs.push({text:plain}); plain = ''; }
      for (var i = 0; i < text.length;) {
        if (text[i] === '√') {
          var b = rootEnd(text, i);
          if (b) {
            var index = '', end = plain.length;
            while (end > 0 && sups[plain[end - 1]]) index = sups[plain[--end]] + index;
            if (index && /[A-Za-zα-ωΑ-Ω0-9∫₀-₉⁰-⁹]/.test(plain[end - 1] || '')) index = '';
            if (index) plain = plain.slice(0, end);
            flush(); runs.push({root:expression(text.slice(b.from, b.to)), index:index}); i = b.end; continue;
          }
        } else if (text[i] === '^' && i && /[A-Za-zα-ωΑ-Ω0-9)]/.test(text[i - 1])) {
          var power;
          if ('([{'.includes(text[i + 1])) power = rootEnd(text, i);
          else { var atom = text.slice(i + 1).match(/^(?:[+−-]?\d+(?:\.\d+)?|[A-Za-zα-ωΑ-Ω])(?![A-Za-z0-9])/); if (atom) power = {from:i + 1, to:i + 1 + atom[0].length, end:i + 1 + atom[0].length}; }
          if (power) { flush(); runs.push({script:expression(text.slice(power.from, power.to)), up:true}); i = power.end; continue; }
        } else if (text[i] === '_' && i && /[A-Za-zα-ωΑ-Ω]/.test(text[i - 1])) {
          var sub = text.slice(i + 1).match(/^(?:net|rms|eff|esc|max|min|cm|eq|[A-Za-z]|\d+)(?![A-Za-z0-9_])/);
          if (sub) { flush(); runs.push({script:[{text:sub[0]}], up:false}); i += sub[0].length + 1; continue; }
        }
        plain += text[i++];
      }
      flush(); return runs;
    }
    function layout(ctx, runs, size, font) {
      var width = 0, ascent = size * .8, descent = size * .2;
      runs.forEach(function (run) {
        run.x = width;
        ctx.font = font.replace(/\d+(?:\.\d+)?px/, size + 'px');
        if (run.text !== undefined) run.width = ctx.measureText(run.text).width;
        else if (run.script) {
          run.box = layout(ctx, run.script, size * .7, font); run.width = run.box.width;
          run.shift = run.up ? -size * .48 : size * .24;
          ascent = Math.max(ascent, run.box.ascent - run.shift); descent = Math.max(descent, run.box.descent + run.shift);
        } else {
          run.box = layout(ctx, run.root, size, font); ctx.font = font.replace(/\d+(?:\.\d+)?px/, size + 'px');
          run.sign = ctx.measureText('√').width;
          ctx.font = font.replace(/\d+(?:\.\d+)?px/, size * .5 + 'px');
          run.indexWidth = run.index ? ctx.measureText(run.index).width * .65 : 0;
          run.width = run.indexWidth + run.sign + run.box.width + 2;
          ascent = Math.max(ascent, run.box.ascent + 2); descent = Math.max(descent, run.box.descent);
        }
        width += run.width;
      });
      return {runs:runs, width:width, ascent:ascent, descent:descent, size:size};
    }
    function draw(ctx, box, x, y, font) {
      box.runs.forEach(function (run) {
        var at = x + run.x, size = box.size;
        ctx.font = font.replace(/\d+(?:\.\d+)?px/, size + 'px');
        if (run.text !== undefined) native.call(ctx, run.text, at, y);
        else if (run.script) draw(ctx, run.box, at, y + run.shift, font);
        else {
          if (run.index) { ctx.font = font.replace(/\d+(?:\.\d+)?px/, size * .5 + 'px'); native.call(ctx, run.index, at, y - size * .55); }
          ctx.font = font.replace(/\d+(?:\.\d+)?px/, size + 'px');
          var signX = at + run.indexWidth, top = Math.max(size * .8, run.box.ascent) + 1;
          ctx.save(); ctx.translate(signX, y); ctx.scale(1, top / (size * .8)); native.call(ctx, '√', 0, 0); ctx.restore();
          draw(ctx, run.box, signX + run.sign, y, font);
          // fillRect does not disturb the caller's current path or stroke settings.
          ctx.fillRect(signX + run.sign * .7, y - top, run.sign * .3 + run.box.width + 2, Math.max(.7, size / 20));
        }
      });
    }
    function fillText(text, x, y, maxWidth) {
      var value = String(text), match = this.font.match(/(\d+(?:\.\d+)?)px/);
      if ((maxWidth !== undefined && !(maxWidth > 0)) || !match || !/[√^_]/.test(value) || !Number.isFinite(x) || !Number.isFinite(y) || this.direction === 'rtl') return native.apply(this, arguments);
      var runs = expression(value);
      if (!runs.some(function (run) { return run.root || run.script; })) return native.apply(this, arguments);
      this.save();
      try {
        var font = this.font, box = layout(this, runs, +match[1], font), align = this.textAlign, baseline = this.textBaseline;
        var drawnWidth = maxWidth !== undefined ? Math.min(box.width, maxWidth) : box.width;
        if (align === 'center') x -= drawnWidth / 2; else if (align === 'right' || align === 'end') x -= drawnWidth;
        if (baseline === 'middle') y += (box.ascent - box.descent) / 2;
        else if (baseline === 'top' || baseline === 'hanging') y += box.ascent;
        else if (baseline === 'bottom' || baseline === 'ideographic') y -= box.descent;
        this.textAlign = 'left'; this.textBaseline = 'alphabetic';
        if (maxWidth !== undefined && maxWidth > 0 && box.width > maxWidth) { this.translate(x, y); this.scale(maxWidth / box.width, 1); x = 0; y = 0; }
        draw(this, box, x, y, font);
      } finally { this.restore(); }
    }
    fillText.fxMathTypography = true; proto.fillText = fillText;
  }

  function start() {
    if (document.getElementById("fx-math-typography-style")) return;
    var style = document.createElement('style'); style.id = 'fx-math-typography-style';
    style.textContent = 'math{font-family:"Cambria Math","STIX Two Math",math;font-size:1.06em;line-height:normal}sub,sup{font-size:.75em;line-height:0}';
    document.head.appendChild(style);
    format(document.body);
    var pending = new Set(), scheduled = false;
    var observer = new MutationObserver(function (changes) {
      changes.forEach(function (change) {
        var target = change.target.nodeType === 3 ? change.target.parentElement : change.target;
        if (target && !target.closest(excluded)) pending.add(target);
      });
      if (!pending.size || scheduled) return;
      scheduled = true;
      requestAnimationFrame(function () {
        observer.disconnect(); pending.forEach(format); pending.clear(); scheduled = false;
        observer.observe(document.body, {childList:true, subtree:true, characterData:true});
      });
    });
    observer.observe(document.body, {childList:true, subtree:true, characterData:true});
  }
  installCanvasMath();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, {once:true}); else start();
})();
