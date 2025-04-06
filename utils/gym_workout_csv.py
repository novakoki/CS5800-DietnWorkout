import pandas as pd
import json

def parse_workout_data(
    input_csv,
    output_path="workouts_cleaned.json",
    output_format="json"
):
    # Load workout CSV
    df = pd.read_csv(input_csv)

    # Drop workouts missing a name or description
    df = df.dropna(subset=["Title", "Desc"])

    # Select and rename relevant fields
    df_cleaned = df.rename(columns={
        "Title": "title",
        "Desc": "desc",
        "Type": "type",
        "BodyPart": "body_part",
        "Equipment": "equipment",
        "Level": "level"
    })[["title", "desc", "type", "body_part", "equipment", "level"]]

    # Remove duplicates
    df_cleaned = df_cleaned.drop_duplicates()

    # Output to file
    if output_format == "json":
        df_cleaned.to_json(output_path, orient="records", indent=2, force_ascii=False)
    elif output_format == "csv":
        df_cleaned.to_csv(output_path, index=False)
    else:
        raise ValueError("Output format must be 'json' or 'csv'")

    print(f"✅ Saved {len(df_cleaned)} workouts to {output_path}")


# ========== Run Script ========== #
if __name__ == "__main__":
    parse_workout_data(
        input_csv="data/GymDataset.csv",
        output_path="data/workouts_cleaned.json",
        output_format="json"  # or "csv"
    )
