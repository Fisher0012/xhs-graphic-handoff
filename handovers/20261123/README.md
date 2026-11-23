# 2026-11-23 完整交接已在本仓库

克隆这个分支之后，先重建大于 50 MiB 的媒体，再做完整校验：

```bash
python3 handovers/20261123/reconstruct_media.py
```

脚本会把 7 个原始视频无损写回 `完整交接/` 里的原路径，并在该目录执行 `sha256sum -c SHA256SUMS`。通过标准是 **3071 项全部 OK、0 项 FAILED**。重建后的交接目录应为 **3072 个文件、2,618,814,122 字节**。冻结校验文件 `完整交接/SHA256SUMS` 的 SHA256 是 `e15c342f97ce480aef0c5ad69144752ca0cd4ac13a9db99bf4dc0ee15fda38a6`。

图片、HTML、来源、英伟达持股真模板、字体，以及所有不超过 50 MiB 的文件已经直接在 `完整交接/` 里，不需要等重建就能读。Burry 四图在 `完整交接/payload/project/notes/20261122-大号-Burry看空与减仓/final/`。真模板在 `完整交接/payload/project/notes/20261113-大号-英伟达持股/`。

## 当前同步事实

这条说明写在冻结快照外面。`完整交接/` 内部的 README、STATE 和 docs 保持 2026-11-23 冻结原文，其中「GitHub尚未更新」「本阶段未 clone/commit/push」描述的是打包当时，不是本仓库现在的状态。

本分支在 `06ad3ee5b098d7fae1741d8d30bef57bbb716c9f` 之上追加交接，不覆盖、不删除 2026-11-07 的 `handoff/` 与 `archive/`。没有使用 Git LFS。账号剩余 LFS 额度和预算接口当时无法读取，不能排除超出免费额度后的计费，所以没有启用 LFS，也没有购买存储。大于 100 MiB 的两个视频不能作为单个 Git 对象提交；大于 50 MiB 的媒体全部改成原始字节分片，避免 GitHub 的 100 MiB 拒绝和 50 MiB 警告。

分片在 `storage/shards/`，清单在 `storage/SHARD_MANIFEST.json`。每片严格小于 45 MiB（实现上限 44 MiB，即 46,137,344 字节）。拼接顺序、原始相对路径、原始字节数、原始 SHA256、每片字节数和每片 SHA256 都在清单里。分片是无损切段，没有压缩包装；Git 传输时自身的包压缩和相同内容去重仍然有效。7 个原始路径都保留，重复出现的历史路径也没有从树上删掉。

| 原始路径 | 字节 | SHA256 | 片数 |
| --- | ---: | --- | ---: |
| `payload/project/商单/20261110-Sphere/rec/raw_A.mp4` | 108047615 | `a18a5220c498796323dd07f85d7ca34f442d3198d00062dcdcc7000223179668` | 3 |
| `payload/project/商单/20261110-Sphere/rec/raw_B_gen.mp4` | 84892405 | `e60aa71d43ae7c1896295af895f0893050cf467ce0f94e6991de2f800d046e30` | 2 |
| `payload/project/商单/20261110-Sphere/refs2/beida.mp4` | 69434643 | `d3c4325128d5b062886e1a0505075df94016e6fc53c72c7172a1d802833c2eb4` | 2 |
| `payload/project/商单/20261110-Sphere/refs2/meidui.mp4` | 101001322 | `aadbef4714b4295e1c7b592a835761d6e54d17f3d786038a47651cfcbcc4a4c4` | 3 |
| `payload/project/商单/20261110-Sphere/refs2/wb.mp4` | 81329684 | `5eaa2899b83bad22f3148927e3b7ac26de8bd7080fdc38302140ea12bf1474e9` | 2 |
| `payload/project/商单/20261110-Sphere/refs2/wbsys.mp4` | 75706936 | `4a0d7e0a7381c0af3f644ebaa61b22c0a12cc898b53f21dee9eeaacb7087347c` | 2 |
| `payload/project/商单/20261110-Sphere/refs2/yuri.mp4` | 133687596 | `4ae3aca2ac61508b94be171a9102a76c8a08fb8d167e94dec40e1366caf5c302` | 3 |

这 7 个文件合计 654,100,201 字节、17 片。快照内的 `docs/08` 仍写着音视频建议走 LFS；那是冻结时的建议。本次交付的替代是上述分片，字节没有改成一份清单。

## 接手时必须单独记住的状态

细节和其余期次见 [STATUS.md](STATUS.md)，以及快照内 [docs/02](完整交接/docs/02-当前任务与用户纠正.md)、[docs/03](完整交接/docs/03-事实来源与版权风险.md)、[docs/04](完整交接/docs/04-规则模板与机制.md)、[docs/06](完整交接/docs/06-状态缺口与Mac归档.md)。

- Getty 头像再使用许可没有确认。`burry_front_astrid_getty.jpg` 是 Astrid Stawiarz / Getty Images，编号 498541178，不是 CC。私有留档不是许可，也不能当成已经发布。
- Burry 四图已制作，等待 Fisher 审阅。成图不是用户批准，没有发布，没有传到 Mac。
- 2026-11-23 的三个候选没有选定，也不要代选或开工。
- 没有启用 LFS，没有合并到 `main`，没有改冻结快照里的文件内容。
