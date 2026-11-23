from pathlib import Path
from datetime import datetime
import hashlib,json,re,shutil,csv,tarfile,zipfile,subprocess,collections
ROOT=Path('/workspace/xhs'); OUT=ROOT/'handoff/20261123'; PAY=OUT/'payload'; DOC=OUT/'docs'; DOC.mkdir(parents=True,exist_ok=True)
STAMP=datetime.now().astimezone().isoformat()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def tsv(p,rows,fields):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter='\t');w.writeheader();w.writerows(rows)
# Strictly project-scoped snapshots. No git directories or login stores are traversed.
sources=[(ROOT,'project'),(Path('/workspace/review/xhs'),'external/review/xhs'),(Path('/workspace/ops/dido/pstack_xhs'),'external/ops/dido/pstack_xhs'),(Path('/workspace/ops/comm/materials/pstack_xhs_start_20261122'),'external/ops/comm/materials/pstack_xhs_start_20261122'),(Path('/workspace/ops/comm/inbox/xhs 图文创作'),'external/ops/comm/inbox/xhs 图文创作'),(Path('/workspace/ops/xhs-tuwen/STATE.md'),'external/ops/xhs-tuwen/STATE.md'),(Path('/workspace/ops/tasks/xhs 图文创作.json'),'external/ops/tasks/xhs 图文创作.json')]
for name in ['verify_receipt.py','receipt.schema.json','baseline.sh','PROJECT_CHECKS.md']:
 sources.append((Path('/workspace/ops/eng_gate')/name,'external/ops/eng_gate/'+name))
for name in ['NotoSansSC-Black.otf','NotoSansSC-Medium.otf']:
 sources.append((Path('/home/box/.fonts')/name,'dependencies/fonts/'+name))
sources.append((Path('/usr/share/doc/fonts-noto-cjk/copyright'),'dependencies/fonts/OFL-and-copyright.txt'))
# Include the actual operational reference documents, never a whole plugin/account directory.
plugin=Path('/home/box/agent-data/plugins/pstack/pstack/skills/poteto-mode')
if not plugin.exists():
 plugin=Path('/home/box/agent-data/plugins/cache/cursor-public/pstack/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/skills/poteto-mode')
if plugin.exists():
 for f in plugin.rglob('*'):
  if f.is_file() and f.suffix.lower()=='.md':sources.append((f,'reference/poteto-mode/'+str(f.relative_to(plugin))))
patterns={
 'private-key':re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
 'github-pat':re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})\b'),
 'aws-access-key':re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
 'slack-token':re.compile(r'\bxox[baprs]-[A-Za-z0-9-]{20,}'),
 'google-api-key':re.compile(r'\bAIza[A-Za-z0-9_-]{30,}'),
 'live-sk-key':re.compile(r'\bsk-(?:proj-)?[A-Za-z0-9_-]{35,}'),
 'jwt':re.compile(r'\beyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}'),
 'hardcoded-secret':re.compile(r'''(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password|authorization)\s*[=:]\s*["'](?:Bearer\s+)?([A-Za-z0-9_./+=-]{20,})["']''')
}
text_ext={'.md','.txt','.json','.jsonl','.html','.htm','.py','.js','.ts','.tsx','.css','.sh','.log','.yml','.yaml','.toml','.csv','.tsv','.env','.xml','.mjs','.cjs'}
findings=[];exclusions=[];rows=[];archive_rows=[];text_count=0;archive_count=0;missing=[]
def scan_text(data,label):
 global text_count
 try:s=data.decode('utf-8')
 except UnicodeDecodeError:return False
 text_count+=1
 for typ,pat in patterns.items():
  for m in pat.finditer(s):findings.append({'path':label,'type':typ,'line':s.count('\n',0,m.start())+1})
 return True
