import json
import random
from user_profile import UserProfile

def generate_daily_meal_plan(user: UserProfile, food_file="data/foods_cleaned_with_portion.json"):
    with open(food_file, "r", encoding="utf-8") as f:
        foods = json.load(f)

    calorie_target = user.daily_calories()
    total_cal = 0
    total_protein = 0
    total_fiber = 0
    meals = []

    # Sort by protein density
    sorted_foods = sorted(foods, key=lambda x: x["protein"] / (x["calories"] + 1), reverse=True)

    for food in sorted_foods:
        if any(restriction.lower() in food['name'].lower() for restriction in user.dietary_restrictions):
            continue  # skip restricted

        if total_cal + food["calories"] <= calorie_target:
            meals.append(food)
            total_cal += food["calories"]
            total_protein += food["protein"]
            total_fiber += food.get("fiber", 0) or 0

        if total_cal >= calorie_target * 0.95:
            break

    return {
        "calorie_target": round(calorie_target, 2),
        "total_calories": round(total_cal, 2),
        "total_protein": round(total_protein, 2),
        "total_fiber": round(total_fiber, 2),
        "meals": meals
    }
