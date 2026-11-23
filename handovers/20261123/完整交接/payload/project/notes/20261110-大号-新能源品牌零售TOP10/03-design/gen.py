import sys, re
sys.path.insert(0, '/workspace/xhs/notes')
from heijin import *
from cover_gen import cover

D = '/workspace/xhs/notes/20261110-大号-新能源品牌零售TOP10/03-design/'
SRC_COVER = '来源：乘联分会 2026-11-09 发布（IT之家、凤凰网、中新网等转载）'

rows = [("比亚迪", "传统车企", 250301, 1), ("吉利", "传统车企", 131708, 0), ("零跑", "新势力", 83573, 0),
        ("长安", "传统车企", 68925, 0), ("上汽通用五菱", "传统车企", 67696, 0), ("小米", "新势力", 50123, 0),
        ("奇瑞", "传统车企", 44747, 0), ("上汽乘用车", "传统车企", 38881, 0), ("长城", "传统车企", 37469, 0),
        ("小鹏", "新势力", 36911, 0)]
cover(D + 'p1.html', '一图看懂｜10月新能源车市', '新能源车零售榜',
      '2026年10月 · 国内新能源乘用车零售 · 企业品牌 · 单位：辆', rows, '辆', SRC_COVER, fmt='{:,.0f}')
h = open(D + 'p1.html').read()
# 本期标题7字：122px 占可用宽约88%，按审查口径(75–85%)本期内覆盖为112px（不改共享 cover_gen.py）
h = h.replace('</style>', 'h1{font-size:112px;letter-spacing:4px}.row{align-items:center;height:62px;padding-top:0}.rk svg{vertical-align:-2px}</style>', 1)
card = ('<div style="margin-top:14px;background:linear-gradient(90deg,#191612,#121113);border:1px solid #26232a;border-radius:14px;padding:16px 24px;font-size:25px;color:#bdb8ae">'
        '前10合计 <b style="color:#e9b519">81.03万</b> 辆，约占新能源零售 <b style="color:#e9b519">73%</b>（作者计算）｜分类为作者整理</div>')
h = h.replace('</div>\n<div class=foot>', '</div>' + card + '\n<div class=foot>', 1) if '</div>\n<div class=foot>' in h else re.sub(r'(</div>)(\s*<div class=foot>)', r'\1' + card + r'\2', h, count=1)
open(D + 'p1.html', 'w').write(h)

T = '<div class=tag>一图看懂｜10月新能源车市</div>'

def stat(lab, num, unit, note):
    return (f'<div class=card style="margin-top:0;padding:20px 24px 22px 32px"><div class=lab>{lab}</div>'
            f'<div style="font-family:NSB;font-size:56px;margin-top:6px" class=g>{num}<span style="font-size:24px;color:#9b9b9e;margin-left:6px">{unit}</span></div>'
            f'<p style="font-size:24px;color:#bdb8ae;margin-top:4px;line-height:1.5">{note}</p></div>')

grid = lambda *c: '<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:22px">' + ''.join(c) + '</div>'

page(D + 'p2.html', 2, f'''{T}{head('先看10月车市大盘', '单位：万辆｜乘用车｜榜单与渗透率均为国内零售口径')}
{grid(stat('10月 乘用车零售', '164.3', '万辆', '同比 <span class=gc>−27.1%</span>｜环比 +1.5%'),
      stat('10月 新能源零售', '110.9', '万辆', '同比 <span class=gc>−13.7%</span>｜环比 +2.3%'),
      stat('1–10月 乘用车累计', '1497.8', '万辆', '同比 <span class=gc>−22.3%</span>'),
      stat('1–10月 新能源累计', '886.9', '万辆', '同比 <span class=gc>−12.9%</span>'))}
{it('先分清｜<span class=k>零售</span>和<span class=k>批发</span>', '零售＝国内卖到消费者手里的车；批发＝厂家发给经销商的车，还包含出口。封面榜单按零售算。')}
<table style="margin-top:22px"><tr class=h><td>10月 · 口径</td><td>数量</td><td>同比</td></tr>
<tr><td>国内零售</td><td>164.3 万</td><td>−27.1%</td></tr>
<tr><td>厂商批发（含出口）</td><td>263.3 万</td><td>−10.2%</td></tr>
<tr><td>出口（含整车与CKD）</td><td>92.8 万</td><td>+68.5%</td></tr></table>
{it('为什么批发跌得比零售少', '乘联分会：出口占厂商销量 <span class=gc>35%</span>（去年同期19%），出口撑住了批发；国内零售被概括为「旺季不旺」。')}
<div class=src>来源：乘联分会 2026-11-09 发布（IT之家、中新网、安兔兔等转载）</div>''', total=4)

