# -*- coding: utf-8 -*-
import os, subprocess
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
  radial-gradient(900px 520px at 85% 8%,rgba(70,160,255,.22),transparent 60%),
  radial-gradient(700px 500px at 0% 40%,rgba(255,40,60,.10),transparent 60%),
  linear-gradient(180deg,#0b0f16 0%,#07090d 55%,#050608 100%)}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(140,190,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(140,190,255,.045) 1px,transparent 1px);background-size:40px 40px;mask-image:linear-gradient(180deg,#000 0%,transparent 50%)}}
.wrap{{position:absolute;inset:0;padding:38px 46px 0}}
.top{{display:flex;align-items:center;gap:14px;font-size:22px;color:#9fb3c8;letter-spacing:1px}}
.brk{{font-family:NSB;background:#ff2d3f;color:#fff;padding:3px 14px;border-radius:6px;font-size:22px;letter-spacing:3px;box-shadow:0 0 24px rgba(255,45,63,.6)}}
.top .dt{{margin-left:auto;font-family:NSB;color:#7fd3ff;letter-spacing:2px}}
h1{{font-family:NSB;font-size:168px;line-height:1;margin-top:16px;letter-spacing:2px;white-space:nowrap;color:#fff;text-shadow:0 0 40px rgba(120,200,255,.35),0 6px 0 rgba(0,0,0,.6)}}
h1 em{{font-style:normal;background:linear-gradient(180deg,#ff6b6b 0%,#ff1f3a 70%,#c80f28 100%);-webkit-background-clip:text;color:transparent;text-shadow:none;filter:drop-shadow(0 0 26px rgba(255,40,60,.55))}}
h2{{font-family:NSB;font-size:52px;margin-top:10px;color:#e9f3ff;letter-spacing:1px;white-space:nowrap}}
h2 span{{color:#0b0f16;background:#7fd3ff;padding:0 8px;border-radius:6px;margin:0 2px}}

.hero{{margin-top:22px;height:292px;display:flex;border-radius:20px;overflow:hidden;background:linear-gradient(100deg,#141b26,#0e121a);border:1px solid rgba(127,211,255,.35);box-shadow:0 0 0 1px rgba(255,45,63,.15),0 20px 60px rgba(0,0,0,.6),inset 0 0 60px rgba(127,211,255,.06);position:relative}}
.hp{{width:280px;flex:none;background:url({PHOTO}) 50% 18%/cover no-repeat;position:relative;filter:contrast(1.05) saturate(.9)}}
.hp:after{{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent 55%,#141b26 100%),linear-gradient(0deg,rgba(7,9,13,.5),transparent 35%)}}
.htag{{position:absolute;left:16px;top:16px;z-index:2;font-family:NSB;font-size:22px;color:#fff;background:linear-gradient(180deg,#ff3b4e,#d3122b);padding:5px 14px;border-radius:8px;box-shadow:0 0 24px rgba(255,45,63,.5);letter-spacing:1px}}
.ht{{padding:22px 32px 0 8px;flex:1;min-width:0;display:flex;flex-direction:column}}
.eyebrow{{font-size:22px;color:#9fb3c8;letter-spacing:1px}}
.pct{{font-family:NSB;font-size:168px;line-height:.9;letter-spacing:-4px;color:#fff;text-shadow:0 0 48px rgba(127,211,255,.45);margin-top:4px}}
.pct em{{font-style:normal;font-size:56px;letter-spacing:0;margin-left:6px;background:linear-gradient(180deg,#7fd3ff,#3aa7e0);-webkit-background-clip:text;color:transparent}}
.share{{margin-top:8px;font-size:28px;color:#dfe6ee}}
.share b{{font-family:NSB;font-size:40px;color:#7fd3ff;margin-right:8px;letter-spacing:1px}}
.subh{{margin-top:8px;font-size:22px;color:#9fb3c8}}

.sec{{display:flex;align-items:center;gap:14px;margin:22px 0 14px;font-family:NSB;font-size:26px;color:#e9f3ff;letter-spacing:2px}}
.sec:after{{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(127,211,255,.6),transparent)}}
.sec i{{font-style:normal;font-family:NSM;font-size:18px;color:#7d8794;letter-spacing:0}}

.ranks{{display:flex;flex-direction:column;gap:12px}}
.row{{height:154px;background:linear-gradient(160deg,#121823,#0c1017);border:1px solid rgba(159,179,200,.16);border-radius:18px;padding:16px 24px 14px;position:relative;display:flex;flex-direction:column;justify-content:space-between}}
.row.me{{border:1px solid rgba(255,45,63,.55);box-shadow:0 0 28px rgba(255,45,63,.18),inset 0 0 40px rgba(255,45,63,.05)}}
.head{{display:flex;align-items:center}}
.rk{{font-family:NSB;font-size:36px;color:#7fd3ff;width:78px;letter-spacing:1px}}
.row.me .rk{{color:#ff6b78}}
.av{{width:48px;height:48px;border-radius:50%;flex:none;margin-right:14px;display:flex;align-items:center;justify-content:center;font-family:NSB;font-size:22px;color:#0b0f16;background:#7fd3ff;box-shadow:0 0 14px rgba(127,211,255,.4)}}
.av.photo{{background:url({PHOTO}) 50% 18%/cover no-repeat;border:2px solid rgba(255,45,63,.7);box-shadow:0 0 14px rgba(255,45,63,.35);color:transparent}}
.nm{{flex:1;min-width:0}}
.n{{font-family:NSB;font-size:36px;color:#fff;line-height:1.1}}
.en{{font-size:18px;color:#9fb3c8;margin-top:3px}}
.nums{{text-align:right}}
.vp{{font-family:NSB;font-size:64px;line-height:1;color:#fff;letter-spacing:-1px}}
.vp span{{font-size:28px;margin-left:2px;color:#7fd3ff}}
.row.me .vp span{{color:#ff6b78}}
.sh{{font-size:18px;color:#9fb3c8;margin-top:4px;letter-spacing:.3px}}
.barwrap{{height:16px;background:#161c26;border-radius:8px;overflow:hidden;margin-top:10px;box-shadow:inset 0 0 8px rgba(0,0,0,.5)}}
.bar{{height:16px;border-radius:8px;background:linear-gradient(90deg,#9ee7ff,#7fd3ff 40%,#3aa7e0);box-shadow:0 0 16px rgba(127,211,255,.55)}}
.row.me .bar{{background:linear-gradient(90deg,#ff8a95,#ff2d3f 50%,#c80f28);box-shadow:0 0 16px rgba(255,45,63,.55)}}

.chips{{display:flex;gap:12px;margin-top:16px}}
.chip{{flex:1;background:linear-gradient(160deg,#121823,#0c1017);border:1px solid rgba(159,179,200,.16);border-radius:14px;padding:14px 16px 16px}}
.chip b{{display:block;font-family:NSB;font-size:22px;color:#7fd3ff;margin-bottom:6px}}
.chip p{{font-size:20px;color:#c5d0db;line-height:1.45}}

.foot{{position:absolute;left:46px;right:46px;bottom:22px;font-size:16.5px;line-height:1.5;color:#6c7684}}
</style></head><body>
<div class=bg></div><div class=grid></div>
<div class=wrap>
  <div class=top><span class=brk>持股</span><span>一图看懂｜英伟达最新持股排名</span><span class=dt>2026.11.13</span></div>
  <h1>黄仁勋<em>还持股</em></h1>
  <h2>辞了职务，股权<span>怎么排</span></h2>

  <div class=hero>
    <div class=hp><div class=htag>已辞职（官方）</div></div>
    <div class=ht>
      <div class=eyebrow>黄仁勋 · 受益所有权 · 最大个人股东</div>
      <div class=pct>3.58<em>%</em></div>
      <div class=share><b>870,604,104</b>股</div>
      <div class=subh>2026年3月23日代理声明 · 同一张表</div>
    </div>
  </div>

  <div class=sec>同一时点｜持股排名<i>机构是代客户持有，与创始人股份不是一类</i></div>
  <div class=ranks>
    <div class=row>
      <div class=head>
        <div class=rk>01</div>
        <div class=av>贝</div>
        <div class=nm><div class=n>贝莱德</div><div class=en>BlackRock, Inc.</div></div>
        <div class=nums><div class=vp>7.43<span>%</span></div><div class=sh>1,805,935,550 股</div></div>
      </div>
      <div class=barwrap><div class=bar style="width:100%"></div></div>
    </div>
    <div class=row>
      <div class=head>
        <div class=rk>02</div>
        <div class=av>先</div>
        <div class=nm><div class=n>先锋</div><div class=en>Vanguard Capital Management</div></div>
        <div class=nums><div class=vp>7.31<span>%</span></div><div class=sh>1,777,408,252 股</div></div>
      </div>
      <div class=barwrap><div class=bar style="width:98.4%"></div></div>
    </div>
    <div class="row me">
      <div class=head>
        <div class=rk>03</div>
        <div class="av photo"></div>
        <div class=nm><div class=n>黄仁勋</div><div class=en>最大个人股东 · 受益所有权</div></div>
        <div class=nums><div class=vp>3.58<span>%</span></div><div class=sh>870,604,104 股</div></div>
      </div>
      <div class=barwrap><div class=bar style="width:48.2%"></div></div>
    </div>
  </div>

  <div class=chips>
    <div class=chip><b>一股一票</b><p>3.58% 是持股比例，不是超级投票权，也不是控制权。</p></div>
    <div class=chip><b>大部分在信托里</b><p>基金会 58,683,830 股计入这个比例，但声明写明没有经济利益。</p></div>
    <div class=chip><b>辞职没写减持</b><p>11月12日公告辞去总裁、CEO和董事。8-K没有要求他卖出股份。</p></div>
  </div>

  <div class=foot>来源：英伟达 2026 年代理声明，持股截至 2026-03-23｜SEC 8-K（事项日 2026-11-11）。制图 2026/11/13。<br>风险提示：本文整理公开文件，不构成任何投资建议。投资有风险，入市需谨慎。照片仅作身份识别。</div>
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
    print(r.stderr[-500:].decode() if isinstance(r.stderr,bytes) else r.stderr[-500:])
