#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成深色电影感 4 页 HTML（封面+3内页）。渲染请用 render_heijin.sh（本地无头 Chrome，不改共享脚本）。"""
from pathlib import Path
D = Path(__file__).resolve().parent

CSS = r'''
@font-face{font-family:NSB;src:url(file:///home/box/.fonts/NotoSansSC-Black.otf)}
@font-face{font-family:NSM;src:url(file:///home/box/.fonts/NotoSansSC-Medium.otf)}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1440px;overflow:hidden;background:#07090d;font-family:NSM,'Noto Sans CJK SC',sans-serif;color:#e8edf3;position:relative}
.bg{position:absolute;inset:0;background:
  radial-gradient(900px 500px at 88% 6%,rgba(70,160,255,.22),transparent 58%),
  radial-gradient(640px 460px at 4% 42%,rgba(255,40,60,.11),transparent 60%),
  radial-gradient(500px 380px at 70% 88%,rgba(232,195,106,.06),transparent 65%),
  linear-gradient(180deg,#0b0f16 0%,#07090d 55%,#050608 100%)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(140,190,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(140,190,255,.045) 1px,transparent 1px);background-size:40px 40px;mask-image:linear-gradient(180deg,#000 0%,transparent 46%)}
.wrap{position:absolute;inset:0;padding:26px 40px 92px;display:block}
.top{display:flex;align-items:center;gap:14px;height:34px;font-size:22px;color:#9fb3c8;letter-spacing:1px}
.brk{font-family:NSB;background:#ff2d3f;color:#fff;padding:3px 14px;border-radius:6px;font-size:22px;letter-spacing:3px;box-shadow:0 0 24px rgba(255,45,63,.6)}
.top .dt{margin-left:auto;font-family:NSB;color:#7fd3ff;letter-spacing:2px}
h1{font-family:NSB;color:#fff;text-shadow:0 0 40px rgba(120,200,255,.35),0 4px 0 rgba(0,0,0,.55);white-space:nowrap}
h1 em{font-style:normal;color:#ff2d3f;text-shadow:0 0 28px rgba(255,45,63,.5),0 4px 0 rgba(0,0,0,.55)}
.cover h1{font-size:108px;line-height:1.04;margin-top:14px;letter-spacing:0}
.inner h1{font-size:64px;line-height:1.08;margin-top:16px;letter-spacing:0}
.h2box{margin-top:22px}
.inner .h2box{margin-top:14px}
h2{font-family:NSM;font-size:32px;color:#bdcddd;letter-spacing:0;line-height:1.2;white-space:nowrap}
.hero{margin-top:18px;height:100px;display:flex;align-items:center;border-radius:16px;padding:0 24px;gap:18px;
  background:linear-gradient(100deg,#141b26,#0e121a);border:1px solid rgba(127,211,255,.28);
  box-shadow:0 10px 30px rgba(0,0,0,.4)}
.hero .k{font-size:22px;color:#c5d0db;white-space:nowrap}
.hero .v{font-family:NSB;font-size:40px;color:#7fd3ff;letter-spacing:0;white-space:nowrap;text-shadow:0 0 16px rgba(127,211,255,.35)}
.hero .u{font-size:20px;color:#9baabb;white-space:nowrap}
.pair{margin-top:20px;display:flex;gap:18px}
.card{flex:1;border-radius:18px;padding:26px 24px 24px;background:rgba(14,18,26,.85);
  border:1px solid rgba(159,179,200,.16);position:relative;overflow:hidden}
.card.tall{min-height:300px}
.card:before{content:'';position:absolute;left:0;top:18px;bottom:18px;width:4px;border-radius:0 2px 2px 0}
.card.a:before{background:linear-gradient(180deg,#7fd3ff,#3a8dff);box-shadow:0 0 12px rgba(127,211,255,.5)}
.card.b:before{background:linear-gradient(180deg,#f3de9a,#c9a227);box-shadow:0 0 12px rgba(243,222,154,.4)}
.badge{font-family:NSB;font-size:20px;letter-spacing:1px;color:#fff;background:rgba(127,211,255,.18);
  border:1px solid rgba(127,211,255,.4);padding:3px 12px;border-radius:6px;display:inline-block}
.card.b .badge{background:rgba(243,222,154,.14);border-color:rgba(243,222,154,.4);color:#f3de9a}
.pct{font-family:NSB;font-size:140px;line-height:.92;margin-top:14px;letter-spacing:-4px;color:#7fd3ff;
  text-shadow:0 0 28px rgba(127,211,255,.35)}
.card.b .pct{color:#f3de9a;text-shadow:0 0 28px rgba(243,222,154,.35)}
.pct i{font-style:normal;font-size:58px;margin-left:2px;letter-spacing:0}
.amt{margin-top:12px;font-size:26px;color:#dfe6ee}
.amt b{font-family:NSB;font-size:28px;color:#fff;font-weight:normal}
.sum{margin-top:20px;border-radius:14px;padding:22px 24px;display:flex;align-items:center;gap:16px;
  background:rgba(18,24,35,.9);border:1px solid rgba(243,222,154,.32)}
.sum .k{font-size:24px;color:#c5d0db;white-space:nowrap}
.sum .v{font-family:NSB;font-size:64px;color:#f3de9a;line-height:1;text-shadow:0 0 18px rgba(232,195,106,.4)}
.sum .why{margin-left:auto;font-size:20px;color:#9baabb;line-height:1.35}
.note{margin-top:18px;border-radius:12px;padding:18px 20px;background:rgba(18,24,35,.85);
  border:1px solid rgba(159,179,200,.14);font-size:24px;line-height:1.5;color:#c5d0db}
.note b{font-family:NSB;color:#7fd3ff;font-weight:normal}
.foot{position:absolute;left:40px;right:40px;bottom:12px;font-size:15px;line-height:1.4;color:#6c7684}
.sec{display:flex;align-items:center;gap:14px;margin:18px 0 10px;font-family:NSB;font-size:27px;line-height:32px;color:#e9f3ff;white-space:nowrap}
.sec span{font-size:20px;color:#8b97a6;font-family:NSM}
.sec:after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(127,211,255,.5),transparent)}
.shell{border:1px solid rgba(159,179,200,.14);border-radius:12px;overflow:hidden;background:rgba(10,14,20,.6)}
table{width:100%;border-collapse:separate;border-spacing:0;table-layout:fixed}
thead th{font-family:NSB;font-size:20px;color:#7fd3ff;letter-spacing:1px;text-align:left;padding:10px 12px;
  font-weight:normal;border-bottom:1px solid rgba(127,211,255,.28);background:rgba(12,16,24,.8)}
thead th.r,td.r{text-align:center}
tbody tr td{padding:22px 12px;border-bottom:1px solid rgba(159,179,200,.10);vertical-align:middle;background:rgba(14,18,26,.55);font-size:23px;color:#dfe6ee;line-height:1.4}
tbody tr:nth-child(odd) td{background:rgba(18,24,35,.72)}
tbody tr:last-child td{border-bottom:0}
.nm{font-family:NSB;font-size:28px;color:#fff;line-height:1.2}
.co{font-size:20px;color:#9baabb;margin-top:4px}
.up{font-family:NSB;color:#ff6b78;font-size:40px}
.dn{font-family:NSB;color:#7fd3ff;font-size:40px}
.na{font-family:NSB;color:#9baabb;font-size:28px}
.bars{margin-top:8px}
.barrow{display:flex;align-items:center;gap:14px;padding:12px 0}
.barrow .lab{width:200px;flex:none;font-size:23px;color:#dfe6ee;white-space:nowrap}
.barrow .lab b{font-family:NSB;color:#fff;font-weight:normal}
.track{flex:1;height:22px;border-radius:11px;background:rgba(255,255,255,.06);overflow:hidden}
.fill{height:100%;border-radius:11px;background:linear-gradient(90deg,#3a8dff,#7fd3ff)}
.fill.gold{background:linear-gradient(90deg,#c9a227,#f3de9a)}
.fill.dim{background:linear-gradient(90deg,#3d4a5c,#6a7a8c)}
.barrow .pv{width:300px;flex:none;text-align:right;font-size:22px;color:#c5d0db;white-space:nowrap}
.barrow .pv b{font-family:NSB;font-size:30px;color:#7fd3ff;font-weight:normal}
.warn{margin-top:14px;border-radius:14px;padding:20px 20px;background:rgba(40,18,22,.7);
  border:1px solid rgba(255,107,120,.35);font-size:24px;line-height:1.55;color:#f0d4d6}
.warn b{font-family:NSB;color:#ff6b78;font-weight:normal}
.pits{margin-top:16px;display:flex;flex-direction:column;gap:14px}
.pit{display:flex;gap:16px;align-items:flex-start;border-radius:14px;padding:22px 20px;
  background:rgba(14,18,26,.85);border:1px solid rgba(159,179,200,.14)}
.no{font-family:NSB;font-size:28px;color:#ff2d3f;width:48px;flex:none;line-height:1.2}
.pit .t{font-family:NSB;font-size:28px;color:#fff;line-height:1.3}
.pit .d{margin-top:8px;font-size:23px;color:#c5d0db;line-height:1.45}
'''

