"""LPR连续18个月不变：用本期 heijin.py 副本（与共享版逐字节一致）生成四页 HTML。"""
import json
from pathlib import Path
# ---- 以下内联自本期 heijin.py 副本（与 /workspace/xhs/notes/heijin.py 逐字节一致），使本脚本自包含 ----
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

# ---- 内联结束 ----

D = Path(__file__).resolve().parent
N = D.parent
data = json.loads((N / 'data.json').read_text())
R = data['new_loan_rates_2026_09']['items']
assert data['unchanged_count'] == 18
T = '<div class=tag>一图看懂｜2026年11月LPR</div>'
SRC_LPR = '来源：中国人民银行LPR公告（2025-04-21至2026-11-20逐月）；「18个月」为作者按公告计数'
EXTRA = """
.num{font-family:NSB;line-height:1}.num small{font-size:30px;color:#9b9b9e;margin-left:4px;font-family:NSM}
.chip{display:inline-block;background:#e9b519;color:#121012;font-family:NSB;border-radius:8px;padding:2px 14px;margin-left:10px}
.k2{color:#e9b519;font-family:NSB}
"""


def write(n, body, total=4, cover=False):
    pn = '' if cover else f'<div class=pn>{n-1}/{total-1}</div>'
    (D / f'p{n}.html').write_text(
        f'<html><head><meta charset="utf-8"><style>{CSS}{EXTRA}</style></head><body>{body}{pn}{FOOT}{GAP_JS}</body></html>')


# ---------- P1 封面（非排名：无奖牌/金银铜/最高标签） ----------
months = [r for r in data['lpr'] if r['date'] > data['unchanged_since']]
cells = ''
for r in months:
    y, m, _ = r['date'].split('-')
    yr = f'<div style="font-size:17px;color:#7d7a80;height:22px">{y}年</div>' if r['date'] in ('2025-06-20', '2026-01-20') else '<div style="height:22px"></div>'
    cells += (f'<div style="width:94px;text-align:center">{yr}<div style="height:46px;border-radius:9px;background:linear-gradient(180deg,#2a2416,#1a1610);'
              f'border:1px solid #5e4a18;color:#f2cd52;font-family:NSB;font-size:24px;line-height:46px">{int(m)}月</div></div>')
cover = f'''<div class=tag style="font-size:30px;letter-spacing:2px">一图看懂｜11月20日最新报价</div>
<h1 style="font-size:122px;letter-spacing:4px;line-height:1.12;margin-top:16px">LPR连续<br>18个月不变</h1>
<div class=ul style="margin:22px 0 16px"></div>
<div class=hsub style="font-size:30px;color:#bdb8ae">1年期 <span class=k2>3.0%</span> · 5年期以上 <span class=k2>3.5%</span><span class=chip>18次报价未变</span></div>
<div style="display:flex;gap:18px;margin-top:34px">
 <div class=card style="flex:1;margin-top:0"><div class=lab>1年期LPR</div><div class="num g" style="font-size:112px;margin-top:10px">3.0<small>%</small></div><p style="font-size:24px;color:#bdb8ae;margin-top:12px">自2025年5月20日起未变</p></div>
 <div class=card style="flex:1;margin-top:0"><div class=lab>5年期以上LPR</div><div class="num g" style="font-size:112px;margin-top:10px">3.5<small>%</small></div><p style="font-size:24px;color:#bdb8ae;margin-top:12px">自2025年5月20日起未变</p></div>
</div>
<div class=lab style="margin-top:52px">2025年6月—2026年11月｜每月20日左右公布，18次全是3.0% / 3.5%</div>
<div style="display:flex;flex-wrap:wrap;gap:12px 8px;margin-top:14px">{cells}</div>
<div class=card style="margin-top:48px;padding:22px 30px"><div class=lab>上次调整｜2025年5月20日</div>
<p style="font-size:27px;color:#fff;margin-top:8px;line-height:1.6">1年期 3.1%→<span class=k2>3.0%</span>，5年期以上 3.6%→<span class=k2>3.5%</span>，各降10个基点</p></div>
<div class=src style="margin-top:26px">{SRC_LPR}</div>'''
write(1, cover, cover=True)

# ---------- P2 房贷利率怎么定 ----------
box = lambda lab, big, note, color='#191612': (
    f'<div style="flex:1;background:{color};border:1px solid #3a3020;border-radius:16px;padding:20px 10px;text-align:center">'
    f'<div class=lab>{lab}</div><div class="num g" style="font-size:64px;margin-top:10px">{big}</div>'
    f'<div style="font-size:22px;color:#9b9b9e;margin-top:10px">{note}</div></div>')
op = lambda s: f'<div style="font-family:NSB;font-size:64px;color:{GOLD};align-self:center">{s}</div>'
p2 = f'''{T}{head('房贷利率＝LPR＋加点', '浮动利率房贷的定价公式｜加点可以是负数')}
<div style="display:flex;gap:14px;margin-top:34px">{box('定价基准', '3.5<small>%</small>', '5年期以上LPR')}{op('＋')}{box('加点', '±', '合同约定，可为负')}{op('＝')}{box('房贷利率', '？', '看你的合同')}</div>
<table style="margin-top:46px"><tr class=h><td>举例（非真实合同）</td><td>LPR</td><td>加点</td><td>房贷利率</td></tr>
<tr><td>加点为正</td><td>3.5%</td><td>+0.3</td><td>3.8%</td></tr>
<tr><td>加点为负</td><td>3.5%</td><td>−0.3</td><td>3.2%</td></tr></table>
<div style="height:18px"></div>{it('<span class=k>①</span> 加点在签合同时约定', '浮动利率房贷以最近一个月LPR为基准加点形成。央行2024年第11号公告写明：加点可为负值。')}
<div style="height:18px"></div>{it('<span class=k>②</span> 也可以选固定利率', '合同约定为固定利率的，合同期内利率保持不变，LPR变不变都不影响。')}
<div class=src style="margin-top:34px">来源：中国人民银行公告〔2024〕第11号（2024-09-29）；表格为举例，具体以贷款合同为准。</div>'''.replace('class=src style="margin-top:34px"','class=src style="margin-top:56px"')
write(2, p2)

