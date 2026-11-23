# 小红书图文创作交接入口

**最新入口是 2026-11-23 完整交接，已经写入本仓库：** [handovers/20261123/README.md](handovers/20261123/README.md)。克隆后先运行 `python3 handovers/20261123/reconstruct_media.py`，再按冻结 `SHA256SUMS` 验收。快照文件 `handovers/20261123/完整交接/README.md` 里的「GitHub尚未更新」是 11 月 23 日打包当时的原文，不是仓库现在的状态。Getty 再使用许可未确认；Burry 四图待审；未发布；未传 Mac；11 月 23 日三个候选未选。

本仓库保存 2026-11-07 从 Grok Bot「xhs 图文创作」导出的受限业务交接包。

- [开始接手](handoff/xhs/START_HERE.md)
- [新机器人提示词](handoff/xhs/NEXT_BOT_PROMPT.md)
- [当前规则](handoff/xhs/source-export/rules-current.md)
- [任务与证据](handoff/xhs/source-export/tasks-and-evidence.md)
- [资产定位清单](handoff/xhs/source-export/path-inventory.json)
- [缺口](handoff/xhs/source-export/gaps.md)
- [原始导出 ZIP](archive/xhs-source-export-handoff-20261107.zip)

## 已验证与未验证
已验证本机 ZIP 散列、42 个普通文件无符号链接、SHA256SUMS 41 项逐项匹配；常见密钥模式未命中。导出包含目标、风格、历史经验、资产清单、当前任务与提示词。

这是核心文字资料备份，不是全量项目或历史资产备份，不构成永久删除许可。未复制大图或外部技能正文，未核实全量历史、其他例程、Mac 全量存档、发布状态或连接器；旧例程仍可能运行。旧机器人和原资料保留。未改生产、例程、凭据或权限。

原 ZIP SHA256：`6cdc868ed81432491212c8f8d7c89f25d1b87cf56905cceaf535da4dcd3ec134`。

## 新机器人验证

「小红书图文 接手验证 1107」已在固定提交 2e48686076e62f8102208cc75e23224eb178867f 完成五份核心文件的最简文字理解验证。[查看验证回执](handoff/xhs/READBACK_VERIFICATION.md)。这不改变上述未迁移范围和禁止删除结论。

## 2026-11-23 完整交接

11 月 7 日的文字包仍然保留在 `handoff/` 和 `archive/`。2026-11-23 的全量交接追加在 [handovers/20261123/README.md](handovers/20261123/README.md)，状态摘要在 [handovers/20261123/STATUS.md](handovers/20261123/STATUS.md)，冻结实体在 `handovers/20261123/完整交接/`。

- 冻结 `SHA256SUMS` 文件摘要：`e15c342f97ce480aef0c5ad69144752ca0cd4ac13a9db99bf4dc0ee15fda38a6`
- 重建后的验收：3072 个文件，2,618,814,122 字节，`sha256sum -c SHA256SUMS` 为 3071 项 OK
- 大于 50 MiB 的 7 个视频按原始字节切成小于 45 MiB 的分片，放在 `handovers/20261123/storage/shards/`。没有使用 Git LFS
- 这次更新从 `06ad3ee5b098d7fae1741d8d30bef57bbb716c9f` 另起分支，不合并、不改写已有历史

