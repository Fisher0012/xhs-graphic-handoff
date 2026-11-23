#!/usr/bin/env python3
"""双向核数：官方金额相除 vs 官方百分比；分项加总 vs 净收入。"""
import json, sys
from pathlib import Path
N = Path(__file__).resolve().parents[1]
D = json.loads((N/"data.json").read_text())
rev = D["net_revenue_mn"]
lines = []
bad = 0

def ok(cond, msg):
    global bad
    tag = "PASS" if cond else "FAIL"
    if not cond:
        bad += 1
    lines.append(f"{tag}  {msg}")

# 分项加总
for year, key in [("2023","platform_mn_2023"),("2024","platform_mn_2024")]:
    s = sum(D[key].values())
    ok(abs(s - rev[year]) < 0.05, f"{year} 平台加总 {s} == 净收入 {rev[year]}")
s = sum(D["platform_mn_2025"].values())
ok(abs(s - rev["2025"]) < 0.05, f"2025 平台加总 {s} == 净收入 {rev['2025']}")
s = sum(D["geo_mn_2025"].values())
ok(abs(s - rev["2025"]) < 0.05, f"2025 地区加总 {s} == 净收入 {rev['2025']}")
s = sum(D["product_mn_2025"].values())
ok(abs(s - rev["2025"]) < 0.05, f"2025 产品加总 {s} == 净收入 {rev['2025']}")

# 客户官方百分比 vs 金额/净收入
for name, years in D["customers"].items():
    for y, rec in years.items():
        if rec.get("amount_mn") is None:
            ok(rec.get("status") == "NA_lt_10", f"客户{name} {y} 无金额且标记未达10%")
            continue
        calc = rec["amount_mn"] / rev[y] * 100
        official = rec["pct_official"]
        # 官方百分比为四舍五入到整数
        rounded = int(calc + 0.5) if calc >= 0 else int(calc - 0.5)
        # 22% for 21.571 should be rounded half up? 21.571 -> 22; 16.938 -> 17; 19.085 -> 19; 12.171 -> 12; 25.283 -> 25; 11.156 -> 11
        ok(abs(calc - official) < 0.6 and rounded == official,
           f"客户{name} {y}: {rec['amount_mn']}/{rev[y]}={calc:.3f}% 官方 {official}%")

# 2025 A+B
a = D["customers"]["A"]["2025"]["amount_mn"]
b = D["customers"]["B"]["2025"]["amount_mn"]
combo_amt = (a+b)/rev["2025"]*100
combo_pct_sum = D["customers"]["A"]["2025"]["pct_official"] + D["customers"]["B"]["2025"]["pct_official"]
ok(abs(combo_amt - 36.0) < 0.05, f"2025 A+B 金额占比 {combo_amt:.3f}% ≈ 36.0%")
ok(combo_pct_sum == 36, f"2025 官方百分比相加 {combo_pct_sum}% = 36%")

# 平台/地区作者计算（保留一位）
def pct1(x):
    return round(x / rev["2025"] * 100, 1)

expected = {
    "High Performance Computing": 57.6,
    "Smartphone": 29.2,
    "Internet of Things": 5.0,
    "Automotive": 4.9,
    "Digital Consumer Electronics": 1.3,
    "Others": 2.1,
}
# check my rounding
for k,v in D["platform_mn_2025"].items():
    p = pct1(v)
    lines.append(f"INFO  2025 平台 {k}: {v} → 作者计算 {p}% （金额/净收入，四舍五入到一位）")
    ok(p == expected[k], f"平台 {k} 一位百分比 {p} == 预设 {expected[k]}")

geo_expected = {
    "United States": 74.4,
    "China": 8.6,
    "Taiwan": 7.9,
    "Japan": 3.9,
    "Europe, the Middle East and Africa": 3.3,
    "Others": 1.8,
}
for k,v in D["geo_mn_2025"].items():
    p = pct1(v)
    lines.append(f"INFO  2025 地区 {k}: {v} → 作者计算 {p}%")
    ok(p == geo_expected[k], f"地区 {k} 一位百分比 {p} == 预设 {geo_expected[k]}")

# 换算：百万 ÷ 100 = 亿
ok(abs(726974.3/100 - 7269.743)<1e-9, "客户A 2025 726974.3百万 = 7269.743亿")
ok(abs(645178.7/100 - 6451.787)<1e-9, "客户B 2025 645178.7百万 = 6451.787亿")

text = "\n".join(lines)+"\n"
out = N/"tools_local/verify_numbers_result.txt"
out.write_text(text)
print(text)
print("verify_numbers:", "PASS" if not bad else f"FAIL({bad})")
sys.exit(1 if bad else 0)
