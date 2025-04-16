import pulp
import random
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, Optional, Callable
from collections import defaultdict

from diet_workout_planning.diet.food_model import (
    FoodItem, Constraint, OptimizationObjective, DietaryRequirements,
    MealAssignment, Meal, DailyPlan, WeeklyPlan, FoodDatabase,
    ConstraintType, ConstraintOperation, MealType, DietGuideGroup
)


class DietOptimizer:
    """Flexible diet optimization engine with extensible constraints and objectives"""
    
    def __init__(self, food_database: FoodDatabase, dietary_requirements: DietaryRequirements):
        self.foods = food_database
        self.requirements = dietary_requirements
        self.problem = None
        self.variables = None
        self.solution = None
        
        # Register constraint handlers
        self.constraint_handlers = {
            'calories': self._handle_calorie_constraint,
            'diet_guide_group': self._handle_food_group_constraint,
            'proteins': self._handle_nutrient_constraint,
            'meal_balance': self._handle_meal_balance_constraint,
            'food_group_category': self._handle_food_group_category_constraint,
            # Extensible: add new constraint handlers here
        }
        
        # Register objective handlers
        self.objective_handlers = {
            'proteins': self._handle_protein_objective,
            'diversity': self._handle_diversity_objective,
            'creativity': self._handle_creativity_objective,
            # Extensible: add new objective handlers here
        }
    
    def create_optimization_problem(self):
        """Define the optimization problem with variables, constraints, and objectives"""
        # Create the optimization problem (default to minimization)
        self.problem = pulp.LpProblem("Diet_Optimization", pulp.LpMinimize)
        
        # Define decision variables
        days = range(1, 8)  # 7 days
        meal_types = list(MealType)
        food_ids = list(self.foods.foods.keys())
        
        # Create variables for food quantities (continuous variables representing servings)
        self.variables = {}
        self.variables['food_qty'] = pulp.LpVariable.dicts(
            "Food_Qty", 
            [(i, j.value, k) for i in food_ids 
                             for j in meal_types 
                             for k in days],
            lowBound=0,
            cat='Integer'  # Integer servings
        )
        
        # Create binary variables for food selection (1 if food is used, 0 otherwise)
        self.variables['food_used'] = pulp.LpVariable.dicts(
            "Food_Used",
            [(i, j.value, k) for i in food_ids 
                            for j in meal_types 
                            for k in days],
            cat='Binary'
        )
        
        # Link quantity and selection variables
        # If food_qty > 0, then food_used must be 1
        M = 10  # A sufficiently large number (maximum servings per food)
        for i in food_ids:
            for j in meal_types:
                for k in days:
                    # food_qty <= M * food_used
                    # This ensures food_used = 1 if food_qty > 0
                    self.problem += (self.variables['food_qty'][(i, j.value, k)] <= M * self.variables['food_used'][(i, j.value, k)])
        
        # Meal suitability constraints - only assign foods suitable for specific meal types
        for i in food_ids:
            food = self.foods.get_by_id(i)
            for j in meal_types:
                if not food.meal_suitability.get(j, False):
                    for k in days:
                        self.problem += self.variables['food_qty'][(i, j.value, k)] == 0
        
        # Apply all registered constraints
        self._apply_all_constraints()
        
        # Set up the objective function
        self._apply_all_objectives()
        
        return self.problem
    
    def _apply_all_constraints(self):
        """Apply all registered constraints to the problem"""
        for constraint in self.requirements.constraints:
            if constraint.attribute in self.constraint_handlers:
                handler = self.constraint_handlers[constraint.attribute]
                try:
                    handler(constraint)
                except Exception as e:
                    print(f"Error applying constraint '{constraint.name}': {e}")
                    exit(1)
            else:
                print(f"Warning: No handler for constraint attribute '{constraint.attribute}'")
    
    def _apply_all_objectives(self):
        """Apply all registered objectives to create a weighted objective function"""
        objective_terms = []
        
        for objective in self.requirements.objectives:
            if objective.attribute in self.objective_handlers:
                handler = self.objective_handlers[objective.attribute]
                term = handler(objective)
                objective_terms.append(term)
            else:
                print(f"Warning: No handler for objective attribute '{objective.attribute}'")
        
        # If no objectives defined, use a default (minimize calories)
        if not objective_terms:
            default_term = self._create_calorie_objective()
            objective_terms.append(default_term)
        
        # Set the final objective function
        self.problem += pulp.lpSum(objective_terms)
    
    def _handle_calorie_constraint(self, constraint: Constraint):
        """Handle calorie constraints"""
        days = range(1, 8)
        food_ids = list(self.foods.foods.keys())
        meal_types = list(MealType)
        
        if constraint.type == ConstraintType.DAILY:
            # Apply constraint for each day
            for day in days:
                daily_calories = pulp.lpSum([
                    self.variables['food_qty'][(i, j.value, day)] * self.foods.get_by_id(i).calories
                    for i in food_ids for j in meal_types
                ])
                
                if constraint.operation == ConstraintOperation.EQUAL:
                    self.problem += daily_calories == constraint.value
                elif constraint.operation == ConstraintOperation.GREATER_EQUAL:
                    self.problem += daily_calories >= constraint.value
                elif constraint.operation == ConstraintOperation.LESS_EQUAL:
                    self.problem += daily_calories <= constraint.value
                elif constraint.operation == ConstraintOperation.RANGE:
                    min_val, max_val = constraint.value
                    self.problem += (daily_calories >= min_val)
                    self.problem += (daily_calories <= max_val)

            # print(daily_calories)
        
        elif constraint.type == ConstraintType.WEEKLY:
            # Apply constraint for the full week
            weekly_calories = pulp.lpSum([
                self.variables['food_qty'][(i, j.value, k)] * self.foods.get_by_id(i).calories
                for i in food_ids for j in meal_types for k in days
            ])
            
            if constraint.operation == ConstraintOperation.EQUAL:
                self.problem += weekly_calories == constraint.value
            elif constraint.operation == ConstraintOperation.GREATER_EQUAL:
                self.problem += weekly_calories >= constraint.value
            elif constraint.operation == ConstraintOperation.LESS_EQUAL:
                self.problem += weekly_calories <= constraint.value
            elif constraint.operation == ConstraintOperation.RANGE:
                min_val, max_val = constraint.value
                self.problem += weekly_calories >= min_val
                self.problem += weekly_calories <= max_val
    
    def _handle_food_group_constraint(self, constraint: Constraint):
        """Handle food group constraints"""
        days = range(1, 8)
        food_ids = list(self.foods.foods.keys())
        meal_types = list(MealType)
        
        # Get foods in the specific group
        group_foods = {
            food.id for food in self.foods.foods.values() 
            if str(food.diet_guide_group) == constraint.name.value
        }

        # print(group_foods)
        
        if not group_foods:
            print(f"Warning: No foods found in group '{constraint.name}'")
            return
        
        if constraint.type == ConstraintType.DAILY:
            # Apply constraint for each day
            for day in days:
                group_servings = pulp.lpSum([
                    self.variables['food_qty'][(i, j.value, day)]
                    for i in group_foods for j in meal_types
                ])
                
                if constraint.operation == ConstraintOperation.EQUAL:
                    self.problem += group_servings == constraint.value
                elif constraint.operation == ConstraintOperation.GREATER_EQUAL:
                    self.problem += group_servings >= constraint.value
                elif constraint.operation == ConstraintOperation.LESS_EQUAL:
                    self.problem += group_servings <= constraint.value
        
        elif constraint.type == ConstraintType.WEEKLY:
            # Apply constraint for the full week
            weekly_servings = pulp.lpSum([
                self.variables['food_qty'][(i, j.value, k)]
                for i in group_foods for j in meal_types for k in days
            ])

            # print(weekly_servings)
            
            if constraint.operation == ConstraintOperation.EQUAL:
                self.problem += weekly_servings == constraint.value
            elif constraint.operation == ConstraintOperation.GREATER_EQUAL:
                self.problem += weekly_servings >= constraint.value
            elif constraint.operation == ConstraintOperation.LESS_EQUAL:
                self.problem += weekly_servings <= constraint.value

    def _handle_food_group_category_constraint(self, constraint):
        """
        Handle constraints for aggregated food group categories
        
        This allows combining multiple food groups into categories like 'protein' or 'vegetable'
        """
        
        days = range(1, 8)
        food_ids = list(self.foods.foods.keys())
        meal_types = list(MealType)
        
        category = constraint.value["category"]
        min_amount = constraint.value["amount"]
        
        # Define which food groups belong to each category
        category_groups = {
            "protein": [
                DietGuideGroup.MEATS_POULTRY_EGGS,
                DietGuideGroup.SEAFOOD,
                DietGuideGroup.BEANS_PEAS_LENTILS,
                DietGuideGroup.NUTS_SEEDS_SOY
            ],
            "vegetable": [
                DietGuideGroup.DARK_GREEN_VEGETABLES,
                DietGuideGroup.RED_ORANGE_VEGETABLES,
                DietGuideGroup.STARCHY_VEGETABLES,
                DietGuideGroup.OTHER_VEGETABLES
            ]
        }
        
        # Get the relevant food groups for this category
        if category not in category_groups:
            print(f"Warning: Unknown food group category '{category}'")
            return
            
        relevant_groups = {_.value for _ in category_groups[category]}
        
        # For daily constraints, apply to each day
        if constraint.type == ConstraintType.DAILY:
            for day in days:
                # Calculate total servings of the category for this day
                category_servings = pulp.lpSum([
                    self.variables['food_qty'][(i, j.value, day)]
                    for i in food_ids
                    for j in meal_types
                    if self.foods.get_by_id(i).diet_guide_group in relevant_groups
                ])
                
                # Apply the constraint
                if constraint.operation == ConstraintOperation.GREATER_EQUAL:
                    self.problem += category_servings >= min_amount
                elif constraint.operation == ConstraintOperation.LESS_EQUAL:
                    self.problem += category_servings <= min_amount
                elif constraint.operation == ConstraintOperation.EQUAL:
                    self.problem += category_servings == min_amount
    
    def _handle_nutrient_constraint(self, constraint: Constraint):
        """Handle general nutrient constraints (proteins, etc.)"""
        days = range(1, 8)
        food_ids = list(self.foods.foods.keys())
        meal_types = list(MealType)
        
        attribute = constraint.attribute  # e.g., 'proteins'
        
        if constraint.type == ConstraintType.DAILY:
            # Apply constraint for each day
            for day in days:
                daily_amount = pulp.lpSum([
                    self.variables['food_qty'][(i, j.value, day)] * getattr(self.foods.get_by_id(i), attribute, 0)
                    for i in food_ids for j in meal_types
                ])
                
                if constraint.operation == ConstraintOperation.EQUAL:
                    self.problem += daily_amount == constraint.value
                elif constraint.operation == ConstraintOperation.GREATER_EQUAL:
                    self.problem += daily_amount >= constraint.value
                elif constraint.operation == ConstraintOperation.LESS_EQUAL:
                    self.problem += daily_amount <= constraint.value
        
        elif constraint.type == ConstraintType.WEEKLY:
            # Apply constraint for the full week
            weekly_amount = pulp.lpSum([
                self.variables['food_qty'][(i, j.value, k)] * getattr(self.foods.get_by_id(i), attribute, 0)
                for i in food_ids for j in meal_types for k in days
            ])
            
            if constraint.operation == ConstraintOperation.EQUAL:
                self.problem += weekly_amount == constraint.value
            elif constraint.operation == ConstraintOperation.GREATER_EQUAL:
                self.problem += weekly_amount >= constraint.value
            elif constraint.operation == ConstraintOperation.LESS_EQUAL:
                self.problem += weekly_amount <= constraint.value

    

    def _handle_meal_balance_constraint(self, constraint):
        """
        Handle constraints for balancing calories across meals in a day
        
        This ensures that no meal is too large or too small relative to the day's total
        """
        
        days = range(1, 8)
        food_ids = list(self.foods.foods.keys())
        meal_types = list(MealType)
        
        min_percent, max_percent = constraint.value
        
        # For each day
        for day in days:
            # Calculate total daily calories
            daily_calories = pulp.lpSum([
                self.variables['food_qty'][(i, j.value, day)] * self.foods.get_by_id(i).calories
                for i in food_ids for j in meal_types
            ])
            
            # For each meal type, ensure it's within the allowed percentage range
            for meal_type in meal_types:
                meal_calories = pulp.lpSum([
                    self.variables['food_qty'][(i, meal_type.value, day)] * self.foods.get_by_id(i).calories
                    for i in food_ids
                ])
                
                # Ensure meal is at least min_percent of daily calories
                self.problem += meal_calories >= min_percent * daily_calories
                
                # Ensure meal is at most max_percent of daily calories
                self.problem += meal_calories <= max_percent * daily_calories
    
    def _handle_protein_objective(self, objective: OptimizationObjective):
        """Handle protein maximization objective"""
        days = range(1, 8)
        food_ids = list(self.foods.foods.keys())
        meal_types = list(MealType)
        
        # Calculate total protein
        total_protein = pulp.lpSum([
            self.variables['food_qty'][(i, j.value, k)] * self.foods.get_by_id(i).proteins
            for i in food_ids for j in meal_types for k in days
        ])
        
        # If maximizing, negate the term (since we're minimizing by default)
        if objective.maximize:
            return -1 * objective.weight * total_protein
        else:
            return objective.weight * total_protein
    
    def _handle_diversity_objective(self, objective: OptimizationObjective):
        """Handle diversity maximization objective"""
        days = range(1, 8)
        food_ids = list(self.foods.foods.keys())
        meal_types = list(MealType)
        
        # For diversity, we'll count unique foods used each day
        # Since we already have binary variables for whether a food is used,
        # we can maximize the sum of these variables
        
        diversity_term = pulp.lpSum([
            self.variables['food_used'][(i, j.value, k)]
            for i in food_ids for j in meal_types for k in days
        ])
        
        # If maximizing diversity, negate the term
        if objective.maximize:
            return -1 * objective.weight * diversity_term
        else:
            return objective.weight * diversity_term
    
    def _handle_creativity_objective(self, objective: OptimizationObjective):
        """
        Handle creativity/randomness objective
        
        This is more complex since true creativity is hard to model in LP
        We'll use a proxy approach: encourage variety across days
        """
        days = range(1, 8)
        food_ids = list(self.foods.foods.keys())
        meal_types = list(MealType)
        
        # We need additional variables to track day-to-day differences
        # This is a complex objective that might be better handled post-optimization
        
        # For now, we'll use a simpler proxy: discourage using the same food on consecutive days
        # This requires binary variables to track food usage by day (not by meal)
        
        # Create a summary variable for food usage by day
        food_used_by_day = pulp.LpVariable.dicts(
            "Food_Used_Day",
            [(i, k) for i in food_ids for k in days],
            cat='Binary'
        )
        
        # Link meal variables to day variables
        for i in food_ids:
            for k in days:
                # food_used_by_day[i,k] = 1 if food i is used on day k in any meal
                self.problem += food_used_by_day[(i, k)] <= pulp.lpSum([
                    self.variables['food_used'][(i, j.value, k)] for j in meal_types
                ])
                
                for j in meal_types:
                    self.problem += food_used_by_day[(i, k)] >= self.variables['food_used'][(i, j.value, k)]
        
        # Count consecutive day usage
        consecutive_usage = pulp.LpVariable.dicts(
            "Consecutive_Usage",
            [(i, k) for i in food_ids for k in range(1, 7)],  # Only need 6 days for consecutive pairs
            cat='Binary'
        )
        
        # Set consecutive_usage[i,k] = 1 if food i is used on both day k and k+1
        for i in food_ids:
            for k in range(1, 7):
                self.problem += consecutive_usage[(i, k)] >= food_used_by_day[(i, k)] + food_used_by_day[(i, k+1)] - 1
                self.problem += consecutive_usage[(i, k)] <= food_used_by_day[(i, k)]
                self.problem += consecutive_usage[(i, k)] <= food_used_by_day[(i, k+1)]
        
        # Minimize consecutive usage (to promote variety)
        consecutive_term = pulp.lpSum([consecutive_usage[(i, k)] for i in food_ids for k in range(1, 7)])
        
        # We want to minimize consecutive usage
        return objective.weight * consecutive_term
    
    def _create_calorie_objective(self):
        """Create a default objective to minimize total calories"""
        days = range(1, 8)
        food_ids = list(self.foods.foods.keys())
        meal_types = list(MealType)
        
        # Calculate total calories
        total_calories = pulp.lpSum([
            self.variables['food_qty'][(i, j.value, k)] * self.foods.get_by_id(i).calories
            for i in food_ids for j in meal_types for k in days
        ])
        
        return total_calories
    
    def solve(self):
        """Solve the optimization problem and return the solution"""
        # Make sure the problem is defined
        if self.problem is None:
            self.create_optimization_problem()
        
        # Solve the problem
        solver = pulp.PULP_CBC_CMD(msg=False, timeLimit=120)
        self.problem.solve(solver)
        
        # Check if a solution was found
        if pulp.LpStatus[self.problem.status] != 'Optimal':
            print(f"No optimal solution found. Status: {pulp.LpStatus[self.problem.status]}")
            return None
        
        # print all valid variables
        # for v in self.problem.variables():
        #     if v.varValue > 0:
        #         print(f"{v.name}: {v.varValue}")
        
        # Extract the solution
        solution = {}
        for k in range(1, 8):  # days
            solution[k] = {}
            for j in MealType:  # meals
                solution[k][j] = []
                for i in self.foods.foods.keys():  # foods
                    qty = self.variables['food_qty'][(i, j.value, k)].value()
                    if qty is not None and qty > 0.001:  # Some small epsilon to handle floating-point issues
                        food = self.foods.get_by_id(i)
                        solution[k][j].append({
                            'food_id': i,
                            'food_name': food.name,
                            'quantity': qty,
                            'calories': food.calories,
                            'proteins': food.proteins,
                            'diet_guide_group': food.diet_guide_group
                        })
        
        self.solution = solution
        return solution
    
    def enhance_creativity(self, base_solution, creativity_level=0.3):
        """
        Post-process the solution to enhance creativity and randomness
        
        This is done after the LP solution to ensure we maintain feasibility
        of the critical constraints while adding some randomness.
        
        Parameters:
        -----------
        base_solution : dict
            The base solution from the LP optimizer
        creativity_level : float (0-1)
            How much randomness to introduce
            
        Returns:
        --------
        dict : Enhanced solution with added creativity
        """
        # Clone the solution to avoid modifying the original
        enhanced_solution = self._deep_copy_solution(base_solution)
        
        # Randomly select days to modify
        days = list(enhanced_solution.keys())
        days_to_modify = random.sample(days, int(len(days) * creativity_level) + 1)
        
        for day in days_to_modify:
            # Randomly select a meal to modify
            meal_types = list(enhanced_solution[day].keys())
            if not meal_types:
                continue
                
            meal_type = random.choice(meal_types)
            
            # Get suitable alternative foods for this meal type
            suitable_foods = self.foods.get_by_meal_type(meal_type)
            
            # Get current foods in this meal
            current_meal = enhanced_solution[day][meal_type]
            current_food_ids = {item['food_id'] for item in current_meal}
            
            # Find alternative foods
            alternative_foods = [food for food in suitable_foods if food.id not in current_food_ids]
            
            if not alternative_foods or not current_meal:
                continue
            
            # Select a food to replace
            food_to_replace = random.choice(current_meal)
            
            # Select a replacement food with similar calories
            target_calories = food_to_replace['calories']
            
            # Sort alternatives by calorie similarity
            alternatives_by_calories = sorted(
                alternative_foods,
                key=lambda f: abs(f.calories - target_calories/food_to_replace['quantity'])
            )
            
            # Choose from the top 3 closest matches (or fewer if not enough options)
            top_n = min(3, len(alternatives_by_calories))
            if top_n == 0:
                continue
                
            replacement = random.choice(alternatives_by_calories[:top_n])
            
            # Calculate quantity to maintain similar calories
            replacement_qty = target_calories / replacement.calories
            
            # Replace the food
            new_food = {
                'food_id': replacement.id,
                'food_name': replacement.name,
                'quantity': replacement_qty,
                'calories': replacement.calories * replacement_qty,
                'proteins': replacement.proteins * replacement_qty,
                'diet_guide_group': replacement.diet_guide_group
            }
            
            # Find the index of the food to replace
            for i, item in enumerate(current_meal):
                if item['food_id'] == food_to_replace['food_id']:
                    enhanced_solution[day][meal_type][i] = new_food
                    break
        
        return enhanced_solution
    
    def _deep_copy_solution(self, solution):
        """Make a deep copy of the solution dictionary"""
        import copy
        return copy.deepcopy(solution)
    
    def generate_meal_plan(self):
        """Generate a structured meal plan from the optimization solution"""
        if self.solution is None:
            solution = self.solve()
            if solution is None:
                return None
        
        # Post-process to enhance creativity
        enhanced_solution = self.enhance_creativity(self.solution)
        
        # Create a structured weekly plan
        weekly_plan = WeeklyPlan()
        
        for day_num in range(1, 8):
            day_plan = DailyPlan(day_of_week=day_num)
            
            for meal_type in MealType:
                if meal_type in enhanced_solution[day_num]:
                    meal = Meal(meal_type=meal_type)
                    
                    for food_item in enhanced_solution[day_num][meal_type]:
                        meal_assignment = MealAssignment(
                            food_id=food_item['food_id'],
                            food_name=food_item['food_name'],
                            quantity=food_item['quantity'],
                            calories=food_item['calories'],
                            proteins=food_item['proteins'],
                            diet_guide_group=food_item['diet_guide_group']
                        )
                        meal.add_food(meal_assignment)
                    
                    day_plan.meals[meal_type] = meal
            
            weekly_plan.days.append(day_plan)
        
        return weekly_plan