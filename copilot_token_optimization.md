# Copilot Token Optimization Guide

## 1. Control Usage (High-Value Tasks Only)
- Use Copilot for: complex logic, debugging, refactoring
- Avoid: basic syntax, repetitive queries

---

## 2. Use Secondary Tools
- Use local tools like Ollama / LM Studio for:
  - brainstorming
  - documentation
- Then send refined prompt to Copilot

---

## 3. Prompt Compression
❌ Bad:
Analyze this 500-line file

✅ Good:
This function fails for edge case X. Fix only this part:
<20 lines>

---

## 4. Staged Prompting
- Step 1: Use cheap/local tool to refine prompt
- Step 2: Use Copilot for execution

---

## 5. Reusable Prompt Templates
- Create templates for:
  - bug fixing
  - code generation
  - PR comments

---

## 6. Limit Chat Depth
- Start new chat after 3–5 interactions
- Prevents context/token bloat

---

## 7. Avoid Retry Loops
- Don’t use “Try Again” repeatedly
- Instead: rephrase prompt or start new chat

---

## 8. Prefer Inline over Chat
- Use inline suggestions for small edits
- Chat is heavier and consumes more tokens

---

## 9. Restrict Output Size
Example:
Keep response under 10 lines. No explanation.

---

## 10. Use Graph/Workflows
- Move repeated logic into reusable workflows
- Avoid repeated Copilot queries

---

## Key Takeaway
Use Copilot as a precision tool for high-value tasks, not general usage.
