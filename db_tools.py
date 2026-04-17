import database
from models import Success, Error
from enum import Enum


class DBToolName(Enum):
    # Tasks
    CREATE_TASK = "create_task"
    GET_TASKS_TODAY = "get_tasks_today"
    GET_HIGH_PRIORITY_TASKS = "get_high_priority_tasks"
    GET_ALL_PENDING_TASKS = "get_all_pending_tasks"
    UPDATE_TASK = "update_task"
    UPDATE_TASK_STATUS = "update_task_status"
    UPDATE_TASK_PRIORITY = "update_task_priority"
    DELETE_TASK = "delete_task"
    AUTO_UPDATE_PRIORITIES = "auto_update_priorities"
    # Events
    CREATE_EVENT = "create_event"
    UPDATE_EVENT = "update_event"
    GET_EVENTS_TODAY = "get_events_today"
    GET_UPCOMING_EVENTS = "get_upcoming_events"
    DELETE_EVENT = "delete_event"
    # Routines
    CREATE_ROUTINE = "create_routine"
    UPDATE_ROUTINE = "update_routine"
    GET_ROUTINES_TODAY = "get_routines_today"
    COMPLETE_ROUTINE = "complete_routine"
    GET_STREAK = "get_streak"
    DELETE_ROUTINE = "delete_routine"
    # Goals
    CREATE_GOAL = "create_goal"
    UPDATE_GOAL = "update_goal"
    UPDATE_GOAL_PROGRESS = "update_goal_progress"
    GET_ACTIVE_GOALS = "get_active_goals"
    DELETE_GOAL = "delete_goal"
    # Notes
    CREATE_NOTE = "create_note"
    UPDATE_NOTE = "update_note"
    GET_NOTES_FOR = "get_notes_for"
    GET_ALL_NOTES = "get_all_notes"
    DELETE_NOTE = "delete_note"
    # Daily Context
    SAVE_DAILY_CONTEXT = "save_daily_context"
    GET_TODAY_CONTEXT = "get_today_context"
    GET_RECENT_CONTEXT = "get_recent_context"
    # User Patterns
    SAVE_PATTERN = "save_pattern"
    GET_PATTERNS = "get_patterns"
    # Briefing
    GET_BRIEFING_DATA = "get_briefing_data"


# ── Tasks ────────────────────────────────────────────

def create_task(title, description=None, priority="athena_decided",
                due_date=None, due_time=None, is_flexible=True):
    try:
        result = database.create_task(title, description, priority,
                                      due_date, due_time, is_flexible)
        return Success(data=result, tool_name=DBToolName.CREATE_TASK.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.CREATE_TASK.value)

def get_tasks_today():
    try:
        result = database.get_tasks_today()
        return Success(data=result, tool_name=DBToolName.GET_TASKS_TODAY.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.GET_TASKS_TODAY.value)

def get_high_priority_tasks():
    try:
        result = database.get_high_priority_tasks()
        return Success(data=result, tool_name=DBToolName.GET_HIGH_PRIORITY_TASKS.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.GET_HIGH_PRIORITY_TASKS.value)

def get_all_pending_tasks():
    try:
        result = database.get_all_pending_tasks()
        return Success(data=result, tool_name=DBToolName.GET_ALL_PENDING_TASKS.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.GET_ALL_PENDING_TASKS.value)

def update_task(task_id, **kwargs):
    try:
        result = database.update_task(task_id, **kwargs)
        return Success(data=result, tool_name=DBToolName.UPDATE_TASK.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.UPDATE_TASK.value)

def update_task_status(task_id, status):
    try:
        result = database.update_task_status(task_id, status)
        return Success(data=result, tool_name=DBToolName.UPDATE_TASK_STATUS.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.UPDATE_TASK_STATUS.value)

def update_task_priority(task_id, priority):
    try:
        result = database.update_task_priority(task_id, priority)
        return Success(data=result, tool_name=DBToolName.UPDATE_TASK_PRIORITY.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.UPDATE_TASK_PRIORITY.value)

def delete_task(task_id):
    try:
        result = database.delete_task(task_id)
        return Success(data=result, tool_name=DBToolName.DELETE_TASK.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.DELETE_TASK.value)

def auto_update_priorities():
    try:
        result = database.auto_update_priorities()
        return Success(data=result, tool_name=DBToolName.AUTO_UPDATE_PRIORITIES.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.AUTO_UPDATE_PRIORITIES.value)

# ── Events ───────────────────────────────────────────

def create_event(title, start_time, end_time=None,
                 location=None, notes=None, related_task_id=None):
    try:
        result = database.create_event(title, start_time, end_time,
                                       location, notes, related_task_id)
        return Success(data=result, tool_name=DBToolName.CREATE_EVENT.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.CREATE_EVENT.value)
    
def update_event(event_id, **kwargs):
    try:
        result = database.update_event(event_id, **kwargs)
        return Success(data=result, tool_name=DBToolName.UPDATE_EVENT.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.UPDATE_EVENT.value)

