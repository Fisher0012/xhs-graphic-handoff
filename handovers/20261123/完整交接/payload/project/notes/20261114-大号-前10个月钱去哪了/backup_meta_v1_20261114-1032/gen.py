# -*- coding: utf-8 -*-
import sys, re
sys.path.insert(0, "/workspace/xhs/notes")
from heijin import *
from cover_gen import cover

D = "/workspace/xhs/notes/20261114-大号-前10个月钱去哪了/03-design/"
SRC = "来源：中国人民银行《2026年10月金融统计数据报告》2026-11-13｜差值为作者计算"

rows = [
    ("住户存款", "个人及家庭在银行的存款", 8.47, 1),
    ("非银机构", "非银行业金融机构存款", 5.99, 0),
    ("财政存款", "财政性存款", 3.03, 0),
    ("企业存款", "非金融企业存款", 1.91, 0),
]
cover(D + "p1.html", "一图看懂｜2026年前10个月金融数据", "前10月钱去哪了",
      "2026年1–10月｜人民币存款和贷款增量｜央行11月13日发布",
      rows, "万亿", SRC, fmt="+{:.2f}")

h = open(D + "p1.html").read()
# 标题先按 8 字全角近似收一档，稍后用实测宽度再微调到 75–85%
h = h.replace("</style>", "h1{font-size:108px;letter-spacing:4px}.nm{font-size:42px;width:250px}.row{align-items:center;height:102px;padding-top:0}.rk svg{vertical-align:-2px}.list{margin-top:20px}.bar{margin:6px 0 8px;height:8px}</style>", 1)

hero = (
    '<div style="display:flex;gap:16px;margin-top:22px">'
    '<div style="flex:1;background:linear-gradient(90deg,#191612,#121113);border:1px solid #26232a;border-radius:14px;padding:22px 22px 24px 26px">'
    '<div style="color:#e9b519;font-family:NSB;font-size:22px;letter-spacing:1px">人民币存款增加</div>'
    '<div style="font-family:NSB;font-size:68px;margin-top:4px" class=g>21.97'
    '<span style="font-size:26px;color:#9b9b9e;margin-left:6px">万亿元</span></div>'
    '<div style="font-size:22px;color:#bdb8ae;margin-top:2px">前十个月累计｜初步数</div></div>'
    '<div style="flex:1;background:linear-gradient(90deg,#191612,#121113);border:1px solid #26232a;border-radius:14px;padding:22px 22px 24px 26px">'
    '<div style="color:#e9b519;font-family:NSB;font-size:22px;letter-spacing:1px">人民币贷款增加</div>'
    '<div style="font-family:NSB;font-size:68px;margin-top:4px" class=g>11.42'
    '<span style="font-size:26px;color:#9b9b9e;margin-left:6px">万亿元</span></div>'
    '<div style="font-size:22px;color:#bdb8ae;margin-top:2px">先看总量，不是整体在降</div></div>'
    '</div>'
)
card = (
    '<div style="margin-top:22px;background:linear-gradient(90deg,#191612,#121113);border:1px solid #26232a;border-radius:14px;padding:26px 28px;font-size:27px;color:#bdb8ae;line-height:1.7">'
    '四项合计 <b style="color:#e9b519">19.40万亿</b>，与 21.97 万亿相差 <b style="color:#e9b519">2.57万亿</b>（作者计算，报告未分列）。'
    '住户贷款减少 <b style="color:#e9b519">1.46万亿</b>，内页拆开看。存款增加不等于收入增加。'
    '</div>'
)
h = h.replace('<div class=list>', hero + '<div class=list>')
h = re.sub(r'(</div>)(\s*<div class=foot>)', r'\1' + card + r'\2', h, count=1)

FILL = """<script>document.fonts.ready.then(function(){
var f=document.querySelector('.foot');
var limit=f.getBoundingClientRect().top-28;
function bottom(){var m=0;[].slice.call(document.body.children).forEach(function(e){if(e.matches('.foot,style,script'))return;var r=e.getBoundingClientRect();if(r.height)m=Math.max(m,r.bottom)});return m}
var card=[].slice.call(document.querySelectorAll('body > div')).pop();
var rows=[].slice.call(document.querySelectorAll('.row'));
var bars=[].slice.call(document.querySelectorAll('.bar'));
for(var i=0;i<80;i++){
  var free=limit-bottom();
  if(free<=24) break;
  var add=Math.min(2, free/ (rows.length+2));
  rows.forEach(function(e){e.style.height=(parseFloat(getComputedStyle(e).height)+add)+'px'});
  if(card){var cs=getComputedStyle(card);card.style.paddingTop=(parseFloat(cs.paddingTop)+0.4)+'px';card.style.paddingBottom=(parseFloat(cs.paddingBottom)+0.4)+'px';card.style.marginTop=(parseFloat(cs.marginTop)+0.4)+'px'}
}
})</script>"""
h = h.replace('</body>', FILL + '</body>')

open(D + "p1.html", "w").write(h)

T = '<div class=tag>一图看懂｜2026年前10个月金融数据</div>'

def duo(a, b):
    def one(lab, num, unit, note):
        return (
            f'<div class=card style="flex:1;margin-top:0;padding:20px 24px 22px 32px">'
            f'<div class=lab>{lab}</div>'
            f'<div style="font-family:NSB;font-size:60px;margin-top:4px" class=g>{num}'
            f'<span style="font-size:24px;color:#9b9b9e;margin-left:6px">{unit}</span></div>'
            f'<p style="font-size:23px;color:#bdb8ae;line-height:1.5">{note}</p></div>'
        )
    return f'<div style="display:flex;gap:18px;margin-top:20px">{one(*a)}{one(*b)}</div>'

