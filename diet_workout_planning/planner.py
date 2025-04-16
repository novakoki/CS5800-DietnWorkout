from user_profile import UserProfile
from generate_meals import generate_daily_meal_plan
from generate_workout import select_daily_workout
import json

# Example user
user = UserProfile(
    age=25,
    gender="male",
    weight_kg=75,
    height_cm=180,
    goal="muscle_gain",
    activity_level="moderate",
    dietary_restrictions=["pork", "beef"],
    fitness_level="beginner",
    available_equipment=["Body Only", "Dumbbells"]
)

# Generate plan
day_plan = {
    "user_summary": user.summary(),
    "meals": generate_daily_meal_plan(user),
    "workout": select_daily_workout(user)
}

# Save or print
print(json.dumps(day_plan, indent=2, ensure_ascii=False))
