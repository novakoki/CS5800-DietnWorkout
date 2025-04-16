# Dictionary of user profiles for different calorie levels based on USDA dietary guidelines

dietary_profiles = {
    # 1,000 Calorie Level
    1000: {
        'daily_calories': 1000,
        # Daily amounts
        'daily_vegetables': 1.0,  # cup eq/day
        'daily_fruits': 1.0,  # cup eq/day
        'daily_grains': 3.0,  # ounce eq/day
        'daily_whole_grains': 1.5,  # ounce eq/day
        'daily_refined_grains': 1.5,  # ounce eq/day
        'daily_dairy': 2.0,  # cup eq/day
        'daily_protein_foods': 2.0,  # ounce eq/day
        'daily_oils': 15.0,  # grams/day
        # Weekly amounts
        'weekly_dark_green_vegetables': 0.5,  # cup eq/wk
        'weekly_red_orange_vegetables': 2.5,  # cup eq/wk
        'weekly_beans_peas_lentils': 0.5,  # cup eq/wk
        'weekly_starchy_vegetables': 2.0,  # cup eq/wk
        'weekly_other_vegetables': 1.5,  # cup eq/wk
        'weekly_meats_poultry_eggs': 10.0,  # ounce eq/wk
        'weekly_seafood': 2.5,  # ounce eq/wk (average of range 2-3)
        'weekly_nuts_seeds_soy': 2.0,  # ounce eq/wk
        # Other
        'other_calories': 130  # kcal/day
    },
    
    # 1,200 Calorie Level
    1200: {
        'daily_calories': 1200,
        # Daily amounts
        'daily_vegetables': 1.5,  # cup eq/day
        'daily_fruits': 1.0,  # cup eq/day
        'daily_grains': 4.0,  # ounce eq/day
        'daily_whole_grains': 2.0,  # ounce eq/day
        'daily_refined_grains': 2.0,  # ounce eq/day
        'daily_dairy': 2.5,  # cup eq/day
        'daily_protein_foods': 3.0,  # ounce eq/day
        'daily_oils': 17.0,  # grams/day
        # Weekly amounts
        'weekly_dark_green_vegetables': 1.0,  # cup eq/wk
        'weekly_red_orange_vegetables': 3.0,  # cup eq/wk
        'weekly_beans_peas_lentils': 0.5,  # cup eq/wk
        'weekly_starchy_vegetables': 3.5,  # cup eq/wk
        'weekly_other_vegetables': 2.5,  # cup eq/wk
        'weekly_meats_poultry_eggs': 14.0,  # ounce eq/wk
        'weekly_seafood': 4.0,  # ounce eq/wk
        'weekly_nuts_seeds_soy': 2.0,  # ounce eq/wk
        # Other
        'other_calories': 80  # kcal/day
    },
    
    # 1,400 Calorie Level
    1400: {
        'daily_calories': 1400,
        # Daily amounts
        'daily_vegetables': 1.5,  # cup eq/day
        'daily_fruits': 1.5,  # cup eq/day
        'daily_grains': 5.0,  # ounce eq/day
        'daily_whole_grains': 2.5,  # ounce eq/day
        'daily_refined_grains': 2.5,  # ounce eq/day
        'daily_dairy': 2.5,  # cup eq/day
        'daily_protein_foods': 4.0,  # ounce eq/day
        'daily_oils': 17.0,  # grams/day
        # Weekly amounts
        'weekly_dark_green_vegetables': 1.0,  # cup eq/wk
        'weekly_red_orange_vegetables': 3.0,  # cup eq/wk
        'weekly_beans_peas_lentils': 0.5,  # cup eq/wk
        'weekly_starchy_vegetables': 3.5,  # cup eq/wk
        'weekly_other_vegetables': 2.5,  # cup eq/wk
        'weekly_meats_poultry_eggs': 19.0,  # ounce eq/wk
        'weekly_seafood': 6.0,  # ounce eq/wk
        'weekly_nuts_seeds_soy': 3.0,  # ounce eq/wk
        # Other
        'other_calories': 90  # kcal/day
    },
    
    # 1,600 Calorie Level
    1600: {
        'daily_calories': 1600,
        # Daily amounts
        'daily_vegetables': 2.0,  # cup eq/day
        'daily_fruits': 1.5,  # cup eq/day
        'daily_grains': 5.0,  # ounce eq/day
        'daily_whole_grains': 3.0,  # ounce eq/day
        'daily_refined_grains': 2.0,  # ounce eq/day
        'daily_dairy': 3.0,  # cup eq/day
        'daily_protein_foods': 5.0,  # ounce eq/day
        'daily_oils': 22.0,  # grams/day
        # Weekly amounts
        'weekly_dark_green_vegetables': 1.5,  # cup eq/wk
        'weekly_red_orange_vegetables': 4.0,  # cup eq/wk
        'weekly_beans_peas_lentils': 1.0,  # cup eq/wk
        'weekly_starchy_vegetables': 4.0,  # cup eq/wk
        'weekly_other_vegetables': 3.5,  # cup eq/wk
        'weekly_meats_poultry_eggs': 23.0,  # ounce eq/wk
        'weekly_seafood': 8.0,  # ounce eq/wk
        'weekly_nuts_seeds_soy': 4.0,  # ounce eq/wk
        # Other
        'other_calories': 100  # kcal/day
    },
    
    # 1,800 Calorie Level
    1800: {
        'daily_calories': 1800,
        # Daily amounts
        'daily_vegetables': 2.5,  # cup eq/day
        'daily_fruits': 1.5,  # cup eq/day
        'daily_grains': 6.0,  # ounce eq/day
        'daily_whole_grains': 3.0,  # ounce eq/day
        'daily_refined_grains': 3.0,  # ounce eq/day
        'daily_dairy': 3.0,  # cup eq/day
        'daily_protein_foods': 5.0,  # ounce eq/day
        'daily_oils': 24.0,  # grams/day
        # Weekly amounts
        'weekly_dark_green_vegetables': 1.5,  # cup eq/wk
        'weekly_red_orange_vegetables': 5.5,  # cup eq/wk
        'weekly_beans_peas_lentils': 1.5,  # cup eq/wk
        'weekly_starchy_vegetables': 5.0,  # cup eq/wk
        'weekly_other_vegetables': 4.0,  # cup eq/wk
        'weekly_meats_poultry_eggs': 23.0,  # ounce eq/wk
        'weekly_seafood': 8.0,  # ounce eq/wk
        'weekly_nuts_seeds_soy': 4.0,  # ounce eq/wk
        # Other
        'other_calories': 140  # kcal/day
    },
    
    # 2,000 Calorie Level
    2000: {
        'daily_calories': 2000,
        # Daily amounts
        'daily_vegetables': 2.5,  # cup eq/day
        'daily_fruits': 2.0,  # cup eq/day
        'daily_grains': 6.0,  # ounce eq/day
        'daily_whole_grains': 3.0,  # ounce eq/day
        'daily_refined_grains': 3.0,  # ounce eq/day
        'daily_dairy': 3.0,  # cup eq/day
        'daily_protein_foods': 5.5,  # ounce eq/day
        'daily_oils': 27.0,  # grams/day
        # Weekly amounts
        'weekly_dark_green_vegetables': 1.5,  # cup eq/wk
        'weekly_red_orange_vegetables': 5.5,  # cup eq/wk
        'weekly_beans_peas_lentils': 1.5,  # cup eq/wk
        'weekly_starchy_vegetables': 5.0,  # cup eq/wk
        'weekly_other_vegetables': 4.0,  # cup eq/wk
        'weekly_meats_poultry_eggs': 26.0,  # ounce eq/wk
        'weekly_seafood': 8.0,  # ounce eq/wk
        'weekly_nuts_seeds_soy': 5.0,  # ounce eq/wk
        # Other
        'other_calories': 240  # kcal/day
    },
    
    # 2,200 Calorie Level
    2200: {
        'daily_calories': 2200,
        # Daily amounts
        'daily_vegetables': 3.0,  # cup eq/day
        'daily_fruits': 2.0,  # cup eq/day
        'daily_grains': 7.0,  # ounce eq/day
        'daily_whole_grains': 3.5,  # ounce eq/day
        'daily_refined_grains': 3.5,  # ounce eq/day
        'daily_dairy': 3.0,  # cup eq/day
        'daily_protein_foods': 6.0,  # ounce eq/day
        'daily_oils': 29.0,  # grams/day
        # Weekly amounts
        'weekly_dark_green_vegetables': 2.0,  # cup eq/wk
        'weekly_red_orange_vegetables': 6.0,  # cup eq/wk
        'weekly_beans_peas_lentils': 2.0,  # cup eq/wk
        'weekly_starchy_vegetables': 6.0,  # cup eq/wk
        'weekly_other_vegetables': 5.0,  # cup eq/wk
        'weekly_meats_poultry_eggs': 28.0,  # ounce eq/wk
        'weekly_seafood': 9.0,  # ounce eq/wk
        'weekly_nuts_seeds_soy': 5.0,  # ounce eq/wk
        # Other
        'other_calories': 250  # kcal/day
    },
    
    # 2,400 Calorie Level
    2400: {
        'daily_calories': 2400,
        # Daily amounts
        'daily_vegetables': 3.0,  # cup eq/day
        'daily_fruits': 2.0,  # cup eq/day
        'daily_grains': 8.0,  # ounce eq/day
        'daily_whole_grains': 4.0,  # ounce eq/day
        'daily_refined_grains': 4.0,  # ounce eq/day
        'daily_dairy': 3.0,  # cup eq/day
        'daily_protein_foods': 6.5,  # ounce eq/day
        'daily_oils': 31.0,  # grams/day
        # Weekly amounts
        'weekly_dark_green_vegetables': 2.0,  # cup eq/wk
        'weekly_red_orange_vegetables': 6.0,  # cup eq/wk
        'weekly_beans_peas_lentils': 2.0,  # cup eq/wk
        'weekly_starchy_vegetables': 6.0,  # cup eq/wk
        'weekly_other_vegetables': 5.0,  # cup eq/wk
        'weekly_meats_poultry_eggs': 31.0,  # ounce eq/wk
        'weekly_seafood': 10.0,  # ounce eq/wk
        'weekly_nuts_seeds_soy': 5.0,  # ounce eq/wk
        # Other
        'other_calories': 320  # kcal/day
    },
    
    # 2,600 Calorie Level
    2600: {
        'daily_calories': 2600,
        # Daily amounts
        'daily_vegetables': 3.5,  # cup eq/day
        'daily_fruits': 2.0,  # cup eq/day
        'daily_grains': 9.0,  # ounce eq/day
        'daily_whole_grains': 4.5,  # ounce eq/day
        'daily_refined_grains': 4.5,  # ounce eq/day
        'daily_dairy': 3.0,  # cup eq/day
        'daily_protein_foods': 6.5,  # ounce eq/day
        'daily_oils': 34.0,  # grams/day
        # Weekly amounts
        'weekly_dark_green_vegetables': 2.5,  # cup eq/wk
        'weekly_red_orange_vegetables': 7.0,  # cup eq/wk
        'weekly_beans_peas_lentils': 2.5,  # cup eq/wk
        'weekly_starchy_vegetables': 7.0,  # cup eq/wk
        'weekly_other_vegetables': 5.5,  # cup eq/wk
        'weekly_meats_poultry_eggs': 31.0,  # ounce eq/wk
        'weekly_seafood': 10.0,  # ounce eq/wk
        'weekly_nuts_seeds_soy': 5.0,  # ounce eq/wk
        # Other
        'other_calories': 350  # kcal/day
    },
    
    # 2,800 Calorie Level
    2800: {
        'daily_calories': 2800,
        # Daily amounts
        'daily_vegetables': 3.5,  # cup eq/day
        'daily_fruits': 2.5,  # cup eq/day
        'daily_grains': 10.0,  # ounce eq/day
        'daily_whole_grains': 5.0,  # ounce eq/day
        'daily_refined_grains': 5.0,  # ounce eq/day
        'daily_dairy': 3.0,  # cup eq/day
        'daily_protein_foods': 7.0,  # ounce eq/day
        'daily_oils': 36.0,  # grams/day
        # Weekly amounts
        'weekly_dark_green_vegetables': 2.5,  # cup eq/wk
        'weekly_red_orange_vegetables': 7.0,  # cup eq/wk
        'weekly_beans_peas_lentils': 2.5,  # cup eq/wk
        'weekly_starchy_vegetables': 7.0,  # cup eq/wk
        'weekly_other_vegetables': 5.5,  # cup eq/wk
        'weekly_meats_poultry_eggs': 33.0,  # ounce eq/wk
        'weekly_seafood': 10.0,  # ounce eq/wk
        'weekly_nuts_seeds_soy': 6.0,  # ounce eq/wk
        # Other
        'other_calories': 370  # kcal/day
    },
    
    # 3,000 Calorie Level
    3000: {
        'daily_calories': 3000,
        # Daily amounts
        'daily_vegetables': 4.0,  # cup eq/day
        'daily_fruits': 2.5,  # cup eq/day
        'daily_grains': 10.0,  # ounce eq/day
        'daily_whole_grains': 5.0,  # ounce eq/day
        'daily_refined_grains': 5.0,  # ounce eq/day
        'daily_dairy': 3.0,  # cup eq/day
        'daily_protein_foods': 7.0,  # ounce eq/day
        'daily_oils': 44.0,  # grams/day
        # Weekly amounts
        'weekly_dark_green_vegetables': 2.5,  # cup eq/wk
        'weekly_red_orange_vegetables': 7.5,  # cup eq/wk
        'weekly_beans_peas_lentils': 3.0,  # cup eq/wk
        'weekly_starchy_vegetables': 8.0,  # cup eq/wk
        'weekly_other_vegetables': 7.0,  # cup eq/wk
        'weekly_meats_poultry_eggs': 33.0,  # ounce eq/wk
        'weekly_seafood': 10.0,  # ounce eq/wk
        'weekly_nuts_seeds_soy': 6.0,  # ounce eq/wk
        # Other
        'other_calories': 440  # kcal/day
    },
    
    # 3,200 Calorie Level
    3200: {
        'daily_calories': 3200,
        # Daily amounts
        'daily_vegetables': 4.0,  # cup eq/day
        'daily_fruits': 2.5,  # cup eq/day
        'daily_grains': 10.0,  # ounce eq/day
        'daily_whole_grains': 5.0,  # ounce eq/day
        'daily_refined_grains': 5.0,  # ounce eq/day
        'daily_dairy': 3.0,  # cup eq/day
        'daily_protein_foods': 7.0,  # ounce eq/day
        'daily_oils': 51.0,  # grams/day
        # Weekly amounts
        'weekly_dark_green_vegetables': 2.5,  # cup eq/wk
        'weekly_red_orange_vegetables': 7.5,  # cup eq/wk
        'weekly_beans_peas_lentils': 3.0,  # cup eq/wk
        'weekly_starchy_vegetables': 8.0,  # cup eq/wk
        'weekly_other_vegetables': 7.0,  # cup eq/wk
        'weekly_meats_poultry_eggs': 33.0,  # ounce eq/wk
        'weekly_seafood': 10.0,  # ounce eq/wk
        'weekly_nuts_seeds_soy': 6.0,  # ounce eq/wk
        # Other
        'other_calories': 580  # kcal/day
    }
}

# Example function to get the appropriate user profile based on calorie needs
def get_profile(calorie_target):
    """
    Get the appropriate dietary profile based on calorie target
    
    Args:
        calorie_target: The target daily calorie intake
        
    Returns:
        The dietary profile dictionary for that calorie level
    """
    # Find the closest calorie level that doesn't exceed the target
    available_levels = sorted(dietary_profiles.keys())
    
    for level in available_levels:
        if level >= calorie_target:
            return dietary_profiles[level]
    
    # If target exceeds all available levels, return the highest
    return dietary_profiles[available_levels[-1]]