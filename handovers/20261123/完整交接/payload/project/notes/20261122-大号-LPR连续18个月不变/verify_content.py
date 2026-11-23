"""LPR期内容门：官方原文→data.json→HTML→PNG 双向核对、标题/间距/合规。
只用标准库+bs4+PIL；共享工具通过子进程按原路径调用，不在本文件顶层导入。"""
import glob
import html
import json
import re
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from PIL import Image

N = Path(__file__).resolve().parent
S = N / 'sources'
TOOLS = '/workspace/xhs/tools'
D = json.loads((N / 'data.json').read_text())
fails = []


def ok(c, msg):
    print(('PASS ' if c else 'FAIL ') + msg)
    if not c:
        fails.append(msg)


def text(f):
    raw = (S / f).read_text(encoding='utf-8', errors='ignore')
    raw = re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>', '', raw, flags=re.S)
    return html.unescape(re.sub(r'\s+', '', raw))


# 1 LPR 逐份公告复算
for r in D['lpr']:
    y, m, d = r['date'].split('-')
    head = f'{int(y)}年{int(m)}月{int(d)}日贷款市场报价利率（LPR）为：1年期LPR为{r["one_year"]:.1f}%，5年期以上LPR为{r["five_year"]:.1f}%'
    ok(head in text(r['file']), f'公告原文 {r["date"]} {r["one_year"]}/{r["five_year"]}')
after = [r for r in D['lpr'] if r['date'] > '2025-05-20']
ok(len(after) == 18 and all((r['one_year'], r['five_year']) == (3.0, 3.5) for r in after), '2025-06至2026-11共18次均为3.0/3.5')
ok([r['date'][:7] for r in after] == [f'2025-{m:02d}' for m in range(6, 13)] + [f'2026-{m:02d}' for m in range(1, 12)], '18次逐月连续无缺月')
apr = next(r for r in D['lpr'] if r['date'] == '2025-04-21'); may = next(r for r in D['lpr'] if r['date'] == '2025-05-20')
ok((apr['one_year'], apr['five_year'], may['one_year'], may['five_year']) == (3.1, 3.6, 3.0, 3.5), '上次调整2025-05-20各降10个基点')
ok(not any(r['date'] > '2025-05-20' and (r['one_year'], r['five_year']) != (3.0, 3.5) for r in D['lpr'] + [dict(date='2026-12-01', one_year=3.0, five_year=3.5)]), '反例防护：计数逻辑不接受异常值')
# 反例：插入一次变化后计数必须不再是18连续
bad = after[:5] + [dict(after[5], one_year=2.9)] + after[6:]
ok(not all((r['one_year'], r['five_year']) == (3.0, 3.5) for r in bad), '反例：任一月变化即判不连续')
# 2 新发放利率
flat = re.sub(r'\s+', '', (S / 'mpr_2026q3.txt').read_text())
for k, v in D['new_loan_rates_2026_09']['items'].items():
    ok(f'{k}{v["sep"]:.2f}{v["vs_jun"]:.2f}{v["yoy"]:.2f}' in flat.replace('其中：', ''), f'报告表4 {k} {v}')
ok('个人住房贷款加权平均利率' not in text('finstat_202610.html'), '10月金融统计原文未列房贷利率，故不用10月数')
# 3 规则原文
ok('加点可为负值' in text('pboc_2024_11.html') and '在利率重定价日，定价基准调整为最近一个月贷款市场报价利率' in text('pboc_2024_11.html'), '2024第11号：加点可负、重定价日换基准')
ok('合同约定为固定利率的，利率水平在合同期保持不变' in text('pboc_2024_11.html'), '2024第11号：固定利率合同期不变')
ok('商业性个人住房贷款重新约定的重定价周期最短为一年' in text('pboc_2019_30.html'), '2019第30号：转换后重定价周期最短一年')
ok('2024年12月20日贷款市场报价利率（LPR）为：1年期LPR为3.1%，5年期以上LPR为3.6%' in text('lpr_2024-12-20.html'), '举例：2024-12 LPR 3.6%')
ok('2025年12月22日贷款市场报价利率（LPR）为：1年期LPR为3.0%，5年期以上LPR为3.5%' in text('lpr_2025-12-22.html'), '举例：2025-12 LPR 3.5%')
# 4 成图文字反查（HTML）
pages = {i: BeautifulSoup((N / f'03-design/p{i}.html').read_text(), 'html.parser').get_text(' ', strip=True) for i in range(1, 5)}
need = {1: ['LPR连续', '18个月不变', '3.0%', '3.5%', '18次报价未变', '3.1%→', '3.6%→', '各降10个基点'],
        2: ['加点可为负值', '举例', '固定利率'], 3: ['3.6%', '3.5%', '待公布', '不做预测', '举例'],
        4: ['3.05', '3.03', '2.96', '-0.08', '-0.19', '-0.01', '0.45', '作者计算', '表4']}
