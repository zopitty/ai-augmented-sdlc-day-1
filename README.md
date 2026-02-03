# Hands-on Lab: The "Legacy Code" Rescue Mission
**Tools:** VS Code, GitHub Copilot Chat  

## Scenario
You are a Senior Developer at **QuickShip Logistics**. You have received **JIRA Ticket #404**: 
> "The `shipping_calculator.py` function is failing on edge cases and is unreadable. Refactor it, add logging, and write tests."

The provided `shipping_calculator.py` is intentionally written like **messy legacy code**: it runs, but it does not follow our standards and is awkward to maintain. Your job is to use Copilot effectively to turn it into clean, testable, production-style code.

This is a **Skill Drill**. Your goal is to practice specific **Prompt Engineering** techniques to prepare for the main project later today.

---

## Instructions
**IMPORTANT (graded/checked):** Continuously update `lab_prompts.md` with **every prompt you use**.

- Add prompts **as you go** (don’t wait until the end).
- Include both your prompts and Copilot’s key responses when helpful.
- Your submission is incomplete without an updated `lab_prompts.md`.

### Step 1: Context & Role
**Techniques:** Role Prompting, Reverse Prompting

1.  Open `shipping_calculator.py`.
2.  Open **Copilot Chat**.
3.  **Define the Persona:** Instruct Copilot to act as a "Senior Python Backend Engineer" who cares about clean architecture and PEP8.
4.  **Gather Requirements:** Instead of guessing what `w`, `d`, and `p` mean, use **Reverse Prompting**. Ask Copilot to interview *you* about the business rules before it writes any code.
    * *Hint:* "Before you write code, ask me 3 clarifying questions..."
    * *Context:* If asked, tell Copilot: Weight is in kg, Distance in km, Currency in USD.
5.  **Update `lab_prompts.md`:** Paste the exact prompts you used in this step.

### Step 2: The Plan
**Techniques:** RAG (Retrieval Augmented Generation), Zero-Shot CoT (Chain of Thought)

1.  Keep `shipping_calculator.py` open.
2.  Open `coding_standards.md` so Copilot can see it (this acts as our RAG context).
3.  **Generate a Plan:** Ask Copilot to create a refactoring plan.
    * Reference the standards file explicitly (e.g., "Based on @coding_standards.md...").
    * Use **Zero-Shot CoT** by adding the phrase: **"Let's think step by step."**
4.  **Action:** Do not generate code yet. Just review the logic plan it proposes.
5.  **Update `lab_prompts.md`:** Paste the exact prompts you used in this step.

### Step 3: Execution
**Techniques:** Few-Shot Prompting, Tool Use Prompting

1.  **Generate Code:** Ask Copilot to rewrite the function based on the plan.
    * Use **Few-Shot Prompting**: Provide 2 examples of the exact docstring format you want.
    * *Examples:*
      * `Input: w=10 (int), d=100 (int), p='standard' (str) -> Output: 12.34 (Decimal)`
      * `Input: w='2.5' (str), d='0' (str), p=None (None) -> Output: 5.00 (Decimal)`
2.  **Generate Tests:** Instruct Copilot to act as a specific tool: **"Act as a Python Unit Test Generator."**
    * Ask it to generate a `unittest` suite that specifically targets the edge cases you discovered in Step 1.
3.  **Update `lab_prompts.md`:** Paste the exact prompts you used in this step.

### Step 4: The Review
**Techniques:** Reflexion, Self-Consistency

1.  **Reflexion:** Do not accept the code immediately.
    * Prompt Copilot: "Review the code you just wrote. Identify potential logic errors or missing type hints. Then generate a V2."
2.  **Self-Consistency:** Ask Copilot to generate **three different implementations** (e.g., using `if/else`, `match/case`, and `dictionary lookup`).
    * Ask it to evaluate which one is best for readability and choose the winner.
3.  **Update `lab_prompts.md`:** Paste the exact prompts you used in this step.

### Submission
Save your final `shipping_calculator.py` and your completed `lab_prompts.md`.