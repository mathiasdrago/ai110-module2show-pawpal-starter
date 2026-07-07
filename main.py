from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def format_time(value: time | None) -> str:
    if value is None:
        return "unscheduled"
    return value.strftime("%H:%M")


def build_sample_owner() -> Owner:
    owner = Owner(id="owner-1", name="Jordan")

    pet_one = Pet(id="pet-1", name="Mochi", species="cat")
    # Add tasks with scheduled times out of order and mixed frequencies
    pet_one.add_task(Task(description="Evening feeding", duration_minutes=10, frequency="daily", scheduled_time=time(18, 30)))
    pet_one.add_task(Task(description="Morning feeding", duration_minutes=10, frequency="daily", scheduled_time=time(7, 30)))
    pet_one.add_task(Task(description="Litter box cleanup", duration_minutes=15, frequency="once", scheduled_time=time(12, 0)))
    pet_one.add_task(Task(description="Play time", duration_minutes=20, frequency="daily", scheduled_time=None))  # Unscheduled

    pet_two = Pet(id="pet-2", name="Biscuit", species="dog")
    # Add tasks with scheduled times out of order
    pet_two.add_task(Task(description="Evening walk", duration_minutes=30, frequency="daily", scheduled_time=time(19, 0)))
    pet_two.add_task(Task(description="Morning walk", duration_minutes=30, frequency="daily", scheduled_time=time(8, 0)))
    pet_two.add_task(Task(description="Training", duration_minutes=15, frequency="daily", scheduled_time=time(14, 30)))

    owner.add_pet(pet_one)
    owner.add_pet(pet_two)
    return owner


def print_schedule(owner: Owner) -> None:
    scheduler = Scheduler()
    schedule = scheduler.schedule_tasks(owner)

    print("Today's Schedule")
    print("=" * 17)

    for entry in schedule:
        task: Task = entry["task"]
        print(
            f"{entry['pet_name']} ({entry['pet_id']}) - "
            f"{task.description} | {format_time(task.scheduled_time)} | "
            f"{task.duration_minutes} min | completed={task.completed}"
        )


def demo_sorting_and_filtering(owner: Owner) -> None:
    scheduler = Scheduler()
    
    print("\n" + "=" * 60)
    print("DEMONSTRATING SORT_BY_TIME METHOD")
    print("=" * 60)
    
    # Collect all tasks and extract just the Task objects
    all_task_pairs = scheduler.collect_tasks(owner, include_completed=True)
    all_tasks = [task for pet, task in all_task_pairs]
    
    print("\nTasks BEFORE sorting by time:")
    for task in all_tasks:
        print(f"  {task.description} | {format_time(task.scheduled_time)}")
    
    # Sort by time
    sorted_tasks = scheduler.sort_by_time(all_tasks)
    
    print("\nTasks AFTER sorting by time:")
    for task in sorted_tasks:
        print(f"  {task.description} | {format_time(task.scheduled_time)}")
    
    print("\n" + "=" * 60)
    print("DEMONSTRATING FILTER_TASKS METHOD")
    print("=" * 60)
    
    # Filter by pet name
    print("\nFiltering by pet name 'Mochi':")
    mochi_tasks = scheduler.filter_tasks(owner, pet_name="Mochi")
    for pet, task in mochi_tasks:
        print(f"  {pet.name} - {task.description} | {format_time(task.scheduled_time)}")
    
    # Filter by completion status (incomplete)
    print("\nFiltering by completed=False (incomplete tasks):")
    incomplete_tasks = scheduler.filter_tasks(owner, completed=False)
    for pet, task in incomplete_tasks:
        print(f"  {pet.name} - {task.description} | {format_time(task.scheduled_time)}")
    
    # Filter by both pet name and completion status
    print("\nFiltering by pet name 'Biscuit' AND completed=False:")
    biscuit_incomplete = scheduler.filter_tasks(owner, pet_name="Biscuit", completed=False)
    for pet, task in biscuit_incomplete:
        print(f"  {pet.name} - {task.description} | {format_time(task.scheduled_time)}")
    
    # Mark one task as complete to test filtering
    print("\nMarking 'Morning feeding' for Mochi as complete...")
    for pet, task in scheduler.filter_tasks(owner, pet_name="Mochi"):
        if task.description == "Morning feeding":
            task.mark_complete()
            break
    
    print("\nFiltering by completed=True (completed tasks):")
    completed_tasks = scheduler.filter_tasks(owner, completed=True)
    for pet, task in completed_tasks:
        print(f"  {pet.name} - {task.description} | {format_time(task.scheduled_time)}")


