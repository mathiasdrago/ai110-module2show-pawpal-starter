import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pawpal_system import Task, Pet


def test_task_completion():
    """Verify that calling mark_complete() actually changes the task's status."""
    task = Task(description="Morning walk", duration_minutes=30)
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(id="pet-1", name="Mochi")
    initial_count = len(pet.tasks)
    task = Task(description="Feeding", duration_minutes=10)
    pet.add_task(task)
    assert len(pet.tasks) == initial_count + 1