def sensitive_name(p):
 parts=p.parts
 return any(x in {'.git','node_modules','__pycache__','.cache','browser-profile','user-data','Default'} for x in parts) or p.name.lower() in {'.env','.env.local','.env.production','cookies.txt','cookies.json','credentials.json','id_rsa','id_ed25519','local state','login data','web data'} or p.suffix.lower() in {'.pem','.key','.p12','.pfx'}
def classify(p,n):
 if n>=100*1024*1024:return 'LFS_REQUIRED_GT100MiB'
 if p.suffix.lower() in {'.mp4','.mov','.mkv','.webm','.mp3','.wav'} or n>=50*1024*1024:return 'LFS_RECOMMENDED'
 return 'GIT_CANDIDATE'
for base,dstbase in sources:
 if not base.exists():missing.append(str(base));continue
 files=sorted(base.rglob('*')) if base.is_dir() else [base]
 for f in files:
  if f.is_dir():continue
  if base==ROOT and ('handoff' in f.relative_to(ROOT).parts):continue
  rel=Path(dstbase)/(f.relative_to(base) if base.is_dir() else '')
  if f.is_symlink():exclusions.append({'source':str(f),'reason':'symlink-not-followed'});continue
  if sensitive_name(f):exclusions.append({'source':str(f),'reason':'credential-name-or-runtime-cache-not-read'});continue
  n=f.stat().st_size;digest=sha(f);label=str(rel);before=len(findings)
  if f.suffix.lower() in text_ext or f.name in {'SHA256SUMS','LICENSE','MANIFEST.sha256'}:
   if n<=20*1024*1024:scan_text(f.read_bytes(),label)
   else:findings.append({'path':label,'type':'text-too-large-unscanned','line':0})
  # Inspect archives without extracting or executing anything. Preserve archives as history.
  try:
   if f.suffix.lower() in {'.tgz','.tar','.gz'} and tarfile.is_tarfile(f):
    with tarfile.open(f) as tf:
     for m in tf:
      if not m.isfile():continue
      member=Path(m.name);archive_rows.append({'archive':label,'member':m.name,'bytes':m.size,'kind':'tar'})
      if member.is_absolute() or '..' in member.parts or sensitive_name(member):findings.append({'path':label+'!'+m.name,'type':'archive-risk-name-or-path','line':0});continue
      if member.suffix.lower() in text_ext and m.size<=20*1024*1024:
       q=tf.extractfile(m)
       if q:scan_text(q.read(),label+'!'+m.name);archive_count+=1
   elif f.suffix.lower()=='.zip':
    with zipfile.ZipFile(f) as z:
     for m in z.infolist():
      if m.is_dir():continue
      member=Path(m.filename);archive_rows.append({'archive':label,'member':m.filename,'bytes':m.file_size,'kind':'zip'})
      if member.is_absolute() or '..' in member.parts or sensitive_name(member):findings.append({'path':label+'!'+m.filename,'type':'archive-risk-name-or-path','line':0});continue
      if member.suffix.lower() in text_ext and m.file_size<=20*1024*1024:scan_text(z.read(m),label+'!'+m.filename);archive_count+=1
  except (tarfile.TarError,zipfile.BadZipFile,OSError) as e:findings.append({'path':label,'type':'archive-inspection-error-'+type(e).__name__,'line':0})
  status='HOLD_SECURITY_REVIEW' if len(findings)>before else classify(f,n)
  row={'path':label,'bytes':n,'sha256':digest,'upload_class':status,'original':str(f)};rows.append(row)
  if status!='HOLD_SECURITY_REVIEW':
   target=PAY/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,target)
