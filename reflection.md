# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

user  inputs their information and their pets information --- dashboard gets created --- user gets prompted to create timeline constraints (from/to sleephours and workhours) --- user gets prompted to order pet activity by priority (walks, feeding, meds, enrichment, grooming, etc.) --- the program automatically creates a pet upkeep schedule considering time constraints and priority of actions
 


- What classes did you include, and what responsibilities did you assign to each?

User: Stores personal info, time windows (sleep/work), preferences and  constraints.

Pet: pets name, species, age and care needs plus repsective default durations and priority weights.

Activity: Info about each task; serializable for storage and display.

Constraint: Time window rules and input constraints set by scheduler.

Scheduler: logic that generates a conflict aware timeline considering priorities and tradeoffs.

Schedule: Timeline data containing Activity; includes methods to add/remove/query and handle conflicts

Dashboard: UI/CLI layer that gathers user input, shows the generated schedule, accepts edits, and triggers re-scheduling.

Storage: Persistence layer to save/load users, pets, and schedules (e.g., JSON file wrapper).

Notifier (optional): Handles reminders/alerts and integration with system notifications or logs.



**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
