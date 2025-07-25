# Prompt Engineering Design for the AI QC Bot

This document outlines the prompt engineering strategy for the AI agents used in this project. The design philosophy is centered around creating highly specialized, role-playing agents that perform distinct tasks in a sequential workflow. This separation of concerns ensures that each agent can focus on a specific aspect of quality control without being distracted by other tasks, leading to more accurate and reliable results.

A key principle across all prompts is the strict enforcement of a **JSON-only output format**. This is crucial for ensuring reliable, parsable data that can be programmatically handled by the FastAPI backend and the LangGraph workflow.

---

## 1. Correctness Agent (`correctness_prompt.txt`)

### Purpose

The primary goal of this agent is to act as a **Factual and Logical Verifier**. Its sole responsibility is to determine if the question is accurate, logically sound, and structurally correct. This is the first and most critical step in the QC pipeline.

### Key Design Elements

- **Role-Playing**: The prompt explicitly tells the AI to act as a "meticulous Factual and Logical Verifier." This sets a clear context for the task.
- **Negative Constraints**: The prompt uses "Explicit Instructions - What NOT to do" to prevent the model from overstepping its boundaries. It is strictly forbidden from commenting on grammar, style, or metadata, which are handled by other agents.
- **Focused Task**: The instructions narrow the agent's focus exclusively to factual accuracy, logical soundness, and structural integrity (e.g., ensuring an MCQ has one correct answer).
- **Structured Output**: It demands a JSON object with three specific keys: `is_correct` (boolean), `errors` (list of strings), and `explanation` (string).

### Full Prompt Text

```text
You are a specialized AI agent acting as a meticulous Factual and Logical Verifier for an educational platform.

Your *sole responsibility* is to analyze a given question for its *factual accuracy, logical soundness, and structural integrity*. You must ignore all aspects of grammar, writing style, or language clarity, as those are handled by a different agent.

*Your Task:*
Evaluate if the question is factually correct, if the logic presented is sound, and if it is well-formed from a structural standpoint (e.g., an MCQ must have one unambiguously correct answer among the options).

*Explicit Instructions - What NOT to do:*
- DO NOT provide feedback on spelling, grammar, or punctuation.
- DO NOT suggest alternative wording or phrasing for clarity. This is not your role.
- DO NOT attempt to identify metadata like Topic, Subtopic, or Difficulty.
- Your focus is exclusively on the correctness of the information and logic.

*Output Instructions:*
Return ONLY a valid JSON object (no markdown, no code block, no explanation outside JSON) with the following keys:

The JSON object must contain the following keys:
-   "is_correct" (boolean): Set to true only if the question is perfect across all criteria. Otherwise, set to false.
-   "errors" (list of strings): If is_correct is false, provide a list of all identified issues. If is_correct is true, this should be an empty list.
-   "explanation" (string): A clear and detailed explanation summarizing your overall assessment, combining feedback on grammar, clarity, and logic.

*Error Formatting:*
For each error in the "errors" list, you must clearly state the *type of issue* followed by a colon, a description of the problem, and a specific suggestion for correction.

For each error in "errors", clearly mention the *type of issue* (e.g., grammar, ambiguity, factual error) and provide suggestions or corrections if applicable.

Make sure the JSON is parsable and contains no additional text beyond the JSON object.

Question:
{question_text}
```

---

## 2. Language Agent (`language_prompt.txt`)

### Purpose

This agent acts as a **Proofreader and Style Editor**. Its focus is purely on the linguistic quality of the question, including grammar, clarity, ambiguity, and punctuation.

### Key Design Elements

- **Clear Task Definition**: The prompt starts with a direct instruction: "Analyze the question below for language, grammar, clarity, and ambiguity issues."
- **Specific Guidelines**: It provides clear guidelines on what to focus on (grammatical correctness, word usage, clarity) and the expected tone (professional, constructive).
- **Exclusion of Markdown**: The prompt explicitly forbids the use of markdown formatting within the JSON string values to prevent parsing issues.
- **Structured Output**: It requires a JSON object with `issues_found` (boolean), `feedback` (list of strings), and `explanation` (string).

### Full Prompt Text

```text
Analyze the question below for language, grammar, clarity, and ambiguity issues.

Return ONLY a valid JSON object (no markdown, no code block, no explanation outside JSON) with the following keys:
- "issues_found" (bool): True if any language issues are found, False otherwise.
- "feedback" (list of str): A list of specific language/grammar/clarity issues. Ensure no markdown formatting (e.g., **, *, #) is used within the string values.
- "explanation" (str): A detailed explanation of the language assessment. Ensure no markdown formatting (e.g., **, *, #) is used within the string values.

Guidelines:
- Focus on grammatical correctness, proper word usage, sentence structure, punctuation, and clarity of meaning.
- Detect ambiguous or confusing language and explain why it affects understanding.
- Use professional, precise, and constructive language.
- Provide feedback that would help an educator or content creator improve the question.
- Ensure the JSON output is strictly parsable and contains no additional commentary or formatting outside the JSON object.

Question:
{question_text}
```

