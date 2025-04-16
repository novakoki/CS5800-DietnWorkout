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
{'daily_calories': 2400, 'daily_vegetables': 3.0, 'daily_fruits': 2.0, 'daily_grains': 8.0, 'daily_whole_grains': 4.0, 'daily_refined_grains': 4.0, 'daily_dairy': 3.0, 'daily_protein_foods': 6.5, 'daily_oils': 31.0, 'weekly_dark_green_vegetables': 2.0, 'weekly_red_orange_vegetables': 6.0, 'weekly_beans_peas_lentils': 2.0, 'weekly_starchy_vegetables': 6.0, 'weekly_other_vegetables': 5.0, 'weekly_meats_poultry_eggs': 31.0, 'weekly_seafood': 10.0, 'weekly_nuts_seeds_soy': 5.0, 'other_calories': 320}


Generating basic meal plan...
Generating base meal plan through optimization...
Base plan metrics: {'total_unique_foods': 46, 'avg_daily_unique': 7.857142857142857, 'max_repetition': 3, 'avg_repetition': 1.1956521739130435, 'has_themes': False, 'surprise_count': 0, 'creativity_score': 0.5261904761904762}

================================================================================
WEEKLY MEAL PLAN
================================================================================
Total Calories: 17126.0
Total Proteins: 661.6g

Food Group Totals:
  - Dark-Green Vegetables: 4.0 servings
  - Red and Orange Vegetables: 6.0 servings
  - Starchy Vegetables: 6.0 servings
  - Other Vegetables: 6.0 servings
  - Beans, Peas, Lentils: 2.0 servings
  - Nuts, Seeds, Soy Products: 2.0 servings
  - Whole Grains: 34.0 servings
  - Refined Grains: 28.0 servings
  - Meats, Poultry, Eggs: 37.4 servings
  - Seafood: 6.0 servings
  - Fruits: 14.0 servings
  - Dairy: 23.2 servings
  - Oil: 0.0 servings

--------------------------------------------------------------------------------
Monday (Day 1)
Daily Calories: 2636.7
Daily Proteins: 118.8g

Breakfast - 562.7 calories
• Cheese, American, restaurant (3.0 servings) - 106.3 cal, 5.0g protein
• Cookies, oatmeal, soft, with raisins (2.0 servings) - 121.9 cal, 1.6g protein

Lunch - 1117.7 calories
• Tomato, sauce, canned, with salt added (3.0 servings) - 85.4 cal, 3.4g protein
• Farro, pearled, dry, raw (2.0 servings) - 104.0 cal, 3.6g protein
• Flour, amaranth (6.0 servings) - 108.9 cal, 3.7g protein

Dinner - 956.2 calories
• Grapes, green, seedless, raw (2.0 servings) - 200.3 cal, 2.2g protein
• Beef, loin, top loin steak, boneless, lip-on, separable lean only, trimmed to 1/8" fat, choice, raw (6.0 servings) - 43.9 cal, 6.5g protein
• Beans, great northern, canned, sodium added, drained and rinsed (1.0 servings) - 292.1 cal, 17.6g protein

--------------------------------------------------------------------------------
Tuesday (Day 2)
Daily Calories: 2524.8
Daily Proteins: 89.2g

Breakfast - 654.9 calories
• Eggs, Grade A, Large, egg white (10.0 servings) - 65.5 cal, 3.0g protein

Lunch - 1072.8 calories
• Cheese, cotija, solid (3.0 servings) - 99.6 cal, 6.8g protein
• Cranberry juice, not fortified, from concentrate, shelf stable (2.0 servings) - 80.2 cal, 0.0g protein
• Potatoes, russet, without skin, raw (1.0 servings) - 208.5 cal, 5.7g protein
• Flour, 00 (4.0 servings) - 101.2 cal, 3.2g protein

Dinner - 797.2 calories
• Potatoes, red, without skin, raw (2.0 servings) - 188.9 cal, 5.2g protein
• Rice, red, unenriched, dry, raw (4.0 servings) - 104.8 cal, 2.4g protein

--------------------------------------------------------------------------------
Wednesday (Day 3)
Daily Calories: 2262.4
Daily Proteins: 74.3g

Breakfast - 519.1 calories
• Cheese, American, restaurant (1.0 servings) - 106.3 cal, 5.0g protein
• Flour, corn, yellow, fine meal, enriched (4.0 servings) - 103.2 cal, 1.8g protein

Lunch - 879.7 calories
• Cheese, oaxaca, solid (2.0 servings) - 84.2 cal, 6.3g protein
• Grapes, green, seedless, raw (1.0 servings) - 200.3 cal, 2.2g protein
• Kale, raw (3.0 servings) - 30.5 cal, 0.6g protein
• Rice, black, unenriched, raw (4.0 servings) - 104.9 cal, 2.1g protein

