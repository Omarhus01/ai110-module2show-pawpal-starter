import pytest
from datetime import date, time, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_task():
    return Task(
        task_id="t1",
        title="Morning Walk",
        category="exercise",
        duration_min=30,
        priority=3,
        scheduled_time=time(8, 0),
        recurrence="daily",
        due_date=date.today()
    )

@pytest.fixture
def sample_pet():
    return Pet(pet_id="p1", name="Buddy", species="Dog", age_years=3)

@pytest.fixture
def sample_owner():
    owner = Owner(owner_id="o1", name="Omar", daily_time_budget_min=120)
    pet = Pet(pet_id="p1", name="Buddy", species="Dog", age_years=3)
    owner.add_pet(pet)
    return owner

@pytest.fixture
def scheduler(sample_owner):
    return Scheduler(owner=sample_owner)


# ── Test 1: Task Completion ────────────────────────────────────────────────────

def test_mark_complete_changes_status(sample_task):
    assert sample_task.is_completed is False
    sample_task.mark_complete()
    assert sample_task.is_completed is True


# ── Test 2: Task Addition ──────────────────────────────────────────────────────

def test_add_task_increases_count(sample_pet, sample_task):
    assert len(sample_pet.tasks) == 0
    sample_pet.add_task(sample_task)
    assert len(sample_pet.tasks) == 1


# ── Test 3: Sorting Correctness ────────────────────────────────────────────────

def test_sort_tasks_returns_chronological_order(scheduler, sample_owner):
    pet = sample_owner.pets[0]

    # Add tasks out of order
    pet.add_task(Task(
        task_id="t3", title="Evening Feed", category="feeding",
        duration_min=10, priority=4,
        scheduled_time=time(18, 0),
        recurrence="daily", due_date=date.today()
    ))
    pet.add_task(Task(
        task_id="t1", title="Morning Walk", category="exercise",
        duration_min=30, priority=3,
        scheduled_time=time(8, 0),
        recurrence="daily", due_date=date.today()
    ))
    pet.add_task(Task(
        task_id="t2", title="Medication", category="medication",
        duration_min=5, priority=5,
        scheduled_time=time(9, 0),
        recurrence="daily", due_date=date.today()
    ))

    plan = scheduler.build_daily_plan(date.today())
    times = [t.scheduled_time for t in plan]
    assert times == sorted(times), "Tasks are not sorted in chronological order"


# ── Test 4: Recurrence Logic ───────────────────────────────────────────────────

def test_daily_task_creates_new_task_for_tomorrow(scheduler, sample_owner):
    pet = sample_owner.pets[0]
    pet.add_task(Task(
        task_id="t1", title="Morning Walk", category="exercise",
        duration_min=30, priority=3,
        scheduled_time=time(8, 0),
        recurrence="daily", due_date=date.today()
    ))

    initial_count = len(pet.tasks)
    new_task = scheduler.mark_task_complete("t1")

    assert new_task is not None, "No new task was created for recurring task"
    assert new_task.due_date == date.today() + timedelta(days=1), "New task not due tomorrow"
    assert len(pet.tasks) == initial_count + 1, "Pet task count did not increase"


# ── Test 5: Conflict Detection ─────────────────────────────────────────────────

def test_detect_conflicts_flags_duplicate_times(scheduler, sample_owner):
    pet = sample_owner.pets[0]

    task_a = Task(
        task_id="t1", title="Morning Walk", category="exercise",
        duration_min=30, priority=3,
        scheduled_time=time(8, 0),
        recurrence="daily", due_date=date.today()
    )
    task_b = Task(
        task_id="t2", title="Vet Check-in", category="medication",
        duration_min=15, priority=5,
        scheduled_time=time(8, 0),
        recurrence="once", due_date=date.today()
    )
    pet.add_task(task_a)
    pet.add_task(task_b)

    plan = scheduler.build_daily_plan(date.today())
    conflicts = scheduler.detect_conflicts(plan)

    assert len(conflicts) == 1, "Expected 1 conflict but got a different number"
    assert task_a in conflicts[0] and task_b in conflicts[0], "Wrong tasks flagged as conflict"


# ── Test 6: Pet With No Tasks ──────────────────────────────────────────────────

def test_empty_pet_returns_empty_schedule(scheduler):
    plan = scheduler.build_daily_plan(date.today())
    assert plan == [], "Expected empty schedule for pet with no tasks"
