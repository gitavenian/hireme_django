import pandas as pd
import random

print("Script started")

# Define the skills categorized by fields
skills = {
    "IT and Engineering": [
        "Front End Developer", "Back End Developer", "Full Stack Developer", "Flutter Developer", 
        "AI Development", "UX/UI Designer", "Graphic Designer", "IT Engineer", "Solutions Architect",
        "Game Developer", "Mechanical Engineer", "Electrical Engineer", "Civil Engineer",
        "Chemical Engineer", "Biomedical Engineer", "Environmental Engineer"
    ],
    "Healthcare": [
        "Medical Doctor", "Nurse", "Pharmacist", "Physiotherapist", "Veterinarian", "Dentist",
        "Lab Technician"
    ],
    "Arts and Entertainment": [
        "Jeweler", "Makeup Artist", "Hairdresser / Barber", "Artist"
    ],
    "Hospitality and Services": [
        "Chef", "Barista / Waitor", "Tour Guide", "Event Planner", "Hotel / Restaurant Manager"
    ],
    "Sports and Fitness": [
        "Fitness Coach", "Personal Trainer", "Yoga Instructor", "Sports Therapist"
    ],
    "Marketing and Management": [
        "Marketing Manager", "Manager", "Project Manager", "Business Analyst", "Human Resources Manager"
    ],
    "Law and Order": [
        "Lawyer", "Judge"
    ],
    "Academia and Education": [
        "Teacher", "Professor"
    ],
    "Miscellaneous": [
        "Cybersecurity Analyst", "Technical Writer", "Florist", "Machinist", "Electrician", "Pilot",
        "Translator"
    ]
}

print("Skills defined")

# Flatten the skills list
all_skills = [skill for sublist in skills.values() for skill in sublist]

# Function to calculate user points
def calculate_points(main_skill, soft_skill, user_skills, years_experience):
    points = 0
    if main_skill in user_skills:
        points += 2
    if soft_skill in user_skills:
        points += 1
    points += (years_experience * (years_experience + 1)) // 2
    return points

print("Points calculation function defined")

# Generate dataset
data = []
for i in range(1000):
    print(f"Generating record {i}")
    # Randomly select a field of work
    field = random.choice(list(skills.keys()))
    field_skills = skills[field]
    
    main_required_skill = random.choice(field_skills)
    print(f"Main required skill: {main_required_skill}")
    
    if len(field_skills) > 1:
        # Ensure soft_required_skill is not the same as main_required_skill
        soft_required_skill = random.choice(field_skills)
        while soft_required_skill == main_required_skill:
            print(f"soft_required_skill {soft_required_skill} is same as main_required_skill {main_required_skill}, selecting again")
            soft_required_skill = random.choice(field_skills)
    else:
        soft_required_skill = main_required_skill
    print(f"Soft required skill: {soft_required_skill}")
    
    # User skills
    user_skill1 = main_required_skill
    user_skill2 = random.choice(all_skills)
    
    # Ensure user_skill1 and user_skill2 are not the same
    while user_skill1 == user_skill2:
        user_skill2 = random.choice(all_skills)
    print(f"User skills: {user_skill1}, {user_skill2}")
    
    years_experience = random.randint(1, 5)
    print(f"Years experience: {years_experience}")
    user_skills = {user_skill1, user_skill2}
    user_points = calculate_points(main_required_skill, soft_required_skill, user_skills, years_experience)
    print(f"User points: {user_points}")
    
    data.append([
        main_required_skill, soft_required_skill,
        user_skill1, user_skill2,
        years_experience, user_points
    ])

print("Dataset generated")

# Create DataFrame
df = pd.DataFrame(data, columns=[
    'main_required_skill', 'soft_required_skill', 'user_skill1',
    'user_skill2', 'years_experience', 'user_points'
])

print("DataFrame created")

# Save to CSV
df.to_csv("generated_dataset.csv", index=False)

print("Dataset saved to generated_dataset.csv")
