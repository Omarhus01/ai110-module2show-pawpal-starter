import uuid
import streamlit as st
from datetime import date, time
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("Smart pet care scheduling assistant")

# ── Session State Setup ────────────────────────────────────────────────────────

if "owner" not in st.session_state:
    st.session_state.owner = None

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

# ── Section 1: Owner Setup ─────────────────────────────────────────────────────

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
        st.success(f"Owner '{owner_name}' saved with a {budget}-minute daily budget.")

st.divider()

# ── Section 2: Add a Pet ───────────────────────────────────────────────────────

st.subheader("2. Add a Pet")

if st.session_state.owner is None:
    st.info("Save your owner info first.")
else:
    with st.form("pet_form"):
        pet_name = st.text_input("Pet name", value="Buddy")
        species  = st.selectbox("Species", ["Dog", "Cat", "Bird", "Other"])
        age      = st.number_input("Age (years)", min_value=0, max_value=30, value=2)
        add_pet  = st.form_submit_button("Add Pet")

        if add_pet:
            pet = Pet(
                pet_id=str(uuid.uuid4()),
                name=pet_name,
                species=species,
                age_years=int(age)
            )
            st.session_state.owner.add_pet(pet)
            st.success(f"{species} '{pet_name}' added!")

    if st.session_state.owner.pets:
        st.markdown("**Your pets:**")
        cols = st.columns(len(st.session_state.owner.pets))
        for col, p in zip(cols, st.session_state.owner.pets):
            with col:
                st.metric(label=p.name, value=p.species, delta=f"{p.age_years} yrs old")

st.divider()

# ── Section 3: Add a Task ──────────────────────────────────────────────────────

st.subheader("3. Add a Task")

if st.session_state.owner is None or not st.session_state.owner.pets:
    st.info("Add at least one pet before adding tasks.")
else:
    pet_names = [p.name for p in st.session_state.owner.pets]

    with st.form("task_form"):
        col1, col2 = st.columns(2)
        with col1:
            selected_pet = st.selectbox("Assign to pet", pet_names)
            task_title   = st.text_input("Task title", value="Morning Walk")
            category     = st.selectbox("Category", ["exercise", "feeding", "medication", "grooming", "enrichment"])
        with col2:
            duration   = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
            priority   = st.slider("Priority (1=low, 5=high)", 1, 5, 3)
            sched_time = st.time_input("Scheduled time", value=time(8, 0))
            recurrence = st.selectbox("Recurrence", ["once", "daily", "weekly"])

        add_task = st.form_submit_button("Add Task")

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

    # Show all current tasks per pet
    all_tasks = st.session_state.owner.get_all_tasks()
    if all_tasks:
        st.markdown("**All scheduled tasks:**")
        task_rows = []
        for p in st.session_state.owner.pets:
            for t in p.tasks:
                task_rows.append({
                    "Pet": p.name,
                    "Task": t.title,
                    "Category": t.category,
                    "Time": t.scheduled_time.strftime("%H:%M"),
                    "Duration (min)": t.duration_min,
                    "Priority": t.priority,
                    "Recurrence": t.recurrence.capitalize()
                })
        st.dataframe(task_rows, use_container_width=True)

st.divider()

# ── Section 4: Generate Schedule ──────────────────────────────────────────────

st.subheader("4. Today's Schedule")

if st.session_state.owner is None or not st.session_state.owner.pets:
    st.info("Set up your owner and pets first.")
else:
    if st.button("Generate Schedule", type="primary"):
        scheduler = st.session_state.scheduler
        plan = scheduler.build_daily_plan(date.today())

        if not plan:
            st.warning("No tasks are scheduled for today.")
        else:
            # Conflict detection with detailed warnings
            conflicts = scheduler.detect_conflicts(plan)
            if conflicts:
                for task_a, task_b in conflicts:
                    st.warning(
                        f"Conflict at {task_a.scheduled_time.strftime('%H:%M')}: "
                        f"**'{task_a.title}'** and **'{task_b.title}'** overlap. "
                        f"'{task_b.title}' has been shifted forward by 30 minutes."
                    )
                plan = scheduler.resolve_conflicts(plan)

            st.success(f"Schedule ready — {len(plan)} tasks for {date.today().strftime('%A, %B %d')}")

            # Schedule table
            rows = []
            for task in plan:
                pet_name = next(
                    (p.name for p in st.session_state.owner.pets
                     if any(t.task_id == task.task_id for t in p.tasks)),
                    "Unknown"
                )
                priority_label = {1: "1 - Very Low", 2: "2 - Low", 3: "3 - Medium",
                                   4: "4 - High", 5: "5 - Critical"}.get(task.priority, str(task.priority))
                rows.append({
                    "Time": task.scheduled_time.strftime("%H:%M"),
                    "Task": task.title,
                    "Pet": pet_name,
                    "Category": task.category.capitalize(),
                    "Duration (min)": task.duration_min,
                    "Priority": priority_label,
                    "Recurrence": task.recurrence.capitalize(),
                    "Status": "Done" if task.is_completed else "Pending"
                })

            st.dataframe(rows, use_container_width=True)

            # Filter section
            st.markdown("---")
            st.markdown("**Filter the schedule:**")
            filter_col1, filter_col2 = st.columns(2)

            with filter_col1:
                pet_filter = st.selectbox(
                    "Filter by pet",
                    ["All"] + [p.name for p in st.session_state.owner.pets]
                )
            with filter_col2:
                status_filter = st.selectbox("Filter by status", ["All", "Pending", "Done"])

            filtered = plan
            if pet_filter != "All":
                filtered = scheduler.filter_tasks(filtered, pet_name=pet_filter)
            if status_filter == "Pending":
                filtered = scheduler.filter_tasks(filtered, completed=False)
            elif status_filter == "Done":
                filtered = scheduler.filter_tasks(filtered, completed=True)

            if filtered:
                st.markdown(f"Showing **{len(filtered)}** task(s):")
                for task in filtered:
                    st.write(f"- [{task.scheduled_time.strftime('%H:%M')}] **{task.title}** — {task.duration_min} min | Priority: {task.priority}")
            else:
                st.info("No tasks match the selected filters.")

            # Plan explanation
            st.markdown("---")
            with st.expander("Plan Explanation", expanded=False):
                for note in scheduler.explain_plan(plan):
                    st.write(f"- {note}")
