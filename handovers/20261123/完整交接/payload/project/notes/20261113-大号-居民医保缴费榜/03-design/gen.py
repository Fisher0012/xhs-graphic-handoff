import sys,re,json
from pathlib import Path
sys.path.insert(0,'/workspace/xhs/notes')
from heijin import *
from cover_gen import cover
D=Path(__file__).parent
N=D.parent
data=json.loads((N/'data.json').read_text())
RISK='风险提示：本文信息仅供参考，不构成投资或保险建议；具体以当地医保部门为准。'
rows=[(x['city'],x['scope'],x['personal'],0) for x in data['cities']]
cover(str(D/'p1.html'),'阿信学财经｜8城样本 · 2027年度','各地医保交多少',
 '成年居民所列档次降序 · 个人医保费 · 不含长护 · 元/年',rows,'元',
 '来源：8城政府及医保官网｜2026-11-13核对',fmt='{:.0f}')
h=(D/'p1.html').read_text().replace('</style>','h1{font-size:110px;letter-spacing:4px}.row{height:68px;align-items:center;padding-top:0}.bar{margin:4px 0 15px}.rk svg{vertical-align:-2px}.pn{position:absolute;right:40px;top:82px;color:#66666a;font-size:23px}.list{margin-top:24px}</style>')
for k in ['05','06','07','08']: h=h.replace('</span>'+k+'</div>','</span>04</div>',1)
note='<div style="margin-top:22px;padding:18px 24px;border:1px solid #26232a;border-radius:14px;font-size:23px;line-height:1.65;color:#bdb8ae">天津1130元为高档；当地另有450元低档。<br>海口成年居民另缴长护26元；伊春400元为暂定。<br>仅比较所列档次，不代表全国全榜或待遇优劣；同额并列。</div>'
h=h.replace('<div class=foot>',note+'<div class=pn>1/5</div><div class=foot>',1)
h=h.replace('风险提示：本文信息仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。',RISK)
(D/'p1.html').write_text(h)
T='<div class=tag>阿信学财经｜居民医保缴费读本</div>'
def box(lab,num,unit,detail):
 return f'<div class=card><div class=lab style="font-size:30px">{lab}</div><div class=g style="font-family:NSB;font-size:76px;line-height:1.2;margin-top:8px">{num}<span style="font-size:30px;margin-left:12px">{unit}</span></div><p style="font-size:29px;color:#bdb8ae;line-height:1.65;margin-top:10px">{detail}</p></div>'
def make(i,title,sub,body):
 page(str(D/f'p{i}.html'),i,T+head(title,sub)+body,total=5)
 p=D/f'p{i}.html';s=p.read_text().replace(FOOT,f'<div class="foot">{RISK}</div>').replace(f'<div class=pn>{i-1}/4</div>',f'<div class=pn>{i}/5</div>');p.write_text(s)
make(2,'你交的不是全部','全国筹资口径示意 · 单位：元/人/年',
 box('个人缴费最低标准','400','元','地方可按规定制定更高的个人缴费标准。')+
 box('人均财政补助标准','724','元','财政补助与个人缴费共同形成医保基金，不是现金发到个人手里。')+
 box('两项相加示意｜作者计算','1124','元','400＋724＝1124。不是个人可领取或可报销的固定金额。')+
 '<div class=src>来源：新华社经济参考报2026-10-14，引述国家医保局副局长黄华波。全国人均标准不等于每个城市的实际补助额。</div>')
make(3,'断保后要等多久','国家框架 · 自2025年起 · 具体执行以各省规定为准',
 box('固定待遇等待期','3','个月','非集中期参保或未连续参保，参保后设置；新生儿等特殊群体除外。')+
 box('每多断保1年，原则上增加','1','个月','这是变动待遇等待期，可通过缴费修复；每多缴纳1年可减少1个月。')+
 box('连续断缴4年及以上','≥6','个月','修复后，固定与变动等待期合计原则上不少于6个月。')+
 '<div class=src>来源：国办发〔2024〕38号，国家医保局2024-08-01发布。等待期内的具体待遇及特殊群体衔接，请核对参保地政策。</div>')
make(4,'连续参保有什么','激励的是大病保险最高支付限额 · 不是现金奖励',
 box('连续参加居民医保满','4','年','之后每连续参保1年，可适当提高大病保险最高支付限额。')+
 box('原则上，每次提高限额不低于','1000','元','当年基金零报销的，次年也可提高限额；两项激励具体由各省确定。')+
 box('累计提高总额，不超过原封顶线','20','%','断保后再次参保，连续参保年数重新计算。')+
 '<div class=src>来源：国办发〔2024〕38号。发生大病报销并使用奖励额度后，前期积累的零报销激励额度清零；不要混同连续参保激励。</div>')
make(5,'截止日期别看错','集中参保缴费期 · 以下均为各地官方已公布日期',
 box('西安','12月25日','2026年','按陕西省集中缴费安排；以当地登记与缴费结果为准。')+
 box('天津、佛山、江门、哈尔滨、伊春','12月31日','2026年','佛山：申报12月21日截止，缴费12月31日截止。')+
 box('海口、长沙','1月31日','2027年','海口按海南省安排，长沙按湖南省安排；不要套用别处截止日。')+
 '<div class=src>来源：天津/佛山税务局、江门市政府、黑龙江省政府/医保局、西安市医保局、海口社保中心、湖南省医保局。访问：2026-11-13。</div>')
print('gen ok: 5 pages')