FOOT_COVER = "来源：台积电 2025 年 Form 20-F（报告期 2025-12-31，SEC 提交 2026-04-16）。净收入为合并报表、新台币百万、日历年。客户占比为年报公布的净收入百分比。两家合计 36% 为作者把官方 19% 与 17% 相加。年报未公布客户名称，图中只用客户 A、B、C。不构成投资建议。投资有风险，入市需谨慎。制图 2026/11/19。"
FOOT_P2 = "来源：台积电 2025 年 20-F「至少占净收入 10% 的主要客户」表。NA 表示该年不足净收入的 10%，年报不列金额，不等于没有业务。金额单位为新台币百万。客户 A/B/C 为年报匿名代号，不是某家公司的名字。不构成投资建议。投资有风险，入市需谨慎。制图 2026/11/19。"
FOOT_P3 = "来源：同一份 20-F 净收入附注。平台与地区占比均为作者用官方金额除以当年净收入 3,809,054.3 百万新台币，四舍五入到一位。地区按客户总部所在国家分类，不是终销售地或使用地。不构成投资建议。投资有风险，入市需谨慎。制图 2026/11/19。"
FOOT_P4 = "来源：台积电 2025 年 Form 20-F。以上为阅读年报时的口径说明，不是投资判断，也不对未点名的客户做推测。不构成投资建议。投资有风险，入市需谨慎。制图 2026/11/19。"

