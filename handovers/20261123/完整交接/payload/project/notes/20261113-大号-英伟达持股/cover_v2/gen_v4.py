# -*- coding: utf-8 -*-
import subprocess
from pathlib import Path

DIR = Path('/workspace/xhs/notes/20261113-大号-英伟达持股/cover_v2')
PHOTO = 'file:///workspace/xhs/notes/20261112-大号-科技大佬恋情翻车/photos/huang.jpg'
F = 'file:///home/box/.fonts/'

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
.wrap{{position:absolute;inset:0;padding:34px 46px 0}}

.top{{display:flex;align-items:center;gap:14px;font-size:22px;color:#9fb3c8;letter-spacing:1px}}
.brk{{font-family:NSB;background:#ff2d3f;color:#fff;padding:3px 14px;border-radius:6px;font-size:22px;letter-spacing:3px;box-shadow:0 0 24px rgba(255,45,63,.6)}}
.top .dt{{margin-left:auto;font-family:NSB;color:#7fd3ff;letter-spacing:2px}}

.brand{{font-family:NSB;font-size:36px;color:#7fd3ff;letter-spacing:8px;margin-top:16px}}
h1{{font-family:NSB;font-size:172px;line-height:.92;margin-top:2px;letter-spacing:8px;white-space:nowrap;color:#fff;text-shadow:0 0 40px rgba(120,200,255,.35),0 6px 0 rgba(0,0,0,.6)}}
h1 em{{font-style:normal;background:linear-gradient(180deg,#ff6b6b 0%,#ff1f3a 70%,#c80f28 100%);-webkit-background-clip:text;color:transparent;text-shadow:none;filter:drop-shadow(0 0 26px rgba(255,40,60,.55));letter-spacing:8px}}
h2{{font-family:NSB;font-size:40px;margin-top:12px;color:#e9f3ff;letter-spacing:1.5px;white-space:nowrap}}
h2 span{{color:#0b0f16;background:#7fd3ff;padding:0 10px;border-radius:6px;margin:0 2px}}

.hero{{margin-top:20px;height:236px;display:flex;border-radius:20px;overflow:hidden;background:linear-gradient(100deg,#141b26,#0e121a);border:1px solid rgba(127,211,255,.35);box-shadow:0 0 0 1px rgba(255,45,63,.15),0 18px 50px rgba(0,0,0,.55),inset 0 0 60px rgba(127,211,255,.06);position:relative}}
.hp{{width:236px;flex:none;background:url({PHOTO}) 50% 18%/cover no-repeat;position:relative;filter:contrast(1.05) saturate(.9)}}
.hp:after{{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent 50%,#141b26 100%),linear-gradient(0deg,rgba(7,9,13,.45),transparent 38%)}}
.htag{{position:absolute;left:14px;top:14px;z-index:2;font-family:NSB;font-size:20px;color:#fff;background:linear-gradient(180deg,#ff3b4e,#d3122b);padding:5px 12px;border-radius:8px;box-shadow:0 0 24px rgba(255,45,63,.5);letter-spacing:1px}}
.ht{{padding:18px 28px 0 10px;flex:1;min-width:0;display:flex;flex-direction:column;justify-content:center}}
.eyebrow{{font-size:20px;color:#9fb3c8;letter-spacing:1px}}
.pctrow{{display:flex;align-items:flex-end;gap:18px;margin-top:2px}}
.pct{{font-family:NSB;font-size:148px;line-height:.88;letter-spacing:-4px;color:#fff;text-shadow:0 0 48px rgba(127,211,255,.45)}}
.pct em{{font-style:normal;font-size:48px;letter-spacing:0;margin-left:4px;background:linear-gradient(180deg,#7fd3ff,#3aa7e0);-webkit-background-clip:text;color:transparent}}
.pright{{padding-bottom:16px}}
.share b{{font-family:NSB;font-size:34px;color:#7fd3ff;letter-spacing:.5px}}
.share{{font-size:22px;color:#dfe6ee}}
.subh{{margin-top:6px;font-size:22px;color:#c5d0db}}
.subh b{{font-family:NSB;color:#ff6b78;font-weight:normal}}

.sec{{display:flex;align-items:center;gap:12px;margin:18px 0 10px;font-family:NSB;font-size:24px;color:#e9f3ff;letter-spacing:2px;white-space:nowrap}}
.sec i{{font-style:normal;font-family:NSM;font-size:16px;color:#7d8794;letter-spacing:0;white-space:nowrap}}
.sec:after{{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(127,211,255,.5),transparent)}}

.ranks{{display:flex;flex-direction:column;gap:8px}}
.row{{height:104px;background:linear-gradient(160deg,rgba(18,24,35,.92),rgba(12,16,23,.92));border:1px solid rgba(159,179,200,.10);border-radius:14px;padding:11px 20px 11px 16px;display:flex;flex-direction:column;justify-content:center;position:relative;overflow:hidden}}
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
.rkbox{{width:62px;flex:none;display:flex;align-items:center;justify-content:flex-start;padding-left:8px}}
.rk{{font-family:NSB;font-size:28px;color:#7fd3ff;letter-spacing:1px;line-height:1}}
.row.g1 .rk{{color:#f3de9a}}
.row.g2 .rk{{color:#d5dee6}}
.row.g3 .rk{{color:#e0b07a}}
.row.me .rk{{color:#ff6b78;font-size:30px}}
.medal{{font-family:NSB;font-size:16px;letter-spacing:2px;padding:2px 8px;border-radius:5px;line-height:1.25;flex:none}}
.medal.gold{{color:#1a1406;background:linear-gradient(180deg,#f8e7b0,#d4a017);box-shadow:0 0 12px rgba(232,195,106,.5)}}
.medal.silver{{color:#16181c;background:linear-gradient(180deg,#f4f7fa,#9aa7b4);box-shadow:0 0 10px rgba(200,214,226,.4)}}
.medal.bronze{{color:#1a120a;background:linear-gradient(180deg,#f0c99a,#b06a32);box-shadow:0 0 10px rgba(196,137,90,.45)}}
.av{{width:44px;height:44px;border-radius:50%;flex:none;margin-right:12px;background:url({PHOTO}) 50% 18%/cover no-repeat;border:2px solid rgba(255,45,63,.7);box-shadow:0 0 14px rgba(255,45,63,.35)}}
.nm{{flex:1;min-width:0}}
.n{{font-family:NSB;font-size:30px;color:#fff;line-height:1.15;display:flex;align-items:center;gap:10px}}
.row.me .n{{font-size:32px}}
.tag{{font-family:NSB;font-size:15px;color:#fff;background:linear-gradient(180deg,#ff3b4e,#d3122b);padding:2px 8px;border-radius:5px;letter-spacing:1px;box-shadow:0 0 10px rgba(255,45,63,.4)}}
.en{{font-size:15px;color:#8b97a6;margin-top:2px}}
.nums{{text-align:right;flex:none}}
.vp{{font-family:NSB;font-size:46px;line-height:1;color:#fff;letter-spacing:-1px}}
.row.me .vp{{font-size:56px}}
.vp i{{font-style:normal;font-family:NSM;font-size:18px;color:#8b97a6;margin-right:3px;letter-spacing:0}}
.vp span{{font-size:20px;margin-left:1px;color:#7fd3ff}}
.row.g1 .vp span{{color:#f3de9a}}
.row.g2 .vp span{{color:#c5d0db}}
.row.g3 .vp span{{color:#e0b07a}}
.row.me .vp span{{color:#ff6b78}}
.sh{{font-size:14px;color:#8b97a6;margin-top:3px;letter-spacing:.2px}}
.barwrap{{height:6px;background:rgba(22,28,38,.95);border-radius:4px;overflow:hidden;margin-top:8px;margin-left:8px}}
.row.me .barwrap{{height:8px;margin-top:10px}}
.bar{{height:100%;border-radius:4px;background:linear-gradient(90deg,#9ee7ff,#7fd3ff 50%,#3aa7e0);box-shadow:0 0 10px rgba(127,211,255,.4)}}
.row.g1 .bar{{background:linear-gradient(90deg,#f8e7b0,#e8c36a 50%,#c9a227);box-shadow:0 0 12px rgba(232,195,106,.5)}}
.row.g2 .bar{{background:linear-gradient(90deg,#f4f7fa,#b9c5d0 50%,#8e9aaa);box-shadow:0 0 10px rgba(200,214,226,.35)}}
.row.g3 .bar{{background:linear-gradient(90deg,#f0c99a,#d08a48 50%,#a86b38);box-shadow:0 0 10px rgba(196,137,90,.4)}}
.row.me .bar{{background:linear-gradient(90deg,#ff8a95,#ff2d3f 50%,#c80f28);box-shadow:0 0 14px rgba(255,45,63,.55)}}

.foot{{position:absolute;left:46px;right:46px;bottom:22px;font-size:15.5px;line-height:1.5;color:#6c7684}}
</style></head><body>
<div class=bg></div><div class=grid></div>
<div class=wrap>
  <div class=top><span class=brk>持股</span><span>一图看懂｜英伟达最新持股排名</span><span class=dt>2026.11.13</span></div>
  <div class=brand>英伟达</div>
  <h1>股份<em>排名</em></h1>
  <h2>黄仁勋辞了职务，仍是<span>最大个人股东</span></h2>

  <div class=hero>
    <div class=hp><div class=htag>已辞职（官方）</div></div>
    <div class=ht>
      <div class=eyebrow>黄仁勋 · 受益所有权 · 在这份排名里排第 5</div>
      <div class=pctrow>
        <div class=pct>3.58<em>%</em></div>
        <div class=pright>
          <div class=share><b>870,604,104</b> 股</div>
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
        <div class=nm><div class=n>贝莱德<span class="medal gold">冠军</span></div><div class=en>BlackRock, Inc. · 13F</div></div>
        <div class=nums><div class=vp><i>约</i>8.0<span>%</span></div><div class=sh>截至 2026-06-30</div></div>
      </div>
      <div class=barwrap><div class=bar style="width:100%"></div></div>
    </div>
    <div class="row g2">
      <div class=head>
        <div class=rkbox><div class=rk>02</div></div>
        <div class=nm><div class=n>先锋<span class="medal silver">亚军</span></div><div class=en>Vanguard Capital Management · 13F</div></div>
        <div class=nums><div class=vp><i>约</i>6.4<span>%</span></div><div class=sh>截至 2026-06-30</div></div>
      </div>
      <div class=barwrap><div class=bar style="width:80%"></div></div>
    </div>
    <div class="row g3">
      <div class=head>
        <div class=rkbox><div class=rk>03</div></div>
        <div class=nm><div class=n>富达<span class="medal bronze">季军</span></div><div class=en>FMR LLC · 13F</div></div>
        <div class=nums><div class=vp><i>约</i>4.2<span>%</span></div><div class=sh>截至 2026-06-30</div></div>
      </div>
      <div class=barwrap><div class=bar style="width:52.5%"></div></div>
    </div>
    <div class="row g4">
      <div class=head>
        <div class=rkbox><div class=rk>04</div></div>
        <div class=nm><div class=n>州街</div><div class=en>State Street Corporation · 13F</div></div>
        <div class=nums><div class=vp><i>约</i>4.2<span>%</span></div><div class=sh>截至 2026-06-30</div></div>
      </div>
      <div class=barwrap><div class=bar style="width:52%"></div></div>
    </div>
    <div class="row me">
      <div class=head>
        <div class=rkbox><div class=rk>05</div></div>
        <div class=av></div>
        <div class=nm><div class=n>黄仁勋<span class=tag>最大个人股东</span></div><div class=en>受益所有权 · 870,604,104 股 · 代理声明</div></div>
        <div class=nums><div class=vp>3.58<span>%</span></div><div class=sh>截至 2026-03-23</div></div>
      </div>
      <div class=barwrap><div class=bar style="width:44.8%"></div></div>
    </div>
  </div>

  <div class=foot>来源：机构为 SEC 13F，截至 2026-06-30，比例为约数｜黄仁勋为英伟达 2026 年代理声明，截至 2026-03-23。制图 2026/11/13。<br>机构代客户持有，与创始人股份不是一类。本文整理公开文件，不构成投资建议。投资有风险，入市需谨慎。照片仅作身份识别。</div>
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
    # only print if not just dbus
    lines = [x for x in err.splitlines() if 'dbus' not in x.lower() and 'ERROR' in x]
    print('\n'.join(lines[-8:]))
