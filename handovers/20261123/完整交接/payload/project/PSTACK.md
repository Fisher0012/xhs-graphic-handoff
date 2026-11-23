# 小红书图文项目 pstack 生效记录

生效时间：2026-11-22 11:34（北京时间）。Fisher 在 Dido 会话 t151u 决定「现在应用到小红书图文」（此前 t136u 已定采用原机制，当时仅延后）。本项目自本轮约 11:36（北京时间）起按 pstack 原机制执行。

授权范围：仅 `/workspace/xhs` 项目与本项目工作方式。不改共享技能、全局模型配置、例程或其他项目。不运行全局 `/setup-pstack`。不发布、不传 Mac、不登录。

## 当前任务完成谓词（LPR 孤字微修）

任务：保留已有 LPR 成稿，修 01 第②段孤字「它。」、02 规则段孤字「期。」，核四页其他段落和脚注无 1–2 字孤行，核实图 01 脚注「〔2019〕第16号」，同步文案，重渲并更新总览 / SHA / 归档校验。不发布、不传 Mac。

谓词（全部满足才算本微修技术完成；技术通过不等于 Fisher 已审阅）：

1. 亲看修改后 2160×2880 原图：01 第②段、02 规则段不再以 1–2 字（含标点）收尾；四页其余正文和脚注同样没有 1–2 字孤行。
2. 改前改后并排对比与像素差分：改动限于上述文案与 01 脚注；封面和 03 在文案未改时应保持一致或仅有渲染抖动；未改字号，未改版式 CSS / 模板。
3. 第 16 号核实结论已落实：留档为央行公告〔2019〕第16号（2019-08-25，新发放住房贷款利率，LPR 改革过程中的房贷定价文件，不是 LPR 形成机制本身）；现行「加点可为负、固定利率合同期不变」以〔2024〕第11号为依据（第11号同时废止第16号），01 脚注改为已核实的第11号。
4. 发布文案中同一句已同步；字数仍不超过 1000。
5. H1：本期 `verify_content.py`（内含标题与留白检查）退出码 0；`measure_space.py` 内页最大连续空白 ≤8%。
6. H2：`compliance_precheck.py --dir` 退出码 0。
7. `once_pipeline.sh` 渲染与合规、定稿门禁通过；final 中 SHA256 与文件一致。
8. 数字仍以央行一手原文为准；本微修不改任何官方数字。

不再作为本项目新门：`verify_receipt.py` 额外签核、送审查官、每阶段两轮限制。旧回执可保留为历史证据；不伪称取消历史 FAIL（税收篇 C06 FAIL 仍在 `/workspace/review/xhs/20261121-tax/`）。不必为新机制重生产回执。

## 冲突替代

按 `/workspace/ops/dido/pstack_xhs/冲突对照表.md` 执行。切入后按 pstack 取代的条目：#3 审查官与两轮送审、#7 自建续推模型例程（但本宿主未见 `/loop`，不承诺也不新建）、#9 换模型须当场报批（本宿主无法按角色指定模型，见下）、#10 失败两次停手提问、#11 复述后等人确认、#13 中 verify_receipt 额外签核（H1/H2 仍是完成谓词）、#14 总览送审查官、#16 例行逐步确认、#19 五步固定顺序、#20 送审计数、#21 自定升级白名单、#22 Cloud Agent 机制冲突条款（本轮不开 Cloud Agent）。

保留且兼容：STATE 三行头、完成证据、黑金硬规则 1–8、数字真实与亲看图、Fisher 本人手动发布、Mac 传输须另有授权、平台安全审批。

## 真实工具限制（不得声称已完整生效）

1. 本宿主 Task 仅支持 executor 等公开类型，不暴露 `model` 或 `run_in_background` 字段，没有 `poteto-agent`，不能按角色指定或混用跨厂商模型。
2. 因此完整模型栈、跨模型审计、interrogate 面板、Cursor `/loop` 均未在本环境落地，不能声称已经生效。show-me-your-work 要求的「另一厂商模型审 trail」本次无法派出，不编造评审意见。
3. poteto-mode 技能目录在文档中为 `/home/box/agent-data/plugins/pstack/pstack/skills/poteto-mode/`，该路径在本机不存在。本轮实际读取的是 cache 副本：`/home/box/agent-data/plugins/cache/cursor-public/pstack/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/skills/poteto-mode/`（含 `worker.md` 与 playbooks）。
4. 未运行全局 `/setup-pstack`，没有可用的 `~/.cursor/rules/pstack-models.mdc`。
5. 图文成品不走 PR；本任务不执行 Opening a PR。`/workspace/xhs` 即使存在 git 元数据，也不为这次微修建 PR 或改共享工具。
6. 发布与 Mac 传输未恢复。

## 日志与证据

- 决策日志：`/workspace/xhs/decisions.tsv`
- 切入证据汇总：`/workspace/xhs/pstack/20261122-切入证据.md`
- 本任务改前快照：`/workspace/review/xhs/20261122-lpr/before_fix/`
- 准备包与授权：`/workspace/ops/dido/pstack_xhs/`，`/workspace/ops/comm/materials/pstack_xhs_start_20261122/切入授权与任务.md`
