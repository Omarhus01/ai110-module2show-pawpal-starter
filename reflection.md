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

A future improvement would be to calculate `end_time = scheduled_time + duration_min` for each task and flag any pair where one task's window overlaps another's.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
