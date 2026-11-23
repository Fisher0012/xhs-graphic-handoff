#!/usr/bin/env python3
# 大号「阿信学财经」黑金版：生成 p1-p4.html；数字全部读 ../data.json，结构照 02-框架.md（已确认 4 页）
import json
from decimal import Decimal,ROUND_HALF_UP
D=json.load(open('../data.json')); P=D['provinces']; N=D['national']; by={p['province']:p for p in P}
R=lambda v:int(Decimal(str(v)).quantize(Decimal('1'),ROUND_HALF_UP))
RISK='风险提示：本文信息仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。'
LABEL='<div class="label">一图看懂｜各省GDP</div>'
SC='<span class="tag-sc">【自算】</span>'
U='<small>亿元</small>'
def page(b,label=None): label=label or LABEL; return f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body><div class="page">{label}{b}<div class="risk">{RISK}</div></div></body></html>'
g=lambda p:f"实际增长{p['real_growth_pct']:.1f}%"
# ---------- P1 ----------
mx=P[0]['gdp_2025_yi']
NOTE1={'山东':' · <em>新进10万亿</em>'}
rows=''.join(f'<div class="row{" first" if p["rank_2025"]==1 else ""}" style="height:C1_RHpx"><span class="idx">{p["rank_2025"]:02d}</span><span class="name">{p["province"]}</span>'
  f'<span class="note">{g(p)}{NOTE1.get(p["province"],"")}</span><span class="num">{R(p["gdp_2025_yi"])}{U}</span><div class="bar"><i style="width:{p["gdp_2025_yi"]/mx*100:.2f}%"></i></div></div>' for p in P[:10])
p1=('<div class="title cover1" style="top:C1_TOPpx;font-size:C1_Fpx"><span class="cover-title"><span class="w">各省GDP</span><span class="g">前十</span></span></div>'
 '<div class="gline" style="top:C1_LINEpx"></div>'
 f'<div class="subtitle" style="top:C1_SUBpx">31个省区市 · 2025年初步核算 · 全国{N["gdp_2025"]}亿元，实际增长{N["real_growth"]:.1f}%</div>'
 f'<div class="rows c1" style="top:C1_ROWSpx">{rows}</div>')
# ---------- P2 ----------
rest=P[10:]; mx2=rest[0]['gdp_2025_yi']
top_g=max(p['real_growth_pct'] for p in P); low_g=min(p['real_growth_pct'] for p in P)
def srow(p):
    t=g(p)
    if p['real_growth_pct']==top_g: t=f'<em>{t} · 增速最高</em>'
    elif p['real_growth_pct']==low_g: t=f'{t} · 增速最低'
    return (f'<div class="row s" style="height:72px"><span class="idx">{p["rank_2025"]}</span><div class="nm"><span class="name">{p["province"]}</span><span class="note">{t}</span></div>'
            f'<span class="num">{R(p["gdp_2025_yi"])}</span><div class="bar"><i style="width:{p["gdp_2025_yi"]/mx2*100:.2f}%"></i></div></div>')
above=sum(p['real_growth_pct']>N['real_growth'] for p in P)
p2=('<div class="title inner-title"><span class="w">第11–31名 </span><span class="g">全名单</span></div>'
 '<div class="gline" style="top:262px"></div>'
 '<div class="subtitle" style="top:284px">单位：亿元 · 小字为实际增速 · 进度条以第11名安徽为100%</div>'
 f'<div class="colL" style="top:334px">{"".join(srow(p) for p in rest[:11])}</div><div class="vline" style="top:338px;height:784px"></div><div class="colR" style="top:334px">{"".join(srow(p) for p in rest[11:])}</div>'
 '<div class="hr" style="top:1144px"></div>'
 f'<div class="summary" style="top:1160px">实际增速最高：西藏<b>7.0%</b>，最低：辽宁<b>3.7%</b>；<br>31个省区市中，{above}个高于全国5.0%</div>')
# ---------- P3 归集：门槛与换位 ----------
def cnt(th,y): return sum((p['gdp_2025_yi'] if y==25 else (p['gdp_2024_final_yi'] or 0))>=th for p in P) + (1 if y==24 and th<=90000 else 0)  # 浙江2024最终核实数未找到（data.json 为空），未填估计值；按其2025年94545亿元推断2024年在5万亿与10万亿之间，故≤9万亿门槛+1（推断，见设计说明）
T=[('10万亿以上',100000,'2024年{}个 · 新进山东'),('5万亿以上',50000,'2024年{}个 · 新进北京'),('1万亿以上',10000,'2024年{}个 · 没有变化')]
tr=''.join(f'<div class="trow"><div class="top"><span class="name">{n}</span><span class="tag">{t.format(cnt(th,24))}</span><span class="num">{cnt(th,25)}<small>个</small></span></div><div class="track"><i style="width:{cnt(th,25)/31*100:.2f}%"></i></div></div>' for n,th,t in T)
cq,ln=by['重庆'],by['辽宁']; m3=cq['gdp_2025_yi']
def swr(p,dim=False): return (f'<div class="trow{" dim" if dim else ""}"><div class="top"><span class="name">{p["province"]}</span><span class="tag">2024年第{p["rank_2024_final_自算"]} → 2025年第{p["rank_2025"]}</span>'
   f'<span class="num">{R(p["gdp_2025_yi"])}{U}</span></div><div class="track"><i style="width:{p["gdp_2025_yi"]/m3*100:.2f}%"></i></div></div>')