def page(body_class, body):
    return f"""<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>
<div class=bg></div><div class=grid></div>
<div class="wrap {body_class}">
{body}
</div>
</body></html>"""

p1 = page("cover", f"""
  <div class=top><span class=brk>对照</span><span>台积电 2025 年报｜不猜测客户名字</span><span class=dt>2026.11.19</span></div>
  <h1>台积电有多<em>靠大客户</em></h1>
  <div class=h2box><h2 class=sub>年报只点出两家达到一成的客户，没有公布名字</h2></div>
  <div class=hero>
    <div class=k>2025 年合并净收入</div>
    <div class=v>3,809,054.3</div>
    <div class=u>百万新台币 · 日历年 · 官方金额</div>
  </div>
  <div class=pair>
    <div class="card a tall">
      <div class=badge>客户 A · 年报未点名</div>
      <div class=pct>19<i>%</i></div>
      <div class=amt>金额 <b>726,974.3</b> 百万新台币</div>
    </div>
    <div class="card b tall">
      <div class=badge>客户 B · 年报未点名</div>
      <div class=pct>17<i>%</i></div>
      <div class=amt>金额 <b>645,178.7</b> 百万新台币</div>
    </div>
  </div>
  <div class=sum>
    <div class=k>两家合计</div>
    <div class=v>36%</div>
    <div class=why>作者把官方 19% 与 17% 相加<br>用金额相除约为 36.0%</div>
  </div>
  <div class=sum style="border-color:rgba(127,211,255,.28)">
    <div class=k>其余客户合计</div>
    <div class=v style="color:#7fd3ff;text-shadow:0 0 18px rgba(127,211,255,.35)">64%</div>
    <div class=why>作者用 100% 减去上面的 36%<br>里面包含所有未点名、未达 10% 的客户</div>
  </div>
  <div class=note><b>只列出至少占净收入 10% 的客户。</b> 2025 年报没有第三家达到这一门槛。未达门槛的，不列名称也不列金额，不能据此猜测是谁。也不要用这张表去反推某家公司有多依赖台积电。</div>
  <div class=pair>
    <div class=card style="min-height:0;padding:18px 16px">
      <div class=badge>怎么读</div>
      <div class=nm style="margin-top:10px;font-size:28px">门槛是 10%</div>
      <div class=co style="margin-top:8px;line-height:1.4;white-space:normal;font-size:21px">年报只披露至少占净收入 10% 的客户，不是前十大完整名单。</div>
    </div>
    <div class=card style="min-height:0;padding:18px 16px">
      <div class=badge>怎么读</div>
      <div class=nm style="margin-top:10px;font-size:28px">没有公布名字</div>
      <div class=co style="margin-top:8px;line-height:1.4;white-space:normal;font-size:21px">客户 A、B 只是年报代号，不能写成某家具体公司。</div>
    </div>
    <div class=card style="min-height:0;padding:18px 16px">
      <div class=badge>怎么读</div>
      <div class=nm style="margin-top:10px;font-size:28px">不能反着推</div>
      <div class=co style="margin-top:8px;line-height:1.4;white-space:normal;font-size:21px">这是占台积电净收入的比重，不是某家公司对台积电的采购依赖。</div>
    </div>
  </div>
  <div class=foot>{FOOT_COVER}</div>
""")

