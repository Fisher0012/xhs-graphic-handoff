#!/usr/bin/env python3
# 生成 p1-p4.html；数字读 ../data.json，文字照 02-框架.md（Fisher 2026-10-30 确认，封面标题「美股单日蒸发 / 前十名」）
import json
D=json.load(open('../data.json')); T=D['top10']; G=D['alphabet_selfcalc']
RISK='风险提示：本文信息仅供参考，不构成任何投资建议。'
LABEL='<div class="label">一图看懂｜美股</div>'
CALC='<span class="calc">（按收盘价计算）</span>'
def page(b): return f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body><div class="page">{LABEL}{b}<div class="risk">{RISK}</div></div></body></html>'
def cn(d): y,m,dd=d.split('-'); return f'{y}年{int(m)}月{int(dd)}日'
def v(e): return round(e['check_yi'])
NAME={'谷歌（Alphabet）':'谷歌'}
# 媒体数只写已打开原文核实、且口径为单日收盘的
MEDIA={('英伟达','2025-01-27'):'媒体报约5890亿',('谷歌（Alphabet）','2026-10-29'):'媒体报4770–5000亿',
       ('SpaceX','2026-06-22'):'媒体报约4000亿',('微软','2026-01-29'):'媒体报约3570亿',('苹果','2025-04-03'):'媒体报约3110亿',
       ('谷歌（Alphabet）','2026-07-23'):'各家媒体报2550–3000亿',('博通','2026-06-04'):'媒体报2800–2860亿',('英伟达','2024-09-03'):'媒体报约2790亿'}
rank=sorted(T,key=lambda e:-e['check_yi'])
assert [e['rank'] for e in rank]==list(range(1,11)), [e['rank'] for e in rank]
mx=v(rank[0])
# ---------- P1 ----------
rows=''
for i,e in enumerate(rank,1):
    hl=' hl' if e['date']=='2026-10-29' else ''
    m=MEDIA.get((e['company'],e['date']),'')
    note=f'{cn(e["date"])}｜跌{abs(e["pct"]):.2f}%'+('（A类股）' if 'GOOG' in e['ticker'] else '')+(f'｜{m}' if m else '')
    rows+=(f'<div class="row{hl}" style="height:76px"><div class="idx">{i:02d}</div><div class="nm"><div class="name">{NAME.get(e["company"],e["company"])}</div>'
           f'<div class="note">{note}</div></div><div class="num"><small>约</small>{v(e)}</div><div class="bar"><i style="width:{v(e)/mx*100:.2f}%"></i></div></div>')
p1=('<div class="title cover2"><div class="w">美股单日蒸发</div><div class="t">前十名</div></div>'
 '<div class="gline" style="top:404px"></div>'
 '<div class="subtitle" style="top:426px">单日市值蒸发额｜单位：亿美元｜按收盘价计算｜截至2026年10月29日</div>'
 f'<div class="rows" style="top:482px">{rows}</div>'
 '<div class="foot" style="top:1252px">名义美元，没算通胀；同一家公司可多次上榜；排序和口径见第4页</div>')
# ---------- P2 ----------
S=G['shares_mn']; C=G['close']
a0,a1=C['GOOGL']['2026-10-28'],C['GOOGL']['2026-10-29']; c0,c1=C['GOOG']['2026-10-28'],C['GOOG']['2026-10-29']
ab=(S['A']+S['B'])/100; cc=S['C']/100   # 亿股
pA=(S['A']+S['B'])*(a0-a1)/100; pC=S['C']*(c0-c1)/100; tot=pA+pC
bef=((S['A']+S['B'])*a0+S['C']*c0)/1e6; aft=((S['A']+S['B'])*a1+S['C']*c1)/1e6   # 万亿美元
pct=(aft/bef-1)*100
assert round(tot)==round(G['loss_yi'])
fc=('<div class="fcard" style="top:340px">'
 f'<div class="fr"><span class="fl">A类+B类</span><span class="fx">{ab:.2f}亿股 × 每股少{a0-a1:.2f}美元</span><span class="fv">≈{pA:.0f}<small>亿</small></span></div>'
 f'<div class="fr"><span class="fl">C类</span><span class="fx">{cc:.2f}亿股 × 每股少{c0-c1:.2f}美元</span><span class="fv">≈{pC:.0f}<small>亿</small></span></div>'
 f'<div class="fr tot"><span class="fl">合计</span><span class="fx">单位：亿美元</span><span class="fv">≈{tot:.0f}<small>亿</small></span></div></div>')
cap=('<div class="cap" style="top:690px">'
 f'<div class="cb"><div class="cd">10月28日收盘市值</div><div class="cv">约{bef:.2f}<small>万亿</small></div></div>'
 f'<div class="ar">总市值<br>约{pct:.1f}%<br>→</div>'
 f'<div class="cb af"><div class="cd">10月29日收盘市值</div><div class="cv">约{aft:.2f}<small>万亿</small></div></div></div>')
MD=[('自算','收盘价 × 三类股本',round(tot),'约',True),('NBC News','收盘市值3.47万亿',5000,'约',False),
    ('Yahoo Finance','',4820,'',False),('Report.az','盘中数',4770,'',False)]
