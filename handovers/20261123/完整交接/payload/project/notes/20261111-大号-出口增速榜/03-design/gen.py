import sys, re
sys.path.insert(0, '/workspace/xhs/notes')
from heijin import *
from cover_gen import cover

D = '/workspace/xhs/notes/20261111-大号-出口增速榜/03-design/'
SRC_COVER = '来源：海关总署 2026-11-10 发布（统计月报表、新华社）｜作者按增速排序'

rows = [("存储部件", "数据存储设备", 132.5, 1), ("3D打印机", "增材制造设备", 104.8, 0), ("集成电路", "也就是芯片", 101.9, 0),
        ("电脑及零部件", "自动数据处理设备", 53.6, 0), ("新三样", "电动车·锂电池·光伏电池", 46.5, 0), ("汽车", "含底盘", 45.8, 0),
        ("数码相机", "数字照相机", 41.4, 0), ("电动摩托车", "含电动脚踏车", 33.3, 0), ("船舶", "整船出口", 22.4, 0),
        ("风电机组", "含零件", 19.7, 0)]
cover(D + 'p1.html', '一图看懂｜前10个月中国出口', '中国出口增速榜',
      '2026年1–10月 · 机电类重点商品 · 出口额同比 · 人民币计', rows, '%', SRC_COVER, fmt='+{:.1f}')
h = open(D + 'p1.html').read()
h = h.replace('</style>', 'h1{font-size:112px;letter-spacing:4px}.row{align-items:center;height:62px;padding-top:0}.rk svg{vertical-align:-2px}</style>', 1)
card = ('<div style="margin-top:14px;background:linear-gradient(90deg,#191612,#121113);border:1px solid #26232a;border-radius:14px;padding:16px 24px;font-size:25px;color:#bdb8ae">'
        '同期全部出口 <b style="color:#e9b519">25.99万亿元</b>，同比 <b style="color:#e9b519">+17.6%</b>｜品类有交叉，不能相加</div>')
h = re.sub(r'(</div>)(\s*<div class=foot>)', r'\1' + card + r'\2', h, count=1)
open(D + 'p1.html', 'w').write(h)

T = '<div class=tag>一图看懂｜前10个月中国出口</div>'

def stat(lab, num, unit, note):
    return (f'<div class=card style="margin-top:0;padding:20px 24px 22px 32px"><div class=lab>{lab}</div>'
            f'<div style="font-family:NSB;font-size:56px;margin-top:6px" class=g>{num}<span style="font-size:24px;color:#9b9b9e;margin-left:6px">{unit}</span></div>'
            f'<p style="font-size:24px;color:#bdb8ae;margin-top:4px;line-height:1.5">{note}</p></div>')
grid = lambda *c: '<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:22px">' + ''.join(c) + '</div>'
def duo(a, b):
    def one(lab, num, unit, note):
        return (f'<div class=card style="flex:1;margin-top:0;padding:20px 24px 22px 32px"><div class=lab>{lab}</div><div style="font-family:NSB;font-size:68px;margin-top:4px" class=g>{num}'
                f'<span style="font-size:26px;color:#9b9b9e;margin-left:6px">{unit}</span></div><p style="font-size:24px;color:#bdb8ae;line-height:1.5">{note}</p></div>')
    return f'<div style="display:flex;gap:18px;margin-top:22px">{one(*a)}{one(*b)}</div>'

page(D + 'p2.html', 2, f'''{T}{head('机电产品占出口近2/3', '2026年1–10月｜人民币计｜海关总署 11月10日发布')}
{grid(stat('全部出口', '25.99', '万亿元', '同比 <span class=gc>+17.6%</span>'),
      stat('机电产品', '16.81', '万亿元', '同比 <span class=gc>+25.2%</span>'),
      stat('机电占出口比重', '64.7%', '', '比去年同期 +3.9 个百分点'),
      stat('高新技术产品', '7.77', '万亿元', '同比 +41.6%｜和机电有交叉'))}
{it('<span class=k>机电产品</span>是什么', '机器、电器、电子产品及零部件，汽车、船舶也算。<br>每出口100元货物，约65元来自机电产品。')}
<table style="margin-top:22px"><tr class=h><td>机电里的大块头</td><td>出口额（亿元）</td><td>同比</td></tr>
<tr><td>集成电路</td><td>23,381</td><td>+101.9%</td></tr>
<tr><td>电脑及零部件</td><td>18,279</td><td>+53.6%</td></tr>
<tr><td>汽车（含底盘）</td><td>11,640</td><td>+45.8%</td></tr>
<tr><td>手机</td><td>7,353</td><td>+8.8%</td></tr>
</table>
{it('芯片：颗数只多<span class=k>3.2%</span>，金额多一倍', '平均每颗出口额从约3.96元涨到约7.74元（作者计算）。新华财经称AI相关产品「涨价效应突出」：10月芯片出口数量−2.4%，金额+125.7%。')}
<div class=src>来源：海关总署统计月报表（人民币）、新华社、新华财经 2026-11-10；标注处为作者计算</div>''', total=4)

