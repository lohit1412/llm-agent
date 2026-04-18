from supabase import create_client
import config
from datetime import date, datetime, timedelta

supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def test_connection():
    result = supabase.table("tasks").select("*").execute()
    return result.data

# ── Tasks ────────────────────────────────────────────

def create_task(title, description=None, priority="athena_decided",
                due_date=None, due_time=None, is_flexible=True):
    result = supabase.table("tasks").insert({
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "due_time": due_time,
        "is_flexible": is_flexible,
        "status": "pending"
    }).execute()
    return result.data

def get_tasks_today():
    today = date.today().isoformat()
    result = supabase.table("tasks").select("*").lte("due_date", today).eq("status", "pending").execute()
    return result.data

def get_high_priority_tasks():
    result = supabase.table("tasks").select("*").in_("priority", ["high", "critical"]).eq("status", "pending").execute()
    return result.data

def get_all_pending_tasks():
    result = supabase.table("tasks").select("*").eq("status", "pending").execute()
    return result.data

def update_task(task_id, **kwargs):
    result = supabase.table("tasks").update(kwargs).eq("id", task_id).execute()
    return result.data

def update_task_status(task_id, status):
    result = supabase.table("tasks").update({"status": status}).eq("id", task_id).execute()
    return result.data

def update_task_priority(task_id, priority):
    result = supabase.table("tasks").update({"priority": priority}).eq("id", task_id).execute()
    return result.data

def delete_task(task_id):
    result = supabase.table("tasks").delete().eq("id", task_id).execute()
    return result.data

def auto_update_priorities():
    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    # Overdue → critical
    supabase.table("tasks").update({"priority": "critical"}).lt("due_date", today).eq("status", "pending").execute()
    # Due tomorrow → high
    supabase.table("tasks").update({"priority": "high"}).eq("due_date", tomorrow).eq("status", "pending").execute()

# ── Events ───────────────────────────────────────────

def create_event(title, start_time, end_time=None,
                location=None, notes=None, related_task_id=None):
    result = supabase.table("events").insert({
        "title": title,
        "start_time": start_time,
        "end_time": end_time,
        "location": location,
        "notes": notes,
        "related_task_id": related_task_id
    }).execute()
    return result.data

def get_events_today():
    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    result = supabase.table("events").select("*").gte("start_time", today).lt("start_time", tomorrow).execute()
    return result.data

def update_event(event_id, **kwargs):
    result = supabase.table("events").update(kwargs).eq("id", event_id).execute()
    return result.data

def get_upcoming_events(days=7):
    today = date.today().isoformat()
    future = (date.today() + timedelta(days=days)).isoformat()
    result = supabase.table("events").select("*").gte("start_time", today).lte("start_time", future).execute()
    return result.data

def delete_event(event_id):
    result = supabase.table("events").delete().eq("id", event_id).execute()
    return result.data

# ── Routines ─────────────────────────────────────────

def create_routine(title, frequency, preferred_time=None, duration_minutes=None):
    result = supabase.table("routines").insert({
        "title": title,
        "frequency": frequency,
        "preferred_time": preferred_time,
        "duration_minutes": duration_minutes,
        "current_streak": 0,
        "longest_streak": 0
    }).execute()
    return result.data

def get_routines_today():
    result = supabase.table("routines").select("*").execute()
    return result.data

def update_routine(routine_id, **kwargs):
    result = supabase.table("routines").update(kwargs).eq("id", routine_id).execute()
    return result.data

def complete_routine(routine_id):
    today = date.today().isoformat()
    # Get current routine
    routine = supabase.table("routines").select("*").eq("id", routine_id).execute().data
    if not routine:
        return None
    routine = routine[0]
    
    last_completed = routine.get("last_completed")
    current_streak = routine.get("current_streak", 0)
    longest_streak = routine.get("longest_streak", 0)
    
    # Check if completed yesterday — continue streak
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    if last_completed == yesterday or last_completed == today:
        new_streak = current_streak + 1
    else:
        new_streak = 1  # reset streak
    
    new_longest = max(new_streak, longest_streak)
    
    result = supabase.table("routines").update({
        "last_completed": today,
        "current_streak": new_streak,
        "longest_streak": new_longest
    }).eq("id", routine_id).execute()
    return result.data

def get_streak(routine_id):
    result = supabase.table("routines").select("current_streak, longest_streak, last_completed").eq("id", routine_id).execute()
    return result.data

def delete_routine(routine_id):
    result = supabase.table("routines").delete().eq("id", routine_id).execute()
    return result.data

# ── Goals ────────────────────────────────────────────

def create_goal(title, target, deadline=None, related_routine_id=None):
    result = supabase.table("goals").insert({
        "title": title,
        "target": target,
        "deadline": deadline,
        "related_routine_id": related_routine_id,
        "current_progress": 0
    }).execute()
    return result.data

def update_goal(goal_id, **kwargs):
    result = supabase.table("goals").update(kwargs).eq("id", goal_id).execute()
    return result.data

def update_goal_progress(goal_id, progress):
    result = supabase.table("goals").update({"current_progress": progress}).eq("id", goal_id).execute()
    return result.data

def get_active_goals():
    today = date.today().isoformat()
    result = supabase.table("goals").select("*").or_(f"deadline.gte.{today},deadline.is.null").execute()
    return result.data

