from pathlib import Path
import subprocess,concurrent.futures,json
from bs4 import BeautifulSoup
P=Path(__file__).resolve().parents[1]
files=[P/'cover/00_封面.html',*sorted((P/'pages').glob('*.html'))]
def run(f):
 base=['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--allow-file-access-from-files','--hide-scrollbars','--window-size=1080,1440','--virtual-time-budget=3000']
 a=subprocess.run(base+['--force-device-scale-factor=2','--screenshot='+str(P/'final'/(f.stem+'.png')),'file://'+str(f)],capture_output=True,text=True,check=True)
 (P/'evidence'/(f.stem+'_render.log')).write_text(a.stderr)
 r=subprocess.run(base+['--dump-dom','file://'+str(f)],capture_output=True,text=True,check=True)
 (P/'evidence'/(f.stem+'_dom.html')).write_text(r.stdout)
 soup=BeautifulSoup(r.stdout,'html.parser');j=json.loads(soup.select_one('#layout-check').text)
 return f.stem,j
out=dict(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(run,files))
(P/'evidence/四图DOM检查.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
for n,j in out.items():print(n,'footerGap',j.get('footerGap'),'overflow',j.get('overflows'),'lineIssues',j.get('lineIssues'))
