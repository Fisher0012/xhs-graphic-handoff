# 从渲染用HTML抽出标题实际样式：用headless Chrome计算 computed style 与行数
import sys,glob,os,re,subprocess,json,tempfile
JS='''<script>window.addEventListener('load',()=>{document.fonts.ready.then(()=>{const o=[];
for(const sel of ['h1','.hsub, .sub']){const e=document.querySelector(sel);if(!e){o.push(null);continue}
const s=getComputedStyle(e);const r=document.createRange();r.selectNodeContents(e);const rects=[...r.getClientRects()];
const tops=new Set(rects.map(x=>Math.round(x.top)));const R=e.getBoundingClientRect();
const right=Math.max(...rects.map(x=>x.right));
o.push({fs:s.fontSize,ff:s.fontFamily,ls:s.letterSpacing,color:s.color,bg:s.backgroundImage.slice(0,90),lines:tops.size,top:Math.round(R.top),right:Math.round(right),text:e.innerText.replace(/\\n/g,'⏎')})}
const d=document.createElement('pre');d.id='OUT';d.textContent=JSON.stringify(o);document.body.appendChild(d);})})</script>'''
def check(html):
    src=open(html).read().replace('</body>',JS+'</body>')
    t=html+'.chk.html';open(t,'w').write(src)
    out=subprocess.run(['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--allow-file-access-from-files','--window-size=1080,1440','--virtual-time-budget=4000','--dump-dom','file://'+t],capture_output=True,text=True).stdout
    os.remove(t);m=re.search(r'<pre id="OUT">(.*?)</pre>',out,re.S)
    return json.loads(m.group(1).replace('&amp;','&').replace('&lt;','<').replace('&gt;','>')) if m else None
if __name__=='__main__':
    rows=[]
    for d in sorted(glob.glob('/workspace/xhs/notes/20261031-*/03-design')):
        for i in range(1,7):
            r=check(f'{d}/p{i}.html');h,s=r[0],r[1]
            name=d.split('/')[-2].replace('20261031-','')
            rows.append((name,f'{i-1:02d}',h['fs'],h['ls'],h['bg'][:40] if h['bg']!='none' else h['color'],h['lines'],h['right'],h['text'],s and s['fs'],s and s['color'],s and s['lines'],s and s['top']))
    for r in rows: print('\t'.join(map(str,r)))
