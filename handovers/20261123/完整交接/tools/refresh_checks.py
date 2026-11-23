from pathlib import Path
import csv,json,hashlib,re,shutil,collections
from datetime import datetime
O=Path('/workspace/xhs/handoff/20261123');P=O/'payload'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4194304),b''):h.update(b)
 return h.hexdigest()
def wt(p,rows,fields):
 with p.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fields,delimiter='\t');w.writeheader();w.writerows(rows)
M=list(csv.DictReader((O/'UPLOAD_MANIFEST.tsv').open(),delimiter='\t'));known={r['path'] for r in M}
cache=Path('/home/box/agent-data/plugins/cache/cursor-public/pstack/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/skills/poteto-mode')
for f in sorted(cache.rglob('*.md')):
 rel='reference/poteto-mode/'+str(f.relative_to(cache));target=P/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,target)
 if rel not in known:M.append({'path':rel,'bytes':f.stat().st_size,'sha256':sha(f),'upload_class':'GIT_CANDIDATE','original':str(f)});known.add(rel)
wt(O/'UPLOAD_MANIFEST.tsv',M,['path','bytes','sha256','upload_class','original'])
for p in [O/'README.md',O/'docs/08-安全范围与完整性说明.md']:
 text=p.read_text().replace('3017','3042').replace('3014','3039').replace('1671份','1696份');p.write_text(text)
p=O/'docs/04-规则模板与机制.md';text=p.read_text().replace('本轮确已读到逻辑目录的worker.md，不能照搬旧路径状态为当前事实。实际已复制reference/poteto-mode参考文档，未改共享技能。','本轮Read工具能读逻辑目录worker.md，Shell实查逻辑目录仍不存在；实际文件来自PSTACK已记录的cache路径7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9。已将该cache的25份Markdown实体复制到reference/poteto-mode，含worker与playbooks；未改共享技能。参考文档不扩张用户授权。');p.write_text(text)
# Preserve the known fallback in the archival preparation helper too.
p=O/'tools/prepare_handoff.py';text=p.read_text().replace("if plugin.exists():\n for f in plugin.rglob('*'):","if not plugin.exists():\n plugin=Path('/home/box/agent-data/plugins/cache/cursor-public/pstack/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/skills/poteto-mode')\nif plugin.exists():\n for f in plugin.rglob('*'):");p.write_text(text)
(O/'STATE.md').write_text('更新: '+datetime.now().astimezone().isoformat()+' Asia/Shanghai\n状态: BLOCKED（本地实体交接备妥；GitHub未更新，留主助手正式CloudAgent继续）\n下一项: 主助手搬运实体、处理LFS后增量PR并远端回读SHA；本线程不制作、不发布、不传Mac\n')
# Verify actual payload files, then post-redaction patterns and local entry links.
bad=[r['path'] for r in M if not (P/r['path']).exists() or sha(P/r['path'])!=r['sha256']]
patterns=[re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})\b'),re.compile(r'\beyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}'),re.compile(r'''(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password|authorization)\s*[=:]\s*["'](?:Bearer\s+)?[A-Za-z0-9_./+=-]{20,}["']''')]
hits=[]
for p in O.rglob('*'):
 if p.is_file() and '__pycache__' not in p.parts and p.suffix in {'.md','.txt','.json','.html','.py','.js','.sh','.tsv','.csv','.log','.yml','.yaml','.toml'} and p.stat().st_size<=20*1024*1024:
  try:s=p.read_text()
  except UnicodeError:continue
  if any(q.search(s) for q in patterns):hits.append(str(p.relative_to(O)))
links=[]
for p in [O/'README.md',*sorted((O/'docs').glob('*.md'))]:
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' not in link and not link.startswith('#') and not (p.parent/link).exists():links.append({'file':str(p.relative_to(O)),'target':link})
V=json.loads((O/'SNAPSHOT_VERIFICATION.json').read_text());V.update({'verified_Asia_Shanghai':datetime.now().astimezone().isoformat(),'payload_files_verified':len(M),'sha256_mismatches':bad,'unmodified_source_copies':len(M)-3,'sanitized_source_copies':3});(O/'SNAPSHOT_VERIFICATION.json').write_text(json.dumps(V,ensure_ascii=False,indent=2))
S=json.loads((O/'INVENTORY_SUMMARY.json').read_text());S.update({'source_count':len(M),'source_bytes':sum(int(r['bytes']) for r in M)+3455,'candidate_count':len(M),'candidate_bytes':sum(int(r['bytes']) for r in M),'classes':dict(collections.Counter(r['upload_class'] for r in M)),'finalized_Asia_Shanghai':datetime.now().astimezone().isoformat(),'poteto_reference_markdown_files':25});(O/'INVENTORY_SUMMARY.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
sec=json.loads((O/'SECURITY_FINDINGS.json').read_text());sec['text_files_and_archive_members_scanned']=1696;sec['added_reference_files']=25;(O/'SECURITY_FINDINGS.json').write_text(json.dumps(sec,ensure_ascii=False,indent=2))
classes=collections.defaultdict(lambda:{'files':0,'bytes':0})
for r in M:classes[r['upload_class']]['files']+=1;classes[r['upload_class']]['bytes']+=int(r['bytes'])
report={'verified_Asia_Shanghai':datetime.now().astimezone().isoformat(),'payload_files':len(M),'payload_bytes':S['candidate_bytes'],'classes':dict(classes),'sanitized_files':3,'unmodified_source_copies':len(M)-3,'sha256_mismatches':bad,'burry_final_sha_items_verified':len(V['burry_existing_final_sha_items']),'internal_markdown_broken_links':links,'post_redaction_pat_jwt_hardcoded_secret_pattern_hits':hits,'scope':'Local copy/archive checks only; no remote write, user approval, rights clearance, full media inspection or clean-OS rerender.'}
(O/'FINAL_LOCAL_CHECK.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
files=sorted(p for p in O.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in {'SHA256SUMS','TRANSFER_MANIFEST.tsv'})
mr={r['path']:r for r in M}
with (O/'TRANSFER_MANIFEST.tsv').open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f,delimiter='\t');w.writerow(['relative_path','bytes','sha256','upload_class'])
 for p in files:
  rel=str(p.relative_to(O));w.writerow([rel,p.stat().st_size,sha(p),mr.get(rel.removeprefix('payload/'),{}).get('upload_class','GIT_CANDIDATE_HANDOFF_DOCUMENT')])
files.append(O/'TRANSFER_MANIFEST.tsv');files.sort()
(O/'SHA256SUMS').write_text(''.join(sha(p)+'  '+str(p.relative_to(O))+'\n' for p in files))
print(json.dumps(report,ensure_ascii=False,indent=2));print('FULL_TRANSFER_FILES',len(files)+1);print('FULL_TRANSFER_BYTES',sum(f.stat().st_size for f in files)+(O/'SHA256SUMS').stat().st_size);print('SHA256SUMS_DIGEST',sha(O/'SHA256SUMS'))
assert not bad and not links and not hits
