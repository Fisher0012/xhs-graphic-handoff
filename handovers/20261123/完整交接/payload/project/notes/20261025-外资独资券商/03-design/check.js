window.addEventListener('load',()=>{document.fonts.ready.then(()=>{
 const R=[];const vw=1080,vh=1440;
 const els=[...document.querySelectorAll('.page *')].filter(e=>e.children.length==0||e.matches('.title,.summary,.note,.num,.name,.desc,.paren,.src'));
 const leaf=[...document.querySelectorAll('.page *')].filter(e=>[...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim()));
 for(const e of leaf){const r=e.getBoundingClientRect();
   if(r.right>vw-63.5||r.left<63.5||r.bottom>vh||r.top<0) R.push('OUT '+e.className+' '+e.textContent.slice(0,15)+' '+[r.left,r.right,r.bottom].map(Math.round));
   if(e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).display!='inline') R.push('SCROLL '+e.className+' '+e.textContent.slice(0,15));}
 for(let i=0;i<leaf.length;i++)for(let j=i+1;j<leaf.length;j++){const a=leaf[i],b=leaf[j];if(a.contains(b)||b.contains(a))continue;
   const p=a.getBoundingClientRect(),q=b.getBoundingClientRect();
   if(p.left<q.right-1&&q.left<p.right-1&&p.top<q.bottom-1&&q.top<p.bottom-1)R.push('OVERLAP '+a.textContent.slice(0,10)+' | '+b.textContent.slice(0,10));}
 // bars
 document.querySelectorAll('.bar i,.track i').forEach(i=>{R.push('BAR '+(i.getBoundingClientRect().width/i.parentElement.getBoundingClientRect().width*100).toFixed(1))});
 const t=document.querySelector('.cover-title');if(t){const r=t.getBoundingClientRect();R.push('TITLEW '+r.width.toFixed(0)+' '+(r.width/952*100).toFixed(1)+'%')}
 const pre=document.createElement('pre');pre.id='RES';pre.textContent=R.join('\n');document.body.appendChild(pre);
});});
