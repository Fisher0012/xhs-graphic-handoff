#!/usr/bin/env python3
# 生成 p1-p4.html；文字/数字照抄 02-框架.md 与 data.json
RISK='风险提示：本文信息仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。'
LABEL='<div class="label">一图看懂｜外汇储备</div>'
SC='<span class="tag-sc">【自算】</span>'
def page(body):
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head>
<body><div class="page">{LABEL}{body}<div class="risk">{RISK}</div></div></body></html>'''

# ---------- P1 ----------
P1=[('01','中国','9月末｜比8月末少381亿',34003),('02','日本','9月末｜比8月末少181亿【自算】',9769),
('03','瑞士','8月末｜比7月末多67亿【自算】',9525),('04','印度','8月末｜比7月末多471亿【自算】',6118),
('05','中国台湾','9月末｜比8月末少12亿',6007),('06','沙特','8月末｜比7月末少15亿【自算】',4622),
('07','中国香港','8月末｜比7月末少57亿【自算】',4296),('08','新加坡','8月末｜比7月末多51亿【自算】',4188),
('09','韩国','8月末｜比7月末多143亿【自算】',4161),('10','俄罗斯','9月末｜另有黄金3016亿 未计入',4004)]
H=80; out=[]
for i,(idx,name,note,v) in enumerate(P1):
    out.append(f'<div class="row{" first" if i==0 else ""}" style="height:{H}px"><div class="idx">{idx}</div>'
      f'<div class="nm"><div class="name">{name}</div><div class="note">{note}</div></div><div class="num">{v}</div>'
      f'<div class="bar"><i style="width:{v/34003*100:.2f}%"></i></div></div>')
p1=('<div class="title cover-title" id="ct"><span class="w">全球外汇储备</span><span class="t">前十</span></div>'
 '<div class="gline"></div><div class="subtitle cover-sub">只算外汇储备 不含黄金｜单位：亿美元｜截至2026年8月末或9月末</div>'
 f'<div class="rows" style="top:350px">{"".join(out)}</div>'
 '<div class="hr" style="top:1168px"></div>'
 f'<div class="summary" style="top:1182px">中国是第2名日本的<b>3.5倍</b>{SC}；<br>第11名巴西3054亿</div>')

# ---------- P2 ----------
cards=[('约1/4','占全球外汇储备','6月末｜【自算】25.8%'),('3.5倍','是第2名日本的倍数','9月末｜【自算】'),('−381亿','9月比8月','降1.11%')]
kc=''.join(f'<div class="kcard" style="top:{318+i*108}px"><div class="big {"t" if i<2 else "w"}">{a}</div><div class="lab">{b}</div><div class="sm">{c}</div></div>' for i,(a,b,c) in enumerate(cards))
M=[('1月',33991,''),('2月',34278,''),('3月',33421,'lo'),('4月',34105,''),('5月',34422,'hi'),('6月',34163,''),('7月',34188,''),('8月',34383,''),('9月',34003,'last')]
K={'lo':'年内最低','hi':'年内最高','last':''}
cols=''.join(f'<div class="col {c}"><div class="k">{K.get(c,"")}</div><div class="v">{v}</div><div class="b" style="height:{v/34422*170:.1f}px"></div><div class="m">{m}</div></div>' for m,v,c in M)
p2=('<div class="title inner-title"><span class="w">中国这</span><span class="t">3.4万亿</span></div>'
 '<div class="subtitle inner-sub">单位：亿美元｜外汇局口径「外汇储备」，不含黄金</div>'
 + kc +
 f'<div class="chart" style="top:650px;height:280px">{cols}</div>'
 '<div class="gbox" style="top:956px"><p><b style="color:var(--teal)">外汇局：</b>9月美元指数上涨、全球主要金融资产价格总体下跌，汇率折算和资产价格变化等因素综合作用</p></div>'
 '<div class="small" style="top:1124px">另有黄金3235亿美元（7747万盎司），不在这3.4万亿里；<br>加上黄金等，官方储备资产共37894亿</div>'
 f'<div class="summary" style="top:1214px">今年9个月都在3.3万亿–3.5万亿之间{SC}</div>')

# ---------- P3 ----------
P3=[('中国','9月末比去年9月末｜+1.8%',616),('瑞士','8月末比去年8月末｜+6.7%',598),('新加坡','8月末｜+10.8%',409),
('沙特','8月末｜+7.2%',310),('印度','8月末｜+4.7%',273),('韩国','8月末｜+6.7%',260),('中国香港','8月末｜+5.3%',218),
('俄罗斯','9月末｜−0.2%',-8),('中国台湾','9月末｜−0.4%',-22),('日本','9月末｜−15.0%',-1718)]
NEG=1718; POS=616; RNG=NEG+POS; Z=NEG/RNG*100
rows=[]
for name,tag,v in P3:
    w=abs(v)/RNG*100; left=Z if v>0 else Z-w
    s=('+' if v>0 else '−')+str(abs(v))
    rows.append(f'<div class="drow{" neg" if v<0 else ""}"><div class="top"><span class="name">{name}</span><span class="tag">{tag}</span><span class="num">{s}</span></div>'
                f'<div class="track"><i style="left:{left:.2f}%;width:{max(w,0.35):.2f}%"></i></div></div>')
p3=('<div class="title inner-title"><span class="w">一年来 </span><span class="t">谁增谁减</span></div>'
 f'<div class="subtitle inner-sub">和一年前同一个月比｜单位：亿美元｜数字均为{"【自算】"}</div>'
 f'<div class="rows" style="top:316px">{"".join(rows)}</div>'
 '<div class="callout" style="top:1050px"><p>日本今年2月末11799亿是年内最高，到9月末少了<b>2030亿</b>；8月末日本和瑞士只差<b>424亿</b>，<span class="nw">一年前差2497亿</span>'+SC+'</p></div>'
 '<div class="small" style="top:1266px">官方数据只给余额，不给增减原因；变化里包含汇率折算和资产价格变化</div>')

# ---------- P4 ----------
IT=[('只算外汇：','本文「外汇储备」＝外币证券＋外币存款（IMF储备模板第一项），不含黄金、特别提款权、<span class="nw">IMF头寸</span>和其他储备资产；和外汇局公布的「外汇储备」是<span class="nw">同一口径</span>'),
('月份不同：','<span class="nw"><span class="mo">9月末</span> 中国 日本 中国台湾 俄罗斯</span><br><span class="nw"><span class="mo">8月末</span> 瑞士 印度 沙特 中国香港 新加坡 韩国</span><br>这6家同口径的9月数10月底才陆续公布；瑞士、沙特、新加坡已公布的9月数只有本币，本文不换算'),
('新闻数为什么更大：','新闻常报「总储备」<span class="nw">（含黄金等）</span>：中国37894亿、日本11784亿、<span class="nw">俄罗斯7318亿</span><span class="nw">（均9月末）</span>；香港新闻稿<span class="nw">「官方外汇储备资产」</span><span class="nw">4330亿</span><span class="nw">（9月末）</span><span class="nw">含其他储备资产；</span>印度央行周报是另一口径'),
('怎么算的：','数字均为官方公布的美元数，未做<span class="nw">汇率换算</span>；比上月、一年变化、倍数、占比<span class="nw">按官方数计算</span>'+SC+'；中国台湾、中国香港<span class="nw">按经济体列示</span>，<span class="nw">中国台湾数据</span>来自台湾地区央行')]
NO='①②③④'
items=''.join(f'<div class="item"><p><b>{NO[i]} {h}</b>{t}</p></div>' for i,(h,t) in enumerate(IT))
p4=('<div class="title inner-title"><span class="w">这几个数 </span><span class="t">要说明</span></div>'
 f'<div class="items" style="top:262px">{items}</div>'
 '<div class="src" id="src" style="top:1242px">来源：国家外汇管理局、IMF、日本财务省、瑞士央行、台湾地区央行、香港金管局；<br>数据截至2026年10月25日公布</div>')
for i,b in enumerate([p1,p2,p3,p4],1):
    open(f'p{i}.html','w').write(page(b))
