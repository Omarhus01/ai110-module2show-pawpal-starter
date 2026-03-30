from dataclasses import dataclass, field
from datetime import date, time, timedelta
from typing import Optional


@dataclass
class Task:
    """Represents a single care activity scheduled for a pet."""

    task_id: str
    title: str
    category: str
    duration_min: int
    priority: int
    scheduled_time: time
    recurrence: str
    due_date: date
    is_completed: bool = False
    next_due_date: Optional[date] = None

    def is_due_on(self, target_date: date) -> bool:
        """Return True if this task is due on the given date based on its recurrence rule."""
        if self.recurrence == "daily":
            return True
        if self.recurrence == "weekly":
            return self.due_date.weekday() == target_date.weekday()
        return self.due_date == target_date

    def mark_complete(self) -> None:
        """Mark the task as completed and calculate the next due date for recurring tasks."""
        self.is_completed = True
        if self.recurrence == "daily":
            self.next_due_date = date.today() + timedelta(days=1)
        elif self.recurrence == "weekly":
            self.next_due_date = date.today() + timedelta(weeks=1)
        else:
            self.next_due_date = None


@dataclass
class Pet:
    """Represents a pet owned by the user, along with its list of care tasks."""

    pet_id: str
    name: str
    species: str
    age_years: int
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by ID; return True if found and removed, False otherwise."""
        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task)
                return True
        return False

    def get_tasks_for_date(self, target_date: date) -> list:
        """Return all tasks that are due on the given date."""
        return [task for task in self.tasks if task.is_due_on(target_date)]


class Owner:
    """Represents the pet owner who manages multiple pets and has a daily time budget."""

    def __init__(self, owner_id: str, name: str, daily_time_budget_min: int,
                 preferences: Optional[dict] = None):
        self.owner_id = owner_id
        self.name = name
        self.daily_time_budget_min = daily_time_budget_min
        self.preferences = preferences or {}
        self.pets: list = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's list of pets."""
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> bool:
        """Remove a pet by ID; return True if found and removed, False otherwise."""
        for pet in self.pets:
            if pet.pet_id == pet_id:
                self.pets.remove(pet)
                return True
        return False

    def get_all_tasks(self) -> list:
        """Return a flat list of all tasks across all of the owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    """Builds and manages the daily care plan for all pets belonging to an owner."""

    def __init__(self, owner: Owner, max_parallel_tasks: int = 1):
        self.owner = owner
        self.max_parallel_tasks = max_parallel_tasks

    def build_daily_plan(self, target_date: date) -> list:
        """Collect and sort all tasks due on the target date across all pets."""
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend(pet.get_tasks_for_date(target_date))
        return self.sort_tasks(all_tasks)

    def sort_tasks(self, tasks: list) -> list:
        """Sort tasks by scheduled time, then by descending priority."""
        return sorted(tasks, key=lambda t: (t.scheduled_time, -t.priority))

    def detect_conflicts(self, tasks: list) -> list:
        """Return a list of (task_a, task_b) pairs that share the same scheduled time."""
        conflicts = []
        seen_times = {}
        for task in tasks:
            t = task.scheduled_time
            if t in seen_times:
                conflicts.append((seen_times[t], task))
            else:
                seen_times[t] = task
        return conflicts

    def resolve_conflicts(self, tasks: list) -> list:
        """Shift conflicting tasks forward by 30 minutes to eliminate time collisions."""
        conflicts = self.detect_conflicts(tasks)
        resolved = list(tasks)
        for task_a, task_b in conflicts:
            if task_b in resolved:
                idx = resolved.index(task_b)
                original = task_b.scheduled_time
                new_hour = original.hour
                new_minute = original.minute + 30
                if new_minute >= 60:
                    new_hour += 1
                    new_minute -= 60
                resolved[idx].scheduled_time = time(new_hour, new_minute)
        return resolved

    def filter_tasks(self, tasks: list, pet_name: str = None, completed: bool = None) -> list:
        """Filter tasks by pet name and/or completion status."""
        result = tasks
        if pet_name is not None:
            pet_task_ids = set()
            for pet in self.owner.pets:
                if pet.name.lower() == pet_name.lower():
                    pet_task_ids.update(t.task_id for t in pet.tasks)
            result = [t for t in result if t.task_id in pet_task_ids]
        if completed is not None:
            result = [t for t in result if t.is_completed == completed]
        return result

    def explain_plan(self, tasks: list) -> list:
        """Return a human-readable explanation string for each task in the plan."""
        explanations = []
        for task in tasks:
            reason = (
                f"'{task.title}' scheduled at {task.scheduled_time.strftime('%H:%M')} "
                f"(priority {task.priority}, {task.duration_min} min, {task.recurrence})"
            )
            explanations.append(reason)
        return explanations
