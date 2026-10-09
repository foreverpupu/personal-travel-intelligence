# Installation and quick start / 安装与快速上手

## Codex workspace (experimental; not yet client-validated)

Run these commands **from the cloned repository root**, the folder that contains `README.md`, `personal-travel-intelligence/SKILL.md`, and `travel-workspace-template/`. The *outer* Git repository and *inner* skill folder happen to share a name; only the inner folder contains `SKILL.md`.

```bash
mkdir -p "$HOME/Travel-Intelligence/.agents/skills"
cp -R ./personal-travel-intelligence "$HOME/Travel-Intelligence/.agents/skills/"
```

Choose an empty/new workspace if possible. If the target already has `AGENTS.md`, **merge** its instructions with the contents of `travel-workspace-template/AGENTS.md`; never silently overwrite existing project instructions. Copy `travel-workspace-template/travel-data/` to the workspace's `travel-data/` folder, keeping `_templates/` available.

```bash
mkdir -p "$HOME/Travel-Intelligence/travel-data"
cp -R ./travel-workspace-template/travel-data/. "$HOME/Travel-Intelligence/travel-data/"
cp ./travel-workspace-template/AGENTS.md "$HOME/Travel-Intelligence/AGENTS.md"  # ONLY for a NEW workspace
cp "$HOME/Travel-Intelligence/travel-data/USER-preferences.example.md" \
   "$HOME/Travel-Intelligence/travel-data/USER-preferences.md"
```

The example profile is fictitious/blank. Edit it yourself or explicitly authorize the assistant to fill it from your statements. Never treat examples as real user preferences. To start a trip, either manually copy the four files from `travel-data/trips/_templates/` to `travel-data/trips/<trip-id>/`, or explicitly ask an assistant *with authorized file-write access* to copy and populate them; ask it to read back and verify. No private records are saved just by chatting.

Open the workspace in Codex and refresh/restart skills. Where supported, invoke `$personal-travel-intelligence`; otherwise use the client's skill picker or ask it to read `.agents/skills/personal-travel-intelligence/SKILL.md` and report whether the references are accessible. This last fallback merely asks it to read a file; it is **not** proof that automatic skill activation works. Codex Desktop and Tencent WorkBuddy remain untested for this repository.

## ChatGPT Project

Upload the inner `personal-travel-intelligence/SKILL.md` and the seven `personal-travel-intelligence/references/*.md` as eight separate Project sources. Paste [Project instructions](PROJECT-INSTRUCTIONS.md) into Project settings. This portable repository is not the exact layout of the earlier personally tested Project kit. Upload your own private records separately; Project sources are not automatically writable. Don't upload `examples/` or `evaluation/` as real trip facts.

## Word/PDF generation is separate from QA

The bundled `check_docx_pdf.py` **does not generate files**. To *create* DOCX/PDF, use your host's available document-authoring and export tools and check the resulting artifacts. A possible local conversion route on **macOS/Linux**, **only when these third-party programs are installed**, is:

```bash
pandoc YOUR_GUIDE.md -o YOUR_GUIDE.docx
# Pandoc may default to US Letter. Explicitly set every DOCX section to A4:
python3 - <<'PYSET_A4'
from docx import Document
from docx.shared import Mm
doc = Document('YOUR_GUIDE.docx')
for section in doc.sections:
    section.page_width, section.page_height = Mm(210), Mm(297)
doc.save('YOUR_GUIDE.docx')
PYSET_A4
libreoffice -env:UserInstallation=file:///tmp/pti-lo-profile --headless --convert-to pdf --outdir . YOUR_GUIDE.docx
```

This example is not a tested, bundled one-click publishing pipeline. The `/tmp/pti-lo-profile` configuration path is macOS/Linux-specific; Windows users must adapt the command and installation paths. LibreOffice defaults and installed CJK fonts may affect paper size and layout; **do not assume A4**. Word and PDF may need formatting adjustments; render and visually review every page.

Then install the separate QA dependencies and run the smoke check:

```bash
python3 -m pip install -r requirements.txt
python3 personal-travel-intelligence/scripts/check_docx_pdf.py YOUR_GUIDE.docx YOUR_GUIDE.pdf qa.json --require-chinese
```

If PyPI downloads time out, use an accessible package mirror approved by your organization, e.g. `python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt`. Verify trust and your environment policy before switching mirrors.

`--require-chinese` is recommended for Chinese routebooks. Omit it for deliberately English-only documents. QA return codes: 0 = no hard failures found (not a visual quality guarantee); 1 = actual hard check failed; 2 = setup/input problem. Near-margin spans and extra text require human review even when the exit code is 0.

## Tencent WorkBuddy

Unverified: exact importer, permissions and reference resolution vary by version. Do not promise direct ZIP installation; test with read-only file listing first.

## First task / 首次测试

Copy the following text and **paste it into your AI assistant chat box** (not a terminal command). / 将以下文字**粘贴到助手对话框**，不要在终端运行：

“请先只读检查是否加载 Personal Travel Intelligence 的 SKILL.md 和参考文件，列出实际可访问的规则与旅行资料，不修改文件。然后根据我提供的虚构旅行资料对比两种路线，并区分已确认与未知。”

## Privacy

Never publish real `travel-data/` records, personal photos, orders, locations or companion information. Review Git history before making a repository public.