for i, ws in need.items():
    for w in ws:
        ok(w in pages[i], f'p{i} 含「{w}」')
allt = ' '.join(pages.values()) + (N / 'final/04_发布文案.txt').read_text()
for w in ['降息', '将下调', '有望下调', '建议提前还款', '赶紧', '工商银行', '建设银行', '农业银行', '中国银行', '招商银行', '最高', '金牌', '银牌', '铜牌']:
    ok(w not in allt, f'禁写词不出现：{w}')
ok('<svg' not in (N / '03-design/p1.html').read_text(), '封面无皇冠/奖牌SVG（非排名）')
ok('10月份' not in allt and '10月企业' not in allt and '约3.1%' not in allt, '未使用非官方原文的10月新发放利率')
# 5 标题（共享 check_titles.check，子进程按原路径调用）
code = ("import sys,json;sys.path.insert(0,%r);import check_titles;"
        "print(json.dumps([check_titles.check(%r%%i) for i in range(1,5)],ensure_ascii=False))") % (TOOLS, str(N / '03-design/p%d.html'))
res = json.loads(subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, check=True).stdout.strip().splitlines()[-1])
print(json.dumps(res, ensure_ascii=False))
h, s = res[0]
ok(h['fs'] == '122px' and h['lines'] == 2 and h['right'] <= 1040 and '165deg' in h['bg'], '封面标题122px两行（每行≤7字）、金渐变、未越界')
ok(all(len(x) <= 7 for x in h['text'].split('⏎')), '封面每行≤7字')
for i in range(1, 4):
    h, s = res[i]
    ok(h['fs'] == '64px' and h['lines'] == 1 and h['right'] <= 1040 and s['fs'] == '26px' and s['lines'] == 1, f'内页{i}标题64px一行、副标题26px一行')
# 6 成品
for f in sorted((N / 'final').glob('0[0-3]_*.png')):
    ok(Image.open(f).size == (2160, 2880), f'{f.name} 2160×2880')
for i, f in enumerate(['00_封面.png', '01_房贷利率怎么定.png', '02_存量房贷看重定价日.png', '03_新发放利率对照.png'], 1):
    ok((N / f'03-design/p{i}.png').read_bytes() == (N / 'final' / f).read_bytes(), f'final/{f} 与渲染稿一致')
body = (N / 'final/04_发布文案.txt').read_text().split('正文：\n')[1].split('\n\n话题：')[0]
ok(len(body.replace('\n', '')) <= 1000 and '不构成投资建议' in body, f'正文{len(body.replace(chr(10), ""))}字≤1000且有风险提示')
# 7 间距：共享 measure_space.py 原公式（子进程中仅替换文件发现路径）
ms = ("import glob,runpy;o=glob.glob;glob.glob=lambda p:sorted(o(%r)) if p=='2026103*/03-design/final/0[1-4]_*.png' else o(p);"
      "runpy.run_path('%s/measure_space.py',run_name='__main__')") % (str(N / 'final/0[1-3]_*.png'), TOOLS)
out = subprocess.run([sys.executable, '-c', ms], capture_output=True, text=True).stdout
print(out)
gaps = [float(x) for x in re.findall(r'最大空白\s*([\d.]+)%', out)]
ok(len(gaps) == 3 and max(gaps) <= 8, '内页最大连续空白≤8%')
# 8 合规初筛
c = subprocess.run([sys.executable, f'{TOOLS}/compliance_precheck.py', '--dir', str(N)], capture_output=True, text=True)
print(c.stdout)
ok(c.returncode == 0, 'compliance_precheck.py 退出码0')
print('RESULT', 'FAIL' if fails else 'PASS', len(fails))
sys.exit(1 if fails else 0)
