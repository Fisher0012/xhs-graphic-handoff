# 阿信学财经·大号黑金 统一样式（色值与 notes/20261026-2025各省GDP/03-design/style.css 一致）
F="file:///home/box/.fonts/"
# ===== 内页标题统一规范（Fisher 2026-10-31）：所有内页页标题 64px NSB 字距2px 整行金渐变、强制一行；副标题 26px #9b9b9e 一行。只能用 head() 生成 =====
PAGE_TITLE_PX=64; PAGE_SUB_PX=26
GOLD="#e9b519";GOLD_HI="#f7e6ae";GOLD_DK="#8a6a12"
TITLE_GRAD="linear-gradient(165deg,#f7e6ae 0%,#f2cd52 40%,#e2ab12 75%,#c98f0c 100%)"
BAR_HI="linear-gradient(90deg,#fff4cf 0%,#f5d873 30%,#e9b519 100%)"
BAR="linear-gradient(90deg,#f5dc84 0%,#e9b519 55%,#b8860f 100%)"
BAR_DIM="linear-gradient(90deg,#7a6020,#5e4a18)"
BG="radial-gradient(ellipse 760px 620px at 88% 4%,rgba(214,160,30,.16),rgba(214,160,30,0) 72%),linear-gradient(175deg,#121012 0%,#0a090a 50%,#030304 100%)"
CSS=f"""@font-face{{font-family:NSB;src:url({F}NotoSansSC-Black.otf)}}@font-face{{font-family:NSM;src:url({F}NotoSansSC-Medium.otf)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1440px;overflow:hidden;background:{BG};color:#fff;font-family:NSM;position:relative;padding:76px 66px 0;line-break:strict}}
.tag{{color:{GOLD};font-family:NSB;font-size:28px;letter-spacing:1px}}
h1{{font-family:NSB;font-size:{PAGE_TITLE_PX}px;letter-spacing:2px;line-height:1.2;margin-top:20px;white-space:nowrap;display:inline-block;background:{TITLE_GRAD};-webkit-background-clip:text;background-clip:text;color:transparent}}
.hsub{{color:#9b9b9e;font-family:NSM;font-size:{PAGE_SUB_PX}px;line-height:1.4;white-space:nowrap;margin-bottom:6px}}
.g{{background:{TITLE_GRAD};-webkit-background-clip:text;background-clip:text;color:transparent}}
.gc{{color:{GOLD}}}
.ul{{width:124px;height:6px;border-radius:3px;background:linear-gradient(90deg,{GOLD_HI},{GOLD});margin:24px 0 18px}}
.sub{{color:#9b9b9e;font-size:25px;line-height:1.55}}
.foot{{position:absolute;left:0;right:0;bottom:36px;text-align:center;color:#66666a;font-size:20px}}
.pn{{position:absolute;right:56px;top:76px;color:#66666a;font-size:24px}}
.card{{position:relative;background:linear-gradient(90deg,#191612,#121113);border:1px solid #26232a;border-radius:16px;padding:26px 32px 28px 38px;margin-top:24px;overflow:hidden}}
.card:before{{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;background:linear-gradient(180deg,{GOLD_HI},{GOLD})}}
.it{{margin-top:40px}}
.it h3{{font-family:NSB;font-size:38px;line-height:1.3;color:#fff}}
.it h3 .k{{color:{GOLD}}}
.it p{{font-size:27px;line-height:1.8;color:#bdb8ae;margin-top:10px}}
.lab{{color:{GOLD};font-family:NSB;font-size:24px;letter-spacing:1px}}
.big{{font-family:NSB;color:{GOLD}}}
.src{{color:#7d7a80;font-size:20px;line-height:1.55;margin-top:20px}}
table{{width:100%;border-collapse:collapse}}
td{{padding:14px 0;font-family:NSB;font-size:32px;border-bottom:1px solid #232124}}
td+td{{text-align:right}}
tr.h td{{font-family:NSM;font-size:22px;color:#9b9b9e;border-bottom:2px solid {GOLD};padding:10px 0}}
"""
FOOT='<div class="foot">风险提示：本文信息仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。</div>'
# ===== 版面撑满（Fisher 2026-10-31 21:12）：内容从页头到页脚均匀分布，不留大块空白 =====
# 渲染时 JS 量出内容底部到页脚的剩余高度，先加大表格行距，再均分到页标题以下各内容块之间的间距（单处上限）。
FILL_JS="""<script>document.fonts.ready.then(function(){
var b=document.body,f=document.querySelector('.foot'),limit=1440-36-f.offsetHeight-56;
/* 来源行与风险提示页脚至少留 40px（审查 2026-10-31）：内容超出时先压缩块间距/字号 */
var kids=[].slice.call(b.children).filter(function(e){return !e.matches('.foot,.pn,style,script')&&getComputedStyle(e).position!='absolute'});
var hs=kids.findIndex(function(e){return e.matches('.hsub')});var blocks=kids.slice(hs+1);
function bottom(){var m=0;kids.forEach(function(e){var r=e.getBoundingClientRect();if(r.height)m=Math.max(m,r.bottom)});return m}
var free=limit-bottom();
if(free<0){var sh=[].slice.call(document.querySelectorAll('.it,.card,.src,table'));for(var t=0;t<30&&limit-bottom()<0;t++){sh.forEach(function(e){var m=parseFloat(getComputedStyle(e).marginTop);if(m>10)e.style.marginTop=(m-2)+'px'});[].slice.call(document.querySelectorAll('.it p,.card p,.src,td')).forEach(function(e){var cs=getComputedStyle(e);if(e.matches('td')){var pt=parseFloat(cs.paddingTop);if(pt>6){e.style.paddingTop=(pt-1)+'px';e.style.paddingBottom=(parseFloat(cs.paddingBottom)-1)+'px'}}else{var lh=parseFloat(cs.lineHeight)/parseFloat(cs.fontSize);if(lh>1.5)e.style.lineHeight=lh-0.02}})}}
for(var t2=0;t2<6&&limit-bottom()<0;t2++){[].slice.call(document.querySelectorAll('.it p,.it h3,.card p,.src,td,.sub')).forEach(function(e){e.style.fontSize=(parseFloat(getComputedStyle(e).fontSize)-1)+'px'})}
free=limit-bottom();if(free<=8)return;
var rows=[].slice.call(document.querySelectorAll('tr:not(.h) td'));var trs=document.querySelectorAll('tr:not(.h)').length;
if(trs){var add=Math.min(free*0.45/trs,14)/2;rows.forEach(function(td){var cs=getComputedStyle(td);td.style.paddingTop=(parseFloat(cs.paddingTop)+add)+'px';td.style.paddingBottom=(parseFloat(cs.paddingBottom)+add)+'px'})}
var tx=[].slice.call(document.querySelectorAll('.it h3, .it p, .card p, .card .lab, .card h3'));var base=tx.map(function(e){return parseFloat(getComputedStyle(e).fontSize)});
if(limit-bottom()>120){for(var k=1.02;k<=1.161;k+=0.02){tx.forEach(function(e,i){e.style.fontSize=(base[i]*k)+'px'});if(bottom()>limit-60){tx.forEach(function(e,i){e.style.fontSize=(base[i]*(k-0.02))+'px'});break}}}
var items=[].slice.call(document.querySelectorAll('.it p, .card p'));
free=limit-bottom();if(free>8&&items.length){items.forEach(function(p){var cs=getComputedStyle(p);var lh=parseFloat(cs.lineHeight)/parseFloat(cs.fontSize);if(lh<1.85)p.style.lineHeight=Math.min(1.85,lh+0.15)})}
free=limit-bottom();var gs=blocks.filter(function(e){return e.getBoundingClientRect().height>0&&!e.matches('style')});
if(free>8&&gs.length){var g=Math.min(free/gs.length,90);gs.forEach(function(e){var cs=getComputedStyle(e);e.style.marginTop=(parseFloat(cs.marginTop)+g)+'px'})}
/* 收尾保护：撑满后若越过 limit，回收行高/字号直到来源行离页脚≥56px */
for(var t3=0;t3<80&&limit-bottom()<0;t3++){[].slice.call(document.querySelectorAll('td')).forEach(function(e){var cs=getComputedStyle(e);var pt=parseFloat(cs.paddingTop);if(pt>6){e.style.paddingTop=(pt-1)+'px';e.style.paddingBottom=(parseFloat(cs.paddingBottom)-1)+'px'}});[].slice.call(document.querySelectorAll('.it p,.card p')).forEach(function(p){var cs=getComputedStyle(p);var lh=parseFloat(cs.lineHeight)/parseFloat(cs.fontSize);if(lh>1.5)p.style.lineHeight=lh-0.03;else p.style.fontSize=(parseFloat(cs.fontSize)-0.5)+'px'});blocks.forEach(function(e){var m=parseFloat(getComputedStyle(e).marginTop);if(m>14)e.style.marginTop=(m-2)+'px'})}
})</script>"""
GAP_JS="""<script>document.fonts.ready.then(function(){setTimeout(function(){var f=document.querySelector('.foot');var m=0;[].slice.call(document.body.children).forEach(function(e){if(e.matches('.foot,.pn,style,script'))return;var r=e.getBoundingClientRect();if(r.height)m=Math.max(m,r.bottom)});document.body.setAttribute('data-gap',Math.round(f.getBoundingClientRect().top-m))},50)})</script>"""
def page(path,n,body,total=6):
    # 01_排行榜已删除（2026-10-31 21:10），内页页码顺延：p3→2/5 … p6→5/5（封面算第1张）
    open(path,"w").write(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}<div class=pn>{n-1}/{total-1}</div>{FOOT}{FILL_JS}{GAP_JS}</body></html>')
