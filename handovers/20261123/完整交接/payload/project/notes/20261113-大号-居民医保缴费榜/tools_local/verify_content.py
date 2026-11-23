from pathlib import Path
import json,hashlib,sys
from PIL import Image
D=Path(__file__).resolve().parents[1]
def validate(data):
 assert len(data['cities'])==8
 assert len({x['city'] for x in data['cities']})==8
 src={s['id']:s for s in data['sources']}
 for v in src.values(): assert v['published'] <= data['date']
 assert [x['personal'] for x in data['cities']]==sorted((x['personal'] for x in data['cities']),reverse=True)
 for x in data['cities']:
  assert x['source'] in src
  p=D/src[x['source']]['file'];assert p.exists() and p.stat().st_size>500
  assert '2026-11-13' in src[x['source']]['accessed']
 assert data['national']['total_example']['value']==400+724
 assert data['cities'][1]['personal']==596
 return True
data=json.loads((D/'data.json').read_text());assert validate(data)
# 反例：无来源的城市数据必须被拒，不将反例写入成稿。
import copy
negative=copy.deepcopy(data);negative['cities'][0]['source']='MISSING'
try:validate(negative)
except AssertionError:print('negative missing-source: PASS (rejected)')
else:raise AssertionError('missing source unexpectedly accepted')
for p in (D/'final').glob('0[0-4]_*.png'):
 assert Image.open(p).size==(2160,2880)
a=json.loads((D/'final/07_归档校验.json').read_text())
for x in a['files']:
 p=D/'final'/x['name'];assert p.stat().st_size==x['bytes'];assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
print('sources, count, dates, calculations, dimensions, hashes: PASS')
