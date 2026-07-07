# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

user  inputs their information and their pets information --- dashboard gets created --- user gets prompted to create timeline constraints (from/to sleephours and workhours) --- user gets prompted to order pet activity by priority (walks, feeding, meds, enrichment, grooming, etc.) --- the program automatically creates a pet upkeep schedule considering time constraints and priority of actions
 


- What classes did you include, and what responsibilities did you assign to each?

User: Stores personal info, time windows (sleep/work), preferences and  constraints.

Pet: pets name, species, age and care needs plus repsective default durations and priority weights.

Task: Info about each task; serializable for storage and display.

Constraint: Time window rules and input constraints set by scheduler.

Scheduler: logic that generates a conflict aware timeline considering priorities and tradeoffs.

Schedule: Timeline data containing Activity; includes methods to add/remove/query and handle conflicts

Storage: Persistence layer to save/load users, pets, and schedules (e.g., JSON file wrapper).


**b. Design changes**

- Did your design change during implementation?

yes

- If yes, describe at least one change and why you made it.

for example i was going to implement a UI haning class to handle a dashboard and also a storage class to help load and save, but since its a streamlit app, I decided that dashboard class is redundant and storage class is overkill.

Also I revamped the schedule/scheduler classes into scheduleentry/scheduler for semantic clarity, and implemented the constraints and time logic along the way because it was useless when generated
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

timeoff (work, sleep etc), time (needed for tasks), priority
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

the scheduler sorts tasks by duration (shortest fist) instead of by priority, this is for simplicity since shortest task can be done faster and easier in real life scenarios

- Why is that tradeoff reasonable for this scenario?

because it follows human nature to do fast tasks first instead of the most technically important ones
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

refactoring methods/classes, asking questions about the structure and logic to better understand how everything works together and generating fixes for bugs and redundancies

- What kinds of prompts or questions were most helpful?

for learning, I usually use very specific promts eg "how come 2 way reference in a class is more effcient if each class appends whatever they need from the top one anyways? wouldnt that just be redundant or overkill??"

for debugging I usually use broader prompts and allow the AI to generate solutions that might not be what i have in mind, but am open to see what it comes up with

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

I didnt accept the first generated pawpal_system.py scheduler class because it didnt include any time constrain logic, also as I was building the time logic, AI defaulted to common cases as hardcoded values, such as work is always 9:00 to 17:00

- How did you evaluate or verify what the AI suggested?

By taking a quick look, sometimes dirctly asking questions about why it did what it did and what it achieves now and how. but specially by running the code and using it myself
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?

I am around 95% confident, this is because most cases (including a few edge cases) it did work smoothly, only once did it glitch and returned weird duplicate times

- What edge cases would you test next if you had more time?

I would test entering tons of pets and tons of tasks each to check the time handling algorithm, and also 

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I love how smooth the bridge between the terminal interface and the streamlit interface was, i expectedd it to be a bigger pain, also the timing logic does work very accurately surprisingly

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

for usability, i would honein the edge cases, maybe make a visual  google calendar style timetable instead of a text based one


**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned a ton about class and method interaction, bridging python to streamlit, and specally memory handling for streamlit and how to make it more efficient through fusing class values through appending and feeding streamlit the most "parent" one, which is very efficient conceptually.