# Feature Specification: Python Agents and rclpy

**Feature Branch**: `002-python-agents-rclpy`  
**Created**: 2025-12-07  
**Status**: Draft  
**Input**: User description: "Module 1, Chapter 1.2: Python Agents and rclpy Target audience: Developers learning to interface Python with ROS 2. Focus: Hands-on implementation of the core communication paradigms using the Python client library. Success criteria: - **Functionality:** Provides complete, runnable Python code for a minimal **Publisher Node** and a minimal **Subscriber Node**. - **Package Management:** Details the necessary updates to `setup.py` and `package.xml` to correctly build a Python ROS 2 package. - **Testing:** Includes instructions for building the package using `colcon build` and running the publisher/subscriber pair to verify communication. Constraints: - **Output:** Docusaurus markdown file (`01-ros2/python-agents-rclpy.mdx`). - **Code:** Python code must use the **rclpy** library and the standard `std_msgs/String` message type. - **Example Analogy:** Use a simple robot scenario, like a ""Telemetry Publisher"" and a ""Data Logger Subscriber,"" to contextualize the code. Not building: - Code examples for ROS 2 Services or Actions. - C++ code examples."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Implement Minimal Publisher Node (Priority: P1)

Readers will implement a minimal, runnable Python Publisher Node using `rclpy` and `std_msgs/String`.

**Why this priority**: Fundamental building block for ROS 2 communication in Python.

**Independent Test**: Reader can execute the provided Python code and verify it publishes messages on a specified topic.

**Acceptance Scenarios**:

1. **Given** a new ROS 2 Python package, **When** the reader implements the publisher code, **Then** a node is created that publishes `std_msgs/String` messages.
2. **Given** the publisher node is running, **When** `ros2 topic echo <topic_name>` is used, **Then** the published string messages are displayed.

---

### User Story 2 - Implement Minimal Subscriber Node (Priority: P1)

Readers will implement a minimal, runnable Python Subscriber Node using `rclpy` and `std_msgs/String`.

**Why this priority**: Completes the basic communication paradigm (Publisher-Subscriber).

**Independent Test**: Reader can execute the provided Python code and verify it receives messages published on a specified topic.

**Acceptance Scenarios**:

1. **Given** a new ROS 2 Python package, **When** the reader implements the subscriber code, **Then** a node is created that subscribes to `std_msgs/String` messages.
2. **Given** a publisher node is active and sending messages, **When** the subscriber node is running, **Then** it prints the received string messages to the console.

---

### User Story 3 - Manage ROS 2 Python Package (Priority: P2)

Readers will update `setup.py` and `package.xml` to correctly build a Python ROS 2 package.

**Why this priority**: Essential for proper package management and build process in ROS 2.

**Independent Test**: Reader can successfully build the Python ROS 2 package using `colcon build` after modifying `setup.py` and `package.xml`.

**Acceptance Scenarios**:

1. **Given** Python publisher and subscriber nodes, **When** `setup.py` and `package.xml` are configured as detailed, **Then** the package can be built without errors using `colcon build`.
2. **Given** a built package, **When** the environment is sourced, **Then** the Python nodes are discoverable and runnable via `ros2 run`.

### Edge Cases

- None explicitly defined in prompt.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The chapter MUST provide complete, runnable Python code for a minimal Publisher Node.
- **FR-002**: The chapter MUST provide complete, runnable Python code for a minimal Subscriber Node.
- **FR-003**: The chapter MUST detail necessary updates to `setup.py` and `package.xml` to correctly build a Python ROS 2 package.
- **FR-004**: The chapter MUST include instructions for building the package using `colcon build`.
- **FR-005**: The chapter MUST include instructions for running the publisher/subscriber pair to verify communication.
- **FR-006**: Python code MUST use the `rclpy` library and the standard `std_msgs/String` message type.
- **FR-007**: The chapter MUST use a simple robot scenario (e.g., "Telemetry Publisher" and "Data Logger Subscriber") to contextualize the code.
- **FR-008**: The chapter MUST be formatted as a Docusaurus markdown file (`01-ros2/python-agents-rclpy.mdx`).

### Non-Functional Requirements

- **NFR-001**: The chapter MUST be targeted at developers learning to interface Python with ROS 2.
- **NFR-002**: Focus on hands-on implementation of core communication paradigms.

### Key Entities (Conceptual)

- **Publisher Node**: A ROS 2 node that sends messages on a topic.
- **Subscriber Node**: A ROS 2 node that receives messages from a topic.
- **rclpy**: The ROS 2 client library for Python.
- **std_msgs/String**: A standard ROS 2 message type for plain text.
- **setup.py**: Python setuptools script for package installation.
- **package.xml**: ROS 2 manifest file for package metadata.
- **colcon build**: ROS 2 build tool.

### Explicit Out-of-Scope

- Code examples for ROS 2 Services or Actions.
- C++ code examples.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The chapter provides complete, runnable Python code for a minimal Publisher Node and a minimal Subscriber Node.
- **SC-002**: The chapter details the necessary updates to `setup.py` and `package.xml` to correctly build a Python ROS 2 package.
- **SC-003**: The chapter includes instructions for building the package using `colcon build` and running the publisher/subscriber pair to verify communication.
