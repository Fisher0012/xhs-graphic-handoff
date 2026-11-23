#!/usr/bin/env python3
# 生成 p1-p4.html；所有文字/数字照抄 02-框架.md（第 3 版）
RISK='风险提示：本文信息仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。'
LABEL='<div class="label">一图看懂｜金融开放</div>'
def page(body):
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head>
<body><div class="page">{body}<div class="risk">{RISK}</div></div></body></html>'''

# ---------- P1 ----------
P1=[('01','摩根大通证券（中国）','美国 · 2021年8月 · 合资转独资','19.99',19.99),
('02','高盛（中国）证券','美国 · 2021年10月 · 合资转独资','33.86',33.86),
('03','渣打证券（中国）','英国 · 2023年1月 · 新设','10.5',10.5),
('04','法巴证券（中国）','法国 · 2024年4月 · 新设','11',11),
('05','瑞银证券','瑞士 · 2025年3月 · 合资转独资','22.1',22.1),
('06','瑞穗证券（中国）','日本 · 2025年9月 · 新设','23',23),
('07','花旗证券（中国）','美国 · 2026年10月 · 新设','12',12)]
mx=33.86
rows=''.join(f'<div class="row{" new" if i=="07" else ""}"><div class="idx">{i}</div><div class="nm"><div class="name">{n}</div><div class="note">{no}</div></div>'
             f'<div class="num">{s}</div><div class="bar"><i style="width:{v/mx*100:.2f}%"></i></div></div>' for i,n,no,s,v in P1)
p1=(LABEL+'<div class="title cover-title"><span class="t">7家</span><span class="w">外资独资券商</span></div>'
 '<div class="gline"></div><div class="subtitle cover-sub">按获批独资时间排序 · 右侧为注册资本（亿元）</div>'
 f'<div class="rows" style="top:384px">{rows}</div>'
 '<div class="hr" style="top:1196px"></div>'
 '<div class="summary" style="top:1222px">7家注册资本合计 <b>132.45亿元</b>（自算）；母公司来自 <b>5</b> 国，<span class="nw">美国 <b>3</b> 家的注册资本约占 <b>一半</b>。</span></div>')

# ---------- P2 ----------
TL=[('摩根大通',[('2019年','51%'),('2021年','100%')]),
    ('高盛',[('2004年','33%'),('2020年','51%'),('2021年','100%')]),
    ('瑞银',[('2018年','51%'),('2022年','67%'),('2025年','100%')])]
def tl(who,nodes,top):
    k=len(nodes); out=[]
    for j,(y,p) in enumerate(nodes):
        x=4+(j/(k-1))*86
        out.append(f'<div class="nd{" full" if p=="100%" else ""}" style="left:{x:.1f}%"><div class="yr">{y}</div><div class="dot"></div><div class="pc">{p}</div></div>')
    return f'<div class="tl" style="top:{top}px"><div class="who">{who}</div><div class="axis">{"".join(out)}</div></div>'
# axis 内节点：.nd 相对 axis 定位，yr 在轴上方
NEW=[('03','渣打','2023年1月19日','首家新设'),('04','法巴','2024年4月12日',''),('06','瑞穗','2025年9月30日',''),('07','花旗','2026年10月23日','')]  # 编号沿用封面 01–07
p2=(LABEL+'<div class="title inner-title"><span class="w">两条路走到</span><span class="t">100%</span></div>'
 '<div class="subtitle inner-sub">合资转独资 vs 直接新设</div>'
 '<div class="sec" style="top:330px">合资转独资 · 外资持股比例变化</div>'
 + tl(*TL[0],392)+tl(*TL[1],530)+tl(*TL[2],668) +
 '<div class="band" style="top:818px">2020年4月1日起，全国取消证券公司<b>外资股比限制</b></div>'
 '<div class="sec" style="top:930px">直接新设 · 证监会核准设立</div>'
 + ''.join(f'<div class="nrow" style="top:{984+i*70}px"><div class="idx">{no}</div><div class="name">{n}</div><div class="date">{d}</div>'
           + (f'<div class="tag">{t}</div>' if t else '') + '</div>' for i,(no,n,d,t) in enumerate(NEW)) +
 '<div class="summary" style="top:1292px">限制取消后，<b>3家</b>合资券商增持到100%，另有<b>4家</b>直接新设。</div>')

# ---------- P3 ----------
COLS=['经纪','咨询','承销','自营','资管','两融','代销']
M=[('01','摩根大通','●●●●○○○'),('02','高盛','●●●●○○●'),('03','渣打','●○◐●◐○○'),('04','法巴','●●○●●○○'),
   ('05','瑞银','●●●●●●●'),('06','瑞穗','○○◐●◐○○'),('07','花旗','●●●●○○○')]
cls={'●':'y','◐':'h','○':'n'}
mrows=''.join(f'<div class="mr{" dash" if i=="07" else ""}"><div class="idx">{i}</div><div class="nm">{n}'
   + ('<span class="pend">未展业</span>' if i=='07' else '') + '</div>'
   + ''.join(f'<div class="c"><i class="dt {cls[ch]}"></i></div>' for ch in s) + '</div>' for i,n,s in M)
p3=(LABEL+'<div class="title inner-title"><span class="w">7家能做</span><span class="t">哪些业务</span></div>'
 '<div class="subtitle inner-sub">按业务许可证或公司披露 · 截至2026年10月25日</div>'
 '<div class="legend" style="top:326px"><span><i class="dt y"></i>有</span><span><i class="dt h"></i>受限</span><span><i class="dt n"></i>无</span></div>'
 '<div class="mx" style="top:376px"><div class="mh"><div class="nm"></div>' + ''.join(f'<div class="c">{c}</div>' for c in COLS) + '</div>'
 + mrows + '</div>'
 '<div class="fn" style="top:1100px"><i class="dt h"></i>：渣打、瑞穗只做承销不做保荐，资管限资产证券化。<br>花旗、瑞穗按证监会批复范围；花旗还没拿到业务许可证。</div>'
 '<div class="hr" style="top:1204px"></div>'
 '<div class="summary" style="top:1226px">7家都有<b>自营</b>；<b>融资融券</b>只有瑞银1家；瑞穗是唯一<b>没有经纪</b>业务的。</div>')

# ---------- P4 ----------
IT=[('独资','外资持股100%。'),
    ('获批时间','新设看核准日，转独资看备案日。'),
    ('注册资本','最新公开数，不代表经营规模；<br>渣打按设立批复，未查到年报。'),
    ('业务','按许可证或公司披露；<br>花旗、瑞穗按批复，瑞穗许可证范围未公布。'),
    ('第7家','媒体统计；大和在办股权变更，未计入。'),
    ('花旗','拿到业务许可证后才能展业。')]
p4=(LABEL+'<div class="title inner-title"><span class="w">这几个数</span><span class="t">要说明</span></div>'
 '<div class="items" style="top:300px">' + ''.join(f'<div class="it"><div class="no">{i+1}</div><div class="k">{k}</div><div class="v">{v}</div></div>' for i,(k,v) in enumerate(IT)) + '</div>'
 '<div class="hr" style="top:1214px"></div>'
 '<div class="src" style="top:1236px">数据来源：中国证监会、各公司官网披露、新华财经、上海证券报等；截至2026年10月25日。</div>')

for i,b in enumerate([p1,p2,p3,p4],1):
    open(f'p{i}.html','w').write(page(b))
