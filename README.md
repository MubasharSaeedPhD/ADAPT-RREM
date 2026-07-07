# ADAPT — Runtime Risk-Aware Execution Monitoring for LLM-Based Robotic Task and Motion Planning with Experience-Driven Adaptation

## Abstract

Large language model (LLM)-based robotic task planning has demonstrated
impressive generalisation, but remains prone to constraint violations arising
from execution-time world-state changes that planning-time validators cannot
anticipate. We present **ADAPT** — a five-module closed-loop architecture
that integrates a novel Runtime Risk-Aware Execution Monitor (RREM) with
experience-driven adaptation. The RREM evaluates five typed constraint
categories (reachability, collision safety, grasp feasibility, spatial
constraints, and execution risk) through a structured binary Q&A loop
immediately before each action commitment, using the live simulator state
rather than planning-time assumptions. A Semantic Validation Module (SVM)
provides plan-level causal consistency checking, and an Experience
Consolidation Module (ECM) accumulates validated plans and RREM resolution
patterns for reuse across tasks. Evaluated on 10 RLBench tasks (500 trials),
ADAPT achieves 93.0% mean success rate, outperforming the strongest baseline
by +24.3 percentage points, with zero false negatives across all
safety-critical geometric constraint categories.

---

## System Overview

```
┌─────────────────────────────────────────────────────┐
│                     ADAPT Pipeline                   │
│                                                      │
│  Task T                                              │
│    │                                                 │
│    ▼                                                 │
│  ┌─────────┐    ┌─────┐    ┌─────┐                  │
│  │Mediator │───▶│ HDM │───▶│ SVM │                  │
│  │  (ECM)  │    └─────┘    └──┬──┘                  │
│  └────┬────┘                  │ plan π               │
│       │                       ▼                      │
│       │              ┌──────────────┐                │
│       │◀─────────────│     RREM     │                │
│       │  F_i (fail)  │  5-category  │                │
│       │              │   Q&A loop   │                │
│       │              └──────────────┘                │
│       │                    │ approved                 │
│       │                    ▼                          │
│       │              Execute a_i                      │
│       │                    │                          │
│       └────────────────────┘                         │
│         ECM.store(T, π, outcome)                     │
└─────────────────────────────────────────────────────┘
```

---

## RREM Question Templates

The RREM evaluates **5 constraint categories** using action-type-specific
question templates. Each template is instantiated with live robot state
before action execution.

### Category 1 — Reachability

Checks whether the end-effector can reach the target from current configuration.

```
Template (grasp):
"EE is at {ee_pos}, workspace [{ws_min},{ws_max}].
Is EE within valid workspace to approach and grasp '{target}'?"

Template (slide):
"EE is at {ee_pos}, workspace [{ws_min},{ws_max}].
Is EE within reach to slide '{target}'?"
```

### Category 2 — Collision Safety

Checks joint velocity for collision proxy detection.

```
Template (generic):
"The arm's maximum joint velocity is {joint_vel:.6f} rad/s.
Is this below the safe threshold of 1.0 rad/s,
indicating no collision is occurring during '{action}'?"
```

### Category 3 — Grasp Feasibility

Checks gripper state appropriateness for action phase.

```
Template (grasp):
"Gripper openness={gripper_open:.2f}.
For GRASPING '{target}', gripper should be OPEN (>0.5).
Is the gripper correctly open for approach?"

Template (place):
"Gripper openness={gripper_open:.2f}.
For PLACING onto '{target}', gripper should be CLOSED (<0.3).
Is the gripper closed with object held?"
```

### Category 4 — Spatial Constraints

Checks end-effector proximity to workspace center.

```
Template (generic):
"EE at {ee_pos}, ws_center={ws_center}.
Is EE within acceptable spatial range of the workspace
center for action on '{target}'?"
```

### Category 5 — Execution Risk

Contextual risk estimation from action history and ECM patterns.
*(No deterministic formula — LLM reasoning required)*

```
Template (generic):
"Joint vel={joint_vel:.6f} rad/s, gripper={gripper_open:.2f}.
Is execution risk acceptable to perform '{action}'
given current robot state?"
```

---

## RREM System Prompt

```
You are the Runtime Risk-Aware Execution Monitor (RREM) of a
robotic manipulation system. Your job is to answer YES or NO to
specific constraint questions about the robot's current state.

Answer ONLY with JSON: {"answer": true/false, "explanation": "brief reason"}
Base answers STRICTLY on provided sensor data.
Be conservative — if uncertain, answer false.

IMPORTANT: At task START, gripper OPEN (openness=1.0) is CORRECT
for grasping tasks — the robot has not yet grasped the object.
```

---

## HDM Prompt Structure

The Hierarchical Decomposition Module uses a three-part prompt:

```
Part 1 — System role:
  "You are a robot task planner. Generate a step-by-step plan
   using only the provided primitive action vocabulary A."

Part 2 — State block:
  Symbolic state φ(s): object locations, gripper state,
  geometric scene summary σ(s)

Part 3 — Task instruction:
  T = "put rubbish in bin"

Part 4 (replanning only) — RREM failure report:
  F_i: failed constraint category, violated condition,
  recommended correction type
```

