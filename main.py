from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def format_time(value: time | None) -> str:
    if value is None:
        return "unscheduled"
    return value.strftime("%H:%M")


def build_sample_owner() -> Owner:
    owner = Owner(id="owner-1", name="Jordan")

    pet_one = Pet(id="pet-1", name="Mochi", species="cat")
    pet_one.add_task(Task(description="Morning feeding", duration_minutes=10, frequency="daily", scheduled_time=time(8, 0)))
    pet_one.add_task(Task(description="Litter box cleanup", duration_minutes=15, frequency="daily", scheduled_time=time(9, 30)))

    pet_two = Pet(id="pet-2", name="Biscuit", species="dog")
    pet_two.add_task(Task(description="Morning walk", duration_minutes=30, frequency="daily", scheduled_time=time(7, 30)))

    owner.add_pet(pet_one)
    owner.add_pet(pet_two)
    return owner


def print_schedule(owner: Owner) -> None:
    scheduler = Scheduler()
    schedule = scheduler.get_daily_plan(owner)

    print("Today's Schedule")
    print("=" * 17)

    for entry in schedule:
        task: Task = entry["task"]
        print(
            f"{entry['pet_name']} ({entry['pet_id']}) - "
            f"{task.description} | {format_time(task.scheduled_time)} | "
            f"{task.duration_minutes} min | completed={task.completed}"
        )


if __name__ == "__main__":
    sample_owner = build_sample_owner()
    print_schedule(sample_owner)