# LEP Workflow Runtime v1.0

## Overview

The LEP Workflow Runtime provides deterministic workflow definition, validation,
lifecycle management, and execution control for LEP engineering processes.

## Architecture

```
WorkflowManager (orchestrator)
  ├── WorkflowRegistry     — deterministic registration, tag filtering
  ├── WorkflowLifecycle    — 7-state machine (CREATED → ... → COMPLETED)
  ├── WorkflowExecutor     — deterministic step execution engine
  ├── WorkflowValidator    — Tier 1 (schema/metadata), Tier 2 (dependency)
  ├── WorkflowHistory      — execution records with step results
  ├── WorkflowEventPublisher   — EventBus integration (8 events)
  ├── WorkflowSnapshot     — immutable state snapshots
  └── WorkflowDependencyValidator — asset/capability dependency checks
```

## Lifecycle States

```
CREATED → VALIDATED → READY → RUNNING → COMPLETED
    │         │                  │
    └─ FAILED ┴─ FAILED          ├─ FAILED
                                 └─ STOPPED
FAILED → CREATED  (retry)
STOPPED → CREATED (restart)
```

## Workflow Model

| Concept | Type | Description |
|---------|------|-------------|
| `WorkflowDefinition` | dataclass | Identity, name, version, steps, owner, tags |
| `WorkflowStep` | frozen dataclass | step_id, name, type (task/conditional/parallel/sub_workflow) |
| `WorkflowExecution` | dataclass | Runtime execution state with step results |
| `WorkflowResult` | dataclass | Execution outcome with `successful()`/`failed()` helpers |

## Execution Model

- Deterministic — no AI behavior, no autonomous planning
- Step-by-step sequential execution
- Each step captures: step_id, status, timestamps, output/error
- Failure stops execution immediately
- Results recorded in WorkflowHistory

## Events

- `workflow.WorkflowCreated`
- `workflow.WorkflowValidated`
- `workflow.WorkflowStarted`
- `workflow.WorkflowStepStarted`
- `workflow.WorkflowStepCompleted`
- `workflow.WorkflowCompleted`
- `workflow.WorkflowFailed`
- `workflow.WorkflowStopped`

## Validation Tiers

**Tier 1:**
- Schema validation (Draft 2020-12)
- Metadata correctness (workflow_id, name, steps required)
- Step validation (unique step_ids)

**Tier 2:**
- Dependency validation (asset availability)
- Capability validation (extension capability availability)
- Execution constraint validation

## Limitations

- Sequential execution only — no DAG/parallel branching in v1.0
- No AI or autonomous planning
- Timeout and retry declared but not enforced in v1.0 executor

## Future Evolution

- DAG-based workflow definitions
- Parallel step execution
- Conditional branching
- Sub-workflow composition
- Dynamic step routing
