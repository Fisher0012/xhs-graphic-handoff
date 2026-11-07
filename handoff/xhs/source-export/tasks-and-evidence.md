# 当前任务、验收与证据
## 当前真实状态（本次父会话优先）
1. 11-07原三题：金饰消费/互换便利/创业板权重，全部被否，禁止按STATE旧候选开工。
2. 新五题已交付，t79s575待选：行业工资、消费结构、幼儿园与大学、结婚登记、侨汇。详细两条事实/来源/统计期/口径/风险见evidence内重选文件和选题库近期段。研究已结束；候选合格不代表前十每行成稿数据验收完成。
3. 11-06宽基ETF：交付.md、送审摘要.md、合规、pipeline、final归档校验、review-result.md已核文件存在。审查结果11-06 11:41 Asia/Shanghai通过，曾提示原话出处不足、封面宽87.1%；交付更新11:43记已收标题116/字距2并补选定原话。Mac存档为文件记录，本轮未远程复核；用户手动发布未知。
4. B5已落地：指定回执 /workspace/ops/usage/回执_xhs_一次成稿接线_20261106.md（14:31批）；上午关联版 /workspace/ops/usage/回执_xhs一次成稿接线_20261106.md（11:00批），不可混同。试跑日志evidence_xhs_20261106_b5_once_pipeline.txt为历史证据，本轮未重跑生产。
5. 11-02大号产油国/进口商品/券商净利/资管公司四框架待确认，不自动执行。
6. 11-01小号胡润/A股利润/省收入/人均GDP为遗留待对账，历史状态未核定，不自动列新任务。
## 运行与待人项
父bot没有其他已知运行生产任务，研究已结束，本导出是当前唯一已知运行工作；未做全系统后台扫描，不声称系统无后台。原bot例程5仍enabled，不等于冻结；新旧重复由迁移方获授权后处理。等Fisher选新5题后才进入一次成稿。
## 未来一次成稿验收
核齐逐行原值、统计期样本/估算边界、自算标注；HTML渲染并逐张看图；合规与黑金门禁；审查通过才存档。无具体产品推荐收益承诺，不大号代发。4图优先，来源文案校验齐，Mac归档需在线和复制批准。
## 可跑命令（仅记录，本轮未执行）
python3 /workspace/xhs/tools/topic_candidates.py
bash /workspace/xhs/tools/once_pipeline.sh --note-dir /workspace/xhs/notes/<期目录>
bash /workspace/xhs/tools/once_pipeline.sh --note-dir /workspace/xhs/notes/<期目录> --skip-render
脚本只编排已有数据/HTML：无HTML会WARN，notes无final用宽松检查，PASS不等于完整成稿，不能替代核数/视觉/黑金审核。
## 本导出验收
必需文档、源路径存在性/大小、必要小证据、附件仅清单、SHA256；例程5完整七步prompt已由父bot从实时get补齐；记忆已补当前上下文与Recall检索业务事实，非全量历史。其他真实缺口见gaps.md。
