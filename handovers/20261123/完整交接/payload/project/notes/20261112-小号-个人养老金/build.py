import sys;sys.path.insert(0,'/workspace/xhs/tools');import xhlib
from xhlib import *
D='/workspace/xhs/notes/20261112-小号-个人养老金'
xhlib.EXTRA+='''
.co,.kc,.wcard{position:relative}
.ibody>*{flex-shrink:0}
.kg3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.kg3 .kc{padding:26px 22px}
.kg3 .k{font-size:62px}
.kg3 .l{font-size:26px;color:#d0d5d8;font-weight:700}
.kg3 .s2{font-size:21px;color:var(--note);margin-top:6px;white-space:nowrap}
.kc.hot .k{color:var(--teal-hi)}
.big1{font-size:30px;color:var(--sum);line-height:1.5}
.tbl{width:100%;border-collapse:collapse}
.tbl th{font-size:24px;color:var(--note);font-weight:400;text-align:right;padding:0 0 14px;white-space:nowrap}
.tbl th:first-child{text-align:left}
.tbl td{border-top:1px solid var(--sep);padding:12px 0;text-align:right;white-space:nowrap;font-size:34px;color:#c9cfd2;font-family:"Noto Sans SC";font-weight:500}
.tbl td:first-child{text-align:left;font-weight:700;color:#fff;font-size:36px}
.tbl td:first-child small{font-size:22px;color:var(--note);font-weight:400;margin-left:12px}
.tbl td.net{font-weight:900;font-size:42px;color:var(--teal-hi)}
.tbl tr.lo td.net{color:#e0a38f}
.tbl tr.lo td:first-child{color:#e0a38f}
.tl{position:relative;padding-left:58px}
.tl:before{content:"";position:absolute;left:21px;top:20px;bottom:20px;width:3px;background:#1f3a36}
.st{position:relative;margin-bottom:0}
.st .dot{position:absolute;left:-58px;top:2px;width:44px;height:44px;border-radius:50%;background:var(--teal);color:#041010;font-family:"Noto Sans SC";font-weight:900;font-size:26px;line-height:44px;text-align:center}
.st .when{font-size:26px;color:var(--teal);font-weight:700;white-space:nowrap}
.st .what{font-size:40px;font-weight:700;color:#fff;white-space:nowrap;line-height:1.3}
.st ul{list-style:none;margin-top:6px}
.st li{position:relative;padding-left:26px;font-size:29px;line-height:1.55;color:#b9c0c4}
.st li:before{content:"";position:absolute;left:4px;top:19px;width:8px;height:8px;border-radius:50%;background:#4a6a64}
.st li b{color:#e8ecee}
.wcard{background:var(--card);border:1px solid var(--card-bd);border-radius:16px;padding:22px 28px 22px 34px;position:relative;overflow:hidden}
.wcard:before{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;background:#e0a38f}
.wcard .h{font-size:40px;font-weight:900;color:#fff;white-space:nowrap}
.wcard .h em{font-style:normal;color:#e0a38f;margin-right:14px}
.wcard p{font-size:29px;line-height:1.55;color:#c2c8cc;margin-top:8px}
.wcard p b{color:#fff}
.wcard p .x{font-size:23px;color:var(--note)}
.prev{display:flex;gap:16px}
.prev div{flex:1;background:#0c1416;border:1px solid #1d2b2c;border-radius:12px;padding:16px 18px;font-size:27px;color:#d6dbde;white-space:nowrap;font-weight:700}
.prev div i{font-style:normal;color:var(--teal);margin-right:8px;font-family:"Noto Sans SC";font-weight:900}
.cs1{font-size:24px;color:var(--note);white-space:nowrap}
'''
# ---- 封面
p0=f'''<div class="title cover2"><div class="w">开户超1.5亿</div><div class="t">户均不到1000块</div></div>
<div class="subtitle" style="top:398px">个人养老金 · 截至2025年末 · 今年1.2万元额度12月31日清零</div>
<div style="position:absolute;left:0;right:0;top:478px;bottom:150px;display:flex;flex-direction:column;justify-content:space-between">
<div class="kg3">
 <div class="kc"><div class="k"><small style="margin:0 4px 0 0">超</small>1.5<small>亿</small></div><div class="l">个人养老金账户</div><div class="s2">媒体报道</div></div>
 <div class="kc"><div class="k">1452<small>亿</small></div><div class="l">累计缴存</div><div class="s2">老龄事业发展公报</div></div>
 <div class="kc hot"><div class="k">≈968<small>元</small></div><div class="l">平均每户</div><div class="s2">作者计算</div></div>
</div>
<div class="co"><p>1452亿 ÷ 1.5亿户 ≈ <b>968元</b><br>账户数是“超过1.5亿”，真实户均只会更低<br>多数账户<b>开了户、没存钱</b></p></div>
<div class="co"><p>每年<b>1.2万元</b>税前扣除额度<b>当年有效</b><br>不滚存、不累计，今年没存，明年不能补扣</p></div>
<div><div class="cs1" style="margin-bottom:16px">这篇只算税，帮你判断今年要不要存</div>
<div class="prev"><div><i>①</i>按税率档算账</div><div><i>②</i>最晚怎么存</div><div><i>③</i>谁可能不划算</div></div></div>
</div>'''
rows=[('不交个税','收入没到起征点',0,'lo'),('3%档','应纳税所得额≤3.6万',3,'lo'),('10%档','3.6万–14.4万',10,''),('20%档','14.4万–30万',20,''),('25%档','30万–42万',25,''),('30%档','42万–66万',30,''),('35%档','66万–96万',35,''),('45%档','96万以上',45,'')]
tr=''
for n,s,r,c in rows:
    g=12000*r//100; net=g-360
    ns=('+' if net>0 else ('−' if net<0 else ''))+f'{abs(net):,}'
    tr+=f'<tr class="{c}"><td>{n}<small>{s}</small></td><td>{g:,}</td><td>−360</td><td class="net">{ns}</td></tr>'
