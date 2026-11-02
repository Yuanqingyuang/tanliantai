# T-0037 仓库同步任务
> 状态：草案

## 1. 基本信息

任务 T-0037，T1 文档同步，2026-11-02。执行：Agent；监督及确认：袁青扬。

## 2. 目标

拉取 origin/main 的最新已合并进度，合并本地既有文档，提交并推送，验证远程与本地提交一致。

## 3. 范围

既有本地申报材料、技术方案及留痕、三处冲突索引、答辩PPT与讲稿、预算截图。

## 4. 非目标

不修改核算公式、因子、正式契约，不宣告技术验证或学术审核完成；不合并尚未合入主分支的远程开发分支。

## 5. 输入资料

用户本次同步指令、origin/main（6b5adb5）、本地改动备份 stash（codex-sync-backup-2026-11-02）、申报书v2.0及8页PPT和演讲稿。

## 6. 验收标准

无未解决冲突；结构、环境、安全、链接、治理及联动检查通过；推送后本地HEAD等于origin/main。

## 7. 影响目录

docs/product/、docs/planning/、docs/decisions/、CHANGELOG.md、tools/安全脚本与精确登记及既有根目录预算截图。

## 8. 测试要求

执行 tools/check_repo_structure.py、environment/scripts/check_environment.py、tools/check_data_safety.py、tools/check_links.py、tools/check_governance.py、tools/check_doc_sync.py，追加 git diff --check 与远程提交比对。

## 9. 数据与安全

不接触真实企业BOM或工艺数据。预算截图为项目申报预算，不是企业交易数据。提交前执行安全扫描；原始附件保持原字节。

## 10. 交付物

同步提交、答辩文件与讲稿归档、当前任务及交付报告、GitHub主分支。

## 11. 未决事项

历史本地与远程ADR存在同号，保留完整文件名并在索引说明。WBS五阶段与最新两年八阶段进度的后续对齐由项目负责人另行确认，不在本次同步中改写远程任务分工。

## 同步检查修正

6份申报Word因安全脚本的统一数据后缀规则被阻塞。核对申报文本结构与嵌入附件后，以tools/document-artifacts.json登记完整路径和SHA-256，仅豁免匹配文件的目录规则，不豁免凭据及强敏感文件名。任务影响范围补充tools/。修复一条旧Word文件名失效链接。
