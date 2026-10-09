# Decisions — append-only

Canonical schema (defined only in the public repo path `personal-travel-intelligence/references/data-model.md`; in an installed Codex workspace, use `.agents/skills/personal-travel-intelligence/references/data-model.md`):

```yaml
- id: ""
  date: ""
  topic: ""
  options: []
  constraints: []
  choice: ""
  rejected_reasons: []
  expected: ""
  actual: ""
  lesson: ""
  source_ids: []
  status: proposed
  reopen_trigger: ""
  updated: ""
```

Never invent missing reasons; use `unknown`. Append amendments rather than silently replacing historical records.