p1=inner('按税率档算一笔账','举例：今年存满12000元 · 只算税、未计投资收益（作者计算）',[
 f'<table class="tbl"><tr><th>你的税率档</th><th>现在少交</th><th>领取时交3%</th><th>净省</th></tr>{tr}</table>',
 co('净省 = 12000 × 税率 − 12000 × 3%<br><b>3%档净省≈0，不交个税的人还倒贴360元</b>'),
 '<div class="srcl">应纳税所得额 = 全年收入 − 6万 − 五险一金个人部分 − 专项附加扣除等<br>存完若跨到更低一档，实际少交的会比表里少，以年度汇算为准</div>'])
st=[('1','现在 – 12月31日','把钱存进个人养老金资金账户',['可按月、分次存，<b>不用一次存满</b>','12月是办理高峰，<b>别拖到最后几天</b>']),
    ('2','12月31日','今年的1.2万元额度到期',['当年有效，<b>不滚存、不累计</b>','今年没存，明年汇算不能补扣今年额度']),
    ('3','存钱的次月8日起（通常）','缴费凭证生成',['到“个人所得税”App填报扣除信息','扫码或按提示录入凭证']),
    ('4','两种扣法选一种','当年扣，或明年汇算时扣',['当年：把凭证交给单位，按月预扣时扣','明年：<b>3月1日–6月30日</b>年度汇算时扣'])]
tl='<div class="tl" style="display:flex;flex-direction:column;justify-content:space-between;height:100%">'+''.join(f'<div class="st"><div class="dot">{a}</div><div class="when">{b}</div><div class="what">{c}</div><ul>{"".join(f"<li>{x}</li>" for x in d)}</ul></div>' for a,b,c,d in st)+'</div>'
p2=f'<div class="title it1"><span class="w">今年最晚怎么存</span></div><div class="isub">时间线 · 以开户银行和个税App实际显示为准</div><div style="position:absolute;left:0;right:0;top:330px;bottom:250px">{tl}</div><div class="srcl" style="position:absolute;left:0;right:0;top:1218px">来源：广州市社保中心提示（广州日报2026-11-05）；个人所得税法第十一条；<br>财政部 税务总局公告2024年第21号</div>'
p3=inner('这3类人先别急着存','不是人人都划算 · 存之前先对照一下',[
 '<div class="wcard"><div class="h"><em>01</em>不交个税、或在3%档</div><p>少交的税 ≈ 领取时要交的3%，<b>净省约0元</b><br>不交个税的人存1.2万，将来还要<b>倒交360元</b><br><span class="x">举例：月薪1万、五险一金个人约2000元/月、无专项附加扣除，应纳税所得额约<span class="nw">3.6万</span>，正好在3%档上限</span></p></div>',
 '<div class="wcard"><div class="h"><em>02</em>近几年就要用这笔钱</div><p>钱<b>基本锁到退休</b>才能领。提前领只限完全丧失劳动能力、出国（境）定居、大额医疗自付、领失业金满12个月、领低保等情形</p></div>',
 '<div class="wcard"><div class="h"><em>03</em>存完会掉到更低一档</div><p>扣掉1.2万后应纳税所得额跨到低一档的，实际少交的税会比按原税率算的少，以年度汇算结果为准</p></div>',
 co('领取时<b>本金和收益都按3%交税</b>；账户里买不买产品、买什么由自己决定，<b>本文不推荐任何产品</b>')])
p4=inner('这几个数要说明','口径和来源',[
 blk(hd('1.5亿是媒体报道的数')+klist(['账户数来自中国证券网2026-11-03报道，<b>没查到官方原文</b>','原文说法是“超过1.5亿”，所以户均写“不到1000元”']),'kblk'),
 blk(hd('户均968元是作者计算')+klist(['1452亿 ÷ 1.5亿 ≈ 968元，含大量没存钱的账户','1452亿是<b>累计缴存额</b>，不是账户余额']),'kblk'),
 blk(hd('3%和1.2万怎么来的')+klist(['财政部 税务总局公告2024年第21号','截至11月12日，没查到调整3%的官方公告']),'kblk'),
 blk(hd('算账的假设')+klist(['净省 = 12000×税率 − 12000×3%','未计投资收益、跨档影响和时间价值']),'kblk'),
 '<div class="srcl">来源：民政部、全国老龄办《2025年度国家老龄事业发展公报》；中国证券网；<br>人社部发〔2025〕39号；广州市社保中心；整理：阿信财读笔记</div>'])
build(D,'个人养老金',[p0,p1,p2,p3,p4],['00_封面','01_按税率档算账','02_今年最晚怎么存','03_哪些人可能不划算','04_口径说明'])
