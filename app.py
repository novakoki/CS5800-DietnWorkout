
from diet_workout_planning.user_profile import UserProfile
from diet_workout_planning.diet.diet_profiles import get_profile
from diet_workout_planning.diet.planner import DietPlanner


def main():
    # get user profile parameters from command line
    age = int(input("Enter your age: "))
    gender = input("Enter your gender (male or female): ")
    weight_kg = float(input("Enter your weight in kg: "))
    height_cm = float(input("Enter your height in cm: "))
    goal = input("Enter your goal (weight_loss, muscle_gain, maintenance): ")
    activity_level = input("Enter your activity level (light, moderate, active): ")

    user_profile = UserProfile(
        age=age, gender=gender, weight_kg=weight_kg,
        height_cm=height_cm, goal=goal, activity_level=activity_level
    )

    diet_profile = get_profile(user_profile.daily_calories())
    print("Diet profile selected:", diet_profile)

    # Create the application
    diet_planner = DietPlanner()
    
    # Configure the application
    diet_planner.set_default_constraints(diet_profile)
    diet_planner.set_default_objectives()
    
    # Generate a basic meal plan (low creativity)
    print("\n\nGenerating basic meal plan...")
    basic_plan = diet_planner.generate_meal_plan(creativity_level=0)
    diet_planner.display_meal_plan(basic_plan, detailed=True)
    
    # Generate a creative meal plan
    # print("\n\nGenerating creative meal plan...")
    # creative_plan = app.generate_meal_plan(creativity_level=0.7)
    # app.display_meal_plan(creative_plan, detailed=True)
    
    # Example of extending the system - adding price data and budget constraint
    # print("\n\nExtending the system with budget constraints...")
    
    # # Mock adding price data to the food database
    # prices = {
    #     'Oatmeal': 0.5, 'Eggs': 0.3, 'Spinach': 0.8, 'Chicken Breast': 2.5, 'Salmon': 4.0,
    #     'Brown Rice': 0.7, 'Broccoli': 1.0, 'Sweet Potato': 0.9, 'Greek Yogurt': 1.2, 'Almonds': 3.0,
    #     'Black Beans': 0.6, 'Avocado': 1.5, 'Quinoa': 1.8, 'Tofu': 1.2, 'Lentils': 0.7
    # }
    
    # for food_id, food in app.food_db.foods.items():
    #     if food.name in prices:
    #         food.attributes['price'] = prices[food.name]
    
    # # Add a budget constraint
    # app.add_budget_constraint(max_weekly_budget=50)
    
    # # Generate a budget-constrained meal plan
    # print("Generating budget-optimized meal plan...")
    # budget_plan = app.generate_meal_plan(creativity_level=0.4)
    # app.display_meal_plan(budget_plan, detailed=True)


if __name__ == "__main__":
    main()
