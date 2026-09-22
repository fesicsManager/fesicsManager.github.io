const fs=require('fs'),path=require('path');
const root=process.argv[2], real=process.argv[3]; const folders=process.argv.slice(4);
let bad=0;
for(const f of folders){
  const dir=path.join(root,'content',f);
  for(const fn of fs.readdirSync(dir).filter(x=>x.endsWith('.json'))){
    const p=path.join(dir,fn); let j;
    try{ j=JSON.parse(fs.readFileSync(p,'utf8')); }catch(e){ console.log('PARSE',f,fn,e.message); bad++; continue; }
    const req=['unit','title','lead','flow','lab','index','recall','concepts','formula','cuts','examples','quiz','checklist','next'];
    for(const k of req) if(!(k in j)){console.log('MISSING',f,fn,k);bad++;}
    if(j.quiz.length!==4){console.log('QUIZLEN',f,fn,j.quiz.length);bad++;}
    j.quiz.forEach((q,i)=>{
      if(q.opts.length!==4){console.log('OPTS',f,fn,i);bad++;}
      if(!(q.ans>=0&&q.ans<=3)){console.log('ANS',f,fn,i);bad++;}
      const keys=Object.keys(q.wrong).sort();
      const exp=[0,1,2,3].filter(x=>x!==q.ans).map(String);
      if(keys.join()!==exp.join()){console.log('WRONG',f,fn,i,keys.join());bad++;}
    });
    const txt=fs.readFileSync(p,'utf8');
    if(/&[lr]squo>|&[lr]dquo>/.test(txt)){console.log('TYPO',f,fn);bad++;}
    // links
    const base=path.join(real,'notes',f);
    for(const h of [j.lab.href,j.next.href,j.index]){
      const t=path.resolve(base,h.split('#')[0]);
      if(!fs.existsSync(t)){console.log('LINK',f,fn,h);bad++;}
    }
  }
  console.log(f, fs.readdirSync(dir).filter(x=>x.endsWith('.json')).length,'files');
}
console.log('bad=',bad);
