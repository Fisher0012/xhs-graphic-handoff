#!/usr/bin/env python3
# 生成 p1-p4.html；数字全部读 ../data.json，文字照 02-框架.md（Fisher 2026-10-29 21:16 确认）
import json
from decimal import Decimal,ROUND_HALF_UP
D=json.load(open('../data.json')); B=D['banks']; T=D['total_yi']; Y5=D['y2025']
r1=lambda x:str(Decimal(str(x)).quantize(Decimal('0.1'),ROUND_HALF_UP))
RISK='风险提示：本文信息仅供参考，不构成任何投资建议。'
LABEL='<div class="label">一图看懂｜政策性金融</div>'
CALC='<span class="calc">（按官方数据计算）</span>'
def page(b): return f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body><div class="page">{LABEL}{b}<div class="risk">{RISK}</div></div></body></html>'
by={b['key']:b for b in B}
# 自算
share={b['key']:r1(b['amount_yi']/T*100) for b in B}
mult={b['key']:b['invest_wan_yi']*10000/b['amount_yi'] for b in B}
inv_sum=round(sum(b['invest_wan_yi'] for b in B),2)          # 11.59
m_sum=inv_sum*10000/T                                          # 14.49
m25=Y5['invest_wan_yi']*10000/Y5['total_yi']                   # 14.0
assert sum(b['amount_yi'] for b in B)==T
# ---------- P1 ----------
order=sorted(B,key=lambda b:-b['amount_yi'])
rows=''.join(f'<div class="brow" style="top:{486+i*150}px"><div class="top"><span class="name">{b["name"]}</span><span class="tag">占{share[b["key"]]}%</span>'
  f'<span class="num">{b["amount_yi"]}<small>亿元</small></span></div><div class="bar"><i style="width:{b["amount_yi"]/T*100:.2f}%"></i></div></div>' for i,b in enumerate(order))
p1=('<div class="title cover-title" id="ct"><div class="w">8000亿工具</div><div class="t">钱去了哪</div></div>'
 '<div class="gline" style="top:396px"></div>'
 '<div class="subtitle" style="top:416px">截至10月28日已全部投放 · 全部用于补充项目资本金</div>'
 f'{rows}'
 '<div class="subtitle" style="top:946px">进度条＝占8000亿元的比例'+CALC+'</div>'
 '<div class="kbox" style="top:1040px">'
 f'<div class="kl">三家对应的项目总投资合计约{inv_sum}万亿元'+CALC+'</div>'
 f'<div class="kv">每<em>1</em>元工具资金 <small>对应约</small> <em>{r1(m_sum)}</em><small>元项目总投资</small></div>'
 '<div class="kl" style="font-size:24px;color:var(--note)">三家口径不同，见第4页</div></div>')
# ---------- P2 ----------
cards=''
for i,k in enumerate(['cdb','eximbank','adbc']):
    b=by[k]
    rs=''.join(f'<div class="r"><span class="rl">{l}</span><span class="rv">{v}</span></div>' for l,v in b['dirs'])
    cards+=f'<div class="bcard" style="top:{318+i*300}px"><div class="hd"><span class="bn">{b["name"]}</span><span class="ba">投放<b>{b["amount_yi"]}</b>亿元</span></div>{rs}</div>'
p2=('<div class="title inner-title"><span class="w">钱</span><span class="t">去了哪</span></div>'
 '<div class="gline" style="top:252px"></div>'
 '<div class="subtitle" style="top:272px">三家分开说 · 官方按三个方向公布 · 三项有交叉，不能相加</div>'
 f'{cards}'
 '<div class="fn" style="top:1214px">新兴领域：人工智能、数字经济、绿色低碳、生物医药、低空经济、消费等，各行列举略有不同。民间投资：含民间资本参与项目。11个经济大省：原文为「11个经济体量较大省份」。</div>')
# ---------- P3 ----------
tab=('<div class="ctab" style="top:390px">'
 '<div class="tr th"><div class="c0"></div><div class="c1">项目资本金</div><div class="c2">贷款</div></div>'
 '<div class="tr"><div class="c0">是什么</div><div class="c1">投资者认缴的出资，即项目本钱</div><div class="c2">项目借来的钱</div></div>'
 '<div class="tr"><div class="c0">还本付息</div><div class="c1">不承担这部分的债务和利息</div><div class="c2">要按约定还本付息</div></div>'
 '<div class="tr"><div class="c0">算不算资本金</div><div class="c1">—</div><div class="c2">借贷资金不能算作资本金</div></div>'
 '<div class="tr"><div class="c0">比例要求</div><div class="c1">基础设施项目一般最低20%</div><div class="c2">银行审查资本金后决定贷多少</div></div>'
 '</div>')
