import sys,json,re
from pathlib import Path
sys.path.insert(0,'/workspace/xhs/notes')
from heijin import *
from cover_gen import cover
N=Path(__file__).resolve().parent.parent; D=N/'03-design'
data=json.loads((N/'data.json').read_text()); rows=sorted(data['items'],key=lambda x:-x['growth'])
cover(str(D/'p1.html'),'前10个月｜主要税收项目增速榜','税收增速分化','印花税 <b style="color:#e9b519">+24.6%</b>领跑 · 土地增值税 <b style="color:#7fd3ff">−16.6%</b>垫底',[(r['name'],str(r['amount'])+'亿元'+('·含证券交易' if r['name']=='印花税' else '·进口增值税消费税' if r['name']=='进口环节税' else ''),r['growth'],0) for r in rows[:10]],'%','来源：财政部 2026-11-20｜2026年1—10月累计同比｜作者排序',fmt='+{:.1f}')
h=(D/'p1.html').read_text().replace('</style>','h1{font-size:122px;letter-spacing:4px}.nm{font-size:40px;width:310px}.row{align-items:center;height:62px;padding-top:0}.rk svg{vertical-align:-2px}</style>',1)
card='<div style="margin-top:14px;background:linear-gradient(90deg,#191612,#121113);border:1px solid #26232a;border-radius:14px;padding:16px 24px;font-size:25px;color:#bdb8ae">主榜前10项｜后7项见第3张；证券交易印花税为子项，<b style="color:#e9b519">不重复排名</b></div>'
h=re.sub(r'(</div>)(\s*<div class=foot>)',r'\1'+card+r'\2',h,count=1)
(D/'p1.html').write_text(h)
T='<div class=tag>一图看懂｜2026年前10个月税收</div>'
def duo(a,b):
 def one(lab,num,unit,note):
  return f'<div class=card style="flex:1;margin-top:0;padding:20px 24px 22px 32px"><div class=lab>{lab}</div><div style="font-family:NSB;font-size:68px;margin-top:4px" class=g>{num}<span style="font-size:26px;color:#9b9b9e;margin-left:6px">{unit}</span></div><p style="font-size:25px;color:#bdb8ae;line-height:1.5">{note}</p></div>'
 return '<div style="display:flex;gap:18px;margin-top:22px">'+one(*a)+one(*b)+'</div>'
# Keep approved typography and block language. Remove automatic font shrinking: content is sized to fit.
def out(num,title,sub,body):
 page(str(D/f'p{num}.html'),num,T+head(title,sub)+body,total=4)
 p=D/f'p{num}.html'; h=p.read_text().replace(FILL_JS,''); h=h.replace('</style>', ('td:nth-child(2){text-align:left}td{padding-top:16px;padding-bottom:16px}' if num==3 else '.it{margin-top:62px}.src{margin-top:50px}' if num==4 else '')+'</style>'); p.write_text(h)
source='<div class=src>来源：财政部2026-11-20《2026年1-10月财政收支情况》；金额均为亿元人民币，增速均为累计同比。</div>'
out(2,'个税涨，不等于工资涨','个税收入是多种所得的税款，不是居民工资增速',
 duo(('个人所得税','16,428','亿元','前10个月同比 <span class=gc>+22.9%</span>'),('全国税收','162,622','亿元','前10个月同比 <span class=gc>+6.0%</span>'))+
 it('<span class=k>①</span> 先分清：这是税款，不是工资','个税收入增长22.9%，不能理解成“大家工资都涨了22.9%”。不同所得和纳税群体会共同影响总额。')+
 it('<span class=k>②</span> 官方曾解释过，但时期不同','税务总局6月10日解释的是<span class=gc>今年1—5月</span>：资本市场活跃、部分行业缴税增长、加强高收入人员纳税引导规范。')+
 it('<span class=k>③</span> 不能把旧解释硬套新数据','本次财政收支表没有单列前10个月个税增长原因。以上作为往期背景，不作为22.9%的同期间归因。')+
 '<div style="margin-top:40px;padding:22px 28px;border-left:5px solid #e9b519;background:#191612;font-size:29px;line-height:1.6;color:#bdb8ae">看总量，更要看构成：<span class=gc>税收增速 ≠ 工资增速</span></div>'+
 '<div class=src style="margin-top:36px">来源：财政部2026-11-20；国家税务总局2026-06-10（解释对应2026年1—5月，不对应前10个月）。</div>')
trs=''.join(f'<tr><td style="width:68px;color:#777">{i:02d}</td><td>{r["name"]}</td><td>{r["amount"]:,}</td><td>{r["growth"]:+.1f}%</td></tr>' for i,r in enumerate(rows[10:],11))
out(3,'地产相关税，有涨有跌','接封面：主榜第11—17项；没有把母子项混排',
 '<table style="margin-top:30px"><tr class=h><td>序</td><td style="text-align:left">收入项目</td><td>亿元</td><td>同比</td></tr>'+trs+'</table>'+
 it('<span class=k>不能说</span> 房地产相关税“全线下降”','契税 <span class=gc>−14.9%</span>、土地增值税 <span class=gc>−16.6%</span>；但房产税 <span class=gc>+6.4%</span>、城镇土地使用税 <span class=gc>+4.2%</span>。')+
 '<div style="margin-top:32px;font-size:26px;color:#bdb8ae;line-height:1.7">“其他税收合计”含车船税、船舶吨税、烟叶税等。主榜共17个收入项目，<span class=gc>不是17个独立税种</span>。</div>'+source)
out(4,'财政收入，不全是税','全国一般公共预算｜2026年1—10月累计',
 duo(('一般公共预算收入','195,671','亿元','同比 <span class=gc>+4.9%</span>'),('一般公共预算支出','228,042','亿元','同比 <span class=gc>+1.0%</span>'))+
 '<div style="margin-top:70px"><div class=lab>收入拆开看｜税收＋非税收入</div><div style="display:flex;height:24px;margin-top:22px;border-radius:7px;overflow:hidden"><div style="width:83.11%;background:#e9b519"></div><div style="flex:1;background:#7fd3ff"></div></div><table style="margin-top:18px"><tr><td>税收收入</td><td>162,622亿元</td><td class=gc>+6.0%</td></tr><tr><td>非税收入</td><td>33,049亿元</td><td style="color:#7fd3ff">−0.2%</td></tr></table></div>'+
 it('<span class=k>单独看</span> 证券交易印花税','收入 <span class=gc>2,511亿元</span>，同比 <span class=gc>+54.1%</span>。它包含在印花税4,712亿元中，不能当成另一项再相加或重复排名。')+
 '<div style="margin-top:62px;font-size:27px;line-height:1.7;color:#bdb8ae">出口退税<span class=gc>19,563亿元</span>是减项，不列收入增速榜。<br>17项收入合计−出口退税＝税收总额（作者复算）。</div>'+source)
print('generated four pages from approved heijin/cover_gen and previous tax layout')