def get_events_today():
    try:
        result = database.get_events_today()
        return Success(data=result, tool_name=DBToolName.GET_EVENTS_TODAY.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.GET_EVENTS_TODAY.value)

def get_upcoming_events(days=7):
    try:
        result = database.get_upcoming_events(days)
        return Success(data=result, tool_name=DBToolName.GET_UPCOMING_EVENTS.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.GET_UPCOMING_EVENTS.value)

def delete_event(event_id):
    try:
        result = database.delete_event(event_id)
        return Success(data=result, tool_name=DBToolName.DELETE_EVENT.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.DELETE_EVENT.value)

# ── Routines ─────────────────────────────────────────

def create_routine(title, frequency, preferred_time=None, duration_minutes=None):
    try:
        result = database.create_routine(title, frequency, preferred_time, duration_minutes)
        return Success(data=result, tool_name=DBToolName.CREATE_ROUTINE.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.CREATE_ROUTINE.value)
    
def update_routine(routine_id, **kwargs):
    try:
        result = database.update_routine(routine_id, **kwargs)
        return Success(data=result, tool_name=DBToolName.UPDATE_ROUTINE.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.UPDATE_ROUTINE.value)

def get_routines_today():
    try:
        result = database.get_routines_today()
        return Success(data=result, tool_name=DBToolName.GET_ROUTINES_TODAY.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.GET_ROUTINES_TODAY.value)

def complete_routine(routine_id):
    try:
        result = database.complete_routine(routine_id)
        return Success(data=result, tool_name=DBToolName.COMPLETE_ROUTINE.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.COMPLETE_ROUTINE.value)

def get_streak(routine_id):
    try:
        result = database.get_streak(routine_id)
        return Success(data=result, tool_name=DBToolName.GET_STREAK.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.GET_STREAK.value)

def delete_routine(routine_id):
    try:
        result = database.delete_routine(routine_id)
        return Success(data=result, tool_name=DBToolName.DELETE_ROUTINE.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.DELETE_ROUTINE.value)

# ── Goals ────────────────────────────────────────────

def create_goal(title, target, deadline=None, related_routine_id=None):
    try:
        result = database.create_goal(title, target, deadline, related_routine_id)
        return Success(data=result, tool_name=DBToolName.CREATE_GOAL.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.CREATE_GOAL.value)
    
def update_goal(goal_id, **kwargs):
    try:
        result = database.update_goal(goal_id, **kwargs)
        return Success(data=result, tool_name=DBToolName.UPDATE_GOAL.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.UPDATE_GOAL.value)

def update_goal_progress(goal_id, progress):
    try:
        result = database.update_goal_progress(goal_id, progress)
        return Success(data=result, tool_name=DBToolName.UPDATE_GOAL_PROGRESS.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.UPDATE_GOAL_PROGRESS.value)

def get_active_goals():
    try:
        result = database.get_active_goals()
        return Success(data=result, tool_name=DBToolName.GET_ACTIVE_GOALS.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.GET_ACTIVE_GOALS.value)

def delete_goal(goal_id):
    try:
        result = database.delete_goal(goal_id)
        return Success(data=result, tool_name=DBToolName.DELETE_GOAL.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.DELETE_GOAL.value)

# ── Notes ────────────────────────────────────────────

def create_note(content, title=None, linked_to_type=None, linked_to_id=None):
    try:
        result = database.create_note(content, title, linked_to_type, linked_to_id)
        return Success(data=result, tool_name=DBToolName.CREATE_NOTE.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.CREATE_NOTE.value)
    
def update_note(note_id, **kwargs):
    try:
        result = database.update_note(note_id, **kwargs)
        return Success(data=result, tool_name=DBToolName.UPDATE_NOTE.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.UPDATE_NOTE.value)

def get_notes_for(linked_to_type, linked_to_id):
    try:
        result = database.get_notes_for(linked_to_type, linked_to_id)
        return Success(data=result, tool_name=DBToolName.GET_NOTES_FOR.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.GET_NOTES_FOR.value)

def get_all_notes():
    try:
        result = database.get_all_notes()
        return Success(data=result, tool_name=DBToolName.GET_ALL_NOTES.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.GET_ALL_NOTES.value)

def delete_note(note_id):
    try:
        result = database.delete_note(note_id)
        return Success(data=result, tool_name=DBToolName.DELETE_NOTE.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.DELETE_NOTE.value)

# ── Daily Context ────────────────────────────────────

def save_daily_context(wake_time=None, sleep_duration=None,
                       sleep_quality=None, day_type="normal", notes=None):
    try:
        result = database.save_daily_context(wake_time, sleep_duration,
                                             sleep_quality, day_type, notes)
        return Success(data=result, tool_name=DBToolName.SAVE_DAILY_CONTEXT.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.SAVE_DAILY_CONTEXT.value)

def get_today_context():
    try:
        result = database.get_today_context()
        return Success(data=result, tool_name=DBToolName.GET_TODAY_CONTEXT.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.GET_TODAY_CONTEXT.value)