mx=max(list(mult.values())+[m_sum,m25])
def mrow(name,tag,v,top,cls='',q='约'):
    return (f'<div class="mrow {cls}" style="top:{top}px"><div class="top"><span class="name">{name}</span><span class="tag">{tag}</span>'
            f'<span class="num"><small>{q}</small>{v}<small>元</small></span></div><div class="bar"><i style="width:{float(v)/mx*100:.2f}%"></i></div></div>')
# 进银：逾1.7万亿÷1200亿=14.17 → 写「超14.1」
m_ex=str(Decimal(str(mult['eximbank'])).quantize(Decimal('0.1'),rounding='ROUND_DOWN'))
mr=(mrow('国开行','5.5万亿 ÷ 3650亿',r1(mult['cdb']),918)
   +mrow('进出口银行','逾1.7万亿 ÷ 1200亿',m_ex,992,q='超')
   +mrow('农发行','约4.39万亿 ÷ 3150亿',r1(mult['adbc']),1066)
   +mrow('三家合计',f'约{inv_sum}万亿 ÷ 8000亿',r1(m_sum),1140,'sum')
   +mrow('2025年那轮','约7万亿 ÷ 5000亿',f'{m25:.0f}',1214,'old'))
p3=('<div class="title inner-title"><span class="w">资本金 ≠ </span><span class="t">贷款</span></div>'
 '<div class="gline" style="top:252px"></div>'
 '<div class="subtitle" style="top:272px">依据：国发〔2019〕26号 · 这8000亿全部用于补充项目资本金</div>'
 '<div class="ccl" style="top:318px">结论：这笔钱是给项目当<b>本钱</b>，不是借给项目的<b>贷款</b></div>'
 f'{tab}'
 '<div class="sech" style="top:792px"><span class="ht">1元工具资金，对应多少元项目总投资</span></div>'
 '<div class="subtitle" style="top:856px">按官方数据计算 · 项目总投资里也包括工具资金本身、其他资本金和贷款</div>'
 f'{mr}')
# ---------- P4 ----------
IT=[('「投完」指什么',['截至2026年10月28日，8000亿元全部完成投放','指资金已投放到项目，不代表项目已经建成']),
 ('项目总投资 ≠ 当年投资',['是所支持项目的总投资额，含工具资金、其他资本金和贷款','不宜和当年的固定资产投资直接比较']),
 ('「拉动」和「涉及」口径不同',['国开行、农发行：<b>涉及</b>项目总投资5.5万亿元、约4.39万亿元','进出口银行：<b>拉动</b>总投资逾1.7万亿元',f'封面约{r1(m_sum)}元是三个口径不同的数相加后按官方数据计算']),
 ('投向不能相加',['新兴领域、民间投资、11个经济大省三项有交叉','进出口银行只公布占比；农发行照原文写「投资金额」']),
 ('2025年那一轮',[f'{Y5["total_yi"]}亿元，支持{Y5["projects"]}项目，项目总投资约{Y5["invest_wan_yi"]}万亿元',f'今年比上年多{T-Y5["total_yi"]}亿元（按官方数据计算）'])]
items=''
for i,(h,ls) in enumerate(IT,1):
    items+=(f'<div class="item2"><div class="h"><span class="no2">{i}</span><span class="ht">{h}</span></div><ul>'+''.join(f'<li>{l}</li>' for l in ls)+'</ul></div>'
            +('<div class="sep"></div>' if i<len(IT) else ''))
p4=('<div class="title inner-title"><span class="w">这几个数</span><span class="t">要说明</span></div>'
 f'<div class="items p4sep" style="top:262px">{items}</div>'
 '<div class="src" id="src" style="top:1250px">来源：国家发展改革委；新华社（据国开行、进出口银行、农发行）；2026年政府工作报告；国发〔2019〕26号<br>数据截至2026年10月28日</div>')
for i,b in enumerate([p1,p2,p3,p4],1): open(f'p{i}.html','w').write(page(b))
print('share',share,'mult',{k:round(v,3) for k,v in mult.items()},'sum',inv_sum,round(m_sum,3),'m25',m25,'m_ex',m_ex)
