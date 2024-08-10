import numpy as np
from hireme.ml_utils import check_job_suitability

# Define the simple classes for testing
class Skill:
    def __init__(self, skill_name, experience):
        self.skill_name = skill_name
        self.experience = experience

class User:
    def __init__(self, skills):
        self.skill_set = skills

class JobAnnouncement:
    def __init__(self, main_skill, experience):
        self.main_skill = main_skill
        self.experience = experience

# Create test data
user_skills = [
    Skill("Front End Developer", 3),
    Skill("UX/UI Designer", 2)
]

user = User(user_skills)
job_announcement = JobAnnouncement("Front End Developer", 3)

# Run the function with test data
suitability = check_job_suitability(job_announcement, user)
print("Final Suitability Score:", suitability)
