# Personal Travel Intelligence（PTI）

**认真规划，灵活旅行，真实记录每一次经历。**

[English](README.md) · [安装与快速上手](docs/QUICKSTART.md) · [已知限制](docs/LIMITATIONS.md) · [评价实验](evaluation/README.md)

PTI 是一套**以 Markdown 文件为基础的个人旅行 AI Skill**。它把行前规划、旅中调整、行后复盘及朋友版路书整理成可复用的工作方法，并让用户掌握自己的旅行资料。**Skill 不会让底层模型更聪明；相比认真提示的通用模型是否更好，尚待公平对照验证。**

### 可以做什么

- **行前：** 比较目的地、路线与取舍，尊重已预订、不可退改和旅行限制。
- **旅中：** 根据体力、天气、交通变化提出下一步建议，不谎称已改订单。
- **行后：** 区分计划、实际与推测，把用户提供的真实经历整理成路书。
- **归档与出版：** 在授权环境里管理 Markdown 台账，并生成可编辑 Word/可搜索 PDF，按条件检查输出质量。

### 不承诺什么

不内置实时酒店/交通库存，不自动预订、取消或退款；ChatGPT Project 的来源文件不会因聊天自动改写；不同平台不会自动同步私人资料；路书需要作者亲自审稿。

**语言范围：** 优先为中文旅行写作设计；行前规划可用于其他语言，但出版规则、中文加英文地名写法及简体中文 QA 主要针对中文；其他语言出版未验证。

### 手动配置（实验性，所需时间取决于宿主环境）

- **Codex：** 将 `personal-travel-intelligence/` 放到工作空间 `.agents/skills/`；将 `travel-workspace-template/` 内部内容复制到工作空间根目录；重新打开工作空间或刷新技能发现；在支持的输入框试 `$personal-travel-intelligence`。**尚未在真实 Codex 客户端完成验收。**
- **ChatGPT Project：** 上传 `SKILL.md` 与 `references/` 中七个规则文件，使用 [Project instructions 模板](docs/PROJECT-INSTRUCTIONS.md)；私人资料单独上传并人工更新。
- **腾讯 WorkBuddy：** 未验证真实客户端的导入格式、引用目录加载及脚本权限，不能承诺直接 ZIP 安装。

具体操作参阅 [Quick Start](docs/QUICKSTART.md)。需要 `pymupdf` 和 `python-docx` 运行随附 QA 脚本；QA 脚本仅检查已经生成的文件，**不负责生成** Word/PDF；生成方式和依赖请参阅 [快速上手](docs/QUICKSTART.md)。

### 已验证 / 未验证

- **已有限验证：** 一个个人旅行历史、数项 ChatGPT Project 场景和 Word/PDF 产物。此前发现过 PDF 实际为 Letter 却被描述为 A4、朋友版混入内部文件名。
- **已实现待宿主验证：** 标准 Skill 目录、四份旅行台账模板、QA 脚本。
- **仍是假设：** 相比公平提示的 GPT/Gemini 等有多少增量价值、陌生人是否愿意使用、是否值得独立产品化。

公开仓库**不包含**个人偏好、旅行订单、私人路书或私人聊天。公开 Skill 和示例使用虚构或通用情境。发布前请自行确认知识产权与利益冲突边界。项目以 [MIT License](LICENSE) 开源，Copyright (c) 2026 Amy Wei。

[规则设计原因](docs/WHY-THE-RULES.md) · [实验材料](evaluation/README.md) · [贡献说明及隐私提示](CONTRIBUTING.md)
