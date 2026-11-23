#!/usr/bin/env python3
# 生成 p1-p4.html；数字全部读 ../../data.json，文字照 02-框架.md
import json
from decimal import Decimal,ROUND_HALF_UP
D=json.load(open('../../data.json'))
P=D['provinces']; N=D['national']
R=lambda v:int(Decimal(str(v)).quantize(Decimal('1'),ROUND_HALF_UP))   # 四舍五入到整数亿元
RISK='风险提示：本文信息仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。'
LABEL='<div class="label">一图看懂｜各省GDP</div>'
SC='<span class="tag-sc">【自算】</span>'
def page(b): return f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body><div class="page">{LABEL}{b}<div class="risk">{RISK}</div></div></body></html>'
g=lambda p:f"实际增长{p['real_growth_pct']:.1f}%"
# ---------- P1 封面 前十 ----------
NOTE1={'山东':'｜<em>新进10万亿</em>'}
mx=P[0]['gdp_2025_yi']; rows=[]
for p in P[:10]:
    i=p['rank_2025']
    rows.append(f'<div class="row c{" first" if i==1 else ""}" style="height:74px"><div class="idx">{i:02d}</div>'
      f'<div class="nm"><div class="name">{p["province"]}</div><div class="note">{g(p)}{NOTE1.get(p["province"],"")}</div></div>'
      f'<div class="num">{R(p["gdp_2025_yi"])}</div><div class="bar"><i style="width:{p["gdp_2025_yi"]/mx*100:.2f}%"></i></div></div>')
n10=sum(p['gdp_2025_yi']>=100000 for p in P); n1=sum(p['gdp_2025_yi']>=10000 for p in P)
p1=(f'<div class="title cover2" id="ct"><div class="w">2025年各省</div><div><span class="w">GDP</span><span class="t">前十</span></div></div>'
 '<div class="gline" style="top:396px"></div>'
 f'<div class="subtitle" style="top:414px">31个省区市｜单位：亿元｜初步核算｜全国{N["gdp_2025"]}亿元，实际增长{N["real_growth"]:.1f}%</div>'
 f'<div class="rows" style="top:466px">{"".join(rows)}</div>'
 '<div class="hr" style="top:1218px"></div>'
 f'<div class="summary" style="top:1230px"><b>{n10}</b>个省过10万亿，<b>{n1}</b>个省过万亿</div>')
# ---------- P2 第11–31 ----------
rest=P[10:]; mx2=rest[0]['gdp_2025_yi']
top_g=max(p['real_growth_pct'] for p in P); low_g=min(p['real_growth_pct'] for p in P)
def srow(p):
    gp=p['real_growth_pct']; t=g(p)
    if gp==top_g: t=f'<em>{t}｜增速最高</em>'
    elif gp==low_g: t=f'{t}｜增速最低'
    return (f'<div class="row s" style="height:72px"><div class="idx">{p["rank_2025"]}</div><div class="nm"><div class="name">{p["province"]}</div>'
            f'<div class="note">{t}</div></div><div class="num">{R(p["gdp_2025_yi"])}</div><div class="bar"><i style="width:{p["gdp_2025_yi"]/mx2*100:.2f}%"></i></div></div>')
L=''.join(srow(p) for p in rest[:11]); Rr=''.join(srow(p) for p in rest[11:])
hi=sorted(P,key=lambda p:-p['real_growth_pct'])
above=sum(p['real_growth_pct']>N['real_growth'] for p in P)
p2=('<div class="title inner-title"><span class="w">第11–31名 </span><span class="t">全名单</span></div>'
 '<div class="subtitle inner-sub">单位：亿元｜小字为实际增速｜进度条以第11名安徽为100%</div>'
 f'<div class="colL" style="top:316px">{L}</div><div class="vline" style="top:320px;height:784px"></div><div class="colR" style="top:316px">{Rr}</div>'
 '<div class="hr" style="top:1124px"></div>'
 f'<div class="summary" style="top:1136px">实际增速最高：西藏<b>7.0%</b>，最低：辽宁<b>3.7%</b>；<br>31个省区市中，{above}个高于全国5.0%</div>')