def tcard(lab, big, p):
    return (
        f'<div class=card><div class=lab>{lab}</div>'
        f'<div style="font-family:NSB;font-size:36px;margin-top:6px;color:#fff">{big}</div>'
        f'<p style="font-size:25px;color:#bdb8ae;margin-top:8px;line-height:1.65">{p}</p></div>'
    )

page(D + "p2.html", 2, f'''{T}{head('存款加在哪几块', '2026年1–10月｜人民币存款增量｜初步数')}
{duo(('人民币存款余额', '350.65', '万亿元', '10月末｜同比 <span class=gc>+7.7%</span>'),
     ('本外币存款余额', '358.81', '万亿元', '另一口径｜同比 +7.8%<br>不能和左边的数加总或替换'))}
{tcard('四项加起来不够 21.97 万亿', '19.40 万亿 + 相差 2.57 万亿（作者计算）',
       '央行用「其中」列出住户、非银行业金融机构、财政性存款、非金融企业四项，合计 19.40 万亿元。用 21.97 减去这四项，还差 2.57 万亿元。报告没有列出其余部门，这里也不猜测是谁。')}
{it('<span class=k>存款增加</span>不等于收入增加',
    '这是账户里人民币存款余额的净增加，不是一份「居民收入排行」。余额变化里还可能包含利息结转、资金在不同账户之间搬家、财政库存变化等。报告没有解释原因，所以这里只摆数字，不把它写成收入提高或钱都去了银行。')}
<div class=src>来源：中国人民银行《2026年10月金融统计数据报告》2026-11-13；2.57万亿元为作者按公布数计算</div>''', total=4)

page(D + "p3.html", 3, f'''{T}{head('贷款谁增谁在减', '2026年1–10月｜人民币贷款增量｜企事业单位含机关团体')}
{duo(('人民币贷款增加', '11.42', '万亿元', '前十个月合计｜初步数'),
     ('人民币贷款余额', '283.33', '万亿元', '10月末｜同比 <span class=gc>+4.7%</span>'))}
<table style="margin-top:20px;table-layout:fixed"><colgroup><col style="width:30%"><col style="width:28%"><col style="width:42%"></colgroup>
<tr class=h><td>部门（人民币贷款）</td><td style="text-align:right;padding-right:28px">前10个月增量</td><td style="text-align:left;padding-left:36px">再拆开看</td></tr>
<tr><td>企事业单位</td><td style="white-space:nowrap;padding-right:28px">+12.39万亿元</td><td style="text-align:left;padding-left:36px;font-family:NSM;font-size:26px;line-height:1.45">短期+4.65万亿<br>中长期+6.69万亿<br>票据融资+9283亿元</td></tr>
<tr><td>住户</td><td style="white-space:nowrap;padding-right:28px">−1.46万亿元</td><td style="text-align:left;padding-left:36px;font-family:NSM;font-size:26px;line-height:1.45">短期−1.41万亿<br>中长期−501亿元</td></tr>
<tr><td>非银金融机构</td><td style="white-space:nowrap;padding-right:28px">−2395亿元</td><td style="text-align:left;padding-left:36px;font-family:NSM;font-size:26px">报告未再分项</td></tr>
</table>
{tcard('怎么读这些「减少」', '净增量 ≠ 借款意愿，也不等于提前还贷',
       '贷款「减少」是这段时间新发放减去还款等之后的净结果。报告没有把新发放和还款分开，不能据此判断大家愿不愿意借钱，也不能写成提前还贷潮。企（事）业单位按报告注3是非金融企业及机关团体，不是只指公司。其中三项相加约12.27万亿，与12.39万亿相差约0.12万亿（作者计算），报告未列其余分项。住户短期与中长期相加约减少1.46万亿（作者验算）。')}
<div class=src>来源：中国人民银行《2026年10月金融统计数据报告》2026-11-13；分项加减为作者按公布数计算</div>''', total=4)

page(D + "p4.html", 4, f'''{T}{head('当月和统计口径', '10月当月由两期累计相减｜M1为2025年起新口径')}
{tcard('10月当月人民币贷款（作者计算）', '11.42万亿 − 11.52万亿 ＝ 减少1000亿元',
       '央行10月报告只给了前十个月累计，没有单列10月当月增量。用前十个月增加11.42万亿元，减去前三季度增加11.52万亿元（2026-10-14报告），得到减少1000亿元。对照余额：9月末283.44万亿元，10月末283.33万亿元，少了0.11万亿元。两个结果因公布值精确到0.01万亿元而不完全相同，比较时用累计相减，不用余额差替代。')}
<table style="margin-top:20px"><tr class=h><td>10月末货币供应量</td><td>余额</td><td>同比</td></tr>
<tr><td>广义货币 M2</td><td>359.06万亿元</td><td>+7.1%</td></tr>
<tr><td>狭义货币 M1</td><td>116.9万亿元</td><td>+4.4%</td></tr>
<tr><td>流通中货币 M0</td><td>15万亿元</td><td>+10.7%</td></tr>
</table>
{it('<span class=k>两个不要混的口径</span>',
    'M1从统计2025年1月数据起改口径，包含个人活期存款和非银行支付机构客户备付金，不宜和旧口径直接比。前十个月净投放现金9023亿元。另外，社会融资规模里「对实体经济发放的人民币贷款」前十个月增加10.91万亿元，不是上面的11.42万亿元。当期数据为初步数。这里只列数字和算法，不预测降息，也不下政策结论。')}
<div class=src>来源：央行《2026年10月金融统计数据报告》2026-11-13；前三季度累计与9月末余额来自《2026年前三季度金融统计数据报告》2026-10-14；当月1000亿元为作者计算</div>''', total=4)

print("gen ok")
