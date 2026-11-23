# 工程门禁 ADR-EG1：各项目专属检查（2026-11-10 14:35 起全项目执行）

> 依据：各项目根目录 AGENTS.md / STATE.md 和本机目录实查（2026-11-10 14:40 上海时间）。查不到的写 unknown，不编。
> 通用门（所有项目都要过）：回执 receipt.json 能被
> `python3 /workspace/ops/eng_gate/verify_receipt.py <receipt.json> --project-root <项目根> --baseline <总协调基线>` 重跑通过（退出码 0）。
> 下表是在通用门之外，每个项目另加的检查。写进回执的方式：能用命令跑的放进 `gates.gate2_invariants_and_tests.command`（argv 列表，box 上可执行）；要保护的文件由总协调放进基线；其余写进回执 `project_checks` 字段（逐条 PASS/FAIL + 证据路径）。

| 项目 | 收件名（post.sh） | 项目根（--project-root） | 已知产物/代码位置 | 默认档 |
|---|---|---|---|---|
| Foundation | foundation（复核：foundation 内部独立复核，2026-11-13 t101u 起；原 Foundation复核官 81c47d91 不再收送审） | /workspace/foundation（状态）；代码 worktree 以 PR 为准，box 上已知 /workspace/review/repo、/workspace/fnd-takeover/repo | GitHub Fisher0012/financial-intelligence-foundation；Mac /Volumes/FNDWORK/wt；原始数据 /Volumes/ORICO/fnd/raw | T0/T1；写服务器 T2；数据迁移 T3 |
| 小财看涨跌 | 小财看涨跌 | /workspace/xiaocai-kanzhangdie | scenarios.md、eval/eval_set.jsonl、eval/README.md；代码仓库 unknown（等 Codex 资料） | T0；上线 T4 |
| A股技术分析 | A股技术分析 | /workspace/a-share-ta | m3src/（Makefile 有 check 目标）、workbench/；仓库 cursor.com/codebase/fisher-s/a-share-ta；Mac ~/ta-supervise | T0/T1（11-06 起 Fisher 暂停推进） |
| 财经视频 | 财经视频搬运加工（大小号） | /workspace/video-slice | 代码 video-slice-code（git，GitHub Fisher0012/video-slice-mvp）；批次 batch6-20261106/；成片 ORICO /Volumes/ORICO/视频成片/财经视频搬运/ | 内容类 C；改码 T0；发布 T4 |
| 小红书图文 | xhs 图文创作 | /workspace/xhs | notes/<日期>-<名>/final/、交付.md、送审摘要.md；tools/check_titles.py、measure_space.py、compliance_precheck.py | 内容类 C；发布 T4（大号仅 Fisher 手动） |
| 技能变现 | 技能变现 | /workspace/skill-monetization | compliance-check/package/、renovation-quote/dist/*.zip、absolute-terms/tests/check_v103.py、renovation-quote/tests/prep_submit_v102.py | T0；提交/改上架 T4 |
| IGTrack | igtrack | /workspace/ig-publish（状态、证据）；代码以 PR worktree 为准，box 已知副本 /workspace/mmfix5-20261026/repo、/workspace/igb1-baseline-20261029/repo | GitHub Fisher0012/igtrack；服务器 /opt/igtrack（pm2 igtrack-web、igtrack-scheduler）；爬虫机 /opt/igtrack-fetcher；验收证据 /workspace/review/igtrack/ | 服务器补丁 T2；写库 T3；上线/支付/群发 T4 |
| seeworld | seeworld | /workspace/seeworld | scripts/（preflight_daily.sh、make_deliver_dir.py、check_orico_prefix.sh、pool_low_alert.sh、testdata/）；Mac 项目根 /Volumes/ORICO/project_data/seeworld_project | 内容类 C；改脚本 T0；发布 T4 |
| app 开发工程师 | app开发工程师 | /workspace/app-dev | 归档包 /workspace/fasttimer-handoff-20261107；GitHub Fisher0012/FastTimer（main 0c15a32）；CI = GitHub Actions ci.yml / testflight.yml | T0；提审/TestFlight/花钱 T4（11-06 起暂停） |

## 各项目专属检查

### Foundation（foundation；2026-11-13 t101u 起由 foundation 内部独立复核代理担任红队和数据裁决，按共享技能「foundation内置独立复核」；原复核官 81c47d91 已不收送审）
- F1 本 PR 相关 pytest 用例写进 gate2.command，必须 0 失败；另附全量 pytest 对比，失败集合与基线「4 failed / 89 errors」逐项一致，不得新增。
- F2 `gate4_evidence.git_repo` 指向本 PR 的 worktree，`git status` 干净；`environment.git_commit` 写 PR head（≥8 位），与送审标题一致。
- F3 数据产物（快照、日线等）登记 ASSET_REGISTER：路径、行数、SHA-256、恢复方案；写服务器按 T2（只在 Staging 演练），数据迁移按 T3（副本上演练恢复）。
- F4 gitleaks 0 发现；/workspace/ops/tasks/foundation.json 第 860 行疑似密钥须在 11-12 18:00 前清掉（已有待办）。
- 注意：代码多在 Mac（/Volumes/FNDWORK）跑。回执里的路径必须是 box 上能读的路径，否则总协调无法重算 → 判 FAIL。Mac 产物怎么同步到 box：unknown，需 foundation 在第一份回执里写明。

### 小财看涨跌
- X1 评测成绩单：越界 0、编数字 0、事实准确率 ≥90%、格式完整率 ≥95%（按 eval/README.md）。打分脚本写进 gate2.command；打分脚本目前不存在（unknown），建第一版时一并交测试。
- X2 eval/eval_set.jsonl 条数守恒（现 47 条；增删要在回执说明），eval/ 和 scenarios.md 列入项目 MANIFEST.sha256。
- X3 不变量用例：每条解读六段齐全，每个数字有出处或写「未查到」；至少 1 个反向用例（含荐股/目标价的输入必须被拒）。

### A股技术分析（当前 Fisher 暂停推进，恢复后的第一次交付起执行）
- A1 gate2.command = `make check`（cwd 为 m3src 或对应 worktree），必须全绿。
- A2 gitleaks 0 发现，原始输出存档并写进回执。
- A3 回测不变量：无未来函数（反向用例：打乱/截断未来数据，历史信号不变）、无补值；样本数和数据缺口写进 project_checks。
- A4 不碰 Foundation 路径（~/projects/financial-intelligence-foundation、/opt/foundation-*）：targets 越出项目根即 C15 判 FAIL。

### 财经视频（财经视频搬运加工（大小号））
- V1 产物门（内容类 C）：每条成片 ffprobe 读分辨率、时长、音轨，文件非空，SHA-256 入 ASSET_REGISTER；ffprobe 检查命令写进 gate2.command。
- V2 抽帧核对：标题、字幕、底部安全区互不重叠；标题里的数字是本人原话（对照字幕）；帧图路径写进 project_checks。
- V3 改 video-slice-code 按 T0：`gate4_evidence.git_repo=/workspace/video-slice/video-slice-code` 要求 git 干净。现状 head ac19f92、未提交改动 4 项，下次改码前先收口（不要求返工旧件）。
- V4 发布按 T4：核对账号 ID，绝不发「娱乐看世界」；成片发布后拷 ORICO 并核对文件数和大小。

### 小红书图文（xhs 图文创作）
- H1 黑金系列：gate2.command 跑 /workspace/xhs/tools/check_titles.py 和 measure_space.py（技能 skill-1793452849757），退出码 0。
- H2 合规门：/workspace/xhs/tools/compliance_precheck.py 退出码 0（对应合规自查技能 skill-1792678316447）。
- H3 内容不变量：条目数和标题一致；数据日期不晚于发布日期；每个数字可追溯到一手出处（交付.md 出处表）。
- H4 final/ 成品哈希入 ASSET_REGISTER；大号只由 Fisher 手动发，回执不得包含任何发布动作。

### 技能变现
- S1 离线测试写进 gate2.command：如 `python3 renovation-quote/tests/prep_submit_v102.py`（现 19/19）、`python3 absolute-terms/tests/check_v103.py`（现 21/21），退出码 0。
- S2 zip 与 package 目录逐文件一致（zip≡package），zip 的 SHA-256 入 ASSET_REGISTER。
- S3 规则文件和免责声明不许动：由总协调放进基线，C14 校验哈希不变。
- S4 提交审核、改已上架内容按 T4，回执附 Fisher 批准出处（approval_ref）。

### IGTrack（igtrack）
- I1 服务器补丁一律 T2：Staging 演练、附 rollback_plan 文件，记录部署前后 DEPLOYED_SHA 和改动文件 SHA-256；禁止整仓部署（服务器 DO-NOT-FULL-DEPLOY.md；PR#32 只留存）。
- I2 产品四项分别给运行证据：抓取、订阅推送（含无声门禁 SKIPPED_SILENT）、付费、链接解析；能跑的测试或只读探针写进 gate2.command，跑不了的写 unknown，不得当 PASS。
- I3 fetcher 测试：现有 9 个旧失败作为已知基线列出，不得新增失败。
- I4 写库按 T3、上线/支付/删除/群发按 T4，须 Fisher 当次原话（approval_ref）。
- 注意：服务器文件 verify_receipt.py 在 box 上无法直接重算；T2 回执需附从服务器只读拉回的哈希清单。fetcher SSH 目前被拒（STATE 11-08），该部分 unknown。

### seeworld
- W1 产物门（内容类 C）：subcheck、tck、QC 全部通过。这三个脚本在 Mac 项目根，box 上的路径 unknown；回执的 gate2.command 必须是 box 上能跑的命令，跑不了则判 FAIL——需 seeworld 在第一份回执前说明在 box 上怎么跑。
- W2 不变量：md 标题、封面标题、视频标题三者一致；字幕中英各 ≤2 行。
- W3 去重登记 _known_ids.json 已写入（作为 target 交前后哈希）。
- W4 改 /workspace/seeworld/scripts 按 T0：附 testdata 下的正反用例；`scripts/preflight_daily.sh` 退出码语义（0 全净 / 1 有告警）不得改。

### app 开发工程师（当前暂停归档，恢复后的第一次交付起执行）
- P1 CI 证据：回执附 GitHub Actions run id，gate2.command 用只读 `gh run view <id> --json conclusion` 核对为 success（box 上 gh 是否已登录该仓库：unknown）。
- P2 密钥不入仓：gitleaks 0 发现。
- P3 提交审核、TestFlight 外测、花钱、下架按 T4，附 Fisher 批准出处。

## 共用审查官（4e343c3b）——红队
- 对 T0/T1 大档、T2、T3（Foundation 除外）写 3~5 个可执行恶意用例，放 `/workspace/review/<项目>/<任务>/redteam/`，每个用例是可直接运行的脚本或 pytest 文件，退出码 0=被拦住（期望行为）。
- 不写评语长文；结论只有 PASS，或 FAIL 加必修清单（每条附实证）。用例由总协调用 verify_receipt.py 和用例脚本重跑。
- 每次计入每周 25 次普通审查上限。
