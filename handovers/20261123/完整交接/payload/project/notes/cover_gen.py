# 黑金封面：一行标题 + TOP10榜单
# 榜单高亮规范见 heijin.py 的 MEDAL/rank_style：只突出前三(金银铜+皇冠)，4–10名白字普通金条
# ===== 封面标题固定参数（所有期统一，不得按期调整；Fisher 2026-10-31 要求）=====
# 画布 1080x1440（2x 渲染 2160x2880）
# 字号 TITLE_PX=122px（固定，标题太长也不缩字号，只能缩左右边距，最小 30px）
# 字重 Noto Sans SC Black(NSB)；字间距 TITLE_LS=4px（不用负字间距）；行高 1.15；white-space:nowrap 一行
# 渐变 linear-gradient(165deg,#f7e6ae 0%,#f2cd52 40%,#e2ab12 75%,#c98f0c 100%)
# 页面左右边距 SIDE=40px；8字标题宽约 1004px≈93%
# 标题下方：下划线 → 副标题 → 榜单(10行×84px)，页脚两行固定贴底
TITLE_PX=122; TITLE_LS=4; SIDE=40
TITLE_GRAD="linear-gradient(165deg,#f7e6ae 0%,#f2cd52 40%,#e2ab12 75%,#c98f0c 100%)"
import sys
import sys;sys.path.insert(0,'/workspace/xhs/notes');from heijin import rank_style
F="file:///home/box/.fonts/"
def cover(path,tag,title_html,sub,rows,unit,src,fmt='{:.2f}'):
    mx=max(r[2] for r in rows);h=""
    for i,(cn,en,v,hl) in enumerate(rows):
        cr,rc,col,bar=rank_style(i)
        h+=f'''<div class=row><div class=rk style="color:{rc}">{cr}{i+1:02d}</div><div class=nm style="color:{col}">{cn}</div><div class=en>{en}</div><div class=v style="color:{col}">{fmt.format(v)}<span>{unit}</span></div></div>
<div class=bar style="width:{v/mx*952:.0f}px;background:{bar}"></div>'''
    # 一行封面按标题微调字号/字距（Fisher 2026-10-31 20:44：≤8字一行，字号从122往下调到刚好放下）
    FIT={'中国十大贸易伙伴':(102,4),'全球最大10家银行':(101,2),'全球最能借钱10国':(101,2),'全球通胀最高10国':(101,2),'全国城市GDP前十':(117,4)}
    TWO='h1{font-size:%dpx;letter-spacing:%dpx}'%FIT[title_html] if title_html in FIT else ''
    open(path,'w').write(f'''<html><head><meta charset="utf-8"><style>
@font-face{{font-family:NSB;src:url({F}NotoSansSC-Black.otf)}}@font-face{{font-family:NSM;src:url({F}NotoSansSC-Medium.otf)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1440px;overflow:hidden;background:radial-gradient(ellipse 760px 620px at 88% 4%,rgba(214,160,30,.16),rgba(214,160,30,0) 72%),linear-gradient(175deg,#121012 0%,#0a090a 50%,#030304 100%);color:#fff;font-family:NSM;padding:80px {SIDE}px 0;position:relative}}
.tag{{color:#e9b519;font-family:NSB;font-size:30px;letter-spacing:2px}}
h1{{font-family:NSB;font-size:{TITLE_PX}px;letter-spacing:{TITLE_LS}px;line-height:1.15;margin-top:18px;white-space:nowrap;display:inline-block;background:{TITLE_GRAD};-webkit-background-clip:text;color:transparent}}
.ul{{width:130px;height:6px;background:linear-gradient(90deg,#e9b519,transparent);margin:20px 0 16px}}
.sub{{color:#9b9b9e;font-size:26px}}
.list{{margin-top:26px}}
.row{{display:flex;align-items:baseline;height:62px;padding-top:6px}}
.rk{{width:112px;white-space:nowrap;font-family:NSB;font-size:32px}}
.nm{{font-family:NSB;font-size:44px;width:300px}}
.en{{flex:1;color:#8a8a8e;font-size:24px}}
.v{{font-family:NSB;font-size:48px}}.v span{{font-size:24px;color:#9b9b9e;margin-left:4px}}
.bar{{height:7px;border-radius:4px;margin:4px 0 11px}}
.foot{{position:absolute;left:0;right:0;bottom:34px;text-align:center;color:#66666a;font-size:21px;line-height:1.6}}
{TWO}</style></head><body><div class=tag>{tag}</div><h1 id=t>{title_html}</h1><div class=ul></div><div class=sub>{sub}</div><div class=list>{h}</div>
<div class=foot>{src}<br>风险提示：本文信息仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。</div></body></html>''')
