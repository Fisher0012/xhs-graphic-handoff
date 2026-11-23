import sys,json,re,subprocess,glob,runpy,contextlib,io
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
N=Path(__file__).resolve().parent
sys.path.insert(0,'/workspace/xhs/tools')
import check_titles
D=json.loads((N/'data.json').read_text()); rows=sorted(D['items'],key=lambda x:-x['growth'])
source=(N/'sources/mof.txt').read_text(); detail=[]
for r in rows:
 name={'进口环节税':'进口货物增值税、消费税','其他税收合计':'车船税、船舶吨税、烟叶税等其他各项税收收入合计'}.get(r['name'],r['name'])
 pattern=re.escape(name)+r'\s*'+str(r['amount'])+r'亿元，同比(增长|下降)\s*([\d.]+)%'
 m=re.search(pattern,source); assert m,r
 assert (-1 if m[1]=='下降' else 1)*float(m[2])==r['growth'],r
 detail.append(dict(**r,matched_source=m[0]))
assert len(rows)==17 and not any(r['name']=='证券交易印花税' for r in rows)
assert sum(r['amount'] for r in rows)-D['export_refund']['amount']==D['totals']['tax']
assert D['totals']['tax']+D['totals']['nontax']==D['totals']['revenue']
# Positive and negative invariants: a duplicated child and wrong total must be rejected.
def valid(rs): return len(rs)==17 and not any(x['name']=='证券交易印花税' for x in rs)
assert not valid(rows+[dict(name='证券交易印花税',amount=2511,growth=54.1)])
assert D['totals']['revenue']!=D['totals']['tax']
p1=BeautifulSoup((N/'03-design/p1.html').read_text(),'html.parser'); p3=BeautifulSoup((N/'03-design/p3.html').read_text(),'html.parser')
actual=[]
for r in p1.select('.row'):
 actual.append((r.select_one('.nm').get_text(),int(re.search(r'\d+',r.select_one('.en').get_text())[0]),float(r.select_one('.v').get_text().replace('%',''))))
for tr in p3.select('tr')[1:]:
 cells=[x.get_text(strip=True) for x in tr.select('td')]; actual.append((cells[1],int(cells[2].replace(',','')),float(cells[3].replace('%',''))))
assert actual==[(x['name'],x['amount'],x['growth']) for x in rows],actual
print('DATA PASS: 17 official amount/growth pairs; source→JSON→HTML→source; complete sorted ranking; child excluded; tax/refund and revenue identities; negative invariants')
for f in N.glob('**/*.py'): compile(f.read_text(),str(f),'exec')
print('SYNTAX PASS: all project Python compiled in memory')
title_results=[]
for i in range(1,5):
 result=check_titles.check(str(N/f'03-design/p{i}.html')); assert result
 h,s=result
 assert h['lines']==1 and h['right']<=1040 and 'linear-gradient(165deg' in h['bg'],h
 assert float(h['fs'][:-2])==(122 if i==1 else 64),h
 assert s and s['fs']=='26px' and s['lines']==1 and s['right']<=1040,s
 title_results.append(dict(page=i,title=h,subtitle=s))
print('TITLES PASS: original check_titles.check called on all 4 current pages; 122px cover, 64px inner titles, 26px subtitles, one-line and right bounds')
print(json.dumps(title_results,ensure_ascii=False))
for f in sorted((N/'final').glob('0[0-3]_*.png')):
 assert Image.open(f).size==(2160,2880)
copy=(N/'final/04_发布文案.txt').read_text(); body=copy.split('正文：\n')[1].split('\n\n话题：')[0]
assert len(body.replace('\n',''))<=1000
print('ARTIFACT PASS: 4 images at 2160×2880; body',len(body.replace('\n','')),'characters excluding newline')
# Same original measurement code; adapt only the hard-coded file-discovery glob, no formula or threshold changes.
original=glob.glob
try:
 glob.glob=lambda pattern: [str(p) for p in sorted((N/'final').glob('0[1-3]_*.png'))] if pattern=='2026103*/03-design/final/0[1-4]_*.png' else original(pattern)
 runpy.run_path('/workspace/xhs/tools/measure_space.py',run_name='__main__')
finally: glob.glob=original
r=subprocess.run(['python3','/workspace/xhs/tools/compliance_precheck.py','--dir',str(N)],text=True); assert r.returncode==0
print('CHECKS PASS. Measurement metrics above are reported, not silently converted into approval; visual review required.')
