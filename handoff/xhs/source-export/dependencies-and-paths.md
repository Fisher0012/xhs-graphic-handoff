# 业务依赖与路径
## 七项业务技能（只列依赖，不修改/复制整份profile）
- skill-1792678166250：财经图文总流程
- skill-1792678206639：选题
- skill-1792678236073：框架
- skill-1792678262793：设计出图
- skill-1792678283860：标题正文话题
- skill-1792678316447：金融内容合规
- skill-1793452849757：黑金硬规则自查
另用：skill-1792368754818纠错复盘；skill-1792368762410经验入库；skill-1792368769729交接；skill-1792368748998周复盘（目录显示实际ID为skill-1792368748998，如父bot目录不同请核对）；skill-1793884039177完成证据。共享技能仅Dido经批准写，本轮未改。
## 工具
/workspace/xhs/tools/once_pipeline.sh → render_heijin.sh → compliance_precheck.py → gate_archive.sh；topic_candidates.py、dedup_topics.py；check_titles.py、measure_space.py、xhlib.py；共用 /workspace/xhs/notes/heijin.py、cover_gen.py。导出只带必要小脚本快照；未执行生产。渲染依赖google-chrome、bash、Python3，网页与HTML为主，Canva可选；未安装/版本检查。
## 连接器：目录可见≠实时已授权
旧自查2026-11-05仅历史证据：Canva备用保留；Gmail/Outlook/X/Figma/Finance非日常核心；GitHub/Origin偶发待裁。本轮可见目录含user-Canva、user-Figma、Gmail两项、user-X-8067074、x、cursor-github、cursor-origin；未进行实时鉴权、不读账号密钥。公开网页读取是核心，X偶用需相应技能。新bot若用Canva/X/GitHub/Origin，需由用户确认重新授权，不能复制token/cookies。发布授权归发布方管理。
## 路径
项目根 /workspace/xhs/；STATE/AGENTS/LESSONS/复盘/选题库；tools/；notes/；archive/；tmp/20261107_重选候选.md；tmp/reselect_sources/（本轮仅已知路径，不重翻网页大文件）。
ETF根 /workspace/xhs/notes/20261106-大号-宽基ETF吸金榜/；review /workspace/review/xhs/20261106-大号-宽基ETF吸金榜/review-result.md。
11-02目录前缀 /workspace/xhs/notes/20261102-大号-（产油国/进口商品/券商净利/资管公司）；11-01小号目录见path-inventory与源notes目录，不遍历历史内容。
附件根 /cursor/stores/store-3c6cbb4d-9944-4f4d-a913-936a73491132/grok-bot/agents/28ab212d-7512-4d34-9e90-4ad338c81595/attachments/，只列直接目录项与大小，不复制大图。
Mac已知 /Users/donnie/Desktop/新图文笔记/阿信学财经/ 与 /Users/donnie/Desktop/新图文笔记/阿信财读笔记/；machineId 1955f62c-ee17-45e0-9e5b-3d70dff2b5c5；本轮未访问、未验证在线，复制需批准。
通知依赖 /workspace/ops/comm/post.sh（仅已知，未读取/执行；父bot通知前先Read核用法）；任务清单路径仅AGENTS引用未读取，不当实时事实。