def delete_goal(goal_id):
    result = supabase.table("goals").delete().eq("id", goal_id).execute()
    return result.data

# ── Notes ────────────────────────────────────────────

def create_note(content, title=None, linked_to_type=None, linked_to_id=None):
    result = supabase.table("notes").insert({
        "title": title,
        "content": content,
        "linked_to_type": linked_to_type,
        "linked_to_id": linked_to_id
    }).execute()
    return result.data

def update_note(note_id, **kwargs):
    result = supabase.table("notes").update(kwargs).eq("id", note_id).execute()
    return result.data

def get_notes_for(linked_to_type, linked_to_id):
    result = supabase.table("notes").select("*").eq("linked_to_type", linked_to_type).eq("linked_to_id", str(linked_to_id)).execute()
    return result.data

def get_all_notes():
    result = supabase.table("notes").select("*").order("created_at", desc=True).execute()
    return result.data

def delete_note(note_id):
    result = supabase.table("notes").delete().eq("id", note_id).execute()
    return result.data

# ── Daily Context ────────────────────────────────────

def save_daily_context(wake_time=None, sleep_duration=None,
                       sleep_quality=None, day_type="normal", notes=None):
    today = date.today().isoformat()
    # Upsert — update if exists, insert if not
    result = supabase.table("daily_context").upsert({
        "date": today,
        "wake_time": wake_time,
        "sleep_duration_hours": sleep_duration,
        "sleep_quality": sleep_quality,
        "day_type": day_type,
        "notes": notes
    }).execute()
    return result.data

def get_today_context():
    today = date.today().isoformat()
    result = supabase.table("daily_context").select("*").eq("date", today).execute()
    return result.data[0] if result.data else None

def get_recent_context(days=7):
    past = (date.today() - timedelta(days=days)).isoformat()
    result = supabase.table("daily_context").select("*").gte("date", past).order("date", desc=True).execute()
    return result.data

# ── User Patterns ────────────────────────────────────

def save_pattern(pattern_type, description, learned_from=None, confidence=0.5):
    # Check if pattern type already exists — update if so
    existing = supabase.table("user_patterns").select("*").eq("pattern_type", pattern_type).execute()
    if existing.data:
        result = supabase.table("user_patterns").update({
            "description": description,
            "confidence": confidence
        }).eq("pattern_type", pattern_type).execute()
    else:
        result = supabase.table("user_patterns").insert({
            "pattern_type": pattern_type,
            "description": description,
            "learned_from": learned_from,
            "confidence": confidence
        }).execute()
    return result.data

def get_patterns():
    result = supabase.table("user_patterns").select("*").order("confidence", desc=True).execute()
    return result.data

# ── Briefing Data ────────────────────────────────────

def get_briefing_data():
    """Single function that pulls everything needed for morning briefing"""
    return {
        "tasks_today": get_tasks_today(),
        "high_priority": get_high_priority_tasks(),
        "events_today": get_events_today(),
        "routines": get_routines_today(),
        "goals": get_active_goals(),
        "context": get_today_context(),
        "patterns": get_patterns()
    }

# ── User Memory ──────────────────────────────────────

def save_summary_to_db(summary, user_id="default_user"):
    existing = supabase.table("user_memory").select("*").eq("user_id", user_id).execute()
    if existing.data:
        result = supabase.table("user_memory").update({
            "summary": summary,
            "updated_at": datetime.now().isoformat()
        }).eq("user_id", user_id).execute()
    else:
        result = supabase.table("user_memory").insert({
            "user_id": user_id,
            "summary": summary
        }).execute()
    return result.data

def load_summary_from_db(user_id="default_user"):
    result = supabase.table("user_memory").select("summary").eq("user_id", user_id).execute()
    if result.data:
        return result.data[0]["summary"]
    return None

# ── Sessions ─────────────────────────────────────────

def save_session_to_db(session_id, messages, user_id="default_user"):
    import json
    # Strip embeddings before saving
    clean = [{"role": m["role"], "content": m["content"]}
             for m in messages
             if isinstance(m.get("content"), str)]
    existing = supabase.table("sessions").select("id").eq("id", session_id).execute()
    if existing.data:
        result = supabase.table("sessions").update({
            "messages": json.dumps(clean),
            "last_active": datetime.now().isoformat()
        }).eq("id", session_id).execute()
    else:
        result = supabase.table("sessions").insert({
            "id": session_id,
            "user_id": user_id,
            "messages": json.dumps(clean)
        }).execute()
    return result.data

def load_session_from_db(session_id):
    import json
    result = supabase.table("sessions").select("*").eq("id", session_id).execute()
    if result.data:
        messages = result.data[0]["messages"]
        if isinstance(messages, str):
            return json.loads(messages)
        return messages
    return None

# ── Embeddings ───────────────────────────────────────

def save_embedding(content, role, embedding, user_id="default_user"):
    result = supabase.table("embeddings").insert({
        "user_id": user_id,
        "content": content,
        "role": role,
        "embedding": embedding
    }).execute()
    return result.data

def search_embeddings(query_embedding, top_k=5, user_id="default_user"):
    result = supabase.rpc("match_embeddings", {
        "query_embedding": query_embedding,
        "match_count": top_k,
        "user_id_filter": user_id
    }).execute()
    return result.data