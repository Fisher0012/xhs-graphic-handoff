# 期目录内适配：复用共享 /workspace/xhs/tools/check_titles.py 的 check()（不改原文件），指向本期 p1–p5
import sys, importlib.util
spec = importlib.util.spec_from_file_location('ct', '/workspace/xhs/tools/check_titles.py'); ct = importlib.util.module_from_spec(spec); spec.loader.exec_module(ct)
D = sys.argv[1] if len(sys.argv) > 1 else '/workspace/xhs/notes/20261113-大号-居民医保缴费榜/03-design'
bad = 0
for i in range(1, 6):
    h, s = ct.check(f'{D}/p{i}.html')
    fs = float(h['fs'][:-2]); grad = '165deg' in h['bg'] or 'f7e6ae' in h['bg'] or 'rgb(247, 230, 174)' in h['bg']
    if i == 1:
        avail = 1080 - 80; ratio = (h['right'] - 40) / avail
        ok = h['lines'] == 1 and 90 <= fs <= 125 and 0.75 <= ratio <= 0.85 and grad
        print(f"p{i} 封面 h1={h['text']} fs={h['fs']} lines={h['lines']} 占可用宽={ratio:.1%} 渐变={grad} | sub fs={s and s['fs']} color={s and s['color']} -> {'PASS' if ok else 'FAIL'}")
    else:
        ok = h['lines'] == 1 and fs == 64 and grad and h['right'] <= 1080 - 56 and s and s['fs'] == '26px' and s['color'] == 'rgb(155, 155, 158)' and s['lines'] == 1
        print(f"p{i} 内页 h1={h['text']} fs={h['fs']} lines={h['lines']} right={h['right']} 渐变={grad} | sub fs={s['fs']} color={s['color']} lines={s['lines']} -> {'PASS' if ok else 'FAIL'}")
    bad += (not ok)
print('check_titles:', 'PASS' if not bad else f'FAIL({bad})'); sys.exit(1 if bad else 0)
