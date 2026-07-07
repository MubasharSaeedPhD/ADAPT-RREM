"""
RREM Template Library — 12 Action-Type-Specific Variants
=========================================================
5 constraint categories × action-type-specific question variants.

Action types covered (12 variants):
  grasp, place, open_drawer, close_drawer, pick_and_lift,
  move_to, push, slide, stack, put_in, open_box, generic

Each variant is instantiated at runtime with:
  {target}       : object/surface name
  {ee_pos}       : end-effector position [x, y, z]
  {gripper_open} : gripper openness ratio (0=closed, 1=open)
  {joint_vel}    : max joint velocity (rad/s)
  {ws_min}       : workspace minimum bounds
  {ws_max}       : workspace maximum bounds
  {ws_center}    : workspace center
"""

# ═══════════════════════════════════════════════════════════
#  Category 1: REACHABILITY
#  Can the end-effector reach the target from current config?
# ═══════════════════════════════════════════════════════════

REACHABILITY = {

    "grasp": (
        "The end-effector is at {ee_pos} and workspace bounds are "
        "[{ws_min}, {ws_max}]. Is the end-effector within the valid "
        "workspace to approach and grasp object '{target}'?"
    ),

    "place": (
        "The end-effector is at {ee_pos}. Is this position within the "
        "workspace bounds [{ws_min}, {ws_max}] to reach placement "
        "surface '{target}' and place the held object?"
    ),

    "open_drawer": (
        "The end-effector is at {ee_pos} with workspace [{ws_min}, {ws_max}]. "
        "Is the arm within reachable range to pull open drawer '{target}'?"
    ),

    "close_drawer": (
        "The end-effector is at {ee_pos} with workspace [{ws_min}, {ws_max}]. "
        "Is the arm within reachable range to push close drawer '{target}'?"
    ),

    "pick_and_lift": (
        "The end-effector is at {ee_pos}. Is it within workspace bounds "
        "[{ws_min}, {ws_max}] to reach, grasp, and lift object '{target}'?"
    ),

    "move_to": (
        "The end-effector is at {ee_pos}. Is the target position '{target}' "
        "reachable within workspace [{ws_min}, {ws_max}] from current config?"
    ),

    "push": (
        "The end-effector is at {ee_pos}. Is it within workspace "
        "[{ws_min}, {ws_max}] to approach and push object '{target}'?"
    ),

    "slide": (
        "The end-effector is at {ee_pos}. Is it within workspace "
        "[{ws_min}, {ws_max}] to slide object '{target}' to target position?"
    ),

    "stack": (
        "The end-effector is at {ee_pos}. Is the arm within workspace "
        "[{ws_min}, {ws_max}] to stack the held object onto '{target}'?"
    ),

    "put_in": (
        "The end-effector is at {ee_pos}. Is workspace [{ws_min}, {ws_max}] "
        "sufficient to place the held object into container '{target}'?"
    ),

    "open_box": (
        "The end-effector is at {ee_pos}. Is it within workspace "
        "[{ws_min}, {ws_max}] to reach and open box '{target}'?"
    ),

    "generic": (
        "The end-effector is at {ee_pos}. Is it within the valid workspace "
        "bounds [{ws_min}, {ws_max}] to execute action on '{target}'?"
    ),
}


# ═══════════════════════════════════════════════════════════
#  Category 2: COLLISION SAFETY
#  Is the arm moving safely without collision?
# ═══════════════════════════════════════════════════════════

