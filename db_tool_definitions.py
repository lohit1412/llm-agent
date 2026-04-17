from db_tools import DBToolName

db_tool_definitions = [
    {
        "name": DBToolName.CREATE_TASK.value,
        "description": "Create a new task. Use when the user mentions something they need to do, a reminder, or a to-do item.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "The task title"},
                "description": {"type": "string", "description": "Optional details about the task"},
                "priority": {"type": "string", "description": "Priority: high, medium, low, or athena_decided"},
                "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format"},
                "due_time": {"type": "string", "description": "Due time in HH:MM format"},
                "is_flexible": {"type": "boolean", "description": "Whether this task can be rescheduled"}
            },
            "required": ["title"]
        }
    },
    {
        "name": DBToolName.GET_TASKS_TODAY.value,
        "description": "Get all pending tasks due today or overdue. Use when user asks what they need to do today.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": DBToolName.GET_HIGH_PRIORITY_TASKS.value,
        "description": "Get all high priority and critical pending tasks.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": DBToolName.GET_ALL_PENDING_TASKS.value,
        "description": "Get all pending tasks regardless of due date.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": DBToolName.UPDATE_TASK.value,
        "description": "Update any field on an existing task including title, due_date, due_time, priority, status, description or is_flexible.",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "The task UUID"},
                "title": {"type": "string", "description": "New title"},
                "due_date": {"type": "string", "description": "New due date in YYYY-MM-DD format"},
                "due_time": {"type": "string", "description": "New due time in HH:MM format"},
                "priority": {"type": "string", "description": "New priority"},
                "status": {"type": "string", "description": "New status"},
                "description": {"type": "string", "description": "New description"},
                "is_flexible": {"type": "boolean", "description": "Whether task is flexible"}
            },
            "required": ["task_id"]
        }
    },
    {
        "name": DBToolName.UPDATE_TASK_STATUS.value,
        "description": "Update a task status. Use when user says they completed, snoozed, or cancelled a task.",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "The task UUID"},
                "status": {"type": "string", "description": "New status: pending, in_progress, done, snoozed"}
            },
            "required": ["task_id", "status"]
        }
    },
    {
        "name": DBToolName.UPDATE_TASK_PRIORITY.value,
        "description": "Update a task priority manually.",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "The task UUID"},
                "priority": {"type": "string", "description": "New priority: critical, high, medium, low"}
            },
            "required": ["task_id", "priority"]
        }
    },
    {
        "name": DBToolName.DELETE_TASK.value,
        "description": "Delete a task permanently.",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "The task UUID"}
            },
            "required": ["task_id"]
        }
    },
    {
        "name": DBToolName.AUTO_UPDATE_PRIORITIES.value,
        "description": "Automatically update task priorities based on due dates. Run this daily.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": DBToolName.CREATE_EVENT.value,
        "description": "Create a calendar event. Use when user mentions a meeting, appointment, match, or scheduled activity.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Event title"},
                "start_time": {"type": "string", "description": "Start time in ISO format: YYYY-MM-DDTHH:MM:SS"},
                "end_time": {"type": "string", "description": "End time in ISO format"},
                "location": {"type": "string", "description": "Event location"},
                "notes": {"type": "string", "description": "Notes or briefing context for the event"},
                "related_task_id": {"type": "string", "description": "UUID of related task if any"}
            },
            "required": ["title", "start_time"]
        }
    },
    {
        "name": DBToolName.UPDATE_EVENT.value,
        "description": "Update any field on an existing event including title, start_time, end_time, location or notes.",
        "input_schema": {
            "type": "object",
            "properties": {
                "event_id": {"type": "string", "description": "The event UUID"},
                "title": {"type": "string", "description": "New title"},
                "start_time": {"type": "string", "description": "New start time in ISO format"},
                "end_time": {"type": "string", "description": "New end time in ISO format"},
                "location": {"type": "string", "description": "New location"},
                "notes": {"type": "string", "description": "New notes"}
            },
            "required": ["event_id"]
        }
    },
    {
        "name": DBToolName.GET_EVENTS_TODAY.value,
        "description": "Get all events happening today.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": DBToolName.GET_UPCOMING_EVENTS.value,
        "description": "Get upcoming events for the next N days.",
        "input_schema": {
            "type": "object",
            "properties": {
                "days": {"type": "integer", "description": "Number of days to look ahead. Default 7."}
            }
        }
    },
    {
        "name": DBToolName.DELETE_EVENT.value,
        "description": "Delete a calendar event.",
        "input_schema": {
            "type": "object",
            "properties": {
                "event_id": {"type": "string", "description": "The event UUID"}
            },
            "required": ["event_id"]
        }
    },
    {
        "name": DBToolName.CREATE_ROUTINE.value,
        "description": "Create a recurring routine. Use when user mentions a regular habit like gym, reading, studying.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Routine title e.g. Gym, Morning run"},
                "frequency": {"type": "string", "description": "How often: daily, weekly, weekdays, weekends"},
                "preferred_time": {"type": "string", "description": "Preferred time in HH:MM format"},
                "duration_minutes": {"type": "integer", "description": "How long in minutes"}
            },
            "required": ["title", "frequency"]
        }
    },
    {
        "name": DBToolName.UPDATE_ROUTINE.value,
        "description": "Update any field on an existing routine including title, frequency, preferred_time or duration_minutes.",
        "input_schema": {
            "type": "object",
            "properties": {
                "routine_id": {"type": "string", "description": "The routine UUID"},
                "title": {"type": "string", "description": "New title"},
                "frequency": {"type": "string", "description": "New frequency"},
                "preferred_time": {"type": "string", "description": "New preferred time in HH:MM format"},
                "duration_minutes": {"type": "integer", "description": "New duration in minutes"}
            },
            "required": ["routine_id"]
        }
    },
    {
        "name": DBToolName.GET_ROUTINES_TODAY.value,
        "description": "Get all routines scheduled for today.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": DBToolName.COMPLETE_ROUTINE.value,
        "description": "Mark a routine as completed for today. Updates streak.",
        "input_schema": {
            "type": "object",
            "properties": {
                "routine_id": {"type": "string", "description": "The routine UUID"}
            },
            "required": ["routine_id"]
        }
    },
    {
        "name": DBToolName.GET_STREAK.value,
        "description": "Get current and longest streak for a routine.",
        "input_schema": {
            "type": "object",
            "properties": {
                "routine_id": {"type": "string", "description": "The routine UUID"}
            },
            "required": ["routine_id"]
        }
    },
    {
        "name": DBToolName.DELETE_ROUTINE.value,
        "description": "Delete a routine.",
        "input_schema": {
            "type": "object",
            "properties": {
                "routine_id": {"type": "string", "description": "The routine UUID"}
            },
            "required": ["routine_id"]
        }
    },
    {
        "name": DBToolName.CREATE_GOAL.value,
        "description": "Create a goal. Use when user mentions a target they want to achieve.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Goal title"},
                "target": {"type": "string", "description": "What success looks like e.g. 4x gym per week"},
                "deadline": {"type": "string", "description": "Deadline in YYYY-MM-DD format"},
                "related_routine_id": {"type": "string", "description": "UUID of related routine if any"}
            },
            "required": ["title", "target"]
        }
    },
    {
        "name": DBToolName.UPDATE_GOAL.value,
        "description": "Update any field on an existing goal including title, target, deadline or progress.",
        "input_schema": {
            "type": "object",
            "properties": {
                "goal_id": {"type": "string", "description": "The goal UUID"},
                "title": {"type": "string", "description": "New title"},
                "target": {"type": "string", "description": "New target"},
                "deadline": {"type": "string", "description": "New deadline in YYYY-MM-DD format"},
                "current_progress": {"type": "integer", "description": "Updated progress value"}
            },
            "required": ["goal_id"]
        }
    },
    {
        "name": DBToolName.UPDATE_GOAL_PROGRESS.value,
        "description": "Update progress toward a goal.",
        "input_schema": {
            "type": "object",
            "properties": {
                "goal_id": {"type": "string", "description": "The goal UUID"},
                "progress": {"type": "integer", "description": "Current progress value"}
            },
            "required": ["goal_id", "progress"]
        }
    },
    {
        "name": DBToolName.GET_ACTIVE_GOALS.value,
        "description": "Get all active goals that have not expired.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": DBToolName.DELETE_GOAL.value,
        "description": "Delete a goal.",
        "input_schema": {
            "type": "object",
            "properties": {
                "goal_id": {"type": "string", "description": "The goal UUID"}
            },
            "required": ["goal_id"]
        }
    },
    {
        "name": DBToolName.CREATE_NOTE.value,
        "description": "Save a note. Use when user shares information worth remembering that is not a task or event.",
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "The note content"},
                "title": {"type": "string", "description": "Optional note title"},
                "linked_to_type": {"type": "string", "description": "Type of linked item: task, event, routine, general"},
                "linked_to_id": {"type": "string", "description": "UUID of linked item"}
            },
            "required": ["content"]
        }
    },
    {
        "name": DBToolName.UPDATE_NOTE.value,
        "description": "Update an existing note's title or content.",
        "input_schema": {
            "type": "object",
            "properties": {
                "note_id": {"type": "string", "description": "The note UUID"},
                "title": {"type": "string", "description": "New title"},
                "content": {"type": "string", "description": "New content"}
            },
            "required": ["note_id"]
        }
    },
    {
        "name": DBToolName.GET_NOTES_FOR.value,
        "description": "Get notes linked to a specific task, event or routine.",
        "input_schema": {
            "type": "object",
            "properties": {
                "linked_to_type": {"type": "string", "description": "Type: task, event, routine"},
                "linked_to_id": {"type": "string", "description": "UUID of the linked item"}
            },
            "required": ["linked_to_type", "linked_to_id"]
        }
    },
    {
        "name": DBToolName.GET_ALL_NOTES.value,
        "description": "Get all saved notes.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": DBToolName.DELETE_NOTE.value,
        "description": "Delete a note.",
        "input_schema": {
            "type": "object",
            "properties": {
                "note_id": {"type": "string", "description": "The note UUID"}
            },
            "required": ["note_id"]
        }
    },
    {
        "name": DBToolName.SAVE_DAILY_CONTEXT.value,
        "description": "Save today's context including wake time and sleep data.",
        "input_schema": {
            "type": "object",
            "properties": {
                "wake_time": {"type": "string", "description": "Wake time in HH:MM format"},
                "sleep_duration": {"type": "number", "description": "Hours of sleep"},
                "sleep_quality": {"type": "string", "description": "Quality: good, fair, poor"},
                "day_type": {"type": "string", "description": "Type of day: normal, late_start, rest_day"},
                "notes": {"type": "string", "description": "Any notes about today"}
            }
        }
    },
    {
        "name": DBToolName.GET_TODAY_CONTEXT.value,
        "description": "Get today's context including wake time and sleep data.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": DBToolName.GET_RECENT_CONTEXT.value,
        "description": "Get daily context for the past N days to understand patterns.",
        "input_schema": {
            "type": "object",
            "properties": {
                "days": {"type": "integer", "description": "Number of past days to retrieve. Default 7."}
            }
        }
    },
    {
        "name": DBToolName.SAVE_PATTERN.value,
        "description": "Save a learned pattern about the user's habits or preferences.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pattern_type": {"type": "string", "description": "Type of pattern e.g. morning_routine, work_hours"},
                "description": {"type": "string", "description": "Description of the pattern"},
                "learned_from": {"type": "string", "description": "How this was learned: conversation, observation"},
                "confidence": {"type": "number", "description": "Confidence 0.0 to 1.0"}
            },
            "required": ["pattern_type", "description"]
        }
    },
    {
        "name": DBToolName.GET_PATTERNS.value,
        "description": "Get all learned user patterns ordered by confidence.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": DBToolName.GET_BRIEFING_DATA.value,
        "description": "Get all data needed for a morning briefing — tasks, events, routines, goals and context for today.",
        "input_schema": {"type": "object", "properties": {}}
    }
]
