import pytest
from datetime import date, time
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
    return Owner(owner_id="o1", name="Omar", daily_time_budget_min=120)


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