# ---------- P3 门槛与换位 ----------
by={p['province']:p for p in P}
def cnt(th,y): return sum(((p['gdp_2025_yi'] if y==25 else (p['gdp_2024_final_yi'] or 0)))>=th for p in P) + (1 if y==24 and th<=90000 and by['浙江']['gdp_2024_final_yi'] is None else 0)
c=[(cnt(100000,25),'10万亿以上',f'2024年{cnt(100000,24)}个｜新进：山东'),(cnt(50000,25),'5万亿以上',f'2024年{cnt(50000,24)}个｜新进：北京'),(cnt(10000,25),'1万亿以上',f'2024年{cnt(10000,24)}个｜没有变化')]
kc=''.join(f'<div class="kcard" style="top:{392+i*118}px"><div class="big2 {"t" if i<2 else "w"}">{a}个</div><div class="lab">{b}</div><div class="sm">{s}</div></div>' for i,(a,b,s) in enumerate(c))
cq,ln=by['重庆'],by['辽宁']; m3=max(cq['gdp_2025_yi'],ln['gdp_2025_yi'])
def crow(p): return (f'<div class="row" style="height:84px"><div class="idx">{p["rank_2025"]}</div><div class="nm"><div class="name">{p["province"]}</div>'
   f'<div class="note">2024年第{p["rank_2024_final_自算"]} → 2025年第{p["rank_2025"]}</div></div><div class="num">{R(p["gdp_2025_yi"])}</div><div class="bar"><i style="width:{p["gdp_2025_yi"]/m3*100:.2f}%"></i></div></div>')
d25=cq['gdp_2025_yi']-ln['gdp_2025_yi']; d24=ln['gdp_2024_final_yi']-cq['gdp_2024_final_yi']
same=sum(p['rank_change']==0 for p in P)
p3=('<div class="title inner-title"><span class="w">门槛与 </span><span class="t">换位</span></div>'
 '<div class="subtitle inner-sub">单位：亿元｜2025年初步核算 vs 2024年最终核实</div>'
 '<div class="sech" style="top:318px"><span class="no2">1</span><span class="ht">过门槛的省份</span></div>' + kc +
 '<div class="sepl" style="top:762px"></div>'
 '<div class="sech" style="top:792px"><span class="no2">2</span><span class="ht">唯一一处换位：重庆和辽宁</span></div>'
 f'<div class="rows" style="top:870px">{crow(cq)}{crow(ln)}</div>'
 f'<ul class="plain" style="top:1072px"><li>2025年重庆比辽宁多<b>{d25:.0f}亿元</b>；2024年是辽宁多{d24:.0f}亿元{SC}</li>'
 f'<li>其余<b>{same}个</b>省份位次和2024年相同</li><li>2024年位次按最终核实数排列{SC}，进度条以重庆为100%</li></ul>')
# ---------- P4 口径 ----------
NW=lambda s:f'<span class="nw">{s}</span>'
IT=[('2025年都是初步核算数',['31个省区市和全国的2025年数据均为<b>初步核算</b>','国家统计局年度最终核实一般在隔年1月前完成，届时可能修订']),
 ('2024年用的是最终核实数',['位次对比用各省2025年发布中注明的2024年<b>最终核实数</b>','可能与部分媒体榜单使用的2024年初步数不同','例：辽宁2024年初步数32612.7亿元，最终核实32540.8亿元']),
 ('增速是实际增速',['各省公布的是按不变价计算的<b>实际增速</b>，不是名义增速','图中GDP四舍五入到整数亿元，原始数见各地发布']),
 ('31省合计≠全国',[f'31个省区市合计{R(D["provinces_sum_自算"])}亿元{SC}，全国{N["gdp_2025"]}亿元',
   '地区数由各省核算，全国数由国家统计局单独核算','两者口径不同，不宜直接相加比较','本图只含31个省区市'])]
items='<div class="sep"></div>'.join(f'<div class="item2"><div class="h"><span class="no2">{i}</span><span class="ht">{h}</span></div><ul>'+''.join(f'<li>{x}</li>' for x in xs)+'</ul></div>' for i,(h,xs) in enumerate(IT,1))
p4=('<div class="title inner-title p4t"><span class="w">这几个数 </span><span class="t">要说明</span></div>'
 f'<div class="items p4sep" style="top:258px">{items}</div>'
 '<div class="src" id="src" style="top:1264px">来源：国家统计局，31个省区市统计局及政府新闻发布<br>2026年1月20日–30日发布</div>')
for i,b in enumerate([p1,p2,p3,p4],1): open(f'p{i}.html','w').write(page(b))
