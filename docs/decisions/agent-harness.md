---
type: Decision
title: Agent harness - own nodes on the LangGraph runtime
description: The agent loop is built by hand first, then its functions run as nodes in a LangGraph graph. LangGraph's prebuilt agents are not used.
tags: [decision, ai, agent, langgraph]
status: stable
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-11-22T18:47:12Z"
sources:
  - id: ike-2026-11-22
    resource: process:planning-session
    author: human:ike
    title: Planning conversation with Ike, 2026-11-22
---

# Decision

1. **Hand-build the loop first** in plain Python on the Anthropic SDK. The loop calls the model, runs the requested tools (validated with Pydantic, with errors returned to the model as tool results), and stops on a final answer, an iteration limit, a token or cost budget, or an unrecoverable error.
2. **Then run those same functions as nodes in a LangGraph graph.** Ike's code keeps the parts interviews ask about: building the prompt, calling the model, running tools, stopping conditions. LangGraph supplies the runtime parts that are slow to build: checkpointing, resuming, human-in-the-loop interrupts, streaming and parallel tool calls.
3. **Don't use LangGraph's prebuilt agents** (such as `create_react_agent`), because they hide the loop.[^ike-2026-11-22]

# Why

* Ike can explain the loop from his own code, and can explain what LangGraph adds from having used both.
* LangGraph appears in many job postings.

# Open

* Which runtime features to take from LangGraph, and when. This will be decided during design.

[^ike-2026-11-22]: Ike agreed to the hybrid ("sounds good to me") and said which parts LangGraph covers "can be decided on later."
