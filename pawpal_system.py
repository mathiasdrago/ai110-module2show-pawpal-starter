from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
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

    def create_next_occurrence(self) -> Optional[Task]:
        """Create a new task instance for the next occurrence if this is a recurring task.
        
        Uses timedelta arithmetic to calculate the next occurrence date:
        - Daily: adds 1 day to the current scheduled time
        - Weekly: adds 7 days to the current scheduled time
        - Once: returns None (no recurrence)
        
        Time Complexity: O(1) - constant time arithmetic operations.
        Space Complexity: O(1) - creates at most one new Task object.
        
        Returns:
            A new Task instance for the next occurrence, or None if frequency is "once".
        """
        if self.frequency == "once":
            return None
        
        if self.frequency == "daily":
            # Calculate next day's time
            if self.scheduled_time is not None:
                from datetime import datetime, timedelta
                today = datetime.combine(datetime.today().date(), self.scheduled_time)
                next_day = today + timedelta(days=1)
                return Task(
                    description=self.description,
                    duration_minutes=self.duration_minutes,
                    frequency=self.frequency,
                    completed=False,
                    scheduled_time=next_day.time()
                )
            else:
                # If no scheduled time, just create a new unscheduled task
                return Task(
                    description=self.description,
                    duration_minutes=self.duration_minutes,
                    frequency=self.frequency,
                    completed=False,
                    scheduled_time=None
                )
        
        if self.frequency == "weekly":
            # Calculate next week's time
            if self.scheduled_time is not None:
                from datetime import datetime, timedelta
                today = datetime.combine(datetime.today().date(), self.scheduled_time)
                next_week = today + timedelta(weeks=1)
                return Task(
                    description=self.description,
                    duration_minutes=self.duration_minutes,
                    frequency=self.frequency,
                    completed=False,
                    scheduled_time=next_week.time()
                )
            else:
                # If no scheduled time, just create a new unscheduled task
                return Task(
                    description=self.description,
                    duration_minutes=self.duration_minutes,
                    frequency=self.frequency,
                    completed=False,
                    scheduled_time=None
                )
        
        return None


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

    def complete_task(self, task_description: str) -> Optional[Task]:
        """Mark a task as complete and create next occurrence if recurring.
        
        Searches for the first incomplete task matching the description,
        marks it complete, and automatically generates the next occurrence
        if the task has daily or weekly frequency.
        
        Time Complexity: O(n) where n is the number of tasks in this pet's task list.
        Space Complexity: O(1) - modifies existing task and optionally creates one new task.
        
        Args:
            task_description: The description of the task to complete.
        
        Returns:
            The next occurrence task if created, None otherwise.
        """
        for task in self.tasks:
            if task.description == task_description and not task.completed:
                task.mark_complete()
                next_task = task.create_next_occurrence()
                if next_task is not None:
                    self.add_task(next_task)
                return next_task
        return None


