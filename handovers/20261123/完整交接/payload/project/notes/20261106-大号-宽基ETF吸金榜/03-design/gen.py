import sys
sys.path.insert(0, '/workspace/xhs/notes')
from heijin import *

T = '<div class=tag>一图看懂｜ETF资金流向</div>'

page('p2.html', 2, f'''{T}{head('钱进了哪一层', '22个交易日净流入｜单位：亿元｜层层收窄看结构')}
<div class=card style="margin-top:18px;padding:22px 30px 24px 36px"><div class=lab>① 股票型 ETF</div>
<div style="font-family:NSB;font-size:52px;margin-top:8px" class=g>约 5560<span style="font-size:26px;color:#9b9b9e;margin-left:8px">亿元</span></div>
<p style="font-size:26px;color:#bdb8ae;margin-top:8px;line-height:1.6">连续净流入合计（媒体转 Wind）</p></div>
<div class=card style="margin-top:18px;padding:22px 30px 24px 36px"><div class=lab>② 其中 · 宽基 ETF</div>
<div style="font-family:NSB;font-size:52px;margin-top:8px" class=g>5389.04<span style="font-size:26px;color:#9b9b9e;margin-left:8px">亿元</span></div>
<p style="font-size:26px;color:#bdb8ae;margin-top:8px;line-height:1.6">约占股票型 ETF 的 <span class=gc>96.9%</span>（作者计算：5389.04÷5560）</p></div>
<div class=card style="margin-top:18px;padding:22px 30px 24px 36px"><div class=lab>③ 7 大核心宽基</div>
<div style="font-family:NSB;font-size:52px;margin-top:8px" class=g>4999.44<span style="font-size:26px;color:#9b9b9e;margin-left:8px">亿元</span></div>
<p style="font-size:26px;color:#bdb8ae;margin-top:8px;line-height:1.6">约占宽基的 <span class=gc>92.8%</span>（作者计算）；沪深300 一类约占 7 大的 <span class=gc>41.8%</span>（作者计算：2088.22÷4999.44）</p></div>
{it('先看懂｜<span class=k>净流入</span>','申购减赎回后的资金净增加，不是指数涨跌幅，也不等于你账户盈亏。')}
<div class=src>来源：Wind（券商中国/第一财经转证券时报）；占比为作者计算</div>''', total=4)

page('p3.html', 3, f'''{T}{head('宽基ETF是什么', '按指数类别看资金，不点名任何具体产品')}
{it('<span class=k>①</span> 宽基是什么','覆盖面较宽的市场指数，比如沪深300、中证500。相对「单一行业/主题」指数，它更偏整体市场切片。')}
{it('<span class=k>②</span> ETF是什么','在交易所上市交易、通常跟踪某一指数的基金。本篇只按「挂钩哪条指数」合计净流入，不列基金代码、不点名公司。')}
{it('<span class=k>③</span> 本榜7个怎么理解','大盘代表：上证50、沪深300；中盘：中证500、中证A500；小盘：中证1000；偏成长风格常见代表：科创50、创业板指。分类只为好记，不是官方评级或投资建议。')}
<div class=card style="margin-top:28px"><div class=lab>重要提醒</div><p style="font-size:27px;line-height:1.75;color:#bdb8ae;margin-top:8px">看懂资金流向 ≠ 判断该买谁。涨跌、估值、自身风险承受能力，本篇都不评价。</p></div>
<div class=src>概念为财经通识表述；净流入数字来自上述 Wind 转引，查阅 2026-11-06</div>''', total=4)

page('p4.html', 4, f'''{T}{head('22天里发生了什么', '区间事实｜单日峰值口径｜三句话带走')}
{it('<span class=k>·</span> 连续22个交易日','2026-09-28 至 11-03，股票型 ETF 连续净流入合计约 5560 亿元。')}
{it('<span class=k>·</span> 宽基很集中','宽基合计 5389.04 亿；其中 7 大核心宽基 4999.44 亿。')}
{it('<span class=k>·</span> 11-03 单日峰值','股票 ETF 净流入 <span class=k>837.59</span> 亿元，为年内新高。')}
<div class=card style="margin-top:22px;padding:22px 30px 24px 36px"><div class=lab>口径注意</div><p style="font-size:26px;line-height:1.7;color:#bdb8ae;margin-top:8px">单日峰值以 Wind <b style="color:#e9b519;font-weight:normal">股票ETF合计口径 837.59 亿元</b>为准（不用文中另见的 845.34）。</p></div>
<div style="margin-top:28px" class=lab>三句话带走</div>
{it('<span class=k>01</span> 钱主要进了宽基','且高度集中在 7 大核心指数类别（结构见第2页）。')}
{it('<span class=k>02</span> 沪深300 一类领先','挂钩沪深300 的 ETF 合计净流入 2088.22 亿，明显居首。')}
{it('<span class=k>03</span> 先分清两个概念','「净流入」≠「涨跌」；本篇只摆资金事实，不评价该不该买。')}
<div class=src>来源：Wind（券商中国/第一财经转证券时报）；查阅 2026-11-06</div>''', total=4)

print('gen.py pages written')