def get_recent_context(days=7):
    try:
        result = database.get_recent_context(days)
        return Success(data=result, tool_name=DBToolName.GET_RECENT_CONTEXT.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.GET_RECENT_CONTEXT.value)

# ── User Patterns ────────────────────────────────────

def save_pattern(pattern_type, description, learned_from=None, confidence=0.5):
    try:
        result = database.save_pattern(pattern_type, description, learned_from, confidence)
        return Success(data=result, tool_name=DBToolName.SAVE_PATTERN.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.SAVE_PATTERN.value)

def get_patterns():
    try:
        result = database.get_patterns()
        return Success(data=result, tool_name=DBToolName.GET_PATTERNS.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.GET_PATTERNS.value)

# ── Briefing ─────────────────────────────────────────

def get_briefing_data():
    try:
        result = database.get_briefing_data()
        return Success(data=result, tool_name=DBToolName.GET_BRIEFING_DATA.value)
    except Exception as e:
        return Error(message=str(e), tool_name=DBToolName.GET_BRIEFING_DATA.value)


# ── Dispatcher ───────────────────────────────────────

def run_db_tool(tool_name, tool_input):
    match tool_name:
        # Tasks
        case DBToolName.CREATE_TASK.value:
            return create_task(**tool_input)
        case DBToolName.GET_TASKS_TODAY.value:
            return get_tasks_today(**tool_input)
        case DBToolName.GET_HIGH_PRIORITY_TASKS.value:
            return get_high_priority_tasks(**tool_input)
        case DBToolName.GET_ALL_PENDING_TASKS.value:
            return get_all_pending_tasks(**tool_input)
        case DBToolName.UPDATE_TASK.value:
            return update_task(**tool_input)
        case DBToolName.UPDATE_TASK_STATUS.value:
            return update_task_status(**tool_input)
        case DBToolName.UPDATE_TASK_PRIORITY.value:
            return update_task_priority(**tool_input)
        case DBToolName.DELETE_TASK.value:
            return delete_task(**tool_input)
        case DBToolName.AUTO_UPDATE_PRIORITIES.value:
            return auto_update_priorities(**tool_input)
        # Events
        case DBToolName.CREATE_EVENT.value:
            return create_event(**tool_input)
        case DBToolName.UPDATE_EVENT.value:
            return update_event(**tool_input)
        case DBToolName.GET_EVENTS_TODAY.value:
            return get_events_today(**tool_input)
        case DBToolName.GET_UPCOMING_EVENTS.value:
            return get_upcoming_events(**tool_input)
        case DBToolName.DELETE_EVENT.value:
            return delete_event(**tool_input)
        # Routines
        case DBToolName.CREATE_ROUTINE.value:
            return create_routine(**tool_input)
        case DBToolName.UPDATE_ROUTINE.value:
            return update_routine(**tool_input)
        case DBToolName.GET_ROUTINES_TODAY.value:
            return get_routines_today(**tool_input)
        case DBToolName.COMPLETE_ROUTINE.value:
            return complete_routine(**tool_input)
        case DBToolName.GET_STREAK.value:
            return get_streak(**tool_input)
        case DBToolName.DELETE_ROUTINE.value:
            return delete_routine(**tool_input)
        # Goals
        case DBToolName.CREATE_GOAL.value:
            return create_goal(**tool_input)
        case DBToolName.UPDATE_GOAL.value:
            return update_goal(**tool_input)
        case DBToolName.UPDATE_GOAL_PROGRESS.value:
            return update_goal_progress(**tool_input)
        case DBToolName.GET_ACTIVE_GOALS.value:
            return get_active_goals(**tool_input)
        case DBToolName.DELETE_GOAL.value:
            return delete_goal(**tool_input)
        # Notes
        case DBToolName.CREATE_NOTE.value:
            return create_note(**tool_input)
        case DBToolName.UPDATE_NOTE.value:
            return update_note(**tool_input)
        case DBToolName.GET_NOTES_FOR.value:
            return get_notes_for(**tool_input)
        case DBToolName.GET_ALL_NOTES.value:
            return get_all_notes(**tool_input)
        case DBToolName.DELETE_NOTE.value:
            return delete_note(**tool_input)
        # Daily Context
        case DBToolName.SAVE_DAILY_CONTEXT.value:
            return save_daily_context(**tool_input)
        case DBToolName.GET_TODAY_CONTEXT.value:
            return get_today_context(**tool_input)
        case DBToolName.GET_RECENT_CONTEXT.value:
            return get_recent_context(**tool_input)
        # User Patterns
        case DBToolName.SAVE_PATTERN.value:
            return save_pattern(**tool_input)
        case DBToolName.GET_PATTERNS.value:
            return get_patterns(**tool_input)
        # Briefing
        case DBToolName.GET_BRIEFING_DATA.value:
            return get_briefing_data(**tool_input)
        case _:
            return Error(message=f"Unknown db tool: {tool_name}", tool_name=tool_name)
