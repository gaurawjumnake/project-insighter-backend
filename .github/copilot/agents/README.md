# Agents Directory

**Purpose:** Agent specifications — source of truth for agent capabilities, constraints, and collaboration rules  
**Token Focus:** Load only AGENTS.md (single source of truth)

---

## 📂 Structure

```
agents/
├── README.md (this file)
└── AGENTS.md ← Source of truth for all agent specs
```

---

## 🤖 Quick Reference

| Agent | Specialization | SDLC Phases | When to Load |
|-------|---|---|---|
| **@api-dev** | FastAPI endpoints, services, tests | PHASE 3, 4, 7 | Working on API changes |
| **@ai-arch** | CrewAI crews, LLM prompts, pipelines | PHASE 3, 4, 7 | Working on AI/ML features |
| **Orchestrator** | Workflow management, phase coordination | PHASE 1, 2, 5, 6, 8 | Incoming tickets/requirements |

---

## 📋 AGENTS.md Content

**Load:** [AGENTS.md](AGENTS.md)  
**Size:** 500+ lines  
**Contains:**
- Full agent configuration (YAML format)
- Expertise & capabilities for each agent
- Tools available to each agent
- Constraints & rules
- Context sources for each agent
- Handoff triggers & collaboration rules
- Success metrics

---

## 🚀 Usage Pattern

**For any agent-related question:**

1. Go to: [AGENTS.md](AGENTS.md)
2. Find: Agent you need (@api-dev, @ai-arch, Orchestrator)
3. Load: Full YAML specification for that agent
4. Use: For dispatching work, understanding capabilities, or coordinating handoffs

---

## 🔗 Related

- **Workflow orchestration:** [../instructions/workflow-orchestrator.md](../instructions/workflow-orchestrator.md)
- **Phase details:** [../instructions/phases/](../instructions/phases/)
- **Code patterns:** [../context/PATTERNS.md](../context/PATTERNS.md)

### Pattern: Working with Agents

```
1. Need to know which agent handles what? → Load: [../../ROUTING.md](../../ROUTING.md)
2. Need agent's detailed specs? → Load: [AGENTS.md](AGENTS.md)
3. Submitting work to an agent? → Reference: [AGENTS.md](AGENTS.md) handoff triggers
```

---

## 📊 Token Optimization

Load strategically based on your task:

| Task | Load | Tokens |
|------|------|--------|
| Route feature request to agent | [../../ROUTING.md](../../ROUTING.md) | ~200 |
| Get full @api-dev specs | [AGENTS.md](AGENTS.md) (@api-dev section) | ~300 |
| Get full @ai-arch specs | [AGENTS.md](AGENTS.md) (@ai-arch section) | ~300 |

**Recommendation:** Load ROUTING.md first to determine which agent to use, then load full AGENTS.md for that specific agent only.

---

## 🔗 Related Docs

- [../../ROUTING.md](../../ROUTING.md) — Task routing, agent assignment, phase mapping
- [../instructions/workflow-orchestrator.md](../instructions/workflow-orchestrator.md) — SDLC workflow overview
- [../context/PATTERNS.md](../context/PATTERNS.md) — Code patterns agents must follow
