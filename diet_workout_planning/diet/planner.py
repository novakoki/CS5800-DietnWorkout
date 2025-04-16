import pandas as pd
import numpy as np
import random
from typing import Dict, List

from diet_workout_planning.diet.food_model import (
    FoodItem, Constraint, OptimizationObjective, DietaryRequirements, 
    FoodDatabase, ConstraintType, ConstraintOperation, MealType, DietGuideGroup, WeeklyPlan
)
from diet_workout_planning.diet.optimizer import DietOptimizer
from diet_workout_planning.diet.creativity_engine import MealCreativityEngine, measure_creativity
from diet_workout_planning.diet.data_loader import get_food_data

class DietPlanner:
    """Main application for diet planning"""
    
    def __init__(self):
        self.food_db = FoodDatabase()
        self.dietary_requirements = DietaryRequirements()
        self.food_db.load_from_dataframe(get_food_data())
        self.optimizer = DietOptimizer(self.food_db, self.dietary_requirements)
        self.creativity_engine = MealCreativityEngine(self.food_db)
        
    def load_food_database(self, food_data_path):
        """Load food database from CSV file"""
        df = pd.read_csv(food_data_path)
        
        # Process diet_guide_group into proper enum values
        df['diet_guide_group'] = df['diet_guide_group'].astype(str)
        
        # Initialize optimizer and creativity engine after loading the data
        self.food_db.load_from_dataframe(df)
        self.optimizer = DietOptimizer(self.food_db, self.dietary_requirements)
        self.creativity_engine = MealCreativityEngine(self.food_db)
        
        print(f"Loaded {len(self.food_db.foods)} food items from {food_data_path}")
    
    def set_default_constraints(self, user_profile):
        """Set up default constraints based on user profile"""
        # Clear any existing constraints
        self.dietary_requirements.constraints = []
        # print(user_profile)
        
        # 1. Daily calorie constraint
        daily_calories = user_profile.get('daily_calories', 2000)
        calorie_range = [daily_calories * 0.9, daily_calories * 1.1]  # ±10%
        
        self.dietary_requirements.add_constraint(
            Constraint(
                name="Daily Calories",
                type=ConstraintType.DAILY,
                attribute="calories",
                operation=ConstraintOperation.RANGE,
                value=calorie_range
            )
        )
        
        # # 2. Daily food group requirements
        daily_groups = {
            DietGuideGroup.WHOLE_GRAINS: user_profile.get('daily_whole_grains', 1),
            DietGuideGroup.REFINED_GRAINS: user_profile.get('daily_refined_grains', 1),
            DietGuideGroup.FRUITS: user_profile.get('daily_fruits', 1),
            DietGuideGroup.DAIRY: user_profile.get('daily_dairy', 1)
        }
        
        for group, amount in daily_groups.items():
            self.dietary_requirements.add_constraint(
                Constraint(
                    name=group,
                    type=ConstraintType.DAILY,
                    attribute="diet_guide_group",
                    operation=ConstraintOperation.GREATER_EQUAL,
                    value=amount,
                    weight=1.0
                )
            )
        
        # 3. Weekly food group requirements
        weekly_groups = {
            DietGuideGroup.DARK_GREEN_VEGETABLES: user_profile.get('weekly_dark_green_vegetables', 1),
            DietGuideGroup.RED_ORANGE_VEGETABLES: user_profile.get('weekly_red_orange_vegetables', 1),
            DietGuideGroup.STARCHY_VEGETABLES: user_profile.get('weekly_starchy_vegetables', 1),
            DietGuideGroup.OTHER_VEGETABLES: user_profile.get('weekly_other_vegetables', 1),
            DietGuideGroup.BEANS_PEAS_LENTILS: user_profile.get('weekly_beans', 1),
            DietGuideGroup.MEATS_POULTRY_EGGS: user_profile.get('weekly_meat', 1),
            DietGuideGroup.SEAFOOD: user_profile.get('weekly_seafood', 1),
            DietGuideGroup.NUTS_SEEDS_SOY: user_profile.get('weekly_nuts_seeds_soy', 1),
        }
        
        for group, amount in weekly_groups.items():
            self.dietary_requirements.add_constraint(
                Constraint(
                    name=group,
                    type=ConstraintType.WEEKLY,
                    attribute="diet_guide_group",
                    operation=ConstraintOperation.GREATER_EQUAL,
                    value=amount,
                    weight=1.0
                )
            )

        # 4. Meal balance constraint
        self.dietary_requirements.add_constraint(Constraint(
            name="Meal Calorie Balance",
            type=ConstraintType.DAILY,
            attribute="meal_balance", 
            operation=ConstraintOperation.RANGE,
            value=[0.2, 0.45],
            weight=1.0
        ))

        
        self.dietary_requirements.add_constraint(Constraint(
            name="Daily Vegetables",
            type=ConstraintType.DAILY,
            attribute="food_group_category",
            operation=ConstraintOperation.GREATER_EQUAL,
            value={"category": "vegetable", "amount": user_profile.get('daily_vegetables', 1)},
            weight=1.0
        ))

    
        self.dietary_requirements.add_constraint(Constraint(
            name="Daily Protein Foods",
            type=ConstraintType.DAILY,
            attribute="food_group_category",
            operation=ConstraintOperation.GREATER_EQUAL,
            value={"category": "protein", "amount": user_profile.get('daily_protein_foods', 1)},
            weight=1.0
        ))

        # print(self.dietary_requirements)
    
    def set_default_objectives(self):
        """Set up default optimization objectives"""
        # Clear any existing objectives
        self.dietary_requirements.objectives = []
        
        # 1. Maximize protein
        # self.dietary_requirements.add_objective(
        #     OptimizationObjective(
        #         name="Maximize Protein",
        #         attribute="proteins",
        #         maximize=True,
        #         weight=1.0
        #     )
        # )
        
        # 2. Maximize diversity
        self.dietary_requirements.add_objective(
            OptimizationObjective(
                name="Maximize Diversity",
                attribute="diversity",
                maximize=True,
                weight=1.0
            )
        )
        
        # 3. Enhance creativity
        self.dietary_requirements.add_objective(
            OptimizationObjective(
                name="Enhance Creativity",
                attribute="creativity",
                maximize=True,
                weight=0.5  # Lower weight since this is handled post-optimization
            )
        )
    
    def add_constraint(self, constraint: Constraint):
        """Add a new constraint to the requirements"""
        self.dietary_requirements.add_constraint(constraint)
        
    def add_objective(self, objective: OptimizationObjective):
        """Add a new optimization objective"""
        self.dietary_requirements.add_objective(objective)
    
    def generate_meal_plan(self, creativity_level=0.5):
        """Generate a complete meal plan"""
        if not self.optimizer:
            raise ValueError("Optimizer not initialized. Load food database first.")
            
        # Create and solve the optimization problem
        print("Generating base meal plan through optimization...")
        self.optimizer.create_optimization_problem()
        solution = self.optimizer.solve()
        
        if not solution:
            print("Failed to find a feasible meal plan.")
            return None
        
        # Convert solution to structured meal plan
        base_plan = self.optimizer.generate_meal_plan()
        
        # Calculate base metrics
        base_metrics = measure_creativity(base_plan)
        print(f"Base plan metrics: {base_metrics}")
        
        # Apply creativity enhancements
        if self.creativity_engine and creativity_level > 0:
            print(f"Enhancing meal plan with creativity (level: {creativity_level})...")
            enhanced_plan = self.creativity_engine.enhance_meal_plan(
                base_plan,
                creativity_level=creativity_level,
                flavor_exploration=creativity_level * 0.8,
                maintain_nutrition=True,
                theme_consistency=0.5
            )
            
            # Calculate enhanced metrics
            enhanced_metrics = measure_creativity(enhanced_plan)
            print(f"Enhanced plan metrics: {enhanced_metrics}")
            
            return enhanced_plan
        else:
            return base_plan
    
    def display_meal_plan(self, plan: WeeklyPlan, detailed=False):
        """Display a meal plan in a readable format"""
        if not plan:
            print("No meal plan to display.")
            return
        
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        print("\n" + "="*80)
        print("WEEKLY MEAL PLAN")
        print("="*80)
        
        # Weekly summary
        print(f"Total Calories: {plan.total_calories:.1f}")
        print(f"Total Proteins: {plan.total_proteins:.1f}g")
        
        food_groups = plan.get_food_group_counts()
        print("\nFood Group Totals:")
        for group, count in food_groups.items():
            print(f"  - {group.value}: {count:.1f} servings")
        
        # Day by day plan
        for day in plan.days:
            day_name = days_of_week[day.day_of_week - 1]
            print("\n" + "-"*80)
            print(f"{day_name} (Day {day.day_of_week})")
            
            if hasattr(day, 'theme'):
                print(f"Theme: {day.theme.capitalize()}")
                
            print(f"Daily Calories: {day.total_calories:.1f}")
            print(f"Daily Proteins: {day.total_proteins:.1f}g")
            
            # Each meal
            for meal_type, meal in day.meals.items():
                print(f"\n{meal_type.value.capitalize()} - {meal.total_calories:.1f} calories")
                
                # Foods in meal
                for food in meal.food_items:
                    food_info = f"• {food.food_name} ({food.quantity:.1f} servings)"
                    
                    if detailed:
                        food_info += f" - {food.calories:.1f} cal, {food.proteins:.1f}g protein"
                        
                    # Check if it's a surprise ingredient
                    is_surprise = food.additional_attributes.get('is_surprise', False)
                    if is_surprise:
                        food_info += " [SURPRISE!]"
                        
                    print(food_info)
    
    def add_budget_constraint(self, max_weekly_budget):
        """Example of adding a new constraint - budget limit"""
        # We assume the food database has been updated with price information
        if 'price' not in next(iter(self.food_db.foods.values())).attributes:
            print("Food database doesn't have price information yet.")
            return False
        
        # Add a weekly budget constraint
        self.dietary_requirements.add_constraint(
            Constraint(
                name="Weekly Budget",
                type=ConstraintType.WEEKLY,
                attribute="price",  # This would be a food attribute
                operation=ConstraintOperation.LESS_EQUAL,
                value=max_weekly_budget,
                weight=1.0
            )
        )
        
        return True