def head(title,sub):
    return f'<h1>{title}</h1><div class=ul style="margin:18px 0 14px"></div><div class=hsub>{sub}</div>'
def it(h,p): return f'<div class=it><h3>{h}</h3><p>{p}</p></div>'
def tr(*c,hl=False,cls=""):
    # Fisher「只突出前三名」：表格行不再按重点加金色，hl 参数保留但不生效（2026-10-31 21:25）
    return f'<tr class="{cls}">'+''.join(f'<td>{x}</td>' for j,x in enumerate(c))+'</tr>'
def ranking(rows,unit_note,src,tag,title,explain="",unit="万亿",fmt="{:.2f}"):
    mx=max(r[2] for r in rows);h=""
    for i,(cn,en,v,hl) in enumerate(rows):
        cr,rc,col,bar=rank_style(i); cr=cr.replace('width="36"','width="30"').replace('height="28"','height="23"').replace('width:44px','width:38px')
        h+=f'''<div style="display:flex;align-items:baseline;height:56px"><div style="width:100px;white-space:nowrap;font-family:NSB;font-size:28px;color:{rc}">{cr}{i+1:02d}</div>
<div style="font-family:NSB;font-size:38px;width:276px;color:{col}">{cn}</div><div style="flex:1;color:#8a8a8e;font-size:21px">{en}</div>
<div style="font-family:NSB;font-size:42px;color:{col}">{fmt.format(v)}<span style="font-size:20px;color:#9b9b9e;margin-left:4px">{unit}</span></div></div>
<div style="height:6px;border-radius:3px;width:{v/mx*948:.0f}px;background:{bar};margin:2px 0 12px"></div>'''
    return f'<div class=tag>{tag}</div>{head(title,unit_note)}<div style="margin-top:14px">{h}</div>{explain}<div class=src style="margin-top:10px">{src}</div>'

