## Personalized Workout & Diet Planning System

**CS5800 Final Project — Northeastern University**
 By: Weifan Li, Hui Zheng, Ziqi Shao

------

### Overview

This project aims to provide **personalized daily fitness and nutrition plans** based on user profiles using **algorithmic optimization techniques**.

Users get:

- A tailored **daily meal plan** based on nutritional needs and dietary restrictions.
- A matching **workout routine** based on fitness level and equipment access.
- Data-driven, dynamic results based on real USDA nutrition data and gym workout datasets.

------

### 🧠 Features

- 🧬 **Meal Planning Algorithm**
   Use Linear Programming to solve multi-target optimization according to a set of constraints from US diet guidelines
- 💪 **Workout Selector**
   Chooses exercises filtered by body part, equipment, and fitness level.
- 📝 **User Profile Modeling**
   Supports goals like `muscle_gain`, `weight_loss`, `endurance`.
- 📊 **Real Datasets**
  - [USDA FoodData Central](https://fdc.nal.usda.gov/download-datasets)
  - [Gym Dataset (over 600 exercises) from Kaggle.com](https://www.kaggle.com/datasets/niharika41298/gym-exercise-data?resource=download)
  - [Dietary Guidelines for Americans, 2020-2025](https://www.dietaryguidelines.gov/sites/default/files/2020-12/Dietary_Guidelines_for_Americans_2020-2025.pdf)

------

### ⚙️ How to Run

#### 1. Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

#### 2. Make sure your data is in the `data/` folder

Include:

- `foods_cleaned_with_portion.json`
- `workouts_cleaned.json`

#### 3. Run the planner

```bash
python app.py
```

------

### Example Output

```
Enter your age: 25
Enter your gender (male or female): male
Enter your weight in kg: 50
Enter your height in cm: 165
Enter your goal (weight_loss, muscle_gain, maintenance): muscle_gain
Enter your activity level (light, moderate, active): light
Diet profile selected: {'daily_calories': 2400, 'daily_vegetables': 3.0, 'daily_fruits': 2.0, 'daily_grains': 8.0, 'daily_whole_grains': 4.0, 'daily_refined_grains': 4.0, 'daily_dairy': 3.0, 'daily_protein_foods': 6.5, 'daily_oils': 31.0, 'weekly_dark_green_vegetables': 2.0, 'weekly_red_orange_vegetables': 6.0, 'weekly_beans_peas_lentils': 2.0, 'weekly_starchy_vegetables': 6.0, 'weekly_other_vegetables': 5.0, 'weekly_meats_poultry_eggs': 31.0, 'weekly_seafood': 10.0, 'weekly_nuts_seeds_soy': 5.0, 'other_calories': 320}


Generating basic meal plan...
Generating base meal plan through optimization...
Base plan metrics: {'total_unique_foods': 59, 'avg_daily_unique': 10.428571428571429, 'max_repetition': 4, 'avg_repetition': 1.2542372881355932, 'has_themes': False, 'surprise_count': 0, 'creativity_score': 0.5988095238095238}

================================================================================
WEEKLY MEAL PLAN
================================================================================
Total Calories: 17599.1
Total Proteins: 654.8g

Food Group Totals:
  - Dark-Green Vegetables: 4.0 servings
  - Red and Orange Vegetables: 6.0 servings
  - Starchy Vegetables: 6.0 servings
  - Other Vegetables: 7.0 servings
  - Beans, Peas, Lentils: 1.0 servings
  - Nuts, Seeds, Soy Products: 22.0 servings
  - Whole Grains: 29.0 servings
  - Refined Grains: 24.0 servings
  - Meats, Poultry, Eggs: 19.0 servings
  - Seafood: 10.0 servings
  - Fruits: 14.0 servings
  - Dairy: 24.8 servings
  - Oil: 0.0 servings

--------------------------------------------------------------------------------
Monday (Day 1)
Daily Calories: 2611.7
Daily Proteins: 84.0g

Breakfast - 829.6 calories
• Eggs, Grade A, Large, egg yolk (3.0 servings) - 94.7 cal, 4.6g protein
• Nuts, hazelnuts or filberts, raw (3.0 servings) - 181.8 cal, 3.8g protein

Lunch - 1069.3 calories
• Cheese, mozzarella, low moisture, part-skim (3.0 servings) - 84.5 cal, 6.7g protein
• Plum, black, with skin, raw (2.0 servings) - 146.7 cal, 1.4g protein
• Flour, barley (3.0 servings) - 103.9 cal, 2.5g protein
• Flour, pastry, unenriched, unbleached (1.0 servings) - 101.5 cal, 2.5g protein
• Flour, quinoa (1.0 servings) - 109.2 cal, 3.4g protein

Dinner - 712.9 calories
• Asparagus, green, raw (2.0 servings) - 70.3 cal, 3.6g protein
• Cabbage, bok choy, raw (1.0 servings) - 50.6 cal, 2.6g protein
• Flour, chestnut (2.0 servings) - 109.1 cal, 1.5g protein
• Flour, 00 (3.0 servings) - 101.2 cal, 3.2g protein

--------------------------------------------------------------------------------
Tuesday (Day 2)
Daily Calories: 2631.3
Daily Proteins: 104.2g

Breakfast - 526.4 calories
• Milk, nonfat, fluid, with added vitamin A and vitamin D (fat free or skim) (3.0 servings) - 9.6 cal, 1.0g protein
• Grapefruit juice, red, not fortified, not from concentrate, refrigerated (1.0 servings) - 102.7 cal, 1.4g protein
• Nuts, brazilnuts, raw (1.0 servings) - 188.1 cal, 4.3g protein
• Bulgur, dry, raw (1.0 servings) - 105.6 cal, 3.3g protein
• Flour, semolina, coarse and semi-coarse (1.0 servings) - 101.1 cal, 3.3g protein

Lunch - 948.7 calories
• Egg, yolk, raw, frozen, pasteurized (3.0 servings) - 83.9 cal, 4.4g protein
• Mushroom, pioppini (2.0 servings) - 196.2 cal, 17.5g protein
• Flour, rice, glutinous (3.0 servings) - 101.5 cal, 1.9g protein

Dinner - 1156.1 calories
• Cabbage, bok choy, raw (3.0 servings) - 50.6 cal, 2.6g protein
• Nuts, brazilnuts, raw (3.0 servings) - 188.1 cal, 4.3g protein
• Chia seeds, dry, raw (3.0 servings) - 146.6 cal, 4.8g protein

--------------------------------------------------------------------------------
Wednesday (Day 3)
Daily Calories: 2167.9
Daily Proteins: 83.0g

Breakfast - 474.4 calories
• Milk, reduced fat, fluid, 2% milkfat, with added vitamin A and vitamin D (3.0 servings) - 59.3 cal, 0.9g protein
• Grapefruit juice, white, canned or bottled, unsweetened (2.0 servings) - 95.1 cal, 1.4g protein
• Millet, whole grain (1.0 servings) - 106.5 cal, 2.8g protein

Lunch - 972.7 calories
• Beef, round, top round, boneless, choice, raw (3.0 servings) - 39.9 cal, 6.1g protein
• Fish, catfish, farm raised, raw (3.0 servings) - 36.6 cal, 4.7g protein
• Corn flour, masa harina, white or yellow, dry, raw (3.0 servings) - 106.6 cal, 2.1g protein
• Flour, spelt, whole grain (3.0 servings) - 103.1 cal, 4.1g protein
• Sorghum bran, white, unenriched, dry, raw (1.0 servings) - 114.2 cal, 3.2g protein

Dinner - 720.7 calories
• Plum, black, with skin, raw (1.0 servings) - 146.7 cal, 1.4g protein
• Potatoes, gold, without skin, raw (3.0 servings) - 183.7 cal, 4.5g protein
• Crustaceans, crab, blue swimming, lump, pasteurized, refrigerated (1.0 servings) - 23.0 cal, 5.3g protein

--------------------------------------------------------------------------------
Thursday (Day 4)
Daily Calories: 2504.4
Daily Proteins: 84.2g

Breakfast - 932.5 calories
• Cheese, pasteurized process cheese food or product, American, singles (3.0 servings) - 87.8 cal, 4.4g protein
• Nuts, brazilnuts, raw (3.0 servings) - 188.1 cal, 4.3g protein
• Fonio, grain, dry, raw (1.0 servings) - 104.6 cal, 2.0g protein

Lunch - 1027.2 calories
• Egg, yolk, raw, frozen, pasteurized (3.0 servings) - 83.9 cal, 4.4g protein
• Oranges, raw, navels (Includes foods for USDA's Food Distribution Program) (2.0 servings) - 77.5 cal, 1.5g protein
• Flour, pastry, unenriched, unbleached (3.0 servings) - 101.5 cal, 2.5g protein
• Khorasan, grain, dry, raw (3.0 servings) - 105.3 cal, 4.2g protein

Dinner - 544.7 calories
• Sausage, breakfast sausage, beef, pre-cooked, unprepared (3.0 servings) - 93.0 cal, 3.8g protein
• Tomato, roma (3.0 servings) - 54.9 cal, 1.7g protein
• Flour, semolina, coarse and semi-coarse (1.0 servings) - 101.1 cal, 3.3g protein

--------------------------------------------------------------------------------
Friday (Day 5)
Daily Calories: 2541.7
Daily Proteins: 125.9g

Breakfast - 595.3 calories
• Flour, barley (2.0 servings) - 103.9 cal, 2.5g protein
• Yogurt, Greek, plain, whole milk (3.8 servings) - 101.4 cal, 9.5g protein

Lunch - 1057.6 calories
• Cheese, American, restaurant (3.0 servings) - 106.3 cal, 5.0g protein
• Nuts, almonds, whole, raw (1.0 servings) - 177.4 cal, 6.1g protein
• Fish, salmon, Atlantic, farm raised, raw (3.0 servings) - 55.9 cal, 5.8g protein
• Beans, great northern, canned, sodium added, drained and rinsed (1.0 servings) - 292.1 cal, 17.6g protein
• Flour, semolina, fine (1.0 servings) - 101.4 cal, 3.8g protein

Dinner - 888.8 calories
• Melons, honeydew, raw (2.0 servings) - 91.7 cal, 1.3g protein
• Tomatoes, canned, red, ripe, diced (3.0 servings) - 44.1 cal, 2.1g protein
• Nuts, hazelnuts or filberts, raw (2.0 servings) - 181.8 cal, 3.8g protein
• Einkorn, grain, dry, raw (2.0 servings) - 104.7 cal, 4.3g protein

--------------------------------------------------------------------------------
Saturday (Day 6)
Daily Calories: 2606.3
Daily Proteins: 87.4g

Breakfast - 557.7 calories
• Yogurt, Greek, strawberry, nonfat (3.0 servings) - 23.5 cal, 2.3g protein
• Cranberry juice, not fortified, from concentrate, shelf stable (2.0 servings) - 80.2 cal, 0.0g protein
• Flour, amaranth (3.0 servings) - 108.9 cal, 3.7g protein

Lunch - 903.2 calories
• Nuts, walnuts, English, halves, raw (3.0 servings) - 206.8 cal, 4.1g protein
• Beef, round, eye of round roast, boneless, separable lean only, trimmed to 0" fat, select, raw (1.0 servings) - 34.6 cal, 6.6g protein
• Chia seeds, dry, raw (1.0 servings) - 146.6 cal, 4.8g protein
• Flour, pastry, unenriched, unbleached (1.0 servings) - 101.5 cal, 2.5g protein

Dinner - 1145.5 calories
• Asparagus, green, raw (3.0 servings) - 70.3 cal, 3.6g protein
• Beef, loin, tenderloin roast, separable lean only, boneless, trimmed to 0" fat, select, cooked, roasted (3.0 servings) - 208.4 cal, 7.9g protein
• Sorghum flour, white, pearled, unenriched, dry, raw (3.0 servings) - 103.2 cal, 2.9g protein

--------------------------------------------------------------------------------
Sunday (Day 7)
Daily Calories: 2535.8
Daily Proteins: 86.0g

Breakfast - 570.4 calories
• Orange juice, no pulp, not fortified, from concentrate, refrigerated (2.0 servings) - 118.1 cal, 1.8g protein
• Bread, white, commercially prepared (3.0 servings) - 76.5 cal, 2.7g protein
• Fonio, grain, dry, raw (1.0 servings) - 104.6 cal, 2.0g protein

Lunch - 1081.4 calories
• Cottage cheese, full fat, large or small curd (3.0 servings) - 29.2 cal, 3.3g protein
• Potatoes, red, without skin, raw (3.0 servings) - 188.9 cal, 5.2g protein
• Fish, salmon, sockeye, wild caught, raw (3.0 servings) - 36.8 cal, 6.3g protein
• Bulgur, dry, raw (3.0 servings) - 105.6 cal, 3.3g protein

Dinner - 884.0 calories
• Nuts, brazilnuts, raw (3.0 servings) - 188.1 cal, 4.3g protein
• Nuts, pecans, halves, raw (1.0 servings) - 212.7 cal, 2.8g protein
• Flour, sorghum (1.0 servings) - 106.6 cal, 2.4g protein
```

------

### Algorithms Used

- **Linear Programming** for Meal Planning
- **Filtering Logic** for workout selection by fitness constraints
- Future extensions may include:
  - Genetic Algorithm (GA) for multi-objective optimization
  - Dynamic programming for weekly balancing

------

### Team Roles

- **Weifan Li** – Nutrition modeling, Data preprocessing 
- **Hui Zheng** – Workout generation, evaluation metrics
- **Ziqi Shao** – Meal planning, algorithm comparison, optimization logic

------

### 📌 Notes

- This is not a medical tool. For clinical advice, consult a professional.
- Foods and workouts are examples for academic and prototype purposes.