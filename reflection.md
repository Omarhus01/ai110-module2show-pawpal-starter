# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Before writing any code, I identified three core actions a user needs to perform in PawPal+:

1. **Add a pet** — The user should be able to enter owner information and register one or more pets with basic details like name and species. This is the starting point for everything else in the app.

2. **Add and edit tasks** — The user should be able to create care tasks for each pet, such as walks, feedings, medications, or grooming sessions. Each task should have a type, a scheduled time, a duration, and a priority level so the system can make smart decisions.

3. **Generate and view today's schedule** — The user should be able to request a daily plan that organizes all tasks across their pets in a logical order based on priority and time constraints. The schedule should be clear and explain why tasks were arranged the way they were.

The system is built around four classes, each with a single clear responsibility:

- **Task** — Represents one care activity for a pet. It holds all the details needed to schedule it: title, category, duration, priority, scheduled time, recurrence rule, due date, and completion status. It knows how to check if it is due on a given date and how to mark itself complete.

- **Pet** — Represents a single animal owned by the user. It stores basic info (name, species, age) and owns a list of Task objects. It is responsible for adding, removing, and retrieving tasks filtered by date.

- **Owner** — Represents the human user. It holds a daily time budget and personal preferences, and manages a list of Pet objects. It provides a single entry point to retrieve all tasks across all pets, which makes it easy for the Scheduler to access everything it needs.

- **Scheduler** — The brain of the system. It takes an Owner and builds an optimized daily plan by sorting tasks, detecting time conflicts, resolving them, and explaining why tasks were arranged the way they were. It does not store tasks itself — it always pulls them from the Owner's pets.

**b. Design changes**

After reviewing the skeleton, two changes were made based on potential logic bottlenecks:

1. **Added `next_due_date` to `Task`** — The original skeleton had no way to track when a recurring task should next appear after being marked complete. Without this field, the recurrence logic in Phase 4 would have no place to store the rescheduled date.

2. **Added `filter_tasks()` to `Scheduler`** — The original skeleton only had `sort_tasks()` but the Phase 4 requirements call for filtering by pet name and completion status. Adding this method stub now keeps the Scheduler's interface complete and avoids a bottleneck later.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers three constraints when building the daily plan:

1. **Scheduled time** — Tasks are sorted chronologically so the owner sees them in the order they need to happen throughout the day.
2. **Priority (1–5)** — When two tasks share the same time slot, higher priority tasks are placed first. This ensures critical tasks like medications are never buried behind lower-priority ones like grooming.
3. **Recurrence** — The scheduler only includes tasks that are due on the target date based on their recurrence rule (once, daily, weekly), so the owner is never shown tasks that do not apply to today.

Time was chosen as the primary sort key because a daily schedule must be chronological to be usable. Priority was chosen as the secondary key because it resolves ties in a meaningful way — if two things are due at the same time, the more important one should come first.

**b. Tradeoffs**

The scheduler's conflict detection only flags tasks that share the **exact same start time** — it does not check for overlapping durations. For example, if "Morning Walk" starts at 08:00 and lasts 30 minutes, and "Vet Check-in" starts at 08:15, the system will not flag this as a conflict even though the two tasks overlap in real time.

This tradeoff is reasonable for this scenario because:
1. Most pet care tasks are short and sequential — owners typically do not run two tasks in parallel.
2. Checking for duration overlap would require knowing the end time of every task and comparing all pairs, which adds complexity without much benefit for a basic daily planner.
3. A warning-based system (rather than a hard block) already gives the owner enough information to adjust manually if needed.

**Known bug discovered during testing:** The conflict resolution logic always shifts the conflicting task forward by a fixed 30 minutes, regardless of how long the first task actually is. During manual testing, a "Morning Walk" for Jax was set to 60 minutes starting at 08:00. When "home play" for kitty was also scheduled at 08:00, the system shifted kitty's task to 08:30 — which is still inside the 60-minute walk window. The correct behavior would be to shift the conflicting task forward by the full duration of the blocking task (in this case, 60 minutes to 09:00). This is a logic gap that should be fixed in the next iteration by replacing the hardcoded 30-minute shift with `scheduled_time + duration_min` of the blocking task.

