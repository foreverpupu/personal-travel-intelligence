# Validation prompt — deep version

## Why the old "assume it is broken" stance is gone

"默认立场：这份材料有缺陷" buys compliance at the price of judgment: a model told to find defects will produce defects, including invented ones, and a model told nothing will produce praise. Neither is evidence. The replacement is **goal + method + evidence chain**: the reviewer is asked to decide whether this can ship and to show the steps that justify the decision. Sycophancy becomes unprofitable because approval now requires executed checks, quoted output, and a mutation test — not because the prompt orders a verdict.

## Three delivery modes

| Mode | Requires | Use when |
|---|---|---|
| Path mode | Filesystem + shell tool, folder granted | Codex, Claude Code, this harness |
| Upload mode | File attachments only | ChatGPT web/app, any chat without tools |
| Blind mode | Two outputs, no labels | Comparing two rule versions |

On this Mac: Codex has workspace access; Claude Desktop trusts only the folders listed in its settings until you add this one; ChatGPT has no local file tool. Build the bundle first — it contains only publishable files:

```bash
python3 scripts/pack_review.py     # → dist/review-<version>/ with MANIFEST.sha256
```

## Prompt 1 — path mode (main)

```text
# 角色与目标
你是独立评审者。目标只有一个：判断这份 PTI 技能材料能否发布为 v{版本}，并留下别人可以复核的证据链。
不要预设结论。若结论是"可发布"，说明你用什么方法排除了哪些失败模式；若结论是"需修"，每个缺陷都要能被别人按你写的步骤复现。

# 环境与边界
你有文件系统和 shell 权限。唯一允许读取的目录：{BUNDLE}
若 {BUNDLE} 不存在、或其中没有 MANIFEST.sha256，立即停止并报告"无法评审：包路径无效"。不要用仓库根目录或其他目录代替。
第一步，按顺序执行，并原样粘贴输出：
1. cd {BUNDLE} && shasum -a 256 -c MANIFEST.sha256
2. python3 scripts/check_all.py; echo "exit=$?"
   注意：exit=0 只代表工作区结构检查通过。若同时出现 PROJECT DRIFT 列表，那是 5 条未镜像规则，必须单独判定，不得当作"全部通过"。
3. git -C {REPO} log --oneline -8
不要读取该目录之外的任何文件。不要修改原文件；需要实验就复制到 /tmp。

# 证据优先级（从原始到二手）
1. 机器产物：哈希校验、check_all 输出、退出码、git diff
2. 规则正文与模板
3. CHANGELOG / 作者说明（只用于解释差异，不能当作证据）
先读 1，再读 2。三者冲突时以 1 为准，并指出冲突本身。

# 必须执行的方法（不是建议）
M1 规范性分级：每条规则标 MUST / SHOULD / MAY / 不可测，给出"不可测"占比。
M2 可追溯矩阵：规则ID → 文件:行 → 如何检查 → 证据 → 状态。
M3 变异测试（最高优先级）：把材料复制到 /tmp，删掉 SKILL.md 中 R5 的整段，运行 check_all，确认它变红；恢复后再确认变绿。报告"检查器能否被杀死"。无法执行时写 UNVERIFIABLE，不要猜。
M4 差分：工作区版与项目版逐条对照同一条规则，标"等价 / 不等价 / 项目版缺失"。
M5 反例：为每条 MUST 构造一个"字面遵守、意图违背"的例子（例如：列出了历史与文化选项，实际仍只推荐酒庄），判断现有规则能否识别。
M6 版本审计：VERSION、SKILL 标题、CHANGELOG、tag、发布单哈希是否指向同一提交；指出任何不存在的版本号。

# 五道门（每门给 PASS / FAIL / UNVERIFIABLE，附文件:行 + 不超过 2 行原文）
G1 结构：frontmatter 完整；references 引用存在；模板字段与 data-model 一致。
G2 一致性：同一条规则跨文件是否矛盾；两版是否声明同一组规则（用 M4 结果）。
G3 可执行性：规则能否从输出中被观察到；列出"不可测"条款。
G4 事实与隐私：有无编造的价格、营业时间、预订状态、排名；有无私人信息会进入公开仓库。
G5 版本与证据：M6 结果；发布单哈希与包内文件是否一致。

# 输出
表A 门结论（门 / 结论 / 证据）
表B 缺陷（编号 / 门 / 文件:行 / 原文 / 最小修法 / 复现步骤）
表C 可追溯矩阵（M2）
表D 无法判断（缺什么材料才能判断）
表E 残余风险（发布后仍可能错的地方，按影响排序）
最后：
- 发布建议：可发布 / 需修（列出阻塞项）
- 三条最高杠杆修改，按阻塞程度排序
- 你凭什么相信自己：写出实际执行过的步骤与结果；没执行的明确标"未执行"
```

