---
id: 1
title: Refactor Specs Directory Prefixes
stage: general
date: 2025-12-07
surface: agent
model: gemini
feature: none
branch: main
user: unknown
command: user request to align prefixes
labels: [refactor, directory-structure, specs]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-python-agents-rclpy/spec.md
 - specs/002-python-agents-rclpy/checklists/requirements.md
 - specs/003-robot-description-urdf/spec.md
 - specs/003-robot-description-urdf/checklists/requirements.md
 - specs/004-simulation-env-setup/spec.md
 - specs/004-simulation-env-setup/checklists/requirements.md
 - specs/005-physics-sensor-sim/spec.md
 - specs/005-physics-sensor-sim/checklists/requirements.md
 - specs/006-kinematics-visualization/spec.md
 - specs/006-kinematics-visualization/checklists/requirements.md
 - specs/007-isaac-sim-sdg/spec.md
 - specs/007-isaac-sim-sdg/checklists/requirements.md
 - specs/008-perception-navigation/spec.md
 - specs/008-perception-navigation/checklists/requirements.md
 - specs/009-training-sim-to-real/spec.md
 - specs/009-training-sim-to-real/checklists/requirements.md
 - specs/010-conversational-robotics-stack/spec.md
 - specs/010-conversational-robotics-stack/checklists/requirements.md
 - specs/011-cognitive-planning-llms/spec.md
 - specs/011-cognitive-planning-llms/checklists/requirements.md
 - specs/012-capstone-autonomous-humanoid/spec.md
 - specs/012-capstone-autonomous-humanoid/checklists/requirements.md
 - specs/013-test-feature/spec.md
tests:
 - none
---

## Prompt

ok now align the prefixes in my specs folder as every folder has prefix of 001.I want like 001,002 and so on...

## Response snapshot

I have refactored the prefixes of all directories within the `specs/` folder to align with a sequential numbering scheme based on module and chapter order. All internal references within `spec.md` and `checklists/requirements.md` files have been updated accordingly.

## Outcome

- ✅ Impact: Successfully refactored the directory naming scheme under `specs/` for better organization and sequential access.
- 🧪 Tests: none
- 📁 Files: All `specs/` directories were renamed (13 in total). All `spec.md` files (13) and 12 `checklists/requirements.md` files were updated internally.
- 🔁 Next prompts: Awaiting further instructions.
- 🧠 Reflection: This refactoring improves project structure and readability. Note that existing PHRs' `feature` fields were not updated to reflect these new directory names, which could lead to broken links in their metadata.

## Evaluation notes (flywheel)

- Failure modes observed: `checklists/requirements.md` for `013-test-feature` did not exist, so it was skipped.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Implement a recursive search and replace for PHR `feature` fields in future refactoring tasks involving directory renames, or provide a tool to fix them.
