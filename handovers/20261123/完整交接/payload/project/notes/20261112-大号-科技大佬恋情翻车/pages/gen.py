import subprocess,os
P='../photos/'; F='file:///home/box/.fonts/'
BASE=f'''@font-face{{font-family:NSB;src:url({F}NotoSansSC-Black.otf)}}
@font-face{{font-family:NSM;src:url({F}NotoSansSC-Medium.otf)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1440px;overflow:hidden;background:#07090d;font-family:NSM,'Noto Sans CJK SC',sans-serif;color:#e8edf3;position:relative}}
.bg{{position:absolute;inset:0;background:radial-gradient(900px 520px at 85% 8%,rgba(70,160,255,.22),transparent 60%),radial-gradient(700px 500px at 0% 45%,rgba(255,40,60,.09),transparent 60%),linear-gradient(180deg,#0b0f16 0%,#07090d 55%,#050608 100%)}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(140,190,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(140,190,255,.045) 1px,transparent 1px);background-size:40px 40px;mask-image:linear-gradient(180deg,#000 0%,transparent 45%)}}
.wrap{{position:absolute;inset:0;padding:38px 46px 0}}
.top{{display:flex;align-items:center;gap:14px;font-size:22px;color:#9fb3c8;letter-spacing:1px}}
.brk{{font-family:NSB;background:#ff2d3f;color:#fff;padding:3px 14px;border-radius:6px;font-size:22px;letter-spacing:3px;box-shadow:0 0 24px rgba(255,45,63,.6)}}
.brk.b{{background:#7fd3ff;color:#0b0f16;box-shadow:0 0 24px rgba(127,211,255,.5)}}
.top .dt{{margin-left:auto;font-family:NSB;color:#7fd3ff;letter-spacing:2px}}
.k{{font-family:NSB;color:#7fd3ff}} .red{{color:#ff3b4e}}
h1{{font-family:NSB;color:#fff;line-height:1.08;white-space:nowrap;text-shadow:0 0 40px rgba(120,200,255,.3),0 5px 0 rgba(0,0,0,.6)}}
h1 em{{font-style:normal;color:#ff2d3f;text-shadow:0 0 28px rgba(255,40,60,.55)}}
.foot{{position:absolute;left:46px;right:46px;bottom:24px;font-size:16.5px;line-height:1.5;color:#6c7684}}
.av{{border-radius:50%;background-repeat:no-repeat;border:2px solid rgba(127,211,255,.55);box-shadow:0 0 16px rgba(127,211,255,.25);flex:none}}
'''
def render(name):
    subprocess.run(['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--allow-file-access-from-files','--hide-scrollbars','--force-device-scale-factor=2','--window-size=1080,1440','--virtual-time-budget=4000',f'--screenshot={name}.png','file://'+os.path.abspath(name+'.html')],capture_output=True)
def page(name,css,body):
    open(name+'.html','w').write(f'<!doctype html><html><head><meta charset=utf-8><style>{BASE}{css}</style></head><body><div class=bg></div><div class=grid></div><div class=wrap>{body}</div></body></html>')
    render(name)

# ---------- 01 ----------
beats=[('01','向员工承认对妻子不忠','本人向员工承认','c'),
       ('02','《纽约时报》报道其与直属下属的关系','媒体报道 · 本人未公开承认','y'),
       ('03','美方认定相关女子为中国间谍','美方认定 · 未经法庭判决','y'),
       ('04','英伟达官网新闻稿：辞去总裁、CEO和董事，即刻生效；<br>CFO克雷斯任临时CEO','官方 · 2026-11-12','r')]
