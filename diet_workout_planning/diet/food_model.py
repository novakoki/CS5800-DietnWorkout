from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Union, Any
from enum import Enum
import pandas as pd


class DietGuideGroup(Enum):
    """Enum representing different food groups according to dietary guidelines"""
    DARK_GREEN_VEGETABLES = "Dark-Green Vegetables"
    RED_ORANGE_VEGETABLES = "Red and Orange Vegetables"
    STARCHY_VEGETABLES = "Starchy Vegetables"
    OTHER_VEGETABLES = "Other Vegetables"
    BEANS_PEAS_LENTILS = "Beans, Peas, Lentils"
    NUTS_SEEDS_SOY = "Nuts, Seeds, Soy Products"
    WHOLE_GRAINS = "Whole Grains"
    REFINED_GRAINS = "Refined Grains"
    MEATS_POULTRY_EGGS = "Meats, Poultry, Eggs"
    SEAFOOD = "Seafood"
    FRUITS = "Fruits"
    DAIRY = "Dairy"
    OIL = "Oil"


class MealType(Enum):
    """Enum representing different meal types"""
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"


class ConstraintType(Enum):
    """Different types of constraints that can be applied"""
    DAILY = "daily"
    WEEKLY = "weekly"
    TOTAL = "total"


class ConstraintOperation(Enum):
    """Operations that can be used for constraints"""
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    EQUAL = "=="
    RANGE = "range"


@dataclass
class FoodItem:
    """Class representing a food item in the database"""
    id: int
    name: str
    diet_guide_group: DietGuideGroup
    calories: float
    proteins: float
    meal_suitability: Dict[MealType, bool]
    # Extended attributes that can be added in the future
    attributes: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dataframe_row(cls, row, id_counter=None):
        """Create a FoodItem from a DataFrame row"""
        if id_counter is None:
            id_val = getattr(row, 'id', 0)
        else:
            id_val = next(id_counter)
            
        return cls(
            id=id_val,
            name=row["name"],
            diet_guide_group=row.diet_guide_group,
            calories=row.calories,
            proteins=row.proteins,
            meal_suitability={
                MealType.BREAKFAST: row.breakfast,
                MealType.LUNCH: row.lunch,
                MealType.DINNER: row.dinner
            },
            attributes={}  # Empty by default, can be populated with additional columns
        )


@dataclass
class Constraint:
    """A flexible constraint definition"""
    name: str
    type: ConstraintType
    attribute: str  # What attribute the constraint applies to (e.g., 'calories', 'diet_guide_group')
    operation: ConstraintOperation
    value: Union[float, List[float], str]  # Target value or range [min, max]
    weight: float = 1.0  # Weight for soft constraints in optimization
    
    def __str__(self):
        if self.operation == ConstraintOperation.RANGE:
            value_str = f"[{self.value[0]}, {self.value[1]}]"
        else:
            value_str = str(self.value)
        return f"{self.name}: {self.attribute} {self.operation.value} {value_str} ({self.type.value})"


@dataclass
class OptimizationObjective:
    """Definition of an optimization objective"""
    name: str
    attribute: str  # What attribute to optimize
    maximize: bool  # True if maximizing, False if minimizing
    weight: float  # Weight in the multi-objective function
    
    def __str__(self):
        direction = "Maximize" if self.maximize else "Minimize"
        return f"{self.name}: {direction} {self.attribute} (weight: {self.weight})"


@dataclass
class DietaryRequirements:
    """Collection of all dietary requirements"""
    constraints: List[Constraint] = field(default_factory=list)
    objectives: List[OptimizationObjective] = field(default_factory=list)
    
    def add_constraint(self, constraint: Constraint):
        """Add a new constraint"""
        self.constraints.append(constraint)
        
    def add_objective(self, objective: OptimizationObjective):
        """Add a new optimization objective"""
        self.objectives.append(objective)
        
    def get_daily_constraints(self):
        """Return all daily constraints"""
        return [c for c in self.constraints if c.type == ConstraintType.DAILY]
    
    def get_weekly_constraints(self):
        """Return all weekly constraints"""
        return [c for c in self.constraints if c.type == ConstraintType.WEEKLY]


@dataclass
class MealAssignment:
    """Assignment of a food item to a specific meal"""
    food_id: int
    food_name: str
    quantity: float  # Number of servings
    calories: float
    proteins: float
    diet_guide_group: DietGuideGroup
    additional_attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Meal:
    """A collection of food items for a specific meal"""
    meal_type: MealType
    food_items: List[MealAssignment] = field(default_factory=list)
    
    @property
    def total_calories(self):
        return sum(item.calories * item.quantity for item in self.food_items)
    
    @property
    def total_proteins(self):
        return sum(item.proteins * item.quantity for item in self.food_items)
    
    def add_food(self, food_assignment: MealAssignment):
        self.food_items.append(food_assignment)


@dataclass
class DailyPlan:
    """Food plan for a full day"""
    day_of_week: int  # 1-7 for Monday-Sunday
    meals: Dict[MealType, Meal] = field(default_factory=dict)
    
    @property
    def total_calories(self):
        return sum(meal.total_calories for meal in self.meals.values())
    
    @property
    def total_proteins(self):
        return sum(meal.total_proteins for meal in self.meals.values())


@dataclass
class WeeklyPlan:
    """Complete weekly meal plan"""
    days: List[DailyPlan] = field(default_factory=list)
    
    @property
    def total_calories(self):
        return sum(day.total_calories for day in self.days)
    
    @property
    def total_proteins(self):
        return sum(day.total_proteins for day in self.days)
    
    def get_food_group_counts(self):
        """Count occurrences of each food group in the plan"""
        counts = {group: 0 for group in DietGuideGroup}
        
        for day in self.days:
            for meal in day.meals.values():
                for food in meal.food_items:
                    counts[DietGuideGroup(food.diet_guide_group)] += food.quantity
        
        return counts
    
    def get_food_diversity_score(self):
        """Calculate food diversity score"""
        # Count unique foods per day
        daily_unique_foods = []
        
        for day in self.days:
            day_foods = set()
            for meal in day.meals.values():
                for food in meal.food_items:
                    day_foods.add(food.food_id)
            daily_unique_foods.append(len(day_foods))
        
        # Average unique foods per day
        if not daily_unique_foods:
            return 0
        return sum(daily_unique_foods) / len(daily_unique_foods)


class FoodDatabase:
    """Manager for the food database"""
    def __init__(self):
        self.foods = {}  # id -> FoodItem
        
    def load_from_dataframe(self, df):
        """Load food items from a pandas DataFrame"""
        id_counter = iter(range(1, len(df) + 1))
        for _, row in df.iterrows():
            food_item = FoodItem.from_dataframe_row(row, id_counter)
            self.foods[food_item.id] = food_item
    
    def get_by_id(self, food_id) -> FoodItem:
        """Get a food item by ID"""
        return self.foods.get(food_id)
    
    def get_by_meal_type(self, meal_type):
        """Get all foods suitable for a specific meal type"""
        return [food for food in self.foods.values() 
                if food.meal_suitability.get(meal_type, False)]
    
    def get_by_food_group(self, food_group):
        """Get all foods in a specific food group"""
        return [food for food in self.foods.values() 
                if food.diet_guide_group == food_group]
                
    def add_attribute_to_foods(self, attribute_name, attribute_values):
        """Add a new attribute to all food items"""
        for food_id, value in attribute_values.items():
            if food_id in self.foods:
                self.foods[food_id].attributes[attribute_name] = value