---

## SVM Validation Rules

The Semantic Validation Module checks plans in three stages:

### Stage 1 — Precondition Checking

| Action | Required Preconditions |
|--------|----------------------|
| grasp | gripper_empty=True, object_visible=True |
| place | holding_object=True, surface_clear=True |
| open_drawer | drawer_closed=True, gripper_empty=True |
| close_drawer | drawer_open=True |
| stack | holding_object=True, target_clear=True |
| put_in | holding_object=True, container_open=True |

### Stage 2 — Causal Consistency (DFS)

| Action | Requires Prior |
|--------|---------------|
| place | grasp or pick_and_lift |
| stack | grasp or pick_and_lift |
| put_in | grasp or pick_and_lift |
| close_drawer | open_drawer |

### Stage 3 — Geometric Feasibility

- EE position within workspace bounds ± 5cm
- Joint velocity below collision threshold (2.0 rad/s)

---

## RREM Base Templates (from Paper Section 4.4.3)

The five base templates exactly as defined in the paper:

```
REACH: "Can the end-effector reach {target_pose}
        from joint configuration {q}?"

COLL:  "Is the approach path to {target_pose}
        free of obstacles given scene {scene_summary}?"

GRASP: "Is {object_name} at pose {obj_pose}
        graspable with gripper state {gripper_state}?"

SPAT:  "Is the end-effector within tolerance
        [{dist_tol}, {angle_tol}] for {action_type}?"

EXEC:  "Based on prior experience with {action_type},
        does {state_summary} indicate acceptable execution risk?"
```

Parameters in braces are substituted from:
- `θ(a_i)` — action parameters
- `φ(s)` — symbolic state predicates
- `σ(s)` — geometric observation summary

> The full 12-variant library (60 templates total) is in `rrem_templates.py`

---

## Micro-Correction Protocol

When RREM detects a constraint violation, the Mediator applies:

```
If violation is RECOVERABLE (micro-correction):
  1. Generate corrective action μ
     (e.g., adjust gripper pose, retry with offset)
  2. Re-evaluate RREM constraints
  3. Retry up to K_max = 3 times
  4. If still failing → trigger localised replanning

If violation is NON-RECOVERABLE (CPV):
  1. Send structured failure report F_i to Mediator
  2. Mediator invokes HDM.LocalReplan(T, s_{i-1}, F_i)
  3. Preserve valid plan prefix and suffix
  4. Regenerate only the failed sub-sequence
```

**Failure report structure F_i:**
```json
{
  "action": "grasp the rubbish",
  "failed_categories": ["grasp", "spatial"],
  "constraint_answers": {
    "reachability": true,
    "collision": true,
    "grasp": false,
    "spatial": false,
    "exec_risk": true
  },
  "recovery_type": "localised_replan",
  "retry_count": 3
}
```

---

## Scene Summary Format σ(s)

The observation summary passed to RREM Q&A:

```json
{
  "ee_pos": [x, y, z],
  "gripper_open": 0.0,
  "gripper_pos": [x, y, z],
  "joint_vel": 0.004311,
  "ws_min": [-0.275, -0.655, 0.752],
  "ws_max": [0.775, 0.655, 1.752],
  "ws_center": [0.25, 0.0, 1.252]
}
```

---

## ECM Memory Protocol

```
TES (Task Experience Store):
  Key    : MD5(task_name + instruction)
  Value  : {plan, confidence, count}
  Reuse  : confidence >= θ = 0.85 → skip HDM
  Update : EMA(α=0.3) after each execution

EES (Execution Experience Store):
  Stores : per-action RREM Q&A resolution patterns
  Written: incrementally after each successful resolution
  Used   : prime template instantiation for similar actions
```

---

---

## Repository Contents

```
ADAPT-RREM/
├── README.md                  ← This file
├── rrem_templates.py          ← Complete 60-variant template library
│                                (5 categories × 12 action types)
├── svm.py                     ← Semantic Validation Module
│                                (3-stage plan validation)
└── [Full implementation]      ← Released after publication
    ├── adapt_complete.py      ← Full ADAPT pipeline
    ├── ecm.py                 ← Experience Consolidation Module
    └── requirements.txt
```

> **Note:** Complete implementation code including the full ADAPT
> pipeline, ECM module, and evaluation scripts will be released
> upon journal publication at this repository.

---
## Complete Code will be released soon
## Citation

```bibtex
@article{saeed2025adapt,
  title   = {Runtime Risk-Aware Execution Monitoring for LLM-Based
             Robotic Task and Motion Planning with Experience-Driven
             Adaptation},
  author  = {Saeed, Mubashar and Lu, Mingming and Awan, Arshad},
  journal = {Expert Systems with Applications},
  year    = {2025},
  note    = {Under review}
}
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Contact

For questions: **mubashar.saeed@csu.edu.cn**