bl=''.join(f'<div class="bt {c}"><div class=bn>{n}</div><div class=bx><div class=btx>{t}</div><span class=bdg>{b}</span></div></div>' for n,t,b,c in beats)
css1='''h1.a{font-size:60px;margin-top:22px;color:#cfe6ff}
h1.b{font-size:94px;margin-top:2px}
.hero{margin-top:26px;display:flex;gap:18px;height:470px}
.ph{width:360px;flex:none;border-radius:20px;background:url(../photos/huang.jpg) 50% 15%/cover no-repeat;position:relative;overflow:hidden;border:1px solid rgba(127,211,255,.35)}
.ph:after{content:'';position:absolute;inset:0;background:linear-gradient(0deg,rgba(7,9,13,.92) 0%,transparent 42%)}
.ph .cap{position:absolute;left:22px;bottom:18px;z-index:2}
.ph .cap b{font-family:NSB;font-size:46px;color:#fff;display:block;line-height:1.1}
.ph .cap span{font-size:19px;color:#9fb3c8}
.res{flex:1;border-radius:20px;background:linear-gradient(160deg,#151c28,#0d1118);border:1px solid rgba(255,45,63,.45);box-shadow:0 0 40px rgba(255,45,63,.12);padding:24px 28px;display:flex;flex-direction:column}
.res .lab{font-family:NSB;font-size:20px;color:#ff6b78;letter-spacing:3px}
.res .row{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid rgba(159,179,200,.14);padding:15px 0 13px}
.res .row:last-child{border:none}
.res .row span{font-size:21px;color:#9fb3c8}
.res .row b{font-family:NSB;font-size:32px;color:#fff}
.res .row b.r{color:#ff3b4e}
.sec{display:flex;align-items:center;gap:14px;margin:30px 0 14px;font-family:NSB;font-size:28px;color:#e9f3ff;letter-spacing:2px}
.sec:after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(127,211,255,.6),transparent)}
.sec i{font-style:normal;font-family:NSM;font-size:18px;color:#7d8794;letter-spacing:0}
.bt{display:flex;gap:16px;margin-bottom:14px;align-items:stretch}
.bn{width:62px;flex:none;font-family:NSB;font-size:30px;color:#7fd3ff;display:flex;align-items:center;justify-content:center;border-radius:14px;background:rgba(127,211,255,.08);border:1px solid rgba(127,211,255,.3)}
.bx{flex:1;border-radius:14px;background:linear-gradient(100deg,#131a25,#0d1118);border:1px solid rgba(159,179,200,.16);padding:14px 20px;display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:86px}
.btx{font-size:25px;line-height:1.4;color:#fff;white-space:nowrap}
.bdg{flex:none;font-family:NSB;font-size:17px;padding:3px 12px;border-radius:6px;white-space:nowrap}
.c .bdg{color:#7fd3ff;border:1px solid #7fd3ff;background:rgba(127,211,255,.1)}
.y .bdg{color:#ffc857;border:1px solid #ffc857;background:rgba(255,200,87,.1)}
.r .bdg{color:#fff;background:#ff2d3f}
.r .bx{border-color:rgba(255,45,63,.55);background:linear-gradient(100deg,#221319,#0d1118)}
.r .bn{color:#ff3b4e;background:rgba(255,45,63,.1);border-color:rgba(255,45,63,.45)}
.tip{margin-top:6px;font-size:19px;line-height:1.55;color:#9fb3c8;padding:12px 18px;border-left:3px solid #ffc857;background:rgba(255,200,87,.05);border-radius:0 10px 10px 0}
.tip b{font-family:NSB;color:#ffc857}'''
page('01_黄仁勋辞职始末',css1,f'''
<div class=top><span class=brk>突发</span><span>英伟达一把手变动｜事件梳理</span><span class=dt>2026.11.12</span></div>
<h1 class=a>英伟达官网宣布：</h1>
<h1 class=b>黄仁勋<em>辞职</em>，即刻生效</h1>
<div class=hero><div class=ph><div class=cap><b>黄仁勋</b><span>英伟达创始人、总裁兼CEO</span></div></div>
<div class=res><div class=lab>官方结果｜英伟达官网新闻稿</div>
<div class=row><span>辞去职务</span><b class=r>总裁、CEO、董事</b></div>
<div class=row><span>生效时间</span><b>即刻生效</b></div>
<div class=row><span>临时CEO</span><b>CFO 克雷斯</b></div>
<div class=row><span>发布日期</span><b>2026-11-12</b></div>
<div class=row><span>官方用词</span><b>辞职</b></div></div></div>
<div class=sec>四个关键信息<i>按口径标注：官方 / 本人 / 媒体 / 美方</i></div>
{bl}
<div class=tip><b>看清口径：</b>只有第04条是英伟达官方公告；「媒体报道」「美方认定」不等于公司或法院的结论。</div>
<div class=foot>来源：英伟达官网新闻稿 2026-11-12；其余按公开报道整理，口径见标签。制图 2026/11/12。本文不构成任何投资建议。<br>照片：Wikimedia Commons（CC BY-SA 4.0，Anderseidesvik）。</div>''')

# ---------- 02 ----------
def chip(ph,pos,size,n,ry,ev):
    return f'<div class=chip><div class=av style="width:96px;height:96px;background-image:url({P}{ph});background-position:{pos};background-size:{size}"></div><div class=cn>{n}</div><div class=cr>{ry}</div><div class=ce>{ev}</div></div>'