def demo_recurring_tasks(owner: Owner) -> None:
    print("\n" + "=" * 60)
    print("DEMONSTRATING RECURRING TASK FUNCTIONALITY")
    print("=" * 60)
    
    # Create a fresh pet for this demo to avoid conflicts
    demo_pet = Pet(id="demo-pet", name="Demo Pet", species="cat")
    
    # Add tasks with different frequencies
    demo_pet.add_task(Task(description="Morning feeding", duration_minutes=10, frequency="daily", scheduled_time=time(7, 30)))
    demo_pet.add_task(Task(description="Litter box cleanup", duration_minutes=15, frequency="once", scheduled_time=time(12, 0)))
    
    print(f"\n{demo_pet.name}'s initial tasks:")
    for task in demo_pet.tasks:
        print(f"  {task.description} | {format_time(task.scheduled_time)} | frequency={task.frequency} | completed={task.completed}")
    
    # Complete a daily task
    print("\n--- Completing 'Morning feeding' (daily) ---")
    next_task = demo_pet.complete_task("Morning feeding")
    if next_task:
        print(f"✓ Task marked complete")
        print(f"✓ Next occurrence created: {next_task.description} | {format_time(next_task.scheduled_time)}")
    else:
        print(f"✗ No next occurrence created")
    
    print(f"\n{demo_pet.name}'s tasks after daily completion:")
    for task in demo_pet.tasks:
        print(f"  {task.description} | {format_time(task.scheduled_time)} | frequency={task.frequency} | completed={task.completed}")
    
    # Complete a weekly task
    print("\n--- Adding and completing a weekly task ---")
    weekly_task = Task(description="Vet checkup", duration_minutes=30, frequency="weekly", scheduled_time=time(10, 0))
    demo_pet.add_task(weekly_task)
    print(f"Added weekly task: {weekly_task.description} | {format_time(weekly_task.scheduled_time)}")
    
    next_weekly = demo_pet.complete_task("Vet checkup")
    if next_weekly:
        print(f"✓ Task marked complete")
        print(f"✓ Next occurrence created: {next_weekly.description} | {format_time(next_weekly.scheduled_time)}")
    else:
        print(f"✗ No next occurrence created")
    
    print(f"\n{demo_pet.name}'s tasks after weekly completion:")
    for task in demo_pet.tasks:
        print(f"  {task.description} | {format_time(task.scheduled_time)} | frequency={task.frequency} | completed={task.completed}")
    
    # Complete a one-time task (should not create next occurrence)
    print("\n--- Completing 'Litter box cleanup' (once) ---")
    next_once = demo_pet.complete_task("Litter box cleanup")
    if next_once:
        print(f"✗ Unexpected: Next occurrence created: {next_once.description}")
    else:
        print(f"✓ Task marked complete (no next occurrence for 'once' frequency)")
    
    print(f"\n{demo_pet.name}'s final tasks:")
    for task in demo_pet.tasks:
        print(f"  {task.description} | {format_time(task.scheduled_time)} | frequency={task.frequency} | completed={task.completed}")


def demo_conflict_detection(owner: Owner) -> None:
    print("\n" + "=" * 60)
    print("DEMONSTRATING CONFLICT DETECTION")
    print("=" * 60)
    
    # Create a fresh owner with conflicting tasks
    conflict_owner = Owner(id="conflict-owner", name="Test Owner")
    
    # Create two pets
    pet1 = Pet(id="pet-1", name="Whiskers", species="cat")
    pet2 = Pet(id="pet-2", name="Rex", species="dog")
    
    # Add tasks with conflicting times (same pet, same time)
    pet1.add_task(Task(description="Morning feeding", duration_minutes=10, scheduled_time=time(8, 0)))
    pet1.add_task(Task(description="Morning play", duration_minutes=15, scheduled_time=time(8, 0)))  # CONFLICT!
    
    # Add tasks with conflicting times (different pets, same time)
    pet1.add_task(Task(description="Evening grooming", duration_minutes=20, scheduled_time=time(18, 0)))
    pet2.add_task(Task(description="Evening walk", duration_minutes=30, scheduled_time=time(18, 0)))  # CONFLICT!
    
    # Add non-conflicting tasks
    pet1.add_task(Task(description="Lunch feeding", duration_minutes=5, scheduled_time=time(12, 0)))
    pet2.add_task(Task(description="Afternoon nap", duration_minutes=60, scheduled_time=time(14, 0)))
    
    conflict_owner.add_pet(pet1)
    conflict_owner.add_pet(pet2)
    
    print("\nScheduled tasks:")
    for pet, task in conflict_owner.get_all_tasks(include_completed=False):
        if task.scheduled_time:
            print(f"  {pet.name}: {task.description} at {format_time(task.scheduled_time)}")
    
    # Detect conflicts
    scheduler = Scheduler()
    warnings = scheduler.detect_conflicts(conflict_owner)
    
    print("\n" + "-" * 60)
    if warnings:
        print(f"Found {len(warnings)} conflict(s):")
        for warning in warnings:
            print(f"  {warning}")
    else:
        print("No conflicts detected.")


if __name__ == "__main__":
    sample_owner = build_sample_owner()
    print_schedule(sample_owner)
    demo_sorting_and_filtering(sample_owner)
    demo_recurring_tasks(sample_owner)
    demo_conflict_detection(sample_owner)