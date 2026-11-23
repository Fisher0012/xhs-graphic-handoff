#!/usr/bin/env python3
"""按首日收盘价 $97.17 与 424B4 资本化/受益所有权表验算上图数字。"""
import json, re, sys
from pathlib import Path
N = Path(__file__).resolve().parents[1]
D = json.loads((N / "data.json").read_text())
lines = []
bad = 0

def ok(cond, msg):
    global bad
    tag = "PASS" if cond else "FAIL"
    if not cond:
        bad += 1
    lines.append(f"{tag}  {msg}")

price = D["ipo_price"]
close = D["close_price"]
ok(price == 83, f"发行价 {price}")
ok(close == 97.17, f"收盘价 {close}")
ok(round((close - price) / price * 100, 2) == 17.07 == D["close_change_pct"], "涨幅 17.07%")
ok(D["ticker"] == "ANT", f"代码 {D['ticker']}")
ok(D["offering_shares"] * 83 == 81340000000 == D["offering_usd"], "公开发行 980,000,000 × 83 = 81,340,000,000")
ok(D["primary_shares"] + D["selling_shares"] == D["offering_shares"], "新发 + 老股 = 公开发行")
ok(D["selling_shares"] == 23648646, "老股 23,648,646")
ok(D["private_placement_shares"] == 313253007, "私募股数 313,253,007")
ok(D["class_a_outstanding_as_adjusted"] + D["class_n_outstanding_as_adjusted"] == D["a_plus_n_outstanding"], "A+N 会计在外股数")
ok(D["a_plus_n_outstanding"] == 12372801314, "A+N = 12,372,801,314")
ok(D["a_plus_n_outstanding"] * 83 == 1026942509062 == D["author_mcap_at_ipo_usd"], "发行价市值测算 1,026,942,509,062")
ok(abs(D["a_plus_n_outstanding"] * 97.17 - D["author_mcap_at_close_usd"]) < 0.01, "收盘价市值测算 1,202,265,103,681.38")
ok(D["author_mcap_at_close_trillion_rounded"] == 1.20, "约 1.20 万亿美元")
ok(D["revenue_9m_2026_million"] == 33242, "前三季度收入 33,242")
ok(D["revenue_9m_2025_million"] == 2545, "上年同期收入 2,545")
ok(D["op_loss_9m_2026_million"] == 1260, "经营亏损 1,260")
ok(D["op_loss_9m_2025_million"] == 5224, "上年同期经营亏损 5,224")
ok(D["net_loss_9m_2026_million"] == 104039, "净亏损 104,039")
ok(D["fv_charge_9m_2026_million"] == 94324, "公允价值变动 94,324")
ok(D["net_loss_ex_fv_million_author"] == 104039 - 94324 == 9715, "其余 97.15 亿为作者相减")
ok(D["class_f_voting_pct"] == 50.1, "Class F 50.1%")
ok(D["amazon_class_n"] == 1936452353 and D["amazon_pct_capital"] == 14.6, "亚马逊 14.6%")
ok(D["google_class_n"] == 1774959745 and D["google_pct_capital"] == 13.4, "谷歌 13.4%")
ok(abs(D["amazon_pct_capital"] + D["google_pct_capital"] - D["combined_economic_pct"]) < 0.01, "两家合计约 28.0%")
ok(D["lockup_days"] == 365 and D["philanthropy_pledge_pct"] == 80, "锁定期 365 天，股权用于公益 80%")

expect_yi = {"Tom Brown": 234, "Sam McCandlish": 233, "Christopher Olah": 233, "Jared Kaplan": 232, "Jack Clark": 232, "Daniela Amodei": 231, "Dario Amodei": 231}
for f in D["founders"]:
    calc = f["shares"] * close
    yi = round(calc / 1e8)
    ok(abs(calc - f["close_paper_usd"]) < 0.01 and yi == f["rounded_yi_close"] == expect_yi[f["name"]], f"{f['name']} {f['shares']:,}×97.17={calc:,.2f} → 约{yi}亿")
    ok(f["sold_shares"] == 3378378 and f["sold_usd"] == 3378378 * 83, f"{f['name']} 出售 3,378,378×83={3378378*83:,}")

ok(min(f["rounded_yi_close"] for f in D["founders"]) >= 231, "七人按收盘价均超过 230 亿美元")

texts = []
for rel in [
    "03-design/p1.html", "03-design/p2.html", "03-design/p3.html", "03-design/p4.html",
    "04-文案.md", "final/04_发布文案.txt", "final/04_发布文案.md",
]:
    texts.append(((N / rel).read_text(encoding="utf-8"), rel))
alltxt = "\n".join(t for t, _ in texts)
p1 = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", texts[0][0]))
ok("Anthropic上市" in p1 and "7位创始人身价盘点" in p1, "封面去标签后含已定标题两行")
ok("按首日收盘价计算，人均超230亿美元" in re.sub(r"<[^>]+>", "", texts[0][0]), "封面副题逐字")
for label in ["约 231 亿美元", "约 234 亿美元", "约 233 亿美元", "约 232 亿美元"]:
    ok(label in texts[0][0] or label.replace(" ", "") in p1, f"封面有 {label}")
ok("97.17" in texts[1][0] and "17.07%" in texts[1][0], "内页1有收盘价与涨幅")
ok("12,372,801,314" in texts[1][0], "内页1有股数口径")
ok("813.4" in texts[1][0] and "1,048" in texts[1][0], "内页1有募资口径")
ok("23,648,646" in texts[1][0], "老股用精确股数")
ok("1.20" in texts[1][0], "内页1有 1.20 万亿")
ok("332.42" in texts[2][0] and "1,206%" in texts[2][0], "内页2收入与同比")
ok("170" in texts[2][0] and "1,127%" in texts[2][0], "内页2单季收入")
ok("12.60" in texts[2][0] and "1,040.39" in texts[2][0] and "943.24" in texts[2][0] and "97.15" in texts[2][0], "内页2亏损口径")
ok("50.1%" in texts[3][0], "内页3 Class F 投票权")
ok("14.6%" in texts[3][0] and "13.4%" in texts[3][0], "内页3 大股东比例")
ok("不是现金" in texts[0][0] or "不是现金" in alltxt, "标明纸面价值不是现金")
ok("Menlo" not in alltxt and "LLM API" not in alltxt, "未把未核市场份额写进图或文案")
banned = ["推荐股票", "荐股", "建议买入", "赶紧买", "必涨"]
ok(all(s not in alltxt for s in banned), "无个股买卖暗示")
inners = texts[1][0] + texts[2][0] + texts[3][0]
ok("约 234 亿美元" not in inners and "约 231 亿美元" not in inners, "内页不重复封面身价榜")

text = "\n".join(lines)
bad = sum(1 for ln in text.splitlines() if ln.startswith("FAIL"))
print(text)
print("verify_numbers:", "PASS" if not bad else f"FAIL({bad})")
sys.exit(1 if bad else 0)
