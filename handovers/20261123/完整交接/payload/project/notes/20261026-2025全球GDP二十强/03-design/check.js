window.addEventListener('load',()=>{document.fonts.ready.then(()=>{
 const R=[];const vw=1080,vh=1440,mx=1080*0.06,my=1440*0.06;
 const leaf=[...document.querySelectorAll('.page *')].filter(e=>[...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim()));
 for(const e of leaf){const r=e.getBoundingClientRect();
   if(r.right>vw-mx+0.5||r.left<mx-0.5||r.bottom>vh-my||r.top<my) R.push('MARGIN '+e.className+' '+e.textContent.slice(0,15)+' '+[r.left,r.right,r.top,r.bottom].map(Math.round));
   if(e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).display!='inline') R.push('SCROLL '+e.className+' '+e.textContent.slice(0,15));}
 for(let i=0;i<leaf.length;i++)for(let j=i+1;j<leaf.length;j++){const a=leaf[i],b=leaf[j];if(a.contains(b)||b.contains(a))continue;
   const p=a.getBoundingClientRect(),q=b.getBoundingClientRect();
   if(p.left<q.right-1&&q.left<p.right-1&&p.top<q.bottom-6&&q.top<p.bottom-6)R.push('OVERLAP '+a.textContent.slice(0,10)+' | '+b.textContent.slice(0,10));}
 // 段落按行切分：孤字成行、行首标点
 const P='，。；：、）」】！？％,.;:)';
 document.querySelectorAll('li,.ht,p,.summary,.small,.src,.note,.tag,.lab,.sm,.subtitle,.risk').forEach(el=>{
   const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);const ch=[];let n;
   while(n=w.nextNode())for(let k=0;k<n.textContent.length;k++){const rg=document.createRange();rg.setStart(n,k);rg.setEnd(n,k+1);const rs=rg.getClientRects();if(rs.length)ch.push([n.textContent[k],rs[0].bottom])}
   const lines=[];for(const [c,t] of ch){if(!lines.length||Math.abs(t-lines[lines.length-1].t)>16)lines.push({t,s:''});lines[lines.length-1].s+=c}
   lines.forEach((l,i)=>{const s=l.s.trim();if(i>0&&P.includes(s[0]))R.push('PUNCT-START '+s.slice(0,8));if(lines.length>1&&s.replace(/[【】自算，。；]/g,'').length<=1)R.push('ORPHAN '+JSON.stringify(s))});
   if(lines.length>1)R.push('LINES '+el.className+': '+lines.map(l=>l.s.trim()).join(' / '));
 });
 // 字号
 const fs={};leaf.forEach(e=>{const s=parseFloat(getComputedStyle(e).fontSize);const k=e.className||e.tagName;fs[k]=Math.min(fs[k]||999,s)});
 R.push('FONTS '+Object.entries(fs).map(([k,v])=>k+':'+v).join(' '));
 document.querySelectorAll('.bar i').forEach(i=>{R.push('BAR '+(i.getBoundingClientRect().width/i.parentElement.getBoundingClientRect().width*100).toFixed(1))});
 const t=document.querySelector('.cover-title');if(t){const r=t.getBoundingClientRect();R.push('TITLEW '+r.width.toFixed(0)+' '+(r.width/948*100).toFixed(1)+'%')}
 const last=[...leaf].reduce((a,e)=>Math.max(a,e.getBoundingClientRect().bottom),0);R.push('LOWEST '+Math.round(last));
 const pre=document.createElement('pre');pre.id='RES';pre.textContent=R.join('\n');document.body.appendChild(pre);
});});
