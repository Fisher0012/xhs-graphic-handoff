import json,re,html,subprocess,sys
from pathlib import Path
from PIL import Image
d=Path('.');js=(d/'measure.js').read_text();ok=True
for n in ['01','02']:
    src=(d/f'{n}_内页.html').read_text();(d/f'.{n}_qa.html').write_text(src.replace('</body>',js+'</body>'))
    dom=subprocess.run(['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--allow-file-access-from-files','--window-size=1080,1440','--virtual-time-budget=5000','--dump-dom',f'file://{d.resolve()}/.{n}_qa.html'],capture_output=True,text=True).stdout
    q=json.loads(html.unescape(re.search(r'<pre id="qa">(.*?)</pre>',dom,re.S).group(1)))
    Image.open(d/f'{n}_内页.png').resize((400,533),Image.Resampling.LANCZOS).save(d/f'{n}_内页_400.png')
    q['png_size']=Image.open(d/f'{n}_内页.png').size
    issues=[]
    for c in q['cells']:
        if c['cls'] in('info','tx','person') and c['lines']!=2: issues.append(('not 2 lines',c['text']))
        if c['lines']>2: issues.append(('>2 lines',c['text']))
        for l in c['text']:
            if l['text'][:1] in '，。；、：）': issues.append(('leading punct',l['text']))
    if q['overflows']: issues.append(('overflow',q['overflows']))
    if q['bottom_gap']<24 or q['bottom_gap']>80: issues.append(('bottom gap',q['bottom_gap']))
    if q['min_body_font_excl_labels_footer']<20: issues.append(('small font',q['min_body_font_excl_labels_footer']))
    q['issues']=issues;q['pass']=not issues;ok&=not issues
    (d/f'{n}_排版检查.json').write_text(json.dumps(q,ensure_ascii=False,indent=2))
    print(n,q['title_font'],[t['text'] for t in q['title_lines']],'gap',q['subtitle_gap'],'bottom_gap',q['bottom_gap'],'minfont',q['min_body_font_excl_labels_footer'],'size',q['png_size'])
    for c in q['cells']:print('  ',c['cls'],c['lines'],' | '.join(f"{l['text']}({l['right']})" for l in c['text']))
    print('  issues',issues)
sys.exit(0 if ok else 1)
