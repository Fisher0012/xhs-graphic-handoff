# 小红书图文完整交接 · 2026-11-23

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
- `TRANSFER_MANIFEST.tsv`列整个交接目录候选实体；它自身及SHA256SUMS也须上传。`UPLOAD_MANIFEST.tsv`是payload上传候选逐文件清单（相对路径/体积/SHA/类别）；`INVENTORY_SUMMARY.json`汇总；`LARGE_FILES.tsv`大文件；`ARCHIVE_CONTENTS.tsv`历史包成员；`SNAPSHOT_VERIFICATION.json`本地快照逐哈希核对；`SECURITY_FINDINGS.json`扫描范围及限制；`SHA256SUMS`为整个本地交接目录的最终校验（不含自身）。

## 当前禁止事项
Fisher手动发布；不自动发布、不传Mac、不代选、不继续内容制作、不改例程/共享技能/其他项目。本阶段未clone/commit/push/发PR。主助手后续用正式CloudAgent做正常远端更新并回读核实；不能只给云端box路径，也不能把本地准备完成说成GitHub已更新。

用户批准≠文件已做≠门禁PASS≠Mac已传≠GitHub已同步。Getty再使用许可未确认；媒体转述交易细节不能冒充已读取付费一手正文。全部原始资料保留，无删除历史许可。

更新时间见INVENTORY_SUMMARY.json（Asia/Shanghai）；整理者：Grok Bot executor，仅本地交接。

本轮扫描：3份历史网页发现JWT/API-key样式，已只对归档副本脱敏（原件不入包），见SANITIZED_FILES.tsv；其余3039份原样保留。3042份payload实体SHA复核一致。音视频/图片未逐帧隐私审查，版权限制不变。
