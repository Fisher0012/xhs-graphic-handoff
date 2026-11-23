// 自动检查：越出版心(76px)/画布、元素重叠、横向溢出、行首标点、孤字成行；打印封面标题字号与占宽
window.addEventListener('load',()=>{document.fonts.ready.then(()=>{
 const R=[];const vw=1080,vh=1440,M=75;
 const leaf=[...document.querySelectorAll('.wrap *')].filter(e=>[...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim()));
 for(const e of leaf){const r=e.getBoundingClientRect();
   if(r.right>vw-M+0.5||r.left<M-0.5||r.bottom>vh||r.top<0) R.push('OUT '+e.className+' '+e.textContent.slice(0,15)+' '+[r.left,r.right,r.bottom].map(Math.round));
   if(e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).display!='inline') R.push('SCROLL '+e.className+' '+e.textContent.slice(0,15));}
 for(let i=0;i<leaf.length;i++)for(let j=i+1;j<leaf.length;j++){const a=leaf[i],b=leaf[j];if(a.contains(b)||b.contains(a))continue;
   const p=a.getBoundingClientRect(),q=b.getBoundingClientRect();
   if(p.left<q.right-1&&q.left<p.right-1&&p.top<q.bottom-1&&q.top<p.bottom-1)R.push('OVERLAP '+a.textContent.slice(0,10)+' | '+b.textContent.slice(0,10));}
 // 页脚红线与正文的距离
 const ln=document.querySelector('.foot .ln');if(ln){const lr=ln.getBoundingClientRect();let mx=0,who='';for(const e of leaf){if(e.closest('.foot'))continue;const r=e.getBoundingClientRect();if(r.bottom>mx){mx=r.bottom;who=e.textContent.slice(0,10)}}R.push('GAP_TO_FOOTLINE '+(lr.top-mx).toFixed(0)+'px (最低文字: '+who+')');if(lr.top-mx<16)R.push('TOO_CLOSE_FOOT');}
 // 行检查：按块级元素收集字符所在行
 const blocks=[...document.querySelectorAll('.wrap *')].filter(e=>getComputedStyle(e).display!='inline'&&[...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim()||n.nodeType==1&&getComputedStyle(n).display=='inline'));
 const P='，。、；：？！）》」』】,.;:?!)%';
 for(const b of blocks){const lines=[];const w=document.createTreeWalker(b,NodeFilter.SHOW_TEXT);let n;
   while(n=w.nextNode()){let pe=n.parentElement;let own=pe;while(own!==b&&getComputedStyle(own).display=='inline')own=own.parentElement;if(own!==b)continue;
     for(let k=0;k<n.textContent.length;k++){const ch=n.textContent[k];if(!ch.trim())continue;const rg=document.createRange();rg.setStart(n,k);rg.setEnd(n,k+1);const rr=rg.getClientRects()[0];if(!rr)continue;
       let L=lines.find(l=>Math.abs(l.y-rr.top)<rr.height*0.5);if(!L){L={y:rr.top,s:[]};lines.push(L)}L.s.push([rr.left,ch]);}}
   lines.sort((a,c)=>a.y-c.y);if(lines.length<2)continue;
   lines.forEach((l,idx)=>{l.s.sort((a,c)=>a[0]-c[0]);const t=l.s.map(x=>x[1]).join('');
     if(idx>0&&P.includes(t[0]))R.push('LINESTART_PUNCT '+t.slice(0,12));
     if(idx==lines.length-1&&t.replace(/[，。、；：？！）%]/g,'').length<=1)R.push('ORPHAN '+t+' in '+b.textContent.slice(0,12));});
   R.push('LINES '+lines.length+' '+b.className+' '+b.textContent.slice(0,14));}
 const t=document.querySelector('.title');if(t&&document.querySelector('.cover')){const fs=getComputedStyle(t).fontSize;
   [...t.querySelectorAll('.ln')].forEach(l=>{const r=l.getBoundingClientRect();R.push('TITLE '+fs+' line w='+r.width.toFixed(0)+' '+(r.width/928*100).toFixed(1)+'% top='+r.top.toFixed(0)+' bottom='+r.bottom.toFixed(0))});}
 document.querySelectorAll('.bar').forEach(i=>R.push('BAR '+(i.getBoundingClientRect().width/i.parentElement.getBoundingClientRect().width*100).toFixed(1)));
 const pre=document.createElement('pre');pre.id='RES';pre.textContent=R.join('\n');document.body.appendChild(pre);
});});
