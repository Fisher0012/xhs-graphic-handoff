import json
# (省, 2025亿元, 实际增速, 发布日期, 来源URL, 核验等级, 2024最终核实, 2024值核验)
P=[
("广东",145846.76,3.9,"2026-01-30","http://stats.gd.gov.cn/tjkx185/content/post_4850449.html","L2",141488.86,"官方页摘要"),
("江苏",142351.5,5.3,"2026-01-28","https://tj.jiangsu.gov.cn/art/2026/1/28/art_87595_11722712.html","L1",136696.9,"官方页"),
("山东",103197.0,5.5,"2026-01-23","http://tjj.shandong.gov.cn/art/2026/1/23/art_6109_10322052.html","L1",98407.0,"官方页"),
("浙江",94545.0,5.5,"2026-01-21","https://zjic.zj.gov.cn/ywdh/jjyx/202601/t20260122_23914311.shtml","L3",None,"未找到"),
("四川",67665.3,5.5,"2026-01-21","https://cbgc.scol.com.cn/news/7387717","L3",64537.85,"摘要待核"),
("河南",66632.79,5.6,"2026-01-21","https://dzb.henandaily.cn/html5/2026-04/16/content_15_1789157.htm","L3",63557.10,"政府网转载"),
("湖北",62660.90,5.5,"2026-01-23","https://tjj.hubei.gov.cn/tjsj/tjfx/qstjfx/202601/t20260123_5862737.shtml","L1",59644.31,"官方页"),
("福建",60199.45,5.0,"2026-01-23","https://tjj.fujian.gov.cn/xxgk/jdsj/202601/t20260123_7084352.htm","L1",57476.58,"官方页"),
("上海",56708.71,5.4,"2026-01-20","https://tjj.sh.gov.cn/tjxw/20260120/d3f4918a77484c77bed173db6aaef33c.html","L1",53759.53,"官方页"),
("湖南",55308.65,4.8,"2026-01-26","http://tjj.hunan.gov.cn/hntj/tjfx/jmxx/2026sjjd/202601/t20260126_33902175.html","L1",53084.70,"摘要待核"),
("安徽",52989.0,5.5,"2026-01-23","http://fbh.anhuinews.com/fbh/202601/t20260123_9053822.html","L3",50647.0,"摘要待核"),
("北京",52073.4,5.4,"2026-01-21","https://tjj.beijing.gov.cn/zxfbu/202601/t20260121_4451699.html","L1",49670.2,"官方页"),
("河北",49305.2,5.6,"2026-01-22","https://hebfb.hebccw.cn/system/2026/01/22/102146852.shtml","L3",47448.1,"摘要待核"),
("陕西",36551.10,5.1,"2026-01-23","https://tjj.shaanxi.gov.cn/tjsj/tjxx/qs/202601/t20260123_3607209.html","L2",35437.10,"摘要待核"),
("江西",36020.0,5.2,"2026-01-22","https://jiangxi.jxnews.com.cn/system/2026/01/22/031034486.shtml","L3",34227.88,"摘要待核"),
("重庆",33757.93,5.3,"2026-01-26","https://tjj.cq.gov.cn/zwgk_233/fdzdgknr/tjxx/sjjd_55469/202601/t20260126_15352347.html","L1",32046.73,"官方页"),
("辽宁",33182.9,3.7,"2026-01-21","https://tjj.ln.gov.cn/tjj/tjsj/sjfb/sqzx/2026012109084644983/index.shtml","L1",32540.8,"官方页"),
("云南",32765.78,4.1,"2026-01-21","https://stats.yn.gov.cn/zwgk/zfxxgk/fdzdgknr/tjsj/sjfb/202601/t20260121_3052863.html","L1",31423.36,"官方页"),
("广西",29727.45,5.1,"2026-01-26","http://tjj.gxzf.gov.cn/tjsj/xwfb/tjxx_sjfb/t27180801.shtml","L2",28694.14,"摘要待核"),
("内蒙古",26710.0,4.7,"2026-01-23","https://tj.nmg.gov.cn/tjdt/fbyjd_11654/202601/t20260123_2853022.html","L2",26337.0,"摘要待核"),
("山西",25495.68,4.0,"2026-01-24","http://tjj.shanxi.gov.cn/tjsj/tjgb/ndtjgb/202603/t20260325_10086636.shtml","L2",25353.5,"摘要待核"),
("贵州",23562.17,4.9,"2026-01-21","https://stjj.guizhou.gov.cn/tjsj/tjfbyjd/202601/t20260121_89321112.html","L1",22645.70,"官方页"),
("新疆",21462.14,5.5,"2026-01-30","https://tjj.xinjiang.gov.cn/tjj/xwfb/202601/6c0d10013e8b4841be2c9c0394dd48c8.shtml","L1",20492.45,"官方页"),
("天津",18539.82,4.8,"2026-01-22","https://www.tj.gov.cn/sq/tjgb/202603/t20260327_7271193.html","L1",17931.55,"摘要待核"),
("黑龙江",16878.0,4.2,"2026-01-25","https://tjj.hlj.gov.cn/tjj/c106736/202601/c00_31908284.shtml","L1",16478.1,"官方页"),
("吉林",14973.88,5.0,"2026-01-26","https://tjj.jl.gov.cn/tjsj/qwfb/202601/t20260126_3548116.html","L1",14305.01,"官方页"),
("甘肃",13697.5,5.8,"2026-01-20","https://www.gsei.com.cn/html/1288/2026-03-30/content-659637.html","L3",13020.5,"摘要待核"),
("海南",8108.85,4.0,"2026-01-23","https://stats.hainan.gov.cn/tjj/ywdt/xwfb/202601/t20260123_4016079.html","L2",7972.71,"摘要待核"),
("宁夏",5696.49,5.3,"2026-01-23","https://tj.nx.gov.cn/tjxx/202601/t20260123_5148302.html","L1",5520.18,"官方页"),
("青海",4121.84,4.1,"2026-01-27","http://www.qinghai.gov.cn/zwgk/system/2026/01/28/030091767.shtml","L1",None,"未找到"),
("西藏",3031.89,7.0,"2026-01-29","https://tjj.xizang.gov.cn/xxgk/tjxx/zxfb/202601/t20260129_521543.html","L1",2789.07,"官方页"),
]
assert len(P)==31
s25=sum(p[1] for p in P)
NAT=1401879; NAT24=1348066
# 2024 ranks using final values; 浙江/青海 2024 position unambiguous (浙江 4th between 山东98407 and 四川64537; 青海 29th between 宁夏5520 and 西藏2789)
v24={p[0]:p[6] for p in P}
v24["浙江"]=90000; v24["青海"]=4000  # placeholder ONLY for rank ordering, not output
r24={k:i+1 for i,(k,v) in enumerate(sorted(v24.items(),key=lambda t:-t[1]))}
out=[]
for i,p in enumerate(P):
    n=round((p[1]/p[6]-1)*100,2) if p[6] else None
    out.append(dict(rank_2025=i+1,province=p[0],gdp_2025_yi=p[1],real_growth_pct=p[2],nominal_growth_pct_自算=n,
      gdp_2024_final_yi=p[6],gdp_2024_final_check=p[7],rank_2024_final_自算=r24[p[0]],rank_change=r24[p[0]]-(i+1),
      share_of_national_pct_自算=round(p[1]/NAT*100,2),release_date=p[3],source_url=p[4],verify_level=p[5],revision="初步核算"))
