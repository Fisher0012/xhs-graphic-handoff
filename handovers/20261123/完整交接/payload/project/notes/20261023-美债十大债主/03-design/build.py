#!/usr/bin/env python3
# 生成 p1-p4.html；所有文字/数字照抄 02-框架.md
RISK='风险提示：本文信息仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。'
def page(body):
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head>
<body><div class="page">{body}<div class="risk">{RISK}</div></div></body></html>'''
def n(v): return f'{v:,}'
def rows(data, top, h, first_big):
    mx=max(d[3] for d in data); out=[]
    for i,(idx,name,note,v) in enumerate(data):
        cls='row first' if (i==0 and first_big) else 'row'
        out.append(f'<div class="{cls}" style="height:{h}px"><div class="idx">{idx}</div><div class="name">{name}</div>'
                   f'<div class="note">{note}</div><div class="num">{n(v)}</div>'
                   f'<div class="bar"><i style="width:{v/mx*100:.2f}%"></i></div></div>')
    return f'<div class="rows" style="top:{top}px">{"".join(out)}</div>'

P1=[('01','日本','连续4个月减少，比上月少356亿',10683),('02','英国','首次超过1万亿，2000年有数据以来最高',10095),
('03','中国大陆','2008年8月以来最低，比上月少273亿',5907),('04','比利时','比上月多198亿',4905),
('05','加拿大','比上月多383亿，前20名里增得最多',4646),('06','开曼群岛','一年多525亿，增12.8%',4630),
('07','卢森堡','一年多374亿',4482),('08','法国','比上月多150亿，但比一年前少257亿',3634),
('09','爱尔兰','一年多121亿',3521),('10','中国台湾','一年少150亿',2984)]
p1=('<div class="label">一图看懂｜美债 · 2026年8月末</div>'
 '<div class="title cover-title" id="ct"><span class="w">美债</span><span class="t">十大债主</span></div>'
 '<div class="gline"></div><div class="subtitle cover-sub">外国持有的美国国债 · 2026年8月末 · 单位：亿美元 · 来源 美国财政部TIC</div>'
 + rows(P1,398,76,True) +
 '<div class="hr" style="top:1188px"></div>'
 '<div class="summary" style="top:1212px">前十合计 <b>5.55万亿</b> 美元，占外国持有总额的 <b>59.5%</b>。英国首次超过 <b>1万亿</b>；中国大陆为 <b>2008年8月</b> 以来最低。</div>')

P2=[('11','瑞士','一年少172亿',2858),('12','新加坡','一年多169亿',2779),('13','中国香港','一年多96亿',2615),
('14','印度','比上月多171亿',2197),('15','挪威','比上月多71亿',2140),('16','巴西','一年少162亿，降8.8%',1684),
('17','沙特','一年多82亿',1412),('18','韩国','比上月多27亿',1342),('19','阿联酋','比上月多60亿',1161),
('20','百慕大','一年多129亿，增13.0%',1118)]
stats=[('9.33万亿','外国合计持有','一年增0.9%'),('40.18万亿','美国国债总额','2026年8月31日，未偿公共债务总额'),
('28.8%','外国持有占比','占公众持有部分32.41万亿')]
p2=('<div class="label">一图看懂｜美债 · 2026年8月末</div>'
 '<div class="title inner-title"><span class="w">第</span><span class="t">11到20名</span></div>'
 '<div class="subtitle inner-sub">外国持有的美国国债 · 2026年8月末 · 单位：亿美元</div>'
 + rows(P2,306,68,False) +
 '<div class="stats" style="top:1020px">' + ''.join(f'<div class="stat"><div class="big">{a}</div><div class="lab">{b}</div><div class="sm">{c}</div></div>' for a,b,c in stats) + '</div>'
 '<div class="hr" style="top:1218px"></div>'
 '<div class="summary" style="top:1240px">外国官方机构持有 <b>3.76万亿</b>，占外国合计的 <b>40.2%</b>，比一年前少 <b>1,642亿</b>。其余为<span class="nw">外国私人投资者</span>等持有。</div>')

P3=[('日本','减少',-1156),('中国大陆','减少',-1090),('英国','增加',1082),('开曼群岛','增加',525),('比利时','增加',394),
('卢森堡','增加',374),('法国','减少',-257),('加拿大','增加',206),('瑞士','减少',-172),('新加坡','增加',169)]
mx=max(abs(v) for _,_,v in P3); mxpos=max(v for _,_,v in P3); out=[]
for name,tag,v in P3:
    cls='drow'+(' neg' if v<0 else '')+(' max' if v==mxpos else '')
    s=('+' if v>0 else '−')+n(abs(v))
    out.append(f'<div class="{cls}" style="margin-bottom:9px"><div class="top"><span class="name">{name}</span><span class="tag">{tag}</span><span class="num">{s}</span></div><div class="track"><i style="width:{abs(v)/mx*100:.2f}%"></i></div></div>')
p3=('<div class="label">一图看懂｜美债 · 2025年8月→2026年8月</div>'
 '<div class="title inner-title"><span class="w">一年来 </span><span class="t">谁增谁减</span></div>'
 '<div class="subtitle inner-sub">持有额变化 · 2026年8月末对比2025年8月末 · 单位：亿美元</div>'
 f'<div class="rows" style="top:318px">{"".join(out)}</div>'
 '<div class="callout" style="top:1022px"><h3>中国大陆比峰值少了一半多</h3><p>2013年11月峰值13,167亿，2026年8月为5,907亿，少7,260亿，降55.1%；是2008年8月<span class="nw">（5,737亿）</span>以来最低。</p></div>'
 '<div class="hr" style="top:1222px"></div>'
 '<div class="summary small-sum" style="top:1242px">外国合计一年只多 <b>826亿</b>（+0.9%），总量基本持平，变化主要是内部此消彼长。灰色条为减少；增减含价格变动，不全是主动增减。</div>')

C=[('托管地','（按存放地，不按真正的主人）','18.8%',[('','开曼+卢森堡+比利时+爱尔兰'),('合计','17,538亿'),('占外国合计','18.8%')],
    '财政部说明，存在第三国托管账户里的美债，数据反映不出真正的主人。'),
 ('价格','（持有额变了，不全是主动增减）','含价格变动',[('中长期国债','按市值'),('短期国库券','按面值'),('持有额 =','月末估算')],
    '中长期美债按市值计，价格下跌时数量不变，持有额也会变少。'),
 ('时间','（数据晚一个半月才出）','8月31日',[('数据截至','2026年8月末'),('发布','10月16日'),('下次','11月18日（9月数据）')],
    '均为华盛顿时间16:00发布，北京时间为10月17日、11月19日凌晨；2025年数据同期做了修订。'),
 ('总额','（40.18万亿是哪个数）','40.18万亿',[('未偿公共债务总额','40.18万亿'),('公众持有','32.41万亿'),('政府内部持有','7.76万亿')],
    '取2026年8月31日；外国持有占公众持有约28.8%为自算，两套统计口径不同，只看量级。')]
cards=''.join(f'<div class="card"><div class="head"><h3>{t}</h3><span class="paren">{p}</span></div>'
  f'<div class="key"><small>关键数字</small><span>{k}</span></div>'
  '<div class="fields">'+''.join(f'<div class="f"><small>{a}</small><span>{b}</span></div>' for a,b in fs)+'</div>'
  f'<div class="desc">{d}</div></div>' for t,p,k,fs,d in C)
p4=('<div class="label">一图看懂｜美债</div>'
 '<div class="title inner-title"><span class="w">这几个数 </span><span class="t">要说明</span></div>'
 '<div class="subtitle inner-sub">看排名之前先知道这四件事</div>'
 f'<div class="cards">{cards}</div>'
 '<div class="hr" style="top:1268px"></div>'
 '<div class="src" style="top:1284px">来源：美国财政部TIC「Major Foreign Holders of Treasury Securities」表5及历史表、TIC发布日程、财政部Fiscal Data「Debt to the Penny」。</div>')
for i,b in enumerate([p1,p2,p3,p4],1):
    open(f'p{i}.html','w').write(page(b))
