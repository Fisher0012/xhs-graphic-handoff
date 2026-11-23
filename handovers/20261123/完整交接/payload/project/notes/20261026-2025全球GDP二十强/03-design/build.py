#!/usr/bin/env python3
# 生成 p1-p4.html；数字全部读 ../data.json，文字照 02-框架.md；单位：亿美元（=十亿美元×10，取整）
import json
from decimal import Decimal,ROUND_HALF_UP
D=json.load(open('../data.json')); E=D['economies']; C=D['china_check']
Y=lambda bn:int((Decimal(str(bn))*10).quantize(Decimal('1'),ROUND_HALF_UP))
RISK='风险提示：本文信息仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。'
LABEL='<div class="label">一图看懂｜全球GDP</div>'
SC='<span class="tag-sc">【自算】</span>'
def page(b): return f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body><div class="page">{LABEL}{b}<div class="risk">{RISK}</div></div></body></html>'
share=lambda e:f"占全球{e['share_world_pct_自算']:.2f}%"
EXTRA={'IND':'｜财年口径','AUS':'｜世行数据排第15','MEX':'｜世行数据排第14'}
def row(e,mx,h,cls='c'):
    i=e['rank_imf_2025']
    return (f'<div class="row {cls}{" first" if i==1 else ""}" style="height:{h}px"><div class="idx">{i:02d}</div>'
      f'<div class="nm"><div class="name">{e["name"]}</div><div class="note">{share(e)}{EXTRA.get(e["iso3"],"")}</div></div>'
      f'<div class="num">{Y(e["gdp_2025_usd_bn"])}</div><div class="bar"><i style="width:{e["gdp_2025_usd_bn"]/mx*100:.2f}%"></i></div></div>')
W=D['imf']['world_2025_usd_bn']
# P1
mx=E[0]['gdp_2025_usd_bn']
us_cn=round((E[0]['gdp_2025_usd_bn']+E[1]['gdp_2025_usd_bn'])/W*100,1)
p1=('<div class="title cover2" id="ct"><div class="w">2025年全球</div><div><span class="w">GDP</span><span class="t">二十强</span></div></div>'
 '<div class="gline" style="top:396px"></div>'
 '<div class="subtitle" style="top:414px">现价美元｜单位：亿美元｜IMF 2026年10月版｜2025年为实际值</div>'
 f'<div class="rows" style="top:466px">{"".join(row(e,mx,74) for e in E[:10])}</div>'
 '<div class="hr" style="top:1218px"></div>'
 f'<div class="summary" style="top:1230px">美中合计占全球<b>{us_cn}%</b>{SC}；全球约{W/1000:.2f}万亿美元</div>')
# P2
mx2=E[10]['gdp_2025_usd_bn']
top20=round(sum(e['gdp_2025_usd_bn'] for e in E[:20])/W*100,1)
p2=('<div class="title inner-title"><span class="w">第11–20名</span></div>'
 '<div class="subtitle inner-sub">现价美元｜单位：亿美元｜进度条以第11名巴西为100%</div>'
 f'<div class="rows" style="top:330px">{"".join(row(e,mx2,80) for e in E[10:20])}</div>'
 '<div class="hr" style="top:1146px"></div>'
 f'<div class="summary" style="top:1160px">前20合计占全球<b>{top20}%</b>{SC}；<br>第21名波兰{Y(E[20]["gdp_2025_usd_bn"])}亿美元</div>')
# P3 名次变化
ch=[e for e in E[:20] if e['rank_imf_2024_same_edition_自算']!=e['rank_imf_2025']]
for e in ch: e['d']=e['rank_imf_2024_same_edition_自算']-e['rank_imf_2025']
ch.sort(key=lambda e:(-e['d'],e['rank_imf_2025']))
same=[e['name'] for e in E[:20] if e['rank_imf_2024_same_edition_自算']==e['rank_imf_2025']]
cr=''.join(f'<div class="crow{" dn" if e["d"]<0 else ""}"><span class="name">{e["name"]}</span><span class="tag">2024年第{e["rank_imf_2024_same_edition_自算"]} → 2025年第{e["rank_imf_2025"]}</span><span class="num">{"↑" if e["d"]>0 else "↓"}{abs(e["d"])}</span></div>' for e in ch)
p3=('<div class="title inner-title"><span class="w">名次 </span><span class="t">谁升谁降</span></div>'
 f'<div class="subtitle inner-sub">前20名｜2025年 vs 2024年｜同一版IMF数据｜名次变化为【自算】</div>'
 f'<div class="rows" style="top:318px">{cr}</div>'
 f'<div class="callout" style="top:{318+len(ch)*60+22}px"><p><b>名次不变：</b>{"、".join(same)}</p></div>'
 f'<div class="small" style="top:{318+len(ch)*60+22+174}px">美元计价的名次会受汇率变动影响；本页只列名次，不分析原因</div>')
# P4
NW=lambda s:f'<span class="nw">{s}</span>'
IT=[('IMF 2026年10月版',['IMF《世界经济展望》数据库，2026年10月13日发布','指标为<b>现价美元GDP</b>，未按购买力平价调整','该版中2025年为<b>实际值</b>，不是预测']),
 ('和世界银行对照',['世行WDI（2026年10月8日更新）前20名单与IMF相同','只有一处名次不同：世行墨西哥第14、澳大利亚第15']),
 ('中国的口径',[f'国家统计局：初步核算{C["nbs_gdp_2025_yi"]}亿元，公报年均汇率{C["nbs_avg_rate"]}',f'两者相除约{C["nbs_converted_usd_bn_自算"]/1000:.2f}万亿美元{SC}，与IMF一致',f'世行用年均汇率{C["wb_rate_PA_NUS_FCRF"]:.4f}折算，约{C["wb_usd_bn"]/1000:.2f}万亿美元']),
 ('其他',['印度按财年统计（2025年4月–2026年3月）','美元计价的名次受汇率影响','占比、名次变化为'+SC+'；数值四舍五入到整数亿美元'])]
items='<div class="sep"></div>'.join(f'<div class="item2"><div class="h"><span class="no2">{i}</span><span class="ht">{h}</span></div><ul>'+''.join(f'<li>{x}</li>' for x in xs)+'</ul></div>' for i,(h,xs) in enumerate(IT,1))
p4=('<div class="title inner-title p4t"><span class="w">这几个数 </span><span class="t">要说明</span></div>'
 f'<div class="items p4sep" style="top:258px">{items}</div>'
 '<div class="src" id="src" style="top:1264px">来源：IMF World Economic Outlook（2026年10月）、世界银行WDI、国家统计局<br>数据截至2026年10月26日查询</div>')
for i,b in enumerate([p1,p2,p3,p4],1): open(f'p{i}.html','w').write(page(b))
