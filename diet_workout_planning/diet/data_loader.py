import pandas as pd
import numpy as np

def get_food_data():
    food_data = pd.read_csv("data/foundation_food_with_nutrients_and_diet_group.csv")
    food_data.rename(columns={"Energy": "calories", "Protein": "proteins"}, inplace=True)

    food_portion_data = pd.read_csv("data/FoodData_Central_foundation_food_csv_2024-10-31/food_portion.csv")

    for index, row in food_data.iterrows():
        if np.isnan(row["calories"]):
            if not np.isnan(row["Energy (Atwater General Factors)"]):
                food_data.at[index, "calories"] = row["Energy (Atwater General Factors)"]
            else:
                food_data.at[index, "calories"] = 10000

    food_data = food_data[["fdc_id", "name", "diet_guide_group", "calories", "proteins", "breakfast", "lunch", "dinner"]]

    # vegetables and fruits use cup as the unit
    cup_groups = ["Dark-Green Vegetables", "Red and Orange Vegetables", "Starchy Vegetables", "Other Vegetables", "Beans, Peas, Lentils", "Fruits"]

    cup_food = food_data[food_data["diet_guide_group"].isin(cup_groups)]
    # print(cup_food)

    for index, row in cup_food.iterrows():
        food_portion_data_rows = food_portion_data[food_portion_data["fdc_id"] == row["fdc_id"]]
        cup_rows = food_portion_data_rows[food_portion_data_rows["measure_unit_id"] == 1000]

        if len(cup_rows) != 0:
            cup_to_grams = cup_rows["gram_weight"].values[0] / cup_rows["amount"].values[0]
        else:
            tablespoon_rows = food_portion_data_rows[food_portion_data_rows["measure_unit_id"] == 1001]

            if len(tablespoon_rows) != 0:
                cup_to_grams = tablespoon_rows["gram_weight"].values[0] / tablespoon_rows["amount"].values[0] * 16
            else:
                cup_to_grams = 250
        
        food_data.at[index, "calories"] = row["calories"] / (100 / cup_to_grams)
        food_data.at[index, "proteins"] = row["proteins"] / (100 / cup_to_grams)

    # print(food_data[food_data["diet_guide_group"].isin(cup_groups)])

    ounce_groups = ["Meats, Poultry, Eggs", "Seafood", "Nuts, Seeds, Soy Products", "Dairy", "Whole Grains", "Refined Grains"]
    ounce_to_grams = 28.3495

    ounce_food = food_data[food_data["diet_guide_group"].isin(ounce_groups)]
    # print(ounce_food)
    for index, row in ounce_food.iterrows():
        if row["calories"] != 10000:
            food_data.at[index, "calories"] = row["calories"] / (100 / ounce_to_grams)
        food_data.at[index, "proteins"] = row["proteins"] / (100 / ounce_to_grams)
    # print(food_data[food_data["diet_guide_group"].isin(ounce_groups)])

    return food_data