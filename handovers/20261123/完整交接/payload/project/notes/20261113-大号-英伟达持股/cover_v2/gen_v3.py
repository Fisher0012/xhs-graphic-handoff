# -*- coding: utf-8 -*-
import subprocess
from pathlib import Path

DIR = Path('/workspace/xhs/notes/20261113-大号-英伟达持股/cover_v2')
PHOTO = 'file:///workspace/xhs/notes/20261112-大号-科技大佬恋情翻车/photos/huang.jpg'
F = 'file:///home/box/.fonts/'

# 13F Q2 2026 (as of 2026-06-30) percentages shown as 约, because
# aggregator share counts disagree at the exact-share level and % depends
# on the outstanding-share denominator. Ballpark is consistent across
# Yahoo Finance and VCP Scanner Q2 tables:
# BlackRock ~8.0–8.06%, Vanguard CM ~6.36–6.39%, FMR ~4.2%, State Street ~4.17–4.19%, Geode ~2.50%.
# Huang is exact: DEF 14A as of 2026-03-23, 870,604,104 / 3.58%.
# Bar widths relative to 8.0.

html = f'''<!doctype html><html><head><meta charset=utf-8><style>
@font-face{{font-family:NSB;src:url({F}NotoSansSC-Black.otf)}}
@font-face{{font-family:NSM;src:url({F}NotoSansSC-Medium.otf)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1440px;overflow:hidden;background:#07090d;font-family:NSM,'Noto Sans CJK SC',sans-serif;color:#e8edf3;position:relative}}
.bg{{position:absolute;inset:0;background:
  radial-gradient(900px 520px at 85% 8%,rgba(70,160,255,.22),transparent 60%),
  radial-gradient(700px 500px at 0% 48%,rgba(255,40,60,.10),transparent 60%),
  linear-gradient(180deg,#0b0f16 0%,#07090d 55%,#050608 100%)}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(140,190,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(140,190,255,.045) 1px,transparent 1px);background-size:40px 40px;mask-image:linear-gradient(180deg,#000 0%,transparent 48%)}}
.wrap{{position:absolute;inset:0;padding:36px 46px 0}}
.top{{display:flex;align-items:center;gap:14px;font-size:22px;color:#9fb3c8;letter-spacing:1px}}
.brk{{font-family:NSB;background:#ff2d3f;color:#fff;padding:3px 14px;border-radius:6px;font-size:22px;letter-spacing:3px;box-shadow:0 0 24px rgba(255,45,63,.6)}}
.top .dt{{margin-left:auto;font-family:NSB;color:#7fd3ff;letter-spacing:2px}}
h1{{font-family:NSB;font-size:164px;line-height:.98;margin-top:14px;letter-spacing:2px;white-space:nowrap;color:#fff;text-shadow:0 0 40px rgba(120,200,255,.35),0 6px 0 rgba(0,0,0,.6)}}
h1 em{{font-style:normal;background:linear-gradient(180deg,#ff6b6b 0%,#ff1f3a 70%,#c80f28 100%);-webkit-background-clip:text;color:transparent;text-shadow:none;filter:drop-shadow(0 0 26px rgba(255,40,60,.55))}}
h2{{font-family:NSB;font-size:52px;margin-top:10px;color:#e9f3ff;letter-spacing:1px;white-space:nowrap}}
h2 span{{color:#0b0f16;background:#7fd3ff;padding:0 10px;border-radius:6px;margin:0 2px}}

.sec{{display:flex;align-items:baseline;gap:12px;margin:22px 0 12px;font-family:NSB;font-size:26px;color:#e9f3ff;letter-spacing:2px}}
.sec i{{font-style:normal;font-family:NSM;font-size:18px;color:#7d8794;letter-spacing:0;flex:1}}
.sec:after{{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(127,211,255,.55),transparent);align-self:center;min-width:40px}}

.ranks{{display:flex;flex-direction:column;gap:10px}}
.row{{height:122px;background:linear-gradient(160deg,#121823,#0c1017);border:1px solid rgba(159,179,200,.16);border-radius:16px;padding:12px 22px 12px;position:relative;display:flex;flex-direction:column;justify-content:space-between}}
.row.me{{border:1px solid rgba(255,45,63,.6);box-shadow:0 0 28px rgba(255,45,63,.2),inset 0 0 36px rgba(255,45,63,.05);height:132px}}
.head{{display:flex;align-items:center}}
.rk{{font-family:NSB;font-size:32px;color:#7fd3ff;width:70px;letter-spacing:1px;flex:none}}
.row.me .rk{{color:#ff6b78}}
.av{{width:42px;height:42px;border-radius:50%;flex:none;margin-right:12px;display:flex;align-items:center;justify-content:center;font-family:NSB;font-size:20px;color:#0b0f16;background:#7fd3ff;box-shadow:0 0 12px rgba(127,211,255,.4)}}
.av.photo{{background:url({PHOTO}) 50% 18%/cover no-repeat;border:2px solid rgba(255,45,63,.7);box-shadow:0 0 14px rgba(255,45,63,.35);color:transparent}}
.nm{{flex:1;min-width:0}}
.n{{font-family:NSB;font-size:32px;color:#fff;line-height:1.1;display:flex;align-items:center;gap:8px}}
.tag{{font-family:NSB;font-size:16px;color:#fff;background:linear-gradient(180deg,#ff3b4e,#d3122b);padding:2px 8px;border-radius:5px;letter-spacing:1px;box-shadow:0 0 12px rgba(255,45,63,.45)}}
.en{{font-size:16px;color:#9fb3c8;margin-top:2px}}
.nums{{text-align:right;flex:none}}
.vp{{font-family:NSB;font-size:52px;line-height:1;color:#fff;letter-spacing:-1px}}
.vp i{{font-style:normal;font-family:NSM;font-size:22px;color:#9fb3c8;margin-right:4px;letter-spacing:0}}
.vp span{{font-size:24px;margin-left:1px;color:#7fd3ff}}
.row.me .vp span{{color:#ff6b78}}
.sh{{font-size:16px;color:#9fb3c8;margin-top:3px;letter-spacing:.2px}}
.barwrap{{height:12px;background:#161c26;border-radius:7px;overflow:hidden;margin-top:6px;box-shadow:inset 0 0 8px rgba(0,0,0,.5)}}
.bar{{height:12px;border-radius:7px;background:linear-gradient(90deg,#9ee7ff,#7fd3ff 40%,#3aa7e0);box-shadow:0 0 14px rgba(127,211,255,.55)}}
.row.me .bar{{background:linear-gradient(90deg,#ff8a95,#ff2d3f 50%,#c80f28);box-shadow:0 0 16px rgba(255,45,63,.55)}}

.note{{margin-top:14px;font-size:20px;color:#9fb3c8;line-height:1.45}}
.note b{{color:#7fd3ff;font-family:NSB;font-weight:normal}}
.foot{{position:absolute;left:46px;right:46px;bottom:20px;font-size:16px;line-height:1.45;color:#6c7684}}
</style></head><body>
<div class=bg></div><div class=grid></div>
<div class=wrap>
  <div class=top><span class=brk>持股</span><span>一图看懂｜英伟达持股怎么排</span><span class=dt>2026.11.13</span></div>
  <h1>黄仁勋<em>辞职了</em></h1>
  <h2>股份还在，<span>怎么排</span></h2>

  <div class=sec>持股排名<i>机构是 13F，截至 6 月 30 日，比例为约数；黄仁勋是 3 月 23 日代理声明</i></div>
  <div class=ranks>
    <div class=row>
      <div class=head>
        <div class=rk>01</div>
        <div class=av>贝</div>
        <div class=nm><div class=n>贝莱德</div><div class=en>BlackRock, Inc. · 13F</div></div>
        <div class=nums><div class=vp><i>约</i>8.0<span>%</span></div><div class=sh>截至 2026-06-30</div></div>
      </div>
      <div class=barwrap><div class=bar style="width:100%"></div></div>
    </div>
    <div class=row>
      <div class=head>
        <div class=rk>02</div>
        <div class=av>先</div>
        <div class=nm><div class=n>先锋</div><div class=en>Vanguard Capital Management · 13F</div></div>
        <div class=nums><div class=vp><i>约</i>6.4<span>%</span></div><div class=sh>截至 2026-06-30</div></div>
      </div>
      <div class=barwrap><div class=bar style="width:80%"></div></div>
    </div>
    <div class=row>
      <div class=head>
        <div class=rk>03</div>
        <div class=av>富</div>
        <div class=nm><div class=n>富达</div><div class=en>FMR LLC · 13F</div></div>
        <div class=nums><div class=vp><i>约</i>4.2<span>%</span></div><div class=sh>截至 2026-06-30</div></div>
      </div>
      <div class=barwrap><div class=bar style="width:52.5%"></div></div>
    </div>
    <div class=row>
      <div class=head>
        <div class=rk>04</div>
        <div class=av>州</div>
        <div class=nm><div class=n>州街</div><div class=en>State Street Corporation · 13F</div></div>
        <div class=nums><div class=vp><i>约</i>4.2<span>%</span></div><div class=sh>截至 2026-06-30</div></div>
      </div>
      <div class=barwrap><div class=bar style="width:52%"></div></div>
    </div>
    <div class="row me">
      <div class=head>
        <div class=rk>05</div>
        <div class="av photo"></div>
        <div class=nm><div class=n>黄仁勋<span class=tag>已辞职（官方）</span></div><div class=en>最大个人股东 · 受益所有权 · 870,604,104 股</div></div>
        <div class=nums><div class=vp>3.58<span>%</span></div><div class=sh>代理声明 2026-03-23</div></div>
      </div>
      <div class=barwrap><div class=bar style="width:44.8%"></div></div>
    </div>
    <div class=row>
      <div class=head>
        <div class=rk>06</div>
        <div class=av>G</div>
        <div class=nm><div class=n>Geode</div><div class=en>Geode Capital Management · 13F</div></div>
        <div class=nums><div class=vp><i>约</i>2.5<span>%</span></div><div class=sh>截至 2026-06-30</div></div>
      </div>
      <div class=barwrap><div class=bar style="width:31.3%"></div></div>
    </div>
  </div>

  <div class=note>第 7 名起大约 2% 以下，逐步稀释，封面只排有分量的这几家。机构是代客户持有，与创始人股份不是一类。一股一票，3.58% 不是控制权。</div>

  <div class=foot>来源：机构为 SEC 13F，持股截至 2026-06-30，比例为约数｜黄仁勋为英伟达 2026 年代理声明，截至 2026-03-23。制图 2026/11/13。<br>风险提示：本文整理公开文件，不构成任何投资建议。投资有风险，入市需谨慎。照片仅作身份识别。</div>
</div>
</body></html>'''

(DIR/'00_封面.html').write_text(html, encoding='utf-8')
out = DIR/'00_封面.png'
r = subprocess.run([
    'google-chrome','--headless=new','--no-sandbox','--disable-gpu',
    '--allow-file-access-from-files','--hide-scrollbars',
    '--force-device-scale-factor=2','--window-size=1080,1440',
    '--virtual-time-budget=5000',
    f'--screenshot={out}',
    'file://'+str(DIR/'00_封面.html')
], capture_output=True)
print('return', r.returncode, out.exists(), out.stat().st_size if out.exists() else 0)
if r.stderr:
    err = r.stderr.decode() if isinstance(r.stderr, bytes) else r.stderr
    print(err[-800:])
