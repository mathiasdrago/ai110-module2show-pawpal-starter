from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time
from typing import Dict, List, Optional, Tuple


@dataclass
class Task:
    """A single pet activity."""

    description: str
    duration_minutes: int
    frequency: str = "once"
    completed: bool = False
    scheduled_time: Optional[time] = None

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        self.completed = False


@dataclass
class Pet:
    """Stores pet details and its tasks."""

    id: str
    name: str
    species: Optional[str] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, description: str) -> bool:
        """Remove a task by description, return True if found."""
        for index, task in enumerate(self.tasks):
            if task.description == description:
                del self.tasks[index]
                return True
        return False

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.completed]


@dataclass
class Owner:
    """Manages multiple pets and exposes all their tasks."""

    id: str
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> bool:
        """Remove a pet by ID, return True if found."""
        for index, pet in enumerate(self.pets):
            if pet.id == pet_id:
                del self.pets[index]
                return True
        return False

    def get_all_tasks(self, include_completed: bool = False) -> List[Tuple[Pet, Task]]:
        """Return all tasks from all pets, optionally including completed ones."""
        all_tasks: List[Tuple[Pet, Task]] = []
        for pet in self.pets:
            for task in pet.tasks:
                if include_completed or not task.completed:
                    all_tasks.append((pet, task))
        return all_tasks


class Scheduler:
    """The brain that retrieves, organizes, and manages tasks across pets."""

    def collect_tasks(self, owner: Owner, include_completed: bool = False) -> List[Tuple[Pet, Task]]:
        """Retrieve every task from every pet owned by the owner."""

        return owner.get_all_tasks(include_completed=include_completed)

    def organize_tasks(self, owner: Owner) -> Dict[str, List[Task]]:
        """Group pending tasks by pet and sort them by priority, duration, and name."""

        organized: Dict[str, List[Task]] = {}
        for pet in owner.pets:
            organized[pet.id] = sorted(
                pet.get_pending_tasks(),
                key=lambda task: (task.duration_minutes, task.description),
            )
        return organized

    def get_daily_plan(self, owner: Owner) -> List[Dict[str, object]]:
        """Flatten all pending tasks into one owner-wide plan."""

        plan: List[Dict[str, object]] = []
        for pet, task in self.collect_tasks(owner, include_completed=False):
            plan.append(
                {
                    "pet_id": pet.id,
                    "pet_name": pet.name,
                    "task": task,
                }
            )
        return plan


__all__ = ["Task", "Pet", "Owner", "Scheduler"]
