import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(22, 13))
ax.set_xlim(0, 22)
ax.set_ylim(0, 13)
ax.axis('off')
fig.patch.set_facecolor('#f0f4f8')

def draw_class_box(ax, x, y, width, height, title, attributes, methods, header_color='#4a90d9'):
    # Header
    header = mpatches.FancyBboxPatch((x, y + height - 1.1), width, 1.1,
                                      boxstyle="square,pad=0", linewidth=1.5,
                                      edgecolor='#2c3e50', facecolor=header_color)
    ax.add_patch(header)
    ax.text(x + width / 2, y + height - 0.52, title,
            ha='center', va='center', fontsize=12, fontweight='bold', color='white')

    # Attributes section
    attr_height = len(attributes) * 0.37 + 0.2
    attr_box = mpatches.FancyBboxPatch((x, y + height - 1.1 - attr_height), width, attr_height,
                                        boxstyle="square,pad=0", linewidth=1.5,
                                        edgecolor='#2c3e50', facecolor='#eaf2fb')
    ax.add_patch(attr_box)
    for i, attr in enumerate(attributes):
        ax.text(x + 0.15, y + height - 1.1 - 0.26 - i * 0.37, attr,
                ha='left', va='center', fontsize=8.5, color='#1a252f', family='monospace')

    # Methods section
    meth_height = len(methods) * 0.37 + 0.2
    meth_box = mpatches.FancyBboxPatch((x, y + height - 1.1 - attr_height - meth_height), width, meth_height,
                                        boxstyle="square,pad=0", linewidth=1.5,
                                        edgecolor='#2c3e50', facecolor='#fdfefe')
    ax.add_patch(meth_box)
    for i, meth in enumerate(methods):
        ax.text(x + 0.15, y + height - 1.1 - attr_height - 0.26 - i * 0.37, meth,
                ha='left', va='center', fontsize=8.5, color='#1a252f', family='monospace')

# ── Class Definitions ──────────────────────────────────────────────────────────

# Scheduler (top-left)
draw_class_box(ax, x=0.3, y=5.5, width=6.0, height=6.2,
               title='Scheduler',
               attributes=[
                   '+ owner: Owner',
                   '+ max_parallel_tasks: int',
               ],
               methods=[
                   '+ build_daily_plan(target_date)',
                   '+ sort_tasks(tasks)',
                   '+ detect_conflicts(tasks)',
                   '+ resolve_conflicts(tasks)',
                   '+ filter_tasks(tasks, pet_name, completed)',
                   '+ handle_recurring(task, pet)',
                   '+ mark_task_complete(task_id)',
                   '+ explain_plan(tasks)',
               ],
               header_color='#8e44ad')

# Owner (top-right)
draw_class_box(ax, x=8.0, y=7.5, width=5.5, height=4.5,
               title='Owner',
               attributes=[
                   '+ owner_id: str',
                   '+ name: str',
                   '+ daily_time_budget_min: int',
                   '+ preferences: dict',
                   '+ pets: list[Pet]',
               ],
               methods=[
                   '+ add_pet(pet)',
                   '+ remove_pet(pet_id)',
                   '+ get_all_tasks()',
               ],
               header_color='#2980b9')

# Pet (bottom-center)
draw_class_box(ax, x=8.0, y=1.0, width=5.5, height=5.0,
               title='Pet',
               attributes=[
                   '+ pet_id: str',
                   '+ name: str',
                   '+ species: str',
                   '+ age_years: int',
                   '+ tasks: list[Task]',
               ],
               methods=[
                   '+ add_task(task)',
                   '+ remove_task(task_id)',
                   '+ get_tasks_for_date(target_date)',
               ],
               header_color='#27ae60')

# Task (far right)
draw_class_box(ax, x=15.5, y=1.0, width=6.0, height=8.5,
               title='Task',
               attributes=[
                   '+ task_id: str',
                   '+ title: str',
                   '+ category: str',
                   '+ duration_min: int',
                   '+ priority: int',
                   '+ scheduled_time: time',
                   '+ recurrence: str',
                   '+ due_date: date',
                   '+ is_completed: bool',
                   '+ next_due_date: date',
               ],
               methods=[
                   '+ is_due_on(target_date)',
                   '+ mark_complete()',
               ],
               header_color='#e67e22')

# ── Arrows ─────────────────────────────────────────────────────────────────────

# Scheduler → Owner (manages)
ax.annotate('', xy=(8.0, 10.0), xytext=(6.3, 10.0),
            arrowprops=dict(arrowstyle='->', color='#8e44ad', lw=2))
ax.text(7.15, 10.25, 'manages', ha='center', fontsize=9, color='#8e44ad', style='italic')

# Owner → Pet (has many) - vertical
ax.annotate('', xy=(10.75, 6.0), xytext=(10.75, 7.5),
            arrowprops=dict(arrowstyle='->', color='#2980b9', lw=2))
ax.text(11.2, 6.7, 'has many', ha='left', fontsize=9, color='#2980b9', style='italic')

# Pet → Task (has many) - horizontal
ax.annotate('', xy=(15.5, 4.5), xytext=(13.5, 4.5),
            arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2))
ax.text(14.5, 4.75, 'has many', ha='center', fontsize=9, color='#27ae60', style='italic')

# Scheduler → Pet (handle_recurring touches Pet)
ax.annotate('', xy=(8.0, 3.5), xytext=(6.3, 3.5),
            arrowprops=dict(arrowstyle='->', color='#8e44ad', lw=1.5, linestyle='dashed'))
ax.text(7.15, 3.75, 'recurring', ha='center', fontsize=8, color='#8e44ad', style='italic')

# ── Title ──────────────────────────────────────────────────────────────────────
ax.text(11, 12.5, 'PawPal+ — Final UML Class Diagram',
        ha='center', va='center', fontsize=16, fontweight='bold', color='#2c3e50')

plt.tight_layout()
plt.savefig('uml_final.png', dpi=150, bbox_inches='tight', facecolor='#f0f4f8')
print("uml_final.png saved.")
