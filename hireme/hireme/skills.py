
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
skill_keywords = {
    'Developer': ['developer', 'development'],
    'Engineer': ['engineer', 'engineering'],
    'Designer': ['designer', 'designing'],
    'Architect': ['architect', 'architecture'],
    'Manager': ['manager', 'management'],
    'Coach': ['coach', 'coaching'],
    'Trainer': ['trainer', 'training'],
    'Instructor': ['instructor', 'instruction'],
    'Analyst': ['analyst', 'analysis'],
    'Technician': ['technician', 'technical'],
    'Therapist': ['therapist', 'therapy'],
    'Chef': ['chef', 'cooking', 'culinary'],
    'Waitor': ['waitor', 'waiter', 'waiting', 'waitstaff'],
    'Guide': ['guide', 'guiding'],
    'Planner': ['planner', 'planning'],
    'Doctor': ['doctor', 'medical'],
    'Nurse': ['nurse', 'nursing'],
    'Pharmacist': ['pharmacist', 'pharmacy'],
    'Veterinarian': ['veterinarian', 'veterinary'],
    'Dentist': ['dentist', 'dentistry'],
    'Artist': ['artist', 'artistic'],
    'Jeweler': ['jeweler', 'jeweller', 'jewelry'],
    'Barber': ['barber', 'barbering', 'hairdresser'],
    'Writer': ['writer', 'writing'],
    'Machinist': ['machinist', 'machinery'],
    'Electrician': ['electrician', 'electrical'],
    'Pilot': ['pilot', 'piloting'],
    'Translator': ['translator', 'translation'],
    'Professor': ['professor', 'professorial', 'academic'],
    'Teacher': ['teacher', 'teaching', 'education'],
    'Lawyer': ['lawyer', 'legal'],
    'Judge': ['judge', 'judicial'],
    'Florist': ['florist', 'floral'],
}

def find_matching_skill(job_title):
    all_skills = [skill for sublist in skills.values() for skill in sublist]

    # Convert the job title to lower case for case-insensitive matching
    job_title_lower = job_title.lower()

    # Variable to hold the matched skill
    main_skill = None

    # Loop through all skills to find a match based on the keyword variations
    for skill in all_skills:
        skill_lower = skill.lower()
        # Check if any keyword related to the skill is in the job title
        for key, variations in skill_keywords.items():
            if key.lower() in skill_lower and any(variant in job_title_lower for variant in variations):
                main_skill = skill
                break
        if main_skill:
            break

    # Default to 'General Skill' if no match is found
    if not main_skill:
        main_skill = 'General Skill'

    print(f"Job Title: '{job_title}', Matched Skill: '{main_skill}'")  # Debugging output to trace matching
    return main_skill