p2 = page("inner", f"""
  <div class=top><span class=brk>对照</span><span>同一张主要客户表 · 三年对比</span><span class=dt>2026.11.19</span></div>
  <h1>三年里大客户在换位置</h1>
  <div class=h2box><h2 class=sub>份额在变，能上榜的客户也不完全一样</h2></div>
  <div class=sec>占净收入的官方百分比<span>金额单位：百万新台币</span></div>
  <div class=shell><table>
    <thead><tr><th style="width:200px">客户</th><th class=r>2023</th><th class=r>2024</th><th class=r>2025</th><th>金额怎么变</th></tr></thead>
    <tbody>
      <tr>
        <td><div class=nm>客户 A</div><div class=co>年报未点名</div></td>
        <td class="r na">未达 10%</td>
        <td class="r up">12%</td>
        <td class="r up">19%</td>
        <td>2024 年为 352,271.2，2025 年增至 726,974.3</td>
      </tr>
      <tr>
        <td><div class=nm>客户 B</div><div class=co>年报未点名</div></td>
        <td class="r dn">25%</td>
        <td class="r dn">22%</td>
        <td class="r dn">17%</td>
        <td>份额下降，金额仍从 546,550.9 增至 645,178.7</td>
      </tr>
      <tr>
        <td><div class=nm>客户 C</div><div class=co>年报未点名</div></td>
        <td class="r dn">11%</td>
        <td class="r na">未达 10%</td>
        <td class="r na">未达 10%</td>
        <td>2023 年金额 241,152.4；其后两年年报不再列金额</td>
      </tr>
    </tbody>
  </table></div>
  <div class=pair>
    <div class=card style="min-height:0;padding:20px 18px">
      <div class=badge>客户 A</div>
      <div class=nm style="margin-top:12px;font-size:30px">从榜外到 19%</div>
      <div class=co style="margin-top:8px;line-height:1.4;white-space:normal;font-size:22px">2023 年还不到 10%，两年后成为表上占比最高的客户。</div>
    </div>
    <div class=card style="min-height:0;padding:20px 18px">
      <div class=badge>客户 B</div>
      <div class=nm style="margin-top:12px;font-size:30px">份额降，金额升</div>
      <div class=co style="margin-top:8px;line-height:1.4;white-space:normal;font-size:22px">三年份额从 25% 降到 17%，但金额仍从 546,550.9 增至 645,178.7。</div>
    </div>
    <div class=card style="min-height:0;padding:20px 18px">
      <div class=badge>客户 C</div>
      <div class=nm style="margin-top:12px;font-size:30px">一度上榜后掉出</div>
      <div class=co style="margin-top:8px;line-height:1.4;white-space:normal;font-size:22px">2023 年占 11%，之后两年未达门槛，年报不再列金额。</div>
    </div>
  </div>
  <div class=note style="margin-top:14px"><b>每年上榜的也不完全是同一批。</b> 按这张表：2023 年达到门槛的是客户 B、客户 C；2024 年和 2025 年是客户 A、客户 B。客户 C 在后两年未达 10%，不再列出金额。</div>
  <div class=note><b>「未达 10%」不是「没有这家客户」。 </b>年报脚注写明：NA 表示该年收入不足公司净收入的 10%。掉出名单，只说明没跨过披露门槛，不能写成已经没有业务。</div>
  <div class=foot>{FOOT_P2}</div>
""")

