# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic` owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

Today's Schedule
=================
Mochi (pet-1) - Morning feeding | 08:00 | 10 min | completed=False
Mochi (pet-1) - Litter box cleanup | 09:30 | 15 min | completed=False
Biscuit (pet-2) - Morning walk | 07:30 | 30 min | completed=False


## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

test output:
========== test session starts ===========
platform win32 -- Python 3.13.2, pytest-9.0.3, pluggy-1.6.0 -- C:\Python313\python.exe
i110-module2show-pawpal-starter
plugins: anyio-4.13.0, cov-7.1.0
collected 2 items                         

tests/test_pawpal.py::test_task_completion PASSED [ 50%]
tests/test_pawpal.py::test_task_addition PASSED [100%]

=========== 2 passed in 0.03s ============
PS C:\Users\mathi\projects\a110 NEW\ai110-module2show-pawpal-starter> 


## 📐 Smarter Scheduling

The PawPal+ scheduler includes several advanced features to help pet owners manage their tasks efficiently:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting by time | `Scheduler.sort_by_time()` | Sorts tasks chronologically using Timsort algorithm (O(n log n)). Tasks without scheduled times are placed at the end using a sentinel value. |
| Task filtering | `Scheduler.filter_tasks()` | Filters tasks by completion status (completed/incomplete) and/or pet name using linear search (O(n)). Both filters can be used together or independently. |
| Conflict detection | `Scheduler.detect_conflicts()` | Detects scheduling conflicts using pairwise comparison algorithm (O(n²)). Identifies when two tasks for the same or different pets are scheduled at the exact same time. Returns warning messages rather than crashing. |
| Recurring task creation | `Task.create_next_occurrence()` | Automatically generates next occurrence for daily/weekly tasks using timedelta arithmetic. Daily adds 1 day, weekly adds 7 days to scheduled time. Returns None for "once" frequency tasks. |
| Recurring task completion | `Pet.complete_task()` | Marks a task complete and automatically creates the next occurrence if the task is recurring. Searches for incomplete tasks by description (O(n)). |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
