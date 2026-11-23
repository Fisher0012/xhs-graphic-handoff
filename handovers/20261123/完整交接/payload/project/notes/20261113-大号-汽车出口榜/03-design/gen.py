import sys,re
from pathlib import Path
sys.path.insert(0,'/workspace/xhs/notes')
from heijin import *
from cover_gen import cover
D=Path(__file__).parent
# 共用 cover_gen 建封面；本期不使用企业榜，改成已核实的中汽协总量。
cover(str(D/'p1.html'),'阿信学财经｜汽车出口观察','汽车出口新数据','2026年10月 · 中汽协 · 全部汽车（含商用车）', [('占位','',106.6,0)],'万辆','来源：中汽协数据｜新华网·经济参考报 2026-11-12｜2026-11-13查')
h=(D/'p1.html').read_text()
content='''<div class="list covercontent">
<div class="hero"><div class="eyebrow">10月汽车出口</div><div class="main g">106.6<span>万辆</span></div><div class="yoy">同比增长 <b class="g">60.2%</b></div></div>
<div class="strip"><div>连续<span class="g">5</span>个月</div><div>月出口超过<span class="g">100</span>万辆</div></div>
<div class="coverpair"><div><small>1—10月累计出口</small><b class="g">927.1<em>万辆</em></b></div><div><small>累计同比增长</small><b class="g">65.1<em>%</em></b></div></div>
<div class="guide"><b>这次看三个问题</b><p>国内销量与出口，差在哪？</p><p>新能源出口，占了多少？</p><p>出口退税，何时调整？</p></div>
</div>'''
h=re.sub(r'<div class=list>.*?(?=<div class=foot>)',content+'\n',h,flags=re.S)
h=h.replace('</style>','''h1{font-size:112px;letter-spacing:4px}.g{background:linear-gradient(165deg,#f7e6ae 0%,#f2cd52 40%,#e2ab12 75%,#c98f0c 100%);-webkit-background-clip:text;color:transparent}
.covercontent{height:960px;display:flex;flex-direction:column;justify-content:space-between;margin-top:34px;padding:0 26px}.hero{padding:22px 0 24px;border-bottom:1px solid #35302a}.eyebrow{font-size:32px;color:#9b9b9e}.main{font-family:NSB;font-size:162px;line-height:1.15;letter-spacing:-2px}.main span{font-size:40px;margin-left:14px;letter-spacing:0}.yoy{font-size:34px;margin-top:6px}.yoy b{font-family:NSB;font-size:57px;margin-left:14px}.strip{font-size:36px;line-height:1.55;border-bottom:1px solid #35302a;padding:20px 0}.strip span{font-family:NSB;font-size:50px;margin:0 10px}.coverpair{display:flex;gap:36px;padding:20px 0;border-bottom:1px solid #35302a}.coverpair>div{flex:1}.coverpair small{font-size:27px;color:#9b9b9e}.coverpair b{display:block;font-family:NSB;font-size:64px;margin-top:12px}.coverpair em{font-style:normal;font-size:26px;margin-left:8px}.guide{padding:22px 0 30px}.guide b{font-family:NSB;font-size:36px}.guide p{font-size:28px;color:#bdb8ae;line-height:1.8}.foot{font-size:19px}
</style>''')
(D/'p1.html').write_text(h)
T='<div class=tag>阿信学财经｜汽车出口观察</div>'
STYLE='''<style>.src,.foot{transform:translateZ(0);isolation:isolate;z-index:2}.content{height:990px;display:flex;flex-direction:column;justify-content:space-between;margin-top:26px}.content .card{margin-top:0;padding:22px 28px;flex-shrink:0}.content h3{font-family:NSB;font-size:34px;line-height:1.25;margin-bottom:12px}.content p{font-size:26px;line-height:1.55;color:#bdb8ae}.pair{display:flex;gap:28px}.pair>div{flex:1}.num{font-family:NSB;font-size:68px;line-height:1.15}.num small{font-family:NSM;font-size:25px;color:#9b9b9e;margin-left:8px}.caption{font-size:25px;color:#9b9b9e;margin-bottom:8px}.delta{font-family:NSB;font-size:34px;line-height:1.3;margin-top:8px}.rule{height:1px;background:#35302a;margin:16px 0}.content table td{font-size:31px;padding:16px 0}.note{font-size:24px;color:#9b9b9e;line-height:1.5}.content .src{font-size:20px;line-height:1.6;margin-top:0}.rate{font-family:NSB;font-size:112px;line-height:1.3}.rate span{font-size:62px;color:#9b9b9e;margin:0 20px}.bartrack{height:22px;background:#35302a;border-radius:8px;margin:20px 0}.barfill{height:100%;background:linear-gradient(90deg,#f7e6ae,#e9b519);border-radius:8px}</style>'''
def make(n,title,sub,content):
 page(str(D/f'p{n}.html'),n,T+head(title,sub)+STYLE+'<div class=content>'+content+'</div>',total=4)
