import streamlit as st
from pawpal_system import Owner, Pet, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Initialize Owner in session state to persist data across page refreshes
if "owner" not in st.session_state:
    st.session_state.owner = Owner(id="owner-1", name="Jordan")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Your Schedule Constraints")
st.caption("Set your work hours and sleep windows for scheduling.")

col1, col2 = st.columns(2)
with col1:
    work_start = st.time_input("Work start time", value=st.session_state.owner.work_start)
    work_end = st.time_input("Work end time", value=st.session_state.owner.work_end)
with col2:
    sleep_start = st.time_input("Sleep start time", value=st.session_state.owner.sleep_start)
    sleep_end = st.time_input("Sleep end time", value=st.session_state.owner.sleep_end)

if st.button("Update constraints"):
    st.session_state.owner.work_start = work_start
    st.session_state.owner.work_end = work_end
    st.session_state.owner.sleep_start = sleep_start
    st.session_state.owner.sleep_end = sleep_end
    st.success("Constraints updated!")

st.divider()

st.subheader("Add Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    new_pet = Pet(id=f"pet-{len(st.session_state.owner.pets) + 1}", name=pet_name, species=species)
    st.session_state.owner.add_pet(new_pet)
    st.success(f"Added {pet_name}!")

if st.session_state.owner.pets:
    st.write("Current pets:")
    for pet in st.session_state.owner.pets:
        st.write(f"- {pet.name} ({pet.species})")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Add Task")
if st.session_state.owner.pets:
    selected_pet = st.selectbox("Select pet", [pet.name for pet in st.session_state.owner.pets])
    task_title = st.text_input("Task title", value="Morning walk")
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    
    if st.button("Add task"):
        pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet)
        new_task = Task(description=task_title, duration_minutes=int(duration))
        pet.add_task(new_task)
        st.success(f"Added '{task_title}' to {selected_pet}!")
    
    st.write("All tasks:")
    for pet in st.session_state.owner.pets:
        if pet.tasks:
            st.write(f"**{pet.name}:**")
            for task in pet.tasks:
                st.write(f"  - {task.description} ({task.duration_minutes} min) - {'✓' if task.completed else '○'}")
        else:
            st.write(f"**{pet.name}:** No tasks")
else:
    st.info("Add a pet first before adding tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily plan for all pets.")

if st.button("Generate schedule"):
    from pawpal_system import Scheduler
    scheduler = Scheduler()
    plan = scheduler.schedule_tasks(st.session_state.owner)
    
    if plan:
        st.write("**Today's Schedule:**")
        for item in plan:
            task = item["task"]
            time_str = task.scheduled_time.strftime("%H:%M") if task.scheduled_time else "unscheduled"
            st.write(f"{time_str} - {item['pet_name']} - {task.description} ({task.duration_minutes} min)")
    else:
        st.info("No pending tasks to schedule.")
