from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from datetime import time, timedelta, datetime

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from typing import Dict, List, Optional, Tuple


@dataclass
class Task:
    """A single pet-related task (feeding, walk, meds, etc.)."""

    name: str
    duration_minutes: int
    priority: int = 0
    earliest_start: Optional[time] = None
    latest_end: Optional[time] = None


@dataclass
class Pet:
    """Pet profile and its tasks."""

    id: str
    name: str
    species: Optional[str] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)


@dataclass
class Constraints:
    """User timeline constraints (sleep/work windows, etc.)."""

    sleep_from: Optional[time] = None
    sleep_to: Optional[time] = None
    work_from: Optional[time] = None
    work_to: Optional[time] = None


@dataclass
class ScheduleEntry:
    """A concrete task placement inside a time slot."""

    start_time: time
    end_time: time
    task: Task


@dataclass
class User:
    """User profile holding preferences, constraints and pets."""

    id: str
    name: str
    constraints: Optional[Constraints] = None
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)


class Scheduler:
    """Scheduler responsible for producing an upkeep schedule."""

    def _to_minutes(self, value: time) -> int:
        return value.hour * 60 + value.minute

    def _to_time(self, minutes: int) -> time:
        minutes = max(0, min(24 * 60 - 1, minutes))
        return (datetime.min + timedelta(minutes=minutes)).time()

    def _get_window(self, constraints: Optional[Constraints]) -> Tuple[int, int]:
        start_minutes = 8 * 60
        end_minutes = 20 * 60

        if constraints and constraints.work_from is not None:
            start_minutes = max(start_minutes, self._to_minutes(constraints.work_from))
        if constraints and constraints.work_to is not None:
            end_minutes = min(end_minutes, self._to_minutes(constraints.work_to))

        return start_minutes, end_minutes

    def _avoid_sleep_window(self, minute: int, constraints: Optional[Constraints]) -> int:
        if not constraints or constraints.sleep_from is None or constraints.sleep_to is None:
            return minute

        sleep_start = self._to_minutes(constraints.sleep_from)
        sleep_end = self._to_minutes(constraints.sleep_to)

        if sleep_start <= sleep_end:
            if sleep_start <= minute < sleep_end:
                return sleep_end
        elif minute >= sleep_start or minute < sleep_end:
            return sleep_end

        return minute

    def generate_schedule(self, user: User) -> Dict[str, List[ScheduleEntry]]:
        """Generate a simple day plan for the user's pets."""

        schedule: Dict[str, List[ScheduleEntry]] = {}
        window_start, window_end = self._get_window(user.constraints)

        for pet in user.pets:
            pet_schedule: List[ScheduleEntry] = []
            current_minute = window_start

            ordered_tasks = sorted(
                pet.tasks,
                key=lambda task: (-task.priority, task.duration_minutes, task.name),
            )

            for task in ordered_tasks:
                task_start = current_minute

                if task.earliest_start is not None:
                    task_start = max(task_start, self._to_minutes(task.earliest_start))

                task_start = self._avoid_sleep_window(task_start, user.constraints)
                task_end = task_start + task.duration_minutes

                if task.latest_end is not None and task_end > self._to_minutes(task.latest_end):
                    continue

                if task_end > window_end:
                    continue

                if user.constraints and user.constraints.sleep_from and user.constraints.sleep_to:
                    sleep_start = self._to_minutes(user.constraints.sleep_from)
                    sleep_end = self._to_minutes(user.constraints.sleep_to)
                    if sleep_start <= sleep_end:
                        overlaps_sleep = task_start < sleep_end and task_end > sleep_start
                    else:
                        overlaps_sleep = task_start >= sleep_start or task_end <= sleep_end

                    if overlaps_sleep:
                        task_start = self._avoid_sleep_window(task_start, user.constraints)
                        task_end = task_start + task.duration_minutes
                        if task_end > window_end:
                            continue

                pet_schedule.append(
                    ScheduleEntry(
                        start_time=self._to_time(task_start),
                        end_time=self._to_time(task_end),
                        task=task,
                    )
                )
                current_minute = task_end

            schedule[pet.id] = pet_schedule

        return schedule


__all__ = ["Task", "Pet", "Constraints", "ScheduleEntry", "User", "Scheduler"]
