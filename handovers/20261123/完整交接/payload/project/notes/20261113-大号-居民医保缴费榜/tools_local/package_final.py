from pathlib import Path
from PIL import Image
from bs4 import BeautifulSoup
import json,hashlib,shutil,datetime
D=Path(__file__).resolve().parents[1]
names=['00_封面.png','01_个人缴费与财政补助.png','02_断保待遇等待期.png','03_连续参保激励.png','04_各地集中缴费截止日.png']
for i,n in enumerate(names,1):shutil.copy2(D/f'03-design/p{i}.png',D/'final'/n)
over=Image.new('RGB',(2160,576),(3,3,4))
for i,n in enumerate(names):
 im=Image.open(D/'final'/n).convert('RGB');im.thumbnail((432,576));over.paste(im,(i*432,0))
over.save(D/'final/08_全套总览.png')
frame=['# 五页框架（最终稿）\n\n8城成年居民所列档次样本，不含长护；不是全国全榜；同额并列。每页只讲一个信息点。']
for i,role in enumerate(['8城样本缴费榜','个人与财政筹资','待遇等待期','连续参保激励','集中参保与缴费截止日'],1):
 soup=BeautifulSoup((D/f'03-design/p{i}.html').read_text(),'html.parser')
 for e in soup(['script','style']):e.decompose()
 frame.append(f'## {i:02d} {role}\n呈现：'+('条形榜' if i==1 else '三组卡片')+'\n\n'+soup.body.get_text('｜',strip=True))
for n in ['02-框架.md','框架.md']:(D/n).write_text('\n\n'.join(frame)+'\n')
a=json.loads((D/'final/07_归档校验.json').read_text());a['files']=[dict(name=p.name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted((D/'final').iterdir()) if p.is_file() and p.name!='07_归档校验.json'];a['source_urls']=[s['url'] for s in json.loads((D/'data.json').read_text())['sources']];a['checks']['visual_read']='5/5 Read inspected; cover overlap fixed; cutoff-page dangling two-character line shortened; final sources use Foshan instead of Hangzhou repost';a['checks']['once_pipeline']='PASS (warn=0); 合规初筛 PASS; 定稿门禁 PASS'
(D/'final/07_归档校验.json').write_text(json.dumps(a,ensure_ascii=False,indent=2))
assets=[dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted((D/'final').iterdir()) if p.is_file()]
(D/'ASSET_REGISTER.json').write_text(json.dumps({'assets':assets},ensure_ascii=False,indent=2));(D/'MANIFEST.sha256').write_text('\n'.join(f"{x['sha256']}  {x['path']}" for x in assets)+'\n')
r=json.loads((D/'receipt.json').read_text());r['executed_at']=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat();r['targets']=[dict(path=x['path'],change='add',after_sha256=x['sha256']) for x in assets];(D/'receipt.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
print('package hashes refreshed: 9 files')