COLLISION = {

    "grasp": (
        "The arm's maximum joint velocity is {joint_vel:.6f} rad/s during "
        "approach to grasp '{target}'. Is this below the safe threshold of "
        "1.0 rad/s, indicating no collision is occurring?"
    ),

    "place": (
        "The arm's maximum joint velocity is {joint_vel:.6f} rad/s while "
        "approaching placement surface '{target}'. Is this safely below "
        "1.0 rad/s with no collision risk?"
    ),

    "open_drawer": (
        "The arm's maximum joint velocity is {joint_vel:.6f} rad/s while "
        "approaching drawer '{target}'. Is this below 1.0 rad/s, indicating "
        "safe collision-free approach?"
    ),

    "close_drawer": (
        "The arm's maximum joint velocity is {joint_vel:.6f} rad/s while "
        "closing drawer '{target}'. Is this below 0.8 rad/s to avoid "
        "pushing too fast?"
    ),

    "pick_and_lift": (
        "The arm's maximum joint velocity is {joint_vel:.6f} rad/s during "
        "pick-and-lift of '{target}'. Is this safely below 1.0 rad/s with "
        "no collision occurring?"
    ),

    "move_to": (
        "The arm's maximum joint velocity is {joint_vel:.6f} rad/s during "
        "movement toward '{target}'. Is this below 1.5 rad/s, indicating "
        "safe transit speed?"
    ),

    "push": (
        "The arm's maximum joint velocity is {joint_vel:.6f} rad/s during "
        "push action on '{target}'. Is this below 0.5 rad/s, indicating "
        "a controlled push without collision risk?"
    ),

    "slide": (
        "The arm's maximum joint velocity is {joint_vel:.6f} rad/s during "
        "slide action on '{target}'. Is this below 0.8 rad/s for safe "
        "sliding without collision?"
    ),

    "stack": (
        "The arm's maximum joint velocity is {joint_vel:.6f} rad/s during "
        "stacking onto '{target}'. Is this below 0.5 rad/s for safe "
        "precision stacking?"
    ),

    "put_in": (
        "The arm's maximum joint velocity is {joint_vel:.6f} rad/s while "
        "placing into container '{target}'. Is this below 0.8 rad/s for "
        "safe insertion without collision?"
    ),

    "open_box": (
        "The arm's maximum joint velocity is {joint_vel:.6f} rad/s while "
        "opening box '{target}'. Is this below 1.0 rad/s for safe "
        "lid removal?"
    ),

    "generic": (
        "The arm's maximum joint velocity is {joint_vel:.6f} rad/s. "
        "Is this below the safe threshold of 1.0 rad/s, indicating "
        "no collision is occurring during action on '{target}'?"
    ),
}


# ═══════════════════════════════════════════════════════════
#  Category 3: GRASP FEASIBILITY
#  Is the gripper in correct state to perform this action?
# ═══════════════════════════════════════════════════════════

GRASP_FEASIBILITY = {

    "grasp": (
        "The gripper openness is {gripper_open:.2f} (0=closed, 1=open) and "
        "end-effector is at {ee_pos}. Is the gripper sufficiently open "
        "(>0.7) and positioned to grasp object '{target}'?"
    ),

    "place": (
        "The gripper openness is {gripper_open:.2f}. To place an object, the "
        "gripper must be closed (<0.3) holding the object. Is the gripper "
        "correctly closed to place onto '{target}'?"
    ),

    "open_drawer": (
        "The gripper openness is {gripper_open:.2f}. To open drawer '{target}', "
        "the gripper should be partially open (0.4-0.7) for handle grip. "
        "Is the gripper in the correct state?"
    ),

    "close_drawer": (
        "The gripper openness is {gripper_open:.2f}. To close drawer '{target}', "
        "the gripper should be partially open (0.4-0.7) to push. "
        "Is the gripper correctly configured?"
    ),

    "pick_and_lift": (
        "The gripper openness is {gripper_open:.2f} at position {ee_pos}. "
        "To pick and lift '{target}', gripper must open (>0.6) for approach "
        "then close. Is the gripper ready?"
    ),

    "move_to": (
        "The gripper openness is {gripper_open:.2f}. For move_to action "
        "toward '{target}', gripper state is not critical. "
        "Is the current gripper state acceptable?"
    ),

    "push": (
        "The gripper openness is {gripper_open:.2f}. To push '{target}', "
        "gripper should be closed (<0.3) for firm contact. "
        "Is the gripper correctly closed?"
    ),

    "slide": (
        "The gripper openness is {gripper_open:.2f}. To slide '{target}', "
        "gripper should be partially closed (0.2-0.5). "
        "Is the gripper in the correct state?"
    ),

    "stack": (
        "The gripper openness is {gripper_open:.2f}. To stack onto '{target}', "
        "gripper must be closed (<0.3) holding the object. "
        "Is the gripper correctly holding the object?"
    ),

    "put_in": (
        "The gripper openness is {gripper_open:.2f}. To put object into "
        "'{target}', gripper must be closed (<0.3) holding the object. "
        "Is the gripper correctly gripping?"
    ),

    "open_box": (
        "The gripper openness is {gripper_open:.2f}. To open box '{target}', "
        "gripper should be partially open (0.5-0.8) for lid grip. "
        "Is the gripper configured correctly?"
    ),

    "generic": (
        "The gripper openness is {gripper_open:.2f} at position {ee_pos}. "
        "Is the gripper in an appropriate state to perform "
        "the action on '{target}'?"
    ),
}


