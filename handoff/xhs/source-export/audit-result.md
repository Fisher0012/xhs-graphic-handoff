# 受限材料核验与交付准备
日期：2026-11-07 Asia/Shanghai；仅复用source-export原37文件，未财经复研或制图。

## 六类核查
|材料|结论|现有证据|
|项目目标|齐|README.md、evidence/02_AGENTS.md|
|大小号风格|齐|rules-current.md黑金尺寸色值；memory-available.md排版段含小号墨绿近黑/白青绿样式|
|重要历史经验|齐|memory-available.md、evidence/03_LESSONS.md、evidence/04_复盘.md，保留新旧规则来源|
|资产清单|齐（仅清单，不携大资产）|path-inventory.json、dependencies-and-paths.md|
|当前待办|齐|tasks-and-evidence.md、README.md：新五题待选，旧三题否决|
|接手提示词|原缺独立可直接使用文本，已补|HANDOFF_PROMPT.md，只读接手，不触发生产/例程|

## 基线、脱敏、校验
- 修改前实际37文件；原SHA256SUMS的36条逐项核验全部通过。原清单SHA256：7bd154a8dd94ba5b0a938504116f312af53810c46b32a3207aa4b49da2281b2e。
- 基线原文保留BASELINE-37-SHA256SUMS.txt，原37项独立散列记录baseline-37-result.json；manifest与当前SHA256SUMS更新不抹除基线。
- 对导出所有文本检查私钥、常见token值、password/access_token/refresh_token/cookie赋值、邮箱、内地手机号码模式，未命中；未添加原始profile或读取凭据。机器ID、个人本机路径、公开号标识属于接手定位信息非认证秘密，保留且不作为在线/授权证据。模式扫描不能保证所有未知格式秘密均已识别。
- 原业务材料不重写，只补接手提示词、文件清单、核验报告和基线凭证，刷新manifest与SHA256SUMS；无大资产复制。
- 当前manifest逐文件hash与SHA256SUMS逐项校验；ZIP以source-export/为单一前缀，仅收导出文件，不含ZIP自身；zipfile完整性测试、包内SHA256SUMS及manifest文件散列全过。ZIP自身SHA256由最终工具结果提供，避免自引用。
- 本次用户明确要求ZIP交接包装，仅此次覆盖旧成稿不zip规则，不改变日常生产存档规范。

## GitHub目标线索（不猜仓库）
限定读取迁移项目小.md/.json以及同一bot-rebuild根小入口，未找到明确私有GitHub URL+本项目路径。根入口无相关小文件线索。ARCHIVE-STATUS.md第16行、ARCHIVE-MANIFEST.json的缺口均记私有GitHub文字仓库未创建/未上传。未用ETF工具URL冒充仓库，未读取任何凭据，未写远端、未启动CloudAgent。父bot如掌握新增明确目标另核；本报告不能证明当前已远端备份或远端读回。

## 现有重建验证bot：身份未核实，文件报告为有限验证
只提取/home/box/agent-data/agents/*/profile.json中id/name/title/description身份字段，当前24份profile未发现准确显示名「xhs 图文创作·重建验证」。不能猜id或把原bot当新bot；原bot28ab212d-7512-4d34-9e90-4ad338c81595显示名「xhs 图文创作」，不是目标身份。
可见报告：/workspace/ops/bot-rebuild/xhs-20261107/new-bot/VALIDATION-RESULT.md（20:14 Asia/Shanghai）报有限只读核验：文件齐、6文件hash仅比较前16位、仅目视封面和01内页、02/03未看、核心算术复算，未回核网页或重跑标题/空间脚本，未加载全部专项技能；报告明确不是全面验收。报告未提供可核实新bot身份，不据此宣称目标bot完整验证通过。本轮只读这份报告，没有重做生产验收。

## 真实边界
非全量历史/记忆/例程；仅编号5可见，原get仍enabled，并非本轮实时重查或已冻结。新旧防重复由获授权迁移方控制。研究结束、父bot没有其他已知生产任务不等于全系统无后台。新五题仍待选；无发布、无重建、无新权限授权；本包准备不等于已经迁移。Mac未在线核验、发布未知、ORICO未验完整、连接器未实时鉴权；遗留待对账。未联系其他bot，未更改生产、例程或权限。
