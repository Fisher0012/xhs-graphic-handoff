from pathlib import Path
import json,hashlib
from PIL import Image
P=Path(__file__).resolve().parents[1];F=P/'final'
a=json.loads((F/'06_归档校验.json').read_text());n=0
for e in a['files']:
 p=Path(e['path']);assert p.stat().st_size==e['bytes'];assert hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256'];n+=1
for i,name in enumerate(['00_封面.png','01_国内销量与出口.png','02_新能源出口占比.png','03_出口退税节点.png'],1):
 assert Image.open(F/name).size==(2160,2880)
 assert (P/'03-design'/f'p{i}.png').read_bytes()==(F/name).read_bytes()
d=json.loads((P/'data.json').read_text());facts={x['id']:x['value'] for x in d['facts']}
assert round(facts['oct_nev_export']/facts['oct_export']*100,1)==56.8
assert round(facts['ytd_nev_export']/facts['ytd_export']*100,1)==49.7
assert facts['oct_domestic']+facts['oct_export']==facts['oct_total_sales']
assert all(x['url'] and '2026-11-13' in x['accessed'] for x in d['facts']+d['author_calc'])
assert d['cover_mode']=='中汽协总量；未采用企业排名'
print(f'verify_artifacts: PASS；{n}项字节/哈希匹配；4张2160×2880成品与渲染一致；占比公式和来源元数据均通过')