Dinner - 863.6 calories
• Chicken, broilers or fryers, drumstick, meat only, cooked, braised (1.0 servings) - 184.8 cal, 6.8g protein
• Mandarin, seedless, peeled, raw (1.0 servings) - 154.9 cal, 2.6g protein
• Fish, haddock, raw (6.0 servings) - 87.3 cal, 4.6g protein

--------------------------------------------------------------------------------
Thursday (Day 4)
Daily Calories: 2262.8
Daily Proteins: 77.9g

Breakfast - 755.2 calories
• Yogurt, plain, nonfat (3.0 servings) - 14.2 cal, 1.2g protein
• Raspberries, raw (2.0 servings) - 143.3 cal, 2.5g protein
• Millet, whole grain (4.0 servings) - 106.5 cal, 2.8g protein

Lunch - 457.4 calories
• Egg, white, raw, frozen, pasteurized (1.7 servings) - 23.0 cal, 4.8g protein
• Wild rice, dry, raw (4.0 servings) - 104.7 cal, 3.6g protein

Dinner - 1050.3 calories
• Corn, sweet, yellow and white kernels, fresh, raw (3.0 servings) - 211.4 cal, 7.0g protein
• Farro, pearled, dry, raw (4.0 servings) - 104.0 cal, 3.6g protein

--------------------------------------------------------------------------------
Friday (Day 5)
Daily Calories: 2450.6
Daily Proteins: 140.3g

Breakfast - 471.3 calories
• Eggs, Grade A, Large, egg whole (2.7 servings) - 114.4 cal, 9.6g protein
• Pears, raw, bartlett (2.0 servings) - 79.8 cal, 0.5g protein

Lunch - 870.9 calories
• Cheese, feta, whole milk, crumbled (2.0 servings) - 77.4 cal, 5.6g protein
• Beans, snap, green, raw (3.0 servings) - 100.0 cal, 4.9g protein
• Farro, pearled, dry, raw (4.0 servings) - 104.0 cal, 3.6g protein

Dinner - 1108.4 calories
• Arugula, baby, raw (1.0 servings) - 77.5 cal, 4.1g protein
• Beef, flank, steak, boneless, choice, raw (6.0 servings) - 46.5 cal, 5.7g protein
• Beans, kidney, dark red, canned, sodium added, sugar added, drained and rinsed (1.0 servings) - 316.6 cal, 19.5g protein
• Flour, amaranth (4.0 servings) - 108.9 cal, 3.7g protein

--------------------------------------------------------------------------------
Saturday (Day 6)
Daily Calories: 2451.0
Daily Proteins: 89.0g

Breakfast - 644.8 calories
• Yogurt, Greek, plain, whole milk (3.0 servings) - 26.6 cal, 2.5g protein
• Cream, sour, full fat (3.2 servings) - 177.4 cal, 2.8g protein

Lunch - 732.8 calories
• Tomato, puree, canned (3.0 servings) - 102.1 cal, 3.9g protein
• Corn flour, masa harina, white or yellow, dry, raw (4.0 servings) - 106.6 cal, 2.1g protein

Dinner - 1073.4 calories
• Kiwifruit, green, raw (2.0 servings) - 145.0 cal, 2.6g protein
• Flour, almond (1.0 servings) - 176.3 cal, 7.4g protein
• Beef, flank, steak, boneless, choice, raw (4.0 servings) - 46.5 cal, 5.7g protein
• Khorasan, grain, dry, raw (4.0 servings) - 105.3 cal, 4.2g protein

--------------------------------------------------------------------------------
Sunday (Day 7)
Daily Calories: 2537.7
Daily Proteins: 72.1g

Breakfast - 984.4 calories
• Sausage, breakfast sausage, beef, pre-cooked, unprepared (6.0 servings) - 93.0 cal, 3.8g protein
• Corn flour, masa harina, white or yellow, dry, raw (4.0 servings) - 106.6 cal, 2.1g protein

Lunch - 925.3 calories
• Cheese, ricotta, whole milk (3.0 servings) - 186.3 cal, 2.2g protein
• Pears, raw, bartlett (2.0 servings) - 79.8 cal, 0.5g protein
• Cauliflower, raw (3.0 servings) - 69.0 cal, 4.1g protein

Dinner - 628.0 calories
• Nuts, walnuts, English, halves, raw (1.0 servings) - 206.8 cal, 4.1g protein
• Khorasan, grain, dry, raw (4.0 servings) - 105.3 cal, 4.2g protein
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