page(D + 'p3.html', 3, f'''{T}{head('燃油车同比少了45%', '常规燃油车＝纯燃油＋普通混动（不插电）｜国内零售')}
<div style="display:flex;gap:18px;margin-top:22px">
<div class=card style="flex:1;margin-top:0;padding:20px 24px 22px 32px"><div class=lab>新能源零售渗透率</div><div style="font-family:NSB;font-size:72px;margin-top:4px" class=g>67.5%</div><p style="font-size:24px;color:#bdb8ae;line-height:1.5">比去年同期 +10.5 个百分点</p></div>
<div class=card style="flex:1;margin-top:0;padding:20px 24px 22px 32px"><div class=lab>常规燃油车零售</div><div style="font-family:NSB;font-size:72px;margin-top:4px" class=g>53<span style="font-size:26px;color:#9b9b9e;margin-left:6px">万辆</span></div><p style="font-size:24px;color:#bdb8ae;line-height:1.5">同比 −45%｜环比 −0.1%</p></div></div>
<div style="margin-top:26px;height:46px;border-radius:10px;overflow:hidden;display:flex;font-family:NSB;font-size:24px">
<div style="width:67.5%;background:{BAR};color:#1a1406;display:flex;align-items:center;padding-left:18px">新能源 110.9万</div>
<div style="flex:1;background:#2b2a2e;color:#d8d6d0;display:flex;align-items:center;padding-left:14px">燃油 53万</div></div>
<table style="margin-top:22px"><tr class=h><td>燃油车拆开看</td><td>同比</td></tr>
<tr><td>纯燃油车</td><td>−51%</td></tr><tr><td>普通混动</td><td>+28%</td></tr>
<tr><td>其中 · 自主 / 主流合资</td><td>−46% / −46%</td></tr><tr><td>其中 · 豪华品牌</td><td>−37%</td></tr></table>
{it('<span class=k>渗透率</span>是什么', '每卖出100辆乘用车里新能源占几辆。67.5%约等于每3辆里有2辆；去年同期约57.0%（作者计算：67.5−10.5）。')}
{it('乘联分会怎么解释', '燃油车各阵营「均无差别地受到高油价剧烈冲击」。这是协会的说法，本文不预测油价和车市。')}
<div class=src>来源：乘联分会 2026-11-09 发布（IT之家、凤凰网、安兔兔转载）；标注处为作者计算</div>''', total=4)

page(D + 'p4.html', 4, f'''{T}{head('新势力与传统车企', '新能源零售口径｜「新势力/传统」分类为作者整理')}
<div style="display:flex;gap:18px;margin-top:22px">
<div class=card style="flex:1;margin-top:0;padding:20px 24px 22px 32px"><div class=lab>新势力零售份额</div><div style="font-family:NSB;font-size:68px;margin-top:4px" class=g>23.9%</div><p style="font-size:24px;color:#bdb8ae;line-height:1.5">同比 +1.2 个百分点</p></div>
<div class=card style="flex:1;margin-top:0;padding:20px 24px 22px 32px"><div class=lab>传统车企独立新能源品牌</div><div style="font-family:NSB;font-size:68px;margin-top:4px" class=g>15.3%</div><p style="font-size:24px;color:#bdb8ae;line-height:1.5">同比 +0.8 个百分点</p></div></div>
{it('<span class=k>①</span> 前10名里谁占大头', '传统车企7家合计约 <span class=gc style="white-space:nowrap">63.97万辆</span>；新势力3家（零跑、小米、小鹏）合计约 <span class=gc style="white-space:nowrap">17.06万辆</span>（作者计算）。')}
<table style="margin-top:20px"><tr class=h><td>榜外紧追 · 第11–14名</td><td>10月零售（辆）</td></tr>
<tr><td>蔚来</td><td>34,030</td></tr><tr><td>鸿蒙智行</td><td>33,538</td></tr><tr><td>广汽埃安</td><td>30,011</td></tr><tr><td>理想</td><td>27,018</td></tr></table>
{it('<span class=k>②</span> 新势力在变', '新势力卖出的车里纯电占 <span class=gc>66.9%</span>，去年同期是74.3%；纯电里10–15万元价位占比大幅增长。')}
{it('<span class=k>③</span> 按阵营看新能源零售', '同比：自主 −15%，主流合资 <span class=gc>+69%</span>，豪华 −45%。只摆数据，不评车、不涉及任何股票。')}
<div class=src>来源：乘联分会 2026-11-09 发布（凤凰网、新浪财经等转载）；合计为作者计算</div>''', total=4)
print('gen ok')
