from datetime import date, time
from pawpal_system import Task, Pet, Owner, Scheduler

# ── Setup ──────────────────────────────────────────────────────────────────────

owner = Owner(
    owner_id="o1",
    name="Omar",
    daily_time_budget_min=120,
    preferences={"prefer_morning": True}
)

# Pets
buddy = Pet(pet_id="p1", name="Buddy", species="Dog", age_years=3)
luna  = Pet(pet_id="p2", name="Luna",  species="Cat", age_years=2)

owner.add_pet(buddy)
owner.add_pet(luna)

# Tasks for Buddy (added OUT OF ORDER to test sorting)
buddy.add_task(Task(
    task_id="t3", title="Evening Feed", category="feeding",
    duration_min=10, priority=4,
    scheduled_time=time(18, 0),
    recurrence="daily", due_date=date.today()
))
buddy.add_task(Task(
    task_id="t1", title="Morning Walk", category="exercise",
    duration_min=30, priority=3,
    scheduled_time=time(8, 0),
    recurrence="daily", due_date=date.today()
))
buddy.add_task(Task(
    task_id="t2", title="Flea Medication", category="medication",
    duration_min=5, priority=5,
    scheduled_time=time(9, 0),
    recurrence="weekly", due_date=date.today()
))

# Tasks for Luna (added OUT OF ORDER to test sorting)
luna.add_task(Task(
    task_id="t5", title="Grooming", category="grooming",
    duration_min=20, priority=2,
    scheduled_time=time(11, 0),
    recurrence="weekly", due_date=date.today()
))
luna.add_task(Task(
    task_id="t4", title="Breakfast Feed", category="feeding",
    duration_min=10, priority=4,
    scheduled_time=time(8, 0),
    recurrence="daily", due_date=date.today()
))

# Intentional conflict: two tasks at the same time (08:00)
buddy.add_task(Task(
    task_id="t6", title="Vet Check-in", category="medication",
    duration_min=15, priority=5,
    scheduled_time=time(8, 0),
    recurrence="once", due_date=date.today()
))

# ── Build Schedule ─────────────────────────────────────────────────────────────

scheduler = Scheduler(owner=owner)
today = date.today()
plan = scheduler.build_daily_plan(today)

# ── Conflict Check ─────────────────────────────────────────────────────────────

conflicts = scheduler.detect_conflicts(plan)
if conflicts:
    print("=" * 50)
    print("  WARNING: Schedule Conflicts Detected!")
    print("=" * 50)
    for task_a, task_b in conflicts:
        print(f"  CONFLICT at {task_a.scheduled_time.strftime('%H:%M')}:")
        print(f"    - '{task_a.title}' vs '{task_b.title}'")
        print(f"    -> '{task_b.title}' will be shifted forward by 30 minutes.")
    print()
    plan = scheduler.resolve_conflicts(plan)

# ── Print Today's Schedule ─────────────────────────────────────────────────────

print("=" * 50)
print(f"  PawPal+ - Today's Schedule ({today})")
print("=" * 50)

for i, task in enumerate(plan, 1):
    status = "[DONE]" if task.is_completed else "[    ]"
    pet_name = next(
        (p.name for p in owner.pets if any(t.task_id == task.task_id for t in p.tasks)),
        "Unknown"
    )
    print(f"{i}. {status} [{task.scheduled_time.strftime('%H:%M')}] "
          f"{task.title} ({pet_name}) - {task.duration_min} min | "
          f"Priority: {task.priority} | {task.recurrence.capitalize()}")

print("=" * 50)
print("\nPlan Explanation:")
for note in scheduler.explain_plan(plan):
    print(f"  - {note}")

# ── Recurring Task Demo ────────────────────────────────────────────────────────

print("\n" + "=" * 50)
print("  Recurring Task: Mark 'Morning Walk' complete")
print("=" * 50)
new_task = scheduler.mark_task_complete("t1")
if new_task:
    print(f"  'Morning Walk' marked done.")
    print(f"  New task created: '{new_task.title}' due on {new_task.due_date}")
else:
    print("  Task not recurring - no new task created.")

# ── Filter Demo ────────────────────────────────────────────────────────────────

print("\n" + "=" * 50)
print("  Filter: Buddy's tasks only")
print("=" * 50)
buddy_tasks = scheduler.filter_tasks(plan, pet_name="Buddy")
for task in buddy_tasks:
    print(f"  - [{task.scheduled_time.strftime('%H:%M')}] {task.title}")

print("\n" + "=" * 50)
print("  Filter: Incomplete tasks only")
print("=" * 50)
incomplete = scheduler.filter_tasks(plan, completed=False)
for task in incomplete:
    print(f"  - [{task.scheduled_time.strftime('%H:%M')}] {task.title} (not done)")
