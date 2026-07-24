# LEP Automation Runtime v1.0

## Overview

The LEP Automation Runtime provides governed execution of repeatable engineering
operations through event triggers, schedules, manual execution, policy enforcement,
workflow invocation, and execution tracking.

## Architecture

```
AutomationManager (orchestrator)
  ├── AutomationRegistry     — deterministic registration, trigger-based lookup
  ├── AutomationLifecycle    — 8-state machine (CREATED → ... → ARCHIVED)
  ├── TriggerRegistry        — event/schedule/manual trigger management
  ├── Scheduler              — interval-based schedule evaluation
  ├── AutomationExecutor     — execution boundary, result recording
  ├── PolicyEngine           — deny-by-default security and governance
  ├── AutomationValidator    — Tier 1 (schema/metadata), Tier 2 (deps/capabilities)
  ├── AutomationHistory      — execution history with trigger source tracking
  ├── AutomationEventPublisher — EventBus integration (8 events)
  └── AutomationSnapshot     — immutable state snapshots
```

## Lifecycle States

```
CREATED → VALIDATED → READY → ENABLED → EXECUTING → DISABLED → ARCHIVED
    │          │         │        │          │          │
    └─ FAILED ─┴─ FAILED ─┴─ FAILED┴─ FAILED ─┴─ FAILED ─┴─ FAILED
                               └─ DISABLED ─┤
                                             └── ENABLED (reenable)
                                             └── READY (reset)
ARCHIVED → CREATED (restore)
FAILED → CREATED (retry) or ARCHIVED
```

## Automation Model

| Concept | Type | Description |
|---------|------|-------------|
| `Automation` | dataclass | Identity, name, triggers, actions, policy |
| `TriggerDefinition` | frozen dataclass | trigger_id, type (event/schedule/manual), source |
| `AutomationAction` | frozen dataclass | action_id, target (workflow/ai/plugin), input |
| `ExecutionPolicy` | frozen dataclass | allowed_targets, approval, max_executions, environments |
| `AutomationExecution` | dataclass | execution_id, trigger_type, status, timestamps, result/error |

## Triggers

- **Event Trigger**: Activated by platform events (deploy, push, etc.)
- **Schedule Trigger**: Time-based activation via interval or cron
- **Manual Trigger**: Explicit user invocation

Triggers only emit execution requests — they do not execute actions.

## Scheduler

- Interval-based schedule registration
- `is_due()` evaluation
- `mark_run()` tracking
- No external scheduler dependency

## Policies (Deny by Default)

- Allowed capability targets (workflow, ai, plugin)
- Pre-execution policy checks
- `PolicyDeniedError` raised on violation

## Events

- `automation.AutomationCreated`
- `automation.AutomationValidated`
- `automation.AutomationEnabled`
- `automation.AutomationTriggered`
- `automation.AutomationStarted`
- `automation.AutomationCompleted`
- `automation.AutomationFailed`
- `automation.AutomationDisabled`

## Execution History

Tracks: execution_id, automation_id, trigger_type, status, timestamps, result, error

## Integration Points

- **Workflow Runtime**: actions targeting workflows
- **AI Runtime**: actions targeting AI agents
- **Plugin Runtime**: actions targeting plugin capabilities
- **Knowledge Runtime**: policy-aware knowledge access
- **EventBus**: all lifecycle events published
