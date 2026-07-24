# LEP AI Runtime v1.0

## Overview

The LEP AI Runtime provides governed AI execution capabilities inside LEP.
It is an LEP extension capability that consumes existing LEP runtimes without
becoming the platform root.

## Architecture

```
AIManager (orchestrator)
  ├── AgentRegistry         — deterministic registration, capability-based lookup
  ├── AgentLifecycle        — 9-state machine (CREATED → ... → ARCHIVED)
  ├── AIExecutor            — ModelProvider abstraction, pluggable providers
  ├── Planner               — planning abstraction, objective decomposition
  ├── AgentMemory           — session-based context management
  ├── ToolInvocation        — tool registration, permission-gated invocation
  ├── AgentPermissions      — deny-by-default security controls
  ├── Evaluator             — execution evaluation hooks, quality metrics
  ├── AIValidator           — Tier 1 (schema/metadata), Tier 2 (permissions/deps)
  ├── Telemetry             — execution tracking, failure monitoring
  ├── AIEventPublisher      — EventBus integration (8 events)
  └── AISnapshot            — immutable state snapshots
```

## Agent Lifecycle

```
CREATED → REGISTERED → VALIDATED → READY → RUNNING → STOPPED → ARCHIVED
    │          │            │        │      │              │
    └─ FAILED ─┴─ FAILED ───┴─ FAILED─┴─ FAILED─┴─ FAILED ─┴─ FAILED
                                          │
                                      PAUSED → RUNNING
ARCHIVED → CREATED (restore)
FAILED → CREATED (retry) or ARCHIVED
```

## Agent Model

| Concept | Type | Description |
|---------|------|-------------|
| `Agent` | dataclass | Identity, name, version, capabilities, model, config |
| `AgentMetadata` | frozen dataclass | agent_id, name, version, model, owner, tags, timestamps |
| `AgentCapability` | frozen dataclass | capability_id, version, description |
| `AgentContext` | frozen dataclass | session_id, created_at, metadata |
| `AgentExecution` | dataclass | execution_id, status, timestamps, input/output, duration |

## Execution Model

- **ModelProvider**: Protocol for pluggable AI execution
- **InProcessProvider**: Default mock provider (no external AI required)
- No vendor lock-in — providers are pluggable
- No uncontrolled execution — all executions require proper lifecycle state

## Permissions

- Deny by default
- Explicit tool/knowledge/project grants
- `enforce_tool()` raises `PermissionDeniedError` on violation

## Tool Integration

Tools originate from:
- Plugin Runtime capabilities
- Future MCP Extension

ToolBoundary provides: registration, permission-gated invocation, result handling

## Knowledge & Workflow Integration

- **Knowledge Runtime**: agents can access knowledge via permission grants
- **Workflow Runtime**: plans can produce workflow-compatible definitions
- **Plugin Runtime**: tools are sourced from plugin capabilities

## Events

- `ai.AgentCreated`
- `ai.AgentRegistered`
- `ai.AgentValidated`
- `ai.AgentStarted`
- `ai.AgentExecutionStarted`
- `ai.AgentExecutionCompleted`
- `ai.AgentFailed`
- `ai.AgentStopped`

## Telemetry

Tracks: executions, failures, duration, agent state changes

## Future Evolution

- Local model providers (Ollama, llama.cpp)
- External API providers (OpenAI, Anthropic)
- MCP tool integration
- Autonomous workflow planning
- Agent-to-agent communication
