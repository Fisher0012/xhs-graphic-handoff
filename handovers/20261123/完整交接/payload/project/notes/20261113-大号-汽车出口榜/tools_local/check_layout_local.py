from pathlib import Path
import re,subprocess,json,sys
D=Path(__file__).resolve().parents[1]/'03-design'
JS='''<script>window.addEventListener('load',()=>document.fonts.ready.then(()=>{let bad=[];document.querySelectorAll('.card').forEach(e=>{if(e.scrollHeight>e.clientHeight+1)bad.push('card vertical clipping');if(e.scrollWidth>e.clientWidth+1)bad.push('card horizontal clipping')});let foot=document.querySelector('.foot').getBoundingClientRect();let content=document.querySelector('.content,.covercontent').getBoundingClientRect();if(content.bottom>foot.top)bad.push('footer overlaps content');let gap=foot.top-content.bottom;if(gap>1440*.06)bad.push('footer gap >6%');if(foot.bottom>1440)bad.push('footer cut');let o=document.createElement('pre');o.id='LAYOUT_RESULT';o.textContent=JSON.stringify({bad,gap});document.body.appendChild(o)}))</script>'''
bad=0
for i in range(1,5):
 p=D/f'p{i}.html';tmp=D/f'layout_check_{i}.html';tmp.write_text(p.read_text().replace('</body>',JS+'</body>'))
 try:
  r=subprocess.run(['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--allow-file-access-from-files','--window-size=1080,1440','--virtual-time-budget=3000','--dump-dom','file://'+str(tmp)],capture_output=True,text=True,check=True)
  m=re.search(r'<pre id="LAYOUT_RESULT">(.*?)</pre>',r.stdout,re.S);x=json.loads(m.group(1));bad+=bool(x['bad']);print(f'p{i} '+json.dumps(x,ensure_ascii=False))
 finally:tmp.unlink(missing_ok=True)
print('check_layout:', 'PASS' if not bad else 'FAIL');sys.exit(bool(bad))
