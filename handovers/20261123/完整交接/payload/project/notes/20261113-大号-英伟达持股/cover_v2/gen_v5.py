# -*- coding: utf-8 -*-
import subprocess
from pathlib import Path

DIR = Path('/workspace/xhs/notes/20261113-大号-英伟达持股/cover_v2')
PHOTO = 'file:///workspace/xhs/notes/20261112-大号-科技大佬恋情翻车/photos/huang.jpg'
F = 'file:///home/box/.fonts/'

# Medal icons: circular metallic medals with a star and ribbon. No text.
def medal_svg(cid, c1, c2, c3, rib1, rib2):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 92" width="80" height="92">
  <defs>
    <linearGradient id="{cid}g" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="45%" stop-color="{c2}"/>
      <stop offset="100%" stop-color="{c3}"/>
    </linearGradient>
    <linearGradient id="{cid}r" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{rib1}"/>
      <stop offset="100%" stop-color="{rib2}"/>
    </linearGradient>
    <linearGradient id="{cid}s" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fff" stop-opacity=".9"/>
      <stop offset="100%" stop-color="{c1}" stop-opacity=".3"/>
    </linearGradient>
  </defs>
  <path d="M28 46 L16 90 L32 74 L40 92 L48 74 L64 90 L52 46" fill="url(#{cid}r)"/>
  <path d="M32 74 L40 58 L48 74 L40 92 Z" fill="{c3}" opacity=".55"/>
  <circle cx="40" cy="36" r="30" fill="url(#{cid}g)" stroke="{c1}" stroke-width="2"/>
  <circle cx="40" cy="36" r="23" fill="none" stroke="{c3}" stroke-width="2.2" opacity=".7"/>
  <polygon points="40,16 44.6,30.2 59.5,30.6 47.6,39.6 52.2,53.8 40,45.4 27.8,53.8 32.4,39.6 20.5,30.6 35.4,30.2" fill="url(#{cid}s)" stroke="{c3}" stroke-width="1"/>
