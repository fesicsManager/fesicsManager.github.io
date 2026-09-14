# -*- coding: utf-8 -*-
"""전체 실험 목록 허브 페이지 생성"""
import os, re, json, html

OUT = "/mnt/user-data/outputs"

GROUPS = [
    ("elem34", "초등 3-4학년군"),
    ("elem56", "초등 5-6학년군"),
    ("m1", "중학교 1학년"),
    ("m2", "중학교 2학년"),
    ("m3", "중학교 3학년"),
    ("h1", "공통수학1"),
    ("h2", "공통수학2"),
    ("hd", "대수"),
    ("hc", "미적분Ⅰ"),
    ("hp", "확률과 통계"),
    ("hg", "기하"),
    ("hm", "미적분Ⅱ"),
]
GMAP = dict(GROUPS)

items = []
for fn in os.listdir(OUT):
    if not fn.endswith(".html") or fn == "index.html":
        continue
    pre = fn.split("_")[0]
    if pre not in GMAP:
        continue
    src = open(os.path.join(OUT, fn), encoding="utf-8").read()
    t = re.search(r"<title>(.*?)</title>", src, re.S)
    h = re.search(r'<h1>(.*?)</h1>', src, re.S)
    p = re.search(r'<p class="lead">(.*?)</p>', src, re.S)
    title = (h.group(1) if h else (t.group(1) if t else fn)).strip()
    lead = (p.group(1) if p else "").strip()
    # 제목에서 "— 질문" 부분 분리
    parts = re.split(r"\s+—\s+", title, 1)
    name = parts[0].strip()
    q = parts[1].strip() if len(parts) > 1 else ""
    items.append({
        "file": fn, "group": pre, "gname": GMAP[pre],
        "name": name, "q": q, "lead": lead,
        "mtime": os.path.getmtime(os.path.join(OUT, fn)),
    })

order = {g: i for i, (g, _) in enumerate(GROUPS)}
items.sort(key=lambda x: (order[x["group"]], x["mtime"]))

counts = {}
for it in items:
    counts[it["group"]] = counts.get(it["group"], 0) + 1

DATA = json.dumps(items, ensure_ascii=False)

btns = "".join(
    '<button class="fb" data-g="%s">%s <span class="cnt">%d</span></button>' % (g, n, counts.get(g, 0))
    for g, n in GROUPS if counts.get(g)
)

HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>수학 인터랙티브 실험 모음</title>
<style>
:root{--bg:#f6f9fc;--ink:#1f2937;--sub:#52627a;--line:#d7e0ec;--accent:#2563eb}
html{font-size:20px}
@media (max-width:760px){html{font-size:19.5px}}
@media (max-width:420px){html{font-size:19px}}
*{box-sizing:border-box}
body{margin:0;padding:1.2rem 0 4rem;
  font-family:"Pretendard","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;
  color:var(--ink);line-height:1.6;background-color:var(--bg);
  background-image:radial-gradient(circle,#ccd7e6 1.3px,transparent 1.3px);background-size:22px 22px}
.wrap{width:97%;max-width:1840px;margin:0 auto}
h1{font-size:1.6rem;margin:0 0 .3rem}
.lead{font-size:1rem;color:var(--sub);margin:0 0 1rem}
.tools{position:sticky;top:0;z-index:5;background:rgba(246,249,252,.96);
  padding:.8rem 0;border-bottom:2px solid var(--line);margin-bottom:1.2rem}
input[type=search]{width:100%;font-family:inherit;font-size:1rem;padding:.7rem .9rem;
  border:2px solid var(--line);border-radius:.7rem;background:#fff;color:var(--ink)}
input[type=search]:focus{outline:none;border-color:var(--accent)}
.filters{display:flex;gap:.4rem;flex-wrap:wrap;margin-top:.7rem}
.fb{font-family:inherit;font-size:.9rem;font-weight:700;padding:.45rem .8rem;
  border:2px solid var(--line);border-radius:.6rem;background:#fff;color:var(--sub);cursor:pointer;
  transition:background .15s,color .15s,border-color .15s,transform .1s}
.fb:hover{border-color:#b9c8dc}
.fb:active{transform:translateY(2px) scale(.98)}
.fb.on{background:var(--accent);border-color:var(--accent);color:#fff}
.fb .cnt{opacity:.65;font-weight:400;margin-left:.2rem}
h2.sec{font-size:1.15rem;margin:1.6rem 0 .7rem;padding-bottom:.3rem;border-bottom:2px solid var(--line)}
h2.sec .n{font-size:.9rem;font-weight:400;color:var(--sub);margin-left:.4rem}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:.8rem}
a.card{display:block;background:#fff;border:2px solid var(--line);border-radius:.9rem;
  padding:.9rem 1rem;text-decoration:none;color:inherit;
  transition:border-color .15s,transform .1s,box-shadow .15s}
a.card:hover{border-color:var(--accent);box-shadow:0 4px 14px rgba(37,99,235,.10)}
a.card:active{transform:translateY(2px)}
.card .nm{font-size:1rem;font-weight:800;margin-bottom:.25rem}
.card .q{font-size:.92rem;color:#b45309;font-weight:700;margin-bottom:.35rem}
.card .ld{font-size:.88rem;color:var(--sub)}
.empty{padding:2rem;text-align:center;color:var(--sub)}
.note{background:#fff8e1;border:2px solid #f5d97a;border-radius:.8rem;padding:.8rem 1rem;
  font-size:.95rem;margin-bottom:1.2rem}
</style>
</head>
<body>
<div class="wrap">
  <h1>수학 인터랙티브 실험 모음</h1>
  <p class="lead">초등 3학년부터 미적분Ⅱ까지 __TOTAL__개. 모두 «자유 탐구 → 기록표 → 데이터 확인» 구조이고, 값은 실제 계산으로 나옵니다.</p>
  <div class="note">각 실험은 슬라이더를 움직여 조건을 바꾸고, 실행 버튼으로 관찰한 뒤 <b>기록하기</b>를 누릅니다. 기록이 4개 이상 쌓이면 «데이터 확인» 탭이 열려 학생 자신의 기록만으로 결론을 검증합니다. 반례가 나오지 않으면 결론 대신 «더 해 보자»가 뜹니다.</div>

  <div class="tools">
    <input type="search" id="q" placeholder="실험 이름, 질문, 개념으로 검색">
    <div class="filters">
      <button class="fb on" data-g="all">전체 <span class="cnt">__TOTAL__</span></button>
      __BTNS__
    </div>
  </div>

  <div id="list"></div>
</div>

<script>
var DATA = __DATA__;
var GROUPS = __GORDER__;
var cur = 'all';

function esc(s){ return s.replace(/[&<>]/g, function(m){ return {'&':'&amp;','<':'&lt;','>':'&gt;'}[m]; }); }

function render(){
  var kw = document.getElementById('q').value.trim().toLowerCase();
  var list = document.getElementById('list');
  var shown = DATA.filter(function(d){
    if(cur !== 'all' && d.group !== cur) return false;
    if(!kw) return true;
    var hay = (d.name + ' ' + d.q + ' ' + d.lead + ' ' + d.gname).toLowerCase();
    return hay.indexOf(kw) >= 0;
  });
  if(shown.length === 0){
    list.innerHTML = '<div class="empty">찾는 실험이 없습니다.</div>';
    return;
  }
  var out = '', i, g;
  for(g = 0; g < GROUPS.length; g++){
    var key = GROUPS[g][0], gname = GROUPS[g][1];
    var arr = shown.filter(function(d){ return d.group === key; });
    if(arr.length === 0) continue;
    out += '<h2 class="sec">' + gname + '<span class="n">' + arr.length + '개</span></h2><div class="grid">';
    for(i = 0; i < arr.length; i++){
      var d = arr[i];
      out += '<a class="card" href="' + d.file + '">'
           + '<div class="nm">' + esc(d.name) + '</div>'
           + (d.q ? ('<div class="q">' + esc(d.q) + '</div>') : '')
           + '<div class="ld">' + esc(d.lead) + '</div></a>';
    }
    out += '</div>';
  }
  list.innerHTML = out;
}

document.getElementById('q').addEventListener('input', render);
var fbs = document.querySelectorAll('.fb');
for(var k = 0; k < fbs.length; k++){
  fbs[k].addEventListener('click', function(){
    for(var j = 0; j < fbs.length; j++) fbs[j].classList.remove('on');
    this.classList.add('on');
    cur = this.getAttribute('data-g');
    render();
  });
}
render();
</script>
</body>
</html>
"""

HTML = (HTML.replace("__TOTAL__", str(len(items)))
            .replace("__BTNS__", btns)
            .replace("__DATA__", DATA)
            .replace("__GORDER__", json.dumps([[g, n] for g, n in GROUPS if counts.get(g)], ensure_ascii=False)))

path = os.path.join(OUT, "index.html")
open(path, "w", encoding="utf-8").write(HTML)

print("총", len(items), "개")
for g, n in GROUPS:
    if counts.get(g):
        print(" ", n, counts[g])
print(path)
