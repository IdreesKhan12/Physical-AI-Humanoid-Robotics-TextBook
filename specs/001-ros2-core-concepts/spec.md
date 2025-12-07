# Feature Specification: ROS 2 Architecture and Core Concepts

**Feature Branch**: `001-ros2-core-concepts`  
**Created**: 2025-12-07  
**Status**: Draft  
**Input**: User description: "Module 1, Chapter 1.1: ROS 2 Architecture and Core Concepts Target audience: Engineering students starting robotics middleware. Focus: Introduce the fundamental distributed architecture of ROS 2 (Humble/Iron) using simple analogies. Success criteria: - **Clarity:** Reader can accurately define and differentiate **Nodes, Topics, Services, and Actions**. - **Practicality:** Includes a step-by-step terminal guide for setting up a ROS 2 workspace and sourcing the environment. - **Verification:** Includes commands for using `ros2 run`, `ros2 node list`, and `ros2 topic echo`. Constraints: - **Output:** Docusaurus markdown file (`01-ros2/ros2-core-concepts.mdx`). - **Language:** Instructional and technically precise. - **Code:** Only terminal commands and configuration files (no Python code yet). - **Visualization:** Must include a blockquote explaining the DDS layer as the underlying data transport mechanism. Not building: - Python code for publishers or subscribers (covered in 1.2). - Detailed explanation of Quality of Service (QoS) settings. - Installation instructions for ROS 2 (assume OS/ROS is installed)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Understand ROS 2 Core Concepts (Priority: P1)

Readers will learn and differentiate key ROS 2 concepts: Nodes, Topics, Services, and Actions.

**Why this priority**: Fundamental understanding required for all subsequent ROS 2 learning.

**Independent Test**: Reader can accurately define and differentiate Nodes, Topics, Services, and Actions without external help.

**Acceptance Scenarios**:

1. **Given** a reader with basic programming knowledge, **When** they complete this chapter, **Then** they can explain the role of a Node in ROS 2.
2. **Given** a reader understanding Nodes, **When** they review the Topic section, **Then** they can describe how Topics enable data streaming.
3. **Given** a reader understands Topics, **When** they review Services and Actions, **Then** they can differentiate between request-response (Services) and long-running goal-oriented (Actions) communication patterns.

---

### User Story 2 - Setup ROS 2 Workspace and Environment (Priority: P1)

Readers will be able to set up a ROS 2 workspace and correctly source the environment from the terminal.

**Why this priority**: Essential for running any ROS 2 commands or code examples.

**Independent Test**: Reader can execute the provided terminal commands to set up and source a ROS 2 workspace, confirming environment variables are set.

**Acceptance Scenarios**:

1. **Given** a clean terminal, **When** the reader follows the step-by-step guide, **Then** a new ROS 2 workspace is created.
2. **Given** an existing ROS 2 workspace, **When** the reader executes the sourcing command, **Then** `ROS_DISTRO` and `AMENT_PREFIX_PATH` are correctly set for the workspace.

---

### User Story 3 - Verify ROS 2 Communication (Priority: P2)

Readers will use ROS 2 command-line tools to verify nodes, topics, and echo topic data.

**Why this priority**: Provides immediate feedback and reinforces conceptual understanding with practical application.

**Independent Test**: Reader can run sample ROS 2 commands to list active nodes, list available topics, and echo data from a topic.

**Acceptance Scenarios**:

1. **Given** a running ROS 2 system, **When** the reader uses `ros2 node list`, **Then** all active nodes are displayed.
2. **Given** an active publisher, **When** the reader uses `ros2 topic echo <topic_name>`, **Then** messages published on that topic are displayed in the terminal.

### Edge Cases

- The chapter MUST address common troubleshooting steps or errors students might encounter when setting up a ROS 2 workspace or running basic `ros2` commands.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The chapter MUST introduce the fundamental distributed architecture of ROS 2.
- **FR-002**: The chapter MUST define and differentiate ROS 2 Nodes, Topics, Services, and Actions.
- **FR-003**: The chapter MUST provide a step-by-step terminal guide for setting up a ROS 2 workspace.
- **FR-004**: The chapter MUST provide instructions for sourcing the ROS 2 environment.
- **FR-005**: The chapter MUST include commands for using `ros2 run`, `ros2 node list`, and `ros2 topic echo`.
- **FR-006**: The chapter MUST include a blockquote explaining the DDS layer as the underlying data transport mechanism.
- **FR-007**: The chapter MUST be formatted as a Docusaurus markdown file (`01-ros2/ros2-core-concepts.mdx`).
- **FR-008**: The chapter MUST include a section on common troubleshooting steps or errors students might encounter and how to resolve them.

### Non-Functional Requirements

- **NFR-001**: The language MUST be instructional and technically precise.
- **NFR-002**: Code examples MUST be limited to terminal commands and configuration files (no Python code).

### Key Entities (Conceptual)

- **Node**: A process that performs computation.
- **Topic**: A named bus over which nodes exchange messages.
- **Service**: A request/reply communication between nodes.
- **Action**: A long-running goal-oriented communication between nodes.
- **DDS (Data Distribution Service)**: The underlying data transport mechanism for ROS 2.

### Explicit Out-of-Scope

- Python code for publishers or subscribers (covered in 1.2).
- Detailed explanation of Quality of Service (QoS) settings.
- Installation instructions for ROS 2 (assume OS/ROS is installed).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The reader can accurately define and differentiate Nodes, Topics, Services, and Actions.
- **SC-002**: The reader can successfully set up a ROS 2 workspace and source the environment using the provided terminal guide.
- **SC-003**: The reader can use `ros2 run`, `ros2 node list`, and `ros2 topic echo` commands as instructed.
- **SC-004**: The chapter provides clear guidance on common troubleshooting steps or errors.

## Clarifications
### Session 2025-12-07
- Q: Should the chapter include a section on common troubleshooting steps or errors students might encounter when setting up a ROS 2 workspace or running basic `ros2` commands, and how to resolve them? → A: Yes
