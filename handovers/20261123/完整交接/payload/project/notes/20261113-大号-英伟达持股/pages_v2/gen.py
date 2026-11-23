# -*- coding: utf-8 -*-
import subprocess, shutil
from pathlib import Path

COVER_DIR = Path('/workspace/xhs/notes/20261113-大号-英伟达持股/cover_v2')
PAGE_DIR = Path('/workspace/xhs/notes/20261113-大号-英伟达持股/pages_v2')
PHOTO = 'file:///workspace/xhs/notes/20261112-大号-科技大佬恋情翻车/photos/huang.jpg'
F = 'file:///home/box/.fonts/'
MG = 'file://' + str(COVER_DIR/'medal_gold.svg')
MS = 'file://' + str(COVER_DIR/'medal_silver.svg')
MB = 'file://' + str(COVER_DIR/'medal_bronze.svg')

SHARED = f'''
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
.wrap{{position:absolute;inset:0;padding:28px 44px 0;display:flex;flex-direction:column}}
.top{{display:flex;align-items:center;gap:14px;font-size:22px;color:#9fb3c8;letter-spacing:1px;flex:none}}
.brk{{font-family:NSB;background:#ff2d3f;color:#fff;padding:3px 14px;border-radius:6px;font-size:22px;letter-spacing:3px;box-shadow:0 0 24px rgba(255,45,63,.6)}}
.top .dt{{margin-left:auto;font-family:NSB;color:#7fd3ff;letter-spacing:2px}}
h1{{font-family:NSB;font-size:108px;line-height:.98;margin-top:14px;letter-spacing:1px;color:#fff;text-shadow:0 0 40px rgba(120,200,255,.35),0 6px 0 rgba(0,0,0,.6);flex:none;white-space:nowrap}}
h1 em{{font-style:normal;background:linear-gradient(180deg,#ff6b6b 0%,#ff1f3a 70%,#c80f28 100%);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 0 26px rgba(255,40,60,.55))}}
h2{{font-family:NSM;font-size:28px;margin:12px 0 18px;color:#9fb3c8;letter-spacing:.4px;flex:none;white-space:nowrap}}
.foot{{flex:none;padding:12px 0 22px;font-size:16px;line-height:1.5;color:#6c7684}}
'''

# ---------- COVER (content unchanged, fill bottom) ----------
# Read current cover body content, rebuild with flex layout
# Easier: patch current html styles

cover_html = (COVER_DIR/'00_封面.html').read_text()
# backup already have v4; also snapshot current as v5 before layout tweak
shutil.copy(COVER_DIR/'00_封面.png', COVER_DIR/'00_封面_v5.png')