</svg>'''

(DIR/'medal_gold.svg').write_text(medal_svg('g','#fff3c4','#f0c94a','#b8870c','#c81e2a','#7a0e18'), encoding='utf-8')
(DIR/'medal_silver.svg').write_text(medal_svg('s','#ffffff','#cfd8e0','#7d8b97','#4a6fa0','#2a4568'), encoding='utf-8')
(DIR/'medal_bronze.svg').write_text(medal_svg('b','#ffd7a8','#d4894a','#8a4e1c','#8b3a1c','#5a2410'), encoding='utf-8')

MG = 'file://' + str(DIR/'medal_gold.svg')
MS = 'file://' + str(DIR/'medal_silver.svg')
MB = 'file://' + str(DIR/'medal_bronze.svg')

html = f'''<!doctype html><html><head><meta charset=utf-8><style>
@font-face{{font-family:NSB;src:url({F}NotoSansSC-Black.otf)}}
@font-face{{font-family:NSM;src:url({F}NotoSansSC-Medium.otf)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1440px;overflow:hidden;background:#07090d;font-family:NSM,'Noto Sans CJK SC',sans-serif;color:#e8edf3;position:relative}}
.bg{{position:absolute;inset:0;background:
  radial-gradient(900px 500px at 88% 6%,rgba(70,160,255,.22),transparent 58%),
  radial-gradient(640px 460px at 4% 42%,rgba(255,40,60,.11),transparent 60%),
  radial-gradient(500px 380px at 70% 78%,rgba(232,195,106,.06),transparent 65%),
  linear-gradient(180deg,#0b0f16 0%,#07090d 55%,#050608 100%)}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(140,190,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(140,190,255,.045) 1px,transparent 1px);background-size:40px 40px;mask-image:linear-gradient(180deg,#000 0%,transparent 46%)}}
.wrap{{position:absolute;inset:0;padding:32px 44px 0}}

.top{{display:flex;align-items:center;gap:14px;font-size:22px;color:#9fb3c8;letter-spacing:1px}}
.brk{{font-family:NSB;background:#ff2d3f;color:#fff;padding:3px 14px;border-radius:6px;font-size:22px;letter-spacing:3px;box-shadow:0 0 24px rgba(255,45,63,.6)}}
.top .dt{{margin-left:auto;font-family:NSB;color:#7fd3ff;letter-spacing:2px}}

h1{{font-family:NSB;font-size:124px;line-height:.95;margin-top:14px;letter-spacing:2px;white-space:nowrap;color:#fff;text-shadow:0 0 40px rgba(120,200,255,.35),0 6px 0 rgba(0,0,0,.6)}}
h1 em{{font-style:normal;background:linear-gradient(180deg,#ff6b6b 0%,#ff1f3a 70%,#c80f28 100%);-webkit-background-clip:text;color:transparent;text-shadow:none;filter:drop-shadow(0 0 26px rgba(255,40,60,.55))}}
h2{{font-family:NSB;font-size:42px;margin-top:12px;color:#e9f3ff;letter-spacing:.5px;white-space:nowrap}}
h2 .pct{{color:#7fd3ff}}
h2 span{{color:#0b0f16;background:#7fd3ff;padding:0 10px;border-radius:6px;margin:0 2px}}

.hero{{margin-top:18px;height:228px;display:flex;border-radius:20px;overflow:hidden;background:linear-gradient(100deg,#141b26,#0e121a);border:1px solid rgba(127,211,255,.35);box-shadow:0 0 0 1px rgba(255,45,63,.15),0 18px 50px rgba(0,0,0,.55),inset 0 0 60px rgba(127,211,255,.06);position:relative}}
.hp{{width:228px;flex:none;background:url({PHOTO}) 50% 18%/cover no-repeat;position:relative;filter:contrast(1.05) saturate(.9)}}
.hp:after{{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent 50%,#141b26 100%),linear-gradient(0deg,rgba(7,9,13,.45),transparent 38%)}}
.htag{{position:absolute;left:14px;top:14px;z-index:2;font-family:NSB;font-size:22px;color:#fff;background:linear-gradient(180deg,#ff3b4e,#d3122b);padding:5px 12px;border-radius:8px;box-shadow:0 0 24px rgba(255,45,63,.5);letter-spacing:1px}}
.ht{{padding:16px 26px 0 8px;flex:1;min-width:0;display:flex;flex-direction:column;justify-content:center}}
.eyebrow{{font-size:22px;color:#9fb3c8;letter-spacing:1px}}
.pctrow{{display:flex;align-items:flex-end;gap:16px;margin-top:2px}}
.hpct{{font-family:NSB;font-size:148px;line-height:.88;letter-spacing:-4px;color:#fff;text-shadow:0 0 48px rgba(127,211,255,.45)}}
.hpct em{{font-style:normal;font-size:50px;letter-spacing:0;margin-left:4px;background:linear-gradient(180deg,#7fd3ff,#3aa7e0);-webkit-background-clip:text;color:transparent}}
.pright{{padding-bottom:10px}}
.share b{{font-family:NSB;font-size:32px;color:#7fd3ff;letter-spacing:.4px}}
.share{{font-size:22px;color:#dfe6ee}}
.mv{{margin-top:4px;font-family:NSB;font-size:28px;color:#fff;letter-spacing:.3px}}
.mv i{{font-style:normal;font-family:NSM;font-size:20px;color:#9fb3c8;margin-right:4px}}
.subh{{margin-top:4px;font-size:18px;color:#8b97a6}}

.sec{{display:flex;align-items:center;gap:12px;margin:16px 0 10px;font-family:NSB;font-size:24px;color:#e9f3ff;letter-spacing:2px;white-space:nowrap}}
.sec i{{font-style:normal;font-family:NSM;font-size:17px;color:#7d8794;letter-spacing:0;white-space:nowrap}}
.sec:after{{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(127,211,255,.5),transparent)}}

.ranks{{display:flex;flex-direction:column;gap:8px}}
.row{{height:110px;background:linear-gradient(160deg,rgba(18,24,35,.92),rgba(12,16,23,.92));border:1px solid rgba(159,179,200,.10);border-radius:14px;padding:10px 18px 10px 12px;display:flex;flex-direction:column;justify-content:center;position:relative;overflow:hidden}}
.row:before{{content:'';position:absolute;left:0;top:14px;bottom:14px;width:3px;border-radius:0 2px 2px 0}}
.row.g1{{border-color:rgba(232,195,106,.38);background:linear-gradient(100deg,rgba(232,195,106,.10),rgba(12,16,23,.95) 42%)}}
.row.g1:before{{background:linear-gradient(180deg,#f3de9a,#c9a227);box-shadow:0 0 10px rgba(232,195,106,.55)}}
.row.g2{{border-color:rgba(196,210,224,.28);background:linear-gradient(100deg,rgba(196,210,224,.08),rgba(12,16,23,.95) 42%)}}
.row.g2:before{{background:linear-gradient(180deg,#e8eef4,#8e9aaa);box-shadow:0 0 10px rgba(200,214,226,.4)}}
.row.g3{{border-color:rgba(196,137,90,.38);background:linear-gradient(100deg,rgba(196,137,90,.11),rgba(12,16,23,.95) 42%)}}
.row.g3:before{{background:linear-gradient(180deg,#e0b07a,#a86b38);box-shadow:0 0 10px rgba(196,137,90,.45)}}
.row.g4:before{{background:rgba(127,211,255,.28)}}
.row.me{{height:122px;border:1px solid rgba(255,45,63,.58);background:linear-gradient(100deg,rgba(255,45,63,.12),rgba(12,16,23,.96) 48%);box-shadow:0 0 28px rgba(255,45,63,.18),inset 0 0 40px rgba(255,45,63,.04)}}
.row.me:before{{background:linear-gradient(180deg,#ff6b78,#c80f28);box-shadow:0 0 12px rgba(255,45,63,.6);top:12px;bottom:12px}}

.head{{display:flex;align-items:center}}
.rkbox{{width:54px;flex:none;display:flex;align-items:center;justify-content:flex-start;padding-left:8px}}
.rk{{font-family:NSB;font-size:30px;color:#7fd3ff;letter-spacing:1px;line-height:1}}
.row.g1 .rk{{color:#f3de9a}}
.row.g2 .rk{{color:#d5dee6}}
.row.g3 .rk{{color:#e0b07a}}
.row.me .rk{{color:#ff6b78;font-size:32px}}
.ico{{width:44px;height:50px;flex:none;margin-right:10px;background-size:contain;background-repeat:no-repeat;background-position:center;filter:drop-shadow(0 2px 6px rgba(0,0,0,.45))}}
.ico.gold{{background-image:url({MG})}}
.ico.silver{{background-image:url({MS})}}
.ico.bronze{{background-image:url({MB})}}
.av{{width:48px;height:48px;border-radius:50%;flex:none;margin-right:12px;background:url({PHOTO}) 50% 18%/cover no-repeat;border:2px solid rgba(255,45,63,.7);box-shadow:0 0 14px rgba(255,45,63,.35)}}
.nm{{flex:1;min-width:0}}
.n{{font-family:NSB;font-size:34px;color:#fff;line-height:1.15;display:flex;align-items:center;gap:10px;white-space:nowrap}}
.row.me .n{{font-size:36px}}
.tag{{font-family:NSB;font-size:16px;color:#fff;background:linear-gradient(180deg,#ff3b4e,#d3122b);padding:2px 8px;border-radius:5px;letter-spacing:1px;box-shadow:0 0 10px rgba(255,45,63,.4)}}
.en{{font-size:17px;color:#8b97a6;margin-top:2px;white-space:nowrap}}
.nums{{text-align:right;flex:none;padding-left:8px}}
.vp{{font-family:NSB;font-size:50px;line-height:1;color:#fff;letter-spacing:-1px}}
.row.me .vp{{font-size:56px}}
.vp i{{font-style:normal;font-family:NSM;font-size:20px;color:#8b97a6;margin-right:3px;letter-spacing:0}}
.vp span{{font-size:22px;margin-left:1px;color:#7fd3ff}}
.row.g1 .vp span{{color:#f3de9a}}
.row.g2 .vp span{{color:#c5d0db}}
.row.g3 .vp span{{color:#e0b07a}}
.row.me .vp span{{color:#ff6b78}}
.sh{{font-size:18px;color:#c5d0db;margin-top:3px;letter-spacing:.2px;white-space:nowrap}}
.sh b{{font-family:NSB;color:#fff;font-weight:normal}}
.row.g1 .sh b{{color:#f3de9a}}
.row.me .sh b{{color:#ff8a95}}
.barwrap{{height:6px;background:rgba(22,28,38,.95);border-radius:4px;overflow:hidden;margin-top:8px;margin-left:8px}}
.row.me .barwrap{{height:8px;margin-top:9px}}
.bar{{height:100%;border-radius:4px;background:linear-gradient(90deg,#9ee7ff,#7fd3ff 50%,#3aa7e0);box-shadow:0 0 10px rgba(127,211,255,.4)}}
.row.g1 .bar{{background:linear-gradient(90deg,#f8e7b0,#e8c36a 50%,#c9a227);box-shadow:0 0 12px rgba(232,195,106,.5)}}
.row.g2 .bar{{background:linear-gradient(90deg,#f4f7fa,#b9c5d0 50%,#8e9aaa);box-shadow:0 0 10px rgba(200,214,226,.35)}}
.row.g3 .bar{{background:linear-gradient(90deg,#f0c99a,#d08a48 50%,#a86b38);box-shadow:0 0 10px rgba(196,137,90,.4)}}
.row.me .bar{{background:linear-gradient(90deg,#ff8a95,#ff2d3f 50%,#c80f28);box-shadow:0 0 14px rgba(255,45,63,.55)}}

.foot{{position:absolute;left:44px;right:44px;bottom:18px;font-size:16px;line-height:1.5;color:#6c7684}}
</style></head><body>
<div class=bg></div><div class=grid></div>
<div class=wrap>
  <div class=top><span class=brk>持股</span><span>一图看懂｜英伟达最新持股排名</span><span class=dt>2026.11.13</span></div>
  <h1>英伟达<em>持股排名</em></h1>
  <h2>黄仁勋持股<span class=pct>3.58%</span>，仍是<span>最大个人股东</span></h2>

  <div class=hero>
    <div class=hp><div class=htag>已辞职（官方）</div></div>
    <div class=ht>
      <div class=eyebrow>黄仁勋 · 受益所有权 · 在这份排名里排第 5</div>
      <div class=pctrow>
        <div class=hpct>3.58<em>%</em></div>
        <div class=pright>
          <div class=share><b>870,604,104</b> 股</div>
          <div class=mv><i>约合</i>1,447 亿美元</div>
          <div class=subh>代理声明截至 2026-03-23</div>
        </div>
      </div>
    </div>
  </div>

  <div class=sec>前五名<i>机构 13F 截至 6 月 30 日（约数）；黄仁勋为 3 月 23 日代理声明</i></div>
  <div class=ranks>
    <div class="row g1">
      <div class=head>
        <div class=rkbox><div class=rk>01</div></div>
        <div class="ico gold"></div>
        <div class=nm><div class=n>贝莱德公司</div><div class=en>BlackRock, Inc. · 13F · 截至 6 月 30 日</div></div>
        <div class=nums><div class=vp><i>约</i>8.0<span>%</span></div><div class=sh>约合 <b>3,200 亿美元</b></div></div>
      </div>
      <div class=barwrap><div class=bar style="width:100%"></div></div>
    </div>
    <div class="row g2">
      <div class=head>
        <div class=rkbox><div class=rk>02</div></div>
        <div class="ico silver"></div>
        <div class=nm><div class=n>先锋资本管理</div><div class=en>Vanguard Capital Management · 13F · 截至 6 月 30 日</div></div>
        <div class=nums><div class=vp><i>约</i>6.4<span>%</span></div><div class=sh>约合 <b>2,560 亿美元</b></div></div>
      </div>
      <div class=barwrap><div class=bar style="width:80%"></div></div>
    </div>
    <div class="row g3">
      <div class=head>
        <div class=rkbox><div class=rk>03</div></div>
        <div class="ico bronze"></div>
        <div class=nm><div class=n>富达管理公司</div><div class=en>FMR LLC · 13F · 截至 6 月 30 日</div></div>
        <div class=nums><div class=vp><i>约</i>4.2<span>%</span></div><div class=sh>约合 <b>1,680 亿美元</b></div></div>
      </div>
      <div class=barwrap><div class=bar style="width:52.5%"></div></div>
    </div>
    <div class="row g4">
      <div class=head>
        <div class=rkbox><div class=rk>04</div></div>
        <div class=nm style="margin-left:54px"><div class=n>州街公司</div><div class=en>State Street Corporation · 13F · 截至 6 月 30 日</div></div>
        <div class=nums><div class=vp><i>约</i>4.2<span>%</span></div><div class=sh>约合 <b>1,680 亿美元</b></div></div>
      </div>
      <div class=barwrap><div class=bar style="width:52%"></div></div>
    </div>
    <div class="row me">
      <div class=head>
        <div class=rkbox><div class=rk>05</div></div>
        <div class=av></div>
        <div class=nm><div class=n>黄仁勋<span class=tag>最大个人股东</span></div><div class=en>受益所有权 · 870,604,104 股 · 代理声明</div></div>
        <div class=nums><div class=vp>3.58<span>%</span></div><div class=sh>约合 <b>1,447 亿美元</b></div></div>
      </div>
      <div class=barwrap><div class=bar style="width:44.8%"></div></div>
    </div>
  </div>

  <div class=foot>来源：机构为 SEC 13F，截至 2026-06-30，比例为约数｜黄仁勋为英伟达 2026 年代理声明，截至 2026-03-23。制图 2026/11/13。<br>市值按 2026 年 11 月 12 日收盘价 166.19 美元测算。机构代客户持有，与创始人股份不是一类。不构成投资建议。照片仅作身份识别。</div>
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
