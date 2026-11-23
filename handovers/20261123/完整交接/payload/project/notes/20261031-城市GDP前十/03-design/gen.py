import sys;sys.path.insert(0,'/workspace/xhs/notes');from heijin import *;from cover_gen import cover
T='<div class=tag>一图看懂｜城市经济排行</div>'
S='来源：各市统计局2026年前三季度经济运行情况（初步核算）'
D=[('上海',43306.62,5.5,6.3),('北京',40468.4,5.2,5.3),('深圳',30250.85,6.0,8.4),('重庆',25711.51,4.3,5.2),('广州',24851,5.7,6.8),('苏州',21190.90,5.6,6.3),('成都',19421.9,5.0,6.6),('杭州',18128,5.2,7.3),('武汉',16714.43,5.6,7.6),('南京',14959.14,5.3,6.4)]
R4=[(c,f'可比+{r:.1f}% · 名义+{n:.1f}%',v/10000,0) for c,v,r,n in D]
cover('p1.html','一图看懂｜城市经济排行','全国城市GDP前十','2026年前三季度（1–9月） · 单位：万亿元 · 上海第一，深圳增速最快',R4,'万亿','来源：各市统计局初步核算；名义增速为作者计算',fmt='{:.2f}')
X='<style>td{padding:7px 0;font-size:28px}.it{margin-top:26px}.it h3{font-size:34px}.it p{font-size:25px;line-height:1.65}</style>'
P=lambda t: f'<p style="font-size:25px;line-height:1.7;color:#bdb8ae;margin-top:6px">{t}</p>'
ex=f'''<div class=card style="margin-top:8px;padding:20px 30px 22px 36px"><div class=lab>先看懂｜两个增速</div>{P('可比增速＝扣掉价格变化后的“实打实”增长，统计局公布的就是它；名义增速＝今年总量直接比去年总量，含价格因素。')}</div>'''
page('p2.html',2,ranking(R4,'单位：万亿元｜2026年1–9月地区生产总值｜括号外为统计局可比增速',S+'；名义增速为作者计算',T,'上海第一，深圳跑最快',ex,unit='万亿',fmt='{:.2f}'))
rows=''.join(tr(c,f'+{r:.1f}%',f'+{n:.1f}%',f'{n-r:.1f}',hl=(c=='深圳')) for c,v,r,n in D)
page('p3.html',3,f'''{T}{head('名义和可比增速差在哪？','差值大，说明价格也在涨')}
{X}<table style="margin-top:4px"><tr class=h><td>1–9月</td><td>可比增速</td><td>名义增速</td><td>差（百分点）</td></tr>{rows}</table>
{it('<span class=k>①</span> 差值大，说明价格也在涨','深圳名义+8.4%、可比+6.0%，差2.4个百分点；杭州、武汉差约2个点。北京两者几乎一样，只差0.1个点。')}
{it('<span class=k>②</span> 比“谁增长快”，看可比增速','名义增速里混着价格变化。城市之间比真实增长，用统计局公布的可比增速。')}
<div class=src>可比增速：各市统计局；名义增速＝今年前三季度GDP÷上年前三季度初次公布值−1，作者计算</div>''')
I=sorted([(c,v,round(v-v/(1+n/100))) for c,v,r,n in D],key=lambda x:-x[2])
B=[('上海',2585.45),('深圳',2354.41),('北京',2052.50),('广州',1585.35),('重庆',1262.15),('苏州',1260.69),('杭州',1228),('成都',1195.0),('武汉',1176.61),('南京',899.65)]
# p4 重排（Fisher 2026-10-31 21:12）：表格改为条形图，前三名金银铜；数据不变
mxB=B[0][1];bars=''
for i,(c,x) in enumerate(B):
    cr,rc,col,bar=rank_style(i)
    bars+=f'''<div style="display:flex;align-items:center;height:52px;margin-top:8px"><div style="width:92px;font-family:NSB;font-size:26px;color:{rc}">{i+1:02d}</div><div style="width:120px;font-family:NSB;font-size:36px;color:{col}">{c}</div>
<div style="flex:1;height:26px;position:relative"><div style="height:26px;border-radius:13px;width:{x/mxB*100:.1f}%;background:{bar}"></div></div><div style="width:150px;text-align:right;font-family:NSB;font-size:38px;color:{col}">{x:.0f}<span style="font-size:20px;color:#9b9b9e;margin-left:4px">亿</span></div></div>'''
Q=lambda h,t: f'<div class=it style="margin-top:34px"><h3 style="font-size:40px">{h}</h3><p style="font-size:26px;line-height:1.85;color:#9b9b9e;margin-top:12px">{t}</p></div>'
page('p4.html',4,f'''{T}{head('一年多出多少？深圳增量超北京','增量＝今年总量−去年总量')}
<div class=lab style="margin-top:22px;color:#9b9b9e;font-family:NSM">比上年同期多出（名义，亿元）</div><div>{bars}</div>
{Q('<span class=k>①</span> 只有三城多出2000亿元以上','上海、深圳、北京三城一年多出2000亿元以上，其余七城在900–1600亿元之间。')}
{Q('<span class=k>②</span> 总量第三，增量第二','深圳总量比北京少约1.02万亿元，但一年多出2354亿元，比北京多约302亿元。')}
<div class=src>增量＝2026年前三季度GDP−2025年前三季度初次公布值，作者计算（未考虑上年数据修订）</div>''')
page('p5.html',5,f'''{T}{head('为什么有的快、有的慢？','工业城和服务业城分化')}
{X}<table style="margin-top:4px"><tr class=h><td>可比增速</td><td>第二产业</td><td>第三产业</td></tr>
{tr("武汉","+10.3%","+3.3%",hl=True)}{tr("深圳","+7.3%","+5.4%",hl=True)}{tr("苏州","+7.3%","+4.3%",hl=True)}{tr("北京","+2.7%","+5.6%")}{tr("南京","+3.2%","+6.4%")}{tr("重庆","+1.7%","+5.8%")}</table>
{it('<span class=k>①</span> 电子制造拉动武汉、深圳、苏州','武汉计算机通信电子设备制造业增加值+98.2%；深圳规上工业+9.5%；苏州工业对经济增长贡献达58.5%。')}
{it('<span class=k>②</span> 北京、上海靠金融和信息服务','北京金融业+9.6%、信息服务业+8.4%；上海金融业+9.5%、信息服务业+8.9%。')}
{it('<span class=k>③</span> 重庆为什么偏慢','第二产业只增1.7%，规上工业+3.5%，可比增速4.3%，低于全国的4.6%。')}
<div class=src>{S}。均为统计局可比口径</div>''')
page('p6.html',6,f'''{T}{head('和“各省GDP榜”有啥不一样？','城市≠省，前三季度≠全年')}
{it('<span class=k>①</span> 城市≠省','北京、上海、重庆是直辖市，既是城市也是省级单位；深圳、苏州等是省内的城市，城市数据已包含在所属省份里。')}
{it('<span class=k>②</span> 前三季度≠全年','本榜是2026年1–9月累计，全年数据要到明年初公布，排名可能变化。')}
{it('<span class=k>③</span> 名义增速的基数','名义增速用的是上年前三季度初次公布值；若上年数据后来修订，结果会略有不同。')}
{it('<span class=k>④</span> 初步核算','各市数据均为初步核算，后续可能修订。')}
<div class=src>来源：各市统计局2026年前三季度经济运行情况</div>''')