for o in out: print(o['rank_2025'],o['province'],o['gdp_2025_yi'],o['real_growth_pct'],o['nominal_growth_pct_自算'],o['rank_2024_final_自算'],o['rank_change'],o['share_of_national_pct_自算'],o['verify_level'])
print('sum',round(s25,2),'nat',NAT,'diff',round(s25-NAT,2),'ratio',round(s25/NAT*100,2))
print('>=1万亿',sum(p[1]>=10000 for p in P),'2024',sum((p[6] or 0)>=10000 or p[0]=='浙江' for p in P))
print('>=5万亿',[p[0] for p in P if p[1]>=50000],'2024',[p[0] for p in P if (p[6] or 0)>=50000 or p[0]=='浙江'])
print('>=10万亿',[p[0] for p in P if p[1]>=100000],'2024',[p[0] for p in P if (p[6] or 0)>=100000])
print('top10 sum share',round(sum(p[1] for p in P[:10])/NAT*100,2))
print('growth>5.0',sum(p[2]>5.0 for p in P),'>=5.0',sum(p[2]>=5.0 for p in P))
print('nat nominal',round((NAT/NAT24-1)*100,2))
data=dict(title="2025年31省份GDP（初步核算）",generated="2026-10-26",unit="亿元",
 national=dict(gdp_2025=NAT,real_growth=5.0,revision="初步核算",release="2026-01-20",url="https://www.stats.gov.cn/sj/zxfb/202601/t20260120_1962349.html",
   gdp_2024_final=NAT24,gdp_2024_final_url="https://www.stats.gov.cn/sj/zxfb/202512/t20251226_1962144.html",nominal_growth_自算=round((NAT/NAT24-1)*100,2)),
 provinces_sum_自算=round(s25,2),provinces_sum_minus_national_自算=round(s25-NAT,2),
 verify_levels={"L1":"统计局/省(市、区)政府官网原页已打开核对","L2":"统计局官网页面本机打不开(403/超时)，数字取自该官方页搜索摘要，并与其他官方转载一致","L3":"未取到统计局原页；数字来自省政府新闻发布会/党报或政府网全文转载的公报"},
 notes=["2025年各省数据均为初步核算；国家统计局2025年最终核实预计隔年1月前后发布","2024年为最终核实数（来自各省2025发布的注释），浙江、青海2024最终核实数未找到，名义增速留空","名义增速、排名、占比、合计均为【自算】","各省未公布名义增速，实际增速为不变价"],
 provinces=out)
json.dump(data,open('data.json','w'),ensure_ascii=False,indent=1)