make(2,'国内销量与出口','2026年10月 · 中汽协 · 单位：万辆', '''
<div class=card><h3>同一个月，方向不同</h3><div class=pair><div><div class=caption>国内销量</div><div class=num>195.0<small>万辆</small></div><div class=delta>同比 −26.6%</div></div><div><div class=caption>出口量</div><div class="num g">106.6<small>万辆</small></div><div class="delta gc">同比 +60.2%</div></div></div></div>
<div class=card><h3>拉长到前10个月</h3><table><tr class=h><td>1—10月</td><td>数量</td><td>同比</td></tr><tr><td>国内销量</td><td>1701.4</td><td>−22.9%</td></tr><tr><td>出口量</td><td>927.1</td><td>+65.1%</td></tr></table></div>
<div class=card><h3>别把“总销量”当内销</h3><p>10月汽车总销量301.6万辆<br>＝国内销量195.0＋出口106.6</p><div class=rule></div><div class=note>均为中汽协全部汽车口径<br>不是终端零售，也不等同于上牌量</div></div>
<div class=src>来源：中汽协数据；新浪·智通财经2026-11-12、新华网·经济参考报2026-11-12｜2026-11-13查</div>''')
make(3,'新能源出口占多少','全部汽车出口口径 · 占比由作者计算', '''
<div class=card><h3>10月：超过一半</h3><div class="num g">56.8<small>%</small></div><div class=bartrack><div class=barfill style="width:56.8%"></div></div><p>新能源出口60.6万辆<br>÷ 全部汽车出口106.6万辆</p></div>
<div class=card><h3>1—10月：接近一半</h3><div class="num g">49.7<small>%</small></div><div class=bartrack><div class=barfill style="width:49.7%"></div></div><p>新能源出口461.2万辆<br>÷ 全部汽车出口927.1万辆</p></div>
<div class=card><h3>月度 ≠ 累计</h3><p>10月占比超过一半<br>不代表前10个月累计也超过一半</p><div class=note style="margin-top:12px">作者计算：分子÷分母×100%，四舍五入至一位小数；均含乘用车及商用车。</div></div>
<div class=src>来源：中汽协数据｜新华网·经济参考报2026-11-12<br>中新经纬2026-11-11交叉核对｜2026-11-13查</div>''')
make(4,'出口退税何时调整','新能源汽车 · 增值税出口退税率', '''
<div class=card><h3>2027年4月1日起</h3><div class="rate g">13%<span>→</span>9%</div><p>具体适用产品见公告附件1</p></div>
<div class=card><h3>日期怎么认？</h3><p>以出口货物报关单注明的<br>出口日期界定</p><div class=rule></div><div class=note>不是按签约日，也不是按下单日<br>具体执行以公告及税务规定为准</div></div>
<div class=card><h3>政策出处</h3><p>财政部 税务总局<br>公告2026年第29号</p><div class=rule></div><div class=note>成文：2026年10月12日<br>仅梳理政策，不据此推测后续销量</div></div>
<div class=src>来源：财政部、税务总局《关于调整部分产品出口退税政策的公告》及附件1｜2026-11-13查</div>''')
print('gen: 4 pages')

# 本期固定内容容器，不使用动态增字号填充，避免卡片被 flex 压缩裁字。
for f in D.glob('p[2-4].html'):
 s=f.read_text().replace(FILL_JS,'')
 f.write_text(s)
