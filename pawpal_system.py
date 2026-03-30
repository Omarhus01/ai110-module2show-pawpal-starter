from dataclasses import dataclass, field
from datetime import date, time
from typing import Optional


@dataclass
class Task:
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
        pass

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    pet_id: str
    name: str
    species: str
    age_years: int
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_id: str) -> bool:
        pass

    def get_tasks_for_date(self, target_date: date) -> list:
        pass


class Owner:
    def __init__(self, owner_id: str, name: str, daily_time_budget_min: int,
                 preferences: Optional[dict] = None):
        self.owner_id = owner_id
        self.name = name
        self.daily_time_budget_min = daily_time_budget_min
        self.preferences = preferences or {}
        self.pets: list = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet_id: str) -> bool:
        pass

    def get_all_tasks(self) -> list:
        pass


class Scheduler:
    def __init__(self, owner: Owner, max_parallel_tasks: int = 1):
        self.owner = owner
        self.max_parallel_tasks = max_parallel_tasks

    def build_daily_plan(self, target_date: date) -> list:
        pass

    def sort_tasks(self, tasks: list) -> list:
        pass

    def detect_conflicts(self, tasks: list) -> list:
        pass

    def resolve_conflicts(self, tasks: list) -> list:
        pass

    def filter_tasks(self, tasks: list, pet_name: str = None, completed: bool = None) -> list:
        pass

    def explain_plan(self, tasks: list) -> list:
        pass
