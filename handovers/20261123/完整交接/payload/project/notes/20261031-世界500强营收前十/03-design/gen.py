import sys;sys.path.insert(0,'/workspace/xhs/notes');from heijin import *;from cover_gen import cover
T='<div class=tag>一图看懂｜全球大公司排行</div>'
S='来源：《财富》2026年世界500强排行榜（财富中文网/Fortune，2026-07-28发布），按2025财年营业收入排名'
D=[('亚马逊','美国',716924,77670),('沃尔玛','美国',713163,21893),('国家电网','中国',555371.4,11116.2),('联合健康','美国',447567,12056),('沙特阿美','沙特',445528.7,92785),('苹果','美国',416161,112010),('麦克森','美国',403430,4762),('Alphabet','美国',402836,132170),('CVS Health','美国',402067,1768),('中国石油','中国',401927,21159.2)]
R=[(n,c,r/100,0) for n,c,r,p in D]
cover('p1.html','一图看懂｜全球大公司排行','500强营收前十','《财富》世界500强2026年榜（2025财年） · 单位：亿美元 · 亚马逊首次登顶',R,'亿美元','来源：《财富》2026年世界500强排行榜',fmt='{:.0f}')
X='<style>td{padding:7px 0;font-size:28px}.it{margin-top:26px}.it h3{font-size:34px}.it p{font-size:25px;line-height:1.65}</style>'
P=lambda t: f'<p style="font-size:25px;line-height:1.7;color:#bdb8ae;margin-top:6px">{t}</p>'
ex=f'''<div class=card style="margin-top:8px;padding:20px 30px 22px 36px"><div class=lab>先看懂｜排的是什么</div>{P('按营业收入（卖了多少钱）排名，不是利润，也不是市值。前十里美国7家、中国2家、沙特1家。')}</div>'''
page('p2.html',2,ranking(R,'单位：亿美元｜2025财年营业收入｜中间为总部所在国家',S,T,'亚马逊第一，国家电网第三',ex,unit='亿美元',fmt='{:.0f}'))
page('p3.html',3,f'''{T}{head('亚马逊登顶，沃尔玛12连冠结束','2025财年两家营收都超过7000亿美元')}
{X}<table style="margin-top:4px"><tr class=h><td>2025财年</td><td>营收（亿美元）</td><td>利润（亿美元）</td></tr>{tr("亚马逊","7169.24","776.70",hl=True)}{tr("沃尔玛","7131.63","218.93")}</table>
{it('<span class=k>①</span> 只差约38亿美元','两家营收都超过7000亿美元，亚马逊比沃尔玛多约37.6亿美元，差距不到1%。')}
{it('<span class=k>②</span> 营收增长12%','《财富》称，亚马逊2025年营收增长12%，突破7000亿美元，成为榜单37年来第6家登顶的公司。')}
{it('<span class=k>③</span> 赚得也更多','亚马逊利润776.70亿美元，约为沃尔玛（218.93亿美元）的3.5倍。')}
<div class=src>{S}；差额、倍数为作者计算</div>''')
rows=''.join(tr(n,f'{r/100:.0f}',f'{p/100:.0f}',f'{p/r*100:.1f}%',hl=(n in('Alphabet','苹果','沙特阿美'))) for n,c,r,p in D)
page('p4.html',4,f'''{T}{head('营收大≠最赚钱','利润率＝利润÷营收，前十差距很大')}
{X}<table style="margin-top:4px"><tr class=h><td>公司</td><td>营收</td><td>利润</td><td>利润率</td></tr>{rows}</table>
{it('<span class=k>①</span> Alphabet全球最赚钱','营收排第8，利润1321.7亿美元为全榜第一，利润率约32.8%。')}
{it('<span class=k>②</span> 医药流通利润薄','CVS Health利润率约0.4%、麦克森约1.2%，与Alphabet相差约80倍。')}
<div class=src>单位：亿美元；利润率＝利润÷营收，作者计算。{S}</div>''')
page('p5.html',5,f'''{T}{head('前十都做什么？','科技、医疗、能源占了八席')}
{X}<table style="margin-top:4px"><tr class=h><td>主营方向（作者归类）</td><td>公司</td></tr>{tr("科技/互联网","亚马逊、苹果、Alphabet",hl=True)}{tr("医疗健康","联合健康、麦克森、CVS")}{tr("能源","沙特阿美、中国石油")}{tr("零售","沃尔玛")}{tr("电网","国家电网")}</table>
{it('<span class=k>①</span> 科技行业增长最快','《财富》统计，榜单38家科技企业营收增长超20%，约4万亿美元。Alphabet首次进入前十。')}
{it('<span class=k>②</span> 中国两家都是国企','国家电网继续排第三，中国石油排第十；伯克希尔（第11）、中国石化（第12）紧随其后。')}
{it('<span class=k>③</span> 美国与中国','美国141家上榜；中国（含台湾地区）122家，比去年少8家。')}
<div class=src>{S}；行业归类为作者按主营业务粗分</div>''')
page('p6.html',6,f'''{T}{head('这个榜该怎么读？','看营收、不看市值，4点要注意')}
{it('<span class=k>①</span> 看营收，不看市值','排名只看营业收入，不代表公司价值高低，也不代表股价表现。')}
{it('<span class=k>②</span> 财年不同','统计各公司截至2026年3月31日或之前结束的财年，财年起止时间并不统一。')}
{it('<span class=k>③</span> 前十有多大','前十营收合计约4.90万亿美元，占500家总营收（43.1万亿美元）约11%。')}
{it('<span class=k>④</span> 汇率也有影响','榜单统一以美元列示，非美元公司的名次也会受汇率变化影响。')}
<div class=src>{S}；合计与占比为作者计算</div>''')
