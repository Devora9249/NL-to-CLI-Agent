# NL to CLI Agent - Prompt Engineering Project

A specialized AI Agent that converts natural language instructions into executable Windows terminal commands (CMD/PowerShell). This project focuses on the iterative refinement of system prompts to ensure security, accuracy, and strict formatting.

## About the Project
This project was developed as a Prompt Engineering assignment. The goal was to create an LLM-based agent (using llama-3.3-70b-versatile) that evolves through systematic testing and measurement—moving from a basic model that executes dangerous commands to a secure, professional-grade CLI assistant.

## The Prompt Engineering Process
My core work focused on the iterative improvement of the system prompt to handle edge cases and security risks. The process followed these four distinct stages:

1.  **Stage 1: Basic Inputs & Initial Discovery** I started with simple inputs. The model performed basic translations well but had significant flaws: it was willing to execute dangerous commands (like `shutdown`) and attempted to answer general knowledge questions (like "Who is the president?") instead of sticking to CLI tasks.
    
2.  **Stage 2: Addressing Scope** I added specific constraints to the prompt to define its scope. This successfully solved the "general knowledge" issue (the model began refusing non-CLI questions), but it still provided dangerous commands because it viewed them as "technically valid" CLI requests.
    
3.  **Stage 3: Enforcing Security** In this stage, the safety mechanisms were fully realized. I revised the prompt with unequivocal, "zero-tolerance" language regarding safety. By explicitly listing forbidden actions and mandating a specific error message for dangerous requests, I successfully blocked all harmful commands.
    
4.  **Stage 4: Stress Testing** In the final stage, I introduced complex, long, and ambiguous inputs, including chained commands, slang, and "social engineering" attempts. The model stood its ground honorably, maintaining both security and logical accuracy even under pressure.

## Tech Stack
* **Language Model:** Groq (Llama-3.1-8b-instant)
* **Framework:** Python, Gradio
* **Package Manager:** `uv`

## Evaluation Metrics
Performance was measured across multiple iterations using a Google Sheet with 15+ test scenarios. Each test was graded on:
> **Note:** The complete tracking tables with inputs, outputs, and scores for each iteration are included in the attached file:  
> 📂 **[Click here to view the Tracking Tables](./Tracking_Tables.pdf)**
* **Syntactic Correctness:** Is the command valid for Windows?
* **Consistency:** Does it return *only* the command without explanations?
* **Safety:** Does it block dangerous or irrelevant requests?

## Example Outputs
| User Input | AI Agent Output |
| :--- | :--- |
| "Create a folder named Old_Emails and move all .msg files into it" | `mkdir Old_Emails && move *.msg Old_Emails` |