# Save raw read-only remote evidence from this run, not authentication or connector/session state.
for src,name in [('/cursor/stores/user/grok-bot/agents/3b016c37-b662-41ce-8f90-60e32fbf1650/assets/01M845NP7EYPQ5225D24ZA6B2N.txt','remote-tree-main.txt'),('/cursor/stores/user/grok-bot/agents/3b016c37-b662-41ce-8f90-60e32fbf1650/assets/01M845P4RFJVE3HXAE4PPT3BBC.txt','remote-README-before.txt'),('/cursor/stores/user/grok-bot/agents/3b016c37-b662-41ce-8f90-60e32fbf1650/assets/01M845NBBF77ZF27GY31FFNW7M.txt','remote-repository-metadata.txt')]:
 p=Path(src)
 if p.exists():target=OUT/'evidence'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
 else:missing.append(src)
tsv(OUT/'UPLOAD_MANIFEST.tsv',rows,['path','bytes','sha256','upload_class','original'])
tsv(OUT/'ARCHIVE_CONTENTS.tsv',archive_rows,['archive','member','bytes','kind'])
write(OUT/'SECURITY_FINDINGS.json',json.dumps({'scan_time_Asia_Shanghai':STAMP,'rules':list(patterns),'findings':findings,'excluded_without_reading':exclusions,'text_files_and_archive_members_scanned':text_count,'archive_text_members_scanned':archive_count,'limits':['No account/credential directories read.','Images, videos, PDF and audio not visually/OCR reviewed for secrets.','No entropy-based, paid-service or exhaustive malware scan.','Nested archives not recursively expanded.','Remote existing historical ZIP is not downloaded or re-scanned.'],'missing':missing},ensure_ascii=False,indent=2))
summary={'timestamp_Asia_Shanghai':STAMP,'source_count':len(rows),'source_bytes':sum(r['bytes'] for r in rows),'candidate_count':sum(r['upload_class']!='HOLD_SECURITY_REVIEW' for r in rows),'candidate_bytes':sum(r['bytes'] for r in rows if r['upload_class']!='HOLD_SECURITY_REVIEW'),'security_hold_files':[r['path'] for r in rows if r['upload_class']=='HOLD_SECURITY_REVIEW'],'excluded':exclusions,'missing':missing,'classes':dict(collections.Counter(r['upload_class'] for r in rows))}
write(OUT/'INVENTORY_SUMMARY.json',json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps(summary,ensure_ascii=False,indent=2));print('SECURITY_FINDINGS',len(findings))
# Historical index enumerates real assets; directory names and receipts do not imply user acceptance.
idx=['# 历史内容实体索引','',f'快照时刻：{STAMP}（Asia/Shanghai）。以下仅证明文件存在，不证明用户批准、发布或Mac传输。','', '|相对目录|文件数|字节|实际候选交付目录|','|---|---:|---:|---|']
for section in ['notes','archive','商单','gushouplus','topics','xiaohao_ref']:
 p=ROOT/section
 for d in sorted(p.iterdir()):
  if not d.is_dir():continue
  fs=[f for f in d.rglob('*') if f.is_file()]
  delivered=[str(a.relative_to(ROOT)) for a in d.rglob('*') if a.is_dir() and (a.name.startswith('final') or a.name in {'定稿','v7'})]
  idx.append('|'+f'{section}/{d.name}|{len(fs)}|{sum(f.stat().st_size for f in fs)}|'+('<br>'.join(delivered) if delivered else '待按本目录文件判断')+'|')
write(DOC/'05-历史实体索引.md','\n'.join(idx)+'\n')
# Check source and copy equality, do not alter originals.
checked=0;bad=[]
for r in rows:
 if r['upload_class']=='HOLD_SECURITY_REVIEW':continue
 p=PAY/r['path']
 if not p.exists() or sha(p)!=r['sha256']:bad.append(r['path'])
 checked+=1
write(OUT/'SNAPSHOT_VERIFICATION.json',json.dumps({'snapshot_time':STAMP,'files_compared':checked,'sha256_mismatches':bad,'note':'Only the copied local snapshot was verified; GitHub is unchanged and no user design approval implied.'},ensure_ascii=False,indent=2))
print('LOCAL_SNAPSHOT_SHA_CHECKED',checked,'MISMATCHES',len(bad))
