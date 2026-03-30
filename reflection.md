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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