def bar(label, pct, amount, cls=""):
    w = min(pct / 74.4 * 100, 100)  # scale vs largest geo; for platform HPC 57.6 still fine
    return f'''<div class=barrow>
      <div class=lab><b>{label}</b></div>
      <div class=track><div class="fill {cls}" style="width:{pct}%"></div></div>
      <div class=pv><b>{pct}%</b> · {amount}</div>
    </div>'''

# Use percent width directly for platform (max 57.6 looks good). For geo US 74.4 also fine in 100% track.
p3 = page("inner", f"""
  <div class=top><span class=brk>对照</span><span>同一份年报的平台与地区</span><span class=dt>2026.11.19</span></div>
  <h1>收入主要靠哪类平台</h1>
  <div class=h2box><h2 class=sub>占比为作者计算，用官方金额除以当年净收入</h2></div>
  <div class=sec>2025 年按平台<span>金额为官方数，单位百万新台币</span></div>
  <div class="shell bars" style="padding:8px 18px 12px">
    {bar("高性能计算", 57.6, "2,192,931.0")}
    {bar("智能手机", 29.2, "1,110,816.4", "gold")}
    {bar("物联网", 5.0, "191,046.8", "dim")}
    {bar("汽车", 4.9, "186,667.0", "dim")}
    {bar("数字消费电子", 1.3, "47,996.5", "dim")}
    {bar("其他", 2.1, "79,596.6", "dim")}
  </div>
  <div class=sec>2025 年按客户总部所在地<span>金额为官方数，单位百万新台币</span></div>
  <div class="shell bars" style="padding:8px 18px 12px">
    {bar("美国", 74.4, "2,834,692.1 百万")}
    {bar("中国", 8.6, "327,502.8 百万", "gold")}
    {bar("台湾", 7.9, "299,445.8 百万", "dim")}
    {bar("日本 / 欧中非 / 其他", 9.1, "347,413.6 百万", "dim")}
  </div>
  <div class=warn><b>地区不要读成「美国市场占了七成」。 </b>年报写明，净收入主要按客户总部所在国家分类。总部在美国的客户，不等于产品都在美国使用。</div>
  <div class=foot>{FOOT_P3}</div>
""")

# Japan+EMEA+Others official amounts: 150427.9+126584.1+70401.6 = 347413.6
# 347413.6/3809054.3 = 9.1207% → 9.1% author calc. Good, I'll verify in script later - add to verify_numbers? Already have individual geos. 3.9+3.3+1.8=9.0 due to rounding! Official one-decimal sum of 3.9+3.3+1.8=9.0, but amount ratio is 9.1%.

# THIS IS A PROBLEM. If I write 9.1% for the combined bar, that's amount-based.
# If I add official one-decimal percentages 3.9+3.3+1.8=9.0%.
# I should either list three separately or label 9.1% as 作者用三地金额合计再除。
# Don't write 9.1% as if it's 3.9+3.3+1.8.
# Better show three small rows instead of combining, or show amounts only for the rest.

# I'll change p3 to show Japan 3.9, EMEA 3.3, Others 1.8 separately - but that might be too many bars and overflow.
# Alternative: "日本、欧中非及其他 合计 347,413.6 百万，作者计算占 9.1%" clearly labeled, not as sum of rounded %.

# Space: platform 6 + geo 4 + warn might be tight. Let me show US, China, Taiwan, and a combined rest with clear 作者用三地金额合计再除 = 9.1%.