replacements = {
'.wrap{position:absolute;inset:0;padding:32px 44px 0}':
'.wrap{position:absolute;inset:0;padding:28px 44px 0;display:flex;flex-direction:column}',

'.hero{margin-top:18px;height:228px;display:flex;':
'.hero{margin-top:16px;height:236px;display:flex;flex:none;',

'.sec{display:flex;align-items:center;gap:12px;margin:16px 0 10px;font-family:NSB;font-size:24px;color:#e9f3ff;letter-spacing:2px;white-space:nowrap}':
'.sec{display:flex;align-items:center;gap:12px;margin:16px 0 12px;font-family:NSB;font-size:24px;color:#e9f3ff;letter-spacing:2px;white-space:nowrap;flex:none}',

'.ranks{display:flex;flex-direction:column;gap:8px}':
'.ranks{flex:1;display:flex;flex-direction:column;gap:11px;min-height:0;margin:0}',

'.row{height:110px;background:linear-gradient(160deg,rgba(18,24,35,.92),rgba(12,16,23,.92));border:1px solid rgba(159,179,200,.10);border-radius:14px;padding:10px 18px 10px 12px;display:flex;flex-direction:column;justify-content:center;position:relative;overflow:hidden}':
'.row{flex:1;height:auto;background:linear-gradient(160deg,rgba(18,24,35,.92),rgba(12,16,23,.92));border:1px solid rgba(159,179,200,.10);border-radius:16px;padding:14px 20px 14px 12px;display:flex;flex-direction:column;justify-content:center;position:relative;overflow:hidden}',

'.row.me{height:122px;border:1px solid rgba(255,45,63,.58);background:linear-gradient(100deg,rgba(255,45,63,.12),rgba(12,16,23,.96) 48%);box-shadow:0 0 28px rgba(255,45,63,.18),inset 0 0 40px rgba(255,45,63,.04)}':
'.row.me{flex:1.16;height:auto;border:1px solid rgba(255,45,63,.58);background:linear-gradient(100deg,rgba(255,45,63,.12),rgba(12,16,23,.96) 48%);box-shadow:0 0 28px rgba(255,45,63,.18),inset 0 0 40px rgba(255,45,63,.04)}',

'.n{font-family:NSB;font-size:34px;color:#fff;line-height:1.15;display:flex;align-items:center;gap:10px;white-space:nowrap}':
'.n{font-family:NSB;font-size:38px;color:#fff;line-height:1.15;display:flex;align-items:center;gap:10px;white-space:nowrap}',

'.row.me .n{font-size:36px}':
'.row.me .n{font-size:40px}',

'.vp{font-family:NSB;font-size:50px;line-height:1;color:#fff;letter-spacing:-1px}':
'.vp{font-family:NSB;font-size:56px;line-height:1;color:#fff;letter-spacing:-1px}',

'.row.me .vp{font-size:56px}':
'.row.me .vp{font-size:62px}',

'.en{font-size:17px;color:#8b97a6;margin-top:2px;white-space:nowrap}':
'.en{font-size:18px;color:#8b97a6;margin-top:3px;white-space:nowrap}',

'.sh{font-size:18px;color:#c5d0db;margin-top:3px;letter-spacing:.2px;white-space:nowrap}':
'.sh{font-size:20px;color:#c5d0db;margin-top:4px;letter-spacing:.2px;white-space:nowrap}',

'.rk{font-family:NSB;font-size:30px;color:#7fd3ff;letter-spacing:1px;line-height:1}':
'.rk{font-family:NSB;font-size:34px;color:#7fd3ff;letter-spacing:1px;line-height:1}',

'.ico{width:52px;height:60px;flex:none;margin-right:10px;background-size:contain;background-repeat:no-repeat;background-position:center;filter:drop-shadow(0 2px 6px rgba(0,0,0,.45))}':
'.ico{width:58px;height:68px;flex:none;margin-right:12px;background-size:contain;background-repeat:no-repeat;background-position:center;filter:drop-shadow(0 2px 6px rgba(0,0,0,.45))}',

'.av{width:48px;height:48px;border-radius:50%;flex:none;margin-right:12px;':
'.av{width:56px;height:56px;border-radius:50%;flex:none;margin-right:14px;',

'.barwrap{height:6px;background:rgba(22,28,38,.95);border-radius:4px;overflow:hidden;margin-top:8px;margin-left:8px}':
'.barwrap{height:8px;background:rgba(22,28,38,.95);border-radius:4px;overflow:hidden;margin-top:12px;margin-left:8px}',

'.row.me .barwrap{height:8px;margin-top:9px}':
'.row.me .barwrap{height:10px;margin-top:12px}',

'.foot{position:absolute;left:44px;right:44px;bottom:18px;font-size:16px;line-height:1.5;color:#6c7684}':
'.foot{position:relative;left:auto;right:auto;bottom:auto;flex:none;padding:12px 0 22px;font-size:16px;line-height:1.55;color:#6c7684}',

# 04 name alignment after larger medal: 58+12=70
'margin-left:54px':
'margin-left:70px',
}

for a,b in replacements.items():
    if a not in cover_html:
        print('MISSING REPLACE:', a[:80])
    else:
        cover_html = cover_html.replace(a,b)
        print('ok:', a[:40])

(COVER_DIR/'00_封面.html').write_text(cover_html)

