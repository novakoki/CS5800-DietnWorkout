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

- 🧬 **Greedy Meal Planning Algorithm**
   Maximizes protein and fiber intake within a calorie budget.
- 💪 **Workout Selector**
   Chooses exercises filtered by body part, equipment, and fitness level.
- 📝 **User Profile Modeling**
   Supports goals like `muscle_gain`, `weight_loss`, `endurance`.
- 📊 **Real Datasets**
  - [USDA FoodData Central](https://fdc.nal.usda.gov/download-datasets)
  - [Gym Dataset (over 600 exercises) from Kaggle.com](https://www.kaggle.com/datasets/niharika41298/gym-exercise-data?resource=download)

------

### Project Structure

```bash
CS5800-DietnWorkout/
┣ data/
┃ ┣ food.csv
┃ ┣ foods_cleaned_with_portion.json
┃ ┣ food_nutrient.csv
┃ ┣ food_portion.csv
┃ ┣ GymDataset.csv
┃ ┣ nutrient.csv
┃ ┗ workouts_cleaned.json
┣ src/
┃ ┣ __pycache__/
┃ ┣ generate_meals.py
┃ ┣ generate_workout.py
┃ ┣ planner.py
┃ ┗ user_profile.py
┣ utils/
┃ ┣ food_data_csv.py
┃ ┗ gym_workout_csv.py
┣ README.md
┗ requirements.txt
```

------

### ⚙️ How to Run

#### 1. Install dependencies

```bash
pip install -r requirements.txt
```

#### 2. Make sure your data is in the `data/` folder

Include:

- `foods_cleaned_with_portion.json`
- `workouts_cleaned.json`

#### 3. Run the planner

```bash
cd src
python planner.py
```

------

### Example Output

```jason
json{
  "user_summary": {
    "BMR": 1700,
    "Daily Calorie Target": 2400,
    "Fitness Level": "beginner",
    "Equipment": ["Body Only", "Dumbbells"]
  },
  "meals": {
    "calorie_target": 2400,
    "total_calories": 2322,
    "total_protein": 132,
    "meals": [ ... ]
  },
  "workout": [
    {
      "title": "Push-Up",
      "desc": "...",
      "type": "Strength",
      "equipment": "Body Only",
      "level": "Beginner"
    }
  ]
}
```

------

### Algorithms Used

- **Greedy Selection** for maximizing protein-to-calorie ratio in meals
- **Filtering Logic** for workout selection by fitness constraints
- Future extensions may include:
  - Genetic Algorithm (GA) for multi-objective optimization
  - Dynamic programming for weekly balancing

------

### Team Roles

- **Weifan Li** – Nutrition modeling, Data preprocessing 
- **Hui Zheng** – Workout generation, evaluation metrics
- **Ziqi Shao** – algorithm comparison, optimization logic

------

### 📌 Notes

- This is not a medical tool. For clinical advice, consult a professional.
- Foods and workouts are examples for academic and prototype purposes.