# ═══════════════════════════════════════════════════════════
#  Category 4: SPATIAL CONSTRAINTS
#  Is the EE within acceptable spatial range for this action?
# ═══════════════════════════════════════════════════════════

SPATIAL = {

    "grasp": (
        "The end-effector is at {ee_pos} and workspace center is {ws_center}. "
        "For grasping '{target}', the EE should be within 0.4m of the "
        "workspace center. Is this spatial constraint satisfied?"
    ),

    "place": (
        "The end-effector is at {ee_pos} and workspace center is {ws_center}. "
        "For placing onto '{target}', the EE should be within 0.5m of the "
        "workspace center. Is this satisfied?"
    ),

    "open_drawer": (
        "The end-effector is at {ee_pos}. For opening drawer '{target}', "
        "the EE must be aligned with the drawer handle (within 0.1m lateral). "
        "Is the spatial alignment acceptable?"
    ),

    "close_drawer": (
        "The end-effector is at {ee_pos}. For closing drawer '{target}', "
        "the EE must be in front of the drawer (within 0.15m). "
        "Is the spatial position acceptable?"
    ),

    "pick_and_lift": (
        "The end-effector is at {ee_pos} and workspace center is {ws_center}. "
        "For pick-and-lift of '{target}', the EE should be within 0.4m of "
        "workspace center. Is this spatial constraint met?"
    ),

    "move_to": (
        "The end-effector is at {ee_pos} and workspace center is {ws_center}. "
        "For moving toward '{target}', the EE should remain within the "
        "workspace diagonal distance. Is this satisfied?"
    ),

    "push": (
        "The end-effector is at {ee_pos}. For pushing '{target}', the EE "
        "must be within 0.05m of the object surface. "
        "Is the approach distance acceptable?"
    ),

    "slide": (
        "The end-effector is at {ee_pos}. For sliding '{target}', the EE "
        "must maintain contact within 0.03m of the object. "
        "Is the spatial contact acceptable?"
    ),

    "stack": (
        "The end-effector is at {ee_pos} and workspace center is {ws_center}. "
        "For stacking onto '{target}', the EE must be within 0.05m lateral "
        "of the target. Is this precision constraint met?"
    ),

    "put_in": (
        "The end-effector is at {ee_pos}. For putting object into '{target}', "
        "the EE must be within 0.08m above the container opening. "
        "Is this spatial constraint satisfied?"
    ),

    "open_box": (
        "The end-effector is at {ee_pos}. For opening box '{target}', the EE "
        "must be within 0.1m of the box lid. "
        "Is the approach distance acceptable?"
    ),

    "generic": (
        "The end-effector is at {ee_pos} and workspace center is {ws_center}. "
        "Is the end-effector within acceptable spatial range of the "
        "workspace center to perform the action on '{target}'?"
    ),
}


# ═══════════════════════════════════════════════════════════
#  Category 5: EXECUTION RISK
#  Is it safe to execute this action given current context?
# ═══════════════════════════════════════════════════════════