# ---------- PAGE 1 ----------
p1 = f'''<!doctype html><html><head><meta charset=utf-8><style>{SHARED}
.mid{{flex:1;display:flex;flex-direction:column;min-height:0;gap:14px}}
.note{{flex:none;display:flex;align-items:flex-start;gap:12px;background:linear-gradient(90deg,rgba(232,195,106,.12),rgba(18,24,35,.5));border:1px solid rgba(232,195,106,.38);border-radius:12px;padding:14px 18px;font-size:24px;line-height:1.45;color:#f3e6c0}}
.note b{{font-family:NSB;color:#f3de9a}}
.note .k{{font-family:NSB;flex:none;background:#e8c36a;color:#1a1406;padding:3px 10px;border-radius:6px;font-size:20px;letter-spacing:1px;margin-top:2px}}
.ranks{{flex:1.15;display:flex;flex-direction:column;gap:12px;min-height:0}}
.row{{flex:1;background:linear-gradient(160deg,rgba(18,24,35,.92),rgba(12,16,23,.92));border:1px solid rgba(159,179,200,.10);border-radius:16px;padding:14px 22px 14px 16px;display:flex;flex-direction:column;justify-content:center;position:relative;overflow:hidden}}
.row:before{{content:'';position:absolute;left:0;top:16px;bottom:16px;width:4px;border-radius:0 2px 2px 0}}
.row.g1{{border-color:rgba(232,195,106,.38);background:linear-gradient(100deg,rgba(232,195,106,.10),rgba(12,16,23,.95) 42%)}}
.row.g1:before{{background:linear-gradient(180deg,#f3de9a,#c9a227);box-shadow:0 0 10px rgba(232,195,106,.55)}}
.row.g2{{border-color:rgba(196,210,224,.28);background:linear-gradient(100deg,rgba(196,210,224,.08),rgba(12,16,23,.95) 42%)}}
.row.g2:before{{background:linear-gradient(180deg,#e8eef4,#8e9aaa)}}
.row.me{{border:1px solid rgba(255,45,63,.58);background:linear-gradient(100deg,rgba(255,45,63,.12),rgba(12,16,23,.96) 48%);box-shadow:0 0 28px rgba(255,45,63,.18)}}
.row.me:before{{background:linear-gradient(180deg,#ff6b78,#c80f28);box-shadow:0 0 12px rgba(255,45,63,.6)}}
.head{{display:flex;align-items:center}}
.rk{{width:70px;flex:none;font-family:NSB;font-size:40px;color:#7fd3ff;letter-spacing:1px;padding-left:10px}}
.row.g1 .rk{{color:#f3de9a}}
.row.g2 .rk{{color:#d5dee6}}
.row.me .rk{{color:#ff6b78}}
.av{{width:64px;height:64px;border-radius:50%;flex:none;margin-right:16px;background:url({PHOTO}) 50% 18%/cover no-repeat;border:2px solid rgba(255,45,63,.7);box-shadow:0 0 14px rgba(255,45,63,.35)}}
.nm{{flex:1;min-width:0}}
.n{{font-family:NSB;font-size:42px;color:#fff;line-height:1.15;display:flex;align-items:center;gap:12px;white-space:nowrap}}
.tag{{font-family:NSB;font-size:18px;color:#fff;background:linear-gradient(180deg,#ff3b4e,#d3122b);padding:3px 10px;border-radius:6px;letter-spacing:1px}}
.en{{font-size:20px;color:#8b97a6;margin-top:4px;white-space:nowrap}}
.nums{{text-align:right;flex:none}}
.vp{{font-family:NSB;font-size:68px;line-height:1;color:#fff;letter-spacing:-1px}}
.vp span{{font-size:28px;margin-left:2px;color:#7fd3ff}}
.row.g1 .vp span{{color:#f3de9a}}
.row.g2 .vp span{{color:#c5d0db}}
.row.me .vp span{{color:#ff6b78}}
.sh{{font-size:22px;color:#c5d0db;margin-top:4px;white-space:nowrap}}
.sh b{{font-family:NSB;color:#fff;font-weight:normal}}
.row.g1 .sh b{{color:#f3de9a}}
.row.me .sh b{{color:#ff8a95}}
.barwrap{{height:10px;background:rgba(22,28,38,.95);border-radius:5px;overflow:hidden;margin-top:12px;margin-left:10px}}
.bar{{height:100%;border-radius:5px;box-shadow:0 0 10px rgba(127,211,255,.35)}}
.row.g1 .bar{{background:linear-gradient(90deg,#f8e7b0,#e8c36a 50%,#c9a227);box-shadow:0 0 12px rgba(232,195,106,.5)}}
.row.g2 .bar{{background:linear-gradient(90deg,#f4f7fa,#b9c5d0 50%,#8e9aaa)}}
.row.me .bar{{background:linear-gradient(90deg,#ff8a95,#ff2d3f 50%,#c80f28);box-shadow:0 0 14px rgba(255,45,63,.55)}}
.sec{{font-family:NSB;font-size:28px;color:#e9f3ff;letter-spacing:2px;flex:none;display:flex;align-items:center;gap:12px;margin-top:2px}}
.sec:after{{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(127,211,255,.5),transparent)}}
.grid4{{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:12px;min-height:0}}
.card{{background:linear-gradient(160deg,rgba(18,24,35,.92),rgba(12,16,23,.92));border:1px solid rgba(159,179,200,.12);border-radius:16px;padding:20px 22px;display:flex;flex-direction:column;justify-content:center;position:relative;overflow:hidden}}
.card:before{{content:'';position:absolute;left:0;top:16px;bottom:16px;width:3px;background:rgba(127,211,255,.45);border-radius:0 2px 2px 0}}
.card .k{{font-size:20px;color:#8b97a6;letter-spacing:1px;margin-bottom:6px}}
.card .t{{font-family:NSB;font-size:32px;color:#fff;line-height:1.25}}
.card .t em{{font-style:normal;color:#7fd3ff}}
.card.red .t em{{color:#ff6b78}}
.card .d{{margin-top:8px;font-size:22px;line-height:1.45;color:#c5d0db}}
.card.gold{{border-color:rgba(232,195,106,.32)}}
.card.gold:before{{background:linear-gradient(180deg,#f3de9a,#c9a227)}}
.card.gold .t{{color:#f3de9a}}
.card.red{{border-color:rgba(255,45,63,.4)}}
.card.red:before{{background:linear-gradient(180deg,#ff6b78,#c80f28)}}
</style></head><body>
<div class=bg></div><div class=grid></div>
<div class=wrap>
  <div class=top><span class=brk>口径</span><span>官方同一时点｜代理声明受益所有权</span><span class=dt>2026.03.23</span></div>
  <h1>同一时点，<em>谁持股更多</em></h1>
  <h2>全部来自 2026 年 3 月 23 日同一张表 · 流通股本 24,312,141,810 股</h2>
  <div class=mid>
    <div class=ranks>
      <div class="row g1">
        <div class=head>
          <div class=rk>01</div>
          <div class=nm><div class=n>贝莱德公司</div><div class=en>BlackRock, Inc. · 1,805,935,550 股</div></div>
          <div class=nums><div class=vp>7.43<span>%</span></div><div class=sh>约合 <b>3,001 亿美元</b></div></div>
        </div>
        <div class=barwrap><div class=bar style="width:100%"></div></div>
      </div>
      <div class="row g2">
        <div class=head>
          <div class=rk>02</div>
          <div class=nm><div class=n>先锋资本管理</div><div class=en>Vanguard Capital Management · 1,777,408,252 股</div></div>
          <div class=nums><div class=vp>7.31<span>%</span></div><div class=sh>约合 <b>2,954 亿美元</b></div></div>
        </div>
        <div class=barwrap><div class=bar style="width:98.4%"></div></div>
      </div>
      <div class="row me">
        <div class=head>
          <div class=rk>03</div>
          <div class=av></div>
          <div class=nm><div class=n>黄仁勋<span class=tag>最大个人股东</span></div><div class=en>受益所有权 · 870,604,104 股</div></div>
          <div class=nums><div class=vp>3.58<span>%</span></div><div class=sh>约合 <b>1,447 亿美元</b></div></div>
        </div>
        <div class=barwrap><div class=bar style="width:48.2%"></div></div>
      </div>
    </div>
    <div class=note><span class=k>看清口径</span><div>封面上的机构数字，用的是更新的 <b>13F（截至 6 月 30 日，约数）</b>。要和黄仁勋 3.58% 在同一天比，以本页这张代理声明为准。市值均按 11 月 12 日收盘价 166.19 美元测算。</div></div>
    <div class=sec>3.58% 里，有四点要看清</div>
    <div class=grid4>
      <div class=card>
        <div class=k>怎么持有</div>
        <div class=t>大部分在信托和公司</div>
        <div class=d>活体信托、2012 信托、剩余权益信托，以及以信托为唯一成员的公司，持有其中大部分。不在个人名下。</div>
      </div>
      <div class="card gold">
        <div class=k>基金会计入，但没有经济利益</div>
        <div class=t>58,683,830 股</div>
        <div class=d>The Jen-Hsun &amp; Lori Huang Foundation 计入 3.58%，代理声明写明他对这部分没有经济利益。</div>
      </div>
      <div class=card>
        <div class=k>投票权</div>
        <div class=t>一股一票，不是超级投票权</div>
        <div class=d>英伟达是单一普通股。3.58% 是持股比例，不是对公司的控制权。</div>
      </div>
      <div class="card red">
        <div class=k>临时首席执行官 · 董事及高管</div>
        <div class=t>克雷斯持股不足 1%</div>
        <div class=d>科莱特·克雷斯持有 4,443,523 股。董事及高管 14 人合计 3.94%，其中大部分是黄仁勋。</div>
      </div>
    </div>
  </div>
  <div class=foot>来源：英伟达 2026 年代理声明 DEF 14A，受益所有权截至 2026-03-23；提交日 2026-05-12。制图 2026/11/13。<br>市值按 2026 年 11 月 12 日收盘价 166.19 美元测算。机构代客户持有，与创始人股份不是一类。不构成投资建议。照片仅作身份识别。</div>
</div>
</body></html>'''
(PAGE_DIR/'01_同一时点持股.html').write_text(p1)

