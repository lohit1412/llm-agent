import database

# Test create
database.create_task("Apply to Apple AI role", priority="high", due_date="2026-04-20")
database.create_routine("Gym", frequency="daily", preferred_time="09:00")
database.create_goal("Job applications", target="5 per week", deadline="2026-05-01")

# Test read
print("Tasks today:", database.get_tasks_today())
print("Routines:", database.get_routines_today())
print("Goals:", database.get_active_goals())
print("Briefing data:", database.get_briefing_data())
