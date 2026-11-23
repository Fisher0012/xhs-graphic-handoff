import sys, re
sys.path.insert(0, '/workspace/xhs/notes')
from heijin import *
from cover_gen import cover

D = '/workspace/xhs/notes/20261112-大号-税种增速榜/03-design/'
SRC_COVER = '来源：财政部国库司 2026-10-23《2026年前三季度财政收支情况》｜作者按增速排序'

rows = [("证券交易印花税", "2391亿元·股票交易环节", 65.1, 1), ("印花税", "4121亿元·合计，含第1名", 31.1, 0),
        ("环境保护税", "248亿元", 18.8, 0), ("个人所得税", "13464亿元", 14.1, 0),
        ("进口环节税", "15171亿·进口增值税消费税", 12.7, 0), ("车辆购置税", "1702亿元", 12.2, 0),
        ("资源税", "2417亿元", 12.1, 0), ("企业所得税", "34832亿元", 7.1, 0),
        ("房产税", "3697亿元", 6.3, 0), ("国内增值税", "55416亿元·第一大税种", 6.0, 0)]
cover(D + 'p1.html', '一图看懂｜前三季度全国税收', '主要税种增速榜',
      '2026年1–9月 · 全国税收收入 · 同比增速 · 财政部10月23日发布', rows, '%', SRC_COVER, fmt='+{:.1f}')
h = open(D + 'p1.html').read()
h = h.replace('</style>', 'h1{font-size:112px;letter-spacing:4px}.nm{font-size:40px;width:310px}.row{align-items:center;height:62px;padding-top:0}.rk svg{vertical-align:-2px}</style>', 1)
card = ('<div style="margin-top:14px;background:linear-gradient(90deg,#191612,#121113);border:1px solid #26232a;border-radius:14px;padding:16px 24px;font-size:25px;color:#bdb8ae">'
        '全国税收 <b style="color:#e9b519">14.07万亿元</b>，同比 <b style="color:#e9b519">+6.1%</b>｜第1名是第2名的一部分，不能相加</div>')
h = re.sub(r'(</div>)(\s*<div class=foot>)', r'\1' + card + r'\2', h, count=1)
open(D + 'p1.html', 'w').write(h)

T = '<div class=tag>一图看懂｜前三季度全国税收</div>'

def duo(a, b):
    def one(lab, num, unit, note):
        return (f'<div class=card style="flex:1;margin-top:0;padding:20px 24px 22px 32px"><div class=lab>{lab}</div><div style="font-family:NSB;font-size:68px;margin-top:4px" class=g>{num}'
                f'<span style="font-size:26px;color:#9b9b9e;margin-left:6px">{unit}</span></div><p style="font-size:24px;color:#bdb8ae;line-height:1.5">{note}</p></div>')
    return f'<div style="display:flex;gap:18px;margin-top:22px">{one(*a)}{one(*b)}</div>'

def tcard(lab, big, p):
    return (f'<div class=card><div class=lab>{lab}</div>'
            f'<div style="font-family:NSB;font-size:44px;margin-top:6px;color:#fff">{big}</div>'
            f'<p style="font-size:25px;color:#bdb8ae;margin-top:8px;line-height:1.65">{p}</p></div>')

