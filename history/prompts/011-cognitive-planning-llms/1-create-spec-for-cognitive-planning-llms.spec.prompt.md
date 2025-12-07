---
id: 1
title: Create Spec for Cognitive Planning with LLMs
stage: spec
date: 2025-12-07
surface: agent
model: gemini
feature: 011-cognitive-planning-llms
branch: main
user: unknown
command: /sp.specify (manual workaround)
labels: [spec, manual-creation, llm, cognitive-planning]
links:
  spec: specs/011-cognitive-planning-llms/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/011-cognitive-planning-llms/spec.md
 - specs/011-cognitive-planning-llms/checklists/requirements.md
tests:
 - none
---

## Prompt

Module 4, Chapter 4.2: Cognitive Planning with LLMs Target audience: Students focused on high-level robot control and decision-making. Focus: Using Large Language Models (LLMs) to bridge human intention to technical robot actions. Success criteria: - **Cognitive Planning:** Clearly defines the role of the LLM: translating a goal (""Clean the room"") into a sequence of low-level **ROS 2 actions** (e.g., Navigate to X, Grasp Y, Deposit Z). - **Prompt Engineering:** Provides a template for the system prompt used to instruct the LLM on valid ROS 2 actions (the robot's API). - **Action Sequence:** Demonstrates a simplified example of the LLM outputting a structured action sequence (e.g., JSON or YAML). Constraints: - **Output:** Docusaurus markdown file (`04-vla/llm-cognitive-planning.mdx`). - **Focus:** Emphasis on the **reasoning** and **translation** step of the VLA loop. - **Tools:** Requires discussion of how the LLM communicates with the ROS 2 system (e.g., via a ROS 2 Service call). Not building: - Training a custom LLM from scratch. - Detailed implementation of the final action controllers (already covered in Module 1).

## Response snapshot

I have manually created the specification for Module 4, Chapter 4.2: Cognitive Planning with LLMs, including the spec.md and an initial requirements.md checklist.

## Outcome

- ✅ Impact: Successfully created the spec file and associated checklist for Chapter 4.2, bypassing the blocking script issue.
- 🧪 Tests: none
- 📁 Files: specs/001-cognitive-planning-llms/spec.md, specs/001-cognitive-planning-llms/checklists/requirements.md
- 🔁 Next prompts: Continue with remaining chapters.
- 🧠 Reflection: Manual creation process is consistent and effective for creating specs.

## Evaluation notes (flywheel)

- Failure modes observed: `create-new-feature.ps1` script failing with `PositionalParameterNotFound` error.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Continue manual creation for remaining chapters.
