# PHASE 2: Task Breakdown

**Tokens:** ~150 | **Duration:** 15-20 min | **Owner:** Orchestrator  
**Gate:** ⏸️ WAIT_FOR_APPROVAL

---

## 📋 INPUT

- Impact analysis from PHASE 1
- Project conventions (from [PROJECT_CONTEXT.md](../../../../PROJECT_CONTEXT.md), PATTERNS.md)

---

## 🎯 ACTIONS

1. **Break requirement into atomic tasks** (T1, T2, T3, ...)
2. **Assign task type**: code | test | doc | refactor
3. **Identify dependencies** between tasks
4. **Estimate scope** (T-shirt: xs / s / m / l / xl)
5. **Estimate total tokens** for PHASE 3-4

---

## 📤 OUTPUT (YAML Format)

```yaml
phase: 2_task_breakdown
ticket_id: "PROJ-123"
mode: feature  # From PHASE 1

tasks:
  - id: T1
    type: code
    title: "Update AccountCreate schema"
    description: "Add new_field: Optional[str] to Pydantic model"
    files:
      - backend/finance/app/schemas/account.py
    dependencies: []
    scope: xs  # < 15 min
    
  - id: T2
    type: code
    title: "Add column to ORM model"
    description: "Add new_field column to Account SQLAlchemy model"
    files:
      - backend/finance/app/models/account.py
    dependencies: [T1]
    scope: xs
    
  - id: T3
    type: code
    title: "Update service layer"
    description: "Modify AccountService.create() to handle new_field"
    files:
      - backend/finance/app/services/account.py
    dependencies: [T1, T2]
    scope: s  # 15-30 min
    
  - id: T4
    type: test
    title: "Write unit tests"
    description: "Happy path, edge cases, error scenarios for new_field"
    files:
      - tests/finance/test_account_service.py
    dependencies: [T3]
    scope: s
    
  - id: T5
    type: doc
    title: "Update documentation"
    description: "API docs, README, docstrings with new_field"
    files:
      - backend/finance/app/api/account.py  # docstring
      - readme.md
    dependencies: [T3, T4]
    scope: xs

summary:
  total_tasks: 5
  total_scope: "s (small - 1-2 hours)"
  estimated_tokens_phase_3_4: 800
  critical_path: "T1 → T2 → T3 → T4 → T5"
```

---

## ✅ APPROVAL CHECKLIST

Before approving PHASE 2, verify:

- [ ] Each task is atomic (can be completed independently)
- [ ] Dependencies are clear and logical
- [ ] Scope estimates are realistic
- [ ] No task exceeds 1 hour (break larger ones)
- [ ] Test coverage plan included
- [ ] Documentation requirements clear

---

## 🚨 COMMON ISSUES

| Issue | Resolution |
|-------|-----------|
| Task too large (> 1 hour) | Split into subtasks (T3a, T3b, T3c) |
| Circular dependencies | Reorder or merge tasks |
| Missing test task | Add T_test before code review phase |
| Unclear scope | Reference similar completed tickets |

---

## 📞 ESCALATION

If any of these apply, **revise or escalate:**
- Total scope > 8 hours (xl: needs split)
- Critical path > 5 tasks
- Multiple god node changes
- Cross-team coordination required

---

## 🔗 NEXT STEP

→ Upon approval, proceed to **PHASE 3: Code Generation** (`phases/PHASE-3-CODE-GENERATION.md`)
