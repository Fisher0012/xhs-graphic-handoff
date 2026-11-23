from pathlib import Path
from datetime import datetime
import json
O=Path('/workspace/xhs/handoff/20261123');D=O/'docs';D.mkdir(exist_ok=True)
def w(name,text):(D/name).write_text(text.strip()+'\n')
w('01-仓库与上传操作边界.md','''
# 已确认仓库与本阶段权限

- 既有专用私有仓库：https://github.com/Fisher0012/xhs-graphic-handoff
- GitHub只读API确认：唯一分支 `main`，HEAD `06ad3ee5b098d7fae1741d8d30bef57bbb716c9f`，未保护；当前开放PR为0。未查询已关闭PR全历史。查询后远端仍可能变化，写入前重新读取。
- 仓库上次推送时间：2026-11-07 22:32:07 Asia/Shanghai。现有README明确仅为11/07受限文字交接，不含大图/全量资产。本次应**增量追加**新的日期目录，不删除或改写旧交接、原ZIP和旧缺口。
- 此轮只读了仓库元数据、分支、树、README及开放PR；原始返回留于 `../evidence/`。不是clone，没有checkout、commit、push、PR创建或远端文件修改。
- `/workspace/xhs` 不是Git工作区，没有本地分支、origin或可报告的dirty状态；不能把它说成main已同步。根目录与所有资产的快照位于 `../payload/project/`。
- 本地另有 `/workspace/ops-state-repo`：main，641b3dc，status clean，没有配置origin；它含多个其他项目，不作为本次目标、更不修改。GitHub存在Fisher0012/ops-state，只作历史旁证，不以此推断本地快照与远端一致。
- xhs-daily-brief、xhs-auto-reply是另外两个仓库，不是本图文交接仓库，不应触碰。

## 留给主助手的正式CloudAgent更新任务（本轮未执行）
1. 通过正式CloudAgent选择上述**既有私有仓库**，重新核HEAD和最新PR；正常分支/PR增量提交，不直接覆盖main，不force-push。若接手方式需主助手额外权限，由主助手处理，本线程不读取token。
2. 在 `handoff/xhs/20261123/` 放本目录所有实体，README链接新入口；历史 `handoff/xhs/source-export/`、`archive/` 保持。仅限本项目，不夹带其他项目代码/配置或全局运维状态。
3. 按UPLOAD_MANIFEST.tsv处理全部候选；大文件不能假装已上传。>100MiB文件必须LFS或经确认的受控附件方案；建议全部视频/音频采用LFS。单次push也有大小限制，不能直接普通Git塞进2.7GB。
4. 媒体未做逐帧隐私检查，Getty等图片再使用许可未清。保持私有仓库，不生成公开链接；若要对外公开，先清权并审查媒体隐私。自动扫描零命中不等于全媒体安全审查。
5. 上传后从GitHub/CloudAgent新鲜checkout读取README、四张PNG、源HTML、完整长推及清单；验证LFS已拉取实体而非仅指针，并逐项复算SHA。报PR/commit精确URL、上传与未上传数量/体积、剩余缺口；没有远端验证不得说“GitHub已更新完整”。
6. 如果云代理不能读取盒子文件，主助手先用批准的文件交付渠道搬运本目录实体；不能只把 `/workspace/...` 路径塞进提示词。当前还未建立盒子到CloudAgent的数据搬运链路。
''')
w('02-当前任务与用户纠正.md','''
# 当前Burry任务：四图待Fisher审阅，不是已批准成品

实体：[完整Burry目录](../payload/project/notes/20261122-大号-Burry看空与减仓/)。最新四图是该目录final/00_封面.png、01_原先为何做空.png、02_财报与看空逻辑.png、03_减仓不等于转多.png；四图2160×2880。源HTML分别在cover/与pages/。final/07_总览.png是总览，05_来源说明.txt与06_交付证据.md必须一起读。

## Fisher原话与返工原因
- t87u：“认真了解这个推文，补充必要的信息和观点以及维度，数据和信息要准确。创作一篇，用英伟达那个模板，先输出内容框架。” https://x.com/Kshsb783142/status/2124077630270177531
- t88u：“为什么把 burry 原先的做空理由去掉？这是个重点。而且现在的结构很奇怪，重新思考输出结构”。第一版把原始逻辑削弱，变成减仓→仓位→基本面→期权→已知未知，重复割裂，偏离推文。不能再次删掉原始理由。
- t89u：“太繁琐，精简成 4 张。然后直接输出封面给我看。注意模板规则，不要犯低级错误”。不再给长框架、不等中间确认，不凑5—6张。
- t90u：“人物头像太差了，重新换一个，都偏了。同时把三张配图一起做出来”。仅换封面人物及必要裁切/位置，其余标题、主卡与布局保留，另做三张内页。
- t91u：“更新 GitHub，不要遗漏任何信息，我让其他 ai 接管这个任务”。**当前已暂停内容制作，转为交接**。本线程只本地整理，正式CloudAgent远端更新留主助手。

## 最终四页内容与状态
1. 封面：两行“伯里做空英伟达 / 为何又减仓一半”；50%明确是NVDA、SMH原有看跌期权各卖一半，不是持股、总资产或全部风险减半。图中媒体转述标记不能删。
2. 原先为何做空：需求持续性、客户采购/融资结构、云厂商设备折旧年限争议，保留各自经济机制，不把观点当查实欺诈。
3. 财报与看空逻辑：强业绩证明当期需求/利润，不自动证伪长期回报风险；风险报道也不能一举否定财报。GAAP口径、日期不能混。
4. 减仓不等于转多：交易报道与仍保留的头寸一次说清；具体动机是分析，不编成本/净盈利，不搞独立期权算例。

## 必须一并保留的历史
- 02-框架.md为四页版，02-框架_v1_已被替代.md、02-框架_v2_五张_已被替代.md为被替代版本，不再沿用但不删除。
- sources/x_full_posts.json.txt存两条完整长推（note_tweet.text）；quoted_post.jpg为引用附图。不是只拿截断摘要假装读全文。
- sources/01、02为原文摘录/原始理由补核；nvidia_FY27Q3_本轮复核原文.txt为财报；decisions.tsv和00-研究记录.md为决策过程。
- 旧照片burry_bi_getty.jpg、burry_portrait_crop.jpg用户否决（蓝衬衫侧脸仰头）；不能换个裁切继续用。burry_jonas_karlsson.jpg候选脸小未用；candidate_cc_ben.jpg实际是摩根大通楼，不是Burry，不可误用。
- 新图burry_front_astrid_getty.jpg及burry_front_portrait.jpg；来源与许可见sources/04-新照片出处与检索限制.md。Getty再使用权**未取得**，不是CC，不能说已清权。
- evidence/before_t90保留旧封面；封面人物改前后.png、四张模板对比、400px总览、DOM检查、最小改动像素检查均在evidence/。
- 旧evidence/封面验收.md已失效，以final/06_交付证据.md为最新；不能把旧回执当新四图完整PASS。

## 实际验证及仍未做
既有证据记载：四原图/400px缩略/真实模板并排亲看；内页溢出0、1—2字孤行0、行首标点0；封面人物与必需署名区域外像素差异0。本次交接重新核实体/尺寸/哈希，不再渲染修改内容。没有完整成品正文、没有完整九件门禁PASS、没有跨模型复核、没有用户已通过证据；未发布、未传Mac。本轮不推进修图、文案或选题。
''')
w('03-事实来源与版权风险.md','''
# 核数要点与来源层级

完整URL、日期与摘录见[本期来源说明](../payload/project/notes/20261122-大号-Burry看空与减仓/final/05_来源说明.txt)与sources/全部文件。这里只列接手时不能丢的区别；本轮未重新访问核实市场新闻。

- 完整主帖2124077630270177531与引用帖2124051800944992668已保存。原推作者的交易解释不等于Burry亲口动机。
- Burry 2026-05-23公开摘要承认当时需求强，质疑可持续性和集中采购；2026-08-13 Moneywise/Yahoo是融资观点的媒体转述；折旧争议来自2025-11-11 CNBC引语，是既有观点，不装成2026新披露。
- 折旧针对客户云厂商对服务器/GPU的会计年限，不直接写成“英伟达本期利润被同项折旧延长抬高”。产品迭代不等于旧GPU立即失去经济价值。循环融资是需审视的结构，不是已证实造假。
- 英伟达公司公告标2026-11-17；2027财年第三季度截至2026-10-25：营收1158亿美元、同比+103%；GAAP净利653亿美元、同比+105%。非GAAP为649亿/+109%，不可串用。实体原文留存，不用“Q3”误指自然季度。
- 交易细节主要据Stocktwits/Shashank Nayar、Yahoo分发（2026-11-21 02:32 Asia/Shanghai）、Benzinga（04:15 Asia/Shanghai）及Newsquawk（01:02 Asia/Shanghai）。NVDA、SMH看跌各卖原有一半；另一半保留，纳指100的2027年4月看跌据报道未减。不是13F名义本金，也不是当前全账户资产表。
- 原始Substack trading-post-november-20-2026-turn页面Paid，交易正文未读，不越付费墙。媒体称获利≠已核精确成本/成交价/净利润，不写“暴赚多少”。
- Reuters调查报道2026-11-21 03:13 Asia/Shanghai晚于01:02减仓快讯，不得因果倒置。调查不等于认定违法。
- https://michaeljburry.substack.com/p/abridged-the-heretics-guide-to-ais
- https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Third-Quarter-Fiscal-2027/default.aspx
- https://finance.yahoo.com/markets/stocks/articles/michael-burry-locks-gains-nvidia-183241854.html
- https://www.reuters.com/3fec1b0a85a0/world/us-secs-nvidia-probe-is-examining-potential-accounting-issues-sources-say-2026-11-20/

## 新头像权利限制（必须醒目交接）
Michael Burry真人，Astrid Stawiarz / Getty Images，2015-11-23纽约首映，编号498541178；原图1500×1021，使用裁切887×1167，近正面、保留头和下巴。照片页：
https://www.gettyimages.co.uk/detail/news-photo/michael-burry-attends-the-big-short-new-york-screening-news-photo/498541178
使用及图注页面：https://www.investopedia.com/short-sellers-now-betting-big-against-ai-11842994

已保留署名与来源；**非CC、独立公开/商业再使用授权未确认**。主动找过Commons/CC但未找到合适且可核可用肖像，不等于世上不存在。私有交接保留原图是资产留档，不是版权许可。公开发图前必须处理权利。其他历史素材/媒体也不因进入本包自动清权。
''')
w('04-规则模板与机制.md','''
# 长期规则、真模板与PSTACK边界

## 账号与操作红线
主号「阿信学财经」；小号当前使用「阿信财经笔记」，历史名「阿信财读笔记」仍在AGENTS等旧文档。不要抹去旧名称造成索引失联。历史Sphere商单实体保留；最新STATE写“不接商单”，在未有新授权前不据历史资料继续接单。

Fisher publishes by hand and I never publish for him.
No Playwright or other bot-like publishing automation is allowed; local headless Chrome rendering is fine.
任何机器人做发布自动化都不得再用 Playwright 或其他易被平台识别为机器人的手段，新方案须先经 Fisher 批准。

- 本次不发布、不传Mac、不外联、不改共享资产、例程或其他项目。旧AGENTS写小号交自动化发布调研，不构成当前自动发布授权，禁止据此启用旧发布代码。
- 数字真实且有来源：期间、币种、单位、GAAP、统计分母、百分比/百分点准确。不荐具体产品、不承诺收益、不编盈利。
- Fisher指定标题照用；更换已选标题先取得指示。只改点名部分，不顺手重构其余布局。
- 每日≥3候选（大号2+小号1），待选不代选、不自动开工。本次不更改任何原例程，活动状态尚未实时核实，接手后应协调避免重复执行。
- 简洁中文、直接做；脚本PASS不能代替亲看真实原图与缩略。
- Mac历史目标：桌面/新图文笔记/阿信学财经/。有些期次已传、有些未传，见状态表，不能统称已归档。传Mac需具体授权，不因GitHub交接顺手传。
- 旧“只留文件夹，不打压缩包”遵守：本次为实体文件夹；既有历史tgz/zip保留并清单列出，不删历史。

## 唯一指定模板
实体已一并带入payload/project/notes/20261113-大号-英伟达持股：
- final_v2/00_封面.png（真正通过的封面参考）
- cover_v2/00_封面.html（封面底稿）
- pages_v2/02_辞职与股份.html、final_v2/02_辞职与股份.png（内页底稿）
不是创始人离职模板，不是税种榜通用黑金模板。黑网格、白红大标题、蓝色数字/高亮块、真人头像、红身份角标、小标签、大数字小单位。非排名事件**无奖牌/金银铜/最高/进度条**。主副标题需留呼吸，两行标题间隔明显；头像居中，脸够大、头和下巴完整，不向侧面偏出卡。不能缩字号硬塞、不能堆等宽卡填满。内页标题尽量一行、字体中等，三页不同结构但同视觉语言；底部不过空，不能有孤字、行首标点、重叠/裁切。

## PSTACK真实状态
2026-11-22 11:34 Asia/Shanghai正式切入，范围仅本项目。原件PSTACK.md及pstack/20261122-切入证据.md、外置准备包与授权回执都已带入。PSTACK.md的“当前任务”是当时LPR微修，不是本次Burry/交接的新要求。
- 不再额外加审查官、独立回执和阶段重复签核；保留H1/H2及真实视觉核验。
- 原verify_receipt FAIL仍是历史FAIL，不能删掉或改写。LPR微修后旧receipt哈希不再覆盖新文件；税收C06 FAIL仍在；存贷款C14 FAIL也保留。
- 宿主未暴露model指定、poteto-agent、跨厂商面板、/loop；没有完整模型栈落地，不得编造跨模型复核或后台循环。
- 历史PSTACK.md称逻辑目录不存在是历史时点记录；本轮确已读到逻辑目录的worker.md，不能照搬旧路径状态为当前事实。实际已复制reference/poteto-mode参考文档，未改共享技能。
- 不运行全局setup；本次不改例程。不因为PSTACK里旧“图文不走PR”就阻止Fisher本次GitHub交接；本阶段仍仅本地，正式远端正常流程由主助手。
- tools/check_titles.py、measure_space.py主入口写死20261031旧批次，不能拿空跑PASS冒充Burry通过，更不能为过门改共享脚本。
- once_pipeline.sh主要支持03-design/p*.html与data.json/框架.md；Burry实际为cover/pages、02-框架.md，且本次只四图无完整正文，不适配就不硬造全PASS。使用本期evidence检查脚本与已存图像证据，不新造完整流水线回执。
''')
w('06-状态缺口与Mac归档.md','''
# 未完、阻塞、废弃与Mac归档状态

## 状态来源优先级
payload/project/STATE.md实读更新为2026-11-23 09:20 Asia/Shanghai，含Burry四图待审及11/23待选。payload/external/ops/xhs-tuwen/STATE.md是11/22旧状态，仍WAITING LPR，已滞后，不覆盖较新记录。其他老AGENTS、旧回执只按历史时点解释。

|项目|状态/缺口|Mac与发布证据层级|
|---|---|---|
|Burry 11/22|四图已做，待Fisher审阅；Getty权利未清；未完整正文|未发、未传Mac；本线程亲核本地实体，不能等同用户批准|
|LPR 11/22|四图成稿，孤字及脚注微修证据齐；旧回执哈希不再覆盖微修|较新STATE与切入证据均称未传Mac；待用户看图手动发|
|前10个月税收11/21|成稿待审，C06 FAIL保留，不能说全PASS|external/review/xhs/20261121-tax/mac_archive_verify.log记载10/10哈希一致；只读历史日志，未实时查Mac，未发布|
|青年失业率11/20|STATE称成稿待审；旧交接记载官方青年序列与C14双阻塞，保留矛盾/待核|没有据此宣称用户通过或已传Mac，接手需先核本期receipt与数据|
|创始人离职11/13|v8中列恢复已定原文；历史上下文记载t58u通过，t58回执实体保留|旧STATE记载9/9 SHA传Mac及v7备份，本轮未复查Mac；不是本次Burry模板|
|英伟达持股11/13|final_v2是Burry指定真实视觉底稿|历史上下文记载已传Mac，本轮只有实体/归档json，未查Mac实时状态|
|汽车出口/居民医保11/13|多版本成品、来源与归档实体全留|历史上下文记载已传Mac；医保审计目录保留；本轮未查Mac|
|存贷款11/14|成稿待审，C14历史FAIL；封面宽97.8%惯例告警与派生同步说明保留|交付文档写未覆盖Mac；旧STATE称等Mac恢复，不自动重试|
|扎克伯格控制权11/19|历史上下文v3.1四图待审；旧PASS不是用户批准|未取得新的传Mac/发布证据，不冒认已发布|
|Anthropic IPO11/20|历史上下文最新标签封面待反馈|未取得已发布/传Mac证据|
|台积电大客户11/19|用户已否决，作废素材与版本仍保留|不得自行恢复、换名重做或列为已批准|
|Sphere商单11/10|v7待反馈；完整源视频、录屏、音频、工程、脚本、许可说明均保留|不因留有demo等于商业验收或版权全清；禁止擅自接单/发布|
|11/11出口榜、11/12公积金/税种/个人养老金、10月底系列|实体历史见05索引及archive，不能仅凭“定稿”目录认定已发|本轮未逐项远端/用户电脑核查；完整原件保留供接手查证|

税收历史Mac路径：`/Users/donnie/Desktop/新图文笔记/阿信学财经/20261121_前10个月税收增速榜_待送审`。创始人v7旧备份历史为`_历史备份/20261113_创始人离职影响_待送审_t58前`。这些是历史证据线索，**不是本轮传输**。本轮未列机器、不操作Mac。

## 11/23三个待选题（不代选、不制作）
以payload/project/tmp/今日候选.md与选题库.md当日段为准，本线程未重新访问核实候选数据。
1. 大号：融资保证金下限100%→80%，拟按候选记载11/30实施；100万保证金理论100→125万，增25%；“近4000亿”是测算非已实现。
2. 大号：工行重夺A股市值第一；先统一A股股本×股价口径，不混H股总市值，重核11/20收盘数字。
3. 小号：创业板拟引入做市商，11/22征求意见，未实施。
其他11/22金价/外资、11/21社零/70城、11/20英伟达/互联网三季报等仍待选，以选题库原状态为准。

## 接手第一步
先读README→02当前任务与纠正→03核数/版权→04模板规则；看Burry最终四原图/总览与改前后图。Fisher本轮要的是完整GitHub接手，不是新内容制作。主助手完成远端正式更新并报告真实缺口后再按用户新指示推进；不要自动重启失败稿、选候选、发平台或传Mac。旧例程未在本轮停用或核实，需要交接双方协调，但不凭本说明自行更改。
''')
w('07-干净环境复现.md','''
# 干净环境复现（本轮未重渲染）

本包保留所有原始HTML/脚本，不改原稿里的绝对路径。`tools/reproduce_burry.py`提供**派生副本重定位+本地Chrome截图**；不运行研究/发布/原once_pipeline，不写回原稿。本轮只写此复现帮助程序并做语法检查，没有制作新图，也未在全新系统实跑，因此不能称已证明像素级干净环境复现。

## 依赖与字体
Linux、Python3、google-chrome或Chromium CLI；分析/对照脚本需Pillow、numpy、beautifulsoup4，部分历史采集脚本另需requests；可用venv安装，浏览器经系统官方包安装。参考快照实际版本：Python3.13.5；Google Chrome156.0.8078.47；Pillow13.0.0、numpy2.5.5、beautifulsoup4 4.15.0、requests2.34.2、fonttools4.65.0（记录环境，不保证新系统每个精确版本可安装）。

字体已实体携带于payload/dependencies/fonts：NotoSansSC-Black.otf（8855916B）、NotoSansSC-Medium.otf（8345436B）。嵌入元数据：©2014–2021 Adobe；SIL Open Font License1.1。OFL-and-copyright.txt保留本机发行版权与完整OFL条款；未更名或改造字体。原字体file:///home/box/.fonts路径由帮助程序替换，不依赖盒子目录。

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install Pillow numpy beautifulsoup4 requests fonttools
# 装好浏览器后，从本交接目录执行；默认只预览命令，明确加--render才渲染
python3 tools/reproduce_burry.py
python3 tools/reproduce_burry.py --render --chrome google-chrome
# 或 --chrome chromium；输出仅在reproduction/，不覆盖payload原始文件
```

每张原设计1080×1440、deviceScaleFactor2，输出2160×2880。等价命令：
`google-chrome --headless=new --no-sandbox --disable-gpu --allow-file-access-from-files --hide-scrollbars --force-device-scale-factor=2 --window-size=1080,1440 --virtual-time-budget=3000 --screenshot=<输出.png> file://<已重定位.html>`

原始evidence/render_and_check.py、make_review_images.py和旧期生成器有绝对路径。可在**副本**上按payload根重定位，不能不看路径直接跑后覆盖本地/其他项目。帮助程序只处理本Burry四张源HTML中/workspace/xhs与/home/box/.fonts资产路径；其他历史工程依赖路径见清单和源码，**未全部迁移/逐个复跑**。Sphere的视频等工程也未在干净环境重建；不可把“实体已完整快照”说成“所有历史工程均可一键复现”。

## 复现验收
先核本包SHA256SUMS与UPLOAD_MANIFEST；确认LFS文件非指针；看输出四张真实原图、400px缩略、与英伟达持股真模板并排。核头/下巴无切断、主副题间距、孤字/行首标点、底部留白、所有数字/日期/口径和Getty署名。不同Chrome/字体环境可能有抗锯齿差异；像素哈希不同时需视觉比较，不能仅空跑脚本说PASS。权利与内容批准独立于复现。
''')
w('08-安全范围与完整性说明.md','''
# 上传候选与安全/完整性边界

- UPLOAD_MANIFEST.tsv逐项给出实体相对路径、原始字节、SHA256、上传类别和来源映射；GitHub入库时`payload/`必须跟随，不能只传清单。
- project/完整保留notes、archive、商单（含大视频/工程）、tools、refs、gushouplus、topics、xiaohao_ref、tmp历史交付备份/当日候选及根文件。tmp并非全是运行缓存，因此未笼统排除。历史压缩包保留，ARCHIVE_CONTENTS.tsv列成员且可读文本做模式扫描。
- 本次handoff自身不递归进project快照，防无限复制；运行缓存、Git元数据、凭据命名文件/符号链接会排除并列原因。本机实际排除项与缺失项以SECURITY_FINDINGS.json为准，不编“全部已搬”。
- 外置仅本项目review、授权/机制准备包、项目收件箱、项目STATE/任务，以及历史回执工具四项和实际字体、poteto文档；不打包整个ops目录、其他项目或登录环境。
- **没有读取账户凭据、cookie、token、私钥或浏览器会话来认证；不包含账号登录状态。** 对普通业务文本与压缩包文本做常见PAT/API key/JWT/私钥/硬编码口令模式检查，仅记路径/类型/行号，不输出匹配值。命中候选暂不复制，清单标HOLD_SECURITY_REVIEW，须复核后再处理，不静默丢失。
- 模式检查不是取证认证：图片、PDF、音视频未OCR/逐帧隐私检查；参考素材与屏幕录制可能含姓名/界面等，需要受控私有保存和必要人工审视。不能因零文本命中宣称全包毫无敏感信息。嵌套压缩包不递归展开，远端历史ZIP未下载重扫。
- Getty授权未确认及其他历史媒体许可不足单独留档。扫描通过不表示版权通过、合规通过、用户审稿通过或可公开发布。
- >100MiB的两个视频不能普通Git直接提交；全部大文件和类别见LARGE_FILES.tsv，建议音视频LFS。当前本地完整实体保留，不因GitHub限制静默省略。若CloudAgent不支持搬运/LFS，应主助手明确报告缺口和替代存储决定，而不是假装已全量上传。
- GitHub旧资料不覆盖删除；旧文件中的路径、已失效状态/FAIL/回执都保留并由本次说明分层解释。
''')
(O/'README.md').write_text('''# 小红书图文完整交接 · 2026-11-23

**现状：Burry四图已制作待Fisher审阅，版权未清；当前暂停制作，准备交给其他AI。本目录是本地实体交接包，GitHub尚未更新。**

目标私有仓库：https://github.com/Fisher0012/xhs-graphic-handoff  
只读确认main：`06ad3ee5b098d7fae1741d8d30bef57bbb716c9f`，开放PR 0；原仓库是11/07文字交接，本次不覆盖旧资料。

## 接手顺序
1. [用户原意、历次纠正与Burry当前四图](docs/02-当前任务与用户纠正.md)
2. [事实、原文、核数与Getty版权风险](docs/03-事实来源与版权风险.md)
3. [长期规则、真正英伟达模板、PSTACK边界](docs/04-规则模板与机制.md)
4. [历史实体全索引](docs/05-历史实体索引.md) · [未完/阻塞/废弃/Mac归档/11月23日未选三题](docs/06-状态缺口与Mac归档.md)
5. [干净环境依赖与复现](docs/07-干净环境复现.md)
6. [仓库核实与主助手正式CloudAgent下一步](docs/01-仓库与上传操作边界.md) · [安全与上传完整性边界](docs/08-安全范围与完整性说明.md)

## 必带实体与可查证据
- [Burry四图](payload/project/notes/20261122-大号-Burry看空与减仓/final/)：00封面、01原先理由、02财报对照、03减仓观点；源HTML、完整长推、附图、历次框架、已否/新头像、来源/许可、视觉对照/证据均在该期目录。
- [真实英伟达持股模板](payload/project/notes/20261113-大号-英伟达持股/)，不是创始人离职/税种榜模板。
- [全项目资产](payload/project/) · [外置本项目审计/机制/任务](payload/external/) · [字体与许可](payload/dependencies/fonts/) · [poteto参考](payload/reference/poteto-mode/)
- `UPLOAD_MANIFEST.tsv`是完整上传候选逐文件清单（相对路径/体积/SHA/类别）；`INVENTORY_SUMMARY.json`汇总；`LARGE_FILES.tsv`大文件；`ARCHIVE_CONTENTS.tsv`历史包成员；`SNAPSHOT_VERIFICATION.json`本地快照逐哈希核对；`SECURITY_FINDINGS.json`扫描范围及限制；`SHA256SUMS`为整个本地交接目录的最终校验（不含自身）。

## 当前禁止事项
Fisher手动发布；不自动发布、不传Mac、不代选、不继续内容制作、不改例程/共享技能/其他项目。本阶段未clone/commit/push/发PR。主助手后续用正式CloudAgent做正常远端更新并回读核实；不能只给云端box路径，也不能把本地准备完成说成GitHub已更新。

用户批准≠文件已做≠门禁PASS≠Mac已传≠GitHub已同步。Getty再使用许可未确认；媒体转述交易细节不能冒充已读取付费一手正文。全部原始资料保留，无删除历史许可。

更新时间见INVENTORY_SUMMARY.json（Asia/Shanghai）；整理者：Grok Bot executor，仅本地交接。
''')
(O/'STATE.md').write_text('更新：'+datetime.now().astimezone().isoformat()+' Asia/Shanghai\n状态：HANDOFF_LOCAL_ONLY，未更新GitHub，内容制作暂停\n下一项：主助手正式CloudAgent按清单增量入库并回读SHA，保留版权/媒体安全/大文件限制\n')
print('WROTE_DOCS',len(list(D.glob('*.md'))))
