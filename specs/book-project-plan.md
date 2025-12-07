# Physical AI & Humanoid Robotics — Technical Creation Plan

## Goal:
Translate the Constitution and Specification into a structured, technical plan to guide book creation using Spec-Kit Plus, Docusaurus, Claude Code, and iterative research-driven writing.

----------------------------------------
Architecture Sketch (High-Level Book System)
----------------------------------------

Book Structure:
- 4 Modules aligned with course requirements
- 16 Core Chapters + 2 Appendix Chapters
- Docusaurus structure:
  /docs/
     module-1/
     module-2/
     module-3/
     module-4/
     appendix/
- Sidebar auto-generated from folder structure
- Each chapter contains:
  - Introduction
  - Learning Objectives
  - Explanations
  - Diagrams (ASCII/Markdown)
  - Tables (when needed)
  - Minimal conceptual code
  - End-of-chapter summary

Content Pipeline Architecture:
1. **Research-Concurrent Writing Loop**
   - Each chapter is researched while writing
   - No upfront research dump
   - Validation and revisions done at the end of each chapter

2. **Source Verification**
   - Verify robotics & AI content via official docs:
     - ROS 2 Documentation
     - Gazebo Classic & Ignition docs
     - Unity Robotics Hub
     - NVIDIA Isaac & Omniverse docs
     - Scientific/academic papers (as needed)
   - All factual claims must have sources

3. **Model Interaction Architecture**
   - Writer (you) → /sp.specify → /sp.plan → /sp.generate
   - Claude/Gemini produce drafts
   - Human verifies and finalizes

4. **Deployment Architecture**
   - Docusaurus v3 project
   - GitHub repo + GitHub Pages deployment
   - Continuous writing workflow via Claude Code & Gemini CLI

----------------------------------------
Section (Chapter) Structure Plan
----------------------------------------

All chapters must follow the SAME template for consistency:

1. **Title**
2. **Short Overview (3–5 lines)**
3. **Learning Objectives (3–6 bullets)**
4. **Main Sections**
   - Concepts explained in small subsections
   - Maximum clarity
   - Use diagrams and tables
5. **Mini Case Study / Example**
6. **Robotics Insight Box** (optional)
7. **Summary Key Points**
8. **Reading/Research References (APA format)**

Chapters must avoid:
- Code-heavy content
- Advanced math derivations
- Hardware-specific deep wiring

Chapters must include:
- Real robotics concepts
- Industry terminology
- Simple visuals
- Flow diagrams for pipelines

----------------------------------------
Research Approach
----------------------------------------

Use **Research-Concurrent Strategy**, meaning:

Step 1 — Read a small part of official documentation  
Step 2 — Write the section  
Step 3 — Verify the claims  
Step 4 — Add APA citations  
Step 5 — Move to the next section  

Primary Research Sources:
- ROS 2 Official Docs  
- Gazebo Documentation  
- Unity Robotics Hub  
- NVIDIA Isaac Sim, Isaac ROS, Nav2 Docs  
- Academic papers on embodied intelligence  
- Robotics textbooks on kinematics/perception  

Research Priorities by Module:
- **Module 1:** ROS architecture, sensors, URDF basics  
- **Module 2:** Physics simulation, digital twin principles  
- **Module 3:** Isaac Sim, SLAM, Nav2, path planning  
- **Module 4:** VLA systems, LLM planning, Whisper pipeline  

Citation Style:
- APA (7th Edition)
- Inline parentheses + reference list at end of chapter

----------------------------------------
Quality Validation Plan
----------------------------------------

Each chapter must pass the following checks:

1. **Accuracy Check**
   - Are technical statements correct?
   - Are robotics terms used properly?
   - If needed, validated against primary sources

2. **Readability Check**
   - Grade 7–10 reading level  
   - Short sentences  
   - Avoid jargon unless defined  

3. **Structure Compliance**
   - All sections present  
   - Diagrams included where required  
   - Summary at the end  

4. **Plagiarism Check**
   - MUST be 0%
   - Every definition written originally  
   - No copying text from ROS docs or Isaac docs  

5. **Traceability Check**
   - Every factual claim traceable to source  
   - APA citations used properly  

6. **Consistency Check**
   - Same tone across chapters  
   - Same explanation style  
   - Consistent terminology  

7. **Docusaurus Build Check**
   - Markdown renders without errors  
   - No invalid syntax  
   - Sidebars auto-generate properly  

----------------------------------------
Constitution Check
----------------------------------------

- [x] **Utility:** The book must serve as a practical, actionable guide for readers.
- [x] **Clarity & Accessibility:** Content must be easy to understand for developers and technical writers.
- [x] **Spec-Driven Consistency:** Strict adherence to all defined specifications, including spec-kit-plus conventions and Docusaurus structure.
- [x] **Reproducibility:** All code examples and setup steps must be fully functional and verifiable by the reader.

----------------------------------------
Decisions Needing Documentation (with Tradeoffs)
----------------------------------------

1. **Depth Level: Beginner-friendly vs Expert Detail**
   - Option A: Very beginner  
     + Accessible  
     – Too shallow  
   - Option B: Balanced (Chosen)  
     + Enough depth  
     + Clear explanations  
     – Requires more research  

2. **Simulation Tools Emphasis**
   - Gazebo vs Isaac Sim  
   - Decision: Both equally covered per Q4 curriculum  

3. **LLM Role in Robotics**
   - Option A: Heavy code examples  
   - Option B: Conceptual architecture only (Chosen)  

4. **Docusaurus Theme Choice**
   - Default classic theme  
     + Stable  
     + Easy deployment  
     – Less visual customization  
   - Chosen: Keep default for simplicity  

5. **Research Style**
   - Upfront research vs concurrent  
   - Chosen: concurrent (per Spec-Kit standards)  

----------------------------------------
Testing Strategy (Validation Based on Acceptance Criteria)
----------------------------------------

You will validate the project in 3 layers:

### 1. **Content Acceptance Tests**
- Does each chapter answer the module’s expected outcomes?  
- Does the content match the 4-module structure?  
- Are all diagrams readable?  
- Does every chapter include summaries?

### 2. **Technical Tests**
- Docusaurus runs using `npm run start`  
- No broken markdown  
- Images and diagrams load  
- Sidebar navigation works  
- GitHub Pages deployment builds successfully  

### 3. **Spec Compliance Tests**
- Does each output fulfill the /sp.constitution rules?  
- Does each chapter match the /sp.specify requirements?  
- Are APA citations included?  
- Does each chapter maintain 900–1500 words?  

----------------------------------------
Phased Work Plan
----------------------------------------

### **Phase 1 — Research**
- Gather required docs  
- Create minimal notes  
- No deep reading upfront  

### **Phase 2 — Foundation**
- Set up Docusaurus  
- Create folder and sidebar structure  
- Define chapter templates  

### **Phase 3 — Analysis**
- For each chapter:  
  - Identify required research  
  - Validate technical points  
  - Outline sub-sections  

### **Phase 4 — Synthesis & Writing**
- Write chapters one-by-one  
- Validate via checks  
- Insert APA citations  
- Render Docusaurus preview  
- Commit to GitHub  

----------------------------------------
Success Criteria for the Plan
----------------------------------------

- Book can be generated incrementally by Spec-Kit Plus  
- Writing style stays consistent  
- Content is accurate and accessible  
- All modules match course curriculum  
- GitHub Pages deployment works  
- Students can learn end-to-end Physical AI fundamentals