K=chip('krzanich.jpg','50% 22%','190%','布莱恩·科再奇','英特尔CEO · 2018','与员工交往，违反<br>禁止办公室恋情政策')
H=chip('hurd.jpg','52% 18%','200%','马克·赫德','惠普CEO · 2010','与承包商关系被查，<br>涉及报销问题')
S=chip('stonecipher.jpg','50% 13%','200%','哈里·斯通西弗','波音总裁兼CEO · 2005','与女高管关系，<br>违反行为准则')
Z=chip('zucker.jpg','56% 20%','220%','杰夫·扎克','CNN全球总裁 · 2022','未申报与首席营销官<br>的恋情')
E=chip('easterbrook.jpg','52% 33%','160%','史蒂夫·伊斯布鲁克','麦当劳总裁兼CEO · 2019','与员工不当关系')
FX=chip('freixe.jpg','56% 28%','200%','洛朗·弗雷克斯','雀巢CEO · 2025','与直属下属交往<br>且未申报')
R=chip('rubin.jpg','45% 25%','150%','安迪·鲁宾','谷歌Android之父 · 2014','因性不当行为指控离开谷歌，<br>本人否认；2018年曝光')
G=chip('gates.jpg','50% 16%','190%','比尔·盖茨','微软联合创始人 · 2020','公司调查期间辞去董事，<br>当时已非CEO')
css2='''h1.a{font-size:66px;margin-top:22px;color:#cfe6ff}
h1.b{font-size:86px;margin-top:0}
.sub{font-size:22px;color:#9fb3c8;margin-top:10px}
.grp{margin-top:24px;border-radius:18px;background:linear-gradient(160deg,#131a25,#0c1017);border:1px solid rgba(159,179,200,.16);padding:16px 16px 18px;position:relative}
.gh{display:flex;align-items:center;gap:12px;margin-bottom:12px}
.gt{font-family:NSB;font-size:24px;padding:2px 14px;border-radius:7px;line-height:36px}
.gt.r{color:#ff6b78;background:rgba(255,45,63,.16);border:1px solid #ff2d3f}
.gt.o{color:#fff;background:#ff2d3f;box-shadow:0 0 20px rgba(255,45,63,.45)}
.gt.b{color:#7fd3ff;background:rgba(127,211,255,.1);border:1px solid #7fd3ff}
.gt.g{color:#5df0ae;background:rgba(61,220,151,.14);border:1px solid #3ddc97}
.gh span{font-size:19px;color:#9fb3c8}
.chips{display:flex;gap:10px}
.chip{flex:1;min-width:0;display:flex;flex-direction:column;align-items:center;text-align:center;padding:4px 0}
.cn{font-family:NSB;font-size:23px;color:#fff;margin-top:10px;white-space:nowrap}
.cr{font-size:16px;color:#7fd3ff;margin-top:2px;white-space:nowrap}
.ce{font-size:17px;line-height:1.45;color:#cfd7e0;margin-top:6px;white-space:nowrap}
.two{display:flex;gap:14px}.two .grp{flex:1}
.bz{display:flex;align-items:center;gap:22px;border-color:rgba(61,220,151,.45);background:linear-gradient(100deg,#0f1f1a,#0c1017)}
.bz .t b{font-family:NSB;font-size:30px;color:#fff}.bz .t span{font-size:18px;color:#7fd3ff;margin-left:10px}
.bz .t p{font-size:21px;color:#dfe6ee;margin-top:6px}
.take{margin-top:26px;border-radius:16px;padding:18px 24px;background:linear-gradient(100deg,rgba(127,211,255,.14),rgba(127,211,255,.03));border:1px solid rgba(127,211,255,.45)}
.take .l{font-family:NSB;font-size:20px;color:#7fd3ff;letter-spacing:3px}
.take p{font-size:25px;line-height:1.5;color:#fff;margin-top:4px}
.take p b{font-family:NSB;color:#7fd3ff}'''
page('02_九个先例结局对照',css2,f'''
<div class=top><span class="brk b">对照</span><span>9位大佬的恋情代价｜按结局分组</span><span class=dt>2005—2025</span></div>
<h1 class=a>前车之鉴：</h1>
<h1 class=b>同样是恋情，<em>结局</em>不一样</h1>
<div class=grp><div class=gh><span class="gt o">辞职</span><span>4人｜以辞职方式离开职位</span></div><div class=chips>{K}{H}{S}{Z}</div></div>
<div class=two>
<div class=grp><div class=gh><span class="gt r">被解雇</span><span>2人</span></div><div class=chips>{E}{FX}</div></div>
<div class=grp><div class=gh><span class="gt b">离职 / 辞去董事</span><span>2人</span></div><div class=chips>{R}{G}</div></div></div>
<div class="grp bz"><div class=av style="width:104px;height:104px;background-image:url({P}bezos.jpg);background-position:40% 14%;background-size:190%;border-color:#3ddc97"></div>
<div class=t><span class="gt g">未因此辞职</span><div style="margin-top:8px"><b>杰夫·贝佐斯</b><span>亚马逊创始人、时任CEO · 2019</span></div><p>恋情曝光，仍任CEO，2021年才交棒</p></div></div>
<div class=take><div class=l>规律</div><p>常见原因是<b>违反公司对管理层的办公室恋情／未申报政策</b>，<br>不是「恋爱就一定辞职」。</p></div>
<div class=foot>按此前公开报道整理；不构成任何投资建议。制图 2026/11/12。<br>照片来源与封面一致：Wikimedia Commons（CC BY/BY-SA/公有领域）；斯通西弗、伊斯布鲁克为公司官方肖像，仅作身份识别。</div>''')
