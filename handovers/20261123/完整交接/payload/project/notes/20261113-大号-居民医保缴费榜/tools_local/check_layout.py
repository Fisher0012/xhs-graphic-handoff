import subprocess,json,re,html,sys
from pathlib import Path
D=Path(__file__).resolve().parents[1]/'03-design'
JS="""<script>document.fonts.ready.then(()=>setTimeout(()=>{let foot=document.querySelector('.foot').getBoundingClientRect(), kids=[...document.body.children].filter(e=>!e.matches('.foot,.pn,style,script')&&getComputedStyle(e).position!='absolute');let r=kids.map(e=>e.getBoundingClientRect());let bad=[];for(let i=1;i<r.length;i++){if(r[i].top<r[i-1].bottom-1)bad.push('block '+i+' overlaps previous')};let bottom=Math.max(...r.map(x=>x.bottom));if(foot.top-bottom<40)bad.push('footer gap '+(foot.top-bottom));for(let e of document.querySelectorAll('h1,.hsub,.sub,p,.lab,.nm,.en,.v')){let a=e.getBoundingClientRect();if(a.right>1080||a.left<0||e.scrollWidth>e.clientWidth+2)bad.push('overflow '+e.innerText)}let x=document.createElement('pre');x.id='LAYOUT';x.textContent=JSON.stringify({bad:bad,gap:foot.top-bottom,bottom:bottom});document.body.append(x)},150))</script>"""
bad=0
for i in range(1,6):
 p=D/f'p{i}.html';tmp=D/f'layout{i}.html';tmp.write_text(p.read_text().replace('</body>',JS+'</body>'))
 o=subprocess.run(['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--allow-file-access-from-files','--window-size=1080,1440','--virtual-time-budget=4000','--dump-dom',tmp.as_uri()],capture_output=True,text=True).stdout;tmp.unlink()
 m=re.search('<pre id="LAYOUT">(.*?)</pre>',o,re.S)
 if not m:print('p',i,'FAIL no result');bad+=1;continue
 a=json.loads(html.unescape(m.group(1)));ok=not a['bad'];bad+=not ok;print(f'p{i}: footer_gap={a["gap"]:.1f}px content_bottom={a["bottom"]:.1f}px '+('PASS' if ok else 'FAIL '+str(a['bad'])))
print('check_layout:', 'PASS' if not bad else 'FAIL');sys.exit(bool(bad))