## Prompt 1b — upload mode (replace the 环境 block only)

```text
# 环境与边界（无 shell）
我没有给你文件系统权限。材料以附件提供：M1 SKILL.md、M2 references/pre-trip.md、M3 references/data-model.md、
M4 docs/rule-manifest.json、M5 VERSION + CHANGELOG 顶部、M6 项目版 SKILL.md 与 pre-trip.md。
M3 变异测试无法执行：请给出让人类在终端执行的三条命令和预期输出，并把它标为 UNVERIFIABLE。
其余方法照常执行。无法校验哈希时以正文为准，并明确说明这一点。
```

## Prompt 2 — blind comparison (rule changes only)

```text
下面有 X 和 Y 两份输出，同一场景、同一输入，只有一处规则不同。我不告诉你哪份是新版。

行为要求（逐条判断，不要合并）：
1) <不把上一趟的活动组合当默认模板>
2) <不丢掉已确认的同伴偏好>
3) <不编造预订、价格、营业时间>

对每条要求给 X / Y / 平手，各引用一句原文。
若两份都满足，直接写"未观察到差异"；这比编造差异有用。
最后：你更愿意把哪一份给朋友看？三句话内说明，不确定就说不确定。
```

## Prompt 3 — Project upload check

```text
这是项目版的前一版 P 和待上传版 N。只做三件事：
1. 列出所有变化的行（新增/删除），按文件分组。
2. 检查 N 是否引用了 P 中存在、但 N 中已不存在的文件或章节。
3. 检查 N 是否丢失了 P 中与 A4 校验、隐私、QA PASS 相关的段落；如丢失，判断是有意删除还是误删，并给出依据。

不要评价文风，不要建议新增规则。
输出：变化清单 / 断链 / 丢失段落 / 结论（可上传 或 需修）。
```

## Beyond us: what can actually prove the result

Reviewer opinion is the weakest link. Ranked evidence, strongest first:

1. **Gate exit code** — `check_all.py` returns 0/1; reproducible by anyone.
2. **Mutation kill** — a deliberately broken copy must fail the gate. If it passes, the gate is decoration.
3. **Hash equality** — `MANIFEST.sha256` after packing, and after re-downloading from GitHub/Project.
4. **A second model family, blind** — with inter-rater agreement reported (κ), not averaged.
5. **Downstream consumer** — another agent loads the skill and a human rates the output.
6. **Real trip outcome** — the only ground truth for "helpful". Not available on this machine; until it exists, no claim about usefulness is supported.

## Reading results

- FAIL on G1/G5: mechanical, fix first.
- FAIL on G2: usually edition drift; check `docs/EDITION-PARITY.md`.
- FAIL on G3: the rule is unobservable — redesign, do not reword.
- FAIL on G4: blocks publication; re-run `scripts/release.py` after fixing.
- UNVERIFIABLE: record the missing input; never count as pass.
- All PASS with thin evidence: rerun one gate per message.

## Limits

- Review checks consistency and traceability, not usefulness.
- Two models disagreeing is information; averaging their scores destroys it.
- Re-running the same model on the same material mostly reproduces the same blind spots.
- A reviewer who helped write the rules is not an independent reviewer.
