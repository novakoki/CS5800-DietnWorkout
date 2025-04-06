class UserProfile:
    def __init__(self, age, gender, weight_kg, height_cm, goal, activity_level,
                 dietary_restrictions=None, fitness_level="beginner", available_equipment=None):
        self.age = age
        self.gender = gender
        self.weight_kg = weight_kg
        self.height_cm = height_cm
        self.goal = goal
        self.activity_level = activity_level
        self.dietary_restrictions = dietary_restrictions or []
        self.fitness_level = fitness_level
        self.available_equipment = available_equipment or []

    def calculate_bmr(self):
        if self.gender == "male":
            bmr = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age + 5
        else:
            bmr = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age - 161
        return bmr

    def daily_calories(self):
        multiplier = {
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725
        }.get(self.activity_level, 1.55)

        bmr = self.calculate_bmr()
        maintenance = bmr * multiplier

        if self.goal == "weight_loss":
            return maintenance - 500
        elif self.goal == "muscle_gain":
            return maintenance + 300
        else:
            return maintenance

    def summary(self):
        return {
            "BMR": self.calculate_bmr(),
            "Daily Calorie Target": self.daily_calories(),
            "Fitness Level": self.fitness_level,
            "Equipment": self.available_equipment
        }
