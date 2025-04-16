import random
import numpy as np
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Optional, Any
import copy

from diet_workout_planning.diet.food_model import (
    FoodItem, MealAssignment, Meal, DailyPlan, WeeklyPlan, FoodDatabase,
    MealType, DietGuideGroup
)


class MealCreativityEngine:
    """Engine to enhance meal plans with creativity and randomness"""
    
    def __init__(self, food_database: FoodDatabase):
        """
        Initialize the creativity engine
        
        Parameters:
        -----------
        food_database : FoodDatabase
            The database of available foods
        """
        self.food_db = food_database
        
        # Creativity strategies - different ways to introduce creativity
        self.creativity_strategies = [
            self._apply_food_substitutions,
            self._apply_meal_themes,
            self._apply_complementary_flavors,
            self._apply_surprise_ingredients
        ]
    
    def enhance_meal_plan(self, original_plan: WeeklyPlan, 
                         creativity_level: float = 0.5,
                         flavor_exploration: float = 0.3,
                         maintain_nutrition: bool = True,
                         theme_consistency: float = 0.5) -> WeeklyPlan:
        """
        Enhance a meal plan with creativity while maintaining constraints
        
        Parameters:
        -----------
        original_plan : WeeklyPlan
            The original, nutritionally sound meal plan
        creativity_level : float (0-1)
            The overall level of creativity to apply
        flavor_exploration : float (0-1)
            How much to explore new flavor combinations
        maintain_nutrition : bool
            Whether to strictly maintain nutritional equivalence during substitutions
        theme_consistency : float (0-1)
            How consistent meal themes should be (higher means more day-to-day consistency)
            
        Returns:
        --------
        WeeklyPlan : Enhanced meal plan with added creativity
        """
        # Create a deep copy of the original plan to modify
        enhanced_plan = copy.deepcopy(original_plan)
        
        # Store original nutritional values if we need to maintain them
        if maintain_nutrition:
            original_nutrition = self._extract_nutritional_profile(original_plan)
        
        # Determine how many strategies to apply based on creativity level
        num_strategies = max(1, int(len(self.creativity_strategies) * creativity_level))
        selected_strategies = random.sample(self.creativity_strategies, num_strategies)
        
        # Apply each selected strategy
        for strategy in selected_strategies:
            strategy(enhanced_plan, creativity_level, flavor_exploration, theme_consistency)
        
        # If needed, check and adjust nutrition to maintain constraints
        if maintain_nutrition:
            self._adjust_for_nutritional_equivalence(enhanced_plan, original_nutrition)
            
        return enhanced_plan
    
    def _extract_nutritional_profile(self, plan: WeeklyPlan) -> Dict:
        """Extract key nutritional information from a meal plan"""
        profile = {
            'total_calories': plan.total_calories,
            'total_proteins': plan.total_proteins,
            'food_groups': plan.get_food_group_counts()
        }
        
        # Daily profiles
        profile['daily'] = []
        for day in plan.days:
            day_profile = {
                'calories': day.total_calories,
                'proteins': day.total_proteins,
                'food_groups': defaultdict(float)
            }
            
            # Count food groups per day
            for meal in day.meals.values():
                for food in meal.food_items:
                    day_profile['food_groups'][food.diet_guide_group] += food.quantity
            
            profile['daily'].append(day_profile)
            
        return profile
    
    def _adjust_for_nutritional_equivalence(self, plan: WeeklyPlan, target_profile: Dict):
        """Adjust a meal plan to better match a target nutritional profile"""
        # This is a simplified version that focuses on calorie adjustment
        # A more comprehensive version would balance all nutrients and food groups
        
        # Check and adjust total calories
        current_calories = plan.total_calories
        target_calories = target_profile['total_calories']
        
        # If calories are off by more than 5%, adjust
        if abs(current_calories - target_calories) / target_calories > 0.05:
            adjustment_factor = target_calories / current_calories
            
            # Apply adjustment to all food quantities
            for day in plan.days:
                for meal in day.meals.values():
                    for food in meal.food_items:
                        # Adjust quantity
                        food.quantity *= adjustment_factor
                        # Update derived values
                        food.calories = food.quantity * self.food_db.get_by_id(food.food_id).calories
                        food.proteins = food.quantity * self.food_db.get_by_id(food.food_id).proteins
        
        # Similarly, we could adjust for protein and food group targets
        # This would be more complex and might require solving another optimization problem
    
    def _apply_food_substitutions(self, plan: WeeklyPlan, 
                                 creativity_level: float,
                                 flavor_exploration: float,
                                 theme_consistency: float):
        """
        Apply random food substitutions to introduce variety
        
        This strategy replaces some foods with nutritionally similar alternatives
        """
        # Determine how many substitutions to make
        max_substitutions = sum(len(day.meals) for day in plan.days) * 2  # Up to 2 per meal
        num_substitutions = int(max_substitutions * creativity_level)
        
        # Create a pool of all food assignments
        food_assignments = []
        for day_idx, day in enumerate(plan.days):
            for meal_type, meal in day.meals.items():
                for food_idx, food in enumerate(meal.food_items):
                    food_assignments.append((day_idx, meal_type, food_idx, food))
        
        # Randomly select food assignments to substitute
        if food_assignments:
            to_substitute = random.sample(food_assignments, min(num_substitutions, len(food_assignments)))
            
            for day_idx, meal_type, food_idx, food in to_substitute:
                # Find a suitable replacement
                original_food = self.food_db.get_by_id(food.food_id)
                
                # Get alternatives in the same food group
                alternatives = [f for f in self.food_db.get_by_food_group(original_food.diet_guide_group)
                               if f.id != original_food.id and 
                                  meal_type in f.meal_suitability]
                
                if alternatives:
                    # Based on flavor_exploration, either pick a similar food or a more different one
                    if random.random() < flavor_exploration:
                        # More exploration - pick more randomly
                        replacement = random.choice(alternatives)
                    else:
                        # Less exploration - pick something with similar calories
                        alternatives.sort(key=lambda f: abs(f.calories - original_food.calories))
                        replacement = alternatives[0]
                    
                    # Calculate new quantity to maintain nutrition
                    new_quantity = food.quantity * (original_food.calories / replacement.calories) if replacement.calories > 0 else food.quantity
                    
                    # Create the replacement
                    new_food = MealAssignment(
                        food_id=replacement.id,
                        food_name=replacement.name,
                        quantity=new_quantity,
                        calories=new_quantity * replacement.calories,
                        proteins=new_quantity * replacement.proteins,
                        diet_guide_group=replacement.diet_guide_group
                    )
                    
                    # Apply the substitution
                    plan.days[day_idx].meals[meal_type].food_items[food_idx] = new_food
    
    def _apply_meal_themes(self, plan: WeeklyPlan, 
                          creativity_level: float,
                          flavor_exploration: float,
                          theme_consistency: float):
        """
        Apply meal themes to create coherent daily experiences
        
        This strategy introduces themed days (e.g., Mediterranean Monday, Taco Tuesday)
        """
        # Define some meal themes
        themes = {
            'mediterranean': {
                'food_groups_emphasis': [DietGuideGroup.OIL, DietGuideGroup.SEAFOOD],
                'compatible_foods': ['olive', 'feta', 'cucumber', 'tomato', 'fish']
            },
            'asian': {
                'food_groups_emphasis': [DietGuideGroup.SEAFOOD, DietGuideGroup.OTHER_VEGETABLES],
                'compatible_foods': ['rice', 'soy', 'ginger', 'tofu', 'noodle']
            },
            'mexican': {
                'food_groups_emphasis': [DietGuideGroup.BEANS_PEAS_LENTILS, DietGuideGroup.RED_ORANGE_VEGETABLES],
                'compatible_foods': ['bean', 'corn', 'avocado', 'tomato', 'pepper']
            },
            'comfort': {
                'food_groups_emphasis': [DietGuideGroup.WHOLE_GRAINS, DietGuideGroup.DAIRY],
                'compatible_foods': ['cheese', 'potato', 'pasta', 'soup', 'bread']
            }
        }
        
        # Determine how many days to apply themes to
        num_days_to_theme = int(len(plan.days) * creativity_level)
        days_to_theme = random.sample(range(len(plan.days)), num_days_to_theme)
        
        # If theme_consistency is high, use the same theme for multiple days
        if theme_consistency > 0.7 and num_days_to_theme > 1:
            # Pick one theme for all days
            theme_name = random.choice(list(themes.keys()))
            selected_themes = {day: theme_name for day in days_to_theme}
        else:
            # Pick different themes for each day
            selected_themes = {day: random.choice(list(themes.keys())) for day in days_to_theme}
        
        # Apply themes to selected days
        for day_idx in days_to_theme:
            theme_name = selected_themes[day_idx]
            theme = themes[theme_name]
            
            # Add the theme to the day plan for reference
            plan.days[day_idx].theme = theme_name
            
            # For each meal in the day, try to incorporate themed elements
            for meal_type, meal in plan.days[day_idx].meals.items():
                self._apply_theme_to_meal(meal, theme, flavor_exploration)
    
    def _apply_theme_to_meal(self, meal: Meal, theme: Dict, flavor_exploration: float):
        """Apply a theme to a specific meal"""
        # This is a simplified implementation - a full version would be more sophisticated
        
        # Find theme-compatible foods in our database
        compatible_foods = []
        for food in self.food_db.foods.values():
            if meal.meal_type in food.meal_suitability:
                # Check if the food name contains any of the theme's compatible food keywords
                if any(keyword in food.name.lower() for keyword in theme['compatible_foods']):
                    compatible_foods.append(food)
        
        if not compatible_foods:
            return  # No theme-compatible foods found
        
        # Only add theme foods if we're being exploratory
        if random.random() < flavor_exploration:
            # Add a theme-compatible food to the meal
            theme_food = random.choice(compatible_foods)
            
            # Check if it's already in the meal
            if theme_food.id not in [f.food_id for f in meal.food_items]:
                # Add it as a small portion
                quantity = 0.5  # Small portion
                
                new_food = MealAssignment(
                    food_id=theme_food.id,
                    food_name=theme_food.name,
                    quantity=quantity,
                    calories=quantity * theme_food.calories,
                    proteins=quantity * theme_food.proteins,
                    diet_guide_group=theme_food.diet_guide_group
                )
                
                meal.add_food(new_food)
    
    def _apply_complementary_flavors(self, plan: WeeklyPlan, 
                                    creativity_level: float,
                                    flavor_exploration: float,
                                    theme_consistency: float):
        """
        Apply flavor theory to create complementary combinations
        
        This strategy uses flavor principles (e.g., sweet+salty, acid+fat) 
        to create interesting combinations
        """
        # This is a placeholder - a real implementation would require a flavor database
        # Define some flavor principles (very simplified)
        flavor_principles = {
            'sweet_salty': {
                'sweet_foods': ['fruit', 'honey', 'sweet potato'],
                'salty_foods': ['cheese', 'ham', 'soy sauce']
            },
            'acid_fat': {
                'acid_foods': ['lemon', 'vinegar', 'tomato'],
                'fatty_foods': ['olive oil', 'avocado', 'cheese']
            },
            'umami_acid': {
                'umami_foods': ['mushroom', 'tomato', 'meat'],
                'acid_foods': ['lemon', 'vinegar', 'tomato']
            }
        }
        
        # For each day, randomly select a meal to apply flavor principles to
        for day in plan.days:
            if random.random() < creativity_level:
                # Select a random meal
                if not day.meals:
                    continue
                    
                meal_type = random.choice(list(day.meals.keys()))
                meal = day.meals[meal_type]
                
                # Select a random flavor principle
                principle_name = random.choice(list(flavor_principles.keys()))
                principle = flavor_principles[principle_name]
                
                # Try to apply the principle
                self._apply_flavor_principle(meal, principle, flavor_exploration)
    
    def _apply_flavor_principle(self, meal: Meal, principle: Dict, flavor_exploration: float):
        """Apply a flavor principle to a meal"""
        # This is a simplified implementation
        
        # For each category in the principle, try to find foods in the database
        principle_foods = {}
        for category, keywords in principle.items():
            category_foods = []
            for food in self.food_db.foods.values():
                if meal.meal_type in food.meal_suitability:
                    if any(keyword in food.name.lower() for keyword in keywords):
                        category_foods.append(food)
            
            if category_foods:
                principle_foods[category] = category_foods
        
        # If we don't have foods for all categories, skip
        if len(principle_foods) < len(principle):
            return
        
        # Only add principle foods if we're being exploratory
        if random.random() < flavor_exploration:
            # Add one food from each category
            for category, foods in principle_foods.items():
                principle_food = random.choice(foods)
                
                # Check if it's already in the meal
                if principle_food.id not in [f.food_id for f in meal.food_items]:
                    # Add it as a small portion
                    quantity = 0.5  # Small portion
                    
                    new_food = MealAssignment(
                        food_id=principle_food.id,
                        food_name=principle_food.name,
                        quantity=quantity,
                        calories=quantity * principle_food.calories,
                        proteins=quantity * principle_food.proteins,
                        diet_guide_group=principle_food.diet_guide_group
                    )
                    
                    meal.add_food(new_food)
    
    def _apply_surprise_ingredients(self, plan: WeeklyPlan, 
                                   creativity_level: float,
                                   flavor_exploration: float,
                                   theme_consistency: float):
        """
        Add occasional surprise ingredients to meals
        
        This strategy introduces unexpected but compatible ingredients to add interest
        """
        # Determine how many surprise ingredients to add
        max_surprises = len(plan.days) * 2  # Up to 2 per day
        num_surprises = int(max_surprises * creativity_level)
        
        # Create a pool of all meals
        all_meals = []
        for day_idx, day in enumerate(plan.days):
            for meal_type, meal in day.meals.items():
                all_meals.append((day_idx, meal_type, meal))
        
        # Randomly select meals to enhance
        if all_meals:
            to_enhance = random.sample(all_meals, min(num_surprises, len(all_meals)))
            
            for day_idx, meal_type, meal in to_enhance:
                # Find surprise ingredient options
                surprise_options = []
                
                # Get suitable foods for this meal type
                suitable_foods = [f for f in self.food_db.foods.values() 
                                 if meal_type in f.meal_suitability]
                
                # Filter out foods already in the meal
                current_food_ids = {food.food_id for food in meal.food_items}
                surprise_options = [f for f in suitable_foods if f.id not in current_food_ids]
                
                if surprise_options:
                    # Pick a surprise ingredient - more exploration means more exotic picks
                    if random.random() < flavor_exploration:
                        # More exotic pick - less common food groups
                        less_common_groups = [
                            DietGuideGroup.NUTS_SEEDS_SOY,
                            DietGuideGroup.DARK_GREEN_VEGETABLES,
                            DietGuideGroup.SEAFOOD
                        ]
                        group_options = [f for f in surprise_options 
                                        if f.diet_guide_group in less_common_groups]
                        
                        if group_options:
                            surprise_food = random.choice(group_options)
                        else:
                            surprise_food = random.choice(surprise_options)
                    else:
                        # More conservative pick - pick randomly
                        surprise_food = random.choice(surprise_options)
                    
                    # Add the surprise in a small quantity
                    quantity = 0.25  # Small surprise amount
                    
                    surprise_assignment = MealAssignment(
                        food_id=surprise_food.id,
                        food_name=f"Surprise {surprise_food.name}",  # Mark as surprise
                        quantity=quantity,
                        calories=quantity * surprise_food.calories,
                        proteins=quantity * surprise_food.proteins,
                        diet_guide_group=surprise_food.diet_guide_group,
                        additional_attributes={'is_surprise': True}
                    )
                    
                    meal.add_food(surprise_assignment)