# ---------- PAGE 2 ----------
p2 = f'''<!doctype html><html><head><meta charset=utf-8><style>{SHARED}
h1{{font-size:108px}}
.mid{{flex:1;display:flex;flex-direction:column;min-height:0;gap:14px}}
.banner{{flex:none;border-radius:18px;padding:26px 32px;background:linear-gradient(100deg,rgba(255,45,63,.16),rgba(12,16,23,.95) 55%);border:1px solid rgba(255,45,63,.55);box-shadow:0 0 36px rgba(255,45,63,.18),inset 0 0 50px rgba(255,45,63,.04);display:flex;align-items:center;gap:28px}}
.banner .lab{{font-family:NSB;font-size:20px;color:#fff;background:linear-gradient(180deg,#ff3b4e,#d3122b);padding:5px 12px;border-radius:6px;letter-spacing:2px;flex:none}}
.banner .tx{{font-family:NSB;font-size:46px;line-height:1.2;color:#fff;letter-spacing:.5px}}
.banner .tx em{{font-style:normal;color:#ff6b78}}
.banner .sub{{margin-top:6px;font-size:22px;color:#c5d0db;font-family:NSM}}
.tiles{{flex:none;display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}}
.tile{{background:linear-gradient(160deg,rgba(18,24,35,.92),rgba(12,16,23,.92));border:1px solid rgba(159,179,200,.12);border-radius:16px;padding:20px 20px 22px;position:relative;overflow:hidden;display:flex;flex-direction:column;justify-content:center;min-height:148px}}
.tile:before{{content:'';position:absolute;left:0;top:16px;bottom:16px;width:3px;background:rgba(127,211,255,.5);border-radius:0 2px 2px 0}}
.tile .k{{font-size:20px;color:#8b97a6;letter-spacing:1px;margin-bottom:8px}}
.tile .t{{font-family:NSB;font-size:32px;color:#fff;line-height:1.3}}
.tile .t em{{font-style:normal;color:#7fd3ff}}
.tile.red{{border-color:rgba(255,45,63,.4)}}
.tile.red:before{{background:linear-gradient(180deg,#ff6b78,#c80f28)}}
.tile.red .t em{{color:#ff6b78}}
.two{{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:14px;min-height:0}}
.panel{{background:linear-gradient(160deg,rgba(18,24,35,.94),rgba(12,16,23,.94));border:1px solid rgba(159,179,200,.12);border-radius:18px;padding:26px 26px 22px;display:flex;flex-direction:column;position:relative;overflow:hidden}}
.panel.red{{border-color:rgba(255,45,63,.45);background:linear-gradient(160deg,rgba(255,45,63,.10),rgba(12,16,23,.96) 50%);box-shadow:0 0 28px rgba(255,45,63,.12)}}
.panel .k{{font-family:NSB;font-size:24px;color:#9fb3c8;letter-spacing:2px}}
.panel .big{{font-family:NSB;font-size:72px;line-height:.95;color:#fff;margin:14px 0 6px;letter-spacing:-1px}}
.panel .big em{{font-style:normal;font-size:32px;color:#7fd3ff;letter-spacing:0;margin-left:4px}}
.panel.red .big em{{color:#ff6b78}}
.panel .unit{{font-size:24px;color:#9fb3c8;margin-bottom:16px}}
.panel .unit b{{font-family:NSB;color:#fff;font-weight:normal}}
.li{{display:flex;gap:12px;align-items:flex-start;margin-top:12px;font-size:24px;line-height:1.45;color:#dfe6ee}}
.li .dot{{flex:none;width:10px;height:10px;border-radius:50%;background:#7fd3ff;margin-top:12px;box-shadow:0 0 8px rgba(127,211,255,.6)}}
.panel.red .li .dot{{background:#ff6b78;box-shadow:0 0 8px rgba(255,45,63,.6)}}
.li b{{font-family:NSB;color:#fff;font-weight:normal}}
.li em{{font-style:normal;color:#7fd3ff;font-family:NSB}}
.panel.red .li em{{color:#ff8a95}}
.warn{{margin-top:auto;padding-top:16px;font-family:NSB;font-size:24px;line-height:1.4;color:#f3de9a;border-top:1px solid rgba(232,195,106,.28)}}
.photo{{position:absolute;right:-8px;bottom:-8px;width:168px;height:200px;border-radius:16px 0 18px 0;background:url({PHOTO}) 50% 18%/cover no-repeat;opacity:.95;mask-image:linear-gradient(90deg,transparent 0%,#000 28%);filter:contrast(1.05) saturate(.9)}}
</style></head><body>
<div class=bg></div><div class=grid></div>
<div class=wrap>
  <div class=top><span class=brk>解读</span><span>辞职与股份｜对照官方公告和最新内部人报告</span><span class=dt>2026.11.13</span></div>
  <h1>辞了职务，<em>股份还在吗</em></h1>
  <h2>职务和股权是两件事 · 官方 8-K 没有要求卖出或交出股份</h2>
  <div class=mid>
    <div class=banner>
      <div>
        <span class=lab>官方 8-K</span>
      </div>
      <div>
        <div class=tx>全文<em>没有要求</em>他卖出或交出股份</div>
        <div class=sub>事项日 2026-11-11，签署并公告 2026-11-12 · 新闻稿同日发布</div>
      </div>
    </div>
    <div class=tiles>
      <div class="tile red">
        <div class=k>董事会决定</div>
        <div class=t>接受辞职<br><em>即刻生效</em></div>
      </div>
      <div class=tile>
        <div class=k>辞去职务</div>
        <div class=t>总裁、CEO<br>和<em>董事</em></div>
      </div>
      <div class=tile>
        <div class=k>谁来接</div>
        <div class=t>临时 CEO <em>克雷斯</em><br>董事长 哈维·琼斯</div>
      </div>
    </div>
    <div class=two>
      <div class=panel>
        <div class=k>股份怎么持有</div>
        <div class=big>3.58<em>%</em></div>
        <div class=unit>受益所有权 · <b>870,604,104</b> 股</div>
        <div class=li><span class=dot></span><div>大部分在他与妻子共同任受托人的<b>信托和公司</b>里，不在个人名下。</div></div>
        <div class=li><span class=dot></span><div>基金会 <em>58,683,830</em> 股计入这个比例，但代理声明写明：他对这部分<b>没有经济利益</b>。</div></div>
        <div class=li><span class=dot></span><div>英伟达是单一普通股、<b>一股一票</b>。3.58% 是持股比例，不是超级投票权，也不是控制权。</div></div>
      </div>
      <div class="panel red">
        <div class=k>9 月之后有没有卖</div>
        <div class=big>811,521,160</div>
        <div class=unit>9 月 18 日 Form 4 各栏合计 · <b>作者计算，不含基金会</b></div>
        <div class=li><span class=dot></span><div>当日变动是<b>税款代扣</b>和<b>慈善赠与</b>，不是公开市场出售。</div></div>
        <div class=li><span class=dot></span><div>截至 11 月 13 日检索，<em>未见辞职后新的 Form 4</em>。</div></div>
        <div class=warn>会不会卖，要看依法披露。现在不能当作已经卖了，也不能当作一定会卖。</div>
      </div>
    </div>
  </div>
  <div class=foot>来源：SEC 8-K（事项日 2026-11-11，签署 2026-11-12）｜Form 4（2026-09-18 提交，报告期 09-16）｜2026 年代理声明脚注。制图 2026/11/13。<br>官方用词为辞职。不构成投资建议。投资有风险，入市需谨慎。</div>
</div>
</body></html>'''
(PAGE_DIR/'02_辞职与股份.html').write_text(p2)

def render(html, png):
    r = subprocess.run([
        'google-chrome','--headless=new','--no-sandbox','--disable-gpu',
        '--allow-file-access-from-files','--hide-scrollbars',
        '--force-device-scale-factor=2','--window-size=1080,1440',
        '--virtual-time-budget=5000',
        f'--screenshot={png}',
        'file://'+str(html)
    ], capture_output=True)
    print(html.name, r.returncode, Path(png).stat().st_size if Path(png).exists() else 0)

render(COVER_DIR/'00_封面.html', COVER_DIR/'00_封面.png')
render(PAGE_DIR/'01_同一时点持股.html', PAGE_DIR/'01_同一时点持股.png')
render(PAGE_DIR/'02_辞职与股份.html', PAGE_DIR/'02_辞职与股份.png')
print('done')