EXECUTION_RISK = {

    "grasp": (
        "The arm's joint velocity is {joint_vel:.6f} rad/s and gripper "
        "is {gripper_open:.2f} open. For grasping '{target}', is the "
        "overall execution risk acceptable (low velocity, gripper ready)?"
    ),

    "place": (
        "The arm's joint velocity is {joint_vel:.6f} rad/s and gripper "
        "is {gripper_open:.2f} open. For placing onto '{target}', is the "
        "execution risk acceptable (stable arm, object held)?"
    ),

    "open_drawer": (
        "The arm's joint velocity is {joint_vel:.6f} rad/s at position {ee_pos}. "
        "For opening drawer '{target}', is the execution risk acceptable "
        "(arm stable, correct approach direction)?"
    ),

    "close_drawer": (
        "The arm's joint velocity is {joint_vel:.6f} rad/s at position {ee_pos}. "
        "For closing drawer '{target}', is the execution risk low enough "
        "to proceed safely?"
    ),

    "pick_and_lift": (
        "The arm's joint velocity is {joint_vel:.6f} rad/s. For pick-and-lift "
        "of '{target}', is the execution risk acceptable (stable approach, "
        "no high velocity)?"
    ),

    "move_to": (
        "The arm's joint velocity is {joint_vel:.6f} rad/s during transit "
        "to '{target}'. Is the execution risk acceptable for this "
        "movement action?"
    ),

    "push": (
        "The arm's joint velocity is {joint_vel:.6f} rad/s for pushing "
        "'{target}'. Is the execution risk acceptable (controlled speed, "
        "stable contact)?"
    ),

    "slide": (
        "The arm's joint velocity is {joint_vel:.6f} rad/s for sliding "
        "'{target}'. Is the execution risk acceptable for maintaining "
        "contact without losing control?"
    ),

    "stack": (
        "The arm's joint velocity is {joint_vel:.6f} rad/s for stacking "
        "onto '{target}'. Is the execution risk acceptable for this "
        "precision placement?"
    ),

    "put_in": (
        "The arm's joint velocity is {joint_vel:.6f} rad/s for inserting "
        "object into '{target}'. Is the execution risk acceptable "
        "for this insertion action?"
    ),

    "open_box": (
        "The arm's joint velocity is {joint_vel:.6f} rad/s for opening "
        "box '{target}'. Is the execution risk acceptable for lid removal?"
    ),

    "generic": (
        "The arm's joint velocity is {joint_vel:.6f} rad/s at position {ee_pos}. "
        "Is the execution risk acceptable to safely proceed with "
        "action on '{target}'?"
    ),
}


# ═══════════════════════════════════════════════════════════
#  Template Library — Combined
# ═══════════════════════════════════════════════════════════

TEMPLATE_LIBRARY = {
    "reachability": REACHABILITY,
    "collision":    COLLISION,
    "grasp":        GRASP_FEASIBILITY,
    "spatial":      SPATIAL,
    "exec_risk":    EXECUTION_RISK,
}

# All action types (12 variants)
ACTION_TYPES = [
    "grasp", "place", "open_drawer", "close_drawer",
    "pick_and_lift", "move_to", "push", "slide",
    "stack", "put_in", "open_box", "generic",
]


def get_question(category: str, action_type: str, **kwargs) -> str:
    """
    Get instantiated question for given category and action type.

    Parameters
    ----------
    category    : one of 'reachability', 'collision', 'grasp',
                  'spatial', 'exec_risk'
    action_type : one of ACTION_TYPES (falls back to 'generic')
    **kwargs    : template parameters (target, ee_pos, etc.)

    Returns
    -------
    Instantiated question string.
    """
    cat_templates = TEMPLATE_LIBRARY.get(category, {})
    # Use action-specific variant or fall back to generic
    template = cat_templates.get(action_type, cat_templates.get("generic", ""))
    if not template:
        return f"Is it safe to perform {action_type} on {kwargs.get('target', 'target')}?"
    try:
        return template.format(**kwargs)
    except KeyError:
        return template


def count_variants():
    """Count total variants in library."""
    total = 0
    for cat, variants in TEMPLATE_LIBRARY.items():
        total += len(variants)
        print(f"  {cat:15s}: {len(variants)} variants")
    print(f"  {'TOTAL':15s}: {total} variants")
    return total


if __name__ == "__main__":
    print("RREM Template Library Summary:")
    count_variants()
    print()
    print("Example — grasp reachability:")
    print(get_question(
        "reachability", "grasp",
        target="rubbish",
        ee_pos=[0.279, -0.008, 1.472],
        ws_min=[-0.275, -0.655, 0.752],
        ws_max=[0.775, 0.655, 1.752],
        ws_center=[0.25, 0.0, 1.252],
        joint_vel=0.0043,
        gripper_open=1.0,
    ))