def measure_creativity(plan: WeeklyPlan) -> Dict:
    """
    Measure the creativity level of a meal plan
    
    Parameters:
    -----------
    plan : WeeklyPlan
        The meal plan to evaluate
        
    Returns:
    --------
    Dict : Various creativity metrics
    """
    metrics = {}
    
    # Measure diversity - count unique foods
    all_foods = set()
    daily_unique = []
    
    for day in plan.days:
        day_foods = set()
        for meal in day.meals.values():
            for food in meal.food_items:
                all_foods.add(food.food_id)
                day_foods.add(food.food_id)
        daily_unique.append(len(day_foods))
    
    metrics['total_unique_foods'] = len(all_foods)
    metrics['avg_daily_unique'] = sum(daily_unique) / len(daily_unique) if daily_unique else 0
    
    # Measure repetition - count how often each food appears
    food_counts = defaultdict(int)
    for day in plan.days:
        for meal in day.meals.values():
            for food in meal.food_items:
                food_counts[food.food_id] += 1
    
    metrics['max_repetition'] = max(food_counts.values()) if food_counts else 0
    metrics['avg_repetition'] = sum(food_counts.values()) / len(food_counts) if food_counts else 0
    
    # Check for themes and surprises
    has_themes = any(hasattr(day, 'theme') for day in plan.days)
    
    surprise_count = 0
    for day in plan.days:
        for meal in day.meals.values():
            for food in meal.food_items:
                if food.additional_attributes and food.additional_attributes.get('is_surprise', False):
                    surprise_count += 1
    
    metrics['has_themes'] = has_themes
    metrics['surprise_count'] = surprise_count
    
    # Calculate an overall creativity score (simplified)
    creativity_score = (
        metrics['total_unique_foods'] / 30 +  # Normalize to approx 0-1
        (7 - metrics['max_repetition']) / 7 +  # Lower repetition is better
        (1 if has_themes else 0) + 
        min(1, surprise_count / 5)  # Up to 1 point for surprises
    ) / 4  # Average the components
    
    metrics['creativity_score'] = min(1, max(0, creativity_score))  # Clamp to 0-1
    
    return metrics