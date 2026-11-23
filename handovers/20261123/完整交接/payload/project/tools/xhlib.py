# 小号墨绿统计类：通用生成库（20261101）
import os, shutil, subprocess, html
TPL='/workspace/xhs/notes/20261030-美股市值蒸发榜/03-design'
EXTRA='''
.it1{position:absolute;top:140px;font-size:76px;line-height:1.15}
.isub{position:absolute;top:248px;font-size:26px;color:var(--sub);white-space:nowrap}
.ibody{position:absolute;left:0;right:0;top:318px;bottom:150px;display:flex;flex-direction:column;justify-content:space-between}
.ibody > *{position:relative!important;top:auto!important}
.hd{font-size:40px;font-weight:700;display:flex;align-items:center;white-space:nowrap}
.hd i{display:inline-block;width:8px;height:36px;border-radius:4px;background:var(--teal);margin-right:18px}
.hd span{font-size:24px;color:var(--note);font-weight:400;margin-left:16px}
.hr2{display:flex;align-items:flex-end;padding:10px 0 14px;position:relative}
.hr2 .n{font-size:34px;font-weight:700;white-space:nowrap}
.hr2 .s{font-size:22px;color:var(--note);margin-left:14px;white-space:nowrap;padding-bottom:4px}
.hr2 .v{margin-left:auto;font-family:"Noto Sans SC";font-weight:900;font-size:42px;white-space:nowrap;line-height:1}
.hr2 .v small{font-size:22px;color:var(--note);font-weight:500;margin-left:4px}
.hr2 .b{position:absolute;left:0;right:0;bottom:0;height:8px;border-radius:4px;background:var(--track)}
.hr2 .b i{display:block;height:100%;border-radius:4px;background:linear-gradient(90deg,#3fd9bb,var(--teal) 60%,#15806d)}
.hr2.neg .v{color:var(--negnum)} .hr2.neg .b i{background:#4a5256}
.hr2.hi .v{color:var(--teal-hi)}
.kg{display:grid;gap:22px}
.kc{background:var(--card);border:1px solid var(--card-bd);border-radius:16px;padding:24px 26px;position:relative;overflow:hidden}
.kc:before{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;background:var(--teal)}
.kc .k{font-family:"Noto Sans SC";font-weight:900;font-size:56px;line-height:1.1;white-space:nowrap}
.kc .k small{font-size:26px;font-weight:700;margin-left:4px}
.kc .l{font-size:25px;color:var(--sub);margin-top:8px;white-space:nowrap}
.co{background:var(--card);border:1px solid var(--card-bd);border-radius:16px;padding:24px 28px 24px 34px;overflow:hidden}
.co:before{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;background:var(--teal)}
.co p{font-size:32px;line-height:1.5;color:#dde2e4}
.co b{color:var(--teal-hi)}
.dual{padding:8px 0}
.dual .top{display:flex;align-items:baseline}
.dual .n{font-size:32px;font-weight:700;width:150px;white-space:nowrap}
.dual .t{font-size:22px;color:var(--note);white-space:nowrap}
.dual .v{margin-left:auto;font-size:26px;color:var(--sub);white-space:nowrap}
.dual .v b{color:#fff;font-family:"Noto Sans SC";font-weight:900;font-size:32px}
.dual .bb{height:12px;border-radius:4px;margin-top:8px;background:var(--track);position:relative}
.dual .bb i{position:absolute;left:0;top:0;bottom:0;border-radius:4px}
.dual .bb i.u{background:var(--teal)} .dual .bb i.r{background:#8ff2dd;opacity:.55}
.leg{font-size:24px;color:var(--note);white-space:nowrap}
.leg i{display:inline-block;width:22px;height:12px;border-radius:3px;margin:0 8px 0 18px;vertical-align:middle}
.stk{display:flex;height:64px;border-radius:10px;overflow:hidden}
.stk div{display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:700;color:#041010;white-space:nowrap}
.kl{list-style:none}
.kl li{position:relative;padding-left:40px;font-size:31px;line-height:1.5;color:#c9cfd2}
.kl li:before{content:"";position:absolute;left:6px;top:19px;width:10px;height:10px;border-radius:50%;background:var(--teal)}
.kl li b{color:#fff}
.kblk .hd{margin-bottom:14px}
.srcl{font-size:21px;line-height:1.55;color:var(--note)}
.csum{position:absolute;left:0;right:0;font-size:32px;color:var(--sum);white-space:nowrap}
.csum b{color:var(--teal)}
'''
RISK='风险提示：本文信息仅供参考，不构成任何投资建议。'
def esc(s): return s
def page(label,body):
    return f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body><div class="page">