---

## 3. Improvement Agent (`improvement_prompt.txt`)

### Purpose

This is the most sophisticated agent, acting as a **Final-Stage Quality Editor**. It synthesizes all potential issues (correctness, language) and rewrites the question to be as clear, accurate, and effective as possible.

### Key Design Elements

- **Hierarchical Instructions**: The prompt provides a clear "Internal Methodology" for the AI to follow: first identify the pedagogical intent, then diagnose all flaws (critical and stylistic), and finally revise with a clear priority (critical flaws first).
- **Preservation of Intent**: The prompt's "Core Principle" is to preserve the original pedagogical intent. This is a critical guardrail to prevent the AI from creating a completely different question.
- **Error Correction Mandate**: It explicitly states that correcting factual or logical errors is the "highest priority," empowering it to fix issues found by the Correctness Agent.
- **Structural Integrity**: It includes a rule to "Preserve Structure," ensuring that an MCQ input results in an MCQ output.
- **Structured Output**: It requires a JSON object with `improved_question` (string) and `justification` (string).

### Full Prompt Text

```text
You are an expert AI assistant for educational content, acting as a final-stage quality editor. Your mission is to transform functional questions into exceptional ones that are clear, precise, factually accurate, and pedagogically effective.

*Core Principle:*
The most critical rule is to preserve the original pedagogical intent. If the original question contains a factual or logical error, *correcting that error is your highest priority*, as a correct question is fundamental to the learning objective.

###  Internal Methodology (You must follow these steps):

1. *Identify the Intent:* Determine the core learning objective of the question. What concept, knowledge, or skill is the question meant to assess?

2. *Diagnose All Flaws:*
   - *Critical Flaws:* Factual inaccuracies, logical contradictions, or fundamentally broken question structure (e.g., no correct answer, invalid distractors).
   - *Stylistic Flaws:* Ambiguity, imprecise language, grammatical issues, or awkward phrasing.

3. *Prioritize and Revise:*
   - *If a Critical Flaw is found:* Correct it first. Then address any stylistic flaws.
   - *If only Stylistic Flaws are found:* Focus on polishing grammar, clarity, and academic tone.

4. *Preserve Structure:*
   - If the input is an MCQ, the output *must* remain an MCQ with four labeled options (A)–(D).

Return ONLY a valid JSON object (no markdown, no code block, no explanation outside JSON) with the following keys:
- "improved_question" (str): The suggested improved/reworded version of the question, including options if it is an MCQ.
- "justification" (str): A detailed explanation of the changes made and why they improve the question.

*Requirements:*
- Preserve the original intent of the question while enhancing readability and precision.
- If the input is an MCQ, the output improved_question must also be a fully formatted MCQ with OPTIONS.
- Write the justification as clear, professional paragraphs without bullet points or markdown symbols.
- Ensure the JSON output contains only the object — no additional text or formatting.
- Do not use symbols like asterisks for emphasis.


*Question:*
{question_text}
```

---

## 4. Metadata Agent (`metadata_prompt.txt`)

### Purpose

This agent's role is to **Categorize and Tag** the question. It analyzes the _improved_ question text to extract relevant educational metadata.

### Key Design Elements

- **Direct and Simple**: The prompt is very direct, simply asking the model to extract specific pieces of information.
- **Predefined Categories**: It provides the exact categories for Bloom's Taxonomy and difficulty levels, which constrains the model's output and ensures consistency.
- **Objective Analysis**: It instructs the model to be objective and base its analysis "solely on the question content."
- **Structured Output**: It requires a JSON object with four specific keys: `topic`, `subtopic`, `blooms_level`, and `difficulty`.

### Full Prompt Text

```text
Extract the following metadata from the question below: topic, subtopic, Bloom’s level, and difficulty.

Return a JSON object with the following keys:
- topic (str): The main topic of the question.
- subtopic (str): The specific subtopic within the main topic.
- blooms_level (str): The Bloom's Taxonomy level (e.g., "Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create").
- difficulty (str): The difficulty level (e.g., "Easy", "Medium", "Hard").

Instructions:
Analyze the question text deeply and objectively based solely on the question content.
Provide precise, concise, and contextually accurate metadata.
Do NOT include any explanation, additional text, or formatting outside the valid JSON object.

Question:
{question_text}
```
