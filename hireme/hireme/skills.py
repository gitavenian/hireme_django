
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

def find_matching_skill(job_title, skill_keywords):
    all_skills = [skill for sublist in skills.values() for skill in sublist]
    job_title_lower = job_title.lower()
    main_skill = None

    if not skill_keywords:
        print("Warning: Skill keywords dictionary is empty.")
        return 'General Skill'

    for skill in all_skills:
        skill_lower = skill.lower()
        if skill_lower in job_title_lower:
            main_skill = skill
            print(f"Direct match found: {main_skill} for job title: {job_title}")
            break

        for key, variations in skill_keywords.items():
            if key.lower() in skill_lower:
                if any(variant.lower() in job_title_lower for variant in variations):
                    main_skill = skill
                    print(f"Keyword match found: {main_skill} for job title: {job_title} using {variations}")
                    break
        if main_skill:
            break

    if not main_skill:
        main_skill = 'General Skill'
        print(f"No match found, defaulting to: {main_skill}")

    return main_skill
