import sys;sys.path.insert(0,'/workspace/xhs/notes');from heijin import *
T='<div class=tag>一图看懂｜全球银行排行</div>'
R=[("工商银行","ICBC · 中国",7.6458,1),("农业银行","ABC · 中国",6.9748,1),("建设银行","CCB · 中国",6.5241,1),("中国银行","BOC · 中国",5.4841,1),("摩根大通","JPMorgan · 美国",4.4249,0),("美国银行","Bank of America · 美国",3.4117,0),("法国巴黎银行","BNP Paribas · 法国",3.2793,0),("汇丰控股","HSBC · 英国",3.212,0),("法国农业信贷","Crédit Agricole · 法国",3.1489,0),("邮储银行","PSBC · 中国",2.671,0)]
ex='''<div class=card style="margin-top:8px;padding:20px 30px 22px 36px"><div class=lab>先看懂｜总资产</div><p style="font-size:25px;line-height:1.7;color:#bdb8ae;margin-top:6px">银行手里所有“家当”：发出去的贷款、买的债券、现金等。其中大部分是存款等借来的钱——工行总权益只占总资产的7.99%，所以总资产≠银行自己的钱。</p></div>'''
page('p2.html',2,ranking(R,'单位：万亿美元｜2025年末｜按期末汇率折算｜第11名三菱日联2.67万亿','来源：S&P Global 2026榜单（汇丰按2025年报3.23万亿）；工行2025年报',T,'总资产TOP10',ex))
page('p3.html',3,f'''{T}{head('中国的银行为什么这么大？','企业融资靠银行、客户多、大量买入政府债')}
<div class=card style="margin-top:22px;padding:20px 30px 22px 38px"><div class=lab>前10名合计（万亿美元）</div><div style="display:flex;justify-content:space-between;margin-top:10px;font-family:NSB;font-size:30px;white-space:nowrap"><span>中国5家 29.30<span style="color:#9b9b9e;font-size:22px">（62.6%）</span></span><span>欧洲3家 9.66<span style="color:#9b9b9e;font-size:22px">（20.6%）</span></span><span>美国2家 7.84<span style="color:#9b9b9e;font-size:22px">（16.8%）</span></span></div></div>
{it('<span class=k>①</span> 企业借钱主要靠银行','2025年末社会融资规模存量442.12万亿元，其中人民币贷款268.4万亿元，占60.7%；企业债券只占7.7%。钱大多经过银行，银行资产自然大。')}
{it('<span class=k>②</span> 客户基数大','工行有7.82亿个人客户、1470多万公司客户（标普引工行数据），存款多，能放的贷款和买的债券也多。')}
{it('<span class=k>③</span> 大量买入政府债','标普引晨星分析：2025年国有大行金融投资增长19%，是财政发力的主要资金渠道；同年政府债券余额增长17.1%。')}
{it('<span class=k>④</span> 汇率也有影响','2025年美元走弱，非美银行资产换成美元后“变大”；标普指出榜上12家美国银行无一上升。')}
<div class=src>来源：人民银行《2025年金融统计数据报告》；工行客户数、③④均引自S&P Global 2026榜单原文；占比为作者按榜单加总计算</div>''')
page('p4.html',4,f'''{T}{head('银行资产和GDP比一比','总资产是存量，GDP是一年的流量')}
<div class=sub>均用人民币计算，不受汇率影响</div>
<table style="margin-top:14px"><tr class=h><td>2025年</td><td>金额</td><td>相当于GDP</td></tr>
<tr><td>四大行总资产</td><td>186.25万亿元</td><td>1.33倍</td></tr>
<tr><td>工商银行一家</td><td>53.48万亿元</td><td>38%</td></tr>
<tr><td>全国银行业总资产</td><td>480.0万亿元</td><td>3.4倍</td></tr>
<tr><td>摩根大通+美国银行</td><td>7.84万亿美元</td><td>美国GDP的25%</td></tr></table>
{it('先看懂｜<span class=k>存量 vs 流量</span>','总资产是年底那一刻“攒下的家底”（存量）；GDP是一年里“新挣的”（流量）。好比拿存款余额和年收入比，能看量级，但不能说银行“比经济还大”。')}
{it('倍数高说明什么？','说明这个经济体的融资更依赖银行：2025年末中国社会融资规模存量中，人民币贷款占60.7%，企业债券占7.7%（人民银行）。')}
<div class=src>来源：四大行2025年报；中国银行2025年报（引银行业总资产）；国家统计局2025年统计公报（GDP 140.19万亿元）；美国BEA（GDP 30.86万亿美元）；倍数为作者计算</div>''')
page('p5.html',5,f'''{T}{head('资产最大≠赚得最多','规模和盈利要分开看')}
<table><tr class=h><td>2025年</td><td>总资产</td><td>净利润</td><td>利润/资产</td></tr>
{tr("工商银行","7.65万亿","530亿","0.69%")}{tr("摩根大通","4.42万亿","570亿","1.29%",hl=True)}{tr("汇丰控股","3.23万亿","231亿","0.72%")}</table>
<div class=sub style="font-size:21px;margin-top:6px">单位：美元；工行利润按标普同口径汇率折算；利润/资产＝净利润÷年末总资产，作者计算</div>
{it('先看懂｜<span class=k>ROA（资产回报率）</span>','净利润÷平均总资产，意思是每100元资产一年赚多少。工行年报ROA为0.72%，即每100元资产赚约7毛2。')}
{it('先看懂｜<span class=k>净息差</span>','利息净收入÷生息资产平均余额，就是“贷款收的利息减去存款付的利息”这道差价。四大行2025年为1.26%–1.34%，汇丰为1.59%。')}
{it('为什么中国大行赚得相对少？','主要差在息差：工行、农行净息差都从2024年的1.42%降到1.28%。息差越薄，同样一笔资产赚到的利息就越少。')}
<div class=src>来源：工行、农行、建行、中行、摩根大通10-K、汇丰2025年报；ROA、净息差定义见中国银行2025年报释义</div>''')
page('p6.html',6,f'''{T}{head('3句话看懂这张榜','规模、盈利、排名口径')}
{it('<span class=k>01</span> 规模：中国领先','前4名全是中国国有大行，工行蝉联第一。背后是“企业融资主要靠银行”的金融结构。')}
{it('<span class=k>02</span> 盈利：美国更强','摩根大通资产约为工行的58%，净利润却更高。大不等于赚得多，要看息差和收入结构。')}
{it('<span class=k>03</span> 排名：先看口径','排名受汇率、并购调整影响；第10、11名几乎持平，换个汇率顺序就可能互换。')}
<div class=card style="margin-top:40px"><div class=lab>本榜口径</div><p style="font-size:24px;line-height:1.75;color:#bdb8ae;margin-top:6px">标普按各行披露的总资产原值排名，未调整会计准则差异；非美元按期末汇率折算；多数为2025-12-31数据。</p></div>
<div class=sub style="margin-top:28px">你觉得银行该比“大”还是比“赚”？评论区聊聊</div>''')