# ===== 榜单高亮固定规范（Fisher 2026-10-31，所有封面/内页TOP10统一）=====
# 只突出前三名：1金 2银 3铜；序号前放皇冠SVG(平面微渐变)；前三名名称、数字、进度条用对应色
# 第4–10名：白字、序号灰#5b5b5f、普通金色进度条 BAR_DIM；不再按"国别/主题"加色，主题用副标题文字表达
MEDAL=[  # (文字色, 进度条渐变, 皇冠渐变上, 皇冠渐变下)
 ("#f2c94c","linear-gradient(90deg,#fff4cf 0%,#f5d873 30%,#e9b519 100%)","#fbe7a1","#d9a514"),
 ("#d9dde3","linear-gradient(90deg,#ffffff 0%,#d9dde3 40%,#9aa1ab 100%)","#ffffff","#a7aeb8"),
 ("#e0975e","linear-gradient(90deg,#f6c9a0 0%,#d98a4e 45%,#a8602e 100%)","#f3c29a","#b06a36"),
]
def crown(i,s=30):
    a,b=MEDAL[i][2],MEDAL[i][3]
    return f'''<svg width="{s}" height="{s*0.78:.0f}" viewBox="0 0 32 25" style="vertical-align:-1px"><defs><linearGradient id="cg{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs><path d="M2 7 L9 13 L16 3 L23 13 L30 7 L27 20 L5 20 Z" fill="url(#cg{i})"/><rect x="5" y="21.5" width="22" height="3" rx="1.2" fill="url(#cg{i})"/><circle cx="2" cy="6" r="2" fill="{a}"/><circle cx="16" cy="2.2" r="2.2" fill="{a}"/><circle cx="30" cy="6" r="2" fill="{a}"/></svg>'''
def rank_style(i):
    "返回 (序号html内容前缀, 序号色, 名称/数字色, 进度条)"
    slot=lambda c,w: f'<span style="display:inline-block;width:{w}px">{c}</span>'
    if i<3: return slot(crown(i,36),44), MEDAL[i][0], MEDAL[i][0], MEDAL[i][1]
    return slot("",44), "#5b5b5f", "#fff", BAR_DIM
