import sys, re
sys.path.insert(0, '/workspace/xhs/notes')
from heijin import *
from cover_gen import cover

D = '/workspace/xhs/notes/20261112-大号-公积金10城额度榜/03-design/'
SRC_COVER = '来源：10城公积金中心/政府官网通知（2026年2–8月发布），2026-11-12查｜作者按单人额度排序，同额并列'
# (城市, 副列, 单人基础最高额度万元, hl)
rows = [("苏州", "家庭 200", 150, 0), ("北京", "家庭 240", 120, 0), ("扬州*", "家庭 180", 108, 0),
        ("上海", "家庭 200", 100, 0), ("广州", "两人及以上 200", 100, 0), ("重庆*", "家庭 200", 100, 0),
        ("济南", "家庭 130", 90, 0), ("青岛", "双方申贷 130", 90, 0), ("成都", "双缴存 120", 80, 0), ("深圳", "共同申请 130", 70, 0)]
cover(D + 'p1.html', '一图看懂｜10城公积金最高能贷多少', '公积金贷款额度榜',
      '首套 · 一人缴存的「基础」最高额度 · 单位：万元', rows, '万', SRC_COVER, fmt='{:.0f}')
h = open(D + 'p1.html').read()
h = h.replace('</style>', 'h1{font-size:100px;letter-spacing:4px}.row{align-items:center;height:62px;padding-top:0}.rk svg{vertical-align:-2px}</style>', 1)
# 并列名次：上海/广州/重庆同为100万→并列第4；济南/青岛同为90万→并列第7
for a, b in (('05', '04'), ('06', '04'), ('08', '07')):
    h = h.replace(f'</span>{a}</div>', f'</span>{b}</div>', 1)
card = ('<div style="margin-top:14px;background:linear-gradient(90deg,#191612,#121113);border:1px solid #26232a;border-radius:14px;padding:14px 24px;font-size:24px;line-height:1.55;color:#bdb8ae">'
        '这是<b style="color:#e9b519">封顶额度</b>，不是你一定能贷到的钱｜叠满上浮后深圳最高 <b style="color:#e9b519">351万</b>，见内页<br>'
        '<span style="color:#8a8a8e;font-size:22px">*阶段性政策：扬州至2026-12-31；重庆2026年9月至2027年8月</span></div>')
h = re.sub(r'(</div>)(\s*<div class=foot>)', r'\1' + card + r'\2', h, count=1)
open(D + 'p1.html', 'w').write(h)

T = '<div class=tag>一图看懂｜10城公积金最高能贷多少</div>'
TOT = 5

def stat(lab, num, unit, note):
    return (f'<div class=card style="flex:1;margin-top:0;padding:20px 24px 22px 32px"><div class=lab>{lab}</div><div style="font-family:NSB;font-size:64px;margin-top:4px" class=g>{num}'
            f'<span style="font-size:26px;color:#9b9b9e;margin-left:6px">{unit}</span></div><p style="font-size:24px;color:#bdb8ae;line-height:1.5">{note}</p></div>')
duo = lambda a, b: f'<div style="display:flex;gap:18px;margin-top:22px">{stat(*a)}{stat(*b)}</div>'
def city(name, base, p):
    return (f'<div class=card><div class=lab>{name}<span style="color:#9b9b9e;font-family:NSM;font-size:22px;margin-left:12px">{base}</span></div>'
            f'<p style="font-size:25px;color:#bdb8ae;line-height:1.6;margin-top:6px">{p}</p></div>')

page(D + 'p2.html', 2, f'''{T}{head('叠满上浮最高能贷多少', '官方写明了合计上限的6城｜首套｜单位：万元')}
<table style="margin-top:20px"><tr class=h><td>城市</td><td>基础：单人 / 家庭</td><td>叠满：单人 / 家庭</td></tr>
<tr><td>深圳</td><td>70 / 130</td><td>189 / 351</td></tr>
<tr><td>北京</td><td>120 / 240</td><td>180 / 340</td></tr>
<tr><td>济南</td><td>90 / 130</td><td>170 / 240</td></tr>
<tr><td>青岛</td><td>90 / 130</td><td>160 / 240</td></tr>
<tr><td>重庆（多子女）*</td><td>100 / 200</td><td>120 / 240</td></tr>
<tr><td>成都（现房/拆迁）</td><td>80 / 120</td><td>96 / 144</td></tr></table>
{it('深圳：基础垫底，叠满能到<span class=k>2.7倍</span>', '买本市首套+60%，两孩及以上+70%（或初婚初育+50%，二选一），买保障房+40%，累加最多+170%：70万→189万，130万→351万。')}
{it('北京：直接<span class=k>加钱</span>', '城六区户籍去城六区外买首套+20万，绿色建筑+40万，本市户籍<span style="white-space:nowrap">多子女+40万</span>；叠加最多单人+60万、夫妻+100万。')}
<div class=src>来源：深圳市住建局、北京/济南公积金中心、山东省政府网、青岛西海岸新区政务网、重庆市政府、新华社（成都）｜北京叠满为作者计算（基础＋官方上浮上限）｜*重庆为阶段性额度</div>''', total=TOT)

