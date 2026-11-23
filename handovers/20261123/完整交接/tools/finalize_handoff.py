from pathlib import Path
from datetime import datetime
import csv,json,re,hashlib,collections
from PIL import Image
O=Path('/workspace/xhs/handoff/20261123');P=O/'payload'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4194304),b''):h.update(b)
 return h.hexdigest()
def wt(p,rows,fields):
 with p.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fields,delimiter='\t');w.writeheader();w.writerows(rows)
manifest=list(csv.DictReader((O/'UPLOAD_MANIFEST.tsv').open(),delimiter='\t'))
for row in manifest:row['bytes']=int(row['bytes'])
redacted=list(csv.DictReader((O/'SANITIZED_FILES.tsv').open(),delimiter='\t')) if (O/'SANITIZED_FILES.tsv').exists() else []
# Redact matching strings in derived archive copies; originals remain unchanged on box.
# No token values are printed, decoded or used for authentication.
patterns=[re.compile(r'\beyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}'),re.compile(r'''(?i)((?:api[_-]?key|access[_-]?token|client[_-]?secret|password|authorization)\s*[=:]\s*["'])(?:Bearer\s+)?[A-Za-z0-9_./+=-]{20,}(["'])''')]
for row in manifest:
 if row['upload_class']!='HOLD_SECURITY_REVIEW':continue
 src=Path(row['original']);s=src.read_text();n=0
 s,c=patterns[0].subn('[REDACTED_JWT_FOR_HANDOFF]',s);n+=c
 s,c=patterns[1].subn(lambda m:m.group(1)+'[REDACTED_SECRET_LIKE_VALUE_FOR_HANDOFF]'+m.group(2),s);n+=c
 if not n:raise RuntimeError('Unexpected unhandled security finding at '+row['path'])
 target=P/row['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_text(s)
 redacted.append({'path':row['path'],'original_sha256':row['sha256'],'upload_sha256':sha(target),'redactions':n,'original_bytes':row['bytes'],'upload_bytes':target.stat().st_size})
 row['sha256']=sha(target);row['bytes']=target.stat().st_size;row['upload_class']='GIT_CANDIDATE_SANITIZED'
wt(O/'UPLOAD_MANIFEST.tsv',manifest,['path','bytes','sha256','upload_class','original'])
wt(O/'SANITIZED_FILES.tsv',redacted,['path','original_sha256','upload_sha256','redactions','original_bytes','upload_bytes'])
wt(O/'LARGE_FILES.tsv',[r for r in manifest if r['bytes']>=20*1024*1024 or r['upload_class'].startswith('LFS')],['path','bytes','sha256','upload_class','original'])
s=json.loads((O/'INVENTORY_SUMMARY.json').read_text());s['raw_files_withheld_and_sanitized']=redacted;s['security_hold_files']=[];s['candidate_count']=len(manifest);s['candidate_bytes']=sum(r['bytes'] for r in manifest);s['classes']=dict(collections.Counter(r['upload_class'] for r in manifest));s['finalized_Asia_Shanghai']=datetime.now().astimezone().isoformat()
(O/'INVENTORY_SUMMARY.json').write_text(json.dumps(s,ensure_ascii=False,indent=2))
security=json.loads((O/'SECURITY_FINDINGS.json').read_text());security['disposition']='3 historical public-news HTML files contain JWT/API-key-like strings. Raw originals excluded; local archive derivatives redact the exact matched strings. No value decoded or used; no original altered. See SANITIZED_FILES.tsv.'
(O/'SECURITY_FINDINGS.json').write_text(json.dumps(security,ensure_ascii=False,indent=2))
# Verify Burry images and its existing seven-item delivery SHA file without rendering.
b=P/'project/notes/20261122-大号-Burry看空与减仓';checks=[]
for line in (b/'final/SHA256.txt').read_text().splitlines():
 if not line.strip():continue
 digest,name=line.split(maxsplit=1);name=name.lstrip('*');f=b/'final'/name
 checks.append({'file':name,'exists':f.exists(),'matches':f.exists() and sha(f)==digest})
dims={}
for f in (b/'final').glob('0[0-3]_*.png'):
 with Image.open(f) as im:dims[f.name]=list(im.size)
# Preserve original labels and write fresh checks under the handoff only.
bad=[]
for r in manifest:
 if sha(P/r['path'])!=r['sha256']:bad.append(r['path'])
verification={'verified_Asia_Shanghai':datetime.now().astimezone().isoformat(),'payload_files_verified':len(manifest),'sha256_mismatches':bad,'unmodified_source_copies':len(manifest)-len(redacted),'sanitized_source_copies':len(redacted),'burry_existing_final_sha_items':checks,'burry_four_dimensions':dims,'new_renderings':0,'remote_writes':0,'note':'Local copy/hash verification only; not user approval, media privacy clearance or completed GitHub update.'}
(O/'SNAPSHOT_VERIFICATION.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2))
# Static absolute dependency inventory. Do not read or follow external credentials/sessions.
refs=collections.defaultdict(set)
for f in (P/'project').rglob('*'):
 if f.is_file() and f.suffix in {'.html','.py','.sh','.js'} and f.stat().st_size<2000000:
  for m in re.finditer(r'''/(?:workspace|home/box|usr/share/fonts)/[^\s'"<>`;\)\}]+''',f.read_text(errors='replace')):
   path=m.group(0)
   if len(path)<500:refs[path].add(str(f.relative_to(P)))
rrows=[]
for target,referrers in sorted(refs.items()):
 if target.startswith('/workspace/xhs/'):
  mapped=P/'project'/target.removeprefix('/workspace/xhs/')
 elif target.startswith('/home/box/.fonts/'):
  mapped=P/'dependencies/fonts'/Path(target).name
 elif target.startswith('/workspace/'):
  mapped=P/'external'/target.removeprefix('/workspace/')
 else:mapped=None
 rrows.append({'literal_reference':target,'included_exact_path':str(mapped.relative_to(P)) if mapped and mapped.exists() else 'NOT_EXACTLY_MAPPED_OR_DYNAMIC_LITERAL','referrer_count':len(referrers),'referrers':' | '.join(sorted(referrers))})
wt(O/'ABSOLUTE_DEPENDENCIES.tsv',rrows,['literal_reference','included_exact_path','referrer_count','referrers'])
# Exclude newly made Python bytecode from transfer manifest (leave local run cache alone).
allfiles=sorted(f for f in O.rglob('*') if f.is_file() and f.name!='SHA256SUMS' and '__pycache__' not in f.parts)
lines=[sha(f)+'  '+str(f.relative_to(O)) for f in allfiles]
(O/'SHA256SUMS').write_text('\n'.join(lines)+'\n')
print(json.dumps({'payload_candidates':len(manifest),'payload_bytes':s['candidate_bytes'],'classes':s['classes'],'redacted_files':len(redacted),'four_png_dimensions':dims,'existing_final_sha_checks':checks,'mismatches':bad,'entire_handoff_files_except_bytecode_and_self':len(allfiles),'entire_handoff_bytes_except_bytecode_and_self':sum(f.stat().st_size for f in allfiles),'static_dependency_literals':len(rrows)},ensure_ascii=False,indent=2))