<div class="label">一图看懂｜{label}</div>{body}<div class="risk">{RISK}</div></div></body></html>'''
def cover(label,t1,t2,sub,rows,summ,unit=''):
    mx=max(r[3] for r in rows); top=470; h=68
    rs=''
    for i,(n,note,show,val) in enumerate(rows):
        f=' first' if i==0 else ''
        rs+=f'<div class="row c{f}" style="height:{h}px"><div class="idx">{i+1:02d}</div><div class="nm"><div class="name">{n}</div><div class="note">{note}</div></div><div class="num">{show}</div><div class="bar"><i style="width:{val/mx*100:.1f}%"></i></div></div>'
    body=f'''<div class="title cover2"><div class="w">{t1}</div><div class="t">{t2}</div></div>
<div class="subtitle" style="top:398px">{sub}</div>
<div class="rows" style="top:{top}px;display:flex;flex-direction:column;gap:6px">{rs}</div>
<div class="csum" style="top:{top+10*h+9*6+40}px">{summ}</div>'''
    return body
def inner(title,sub,blocks):
    return f'<div class="title it1"><span class="w">{title}</span></div><div class="isub">{sub}</div><div class="ibody">{"".join(blocks)}</div>'
def hbars(items,mx=None,unit=''):
    mx=mx or max(abs(x[3]) for x in items)
    o=''
    for it in items:
        n,s,show,val=it[:4]; cls=it[4] if len(it)>4 else ''
        o+=f'<div class="hr2 {cls}"><div class="n">{n}</div><div class="s">{s}</div><div class="v">{show}</div><div class="b"><i style="width:{abs(val)/mx*100:.1f}%"></i></div></div>'
    return o
def blk(inner,cls=''): return f'<div class="{cls}">{inner}</div>'
def hd(t,s=''): return f'<div class="hd"><i></i>{t}{f"<span>{s}</span>" if s else ""}</div>'
def kgrid(cards,cols):
    c=''.join(f'<div class="kc"><div class="k">{k}</div><div class="l">{l}</div></div>' for k,l in cards)
    return f'<div class="kg" style="grid-template-columns:repeat({cols},1fr)">{c}</div>'
def co(t): return f'<div class="co"><p>{t}</p></div>'
def klist(items): return '<ul class="kl">'+''.join(f'<li>{x}</li>' for x in items)+'</ul>'
def build(d,label,pages,names):
    des=os.path.join(d,'03-design'); os.makedirs(des,exist_ok=True)
    for f in ['base.css','check.js','check.sh']: shutil.copy(os.path.join(TPL,f),des)
    open(os.path.join(des,'style.css'),'w').write('@import url("base.css");\n'+EXTRA)
    fin=os.path.join(d,'final'); os.makedirs(fin,exist_ok=True)
    for i,b in enumerate(pages,1):
        open(f'{des}/p{i}.html','w').write(page(label,b))
        subprocess.run(['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--allow-file-access-from-files','--hide-scrollbars','--force-device-scale-factor=2','--window-size=1080,1440','--virtual-time-budget=3000',f'--screenshot={des}/p{i}.png',f'file://{des}/p{i}.html'],capture_output=True)
        shutil.copy(f'{des}/p{i}.png',f'{fin}/{names[i-1]}.png')
    from PIL import Image
    im=Image.open(f'{des}/p1.png'); im.resize((400,533)).save(f'{des}/thumb_p1.png')