page(D + 'p3.html', 3, f'''{T}{head('另外4城怎么往上加', '官方只写了上浮规则、没写合计上限，本文不替它算总数')}
{city('上海', '基础 单人100 / 家庭200', '缴补充公积金：单人+20万、家庭+40万。多子女+20%、二星及以上新建绿色建筑+15%，两项可叠加为+35%。')}
{city('广州', '基础 一人100 / 两人及以上200', '一孩+10%、二孩+40%、三孩及以上+50%；绿色/装配式建筑<span style="white-space:nowrap">+10%～20%</span>，「好房子」+30%（房屋类取最高）；两类可叠加。')}
{city('苏州', '基础 个人150 / 家庭200', '买现房+50%；二星及以上绿色建筑+20%、「两智一全」等<span style="white-space:nowrap">改善型住宅+50%</span>（两项取高）。现房和「好房子」两类可叠加。')}
{city('扬州*', '基础 单缴存108 / 双缴存180', '绿色建筑+20%～40%，改善型住宅+30%，「以旧换新」+30%，<span style="white-space:nowrap">认定人才最高放宽160万元</span>；与多子女政策均可叠加。')}
<div class=src>来源：上海市住建委2026-02-25、广州公积金中心穗公积金中心规字〔2026〕1号、苏州公积金中心苏房金〔2026〕24号、扬州公积金中心扬金管委〔2026〕2号｜*扬州阶段性政策至2026-12-31</div>''', total=TOT)

page(D + 'p4.html', 4, f'''{T}{head('同样贷100万差多少', '举例：贷100万元｜30年｜等额本息｜作者计算')}
{duo(('公积金 首套 2.6%', '4003', '元/月', '5年以上首套公积金利率'), ('商贷 约3.1%', '4270', '元/月', '9月新发放房贷平均利率'))}
<table style="margin-top:22px"><tr class=h><td>举例：100万 · 30年</td><td>公积金 2.6%</td><td>商贷 约3.1%</td></tr>
<tr><td>30年利息合计</td><td>约44.1万</td><td>约53.7万</td></tr>
<tr><td>30年本息合计</td><td>约144.1万</td><td>约153.7万</td></tr>
<tr><td>30年多付利息</td><td>—</td><td>约9.6万</td></tr></table>
{it('每月少还约<span class=k>267元</span>，30年少还约<span class=k>9.6万</span>', '前提是100万全部在公积金额度内；超出额度的部分只能另找商贷。以上为作者按等额本息公式计算的举例。')}
{it('利率从哪来', '首套公积金：5年以上2.6%、5年及以下2.1%；二套：3.075%、2.525%。3.1%是央行披露的9月全国新发放个人住房贷款利率（约数），个人实际利率以合同为准。')}
<div class=src>来源：中央国家机关住房资金管理中心2026-06-12、福州公积金中心2026-01-15、中国人民银行《2026年第三季度中国货币政策执行报告》2026-11-11；月供与利息为作者计算</div>''', total=TOT)

page(D + 'p5.html', 5, f'''{T}{head('能贷多少还看这三条', '最高额度只是封顶，以下为各地官方规则举例')}
{it('<span class=k>①</span> 账户余额倍数', '深圳：可贷额度＝公积金账户余额×16倍（夫妻合并计算）。青岛：倍数扩大到20倍，余额不足1万元按1万元算。')}
{it('<span class=k>②</span> 缴存年限', '北京：一人缴存，每缴存1年可贷20万元；夫妻都缴存，每年40万元，按<span style="white-space:nowrap">缴存年限</span>较长的一方算。举例：单人缴存3年，最多约60万元（作者计算）。')}
{it('<span class=k>③</span> 还款能力', '深圳：按等额本息算的月供，不超过缴存基数（夫妻合计）的50%。北京：实际贷款额度依据购房家庭还款能力确定。')}
<div class=card><div class=lab>申请前自查清单</div><p style="font-size:25px;color:#bdb8ae;line-height:1.75;margin-top:6px">□ 当地基础额度和自己符合哪几项上浮<br>□ 账户余额×当地倍数，算出余额上限<br>□ 缴存年限是否挂钩额度<br>□ 月供占缴存基数或收入的比例<br>□ 首套/二套认定，阶段性政策截止日</p></div>
<div class=src>来源：深圳市住房和建设局2026-05-21答问、青岛西海岸新区政务网<span style="white-space:nowrap">2026-05-09</span>解读、北京三部门通知<span style="white-space:nowrap">2026-08-07</span>；实际以当地公积金中心审批为准</div>''', total=TOT)
print('gen ok')