# ---------- P3 存量房贷看重定价日 ----------
step = lambda d, ref, rate, note, hi=False: (
    f'<div style="display:flex;align-items:center;gap:22px;margin-top:28px"><div style="width:22px;height:22px;border-radius:50%;background:{GOLD if hi else "#5e4a18"};flex:none"></div>'
    f'<div style="flex:1;background:#191612;border:1px solid #26232a;border-radius:14px;padding:16px 24px;display:flex;align-items:center">'
    f'<div style="width:300px;font-family:NSB;font-size:30px">{d}</div><div style="flex:1;font-size:24px;color:#bdb8ae">{ref}</div>'
    f'<div class="num {"g" if hi else ""}" style="font-size:44px;color:#fff">{rate}</div></div></div>'
    + (f'<div style="margin:6px 0 0 44px;font-size:22px;color:#9b9b9e">{note}</div>' if note else ''))
p3 = f'''{T}{head('存量房贷，看重定价日', 'LPR每月公布，存量浮动利率房贷不是每月跟着变')}
<div class=lab style="margin-top:32px">举例｜合同约定每年1月1日重定价，加点不变</div>
{step('2025年1月1日', '参考2024年12月LPR', '3.6%', '')}
{step('2026年1月1日', '参考2025年12月LPR', '3.5%', '基准比上一年低0.1个百分点，月供随之重算', True)}
{step('2027年1月1日', '参考2026年12月LPR', '待公布', '12月报价还没出，这里不做预测')}
<div style="height:22px"></div>{it('<span class=k>规则</span> 到了重定价日才换基准', '利率重定价日，定价基准调整为最近一个月LPR，加点数值不变。2020年转换的存量房贷，重定价周期最短一年；自2024年11月1日起，可与银行协商调整重定价周期。')}
<div class=card style="margin-top:52px;padding:22px 30px"><p style="font-size:27px;color:#fff;line-height:1.6;margin:0">这18个月里，不管重定价日在哪一天，参考的5年期以上LPR都是 <span class=k2>3.5%</span></p></div>
<div class=src style="margin-top:30px">来源：中国人民银行公告〔2019〕第30号、〔2024〕第11号；LPR公告2024-12-20、2025-12-22。时间轴为举例，具体以合同为准。</div>'''.replace('class=src style="margin-top:30px"','class=src style="margin-top:44px"')
write(3, p3)

# ---------- P4 新发放利率对照 ----------
bars = [('5年期以上LPR', 3.5, '9月、11月均为'), ('新发放个人住房贷款', R['个人住房贷款加权平均利率']['sep'], '9月加权平均'),
        ('新发放贷款（整体）', R['新发放贷款加权平均利率']['sep'], '9月加权平均'), ('1年期LPR', 3.0, '9月、11月均为'),
        ('新发放企业贷款', R['企业贷款加权平均利率']['sep'], '9月加权平均')]
bh = ''
for name, v, note in bars:
    lpr = 'LPR' in name
    bh += (f'<div style="display:flex;align-items:baseline;margin-top:20px"><div style="width:330px;font-family:NSB;font-size:30px;color:{"#fff" if lpr else "#f2cd52"}">{name}</div>'
           f'<div style="flex:1;font-size:21px;color:#8a8a8e">{note}</div><div class=num style="font-size:44px;color:{"#fff" if lpr else "#f2cd52"}">{v:.2f}<small>%</small></div></div>'
           f'<div style="height:10px;border-radius:5px;margin-top:8px;width:{v/3.5*948:.0f}px;background:{"linear-gradient(90deg,#9aa1ab,#5b5b5f)" if lpr else "linear-gradient(90deg,#f5dc84,#e9b519,#b8860f)"}"></div>')
hz = R['个人住房贷款加权平均利率']
p4 = f'''{T}{head('9月新发放房贷3.05%', '央行三季度货币政策执行报告｜加权平均利率 vs LPR')}
<div style="margin-top:22px">{bh}</div>
<table style="margin-top:50px"><tr class=h><td>9月加权平均利率</td><td>比6月</td><td>同比</td></tr>
<tr><td>新发放个人住房贷款 3.05%</td><td>{hz["vs_jun"]:+.2f}</td><td>{hz["yoy"]:+.2f}</td></tr>
<tr><td>新发放企业贷款 2.96%</td><td>{R["企业贷款加权平均利率"]["vs_jun"]:+.2f}</td><td>{R["企业贷款加权平均利率"]["yoy"]:+.2f}</td></tr></table>
<div style="height:20px"></div>{it('<span class=k>怎么看</span> 新房贷平均比同期LPR低约0.45个百分点', '3.05%是9月所有新发放房贷的加权平均，不代表每一笔贷款都是这个利率；也不说明存量房贷已调到这个水平。')}
<div class=src style="margin-top:30px">来源：中国人民银行《2026年第三季度中国货币政策执行报告》表4（2026-11-11）；变化单位为百分点；“约0.45”=3.5−3.05，作者计算。</div>'''
write(4, p4)
print('gen ok')
