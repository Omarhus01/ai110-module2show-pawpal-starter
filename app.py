import uuid
import streamlit as st
from datetime import date, time
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("Smart pet care scheduling assistant")

# ── Session State Setup ────────────────────────────────────────────────────────
# Streamlit reruns top-to-bottom on every interaction.
# We store the Owner object in session_state so it persists across reruns.

if "owner" not in st.session_state:
    st.session_state.owner = None

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

# ── Step 1: Owner Setup ────────────────────────────────────────────────────────

st.subheader("1. Owner Info")

with st.form("owner_form"):
    owner_name = st.text_input("Your name", value="Omar")
    budget = st.number_input("Daily time budget (minutes)", min_value=10, max_value=480, value=120)
    submitted = st.form_submit_button("Save Owner")

    if submitted:
        st.session_state.owner = Owner(
            owner_id=str(uuid.uuid4()),
            name=owner_name,
            daily_time_budget_min=int(budget)
        )
        st.session_state.scheduler = Scheduler(owner=st.session_state.owner)
        st.success(f"Owner '{owner_name}' saved!")

st.divider()

# ── Step 2: Add a Pet ──────────────────────────────────────────────────────────

st.subheader("2. Add a Pet")

if st.session_state.owner is None:
    st.info("Save your owner info first.")
else:
    with st.form("pet_form"):
        pet_name = st.text_input("Pet name", value="Buddy")
        species   = st.selectbox("Species", ["Dog", "Cat", "Bird", "Other"])
        age       = st.number_input("Age (years)", min_value=0, max_value=30, value=2)
        add_pet   = st.form_submit_button("Add Pet")

        if add_pet:
            pet = Pet(
                pet_id=str(uuid.uuid4()),
                name=pet_name,
                species=species,
                age_years=int(age)
            )
            st.session_state.owner.add_pet(pet)
            st.success(f"Pet '{pet_name}' added!")

    if st.session_state.owner.pets:
        st.write("**Your pets:**")
        for p in st.session_state.owner.pets:
            st.write(f"- {p.name} ({p.species}, {p.age_years} yrs)")

st.divider()

# ── Step 3: Add a Task ─────────────────────────────────────────────────────────

st.subheader("3. Add a Task")

if st.session_state.owner is None or not st.session_state.owner.pets:
    st.info("Add at least one pet before adding tasks.")
else:
    pet_names = [p.name for p in st.session_state.owner.pets]

    with st.form("task_form"):
        selected_pet = st.selectbox("Assign to pet", pet_names)
        task_title   = st.text_input("Task title", value="Morning Walk")
        category     = st.selectbox("Category", ["exercise", "feeding", "medication", "grooming", "enrichment"])
        duration     = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority     = st.slider("Priority (1=low, 5=high)", 1, 5, 3)
        sched_time   = st.time_input("Scheduled time", value=time(8, 0))
        recurrence   = st.selectbox("Recurrence", ["once", "daily", "weekly"])
        add_task     = st.form_submit_button("Add Task")

        if add_task:
            task = Task(
                task_id=str(uuid.uuid4()),
                title=task_title,
                category=category,
                duration_min=int(duration),
                priority=priority,
                scheduled_time=sched_time,
                recurrence=recurrence,
                due_date=date.today()
            )
            pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet)
            pet.add_task(task)
            st.success(f"Task '{task_title}' added to {selected_pet}!")

st.divider()

# ── Step 4: Generate Schedule ──────────────────────────────────────────────────

st.subheader("4. Today's Schedule")

if st.session_state.owner is None or not st.session_state.owner.pets:
    st.info("Set up your owner and pets first.")
else:
    if st.button("Generate Schedule"):
        scheduler = st.session_state.scheduler
        plan = scheduler.build_daily_plan(date.today())

        if not plan:
            st.warning("No tasks scheduled for today.")
        else:
            conflicts = scheduler.detect_conflicts(plan)
            if conflicts:
                st.warning(f"{len(conflicts)} conflict(s) detected - times adjusted automatically.")
                plan = scheduler.resolve_conflicts(plan)

            st.success(f"Schedule ready - {len(plan)} tasks for today.")

            rows = []
            for task in plan:
                pet_name = next(
                    (p.name for p in st.session_state.owner.pets
                     if any(t.task_id == task.task_id for t in p.tasks)),
                    "Unknown"
                )
                rows.append({
                    "Time": task.scheduled_time.strftime("%H:%M"),
                    "Task": task.title,
                    "Pet": pet_name,
                    "Duration (min)": task.duration_min,
                    "Priority": task.priority,
                    "Recurrence": task.recurrence.capitalize(),
                    "Done": "Yes" if task.is_completed else "No"
                })

            st.table(rows)

            st.markdown("**Plan Explanation:**")
            for note in scheduler.explain_plan(plan):
                st.write(f"- {note}")
