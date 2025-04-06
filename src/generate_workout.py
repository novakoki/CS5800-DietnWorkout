import pandas as pd
from user_profile import UserProfile

def select_daily_workout(user: UserProfile, workout_file="data/workouts_cleaned.json"):
    df = pd.read_json(workout_file)

    df_filtered = df[
        (df["level"].str.lower() == user.fitness_level.lower()) &
        (df["equipment"].isin(user.available_equipment))
    ]

    if df_filtered.empty:
        df_filtered = df  # fallback to all workouts

    selected = df_filtered.sample(n=2 if user.goal == "muscle_gain" else 1)

    return selected.to_dict(orient="records")
