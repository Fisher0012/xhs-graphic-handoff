from pathlib import Path
import re
root=Path('/workspace/xhs/notes/20261113-大号-创始人离职影响')
tpl=(root/'template-02/approved_cover_v6.html').read_text()
style=re.search(r'<style>(.*)</style>',tpl,re.S).group(1)
ph='file:///workspace/xhs/notes/20261113-大号-创始人离职影响/photos/'
extra='''
/* inner pages: same approved template-02 tokens */
.sec{margin:22px 0 10px}
.info .ln{display:block;white-space:nowrap}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.cd{border-radius:12px;padding:16px 18px;background:rgba(18,24,35,.85);border:1px solid rgba(159,179,200,.14)}
.cd h3{font-family:NSB;font-weight:normal;font-size:28px;color:#7fd3ff;line-height:1.2;white-space:nowrap}
.cd p{margin-top:8px;font-size:26px;line-height:1.44;color:#dfe6ee}
.cd p span{display:block;white-space:nowrap}
.pt{border-radius:14px;padding:16px 22px 18px;background:rgba(14,18,26,.72);border:1px solid rgba(159,179,200,.14);margin-top:14px}
.pt:first-of-type{margin-top:0}
.ph{display:flex;align-items:center;gap:14px}
.num{font-family:NSB;font-size:26px;color:#fff;background:linear-gradient(180deg,#ff3b4e,#d3122b);border-radius:8px;padding:0 10px;line-height:40px;box-shadow:0 0 16px rgba(255,45,63,.4)}
.ph h3{font-family:NSB;font-weight:normal;font-size:32px;color:#fff;white-space:nowrap}
.rw{display:flex;gap:14px;margin-top:10px;align-items:flex-start}
.lb{flex:none;font-family:NSB;font-size:22px;line-height:37px;width:72px;text-align:center;border-radius:6px;margin-top:0}
.lb.a{color:#7fd3ff;background:rgba(127,211,255,.12);border:1px solid rgba(127,211,255,.35)}
.lb.b{color:#ff6b78;background:rgba(255,45,63,.12);border:1px solid rgba(255,45,63,.45)}
.tx{font-size:26px;line-height:1.44;color:#dfe6ee;min-width:0}
.tx span{display:block;white-space:nowrap}
.tx b{font-family:NSB;font-weight:normal;color:#fff}
.tx em{font-style:normal;font-family:NSB;color:#f3de9a}
.tx i{font-style:normal;font-family:NSB;color:#ff6b78}
.end{margin-top:16px;display:flex;align-items:center;gap:18px;border-radius:14px;padding:14px 20px;background:linear-gradient(100deg,#141b26,#0e121a);border:1px solid rgba(255,45,63,.52)}
.bar{margin-top:14px;border-radius:12px;padding:12px 20px;font-size:26px;line-height:1.44;white-space:nowrap;color:#dfe6ee;background:linear-gradient(100deg,#141b26,#0e121a);border:1px solid rgba(255,45,63,.52)}
.bar b{font-family:NSB;font-weight:normal;color:#ff6b78}
.bar em{font-style:normal;font-family:NSB;color:#f3de9a}
.end .av{width:84px;height:84px}
.end .tx b{color:#fff}
'''
def page(name,title1,title2,sub,body):
    return f'''<!doctype html><html><head><meta charset=utf-8><style>{style}{extra}</style></head><body>
<div class=bg></div><div class=grid></div>
<div class=wrap>
  <div class=top><span class=brk>对照</span><span>公开交棒案例｜不预测走向</span><span class=dt>2026.11.13</span></div>
  <h1><span>{title1}</span><span>{title2}</span></h1>
  <div class=h2box><h2>{sub}</h2></div>
{body}
  <div class=foot>根据公司公告和权威报道整理，不构成投资建议。投资有风险，入市需谨慎。制图 2026/11/13。官方用词为辞职。头像仅作身份识别。</div>
</div></body></html>'''
def norm(x):
    import re
    cj='\u4e00-\u9fff，。；：、'
    x=re.sub(r'(?<=['+cj+r'])\s+(?=(?:<[^>]+>)*[A-Za-z0-9])','',x)
    x=re.sub(r'(?<=[A-Za-z0-9%])((?:</?[a-z][^>]*>)*)\s+(?=(?:<[^>]+>)*['+cj+'])',r'\1',x)
    x=re.sub(r'(?<=['+cj+r'])((?:</?[a-z][^>]*>)*)\s+(?=[A-Za-z0-9])',r'\1',x)
    return x
