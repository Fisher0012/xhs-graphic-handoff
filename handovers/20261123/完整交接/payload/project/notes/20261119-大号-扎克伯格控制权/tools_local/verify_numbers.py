#!/usr/bin/env python3
"""双向核数：官方股数验算 vs 官方约数；扫描 HTML/文案禁止混用口径。作者验算不上图。"""
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

az = D["zuckerberg_beneficial_2026_10_01"]["class_a"]
bz = D["zuckerberg_beneficial_2026_10_01"]["class_b"]
ao = D["outstanding_2026_10_01"]["class_a"]
bo = D["outstanding_2026_10_01"]["class_b"]
econ = (az + bz) / (ao + bo) * 100
vote = (1 * az + 10 * bz) / (1 * ao + 10 * bo) * 100
bshare = bz / bo * 100
ashare = az / ao * 100
ok(az == 1220703 and bz == 341215148, f"受益所有股数 {az:,} / {bz:,}")
ok(ao == 2214455318 and bo == 341786026, f"10-01 已发行 {ao:,} / {bo:,}")
ok(abs(econ - 13.396068872908426) < 1e-12, f"经济权益精确值 {econ:.12f}%")
ok(abs(vote - 60.60335461906179) < 1e-12, f"投票权精确值 {vote:.12f}%")
ok(round(econ + 1e-15, 1) == 13.4, f"经济权益一位小数 {round(econ,1)} == 官方约数 13.4")
ok(round(vote, 1) == 60.6, f"投票权一位小数 {round(vote,1)} == 官方约数 60.6")
ok(round(bshare, 1) == 99.8, f"B类占已发行B类一位小数 {round(bshare,1)} == 官方表 99.8")
ok(ashare < 1, f"A类占已发行A类 {ashare:.6f}% < 1%，对应官方 *")
ok(D["outstanding_record_date"]["class_a"] == 2214472367, "登记日 A 已发行备查（不上图重算）")
ok(D["votes_per_share"]["class_a"] == 1 and D["votes_per_share"]["class_b"] == 10, "A=1票 B=10票")
ok(D["class_c_plan_2026"]["charter_effective"] == "2027-01-19", "C类章程生效日 2027-01-19")
ok(D["class_c_plan_2026"]["board_approved"] == "2026-10-19", "董事会批准 2026-10-19")
ok(D["footnote2_biohub"]["official_13_4_includes_these"] is True, "官方13.4%含 Biohub A类")
ok((az + bz) == 342435851, f"A+B 合计 {az+bz}")
ok((1 * az + 10 * bz) == 3413372183, f"投票权分子 {1*az+10*bz}")
ok((1 * ao + 10 * bo) == 5632315578, f"投票权分母 {1*ao+10*bo}")

texts = []
for rel in [
    "03-design/p1.html", "03-design/p2.html", "03-design/p3.html", "03-design/p4.html",
    "04-文案.md", "final/04_发布文案.txt", "final/04_发布文案.md",
]:
    texts.append(((N / rel).read_text(encoding="utf-8"), rel))
alltxt = "\n".join(t for t, _ in texts)

p1 = re.sub(r"<[^>]+>", "", texts[0][0])
p1 = re.sub(r"\s+", "", p1)
ok("扎克伯格为啥能掌权" in p1, "封面去标签后含逐字标题")
ok("13.4%" in alltxt, "出现 13.4%")
ok("60.6%" in alltxt, "出现 60.6%")
# 图上只保留官方约数，不要求出现「作者验算」或示例公式
pages = texts[0][0] + texts[1][0] + texts[2][0] + texts[3][0]
ok("作者验算" not in pages and "作者计算" not in pages, "四张图不上作者验算公式")
ok("99.8%" in texts[1][0], "内页1写明 B 类 99.8%")
ok("Biohub" in texts[2][0] and "没有金钱利益" in texts[2][0], "内页2说明 Biohub 无金钱利益")
ok("2026-10-20" in texts[2][0] or "股权登记日" in texts[2][0] or "10 月 20 日" in texts[2][0], "内页2提醒勿混用登记日")
ok("2027-01-19" in texts[1][0] or "2027 年 1 月 19 日" in texts[3][0] or "2027-01-19" in texts[3][0], "内页写明章程生效日")
ok("20%" in texts[3][0] and "80%" in texts[3][0], "内页3写明 20%/80% 捆绑")
ok("无限权力" in texts[3][0], "内页3明确写不是无限权力")
ok("2016" not in alltxt, "正文与图未引入 2016 年撤回方案")
ok("暂停发行" not in alltxt and "发行暂停" not in alltxt, "未把媒体暂停发行写成事实")
ok("56.1" not in alltxt, "未把登记日 56.1% 混进主口径")
ok("5,000,000,000" not in alltxt and "5000000000" not in alltxt, "未把授权股本当作已发行")
banned = ["\u63a8\u8350\u80a1\u7968", "\u8350\u80a1", "\u5efa\u8bae\u4e70\u5165", "\u8d76\u7d27\u4e70", "\u5fc5\u6da8"]
ok(all(s not in alltxt for s in banned), "无个股买卖暗示")

text = "\n".join(lines)
bad = sum(1 for ln in text.splitlines() if ln.startswith("FAIL"))
print(text)
print("verify_numbers:", "PASS" if bad == 0 else f"FAIL({bad})")
sys.exit(1 if bad else 0)