A future improvement would be to calculate `end_time = scheduled_time + duration_min` for each task and use that as both the conflict detection threshold and the resolution offset.

---

## 3. AI Collaboration

**a. How you used AI**

AI was used across every phase of the project in different ways:

- **Design brainstorming (Phase 1)** — AI helped generate the initial Mermaid.js UML diagram and suggested adding `daily_time_budget_min` to Owner and `max_parallel_tasks` to Scheduler, which made the design more realistic.
- **Scaffolding (Phase 2)** — Agent mode was used to flesh out the full implementation of all four classes from the skeleton, saving time on boilerplate while keeping the architecture decisions in human hands.
- **Algorithmic logic (Phase 4)** — AI suggested using a `lambda` with Python's `sorted()` for the time-based sort, and using `timedelta` for the recurring task date calculation.
- **Test generation (Phase 5)** — AI drafted the test suite structure, which was then reviewed and adjusted to ensure the tests were meaningful and not just checking obvious things.

The most helpful prompts were specific and context-rich — for example, asking "how should the Scheduler retrieve all tasks from the Owner's pets?" produced a much more useful answer than a vague question like "how do I connect these classes?"

**b. Judgment and verification**

When AI suggested a more "Pythonic" version of `detect_conflicts()` using `itertools.combinations`, the suggestion was reviewed and rejected. While the `itertools` version was shorter, it checked every pair of tasks instead of using a dictionary to track seen times, making it harder to read and slightly less efficient. The original dictionary-based version was kept because clarity matters more than cleverness in code that others will maintain.

The AI suggestion was verified by running both versions manually in the terminal and comparing their outputs — they produced the same results, confirming the choice to keep the readable version was safe.

---

## 4. Testing and Verification

**a. What you tested**

Six behaviors were tested in the automated suite:

1. `mark_complete()` correctly flips the task's completion status
2. Adding a task to a pet increases the pet's task count
3. Tasks added out of chronological order are returned in the correct sorted order
4. Marking a daily task complete creates a new task due the following day
5. Two tasks at the same time are correctly flagged as a conflict
6. A pet with no tasks returns an empty schedule without crashing

These tests were important because they cover the core promise of the app — that the schedule will always be in the right order, that conflicts will be caught, and that recurring tasks will never be forgotten.

**b. Confidence**

Confidence level: **★★★★☆**

The core behaviors are solid and all 6 tests pass. However, the known bug in conflict resolution (shifting by a fixed 30 minutes instead of the blocking task's full duration) reduces confidence. If the next thing to test were added, the first would be: does `resolve_conflicts()` correctly shift tasks by the full duration of the blocking task, not a hardcoded value? That test would currently fail and point directly to the bug.

---

## 5. Reflection

**a. What went well**

The "CLI-first" workflow was the best decision made in this project. Building and verifying all the logic in `main.py` before touching the Streamlit UI meant that by the time `app.py` was connected, the backend was already proven to work. This made the UI integration in Phase 3 fast and nearly bug-free — there was no uncertainty about whether a problem was in the logic or the UI, because the logic had already been tested in the terminal.

**b. What you would improve**

The conflict resolution logic would be the first thing to fix in the next iteration. The hardcoded 30-minute shift should be replaced with a dynamic shift based on the blocking task's actual duration. For example, if "Morning Walk" lasts 60 minutes starting at 08:00, any conflicting task should be pushed to 09:00, not 08:30. This would make the scheduler genuinely safe rather than just approximately correct.

**c. Key takeaway**

The most important thing learned was that AI is a powerful collaborator but a poor architect. AI could generate code, suggest methods, and draft tests quickly — but it had no way of knowing which tradeoffs were acceptable, which design decisions matched the project's goals, or when a "cleaner" suggestion would actually make the system harder to understand. The human role was not just to type prompts but to stay in charge of every design decision, review every suggestion critically, and catch the things AI missed — like the conflict resolution bug that only surfaced during real manual testing.