def av(n):return f'<div class=av style="background-image:url({ph}{n}.jpg)"></div>'
def row(img,nm,co,yr,l1,l2):
    p=('<div class=avs>'+av('page')+av('brin')+'</div>') if img=='pair' else av(img)
    return f'<tr><td><div class=person>{p}<div><div class=nm>{nm}</div><div class=co>{co} · <span>{yr}</span></div></div></div></td><td><div class=info><span class=ln>{l1}</span><span class=ln>{l2}</span></div></td></tr>\n'
rows=[('jobs','乔布斯','苹果','1985/2011','1985年离开后，苹果陷入<em>经营困境</em>；','1997年回归，2011年交棒库克并<b>改任董事长</b>。'),
('gates','比尔·盖茨','微软','2000','交棒内部高管鲍尔默，盖茨<b>留任董事长</b>；','兼任首席软件架构师，2014年纳德拉接任。'),
('bezos','贝索斯','亚马逊','2021','提前约五个月宣布，长期执掌AWS的贾西接任；','贝索斯<b>改任执行董事长</b>，离开日常经营。'),
('pair','佩奇、布林','Alphabet','2019','交出CEO和总裁，由皮查伊兼任；','两人<b>留任董事</b>，并持有<b>高投票权B股</b>。'),
('ma','马云','阿里巴巴','2019','2013年已交CEO，提前一年宣布卸任主席；','张勇接任，马云<b>留任董事</b>至2020年股东大会。')]
t='  <div class=sec>同样是交棒，留下的不一样<span>只写公开事实</span></div>\n  <div class=shell><table><thead><tr><th class=p>人物 / 交棒年份</th><th>离开方式与接班 / 留下了什么</th></tr></thead><tbody>'+''.join(row(*r) for r in rows)+'</tbody></table></div>\n'
t+='''  <div class=sec>三个概念别混<span>职务、席位、投票权是三件事</span></div>
  <div class=cards>
    <div class=cd><h3>CEO / 总裁</h3><p><span>负责公司日常经营；</span><span>辞职不等于卖股份。</span></p></div>
    <div class=cd><h3>董事会席位</h3><p><span>监督管理层的工作，</span><span>也有权任免 CEO。</span></p></div>
    <div class=cd><h3>高投票权股</h3><p><span>一股可以投多票；</span><span>职务走了控制可留。</span></p></div>
  </div>
  <div class=bar><b>对照黄仁勋：</b>辞了 CEO、总裁和董事席位，股份还在，<em>一股一票</em>。</div>
'''
(root/'pages/01_内页.html').write_text(page('01','创始人走后','<em>留下了什么？</em>','顶级创始人交棒：谁接班，谁还留在董事会',norm(t)))
def pt(n,h,a1,a2,b1,b2):
    return f'''  <div class=pt><div class=ph><span class=num>{n}</span><h3>{h}</h3></div>
    <div class=rw><span class="lb a">前人</span><div class=tx><span>{a1}</span><span>{a2}</span></div></div>
    <div class=rw><span class="lb b">这次</span><div class=tx><span>{b1}</span><span>{b2}</span></div></div></div>
'''
b='  <div class=sec>三点对照<span>前人做法｜黄仁勋已知事实</span></div>\n'
b+=pt('01','交班准备：提前安排，还是即刻生效','库克原是 COO，贾西长期执掌 AWS，马云提前一年宣布；','这些交棒大多提前安排，接班人多来自公司内部核心岗位。','董事会 11 月 11 日接受辞职，<b>即刻生效</b>；CFO 科莱特·克雷斯','出任<b>临时 CEO</b> 并续任 CFO，董事会正在寻找正式继任者。')
b+=pt('02','影响力来源：职务、董事席位、投票权','贝索斯改任执行董事长，盖茨留任董事长兼首席软件架构师；','佩奇、布林留任董事并持<b>高投票权 B 股</b>，经营权与控制权分离。','总裁、CEO 和董事三项<b>全部辞去</b>，已离开英伟达董事会；','代理声明显示截至 2026 年 3 月 23 日持股 <em>3.58%</em>，英伟达<b>一股一票</b>。')
b+=pt('03','结果：没有统一公式','乔布斯 1985 年离开后苹果陷入<em>经营困境</em>，2011 年交棒后','苹果继续发展；戴尔创始人 2007 年又重新出任 CEO。','公司后来的变化，往往叠加行业、监管和接班人本身；','<i>不能简单归因于创始人离开，</i>本文也不预测英伟达。')
b+=f'''  <div class=end>{av('huang')}<div class=tx><span><b>辞了职务和董事，股份还在；现由临时 CEO 接班。</b></span><span>以上只是公开事实，不预测走向。你怎么看这次交棒？</span></div></div>
'''
(root/'pages/02_内页.html').write_text(page('02','黄仁勋这次','<em>关键看三点</em>','对照前人交棒，只看已公开的事实',norm(b)))