mm=max(x[2] for x in MD)
mr=''.join(f'<div class="mrow{" me" if me else ""}" style="top:{966+i*68}px"><div class="top"><span class="name">{n}</span><span class="tag">{t}</span>'
           f'<span class="num"><small>{q}</small>{x}<small>亿</small></span></div><div class="bar"><i style="width:{x/mm*100:.2f}%"></i></div></div>' for i,(n,t,x,q,me) in enumerate(MD))
p2=('<div class="title inner-title"><span class="w">谷歌这一天</span><span class="t">自己算一遍</span></div>'
 '<div class="gline" style="top:252px"></div>'
 '<div class="subtitle" style="top:272px">2026年10月29日｜收盘价 × 总股本，A、B、C三类股合计｜按收盘价计算</div>'
 f'{fc}{cap}'
 '<div class="sech" style="top:892px"><span class="ht">媒体怎么说</span></div>'
 f'{mr}'
 f'<div class="fn" style="top:1250px">B类股不上市，按A类股价计；股本为10月21日数（公司季报）；分项四舍五入</div>')
# ---------- P3 ----------
def items(IT,top,extra=''):
    s=''
    for i,(h,ls) in enumerate(IT,1):
        s+=(f'<div class="item2"><div class="h"><span class="no2">{i}</span><span class="ht">{h}</span></div><ul>'+''.join(f'<li>{l}</li>' for l in ls)+'</ul></div>'
            +('<div class="sep"></div>' if i<len(IT) else ''))
    return f'<div class="items p4sep" style="top:{top}px">{s}</div>'
yrs={}
for e in T: yrs[e['date'][:4]]=yrs.get(e['date'][:4],0)+1
cos={}
for e in T: cos[e['company']]=cos.get(e['company'],0)+1
assert yrs=={'2025':2,'2026':7,'2024':1} and cos['英伟达']==3 and cos['谷歌（Alphabet）']==2 and cos['苹果']==2
nv=[e for e in T if e['date']=='2026-06-05'][0]
CT=D['context']['yahoo_200bn_days']
IT3=[('前十里有7次在2026年',['另有2025年2次、2024年1次','按日期统计，截至2026年10月29日']),
 ('英伟达上榜3次',['谷歌、苹果各2次','SpaceX、微软、博通各1次']),
 ('跌得多 ≠ 蒸发得多',[f'英伟达2026年6月5日跌{abs(nv["pct"]):.2f}%，蒸发约{v(nv)}亿'+CALC,'Meta 2022年2月3日跌26.39%，蒸发约2320亿，不在前十']),
 ('超2000亿的单日越来越多',['单日蒸发2000亿美元以上的次数（2026年截至10月28日）','来源：Yahoo Finance（据Bloomberg数据）'])]
cols=[('2022年以前',CT['2022年以前']),('2025年',CT['2025']),('2026年',CT['2026（截至10-28）'])]
cm=max(c for _,c in cols)
chart=('<div class="chart minic" style="top:1050px;height:240px;left:110px;right:110px">'+''.join(
 f'<div class="col{" hi" if i==2 else ""}"><div class="v">{c}次</div><div class="b" style="height:{max(c/cm*170,3):.0f}px"></div><div class="m">{n}</div></div>' for i,(n,c) in enumerate(cols))
 +'</div>')
p3=('<div class="title inner-title"><span class="w">榜单里的</span><span class="t">几个规律</span></div>'
 +items(IT3,262)+chart)
# ---------- P4 ----------
ap=[e for e in T if e['date']=='2026-07-31'][0]; ms=[e for e in T if e['date']=='2026-01-29'][0]
IT4=[('名义美元，没算通胀',['按当时的美元金额直接比，没有按通胀调整','市值越大，同样的跌幅对应的金额越大']),
 ('蒸发是账面数，不是现金',['前一交易日收盘市值减当日收盘市值','是市值的账面变化，不是谁付出的现金；盘中数字不算']),
 ('各家媒体数字为什么不同',['股本取哪一天、多类股怎么算、用盘中价还是收盘价都会影响结果',f'谷歌10月29日：媒体报4770–5000亿，自算约{round(tot)}亿']),
 ('排序怎么算',['（前一日收盘价 − 当日收盘价）× 最近一期财报封面股本',f'第4名苹果约{v(ap)}亿、第5名微软约{v(ms)}亿，只差约{v(ap)-v(ms)}亿']),
 ('只统计美股上市公司',['同一家公司可以多次上榜，如英伟达3次','数据截至2026年10月29日美东时间收盘'])]
p4=('<div class="title inner-title"><span class="w">这几个数</span><span class="t">要说明</span></div>'
 +items(IT4,262)+
 '<div class="src" id="src" style="top:1250px">来源：CNBC、Yahoo Finance、NBC News、Bloomberg、Reuters、MarketWatch、Investopedia、Statista<br>股本：美国SEC公司财报；股价：纳斯达克、Yahoo Finance</div>')
for i,b in enumerate([p1,p2,p3,p4],1): open(f'p{i}.html','w').write(page(b))
print('tot',tot,pA,pC,'bef',bef,'aft',aft,'pct',pct)