@dataclass
class Owner:
    """Manages multiple pets and exposes all their tasks."""

    id: str
    name: str
    pets: List[Pet] = field(default_factory=list)
    work_start: time = time(9, 0)
    work_end: time = time(17, 0)
    sleep_start: time = time(22, 0)
    sleep_end: time = time(7, 0)

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

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their scheduled_time attribute using Timsort algorithm.
        
        Tasks with scheduled_time=None are placed at the end by using a sentinel time value.
        Uses Python's built-in sorted() with a lambda function as the key to sort by time objects.
        
        Time Complexity: O(n log n) where n is the number of tasks.
        Space Complexity: O(n) for the sorted result.
        
        Args:
            tasks: List of Task objects to sort.
        
        Returns:
            A new list of tasks sorted chronologically by scheduled_time.
        """
        return sorted(tasks, key=lambda task: task.scheduled_time if task.scheduled_time is not None else time(23, 59, 59))

    def filter_tasks(self, owner: Owner, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Tuple[Pet, Task]]:
        """Filter tasks by completion status and/or pet name using linear search.
        
        Iterates through all tasks and applies filter conditions sequentially.
        Both filters can be used together or independently.
        
        Time Complexity: O(n) where n is the total number of tasks.
        Space Complexity: O(n) for the filtered result.
        
        Args:
            owner: The owner whose tasks to filter
            completed: If True, return only completed tasks. If False, return only incomplete tasks. If None, return all.
            pet_name: If provided, return only tasks for pets matching this name. If None, return tasks for all pets.
        
        Returns:
            List of (pet, task) tuples matching the filter criteria.
        """
        all_tasks = owner.get_all_tasks(include_completed=True)
        
        filtered = []
        for pet, task in all_tasks:
            # Filter by completion status
            if completed is not None and task.completed != completed:
                continue
            # Filter by pet name
            if pet_name is not None and pet.name != pet_name:
                continue
            filtered.append((pet, task))
        
        return filtered

    def detect_conflicts(self, owner: Owner) -> List[str]:
        """Detect scheduling conflicts between tasks using pairwise comparison algorithm.
        
        A conflict occurs when two tasks have the exact same scheduled time.
        Uses nested loops to compare each task against every other task (O(n²) complexity).
        Only considers tasks with scheduled_time set (ignores unscheduled tasks).
        
        Time Complexity: O(n²) where n is the number of scheduled tasks.
        Space Complexity: O(k) where k is the number of conflicts found.
        
        Args:
            owner: The owner whose tasks to check for conflicts.
        
        Returns:
            A list of warning messages for each conflict found. Empty list if no conflicts.
        """
        warnings = []
        all_tasks = owner.get_all_tasks(include_completed=False)
        
        # Filter to only tasks with scheduled times
        scheduled_tasks = [(pet, task) for pet, task in all_tasks if task.scheduled_time is not None]
        
        # Check each pair of tasks for conflicts
        for i in range(len(scheduled_tasks)):
            for j in range(i + 1, len(scheduled_tasks)):
                pet1, task1 = scheduled_tasks[i]
                pet2, task2 = scheduled_tasks[j]
                
                # Check if tasks overlap in time
                if task1.scheduled_time == task2.scheduled_time:
                    if pet1.id == pet2.id:
                        warning = f"⚠️ CONFLICT: {pet1.name}'s tasks '{task1.description}' and '{task2.description}' are both scheduled at {task1.scheduled_time.strftime('%H:%M')}"
                    else:
                        warning = f"⚠️ CONFLICT: {pet1.name}'s '{task1.description}' and {pet2.name}'s '{task2.description}' are both scheduled at {task1.scheduled_time.strftime('%H:%M')}"
                    warnings.append(warning)
        
        return warnings

    def schedule_tasks(self, owner: Owner) -> List[Dict[str, object]]:
        """Automatically schedule tasks using a greedy packing algorithm.
        
        Sorts tasks by duration (shortest first) to maximize task packing efficiency,
        then iteratively assigns time slots while respecting work and sleep constraints.
        Tasks already scheduled are preserved. Uses a 15-minute buffer between tasks.
        
        Time Complexity: O(n log n) for sorting + O(n * m) for scheduling where m is the number of time slot attempts.
        Space Complexity: O(n) for the scheduled result.
        
        Args:
            owner: The owner whose tasks need scheduling.
        
        Returns:
            A list of dictionaries containing pet_id, pet_name, and task for each scheduled task.
        """
        tasks = self.collect_tasks(owner, include_completed=False)
        
        # Sort tasks by duration (shorter first) for better packing
        sorted_tasks = sorted(tasks, key=lambda x: x[1].duration_minutes)
        
        scheduled: List[Dict[str, object]] = []
        current_time = datetime.combine(datetime.today().date(), owner.sleep_end)
        
        for pet, task in sorted_tasks:
            # Skip if already scheduled
            if task.scheduled_time is not None:
                scheduled.append({
                    "pet_id": pet.id,
                    "pet_name": pet.name,
                    "task": task,
                })
                continue
            
            # Find next available time slot
            while True:
                task_end = current_time + timedelta(minutes=task.duration_minutes)
                current_time_only = current_time.time()
                task_end_time = task_end.time()
                
                # Check if time slot conflicts with work hours
                conflicts_work = (owner.work_start <= current_time_only < owner.work_end or
                                  owner.work_start <= task_end_time < owner.work_end or
                                  (current_time_only < owner.work_start and task_end_time > owner.work_start))
                
                # Check if time slot conflicts with sleep
                conflicts_sleep = (current_time_only >= owner.sleep_start or
                                   task_end_time <= owner.sleep_end)
                
                if not conflicts_work and not conflicts_sleep:
                    # Assign this time slot
                    task.scheduled_time = current_time_only
                    scheduled.append({
                        "pet_id": pet.id,
                        "pet_name": pet.name,
                        "task": task,
                    })
                    current_time = task_end + timedelta(minutes=15)  # 15 min buffer between tasks
                    break
                else:
                    # Move to next available slot
                    if conflicts_work:
                        # Jump to after work hours
                        current_time = datetime.combine(datetime.today().date(), owner.work_end)
                    elif conflicts_sleep:
                        # Jump to after sleep ends (next day)
                        current_time = datetime.combine(datetime.today().date() + timedelta(days=1), owner.sleep_end)
        
        return scheduled


__all__ = ["Task", "Pet", "Owner", "Scheduler"]
