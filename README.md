# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Testing PawPal+

Run the full test suite with:

```bash
python -m pytest
```

The test suite covers 6 behaviors:

- **Task completion** — verifies `mark_complete()` correctly updates the task status
- **Task addition** — verifies adding a task to a pet increases the task count
- **Sorting correctness** — verifies tasks added out of order are returned in chronological order
- **Recurrence logic** — verifies that marking a daily task complete auto-creates a new task due the following day
- **Conflict detection** — verifies that two tasks scheduled at the same time are flagged as a conflict
- **Edge case: empty pet** — verifies the scheduler returns an empty list for a pet with no tasks, without crashing

**Confidence Level: ★★★★☆** — Core scheduling behaviors are well covered. The main gap is duration-based overlap detection, which is a known tradeoff documented in `reflection.md`.

---

## Smarter Scheduling

PawPal+ goes beyond a simple task list with four algorithmic features built into the `Scheduler` class:

- **Sorting by time and priority** — Tasks are always displayed in chronological order. When two tasks share the same time slot, the higher-priority task appears first.
- **Filtering** — The schedule can be filtered by pet name or completion status, so owners can focus on one pet at a time or see only what still needs to be done.
- **Recurring task automation** — When a daily or weekly task is marked complete, a new instance is automatically created for the next occurrence using Python's `timedelta`. The owner never has to re-enter repeating tasks.
- **Conflict detection and resolution** — If two tasks are scheduled at the same time, the system warns the owner with the names of the conflicting tasks and automatically shifts the lower-priority one forward by 30 minutes.

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