p3 = page("inner", f"""
  <div class=top><span class=brk>对照</span><span>同一份年报的平台与地区</span><span class=dt>2026.11.19</span></div>
  <h1>收入主要靠哪类平台</h1>
  <div class=h2box><h2 class=sub>占比为作者计算，用官方金额除以当年净收入</h2></div>
  <div class=sec>2025 年按平台<span>金额为官方数，单位百万新台币</span></div>
  <div class="shell bars" style="padding:6px 18px 8px">
    {bar("高性能计算", 57.6, "2,192,931.0")}
    {bar("智能手机", 29.2, "1,110,816.4", "gold")}
    {bar("物联网", 5.0, "191,046.8", "dim")}
    {bar("汽车", 4.9, "186,667.0", "dim")}
    {bar("数字消费电子", 1.3, "47,996.5", "dim")}
    {bar("其他", 2.1, "79,596.6", "dim")}
  </div>
  <div class=sec>2025 年按客户总部所在地<span>金额为官方数，单位百万新台币</span></div>
  <div class="shell bars" style="padding:6px 18px 8px">
    {bar("美国", 74.4, "2,834,692.1")}
    {bar("中国", 8.6, "327,502.8", "gold")}
    {bar("台湾", 7.9, "299,445.8", "dim")}
    {bar("日本", 3.9, "150,427.9", "dim")}
    {bar("欧洲中东非洲", 3.3, "126,584.1", "dim")}
    {bar("其他地区", 1.8, "70,401.6", "dim")}
  </div>
  <div class=warn><b>地区不要读成「美国市场占了七成」。 </b>年报写明，净收入主要按客户总部所在国家分类。总部在美国的客户，不等于产品都在美国使用。平台名称按年报原文翻译，高性能计算对应 High Performance Computing，不能直接写成只做人工智能。</div>
  <div class=foot>{FOOT_P3}</div>
""")

p4 = page("inner", f"""
  <div class=top><span class=brk>对照</span><span>读年报时的口径清单</span><span class=dt>2026.11.19</span></div>
  <h1>读年报别踩这些坑</h1>
  <div class=h2box><h2 class=sub>这些数字能说明什么，不能说明什么</h2></div>
  <div class=pits>
    <div class=pit><div class=no>01</div><div><div class=t>客户没有公布名字</div><div class=d>图里的客户 A、B、C 只是年报代号。没有官方点名，就不能写成某家具体公司，也不能把媒体推测当成事实。</div></div></div>
    <div class=pit><div class=no>02</div><div><div class=t>这是占台积电净收入的比重</div><div class=d>19% 或 17% 说的是占台积电净收入多少。不能反过来，用这个数字去推某家公司有多依赖台积电。</div></div></div>
    <div class=pit><div class=no>03</div><div><div class=t>只披露至少占净收入 10% 的客户</div><div class=d>2023 年客户 C 占 11%，后来两年未达门槛，年报不再列金额。掉出名单，不等于已经没有业务。</div></div></div>
    <div class=pit><div class=no>04</div><div><div class=t>地区是按客户总部所在地</div><div class=d>美国总部客户约占 74.4%（作者计算），不能读成芯片都卖到了美国，也不能读成美国本地制造。</div></div></div>
    <div class=pit><div class=no>05</div><div><div class=t>口径要写在数字旁边</div><div class=d>这是 2025 日历年、合并报表、新台币百万。合计 36%，以及平台、地区占比，凡不是年报直接公布的百分比，都已标明作者计算。</div></div></div>
  </div>
  <div class=note style="margin-top:16px"><b>可以带走的结论：</b> 2025 年报里，达到 10% 门槛的只有两家匿名客户，官方占比 19% 和 17%。结构高度集中，但年报没有点名，也不能用这些数字去反推某家公司的采购依赖。</div>
  <div class=note><b>读完先记住：</b> 合并报表、日历年、新台币百万；地区按客户总部；作者计算的百分比会单独标明。以上只是帮你看懂年报，不是买卖建议。</div>
  <div class=foot>{FOOT_P4}</div>
""")

for name, html in [("p1", p1), ("p2", p2), ("p3", p3), ("p4", p4)]:
    (D/f"{name}.html").write_text(html)
    print("wrote", name, "bytes", len(html))
