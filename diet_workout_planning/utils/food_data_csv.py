import pandas as pd
import json
import os


def parse_usda_csv(
    food_csv,
    nutrient_csv,
    food_nutrient_csv,
    food_portion_csv,
    output_path="foods_cleaned.json"
):
    # Load data
    food_df = pd.read_csv(food_csv)
    nutrient_df = pd.read_csv(nutrient_csv)
    food_nutrient_df = pd.read_csv(food_nutrient_csv)
    portion_df = pd.read_csv(food_portion_csv)

    # Target nutrient names
    target_nutrients = [
        "Energy",
        "Protein",
        "Total lipid (fat)",
        "Carbohydrate, by difference",
        "Fiber, total dietary"
    ]

    # Get nutrient IDs
    nutrients = nutrient_df[nutrient_df['name'].isin(target_nutrients)][['id', 'name']]
    nutrient_id_to_name = dict(zip(nutrients['id'], nutrients['name']))

    # Filter nutrient values
    filtered_fn = food_nutrient_df[food_nutrient_df['nutrient_id'].isin(nutrient_id_to_name.keys())]

    # Pivot to get one row per food with each nutrient
    pivoted = filtered_fn.pivot_table(
        index='fdc_id',
        columns='nutrient_id',
        values='amount',
        aggfunc='first'
    ).reset_index()

    # Rename nutrient_id columns to names
    pivoted.rename(columns=nutrient_id_to_name, inplace=True)

    # Merge with food descriptions
    merged = pd.merge(pivoted, food_df[['fdc_id', 'description']], on='fdc_id', how='left')

    # Add portion size (use first available portion per food)
    portion_first = portion_df.sort_values('seq_num').drop_duplicates('fdc_id')
    merged = pd.merge(merged, portion_first[['fdc_id', 'gram_weight']], on='fdc_id', how='left')

    # Rename columns
    merged.rename(columns={'description': 'name', 'gram_weight': 'portion_g'}, inplace=True)

    # Fix duplicate "Energy" column if needed
    energy_columns = [col for col in merged.columns if col == 'Energy']
    if len(energy_columns) > 1:
        merged.columns.values[list(merged.columns).index('Energy')] = 'Energy_kcal'
        merged.columns.values[list(merged.columns).index('Energy', 1)] = 'Energy_kJ'
    elif 'Energy' in merged.columns:
        merged.rename(columns={'Energy': 'Energy_kcal'}, inplace=True)

    # Handle fallback to kJ if kcal missing
    if 'Energy_kJ' in merged.columns:
        merged['calories'] = merged['Energy_kcal'].fillna(merged['Energy_kJ'] * 0.239006)
    else:
        merged['calories'] = merged['Energy_kcal']

    # Final output
    final_df = merged.rename(columns={
        'Protein': 'protein',
        'Total lipid (fat)': 'fat',
        'Carbohydrate, by difference': 'carbs',
        'Fiber, total dietary': 'fiber'
    })[['name', 'portion_g', 'calories', 'protein', 'fat', 'carbs', 'fiber']]

    # Drop rows with missing values
    final_df = final_df.dropna(subset=['calories', 'protein'])

    # Save to JSON
    final_df.to_json(output_path, orient="records", indent=2, force_ascii=False)
    print(f"Saved {len(final_df)} entries to {output_path}")


# ========== Run Script ========== #
if __name__ == "__main__":
    parse_usda_csv(
        food_csv="data/food.csv",
        nutrient_csv="data/nutrient.csv",
        food_nutrient_csv="data/food_nutrient.csv",
        food_portion_csv="data/food_portion.csv",
        output_path="data/foods_cleaned_with_portion.json"
    )