page(D + 'p3.html', 3, f'''{T}{head('新三样是哪三样', '新三样＝电动载人汽车＋锂离子蓄电池＋太阳能电池')}
{duo(('「新三样」出口', '+46.5%', '', '前10个月同比｜海关数据'), ('工业机器人出口', '+17.8%', '', '前10个月同比｜排在第10名之后'))}
{it('<span class=k>新三样</span>和<span class=k>老三样</span>', '过去说外贸「老三样」，指服装、家具、家电；现在说「新三样」，指电动汽车、锂电池、光伏电池。后者技术更密集，增速也更快。')}
<table style="margin-top:22px"><tr class=h><td>汽车出口算笔账</td><td>去年1–10月</td><td>今年1–10月</td></tr>
<tr><td>数量（万辆）</td><td>651.0</td><td>973.6</td></tr>
<tr><td>金额（亿元）</td><td>7,982</td><td>11,640</td></tr>
<tr><td>平均每辆（万元）</td><td>约12.26</td><td>约11.96</td></tr></table>
{it('车卖得多，单价略低', '数量 +49.6%，金额 +45.8%：数量涨得比金额快，平均每辆出口额小幅下降（作者计算）。')}
{it('订单也在分化', '机电商会秋季广交会调研：订单增长的企业占40.7%，下降的占28.2%，都比春季多；新能源、光储充、储能订单较满，家电、工具、汽配、照明偏弱。')}
<div class=src>来源：新华社、海关总署统计月报表、新华财经 2026-11-10；单车均价为作者计算</div>''', total=4)

page(D + 'p4.html', 4, f'''{T}{head('劳密产品为啥只涨2.4%', '劳密产品＝劳动密集型产品，需要大量人手的商品｜人民币计')}
{duo(('劳密产品出口', '3.45', '万亿元', '同比 <span class=gc>+2.4%</span>'), ('农产品出口', '6220.8', '亿元', '同比 +3.9%'))}
<table style="margin-top:22px"><tr class=h><td>海关口径的7类劳密产品</td><td>出口额（亿元）</td><td>同比</td></tr>
<tr><td>服装</td><td>9,193</td><td>+1.6%</td></tr>
<tr><td>纺织品</td><td>8,610</td><td>+2.0%</td></tr>
<tr><td>塑料制品</td><td>6,752</td><td>+9.9%</td></tr>
<tr><td>家具</td><td>3,817</td><td>+2.7%</td></tr>
<tr><td>鞋靴</td><td>2,345</td><td>−5.3%</td></tr>
<tr><td>玩具</td><td>2,068</td><td>−3.2%</td></tr>
<tr><td>箱包</td><td>1,763</td><td>−1.1%</td></tr></table>
{it('<span class=k>①</span> 不是没卖，是没怎么涨', '7类合计约3.45万亿元，同比约+2.4%，和官方数一致（作者核算）。全部出口涨17.6%，劳密产品明显掉队。')}
{it('<span class=k>②</span> 专家怎么解释', '东方金诚冯琳：外需边际放缓，10月全球制造业PMI降至52.6%，箱包、服装、玩具增速普遍放缓。机电商会高士旺：传统品类增长贡献减弱，外部关税约束长期化。')}
<div class=src>来源：海关总署统计月报表、新京报转「海关发布」、新华财经、每日经济新闻 2026-11-10；合计为作者核算</div>''', total=4)
print('gen ok')