page(D + 'p2.html', 2, f'''{T}{head('哪些收入在下降', '前三季度｜同比下降的税种，外加一项「不是税」的土地收入')}
<table style="margin-top:22px"><tr class=h><td>同比下降的税种</td><td>金额（亿元）</td><td>同比</td></tr>
<tr><td>契税</td><td>2,884</td><td>−14.5%</td></tr>
<tr><td>土地增值税</td><td>2,818</td><td>−14.5%</td></tr>
<tr><td>耕地占用税</td><td>1,059</td><td>−6.2%</td></tr>
<tr><td>国内消费税</td><td>12,402</td><td>−4.1%</td></tr>
<tr><td>车船税等其他税</td><td>958</td><td>−0.8%</td></tr>
<tr><td>关税</td><td>1,741</td><td>−0.5%</td></tr>
</table>
{it('<span class=k>契税</span>和<span class=k>土地增值税</span>是什么', '契税：买房、受让土地的一方交。土地增值税：转让房地产的增值部分要交，主要由房企缴纳。两项合计5,702亿元，比去年同期约少967亿元（作者计算）。')}
{tcard('口径说明｜这一项不是税', '国有土地使用权出让收入 <span class=gc>16,087</span><span style="font-size:24px;color:#9b9b9e">亿元</span> <span class=gc>−27.9%</span>',
       '属于「政府性基金预算」，和上面的税收分开统计，不放进税种排名比较。比去年同期约少6,225亿元（作者计算）。')}
<div class=src>来源：财政部国库司《2026年前三季度财政收支情况》2026-10-23；契税、土地增值税说明据《契税法》等；标注处为作者计算</div>''', total=4)

page(D + 'p3.html', 3, f'''{T}{head('个税涨14.1%，官方说法', '只摘官方原话，不做额外推断')}
{duo(('个人所得税', '13,464', '亿元', '前三季度 同比 <span class=gc>+14.1%</span>'), ('全国税收', '14.07', '万亿元', '同比 +6.1%<br>个税约占9.6%（作者计算）'))}
{it('<span class=k>①</span> 财政部发布会（10月23日）', '「价格上行、股市活跃、外贸增势强劲等因素也有力支撑了财政收入增长。」<br>这句说的是财政收入整体，发布会没有单独解读个税。')}
{it('<span class=k>②</span> 税务总局官网（6月10日，1—5月数据）', '个税增长较快「主要有三个原因：一是资本市场活跃带动相关所得项目高速增长；二是部分行业缴税增长较快；三是税务机关持续加强高收入人员纳税引导规范带来增收。」')}
{it('<span class=k>③</span> 同一篇还提到', '「资本市场活跃对个人所得税增长的贡献度近五成」；2025年度汇算截至5月底，「超过1.1亿人办理了退税」，退税规模同比增加超过17%。')}
<div class=src>来源：财政部 2026-10-23 前三季度财政收支情况新闻发布会文字实录；国家税务总局官网 2026-06-10（税收科学研究所所长黄立新）；占比为作者计算</div>''', total=4)

page(D + 'p4.html', 4, f'''{T}{head('和你有关的3个税', '谁交、怎么算｜粗口径，具体以当地税务机关为准')}
{tcard('个人所得税｜前三季度 +14.1%', '工资：单位每月先预扣预缴',
       '需要汇算的，次年3月1日—6月30日办理。应纳税所得额＝年收入额−6万元−专项扣除（三险一金等）−专项附加扣除−其他扣除，税率3%—45%。')}
{tcard('契税｜前三季度 −14.5%', '买房：买方在办登记前交',
       '法定税率3%—5%。个人买家庭唯一住房或第二套住房，140㎡及以下减按1%；140㎡以上，唯一住房1.5%、第二套2%。')}
{tcard('车辆购置税｜前三季度 +12.2%', '买车：税率10%，按不含增值税价算',
       '2026—2027年新能源车减半征收，每辆新能源乘用车最多减1.5万元。')}
<table style="margin-top:22px"><tr class=h><td>新能源乘用车 算笔账</td><td>车价30万元</td><td>车价50万元</td></tr>
<tr><td>按10%应纳</td><td>3万元</td><td>5万元</td></tr>
<tr><td>减半，最多减1.5万</td><td>−1.5万元</td><td>−1.5万元</td></tr>
<tr><td>实际要交</td><td>1.5万元</td><td>3.5万元</td></tr></table>
<div class=src>来源：《个人所得税法》《契税法》《车辆购置税法》；财政部等公告2024年第16号、2023年第10号；算例来自税务总局政策解读（车价为不含增值税价）</div>''', total=4)
print('gen ok')