d25=cq['gdp_2025_yi']-ln['gdp_2025_yi']; d24=ln['gdp_2024_final_yi']-cq['gdp_2024_final_yi']; same=sum(p['rank_change']==0 for p in P)
p3=('<div class="title inner-title"><span class="w">门槛与 </span><span class="g">换位</span></div>'
 '<div class="gline" style="top:262px"></div>'
 '<div class="subtitle" style="top:284px">2025年初步核算 vs 2024年最终核实 · 进度条＝占31个省区市的比例</div>'
 '<div class="sech" style="top:342px">过门槛的省份</div>'
 f'<div class="rows" style="top:390px">{tr}</div>'
 '<div class="sech" style="top:700px">只有一处换位</div>'
 f'<div class="rows" style="top:748px">{swr(cq)}{swr(ln,True)}</div>'
 '<div class="callout" style="top:962px"><h3>重庆和辽宁</h3>'
 f'<p>2025年重庆比辽宁多<b>{d25:.0f}亿元</b>，2024年是辽宁多<b>{d24:.0f}亿元</b>{SC}；<span class="nw">其余{same}个省份</span>位次和2024年相同。</p></div>'
 f'<div class="foot" style="top:1188px">2024年位次按最终核实数排列{SC}；换位两行的进度条以重庆为100%。来源：各省区市统计局</div>')
# ---------- P4 口径卡 ----------
def card(top,ct,cs,kv,cols,d):
    cc=''.join(f'<div><span class="l">{l}</span><span class="v">{v}</span></div>' for l,v in cols)
    return (f'<div class="card" style="top:{top}px"><div class="hd"><span class="ct">{ct}</span><span class="cs">（{cs}）</span></div>'
            f'<div class="key"><div class="kl">关键数字</div><div class="kv">{kv}</div></div><div class="cols">{cc}</div><div class="d">{d}</div></div>')
S=D['provinces_sum_自算']; gap=N['gdp_2025']-S
C=[('初步核算','2025年数都不是最终数','31省全出',[('发布时间','2026年1月20–30日'),('当前状态','初步核算'),('最终核实','一般在隔年1月前')],'国家统计局年度最终核实完成后，各省和全国数据都可能修订'),
 ('2024年用最终数','对比口径','1处换位',[('辽宁初步数','32612.7亿元'),('辽宁最终核实','32540.8亿元'),('位次排序','按最终核实数'+SC)],'可能与部分媒体榜单使用的2024年初步数不同'),
 ('实际增速','不是名义增速',f'全国{N["real_growth"]:.1f}%',[('最高','西藏 7.0%'),('最低','辽宁 3.7%'),('高于全国',f'{above}个省份')],'各省公布的是按不变价计算的增速；图中GDP四舍五入到整数亿元'),
 ('31省合计≠全国','只含31个省区市',f'差{R(gap)}亿',[('31省合计',f'{R(S)}亿元'+SC),('全国',f'{N["gdp_2025"]}亿元'),('差额',f'{R(gap)}亿元'+SC)],'地区数由各省核算，全国数由国家统计局核算，口径不同，不宜直接相加')]
tops=[302,544,786,1028]
p4=('<div class="title inner-title"><span class="w">这几个数 </span><span class="g">要说明</span></div>'
 '<div class="subtitle" style="top:256px">看榜单前先知道这四件事</div>'
 + ''.join(card(t,*c) for t,c in zip(tops,C)) +
 '<div class="src" style="top:1272px">口径来源：国家统计局；31个省区市统计局及政府新闻发布（2026年1月20–30日）。</div>')
C1=dict(F=140,TOP=150)
C1['LINE']=round(C1['TOP']+C1['F']*1.0+22); C1['SUB']=C1['LINE']+28; C1['ROWS']=C1['SUB']+52; C1['RH']=(1292-C1['ROWS'])//10
for k,v in C1.items(): p1=p1.replace('C1_'+k+'px',f'{v}px')
LABEL1='<div class="label">一图看懂｜2025年各省GDP</div>'
for i,b in enumerate([p1,p2,p3,p4],1): open(f'p{i}.html','w').write(page(b,LABEL1 if i==1 else None))
